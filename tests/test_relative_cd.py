"""v2 Tasks C/D with a non-v1 relative: reference units and the entry-2 scorer (toy language only)."""
from ibdb import phonology
from ibdb import relative_cd as RC
from ibdb.corpus import AnswerKey
from ibdb.generator.build import _segments


def _toy_relative(source, regular=None, attested=None):
    words = _segments(source)["words"]
    clauses = [[tuple(words[i][1]) for i in range(j, j + 3)] for j in range(0, 60, 3)]
    reg = {"k": "g", "s": None} if regular is None else regular
    return RC.Relative("toyrel", "indo-european", clauses, reg, attested or {"k": {"g", "c"}})


def test_groups_match_v1_syllabify():
    v = phonology.LATIN.vowels
    for phon in (["p", "r", "o", "d", "u", "c", "e", "d"], ["a", "e", "t"], ["s", "t", "r"]):
        assert ["".join(g) for g in RC._groups(phon, v)] == phonology.syllabify(phon, v)


def test_reference_units_per_script_type(toy_source):
    rel = RC.Relative("r", "indo-european", [[("k", "a"), ("s", "e", "t")]] * 3, {})
    assert RC.reference(rel, "alphabetic", toy_source).texts[0] == ["k", "a", "s", "e", "t"]
    assert RC.reference(rel, "syllabic", toy_source).texts[0] == ["ka", "se", "t"]
    assert RC.reference(rel, "logographic", toy_source).texts[0] == ["ka", "set"]
    rel2 = RC.Relative("r", "indo-european", [[("k", "a"), ("s", "e", "t")], [("s", "e", "t")]], {})
    assert RC.reference(rel2, "logosyllabic", toy_source, logogram_vocab=1).texts[0] == ["ka", "set"]
    assert RC.reference(rel2, "logosyllabic", toy_source, logogram_vocab=0).texts[0] == ["ka", "se", "t"]
    assert RC.reference(rel, "alphabetic", toy_source).to_hidden == {}


def test_derivable_uses_attested_reflexes_in_order(toy_source):
    rel = _toy_relative(toy_source)
    assert RC._derivable("ga", ("k", "a"), rel)
    assert RC._derivable("ca", ("k", "a"), rel)
    assert RC._derivable("a", ("s", "a"), rel)          # s has no reflex
    assert not RC._derivable("ka", ("k", "a"), rel)     # k is never k in this relative
    assert not RC._derivable("ag", ("k", "a"), rel)


def test_strict_and_lenient_alphabetic_and_syllabic(toy_source):
    rel = _toy_relative(toy_source)
    g = RC.Gold(rel, toy_source, "alphabetic", set())
    assert g.strict("g", "k") and not g.strict("c", "k") and g.lenient("c", "k")
    assert not g.recoverable("s") and not g.strict(None, "s") and not g.lenient("", "s")
    assert g.strict("a", "a")
    assert not g.recoverable("<DET:0>") and not g.recoverable("<DIV>")
    assert g.strict("#1(disz)", "#1(disz)")                 # source units no sound law touches keep their value
    gs = RC.Gold(rel, toy_source, "syllabic", set())
    syl = next(s for s, ph in RC._hidden_lookup(toy_source)[1].items() if ph[0] == "k" and len(ph) == 2)
    reflex = "g" + syl[1:]
    assert gs.strict(reflex, syl) and gs.lenient("c" + syl[1:], syl) and not gs.strict(syl, syl)


def test_logogram_needs_a_cognate_in_the_relative(toy_source):
    words = _segments(toy_source)["words"]
    rel = _toy_relative(toy_source, regular={})                     # identity map
    g = RC.Gold(rel, toy_source, "logographic", set())
    inside = words[0]
    outside = next(w for w in words[60:] if "".join(w[1]) not in g.vocab)
    assert g.strict("".join(inside[1]), inside[0])
    assert not g.recoverable(outside[0])
    assert not g.lenient("".join(outside[1]), outside[0])


def test_score_counts_every_token(toy_source):
    rel = _toy_relative(toy_source)
    g = RC.Gold(rel, toy_source, "alphabetic", set())
    key = AnswerKey("c", toy_source, "indo-european", "language", True, "alphabetic",
                    {1: ["k"], 2: ["a"], 3: ["s"]}, [["k", "a", "s", "a"]], [[0]])
    s = RC.score({1: "c", 2: "a", 3: "s"}, key, [[1, 2, 3, 2]], g)
    assert s == {"strict": 0.5, "lenient": 0.75, "recoverable": 0.75}


def test_align_and_greedy_for_reading_based_syllables():
    assert RC._align(["ur", "{d}", "nanna"], ["u", "r", "{d}", "n", "a", "n", "n", "a"]) == \
        [("u", "r"), ("{d}",), ("n", "a", "n", "n", "a")]
    assert RC._align(["ga", "x"], ["g", "a", "n"]) is None
    assert RC._greedy(("g", "a", "n", "u"), {"gan", "ga"}, 3) == ["gan", "u"]
    assert RC._greedy(("k", "a"), set(), 3) == ["k", "a"]
