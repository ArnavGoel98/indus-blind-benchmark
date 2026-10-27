"""Pre-registration entry 11: does the syllable-cutter fix work? Old (entry-10 records) against new (entry-11 rerun).

Checks D.1-D.3 of entry 11 (references that may and may not change; words still join; 0 errors) and reports,
for the 24 rerun corpora (seeds 0-2), Task D strict and lenient, raw and reachable ceilings and Task C picks,
per corpus and per cell. Scores are not a criterion.
Usage (repository root): python reports/v2/cd/analysis/entry11_summary.py -> reports/v2/cd/entry11.{md,json}
"""
import dataclasses
import gzip
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ["IBDB_SISTER_VERSION"] = "v2"
import cd_v2  # noqa: E402
import v2_analysis as A  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402

EM, EMO, FR = "knight2006_em", "knight2006_em_original", "baseline_frequency_rank"
REAL = {"finnish": ["estonian"], "tamil": ["malayalam", "kannada"]}
LABEL = {"estonian": "Estonian (weak gold: 10 word pairs, 13 of 27 letters)", "malayalam": "Malayalam", "kannada": "Kannada"}
K = lambda r: (r["lang"], r["script_type"], r["seed"], r["sampler"])  # noqa: E731


def lines(name: str) -> list[str]:
    p = A.RUNS / name / "records.jsonl"
    if p.exists():
        return p.read_text().splitlines()
    return gzip.decompress((A.ARCHIVE / f"{name}.jsonl.gz").read_bytes()).decode().splitlines()


def reference_checks() -> dict:
    """D.1-D.2 over every real relative and harsh (seed 0), whole texts."""
    out = {"changed": [], "unchanged": 0, "join_ok": True, "changed_words_without_added_vowel": 0, "changed_words": 0}
    for lang in ("latin", "tamil", "finnish", "sanskrit", "sumerian"):
        rels = {f"real:{r}": RC.real_relative(lang, r) for r in cd_v2.REAL.get(lang, [])}
        rels["harsh"] = RC.harsh_relative(lang, 0, cd_v2.HARSH[lang]["knobs"])
        for n, rel in rels.items():
            old = dataclasses.replace(rel, vowels=frozenset())
            for st in cd_v2.SCRIPTS:
                if RC.reference(rel, st, lang, 250).texts == RC.reference(old, st, lang, 250).texts:
                    out["unchanged"] += 1
                else:
                    out["changed"].append(f"{lang} {n} {st}")
            added = set(rel.vowels - RC._vowels(lang))
            if n.startswith("real:") and added:
                v_new, v_old = RC._vowels(lang) | rel.vowels, RC._vowels(lang)
                for c in rel.clauses:
                    for w in c:
                        new = RC._groups(w, v_new)
                        out["join_ok"] &= "".join("".join(g) for g in new) == "".join(w)
                        if new != RC._groups(w, v_old):
                            out["changed_words"] += 1
                            out["changed_words_without_added_vowel"] += not (set(w) & added)
    return out


def main() -> None:
    new_all = [json.loads(x) for x in lines("v2_e11")]
    errors = [r for r in new_all if "error" in r]
    new = {K(r): r for r in new_all if "error" not in r}
    old = {K(r): r for r in (json.loads(x) for x in lines("v2_e10")) if "error" not in r and K(r) in new}
    assert len(new) == 24 and len(old) == 24, (len(new), len(old))
    ref = reference_checks()
    rows, cells = [], {}
    for k in sorted(new, key=lambda k: (k[0], k[1], k[2], k[3])):
        for rel in REAL[k[0]]:
            TR, TC, g = f"related_real:{rel}", f"candidates_real:{rel}", f"real:{rel}"
            o, n = old[k]["tiers"], new[k]["tiers"]
            row = {"lang": k[0], "rel": rel, "script": k[1], "seed": k[2], "sampler": k[3],
                   **{f"{m}_old": 100 * o[TR][m]["strict"] for m in (EM, EMO, FR)},
                   **{f"{m}_new": 100 * n[TR][m]["strict"] for m in (EM, EMO, FR)},
                   "lenient_old": 100 * o[TR][EM]["lenient"], "lenient_new": 100 * n[TR][EM]["lenient"],
                   "raw_old": 100 * o[TR][EM]["recoverable"], "raw_new": 100 * new[k]["ceiling"][g]["raw"],
                   "reach_old": 100 * new[k]["ceiling"][g]["reachable_old_cut"], "reach_new": 100 * new[k]["ceiling"][g]["reachable"],
                   "pick_old": o[TC][EM]["reference"], "pick_new": n[TC][EM]["reference"]}
            rows.append(row)
            cells.setdefault(f"{rel}|{k[1]}", []).append(row)
    agg = {c: {f: float(np.mean([r[f] for r in rs])) for f in rs[0] if f.endswith(("_old", "_new")) and not f.startswith("pick")}
           | {"picks_old": sum(r["pick_old"] == r["rel"] for r in rs), "picks_new": sum(r["pick_new"] == r["rel"] for r in rs),
              "n": len(rs)} for c, rs in cells.items()}
    raw_same = all(abs(r["raw_old"] - r["raw_new"]) < 1e-9 for r in rows)
    res = {"errors": len(errors), "reference_checks": ref, "raw_ceiling_unchanged": raw_same, "cells": agg, "rows": rows}
    (A.CD / "entry11.json").write_text(json.dumps(res, indent=1, default=float, ensure_ascii=False))
    write_md(res)


def write_md(res: dict) -> None:
    f = lambda v: f"{v:.1f}"  # noqa: E731
    ref = res["reference_checks"]
    ok1 = sorted(ref["changed"]) == sorted(f"{lg} real:{r} {st}" for lg, rs in REAL.items() for r in rs
                                          for st in ("syllabic", "logosyllabic"))
    ok2 = ref["join_ok"] and ref["changed_words_without_added_vowel"] == 0
    ok3 = res["errors"] == 0
    L = ["# Entry 11: the syllable-cutter fix, confirmed on development seeds 0-2", "",
         "Pre-registration entry 11 (declared before any code or rerun). Real relatives are now cut into syllables with the "
         "hidden language's vowels and their own vowel letters (adds õ and ü for Estonian, vocalic ṛ for Malayalam and "
         "Kannada). The rerun covers only the cells whose solver input changes: Finnish and Old Tamil, syllabic and "
         "logo-syllabic, seeds 0-2, samplers A and B (24 corpora); entry-10 scorer; entry-6 methods and budget. "
         "*Old* = the entry-10 records (frozen-v2 cutter); *new* = this rerun. Development seeds only: these values do not "
         "replace the development tables, and the cutter's effect is read in the final run (entry 12).", "",
         "## Does the fix work? (criteria fixed in entry 11, D)", "",
         "| Criterion | Result | Met? |", "|---|---|---|",
         f"| D.1 Only the references that may change do: Estonian, Malayalam, Kannada; syllabic and logo-syllabic "
         f"(Italian, every alphabetic and logographic reference and every `harsh` reference unchanged; tests in "
         f"`tests/test_entry11.py`) | {len(ref['changed'])} of {len(ref['changed']) + ref['unchanged']} references changed: "
         f"{'; '.join(sorted(ref['changed']))} | {'yes' if ok1 else 'NO'} |",
         f"| D.2 Units of every word still join to the word; every word cut differently contains an added vowel letter | "
         f"{ref['changed_words']:,} words cut differently, {ref['changed_words_without_added_vowel']} without an added vowel; "
         f"joins {'all correct' if ref['join_ok'] else 'NOT all correct'} | {'yes' if ok2 else 'NO'} |",
         f"| D.3 Rerun completes with 0 errors | {res['errors']} errors in 24 corpora | {'yes' if ok3 else 'NO'} |", "",
         f"The raw ceiling depends on the gold only and is {'unchanged in every corpus' if res['raw_ceiling_unchanged'] else 'CHANGED (unexpected)'}.", "",
         "## Old and new, per cell (seeds 0-2, 6 corpora each)", "",
         "| Relative | Script | Revised EM old → new | Original EM old → new | Frequency rank old → new | Lenient old → new | "
         "Reachable ceiling old → new | Raw ceiling | Picks the relative (of 6) old → new |",
         "|---|---|---|---|---|---|---|---|---|"]
    for c, a in res["cells"].items():
        rel, st = c.split("|")
        L.append(f"| {LABEL[rel]} | {st} | {f(a[EM + '_old'])} → {f(a[EM + '_new'])} | {f(a[EMO + '_old'])} → {f(a[EMO + '_new'])} | "
                 f"{f(a[FR + '_old'])} → {f(a[FR + '_new'])} | {f(a['lenient_old'])} → {f(a['lenient_new'])} | "
                 f"{f(a['reach_old'])} → {f(a['reach_new'])} | {f(a['raw_new'])} | {a['picks_old']} → {a['picks_new']} |")
    L += ["", "## Per corpus (revised EM, strict)", "",
          "| Relative | Script | Seed | Sampler | Old | New | Difference | Reachable old → new | Reference chosen in `candidates_real`, old → new |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in res["rows"]:
        L.append(f"| {LABEL[r['rel']]} | {r['script']} | {r['seed']} | {r['sampler']} | {f(r[EM + '_old'])} | {f(r[EM + '_new'])} | "
                 f"{r[EM + '_new'] - r[EM + '_old']:+.1f} | {f(r['reach_old'])} → {f(r['reach_new'])} | {r['pick_old']} → {r['pick_new']} |")
    (A.CD / "entry11.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:30]))


if __name__ == "__main__":
    main()
