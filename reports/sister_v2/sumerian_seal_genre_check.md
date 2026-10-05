# Genre check: Sumerian seal inscriptions only

Hidden corpus AND synthetic sister built only from the 19,076 Ur III seal inscriptions in the CDLI dump (sister-v2 content split); other candidate languages unchanged. Indus point, seeds 0-2, 4 script types, methods frozen. Full-source Sumerian = the same jobs in the sister-v2 runs (`none` tier from the frozen-v1 runs, which do not use the sister). 12 corpora per generator and genre; no intervals (one language).

## Generator v1 (12 seal-only corpora, 12 full-source)

| Tier and score | Seal only | Full source |
|---|---|---|
| related, primary | 13.1% (max 32.6%) | 5.0% (max 13.2%) |
| related, with oracle sound correspondences | 29.4% (max 65.1%) | 6.8% (max 18.0%) |
| candidates, primary | 9.0% (max 26.3%) | 5.0% (max 13.2%) |
| candidates, with oracle sound correspondences | 26.1% (max 65.1%) | 6.8% (max 18.0%) |
| candidates, revised rule (post hoc), before cognate | 0.2% (max 1.1%) | 1.5% (max 5.3%) |
| none, original rule | 1.5% (max 7.2%) | 2.2% (max 9.2%) |
| none, revised rule | 0.2% (max 1.1%) | 2.2% (max 12.6%) |

Original rule, candidates tier, references chosen (seal only): {'sanskrit': 3, 'sumerian-sister': 9}

| Corpus statistic | Seal only | Full source |
|---|---|---|
| sign_inventory | 346 | 528 |
| duplicate_text_fraction | 0.585 | 0.374 |
| mean_length | 4.55 | 4.55 |
| coverage80_signs | 37.8 | 70.5 |
| beginners80_signs | 36.9 | 68.1 |

Seal-only corpora meeting every calibration target: 0% (knobs were calibrated on the full source).

## Generator v2 (12 seal-only corpora, 12 full-source)

| Tier and score | Seal only | Full source |
|---|---|---|
| related, primary | 8.8% (max 38.5%) | 13.7% (max 71.2%) |
| related, with oracle sound correspondences | 24.1% (max 63.7%) | 17.2% (max 81.5%) |
| candidates, primary | 7.7% (max 38.5%) | 13.7% (max 71.2%) |
| candidates, with oracle sound correspondences | 22.8% (max 63.7%) | 17.2% (max 81.5%) |
| candidates, revised rule (post hoc), before cognate | 3.6% (max 20.0%) | 2.9% (max 16.3%) |
| none, original rule | 3.6% (max 20.2%) | 2.3% (max 11.1%) |
| none, revised rule | 3.6% (max 20.0%) | 3.4% (max 15.5%) |

Original rule, candidates tier, references chosen (seal only): {'sanskrit': 1, 'sumerian-sister': 11}

| Corpus statistic | Seal only | Full source |
|---|---|---|
| sign_inventory | 336 | 503 |
| duplicate_text_fraction | 0.512 | 0.231 |
| mean_length | 4.54 | 4.54 |
| coverage80_signs | 36.8 | 71.1 |
| beginners80_signs | 25.9 | 68.7 |

Seal-only corpora meeting every calibration target: 0% (knobs were calibrated on the full source).

