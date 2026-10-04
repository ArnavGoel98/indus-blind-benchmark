"""Build one synthetic corpus (public Corpus + private AnswerKey) from a source and a script spec."""

from __future__ import annotations

import hashlib
import json
import zlib
from collections import Counter
from dataclasses import asdict, dataclass, field, replace
from functools import lru_cache
from typing import Any

import numpy as np

from .. import config
from ..controls import CONTROLS, Adversarial
from ..corpus import AnswerKey, Corpus
from ..data.prepare import load_segments
from . import sampler
from .script import DIV, ScriptSpec, build_script, spell_word, word_sem, word_units

LANGUAGES = ("sanskrit", "tamil", "sumerian", "latin", "finnish")


@dataclass
class Knobs:
    """Calibration knobs (see generator.calibrate)."""

    alpha: float = 1.0          # preference for windows of frequent words
    beta: float = 0.5           # preference for frequent final words
    kappa: float = 1.0          # preference for clause-initial / seal-genre windows
    gamma: float = 0.0          # preference for frequent first words (negative: diverse beginnings)
    rho: float = 0.05           # share of texts that are copies of a few popular texts
    allograph_rate: float | None = None
    allograph_extra_mean: float | None = None
    vocab_cap: int | None = None        # only windows whose words are all within this frequency rank
    concentration: float = 1.0          # controls: Zipf exponent multiplier
    adv_target_ratio: float = 0.55      # adversarial control: target H(X2|X1)/H(X1)
    first_word_exponent: float = 1.0    # generator-v2 only: first-word-type sampling exponent

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_DISGUISED: dict[str, dict] = {}   # challenge sources: name "lang~secret" -> transformed segments


def base_source(source: str) -> str:
    return source.split("~", 1)[0]


def source_kind(source: str) -> str:
    source = base_source(source)
    if source in LANGUAGES:
        return "language"
    if source == "kamon":
        return "nl_derived"
    return CONTROLS[source].kind


def source_family(source: str) -> str:
    source = base_source(source)
    if source in LANGUAGES:
        return config.sources()["languages"][source]["family"]
    return "none"


@lru_cache(maxsize=16)
def _segments(source: str) -> dict:
    if source in _DISGUISED:
        return _DISGUISED[source]
    d = load_segments(source)
    freq = Counter(w for _, ids in d["clauses"] for w in ids)
    n = len(d["words"])
    f = np.array([freq.get(i, 0) for i in range(n)], dtype=np.float64)
    order = np.argsort(-f, kind="stable")
    rank = np.empty(n, dtype=np.int64)
    rank[order] = np.arange(1, n + 1)
    logf = np.log((f + 0.5) / f.sum())
    d["_rank"], d["_logf"] = rank, logf
    return d


def split_clauses(source: str, d: dict, half: str) -> list:
    """Disjoint halves of a source's clauses.

    'hidden' feeds corpus generation; 'reference' feeds the known-language models used by
    decipherment methods (knowledge tiers). Without this split a solver's "related language"
    would contain the very phrases it is asked to decipher.
    """
    want = 0 if half == "hidden" else 1
    if sister_version() == "v2":
        # sister-v2: split by clause CONTENT, so identical clauses always fall in the same half
        # (sister-v1 split by position, which put repeated clauses in both halves).
        return [c for c in d["clauses"]
                if zlib.crc32(f"{base_source(source)}:{' '.join(map(str, c[1]))}".encode()) % 2 == want]
    return [c for i, c in enumerate(d["clauses"]) if zlib.crc32(f"{source}:{i}".encode()) % 2 == want]


def sister_version() -> str:
    """'v1' (split by clause position, the frozen-v1 runs) or 'v2' (split by clause content).
    Set per run via the IBDB_SISTER_VERSION environment variable (profiles set it)."""
    import os
    return os.environ.get("IBDB_SISTER_VERSION", "v1")


@dataclass
class Plan:
    words: list
    units: list[list[str]]
    sems: list[int | None]
    windows: sampler.WindowIndex
    logograms: set[int] = field(default_factory=set)


_PLAN_CACHE: dict[tuple, Plan] = {}


def language_plan(source: str, spec: ScriptSpec, seed: int, max_len: int) -> Plan:
    key = (sister_version(), source, spec.script_type, spec.determinatives, spec.word_divider, spec.logogram_vocab,
           spec.sem_rate, spec.n_sem_classes, seed, max_len)
    if key in _PLAN_CACHE:
        return _PLAN_CACHE[key]
    d = _segments(source)
    words, rank = d["words"], d["_rank"]
    logograms: set[int] = set()
    if spec.script_type == "logosyllabic":
        logograms = set(np.flatnonzero(rank <= spec.logogram_vocab).tolist())
    st = spec if base_source(source) != "kamon" else replace(spec, script_type="logographic")
    units = [word_units(w, st, logograms, i) for i, w in enumerate(words)]
    # Sumerian determinatives are already explicit readings in the transliteration.
    use_det = spec.determinatives and base_source(source) != "sumerian"
    sems = [word_sem(w, spec, seed, base_source(source)) if use_det else None for w in words]
    wlen = np.array([len(u) + (1 if s is not None else 0) for u, s in zip(units, sems)], dtype=np.int64)
    wlen[wlen == 0] = 10_000  # unusable word (no units)
    windows = sampler.build_windows(split_clauses(source, d, "hidden"), wlen, rank, d["_logf"], max_len, spec.word_divider)
    plan = Plan(words, units, sems, windows, logograms)
    if len(_PLAN_CACHE) > 24:
        _PLAN_CACHE.pop(next(iter(_PLAN_CACHE)))
    _PLAN_CACHE[key] = plan
    return plan


def corpus_id_for(params: dict[str, Any]) -> str:
    return hashlib.sha1(json.dumps(params, sort_keys=True, default=str).encode()).hexdigest()[:12]


def make_corpus(source: str, spec: ScriptSpec, n_texts: int, mean_length: float, seed: int,
                knobs: Knobs | None = None, corpus_id: str | None = None,
                median_length: float | None = None, adv_ratio_fn=None,
                generator_version: str = "v1") -> tuple[Corpus, AnswerKey, dict]:
    knobs = knobs or Knobs()
    spec = replace(spec)
    if knobs.allograph_rate is not None:
        spec.allograph_rate = knobs.allograph_rate
    if knobs.allograph_extra_mean is not None:
        spec.allograph_extra_mean = knobs.allograph_extra_mean
    kind = source_kind(source)
    ss = np.random.SeedSequence([seed, n_texts, int(mean_length * 100)])
    r_len, r_pick, r_script, r_spell, r_dup = [np.random.default_rng(s) for s in ss.spawn(5)]

    targets = sampler.draw_lengths(r_len, n_texts, mean_length, median_length)
    max_len = int(targets.max())

    texts_units: list[list[tuple[str, list[str], int | None]]] = []  # per text: (form, units, sem) words
    truncs: list[int] = []
    n_trunc = n_concat = 0
    if kind in ("language", "nl_derived"):
        plan = language_plan(source, spec, seed, max_len)
        wi = plan.windows
        logits = sampler.window_logits(wi, knobs.alpha, knobs.beta, knobs.kappa, knobs.gamma)
        mask = np.ones(len(wi.start), dtype=bool)
        if knobs.vocab_cap is not None:
            mask &= wi.maxrank <= knobs.vocab_cap
        if not mask.any():
            mask[:] = True
        if generator_version == "v2":
            rest = sampler.window_logits(wi, knobs.alpha, knobs.beta, knobs.kappa, 0.0)
            picks = sampler.pick_windows_v2(wi, targets, rest, mask, r_pick, knobs.first_word_exponent)
        else:
            picks = sampler.pick_windows(wi, targets, logits, mask, r_pick)
        valid = np.flatnonzero(mask)
        for (start, nw, trunc), L in zip(picks, targets.tolist()):
            if start >= 0:
                ids = wi.flat[start:start + nw].tolist()
            else:
                ids, total = [], 0
                while total < L:  # concatenate random windows (only for very long targets)
                    c = int(valid[r_pick.integers(len(valid))])
                    seg = wi.flat[wi.start[c]: wi.start[c] + wi.nwords[c]].tolist()
                    ids += seg
                    total += int(wi.length[c])
                trunc = int(L)
                n_concat += 1
            if trunc:
                n_trunc += 1
            truncs.append(int(trunc))
            texts_units.append([(plan.words[i][0], plan.units[i], plan.sems[i]) for i in ids])
        script_type = spec.script_type if kind == "language" else "emblem"
        plaintext = [" ".join(w[0] for w in t) for t in texts_units]
    else:
        ctrl_cls = CONTROLS[source]
        ctrl = ctrl_cls(seed, knobs.concentration)
        if isinstance(ctrl, Adversarial) and adv_ratio_fn is not None:
            ctrl.tune_mix(knobs.adv_target_ratio, adv_ratio_fn)
        for L in targets.tolist():
            toks = ctrl.make_text(r_pick, int(L))
            texts_units.append([(t, [t], None) for t in toks])
            truncs.append(0)
        spec = replace(spec, script_type="emblem", determinatives=False, word_divider=False,
                       homophony_rate=0.0, polyvalence_rate=0.0)
        script_type = "emblem"
        plaintext = [" ".join(w[0] for w in t) for t in texts_units]

    values = Counter(u for t in texts_units for (_, units, _) in t for u in units)
    sem_classes = {s for t in texts_units for (_, _, s) in t if s is not None}
    script = build_script(values, spec, r_script, seed, sem_classes)

    logical_texts: list[list[int]] = []
    token_values: list[list[str]] = []
    word_starts: list[list[int]] = []
    for t, trunc in zip(texts_units, truncs):
        signs: list[int] = []
        vals: list[str] = []
        starts: list[int] = []
        for wi_, (form, units, sem) in enumerate(t):
            if wi_ > 0 and script.divider is not None:
                signs.append(script.divider)
                vals.append(DIV)
            starts.append(len(signs))
            s, v = spell_word(script, form, units, sem, r_spell)
            signs += s
            vals += v
        if trunc:
            signs, vals = signs[:trunc], vals[:trunc]
            starts = [p for p in starts if p < trunc]
        logical_texts.append(signs)
        token_values.append(vals)
        word_starts.append(starts)

    # Formulaic repetition: a few popular texts recur (as in raw M77; see indus_targets.yaml).
    n_dup = int(round(knobs.rho * n_texts))
    if n_dup > 0 and n_texts > 10:
        n_pop = max(1, n_texts // 100)
        pop = r_dup.choice(n_texts, size=n_pop, replace=False)
        w = 1.0 / np.arange(1, n_pop + 1) ** 1.1
        src = pop[r_dup.choice(n_pop, size=n_dup, p=w / w.sum())]
        dst = r_dup.choice(np.setdiff1d(np.arange(n_texts), pop), size=n_dup, replace=False)
        for a, b in zip(dst.tolist(), src.tolist()):
            logical_texts[a] = list(logical_texts[b])
            token_values[a] = list(token_values[b])
            word_starts[a] = list(word_starts[b])
            plaintext[a] = plaintext[b]

    used = {s for t in logical_texts for s in t}
    sign_values = {s: v for s, v in script.sign_values.items() if s in used}
    params = {"source": source, "spec": spec.to_dict(), "knobs": knobs.to_dict(), "seed": seed,
              "n_texts": n_texts, "mean_length": mean_length}
    cid = corpus_id or corpus_id_for(params)
    phys = [np.array(t[::-1] if spec.direction == "rtl" else t, dtype=np.int64) for t in logical_texts]
    corpus = Corpus(cid, phys, spec.direction, {"corpus_id": cid, "n_texts": n_texts})
    key = AnswerKey(cid, source, source_family(source), kind, kind == "language", script_type,
                    sign_values, token_values, word_starts, params, plaintext)
    info = {"truncated": n_trunc, "concatenated": n_concat, "n_values": len(values)}
    return corpus, key, info
