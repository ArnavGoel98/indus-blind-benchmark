# Finnish-Estonian, Tasks C and D (pre-registration entry 9)

Hidden Finnish (Indus-point corpora, 2,906 texts, mean length 4.6) against Kalevipoeg, normalised spelling. Gold from the word pairs printed in Pajusalu (2012), 13 of 27 rows with a regular reflex; reported in its own rows and not pooled with the other pairs. Revised EM, strict, `related_real:estonian` unless stated; % of sign tokens. Seeds 0-2 primary; brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only.

## Task D

| Script | Revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | Lenient 0-2 | Ceiling | `harsh` 0-2 | v1 sister 0-2 |
|---|---|---|---|---|---|---|---|---|---|
| logographic | 0.0 [0.0, 0.0] | 0.3 | 0.2 [0.0, 0.5] | 0.0 | 0.0 | 0.0 | 22.4 | 0.0 | 1.0 |
| syllabic | 9.3 [3.3, 15.6] | 7.5 | 8.4 [4.8, 12.5] | 10.2 | 1.8 | 11.1 | 96.5 | 19.9 | 43.6 |
| logosyllabic | 3.9 [1.9, 5.9] | 3.7 | 3.8 [2.2, 5.3] | 3.7 | 0.6 | 5.3 | 60.5 | 8.6 | 21.2 |
| alphabetic | 29.8 [17.8, 40.3] | 32.5 | 31.1 [25.1, 36.3] | 30.0 | 3.0 | 39.8 | 86.5 | 35.9 | 65.3 |

## Readings (fixed in entry 9 before the run)

| Script | E1: floor (C2), pooled | E1: reading (gap) | E2: better unrelated ref., mean | E2: added value; paired wins | E2: measurably helps? | E3: minus `harsh` (0-2) | E4: picks Estonian (of 6) |
|---|---|---|---|---|---|---|---|
| logographic | 5.8 | at the floor (-5.6) | Latin, 0.0 | +0.2; 2 of 12 | no | +0.0 | 0 |
| syllabic | 13.8 | at the floor (-5.4) | Latin, 3.8 | +4.6; 7 of 12 | no | -10.5 | 6 |
| logosyllabic | 9.6 | at the floor (-5.8) | Latin, 1.6 | +2.2; 8 of 12 | no | -4.7 | 6 |
| alphabetic | 12.9 | above the floor (+18.3) | Latin, 11.1 | +20.1; 11 of 12 | yes | -6.1 | 3 |

E4 counts the 6 seeds 0-2 corpora per script type (24 in all: 15). References chosen in `candidates_real:estonian`: logographic: latin 4, sanskrit 1, tamil 1; syllabic: estonian 6; logosyllabic: estonian 6; alphabetic: latin 3, estonian 3.

*At the floor* = no more than 2 points above the C2 floor, as in `controls.md` (entry 8).

## Scorer diagnostics (entry 9; no solver)

| Script | Ceiling | Tokens whose reflex silently drops a no-source letter | Ceiling reachable by the solver (top 250 units) |
|---|---|---|---|
| logographic | 22.7 | 7.0 | 15.8 |
| syllabic | 96.5 | 13.6 | 96.5 |
| logosyllabic | 60.5 | 10.0 | 58.6 |
| alphabetic | 86.4 | 0.0 | 86.4 |

The middle column is an upper bound on how far the frozen scorer's handling of "no source" rows can raise a score (entry 9): such tokens count as recoverable with a shortened reflex. Seeds 0-5, both samplers.

**Frozen-code notes.** The syllable cutter uses the hidden language's vowel set, so Estonian õ and ü (not Finnish letters) are cut as consonants in the Estonian reference; neither is the regular reflex of any Finnish letter in this gold.
