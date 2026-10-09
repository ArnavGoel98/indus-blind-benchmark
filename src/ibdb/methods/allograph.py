"""v2 method: allograph merging by distributional similarity (pre-processing for Tasks C and D).

Not part of frozen-v1. It will be frozen with the other v2 methods as `frozen-v2` before any v2
final run.

Idea. Graphic variants of one sign are interchangeable, so each variant's neighbours are drawn from
the same distribution as its base sign's. For every sign b (rarest first), find the more frequent
sign a whose left- and right-neighbour distribution is closest. Merge b into a only if b's
neighbour counts are consistent with having been drawn from the distribution of a and b pooled. The
test is a parametric bootstrap of the G statistic for homogeneity of a 2 x K table. Because a rare
sign is consistent with almost anything, the best match must also stand out: its Jensen-Shannon
divergence must be at most max_ratio times the median divergence to all candidates. Nothing reads
the answer key. Parameters: min_count (the rarer sign needs at least this many tokens), alpha (the
test level), max_ratio, and rounds (passes, recomputing neighbours over merged signs). They were chosen on
development corpora (seeds 90-91), never on benchmark corpora: min_count=10, alpha=0.05,
max_ratio=0.6, chosen for merge precision (reports/v2/allograph/dev2.md), not for Task D accuracy.
"""

from __future__ import annotations

from collections import Counter
from typing import Sequence

import numpy as np

from ..corpus import Corpus


def _contexts(texts: Sequence[Sequence[int]], rep: dict[int, int], index: dict[int, int]) -> np.ndarray:
    """Row per sign: counts of left neighbours (or text start) then right neighbours (or text end),
    with neighbours mapped through the current merge `rep`."""
    V = len(index)
    reps = sorted({rep[s] for s in index})
    col = {r: i for i, r in enumerate(reps)}
    K = len(reps)
    M = np.zeros((V, 2 * (K + 1)), dtype=np.float64)
    for t in texts:
        for i, s in enumerate(t):
            row = index[s]
            left = col[rep[t[i - 1]]] if i > 0 else K
            right = col[rep[t[i + 1]]] if i + 1 < len(t) else K
            M[row, left] += 1
            M[row, K + 1 + right] += 1
    return M


def _g(x: np.ndarray, y: np.ndarray) -> float:
    """G statistic for homogeneity of two count vectors."""
    tot = x + y
    nz = tot > 0
    x, y, tot = x[nz], y[nz], tot[nz]
    nx, ny = x.sum(), y.sum()
    n = nx + ny
    ex, ey = tot * nx / n, tot * ny / n
    with np.errstate(divide="ignore", invalid="ignore"):
        g = np.where(x > 0, x * np.log(x / ex), 0.0).sum() + np.where(y > 0, y * np.log(y / ey), 0.0).sum()
    return float(2 * g)


def _jsd(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Jensen-Shannon divergence between one row p and each row of q (both normalised)."""
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(p > 0, p * np.log(p / m), 0.0).sum(axis=1)
        b = np.where(q > 0, q * np.log(q / m), 0.0).sum(axis=1)
    return 0.5 * (a + b)


class AllographMerger:
    name = "allograph_merge_v2"

    def __init__(self, min_count: int = 10, alpha: float = 0.05, max_ratio: float | None = 0.6, n_boot: int = 200,
                 rounds: int = 2, seed: int = 0):
        self.min_count, self.alpha, self.max_ratio = min_count, alpha, max_ratio
        self.n_boot, self.rounds, self.seed = n_boot, rounds, seed

    def fit(self, texts: Sequence[Sequence[int]]) -> dict[int, int]:
        """Return sign -> representative sign (a representative maps to itself)."""
        rng = np.random.default_rng(self.seed)
        freq = Counter(s for t in texts for s in t)
        signs = sorted(freq, key=lambda s: (-freq[s], s))
        index = {s: i for i, s in enumerate(signs)}
        rep = {s: s for s in signs}
        for _ in range(self.rounds):
            C = _contexts(texts, rep, index)
            P = C / np.maximum(C.sum(axis=1, keepdims=True), 1)
            changed = False
            for b in reversed(signs):                      # rarest first
                if rep[b] != b or freq[b] < self.min_count:
                    continue
                ib = index[b]
                cands = [index[a] for a in signs if a != b and rep[a] == a and freq[a] >= freq[b]]
                if not cands:
                    continue
                cands = np.array(cands)
                d = _jsd(P[ib], P[cands])
                k = int(np.argmin(d))
                ia = int(cands[k])
                # The best match must stand out: a rare sign with few contexts is "consistent" with
                # almost anything, so require its divergence to be well below the typical one.
                if self.max_ratio is not None and d[k] > self.max_ratio * float(np.median(d)):
                    continue
                if self._consistent(C[ib], C[ia], rng):
                    a = signs[ia]
                    for s, r in rep.items():
                        if r == b:
                            rep[s] = a
                    changed = True
            if not changed:
                break
        return rep

    def _consistent(self, cb: np.ndarray, ca: np.ndarray, rng: np.random.Generator) -> bool:
        g_obs = _g(cb, ca)
        pooled = (cb + ca) / (cb + ca).sum()
        nb, na = int(cb.sum()), int(ca.sum())
        null = np.empty(self.n_boot)
        for k in range(self.n_boot):
            null[k] = _g(rng.multinomial(nb, pooled).astype(float), rng.multinomial(na, pooled).astype(float))
        return g_obs <= np.quantile(null, 1 - self.alpha)

    def merge(self, corpus: Corpus) -> tuple[Corpus, dict[int, int]]:
        """Corpus with every sign replaced by its representative (physical order kept)."""
        rep = self.fit([t.tolist() for t in corpus.logical()])
        texts = [np.array([rep[int(x)] for x in t], dtype=np.int64) for t in corpus.texts]
        return Corpus(corpus.corpus_id + "-merged", texts, corpus.direction, dict(corpus.meta)), rep


def expand_values(pred: dict[int, str], rep: dict[int, int]) -> dict[int, str]:
    """Give every original sign the value predicted for its representative."""
    return {s: pred[r] for s, r in rep.items() if r in pred}


def merge_scores(rep: dict[int, int], allographs: dict[int, list[int]],
                 sign_values: dict[int, list[str]]) -> dict[str, float]:
    """Pairwise precision / recall of merged pairs against the hidden allograph groups; also the
    share of merged pairs whose signs carry the same value(s) (harmless merges such as homophones)."""
    signs = sorted(rep)
    true = {}
    for base, grp in allographs.items():
        for s in grp:
            true[s] = base
    pred_groups: dict[int, list[int]] = {}
    for s in signs:
        pred_groups.setdefault(rep[s], []).append(s)
    pred_pairs = {(a, b) for g in pred_groups.values() for i, a in enumerate(g) for b in g[i + 1:]}
    true_groups: dict[int, list[int]] = {}
    for s in signs:
        true_groups.setdefault(true.get(s, s), []).append(s)
    true_pairs = {tuple(sorted((a, b))) for g in true_groups.values() for i, a in enumerate(g) for b in g[i + 1:]}
    pred_pairs = {tuple(sorted(p)) for p in pred_pairs}
    tp = len(pred_pairs & true_pairs)
    same_val = sum(1 for a, b in pred_pairs if sign_values.get(a) == sign_values.get(b))
    return {"n_signs": len(signs), "n_true_groups": len(true_groups), "n_pred_groups": len(pred_groups),
            "pairs_pred": len(pred_pairs), "pairs_true": len(true_pairs),
            "precision": tp / len(pred_pairs) if pred_pairs else 1.0,
            "recall": tp / len(true_pairs) if true_pairs else 1.0,
            "value_consistent": same_val / len(pred_pairs) if pred_pairs else 1.0}
