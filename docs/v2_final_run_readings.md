# v2 final run (seeds 6-11): hypotheses, metrics, thresholds and table layouts

Written 2026-10-27, before any seed 6-11 corpus is generated, as decision 4 of the approved freeze plan
(`docs/v2_freeze_and_final_run_PROPOSAL.md`). Declared by pre-registration entry 12 and frozen with the
code by the tag `frozen-v2.1`. Nothing here may change after the tag; anything added later is a dated,
labelled entry and is reported as post hoc.

Seeds 0-5 are the **development set**: every reading below was formed on them. Seeds 6-11 are the
**confirmatory set**: no v2 code has generated them (checked: no record in `runs/results/` and no
archive in `reports/v2/cd/records/` has a seed above 5 other than development seed 90).

## 1. What runs

| Item | Fixed value |
|---|---|
| Code | the commit tagged `frozen-v2.1` (entries 1-12); `scripts/v2/final_v2.py` refuses to run unless every file outside `reports/` and `docs/` equals the tag, with no untracked code files |
| Corpora | Indus point (2,906 texts, mean length 4.6), regime `full`; sampler A (generator v1) and sampler B (generator v2); seeds 6, 7, 8, 9, 10, 11; five hidden languages (Sanskrit, Old Tamil, Sumerian, Latin, Finnish); four script types: **240 corpora** |
| Real relatives (`related_real`, `candidates_real`) | Latin: Italian (descendant). Old Tamil: Malayalam (descendant), Kannada (sister). Finnish: Estonian (sister; **weak gold: 10 word pairs, 13 of 27 letters**). Normalised spelling; gold as committed; entry-10 scorer; entry-11 cutter. **No Pali** unless SuttaCentral's permission is recorded in a dated entry before the tag (not the case on 2026-10-27) |
| Synthetic optimistic upper references | `harsh` (sister-v4, `reports/v2/sister/harsh.json`), all five languages, entry-2 scorer; the v1 sister (sister-v2 content split), all five languages, run with the frozen v1 `evaluate.run_job` on the same corpora, scored before the cognate step as in entries 4-7 |
| Sumerian | `harsh` and the v1 sister only (an isolate: no real relative) |
| Methods | revised EM (primary), original EM, frequency-rank baseline; 3 restarts, 60 iterations (as entry 6) |
| Controls | C1 unrelated references (Latin: Old Tamil, Finnish; Old Tamil: Latin, Finnish; Finnish: Latin, Old Tamil; revised EM and frequency rank), scored against each real relative's gold; C2 floors; C3 revised EM with 10 restarts, `related_real`, every real relative, **seeds 6-8**; C4 determinism (section 5) |
| Ceilings | per corpus and real relative: **reachable** (primary, entry 11) and raw (entry 2, with entry 10) |
| Records | `runs/results/v2_final/`: `records.jsonl`, `predictions.jsonl` (every solver call), `v1_sister.jsonl`; archived gzipped with SHA-256 in `reports/v2/final/records/` after the run |
| Yardsticks | not rerun: they depend on no seed, and entries 10-11 already fixed their values (`reports/v2/real_relatives/`) |

**Errors.** A corpus that raises an error is recorded with its traceback. After the main run, errored
corpora are retried once on the same code. A corpus that fails twice is reported as missing, as a
process failure, and every cell is computed on the corpora that exist, with n shown. Nothing is rerun
for any other reason.

## 2. Primary metric and summary statistics

- **Primary metric:** revised EM, strict score (entry 2 with entry 10), `related` tier, % of sign
  tokens, before the cognate step.
- **Cell:** one relative (or synthetic reference) and one script type; its value is the mean over its
  **12 corpora** (6 seeds x 2 samplers). There are 16 real-relative cells (4 relatives x 4 script types).
- **Intervals:** 95% bootstrap over corpora, 2,000 resamples, generator seed 2026 (as entries 7-10);
  descriptive only. **No hypothesis test is made and no correction for multiple readings is applied:**
  each reading is a threshold on a mean or a count, stated in advance.
- Secondary: original EM, frequency rank, lenient score, Task C family correctness; reported, no readings.

## 3. Confirmatory readings (each met or not met)

The development answer is given for each. A reading is **met** if the seed 6-11 value satisfies the
stated condition; otherwise **not met**. No reading is re-defined after the run.

| ID | Reading (seeds 6-11) | Threshold | Development answer (seeds 0-5) |
|---|---|---|---|
| H1 | Every real-relative cell mean is below 50% | 16 of 16 cells < 50.0 | met: highest 34.4 (Kannada, alphabetic) |
| H2a | Estonian **measurably helps** on alphabetic scripts (C1 rule) | added value >= 5.0 points **and** ahead of the better unrelated reference in >= 9 of 12 paired corpora | met: +20.1; 11 of 12 |
| H2b | Kannada measurably helps on alphabetic scripts | as H2a | met: +15.1; 9 of 12 |
| H3 | On syllabic and logo-syllabic scripts, a real relative measurably helps in **at most 1** of the 8 cells | count of 8 cells meeting the C1 rule <= 1 | met: 1 (Malayalam, syllabic, +7.6; 10 of 12) |
| H4 | Every real relative scores below the v1 sister on the same corpora, in each syllabic, logo-syllabic and alphabetic cell | 12 of 12 cells: real mean < v1-sister mean | met: 12 of 12 |
| H5 (R2) | Old Tamil alphabetic with Malayalam and with Kannada both within 10 points of the Ugaritic result (32.0%) | both means in 22.0-42.0 | met: 30.5 and 34.4 |
| H6 (R3) | Italian below `harsh` on alphabetic and on syllabic scripts | both cells: Italian mean < `harsh` mean | met: 20.3 < 31.5; 4.2 < 16.9 |
| H7 (R4) | In `candidates_real`, revised EM picks the real relative in fewer than half of its 48 corpora, for Italian, Malayalam and Kannada | each count <= 23 of 48 | met (seeds 0-5): Italian 12, Malayalam 0, Kannada 19 of 48 |
| H8 (C4) | Determinism | every compared value identical (section 5) | met: 120 of 120 (entry 8); 3,348 of 3,348 (entry 10) |

*Measurably helps* (entry 8): the relative's cell mean minus the higher of the two unrelated-reference
means on the same corpora and gold is at least 5 points, and the relative's score is higher than that
unrelated reference's in at least 9 of the 12 paired corpora (ties count as not higher).

**What would count against the current picture:** H1 not met (a real relative at or above 50% on
average); H2a or H2b not met (the alphabetic help disappears); H3 not met (help on the script types
closest to Indus); H4 not met (a real relative as good as the optimistic synthetic one).

The development answers for H7 count seeds 0-5 together (48 corpora per relative: 6+6 for Italian,
0+0 for Malayalam, 9+10 for Kannada); entry 7 evaluated R4 on seeds 3-5 alone.

## 4. Descriptive readings (reported, no threshold)

| ID | Reading | Development answer |
|---|---|---|
| D1 | At the floor (C2): cell mean no more than 2 points above the mean constant-prediction floor | at the floor: every logographic cell; Italian syllabic and logo-syllabic; Kannada syllabic and logo-syllabic; Estonian syllabic and logo-syllabic. Above: every alphabetic cell; Malayalam syllabic and logo-syllabic |
| D2 | C1 "measurably helps" in each of the 16 cells (H2-H3 use 10 of them) | helps: Estonian alphabetic, Kannada alphabetic, Malayalam syllabic; no elsewhere |
| D3 | Real relative minus `harsh`, each cell | below `harsh` on alphabetic: Italian (-11.2 pooled), Estonian (-10.1 pooled); above: Malayalam (+17.6), Kannada (+21.5) |
| D4 | Estonian picked in `candidates_real:estonian` | 29 of 48 (15 + 14), more than half |
| D5 | C3: budget first-order (10-restart mean differs from 3-restart mean by more than 10 points), each real-relative cell, seeds 6-8 | first-order in 1 of 12 cells run (Malayalam alphabetic, +11.5); none for Italian or Kannada; Estonian not run |
| D6 | Ceilings: reachable (primary) and raw, each real-relative cell | logographic reachable 2.3-25.4; syllabic 82.9-100.0 |
| D7 | Synthetic references for all five languages (`harsh`, v1 sister), `related` and `candidates` | `pooled.md` |
| D8 | Number of corpora per cell at or above 50% | `pooled.md` |

The cutter changed in entry 11 for six cells (Estonian, Malayalam, Kannada; syllabic and logo-syllabic).
Their development answers come from runs with the old cutter; `reports/v2/cd/entry11.md` shows the
fixed cutter on seeds 0-2.

## 5. C4: determinism

After the main run, the full per-corpus job is run a second time, on the same frozen code, for 24
corpora: Latin, Old Tamil and Finnish, four script types, samplers A and B, seed 6. Every numeric value
in the two records (every tier, method and score; floors; unrelated-reference scores; ceilings; the
v1-sister scores; C3 where present) is compared for exact equality. H8 is met only if all are equal.

## 6. Agreement with the development seeds

For H1-H7 and for each cell of D1-D3: the development answer (sections 3-4), the seed 6-11 answer, and
whether they agree. Disagreements are reported, not resolved, and nothing is pooled across the two sets.

## 7. Report order and table layouts (Monday 2026-11-02)

The report `reports/v2/final/results.md` is generated by `reports/v2/final/analysis/final_summary.py`
(committed with the tag) and contains, in this order:

1. **Readings not met**, each with its value, its threshold and its development answer. Then **process
   failures**: missing corpora, errors, C4 mismatches. If there are none, the section says so.
2. **Readings met**, same columns.
3. **Table T1, readings:** `| ID | Reading | Threshold | Seeds 6-11 value | Met? | Development answer | Agrees? |`
4. **Table T2, Task D per pair** (one block per real relative, in the format of
   `reports/v2/cd/estonian.md`): `| Relative | Script | Revised EM mean [95% CI] | Corpora >= 50% |
   Original EM | Frequency rank | Lenient | Reachable ceiling (primary) | Raw ceiling | harsh | v1 sister |`
5. **Table T3, controls per pair:** `| Relative | Script | Floor (C2) | At the floor? (gap) | Better
   unrelated ref., mean | Added value; paired wins | Measurably helps? | Minus harsh | Minus v1 sister |
   Picks the relative (of 12) |`
6. **Table T4, synthetic references, all five languages:** `| Hidden | Reference | logographic |
   syllabic | logo-syllabic | alphabetic |` for `harsh` and the v1 sister, `related` and `candidates`
   (mean [95% CI], n).
7. **Table T5, Task C:** per relative, the references chosen by revised EM in `candidates_real`, and
   family correctness for all three methods.
8. **Table T6, C3 (seeds 6-8):** `| Relative | Script | 3 restarts | 10 restarts | Difference | First-order? |`
9. **Table T7, agreement with development seeds** (section 6).

Every Finnish-Estonian row is labelled "weak gold: 10 word pairs, 13 of 27 letters". The synthetic
references are labelled "optimistic upper reference". Cross-script comparisons, including with
Ugaritic-Hebrew, are indicative only. No result is written into the paper before the project owner
has seen this report.
