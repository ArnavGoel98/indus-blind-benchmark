# v2 rank 6: sister-v4 calibration — yardstick table (dev seeds 90-91; held-out 0-2)

**Result: no language matches the pre-declared targets in either setting.** The selection rule picked the
closest grid point that keeps verbatim text at or below 2%; all are marked "not matched". Sumerian has no grid
point at or below 2% verbatim. No Task C or D score has been computed with sister-v4.

## Targets (Ugaritic-Hebrew, shared code)

| Yardstick | Ugaritic-Hebrew | `close` target (accept) | `distant` target (accept) |
|---|---|---|---|
| JSD above floor (bits) | 0.166 | 0.166 (0.126 to 0.206) | 0.332 (0.272 to 0.392) |
| Shared word forms, chance-corr. | 46.8% | 46.8% (36.8% to 56.8%) | 23.4% (13.4% to 33.4%) |
| Word pairs, chance-corr. | 1.5% | 1.5% (-8.5% to 11.5%) | 0.7% (-9.3% to 10.7%) |
| Verbatim 6+ letters | 0.8% | <= 2% | <= 2% |
| Mergers | 7 of 29 | 24% of consonants | 24% of consonants |

## `close`: chosen settings (closest grid point; mean of 20 draws)

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, chance-corr. | Word pairs, chance-corr. | Verbatim 6+ units | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 90-91 | 0.225 | 3.5% | 0.4% | 2.5% | no |
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 0-2 (held out) | 0.216 | 5.3% | 0.2% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 90-91 | 0.187 | 3.0% | 0.1% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 0-2 (held out) | 0.185 | 3.6% | 0.1% | 1.8% | no |
| sumerian | none (no grid point with verbatim <= 2%) | | - | - | - | - | no |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 90-91 | 0.158 | 6.3% | 1.1% | 2.1% | no |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 0-2 (held out) | 0.135 | 7.8% | 1.1% | 2.4% | no |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 90-91 | 0.163 | 4.1% | 0.2% | 2.1% | no |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 0-2 (held out) | 0.154 | 4.8% | 0.2% | 3.5% | no |

## `distant`: chosen settings (closest grid point; mean of 20 draws)

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, chance-corr. | Word pairs, chance-corr. | Verbatim 6+ units | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 12 / 1.0 / 0.5 / 0.5 / 0 | 90-91 | 0.276 | 1.7% | 0.3% | 2.1% | no |
| sanskrit | 12 / 1.0 / 0.5 / 0.5 / 0 | 0-2 (held out) | 0.276 | 1.5% | 0.0% | 1.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0 | 90-91 | 0.194 | 2.7% | 0.1% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0 | 0-2 (held out) | 0.189 | 3.0% | 0.1% | 2.0% | no |
| sumerian | none (no grid point with verbatim <= 2%) | | - | - | - | - | no |
| latin | 6 / 1.0 / 0.5 / 0 / 0 | 90-91 | 0.208 | 3.6% | 0.4% | 1.4% | no |
| latin | 6 / 1.0 / 0.5 / 0 / 0 | 0-2 (held out) | 0.197 | 3.3% | 0.2% | 1.3% | no |
| finnish | 9 / 0.75 / 0.1 / 0 / 0 | 90-91 | 0.199 | 2.9% | 0.3% | 1.8% | no |
| finnish | 9 / 0.75 / 0.1 / 0 / 0 | 0-2 (held out) | 0.198 | 3.0% | 0.5% | 2.5% | no |

## v1-like sister, same code (shift + 20% lexical replacement, no mergers; held-out seeds 0-2)

| Language | JSD above floor (bits) | Shared word forms, chance-corr. | Word pairs, chance-corr. | Verbatim 6+ units |
|---|---|---|---|---|
| sanskrit | 0.004 | 76.1% | 29.2% | 38.4% |
| tamil | 0.002 | 57.6% | 8.5% | 17.8% |
| sumerian | 0.030 | 69.5% | 39.1% | 35.1% |
| latin | 0.006 | 53.1% | 7.1% | 12.4% |
| finnish | 0.004 | 53.9% | 10.4% | 19.8% |

## Why nothing matches: the trade-off over the whole grid (1,080 settings, dev means)

Best chance-corrected shared word forms reachable at a given letter-pair distance:

| Language | JSD >= 0.090 | JSD >= 0.126 | JSD >= 0.166 | ... and verbatim <= 2% (JSD >= 0.126) | Lowest verbatim with forms >= 37% |
|---|---|---|---|---|---|
| sanskrit | 38.6% | 27.5% | 13.3% | 3.3% | 14.5% |
| tamil | 26.7% | 9.2% | 3.4% | 2.6% | 8.4% |
| sumerian | 45.0% | 21.5% | 7.5% | none | 12.6% |
| latin | 21.4% | 10.9% | 6.2% | 6.6% | 8.8% |
| finnish | 18.0% | 13.3% | 6.0% | 4.1% | 9.2% |

