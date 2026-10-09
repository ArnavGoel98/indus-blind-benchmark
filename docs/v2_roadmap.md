# IBDB stage 2 (v2) roadmap

Status: draft for review, 2026-10-09. Branch `v2`. `main` receives only v1 fixes from reviewer comments.

Ground rules:
- v1 methods stay frozen at `frozen-v1`.
- New v2 methods get their own freeze tag, `frozen-v2`, before any v2 final run.
- Every v2 result is labelled v2 and never overwrites a v1 number.
- Licences below were read at the source on 2026-10-09 unless marked otherwise.
- "Not verified" means we could not read the terms ourselves.

## Ranking (impact / effort)

Impact is scored 1-5 by how much the item changes what the paper can claim. Effort is in working days, including the write-up, and assumes no new run larger than the v1 main run.

| Rank | Item | Impact | Effort (days) | Impact / effort | Licence status | v1 limitation addressed |
|---|---|---|---|---|---|---|
| 1 | 7. Allograph-merging method | 3 | 2.5 | 1.2 | No external data | 1 (allograph merging); reinterprets the inventory axis of the map |
| 2 | 3. Real decipherment anchor: Ugaritic-Hebrew first, Linear B-Greek second | 5 | 5 | 1.0 | Ugaritic: CC BY-SA (EUPT) or CC BY-NC (CUC). Hebrew: public domain text. Linear B: CC BY-NC-SA (DAMOS) | 2 (sister optimistic), 4 (no positive control for the cognate-matcher) |
| 3 | 4. More source languages (Ancient Greek, Akkadian, Egyptian, Biblical Hebrew) | 4 | 4 | 1.0 | All checked open; three are share-alike | 7 (few clusters), 5 (genre), partly 10 (CDLI licence) |
| 4 | 1. NeuroDecipher (Luo, Cao & Barzilay 2019) | 4 | 4 | 1.0 nominal; **blocked** | **No licence in the repository** | 17 (no neural model) |
| 5 | 6. Mixed-language and diachronic corpora | 3 | 4 | 0.75 | No external data | 6 (one language, one fixed script) |
| 6 | 2. Realistic sister language | 5 | 7 | 0.71 | No external data (optionally sound-change data from item 3) | 2 (sister optimistic): the main caveat on headlines 3 and 4 |
| 7 | 5. Improved logo-syllabic script model | 3 | 5 | 0.6 | Depends on item 4 (Akkadian, Egyptian) | Logo-syllabic results (Sections 4.4, 4.7); partly 3 |

**Recommendation.** Start with item 7, allograph merging. It needs no data and no permission, and it is the cheapest item. It also changes how the inventory axis of the published map can be read.

On day 1, send two requests so the slow items are not waiting later:
- Licence or permission for NeuroDecipher from its author (item 1).
- Confirmation of DAMOS export and reuse terms (item 3, Linear B).

Then do item 3 (Ugaritic-Hebrew), then item 4. Item 2 is the most important for the headlines, but it is also the most expensive. Item 3 gives it a real target for how far a relative should be, so do it after item 3.

---

## 7. Allograph-merging method (rank 1)

**What.** A new Task D pre-processing method that proposes which sign types are variants of one another, then merges them before decipherment. Candidate approaches:
- distributional similarity: shared left and right contexts, and complementary distribution;
- clustering with a stopping rule.

Scored against the hidden allograph map: pairwise precision and recall, and merged-inventory error. Also scored end to end, as Task D with and without merging.

**Data and licence.** None. It uses existing synthetic corpora, whose keys already record allographs.

**Effort.** 2.5 days:
- 1 day for the method;
- 0.5 day for scoring;
- 1 day to re-run the sensitivity sweep's inventory axis with merging on, using sister-v2 settings and only the cells in the plausible box at first.

**v1 limitation addressed.** Limitation 1 ("Inventory rises only through allographs, which no tested method merges"). The map's inventory axis currently measures robustness to unmerged variants; with merging it can say how much of that loss is recoverable.

**Risks.**
- Merging may only work when allographs are in strict complementary distribution, which is how our generator makes them. That would overstate its value on real data.
- Mitigation: add a generator setting where allographs overlap in context (a v2 data change, labelled as such).
- A wrong merge destroys distinct signs, so false-merge rates must be reported, not only recall.

## 3. Real decipherment anchors (rank 2)

**What.** Use real lost-language / known-language pairs as anchors for how far a "related" language really is. The benchmark methods would run on the real script corpus with the real relative as the reference: a real-relative tier next to the synthetic sister.
- Ugaritic with Biblical Hebrew comes first, because both have open texts.
- Linear B with Greek comes second.

**Data sources and licences.**

| Corpus | Content | Licence (as read) | Evidence | Use |
|---|---|---|---|---|
| EUPT, Edition des ugaritischen poetischen Textkorpus (Göttingen) | 68 poetic tablets, about 4,000 lines | "Creative Commons Attribution-ShareAlike 4.0 International License" | uni-goettingen.de/en/672442.html | Preferred Ugaritic source. Download format not stated on the page; may need export or contact |
| Copenhagen Ugaritic Corpus (DT-UCPH/cuc) | 278 KTU tablets, Text-Fabric | CC BY-NC 4.0 | README badge, github.com/DT-UCPH/cuc | Larger, but non-commercial. Usable for research; constrains any public release |
| Open Scriptures Hebrew Bible (morphhb) | Westminster Leningrad Codex with lemma and morphology | WLC text "remains in the Public Domain"; lemma and morphology CC BY 4.0 | README, github.com/openscriptures/morphhb | Known language for Ugaritic. Preferred over ETCBC BHSA, which is CC BY-NC 4.0 |
| DĀMOS, Database of Mycenaean at Oslo | Linear B texts with notes and metadata | Content "CC BY-NC-SA 4.0"; software GPL-3.0 | damos.hf.uio.no/about/online/ | Linear B source. **No bulk export found**; must ask the project |
| Perseus canonical-greekLit | Ancient Greek texts (TEI) | "Unless otherwise indicated ... CC BY-SA 4.0" | README, github.com/PerseusDL/canonical-greekLit | Known language for Linear B (alphabetic Greek is a distant stand-in for Mycenaean) |
| NeuroDecipher data files (linear_b-greek.cog, uga-heb.no_spe.cog) | Cognate lists, not running text | **No licence**; README says the Ugaritic file was "obtained from Ben Snyder" | github.com/j-luo93/NeuroDecipher | Not usable without permission; useful only as a cross-check |

**Effort.** 5 days for Ugaritic-Hebrew:
- 1.5 days for parsers;
- 1 day for alignment of units (Ugaritic alphabetic cuneiform against consonantal Hebrew);
- 1 day for runs;
- 1.5 days for the write-up.

Linear B adds about 3 days once DAMOS data are obtainable.

**v1 limitations addressed.**
- Limitation 2: gives a measured distance for a real relative, against which the synthetic sister can be compared.
- Limitation 4: the cognate-matcher has no positive control; Snyder et al. (2010) and Luo et al. (2019) report Ugaritic results to compare against.

**Risks.**
- Licences:
  - EUPT is share-alike, so derived corpora would have to be released CC BY-SA.
  - CUC and DAMOS are non-commercial, so they can be used internally and in the paper's numbers, but challenge rounds built from them would carry NC terms.
- Neither Ugaritic nor Linear B is at Indus scale or in Indus genre: Ugaritic poetry has long lines, and Linear B is administrative.
- The anchor measures relative distance, not Indus difficulty.
- Linear B data access may take weeks.

## 4. More source languages (rank 3)

**Candidates and licences.**

| Language | Source | Licence (as read) | Evidence | Notes |
|---|---|---|---|---|
| Ancient Greek | Perseus canonical-greekLit | CC BY-SA 4.0, "unless otherwise indicated" | repository README | Indo-European; alphabetic. Check per-text exceptions |
| Akkadian | ORACC downloadable snapshot, May 2019 (Language Bank of Finland, `oracc-2019-05-vrt`) | "CC-BY-SA (https://creativecommons.org/licenses/by-sa/4.0/)" | kielipankki.fi README.txt | Semitic; logo-syllabic cuneiform; includes royal inscriptions and letters (genre). ORACC's own licensing page returned HTTP 503: per-project terms **not verified** |
| Egyptian | Thesaurus Linguae Aegyptiae datasets on Hugging Face (Earlier Egyptian, Late Egyptian, Demotic) | `license:cc-by-sa-4.0` | Hugging Face API dataset tags (card text not read) | Afro-Asiatic; logo-consonantal. Strong second logo-syllabic-type anchor |
| Biblical Hebrew | Open Scriptures Hebrew Bible | Public domain text; CC BY 4.0 annotations | repository README | Semitic; abjad. Doubles as the Ugaritic reference in item 3 |

These give 9 source languages and 6 families in place of 5 languages and 4 families. Not chosen: ETCSL Sumerian (no open licence), ETCBC BHSA (NC), PROIEL treebanks (NC; not re-checked).

**Effort.** 4 days:
- 2 days for parsers and clause extraction;
- 1 day for calibration;
- 1 day of compute and checks.

A full v2 main run at the v1 scale with 9 languages is about 1.8 times the v1 run time.

**v1 limitations addressed.**
- 7: few clusters. Nine languages give more reliable cluster-bootstrap intervals.
- 5: genre. ORACC includes royal inscriptions and administrative letters.
- 10: CDLI licence. Akkadian and Egyptian give openly licensed cuneiform and hieroglyphic material for public rounds.

**Risks.**
- Share-alike terms apply to any published derived corpus.
- ORACC project-level terms are unconfirmed.
- Ancient Greek and Hebrew texts are mostly literary and religious, so the genre caveat remains for them.
- Adding languages changes all pooled v1 numbers: v2 must report v1-language-only and all-language results separately.

## 1. NeuroDecipher (rank 4; blocked)

**Repository.** github.com/j-luo93/NeuroDecipher (read 2026-10-09).

**Licence.**
- No LICENSE, LICENSE.md or LICENSE.txt in the repository root.
- setup.py declares no licence.
- The submodules `arglib` and `dev_misc` also have no LICENSE file.
- Under default copyright this means **all rights reserved**: running it privately for research is a grey area, and redistributing or vendoring it is not allowed.
- **Action:** ask the author for a licence or written permission before using it.

**Dependencies (from README and requirements.txt).**
- PyTorch ">= 1.3".
- Python packages: cython, ortools, cvxopt, pandas, prettytable, tensorflow, treelib, enlighten, pytrie, colorlog, numpy.
- Three local packages: `editdistance`, `arglib`, `dev_misc`.
- The requirements are unpinned and the code is from 2019, so expect version breakage (TensorFlow is listed alongside PyTorch).

**Does it run at Indus scale?**
- The model deciphers at the word level from two vocabularies, the lost language and the known language.
- It needs word segmentation of the lost script, which the Indus corpus does not have. On our corpora it would have to use either the hidden gold word boundaries (an oracle, labelled as such) or our branching-entropy segmentation.
- Vocabulary size at the Indus point is small, a few thousand word types, so compute is not the problem. Segmentation and the need for a single known relative are.
- It is meaningful only in the `related` tier.

**Effort.** 4 days once permission is granted:
- 1 day for the environment;
- 1.5 days for an adapter from our corpora to its cognate-list input;
- 1.5 days for runs and the write-up.

**v1 limitation addressed.** Limitation 17 ("No neural decipherment model is evaluated").

**Risks.**
- Licence refusal or no reply.
- Dependency rot.
- The method assumes a close relative with shared cognates, which is our most optimistic tier.
- Results with oracle segmentation would overstate it.

## 6. Mixed-language and diachronic corpora (rank 5)

**What.** Generator options for:
- corpora that mix two languages in one script, with a set share each;
- corpora written in a script that drifts over time. Drift means sign forms splitting or merging, and inventory and value changes across periods, with period labels hidden.

Score how Tasks A-D degrade with the mix share and the amount of drift.

**Data and licence.** None new. It uses existing languages, plus item 4's if available.

**Effort.** 4 days:
- 2 days for the generator;
- 1 day for calibration checks;
- 1 day for runs and the write-up.

**v1 limitation addressed.** Limitation 6. The Indus script changed over about 700 years and may have written more than one language (Kenoyer & Meadow 2010; Kenoyer 2020b).

**Risks.**
- The likely result, that recovery falls, is predictable, so the value is in the size of the drop.
- The drift model is our invention, with no published Indus drift rates to calibrate against; it must be framed as a sensitivity analysis.

## 2. Realistic sister language (rank 6)

**What.** Replace the v1 sister with one built by:
- conditioned sound changes, depending on neighbouring sounds and word position;
- mergers and splits, so correspondences are no longer one-to-one;
- morphological divergence: affix loss and replacement;
- word-order divergence;
- independent source text, with no shared clauses.

Sweep the distance. Calibrate the realistic range against item 3's measured Ugaritic-Hebrew distance.

**Data and licence.** None required. Sound-change patterns are coded from general phonology; optionally checked against item 3.

**Effort.** 7 days:
- 3 days for the sound-change and morphology engine;
- 1 day for the word-order component;
- 1 day for a non-oracle cognate step, since the solver can no longer be given the true table;
- 2 days for runs and the write-up.

**v1 limitation addressed.** Limitation 2, the main caveat on every sister-tier result, including headlines 3 and 4.

**Risks.**
- Headline 4's three- to fivefold contrast may shrink or vanish. That is a real result, but it must be framed as v2 and not overwrite v1.
- With a realistic sister, the frozen cognate step no longer applies. A new cognate method is needed, and it must be frozen as part of `frozen-v2`.
- Distance parameters remain free unless anchored by item 3.

## 5. Improved logo-syllabic script model (rank 7)

**What.** Replace the v1 logo-syllabic generator with one fitted to real logo-syllabic writing:
- logogram share by word frequency;
- phonetic complements;
- determinatives;
- polyvalence.

Fit it to ORACC Akkadian and TLA Egyptian sign statistics from item 4.

**Data and licence.** Depends on item 4: ORACC (CC BY-SA 4.0 snapshot; project terms not verified) and TLA (CC BY-SA 4.0 tags).

**Effort.** 5 days after item 4:
- 2 days for sign-statistics extraction;
- 2 days for the generator;
- 1 day for runs.

**v1 limitation addressed.** The logo-syllabic results (Sections 4.4 and 4.7) rest on our own script model, and the candidates-tier contrast is unresolved there. It also sharpens limitation 3 (oracle script type), because script-type estimation can be tested on real logo-syllabic statistics.

**Risks.**
- Fitting to Akkadian and Egyptian makes "logo-syllabic" mean "like these two".
- The Indus script's type is itself unknown.
- Extraction of logogram/syllabogram roles from ORACC transliteration needs care: determinatives, sign readings.

---

## Release and freeze plan

1. v2 data changes, meaning generator options and new languages, are tagged `data-v2` when complete.
2. New v2 methods (allograph merging, non-oracle cognate step, NeuroDecipher adapter) are developed on `v2`. They are frozen as `frozen-v2` before any v2 final run, and the freeze is recorded in the analysis history.
3. Every v2 table states its versions: frozen-v1 or frozen-v2 methods, data-v1 or data-v2.

## Tag that could not be pushed

The proxy refused the tag push from this session. To push `paper-v1` (main at aa9a359) from your machine:

    git fetch origin && git tag -a paper-v1 aa9a35967cd0bf34feacbf610adb35e472d46ae5 -m "Paper v1 as submitted for review" && git push origin paper-v1
