"""Positive control, post hoc: Rao et al. (2009) relative conditional entropy with THEIR estimator.

Follows the Science supplement (homes.cs.washington.edu/~rao/ScienceIndus.pdf): modified Kneser-Ney
bigram probabilities, P(i) by frequency, C in nats, relative = C / ln N (ibdb.rao_kn). Token sets as in
the supplement where our data allow:
  English characters: all ASCII characters incl. case, digits, punctuation, space (Brown corpus, NLTK copy)
  English words: 417 most frequent Brown words (lower-cased, punctuation tokens removed)
  Sanskrit: Devanagari alpha-syllabic units (aksharas) of Rig Veda 1.1-1.100, incl. spaces (DCS, CC BY 4.0)
  Old Tamil: Tamil alpha-syllabic units of the eight Ettuthokai anthologies, incl. spaces (Project Madurai)
  Sumerian: 417 most frequent sign readings, no spaces (CDLI; Rao used ETCSL, which has no open licence)
  Type 1 / Type 2 controls: 10,000 lines x 20 signs over 417 signs; uniform successor / unique successor.
The frozen benchmark method is not touched. Usage:
  python scripts/positive_control_rao_kn.py   -> reports/positive_controls/rao2009_kn_ordering.{md,json}
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

from ibdb.data.prepare import _html_lines, load_segments
from ibdb.paths import ensure, raw_dir, reports_dir
from ibdb.rao_kn import conditional_entropy_kn

OUT = ensure(reports_dir() / "positive_controls")
RAO_FIG1B = {"Type 1 (no order)": 1.00, "Sanskrit": 0.66, "English words": 0.64, "Sumerian": 0.57,
             "Old Tamil": 0.56, "English chars": 0.51, "Type 2 (rigid)": 0.0}   # read by eye from Fig. 1B
RAO_N = {"Sanskrit": 388, "Old Tamil": 244, "English chars": 128, "English words": 417, "Sumerian": 417,
         "Type 1 (no order)": 417, "Type 2 (rigid)": 417}
ETTUTHOKAI = ["pmuni0296", "pmuni0110", "pmuni0028", "pmuni0038", "pmuni0087", "pmuni0221", "pmuni0229",
              "pmuni0057"]


# ------------------------------------------------------------------ corpora
def brown_sentences() -> list[list[str]]:
    sents = []
    for f in sorted((raw_dir() / "brown" / "brown").glob("c[a-r][0-9][0-9]")):
        for ln in f.read_text(encoding="ascii", errors="ignore").splitlines():
            toks = [t.rsplit("/", 1)[0] for t in ln.split() if "/" in t]
            if toks:
                sents.append(toks)
    return sents


_V = ["ai", "au", "ā", "ī", "ū", "ṝ", "ḹ", "a", "i", "u", "ṛ", "ḷ", "e", "o"]
_C = ["kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh", "k", "g", "ṅ", "c", "j", "ñ", "ṭ", "ḍ",
      "ṇ", "t", "d", "n", "p", "b", "m", "y", "r", "l", "v", "ś", "ṣ", "s", "h", "ḻ"]
_MARK = {"ṃ": "ṃ", "ṁ": "ṃ", "ḥ": "ḥ", "'": "'"}


def _phonemes(word: str):
    i = 0
    while i < len(word):
        for unit, kind in ([(c, "C") for c in _C if len(c) == 2] + [(v, "V") for v in _V if len(v) == 2] +
                           [(c, "C") for c in _C if len(c) == 1] + [(v, "V") for v in _V if len(v) == 1]):
            if word.startswith(unit, i):
                yield unit, kind
                i += len(unit)
                break
        else:
            if word[i] in _MARK:
                yield _MARK[word[i]], "M"
            i += 1


def aksharas_iast(line: str) -> list[str]:
    """IAST -> Devanagari-style alpha-syllabic units: C+V, C+virama, independent V, anusvara, visarga."""
    out: list[str] = []
    for w in unicodedata.normalize("NFC", line.lower()).split():
        ph = list(_phonemes(w))
        if not ph:
            continue
        if out:
            out.append(" ")
        k = 0
        while k < len(ph):
            u, kind = ph[k]
            if kind == "C" and k + 1 < len(ph) and ph[k + 1][1] == "V":
                out.append(u + ph[k + 1][0]); k += 2
            elif kind == "C":
                out.append(u + "्"); k += 1
            else:
                out.append(u); k += 1
    return out


def rigveda() -> list[list[str]]:
    d = raw_dir() / "sanskrit" / "repo" / "dcs" / "data" / "conllu" / "files" / "Ṛgveda"
    lines = []
    for f in sorted(d.glob("*.conllu")):
        m = re.search(r"ṚV, 1, (\d+)-", unicodedata.normalize("NFC", f.name))
        if not m or int(m.group(1)) > 100:
            continue
        for ln in f.read_text(encoding="utf-8").splitlines():
            if ln.startswith("# text ="):
                a = aksharas_iast(ln.split("=", 1)[1])
                if a:
                    lines.append(a)
    return lines


_TA = re.compile(r"[க-ஹ][ா-்ௗ]?|[அ-ஔ]|ஃ")


def ettuthokai() -> list[list[str]]:
    lines = []
    for name in ETTUTHOKAI:
        ls = _html_lines(raw_dir() / "tamil" / f"{name}.html")
        start = next((i for i, ln in enumerate(ls) if "freely distribute" in ln), 0) + 1
        for ln in ls[start:]:
            words = [w for w in (_TA.findall(unicodedata.normalize("NFC", w)) for w in ln.split()) if w]
            if not words:
                continue
            toks: list[str] = []
            for w in words:
                if toks:
                    toks.append(" ")
                toks.extend(w)
            lines.append(toks)
    return lines


def sumerian() -> list[list[str]]:
    d = load_segments("sumerian")
    forms = [w[0] for w in d["words"]]
    return [[s for wid in ids for s in forms[wid].split("-")] for kind, ids in d["clauses"] if kind == "line"]


def type_controls(V: int = 417, lines: int = 10_000, L: int = 20, seed: int = 0):
    rng = np.random.default_rng(seed)
    t1 = [list(map(int, rng.integers(0, V, size=L))) for _ in range(lines)]
    succ = rng.permutation(V)
    t2 = []
    for _ in range(lines):
        x = int(rng.integers(V)); ln = [x]
        for _ in range(L - 1):
            x = int(succ[x]); ln.append(x)
        t2.append(ln)
    return t1, t2


def corpora() -> dict[str, tuple[list, int | None]]:
    br = brown_sentences()
    words = [[w.lower() for w in s if re.fullmatch(r"[A-Za-z][A-Za-z'-]*", w)] for s in br]
    chars = [list(" ".join(s)) for s in br]
    t1, t2 = type_controls()
    return {"Type 1 (no order)": (t1, None), "Sanskrit": (rigveda(), None), "English words": (words, 417),
            "Sumerian": (sumerian(), 417), "Old Tamil": (ettuthokai(), None), "English chars": (chars, None),
            "Type 2 (rigid)": (t2, None)}


def main() -> None:
    res = {}
    for name, (texts, top) in corpora().items():
        types = len({x for t in texts for x in t})
        r = conditional_entropy_kn(texts, top)
        rm = conditional_entropy_kn(texts, top, oov="merge") if top else r
        res[name] = {"lines": len(texts), "tokens_total": sum(map(len, texts)), "types_total": types,
                     "N": r["N"], "rao_N": RAO_N[name], "C_nats": r["C"], "relative": r["relative"],
                     "relative_oov_merge": rm["relative"], "rao_fig1b": RAO_FIG1B[name]}
        print(name, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[name].items()}, flush=True)
    (OUT / "rao2009_kn_ordering.json").write_text(json.dumps(res, indent=1))
    ours = sorted(res, key=lambda k: -res[k]["relative"])
    rao = sorted(res, key=lambda k: -res[k]["rao_fig1b"])
    L = ["# Positive control (post hoc): Rao et al. (2009) estimator", "",
         "Modified Kneser-Ney bigrams, P(i) by frequency, relative = C / ln N (`ibdb.rao_kn`). Rao's values are "
         "read by eye from Fig. 1B. Corpora differ where licences forced it (Sumerian: CDLI, not ETCSL).", "",
         "| Corpus | Lines | Tokens | N used (Rao's N) | C, nats | Relative | Relative, OOV merged | Rao Fig. 1B |",
         "|---|---|---|---|---|---|---|---|"]
    for k in rao:
        d = res[k]
        L.append(f"| {k} | {d['lines']:,} | {d['tokens_total']:,} | {d['N']} ({d['rao_N']}) | {d['C_nats']:.2f} | "
                 f"{d['relative']:.2f} | {d['relative_oov_merge']:.2f} | {d['rao_fig1b']:.2f} |")
    L += ["", "**Rao ordering (high to low):** " + " > ".join(rao),
          "", "**Ours (high to low):** " + " > ".join(ours), ""]
    (OUT / "rao2009_kn_ordering.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
