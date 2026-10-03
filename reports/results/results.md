# Results

Profile `full`: 1554 runs, 0 failed (listed at the end if any). Seeds: [0, 1, 2]. Indus point: 2,906 texts, mean 4.6 signs (Mahadevan 1977, verified).

**Methods were frozen before this run** at git tag `frozen-v1` (commit e625f568d7). No method code changed afterwards.

**Intervals.** Pooled rates and means carry 95% *cluster-bootstrap* intervals: whole source languages or control families are resampled, then corpora within them. Corpora from one source are not independent, so these intervals are wider than Wilson intervals (Wilson bounds are kept in `aggregate.json`). Per-family rates use Wilson intervals. Task A and B decision rules are learned leave-one-source-out.

**How to read Task D.** Solvers are given the true script type (an oracle; Section 6 removes it). The `related` tier gives them a close synthetic relative, which is **not** the Indus situation: treat it as an upper bound. The Indus-relevant tiers are `candidates` and `none`. Default sister distance: sound change 0.3, lexical replacement 0.2. Section 5 varies it.

## 1. Leading result: the `holdout` regime

Under `holdout` only size, length and inventory are calibrated. The frequency and positional statistics that methods 1-3 measure are left free, so methods cannot be rewarded for statistics we injected. `full` tunes them too. `wrong_prior` calibrates to deliberately wrong targets. A conclusion that holds only under `full` is suspect.

| Task | Method | `holdout` | `full` | `wrong_prior` |
|---|---|---|---|---|
| A | Rao 2009 entropy | 0.57 [0.32, 0.81] | 0.77 [0.57, 0.90] | 0.30 [0.14, 0.47] |
| A | Yadav 2010 n-gram | 0.68 [0.45, 0.90] | 0.66 [0.44, 0.86] | 0.39 [0.26, 0.50] |
| A | Positional | 0.57 [0.37, 0.78] | 0.65 [0.45, 0.89] | 0.35 [0.27, 0.42] |
| A | Lee 2010 tree | 0.66 [0.42, 0.89] | 0.65 [0.44, 0.85] | 0.66 [0.44, 0.87] |
| A | Multi-feature LR | 0.59 [0.38, 0.83] | 0.55 [0.43, 0.72] | 0.80 [0.60, 0.99] |
| B | Inventory rule | 0.25 [0.15, 0.37] | 0.25 [0.15, 0.35] | 0.15 [0.03, 0.30] |
| B | Inventory/freq. LR | 0.38 [0.23, 0.53] | 0.43 [0.30, 0.58] | 0.72 [0.55, 0.88] |
| B | Segment length | 0.23 [0.08, 0.40] | 0.22 [0.12, 0.32] | 0.30 [0.17, 0.47] |
| D (related, upper bound) | Frequency-rank baseline | 0.038 [0.02, 0.06] | 0.055 [0.03, 0.09] | 0.067 [0.03, 0.11] |
| D (related, upper bound) | Knight-style EM (revised rule) | 0.282 [0.15, 0.43] | 0.258 [0.13, 0.38] | 0.378 [0.21, 0.53] |
| D (related, upper bound) | Knight-style EM (original rule) | 0.264 [0.14, 0.41] | 0.246 [0.12, 0.36] | 0.376 [0.22, 0.52] |
| D (related, upper bound) | EM cognate-matcher | 0.055 [0.03, 0.08] | 0.067 [0.03, 0.11] | 0.092 [0.05, 0.13] |

Kendall's tau between Task A method rankings under `full` and each other regime:

- `holdout`: tau = 0.00
- `wrong_prior`: tau = -0.80

## 2. Indus point, regime `full` (81 corpora)

### Task A: language vs non-language. **Status: UNRESOLVED**

We label language detection unresolved. Balanced accuracy averages over control families we built ourselves, and a method can score well on average while misclassifying a whole family. The false-positive rates per family below are the result to cite. The adversarial control is tuned to imitate language entropy (Sproat 2014).

| Method | Balanced acc. | Recall on languages | Specificity on controls |
|---|---|---|---|
| Rao 2009 entropy | 0.77 [0.57, 0.90] | 0.70 [0.55, 0.83] | 0.83 [0.50, 1.00] |
| Yadav 2010 n-gram | 0.66 [0.44, 0.86] | 0.82 [0.68, 0.93] | 0.50 [0.17, 0.83] |
| Positional | 0.65 [0.45, 0.89] | 0.80 [0.67, 0.93] | 0.50 [0.17, 0.83] |
| Lee 2010 tree | 0.65 [0.44, 0.85] | 0.85 [0.70, 0.98] | 0.44 [0.11, 0.83] |
| Multi-feature LR | 0.55 [0.43, 0.72] | 0.93 [0.82, 1.00] | 0.17 [0.00, 0.50] |

**False-positive rate per control family** (share classified as linguistic; 0 is correct for every control. Kamon descriptions are Japanese text, so a high rate there is defensible):

| Method | heraldry | admin_tags | emblem_markov | adversarial | rao_type1 | rao_type2 | kamon | languages (recall) |
|---|---|---|---|---|---|---|---|---|
| Rao 2009 entropy | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.70 |
| Yadav 2010 n-gram | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.82 |
| Positional | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.80 |
| Lee 2010 tree | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 0.33 [0.06, 0.79] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.85 |
| Multi-feature LR | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.93 |

### Task B: script type (chance 0.25)

| Method | Accuracy |
|---|---|
| Inventory rule | 0.25 [0.15, 0.35] (n=60, 5 languages) |
| Inventory/freq. LR | 0.43 [0.30, 0.58] (n=60, 5 languages) |
| Segment length | 0.22 [0.12, 0.32] (n=60, 5 languages) |

The inventory rule is defeated by construction: every corpus is calibrated to 400-700 signs.

### Tasks C and D: family and sign values (Indus-relevant tiers first)

Both EM selection rules are reported. The *revised* rule was adopted during development after the *original* rule picked Sumerian for almost every corpus. Readers should compare both.

| Tier | Method | Task C acc. (chance) | Task D mean token acc. | D: corpora ≥50% | D: sign-type acc. |
|---|---|---|---|---|---|
| candidates | Frequency-rank baseline | 0.42 [0.23, 0.62] (0.25) | 0.029 [0.01, 0.05] | 0.00 [0.00, 0.00] | 0.002 |
| candidates | Knight-style EM (revised rule) | 0.45 [0.12, 0.80] (0.25) | 0.146 [0.05, 0.24] | 0.08 [0.00, 0.18] | 0.073 |
| candidates | Knight-style EM (original rule) | 0.20 [0.00, 0.60] (0.25) | 0.021 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.014 |
| candidates | EM cognate-matcher | 0.23 [0.12, 0.37] (0.25) | 0.023 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.002 |
| none | Frequency-rank baseline | 0.18 [0.00, 0.42] (0.30) | 0.014 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.001 |
| none | Knight-style EM (revised rule) | 0.10 [0.00, 0.32] (0.30) | 0.033 [0.02, 0.05] | 0.00 [0.00, 0.00] | 0.017 |
| none | Knight-style EM (original rule) | 0.00 [0.00, 0.00] (0.30) | 0.018 [0.01, 0.03] | 0.00 [0.00, 0.00] | 0.011 |
| none | EM cognate-matcher | 0.03 [0.00, 0.12] (0.30) | 0.012 [0.01, 0.02] | 0.00 [0.00, 0.00] | 0.002 |
| related (upper bound) | Frequency-rank baseline | n/a | 0.055 [0.03, 0.09] | 0.00 [0.00, 0.00] | 0.005 |
| related (upper bound) | Knight-style EM (revised rule) | n/a | 0.258 [0.13, 0.38] | 0.22 [0.07, 0.38] | 0.130 |
| related (upper bound) | Knight-style EM (original rule) | n/a | 0.246 [0.12, 0.36] | 0.23 [0.07, 0.42] | 0.146 |
| related (upper bound) | EM cognate-matcher | n/a | 0.067 [0.03, 0.11] | 0.00 [0.00, 0.00] | 0.006 |

Segmentation boundary F1 (branching entropy vs true word starts): 0.46

## 3. Robustness: only corpora that meet every calibration target

At the Indus point, 7 of 81 corpora meet every hard target (7 of them languages). Rules are re-learned inside this subset.

| Task | Method | All corpora | Passing only |
|---|---|---|---|
| A | Rao 2009 entropy | - | - |
| A | Yadav 2010 n-gram | - | - |
| A | Positional | - | - |
| A | Lee 2010 tree | - | - |
| A | Multi-feature LR | - | - |
| B | Inventory rule | 0.25 [0.15, 0.35] | 0.00 [0.00, 0.00] |
| B | Inventory/freq. LR | 0.43 [0.30, 0.58] | 0.00 [0.00, 0.00] |
| B | Segment length | 0.22 [0.12, 0.32] | 0.33 [0.00, 1.00] |
| D (candidates) | Frequency-rank baseline | 0.029 | 0.010 |
| D (candidates) | Knight-style EM (revised rule) | 0.146 | 0.211 |
| D (candidates) | Knight-style EM (original rule) | 0.021 | 0.029 |
| D (candidates) | EM cognate-matcher | 0.023 | 0.015 |
| D (none) | Frequency-rank baseline | 0.014 | 0.006 |
| D (none) | Knight-style EM (revised rule) | 0.033 | 0.025 |
| D (none) | Knight-style EM (original rule) | 0.018 | 0.013 |
| D (none) | EM cognate-matcher | 0.012 | 0.015 |
| D (related) | Frequency-rank baseline | 0.055 | 0.022 |
| D (related) | Knight-style EM (revised rule) | 0.258 | 0.254 |
| D (related) | Knight-style EM (original rule) | 0.246 | 0.255 |
| D (related) | EM cognate-matcher | 0.067 | 0.062 |

## 4. Task D vs sister-language distance (Indus point)

| Sound change / lexical repl. | Tier | Method | Mean token acc. | Task C acc. |
|---|---|---|---|---|
| 0.10 / 0.05 | related | Frequency-rank baseline | 0.057 [0.03, 0.09] | n/a |
| 0.10 / 0.05 | related | Knight-style EM (revised rule) | 0.281 [0.15, 0.40] | n/a |
| 0.10 / 0.05 | related | Knight-style EM (original rule) | 0.251 [0.13, 0.36] | n/a |
| 0.10 / 0.05 | related | EM cognate-matcher | 0.066 [0.03, 0.10] | n/a |
| 0.10 / 0.05 | candidates | Frequency-rank baseline | 0.030 [0.01, 0.06] | 0.45 [0.25, 0.67] |
| 0.10 / 0.05 | candidates | Knight-style EM (revised rule) | 0.169 [0.06, 0.29] | 0.45 [0.12, 0.80] |
| 0.10 / 0.05 | candidates | Knight-style EM (original rule) | 0.028 [0.01, 0.06] | 0.20 [0.00, 0.60] |
| 0.10 / 0.05 | candidates | EM cognate-matcher | 0.024 [0.01, 0.05] | 0.22 [0.12, 0.33] |
| 0.30 / 0.20 | related | Frequency-rank baseline | 0.055 [0.03, 0.09] | n/a |
| 0.30 / 0.20 | related | Knight-style EM (revised rule) | 0.258 [0.13, 0.38] | n/a |
| 0.30 / 0.20 | related | Knight-style EM (original rule) | 0.246 [0.12, 0.36] | n/a |
| 0.30 / 0.20 | related | EM cognate-matcher | 0.067 [0.03, 0.11] | n/a |
| 0.30 / 0.20 | candidates | Frequency-rank baseline | 0.029 [0.01, 0.05] | 0.42 [0.23, 0.63] |
| 0.30 / 0.20 | candidates | Knight-style EM (revised rule) | 0.146 [0.05, 0.24] | 0.45 [0.12, 0.80] |
| 0.30 / 0.20 | candidates | Knight-style EM (original rule) | 0.021 [0.01, 0.04] | 0.20 [0.00, 0.60] |
| 0.30 / 0.20 | candidates | EM cognate-matcher | 0.023 [0.01, 0.05] | 0.23 [0.12, 0.37] |
| 0.50 / 0.35 | related | Frequency-rank baseline | 0.055 [0.02, 0.09] | n/a |
| 0.50 / 0.35 | related | Knight-style EM (revised rule) | 0.258 [0.13, 0.37] | n/a |
| 0.50 / 0.35 | related | Knight-style EM (original rule) | 0.238 [0.12, 0.35] | n/a |
| 0.50 / 0.35 | related | EM cognate-matcher | 0.060 [0.03, 0.09] | n/a |
| 0.50 / 0.35 | candidates | Frequency-rank baseline | 0.027 [0.01, 0.05] | 0.37 [0.15, 0.62] |
| 0.50 / 0.35 | candidates | Knight-style EM (revised rule) | 0.148 [0.05, 0.25] | 0.43 [0.12, 0.77] |
| 0.50 / 0.35 | candidates | Knight-style EM (original rule) | 0.021 [0.01, 0.04] | 0.20 [0.00, 0.60] |
| 0.50 / 0.35 | candidates | EM cognate-matcher | 0.021 [0.01, 0.04] | 0.18 [0.05, 0.33] |
| 0.70 / 0.50 | related | Frequency-rank baseline | 0.052 [0.02, 0.08] | n/a |
| 0.70 / 0.50 | related | Knight-style EM (revised rule) | 0.237 [0.13, 0.34] | n/a |
| 0.70 / 0.50 | related | Knight-style EM (original rule) | 0.223 [0.11, 0.33] | n/a |
| 0.70 / 0.50 | related | EM cognate-matcher | 0.061 [0.02, 0.10] | n/a |
| 0.70 / 0.50 | candidates | Frequency-rank baseline | 0.025 [0.01, 0.04] | 0.35 [0.15, 0.58] |
| 0.70 / 0.50 | candidates | Knight-style EM (revised rule) | 0.137 [0.05, 0.23] | 0.43 [0.12, 0.75] |
| 0.70 / 0.50 | candidates | Knight-style EM (original rule) | 0.022 [0.01, 0.04] | 0.20 [0.00, 0.60] |
| 0.70 / 0.50 | candidates | EM cognate-matcher | 0.021 [0.01, 0.04] | 0.17 [0.05, 0.30] |

## 5. Removing the script-type oracle (Indus point)

The solver's unit level comes from the leave-one-source-out prediction of `script_type_lr`, which is correct for 43% of these corpora.

| Tier | Method | Mean token acc. (oracle script type) | Mean token acc. (predicted) | Task C (oracle → predicted) |
|---|---|---|---|---|
| candidates | Frequency-rank baseline | 0.029 [0.01, 0.05] | 0.031 [0.01, 0.06] | 0.42 → 0.35 |
| candidates | Knight-style EM (revised rule) | 0.146 [0.05, 0.25] | 0.119 [0.03, 0.21] | 0.45 → 0.45 |
| candidates | Knight-style EM (original rule) | 0.021 [0.01, 0.04] | 0.016 [0.00, 0.03] | 0.20 → 0.20 |
| candidates | EM cognate-matcher | 0.023 [0.01, 0.05] | 0.016 [0.01, 0.03] | 0.23 → 0.17 |
| none | Frequency-rank baseline | 0.014 [0.01, 0.02] | 0.014 [0.01, 0.02] | 0.18 → 0.15 |
| none | Knight-style EM (revised rule) | 0.033 [0.02, 0.05] | 0.028 [0.01, 0.04] | 0.10 → 0.13 |
| none | Knight-style EM (original rule) | 0.018 [0.01, 0.03] | 0.015 [0.00, 0.03] | 0.00 → 0.00 |
| none | EM cognate-matcher | 0.012 [0.01, 0.02] | 0.009 [0.00, 0.02] | 0.03 → 0.03 |
| related | Frequency-rank baseline | 0.055 [0.03, 0.09] | 0.047 [0.02, 0.08] | n/a |
| related | Knight-style EM (revised rule) | 0.258 [0.13, 0.38] | 0.214 [0.10, 0.33] | n/a |
| related | Knight-style EM (original rule) | 0.246 [0.12, 0.36] | 0.208 [0.09, 0.32] | n/a |
| related | EM cognate-matcher | 0.067 [0.03, 0.11] | 0.050 [0.02, 0.08] | n/a |

## 6. Size sweep (mean length 4.6)

| texts | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 500 | 0.82 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.42 (Knight-style EM (revised rule)) | 0.102 (Knight-style EM (revised rule)) | 0.028 (Knight-style EM (revised rule)) | 0.189 (Knight-style EM (revised rule)) |
| 1000 | 0.69 (Lee 2010 tree) | 0.47 (Inventory/freq. LR) | 0.43 (Knight-style EM (revised rule)) | 0.117 (Knight-style EM (revised rule)) | 0.031 (Knight-style EM (revised rule)) | 0.203 (Knight-style EM (revised rule)) |
| 2000 | 0.69 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.35 (Frequency-rank baseline) | 0.128 (Knight-style EM (revised rule)) | 0.028 (Knight-style EM (revised rule)) | 0.267 (Knight-style EM (revised rule)) |
| 2906 | 0.77 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.45 (Knight-style EM (revised rule)) | 0.146 (Knight-style EM (revised rule)) | 0.033 (Knight-style EM (revised rule)) | 0.258 (Knight-style EM (revised rule)) |
| 5500 | 0.79 (Lee 2010 tree) | 0.40 (Inventory/freq. LR) | 0.45 (Knight-style EM (revised rule)) | 0.175 (Knight-style EM (revised rule)) | 0.036 (Knight-style EM (revised rule)) | 0.264 (Knight-style EM (revised rule)) |
| 10000 | 0.74 (Rao 2009 entropy) | 0.48 (Inventory/freq. LR) | 0.42 (Knight-style EM (revised rule)) | 0.190 (Knight-style EM (revised rule)) | 0.038 (Knight-style EM (revised rule)) | 0.283 (Knight-style EM (revised rule)) |
| 20000 | 0.73 (Lee 2010 tree) | 0.40 (Inventory/freq. LR) | 0.43 (Knight-style EM (revised rule)) | 0.167 (Knight-style EM (revised rule)) | 0.032 (Knight-style EM (revised rule)) | 0.293 (Knight-style EM (revised rule)) |
| 50000 | 0.71 (Rao 2009 entropy) | 0.45 (Inventory/freq. LR) | 0.42 (Knight-style EM (revised rule)) | 0.169 (Knight-style EM (revised rule)) | 0.036 (Knight-style EM (revised rule)) | 0.290 (Knight-style EM (revised rule)) |

Same sweep, only corpora meeting every target:

| texts | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 2906 | nan (-) | 0.33 (Segment length) | 0.57 (Knight-style EM (original rule)) | 0.211 (Knight-style EM (revised rule)) | 0.025 (Knight-style EM (revised rule)) | 0.255 (Knight-style EM (original rule)) |

## 7. Length sweep (2,906 texts)

| mean signs/text | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 3.0 | 0.83 (Rao 2009 entropy) | 0.38 (Inventory/freq. LR) | 0.33 (Frequency-rank baseline) | 0.086 (Knight-style EM (revised rule)) | 0.025 (Knight-style EM (revised rule)) | 0.171 (Knight-style EM (revised rule)) |
| 4.6 | 0.77 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.45 (Knight-style EM (revised rule)) | 0.146 (Knight-style EM (revised rule)) | 0.033 (Knight-style EM (revised rule)) | 0.258 (Knight-style EM (revised rule)) |
| 6.0 | 0.64 (Rao 2009 entropy) | 0.40 (Inventory/freq. LR) | 0.50 (Knight-style EM (revised rule)) | 0.193 (Knight-style EM (revised rule)) | 0.034 (Knight-style EM (revised rule)) | 0.332 (Knight-style EM (revised rule)) |
| 10.0 | 0.64 (Multi-feature LR) | 0.48 (Inventory/freq. LR) | 0.65 (Knight-style EM (original rule)) | 0.332 (Knight-style EM (revised rule)) | 0.062 (Knight-style EM (revised rule)) | 0.435 (Knight-style EM (revised rule)) |
| 20.0 | 0.71 (Multi-feature LR) | 0.50 (Inventory/freq. LR) | 0.82 (Knight-style EM (original rule)) | 0.438 (Knight-style EM (revised rule)) | 0.057 (Knight-style EM (revised rule)) | 0.485 (Knight-style EM (revised rule)) |

## 8. Smallest corpus where a method beats chance (lower 95% cluster bound above chance)

Size sweep at mean length 4.6. `never` = not reached by 50,000 texts.

| Task | Method | Smallest size | Smallest size for a strong result |
|---|---|---|---|
| A | Rao 2009 entropy | 500 | never (bal. acc. ≥ 0.9) |
| A | Yadav 2010 n-gram | never | never (bal. acc. ≥ 0.9) |
| A | Positional | never | never (bal. acc. ≥ 0.9) |
| A | Lee 2010 tree | 5500 | never (bal. acc. ≥ 0.9) |
| A | Multi-feature LR | never | never (bal. acc. ≥ 0.9) |
| B | Inventory rule | never | never (acc. ≥ 0.5) |
| B | Inventory/freq. LR | 500 | never (acc. ≥ 0.5) |
| B | Segment length | never | never (acc. ≥ 0.5) |
| C (candidates) | Frequency-rank baseline | never | never (acc. ≥ 0.5) |
| C (candidates) | Knight-style EM (revised rule) | never | never (acc. ≥ 0.5) |
| C (candidates) | Knight-style EM (original rule) | never | never (acc. ≥ 0.5) |
| C (candidates) | EM cognate-matcher | never | never (acc. ≥ 0.5) |
| C (none) | Frequency-rank baseline | never | never (acc. ≥ 0.5) |
| C (none) | Knight-style EM (revised rule) | never | never (acc. ≥ 0.5) |
| C (none) | Knight-style EM (original rule) | never | never (acc. ≥ 0.5) |
| C (none) | EM cognate-matcher | never | never (acc. ≥ 0.5) |
| D (candidates) | Knight-style EM (revised rule) | 5500 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (candidates) | Knight-style EM (original rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (candidates) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | Knight-style EM (revised rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | Knight-style EM (original rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | Knight-style EM (revised rule) | 500 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | Knight-style EM (original rule) | 1000 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |

## 9. Feasibility region at the Indus point (120 random writing-system scenarios)

Each scenario draws allograph, homophony and polyvalence rates, determinatives, word dividers and direction at random around a calibrated script. Language and script type are also random. Scenarios are perturbations, not re-calibrated: mean share of targets still met = 74%.

| Task | Method | Share of scenarios where the method succeeds |
|---|---|---|
| A (languages called languages) | Rao 2009 entropy | 0.79 [0.68, 0.89] |
| A (languages called languages) | Yadav 2010 n-gram | 0.86 [0.76, 0.95] |
| A (languages called languages) | Positional | 0.81 [0.67, 0.92] |
| A (languages called languages) | Lee 2010 tree | 0.69 [0.58, 0.79] |
| A (languages called languages) | Multi-feature LR | 0.80 [0.62, 0.98] |
| B | Inventory rule | 0.27 [0.16, 0.36] |
| B | Inventory/freq. LR | 0.44 [0.32, 0.61] |
| B | Segment length | 0.28 [0.18, 0.37] |
| C (candidates) | Frequency-rank baseline | 0.34 [0.16, 0.54] |
| C (candidates) | Knight-style EM (revised rule) | 0.42 [0.13, 0.73] |
| C (candidates) | Knight-style EM (original rule) | 0.17 [0.00, 0.56] |
| C (candidates) | EM cognate-matcher | 0.20 [0.09, 0.34] |
| C (none) | Frequency-rank baseline | 0.20 [0.00, 0.44] |
| C (none) | Knight-style EM (revised rule) | 0.16 [0.00, 0.42] |
| C (none) | Knight-style EM (original rule) | 0.00 [0.00, 0.00] |
| C (none) | EM cognate-matcher | 0.03 [0.00, 0.08] |
| D ≥50% tokens (candidates) | Frequency-rank baseline | 0.00 [0.00, 0.00] |
| D ≥50% tokens (candidates) | Knight-style EM (revised rule) | 0.07 [0.00, 0.15] |
| D ≥50% tokens (candidates) | Knight-style EM (original rule) | 0.00 [0.00, 0.00] |
| D ≥50% tokens (candidates) | EM cognate-matcher | 0.00 [0.00, 0.00] |
| D ≥50% tokens (none) | Frequency-rank baseline | 0.00 [0.00, 0.00] |
| D ≥50% tokens (none) | Knight-style EM (revised rule) | 0.00 [0.00, 0.00] |
| D ≥50% tokens (none) | Knight-style EM (original rule) | 0.00 [0.00, 0.00] |
| D ≥50% tokens (none) | EM cognate-matcher | 0.00 [0.00, 0.00] |
| D ≥50% tokens (related, upper bound) | Frequency-rank baseline | 0.00 [0.00, 0.00] |
| D ≥50% tokens (related, upper bound) | Knight-style EM (revised rule) | 0.15 [0.06, 0.24] |
| D ≥50% tokens (related, upper bound) | Knight-style EM (original rule) | 0.15 [0.06, 0.24] |
| D ≥50% tokens (related, upper bound) | EM cognate-matcher | 0.00 [0.00, 0.00] |
