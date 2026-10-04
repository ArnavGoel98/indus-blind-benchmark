# DRAFT OUTLINE (revision 4): awaiting approval, no prose written

**Title:** A Blind Benchmark of Decipherment Methods on Synthetic Scripts Calibrated to Indus Statistics

**Abstract:** about 200 words. The five findings in order, the original (frozen) EM rule primary and the
revised rule secondary and post hoc, limitations in one sentence, and an explicit statement that
nothing here deciphers or claims to decipher the Indus script.

## 1. Introduction
One line: which question can be asked without a bilingual (could existing methods read an Indus-like corpus?), and why "Indus-like" must be defined by citable statistics.

## 2. Related work
One line: Rao and Yadav entropy/Markov studies, Farmer-Sproat-Witzel, Sproat's non-linguistic controls, Knight-style EM, cognate matching (Luo et al.).

## 3. Benchmark design
- **3.1 Sources and licences:** one line on five languages, the controls and each licence (CDLI stated plainly).
- **3.2 Synthetic scripts:** one line on four script types and their phenomena.
- **3.3 Calibration targets:** one line on 2,906 × 4.6 and each target's citation and verification status.
- **3.4 Calibration regimes:** one line on full, holdout and wrong-prior; holdout leads.
- **3.5 Non-linguistic controls:** one line on structurally independent families plus an adversarial control.
- **3.6 Knowledge tiers:** one line: the synthetic sister is built from the other half of the same source text and the solver receives its true sound correspondences, so related/candidates tiers are upper bounds (quantified in 5.9).
- **3.7 Methods, frozen:** one line on the frozen-v1 tag, the original EM rule as primary, and the revised rule as post-hoc secondary.
- **3.8 Tasks and scoring:** one line on tasks A-D, intervals that resample whole languages, and the shuffled-prediction control.
- **3.9 Sensitivity sweep:** one line on setting duplicates and inventory exactly, the 6 × 5 grid, the panels and the published reference points.

## 4. Results
- **4.1 Entropy statistics fail at Indus scale (UNAFFECTED by the sister-tier defect: Task A uses no reference language):** same entropy ratio (about 0.47) for synthetic languages and i.i.d. signs; the classifier is at chance under holdout (0.57 [0.32, 0.81]; 0.49 on fresh seeds). Rule-independent.
- **4.2 No related language (UNAFFECTED by the sister-tier defect: the hidden language and its sister are excluded from this tier):** "Without a related language among candidates, mean recovery stays at or below 4.8% in every run; no corpus reaches 50% of tokens; the best single corpus reaches 28%." Both rules, both generators, fresh seeds.
- **4.3 Difficulty is underdetermined by published Indus statistics, mainly when a related language is available (final wording after the sister-v2 rerun):** primary evidence is the frozen original rule across generators (v1 -> v2 at the Indus point: 2.1% -> 15.0%, the v2 corpora inside the plausible box averaging 12.4%), while within the v1 box the original rule stays at 3.5-5.1%. Secondary, post hoc: the revised rule (14.6% -> 42.7%; 8.7-21.8% across the v1 box, within-combination swings up to 62 points). Candidates tier: sister-v1 numbers reported as "upper bound (sister-v1, known overlap)" beside sister-v2, each with the score before the cognate step; after-cognate scores labelled "with oracle sound correspondences".
- **4.4 Longer inscriptions vs more inscriptions:** "Under the frozen rule, longer inscriptions help more than more inscriptions in both generators", at equal total tokens with a related language among candidates (v1: 32.6% vs 3.0% at about 29k tokens; v2: 55.3% vs 19.7%). Without a relative, both stay at or below 6.5%. Candidates tier: sister-v1 numbers reported as "upper bound (sister-v1, known overlap)" beside sister-v2, each with the score before the cognate step; after-cognate scores labelled "with oracle sound correspondences".
- **4.5 Archaeological predictions (prediction, not measurement):** seals-only regions above tablets-only regions under both rules, testable once per-object data is available.

## 5. Limitations
- **5.1 Allograph merging:** inventory is raised only through allographs, and no tested method merges them.
- **5.2 Sister-language distance:** a bijective sound change is absorbed by the solver; the distance dependence is unknown.
- **5.3 Text-beginner calibration:** most generator-v1 corpora miss the target; v2 did not fix it.
- **5.4 CDLI licence:** academic reuse with citation, not an open licence; Sumerian is excluded from public rounds.
- **5.5 The 2,591 vs 2,906 discrepancy:** in the M77 duplicate-rate source.
- **5.6 Subset positions are estimated:** qualitative statements and raw counts only.
- **5.7 The single-period subset cannot be placed:** below the smallest buildable inventory; every subset is smaller than 2,906 texts.
- **5.8 Post-hoc selection rule:** the original rule is primary throughout.
- **5.9 Sister tiers are optimistic (new, from the audit):** the true sound correspondences are given to the solver (+35 points on the inspected corpus); the sister is the same source text, so 42-90% of seal-like texts recur word for word in its half; and a split defect puts identical clauses in both halves (6-60% of clauses, by language).

## 6. Blind challenge and reproducibility
One line: public and hidden rounds, SHA-256 key commitments, one submission per team, reproduction from the frozen-v1 and data-v1 tags.

## 7. Conclusion
One line: any statement about Indus difficulty must name its corpus (object types, period, duplication), its knowledge tier and its selection rule.

## Back matter
- **Data and code availability:** one line on the repository, tags and licences; no third-party text redistributed.
- **Acknowledgements:** one line: name J. M. Kenoyer, S. Houston or R. Sproat only after each has confirmed; until then, no names.
- **References:** one line: only sources read, or marked "via".
- **Appendices:** one line on calibration, full tables, sensitivity tables, the rule comparison, the audit (`reports/audit_2026-10-04.md`) and method deviations.

## Open points before writing
1. The sister-v2 rerun (split by clause content) is running: 2,280 jobs, about 4 h. Results are reviewed before any prose.
2. **Before-cognate scores exist only for sister-v2.** The sister-v1 records saved scores, not per-sign predictions, so their before-cognate column needs a sister-v1 rerun (~4 h more) if wanted.
3. **Residual verbatim overlap under sister-v2 is not near zero:** 38-82% of seal-like texts by language. Identical shared clauses are 0, but short phrases recur within one language. Reaching near zero needs a different design, for example dropping reference clauses that contain any hidden-text word sequence, or a sister with divergent vocabulary and syntax.
