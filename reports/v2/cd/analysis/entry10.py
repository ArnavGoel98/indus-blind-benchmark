"""Pre-registration entry 10: rerun Tasks C/D and the controls for the pairs with no-source gold rows.

Finnish (Estonian) first, then Old Tamil (Malayalam, Kannada): seeds 0-5, samplers A and B, four script
types. For each corpus: `related_real` and `candidates_real` tiers (the entry-6 methods and budget), C1
unrelated references (entries 8 and 9), C2 floors, and for Old Tamil on seeds 0-2 except alphabetic C3
(revised EM, 10 restarts). Every prediction is scored with the old gold map (no-source rows as lost) and
the new one (unknown); the old scores are later compared with the archived records. Predictions are
stored, so later scoring changes need no rerun.

Refuses to run unless every file outside the data, tests, reports/ and docs/ equals `frozen-v2`, except
the v2 harness files named in entry 10, which must be committed.
Usage (repository root): python reports/v2/cd/analysis/entry10.py [--workers 4]
Writes runs/results/v2_e10/records.jsonl and predictions.jsonl (resumable).
"""
import argparse
import json
import subprocess
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import)
import controls  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.data.gold import old_semantics  # noqa: E402
from ibdb.generator.build import LANGUAGES, make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.knowledge import build_reference  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import FrequencyRankBaseline, KnightEM  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

HARNESS = {"src/ibdb/relative_cd.py", "src/ibdb/yardsticks.py", "scripts/v2/real_relatives_verbatim.py",
           "scripts/v2/real_relatives_yardsticks.py", "scripts/v2/cd_v2_summary.py"}
UNREL = {"finnish": ["latin", "tamil"], "tamil": ["latin", "finnish"]}
REAL = {"finnish": ["estonian"], "tamil": ["malayalam", "kannada"]}


def check_guard() -> str:
    changed = set(subprocess.run(["git", "diff", "--name-only", "frozen-v2", "--", ".", ":(exclude)src/ibdb/data",
                                  ":(exclude)reports", ":(exclude)docs", ":(exclude)tests"],
                                 capture_output=True, text=True, check=True).stdout.split())
    if not changed <= HARNESS:
        raise SystemExit(f"refused: files outside the entry-10 harness differ from frozen-v2: {sorted(changed - HARNESS)}")
    dirty = subprocess.run(["git", "status", "--porcelain", "--", *sorted(HARNESS), "src/ibdb/data"],
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        raise SystemExit(f"refused: uncommitted harness or data changes:\n{dirty}")
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def both(pred, key, logical, gn, go) -> dict:
    return {**RC.score(pred, key, logical, gn), "old": RC.score(pred, key, logical, go)}


def job(args) -> tuple[dict, dict]:
    lang, st, seed, sampler, c3 = args
    t0 = time.time()
    gv = cd_v2.SAMPLERS[sampler]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    others = [build_reference(o, st, False, seed, spec.logogram_vocab) for o in LANGUAGES if o != lang]
    rec = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler, "family": key.family,
           "n_tokens": corpus.n_tokens, "tiers": {}, "floor": {}, "unrelated": {}, "budget": {}}
    preds = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler, "tiers": {}, "unrelated": {}, "budget": {}}
    sv = lambda p: {str(k): v for k, v in (p.sign_values or {}).items()}  # noqa: E731
    golds, refs = {}, {}
    for r in REAL[lang]:
        rel = RC.real_relative(lang, r)
        rel_old = RC.Relative(rel.name, rel.family, rel.clauses, old_semantics(rel.regular), rel.attested)
        golds[f"real:{r}"] = (RC.Gold(rel, lang, st, logos), RC.Gold(rel_old, lang, st, logos))
        refs[r] = RC.reference(rel, st, lang, spec.logogram_vocab)
        gn, go = golds[f"real:{r}"]
        for tier, rl in ((f"related_real:{r}", [refs[r]]), (f"candidates_real:{r}", [refs[r]] + others)):
            kn = Knowledge(tier.split("_")[0], st, rl)
            rec["tiers"][tier], preds["tiers"][tier] = {}, {}
            for M in cd_v2.D_METHODS:
                m = M(restarts=3, iterations=60) if issubclass(M, KnightEM) else M()
                p = m.analyze(corpus, kn)
                rec["tiers"][tier][m.name] = {"reference": p.extra.get("reference"), "family": p.family,
                                              "family_correct": p.family == key.family, **both(p.sign_values, key, logical, gn, go)}
                preds["tiers"][tier][m.name] = sv(p)
        rec["floor"][f"real:{r}"] = {"new": controls.floor(key, logical, gn), "old": controls.floor(key, logical, go)}
    for u in UNREL[lang]:
        kn = Knowledge("related", st, [build_reference(u, st, False, seed, spec.logogram_vocab)])
        rec["unrelated"][u], preds["unrelated"][u] = {}, {}
        for M in (KnightEM, FrequencyRankBaseline):
            m = M(restarts=3, iterations=60) if M is KnightEM else M()
            p = m.analyze(corpus, kn)
            rec["unrelated"][u][m.name] = {"diag": controls.diag(p.sign_values, corpus),
                                          **{n: both(p.sign_values, key, logical, gn, go) for n, (gn, go) in golds.items()}}
            preds["unrelated"][u][m.name] = sv(p)
    if c3:
        for r in REAL[lang]:
            gn, go = golds[f"real:{r}"]
            p = KnightEM(restarts=10, iterations=60).analyze(corpus, Knowledge("related", st, [refs[r]]))
            rec["budget"][f"real:{r}"] = {"10": {"diag": controls.diag(p.sign_values, corpus), **both(p.sign_values, key, logical, gn, go)}}
            preds["budget"][f"real:{r}"] = sv(p)
    rec["seconds"] = time.time() - t0
    return rec, preds


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    head = check_guard()
    assert RC.has_gold("estonian")
    jobs = [(lang, st, s, smp, lang == "tamil" and s < 3 and st != "alphabetic")
            for lang in ("finnish", "tamil") for smp in cd_v2.SAMPLERS for s in range(6) for st in cd_v2.SCRIPTS]
    out = ensure(runs_dir() / "results" / "v2_e10")
    path, ppath = out / "records.jsonl", out / "predictions.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j[:4] not in done]
    print(f"[entry10] HEAD {head}; {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(job, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r, pr = f.result()
                r["commit"] = head
                with open(ppath, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(pr, ensure_ascii=False) + "\n")
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[entry10] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}", flush=True)


if __name__ == "__main__":
    main()
