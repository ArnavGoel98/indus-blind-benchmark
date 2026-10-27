"""Pre-registration entry 11: the relative's own vowel letters in the syllable cutter; the reachable ceiling."""
import dataclasses
import os
from types import SimpleNamespace

import pytest

os.environ.setdefault("IBDB_SISTER_VERSION", "v2")

from ibdb import relative_cd as RC  # noqa: E402
from ibdb.data import dravidian as D  # noqa: E402
from ibdb.data import relatives as R  # noqa: E402

ADDED = {("finnish", "estonian"): {"õ", "ü"}, ("tamil", "malayalam"): {"ṛ"}, ("tamil", "kannada"): {"ṛ"},
         ("latin", "italian"): set()}


def _old(rel):
    """The relative as the frozen-v2 cutter saw it: the hidden language's vowels only."""
    return dataclasses.replace(rel, vowels=frozenset())


def test_added_vowels_are_exactly_the_declared_ones():
    for (h, r), added in ADDED.items():
        assert set(RC.real_relative(h, r).vowels - RC._vowels(h)) == added, (h, r)
    assert R.ITALIAN_VOWELS <= RC._vowels("latin")
    assert D.vowel_letters("malayalam") == D.vowel_letters("kannada")


def test_toy_word_is_cut_with_the_relatives_vowels():
    rel = RC.Relative("toy", "x", [[("s", "õ", "n", "a")]], {}, {}, frozenset("õ"))
    assert RC.reference(_old(rel), "syllabic", "finnish").texts == [["s", "õ", "na"]]
    assert RC.reference(rel, "syllabic", "finnish").texts == [["sõ", "na"]]


@pytest.mark.parametrize("pair", [("finnish", "estonian"), ("tamil", "malayalam"), ("tamil", "kannada")])
def test_added_vowels_end_their_syllable(pair):
    h, r = pair
    rel = RC.real_relative(h, r)
    vowels = RC._vowels(h) | rel.vowels
    for st in ("syllabic", "logosyllabic"):
        for t in RC.reference(rel, st, h, 250).texts:
            for u in t:
                for v in ADDED[pair]:
                    if v in u and st == "syllabic":
                        assert u.endswith(v), (st, u)      # a CV unit closes at its vowel
    # entry 11, D.2: units still join to the word; a word cut differently contains an added vowel
    changed = 0
    for c in rel.clauses[:2000]:
        for w in c:
            new = RC._groups(w, vowels)
            old = RC._groups(w, RC._vowels(h))
            assert "".join("".join(g) for g in new) == "".join(w)
            if new != old:
                changed += 1
                assert set(w) & ADDED[pair], w
    assert changed > 0


@pytest.mark.parametrize("pair", list(ADDED))
def test_unchanged_references(pair):
    h, r = pair
    rel = RC.real_relative(h, r)
    for st in ("alphabetic", "logographic") + (("syllabic", "logosyllabic") if not ADDED[pair] else ()):
        assert RC.reference(rel, st, h, 250).texts == RC.reference(_old(rel), st, h, 250).texts, (pair, st)


def test_sisters_have_no_own_vowels():
    assert RC.Relative("s", "x", [], {}).vowels == frozenset()


def test_reachable_counts_only_the_solvers_units():
    ref = SimpleNamespace(texts=[["a", "a", "a", "b", "b", "c"]])
    key = SimpleNamespace(token_values=[["x", "y", "z", "z"]])
    gold = SimpleNamespace(_value=lambda v: ({"x": "a", "y": "b", "z": "c"}[v], None, False))
    assert RC.reachable(ref, key, gold, 2) == 0.5          # c is outside the top 2 units
    assert RC.reachable(ref, key, gold, 3) == 1.0
