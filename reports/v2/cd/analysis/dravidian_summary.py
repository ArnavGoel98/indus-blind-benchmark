"""Old Tamil-Malayalam and Old Tamil-Kannada Task C/D tables and readings, in the format of estonian.md.

Reads the entry-10 records through pair_summary.py (seeds 0-5, both samplers; C1 with Latin and Finnish as
the unrelated references, C2 floors). The readings are those fixed in entries 7 and 8 for these pairs.
Usage (repository root): python reports/v2/cd/analysis/dravidian_summary.py -> reports/v2/cd/dravidian.{md,json}
"""
import json

import pair_summary as P

INTRO = ("Hidden Old Tamil (Indus-point corpora, 2,906 texts, mean length 4.6) against the Malayalam and Kannada texts, "
         "normalised spelling. Gold: Caldwell (1875), with Old Tamil h, s, ṣ and ḵ \"no source\" for both relatives, "
         "scored with the entry-10 rule (a no-source gold row is unknown, not lost; old values in `entry10.md`). "
         "Malayalam is a descendant, Kannada a sister. The synthetic sisters (`harsh`, v1 sister) are optimistic upper "
         "references, not bounds (entry 10). Revised EM, strict, `related_real:<relative>` unless stated; % of sign "
         "tokens. Seeds 0-2 primary (entry 6), seeds 3-5 the replication (entry 7); brackets are 95% bootstrap "
         "intervals over corpora (2,000 resamples), descriptive only. The same numbers, in other layouts, are in "
         "`results.md`, `pooled.md` and `controls.md`.")
NOTES = ["**Frozen-code note (fixed by entry 11 for the final run).** These runs cut the Malayalam and Kannada "
         "references with Old Tamil's vowel set, so vocalic ṛ (0.24% of each text's units, in Sanskrit loans) was cut "
         "as a consonant in the syllabic and logo-syllabic references. The confirmation rerun on seeds 0-2 with the "
         "fixed cutter is in `entry11.md`."]


def budget_note() -> str:
    """C3 (entry 8): revised EM with 10 restarts against 3, seeds 0-2, from controls.json (entry-10 values)."""
    rows = [r for r in json.loads((P.A.CD / "controls.json").read_text())["C3"] if r["lang"] == "tamil" and r["tier"] != "harsh"]
    first = [f"{r['tier'].capitalize()} {r['script']} ({P.pct(r['r3'])} with 3 restarts, {P.pct(r['r10'])} with 10)"
             for r in rows if r["first_order"]]
    return ("**Solver budget (C3, entry 8; seeds 0-2).** More restarts change a cell by more than 10 points (first-order) "
            f"in {len(first)} of {len(rows)} real-relative cells: " + ("; ".join(first) if first else "none") +
            ". The primary results stay at 3 restarts (`controls.md`). Not run for Estonian.")


def main() -> None:
    res = P.summarise("tamil", ["malayalam", "kannada"])
    (P.A.CD / "dravidian.json").write_text(json.dumps(res, indent=1, default=float))
    P.write_md(res, P.A.CD / "dravidian.md", "Old Tamil-Malayalam and Old Tamil-Kannada, Tasks C and D (entries 6-8, 10, 11)",
               INTRO, {"malayalam": "Malayalam (descendant)", "kannada": "Kannada (sister)"}, [budget_note(), ""] + NOTES)


if __name__ == "__main__":
    main()
