# v2 negative results

## 1. Allograph merging (roadmap rank 1) — shelved 2026-10-09

**Method.** `src/ibdb/methods/allograph.py` (`AllographMerger`), a v2 method that is not part of
`frozen-v1` and is not to be included in `frozen-v2` as it stands. It merges a rarer sign into the
more frequent sign with the most similar left and right neighbours when two conditions hold:
- the rarer sign's neighbour counts pass a parametric-bootstrap homogeneity test;
- the best match stands out (Jensen-Shannon divergence at most 0.6 times the median).

It never reads the answer key. Its parameters were fixed on development corpora (seeds 90-91) before
the sweep was scored: `min_count=10, alpha=0.05, max_ratio=0.6`. Commit `be22aed`; development grids
are in `reports/v2/allograph/dev.md` and `dev2.md`.

**Test.** All 1,451 valid corpora of the `sensitivity_sister_v2` sweep were rebuilt exactly; all
1,451 regenerated corpora and all recomputed no-merge scores match the stored ones. The frozen
original-rule EM (primary score, before the cognate step) was then run three ways:
- with no merging;
- with the learned merger;
- with an oracle merge of the hidden allograph groups.

Full tables: `reports/v2/allograph/sweep.md` (commit `c400d21`).

**Results.**
- **Merge accuracy:** precision 0.74-0.80 by inventory and recall 0.17 at 400 signs falling to 0.05
  at 800. By script type, precision is 0.64 for logo-syllabic and up to 0.87 for alphabetic. Wrong
  merges join signs with different values.
- **Task D:** learned merging changes mean recovery by 0.1-0.3 points. Per corpus it is better in 401
  cases, worse in 412 and equal in 638 (`candidates` tier); the `none` tier is similar.
- **Oracle bound:** perfect merging adds about 0.7 points on average. On matched corpora it goes
  from 3.1% to 4.7% at 400 signs, and adds nothing at 800 signs (2.4% either way).

**Why even the oracle gains little at high inventories: hidden duplication.** The sweep raises
inventory by adding allographs, and allographs disguise repeated texts as distinct ones. After oracle
merging, the true duplicate rate at 800 signs is 6-15 points higher than at 400 signs for the same
nominal duplicate setting; one Sanskrit syllabic example is 0.20 against 0.05. The inventory axis
therefore partly measures how much distinct text a corpus holds. This was added to the v1 paper as
a caveat (Section 3.9, limitation 1, Appendix A entry 29; `main` commit 3f01abf).

**Why shelved.**
- A Task D gain would need much higher recall at the same precision.
- Our generator's free-variation allographs are the easiest case for a distributional merger, so
  real-data performance would likely be lower.
- The oracle bound shows little is available to gain on these corpora anyway.

**What could revive it.**
- A merger evaluated on real allograph data, such as a sign list with variant annotations under an
  open licence.
- A generator in which the inventory is raised without disguising duplicates, so that the inventory
  effect can be separated from the duplication effect.

## 2. Synthetic-sister calibration (roadmap rank 6) — killed 2026-10-11

**What was tried.** Sister-v4 (`src/ibdb/sister_v4.py`) adds to the v1 sister several mechanisms:
- mergers (24% of consonants);
- context-dependent sound changes;
- final-vowel loss;
- affix replacement;
- word-order changes.

It was calibrated to the distance between Ugaritic and Hebrew, measured with the same code
(`src/ibdb/yardsticks.py`). Two settings were tried: `close` (the Ugaritic-Hebrew values) and
`distant` (twice the distance). Each calibration was a grid of 1,080 settings per language on dev
seeds 90-91, then a check on held-out seeds 0-2. Plan: `docs/v2_sister_plan.md`; pre-registration
entries 2 and 3.

**Results** (`reports/v2/sister/yardsticks.md`):
1. **Original targets** (Hebrew as written: JSD above floor 0.166, shared word forms 47%, verbatim
   at most 2%): 0 of 5 languages matched in either setting. Sumerian had no setting at or below 2%
   verbatim.
2. **Corrected targets** (entry 3, post hoc; Hebrew vowel letters removed: JSD 0.089, shared forms
   58%, word pairs 4.6%; contiguous-block split): 0 of 5 matched in either setting. Sumerian again had
   no setting at or below 2% verbatim. For Sanskrit and Finnish the closest `close` and `distant`
   settings were the same grid point.

**Why it fails.**
- **Every mechanism that changes letter pairs also changes words.** Over the whole grid, at the
  lowest accepted JSD (0.049) the best chance-corrected shared word forms were 32-43% for four of the
  five languages, against a floor of 48%. Only Sumerian (63%) reached it.
- **Verbatim text is the binding constraint.** A sister cut from the same source text shares its
  formulaic phrases. Settings that keep shared forms near the target leave 10-21% verbatim; the only
  settings at or below 2% keep 4-13% of shared forms. Contiguous blocks instead of clause-level
  splits barely help: verbatim for the v1-like sister stays at 10-39%.

**Findings kept.**
- **Spelling inflates the Ugaritic-Hebrew distance.** Removing Hebrew vowel letters (matres
  lectionis; method in entry 3) cuts the letter-pair distance above floor from 0.166 to 0.089 bits
  (rule variants 0.084-0.106), and raises chance-corrected shared word forms from 47% to 58%.
  About half the measured distance was spelling, not language.
- **Low verbatim overlap between a real pair is about different texts, not spelling.** It stays at
  0.8% with or without vowel letters (`reports/v2/sister/anchor_corrected.md`).
- **A real relative differs from a resampled sister in what is written, not only in how.** No
  sound-change or morphology mechanism applied to the same text reproduced that.

**What replaces it.**
- **v2 `related` tier:** a bracket (pre-registration entry 4), with the v1 sister as the upper bound,
  `harsh` as the lower bound, and the Ugaritic-Hebrew yardsticks beside both. The corrected `close`
  and `distant` settings are not used.
- **Roadmap rank 6b:** real related languages written in different texts.

**What could revive it.** A mechanism that changes word frequencies and phrasing without destroying
word forms (e.g. genre shift). It was not tried, to stop revising targets after seeing results.
