# Original vs revised EM selection rule: reanalysis (no new runs)

Sources: `reports/sensitivity/aggregate.json` (1,800-corpus sweep, generator-v1),
`reports/results`, `reports/replication/results`, `reports/generator_v2/results` (main run seeds 0-2,
fresh seeds 3-5, generator-v2), and the per-corpus records behind them. Methods are frozen at `frozen-v1`.
The **original** rule is the frozen pre-registration choice. The **revised** rule was adopted after the
original rule picked Sumerian for almost every corpus, so its numbers are post hoc.
Task D token accuracy throughout. "Box" = duplicates 0.2-0.4 by inventory 400-700.

## (a) Within-combination variation across the plausible box (box panel, 10 combinations)

| Rule | Tier | Median spread | Max spread (combination) | Mean spread [95% CI] | Spread >= 10 points | Sanskrit/syllabic |
|---|---|---|---|---|---|---|
| Original | candidates | 2.1 | 7.6 (Sumerian/alphabetic, 13.2 -> 20.8) | 2.7 [0.9, 4.9] | 0 of 10 | 0.0 -> 0.2 |
| Revised | candidates | 5.5 | 61.8 (Sanskrit/syllabic) | 15.4 [3.6, 31.4] | 4 of 10 | 13.0 -> 74.7 |
| Original | no relative | 1.2 | 3.0 | 1.2 [0.6, 2.0] | 0 of 10 | 0.0 -> 0.2 |
| Revised | no relative | 3.1 | 6.2 | 2.9 [1.6, 4.3] | 0 of 10 | 1.5 -> 4.6 |

Inside the box, the large within-combination swings are a revised-rule phenomenon. Under the original
rule the box is nearly flat. Across the WHOLE grid the original rule does move: the strict panel goes
from 0.2% to 20.5% and all corpora reach 14.5%, almost entirely in the corner with 0 duplicates and
400 signs, which lies outside the published range.

## (b) No related language: holds under both rules

| Run | Rule | Mean | Max cell mean | Max single corpus | Corpora >= 50% |
|---|---|---|---|---|---|
| Sweep, box panel | original / revised | 2.6-3.2 / 3.3-4.3 (cells) | 3.2 / 4.3 | - | 0 / 0 |
| Sweep, whole grid | original / revised | - | 4.6 / 7.1 | 24.6 / 27.9 | 0 of 1,571 / 0 of 1,571 |
| Main v1, Indus point | original / revised | 1.8 / 3.3 | - | 16.4 / 18.1 | 0 of 60 / 0 of 60 |
| Replication v1 | original / revised | 2.4 / 3.0 | - | 19.7 / 23.8 | 0 / 0 |
| Generator-v2 | original / revised | 3.3 / 4.8 | - | 23.2 / 27.6 | 0 / 0 |

Holds under both rules, both generators and fresh seeds: mean recovery stays at or below 4.8%, no cell
mean exceeds 7.1%, and no corpus reaches 50%. Individual corpora reach up to 28%, so "nothing works"
should be phrased in terms of means and the 50% threshold, not as zero.

## (c) Which headline claims are rule-independent?

| Claim | Rule-independent? | Evidence |
|---|---|---|
| Entropy statistics fail at Indus scale | **Yes** (no EM involved) | Task A only |
| No relative -> low recovery | **Yes** | Table (b) |
| Original rule <= ~5% inside the box | **Generator-v1 only** | Sweep box: original 3.5-5.1% (box panel), 2.2-5.2% (all corpora). But the 22 generator-v2 corpora that fall INSIDE the box (mean duplicates 0.25, inventory 428 overall) average **12.4%** under the original rule (one reaches 93%). |
| Difficulty depends on unconstrained corpus properties | **Direction: yes. Size within the v1 box: no.** | v1 -> v2 at the Indus point: original 2.1% -> 15.0%, revised 14.6% -> 42.7% (about 7x and 3x). Within the v1 box only the revised rule moves much (see (a)). |
| Corpus size barely helps | **v1: yes. v2: no.** | v1, 2,906 -> 50,000: original 2.1 -> 5.1, revised 14.6 -> 16.9. v2: original 15.0 -> 32.0, revised 42.7 -> 44.6. |
| Length effect is generator-dependent | **No: revised rule only** | Original: v1 2.1 -> 43.6 and v2 15.0 -> 50.1 (4.6 -> 20 signs), strong in both generators. Revised: v1 14.6 -> 43.8, v2 42.7 -> 48.5 (flat). Replication v1 matches (original 3.3 -> 45.0). |
| Seals-only (S) above tablets-only (T), prediction not measurement | **Direction: yes** | Original, all corpora: S 3.5-14.5% vs T 1.4-4.9%. Strict panel: S 0.7-20.5% vs T 0.1-1.4%. Revised: S 18.0-38.6% vs T 4.2-17.3%. Under the original rule, S is high only at 400 signs. |

**Plain summary.** Entropy failure and the no-relative floor do not depend on the rule. The
generator-dependence of difficulty holds in direction under both rules (v1 vs v2). The claim that
"the original rule never exceeds ~5% in the plausible box" is true only for generator-v1, and
generator-v2 corpora in the same box break it. Under the original rule, longer texts help strongly
in BOTH generators, so "the length effect is generator-dependent" is a revised-rule result.
