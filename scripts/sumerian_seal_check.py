"""Genre check: Sumerian corpora built ONLY from real Ur III seal inscriptions (CDLI @seal clauses).

Both halves (hidden corpus and synthetic sister) are restricted to seal clauses; the other candidate
languages are unchanged. Indus point, generators v1 and v2, seeds 0-2, sister-v2 split, methods frozen.
Runs in one process (restricts the cached Sumerian segments in place), so it is not a profile.
Usage: IBDB_SISTER_VERSION=v2 python scripts/sumerian_seal_check.py
"""
import json
import os
from collections import Counter

import numpy as np

from ibdb.evaluate import Job, run_job
from ibdb.generator.build import _segments

assert os.environ.get("IBDB_SISTER_VERSION") == "v2"
OUT = "runs/results/sumerian_seal/records.jsonl"


def restrict_to_seals():
    d = _segments("sumerian")
    d["clauses"] = [c for c in d["clauses"] if c[0] == "seal"]
    freq = Counter(w for _, ids in d["clauses"] for w in ids)
    n = len(d["words"])
    f = np.array([freq.get(i, 0) for i in range(n)], dtype=np.float64)
    order = np.argsort(-f, kind="stable")
    rank = np.empty(n, dtype=np.int64)
    rank[order] = np.arange(1, n + 1)
    d["_rank"], d["_logf"] = rank, np.log((f + 0.5) / f.sum())
    return len(d["clauses"])


def main():
    print("seal clauses:", restrict_to_seals(), flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    done = set()
    if os.path.exists(OUT):
        done = {json.dumps([r["job"]["script_type"], r["job"]["seed"], r["generator_version"]]) for r in map(json.loads, open(OUT))}
    for gv in ("v1", "v2"):
        for st in ("logographic", "syllabic", "logosyllabic", "alphabetic"):
            for seed in (0, 1, 2):
                if json.dumps([st, seed, gv]) in done:
                    continue
                job = Job("size", "sumerian", st, seed, 2906, 4.6, tiers=("related", "candidates", "none"))
                try:
                    rec = run_job(job, 3, 60, gv)
                except Exception as e:  # noqa: BLE001
                    rec = {"job": job.__dict__, "generator_version": gv, "error": repr(e)}
                rec["genre"] = "seal_only"
                with open(OUT, "a") as fh:
                    fh.write(json.dumps(rec, default=float) + "\n")
                print(gv, st, seed, "error" in rec, flush=True)


if __name__ == "__main__":
    main()
