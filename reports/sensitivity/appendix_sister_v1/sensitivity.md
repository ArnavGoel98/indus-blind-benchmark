# Sensitivity: duplicate-text rate x sign inventory at the Indus point

Methods frozen at `frozen-v1`; generator-v1 with `full`-regime knobs. Each corpus has 2,906 texts with mean length 4.6. Two properties that published Indus statistics leave open are set exactly: the share of texts that repeat an earlier text, and the number of sign types (reached by adding allographs). Everything else is unchanged. Accuracy is Task D token accuracy. The 95% intervals resample whole source languages (cluster bootstrap).

**Scores in this report.** Upper bound (sister-v1, known overlap), with oracle sound correspondences.

**Nothing here is a measurement of the Indus script.** The map shows how much the difficulty of our synthetic Indus-like corpora depends on two properties the published Indus statistics do not pin down.

> **LIMITATION: inventory is raised only by adding allographs (graphic variants of one value), and no tested method merges allographs. High-inventory cells therefore measure these solvers' failure to merge variants, not decipherability in general.**

## Coverage

Records: 1800. Status counts (after the validity rule): length_distorted 117, ok 1454, tolerance_miss 15, unreachable_high 127, unreachable_low 87.

* `unreachable_low`: the script has more sign types than the target even with no allographs.
* `unreachable_high`: even ~400 variants per sign do not reach the target. The variant weights are 1/(j+1)^2, so rare variants hardly occur.
* `unreachable_dup`: too few distinct texts for so low a duplicate rate.
* `length_distorted`: more than 10% of texts needed a substitute length.
* `tolerance_miss`: bisection ended outside +/-3% (min 10 signs) of the target.

**Strict panel** (every cell has the same composition): the 5 of 20 language x script combinations that are valid in all 30 cells: latin/logosyllabic, sanskrit/logographic, sanskrit/syllabic, sumerian/logographic, tamil/syllabic.

**Plausible-box panel**: the 10 combinations valid in every cell of the plausible box (duplicates 0.2-0.4, inventory 400-700; fixed in the profile before results): finnish/syllabic, latin/logosyllabic, latin/syllabic, sanskrit/alphabetic, sanskrit/logographic, sanskrit/syllabic, sumerian/alphabetic, sumerian/logographic, sumerian/syllabic, tamil/syllabic.

Combinations missing from the balanced panel: finnish/alphabetic, finnish/logographic, finnish/logosyllabic, finnish/syllabic, latin/alphabetic, latin/logographic, latin/syllabic, sanskrit/alphabetic, sanskrit/logosyllabic, sumerian/alphabetic, sumerian/logosyllabic, sumerian/syllabic, tamil/alphabetic, tamil/logographic, tamil/logosyllabic. The `all` panel uses every valid corpus, so its cell composition varies.

## Published reference points

| Quantity | Label | Value | Source | Verified |
|---|---|---|---|---|
| duplicate_text_fraction | M77 raw (Yadav 2010 Fig. 2) | 0.354 | YADAV2010 | True |
| duplicate_text_fraction | M77 without 4 outlier texts | 0.281 | YADAV2010 | True |
| duplicate_text_fraction | ICIT (Nair 2026, preprint) | 0.237 | NAIR2026 | False |
| sign_inventory | Parpola 1994 | 386 | PARPOLA1994 | VIA RAO2018 |
| sign_inventory | Mahadevan 1977 | 417 | M77 | VIA YADAV2010 and RAO2018 |
| sign_inventory | Wells 2006 | 676 | WELLS2006 | VIA YADAV2010 |
| sign_inventory | Wells 2015 | 694 | WELLS2015 | VIA RAO2018 |
| sign_inventory | Fuls 2023 (>700, unverified) | 700 | FULS2023 | False |

Sign-list sizes are catalogue sizes over each author's whole corpus (ICIT-based lists cover more texts than M77's 2,906). The map's inventory axis counts sign types observed in a 2,906-text corpus, so only M77 is like-for-like. The others show where lumping vs splitting of variants would place the corpus, approximately and probably too high.

Duplicate-rate method (M77): Exact series values read from the vector drawing commands of Fig. 2 in arXiv:0901.3017 (page 3), not by eye. Texts by length 1..14: M77 raw = 177, 608, 473, 429, 368, 225, 169, 74, 29, 24, 11, 1, 1, 2 (sum 2,591); M77-unique = 82, 215, 309, 292, 308, 209, 136, 60, 27, 22, 9, 1, 1, 2 (sum 1,673). Check: the EBUDS series from the same figure sums to 1,548, the published EBUDS size. Duplicate fraction = 1 - 1673/2591 = 0.354.

Caveat: The plotted raw M77 holds 2,591 texts, not the 2,906 of M77; the paper does not say which 315 are left out (we guess multi-line or unmeasurable texts, but this is NOT verified). Identity is identity of M77 sign readings, so allograph decisions in M77's sign list affect the count.

## Within one language and script: spread across the plausible box

For each combination in the plausible-box panel: seed-averaged accuracy in each box cell, then spread = best cell - worst cell. Each spread compares a combination with itself, so composition cannot cause it. The 95% CI of the mean spread resamples source languages.

| Tier | Method | Combos | Median spread | Mean spread [95% CI] | Share with spread >= 10 points |
|---|---|---|---|---|---|
| candidates | Frequency-rank baseline | 10 | 2.0 | 3.1 [1.3, 7.0] | 10% |
| candidates | Knight-style EM (revised rule) | 10 | 5.5 | 15.4 [3.6, 31.4] | 40% |
| candidates | Knight-style EM (original rule) | 10 | 2.1 | 2.7 [0.9, 4.9] | 0% |
| candidates | EM cognate-matcher | 10 | 2.7 | 4.0 [1.6, 8.6] | 20% |
| none | Frequency-rank baseline | 10 | 1.1 | 1.3 [0.6, 2.0] | 0% |
| none | Knight-style EM (revised rule) | 10 | 3.1 | 2.9 [1.6, 4.3] | 0% |
| none | Knight-style EM (original rule) | 10 | 1.2 | 1.2 [0.6, 2.0] | 0% |
| none | EM cognate-matcher | 10 | 0.9 | 2.0 [0.6, 4.4] | 10% |

Per combination, revised EM, candidates tier (accuracy %, cells as (duplicates, inventory)):

| Combination | Worst cell | Best cell | Spread |
|---|---|---|---|
| sanskrit/syllabic | 13.0 (0.4, 700) | 74.7 (0.2, 400) | 61.8 |
| latin/logosyllabic | 5.7 (0.3, 500) | 47.7 (0.2, 400) | 42.0 |
| finnish/syllabic | 32.3 (0.4, 700) | 49.6 (0.3, 600) | 17.3 |
| latin/syllabic | 2.4 (0.4, 500) | 19.2 (0.2, 400) | 16.8 |
| sanskrit/alphabetic | 14.2 (0.4, 400) | 20.3 (0.2, 500) | 6.2 |
| tamil/syllabic | 0.2 (0.4, 700) | 4.9 (0.3, 500) | 4.7 |
| sumerian/alphabetic | 6.3 (0.3, 400) | 10.9 (0.2, 600) | 4.6 |
| sumerian/syllabic | 0.0 (0.2, 400) | 0.7 (0.2, 500) | 0.7 |
| sanskrit/logographic | 0.0 (0.2, 400) | 0.0 (0.4, 700) | 0.0 |
| sumerian/logographic | 0.0 (0.2, 400) | 0.0 (0.4, 700) | 0.0 |

## How much does difficulty move? (strict panel)

The **plausible box** is duplicates 0.2-0.4 by inventory 400-700. It brackets the published duplicate rates (0.24-0.35) and the sign-list sizes (386 to ~700). Lowest and highest cell means, strict panel:

| Tier | Method | Whole grid: min -> max (cells) | Plausible box: min -> max (cells) |
|---|---|---|---|
| candidates | Frequency-rank baseline | 0.1% -> 4.4% ((0.5, 700) -> (0.0, 400)) | 0.5% -> 1.6% ((0.4, 400) -> (0.3, 400)) |
| candidates | Knight-style EM (revised rule) | 2.6% -> 41.7% ((0.5, 700) -> (0.0, 400)) | 3.9% -> 25.4% ((0.4, 700) -> (0.2, 400)) |
| candidates | Knight-style EM (original rule) | 0.0% -> 20.5% ((0.4, 800) -> (0.0, 400)) | 0.2% -> 1.4% ((0.2, 700) -> (0.4, 400)) |
| candidates | EM cognate-matcher | 0.2% -> 1.7% ((0.4, 500) -> (0.1, 700)) | 0.2% -> 0.8% ((0.4, 500) -> (0.3, 600)) |
| none | Frequency-rank baseline | 0.0% -> 0.7% ((0.0, 400) -> (0.4, 400)) | 0.1% -> 0.7% ((0.4, 700) -> (0.4, 400)) |
| none | Knight-style EM (revised rule) | 0.8% -> 2.4% ((0.5, 700) -> (0.2, 400)) | 0.9% -> 2.4% ((0.3, 400) -> (0.2, 400)) |
| none | Knight-style EM (original rule) | 0.0% -> 0.6% ((0.4, 700) -> (0.5, 800)) | 0.0% -> 0.4% ((0.4, 700) -> (0.2, 500)) |
| none | EM cognate-matcher | 0.0% -> 0.5% ((0.0, 800) -> (0.0, 500)) | 0.0% -> 0.5% ((0.4, 700) -> (0.2, 400)) |

Cells are (duplicates, inventory). The interval for each cell is in the tables below.

## Token accuracy, % [95% cluster CI], box panel

### Frequency-rank baseline, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 4.2 [1.5, 9.8] | 3.8 [0.8, 9.3] | 3.9 [1.1, 9.1] | 3.8 [1.0, 8.6] |
| 0.3 | 3.9 [1.6, 7.8] | 4.2 [1.5, 9.6] | 3.5 [1.3, 7.2] | 3.1 [0.8, 7.1] |
| 0.4 | 3.1 [0.8, 6.8] | 3.5 [0.5, 8.6] | 2.7 [0.7, 5.6] | 2.4 [0.6, 5.1] |

### Knight-style EM (revised rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 21.8 [7.5, 38.6] | 15.9 [4.3, 31.3] | 14.1 [4.4, 27.9] | 12.8 [4.7, 25.5] |
| 0.3 | 19.2 [5.7, 35.3] | 12.8 [4.2, 25.3] | 13.3 [4.9, 27.3] | 11.1 [3.3, 23.1] |
| 0.4 | 14.8 [5.2, 27.2] | 10.4 [3.3, 23.1] | 10.0 [3.4, 20.9] | 8.7 [3.1, 17.6] |

### Knight-style EM (original rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 4.5 [0.3, 8.4] | 4.7 [1.1, 8.3] | 4.6 [0.4, 8.5] | 4.4 [0.8, 7.8] |
| 0.3 | 4.2 [0.4, 7.9] | 4.5 [0.1, 8.5] | 4.3 [0.5, 8.0] | 4.2 [0.3, 7.9] |
| 0.4 | 5.1 [0.6, 8.9] | 3.7 [0.5, 6.7] | 3.5 [0.3, 6.4] | 3.6 [0.1, 6.7] |

### EM cognate-matcher, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 3.0 [1.1, 7.6] | 2.8 [1.2, 5.5] | 2.9 [0.7, 7.3] | 2.2 [0.7, 5.0] |
| 0.3 | 1.6 [0.6, 2.7] | 3.0 [1.0, 7.4] | 2.4 [1.0, 4.6] | 3.1 [0.9, 7.2] |
| 0.4 | 1.8 [0.4, 3.8] | 1.8 [0.2, 4.0] | 1.8 [0.5, 3.9] | 2.2 [0.4, 5.0] |

### Frequency-rank baseline, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 1.6 [0.3, 3.4] | 1.5 [0.1, 3.3] | 1.3 [0.1, 3.4] | 1.4 [0.1, 3.4] |
| 0.3 | 1.6 [0.4, 3.5] | 1.4 [0.1, 3.3] | 1.4 [0.2, 3.4] | 1.5 [0.3, 3.4] |
| 0.4 | 1.9 [0.4, 3.8] | 1.9 [0.2, 4.0] | 1.7 [0.4, 3.8] | 1.4 [0.2, 3.5] |

### Knight-style EM (revised rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 4.1 [2.2, 6.6] | 4.1 [1.6, 7.3] | 4.1 [1.6, 7.0] | 3.8 [1.4, 6.5] |
| 0.3 | 3.7 [1.5, 6.7] | 4.1 [1.8, 7.2] | 4.3 [1.9, 7.4] | 3.9 [1.3, 7.4] |
| 0.4 | 3.3 [1.4, 5.7] | 3.9 [1.6, 6.8] | 3.9 [1.4, 7.1] | 3.7 [1.1, 7.2] |

### Knight-style EM (original rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 2.8 [0.2, 5.7] | 3.2 [1.0, 6.0] | 2.9 [0.4, 5.8] | 3.1 [0.7, 5.8] |
| 0.3 | 3.0 [0.4, 5.8] | 2.6 [0.1, 5.4] | 2.7 [0.5, 5.3] | 2.7 [0.3, 5.6] |
| 0.4 | 3.1 [0.5, 6.1] | 2.8 [0.5, 5.8] | 2.8 [0.3, 5.6] | 2.6 [0.1, 5.5] |

### EM cognate-matcher, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 1.2 [0.6, 1.8] | 1.5 [0.4, 2.8] | 1.3 [0.2, 2.9] | 1.4 [0.4, 2.6] |
| 0.3 | 1.2 [0.4, 2.3] | 1.3 [0.4, 2.6] | 1.5 [0.6, 2.9] | 1.8 [0.5, 3.5] |
| 0.4 | 1.7 [0.3, 3.8] | 1.8 [0.2, 4.0] | 1.7 [0.3, 3.8] | 1.4 [0.1, 3.4] |

Corpora per cell:

| duplicates \ inventory | 400 | 500 | 600 | 700 |
|---|---|---|---|---|
| 0.2 | 30 | 30 | 30 | 30 |
| 0.3 | 30 | 30 | 30 | 30 |
| 0.4 | 30 | 30 | 30 | 30 |

## Token accuracy, % [95% cluster CI], balanced panel

### Frequency-rank baseline, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 4.4 [1.0, 9.8] | 1.8 [0.3, 3.9] | 1.3 [0.2, 3.4] | 1.6 [0.2, 4.1] | 1.3 [0.0, 4.4] |
| 0.1 | 2.5 [0.3, 7.2] | 1.6 [0.3, 3.7] | 1.0 [0.2, 2.4] | 1.7 [0.1, 4.9] | 1.8 [0.3, 4.1] |
| 0.2 | 1.4 [0.1, 3.5] | 0.7 [0.1, 2.4] | 1.2 [0.2, 2.8] | 1.0 [0.2, 2.2] | 1.2 [0.1, 3.1] |
| 0.3 | 1.6 [0.1, 3.9] | 1.2 [0.2, 3.0] | 1.2 [0.2, 2.8] | 0.7 [0.0, 1.7] | 0.6 [0.0, 1.2] |
| 0.4 | 0.5 [0.1, 1.5] | 0.8 [0.0, 1.7] | 0.9 [0.1, 2.1] | 0.6 [0.1, 1.3] | 0.8 [0.0, 1.7] |
| 0.5 | 0.8 [0.1, 2.1] | 0.6 [0.1, 1.4] | 0.5 [0.0, 1.7] | 0.1 [0.0, 0.3] | 0.4 [0.0, 1.3] |

### Knight-style EM (revised rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 41.7 [12.4, 68.4] | 37.7 [12.6, 60.9] | 23.6 [6.3, 40.1] | 21.1 [4.1, 38.2] | 13.0 [1.6, 27.1] |
| 0.1 | 29.1 [6.5, 54.4] | 21.7 [1.6, 39.8] | 16.4 [2.7, 31.3] | 13.0 [0.8, 26.5] | 10.9 [1.5, 23.1] |
| 0.2 | 25.4 [2.2, 46.0] | 14.6 [0.6, 30.2] | 11.5 [0.6, 24.2] | 8.1 [0.1, 17.7] | 5.5 [0.8, 12.9] |
| 0.3 | 21.3 [0.1, 40.2] | 9.5 [1.4, 20.1] | 8.0 [1.5, 16.2] | 6.2 [0.6, 13.3] | 3.5 [0.2, 7.7] |
| 0.4 | 15.7 [0.2, 30.2] | 5.7 [0.4, 12.4] | 5.1 [0.7, 11.6] | 3.9 [0.1, 8.2] | 4.3 [1.1, 7.6] |
| 0.5 | 6.4 [0.8, 11.8] | 5.0 [1.4, 8.8] | 4.0 [0.2, 9.3] | 2.6 [0.1, 5.4] | 3.5 [0.8, 6.2] |

### Knight-style EM (original rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 20.5 [0.0, 45.8] | 6.1 [0.1, 18.4] | 0.7 [0.0, 2.8] | 0.7 [0.1, 1.7] | 1.0 [0.0, 2.9] |
| 0.1 | 12.9 [0.3, 31.1] | 1.0 [0.0, 3.6] | 0.7 [0.1, 2.2] | 0.5 [0.0, 1.5] | 0.5 [0.1, 1.3] |
| 0.2 | 1.3 [0.0, 4.1] | 0.9 [0.1, 2.4] | 0.8 [0.0, 2.0] | 0.2 [0.0, 0.6] | 0.4 [0.1, 0.8] |
| 0.3 | 0.4 [0.0, 1.7] | 0.8 [0.0, 2.2] | 0.6 [0.0, 1.9] | 0.4 [0.0, 0.9] | 0.7 [0.0, 2.2] |
| 0.4 | 1.4 [0.0, 5.0] | 0.4 [0.0, 1.0] | 0.4 [0.0, 1.1] | 0.4 [0.0, 1.6] | 0.0 [0.0, 0.1] |
| 0.5 | 0.4 [0.0, 1.2] | 0.1 [0.0, 0.4] | 0.4 [0.0, 1.8] | 0.3 [0.0, 0.9] | 0.8 [0.0, 2.3] |

### EM cognate-matcher, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.3 [0.0, 0.6] | 0.9 [0.1, 2.8] | 0.2 [0.0, 0.4] | 1.3 [0.0, 4.3] | 0.5 [0.0, 1.9] |
| 0.1 | 1.5 [0.1, 4.9] | 1.0 [0.0, 3.7] | 0.6 [0.0, 2.0] | 1.7 [0.0, 5.7] | 1.0 [0.0, 3.5] |
| 0.2 | 0.7 [0.0, 1.6] | 0.6 [0.0, 1.5] | 0.5 [0.0, 1.9] | 0.2 [0.0, 0.6] | 1.0 [0.0, 3.0] |
| 0.3 | 0.7 [0.0, 2.3] | 0.5 [0.0, 2.0] | 0.8 [0.0, 2.4] | 0.3 [0.0, 0.6] | 0.5 [0.0, 1.9] |
| 0.4 | 0.5 [0.0, 1.6] | 0.2 [0.0, 0.5] | 0.4 [0.0, 1.4] | 0.4 [0.0, 1.5] | 0.4 [0.0, 0.9] |
| 0.5 | 0.4 [0.0, 1.0] | 0.3 [0.0, 0.9] | 0.2 [0.0, 0.4] | 0.4 [0.0, 0.9] | 0.5 [0.0, 1.4] |

### Frequency-rank baseline, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.0 [0.0, 0.0] | 0.5 [0.0, 1.1] | 0.3 [0.0, 0.8] | 0.5 [0.0, 1.1] | 0.2 [0.0, 0.7] |
| 0.1 | 0.2 [0.0, 0.9] | 0.4 [0.0, 1.0] | 0.5 [0.1, 1.1] | 0.3 [0.0, 1.0] | 0.4 [0.0, 0.9] |
| 0.2 | 0.6 [0.0, 1.8] | 0.4 [0.0, 1.3] | 0.2 [0.0, 0.4] | 0.4 [0.0, 1.0] | 0.4 [0.0, 1.3] |
| 0.3 | 0.4 [0.0, 1.1] | 0.6 [0.1, 1.4] | 0.3 [0.1, 0.7] | 0.3 [0.0, 0.7] | 0.3 [0.0, 0.7] |
| 0.4 | 0.7 [0.1, 1.9] | 0.6 [0.0, 1.4] | 0.6 [0.0, 1.4] | 0.1 [0.0, 0.3] | 0.5 [0.1, 1.1] |
| 0.5 | 0.5 [0.1, 1.3] | 0.4 [0.0, 0.9] | 0.2 [0.0, 0.5] | 0.1 [0.0, 0.3] | 0.1 [0.0, 0.3] |

### Knight-style EM (revised rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 1.9 [0.4, 3.6] | 2.2 [0.6, 3.7] | 1.4 [0.2, 2.8] | 1.4 [0.2, 2.6] | 1.7 [0.3, 3.0] |
| 0.1 | 1.4 [0.0, 2.9] | 2.4 [0.7, 4.0] | 2.1 [0.6, 4.1] | 1.8 [0.5, 3.0] | 1.9 [0.6, 3.0] |
| 0.2 | 2.4 [0.7, 4.5] | 1.4 [0.3, 2.8] | 1.3 [0.1, 2.3] | 0.9 [0.1, 1.9] | 2.1 [0.6, 4.2] |
| 0.3 | 0.9 [0.1, 1.9] | 1.7 [0.1, 3.8] | 2.0 [0.6, 3.9] | 1.7 [0.4, 3.1] | 1.2 [0.2, 2.3] |
| 0.4 | 0.9 [0.1, 2.1] | 1.4 [0.3, 2.5] | 1.4 [0.2, 2.7] | 1.2 [0.1, 2.2] | 2.0 [0.4, 3.6] |
| 0.5 | 1.0 [0.3, 2.0] | 1.5 [0.3, 3.2] | 1.1 [0.2, 2.0] | 0.8 [0.1, 1.6] | 1.1 [0.3, 2.0] |

### Knight-style EM (original rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.0 [0.0, 0.1] | 0.1 [0.0, 0.6] | 0.1 [0.0, 0.2] | 0.4 [0.0, 1.1] | 0.3 [0.0, 1.0] |
| 0.1 | 0.3 [0.0, 0.9] | 0.1 [0.0, 0.4] | 0.1 [0.0, 0.3] | 0.2 [0.0, 1.0] | 0.2 [0.0, 0.5] |
| 0.2 | 0.2 [0.0, 0.7] | 0.4 [0.0, 1.2] | 0.3 [0.0, 1.0] | 0.1 [0.0, 0.2] | 0.2 [0.0, 0.4] |
| 0.3 | 0.0 [0.0, 0.2] | 0.1 [0.0, 0.6] | 0.0 [0.0, 0.1] | 0.2 [0.0, 0.5] | 0.3 [0.0, 1.2] |
| 0.4 | 0.1 [0.0, 0.5] | 0.2 [0.0, 0.8] | 0.1 [0.0, 0.5] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| 0.5 | 0.1 [0.0, 0.5] | 0.1 [0.0, 0.3] | 0.0 [0.0, 0.0] | 0.1 [0.0, 0.3] | 0.6 [0.0, 1.9] |

### EM cognate-matcher, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.3 [0.0, 0.6] | 0.5 [0.1, 1.3] | 0.2 [0.0, 0.4] | 0.4 [0.0, 1.2] | 0.0 [0.0, 0.1] |
| 0.1 | 0.4 [0.1, 1.3] | 0.4 [0.0, 1.2] | 0.3 [0.0, 0.8] | 0.3 [0.0, 0.8] | 0.0 [0.0, 0.1] |
| 0.2 | 0.5 [0.0, 1.0] | 0.3 [0.0, 0.7] | 0.2 [0.0, 0.3] | 0.2 [0.0, 0.6] | 0.5 [0.0, 1.2] |
| 0.3 | 0.2 [0.0, 0.5] | 0.1 [0.0, 0.3] | 0.4 [0.0, 0.9] | 0.2 [0.0, 0.5] | 0.1 [0.0, 0.4] |
| 0.4 | 0.5 [0.0, 1.4] | 0.2 [0.0, 0.5] | 0.3 [0.0, 0.9] | 0.0 [0.0, 0.1] | 0.4 [0.0, 0.9] |
| 0.5 | 0.4 [0.0, 1.0] | 0.1 [0.0, 0.4] | 0.4 [0.0, 0.8] | 0.2 [0.0, 0.5] | 0.4 [0.0, 1.1] |

Corpora per cell:

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 13 | 15 | 15 | 15 | 15 |
| 0.1 | 13 | 15 | 15 | 15 | 15 |
| 0.2 | 15 | 15 | 15 | 15 | 15 |
| 0.3 | 15 | 15 | 15 | 15 | 15 |
| 0.4 | 15 | 15 | 15 | 15 | 15 |
| 0.5 | 15 | 15 | 15 | 15 | 15 |

## Token accuracy, % [95% cluster CI], all panel

### Frequency-rank baseline, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 5.5 [3.3, 8.2] | 4.4 [2.4, 7.7] | 4.7 [2.2, 8.8] | 4.0 [2.1, 6.4] | 3.1 [1.8, 4.9] |
| 0.1 | 6.0 [3.3, 9.7] | 5.2 [2.5, 9.4] | 3.9 [2.0, 6.2] | 4.0 [1.9, 6.4] | 3.4 [1.6, 5.9] |
| 0.2 | 5.4 [2.5, 9.7] | 4.3 [2.0, 7.3] | 4.0 [1.9, 6.5] | 3.5 [1.7, 5.8] | 3.4 [1.5, 5.8] |
| 0.3 | 4.2 [2.3, 6.7] | 4.1 [2.3, 6.3] | 3.7 [2.2, 5.5] | 2.8 [0.8, 5.4] | 2.2 [0.4, 4.8] |
| 0.4 | 3.6 [1.8, 5.8] | 3.8 [1.8, 6.3] | 3.0 [1.3, 5.0] | 2.4 [0.7, 4.7] | 1.4 [0.2, 3.6] |
| 0.5 | 3.5 [2.0, 5.2] | 3.3 [1.7, 5.2] | 2.1 [0.4, 4.2] | 1.7 [0.3, 4.5] | 1.6 [0.2, 4.6] |

### Knight-style EM (revised rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 38.6 [16.4, 64.9] | 33.5 [16.6, 53.8] | 25.6 [9.3, 44.3] | 18.0 [8.7, 27.2] | 10.9 [3.5, 19.8] |
| 0.1 | 35.9 [15.1, 59.4] | 25.1 [7.9, 46.5] | 19.8 [7.5, 33.0] | 12.6 [4.2, 22.4] | 9.9 [3.3, 17.8] |
| 0.2 | 28.8 [10.0, 49.2] | 19.6 [5.9, 33.7] | 15.0 [5.2, 26.1] | 9.1 [3.3, 16.9] | 6.9 [2.4, 13.6] |
| 0.3 | 23.8 [8.2, 39.9] | 16.0 [5.4, 28.8] | 12.1 [4.0, 21.8] | 7.1 [2.0, 13.8] | 6.4 [1.6, 14.0] |
| 0.4 | 17.3 [5.7, 30.0] | 12.1 [4.0, 22.2] | 7.2 [2.8, 12.7] | 5.7 [2.0, 10.6] | 4.8 [1.8, 9.6] |
| 0.5 | 13.1 [4.2, 22.3] | 9.0 [3.5, 16.3] | 6.2 [2.3, 11.5] | 4.2 [1.2, 9.5] | 4.3 [1.0, 9.9] |

### Knight-style EM (original rule), candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 14.5 [2.1, 31.5] | 6.7 [1.8, 12.6] | 4.4 [1.5, 7.9] | 3.5 [0.9, 6.6] | 3.7 [0.9, 6.5] |
| 0.1 | 11.6 [2.9, 22.7] | 4.5 [1.5, 7.7] | 3.6 [1.2, 6.5] | 3.2 [0.8, 6.1] | 2.9 [0.5, 5.6] |
| 0.2 | 5.2 [1.7, 8.7] | 4.1 [1.7, 7.0] | 3.7 [1.2, 6.8] | 3.6 [1.1, 6.3] | 2.8 [0.2, 6.0] |
| 0.3 | 4.4 [1.6, 7.6] | 3.5 [1.1, 6.6] | 3.2 [0.9, 6.2] | 2.8 [0.1, 6.1] | 1.8 [0.1, 4.8] |
| 0.4 | 4.9 [2.0, 8.2] | 3.1 [1.1, 5.5] | 2.8 [0.7, 5.1] | 2.2 [0.0, 4.8] | 1.4 [0.0, 4.2] |
| 0.5 | 3.1 [0.8, 6.2] | 3.3 [0.7, 6.4] | 2.7 [0.2, 5.8] | 1.4 [0.0, 4.1] | 0.4 [0.1, 1.0] |

### EM cognate-matcher, candidates tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 3.0 [1.0, 6.1] | 5.2 [1.3, 11.5] | 4.3 [1.0, 9.4] | 4.2 [1.6, 7.5] | 2.7 [1.0, 5.8] |
| 0.1 | 4.7 [1.5, 10.0] | 3.7 [1.3, 7.2] | 2.6 [1.4, 4.0] | 2.7 [1.5, 4.4] | 1.3 [0.5, 2.2] |
| 0.2 | 3.9 [1.5, 8.0] | 3.3 [1.9, 5.1] | 2.4 [1.0, 4.5] | 1.8 [0.8, 3.2] | 1.2 [0.3, 2.2] |
| 0.3 | 3.0 [1.6, 4.8] | 2.8 [1.4, 4.8] | 2.1 [1.2, 3.2] | 2.1 [0.8, 4.2] | 0.8 [0.2, 1.5] |
| 0.4 | 3.1 [0.9, 6.4] | 1.6 [0.6, 2.9] | 1.5 [0.4, 2.9] | 1.5 [0.5, 3.2] | 0.9 [0.2, 2.1] |
| 0.5 | 2.6 [1.0, 4.9] | 2.4 [1.0, 3.9] | 1.5 [0.5, 3.4] | 1.1 [0.3, 2.6] | 0.4 [0.1, 0.9] |

### Frequency-rank baseline, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 3.1 [1.1, 5.7] | 2.6 [1.1, 4.4] | 2.4 [1.0, 4.0] | 1.6 [0.6, 2.9] | 1.3 [0.3, 2.5] |
| 0.1 | 3.2 [1.2, 5.4] | 2.9 [1.3, 4.7] | 2.2 [1.0, 3.4] | 1.8 [0.6, 3.1] | 1.0 [0.2, 2.2] |
| 0.2 | 3.3 [1.3, 5.6] | 2.6 [1.1, 4.1] | 2.3 [1.0, 3.6] | 1.3 [0.2, 2.6] | 1.0 [0.2, 2.4] |
| 0.3 | 2.7 [1.2, 4.3] | 2.3 [1.0, 3.5] | 2.0 [0.7, 3.3] | 0.9 [0.2, 2.3] | 0.3 [0.1, 0.5] |
| 0.4 | 2.9 [1.5, 4.4] | 2.4 [1.3, 3.7] | 1.7 [0.5, 3.2] | 0.9 [0.1, 2.4] | 0.5 [0.2, 0.9] |
| 0.5 | 2.2 [1.0, 3.7] | 1.8 [0.5, 3.2] | 1.1 [0.2, 2.8] | 0.3 [0.1, 0.4] | 0.3 [0.1, 0.5] |

### Knight-style EM (revised rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 7.1 [3.7, 11.5] | 6.0 [3.8, 8.5] | 4.8 [2.4, 7.6] | 3.4 [1.4, 5.9] | 2.6 [1.1, 4.4] |
| 0.1 | 6.9 [3.8, 10.2] | 5.3 [2.9, 8.2] | 4.1 [2.5, 6.0] | 3.2 [1.7, 5.1] | 2.7 [1.0, 5.1] |
| 0.2 | 5.3 [3.3, 7.5] | 3.9 [2.3, 6.0] | 3.7 [2.1, 5.6] | 2.6 [1.2, 4.5] | 2.3 [1.0, 4.3] |
| 0.3 | 4.3 [2.5, 6.7] | 3.6 [2.3, 5.3] | 3.0 [1.6, 5.1] | 2.5 [0.8, 5.2] | 1.3 [0.5, 2.3] |
| 0.4 | 3.5 [2.1, 5.3] | 3.6 [2.1, 5.4] | 2.6 [1.0, 5.0] | 2.5 [0.7, 5.1] | 1.8 [0.9, 2.8] |
| 0.5 | 3.4 [1.6, 6.0] | 2.8 [1.4, 4.8] | 2.7 [0.9, 5.1] | 1.3 [0.5, 2.6] | 0.8 [0.5, 1.2] |

### Knight-style EM (original rule), none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 4.2 [1.1, 7.1] | 3.7 [1.4, 5.8] | 3.2 [1.1, 5.6] | 2.6 [0.7, 5.1] | 2.5 [0.7, 4.6] |
| 0.1 | 4.6 [2.0, 7.2] | 3.5 [1.1, 5.9] | 2.8 [0.9, 4.9] | 2.4 [0.6, 4.4] | 1.9 [0.4, 3.9] |
| 0.2 | 3.9 [1.3, 7.2] | 3.2 [1.5, 5.1] | 2.7 [0.9, 4.9] | 2.5 [0.9, 4.4] | 1.6 [0.1, 3.6] |
| 0.3 | 3.6 [1.3, 6.1] | 2.5 [0.9, 4.5] | 2.3 [0.6, 4.2] | 1.6 [0.1, 3.9] | 0.7 [0.1, 1.6] |
| 0.4 | 3.7 [1.5, 6.2] | 2.7 [0.9, 4.8] | 2.4 [0.6, 4.5] | 1.6 [0.0, 3.8] | 0.6 [0.0, 1.9] |
| 0.5 | 2.4 [0.6, 4.7] | 2.5 [0.5, 4.8] | 1.8 [0.2, 4.3] | 0.5 [0.0, 1.5] | 0.2 [0.0, 0.7] |

### EM cognate-matcher, none tier

*Inventory raised only via allographs; no tested method merges allographs.*

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 1.8 [0.6, 3.9] | 1.4 [0.5, 2.7] | 1.4 [0.6, 2.4] | 1.3 [0.6, 2.3] | 1.1 [0.3, 2.2] |
| 0.1 | 2.1 [0.7, 4.2] | 2.0 [1.0, 3.4] | 1.6 [0.8, 2.5] | 1.3 [0.5, 2.3] | 0.9 [0.2, 1.8] |
| 0.2 | 2.3 [1.2, 3.7] | 1.8 [0.8, 3.0] | 1.4 [0.4, 2.4] | 1.0 [0.4, 1.8] | 0.8 [0.2, 1.7] |
| 0.3 | 1.9 [1.1, 2.9] | 1.8 [1.0, 2.7] | 1.3 [0.5, 2.1] | 1.1 [0.2, 2.4] | 0.4 [0.1, 0.8] |
| 0.4 | 1.9 [0.7, 3.5] | 1.5 [0.5, 2.8] | 1.1 [0.3, 2.6] | 0.9 [0.1, 2.3] | 0.4 [0.1, 0.8] |
| 0.5 | 1.7 [0.6, 3.3] | 1.3 [0.4, 2.4] | 1.2 [0.2, 3.3] | 0.4 [0.1, 0.6] | 0.2 [0.1, 0.5] |

Corpora per cell:

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 29 | 38 | 45 | 50 | 52 |
| 0.1 | 29 | 42 | 53 | 56 | 52 |
| 0.2 | 39 | 51 | 56 | 53 | 51 |
| 0.3 | 44 | 56 | 54 | 51 | 48 |
| 0.4 | 47 | 56 | 51 | 51 | 48 |
| 0.5 | 54 | 54 | 51 | 48 | 45 |

## Other statistics drift (not re-calibrated), balanced panel

Only the two knobs were set. These statistics move as a side effect and are reported, not corrected.

**realized_dup**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 0.1 | 0.100 | 0.100 | 0.100 | 0.100 | 0.100 |
| 0.2 | 0.200 | 0.200 | 0.200 | 0.200 | 0.200 |
| 0.3 | 0.300 | 0.300 | 0.300 | 0.300 | 0.300 |
| 0.4 | 0.400 | 0.400 | 0.400 | 0.400 | 0.400 |
| 0.5 | 0.500 | 0.500 | 0.500 | 0.500 | 0.500 |

**realized_inventory**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 398.3 | 500.4 | 600.8 | 698.8 | 800.5 |
| 0.1 | 401.5 | 503.5 | 603.0 | 702.5 | 801.4 |
| 0.2 | 398.5 | 498.6 | 600.1 | 702.1 | 800.9 |
| 0.3 | 398.1 | 500.0 | 600.1 | 699.1 | 802.9 |
| 0.4 | 400.3 | 503.8 | 600.3 | 701.7 | 800.1 |
| 0.5 | 396.7 | 498.2 | 595.7 | 704.0 | 801.6 |

**mean_length**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 4.577 | 4.580 | 4.582 | 4.582 | 4.582 |
| 0.1 | 4.594 | 4.595 | 4.595 | 4.595 | 4.595 |
| 0.2 | 4.639 | 4.644 | 4.644 | 4.644 | 4.644 |
| 0.3 | 4.650 | 4.651 | 4.651 | 4.651 | 4.651 |
| 0.4 | 4.621 | 4.621 | 4.621 | 4.621 | 4.621 |
| 0.5 | 4.616 | 4.616 | 4.616 | 4.616 | 4.616 |

**top1_share**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.071 | 0.071 | 0.071 | 0.071 | 0.069 |
| 0.1 | 0.078 | 0.074 | 0.072 | 0.073 | 0.073 |
| 0.2 | 0.079 | 0.081 | 0.078 | 0.077 | 0.077 |
| 0.3 | 0.086 | 0.083 | 0.082 | 0.081 | 0.079 |
| 0.4 | 0.091 | 0.089 | 0.085 | 0.084 | 0.082 |
| 0.5 | 0.100 | 0.093 | 0.092 | 0.088 | 0.085 |

**hapax_fraction**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 0.122 | 0.165 | 0.199 | 0.229 | 0.259 |
| 0.1 | 0.126 | 0.173 | 0.204 | 0.231 | 0.254 |
| 0.2 | 0.131 | 0.172 | 0.200 | 0.233 | 0.255 |
| 0.3 | 0.136 | 0.171 | 0.205 | 0.228 | 0.255 |
| 0.4 | 0.145 | 0.174 | 0.204 | 0.225 | 0.248 |
| 0.5 | 0.143 | 0.170 | 0.198 | 0.225 | 0.239 |

**beginners80_signs**

| duplicates \ inventory | 400 | 500 | 600 | 700 | 800 |
|---|---|---|---|---|---|
| 0.0 | 84.2 | 104.6 | 120.5 | 136.9 | 148.1 |
| 0.1 | 90.8 | 104.3 | 121.0 | 133.2 | 143.6 |
| 0.2 | 86.3 | 102.9 | 115.9 | 129.3 | 141.7 |
| 0.3 | 84.9 | 100.1 | 113.3 | 124.0 | 136.5 |
| 0.4 | 82.4 | 98.3 | 110.1 | 121.9 | 130.5 |
| 0.5 | 79.3 | 94.1 | 104.9 | 115.0 | 124.5 |

## Per script type, revised EM, candidates tier (balanced panel)

| cell (dup, inv) | logographic | logosyllabic | syllabic |
|---|---|---|---|
| (0.0, 400) | 0.0 | 68.1 | 67.6 |
| (0.0, 600) | 0.0 | 29.4 | 44.4 |
| (0.0, 800) | 0.0 | 10.4 | 27.4 |
| (0.3, 400) | 0.0 | 33.9 | 36.2 |
| (0.3, 600) | 0.0 | 9.7 | 15.1 |
| (0.3, 800) | 0.0 | 5.1 | 6.1 |
| (0.5, 400) | 0.1 | 10.6 | 10.7 |
| (0.5, 600) | 0.0 | 6.6 | 6.7 |
| (0.5, 800) | 0.0 | 5.7 | 5.9 |

## Archaeological subsets: predicted positions (prediction, not measurement)

> **Every region in this section is a prediction, not a measurement.** No corpus of seals only, tablets only or a single period was generated or tested.

Kenoyer & Meadow (2010) report that seals are almost all unique while tablets are often copied or molded in duplicate. Kenoyer (2020b) notes that each sub-period may have used considerably fewer than 400-450 signs. The regions below are where subsets defined by object type or period would fall on the map. **Every region is an estimate**: the sources give qualitative statements and raw counts, not subset rates. See `config/indus_targets.yaml` -> `reference_points.archaeological_subsets`. The map holds N at 2,906 texts, and every subset is smaller (main size sweep, revised EM, candidates tier: 10.2% at 500 texts vs 14.6% at 2,906).

| Subset | Region on map | Basis | Revised EM, candidates (all panel, cells in region, inventory 400-700) | Same, strict panel (fixed composition) | Revised EM, no relative (all panel) |
|---|---|---|---|---|---|
| S: Seals only (low duplication): prediction, not measurement | duplicates 0.0-0.05, inventory: any | KENOYER_MEADOW2010 p. 6: seals, "almost all of which are unique". "Almost all" is placed at 0-5% duplicates; that cut-off is OUR ESTIMATE, not a published number. | 18.0-38.6% (4 cells) | 21.1-41.7% (4 cells) | 3.4-7.1% (4 cells) |
| T: Tablets only (high duplication): prediction, not measurement | duplicates 0.354-0.5, inventory: any | KENOYER_MEADOW2010 pp. 6-7: tablets have numerous copies and same-mold duplicates (22 incised copies; 31 molded duplicates in two Harappa instances). The counts have no denominators, so no rate can be computed. DERIVED LOWER BOUND: the pooled M77 rate is 0.354 (YADAV2010 Fig. 2). If seals are nearly unique, the non-seal remainder must duplicate at least as often as the pool, i.e. >= 0.354. The upper edge (0.5) is just the edge of our grid. | 4.2-17.3% (8 cells) | 2.6-15.7% (8 cells) | 1.3-3.6% (8 cells) |
| P: Single period (smaller inventory): prediction, not measurement | duplicates: any, inventory < 400 | KENOYER2020B p. 249: "considerably less" than 400-450 discrete symbols per sub-period. No number is published; the region is drawn left of 400 and is OUTSIDE the measured grid (400-800). | outside the grid (not measured) | outside the grid (not measured) | outside the grid (not measured) |

Reading (prediction, not measurement): with a relative among the candidates, the seals-only band (S) is the easiest part of the map and the tablets-only band (T) among the hardest. Without a relative, every band stays low. The single-period region (P) lies below the measured inventory range, so the map does not say how decipherable a single-period corpus would be. The gradient toward fewer signs points to easier, but that is an extrapolation and it ignores the smaller text count.

## Design choices that could make this map misleading

* **Inventory is reached only through allographs.** Other ways to add sign types (more logograms, more homophones, compound signs) would change difficulty differently. Alphabetic and syllabic corpora reach 700-800 types only with dozens of variants per value. That may be unrealistic, and it is maximally hard for solvers that do not merge variants.
* **No tested method merges allographs.** A method that clusters graphic variants first would be hurt less by large inventories. The map measures these solvers, not decipherability in general.
* **Copies follow plaintext popularity.** Real duplicates (for example moulded tablets) may cluster differently.
* **Sign-list sizes are catalogue sizes**, not types observed in 2,906 texts. Only M77 (417) is like-for-like. M77's 0.354 duplicate rate is computed on the 2,591 texts plotted in Yadav et al. (2010), Fig. 2.
* **Other targets are not re-fit per cell** (see the drift tables), so a cell's difficulty mixes the direct effect of the knob with these side effects.

## References

* **M77**: Mahadevan, I. (1977). The Indus Script: Texts, Concordance and Tables. Memoirs of the Archaeological Survey of India 77. New Delhi.
* **YADAV2010**: Yadav, N., Joglekar, H., Rao, R. P. N., Vahia, M. N., Adhikari, R., Mahadevan, I. (2010). Statistical analysis of the Indus script using n-grams. PLoS ONE. arXiv:0901.3017.
* **NAIR2026**: Nair, A. (2026). How Non-Linguistic Is the Indus Sign System? A Synthetic-Baseline Scorecard. arXiv:2604.17828v1, 20 Apr 2026 (preprint, not peer reviewed; only version as of 2026-10-05). Corpus: ICIT as extracted from the "Yajnadevam digital corpus" (1,916 deduplicated inscriptions, 52 sites). AVAILABILITY (checked 2026-10-05): the abstract says "All code and data are publicly available", but the arXiv comment ("Code available from corresponding author upon request") and the paper body ("available from the corresponding author ... upon request and will be released as a public repository upon acceptance") say on request only. No public repository and no licence found. Whether the data carry object-type or period tags is therefore unknown; the paper describes the corpus as mostly seals, tablets and pottery from 52 sites but does not say the released data include those tags.
* **PARPOLA1994**: Parpola, A. (1994). Deciphering the Indus Script. Cambridge University Press. (386 signs read VIA RAO2018.)
* **RAO2018**: Rao, R. P. N. (2018). The Indus script and economics. In: Walking with the Unicorn (Kenoyer felicitation volume), Archaeopress, pp. 518-525. arXiv:1812.00049.
* **WELLS2006**: Wells, B. K. (2006). Epigraphic Approaches to Indus Writing. PhD thesis, Harvard University. (676 signs read VIA YADAV2010, ref. [4].)
* **WELLS2015**: Wells, B. K. (2015). The Archaeology and Epigraphy of Indus Writing. Oxford: Archaeopress. (Bibliographic entry as given in RAO2018; 694 signs read VIA RAO2018 and VIA the English Wikipedia article "Indus script", accessed 2026-10-03.)
* **FULS2023**: Fuls, A. (2023). A Catalog of Indus Signs. Self-published (ISBN 9798398422306). ("More than 700 distinct signs" read only in the book's publisher/retailer description via a web search summary, 2026-10-03; exact count NOT verified.)
* **KENOYER_MEADOW2010**: Kenoyer, J. M. & Meadow, R. H. (2010). Inscribed objects from Harappa excavations 1986-2007. In: A. Parpola, B. M. Pande & P. Koskikallio (eds.), Corpus of Indus Seals and Inscriptions, Vol. 3: New material, untraced objects, and collections outside India and Pakistan, Part 1: Mohenjo-daro and Harappa (Annales Academiae Scientiarum Fennicae, Humaniora 359; Memoirs of the Archaeological Survey of India 96). Helsinki: Suomalainen Tiedeakatemia. Introductory essay, pp. xliv-lviii (front-matter pages as listed by harappa.com via a search result; the PDF we read is paginated 1-15 and the page numbers we quote refer to that PDF). READ IN FULL by us from a PDF supplied by the project owner, 2026-10-04.
* **KENOYER2020A**: Kenoyer, J. M. (2020). The origin and development of the Indus script: insights from Harappa and other sites. In: K. Lashari (ed.), Studies on Indus Script. Karachi: National Fund for Mohenjodaro, pp. 217-236. READ by us (PDF supplied by the project owner, 2026-10-04).
* **KENOYER2020B**: Kenoyer, J. M. (2020, in press at the time of the PDF). The Indus script: origins, use and disappearance. In: H. Zhao (ed.), Dialogue of Civilisation: Comparing Multiple Centers. Shanghai: Shanghai Guji Press, pp. 220-255. READ by us (same PDF as KENOYER2020A, second article). Page numbers we quote are the printed numbers in that PDF (237-...), which may not match the final published pagination.
* **MEADOW_KENOYER2000**: Meadow, R. H. & Kenoyer, J. M. (2000). The "tiny steatite seals" (incised steatite tablets) of Harappa: some observations on their context and dating. In: M. Taddei & G. De Marco (eds.), South Asian Archaeology 1997 (Serie Orientale Roma 90), pp. 321-340. Rome: IsIAO / Naples: IUO. (Entry as given in KENOYER_MEADOW2010 and RAO2018; NOT read by us.)
* **KENOYER_PC2026**: J. M. Kenoyer (UW-Madison), comments relayed by the project owner, 2026-10-04. Used only where the published papers above say the same thing.
