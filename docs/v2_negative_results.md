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
