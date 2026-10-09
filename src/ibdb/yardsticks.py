"""v2: distance yardsticks between a hidden language and its relative (real or synthetic).

One implementation for both uses, so the Ugaritic-Hebrew anchor and the synthetic sisters are
measured with the same code (plan: docs/v2_sister_plan.md). The texts compared are unit sequences
(letters or phonemes); a `mapping` sends hidden units forward to the relative's units.

- bigram_jsd: Jensen-Shannon divergence (bits) between unit-bigram distributions within texts.
- floor: the same JSD between a same-size sample of a text and the whole text (sampling noise).
- verbatim: share of hidden strings found as substrings of the relative's text.
- overlap: share of hidden word types (and tokens) whose mapped form occurs in the relative's
  word types; word_pair_overlap: the same for adjacent word pairs.
- chance_corrected: (observed - chance) / (1 - chance), chance from shuffled mappings.
"""

from __future__ import annotations

from collections import Counter
from typing import Callable, Iterable, Sequence

import numpy as np


def bigram_jsd(a: Sequence[Sequence[str]], b: Sequence[Sequence[str]]) -> float:
    def dist(texts):
        c = Counter((t[i], t[i + 1]) for t in texts for i in range(len(t) - 1))
        n = sum(c.values())
        return {k: v / n for k, v in c.items()}
    p, q = dist(a), dist(b)
    ks = sorted(set(p) | set(q))      # fixed order: the float sum must not depend on string hashing
    P = np.array([p.get(k, 0.0) for k in ks])
    Q = np.array([q.get(k, 0.0) for k in ks])
    M = 0.5 * (P + Q)
    kl = lambda x: float(np.sum(x[x > 0] * np.log2(x[x > 0] / M[x > 0])))  # noqa: E731
    return 0.5 * (kl(P) + kl(Q))


def sample_texts(texts: Sequence, n_units: int, rng) -> list:
    """Whole texts in random order until n_units units are reached (size-matched sample)."""
    out, k = [], 0
    for i in rng.permutation(len(texts)):
        out.append(texts[i])
        k += len(texts[i])
        if k >= n_units:
            break
    return out


def sample_tokens(words: Counter, n_tokens: int, rng) -> Counter:
    keys = list(words)
    p = np.array([words[k] for k in keys], dtype=float)
    idx = rng.choice(len(keys), size=n_tokens, p=p / p.sum())
    return Counter(keys[i] for i in idx)


def verbatim(strings: Iterable[str], blob: str, min_len: int = 0) -> float:
    xs = [x for x in strings if len(x) >= max(min_len, 1)]
    return sum(x in blob for x in xs) / len(xs) if xs else float("nan")


def overlap(hidden: dict, rel: set, mapf: Callable) -> tuple[float, float]:
    """(type share, token share) of hidden items whose mapped form is in `rel`."""
    keys = list(hidden)
    m = [mapf(k) in rel for k in keys]
    return sum(m) / len(keys), sum(hidden[k] for k, ok in zip(keys, m) if ok) / sum(hidden.values())


def chance_corrected(obs: float, chance: float) -> float:
    return (obs - chance) / (1 - chance) if chance < 1 else float("nan")


def shuffled_mapping(mapping: dict, rng) -> dict:
    """Same keys, values permuted (keeps the many-to-one structure)."""
    ks = sorted(mapping)
    return dict(zip(ks, rng.permutation([mapping[k] for k in ks])))


# ---------------------------------------------------------------- Ugaritic-Hebrew anchor

def ugaritic_hebrew(heb_texts, heb_words, poetic_texts, n_shuffle: int = 200, recut_mean: float = 4.6) -> dict:
    """The anchor's yardsticks. The order of random draws is that of the original anchor script
    (reports/v2/ugaritic/records.json), so the published values are reproduced exactly; the word-pair
    yardstick, added later, uses its own generator."""
    from .data import ugaritic as U
    seg = U.ugaritic_texts("segment")
    blob = "|".join("".join(t) for t in heb_texts)
    hw = {"".join(w) for w in heb_words}
    uw = U.ugaritic_words()
    rng = np.random.default_rng(0)
    gold = U.GOLD
    shuf = [shuffled_mapping(gold, rng) for _ in range(n_shuffle)]
    recut = U.recut(seg, recut_mean, 0)
    gm = lambda m, t: "".join(m[x] for x in t if x != U.DIVIDER)  # noqa: E731
    out = {"mergers": len(gold) - len(set(gold.values())), "n_word_types": len(uw), "n_word_tokens": sum(uw.values())}
    for name, texts, ml in (("natural", seg, 0), ("natural_6plus", seg, 6), ("recut4.6", recut, 0)):
        out[f"verbatim_{name}"] = verbatim((gm(gold, t) for t in texts), blob, ml)
        out[f"verbatim_{name}_chance"] = float(np.mean([verbatim((gm(m, t) for t in texts), blob, ml) for m in shuf[:50]]))
    wmap = lambda m: (lambda w: "".join(m[x] for x in w))  # noqa: E731
    ct, ck = overlap(uw, hw, wmap(gold))
    ch = np.array([overlap(uw, hw, wmap(m)) for m in shuf])
    out.update({"cognate_types": ct, "cognate_tokens": ck,
                "cognate_types_chance": float(ch[:, 0].mean()), "cognate_types_chance_p95": float(np.quantile(ch[:, 0], 0.95)),
                "cognate_tokens_chance": float(ch[:, 1].mean())})
    letters = [[gold[x] for x in t if x != U.DIVIDER] for t in seg]
    out["bigram_jsd"] = bigram_jsd(letters, heb_texts)
    out["bigram_jsd_poetic"] = bigram_jsd(letters, poetic_texts)
    out["bigram_jsd_shuffled_mean"] = float(np.mean([bigram_jsd([[m[x] for x in t if x != U.DIVIDER] for t in seg],
                                                                heb_texts) for m in shuf[:50]]))
    out["bigram_jsd_hebrew_poetic_vs_whole"] = bigram_jsd(poetic_texts, heb_texts)
    n_letters = sum(map(len, letters))
    out["bigram_jsd_hebrew_sample_floor"] = float(np.mean([bigram_jsd(sample_texts(heb_texts, n_letters, rng), heb_texts)
                                                           for _ in range(20)]))
    out["n_letters"] = n_letters
    # Derived targets (sister plan).
    out["jsd_above_floor"] = out["bigram_jsd"] - out["bigram_jsd_hebrew_sample_floor"]
    out["cognate_types_cc"] = chance_corrected(ct, out["cognate_types_chance"])
    out["verbatim_6plus_lengths"] = sorted(len(gm(gold, t)) for t in seg if len(gm(gold, t)) >= 6)
    # Word-pair overlap (added for the sister plan; own generator so the values above are unchanged).
    from .data.ugaritic import hebrew_word_pairs, ugaritic_word_pairs
    up = ugaritic_word_pairs()
    hp = {("".join(a), "".join(b)) for a, b in hebrew_word_pairs()}
    pmap = lambda m: (lambda p: ("".join(m[x] for x in p[0]), "".join(m[x] for x in p[1])))  # noqa: E731
    r2 = np.random.default_rng(1)
    pt, pk = overlap(up, hp, pmap(gold))
    pc = np.array([overlap(up, hp, pmap(shuffled_mapping(gold, r2))) for _ in range(n_shuffle)])
    out.update({"n_word_pair_types": len(up), "n_word_pair_tokens": sum(up.values()),
                "word_pairs_types": pt, "word_pairs_tokens": pk,
                "word_pairs_types_chance": float(pc[:, 0].mean()),
                "word_pairs_types_chance_p95": float(np.quantile(pc[:, 0], 0.95)),
                "word_pairs_types_cc": chance_corrected(pt, float(pc[:, 0].mean()))})
    return out


# ---------------------------------------------------------------- synthetic sister (sister-v4 or v1)

def sister_yardsticks(hidden_clauses, sister_clauses, regular: dict, anchor: dict, n_draws: int = 20,
                      seed: int = 0) -> dict:
    """Yardsticks for a hidden half (clauses as word phoneme tuples) and a sister (same form),
    computed exactly as for the anchor: the hidden side is mapped forward through `regular`, samples
    are size-matched to the anchor (anchor['n_letters'] units, anchor['n_word_tokens'] word tokens,
    anchor['n_word_pair_tokens'] word pairs, the anchor's 6+ letter text lengths), and chance uses
    shuffled mappings. The floor is a same-size sample of the sister against the whole sister, as
    the anchor's floor is a Hebrew sample against all Hebrew."""
    rng = np.random.default_rng(seed)
    f = lambda p: regular.get(p, p)  # noqa: E731
    htexts = [[p for w in c for p in w] for c in hidden_clauses]
    stexts = [[p for w in c for p in w] for c in sister_clauses]
    fwd = [[f(p) for p in t] for t in htexts]
    jsd = float(np.mean([bigram_jsd(sample_texts(fwd, anchor["n_letters"], rng), stexts) for _ in range(n_draws)]))
    floor = float(np.mean([bigram_jsd(sample_texts(stexts, anchor["n_letters"], rng), stexts) for _ in range(n_draws)]))

    keys = sorted(regular)
    shuf = [dict(zip(keys, rng.permutation([regular[k] for k in keys]))) for _ in range(n_draws)]
    hw = Counter(w for c in hidden_clauses for w in c)
    sw = {w for c in sister_clauses for w in c}
    mapw = lambda m: (lambda w: tuple(m.get(p, p) for p in w))  # noqa: E731
    samples = [sample_tokens(hw, anchor["n_word_tokens"], rng) for _ in range(n_draws)]
    ov = np.array([overlap(s, sw, mapw(regular)) for s in samples])
    ch = np.array([overlap(s, sw, mapw(m)) for s, m in zip(samples, shuf)])

    hp = Counter(p for c in hidden_clauses for p in zip(c, c[1:]))
    sp = {p for c in sister_clauses for p in zip(c, c[1:])}
    mapp = lambda m: (lambda p: (mapw(m)(p[0]), mapw(m)(p[1])))  # noqa: E731
    psamples = [sample_tokens(hp, anchor["n_word_pair_tokens"], rng) for _ in range(n_draws)]
    pov = np.array([overlap(s, sp, mapp(regular)) for s in psamples])
    pch = np.array([overlap(s, sp, mapp(m)) for s, m in zip(psamples, shuf)])

    # Verbatim: windows of the anchor's 6+ letter text lengths, from random hidden texts.
    SEP = "\x1f"
    blob = "|".join(SEP.join(t) + SEP for t in stexts)
    long_ = [t for t in fwd if len(t) >= 6]
    hits = []
    for L in anchor["verbatim_6plus_lengths"]:
        t = long_[int(rng.integers(len(long_)))]
        if len(t) < L:
            continue
        i = int(rng.integers(len(t) - L + 1))
        hits.append(SEP.join(t[i:i + L]) + SEP in blob)
    cc = chance_corrected(float(ov[:, 0].mean()), float(ch[:, 0].mean()))
    pcc = chance_corrected(float(pov[:, 0].mean()), float(pch[:, 0].mean()))
    return {"bigram_jsd": jsd, "floor": floor, "jsd_above_floor": jsd - floor,
            "cognate_types": float(ov[:, 0].mean()), "cognate_types_chance": float(ch[:, 0].mean()), "cognate_types_cc": cc,
            "cognate_tokens": float(ov[:, 1].mean()),
            "word_pairs_types": float(pov[:, 0].mean()), "word_pairs_types_chance": float(pch[:, 0].mean()),
            "word_pairs_types_cc": pcc,
            "verbatim_6plus": float(np.mean(hits)) if hits else float("nan"), "n_verbatim_windows": len(hits)}
