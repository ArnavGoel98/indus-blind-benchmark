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
  public domain), fetched 2026-10-15. Parsed here for size only: its gold source (Pajusalu 2012) is
  not reachable from this environment yet, so no Finnish-Estonian yardstick is computed.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

from .. import phonology
from ..paths import raw_dir

SOURCES = {
    "dante_pg1000.txt": {"url": "https://www.gutenberg.org/cache/epub/1000/pg1000.txt",
                         "sha256": "4669dcc00ee61ceffe92d871e61ea430cec87b35cbab24f19a4c0b1c7da521b2",
                         "licence": "Public domain in the USA (Project Gutenberg #1000)", "fetched": "2026-10-15"},
}
KALEVIPOEG_CANTOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV",
                     "XV", "XVI", "XVII", "XVIII", "XIX", "XX"]
RELATIONSHIP = {("latin", "italian"): "descendant", ("finnish", "estonian"): "sister",
                ("tamil", "malayalam"): "descendant", ("tamil", "kannada"): "sister", ("sanskrit", "pali"): "descendant"}

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


# ------------------------------------------------------------------ Kalevipoeg (size only for now)

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
