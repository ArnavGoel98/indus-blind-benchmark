# Reproducibility kit for the v2 final run

Written 2026-11-17, after the final run (entry 12) and entry 13 were reported. Nothing here changes a
reported number. The kit lives under `reports/` because the freeze guard in `scripts/v2/final_v2.py`
only allows changes there and in `docs/`.

## One command

```
bash reports/v2/repro/reproduce.sh [WORKERS]
```

This command:

1. Builds a Python 3.11 environment with the versions in `requirements-lock.txt`.
2. Fetches and prepares the v1 sources. If Project Gutenberg is down, it uses its official mirror
   `gutenberg.pglaf.org`. The texts are then checked against `v1_sources_manifest.json`.
3. Fetches the Wikisource relatives as they stood at the 2026-10-15 cutoff, checked against
   `relatives_manifest.json`.
4. Recalibrates the generator and checks the calibration against the committed calibration reports.
5. Runs the tests.
6. Reruns the final run and C4 on `frozen-v2.1`. This takes about 10-11 hours on 4 cores.
7. Compares the rerun with the archived records in `reports/v2/final/records/`.

## Files

| File | What it does |
|---|---|
| `reproduce.sh` | The steps above |
| `requirements-lock.txt` | Exact library versions of the rerun environment (Python 3.11.18) |
| `v1_sources_manifest.json`, `check_sources.py` | SHA-256 of the 634 v1 source and segment files, and its check |
| `fetch_relatives_pinned.py`, `relatives_manifest.json` | Revision id and SHA-256 of the 239 Wikisource pages at the cutoff |
| `recalibrate.py` | Recreates `runs/calibration*/full/` and checks 400 seed-0 statistics against the reports |
| `compare_rerun.py` | Compares the rerun with the archive and re-evaluates H1-H8 independently of `final_summary.py` |
| `rerun_comparison.md` | Its output for the 2026-11-17 rerun, once the rerun finishes |

## Gaps found, and what was done about them

**1. Old Tamil text changed upstream; the 2026-10-03 text is lost.**
- The Old Tamil source is 17 Project Madurai files, fetched on 2026-10-03. The repository kept no
  checksum of them.
- Today's files give different corpora:
  - 0 of 48 final-run Old Tamil corpora have the archived token count.
  - 55 of the 80 Old Tamil calibration statistics differ from the calibration report.
- Every other language reproduces exactly:
  - Latin, Finnish, Sumerian and Sanskrit corpora: 48 of 48 each.
  - Their calibration statistics: 320 of 320.
- The Internet Archive lists snapshots of 14 of the 17 files from before 2026-10-03. They could not be
  downloaded from the session that built this kit, and they are not guaranteed to equal the text fetched
  then.
- Today's Old Tamil files are now pinned, so any further change will be detected.

What this means for the rerun:
- Values that depend on the Old Tamil text are a replication on new corpora, not an exact
  reproduction. These are:
  - every Old Tamil corpus, so every Malayalam and Kannada score;
  - the `candidates_*` tiers of every language, because the candidate list includes an Old Tamil
    reference;
  - C1 runs with Old Tamil as the unrelated reference.
- `compare_rerun.py` fixes these classes in code, before reading the rerun.

**2. The Wikisource texts were not pinned.**
- The original fetchers took each page's current revision, and their manifests stayed in the
  git-ignored `data/`.
- `fetch_relatives_pinned.py` now asks the MediaWiki API for the revision current at the end of
  2026-10-15. That is the fetch date in `config/sources.yaml`, and the date the owner accepted the
  texts.
- Results for the 239 pages:
  - Malayalam: 126 pages.
  - Kannada: 93 pages. The other 61 sandhi pages are red links, as recorded in
    `reports/v2/real_relatives/yardsticks.md`.
  - Kalevipoeg: 20 cantos.
  - None was edited after the cutoff.
- The rebuilt relatives match the recorded sizes exactly:

| Pair | Lines | Words | Units |
|---|---|---|---|
| Latin-Italian | 14,233 | 101,601 | 391,950 |
| Old Tamil-Malayalam | 15,901 | 42,648 | 479,851 |
| Old Tamil-Kannada | 29,880 | 105,385 | 857,617 |
| Finnish-Estonian | 18,664 | 58,926 | 369,658 |

**3. Library versions were not recorded.**
- `pyproject.toml` gives only lower bounds, and the versions of the original environment were not
  recorded.
- `requirements-lock.txt` records the rerun environment. If the exact class reproduces bit for bit,
  these versions are shown to give the archived numbers.

**4. Calibration files are git-ignored.**
- Calibration is seeded, so `recalibrate.py` recreates the files, then checks them before any corpus
  is drawn.
- The non-Tamil statistics reproduce exactly (gap 1).

## Recommendations for v3

Pin every source by checksum at fetch time, and commit the manifest. Record the library versions with
every run. Commit the calibration files, or their checksums, with the freeze.
