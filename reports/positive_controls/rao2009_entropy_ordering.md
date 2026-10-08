# Positive control: conditional-entropy ordering vs Rao et al. (2009)

Rao et al. give these measures only as figures (Fig. 1A curves, Fig. 1B bars; the supplement's Table S1 has Indus perplexities only), so their values below are read by eye. Their corpora differ from ours (Rig Veda vs Ramayana; Brown corpus vs Pride and Prejudice; ETCSL vs CDLI), so only the ORDERING is comparable. Note: Rao's 'type 1' is the system without sequential order and 'type 2' the rigid one; our control keys use the opposite numbering.

| Corpus | H(X2|X1), nats, N=20 | N=100 | N=200 | N=400 | Relative (vs shuffled), N=400 |
|---|---|---|---|---|---|
| Sanskrit (syllables) | 2.05 | 3.24 | 3.36 | 3.35 | 0.75 |
| Old Tamil (syllables) | 1.80 | 3.26 | 3.34 | 3.34 | 0.74 |
| Sumerian (logo-syllabic signs) | 1.19 | 2.67 | 3.09 | 3.24 | 0.67 |
| English words | 1.46 | 2.59 | 2.97 | 3.31 | 0.81 |
| English chars | 2.47 | 2.47 | 2.47 | 2.47 | 0.85 |
| Our i.i.d. control (Rao type 1; our `rao_type2`) | 0.36 | 1.69 | 3.19 | 5.45 | 1.00 |
| Our rigid control (Rao type 2; our `rao_type1`) | 0.18 | 0.64 | 0.64 | 0.08 | 0.02 |

**Rao et al. 2009, Fig. 1B (read by eye):** Type 1 (no order) 1.00, DNA 0.98, Protein 0.96, Sanskrit 0.66, English words 0.64, Sumerian 0.57, Old Tamil 0.56, Indus 0.55, English chars 0.51, Fortran 0.39, Type 2 (rigid) 0.00.

**Our ordering (relative, N=400, high to low):** Our i.i.d. control (Rao type 1; our `rao_type2`) (1.00) > English chars (0.85) > English words (0.81) > Sanskrit (syllables) (0.75) > Old Tamil (syllables) (0.74) > Sumerian (logo-syllabic signs) (0.67) > Our rigid control (Rao type 2; our `rao_type1`) (0.02).

