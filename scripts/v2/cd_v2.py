"""v2 Tasks C and D: bracket lower bound `harsh` (entry 4) and real relatives (entry 5).

Corpora: the v1 Indus-point corpora with the sister-v2 content split, i.e. those of profiles
`sister_v2_main` (sampler A, generator v1) and `sister_v2_gen2` (sampler B, generator v2): 2,906 texts,
mean length 4.6, seeds 0-2, four script types, regenerated here from the same seeds.

Tiers per hidden language (entries 4 and 5):
- related_harsh / candidates_harsh: sister-v4 with the `harsh` settings (reports/v2/sister/harsh.json),
  alone or with every other v1 language (v1 references, content split);
- related_real:<relative> / candidates_real:<relative>: Latin-Italian, Tamil-Malayalam, Tamil-Kannada
  (Finnish-Estonian when its gold table exists), normalised spelling.
The upper bound (v1 sister) is read from the existing sister_v2_main / sister_v2_gen2 records; it is
not rerun (frozen-v1 methods, same corpora).

Methods (entry 1): revised EM (primary), original EM, frequency-rank baseline; unchanged.
Scoring (entry 2): `relative_cd.score`, strict primary, lenient secondary, before the cognate step;
Task C: family of the chosen reference; the chosen reference is recorded for every method.

A final run refuses to start unless every file outside src/ibdb/data is identical to the `frozen-v2`
tag (working tree included), so data (the Estonian gold table) may be added after the tag; code may not.

Usage:
  python scripts/v2/cd_v2.py --dev OUTDIR      # pipeline check: seed 90, sampler A, 1 EM restart (not a result)
  python scripts/v2/cd_v2.py                   # final run -> runs/results/v2_cd/records.jsonl
  python scripts/v2/cd_v2.py --relative estonian   # add one real relative later -> records_estonian.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

os.environ["IBDB_SISTER_VERSION"] = "v2"      # content split, as the v1 paper's sister runs

from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import LANGUAGES, make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.knowledge import build_reference  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import FrequencyRankBaseline, KnightEM, KnightEMOriginal  # noqa: E402
from ibdb.paths import ensure, reports_dir, runs_dir  # noqa: E402

D_METHODS = [KnightEM, KnightEMOriginal, FrequencyRankBaseline]
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
REAL = {"latin": ["italian"], "tamil": ["malayalam", "kannada"],
        "finnish": ["estonian"] if RC.has_gold("estonian") else []}
SAMPLERS = {"A": "v1", "B": "v2"}
N_TEXTS, MEAN_LEN = 2906, 4.6
HARSH = json.loads((reports_dir() / "v2" / "sister" / "harsh.json").read_text())["chosen"]


def relatives_for(lang: str, seed: int, only: str | None = None) -> dict[str, RC.Relative]:
    if only:
        return {f"real:{only}": RC.real_relative(lang, only)}
    out = {"harsh": RC.harsh_relative(lang, seed, HARSH[lang]["knobs"])}
    for r in REAL.get(lang, []):
        out[f"real:{r}"] = RC.real_relative(lang, r)
    return out


def check_frozen() -> None:
    """Refuse unless all code (everything outside src/ibdb/data) matches the frozen-v2 tag."""
    ok = subprocess.run(["git", "rev-parse", "-q", "--verify", "refs/tags/frozen-v2"], capture_output=True).returncode == 0
    same = ok and subprocess.run(["git", "diff", "--quiet", "frozen-v2", "--", ".", ":(exclude)src/ibdb/data",
                                  ":(exclude)reports", ":(exclude)docs"]).returncode == 0
    if not same:
        raise SystemExit("final run refused: code differs from the frozen-v2 tag (or the tag is missing)")


def run_corpus(args) -> dict:
    lang, st, seed, sampler, restarts, iterations, only = args
    t0 = time.time()
    gv = SAMPLERS[sampler]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, info = make_corpus(lang, spec, N_TEXTS, MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    others = [build_reference(o, st, False, seed, spec.logogram_vocab) for o in LANGUAGES if o != lang]
    rec = {"lang": lang, "script_type": st, "seed": seed, "sampler": sampler, "family": key.family,
           "n_tokens": corpus.n_tokens, "tiers": {}}
    for rname, rel in relatives_for(lang, seed, only).items():
        ref = RC.reference(rel, st, lang, spec.logogram_vocab)
        gold = RC.Gold(rel, lang, st, logos)
        for tier, refs in ((f"related_{rname}", [ref]), (f"candidates_{rname}", [ref] + others)):
            kn = Knowledge(tier.split("_")[0], st, refs)
            out = {}
            for M in D_METHODS:
                m = M(restarts=restarts, iterations=iterations) if issubclass(M, KnightEM) else M()
                p = m.analyze(corpus, kn)
                out[m.name] = {"reference": p.extra.get("reference"), "family": p.family,
                               "family_correct": p.family == key.family, **RC.score(p.sign_values, key, logical, gold)}
            rec["tiers"][tier] = out
    rec["seconds"] = time.time() - t0
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", metavar="OUTDIR", help="pipeline check only: seed 90, sampler A, 1 restart")
    ap.add_argument("--relative", help="run only this real relative's tiers (added after the main run)")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.dev:
        jobs = [(lang, st, 90, "A", 1, 60, None) for lang in LANGUAGES for st in SCRIPTS]
        path = Path(a.dev) / "records_dev.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        check_frozen()
        langs = [lg for lg, rs in REAL.items() if a.relative in rs] if a.relative else LANGUAGES
        if a.relative and not langs:
            raise SystemExit(f"no gold table for {a.relative} yet")
        jobs = [(lang, st, s, smp, 3, 60, a.relative) for smp in SAMPLERS for s in (0, 1, 2) for lang in langs for st in SCRIPTS]
        name = f"records_{a.relative}.jsonl" if a.relative else "records.jsonl"
        path = ensure(runs_dir() / "results" / "v2_cd") / name
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j[:4] not in done]
    print(f"[v2_cd] {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(run_corpus, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r = f.result()
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[v2_cd] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}", flush=True)


if __name__ == "__main__":
    main()
