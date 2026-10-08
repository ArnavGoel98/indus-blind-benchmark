"""Sproat's non-linguistic symbol corpora (held-out control family; used with the author's permission).

Source: richardsproat.com/data/non-linguistic-symbols (corpora.zip). Cite Sproat (2014) and
Wu, Solman, Linehan & Sproat (2012). The XML files carry an Apache 2.0 header.

Linearisation follows Sproat's own tools/xtract.py with its default options (one text per
<document>, symbol titles in document order, spaces inside a title replaced by '_', '>' removed
except where his README says to use --raw). This is a Python 3 port of that logic, not new rules.
"""

from __future__ import annotations

import xml.sax
import xml.sax.handler
from pathlib import Path

import numpy as np

from ..corpus import Corpus
from ..paths import raw_dir

# Systems used as the held-out control family. IndusBarSeals is the Indus script itself (its status
# is the open question), so it is never a control. Pictish is kept but reported separately because
# its status is disputed (Lee, Jonathan & Ziman 2010 argue it is writing).
SYSTEMS = ["Vinca", "Kudurrus", "BarnStars", "TotemPoles", "WeatherIcons", "AsianEmoticons", "Pictish"]
EXCLUDED = {"IndusBarSeals": "Indus script itself; its status is what is being tested"}
DISPUTED = {"Pictish"}
RAW = {"AsianEmoticons"}   # per Sproat's corpora/README: "Use tools/xtract.py --raw"


class _Handler(xml.sax.handler.ContentHandler):
    """Port of xtract.py XmlHandler (default options)."""

    def __init__(self, clean: bool):
        super().__init__()
        self.docs: list[list[str]] = []
        self.text: list[str] = []
        self.this = ""
        self.in_desc = self.in_symbol = self.in_title = False
        self.clean = clean

    def startElement(self, name, attrs):
        if name == "description":
            self.in_desc = True
        elif name == "symbol":
            self.in_symbol = True
        elif name == "title" and self.in_symbol:
            self.this = ""
            self.in_title = True

    def characters(self, data):
        if self.in_symbol and self.in_title and not self.in_desc:
            s = data.strip().replace(" ", "_")
            self.this += s.replace(">", "") if self.clean else s

    def endElement(self, name):
        if name == "description":
            self.in_desc = False
        elif name == "document":
            if self.text:
                self.docs.append(self.text)
            self.text = []
        elif name == "symbol":
            self.in_symbol = False
        elif name == "title" and self.in_symbol:
            if self.this:
                self.text.append(self.this)
                self.this = ""
            self.in_title = False


def corpora_dir() -> Path:
    """Extracted corpora; unpacks the fetched corpora.zip (``ibdb fetch sproat_nonling``) on first use."""
    d = raw_dir() / "sproat_nonling" / "corpora"
    if not d.exists():
        import zipfile
        with zipfile.ZipFile(d.parent / "corpora.zip") as z:
            z.extractall(d.parent)
    return d


def load_texts(system: str) -> list[list[str]]:
    if system in EXCLUDED:
        raise ValueError(f"{system} is excluded: {EXCLUDED[system]}")
    h = _Handler(clean=system not in RAW)
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_external_ges, False)
    parser.setContentHandler(h)
    parser.parse(str(corpora_dir() / f"{system}.xml"))
    return h.docs


def to_corpus(system: str, texts: list[list[str]], tag: str = "native") -> Corpus:
    """Symbols -> integer IDs in first-seen order. Direction 'ltr': texts are already in the
    order Sproat's tool emits them, so logical() returns them unchanged."""
    ids: dict[str, int] = {}
    arr = [np.array([ids.setdefault(s, len(ids)) for s in t], dtype=np.int64) for t in texts]
    return Corpus(f"sproat-{system}-{tag}", arr, "ltr", {"n_texts": len(arr)})


def indus_size_samples(texts: list[list[str]], n_texts: int, seeds: list[int]) -> list[list[list[str]]]:
    """Samples of n_texts whole texts, drawn without replacement. Only possible when the system
    has at least n_texts texts; nothing is padded, split or resampled with replacement."""
    if len(texts) < n_texts:
        return []
    out = []
    for s in seeds:
        idx = np.random.default_rng([20261008, s]).choice(len(texts), n_texts, replace=False)
        out.append([texts[i] for i in sorted(idx)])
    return out
