# Unit-frequency agreement against Task D (exploratory, post hoc)

Added 2026-10-21. Tests the first reason offered (untested) in `docs/v2_negative_results.md`, item 3. Alphabetic level: the hidden half mapped forward through the gold regular reflexes, against the relative's text (`harsh`: seed 0). Lower JSD and higher rank correlation mean closer unit frequencies. Task D: primary table (`results.md`), revised EM, related tier, alphabetic, seeds 0-2.

| Hidden | Relative | Unigram JSD (bits) | Spearman rank correlation | Top 6 units, hidden mapped | Top 6 units, relative | Task D alphabetic |
|---|---|---|---|---|---|---|
| latin | italian | 0.026 | 0.85 | e i s t a r | e a i o n r | 16.9 |
| latin | harsh | 0.059 | 0.79 | n e i s f au | n i e f l a | 36.1 |
| tamil | malayalam | 0.040 | 0.89 | a u i n k t | a n t m u ā | 30.4 |
| tamil | kannada | 0.062 | 0.97 | a u i n k t | a t i u n k | 32.2 |
| tamil | harsh | 0.073 | 0.80 | o t u r a n | r o t a u n | 16.4 |

**Reading.** Italian agrees with Latin in unit frequencies better than `harsh` does (lower JSD, higher rank correlation), yet scores lower on Task D. Unigram frequency agreement therefore does not explain the bracket failure for Latin. For Old Tamil the two measures disagree (Malayalam is closer by JSD, Kannada by rank order) while Task D is level for the two relatives. Three points per hidden language; nothing is tested.
