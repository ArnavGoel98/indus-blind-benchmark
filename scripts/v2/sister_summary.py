"""reports/v2/sister/calibration.json + grid -> reports/v2/sister/yardsticks.md (v2; not in the paper)."""
from __future__ import annotations

import json

import numpy as np

from ibdb.paths import reports_dir, runs_dir

D = reports_dir() / "v2" / "sister"
cal = json.loads((D / "calibration.json").read_text())
A = json.loads((D / "anchor.json").read_text())
T = cal["targets"]
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
YS = [("jsd_above_floor", "JSD above floor (bits)", 3), ("cognate_types_cc", "Shared word forms, chance-corr.", 1),
      ("word_pairs_types_cc", "Word pairs, chance-corr.", 1), ("verbatim_6plus", "Verbatim 6+ units", 1)]
fmt = lambda v, d: f"{v:.3f}" if d == 3 else f"{100 * v:.{d}f}%"  # noqa: E731

L = ["# v2 rank 6: sister-v4 calibration — yardstick table (dev seeds 90-91; held-out 0-2)", "",
     "**Result: no language matches the pre-declared targets in either setting.** The selection rule picked the",
     "closest grid point that keeps verbatim text at or below 2%; all are marked \"not matched\". Sumerian has no grid",
     "point at or below 2% verbatim. No Task C or D score has been computed with sister-v4.", "",
     "## Targets (Ugaritic-Hebrew, shared code)", "",
     "| Yardstick | Ugaritic-Hebrew | `close` target (accept) | `distant` target (accept) |", "|---|---|---|---|"]
for y, name, d in YS[:3]:
    c, dd = T["close"][y], T["distant"][y]
    L.append(f"| {name} | {fmt(A[y], d)} | {fmt(c[0], d)} ({fmt(c[0] - c[1], d)} to {fmt(c[0] + c[1], d)}) | "
             f"{fmt(dd[0], d)} ({fmt(dd[0] - dd[1], d)} to {fmt(dd[0] + dd[1], d)}) |")
L.append(f"| Verbatim 6+ letters | {fmt(A['verbatim_natural_6plus'], 1)} | <= 2% | <= 2% |")
L.append(f"| Mergers | {A['mergers']} of 29 | 24% of consonants | 24% of consonants |")

for setting in ("close", "distant"):
    L += ["", f"## `{setting}`: chosen settings (closest grid point; mean of 20 draws)", "",
          "| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | " +
          " | ".join(n for _, n, _ in YS) + " | Matched |", "|---|---|---|" + "---|" * len(YS) + "---|"]
    for lang in LANGS:
        ch = cal["chosen"][setting][lang]
        if ch["knobs"] is None:
            L.append(f"| {lang} | none (no grid point with verbatim <= 2%) | | " + " | ".join("-" for _ in YS) + " | no |")
            continue
        k = ch["knobs"]
        ks = f"{k['n_cond']} / {k['affix_share']} / {k['lexical']} / {k['word_order']} / {k['final_vowel_loss']}"
        for part, lab in (("dev", "90-91"), ("held", "0-2 (held out)")):
            rs = cal["confirm"][setting][lang][part]
            L.append(f"| {lang} | {ks} | {lab} | " + " | ".join(fmt(np.mean([r[y] for r in rs]), d) for y, _, d in YS) +
                     f" | {'yes' if ch['matched'] else 'no'} |")

L += ["", "## v1-like sister, same code (shift + 20% lexical replacement, no mergers; held-out seeds 0-2)", "",
      "| Language | " + " | ".join(n for _, n, _ in YS) + " |", "|---|" + "---|" * len(YS)]
for lang in LANGS:
    rs = cal["confirm"]["v1_like"][lang]["held"]
    L.append(f"| {lang} | " + " | ".join(fmt(np.mean([r[y] for r in rs]), d) for y, _, d in YS) + " |")

rows = [json.loads(l) for l in (runs_dir() / "results" / "v2_sister_grid" / "records.jsonl").read_text().splitlines()]
by: dict = {}
for r in rows:
    by.setdefault((r["lang"], json.dumps(r["knobs"], sort_keys=True)), []).append(r)
agg = [(l, {y: float(np.mean([r[y] for r in rs])) for y, _, _ in YS}) for (l, _), rs in by.items()]
L += ["", "## Why nothing matches: the trade-off over the whole grid (1,080 settings, dev means)", "",
      "Best chance-corrected shared word forms reachable at a given letter-pair distance:", "",
      "| Language | JSD >= 0.090 | JSD >= 0.126 | JSD >= 0.166 | ... and verbatim <= 2% (JSD >= 0.126) | Lowest verbatim with forms >= 37% |",
      "|---|---|---|---|---|---|"]
for lang in LANGS:
    g = [m for l, m in agg if l == lang]
    def best(jt, vmax=1.0):
        v = [m["cognate_types_cc"] for m in g if m["jsd_above_floor"] >= jt and m["verbatim_6plus"] <= vmax]
        return fmt(max(v), 1) if v else "none"
    lv = [m["verbatim_6plus"] for m in g if m["cognate_types_cc"] >= 0.37]
    L.append(f"| {lang} | {best(0.09)} | {best(0.126)} | {best(0.166)} | {best(0.126, 0.02)} | {fmt(min(lv), 1) if lv else 'none'} |")
L.append("")
(D / "yardsticks.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
