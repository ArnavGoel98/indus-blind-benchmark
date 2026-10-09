# v2: allograph merging before Task D (sensitivity sweep, sister-v2 profile)

Primary score: frozen original-rule EM, before the cognate step, % of sign tokens. Merger parameters were
fixed on development corpora (seeds 90-91) before this run. Oracle = merge the hidden allograph groups.

Corpora: 1451 (errors: 0). Regenerated corpora matching their stored statistics: 1451/1451. Recomputed no-merge score equal to the stored score (both tiers): 1451/1451.

## Merge accuracy (learned merger vs hidden allograph map)

| Inventory | Precision | Recall | Value-consistent | Signs | Groups after merge | True groups |
|---|---|---|---|---|---|---|
| 400 | 0.74 | 0.17 | 0.75 | 400 | 363 | 182 |
| 500 | 0.78 | 0.11 | 0.78 | 500 | 456 | 203 |
| 600 | 0.78 | 0.09 | 0.79 | 600 | 552 | 216 |
| 700 | 0.79 | 0.08 | 0.79 | 700 | 650 | 245 |
| 800 | 0.80 | 0.05 | 0.80 | 800 | 750 | 265 |

| Script type | Precision | Recall |
|---|---|---|
| logographic | 0.75 | 0.12 |
| syllabic | 0.84 | 0.08 |
| logosyllabic | 0.64 | 0.17 |
| alphabetic | 0.87 | 0.03 |

## Task D, `candidates` tier, by inventory (mean over corpora, all duplicate rates)

| Inventory | n | No merge | Learned merge | Oracle merge |
|---|---|---|---|---|
| 400 | 245 | 4.0 | 4.3 | 5.9 |
| 500 | 300 | 2.9 | 3.0 | 3.6 |
| 600 | 303 | 2.7 | 2.9 | 3.3 |
| 700 | 306 | 2.0 | 2.1 | 2.4 |
| 800 | 297 | 1.6 | 1.7 | 1.6 |
| Plausible box | 603 | 2.7 | 2.7 | 3.3 |

By script type (no merge / learned / oracle):

| Script type | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| logographic | 0.8 / 0.5 / 1.0 | 0.3 / 0.3 / 0.5 | 0.3 / 0.3 / 0.6 | 0.1 / 0.2 / 0.5 | 0.2 / 0.2 / 0.4 |
| syllabic | 1.4 / 2.8 / 4.7 | 1.0 / 1.1 / 2.1 | 1.1 / 0.9 / 1.8 | 1.0 / 0.7 / 1.4 | 1.0 / 0.8 / 0.9 |
| logosyllabic | 0.0 / 0.1 / 0.0 | 0.1 / 0.1 / 0.0 | 0.1 / 0.1 / 0.1 | 0.3 / 0.4 / 0.3 | 0.3 / 0.3 / 0.4 |
| alphabetic | 9.3 / 8.9 / 11.3 | 8.9 / 9.2 / 9.9 | 9.7 / 10.7 / 10.9 | 10.5 / 10.9 / 11.5 | 12.0 / 13.2 / 11.3 |

Learned merge vs none, per corpus: better 401, worse 412, equal 638.

## Task D, `none` tier, by inventory (mean over corpora, all duplicate rates)

| Inventory | n | No merge | Learned merge | Oracle merge |
|---|---|---|---|---|
| 400 | 245 | 3.5 | 3.5 | 4.2 |
| 500 | 300 | 2.8 | 3.1 | 3.2 |
| 600 | 303 | 2.5 | 2.7 | 3.1 |
| 700 | 306 | 2.0 | 1.9 | 2.4 |
| 800 | 297 | 1.4 | 1.4 | 1.7 |
| Plausible box | 603 | 2.6 | 2.6 | 3.0 |

By script type (no merge / learned / oracle):

| Script type | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| logographic | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 | 0.0 / 0.0 / 0.0 |
| syllabic | 0.5 / 0.4 / 0.6 | 0.6 / 0.8 / 0.7 | 0.7 / 0.6 / 0.9 | 0.7 / 0.4 / 0.6 | 0.6 / 0.5 / 0.8 |
| logosyllabic | 0.0 / 0.1 / 0.0 | 0.1 / 0.1 / 0.0 | 0.1 / 0.1 / 0.0 | 0.1 / 0.2 / 0.1 | 0.1 / 0.1 / 0.1 |
| alphabetic | 9.2 / 9.1 / 10.9 | 9.0 / 9.9 / 10.4 | 9.6 / 10.5 / 11.8 | 11.1 / 11.3 / 13.8 | 12.5 / 12.5 / 15.1 |

Learned merge vs none, per corpus: better 361, worse 347, equal 743.

## Matched corpora (same language, script, seed and duplicate rate at both inventories)

| Tier | Inventories | n | No merge | Learned merge | Oracle merge |
|---|---|---|---|---|---|
| candidates | 400 -> 800 | 184 | 3.1 -> 2.4 | 3.4 -> 2.5 | 4.7 -> 2.4 |
| candidates | 400 -> 700 | 203 | 3.6 -> 2.9 | 3.9 -> 3.0 | 5.4 -> 3.5 |
| candidates | 500 -> 700 | 261 | 2.6 -> 2.3 | 2.6 -> 2.4 | 3.2 -> 2.8 |
| none | 400 -> 800 | 184 | 2.4 -> 2.2 | 2.3 -> 2.2 | 2.5 -> 2.7 |
| none | 400 -> 700 | 203 | 3.0 -> 2.9 | 2.9 -> 2.9 | 3.3 -> 3.5 |
| none | 500 -> 700 | 261 | 2.5 -> 2.3 | 2.6 -> 2.3 | 2.7 -> 2.8 |
