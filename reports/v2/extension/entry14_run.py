"""Pre-registration entry 14: a prospective test of the H3 explanation on fresh seeds 12-17.

Declared before any seed 12-17 corpus was generated (docs/v2_preregistration.md, entry 14). Code is
`frozen-v2.1`, unchanged: this driver only chooses seeds and cells and calls the frozen functions the final
run (`scripts/v2/final_v2.py`) calls, with the same settings.

Corpora: Old Tamil and Finnish; syllabic and logo-syllabic; seeds 12-17; samplers A and B (48 corpora).
Per corpus and real relative (Malayalam, Kannada for Old Tamil; Estonian for Finnish), entry-11 cutter:
- `related_real:<relative>`: revised EM, 3 restarts, 60 iterations; entry-10 scorer (strict primary);
- raw and reachable ceilings (entry 11), the C2 floor (entry 8);
- C1: revised EM with each unrelated reference (Old Tamil: Latin, Finnish; Finnish: Latin, Old Tamil), scored
  against each real relative's gold.
No synthetic tiers, no `candidates_*` tiers, no v1 sister, no C3/C4.

Usage (repository root):
  python reports/v2/extension/entry14_run.py --dev OUTDIR    # pipeline check: seed 90, sampler A, 1 restart (not a result)
  python reports/v2/extension/entry14_run.py [--workers 4]   # the run -> runs/results/v2_e14/records.jsonl, then the report
  python reports/v2/extension/entry14_run.py --report-only
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts" / "v2"))
import final_v2  # noqa: E402  (imports cd_v2, which sets IBDB_SISTER_VERSION=v2, and the entry-8 controls)
from final_v2 import RC, Knowledge, KnightEM, build_reference, cd_v2, controls, load_knobs, make_corpus  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

EM = "knight2006_em"
REAL = {"tamil": ["malayalam", "kannada"], "finnish": ["estonian"]}
UNREL = final_v2.UNREL
SCRIPTS = ["syllabic", "logosyllabic"]
SEEDS = (12, 13, 14, 15, 16, 17)
HELPED = [("malayalam", "syllabic"), ("estonian", "syllabic"), ("estonian", "logosyllabic")]   # X1
KANNADA = [("kannada", "syllabic"), ("kannada", "logosyllabic")]                                # X2
OUT = Path(__file__).resolve().parent


def job(a) -> dict:
    lang, st_, seed, smp, restarts = a
    t0 = time.time()
    gv = cd_v2.SAMPLERS[smp]
    knobs, spec = load_knobs("full", lang, st_, gv)
    corpus, key, _ = make_corpus(lang, spec, cd_v2.N_TEXTS, cd_v2.MEAN_LEN, seed, knobs, generator_version=gv)
    logical = [t.tolist() for t in corpus.logical()]
    logos = RC.hidden_logograms(lang, spec.logogram_vocab) if st_ == "logosyllabic" else set()
    rec = {"lang": lang, "script_type": st_, "seed": seed, "sampler": smp, "family": key.family,
           "n_tokens": corpus.n_tokens, "related": {}, "ceiling": {}, "floor": {}, "unrelated": {}}
    golds = {}
    for r in REAL[lang]:
        rel = RC.real_relative(lang, r)
        ref = RC.reference(rel, st_, lang, spec.logogram_vocab)
        gold = golds[r] = RC.Gold(rel, lang, st_, logos)
        rec["ceiling"][r] = {"raw": RC.score({}, key, logical, gold)["recoverable"],
                             "reachable": RC.reachable(ref, key, gold, final_v2.CAP)}
        p = KnightEM(restarts=restarts, iterations=60).analyze(corpus, Knowledge("related", st_, [ref]))
        rec["related"][r] = RC.score(p.sign_values, key, logical, gold)
        rec["floor"][r] = controls.floor(key, logical, gold)
    for u in UNREL[lang]:
        kn = Knowledge("related", st_, [build_reference(u, st_, False, seed, spec.logogram_vocab)])
        p = KnightEM(restarts=restarts, iterations=60).analyze(corpus, kn)
        rec["unrelated"][u] = {r: RC.score(p.sign_values, key, logical, g) for r, g in golds.items()}
    rec["seconds"] = time.time() - t0
    return rec


def run(jobs: list, path: Path, head: str, workers: int) -> None:
    done = set()
    if path.exists():
        done = {tuple(r[k] for k in ("lang", "script_type", "seed", "sampler"))
                for r in map(json.loads, path.read_text().splitlines()) if "error" not in r}
    todo = [j for j in jobs if j[:4] not in done]
    print(f"[entry14] HEAD {head}; {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(job, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r = f.result()
                r["commit"] = head
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float) + "\n")
            print(f"[entry14] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}", flush=True)


def cells(recs: list[dict]) -> dict:
    out = {}
    for lang, rels in REAL.items():
        for rel in rels:
            for s in SCRIPTS:
                rs = sorted((r for r in recs if r["lang"] == lang and r["script_type"] == s), key=lambda r: (r["seed"], r["sampler"]))
                assert len(rs) == 12, (lang, s, len(rs))
                real = [100 * r["related"][rel]["strict"] for r in rs]
                un = {u: [100 * r["unrelated"][u][rel]["strict"] for r in rs] for u in UNREL[lang]}
                best = max(un, key=lambda u: st.fmean(un[u]))
                c = {"real": st.fmean(real), "best_unrel": best, "unrel": st.fmean(un[best]),
                     "added": st.fmean(real) - st.fmean(un[best]), "wins": sum(x > y for x, y in zip(real, un[best])),
                     "floor": st.fmean(100 * r["floor"][rel] for r in rs),
                     "reachable": st.fmean(100 * r["ceiling"][rel]["reachable"] for r in rs)}
                c["helps"] = c["added"] >= 5 and c["wins"] >= 9
                out[f"{rel}|{s}"] = c
    return out


def report(path: Path) -> None:
    recs = [json.loads(x) for x in path.read_text().splitlines()]
    errors = [(r["lang"], r["script_type"], r["seed"], r["sampler"]) for r in recs if "error" in r]
    recs = [r for r in recs if "error" not in r]
    c = cells(recs)
    x1 = sum(c[f"{r}|{s}"]["helps"] for r, s in HELPED)
    x2 = not any(c[f"{r}|{s}"]["helps"] for r, s in KANNADA)
    x3 = all(v["real"] < 15 for v in c.values())
    R = {"X1": (x1 >= 2, f"{x1} of 3 helped cells help again"),
         "X2": (x2, "; ".join(f"Kannada {s}: {c['kannada|' + s]['added']:+.1f}, {c['kannada|' + s]['wins']} of 12" for s in SCRIPTS)),
         "X3": (x3, f"highest {max(v['real'] for v in c.values()):.1f}")}
    yn = lambda b: "met" if b else "**not met**"  # noqa: E731
    L = ["# Entry 14: prospective test of the H3 explanation (seeds 12-17)", "",
         "Pre-registered (docs/v2_preregistration.md, entry 14). Code `frozen-v2.1`; Old Tamil from the 2026-11-17 Project "
         "Madurai text (pinned in `reports/v2/repro/v1_sources_manifest.json`). Revised EM, strict, `related_real`, 12 corpora "
         "per cell. Helps = at least +5 points over the better unrelated reference and ahead in at least 9 of 12 paired corpora.",
         "", "## Failures first", "", f"- Run errors: {len(errors)}{' ' + str(errors) if errors else ''}.",
         f"- Readings not met: {', '.join(k for k, v in R.items() if not v[0]) or 'none'}.", "",
         "## Readings", "", "| Reading | Result |", "|---|---|"]
    L += [f"| {k} | {yn(v[0])}: {v[1]} |" for k, v in R.items()]
    L += ["", "## Cells", "", "| Relative | Script | Real relative | Better unrelated ref. | Added; wins | Helps? | Floor | "
          "Reachable ceiling |", "|---|---|---|---|---|---|---|---|"]
    for k, v in c.items():
        rel, s = k.split("|")
        lab = rel.capitalize() + (" (weak gold)" if rel == "estonian" else "")
        L.append(f"| {lab} | {s} | {v['real']:.1f} | {v['best_unrel'].capitalize()}, {v['unrel']:.1f} | {v['added']:+.1f}; "
                 f"{v['wins']} of 12 | {'yes' if v['helps'] else 'no'} | {v['floor']:.1f} | {v['reachable']:.1f} |")
    (OUT / "entry14.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT / "entry14.json").write_text(json.dumps({"errors": errors, "readings": R, "cells": c}, indent=1), encoding="utf-8")
    print("\n".join(L))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", metavar="OUTDIR", help="pipeline check only: seed 90, sampler A, 1 restart")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()
    if a.dev:
        out = Path(a.dev)
        out.mkdir(parents=True, exist_ok=True)
        run([(lang, s, 90, "A", 1) for lang in REAL for s in SCRIPTS], out / "records.jsonl", "dev", a.workers)
        return
    path = ensure(runs_dir() / "results" / "v2_e14") / "records.jsonl"
    if not a.report_only:
        head = final_v2.check_final()
        run([(lang, s, seed, smp, 3) for lang in REAL for s in SCRIPTS for seed in SEEDS for smp in cd_v2.SAMPLERS],
            path, head, a.workers)
    report(path)


if __name__ == "__main__":
    main()
