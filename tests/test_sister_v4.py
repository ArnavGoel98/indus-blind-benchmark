"""Sister-v4 mechanism tests (v2 rank 6). Need the prepared language segments (data/segments)."""
import pytest

from ibdb import phonology
from ibdb.paths import segments_dir

pytestmark = pytest.mark.skipif(not (segments_dir() / "latin.json.gz").exists(), reason="segments not prepared")

LANGS = ("sanskrit", "tamil", "sumerian", "latin", "finnish")


def _sv4():
    from ibdb import sister_v4 as S
    return S


@pytest.mark.parametrize("lang", LANGS)
def test_merger_count_and_disjoint(lang):
    S = _sv4()
    s = S.build(lang, 90, S.Knobs())
    n = int(round(S.MERGER_SHARE * len(phonology.PROFILES[lang].consonants)))
    assert len(s.mergers) == n
    assert not set(s.mergers) & set(s.mergers.values())
    for src, tgt in s.mergers.items():                 # merged pair shares one regular reflex
        assert s.regular[src] == s.regular[tgt]


def test_conditioned_rules_give_two_reflexes():
    S = _sv4()
    s = S.build("latin", 90, S.Knobs(n_cond=4))
    assert len(s.rules) == 4
    for X, Y, ctx, _ in s.rules:
        assert Y != s.regular[X]
        assert {s.regular[X], Y} <= set(s.attested[X])


def test_affix_replacement_is_consistent():
    S = _sv4()
    s = S.build("latin", 90, S.Knobs(affix_share=1.0, lexical=0.0))
    d, clauses, phon = S._source("latin")
    suf = s.affixes["suffix"]
    assert suf
    seen = 0
    for (_, ids), out in zip(clauses, s.clauses):
        for w, o in zip(ids, out):
            t = phon[w]
            k = next((k for k in (3, 2, 1) if len(t) > k + 1 and t[-k:] in suf), 0)
            if k:
                assert o[-k:] == suf[t[-k:]]
                seen += 1
    assert seen > 100


@pytest.mark.parametrize("share", [0.0, 0.5, 1.0])
def test_word_order_share(share):
    S = _sv4()
    a = S.build("finnish", 90, S.Knobs(lexical=0.0))
    b = S.build("finnish", 90, S.Knobs(lexical=0.0, word_order=share))
    multi = [(x, y) for x, y in zip(a.clauses, b.clauses) if len(x) > 1 and len(set(x)) > 1]
    changed = sum(x != y for x, y in multi) / len(multi)
    assert abs(changed - share) < 0.05


def test_same_seed_same_sister():
    S = _sv4()
    k = S.Knobs(n_cond=6, affix_share=0.5, lexical=0.35, word_order=0.5, final_vowel_loss=0.3)
    a, b = S.build("tamil", 91, k), S.build("tamil", 91, k)
    assert a.clauses == b.clauses and a.regular == b.regular and a.rules == b.rules
    c = S.build("tamil", 90, k)
    assert c.clauses != a.clauses
