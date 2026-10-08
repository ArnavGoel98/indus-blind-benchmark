"""Sensitivity sweep: sister-v2 (primary = original rule, before the cognate step) vs sister-v1
(upper bound, after the cognate step). Analysis of saved records only; methods frozen.
Usage: python scripts/sensitivity_v2_compare.py > reports/sensitivity/sister_v2_compare.md
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from ibdb import sensitivity as S  # noqa: E402
from sister_compare import load  # noqa: E402

O, R = "knight2006_em_original", "knight2006_em"


def rng(cells, key, pred=lambda c: True):
    v = [c[key]["mean"] for c in cells if c["n"] and key in c and pred(c)]
    return (100 * min(v), 100 * max(v)) if v else (np.nan, np.nan)


def f(r):
    return f"{r[0]:.1f}-{r[1]:.1f}%"


def main():
    runs = {"sister-v2, primary (before cognate)": S.aggregate("sensitivity_sister_v2", before_cognate=True),
            "sister-v2, with oracle sound correspondences": S.aggregate("sensitivity_sister_v2", before_cognate=False),
            "upper bound (sister-v1, known overlap), with oracle sound correspondences": S.aggregate("sensitivity", before_cognate=False)}
    print("# Sensitivity sweep: sister-v2 primary vs sister-v1 upper bound\n")
    print("Generator v1, Indus point, 6 x 5 grid, seeds 0-2, methods frozen. Cell means of Task D token accuracy. "
          "Box = duplicates 0.2-0.4 x inventory 400-700. S = seals-only region (duplicates 0.0); T = tablets-only "
          "region (duplicates 0.4-0.5); prediction, not measurement.\n")
    for lab, a in runs.items():
        P = a["panels"]
        print(f"## {lab}\n")
        print(f"- Records: {a['n_records']}; status {a['status_counts']}; strict panel {len(a['balanced_combos'])} "
              f"combinations; box panel {len(a['box_combos'])} combinations.")
        print(f"- Candidates, original rule, box panel: {f(rng(P['box'], 'candidates:'+O))}; all corpora in box: "
              f"{f(rng(P['all'], 'candidates:'+O, lambda c: 0.2<=c['dup']<=0.4 and c['inventory']<=700))}.")
        bs = a["box_spread"].get("candidates:" + O)
        if bs:
            mx = max(bs["rows"], key=lambda r: r["spread"])
            print(f"- Within-combination spread across the box (original): median {100*bs['median_spread']:.1f} points, "
                  f"max {100*mx['spread']:.1f} ({mx['source']}/{mx['script_type']}), {sum(r['spread']>=0.1 for r in bs['rows'])} of {bs['n_combos']} >= 10 points.")
        bsr = a["box_spread"].get("candidates:" + R)
        if bsr:
            print(f"- Same, revised rule (post hoc): median {100*bsr['median_spread']:.1f}, max {100*max(r['spread'] for r in bsr['rows']):.1f} points.")
        print(f"- Candidates, revised rule, box panel: {f(rng(P['box'], 'candidates:'+R))}.")
        print(f"- No relative, box panel max cell: original {rng(P['box'],'none:'+O)[1]:.1f}%, revised {rng(P['box'],'none:'+R)[1]:.1f}%; "
              f"whole grid max cell: original {rng(P['all'],'none:'+O)[1]:.1f}%, revised {rng(P['all'],'none:'+R)[1]:.1f}%.")
        for panel in ("all", "balanced"):
            s_ = lambda k: rng(P[panel], k, lambda c: c["dup"] == 0.0)  # noqa: E731
            t_ = lambda k: rng(P[panel], k, lambda c: c["dup"] >= 0.354)  # noqa: E731
            print(f"- Archaeology ({panel} panel), original: S {f(s_('candidates:'+O))} vs T {f(t_('candidates:'+O))}; "
                  f"revised: S {f(s_('candidates:'+R))} vs T {f(t_('candidates:'+R))}; none tier max "
                  f"{max(s_('none:'+R)[1], t_('none:'+R)[1], s_('none:'+O)[1], t_('none:'+O)[1]):.1f}%.")
        print()
    recs = [json.loads(l) for l in open("runs/results/sensitivity_sister_v2/records.jsonl")]
    ok = [r for r in recs if r["status"] == "ok" and S.valid(r)]
    allx = [S._acc(r["CD"]["none"][m], False) for r in ok for m in (O, R)]
    print(f"No relative, sister-v2 sweep, every valid corpus: best {100*max(allx):.1f}%, corpora >= 50%: "
          f"{sum(x >= .5 for x in allx)} of {len(allx)} (both rules).\n")
    print("## Generator-v2 corpora inside the plausible box (Indus point, sister-v2 runs, seeds 0-5)\n")
    for lab, bf in (("primary", True), ("with oracle sound correspondences", False)):
        xs = []
        for n in ("sister_v2_gen2", "sister_v2_gen2_repl"):
            for k, r in load(n).items():
                if k[0] == "size" and k[4] == 2906 and 0.2 <= r["stats"]["duplicate_text_fraction"] <= 0.4 \
                        and 400 <= r["stats"]["sign_inventory"] <= 700:
                    d = r["CD"]["candidates"][O]
                    xs.append(d.get("token_acc_before_cognate", d["token_acc"]) if bf else d["token_acc"])
        print(f"- {lab}: {len(xs)} corpora, mean {100*np.mean(xs):.1f}%, max {100*max(xs):.1f}%")


if __name__ == "__main__":
    main()
