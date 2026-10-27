# Old Tamil-Malayalam and Old Tamil-Kannada, Tasks C and D (entries 6-8, 10, 11)

Hidden Old Tamil (Indus-point corpora, 2,906 texts, mean length 4.6) against the Malayalam and Kannada texts, normalised spelling. Gold: Caldwell (1875), with Old Tamil h, s, ṣ and ḵ "no source" for both relatives, scored with the entry-10 rule (a no-source gold row is unknown, not lost; old values in `entry10.md`). Malayalam is a descendant, Kannada a sister. The synthetic sisters (`harsh`, v1 sister) are optimistic upper references, not bounds (entry 10). Revised EM, strict, `related_real:<relative>` unless stated; % of sign tokens. Seeds 0-2 primary (entry 6), seeds 3-5 the replication (entry 7); brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only. The same numbers, in other layouts, are in `results.md`, `pooled.md` and `controls.md`.

## Task D

| Relative | Script | Revised EM, seeds 0-2 | Seeds 3-5 | Pooled 0-5 | Original EM 0-2 | Frequency rank 0-2 | Lenient 0-2 | Reachable ceiling 0-2 (primary) | Raw ceiling 0-2 | `harsh` (synthetic, optimistic) 0-2 | v1 sister (synthetic, optimistic) 0-2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Malayalam (descendant) | logographic | 0.0 [0.0, 0.0] | 0.0 | 0.0 [0.0, 0.0] | 0.0 | 0.0 | 0.0 | 10.2 | 17.0 | 0.1 | 0.0 |
| Malayalam (descendant) | syllabic | 6.2 [4.3, 8.5] | 15.1 | 10.7 [6.9, 15.7] | 5.9 | 2.2 | 9.8 | 99.9 | 100.0 | 6.2 | 26.7 |
| Malayalam (descendant) | logosyllabic | 5.9 [2.3, 11.2] | 7.2 | 6.6 [3.9, 9.7] | 6.6 | 1.9 | 8.4 | 69.1 | 72.8 | 5.9 | 19.0 |
| Malayalam (descendant) | alphabetic | 30.4 [12.8, 47.0] | 30.5 | 30.5 [16.9, 44.2] | 30.4 | 3.5 | 33.6 | 100.0 | 100.0 | 16.4 | 42.5 |
| Kannada (sister) | logographic | 0.0 [0.0, 0.1] | 0.0 | 0.0 [0.0, 0.0] | 0.0 | 0.0 | 0.0 | 2.3 | 24.0 | 0.1 | 0.0 |
| Kannada (sister) | syllabic | 3.3 [1.8, 4.7] | 4.8 | 4.0 [2.5, 5.8] | 3.4 | 1.3 | 4.8 | 95.1 | 100.0 | 6.2 | 26.7 |
| Kannada (sister) | logosyllabic | 2.9 [1.0, 4.8] | 5.0 | 3.9 [2.0, 6.2] | 2.5 | 1.4 | 3.9 | 65.9 | 72.5 | 5.9 | 19.0 |
| Kannada (sister) | alphabetic | 32.2 [26.8, 37.6] | 36.7 | 34.4 [28.8, 41.2] | 33.5 | 6.3 | 34.2 | 97.7 | 100.0 | 16.4 | 42.5 |

## Readings (fixed before each run)

| Relative | Script | Floor (C2), pooled | At the floor? (gap) | Better unrelated ref., mean | Added value; paired wins | Measurably helps? (C1) | Minus `harsh` (0-2) | Picks the relative (of 6, seeds 0-2) |
|---|---|---|---|---|---|---|---|---|
| Malayalam (descendant) | logographic | 8.6 | at the floor (-8.6) | Latin, 0.0 | +0.0; 0 of 12 | no | -0.1 | 0 |
| Malayalam (descendant) | syllabic | 6.2 | above the floor (+4.5) | Latin, 3.1 | +7.6; 10 of 12 | yes | +0.0 | 0 |
| Malayalam (descendant) | logosyllabic | 3.6 | above the floor (+3.0) | Finnish, 2.3 | +4.3; 10 of 12 | no | +0.0 | 0 |
| Malayalam (descendant) | alphabetic | 15.8 | above the floor (+14.6) | Finnish, 19.7 | +10.7; 7 of 12 | no | +14.0 | 0 |
| Kannada (sister) | logographic | 17.5 | at the floor (-17.5) | Latin, 0.0 | +0.0; 2 of 12 | no | -0.0 | 0 |
| Kannada (sister) | syllabic | 6.2 | at the floor (-2.1) | Latin, 3.1 | +0.9; 8 of 12 | no | -2.9 | 3 |
| Kannada (sister) | logosyllabic | 3.5 | at the floor (+0.5) | Finnish, 2.2 | +1.7; 9 of 12 | no | -3.1 | 6 |
| Kannada (sister) | alphabetic | 14.2 | above the floor (+20.3) | Finnish, 19.4 | +15.1; 9 of 12 | yes | +15.8 | 0 |

Malayalam (descendant): picked in 0 of 24 seeds 0-2 corpora (seeds 3-5: 0 of 24). References chosen in `candidates_real:malayalam`, seeds 0-2: logographic: latin 6; syllabic: finnish 3, latin 3; logosyllabic: latin 4, finnish 2; alphabetic: latin 3, finnish 3.

Kannada (sister): picked in 9 of 24 seeds 0-2 corpora (seeds 3-5: 10 of 24). References chosen in `candidates_real:kannada`, seeds 0-2: logographic: latin 6; syllabic: kannada 3, finnish 2, latin 1; logosyllabic: kannada 6; alphabetic: latin 3, finnish 3.

*At the floor* = no more than 2 points above the C2 floor; *measurably helps* = at least 5 points above the better unrelated reference and ahead of it in at least 9 of the 12 paired corpora (entry 8). The difference from `harsh` is descriptive (no test).

## Ceilings (no solver; seeds 0-5, both samplers)

| Relative | Script | Reachable by the solver (top 250 units; primary, entry 11) | Raw ceiling, entry 10 (no source = unknown) | Raw ceiling before entry 10 (no-source letters dropped) |
|---|---|---|---|---|
| Malayalam (descendant) | logographic | 10.1 | 16.9 | 16.9 |
| Malayalam (descendant) | syllabic | 99.9 | 100.0 | 100.0 |
| Malayalam (descendant) | logosyllabic | 69.5 | 73.2 | 73.2 |
| Malayalam (descendant) | alphabetic | 100.0 | 100.0 | 100.0 |
| Kannada (sister) | logographic | 2.3 | 24.3 | 24.3 |
| Kannada (sister) | syllabic | 95.2 | 100.0 | 100.0 |
| Kannada (sister) | logosyllabic | 66.3 | 72.8 | 72.8 |
| Kannada (sister) | alphabetic | 97.7 | 100.0 | 100.0 |

*Reachable* is the share of sign tokens whose strict regular reflex is among the reference's 250 most frequent units, the only units the EM solver can predict (entry 11 makes it the primary ceiling). The references are cut as these runs cut them (frozen-v2 cutter). Before entry 10 the harness dropped a no-source letter from a syllable or word reflex, so such tokens counted as recoverable with a shortened reflex; entry 10 makes them unrecoverable.

**Solver budget (C3, entry 8; seeds 0-2).** More restarts change a cell by more than 10 points (first-order) in 1 of 8 real-relative cells: Malayalam alphabetic (30.4 with 3 restarts, 41.9 with 10). The primary results stay at 3 restarts (`controls.md`). Not run for Estonian.

**Frozen-code note (fixed by entry 11 for the final run).** These runs cut the Malayalam and Kannada references with Old Tamil's vowel set, so vocalic ṛ (0.24% of each text's units, in Sanskrit loans) was cut as a consonant in the syllabic and logo-syllabic references. The confirmation rerun on seeds 0-2 with the fixed cutter is in `entry11.md`.
