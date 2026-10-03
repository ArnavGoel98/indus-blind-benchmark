from collections import Counter

import numpy as np

from ibdb import ml
from ibdb.corpus import AnswerKey
from ibdb.scoring import score_sign_values, segmentation_f1, wilson
from ibdb.stats import check_targets, conditional_entropy, corpus_stats, coverage_count, zipf_mandelbrot_fit


def test_coverage_count():
    assert coverage_count(Counter({"a": 80, "b": 10, "c": 10})) == 1
    assert coverage_count(Counter({"a": 50, "b": 30, "c": 20})) == 2


def test_conditional_entropy_extremes():
    det = [[i % 10, (i + 1) % 10, (i + 2) % 10] for i in range(500)]
    h1, h2 = conditional_entropy(det)
    assert h2 < 1e-9 and h1 > 3
    rng = np.random.default_rng(0)
    iid = [list(rng.integers(0, 8, size=6)) for _ in range(5000)]
    h1, h2 = conditional_entropy(iid)
    assert abs(h1 - 3) < 0.05 and abs(h2 - 3) < 0.05


def test_zipf_mandelbrot_recovers_parameters():
    r = np.arange(1, 400)
    f = np.exp(12 - 1.5 * np.log(r + 5))
    fit = zipf_mandelbrot_fit(Counter({i: max(1, int(v)) for i, v in enumerate(f)}))
    assert abs(fit["b"] - 1.5) < 0.2


def test_check_targets_range_and_tolerance():
    res = check_targets({"sign_inventory": 450, "mean_length": 4.9},
                        {"sign_inventory": {"range": [400, 700]}, "mean_length": {"value": 4.4, "tolerance": 0.25}})
    assert res["sign_inventory"]["ok"] and not res["mean_length"]["ok"]


def test_corpus_stats_basic():
    s = corpus_stats([[1, 2, 3], [1, 2], [4]])
    assert s["n_texts"] == 3 and s["sign_inventory"] == 4 and s["max_length"] == 3


def _key():
    return AnswerKey("x", "latin", "indo-european", "language", True, "syllabic",
                     {1: ["ka"], 2: ["ta", "ra"], 3: ["<DIV>"]}, [["ka", "ta"], ["ra", "<DIV>"]], [[0], [0]])


def test_score_sign_values():
    k = _key()
    texts = [[1, 2], [2, 3]]
    perfect_type = score_sign_values({1: "ka", 2: "ta", 3: "<DIV>"}, k, texts)
    assert perfect_type["type_acc"] == 1.0
    assert perfect_type["token_acc"] == 0.75  # polyvalent sign 2 is wrong on its 'ra' token
    assert score_sign_values({}, k, texts)["token_acc"] == 0.0


def test_segmentation_f1():
    k = _key()
    k.word_starts = [[0, 2, 4], [0, 3]]
    assert segmentation_f1([[0, 2, 4], [0, 3]], k) == 1.0
    assert segmentation_f1([[0], [0]], k) == 0.0


def test_wilson_interval_contains_rate():
    lo, hi = wilson(30, 100)
    assert lo < 0.3 < hi and 0 <= lo and hi <= 1


def test_threshold_band_logreg():
    x = np.array([0.1, 0.2, 0.3, 0.8, 0.9, 1.0])
    y = np.array([0, 0, 0, 1, 1, 1], bool)
    c, d = ml.fit_threshold(x, y)
    assert ml.balanced_accuracy(y, ml.apply_threshold(x, c, d)) == 1.0
    xb = np.array([0.0, 0.1, 0.5, 0.55, 0.6, 0.95, 1.0])
    yb = np.array([0, 0, 1, 1, 1, 0, 0], bool)
    lo, hi, inside = ml.fit_band(xb, yb)
    assert ml.balanced_accuracy(yb, ml.apply_band(xb, lo, hi, inside)) == 1.0
    X = np.c_[x, -x]
    model = ml.fit_logreg(X, y)
    assert ((ml.predict_logreg(model, X) > 0.5) == y).all()
    sm = ml.fit_softmax(np.c_[x], ["a", "a", "a", "b", "b", "b"])
    assert ml.predict_softmax(sm, np.c_[x]) == ["a", "a", "a", "b", "b", "b"]
