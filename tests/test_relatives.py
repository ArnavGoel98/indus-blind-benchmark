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
