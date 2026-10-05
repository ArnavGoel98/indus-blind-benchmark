"""Genre check report: Sumerian seal-only corpora vs Sumerian corpora from the full source (Indus point,
seeds 0-2). Analysis of saved records only. Primary = original (frozen) rule, before the cognate step.
Usage: python scripts/sumerian_seal_report.py > reports/sister_v2/sumerian_seal_genre_check.md
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from sister_compare import load, point_keys  # noqa: E402

ORIG, REV = "knight2006_em_original", "knight2006_em"


def acc(d, before):
    return d.get("token_acc_before_cognate", d["token_acc"]) if before else d["token_acc"]


def summ(recs, tier, m, before):
    xs = [acc(r["CD"][tier][m], before) for r in recs if tier in r["CD"]]
    return f"{100*np.mean(xs):.1f}% (max {100*max(xs):.1f}%)" if xs else "n/a"


def main():
    seal = [json.loads(l) for l in open("runs/results/sumerian_seal/records.jsonl")]
    seal = [r for r in seal if "error" not in r]
    print("# Genre check: Sumerian seal inscriptions only\n")
    print("Hidden corpus AND synthetic sister built only from the 19,076 Ur III seal inscriptions in the CDLI "
          "dump (sister-v2 content split); other candidate languages unchanged. Indus point, seeds 0-2, 4 script "
          "types, methods frozen. Full-source Sumerian = the same jobs in the sister-v2 runs (`none` tier from the "
          "frozen-v1 runs, which do not use the sister). 12 corpora per generator and genre; no intervals (one "
          "language).\n")
    for gv, full_name, none_name in (("v1", "sister_v2_main", "full"), ("v2", "sister_v2_gen2", "generator_v2")):
        s = [r for r in seal if r["generator_version"] == gv]
        f = [r for k, r in load(full_name).items() if k[1] == "sumerian" and k in point_keys(load(full_name), "size", 2906, 4.6)]
        fn = [r for k, r in load(none_name).items() if k[1] == "sumerian" and k[0] == "size" and k[4] == 2906]
        print(f"## Generator {gv} ({len(s)} seal-only corpora, {len(f)} full-source)\n")
        print("| Tier and score | Seal only | Full source |")
        print("|---|---|---|")
        for tier, m, bf, lab in (("related", ORIG, True, "related, primary"), ("related", ORIG, False, "related, with oracle sound correspondences"),
                                 ("candidates", ORIG, True, "candidates, primary"), ("candidates", ORIG, False, "candidates, with oracle sound correspondences"),
                                 ("candidates", REV, True, "candidates, revised rule (post hoc), before cognate"),
                                 ("none", ORIG, False, "none, original rule"), ("none", REV, False, "none, revised rule")):
            src = fn if tier == "none" else f
            print(f"| {lab} | {summ(s, tier, m, bf)} | {summ(src, tier, m, bf)} |")
        ch = [r["CD"]["candidates"][ORIG]["reference"] for r in s]
        print(f"\nOriginal rule, candidates tier, references chosen (seal only): "
              f"{ {x: ch.count(x) for x in sorted(set(ch))} }\n")
        st = lambda rs, k: np.mean([r["stats"][k] for r in rs])  # noqa: E731
        print("| Corpus statistic | Seal only | Full source |")
        print("|---|---|---|")
        for k in ("sign_inventory", "duplicate_text_fraction", "mean_length", "coverage80_signs", "beginners80_signs"):
            print(f"| {k} | {st(s, k):.3g} | {st(f, k):.3g} |")
        ok = np.mean([all(r["calibration"].values()) for r in s])
        print(f"\nSeal-only corpora meeting every calibration target: {100*ok:.0f}% (knobs were calibrated on the full source).\n")


if __name__ == "__main__":
    main()
