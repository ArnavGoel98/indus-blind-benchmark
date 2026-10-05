"""Verbatim overlap: share of hidden texts (Indus point) whose word sequence occurs inside some clause
of the sister's source half. Analysis only (regenerates corpora deterministically; methods not run).
Usage: IBDB_SISTER_VERSION=v3 python scripts/sister_overlap.py   (v3 split == v2 split; v3 only exposes word ids)
"""
import sys
import numpy as np
from ibdb.evaluate import load_knobs
from ibdb.generator.build import make_corpus, split_clauses, _segments
from ibdb.knowledge import MAX_REF_CLAUSES

LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]

def contained_share(word_ids, clauses):
    texts = [tuple(ids) for ids, _ in word_ids]
    want = set(texts)
    lens = sorted({len(t) for t in want})
    found = set()
    for c in clauses:
        ids = tuple(c[1]); n = len(ids)
        for L in lens:
            if L > n: break
            for i in range(n - L + 1):
                s = ids[i:i + L]
                if s in want: found.add(s)
    return np.mean([t in found for t in texts])

def main():
  for gv in ("v1", "v2"):
      for lang in LANGS:
          ref = split_clauses(lang, _segments(lang), "reference")[:MAX_REF_CLAUSES]
          shares = []
          for st in SCRIPTS:
              for seed in (0, 1, 2):
                  knobs, spec = load_knobs("full", lang, st, gv)
                  _, _, info = make_corpus(lang, spec, 2906, 4.6, seed, knobs, generator_version=gv)
                  shares.append(contained_share(info["_word_ids"], ref))
          print(f"generator {gv} {lang}: {100*np.mean(shares):.0f}% (range {100*min(shares):.0f}-{100*max(shares):.0f}%, n={len(shares)})", flush=True)


if __name__ == "__main__":
    main()
