"""Summarise runs/results/v2_allograph_sweep -> reports/v2/allograph/sweep.md (v2; not in the paper)."""
from __future__ import annotations

import json
from collections import defaultdict

import numpy as np

from ibdb.paths import ensure, reports_dir, runs_dir

OUT = ensure(reports_dir() / "v2" / "allograph")
rows = [json.loads(l) for l in (runs_dir() / "results" / "v2_allograph_sweep" / "records.jsonl").read_text().splitlines() if l.strip()]
err = [r for r in rows if "error" in r]
rows = [r for r in rows if "error" not in r]
INV = [400, 500, 600, 700, 800]
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
BOX = lambda r: 0.2 <= r["job"]["dup"] <= 0.4 and 400 <= r["job"]["inventory"] <= 700  # noqa: E731


def m(v):
    return 100 * float(np.mean(v)) if v else float("nan")


L = ["# v2: allograph merging before Task D (sensitivity sweep, sister-v2 profile)", "",
     "Primary score: frozen original-rule EM, before the cognate step, % of sign tokens. Merger parameters were",
     "fixed on development corpora (seeds 90-91) before this run. Oracle = merge the hidden allograph groups.", "",
     f"Corpora: {len(rows)} (errors: {len(err)}). Regenerated corpora matching their stored statistics: "
     f"{sum(r['regenerated_matches_record'] for r in rows)}/{len(rows)}. Recomputed no-merge score equal to the "
     f"stored score (both tiers): {sum(all(abs(r['D'][t]['none']['primary'] - r['D'][t]['stored_primary']) < 1e-9 for t in r['D']) for r in rows)}/{len(rows)}.", ""]

L += ["## Merge accuracy (learned merger vs hidden allograph map)", "",
      "| Inventory | Precision | Recall | Value-consistent | Signs | Groups after merge | True groups |", "|---|---|---|---|---|---|---|"]
for inv in INV:
    g = [r["merge"]["learned"] for r in rows if r["job"]["inventory"] == inv]
    L.append(f"| {inv} | {np.mean([x['precision'] for x in g]):.2f} | {np.mean([x['recall'] for x in g]):.2f} | "
             f"{np.mean([x['value_consistent'] for x in g]):.2f} | {np.mean([x['n_signs'] for x in g]):.0f} | "
             f"{np.mean([x['n_pred_groups'] for x in g]):.0f} | {np.mean([x['n_true_groups'] for x in g]):.0f} |")
L += ["", "| Script type | Precision | Recall |", "|---|---|---|"]
for st in SCRIPTS:
    g = [r["merge"]["learned"] for r in rows if r["job"]["script_type"] == st]
    L.append(f"| {st} | {np.mean([x['precision'] for x in g]):.2f} | {np.mean([x['recall'] for x in g]):.2f} |")

for tier in ("candidates", "none"):
    L += ["", f"## Task D, `{tier}` tier, by inventory (mean over corpora, all duplicate rates)", "",
          "| Inventory | n | No merge | Learned merge | Oracle merge |", "|---|---|---|---|---|"]
    for inv in INV:
        g = [r["D"][tier] for r in rows if r["job"]["inventory"] == inv]
        L.append(f"| {inv} | {len(g)} | {m([x['none']['primary'] for x in g]):.1f} | {m([x['learned']['primary'] for x in g]):.1f} | "
                 f"{m([x['oracle']['primary'] for x in g]):.1f} |")
    g = [r["D"][tier] for r in rows if BOX(r)]
    L.append(f"| Plausible box | {len(g)} | {m([x['none']['primary'] for x in g]):.1f} | {m([x['learned']['primary'] for x in g]):.1f} | "
             f"{m([x['oracle']['primary'] for x in g]):.1f} |")
    L += ["", "By script type (no merge / learned / oracle):", "", "| Script type | " + " | ".join(map(str, INV)) + " |",
          "|---|" + "---|" * len(INV)]
    for st in SCRIPTS:
        cells = []
        for inv in INV:
            g = [r["D"][tier] for r in rows if r["job"]["inventory"] == inv and r["job"]["script_type"] == st]
            cells.append(f"{m([x['none']['primary'] for x in g]):.1f} / {m([x['learned']['primary'] for x in g]):.1f} / "
                         f"{m([x['oracle']['primary'] for x in g]):.1f}" if g else "-")
        L.append(f"| {st} | " + " | ".join(cells) + " |")
    worse = sum(r["D"][tier]["learned"]["primary"] < r["D"][tier]["none"]["primary"] - 1e-9 for r in rows)
    better = sum(r["D"][tier]["learned"]["primary"] > r["D"][tier]["none"]["primary"] + 1e-9 for r in rows)
    L += ["", f"Learned merge vs none, per corpus: better {better}, worse {worse}, equal {len(rows) - better - worse}."]

(OUT / "sweep.md").write_text("\n".join(L) + "\n")
print("\n".join(L))

# Matched comparison: inventory columns hold different language x script combinations (not every
# combination reaches every inventory), so compare only corpora present at both inventories.
by: dict = {}
for r in rows:
    by.setdefault((r["job"]["source"], r["job"]["script_type"], r["job"]["seed"], r["job"]["dup"]), {})[r["job"]["inventory"]] = r
M = ["", "## Matched corpora (same language, script, seed and duplicate rate at both inventories)", "",
     "| Tier | Inventories | n | No merge | Learned merge | Oracle merge |", "|---|---|---|---|---|---|"]
for tier in ("candidates", "none"):
    for lo, hi in ((400, 800), (400, 700), (500, 700)):
        pairs = [(v[lo], v[hi]) for v in by.values() if lo in v and hi in v]
        cells = [f"{m([p[0]['D'][tier][c]['primary'] for p in pairs]):.1f} -> {m([p[1]['D'][tier][c]['primary'] for p in pairs]):.1f}"
                 for c in ("none", "learned", "oracle")]
        M.append(f"| {tier} | {lo} -> {hi} | {len(pairs)} | " + " | ".join(cells) + " |")
with open(OUT / "sweep.md", "a") as fh:
    fh.write("\n".join(M) + "\n")
print("\n".join(M))
