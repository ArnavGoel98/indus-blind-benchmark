**Pre-registered success criterion: FAILED (33.9% < 50% of tokens; frozen EM original rule, `related` tier, natural texts).** It also fails in every other condition and tier.

# v2 rank 2: Ugaritic-Hebrew real-relative anchor — results

Plan pre-registered in `docs/v2_ugaritic_plan.md` (pushed b05772d; amendment committed before the run).
Methods frozen-v1, unchanged. Not in the v1 paper.

## Sources

- EUPT, version Draft 3.2 [2025-07-18], accessed 2026-10-09, CC BY-SA 4.0:
  - https://eupt.uni-goettingen.de/api/eupt/html/KTU_1.14_facsimile.html (SHA-256 ad851529e956ae5c…)
  - https://eupt.uni-goettingen.de/api/eupt/html/KTU_1.15_facsimile.html (SHA-256 48a0eca1ded4ce4b…)
  - https://eupt.uni-goettingen.de/api/eupt/html/KTU_1.16_facsimile.html (SHA-256 d6e6d6b80edec566…)
- OSHB (WLC 4.20), commit 3d15126fb1ef74867fc1434be1942e837932691f, CC BY 4.0 (WLC public domain). Original work of the Open Scriptures Hebrew Bible available at https://github.com/openscriptures/morphhb
- Gold: Wikipedia 'Ugaritic alphabet' letters table (read 2026-10-09), citing Kogan 2011 Tab. 6.2 (not read).

**Gold table status: SECONDARY SOURCE, not yet verified against an academic source we have read.** The table is Wikipedia's; its cited source, Kogan (2011), has not been read. Search for an openly accessible academic source (2026-10-09):
- Partly corroborated by P. Merlo, "Ugaritic", *Mnamon: Ancient writing systems in the Mediterranean*, Scuola Normale Superiore (DOI 10.25429/sns.it/lettere/mnamon000), read 2026-10-09: ṯ and š merged into Hebrew š, ʿ and ġ into ʿ, and ẓ is written ṣ in Hebrew in the word for "summer" (one example). It does not cover ḫ/ḥ, ḏ/z or the three aleph signs.
- Segert (1984), *A Basic Grammar of the Ugaritic Language* (UC Press): no openly licensed copy found (publisher and JSTOR access restricted; an Internet Archive scan of unclear legal status was not used).
- Gianto, "Ugaritic" (ResearchGate full text): not accessible (HTTP 403).
Until a read source covers ḫ/ḥ, ḏ/z and the alephs, all Task D numbers carry this caveat.

## Corpora

| Condition | Texts | Tokens | Letters | Mean length | Duplicate rate | One-to-one ceiling (letters) |
|---|---|---|---|---|---|---|
| natural | 791 | 6928 | 5876 | 8.76 | 0.102 | 90.6% |
| lines | 678 | 6928 | 5876 | 10.22 | 0.049 | 90.6% |
| recut4.6/s0 | 1451 | 6693 | 5876 | 4.61 | 0.276 | 90.6% |
| recut4.6/s1 | 1462 | 6702 | 5876 | 4.58 | 0.295 | 90.6% |
| recut4.6/s2 | 1448 | 6709 | 5876 | 4.63 | 0.277 | 90.6% |

References: hebrew 1,197,042 units (22 types); hebrew-poetic 137,202 units (22 types); sanskrit 872,338 units (47 types); tamil 502,785 units (34 types); sumerian 415,308 units (262 types); latin 118,647 units (29 types); finnish 222,028 units (24 types).

## Task D: sign values

Token accuracy, %, v1 convention (every token; word dividers count and are unrecoverable) / letters only / letters without ỉ and ủ. Letter types right out of 29. Pre-registered success: token accuracy >= 50%.

### `related`

| Condition | Frequency rank | EM, original rule (primary) | EM, revised rule |
|---|---|---|---|
| natural | 2.3 / 2.7 / 2.8; 1/29; ref hebrew | 33.9 / 40.0 / 41.3; 11/29; ref hebrew | 32.0 / 37.8 / 39.0; 9/29; ref hebrew |
| lines | 2.3 / 2.7 / 2.8; 1/29; ref hebrew | 32.5 / 38.4 / 39.7; 10/29; ref hebrew | 29.7 / 35.0 / 36.2; 8/29; ref hebrew |
| recut4.6/s0 | 2.4 / 2.7 / 2.8; 1/29; ref hebrew | 30.6 / 34.9 / 36.0; 10/29; ref hebrew | 26.8 / 30.5 / 31.6; 8/29; ref hebrew |
| recut4.6/s1 | 2.4 / 2.7 / 2.8; 1/29; ref hebrew | 36.8 / 42.0 / 43.4; 11/29; ref hebrew | 29.9 / 34.1 / 35.2; 9/29; ref hebrew |
| recut4.6/s2 | 2.4 / 2.7 / 2.8; 1/29; ref hebrew | 27.2 / 31.1 / 32.1; 9/29; ref hebrew | 24.6 / 28.1 / 29.0; 7/29; ref hebrew |

### `related_poetic`

| Condition | Frequency rank | EM, original rule (primary) | EM, revised rule |
|---|---|---|---|
| natural | 13.4 / 15.8 / 16.3; 3/29; ref hebrew-poetic | 39.4 / 46.5 / 48.0; 13/29; ref hebrew-poetic | 37.2 / 43.8 / 45.3; 10/29; ref hebrew-poetic |
| lines | 13.4 / 15.8 / 16.3; 3/29; ref hebrew-poetic | 40.4 / 47.7 / 49.2; 13/29; ref hebrew-poetic | 39.3 / 46.4 / 47.9; 11/29; ref hebrew-poetic |
| recut4.6/s0 | 13.8 / 15.8 / 16.3; 3/29; ref hebrew-poetic | 45.4 / 51.7 / 53.5; 11/29; ref hebrew-poetic | 43.0 / 49.0 / 50.6; 10/29; ref hebrew-poetic |
| recut4.6/s1 | 13.8 / 15.8 / 16.3; 3/29; ref hebrew-poetic | 39.6 / 45.2 / 46.7; 13/29; ref hebrew-poetic | 38.4 / 43.8 / 45.3; 12/29; ref hebrew-poetic |
| recut4.6/s2 | 13.8 / 15.8 / 16.3; 3/29; ref hebrew-poetic | 41.6 / 47.5 / 49.1; 11/29; ref hebrew-poetic | 40.5 / 46.2 / 47.7; 10/29; ref hebrew-poetic |

### `candidates`

| Condition | Frequency rank | EM, original rule (primary) | EM, revised rule |
|---|---|---|---|
| natural | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 32.0 / 37.8 / 39.0; 9/29; ref hebrew |
| lines | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 29.7 / 35.0 / 36.2; 8/29; ref hebrew |
| recut4.6/s0 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 26.8 / 30.5 / 31.6; 8/29; ref hebrew |
| recut4.6/s1 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 29.9 / 34.1 / 35.2; 9/29; ref hebrew |
| recut4.6/s2 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 24.6 / 28.1 / 29.0; 7/29; ref hebrew |

### `none`

| Condition | Frequency rank | EM, original rule (primary) | EM, revised rule |
|---|---|---|---|
| natural | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 0.0 / 0.0 / 0.0; 0/29; ref latin |
| lines | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 0.0 / 0.0 / 0.0; 0/29; ref latin |
| recut4.6/s0 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 0.0 / 0.0 / 0.0; 0/29; ref latin |
| recut4.6/s1 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 0.0 / 0.0 / 0.0; 0/29; ref latin |
| recut4.6/s2 | 0.0 / 0.0 / 0.0; 0/29; ref tamil | 0.0 / 0.0 / 0.0; 0/29; ref sumerian | 0.0 / 0.0 / 0.0; 0/29; ref latin |

Re-cut seeds, EM original, `related`: 30.6, 36.8, 27.2 (mean 31.5).

EM restart seed (natural, `related`; primary uses seed 0): knight2006_em_original/seed1 33.9; knight2006_em_original/seed2 33.9; knight2006_em/seed1 32.0; knight2006_em/seed2 32.0.

Letters right, natural, `related`, EM original: k l n p q r s w ḥ ṣ ṭ.

## Task C: language family (`candidates`: Hebrew + 5 v1 languages; chance 1/6)

| Condition | Frequency rank | EM, original rule (primary) | EM, revised rule |
|---|---|---|---|
| natural | tamil | sumerian | hebrew |
| lines | tamil | sumerian | hebrew |
| recut4.6/s0 | tamil | sumerian | hebrew |
| recut4.6/s1 | tamil | sumerian | hebrew |
| recut4.6/s2 | tamil | sumerian | hebrew |

## Tasks A and B (frozen rules, fit on v1 run records as for Sproat's corpora)

Task A is a check only (pre-registered as weak evidence). Real Ugaritic is called "not language" by 3-4 of the 5 frozen rules in every condition. **Training-distribution caveat:** the rules were fit on synthetic corpora with 400+ signs calibrated to Indus statistics; a 30-sign alphabet lies far outside that range, so this shows the rules do not transfer to small alphabets, not that the methods judge Ugaritic non-linguistic in any wider sense.

### `full/full`

| Condition | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio | Task B (inventory / LR / branching) |
|---|---|---|---|---|---|---|---|
| natural | not | not | not | language | language | 0.855 | alphabetic / alphabetic / syllabic |
| lines | not | not | not | language | language | 0.860 | alphabetic / alphabetic / syllabic |
| recut4.6/s0 | not | not | not | language | language | 0.851 | alphabetic / alphabetic / logographic |
| recut4.6/s1 | not | not | not | language | language | 0.848 | alphabetic / alphabetic / logographic |
| recut4.6/s2 | not | not | not | language | language | 0.849 | alphabetic / alphabetic / logographic |

### `full/holdout`

| Condition | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio | Task B (inventory / LR / branching) |
|---|---|---|---|---|---|---|---|
| natural | not | not | not | language | not | 0.855 | alphabetic / alphabetic / syllabic |
| lines | not | not | not | language | not | 0.860 | alphabetic / alphabetic / syllabic |
| recut4.6/s0 | not | not | not | language | not | 0.851 | alphabetic / alphabetic / logosyllabic |
| recut4.6/s1 | not | not | not | language | not | 0.848 | alphabetic / alphabetic / logosyllabic |
| recut4.6/s2 | not | not | not | language | not | 0.849 | alphabetic / alphabetic / logosyllabic |

### `replication/full`

| Condition | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio | Task B (inventory / LR / branching) |
|---|---|---|---|---|---|---|---|
| natural | not | not | not | language | language | 0.855 | alphabetic / alphabetic / syllabic |
| lines | not | not | not | language | language | 0.860 | alphabetic / alphabetic / syllabic |
| recut4.6/s0 | not | not | not | language | language | 0.851 | alphabetic / alphabetic / logographic |
| recut4.6/s1 | not | not | not | language | language | 0.848 | alphabetic / alphabetic / logographic |
| recut4.6/s2 | not | not | not | language | language | 0.849 | alphabetic / alphabetic / logographic |

### `replication/holdout`

| Condition | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio | Task B (inventory / LR / branching) |
|---|---|---|---|---|---|---|---|
| natural | not | not | not | language | not | 0.855 | alphabetic / alphabetic / syllabic |
| lines | not | not | not | language | not | 0.860 | alphabetic / alphabetic / syllabic |
| recut4.6/s0 | not | not | not | language | not | 0.851 | alphabetic / alphabetic / logosyllabic |
| recut4.6/s1 | not | not | not | language | not | 0.848 | alphabetic / alphabetic / logosyllabic |
| recut4.6/s2 | not | not | not | language | not | 0.849 | alphabetic / alphabetic / logographic |

## Distance yardsticks: real relative vs synthetic sister

| Measure | Ugaritic-Hebrew | Chance / floor | v1 sister (Sanskrit / Tamil / Sumerian / Latin / Finnish) |
|---|---|---|---|
| Sound mergers | 7 | - | 0 (bijective) |
| Texts found verbatim in the reference, natural texts, % | 30.8 | 23.9 (shuffled map) | see note |
| ... texts of 6+ letters, % | 0.8 | 0.1 | |
| ... re-cut to 4.6, % | 66.1 | 55.3 | |
| Cognate-form overlap, word types, % (576 types, 977 tokens) | 54.9 | 15.1 (95th pct 19.1) | 75.3 / 58.0 / 73.1 / 52.2 / 54.3 (chance 0.1 / 0.3 / 10.5 / 0.5 / 0.1) |
| ... word tokens, % | 63.7 | 19.3 | 77.4 / 60.2 / 80.0 / 57.6 / 60.1 (chance 0.1 / 0.4 / 19.7 / 1.0 / 0.2) |
| Letter-bigram JSD, bits | 0.184 (poetic ref 0.185) | 0.018 (same-size Hebrew sample vs Hebrew); shuffled map 0.475 | 0.035 / 0.024 / 0.087 / 0.022 / 0.014 (size-matched) |

v1 sister cognate overlap is measured on samples of the same number of word tokens as the Ugaritic text (20 draws), hidden half vs sister half, alphabetic units.

## Exploratory comparison (NOT pre-registered)

Added after the results were seen. The v1 alphabetic corpora at the Indus point, `related` tier, frozen EM original rule, before the cognate step, score 38.9% (sampler A, 15 corpora) and 57.8% (sampler B); they have about 320-340 signs (allographs, homophones) and twice the tokens, but a synthetic sister reference. Ugaritic (30 signs, real relative, half the tokens) scores 33.9%. One reading: a real relative costs roughly what v1's inventory and duplication cost. This is not a controlled comparison (sign inventory, size, script and reference all differ) and is not a test of any pre-registered hypothesis.

