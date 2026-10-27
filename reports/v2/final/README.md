# v2 final run (seeds 6-11): what each file is

Pre-registration entry 12; hypotheses, thresholds and table layouts in `docs/v2_final_run_readings.md`,
fixed before any seed 6-11 corpus existed and frozen with the code by the tag `frozen-v2.1`.

| File | Status | What it is | Produced by |
|---|---|---|---|
| `results.md`, `results.json` | pre-registered (entry 12) | Readings H1-H8 (not met and process failures first), tables T1-T7. Written after the run. | `analysis/final_summary.py` (committed before the tag) |
| `records/` | raw | Gzipped run records and predictions with SHA-256, added after the run. | copies of `runs/results/v2_final`, `v2_final_c4` |

Driver: `scripts/v2/final_v2.py` (refuses to run unless the working tree equals `frozen-v2.1` outside
`reports/` and `docs/`).
