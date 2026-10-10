**Original calibration FAILED: no language matched the pre-declared targets (sister plan) in either setting; Sumerian had no grid point at or below 2% verbatim.** Details in the last sections.

**Corrected calibration (pre-registration entry 3, post hoc) also FAILED: 0/5 languages matched in `close` or `distant`; Sumerian again had no grid point at or below 2% verbatim.** For Sanskrit and Finnish the closest `close` and `distant` settings are the same grid point, so the two corrected tiers are not distinct.

# v2 rank 6: sister-v4 yardsticks — original and corrected calibration

No Task C or D score has been computed with sister-v4.

## Corrected targets (pre-registration entry 3, POST HOC: Hebrew vowel letters removed)

Ugaritic-Hebrew, shared code, the entry-3 method. Full table with bootstrap and rule variants: `anchor_corrected.md`.

| Setting | JSD above floor | Shared word forms, cc | Word pairs, cc | Verbatim max |
|---|---|---|---|---|
| `close` | 0.089 +/- 0.040 | 58.4% +/- 10.0% | 4.6% +/- 10.0% | 2.0% |
| `distant` | 0.178 +/- 0.060 | 29.2% +/- 10.0% | 2.3% +/- 10.0% | 2.0% |

Split: contiguous blocks per language (`block_test.md`): sanskrit block4000, tamil block4000, sumerian block4000, latin block1000, finnish block1000. Blocks do not remove shared formulaic text (recorded limitation).

## Corrected `close`: chosen settings (0/5 languages matched; mean of 20 draws)

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 4 / 0.75 / 0.1 / 0 / 0.3 | 90-91 | 0.214 | 4.3% | 0.7% | 3.3% | no |
| sanskrit | 4 / 0.75 / 0.1 / 0 / 0.3 | 0-2 held out | 0.192 | 6.6% | 0.6% | 4.3% | no |
| tamil | 9 / 0.75 / 0.1 / 0.5 / 0.6 | 90-91 | 0.165 | 3.5% | 0.1% | 2.4% | no |
| tamil | 9 / 0.75 / 0.1 / 0.5 / 0.6 | 0-2 held out | 0.139 | 6.7% | 0.1% | 2.7% | no |
| sumerian | no grid point with verbatim <= 2% | | - | - | - | - | no |
| latin | 0 / 0.5 / 0.1 / 1.0 / 0.3 | 90-91 | 0.128 | 9.1% | 1.5% | 1.7% | no |
| latin | 0 / 0.5 / 0.1 / 1.0 / 0.3 | 0-2 held out | 0.118 | 12.4% | 1.7% | 4.1% | no |
| finnish | 2 / 0.75 / 0.1 / 1.0 / 0 | 90-91 | 0.151 | 6.7% | 0.5% | 2.9% | no |
| finnish | 2 / 0.75 / 0.1 / 1.0 / 0 | 0-2 held out | 0.153 | 4.4% | 0.4% | 3.2% | no |

## Corrected `distant`: chosen settings (0/5 languages matched; mean of 20 draws)

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 4 / 0.75 / 0.1 / 0 / 0.3 | 90-91 | 0.214 | 4.3% | 0.7% | 3.3% | no |
| sanskrit | 4 / 0.75 / 0.1 / 0 / 0.3 | 0-2 held out | 0.192 | 6.6% | 0.6% | 4.3% | no |
| tamil | 12 / 0.75 / 0.1 / 0.5 / 0.3 | 90-91 | 0.169 | 3.5% | 0.1% | 2.4% | no |
| tamil | 12 / 0.75 / 0.1 / 0.5 / 0.3 | 0-2 held out | 0.143 | 6.6% | 0.1% | 2.8% | no |
| sumerian | no grid point with verbatim <= 2% | | - | - | - | - | no |
| latin | 0 / 0.5 / 0.2 / 0 / 0 | 90-91 | 0.131 | 9.1% | 1.5% | 2.7% | no |
| latin | 0 / 0.5 / 0.2 / 0 / 0 | 0-2 held out | 0.123 | 12.8% | 1.7% | 4.5% | no |
| finnish | 2 / 0.75 / 0.1 / 1.0 / 0 | 90-91 | 0.151 | 6.7% | 0.5% | 2.9% | no |
| finnish | 2 / 0.75 / 0.1 / 1.0 / 0 | 0-2 held out | 0.153 | 4.4% | 0.4% | 3.2% | no |

## `harsh` tier (lower bound): settings chosen against the original targets, original content split

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 90-91 | 0.225 | 3.5% | 0.4% | 2.5% | harsh (original close) |
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 0-2 held out | 0.216 | 5.3% | 0.2% | 2.9% | harsh (original close) |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 90-91 | 0.187 | 3.0% | 0.1% | 2.9% | harsh (original close) |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 0-2 held out | 0.185 | 3.6% | 0.1% | 1.8% | harsh (original close) |
| sumerian | 12 / 1.0 / 0.35 / 1.0 / 0.6 | 90-91 | 0.169 | 6.6% | 3.5% | 3.2% | harsh (lowest verbatim, 2.8% on dev grid) |
| sumerian | 12 / 1.0 / 0.35 / 1.0 / 0.6 | 0-2 held out | 0.154 | 8.0% | 3.1% | 2.3% | harsh (lowest verbatim, 2.8% on dev grid) |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 90-91 | 0.158 | 6.3% | 1.1% | 2.1% | harsh (original close) |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 0-2 held out | 0.135 | 7.8% | 1.1% | 2.4% | harsh (original close) |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 90-91 | 0.163 | 4.1% | 0.2% | 2.1% | harsh (original close) |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 0-2 held out | 0.154 | 4.8% | 0.2% | 3.5% | harsh (original close) |

## The three tiers side by side (held-out seeds 0-2)

| Language | harsh: JSD / forms / pairs / verbatim | close: JSD / forms / pairs / verbatim | distant: JSD / forms / pairs / verbatim |
|---|---|---|---|
| sanskrit | 0.216 / 5.3% / 0.2% / 2.9% | 0.192 / 6.6% / 0.6% / 4.3% | 0.192 / 6.6% / 0.6% / 4.3% |
| tamil | 0.185 / 3.6% / 0.1% / 1.8% | 0.139 / 6.7% / 0.1% / 2.7% | 0.143 / 6.6% / 0.1% / 2.8% |
| sumerian | 0.154 / 8.0% / 3.1% / 2.3% | - | - |
| latin | 0.135 / 7.8% / 1.1% / 2.4% | 0.118 / 12.4% / 1.7% / 4.1% | 0.123 / 12.8% / 1.7% / 4.5% |
| finnish | 0.154 / 4.8% / 0.2% / 3.5% | 0.153 / 4.4% / 0.4% / 3.2% | 0.153 / 4.4% / 0.4% / 3.2% |

## v1-like sister, same code (held-out seeds 0-2): content split / block split

| Language | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ |
|---|---|---|---|---|
| sanskrit | 0.004 / 0.008 | 76.1% / 66.7% | 29.2% / 14.9% | 38.4% / 25.2% |
| tamil | 0.002 / 0.007 | 57.6% / 55.1% | 8.5% / 4.8% | 17.8% / 14.8% |
| sumerian | 0.030 / 0.029 | 69.5% / 69.3% | 39.1% / 39.3% | 35.1% / 39.1% |
| latin | 0.006 / 0.009 | 53.1% / 47.6% | 7.1% / 6.2% | 12.4% / 10.5% |
| finnish | 0.004 / 0.004 | 53.9% / 51.1% | 10.4% / 12.4% | 19.8% / 19.0% |

## Trade-off over the corrected grid (1,080 settings, dev means)

Best shared word forms (cc) reachable at a given JSD above floor, and the lowest verbatim among settings keeping forms >= 48.4%:

| Language | JSD >= 0.049 | JSD >= 0.089 | JSD >= 0.126 | JSD >= 0.166 | Lowest verbatim |
|---|---|---|---|---|---|
| sanskrit | 43.0% | 34.9% | 27.0% | 14.1% | 16.1% |
| tamil | 42.2% | 23.3% | 5.0% | 3.9% | 11.0% |
| sumerian | 63.2% | 45.6% | 24.9% | 8.7% | 20.7% |
| latin | 32.1% | 19.6% | 9.3% | 5.8% | 9.9% |
| finnish | 33.6% | 18.6% | 9.0% | 5.9% | 12.7% |

## Trade-off over the original grid (1,080 settings, dev means)

Best shared word forms (cc) reachable at a given JSD above floor, and the lowest verbatim among settings keeping forms >= 36.8%:

| Language | JSD >= 0.049 | JSD >= 0.089 | JSD >= 0.126 | JSD >= 0.166 | Lowest verbatim |
|---|---|---|---|---|---|
| sanskrit | 54.6% | 38.6% | 27.5% | 13.3% | 14.5% |
| tamil | 44.3% | 26.7% | 9.2% | 3.4% | 8.4% |
| sumerian | 63.6% | 45.0% | 21.5% | 7.5% | 12.6% |
| latin | 35.5% | 21.4% | 10.9% | 6.2% | 8.8% |
| finnish | 36.3% | 18.0% | 13.3% | 6.0% | 9.2% |

## Original calibration (sister plan targets; content split) — FAILED

### Original `close`

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 90-91 | 0.225 | 3.5% | 0.4% | 2.5% | no |
| sanskrit | 12 / 0.75 / 0.5 / 1.0 / 0.3 | 0-2 held out | 0.216 | 5.3% | 0.2% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 90-91 | 0.187 | 3.0% | 0.1% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0.3 | 0-2 held out | 0.185 | 3.6% | 0.1% | 1.8% | no |
| sumerian | no grid point with verbatim <= 2% | | - | - | - | - | no |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 90-91 | 0.158 | 6.3% | 1.1% | 2.1% | no |
| latin | 0 / 0.75 / 0.35 / 0 / 0 | 0-2 held out | 0.135 | 7.8% | 1.1% | 2.4% | no |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 90-91 | 0.163 | 4.1% | 0.2% | 2.1% | no |
| finnish | 9 / 0.5 / 0.5 / 1.0 / 0.3 | 0-2 held out | 0.154 | 4.8% | 0.2% | 3.5% | no |

### Original `distant`

| Language | Knobs (n_cond / affix / lexical / word order / final-V loss) | Seeds | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Matched |
|---|---|---|---|---|---|---|---|
| sanskrit | 12 / 1.0 / 0.5 / 0.5 / 0 | 90-91 | 0.276 | 1.7% | 0.3% | 2.1% | no |
| sanskrit | 12 / 1.0 / 0.5 / 0.5 / 0 | 0-2 held out | 0.276 | 1.5% | 0.0% | 1.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0 | 90-91 | 0.194 | 2.7% | 0.1% | 2.9% | no |
| tamil | 12 / 1.0 / 0.1 / 0.5 / 0 | 0-2 held out | 0.189 | 3.0% | 0.1% | 2.0% | no |
| sumerian | no grid point with verbatim <= 2% | | - | - | - | - | no |
| latin | 6 / 1.0 / 0.5 / 0 / 0 | 90-91 | 0.208 | 3.6% | 0.4% | 1.4% | no |
| latin | 6 / 1.0 / 0.5 / 0 / 0 | 0-2 held out | 0.197 | 3.3% | 0.2% | 1.3% | no |
| finnish | 9 / 0.75 / 0.1 / 0 / 0 | 90-91 | 0.199 | 2.9% | 0.3% | 1.8% | no |
| finnish | 9 / 0.75 / 0.1 / 0 / 0 | 0-2 held out | 0.198 | 3.0% | 0.5% | 2.5% | no |

