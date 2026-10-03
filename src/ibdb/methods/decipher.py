"""Methods 7-8: sign-value recovery against a known language, plus a frequency baseline.

Both solvers need a ``Knowledge`` object with one or more ``Reference`` languages, written in
the same unit level as the script (oracle script type; an optimistic assumption that makes
reported recovery rates an UPPER bound). With several references they pick the best-fitting
one, which gives the Task C (language family) prediction.
"""

from __future__ import annotations

from collections import Counter

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..corpus import Corpus
from .base import Knowledge, Method, Prediction, Reference

OTHER = "<OTHER>"
OTHER_MASS = 0.03
BOUND = "<#>"


def _translate(values: dict[int, str], ref: Reference) -> dict[int, str]:
    """Map reference-language units to their hidden-language cognates where one exists."""
    if not ref.to_hidden:
        return values
    return {s: ref.to_hidden.get(v, v) for s, v in values.items()}


class FrequencyRankBaseline(Method):
    name = "baseline_frequency_rank"
    tasks = ("C", "D")
    needs_knowledge = True
    paper = "Classical frequency-analysis baseline (k-th most frequent sign = k-th most frequent unit)."
    deviations = "None; reported as the floor every solver must beat."

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        if not knowledge or not knowledge.references:
            return Prediction(self.name)
        sc = Counter(s for t in corpus.texts for s in t.tolist())
        best = None
        for ref in knowledge.references:
            uc = Counter(u for t in ref.texts for u in t)
            sv = [s for s, _ in sc.most_common()]
            uv = [u for u, _ in uc.most_common()]
            vals = {s: uv[i] for i, s in enumerate(sv) if i < len(uv)}
            # fit: correlation of log rank-frequency profiles (scale-free)
            a = np.log(np.array([c for _, c in sc.most_common(50)], dtype=float))
            b = np.log(np.array([c for _, c in uc.most_common(50)], dtype=float))
            m = min(len(a), len(b))
            score = -float(np.mean(((a[:m] - a[:m].mean()) - (b[:m] - b[:m].mean())) ** 2)) if m > 2 else -1e9
            if best is None or score > best[0]:
                best = (score, ref, vals)
        scores = {}
        return Prediction(self.name, sign_values=_translate(best[2], best[1]), family=best[1].family,
                          family_scores=scores, extra={"reference": best[1].name})


class KnightEM(Method):
    name = "knight2006_em"
    tasks = ("C", "D")
    needs_knowledge = True
    paper = ("Knight, K., Nair, A., Rathod, N., Yamada, K. (2006). Unsupervised analysis for decipherment "
             "problems. Proc. COLING/ACL 2006. Bigram-count EM as in Berg-Kirkpatrick, T., Klein, D. (2013). "
             "Decipherment with a million random restarts. Proc. EMNLP 2013.")
    deviations = ("HMM substitution decipherment: hidden units follow a bigram LM of the reference language, "
                  "each emits a sign with learned P(sign|unit). EM on sign-bigram counts (text boundaries "
                  "included) instead of full sequences, a few random restarts rather than a million, "
                  "units capped at the 250 most frequent (+OTHER, emitting uniformly), signs at the 350 most "
                  "frequent (+OTHER). One frequency-informed start plus random restarts. With several "
                  "candidate languages, a short screening run picks the reference, then a full fit runs on it. "
                  "No null emissions, so determinatives and word dividers cannot be modelled.")

    def __init__(self, restarts: int = 3, iterations: int = 60, max_units: int = 250, max_signs: int = 350, seed: int = 0):
        self.restarts, self.iterations = restarts, iterations
        self.max_units, self.max_signs, self.seed = max_units, max_signs, seed

    def _fit(self, corpus: Corpus, ref: Reference, rng: np.random.Generator, restarts: int, iterations: int,
             unigram_only: bool = False):
        sc = Counter(s for t in corpus.logical() for s in t.tolist())
        signs = [s for s, _ in sc.most_common(self.max_signs)]
        sidx = {s: i for i, s in enumerate(signs)}
        S = len(signs) + 2                              # + OTHER + boundary
        s_other, s_b = len(signs), len(signs) + 1
        B = np.zeros((S, S))
        for t in corpus.logical():
            seq = [s_b] + [sidx.get(s, s_other) for s in t.tolist()] + [s_b]
            np.add.at(B, (seq[:-1], seq[1:]), 1)

        uc = Counter(u for t in ref.texts for u in t)
        units = [u for u, _ in uc.most_common(self.max_units)]
        uidx = {u: i for i, u in enumerate(units)}
        K = len(units) + 2
        u_other, u_b = len(units), len(units) + 1
        J = np.full((K, K), 0.1)
        for t in ref.texts:
            seq = [u_b] + [uidx.get(u, u_other) for u in t] + [u_b]
            np.add.at(J, (seq[:-1], seq[1:]), 1)
        J[u_b, u_b] = 0.0
        J /= J.sum()
        # Pin the pooled-rare-unit mass to the same share for every reference, so model
        # comparison across candidate languages is not decided by how heavy each tail is.
        p_o = J[u_other].sum()
        if p_o > 0:
            f = OTHER_MASS / p_o
            J[u_other] *= f
            J[:, u_other] *= f
            J[u_other, u_other] /= f
            J /= J.sum()
        pi = J.sum(axis=1)
        indep = np.outer(pi, pi)
        mask = J > 0
        mi_ref = float((J[mask] * np.log(J[mask] / indep[mask])).sum())
        if unigram_only:  # same units and marginals, no sequential structure
            J = np.outer(pi, pi)
            J[u_b, u_b] = 0.0
            J /= J.sum()
            pi = J.sum(axis=1)
        # The OTHER unit (all rarer units pooled) emits uniformly and is never re-estimated.
        # Otherwise it becomes a free wildcard state, and references with heavy tails win
        # model comparison for the wrong reason.
        uniform = np.zeros(S)
        uniform[:s_b] = 1.0 / s_b

        def init(r):
            if r == 0:  # frequency-informed start: unit rank k prefers sign rank k
                rs = np.log1p(np.arange(S - 1))
                ru = np.log1p(np.argsort(np.argsort(-pi[:K - 2])))
                E0 = np.exp(-np.abs(ru[:, None] - rs[None, :]) / 0.3) + 1e-3
                E0 = np.vstack([E0, np.ones((2, S - 1))])
            else:
                E0 = rng.dirichlet(np.ones(S - 1), size=K)
            E0 = E0 / E0.sum(axis=1, keepdims=True)
            return np.concatenate([E0, np.zeros((K, 1))], axis=1)

        best = None
        nz = B > 0
        for r in range(restarts):
            E = init(r)
            E[u_other] = uniform
            E[u_b] = 0.0
            E[u_b, s_b] = 1.0
            ll = -np.inf
            for it in range(iterations):
                M = E.T @ J @ E
                R = np.zeros_like(B)
                R[nz] = B[nz] / np.maximum(M[nz], 1e-300)
                C = E * ((J @ E) @ R.T) + E * ((J.T @ E) @ R)
                C[:, s_b] = 0.0
                rows = C.sum(axis=1, keepdims=True)
                E = np.where(rows > 0, C / np.maximum(rows, 1e-300), E)
                E[u_other] = uniform
                E[u_b] = 0.0
                E[u_b, s_b] = 1.0
                new_ll = float((B[nz] * np.log(np.maximum(M[nz], 1e-300))).sum())
                if it >= 15 and new_ll - ll < 1e-5 * abs(new_ll):
                    ll = new_ll
                    break
                ll = new_ll
            if best is None or ll > best[0]:
                best = (ll, E.copy())
        ll, E = best
        post = pi[:, None] * E                          # P(unit, sign)
        vals: dict[int, str] = {}
        for s, i in sidx.items():
            k = int(np.argmax(post[: len(units) + 1, i]))
            if k < len(units):
                vals[s] = units[k]
        return ll / max(B.sum(), 1), vals, mi_ref

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        if not knowledge or not knowledge.references:
            return Prediction(self.name)
        rng = np.random.default_rng(self.seed)
        refs = knowledge.references
        scores: dict[str, float] = {}
        if len(refs) > 1:
            # Model selection with short runs (frequency-informed start only), full fit on the winner.
            for ref in refs:
                lb, _, mi = self._fit(corpus, ref, rng, 1, 25)
                lu = self._fit(corpus, ref, rng, 1, 25, unigram_only=True)[0]
                scores[ref.name] = (lb - lu) / max(mi, 1e-9)
            ref = max(refs, key=lambda r: scores[r.name])
        else:
            ref = refs[0]
        ll, vals, _ = self._fit(corpus, ref, rng, self.restarts, self.iterations)
        scores.setdefault(ref.name, ll)
        return Prediction(self.name, features={"em_ll_per_bigram": ll}, sign_values=_translate(vals, ref),
                          family=ref.family, family_scores=scores, extra={"reference": ref.name})


class LuoLite(Method):
    name = "luo2019_lite"
    tasks = ("C", "D")
    needs_knowledge = True
    paper = ("Luo, J., Cao, Y., Barzilay, R. (2019). Neural decipherment via minimum-cost flow: from Ugaritic "
             "to Linear B. Proc. ACL 2019. Predecessor: Snyder, B., Barzilay, R., Knight, K. (2010). "
             "A statistical model for lost language decipherment. Proc. ACL 2010.")
    deviations = ("NOT NEURAL. Keeps Luo et al.'s alternation between (i) a character mapping model and (ii) a "
                  "one-to-one lost-word/known-word matching solved as an assignment problem (the min-cost-flow "
                  "step). Replaces their character-level LSTM sequence-to-sequence model with a categorical "
                  "P(unit|sign) table and compares only equal-length words. So it cannot learn context-dependent "
                  "sound changes. Lost-language words come from branching-entropy segmentation, because Indus has "
                  "no agreed word divider. Treat results as a lower bound on what the full neural model might do.")

    def __init__(self, iterations: int = 6, n_lost: int = 400, n_known: int = 1500, keep_frac: float = 0.5):
        self.iterations, self.n_lost, self.n_known, self.keep_frac = iterations, n_lost, n_known, keep_frac

    def _fit(self, lost: list[tuple[tuple[int, ...], int]], sc: Counter, ref: Reference):
        known = sorted(ref.words.items(), key=lambda kv: -kv[1])[: self.n_known]
        uc = Counter(u for t in ref.texts for u in t)
        signs = sorted({s for w, _ in lost for s in w})
        units = sorted({u for w, _ in known for u in w})
        if not signs or not units:
            return -1e9, {}
        si = {s: i for i, s in enumerate(signs)}
        ui = {u: i for i, u in enumerate(units)}
        # rank-frequency prior
        s_rank = {s: r for r, (s, _) in enumerate(sc.most_common())}
        rs = np.array([np.log(1 + s_rank.get(s, len(s_rank))) for s in signs])
        u_rank = {u: r for r, (u, _) in enumerate(uc.most_common())}
        ru = np.array([np.log(1 + u_rank.get(u, len(u_rank))) for u in units])
        prior = np.exp(-np.abs(rs[:, None] - ru[None, :]) / 0.5)
        prior /= prior.sum(axis=1, keepdims=True)
        P = prior.copy()

        lost_by_len: dict[int, list[int]] = {}
        known_by_len: dict[int, list[int]] = {}
        for i, (w, _) in enumerate(lost):
            lost_by_len.setdefault(len(w), []).append(i)
        for j, (w, _) in enumerate(known):
            known_by_len.setdefault(len(w), []).append(j)
        lf = np.log(np.array([c for _, c in lost], dtype=float))
        kf = np.log(np.array([c for _, c in known], dtype=float))
        lf -= lf.mean()
        kf -= kf.mean()

        score_val = -1e9
        for _ in range(self.iterations):
            logP = np.log(np.maximum(P, 1e-12))
            W = np.full((len(lost), len(known)), -1e6)
            for L, li in lost_by_len.items():
                kj = known_by_len.get(L)
                if not kj:
                    continue
                Ls = np.array([[si[s] for s in lost[i][0]] for i in li])
                Ku = np.array([[ui[u] for u in known[j][0]] for j in kj])
                sc_ = np.zeros((len(li), len(kj)))
                for p in range(L):
                    sc_ += logP[Ls[:, p][:, None], Ku[:, p][None, :]]
                sc_ = sc_ / L - 0.3 * np.abs(lf[li][:, None] - kf[kj][None, :])
                W[np.ix_(li, kj)] = sc_
            r, c = linear_sum_assignment(-W)
            ok = W[r, c] > -1e5
            r, c = r[ok], c[ok]
            if len(r) == 0:
                break
            order = np.argsort(-W[r, c])
            keep = order[: max(1, int(len(order) * self.keep_frac))]
            score_val = float(W[r[keep], c[keep]].mean())
            counts = np.zeros_like(P)
            for a, b in zip(r[keep], c[keep]):
                wt = lost[a][1]
                for s, u in zip(lost[a][0], known[b][0]):
                    counts[si[s], ui[u]] += wt
            P = (counts + 2.0 * prior)
            P /= P.sum(axis=1, keepdims=True)
        vals = {s: units[int(np.argmax(P[si[s]]))] for s in signs}
        return score_val, vals

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        if not knowledge or not knowledge.references:
            return Prediction(self.name)
        from .structural import branching_entropy_segment
        texts = [t.tolist() for t in corpus.logical()]
        seg = branching_entropy_segment(texts)
        words: Counter = Counter()
        for t, st in zip(texts, seg):
            bounds = st + [len(t)]
            for a, b in zip(bounds, bounds[1:]):
                if b > a:
                    words[tuple(t[a:b])] += 1
        lost = words.most_common(self.n_lost)
        sc = Counter(s for t in texts for s in t)
        fits = [(ref, *self._fit(lost, sc, ref)) for ref in knowledge.references]
        ref, score, vals = max(fits, key=lambda x: x[1])
        return Prediction(self.name, features={"luo_match_score": score}, sign_values=_translate(vals, ref),
                          family=ref.family, family_scores={r.name: s for r, s, _ in fits},
                          extra={"reference": ref.name})
