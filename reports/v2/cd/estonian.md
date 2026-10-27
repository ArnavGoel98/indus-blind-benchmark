# Finnish-Estonian, Tasks C and D (pre-registration entries 9 and 10)

Hidden Finnish (Indus-point corpora, 2,906 texts, mean length 4.6) against Kalevipoeg, normalised spelling. **Gold: weak (10 word pairs, 13 of 27 letters)**, from the word pairs printed in Pajusalu (2012); reported in its own rows and not pooled with the other pairs. Scored with the entry-10 rule: a no-source gold row is unknown, not lost (old values in `entry10.md`). The synthetic sisters (`harsh`, v1 sister) are optimistic upper references, not bounds (entry 10). Revised EM, strict, `related_real:estonian` unless stated; % of sign tokens. Seeds 0-2 primary; brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only.

## Task D

| Script | Estonian (weak gold), revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | Lenient 0-2 | Ceiling | `harsh` (synthetic, optimistic) 0-2 | v1 sister (synthetic, optimistic) 0-2 |
|---|---|---|---|---|---|---|---|---|---|
| logographic | 0.0 [0.0, 0.0] | 0.3 | 0.2 [0.0, 0.5] | 0.0 | 0.0 | 0.0 | 15.5 | 0.0 | 1.0 |
| syllabic | 9.3 [3.3, 15.5] | 6.8 | 8.1 [4.4, 12.3] | 9.7 | 1.8 | 11.0 | 82.9 | 19.9 | 43.6 |
| logosyllabic | 3.7 [1.7, 5.7] | 3.5 | 3.6 [2.1, 5.1] | 3.5 | 0.6 | 5.0 | 50.5 | 8.6 | 21.2 |
| alphabetic | 29.8 [17.8, 40.3] | 32.5 | 31.1 [25.1, 36.3] | 30.0 | 3.0 | 39.8 | 86.5 | 35.9 | 65.3 |

## Readings (fixed in entry 9 before the run)

| Script | E1: floor (C2), pooled | E1: reading (gap) | E2: better unrelated ref., mean | E2: added value; paired wins | E2: measurably helps? | E3: minus `harsh` (0-2) | E4: picks Estonian (of 6) |
|---|---|---|---|---|---|---|---|
| logographic | 5.8 | at the floor (-5.6) | Latin, 0.0 | +0.2; 1 of 12 | no | +0.0 | 0 |
| syllabic | 12.6 | at the floor (-4.6) | Latin, 2.6 | +5.5; 7 of 12 | no | -10.5 | 6 |
| logosyllabic | 9.3 | at the floor (-5.7) | Latin, 1.1 | +2.5; 10 of 12 | no | -4.9 | 6 |
| alphabetic | 12.9 | above the floor (+18.3) | Latin, 11.1 | +20.1; 11 of 12 | yes | -6.1 | 3 |

E4 counts the 6 seeds 0-2 corpora per script type (24 in all: 15). References chosen in `candidates_real:estonian`: logographic: latin 4, sanskrit 1, tamil 1; syllabic: estonian 6; logosyllabic: estonian 6; alphabetic: latin 3, estonian 3.

*At the floor* = no more than 2 points above the C2 floor, as in `controls.md` (entry 8).

## Ceilings (entries 9 and 10; no solver)

| Script | Ceiling, entry 10 (no source = unknown) | Ceiling, before entry 10 (no-source letters dropped) | Ceiling reachable by the solver (top 250 units) |
|---|---|---|---|
| logographic | 15.6 | 22.7 | 12.3 |
| syllabic | 82.9 | 96.5 | 82.9 |
| logosyllabic | 50.5 | 60.5 | 49.7 |
| alphabetic | 86.4 | 86.4 | 86.4 |

Before entry 10 the harness dropped a no-source letter from a syllable or word reflex, so such tokens counted as recoverable with a shortened reflex; entry 10 makes them unrecoverable. Seeds 0-5, both samplers.

**Frozen-code notes.** The syllable cutter uses the hidden language's vowel set, so Estonian õ and ü (not Finnish letters) are cut as consonants in the Estonian reference; neither is the regular reflex of any Finnish letter in this gold.
