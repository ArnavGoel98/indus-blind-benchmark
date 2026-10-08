"""Positive control: ordering of conditional entropy across reference corpora, compared with
Rao et al. (2009, Science 324:1165, Fig. 1A and 1B; values read by eye from the published figure, no table
exists). Uses the frozen `ibdb.stats.conditional_entropy` unchanged; analysis only.

Rao's measures: (A) H(X2|X1) in nats over the N most frequent tokens (rarer merged); (B) "relative
conditional entropy": conditional entropy relative to a uniformly random sequence with the same number of
tokens. We approximate (B) by dividing by H(X2|X1) of the same tokens randomly shuffled (same unigram
distribution), at N = 400 most frequent tokens.
Usage: python scripts/positive_control_rao.py > reports/positive_controls/rao2009_entropy_ordering.md
"""
import math
import re
from pathlib import Path

import numpy as np

from ibdb.controls import CONTROLS
from ibdb.knowledge import build_reference
from ibdb.stats import conditional_entropy

N_LIST = [20, 100, 200, 400]
MAX_TOKENS = 400_000
RAO_FIG1B = {"Type 1 (no order)": 1.00, "DNA": 0.98, "Protein": 0.96, "Sanskrit": 0.66, "English words": 0.64,
             "Sumerian": 0.57, "Old Tamil": 0.56, "Indus": 0.55, "English chars": 0.51, "Fortran": 0.39,
             "Type 2 (rigid)": 0.0}


def ints(texts):
    m = {}
    out, n = [], 0
    for t in texts:
        if n >= MAX_TOKENS:
            break
        out.append([m.setdefault(x, len(m)) for x in t]); n += len(t)
    return out


def h_cond(texts, N):
    return conditional_entropy(texts, N)[1] * math.log(2)   # bits -> nats


def shuffled(texts, seed=0):
    rng = np.random.default_rng(seed)
    flat = np.array([x for t in texts for x in t]); rng.shuffle(flat)
    out, i = [], 0
    for t in texts:
        out.append(flat[i:i + len(t)].tolist()); i += len(t)
    return out


def english():
    p = Path("data/raw/english/pg1342.txt")
    w = re.findall(r"[a-z]+", p.read_text(encoding="utf-8", errors="ignore").lower())
    sent = [w[i:i + 12] for i in range(0, len(w), 12)]
    return sent, [list("".join(s)) for s in sent]


def main():
    corp = {"Sanskrit (syllables)": build_reference("sanskrit", "syllabic", False, 0).texts,
            "Old Tamil (syllables)": build_reference("tamil", "syllabic", False, 0).texts,
            "Sumerian (logo-syllabic signs)": build_reference("sumerian", "logosyllabic", False, 0).texts}
    ew, ec = english()
    corp["English words"] = ew
    corp["English chars"] = ec
    rng = np.random.default_rng(0)
    corp["Our i.i.d. control (Rao type 1; our `rao_type2`)"] = [CONTROLS["rao_type2"](0).make_text(rng, 6) for _ in range(40000)]
    corp["Our rigid control (Rao type 2; our `rao_type1`)"] = [CONTROLS["rao_type1"](0).make_text(rng, 6) for _ in range(40000)]
    print("# Positive control: conditional-entropy ordering vs Rao et al. (2009)\n")
    print("Rao et al. give these measures only as figures (Fig. 1A curves, Fig. 1B bars; the supplement's "
          "Table S1 has Indus perplexities only), so their values below are read by eye. Their corpora differ "
          "from ours (Rig Veda vs Ramayana; Brown corpus vs Pride and Prejudice; ETCSL vs CDLI), so only the "
          "ORDERING is comparable. Note: Rao's 'type 1' is the system without sequential order and 'type 2' the "
          "rigid one; our control keys use the opposite numbering.\n")
    print("| Corpus | H(X2|X1), nats, N=20 | N=100 | N=200 | N=400 | Relative (vs shuffled), N=400 |")
    print("|---|---|---|---|---|---|")
    rel = {}
    for name, texts in corp.items():
        t = ints(texts)
        hs = [h_cond(t, N) for N in N_LIST]
        r = hs[-1] / h_cond(shuffled(t), 400) if h_cond(shuffled(t), 400) > 0 else float("nan")
        rel[name] = r
        print(f"| {name} | " + " | ".join(f"{h:.2f}" for h in hs) + f" | {r:.2f} |", flush=True)
    print("\n**Rao et al. 2009, Fig. 1B (read by eye):** " + ", ".join(f"{k} {v:.2f}" for k, v in RAO_FIG1B.items()) + ".\n")
    order = sorted(rel, key=lambda k: -rel[k])
    print("**Our ordering (relative, N=400, high to low):** " + " > ".join(f"{k} ({rel[k]:.2f})" for k in order) + ".\n")


if __name__ == "__main__":
    main()
