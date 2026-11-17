#!/usr/bin/env bash
# Reproduce the v2 final run (pre-registration entry 12) from a fresh clone, then compare it with the archive.
# Usage (repository root, on the tag frozen-v2.1 or a later commit that equals it outside reports/ and docs/):
#   bash reports/v2/repro/reproduce.sh [WORKERS]
# Needs Python 3.11, uv, network access, about 2 GB of disk and about 10-11 hours on 4 cores (final run + C4).
# What reproduces exactly and what cannot (Old Tamil) is explained in reports/v2/repro/README.md.
set -euo pipefail
WORKERS="${1:-4}"
K=reports/v2/repro
mkdir -p runs/logs

echo "== 1. environment (versions pinned in $K/requirements-lock.txt)"
[ -x .venv/bin/python ] || uv venv -p python3.11 .venv
uv pip install -q -p .venv -r "$K/requirements-lock.txt"
uv pip install -q -p .venv --no-deps -e .

echo "== 2. v1 source texts and segments"
if ! .venv/bin/ibdb fetch; then
  echo "   ibdb fetch failed; retrying the Project Gutenberg texts from the official mirror gutenberg.pglaf.org"
  .venv/bin/python - <<'EOF'
from ibdb import config
from ibdb.data.fetch import http_get
from ibdb.paths import raw_dir
from ibdb.data import relatives as R
c = config.sources()
for name in ("latin", "finnish"):
    s = c["languages"][name]
    for i in s["ids"]:
        url = s["url_pattern"].format(id=i).replace("https://www.gutenberg.org", "https://gutenberg.pglaf.org")
        http_get(url, raw_dir() / name / f"pg{i}.txt", s["license"], 500)
http_get("https://gutenberg.pglaf.org/cache/epub/1000/pg1000.txt", R.relatives_dir() / "dante_pg1000.txt", "PD-US", 500)
EOF
  .venv/bin/ibdb fetch
fi
.venv/bin/ibdb prepare
.venv/bin/python "$K/check_sources.py"

echo "== 3. Wikisource relatives, as they stood at the 2026-10-15 cutoff"
.venv/bin/python "$K/fetch_relatives_pinned.py" --check-only 2>/dev/null || \
  .venv/bin/python "$K/fetch_relatives_pinned.py" --resume
git diff --quiet -- "$K/relatives_manifest.json" || { echo "relatives differ from the committed pin"; git diff --stat -- "$K/relatives_manifest.json"; exit 1; }
.venv/bin/python "$K/fetch_relatives_pinned.py" --check-only

echo "== 4. generator calibration (git-ignored), checked against the committed calibration reports"
.venv/bin/python "$K/recalibrate.py"

echo "== 5. tests"
.venv/bin/python -m pytest -q

echo "== 6. final run and C4 (refuse to start unless the tree equals frozen-v2.1)"
.venv/bin/python scripts/v2/final_v2.py --workers "$WORKERS" | tee runs/logs/final.log
.venv/bin/python scripts/v2/final_v2.py --c4 --workers "$WORKERS" | tee runs/logs/final_c4.log

echo "== 7. comparison with the archived records"
.venv/bin/python "$K/compare_rerun.py" --out runs/logs/rerun_comparison.md
