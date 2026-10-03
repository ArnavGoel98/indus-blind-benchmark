"""Corpus statistics used for calibration and reporting.

Size-dependent statistics are computed on a random subsample with the same number of texts
as the published reference corpus (``reference_n_texts`` in config/indus_targets.yaml), so
synthetic and Indus numbers are compared like-for-like.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Sequence

import numpy as np
from scipy.optimize import curve_fit


def _subsample(texts: Sequence, n: int | None, seed: int) -> list:
    if n is None or n >= len(texts):
        return list(texts)
    idx = np.random.default_rng(seed).choice(len(texts), size=n, replace=False)
    return [texts[i] for i in sorted(idx)]


def coverage_count(counts: Counter, share: float = 0.8) -> int:
    """Smallest number of types whose tokens reach ``share`` of all tokens."""
    if not counts:
        return 0
    c = np.sort(np.fromiter(counts.values(), dtype=np.float64))[::-1]
    cum = np.cumsum(c) / c.sum()
    return int(np.searchsorted(cum, share - 1e-12) + 1)


def zipf_mandelbrot_fit(counts: Counter) -> dict[str, float]:
    """Fit log f_r = a - b log(r + c) (natural log), as in Yadav et al. (2010)."""
    f = np.sort(np.fromiter(counts.values(), dtype=np.float64))[::-1]
    if len(f) < 5:
        return {"a": float("nan"), "b": float("nan"), "c": float("nan")}
    r = np.arange(1, len(f) + 1, dtype=np.float64)

    def model(r, a, b, c):
        return a - b * np.log(r + c)

    try:
        p, _ = curve_fit(model, r, np.log(f), p0=[np.log(f[0]) + 1, 1.0, 1.0],
                         bounds=([-np.inf, 0.01, 0.0], [np.inf, 10.0, 1000.0]), maxfev=20000)
        return {"a": float(p[0]), "b": float(p[1]), "c": float(p[2])}
    except (RuntimeError, ValueError):
        return {"a": float("nan"), "b": float("nan"), "c": float("nan")}


def corpus_stats(texts: Sequence[Sequence[int]], targets: dict[str, Any] | None = None,
                 seed: int = 0) -> dict[str, Any]:
    """All calibration statistics. ``texts`` must be in reading order."""
    texts = [list(t) for t in texts if len(t) > 0]
    lengths = np.array([len(t) for t in texts])
    counts = Counter(s for t in texts for s in t)
    ref = lambda name, default: (targets or {}).get(name, {}).get("reference_n_texts", default)  # noqa: E731

    sub_cov = _subsample(texts, ref("coverage80_signs", 1548), seed)
    c_cov = Counter(s for t in sub_cov for s in t)
    sub_hap = _subsample(texts, ref("hapax_fraction", 2906), seed + 1)
    c_hap = Counter(s for t in sub_hap for s in t)
    sub_pos = _subsample(texts, ref("enders80_signs", 1548), seed + 2)
    seen = set()
    dup = 0
    for t in texts:
        k = tuple(t)
        if k in seen:
            dup += 1
        seen.add(k)
    out = {
        "n_texts": len(texts),
        "n_tokens": int(lengths.sum()),
        "mean_length": float(lengths.mean()) if len(texts) else 0.0,
        "median_length": float(np.median(lengths)) if len(texts) else 0.0,
        "max_length": int(lengths.max()) if len(texts) else 0,
        "sign_inventory": len(counts),
        "coverage80_signs": coverage_count(c_cov),
        "top1_share": float(max(c_cov.values()) / sum(c_cov.values())) if c_cov else 0.0,
        "hapax_fraction": float(sum(1 for v in c_hap.values() if v == 1) / len(c_hap)) if c_hap else 0.0,
        "enders80_signs": coverage_count(Counter(t[-1] for t in sub_pos)),
        "beginners80_signs": coverage_count(Counter(t[0] for t in sub_pos)),
        "duplicate_text_fraction": dup / max(len(texts), 1),
    }
    zm = zipf_mandelbrot_fit(c_cov)
    out.update({"zm_a": zm["a"], "zm_b": zm["b"], "zm_c": zm["c"]})
    return out


def check_targets(stats: dict[str, Any], specs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per-target pass/fail and normalized deviation."""
    res: dict[str, dict[str, Any]] = {}
    for name, spec in specs.items():
        v = stats.get(name)
        if v is None:
            continue
        if "range" in spec:
            lo, hi = spec["range"]
            dev = 0.0 if lo <= v <= hi else (lo - v if v < lo else v - hi) / max(0.1 * (hi - lo), 1.0)
            ok = lo <= v <= hi
            target = f"[{lo}, {hi}]"
        else:
            tol = float(spec.get("tolerance", 0))
            diff = v - spec["value"]
            dev = diff / tol if tol > 0 else (0.0 if diff == 0 else diff / max(abs(spec["value"]) * 0.01, 1e-9))
            ok = abs(diff) <= tol + 1e-9
            target = f"{spec['value']} ± {tol}"
        res[name] = {"value": v, "target": target, "ok": bool(ok), "dev": float(dev)}
    return res


# --------------------------------------------------------------------------- entropy helpers


def entropy_from_counts(c: np.ndarray) -> float:
    c = c[c > 0].astype(np.float64)
    if c.size == 0:
        return 0.0
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def conditional_entropy(texts: Sequence[Sequence[int]], top_k: int | None = None) -> tuple[float, float]:
    """(H(X1) unigram entropy, H(X2|X1)) over within-text bigrams, rarer signs merged to UNK."""
    counts = Counter(s for t in texts for s in t)
    if top_k is not None:
        keep = {s for s, _ in counts.most_common(top_k)}
        texts = [[s if s in keep else -1 for s in t] for t in texts]
        counts = Counter(s for t in texts for s in t)
    uni = entropy_from_counts(np.fromiter(counts.values(), dtype=np.float64))
    big = Counter((a, b) for t in texts for a, b in zip(t, t[1:]))
    if not big:
        return uni, 0.0
    first = Counter()
    for (a, _), v in big.items():
        first[a] += v
    hj = entropy_from_counts(np.fromiter(big.values(), dtype=np.float64))
    h1 = entropy_from_counts(np.fromiter(first.values(), dtype=np.float64))
    return uni, hj - h1


def ratio_from_token_texts(texts: list[list[str]], top_k: int | None = 100) -> float:
    m = {}
    ints = [[m.setdefault(x, len(m)) for x in t] for t in texts]
    h1, h2 = conditional_entropy(ints, top_k)
    return h2 / h1 if h1 > 0 else 0.0
