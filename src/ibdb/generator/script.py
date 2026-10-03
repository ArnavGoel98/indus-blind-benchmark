"""Fake-script definition: map plaintext units to invented sign IDs.

Supported script types
----------------------
alphabetic    one unit per phoneme (control: inventory far below Indus)
syllabic      CV / V / C units (see ibdb.phonology.syllabify)
logographic   one unit per word form
logosyllabic  the ``logogram_vocab`` most frequent words get logograms, other words are
              spelled syllabically, optional determinatives
emblem        non-linguistic controls: one unit per visual/administrative element

Writing-system phenomena (each a rate in [0, 1])
-------------------------------------------------
allographs    graphic variants of one value, chosen per TOKEN, base form dominant
              (variant j has weight 1/(j+1)^2); the main inventory and hapax knob
homophony     one value written with 2-3 different signs, chosen per WORD (lexically
              conditioned, like Sumerian du / du3)
polyvalence   one sign carries a second, unrelated value
determinatives unpronounced classifier sign before words of selected semantic classes
word divider  a sign after every word except the last
direction     texts stored in physical order; 'rtl' means the reading order is reversed
"""

from __future__ import annotations

import zlib
from collections import Counter
from dataclasses import asdict, dataclass, field
from typing import Any

import numpy as np

SCRIPT_TYPES = ("logographic", "syllabic", "logosyllabic", "alphabetic")
DIV = "<DIV>"


def stable_hash(*parts: Any) -> int:
    return zlib.crc32("\x1f".join(map(str, parts)).encode("utf-8"))


@dataclass
class ScriptSpec:
    script_type: str = "syllabic"
    allograph_rate: float = 0.25
    allograph_extra_mean: float = 2.0
    homophony_rate: float = 0.10
    polyvalence_rate: float = 0.05
    determinatives: bool = False
    word_divider: bool = False
    direction: str = "rtl"
    logogram_vocab: int = 250
    sem_rate: float = 0.30        # languages without semantic annotation: share of word types given a class
    n_sem_classes: int = 8

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Script:
    """A concrete script instance: value->signs tables plus the per-word spellings."""

    spec: ScriptSpec
    seed: int
    value_signs: dict[str, list[int]] = field(default_factory=dict)     # value -> [base, homophones...]
    allographs: dict[int, list[int]] = field(default_factory=dict)      # sign -> [sign, variants...]
    sign_values: dict[int, list[str]] = field(default_factory=dict)
    det_signs: dict[int, int] = field(default_factory=dict)
    divider: int | None = None

    def all_signs(self) -> set[int]:
        return set(self.sign_values)


def word_units(word: list, spec: ScriptSpec, logograms: set[int], wid: int) -> list[str]:
    """Units a word is spelled with (before signs are chosen). word = [form, phon, syl, sem]."""
    form, phon, syl, _ = word
    st = spec.script_type
    if st == "alphabetic":
        return list(phon)
    if st == "syllabic":
        return list(syl)
    if st in ("logographic", "emblem"):
        return [form]
    if st == "logosyllabic":
        return [form] if wid in logograms else list(syl)
    raise ValueError(st)


def word_sem(word: list, spec: ScriptSpec, seed: int, language: str) -> int | None:
    """Semantic class for determinatives.

    Sanskrit (DCS WordSem buckets) and Sumerian (real determinatives) carry annotated
    classes. For the other languages a seeded hash gives ``sem_rate`` of word types one of
    ``n_sem_classes`` classes. That is a simplification: real determinatives track meaning.
    """
    if word[3] is not None:
        return int(word[3]) % max(spec.n_sem_classes, 1)
    h = stable_hash("sem", seed, language, word[0])
    if (h % 1000) / 1000.0 < spec.sem_rate:
        return (h // 1000) % spec.n_sem_classes
    return None


class IdPool:
    """Unique random sign IDs from a large space: IDs carry no information about values."""

    def __init__(self, rng: np.random.Generator, low: int = 100, high: int = 1_000_000):
        self.rng, self.low, self.high, self.used = rng, low, high, set()

    def __iter__(self):
        return self

    def __next__(self) -> int:
        while True:
            x = int(self.rng.integers(self.low, self.high))
            if x not in self.used:
                self.used.add(x)
                return x


def build_script(values: Counter, spec: ScriptSpec, rng: np.random.Generator, seed: int,
                 sem_classes: set[int]) -> Script:
    """Create sign tables for the given unit values (Counter of token counts)."""
    sc = Script(spec=spec, seed=seed)
    ordered = [v for v, _ in sorted(values.items(), key=lambda kv: (-kv[1], kv[0]))]
    n_vals = len(ordered)
    id_pool = IdPool(rng)

    for v in ordered:
        signs = [next(id_pool)]
        if rng.random() < spec.homophony_rate:
            signs += [next(id_pool) for _ in range(int(rng.integers(1, 3)))]
        sc.value_signs[v] = signs
        for s in signs:
            sc.sign_values[s] = [v]

    # Polyvalence: a sign takes over a second value (that value loses its own base sign).
    if spec.polyvalence_rate > 0 and n_vals > 2:
        n_poly = int(round(spec.polyvalence_rate * n_vals))
        donors = rng.choice(n_vals, size=min(n_poly, n_vals // 2), replace=False)
        for i in donors:
            v1 = ordered[i]
            v2 = ordered[int(rng.integers(n_vals))]
            if v2 == v1 or len(sc.sign_values.get(sc.value_signs[v1][0], [])) > 1:
                continue
            s = sc.value_signs[v1][0]
            old = sc.value_signs[v2][0]
            if len(sc.sign_values.get(old, [])) > 1:
                continue
            sc.value_signs[v2][0] = s
            sc.sign_values[s] = sc.sign_values[s] + [v2]
            sc.sign_values.pop(old, None)

    # Allographs: per-sign graphic variants, chosen per token.
    for s in list(sc.sign_values):
        if rng.random() < spec.allograph_rate:
            k = 1 + int(rng.poisson(max(spec.allograph_extra_mean - 1.0, 0.0)))
            variants = [next(id_pool) for _ in range(k)]
            sc.allographs[s] = [s] + variants
            for vs in variants:
                sc.sign_values[vs] = list(sc.sign_values[s])

    if spec.determinatives:
        for c in sorted(sem_classes):
            s = next(id_pool)
            sc.det_signs[c] = s
            sc.sign_values[s] = [f"<DET:{c}>"]
    if spec.word_divider:
        sc.divider = next(id_pool)
        sc.sign_values[sc.divider] = [DIV]
    return sc


_ALLO_W: dict[int, np.ndarray] = {}


def _allo_probs(k: int) -> np.ndarray:
    if k not in _ALLO_W:
        w = 1.0 / (np.arange(k) + 1.0) ** 2
        _ALLO_W[k] = w / w.sum()
    return _ALLO_W[k]


def spell_word(sc: Script, form: str, units: list[str], sem: int | None,
               rng: np.random.Generator) -> tuple[list[int], list[str]]:
    """Signs and per-token values for one word occurrence."""
    signs: list[int] = []
    vals: list[str] = []
    if sem is not None and sc.spec.determinatives and sem in sc.det_signs:
        signs.append(sc.det_signs[sem])
        vals.append(f"<DET:{sem}>")
    for u in units:
        options = sc.value_signs[u]
        base = options[stable_hash("homo", sc.seed, form, u) % len(options)] if len(options) > 1 else options[0]
        allo = sc.allographs.get(base)
        if allo is not None:
            base = allo[int(rng.choice(len(allo), p=_allo_probs(len(allo))))]
        signs.append(base)
        vals.append(u)
    return signs, vals
