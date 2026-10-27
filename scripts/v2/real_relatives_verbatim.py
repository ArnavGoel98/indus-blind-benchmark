"""Rank 6b follow-up: inspect the verbatim 6+ unit windows that the real-relative yardstick counts.

Exploratory inspection (not a pre-registered measurement). The yardstick (`yardsticks.sister_yardsticks`)
draws windows of the anchor's 6+ letter text lengths from random hidden texts, mapped forward through
the gold regular reflexes, and counts a window as verbatim when it occurs anywhere in the relative's
text (word boundaries ignored on both sides, as for the anchor). Here, for normalised spelling:

- the same windows are drawn in 20 passes, and every distinct hit is listed with the hidden words it
  spans and the relative's line(s) containing it;
- each hit is classed automatically:
  - `word`: the window is one whole hidden word and one whole relative word;
  - `within words`: it lies inside one hidden word and inside one relative word;
  - `across boundaries`: it spans a word boundary on either side;
  - `normalised only` (flag): the matched stretch of the relative is written with a voiced or
    aspirated stop, so it matches only after normalisation. In Malayalam such letters mostly mark
    Sanskrit loans; Kannada also writes voicing in native words, so there the flag is weaker;
- chance: the same draws through shuffled gold maps (20 maps, keys permuted, as for the anchor).
  Shuffling breaks the hidden language's phonotactics, so this understates coincidence;
- an unrelated-language baseline: the same draws from the v1 Finnish hidden half, letters kept as
  they are (j -> y and doubled vowels -> long vowels for the Dravidian relatives; j -> i for Italian,
  as Italian is read), against the same relative text. Finnish shares the open CV syllable shape,
  so this is the coincidence level for an unrelated language of similar phonotactics.

Usage: python scripts/v2/real_relatives_verbatim.py -> reports/v2/real_relatives/verbatim.{json,md}
"""
from __future__ import annotations

import json
import re
from collections import Counter

import numpy as np

from ibdb import sister_v4 as S
from ibdb.data import dravidian as D
from ibdb.data import relatives as R
from ibdb.data.gold import NO_SOURCE
from ibdb.paths import ensure, reports_dir

OUT = ensure(reports_dir() / "v2" / "real_relatives")
SIS = reports_dir() / "v2" / "sister"
N_PASS, N_SHUF = 20, 20
SEP = "\x1f"
VOICED_ASPIRATED = set(D.NORMALISE)


def _forward(hidden, regular):
    """Hidden texts mapped forward, with the hidden word index of every unit (texts of 6+ units).
    A no-source unit (entry 10) breaks the text: each stretch between such units is a text of its own."""
    out = []
    for c in hidden:
        units, word_of = [], []
        for wi, w in enumerate(c):
            for p in w:
                q = regular.get(p, p)
                if q == NO_SOURCE:
                    if len(units) >= 6:
                        out.append((units, word_of, c))
                    units, word_of = [], []
                elif q is not None:
                    units.append(q)
                    word_of.append(wi)
        if len(units) >= 6:
            out.append((units, word_of, c))
    return out


def _draws(fwd, lengths, seed):
    rng = np.random.default_rng(seed)
    for _ in range(N_PASS):
        for L in lengths:
            k = int(rng.integers(len(fwd)))
            if len(fwd[k][0]) < L:
                continue
            yield k, int(rng.integers(len(fwd[k][0]) - L + 1)), L


class Relative:
    def __init__(self, texts, written, raw):
        self.texts, self.written, self.raw = texts, written, raw
        self.lines = [SEP.join(p for w in t for p in w) + SEP for t in texts]
        self.blob = "|".join(self.lines)
        self.words = {SEP.join(w) + SEP for t in texts for w in t}

    def locate(self, key: str) -> dict:
        """Lines holding `key`; for the first, the relative word(s) it spans."""
        idx = [j for j, u in enumerate(self.lines) if key in u]
        j = idx[0]
        n_before = self.lines[j][:self.lines[j].index(key)].count(SEP)
        n = key.count(SEP)
        pos, spans = 0, []
        for wi, w in enumerate(self.texts[j]):
            if pos + len(w) > n_before and pos < n_before + n:
                spans.append(wi)
            pos += len(w)
        whole = len(spans) == 1 and sum(len(w) for w in self.texts[j][:spans[0]]) == n_before \
            and len(self.texts[j][spans[0]]) == n
        flat = [p for w in self.written[j] for p in w]
        return {"lines": idx, "spans": spans, "whole_word": whole,
                "written": [self.written[j][k] for k in spans], "span_written": flat[n_before:n_before + n]}


def inspect(hidden_lang: str, rel: Relative, regular: dict, lengths: list[int], flag: set | None = None) -> dict:
    fwd = _forward(S.hidden_half(hidden_lang)[0], regular)
    hits, info, n = Counter(), {}, 0
    for k, i, L in _draws(fwd, lengths, 0):
        n += 1
        units, word_of, c = fwd[k]
        key = SEP.join(units[i:i + L]) + SEP
        if key not in rel.blob:
            continue
        hits[key] += 1
        if key in info:
            continue
        span = sorted(set(word_of[i:i + L]))
        whole_hidden = len(span) == 1 and len([p for p in c[span[0]] if regular.get(p, p) not in (None, NO_SOURCE)]) == L
        starts = i == 0 or word_of[i - 1] != word_of[i]
        ends = i + L == len(units) or word_of[i + L] != word_of[i + L - 1]
        loc = rel.locate(key)
        if len(span) == 1 and len(loc["spans"]) == 1:
            cls = "word" if whole_hidden and loc["whole_word"] else "within words"
        else:
            cls = "across boundaries"
        j = loc["lines"][0]
        info[key] = {"window": " ".join(units[i:i + L]), "length": L, "class": cls,
                     "whole_words_multi": len(span) >= 2 and starts and ends,
                     "normalised_only": bool(flag) and any(p in flag for p in loc["span_written"]),
                     "hidden_words": ["".join(c[s]) for s in span],
                     "relative_words_as_written": ["".join(w) for w in loc["written"]],
                     "n_relative_lines": len(loc["lines"]),
                     "relative_line": " ".join("".join(w) for w in rel.texts[j]),
                     "relative_line_as_printed": rel.raw[j] if rel.raw else None}
    rows = sorted(info.values(), key=lambda r: (r["class"], -r["n_relative_lines"], r["window"]))
    for r in rows:
        r["times_hit"] = hits[SEP.join(r["window"].split()) + SEP]
    by = lambda f: {c: sum(r["times_hit"] for r in rows if f(r) == c) for c in sorted({f(r) for r in rows})}  # noqa: E731
    # Chance: the same draw positions through shuffled maps.
    rng = np.random.default_rng(1)
    keys = sorted(q for q in regular if regular[q] != NO_SOURCE)      # entry 10: permute known rows only
    chance = []
    for _ in range(N_SHUF):
        m = regular | dict(zip(keys, rng.permutation([regular[q] for q in keys])))
        fs = _forward(S.hidden_half(hidden_lang)[0], m)
        h = t = 0
        for k, i, L in _draws(fs, lengths, 0):
            t += 1
            h += (SEP.join(fs[k][0][i:i + L]) + SEP) in rel.blob
            if t >= len(lengths):       # one pass per shuffled map
                break
        chance.append(h / t)
    return {"n_windows_drawn": n, "n_hits": sum(hits.values()), "share": sum(hits.values()) / n,
            "chance_share_mean": float(np.mean(chance)), "chance_share_p95": float(np.quantile(chance, 0.95)),
            "n_distinct_hits": len(rows), "hits_by_class": by(lambda r: r["class"]),
            "hits_normalised_only": None if flag is None else sum(r["times_hit"] for r in rows if r["normalised_only"]),
            "hits_whole_multiword": sum(r["times_hit"] for r in rows if r["whole_words_multi"]),
            "hits_in_10plus_relative_lines": sum(r["times_hit"] for r in rows if r["n_relative_lines"] >= 10),
            "hits": rows}


def finnish_unrelated(target: str) -> list:
    out = []
    for c in S.hidden_half("finnish")[0]:
        cl = []
        for w in c:
            w = [("y" if target == "dravidian" else "i") if p == "j" else p for p in w]
            if target == "dravidian":
                v = []
                for p in w:
                    if v and p in "aeiou" and v[-1] == p:
                        v[-1] = {"a": "ā", "e": "ē", "i": "ī", "o": "ō", "u": "ū"}[p]
                    else:
                        v.append(p)
                w = v
            cl.append(tuple(w))
        out.append(cl)
    return out


def unrelated_share(clauses, rel: Relative, lengths: list[int]) -> float:
    fwd = _forward(clauses, {})
    draws = list(_draws(fwd, lengths, 0))
    return sum((SEP.join(fwd[k][0][i:i + L]) + SEP) in rel.blob for k, i, L in draws) / len(draws)


def _aligned(raw: list[str], texts: list, words) -> list[str]:
    out = [line for line in raw if words(line)]
    return out if len(out) == len(texts) else []


def main() -> None:
    lengths = json.loads((SIS / "anchor.json").read_text())["verbatim_6plus_lengths"]
    res = {}
    for lang in ("malayalam", "kannada"):
        tx = D.texts(lang, "normalised")
        raw = _aligned(D.lines(lang), tx, lambda s: [w for w in re.split(r"[\s\-–—,.;:!?\"'‘’“”()\[\]]+", s)
                                                    if D.script_phonemes(w, lang)])
        rel = Relative(tx, D.texts(lang, "as_written"), raw)
        res[f"tamil-{lang}"] = inspect("tamil", rel, D.gold_map(lang)[0], lengths, VOICED_ASPIRATED)
        res[f"tamil-{lang}"]["unrelated_finnish_share"] = unrelated_share(finnish_unrelated("dravidian"), rel, lengths)
    tx = R.dante_texts("normalised")
    rel = Relative(tx, R.dante_texts("as_written"), _aligned(R.dante_lines(), tx, R.italian_words))
    res["latin-italian"] = inspect("latin", rel, R.latin_italian_map()[0], lengths)
    res["latin-italian"]["unrelated_finnish_share"] = unrelated_share(finnish_unrelated("italian"), rel, lengths)
    (OUT / "verbatim.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    write_md(res)


def write_md(res: dict) -> None:
    pc = lambda x: f"{100 * x:.1f}%"  # noqa: E731
    L = ["# Rank 6b: what the verbatim 6+ matches are (exploratory)", "",
         "Not pre-registered; an inspection of the yardstick in `yardsticks.md`. Normalised spelling. The anchor's "
         "6+ letter window lengths are drawn 20 times over (so the share differs slightly from the yardstick's "
         "single pass). Word boundaries are ignored on both sides, as in the yardstick and the anchor. Chance: the "
         "same draws through 20 shuffled gold maps (one pass each); it breaks the hidden language's phonotactics and so "
         "understates coincidence. *Unrelated (Finnish)*: the same draws from the v1 Finnish hidden half (letters as "
         "they are; j -> y and doubled vowels -> long for the Dravidian relatives, j -> i for Italian) against the same "
         "relative text: the coincidence level for an unrelated language with a similar open syllable shape.", "",
         "| Pair | Windows | Hits | Share | Chance (mean / 95th pct.) | Unrelated (Finnish) | One whole word | Inside words | Across word boundaries | Normalised only | In 10+ relative lines |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in res.items():
        hb = v["hits_by_class"]
        L.append(f"| {k} | {v['n_windows_drawn']:,} | {v['n_hits']} | {pc(v['share'])} | {pc(v['chance_share_mean'])} / "
                 f"{pc(v['chance_share_p95'])} | {pc(v['unrelated_finnish_share'])} | {hb.get('word', 0)} | {hb.get('within words', 0)} | "
                 f"{hb.get('across boundaries', 0)} | {'n/a' if v['hits_normalised_only'] is None else v['hits_normalised_only']} | {v['hits_in_10plus_relative_lines']} |")
    L += [""]
    for k, v in res.items():
        hb = v["hits_by_class"]
        L.append(f"- **{k}:** {pc(v['share'])} of windows, {v['share'] / v['unrelated_finnish_share']:.1f} times the "
                 f"unrelated-language level ({pc(v['unrelated_finnish_share'])}). {pc(hb.get('across boundaries', 0) / v['n_hits'])} "
                 f"of hits run across a word boundary. Hits that are one whole word on both sides: {hb.get('word', 0)}; "
                 f"that cover two or more whole hidden words: {v['hits_whole_multiword']}.")
    L += ["", "Classes count hits (a window drawn twice counts twice). *Normalised only*: the matched stretch of the "
          "relative is written with a voiced or aspirated stop, so it matches only after normalisation. In Malayalam "
          "such letters mostly mark Sanskrit loans; Kannada also writes voicing in native words. The flag is not "
          "defined for Latin-Italian (n/a).", ""]
    for k, v in res.items():
        L += [f"## {k}: every distinct hit", "",
              "| Class | Window | Hidden word(s) | Relative word(s), as written | Relative lines holding it | Normalised only |",
              "|---|---|---|---|---|---|"]
        for r in v["hits"]:
            L.append(f"| {r['class']} | {r['window']} | {' '.join(r['hidden_words'])} | "
                     f"{' '.join(r['relative_words_as_written'])} | {r['n_relative_lines']} | {'yes' if r['normalised_only'] else ''} |")
        L.append("")
    (OUT / "verbatim.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
