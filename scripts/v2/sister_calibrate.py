"""v2 rank 6: calibrate sister-v4 on development seeds 90-91 only (plan: docs/v2_sister_plan.md).

Stage 1 (grid): every knob setting x language x seed {90, 91}, yardsticks with 5 draws.
Stage 2 (select): per language and setting (close, distant), the pre-declared selection rule.
Stage 3 (confirm): chosen settings re-measured with 20 draws on seeds 90-91, then on held-out seeds
0-2 without change; a v1-like sister (shift + 20% lexical, no mergers) measured with the same code.
No Task C or D score is computed here.

Usage: WORKERS=4 python scripts/v2/sister_calibrate.py [grid|select|confirm|all]
Writes runs/results/v2_sister_grid/records.jsonl and reports/v2/sister/{anchor.json,calibration.json,yardsticks.md}.
"""
from __future__ import annotations

import itertools
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context

import numpy as np

LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
DEV, HELD = [90, 91], [0, 1, 2]
GRID = {"n_cond": [0, 2, 4, 6, 9, 12], "affix_share": [0, 0.25, 0.5, 0.75, 1.0],
        "lexical": [0.1, 0.2, 0.35, 0.5], "word_order": [0, 0.5, 1.0], "final_vowel_loss": [0, 0.3, 0.6]}
VERBATIM_MAX = 0.02


def paths():
    from ibdb.paths import ensure, reports_dir, runs_dir
    return ensure(runs_dir() / "results" / "v2_sister_grid") / "records.jsonl", ensure(reports_dir() / "v2" / "sister")


def anchor() -> dict:
    """Ugaritic-Hebrew yardsticks from the shared module (computed once, cached)."""
    _, out = paths()
    f = out / "anchor.json"
    if not f.exists():
        from ibdb import yardsticks as Y
        from ibdb.data import ugaritic as U
        y = Y.ugaritic_hebrew(U.hebrew_texts(), U.hebrew_words(), U.hebrew_texts(U.POETIC_BOOKS))
        f.write_text(json.dumps(y, ensure_ascii=False, indent=1))
    return json.loads(f.read_text())


def targets(a: dict) -> dict:
    return {"close": {"jsd_above_floor": (a["jsd_above_floor"], 0.04), "cognate_types_cc": (a["cognate_types_cc"], 0.10),
                      "word_pairs_types_cc": (a["word_pairs_types_cc"], 0.10)},
            "distant": {"jsd_above_floor": (2 * a["jsd_above_floor"], 0.06), "cognate_types_cc": (a["cognate_types_cc"] / 2, 0.10),
                        "word_pairs_types_cc": (a["word_pairs_types_cc"] / 2, 0.10)}}


_H: dict = {}


def measure(lang: str, seed: int, knobs: dict, draws: int, merger_share=None) -> dict:
    for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
        os.environ.setdefault(v, "1")
    from ibdb import sister_v4 as S
    from ibdb import yardsticks as Y
    if lang not in _H:
        _H[lang] = S.hidden_half(lang)[0]
    kw = {} if merger_share is None else {"merger_share": merger_share}
    s = S.build(lang, seed, S.Knobs(**knobs), **kw)
    y = Y.sister_yardsticks(_H[lang], s.clauses, s.regular, anchor(), n_draws=draws, seed=seed)
    return {"lang": lang, "seed": seed, "knobs": knobs, "draws": draws, "n_mergers": len(s.mergers), **y}


def grid() -> None:
    path, _ = paths()
    anchor()
    done = set()
    if path.exists():
        done = {(r["lang"], r["seed"], json.dumps(r["knobs"], sort_keys=True)) for r in map(json.loads, path.read_text().splitlines())}
    keys = list(GRID)
    jobs = [(l, s, dict(zip(keys, v))) for l in LANGS for s in DEV for v in itertools.product(*GRID.values())]
    jobs = [j for j in jobs if (j[0], j[1], json.dumps(j[2], sort_keys=True)) not in done]
    print(f"[grid] {len(jobs)} to do", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(int(os.environ.get("WORKERS", "4")), mp_context=get_context("fork")) as ex:
        futs = [ex.submit(measure, l, s, k, 5) for l, s, k in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            with open(path, "a") as fh:
                fh.write(json.dumps(f.result(), default=float) + "\n")
            if i % 500 == 0:
                el = time.time() - t0
                print(f"[grid] {i}/{len(jobs)} eta {el / i * (len(jobs) - i) / 60:.0f} min", flush=True)


def select() -> dict:
    path, out = paths()
    T = targets(anchor())
    rows = [json.loads(l) for l in path.read_text().splitlines()]
    by: dict = {}
    for r in rows:
        by.setdefault((r["lang"], json.dumps(r["knobs"], sort_keys=True)), []).append(r)
    order = lambda k: tuple(json.loads(k)[n] for n in GRID)  # noqa: E731  (ties: smaller knobs first)
    chosen: dict = {}
    for setting, tg in T.items():
        chosen[setting] = {}
        for lang in LANGS:
            best = None
            for (l, k), rs in sorted(by.items(), key=lambda kv: order(kv[0][1])):
                if l != lang or len(rs) < len(DEV):
                    continue
                m = {y: float(np.mean([r[y] for r in rs])) for y in tg}
                if float(np.mean([r["verbatim_6plus"] for r in rs])) > VERBATIM_MAX:
                    continue
                loss = sum(((m[y] - t) / hw) ** 2 for y, (t, hw) in tg.items())
                if best is None or loss < best[0] - 1e-12:
                    inside = all(abs(m[y] - t) <= hw for y, (t, hw) in tg.items())
                    best = (loss, json.loads(k), m, inside)
            chosen[setting][lang] = {"knobs": best[1], "loss": best[0], "dev_grid_means": best[2], "matched": best[3]} \
                if best else {"knobs": None, "matched": False, "note": "no grid point with verbatim <= 2%"}
    (out / "calibration.json").write_text(json.dumps({"targets": T, "chosen": chosen}, indent=1))
    return chosen


def confirm() -> None:
    _, out = paths()
    cal = json.loads((out / "calibration.json").read_text())
    res: dict = {"close": {}, "distant": {}, "v1_like": {}}
    v1 = {"n_cond": 0, "affix_share": 0.0, "lexical": 0.2, "word_order": 0.0, "final_vowel_loss": 0.0}
    for lang in LANGS:
        for setting in ("close", "distant"):
            k = cal["chosen"][setting][lang]["knobs"]
            if k is None:
                continue
            res[setting][lang] = {"dev": [measure(lang, s, k, 20) for s in DEV], "held": [measure(lang, s, k, 20) for s in HELD]}
        res["v1_like"][lang] = {"held": [measure(lang, s, v1, 20, merger_share=0.0) for s in HELD]}
        print(f"[confirm] {lang}", flush=True)
    cal["confirm"] = res
    (out / "calibration.json").write_text(json.dumps(cal, indent=1, default=float))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("grid", "all"):
        grid()
    if step in ("select", "all"):
        print(json.dumps(select(), indent=1))
    if step in ("confirm", "all"):
        confirm()
