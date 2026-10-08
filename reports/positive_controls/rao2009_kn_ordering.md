# Positive control (post hoc): Rao et al. (2009) estimator

Modified Kneser-Ney bigrams, P(i) by frequency, relative = C / ln N (`ibdb.rao_kn`). Rao's values are read by eye from Fig. 1B. Corpora differ where licences forced it (Sumerian: CDLI, not ETCSL).

| Corpus | Lines | Tokens | N used (Rao's N) | C, nats | Relative | Relative, OOV merged | Rao Fig. 1B |
|---|---|---|---|---|---|---|---|
| Type 1 (no order) | 10,000 | 200,000 | 417 (417) | 5.99 | 0.99 | 0.99 | 1.00 |
| Sanskrit | 2,154 | 64,087 | 326 (388) | 3.16 | 0.55 | 0.55 | 0.66 |
| English words | 57,340 | 999,057 | 417 (417) | 3.92 | 0.65 | 0.50 | 0.64 |
| Sumerian | 250,000 | 1,266,837 | 417 (417) | 3.09 | 0.51 | 0.53 | 0.57 |
| Old Tamil | 33,883 | 663,420 | 234 (244) | 2.96 | 0.54 | 0.54 | 0.56 |
| English chars | 57,340 | 6,069,734 | 84 (128) | 2.39 | 0.54 | 0.54 | 0.51 |
| Type 2 (rigid) | 10,000 | 200,000 | 417 (417) | 0.04 | 0.01 | 0.01 | 0.00 |

**Rao ordering (high to low):** Type 1 (no order) > Sanskrit > English words > Sumerian > Old Tamil > English chars > Type 2 (rigid)

**Ours (high to low):** Type 1 (no order) > English words > Sanskrit > Old Tamil > English chars > Sumerian > Type 2 (rigid)

