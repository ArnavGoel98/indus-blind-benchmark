# Headline 1 with Rao et al.'s (2009) estimator (post hoc)

Relative conditional entropy C / ln N, modified Kneser-Ney bigrams (`ibdb.rao_kn`). Indus point: 2,906 texts,
mean 4.6 signs. All 324 regenerated corpora match their stored records. The plug-in conditional-to-unigram
ratio (top-100 merge, the frozen method's score) is shown for comparison.

## Relative conditional entropy, all signs

| Run / regime | Synthetic languages: mean (10th-90th pct; min-max) | i.i.d. random control (3) | Rigid control | Other built controls (min-max) | Languages below i.i.d. min | AUC lang vs i.i.d. |
|---|---|---|---|---|---|---|
| full / full | 0.530 (0.418-0.629; 0.332-0.693) | 0.906 (0.899-0.920) | 0.102 | 0.450-0.636 | 60/60 | 1.00 |
| full / holdout | 0.541 (0.423-0.666; 0.278-0.717) | 0.926 (0.920-0.935) | 0.138 | 0.529-0.655 | 60/60 | 1.00 |
| replication / full | 0.525 (0.411-0.612; 0.317-0.687) | 0.900 (0.898-0.901) | 0.102 | 0.475-0.641 | 60/60 | 1.00 |
| replication / holdout | 0.536 (0.395-0.661; 0.336-0.708) | 0.921 (0.915-0.931) | 0.169 | 0.524-0.673 | 60/60 | 1.00 |

Sproat's attested systems:

| System | Size | Relative |
|---|---|---|
| Vinca | native | 0.849 |
| Kudurrus | native | 0.715 |
| BarnStars | native | 0.361 |
| TotemPoles | native | 0.738 |
| WeatherIcons | native | 0.567 |
| WeatherIcons | 2,906-text samples | 0.594 (0.587-0.597) |
| AsianEmoticons | native | 0.580 |
| AsianEmoticons | 2,906-text samples | 0.601 (0.598-0.606) |
| Pictish | native | 0.565 |

## Relative conditional entropy, 417 most frequent signs

| Run / regime | Synthetic languages: mean (10th-90th pct; min-max) | i.i.d. random control (3) | Rigid control | Other built controls (min-max) | Languages below i.i.d. min | AUC lang vs i.i.d. |
|---|---|---|---|---|---|---|
| full / full | 0.538 (0.424-0.629; 0.330-0.701) | 0.906 (0.899-0.920) | 0.105 | 0.454-0.644 | 60/60 | 1.00 |
| full / holdout | 0.550 (0.428-0.673; 0.272-0.741) | 0.930 (0.924-0.938) | 0.114 | 0.542-0.655 | 60/60 | 1.00 |
| replication / full | 0.532 (0.413-0.612; 0.318-0.689) | 0.900 (0.898-0.901) | 0.104 | 0.480-0.653 | 60/60 | 1.00 |
| replication / holdout | 0.544 (0.405-0.666; 0.338-0.728) | 0.922 (0.917-0.932) | 0.111 | 0.542-0.673 | 60/60 | 1.00 |

Sproat's attested systems:

| System | Size | Relative |
|---|---|---|
| Vinca | native | 0.849 |
| Kudurrus | native | 0.715 |
| BarnStars | native | 0.361 |
| TotemPoles | native | 0.731 |
| WeatherIcons | native | 0.567 |
| WeatherIcons | 2,906-text samples | 0.594 (0.587-0.597) |
| AsianEmoticons | native | 0.580 |
| AsianEmoticons | 2,906-text samples | 0.601 (0.598-0.606) |
| Pictish | native | 0.565 |

For comparison, plug-in ratio (top-100 merge), full/full: languages 0.605, i.i.d. random control 0.696.

