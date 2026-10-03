"""Run every method on every corpus, then score tasks A-D.

Stage 1 (``run``): one job per corpus. The worker generates the corpus from calibrated knobs,
runs all methods, scores what can be scored without training (B rule, C, D), and appends a
JSON record to runs/results/<profile>/records.jsonl. Resumable: finished jobs are skipped.

Stage 2 (``aggregate``): trained decisions (Task A thresholds/bands/trees/logistic regression,
Task B classifiers) are fit with LEAVE-ONE-SOURCE-OUT cross-validation within each sweep point.
A corpus from Sanskrit is classified by a rule learned only on non-Sanskrit corpora. A heraldry
corpus is classified by a rule that never saw heraldry. Then success rates get Wilson 95%
intervals and mean accuracies get bootstrap 95% intervals.
"""

from __future__ import annotations

import json
import time
import traceback
from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

from . import config, ml
from .generator.build import LANGUAGES, make_corpus
from .generator.calibrate import load_knobs
from .knowledge import knowledge_for
from .methods.decipher import CognateMatcher, FrequencyRankBaseline, KnightEM, KnightEMOriginal
from .methods.descriptive import FulsPositional, RaoEntropy, YadavMarkov
from .methods.structural import (BranchingSegmentation, InventoryRule, LeeTree, MultiFeatureClassifier,
                                 ScriptTypeLR)
from .paths import ensure, runs_dir
from .scoring import (cluster_bootstrap, score_sign_values, segmentation_f1, summarize_binary,
                      summarize_clustered)
from .stats import check_targets, corpus_stats

A_METHODS = [RaoEntropy, YadavMarkov, FulsPositional, LeeTree, MultiFeatureClassifier]
B_METHODS = [InventoryRule, ScriptTypeLR, BranchingSegmentation]
D_METHODS = [FrequencyRankBaseline, KnightEM, KnightEMOriginal, CognateMatcher]


def _single_thread_blas() -> None:
    """Worker processes inherit this: one BLAS thread each, so N workers use N cores."""
    import os
    for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ.setdefault(v, "1")


def all_methods() -> list:
    return [m() for m in A_METHODS + B_METHODS + D_METHODS]


@dataclass(frozen=True)
class Job:
    sweep: str            # size | length | regime | feasibility | sister | predicted
    source: str
    script_type: str      # 'emblem' for controls
    seed: int
    n_texts: int
    mean_length: float
    regime: str = "full"
    scenario: int = -1    # feasibility scenario id
    tiers: tuple = ("related", "candidates", "none")
    sister: tuple = ()    # (sound_change_rate, lexical_replacement); () = config default
    pred_script: str = "" # predicted script type used for the solver's unit level ("" = oracle)

    def key(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


def build_jobs(profile: dict) -> list[Job]:
    srcs = [(l, st) for l in profile["languages"] for st in profile["script_types"]] + \
           [(c, "emblem") for c in profile["controls"]]
    ip = profile["indus_point"]
    jobs: list[Job] = []
    tiers = tuple(profile["knowledge_tiers"])
    for seed in profile["seeds"]:
        for (s, st) in srcs:
            for n in profile["size_sweep"]:
                jobs.append(Job("size", s, st, seed, n, ip["mean_length"], tiers=tiers))
            for L in profile["length_sweep"]:
                if abs(L - ip["mean_length"]) > 1e-9:
                    jobs.append(Job("length", s, st, seed, ip["n_texts"], L, tiers=tiers))
            for reg in profile["regimes"]:
                if reg != "full":
                    spec = config.regime_targets(reg)
                    jobs.append(Job("regime", s, st, seed, int(spec["n_texts"]["value"]),
                                    float(spec["mean_length"]["value"]), regime=reg, tiers=("related",)))
        # Sister-language distance sweep (Indus point, C/D only): how much of Task D is the free
        # distance parameter?
        for (s, st) in srcs:
            if st == "emblem":
                continue
            for lvl in profile.get("sister_sweep", []):
                jobs.append(Job("sister", s, st, seed, ip["n_texts"], ip["mean_length"],
                                tiers=("related", "candidates"), sister=tuple(lvl)))
    rng = np.random.default_rng(config.experiment()["master_seed"])
    for i in range(profile["feasibility_scenarios"]):
        lang = profile["languages"][int(rng.integers(len(profile["languages"])))]
        st = profile["script_types"][int(rng.integers(len(profile["script_types"])))]
        jobs.append(Job("feasibility", lang, st, 100 + i, ip["n_texts"], ip["mean_length"], scenario=i, tiers=tiers))
    return jobs


def feasibility_spec(spec, scenario: int):
    """Random writing-system parameters around the calibrated script (Judge fix #1)."""
    r = np.random.default_rng([config.experiment()["master_seed"], 7, scenario])
    return replace(spec,
                   allograph_rate=float(r.uniform(0, 0.8)), allograph_extra_mean=float(r.uniform(1, 8)),
                   homophony_rate=float(r.uniform(0, 0.4)), polyvalence_rate=float(r.uniform(0, 0.2)),
                   determinatives=bool(r.random() < 0.5) if spec.script_type != "alphabetic" else False,
                   word_divider=bool(r.random() < 0.3), direction="rtl" if r.random() < 0.7 else "ltr")


def run_job(job: Job, em_restarts: int = 3, em_iterations: int = 60, generator_version: str = "v1") -> dict[str, Any]:
    t0 = time.time()
    knobs, spec = load_knobs(job.regime, job.source, job.script_type, generator_version)
    if job.sweep == "feasibility":
        spec = feasibility_spec(spec, job.scenario)
    regime_t = config.regime_targets(job.regime)
    median = float(regime_t["median_length"]["value"]) if job.sweep == "regime" else None
    corpus, key, info = make_corpus(job.source, spec, job.n_texts, job.mean_length, job.seed, knobs,
                                    median_length=median, generator_version=generator_version)
    logical = [t.tolist() for t in corpus.logical()]
    st = corpus_stats(logical, config.targets()["targets"], seed=job.seed)
    rec: dict[str, Any] = {
        "job": asdict(job), "generator_version": generator_version,
        "truth": {"source": key.source, "family": key.family, "kind": key.kind,
                  "is_linguistic": key.is_linguistic, "script_type": key.script_type},
        "stats": st, "gen": info,
        "calibration": {k: v["ok"] for k, v in check_targets(st, regime_t).items()},
        "A": {}, "B": {}, "CD": {}, "timing": {},
    }
    cd_only = job.sweep in ("sister", "predicted")
    for M in ([] if cd_only else A_METHODS):
        m = M()
        t = time.time()
        p = m.analyze(corpus)
        rec["A"][m.name] = {"score": p.ling_score, "vector": p.extra.get("vector"), "features": p.features}
        rec["timing"][m.name] = time.time() - t
    for M in ([] if cd_only else B_METHODS):
        m = M()
        t = time.time()
        p = m.analyze(corpus)
        rec["B"][m.name] = {"pred": p.script_type, "features": p.script_features}
        if p.segmentation is not None and key.kind == "language":
            rec["seg_f1"] = segmentation_f1(p.segmentation, key)
        rec["timing"][m.name] = time.time() - t
    if key.kind == "language":
        unit_script = job.pred_script or job.script_type
        sis = {"sound_change_rate": job.sister[0], "lexical_replacement": job.sister[1]} if job.sister else {}
        for tier in job.tiers:
            kn = knowledge_for(job.source, unit_script, tier, job.seed,
                               logogram_vocab=spec.logogram_vocab, **sis)
            fams = sorted({r.family for r in kn.references})
            rec["CD"][tier] = {"_families": fams}
            for M in D_METHODS:
                m = M(restarts=em_restarts, iterations=em_iterations) if issubclass(M, KnightEM) else M()
                t = time.time()
                p = m.analyze(corpus, kn)
                s = score_sign_values(p.sign_values, key, logical)
                rec["CD"][tier][m.name] = {"family": p.family, "reference": p.extra.get("reference"),
                                           "family_correct": p.family == key.family, **s}
                rec["timing"][f"{m.name}:{tier}"] = time.time() - t
    rec["timing"]["total"] = time.time() - t0
    return rec


def _worker(args):
    job, path, er, ei, gv = args
    try:
        rec = run_job(job, er, ei, gv)
    except Exception:  # noqa: BLE001 - record and continue; failures are reported, not hidden
        rec = {"job": asdict(job), "error": traceback.format_exc()}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, default=float) + "\n")
    return job.sweep, job.source, job.script_type, job.n_texts, job.mean_length, "error" in rec


def results_path(profile_name: str) -> Path:
    return ensure(runs_dir() / "results" / profile_name) / "records.jsonl"


def load_records(profile_name: str) -> list[dict]:
    p = results_path(profile_name)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def _execute(jobs: list[Job], profile_name: str, workers: int, log) -> None:
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from multiprocessing import get_context
    _single_thread_blas()
    prof = config.experiment()["profiles"][profile_name]
    done = {json.dumps(r["job"], sort_keys=True) for r in load_records(profile_name) if "error" not in r}
    todo = [j for j in jobs if j.key() not in done]
    # Expensive jobs first so the pool finishes evenly.
    todo.sort(key=lambda j: -(j.n_texts * j.mean_length * (3 if j.script_type != "emblem" else 1)))
    log(f"[run] {profile_name}: {len(jobs)} jobs, {len(todo)} to do, {workers} workers")
    if not todo:
        return
    path = results_path(profile_name)
    args = [(j, path, prof["em_restarts"], prof["em_iterations"], prof.get("generator_version", "v1")) for j in todo]
    t0 = time.time()
    with ProcessPoolExecutor(workers, mp_context=get_context("spawn")) as ex:
        futs = [ex.submit(_worker, a) for a in args]
        for i, f in enumerate(as_completed(futs), 1):
            try:
                r = f.result()
            except Exception as e:  # noqa: BLE001 - a dead worker loses one job; rerun resumes it
                log(f"[run] worker failure: {e!r}")
                continue
            if i % 20 == 0 or r[-1]:
                log(f"[run] {i}/{len(todo)} {time.time() - t0:.0f}s last={r}")


def predicted_script_jobs(profile_name: str) -> list[Job]:
    """Stage 2: re-run C/D at the Indus point with the PREDICTED script type (no oracle).

    The prediction is the leave-one-source-out output of script_type_lr from stage 1, so the
    solver's unit level comes from a classifier that never saw the corpus's source language.
    """
    prof = config.experiment()["profiles"][profile_name]
    ip = prof["indus_point"]
    recs = [r for r in load_records(profile_name) if "error" not in r and r["job"]["sweep"] == "size"
            and r["job"]["n_texts"] == ip["n_texts"] and r["job"]["regime"] == "full"]
    if not recs:
        return []
    loso_predictions(recs)
    jobs = []
    for r in recs:
        if r["truth"]["kind"] != "language":
            continue
        pred = r["B_pred"].get(ScriptTypeLR.name)
        if not pred:
            continue
        j = r["job"]
        jobs.append(Job("predicted", j["source"], j["script_type"], j["seed"], j["n_texts"], j["mean_length"],
                        tiers=tuple(prof["knowledge_tiers"]), pred_script=pred))
    return jobs


def run(profile_name: str, workers: int = 4, log=print) -> None:
    prof = config.experiment()["profiles"][profile_name]
    _execute(build_jobs(prof), profile_name, workers, log)
    _execute(predicted_script_jobs(profile_name), profile_name, workers, log)


# --------------------------------------------------------------------------- aggregation

A_ELIGIBLE = {"language", "structural", "adversarial", "trivial"}


def _point(rec) -> tuple:
    j = rec["job"]
    return (j["sweep"], j["n_texts"], j["mean_length"], j["regime"])


def _a_decide(method: str, train: list[dict], test: list[dict]) -> list[bool]:
    m = {c.name: c for c in A_METHODS}[method]
    ytr = np.array([r["truth"]["is_linguistic"] for r in train])
    if m.decision in ("lr",):
        Xtr = np.array([r["A"][method]["vector"] for r in train], dtype=float)
        Xte = np.array([r["A"][method]["vector"] for r in test], dtype=float)
        model = ml.fit_logreg(Xtr, ytr)
        return list(ml.predict_logreg(model, Xte) > 0.5)
    if m.decision == "tree2":
        Xtr = np.array([r["A"][method]["vector"] for r in train], dtype=float)
        Xte = np.array([r["A"][method]["vector"] for r in test], dtype=float)
        c1, d1 = ml.fit_threshold(Xtr[:, 0], ytr)
        p1 = ml.apply_threshold(Xtr[:, 0], c1, d1)
        if p1.sum() >= 2 and len(set(ytr[p1])) > 1:
            c2, d2 = ml.fit_threshold(Xtr[p1, 1], ytr[p1])
        else:
            c2, d2 = -np.inf, 1
        out = ml.apply_threshold(Xte[:, 0], c1, d1) & ml.apply_threshold(Xte[:, 1], c2, d2)
        return list(out)
    xtr = np.array([r["A"][method]["score"] for r in train], dtype=float)
    xte = np.array([r["A"][method]["score"] for r in test], dtype=float)
    if m.decision == "band":
        lo, hi, inside = ml.fit_band(xtr, ytr)
        return list(ml.apply_band(xte, lo, hi, inside))
    c, d = ml.fit_threshold(xtr, ytr)
    return list(ml.apply_threshold(xte, c, d))


def _b_features(rec, method) -> list[float]:
    f = rec["B"][method]["features"]
    return [float(f[k]) for k in sorted(f)]


def loso_predictions(records: list[dict], train_pool: list[dict] | None = None) -> None:
    """Fill rec['A_pred'][method] and rec['B_pred'][method] in place (leave-one-source-out)."""
    pool = train_pool if train_pool is not None else records
    a_pool = [r for r in pool if r["truth"]["kind"] in A_ELIGIBLE]
    b_pool = [r for r in pool if r["truth"]["kind"] == "language"]
    for r in records:
        r.setdefault("A_pred", {})
        r.setdefault("B_pred", {})
    by_src = defaultdict(list)
    for r in records:
        by_src[r["truth"]["source"]].append(r)
    for src, test in by_src.items():
        tr_a = [r for r in a_pool if r["truth"]["source"] != src]
        if len({r["truth"]["is_linguistic"] for r in tr_a}) == 2:
            for M in A_METHODS:
                for r, p in zip(test, _a_decide(M.name, tr_a, test)):
                    r["A_pred"][M.name] = bool(p)
        lang_test = [r for r in test if r["truth"]["kind"] == "language"]
        if not lang_test:
            continue
        tr_b = [r for r in b_pool if r["truth"]["source"] != src]
        for r in lang_test:
            r["B_pred"][InventoryRule.name] = r["B"][InventoryRule.name]["pred"]
        for M in (ScriptTypeLR, BranchingSegmentation):
            if len({r["truth"]["script_type"] for r in tr_b}) < 2:
                continue
            model = ml.fit_softmax(np.array([_b_features(r, M.name) for r in tr_b]),
                                   [r["truth"]["script_type"] for r in tr_b])
            preds = ml.predict_softmax(model, np.array([_b_features(r, M.name) for r in lang_test]))
            for r, p in zip(lang_test, preds):
                r["B_pred"][M.name] = p


def _ba_stat(items) -> float:
    y = np.array([a for a, _ in items], bool)
    p = np.array([b for _, b in items], bool)
    if y.all() or (~y).all():
        raise ValueError("one class missing in resample")
    return ml.balanced_accuracy(y, p)


def cd_tables(records: list[dict]) -> dict[str, Any]:
    """Tasks C and D. Intervals: cluster bootstrap over source languages (corpora from one
    language are not independent)."""
    out: dict[str, Any] = {"C": {}, "D": {}}
    b_recs = [r for r in records if r["truth"]["kind"] == "language"]
    for tier in ("related", "candidates", "none"):
        out["C"][tier], out["D"][tier] = {}, {}
        recs = [r for r in b_recs if tier in r.get("CD", {})]
        if not recs:
            continue
        chance = float(np.mean([1.0 / len(r["CD"][tier]["_families"]) for r in recs]))
        for M in D_METHODS:
            sel = [r for r in recs if M.name in r["CD"][tier]]
            if not sel:
                continue
            vals = [r["CD"][tier][M.name] for r in sel]
            cl = [r["truth"]["source"] for r in sel]
            if tier != "related":
                out["C"][tier][M.name] = {**summarize_clustered([v["family_correct"] for v in vals], cl), "chance": chance}
            acc = np.array([v["token_acc"] for v in vals])
            lo, hi = cluster_bootstrap(acc, cl)
            out["D"][tier][M.name] = {"mean_token_acc": float(acc.mean()), "ci_lo": lo, "ci_hi": hi,
                                      "success50": summarize_clustered(list(acc >= 0.5), cl),
                                      "mean_type_acc": float(np.mean([v["type_acc"] for v in vals])),
                                      "n": len(vals)}
    return out


def task_tables(records: list[dict]) -> dict[str, Any]:
    """Success rates per method for one group of records (already LOSO-predicted).

    Task A per-family rates use Wilson intervals (one family = one source). Every pooled rate
    uses a cluster bootstrap over sources.
    """
    out: dict[str, Any] = {"A": {}, "A_by_kind": {}, "B": {}}
    a_recs = [r for r in records if r["truth"]["kind"] in A_ELIGIBLE]
    for M in A_METHODS:
        sel = [r for r in a_recs if M.name in r.get("A_pred", {})]
        if not sel:
            continue
        y = np.array([r["truth"]["is_linguistic"] for r in sel])
        p = np.array([r["A_pred"][M.name] for r in sel])
        cl = [r["truth"]["source"] for r in sel]
        lo, hi = cluster_bootstrap(list(zip(y, p)), cl, stat=_ba_stat, n_boot=500)
        cl_arr = np.array(cl, dtype=object)
        out["A"][M.name] = {"balanced_acc": ml.balanced_accuracy(y, p), "ci_lo": lo, "ci_hi": hi,
                            "ling_recall": summarize_clustered(list(p[y]), list(cl_arr[y])),
                            "nonling_specificity": summarize_clustered(list(~p[~y]), list(cl_arr[~y]))}
        kinds = defaultdict(list)
        for r in records:
            if M.name in r.get("A_pred", {}):
                kinds[r["truth"]["source"] if r["truth"]["kind"] != "language" else "language"].append(r["A_pred"][M.name])
        out["A_by_kind"][M.name] = {k: summarize_binary(v) for k, v in kinds.items()}  # share called 'linguistic'
    b_recs = [r for r in records if r["truth"]["kind"] == "language"]
    for name in (InventoryRule.name, ScriptTypeLR.name, BranchingSegmentation.name):
        sel = [r for r in b_recs if name in r.get("B_pred", {})]
        if sel:
            out["B"][name] = summarize_clustered([r["B_pred"][name] == r["truth"]["script_type"] for r in sel],
                                                 [r["truth"]["source"] for r in sel])
    out.update(cd_tables(records))
    return out


def _passes(r: dict) -> bool:
    return bool(r.get("calibration")) and all(r["calibration"].values())


def aggregate(profile_name: str) -> dict[str, Any]:
    recs = [r for r in load_records(profile_name) if "error" not in r]
    errors = [r for r in load_records(profile_name) if "error" in r]
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in recs:
        if r["job"]["sweep"] in ("size", "length", "regime"):
            groups[_point(r)].append(r)
    prof = config.experiment()["profiles"][profile_name]
    ip = prof["indus_point"]
    indus_key = ("size", ip["n_texts"], ip["mean_length"], "full")
    out: dict[str, Any] = {"profile": profile_name, "n_records": len(recs), "n_errors": len(errors),
                           "points": {}, "feasibility": None, "sister": {}, "predicted": None}
    for k, g in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][3], kv[0][1], kv[0][2])):
        loso_predictions(g)
        entry = {"sweep": k[0], "n_texts": k[1], "mean_length": k[2], "regime": k[3],
                 "n_corpora": len(g), "tables": task_tables(g),
                 "seg_f1": float(np.mean([r["seg_f1"] for r in g if "seg_f1" in r] or [np.nan]))}
        # Robustness (reviewer fix 3): only corpora that meet EVERY target of their regime,
        # with the leave-one-source-out rules re-learned inside that subset.
        passing = [dict(r, A_pred={}, B_pred={}) for r in g if _passes(r)]
        entry["n_passing"] = len(passing)
        entry["n_passing_languages"] = sum(r["truth"]["kind"] == "language" for r in passing)
        if passing:
            loso_predictions(passing)
            entry["tables_passing"] = task_tables(passing)
        out["points"][json.dumps(k)] = entry
    feas = [r for r in recs if r["job"]["sweep"] == "feasibility"]
    if feas and indus_key in groups:
        loso_predictions(feas, train_pool=groups[indus_key])
        out["feasibility"] = {"n_scenarios": len(feas), "tables": task_tables(feas),
                              "calibration_pass_rate": float(np.mean([np.mean(list(r["calibration"].values())) for r in feas]))}
    sis = defaultdict(list)
    for r in recs:
        if r["job"]["sweep"] == "sister":
            sis[tuple(r["job"]["sister"])].append(r)
    for lvl, g in sorted(sis.items()):
        out["sister"][json.dumps(list(lvl))] = {"sound_change_rate": lvl[0], "lexical_replacement": lvl[1],
                                                "n_corpora": len(g), "tables": cd_tables(g)}
    pred = [r for r in recs if r["job"]["sweep"] == "predicted"]
    if pred:
        keyf = lambda j: (j["source"], j["script_type"], j["seed"])  # noqa: E731
        oracle_by = {keyf(r["job"]): r for r in groups.get(indus_key, [])}
        oracle = [oracle_by[keyf(r["job"])] for r in pred if keyf(r["job"]) in oracle_by]
        out["predicted"] = {"n_corpora": len(pred),
                            "script_type_correct": float(np.mean([r["job"]["pred_script"] == r["truth"]["script_type"] for r in pred])),
                            "tables": cd_tables(pred), "oracle_tables": cd_tables(oracle)}
    out["errors"] = [e["error"][-500:] for e in errors[:5]]
    return out
