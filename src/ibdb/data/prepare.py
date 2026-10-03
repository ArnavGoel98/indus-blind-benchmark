"""Parse raw sources into a lexicon plus "clauses" (short seal-like segments).

The output for each source is ``data/segments/<name>.json.gz``:

    {
      "name": ..., "family": ..., "is_linguistic": bool, "kind": "language" | "nl_derived",
      "words":   [[form, [phonemes], [syllables], sem_class], ...],   # lexicon, indexed by id
      "clauses": [[kind, [word_id, ...]], ...],
    }

Clause kinds aim at genres close to what seals carry:

* ``name`` / ``epithet``: personal names, titles, epithets (Sanskrit nominal runs, Tamil
  poet colophons, Latin capitalized runs)
* ``seal``: real Sumerian seal inscriptions (CDLI @seal sections)
* ``formula``: formulaic headers (Tamil tinai/speaker rubrics)
* ``line`` / ``clause``: verse lines and punctuation-delimited clauses, used as fallback and
  for long-text sweeps

The generator samples contiguous word windows from these clauses, so a clause is an upper
bound on a text, not a text itself.
"""

from __future__ import annotations

import gzip
import html
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from .. import config, phonology
from ..paths import ensure, raw_dir, segments_dir


class Builder:
    def __init__(self, name: str, family: str, is_linguistic: bool = True, kind: str = "language"):
        self.name = name
        self.family = family
        self.is_linguistic = is_linguistic
        self.kind = kind
        self.word_ids: dict[str, int] = {}
        self.words: list[list] = []
        self.clauses: list[list] = []

    def word(self, form: str, phon: list[str], syl: list[str], sem: int | str | None = None) -> int | None:
        if not form or not syl:
            return None
        wid = self.word_ids.get(form)
        if wid is None:
            wid = len(self.words)
            self.word_ids[form] = wid
            self.words.append([form, phon, syl, sem])
        elif sem is not None and self.words[wid][3] is None:
            self.words[wid][3] = sem
        return wid

    def clause(self, kind: str, ids: Iterable[int | None]) -> None:
        ids = [i for i in ids if i is not None]
        if ids:
            self.clauses.append([kind, ids])

    def save(self) -> Path:
        # Map string semantic classes to small ints for compactness.
        sem_map: dict = {}
        for w in self.words:
            if w[3] is not None and not isinstance(w[3], int):
                w[3] = sem_map.setdefault(w[3], len(sem_map))
        out = ensure(segments_dir()) / f"{self.name}.json.gz"
        payload = {"name": self.name, "family": self.family, "is_linguistic": self.is_linguistic,
                   "kind": self.kind, "words": self.words, "clauses": self.clauses,
                   "sem_classes": {str(v): k for k, v in sem_map.items()}}
        with gzip.open(out, "wt", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False)
        return out


def _lang_word(b: Builder, lang: str, form: str, sem=None) -> int | None:
    ph, syl = phonology.word_units(lang, form)
    return b.word(form, ph, syl, sem)


# --------------------------------------------------------------------------- Sanskrit (DCS)

_NOMINAL = {"NOUN", "PROPN", "ADJ", "NUM"}


def prepare_sanskrit() -> Builder:
    b = Builder("sanskrit", config.sources()["languages"]["sanskrit"]["family"])
    root = raw_dir() / "sanskrit" / "repo"
    files = sorted(root.rglob("*.conllu"))
    if not files:
        raise FileNotFoundError("run `ibdb fetch sanskrit` first")
    for f in files:
        sent: list[tuple[str, str, int | None]] = []
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                _flush_skt(b, sent)
                sent = []
                continue
            if line.startswith("#"):
                continue
            cols = line.split("\t")
            if len(cols) < 10 or "-" in cols[0] or "." in cols[0]:
                continue
            misc = dict(kv.split("=", 1) for kv in cols[9].split("|") if "=" in kv)
            form = phonology.normalize_sanskrit(misc.get("Unsandhied", cols[1]))
            sem = None
            if cols[3] in ("NOUN", "PROPN") and "WordSem" in misc:
                sem = f"ws{int(misc['WordSem'].split(',')[0]) % 12}"
            sent.append((form, cols[3], sem))
        _flush_skt(b, sent)
    return b


def _flush_skt(b: Builder, sent: list[tuple[str, str, int | None]]) -> None:
    if not sent:
        return
    ids = [_lang_word(b, "sanskrit", f, s) for f, _, s in sent]
    b.clause("line", ids)
    run: list[int | None] = []
    for wid, (_, pos, _) in zip(ids, sent):
        if pos in _NOMINAL:
            run.append(wid)
        else:
            if run:
                b.clause("epithet", run)
            run = []
    if run:
        b.clause("epithet", run)


# --------------------------------------------------------------------------- Tamil (Project Madurai)

_TAG = re.compile(r"<[^>]+>")
_TA_TOKEN = re.compile(r"[஀-௿]+")


def _html_lines(path: Path) -> list[str]:
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
    t = html.unescape(_TAG.sub(" ", t)).replace("\xa0", " ")
    return [ln.strip() for ln in t.splitlines() if ln.strip()]


def prepare_tamil() -> Builder:
    b = Builder("tamil", config.sources()["languages"]["tamil"]["family"])
    files = sorted((raw_dir() / "tamil").glob("pmuni*.html"))
    if not files:
        raise FileNotFoundError("run `ibdb fetch tamil` first")
    for f in files:
        lines = _html_lines(f)
        start = next((i for i, ln in enumerate(lines) if "freely distribute" in ln), 0) + 1
        for ln in lines[start:]:
            if not phonology.is_tamil_word(ln):
                continue
            kind = "line"
            s = ln
            if s.startswith("-"):
                kind = "name"  # poet colophon, e.g. "-திப்புத் தோளார்."
            elif re.match(r"^\d+\s*\.", s):
                kind = "formula"  # rubric, e.g. "1. குறிஞ்சி - தோழி கூற்று"
            toks = _TA_TOKEN.findall(s)
            ids = [_lang_word(b, "tamil", t) for t in toks]
            b.clause(kind, ids)
    return b


# --------------------------------------------------------------------------- Sumerian (CDLI ATF)

_ATF_LINE = re.compile(r"^(\d+'*)\.\s+(.*)$")


def prepare_sumerian(max_tablet_lines: int = 250_000) -> Builder:
    b = Builder("sumerian", config.sources()["languages"]["sumerian"]["family"])
    path = raw_dir() / "sumerian" / "cdliatf_unblocked.atf"
    if not path.exists():
        raise FileNotFoundError("run `ibdb fetch sumerian` first")
    lang = None
    in_seal = False
    seal_ids: list[int] = []
    n_lines = 0

    def close_seal():
        nonlocal seal_ids
        if seal_ids:
            b.clause("seal", seal_ids)
        seal_ids = []

    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.startswith("&"):
                close_seal()
                lang, in_seal = None, False
                continue
            if line.startswith("#atf:") and "lang" in line:
                rest = line.split("lang", 1)[1].split()
                lang = rest[0] if rest else None
                continue
            if line.startswith("@"):
                close_seal()
                in_seal = line.startswith("@seal")
                continue
            if lang is None or not lang.startswith("sux"):
                continue
            m = _ATF_LINE.match(line)
            if not m:
                continue
            words = []
            ok = True
            for tok in m.group(2).split():
                if tok.startswith("($") or tok in ("|", "/"):
                    continue
                parsed = phonology.sumerian_word(tok)
                if parsed is None:
                    ok = False
                    break
                readings, syl, det = parsed
                form = "-".join(readings)
                words.append(b.word(form, phonology.sumerian_phonemes(syl), syl, det))
            if not ok or not words:
                if in_seal:
                    seal_ids = []  # damaged seal: drop rather than splice fragments
                continue
            if in_seal:
                seal_ids.extend(w for w in words if w is not None)
            elif n_lines < max_tablet_lines:
                b.clause("line", words)
                n_lines += 1
    close_seal()
    return b


# --------------------------------------------------------------------------- Gutenberg (Latin, Finnish)


def _gutenberg_body(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="replace")
    s = re.search(r"\*\*\* ?START OF.*?\*\*\*", t)
    e = re.search(r"\*\*\* ?END OF", t)
    return t[s.end() if s else 0: e.start() if e else len(t)]


def prepare_latin() -> Builder:
    b = Builder("latin", config.sources()["languages"]["latin"]["family"])
    files = sorted((raw_dir() / "latin").glob("pg*.txt"))
    if not files:
        raise FileNotFoundError("run `ibdb fetch latin` first")
    for f in files:
        body = _gutenberg_body(f)
        for clause in re.split(r"[.;:,!?()\[\]\n]{1}\s*(?=[A-Za-z])|[.;:!?]\s+", body.replace("\r", "")):
            toks = clause.split()
            if not toks or len(toks) > 30:
                continue
            ids = [_lang_word(b, "latin", phonology.normalize_latin(t)) for t in toks]
            b.clause("clause", ids)
            if f.name != "pg218.txt":
                continue  # verse capitalizes every line; only mine names from Caesar's prose
            # Capitalized runs after the first token: names and titles (C. Iulius Caesar, ...)
            run: list[int | None] = []
            for t, wid in list(zip(toks, ids))[1:]:
                if t[:1].isupper():
                    run.append(wid)
                else:
                    if len(run) >= 1:
                        b.clause("name", run)
                    run = []
            if run:
                b.clause("name", run)
    return b


def prepare_finnish() -> Builder:
    b = Builder("finnish", config.sources()["languages"]["finnish"]["family"])
    files = sorted((raw_dir() / "finnish").glob("pg*.txt"))
    if not files:
        raise FileNotFoundError("run `ibdb fetch finnish` first")
    for f in files:
        for line in _gutenberg_body(f).splitlines():
            toks = line.split()
            if not toks or len(toks) > 8:
                continue
            ids = [_lang_word(b, "finnish", phonology.normalize_finnish(t)) for t in toks]
            b.clause("line", ids)
    return b


# --------------------------------------------------------------------------- Kamon (NL-derived control)


def prepare_kamon() -> Builder:
    b = Builder("kamon", "none (Japanese description)", is_linguistic=False, kind="nl_derived")
    path = raw_dir() / "kamon" / "synthetic_examples.zip"
    if not path.exists():
        raise FileNotFoundError("run `ibdb fetch kamon` first")
    with zipfile.ZipFile(path) as z:
        with z.open("synthetic_examples/synthetic_parsed.jsonl") as fh:
            for raw in fh:
                rec = json.loads(raw)
                exprs = [a["expr"] for a in rec.get("analysis", []) if a.get("expr")]
                ids = [b.word(e, list(e), [e]) for e in exprs]
                b.clause("description", ids)
    return b


PREPARERS = {
    "sanskrit": prepare_sanskrit,
    "tamil": prepare_tamil,
    "sumerian": prepare_sumerian,
    "latin": prepare_latin,
    "finnish": prepare_finnish,
    "kamon": prepare_kamon,
}


def prepare(names: list[str] | None = None, log=print) -> dict[str, dict]:
    report: dict[str, dict] = {}
    for name, fn in PREPARERS.items():
        if names and name not in names:
            continue
        b = fn()
        path = b.save()
        kinds: dict[str, int] = defaultdict(int)
        for k, _ in b.clauses:
            kinds[k] += 1
        n_tokens = sum(len(c) for _, c in b.clauses)
        report[name] = {"words": len(b.words), "clauses": len(b.clauses), "tokens_in_clauses": n_tokens,
                        "clause_kinds": dict(kinds), "path": str(path)}
        log(f"[prepare] {name}: {len(b.words)} word types, {len(b.clauses)} clauses {dict(kinds)}")
    return report


def load_segments(name: str) -> dict:
    with gzip.open(segments_dir() / f"{name}.json.gz", "rt", encoding="utf-8") as fh:
        return json.load(fh)
