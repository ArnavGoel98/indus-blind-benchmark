"""Small, dependency-free learners used by the evaluator (fit on training corpora only)."""

from __future__ import annotations

import numpy as np


def balanced_accuracy(y: np.ndarray, p: np.ndarray) -> float:
    y, p = np.asarray(y, bool), np.asarray(p, bool)
    pos, neg = y.sum(), (~y).sum()
    tpr = (p & y).sum() / pos if pos else 0.0
    tnr = (~p & ~y).sum() / neg if neg else 0.0
    return 0.5 * (tpr + tnr)


def fit_threshold(x: np.ndarray, y: np.ndarray) -> tuple[float, int]:
    """Best one-sided cut (value, direction) by balanced accuracy. direction +1: x > cut is positive."""
    xs = np.unique(x)
    cuts = np.concatenate([[xs[0] - 1e-9], (xs[:-1] + xs[1:]) / 2, [xs[-1] + 1e-9]]) if len(xs) > 1 else np.array([xs[0]])
    best = (-1.0, 0.0, 1)
    for c in cuts:
        for d in (1, -1):
            ba = balanced_accuracy(y, (x > c) if d == 1 else (x <= c))
            if ba > best[0] + 1e-12:
                best = (ba, float(c), d)
    return best[1], best[2]


def apply_threshold(x: np.ndarray, cut: float, d: int) -> np.ndarray:
    return (x > cut) if d == 1 else (x <= cut)


def fit_band(x: np.ndarray, y: np.ndarray, grid: int = 40) -> tuple[float, float, bool]:
    """Best interval [lo, hi]; inside=True means inside the band is positive (Rao's claim)."""
    qs = np.unique(np.quantile(x, np.linspace(0, 1, grid)))
    best = (-1.0, qs[0], qs[-1], True)
    for i, lo in enumerate(qs):
        for hi in qs[i:]:
            inside = (x >= lo) & (x <= hi)
            for flag in (True, False):
                ba = balanced_accuracy(y, inside if flag else ~inside)
                if ba > best[0] + 1e-12:
                    best = (ba, float(lo), float(hi), flag)
    return best[1], best[2], best[3]


def apply_band(x: np.ndarray, lo: float, hi: float, inside: bool) -> np.ndarray:
    m = (x >= lo) & (x <= hi)
    return m if inside else ~m


class Standardizer:
    def fit(self, X):
        self.mu = X.mean(axis=0)
        self.sd = X.std(axis=0) + 1e-9
        return self

    def transform(self, X):
        return (X - self.mu) / self.sd


def fit_logreg(X: np.ndarray, y: np.ndarray, l2: float = 1.0, iters: int = 300) -> tuple[Standardizer, np.ndarray]:
    """Binary logistic regression with class-balanced weights (Newton steps)."""
    st = Standardizer().fit(X)
    Z = np.hstack([st.transform(X), np.ones((len(X), 1))])
    y = y.astype(float)
    w_pos = 0.5 / max(y.mean(), 1e-9)
    w_neg = 0.5 / max(1 - y.mean(), 1e-9)
    sw = np.where(y > 0, w_pos, w_neg)
    w = np.zeros(Z.shape[1])
    reg = np.eye(Z.shape[1]) * l2
    reg[-1, -1] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(Z @ w, -30, 30)))
        g = Z.T @ (sw * (p - y)) + reg @ w
        H = (Z * (sw * p * (1 - p))[:, None]).T @ Z + reg
        step = np.linalg.solve(H, g)
        w -= step
        if np.abs(step).max() < 1e-8:
            break
    return st, w


def predict_logreg(model, X: np.ndarray) -> np.ndarray:
    st, w = model
    Z = np.hstack([st.transform(X), np.ones((len(X), 1))])
    return 1 / (1 + np.exp(-np.clip(Z @ w, -30, 30)))


def fit_softmax(X: np.ndarray, y: list[str], l2: float = 1.0, iters: int = 2000, lr: float = 0.1):
    classes = sorted(set(y))
    st = Standardizer().fit(X)
    Z = np.hstack([st.transform(X), np.ones((len(X), 1))])
    Y = np.array([[c == v for c in classes] for v in y], dtype=float)
    W = np.zeros((Z.shape[1], len(classes)))
    for _ in range(iters):
        S = Z @ W
        S -= S.max(axis=1, keepdims=True)
        P = np.exp(S)
        P /= P.sum(axis=1, keepdims=True)
        G = Z.T @ (P - Y) / len(Z) + l2 * np.vstack([W[:-1], np.zeros((1, W.shape[1]))]) / len(Z)
        W -= lr * G
    return st, W, classes


def predict_softmax(model, X: np.ndarray) -> list[str]:
    st, W, classes = model
    Z = np.hstack([st.transform(X), np.ones((len(X), 1))])
    return [classes[i] for i in np.argmax(Z @ W, axis=1)]
