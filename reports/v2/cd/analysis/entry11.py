"""Pre-registration entry 11, C: confirmation rerun of the syllable-cutter fix on development seeds.

Finnish (Estonian) and Old Tamil (Malayalam, Kannada), syllabic and logo-syllabic, seeds 0-2, samplers A
and B: 24 corpora. For each corpus and real relative: `related_real` and `candidates_real` tiers (the
entry-6 methods and budget), scored with the entry-10 scorer, and the raw and reachable ceilings (the
reachable one also for the reference as the frozen-v2 cutter cut it). Predictions are stored. C1, C2
and C3 are not rerun (entry 11).

Refuses to run unless every code file outside the data, tests, reports/ and docs/ equals `frozen-v2`,
except the entry-10 harness files (which include src/ibdb/relative_cd.py), and they are committed.
Usage (repository root): python reports/v2/cd/analysis/entry11.py [--workers 4]
Writes runs/results/v2_e11/records.jsonl and predictions.jsonl (resumable).
"""
import argparse
import dataclasses
import json
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import)
import entry10  # noqa: E402
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import LANGUAGES, make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.knowledge import build_reference  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import KnightEM  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

REAL = {"finnish": ["estonian"], "tamil": ["malayalam", "kannada"]}
SCRIPTS = ["syllabic", "logosyllabic"]
CAP = KnightEM().max_units


def job(args) -> tuple[dict, dict]:
    lang, st, seed, sampler = args
    t0 = time.time()
    gv = cd_v2.SAMPLERS[sampler]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    others = [build_reference(o, st, False, seed, spec.logogram_vocab) for o in LANGUAGES if o != lang]
    rec = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler, "family": key.family,
           "n_tokens": corpus.n_tokens, "tiers": {}, "ceiling": {}}
    preds = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler, "tiers": {}}
    for r in REAL[lang]:
        rel = RC.real_relative(lang, r)
        gold = RC.Gold(rel, lang, st, logos)
        ref = RC.reference(rel, st, lang, spec.logogram_vocab)
        ref_old = RC.reference(dataclasses.replace(rel, vowels=frozenset()), st, lang, spec.logogram_vocab)
        rec["ceiling"][f"real:{r}"] = {"raw": RC.score({}, key, logical, gold)["recoverable"],
                                       "reachable": RC.reachable(ref, key, gold, CAP),
                                       "reachable_old_cut": RC.reachable(ref_old, key, gold, CAP)}
        for tier, rl in ((f"related_real:{r}", [ref]), (f"candidates_real:{r}", [ref] + others)):
            kn = Knowledge(tier.split("_")[0], st, rl)
            rec["tiers"][tier], preds["tiers"][tier] = {}, {}
            for M in cd_v2.D_METHODS:
                m = M(restarts=3, iterations=60) if issubclass(M, KnightEM) else M()
                p = m.analyze(corpus, kn)
                rec["tiers"][tier][m.name] = {"reference": p.extra.get("reference"), "family": p.family,
                                              "family_correct": p.family == key.family,
                                              **RC.score(p.sign_values, key, logical, gold)}
                preds["tiers"][tier][m.name] = {str(k): v for k, v in (p.sign_values or {}).items()}
    rec["seconds"] = time.time() - t0
    return rec, preds


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    head = entry10.check_guard()
    jobs = [(lang, st, s, smp) for lang in REAL for smp in cd_v2.SAMPLERS for s in (0, 1, 2) for st in SCRIPTS]
    out = ensure(runs_dir() / "results" / "v2_e11")
    path, ppath = out / "records.jsonl", out / "predictions.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j not in done]
    print(f"[entry11] HEAD {head}; {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(job, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r, pr = f.result()
                r["commit"] = head
                with open(ppath, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(pr, ensure_ascii=False) + "\n")
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[entry11] {i}/{len(todo)} {time.time() - t0:.0f}s {j}{' ERROR' if 'error' in r else ''}", flush=True)


if __name__ == "__main__":
    main()
