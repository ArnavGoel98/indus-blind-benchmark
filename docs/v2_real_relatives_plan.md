# v2 rank 6b: real related languages from different texts — plan (not yet run)

Status: approved 2026-10-15 (pre-registration entry 5), branch `v2`. Order: Finnish-Estonian and
Latin-Italian first; the Dravidian pairs only after the Wikisource provenance check. Replaces the
synthetic-sister calibration, which was killed (`docs/v2_negative_results.md`, item 2).

**Status update 2026-10-21:** run. Yardsticks in `reports/v2/real_relatives/`; Tasks C and D at `frozen-v2` (entries 6-8) in `reports/v2/cd/`; draft section in `reports/drafts/v2_real_relatives_section_DRAFT.md`. Finnish-Estonian (gold source not yet received) and Sanskrit-Pali (no text with clear terms) are still pending.

**Status update 2026-10-24:** Finnish-Estonian done directly on the owner's instruction: Pajusalu (2012) fetched from the Internet Archive copy of the sgr.fi URL (the society's link now redirects), read in full; it has no correspondence table, so the gold is built from the ten Finnish-North Estonian pairs it prints (entry 9; 14 of 27 rows sourced). Sanskrit-Pali: SuttaCentral's licensing page (read 2026-10-24) says the root texts are public domain but asks that its content not be used "for the creation of datasets for generative AI or similar"; still blocked pending permission. Draft request: `docs/v2_pali_permission_request.md` (not sent). The bracket of entry 4 did not hold for the real relatives (`docs/v2_negative_results.md`, item 3).

## Idea

For each v1 language except Sumerian, use a real related language, written in **different texts**,
as the `related` reference. The hidden corpora stay exactly the v1 corpora (Indus point, v1
generator), so results remain comparable with v1. The Ugaritic-Hebrew yardsticks are measured on
each pair. There is **no tuning and no targets**: whatever distance each real pair has is the
distance used.

Sumerian is an isolate, so it has no relative and stays in the `none` tier only.

Not every pair is a pair of sisters. Pali and Italian descend from forms close to Sanskrit and Latin,
and Malayalam from a western dialect of Old Tamil. Finnish-Estonian and Tamil-Kannada are true
sister pairs. Every pair is labelled with its relationship.

## Pairs, sources and licences (checked at source, 2026-10-11)

| Hidden (v1 source) | Relative | Text (different from the hidden text) | Licence, as read at source | Status |
|---|---|---|---|---|
| Sanskrit (DCS Rāmāyaṇa) | **Pali** (Middle Indo-Aryan) | Pali canon | **Unresolved.** SuttaCentral's `bilara-data` has no licence file for the root Pali texts; its README requires CC0 for translations only. SuttaCentral pages are reported to ask that their content not be used for "model/algorithm development or AI-derived technologies". VRI's Chaṭṭha Saṅgāyana text is free for non-commercial use only. The CC0 R packages `tipitaka` and `tipitaka.critical` (CRAN, licence field "CC0") repackage VRI, SuttaCentral, PTS (via GRETIL) and other editions, so CC0 there does not settle the upstream terms. | **Blocked.** Proposed: ask SuttaCentral for permission, as with Sproat's corpora. |
| Finnish (Kalevala, PG #7000) | **Estonian** (sister, Finnic) | Kreutzwald, *Kalevipoeg* (1857-61), Estonian Wikisource, 20 cantos | Site licence (API): CC BY-SA 4.0. Text public domain (author died 1882). | Usable |
| Latin (Caesar, Vergil; PG) | **Italian** (descendant) | Dante, *La Divina Commedia*, Project Gutenberg #1000 | "Public domain in the USA" (Gutenberg page) | Usable |
| Old Tamil (Project Madurai, Sangam) | **Malayalam** (descendant of a western Old Tamil dialect) | Ezhuthachan, *Adhyātma Rāmāyaṇam Kiḷippāṭṭu* (16th c.), Malayalam Wikisource | Site licence (API): CC BY-SA 4.0; text public domain by age. The Wikisource transcription's provenance is to be checked page by page: a scanned edition on Internet Archive is CC BY-NC-ND and must not be the source. | Usable if provenance is clean |
| Old Tamil | **Kannada** (sister, South Dravidian) | Kumāravyāsa, *Karṇāṭa Bhārata Kathāmañjari* (15th c.), Kannada Wikisource | Site licence (API): CC BY-SA 4.0; text public domain by age. Provenance checked as for Malayalam. | Usable if provenance is clean |

Tamil gets two relatives: Malayalam (close) and Kannada (more distant). This gives a *measured*
more-distant real relative, where the killed `distant` sister setting was only a guess.

**Sizes.** These are counted when parsed and reported before any yardstick, not estimated here. The
Commedia has about 14,000 lines and Kalevipoeg about 19,000 lines.

**Content overlap to watch.** The Malayalam text retells the Rāmāyaṇa. That does not overlap with
our Tamil texts (Sangam anthologies), but a Rāmāyaṇa retelling paired with our Sanskrit Rāmāyaṇa
would share names and story. If Pali is replaced by another Indo-Aryan text, that text must not be a
Rāma story. Verbatim overlap is measured for every pair.

## Unit level and spelling normalisation

The Hebrew lesson (pre-registration entry 3) applies: spelling conventions must not count as
language distance. Every pair is measured **as written** and **normalised**; the normalised value is
primary.

| Pair | Relationship | Units | Normalisation (primary) |
|---|---|---|---|
| Sanskrit-Pali | descendant | IAST letters, as the v1 Sanskrit profile | None needed; both romanised phonemically. Pali ṃ = Sanskrit ṃ. |
| Finnish-Estonian | sister | Letters, Finnish profile | Estonian **b, d, g** spell the short (lenis) stops that Finnish writes p, t, k; Estonian doubles letters to mark overlong quantity. Both are spelling conventions, and the normalised text maps them to the Finnish convention. Estonian õ, ü stay (ü vs Finnish y is a gold correspondence, not spelling). |
| Latin-Italian | descendant | Letters by greedy segmentation, as the v1 Latin profile, plus Italian digraphs ch, gh, gl, gn, sc | Strip accents (à → a); drop silent h; apostrophes split words. |
| Tamil-Malayalam (descendant), Tamil-Kannada (sister) | see pair | Phonemes from the script (deterministic converter, as `phonology.tamil_phonemes`) | Collapse the voicing and aspiration distinctions that Tamil script cannot write (Malayalam and Kannada write them, mostly in Sanskrit loans): kh, g, gh → k; and so on. Same purpose as removing Hebrew vowel letters. |

Each rule is listed in code with a test before any yardstick is computed.

## Gold correspondences, from sources we can read

Each table maps every hidden-language unit to its **regular reflex** in the relative ("elsewhere"
case) and to all **attested reflexes** the source lists (for the lenient score). It cites section or
page for every row, and is written only from the source below after reading it. Wikipedia is not
used for any gold value.

| Pair | Relationship | Source (open, read in full for the phonology sections) |
|---|---|---|
| Sanskrit-Pali | descendant | W. Geiger, *Pāli. Literatur und Sprache* (Strassburg, 1916), phonology chapters. Public domain; Internet Archive `in.ernet.dli.2015.70352` (full text, not restricted). |
| Finnish-Estonian | sister | K. Pajusalu, "Phonological innovations of the Southern Finnic languages", *Suomalais-Ugrilaisen Seuran Toimituksia* 266 (2012), open PDF at sgr.fi. Plus P. Kallio, "Historical phonology from Proto-Finnic to Proto-Livonian", *JEFUL* 7(1), 2016, open access, as a cross-check. |
| Latin-Italian | descendant | C. H. Grandgent, *An Introduction to Vulgar Latin* (Boston, 1907), public domain, Internet Archive `introductiontovu00gran` (open). It covers Latin to Romance with Italian outcomes, not Italian alone. The 1927 *From Latin to Italian* is on Internet Archive only as a lending copy of a 1971 reprint; it is used if an open full-view copy of the 1927 edition is found. |
| Tamil-Malayalam (descendant), Tamil-Kannada (sister) | see pair | R. Caldwell, *A Comparative Grammar of the Dravidian or South-Indian Family of Languages* (1856; Public Domain Mark on Internet Archive), with the 2nd edition (1875; Internet Archive `in.ernet.dli.2015.459581`). |

**Caveat, stated now.** Three of the four sources are over a century old. Basic consonant
correspondences are stable, but some details are outdated. Every row records its source, and rows the
source does not cover are marked "no source" and scored as unrecoverable (strict) rather than filled
in from memory.

## Measurements: the Ugaritic-Hebrew yardsticks, nothing tuned

The shared code (`src/ibdb/yardsticks.py`) is used, with each pair's gold regular reflexes as the
forward map. The hidden side is the v1 hidden half of each source; the relative side is the whole
relative text. Sample sizes match the anchor (5,876 units, 977 word tokens, 452 word pairs, the
anchor's 6+ letter text lengths).

Reported per pair, labelled sister or descendant in every table, as written and normalised:
- letter-pair JSD and JSD above the same-size floor;
- shared word forms and word pairs (raw and chance-corrected, chance from shuffled maps);
- verbatim overlap for texts of 6+ letters;
- number of mergers in the gold table;
- uncertainty: a bootstrap over relative texts (200 replicates, interval and SD; the upward bias of
  plug-in statistics under resampling is reported, as for the anchor).

These sit beside Ugaritic-Hebrew (as written and with vowel letters removed), the v1 sister and the
`harsh` bound. No setting is chosen from them.

## Use in Tasks C and D (only after the yardstick table is reported to you)

- **Tiers.**
  - New `related_real`: the relative only.
  - New `candidates_real`: the relative plus the other v1 languages.
  - These sit beside the bracket of pre-registration entry 4 (v1 sister upper bound, `harsh` lower
    bound).
- **Hidden corpora:** the existing v1 Indus-point corpora (both samplers), unchanged.
- **Methods:** frozen. Revised EM primary, original secondary (entry 1); frequency-rank baseline
  reported beside them.
- **Scoring:** entry 2. Strict primary (regular reflex), lenient secondary (any attested reflex),
  many-to-one accepted, before the cognate step. The 50% threshold is reported.
- **Script levels:**
  - alphabetic and syllabic: the relative's normalised phonemes, syllabified for syllabic scripts;
  - logographic and logo-syllabic logograms: the relative's word forms. A logogram is correct when
    mapped to the word that is the regular reflex of the hidden word. That is only defined for
    cognates, so logogram tokens of non-cognate words count as unrecoverable.

## Pre-registration

The text below becomes **entry 5** of `docs/v2_preregistration.md` on your approval of this plan,
before any download, parse or measurement. It is never edited after the run it governs.

> **5. Real related languages (rank 6b).** Pairs: Finnish-Estonian, Latin-Italian, Tamil-Malayalam,
> Tamil-Kannada; Sanskrit-Pali only if its licence is resolved; Sumerian none-only. Sources, unit
> levels, normalisation rules and gold sources as in `docs/v2_real_relatives_plan.md` at the
> commit that adds this entry. Measurements: the Ugaritic-Hebrew yardsticks, as written and
> normalised (primary), no tuning and no targets. Gold tables are written from the named sources
> only, with section or page per row; rows without a source are unrecoverable under strict scoring.
> Tasks C and D use tiers `related_real` and `candidates_real` beside the entry-4 bracket, with the
> frozen methods and the entry-2 scorer, and run only after the yardstick table has been reported.

## Effort

| Step | Effort |
|---|---|
| Parsers (Wikisource ×3, Gutenberg), sizes, provenance checks | 1 day |
| Malayalam and Kannada script converters, normalisation rules, tests | 1 day |
| Reading the four sources; gold tables with citations | 2 days |
| Yardsticks with bootstrap, report | 0.5 day |
| **Total before any Task C/D run** | **about 4.5 days** (Pali excluded) |

## Risks

- **Pali may stay blocked.** Then Sanskrit has only the bracket.
- **Old sources:** Caldwell 1856 and Geiger 1916 are dated. Each gold row is cited; gaps are marked,
  not filled.
- **Ancestor and descendant pairs** (Latin-Italian, Sanskrit-Pali) are not sister pairs, so they are
  labelled and reported separately from the sister pairs.
- **Script conversion** for Malayalam and Kannada is new code; it is tested on hand-checked words
  before use.
- **Genre and date mismatch** (Sangam poetry vs 15th-16th century epics; Caesar and Vergil vs Dante)
  is part of what makes these real pairs. It is reported, not corrected.
