# DRAFT OUTLINE (revision 6): awaiting approval, no prose written

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
- **3.6 Knowledge tiers:** one line: the synthetic sister is built from the other half of the same source text and the solver receives its true sound correspondences, so related/candidates tiers carry oracle sound correspondences (quantified in 5.9); sister-v2 splits clauses by content.
- **3.7 Methods, frozen:** one line on the frozen-v1 tag, the original EM rule as primary, and the revised rule as post-hoc secondary.
- **3.8 Tasks and scoring:** one line on tasks A-D, intervals that resample whole languages, and the shuffled-prediction control.
- **3.9 Sensitivity sweep:** one line on setting duplicates and inventory exactly, the 6 × 5 grid, the panels and the published reference points.

## 4. Results
- **4.1 Entropy statistics fail at Indus scale (UNAFFECTED by the sister-tier defect: Task A uses no reference language):** same entropy ratio (about 0.47) for synthetic languages and i.i.d. signs; the classifier is at chance under holdout (0.57 [0.32, 0.81]; 0.49 on fresh seeds). Rule-independent.
- **4.2 No related language (UNAFFECTED by the sister-tier defect: the hidden language and its sister are excluded from this tier):** "Without a related language among candidates, mean recovery stays at or below 4.8% in every run; no corpus reaches 50% of tokens; the best single corpus reaches 28%." Both rules, both generators, fresh seeds.
- **4.3 Published Indus statistics do not fix how decipherable an Indus-scale corpus is (approved wording):** "Two generators that both match them differ roughly three- to fivefold when a related language is available (frozen rule, no oracle correspondences: 2.4% vs 12.9% on the main seeds, 5.3x; 2.7% vs 9.4% on fresh seeds, 3.5x; 2.6% vs 9.3% with sister-v3, 3.7x)." Sister-v3 intervals do not overlap. Secondary: with oracle sound correspondences 2.8% vs 18.9%; revised rule post hoc.
- **4.4 Longer inscriptions vs more inscriptions:** "Under the frozen rule, longer inscriptions help more than more inscriptions in both generators." At equal tokens (2,906 x 10 vs 6,317 x 4.6, run directly), candidates tier, primary: v1 18.0% vs 2.6% (difference 15.4 [5.8, 24.9]); v2 35.6% vs 18.3% (17.4 [8.5, 25.0]); interpolated on fresh seeds: v1 17.7% vs 3.4%, v2 32.2% vs 11.8%. Sister-v3: v1 17.5% vs 3.9%, v2 34.6% vs 10.5% (filter is corpus-dependent and favours the long-text corpus; check of survival, not of size). Without a relative, both <= 6.5%.
- **4.5 Archaeological predictions (prediction, not measurement):** seals-only regions above tablets-only regions under both rules, testable once per-object data is available.

- **4.6 Robustness: sister-v3** (new section): residual overlap, Indus point, headline 3 and 4 checks, and the corpus-dependence confound (`reports/sister_v2/robustness_sister_v3.md`).
## 5. Limitations
- **5.1 Allograph merging:** inventory is raised only through allographs, and no tested method merges them.
- **5.2 Sister-language distance:** a bijective sound change is absorbed by the solver; the distance dependence is unknown.
- **5.3 Text-beginner calibration:** most generator-v1 corpora miss the target; v2 did not fix it.
- **5.4 CDLI licence:** academic reuse with citation, not an open licence; Sumerian is excluded from public rounds.
- **5.5 The 2,591 vs 2,906 discrepancy:** in the M77 duplicate-rate source.
- **5.6 Subset positions are estimated:** qualitative statements and raw counts only.
- **5.7 The single-period subset cannot be placed:** below the smallest buildable inventory; every subset is smaller than 2,906 texts.
- **5.8 Post-hoc selection rule:** the original rule is primary throughout.
- **5.9 Sister tiers are optimistic:** the true sound correspondences are given to the solver; under sister-v2 they add 7-8 points (v1) and 17-19 points (v2) on the related tier at the Indus point, and up to 51 points on single corpora. Sister-v2 removes identical shared clauses (0 in every language), which changed results within their intervals; 38-82% of seal-like texts still recur word for word in the sister's half because short phrases recur within one language. Sister-v1 numbers are reported only as "upper bound (sister-v1, known overlap)".

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
1. Primary numbers everywhere: original (frozen) rule, before the cognate step; oracle-correspondence scores secondary and labelled.
2. Sister-v3 robustness done (480 jobs, 0 errors after one config fix). Headlines 3 and 4 hold; headline 3 wording is now "roughly three- to fivefold" (5.3x main, 3.5x replication, 3.7x sister-v3).
3. Prose: sections 1-3 drafted (`reports/drafts/paper_sections_1-3_DRAFT.md`); stopped for review.
