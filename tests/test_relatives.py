"""Rank 6b: spelling normalisation and gold-table checks (no raw data needed)."""
from ibdb import phonology
from ibdb.data import relatives as R


def test_italian_normalised_drops_h_and_splits_apostrophes():
    assert R.italian_words("ch’i’ v’ho", "normalised") == [("c",), ("i",), ("v",), ("o",)]
    assert R.italian_words("chiave", "normalised") == [("c", "i", "a", "v", "e")]
    assert R.italian_words("ghiaccio", "normalised") == [("g", "i", "a", "c", "c", "i", "o")]


def test_italian_as_written_keeps_h_and_strips_accents():
    assert R.italian_words("chiave", "as_written") == [("ch", "i", "a", "v", "e")]
    assert R.italian_words("Più così", "as_written") == [("p", "i", "u"), ("c", "o", "s", "i")]
    assert R.italian_words("quella", "as_written") == [("qu", "e", "l", "l", "a")]


def test_gold_covers_every_latin_unit_and_cites_a_section():
    inv = phonology.PROFILES["latin"].consonants | phonology.PROFILES["latin"].vowels
    assert set(R.LATIN_ITALIAN) == inv
    assert all(v[2].startswith("§") for v in R.LATIN_ITALIAN.values())
    reg, att = R.latin_italian_map()
    assert reg["h"] is None and att["h"] == set()
    assert reg["ph"] == "f" and "p" in att["ph"]
    assert all(r is None or r in att[k] for k, r in reg.items())


def test_relationship_labels():
    assert R.RELATIONSHIP[("latin", "italian")] == "descendant"
    assert R.RELATIONSHIP[("finnish", "estonian")] == "sister"


# ---------------------------------------------------------------- Dravidian (rank 6b)
from collections import Counter  # noqa: E402

from ibdb.data import dravidian as D
from ibdb.data.gold import NO_SOURCE  # noqa: E402


def test_malayalam_script_converter():
    assert D.script_phonemes("മലയാളം", "malayalam") == ["m", "a", "l", "a", "y", "ā", "ḷ", "a", "m"]
    assert D.script_phonemes("കണ്ണ്", "malayalam") == ["k", "a", "ṇ", "ṇ"]
    assert D.script_phonemes("അവൻ", "malayalam") == ["a", "v", "a", "n"]
    assert D.script_phonemes("സംഗീതം", "malayalam", "as_written") == ["s", "a", "ṅ", "g", "ī", "t", "a", "m"]
    assert D.script_phonemes("സംഗീതം", "malayalam") == ["s", "a", "ṅ", "k", "ī", "t", "a", "m"]


def test_kannada_script_converter():
    assert D.script_phonemes("ಕನ್ನಡ", "kannada", "as_written") == ["k", "a", "n", "n", "a", "ḍ", "a"]
    assert D.script_phonemes("ಕನ್ನಡ", "kannada") == ["k", "a", "n", "n", "a", "ṭ", "a"]
    assert D.script_phonemes("ಹತ್ತು", "kannada") == ["h", "a", "t", "t", "u"]
    assert D.script_phonemes("ಗಂಗೆ", "kannada") == ["k", "a", "ṅ", "k", "e"]


def test_dravidian_gold_tables():
    tamil_units = set(phonology.PROFILES["tamil"].consonants | phonology.PROFILES["tamil"].vowels) | {"ḵ"}
    for lang in ("malayalam", "kannada"):
        g = D.GOLD[lang]
        assert tamil_units <= set(g), tamil_units - set(g)
        reg, att = D.gold_map(lang)
        assert all(r is None or r == NO_SOURCE or r in att[k] for k, r in reg.items())
        assert all(v[2] for v in g.values())
        assert D.RELATIONSHIP[lang] in ("sister", "descendant")
    assert D.GOLD["malayalam"]["ṉ"][0] == "n" and D.GOLD["kannada"]["ḻ"][0] == "ḷ"


def test_normalisation_only_collapses_voicing_and_aspiration():
    assert set(D.NORMALISE.values()) <= {"k", "c", "ṭ", "t", "p"}
    c = Counter(D.NORMALISE.values())
    assert c["t"] == 3 and c["ṭ"] == 3 and c["k"] == 3 and c["c"] == 3 and c["p"] == 3
