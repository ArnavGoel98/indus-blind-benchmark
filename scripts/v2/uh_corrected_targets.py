"""Pre-registration entry 3: Ugaritic-Hebrew yardsticks against Hebrew with vowel letters removed.

Point estimates with the main method (shared code, yardsticks.ugaritic_hebrew); method uncertainty
from the three rule variants; sampling uncertainty from a bootstrap over Ugaritic texts (200
replicates; word and word-pair statistics from the resampled segments' tablet lines; 20 shuffled
maps per replicate for chance; the same-size floor held at the point estimate's value).
Then the corrected targets and tolerances as entry 3 defines them.

Usage: python scripts/v2/uh_corrected_targets.py -> reports/v2/sister/anchor_corrected.{json,md}
"""
from __future__ import annotations

import json
from collections import Counter

import numpy as np

from ibdb import yardsticks as Y
from ibdb.data import ugaritic as U
from ibdb.paths import ensure, reports_dir

OUT = ensure(reports_dir() / "v2" / "sister")
N_BOOT, N_SHUF = 200, 20
KEYS = ["jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc", "verbatim_natural_6plus"]


def point(variant):
    sp = dict(spelling="defective", variant=variant)
    return Y.ugaritic_hebrew(U.hebrew_texts(**sp), U.hebrew_words(**sp), U.hebrew_texts(U.POETIC_BOOKS, **sp),
                             heb_pairs=U.hebrew_word_pairs(**sp))


def dist(texts):
    c = Counter((t[i], t[i + 1]) for t in texts for i in range(len(t) - 1))
    n = sum(c.values())
    return {k: v / n for k, v in c.items()}


def jsd_d(p, q):
    ks = sorted(set(p) | set(q))
    P = np.array([p.get(k, 0.0) for k in ks]); Q = np.array([q.get(k, 0.0) for k in ks])
    M = 0.5 * (P + Q)
    kl = lambda x: float(np.sum(x[x > 0] * np.log2(x[x > 0] / M[x > 0])))  # noqa: E731
    return 0.5 * (kl(P) + kl(Q))


def bootstrap(main: dict) -> dict:
    sp = dict(spelling="defective", variant=None)
    heb = U.hebrew_texts(**sp)
    hd = dist(heb)
    blob = "|".join("".join(t) for t in heb)
    hw = {"".join(w) for w in U.hebrew_words(**sp)}
    hp = {("".join(a), "".join(b)) for a, b in U.hebrew_word_pairs(**sp)}
    lines = U.ugaritic_lines()
    segs = [(i, s) for i, l in enumerate(lines) for s in l["segments"]]
    rng = np.random.default_rng(2026)
    gold = U.GOLD
    floor = main["bigram_jsd_hebrew_sample_floor"]
    out = {k: [] for k in KEYS}
    for b in range(N_BOOT):
        idx = rng.integers(len(segs), size=len(segs))
        ss = [segs[i][1] for i in idx]
        lc = Counter(segs[i][0] for i in idx)
        words, pairs = Counter(), Counter()
        for li, c in lc.items():
            for w, n in lines[li]["words"].items():
                words[w] += n * c
            for p, n in lines[li]["pairs"].items():
                pairs[p] += n * c
        letters = [[gold[x] for x in t if x != U.DIVIDER] for t in ss]
        out["jsd_above_floor"].append(jsd_d(dist(letters), hd) - floor)
        shuf = [Y.shuffled_mapping(gold, rng) for _ in range(N_SHUF)]
        wm = lambda m: (lambda w: "".join(m[x] for x in w))  # noqa: E731
        pm = lambda m: (lambda p: ("".join(m[x] for x in p[0]), "".join(m[x] for x in p[1])))  # noqa: E731
        ct = Y.overlap(words, hw, wm(gold))[0]
        out["cognate_types_cc"].append(Y.chance_corrected(ct, float(np.mean([Y.overlap(words, hw, wm(m))[0] for m in shuf]))))
        pt = Y.overlap(pairs, hp, pm(gold))[0]
        out["word_pairs_types_cc"].append(Y.chance_corrected(pt, float(np.mean([Y.overlap(pairs, hp, pm(m))[0] for m in shuf]))))
        out["verbatim_natural_6plus"].append(Y.verbatim(("".join(l) for l in letters), blob, 6))
        if (b + 1) % 50 == 0:
            print(f"[boot] {b + 1}/{N_BOOT}", flush=True)
    return {k: {"lo": float(np.quantile(v, 0.025)), "hi": float(np.quantile(v, 0.975)), "sd": float(np.std(v))}
            for k, v in out.items()}


def main() -> None:
    res = {"main": point(None), "variants": {v: point(v) for v in U.SPELLING_VARIANTS[1:]},
           "plene": json.loads((OUT / "anchor.json").read_text())}
    res["bootstrap"] = bootstrap(res["main"])
    m, bt = res["main"], res["bootstrap"]
    half = lambda k: (bt[k]["hi"] - bt[k]["lo"]) / 2  # noqa: E731
    res["targets"] = {
        "close": {"jsd_above_floor": [m["jsd_above_floor"], max(0.04, half("jsd_above_floor"))],
                  "cognate_types_cc": [m["cognate_types_cc"], max(0.10, half("cognate_types_cc"))],
                  "word_pairs_types_cc": [m["word_pairs_types_cc"], max(0.10, half("word_pairs_types_cc"))]},
        "distant": {"jsd_above_floor": [2 * m["jsd_above_floor"], max(0.06, half("jsd_above_floor"))],
                    "cognate_types_cc": [m["cognate_types_cc"] / 2, max(0.10, half("cognate_types_cc"))],
                    "word_pairs_types_cc": [m["word_pairs_types_cc"] / 2, max(0.10, half("word_pairs_types_cc"))]},
        "verbatim_max": max(0.02, bt["verbatim_natural_6plus"]["hi"])}
    (OUT / "anchor_corrected.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=float))
    pc = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
    names = {"jsd_above_floor": "Letter-pair JSD above floor (bits)", "cognate_types_cc": "Shared word forms, chance-corrected",
             "word_pairs_types_cc": "Word pairs, chance-corrected", "verbatim_natural_6plus": "Verbatim, texts of 6+ letters"}
    L = ["# Ugaritic-Hebrew yardsticks with Hebrew vowel letters removed (pre-registration entry 3, post hoc)", "",
         "| Yardstick | Hebrew as written | Vowel letters removed (main) | Bootstrap 95% | Rule variants: + quiescent aleph / keep final he / initial shureq |",
         "|---|---|---|---|---|"]
    for k in KEYS:
        v = res["variants"]
        L.append(f"| {names[k]} | {pc(k, res['plene'][k])} | **{pc(k, m[k])}** | {pc(k, bt[k]['lo'])}-{pc(k, bt[k]['hi'])} | "
                 + " / ".join(pc(k, v[x][k]) for x in U.SPELLING_VARIANTS[1:]) + " |")
    L += ["", f"Hebrew letters: as written 1,197,042; vowel letters removed {sum(map(len, U.hebrew_texts(spelling='defective'))):,}. "
          f"Same-size floor (removed): {m['bigram_jsd_hebrew_sample_floor']:.3f} bits (held fixed in the bootstrap).", "",
          "## Corrected targets (entry 3)", "", "| Setting | JSD above floor | Shared word forms | Word pairs | Verbatim max |", "|---|---|---|---|---|"]
    for s, t in res["targets"].items():
        if s == "verbatim_max":
            continue
        L.append(f"| `{s}` | " + " | ".join(f"{pc(k, t[k][0])} +/- {pc(k, t[k][1])}" for k in KEYS[:3]) + f" | {100 * res['targets']['verbatim_max']:.1f}% |")
    L.append("")
    (OUT / "anchor_corrected.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
