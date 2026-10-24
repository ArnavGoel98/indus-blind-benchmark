"""Pre-registration entry 9: Finnish-Estonian Task C/D tables, readings E1-E4 and the scorer diagnostic.

Reads runs/results/v2_cd/records_estonian.jsonl (seeds 0-2, primary), v2_cd_repl/records_estonian.jsonl
(seeds 3-5), v2_controls/records_estonian.jsonl (C1, C2), the Finnish `harsh` and v1 upper-bound values
of entries 6-7 (same corpora), and regenerates the corpora (no solver) for two diagnostics: the share of
sign tokens whose reflex silently drops a no-source letter (entry 9), and the logographic reachable share
(as reach_check.md). Falls back to the gzipped archives in reports/v2/cd/records/.
Usage (repository root): python reports/v2/cd/analysis/estonian_summary.py -> reports/v2/cd/estonian.{md,json}
"""
import gzip
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
from ibdb.data import relatives as R  # noqa: E402
from ibdb.generator.build import make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.methods.decipher import KnightEM  # noqa: E402

EM, EMO, FR = "knight2006_em", "knight2006_em_original", "baseline_frequency_rank"
OUT = A.CD
REL, TR, TC = "real:estonian", "related_real:estonian", "candidates_real:estonian"


def _recs(name: str, file: str) -> list[dict]:
    p = A.RUNS / name / file
    a = A.ARCHIVE / f"{name}_estonian.jsonl.gz"
    lines = p.read_text().splitlines() if p.exists() else (gzip.decompress(a.read_bytes()).decode().splitlines() if a.exists() else [])
    rs = [json.loads(x) for x in lines]
    bad = [r for r in rs if "error" in r]
    if bad:
        raise SystemExit(f"{name}: {len(bad)} records with errors")
    return rs


def pct(v):
    return f"{v:.1f}"


def cell(vals):
    lo, hi = A.boot(vals)
    return {"mean": float(np.mean(vals)), "lo": lo, "hi": hi, "n": len(vals), "values": vals}


def diagnostics() -> dict:
    """Per script type, mean over seeds 0-5 and both samplers: ceiling, silent-drop share, reachable share."""
    rel = RC.real_relative("finnish", "estonian")
    nosrc = {u for u, v in R.FINNISH_ESTONIAN.items() if v[0] is None}
    cap = KnightEM().max_units
    out = {}
    for st in cd_v2.SCRIPTS:
        d = {"ceiling": [], "silent_drop": [], "reachable": []}
        for smp, gv in cd_v2.SAMPLERS.items():
            for seed in range(6):
                knobs, spec = load_knobs("full", "finnish", st, gv)
                _, key, _ = make_corpus("finnish", spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
                logos = RC.hidden_logograms("finnish", spec.logogram_vocab) if st == "logosyllabic" else set()
                g = RC.Gold(rel, "finnish", st, logos)
                ref = RC.reference(rel, st, "finnish", spec.logogram_vocab)
                top = {u for u, _ in Counter(u for t in ref.texts for u in t).most_common(cap)}
                vals = Counter(v for t in key.token_values for v in t)
                n = sum(vals.values())
                rec = drop = reach = 0
                for v, m in vals.items():
                    r, phon, _ = g._value(v)
                    if r is None:
                        continue
                    rec += m
                    drop += m * any(p in nosrc for p in phon)
                    reach += m * (r in top)
                d["ceiling"].append(100 * rec / n)
                d["silent_drop"].append(100 * drop / n)
                d["reachable"].append(100 * reach / n)
        out[st] = {k: float(np.mean(v)) for k, v in d.items()}
    return out


def main() -> None:
    prim = _recs("v2_cd", "records_estonian.jsonl")
    repl = _recs("v2_cd_repl", "records_estonian.jsonl")
    ctrl = _recs("v2_controls", "records_estonian.jsonl")
    main_recs = [r for r in A.load_runs() if r["lang"] == "finnish"]
    upper = A.load_upper()
    assert len(prim) == 24 and len(repl) == 24 and len(ctrl) == 48, (len(prim), len(repl), len(ctrl))
    both = prim + repl
    res = {"cells": {}, "readings": {}}
    for st in cd_v2.SCRIPTS:
        c = {}
        for m in (EM, EMO, FR):
            for kind, seeds in (("s02", (0, 1, 2)), ("s35", (3, 4, 5)), ("s05", range(6))):
                vals = [100 * r["tiers"][TR][m]["strict"] for r in both if r["script_type"] == st and r["seed"] in seeds]
                c[f"{m}|{kind}"] = cell(vals)
        c["lenient|s02"] = cell([100 * r["tiers"][TR][EM]["lenient"] for r in prim if r["script_type"] == st])
        c["ceiling|s02"] = cell([100 * r["tiers"][TR][EM]["recoverable"] for r in prim if r["script_type"] == st])
        c["harsh|s02"] = cell(A.values(main_recs, upper, "finnish", st, "related", "harsh", (0, 1, 2)))
        c["upper|s02"] = cell(A.values(main_recs, upper, "finnish", st, "related", "upper", (0, 1, 2)))
        c["floor|s05"] = cell([100 * r["floor"][REL] for r in ctrl if r["script_type"] == st])
        for u in ("latin", "tamil"):
            c[f"unrel_{u}|s05"] = cell([100 * r["unrelated"][u][EM][REL]["strict"] for r in ctrl if r["script_type"] == st])
        # candidates tier: picks (revised EM) and strict
        cand = [r["tiers"][TC][EM] for r in prim if r["script_type"] == st]
        c["cand_picks|s02"] = sum(x["reference"] == "estonian" for x in cand)
        c["cand_strict|s02"] = cell([100 * x["strict"] for x in cand])
        c["cand_refs|s02"] = dict(Counter(x["reference"] for x in cand))
        res["cells"][st] = c
        # Readings
        key = lambda r: (r["seed"], r["sampler"])  # noqa: E731
        relv = {key(r): 100 * r["tiers"][TR][EM]["strict"] for r in both if r["script_type"] == st}
        unrel = {u: {key(r): 100 * r["unrelated"][u][EM][REL]["strict"] for r in ctrl if r["script_type"] == st}
                 for u in ("latin", "tamil")}
        best = max(unrel, key=lambda u: np.mean(list(unrel[u].values())))
        added = np.mean(list(relv.values())) - np.mean(list(unrel[best].values()))
        wins = sum(relv[k] > unrel[best][k] for k in relv)
        mean05 = c[f"{EM}|s05"]["mean"]
        res["readings"][st] = {
            "E1_at_floor": bool(mean05 - c["floor|s05"]["mean"] <= 2), "E1_gap": mean05 - c["floor|s05"]["mean"],  # as controls.md
            "E2_best_unrelated": best, "E2_added": float(added), "E2_wins": int(wins),
            "E2_helps": bool(added >= 5 and wins >= 9),
            "E3_minus_harsh": c[f"{EM}|s02"]["mean"] - c["harsh|s02"]["mean"],
            "E4_picks": c["cand_picks|s02"]}
    res["diagnostics"] = diagnostics()
    (OUT / "estonian.json").write_text(json.dumps(res, indent=1, default=float))
    write_md(res)


def write_md(res: dict) -> None:
    C, Rd, D = res["cells"], res["readings"], res["diagnostics"]
    iv = lambda c: f"{pct(c['mean'])} [{pct(c['lo'])}, {pct(c['hi'])}]"  # noqa: E731
    L = ["# Finnish-Estonian, Tasks C and D (pre-registration entry 9)", "",
         "Hidden Finnish (Indus-point corpora, 2,906 texts, mean length 4.6) against Kalevipoeg, normalised spelling. "
         "Gold from the word pairs printed in Pajusalu (2012), 13 of 27 rows with a regular reflex; reported in its own rows and "
         "not pooled with the other pairs. Revised EM, strict, `related_real:estonian` unless stated; % of sign tokens. "
         "Seeds 0-2 primary; brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only.", "",
         "## Task D", "",
         "| Script | Revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | Lenient 0-2 | Ceiling | `harsh` 0-2 | v1 sister 0-2 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for st, c in C.items():
        L.append(f"| {st} | {iv(c[EM + '|s02'])} | {pct(c[EM + '|s35']['mean'])} | {iv(c[EM + '|s05'])} | "
                 f"{pct(c[EMO + '|s02']['mean'])} | {pct(c[FR + '|s02']['mean'])} | {pct(c['lenient|s02']['mean'])} | "
                 f"{pct(c['ceiling|s02']['mean'])} | {pct(c['harsh|s02']['mean'])} | {pct(c['upper|s02']['mean'])} |")
    L += ["", "## Readings (fixed in entry 9 before the run)", "",
          "| Script | E1: floor (C2), pooled | E1: reading (gap) | E2: better unrelated ref., mean | E2: added value; paired wins | E2: measurably helps? | E3: minus `harsh` (0-2) | E4: picks Estonian (of 6) |",
          "|---|---|---|---|---|---|---|---|"]
    for st, r in Rd.items():
        c = C[st]
        L.append(f"| {st} | {pct(c['floor|s05']['mean'])} | {'at the floor' if r['E1_at_floor'] else 'above the floor'} ({r['E1_gap']:+.1f}) | "
                 f"{r['E2_best_unrelated'].capitalize()}, {pct(c['unrel_' + r['E2_best_unrelated'] + '|s05']['mean'])} | "
                 f"{r['E2_added']:+.1f}; {r['E2_wins']} of 12 | {'yes' if r['E2_helps'] else 'no'} | "
                 f"{r['E3_minus_harsh']:+.1f} | {r['E4_picks']} |")
    L += ["", "E4 counts the 6 seeds 0-2 corpora per script type (24 in all: "
          f"{sum(r['E4_picks'] for r in Rd.values())}). References chosen in `candidates_real:estonian`: "
          + "; ".join(f"{st}: " + ", ".join(f"{k} {v}" for k, v in sorted(C[st]['cand_refs|s02'].items(), key=lambda kv: -kv[1]))
                      for st in C) + ".", "",
          "*At the floor* = no more than 2 points above the C2 floor, as in `controls.md` (entry 8).", "", "## Scorer diagnostics (entry 9; no solver)", "",
          "| Script | Ceiling | Tokens whose reflex silently drops a no-source letter | Ceiling reachable by the solver (top 250 units) |",
          "|---|---|---|---|"]
    for st, d in D.items():
        L.append(f"| {st} | {pct(d['ceiling'])} | {pct(d['silent_drop'])} | {pct(d['reachable'])} |")
    L += ["", "The middle column is an upper bound on how far the frozen scorer's handling of \"no source\" rows can raise "
          "a score (entry 9): such tokens count as recoverable with a shortened reflex. Seeds 0-5, both samplers.", "",
          "**Frozen-code notes.** The syllable cutter uses the hidden language's vowel set, so Estonian õ and ü (not "
          "Finnish letters) are cut as consonants in the Estonian reference; neither is the regular reflex of any "
          "Finnish letter in this gold."]
    (OUT / "estonian.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
