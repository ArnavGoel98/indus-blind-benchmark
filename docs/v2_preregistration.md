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

## 5. Real related languages (roadmap rank 6b)

Declared 2026-10-15, on approval of `docs/v2_real_relatives_plan.md` and before any download, parse or
measurement for it.

**Pairs, each labelled by relationship in every table:**

| Hidden | Relative | Relationship | Status |
|---|---|---|---|
| Finnish | Estonian | sister | first |
| Latin | Italian | descendant | first |
| Old Tamil | Malayalam | descendant (western Old Tamil dialect) | only after the Wikisource provenance check |
| Old Tamil | Kannada | sister | only after the Wikisource provenance check |
| Sanskrit | Pali | descendant | only if a source with clear terms is found: SuttaCentral permission, or a public-domain edition as the fallback |
| Sumerian | none (isolate) | - | `none` tier only |

**Fixed by this entry:**
- Sources, unit levels, normalisation rules and gold sources as in the plan at the commit adding
  this entry.
- **Measurements:** the Ugaritic-Hebrew yardsticks, as written and normalised (primary). No tuning,
  no targets. Sister pairs and descendant pairs are reported separately.
- **Gold tables:** written only from the named sources, with section or page per row. Rows the
  source does not cover are marked "no source" and are unrecoverable under strict scoring.
  Wikipedia is not used for any gold value.
- **Normalisation rules** are coded and tested before any yardstick is computed.

**Tasks C and D:**
- tiers `related_real` and `candidates_real`, beside the entry-4 bracket;
- the frozen methods (revised EM rule primary, original secondary, frequency-rank baseline beside
  them) and the entry-2 scorer;
- run only after the yardstick table has been reported.

**Pali fallback:** a public-domain edition (e.g. 19th-century Pali Text Society or Fausbøll
editions) whose transcription carries clear terms. A public-domain scan with an OCR or transcription
under non-commercial or unclear terms does not qualify.

## 6. Task C/D harness for entries 4 and 5 (implementation details)

Proposed 2026-10-17; declared 2026-10-18 on the project owner's instruction to proceed ("do what you
think is best"), before any v2 Task C/D final run, and tagged with `frozen-v2`. Written after a
pipeline check on development seed 90 only (sampler A, one EM restart; its numbers are not results
and are not reported). That check found one scorer error (Sumerian numerals and written determinatives
counted as unrecoverable), fixed before this declaration. It fixes what
entries 4 and 5 left to the implementation (`src/ibdb/relative_cd.py`, `scripts/v2/cd_v2.py`,
`scripts/v2/cd_v2_summary.py`). It replaces nothing.

**Corpora.** The v1 Indus-point corpora with the sister-v2 content split, i.e. those of profiles
`sister_v2_main` (sampler A) and `sister_v2_gen2` (sampler B): 2,906 texts, mean length 4.6, seeds
0-2, the four script types, regenerated from the same seeds (checked: identical corpus statistics).
The `harsh` tiers cover all five languages; the real tiers cover Latin (Italian) and Tamil (Malayalam,
Kannada), and Finnish (Estonian) once its gold table is committed.

**Upper bound.** The v1 sister rows are read from the existing `sister_v2_main` and `sister_v2_gen2`
records (frozen-v1 methods, same corpora), scored before the cognate step; they are not rerun.

**Reference units** (no reference carries a correspondence table):
- alphabetic: the relative's phonemes;
- syllabic: the v1 CV syllabifier (`phonology.syllabify`) with the hidden language's vowels. Sumerian's
  syllable units are sign readings, so for Sumerian (`harsh` only) the relative's syllables are found by
  greedy longest match against the hidden readings mapped through the regular reflexes, single
  phonemes otherwise;
- logographic: the relative's word forms;
- logo-syllabic: word forms for the relative's 250 most frequent word types (as v1 references),
  syllables otherwise;
- the relative text is used whole, up to 40,000 clauses (as v1 references).

**Scoring details (entry 2).**
- The regular reflex of a syllable is the reflexes of its phonemes joined, phonemes with no reflex
  dropped. A logogram's regular reflex is the relative word so formed, and only if that word occurs
  in the relative text. A token with no regular reflex is unrecoverable.
- Lenient: the prediction can be written as attested reflexes (regular included; empty where the
  regular reflex is none) of the hidden phonemes, in order. A logogram must also occur in the relative.
- Units the generator adds (word dividers, determinatives `<DET:n>`) are unrecoverable, as in v1.
  Source units no sound law touches (Sumerian numerals such as `#1(disz)` and written determinatives
  such as `{kuš}`) keep their value, as in the v1 sister.
- Every token counts. Task D is scored whatever reference the solver chose, as in v1. The ceiling
  (share of tokens with a strict reflex) is reported beside every score.

**Methods and settings.** Revised EM (primary), original EM, frequency-rank baseline; 3 EM restarts,
60 iterations (as v1). Task C: the family of the chosen reference; the chosen reference is reported.

**Freeze and later data.** The final run refuses to start unless every file outside `src/ibdb/data`
(and outside `reports/`, `docs/`) is identical to the `frozen-v2` tag. Finnish-Estonian joins later as
data only: the Pajusalu gold table and the Kalevipoeg text function in `src/ibdb/data/relatives.py`,
written and committed before its yardsticks and before its Task C/D tiers, which run on the same
frozen code into their own records file (`--relative estonian`).

**Reporting.** Means over the 6 corpora per hidden language and script type, the number of corpora at
or above 50% of tokens, `related` and `candidates` tables, sister and descendant pairs labelled, the
bracket rows and the Ugaritic result beside them.

## 7. Fresh-seed replication of the Task C/D run (seeds 3-5)

Declared 2026-10-21, after the seeds 0-2 results of entry 6 were reported and before any corpus of
this replication is generated. It changes no method, no score and no entry-6 result; the seeds 0-2
tables stay primary.

**Why.** The entry-6 cells rest on 6 corpora each and single corpora vary widely
(`reports/v2/cd/per_corpus.md`). v1 replicated its headline experiments on fresh seeds 3-5; this
does the same for v2.

**Run.** The frozen `run_corpus` of `scripts/v2/cd_v2.py`, unchanged, on the Indus-point corpora of
profiles `sister_v2_repl` (sampler A) and `sister_v2_gen2_repl` (sampler B): seeds 3-5, five
languages, four script types, 120 corpora, the same tiers (`harsh`; Italian, Malayalam, Kannada), 3 EM
restarts, 60 iterations. The corpora are checked against the statistics in the v1 records before
any score is read. The upper bound is read from the same two profiles' records.

**Where the code lives.** Post-hoc analysis, figure and replication-driver code lives under
`reports/v2/cd/analysis/`, outside the code tree that the frozen-code check guards (everything
outside `src/ibdb/data`, `reports/` and `docs/` must equal `frozen-v2`). The driver only calls the
frozen functions; it does not score anything itself.

**Replication checks, fixed now.** Each is evaluated on seeds 3-5 alone (revised EM, strict,
`related` tier unless stated) and reported as replicated or not replicated:
- R1. Every real-relative mean (each relative, each script type) is below 50%.
- R2. The Old Tamil alphabetic means with Malayalam and with Kannada both lie within 10 points of
  the Ugaritic result (32.0%), i.e. in 22.0-42.0%.
- R3. Italian's mean is below `harsh`'s for alphabetic and for syllabic scripts.
- R4. In `candidates_real`, the revised rule picks the real relative in fewer than half of the 24
  corpora, for each of the three relatives.

**Reporting.** The same tables for seeds 3-5 alone; R1-R4 with their values; then means over all 12
corpora per cell (seeds 0-5) beside the primary seeds 0-2 tables, labelled as pooled. Descriptive
95% intervals from a bootstrap over corpora (2,000 resamples) accompany the pooled means; no
hypothesis test is made.

## 8. Controls for reading the Task D results (unrelated reference, constant floor, solver budget, determinism)

Declared 2026-10-21, before any of these controls is run. **Post hoc in motivation, pre-registered in
procedure.** The motivation comes from results already seen: in `candidates_real`, when the revised rule
chose an unrelated reference, Old Tamil alphabetic still scored about 12% against Malayalam's gold;
and single-corpus scores are bimodal (`reports/v2/cd/per_corpus.md`). Methods are unchanged
(`frozen-v2`); only the reference given and the number of EM restarts vary. Code:
`reports/v2/cd/analysis/controls.py`, which calls only frozen functions.

**Corpora.** As entries 6 and 7: Latin and Old Tamil, four script types, seeds 0-5, samplers A and B
(48 corpora per hidden language), except C3 (seeds 0-2 only).

**C1. Unrelated-reference control.** The `related` tier with one unrelated v1 language as the only
reference (the same v1 reference object the `candidates` tiers use): for Old Tamil, Latin and Finnish;
for Latin, Old Tamil and Finnish (Sanskrit is left out for Latin as a distant relative, and Sumerian
because its syllable units are sign readings). Revised EM (3 restarts, 60 iterations) and the
frequency-rank baseline. Each prediction is scored, strict and lenient, against each real relative's
gold for that hidden language, exactly as the real relative's own run is scored.
- *Reading, fixed now:* in a cell (relative, script type), the relative's added value is its mean
  (seeds 0-5) minus the higher of the two unrelated-reference means on the same corpora and gold. The
  relative **measurably helps** in that cell only if the added value is at least 5 points **and** the
  relative beats the better unrelated reference in at least 9 of the 12 paired corpora. Otherwise the
  cell is reported as "no measurable help over an unrelated reference".

**C2. Constant-prediction floor.** For each corpus and gold, the strict score of the best single-unit
answer (every sign mapped to one unit): the largest token share of one regular reflex. Computed exactly,
no solver. A real-relative mean within 2 points of its floor is reported as "at the floor".

**C3. Solver budget.** Revised EM with 10 restarts instead of 3 (the first three restarts are identical:
same seed, same draws, best likelihood kept), `related` tier, the real relatives and `harsh`, Latin and
Old Tamil, four script types, seeds 0-2, both samplers. Reading, fixed now: budget is **first-order**
in a cell if the 10-restart mean differs from the 3-restart mean by more than 10 points; otherwise
second-order. The primary results stay at 3 restarts.

**C4. Determinism.** C3 also reruns revised EM at 3 restarts on the same corpora and tiers. Every value
must equal the frozen-run record exactly; any mismatch is reported as a reproducibility failure.

**Diagnostics** (recorded, no threshold): number of distinct units predicted, and the share of sign
tokens assigned to the single most common predicted unit (a degeneracy index).

**Reporting.** C1-C4 in `reports/v2/cd/controls.md`, with per-cell values and paired counts, beside
the primary tables. Nothing in entries 1-7 changes.
