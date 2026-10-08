"""Sensitivity sweep: duplicate-text rate x sign inventory at the Indus point (methods frozen).

Published Indus statistics constrain neither how many texts are exact repeats nor how many
graphic variants of one sign a sign list counts as separate signs. Generator-v2 showed that
moving these two properties alone triples Task D accuracy. This module varies them
independently on a grid and maps decipherment accuracy over both.

Two controls, both outside the method code:

* **Duplicate rate (exact).** In this generator, allographs hide repeats: switching
  allographs off turns 26-88% of texts into exact repeats. So `rho` cannot set the duplicate
  rate independently of the inventory. Instead a pool of 3x the needed texts is generated
  with rho = 0. The corpus is then assembled from (1-d)*N distinct texts plus d*N copies of
  them. Slot lengths follow the usual Indus length distribution. A copy's source is drawn in
  proportion to how often its plaintext occurs in the pool, so popular formulae recur.
  The realized duplicate fraction is exactly round(d*N)/N.
* **Inventory (via allographs).** One scalar u sets the allograph knobs: u <= 1 gives
  allograph_rate = u with one variant; u > 1 gives allograph_rate = 1 with exp(u-1) variants
  on average. u is bisected until the realized inventory of the *assembled* corpus is
  within tolerance of the target. A target below the inventory at u = 0 is unreachable for
  that script and is recorded as such (no methods are run).

All other knobs keep their `full`-regime calibrated values, so the remaining calibration
targets are NOT re-fit in each cell: each record stores its full statistics so the drift is
visible.
"""

from __future__ import annotations

import json
import os
import math
import time
import traceback
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

import numpy as np

from . import config
from .corpus import AnswerKey, Corpus
from .evaluate import D_METHODS, KnightEM, _single_thread_blas
from .generator import sampler
from .generator.build import Knobs, make_corpus
from .generator.calibrate import load_knobs
from .evaluate import token_acc_before_cognate
from .knowledge import knowledge_for
from .paths import ensure, runs_dir
from .scoring import cluster_bootstrap, score_sign_values
from .stats import corpus_stats

POOL_FACTORS = (3, 8)   # pool size in multiples of N; the larger pool is tried only if needed
U_MAX = 1.0 + math.log(400.0)   # up to ~400 variants per sign on average (alphabetic at 800 signs)


@dataclass(frozen=True)
class SensJob:
    source: str
    script_type: str
    seed: int
    dup: float          # target duplicate-text fraction
    inventory: int      # target sign inventory
    n_texts: int = 2906
    mean_length: float = 4.6
    tiers: tuple = ("candidates", "none")

    def key(self) -> str:
        return json.dumps(asdict(self), sort_keys=True)


def allograph_knobs(knobs: Knobs, u: float) -> Knobs:
    if u <= 1.0:
        return replace(knobs, rho=0.0, allograph_rate=max(u, 0.0), allograph_extra_mean=1.0)
    return replace(knobs, rho=0.0, allograph_rate=1.0, allograph_extra_mean=float(math.exp(u - 1.0)))


def assemble(pool: Corpus, pkey: AnswerKey, n: int, mean_length: float, dup: float, seed: int,
             corpus_id: str) -> tuple[Corpus, AnswerKey, dict]:
    """Corpus of n texts with exactly round(dup*n) duplicates, drawn from a rho=0 pool."""
    rng = np.random.default_rng([seed, 0x5E45, int(round(dup * 1000))])
    lengths = sampler.draw_lengths(rng, n, mean_length)
    n_dup = int(round(dup * n))
    logical = [tuple(t.tolist()) for t in pool.logical()]
    # Distinct pool texts by length, in pool order (the pool order is already random).
    first: dict[tuple, int] = {}
    for i, t in enumerate(logical):
        if t and t not in first:
            first[t] = i
    by_len: dict[int, list[int]] = defaultdict(list)
    for t, i in first.items():
        by_len[len(t)].append(i)
    popularity = Counter(pkey.plaintext)
    slots = rng.permutation(n)
    uniq_slots, dup_slots = slots[: n - n_dup], slots[n - n_dup:]
    chosen: dict[int, int] = {}          # slot -> pool index
    cursor = {L: 0 for L in by_len}
    n_len_sub = 0

    def take(L: int) -> int:
        nonlocal n_len_sub
        avail = [m for m in by_len if cursor[m] < len(by_len[m])]
        if not avail:
            raise PoolExhausted("not enough distinct texts")
        m = L if L in avail else min(avail, key=lambda x: (abs(x - L), x))
        n_len_sub += m != L
        i = by_len[m][cursor[m]]
        cursor[m] += 1
        return i

    for s in uniq_slots.tolist():
        chosen[s] = take(int(lengths[s]))
    uniq_by_len: dict[int, list[int]] = defaultdict(list)
    for i in chosen.values():
        uniq_by_len[len(logical[i])].append(i)
    for s in dup_slots.tolist():
        L = int(lengths[s])
        m = L if L in uniq_by_len else min(uniq_by_len, key=lambda x: (abs(x - L), x))
        n_len_sub += m != L
        cand = uniq_by_len[m]
        w = np.array([popularity[pkey.plaintext[i]] for i in cand], dtype=float)
        chosen[s] = cand[int(rng.choice(len(cand), p=w / w.sum()))]
    order = [chosen[s] for s in range(n)]
    texts = [pool.texts[i].copy() for i in order]
    used = {int(x) for t in texts for x in t.tolist()}
    key = AnswerKey(corpus_id, pkey.source, pkey.family, pkey.kind, pkey.is_linguistic, pkey.script_type,
                    {s: v for s, v in pkey.sign_values.items() if s in used},
                    [list(pkey.token_values[i]) for i in order], [list(pkey.word_starts[i]) for i in order],
                    dict(pkey.params, dup_target=dup), [pkey.plaintext[i] for i in order])
    corpus = Corpus(corpus_id, texts, pool.direction, {"corpus_id": corpus_id, "n_texts": n})
    return corpus, key, {"length_substitutions": n_len_sub, "pool_distinct": len(first)}


class PoolExhausted(RuntimeError):
    """Not enough distinct texts: this (script, allograph level) cannot reach so low a duplicate rate."""


def controlled_corpus(job: SensJob, u: float, knobs: Knobs, spec) -> tuple[Corpus, AnswerKey, dict]:
    k = allograph_knobs(knobs, u)
    cid = f"sens-{job.source}-{job.script_type}-s{job.seed}-d{job.dup:.2f}-i{job.inventory}"
    for factor in POOL_FACTORS:
        pool, pkey, _ = make_corpus(job.source, spec, factor * job.n_texts, job.mean_length, job.seed, k,
                                    corpus_id="pool")
        try:
            c, key, info = assemble(pool, pkey, job.n_texts, job.mean_length, job.dup, job.seed, cid)
            info["pool_factor"] = factor
            return c, key, info
        except PoolExhausted:
            continue
    raise PoolExhausted(f"{factor}x pool has too few distinct texts")


def _inventory(c: Corpus) -> int:
    return len({int(x) for t in c.texts for x in t.tolist()})


def fit_inventory(job: SensJob, knobs: Knobs, spec, tol_frac: float = 0.03, tol_abs: int = 10,
                  max_iter: int = 14) -> dict[str, Any]:
    """Bisect the allograph scalar u so the assembled corpus hits the target inventory."""
    target = job.inventory
    tol = max(tol_abs, int(round(tol_frac * target)))
    trace = []

    def ev(u):
        try:
            c, k, info = controlled_corpus(job, u, knobs, spec)
        except PoolExhausted:
            trace.append((round(u, 4), None))
            return None, None, None, None
        inv = _inventory(c)
        trace.append((round(u, 4), inv))
        return c, k, info, inv

    lo, hi = 0.0, U_MAX
    best = (math.inf, None, None, None, None, None)
    c, k, info, inv = ev(lo)
    if inv is not None:
        best = (abs(inv - target), lo, c, k, info, inv)
        if inv > target + tol:
            return {"status": "unreachable_low", "inventory_at_u0": inv, "trace": trace}
    if best[0] > tol:
        c, k, info, inv = ev(hi)
        if inv is None:
            return {"status": "unreachable_dup", "trace": trace}
        if inv < target - tol:
            return {"status": "unreachable_high", "inventory_at_umax": inv, "trace": trace}
        if abs(inv - target) < best[0]:
            best = (abs(inv - target), hi, c, k, info, inv)
        for _ in range(max_iter):
            if best[0] <= tol:
                break
            mid = 0.5 * (lo + hi)
            c, k, info, inv = ev(mid)
            if inv is not None and abs(inv - target) < best[0]:
                best = (abs(inv - target), mid, c, k, info, inv)
            if inv is None or inv < target:   # too few distinct texts also means "more variants"
                lo = mid
            else:
                hi = mid
    err, u, c, k, info, inv = best
    if c is None:
        return {"status": "unreachable_dup", "trace": trace}
    return {"status": "ok" if err <= tol else "tolerance_miss", "u": u, "corpus": c, "key": k, "info": info,
            "inventory": inv, "trace": trace}


def run_sens_job(job: SensJob, em_restarts: int = 3, em_iterations: int = 60) -> dict[str, Any]:
    t0 = time.time()
    knobs, spec = load_knobs("full", job.source, job.script_type)
    fit = fit_inventory(job, knobs, spec)
    rec: dict[str, Any] = {"job": asdict(job), "sister_version": os.environ.get("IBDB_SISTER_VERSION", "v1"),
                           "status": fit["status"], "trace": fit["trace"], "CD": {}, "timing": {}}
    rec["timing"]["fit"] = time.time() - t0
    if fit["status"] not in ("ok", "tolerance_miss"):
        rec.update({k: v for k, v in fit.items() if k.startswith("inventory_at")})
        return rec
    corpus, key = fit["corpus"], fit["key"]
    logical = [t.tolist() for t in corpus.logical()]
    ak = allograph_knobs(knobs, fit["u"])
    rec.update({"u": fit["u"], "allograph_rate": ak.allograph_rate, "allograph_extra_mean": ak.allograph_extra_mean,
                "gen": fit["info"], "stats": corpus_stats(logical, config.targets()["targets"], seed=job.seed),
                "truth": {"source": key.source, "family": key.family, "script_type": key.script_type}})
    for tier in job.tiers:
        kn = knowledge_for(job.source, job.script_type, tier, job.seed, logogram_vocab=spec.logogram_vocab)
        rec["CD"][tier] = {"_families": sorted({r.family for r in kn.references})}
        for M in D_METHODS:
            m = M(restarts=em_restarts, iterations=em_iterations) if issubclass(M, KnightEM) else M()
            t = time.time()
            p = m.analyze(corpus, kn)
            s = score_sign_values(p.sign_values, key, logical)
            rec["CD"][tier][m.name] = {"family": p.family, "reference": p.extra.get("reference"),
                                       "family_correct": p.family == key.family, **s}
            bc = token_acc_before_cognate(p, kn, key, logical)
            if bc is not None:
                rec["CD"][tier][m.name]["token_acc_before_cognate"] = bc
            rec["timing"][f"{m.name}:{tier}"] = time.time() - t
    rec["timing"]["total"] = time.time() - t0
    return rec


# --------------------------------------------------------------------------- running

def profile(name: str = "sensitivity") -> dict:
    return config.experiment()["profiles"][name]


def build_sens_jobs(prof: dict) -> list[SensJob]:
    ip = prof["indus_point"]
    return [SensJob(l, st, seed, float(d), int(inv), ip["n_texts"], ip["mean_length"], tuple(prof["knowledge_tiers"]))
            for seed in prof["seeds"] for l in prof["languages"] for st in prof["script_types"]
            for d in prof["dup_grid"] for inv in prof["inventory_grid"]]


def records_path(name: str = "sensitivity") -> Path:
    return ensure(runs_dir() / "results" / name) / "records.jsonl"


def load_records(name: str = "sensitivity") -> list[dict]:
    p = records_path(name)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def _worker(args):
    job, path, er, ei = args
    try:
        rec = run_sens_job(job, er, ei)
    except Exception:  # noqa: BLE001 - recorded and reported, not hidden
        rec = {"job": asdict(job), "status": "error", "error": traceback.format_exc()}
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, default=float) + "\n")
    return rec["status"], rec.get("timing", {}).get("total") or rec.get("timing", {}).get("fit")


def run(name: str = "sensitivity", workers: int = 4, limit: int | None = None, log=print) -> None:
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from multiprocessing import get_context
    _single_thread_blas()
    prof = profile(name)
    os.environ["IBDB_SISTER_VERSION"] = prof.get("sister_version", "v1")   # inherited by spawned workers
    jobs = build_sens_jobs(prof)
    done = {json.dumps(r["job"], sort_keys=True) for r in load_records(name) if r.get("status") != "error"}
    todo = [j for j in jobs if j.key() not in done]
    if limit:
        todo = todo[:limit]
    log(f"[sensitivity] {len(jobs)} jobs, {len(todo)} to do, {workers} workers")
    path = records_path(name)
    t0 = time.time()
    with ProcessPoolExecutor(workers, mp_context=get_context("spawn")) as ex:
        futs = [ex.submit(_worker, (j, path, prof["em_restarts"], prof["em_iterations"])) for j in todo]
        for i, f in enumerate(as_completed(futs), 1):
            try:
                st, dt = f.result()
            except Exception as e:  # noqa: BLE001
                log(f"[sensitivity] worker failure: {e!r}")
                continue
            if i % 20 == 0 or st == "error":
                el = time.time() - t0
                log(f"[sensitivity] {i}/{len(todo)} {el:.0f}s eta {el / i * (len(todo) - i) / 3600:.2f}h last={st}")


# --------------------------------------------------------------------------- aggregation

MAX_LENGTH_SUBSTITUTIONS = 0.10   # share of texts whose length had to differ from the drawn length


def valid(rec: dict) -> bool:
    """In the map: inventory within tolerance AND at most 10% of texts given a substitute length
    (when a script has too few distinct texts of some length to reach a low duplicate rate)."""
    return (rec["status"] == "ok"
            and rec["gen"]["length_substitutions"] <= MAX_LENGTH_SUBSTITUTIONS * rec["job"]["n_texts"])


def _acc(d: dict, before_cognate: bool) -> float:
    """Task D token accuracy; with before_cognate, the score before the solver's cognate step
    (equal to token_acc when no cognate step ran)."""
    return d.get("token_acc_before_cognate", d["token_acc"]) if before_cognate else d["token_acc"]


def aggregate(name: str = "sensitivity", before_cognate: bool = False) -> dict[str, Any]:
    prof = profile(name)
    recs = load_records(name)
    for r in recs:   # a corpus counts only if both knobs were actually hit (see valid())
        if r["status"] == "ok" and not valid(r):
            r["status"] = "length_distorted"
    ok = [r for r in recs if r["status"] == "ok"]
    combos = sorted({(r["job"]["source"], r["job"]["script_type"]) for r in recs})
    cells = [(float(d), int(i)) for d in prof["dup_grid"] for i in prof["inventory_grid"]]
    reach = defaultdict(set)   # combo -> cells reached
    for r in ok:
        reach[(r["job"]["source"], r["job"]["script_type"])].add((r["job"]["dup"], r["job"]["inventory"]))
    balanced = sorted(c for c in combos if all(cell in reach[c] for cell in cells))
    # Plausible box (fixed in the profile before results): the cells bracketing the published duplicate rates
    # and sign-list sizes. Its own balanced panel keeps composition fixed without needing the grid edges.
    bx = prof["plausible_box"]
    box_cells = [(d, i) for d, i in cells if bx["dup"][0] <= d <= bx["dup"][1] and bx["inventory"][0] <= i <= bx["inventory"][1]]
    box_combos = sorted(c for c in combos if all(cell in reach[c] for cell in box_cells))
    methods = [M.name for M in D_METHODS]
    out: dict[str, Any] = {"profile": name, "dup_grid": prof["dup_grid"], "inventory_grid": prof["inventory_grid"],
                           "tiers": prof["knowledge_tiers"], "methods": methods,
                           "n_records": len(recs), "status_counts": dict(Counter(r["status"] for r in recs)),
                           "combos": [list(c) for c in combos], "balanced_combos": [list(c) for c in balanced],
                           "plausible_box": bx, "box_combos": [list(c) for c in box_combos],
                           "excluded": sorted({(r["job"]["source"], r["job"]["script_type"], r["job"]["dup"],
                                                 r["job"]["inventory"], r["status"]) for r in recs
                                                if r["status"] != "ok"}),
                           "panels": {}}
    for panel, keep, pcells in (("all", None, cells), ("balanced", set(balanced), cells),
                                ("box", set(box_combos), box_cells)):
        cells_out = []
        for d, inv in pcells:
            rs = [r for r in ok if r["job"]["dup"] == d and r["job"]["inventory"] == inv
                  and (keep is None or (r["job"]["source"], r["job"]["script_type"]) in keep)]
            cell: dict[str, Any] = {"dup": d, "inventory": inv, "n": len(rs)}
            if rs:
                cell["realized_dup"] = float(np.mean([r["stats"]["duplicate_text_fraction"] for r in rs]))
                cell["realized_inventory"] = float(np.mean([r["stats"]["sign_inventory"] for r in rs]))
                cell["mean_length"] = float(np.mean([r["stats"]["mean_length"] for r in rs]))
                cell["beginners80_signs"] = float(np.mean([r["stats"]["beginners80_signs"] for r in rs]))
                cell["top1_share"] = float(np.mean([r["stats"]["top1_share"] for r in rs]))
                cell["hapax_fraction"] = float(np.mean([r["stats"]["hapax_fraction"] for r in rs]))
                cell["by_script"] = {}
                for tier in prof["knowledge_tiers"]:
                    for m in methods:
                        x = np.array([_acc(r["CD"][tier][m], before_cognate) for r in rs])
                        cl = [r["job"]["source"] for r in rs]
                        lo, hi = cluster_bootstrap(x, cl)
                        cell[f"{tier}:{m}"] = {"mean": float(x.mean()), "ci_lo": lo, "ci_hi": hi,
                                               "share_ge_50": float(np.mean(x >= 0.5))}
                for st in sorted({r["job"]["script_type"] for r in rs}):
                    sub = [r for r in rs if r["job"]["script_type"] == st]
                    cell["by_script"][st] = {f"{t}:{m}": float(np.mean([_acc(r["CD"][t][m], before_cognate) for r in sub]))
                                             for t in prof["knowledge_tiers"] for m in methods} | {"n": len(sub)}
            cells_out.append(cell)
        out["panels"][panel] = cells_out
    out["box_spread"] = box_spread(ok, box_combos, box_cells, prof["knowledge_tiers"], methods, before_cognate)
    out["before_cognate"] = before_cognate
    out["timing_mean_s"] = float(np.mean([r["timing"]["total"] for r in ok])) if ok else None
    return out


def box_spread(ok: list[dict], combos, box_cells, tiers, methods, before_cognate: bool = False) -> dict[str, Any]:
    """Within one language x script combination, how far does accuracy move across the plausible box?
    Per combination: seed-averaged accuracy in each box cell, spread = max - min. Composition is fixed
    by construction (each spread compares a combination only with itself)."""
    out: dict[str, Any] = {}
    for t in tiers:
        for m in methods:
            rows = []
            for c in combos:
                per_cell = []
                for d, i in box_cells:
                    xs = [_acc(r["CD"][t][m], before_cognate) for r in ok if (r["job"]["source"], r["job"]["script_type"]) == c
                          and r["job"]["dup"] == d and r["job"]["inventory"] == i]
                    if xs:
                        per_cell.append((float(np.mean(xs)), d, i))
                if len(per_cell) == len(box_cells):
                    lo, hi = min(per_cell), max(per_cell)
                    rows.append({"source": c[0], "script_type": c[1], "min": lo[0], "min_cell": [lo[1], lo[2]],
                                 "max": hi[0], "max_cell": [hi[1], hi[2]], "spread": hi[0] - lo[0]})
            if not rows:
                continue
            sp = np.array([r["spread"] for r in rows])
            ci = cluster_bootstrap(sp, [r["source"] for r in rows])
            out[f"{t}:{m}"] = {"n_combos": len(rows), "median_spread": float(np.median(sp)),
                               "mean_spread": float(sp.mean()), "ci_lo": ci[0], "ci_hi": ci[1],
                               "share_spread_ge_10pts": float(np.mean(sp >= 0.10)), "rows": rows}
    return out


def write_aggregate(name: str = "sensitivity", out_dir: Path | None = None) -> Path:
    from .paths import project_root
    agg = aggregate(name)
    d = ensure(out_dir or project_root() / "reports" / "sensitivity")
    p = d / "aggregate.json"
    p.write_text(json.dumps(agg, indent=1, default=float))
    return p
