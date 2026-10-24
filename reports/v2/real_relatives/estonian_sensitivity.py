"""Exploratory, post hoc (2026-10-24): why are the Finnish-Estonian word-level yardsticks negative?

Hypothesis: the entry-5 yardstick code deletes letters whose regular reflex is None, and the entry-9 gold
has 14 such rows ("no source", 12.6% of hidden letters), so mapped Finnish words are mangled. This
recomputes the point yardsticks (20 draws, as entry 5) with those rows filled from general knowledge
(p, v, j, oe, ae kept; y -> u-umlaut). NOT a result and not a gold table: the entry-9 table is unchanged.
Usage (repository root): python reports/v2/real_relatives/estonian_sensitivity.py -> estonian_sensitivity.md
"""
import json
import os
from pathlib import Path

os.environ.setdefault("IBDB_SISTER_VERSION", "v2")
from ibdb import sister_v4 as S  # noqa: E402
from ibdb import yardsticks as Y  # noqa: E402
from ibdb.data import relatives as R  # noqa: E402

OUT = Path(__file__).resolve().parent
SIS = OUT.parent / "sister"
FILL = {"p": "p", "v": "v", "j": "j", "ö": "ö", "ä": "ä", "y": "ü"}

anchor = json.loads((SIS / "anchor.json").read_text())
hidden = S.hidden_half("finnish")[0]
rel = R.kalevipoeg_texts("normalised")
gold = R.finnish_estonian_map()[0]
filled = {**gold, **FILL}
f = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
keys = ["jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc", "verbatim_6plus"]
L = ["# Finnish-Estonian yardsticks: sensitivity to the no-source rows (exploratory, post hoc)", "",
     "Added 2026-10-24, after `estonian.md` showed negative chance-corrected word-level yardsticks. The yardstick "
     "code deletes letters whose reflex is None. Here the no-source rows p, v, j, ö, ä, y are filled from general "
     "knowledge (kept; y as ü). **Not a result and not a gold table**; the entry-9 gold and every Task C/D score are "
     "unchanged. Point estimates, 20 draws, normalised spelling.", "",
     "| Gold | " + " | ".join(keys) + " |", "|---|" + "---|" * len(keys)]
for name, reg in (("entry 9 (no-source rows deleted)", gold), ("no-source rows filled (exploratory)", filled)):
    y = Y.sister_yardsticks(hidden, rel, reg, anchor, n_draws=20, seed=0)
    L.append(f"| {name} | " + " | ".join(f(k, y[k]) for k in keys) + " |")
L += ["", "If the filled row is positive and the entry-9 row negative, the negative word-level yardsticks come "
      "from the deletion of no-source letters, not from the language pair."]
(OUT / "estonian_sensitivity.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
