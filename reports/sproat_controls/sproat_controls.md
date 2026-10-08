# Sproat non-linguistic corpora: held-out control family (Tasks A and B)

Used with the author's permission. Cite Sproat (2014) and Wu, Solman, Linehan & Sproat (2012).
Methods frozen; rules fit on the named run's Indus-point records and applied unchanged (no retraining).
IndusBarSeals excluded (it is the Indus script). Pictish reported separately (status disputed).

## Corpora (native size, Sproat's xtract.py defaults)

| System | Texts | Tokens | Types | Mean length | Duplicate rate |
|---|---|---|---|---|---|
| Vinca | 591 | 804 | 185 | 1.36 | 0.587 |
| Kudurrus | 69 | 939 | 64 | 13.61 | 0.014 |
| BarnStars | 310 | 963 | 32 | 3.11 | 0.645 |
| TotemPoles | 325 | 1798 | 477 | 5.53 | 0.037 |
| WeatherIcons | 10142 | 50710 | 16 | 5.00 | 0.604 |
| AsianEmoticons | 10000 | 59186 | 333 | 5.92 | 0.008 |
| Pictish (disputed) | 283 | 984 | 104 | 3.48 | 0.201 |

## Rules fit on `full/full` (81 training corpora)

Task A: corpora labelled 'linguistic' / corpora scored (every corpus here is non-linguistic, so any label of 'linguistic' is a false positive).

| System | Size | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio |
|---|---|---|---|---|---|---|---|
| Vinca | native | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0.363 |
| Kudurrus | native | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0.621 |
| BarnStars | native | 1/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0.388 |
| TotemPoles | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.651 |
| WeatherIcons | native | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0.742 |
| WeatherIcons | 2,906 x3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0.742 |
| AsianEmoticons | native | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0.868 |
| AsianEmoticons | 2,906 x3 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0.836 |
| Pictish | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.450 |
| **All undisputed** | all | 3/12 | 9/12 | 6/12 | 11/12 | 2/12 | |

Training-pool mean entropy ratio: synthetic languages 0.605; i.i.d. random control 0.696.

Task B: predicted script type (no non-linguistic option exists, so every prediction is wrong by construction).

| Method | Predictions over all corpora |
|---|---|
| script_type_inventory_rule | logosyllabic 6, alphabetic 5, syllabic 1, logographic 1 |
| script_type_lr | alphabetic 9, syllabic 3, logosyllabic 1 |
| segmentation_branching | syllabic 10, alphabetic 3 |

## Rules fit on `full/holdout` (81 training corpora)

Task A: corpora labelled 'linguistic' / corpora scored (every corpus here is non-linguistic, so any label of 'linguistic' is a false positive).

| System | Size | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio |
|---|---|---|---|---|---|---|---|
| Vinca | native | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0.363 |
| Kudurrus | native | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0.621 |
| BarnStars | native | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0.388 |
| TotemPoles | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.651 |
| WeatherIcons | native | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0.742 |
| WeatherIcons | 2,906 x3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0.742 |
| AsianEmoticons | native | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0.868 |
| AsianEmoticons | 2,906 x3 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0.836 |
| Pictish | native | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0.450 |
| **All undisputed** | all | 2/12 | 9/12 | 6/12 | 11/12 | 2/12 | |

Training-pool mean entropy ratio: synthetic languages 0.621; i.i.d. random control 0.759.

Task B: predicted script type (no non-linguistic option exists, so every prediction is wrong by construction).

| Method | Predictions over all corpora |
|---|---|
| script_type_inventory_rule | logosyllabic 6, alphabetic 5, syllabic 1, logographic 1 |
| script_type_lr | alphabetic 10, syllabic 2, logographic 1 |
| segmentation_branching | syllabic 10, logosyllabic 3 |

## Rules fit on `replication/full` (81 training corpora)

Task A: corpora labelled 'linguistic' / corpora scored (every corpus here is non-linguistic, so any label of 'linguistic' is a false positive).

| System | Size | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio |
|---|---|---|---|---|---|---|---|
| Vinca | native | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0.363 |
| Kudurrus | native | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0.621 |
| BarnStars | native | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0.388 |
| TotemPoles | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.651 |
| WeatherIcons | native | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0.742 |
| WeatherIcons | 2,906 x3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0.742 |
| AsianEmoticons | native | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0.868 |
| AsianEmoticons | 2,906 x3 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0.836 |
| Pictish | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.450 |
| **All undisputed** | all | 2/12 | 9/12 | 6/12 | 11/12 | 2/12 | |

Training-pool mean entropy ratio: synthetic languages 0.601; i.i.d. random control 0.696.

Task B: predicted script type (no non-linguistic option exists, so every prediction is wrong by construction).

| Method | Predictions over all corpora |
|---|---|
| script_type_inventory_rule | logosyllabic 6, alphabetic 5, syllabic 1, logographic 1 |
| script_type_lr | alphabetic 9, syllabic 3, logosyllabic 1 |
| segmentation_branching | syllabic 10, alphabetic 3 |

## Rules fit on `replication/holdout` (81 training corpora)

Task A: corpora labelled 'linguistic' / corpora scored (every corpus here is non-linguistic, so any label of 'linguistic' is a false positive).

| System | Size | rao2009_entropy | yadav2010_markov | fuls_positional | lee2010_tree | ling_classifier_lr | Entropy ratio |
|---|---|---|---|---|---|---|---|
| Vinca | native | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 | 0.363 |
| Kudurrus | native | 1/1 | 0/1 | 0/1 | 1/1 | 0/1 | 0.621 |
| BarnStars | native | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 0.388 |
| TotemPoles | native | 1/1 | 0/1 | 1/1 | 0/1 | 0/1 | 0.651 |
| WeatherIcons | native | 0/1 | 1/1 | 0/1 | 1/1 | 0/1 | 0.742 |
| WeatherIcons | 2,906 x3 | 0/3 | 3/3 | 0/3 | 3/3 | 0/3 | 0.742 |
| AsianEmoticons | native | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0.868 |
| AsianEmoticons | 2,906 x3 | 0/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0.836 |
| Pictish | native | 1/1 | 0/1 | 0/1 | 0/1 | 1/1 | 0.450 |
| **All undisputed** | all | 2/12 | 9/12 | 6/12 | 11/12 | 2/12 | |

Training-pool mean entropy ratio: synthetic languages 0.616; i.i.d. random control 0.754.

Task B: predicted script type (no non-linguistic option exists, so every prediction is wrong by construction).

| Method | Predictions over all corpora |
|---|---|
| script_type_inventory_rule | logosyllabic 6, alphabetic 5, syllabic 1, logographic 1 |
| script_type_lr | alphabetic 10, syllabic 2, logographic 1 |
| segmentation_branching | syllabic 10, logographic 3 |
