# DRAFT OUTLINE (revision 2): awaiting approval, no prose written

**Title:** A Blind Benchmark of Decipherment Methods on Synthetic Scripts Calibrated to Indus Statistics

**Abstract:** about 200 words. The six findings in order. Both EM selection rules are reported, and the
original (frozen) rule leads. Limitations in one sentence. An explicit statement that nothing here
deciphers or claims to decipher the Indus script.

## 1. Introduction
One line: which question can be asked without a bilingual (could existing methods read an Indus-like corpus?), and why "Indus-like" must be defined by citable statistics.

## 2. Related work
One line: Rao and Yadav entropy/Markov studies, Farmer-Sproat-Witzel, Sproat's non-linguistic controls, Knight-style EM, cognate matching (Luo et al.).

## 3. Benchmark design
- **3.1 Sources and licences:** one line on the five languages, the controls and each licence (CDLI stated plainly).
- **3.2 Synthetic scripts:** one line on four script types and their phenomena (allographs, homophony, polyvalence, determinatives).
- **3.3 Calibration targets:** one line on 2,906 texts × 4.6 signs and each target's citation and verification status.
- **3.4 Calibration regimes:** one line on full, holdout and wrong-prior; holdout leads.
- **3.5 Non-linguistic controls:** one line on structurally independent families plus an adversarial control.
- **3.6 Methods, frozen:** one line on the frozen-v1 tag, the original EM selection rule as the pre-registered primary, and the revised rule as a post-hoc secondary.
- **3.7 Tasks and scoring:** one line on tasks A-D, the knowledge tiers, and intervals that resample whole languages.
- **3.8 Sensitivity sweep:** one line on setting the duplicate rate and the inventory exactly, the 6 × 5 grid, the strict and plausible-box panels, and the published reference points.

## 4. Results
- **4.1 Entropy statistics fail at Indus scale:** synthetic languages and i.i.d. signs score the same entropy ratio (about 0.47), and the entropy classifier is at chance under holdout (0.57 [0.32, 0.81]; 0.49 on fresh seeds). No EM involved, so rule-independent.
- **4.2 No related language: nothing works, under both rules:** mean recovery at most 4.8% in every run, generator and rule; at most 4.3% (fixed-composition panel), never above 7.1% anywhere on the grid; 0 of 1,751 corpora reach 50% (individual corpora up to 28%).
- **4.3 The original frozen rule stays near 5% in the plausible box, for generator-v1:** 3.5-5.1% (box panel), within-combination spread median 2.1 points, max 7.6. The generator-v2 corpora inside the same box average 12.4%, so this holds for v1 only.
- **4.4 Difficulty depends on corpus properties that published statistics leave open (both rules side by side; revised rule post hoc):** v1 -> v2 at the Indus point moves the original rule 2.1% -> 15.0% and the revised rule 14.6% -> 42.7%. Inside the v1 box the revised rule spans 8.7-21.8% (within-combination swings up to 62 points) while the original stays near flat.
- **4.5 Corpus size vs text length:** under v1, more texts barely help either rule (original 2.1 -> 5.1%, revised 14.6 -> 16.9% from 2,906 to 50,000) while longer texts help both (to about 44% at 20 signs). Under v2, size helps the original rule (15.0 -> 32.0%), and only the revised rule's length effect disappears.
- **4.6 Archaeological predictions (prediction, not measurement):** seals-only (near 0 duplicates) sits above tablets-only (at least 0.354) under both rules, testable once per-object data is available.

## 5. Limitations
- **5.1 Allograph merging:** inventory is raised only through allographs, and no tested method merges them.
- **5.2 Sister-language distance:** a bijective sound change is absorbed by the solver, so related-tier results are an upper bound with unknown distance dependence.
- **5.3 Text-beginner calibration:** most generator-v1 corpora miss the beginners target; v2 did not fix it.
- **5.4 CDLI licence:** academic reuse with citation, not an open licence; Sumerian is excluded from public rounds.
- **5.5 The 2,591 vs 2,906 discrepancy:** the M77 duplicate rate is computed on the 2,591 texts plotted by Yadav et al.; the gap is unexplained.
- **5.6 Subset positions are estimated:** they rest on qualitative statements and raw counts, not subset rates.
- **5.7 The single-period subset cannot be placed:** it lies below the smallest buildable inventory, and every subset has fewer than 2,906 texts.
- **5.8 Post-hoc selection rule:** the revised EM rule was chosen after seeing results. The original rule is primary throughout, and the revised rule is reported for comparison only.

## 6. Blind challenge and reproducibility
One line: public and hidden rounds, SHA-256 key commitments, one submission per team, reproduction from the frozen-v1 and data-v1 tags.

## 7. Conclusion
One line: any statement about Indus difficulty must name its corpus (object types, period, duplication) and its selection rule; the benchmark makes both explicit.

## Back matter
- **Data and code availability:** one line on the repository, tags and licences; no third-party text is redistributed.
- **Acknowledgements:** one line: name J. M. Kenoyer, S. Houston or R. Sproat only after each has confirmed; until then, no names.
- **References:** one line: only sources read, or marked "via" (from `config/indus_targets.yaml`).
- **Appendices:** one line on the calibration report, full tables with intervals, sensitivity tables, the rule comparison (`reports/sensitivity/rule_comparison.md`) and method deviations.

## Open points before writing
1. **Headline 3 (4.3) as requested ("never exceeds ~5% in plausible box") is false as a general statement.** It holds for the generator-v1 sweep. The 22 generator-v2 corpora that fall inside the same box average 12.4% under the original rule. Options: (a) keep it with "for generator-v1" in the heading, as drafted above; (b) fold it into 4.4 as evidence that the box does not fix difficulty. Recommendation: (b), because the v2 contrast is the stronger finding.
2. **"Nothing works" (4.2) needs its threshold stated.** Means stay at or below 4.8% and no corpus reaches 50%, but single corpora reach 28%. Drafted wording above.
3. **Headline 5 changed under the reanalysis.** "Length effect generator-dependent" holds for the revised rule only. Under the original rule, longer texts help strongly in both generators, and under v2 more texts also help the original rule. Drafted wording above.
