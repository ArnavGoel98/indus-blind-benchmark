# Generator v1 vs v2 (text-beginner fix attempt)

v2 changes only how text windows are sampled (two stages: opening word type, then the rest). Method code is identical (frozen-v1). Same seeds (0, 1, 2) and the same experiments where both ran: size 500 / 2,906 / 50,000 and lengths 3-20 at 2,906 texts.

## Calibration at the Indus point (all seeds; share of corpora meeting each target)

| Target | v1 languages | v2 languages | v1 all corpora | v2 all corpora |
|---|---|---|---|---|
| `n_texts` | 100% | 100% | 100% | 100% |
| `mean_length` | 100% | 100% | 100% | 100% |
| `median_length` | 100% | 100% | 100% | 100% |
| `max_length` | 100% | 100% | 100% | 100% |
| `sign_inventory` | 83% | 70% | 88% | 78% |
| `coverage80_signs` | 57% | 67% | 54% | 63% |
| `top1_share` | 75% | 43% | 64% | 43% |
| `hapax_fraction` | 83% | 75% | 77% | 72% |
| `enders80_signs` | 63% | 55% | 57% | 53% |
| `beginners80_signs` | 37% | 35% | 30% | 30% |
| **every target** | 12% | 8% | 9% | 9% |

Median beginners-80% count, languages (target 82 ± 20): v1 56, v2 55.

## Results at the Indus point

| Task | Method | v1 | v2 |
|---|---|---|---|
| A bal. acc. | Rao 2009 entropy | 0.77 [0.57, 0.90] | 0.80 [0.59, 0.95] |
| A bal. acc. | Yadav 2010 n-gram | 0.66 [0.44, 0.86] | 0.30 [0.19, 0.43] |
| A bal. acc. | Positional | 0.65 [0.45, 0.89] | 0.48 [0.43, 0.50] |
| A bal. acc. | Lee 2010 tree | 0.65 [0.44, 0.85] | 0.66 [0.45, 0.87] |
| A bal. acc. | Multi-feature LR | 0.55 [0.43, 0.72] | 0.72 [0.48, 0.92] |
| B acc. | Inventory rule | 0.25 [0.15, 0.35] | 0.25 [0.13, 0.37] |
| B acc. | Inventory/freq. LR | 0.43 [0.30, 0.58] | 0.62 [0.38, 0.83] |
| B acc. | Segment length | 0.22 [0.12, 0.32] | 0.32 [0.18, 0.47] |
| D token acc. (candidates) | Frequency-rank baseline | 0.029 [0.01, 0.05] | 0.031 [0.02, 0.05] |
| D token acc. (candidates) | Knight-style EM (revised rule) | 0.146 [0.05, 0.24] | 0.427 [0.19, 0.64] |
| D token acc. (candidates) | Knight-style EM (original rule) | 0.021 [0.01, 0.04] | 0.150 [0.08, 0.22] |
| D token acc. (candidates) | EM cognate-matcher | 0.023 [0.01, 0.04] | 0.025 [0.01, 0.04] |
| D token acc. (none) | Frequency-rank baseline | 0.014 [0.01, 0.02] | 0.016 [0.01, 0.03] |
| D token acc. (none) | Knight-style EM (revised rule) | 0.033 [0.02, 0.05] | 0.048 [0.03, 0.07] |
| D token acc. (none) | Knight-style EM (original rule) | 0.018 [0.01, 0.03] | 0.033 [0.02, 0.05] |
| D token acc. (none) | EM cognate-matcher | 0.012 [0.01, 0.02] | 0.016 [0.01, 0.02] |
| D token acc. (related, upper bound) | Frequency-rank baseline | 0.055 [0.03, 0.09] | 0.054 [0.03, 0.08] |
| D token acc. (related, upper bound) | Knight-style EM (revised rule) | 0.258 [0.13, 0.38] | 0.495 [0.31, 0.66] |
| D token acc. (related, upper bound) | Knight-style EM (original rule) | 0.246 [0.12, 0.36] | 0.483 [0.29, 0.65] |
| D token acc. (related, upper bound) | EM cognate-matcher | 0.067 [0.03, 0.11] | 0.061 [0.04, 0.09] |

## Length vs size, Task D candidates tier, Knight-style EM (revised rule)

| Setting | v1 | v2 |
|---|---|---|
| 500 texts × 4.6 signs | 0.102 [0.03, 0.19] | 0.236 [0.10, 0.38] |
| 2,906 texts × 4.6 signs | 0.146 [0.05, 0.24] | 0.427 [0.19, 0.64] |
| 50,000 texts × 4.6 signs | 0.169 [0.06, 0.29] | 0.446 [0.21, 0.67] |
| 2,906 texts × 3.0 signs | 0.086 [0.02, 0.17] | 0.290 [0.14, 0.43] |
| 2,906 texts × 6.0 signs | 0.193 [0.06, 0.33] | 0.454 [0.21, 0.67] |
| 2,906 texts × 10.0 signs | 0.332 [0.16, 0.49] | 0.511 [0.25, 0.72] |
| 2,906 texts × 20.0 signs | 0.438 [0.20, 0.64] | 0.485 [0.23, 0.71] |

## Without the script-type oracle (Indus point)

| Tier | Method | v1 | v2 |
|---|---|---|---|
| candidates | Frequency-rank baseline | 0.031 [0.01, 0.06] (≥50%: 0.00) | 0.026 [0.01, 0.04] (≥50%: 0.00) |
| candidates | Knight-style EM (revised rule) | 0.119 [0.03, 0.21] (≥50%: 0.07) | 0.390 [0.16, 0.61] (≥50%: 0.42) |
| candidates | Knight-style EM (original rule) | 0.016 [0.00, 0.03] (≥50%: 0.00) | 0.128 [0.06, 0.21] (≥50%: 0.10) |
| candidates | EM cognate-matcher | 0.016 [0.01, 0.03] (≥50%: 0.00) | 0.020 [0.01, 0.03] (≥50%: 0.00) |
| none | Frequency-rank baseline | 0.014 [0.01, 0.02] (≥50%: 0.00) | 0.015 [0.01, 0.02] (≥50%: 0.00) |
| none | Knight-style EM (revised rule) | 0.028 [0.01, 0.04] (≥50%: 0.00) | 0.043 [0.03, 0.06] (≥50%: 0.00) |
| none | Knight-style EM (original rule) | 0.015 [0.00, 0.03] (≥50%: 0.00) | 0.029 [0.01, 0.05] (≥50%: 0.00) |
| none | EM cognate-matcher | 0.009 [0.00, 0.02] (≥50%: 0.00) | 0.012 [0.01, 0.02] (≥50%: 0.00) |
