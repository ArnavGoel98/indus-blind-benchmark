"""v2 final run on the confirmatory seeds 6-11 (pre-registration entry 12; docs/v2_final_run_readings.md).

One job per corpus (Indus point, 2,906 texts, mean length 4.6; samplers A and B; five languages; four
script types; seeds 6-11: 240 corpora):
- Tasks C and D, tiers `related_*` and `candidates_*` for `harsh` and every real relative (cd_v2), scored
  with the entry-10 scorer; raw and reachable ceilings (entry 11) for every relative;
- the v1 sister on the same corpus with the frozen v1 `evaluate.run_job` (Indus point, `related` and
  `candidates`), scored before the cognate step;
- C1 unrelated references and C2 floors for the real relatives; C3 (10 restarts) on seeds 6-8.
Every prediction is stored. C4 (`--c4`) reruns the 24 corpora of the readings document, section 5.

The final run and C4 refuse to start unless the tag `frozen-v2.1` exists and every file outside
reports/ and docs/ (and the entry-8 controls module it calls) equals it, with no untracked code files.

Usage (repository root):
  python scripts/v2/final_v2.py --dev OUTDIR [--limit N]   # pipeline check: seed 90, sampler A, 1 restart (not a result)
  python scripts/v2/final_v2.py [--workers 4]              # final run -> runs/results/v2_final/
  python scripts/v2/final_v2.py --c4 [--workers 4]         # determinism rerun -> runs/results/v2_final_c4/
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

CONTROLS = "reports/v2/cd/analysis/controls.py"     # the entry-8 floor and diagnostics; guarded with the code
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / Path(CONTROLS).parent))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import: content split, as every v2 run)
import controls  # noqa: E402
from ibdb import evaluate  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import LANGUAGES, make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.knowledge import build_reference  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import FrequencyRankBaseline, KnightEM  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

TAG = "frozen-v2.1"
SEEDS = (6, 7, 8, 9, 10, 11)
C3_SEEDS = (6, 7, 8)
C4_JOBS = [(lang, st, 6, smp) for lang in ("latin", "tamil", "finnish") for st in cd_v2.SCRIPTS for smp in cd_v2.SAMPLERS]
UNREL = {"latin": ["tamil", "finnish"], "tamil": ["latin", "finnish"], "finnish": ["latin", "tamil"]}
ORDER = {"tamil": 0, "latin": 1, "finnish": 2, "sumerian": 3, "sanskrit": 4}   # longest jobs first
CAP = KnightEM().max_units


def check_final() -> str:
    """Refuse unless all code, data, tests and config equal the frozen-v2.1 tag; return HEAD."""
    tag = subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{TAG}"], capture_output=True, text=True)
    if tag.returncode != 0:
        raise SystemExit(f"final run refused: tag {TAG} is missing")
    same = subprocess.run(["git", "diff", "--quiet", TAG, "--", ".", ":(exclude)reports", ":(exclude)docs"]).returncode == 0 \
        and subprocess.run(["git", "diff", "--quiet", TAG, "--", CONTROLS]).returncode == 0
    untracked = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", "src", "scripts", "config",
                                "tests"], capture_output=True, text=True).stdout.strip()
    if not same or untracked:
        raise SystemExit(f"final run refused: the working tree differs from {TAG} outside reports/ and docs/ "
                         f"(or in {CONTROLS})\n{untracked}")
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def _sv(p) -> dict:
    return {str(k): v for k, v in (p.sign_values or {}).items()}


def job(args) -> tuple[dict, dict, dict]:
    lang, st, seed, sampler, restarts, c3 = args
    t0 = time.time()
    gv = cd_v2.SAMPLERS[sampler]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    others = [build_reference(o, st, False, seed, spec.logogram_vocab) for o in LANGUAGES if o != lang]
    ident = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler}
    rec = {**ident, "family": key.family, "n_tokens": corpus.n_tokens, "tiers": {}, "ceiling": {}, "floor": {},
           "unrelated": {}, "budget": {}}
    preds = {**ident, "tiers": {}, "unrelated": {}, "budget": {}}
    golds, refs = {}, {}
    for rname, rel in cd_v2.relatives_for(lang, seed).items():
        ref = RC.reference(rel, st, lang, spec.logogram_vocab)
        gold = RC.Gold(rel, lang, st, logos)
        refs[rname], golds[rname] = ref, gold
        rec["ceiling"][rname] = {"raw": RC.score({}, key, logical, gold)["recoverable"],
                                 "reachable": RC.reachable(ref, key, gold, CAP)}
        for tier, rl in ((f"related_{rname}", [ref]), (f"candidates_{rname}", [ref] + others)):
            kn = Knowledge(tier.split("_")[0], st, rl)
            rec["tiers"][tier], preds["tiers"][tier] = {}, {}
            for M in cd_v2.D_METHODS:
                m = M(restarts=restarts, iterations=60) if issubclass(M, KnightEM) else M()
                p = m.analyze(corpus, kn)
                rec["tiers"][tier][m.name] = {"reference": p.extra.get("reference"), "family": p.family,
                                              "family_correct": p.family == key.family,
                                              **RC.score(p.sign_values, key, logical, gold)}
                preds["tiers"][tier][m.name] = _sv(p)
    real = {n: g for n, g in golds.items() if n.startswith("real:")}
    for n, g in real.items():
        rec["floor"][n] = controls.floor(key, logical, g)
    for u in (UNREL.get(lang, []) if real else []):
        kn = Knowledge("related", st, [build_reference(u, st, False, seed, spec.logogram_vocab)])
        rec["unrelated"][u], preds["unrelated"][u] = {}, {}
        for M in (KnightEM, FrequencyRankBaseline):
            m = M(restarts=restarts, iterations=60) if M is KnightEM else M()
            p = m.analyze(corpus, kn)
            rec["unrelated"][u][m.name] = {"diag": controls.diag(p.sign_values, corpus),
                                          **{n: RC.score(p.sign_values, key, logical, g) for n, g in real.items()}}
            preds["unrelated"][u][m.name] = _sv(p)
    if c3:
        for n, g in real.items():
            p = KnightEM(restarts=10, iterations=60).analyze(corpus, Knowledge("related", st, [refs[n]]))
            rec["budget"][n] = {"10": {"diag": controls.diag(p.sign_values, corpus), **RC.score(p.sign_values, key, logical, g)}}
            preds["budget"][n] = _sv(p)
    v1 = evaluate.run_job(evaluate.Job("size", lang, st, seed, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, tiers=("related", "candidates")),
                          restarts, 60, gv)
    assert v1["sister_version"] == "v2" and v1["stats"]["n_tokens"] == sum(len(t) for t in logical) \
        and v1["stats"]["n_texts"] == len(logical), "the v1 sister's corpus differs"
    rec["v1_sister"] = {t: {m: {k: x.get(k) for k in ("reference", "family", "family_correct", "token_acc",
                                                        "token_acc_before_cognate")}
                            for m, x in v1["CD"][t].items() if not m.startswith("_")} for t in ("related", "candidates")}
    rec["seconds"] = time.time() - t0
    return rec, preds, {**ident, **v1}


def _run(jobs: list, out: Path, head: str, workers: int) -> None:
    path, ppath, vpath = out / "records.jsonl", out / "predictions.jsonl", out / "v1_sister.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = sorted((j for j in jobs if j[:4] not in done), key=lambda j: (ORDER[j[0]], j[2], j[3], j[1]))
    print(f"[final_v2] HEAD {head}; {len(jobs)} corpora, {len(todo)} to do -> {out}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(job, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r, pr, v1 = f.result()
                r["commit"] = head
                with open(ppath, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(pr, ensure_ascii=False) + "\n")
                with open(vpath, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(v1, default=float, ensure_ascii=False) + "\n")
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[final_v2] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", metavar="OUTDIR", help="pipeline check only: seed 90, sampler A, 1 restart")
    ap.add_argument("--limit", type=int, help="--dev only: first N corpora")
    ap.add_argument("--c4", action="store_true", help="determinism rerun of the 24 C4 corpora")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.dev:
        jobs = [(lang, st, 90, "A", 1, True) for lang in sorted(LANGUAGES, key=ORDER.get) for st in cd_v2.SCRIPTS][:a.limit]
        out = Path(a.dev)
        out.mkdir(parents=True, exist_ok=True)
        _run(jobs, out, "dev", a.workers)
        return
    head = check_final()
    if a.c4:
        jobs = [(*j, 3, j[2] in C3_SEEDS and j[0] in UNREL) for j in C4_JOBS]
        _run(jobs, ensure(runs_dir() / "results" / "v2_final_c4"), head, a.workers)
        return
    jobs = [(lang, st, s, smp, 3, s in C3_SEEDS and lang in UNREL)
            for lang in LANGUAGES for st in cd_v2.SCRIPTS for s in SEEDS for smp in cd_v2.SAMPLERS]
    _run(jobs, ensure(runs_dir() / "results" / "v2_final"), head, a.workers)


if __name__ == "__main__":
    main()
