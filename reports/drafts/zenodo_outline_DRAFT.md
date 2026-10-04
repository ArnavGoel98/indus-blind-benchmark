# DRAFT OUTLINE: awaiting approval, no prose written

**Working title:** Indus-like corpora are not one difficulty: a blind benchmark of decipherment methods on synthetic scripts calibrated to published Indus statistics

**Abstract:** about 200 words. The five findings in order, the limitations in one sentence, and a statement that nothing here deciphers or claims to decipher the Indus script.

## 1. Introduction
One line: which question can be asked without a bilingual (could existing methods read an Indus-like corpus?), and why "Indus-like" must be defined by citable statistics.

## 2. Related work
One line: entropy and Markov studies (Rao, Yadav), the critique by Farmer, Sproat and Witzel, Sproat's non-linguistic controls, and decipherment by EM and cognate matching (Knight; Luo et al.).

## 3. Benchmark design
- **3.1 Plaintext sources and licences:** one line on the five languages, the controls, and each licence (CDLI terms stated plainly).
- **3.2 Synthetic scripts:** one line on the four script types and their phenomena (allographs, homophony, polyvalence, determinatives).
- **3.3 Calibration targets:** one line on the 2,906 texts × 4.6 signs and each target's citation and verification status.
- **3.4 Calibration regimes:** one line on full, holdout and wrong-prior, and why holdout leads.
- **3.5 Non-linguistic controls:** one line on the structurally independent families and the adversarial control.
- **3.6 Methods, frozen:** one line on the eight families, the frozen-v1 tag, and both EM selection rules (the revised rule is post hoc).
- **3.7 Tasks and scoring:** one line on tasks A–D, the knowledge tiers, and resampling whole languages for intervals.
- **3.8 Sensitivity sweep:** one line on setting the duplicate rate and the sign inventory exactly, the 6 × 5 grid, the strict and plausible-box panels, and the published reference points.

## 4. Results
- **4.1 Decipherability is underdetermined by published Indus statistics:** inside the plausible box, revised EM recovers 8.7–21.8% of tokens (plausible-box panel). Report the original rule beside it.
- **4.2 Entropy statistics fail at Indus scale:** synthetic languages and i.i.d. signs score the same entropy ratio (about 0.47), and the entropy classifier is at chance under holdout (0.57 [0.32, 0.81]; 0.49 on fresh seeds).
- **4.3 No relative language: at most 4.3% recovery:** box panel, upper interval 7.4%. State the wider figures alongside (see the open points).
- **4.4 Corpus size barely helps; the length effect depends on the generator:** 500 → 50,000 texts moves revised EM only from 10.2% to 16.9%. The length effect seen under generator-v1 largely disappears under v2.
- **4.5 Archaeological predictions (prediction, not measurement):** seals-only (near 0 duplicates) against tablets-only (≥ 0.354) regions on the map, testable once per-object data is available.

## 5. Limitations
- **5.1 Allograph merging:** inventory is raised only through allographs, and no tested method merges them.
- **5.2 Sister-language distance:** a bijective sound change is absorbed by the solver, so related-tier results are an upper bound of unknown distance dependence.
- **5.3 Text-beginner calibration:** most generator-v1 corpora miss the beginners target; v2 did not fix it.
- **5.4 CDLI licence:** academic reuse with citation, not an open licence; Sumerian is excluded from public rounds.
- **5.5 The 2,591 vs 2,906 discrepancy:** the M77 duplicate rate comes from the 2,591 texts plotted by Yadav et al.; the 315-text gap is unexplained.
- **5.6 Subset positions are estimated:** they rest on qualitative statements and raw counts, not subset rates.
- **5.7 The single-period subset cannot be placed:** it lies below the smallest buildable inventory, and every subset has fewer than 2,906 texts.

## 6. Blind challenge and reproducibility
One line: public and hidden rounds, SHA-256 key commitments, one submission per team, and one-command reproduction from the frozen-v1 / data-v1 tags.

## 7. Conclusion
One line: any statement about Indus difficulty must name its corpus (object types, period, duplication); the benchmark makes that explicit.

## Back matter
- **Data and code availability:** one line on the repository, tags, licences, and the fact that no third-party text is redistributed.
- **Acknowledgements:** one line on J. M. Kenoyer's comments (to be confirmed with him before naming him).
- **References:** one line: only sources read or explicitly marked "via" (from `config/indus_targets.yaml`).
- **Appendices:** one line: calibration report, full result tables with intervals, sensitivity tables, method deviations.

## Open points before writing
1. Headline 3 says "≤4.3%". That holds for the plausible-box panel (10 fixed combinations; upper interval 7.4%). Across all corpora inside the box the maximum is 5.3%, and anywhere on the grid it is 7.1% (at 0 duplicates and 400 signs). Proposed wording: "at most 4.3% (fixed-composition panel), never above 7.1% anywhere on the grid".
2. Headline 1's 8.7–21.8% uses the revised EM rule, which was adopted post hoc. The earlier agreement was that such figures always carry that caveat. Proposed: state it in 4.1 and report the original rule beside it (3.5–5.1% in the box, same panel).
3. data-v1 is on GitHub (pointing at bbd0e49151), so section 6 can cite both tags.
