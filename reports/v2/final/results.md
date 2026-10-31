# v2 final run, seeds 6-11: results against the pre-registered readings

Readings, thresholds and layout fixed in `docs/v2_final_run_readings.md` (entry 12) before any seed 6-11 corpus existed. Revised EM, strict, `related` tier, % of sign tokens, mean over the corpora of each cell (12 when complete); brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only. No test is made. Seeds 0-5 are the development set; their answers are shown beside each reading, not pooled. Finnish-Estonian gold is weak (10 word pairs, 13 of 27 letters). The synthetic sisters are optimistic upper references.

## 1. Readings not met

- **H3** On syllabic and logo-syllabic scripts, a real relative measurably helps in at most 1 of the 8 cells. Threshold: count <= 1. Seeds 6-11: 3: Malayalam syllabic, Estonian syllabic, Estonian logosyllabic. Development: 1: Malayalam syllabic.

## Process failures

- Missing corpora (failed twice or never run): 0 of 240
- Errors recorded (including retried corpora): 0
- C4: 0 mismatches in 3,904 values

## 2. Readings met

- **H1** Every real-relative cell mean is below 50%. Seeds 6-11: 16 of 16 below; highest 40.5 (Kannada, alphabetic). Development: highest 34.4 (Kannada, alphabetic).
- **H2a** Estonian measurably helps on alphabetic scripts (C1 rule). Seeds 6-11: +17.0; 11 of 12. Development: +20.1; 11 of 12.
- **H2b** Kannada measurably helps on alphabetic scripts (C1 rule). Seeds 6-11: +23.9; 11 of 12. Development: +15.1; 9 of 12.
- **H4** Every real relative scores below the v1 sister in each syllabic, logo-syllabic and alphabetic cell. Seeds 6-11: 12 of 12. Development: 12 of 12.
- **H5** Old Tamil alphabetic with Malayalam and with Kannada both within 10 points of the Ugaritic result (32.0%). Seeds 6-11: 27.8 and 40.5. Development: 30.5 and 34.4.
- **H6** Italian below `harsh` on alphabetic and on syllabic scripts. Seeds 6-11: 16.6 vs 26.3; 3.0 vs 16.3. Development: 20.3 vs 31.5; 4.2 vs 16.9.
- **H7** Revised EM picks the real relative in fewer than half of its `candidates_real` corpora: Italian, Malayalam, Kannada. Seeds 6-11: Italian 12 of 48; Malayalam 0 of 48; Kannada 23 of 48. Development: Italian 12 of 48; Malayalam 0 of 48; Kannada 19 of 48.
- **H8** Determinism (C4): every compared value identical. Seeds 6-11: 3,904 of 3,904 values identical in 24 corpora. Development: met: 120 of 120 (entry 8); 3,348 of 3,348 (entry 10).

## T1. Readings

| ID | Reading | Threshold | Seeds 6-11 value | Met? | Development answer | Agrees? |
|---|---|---|---|---|---|---|
| H1 | Every real-relative cell mean is below 50% | 16 of 16 cells < 50.0 | 16 of 16 below; highest 40.5 (Kannada, alphabetic) | yes | highest 34.4 (Kannada, alphabetic) | yes |
| H2a | Estonian measurably helps on alphabetic scripts (C1 rule) | >= 5.0 points and >= 9 of 12 paired wins | +17.0; 11 of 12 | yes | +20.1; 11 of 12 | yes |
| H2b | Kannada measurably helps on alphabetic scripts (C1 rule) | >= 5.0 points and >= 9 of 12 paired wins | +23.9; 11 of 12 | yes | +15.1; 9 of 12 | yes |
| H3 | On syllabic and logo-syllabic scripts, a real relative measurably helps in at most 1 of the 8 cells | count <= 1 | 3: Malayalam syllabic, Estonian syllabic, Estonian logosyllabic | no | 1: Malayalam syllabic | no |
| H4 | Every real relative scores below the v1 sister in each syllabic, logo-syllabic and alphabetic cell | 12 of 12 cells | 12 of 12 | yes | 12 of 12 | yes |
| H5 | Old Tamil alphabetic with Malayalam and with Kannada both within 10 points of the Ugaritic result (32.0%) | both in 22.0-42.0 | 27.8 and 40.5 | yes | 30.5 and 34.4 | yes |
| H6 | Italian below `harsh` on alphabetic and on syllabic scripts | both cells | 16.6 vs 26.3; 3.0 vs 16.3 | yes | 20.3 vs 31.5; 4.2 vs 16.9 | yes |
| H7 | Revised EM picks the real relative in fewer than half of its `candidates_real` corpora: Italian, Malayalam, Kannada | each < half (<= 23 of 48) | Italian 12 of 48; Malayalam 0 of 48; Kannada 23 of 48 | yes | Italian 12 of 48; Malayalam 0 of 48; Kannada 19 of 48 | yes |
| H8 | Determinism (C4): every compared value identical | 0 mismatches, 24 corpora | 3,904 of 3,904 values identical in 24 corpora | yes | met: 120 of 120 (entry 8); 3,348 of 3,348 (entry 10) | yes |

## T2. Task D per pair

| Relative | Script | Revised EM mean [95% CI] | Corpora >= 50% | Original EM | Frequency rank | Lenient | Reachable ceiling (primary) | Raw ceiling | `harsh` (synthetic, optimistic) | v1 sister (synthetic, optimistic) |
|---|---|---|---|---|---|---|---|---|---|---|
| Italian (descendant of Latin) | logographic | 0.1 [0.0, 0.1] | 0 of 12 | 0.0 | 0.0 | 0.3 | 25.2 | 51.8 | 3.7 [1.4, 6.9] | 1.5 [0.4, 2.9] |
| Italian (descendant of Latin) | syllabic | 3.0 [1.9, 4.2] | 0 of 12 | 3.2 | 2.4 | 4.2 | 100.0 | 100.0 | 16.3 [12.1, 20.7] | 27.6 [14.3, 41.6] |
| Italian (descendant of Latin) | logosyllabic | 1.5 [0.9, 2.3] | 0 of 12 | 2.2 | 3.5 | 2.3 | 66.4 | 76.4 | 4.0 [3.0, 5.0] | 8.2 [6.1, 10.3] |
| Italian (descendant of Latin) | alphabetic | 16.6 [7.8, 26.3] | 0 of 12 | 18.3 | 8.1 | 22.0 | 99.1 | 99.1 | 26.3 [17.7, 36.7] | 43.7 [34.6, 53.5] |
| Malayalam (descendant of Old Tamil) | logographic | 0.0 [0.0, 0.1] | 0 of 12 | 0.0 | 0.0 | 0.0 | 10.0 | 16.6 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| Malayalam (descendant of Old Tamil) | syllabic | 9.7 [6.5, 13.3] | 0 of 12 | 10.0 | 4.3 | 11.7 | 99.6 | 100.0 | 5.6 [2.8, 8.9] | 32.9 [24.3, 41.5] |
| Malayalam (descendant of Old Tamil) | logosyllabic | 7.8 [4.0, 12.7] | 0 of 12 | 8.0 | 2.5 | 11.1 | 71.6 | 75.5 | 4.4 [2.8, 6.4] | 24.3 [13.5, 35.9] |
| Malayalam (descendant of Old Tamil) | alphabetic | 27.8 [16.1, 39.3] | 2 of 12 | 31.2 | 5.8 | 29.2 | 100.0 | 100.0 | 14.1 [7.5, 20.8] | 47.5 [36.7, 57.6] |
| Kannada (sister of Old Tamil) | logographic | 0.0 [0.0, 0.0] | 0 of 12 | 0.0 | 0.0 | 0.0 | 2.2 | 24.5 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| Kannada (sister of Old Tamil) | syllabic | 3.8 [1.8, 5.9] | 0 of 12 | 4.5 | 1.3 | 5.4 | 95.0 | 100.0 | 5.6 [2.8, 8.9] | 32.9 [24.3, 41.5] |
| Kannada (sister of Old Tamil) | logosyllabic | 3.2 [1.8, 5.1] | 0 of 12 | 3.4 | 0.9 | 4.7 | 68.4 | 74.8 | 4.4 [2.8, 6.4] | 24.3 [13.5, 35.9] |
| Kannada (sister of Old Tamil) | alphabetic | 40.5 [33.0, 48.0] | 5 of 12 | 39.7 | 9.8 | 42.6 | 97.6 | 100.0 | 14.1 [7.5, 20.8] | 47.5 [36.7, 57.6] |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 0.6 [0.0, 1.7] | 0 of 12 | 0.4 | 0.0 | 0.6 | 12.4 | 15.8 | 1.3 [0.1, 2.8] | 0.9 [0.0, 2.0] |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 11.0 [5.3, 17.2] | 0 of 12 | 11.1 | 1.7 | 13.1 | 82.8 | 82.8 | 19.0 [12.8, 25.3] | 40.2 [29.9, 50.0] |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 7.7 [4.2, 11.2] | 0 of 12 | 7.6 | 0.5 | 9.2 | 49.0 | 50.1 | 9.3 [6.9, 11.9] | 15.7 [8.8, 23.0] |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 26.9 [19.7, 34.2] | 0 of 12 | 27.5 | 5.5 | 38.8 | 86.1 | 86.1 | 43.0 [35.4, 50.9] | 61.8 [57.5, 65.6] |

## T3. Controls per pair

| Relative | Script | Floor (C2) | At the floor? (gap) | Better unrelated ref., mean | Added value; paired wins | Measurably helps? | Minus `harsh` | Minus v1 sister | Picks the relative |
|---|---|---|---|---|---|---|---|---|---|
| Italian (descendant of Latin) | logographic | 14.3 | at the floor (-14.2) | Finnish, 0.0 | +0.0; 3 of 12 | no | -3.7 | -1.5 | 0 of 12 |
| Italian (descendant of Latin) | syllabic | 10.2 | at the floor (-7.2) | Finnish, 6.1 | -3.1; 3 of 12 | no | -13.3 | -24.6 | 0 of 12 |
| Italian (descendant of Latin) | logosyllabic | 7.3 | at the floor (-5.8) | Finnish, 2.0 | -0.5; 5 of 12 | no | -2.5 | -6.7 | 12 of 12 |
| Italian (descendant of Latin) | alphabetic | 14.2 | above the floor (+2.3) | Finnish, 15.0 | +1.6; 7 of 12 | no | -9.8 | -27.2 | 0 of 12 |
| Malayalam (descendant of Old Tamil) | logographic | 8.7 | at the floor (-8.7) | Latin, 0.0 | +0.0; 1 of 12 | no | +0.0 | +0.0 | 0 of 12 |
| Malayalam (descendant of Old Tamil) | syllabic | 5.9 | above the floor (+3.8) | Finnish, 3.5 | +6.2; 10 of 12 | yes | +4.1 | -23.2 | 0 of 12 |
| Malayalam (descendant of Old Tamil) | logosyllabic | 3.9 | above the floor (+3.9) | Finnish, 2.4 | +5.4; 8 of 12 | no | +3.4 | -16.5 | 0 of 12 |
| Malayalam (descendant of Old Tamil) | alphabetic | 16.0 | above the floor (+11.8) | Finnish, 17.1 | +10.6; 8 of 12 | no | +13.6 | -19.8 | 0 of 12 |
| Kannada (sister of Old Tamil) | logographic | 18.0 | at the floor (-18.0) | Latin, 0.0 | +0.0; 0 of 12 | no | +0.0 | +0.0 | 0 of 12 |
| Kannada (sister of Old Tamil) | syllabic | 5.9 | at the floor (-2.2) | Finnish, 3.6 | +0.2; 7 of 12 | no | -1.8 | -29.1 | 11 of 12 |
| Kannada (sister of Old Tamil) | logosyllabic | 3.9 | at the floor (-0.6) | Finnish, 2.4 | +0.8; 8 of 12 | no | -1.2 | -21.0 | 12 of 12 |
| Kannada (sister of Old Tamil) | alphabetic | 14.2 | above the floor (+26.3) | Finnish, 16.7 | +23.9; 11 of 12 | yes | +26.4 | -7.0 | 0 of 12 |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 5.8 | at the floor (-5.2) | Latin, 0.0 | +0.6; 2 of 12 | no | -0.7 | -0.3 | 0 of 12 |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 12.6 | at the floor (-1.6) | Latin, 2.2 | +8.7; 10 of 12 | yes | -8.1 | -29.2 | 12 of 12 |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 9.1 | at the floor (-1.4) | Latin, 2.4 | +5.4; 9 of 12 | yes | -1.6 | -8.0 | 8 of 12 |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 12.7 | above the floor (+14.2) | Latin, 9.9 | +17.0; 11 of 12 | yes | -16.1 | -34.9 | 8 of 12 |

*At the floor* = no more than 2 points above the constant-prediction floor; *measurably helps* = at least 5 points above the better unrelated reference and ahead of it in at least 9 of 12 paired corpora (entry 8).

## T4. Synthetic references, all five languages

`related` tier

| Hidden | Reference | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|
| Sanskrit | v1 sister (synthetic, optimistic) | 2.3 [0.2, 4.8], n=12 | 33.6 [27.0, 41.1], n=12 | 4.5 [2.4, 6.7], n=12 | 48.0 [43.0, 53.5], n=12 |
| Sanskrit | `harsh` (synthetic, optimistic) | 4.5 [1.3, 8.3], n=12 | 6.6 [3.9, 10.4], n=12 | 0.7 [0.3, 1.3], n=12 | 30.1 [24.8, 35.1], n=12 |
| Old Tamil | v1 sister (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 32.9 [24.3, 41.5], n=12 | 24.3 [13.5, 35.9], n=12 | 47.5 [36.7, 57.6], n=12 |
| Old Tamil | `harsh` (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 5.6 [2.8, 8.9], n=12 | 4.4 [2.8, 6.4], n=12 | 14.1 [7.5, 20.8], n=12 |
| Sumerian | v1 sister (synthetic, optimistic) | 1.6 [0.6, 2.6], n=12 | 2.5 [0.9, 4.5], n=12 | 1.9 [0.7, 3.3], n=12 | 29.9 [15.9, 45.5], n=12 |
| Sumerian | `harsh` (synthetic, optimistic) | 0.6 [0.2, 1.2], n=12 | 1.5 [0.5, 2.4], n=12 | 1.2 [0.4, 2.1], n=12 | 18.8 [12.2, 26.4], n=12 |
| Latin | v1 sister (synthetic, optimistic) | 1.5 [0.4, 2.9], n=12 | 27.6 [14.3, 41.6], n=12 | 8.2 [6.1, 10.3], n=12 | 43.7 [34.6, 53.5], n=12 |
| Latin | `harsh` (synthetic, optimistic) | 3.7 [1.4, 6.9], n=12 | 16.3 [12.1, 20.7], n=12 | 4.0 [3.0, 5.0], n=12 | 26.3 [17.7, 36.7], n=12 |
| Finnish | v1 sister (synthetic, optimistic) | 0.9 [0.0, 2.0], n=12 | 40.2 [29.9, 50.0], n=12 | 15.7 [8.8, 23.0], n=12 | 61.8 [57.5, 65.6], n=12 |
| Finnish | `harsh` (synthetic, optimistic) | 1.3 [0.1, 2.8], n=12 | 19.0 [12.8, 25.3], n=12 | 9.3 [6.9, 11.9], n=12 | 43.0 [35.4, 50.9], n=12 |

`candidates` tier

| Hidden | Reference | logographic | syllabic | logosyllabic | alphabetic |
|---|---|---|---|---|---|
| Sanskrit | v1 sister (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 33.6 [27.0, 41.1], n=12 | 1.3 [0.7, 2.1], n=12 | 16.8 [13.8, 19.8], n=12 |
| Sanskrit | `harsh` (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 1.5 [0.7, 2.3], n=12 | 0.8 [0.3, 1.4], n=12 | 13.3 [9.7, 17.0], n=12 |
| Old Tamil | v1 sister (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 26.2 [14.4, 38.0], n=12 | 22.1 [10.2, 34.9], n=12 | 27.3 [12.5, 44.0], n=12 |
| Old Tamil | `harsh` (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 1.7 [1.0, 2.3], n=12 | 1.1 [0.3, 2.1], n=12 | 10.3 [5.8, 15.3], n=12 |
| Sumerian | v1 sister (synthetic, optimistic) | 0.0 [0.0, 0.0], n=12 | 0.4 [0.0, 0.8], n=12 | 0.9 [0.3, 1.7], n=12 | 14.2 [6.9, 25.8], n=12 |
| Sumerian | `harsh` (synthetic, optimistic) | 0.6 [0.2, 1.2], n=12 | 0.4 [0.1, 0.8], n=12 | 1.0 [0.3, 1.8], n=12 | 8.7 [6.4, 10.9], n=12 |
| Latin | v1 sister (synthetic, optimistic) | 1.3 [0.3, 2.8], n=12 | 28.7 [16.2, 41.9], n=12 | 6.5 [4.4, 8.8], n=12 | 42.3 [32.2, 52.9], n=12 |
| Latin | `harsh` (synthetic, optimistic) | 3.0 [0.6, 6.3], n=12 | 5.8 [3.8, 7.6], n=12 | 0.9 [0.3, 1.5], n=12 | 26.3 [17.7, 36.7], n=12 |
| Finnish | v1 sister (synthetic, optimistic) | 0.9 [0.0, 2.0], n=12 | 40.2 [29.9, 50.0], n=12 | 15.6 [8.6, 22.8], n=12 | 55.2 [43.4, 64.7], n=12 |
| Finnish | `harsh` (synthetic, optimistic) | 1.3 [0.1, 2.8], n=12 | 14.8 [8.0, 22.4], n=12 | 4.8 [1.9, 8.5], n=12 | 33.5 [21.7, 45.9], n=12 |

## T5. Task C

| Relative | Script | References chosen by revised EM (`candidates_real`) | Family correct: revised EM | original EM | frequency rank |
|---|---|---|---|---|---|
| Italian (descendant of Latin) | logographic | finnish 12 | 0.0% | 0.0% | 50.0% |
| Italian (descendant of Latin) | syllabic | finnish 12 | 0.0% | 0.0% | 91.7% |
| Italian (descendant of Latin) | logosyllabic | italian 12 | 100.0% | 0.0% | 16.7% |
| Italian (descendant of Latin) | alphabetic | finnish 11, sumerian 1 | 0.0% | 0.0% | 0.0% |
| Malayalam (descendant of Old Tamil) | logographic | latin 8, finnish 4 | 0.0% | 0.0% | 0.0% |
| Malayalam (descendant of Old Tamil) | syllabic | finnish 6, latin 6 | 0.0% | 0.0% | 41.7% |
| Malayalam (descendant of Old Tamil) | logosyllabic | latin 7, finnish 5 | 0.0% | 0.0% | 0.0% |
| Malayalam (descendant of Old Tamil) | alphabetic | finnish 7, latin 5 | 0.0% | 0.0% | 100.0% |
| Kannada (sister of Old Tamil) | logographic | latin 8, finnish 4 | 0.0% | 0.0% | 0.0% |
| Kannada (sister of Old Tamil) | syllabic | kannada 11, finnish 1 | 91.7% | 0.0% | 0.0% |
| Kannada (sister of Old Tamil) | logosyllabic | kannada 12 | 100.0% | 0.0% | 0.0% |
| Kannada (sister of Old Tamil) | alphabetic | finnish 7, latin 5 | 0.0% | 0.0% | 0.0% |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logographic | latin 9, tamil 2, sanskrit 1 | 0.0% | 0.0% | 0.0% |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | estonian 12 | 100.0% | 0.0% | 0.0% |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | estonian 8, latin 4 | 66.7% | 0.0% | 8.3% |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | estonian 8, latin 4 | 66.7% | 0.0% | 100.0% |

| Hidden | Script | Family correct, v1 sister `candidates` (revised EM) | Family correct, `candidates_harsh` |
|---|---|---|---|
| Sanskrit | logographic | 100.0% | 100.0% |
| Sanskrit | syllabic | 100.0% | 58.3% |
| Sanskrit | logosyllabic | 100.0% | 100.0% |
| Sanskrit | alphabetic | 0.0% | 0.0% |
| Old Tamil | logographic | 0.0% | 50.0% |
| Old Tamil | syllabic | 58.3% | 0.0% |
| Old Tamil | logosyllabic | 50.0% | 0.0% |
| Old Tamil | alphabetic | 33.3% | 0.0% |
| Sumerian | logographic | 8.3% | 91.7% |
| Sumerian | syllabic | 0.0% | 0.0% |
| Sumerian | logosyllabic | 0.0% | 8.3% |
| Sumerian | alphabetic | 8.3% | 0.0% |
| Latin | logographic | 66.7% | 66.7% |
| Latin | syllabic | 58.3% | 16.7% |
| Latin | logosyllabic | 58.3% | 0.0% |
| Latin | alphabetic | 91.7% | 100.0% |
| Finnish | logographic | 75.0% | 100.0% |
| Finnish | syllabic | 100.0% | 50.0% |
| Finnish | logosyllabic | 58.3% | 25.0% |
| Finnish | alphabetic | 83.3% | 66.7% |

## T6. C3 solver budget (seeds 6-8)

| Relative | Script | n | 3 restarts | 10 restarts | Difference | First-order? |
|---|---|---|---|---|---|---|
| Italian (descendant of Latin) | logographic | 6 | 0.1 | 0.2 | +0.1 | no |
| Italian (descendant of Latin) | syllabic | 6 | 3.4 | 3.5 | +0.1 | no |
| Italian (descendant of Latin) | logosyllabic | 6 | 1.5 | 3.6 | +2.2 | no |
| Italian (descendant of Latin) | alphabetic | 6 | 14.2 | 18.2 | +4.1 | no |
| Malayalam (descendant of Old Tamil) | logographic | 6 | 0.0 | 0.0 | +0.0 | no |
| Malayalam (descendant of Old Tamil) | syllabic | 6 | 11.3 | 14.2 | +2.9 | no |
| Malayalam (descendant of Old Tamil) | logosyllabic | 6 | 7.6 | 7.6 | -0.0 | no |
| Malayalam (descendant of Old Tamil) | alphabetic | 6 | 32.4 | 35.3 | +2.9 | no |
| Kannada (sister of Old Tamil) | logographic | 6 | 0.0 | 0.2 | +0.2 | no |
| Kannada (sister of Old Tamil) | syllabic | 6 | 6.2 | 5.5 | -0.8 | no |
| Kannada (sister of Old Tamil) | logosyllabic | 6 | 4.2 | 2.6 | -1.7 | no |
| Kannada (sister of Old Tamil) | alphabetic | 6 | 38.9 | 37.3 | -1.7 | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 6 | 1.1 | 1.1 | +0.0 | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 6 | 8.3 | 13.6 | +5.3 | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 6 | 4.3 | 2.5 | -1.8 | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 6 | 24.4 | 29.3 | +4.9 | no |

## T7. Agreement with the development seeds (0-5)

| Relative | Script | At the floor? 6-11 / dev | Measurably helps? 6-11 / dev | Below `harsh`? 6-11 / dev | Below v1 sister? 6-11 / dev | Agree (all four) |
|---|---|---|---|---|---|---|
| Italian (descendant of Latin) | logographic | yes / yes | no / no | yes / yes | yes / yes | yes |
| Italian (descendant of Latin) | syllabic | yes / yes | no / no | yes / yes | yes / yes | yes |
| Italian (descendant of Latin) | logosyllabic | yes / yes | no / no | yes / yes | yes / yes | yes |
| Italian (descendant of Latin) | alphabetic | no / no | no / no | yes / yes | yes / yes | yes |
| Malayalam (descendant of Old Tamil) | logographic | yes / yes | no / no | no / no | no / no | yes |
| Malayalam (descendant of Old Tamil) | syllabic | no / no | yes / yes | no / no | yes / yes | yes |
| Malayalam (descendant of Old Tamil) | logosyllabic | no / no | no / no | no / no | yes / yes | yes |
| Malayalam (descendant of Old Tamil) | alphabetic | no / no | no / no | no / no | yes / yes | yes |
| Kannada (sister of Old Tamil) | logographic | yes / yes | no / no | no / no | no / no | yes |
| Kannada (sister of Old Tamil) | syllabic | yes / yes | no / no | yes / yes | yes / yes | yes |
| Kannada (sister of Old Tamil) | logosyllabic | yes / yes | no / no | yes / yes | yes / yes | yes |
| Kannada (sister of Old Tamil) | alphabetic | no / no | yes / yes | no / no | yes / yes | yes |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logographic | yes / yes | no / no | yes / no | yes / yes | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | yes / yes | yes / no | yes / yes | yes / yes | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | yes / yes | yes / no | yes / yes | yes / yes | no |
| Estonian (sister of Finnish; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | no / no | yes / yes | yes / yes | yes / yes | yes |

Disagreements are reported, not resolved. Cross-script comparisons, including with Ugaritic-Hebrew, are indicative only. Nothing here enters the paper before the project owner has seen it.
