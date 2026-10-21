# DRAFT v2 section (for review; not for deposit): real related languages written in different texts

Status: draft written 2026-10-20 on branch `v2` from the reports named in each paragraph. It does not
change any v1 number or the v1 paper (`paper-v1`). Every number here is a v2 result. Methods are
frozen at `frozen-v2` (commit `4ce3e90`); pre-registration entries 1-6 are in
`docs/v2_preregistration.md`. Nothing here is, or claims, a decipherment.

## v2.1 Why real relatives

The v1 `related` tier used a synthetic sister cut from the other half of the hidden language's own
source text. It shares phrases with the hidden text and keeps its vocabulary, morphology and word
order, so it is far closer than any attested relative of an undeciphered script is likely to be
(v1, Section 3.6, Table 2). Stage 2 first tried to make the synthetic sister realistic by
calibrating it to the distance between Ugaritic and Hebrew. That failed for all five languages in
both settings tried: every mechanism that changes letter pairs also destroys shared word forms, and
a sister cut from the same text keeps too much verbatim text (`docs/v2_negative_results.md`, item 2).
Stage 2 therefore measures real related languages written in different texts, with no tuning and no
targets: whatever distance each real pair has is the distance used (pre-registration entry 5).

## v2.2 Pairs, texts and gold correspondences

*Table v2.1. Real relatives. Each pair is labelled by relationship in every table.*

| Hidden (v1 source) | Relative | Relationship | Relative's text | Gold correspondences (cited per row) | Status |
|---|---|---|---|---|---|
| Latin (Caesar, Vergil) | Italian | descendant | Dante, *La Divina Commedia*, Project Gutenberg #1000 (public domain in the USA) | Grandgent (1907), section per row | measured |
| Old Tamil (Sangam anthologies) | Malayalam | descendant (of a western Old Tamil dialect) | Ezhuthachan, *Adhyātma Rāmāyaṇam Kiḷippāṭṭu*, Malayalam Wikisource (CC BY-SA 4.0) | Caldwell (1875), pages per row | measured |
| Old Tamil | Kannada | sister | Kumāravyāsa, *Karṇāṭa Bhārata Kathāmañjari*, Kannada Wikisource (CC BY-SA 4.0) | Caldwell (1875), pages per row | measured |
| Finnish (Kalevala) | Estonian | sister | Kreutzwald, *Kalevipoeg*, Estonian Wikisource, cantos I-XX | Pajusalu (2012), not yet read | text parsed; gold pending |
| Sanskrit (Rāmāyaṇa) | Pali | descendant | - | - | blocked: no text with clear terms |
| Sumerian | - | isolate | - | - | `none` tier only |

**Data notes.**

- The two Wikisource transcriptions state no source edition. They were accepted as clean by the
  project owner (2026-10-15): they carry the CC BY-SA site licence and do not link to the
  CC BY-NC-ND scan on Internet Archive.
- Kannada coverage is partial: 93 of the 154 sandhi pages linked from the ten parva pages exist,
  mostly Ādi, Virāṭa and Karṇa parvas. The two commentary (ಸಟೀಕಾ) pages are excluded. Each sandhi page
  opens with a short invocation that may be in Sanskrit; it was not removed.
- Revision ids and SHA-256 hashes per page are kept with the raw data.

**Units and spelling.** Units are those of the v1 hidden language: Latin letters by the v1 greedy
segmentation, and Old Tamil phonemes. Malayalam and Kannada script are converted to the same
phonemes by deterministic tables, tested on hand-checked words. Every pair is measured as written
and normalised, and the normalised value is primary, so that spelling conventions do not count as
language distance (the Hebrew lesson of v2 entry 3):

- Italian: accents stripped, j folded to i, silent h dropped, apostrophes split words.
- Malayalam and Kannada: the voicing and aspiration that Tamil script cannot write are collapsed
  (kh, g, gh → k, and so on).

**Gold tables.** Each hidden unit has a regular reflex (its outcome where no conditioned change
applies) and a list of attested reflexes, with the section or page of the source for every row.
Rows the source does not cover are marked "no source" and are unrecoverable under strict scoring
(Old Tamil h, s, ḵ, ṣ for both Dravidian relatives). Both sources are over a century old; their
basic consonant correspondences are standard, but details are dated. No gold value comes from
Wikipedia.

## v2.3 How far the real relatives are

The Ugaritic-Hebrew yardsticks (v2 anchor) are computed with the same code on each pair. Sample
sizes are matched to the anchor, and chance is estimated from shuffled correspondence maps.

**Cross-script comparisons are indicative only.** Shared word forms and word pairs are not directly
comparable between a consonant-only script (Ugaritic-Hebrew) and scripts that write vowels (all the
other rows): a consonant skeleton matches far more easily than a full word, even after the chance
correction. Comparisons within one script type are the meaningful ones.

*Table v2.2. Yardsticks, normalised spelling (primary). cc = chance-corrected. Real-pair intervals:
bootstrap over the relative's lines, 200 replicates, 95%.*

| Pair | Relationship | Script type | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ units |
|---|---|---|---|---|---|---|
| Ugaritic-Hebrew (vowel letters removed) | sister | consonant-only | 0.089 | 58.4% | 4.6% | 0.8% |
| Latin-Italian | descendant | alphabet | 0.104 (0.101-0.108) | 11.8% (9.6-11.5%) | 0.6% (0.1-0.7%) | 1.9% (0.7-3.3%) |
| Old Tamil-Malayalam | descendant | abugida | 0.139 (0.137-0.145) | 5.7% (4.0-5.2%) | 0.0% (0.0-0.0%) | 1.8% (0.4-2.4%) |
| Old Tamil-Kannada | sister | abugida | 0.180 (0.178-0.186) | 4.7% (3.8-5.1%) | 0.0% (0.0-0.1%) | 1.0% (0.4-2.4%) |
| Latin, v1-like sister / `harsh` | synthetic | as hidden | 0.006 / 0.135 | 53.1% / 7.8% | 7.1% / 1.1% | 12.4% / 2.4% |
| Old Tamil, v1-like sister / `harsh` | synthetic | as hidden | 0.002 / 0.185 | 57.6% / 3.6% | 8.5% / 0.1% | 17.8% / 1.8% |

For Latin-Italian and Malayalam the plug-in estimate of shared word forms lies above its own
bootstrap interval, because resampling duplicates lines and so lowers the share of distinct forms;
the interval is the conservative reading.

**Reading.**

- On these yardsticks the real relatives sit near the `harsh` setting and far from the v1-like
  sister. The v1 sister shares 4-12 times as many word forms as the real relatives.
- The descendant is closer than the sister, as expected: Malayalam is closer to Old Tamil than
  Kannada on the letter-pair distance, and the intervals do not overlap.
- Normalisation matters most where scripts differ most. Kannada writes voicing; collapsing it moves
  the letter-pair distance from 0.309 to 0.180 bits.

**What the verbatim matches are** (exploratory inspection, `reports/v2/real_relatives/verbatim.md`).
Verbatim runs of 6+ units occur in 1.4% (Malayalam), 1.6% (Kannada) and 2.5% (Italian) of sampled
windows, against 0.0-0.1% through shuffled maps and 0.3-0.4% for an unrelated language with a similar
open syllable shape (the v1 Finnish hidden half, letters as they are). They are therefore signal,
but not shared text:

- 60-73% of them run across a word boundary;
- they are mostly short shared morphs and phoneme strings (for example Malayalam *-kkoṇṭu*,
  *colliyatu*, *paricil*), and for Italian, cognate stems and Dante's Latinisms (*principi-*,
  *cantando*, *crudel-*);
- no match is a phrase that respects word boundaries on both sides, so they are not shared formulae.

In Malayalam about a quarter of the matches (35 of 143) exist only after normalisation. By
inspection, most of these pair a native Tamil string with a Sanskrit loanword: the loan is a
coincidental partner, not a shared loan.

## v2.4 Tasks C and D with real relatives

**Design** (entries 1, 2, 4-6).

- **Corpora:** the v1 Indus-point corpora (2,906 texts, mean length 4.6 signs), seeds 0-2, samplers
  A and B, four script types, with the corrected (content-split) sister: 6 corpora per hidden
  language and script type. They were regenerated from the same seeds; all 120 have corpus statistics
  identical to the v1 records (checked 2026-10-20).
- **References:** the relative's whole text at the script's unit level, as v1 writes its
  references:
    - phonemes for alphabetic scripts;
    - CV syllables for syllabic scripts;
    - word forms for logographic scripts;
    - for logo-syllabic scripts, word forms for the relative's 250 most frequent words and syllables
    otherwise.

    No reference carries a correspondence table, so every score is before the cognate step.

- **Tiers:** `related` gives the relative alone. `candidates` gives the relative plus the other v1
  languages.
- **Methods:** the frozen EM solver with the revised selection rule (primary), the original rule,
  and the frequency-rank baseline.
- **Scoring:**
    - Strict (primary): a sign token is right when its predicted unit is the regular reflex of the
    token's hidden value. A logogram is right only when its reflex is a word that occurs in the
    relative (a cognate). Many-to-one predictions are accepted.
    - Lenient (secondary): any combination of attested reflexes counts.
    - Every token counts. The share of tokens that have a strict reflex at all is reported as a
    ceiling.
- **Bracket rows:** beside the real relatives stand the v1 sister (upper bound, read from the v1
  records and scored with the v1 scorer before the cognate step) and `harsh` (lower bound).

*Table v2.3. Task D, `related` tier, revised EM, strict score: mean % of sign tokens over 6 corpora
(number of corpora at or above 50%). From `reports/v2/cd/results.md`.*

| Hidden | Relative | Relationship | Logographic | Syllabic | Logo-syllabic | Alphabetic |
|---|---|---|---|---|---|---|
| Old Tamil | v1 sister (upper bound) | synthetic | 0.0 (0) | 26.7 (0) | 19.0 (0) | 42.5 (2) |
| Old Tamil | **Malayalam** | descendant | 0.0 (0) | 6.2 (0) | 5.9 (0) | **30.4 (1)** |
| Old Tamil | **Kannada** | sister | 0.0 (0) | 3.3 (0) | 2.9 (0) | **32.2 (0)** |
| Old Tamil | `harsh` (lower bound) | synthetic | 0.1 (0) | 6.2 (0) | 5.9 (0) | 16.4 (0) |
| Latin | v1 sister (upper bound) | synthetic | 1.4 (0) | 32.2 (1) | 9.8 (0) | 45.4 (2) |
| Latin | **Italian** | descendant | 0.0 (0) | 6.0 (0) | 1.5 (0) | **16.9 (1)** |
| Latin | `harsh` (lower bound) | synthetic | 1.5 (0) | 24.4 (0) | 4.6 (0) | 36.1 (1) |

The real Ugaritic anchor, for comparison: 32.0% (revised EM) and 33.9% (original EM), natural text,
`related` tier, alphabetic, with its pre-registered 50% criterion failed (`reports/v2/ugaritic/results.md`).

*Table v2.4. Task C, `candidates` tier: share of corpora (24 per row, all script types) where the
solver picked the right family, and the references the revised rule chose.*

| Hidden | Relative offered | EM revised | EM original | Frequency rank | Chosen by EM revised |
|---|---|---|---|---|---|
| Old Tamil | Malayalam | 0% | 0% | 38% | Latin 16, Finnish 8 |
| Old Tamil | Kannada | 38% | 0% | 8% | Latin 10, Kannada 9, Finnish 5 |
| Latin | Italian | 25% | 0% | 50% | Finnish 18, Italian 6 |
| Old Tamil | v1 sister | 33% | 13% | 13% | Latin 13, sister 8, Finnish 3 |
| Latin | v1 sister | 96% | 8% | 63% | sister 23, Finnish 1 |

For Latin, picking Sanskrit also counts as the right family (Indo-European), as in v1.

## v2.5 What the results show

1. **No real relative brings any script type to 50% on average.**
      - In the `related` tier, 2 of the 72 real-relative runs reach 50% (3 relatives, 4 script types,
     6 corpora each). Both are alphabetic: one with Malayalam, one with Italian.
      - With revised EM, none of the 72 reaches 50% in the `candidates` tier.
      - Syllabic and logo-syllabic scripts reach 1.5-6.2% with a real relative.
      - Logographic scripts reach about 0%. Only 17-51% of their tokens have a cognate in the relative
     at all (the strict ceiling).
2. **Alphabetic scripts with a real relative land near the one real anchor.** Old Tamil with
   Malayalam or Kannada reaches 30-32%, close to Ugaritic with Hebrew (32-34%). These are two
   independent real cases on different data, with similar results.
3. **The bracket does not hold** (post hoc, `docs/v2_negative_results.md`, item 3).
      - Italian falls below the `harsh` "lower bound" for alphabetic, syllabic and logo-syllabic scripts
     (alphabetic 16.9% against 36.1%; below in 5 of 6 corpora).
      - Kannada falls below `harsh` for syllabic and logo-syllabic scripts (5 of 6 corpora each).
      - The real relatives therefore replace the bracket as the primary evidence for this tier. That
     reporting decision was taken after seeing the results.
4. **Measured closeness did not predict decipherability.** Italian is closer to Latin than `harsh`
   on every yardstick, yet harder for the solver. Kannada is further from Old Tamil than Malayalam,
   yet level on alphabetic Task D and less variable. The yardsticks measure how similar two texts
   are, not how hard a frequency-based solver finds the mapping.
5. **Task C rarely finds the real relative.**
      - The revised rule picks Italian for Latin in 6 of 24 corpora, Kannada for Old Tamil in 9 of 24,
     and Malayalam in none; it mostly picks Latin or Finnish.
      - This is the bias declared in pre-registration entry 1: the revised rule favours Latin.
      - The original rule picks Sumerian in all 72 real-relative corpora, which gives 0% here.
6. **Single runs are unstable.** For the same relative and script type, scores range from 0.0% to
   56.0% between corpora (Malayalam, alphabetic). The EM solver often lands in a poor optimum
   (`reports/v2/cd/per_corpus.md`). Means over 6 corpora are therefore imprecise. No test was
   pre-registered for these comparisons, and none is reported.

For Indus, where no relative is agreed and the `candidates` and `none` tiers are the relevant ones,
these results add one point: even a genuine relative, offered among the hypotheses, gives these
comparison-based methods little help outside alphabetic scripts.

## v2.6 Limitations of this section

1. **Two hidden languages only.** Latin and Old Tamil; Old Tamil has both relatives, so the two
   Dravidian rows share their hidden side and their gold source. Finnish-Estonian is waiting for its
   gold source and will run on the same frozen code. Sanskrit has no relative with clear terms.
2. **Relationship and text are confounded.** Each relative is one text of one genre and period;
   the effect of the relationship cannot be separated from that of the text.
3. **Old gold sources.** Caldwell (1875) and Grandgent (1907) are cited per row, gaps are marked
   rather than filled, and some details are dated.
4. **Unverified transcriptions.** The Wikisource transcriptions state no source edition, and
   Kannada coverage is partial.
5. **Normalisation choices.** Normalisation is fixed in code and tested, but it is a choice, and it
   moves the Kannada distance a great deal.
6. **Scoring choices.**
      - Task D is scored whatever reference the solver chose, as in v1, so a wrong reference can still
     score by coincidence.
      - The logogram cognate rule (the reflex must occur in the relative) makes logographic ceilings
     low by construction.
7. **v1 assumptions still apply.** The solver is told the script type (an oracle). The Ugaritic
   gold table is still secondary: Wikipedia, citing Kogan (2011), which we have not read.
8. **Six corpora per cell, with high variance.**

## v2 analysis history (dated)

- **2026-10-11:** synthetic-sister calibration killed; pre-registration entry 4 (the bracket).
- **2026-10-15:** pre-registration entry 5 (real relatives) before any download. Dravidian
  Wikisource texts accepted as clean by the project owner. Gold tables committed with citations
  before any measurement.
- **2026-10-17:**
    - Yardstick table reported before any Task C/D run.
    - Verbatim matches inspected (exploratory).
    - Pre-registration entry 6 (harness details) proposed after a pipeline check on development seed
    90 only. That check found a scorer error, fixed before the freeze: Sumerian numerals and
    written determinatives had been counted as unrecoverable.
- **2026-10-18:** entry 6 declared; methods tagged `frozen-v2` (commit `4ce3e90`); final run of
  120 corpora with no errors.
- **2026-10-20 (post hoc):**
    - Per-corpus table added.
    - The bracket failure recorded as negative result 3.
    - Real relatives made the primary `related`-tier evidence; the bracket is secondary.

## References (this section)

- Caldwell, R. (1875). *A Comparative Grammar of the Dravidian or South-Indian Family of
  Languages* (2nd ed.). London. Internet Archive `in.ernet.dli.2015.459581`.
- Grandgent, C. H. (1907). *An Introduction to Vulgar Latin*. Boston. Internet Archive
  `introductiontovu00gran`.
- Knight, K., Nair, A., Rathod, N., & Yamada, K. (2006). Unsupervised analysis for decipherment
  problems. In *Proceedings of the COLING/ACL 2006 Main Conference Poster Sessions* (pp. 499-506).
- Snyder, B., Barzilay, R., & Knight, K. (2010). A statistical model for lost language decipherment.
  In *Proceedings of the 48th Annual Meeting of the Association for Computational Linguistics*
  (pp. 1048-1057).
- Texts: Dante, *La Divina Commedia*, Project Gutenberg #1000. Ezhuthachan, *Adhyātma Rāmāyaṇam
  Kiḷippāṭṭu*, Malayalam Wikisource. Kumāravyāsa, *Karṇāṭa Bhārata Kathāmañjari*, Kannada Wikisource.
  Ugaritic: EUPT (Göttingen), CC BY-SA 4.0. Hebrew: Open Scriptures Hebrew Bible (WLC), CC BY 4.0
  annotations, text public domain.
- Not read, cited only as the source of a secondary table: Kogan (2011), via Wikipedia, "Ugaritic
  alphabet".
