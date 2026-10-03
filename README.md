# IBDB: Indus Blind Decipherment Benchmark

**Question.** Suppose a corpus has the statistics of the Indus inscriptions: a few thousand
texts, about 4-5 signs each, 400-700 sign types, strong positional effects. Could any existing
decipherment method recover the language underneath? If not, how much more data would it need?

**What IBDB does.** It writes *known* languages (Sanskrit, Old Tamil, Sumerian, Latin, Finnish)
and *non-linguistic* sign systems in invented scripts. It calibrates those scripts to published
Indus statistics and hides the answer key. Then it measures which methods recover what, at
which corpus size.

**What IBDB does not do.** It does not decipher the Indus script, and it makes no claim
about the Indus language. A method that scores well here has shown it can read Indus-*like*
synthetic data. That is a necessary condition for a credible decipherment, not evidence of one.

![Decipherability curve](reports/figures/decipherability_headline.png)

## Results at a glance

Read [`reports/results/results.md`](reports/results/results.md) for all numbers with
confidence intervals, and [`reports/calibration_report.md`](reports/calibration_report.md)
for how closely the synthetic corpora match the Indus targets. The draft paper is
[`reports/methods_report.md`](reports/methods_report.md).

## Method in one paragraph

Plaintext comes from openly licensed corpora ([config/sources.yaml](config/sources.yaml)).
Each source is cut into short, seal-like segments: names, epithets, titles, formulae, and
19,076 real Sumerian seal inscriptions. A generator writes them in one of four script types
(logographic, syllabic, logo-syllabic, alphabetic). It can add allographs, homophony,
polyvalence, determinatives, word dividers and a reading direction. Text selection and
writing-system knobs are calibrated until the corpus matches every Indus target in
[config/indus_targets.yaml](config/indus_targets.yaml), each of which carries a citation and
a verified/unverified flag. Eight method families run on every corpus: Rao-style entropy,
Yadav-style n-grams, positional histograms, segmentation, script-type estimation,
language/non-language classifiers, Knight-style EM, and a Luo-style matcher. Four tasks are
scored separately:

| Task | Question | Chance |
|---|---|---|
| A | Is it language at all? | 0.50 balanced accuracy |
| B | Which script type? | 0.25 |
| C | Which language family? | ~0.25 (depends on candidates) |
| D | What does each sign stand for? (token accuracy vs key) | ≈ frequency-rank baseline |

## Design safeguards (and why they exist)

An adversarial review (Believer / Skeptic / Investor / Judge) ruled **"fix first"**. The
Skeptic's fatal flaw: *if the generator's choices determine the curve, the Indus point is a
coordinate in a space we defined.* The fixes are built in:

1. **No single Indus verdict.** Results are reported across a band of corpus sizes, and as a
   *feasibility region*: the share of random writing-system scenarios in which a method
   succeeds at Indus scale.
2. **Three calibration regimes**: `full`, `holdout` (positional and frequency targets left
   free), and `wrong_prior` (deliberately wrong targets). Rank changes across regimes are
   reported, so circularity is measured rather than hidden.
3. **Structurally independent non-linguistic controls**: heraldic bearings (one sign per
   visual element), administrative slot tags, Markov emblems, Rao's type 1 and type 2, and an
   **adversarial** control tuned to match language entropy. Kamon *descriptions* are text and
   are reported separately as a contaminated control.
4. **Knowledge tiers for decipherment**: `related` (a close synthetic sister language, the
   Ugaritic/Hebrew situation, not available for Indus), `candidates`, and `none`. Only the
   last two are Indus-relevant.
5. **"Nothing works" is a first-class output**: the smallest corpus at which each method
   beats chance is tabulated.
6. **The leaderboard cannot be gamed by matching public texts.** Challenge corpora are built
   from secretly disguised sister languages. Keys are committed by SHA-256 before submissions,
   and each team gets one scored submission per hidden round.

## Choices that could make results meaningless (read before citing)

- **Oracle script type in Task D.** Decipherment methods are told the script type and the
  unit level. Real Indus decipherers are not, so Task D numbers are an *upper bound*.
- **Sister-language distance** (sound-change 0.30, lexical replacement 0.20) directly sets
  `related`-tier results. It is a free parameter, so those results are not a measurement of
  Indus.
- **Inventory calibration erases the inventory signal.** Every corpus is forced to 400-700
  signs, so script type cannot be read off inventory size by construction. That is true of
  Indus too, but it makes the inventory rule's score uninformative about the rule itself.
- **Segment selection is tuned.** Positional and frequency targets are hit by preferring
  certain windows of real text, not by modelling what seals actually said. The `holdout`
  regime shows the effect.
- **Unverified targets.** 5,500 texts, mean 4.4 and median 4 come from the project brief.
  Verified neighbours: 2,906 texts / 13,372 signs in Mahadevan (1977), i.e. 4.60 signs per text.
- **Luo-style matcher is not neural.** It keeps the matching and assignment structure of
  Luo, Cao & Barzilay (2019) but uses a table instead of an LSTM. Treat it as a lower bound.
- **Small-sample entropy bias.** With about 400 signs and about 20k bigrams, plug-in
  conditional entropy is biased low (an i.i.d. 420-sign source measures about 0.59 of its
  true ratio). Entropy thresholds learned at one corpus size do not transfer to another.

## Install and reproduce

```bash
python3.11 -m pip install -e ".[dev]"
ibdb reproduce --profile full     # fetch -> prepare -> calibrate -> run -> report  (hours on 4 cores)
ibdb reproduce --profile quick    # smaller sweep for a smoke run
pytest                            # unit tests (no downloads needed)
```

Individual steps: `ibdb fetch`, `ibdb prepare`, `ibdb calibrate`, `ibdb run`, `ibdb report`.
Every random draw descends from `master_seed` in `config/experiment.yaml`.
`ibdb fetch` refuses any single download over 500 MB unless given `--allow-large`. The largest
source is 122 MB.

## How to submit to the blind challenge

1. Get a round: `challenge/public/<round>/` (keys included, for development) or
   `challenge/hidden/<round>/` (keys held by the maintainer; SHA-256 commitments in
   `commitments.json`).
2. Each `corpora/*.json.gz` holds sign-ID sequences in physical order plus the reading direction.
3. Produce one JSON file:

```json
{"team": "...", "method": "...", "url": "...", "claims_indus_decipherment": false,
 "predictions": {"<corpus_id>": {"is_linguistic": true, "script_type": "syllabic",
                                 "family": "dravidian", "sign_values": {"123456": "ka"}}}}
```

4. Score public rounds yourself: `ibdb-score sub.json --round r1 --tier public`. For hidden
   rounds, send the file to the maintainer, who runs `ibdb-score sub.json --round r1 --tier hidden --record`
   and rebuilds the static page with `ibdb leaderboard`.

**Maintainer: create hidden rounds only on a machine you control.** Run
`ibdb challenge build --round h1 --tier hidden` locally, then commit `challenge/hidden/h1/`
(corpora, manifest, commitments). Never commit `private/`: it holds the round secret and the keys.
A hidden round generated anywhere else, such as a shared or cloud session, should be treated as
compromised.

Sign values are compared as transliterated unit strings. The unit conventions are in
`ibdb/phonology.py`: IAST for Sanskrit, ISO-15919-style for Tamil, CDLI readings for Sumerian.

## Repository layout

```
config/            calibration targets (with citations), sources (with licenses), experiment profiles
src/ibdb/          package: data/ (fetch, prepare), generator/ (script, sampler, calibrate, build),
                   controls.py, methods/ (8 families), knowledge.py, evaluate.py, figures.py,
                   reports.py, challenge.py, leaderboard.py, cli.py
tests/             unit tests for generator, metrics, scoring, learners, methods
reports/           calibration report, results tables, figures, methods report
challenge/         public and hidden rounds (hidden keys are NOT here)
leaderboard/       static page (index.html) + data.json
private/           answer keys and challenge secrets; git-ignored, never published
data/              downloaded and derived text; git-ignored (licenses vary)
```

## Licenses

Code: MIT ([LICENSE](LICENSE)). Data keeps its own license and is never committed; see
[DATA_LICENSES.md](DATA_LICENSES.md).
