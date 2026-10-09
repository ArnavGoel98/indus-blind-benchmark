"""Design the allograph merger on DEVELOPMENT corpora only (seeds 90-91; never used in any sweep).
Usage: python scripts/v2/allograph_dev.py  -> reports/v2/allograph/dev.md"""
from __future__ import annotations

import itertools
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from ibdb.paths import ensure, reports_dir  # noqa: E402

OUT = ensure(reports_dir() / "v2" / "allograph")
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
US = [0.3, 1.0, 1.8]
GRID = [(m, r) for m in (3, 5, 10) for r in (None, 0.8, 0.6, 0.4)]


def one(args):
    lang, st, seed, u = args
    from allograph_common import sweep_corpus
    from ibdb.methods.allograph import AllographMerger, merge_scores
    from ibdb.sensitivity import PoolExhausted, SensJob
    try:
        c, key, allo, _ = sweep_corpus(SensJob(lang, st, seed, 0.3, 0), u)
    except PoolExhausted:
        return []
    texts = [t.tolist() for t in c.logical()]
    out = []
    for m, a in GRID:
        rep = AllographMerger(min_count=m, alpha=0.05, max_ratio=a).fit(texts)
        out.append({"lang": lang, "script": st, "seed": seed, "u": u, "min_count": m, "max_ratio": a,
                    **merge_scores(rep, allo, key.sign_values)})
    return out


def main():
    jobs = list(itertools.product(LANGS, SCRIPTS, (90, 91), US))
    with ProcessPoolExecutor(int(os.environ.get("WORKERS", "4")), mp_context=get_context("spawn")) as ex:
        rows = [r for rs in ex.map(one, jobs) for r in rs]
    (OUT / "dev2_records.json").write_text(json.dumps(rows))
    L = ["# Allograph merger: development corpora (seeds 90-91)", "",
         "| min_count | max_ratio | precision | recall | value-consistent | signs -> groups (true groups) |", "|---|---|---|---|---|---|"]
    for m, a in GRID:
        g = [r for r in rows if r["min_count"] == m and r["max_ratio"] == a]
        L.append(f"| {m} | {a} | {np.mean([r['precision'] for r in g]):.3f} | {np.mean([r['recall'] for r in g]):.3f} | "
                 f"{np.mean([r['value_consistent'] for r in g]):.3f} | {np.mean([r['n_signs'] for r in g]):.0f} -> "
                 f"{np.mean([r['n_pred_groups'] for r in g]):.0f} ({np.mean([r['n_true_groups'] for r in g]):.0f}) |")
    L += ["", "By script type (precision / recall):", "", "| min_count | max_ratio | " + " | ".join(SCRIPTS) + " |", "|---|---|" + "---|" * len(SCRIPTS)]
    for m, a in GRID:
        cells = []
        for st in SCRIPTS:
            g = [r for r in rows if r["min_count"] == m and r["max_ratio"] == a and r["script"] == st]
            cells.append(f"{np.mean([r['precision'] for r in g]):.2f} / {np.mean([r['recall'] for r in g]):.2f}")
        L.append(f"| {m} | {a} | " + " | ".join(cells) + " |")
    (OUT / "dev2.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
