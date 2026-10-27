"""Pre-registration entries 9-11: Finnish-Estonian Task C/D tables and readings E1-E4.

The entry-9 records (runs/results/v2_cd, v2_cd_repl, v2_controls: records_estonian.jsonl) were rescored by
entry 10; this reads the entry-10 records through pair_summary.py, which also computes the ceilings (raw,
raw before entry 10, reachable: primary from entry 11).
Usage (repository root): python reports/v2/cd/analysis/estonian_summary.py -> reports/v2/cd/estonian.{md,json}
"""
import json

import pair_summary as P

INTRO = ("Hidden Finnish (Indus-point corpora, 2,906 texts, mean length 4.6) against Kalevipoeg, normalised spelling. "
         "**Gold: weak (10 word pairs, 13 of 27 letters)**, from the word pairs printed in Pajusalu (2012); reported in its "
         "own rows and not pooled with the other pairs. Scored with the entry-10 rule: a no-source gold row is unknown, "
         "not lost (old values in `entry10.md`). The synthetic sisters (`harsh`, v1 sister) are optimistic upper "
         "references, not bounds (entry 10). Revised EM, strict, `related_real:estonian` unless stated; % of sign tokens. "
         "Seeds 0-2 primary; brackets are 95% bootstrap intervals over corpora (2,000 resamples), descriptive only. "
         "The readings E1-E4 of entry 9 are, in order: at the floor (E1), measurably helps (E2), minus `harsh` (E3), "
         "picks Estonian (E4).")
NOTES = ["**Frozen-code note (fixed by entry 11 for the final run).** These runs cut the Estonian reference with "
         "Finnish's vowel set, so Estonian õ and ü were cut as consonants in the syllabic and logo-syllabic references. "
         "The confirmation rerun on seeds 0-2 with the fixed cutter is in `entry11.md`."]


def main() -> None:
    res = P.summarise("finnish", ["estonian"])
    (P.A.CD / "estonian.json").write_text(json.dumps(res, indent=1, default=float))
    P.write_md(res, P.A.CD / "estonian.md", "Finnish-Estonian, Tasks C and D (pre-registration entries 9-11)", INTRO,
               {"estonian": "Estonian (sister; weak gold: 10 word pairs, 13 of 27 letters)"}, NOTES)


if __name__ == "__main__":
    main()
