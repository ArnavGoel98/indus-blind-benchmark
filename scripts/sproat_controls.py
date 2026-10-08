"""Held-out control family: Sproat's non-linguistic symbol corpora on Tasks A and B.

No retraining and no method changes. Every method runs unchanged on each corpus; the Task A rules
and Task B classifiers are fit exactly as for the feasibility scenarios (evaluate.aggregate): on the
existing Indus-point records of a finished run, then applied to corpora that run never saw. Each
system is scored at native size, and on samples of 2,906 whole texts (seeds 0-2) where it has
that many texts. Used with the author's permission; cite Sproat (2014) and Wu, Solman, Linehan &
Sproat (2012).

Usage: python scripts/sproat_controls.py
Writes reports/sproat_controls/{records.jsonl,results.json,sproat_controls.md}.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict

import numpy as np

from ibdb import config, ml
from ibdb.data import sproat
from ibdb.evaluate import (A_METHODS, A_ELIGIBLE, B_METHODS, _a_decide, _b_features, load_records)
from ibdb.methods.structural import BranchingSegmentation, InventoryRule, ScriptTypeLR
from ibdb.paths import ensure, reports_dir
from ibdb.stats import corpus_stats

OUT = ensure(reports_dir() / "sproat_controls")
N_INDUS, SEEDS = 2906, [0, 1, 2]
# Training pools: (profile, regime). 'full' seeds 0-2 is the main run; 'replication' is fresh seeds.
POOLS = [("full", "full"), ("full", "holdout"), ("replication", "full"), ("replication", "holdout")]
IID = "rao_type2"     # our key for the i.i.d. random-order control (Section 3.5 names controls by behaviour)


def analyze(system: str, texts, tag: str) -> dict:
    corpus = sproat.to_corpus(system, texts, tag)
    logical = [t.tolist() for t in corpus.logical()]
    rec = {"system": system, "tag": tag, "disputed": system in sproat.DISPUTED,
           "n_texts": len(texts), "n_tokens": corpus.n_tokens,
           "n_types": len({s for t in texts for s in t}),
           "mean_length": corpus.n_tokens / len(texts),
           "dup_rate": 1 - len({tuple(t) for t in texts}) / len(texts),
           "stats": corpus_stats(logical, config.targets()["targets"], seed=0), "A": {}, "B": {}}
    for M in A_METHODS:
        p = M().analyze(corpus)
        rec["A"][M.name] = {"score": p.ling_score, "vector": p.extra.get("vector"), "features": p.features}
    for M in B_METHODS:
        p = M().analyze(corpus)
        rec["B"][M.name] = {"pred": p.script_type, "features": p.script_features}
    return rec


def pool(profile: str, regime: str) -> list[dict]:
    ip = config.experiment()["profiles"][profile]["indus_point"]
    sweep = "size" if regime == "full" else "regime"
    out = [r for r in load_records(profile) if "error" not in r and r["job"]["sweep"] == sweep
           and r["job"]["regime"] == regime]
    if regime == "full":
        out = [r for r in out if r["job"]["n_texts"] == ip["n_texts"]
               and abs(r["job"]["mean_length"] - ip["mean_length"]) < 1e-9]
    return out


def predict(recs: list[dict], train: list[dict]) -> None:
    """Same fitting as evaluate.loso_predictions with a train_pool that excludes every test source."""
    tr_a = [r for r in train if r["truth"]["kind"] in A_ELIGIBLE]
    tr_b = [r for r in train if r["truth"]["kind"] == "language"]
    for r in recs:
        r["A_pred"], r["B_pred"] = {}, {}
    for M in A_METHODS:
        for r, p in zip(recs, _a_decide(M.name, tr_a, recs)):
            r["A_pred"][M.name] = bool(p)
    for r in recs:
        r["B_pred"][InventoryRule.name] = r["B"][InventoryRule.name]["pred"]
    for M in (ScriptTypeLR, BranchingSegmentation):
        model = ml.fit_softmax(np.array([_b_features(r, M.name) for r in tr_b]),
                               [r["truth"]["script_type"] for r in tr_b])
        for r, p in zip(recs, ml.predict_softmax(model, np.array([_b_features(r, M.name) for r in recs]))):
            r["B_pred"][M.name] = p


def main() -> None:
    recs = []
    for s in sproat.SYSTEMS:
        texts = sproat.load_texts(s)
        recs.append(analyze(s, texts, "native"))
        for seed, smp in zip(SEEDS, sproat.indus_size_samples(texts, N_INDUS, SEEDS)):
            recs.append(analyze(s, smp, f"indus{seed}"))
        print(f"[sproat] {s}: {sum(r['system'] == s for r in recs)} corpora")
    with open(OUT / "records.jsonl", "w") as fh:
        for r in recs:
            fh.write(json.dumps(r, default=float) + "\n")

    results: dict = {"systems": {}, "pools": {}}
    for r in recs:
        if r["tag"] == "native":
            results["systems"][r["system"]] = {k: r[k] for k in ("n_texts", "n_tokens", "n_types",
                                                                 "mean_length", "dup_rate", "disputed")}
    for prof, reg in POOLS:
        train = pool(prof, reg)
        if not train:
            continue
        predict(recs, train)
        key = f"{prof}/{reg}"
        ratio = defaultdict(list)
        for t in train:
            ratio["language" if t["truth"]["kind"] == "language" else t["truth"]["source"]].append(
                t["A"]["rao2009_entropy"]["score"] if "rao2009_entropy" in t["A"] else np.nan)
        res = {"n_train": len(train), "train_entropy_ratio": {k: float(np.nanmean(v)) for k, v in ratio.items()},
               "corpora": []}
        for r in recs:
            res["corpora"].append({"system": r["system"], "tag": r["tag"], "disputed": r["disputed"],
                                   "A_pred": r["A_pred"], "B_pred": r["B_pred"],
                                   "entropy_ratio": r["A"].get("rao2009_entropy", {}).get("score")})
        results["pools"][key] = res
    (OUT / "results.json").write_text(json.dumps(results, indent=1, default=float))
    write_md(results)


def _share(cs, method, sel) -> str:
    v = [c["A_pred"][method] for c in cs if sel(c)]
    return f"{sum(v)}/{len(v)}" if v else "-"


def write_md(res: dict) -> None:
    a_names = [M.name for M in A_METHODS]
    L = ["# Sproat non-linguistic corpora: held-out control family (Tasks A and B)", "",
         "Used with the author's permission. Cite Sproat (2014) and Wu, Solman, Linehan & Sproat (2012).",
         "Methods frozen; rules fit on the named run's Indus-point records and applied unchanged (no retraining).",
         "IndusBarSeals excluded (it is the Indus script). Pictish reported separately (status disputed).", "",
         "## Corpora (native size, Sproat's xtract.py defaults)", "",
         "| System | Texts | Tokens | Types | Mean length | Duplicate rate |", "|---|---|---|---|---|---|"]
    for s, d in res["systems"].items():
        L.append(f"| {s}{' (disputed)' if d['disputed'] else ''} | {d['n_texts']} | {d['n_tokens']} | {d['n_types']} | "
                 f"{d['mean_length']:.2f} | {d['dup_rate']:.3f} |")
    for key, p in res["pools"].items():
        cs = p["corpora"]
        L += ["", f"## Rules fit on `{key}` ({p['n_train']} training corpora)", "",
              "Task A: corpora labelled 'linguistic' / corpora scored (every corpus here is non-linguistic, so any label of 'linguistic' is a false positive).", "",
              "| System | Size | " + " | ".join(a_names) + " | Entropy ratio |", "|---|---|" + "---|" * (len(a_names) + 1)]
        for s in res["systems"]:
            for tag, sel in (("native", lambda c, s=s: c["system"] == s and c["tag"] == "native"),
                             ("2,906 x3", lambda c, s=s: c["system"] == s and c["tag"] != "native")):
                if not any(sel(c) for c in cs):
                    continue
                er = [c["entropy_ratio"] for c in cs if sel(c) and c["entropy_ratio"] is not None]
                L.append(f"| {s} | {tag} | " + " | ".join(_share(cs, m, sel) for m in a_names) +
                         f" | {np.mean(er):.3f} |" if er else " | - |")
        und = lambda c: not c["disputed"]  # noqa: E731
        L.append("| **All undisputed** | all | " + " | ".join(_share(cs, m, und) for m in a_names) + " | |")
        tr = p["train_entropy_ratio"]
        L += ["", f"Training-pool mean entropy ratio: synthetic languages {tr.get('language', float('nan')):.3f}; "
              f"i.i.d. random control {tr.get(IID, float('nan')):.3f}.", "",
              "Task B: predicted script type (no non-linguistic option exists, so every prediction is wrong by construction).", "",
              "| Method | Predictions over all corpora |", "|---|---|"]
        for m in (InventoryRule.name, ScriptTypeLR.name, BranchingSegmentation.name):
            L.append(f"| {m} | " + ", ".join(f"{k} {v}" for k, v in Counter(c["B_pred"][m] for c in cs).most_common()) + " |")
    (OUT / "sproat_controls.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
