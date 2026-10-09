"""Summarise reports/v2/ugaritic/records.json -> reports/v2/ugaritic/results.md (v2; not in the paper)."""
from __future__ import annotations

import json

import numpy as np

from ibdb.paths import reports_dir

D = reports_dir() / "v2" / "ugaritic"
r = json.loads((D / "records.json").read_text())
C = r["corpora"]
METHODS = [("baseline_frequency_rank", "Frequency rank"), ("knight2006_em_original", "EM, original rule (primary)"),
           ("knight2006_em", "EM, revised rule")]
TIERS = ["related", "related_poetic", "candidates", "none"]
pc = lambda x: f"{100 * x:.1f}"  # noqa: E731

nat = C["natural"]["D"]["related"]["knight2006_em_original"]["token_acc"]
L = [f"**Pre-registered success criterion: FAILED ({pc(nat)}% < 50% of tokens; frozen EM original rule, `related` "
     "tier, natural texts).** It also fails in every other condition and tier.", "",
     "# v2 rank 2: Ugaritic-Hebrew real-relative anchor — results", "",
     "Plan pre-registered in `docs/v2_ugaritic_plan.md` (pushed b05772d; amendment committed before the run).",
     "Methods frozen-v1, unchanged. Not in the v1 paper.", "",
     "## Sources", "",
     f"- EUPT, version {r['sources']['eupt_version']}, accessed {r['sources']['eupt_accessed']}, CC BY-SA 4.0:"]
L += [f"  - {u} (SHA-256 {h[:16]}…)" for u, h in r["sources"]["eupt_pages"].items()]
L += [f"- OSHB (WLC 4.20), commit {r['sources']['oshb_commit']}, CC BY 4.0 (WLC public domain). "
      "Original work of the Open Scriptures Hebrew Bible available at https://github.com/openscriptures/morphhb",
      f"- Gold: {r['sources']['gold']}.", "",
      "**Gold table status: SECONDARY SOURCE, not yet verified against an academic source we have read.** The "
      "table is Wikipedia's; its cited source, Kogan (2011), has not been read. Search for an openly accessible "
      "academic source (2026-10-09):",
      "- Partly corroborated by P. Merlo, \"Ugaritic\", *Mnamon: Ancient writing systems in the Mediterranean*, "
      "Scuola Normale Superiore (DOI 10.25429/sns.it/lettere/mnamon000), read 2026-10-09: ṯ and š merged into "
      "Hebrew š, ʿ and ġ into ʿ, and ẓ is written ṣ in Hebrew in the word for \"summer\" (one example). It does not "
      "cover ḫ/ḥ, ḏ/z or the three aleph signs.",
      "- Segert (1984), *A Basic Grammar of the Ugaritic Language* (UC Press): no openly licensed copy found "
      "(publisher and JSTOR access restricted; an Internet Archive scan of unclear legal status was not used).",
      "- Gianto, \"Ugaritic\" (ResearchGate full text): not accessible (HTTP 403).",
      "Until a read source covers ḫ/ḥ, ḏ/z and the alephs, all Task D numbers carry this caveat.", "",
      "## Corpora", "",
      "| Condition | Texts | Tokens | Letters | Mean length | Duplicate rate | One-to-one ceiling (letters) |",
      "|---|---|---|---|---|---|---|"]
for n, c in C.items():
    L.append(f"| {n} | {c['n_texts']} | {c['n_tokens']} | {c['n_letters']} | {c['mean_length']:.2f} | {c['dup_rate']:.3f} | "
             f"{pc(c['ceilings']['one_to_one'])}% |")
L += ["", "References: " + "; ".join(f"{k} {v['units']:,} units ({v['unit_types']} types)" for k, v in r["reference_sizes"].items()) + "."]

L += ["", "## Task D: sign values", "",
      "Token accuracy, %, v1 convention (every token; word dividers count and are unrecoverable) / letters only /"
      " letters without ỉ and ủ. Letter types right out of 29. Pre-registered success: token accuracy >= 50%.", ""]
for tier in TIERS:
    L += [f"### `{tier}`", "", "| Condition | " + " | ".join(m[1] for m in METHODS) + " |", "|---|" + "---|" * len(METHODS)]
    for n, c in C.items():
        cells = []
        for m, _ in METHODS:
            v = c["D"][tier][m]
            cells.append(f"{pc(v['token_acc'])} / {pc(v['letters'])} / {pc(v['letters_sourced'])}; "
                         f"{len(v['types_right'])}/29; ref {v['reference']}")
        L.append(f"| {n} | " + " | ".join(cells) + " |")
    L.append("")
rc = [C[n]["D"]["related"]["knight2006_em_original"]["token_acc"] for n in C if n.startswith("recut")]
L += [f"Re-cut seeds, EM original, `related`: {', '.join(pc(x) for x in rc)} (mean {pc(np.mean(rc))}).", ""]
if "D_em_seeds" in C["natural"]:
    L += ["EM restart seed (natural, `related`; primary uses seed 0): " +
          "; ".join(f"{k} {pc(v['token_acc'])}" for k, v in C["natural"]["D_em_seeds"].items()) + ".", ""]
L += ["Letters right, natural, `related`, EM original: " +
      " ".join(C["natural"]["D"]["related"]["knight2006_em_original"]["types_right"]) + ".", ""]

L += ["## Task C: language family (`candidates`: Hebrew + 5 v1 languages; chance 1/6)", "",
      "| Condition | " + " | ".join(m[1] for m in METHODS) + " |", "|---|" + "---|" * len(METHODS)]
for n, c in C.items():
    L.append(f"| {n} | " + " | ".join(c["D"]["candidates"][m]["reference"] for m, _ in METHODS) + " |")

L += ["", "## Tasks A and B (frozen rules, fit on v1 run records as for Sproat's corpora)", "",
      "Task A is a check only (pre-registered as weak evidence). Real Ugaritic is called \"not language\" by 3-4 of "
      "the 5 frozen rules in every condition. **Training-distribution caveat:** the rules were fit on synthetic "
      "corpora with 400+ signs calibrated to Indus statistics; a 30-sign alphabet lies far outside that range, so "
      "this shows the rules do not transfer to small alphabets, not that the methods judge Ugaritic non-linguistic "
      "in any wider sense.", ""]
for pool, v in r["AB_pools"].items():
    a_names = list(next(iter(v.values()))["A"])
    L += [f"### `{pool}`", "", "| Condition | " + " | ".join(a_names) + " | Entropy ratio | Task B (inventory / LR / branching) |",
          "|---|" + "---|" * (len(a_names) + 2)]
    for n, x in v.items():
        L.append(f"| {n} | " + " | ".join("language" if x["A"][m] else "not" for m in a_names) +
                 f" | {x['entropy_ratio']:.3f} | " + " / ".join(x["B"].values()) + " |")
    L.append("")

y = r["yardsticks"]
L += ["## Distance yardsticks: real relative vs synthetic sister", "",
      "| Measure | Ugaritic-Hebrew | Chance / floor | v1 sister (Sanskrit / Tamil / Sumerian / Latin / Finnish) |", "|---|---|---|---|"]
vs = y["v1_sister"]
langs = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
f = lambda k, p=True: " / ".join((pc(vs[l][k]) if p else f"{vs[l][k]:.3f}") for l in langs)  # noqa: E731
L += [f"| Sound mergers | {y['mergers']} | - | 0 (bijective) |",
      f"| Texts found verbatim in the reference, natural texts, % | {pc(y['verbatim_natural'])} | {pc(y['verbatim_natural_chance'])} (shuffled map) | see note |",
      f"| ... texts of 6+ letters, % | {pc(y['verbatim_natural_6plus'])} | {pc(y['verbatim_natural_6plus_chance'])} | |",
      f"| ... re-cut to 4.6, % | {pc(y['verbatim_recut4.6'])} | {pc(y['verbatim_recut4.6_chance'])} | |",
      f"| Cognate-form overlap, word types, % ({y['n_word_types']} types, {y['n_word_tokens']} tokens) | {pc(y['cognate_types'])} | "
      f"{pc(y['cognate_types_chance'])} (95th pct {pc(y['cognate_types_chance_p95'])}) | {f('cognate_types')} (chance {f('cognate_types_chance')}) |",
      f"| ... word tokens, % | {pc(y['cognate_tokens'])} | {pc(y['cognate_tokens_chance'])} | {f('cognate_tokens')} (chance {f('cognate_tokens_chance')}) |",
      f"| Letter-bigram JSD, bits | {y['bigram_jsd']:.3f} (poetic ref {y['bigram_jsd_poetic']:.3f}) | "
      f"{y['bigram_jsd_hebrew_sample_floor']:.3f} (same-size Hebrew sample vs Hebrew); shuffled map {y['bigram_jsd_shuffled_mean']:.3f} | "
      f"{f('bigram_jsd_size_matched', False)} (size-matched) |", "",
      "v1 sister cognate overlap is measured on samples of the same number of word tokens as the Ugaritic text "
      "(20 draws), hidden half vs sister half, alphabetic units.", ""]
L += ["## Exploratory comparison (NOT pre-registered)", "",
      "Added after the results were seen. The v1 alphabetic corpora at the Indus point, `related` tier, frozen EM "
      "original rule, before the cognate step, score 38.9% (sampler A, 15 corpora) and 57.8% (sampler B); they have "
      "about 320-340 signs (allographs, homophones) and twice the tokens, but a synthetic sister reference. "
      "Ugaritic (30 signs, real relative, half the tokens) scores 33.9%. One reading: a real relative costs "
      "roughly what v1's inventory and duplication cost. This is not a controlled comparison (sign inventory, "
      "size, script and reference all differ) and is not a test of any pre-registered hypothesis.", ""]
(D / "results.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
