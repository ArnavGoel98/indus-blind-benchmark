"""Pre-registration entry 9: Finnish-Estonian replication (seeds 3-5) and controls (C1, C2; seeds 0-5).

The seeds 0-2 primary run is the frozen `python scripts/v2/cd_v2.py --relative estonian`. This driver
calls the frozen `run_corpus` (replication, as entry 7) and the entry-8 `run_control` (C1 with Latin and
Old Tamil as unrelated references, and C2; no budget runs) unchanged.
Usage (repository root): python reports/v2/cd/analysis/estonian.py {repl|controls} [--workers 4]
Writes runs/results/v2_cd_repl/records_estonian.jsonl or runs/results/v2_controls/records_estonian.jsonl.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cd_v2  # noqa: E402  (sets IBDB_SISTER_VERSION=v2 on import, as for the main run)
import controls  # noqa: E402
from ibdb.paths import ensure, runs_dir  # noqa: E402

controls.UNREL["finnish"] = ["latin", "tamil"]


def control_job(job):
    controls.UNREL["finnish"] = ["latin", "tamil"]      # set again in each spawned worker
    return controls.run_control(job)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("part", choices=["repl", "controls"])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    cd_v2.check_frozen()
    assert cd_v2.REAL["finnish"] == ["estonian"], "no Estonian gold table"
    if a.part == "repl":
        jobs = [("finnish", st, s, smp, 3, 60, "estonian") for smp in cd_v2.SAMPLERS for s in (3, 4, 5) for st in cd_v2.SCRIPTS]
        fn, path = cd_v2.run_corpus, ensure(runs_dir() / "results" / "v2_cd_repl") / "records_estonian.jsonl"
    else:
        jobs = [("finnish", st, s, smp, False) for smp in cd_v2.SAMPLERS for s in range(6) for st in cd_v2.SCRIPTS]
        fn, path = control_job, ensure(runs_dir() / "results" / "v2_controls") / "records_estonian.jsonl"
    done = set()
    if path.exists():
        for line in path.read_text().splitlines():
            r = json.loads(line)
            if "error" not in r:
                done.add((r["lang"], r["script_type"], r["seed"], r["sampler"]))
    todo = [j for j in jobs if j[:4] not in done]
    print(f"[estonian {a.part}] {len(jobs)} corpora, {len(todo)} to do -> {path}", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=get_context("spawn")) as ex:
        futs = {ex.submit(fn, j): j for j in todo}
        for i, f in enumerate(as_completed(futs), 1):
            j = futs[f]
            try:
                r = f.result()
            except Exception:  # noqa: BLE001 - recorded, not hidden
                r = {"lang": j[0], "script_type": j[1], "seed": j[2], "sampler": j[3], "error": traceback.format_exc()}
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, default=float, ensure_ascii=False) + "\n")
            print(f"[estonian {a.part}] {i}/{len(todo)} {time.time() - t0:.0f}s {j[:4]}{' ERROR' if 'error' in r else ''}",
                  flush=True)


if __name__ == "__main__":
    main()
