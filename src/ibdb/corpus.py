"""Public corpus and private answer key.

A ``Corpus`` is what a method (or a challenge participant) sees: sign-ID sequences plus
public metadata. An ``AnswerKey`` holds everything hidden: source language, family, script
type, the value of each sign and of each token, word boundaries, and the generator settings.
Keys are written only under ``private/`` (git-ignored).
"""

from __future__ import annotations

import gzip
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

PUBLIC_META_KEYS = ("corpus_id", "n_texts", "direction", "tier", "notes")


@dataclass
class Corpus:
    corpus_id: str
    texts: list[np.ndarray]          # physical left-to-right order, int sign IDs
    direction: str = "rtl"           # 'rtl' or 'ltr'; public, as for the real Indus corpus
    meta: dict[str, Any] = field(default_factory=dict)

    def logical(self) -> list[np.ndarray]:
        """Texts in reading order."""
        if self.direction == "rtl":
            return [t[::-1] for t in self.texts]
        return list(self.texts)

    @property
    def n_tokens(self) -> int:
        return int(sum(len(t) for t in self.texts))

    def to_jsonable(self) -> dict[str, Any]:
        return {"corpus_id": self.corpus_id, "direction": self.direction,
                "meta": {k: v for k, v in self.meta.items() if k in PUBLIC_META_KEYS},
                "texts": [" ".join(map(str, t.tolist())) for t in self.texts]}

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "wt", encoding="utf-8") as fh:
            json.dump(self.to_jsonable(), fh)

    @classmethod
    def load(cls, path: Path) -> "Corpus":
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as fh:
            d = json.load(fh)
        texts = [np.array([int(x) for x in s.split()], dtype=np.int64) for s in d["texts"]]
        return cls(d["corpus_id"], texts, d.get("direction", "ltr"), d.get("meta", {}))


@dataclass
class AnswerKey:
    corpus_id: str
    source: str
    family: str
    kind: str                         # language | structural | adversarial | trivial | nl_derived
    is_linguistic: bool
    script_type: str                  # logographic | syllabic | logosyllabic | alphabetic | emblem
    sign_values: dict[int, list[str]]
    token_values: list[list[str]]     # reading order
    word_starts: list[list[int]]      # reading-order indices where a word starts
    params: dict[str, Any] = field(default_factory=dict)
    plaintext: list[str] = field(default_factory=list)

    def save(self, path: Path) -> str:
        """Write the key; return its SHA-256 (published as a commitment for hidden corpora)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        d = asdict(self)
        d["sign_values"] = {str(k): v for k, v in self.sign_values.items()}
        blob = json.dumps(d, ensure_ascii=False, sort_keys=True).encode("utf-8")
        path.write_bytes(gzip.compress(blob, mtime=0))
        return hashlib.sha256(blob).hexdigest()

    @classmethod
    def load(cls, path: Path) -> "AnswerKey":
        d = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        d["sign_values"] = {int(k): v for k, v in d["sign_values"].items()}
        return cls(**d)
