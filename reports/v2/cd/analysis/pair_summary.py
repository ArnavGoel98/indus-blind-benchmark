"""Task C/D report for one hidden language and its real relatives, in the format of entry 9's estonian.md.

Reads the entry-10 rerun records (runs/results/v2_e10 or its archive: seeds 0-5, both samplers, the
real-relative tiers, C1 unrelated references and C2 floors, scored with the entry-10 rule), the `harsh`
and v1-sister values of entries 6-7 (same corpora), and regenerates the corpora (no solver) for the
ceilings: raw (entry 10), raw before entry 10 (no-source letters dropped) and reachable by the solver
(entry 11: primary). The references are cut as the runs cut them (frozen-v2 cutter, the relative's own
vowel letters not added); entry 11's effect on seeds 0-2 is in entry11.md.
Readings, as fixed before each run: at the floor (C2, entry 8), measurably helps (C1, entry 8), the
difference from `harsh` (descriptive), the corpora in which the relative is picked in `candidates_real`
(R4, entry 7; E4, entry 9). Used by estonian_summary.py and dravidian_summary.py.
"""
import dataclasses
import json
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ["IBDB_SISTER_VERSION"] = "v2"
import cd_v2  # noqa: E402
import v2_analysis as A  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.data.gold import old_semantics  # noqa: E402
from ibdb.generator.build import make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.methods.decipher import KnightEM  # noqa: E402

EM, EMO, FR = "knight2006_em", "knight2006_em_original", "baseline_frequency_rank"
UNREL = {"finnish": ("latin", "tamil"), "tamil": ("latin", "finnish")}


def pct(v):
    return f"{v:.1f}"


def cell(vals):
    lo, hi = A.boot(vals)
    return {"mean": float(np.mean(vals)), "lo": lo, "hi": hi, "n": len(vals), "values": vals}


def records(lang: str) -> list[dict]:
    """Entry-10 records of `lang` with the new scores in place (old ones dropped)."""
    rs = [r for r in (json.loads(x) for x in A._lines("v2_e10") or []) if r.get("lang") == lang and "error" not in r]
    if len(rs) != 48:
        raise SystemExit(f"entry-10 records for {lang}: {len(rs)} of 48")
    strip = lambda x: {k: v for k, v in x.items() if k != "old"}  # noqa: E731
    return [{**r, "tiers": {t: {m: strip(x) for m, x in ms.items()} for t, ms in r["tiers"].items()},
             "floor": {g: v["new"] for g, v in r["floor"].items()},
             "unrelated": {u: {m: {g: (strip(x) if isinstance(x, dict) and "strict" in x else x) for g, x in gs.items()}
                               for m, gs in ms.items()} for u, ms in r["unrelated"].items()}} for r in rs]


def ceilings(lang: str, rels: list[str]) -> dict:
    """(relative, script) -> per (seed, sampler): raw ceiling, raw before entry 10, reachable (frozen-v2 cut)."""
    cap = KnightEM().max_units
    out = {}
    for name in rels:
        rel = dataclasses.replace(RC.real_relative(lang, name), vowels=frozenset())   # as the runs cut it
        rel_old = dataclasses.replace(rel, regular=old_semantics(rel.regular))
        for st in cd_v2.SCRIPTS:
            d = {}
            for smp, gv in cd_v2.SAMPLERS.items():
                for seed in range(6):
                    knobs, spec = load_knobs("full", lang, st, gv)
                    _, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
                    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
                    g, go = RC.Gold(rel, lang, st, logos), RC.Gold(rel_old, lang, st, logos)
                    ref = RC.reference(rel, st, lang, spec.logogram_vocab)
                    vals = Counter(v for t in key.token_values for v in t)
                    n = sum(vals.values())
                    d[f"{seed}{smp}"] = {"raw": 100 * sum(m for v, m in vals.items() if g.recoverable(v)) / n,
                                         "raw_old": 100 * sum(m for v, m in vals.items() if go.recoverable(v)) / n,
                                         "reachable": 100 * RC.reachable(ref, key, g, cap)}
            out[f"{name}|{st}"] = d
    return out


def summarise(lang: str, rels: list[str]) -> dict:
    recs = records(lang)
    main_recs = [r for r in A.load_runs() if r["lang"] == lang]
    upper = A.load_upper()
    ceil = ceilings(lang, rels)
    res = {"lang": lang, "relatives": rels, "cells": {}, "readings": {}, "ceilings": {}}
    key = lambda r: (r["seed"], r["sampler"])  # noqa: E731
    for name in rels:
        TR, TC, REL = f"related_real:{name}", f"candidates_real:{name}", f"real:{name}"
        for st in cd_v2.SCRIPTS:
            rs = sorted((r for r in recs if r["script_type"] == st), key=lambda r: r["seed"] >= 3)   # 0-2, then 3-5
            prim = [r for r in rs if r["seed"] < 3]
            c = {}
            for m in (EM, EMO, FR):
                for kind, seeds in (("s02", (0, 1, 2)), ("s35", (3, 4, 5)), ("s05", range(6))):
                    c[f"{m}|{kind}"] = cell([100 * r["tiers"][TR][m]["strict"] for r in rs if r["seed"] in seeds])
            c["lenient|s02"] = cell([100 * r["tiers"][TR][EM]["lenient"] for r in prim])
            cv = ceil[f"{name}|{st}"]
            for k in ("raw", "raw_old", "reachable"):
                c[f"{k}|s02"] = cell([v[k] for s, v in cv.items() if int(s[0]) < 3])
                c[f"{k}|s05"] = cell([v[k] for v in cv.values()])
            assert abs(c["raw|s02"]["mean"] - np.mean([100 * r["tiers"][TR][EM]["recoverable"] for r in prim])) < 1e-9
            c["harsh|s02"] = cell(A.values(main_recs, upper, lang, st, "related", "harsh", (0, 1, 2)))
            c["upper|s02"] = cell(A.values(main_recs, upper, lang, st, "related", "upper", (0, 1, 2)))
            c["floor|s05"] = cell([100 * r["floor"][REL] for r in rs])
            for u in UNREL[lang]:
                c[f"unrel_{u}|s05"] = cell([100 * r["unrelated"][u][EM][REL]["strict"] for r in rs])
            cand = [r["tiers"][TC][EM] for r in prim]
            c["cand_picks|s02"] = sum(x["reference"] == name for x in cand)
            c["cand_refs|s02"] = dict(Counter(x["reference"] for x in cand))
            c["cand_picks|s35"] = sum(r["tiers"][TC][EM]["reference"] == name for r in rs if r["seed"] >= 3)
            relv = {key(r): 100 * r["tiers"][TR][EM]["strict"] for r in rs}
            unrel = {u: {key(r): 100 * r["unrelated"][u][EM][REL]["strict"] for r in rs} for u in UNREL[lang]}
            best = max(unrel, key=lambda u: np.mean(list(unrel[u].values())))
            added = float(np.mean(list(relv.values())) - np.mean(list(unrel[best].values())))
            wins = sum(relv[k] > unrel[best][k] for k in relv)
            gap = c[f"{EM}|s05"]["mean"] - c["floor|s05"]["mean"]
            res["cells"][f"{name}|{st}"] = c
            res["readings"][f"{name}|{st}"] = {
                "at_floor": bool(gap <= 2), "gap": gap, "best_unrelated": best, "added": added, "wins": int(wins),
                "helps": bool(added >= 5 and wins >= 9), "minus_harsh": c[f"{EM}|s02"]["mean"] - c["harsh|s02"]["mean"],
                "picks": c["cand_picks|s02"]}
    return res


def write_md(res: dict, path: Path, title: str, intro: str, label: dict, notes: list[str]) -> None:
    C, Rd = res["cells"], res["readings"]
    iv = lambda c: f"{pct(c['mean'])} [{pct(c['lo'])}, {pct(c['hi'])}]"  # noqa: E731
    L = [f"# {title}", "", intro, "",
         "## Task D", "",
         "| Relative | Script | Revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | "
         "Lenient 0-2 | Reachable ceiling 0-2 (primary) | Raw ceiling 0-2 | `harsh` (synthetic, optimistic) 0-2 | "
         "v1 sister (synthetic, optimistic) 0-2 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, c in C.items():
        name, st = k.split("|")
        L.append(f"| {label[name]} | {st} | {iv(c[EM + '|s02'])} | {pct(c[EM + '|s35']['mean'])} | {iv(c[EM + '|s05'])} | "
                 f"{pct(c[EMO + '|s02']['mean'])} | {pct(c[FR + '|s02']['mean'])} | {pct(c['lenient|s02']['mean'])} | "
                 f"{pct(c['reachable|s02']['mean'])} | {pct(c['raw|s02']['mean'])} | {pct(c['harsh|s02']['mean'])} | "
                 f"{pct(c['upper|s02']['mean'])} |")
    L += ["", "## Readings (fixed before each run)", "",
          "| Relative | Script | Floor (C2), pooled | At the floor? (gap) | Better unrelated ref., mean | Added value; paired wins | "
          "Measurably helps? (C1) | Minus `harsh` (0-2) | Picks the relative (of 6, seeds 0-2) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for k, r in Rd.items():
        name, st = k.split("|")
        c = C[k]
        L.append(f"| {label[name]} | {st} | {pct(c['floor|s05']['mean'])} | "
                 f"{'at the floor' if r['at_floor'] else 'above the floor'} ({r['gap']:+.1f}) | "
                 f"{r['best_unrelated'].capitalize()}, {pct(c['unrel_' + r['best_unrelated'] + '|s05']['mean'])} | "
                 f"{r['added']:+.1f}; {r['wins']} of 12 | {'yes' if r['helps'] else 'no'} | {r['minus_harsh']:+.1f} | {r['picks']} |")
    L += [""]
    for name in res["relatives"]:
        ks = [k for k in C if k.startswith(name + "|")]
        L.append(f"{label[name]}: picked in {sum(Rd[k]['picks'] for k in ks)} of 24 seeds 0-2 corpora "
                 f"(seeds 3-5: {sum(C[k]['cand_picks|s35'] for k in ks)} of 24). References chosen in "
                 f"`candidates_real:{name}`, seeds 0-2: "
                 + "; ".join(f"{k.split('|')[1]}: " + ", ".join(f"{a} {b}" for a, b in sorted(C[k]['cand_refs|s02'].items(),
                                                                                            key=lambda kv: -kv[1])) for k in ks) + ".")
        L.append("")
    L += ["*At the floor* = no more than 2 points above the C2 floor; *measurably helps* = at least 5 points above the "
          "better unrelated reference and ahead of it in at least 9 of the 12 paired corpora (entry 8). The difference "
          "from `harsh` is descriptive (no test).", "",
          "## Ceilings (no solver; seeds 0-5, both samplers)", "",
          "| Relative | Script | Reachable by the solver (top 250 units; primary, entry 11) | Raw ceiling, entry 10 "
          "(no source = unknown) | Raw ceiling before entry 10 (no-source letters dropped) |",
          "|---|---|---|---|---|"]
    for k, c in C.items():
        name, st = k.split("|")
        L.append(f"| {label[name]} | {st} | {pct(c['reachable|s05']['mean'])} | {pct(c['raw|s05']['mean'])} | "
                 f"{pct(c['raw_old|s05']['mean'])} |")
    L += ["", "*Reachable* is the share of sign tokens whose strict regular reflex is among the reference's 250 most "
          "frequent units, the only units the EM solver can predict (entry 11 makes it the primary ceiling). The "
          "references are cut as these runs cut them (frozen-v2 cutter). Before entry 10 the harness dropped a no-source "
          "letter from a syllable or word reflex, so such tokens counted as recoverable with a shortened reflex; entry 10 "
          "makes them unrecoverable.", ""] + notes
    path.write_text("\n".join(L) + "\n")
    print("\n".join(L))
