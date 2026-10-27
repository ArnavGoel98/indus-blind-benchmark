"""v2 final run (seeds 6-11): the report fixed in docs/v2_final_run_readings.md, section 7.

Reads runs/results/v2_final/records.jsonl and v2_final_c4/records.jsonl (or their archives in
reports/v2/final/records/), evaluates readings H1-H8 and D1-D8 exactly as defined there, and writes
reports/v2/final/results.{md,json}: readings not met and process failures first, then readings met, then
tables T1-T7. The development answers (seeds 0-5) are read from the development reports, not typed in.
`--dir DIR` reads a pipeline-check directory instead (scripts/v2/final_v2.py --dev); its output is
labelled as not a result and written into DIR.
Usage (repository root): python reports/v2/final/analysis/final_summary.py [--dir DIR]
"""
import argparse
import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "reports" / "v2" / "cd" / "analysis"))
import v2_analysis as A  # noqa: E402  (boot, archives)

OUT = ROOT / "reports" / "v2" / "final"
EM, EMO, FR = "knight2006_em", "knight2006_em_original", "baseline_frequency_rank"
METHODS = {EM: "revised EM", EMO: "original EM", FR: "frequency rank"}
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
PAIRS = [("latin", "italian"), ("tamil", "malayalam"), ("tamil", "kannada"), ("finnish", "estonian")]
LABEL = {"italian": "Italian (descendant of Latin)", "malayalam": "Malayalam (descendant of Old Tamil)",
         "kannada": "Kannada (sister of Old Tamil)",
         "estonian": "Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters)"}
UNREL = {"latin": ["tamil", "finnish"], "tamil": ["latin", "finnish"], "finnish": ["latin", "tamil"]}
SEEDS, C3_SEEDS = (6, 7, 8, 9, 10, 11), (6, 7, 8)
SAMPLERS = ("A", "B")
PIPELINE = False          # --dir: a pipeline check, whose C3 runs on the development seed
UGARITIC = 32.0
CHECK_KEYS = ("tiers", "ceiling", "floor", "unrelated", "budget", "v1_sister", "n_tokens", "family")


def _read(name: str, d: Path | None) -> list[dict] | None:
    p = (d or ROOT / "runs" / "results" / name) / "records.jsonl"
    a = OUT / "records" / f"{name}.jsonl.gz"
    if p.exists():
        lines = p.read_text().splitlines()
    elif d is None and a.exists():
        lines = gzip.decompress(a.read_bytes()).decode().splitlines()
    else:
        return None
    return [json.loads(x) for x in lines]


def corpus_key(r):
    return (r["lang"], r["script_type"], r["seed"], r["sampler"])


def latest(rs: list[dict]) -> tuple[dict, list[dict]]:
    """Last successful record per corpus; records of corpora that never succeeded."""
    ok = {corpus_key(r): r for r in rs if "error" not in r}
    failed = [r for r in rs if "error" in r and corpus_key(r) not in ok]
    return ok, failed


def v1(x: dict) -> float:
    """v1-sister score before the cognate step; token accuracy when no cognate step ran (as v2_analysis.load_upper)."""
    return x["token_acc_before_cognate"] if x.get("token_acc_before_cognate") is not None else x["token_acc"]


def mean(v):
    return float(np.mean(v)) if v else math.nan


def cell(v):
    lo, hi = A.boot(v)
    return {"mean": mean(v), "lo": lo, "hi": hi, "n": len(v), "ge50": int(sum(x >= 50 for x in v))}


def pair_cells(recs: dict) -> dict:
    out = {}
    for lang, rel in PAIRS:
        g, TR, TC = f"real:{rel}", f"related_real:{rel}", f"candidates_real:{rel}"
        for st in SCRIPTS:
            rs = sorted((r for k, r in recs.items() if k[0] == lang and k[1] == st and TR in r["tiers"]),
                        key=lambda r: (r["seed"], r["sampler"]))
            pk = [(r["seed"], r["sampler"]) for r in rs]
            real = [100 * r["tiers"][TR][EM]["strict"] for r in rs]
            unrel = {u: [100 * r["unrelated"][u][EM][g]["strict"] for r in rs] for u in UNREL[lang]}
            best = max(unrel, key=lambda u: mean(unrel[u])) if rs else UNREL[lang][0]
            b3 = [r for r in rs if (r["seed"] in C3_SEEDS or PIPELINE) and g in r.get("budget", {})]
            c = {"n": len(rs), "keys": pk, "real": cell(real), "real_values": real,
                 "emo": mean([100 * r["tiers"][TR][EMO]["strict"] for r in rs]),
                 "fr": mean([100 * r["tiers"][TR][FR]["strict"] for r in rs]),
                 "lenient": mean([100 * r["tiers"][TR][EM]["lenient"] for r in rs]),
                 "reachable": mean([100 * r["ceiling"][g]["reachable"] for r in rs]),
                 "raw": mean([100 * r["ceiling"][g]["raw"] for r in rs]),
                 "harsh": cell([100 * r["tiers"]["related_harsh"][EM]["strict"] for r in rs]),
                 "upper": cell([100 * v1(r["v1_sister"]["related"][EM]) for r in rs]),
                 "floor": mean([100 * r["floor"][g] for r in rs]),
                 "unrel": {u: mean(v) for u, v in unrel.items()}, "best_unrel": best,
                 "added": mean(real) - mean(unrel[best]),
                 "wins": int(sum(a > b for a, b in zip(real, unrel[best]))),
                 "picks": int(sum(r["tiers"][TC][EM]["reference"] == rel for r in rs)),
                 "refs": dict(Counter(r["tiers"][TC][EM]["reference"] for r in rs)),
                 "family": {m: mean([100 * r["tiers"][TC][m]["family_correct"] for r in rs]) for m in METHODS},
                 "c3": {"n": len(b3), "r3": mean([100 * r["tiers"][TR][EM]["strict"] for r in b3]),
                        "r10": mean([100 * r["budget"][g]["10"]["strict"] for r in b3])}}
            c["helps"] = bool(c["added"] >= 5 and c["wins"] >= 9)
            c["gap"] = c["real"]["mean"] - c["floor"]
            c["at_floor"] = bool(c["gap"] <= 2)
            c["c3"]["delta"] = c["c3"]["r10"] - c["c3"]["r3"]
            c["c3"]["first_order"] = bool(abs(c["c3"]["delta"]) > 10)
            out[(rel, st)] = c
    return out


def synthetic(recs: dict) -> dict:
    out = {}
    for lang in LANGS:
        for st in SCRIPTS:
            rs = [r for k, r in recs.items() if k[0] == lang and k[1] == st]
            for kind in ("related", "candidates"):
                out[(lang, st, kind, "harsh")] = cell([100 * r["tiers"][f"{kind}_harsh"][EM]["strict"] for r in rs])
                out[(lang, st, kind, "upper")] = cell([100 * v1(r["v1_sister"][kind][EM]) for r in rs])
            out[(lang, st, "family_v1")] = mean([100 * r["v1_sister"]["candidates"][EM]["family_correct"] for r in rs])
            out[(lang, st, "family_harsh")] = mean([100 * r["tiers"]["candidates_harsh"][EM]["family_correct"] for r in rs])
    return out


def _leaves(x, path=""):
    if isinstance(x, dict):
        for k in sorted(x):
            yield from _leaves(x[k], f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _leaves(v, f"{path}/{i}")
    else:
        yield path, x


def determinism(main: dict, c4: dict | None) -> dict:
    if c4 is None:
        return {"run": False, "compared": 0, "mismatches": [], "corpora": 0, "missing": []}
    n, mism, missing = 0, [], []
    for k, r in c4.items():
        if k not in main:
            missing.append(list(k))
            continue
        a = dict(_leaves({x: main[k].get(x) for x in CHECK_KEYS}))
        b = dict(_leaves({x: r.get(x) for x in CHECK_KEYS}))
        for p in sorted(set(a) | set(b)):
            n += 1
            if a.get(p) != b.get(p):
                mism.append({"corpus": list(k), "path": p, "run": a.get(p), "rerun": b.get(p)})
    return {"run": True, "compared": n, "mismatches": mism, "corpora": len(c4), "missing": missing}


def dev_answers() -> dict:
    """Development answers (seeds 0-5), read from the development reports and archives."""
    page = json.loads((A.CD / "page_data.json").read_text())
    pc = {(c["tier"], c["lang"], c["rel"], c["script"]): c["mean"] for c in page["cells"]}
    ctrl = {(c["rel"], c["script"]): c for c in page["controls"]}
    est = json.loads((A.CD / "estonian.json").read_text())
    dev = {}
    for lang, rel in PAIRS:
        for st in SCRIPTS:
            if rel == "estonian":
                c, r = est["cells"][f"estonian|{st}"], est["readings"][f"estonian|{st}"]
                real, floor = c[f"{EM}|s05"]["mean"], c["floor|s05"]["mean"]
                added, wins, helps = r["added"], r["wins"], r["helps"]
            else:
                c = ctrl[(rel, st)]
                real, floor, added, wins, helps = c["real"], c["floor"], c["added"], c["wins"], c["helps"]
            harsh = pc[("related", lang, "harsh", st)]
            upper = pc[("related", lang, "upper", st)]
            dev[(rel, st)] = {"real": real, "floor": floor, "at_floor": real - floor <= 2, "added": added, "wins": wins,
                              "helps": helps, "harsh": harsh, "upper": upper}
    picks = Counter()
    for n in ("v2_cd", "v2_cd_repl"):
        for r in (json.loads(x) for x in A._lines(n) or []):
            for rel in ("italian", "malayalam", "kannada"):
                t = f"candidates_real:{rel}"
                if "error" not in r and t in r["tiers"]:
                    picks[rel] += r["tiers"][t][EM]["reference"] == rel
    picks["estonian"] = sum(est["cells"][f"estonian|{st}"]["cand_picks|s02"] + est["cells"][f"estonian|{st}"]["cand_picks|s35"]
                            for st in SCRIPTS)
    dev["picks"] = dict(picks)
    return dev


def evaluate_readings(C: dict, det: dict, dev: dict | None) -> list[dict]:
    f = lambda v: f"{v:.1f}"  # noqa: E731
    nonlog = [s for s in SCRIPTS if s != "logographic"]
    R = []

    def add(i, text, thr, met, value, dmet, dvalue):
        R.append({"id": i, "reading": text, "threshold": thr, "met": met, "value": value, "dev_met": dmet,
                  "dev_value": dvalue, "agrees": None if dmet is None else (met == dmet)})

    top = max(C, key=lambda k: C[k]["real"]["mean"])
    dtop = max(((k, v) for k, v in (dev or {}).items() if isinstance(k, tuple)), key=lambda kv: kv[1]["real"], default=None)
    add("H1", "Every real-relative cell mean is below 50%", "16 of 16 cells < 50.0",
        all(c["real"]["mean"] < 50 for c in C.values()),
        f"{sum(c['real']['mean'] < 50 for c in C.values())} of {len(C)} below; highest {f(C[top]['real']['mean'])} "
        f"({top[0].capitalize()}, {top[1]})",
        None if not dev else all(v["real"] < 50 for k, v in dev.items() if isinstance(k, tuple)),
        None if not dtop else f"highest {f(dtop[1]['real'])} ({dtop[0][0].capitalize()}, {dtop[0][1]})")
    for i, rel in (("H2a", "estonian"), ("H2b", "kannada")):
        c, d = C[(rel, "alphabetic")], (dev or {}).get((rel, "alphabetic"))
        add(i, f"{rel.capitalize()} measurably helps on alphabetic scripts (C1 rule)", ">= 5.0 points and >= 9 of 12 paired wins",
            c["helps"], f"{c['added']:+.1f}; {c['wins']} of {c['n']}", None if not d else d["helps"],
            None if not d else f"{d['added']:+.1f}; {d['wins']} of 12")
    cells8 = [(rel, st) for _, rel in PAIRS for st in ("syllabic", "logosyllabic")]
    hs = [k for k in cells8 if C[k]["helps"]]
    dhs = [k for k in cells8 if dev and dev[k]["helps"]]
    add("H3", "On syllabic and logo-syllabic scripts, a real relative measurably helps in at most 1 of the 8 cells",
        "count <= 1", len(hs) <= 1, f"{len(hs)}" + (": " + ", ".join(f"{r.capitalize()} {s}" for r, s in hs) if hs else ""),
        None if not dev else len(dhs) <= 1, None if not dev else f"{len(dhs)}: " + ", ".join(f"{r.capitalize()} {s}" for r, s in dhs))
    below = [(rel, st) for _, rel in PAIRS for st in nonlog if C[(rel, st)]["real"]["mean"] < C[(rel, st)]["upper"]["mean"]]
    dbelow = [(rel, st) for _, rel in PAIRS for st in nonlog if dev and dev[(rel, st)]["real"] < dev[(rel, st)]["upper"]]
    add("H4", "Every real relative scores below the v1 sister in each syllabic, logo-syllabic and alphabetic cell",
        "12 of 12 cells", len(below) == 12, f"{len(below)} of 12" + ("" if len(below) == 12 else "; not below: " + ", ".join(
            f"{r.capitalize()} {s} ({f(C[(r, s)]['real']['mean'])} vs {f(C[(r, s)]['upper']['mean'])})"
            for _, r in PAIRS for s in nonlog if (r, s) not in below)),
        None if not dev else len(dbelow) == 12, None if not dev else f"{len(dbelow)} of 12")
    m, k = C[("malayalam", "alphabetic")]["real"]["mean"], C[("kannada", "alphabetic")]["real"]["mean"]
    dm, dk = (dev[("malayalam", "alphabetic")]["real"], dev[("kannada", "alphabetic")]["real"]) if dev else (None, None)
    inr = lambda v: UGARITIC - 10 <= v <= UGARITIC + 10  # noqa: E731
    add("H5", "Old Tamil alphabetic with Malayalam and with Kannada both within 10 points of the Ugaritic result (32.0%)",
        "both in 22.0-42.0", inr(m) and inr(k), f"{f(m)} and {f(k)}", None if not dev else inr(dm) and inr(dk),
        None if not dev else f"{f(dm)} and {f(dk)}")
    ia, isy = C[("italian", "alphabetic")], C[("italian", "syllabic")]
    da, ds = (dev or {}).get(("italian", "alphabetic")), (dev or {}).get(("italian", "syllabic"))
    add("H6", "Italian below `harsh` on alphabetic and on syllabic scripts", "both cells",
        ia["real"]["mean"] < ia["harsh"]["mean"] and isy["real"]["mean"] < isy["harsh"]["mean"],
        f"{f(ia['real']['mean'])} vs {f(ia['harsh']['mean'])}; {f(isy['real']['mean'])} vs {f(isy['harsh']['mean'])}",
        None if not dev else da["real"] < da["harsh"] and ds["real"] < ds["harsh"],
        None if not dev else f"{f(da['real'])} vs {f(da['harsh'])}; {f(ds['real'])} vs {f(ds['harsh'])}")
    pk = {rel: sum(C[(rel, st)]["picks"] for st in SCRIPTS) for _, rel in PAIRS}
    nk = {rel: sum(C[(rel, st)]["n"] for st in SCRIPTS) for _, rel in PAIRS}
    add("H7", "Revised EM picks the real relative in fewer than half of its `candidates_real` corpora: Italian, Malayalam, Kannada",
        "each < half (<= 23 of 48)", all(pk[r] < nk[r] / 2 for r in ("italian", "malayalam", "kannada")),
        "; ".join(f"{r.capitalize()} {pk[r]} of {nk[r]}" for r in ("italian", "malayalam", "kannada")),
        None if not dev else all(dev["picks"][r] < 24 for r in ("italian", "malayalam", "kannada")),
        None if not dev else "; ".join(f"{r.capitalize()} {dev['picks'][r]} of 48" for r in ("italian", "malayalam", "kannada")))
    add("H8", "Determinism (C4): every compared value identical", "0 mismatches, 24 corpora",
        det["run"] and not det["mismatches"] and not det["missing"] and det["corpora"] == 24,
        "not run" if not det["run"] else f"{det['compared'] - len(det['mismatches']):,} of {det['compared']:,} values identical "
        f"in {det['corpora']} corpora", True if dev else None, "met: 120 of 120 (entry 8); 3,348 of 3,348 (entry 10)" if dev else None)
    return R


def write(res: dict, path: Path, pipeline: bool) -> None:
    f = lambda v: "-" if v is None or (isinstance(v, float) and math.isnan(v)) else f"{v:.1f}"  # noqa: E731
    iv = lambda c: f"{f(c['mean'])} [{f(c['lo'])}, {f(c['hi'])}]"  # noqa: E731
    C, R, P, S = res["cells"], res["readings"], res["process"], res["synthetic"]
    L = ["# v2 final run, seeds 6-11: results against the pre-registered readings", ""]
    if pipeline:
        L += ["**PIPELINE CHECK ONLY: development seed 90, sampler A, 1 restart. These numbers are not results and are "
              "not reported.**", ""]
    L += ["Readings, thresholds and layout fixed in `docs/v2_final_run_readings.md` (entry 12) before any seed 6-11 corpus "
          "existed. Revised EM, strict, `related` tier, % of sign tokens, mean over the corpora of each cell (12 when complete); "
          "brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only. No test is made. "
          "Seeds 0-5 are the development set; their answers are shown beside each reading, not pooled. Finnish-Estonian "
          "gold is weak (10 word pairs, 13 of 27 letters). The synthetic sisters are optimistic upper references.", ""]
    fails = [r for r in R if not r["met"]]
    L += ["## 1. Readings not met", ""]
    L += [f"- **{r['id']}** {r['reading']}. Threshold: {r['threshold']}. Seeds 6-11: {r['value']}. "
          f"Development: {r['dev_value'] or '-'}." for r in fails] or ["None."]
    L += ["", "## Process failures", ""]
    pf = [f"- Missing corpora (failed twice or never run): {len(P['missing'])} of {P['expected']}"
          + (": " + "; ".join(" ".join(map(str, k)) for k in P["missing"][:20]) if P["missing"] else "")]
    pf += [f"- Errors recorded (including retried corpora): {P['errors']}"]
    d = res["determinism"]
    pf += [f"- C4: {'not run' if not d['run'] else str(len(d['mismatches'])) + ' mismatches in ' + format(d['compared'], ',') + ' values'}"
           + ("" if not d.get("missing") else f"; {len(d['missing'])} C4 corpora missing from the main run")]
    L += pf + ["", "## 2. Readings met", ""]
    L += [f"- **{r['id']}** {r['reading']}. Seeds 6-11: {r['value']}. Development: {r['dev_value'] or '-'}."
          for r in R if r["met"]] or ["None."]
    L += ["", "## T1. Readings", "", "| ID | Reading | Threshold | Seeds 6-11 value | Met? | Development answer | Agrees? |",
          "|---|---|---|---|---|---|---|"]
    yn = lambda b: "-" if b is None else ("yes" if b else "no")  # noqa: E731
    L += [f"| {r['id']} | {r['reading']} | {r['threshold']} | {r['value']} | {yn(r['met'])} | {r['dev_value'] or '-'} | "
          f"{yn(r['agrees'])} |" for r in R]
    L += ["", "## T2. Task D per pair", "",
          "| Relative | Script | Revised EM mean [95% CI] | Corpora >= 50% | Original EM | Frequency rank | Lenient | "
          "Reachable ceiling (primary) | Raw ceiling | `harsh` (synthetic, optimistic) | v1 sister (synthetic, optimistic) |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for (rel, st), c in C.items():
        L.append(f"| {LABEL[rel]} | {st} | {iv(c['real'])} | {c['real']['ge50']} of {c['n']} | {f(c['emo'])} | {f(c['fr'])} | "
                 f"{f(c['lenient'])} | {f(c['reachable'])} | {f(c['raw'])} | {iv(c['harsh'])} | {iv(c['upper'])} |")
    L += ["", "## T3. Controls per pair", "",
          "| Relative | Script | Floor (C2) | At the floor? (gap) | Better unrelated ref., mean | Added value; paired wins | "
          "Measurably helps? | Minus `harsh` | Minus v1 sister | Picks the relative |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for (rel, st), c in C.items():
        L.append(f"| {LABEL[rel]} | {st} | {f(c['floor'])} | {'at the floor' if c['at_floor'] else 'above the floor'} "
                 f"({c['gap']:+.1f}) | {c['best_unrel'].capitalize()}, {f(c['unrel'][c['best_unrel']])} | {c['added']:+.1f}; "
                 f"{c['wins']} of {c['n']} | {yn(c['helps'])} | {c['real']['mean'] - c['harsh']['mean']:+.1f} | "
                 f"{c['real']['mean'] - c['upper']['mean']:+.1f} | {c['picks']} of {c['n']} |")
    L += ["", "*At the floor* = no more than 2 points above the constant-prediction floor; *measurably helps* = at least 5 "
          "points above the better unrelated reference and ahead of it in at least 9 of 12 paired corpora (entry 8).", "",
          "## T4. Synthetic references, all five languages", ""]
    for kind in ("related", "candidates"):
        L += [f"`{kind}` tier", "", "| Hidden | Reference | " + " | ".join(SCRIPTS) + " |", "|---|---|" + "---|" * 4]
        for lang in LANGS:
            for t, lab in (("upper", "v1 sister (synthetic, optimistic)"), ("harsh", "`harsh` (synthetic, optimistic)")):
                L.append(f"| {A.NAME[lang]} | {lab} | " + " | ".join(
                    f"{iv(S[(lang, st, kind, t)])}, n={S[(lang, st, kind, t)]['n']}" for st in SCRIPTS) + " |")
        L.append("")
    L += ["## T5. Task C", "", "| Relative | Script | References chosen by revised EM (`candidates_real`) | "
          "Family correct: revised EM | original EM | frequency rank |", "|---|---|---|---|---|---|"]
    for (rel, st), c in C.items():
        L.append(f"| {LABEL[rel]} | {st} | " + ", ".join(f"{a} {b}" for a, b in sorted(c["refs"].items(), key=lambda kv: -kv[1]))
                 + " | " + " | ".join(f"{f(c['family'][m])}%" for m in METHODS) + " |")
    L += ["", "| Hidden | Script | Family correct, v1 sister `candidates` (revised EM) | Family correct, `candidates_harsh` |",
          "|---|---|---|---|"]
    L += [f"| {A.NAME[lang]} | {st} | {f(S[(lang, st, 'family_v1')])}% | {f(S[(lang, st, 'family_harsh')])}% |"
          for lang in LANGS for st in SCRIPTS]
    L += ["", "## T6. C3 solver budget (seeds 6-8)", "", "| Relative | Script | n | 3 restarts | 10 restarts | Difference | "
          "First-order? |", "|---|---|---|---|---|---|---|"]
    sg = lambda v: "-" if math.isnan(v) else f"{v:+.1f}"  # noqa: E731
    L += [f"| {LABEL[rel]} | {st} | {c['c3']['n']} | {f(c['c3']['r3'])} | {f(c['c3']['r10'])} | {sg(c['c3']['delta'])} | "
          f"{yn(c['c3']['first_order'])} |" for (rel, st), c in C.items()]
    dv = res.get("dev_cells") or {}
    L += ["", "## T7. Agreement with the development seeds (0-5)", "",
          "| Relative | Script | At the floor? 6-11 / dev | Measurably helps? 6-11 / dev | Below `harsh`? 6-11 / dev | "
          "Below v1 sister? 6-11 / dev | Agree (all four) |", "|---|---|---|---|---|---|---|"]
    for (rel, st), c in C.items():
        d = dv.get(f"{rel}|{st}")
        now = (c["at_floor"], c["helps"], c["real"]["mean"] < c["harsh"]["mean"], c["real"]["mean"] < c["upper"]["mean"])
        was = None if not d else (d["at_floor"], d["helps"], d["real"] < d["harsh"], d["real"] < d["upper"])
        L.append(f"| {LABEL[rel]} | {st} | " + " | ".join(f"{yn(a)} / {yn(None if was is None else b)}"
                                                         for a, b in zip(now, was or (None,) * 4))
                 + f" | {yn(None if was is None else now == was)} |")
    L += ["", "Disagreements are reported, not resolved. Cross-script comparisons, including with Ugaritic-Hebrew, are "
          "indicative only. Nothing here enters the paper before the project owner has seen it."]
    path.write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, help="pipeline-check directory (scripts/v2/final_v2.py --dev); not a result")
    a = ap.parse_args()
    global PIPELINE
    PIPELINE = bool(a.dir)
    rs = _read("v2_final", a.dir)
    if rs is None:
        raise SystemExit("no final-run records")
    recs, failed = latest(rs)
    if a.dir:
        expected = set(recs) | {corpus_key(r) for r in failed}
    else:
        expected = {(lang, st, s, smp) for lang in LANGS for st in SCRIPTS for s in SEEDS for smp in SAMPLERS}
        assert {k[2] for k in recs} <= set(SEEDS), "records outside seeds 6-11"
    c4 = None if a.dir else _read("v2_final_c4", None)
    det = determinism(recs, latest(c4)[0] if c4 else None)
    C = pair_cells(recs)
    dev = dev_answers()
    res = {"pipeline_check": bool(a.dir), "cells": C, "synthetic": synthetic(recs), "determinism": det,
           "process": {"expected": len(expected), "missing": sorted(expected - set(recs)),
                       "errors": sum("error" in r for r in rs)},
           "dev_cells": {f"{k[0]}|{k[1]}": v for k, v in dev.items() if isinstance(k, tuple)}}
    res["readings"] = evaluate_readings(C, det, dev)
    out = a.dir or OUT
    write(res, out / "results.md", bool(a.dir))
    js = {**res, "cells": {f"{k[0]}|{k[1]}": v for k, v in C.items()},
          "synthetic": {"|".join(k): v for k, v in res["synthetic"].items()}}
    (out / "results.json").write_text(json.dumps(js, indent=1, default=float))


if __name__ == "__main__":
    main()
