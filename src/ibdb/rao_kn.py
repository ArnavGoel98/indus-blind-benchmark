"""Rao et al. (2009) conditional entropy, as described in their Science supplement (post-hoc analysis).

Not a benchmark method: the frozen ``rao2009_entropy`` method (plug-in conditional-to-unigram entropy
ratio) is unchanged. This module follows the supplement's Materials and Methods:

* P(j|i) is estimated with interpolated modified Kneser-Ney smoothing (Chen & Goodman 1998, TR-10-98),
  bigram order, with the lower-order continuation distribution interpolated with a uniform
  distribution over the token set;
* P(i) is the token's relative frequency (Rao: "calculated based on the frequency of the token");
* C = -sum_i P(i) sum_j P(j|i) ln P(j|i), in nats (Equation S2);
* relative conditional entropy = C / ln N, i.e. relative to a uniformly random sequence over the same
  number N of tokens (Fig. 1B caption).

Choices the supplement does not fix, kept explicit and reported with the results:
* bigrams are counted within a line only (no boundary tokens);
* with a top-N token set, a token outside the set breaks the line (no bigram spans it); ``oov="merge"``
  instead maps all such tokens to one extra token, as a sensitivity check;
* when a count-of-counts needed for a discount is zero, the discount falls back to its upper bound
  clipped into [0, k] (only happens for tiny or degenerate corpora).
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Hashable, Sequence

import numpy as np


def _discounts(counts: Sequence[int]) -> tuple[float, float, float]:
    """Modified KN discounts D1, D2, D3+ from count-of-counts (Chen & Goodman 1998, eq. 26)."""
    n = Counter(c for c in counts if c > 0)
    n1, n2, n3, n4 = (n.get(k, 0) for k in (1, 2, 3, 4))
    if n1 == 0 or n1 + 2 * n2 == 0:
        return 0.5, 1.0, 1.5
    y = n1 / (n1 + 2 * n2)
    d1 = 1 - 2 * y * n2 / n1
    d2 = 2 - 3 * y * n3 / n2 if n2 else 1.0
    d3 = 3 - 4 * y * n4 / n3 if n3 else 1.5
    return (min(max(d1, 0.0), 1.0), min(max(d2, 0.0), 2.0), min(max(d3, 0.0), 3.0))


def _d(c: np.ndarray, D: tuple[float, float, float]) -> np.ndarray:
    return np.where(c == 0, 0.0, np.where(c == 1, D[0], np.where(c == 2, D[1], D[2])))


def mkn_bigram(seqs: Sequence[Sequence[int]], V: int) -> tuple[np.ndarray, np.ndarray]:
    """Return (P(i) as a length-V vector, P(j|i) as a V x V row-stochastic matrix)."""
    B = np.zeros((V, V), dtype=np.float64)
    uni = np.zeros(V, dtype=np.float64)
    for s in seqs:
        for a in s:
            uni[a] += 1
        for a, b in zip(s, s[1:]):
            B[a, b] += 1
    # Lower order: continuation counts N1+(.w), modified-KN discounted, interpolated with uniform.
    cont = (B > 0).sum(axis=0).astype(np.float64)
    tot = cont.sum()
    if tot > 0:
        Dc = _discounts(cont.astype(int).tolist())
        dc = _d(cont, Dc)
        gamma0 = dc.sum() / tot
        p_low = np.maximum(cont - dc, 0) / tot + gamma0 / V
    else:
        p_low = np.full(V, 1.0 / V)
    # Higher order.
    Db = _discounts(B[B > 0].astype(int).tolist())
    row = B.sum(axis=1)
    P = np.empty_like(B)
    db = _d(B, Db)
    for i in range(V):
        if row[i] == 0:
            P[i] = p_low
            continue
        gamma = db[i].sum() / row[i]
        P[i] = np.maximum(B[i] - db[i], 0) / row[i] + gamma * p_low
    p_i = uni / uni.sum() if uni.sum() else np.full(V, 1.0 / V)
    return p_i, P


def _index(texts: Sequence[Sequence[Hashable]], top_n: int | None, oov: str) -> tuple[list[list[int]], int]:
    freq = Counter(x for t in texts for x in t)
    keep = [x for x, _ in freq.most_common(top_n)] if top_n else list(freq)
    idx = {x: i for i, x in enumerate(keep)}
    seqs: list[list[int]] = []
    V = len(keep)
    for t in texts:
        if oov == "merge":
            seqs.append([idx.get(x, V) for x in t])
            continue
        cur: list[int] = []
        for x in t:
            if x in idx:
                cur.append(idx[x])
            else:
                if cur:
                    seqs.append(cur)
                cur = []
        if cur:
            seqs.append(cur)
    if oov == "merge" and len(freq) > V:
        V += 1
    return seqs, V


def conditional_entropy_kn(texts: Sequence[Sequence[Hashable]], top_n: int | None = None,
                           oov: str = "break") -> dict[str, float]:
    """Rao's C (nats) and relative C / ln N over the top_n most frequent tokens (all tokens if None)."""
    seqs, V = _index(texts, top_n, oov)
    if V < 2:
        return {"C": 0.0, "relative": 0.0, "N": V, "tokens": 0}
    p_i, P = mkn_bigram(seqs, V)
    with np.errstate(divide="ignore", invalid="ignore"):
        h_rows = -np.where(P > 0, P * np.log(P), 0.0).sum(axis=1)
    C = float((p_i * h_rows).sum())
    return {"C": C, "relative": C / math.log(V), "N": V, "tokens": int(sum(len(s) for s in seqs))}
