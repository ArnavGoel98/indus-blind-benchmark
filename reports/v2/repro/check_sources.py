"""Check the v1 source texts and segments on disk against the pin in v1_sources_manifest.json.

The pin was taken on 2026-11-17 from the files that reproduce the archived Latin, Finnish, Sumerian and Sanskrit
corpora exactly (48 of 48 each). Old Tamil is pinned too, but its pin is today's Project Madurai text, not the
2026-10-03 text the final run used (README.md). Exit status 1 if any non-Tamil file is missing or differs.
Usage (repository root): python reports/v2/repro/check_sources.py
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PIN = json.loads((Path(__file__).resolve().parent / "v1_sources_manifest.json").read_text(encoding="utf-8"))


def main() -> None:
    bad, tamil_bad = [], []
    for rel, m in PIN["files"].items():
        p = ROOT / "data" / ("" if rel.startswith("segments/") else "raw") / rel
        ok = p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == m["sha256"]
        if not ok:
            (tamil_bad if rel.startswith(("tamil/", "segments/tamil")) else bad).append(rel)
    n = len(PIN["files"])
    print(f"{n} files pinned; {len(bad)} non-Tamil differ or are missing; {len(tamil_bad)} Old Tamil differ or are missing")
    for r in bad[:10]:
        print("  differs:", r)
    if tamil_bad:
        print("  Old Tamil differs from the 2026-11-17 pin (Project Madurai changed again?): Tamil-dependent values will not "
              "match even the 2026-11-17 rerun")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
