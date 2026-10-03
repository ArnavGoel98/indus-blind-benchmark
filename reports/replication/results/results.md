# Results

Profile `replication`: 1113 runs, 0 failed (listed at the end if any). Seeds: [3, 4, 5]. Indus point: 2,906 texts, mean 4.6 signs (Mahadevan 1977, verified).

**Methods were frozen before this run** at git tag `frozen-v1` (commit e625f568d7). No method code changed afterwards.

**Intervals.** Pooled rates and means carry 95% *cluster-bootstrap* intervals: whole source languages or control families are resampled, then corpora within them. Corpora from one source are not independent, so these intervals are wider than Wilson intervals (Wilson bounds are kept in `aggregate.json`). Per-family rates use Wilson intervals. Task A and B decision rules are learned leave-one-source-out.

**How to read Task D.** Solvers are given the true script type (an oracle; Section 6 removes it). The `related` tier gives them a close synthetic relative, which is **not** the Indus situation: treat it as an upper bound. The Indus-relevant tiers are `candidates` and `none`. Default sister distance: sound change 0.3, lexical replacement 0.2. Section 5 varies it.

## 1. Leading result: the `holdout` regime

Under `holdout` only size, length and inventory are calibrated. The frequency and positional statistics that methods 1-3 measure are left free, so methods cannot be rewarded for statistics we injected. `full` tunes them too. `wrong_prior` calibrates to deliberately wrong targets. A conclusion that holds only under `full` is suspect.

| Task | Method | `holdout` | `full` |
|---|---|---|---|
| A | Rao 2009 entropy | 0.49 [0.25, 0.75] | 0.77 [0.56, 0.90] |
| A | Yadav 2010 n-gram | 0.66 [0.43, 0.86] | 0.64 [0.44, 0.83] |
| A | Positional | 0.56 [0.37, 0.76] | 0.67 [0.46, 0.88] |
| A | Lee 2010 tree | 0.65 [0.43, 0.87] | 0.72 [0.52, 0.93] |
| A | Multi-feature LR | 0.58 [0.39, 0.82] | 0.66 [0.47, 0.87] |
| B | Inventory rule | 0.25 [0.15, 0.37] | 0.25 [0.13, 0.37] |
| B | Inventory/freq. LR | 0.45 [0.30, 0.60] | 0.43 [0.28, 0.60] |
| B | Segment length | 0.27 [0.12, 0.43] | 0.25 [0.12, 0.38] |
| D (related, upper bound) | Frequency-rank baseline | 0.058 [0.04, 0.08] | 0.051 [0.03, 0.08] |
| D (related, upper bound) | Knight-style EM (revised rule) | 0.261 [0.14, 0.39] | 0.259 [0.15, 0.37] |
| D (related, upper bound) | Knight-style EM (original rule) | 0.243 [0.12, 0.37] | 0.239 [0.13, 0.35] |
| D (related, upper bound) | EM cognate-matcher | 0.084 [0.05, 0.12] | 0.061 [0.03, 0.10] |

Kendall's tau between Task A method rankings under `full` and each other regime:

- `holdout`: tau = -0.60

## 2. Indus point, regime `full` (81 corpora)

### Task A: language vs non-language. **Status: UNRESOLVED**

We label language detection unresolved. Balanced accuracy averages over control families we built ourselves, and a method can score well on average while misclassifying a whole family. The false-positive rates per family below are the result to cite. The adversarial control is tuned to imitate language entropy (Sproat 2014).

| Method | Balanced acc. | Recall on languages | Specificity on controls |
|---|---|---|---|
| Rao 2009 entropy | 0.77 [0.56, 0.90] | 0.70 [0.52, 0.88] | 0.83 [0.50, 1.00] |
| Yadav 2010 n-gram | 0.64 [0.44, 0.83] | 0.83 [0.70, 0.95] | 0.44 [0.11, 0.83] |
| Positional | 0.67 [0.46, 0.88] | 0.83 [0.70, 0.95] | 0.50 [0.17, 0.83] |
| Lee 2010 tree | 0.72 [0.52, 0.93] | 0.88 [0.73, 1.00] | 0.56 [0.17, 0.89] |
| Multi-feature LR | 0.66 [0.47, 0.87] | 0.93 [0.82, 1.00] | 0.39 [0.06, 0.78] |

**False-positive rate per control family** (share classified as linguistic; 0 is correct for every control. Kamon descriptions are Japanese text, so a high rate there is defensible):

| Method | heraldry | admin_tags | emblem_markov | adversarial | rao_type1 | rao_type2 | kamon | languages (recall) |
|---|---|---|---|---|---|---|---|---|
| Rao 2009 entropy | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.70 |
| Yadav 2010 n-gram | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.33 [0.06, 0.79] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.83 |
| Positional | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.83 |
| Lee 2010 tree | 0.67 [0.21, 0.94] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.88 |
| Multi-feature LR | 0.67 [0.21, 0.94] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 0.00 [0.00, 0.56] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 1.00 [0.44, 1.00] | 0.93 |

### Task B: script type (chance 0.25)

| Method | Accuracy |
|---|---|
| Inventory rule | 0.25 [0.13, 0.37] (n=60, 5 languages) |
| Inventory/freq. LR | 0.43 [0.28, 0.60] (n=60, 5 languages) |
| Segment length | 0.25 [0.12, 0.38] (n=60, 5 languages) |

The inventory rule is defeated by construction: every corpus is calibrated to 400-700 signs.

### Tasks C and D: family and sign values (Indus-relevant tiers first)

Both EM selection rules are reported. The *revised* rule was adopted during development after the *original* rule picked Sumerian for almost every corpus. Readers should compare both.

| Tier | Method | Task C acc. (chance) | Task D mean token acc. | D: corpora ≥50% | D: sign-type acc. |
|---|---|---|---|---|---|
| candidates | Frequency-rank baseline | 0.40 [0.20, 0.63] (0.25) | 0.037 [0.02, 0.06] | 0.00 [0.00, 0.00] | 0.003 |
| candidates | Knight-style EM (revised rule) | 0.38 [0.10, 0.68] (0.25) | 0.136 [0.05, 0.23] | 0.12 [0.02, 0.25] | 0.066 |
| candidates | Knight-style EM (original rule) | 0.20 [0.00, 0.60] (0.25) | 0.033 [0.01, 0.06] | 0.00 [0.00, 0.00] | 0.016 |
| candidates | EM cognate-matcher | 0.15 [0.05, 0.27] (0.25) | 0.020 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.003 |
| none | Frequency-rank baseline | 0.17 [0.00, 0.38] (0.30) | 0.022 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.002 |
| none | Knight-style EM (revised rule) | 0.13 [0.00, 0.40] (0.30) | 0.030 [0.02, 0.05] | 0.00 [0.00, 0.00] | 0.017 |
| none | Knight-style EM (original rule) | 0.00 [0.00, 0.00] (0.30) | 0.024 [0.01, 0.04] | 0.00 [0.00, 0.00] | 0.011 |
| none | EM cognate-matcher | 0.02 [0.00, 0.07] (0.30) | 0.015 [0.01, 0.03] | 0.00 [0.00, 0.00] | 0.003 |
| related (upper bound) | Frequency-rank baseline | n/a | 0.051 [0.03, 0.08] | 0.00 [0.00, 0.00] | 0.004 |
| related (upper bound) | Knight-style EM (revised rule) | n/a | 0.259 [0.15, 0.37] | 0.25 [0.08, 0.42] | 0.127 |
| related (upper bound) | Knight-style EM (original rule) | n/a | 0.239 [0.13, 0.35] | 0.25 [0.08, 0.42] | 0.142 |
| related (upper bound) | EM cognate-matcher | n/a | 0.061 [0.03, 0.10] | 0.00 [0.00, 0.00] | 0.006 |

Segmentation boundary F1 (branching entropy vs true word starts): 0.47

## 3. Robustness: only corpora that meet every calibration target

At the Indus point, 6 of 81 corpora meet every hard target (6 of them languages). Rules are re-learned inside this subset.

| Task | Method | All corpora | Passing only |
|---|---|---|---|
| A | Rao 2009 entropy | - | - |
| A | Yadav 2010 n-gram | - | - |
| A | Positional | - | - |
| A | Lee 2010 tree | - | - |
| A | Multi-feature LR | - | - |
| B | Inventory rule | 0.25 [0.13, 0.37] | 0.00 [0.00, 0.00] |
| B | Inventory/freq. LR | 0.43 [0.28, 0.60] | 0.00 [0.00, 0.00] |
| B | Segment length | 0.25 [0.12, 0.38] | 0.00 [0.00, 0.00] |
| D (candidates) | Frequency-rank baseline | 0.037 | 0.004 |
| D (candidates) | Knight-style EM (revised rule) | 0.136 | 0.229 |
| D (candidates) | Knight-style EM (original rule) | 0.033 | 0.034 |
| D (candidates) | EM cognate-matcher | 0.020 | 0.002 |
| D (none) | Frequency-rank baseline | 0.022 | 0.014 |
| D (none) | Knight-style EM (revised rule) | 0.030 | 0.021 |
| D (none) | Knight-style EM (original rule) | 0.024 | 0.013 |
| D (none) | EM cognate-matcher | 0.015 | 0.002 |
| D (related) | Frequency-rank baseline | 0.051 | 0.009 |
| D (related) | Knight-style EM (revised rule) | 0.259 | 0.285 |
| D (related) | Knight-style EM (original rule) | 0.239 | 0.262 |
| D (related) | EM cognate-matcher | 0.061 | 0.026 |

## 5. Removing the script-type oracle (Indus point)

The solver's unit level comes from the leave-one-source-out prediction of `script_type_lr`, which is correct for 43% of these corpora.

| Tier | Method | Mean token acc. (oracle script type) | Mean token acc. (predicted) | Task C (oracle → predicted) |
|---|---|---|---|---|
| candidates | Frequency-rank baseline | 0.037 [0.02, 0.06] | 0.032 [0.01, 0.06] | 0.40 → 0.25 |
| candidates | Knight-style EM (revised rule) | 0.136 [0.05, 0.23] | 0.106 [0.03, 0.20] | 0.38 → 0.38 |
| candidates | Knight-style EM (original rule) | 0.033 [0.01, 0.06] | 0.022 [0.01, 0.04] | 0.20 → 0.20 |
| candidates | EM cognate-matcher | 0.020 [0.01, 0.04] | 0.020 [0.01, 0.03] | 0.15 → 0.10 |
| none | Frequency-rank baseline | 0.022 [0.01, 0.03] | 0.021 [0.01, 0.03] | 0.17 → 0.13 |
| none | Knight-style EM (revised rule) | 0.030 [0.02, 0.05] | 0.027 [0.01, 0.05] | 0.13 → 0.15 |
| none | Knight-style EM (original rule) | 0.024 [0.01, 0.04] | 0.018 [0.00, 0.04] | 0.00 → 0.00 |
| none | EM cognate-matcher | 0.015 [0.01, 0.03] | 0.015 [0.00, 0.03] | 0.02 → 0.00 |
| related | Frequency-rank baseline | 0.051 [0.02, 0.08] | 0.042 [0.02, 0.07] | n/a |
| related | Knight-style EM (revised rule) | 0.259 [0.15, 0.37] | 0.213 [0.11, 0.32] | n/a |
| related | Knight-style EM (original rule) | 0.239 [0.13, 0.35] | 0.203 [0.10, 0.32] | n/a |
| related | EM cognate-matcher | 0.061 [0.02, 0.10] | 0.048 [0.02, 0.08] | n/a |

## 6. Size sweep (mean length 4.6)

| texts | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 500 | 0.79 (Rao 2009 entropy) | 0.37 (Inventory/freq. LR) | 0.40 (Frequency-rank baseline) | 0.087 (Knight-style EM (revised rule)) | 0.027 (Knight-style EM (revised rule)) | 0.191 (Knight-style EM (revised rule)) |
| 1000 | 0.74 (Lee 2010 tree) | 0.48 (Inventory/freq. LR) | 0.43 (Frequency-rank baseline) | 0.109 (Knight-style EM (revised rule)) | 0.038 (Knight-style EM (revised rule)) | 0.222 (Knight-style EM (revised rule)) |
| 2000 | 0.80 (Lee 2010 tree) | 0.42 (Inventory/freq. LR) | 0.38 (Knight-style EM (revised rule)) | 0.122 (Knight-style EM (revised rule)) | 0.032 (Knight-style EM (revised rule)) | 0.249 (Knight-style EM (revised rule)) |
| 2906 | 0.77 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.40 (Frequency-rank baseline) | 0.136 (Knight-style EM (revised rule)) | 0.030 (Knight-style EM (revised rule)) | 0.259 (Knight-style EM (revised rule)) |
| 5500 | 0.71 (Rao 2009 entropy) | 0.40 (Inventory/freq. LR) | 0.42 (Frequency-rank baseline) | 0.146 (Knight-style EM (revised rule)) | 0.038 (Knight-style EM (revised rule)) | 0.273 (Knight-style EM (revised rule)) |
| 10000 | 0.76 (Lee 2010 tree) | 0.37 (Inventory/freq. LR) | 0.45 (Knight-style EM (revised rule)) | 0.187 (Knight-style EM (revised rule)) | 0.039 (Knight-style EM (revised rule)) | 0.295 (Knight-style EM (revised rule)) |
| 20000 | 0.74 (Rao 2009 entropy) | 0.45 (Inventory/freq. LR) | 0.45 (Frequency-rank baseline) | 0.159 (Knight-style EM (revised rule)) | 0.035 (Knight-style EM (revised rule)) | 0.286 (Knight-style EM (revised rule)) |
| 50000 | 0.73 (Rao 2009 entropy) | 0.53 (Inventory/freq. LR) | 0.42 (Knight-style EM (revised rule)) | 0.162 (Knight-style EM (revised rule)) | 0.032 (Knight-style EM (revised rule)) | 0.299 (Knight-style EM (revised rule)) |

Same sweep, only corpora meeting every target:

| texts | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 2906 | nan (-) | 0.00 (Inventory rule) | 0.67 (Knight-style EM (original rule)) | 0.229 (Knight-style EM (revised rule)) | 0.021 (Knight-style EM (revised rule)) | 0.285 (Knight-style EM (revised rule)) |

## 7. Length sweep (2,906 texts)

| mean signs/text | A best bal. acc. | B best acc. | C best acc. (candidates) | D best (candidates) | D best (none) | D best (related, upper bound) |
|---|---|---|---|---|---|---|
| 3.0 | 0.91 (Rao 2009 entropy) | 0.50 (Inventory/freq. LR) | 0.35 (Frequency-rank baseline) | 0.085 (Knight-style EM (revised rule)) | 0.031 (Knight-style EM (revised rule)) | 0.167 (Knight-style EM (revised rule)) |
| 4.6 | 0.77 (Rao 2009 entropy) | 0.43 (Inventory/freq. LR) | 0.40 (Frequency-rank baseline) | 0.136 (Knight-style EM (revised rule)) | 0.030 (Knight-style EM (revised rule)) | 0.259 (Knight-style EM (revised rule)) |
| 6.0 | 0.70 (Multi-feature LR) | 0.45 (Inventory/freq. LR) | 0.50 (Knight-style EM (revised rule)) | 0.192 (Knight-style EM (revised rule)) | 0.036 (Knight-style EM (revised rule)) | 0.321 (Knight-style EM (revised rule)) |
| 10.0 | 0.62 (Multi-feature LR) | 0.52 (Inventory/freq. LR) | 0.65 (Knight-style EM (original rule)) | 0.289 (Knight-style EM (revised rule)) | 0.051 (Knight-style EM (revised rule)) | 0.410 (Knight-style EM (original rule)) |
| 20.0 | 0.73 (Multi-feature LR) | 0.50 (Inventory/freq. LR) | 0.87 (Knight-style EM (original rule)) | 0.450 (Knight-style EM (original rule)) | 0.057 (Knight-style EM (revised rule)) | 0.502 (Knight-style EM (revised rule)) |

## 8. Smallest corpus where a method beats chance (lower 95% cluster bound above chance)

Size sweep at mean length 4.6. `never` = not reached by 50,000 texts.

| Task | Method | Smallest size | Smallest size for a strong result |
|---|---|---|---|
| A | Rao 2009 entropy | 500 | never (bal. acc. ≥ 0.9) |
| A | Yadav 2010 n-gram | never | never (bal. acc. ≥ 0.9) |
| A | Positional | never | never (bal. acc. ≥ 0.9) |
| A | Lee 2010 tree | 1000 | never (bal. acc. ≥ 0.9) |
| A | Multi-feature LR | never | never (bal. acc. ≥ 0.9) |
| B | Inventory rule | never | never (acc. ≥ 0.5) |
| B | Inventory/freq. LR | 1000 | 50000 (acc. ≥ 0.5) |
| B | Segment length | never | never (acc. ≥ 0.5) |
| C (candidates) | Frequency-rank baseline | never | never (acc. ≥ 0.5) |
| C (candidates) | Knight-style EM (revised rule) | never | never (acc. ≥ 0.5) |
| C (candidates) | Knight-style EM (original rule) | never | never (acc. ≥ 0.5) |
| C (candidates) | EM cognate-matcher | never | never (acc. ≥ 0.5) |
| C (none) | Frequency-rank baseline | never | never (acc. ≥ 0.5) |
| C (none) | Knight-style EM (revised rule) | never | never (acc. ≥ 0.5) |
| C (none) | Knight-style EM (original rule) | never | never (acc. ≥ 0.5) |
| C (none) | EM cognate-matcher | never | never (acc. ≥ 0.5) |
| D (candidates) | Knight-style EM (revised rule) | 10000 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (candidates) | Knight-style EM (original rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (candidates) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | Knight-style EM (revised rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | Knight-style EM (original rule) | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (none) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | Knight-style EM (revised rule) | 500 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | Knight-style EM (original rule) | 1000 (vs baseline) | never (half of corpora ≥50% tokens) |
| D (related, upper bound) | EM cognate-matcher | never (vs baseline) | never (half of corpora ≥50% tokens) |
