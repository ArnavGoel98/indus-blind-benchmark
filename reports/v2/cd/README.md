# v2 Tasks C and D: what each file is

Every file here is labelled by its epistemic status: **pre-registered** (procedure and reading fixed in
`docs/v2_preregistration.md` before the run), **exploratory** (an inspection with no fixed reading) or
**post hoc** (decided after seeing results). Methods are frozen at `frozen-v2` (commit `4ce3e90`).

| File | Status | What it is | Produced by |
|---|---|---|---|
| `results.md`, `results.json` | pre-registered (entries 1, 2, 4-6) | Primary tables, seeds 0-2. The row label "`harsh` (lower bound)" is entry 4's; it is not a lower bound for real relatives (`docs/v2_negative_results.md`, item 3). | `scripts/v2/cd_v2_summary.py` (frozen) |
| `per_corpus.md` | post hoc, descriptive | Seeds 0-2, one value per corpus, real relatives against `harsh`. | code inside the file |
| `replication.md`, `replication.json` | pre-registered (entry 7) | Seeds 3-5 tables and the four replication checks R1-R4. | `analysis/replication.py`, `analysis/v2_analysis.py` |
| `pooled.md` | pre-registered as reported (entry 7), descriptive | Means over seeds 0-5 with bootstrap intervals over corpora. | `analysis/v2_analysis.py` |
| `controls.md`, `controls.json` | pre-registered in procedure (entry 8), post hoc in motivation | Unrelated reference (C1), constant floor (C2), solver budget (C3), determinism (C4). | `analysis/controls.py`, `analysis/v2_analysis.py` |
| `frequency_check.md` | exploratory, post hoc | Unit-frequency agreement against Task D; refutes one explanation offered in negative result 3. | `analysis/freq_check.py` |
| `page_data.json` | derived | Per-corpus data for the review page. | `analysis/v2_analysis.py` |
| `records/` | raw | Gzipped run records (scores and chosen references only; no answer keys) with SHA-256. | copies of `runs/results/v2_cd*`, `v2_controls` |

The drivers and analysis code in `analysis/` are outside the frozen-code check (which covers everything
except `src/ibdb/data`, `reports/` and `docs/`). They call only frozen functions, and each was committed
before its run. `analysis/check_numbers.py` checks that every decimal in the v2 draft section appears in
one of these reports.
