"""Summary of the v2 Task C/D run (scripts/v2/cd_v2.py): real relatives beside the synthetic references.

Real relatives (entry 5) are the realistic `related` tier. The synthetic sisters are optimistic upper
references, not bounds (entry 10): the v1 sister, read from the sister_v2_main (sampler A) and
sister_v2_gen2 (sampler B) records at the Indus point and scored with the v1 scorer before the cognate
step (entry 4), and `harsh`. Where entry-10 records exist (runs/results/v2_e10, or their archive), the
real-relative tiers of Finnish and Old Tamil are scored with the entry-10 rule (no source = unknown). Beside them, the Ugaritic Task D result (reports/v2/ugaritic/results.md).
Every cell is a mean over the 6 corpora (seeds 0-2, samplers A and B) of one hidden language and script
type; `n>=50%` counts corpora at or above the v1 threshold (50% of tokens).

Usage: python scripts/v2/cd_v2_summary.py [RECORDS] [OUTDIR]
  default RECORDS runs/results/v2_cd (every records*.jsonl in it, merged), OUTDIR reports/v2/cd
"""
from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from ibdb.paths import ensure, reports_dir, runs_dir

SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
METHODS = ["knight2006_em", "knight2006_em_original", "baseline_frequency_rank"]
LABEL = {"knight2006_em": "EM revised (primary)", "knight2006_em_original": "EM original",
         "baseline_frequency_rank": "frequency rank"}
RELATIONSHIP = {"real:italian": "descendant", "real:malayalam": "descendant", "real:kannada": "sister",
                "real:estonian": "sister"}
NAME = {"estonian": "estonian (weak gold: 10 word pairs, 13 of 27 letters)"}
UPPER_LABEL = "v1 sister (synthetic, optimistic upper reference)"
HARSH_LABEL = "`harsh` (synthetic, optimistic upper reference)"
UGARITIC = "Ugaritic-Hebrew, natural text, related tier: 33.9% (EM original), 32.0% (EM revised)"
THRESHOLD = 0.5


def upper_bound() -> dict:
    """(lang, script, tier) -> method -> list of (before-cognate token acc, family correct)."""
    out: dict = defaultdict(lambda: defaultdict(list))
    for prof in ("sister_v2_main", "sister_v2_gen2"):
        for line in (runs_dir() / "results" / prof / "records.jsonl").read_text().splitlines():
            r = json.loads(line)
            j = r.get("job", {})
            if "error" in r or j.get("sweep") != "size" or j.get("n_texts") != 2906 or j.get("seed") not in (0, 1, 2) \
                    or r["truth"]["kind"] != "language":
                continue
            for tier in ("related", "candidates"):
                for m in METHODS:
                    v = r["CD"][tier][m]
                    out[(j["source"], j["script_type"], tier)][m].append(
                        (v.get("token_acc_before_cognate", v["token_acc"]), v["family_correct"], v.get("reference")))
    return out


def entry10_records() -> list[dict]:
    p = runs_dir() / "results" / "v2_e10" / "records.jsonl"
    a = reports_dir() / "v2" / "cd" / "records" / "v2_e10.jsonl.gz"
    lines = p.read_text().splitlines() if p.exists() else (gzip.decompress(a.read_bytes()).decode().splitlines()
                                                             if a.exists() else [])
    return [json.loads(x) for x in lines]


def load(path: Path) -> tuple[dict, list, int]:
    """(lang, script, tier) -> method -> list of records; entry-10 scores replace the old ones per corpus."""
    out: dict = defaultdict(lambda: defaultdict(list))
    errors = []
    files = sorted(path.glob("records*.jsonl")) if path.is_dir() else [path]
    recs = {}
    for line in (ln for f in files for ln in f.read_text().splitlines()):
        r = json.loads(line)
        if "error" in r:
            errors.append(r)
            continue
        key = (r["lang"], r["script_type"], r["seed"], r["sampler"])
        if key in recs:
            recs[key]["tiers"].update(r["tiers"])
        else:
            recs[key] = r
    n10 = 0
    for e in entry10_records():
        key = (e["lang"], e["script_type"], e["seed"], e["sampler"])
        if key in recs:
            for tier, ms in e["tiers"].items():
                recs[key]["tiers"][tier] = {m: {k: v for k, v in x.items() if k not in ("old", "pred")} for m, x in ms.items()}
            n10 += 1
    for r in recs.values():
        for tier, ms in r["tiers"].items():
            for m, v in ms.items():
                out[(r["lang"], r["script_type"], tier)][m].append(v)
    return out, errors, n10


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else runs_dir() / "results" / "v2_cd"
    outdir = ensure(Path(sys.argv[2]) if len(sys.argv) > 2 else reports_dir() / "v2" / "cd")
    res, errors, n10 = load(path)
    ub = upper_bound()
    langs = sorted({k[0] for k in res}, key=lambda x: ["sanskrit", "tamil", "sumerian", "latin", "finnish"].index(x))
    pc = lambda x: f"{100 * x:.1f}" if x == x else "-"  # noqa: E731

    def rows_for(lang: str, kind: str) -> list[tuple[str, str, str]]:
        """(row label, relationship, tier key or 'upper') for the related or candidates tier."""
        rows = [(UPPER_LABEL, "synthetic", "upper")]
        rows += [(NAME.get(t.split(":", 1)[1], t.split(":", 1)[1]), RELATIONSHIP[t.split("_", 1)[1]], t)
                 for t in sorted({k[2] for k in res if k[0] == lang and k[2].startswith(kind + "_real:")})]
        rows.append((HARSH_LABEL, "synthetic", f"{kind}_harsh"))
        return rows

    def cell(lang, st, tier, kind, m, field="strict"):
        if tier == "upper":
            v = [x[0] for x in ub.get((lang, st, kind), {}).get(m, [])]
        else:
            v = [x[field] for x in res.get((lang, st, tier), {}).get(m, [])]
        return (float(np.mean(v)) if v else float("nan")), sum(x >= THRESHOLD for x in v), len(v)

    summary: dict = {"task_d": {}, "task_c": {}, "errors": len(errors)}
    L = ["# v2 Tasks C and D: real relatives beside the synthetic references", "",
         "Real relatives are the realistic `related` tier; the synthetic sisters (v1 sister, `harsh`) are optimistic "
         "upper references, not bounds (pre-registration entry 10). "
         f"Real-relative tiers of {n10} corpora are scored with the entry-10 rule (a no-source gold row is unknown, not "
         "lost); `reports/v2/cd/entry10.md` has the old values.", "",
         f"Records: `{path}` ({len(errors)} corpora with errors). Methods frozen (`frozen-v2`); scoring entry 2 "
         "(strict primary, lenient secondary, before the cognate step); the v1 sister rows use the v1 scorer before "
         "the cognate step (entry 4). Each cell: mean % of sign tokens over 6 corpora (seeds 0-2, samplers A and B), "
         "then corpora at or above 50%. Beside: " + UGARITIC + ".", ""]
    for kind in ("related", "candidates"):
        for m in METHODS:
            L += [f"## Task D, `{kind}` tier, {LABEL[m]} (strict)", "",
                  "| Hidden | Relative | Relationship | " + " | ".join(SCRIPTS) + " |", "|---|---|---|" + "---|" * len(SCRIPTS)]
            for lang in langs:
                for label, rel, tier in rows_for(lang, kind):
                    cells = []
                    for st in SCRIPTS:
                        mean, n50, n = cell(lang, st, tier, kind, m)
                        cells.append(f"{pc(mean)} ({n50}/{n})")
                        summary["task_d"].setdefault(kind, {}).setdefault(m, {}).setdefault(lang, {}).setdefault(label, {})[st] = \
                            {"mean": mean, "n_at_50": n50, "n": n}
                    L.append(f"| {lang} | {label} | {rel} | " + " | ".join(cells) + " |")
            L.append("")
    L += ["## Task D, secondary columns (EM revised): lenient score and the strict ceiling", "",
          "Ceiling: share of tokens with a strict reflex at all (unrecoverable: no reflex, no cognate for a logogram, "
          "determinatives).", "", "| Hidden | Tier | " + " | ".join(f"{st}: lenient / ceiling" for st in SCRIPTS) + " |",
          "|---|---|" + "---|" * len(SCRIPTS)]
    for lang in langs:
        for tier in sorted({k[2] for k in res if k[0] == lang}):
            cells = []
            for st in SCRIPTS:
                v = res.get((lang, st, tier), {}).get("knight2006_em", [])
                cells.append(f"{pc(np.mean([x['lenient'] for x in v]))} / {pc(np.mean([x['recoverable'] for x in v]))}"
                             if v else "-")
            L.append(f"| {lang} | {tier} | " + " | ".join(cells) + " |")
    L += ["", "## Task C (`candidates` tiers): right family, % of corpora (all script types pooled), and the reference chosen", "",
          "| Hidden | Tier | " + " | ".join(LABEL[m] for m in METHODS) + " | References chosen by EM revised |", "|---|---|" + "---|" * (len(METHODS) + 1)]
    for lang in langs:
        tiers = ["upper"] + sorted({k[2] for k in res if k[0] == lang and k[2].startswith("candidates_")})
        for tier in tiers:
            cells = []
            for m in METHODS:
                if tier == "upper":
                    v = [x[1] for st in SCRIPTS for x in ub.get((lang, st, "candidates"), {}).get(m, [])]
                else:
                    v = [x["family_correct"] for st in SCRIPTS for x in res.get((lang, st, tier), {}).get(m, [])]
                cells.append(f"{pc(np.mean(v)) if v else '-'} ({len(v)})")
                summary["task_c"].setdefault(lang, {}).setdefault(tier, {})[m] = float(np.mean(v)) if v else None
            if tier == "upper":
                refs = Counter(x[2] for st in SCRIPTS for x in ub.get((lang, st, "candidates"), {}).get("knight2006_em", []))
            else:
                refs = Counter(x["reference"] for st in SCRIPTS for x in res.get((lang, st, tier), {}).get("knight2006_em", []))
            name = UPPER_LABEL if tier == "upper" else tier
            L.append(f"| {lang} | {name} | " + " | ".join(cells) + " | " + ", ".join(f"{k} {n}" for k, n in refs.most_common()) + " |")
    L.append("")
    (outdir / "results.json").write_text(json.dumps(summary, indent=1, default=float))
    (outdir / "results.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
