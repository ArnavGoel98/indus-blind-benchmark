"""Test fixtures. Tests never need downloaded data: a toy 'language' is registered in memory."""

import numpy as np
import pytest

from ibdb import phonology
from ibdb.generator import build as gbuild

TOY = "latin~toy"  # base 'latin' so it counts as a language (family indo-european)


def _toy_segments(seed: int = 0, n_words: int = 300, n_clauses: int = 3000) -> dict:
    rng = np.random.default_rng(seed)
    cons, vows = list("ptkmnslr"), list("aeiou")
    words = []
    for i in range(n_words):
        k = int(rng.integers(1, 4))
        form = "".join(cons[int(rng.integers(len(cons)))] + vows[int(rng.integers(len(vows)))] for _ in range(k))
        form += str(i) if any(w[0] == form for w in words) else ""
        form = "".join(c for c in form if not c.isdigit()) + ("" if not any(w[0] == form for w in words) else "")
        ph = phonology.LATIN.phonemes(form)
        words.append([f"{form}{i}", ph, phonology.syllabify(ph, phonology.LATIN.vowels), None])
    zipf = 1.0 / np.arange(1, n_words + 1)
    zipf /= zipf.sum()
    clauses = []
    for _ in range(n_clauses):
        L = int(rng.integers(1, 7))
        clauses.append(["line", [int(x) for x in rng.choice(n_words, size=L, p=zipf)]])
    freq = np.bincount([w for _, c in clauses for w in c], minlength=n_words).astype(float)
    order = np.argsort(-freq, kind="stable")
    rank = np.empty(n_words, dtype=np.int64)
    rank[order] = np.arange(1, n_words + 1)
    return {"name": TOY, "family": "indo-european", "is_linguistic": True, "kind": "language",
            "words": words, "clauses": clauses, "_rank": rank, "_logf": np.log((freq + 0.5) / freq.sum())}


@pytest.fixture(scope="session")
def toy_source():
    gbuild._DISGUISED[TOY] = _toy_segments()
    return TOY
