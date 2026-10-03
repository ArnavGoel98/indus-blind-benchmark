from ibdb import phonology


def test_syllabify_cv_and_dead_consonants():
    ph = phonology.SANSKRIT.phonemes("indra")
    assert ph == ["i", "n", "d", "r", "a"]
    assert phonology.syllabify(ph, phonology.SANSKRIT.vowels) == ["i", "n", "d", "ra"]


def test_sanskrit_aspirates_are_single_phonemes():
    assert phonology.SANSKRIT.phonemes("bhārata") == ["bh", "ā", "r", "a", "t", "a"]


def test_tamil_transliteration():
    # தமிழ் = ta-mi-ḻ
    assert phonology.tamil_phonemes("தமிழ்") == ["t", "a", "m", "i", "ḻ"]
    assert phonology.tamil_phonemes("கை") == ["k", "ai"]


def test_sumerian_word_with_determinative():
    readings, syl, det = phonology.sumerian_word("{d}en-lil2")
    assert readings == ["{d}", "en", "lil2"]
    assert syl == ["{d}", "en", "lil"]
    assert det == "d"
    assert phonology.sumerian_word("x-ba") is None
