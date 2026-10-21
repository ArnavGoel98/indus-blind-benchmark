"""Pre-registration entry 8: controls for reading the v2 Task D results. Calls only frozen functions.

C1 unrelated reference (related tier, one unrelated v1 language; revised EM and frequency rank), scored
   against each real relative's gold; C2 constant-prediction floor per gold; C3 revised EM with 10
   restarts against 3 (seeds 0-2); C4 the 3-restart rerun, compared later with the frozen-run record.
Diagnostics: distinct predicted units and the token share of the most common predicted unit.
Usage (repository root): python reports/v2/cd/analysis/controls.py [--workers 4]
                         python reports/v2/cd/analysis/controls.py --dev OUTDIR   (seed 90 only; not a result)
Writes runs/results/v2_controls/records.jsonl (resumable).
"""
import argparse
import json
import sys
import time
import traceback
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import, as for the main run)
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.knowledge import build_reference  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import FrequencyRankBaseline, KnightEM  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

UNREL = {"tamil": ["latin", "finnish"], "latin": ["tamil", "finnish"]}
LANGS = ("latin", "tamil")


def diag(vals: dict | None, corpus) -> dict:
    vals = vals or {}
    tok = Counter(int(s) for t in corpus.texts for s in t.tolist())
    pred = Counter()
    for s, n in tok.items():
        if vals.get(s) is not None:
            pred[vals[s]] += n
    total = sum(tok.values())
    return {"n_distinct": len(set(vals.values())),
            "top_unit_share": pred.most_common(1)[0][1] / total if pred else 0.0}


def floor(key, logical, gold) -> float:
    """Strict score of the best single-unit answer: the largest token share of one regular reflex."""
    c, n = Counter(), 0
    for t, vals in zip(logical, key.token_values):
        for _s, v in zip(t, vals):
            n += 1
            r = gold._value(v)[0]
            if r is not None:
                c[r] += 1
    return c.most_common(1)[0][1] / n if c else 0.0


def run_control(job) -> dict:
    lang, st, seed, sampler, budget = job
    t0 = time.time()
    gv = cd_v2.SAMPLERS[sampler]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    rels = cd_v2.relatives_for(lang, seed)
    golds = {n: RC.Gold(r, lang, st, logos) for n, r in rels.items() if n.startswith("real:")}
    rec = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler,
           "floor": {n: floor(key, logical, g) for n, g in golds.items()}, "unrelated": {}, "budget": {}}
    for u in UNREL[lang]:
        kn = Knowledge("related", st, [build_reference(u, st, False, seed, spec.logogram_vocab)])
        rec["unrelated"][u] = {}
        for M in (KnightEM, FrequencyRankBaseline):
            m = M(restarts=3, iterations=60) if M is KnightEM else M()
            p = m.analyze(corpus, kn)
            rec["unrelated"][u][m.name] = {"diag": diag(p.sign_values, corpus),
                                          **{n: RC.score(p.sign_values, key, logical, g) for n, g in golds.items()}}
    if budget:
        for n, rel in rels.items():
            kn = Knowledge("related", st, [RC.reference(rel, st, lang, spec.logogram_vocab)])
            gold = RC.Gold(rel, lang, st, logos)
            rec["budget"][n] = {}
            for restarts in (3, 10):
                p = KnightEM(restarts=restarts, iterations=60).analyze(corpus, kn)
                rec["budget"][n][str(restarts)] = {"diag": diag(p.sign_values, corpus),
                                                   **RC.score(p.sign_values, key, logical, gold)}
    rec["seconds"] = time.time() - t0
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dev", metavar="OUTDIR", help="pipeline check only: seed 90, sampler A (not a result)")
    a = ap.parse_args()
    if a.dev:
        jobs = [(lang, st, 90, "A", True) for lang in LANGS for st in ("alphabetic", "syllabic")]
        path = Path(a.dev) / "controls_dev.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        cd_v2.check_frozen()
        jobs = [(lang, st, s, smp, s in (0, 1, 2)) for smp in cd_v2.SAMPLERS for s in range(6)
                for lang in LANGS for st in cd_v2.SCRIPTS]
        path = ensure(runs_dir() / "results" / "v2_controls") / "records.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j[:4] not in done]
    # Longest jobs first (the budget runs), so the pool finishes evenly.
    todo.sort(key=lambda j: (not j[4], j[1] != "logographic"))
    print(f"[v2_controls] {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(run_control, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r = f.result()
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[v2_controls] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}",
                  flush=True)


if __name__ == "__main__":
    main()
