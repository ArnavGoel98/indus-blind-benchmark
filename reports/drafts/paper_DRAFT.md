# DRAFT, sections 1-7 (for review; not for deposit)

**A Blind Benchmark of Decipherment Methods on Synthetic Scripts Calibrated to Indus Statistics**

*This work does not decipher, and does not claim to decipher, the Indus script.*

Conventions used throughout. Unless a sentence says otherwise, a recovery number is Task D token
accuracy under the **original (frozen) EM selection rule**, scored **before the cognate step**.
Scores that include the solver's cognate step are secondary and are labelled "with oracle sound
correspondences". The revised selection rule was adopted after the original rule had been run and
is reported as post hoc. Intervals are 95% and resample whole source languages.

[Reviewer notes in square brackets are not part of the text. Every citation below is one already
listed in the repository; entries marked "to verify" there are marked here too.]

## Plain-language summary

The Indus script, used in South Asia about 4,500 years ago, has never been read. Its inscriptions
are very short, and no text repeats an Indus message in a readable script. We asked:
could today's computer methods read writing like this if the answer were known? We wrote
five known languages in invented scripts, matched them to published Indus statistics, and hid the
key. The main method, expectation-maximisation (EM), guesses what each sign stands for, checks how
well the guesses fit a known language, and improves them. We score token accuracy: the
share of all signs in the texts that a method reads correctly. Methods were given either a close
relative of the hidden language (related), a relative mixed with unrelated languages (candidates),
or unrelated languages only (none). Without a relative, methods read about 5% of signs or fewer on average. With
one, results depended strongly on corpus properties that published statistics leave open.

---

## 1. Introduction

The Indus inscriptions are short. The concordance of Mahadevan (1977) holds 2,906 texts with
13,372 sign occurrences, about 4.6 signs per text (Yadav et al. 2010; Rao 2018), and the longest
text is commonly given as 17 signs on a single surface (Farmer, Sproat & Witzel 2004). Published sign lists count between 386 and
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
Indus-scale corpus is. Two generators that both match them differ roughly three- to fivefold when a
related language is available (frozen rule, no oracle correspondences: 2.4% vs 12.9% of sign tokens
on the main seeds, 5.3x; 2.7% vs 9.4% on fresh seeds, 3.5x; 2.6% vs 9.3% with the stricter
sister-v3, 3.7x). (4) Under the frozen rule, longer inscriptions help more than more
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

[Reviewer: see `reports/drafts/citation_check_2026-10-05.md`. Sproat (2010) verified; Sproat (2014)
and Lee, Jonathan & Ziman (2010) partly verified (volume/pages still to verify). Rao (2010) not cited.]

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
Other targets are the longest text (commonly given as 17 signs on a single surface; Farmer, Sproat &
Witzel 2004), the sign inventory (400-700),
the number of signs covering 80% of tokens (69), the share of the most frequent sign (0.10), and
the numbers of text-final and text-initial signs covering 80% of those positions (23 and 82), all
from Yadav et al. (2010). The median length (4) is unsourced (introduced during project planning; not from a primary or
secondary source). The hapax share of sign types (0.27, Possehl 2002) is read only via a secondary
source. Size-dependent statistics are computed on subsamples of the reference corpus size.

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
   **But word-for-word overlap remains high.** At the Indus point, the share of hidden texts that
   occur verbatim inside some clause of the sister's half averages 30-53% by language under
   generator v1 (Sumerian 30%, Tamil 36%, Latin 36%, Sanskrit 46%, Finnish 53%) and 43-56% under
   generator v2 (Latin 43%, Tamil 46%, Finnish 48%, Sumerian 55%, Sanskrit 56%), over 12 corpora per
   language (4 script types, 3 seeds); single corpora range from 8% to 90%. Short phrases recur
   throughout a text in one language, so splitting by clause cannot remove them. A real relative would share far fewer exact phrases, since vocabulary, morphology and
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


## 4. Results

Labels used in this section. **Primary**: original (frozen) rule, scored before the cognate step,
sister-v2. **With oracle sound correspondences**: the same runs scored after the cognate step.
**Upper bound (sister-v1, known overlap)**: runs made before the sister split was corrected; these
were scored only after the cognate step. The sensitivity sweep (Sections 4.3 and 4.5) was run once,
under sister-v1, so its numbers carry both labels and have no primary version.

### 4.1 Entropy statistics fail at Indus scale

This result does not depend on the sister language: Task A uses no reference language.

At the Indus point, the plug-in ratio of conditional to unigram entropy over the full sign alphabet
is 0.470 for an i.i.d. 420-sign control and 0.477 for the synthetic languages (10th-90th percentile
0.35-0.67); fresh seeds give 0.467 and 0.476. With Rao's merge to the 100 most frequent signs, the
i.i.d. control scores higher than the languages (0.696 vs 0.605). At this corpus size the statistic
cannot tell language from independent signs.

The classifier built on it separates languages from controls with balanced accuracy 0.77
[0.57, 0.90] when the generator is calibrated to every target (`full`). When the frequency and
positional targets are left free (`holdout`), it falls to 0.57 [0.32, 0.81], and to 0.49
[0.25, 0.75] on fresh seeds; both intervals include chance. Under `full`, every Task A method
classifies at least one structurally non-linguistic control family as language in all its corpora
(for the entropy classifier, the rigid control of Rao et al. 2009). We therefore treat language
detection at Indus scale as unresolved, and the `full` score as a product of calibration.

### 4.2 Without a related language

This result does not depend on the sister language: the hidden language and its sister are both
excluded from this tier, so no cognate step runs.

Without a related language among candidates, mean recovery stays at or below 4.8% in every run; no
corpus reaches 50% of tokens; the best single corpus reaches 28%.

| Run | Mean, original rule | Mean, revised rule (post hoc) | Best single corpus (original / revised) | Corpora >= 50% |
|---|---|---|---|---|
| Generator v1, seeds 0-2 | 1.8% | 3.3% | 16.4% / 18.1% | 0 of 60 |
| Generator v1, seeds 3-5 | 2.4% | 3.0% | 19.7% / 23.8% | 0 of 60 |
| Generator v2, seeds 0-2 | 3.3% | 4.8% | 23.2% / 27.6% | 0 of 60 |
| Sensitivity sweep, all valid cells | at most 4.6% per cell | at most 7.1% per cell | 24.6% / 27.9% | 0 of 1,571 |

Inside the plausible box the no-relative mean is at most 4.3% (fixed-composition panel: the
same 10 language-script combinations in every box cell), never above
7.1% anywhere on the grid. Longer texts do not change this: at 20 signs per text the no-relative
tier stays at or below 6.5%.

### 4.3 Difficulty is not fixed by published Indus statistics

Published Indus statistics do not fix how decipherable an Indus-scale corpus is. Two generators
that both match them differ roughly three- to fivefold when a related language is available.

| Candidates tier, Indus point | Generator v1 | Generator v2 | Ratio |
|---|---|---|---|
| Primary, seeds 0-2 | 2.4% [1.2, 3.8] | 12.9% [7.8, 17.4] | 5.3x |
| Primary, seeds 3-5 | 2.7% [1.2, 3.8] | 9.4% [4.7, 14.0] | 3.5x |
| Primary, sister-v3 (Section 4.6) | 2.6% [1.2, 4.2] | 9.3% [5.4, 13.5] | 3.7x |
| With oracle sound correspondences, seeds 0-2 | 2.8% | 18.9% | |
| Upper bound (sister-v1, known overlap), seeds 0-2 | 2.1% | 15.0% | |

No generator-v1 corpus reaches 50% of tokens in either seed set (primary); 6 of 120 generator-v2
corpora do. In the `related` tier the contrast is smaller in ratio but larger in points (primary,
seeds 0-2: 15.9% vs 30.2%).

The two generators differ only in how text windows are sampled. Both meet the size and length
targets in every corpus, and neither meets every target in more than 12% of language corpora, so
the published statistics do not choose between them. Corpus size also behaves differently: from 500
to 50,000 texts, generator v1 rises only from 2.5% to 3.7% (primary), while generator v2 rises from
3.5% to 18.7%.

Within one generator the duplicate rate and inventory matter less under the frozen rule. Across the
plausible box (duplicates 0.2-0.4, inventory 400-700), generator-v1 recovery stays at 3.5-5.1%
(box panel: the 10 language-script combinations valid in every box cell; upper bound (sister-v1, known overlap), with oracle sound
correspondences), and the median within-combination spread is 2.1 points (maximum 7.6). Generator-v2
corpora that fall inside the same box average 12.4% under the same labels, so the box does not bound
recovery across generators.

*Secondary, post hoc (revised rule):* primary scores 9.1% (v1) vs 25.1% (v2); within the v1 box the
revised rule ranges 8.7-21.8% and moves by up to 62 points within one language and script.

### 4.4 Longer inscriptions vs more inscriptions

Under the frozen rule, longer inscriptions help more than more inscriptions in both generators.
At equal total tokens (2,906 texts of 10 signs vs 6,317 texts of 4.6 signs, about 29,000 tokens
each, both run directly), candidates tier:

| Generator | Score | Longer | More | Difference, paired [95% CI] |
|---|---|---|---|---|
| v1 | Primary | 18.0% | 2.6% | 15.4 [5.8, 24.9] |
| v2 | Primary | 35.6% | 18.3% | 17.4 [8.5, 25.0] |
| v1 | With oracle sound correspondences | 28.6% | 2.7% | 25.9 [10.5, 41.4] |
| v2 | With oracle sound correspondences | 54.9% | 27.6% | 27.4 [12.8, 39.0] |

On fresh seeds (size interpolated on log tokens, no interval): v1 17.7% vs 3.4%, v2 32.2% vs 11.8%
(primary). The advantage holds from 10 signs per text in generator v1 and from 6 in generator v2.
Without a relative, both stay at or below 6.5%, with a small edge for length.

### 4.5 Archaeological predictions (prediction, not measurement)

No seals-only, tablets-only or single-period corpus was tested. The positions below place
qualitative published statements on the sensitivity map. All numbers here are upper bound
(sister-v1, known overlap), with oracle sound correspondences, under the frozen rule, generator v1.

A seals-only corpus (duplicates near 0, from "almost all ... unique" seals; Kenoyer & Meadow 2010)
falls where recovery is 3.5-14.5%; a tablets-only corpus (duplicates at or above the pooled 0.354,
a derived lower bound) falls at 1.4-4.9%. The direction holds in the strict panel, the 5 combinations valid in
every grid cell (0.7-20.5% vs 0.1-1.4%), and under the revised rule (18.0-38.6% vs 4.2-17.3%). Under the frozen rule the
seals-only region is high mainly at 400 signs. Without a related language every region stays at or
below about 7%. A single-period corpus (fewer signs than the pooled 400-450; Kenoyer 2020b) falls
below the smallest inventory we can build, so the map cannot place it. Every subset also holds
fewer than 2,906 texts.

### 4.6 Robustness: a sister with no shared hidden-text sequences (sister-v3)

Sister-v3 starts from sister-v2 and, for each corpus, drops every sister clause that contains any
hidden text's word sequence. Verbatim containment is then zero by construction. The filter removes
33% (v1) and 42% (v2) of sister clauses at the Indus point, and the share of hidden-text word pairs
still present in the sister falls from 31-35% to 7-8% (Sumerian keeps the most, 19-22%). Seeds 0-2,
both generators, Indus point and the equal-token comparison; 480 corpora.

| Indus point | v1, sister-v2 | v1, sister-v3 | v2, sister-v2 | v2, sister-v3 |
|---|---|---|---|---|
| `related`, primary | 15.9% | 12.4% | 30.2% | 27.3% |
| `candidates`, primary | 2.4% | 2.6% | 12.9% | 9.3% |
| `candidates`, with oracle sound correspondences | 2.8% | 2.6% | 18.9% | 12.3% |

Headline 4.3 holds: 2.6% [1.2, 4.2] vs 9.3% [5.4, 13.5], 3.7x, intervals not overlapping. Headline
4.4 holds: longer beats more by 13.6 [5.8, 21.3] points (v1) and 24.1 [11.9, 35.9] (v2), primary.
The filter depends on the corpus: many short texts remove more of the sister (40-52% of clauses)
than fewer long texts (9-15%), which favours the long-text condition. Sister-v3 therefore confirms
that the length advantage survives; it does not measure its size better than sister-v2.

The original rule chose the sister about as often under sister-v3 as under sister-v2 (v1: 20% vs
20% of corpora; v2: 28% vs 33%), and `related`-tier scores fell by about 3 points. Most of what the
solver recovers from the sister therefore does not come from shared exact phrases.

## 5. Limitations

1. **Allograph merging.** Sign inventory is raised only through allographs, and no tested method
   merges them. The inventory axis measures robustness to unmerged variants.
2. **Sister-language distance and closeness.** The sister keeps word order and morphology, comes from
   the same source text (verbatim overlap 30-56% by language under sister-v2), and is paired with
   oracle sound correspondences. Its distance is a free parameter. Sister tiers are optimistic.
3. **Oracle script type and unit level in Task D.** Solvers are told the script type; real
   decipherers are not.
4. **Text-beginner calibration.** Most corpora miss the text-beginner target (35-37% meet it), and
   generator v2 did not fix this.
5. **Median length is unsourced.** The target of 4 was introduced during project planning. It is
   not only checked but also used: it sets the spread of the generated length distribution, through
   sigma = (ln 17 - ln 4) / z. Removing it from the calibration objective would change nothing,
   because every corpus already meets it and an unmet target is the only kind that enters the
   objective. Removing it from the generator would require another assumption for the spread, whose
   effect is unknown without rerunning.
6. **CDLI licence.** Academic reuse with citation, not an open licence; Sumerian is excluded from
   published challenge rounds.
7. **The 2,591 vs 2,906 discrepancy** in the source of the M77 duplicate rate.
8. **Subset positions are estimated** from qualitative statements and raw counts.
9. **The single-period subset cannot be placed**; every subset is smaller than 2,906 texts.
10. **Post-hoc selection rule.** The revised rule was written after the original rule had run; the
    original rule is primary throughout.
11. **Sensitivity sweep under sister-v1.** The map and the archaeological predictions were run before
    the sister split was corrected and have no before-cognate scores.
12. **Plug-in entropy is biased at this scale**, so any fixed entropy cut-off depends on corpus size.
13. **Five languages, one genre each; controls built by us.** A classifier is only as general as its
    controls.
14. **No neural decipherment model is evaluated.** The EM cognate-matcher contains no neural network.

## 6. Blind challenge and reproducibility

The challenge has public rounds, which release corpora and keys, and hidden rounds, which release
corpora and SHA-256 commitments of their keys. Hidden keys are generated and held by the maintainer
and are not in the repository. Challenge corpora are written from secretly disguised sister
languages, so they cannot be matched against the public source texts. Each team gets one scored
submission per hidden round. Sumerian-derived corpora are excluded from all published rounds. The
static leaderboard marks entries whose authors claim a real Indus decipherment.

Every number in this paper can be regenerated from the repository. Method code is frozen at the tag
`frozen-v1` and the data release at `data-v1`; later changes (sister-v2, sister-v3 and the analysis
scripts) touch only data generation and analysis and are selected per run profile. Each run records
its generator and sister version. Source texts are fetched by the user under their own licences and
are never redistributed.

## 7. Conclusion

On synthetic corpora that match the published Indus statistics, mean recovery without a related
language stays at or below 4.8% in every run, and with one, recovery depends three- to fivefold on corpus properties that
those statistics leave open. A statement about how hard the Indus script is to decipher therefore has
to name its corpus (object types, period, duplication), its knowledge tier, and its selection rule.
None of these results bears on what the Indus signs mean.

---

## Back matter

**Data and code availability.** Code, configurations, run records and reports are in the
repository under the tags above; no third-party text is redistributed.

**Acknowledgements.** Code was developed with AI coding assistance.

[Reviewer: names of J. M. Kenoyer, S. Houston or R. Sproat are added only after each confirms.]

**References.** Only sources read, or marked "via". See `reports/drafts/citation_check_2026-10-05.md`
for verification status.

**Appendices.** Calibration, full result tables, sensitivity tables, the rule comparison, the audit,
the sister-v1/v2/v3 comparisons and method deviations.

[Stop for review.]
