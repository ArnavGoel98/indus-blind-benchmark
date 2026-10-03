import numpy as np
import pytest

from ibdb.controls import CONTROLS
from ibdb.generator.build import Knobs, make_corpus
from ibdb.generator.sampler import draw_lengths
from ibdb.generator.script import ScriptSpec


@pytest.mark.parametrize("st", ["syllabic", "logographic", "logosyllabic", "alphabetic"])
def test_deterministic_given_seed(toy_source, st):
    spec = ScriptSpec(script_type=st, determinatives=(st == "logosyllabic"))
    a, ka, _ = make_corpus(toy_source, spec, 400, 4.4, 7, Knobs())
    b, kb, _ = make_corpus(toy_source, spec, 400, 4.4, 7, Knobs())
    assert [t.tolist() for t in a.texts] == [t.tolist() for t in b.texts]
    assert ka.token_values == kb.token_values
    c, _, _ = make_corpus(toy_source, spec, 400, 4.4, 8, Knobs())
    assert [t.tolist() for t in a.texts] != [t.tolist() for t in c.texts]


def test_key_is_consistent_with_corpus(toy_source):
    spec = ScriptSpec(script_type="syllabic", allograph_rate=0.5, homophony_rate=0.3, polyvalence_rate=0.2,
                      determinatives=True, word_divider=True)
    c, k, _ = make_corpus(toy_source, spec, 600, 5.0, 1, Knobs())
    for t, vals in zip(c.logical(), k.token_values):
        assert len(t) == len(vals)
        for s, v in zip(t.tolist(), vals):
            assert v in k.sign_values[s], "every token value must be one of its sign's values"
    assert any(v == "<DIV>" for vals in k.token_values for v in vals)
    assert any(v.startswith("<DET:") for vals in k.token_values for v in vals)
    assert any(len(v) > 1 for v in k.sign_values.values()), "polyvalent signs exist"


def test_allographs_increase_inventory(toy_source):
    base = ScriptSpec(script_type="syllabic", allograph_rate=0.0, homophony_rate=0, polyvalence_rate=0)
    allo = ScriptSpec(script_type="syllabic", allograph_rate=1.0, allograph_extra_mean=4, homophony_rate=0, polyvalence_rate=0)
    a, _, _ = make_corpus(toy_source, base, 800, 4.4, 2, Knobs(rho=0))
    b, _, _ = make_corpus(toy_source, allo, 800, 4.4, 2, Knobs(rho=0))
    inv = lambda c: len({s for t in c.texts for s in t.tolist()})  # noqa: E731
    assert inv(b) > 1.5 * inv(a)


def test_direction_reverses_physical_order(toy_source):
    r, kr, _ = make_corpus(toy_source, ScriptSpec(direction="rtl"), 50, 4.4, 3, Knobs())
    for phys, logical in zip(r.texts, r.logical()):
        assert phys.tolist() == logical.tolist()[::-1]


def test_length_distribution_matches_targets():
    L = draw_lengths(np.random.default_rng(0), 20000, 4.4)
    assert abs(L.mean() - 4.4) < 0.1
    assert np.median(L) == 4
    assert 13 <= L.max() <= 21


def test_lengths_hit_target_exactly(toy_source):
    c, _, info = make_corpus(toy_source, ScriptSpec(script_type="syllabic"), 1000, 4.4, 4, Knobs(rho=0))
    m = np.mean([len(t) for t in c.texts])
    assert abs(m - 4.4) < 0.25


@pytest.mark.parametrize("name", sorted(CONTROLS))
def test_controls_exact_length(name):
    ctrl = CONTROLS[name](0)
    rng = np.random.default_rng(0)
    for L in (1, 2, 5, 13):
        assert len(ctrl.make_text(rng, L)) == L


def test_rao_controls_are_extremes():
    from ibdb.stats import ratio_from_token_texts
    rng = np.random.default_rng(0)
    # Small alphabet: with ~420 signs and Indus-sized data the plug-in estimate of H(X2|X1) for an
    # i.i.d. source is badly biased downward (one reason entropy arguments need care).
    t1 = [CONTROLS["rao_type1"](0, V=20).make_text(rng, 6) for _ in range(3000)]
    t2 = [CONTROLS["rao_type2"](0, V=20).make_text(rng, 6) for _ in range(3000)]
    # full alphabet (no UNK merging): rigid successor = zero conditional entropy
    assert ratio_from_token_texts(t1, top_k=None) < 0.05
    assert ratio_from_token_texts(t2, top_k=None) > 0.9
