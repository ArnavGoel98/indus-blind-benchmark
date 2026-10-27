"""Pre-registration entry 10: a no-source gold row is an unknown reflex, not a lost sound."""
from collections import Counter

from ibdb import relative_cd as RC
from ibdb import yardsticks as Y
from ibdb.data import dravidian as D
from ibdb.data import relatives as R
from ibdb.data.gold import NO_SOURCE, old_semantics


def _gold(regular, attested, st):
    rel = RC.Relative("toy", "x", [[("p", "a"), ("k", "a")]], regular, attested)
    g = RC.Gold.__new__(RC.Gold)
    g.rel, g.st, g.logograms, g._cache = rel, st, set(), {}
    g.forms = {"pa": ("p", "a"), "ka": ("k", "a")}
    g.syls = {"pa": ("p", "a"), "ka": ("k", "a")}
    g.vocab = {"pa", "ka", "a"}
    return g


def test_no_source_is_unrecoverable_in_every_script():
    reg = {"p": NO_SOURCE, "k": "k", "a": "a"}
    att = {"p": set(), "k": {"k"}, "a": {"a"}}
    for st in ("alphabetic", "syllabic", "logographic"):
        g = _gold(reg, att, st)
        v = "p" if st == "alphabetic" else "pa"
        assert not g.recoverable(v) and not g.strict("a", v) and not g.lenient("a", v), st
        assert g.recoverable("k" if st == "alphabetic" else "ka")


def test_old_semantics_drop_the_phoneme():
    reg = old_semantics({"p": NO_SOURCE, "k": "k", "a": "a"})
    g = _gold(reg, {"p": set(), "k": {"k"}, "a": {"a"}}, "syllabic")
    assert g.recoverable("pa") and g.strict("a", "pa")        # the behaviour entry 10 removes


def test_lenient_keeps_attested_reflexes_of_a_no_source_row():
    g = _gold({"p": NO_SOURCE, "a": "a", "k": "k"}, {"p": {"b"}, "a": {"a"}, "k": {"k"}}, "syllabic")
    assert not g.strict("ba", "pa") and g.lenient("ba", "pa")


def test_yardsticks_leave_out_words_with_unknown_units():
    hidden = [[("p", "a"), ("k", "a")], [("k", "a"), ("k", "a"), ("k", "a")]]
    sister = [[("k", "a")]]
    anchor = {"n_letters": 4, "n_word_tokens": 50, "n_word_pair_tokens": 10, "verbatim_6plus_lengths": [6]}
    y = Y.sister_yardsticks(hidden, sister, {"p": NO_SOURCE, "k": "k", "a": "a"}, anchor, n_draws=3, seed=0)
    assert y["cognate_types"] == 1.0                           # only "ka" is sampled, and it is shared


def test_classification():
    assert R.latin_italian_map()[0]["h"] is None               # lost: Grandgent 1907, §249
    reg = R.finnish_estonian_map()[0]
    assert reg["p"] == NO_SOURCE and reg["ä"] == NO_SOURCE and reg["a"] == "a"
    for lang in ("malayalam", "kannada"):
        reg = D.gold_map(lang)[0]
        assert all(reg[u] == NO_SOURCE for u in ("h", "s", "ṣ", "ḵ"))
        assert None not in reg.values()
    assert Counter(v == NO_SOURCE for v in R.finnish_estonian_map()[0].values())[False] == 13
