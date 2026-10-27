# Finnish-Estonian yardsticks (pre-registration entry 9)

Same code and settings as `yardsticks.md` (entry 5). Normalised spelling is primary. Gold: built from the Finnish-North Estonian word pairs printed in Pajusalu (2012); 13 of 27 rows have a regular reflex, the rest are "no source" (12.6% of the hidden Finnish letters). Both sides are written in alphabets that write vowels, so the comparison with Latin-Italian is within one script type; the comparison with Ugaritic-Hebrew is indicative only.

| Pair | Relationship | Spelling | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Mergers |
|---|---|---|---|---|---|---|---|
| Ugaritic-Hebrew (as written) | sister | - | 0.166 | 46.8% | 1.5% | 0.8% | 7 |
| **finnish-estonian** | sister | as written | 0.241 | -9.8% | -1.8% | 0.8% | 0 |
| **finnish-estonian** | sister | normalised (primary) | 0.184 | -7.9% | -1.8% | 1.4% | 0 |
| finnish, v1-like sister (upper bound) | synthetic | - | 0.004 | 53.9% | 10.4% | 19.8% | 0 |
| finnish, `harsh` (lower bound) | synthetic | - | 0.154 | 4.8% | 0.2% | 3.5% | 24% of consonants |

**Bootstrap over Kalevipoeg's lines (normalised; 200 replicates, 5 draws each): point / bootstrap mean / 95% interval**

| jsd_above_floor | cognate_types_cc | word_pairs_types_cc | verbatim_6plus |
|---|---|---|---|
| 0.184 / 0.184 / 0.180-0.189 | -7.9% / -8.4% / -16.2%--1.3% | -1.8% / -1.6% / -3.2%--0.4% | 1.4% / 1.0% / 0.2%-1.8% |

**Size (normalised):** 18,664 lines, 58,926 words, 369,658 units. "No reflex" in the merger column counts no-source rows.

## Verbatim overlap (entry-5 procedure)

Windows of 6+ hidden Finnish letters mapped through the gold that occur verbatim in Kalevipoeg: **1.2%** of 10,041 windows (shuffled-map chance: mean 0.2%, 95th percentile 0.6%; an unrelated language, Latin, in letters: 0.3%). By class: across boundaries 84, within words 32; spanning 2+ whole words: 0.

Kreutzwald modelled Kalevipoeg on the Kalevala, so shared formulas are possible. The hits spanning several whole words, most often hit first:

- none
