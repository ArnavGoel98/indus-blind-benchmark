# v2 rank 2: Ugaritic-Hebrew anchor — plan (not yet run)

Status: plan for review, 2026-10-09, branch `v2`.
- Methods stay frozen at `frozen-v1`.
- New code is data and adapters only.
- Nothing here goes into the v1 paper.

## Question

The v1 "related" tier uses a synthetic sister that is much closer to the hidden language than any
real relative. This anchor asks what the frozen methods do when the hidden language is a real
ancient language and the reference is its real relative:
- on a real alphabetic script, Ugaritic;
- with a real related language, Biblical Hebrew;
- with real, uncontrolled distance: sound mergers, different vocabulary and morphology, different
  texts, and centuries apart.

It also measures that distance with the same yardsticks used for the synthetic sister (Table 2 of
the v1 paper), so that the sister can be placed relative to a real case.

## Data (licences read at source, 2026-10-09)

| Role | Source | What is available | Licence (as read) |
|---|---|---|---|
| Hidden language | EUPT TextAPI, eupt.uni-goettingen.de/api/eupt/ | Published tablets only: KTU 1.14, 1.15 and 1.16 (the Kirta epic). The Baal epic is scheduled for 2027-2029 | Each tablet manifest: `"license": [{"id": "CC-BY-SA-4.0"}]` |
| Reference language | Open Scriptures Hebrew Bible, `wlc/*.xml` (OSIS) | Westminster Leningrad Codex 4.20, whole Hebrew Bible | Repository LICENSE.md: WLC "is in the public domain"; the OSHB work is CC BY 4.0 with required attribution "Original work of the Open Scriptures Hebrew Bible available at https://github.com/openscriptures/morphhb" |
| Gold correspondences | Wikipedia, "Ugaritic alphabet", letter table, column "Corresponding letter in ... Hebrew" | One Hebrew letter per Ugaritic letter | Wikipedia text is CC BY-SA. The table cites Kogan (2011), Tab. 6.2, in Weninger (ed.), *The Semitic Languages*, p. 55, which we have **not read**; it is cited as "via Wikipedia" |

**Size.** The parsed EUPT transliteration of the three Kirta tablets is about 600 readable lines,
roughly 2,000-3,000 word tokens and 8,000-10,000 letter tokens. This is a first estimate from a
crude parse, to be replaced by exact counts. That is smaller than an Indus-scale corpus (about
13,400 sign tokens) and far smaller than our synthetic corpora's sources.

**Not used:**
- the Copenhagen Ugaritic Corpus (CC BY-NC 4.0);
- ETCBC BHSA (CC BY-NC 4.0);
- NeuroDecipher's Ugaritic-Hebrew cognate file (no licence).

**Release consequence.** Anything derived from EUPT and published (for example a challenge round)
must be released CC BY-SA 4.0 with attribution to EUPT. Raw texts are never redistributed, as in v1.

## Preparing the texts

**Ugaritic (hidden).**
- Parse the published transliteration HTML. Keep letters read as certain or damaged-but-read
  (marked ⸢ ⸣).
- Drop restorations in [ ], illegible x, and editorial deletions { }. Apply emendations as the
  edition gives them.
- One text = one tablet line. Words are split at the word divider; the divider itself is kept as a
  sign, as on the tablets.
- The three aleph signs (written a, i, u in EUPT) stay three distinct signs.
- Each of the about 30 letters is mapped to an arbitrary sign ID, which simulates an undeciphered
  alphabet. The answer key is the Ugaritic letter.

**Hebrew (reference).**
- Consonantal text only: strip vowel points and cantillation, map final forms to base letters, and
  treat maqaf as a word break.
- Shin and sin cannot be told apart without points, so they become one letter, as in the
  unpointed script.
- Units are letters (alphabetic unit level).
- Main reference: the whole Bible. Sensitivity reference: the poetic books (Psalms, Job, Proverbs),
  because Kirta is epic poetry.

**Gold table.** Each Ugaritic letter maps to its Hebrew correspondent from the table above. Several
Ugaritic letters share one Hebrew letter: ḫ and ḥ → ח, ṯ and š → ש, ḏ and z → ז, ẓ and ṣ → צ, ġ and
ʿ → ע, and the three alephs → א. This is many-to-one, unlike the v1 sister's one-to-one table. The
rare third sibilant ś is checked against the table when parsed.

## Which tasks apply

| Task | Applies? | Set-up | What "success" means |
|---|---|---|---|
| A: language or not | Yes, as a check only | Frozen rules fit on the v1 main run, applied unchanged (as for Sproat's corpora) | Called "language" by a method. This is weak evidence: Ugaritic is real language, but its 30-sign alphabet is far outside the training corpora (400+ signs) |
| B: script type | Yes | Frozen classifiers, no retraining | Predicts "alphabetic". The truth here is known |
| C: language family | Yes | `candidates`: Hebrew plus the five v1 languages at alphabetic unit level. `none`: the five v1 languages only | Picks Hebrew (Semitic) in `candidates`. Chance is 1/6 |
| D: sign values | Yes (main result) | Frozen EM, original rule (primary) and revised rule (secondary). Tiers: `related` = Hebrew only; `candidates`; `none` | Token accuracy against the gold table, counted correct when a sign is mapped to its gold Hebrew correspondent. The v1 success threshold of 50% of tokens is kept. Type accuracy is also reported (letters right out of about 30) |

**Score labels.**
- The real reference has no oracle cognate step, because there is no true sound-correspondence
  table to hand the solver. Every score is therefore "before the cognate step" by construction, the
  same as the v1 primary label.
- The revised rule is post hoc, as in v1.

**Size conditions.**
- (a) Natural lines, all published text.
- (b) The same tokens re-cut into texts of mean length 4.6 signs, the Indus mean, to see whether
  text length matters on real data.
- (c) Indus scale cannot be reached: the published text is smaller. This is stated, not padded.

## Distance yardsticks (real relative vs synthetic sister)

These are computed for Ugaritic-Hebrew and set beside v1 Table 2:
1. **Verbatim shared text:** the share of Ugaritic lines whose gold-mapped letter sequence occurs in
   the Hebrew reference. Expected near 0, against 30-56% for the synthetic sister.
2. **Correspondence structure:** the number of mergers, against none for the v1 sister.
3. **Cognate-form overlap:** the share of Ugaritic word types whose gold-mapped consonant skeleton
   occurs as a Hebrew word type. This is a crude upper bound on shared vocabulary, because chance
   matches of short skeletons inflate it. Chance is estimated by shuffling the letter mapping.
4. **Bigram distance:** Jensen-Shannon divergence between the letter-bigram distributions of
   gold-mapped Ugaritic and Hebrew. It is computed the same way for each v1 hidden language and its
   sister.

## What would count as informative

- **If the frozen EM recovers most Ugaritic letters with Hebrew as the only reference:** a small
  alphabetic corpus with a real relative is decipherable by these methods. The v1 `related` tier is
  then optimistic mainly in degree.
- **If it fails in `related`:** the v1 sister tier is optimistic in kind, and the v1 related-tier
  numbers should be read as upper bounds even more strongly.
- **Either way:** the yardsticks give the synthetic sister a real reference distance, which
  roadmap item 6 (realistic sister) needs as its target.

## Comparisons with published work

Snyder, Barzilay & Knight (2010) and Luo, Cao & Barzilay (2019) report Ugaritic-Hebrew results, but on
a different task: cognate and lexicon matching with a gold lexicon, not letter values from running
text. We will not put their numbers beside ours unless we have read them in the papers and the tasks
match. In any case, we will not use their data, which has no licence.

## Effort and order

| Step | Effort |
|---|---|
| EUPT parser and exact counts | 0.5 day |
| OSHB parser | 0.5 day |
| Gold table plus check | 0.25 day |
| Adapters to the v1 Corpus/Knowledge interfaces | 0.5 day |
| Runs: minutes of compute | 0.25 day |
| Yardsticks | 0.5 day |
| Report | 0.5 day |
| **Total** | **about 3 days** |

## Risks

- **Small, single-genre corpus.** One epic, about 10,000 letters. Results may change when the Baal
  epic is published.
- **Damaged text.** Dropping restorations removes letters and breaks words. Keeping them would score
  modern restorations, so they are dropped.
- **Gold table from a secondary source.** Kogan (2011) has not been read. Disputed correspondences,
  such as Ugaritic š vs Hebrew שׂ/שׁ, are handled by collapsing shin and sin.
- **Not Indus-like.** It is an alphabet of about 30 signs, not logo-syllabic, so the anchor
  calibrates relative distance and not Indus difficulty.
- **Chronology.** Biblical Hebrew is centuries later than Ugaritic and a different genre; this is
  part of what makes the anchor realistic.
- **Unit-level oracle.** The solver is told the unit level (letters), as in v1 Task D.

## Amendment before the run (2026-10-09, after b05772d was pushed; no scores seen)

Added at the user's request:
1. **Many-to-one scoring.** A sign counts as correct when it is mapped to its gold Hebrew
   correspondent, so ḫ and ḥ both mapped to ח are both correct. The v1 scorer already compares each
   token with its own gold value; `tests/test_ugaritic.py` checks this. EM chooses each sign's value
   independently, so it can produce many-to-one maps. The frequency-rank baseline is one-to-one by
   construction, so its best possible score (the one-to-one ceiling) is reported beside it.
2. **Frequency-rank baseline** (`baseline_frequency_rank`, frozen) reported beside EM in every tier.
3. **Exact sources.** EUPT pages `KTU_1.14_facsimile.html`, `KTU_1.15_facsimile.html` and
   `KTU_1.16_facsimile.html` under https://eupt.uni-goettingen.de/api/eupt/html/, edition version
   "Draft 3.2 [2025-07-18]", fetched 2026-10-09; SHA-256 recorded in `src/ibdb/data/ugaritic.py` and
   checked on every load. OSHB commit 3d15126fb1ef74867fc1434be1942e837932691f.

Details fixed while parsing, before any scoring:
- **Size.** Exact counts replace the estimate: 6,928 tokens (5,876 letters and 1,052 word
  dividers) from 678 tablet lines with readable text. Smaller than the planned 8,000-10,000.
- **Texts.** A restoration [ ] or an illegible x ends a text: each readable run between gaps is
  one text (primary, "natural"), so dropping text never creates false neighbours. Whole tablet
  lines with gaps joined are a sensitivity check. Erased signs ([[ ]]), the tablet's wrong sign in
  a correction, and editorial additions < > and deletions { } are dropped without a gap.
- **Word dividers.** The primary token accuracy follows the v1 convention: every token counts, and
  dividers are unrecoverable (no Hebrew unit). Letter-only accuracy is reported beside it.
- **Gold source gap.** The Wikipedia table leaves the Hebrew cell empty for ỉ and ủ (and s₂, which
  does not occur in Kirta). The plan's mapping of all three aleph signs to א is kept; accuracy
  without ỉ and ủ tokens is also reported.
- **Yardstick 1** is computed on letters with dividers removed (Hebrew has no divider unit),
  against a chance level from shuffled mappings, also for texts of 6+ letters.
