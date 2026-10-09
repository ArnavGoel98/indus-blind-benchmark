import numpy as np

from ibdb.methods.allograph import AllographMerger, expand_values, merge_scores


def test_free_variants_are_merged_and_distinct_signs_kept():
    rng = np.random.default_rng(0)
    # Markov text over 30 signs; sign 0 is written as 0 or 100 at random (free variation).
    P = rng.dirichlet(np.full(30, 0.2), size=30)
    texts = []
    for _ in range(3000):
        x = int(rng.integers(30)); t = []
        for _ in range(6):
            t.append(100 if (x == 0 and rng.random() < 0.3) else x)
            x = int(rng.choice(30, p=P[x]))
        texts.append(t)
    rep = AllographMerger(seed=0).fit(texts)
    assert rep[100] == 0
    assert len({rep[s] for s in range(1, 30)}) == 29
    sc = merge_scores(rep, {0: [0, 100]}, {s: [str(s)] for s in range(30)} | {100: ["0"]})
    assert sc["recall"] == 1.0
    assert expand_values({0: "a"}, {0: 0, 100: 0}) == {0: "a", 100: "a"}
