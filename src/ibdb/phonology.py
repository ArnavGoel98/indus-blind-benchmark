"""Turn transliterated words into phoneme and syllable sequences.

Each language profile maps a normalized word form to a list of phonemes. A generic
syllabifier then groups phonemes into script units:

* ``CV``: zero or more consonants before a vowel are split so that only the LAST consonant
  joins the vowel. Earlier consonants become stand-alone ``C`` units, like a "dead consonant"
  (virama) sign. This keeps syllabaries near the size of attested ones (Linear B, Brahmi-type
  akṣaras with conjuncts decomposed).
* ``V``: a vowel with no onset.
* ``C``: a coda or pre-consonantal consonant.

Sumerian is special: CDLI transliteration already gives one reading per cuneiform sign, so its
"syllables" are the sign readings with homophone indices stripped.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def greedy_graphemes(word: str, inventory: list[str]) -> list[str]:
    """Longest-match tokenization. Characters not in the inventory are dropped."""
    inv = sorted(inventory, key=len, reverse=True)
    out: list[str] = []
    i = 0
    while i < len(word):
        for g in inv:
            if word.startswith(g, i):
                out.append(g)
                i += len(g)
                break
        else:
            i += 1
    return out


@dataclass(frozen=True)
class Profile:
    name: str
    vowels: frozenset[str]
    consonants: frozenset[str]

    def phonemes(self, word: str) -> list[str]:
        return greedy_graphemes(word, list(self.vowels | self.consonants))


SANSKRIT = Profile(
    "sanskrit",
    frozenset(["ai", "au", "ā", "ī", "ū", "ṛ", "ṝ", "ḷ", "ḹ", "a", "i", "u", "e", "o"]),
    frozenset(
        ["kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh", "k", "g", "ṅ", "c", "j",
         "ñ", "ṭ", "ḍ", "ṇ", "t", "d", "n", "p", "b", "m", "y", "r", "l", "v", "ś", "ṣ", "s",
         "h", "ṃ", "ḥ"]
    ),
)

TAMIL = Profile(
    "tamil",
    frozenset(["ai", "au", "ā", "ī", "ū", "ē", "ō", "a", "i", "u", "e", "o"]),
    frozenset(["k", "ṅ", "c", "ñ", "ṭ", "ṇ", "t", "n", "p", "m", "y", "r", "l", "v", "ḻ", "ḷ",
               "ṟ", "ṉ", "j", "ṣ", "s", "h", "ḵ"]),
)

LATIN = Profile(
    "latin",
    frozenset(["ae", "au", "oe", "a", "e", "i", "o", "u", "y"]),
    frozenset(["qu", "ph", "th", "ch", "b", "c", "d", "f", "g", "h", "k", "l", "m", "n", "p",
               "r", "s", "t", "v", "x", "z"]),
)

FINNISH = Profile(
    "finnish",
    frozenset(["a", "e", "i", "o", "u", "y", "ä", "ö"]),
    frozenset(["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v",
               "z", "š", "ž"]),
)

SUMERIAN = Profile(
    "sumerian",
    frozenset(["a", "e", "i", "u"]),
    frozenset(["b", "d", "g", "ŋ", "ḫ", "k", "l", "m", "n", "p", "r", "s", "š", "ṣ", "t", "ṭ",
               "z", "ř"]),
)

PROFILES = {p.name: p for p in [SANSKRIT, TAMIL, LATIN, FINNISH, SUMERIAN]}


def syllabify(phonemes: list[str], vowels: frozenset[str]) -> list[str]:
    """Group phonemes into CV / V / C units (see module docstring)."""
    units: list[str] = []
    pending: list[str] = []
    for ph in phonemes:
        if ph in vowels:
            if pending:
                units.extend(pending[:-1])
                units.append(pending[-1] + ph)
                pending = []
            else:
                units.append(ph)
        else:
            pending.append(ph)
    units.extend(pending)
    return units


# --------------------------------------------------------------------------- Tamil script

_TA_VOWELS = {
    "அ": "a", "ஆ": "ā", "இ": "i", "ஈ": "ī", "உ": "u", "ஊ": "ū",
    "எ": "e", "ஏ": "ē", "ஐ": "ai", "ஒ": "o", "ஓ": "ō", "ஔ": "au",
}
_TA_CONS = {
    "க": "k", "ங": "ṅ", "ச": "c", "ஞ": "ñ", "ட": "ṭ", "ண": "ṇ", "த": "t", "ந": "n",
    "ப": "p", "ம": "m", "ய": "y", "ர": "r", "ல": "l", "வ": "v", "ழ": "ḻ", "ள": "ḷ",
    "ற": "ṟ", "ன": "ṉ", "ஜ": "j", "ஷ": "ṣ", "ஸ": "s", "ஹ": "h",
}
_TA_SIGNS = {
    "ா": "ā", "ி": "i", "ீ": "ī", "ு": "u", "ூ": "ū", "ெ": "e", "ே": "ē",
    "ை": "ai", "ொ": "o", "ோ": "ō", "ௌ": "au",
}
_TA_PULLI = "்"
_TA_AYTAM = "ஃ"


def tamil_phonemes(word: str) -> list[str]:
    """Tamil script (Unicode) to ISO-15919-style phonemes."""
    word = _nfc(word)
    out: list[str] = []
    i = 0
    while i < len(word):
        ch = word[i]
        if ch in _TA_VOWELS:
            out.append(_TA_VOWELS[ch])
            i += 1
        elif ch in _TA_CONS:
            out.append(_TA_CONS[ch])
            nxt = word[i + 1] if i + 1 < len(word) else ""
            if nxt == _TA_PULLI:
                i += 2
            elif nxt in _TA_SIGNS:
                out.append(_TA_SIGNS[nxt])
                i += 2
            else:
                out.append("a")  # inherent vowel
                i += 1
        elif ch == _TA_AYTAM:
            out.append("ḵ")
            i += 1
        else:
            i += 1
    return out


def is_tamil_word(token: str) -> bool:
    return any("஀" <= c <= "௿" for c in token)


# --------------------------------------------------------------------------- Sumerian (CDLI ATF)

_SUX_DET = re.compile(r"\{([^}]*)\}")
_SUX_SPLIT = re.compile(r"[-.]")
_SUX_CLEAN = re.compile(r"[\[\]#?!<>⸢⸣*]")


def sux_normalize_reading(r: str) -> str:
    """ATF ASCII to Unicode-ish conventions; drop homophone index for phonetic value."""
    r = r.lower()
    r = r.replace("sz", "š").replace("s,", "ṣ").replace("t,", "ṭ").replace("j", "ŋ")
    r = r.replace("h", "ḫ")
    return r


def sux_strip_index(r: str) -> str:
    r = re.sub(r"[0-9₀-₉]+$", "", r)
    return r.replace("x", "")


def sumerian_word(token: str) -> tuple[list[str], list[str], str | None] | None:
    """Parse one ATF word.

    Returns (sign_readings_with_index, phonetic_syllables, determinative_class) or None
    if the word is broken / unreadable. Determinatives become their own reading and set
    the word's semantic class (the real determinative category).
    """
    token = _SUX_CLEAN.sub("", token)
    if not token or "x" in token.split("(")[0] or "..." in token or "$" in token:
        return None
    det_class: str | None = None
    parts: list[str] = []
    pos = 0
    for m in _SUX_DET.finditer(token):
        before = token[pos:m.start()]
        parts.extend(p for p in _SUX_SPLIT.split(before) if p)
        det = m.group(1).strip("+")
        if det:
            parts.append("{" + det + "}")
            det_class = det_class or sux_normalize_reading(det)
        pos = m.end()
    parts.extend(p for p in _SUX_SPLIT.split(token[pos:]) if p)
    if not parts:
        return None
    readings: list[str] = []
    syllables: list[str] = []
    for p in parts:
        if p.startswith("{"):
            rd = "{" + sux_normalize_reading(p[1:-1]) + "}"
            readings.append(rd)
            syllables.append(rd)
            continue
        if re.match(r"^\d+\(", p) or re.match(r"^\d+$", p):
            readings.append("#" + p)
            syllables.append("#" + p)
            continue
        if not re.match(r"^[a-zA-Z,'0-9]+$", p):
            return None
        rd = sux_normalize_reading(p)
        readings.append(rd)
        ph = sux_strip_index(rd)
        if not ph:
            return None
        syllables.append(ph)
    return readings, syllables, det_class


def sumerian_phonemes(syllables: list[str]) -> list[str]:
    out: list[str] = []
    for s in syllables:
        if s.startswith("{") or s.startswith("#"):
            out.append(s)  # keep determinatives / numerals atomic
        else:
            out.extend(SUMERIAN.phonemes(s))
    return out


# --------------------------------------------------------------------------- normalization

_LATIN_KEEP = re.compile(r"[^a-z]")
_FINNISH_KEEP = re.compile(r"[^a-zäöšž]")


def normalize_latin(tok: str) -> str:
    tok = _nfc(tok).lower().replace("j", "i")
    tok = unicodedata.normalize("NFD", tok)
    tok = "".join(c for c in tok if not unicodedata.combining(c))
    return _LATIN_KEEP.sub("", tok)


def normalize_finnish(tok: str) -> str:
    return _FINNISH_KEEP.sub("", _nfc(tok).lower())


_SKT_KEEP = re.compile(r"[^a-zāīūṛṝḷḹṅñṭḍṇśṣṃḥ]")


def normalize_sanskrit(tok: str) -> str:
    tok = _nfc(tok).lower().replace("ṁ", "ṃ")
    return _SKT_KEEP.sub("", tok)


def word_units(language: str, form: str) -> tuple[list[str], list[str]]:
    """(phonemes, syllables) for a normalized word in a non-Sumerian language."""
    if language == "tamil":
        ph = tamil_phonemes(form)
        prof = TAMIL
    else:
        prof = PROFILES[language]
        ph = prof.phonemes(form)
    return ph, syllabify(ph, prof.vowels)
