import numpy as np

from ibdb.rao_kn import conditional_entropy_kn, mkn_bigram


def test_rows_are_distributions():
    rng = np.random.default_rng(0)
    seqs = [list(rng.integers(0, 30, size=8)) for _ in range(200)]
    p, P = mkn_bigram(seqs, 30)
    assert np.isclose(p.sum(), 1)
    assert np.allclose(P.sum(axis=1), 1)
    assert (P > 0).all()


def test_uniform_and_rigid_extremes():
    rng = np.random.default_rng(1)
    V = 417
    iid = [list(rng.integers(0, V, size=20)) for _ in range(10_000)]
    succ = rng.permutation(V)
    rigid = []
    for _ in range(10_000):
        x = int(rng.integers(V))
        line = [x]
        for _ in range(19):
            x = int(succ[x])
            line.append(x)
        rigid.append(line)
    assert conditional_entropy_kn(iid)["relative"] > 0.97
    assert conditional_entropy_kn(rigid)["relative"] < 0.05
