"""Pre-registration entry 3: test contiguous-block splits before the corrected grid (dev seeds 90-91).

For each split: share of the source's clauses and word types each half keeps, and the yardsticks of
the v1-like sister (shift + 20% lexical, no mergers) and one fixed mid-grid setting, measured against
the corrected anchor's sample sizes. Selection rule (entry 3): the largest block size for which each
half keeps >= 40% of clauses and >= 40% of word types.

Usage: python scripts/v2/sister_block_test.py -> reports/v2/sister/block_test.{json,md}
"""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

import numpy as np

LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
SPLITS = ["content", "block250", "block1000", "block4000", "halves"]
SETTINGS = {"v1_like": ({"n_cond": 0, "affix_share": 0.0, "lexical": 0.2, "word_order": 0.0, "final_vowel_loss": 0.0}, 0.0),
            "mid": ({"n_cond": 4, "affix_share": 0.5, "lexical": 0.35, "word_order": 0.5, "final_vowel_loss": 0.3}, None)}
KEYS = ["jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc", "verbatim_6plus"]


def job(lang: str, split: str) -> dict:
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    from ibdb import sister_v4 as S
    from ibdb import yardsticks as Y
    from ibdb.generator.build import _segments
    from ibdb.paths import reports_dir
    A = json.loads((reports_dir() / "v2" / "sister" / "anchor_corrected.json").read_text())["main"]
    d = _segments(lang)
    n_cl = len(d["clauses"])
    types = {w for _, ids in d["clauses"] for w in ids}
    out = {"lang": lang, "split": split}
    for half in ("hidden", "reference"):
        h = S._split(lang, d, half, split)
        out[f"{half}_clause_share"] = len(h) / n_cl
        out[f"{half}_type_share"] = len({w for _, ids in h for w in ids}) / len(types)
    if min(out["hidden_clause_share"], out["reference_clause_share"]) < 0.05:
        out["note"] = "a half is (nearly) empty: too few blocks"
        return out
    hid = S.hidden_half(lang, split)[0]
    for name, (k, ms) in SETTINGS.items():
        rs = []
        for seed in (90, 91):
            kw = {} if ms is None else {"merger_share": ms}
            s = S.build(lang, seed, S.Knobs(**k), split=split, **kw)
            rs.append(Y.sister_yardsticks(hid, s.clauses, s.regular, A, n_draws=10, seed=seed))
        out[name] = {y: float(np.mean([r[y] for r in rs])) for y in KEYS}
    return out


def choose(res: list[dict]) -> dict:
    out = {}
    for lang in LANGS:
        ok = [r["split"] for r in res if r["lang"] == lang and r["split"].startswith("block")
              and min(r["hidden_clause_share"], r["reference_clause_share"]) >= 0.4
              and min(r["hidden_type_share"], r["reference_type_share"]) >= 0.4]
        out[lang] = max(ok, key=lambda s: int(s.removeprefix("block"))) if ok else "content"
    return out


def main() -> None:
    from ibdb.paths import reports_dir
    OUT = reports_dir() / "v2" / "sister"
    with ProcessPoolExecutor(4, mp_context=get_context("fork")) as ex:
        res = list(ex.map(job, *zip(*[(l, s) for l in LANGS for s in SPLITS])))
    (OUT / "block_test.json").write_text(json.dumps(res, indent=1))
    pc = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
    L = ["# Block-split test (pre-registration entry 3; dev seeds 90-91)", "",
         "Halves: share of the source's clauses / word types kept by the hidden and the sister half.",
         "Yardsticks: JSD above floor / shared word forms (cc) / word pairs (cc) / verbatim 6+.", "",
         "| Language | Split | Hidden half | Sister half | v1-like sister | Mid setting |", "|---|---|---|---|---|---|"]
    for r in res:
        cell = lambda n: " / ".join(pc(k, r[n][k]) for k in KEYS) if n in r else r["note"]  # noqa: E731
        L.append(f"| {r['lang']} | {r['split']} | {100 * r['hidden_clause_share']:.0f}% / {100 * r['hidden_type_share']:.0f}% | "
                 f"{100 * r['reference_clause_share']:.0f}% / {100 * r['reference_type_share']:.0f}% | {cell('v1_like')} | {cell('mid')} |")
    chosen = choose(res)
    L += ["", "## Split chosen (entry 3 rule: largest block size, 250 / 1,000 / 4,000, whose halves each keep >= 40% of "
          "clauses and of word types)", "", "| Language | Split |", "|---|---|"]
    L += [f"| {l} | {s} |" for l, s in chosen.items()]
    L += ["", "**Limitation (recorded as entry 3 requires).** Blocks do not remove shared formulaic text: for the "
          "v1-like sister, verbatim overlap stays far above the 2% constraint under every split (it falls only in "
          "Sanskrit and rises slightly in Sumerian). A real relative's texts differ in content as well as in language; "
          "a sister cut from the same source cannot reproduce that, so the verbatim constraint can only be met by changing "
          "word forms heavily.", ""]
    (OUT / "block_split.json").write_text(json.dumps(chosen, indent=1))
    L.append("")
    (OUT / "block_test.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
