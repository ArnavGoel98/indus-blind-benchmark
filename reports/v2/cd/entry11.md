# Entry 11: the syllable-cutter fix, confirmed on development seeds 0-2

Pre-registration entry 11 (declared before any code or rerun). Real relatives are now cut into syllables with the hidden language's vowels and their own vowel letters (adds õ and ü for Estonian, vocalic ṛ for Malayalam and Kannada). The rerun covers only the cells whose solver input changes: Finnish and Old Tamil, syllabic and logo-syllabic, seeds 0-2, samplers A and B (24 corpora); entry-10 scorer; entry-6 methods and budget. *Old* = the entry-10 records (frozen-v2 cutter); *new* = this rerun. Development seeds only: these values do not replace the development tables, and the cutter's effect is read in the final run (entry 12).

## Does the fix work? (criteria fixed in entry 11, D)

| Criterion | Result | Met? |
|---|---|---|
| D.1 Only the references that may change do: Estonian, Malayalam, Kannada; syllabic and logo-syllabic (Italian, every alphabetic and logographic reference and every `harsh` reference unchanged; tests in `tests/test_entry11.py`) | 6 of 36 references changed: finnish real:estonian logosyllabic; finnish real:estonian syllabic; tamil real:kannada logosyllabic; tamil real:kannada syllabic; tamil real:malayalam logosyllabic; tamil real:malayalam syllabic | yes |
| D.2 Units of every word still join to the word; every word cut differently contains an added vowel letter | 10,207 words cut differently, 0 without an added vowel; joins all correct | yes |
| D.3 Rerun completes with 0 errors | 0 errors in 24 corpora | yes |

The raw ceiling depends on the gold only and is unchanged in every corpus.

## Old and new, per cell (seeds 0-2, 6 corpora each)

| Relative | Script | Revised EM old → new | Original EM old → new | Frequency rank old → new | Lenient old → new | Reachable ceiling old → new | Raw ceiling | Picks the relative (of 6) old → new |
|---|---|---|---|---|---|---|---|---|
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 3.7 → 7.6 | 3.5 → 7.8 | 0.6 → 0.9 | 5.0 → 8.8 | 49.8 → 49.6 | 50.5 | 6 → 5 |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 9.3 → 9.9 | 9.7 → 10.0 | 1.8 → 1.9 | 11.0 → 11.9 | 82.9 → 82.9 | 82.9 | 6 → 5 |
| Malayalam | logosyllabic | 5.9 → 5.5 | 6.6 → 5.4 | 1.9 → 1.8 | 8.4 → 7.7 | 69.1 → 69.0 | 72.8 | 0 → 0 |
| Kannada | logosyllabic | 2.9 → 3.5 | 2.5 → 3.4 | 1.4 → 1.4 | 3.9 → 4.4 | 65.9 → 65.9 | 72.5 | 6 → 6 |
| Malayalam | syllabic | 6.2 → 5.9 | 5.9 → 5.3 | 2.2 → 2.0 | 9.8 → 9.0 | 99.9 → 99.7 | 100.0 | 0 → 0 |
| Kannada | syllabic | 3.3 → 4.1 | 3.4 → 4.1 | 1.3 → 0.9 | 4.8 → 6.1 | 95.1 → 95.1 | 100.0 | 3 → 5 |

## Per corpus (revised EM, strict)

| Relative | Script | Seed | Sampler | Old | New | Difference | Reachable old → new | Reference chosen in `candidates_real`, old → new |
|---|---|---|---|---|---|---|---|---|
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 0 | A | 0.7 | 1.7 | +1.0 | 52.7 → 52.7 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 0 | B | 0.6 | 9.7 | +9.1 | 52.2 → 52.0 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 1 | A | 6.7 | 6.1 | -0.6 | 49.2 → 49.1 | estonian → latin |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 1 | B | 6.6 | 5.0 | -1.6 | 48.6 → 48.3 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 2 | A | 3.1 | 0.8 | -2.3 | 45.6 → 45.6 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 2 | B | 4.6 | 22.4 | +17.8 | 50.3 → 50.1 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 0 | A | 1.9 | 3.9 | +2.0 | 86.0 → 86.0 | estonian → latin |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 0 | B | 22.1 | 19.0 | -3.1 | 79.6 → 79.6 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 1 | A | 0.1 | 4.8 | +4.7 | 85.1 → 85.1 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 1 | B | 9.1 | 22.0 | +12.9 | 80.9 → 80.9 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 2 | A | 15.8 | 0.5 | -15.3 | 84.7 → 84.7 | estonian → estonian |
| Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 2 | B | 6.9 | 9.4 | +2.5 | 81.3 → 81.3 | estonian → estonian |
| Malayalam | logosyllabic | 0 | A | 2.0 | 0.8 | -1.2 | 55.9 → 55.9 | latin → latin |
| Kannada | logosyllabic | 0 | A | 0.8 | 0.9 | +0.1 | 53.1 → 53.1 | kannada → kannada |
| Malayalam | logosyllabic | 0 | B | 3.9 | 4.3 | +0.3 | 88.9 → 88.9 | latin → latin |
| Kannada | logosyllabic | 0 | B | 6.0 | 6.8 | +0.8 | 85.2 → 85.2 | kannada → kannada |
| Malayalam | logosyllabic | 1 | A | 1.6 | 3.7 | +2.1 | 44.7 → 44.7 | finnish → finnish |
| Kannada | logosyllabic | 1 | A | 0.4 | 0.3 | -0.1 | 43.0 → 43.0 | kannada → kannada |
| Malayalam | logosyllabic | 1 | B | 18.3 | 18.2 | -0.1 | 88.5 → 88.4 | latin → latin |
| Kannada | logosyllabic | 1 | B | 4.5 | 6.7 | +2.1 | 84.7 → 84.7 | kannada → kannada |
| Malayalam | logosyllabic | 2 | A | 2.6 | 0.3 | -2.3 | 47.8 → 47.8 | latin → latin |
| Kannada | logosyllabic | 2 | A | 0.0 | 1.6 | +1.6 | 45.9 → 45.9 | kannada → kannada |
| Malayalam | logosyllabic | 2 | B | 7.1 | 5.5 | -1.6 | 88.6 → 88.5 | finnish → finnish |
| Kannada | logosyllabic | 2 | B | 5.4 | 4.8 | -0.5 | 83.8 → 83.8 | kannada → kannada |
| Malayalam | syllabic | 0 | A | 3.4 | 3.3 | -0.0 | 99.9 → 99.7 | finnish → finnish |
| Kannada | syllabic | 0 | A | 0.8 | 8.1 | +7.3 | 95.2 → 95.2 | finnish → finnish |
| Malayalam | syllabic | 0 | B | 4.6 | 3.6 | -1.1 | 99.9 → 99.6 | latin → latin |
| Kannada | syllabic | 0 | B | 5.0 | 7.5 | +2.5 | 94.0 → 94.0 | kannada → kannada |
| Malayalam | syllabic | 1 | A | 8.7 | 3.5 | -5.2 | 99.9 → 99.7 | latin → latin |
| Kannada | syllabic | 1 | A | 4.8 | 0.4 | -4.5 | 95.3 → 95.3 | latin → kannada |
| Malayalam | syllabic | 1 | B | 5.4 | 10.0 | +4.5 | 99.9 → 99.7 | finnish → finnish |
| Kannada | syllabic | 1 | B | 5.5 | 5.1 | -0.4 | 95.4 → 95.4 | finnish → kannada |
| Malayalam | syllabic | 2 | A | 4.3 | 5.5 | +1.2 | 99.9 → 99.6 | latin → latin |
| Kannada | syllabic | 2 | A | 1.0 | 1.4 | +0.4 | 95.7 → 95.7 | kannada → kannada |
| Malayalam | syllabic | 2 | B | 10.8 | 9.6 | -1.3 | 100.0 → 99.7 | finnish → finnish |
| Kannada | syllabic | 2 | B | 2.3 | 1.9 | -0.5 | 95.2 → 95.2 | kannada → kannada |
