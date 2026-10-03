---
title: "Could existing decipherment methods read an Indus-sized corpus? A blind benchmark with synthetic, calibrated scripts"
version: "0.1.0 (draft for Zenodo deposit)"
license: "Text CC BY 4.0; code MIT"
keywords: [Indus script, decipherment, benchmark, computational paleography, entropy, substitution cipher, null results]
---

# Could existing decipherment methods read an Indus-sized corpus? A blind benchmark with synthetic, calibrated scripts

**Status: draft.** Numbers in Sections 6-7 are produced by `ibdb report --profile full` and
copied from `reports/results/results.md` and `reports/calibration_report.md`. When those files
and this text disagree, the files are authoritative.

**This work does not decipher, and does not claim to decipher, the Indus script.**

## Abstract

The Indus corpus is small: a few thousand mostly seal inscriptions averaging under five signs,
written with several hundred sign types, with no bilingual. Many decipherment claims and several
statistical arguments about whether the signs encode language at all have been made on this
corpus, but no common test exists of whether the methods involved *can* work on data of this
shape. We build IBDB, a benchmark of synthetic scripts that encode known languages (Sanskrit, Old
Tamil, Sumerian, Latin, Finnish) and non-linguistic sign systems. Each is calibrated to published
Indus summary statistics, and its answer key is hidden. We evaluate eight method families on four
tasks: language vs non-language (A), script type (B), language family (C), and sign values (D).
We sweep corpus size from 500 to 50,000 texts and mean length from 3 to 20 signs, over three
calibration regimes and three levels of solver knowledge. We report a "decipherability curve" with
the Indus corpus marked as a band, the smallest corpus at which each method beats chance, and the
share of randomly drawn writing systems in which each method succeeds at Indus scale. The headline
results are summarized in Section 7. All code, configurations, and calibration evidence are
public. Answer keys for a hidden challenge tier are committed by hash and held by the maintainer.

## 1. Introduction

Arguments about the Indus script fall into two groups. *Decipherment claims* assign readings, often
in a Dravidian or Indo-Aryan language. *Structural arguments* use corpus statistics to argue that
the signs do or do not encode language. Examples are conditional entropy (Rao et al. 2009), n-gram
models (Yadav et al. 2010) and positional analysis. Opposing structural arguments include the
brevity of the texts (Farmer, Sproat & Witzel 2004) and the observation that entropy-type
statistics do not separate writing from non-linguistic symbol systems (Sproat 2010, 2014).

Both groups face the same unasked question: **would the method work on a corpus with Indus
statistics whose answer is known?** Successful computational decipherments, such as Ugaritic
(Snyder, Barzilay & Knight 2010) and Linear B (Luo, Cao & Barzilay 2019), had a closely related
known language and far longer texts. IBDB asks the question directly. We make many synthetic
"Indus-like" corpora with known answers and measure what each method recovers.

Contributions:
(i) a calibrated generator for fake scripts, with every calibration target sourced and flagged;
(ii) plug-in implementations of eight method families behind one interface;
(iii) a scoring protocol for four separate tasks with leave-one-source-out training, confidence
intervals and multiple seeds;
(iv) a blind challenge with hash-committed keys and a static leaderboard.

## 2. Pre-registration of design risks

Before building, we put the design through an adversarial review (an advocate, a critic, an
evaluator of demand, and a judge). The critic's strongest objection, which we accept, is
**circularity**. If the generator is calibrated to the statistics that the methods measure, and
the generator's free choices (script type, allography, how texts are selected) determine the
outcome, then "the Indus point" on any curve is a coordinate in a space we defined. The judge
ruled "fix first" and required six safeguards, all implemented:

1. results reported as a band and as a *feasibility region* over random writing-system parameters,
   never as a single Indus verdict;
2. three calibration regimes (`full`, `holdout`, `wrong_prior`) with rank-stability analysis;
3. non-linguistic controls that are structurally independent of language, including an
   adversarial control tuned to imitate language entropy;
4. an explicit axis for solver knowledge (`related`, `candidates`, `none`);
5. "nothing works" regions reported as first-class results;
6. a challenge design that resists probing.

Section 8 lists the remaining choices that could still make results meaningless.

## 3. Calibration targets

All targets are in `config/indus_targets.yaml`, each with citation, tolerance, the size of the
reference corpus it was measured on, and whether we verified the number in the source.

| Statistic | Target | Source (verified?) |
|---|---|---|
| Texts | 5,500 (band 1,548-5,500 in plots) | project brief (**no**); M77: 2,906 texts / 3,573 lines (yes, via Yadav et al. 2010) |
| Mean length | 4.4 ± 0.25 | brief (**no**); derived from M77: 13,372 signs / 2,906 texts = 4.60 (yes, Rao 2018 + Yadav et al. 2010); FSW 2004: "under 4.6" (yes) |
| Median length | 4 ± 1 | brief (**no**) |
| Longest text | 17 ± 4 | Farmer, Sproat & Witzel 2004 (yes) |
| Sign inventory | 400-700 | Mahadevan 1977: 417 (yes); Possehl 2002: 419; Wells 2015: ~694 (both via Wikipedia, **not checked**) |
| Signs covering 80% of tokens | 69 ± 15 (on 1,548 texts) | Yadav et al. 2010 (yes) |
| Share of most frequent sign | 0.10 ± 0.03 (on 1,548 texts) | Yadav et al. 2010 (yes) |
| Hapax share of sign types | 0.27 ± 0.10 (on 2,906 texts) | Possehl 2002 via Wikipedia (**not checked**) |
| Text enders covering 80% | 23 ± 8 (on 1,548 texts) | Yadav et al. 2010 (yes) |
| Text beginners covering 80% | 82 ± 20 (on 1,548 texts) | Yadav et al. 2010 (yes) |
| Zipf-Mandelbrot fit | a=15.39, b=2.59, c=44.47 (report only) | Yadav et al. 2010 (yes) |
| Duplicate texts | report only, no published number found | - |

Size-dependent statistics are computed on random subsamples of the reference size.

## 4. Data and generator

**Plaintext** (licenses in `DATA_LICENSES.md`):
- Sanskrit: Rāmāyaṇa from the Digital Corpus of Sanskrit (CC BY 4.0), chosen because GRETIL's epic
  files are "for reference purposes only".
- Old Tamil: 17 Sangam root texts from Project Madurai.
- Sumerian: the CDLI ATF dump, including 19,076 intact Ur III seal inscriptions.
- Latin: Caesar and Vergil from Project Gutenberg.
- Finnish: Kalevala from Project Gutenberg.

Each source is split into short clauses biased toward seal-like genres: names, epithets, titles,
formulaic rubrics and seal texts. Clauses are split by a fixed hash into a *hidden* half (used to
generate corpora) and a *reference* half (used as known-language models), so no solver ever sees
the phrases it must decipher.

**Script.** Words are mapped to units by script type:
- alphabetic: phonemes;
- syllabic: CV/V/C units;
- logographic: word forms;
- logo-syllabic: the 250 most frequent words as logograms, other words spelled syllabically,
  plus determinatives.

Units map to random sign IDs. Optional phenomena:
- allographs, chosen per token with a dominant base form;
- homophones, chosen per word;
- polyvalent signs;
- determinatives (real ones for Sumerian, annotated classes for Sanskrit, seeded classes otherwise);
- word dividers;
- reading direction.

**Text sampling.** Target lengths are drawn from a discretized log-normal. Sigma is set so that the
expected maximum of 5,500 draws is 17, and mu so that the mean is 4.4; this also yields median 4.
For each target length, a contiguous window of words with exactly that encoded length is drawn.
Windows are weighted by word frequency, final-word frequency, first-word frequency and genre.
A small share of texts duplicate a few popular texts, modelling the repeated seals of M77.

**Calibration.** Seeded random search plus coordinate refinement over these knobs minimizes the
squared normalized deviation from the regime's targets. The duplicate-text share is capped at 40%.
That cap is our assumption, not a published number.

**Non-linguistic controls:**
- heraldic arms, generated with the rule of tincture, one sign per visual element;
- administrative slot tags;
- sparse Markov emblems with positional preferences;
- Rao's (2009) type 1 (rigid) and type 2 (i.i.d.) systems;
- an adversarial Markov chain whose conditional/unigram entropy ratio is tuned to the median of
  the calibrated language corpora;
- Japanese kamon *descriptions* (Sakana AI), reported separately because they are text.

## 5. Methods evaluated

Each method implements `analyze(corpus, knowledge) -> Prediction`. Exact citations and
deviations are printed by `ibdb methods` and stored with each method class.

| # | Method | Tasks | Original | Main deviation |
|---|---|---|---|---|
| 1 | Conditional & block entropy | A | Rao et al. 2009; Rao 2010 | curve reduced to H(X2\|X1)/H(X1) at top-100 signs; band learned, not read off a plot |
| 2 | Bigram Markov model | A | Yadav et al. 2010 | cross-validated bigram-over-unigram gain used as a language statistic (not proposed by the authors) |
| 3 | Positional histograms | A | Mahadevan 1977 tables; Fuls (ICIT) | specificity + beginner/ender asymmetry summaries; **Fuls reference to be completed** |
| 4 | Segmentation | B (+ diagnostic F1) | Harris 1955; Tanaka-Ishii 2005 | branching-entropy peaks instead of Yadav's frequent-n-gram segmentation |
| 5a | Inventory rule | B | conventional typology rule of thumb; Chao 1984 | fixed thresholds 60/150/1200 on Chao1 estimate |
| 5b | Inventory/frequency classifier | B | - | multinomial LR, leave-one-source-out |
| 6a | Two-parameter tree | A | Lee, Jonathan & Ziman 2010 | cuts learned leave-one-source-out; a = 7 |
| 6b | Multi-feature classifier | A | in the spirit of Sproat 2014 | LR over 11 features |
| 7 | HMM/EM substitution solver | C, D | Knight et al. 2006; Berg-Kirkpatrick & Klein 2013 | bigram-count EM, 3 restarts, 250 units / 350 signs, OTHER emits uniformly; candidate selection by MI-normalized bigram gain |
| 8 | Lost-language matcher | C, D | Luo, Cao & Barzilay 2019 | **not neural**: categorical P(unit\|sign) table + assignment matching on equal-length words |
| - | Frequency-rank baseline | C, D | classical frequency analysis | - |

**Two corrections to EM made during development**, reported because both change results:
(i) the pooled rare-unit state was a free wildcard, so references with heavy tails won every model
comparison; it now emits uniformly and its mass is pinned to 3% for all references;
(ii) raw likelihood favoured high-entropy reference languages, so candidate selection now uses the
likelihood gain of the reference's bigram model over its own unigram model, divided by the
reference's own bigram mutual information.

## 6. Evaluation protocol

*Corpora.*
- Size sweep: 500-50,000 texts at mean length 4.4.
- Length sweep: mean 3-20 at 5,500 texts.
- Each sweep covers 5 languages × 4 script types plus 7 controls, with 3 seeds.
- Regimes `holdout` and `wrong_prior` at the Indus point.
- 120 feasibility scenarios at the Indus point, with random allography, homophony, polyvalence,
  determinatives, dividers and direction around calibrated scripts.

*Training without leakage.* Decision rules for Tasks A and B are learned leave-one-source-out
within each sweep point. A Sanskrit corpus is judged by a rule fit only on non-Sanskrit corpora;
a heraldry corpus by a rule that never saw heraldry.

*Knowledge tiers for C and D:*
- `related`: a synthetic sister language, with 30% of phonemes permuted by regular
  correspondence and 20% of words replaced;
- `candidates`: the sister plus all other benchmark languages;
- `none`: other languages only.

Predicted reference units are mapped through the regular correspondence before scoring, which
credits cognate identification as Ugaritic was credited via Hebrew. Script type and unit level
are given to the solver, an optimistic oracle.

*Scores.* A: balanced accuracy. B: accuracy. C: accuracy vs chance (1/number of candidate
families). D: share of sign tokens whose predicted value equals the token's true value;
"success" = at least 50%. Rates carry Wilson 95% intervals; mean accuracies carry bootstrap 95%
intervals.

## 7. Results

*(Filled from `reports/results/results.md` after the full run; see Section 7 in the final
version.)*

## 8. Limitations: choices that could make results meaningless

1. **Oracle script type and unit level** in Task D: reported recovery is an upper bound.
2. **Sister-language distance** is a free parameter that sets `related`-tier results; it is
   reported with every table.
3. **Inventory calibration** removes the information that inventory-based script typology uses.
4. **Text selection is tuned**, not modelled on what Indus seals said; `holdout` quantifies the effect.
5. **Unverified targets** (5,500 texts, mean 4.4, median 4) come from the brief; plots use a band.
6. **The Luo-style matcher is not neural**; neural models could do better.
7. **Plug-in entropy is biased at Indus scale.** An i.i.d. 420-sign source measures about 0.59
   of its true conditional/unigram entropy ratio on ~15k bigrams, so entropy cut-offs depend on
   corpus size.
8. **Five languages, one text genre each.** Families are coarse (Sumerian is a single "isolate"),
   so Task C chance is about 0.25-0.33.
9. **Controls are generated by us.** A classifier can only be as general as its controls.

## 9. Blind challenge

Public rounds release corpora and keys. Hidden rounds release corpora and SHA-256 commitments of
keys. Challenge corpora are written from *secretly disguised* sister languages, so they cannot be
matched against the public source texts. One scored submission per team per hidden round. The
static leaderboard (`leaderboard/index.html`) marks entries whose authors claim a real Indus
decipherment.

## 10. Reproducibility

`ibdb reproduce --profile full` regenerates every number and figure from `master_seed`. Tests run
without downloads (`pytest`). Data provenance, including URL, SHA-256 and license, is written
next to every downloaded file.

## References

- Berg-Kirkpatrick, T., & Klein, D. (2013). Decipherment with a million random restarts. *EMNLP 2013*.
- Chao, A. (1984). Nonparametric estimation of the number of classes in a population. *Scandinavian Journal of Statistics* 11, 265-270.
- Farmer, S., Sproat, R., & Witzel, M. (2004). The collapse of the Indus-script thesis: the myth of a literate Harappan civilization. *Electronic Journal of Vedic Studies* 11(2).
- Harris, Z. S. (1955). From phoneme to morpheme. *Language* 31(2), 190-222.
- Knight, K., Nair, A., Rathod, N., & Yamada, K. (2006). Unsupervised analysis for decipherment problems. *COLING/ACL 2006*.
- Lee, R., Jonathan, P., & Ziman, P. (2010). Pictish symbols revealed as a written language through application of Shannon entropy. *Proceedings of the Royal Society A* 466 [pages to verify].
- Luo, J., Cao, Y., & Barzilay, R. (2019). Neural decipherment via minimum-cost flow: from Ugaritic to Linear B. *ACL 2019*.
- Mahadevan, I. (1977). *The Indus Script: Texts, Concordance and Tables*. Memoirs of the Archaeological Survey of India 77.
- Possehl, G. L. (2002). *The Indus Civilization: A Contemporary Perspective*. AltaMira. [cited via secondary source]
- Rao, R. P. N., Yadav, N., Vahia, M. N., Joglekar, H., Adhikari, R., & Mahadevan, I. (2009). Entropic evidence for linguistic structure in the Indus script. *Science* 324(5931), 1165.
- Rao, R. P. N. (2010). Probabilistic analysis of an ancient undeciphered script. *IEEE Computer* 43(4) [to verify].
- Rao, R. P. N. (2018). The Indus script and economics. In *Walking with the Unicorn*, Archaeopress, 518-525. arXiv:1812.00049.
- Snyder, B., Barzilay, R., & Knight, K. (2010). A statistical model for lost language decipherment. *ACL 2010*.
- Sproat, R. (2010). Ancient symbols, computational linguistics, and the reviewing practices of the general science journals. *Computational Linguistics* 36(3).
- Sproat, R. (2014). A statistical comparison of written language and nonlinguistic symbol systems. *Language* 90(2), 457-481.
- Tanaka-Ishii, K. (2005). Entropy as an indicator of context boundaries. *IJCNLP 2005*.
- Wells, B. K. (2015). [Cited via secondary source; full entry to be completed.]
- Yadav, N., Joglekar, H., Rao, R. P. N., Vahia, M. N., Adhikari, R., & Mahadevan, I. (2010). Statistical analysis of the Indus script using n-grams. *PLoS ONE*. arXiv:0901.3017.
