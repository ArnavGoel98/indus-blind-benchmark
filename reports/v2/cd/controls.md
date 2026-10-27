# v2 Task D controls (pre-registration entry 8)

Post hoc in motivation, pre-registered in procedure; readings fixed in entry 8 before the run. Revised EM, strict score, % of sign tokens, `related` tier. Corpora: Latin and Old Tamil, four script types, seeds 0-5, samplers A and B (C3 and C4: seeds 0-2). Code: `reports/v2/cd/analysis/controls.py` (frozen functions only). Entry 10: Old Tamil values use the entry-10 rule (a no-source gold row is unknown, not lost; old values in `entry10.md`); C4 compares the records as originally run.

## C1. Does the real relative beat an unrelated reference scored against the same gold?

The unrelated reference is a v1 language given as the only reference; its predictions are scored against the real relative's gold, exactly as the relative's own run. *Helps* = added value at least 5 points and the relative ahead of the better unrelated reference in at least 9 of the 12 paired corpora.

| Relative | Script | Relative | Unrelated: first / second | Added value | Corpora ahead | Reading |
|---|---|---|---|---|---|---|
| Malayalam (Old Tamil) | logographic | 0.0 | Latin 0.0 / Finnish 0.0 | +0.0 | 0 of 12 | no measurable help |
| Malayalam (Old Tamil) | syllabic | 10.7 | Latin 3.1 / Finnish 2.5 | +7.6 | 10 of 12 | helps |
| Malayalam (Old Tamil) | logosyllabic | 6.6 | Latin 2.2 / Finnish 2.3 | +4.3 | 10 of 12 | no measurable help |
| Malayalam (Old Tamil) | alphabetic | 30.5 | Latin 5.7 / Finnish 19.7 | +10.7 | 7 of 12 | no measurable help |
| Kannada (Old Tamil) | logographic | 0.0 | Latin 0.0 / Finnish 0.0 | +0.0 | 2 of 12 | no measurable help |
| Kannada (Old Tamil) | syllabic | 4.0 | Latin 3.1 / Finnish 2.5 | +0.9 | 8 of 12 | no measurable help |
| Kannada (Old Tamil) | logosyllabic | 3.9 | Latin 2.2 / Finnish 2.2 | +1.7 | 9 of 12 | no measurable help |
| Kannada (Old Tamil) | alphabetic | 34.4 | Latin 5.4 / Finnish 19.4 | +15.1 | 9 of 12 | helps |
| Italian (Latin) | logographic | 0.0 | Old Tamil 0.0 / Finnish 0.0 | +0.0 | 1 of 12 | no measurable help |
| Italian (Latin) | syllabic | 4.2 | Old Tamil 1.3 / Finnish 5.4 | -1.2 | 5 of 12 | no measurable help |
| Italian (Latin) | logosyllabic | 2.3 | Old Tamil 0.7 / Finnish 2.5 | -0.2 | 4 of 12 | no measurable help |
| Italian (Latin) | alphabetic | 20.3 | Old Tamil 4.1 / Finnish 14.0 | +6.3 | 6 of 12 | no measurable help |

## C2. Constant-prediction floor

Strict score of the best single-unit answer (every sign mapped to the most common regular reflex), mean over corpora. *At the floor* = the relative's mean is no more than 2 points above it.

| Relative | Script | Floor | Relative | Reading |
|---|---|---|---|---|
| Malayalam (Old Tamil) | logographic | 8.6 | 0.0 | at the floor |
| Malayalam (Old Tamil) | syllabic | 6.2 | 10.7 | above the floor |
| Malayalam (Old Tamil) | logosyllabic | 3.6 | 6.6 | above the floor |
| Malayalam (Old Tamil) | alphabetic | 15.8 | 30.5 | above the floor |
| Kannada (Old Tamil) | logographic | 17.5 | 0.0 | at the floor |
| Kannada (Old Tamil) | syllabic | 6.2 | 4.0 | at the floor |
| Kannada (Old Tamil) | logosyllabic | 3.5 | 3.9 | at the floor |
| Kannada (Old Tamil) | alphabetic | 14.2 | 34.4 | above the floor |
| Italian (Latin) | logographic | 14.4 | 0.0 | at the floor |
| Italian (Latin) | syllabic | 10.3 | 4.2 | at the floor |
| Italian (Latin) | logosyllabic | 8.4 | 2.3 | at the floor |
| Italian (Latin) | alphabetic | 14.2 | 20.3 | above the floor |

## C3. Solver budget: 10 EM restarts against 3 (seeds 0-2)

The first three restarts are identical; the best likelihood is kept. *First-order* = the mean moves by more than 10 points.

| Hidden | Tier | Script | 3 restarts | 10 restarts | Change | Corpora changed | Reading |
|---|---|---|---|---|---|---|---|
| Old Tamil | malayalam | logographic | 0.0 | 0.0 | +0.0 | 0 of 6 | second-order |
| Old Tamil | malayalam | syllabic | 6.2 | 8.4 | +2.2 | 3 of 6 | second-order |
| Old Tamil | malayalam | logosyllabic | 5.9 | 8.7 | +2.8 | 5 of 6 | second-order |
| Old Tamil | malayalam | alphabetic | 30.4 | 41.9 | +11.5 | 5 of 6 | first-order |
| Old Tamil | kannada | logographic | 0.0 | 0.0 | -0.0 | 2 of 6 | second-order |
| Old Tamil | kannada | syllabic | 3.3 | 3.0 | -0.3 | 2 of 6 | second-order |
| Old Tamil | kannada | logosyllabic | 2.9 | 2.6 | -0.3 | 2 of 6 | second-order |
| Old Tamil | kannada | alphabetic | 32.2 | 28.9 | -3.3 | 4 of 6 | second-order |
| Old Tamil | harsh | logographic | 0.1 | 0.0 | -0.1 | 1 of 6 | second-order |
| Old Tamil | harsh | syllabic | 6.2 | 7.9 | +1.7 | 4 of 6 | second-order |
| Old Tamil | harsh | logosyllabic | 5.9 | 4.3 | -1.6 | 5 of 6 | second-order |
| Old Tamil | harsh | alphabetic | 16.4 | 14.0 | -2.4 | 3 of 6 | second-order |
| Latin | italian | logographic | 0.0 | 0.1 | +0.1 | 2 of 6 | second-order |
| Latin | italian | syllabic | 6.0 | 1.3 | -4.6 | 4 of 6 | second-order |
| Latin | italian | logosyllabic | 1.5 | 2.9 | +1.3 | 3 of 6 | second-order |
| Latin | italian | alphabetic | 16.9 | 18.1 | +1.3 | 3 of 6 | second-order |
| Latin | harsh | logographic | 1.5 | 1.8 | +0.3 | 2 of 6 | second-order |
| Latin | harsh | syllabic | 24.4 | 29.4 | +5.0 | 2 of 6 | second-order |
| Latin | harsh | logosyllabic | 4.6 | 2.9 | -1.7 | 2 of 6 | second-order |
| Latin | harsh | alphabetic | 36.1 | 43.6 | +7.5 | 5 of 6 | second-order |

## C4. Determinism

The 3-restart rerun was compared with the frozen-run record for 120 corpus-tier pairs: all identical.

## Diagnostics

Mean share of sign tokens assigned to the single most common predicted unit (a degeneracy index; no threshold):

- Old Tamil: real relatives 12.4%, unrelated references 11.1%.
- Latin: real relatives 12.2%, unrelated references 11.2%.
