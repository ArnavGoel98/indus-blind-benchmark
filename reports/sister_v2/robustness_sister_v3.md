# Robustness check: sister-v3 (no hidden-text word sequence in the sister)

Analysis of saved records only; methods frozen at `frozen-v1`. Seeds 0-2, 5 languages x 4 script types = 60 corpora per point. Task D token accuracy, %, 95% interval resampling whole languages.

- **sister-v2**: clauses split by content hash (no clause in both halves).
- **sister-v3**: sister-v2, then every sister clause containing any hidden text's word sequence (as contiguous words) is dropped, separately for each corpus. A truncated hidden text also contributes its whole words without the last one. Only the sister is filtered.
- **Primary**: original (frozen) rule, before the cognate step. Secondary: with oracle sound correspondences.

## Residual overlap under sister-v3

Verbatim containment of hidden texts in the sister's source half is 0 by construction (word level, before sound change and lexical replacement). The table shows how much of the sister the filter removes and how many of the hidden texts' word pairs (bigrams) still occur in it.

| Generator | Language | Sister clauses dropped | Hidden word bigrams in sister: sister-v2 | sister-v3 |
|---|---|---|---|---|
| Generator v1 | sanskrit | 33% | 39% | 8% |
| Generator v1 | tamil | 27% | 20% | 3% |
| Generator v1 | sumerian | 32% | 50% | 22% |
| Generator v1 | latin | 45% | 19% | 3% |
| Generator v1 | finnish | 30% | 27% | 3% |
| Generator v1 | all | 33% | 31% | 8% |
| Generator v2 | sanskrit | 37% | 46% | 9% |
| Generator v2 | tamil | 29% | 18% | 3% |
| Generator v2 | sumerian | 45% | 69% | 19% |
| Generator v2 | latin | 59% | 21% | 1% |
| Generator v2 | finnish | 42% | 20% | 1% |
| Generator v2 | all | 42% | 35% | 7% |

(Indus point, 2,906 texts x 4.6 signs.)

## Indus point (2,906 texts x 4.6 signs)

| Generator | Tier | sister-v2, primary | sister-v3, primary | sister-v2, with oracle sound correspondences | sister-v3, with oracle sound correspondences |
|---|---|---|---|---|---|
| Generator v1 | related | 15.9 [8.8, 23.1] | 12.4 [6.4, 19.1] | 23.2 [14.0, 32.2] | 16.9 [8.9, 25.4] |
| Generator v1 | candidates | 2.4 [1.2, 3.8] | 2.6 [1.2, 4.2] | 2.8 [1.2, 4.9] | 2.6 [1.2, 4.4] |
| Generator v2 | related | 30.2 [20.9, 38.0] | 27.3 [17.4, 36.0] | 47.6 [32.3, 62.0] | 42.9 [26.9, 59.1] |
| Generator v2 | candidates | 12.9 [7.8, 17.4] | 9.3 [5.4, 13.5] | 18.9 [11.0, 25.5] | 12.3 [5.8, 18.9] |

### Headline 3 check: generator contrast, candidates tier, primary

- sister-v2: v1 2.4 [1.2, 3.8] vs v2 12.9 [7.8, 17.4] (ratio 5.3x; corpora >= 50%: 0 of 60 vs 4 of 60)
- sister-v3: v1 2.6 [1.2, 4.2] vs v2 9.3 [5.4, 13.5] (ratio 3.7x; corpora >= 50%: 0 of 60 vs 2 of 60)

### Which reference the original rule chose (candidates tier, Indus point)

- Generator v1, sister-v2: sister chosen for 20% of corpora
- Generator v1, sister-v3: sister chosen for 20% of corpora
- Generator v2, sister-v2: sister chosen for 33% of corpora
- Generator v2, sister-v3: sister chosen for 28% of corpora

## Headline 4 check: longer vs more inscriptions at equal tokens (~29k), candidates tier

Length: 2,906 texts x 10 signs (29,060 tokens). Size: 6,317 texts x 4.6 signs (29,058 tokens), run directly at this point (no interpolation).

| Generator | Sister | Score | Longer (2,906 x 10) | More (6,317 x 4.6) | Difference [95% CI] |
|---|---|---|---|---|---|
| Generator v1 | sister-v2 | primary | 18.0 [8.6, 27.4] | 2.6 [1.3, 4.0] | 15.4 [5.8, 24.9] |
| Generator v1 | sister-v2 | with oracle sound correspondences | 28.6 [13.0, 44.3] | 2.7 [1.3, 4.1] | 25.9 [10.5, 41.4] |
| Generator v1 | sister-v3 | primary | 17.5 [8.7, 27.3] | 3.9 [1.3, 7.1] | 13.6 [5.8, 21.3] |
| Generator v1 | sister-v3 | with oracle sound correspondences | 26.9 [11.6, 42.2] | 4.5 [1.3, 8.7] | 22.4 [8.6, 36.2] |
| Generator v2 | sister-v2 | primary | 35.6 [25.5, 43.5] | 18.3 [17.1, 19.8] | 17.4 [8.5, 25.0] |
| Generator v2 | sister-v2 | with oracle sound correspondences | 54.9 [36.6, 68.3] | 27.6 [23.8, 31.8] | 27.4 [12.8, 39.0] |
| Generator v2 | sister-v3 | primary | 34.6 [23.6, 42.9] | 10.5 [6.1, 14.8] | 24.1 [11.9, 35.9] |
| Generator v2 | sister-v3 | with oracle sound correspondences | 53.4 [33.9, 67.7] | 15.3 [7.8, 23.0] | 38.1 [18.0, 56.4] |

Difference = longer minus more, paired by (language, script type, seed); interval resamples whole languages.

**Confound under sister-v3.** The filter depends on the corpus. Many short texts contain many short word sequences, so they strip more of the sister than fewer long texts do:

| Generator | Corpus | Sister clauses dropped | Hidden word bigrams left in sister |
|---|---|---|---|
| Generator v1 | 2,906 x 4.6 | 33% | 8% |
| Generator v1 | 2,906 x 10 | 9% | 16% |
| Generator v1 | 6,317 x 4.6 | 40% | 6% |
| Generator v2 | 2,906 x 4.6 | 42% | 7% |
| Generator v2 | 2,906 x 10 | 15% | 16% |
| Generator v2 | 6,317 x 4.6 | 52% | 3% |

So sister-v3 handicaps the 'more inscriptions' corpus more than the 'longer inscriptions' corpus, which can widen the gap. Sister-v2 applies no corpus-dependent filter, and the length advantage is already present there; read sister-v3 as a check that the advantage survives, not as a better estimate of its size.

