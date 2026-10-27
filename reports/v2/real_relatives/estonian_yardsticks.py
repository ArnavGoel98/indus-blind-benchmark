"""Pre-registration entry 9: Finnish-Estonian yardsticks and verbatim overlap (entry-5 code, unchanged).

Runs the hand-checked normalisation examples first, then `measure_pair` of
scripts/v2/real_relatives_yardsticks.py and `inspect` of scripts/v2/real_relatives_verbatim.py on
Finnish (v1 hidden half) against Kalevipoeg. The unrelated-language level for the verbatim check uses
the Latin hidden half, in letters. Lives under reports/ so the frozen-code check keeps guarding the code.
Usage (repository root): python reports/v2/real_relatives/estonian_yardsticks.py [--verbatim-only]
  --verbatim-only keeps the yardsticks in estonian.json and recomputes the verbatim inspection only.
Writes reports/v2/real_relatives/estonian.{json,md}.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
os.environ.setdefault("IBDB_SISTER_VERSION", "v2")
import real_relatives_verbatim as V  # noqa: E402
import real_relatives_yardsticks as Y  # noqa: E402
from ibdb import sister_v4 as S  # noqa: E402
from ibdb.data import relatives as R  # noqa: E402
from ibdb.data.gold import NO_SOURCE  # noqa: E402

OUT = Path(__file__).resolve().parent
KEYS = Y.KEYS


def main() -> None:
    R.check_estonian()
    anchor = json.loads((Y.SIS / "anchor.json").read_text())
    regular = R.finnish_estonian_map()[0]
    if "--verbatim-only" in sys.argv:
        res = json.loads((OUT / "estonian.json").read_text())
    else:
        res = {"pair": Y.measure_pair("finnish-estonian", "finnish", R.RELATIONSHIP[("finnish", "estonian")],
                                      R.kalevipoeg_texts, regular, anchor),
               "synthetic": Y.comparison_rows("finnish")}
    lengths = json.loads((Y.SIS / "anchor.json").read_text())["verbatim_6plus_lengths"]
    tx = R.kalevipoeg_texts("normalised")
    rel = V.Relative(tx, R.kalevipoeg_texts("as_written"), V._aligned(R.kalevipoeg_lines(), tx, R.estonian_words))
    res["verbatim"] = V.inspect("finnish", rel, regular, lengths)
    latin = [[tuple("".join(w)) for w in c] for c in S.hidden_half("latin")[0]]
    res["verbatim"]["unrelated_latin_share"] = V.unrelated_share(latin, rel, lengths)
    res["rows"] = {"sourced": sum(v[0] not in (None, NO_SOURCE) for v in R.FINNISH_ESTONIAN.values()),
                   "total": len(R.FINNISH_ESTONIAN)}
    (OUT / "estonian.json").write_text(json.dumps(res, indent=1, default=float, ensure_ascii=False))
    write_md(res, anchor)


def write_md(res: dict, anchor: dict) -> None:
    f = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
    pr, vb = res["pair"], res["verbatim"]
    hidden_letters = [p for c in S.hidden_half("finnish")[0] for w in c for p in w]
    nosrc = sum(R.FINNISH_ESTONIAN.get(p, (p,))[0] == NO_SOURCE for p in hidden_letters) / len(hidden_letters)
    L = ["# Finnish-Estonian yardsticks (pre-registration entries 9 and 10)", "",
         "Same code and settings as `yardsticks.md` (entry 5). Normalised spelling is primary. **Gold: weak (10 word pairs, "
         f"13 of 27 letters)**, built from the Finnish-North Estonian word pairs printed in Pajusalu (2012); {res['rows']['sourced']} of "
         f"{res['rows']['total']} rows have a regular reflex, the rest are \"no source\" ({100 * nosrc:.1f}% of the hidden Finnish "
         "letters), treated as unknown, not lost (entry 10). "
         "Both sides are written in alphabets that write vowels, so the comparison with Latin-Italian is within one "
         "script type; the comparison with Ugaritic-Hebrew is indicative only.", "",
         "| Pair | Relationship | Spelling | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Mergers |",
         "|---|---|---|---|---|---|---|---|",
         "| Ugaritic-Hebrew (as written) | sister | - | " + " | ".join(f(k, v) for k, v in (
             ("jsd_above_floor", anchor["jsd_above_floor"]), ("cognate_types_cc", anchor["cognate_types_cc"]),
             ("word_pairs_types_cc", anchor["word_pairs_types_cc"]), ("verbatim_6plus", anchor["verbatim_natural_6plus"]))) + " | 7 |"]
    for sp in ("as_written", "normalised"):
        L.append(f"| **finnish-estonian** (weak gold: 10 word pairs, 13 of 27 letters) | {pr['relationship']} | {sp.replace('_', ' ')}{' (primary)' if sp == 'normalised' else ''} | "
                 + " | ".join(f(k, pr[sp]["point"][k]) for k in KEYS) + f" | {pr['mergers']} |")
    b = res["synthetic"]
    L += [f"| finnish, v1-like sister (synthetic, optimistic upper reference) | synthetic | - | " + " | ".join(f(k, b["v1_like"][k]) for k in KEYS) + " | 0 |",
          f"| finnish, `harsh` (synthetic, optimistic upper reference) | synthetic | - | " + " | ".join(f(k, b["harsh"][k]) for k in KEYS) + " | 24% of consonants |",
          "", "**Bootstrap over Kalevipoeg's lines (normalised; 200 replicates, 5 draws each): point / bootstrap mean / 95% interval**", "",
          "| " + " | ".join(KEYS) + " |", "|" + "---|" * len(KEYS)]
    bt = pr["normalised"]["bootstrap"]
    L.append("| " + " | ".join(f"{f(k, pr['normalised']['point'][k])} / {f(k, bt[k]['mean'])} / {f(k, bt[k]['lo'])}-{f(k, bt[k]['hi'])}"
                               for k in KEYS) + " |")
    hb = vb["hits_by_class"]
    L += ["", f"**Size (normalised):** {pr['normalised']['n_texts']:,} lines, {pr['normalised']['n_words']:,} words, "
              f"{pr['normalised']['n_units']:,} units. No-source rows: {', '.join(pr.get('no_source', []))}.", "",
          "## Verbatim overlap (entry-5 procedure)", "",
          f"Windows of 6+ hidden Finnish letters mapped through the gold that occur verbatim in Kalevipoeg: "
          f"**{100 * vb['share']:.1f}%** of {vb['n_windows_drawn']:,} windows (shuffled-map chance: mean "
          f"{100 * vb['chance_share_mean']:.1f}%, 95th percentile {100 * vb['chance_share_p95']:.1f}%; an unrelated language, "
          f"Latin, in letters: {100 * vb['unrelated_latin_share']:.1f}%). By class: "
          + ", ".join(f"{k} {v}" for k, v in hb.items()) + f"; spanning 2+ whole words: {vb['hits_whole_multiword']}.", "",
          "Kreutzwald modelled Kalevipoeg on the Kalevala, so shared formulas are possible. The hits spanning several "
          "whole words, most often hit first:", ""]
    multi = sorted((r for r in vb["hits"] if r["whole_words_multi"]), key=lambda r: -r["times_hit"])[:15]
    L += [f"- `{' '.join(r['hidden_words'])}` -> {' '.join(r['relative_words_as_written'])} ({r['times_hit']}x; "
          f"{r['n_relative_lines']} Kalevipoeg lines)" for r in multi] or ["- none"]
    (OUT / "estonian.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
