"""Headline numbers restricted to logo-syllabic corpora (the most Indus-relevant script type).
Analysis of saved records only. Primary = original (frozen) rule, before the cognate step.
Usage: python scripts/logosyllabic_headlines.py > reports/sister_v2/logosyllabic_headlines.md
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from sister_compare import ci, fmt, load, point_keys, vals  # noqa: E402

ORIG, REV = "knight2006_em_original", "knight2006_em"
LS = "logosyllabic"


def only_ls(recs):
    return {k: v for k, v in recs.items() if k[2] == LS}


def acc(d, before):
    return d.get("token_acc_before_cognate", d["token_acc"]) if before else d["token_acc"]


def main():
    print("# Headline numbers, logo-syllabic corpora only (most Indus-relevant script type)\n")
    print("Analysis of saved records only; methods frozen. 5 languages x 3 seeds = 15 corpora per point "
          "and seed set. Intervals resample whole languages (5 clusters; see the limitations on "
          "undercoverage). Primary = original (frozen) rule, before the cognate step.\n")

    print("## Entropy ratio (Task A, Indus point, Rao top-100 merge, as recorded in `rao_ratio`)\n")
    for name in ("full", "replication"):
        rows = [json.loads(l) for l in open(f"runs/results/{name}/records.jsonl")]
        pt = [r for r in rows if r["job"]["sweep"] == "size" and r["job"]["n_texts"] == 2906
              and r["job"]["regime"] == "full" and not r["job"]["pred_script"]]
        ls = [r["A"]["rao2009_entropy"]["features"]["rao_ratio"] for r in pt
              if r["truth"]["kind"] == "language" and r["job"]["script_type"] == LS]
        allang = [r["A"]["rao2009_entropy"]["features"]["rao_ratio"] for r in pt if r["truth"]["kind"] == "language"]
        iid = [r["A"]["rao2009_entropy"]["features"]["rao_ratio"] for r in pt if r["job"]["source"] == "rao_type2"]
        print(f"- {name}: logo-syllabic {np.mean(ls):.3f} (n={len(ls)}), all languages {np.mean(allang):.3f}, "
              f"i.i.d. control {np.mean(iid):.3f}")
    print("\nThe i.i.d. control scores HIGHER than the languages on this statistic, as in the pooled result.\n")

    print("## No related language (`none` tier, Indus point)\n")
    print("| Run | Mean, original | Mean, revised | Best corpus (orig / rev) | >= 50% |")
    print("|---|---|---|---|---|")
    for label, name in (("Generator v1, seeds 0-2", "full"), ("Generator v1, seeds 3-5", "replication"),
                        ("Generator v2, seeds 0-2", "generator_v2")):
        r = only_ls(load(name))
        ks = point_keys(r, "size", 2906, 4.6)
        o = [r[k]["CD"]["none"][ORIG]["token_acc"] for k in ks]
        v = [r[k]["CD"]["none"][REV]["token_acc"] for k in ks]
        print(f"| {label} | {100*np.mean(o):.1f}% | {100*np.mean(v):.1f}% | {100*max(o):.1f}% / {100*max(v):.1f}% | "
              f"{sum(x >= .5 for x in o + v)} of {2*len(o)} |")
    print()

    print("## Generator contrast (candidates tier, Indus point)\n")
    print("| Seed set | v1 primary | v2 primary | Ratio | v1 with oracle corr. | v2 with oracle corr. |")
    print("|---|---|---|---|---|---|")
    for label, a, b in (("seeds 0-2", "sister_v2_main", "sister_v2_gen2"), ("seeds 3-5", "sister_v2_repl", "sister_v2_gen2_repl"),
                        ("sister-v3, seeds 0-2", "sister_v3_gen1", "sister_v3_gen2")):
        ra, rb = only_ls(load(a)), only_ls(load(b))
        ca = ci(vals(ra, point_keys(ra, "size", 2906, 4.6), "candidates", ORIG, True))
        cb = ci(vals(rb, point_keys(rb, "size", 2906, 4.6), "candidates", ORIG, True))
        oa = ci(vals(ra, point_keys(ra, "size", 2906, 4.6), "candidates", ORIG, False))
        ob = ci(vals(rb, point_keys(rb, "size", 2906, 4.6), "candidates", ORIG, False))
        ratio = f"{cb[0]/ca[0]:.1f}x" if ca[0] > 0 else "n/a (v1 = 0)"
        print(f"| {label} | {fmt(ca)} | {fmt(cb)} | {ratio} | {fmt(oa, False)} | {fmt(ob, False)} |")
    print()

    print("## Related tier (sister only), Indus point\n")
    print("| Seed set | v1 primary | v2 primary | v1 with oracle corr. | v2 with oracle corr. |")
    print("|---|---|---|---|---|")
    for label, a, b in (("seeds 0-2", "sister_v2_main", "sister_v2_gen2"), ("seeds 3-5", "sister_v2_repl", "sister_v2_gen2_repl")):
        ra, rb = only_ls(load(a)), only_ls(load(b))
        c = [ci(vals(r, point_keys(r, "size", 2906, 4.6), "related", ORIG, bf)) for bf in (True, False) for r in (ra, rb)]
        print(f"| {label} | {fmt(c[0])} | {fmt(c[1])} | {fmt(c[2], False)} | {fmt(c[3], False)} |")
    print()

    print("## Longer vs more inscriptions at equal tokens (candidates tier, primary)\n")
    print("| Generator | Longer (2,906 x 10) | More (6,317 x 4.6) |")
    print("|---|---|---|")
    for label, a, b in (("v1", "sister_v2_main", "sister_v2_eqtok_gen1"), ("v2", "sister_v2_gen2", "sister_v2_eqtok_gen2")):
        r = only_ls({**load(a), **load(b)})
        L = ci(vals(r, point_keys(r, "length", 2906, 10.0), "candidates", ORIG, True))
        S = ci(vals(r, point_keys(r, "size", 6317, 4.6), "candidates", ORIG, True))
        print(f"| {label} | {fmt(L)} | {fmt(S)} |")
    print()


if __name__ == "__main__":
    main()
