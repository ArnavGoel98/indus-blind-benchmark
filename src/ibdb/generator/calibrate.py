"""Calibrate generator knobs so a synthetic corpus matches the Indus targets.

Search: seeded random search over the knob box, then coordinate refinement. The objective is
the sum of squared normalized deviations over the regime's targets (0 when every target is
inside tolerance). One sanity term is added that is NOT a published target: the duplicate-text
share is kept at or below 0.40, so the calibrator cannot hit the frequency targets by copying
a handful of texts thousands of times. The report flags it as a design constraint.

Knobs are calibrated once per (source, script type, regime) with seed 0, then reused for other
seeds: "the same kind of script, a fresh random instance". The calibration report checks every
seed against the targets, not just seed 0.
"""

from __future__ import annotations

import json
from dataclasses import replace
from typing import Any

import numpy as np

from .. import config
from ..paths import ensure, runs_dir
from ..stats import check_targets, corpus_stats, ratio_from_token_texts
from .build import LANGUAGES, Knobs, make_corpus
from .script import ScriptSpec

DUP_CAP = 0.40


def knob_box(source: str, script_type: str) -> dict[str, tuple[float, float, str]]:
    box: dict[str, tuple[float, float, str]] = {
        "rho": (0.0, 0.15, "lin"),
        "allograph_rate": (0.0, 1.0, "lin"),
        "allograph_extra_mean": (1.0, 10.0, "lin"),
    }
    if source in LANGUAGES or source == "kamon":
        box.update({"alpha": (0.0, 2.0, "lin"), "beta": (0.0, 3.0, "lin"), "kappa": (0.0, 2.0, "lin"),
                    "gamma": (-2.0, 1.0, "lin")})
        if script_type == "logographic" or source == "kamon":
            box["vocab_cap"] = (60.0, 3000.0, "log")
    else:
        box["concentration"] = (0.5, 2.0, "lin")
    return box


def _decode(x: np.ndarray, box: dict) -> Knobs:
    kw: dict[str, Any] = {}
    for v, (name, (lo, hi, scale)) in zip(x, box.items()):
        if scale == "log":
            val = float(np.exp(np.log(lo) + v * (np.log(hi) - np.log(lo))))
        else:
            val = float(lo + v * (hi - lo))
        kw[name] = int(round(val)) if name == "vocab_cap" else val
    return Knobs(**kw)


def default_spec(script_type: str, gen_cfg: dict | None = None) -> ScriptSpec:
    g = gen_cfg or config.experiment()["generator"]
    det = g.get("determinatives", "auto")
    return ScriptSpec(script_type=script_type,
                      allograph_rate=g["allograph_rate"], homophony_rate=g["homophony_rate"],
                      polyvalence_rate=g["polyvalence_rate"],
                      determinatives=(script_type == "logosyllabic") if det == "auto" else bool(det),
                      word_divider=bool(g["word_divider"]), direction=g["direction"],
                      logogram_vocab=int(g["logogram_vocab"]))


def evaluate(source: str, spec: ScriptSpec, knobs: Knobs, specs: dict, n_texts: int, mean_len: float,
             median_len: float | None, seed: int) -> tuple[float, dict, dict]:
    corpus, _, info = make_corpus(source, spec, n_texts, mean_len, seed, knobs, median_length=median_len,
                                  adv_ratio_fn=ratio_from_token_texts)
    st = corpus_stats(corpus.logical(), config.targets()["targets"], seed=seed)
    chk = check_targets(st, specs)
    obj = sum(min(c["dev"], 20.0) ** 2 for c in chk.values() if not c["ok"])
    if st["duplicate_text_fraction"] > DUP_CAP:
        obj += ((st["duplicate_text_fraction"] - DUP_CAP) / 0.05) ** 2
    st.update({"truncated": info["truncated"], "concatenated": info["concatenated"]})
    return obj, st, chk


def calibrate(source: str, script_type: str, regime: str = "full", seed: int = 0, budget_random: int = 24,
              refine_rounds: int = 4, log=None, adv_target_ratio: float | None = None) -> dict[str, Any]:
    specs = config.regime_targets(regime)
    n_texts = int(specs["n_texts"]["value"])
    mean_len = float(specs["mean_length"]["value"])
    median_len = float(specs["median_length"]["value"])
    spec = default_spec(script_type)
    box = knob_box(source, script_type)
    rng = np.random.default_rng([seed, abs(hash_str(source + script_type + regime)) % (2**31)])
    best = (np.inf, None, None, None, None)

    def try_x(x):
        nonlocal best
        k = _decode(np.clip(x, 0, 1), box)
        if adv_target_ratio is not None:
            k.adv_target_ratio = adv_target_ratio
        obj, st, chk = evaluate(source, spec, k, specs, n_texts, mean_len, median_len, seed)
        if obj < best[0]:
            best = (obj, np.clip(x, 0, 1).copy(), k, st, chk)
        return obj

    # Start from a sensible centre, then random points.
    x0 = np.full(len(box), 0.5)
    names = list(box)
    if "rho" in names:
        x0[names.index("rho")] = 0.2
    try_x(x0)
    for _ in range(budget_random):
        if best[0] == 0:
            break
        try_x(rng.random(len(box)))
    step = 0.15
    for _ in range(refine_rounds):
        if best[0] == 0:
            break
        improved = False
        for i in range(len(box)):
            for d in (+step, -step):
                if best[0] == 0:
                    break
                x = best[1].copy()
                x[i] += d
                before = best[0]
                try_x(x)
                improved |= best[0] < before
        step = step if improved else step / 2
    obj, x, knobs, st, chk = best
    result = {"source": source, "script_type": script_type, "regime": regime, "seed": seed,
              "objective": obj, "all_pass": all(c["ok"] for c in chk.values()),
              "knobs": knobs.to_dict(), "spec": spec.to_dict(), "stats": st, "checks": chk}
    if log:
        n_ok = sum(c["ok"] for c in chk.values())
        log(f"[calibrate] {regime:11s} {source:13s} {script_type:12s} pass {n_ok}/{len(chk)} obj={obj:.2f}")
    return result


def hash_str(s: str) -> int:
    import zlib
    return zlib.crc32(s.encode())


def calibration_path(regime: str, source: str, script_type: str):
    return ensure(runs_dir() / "calibration" / regime) / f"{source}__{script_type}.json"


def save(result: dict) -> None:
    calibration_path(result["regime"], result["source"], result["script_type"]).write_text(
        json.dumps(result, indent=1, default=float))


def load_knobs(regime: str, source: str, script_type: str) -> tuple[Knobs, ScriptSpec]:
    d = json.loads(calibration_path(regime, source, script_type).read_text())
    return Knobs(**d["knobs"]), ScriptSpec(**d["spec"])


def with_overrides(spec: ScriptSpec, **kw) -> ScriptSpec:
    return replace(spec, **kw)


def _job(args):
    source, script_type, regime, adv = args
    res = calibrate(source, script_type, regime, adv_target_ratio=adv)
    save(res)
    return f"{regime:11s} {source:13s} {script_type:12s} pass {sum(c['ok'] for c in res['checks'].values())}/{len(res['checks'])}"


def language_entropy_ratio(regime: str, languages, script_types) -> float:
    """Median H(X2|X1)/H(X1) of the calibrated linguistic corpora (seed 0); target for the
    adversarial control so it imitates language on exactly the statistic Rao (2009) used."""
    from ..stats import conditional_entropy
    ratios = []
    for src in languages:
        for st in script_types:
            k, sp = load_knobs(regime, src, st)
            sp_n = config.regime_targets(regime)
            c, _, _ = make_corpus(src, sp, int(sp_n["n_texts"]["value"]), float(sp_n["mean_length"]["value"]), 0, k,
                                  median_length=float(sp_n["median_length"]["value"]))
            h1, h2 = conditional_entropy(c.logical(), 100)
            ratios.append(h2 / h1)
    return float(np.median(ratios))


def _run_pool(jobs, workers, log):
    from concurrent.futures import ProcessPoolExecutor, as_completed
    from multiprocessing import get_context
    todo = [j for j in jobs if not calibration_path(j[2], j[0], j[1]).exists()]
    for attempt in range(3):  # retry jobs lost to a dead worker
        if not todo:
            return
        try:
            with ProcessPoolExecutor(workers, mp_context=get_context("spawn")) as ex:
                futs = {ex.submit(_job, j): j for j in todo}
                for f in as_completed(futs):
                    try:
                        log("[calibrate] " + f.result())
                    except Exception as e:  # noqa: BLE001
                        log(f"[calibrate] FAILED {futs[f]}: {e!r}")
        except Exception as e:  # noqa: BLE001 - BrokenProcessPool: retry the remainder
            log(f"[calibrate] pool error: {e!r}")
        todo = [j for j in todo if not calibration_path(j[2], j[0], j[1]).exists()]
    if todo:
        raise RuntimeError(f"calibration failed for {todo}")


def calibrate_all(languages, script_types, controls, regimes, workers: int = 4, log=print) -> None:
    """Resumable: configurations with a saved result are skipped."""
    for regime in regimes:
        _run_pool([(s, st, regime, None) for s in languages for st in script_types], workers, log)
        adv = language_entropy_ratio(regime, languages, script_types)
        log(f"[calibrate] {regime}: adversarial control target entropy ratio = {adv:.3f}")
        _run_pool([(c, "emblem", regime, adv) for c in controls], workers, log)
