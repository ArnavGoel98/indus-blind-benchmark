"""Sensitivity sweep: the two controlled knobs are actually hit, and the answer key stays aligned."""

import pytest

from ibdb.generator.build import Knobs, make_corpus
from ibdb.generator.script import ScriptSpec
from ibdb.sensitivity import PoolExhausted, allograph_knobs, assemble


@pytest.mark.parametrize("dup", [0.0, 0.2, 0.45])
def test_assemble_hits_duplicate_rate_exactly(toy_source, dup):
    spec = ScriptSpec(script_type="syllabic", allograph_rate=0.6, allograph_extra_mean=3.0)
    pool, pkey, _ = make_corpus(toy_source, spec, 900, 4.6, 3, allograph_knobs(Knobs(), 1.5))
    c, k, info = assemble(pool, pkey, 300, 4.6, dup, 3, "t")
    texts = [tuple(t.tolist()) for t in c.logical()]
    assert len(texts) == 300
    assert 1 - len(set(texts)) / len(texts) == pytest.approx(round(dup * 300) / 300)
    for t, vals in zip(c.logical(), k.token_values):   # key rows follow the reordered texts
        assert len(t) == len(vals)
        for s, v in zip(t.tolist(), vals):
            assert v in k.sign_values[s]
    assert set(k.sign_values) == {s for t in texts for s in t}


def test_assemble_reports_exhaustion(toy_source):
    spec = ScriptSpec(script_type="syllabic", allograph_rate=0.0)
    pool, pkey, _ = make_corpus(toy_source, spec, 60, 4.6, 3, allograph_knobs(Knobs(), 0.0))
    with pytest.raises(PoolExhausted):
        assemble(pool, pkey, 600, 4.6, 0.0, 3, "t")


def test_allograph_scalar_is_monotone_in_expected_variants():
    k = Knobs()
    exp = [a.allograph_rate * a.allograph_extra_mean for a in (allograph_knobs(k, u) for u in (0, 0.5, 1, 2, 4))]
    assert exp == sorted(exp) and exp[0] == 0
    assert all(allograph_knobs(k, u).rho == 0 for u in (0, 2))
