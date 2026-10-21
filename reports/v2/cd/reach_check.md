# How much of the strict ceiling can the solver reach? (exploratory, post hoc)

Added 2026-10-21. The entry-2 ceiling counts a sign token as recoverable when its regular reflex occurs anywhere in the relative. The frozen EM solver predicts only among the reference's 250 most frequent units, so a reflex outside them can never be predicted. *Reachable* is the share of tokens whose reflex is among those units. Mean over 12 corpora (seeds 0-5, samplers A and B); no solver is run.

| Relative | Script | Ceiling (entry 2) | Reachable by the solver |
|---|---|---|---|
| Italian | logographic | 51.4 | 25.4 |
| Italian | syllabic | 100.0 | 100.0 |
| Italian | logosyllabic | 80.1 | 69.1 |
| Italian | alphabetic | 99.1 | 99.1 |
| Kannada | logographic | 24.3 | 2.3 |
| Kannada | syllabic | 100.0 | 95.2 |
| Kannada | logosyllabic | 72.8 | 66.3 |
| Kannada | alphabetic | 100.0 | 97.7 |
| Malayalam | logographic | 16.9 | 10.1 |
| Malayalam | syllabic | 100.0 | 99.9 |
| Malayalam | logosyllabic | 73.2 | 69.5 |
| Malayalam | alphabetic | 100.0 | 100.0 |

**Reading.** Where *reachable* is far below the ceiling, the solver's unit cap, not only the relative, limits the score: the hidden language's frequent words have cognates in the relative, but those cognates are rare there. Example (checked 2026-10-21): Latin *et* is 19.3% of the sign tokens of the seed-0, sampler-A logographic corpus, and its reflex *et* occurs in Dante, so it counts as recoverable; but it occurs only 4 times there (rank 2,592), while Italian *e* is rank 1. The logographic ceilings in entry 2 therefore overstate what this solver could reach.
