"""v2 Tasks C and D with a relative other than the v1 sister (pre-registration entries 2, 4 and 5).

One code path for two kinds of relative:
- `harsh` (entry 4, lower bound of the bracket): sister-v4 with the settings in
  reports/v2/sister/harsh.json, built from the reference half of the source text;
- real relatives (entry 5): Italian for Latin, Malayalam and Kannada for Tamil (Estonian for
  Finnish once its gold table exists), normalised spelling, whole text.

A relative is given as clauses of words (phoneme tuples), a gold regular-reflex map (hidden phoneme ->
relative phoneme, None = no reflex) and the attested reflexes of each hidden phoneme.

Reference (what the solver sees) is written at the script's unit level as v1 writes its references
(knowledge._word_units): phonemes (alphabetic); CV syllables from phonology.syllabify with the hidden
language's vowels (syllabic); word forms (logographic); in logo-syllabic scripts, word forms for the
relative's `logogram_vocab` most frequent word types and syllables otherwise. Sumerian's syllable units
are sign readings (CVC and longer), not CV syllables, so for such a language the relative's syllables
are found by greedy longest match against the hidden readings mapped through the regular reflexes
(as v1 writes its sister unit by unit), single phonemes otherwise. No reference carries a
correspondence table, so every score is before the cognate step.

Scoring (entry 2), per sign token, against the token's hidden value:
- strict: the predicted unit equals the regular reflex of the hidden value. For a phoneme, its
  reflex; for a syllable, the reflexes of its phonemes joined (phonemes with no reflex dropped); for a
  word form (logogram), the relative word so formed, and only if that word occurs in the relative
  (a cognate; plan, "Script levels"). Otherwise the token is unrecoverable.
- lenient: the predicted unit can be formed from attested reflexes (regular included) of the hidden
  value's phonemes, in order; for a logogram it must also occur in the relative.
- Units the generator adds (word dividers <DIV>, determinatives <DET:n>) are unrecoverable, as in v1.
  Units of the source text that no sound law touches (Sumerian numerals such as #1(disz) and its
  written determinatives such as {kuš}) keep their value, as in the v1 sister. Many-to-one is accepted.
`recoverable` is the share of tokens that have a strict reflex at all (the ceiling for that corpus).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from functools import lru_cache

from . import phonology
from .corpus import AnswerKey
from .generator.build import _segments, base_source, source_family
from .knowledge import MAX_REF_CLAUSES
from .methods.base import Reference


@dataclass
class Relative:
    name: str
    family: str
    clauses: list[list[tuple[str, ...]]]
    regular: dict[str, str | None]
    attested: dict[str, set[str]] = field(default_factory=dict)

    def options(self, p: str) -> set[str]:
        """Strings hidden phoneme `p` may become (lenient); '' where it has no reflex."""
        r = self.regular.get(p, p)
        return {r or ""} | {a for a in self.attested.get(p, ()) if a}


def _groups(phon, vowels) -> list[tuple[str, ...]]:
    """phonology.syllabify, keeping each syllable's phonemes."""
    units: list[tuple[str, ...]] = []
    pending: list[str] = []
    for ph in phon:
        if ph in vowels:
            if pending:
                units.extend((x,) for x in pending[:-1])
                units.append((pending[-1], ph))
                pending = []
            else:
                units.append((ph,))
        else:
            pending.append(ph)
    units.extend((x,) for x in pending)
    return units


def _vowels(hidden_lang: str) -> frozenset[str]:
    return phonology.PROFILES[base_source(hidden_lang)].vowels


def _align(syl: list[str], phon) -> list[tuple[str, ...]] | None:
    """Split `phon` into the syllable units `syl` (their strings concatenate to the same text)."""
    out, i = [], 0
    for u in syl:
        j, acc = i, ""
        while j < len(phon) and len(acc) < len(u):
            acc += phon[j]
            j += 1
        if acc != u:
            return None
        out.append(tuple(phon[i:j]))
        i = j
    return out if i == len(phon) else None


@lru_cache(maxsize=16)
def _cv_language(hidden_lang: str) -> bool:
    """True when the source's syllable units are phonology.syllabify's CV units (all but Sumerian)."""
    v = _vowels(hidden_lang)
    return all(w[2] == phonology.syllabify(w[1], v) for w in _segments(hidden_lang)["words"])


def _greedy(word: tuple[str, ...], inventory: set[str], longest: int) -> list[str]:
    units, i = [], 0
    while i < len(word):
        for k in range(min(longest, len(word) - i), 0, -1):
            u = "".join(word[i:i + k])
            if k == 1 or u in inventory:
                units.append(u)
                i += k
                break
    return units


def reference(rel: Relative, script_type: str, hidden_lang: str, logogram_vocab: int = 250) -> Reference:
    vowels = _vowels(hidden_lang)
    if script_type in ("syllabic", "logosyllabic") and not _cv_language(hidden_lang):
        mapped = {tuple(x for x in (rel.regular.get(p, p) for p in ph) if x) for ph in _hidden_lookup(hidden_lang)[1].values()}
        inventory = {"".join(m) for m in mapped if m}
        longest = max(len(m) for m in mapped)
        syllables = lambda w: _greedy(w, inventory, longest)  # noqa: E731
    else:
        syllables = lambda w: ["".join(g) for g in _groups(w, vowels)]  # noqa: E731
    clauses = rel.clauses[:MAX_REF_CLAUSES]
    freq = Counter(w for c in clauses for w in c)
    logo = {w for w, _ in freq.most_common(logogram_vocab)} if script_type == "logosyllabic" else set()
    texts: list[list[str]] = []
    wcount: Counter = Counter()
    for c in clauses:
        seq: list[str] = []
        for w in c:
            if script_type == "alphabetic":
                units = list(w)
            elif script_type == "logographic" or w in logo:
                units = ["".join(w)]
            elif script_type in ("syllabic", "logosyllabic"):
                units = syllables(w)
            else:
                raise ValueError(script_type)
            seq += units
            wcount[tuple(units)] += 1
        if seq:
            texts.append(seq)
    return Reference(rel.name, rel.family, texts, dict(wcount), {})


@lru_cache(maxsize=16)
def _hidden_lookup(hidden_lang: str) -> tuple[dict, dict]:
    """Hidden word form -> phonemes, and syllable string -> phonemes, from the source segments."""
    forms: dict[str, tuple[str, ...]] = {}
    syls: dict[str, tuple[str, ...]] = {}
    for form, phon, syl, _ in _segments(hidden_lang)["words"]:
        forms.setdefault(form, tuple(phon))
        for g in _align(syl, phon) or ():
            syls.setdefault("".join(g), g)
    return forms, syls


def _derivable(pred: str, phon: tuple[str, ...], rel: Relative) -> bool:
    """Can `pred` be written as the hidden phonemes' attested reflexes, in order?"""
    reach = {0}
    for p in phon:
        nxt = set()
        for i in reach:
            for o in rel.options(p):
                if pred.startswith(o, i):
                    nxt.add(i + len(o))
        reach = nxt
        if not reach:
            return False
    return len(pred) in reach


class Gold:
    """Strict and lenient correctness of a predicted relative unit for one hidden token value."""

    def __init__(self, rel: Relative, hidden_lang: str, script_type: str, logograms: set[str]):
        self.rel, self.st, self.logograms = rel, script_type, logograms
        self.forms, self.syls = _hidden_lookup(hidden_lang)
        self.vocab = {"".join(w) for c in rel.clauses for w in c}
        self._cache: dict[str, tuple[str | None, tuple[str, ...] | None, bool]] = {}

    def _value(self, v: str) -> tuple[str | None, tuple[str, ...] | None, bool]:
        """(strict reflex or None, hidden phonemes or None, is_word)."""
        if v in self._cache:
            return self._cache[v]
        out: tuple[str | None, tuple[str, ...] | None, bool] = (None, None, False)
        if not v.startswith("<"):                     # generator-added: <DIV>, <DET:n>
            if self.st == "logographic" or (self.st == "logosyllabic" and v in self.logograms):
                phon = self.forms.get(v)
                if phon is not None:
                    r = "".join(x for x in (self.rel.regular.get(p, p) for p in phon) if x)
                    out = (r if r in self.vocab else None, phon, True)
            else:
                phon = (v,) if self.st == "alphabetic" else self.syls.get(v)
                if phon is not None:
                    r = "".join(x for x in (self.rel.regular.get(p, p) for p in phon) if x)
                    out = (r or None, phon, False)
        self._cache[v] = out
        return out

    def recoverable(self, v: str) -> bool:
        return self._value(v)[0] is not None

    def strict(self, pred: str | None, v: str) -> bool:
        r = self._value(v)[0]
        return r is not None and pred == r

    def lenient(self, pred: str | None, v: str) -> bool:
        r, phon, is_word = self._value(v)
        if pred is None or phon is None or not pred:
            return False
        if pred == r:
            return True
        if is_word and pred not in self.vocab:
            return False
        return _derivable(pred, phon, self.rel)


def score(pred: dict[int, str] | None, key: AnswerKey, logical: list[list[int]], gold: Gold) -> dict[str, float]:
    pred = pred or {}
    n = strict = lenient = rec = 0
    for t, vals in zip(logical, key.token_values):
        for s, v in zip(t, vals):
            n += 1
            p = pred.get(int(s))
            rec += gold.recoverable(v)
            strict += gold.strict(p, v)
            lenient += gold.lenient(p, v)
    return {"strict": strict / n if n else 0.0, "lenient": lenient / n if n else 0.0,
            "recoverable": rec / n if n else 0.0}


def hidden_logograms(hidden_lang: str, logogram_vocab: int = 250) -> set[str]:
    """Word forms written with logograms in a logo-syllabic corpus (generator: rank <= vocab)."""
    d = _segments(hidden_lang)
    return {w[0] for w, r in zip(d["words"], d["_rank"]) if r <= logogram_vocab}


# ------------------------------------------------------------------ the relatives

@lru_cache(maxsize=8)
def real_relative(hidden_lang: str, relative: str) -> Relative:
    from .data import dravidian as D
    from .data import relatives as R
    if (hidden_lang, relative) == ("latin", "italian"):
        reg, att = R.latin_italian_map()
        clauses = R.dante_texts("normalised")
    elif hidden_lang == "tamil" and relative in ("malayalam", "kannada"):
        reg, att = D.gold_map(relative)
        clauses = D.texts(relative, "normalised")
    else:
        raise ValueError(f"no real relative {relative} for {hidden_lang} yet")
    return Relative(relative, source_family(hidden_lang), clauses, reg, {k: set(v) for k, v in att.items()})


def harsh_relative(hidden_lang: str, seed: int, knobs: dict) -> Relative:
    from . import sister_v4 as S
    sis = S.build(hidden_lang, seed, S.Knobs(**knobs))
    return Relative(f"{hidden_lang}-sister-harsh", source_family(hidden_lang), sis.clauses,
                    dict(sis.regular), {k: set(v) for k, v in sis.attested.items()})
