"""Recreate the generator calibrations the v2 runs load (runs/calibration*/full/, git-ignored), then check
them against the committed calibration reports (seed-0 statistics, regime `full`).

Calibration is seeded (seed 0 and a hash of source, script type and regime), so a rerun on the same
code and source texts reproduces it; the check confirms that it did before any corpus is used.
Usage (repository root): python reports/v2/repro/recalibrate.py [--check-only]
"""
import json
import re
import sys
from pathlib import Path

from ibdb.generator.calibrate import calibrate_all, calibration_path

LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
REPORTS = {"v1": "reports/calibration_report.md", "v2": "reports/generator_v2/calibration_report.md"}
COLS = ["n_texts", "mean_length", "median_length", "max_length", "sign_inventory", "coverage80_signs", "top1_share",
        "hapax_fraction", "enders80_signs", "beginners80_signs"]


def reported(gv: str) -> dict:
    """(source, script) -> seed-0 statistics in the `full` regime table of the committed report."""
    text = Path(REPORTS[gv]).read_text()
    block = text.split("## 2.1 Regime `full`", 1)[1].split("\n## ", 1)[0]
    out = {}
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 12 and cells[0] in LANGS:
            out[(cells[0], cells[1])] = [re.sub(r"[^\d.]", "", c) for c in cells[2:12]]
    return out


def main() -> None:
    if "--check-only" not in sys.argv:
        for gv in ("v1", "v2"):
            calibrate_all(LANGS, SCRIPTS, [], ["full"], workers=4, generator_version=gv)
    bad = n = 0
    for gv in ("v1", "v2"):
        want = reported(gv)
        for (src, st), vals in want.items():
            st_ = json.loads(calibration_path("full", src, st, gv).read_text())["stats"]
            for col, v in zip(COLS, vals):
                n += 1
                got = st_[col]
                fmt = f"{got:.3f}" if isinstance(got, float) and not float(got).is_integer() else f"{got:.0f}"
                if col in ("mean_length", "median_length", "top1_share", "hapax_fraction"):
                    fmt = f"{float(got):.{len(v.split('.')[1]) if '.' in v else 0}f}"
                if fmt != v:
                    bad += 1
                    print(f"DIFF {gv} {src} {st} {col}: report {v}, now {fmt}")
    print(f"{n} reported statistics checked; {bad} differ")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
