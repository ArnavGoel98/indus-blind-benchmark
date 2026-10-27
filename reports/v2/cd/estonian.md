# Finnish-Estonian, Tasks C and D (pre-registration entries 9-11)

Hidden Finnish (Indus-point corpora, 2,906 texts, mean length 4.6) against Kalevipoeg, normalised spelling. **Gold: weak (10 word pairs, 13 of 27 letters)**, from the word pairs printed in Pajusalu (2012); reported in its own rows and not pooled with the other pairs. Scored with the entry-10 rule: a no-source gold row is unknown, not lost (old values in `entry10.md`). The synthetic sisters (`harsh`, v1 sister) are optimistic upper references, not bounds (entry 10). Revised EM, strict, `related_real:estonian` unless stated; % of sign tokens. Seeds 0-2 primary; brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only. The readings E1-E4 of entry 9 are, in order: at the floor (E1), measurably helps (E2), minus `harsh` (E3), picks Estonian (E4).

## Task D

| Relative | Script | Revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | Lenient 0-2 | Reachable ceiling 0-2 (primary) | Raw ceiling 0-2 | `harsh` (synthetic, optimistic) 0-2 | v1 sister (synthetic, optimistic) 0-2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 0.0 [0.0, 0.0] | 0.3 | 0.2 [0.0, 0.5] | 0.0 | 0.0 | 0.0 | 12.2 | 15.5 | 0.0 | 1.0 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 9.3 [3.3, 15.5] | 6.8 | 8.1 [4.4, 12.3] | 9.7 | 1.8 | 11.0 | 82.9 | 82.9 | 19.9 | 43.6 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 3.7 [1.7, 5.7] | 3.5 | 3.6 [2.1, 5.1] | 3.5 | 0.6 | 5.0 | 49.8 | 50.5 | 8.6 | 21.2 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 29.8 [17.8, 40.3] | 32.5 | 31.1 [25.1, 36.3] | 30.0 | 3.0 | 39.8 | 86.5 | 86.5 | 35.9 | 65.3 |

## Readings (fixed before each run)

| Relative | Script | Floor (C2), pooled | At the floor? (gap) | Better unrelated ref., mean | Added value; paired wins | Measurably helps? (C1) | Minus `harsh` (0-2) | Picks the relative (of 6, seeds 0-2) |
|---|---|---|---|---|---|---|---|---|
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 5.8 | at the floor (-5.6) | Latin, 0.0 | +0.2; 1 of 12 | no | +0.0 | 0 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 12.6 | at the floor (-4.6) | Latin, 2.6 | +5.5; 7 of 12 | no | -10.5 | 6 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 9.3 | at the floor (-5.7) | Latin, 1.1 | +2.5; 10 of 12 | no | -4.9 | 6 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 12.9 | above the floor (+18.3) | Latin, 11.1 | +20.1; 11 of 12 | yes | -6.1 | 3 |

Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters): picked in 15 of 24 seeds 0-2 corpora (seeds 3-5: 14 of 24). References chosen in `candidates_real:estonian`, seeds 0-2: logographic: latin 4, sanskrit 1, tamil 1; syllabic: estonian 6; logosyllabic: estonian 6; alphabetic: latin 3, estonian 3.

*At the floor* = no more than 2 points above the C2 floor; *measurably helps* = at least 5 points above the better unrelated reference and ahead of it in at least 9 of the 12 paired corpora (entry 8). The difference from `harsh` is descriptive (no test).

## Ceilings (no solver; seeds 0-5, both samplers)

| Relative | Script | Reachable by the solver (top 250 units; primary, entry 11) | Raw ceiling, entry 10 (no source = unknown) | Raw ceiling before entry 10 (no-source letters dropped) |
|---|---|---|---|---|
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logographic | 12.3 | 15.6 | 22.7 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | syllabic | 82.9 | 82.9 | 96.5 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | logosyllabic | 49.7 | 50.5 | 60.5 |
| Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters) | alphabetic | 86.4 | 86.4 | 86.4 |

*Reachable* is the share of sign tokens whose strict regular reflex is among the reference's 250 most frequent units, the only units the EM solver can predict (entry 11 makes it the primary ceiling). The references are cut as these runs cut them (frozen-v2 cutter). Before entry 10 the harness dropped a no-source letter from a syllable or word reflex, so such tokens counted as recoverable with a shortened reflex; entry 10 makes them unrecoverable.

**Frozen-code note (fixed by entry 11 for the final run).** These runs cut the Estonian reference with Finnish's vowel set, so Estonian õ and ü were cut as consonants in the syllabic and logo-syllabic references. The confirmation rerun on seeds 0-2 with the fixed cutter is in `entry11.md`.
