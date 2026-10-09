"""Exploratory (NOT pre-registered): how much of the Ugaritic-Hebrew letter-bigram distance is spelling?

Hebrew (Masoretic) spelling writes many vowels with the letters ו, י and ה (matres lectionis);
Ugaritic writes consonants only (vowels show only on the three aleph signs). This builds an
approximately "defective" Hebrew by removing vowel letters identified from the pointing:
- ו carrying holam (וֹ, holam male), or carrying only a dagesh with no vowel and not word-initial
  (וּ shureq);
- י with no point of its own, after a letter pointed hiriq, tsere or segol;
- word-final ה with no mappiq, after a letter pointed qamets, segol, tsere or holam.
The rules are approximate (no grammar is consulted). The JSD is then recomputed with the shared code.
The calibration targets are not changed by this check.

Usage: python scripts/v2/ugaritic_orthography_check.py  -> reports/v2/ugaritic/orthography_check.md
"""
from __future__ import annotations

from xml.etree import ElementTree as ET

import numpy as np

from ibdb import yardsticks as Y
from ibdb.data import ugaritic as U
from ibdb.paths import reports_dir

NS = "http://www.bibletechnologies.net/2003/OSIS/namespace"
HOLAM, DAGESH, HIRIQ, TSERE, SEGOL, QAMETS = "ֹ", "ּ", "ִ", "ֵ", "ֶ", "ָ"
POINTS = {chr(c) for c in range(0x05B0, 0x05C8)} - {"־", "׀", "׃", "׆"}


def clusters(word: str) -> list[tuple[str, set[str]]]:
    """Letters with their points (accents and other marks ignored)."""
    out: list[tuple[str, set[str]]] = []
    for ch in word:
        if "א" <= ch <= "ת":
            out.append((U.FINALS.get(ch, ch), set()))
        elif ch in POINTS and out:
            out[-1][1].add(ch)
    return out


def defective(word: str) -> list[str]:
    cl = clusters(word)
    keep = []
    for i, (l, pts) in enumerate(cl):
        prev = cl[i - 1][1] if i > 0 else set()
        vowelpts = pts - {DAGESH, "ׁ", "ׂ"}
        if l == "ו" and i > 0 and (HOLAM in pts or (pts == {DAGESH} and not cl[i - 1][1] - {DAGESH, "ׁ", "ׂ"})):
            continue
        if l == "י" and not vowelpts and DAGESH not in pts and prev & {HIRIQ, TSERE, SEGOL}:
            continue
        if l == "ה" and i == len(cl) - 1 and DAGESH not in pts and prev & {QAMETS, SEGOL, TSERE, HOLAM}:
            continue
        keep.append(l)
    return keep


def hebrew(defect: bool, books=None) -> list[list[str]]:
    files = sorted(p for p in U.oshb_dir().glob("*.xml") if p.stem != "VerseMap")
    if books:
        files = [p for p in files if p.stem in books]
    texts = []
    for p in files:
        for v in ET.parse(p).getroot().iter(f"{{{NS}}}verse"):
            seq: list[str] = []
            for w in U._words(v, NS):
                w = w.replace("/", "")
                seq += defective(w) if defect else U._letters(w)
            if seq:
                texts.append(seq)
    return texts


def hebrew_word_set(defect: bool) -> set[str]:
    out = set()
    for p in sorted(q for q in U.oshb_dir().glob("*.xml") if q.stem != "VerseMap"):
        for v in ET.parse(p).getroot().iter(f"{{{NS}}}verse"):
            for w in U._words(v, NS):
                t = defective(w.replace("/", "")) if defect else U._letters(w)
                if t:
                    out.add("".join(t))
    return out


def main() -> None:
    seg = U.ugaritic_texts("segment")
    letters = [[U.GOLD[x] for x in t if x != U.DIVIDER] for t in seg]
    full, defe = hebrew(False), hebrew(True)
    assert full == U.hebrew_texts(), "plene text must equal the anchor's Hebrew"
    rng = np.random.default_rng(0)
    n = sum(map(len, letters))
    rows = []
    for name, h in (("Hebrew as written (anchor)", full), ("Hebrew, vowel letters removed (approx.)", defe)):
        j = Y.bigram_jsd(letters, h)
        fl = float(np.mean([Y.bigram_jsd(Y.sample_texts(h, n, rng), h) for _ in range(20)]))
        share = {l: sum(t.count(l) for t in h) / sum(map(len, h)) for l in ("ו", "י", "ה")}
        rows.append((name, sum(map(len, h)), j, fl, j - fl, share))
    ug = {l: sum(t.count(l) for t in letters) / n for l in ("ו", "י", "ה")}
    # Verbatim (6+ letters) and shared word forms against both spellings, chance from shuffled maps.
    uw = U.ugaritic_words()
    gm = lambda m, t: "".join(m[x] for x in t if x != U.DIVIDER)  # noqa: E731
    r2 = np.random.default_rng(0)
    shuf = [Y.shuffled_mapping(U.GOLD, r2) for _ in range(50)]
    extra = []
    for name, h, words in (("as written", full, {"".join(w) for w in U.hebrew_words()}),
                           ("vowel letters removed", defe, hebrew_word_set(True))):
        blob = "|".join("".join(t) for t in h)
        v = Y.verbatim((gm(U.GOLD, t) for t in seg), blob, 6)
        vc = float(np.mean([Y.verbatim((gm(m, t) for t in seg), blob, 6) for m in shuf]))
        wm = lambda m: (lambda w: "".join(m[x] for x in w))  # noqa: E731
        ct = Y.overlap(uw, words, wm(U.GOLD))[0]
        cc = float(np.mean([Y.overlap(uw, words, wm(m))[0] for m in shuf]))
        extra.append((name, v, vc, ct, cc, Y.chance_corrected(ct, cc)))
    L = ["# Exploratory check (NOT pre-registered): spelling share of the Ugaritic-Hebrew distance", "",
         "Calibration targets are unchanged by this check. Vowel-letter removal is approximate (rules in the script).", "",
         "| Hebrew text | Letters | JSD to Ugaritic (bits) | Same-size floor | JSD above floor | Share of ו / י / ה |", "|---|---|---|---|---|---|"]
    for name, nl, j, fl, a, sh in rows:
        L.append(f"| {name} | {nl:,} | {j:.3f} | {fl:.3f} | {a:.3f} | {100 * sh['ו']:.1f}% / {100 * sh['י']:.1f}% / {100 * sh['ה']:.1f}% |")
    L += ["", f"Ugaritic (gold-mapped) share of ו / י / ה: {100 * ug['ו']:.1f}% / {100 * ug['י']:.1f}% / {100 * ug['ה']:.1f}%.", ""]
    L += ["| Hebrew spelling | Verbatim 6+ letters (chance) | Shared word forms (chance) | Chance-corrected |", "|---|---|---|---|"]
    for name, v, vc, ct, cc, c in extra:
        L.append(f"| {name} | {100 * v:.1f}% ({100 * vc:.2f}%) | {100 * ct:.1f}% ({100 * cc:.1f}%) | {100 * c:.1f}% |")
    L.append("")
    (reports_dir() / "v2" / "ugaritic" / "orthography_check.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
