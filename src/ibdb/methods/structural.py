"""Methods 4-6: segmentation, script-type estimation, linguistic vs non-linguistic classifier."""

from __future__ import annotations

from collections import Counter, defaultdict

import numpy as np

from ..corpus import Corpus
from ..stats import conditional_entropy, entropy_from_counts, zipf_mandelbrot_fit
from .base import Knowledge, Method, Prediction
from .descriptive import FulsPositional, RaoEntropy, YadavMarkov


def branching_entropy_segment(texts: list[list[int]], order: int = 2, min_count: int = 3) -> list[list[int]]:
    """Word-start positions per text from forward + backward branching entropy peaks."""

    def table(seqs):
        nxt: dict[tuple, Counter] = defaultdict(Counter)
        for t in seqs:
            for n in range(1, order + 1):
                for i in range(len(t) - n):
                    nxt[tuple(t[i:i + n])][t[i + n]] += 1
        return {k: (entropy_from_counts(np.fromiter(v.values(), dtype=np.float64)), sum(v.values())) for k, v in nxt.items()}

    fwd = table(texts)
    bwd = table([t[::-1] for t in texts])

    def h(tab, ctx_full):
        for n in range(min(order, len(ctx_full)), 0, -1):
            e = tab.get(tuple(ctx_full[-n:]))
            if e is not None and e[1] >= min_count:
                return e[0]
        return 0.0

    starts_all = []
    for t in texts:
        L = len(t)
        starts = [0]
        if L > 1:
            hf = [h(fwd, t[:i + 1]) for i in range(L - 1)]                 # uncertainty after position i
            hb = [h(bwd, t[i + 1:][::-1]) for i in range(L - 1)]           # uncertainty before position i+1
            score = np.array(hf) + np.array(hb)
            for i in range(L - 1):
                left = score[i - 1] if i > 0 else -np.inf
                right = score[i + 1] if i + 1 < L - 1 else -np.inf
                if score[i] > left and score[i] >= right:
                    starts.append(i + 1)
        starts_all.append(starts)
    return starts_all


class BranchingSegmentation(Method):
    name = "segmentation_branching"
    tasks = ("B",)
    paper = ("Harris, Z. S. (1955). From phoneme to morpheme. Language 31(2):190-222; Tanaka-Ishii, K. (2005). "
             "Entropy as an indicator of context boundaries. IJCNLP 2005. Indus n-gram segmentation: "
             "Yadav et al. (2010), see yadav2010_markov.")
    deviations = ("Boundaries at local maxima of forward + backward branching entropy (orders 1-2, backoff "
                  "when a context is seen fewer than 3 times). Yadav et al. segmented with frequent n-grams "
                  "instead. Output feeds the Luo-style matcher and Task B (mean segment length).")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        texts = [t.tolist() for t in corpus.logical()]
        seg = branching_entropy_segment(texts)
        n_seg = sum(len(s) for s in seg)
        mean_seg = sum(len(t) for t in texts) / max(n_seg, 1)
        return Prediction(self.name, {"mean_segment_len": mean_seg},
                          script_features={"mean_segment_len": mean_seg}, segmentation=seg)


def chao1(counts: Counter) -> float:
    f1 = sum(1 for v in counts.values() if v == 1)
    f2 = sum(1 for v in counts.values() if v == 2)
    s = len(counts)
    return s + (f1 * f1 / (2 * f2) if f2 > 0 else f1 * (f1 - 1) / 2)


class InventoryRule(Method):
    name = "script_type_inventory_rule"
    tasks = ("B",)
    paper = ("Conventional sign-inventory rule of thumb for script typology (alphabets: tens of signs; "
             "syllabaries: under ~100-150; logo-syllabaries: hundreds; logographies: thousands), as invoked "
             "in Indus debates. Not tied to one verified source. Richness estimator: Chao, A. (1984). "
             "Nonparametric estimation of the number of classes in a population. Scand. J. Statistics 11:265-270.")
    deviations = ("Applied to the Chao1-estimated total inventory, not the raw observed count. Thresholds "
                  "fixed in advance at 60 / 150 / 1200 and never tuned on benchmark data.")
    thresholds = (60, 150, 1200)

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        counts = Counter(s for t in corpus.texts for s in t.tolist())
        est = chao1(counts)
        a, s, l = self.thresholds
        st = "alphabetic" if est < a else "syllabic" if est < s else "logosyllabic" if est < l else "logographic"
        return Prediction(self.name, {"inventory_obs": len(counts), "inventory_chao1": est}, script_type=st)


def script_feature_vector(corpus: Corpus) -> dict[str, float]:
    texts = [t.tolist() for t in corpus.logical()]
    counts = Counter(s for t in texts for s in t)
    zm = zipf_mandelbrot_fit(counts)
    n_tok = sum(counts.values())
    h1, h2 = conditional_entropy(texts, None)
    seg = BranchingSegmentation().analyze(corpus).features["mean_segment_len"]
    return {
        "log_chao1": float(np.log(chao1(counts) + 1)),
        "log_inventory": float(np.log(len(counts) + 1)),
        "hapax_frac": sum(1 for v in counts.values() if v == 1) / len(counts),
        "ttr": len(counts) / n_tok,
        "zm_b": zm["b"] if np.isfinite(zm["b"]) else 1.0,
        "h1_bits": h1,
        "cond_ratio_full": h2 / h1 if h1 > 0 else 0.0,
        "mean_segment_len": seg,
    }


class ScriptTypeLR(Method):
    name = "script_type_lr"
    tasks = ("B",)
    paper = ("Inventory-and-frequency script typology as a trained classifier; features as in the rule-based "
             "method plus Zipf-Mandelbrot slope (Yadav et al. 2010), entropy and segment length.")
    deviations = ("Multinomial logistic regression trained by the evaluator with leave-one-source-out "
                  "cross-validation, so the classifier never sees the source language of the test corpus.")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        f = script_feature_vector(corpus)
        return Prediction(self.name, f, script_features=f)


class LeeTree(Method):
    name = "lee2010_tree"
    tasks = ("A",)
    decision = "tree2"
    paper = ("Lee, R., Jonathan, P., Ziman, P. (2010). Pictish symbols revealed as a written language through "
             "application of Shannon entropy. Proc. R. Soc. A 466:2545-2560 [pages to verify]. Critique: "
             "Sproat, R. (2014). A statistical comparison of written language and nonlinguistic symbol systems. "
             "Language 90(2):457-481.")
    deviations = ("Ur = F2 / log2(Nd/Nu) and Cr = Nd/Nu + a*Sd/Td as in Lee et al. (F2: conditional entropy; "
                  "Nd, Nu: distinct di-grams and un-grams; Sd: di-grams seen once; Td: all di-grams). Lee et al. "
                  "chose thresholds and a on their reference corpora; we learn a 2-level tree (Ur cut, then Cr cut) "
                  "leave-one-source-out, a = 7.")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        texts = [t.tolist() for t in corpus.logical()]
        uni = Counter(s for t in texts for s in t)
        big = Counter((a, b) for t in texts for a, b in zip(t, t[1:]))
        _, f2 = conditional_entropy(texts, None)
        nd, nu = len(big), len(uni)
        sd = sum(1 for v in big.values() if v == 1)
        td = max(sum(big.values()), 1)
        ur = f2 / np.log2(nd / nu) if nd > nu else 0.0
        cr = nd / nu + 7.0 * sd / td
        return Prediction(self.name, {"lee_ur": float(ur), "lee_cr": float(cr)}, ling_score=float(ur),
                          extra={"vector": [float(ur), float(cr)]})


class MultiFeatureClassifier(Method):
    name = "ling_classifier_lr"
    tasks = ("A",)
    decision = "lr"
    paper = ("Feature-based linguistic vs non-linguistic classification in the spirit of Sproat (2014), "
             "combining the statistics of Rao et al. (2009), Yadav et al. (2010), Lee et al. (2010) and "
             "positional analysis.")
    deviations = ("Logistic regression on 10 corpus-level features, trained leave-one-source-out. "
                  "Sproat's (2014) warning applies: a classifier learns its training controls. "
                  "We therefore report false-positive rates per control family, including an adversarial "
                  "control built to imitate language entropy.")

    def analyze(self, corpus: Corpus, knowledge: Knowledge | None = None) -> Prediction:
        f = {}
        for m in (RaoEntropy(), YadavMarkov(), FulsPositional(), LeeTree()):
            f.update(m.analyze(corpus).features)
        sf = script_feature_vector(corpus)
        f.update({k: sf[k] for k in ("log_inventory", "hapax_frac", "zm_b", "mean_segment_len")})
        keys = ["rao_ratio", "block_slope", "markov_gain", "pos_specificity", "pos_asymmetry", "lee_ur",
                "lee_cr", "log_inventory", "hapax_frac", "zm_b", "mean_segment_len"]
        return Prediction(self.name, f, extra={"vector": [float(f[k]) for k in keys], "keys": keys})
