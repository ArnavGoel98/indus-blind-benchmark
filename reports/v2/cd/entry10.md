# Entry 10: "no source" read as unknown instead of lost (old → new)

Pre-registration entry 10 (declared 2026-10-27, before any rerun). Before it, the v2 harness dropped a no-source gold letter from a syllable or word reflex, like a lost sound; now such a token is unrecoverable, and the yardsticks break the text there. Affected pairs: Finnish-Estonian (Finnish p, v, j, y, ö, d, g, loan letters, and ä) and Old Tamil-Malayalam and -Kannada (h, s, ṣ, ḵ). Latin-Italian has no no-source row and is unchanged. Values are % of sign tokens, revised EM, strict, `related` tier unless stated; **bold** = changed.

**Rerun:** 96 corpora, 0 errors. **Reproducibility:** 3,348 old-map values compared with the archived entry 6-9 records, 0 mismatches.

## Ceilings and Task D (seeds 0-2 primary; pooled 0-5)

| Pair | Script | Ceiling 0-2 | Revised EM 0-2 | Pooled 0-5 | Lenient 0-2 | Original EM 0-2 | Frequency rank 0-2 |
|---|---|---|---|---|---|---|---|
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logographic | 22.4 → **15.5** | 0.0 | 0.2 | 0.0 | 0.0 | 0.0 |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 96.5 → **82.9** | 9.3 | 8.4 → **8.1** | 11.0 | 10.2 → **9.7** | 1.8 |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 60.5 → **50.5** | 3.9 → **3.7** | 3.8 → **3.6** | 5.3 → **5.0** | 3.7 → **3.5** | 0.6 |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 86.5 | 29.8 | 31.1 | 39.8 | 30.0 | 3.0 |
| Old Tamil-Malayalam | logographic | 17.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Old Tamil-Malayalam | syllabic | 100.0 | 6.2 | 10.7 | 9.8 | 5.9 | 2.2 |
| Old Tamil-Malayalam | logosyllabic | 72.8 | 5.9 | 6.6 | 8.4 | 6.6 | 1.9 |
| Old Tamil-Malayalam | alphabetic | 100.0 | 30.4 | 30.5 | 33.6 | 30.4 | 3.5 |
| Old Tamil-Kannada | logographic | 24.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Old Tamil-Kannada | syllabic | 100.0 | 3.3 | 4.0 | 4.8 | 3.4 | 1.3 |
| Old Tamil-Kannada | logosyllabic | 72.5 | 2.9 | 3.9 | 3.9 | 2.5 | 1.4 |
| Old Tamil-Kannada | alphabetic | 100.0 | 32.2 | 34.4 | 34.2 | 33.5 | 6.3 |

## Controls (entries 8 and 9 readings, seeds 0-5)

| Pair | Script | Floor (C2) | At the floor? old → new | Better unrelated ref. | Added value | Paired wins (of 12) | Measurably helps? old → new |
|---|---|---|---|---|---|---|---|
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logographic | 5.8 | yes → yes | Latin, 0.0 | 0.2 → 0.2 | 2 → 1 | no → no |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 13.8 → **12.6** | yes → yes | Latin, 3.8 → **2.6** | 4.6 → 5.5 | 7 → 7 | no → no |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 9.6 → **9.3** | yes → yes | Latin, 1.6 → **1.1** | 2.2 → 2.5 | 8 → 10 | no → no |
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 12.9 | no → no | Latin, 11.1 | 20.1 → 20.1 | 11 → 11 | yes → yes |
| Old Tamil-Malayalam | logographic | 8.6 | yes → yes | Latin, 0.0 | 0.0 → 0.0 | 0 → 0 | no → no |
| Old Tamil-Malayalam | syllabic | 6.2 | no → no | Latin, 3.1 | 7.6 → 7.6 | 10 → 10 | yes → yes |
| Old Tamil-Malayalam | logosyllabic | 3.6 | no → no | Finnish, 2.3 | 4.3 → 4.3 | 10 → 10 | no → no |
| Old Tamil-Malayalam | alphabetic | 15.8 | no → no | Finnish, 19.7 | 10.7 → 10.7 | 7 → 7 | no → no |
| Old Tamil-Kannada | logographic | 17.5 | yes → yes | Latin, 0.0 | 0.0 → 0.0 | 2 → 2 | no → no |
| Old Tamil-Kannada | syllabic | 6.2 | yes → yes | Latin, 3.1 | 0.9 → 0.9 | 8 → 8 | no → no |
| Old Tamil-Kannada | logosyllabic | 3.5 | yes → yes | Finnish, 2.2 | 1.7 → 1.7 | 9 → 9 | no → no |
| Old Tamil-Kannada | alphabetic | 14.2 | no → no | Finnish, 19.4 | 15.1 → 15.1 | 9 → 9 | yes → yes |

## Solver budget (C3, Old Tamil, seeds 0-2; alphabetic cannot change)

| Pair | Script | 3 restarts | 10 restarts | First-order? old → new |
|---|---|---|---|---|
| Old Tamil-Malayalam | logographic | 0.0 | 0.0 | no → no |
| Old Tamil-Malayalam | syllabic | 6.2 | 8.4 | no → no |
| Old Tamil-Malayalam | logosyllabic | 5.9 | 8.7 | no → no |
| Old Tamil-Kannada | logographic | 0.0 | 0.0 | no → no |
| Old Tamil-Kannada | syllabic | 3.3 | 3.0 | no → no |
| Old Tamil-Kannada | logosyllabic | 2.9 | 2.6 | no → no |

## Readings re-evaluated

- R1 (entry 7, Old Tamil): every seeds 3-5 real-relative mean stays below 50% (highest 36.7%). Scores can only fall under entry 10, so R1 cannot flip.
- R2 (Old Tamil alphabetic within 22.0-42.0%), R3 (Italian below `harsh`) and R4 (relative picked in fewer than half of the `candidates_real` corpora) do not depend on no-source scoring: alphabetic scores, Latin and the references chosen are unchanged.
- E3 and E4 (entry 9): `harsh` and the choice of reference are unchanged; E3 is recomputed in `estonian.md`.
- Flipped readings: none.

## Yardsticks and verbatim overlap (normalised; point estimates)

| Pair | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Verbatim share (inspection) | Windows drawn | Hits spanning 2+ whole words |
|---|---|---|---|---|---|---|---|
| Finnish-Estonian (weak gold: 10 word pairs, 13 of 27 letters) | 0.184 → **0.183** | -7.9% → **10.6%** | -1.8% → **0.6%** | 1.4% → **1.3%** | 1.2% → **3.1%** | 10,041 → 6,074 | 0 → 0 |
| Old Tamil-Malayalam | 0.139 → **0.141** | 5.7% → **5.9%** | 0.0% | 1.8% → **0.8%** | 1.4% → **1.6%** | 10,089 → 10,082 | 1 → 0 |
| Old Tamil-Kannada | 0.180 → **0.181** | 4.7% → **5.8%** | 0.0% → **0.0%** | 1.0% → **1.2%** | 1.6% → **1.5%** | 10,089 → 10,082 | 3 → 0 |
| Latin-Italian (unchanged by construction) | 0.104 | 11.8% | 0.6% | 1.9% | 2.5% | 8,488 → 8,488 | 0 → 0 |

Under entry 10 a verbatim window cannot span a no-source letter, so windows come only from stretches written in letters the gold covers; for Finnish (12.6% of letters without a source) this favours letters known to correspond, which raises the verbatim share. An implementation error found before these results were reported was corrected on 2026-10-27: after a break inside a word, the stretch's first letter had been counted as a word start, which produced spurious multi-word hits.

Bootstrap intervals for the new values: `reports/v2/real_relatives/yardsticks.md` and `estonian.md`. The exploratory post-hoc check of 2026-10-24 (`estonian_sensitivity.md`, which filled the no-source rows from general knowledge) is superseded by this rule and kept as a dated record.
