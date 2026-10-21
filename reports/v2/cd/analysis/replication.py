"""Pre-registration entry 7: fresh-seed replication (seeds 3-5) of the v2 Task C/D run.

Calls the frozen `run_corpus` and `check_frozen` of scripts/v2/cd_v2.py unchanged; only the seed list
differs. Lives under reports/ (entry 7) so the frozen-code check keeps guarding the methods.
Usage (from the repository root): python reports/v2/cd/analysis/replication.py [--workers 4]
Writes runs/results/v2_cd_repl/records.jsonl (resumable).
"""
import argparse
import json
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts" / "v2"))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import, as for the main run)
from ibdb.paths import ensure, runs_dir  # noqa: E402

SEEDS = (3, 4, 5)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    cd_v2.check_frozen()
    jobs = [(lang, st, s, smp, 3, 60, None) for smp in cd_v2.SAMPLERS for s in SEEDS
            for lang in cd_v2.LANGUAGES for st in cd_v2.SCRIPTS]
    path = ensure(runs_dir() / "results" / "v2_cd_repl") / "records.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j[:4] not in done]
    print(f"[v2_cd_repl] {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(cd_v2.run_corpus, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r = f.result()
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[v2_cd_repl] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}", flush=True)


if __name__ == "__main__":
    main()
