"""Knowledge tiers: what a decipherer is allowed to know (Judge fix #4).

related     one reference: a SYNTHETIC SISTER of the hidden language (regular sound changes +
            lexical replacement), written from the other half of the source text. This is the
            Ugaritic-Hebrew / Linear B-Greek situation and is NOT available for Indus.
candidates  the sister plus every other benchmark language. The solver must pick, which gives
            the Task C prediction. Models "the right family is among the hypotheses, but only a
            distant relative is attested".
none        every other benchmark language, with the hidden language and its sister removed.
            Models "the true family may not be among the hypotheses at all".

The INDUS-RELEVANT tiers are 'candidates' and 'none'. No close relative of the Harappan
language is agreed, and we do not know which of these two tiers applies.

Design choice that moves Task D results directly: the sister's distance (sound_change_rate,
lexical_replacement in config/experiment.yaml). It is reported next to every Task D number.
"""

from __future__ import annotations

import zlib
from collections import Counter
from functools import lru_cache

import numpy as np

from . import config, phonology
from .generator.build import LANGUAGES, _segments, source_family, split_clauses
from .methods.base import Knowledge, Reference

MAX_REF_CLAUSES = 40_000


def _profile(lang: str) -> phonology.Profile:
    return phonology.PROFILES[lang]


def sound_change_map(lang: str, rate: float, seed: int) -> dict[str, str]:
    """A bijective phoneme permutation touching ~rate of consonants and of vowels."""
    prof = _profile(lang)
    rng = np.random.default_rng([seed, zlib.crc32(lang.encode())])
    mapping: dict[str, str] = {}
    for cls in (sorted(prof.consonants), sorted(prof.vowels)):
        n = int(round(rate * len(cls)))
        if n < 2:
            continue
        chosen = list(rng.choice(cls, size=n, replace=False))
        shifted = chosen[1:] + chosen[:1]                  # cyclic derangement: bijective, no fixed points
        mapping.update(dict(zip(chosen, shifted)))
    return mapping


def _change_unit(u: str, lang: str, pmap: dict[str, str]) -> str:
    if u.startswith("{") or u.startswith("#") or u.startswith("<"):
        return u
    if lang == "tamil" and phonology.is_tamil_word(u):
        ph = phonology.tamil_phonemes(u)
    else:
        ph = phonology.greedy_graphemes(u, list(_profile(lang).vowels | _profile(lang).consonants))
    return "".join(pmap.get(p, p) for p in ph)


def _word_units(word: list, script_type: str, logo: bool) -> list[str]:
    form, phon, syl, _ = word
    if script_type == "alphabetic":
        return list(phon)
    if script_type == "syllabic":
        return list(syl)
    if script_type == "logographic":
        return [form]
    if script_type == "logosyllabic":
        return [form] if logo else list(syl)
    raise ValueError(script_type)


@lru_cache(maxsize=64)
def build_reference(lang: str, script_type: str, sister: bool, seed: int, logogram_vocab: int = 250,
                    sound_change_rate: float | None = None, lexical_replacement: float | None = None) -> Reference:
    sis_cfg = config.experiment()["sister_language"]
    rate = sis_cfg["sound_change_rate"] if sound_change_rate is None else sound_change_rate
    lex = sis_cfg["lexical_replacement"] if lexical_replacement is None else lexical_replacement
    d = _segments(lang)
    words, rank = d["words"], d["_rank"]
    clauses = split_clauses(lang, d, "reference")[:MAX_REF_CLAUSES]
    logo = rank <= logogram_vocab
    pmap = sound_change_map(lang, rate, seed) if sister else {}

    # Lexical replacement: a seeded share of word types is swapped for another word of the
    # same unit length (an unrelated word: no cognate exists for it).
    replace_with: dict[int, int] = {}
    if sister and lex > 0:
        rng = np.random.default_rng([seed, 99, zlib.crc32(lang.encode())])
        used = sorted({w for _, ids in clauses for w in ids})
        by_len: dict[int, list[int]] = {}
        for w in used:
            by_len.setdefault(len(_word_units(words[w], script_type, bool(logo[w]))), []).append(w)
        for w in used:
            if rng.random() < lex:
                pool = by_len[len(_word_units(words[w], script_type, bool(logo[w])))]
                replace_with[w] = pool[int(rng.integers(len(pool)))]

    texts: list[list[str]] = []
    wcount: Counter = Counter()
    to_hidden: dict[str, str] = {}
    for _, ids in clauses:
        seq: list[str] = []
        for w in ids:
            src = replace_with.get(w, w)
            units = _word_units(words[src], script_type, bool(logo[w]))
            if sister:
                new = [_change_unit(u, lang, pmap) for u in units]
                if src == w:  # cognate: remember the regular correspondence
                    for a, b in zip(new, units):
                        to_hidden.setdefault(a, b)
                else:  # replaced word: its sub-word units are still regular sound correspondences
                    if script_type in ("alphabetic", "syllabic"):
                        for a, b in zip(new, units):
                            to_hidden.setdefault(a, b)
                units = new
            if units:
                seq += units
                wcount[tuple(units)] += 1
        if seq:
            texts.append(seq)
    name = f"{lang}-sister" if sister else lang
    return Reference(name, source_family(lang), texts, dict(wcount), to_hidden if sister else {})


def knowledge_for(hidden_lang: str, script_type: str, tier: str, seed: int,
                  languages=LANGUAGES, logogram_vocab: int = 250, sound_change_rate: float | None = None,
                  lexical_replacement: float | None = None) -> Knowledge:
    others = [l for l in languages if l != hidden_lang]
    sister = lambda: build_reference(hidden_lang, script_type, True, seed, logogram_vocab,  # noqa: E731
                                     sound_change_rate, lexical_replacement)
    if tier == "related":
        refs = [sister()]
    elif tier == "candidates":
        refs = [sister()] + \
               [build_reference(l, script_type, False, seed, logogram_vocab) for l in others]
    elif tier == "none":
        refs = [build_reference(l, script_type, False, seed, logogram_vocab) for l in others]
    else:
        raise ValueError(tier)
    return Knowledge(tier=tier, script_type=script_type, references=refs)
