# v2 pre-registration

Status: written 2026-10-09 on branch `v2`, before any v2 final run. Every entry here enters the
`frozen-v2` tag. Entries are added before the run they govern and never edited after it; a later
change is a new, dated entry that says what it replaces and why.

## 1. EM language-selection rule (Tasks C and D)

**Declaration.** For v2 final runs, the primary EM solver is the **revised selection rule**
(`knight2006_em`, `rule = "revised"`). The **original rule** (`knight2006_em_original`) is reported
beside it as secondary in every table where EM appears. The v1 paper is unchanged: there the original
rule stays primary.

**What the two rules are** (code unchanged since `frozen-v1`, `src/ibdb/methods/decipher.py`):
- Original: the pooled rare-unit state (OTHER) has learned emissions and unpinned mass, and the
  candidate language is chosen by raw log-likelihood per sign bigram.
- Revised: OTHER emits uniformly and its mass is pinned at 3% for every reference, and the candidate
  is chosen by the gain over a unigram-only model of the same reference, divided by the reference's
  own bigram mutual information.

**Reason.** The original rule's choice is dominated by one reference language, Sumerian, whatever the
hidden language is:
- **v1 main runs, `candidates` tier, all language corpora:** it picks Sumerian for 91% of corpora
  (652/720, sampler A) and 71% (299/420, sampler B). The revised rule picks Sumerian for 0% and 1%.
- **Ugaritic-Hebrew anchor (`reports/v2/ugaritic/results.md`):** in `candidates` (Hebrew plus the
  five v1 languages) the original rule picks Sumerian in all 5 conditions and scores 0% on Task D. The
  revised rule picks Hebrew in all 5 and scores 25-32% of tokens.

**Known weakness of the revised rule, stated now so it cannot be discovered later and explained away.**
It is not unbiased: in v1 sampler A it picks Latin for 58% of corpora (416/720) and Finnish for 33%.
It picks the true sister more often than the original rule (36% vs 28% of corpora, sampler A; 57% vs
47%, sampler B), but far from always. v2 reports which reference each rule picks, by hidden language,
beside every Task C rate.

**Status of the evidence.** The revised rule was written during v1 development after the original
rule was seen to pick Sumerian for almost every corpus (v1 paper, Section 3.7). It is therefore post hoc with
respect to v1. The Ugaritic anchor is the first data it had not been tuned on, and there it picked the
right language in every condition. That is one real case, not a validation.

**What this does not change.** Task D scores stay "before the cognate step". Thresholds (50% of
tokens) and tiers are unchanged. No other method parameter changes.

## 2. Task D scoring with a realistic sister (sister-v4)

Declared 2026-10-09, before sister-v4 is built (plan: `docs/v2_sister_plan.md`).

**Why a new scorer.** v1 scored "before the cognate step" by inverting the sister-to-hidden table,
which was one-to-one. Sister-v4 has mergers (several hidden sounds share one sister sound) and
context-dependent changes (one hidden sound has several sister sounds), so that inversion is no
longer defined.

**Gold values.** The generator records, for each hidden unit, its **regular reflex**: the sister unit
it becomes where no context-dependent rule applies. It also records every **attested reflex**: each
sister unit the hidden unit actually becomes somewhere in the sister text. Units are scored at the
script's unit level (phoneme, syllable or word form).

**Primary: strict score.** A sign token counts as correct when the solver's predicted sister unit is
the regular reflex of that token's hidden value. Several signs mapped to one sister unit all count
(many-to-one accepted). Reflexes produced by context-dependent rules count as wrong.

**Secondary: lenient score.** As strict, but a prediction counts as correct when it is any attested
reflex of the token's hidden value.

**Unchanged from v1.**
- Every token counts. Units with no sister counterpart (word dividers, determinatives) are
  unrecoverable.
- The 50% token threshold.
- Score labels: both scores are "before the cognate step". The solver is never given the
  correspondence table.

**Scope.** This scorer is used for sister-v4 runs only. Runs with the v1 sister keep the v1 scorer, so
v1 numbers stay comparable. The Ugaritic anchor already scores this way (gold = the regular Hebrew
correspondent, many-to-one accepted); it has no attested-reflex list, so it reports the strict score
only.

## 3. Sister-v4 targets corrected for Hebrew spelling (POST HOC amendment)

Declared 2026-10-10, before any new grid run and before the corrected targets below are measured
with this method. **This entry is post hoc.** It was written after the calibration against the
targets of the sister plan failed (`reports/v2/sister/yardsticks.md`: no language matched in either
setting), and after an approximate exploratory check had suggested why
(`reports/v2/ugaritic/orthography_check.md`: about 0.09 bits and 58%). Those approximate values are
not used. The original targets and their failure stay on record and are reported first.

**Reason.** The original targets measured Ugaritic against Hebrew *as written*. Masoretic spelling
writes many vowels with the letters ו, י and ה (matres lectionis); Ugaritic spelling does not. So
part of the Ugaritic-Hebrew distance was a difference in spelling conventions, not in language. Our
synthetic hidden languages and sisters share one spelling convention (all phonemes written), so the
spelling component should not be in their target. The corrected targets aim to measure language
distance only.

**Method for removing vowel letters (fixed now).** It works per word, on the OSHB pointed text as
written (ketiv letters with the pointing OSHB gives them), with accents ignored. A letter is removed
as a vowel letter when:
1. **ו holam male:** ו carries holam U+05B9 and the preceding letter has no vowel point. (Consonantal
   ו with an o-vowel is encoded with U+05BA, holam haser for vav, and is kept.)
2. **ו shureq:** ו carries only a dagesh (U+05BC), is not the first letter of the word, and the
   preceding letter has no vowel point. Word-initial וּ (the conjunction) is kept, because Ugaritic
   writes the conjunction w.
3. **י after i/e vowels:** י carries no point of its own and no dagesh, and the preceding letter has
   hiriq, tsere or segol.
4. **Final ה:** the last letter of the word is ה without mappiq (dagesh), and the preceding letter has
   qamets, segol, tsere or holam.

Kept in all cases: א (quiescent aleph is etymologically consonantal and is written in Ugaritic too),
ו and י with their own vowel or dagesh-plus-vowel, and every other letter. Shin and sin stay
collapsed and final forms stay folded, as in the anchor.

**Measurement.** Every Ugaritic-Hebrew yardstick is recomputed with the shared code against the
vowel-letter-removed Hebrew, for the text, the word types and the word pairs. Uncertainty is reported
two ways:
- **Sampling:** a bootstrap over Ugaritic texts (readable segments, resampled with replacement, 200
  replicates; word and word-pair statistics recomputed from the resampled segments' tablet lines).
  The 95% interval is reported.
- **Method:** three rule variants, each changing one choice: (a) also remove quiescent א; (b) keep
  final ה; (c) treat word-initial וּ as a vowel letter. The range over the variants is reported.

**Corrected targets.**
- `close`: the point estimates of the main method.
- `distant`: twice the JSD above floor, half the chance-corrected shared word forms and word pairs.
  This is still a guess, not a measurement.
- Tolerance half-widths are the original ones (JSD 0.04 for `close`, 0.06 for `distant`; word forms
  0.10; word pairs 0.10), or half the width of the bootstrap 95% interval if that is larger.
- Verbatim (6+ letters) stays a constraint: at most 2%, or the upper bootstrap bound if that is higher.

**Sister source text: contiguous blocks (tested before the grid).**
- The hidden half and the sister half are cut from the source text in contiguous blocks of
  consecutive clauses, assigned to the two halves by a hash of the block index. This stands in for
  "different works": a real relative's texts are different texts, so they share fewer formulaic
  phrases.
- Block sizes tested: 250, 1,000 and 4,000 clauses, plus a plain two-way split (first half, second
  half).
- Test: the v1-like sister and one fixed mid-grid setting (n_cond 4, affix 0.5, lexical 0.35, word
  order 0.5, final-vowel loss 0.3), on seeds 90-91. Verbatim overlap and the other yardsticks are
  reported for every block size.
- Rule: use the largest block size for which each half keeps at least 40% of the source's clauses
  and at least 40% of its word types. If blocks still share formulaic phrases (verbatim
  above the constraint for the v1-like sister), that is recorded as a limitation.
- Hidden corpora for sister-v4 runs are then generated from the hidden blocks (a new split version,
  "v4"). The v1 splits are unchanged for v1 runs.

**Grid and selection.** These are unchanged from the sister plan: the same knobs, the same selection
rule with the corrected targets, dev seeds 90-91 only, then held-out seeds 0-2 with nothing changed.

**Three tiers in v2 `related` and `candidates` results, always reported side by side:**
1. **`harsh`** (lower bound): the settings chosen against the original targets (option A,
   `reports/v2/sister/calibration.json`), which keep 2-8% of shared word forms. For Sumerian, which
   had no grid point at or below 2% verbatim, `harsh` is the grid point with the lowest verbatim (ties
   by loss), measured on the clause split it was calibrated with.
2. **`close`** (corrected, primary): the corrected targets above.
3. **`distant`** (corrected, sensitivity): as above.

**What stays first.** The sister report opens with the original calibration failure.

## 4. v2 `related` tier: a bracket instead of a calibrated sister

Declared 2026-10-11, before any v2 Task C/D run. Synthetic-sister calibration was killed after both
the original and the corrected calibration failed (`docs/v2_negative_results.md`, item 2). This
entry replaces the three tiers of entry 3.

**v2 `related` and `candidates` results report, side by side:**
1. **Upper bound: the v1 sister** (sister-v2 content split; as in the v1 paper). It is closer than any
   real relative (shared word forms 48-76%, verbatim 10-38% by the shared yardsticks). It is scored
   with the v1 scorer.
2. **Lower bound: `harsh`** (sister-v4 with the settings chosen against the original targets, content
   split; `reports/v2/sister/harsh.json`). It keeps 4-8% of shared word forms, harsher than
   Ugaritic-Hebrew, and is scored with the entry 2 scorer (strict primary, lenient secondary).
3. **Beside both: the Ugaritic-Hebrew yardsticks**, as written and with vowel letters removed, and the
   Ugaritic Task D result (33.9%), so readers can place a real relative between the bounds.

The corrected `close` and `distant` settings of entry 3 are not used. Real relatives from different
texts (roadmap rank 6b) will be added as a separate tier by their own pre-registration entry, if
that plan is approved.
