"""Scoring against an answer key. Shared by the evaluator and the public challenge scorer."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .corpus import AnswerKey

FAMILIES = ("indo-european", "dravidian", "isolate", "uralic")
SCRIPT_CLASSES = ("logographic", "syllabic", "logosyllabic", "alphabetic")


def score_sign_values(pred: dict[int, str] | None, key: AnswerKey, logical_texts: list[list[int]]) -> dict[str, float]:
    """Task D.

    token_acc  share of sign TOKENS whose predicted value equals that token's true value
               (polyvalent signs can only be right on some tokens; determinatives and word
               dividers count as tokens and are unrecoverable by value-only solvers)
    type_acc   share of sign TYPES whose prediction is one of the sign's values
    """
    pred = pred or {}
    n = hit = 0
    for t, vals in zip(logical_texts, key.token_values):
        for s, v in zip(t, vals):
            n += 1
            if pred.get(int(s)) == v:
                hit += 1
    types = key.sign_values
    t_hit = sum(1 for s, vs in types.items() if pred.get(int(s)) in vs)
    return {"token_acc": hit / n if n else 0.0, "type_acc": t_hit / len(types) if types else 0.0}


def wilson(k: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


def bootstrap_ci(x: np.ndarray, n_boot: int = 2000, seed: int = 0, alpha: float = 0.05) -> tuple[float, float]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = rng.choice(x, size=(n_boot, len(x)), replace=True).mean(axis=1)
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))


def segmentation_f1(pred: list[list[int]], key: AnswerKey) -> float:
    tp = fp = fn = 0
    for p, g in zip(pred, key.word_starts):
        ps, gs = set(p) - {0}, set(g) - {0}
        tp += len(ps & gs)
        fp += len(ps - gs)
        fn += len(gs - ps)
    return 2 * tp / (2 * tp + fp + fn) if tp else 0.0


def summarize_binary(correct: list[bool]) -> dict[str, Any]:
    k, n = int(sum(correct)), len(correct)
    lo, hi = wilson(k, n)
    return {"rate": k / n if n else float("nan"), "n": n, "ci_lo": lo, "ci_hi": hi}


def cluster_bootstrap(values, clusters, stat=None, n_boot: int = 2000, seed: int = 0,
                      alpha: float = 0.05) -> tuple[float, float]:
    """Two-stage bootstrap: resample clusters (source languages / control families) with
    replacement, then items within each drawn cluster. Corpora from the same source are not
    independent, so this interval is wider than a Wilson or plain bootstrap interval.

    ``values``: per-item values (numbers or bools; or tuples passed to ``stat``).
    ``stat``: function of a list of items -> float (default: mean).
    """
    items = list(values)
    if not items:
        return (float("nan"), float("nan"))
    if stat is None:
        return _cluster_bootstrap_mean(np.asarray(items, dtype=float), list(clusters), n_boot, seed, alpha)
    groups: dict = {}
    for v, c in zip(items, clusters):
        groups.setdefault(c, []).append(v)
    keys = list(groups)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n_boot):
        drawn = []
        for k in rng.choice(len(keys), size=len(keys), replace=True):
            g = groups[keys[int(k)]]
            drawn.extend(g[int(i)] for i in rng.integers(len(g), size=len(g)))
        try:
            out.append(stat(drawn))
        except (ValueError, ZeroDivisionError):
            continue
    out = np.array([o for o in out if np.isfinite(o)])
    if len(out) == 0:
        return (float("nan"), float("nan"))
    return (float(np.quantile(out, alpha / 2)), float(np.quantile(out, 1 - alpha / 2)))


def summarize_clustered(correct: list[bool], clusters: list) -> dict:
    """Rate with a cluster-bootstrap 95% interval (primary) and the Wilson interval (for reference)."""
    k, n = int(sum(correct)), len(correct)
    lo, hi = cluster_bootstrap([float(c) for c in correct], clusters)
    wlo, whi = wilson(k, n)
    return {"rate": k / n if n else float("nan"), "n": n, "n_clusters": len(set(clusters)),
            "ci_lo": lo, "ci_hi": hi, "wilson_lo": wlo, "wilson_hi": whi}


def _cluster_bootstrap_mean(x: np.ndarray, clusters: list, n_boot: int, seed: int, alpha: float) -> tuple[float, float]:
    """Vectorized two-stage bootstrap of the mean (same scheme as cluster_bootstrap)."""
    keys = sorted(set(clusters), key=str)
    idx = {k: np.flatnonzero(np.array([c == k for c in clusters])) for k in keys}
    K = len(keys)
    rng = np.random.default_rng(seed)
    sums = np.empty((K, n_boot, K))
    sizes = np.array([len(idx[k]) for k in keys], dtype=float)
    for j, k in enumerate(keys):
        g = x[idx[k]]
        draws = rng.integers(len(g), size=(n_boot, K, len(g)))
        sums[j] = g[draws].sum(axis=2)
    pick = rng.integers(K, size=(n_boot, K))
    b = np.arange(n_boot)[:, None]
    pos = np.arange(K)[None, :]
    tot = sums[pick, b, pos].sum(axis=1)
    n = sizes[pick].sum(axis=1)
    means = tot / n
    return (float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2)))
