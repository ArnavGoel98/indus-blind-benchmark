"""v2 rank 6b: real related languages written in different texts (pre-registration entry 5).

Plan: docs/v2_real_relatives_plan.md. Each pair is labelled by relationship (sister or descendant).

Latin -> Italian (descendant)
  Text: Dante, La Divina Commedia, Project Gutenberg #1000 ("Public domain in the USA"), fetched
  2026-10-15, SHA-256 in SOURCES. One text per verse line.
  Units: the v1 Latin unit inventory (phonology.PROFILES['latin']), greedy segmentation, so both
  sides are cut the same way.
  Spelling: 'as_written' strips accents and diaereses, folds j to i, and turns apostrophes into
  word breaks. 'normalised' (primary) also drops h, which Italian writes but never pronounces
  (alone, or in ch/gh where it only marks a velar before e/i).
  Gold: C. H. Grandgent, An Introduction to Vulgar Latin (Boston, 1907), Internet Archive
  `introductiontovu00gran`, read in full for Phonology D (Vowels, §§178-245, with §§165-177) and
  E (Consonants, §§246-344). LATIN_ITALIAN gives per Latin unit the regular reflex, other attested
  reflexes and the section. Vowel quantity is not marked in our units; where the reflex depends on
  it, the regular reflex is that of the long vowel (quality kept) and the short-vowel reflex is
  attested (rule stated here before any measurement).

Finnish -> Estonian (sister)
  Text: Kreutzwald, Kalevipoeg, Estonian Wikisource cantos I-XX (CC BY-SA 4.0 site licence; text
  public domain), fetched 2026-10-15. One text per verse line.
  Units: letters, one character each (the Finnish profile is letters; Estonian o-tilde and u-umlaut
  are units of their own).
  Spelling: 'as_written' lowercases and splits words at anything that is not a letter.
  'normalised' (primary) also writes b, d, g as p, t, k: in native Estonian words these letters
  spell short lenis stops, not voiced ones (Pajusalu 2012: 213), which Finnish writes p, t, k.
  Nothing else is changed (pre-registration entry 9).
  Gold: K. Pajusalu, "Phonological innovations of the Southern Finnic languages", in R. Gruenthal and
  P. Kallio (eds.), A Linguistic Map of Prehistoric Northern Europe, Suomalais-Ugrilaisen Seuran
  Toimituksia 266 (Helsinki, 2012), 201-224; read in full. It has no correspondence table, so the
  table is built from the ten Finnish-North Estonian word pairs it prints (FE_PAIRS, aligned by
  hand): a letter kept in a pair gives the regular reflex; a change the paper describes as an
  innovation, or one seen only in a non-initial syllable, is attested only. A letter with no kept
  example is "no source" (entries 5, 10; NO_SOURCE, unknown): p, v, j, y, oe, d, g and the loan letters. P. Kallio, "Historical
  phonology from Proto-Finnic to Proto-Livonian", ESUKA-JEFUL 7(1) (2016), 39-65, is the cross-check
  (it agrees where it overlaps; it prints no Finnish-Estonian pairs). Rules: entry 9.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

from .. import phonology
from ..paths import raw_dir
from .gold import NO_SOURCE

SOURCES = {
    "dante_pg1000.txt": {"url": "https://www.gutenberg.org/cache/epub/1000/pg1000.txt",
                         "sha256": "4669dcc00ee61ceffe92d871e61ea430cec87b35cbab24f19a4c0b1c7da521b2",
                         "licence": "Public domain in the USA (Project Gutenberg #1000)", "fetched": "2026-10-15"},
}
KALEVIPOEG_CANTOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV",
                     "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]
RELATIONSHIP = {("latin", "italian"): "descendant", ("finnish", "estonian"): "sister",
                ("tamil", "malayalam"): "descendant", ("tamil", "kannada"): "sister", ("sanskrit", "pali"): "descendant"}

# The relatives' own vowel letters, for the syllable cutter (entry 11; orthography, not gold). Italian's are
# all Latin vowels; Estonian adds õ and ü to Finnish's.
ITALIAN_VOWELS = frozenset("aeiou")
ESTONIAN_VOWELS = frozenset("aeiouõäöü")

LATIN_INVENTORY = sorted(phonology.PROFILES["latin"].consonants | phonology.PROFILES["latin"].vowels)

# Latin unit -> (regular reflex, other attested reflexes, Grandgent 1907 section). None = no reflex.
LATIN_ITALIAN: dict[str, tuple[str | None, tuple[str, ...], str]] = {
    "a": ("a", (), "§194"),
    "ae": ("e", (), "§§209-210"),
    "au": ("o", ("au",), "§211 (It. au > o after q > uo)"),
    "e": ("e", ("i",), "§§196, 199; §177 (It. ie); §197 i for e"),
    "i": ("i", ("e",), "§200 (long i stays); §201 (short i > e)"),
    "o": ("o", ("u",), "§§202, 205; §177 (It. uo)"),
    "oe": ("e", (), "§215"),
    "u": ("u", ("o",), "§206 (long u stays); §208 (short u > o)"),
    "y": ("i", ("u",), "§187 (popular i; older u)"),
    "b": ("b", ("v",), "§315 (non-intervocalic b stays); §318 (intervocalic b > beta, written v)"),
    "c": ("c", ("g",), "§§258-263 (spelling c kept; palatal before e, i); §256 (voicing, not general in central Italy)"),
    "ch": ("c", ("ch",), "§332 (popular c for Greek chi)"),
    "d": ("d", (), "§281"),
    "f": ("f", (), "§320"),
    "g": ("g", (), "§§259, 263"),
    "h": (None, (), "§249 (no trace of Latin h in Romance)"),
    "k": ("c", (), "§253 (c and k same value)"),
    "l": ("l", ("i",), "§289; §288 (l after consonant palatalised, It. chiave)"),
    "m": ("m", (), "§303; §309 (final m lost)"),
    "n": ("n", (), "§303; §311 (n lost before s)"),
    "p": ("p", ("b",), "§312; §314 (intervocalic p > b only in the north)"),
    "ph": ("f", ("p",), "§334 (f standard from the 4th century); §332 (older p)"),
    "qu": ("qu", ("c",), "§254 (kw kept before a, e, i; k before o, u)"),
    "r": ("r", (), "§290; §295 (final r lost)"),
    "s": ("s", (), "§297; §298 (final s lost in Italy)"),
    "t": ("t", (), "§284; §286 (voicing only in the north)"),
    "th": ("t", (), "§332"),
    "v": ("v", ("b",), "§322; §323 (v > b after liquids, It. nerbo)"),
    "x": ("s", (), "§255 (ks > s before consonants and finally; ss only locally)"),
    "z": ("z", (), "§§338-339"),
}


def relatives_dir() -> Path:
    return raw_dir() / "relatives"


def _check(name: str) -> str:
    raw = (relatives_dir() / name).read_bytes()
    want = SOURCES[name]["sha256"]
    if hashlib.sha256(raw).hexdigest() != want:
        raise ValueError(f"{name} changed since it was fetched")
    return raw.decode("utf-8")


_HEAD = re.compile(r"^(INFERNO|PURGATORIO|PARADISO|Inferno|Purgatorio|Paradiso|Canto [IVXL]+\.?)\s*$")


def dante_lines() -> list[str]:
    t = _check("dante_pg1000.txt")
    body = t.split("*** START OF THE PROJECT GUTENBERG EBOOK", 1)[1].split("***", 1)[1]
    body = body.split("*** END OF THE PROJECT GUTENBERG EBOOK", 1)[0]
    lines = body.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "Inferno")    # first canto heading, after contents
    return [l.strip() for l in lines[start:] if l.strip() and not _HEAD.match(l.strip())]


def italian_words(line: str, spelling: str = "normalised") -> list[tuple[str, ...]]:
    s = unicodedata.normalize("NFD", line.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[’'‘]", " ", s).replace("j", "i")
    out = []
    for w in re.findall(r"[a-z]+", s):
        if spelling == "normalised":
            w = w.replace("h", "")
        if w:
            out.append(tuple(phonology.greedy_graphemes(w, LATIN_INVENTORY)))
    return out


def dante_texts(spelling: str = "normalised") -> list[list[tuple[str, ...]]]:
    """Verse lines as lists of words (unit tuples)."""
    return [ws for ws in (italian_words(l, spelling) for l in dante_lines()) if ws]


def latin_italian_map() -> tuple[dict[str, str | None], dict[str, set]]:
    regular = {k: v[0] for k, v in LATIN_ITALIAN.items()}
    attested = {k: ({v[0]} if v[0] else set()) | set(v[1]) for k, v in LATIN_ITALIAN.items()}
    return regular, attested


# ------------------------------------------------------------------ Finnish -> Estonian (entry 9)

GOLD_SOURCES_FE = {
    "pajusalu2012": {"url": "https://www.sgr.fi/sust/sust266/sust266_pajusalu.pdf",
                     "retrieved_from": "https://web.archive.org/web/2020id_/https://www.sgr.fi/sust/sust266/sust266_pajusalu.pdf",
                     "note": "the society's URL now redirects to its home page; the archived copy is the society's PDF",
                     "sha256": "9be38b56fca0ff90de4522de993a8a6aee60c119efa8fa0d74ed7918c84263fc", "fetched": "2026-10-24"},
    "kallio2016": {"url": "https://ojs.utlib.ee/index.php/jeful/article/download/jeful.2016.7.1.02/9989/",
                   "doi": "10.12697/jeful.2016.7.1.02",
                   "sha256": "cf0e90ce7cf5ff33e213aaa85958f29ea65c5fb1bb1a34c9f50380fa0fc00329", "fetched": "2026-10-24"},
}

# Every Finnish-North Estonian word pair printed in Pajusalu (2012), aligned letter by letter.
# kind: "kept" (same letter after normalisation), "innov" (a change the paper describes, or one in a
# non-initial syllable), "lost" (no Estonian letter), "added" (no Finnish letter). The Kihnu pairs lapset ~ lapsoed and olimme ~
# olimoe (p. 217) are left out: they show velar vowel harmony, which Table 1 (p. 219) marks as absent
# from North Estonian.
FE_PAIRS: list[tuple[str, str, str, list[tuple[str, str | None, str]]]] = [
    ("lukea", "lugeda", "p. 208", [("l", "l", "kept"), ("u", "u", "kept"), ("k", "k", "kept"), ("e", "e", "kept"),
                                   ("", "t", "added"), ("a", "a", "kept")]),     # Estonian d of the -da infinitive
    ("luen", "loen", "p. 208", [("l", "l", "kept"), ("u", "o", "innov"), ("e", "e", "kept"), ("n", "n", "kept")]),
    ("kolmas", "kolmas", "p. 215", [("k", "k", "kept"), ("o", "o", "kept"), ("l", "l", "kept"), ("m", "m", "kept"),
                                    ("a", "a", "kept"), ("s", "s", "kept")]),
    ("sisar", "sõsar", "p. 216", [("s", "s", "kept"), ("i", "õ", "innov"), ("s", "s", "kept"), ("a", "a", "kept"),
                                  ("r", "r", "kept")]),
    ("nenä", "nina", "p. 216", [("n", "n", "kept"), ("e", "i", "innov"), ("n", "n", "kept"), ("ä", "a", "innov")]),
    ("kaikki", "kõik", "p. 216", [("k", "k", "kept"), ("a", "õ", "innov"), ("i", "i", "kept"), ("k", "k", "kept"),
                                  ("k", None, "lost"), ("i", None, "lost")]),
    ("heimo", "hõim", "p. 216", [("h", "h", "kept"), ("e", "õ", "innov"), ("i", "i", "kept"), ("m", "m", "kept"),
                                 ("o", None, "lost")]),
    ("sana", "sõna", "p. 216", [("s", "s", "kept"), ("a", "õ", "innov"), ("n", "n", "kept"), ("a", "a", "kept")]),
    ("lanka", "lõng", "p. 217", [("l", "l", "kept"), ("a", "õ", "innov"), ("n", "n", "kept"), ("k", "k", "kept"),
                                 ("a", None, "lost")]),
    ("kato", "kadu", "p. 218", [("k", "k", "kept"), ("a", "a", "kept"), ("t", "t", "kept"), ("o", "u", "innov")]),
]

# Finnish letter -> (regular reflex or NO_SOURCE, other attested reflexes, Pajusalu 2012 pages).
# NO_SOURCE = "no source" (entries 5, 10): unknown, so unrecoverable under strict scoring.
FINNISH_ESTONIAN: dict[str, tuple[str | None, tuple[str, ...], str]] = {
    "a": ("a", ("õ",), "kept: pp. 208, 215, 216, 218; õ: pp. 216-217 (sõna, kõik, lõng; a > õ in North Estonian)"),
    "e": ("e", ("i", "õ"), "kept: p. 208; i: p. 216 (nina; Finnish e for North Estonian i, p. 216-217); õ: p. 216 (hõim)"),
    "i": ("i", ("õ",), "kept: p. 216 (kõik, hõim); õ: p. 216 (sõsar)"),
    "o": ("o", ("u", "õ"), "kept: p. 215; u: p. 218 (o > u in non-initial syllables, kadu); õ: p. 217 (o-stems in North Estonian)"),
    "u": ("u", ("o",), "kept: p. 208 (lugeda); o: p. 208 (loen)"),
    "ä": (NO_SOURCE, ("a",), "no kept example; a: p. 216 (nina), p. 218 (loss of vowel harmony, non-initial syllables)"),
    "h": ("h", (), "kept: p. 216 (hõim); lost word-initially and finally in most North Estonian dialects: p. 214"),
    "k": ("k", (), "kept: pp. 208, 215, 216, 217, 218 (g spells the short lenis k: p. 213)"),
    "l": ("l", (), "kept: pp. 208, 215, 217"),
    "m": ("m", (), "kept: pp. 215, 216"),
    "n": ("n", (), "kept: pp. 208, 216, 217; lost word-finally and vocalised before s: pp. 214-215"),
    "r": ("r", (), "kept: p. 216 (sõsar)"),
    "s": ("s", (), "kept: pp. 215, 216"),
    "t": ("t", (), "kept: p. 218 (kadu; d spells the short lenis t: p. 213)"),
}
for _u in ("p", "v", "j", "y", "ö", "d", "g", "b", "c", "f", "z", "š", "ž"):
    FINNISH_ESTONIAN[_u] = (NO_SOURCE, (), "no source: no Finnish-Estonian pair with this letter in Pajusalu (2012)")


def _check_fe_table() -> None:
    """Every regular and attested reflex must come from an aligned pair, except o > õ (a statement, p. 217)."""
    kept = {(f, e) for _, _, _, al in FE_PAIRS for f, e, k in al if k == "kept"}
    innov = {(f, e) for _, _, _, al in FE_PAIRS for f, e, k in al if k == "innov"} | {("o", "õ")}
    for u, (reg, att, _) in FINNISH_ESTONIAN.items():
        assert reg == NO_SOURCE or (u, reg) in kept, u
        assert all((u, a) in innov for a in att), u
        assert reg != NO_SOURCE or not any(f == u for f, _ in kept), u
    for fi, et, _, al in FE_PAIRS:
        assert "".join(f for f, _, _ in al) == fi, fi
        assert "".join(e for _, e, _ in al if e) == estonian_normalise(et), et


def finnish_estonian_map() -> tuple[dict[str, str | None], dict[str, set]]:
    _check_fe_table()
    regular = {k: v[0] for k, v in FINNISH_ESTONIAN.items()}
    attested = {k: ({v[0]} if v[0] not in (None, NO_SOURCE) else set()) | set(v[1]) for k, v in FINNISH_ESTONIAN.items()}
    return regular, attested


_LENIS = str.maketrans("bdg", "ptk")


def estonian_normalise(word: str) -> str:
    return word.translate(_LENIS)


def estonian_words(line: str, spelling: str = "normalised") -> list[tuple[str, ...]]:
    out = []
    for w in re.findall(r"[a-zõäöüšž]+", unicodedata.normalize("NFC", line.lower())):
        if spelling == "normalised":
            w = estonian_normalise(w)
        out.append(tuple(w))
    return out


def kalevipoeg_texts(spelling: str = "normalised") -> list[list[tuple[str, ...]]]:
    """Verse lines as lists of words (unit tuples)."""
    return [ws for ws in (estonian_words(l, spelling) for l in kalevipoeg_lines()) if ws]


# Hand-checked examples (entry 9: rules are tested before any measurement).
ESTONIAN_CHECKS = [
    ("Kotkas kõrge kalju peale", "as_written", [tuple("kotkas"), tuple("kõrge"), tuple("kalju"), tuple("peale")]),
    ("Kotkas kõrge kalju peale", "normalised", [tuple("kotkas"), tuple("kõrke"), tuple("kalju"), tuple("peale")]),
    ("Jumalikul juhatusel", "normalised", [tuple("jumalikul"), tuple("juhatusel")]),
    ("Riiki kohe rajatanud,", "normalised", [tuple("riiki"), tuple("kohe"), tuple("rajatanut")]),
    ("Sõitis üle Soome mere,", "as_written", [tuple("sõitis"), tuple("üle"), tuple("soome"), tuple("mere")]),
    ("lugeda : loen, Tütar-lapse", "normalised", [tuple("luketa"), tuple("loen"), tuple("tütar"), tuple("lapse")]),
]


def check_estonian() -> None:
    for line, sp, want in ESTONIAN_CHECKS:
        got = estonian_words(line, sp)
        assert got == want, (line, sp, got)
    _check_fe_table()


# ------------------------------------------------------------------ Kalevipoeg text

def kalevipoeg_lines() -> list[str]:
    out = []
    for c in KALEVIPOEG_CANTOS:
        t = (relatives_dir() / f"kalevipoeg_{c}.wiki").read_text(encoding="utf-8")
        t = re.sub(r"\{\{ReaNr\|\d+\}\}", "", t)
        for blk in re.findall(r"<poem[^>]*>(.*?)</poem>", t, re.S):
            for l in blk.splitlines():
                l = re.sub(r"\{\{[^}]*\}\}|\[\[[^\]|]*\||\]\]|\[\[|'''|''", "", l).strip()
                if l:
                    out.append(l)
    return out
