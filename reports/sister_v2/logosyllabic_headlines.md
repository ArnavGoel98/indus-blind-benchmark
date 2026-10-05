# Headline numbers, logo-syllabic corpora only (most Indus-relevant script type)

Analysis of saved records only; methods frozen. 5 languages x 3 seeds = 15 corpora per point and seed set. Intervals resample whole languages (5 clusters; see the limitations on undercoverage). Primary = original (frozen) rule, before the cognate step.

## Entropy ratio (Task A, Indus point, Rao top-100 merge, as recorded in `rao_ratio`)

- full: logo-syllabic 0.591 (n=15), all languages 0.605, i.i.d. control 0.696
- replication: logo-syllabic 0.587 (n=15), all languages 0.601, i.i.d. control 0.696

The i.i.d. control scores HIGHER than the languages on this statistic, as in the pooled result.

## No related language (`none` tier, Indus point)

| Run | Mean, original | Mean, revised | Best corpus (orig / rev) | >= 50% |
|---|---|---|---|---|
| Generator v1, seeds 0-2 | 0.0% | 0.8% | 0.4% / 4.1% | 0 of 30 |
| Generator v1, seeds 3-5 | 0.1% | 0.9% | 0.5% / 2.3% | 0 of 30 |
| Generator v2, seeds 0-2 | 0.3% | 1.1% | 2.5% / 4.0% | 0 of 30 |

## Generator contrast (candidates tier, Indus point)

| Seed set | v1 primary | v2 primary | Ratio | v1 with oracle corr. | v2 with oracle corr. |
|---|---|---|---|---|---|
| seeds 0-2 | 0.6 [0.0, 1.5] | 3.6 [0.2, 9.3] | 6.3x | 0.6 | 6.8 |
| seeds 3-5 | 0.9 [0.0, 2.6] | 1.6 [0.2, 3.9] | 1.8x | 0.9 | 2.1 |
| sister-v3, seeds 0-2 | 1.1 [0.0, 3.2] | 3.4 [0.2, 9.2] | 3.0x | 1.0 | 6.2 |

## Related tier (sister only), Indus point

| Seed set | v1 primary | v2 primary | v1 with oracle corr. | v2 with oracle corr. |
|---|---|---|---|---|
| seeds 0-2 | 3.6 [2.4, 4.7] | 18.8 [6.6, 31.0] | 5.7 | 35.6 |
| seeds 3-5 | 3.2 [2.0, 4.4] | 20.4 [8.3, 34.8] | 5.1 | 37.2 |

## Longer vs more inscriptions at equal tokens (candidates tier, primary)

| Generator | Longer (2,906 x 10) | More (6,317 x 4.6) |
|---|---|---|
| v1 | 12.7 [2.8, 27.6] | 0.2 [0.0, 0.7] |
| v2 | 27.8 [9.9, 45.3] | 6.4 [0.2, 16.8] |

