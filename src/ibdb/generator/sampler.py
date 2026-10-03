"""Seal-like text sampling.

1. Draw a target length (in signs) for each text from a discretized log-normal whose median
   and mean match the calibration targets. The shape (sigma) stays fixed when the mean is
   swept, so "longer texts" means the same distribution stretched, not a different genre.
2. Pick a contiguous word window (inside one clause) whose ENCODED length equals the target.
   Windows are weighted by
       alpha * mean log-frequency of their words   (formulaic, high-frequency phrases)
     + beta  * log-frequency of their last word     (concentrated text endings)
     + gamma * log-frequency of their first word    (negative = diverse text beginnings)
     + kappa * [window starts the clause]           (titles/names open the clause)
3. If no window has exactly that length, take the shortest longer window and truncate it
   (counted and reported as ``truncated``). If nothing is long enough, concatenate windows.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SEAL_KINDS = {"name": 1.0, "epithet": 0.8, "seal": 1.5, "formula": 1.0, "description": 1.0,
              "line": 0.0, "clause": 0.0}


def lognormal_params(mean: float, median: float, max_len: int, ref_max: float, ref_n: int) -> tuple[float, float]:
    """mu, sigma of round(exp(N(mu, sigma))) clipped to [1, max_len].

    sigma is set so the expected maximum of ``ref_n`` draws equals ``ref_max``
    (sigma = (ln ref_max - ln median) / z, z the 1 - 1/ref_n normal quantile). mu is then
    bisected so the mean of the discretized distribution equals ``mean``. With the Indus
    targets (mean 4.4, median 4, max 17 over 5,500 texts) this gives sigma ~ 0.40, and all
    three statistics hold at once.
    """
    from scipy.stats import norm

    z = norm.ppf(1.0 - 1.0 / ref_n)
    sigma = max((np.log(ref_max) - np.log(median)) / z, 0.05)
    zz = np.random.default_rng(0).standard_normal(60_000)
    lo, hi = np.log(0.5), np.log(max_len)
    for _ in range(50):
        mu = 0.5 * (lo + hi)
        if np.clip(np.rint(np.exp(mu + sigma * zz)), 1, max_len).mean() < mean:
            lo = mu
        else:
            hi = mu
    return 0.5 * (lo + hi), sigma


def draw_lengths(rng: np.random.Generator, n: int, mean: float, median: float | None = None,
                 max_len: int | None = None, ref_mean: float = 4.4, ref_median: float = 4.0,
                 ref_max: int = 17, ref_n: int = 5500) -> np.ndarray:
    """Target lengths. When the mean is swept, the Indus shape is stretched by mean/ref_mean
    (median and maximum scale with it)."""
    scale = mean / ref_mean
    med = (median if median is not None else ref_median * scale)
    mx = ref_max * scale
    if max_len is None:
        max_len = int(np.ceil(mx + 4 * scale))
    mu, sigma = lognormal_params(mean, med, max_len, mx, ref_n)
    return np.clip(np.rint(np.exp(mu + sigma * rng.standard_normal(n))), 1, max_len).astype(np.int64)


@dataclass
class WindowIndex:
    """All candidate word windows of a source under one encoding (lengths fixed per word)."""

    flat: np.ndarray        # word ids, clauses concatenated
    start: np.ndarray       # window start offsets into flat
    nwords: np.ndarray
    length: np.ndarray      # encoded length in signs
    maxrank: np.ndarray     # max frequency rank of words in window (for vocabulary caps)
    mean_logf: np.ndarray
    last_logf: np.ndarray
    first_logf: np.ndarray
    clause_start: np.ndarray  # bool
    kind_w: np.ndarray


def build_windows(clauses: list, word_len: np.ndarray, word_rank: np.ndarray, word_logf: np.ndarray,
                  max_len: int, divider: bool, prefix_only: bool = False,
                  max_words: int = 64) -> WindowIndex:
    flat_parts, cid_parts, pos_parts, kind_parts = [], [], [], []
    clen = []
    for ci, (kind, ids) in enumerate(clauses):
        n = len(ids)
        flat_parts.append(ids)
        clen.append(n)
        kind_parts.append(SEAL_KINDS.get(kind, 0.0))
    clen_a = np.array(clen, dtype=np.int64)
    flat = np.fromiter((w for ids in flat_parts for w in ids), dtype=np.int64)
    cid = np.repeat(np.arange(len(clauses)), clen_a)
    offs = np.concatenate([[0], np.cumsum(clen_a)])
    pos = np.arange(len(flat)) - offs[cid]
    kind_w = np.array(kind_parts)[cid]
    remaining = clen_a[cid] - pos

    wl = word_len[flat]
    lf = word_logf[flat]
    rk = word_rank[flat]
    cs_len = np.concatenate([[0], np.cumsum(wl)])
    cs_lf = np.concatenate([[0.0], np.cumsum(lf)])

    starts, nws, lens, mrs, mlf, llf, flf, cst, kws = [], [], [], [], [], [], [], [], []
    base_idx = np.arange(len(flat))
    if prefix_only:
        base_idx = base_idx[pos == 0]
    running_max = rk[base_idx].copy()
    alive = base_idx
    for w in range(1, max_words + 1):
        ok = remaining[alive] >= w
        alive = alive[ok]
        running_max = running_max[ok]
        if len(alive) == 0:
            break
        if w > 1:
            running_max = np.maximum(running_max, rk[alive + w - 1])
        L = cs_len[alive + w] - cs_len[alive] + (w - 1 if divider else 0)
        keep = L <= max_len
        if not keep.any():
            # windows only get longer
            if (L > max_len).all():
                break
        a = alive[keep]
        starts.append(a)
        nws.append(np.full(len(a), w, dtype=np.int16))
        lens.append(L[keep])
        mrs.append(running_max[keep])
        mlf.append((cs_lf[a + w] - cs_lf[a]) / w)
        llf.append(lf[a + w - 1])
        flf.append(lf[a])
        cst.append(pos[a] == 0)
        kws.append(kind_w[a])
        # drop windows that already exceed max_len (extending can't shorten them)
        alive = alive[keep]
        running_max = running_max[keep]
    cat = np.concatenate
    return WindowIndex(flat, cat(starts), cat(nws), cat(lens), cat(mrs), cat(mlf), cat(llf), cat(flf), cat(cst), cat(kws))


def window_logits(wi: WindowIndex, alpha: float, beta: float, kappa: float = 1.0,
                  gamma: float = 0.0) -> np.ndarray:
    return (alpha * wi.mean_logf + beta * wi.last_logf + gamma * wi.first_logf
            + kappa * (wi.clause_start + wi.kind_w))


def pick_windows(wi: WindowIndex, targets: np.ndarray, logits: np.ndarray, mask: np.ndarray,
                 rng: np.random.Generator) -> list[tuple[int, int, int]]:
    """For each target length, return (start, nwords, truncate_to) ; truncate_to=0 means exact."""
    out: list[tuple[int, int, int]] = [None] * len(targets)  # type: ignore[list-item]
    valid = np.flatnonzero(mask)
    lens = wi.length[valid]
    order = np.argsort(lens, kind="stable")
    valid, lens = valid[order], lens[order]
    uniq, first = np.unique(lens, return_index=True)
    bounds = dict(zip(uniq.tolist(), zip(first.tolist(), np.append(first[1:], len(lens)).tolist())))
    by_len_targets: dict[int, list[int]] = {}
    for i, L in enumerate(targets.tolist()):
        by_len_targets.setdefault(L, []).append(i)
    for L, idxs in by_len_targets.items():
        trunc = 0
        if L in bounds:
            a, b = bounds[L]
        else:
            longer = uniq[uniq > L]
            if len(longer) == 0:
                for i in idxs:
                    out[i] = (-1, 0, int(L))  # signal: concatenate
                continue
            a, b = bounds[int(longer[0])]
            trunc = int(L)
        cand = valid[a:b]
        lg = logits[cand]
        p = np.exp(lg - lg.max())
        p /= p.sum()
        picks = rng.choice(cand, size=len(idxs), p=p)
        for i, c in zip(idxs, picks.tolist()):
            out[i] = (int(wi.start[c]), int(wi.nwords[c]), trunc)
    return out
