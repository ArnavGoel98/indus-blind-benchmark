"""Rank 6b (pre-registration entry 5): Ugaritic-Hebrew yardsticks on real related-language pairs.

No tuning, no targets. For each available pair: point estimates (20 draws) as written and
normalised (primary); a bootstrap over the relative's texts (200 replicates, 5 draws each; interval,
SD and bootstrap mean are reported, because plug-in statistics are biased upward under resampling);
the number of mergers in the gold table. Rows for comparison: Ugaritic-Hebrew (as written; vowel
letters removed), the v1-like sister and the `harsh` bound for the same hidden language (same code).

Available now: Latin-Italian (descendant). Finnish-Estonian waits for its gold source; the Dravidian
pairs wait for the provenance check; Sanskrit-Pali waits for a licence.

Usage: python scripts/v2/real_relatives_yardsticks.py -> reports/v2/real_relatives/yardsticks.{json,md}
"""
from __future__ import annotations

import json

import numpy as np

from ibdb import sister_v4 as S
from ibdb import yardsticks as Y
from ibdb.data import relatives as R
from ibdb.paths import ensure, reports_dir

OUT = ensure(reports_dir() / "v2" / "real_relatives")
SIS = reports_dir() / "v2" / "sister"
KEYS = ["jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc", "verbatim_6plus"]
N_BOOT, BOOT_DRAWS = 200, 5


def pair_latin_italian(anchor: dict) -> dict:
    hidden = S.hidden_half("latin")[0]
    regular, attested = R.latin_italian_map()
    out = {"pair": "latin-italian", "relationship": R.RELATIONSHIP[("latin", "italian")],
           "mergers": len([k for k, v in regular.items() if v is not None]) - len({v for v in regular.values() if v}),
           "deleted": sorted(k for k, v in regular.items() if v is None)}
    for spelling in ("as_written", "normalised"):
        rel = R.dante_texts(spelling)
        out[spelling] = {"n_texts": len(rel), "n_words": sum(map(len, rel)),
                         "n_units": sum(len(w) for t in rel for w in t),
                         "point": Y.sister_yardsticks(hidden, rel, regular, anchor, n_draws=20, seed=0)}
        if spelling == "normalised":
            rng = np.random.default_rng(2026)
            boot = {k: [] for k in KEYS}
            for b in range(N_BOOT):
                smp = [rel[i] for i in rng.integers(len(rel), size=len(rel))]
                y = Y.sister_yardsticks(hidden, smp, regular, anchor, n_draws=BOOT_DRAWS, seed=b + 1)
                for k in KEYS:
                    boot[k].append(y[k])
                if (b + 1) % 50 == 0:
                    print(f"[latin-italian] bootstrap {b + 1}/{N_BOOT}", flush=True)
            out[spelling]["bootstrap"] = {k: {"lo": float(np.quantile(v, 0.025)), "hi": float(np.quantile(v, 0.975)),
                                              "mean": float(np.mean(v)), "sd": float(np.std(v))} for k, v in boot.items()}
    return out


def comparison_rows(lang: str) -> dict:
    cal = json.loads((SIS / "calibration.json").read_text())
    harsh = json.loads((SIS / "harsh.json").read_text())
    mean = lambda rs: {k: float(np.mean([r[k] for r in rs])) for k in KEYS}  # noqa: E731
    return {"v1_like": mean(cal["confirm"]["v1_like"][lang]["held"]), "harsh": mean(harsh["confirm"][lang]["held"])}


def main() -> None:
    anchor = json.loads((SIS / "anchor.json").read_text())
    corr = json.loads((SIS / "anchor_corrected.json").read_text())["main"]
    res = {"anchor_as_written": {k: anchor[k] for k in ("jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc")}
           | {"verbatim_6plus": anchor["verbatim_natural_6plus"]},
           "anchor_vowel_letters_removed": {k: corr[k] for k in ("jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc")}
           | {"verbatim_6plus": corr["verbatim_natural_6plus"]},
           "pairs": {"latin-italian": pair_latin_italian(anchor)},
           "bracket": {"latin": comparison_rows("latin")},
           "not_yet": {"finnish-estonian (sister)": "gold source (Pajusalu 2012) not reachable from this environment",
                       "tamil-malayalam (descendant), tamil-kannada (sister)": "awaiting Wikisource provenance check",
                       "sanskrit-pali (descendant)": "licence unresolved; public-domain fallback being searched"}}
    (OUT / "yardsticks.json").write_text(json.dumps(res, indent=1, default=float))
    write_md(res)


def write_md(res: dict) -> None:
    f = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
    li = res["pairs"]["latin-italian"]
    L = ["# Rank 6b: Ugaritic-Hebrew yardsticks on real related languages (pre-registration entry 5)", "",
         "No tuning, no targets. Shared code (`src/ibdb/yardsticks.py`); sample sizes matched to the anchor. "
         "Normalised spelling is primary. Every pair is labelled sister or descendant.", "",
         "| Pair | Relationship | Spelling | JSD above floor (bits) | Shared word forms, chance-corr. | Word pairs, chance-corr. | Verbatim 6+ units | Mergers |",
         "|---|---|---|---|---|---|---|---|",
         f"| Ugaritic-Hebrew | sister | as written | " + " | ".join(f(k, res["anchor_as_written"][k]) for k in KEYS) + " | 7 |",
         f"| Ugaritic-Hebrew | sister | vowel letters removed | " + " | ".join(f(k, res["anchor_vowel_letters_removed"][k]) for k in KEYS) + " | 7 |"]
    for sp in ("as_written", "normalised"):
        L.append(f"| **Latin-Italian** | {li['relationship']} | {sp.replace('_', ' ')}{' (primary)' if sp == 'normalised' else ''} | "
                 + " | ".join(f(k, li[sp]["point"][k]) for k in KEYS) + f" | {li['mergers']} (+ h deleted) |")
    b = res["bracket"]["latin"]
    L += [f"| Latin, v1-like sister (upper bound) | synthetic | - | " + " | ".join(f(k, b["v1_like"][k]) for k in KEYS) + " | 0 |",
          f"| Latin, `harsh` (lower bound) | synthetic | - | " + " | ".join(f(k, b["harsh"][k]) for k in KEYS) + " | 5 |", "",
          "**Latin-Italian, bootstrap over Dante lines (normalised; 200 replicates, 5 draws each):**", "",
          "| Yardstick | Point (20 draws) | Bootstrap mean | 95% interval | SD |", "|---|---|---|---|---|"]
    for k in KEYS:
        bt = li["normalised"]["bootstrap"][k]
        L.append(f"| {k} | {f(k, li['normalised']['point'][k])} | {f(k, bt['mean'])} | {f(k, bt['lo'])}-{f(k, bt['hi'])} | {f(k, bt['sd'])} |")
    n = li["normalised"]
    L += ["", f"Sizes: Dante {n['n_texts']:,} lines, {n['n_words']:,} words, {n['n_units']:,} units; hidden side = v1 Latin hidden half.",
          f"Gold: Grandgent (1907), section per row in `src/ibdb/data/relatives.py`. Mergers: {li['mergers']}; deleted: {', '.join(li['deleted'])}.", "",
          "**Not measured yet:**", ""] + [f"- {k}: {v}" for k, v in res["not_yet"].items()] + [""]
    (OUT / "yardsticks.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
