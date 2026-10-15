# Rank 6b: Ugaritic-Hebrew yardsticks on real related languages (pre-registration entry 5)

No tuning, no targets. Shared code (`src/ibdb/yardsticks.py`); sample sizes matched to the anchor. Normalised spelling is primary. Every pair is labelled sister or descendant.

| Pair | Relationship | Spelling | JSD above floor (bits) | Shared word forms, chance-corr. | Word pairs, chance-corr. | Verbatim 6+ units | Mergers |
|---|---|---|---|---|---|---|---|
| Ugaritic-Hebrew | sister | as written | 0.166 | 46.8% | 1.5% | 0.8% | 7 |
| Ugaritic-Hebrew | sister | vowel letters removed | 0.089 | 58.4% | 4.6% | 0.8% | 7 |
| **Latin-Italian** | descendant | as written | 0.117 | 11.8% | 0.6% | 1.9% | 9 (+ h deleted) |
| **Latin-Italian** | descendant | normalised (primary) | 0.104 | 11.8% | 0.6% | 1.9% | 9 (+ h deleted) |
| Latin, v1-like sister (upper bound) | synthetic | - | 0.006 | 53.1% | 7.1% | 12.4% | 0 |
| Latin, `harsh` (lower bound) | synthetic | - | 0.135 | 7.8% | 1.1% | 2.4% | 5 |

**Latin-Italian, bootstrap over Dante lines (normalised; 200 replicates, 5 draws each):**

| Yardstick | Point (20 draws) | Bootstrap mean | 95% interval | SD |
|---|---|---|---|---|
| jsd_above_floor | 0.104 | 0.104 | 0.101-0.108 | 0.002 |
| cognate_types_cc | 11.8% | 10.6% | 9.6%-11.5% | 0.5% |
| word_pairs_types_cc | 0.6% | 0.4% | 0.1%-0.7% | 0.2% |
| verbatim_6plus | 1.9% | 1.9% | 0.7%-3.3% | 0.7% |

Sizes: Dante 14,233 lines, 101,601 words, 391,950 units; hidden side = v1 Latin hidden half.
Gold: Grandgent (1907), section per row in `src/ibdb/data/relatives.py`. Mergers: 9; deleted: h.

**Not measured yet:**

- finnish-estonian (sister): gold source (Pajusalu 2012) not reachable from this environment
- tamil-malayalam (descendant), tamil-kannada (sister): awaiting Wikisource provenance check
- sanskrit-pali (descendant): licence unresolved; public-domain fallback being searched

