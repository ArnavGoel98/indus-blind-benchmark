"""Sister-v3 robustness check (analysis of saved records only; methods frozen at frozen-v1).

sister-v3 = sister-v2 content split + drop every sister clause that contains any hidden text's word
sequence (per corpus). Compared against sister-v2 on the same seeds (0-2), generators v1 and v2.
Primary numbers: original (frozen) EM rule, before the cognate step.

Usage: python scripts/sister_v3_robustness.py > reports/sister_v2/robustness_sister_v3.md
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from sister_compare import LANGS, ci, fmt, load, point_keys, vals  # noqa: E402

ORIG, REV = "knight2006_em_original", "knight2006_em"
GENS = [("Generator v1", "sister_v2_main", "sister_v2_eqtok_gen1", "sister_v3_gen1"),
        ("Generator v2", "sister_v2_gen2", "sister_v2_eqtok_gen2", "sister_v3_gen2")]
EQ_N = 6317  # 6,317 texts x 4.6 = 29,058 tokens, vs 2,906 x 10 = 29,060


def merged(*names):
    out = {}
    for n in names:
        out.update(load(n))
    return out


def cell(recs, sweep, n, L, tier, m, before):
    return ci(vals(recs, point_keys(recs, sweep, n, L), tier, m, before))


def main():
    print("# Robustness check: sister-v3 (no hidden-text word sequence in the sister)\n")
    print("Analysis of saved records only; methods frozen at `frozen-v1`. Seeds 0-2, 5 languages x 4 "
          "script types = 60 corpora per point. Task D token accuracy, %, 95% interval resampling whole "
          "languages.\n")
    print("- **sister-v2**: clauses split by content hash (no clause in both halves).")
    print("- **sister-v3**: sister-v2, then every sister clause containing any hidden text's word sequence "
          "(as contiguous words) is dropped, separately for each corpus. A truncated hidden text also "
          "contributes its whole words without the last one. Only the sister is filtered.")
    print("- **Primary**: original (frozen) rule, before the cognate step. Secondary: with oracle sound "
          "correspondences.\n")

    v3all = {}
    for label, v2, v2eq, v3 in GENS:
        a2, b3 = merged(v2, v2eq), load(v3)
        v3all[label] = (a2, b3)

    print("## Residual overlap under sister-v3\n")
    print("Verbatim containment of hidden texts in the sister's source half is 0 by construction (word "
          "level, before sound change and lexical replacement). The table shows how much of the sister "
          "the filter removes and how many of the hidden texts' word pairs (bigrams) still occur in it.\n")
    print("| Generator | Language | Sister clauses dropped | Hidden word bigrams in sister: sister-v2 | "
          "sister-v3 |")
    print("|---|---|---|---|---|")
    for label, (_, b3) in v3all.items():
        for lang in LANGS + ["all"]:
            ds = [r["sister_v3"] for k, r in b3.items()
                  if (lang == "all" or k[1] == lang) and r.get("sister_v3")
                  and k[0] == "size" and k[4] == 2906]
            if not ds:
                continue
            drop = np.mean([d["dropped"] / d["ref_clauses"] for d in ds])
            bb = np.mean([d["hidden_bigram_share_before"] for d in ds])
            ba = np.mean([d["hidden_bigram_share_after"] for d in ds])
            print(f"| {label} | {lang} | {100 * drop:.0f}% | {100 * bb:.0f}% | {100 * ba:.0f}% |")
    print("\n(Indus point, 2,906 texts x 4.6 signs.)\n")

    print("## Indus point (2,906 texts x 4.6 signs)\n")
    print("| Generator | Tier | sister-v2, primary | sister-v3, primary | sister-v2, with oracle sound "
          "correspondences | sister-v3, with oracle sound correspondences |")
    print("|---|---|---|---|---|---|")
    for label, (a2, b3) in v3all.items():
        for tier in ("related", "candidates"):
            row = [fmt(cell(r, "size", 2906, 4.6, tier, ORIG, bf)) for bf in (True,) for r in (a2, b3)]
            row += [fmt(cell(r, "size", 2906, 4.6, tier, ORIG, False)) for r in (a2, b3)]
            print(f"| {label} | {tier} | " + " | ".join(row) + " |")
    print()

    print("### Headline 3 check: generator contrast, candidates tier, primary\n")
    for sv, idx in (("sister-v2", 0), ("sister-v3", 1)):
        c1 = cell(v3all["Generator v1"][idx], "size", 2906, 4.6, "candidates", ORIG, True)
        c2 = cell(v3all["Generator v2"][idx], "size", 2906, 4.6, "candidates", ORIG, True)
        hi = []
        for g in ("Generator v1", "Generator v2"):
            r = v3all[g][idx]
            hi.append(sum(r[k]["CD"]["candidates"][ORIG].get("token_acc_before_cognate",
                                                             r[k]["CD"]["candidates"][ORIG]["token_acc"]) >= 0.5
                          for k in point_keys(r, "size", 2906, 4.6)))
        print(f"- {sv}: v1 {fmt(c1)} vs v2 {fmt(c2)} (ratio {c2[0] / c1[0]:.1f}x; corpora >= 50%: "
              f"{hi[0]} of 60 vs {hi[1]} of 60)")
    print()

    print("### Which reference the original rule chose (candidates tier, Indus point)\n")
    for label, (a2, b3) in v3all.items():
        for sv, r in (("sister-v2", a2), ("sister-v3", b3)):
            ks = point_keys(r, "size", 2906, 4.6)
            sh = np.mean([r[k]["CD"]["candidates"][ORIG]["reference"].endswith("-sister") for k in ks])
            print(f"- {label}, {sv}: sister chosen for {100 * sh:.0f}% of corpora")
    print()

    print("## Headline 4 check: longer vs more inscriptions at equal tokens (~29k), candidates tier\n")
    print("Length: 2,906 texts x 10 signs (29,060 tokens). Size: 6,317 texts x 4.6 signs (29,058 tokens), "
          "run directly at this point (no interpolation).\n")
    print("| Generator | Sister | Score | Longer (2,906 x 10) | More (6,317 x 4.6) | Difference [95% CI] |")
    print("|---|---|---|---|---|---|")
    for label, (a2, b3) in v3all.items():
        for sv, r in (("sister-v2", a2), ("sister-v3", b3)):
            for name, bf in (("primary", True), ("with oracle sound correspondences", False)):
                L = cell(r, "length", 2906, 10.0, "candidates", ORIG, bf)
                S = cell(r, "size", EQ_N, 4.6, "candidates", ORIG, bf)
                d = paired_diff(r, bf)
                print(f"| {label} | {sv} | {name} | {fmt(L)} | {fmt(S)} | {fmt(d)} |")
    print("\nDifference = longer minus more, paired by (language, script type, seed); interval resamples "
          "whole languages.\n")
    print("**Confound under sister-v3.** The filter depends on the corpus. Many short texts contain many "
          "short word sequences, so they strip more of the sister than fewer long texts do:\n")
    print("| Generator | Corpus | Sister clauses dropped | Hidden word bigrams left in sister |")
    print("|---|---|---|---|")
    for label, (_, b3) in v3all.items():
        for sw, n, L in (("size", 2906, 4.6), ("length", 2906, 10.0), ("size", EQ_N, 4.6)):
            ds = [r["sister_v3"] for k, r in b3.items() if k[0] == sw and k[4] == n and abs(k[5] - L) < 1e-9]
            print(f"| {label} | {n:,} x {L:g} | {100 * np.mean([d['dropped'] / d['ref_clauses'] for d in ds]):.0f}% "
                  f"| {100 * np.mean([d['hidden_bigram_share_after'] for d in ds]):.0f}% |")
    print("\nSo sister-v3 handicaps the 'more inscriptions' corpus more than the 'longer inscriptions' "
          "corpus, which can widen the gap. Sister-v2 applies no corpus-dependent filter, and the length "
          "advantage is already present there; read sister-v3 as a check that the advantage survives, "
          "not as a better estimate of its size.\n")


def paired_diff(r, before, n_boot=2000, seed=0):
    def acc(k):
        d = r[k]["CD"]["candidates"][ORIG]
        return d.get("token_acc_before_cognate", d["token_acc"]) if before else d["token_acc"]
    pairs = []
    for k in point_keys(r, "length", 2906, 10.0):
        ks = ("size", k[1], k[2], k[3], EQ_N, 4.6)
        if ks in r:
            pairs.append((k[1], acc(k) - acc(ks)))
    return ci(pairs, n_boot, seed) if pairs else None


if __name__ == "__main__":
    main()
