"""Methods 1-3: entropy (Rao), n-gram Markov (Yadav), positional histograms (Fuls)."""

from __future__ import annotations

from collections import Counter

import numpy as np

from ..corpus import Corpus
from ..stats import conditional_entropy, coverage_count, entropy_from_counts
from .base import Knowledge, Method, Prediction


class RaoEntropy(Method):
    name = "rao2009_entropy"
    tasks = ("A",)
    decision = "band"
    paper = ("Rao, R. P. N., Yadav, N., Vahia, M. N., Joglekar, H., Adhikari, R., Mahadevan, I. (2009). "
             "Entropic evidence for linguistic structure in the Indus script. Science 324(5931):1165. "
             "Block entropy: Rao, R. P. N. (2010). Probabilistic analysis of an ancient undeciphered script. "
             "IEEE Computer 43(4):76-80 [volume/pages to verify].")
    deviations = ("Rao plots conditional entropy against the number of most frequent tokens and compares it "
                  "visually with known scripts and with Type 1 / Type 2 controls. We reduce the curve to one "
                  "number, the ratio H(X2|X1)/H(X1) at k = min(100, inventory) most frequent signs (rarer signs "
                  "merged), plus the slope of normalized block entropy H_N / (N log2 k) for N = 1..4. The decision "
                  "threshold is learned (leave-one-source-out), not read off a plot.")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        texts = [t.tolist() for t in corpus.logical()]
        inv = len({s for t in texts for s in t})
        k = min(100, inv)
        h1, h2 = conditional_entropy(texts, k)
        ratio = h2 / h1 if h1 > 0 else 0.0
        # block entropies over top-k alphabet
        keep = {s for s, _ in Counter(s for t in texts for s in t).most_common(k)}
        tt = [[s if s in keep else -1 for s in t] for t in texts]
        hn = []
        for n in range(1, 5):
            c = Counter(tuple(t[i:i + n]) for t in tt for i in range(len(t) - n + 1))
            if sum(c.values()) < 50:
                break
            hn.append(entropy_from_counts(np.fromiter(c.values(), dtype=np.float64)) / (n * np.log2(k + 1)))
        slope = float(np.polyfit(np.arange(1, len(hn) + 1), hn, 1)[0]) if len(hn) >= 2 else 0.0
        # Rao's claim is that language sits BETWEEN rigid and random systems, so the evaluator
        # learns an interval (decision = "band") on this score rather than a one-sided cut.
        return Prediction(self.name, {"rao_h1": h1, "rao_h2": h2, "rao_ratio": ratio, "block_slope": slope},
                          ling_score=ratio)


class YadavMarkov(Method):
    name = "yadav2010_markov"
    tasks = ("A",)
    paper = ("Yadav, N., Joglekar, H., Rao, R. P. N., Vahia, M. N., Adhikari, R., Mahadevan, I. (2010). "
             "Statistical analysis of the Indus script using n-grams. PLoS ONE. arXiv:0901.3017.")
    deviations = ("Yadav et al. fit a smoothed bigram model and use it for syntax analysis, missing-sign "
                  "restoration and segmentation. We keep the model (interpolated Witten-Bell bigram, 5-fold "
                  "cross-validated) and use the relative cross-entropy gain of bigram over unigram as a "
                  "language-likeness statistic. They did not propose this as a language test.")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        texts = [[-2] + t.tolist() + [-3] for t in corpus.logical()]
        n = len(texts)
        folds = np.arange(n) % 5
        rng = np.random.default_rng(0)
        rng.shuffle(folds)
        h_uni_tot = h_bi_tot = 0.0
        n_tok = 0
        for f in range(5):
            train = [t for t, ff in zip(texts, folds) if ff != f]
            test = [t for t, ff in zip(texts, folds) if ff == f]
            uni = Counter(s for t in train for s in t[1:])
            big = Counter((a, b) for t in train for a, b in zip(t, t[1:]))
            ctx = Counter()
            types_after = Counter()
            for (a, _), v in big.items():
                ctx[a] += v
                types_after[a] += 1
            V = len(uni) + 1
            N = sum(uni.values())
            for t in test:
                for a, b in zip(t, t[1:]):
                    pu = (uni.get(b, 0) + 1) / (N + V)
                    c, T = ctx.get(a, 0), types_after.get(a, 0)
                    if c > 0:
                        lam = c / (c + T)
                        pb = lam * big.get((a, b), 0) / c + (1 - lam) * pu
                    else:
                        pb = pu
                    h_uni_tot -= np.log2(pu)
                    h_bi_tot -= np.log2(pb)
                    n_tok += 1
        hu, hb = h_uni_tot / n_tok, h_bi_tot / n_tok
        gain = (hu - hb) / hu if hu > 0 else 0.0
        return Prediction(self.name, {"markov_h_uni": hu, "markov_h_bi": hb, "markov_gain": gain}, ling_score=gain)


class FulsPositional(Method):
    name = "fuls_positional"
    tasks = ("A",)
    paper = ("Positional sign analysis in the tradition of A. Fuls' studies of the Indus corpus (ICIT) and "
             "Mahadevan (1977) positional tables. EXACT FULS REFERENCE NOT VERIFIED by us; the maintainer "
             "should add it before publication.")
    deviations = ("Per-sign histograms over {solo, initial, medial, final}. Summaries: token-weighted "
                  "positional specificity 1 - H(position|sign)/H(position), and the log ratio of the number "
                  "of signs covering 80% of text beginnings to the number covering 80% of endings (the "
                  "asymmetry Yadav et al. 2010 report for Indus).")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        texts = [t.tolist() for t in corpus.logical()]
        pos_counts: dict[int, np.ndarray] = {}
        for t in texts:
            L = len(t)
            for i, s in enumerate(t):
                p = 0 if L == 1 else (1 if i == 0 else (3 if i == L - 1 else 2))
                pos_counts.setdefault(s, np.zeros(4))[p] += 1
        M = np.array(list(pos_counts.values()))
        tot = M.sum()
        h_pos = entropy_from_counts(M.sum(axis=0))
        h_cond = sum(row.sum() / tot * entropy_from_counts(row) for row in M)
        spec = 1 - h_cond / h_pos if h_pos > 0 else 0.0
        b80 = coverage_count(Counter(t[0] for t in texts if len(t) > 1))
        e80 = coverage_count(Counter(t[-1] for t in texts if len(t) > 1))
        asym = float(np.log((b80 + 1) / (e80 + 1)))
        return Prediction(self.name, {"pos_specificity": spec, "pos_asymmetry": asym}, ling_score=spec)
