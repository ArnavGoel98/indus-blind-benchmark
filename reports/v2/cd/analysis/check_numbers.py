"""Provenance check for the v2 draft section: every decimal number in the draft must appear in a source report.

Sources are the generated reports (reports/v2/cd/*.md, reports/v2/real_relatives/*.md, reports/v2/ugaritic/results.md)
and the yardstick and sister reports they quote. Numbers in headings, section labels (v2.4), dates and code paths
are skipped. Unmatched numbers are printed for a human to resolve; exit code 1 if any remain.
Usage (repository root): python reports/v2/cd/analysis/check_numbers.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAFT = ROOT / "reports" / "drafts" / "v2_real_relatives_section_DRAFT.md"
SOURCES = [*sorted((ROOT / "reports" / "v2" / "cd").glob("*.md")),
           *sorted((ROOT / "reports" / "v2" / "real_relatives").glob("*.md")),
           ROOT / "reports" / "v2" / "ugaritic" / "results.md",
           ROOT / "reports" / "v2" / "sister" / "anchor_corrected.md"]


def main() -> int:
    blob = "\n".join(p.read_text(encoding="utf-8") for p in SOURCES if p.exists())
    have = set(re.findall(r"(?<![\d.])\d+\.\d+(?![\d.])", blob))
    missing = []
    for i, line in enumerate(DRAFT.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("#"):
            continue
        clean = re.sub(r"`[^`]*`|v2\.\d+|\d{4}-\d{2}-\d{2}|entry \d+(\.\d+)?|pp?\. [\d\-, ]+|§+[\d\-, ]+", " ", line)
        for n in re.findall(r"(?<![\d.\w])\d+\.\d+(?![\d.])", clean):
            if n not in have:
                missing.append((i, n, line.strip()[:100]))
    for i, n, ctx in missing:
        print(f"line {i}: {n} not found in any source report | {ctx}")
    print(f"{len(missing)} unmatched number(s)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
