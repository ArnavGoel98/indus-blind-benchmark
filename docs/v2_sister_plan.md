# v2 rank 6: realistic sister language — plan (not yet run)

Status: approved 2026-10-09 with two additions (distant setting; strict and lenient scoring), branch `v2`.
Nothing is built or run at the time of this commit. Methods stay frozen; the
new sister and any scoring change enter `frozen-v2` only after the acceptance checks below pass.

## Why

The v1 sister is far closer to the hidden language than a real relative. The Ugaritic-Hebrew anchor
(`reports/v2/ugaritic/results.md`) measured the gap on the same yardsticks:

| Yardstick | Ugaritic-Hebrew | v1 sister (5 languages) |
|---|---|---|
| Letter-bigram JSD, size-matched (bits) | 0.184 (same-size floor 0.018) | 0.014-0.087 |
| Sound mergers | 7 (29 letters -> 22) | 0 |
| Cognate-form overlap, word types (chance) | 55% (15%) | 52-75% (chance <= 10%) |
| Texts of 6+ letters found verbatim | 0.8% (chance 0.1%) | not comparable |

Goal: a sister generator ("sister-v4") whose yardsticks match Ugaritic-Hebrew, so that `related` and
`candidates` results stop being upper bounds by construction.

## What changes in the sister (built from the reference half, as now; v3's leak filter kept)

All changes act on phonemes before units are formed, so alphabetic, syllabic and logographic
scripts inherit them as now. Each is seeded per language.

1. **Mergers.** Merge a set of hidden-language consonant pairs into one sister consonant: many
   hidden phonemes, one sister phoneme, as Ugaritic ḫ and ḥ became Hebrew ח.
   - Count: 24% of the consonant inventory, the Ugaritic-Hebrew share (7 of 29). That gives Sanskrit
     8, Tamil 6, Latin 5, Finnish 5, Sumerian 4. Fixed at 7 as a sensitivity setting.
   - Pairs: we have no phonetic feature tables, so pairs are chosen first among graphemes sharing a
     base letter (ṭ/t, bh/b, ś/s, ḷ/l), then at random. This is cruder than real phonetics and is
     stated as a limitation.
2. **Conditioned sound changes.** A few rules of the form X -> Y / context (before a given vowel,
   between vowels, word-finally), so that one hidden phoneme has two sister reflexes depending on its
   neighbours. Plus final-vowel loss in a seeded share of words.
3. **Unconditioned shifts.** The existing bijective permutation, kept as a knob.
4. **Morphology.** Find each language's most frequent word-final and word-initial unit strings
   (affix candidates, by type frequency) and replace a share of them with different strings. Every
   word with that affix changes the same way, like a different inflection in the relative.
5. **Word order.** In a seeded share of clauses, move the last word to the front, or swap adjacent
   word pairs.
6. **Lexical replacement.** As now (20%), a knob.

## Calibration: yardsticks only, never Task D

The knobs are chosen to match the Ugaritic-Hebrew yardsticks. **No Task C or D score is computed
while choosing them**, so the sister is not tuned toward any recovery result.

- **Measurement code is shared.** The yardstick functions move from `scripts/v2/ugaritic_anchor.py`
  into `src/ibdb/yardsticks.py`. Ugaritic-Hebrew is recomputed with that module, and the values must
  equal the published ones before any sister is measured.
- **Direction:** the hidden half is mapped forward through the regular (elsewhere) correspondence
  and compared with the sister, the same direction as Ugaritic mapped to Hebrew.
- **Size matching:** samples of the Ugaritic sizes (5,876 units for JSD; 977 word tokens for overlap).
- **Development data:** seeds 90-91 only, with a grid over the knobs per language. The setting
  closest to the targets is fixed in `config/experiment.yaml` before anything else runs.

**Targets and tolerances (declared now):**

| Yardstick | Target | Accept |
|---|---|---|
| Bigram JSD above the same-size floor (bits) | 0.166 (0.184 - 0.018) | 0.126-0.206 |
| Cognate-form overlap, chance-corrected: (obs - chance) / (1 - chance) | 47% | 37-57% |
| Mergers | 24% of consonants | exact |
| Hidden texts of 6+ units found verbatim in the sister | <= 2% | <= 2% |
| Word-pair overlap (new yardstick, below) | Ugaritic-Hebrew value | +/- 10 points |

### Two settings (declared before any calibration run)

Ugaritic and Hebrew are close relatives, centuries apart. Any relative of the Harappan language that
might be attested would be far more distant. So two settings are calibrated, with the same
mechanisms and different targets:

| Setting | Role | JSD above floor | Shared word forms, chance-corrected | Mergers | Verbatim 6+ | Word-pair overlap |
|---|---|---|---|---|---|---|
| `close` ("close real relative") | **Primary** | 0.166 (accept 0.126-0.206) | 47% (37-57%) | 24% of consonants | <= 2% | U-H value +/- 10 points |
| `distant` | Sensitivity tier | 0.332, twice U-H (accept 0.272-0.392) | 24%, half of U-H (14-34%) | 24% of consonants | <= 2% | half the U-H value +/- 10 points |

**The `distant` targets are a guess, not a measurement.** No attested pair at that distance was
measured. "Twice the letter-pair distance, half the shared word forms" is a declared assumption for
a sensitivity tier. It is not a claim about how far any Indus relative would be. The merger share is
kept at 24% in both settings, because distance comes from the other mechanisms here and the anchor
gives no second value. For reference, the JSD ceiling from a shuffled mapping on the anchor is 0.475
bits, so the distant target is reachable in principle.

**New yardstick, computed on Ugaritic-Hebrew first.** Word-pair overlap is the share of adjacent
pairs of complete Ugaritic words whose gold-mapped forms occur as adjacent Hebrew words, corrected
for chance. It is the only yardstick that sees word order. It is computed and reported for
Ugaritic-Hebrew before any sister is built. If it is too sparse to be informative (few complete
pairs), it is reported but dropped as a target, and that is recorded here before calibration.

## Acceptance checks before the sister is used

The new sister is used for nothing until all of these pass and are reported:
1. **Shared code reproduces the anchor.** `yardsticks.py` gives the published Ugaritic-Hebrew
   values exactly.
2. **Mechanism tests** (`tests/test_sister_v4.py`):
   - the merger count is right;
   - conditioned rules give two reflexes for one phoneme;
   - affix replacement is consistent across words;
   - the share of clauses with word-order changes is as set;
   - the same seed gives the same sister.
3. **Yardsticks on held-out seeds.** With knobs frozen from seeds 90-91, every language and script
   type on seeds 0-2 falls inside every tolerance of its setting (`close` and `distant` separately). A language that cannot reach a target without
   breaking another (Tamil and Sanskrit start at JSD 0.005) is reported as not matched, not forced.
4. **Leakage.** v3-filter diagnostics: hidden-text word pairs left in the sister are at or below the
   v1 stricter-sister level (8%).
5. **Report before use.** A yardstick table (sister-v4 vs Ugaritic-Hebrew vs v1 sister) goes to you
   before any Task C or D run uses the sister.

## Scoring consequence (goes into `frozen-v2`, declared now)

With mergers and conditioned changes, the sister-to-hidden table is no longer one-to-one, so v1's
"before the cognate step" scorer, which inverts that table, breaks. Proposed v2 rule, matching the
Ugaritic scoring:
- each hidden unit's gold value is its regular (elsewhere) sister reflex;
- a sign counts as correct when the solver maps it to that reflex;
- many-to-one is accepted;
- conditioned reflexes count as wrong. This is conservative, and EM picks one value per sign anyway.

This replaces `token_acc_before_cognate` for sister-v4 runs only. It is the **strict** score
(primary). A **lenient** secondary score accepts any attested reflex of the hidden sound. Both are
declared in `docs/v2_preregistration.md`, entry 2.

## What it will be used for (later, after `frozen-v2`)

- Re-score Tasks C and D at the Indus point with sister-v4 in `related` and `candidates`, beside the
  v1 sister.
- Report the alphabetic `related` result beside Ugaritic's 33.9% as a check. This is not a target
  and does not count as validation if it happens to match.

## Effort

| Step | Effort |
|---|---|
| `yardsticks.py`, reproduce the anchor, word-pair yardstick | 0.5 day |
| Sister-v4 mechanisms and tests | 1.5 days |
| Calibration grid on seeds 90-91 | 0.5 day (compute about 1-2 h) |
| Held-out yardstick check and report | 0.5 day |
| **Total before any Task C/D use** | **about 3 days** |

## Risks

- **One anchor.** Ugaritic-Hebrew is one pair, one genre, about 6,000 letters. Its yardsticks carry
  sampling noise; the size-matched floor is reported with them.
- **No phonetics.** Mergers by grapheme similarity are not real sound change.
- **Targets can conflict.** High JSD and a 47% cognate overlap may not be reachable together for
  some languages; this is reported, not forced.
- **Gold table.** The Ugaritic targets inherit the secondary-source caveat (Kogan via Wikipedia;
  partly corroborated by Merlo, Mnamon).
- **Script levels.** The yardsticks are defined on phonemes, so syllabic and logographic sisters are
  checked on their phoneme layer only.
