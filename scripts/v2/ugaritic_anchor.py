"""v2 rank 2: Ugaritic-Hebrew real-relative anchor (plan: docs/v2_ugaritic_plan.md, pushed as b05772d).

Methods are frozen-v1 and run unchanged. Hidden: EUPT Kirta epic (KTU 1.14-1.16), letters mapped to
arbitrary sign IDs. Reference: OSHB consonantal Hebrew. Gold: Wikipedia table citing Kogan (2011),
many-to-one (two Ugaritic letters with one Hebrew correspondent both count correct when mapped to it).

Corpora: natural text (each readable run between gaps; primary), whole tablet lines (gaps joined),
and the natural text re-cut to mean length 4.6 (seeds 0-2).
Task A/B: frozen rules fit on the v1 run records exactly as for Sproat's corpora (no retraining).
Task C/D: frequency-rank baseline, frozen EM original rule (primary) and revised rule, in tiers
related (Hebrew), related_poetic (Psalms, Job, Proverbs), candidates (Hebrew + the five v1 languages),
none (the five v1 languages). Every score is before the cognate step by construction (no reference
carries a correspondence table).
Yardsticks: verbatim shared text, mergers, cognate-form overlap, bigram JSD; v1 sister values
computed the same way (sister-v2, alphabetic units, hidden half vs sister half).

Usage: python scripts/v2/ugaritic_anchor.py
Writes reports/v2/ugaritic/{records.json, results.md}.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

import numpy as np

os.environ["IBDB_SISTER_VERSION"] = "v2"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ibdb import config  # noqa: E402
from ibdb.data import ugaritic as U  # noqa: E402
from ibdb.evaluate import A_METHODS, B_METHODS  # noqa: E402
from ibdb.generator.build import LANGUAGES, _segments, split_clauses  # noqa: E402
from ibdb.generator.script import DIV  # noqa: E402
from ibdb.knowledge import MAX_REF_CLAUSES, _word_units, build_reference  # noqa: E402
from ibdb.methods.base import Knowledge, Reference  # noqa: E402
from ibdb.methods.decipher import FrequencyRankBaseline, KnightEM, KnightEMOriginal  # noqa: E402
from ibdb.methods.structural import BranchingSegmentation, InventoryRule, ScriptTypeLR  # noqa: E402
from ibdb.paths import ensure, reports_dir  # noqa: E402
from ibdb.scoring import score_sign_values  # noqa: E402
from ibdb.stats import corpus_stats  # noqa: E402
from sproat_controls import POOLS, pool, predict  # noqa: E402

OUT = ensure(reports_dir() / "v2" / "ugaritic")
INDUS_MEAN = 4.6
SEEDS = [0, 1, 2]
N_SHUFFLE = 200
D_METHODS = [FrequencyRankBaseline, KnightEMOriginal, KnightEM]
PRIMARY = KnightEMOriginal.name
THRESHOLD = 0.5            # pre-registered: v1 success threshold, 50% of tokens


def corpora() -> list[tuple[str, list[list[str]], int]]:
    seg = U.ugaritic_texts("segment")
    out = [("natural", seg, 0), ("lines", U.ugaritic_texts("line"), 0)]
    out += [(f"recut4.6/s{s}", U.recut(seg, INDUS_MEAN, s), s) for s in SEEDS]
    return out


def references() -> dict[str, Reference]:
    heb = Reference("hebrew", "semitic", U.hebrew_texts(), U.hebrew_words())
    poet = Reference("hebrew-poetic", "semitic", U.hebrew_texts(U.POETIC_BOOKS), U.hebrew_words(U.POETIC_BOOKS))
    v1 = {l: build_reference(l, "alphabetic", False, 0) for l in LANGUAGES}
    return {"hebrew": heb, "hebrew-poetic": poet, **v1}


def tiers(refs: dict[str, Reference]) -> dict[str, Knowledge]:
    v1 = [refs[l] for l in LANGUAGES]
    return {"related": Knowledge("related", "alphabetic", [refs["hebrew"]]),
            "related_poetic": Knowledge("related", "alphabetic", [refs["hebrew-poetic"]]),
            "candidates": Knowledge("candidates", "alphabetic", [refs["hebrew"]] + v1),
            "none": Knowledge("none", "alphabetic", v1)}


def d_scores(pred: dict[int, str] | None, key, logical, sid: dict[str, int]) -> dict:
    """token_acc: v1 convention (every token, dividers count and are unrecoverable).
    letters: dividers excluded. letters_sourced: also excluding the aleph signs i and u, whose
    Hebrew cell is empty in the gold source. type_acc_letters: letter types right / letter types."""
    pred = pred or {}
    s = score_sign_values(pred, key, logical)
    inv = {v: k for k, v in sid.items()}
    tot = Counter()
    hit = Counter()
    for t, vals in zip(logical, key.token_values):
        for g, v in zip(t, vals):
            letter = inv[int(g)]
            if v == DIV:
                continue
            ok = pred.get(int(g)) == v
            tot["letters"] += 1
            hit["letters"] += ok
            if letter not in U.UNSOURCED:
                tot["sourced"] += 1
                hit["sourced"] += ok
    lt = [l for l in sid if l != U.DIVIDER]
    right = sorted(l for l in lt if pred.get(sid[l]) == U.GOLD.get(l))
    return {"token_acc": s["token_acc"], "letters": hit["letters"] / tot["letters"],
            "letters_sourced": hit["sourced"] / tot["sourced"], "type_acc_letters": len(right) / len(lt),
            "types_right": right, "n_letter_types": len(lt)}


def ceilings(texts: list[list[str]]) -> dict:
    """Best letter-token accuracy reachable by a one-to-one sign->letter map (the frequency-rank
    baseline is one-to-one by construction) and by a many-to-one map (EM may map many signs to one)."""
    c = Counter(x for t in texts for x in t if x != U.DIVIDER)
    by_heb: dict[str, list[int]] = {}
    for l, n in c.items():
        by_heb.setdefault(U.GOLD.get(l, "?"), []).append(n)
    one = sum(max(v) for h, v in by_heb.items() if h != "?")
    many = sum(sum(v) for h, v in by_heb.items() if h != "?")
    return {"one_to_one": one / sum(c.values()), "many_to_one": many / sum(c.values())}


def task_ab(corpus, logical) -> dict:
    rec = {"stats": corpus_stats(logical, config.targets()["targets"], seed=0), "A": {}, "B": {},
           "n_texts": len(logical), "n_tokens": corpus.n_tokens}
    for M in A_METHODS:
        p = M().analyze(corpus)
        rec["A"][M.name] = {"score": p.ling_score, "vector": p.extra.get("vector"), "features": p.features}
    for M in B_METHODS:
        p = M().analyze(corpus)
        rec["B"][M.name] = {"pred": p.script_type, "features": p.script_features}
    return rec


# ---------------------------------------------------------------- yardsticks

def _gold_map(mapping: dict[str, str], t: list[str]) -> str:
    return "".join(mapping[x] for x in t if x != U.DIVIDER)


def _shuffled(rng) -> dict[str, str]:
    ks = sorted(U.GOLD)
    vs = [U.GOLD[k] for k in ks]
    return dict(zip(ks, rng.permutation(vs)))


def verbatim(texts, heb_blob: str, mapping, min_letters: int = 0) -> float:
    xs = [_gold_map(mapping, t) for t in texts]
    xs = [x for x in xs if len(x) >= max(min_letters, 1)]
    return sum(x in heb_blob for x in xs) / len(xs) if xs else float("nan")


def cognate_overlap(uw: dict, hw: set, mapping) -> tuple[float, float]:
    keys = list(uw)
    m = ["".join(mapping[x] for x in w) in hw for w in keys]
    types = sum(m) / len(keys)
    toks = sum(uw[k] for k, ok in zip(keys, m) if ok) / sum(uw.values())
    return types, toks


def bigram_jsd(a: list[list[str]], b: list[list[str]]) -> float:
    def dist(texts):
        c = Counter((t[i], t[i + 1]) for t in texts for i in range(len(t) - 1))
        n = sum(c.values())
        return {k: v / n for k, v in c.items()}
    p, q = dist(a), dist(b)
    ks = set(p) | set(q)
    P = np.array([p.get(k, 0.0) for k in ks])
    Q = np.array([q.get(k, 0.0) for k in ks])
    M = 0.5 * (P + Q)
    kl = lambda x: float(np.sum(x[x > 0] * np.log2(x[x > 0] / M[x > 0])))  # noqa: E731
    return 0.5 * (kl(P) + kl(Q))


def _sample_texts(texts, n_units: int, rng) -> list:
    """Whole texts in random order until n_units units are reached (size-matched sample)."""
    out, k = [], 0
    for i in rng.permutation(len(texts)):
        out.append(texts[i])
        k += len(texts[i])
        if k >= n_units:
            break
    return out


def _sample_tokens(words: Counter, n_tokens: int, rng) -> Counter:
    keys = list(words)
    p = np.array([words[k] for k in keys], dtype=float)
    idx = rng.choice(len(keys), size=n_tokens, p=p / p.sum())
    return Counter(keys[i] for i in idx)


def v1_sister_yardsticks(lang: str, n_letters: int, n_words: int) -> dict:
    """Same measures for a v1 language and its sister-v2 (alphabetic units): hidden half vs sister
    half mapped back through the true correspondence. Size-matched versions draw as many units
    (bigram JSD) or word tokens (cognate overlap) as the Ugaritic text has; chance levels use
    shuffled correspondences."""
    d = _segments(lang)
    words, rank = d["words"], d["_rank"]
    hid = split_clauses(lang, d, "hidden")[:MAX_REF_CLAUSES]
    htexts, hwords = [], Counter()
    for _, ids in hid:
        seq = []
        for w in ids:
            u = _word_units(words[w], "alphabetic", bool(rank[w] <= 250))
            seq += u
            if u:
                hwords[tuple(u)] += 1
        if seq:
            htexts.append(seq)
    sis = build_reference(lang, "alphabetic", True, 0)
    units = sorted({u for t in sis.texts for u in t})
    rng = np.random.default_rng(0)

    def back_map(perm=None):
        m = {u: sis.to_hidden.get(u, u) for u in units}
        if perm is not None:
            m = dict(zip(units, [m[units[i]] for i in perm]))
        return m

    def overlap(m, sample, sw=None):
        sw = sw if sw is not None else {tuple(m[u] for u in w) for w in sis.words}
        keys = list(sample)
        ok = [k in sw for k in keys]
        return sum(ok) / len(keys), sum(sample[k] for k, o in zip(keys, ok) if o) / sum(sample.values())

    true = back_map()
    stexts = [[true[u] for u in t] for t in sis.texts]
    samples = [_sample_tokens(hwords, n_words, rng) for _ in range(20)]
    sw_true = {tuple(true[u] for u in w) for w in sis.words}
    ov = np.array([overlap(true, smp, sw_true) for smp in samples])
    ch = np.array([overlap(back_map(rng.permutation(len(units))), smp) for smp in samples])
    return {"bigram_jsd": bigram_jsd(htexts, stexts),
            "bigram_jsd_size_matched": float(np.mean([bigram_jsd(_sample_texts(htexts, n_letters, rng), stexts)
                                                       for _ in range(20)])),
            "cognate_types_all": sum(k in sw_true for k in hwords) / len(hwords),
            "cognate_types": float(ov[:, 0].mean()), "cognate_tokens": float(ov[:, 1].mean()),
            "cognate_types_chance": float(ch[:, 0].mean()), "cognate_tokens_chance": float(ch[:, 1].mean()),
            "mergers": 0}


def yardsticks(refs) -> dict:
    seg = U.ugaritic_texts("segment")
    heb = refs["hebrew"]
    blob = "|".join("".join(t) for t in heb.texts)
    hw = {"".join(w) for w in heb.words}
    uw = U.ugaritic_words()
    rng = np.random.default_rng(0)
    shuf = [_shuffled(rng) for _ in range(N_SHUFFLE)]
    recut = U.recut(seg, INDUS_MEAN, 0)
    out = {"mergers": len({l for l in U.GOLD}) - len(set(U.GOLD.values())),
           "n_word_types": len(uw), "n_word_tokens": sum(uw.values())}
    for name, texts, ml in (("natural", seg, 0), ("natural_6plus", seg, 6), ("recut4.6", recut, 0)):
        out[f"verbatim_{name}"] = verbatim(texts, blob, U.GOLD, ml)
        out[f"verbatim_{name}_chance"] = float(np.mean([verbatim(texts, blob, m, ml) for m in shuf[:50]]))
    ct, ck = cognate_overlap(uw, hw, U.GOLD)
    ch = np.array([cognate_overlap(uw, hw, m) for m in shuf])
    out.update({"cognate_types": ct, "cognate_tokens": ck,
                "cognate_types_chance": float(ch[:, 0].mean()), "cognate_types_chance_p95": float(np.quantile(ch[:, 0], 0.95)),
                "cognate_tokens_chance": float(ch[:, 1].mean())})
    letters = [[U.GOLD[x] for x in t if x != U.DIVIDER] for t in seg]
    out["bigram_jsd"] = bigram_jsd(letters, heb.texts)
    out["bigram_jsd_poetic"] = bigram_jsd(letters, refs["hebrew-poetic"].texts)
    out["bigram_jsd_shuffled_mean"] = float(np.mean([bigram_jsd([[m[x] for x in t if x != U.DIVIDER] for t in seg],
                                                                heb.texts) for m in shuf[:50]]))
    out["bigram_jsd_hebrew_poetic_vs_whole"] = bigram_jsd(refs["hebrew-poetic"].texts, heb.texts)
    n_letters = sum(map(len, letters))
    out["bigram_jsd_hebrew_sample_floor"] = float(np.mean([bigram_jsd(_sample_texts(heb.texts, n_letters, rng), heb.texts)
                                                           for _ in range(20)]))
    out["v1_sister"] = {l: v1_sister_yardsticks(l, n_letters, sum(uw.values())) for l in LANGUAGES}
    return out


def main() -> None:
    refs = references()
    kn = tiers(refs)
    rec: dict = {"sources": {"eupt_pages": {U.EUPT_BASE + k: v for k, v in U.EUPT_PAGES.items()},
                             "eupt_version": U.EUPT_VERSION, "eupt_accessed": U.EUPT_ACCESSED,
                             "oshb_commit": U.OSHB_COMMIT, "gold": "Wikipedia 'Ugaritic alphabet' letters table "
                             "(read 2026-10-09), citing Kogan 2011 Tab. 6.2 (not read)"},
                 "reference_sizes": {k: {"texts": len(r.texts), "units": sum(map(len, r.texts)),
                                         "unit_types": len({u for t in r.texts for u in t})} for k, r in refs.items()},
                 "corpora": {}}
    for name, texts, seed in corpora():
        corpus, key, sid = U.to_corpus(texts, f"ugaritic-{name}", seed)
        logical = [t.tolist() for t in corpus.logical()]
        c = Counter(x for t in texts for x in t)
        r = {"n_texts": len(texts), "n_tokens": sum(c.values()), "n_letters": sum(v for k, v in c.items() if k != U.DIVIDER),
             "n_dividers": c[U.DIVIDER], "n_types": len(c), "mean_length": sum(c.values()) / len(texts),
             "dup_rate": 1 - len({tuple(t) for t in texts}) / len(texts), "ceilings": ceilings(texts),
             "AB": task_ab(corpus, logical), "D": {}}
        for tier, k in kn.items():
            r["D"][tier] = {}
            for M in D_METHODS:
                m = M(restarts=3, iterations=60) if issubclass(M, KnightEM) else M()
                p = m.analyze(corpus, k)
                r["D"][tier][M.name] = {**d_scores(p.sign_values, key, logical, sid),
                                        "reference": p.extra.get("reference"), "family": p.family,
                                        "family_scores": p.family_scores}
            print(f"[ugaritic] {name} {tier}: " + ", ".join(f"{m}={v['token_acc']:.3f}/{v['letters']:.3f}"
                                                        for m, v in r["D"][tier].items()), flush=True)
        if name == "natural":   # sensitivity: EM restart seed (primary uses the frozen default, 0)
            r["D_em_seeds"] = {f"{M.name}/seed{sd}": d_scores(M(restarts=3, iterations=60, seed=sd).analyze(
                corpus, kn["related"]).sign_values, key, logical, sid) for M in (KnightEMOriginal, KnightEM) for sd in (1, 2)}
        rec["corpora"][name] = r

    # Task A/B with the frozen rules, fit exactly as for Sproat's corpora.
    names = list(rec["corpora"])
    ab = [rec["corpora"][n]["AB"] for n in names]
    rec["AB_pools"] = {}
    for prof, reg in POOLS:
        train = pool(prof, reg)
        if not train:
            continue
        predict(ab, train)
        rec["AB_pools"][f"{prof}/{reg}"] = {n: {"A": a["A_pred"], "B": a["B_pred"],
                                                "entropy_ratio": a["A"].get("rao2009_entropy", {}).get("score")}
                                            for n, a in zip(names, ab)}
    rec["yardsticks"] = yardsticks(refs)
    for r in rec["corpora"].values():
        r["AB"] = {"stats": r["AB"]["stats"]}
    (OUT / "records.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False, default=float))
    print("[ugaritic] wrote", OUT / "records.json")


if __name__ == "__main__":
    main()
