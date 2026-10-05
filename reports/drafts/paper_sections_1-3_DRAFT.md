# DRAFT, sections 1-3 only (for review; not for deposit)

**A Blind Benchmark of Decipherment Methods on Synthetic Scripts Calibrated to Indus Statistics**

*This work does not decipher, and does not claim to decipher, the Indus script.*

Conventions used throughout. Unless a sentence says otherwise, a recovery number is Task D token
accuracy under the **original (frozen) EM selection rule**, scored **before the cognate step**.
Scores that include the solver's cognate step are secondary and are labelled "with oracle sound
correspondences". The revised selection rule was adopted after the original rule had been run and
is reported as post hoc. Intervals are 95% and resample whole source languages.

[Reviewer notes in square brackets are not part of the text. Every citation below is one already
listed in the repository; entries marked "to verify" there are marked here too.]

---

## 1. Introduction

The Indus inscriptions are short. The concordance of Mahadevan (1977) holds 2,906 texts with
13,372 sign occurrences, about 4.6 signs per text (Yadav et al. 2010; Rao 2018), and the longest
known text has 17 signs (Farmer, Sproat & Witzel 2004). Published sign lists count between 386 and
about 700 sign types, depending on how variants are grouped (Parpola 1994 and Wells 2015, both via
Rao 2018; Mahadevan 1977; Wells 2006 via Yadav et al. 2010). No bilingual text is known, and no
language of the Harappan civilisation is agreed.

Two kinds of argument have been made about this corpus. Some assign readings to the signs. Others
use corpus statistics to argue that the signs do, or do not, encode language: conditional entropy
(Rao et al. 2009), n-gram models (Yadav et al. 2010), and, on the other side, text brevity (Farmer,
Sproat & Witzel 2004) and the finding that entropy-type measures do not separate writing from
non-linguistic symbol systems (Sproat 2010, 2014). Both kinds of argument depend on a question that
is seldom tested: would the method work on a corpus of Indus size and shape whose answer is known?

We test that question directly. We write known languages, and sign systems that encode no
language, in invented scripts. We calibrate each synthetic corpus to published Indus statistics,
hide its answer key, and measure what existing methods recover. The goal is a statement of the
form "on corpora that match the published Indus statistics, method M recovers X% of sign tokens
under conditions K". Such a statement says what a method can do on Indus-like data. It says nothing
about what the Indus signs mean.

Defining "Indus-like" turned out to be the central difficulty. Published statistics fix the
number of texts, their length, the sign inventory and several frequency and positional measures.
They do not fix how often texts repeat, how many sign types are variants of one another, or how
text material is sampled. We find that these unconstrained properties change recovery several
fold. The paper therefore reports a map over them rather than a single Indus number.

**Findings.** (1) Entropy statistics do not separate synthetic languages from independent,
identically distributed (i.i.d.) signs at Indus scale. (2) Without a related language among the
candidates, mean recovery stays at or below 4.8% in every run; no corpus reaches 50% of tokens;
the best single corpus reaches 28%. (3) Published Indus statistics do not fix how decipherable an
Indus-scale corpus is. Two generators that both match them differ roughly fivefold when a related
language is available (2.4% vs 12.9% of sign tokens, frozen rule, no oracle correspondences;
replicated 2.7% vs 9.4%). (4) Under the frozen rule, longer inscriptions help more than more
inscriptions in both generators. (5) Archaeologically defined subsets of the corpus are predicted
to sit at different points on the map; these are predictions, not measurements.

**Contributions.** (i) A generator of synthetic scripts calibrated to published Indus statistics,
with every target cited and flagged as verified or not. (ii) Eight method families behind one
interface, frozen before the final runs. (iii) A protocol that scores four tasks separately,
with intervals that resample whole source languages, three calibration regimes, three levels of
solver knowledge and replication on fresh seeds. (iv) A sensitivity map over duplicate-text rate
and sign inventory, with published reference points marked. (v) A blind challenge with
hash-committed answer keys.

## 2. Related work

**Structural statistics of the Indus corpus.** Rao et al. (2009) compared the conditional entropy
of Indus sign sequences with linguistic and non-linguistic reference systems and argued for
linguistic structure. Yadav et al. (2010) fitted n-gram models to the corpus, reported its
frequency and positional statistics, and are the source of most of our calibration targets.
Farmer, Sproat & Witzel (2004) argued from text brevity and sign repetition that the signs were not
a writing system. Sproat (2010, 2014) showed that entropy-type statistics do not reliably separate
writing from non-linguistic symbol systems; Lee, Jonathan & Ziman (2010) proposed an entropy-based
classifier for the Pictish symbols that we include as a method. Our Task A asks whether these
statistics work at Indus scale when the answer is known.

**Computational decipherment.** Knight et al. (2006) framed decipherment as unsupervised learning
of a substitution model with expectation-maximisation (EM); Berg-Kirkpatrick & Klein (2013) showed
that many random restarts improve such solvers. Snyder, Barzilay & Knight (2010) recovered
Ugaritic using Hebrew as a known relative, and Luo, Cao & Barzilay (2019) recovered Ugaritic and
Linear B cognates with a neural model and minimum-cost flow. Each success had a closely related
known language and far more text per document than the Indus corpus. Our knowledge tiers separate
these conditions. The EM cognate-matcher we test borrows only the one-to-one assignment idea of
Luo, Cao & Barzilay (2019); it contains no neural network, and its results say nothing about
neural methods.

**Script-type estimation and segmentation.** We estimate script type from inventory size, with a
Chao (1984) richness estimate, and segment with branching entropy (Harris 1955; Tanaka-Ishii 2005).

**Archaeological context.** Kenoyer & Meadow (2010) and Kenoyer (2020a, 2020b) describe how
inscribed objects at Harappa differ by type and period: seals are almost all unique, while
incised and molded tablets often occur as copies or same-mold duplicates, and the script was used
and changed over roughly 700 years. We use these statements only qualitatively, to predict where
subsets of the corpus would sit on our map (Section 4.5).

[Reviewer: Rao (2010) and the page range of Lee, Jonathan & Ziman (2010) are marked "to verify"
in the repository and are not cited here until checked. Fuls (ICIT) is cited only for a sign-list
size, flagged unverified.]

## 3. Benchmark design

### 3.1 Sources and licences

Plaintext comes from five languages in four families: Sanskrit (Rāmāyaṇa, Digital Corpus of
Sanskrit, CC BY 4.0), Old Tamil (17 Sangam root texts, Project Madurai), Sumerian (CDLI bulk ATF
dump, including Ur III seal inscriptions), Latin (Caesar and Vergil, Project Gutenberg) and Finnish
(Kalevala, Project Gutenberg). CDLI's terms allow reuse "according to common and fair academic
practice" with citation, which is not an open licence; Sumerian-derived material is therefore used
in internal experiments only and excluded from published challenge rounds. No source text is
redistributed. Each source is cut into short, seal-like clauses (names, epithets, titles, formulae
and, for Sumerian, real seal inscriptions).

### 3.2 Synthetic scripts

Words are written in one of four script types: alphabetic (phonemes), syllabic (CV, V and C
units), logographic (word forms) and logo-syllabic (the 250 most frequent words as logograms, other
words spelled syllabically). Units map to random sign identifiers. Optional phenomena are
allographs, homophones, polyvalent signs, determinatives, word dividers and reading direction.

### 3.3 Calibration targets

Every target is listed in `config/indus_targets.yaml` with its citation, tolerance, the size of
the corpus it was measured on, and whether we read the number in the source ourselves. The Indus
point is 2,906 texts with mean length 4.60 (Mahadevan 1977, via Yadav et al. 2010 and Rao 2018).
Other targets are the longest text (17; Farmer, Sproat & Witzel 2004), the sign inventory (400-700),
the number of signs covering 80% of tokens (69), the share of the most frequent sign (0.10), and
the numbers of text-final and text-initial signs covering 80% of those positions (23 and 82), all
from Yadav et al. (2010). Two targets are not verified in a primary source: the median length (4,
from the project brief) and the hapax share of sign types (0.27, Possehl 2002 read via a secondary
source). Size-dependent statistics are computed on subsamples of the reference corpus size.

The duplicate-text rate is not a target, because no source fixes it for the corpus as a whole. We
report two published values as reference points: 0.354 for Mahadevan's concordance, read from the
vector data of Yadav et al. (2010, Fig. 2; 0.281 without its four most repeated texts), and 0.237
for the ICIT corpus, from a preprint we could not verify (Nair 2026). The figure in Yadav et al.
plots 2,591 texts, not 2,906; the paper does not say which texts are left out.

### 3.4 Calibration regimes

Three regimes control how much of the target set is imposed. `full` imposes every target.
`holdout` imposes only size, length and inventory, leaving the frequency and positional statistics
that Task A methods measure free, so that a method cannot be rewarded for statistics we injected.
`wrong_prior` imposes deliberately wrong targets (longer texts, smaller inventory). Results lead
with `holdout` wherever a method could exploit calibration.

### 3.5 Non-linguistic controls

The controls encode no language: heraldic bearings generated with the rule of tincture (one sign
per visual element), administrative slot tags, sparse Markov emblems with positional preferences,
the rigid and i.i.d. controls of Rao et al. (2009), and an adversarial Markov chain tuned to match
the entropy ratio of the language corpora. Japanese kamon descriptions are text and are reported
separately as a contaminated control.

### 3.6 Knowledge tiers and the synthetic sister language

Tasks C (language family) and D (sign values) are run at three levels of solver knowledge.
`related` gives the solver one reference language, a synthetic sister of the hidden language.
`candidates` gives the sister together with every other benchmark language, so the solver must
choose. `none` removes the hidden language and its sister. Only `candidates` and `none` are
relevant to the Indus case, because no close relative of the Harappan language is agreed, and we
do not know which of the two applies.

The sister is built from the half of the source text not used to generate the hidden corpus. A
seeded 30% of consonants and of vowels are permuted by a regular, bijective correspondence, and 20%
of word types are replaced by unrelated words of the same length. **The sister is therefore much
closer to the hidden language than any attested relative of an undeciphered script is likely to
be, in three measurable ways:**

1. **Oracle sound correspondences.** When the solver selects the sister, its frozen cognate step
   maps sister units to hidden-language units with the true correspondence table. We report every
   sister-tier score before this step. With the step, scores rise by 7-8 points (generator v1) and
   17-19 points (generator v2) in the `related` tier at the Indus point, and by up to 51 points on
   a single corpus. Those higher scores appear only as secondary numbers, labelled "with oracle
   sound correspondences".
2. **Shared text material: residual verbatim overlap.** The sister comes from the same source
   text. In the first version of the benchmark (sister-v1) the clauses were split into the two
   halves by position, so a clause that occurs more than once could fall in both halves. We
   corrected this (sister-v2): clauses are now split by a hash of their content, and no clause
   occurs in both halves. The correction moved no Indus-point mean outside its sister-v1 interval.
   **But word-for-word overlap remains high:** 38-82% of seal-like hidden texts, depending on the
   language (Tamil 38%, Sanskrit 51%, Latin 54%, Sumerian 79%, Finnish 82%), still occur verbatim
   inside some clause of the sister's half, because short phrases recur throughout a text in one
   language. A real relative would share far fewer exact phrases, since vocabulary, morphology and
   word order diverge. All sister-tier results in this paper carry this caveat.
3. **No structural divergence.** The sister keeps the hidden language's word order and morphology;
   only phonemes and a fifth of the vocabulary change. The sister's distance is a free parameter;
   a sweep over four distances is reported in the appendix.

Section 4.6 [robustness section, to be written] repeats the key comparisons with a stricter sister
(sister-v3), which drops every sister clause that contains any hidden text's word sequence; this
removes 33-42% of the sister's clauses at the Indus point and leaves 7-8% of the hidden texts' word
pairs in it (31-35% under sister-v2). Sister-v1 results are reported only as "upper bound
(sister-v1, known overlap)".

### 3.7 Methods, frozen

Eight method families run on every corpus behind one interface: conditional and block entropy
(after Rao et al. 2009), a bigram Markov model (after Yadav et al. 2010), positional histograms,
segmentation, script-type estimation by inventory rule and by classifier, a two-parameter tree (Lee,
Jonathan & Ziman 2010), a multi-feature language classifier, Knight-style EM, an EM cognate-matcher
and a frequency-rank baseline. All method code was frozen at the git tag `frozen-v1` before the
final runs; later changes touch only data generation and analysis.

EM needs a rule for choosing among candidate reference languages. The rule written before the runs
(the **original rule**) selects by raw likelihood with learned emissions for a pooled rare-unit
state. After the original rule selected Sumerian for almost every corpus, we wrote a **revised
rule** (uniform emissions for the pooled state; selection by bigram gain normalised by the
reference's own mutual information). The original rule is primary throughout; the revised rule is
reported as post hoc.

### 3.8 Tasks and scoring

Task A asks whether a corpus encodes language (balanced accuracy; chance 0.5). Task B asks for the
script type (accuracy; chance 0.25). Task C asks for the language family (accuracy against chance
of one over the number of candidate families). Task D asks for the value of each sign and is scored
as the share of sign tokens whose predicted value equals the true value; "success" is at least 50%.
Decision rules for Tasks A and B are learned leave-one-source-out, so a Sanskrit corpus is judged by
a rule fitted only on other sources. Means carry 95% cluster-bootstrap intervals that resample
source languages (or control families) and then corpora within them, because corpora from one
source are not independent. A shuffled-prediction control checks that the Task D scorer is not
generous: permuting a solver's predicted values across signs drops a 93% corpus to 0.9%.

Corpora are generated at three seeds per configuration (0-2) and replicated on fresh seeds (3-5).
Two generators are used. Generator v2 differs from v1 only in how text windows are sampled (first
the opening word type, then the rest); it was written to fix a missed text-beginner target and did
not fix it. Both generators meet the size and length targets in every corpus and the remaining
targets at similar, not identical, rates (all targets met by 12% of v1 and 8% of v2 language corpora
at the Indus point; full table in the appendix).

### 3.9 Sensitivity sweep

Duplicate-text rate and sign inventory are set exactly and varied independently on a 6 by 5 grid
(duplicates 0-0.5, inventory 400-800) at the Indus point, with methods frozen. Duplicates are set by
assembling a corpus from a larger pool of distinct texts plus copies weighted by popularity;
inventory is set through the allograph rate alone, by bisection. Because inventory is raised only
through allographs and no tested method merges allographs, the inventory axis measures robustness to
unmerged variants, not to a larger underlying sign system; every map states this. A cell counts
only if its corpora hit both settings within tolerance without distorting text lengths. The
plausible box (duplicates 0.2-0.4, inventory 400-700) was fixed before results were seen. Published
duplicate rates and sign-list sizes are marked on the map as reference points, not targets.

---

[Stop for review. Sections 4-7 not started.]
