"""Compare a rerun of the v2 final run with the archived records (reproducibility check, not a new result).

Two classes of value, fixed before the rerun was read (2026-11-17):
- EXACT: every value that does not depend on the Old Tamil source text. Old Tamil's Project Madurai files changed
  upstream after the 2026-10-03 fetch and were never pinned (README.md here), so everything else must
  reproduce bit for bit: all values of Latin, Finnish, Sumerian and Sanskrit corpora except the `candidates_*`
  tiers (their candidate list includes an Old Tamil reference) and C1 runs whose unrelated reference is Old Tamil.
- REPLICATION: Old Tamil corpora, and the Tamil-dependent values above. These are new draws from today's text; the
  nine readings (H1-H8, entry 13 aside) are re-evaluated on the rerun and shown beside the archived ones.
The readings are recomputed here independently of reports/v2/final/analysis/final_summary.py, with the
definitions of docs/v2_final_run_readings.md (helps = at least +5 points over the better unrelated reference and
ahead in at least 9 of the 12 paired corpora).

Usage (repository root): python reports/v2/repro/compare_rerun.py [--rerun runs/results] [--out reports/v2/repro/rerun_comparison.md]
"""
from __future__ import annotations

import argparse
import gzip
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ARCH = ROOT / "reports" / "v2" / "final" / "records"
EM = "knight2006_em"
PAIRS = {"italian": "latin", "malayalam": "tamil", "kannada": "tamil", "estonian": "finnish"}
UN = {"latin": ["tamil", "finnish"], "tamil": ["latin", "finnish"], "finnish": ["latin", "tamil"]}
SC = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
H7_RELS = ("italian", "malayalam", "kannada")          # the readings document, H7 (Estonian not part of it)
CHECK_KEYS = ("tiers", "ceiling", "floor", "unrelated", "budget", "v1_sister", "n_tokens", "family")   # section 5, as frozen
VOLATILE = {"timing", "seconds", "commit", "elapsed", "time", "runtime_s", "wall_seconds"}


def load_arch(name: str) -> list[dict]:
    with gzip.open(ARCH / f"{name}.jsonl.gz", "rt", encoding="utf-8") as fh:
        return [json.loads(x) for x in fh]


def load_new(d: Path, name: str) -> list[dict]:
    return [json.loads(x) for x in (d / name).read_text(encoding="utf-8").splitlines()]


def key(r: dict) -> tuple:
    return r["lang"], r["script_type"], r["seed"], r["sampler"]


def leaves(x, p=""):
    if isinstance(x, dict):
        for a in sorted(x):
            if a not in VOLATILE:
                yield from leaves(x[a], f"{p}/{a}")
    elif isinstance(x, list):
        for i, a in enumerate(x):
            yield from leaves(a, f"{p}/{i}")
    else:
        yield p, x


def tamil_dependent(lang: str, path: str) -> bool:
    return lang == "tamil" or "candidates" in path or "/unrelated/tamil" in path


def compare(a_list: list[dict], b_list: list[dict]) -> dict:
    """Leaf-by-leaf comparison by corpus; counts per class and the first differing exact paths."""
    a, b = {key(r): r for r in a_list}, {key(r): r for r in b_list}
    out = {"corpora_archive": len(a), "corpora_rerun": len(b), "missing": sorted(set(a) - set(b)),
           "exact": [0, 0], "replication": [0, 0], "exact_diffs": []}
    for k in sorted(set(a) & set(b)):
        la, lb = dict(leaves(a[k])), dict(leaves(b[k]))
        for p in sorted(set(la) | set(lb)):
            cls = "replication" if tamil_dependent(k[0], p) else "exact"
            same = la.get(p, "<absent>") == lb.get(p, "<absent>")
            out[cls][0] += 1
            out[cls][1] += not same
            if cls == "exact" and not same and len(out["exact_diffs"]) < 20:
                out["exact_diffs"].append(f"{k} {p}: {la.get(p, '<absent>')!r} -> {lb.get(p, '<absent>')!r}")
    return out


def readings(recs: list[dict], c4: list[dict] | None) -> dict:
    """H1-H8 of docs/v2_final_run_readings.md, recomputed from records."""
    cells = {}
    for rel, lang in PAIRS.items():
        for s in SC:
            rs = sorted((r for r in recs if r["lang"] == lang and r["script_type"] == s), key=lambda r: (r["seed"], r["sampler"]))
            assert len(rs) == 12, (lang, s, len(rs))
            real = [100 * r["tiers"][f"related_real:{rel}"][EM]["strict"] for r in rs]
            un = {u: [100 * r["unrelated"][u][EM][f"real:{rel}"]["strict"] for r in rs] for u in UN[lang]}
            best = max(un, key=lambda u: st.fmean(un[u]))
            v1 = []
            for r in rs:
                x = r["v1_sister"]["related"][EM]
                v1.append(100 * (x["token_acc_before_cognate"] if x.get("token_acc_before_cognate") is not None else x["token_acc"]))
            c = {"real": st.fmean(real), "added": st.fmean(real) - st.fmean(un[best]),
                 "wins": sum(x > y for x, y in zip(real, un[best])), "v1": st.fmean(v1),
                 "harsh": st.fmean(100 * r["tiers"]["related_harsh"][EM]["strict"] for r in rs),
                 "picks": sum(r["tiers"][f"candidates_real:{rel}"][EM]["reference"] == rel for r in rs)}
            c["helps"] = c["added"] >= 5 and c["wins"] >= 9
            cells[rel, s] = c
    top = max(cells, key=lambda k: cells[k]["real"])
    h3 = [k for k in cells if k[1] in ("syllabic", "logosyllabic") and cells[k]["helps"]]
    nl = [k for k in cells if k[1] != "logographic"]
    m, k = cells["malayalam", "alphabetic"]["real"], cells["kannada", "alphabetic"]["real"]
    ia, isy = cells["italian", "alphabetic"], cells["italian", "syllabic"]
    picks = {rel: sum(cells[rel, s]["picks"] for s in SC) for rel in H7_RELS}
    R = {
        "H1": (all(c["real"] < 50 for c in cells.values()), f"highest {cells[top]['real']:.1f} ({top[0].capitalize()}, {top[1]})"),
        "H2a": (cells["estonian", "alphabetic"]["helps"],
                f"{cells['estonian', 'alphabetic']['added']:+.1f}; {cells['estonian', 'alphabetic']['wins']} of 12"),
        "H2b": (cells["kannada", "alphabetic"]["helps"],
                f"{cells['kannada', 'alphabetic']['added']:+.1f}; {cells['kannada', 'alphabetic']['wins']} of 12"),
        "H3": (len(h3) <= 1, f"{len(h3)} of 8" + (": " + ", ".join(f"{r.capitalize()} {s} {cells[r, s]['added']:+.1f}, "
                                                                     f"{cells[r, s]['wins']}/12" for r, s in h3) if h3 else "")),
        "H4": (all(cells[x]["real"] < cells[x]["v1"] for x in nl), f"{sum(cells[x]['real'] < cells[x]['v1'] for x in nl)} of {len(nl)}"),
        "H5": (22 <= m <= 42 and 22 <= k <= 42, f"Malayalam {m:.1f}, Kannada {k:.1f}"),
        "H6": (ia["real"] < ia["harsh"] and isy["real"] < isy["harsh"],
               f"{ia['real']:.1f} vs {ia['harsh']:.1f}; {isy['real']:.1f} vs {isy['harsh']:.1f}"),
        "H7": (all(v < 24 for v in picks.values()), ", ".join(f"{r.capitalize()} {v}" for r, v in picks.items()) + " of 48"),
    }
    if c4 is not None:
        main = {key(r): r for r in recs}
        n = bad = 0
        for r in c4:
            la = dict(leaves({x: main[key(r)].get(x) for x in CHECK_KEYS}))
            lb = dict(leaves({x: r.get(x) for x in CHECK_KEYS}))
            for p in set(la) | set(lb):
                n += 1
                bad += la.get(p) != lb.get(p)
        R["H8"] = (bad == 0, f"{n - bad:,} of {n:,} identical ({len(c4)} corpora)")
    return R


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", type=Path, default=ROOT / "runs" / "results")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "rerun_comparison.md")
    a = ap.parse_args()
    new = a.rerun / "v2_final"
    recs_a, recs_b = load_arch("v2_final"), load_new(new, "records.jsonl")
    errors = [key(r) for r in recs_b if "error" in r]
    recs_b = [r for r in recs_b if "error" not in r]
    c4_a = load_arch("v2_final_c4")
    c4_b = load_new(a.rerun / "v2_final_c4", "records.jsonl") if (a.rerun / "v2_final_c4" / "records.jsonl").exists() else None
    cmp = {"records": compare(recs_a, recs_b),
           "predictions": compare(load_arch("v2_final_predictions"), load_new(new, "predictions.jsonl")),
           "v1_sister": compare(load_arch("v2_final_v1_sister"), load_new(new, "v1_sister.jsonl"))}
    if c4_b is not None:
        cmp["c4_records"] = compare(c4_a, c4_b)
    tok = {}
    for r in recs_b:
        o = next(x for x in recs_a if key(x) == key(r))
        tok.setdefault(r["lang"], [0, 0])
        tok[r["lang"]][0] += 1
        tok[r["lang"]][1] += o["n_tokens"] == r["n_tokens"]
    ra, rb = readings(recs_a, c4_a), readings(recs_b, c4_b)
    yn = lambda b: "met" if b else "**not met**"  # noqa: E731
    L = ["# Rerun of the v2 final run: comparison with the archive", "",
         "Reproducibility check, not a new result: the entry-12 readings stand as reported. Same code (`frozen-v2.1`), same "
         "seeds 6-11. Value classes were fixed before the rerun was read (see the script's docstring and `README.md`).", "",
         "## Failures first", ""]
    ex_bad = sum(c["exact"][1] for c in cmp.values())
    L.append(f"- Rerun errors: {len(errors)}{' ' + str(errors) if errors else ''}.")
    L.append(f"- Exact-class values that differ: **{ex_bad:,}**" + (" (listed below)." if ex_bad else "."))
    changed = [h for h in ra if h in rb and ra[h][0] != rb[h][0]]
    L.append(f"- Readings whose verdict changed on the rerun: {', '.join(changed) if changed else 'none'}.")
    L += ["", "## Exact class (must match bit for bit)", "", "| File | Corpora (archive / rerun) | Values compared | Differ |",
          "|---|---|---|---|"]
    for n, c in cmp.items():
        L.append(f"| {n} | {c['corpora_archive']} / {c['corpora_rerun']} | {c['exact'][0]:,} | {c['exact'][1]:,} |")
    for n, c in cmp.items():
        for d in c["exact_diffs"]:
            L.append(f"- {n}: `{d}`")
    L += ["", "Corpora with the archived token count: " + "; ".join(f"{l} {v[1]} of {v[0]}" for l, v in sorted(tok.items())) + ".",
          "", "## Replication class (Old Tamil text changed upstream)", "",
          "| File | Values compared | Identical | Differ |", "|---|---|---|---|"]
    for n, c in cmp.items():
        L.append(f"| {n} | {c['replication'][0]:,} | {c['replication'][0] - c['replication'][1]:,} | {c['replication'][1]:,} |")
    L += ["", "## The readings, archive and rerun", "", "| Reading | Archive | Rerun |", "|---|---|---|"]
    for h in ra:
        b = rb.get(h, (None, "not run"))
        L.append(f"| {h} | {yn(ra[h][0])}: {ra[h][1]} | {yn(b[0]) if b[0] is not None else ''}{': ' if b[0] is not None else ''}{b[1]} |")
    a.out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
