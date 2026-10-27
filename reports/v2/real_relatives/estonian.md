# Finnish-Estonian yardsticks (pre-registration entries 9 and 10)

Same code and settings as `yardsticks.md` (entry 5). Normalised spelling is primary. **Gold: weak (10 word pairs, 13 of 27 letters)**, built from the Finnish-North Estonian word pairs printed in Pajusalu (2012); 13 of 27 rows have a regular reflex, the rest are "no source" (12.6% of the hidden Finnish letters), treated as unknown, not lost (entry 10). Both sides are written in alphabets that write vowels, so the comparison with Latin-Italian is within one script type; the comparison with Ugaritic-Hebrew is indicative only.

| Pair | Relationship | Spelling | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Mergers |
|---|---|---|---|---|---|---|---|
| Ugaritic-Hebrew (as written) | sister | - | 0.166 | 46.8% | 1.5% | 0.8% | 7 |
| **finnish-estonian** (weak gold: 10 word pairs, 13 of 27 letters) | sister | as written | 0.240 | 7.9% | 0.5% | 1.0% | 0 |
| **finnish-estonian** (weak gold: 10 word pairs, 13 of 27 letters) | sister | normalised (primary) | 0.183 | 10.6% | 0.6% | 1.3% | 0 |
| finnish, v1-like sister (synthetic, optimistic upper reference) | synthetic | - | 0.004 | 53.9% | 10.4% | 19.8% | 0 |
| finnish, `harsh` (synthetic, optimistic upper reference) | synthetic | - | 0.154 | 4.8% | 0.2% | 3.5% | 24% of consonants |

**Bootstrap over Kalevipoeg's lines (normalised; 200 replicates, 5 draws each): point / bootstrap mean / 95% interval**

| jsd_above_floor | cognate_types_cc | word_pairs_types_cc | verbatim_6plus |
|---|---|---|---|
| 0.183 / 0.182 / 0.178-0.186 | 10.6% / 9.8% / 8.9%-10.7% | 0.6% / 0.6% / 0.4%-0.9% | 1.3% / 2.4% / 1.0%-4.4% |

**Size (normalised):** 18,664 lines, 58,926 words, 369,658 units. No-source rows: b, c, d, f, g, j, p, v, y, z, ä, ö, š, ž.

## Verbatim overlap (entry-5 procedure)

Windows of 6+ hidden Finnish letters mapped through the gold that occur verbatim in Kalevipoeg: **3.1%** of 6,074 windows (shuffled-map chance: mean 0.2%, 95th percentile 0.4%; an unrelated language, Latin, in letters: 0.3%). By class: across boundaries 129, within words 57, word 2; spanning 2+ whole words: 0.

Kreutzwald modelled Kalevipoeg on the Kalevala, so shared formulas are possible. The hits spanning several whole words, most often hit first:

- none
