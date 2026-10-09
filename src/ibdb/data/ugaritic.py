"""v2 rank 2: Ugaritic (hidden) and Biblical Hebrew (reference) for the real-relative anchor.

Plan: docs/v2_ugaritic_plan.md (pushed to `v2` as b05772d before any run). Not part of the v1 paper.

Ugaritic: EUPT (Edition des ugaritischen poetischen Textkorpus), Version Draft 3.2 [2025-07-18],
facsimile transliteration pages KTU_1.{14,15,16}_facsimile.html, CC BY-SA 4.0 (each tablet
manifest). Only the Kirta epic is published. Pages were fetched on 2026-10-09; their SHA-256 are in
EUPT_PAGES and are checked on load.

Hebrew: Open Scriptures Hebrew Bible (WLC 4.20 in OSIS), `wlc/*.xml`, commit OSHB_COMMIT. WLC is
public domain; OSHB is CC BY 4.0: "Original work of the Open Scriptures Hebrew Bible available at
https://github.com/openscriptures/morphhb".

Gold correspondences: Wikipedia, "Ugaritic alphabet", letters table, Hebrew column (read
2026-10-09), which cites Kogan (2011), Tab. 6.2, in Weninger (ed.), The Semitic Languages, p. 55.
We have not read Kogan. The table leaves the Hebrew cell empty for ỉ, ủ and s₂; the plan maps the
three aleph signs to א, and scores are also reported without ỉ and ủ (UNSOURCED).
"""

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

from ..corpus import AnswerKey, Corpus
from ..generator.script import DIV
from ..paths import raw_dir

EUPT_ACCESSED = "2026-10-09"
EUPT_VERSION = "Draft 3.2 [2025-07-18]"
EUPT_BASE = "https://eupt.uni-goettingen.de/api/eupt/html/"
EUPT_PAGES = {
    "KTU_1.14_facsimile.html": "ad851529e956ae5ca89237c2497a32af3afc365b51411cb40a49de017be886c6",
    "KTU_1.15_facsimile.html": "48a0eca1ded4ce4bc84e4c7d40626cc19360ca7730b696dfc82f13b764bb4ea7",
    "KTU_1.16_facsimile.html": "d6e6d6b80edec566577802cad6628bb02d31b04232dbd6a4b875eba5c244f37f",
}
OSHB_COMMIT = "3d15126fb1ef74867fc1434be1942e837932691f"
POETIC_BOOKS = ("Ps", "Job", "Prov")

# EUPT letter -> Hebrew letter (Wikipedia table citing Kogan 2011; not read). Many-to-one.
GOLD = {
    "a": "א", "i": "א", "u": "א",
    "b": "ב", "g": "ג", "ḫ": "ח", "ḥ": "ח", "d": "ד", "ḏ": "ז", "z": "ז", "h": "ה", "w": "ו",
    "ṭ": "ט", "ẓ": "צ", "ṣ": "צ", "y": "י", "k": "כ", "s": "ס", "š": "ש", "ṯ": "ש", "t": "ת",
    "l": "ל", "m": "מ", "n": "נ", "ˁ": "ע", "ġ": "ע", "p": "פ", "q": "ק", "r": "ר",
}
UNSOURCED = {"i", "u"}           # the table's Hebrew cell is empty for these
LETTERS = set(GOLD) | {"s̀"}       # s̀ (s2) has no Hebrew cell; kept as a sign, scored as unrecoverable
DIVIDER = "."
GAP = None                       # marks a dropped stretch (restoration or illegible sign) in a parsed line
SKIP_CLASSES = {"del", "sic", "surplus", "supplied"}   # erasures, the tablet's wrong sign, editorial deletions/additions
FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def eupt_dir() -> Path:
    return raw_dir() / "eupt"


def oshb_dir() -> Path:
    return raw_dir() / "oshb" / "wlc"


class _Line(HTMLParser):
    """Collect the transliteration of each `line-body` span as a list of segments.

    Kept: letters read as certain, and damaged letters the edition reads (inside ⸢ ⸣, with or
    without '?'); corrected readings (corr of a choice, written 'b!(Text:d)'). Word dividers
    become DIVIDER. Dropped, and treated as a GAP that ends the current segment: restorations
    inside [ ] and illegible 'x'. Dropped without a gap: erased signs ([[ ]], class del; the
    scribe's erasure, usually overwritten), the tablet's wrong sign in a correction (class sic),
    and editorial deletions { } (surplus) and additions < > (supplied)."""

    def __init__(self):
        super().__init__()
        self.stack: list[set[str]] = []
        self.body_depth = 0
        self.lines: list[list[list[str]]] = []
        self.line_ids: list[str] = []
        self.cur_nr: str | None = None
        self.in_nr = 0
        self.seg: list[str] = []
        self.segs: list[list[str]] = []
        self.bracket = 0

    def _skip(self) -> bool:
        return any(c & SKIP_CLASSES for c in self.stack)

    def _gap(self):
        if self.seg:
            self.segs.append(self.seg)
        self.seg = []
        self.segs.append(GAP)

    def handle_starttag(self, tag, attrs):
        cls = set((dict(attrs).get("class") or "").split())
        self.stack.append(cls)
        if "line-nr" in cls:
            self.in_nr = len(self.stack)
            self.cur_nr = ""
        if "line-body" in cls:
            self.body_depth = len(self.stack)
            self.seg, self.segs, self.bracket = [], [], 0

    def handle_endtag(self, tag):
        if self.in_nr and len(self.stack) == self.in_nr:
            self.in_nr = 0
        if self.body_depth and len(self.stack) == self.body_depth:
            self._gap()
            self.lines.append(self.segs)
            self.line_ids.append((self.cur_nr or "").strip())
            self.body_depth = 0
        self.stack.pop()

    def handle_data(self, data):
        if self.in_nr:
            self.cur_nr += data
        if not self.body_depth or self._skip():
            return
        cls = self.stack[-1] if self.stack else set()
        if "tei" in cls:                       # editorial sigla
            for ch in data:
                if ch == "[":
                    self.bracket += 1
                    self._gap()
                elif ch == "]":
                    self.bracket = max(0, self.bracket - 1)
            return
        if self.bracket:
            return
        if "scribal" in cls:                   # 'x' (illegible) or ' . ' (divider)
            if "x" in data:
                self._gap()
            elif DIVIDER in data:
                self.seg.append(DIVIDER)
            return
        i = 0
        while i < len(data):
            ch = data[i]
            if ch == "s" and data[i + 1:i + 2] == "̀":
                self.seg.append("s̀")
                i += 2
                continue
            if ch in LETTERS:
                self.seg.append(ch)
            elif ch == "x":
                self._gap()
            elif ch == DIVIDER:
                self.seg.append(DIVIDER)
            i += 1


def load_eupt(check_hash: bool = True) -> dict[str, list[tuple[str, list]]]:
    """Tablet -> [(line number, parts)]: each part is a list of letters/dividers, or GAP."""
    out = {}
    for name, sha in EUPT_PAGES.items():
        raw = (eupt_dir() / name).read_bytes()
        if check_hash and hashlib.sha256(raw).hexdigest() != sha:
            raise ValueError(f"{name}: page changed since {EUPT_ACCESSED}")
        p = _Line()
        p.feed(raw.decode("utf-8"))
        out[name.split("_facsimile")[0]] = list(zip(p.line_ids, p.lines))
    return out


def ugaritic_texts(unit: str = "segment") -> list[list[str]]:
    """Texts in reading order (left to right). unit='segment': each run of readable text between
    gaps (primary); unit='line': segments of a tablet line joined (gaps ignored)."""
    texts = []
    for lines in load_eupt().values():
        for _, parts in lines:
            segs = [_trim(s) for s in parts if s is not GAP]
            segs = [s for s in segs if any(x != DIVIDER for x in s)]
            if not segs:
                continue
            if unit == "segment":
                texts.extend(segs)
            else:
                texts.append([x for s in segs for x in s])
    return texts


def _trim(seg: list[str]) -> list[str]:
    """Drop dividers at segment edges and collapse repeated dividers."""
    out: list[str] = []
    for x in seg:
        if x == DIVIDER and (not out or out[-1] == DIVIDER):
            continue
        out.append(x)
    while out and out[-1] == DIVIDER:
        out.pop()
    return out


def recut(texts: list[list[str]], mean_len: float, seed: int = 0) -> list[list[str]]:
    """Re-cut the same token stream (in order, text by text) into texts of mean length `mean_len`
    (geometric lengths >= 1). Cuts never join two original texts."""
    rng = np.random.default_rng(seed)
    out = []
    for t in texts:
        i = 0
        while i < len(t):
            L = int(rng.geometric(1.0 / mean_len))
            out.append(t[i:i + L])
            i += L
    return [_trim(t) for t in out if any(x != DIVIDER for x in _trim(t))]


def to_corpus(texts: list[list[str]], corpus_id: str, seed: int = 0) -> tuple[Corpus, AnswerKey, dict[str, int]]:
    """Map letters to arbitrary sign IDs (seeded shuffle). Key values are Hebrew letters (GOLD);
    the divider has value DIV and s̀ has value 's2' (both unrecoverable from a Hebrew reference)."""
    letters = sorted({x for t in texts for x in t})
    rng = np.random.default_rng([seed, 7])
    ids = rng.permutation(len(letters)) + 1
    sid = {l: int(i) for l, i in zip(letters, ids)}
    def val(x: str) -> str:
        return DIV if x == DIVIDER else GOLD.get(x, "s2")
    corpus = Corpus(corpus_id, [np.array([sid[x] for x in t], dtype=np.int64) for t in texts], "ltr",
                    {"corpus_id": corpus_id, "n_texts": len(texts)})
    key = AnswerKey(corpus_id, "ugaritic", "semitic", "language", True, "alphabetic",
                    {sid[l]: [val(l)] for l in letters}, [[val(x) for x in t] for t in texts],
                    [[0] for _ in texts], {"letters": {l: sid[l] for l in letters}})
    return corpus, key, sid


def hebrew_texts(books: tuple[str, ...] | None = None) -> list[list[str]]:
    """Consonantal WLC (ketiv as written; notes, including qere readings, skipped), one text per
    verse. Points and accents stripped, final forms folded, shin/sin one letter, maqaf and
    morpheme slashes ignored. Units are Hebrew letters; no word-boundary unit."""
    ns = {"o": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
    files = sorted(p for p in oshb_dir().glob("*.xml") if p.stem != "VerseMap")
    if books:
        files = [p for p in files if p.stem in books]
    texts = []
    for p in files:
        root = ET.parse(p).getroot()
        for v in root.iter(f"{{{ns['o']}}}verse"):
            seq: list[str] = []
            for w in _words(v, ns["o"]):
                seq += _letters(w)
            if seq:
                texts.append(seq)
    return texts


def _words(el, ns: str):
    for ch in el:
        tag = ch.tag.split("}")[1]
        if tag == "note":
            continue
        if tag == "w":
            yield "".join(ch.itertext())
        else:
            yield from _words(ch, ns)


def _letters(s: str) -> list[str]:
    out = []
    for ch in s:
        ch = FINALS.get(ch, ch)
        if "א" <= ch <= "ת":
            out.append(ch)
    return out


def hebrew_words(books: tuple[str, ...] | None = None) -> dict[tuple[str, ...], int]:
    """Consonantal word types (one per <w>, prefixes included as written) with counts."""
    ns = "http://www.bibletechnologies.net/2003/OSIS/namespace"
    files = sorted(p for p in oshb_dir().glob("*.xml") if p.stem != "VerseMap")
    if books:
        files = [p for p in files if p.stem in books]
    out: dict[tuple[str, ...], int] = {}
    for p in files:
        for v in ET.parse(p).getroot().iter(f"{{{ns}}}verse"):
            for w in _words(v, ns):
                t = tuple(_letters(w))
                if t:
                    out[t] = out.get(t, 0) + 1
    return out


def ugaritic_words() -> dict[tuple[str, ...], int]:
    """Complete word types: runs of letters bounded on both sides by a divider or a line edge.
    Words touching a gap (restoration or illegible sign) are excluded as possibly incomplete."""
    out: dict[tuple[str, ...], int] = {}
    for lines in load_eupt().values():
        for _, parts in lines:
            flat = [x for p in parts for x in ([GAP] if p is GAP else p)]
            cur: list[str] = []
            ok = True                                  # left edge is a divider or the line start
            for x in flat + [DIVIDER]:
                if x is GAP:
                    cur, ok = [], False
                elif x == DIVIDER:
                    if cur and ok:
                        out[tuple(cur)] = out.get(tuple(cur), 0) + 1
                    cur, ok = [], True
                else:
                    cur.append(x)
    return out


__all__ = ["load_eupt", "ugaritic_texts", "recut", "to_corpus", "hebrew_texts", "hebrew_words", "ugaritic_words",
           "GOLD", "UNSOURCED", "POETIC_BOOKS", "EUPT_PAGES", "EUPT_BASE", "EUPT_ACCESSED", "EUPT_VERSION", "OSHB_COMMIT"]
