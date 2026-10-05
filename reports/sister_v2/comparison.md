# Sister-v1 vs sister-v2: related and candidates tiers

Analysis of saved records only. Methods frozen at `frozen-v1`. Task D token accuracy, %, mean over 20 corpora per seed (5 languages x 4 script types), 95% interval resampling whole languages.

- **sister-v1**: upper bound (sister-v1, known overlap). Clauses split by index, so identical clauses can sit in both halves.
- **sister-v2**: clauses split by a hash of their content; 0 identical clauses shared.
- **after cognate** = with oracle sound correspondences (the solver's frozen `_translate` step uses the true sister-to-hidden map). **before cognate** = the raw sister-unit prediction scored directly; equal to after cognate when the sister was not chosen. Recorded for sister-v2 only.

## Generator-v1, seeds 0-2

### Indus point (2,906 texts x 4.6 signs), 60 sister-v2 corpora

| Tier | Rule | sister-v1, upper bound (known overlap) | sister-v2, with oracle sound correspondences | sister-v2, before cognate |
|---|---|---|---|---|
| related | original (frozen) | 24.6 [13.3, 33.8] | 23.2 [14.0, 32.2] | 15.9 [8.8, 23.1] |
| related | revised (post hoc) | 25.8 [13.9, 35.8] | 24.4 [15.1, 33.7] | 16.7 [9.5, 24.9] |
| candidates | original (frozen) | 2.1 [1.1, 3.0] | 2.8 [1.2, 4.9] | 2.4 [1.2, 3.8] |
| candidates | revised (post hoc) | 14.6 [5.9, 23.2] | 12.5 [4.7, 20.3] | 9.1 [3.6, 14.5] |

### Corpus size (4.6 signs), original rule, candidates tier

| Texts | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| 500 | 2.7 | 2.6 | 2.5 |
| 1,000 | 2.7 | 2.2 | 2.0 |
| 2,000 | 2.2 | 2.5 | 2.3 |
| 2,906 | 2.1 | 2.8 | 2.4 |
| 5,500 | 2.6 | 2.7 | 2.7 |
| 10,000 | 4.4 | 3.0 | 2.9 |
| 20,000 | 4.1 | 2.7 | 2.6 |
| 50,000 | 5.1 | 4.4 | 3.7 |

### Longer vs more inscriptions at equal tokens, original rule, candidates tier

Length points: 2,906 texts at the given mean length, with interval. Size: interpolated on log(tokens) between size points, no interval.

| Signs/text (tokens) | sister-v1: length vs size | sister-v2 oracle corr.: length vs size | sister-v2 before cognate: length vs size |
|---|---|---|---|
| 6 (17,436) | 7.1 [1.3, 15.8] vs 2.3 | 6.5 [1.3, 15.4] vs 2.8 | 5.1 [1.3, 11.4] vs 2.5 |
| 10 (29,060) | **32.6 [17.9, 47.4] vs 3.0** | **28.6 [13.0, 44.3] vs 2.8** | **18.0 [8.6, 27.4] vs 2.7** |
| 20 (58,120) | **43.6 [22.4, 62.3] vs 4.3** | **40.2 [19.4, 61.0] vs 2.9** | **25.3 [11.9, 38.1] vs 2.8** |

Bold: the length interval lies above the interpolated size value.

### How often the sister was chosen at the Indus point (candidates tier)

- original (frozen): sister-v2 20% of corpora; sister-v1 20%
- revised (post hoc): sister-v2 37% of corpora; sister-v1 37%

### Per-language, Indus point, original rule, candidates tier

| Language | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| sanskrit | 2.2 | 2.8 | 2.8 |
| tamil | 2.9 | 2.7 | 2.7 |
| sumerian | 3.6 | 6.8 | 5.0 |
| latin | 0.1 | 0.3 | 0.3 |
| finnish | 1.8 | 1.4 | 1.4 |

## Generator-v1, seeds 3-5

### Indus point (2,906 texts x 4.6 signs), 60 sister-v2 corpora

| Tier | Rule | sister-v1, upper bound (known overlap) | sister-v2, with oracle sound correspondences | sister-v2, before cognate |
|---|---|---|---|---|
| related | original (frozen) | 23.9 [15.1, 32.6] | 23.2 [13.9, 32.3] | 15.1 [9.2, 21.3] |
| related | revised (post hoc) | 25.9 [16.8, 34.9] | 24.3 [15.6, 33.0] | 15.0 [9.3, 21.1] |
| candidates | original (frozen) | 3.3 [1.3, 5.4] | 2.7 [1.2, 4.0] | 2.7 [1.2, 3.8] |
| candidates | revised (post hoc) | 13.6 [5.4, 21.7] | 11.7 [4.5, 19.0] | 7.6 [3.3, 12.0] |

### Corpus size (4.6 signs), original rule, candidates tier

| Texts | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| 500 | 2.7 | 3.2 | 3.2 |
| 1,000 | 2.3 | 2.5 | 2.3 |
| 2,000 | 3.2 | 3.4 | 3.4 |
| 2,906 | 3.3 | 2.7 | 2.7 |
| 5,500 | 2.9 | 3.5 | 3.4 |
| 10,000 | 3.1 | 3.2 | 3.2 |
| 20,000 | 6.0 | 3.0 | 2.9 |
| 50,000 | 5.9 | 4.5 | 3.5 |

### Longer vs more inscriptions at equal tokens, original rule, candidates tier

Length points: 2,906 texts at the given mean length, with interval. Size: interpolated on log(tokens) between size points, no interval.

| Signs/text (tokens) | sister-v1: length vs size | sister-v2 oracle corr.: length vs size | sister-v2 before cognate: length vs size |
|---|---|---|---|
| 6 (17,436) | 7.1 [2.1, 12.7] vs 3.1 | 6.5 [1.8, 12.8] vs 3.1 | 4.8 [1.8, 8.3] vs 3.0 |
| 10 (29,060) | **28.6 [15.0, 42.9] vs 2.9** | **29.8 [13.0, 46.6] vs 3.4** | **17.7 [8.6, 26.8] vs 3.4** |
| 20 (58,120) | **45.0 [24.3, 63.4] vs 4.1** | **43.1 [21.3, 64.7] vs 3.1** | **25.7 [14.2, 37.1] vs 3.1** |

Bold: the length interval lies above the interpolated size value.

### How often the sister was chosen at the Indus point (candidates tier)

- original (frozen): sister-v2 20% of corpora; sister-v1 20%
- revised (post hoc): sister-v2 30% of corpora; sister-v1 28%

### Per-language, Indus point, original rule, candidates tier

| Language | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| sanskrit | 3.5 | 3.7 | 3.7 |
| tamil | 3.1 | 2.6 | 2.6 |
| sumerian | 6.9 | 5.0 | 4.6 |
| latin | 0.0 | 0.0 | 0.0 |
| finnish | 3.1 | 2.3 | 2.3 |

## Generator-v2, seeds 0-2

### Indus point (2,906 texts x 4.6 signs), 60 sister-v2 corpora

| Tier | Rule | sister-v1, upper bound (known overlap) | sister-v2, with oracle sound correspondences | sister-v2, before cognate |
|---|---|---|---|---|
| related | original (frozen) | 48.3 [31.4, 62.8] | 47.6 [32.3, 62.0] | 30.2 [20.9, 38.0] |
| related | revised (post hoc) | 49.5 [33.3, 63.7] | 49.9 [34.8, 63.3] | 31.7 [23.3, 38.8] |
| candidates | original (frozen) | 15.0 [12.5, 17.6] | 18.9 [11.0, 25.5] | 12.9 [7.8, 17.4] |
| candidates | revised (post hoc) | 42.7 [20.2, 63.5] | 40.3 [19.1, 58.1] | 25.1 [12.5, 36.2] |

### Corpus size (4.6 signs), original rule, candidates tier

| Texts | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| 500 | 5.6 | 3.9 | 3.5 |
| 2,906 | 15.0 | 18.9 | 12.9 |
| 50,000 | 32.0 | 29.3 | 18.7 |

### Longer vs more inscriptions at equal tokens, original rule, candidates tier

Length points: 2,906 texts at the given mean length, with interval. Size: interpolated on log(tokens) between size points, no interval.

| Signs/text (tokens) | sister-v1: length vs size | sister-v2 oracle corr.: length vs size | sister-v2 before cognate: length vs size |
|---|---|---|---|
| 6 (17,436) | **35.9 [24.4, 50.4] vs 16.6** | **34.3 [25.3, 45.3] vs 19.9** | **21.8 [18.1, 25.8] vs 13.5** |
| 10 (29,060) | **55.3 [36.6, 68.6] vs 19.7** | **54.9 [36.6, 68.3] vs 21.8** | **35.6 [25.5, 43.5] vs 14.5** |
| 20 (58,120) | **50.1 [32.5, 68.0] vs 23.8** | **51.8 [35.2, 68.2] vs 24.3** | **33.6 [24.6, 42.0] vs 15.9** |

Bold: the length interval lies above the interpolated size value.

### How often the sister was chosen at the Indus point (candidates tier)

- original (frozen): sister-v2 33% of corpora; sister-v1 30%
- revised (post hoc): sister-v2 58% of corpora; sister-v1 57%

### Per-language, Indus point, original rule, candidates tier

| Language | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| sanskrit | 18.4 | 26.9 | 20.2 |
| tamil | 17.9 | 26.4 | 14.5 |
| sumerian | 15.2 | 17.2 | 13.7 |
| latin | 12.8 | 20.6 | 12.5 |
| finnish | 10.9 | 3.6 | 3.6 |

## Generator-v2, seeds 3-5

### Indus point (2,906 texts x 4.6 signs), 60 sister-v2 corpora

| Tier | Rule | sister-v1, upper bound (known overlap) | sister-v2, with oracle sound correspondences | sister-v2, before cognate |
|---|---|---|---|---|
| related | original (frozen) | no sister-v1 run | 47.9 [31.5, 61.8] | 29.4 [21.2, 36.4] |
| related | revised (post hoc) | no sister-v1 run | 49.4 [33.0, 63.0] | 29.9 [21.5, 36.9] |
| candidates | original (frozen) | no sister-v1 run | 13.8 [5.6, 21.9] | 9.4 [4.7, 14.0] |
| candidates | revised (post hoc) | no sister-v1 run | 39.5 [17.9, 56.2] | 23.3 [11.3, 33.2] |

### Corpus size (4.6 signs), original rule, candidates tier

| Texts | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| 500 | n/a | 5.3 | 5.1 |
| 2,906 | n/a | 13.8 | 9.4 |
| 50,000 | n/a | 28.1 | 18.2 |

### Longer vs more inscriptions at equal tokens, original rule, candidates tier

Length points: 2,906 texts at the given mean length, with interval. Size: interpolated on log(tokens) between size points, no interval.

| Signs/text (tokens) | sister-v1: length vs size | sister-v2 oracle corr.: length vs size | sister-v2 before cognate: length vs size |
|---|---|---|---|
| 6 (17,436) | no sister-v1 run | **38.4 [25.8, 54.8] vs 15.1** | **24.2 [17.5, 32.3] vs 10.3** |
| 10 (29,060) | no sister-v1 run | **52.0 [36.0, 66.1] vs 17.7** | **32.2 [24.4, 40.6] vs 11.8** |
| 20 (58,120) | no sister-v1 run | **52.3 [36.4, 67.9] vs 21.2** | **32.8 [26.5, 39.1] vs 14.0** |

Bold: the length interval lies above the interpolated size value.

### How often the sister was chosen at the Indus point (candidates tier)

- original (frozen): sister-v2 28% of corpora
- revised (post hoc): sister-v2 57% of corpora

### Per-language, Indus point, original rule, candidates tier

| Language | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |
|---|---|---|---|
| sanskrit | n/a | 26.9 | 16.2 |
| tamil | n/a | 4.3 | 4.3 |
| sumerian | n/a | 15.3 | 13.0 |
| latin | n/a | 20.2 | 11.7 |
| finnish | n/a | 2.1 | 2.1 |

