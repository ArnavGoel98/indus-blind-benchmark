"""reports/v2/sister/*.json + grids -> reports/v2/sister/yardsticks.md (v2; not in the paper).

Opens with the original calibration failure (pre-registration entry 3 keeps it first), then the
corrected calibration (entry 3, post hoc), then the three tiers side by side: harsh (original-target
settings, lower bound), close and distant (corrected).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

from ibdb.paths import reports_dir, runs_dir

D = reports_dir() / "v2" / "sister"
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
YS = [("jsd_above_floor", "JSD above floor (bits)", 3), ("cognate_types_cc", "Shared word forms, cc", 1),
      ("word_pairs_types_cc", "Word pairs, cc", 1), ("verbatim_6plus", "Verbatim 6+", 1)]
fmt = lambda v, d: f"{v:.3f}" if d == 3 else f"{100 * v:.{d}f}%"  # noqa: E731
ks = lambda k: f"{k['n_cond']} / {k['affix_share']} / {k['lexical']} / {k['word_order']} / {k['final_vowel_loss']}"  # noqa: E731


def grid_agg(run: str):
    rows = [json.loads(l) for l in (runs_dir() / "results" / run / "records.jsonl").read_text().splitlines()]
    by: dict = {}
    for r in rows:
        by.setdefault((r["lang"], json.dumps(r["knobs"], sort_keys=True)), []).append(r)
    return [(l, json.loads(k), {y: float(np.mean([r[y] for r in rs])) for y, _, _ in YS}) for (l, k), rs in by.items()]


def tier_rows(L, cal_tier: dict, confirm: dict):
    L += ["| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | " + " | ".join(n for _, n, _ in YS) +
          " | Matched |", "|---|---|---|" + "---|" * len(YS) + "---|"]
    for lang in LANGS:
        ch = cal_tier[lang]
        if ch.get("knobs") is None:
            L.append(f"| {lang} | {ch.get('note', 'none')} | | " + " | ".join("-" for _ in YS) + " | no |")
            continue
        for part, lab in (("dev", "90-91"), ("held", "0-2 held out")):
            rs = confirm.get(lang, {}).get(part)
            if not rs:
                continue
            L.append(f"| {lang} | {ks(ch['knobs'])} | {lab} | " + " | ".join(fmt(np.mean([r[y] for r in rs]), d) for y, _, d in YS) +
                     f" | {ch.get('matched_label', 'yes' if ch.get('matched') else 'no')} |")
    L.append("")


def main() -> None:
    orig = json.loads((D / "calibration.json").read_text())
    corr = json.loads((D / "calibration_corrected.json").read_text())
    harsh = json.loads((D / "harsh.json").read_text())
    ac = json.loads((D / "anchor_corrected.json").read_text())
    L = ["**Original calibration FAILED: no language matched the pre-declared targets (sister plan) in either setting; "
         "Sumerian had no grid point at or below 2% verbatim.** Details in the last sections.", "",
         "**Corrected calibration (pre-registration entry 3, post hoc) also FAILED: 0/5 languages matched in `close` or "
         "`distant`; Sumerian again had no grid point at or below 2% verbatim.** For Sanskrit and Finnish the closest "
         "`close` and `distant` settings are the same grid point, so the two corrected tiers are not distinct.", "",
         "# v2 rank 6: sister-v4 yardsticks — original and corrected calibration", "",
         "No Task C or D score has been computed with sister-v4.", "",
         "## Corrected targets (pre-registration entry 3, POST HOC: Hebrew vowel letters removed)", "",
         "Ugaritic-Hebrew, shared code, the entry-3 method. Full table with bootstrap and rule variants: "
         "`anchor_corrected.md`.", "",
         "| Setting | JSD above floor | Shared word forms, cc | Word pairs, cc | Verbatim max |", "|---|---|---|---|---|"]
    for s in ("close", "distant"):
        t = ac["targets"][s]
        L.append(f"| `{s}` | " + " | ".join(f"{fmt(t[y][0], d)} +/- {fmt(t[y][1], d)}" for y, _, d in YS[:3]) +
                 f" | {fmt(ac['targets']['verbatim_max'], 1)} |")
    L += ["", "Split: contiguous blocks per language (`block_test.md`): " +
          ", ".join(f"{l} {s}" for l, s in json.loads((D / "block_split.json").read_text()).items()) + ". "
          "Blocks do not remove shared formulaic text (recorded limitation).", ""]
    for s in ("close", "distant"):
        n_ok = sum(bool(corr["chosen"][s][l].get("matched")) for l in LANGS)
        L += [f"## Corrected `{s}`: chosen settings ({n_ok}/5 languages matched; mean of 20 draws)", ""]
        tier_rows(L, corr["chosen"][s], corr["confirm"][s])
    L += ["## `harsh` tier (lower bound): settings chosen against the original targets, original content split", ""]
    tier_rows(L, harsh["chosen"], harsh["confirm"])
    L += ["## The three tiers side by side (held-out seeds 0-2)", "",
          "| Language | " + " | ".join(f"{t}: JSD / forms / pairs / verbatim" for t in ("harsh", "close", "distant")) + " |",
          "|---|---|---|---|"]
    for lang in LANGS:
        cells = []
        for src in (harsh["confirm"], corr["confirm"]["close"], corr["confirm"]["distant"]):
            rs = src.get(lang, {}).get("held")
            cells.append(" / ".join(fmt(np.mean([r[y] for r in rs]), d) for y, _, d in YS) if rs else "-")
        L.append(f"| {lang} | " + " | ".join(cells) + " |")
    L += ["", "## v1-like sister, same code (held-out seeds 0-2): content split / block split", "",
          "| Language | " + " | ".join(n for _, n, _ in YS) + " |", "|---|" + "---|" * len(YS)]
    for lang in LANGS:
        a = orig["confirm"]["v1_like"][lang]["held"]
        b = corr["confirm"]["v1_like"][lang]["held"]
        L.append(f"| {lang} | " + " | ".join(f"{fmt(np.mean([r[y] for r in a]), d)} / {fmt(np.mean([r[y] for r in b]), d)}"
                                             for y, _, d in YS) + " |")
    for name, run, cal in (("corrected", "v2_sister_grid_corrected", corr), ("original", "v2_sister_grid", orig)):
        agg = grid_agg(run)
        tc = cal["targets"]["close"]["cognate_types_cc"][0]
        L += ["", f"## Trade-off over the {name} grid (1,080 settings, dev means)", "",
              "Best shared word forms (cc) reachable at a given JSD above floor, and the lowest verbatim among settings "
              f"keeping forms >= {fmt(tc - 0.10, 1)}:", "",
              "| Language | JSD >= 0.049 | JSD >= 0.089 | JSD >= 0.126 | JSD >= 0.166 | Lowest verbatim |", "|---|---|---|---|---|---|"]
        for lang in LANGS:
            g = [m for l, _, m in agg if l == lang]
            def best(j):
                v = [m["cognate_types_cc"] for m in g if m["jsd_above_floor"] >= j]
                return fmt(max(v), 1) if v else "none"
            lv = [m["verbatim_6plus"] for m in g if m["cognate_types_cc"] >= tc - 0.10]
            L.append(f"| {lang} | {best(0.049)} | {best(0.089)} | {best(0.126)} | {best(0.166)} | {fmt(min(lv), 1) if lv else 'none'} |")
    L += ["", "## Original calibration (sister plan targets; content split) — FAILED", ""]
    for s in ("close", "distant"):
        L += [f"### Original `{s}`", ""]
        tier_rows(L, orig["chosen"][s], orig["confirm"][s])
    (D / "yardsticks.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def harsh_tier() -> None:
    """Harsh tier = original-target settings ('close'), content split. Sumerian (no point <= 2%
    verbatim): the original-grid point with the lowest verbatim, ties by loss. Confirmed on 90-91 and 0-2."""
    os.environ["IBDB_SISTER_CAL"] = "original"
    sys.path.insert(0, os.path.dirname(__file__))
    import sister_calibrate as C
    orig = json.loads((D / "calibration.json").read_text())
    T = C.targets(C.anchor())["close"]
    chosen = {}
    for lang in LANGS:
        ch = orig["chosen"]["close"][lang]
        if ch["knobs"] is not None:
            chosen[lang] = {"knobs": ch["knobs"], "matched_label": "harsh (original close)"}
            continue
        g = [(k, m) for l, k, m in grid_agg("v2_sister_grid") if l == lang]
        loss = lambda m: sum(((m[y] - t) / hw) ** 2 for y, (t, hw) in T.items())  # noqa: E731
        k, m = min(g, key=lambda km: (round(km[1]["verbatim_6plus"], 12), loss(km[1])))
        chosen[lang] = {"knobs": k, "matched_label": f"harsh (lowest verbatim, {100 * m['verbatim_6plus']:.1f}% on dev grid)"}
    conf = {l: {"dev": [C.measure(l, s, c["knobs"], 20) for s in C.DEV], "held": [C.measure(l, s, c["knobs"], 20) for s in C.HELD]}
            for l, c in chosen.items()}
    (D / "harsh.json").write_text(json.dumps({"chosen": chosen, "confirm": conf}, indent=1, default=float))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "harsh":
        harsh_tier()
    else:
        main()
