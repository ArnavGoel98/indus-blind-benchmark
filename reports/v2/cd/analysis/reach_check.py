"""Exploratory (post hoc, 2026-10-21): how much of the strict ceiling can the frozen EM solver reach at all?

The entry-2 ceiling counts a token as recoverable when its regular reflex exists anywhere in the relative.
The frozen EM solver, however, only ever predicts one of the reference's 250 most frequent units
(`KnightEM.max_units`, units ranked as in `KnightEM._fit`). This measures, per corpus, the share of sign
tokens whose strict reflex is among those 250 units ("reachable"), beside the entry-2 ceiling. No solver
is run. Corpora: Latin and Old Tamil, four script types, seeds 0-5, samplers A and B (the entry-7/8 corpora).
Usage (repository root): python reports/v2/cd/analysis/reach_check.py -> reports/v2/cd/reach_check.md
"""
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
os.environ["IBDB_SISTER_VERSION"] = "v2"
import cd_v2  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.methods.decipher import KnightEM  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "reach_check.md"
CAP = KnightEM().max_units


def main():
    res = defaultdict(lambda: {"ceiling": [], "reachable": []})
    for lang in ("latin", "tamil"):
        rels = {r: RC.real_relative(lang, r) for r in cd_v2.REAL[lang]}
        for st in cd_v2.SCRIPTS:
            for smp in cd_v2.SAMPLERS:
                for seed in range(6):
                    knobs, spec = load_knobs("full", lang, st, cd_v2.SAMPLERS[smp])
                    _, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs,
                                            generator_version=cd_v2.SAMPLERS[smp])
                    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
                    vals = Counter(v for t in key.token_values for v in t)
                    n = sum(vals.values())
                    for name, rel in rels.items():
                        ref = RC.reference(rel, st, lang, spec.logogram_vocab)
                        top = {u for u, _ in Counter(u for t in ref.texts for u in t).most_common(CAP)}
                        g = RC.Gold(rel, lang, st, logos)
                        rec = sum(m for v, m in vals.items() if g._value(v)[0] is not None)
                        reach = sum(m for v, m in vals.items() if g._value(v)[0] in top)
                        res[(name, st)]["ceiling"].append(100 * rec / n)
                        res[(name, st)]["reachable"].append(100 * reach / n)
    L = ["# How much of the strict ceiling can the solver reach? (exploratory, post hoc)", "",
         f"Added 2026-10-21. The entry-2 ceiling counts a sign token as recoverable when its regular reflex occurs "
         f"anywhere in the relative. The frozen EM solver predicts only among the reference's {CAP} most frequent "
         "units, so a reflex outside them can never be predicted. *Reachable* is the share of tokens whose reflex is "
         "among those units. Mean over 12 corpora (seeds 0-5, samplers A and B); no solver is run.", "",
         "| Relative | Script | Ceiling (entry 2) | Reachable by the solver |", "|---|---|---|---|"]
    for (name, st), d in sorted(res.items(), key=lambda kv: (kv[0][0], cd_v2.SCRIPTS.index(kv[0][1]))):
        L.append(f"| {name.capitalize()} | {st} | {np.mean(d['ceiling']):.1f} | {np.mean(d['reachable']):.1f} |")
    L += ["", "**Reading.** Where *reachable* is far below the ceiling, the solver's unit cap, not only the relative, "
          "limits the score: the hidden language's frequent words have cognates in the relative, but those cognates "
          "are rare there. Example (checked 2026-10-21): Latin *et* is 19.3% of the sign tokens of the seed-0, "
          "sampler-A logographic corpus, and its reflex *et* occurs in Dante, so it counts as recoverable; but it "
          "occurs only 4 times there (rank 2,592), while Italian *e* is rank 1. The logographic ceilings in entry 2 "
          "therefore overstate what this solver could reach."]
    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
