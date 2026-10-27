# PROPOSAL (not approved): v2 freeze date and final-run plan

Written 2026-10-27 after entry 10. **Nothing here is declared or run until the project owner approves.**
On approval, the plan becomes pre-registration entry 11 and is committed before the freeze tag.

## 1. Why a new freeze is needed

`frozen-v2` (tag on commit `4ce3e90`, 2026-10-18) froze the methods and the v2 harness for entries 6-9.
Entry 10 changed the v2 scoring and yardstick harness (no-source rows unknown, not lost) and the report
labels. The entry-10 reruns ran under a narrower guard (`reports/v2/cd/analysis/entry10.py`: everything
equal to `frozen-v2` except the named harness files). A final v2 result should come from one frozen state
that includes entry 10.

**Proposal: keep `frozen-v2` where it is and tag the new state `frozen-v2.1`.** `frozen-v2` is already
on GitHub and documents the code behind entries 6-9; moving it would rewrite published history and break
that provenance. `frozen-v2.1` is a new tag, so nothing already published changes. (If you would rather
have one tag, the alternative is to delete and re-push `frozen-v2`; I recommend against it.)

## 2. Proposed dates

| Date | Step |
|---|---|
| 2026-10-27 to 10-29 | You review the entry-10 results (`reports/v2/cd/entry10.md`) and decide the three open questions in section 3. |
| **2026-10-30 (Fri)** | **Freeze:** entry 11 (this plan, as approved) committed; `cd_v2.check_frozen` pointed at the new tag; `frozen-v2.1` tagged and pushed (you push the tag, as before: tag pushes are blocked in this session). |
| 2026-10-31 to 11-01 | Final run (about 10-14 hours of compute; resumable). |
| 2026-11-02 (Mon) | Results reported to you before anything goes into the draft. |

## 3. Decisions needed before the freeze (each changes code, so it must come before the tag)

1. **Logographic ceiling.** The entry-2 ceiling ignores the solver's 250-unit cap (limitation 13). Option
   A (recommended): add the reachable-unit ceiling as a reported column, with no score change. Option B:
   leave as is. Changing the solver cap itself would change v1 method code, so it is not offered.
2. **Syllable cutter for Estonian.** The frozen cutter uses the hidden language's vowel set, so Estonian õ
   and ü are cut as consonants in the Estonian syllabic reference. Option A (recommended): cut each
   relative with the union of the hidden language's vowels and the relative's own vowel letters (changes
   the solver's input for Estonian syllabic and logo-syllabic only; Italian, Malayalam and Kannada have no
   extra vowels, to be checked). Option B: keep, and report as a limitation.
3. **Pali.** If SuttaCentral grants permission before the freeze, Sanskrit-Pali joins the final run with
   a gold table from Geiger (1916) added as data, as Estonian was. If not, the final run goes without it;
   data can be added later only as a labelled addition, not as part of the final run.

## 4. Final-run plan (draft of entry 11)

**Design: a confirmatory run on fresh seeds.** Every v2 reading so far was formed on seeds 0-5, and
several analysis choices were made after seeing them (the reframing, the controls, entry 10). The final
run therefore uses **seeds 6-11**, which no v2 code has generated, with every reading fixed in entry 11
before any corpus is made. Seeds 0-5 become the development set and stay reported as such.

- **Corpora:** Indus-point corpora (2,906 texts, mean length 4.6), samplers A and B, four script types,
  five hidden languages, seeds 6-11: 240 corpora.
- **Tiers:** the realistic `related` tier with every real relative (Italian; Malayalam, Kannada; Estonian,
  weak gold; Pali if added) and `candidates_real`; the synthetic optimistic references (v1 sister, rerun at
  these seeds with the frozen v1 code, and `harsh`); `none` for Sumerian.
- **Methods and budget:** unchanged (revised EM primary, original EM, frequency rank; 3 restarts, 60
  iterations).
- **Controls:** C1 (unrelated references), C2 (floor), C3 (10 restarts, all real-relative cells, seeds
  6-8), C4 (determinism: a second run of 24 corpora compared value by value).
- **Yardsticks and verbatim checks:** recomputed once on the frozen code (they do not depend on seeds).
- **Records:** scores and predictions stored and archived with SHA-256, so any later scoring question
  needs no rerun.

**Readings to fix in entry 11 (proposed):**
- F1. Each real-relative cell mean (seeds 6-11) below 50%.
- F2. For each real relative, alphabetic: measurably helps over an unrelated reference by the entry-8
  rule (at least 5 points and ahead in 9 of 12 corpora).
- F3. For each real relative and script type: below the `harsh` reference or not (descriptive; the
  framing does not depend on it).
- F4. Old Tamil alphabetic with each relative within 10 points of the Ugaritic anchor.
- F5. Task C: the relative chosen in fewer than half of the `candidates_real` corpora.
- F6. Agreement with the development seeds: for each reading above, whether seeds 6-11 give the same
  answer as seeds 0-5; disagreements reported, not resolved.

**What would count against the current picture:** a real-relative cell at or above 50%; the
alphabetic "helps" pattern disappearing for Estonian or Kannada; or real relatives scoring above `harsh`.

## 5. Not part of this plan

No Zenodo deposit; no change to v1 or to `paper-v1`; nothing enters the paper without your approval.
