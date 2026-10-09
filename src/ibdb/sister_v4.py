"""v2 method data: a realistic synthetic sister language (sister-v4). Plan: docs/v2_sister_plan.md.

Built from the reference half of the source text (as the v1 sister), at the phoneme level. Every
change is regular: it depends only on the word type and its phonemes, never on the token, so the
sister behaves like a real relative rather than like noise.

Mechanisms (knobs in `Knobs`; the merger share and shift rate are fixed by the plan):
1. Mergers: round(0.24 * |consonants|) hidden consonants merge into another consonant. Pairs that
   share a base letter (t/ṭ, b/bh, s/ś) are taken first, then random pairs.
2. Unconditioned shift: a bijective permutation of the remaining consonants and of the vowels
   (rate 0.30, as v1).
   The REGULAR REFLEX of a hidden phoneme is shift(merge(phoneme)).
3. Conditioned changes: n_cond rules "X -> Y / context" (before a given vowel, between vowels,
   word-initially, word-finally). Where a rule applies, X becomes Y instead of its regular reflex.
4. Final-vowel loss in a share of word types.
5. Morphology: the most frequent word-final (30) and word-initial (20) phoneme strings of 1-3
   phonemes are affix candidates; a share of them is replaced, in every word that carries them,
   by a new string of the same consonant/vowel pattern.
6. Lexical replacement: a share of word types is replaced by another word of the same length.
7. Word order: a share of clauses changes order (half move the last word to the front, half swap
   one adjacent pair).

Gold for scoring (docs/v2_preregistration.md, entry 2): `regular` (hidden phoneme -> regular
reflex) and `attested` (hidden phoneme -> every sister phoneme it became through the sound changes,
counted in the sister text). Affix and lexical replacements are not reflexes.
"""

from __future__ import annotations

import unicodedata
import zlib
from collections import Counter
from dataclasses import asdict, dataclass, field
from functools import lru_cache

import numpy as np

from . import phonology
from .generator.build import _segments, base_source

MERGER_SHARE = 0.24        # Ugaritic-Hebrew: 7 mergers among 29 letters
SHIFT_RATE = 0.30          # as the v1 sister
MAX_CLAUSES = 40_000       # as knowledge.MAX_REF_CLAUSES
N_SUFFIX, N_PREFIX = 30, 20
CONTEXTS = ("before_vowel", "between_vowels", "initial", "final")


@dataclass(frozen=True)
class Knobs:
    n_cond: int = 0
    affix_share: float = 0.0
    lexical: float = 0.2
    word_order: float = 0.0
    final_vowel_loss: float = 0.0


@dataclass
class Sister:
    lang: str
    seed: int
    knobs: Knobs
    clauses: list[list[tuple[str, ...]]]        # sister clauses as word phoneme tuples (word order changed)
    word_ids: list[list[int]]                   # source word id per sister word (after lexical replacement)
    regular: dict[str, str]
    attested: dict[str, Counter]
    mergers: dict[str, str]
    rules: list[tuple[str, str, str, str | None]] = field(default_factory=list)  # (X, Y, context, vowel)
    affixes: dict[str, dict[tuple[str, ...], tuple[str, ...]]] = field(default_factory=dict)

    def texts(self) -> list[list[str]]:
        return [[p for w in c for p in w] for c in self.clauses]

    def summary(self) -> dict:
        return {"lang": self.lang, "seed": self.seed, "knobs": asdict(self.knobs), "n_mergers": len(self.mergers),
                "mergers": self.mergers, "rules": self.rules,
                "n_suffix_replaced": len(self.affixes.get("suffix", {})),
                "n_prefix_replaced": len(self.affixes.get("prefix", {}))}


def _base(g: str) -> str:
    b = "".join(c for c in unicodedata.normalize("NFD", g) if not unicodedata.combining(c))
    return b[:-1] if len(b) > 1 and b.endswith("h") else b


def _split(lang: str, d: dict, half: str) -> list:
    """Content-based half split (sister-v2/v3 rule), independent of IBDB_SISTER_VERSION."""
    want = 0 if half == "hidden" else 1
    return [c for c in d["clauses"]
            if zlib.crc32(f"{base_source(lang)}:{' '.join(map(str, c[1]))}".encode()) % 2 == want]


def _rng(lang: str, seed: int, tag: int) -> np.random.Generator:
    return np.random.default_rng([seed, tag, zlib.crc32(lang.encode())])


@lru_cache(maxsize=8)
def _source(lang: str):
    d = _segments(lang)
    clauses = _split(lang, d, "reference")[:MAX_CLAUSES]
    phon = [tuple(w[1]) for w in d["words"]]
    return d, clauses, phon


def mergers_for(lang: str, freq: Counter, seed: int, share: float = MERGER_SHARE) -> dict[str, str]:
    """source consonant -> target consonant; disjoint (no target is also a source)."""
    prof = phonology.PROFILES[lang]
    C = sorted(prof.consonants)
    m = int(round(share * len(C)))
    rng = _rng(lang, seed, 1)
    near = [(a, b) for i, a in enumerate(C) for b in C[i + 1:] if _base(a) == _base(b)]
    near = [near[i] for i in rng.permutation(len(near))]
    far = [(a, b) for i, a in enumerate(C) for b in C[i + 1:] if _base(a) != _base(b)]
    far = [far[i] for i in rng.permutation(len(far))]
    out: dict[str, str] = {}
    used: set[str] = set()
    for a, b in near + far:
        if len(out) >= m:
            break
        if a in used or b in used:
            continue
        tgt, src = (a, b) if freq[a] >= freq[b] else (b, a)
        out[src] = tgt
        used.update((a, b))
    return out


def _shift(lang: str, inventory: list[str], seed: int, tag: int) -> dict[str, str]:
    rng = _rng(lang, seed, tag)
    n = int(round(SHIFT_RATE * len(inventory)))
    if n < 2:
        return {}
    chosen = [str(x) for x in rng.choice(inventory, size=n, replace=False)]
    return dict(zip(chosen, chosen[1:] + chosen[:1]))


def _context_ok(ctx: str, word: tuple[str, ...], i: int, vowels, vowel: str | None) -> bool:
    if ctx == "initial":
        return i == 0
    if ctx == "final":
        return i == len(word) - 1
    nxt = word[i + 1] if i + 1 < len(word) else None
    if ctx == "before_vowel":
        return nxt == vowel
    prv = word[i - 1] if i > 0 else None
    return prv in vowels and nxt in vowels          # between_vowels


def build(lang: str, seed: int, knobs: Knobs, merger_share: float = MERGER_SHARE) -> Sister:
    d, clauses, phon = _source(lang)
    prof = phonology.PROFILES[lang]
    V, Cset = prof.vowels, prof.consonants
    used = sorted({w for _, ids in clauses for w in ids})
    freq = Counter(p for _, ids in clauses for w in ids for p in phon[w])

    # 1-2. Regular reflexes.
    merg = mergers_for(lang, freq, seed, merger_share)
    remaining = sorted(c for c in Cset if c not in merg)
    shift = {**_shift(lang, remaining, seed, 2), **_shift(lang, sorted(V), seed, 3)}
    regular = {p: shift.get(merg.get(p, p), merg.get(p, p)) for p in sorted(Cset | V)}
    reg = lambda p: regular.get(p, p)  # noqa: E731

    # 3. Conditioned rules (one per X; X never a merger source).
    rng = _rng(lang, seed, 4)
    cands = [c for c, _ in freq.most_common() if c in Cset and c not in merg]
    sister_cons = sorted({reg(c) for c in Cset})
    rules: list[tuple[str, str, str, str | None]] = []
    for X in cands[: knobs.n_cond]:
        ctx = CONTEXTS[int(rng.integers(len(CONTEXTS)))]
        vowel = sorted(V)[int(rng.integers(len(V)))] if ctx == "before_vowel" else None
        Ys = [y for y in sister_cons if y != reg(X)]
        rules.append((X, Ys[int(rng.integers(len(Ys)))], ctx, vowel))
    rule_of = {r[0]: r for r in rules}

    # 5. Affixes (by type frequency over the word types used in the reference half).
    rng = _rng(lang, seed, 5)
    suf, pre = Counter(), Counter()
    for w in used:
        t = phon[w]
        for k in (1, 2, 3):
            if len(t) > k + 1:
                suf[t[-k:]] += 1
                pre[t[:k]] += 1
    sister_v = sorted({reg(v) for v in V})

    def new_affix(a: tuple[str, ...]) -> tuple[str, ...]:
        while True:
            out = tuple(sister_v[int(rng.integers(len(sister_v)))] if p in V else
                        sister_cons[int(rng.integers(len(sister_cons)))] for p in a)
            if out != tuple(reg(p) for p in a):
                return out
    affixes = {"suffix": {}, "prefix": {}}
    for kind, cnt, n in (("suffix", suf, N_SUFFIX), ("prefix", pre, N_PREFIX)):
        for a, _ in cnt.most_common(n):
            if rng.random() < knobs.affix_share:
                affixes[kind][a] = new_affix(a)

    # 4, 6. Final-vowel loss and lexical replacement, per word type.
    rng = _rng(lang, seed, 6)
    by_len: dict[int, list[int]] = {}
    for w in used:
        by_len.setdefault(len(phon[w]), []).append(w)
    replace = {}
    fvl = set()
    for w in used:
        if rng.random() < knobs.lexical:
            pool = by_len[len(phon[w])]
            replace[w] = pool[int(rng.integers(len(pool)))]
        if rng.random() < knobs.final_vowel_loss:
            fvl.add(w)

    attested: dict[str, Counter] = {}
    cache: dict[int, tuple[str, ...]] = {}

    def transform(w: int, src: int) -> tuple[str, ...]:
        t = phon[src]
        out = []
        for i, p in enumerate(t):
            r = rule_of.get(p)
            out.append(r[1] if r and _context_ok(r[2], t, i, V, r[3]) else reg(p))
        for k in (3, 2, 1):                                # longest replaced suffix
            if len(t) > k + 1 and t[-k:] in affixes["suffix"]:
                out[-k:] = affixes["suffix"][t[-k:]]
                break
        for k in (3, 2, 1):
            if len(t) > k + 1 and t[:k] in affixes["prefix"]:
                out[:k] = affixes["prefix"][t[:k]]
                break
        if w in fvl and len(out) >= 3 and t[-1] in V:
            out = out[:-1]
        return tuple(out)

    def reflexes(src: int, out: tuple[str, ...]) -> None:
        """Count sound-change reflexes only (positions not overwritten by an affix)."""
        t = phon[src]
        s_k = next((k for k in (3, 2, 1) if len(t) > k + 1 and t[-k:] in affixes["suffix"]), 0)
        p_k = next((k for k in (3, 2, 1) if len(t) > k + 1 and t[:k] in affixes["prefix"]), 0)
        for i, p in enumerate(t):
            if i < p_k or i >= len(t) - s_k or i >= len(out):
                continue
            attested.setdefault(p, Counter())[out[i]] += 1

    out_clauses, out_ids = [], []
    rng = _rng(lang, seed, 7)
    for _, ids in clauses:
        ws, wi = [], []
        for w in ids:
            src = replace.get(w, w)
            if w not in cache:
                cache[w] = transform(w, src)
            if cache[w]:
                ws.append(cache[w])
                wi.append(src)
                reflexes(src, cache[w])
        if len(ws) > 1 and rng.random() < knobs.word_order:
            if rng.random() < 0.5:
                ws, wi = ws[-1:] + ws[:-1], wi[-1:] + wi[:-1]
            else:
                j = int(rng.integers(len(ws) - 1))
                ws[j], ws[j + 1] = ws[j + 1], ws[j]
                wi[j], wi[j + 1] = wi[j + 1], wi[j]
        if ws:
            out_clauses.append(ws)
            out_ids.append(wi)
    return Sister(lang, seed, knobs, out_clauses, out_ids, regular, attested, merg, rules, affixes)


def hidden_half(lang: str) -> tuple[list[list[tuple[str, ...]]], list[list[int]]]:
    """Hidden-half clauses as word phoneme tuples, and word ids (for yardsticks and leakage)."""
    d = _segments(lang)
    phon = [tuple(w[1]) for w in d["words"]]
    cl, ids_ = [], []
    for _, ids in _split(lang, d, "hidden")[:MAX_CLAUSES]:
        ws = [(phon[w], w) for w in ids if phon[w]]
        if ws:
            cl.append([a for a, _ in ws])
            ids_.append([b for _, b in ws])
    return cl, ids_
