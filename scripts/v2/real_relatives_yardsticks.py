"""Rank 6b (pre-registration entry 5): Ugaritic-Hebrew yardsticks on real related-language pairs.

No tuning, no targets. For each available pair: point estimates (20 draws) as written and
normalised (primary); a bootstrap over the relative's texts (200 replicates, 5 draws each; interval,
SD and bootstrap mean are reported, because plug-in statistics are biased upward under resampling);
the number of mergers in the gold table. Rows for comparison: Ugaritic-Hebrew (as written; vowel
letters removed), the v1-like sister and the `harsh` bound for the same hidden language (same code).

Available now: Latin-Italian (descendant), Tamil-Malayalam (descendant), Tamil-Kannada (sister).
Finnish-Estonian waits for its gold source (Pajusalu PDF from the project owner); Sanskrit-Pali waits
on SuttaCentral.

Usage: python scripts/v2/real_relatives_yardsticks.py -> reports/v2/real_relatives/yardsticks.{json,md}
"""
from __future__ import annotations

import json

import numpy as np

from ibdb import sister_v4 as S
from ibdb import yardsticks as Y
from ibdb.data import dravidian as D
from ibdb.data import relatives as R
from ibdb.paths import ensure, reports_dir

OUT = ensure(reports_dir() / "v2" / "real_relatives")
SIS = reports_dir() / "v2" / "sister"
KEYS = ["jsd_above_floor", "cognate_types_cc", "word_pairs_types_cc", "verbatim_6plus"]
N_BOOT, BOOT_DRAWS = 200, 5


def measure_pair(name: str, hidden_lang: str, relationship: str, rel_texts, regular: dict, anchor: dict) -> dict:
    hidden = S.hidden_half(hidden_lang)[0]
    out = {"pair": name, "hidden": hidden_lang, "relationship": relationship,
           "mergers": len([k for k, v in regular.items() if v is not None]) - len({v for v in regular.values() if v}),
           "deleted": sorted(k for k, v in regular.items() if v is None)}
    for spelling in ("as_written", "normalised"):
        rel = rel_texts(spelling)
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
                    print(f"[{name}] bootstrap {b + 1}/{N_BOOT}", flush=True)
            out[spelling]["bootstrap"] = {k: {"lo": float(np.quantile(v, 0.025)), "hi": float(np.quantile(v, 0.975)),
                                              "mean": float(np.mean(v)), "sd": float(np.std(v))} for k, v in boot.items()}
    return out


def pair_latin_italian(anchor: dict) -> dict:
    return measure_pair("latin-italian", "latin", R.RELATIONSHIP[("latin", "italian")], R.dante_texts,
                        R.latin_italian_map()[0], anchor)


def pair_tamil(lang: str, anchor: dict) -> dict:
    return measure_pair(f"tamil-{lang}", "tamil", D.RELATIONSHIP[lang], lambda sp: D.texts(lang, sp),
                        D.gold_map(lang)[0], anchor)


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
           "pairs": {"latin-italian": pair_latin_italian(anchor), "tamil-malayalam": pair_tamil("malayalam", anchor),
                     "tamil-kannada": pair_tamil("kannada", anchor)},
           "bracket": {"latin": comparison_rows("latin"), "tamil": comparison_rows("tamil")},
           "not_yet": {"finnish-estonian (sister)": "waiting for the Pajusalu (2012) PDF from the project owner",
                       "sanskrit-pali (descendant)": "waiting on SuttaCentral; no OCR re-transcription",
                       "sumerian": "isolate; none tier only"}}
    (OUT / "yardsticks.json").write_text(json.dumps(res, indent=1, default=float))
    write_md(res)


SCRIPT = {"Ugaritic-Hebrew": "consonant-only (abjad)", "latin-italian": "alphabet (vowels written)",
          "tamil-malayalam": "abugida (vowels written)", "tamil-kannada": "abugida (vowels written)"}


def write_md(res: dict) -> None:
    f = lambda k, v: f"{v:.3f}" if k == "jsd_above_floor" else f"{100 * v:.1f}%"  # noqa: E731
    L = ["# Rank 6b: Ugaritic-Hebrew yardsticks on real related languages (pre-registration entry 5)", "",
         "No tuning, no targets. Shared code (`src/ibdb/yardsticks.py`); sample sizes matched to the anchor. "
         "Normalised spelling is primary. Every pair is labelled sister or descendant.", "",
         "**Cross-script comparisons are indicative only.** Shared word forms (and word pairs) are not directly "
         "comparable between a consonant-only script (Ugaritic-Hebrew) and scripts that write vowels (all other "
         "rows): a consonant skeleton matches far more easily than a full word, even after the chance correction. "
         "Comparisons within one script type are the meaningful ones.", "",
         "| Pair | Relationship | Script type | Spelling | JSD above floor (bits) | Shared word forms, cc | Word pairs, cc | Verbatim 6+ | Mergers |",
         "|---|---|---|---|---|---|---|---|---|",
         "| Ugaritic-Hebrew | sister | " + SCRIPT["Ugaritic-Hebrew"] + " | as written | " + " | ".join(f(k, res["anchor_as_written"][k]) for k in KEYS) + " | 7 |",
         "| Ugaritic-Hebrew | sister | " + SCRIPT["Ugaritic-Hebrew"] + " | vowel letters removed | " + " | ".join(f(k, res["anchor_vowel_letters_removed"][k]) for k in KEYS) + " | 7 |"]
    for name, pr in res["pairs"].items():
        for sp in ("as_written", "normalised"):
            L.append(f"| **{name}** | {pr['relationship']} | {SCRIPT[name]} | {sp.replace('_', ' ')}{' (primary)' if sp == 'normalised' else ''} | "
                     + " | ".join(f(k, pr[sp]["point"][k]) for k in KEYS)
                     + f" | {pr['mergers']}{' + ' + ', '.join(pr['deleted']) + ' no reflex' if pr['deleted'] else ''} |")
    for lang, b in res["bracket"].items():
        L += [f"| {lang}, v1-like sister (upper bound) | synthetic | as hidden | - | " + " | ".join(f(k, b["v1_like"][k]) for k in KEYS) + " | 0 |",
              f"| {lang}, `harsh` (lower bound) | synthetic | as hidden | - | " + " | ".join(f(k, b["harsh"][k]) for k in KEYS) + " | 24% of consonants |"]
    L += ["", "**Bootstrap over the relative's lines (normalised; 200 replicates, 5 draws each): point / bootstrap mean / 95% interval**", "",
          "| Pair | " + " | ".join(KEYS) + " |", "|---|" + "---|" * len(KEYS)]
    for name, pr in res["pairs"].items():
        bt = pr["normalised"]["bootstrap"]
        L.append(f"| {name} | " + " | ".join(f"{f(k, pr['normalised']['point'][k])} / {f(k, bt[k]['mean'])} / {f(k, bt[k]['lo'])}-{f(k, bt[k]['hi'])}"
                                            for k in KEYS) + " |")
    L += ["", "**Sizes (normalised):** " + "; ".join(f"{n}: {p['normalised']['n_texts']:,} lines, {p['normalised']['n_words']:,} words, "
                                                   f"{p['normalised']['n_units']:,} units" for n, p in res["pairs"].items()) + ".",
          "**Gold sources:** Latin-Italian, Grandgent (1907), section per row (`src/ibdb/data/relatives.py`); Tamil-Malayalam and "
          "Tamil-Kannada, Caldwell (1875), pages per row (`src/ibdb/data/dravidian.py`). Hidden side: the v1 hidden half of each source.",
          "**Data notes:** Malayalam (Adhyatma Ramayanam Kilippattu, 126 section pages) and Kannada (Kumaravyasa Bharata) "
          "Wikisource texts: source edition unstated (accepted as clean by the project owner, 2026-10-15). Kannada coverage "
          "is partial: 93 of the 154 sandhi pages linked from the ten parva pages exist (61 red links), mostly Adi, Virata "
          "and Karna parvas; the 2 commentary (ಸಟೀಕಾ) pages are excluded. Each Kannada sandhi page opens with a short "
          "invocation that may be in Sanskrit; it was not removed. Revision ids and SHA-256 per page are in "
          "`data/raw/relatives/{ml,kn}/manifest.json`.", "",
          "**Not measured:**", ""] + [f"- {k}: {v}" for k, v in res["not_yet"].items()] + [""]
    (OUT / "yardsticks.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
