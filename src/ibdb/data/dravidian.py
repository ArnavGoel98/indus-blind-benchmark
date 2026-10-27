"""v2 rank 6b: Tamil -> Malayalam (descendant) and Tamil -> Kannada (sister) (pre-registration entry 5).

Texts (fetched by scripts/v2/fetch_dravidian_wikisource.py; manifest with revision ids and SHA-256):
- Malayalam: Ezhuthachan, Adhyatma Ramayanam Kilippattu, Malayalam Wikisource section pages.
- Kannada: Kumaravyasa, Karnata Bharata Kathamanjari, Kannada Wikisource pages linked from the index
  page, excluding the "ಸಟೀಕಾ" pages (modern commentary).
Licence: CC BY-SA 4.0 (Wikisource site licence); texts public domain by age. Source edition
unstated on either site; typed by volunteers (ml 2007-08, kn from 2013); no link to the CC BY-NC-ND
scan on Internet Archive. Accepted as clean by the project owner on 2026-10-15.

Units: the v1 Tamil units (ISO-15919-style phonemes from the script, phonology.tamil_phonemes).
Malayalam and Kannada script are converted the same way (deterministic tables below). The anusvara
is written as the nasal of the following consonant's row, m otherwise (Caldwell 1875: 27, 65).
Malayalam has one letter for dental n and alveolar n; it is read as n (Caldwell 1875: 13, the two
Tamil letters differ "in form rather than of sound").

Spelling: 'as_written' keeps every distinction the script writes. 'normalised' (primary) collapses
the voicing and aspiration that Tamil script cannot write (Caldwell 1875: 12-13, 21-22): kh, g, gh
-> k; ch, j, jh -> c; ṭh, ḍ, ḍh -> ṭ; th, d, dh -> t; ph, b, bh -> p.

Gold: R. Caldwell, A Comparative Grammar of the Dravidian or South-Indian Family of Languages, 2nd
ed. (London, 1875), Internet Archive `in.ernet.dli.2015.459581`; read for pp. 11-27 (alphabets,
vowels, consonants) and 48-64 (dialectic interchange, euphonic permutation). Each row cites pages.
Identity rows rest on the shared sound system (pp. 11-14, 21-27); changes on pp. 15-20 and 48-61.
Rows with no statement in the read pages are NO_SOURCE ("no source": unknown, entry 10), unrecoverable
under strict scoring.
"""

from __future__ import annotations

import json
import re
import unicodedata

from ..paths import raw_dir
from .gold import NO_SOURCE

RELATIONSHIP = {"malayalam": "descendant", "kannada": "sister"}

_ML_V = {"അ": "a", "ആ": "ā", "ഇ": "i", "ഈ": "ī", "ഉ": "u", "ഊ": "ū", "ഋ": "ṛ", "എ": "e", "ഏ": "ē", "ഐ": "ai",
         "ഒ": "o", "ഓ": "ō", "ഔ": "au"}
_ML_S = {"ാ": "ā", "ി": "i", "ീ": "ī", "ു": "u", "ൂ": "ū", "ൃ": "ṛ", "െ": "e", "േ": "ē", "ൈ": "ai", "ൊ": "o",
         "ോ": "ō", "ൌ": "au", "ൗ": "au"}
_ML_C = {"ക": "k", "ഖ": "kh", "ഗ": "g", "ഘ": "gh", "ങ": "ṅ", "ച": "c", "ഛ": "ch", "ജ": "j", "ഝ": "jh", "ഞ": "ñ",
         "ട": "ṭ", "ഠ": "ṭh", "ഡ": "ḍ", "ഢ": "ḍh", "ണ": "ṇ", "ത": "t", "ഥ": "th", "ദ": "d", "ധ": "dh", "ന": "n",
         "പ": "p", "ഫ": "ph", "ബ": "b", "ഭ": "bh", "മ": "m", "യ": "y", "ര": "r", "റ": "ṟ", "ല": "l", "ള": "ḷ",
         "ഴ": "ḻ", "വ": "v", "ശ": "ś", "ഷ": "ṣ", "സ": "s", "ഹ": "h"}
_ML_CHILLU = {"ൺ": "ṇ", "ൻ": "n", "ർ": "r", "ൽ": "l", "ൾ": "ḷ", "ൿ": "k", "ൎ": "r"}
_ML = {"V": _ML_V, "S": _ML_S, "C": _ML_C, "virama": "്", "anusvara": "ം", "visarga": "ഃ", "extra": _ML_CHILLU}

_KN_V = {"ಅ": "a", "ಆ": "ā", "ಇ": "i", "ಈ": "ī", "ಉ": "u", "ಊ": "ū", "ಋ": "ṛ", "ಎ": "e", "ಏ": "ē", "ಐ": "ai",
         "ಒ": "o", "ಓ": "ō", "ಔ": "au"}
_KN_S = {"ಾ": "ā", "ಿ": "i", "ೀ": "ī", "ು": "u", "ೂ": "ū", "ೃ": "ṛ", "ೆ": "e", "ೇ": "ē", "ೈ": "ai", "ೊ": "o",
         "ೋ": "ō", "ೌ": "au"}
_KN_C = {"ಕ": "k", "ಖ": "kh", "ಗ": "g", "ಘ": "gh", "ಙ": "ṅ", "ಚ": "c", "ಛ": "ch", "ಜ": "j", "ಝ": "jh", "ಞ": "ñ",
         "ಟ": "ṭ", "ಠ": "ṭh", "ಡ": "ḍ", "ಢ": "ḍh", "ಣ": "ṇ", "ತ": "t", "ಥ": "th", "ದ": "d", "ಧ": "dh", "ನ": "n",
         "ಪ": "p", "ಫ": "ph", "ಬ": "b", "ಭ": "bh", "ಮ": "m", "ಯ": "y", "ರ": "r", "ಱ": "ṟ", "ಲ": "l", "ಳ": "ḷ",
         "ೞ": "ḻ", "ವ": "v", "ಶ": "ś", "ಷ": "ṣ", "ಸ": "s", "ಹ": "h"}
_KN = {"V": _KN_V, "S": _KN_S, "C": _KN_C, "virama": "್", "anusvara": "ಂ", "visarga": "ಃ", "extra": {}}
SCRIPTS = {"malayalam": _ML, "kannada": _KN}

_ROW_NASAL = [({"k", "kh", "g", "gh"}, "ṅ"), ({"c", "ch", "j", "jh"}, "ñ"), ({"ṭ", "ṭh", "ḍ", "ḍh"}, "ṇ"),
              ({"t", "th", "d", "dh"}, "n"), ({"p", "ph", "b", "bh"}, "m")]
NORMALISE = {"kh": "k", "g": "k", "gh": "k", "ch": "c", "j": "c", "jh": "c", "ṭh": "ṭ", "ḍ": "ṭ", "ḍh": "ṭ",
             "th": "t", "d": "t", "dh": "t", "ph": "p", "b": "p", "bh": "p"}


def script_phonemes(word: str, lang: str, spelling: str = "normalised") -> list[str]:
    """Abugida word -> phonemes (inherent a, virama, vowel signs, chillus, anusvara by next row)."""
    t = SCRIPTS[lang]
    w = unicodedata.normalize("NFC", word).replace("‌", "").replace("‍", "")
    out: list[str] = []
    pending_anusvara: list[int] = []
    i = 0
    while i < len(w):
        ch = w[i]
        if ch in t["V"]:
            out.append(t["V"][ch])
            i += 1
        elif ch in t["C"]:
            out.append(t["C"][ch])
            nxt = w[i + 1] if i + 1 < len(w) else ""
            if nxt == t["virama"]:
                i += 2
            elif nxt in t["S"]:
                out.append(t["S"][nxt])
                i += 2
            else:
                out.append("a")
                i += 1
        elif ch in t["extra"]:
            out.append(t["extra"][ch])
            i += 1
        elif ch == t["anusvara"]:
            pending_anusvara.append(len(out))
            out.append("m")
            i += 1
        elif ch == t["visarga"]:
            out.append("ḥ")
            i += 1
        else:
            i += 1
    for k in pending_anusvara:                      # homorganic nasal before a stop
        if k + 1 < len(out):
            out[k] = next((n for row, n in _ROW_NASAL if out[k + 1] in row), "m")
    if spelling == "normalised":
        out = [NORMALISE.get(p, p) for p in out]
    return out


KN_PARVAS = ("ಆದಿಪರ್ವ", "ಸಭಾಪರ್ವ", "ಅರಣ್ಯಪರ್ವ", "ವಿರಾಟಪರ್ವ", "ಉದ್ಯೋಗಪರ್ವ", "ಭೀಷ್ಮಪರ್ವ", "ದ್ರೋಣಪರ್ವ", "ಕರ್ಣಪರ್ವ",
             "ಶಲ್ಯಪರ್ವ", "ಗದಾಪರ್ವ")
KN_SANDHI = re.compile(r"^(" + "|".join(KN_PARVAS) + r"): *[೦-೯0-9]+\..*ಸಂಧಿ")   # Kumaravyasa sandhi pages only
_DIGITS = re.compile(r"[0-9೦-೯൦-൯|।॥]+")


def _poem_lines(text: str) -> list[str]:
    blocks = re.findall(r"<poem[^>]*>(.*?)</poem>", text, re.S) or [text]
    lines = []
    for b in blocks:
        for l in b.splitlines():
            l = re.sub(r"<[^>]+>|\{\{[^}]*\}\}|\[\[[^\]|]*\||\]\]|\[\[|'''|''|^[=:*#;]+|[=]+$", "", l)
            l = _DIGITS.sub(" ", l).strip()
            if l and not l.startswith(("{", "|", "}", "<")):     # templates, tables, navigation links
                lines.append(l)
    return lines


def lines(lang: str) -> list[str]:
    site = {"malayalam": "ml", "kannada": "kn"}[lang]
    d = raw_dir() / "relatives" / site
    man = json.loads((d / "manifest.json").read_text())
    out = []
    for title, m in sorted(man.items(), key=lambda kv: kv[1]["file"]):
        if lang == "kannada" and ("ಸಟೀಕಾ" in title or not KN_SANDHI.match(title)):
            continue
        out += _poem_lines((d / m["file"]).read_text(encoding="utf-8"))
    return out


def texts(lang: str, spelling: str = "normalised") -> list[list[tuple[str, ...]]]:
    """Verse lines as lists of words (phoneme tuples); words with no letters are dropped."""
    out = []
    for l in lines(lang):
        ws = [tuple(script_phonemes(w, lang, spelling)) for w in re.split(r"[\s\-–—,.;:!?\"'‘’“”()\[\]]+", l)]
        ws = [w for w in ws if w]
        if ws:
            out.append(ws)
    return out


# ------------------------------------------------------------------ gold tables (Caldwell 1875)
# Tamil unit -> (regular reflex, other attested reflexes, pages). NO_SOURCE = no source (entry 10).
_SHARED = "pp. 11-14, 21-27 (shared Dravidian sound system)"
TAMIL_MALAYALAM: dict[str, tuple[str | None, tuple[str, ...], str]] = {
    "a": ("a", (), "pp. 15-16 (a less subject to change in Malayalam; neuter plural -a kept)"),
    "ā": ("ā", (), "pp. 15-16"),
    "i": ("i", (), "p. 17 (i, ī call for no remark)"),
    "ī": ("ī", (), "p. 17"),
    "u": ("u", ("a",), "pp. 17-18 (short a sometimes replaces Tamil short u in Malayalam)"),
    "ū": ("ū", (), "p. 17"),
    "e": ("e", (), "pp. 18-19"),
    "ē": ("ē", (), "pp. 18-19"),
    "o": ("o", (), "pp. 18-19"),
    "ō": ("ō", (), "pp. 18-19"),
    "ai": ("a", ("e", "ai"), "p. 19 (Tam. talei = Mal. tala); p. 16 (Tamil ei = Mal. accusative e)"),
    "au": ("au", (), "pp. 19-20 (au only in Sanskrit derivatives)"),
    "k": ("k", ("v",), "pp. 23-24; p. 48 (g ~ v)"),
    "ṅ": ("ṅ", (), "p. 23"),
    "c": ("c", ("y",), "p. 22 (written and pronounced ch in Malayalam); p. 50 (c > y)"),
    "ñ": ("ñ", (), "p. 24 (Mal. initial ñ where Tamil has n)"),
    "ṭ": ("ṭ", (), "p. 25"),
    "ṇ": ("ṇ", ("n",), "pp. 50-51 (Malayalam sometimes softens ṇ into n)"),
    "t": ("t", ("c", "l"), "p. 26; p. 53 (tt > cc after i, e); p. 52 (t > l in Sanskrit words)"),
    "n": ("n", ("ñ",), "p. 26; p. 53 (nd > ñj classical in Malayalam)"),
    "ṉ": ("n", (), "p. 13 (Tamil n and ṉ differ in form, not sound; Malayalam writes one letter)"),
    "p": ("p", ("m",), "p. 27; p. 54 (b > m, Tam. uṇbāṉ = Mal. uṇmān)"),
    "m": ("m", (), "p. 27"),
    "y": ("y", ("ñ",), "pp. 27-28; p. 54 (y ~ ñ)"),
    "r": ("r", ("l",), "pp. 27-28; p. 56 (r > l in Malayalam)"),
    "l": ("l", (), "pp. 27-28"),
    "v": ("v", ("m",), "pp. 27-28; p. 58 (v ~ m in Malayalam)"),
    "ḻ": ("ḻ", ("ḷ", "y"), "p. 11 (Malayalam has Tamil ḻ); pp. 59-60 (ḻ > ḷ finally, > y)"),
    "ḷ": ("ḷ", (), "pp. 27-28"),
    "ṟ": ("ṟ", (), "p. 11 (Malayalam alphabet has the hard r)"),
    "ḵ": (NO_SOURCE, (), "p. 12 (āytam only in the poets; no Malayalam letter: a script fact, not a sound law; entry 10)"),
    "j": ("c", (), "p. 24 (ordinarily the sound of ch/ś used instead of j)"),
    "h": (NO_SOURCE, (), "no source in the pages read"),
    "s": (NO_SOURCE, (), "no source in the pages read"),
    "ṣ": (NO_SOURCE, (), "no source in the pages read (Grantha letter; p. 13: never in the ancient grammars)"),
}
TAMIL_KANNADA: dict[str, tuple[str | None, tuple[str, ...], str]] = {
    "a": ("a", ("e", "u"), "pp. 15-16 (final a > e in Canarese; neuter plurals end in u)"),
    "ā": ("ā", (), "pp. 15-16"),
    "i": ("i", (), "p. 17"),
    "ī": ("ī", (), "p. 17"),
    "u": ("u", (), "pp. 17-18 (enunciative u, rule shared with ancient Canarese)"),
    "ū": ("ū", (), "p. 17"),
    "e": ("e", ("i",), "pp. 18-19; p. 49 (Tam. cevi = Can. kivi)"),
    "ē": ("ē", (), "pp. 18-19"),
    "o": ("o", (), "pp. 18-19"),
    "ō": ("ō", (), "pp. 18-19"),
    "ai": ("e", ("ai",), "p. 16 (Tamil ei = final e of Canarese nouns); p. 19 (talei = tale)"),
    "au": ("au", (), "pp. 19-20"),
    "k": ("k", (), "p. 49 (Canarese generally retains k)"),
    "ṅ": ("ṅ", (), "p. 23"),
    "c": ("c", ("k",), "p. 24; p. 49 (Tamil c where Canarese has k: cevi/kivi, cey/gey)"),
    "ñ": ("ñ", (), "p. 24"),
    "ṭ": ("ṭ", (), "p. 25"),
    "ṇ": ("ṇ", (), "pp. 50-51"),
    "t": ("t", ("r",), "p. 26; p. 51 (d > r in the Canarese oblique increment)"),
    "n": ("n", (), "p. 26"),
    "ṉ": ("n", (), "p. 13 (form not sound); p. 11 (no such letter in the Canarese alphabet)"),
    "p": ("p", ("h",), "p. 27; p. 53 (initial p > h in modern Canarese; old Canarese keeps p)"),
    "m": ("m", ("v",), "p. 27; p. 54 (old Can. nām > modern nāvu)"),
    "y": ("y", ("s", "t"), "pp. 27-28; p. 50 (Can. hesar = Tam. peyar); p. 55 (y > d)"),
    "r": ("r", ("ṟ",), "pp. 27-28; pp. 55-56 (r ~ ṟ interchange)"),
    "l": ("l", (), "pp. 27-28"),
    "v": ("v", ("p",), "pp. 27-28; p. 58 (initial v > b in Canarese)"),
    "ḻ": ("ḷ", ("ḻ",), "p. 59 (Tamil ḻ is always ḷ in modern Canarese; old Canarese has ḻ)"),
    "ḷ": ("ḷ", (), "pp. 27-28"),
    "ṟ": ("ṟ", ("r",), "p. 11 (hard r in the Telugu-Canarese alphabets); pp. 55-56"),
    "ḵ": (NO_SOURCE, (), "p. 12 (āytam only in the poets; nothing on Kannada; entry 10)"),
    "j": ("c", (), "p. 24"),
    "h": (NO_SOURCE, (), "no source in the pages read"),
    "s": (NO_SOURCE, (), "no source in the pages read"),
    "ṣ": (NO_SOURCE, (), "no source in the pages read (Grantha letter; p. 13: never in the ancient grammars)"),
}
GOLD = {"malayalam": TAMIL_MALAYALAM, "kannada": TAMIL_KANNADA}


def gold_map(lang: str) -> tuple[dict[str, str | None], dict[str, set]]:
    g = GOLD[lang]
    regular = {k: v[0] for k, v in g.items()}
    attested = {k: ({v[0]} if v[0] not in (None, NO_SOURCE) else set()) | set(v[1]) for k, v in g.items()}
    return regular, attested
