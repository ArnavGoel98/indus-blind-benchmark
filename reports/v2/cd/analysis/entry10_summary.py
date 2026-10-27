"""Pre-registration entry 10: old (no source read as lost) against new (no source read as unknown).

Reads the entry-10 rerun records (runs/results/v2_e10, or reports/v2/cd/records/v2_e10.jsonl.gz), the archived
entry 6-9 records (reproducibility check of the old scores) and the yardstick and verbatim reports before
(reports/v2/real_relatives/pre_entry10/) and after entry 10. Re-evaluates the readings of entries 7-9 with
both and lists those that flip.
Usage (repository root): python reports/v2/cd/analysis/entry10_summary.py -> reports/v2/cd/entry10.{md,json}
"""
import gzip
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2_analysis as A  # noqa: E402

EM, EMO, FR = A.EM, A.EMO, A.FR
RR = A.ROOT / "reports" / "v2" / "real_relatives"
PAIRS = {"finnish": ["estonian"], "tamil": ["malayalam", "kannada"]}
UNREL = {"finnish": ["latin", "tamil"], "tamil": ["latin", "finnish"]}
LABEL = {"estonian": "Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters)",
         "malayalam": "Old Tamil-Malayalam", "kannada": "Old Tamil-Kannada"}
K = lambda r: (r["lang"], r["script_type"], r["seed"], r["sampler"])  # noqa: E731


def arch(name):
    p = A.ARCHIVE / f"{name}.jsonl.gz"
    return [json.loads(x) for x in gzip.decompress(p.read_bytes()).decode().splitlines()] if p.exists() else []


def mean(v):
    return float(np.mean(v)) if v else float("nan")


def reproducibility(e10):
    """Old-map scores of the rerun against the archived records of entries 6-9 (must be identical)."""
    main = {K(r): r for n in ("v2_cd", "v2_cd_repl", "v2_cd_estonian", "v2_cd_repl_estonian") for r in arch(n)}
    ctrl = {K(r): r for n in ("v2_controls", "v2_controls_estonian") for r in arch(n)}
    n, bad = 0, []
    for k, e in e10.items():
        for tier, ms in e["tiers"].items():
            for m, x in ms.items():
                o = main.get(k, {}).get("tiers", {}).get(tier, {}).get(m)
                if o is None:
                    continue
                for f in ("strict", "lenient", "recoverable"):
                    n += 1
                    if x["old"][f] != o[f]:
                        bad.append((k, tier, m, f, x["old"][f], o[f]))
                if x["reference"] != o["reference"]:
                    bad.append((k, tier, m, "reference", x["reference"], o["reference"]))
        c = ctrl.get(k)
        if not c:
            continue
        for g, v in e["floor"].items():
            if g in c["floor"]:
                n += 1
                if v["old"] != c["floor"][g]:
                    bad.append((k, "floor", g, "", v["old"], c["floor"][g]))
        for u, ms in e["unrelated"].items():
            for m, gs in ms.items():
                for g, x in gs.items():
                    if g == "diag" or g not in c["unrelated"].get(u, {}).get(m, {}):
                        continue
                    n += 1
                    if x["old"]["strict"] != c["unrelated"][u][m][g]["strict"]:
                        bad.append((k, "unrelated", u, m, x["old"]["strict"], c["unrelated"][u][m][g]["strict"]))
        for g, b in e["budget"].items():
            if g in c.get("budget", {}):
                n += 1
                if b["10"]["old"]["strict"] != c["budget"][g]["10"]["strict"]:
                    bad.append((k, "budget10", g, "", b["10"]["old"]["strict"], c["budget"][g]["10"]["strict"]))
    return {"compared": n, "mismatches": [list(map(str, b)) for b in bad]}


def cells(e10):
    out = []
    for lang, rels in PAIRS.items():
        for rel in rels:
            g, tr = f"real:{rel}", f"related_real:{rel}"
            for st in A.SCRIPTS:
                rs = [e for k, e in sorted(e10.items()) if k[0] == lang and k[1] == st]
                row = {"lang": lang, "rel": rel, "script": st}
                for ver in ("old", "new"):
                    s = lambda x: x["old"] if ver == "old" else x  # noqa: E731
                    v = lambda m, f, seeds: [100 * s(r["tiers"][tr][m])[f] for r in rs if r["seed"] in seeds]  # noqa: E731
                    d = {"s02": mean(v(EM, "strict", (0, 1, 2))), "s35": mean(v(EM, "strict", (3, 4, 5))),
                         "s05": mean(v(EM, "strict", range(6))), "emo02": mean(v(EMO, "strict", (0, 1, 2))),
                         "fr02": mean(v(FR, "strict", (0, 1, 2))), "len02": mean(v(EM, "lenient", (0, 1, 2))),
                         "ceil02": mean(v(EM, "recoverable", (0, 1, 2))),
                         "floor": mean([100 * r["floor"][g][ver] for r in rs])}
                    rel_by = {(r["seed"], r["sampler"]): 100 * s(r["tiers"][tr][EM])["strict"] for r in rs}
                    un = {u: {(r["seed"], r["sampler"]): 100 * s(r["unrelated"][u][EM][g])["strict"] for r in rs}
                          for u in UNREL[lang]}
                    best = max(un, key=lambda u: mean(list(un[u].values())))
                    d["best_unrel"], d["unrel"] = best, mean(list(un[best].values()))
                    d["added"] = d["s05"] - d["unrel"]
                    d["wins"] = sum(rel_by[k] > un[best][k] for k in rel_by)
                    d["helps"] = bool(d["added"] >= 5 and d["wins"] >= 9)
                    d["at_floor"] = bool(d["s05"] <= d["floor"] + 2)
                    b = [r for r in rs if r["budget"]]
                    if b:
                        r3 = mean([100 * s(r["tiers"][tr][EM])["strict"] for r in b])
                        r10 = mean([100 * s(r["budget"][g]["10"])["strict"] for r in b])
                        d.update({"r3": r3, "r10": r10, "first_order": bool(abs(r10 - r3) > 10)})
                    d["n_at_50"] = sum(x >= 50 for x in v(EM, "strict", range(6)))
                    row[ver] = d
                out.append(row)
    return out


def yardsticks():
    old = json.loads((RR / "pre_entry10" / "yardsticks.json").read_text())["pairs"]
    new = json.loads((RR / "yardsticks.json").read_text())["pairs"]
    old["finnish-estonian"] = json.loads((RR / "pre_entry10" / "estonian.json").read_text())["pair"]
    new["finnish-estonian"] = json.loads((RR / "estonian.json").read_text())["pair"]
    vo = json.loads((RR / "pre_entry10" / "verbatim.json").read_text())
    vn = json.loads((RR / "verbatim.json").read_text())
    vo["finnish-estonian"] = json.loads((RR / "pre_entry10" / "estonian.json").read_text())["verbatim"]
    vn["finnish-estonian"] = json.loads((RR / "estonian.json").read_text())["verbatim"]
    out = {}
    for p in ("finnish-estonian", "tamil-malayalam", "tamil-kannada", "latin-italian"):
        out[p] = {"old": old[p]["normalised"], "new": new[p]["normalised"],
                  "verbatim_old": vo[p]["share"], "verbatim_new": vn[p]["share"],
                  "windows_old": vo[p]["n_windows_drawn"], "windows_new": vn[p]["n_windows_drawn"],
                  "multi_old": vo[p]["hits_whole_multiword"], "multi_new": vn[p]["hits_whole_multiword"]}
    return out


def main():
    lines = A._lines("v2_e10")
    e10 = {K(r): r for r in (json.loads(x) for x in lines or []) if "error" not in r}
    errors = [x for x in (json.loads(x) for x in lines or []) if "error" in x]
    res = {"n_corpora": len(e10), "errors": len(errors), "reproducibility": reproducibility(e10),
           "cells": cells(e10), "yardsticks": yardsticks()}
    (A.CD / "entry10.json").write_text(json.dumps(res, indent=1, default=float))
    write_md(res)


def write_md(res):
    f = lambda x: f"{x:.1f}"  # noqa: E731
    on = lambda d, k: f"{f(d['old'][k])} → **{f(d['new'][k])}**" if abs(d["old"][k] - d["new"][k]) > 0.05 else f(d["new"][k])  # noqa: E731
    yn = lambda b: "yes" if b else "no"  # noqa: E731
    rp = res["reproducibility"]
    L = ["# Entry 10: \"no source\" read as unknown instead of lost (old → new)", "",
         "Pre-registration entry 10 (declared 2026-10-27, before any rerun). Before it, the v2 harness dropped a "
         "no-source gold letter from a syllable or word reflex, like a lost sound; now such a token is unrecoverable, "
         "and the yardsticks break the text there. Affected pairs: Finnish-Estonian (Finnish p, v, j, y, ö, d, g, loan "
         "letters, and ä) and Old Tamil-Malayalam and -Kannada (h, s, ṣ, ḵ). Latin-Italian has no no-source row and is "
         "unchanged. Values are % of sign tokens, revised EM, strict, `related` tier unless stated; **bold** = changed.", "",
         f"**Rerun:** {res['n_corpora']} corpora, {res['errors']} errors. **Reproducibility:** {rp['compared']:,} old-map "
         f"values compared with the archived entry 6-9 records, {len(rp['mismatches'])} mismatches.", "",
         "## Ceilings and Task D (seeds 0-2 primary; pooled 0-5)", "",
         "| Pair | Script | Ceiling 0-2 | Revised EM 0-2 | Pooled 0-5 | Lenient 0-2 | Original EM 0-2 | Frequency rank 0-2 |",
         "|---|---|---|---|---|---|---|---|"]
    for c in res["cells"]:
        L.append(f"| {LABEL[c['rel']]} | {c['script']} | {on(c, 'ceil02')} | {on(c, 's02')} | {on(c, 's05')} | "
                 f"{on(c, 'len02')} | {on(c, 'emo02')} | {on(c, 'fr02')} |")
    L += ["", "## Controls (entries 8 and 9 readings, seeds 0-5)", "",
          "| Pair | Script | Floor (C2) | At the floor? old → new | Better unrelated ref. | Added value | Paired wins (of 12) | Measurably helps? old → new |",
          "|---|---|---|---|---|---|---|---|"]
    flips = []
    for c in res["cells"]:
        o, n = c["old"], c["new"]
        L.append(f"| {LABEL[c['rel']]} | {c['script']} | {on(c, 'floor')} | {yn(o['at_floor'])} → {yn(n['at_floor'])} | "
                 f"{n['best_unrel'].capitalize()}, {on(c, 'unrel')} | {f(o['added'])} → {f(n['added'])} | {o['wins']} → {n['wins']} | "
                 f"{yn(o['helps'])} → {yn(n['helps'])} |")
        for k, name in (("at_floor", "at the floor (C2/E1)"), ("helps", "measurably helps (C1/E2)"), ("first_order", "budget first-order (C3)")):
            if k in o and o[k] != n[k]:
                flips.append(f"{LABEL[c['rel']]}, {c['script']}: {name} {yn(o[k])} → {yn(n[k])}")
    L += ["", "## Solver budget (C3, Old Tamil, seeds 0-2; alphabetic cannot change)", "",
          "| Pair | Script | 3 restarts | 10 restarts | First-order? old → new |", "|---|---|---|---|---|"]
    for c in res["cells"]:
        if "r3" in c["new"]:
            L.append(f"| {LABEL[c['rel']]} | {c['script']} | {on(c, 'r3')} | {on(c, 'r10')} | "
                     f"{yn(c['old']['first_order'])} → {yn(c['new']['first_order'])} |")
    hi = max(c["new"]["s35"] for c in res["cells"] if c["lang"] == "tamil")
    L += ["", "## Readings re-evaluated", "",
          f"- R1 (entry 7, Old Tamil): every seeds 3-5 real-relative mean stays below 50% (highest {f(hi)}%). Scores can "
          "only fall under entry 10, so R1 cannot flip.",
          "- R2 (Old Tamil alphabetic within 22.0-42.0%), R3 (Italian below `harsh`) and R4 (relative picked in fewer than "
          "half of the `candidates_real` corpora) do not depend on no-source scoring: alphabetic scores, Latin and the "
          "references chosen are unchanged.",
          "- E3 and E4 (entry 9): `harsh` and the choice of reference are unchanged; E3 is recomputed in `estonian.md`.",
          "- Flipped readings: " + ("; ".join(flips) if flips else "none") + ".", "",
          "## Yardsticks and verbatim overlap (normalised; point estimates)", "",
          "| Pair | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Verbatim share (inspection) | Windows drawn | Hits spanning 2+ whole words |",
          "|---|---|---|---|---|---|---|---|"]
    lab = {"finnish-estonian": LABEL["estonian"], "tamil-malayalam": LABEL["malayalam"], "tamil-kannada": LABEL["kannada"],
           "latin-italian": "Latin-Italian (unchanged by construction)"}
    for p, y in res["yardsticks"].items():
        o, n = y["old"]["point"], y["new"]["point"]
        g = lambda k, pc=True: (f"{100 * o[k]:.1f}%" if pc else f"{o[k]:.3f}") + (  # noqa: E731
            "" if o[k] == n[k] else " → **" + (f"{100 * n[k]:.1f}%" if pc else f"{n[k]:.3f}") + "**")
        vb = f"{100 * y['verbatim_old']:.1f}%" + ("" if y["verbatim_old"] == y["verbatim_new"] else f" → **{100 * y['verbatim_new']:.1f}%**")
        L.append(f"| {lab[p]} | {g('jsd_above_floor', False)} | {g('cognate_types_cc')} | {g('word_pairs_types_cc')} | "
                 f"{g('verbatim_6plus')} | {vb} | {y['windows_old']:,} → {y['windows_new']:,} | {y['multi_old']} → {y['multi_new']} |")
    L += ["", "Under entry 10 a verbatim window cannot span a no-source letter, so windows come only from stretches written "
          "in letters the gold covers; for Finnish (12.6% of letters without a source) this favours letters known to "
          "correspond, which raises the verbatim share. An implementation error found before these results were reported "
          "was corrected on 2026-10-27: after a break inside a word, the stretch's first letter had been counted as a word "
          "start, which produced spurious multi-word hits.", "",
          "Bootstrap intervals for the new values: `reports/v2/real_relatives/yardsticks.md` and `estonian.md`. The "
          "exploratory post-hoc check of 2026-10-24 (`estonian_sensitivity.md`, which filled the no-source rows from "
          "general knowledge) is superseded by this rule and kept as a dated record."]
    (A.CD / "entry10.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
