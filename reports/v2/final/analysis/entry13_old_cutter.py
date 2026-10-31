"""Pre-registration entry 13 (POST HOC): the frozen-v2 (old) syllable cutter on the final-run corpora.

Six cells (Estonian, Malayalam, Kannada; syllabic and logo-syllabic), seeds 6-11, samplers A and B: 24
corpora. Revised EM (3 restarts, 60 iterations), `related_real` only, with each relative built with
`vowels=frozenset()` (the cutter entry 11 replaced); entry-10 scorer. Unrelated-reference scores come from
the final-run records. Writes runs/results/v2_e13/records.jsonl, then reports/v2/final/entry13.{md,json}.
Usage (repository root): python reports/v2/final/analysis/entry13_old_cutter.py [--workers 4] [--report-only]
"""
import argparse
import dataclasses
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
import cd_v2  # noqa: E402  (IBDB_SISTER_VERSION=v2)
from ibdb import relative_cd as RC  # noqa: E402
from ibdb.generator.build import make_corpus  # noqa: E402
from ibdb.generator.calibrate import load_knobs  # noqa: E402
from ibdb.methods.base import Knowledge  # noqa: E402
from ibdb.methods.decipher import KnightEM  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

EM = "knight2006_em"
REAL = {"finnish": ["estonian"], "tamil": ["malayalam", "kannada"]}
UNREL = {"finnish": ["latin", "tamil"], "tamil": ["latin", "finnish"]}
SCRIPTS = ["syllabic", "logosyllabic"]
SEEDS = range(6, 12)
OUT = ROOT / "reports" / "v2" / "final"


def job(a):
    lang, st, seed, smp = a
    gv = cd_v2.SAMPLERS[smp]
    knobs, spec = load_knobs("full", lang, st, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st == "logosyllabic" else set()
    rec = {"lang": lang, "script_type": st, "seed": seed, "sampler": smp, "n_tokens": corpus.n_tokens, "old": {}}
    for r in REAL[lang]:
        rel = dataclasses.replace(RC.real_relative(lang, r), vowels=frozenset())
        ref = RC.reference(rel, st, lang, spec.logogram_vocab)
        p = KnightEM(restarts=3, iterations=60).analyze(corpus, Knowledge("related", st, [ref]))
        rec["old"][r] = RC.score(p.sign_values, key, logical, RC.Gold(rel, lang, st, logos))
    return rec


def report() -> None:
    K = lambda r: (r["lang"], r["script_type"], r["seed"], r["sampler"])  # noqa: E731
    old = {K(r): r for r in map(json.loads, (runs_dir() / "results" / "v2_e13" / "records.jsonl").read_text().splitlines())}
    fin = {K(r): r for r in map(json.loads, (runs_dir() / "results" / "v2_final" / "records.jsonl").read_text().splitlines())
           if "error" not in r}
    final = json.loads((OUT / "results.json").read_text())
    res = {}
    for lang, rels in REAL.items():
        for rel in rels:
            for st in SCRIPTS:
                ks = sorted(k for k in old if k[0] == lang and k[1] == st)
                assert len(ks) == 12 and all(old[k]["n_tokens"] == fin[k]["n_tokens"] for k in ks)
                o = [100 * old[k]["old"][rel]["strict"] for k in ks]
                n = [100 * fin[k]["tiers"][f"related_real:{rel}"][EM]["strict"] for k in ks]
                un = {u: [100 * fin[k]["unrelated"][u][EM][f"real:{rel}"]["strict"] for k in ks] for u in UNREL[lang]}
                best = max(un, key=lambda u: np.mean(un[u]))
                c = {"old": float(np.mean(o)), "new": float(np.mean(n)), "best_unrel": best, "unrel": float(np.mean(un[best])),
                     "added_old": float(np.mean(o) - np.mean(un[best])), "wins_old": int(sum(a > b for a, b in zip(o, un[best]))),
                     "added_new": float(np.mean(n) - np.mean(un[best])), "wins_new": int(sum(a > b for a, b in zip(n, un[best])))}
                c["helps_old"] = c["added_old"] >= 5 and c["wins_old"] >= 9
                c["helps_new"] = c["added_new"] >= 5 and c["wins_new"] >= 9
                res[f"{rel}|{st}"] = c
    italian = sum(final["cells"][f"italian|{st}"]["helps"] for st in SCRIPTS)
    h3_old = italian + sum(c["helps_old"] for c in res.values())
    est = [res[f"estonian|{st}"]["helps_old"] for st in SCRIPTS]
    verdict = ("attributed to the cutter fix" if not any(est) else "attributed to the new seeds, not the fix" if all(est)
               else "mixed")
    f = lambda v: f"{v:.1f}"  # noqa: E731
    L = ["# Entry 13 (POST HOC): the old syllable cutter on the final-run corpora", "",
         "**Post hoc, declared after the final-run results were read (entry 13).** It changes no entry-12 reading: H3 stays "
         "*not met*. Revised EM, strict, `related_real`, seeds 6-11, samplers A and B (12 corpora per cell). *Old* = each "
         "relative cut with the hidden language's vowels only (the frozen-v2 cutter); *new* = the final run (entry-11 cutter). "
         "The unrelated reference and its scores are those of the final run.", "",
         "| Relative | Script | Old cutter | New cutter (final) | Better unrelated ref. | Old: added; wins | Old: helps? | "
         "New: added; wins | New: helps? |", "|---|---|---|---|---|---|---|---|---|"]
    for k, c in res.items():
        rel, st = k.split("|")
        lab = rel.capitalize() + (" (weak gold)" if rel == "estonian" else "")
        L.append(f"| {lab} | {st} | {f(c['old'])} | {f(c['new'])} | {c['best_unrel'].capitalize()}, {f(c['unrel'])} | "
                 f"{c['added_old']:+.1f}; {c['wins_old']} of 12 | {'yes' if c['helps_old'] else 'no'} | "
                 f"{c['added_new']:+.1f}; {c['wins_new']} of 12 | {'yes' if c['helps_new'] else 'no'} |")
    L += ["", f"**H3 count with the old cutter:** {h3_old} of 8 cells (final run, new cutter: "
          f"{italian + sum(c['helps_new'] for c in res.values())} of 8). Italian cells are unchanged by the cutter.", "",
          f"**Reading fixed in entry 13:** the Estonian change is **{verdict}** (Estonian syllabic with the old cutter: "
          f"{'helps' if est[0] else 'does not help'}; logo-syllabic: {'helps' if est[1] else 'does not help'})."]
    (OUT / "entry13.md").write_text("\n".join(L) + "\n")
    (OUT / "entry13.json").write_text(json.dumps({"cells": res, "h3_old": h3_old, "verdict": verdict}, indent=1))
    print("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    if not a.report_only:
        jobs = [(lang, st, s, smp) for lang in REAL for st in SCRIPTS for s in SEEDS for smp in cd_v2.SAMPLERS]
        path = ensure(runs_dir() / "results" / "v2_e13") / "records.jsonl"
        done = {tuple(json.loads(x)[k] for k in ("lang", "script_type", "seed", "sampler"))
                for x in (path.read_text().splitlines() if path.exists() else [])}
        with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
            futs = {ex.submit(job, j): j for j in jobs if j not in done}
            for i, fu in enumerate(as_completed(futs), 1):
                with open(path, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(fu.result()) + "\n")
                print(f"[entry13] {i}/{len(futs)} {futs[fu]}", flush=True)
    report()


if __name__ == "__main__":
    main()
