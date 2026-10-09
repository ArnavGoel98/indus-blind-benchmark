"""v2 Ugaritic anchor: many-to-one scoring and the EUPT line parser (no raw data needed)."""
from collections import Counter

import numpy as np

from ibdb.corpus import AnswerKey
from ibdb.data import ugaritic as U
from ibdb.scoring import score_sign_values


def _key(letters_by_text):
    sid = {l: i + 1 for i, l in enumerate(sorted({x for t in letters_by_text for x in t}))}
    key = AnswerKey("t", "ugaritic", "semitic", "language", True, "alphabetic",
                    {sid[l]: [U.GOLD[l]] for l in sid}, [[U.GOLD[x] for x in t] for t in letters_by_text],
                    [[0] for _ in letters_by_text])
    logical = [[sid[x] for x in t] for t in letters_by_text]
    return sid, key, logical


def test_many_to_one_counts_both_letters_correct():
    texts = [["ḫ", "ḥ", "b"], ["ṯ", "š", "ḥ"]]
    sid, key, logical = _key(texts)
    pred = {sid["ḫ"]: "ח", sid["ḥ"]: "ח", sid["ṯ"]: "ש", sid["š"]: "ש", sid["b"]: "ב"}
    s = score_sign_values(pred, key, logical)
    assert s["token_acc"] == 1.0 and s["type_acc"] == 1.0


def test_many_to_one_wrong_letter_still_wrong():
    sid, key, logical = _key([["ḫ", "ḥ"]])
    s = score_sign_values({sid["ḫ"]: "ח", sid["ḥ"]: "ה"}, key, logical)
    assert s["token_acc"] == 0.5


def test_gold_table_mergers():
    assert len(U.GOLD) - len(set(U.GOLD.values())) == 7
    assert {U.GOLD[x] for x in ("a", "i", "u")} == {"א"}


HTML = ('<div class="line"><span class="line-nr">i 9</span><span class="line-body">'
        '<span class="tei">[</span>a<span class="tei">]</span>ḫm<span class="scribal"> . </span>'
        '<span class="tei junicode">⸢</span>l<span class="tei junicode">⸣</span>h'
        '<span class="scribal"> x </span>b<span class="choice"><span class="corr">d</span>'
        '<span class="sic">(Text:b)</span></span><span class="del"><span class="tei">[[</span>p'
        '<span class="tei">]]</span></span>n</span></div>')


def test_parser_restorations_gaps_corrections():
    p = U._Line()
    p.feed(HTML)
    assert p.line_ids == ["i 9"]
    segs = [s for s in p.lines[0] if s is not U.GAP]
    # [a] dropped with a gap; damaged l kept; x is a gap; correction applied; erasure dropped, no gap
    assert ["".join(s) for s in segs] == ["ḫm.lh", "bdn"]


def test_recut_keeps_tokens_in_order():
    texts = [list("abcdefghij"), list("klmno")]
    out = U.recut(texts, 4.6, seed=0)
    assert [x for t in out for x in t] == [x for t in texts for x in t]
    assert Counter(len(t) for t in out)
    assert np.mean([len(t) for t in out]) < 10
