"""v2: re-score the sensitivity sweep (sister-v2 profile) with allograph merging before Task D.

For every valid record of `sensitivity_sister_v2`, rebuild its corpus exactly (same u, same pool and
assembly; checked against the stored statistics), then run the frozen original-rule EM
(knight2006_em_original, the primary score, before the cognate step) in both tiers under three
conditions:
  none    - no merging (recomputed here; must equal the stored score)
  learned - AllographMerger (v2 method, parameters fixed on development corpora)
  oracle  - merge exactly the hidden allograph groups (upper bound; uses the key)
Merged predictions are expanded back to every original sign and scored against the original key.
Merge accuracy (pairwise precision/recall vs the hidden allograph map) is recorded for `learned`.

Usage: WORKERS=4 python scripts/v2/allograph_sweep.py   (resumable)
Writes runs/results/v2_allograph_sweep/records.jsonl
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context

sys.path.insert(0, os.path.dirname(__file__))

PROFILE = "sensitivity_sister_v2"
MERGER = {"min_count": 10, "alpha": 0.05, "max_ratio": 0.6}   # fixed on development corpora before this run


def run_one(rec: dict) -> dict:
    os.environ["IBDB_SISTER_VERSION"] = "v2"
    for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ.setdefault(v, "1")
    from allograph_common import sweep_corpus
    from ibdb import config
    from ibdb.corpus import Corpus
    from ibdb.evaluate import token_acc_before_cognate
    from ibdb.knowledge import knowledge_for
    from ibdb.methods.allograph import AllographMerger, expand_values, merge_scores
    from ibdb.methods.decipher import KnightEMOriginal
    from ibdb.scoring import score_sign_values
    from ibdb.sensitivity import SensJob
    from ibdb.stats import corpus_stats
    import numpy as np

    t0 = time.time()
    j = rec["job"]
    job = SensJob(j["source"], j["script_type"], j["seed"], j["dup"], j["inventory"], j["n_texts"], j["mean_length"],
                  tuple(j["tiers"]))
    corpus, key, allo, spec = sweep_corpus(job, rec["u"])
    logical = [t.tolist() for t in corpus.logical()]
    st = corpus_stats(logical, config.targets()["targets"], seed=job.seed)
    match = all(st[k] == rec["stats"][k] for k in ("n_tokens", "sign_inventory", "duplicate_text_fraction"))
    out = {"job": j, "u": rec["u"], "regenerated_matches_record": match, "inventory": st["sign_inventory"],
           "merge": {}, "D": {}}
    learned = AllographMerger(**MERGER).fit(logical)
    oracle = {s: s for s in {x for t in logical for x in t}}
    for base, grp in allo.items():
        for s in grp:
            if s in oracle:
                oracle[s] = base
    out["merge"]["learned"] = {**merge_scores(learned, allo, key.sign_values), "params": MERGER}
    out["merge"]["oracle"] = {"n_pred_groups": len(set(oracle.values()))}
    conds = {"none": None, "learned": learned, "oracle": oracle}
    for tier in job.tiers:
        kn = knowledge_for(job.source, job.script_type, tier, job.seed, logogram_vocab=spec.logogram_vocab)
        out["D"][tier] = {}
        for cname, rep in conds.items():
            if rep is None:
                c = corpus
            else:
                c = Corpus(corpus.corpus_id, [np.array([rep[int(x)] for x in t], dtype=np.int64) for t in corpus.texts],
                           corpus.direction, dict(corpus.meta))
            p = KnightEMOriginal(restarts=3, iterations=60).analyze(c, kn)
            if rep is not None:
                p.sign_values = expand_values(p.sign_values, rep)
            s = score_sign_values(p.sign_values, key, logical)
            bc = token_acc_before_cognate(p, kn, key, logical)
            out["D"][tier][cname] = {"token_acc": s["token_acc"], "primary": bc if bc is not None else s["token_acc"],
                                     "reference": p.extra.get("reference")}
        stored = rec["CD"][tier]["knight2006_em_original"]
        out["D"][tier]["stored_primary"] = stored.get("token_acc_before_cognate", stored["token_acc"])
    out["seconds"] = time.time() - t0
    return out


def main() -> None:
    from ibdb.paths import ensure, runs_dir
    from ibdb.sensitivity import load_records, valid
    path = ensure(runs_dir() / "results" / "v2_allograph_sweep") / "records.jsonl"
    done = set()
    if path.exists():
        done = {json.dumps(json.loads(l)["job"], sort_keys=True) for l in path.read_text().splitlines() if l.strip()
                and "error" not in json.loads(l)}
    recs = [r for r in load_records(PROFILE) if r.get("status") == "ok" and valid(r)]
    todo = [r for r in recs if json.dumps(r["job"], sort_keys=True) not in done]
    print(f"[allograph_sweep] {len(recs)} valid records, {len(todo)} to do", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(int(os.environ.get("WORKERS", "4")), mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(run_one, r): r for r in todo}
        for i, f in enumerate(as_completed(futs), 1):
            try:
                row = f.result()
            except Exception:  # noqa: BLE001 - recorded, not hidden
                row = {"job": futs[f]["job"], "error": traceback.format_exc()[-800:]}
            with open(path, "a") as fh:
                fh.write(json.dumps(row, default=float) + "\n")
            if i % 25 == 0:
                el = time.time() - t0
                print(f"[allograph_sweep] {i}/{len(todo)} {el:.0f}s eta {el / i * (len(todo) - i) / 3600:.2f}h", flush=True)


if __name__ == "__main__":
    main()
