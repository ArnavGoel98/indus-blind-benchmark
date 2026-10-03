"""Command-line entry points.

    ibdb fetch [names...] [--allow-large]   download sources (refuses >500 MB without approval)
    ibdb prepare [names...]                 extract seal-like segments
    ibdb calibrate --profile full           fit generator knobs to the Indus targets (3 regimes)
    ibdb run --profile full                 run every method on every corpus (resumable)
    ibdb report --profile full              aggregate, figures, calibration + results reports
    ibdb reproduce --profile full           all of the above, in order (one command, every figure)
    ibdb challenge build --round R --tier public|hidden [--n 24]
    ibdb challenge baseline --round R --tier public|hidden [--record]
    ibdb leaderboard                        rebuild leaderboard/index.html from leaderboard/data.json
    ibdb methods                            print each method's paper and documented deviations
    ibdb sensitivity run|report             duplicate-rate x sign-inventory map at the Indus point
    ibdb-score submission.json --round R --tier hidden [--record]
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def _workers(n: int | None) -> int:
    return n or max(1, min(4, (os.cpu_count() or 2)))


def cmd_fetch(a):
    from .data.fetch import fetch
    fetch(a.names or None, allow_large=a.allow_large)


def cmd_prepare(a):
    from .data.prepare import prepare
    prepare(a.names or None)


def cmd_calibrate(a):
    from . import config
    from .generator.calibrate import calibrate_all
    p = config.experiment()["profiles"][a.profile]
    calibrate_all(p["languages"], p["script_types"], p["controls"], p["regimes"], workers=_workers(a.workers),
                  generator_version=p.get("generator_version", "v1"))


def cmd_run(a):
    from .evaluate import run
    run(a.profile, workers=_workers(a.workers))


def cmd_report(a):
    from . import config, figures, reports
    from .evaluate import aggregate
    agg = aggregate(a.profile)
    prof = config.experiment()["profiles"][a.profile]
    from pathlib import Path
    out = Path(a.out_dir) if getattr(a, "out_dir", None) else None
    fig_dir = out / "figures" if out else None
    paths = reports.write_all(a.profile, agg, out)
    paths += figures.decipherability(agg, prof, fig_dir)
    paths.append(figures.headline(agg, prof, fig_dir))
    paths.append(figures.control_fp(agg, prof, fig_dir))
    from .evaluate import load_records
    eb = figures.entropy_bias(load_records(a.profile), fig_dir, prof["indus_point"]["n_texts"])
    if eb:
        paths.append(eb)
    sp = figures.sister_sweep(agg, fig_dir)
    if sp:
        paths.append(sp)
    for p in paths:
        print(f"[report] wrote {p}")


def cmd_reproduce(a):
    for step in (cmd_fetch, cmd_prepare, cmd_calibrate, cmd_run, cmd_report):
        print(f"== {step.__name__.replace('cmd_', '')}")
        step(a)


def cmd_challenge(a):
    from . import challenge, leaderboard
    if a.action == "build":
        root = challenge.build_round(a.round, a.tier, a.n)
        print(f"[challenge] wrote {root}")
    elif a.action == "baseline":
        sub = leaderboard.baseline_submission(a.round, a.tier, a.profile)
        out = challenge.project_root() / "challenge" / a.tier / a.round / "baseline_submission.json"
        out.write_text(json.dumps(sub))
        scores = challenge.score_submission(sub, a.round, a.tier)
        print(json.dumps(scores, indent=1))
        if a.record:
            challenge.record_score(sub, scores, a.round, a.tier, force=True)
            leaderboard.build_page()


def cmd_leaderboard(a):
    from .leaderboard import build_page
    print(f"[leaderboard] wrote {build_page()}")


def cmd_sensitivity(a):
    from . import sensitivity
    if a.action == "run":
        sensitivity.run(a.profile, workers=_workers(a.workers), limit=a.limit)
    else:
        from . import figures, reports
        agg = sensitivity.aggregate(a.profile)
        for p in [sensitivity.write_aggregate(a.profile), *figures.sensitivity_maps(agg),
                  reports.sensitivity_report(agg)]:
            print(f"[sensitivity] wrote {p}")


def cmd_methods(a):
    from .evaluate import all_methods
    for m in all_methods():
        d = m.describe()
        print(f"## {d['name']}  (tasks {', '.join(d['tasks'])})\nPaper: {d['paper']}\nDeviations: {d['deviations']}\n")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="ibdb", description="Indus Blind Decipherment Benchmark")
    sp = ap.add_subparsers(dest="cmd", required=True)

    def common(p, names=False):
        p.add_argument("--profile", default="full")
        p.add_argument("--workers", type=int, default=None)
        p.add_argument("--allow-large", action="store_true")
        p.add_argument("--out-dir", default=None, help="report: write reports/figures here instead of reports/")
        if names:
            p.add_argument("names", nargs="*")
        else:
            p.set_defaults(names=[])

    for name, fn, names in (("fetch", cmd_fetch, True), ("prepare", cmd_prepare, True), ("calibrate", cmd_calibrate, False),
                            ("run", cmd_run, False), ("report", cmd_report, False), ("reproduce", cmd_reproduce, False),
                            ("leaderboard", cmd_leaderboard, False), ("methods", cmd_methods, False)):
        p = sp.add_parser(name)
        common(p, names)
        p.set_defaults(func=fn)
    p = sp.add_parser("challenge")
    p.add_argument("action", choices=["build", "baseline"])
    p.add_argument("--round", required=True)
    p.add_argument("--tier", choices=["public", "hidden"], default="public")
    p.add_argument("--n", type=int, default=24)
    p.add_argument("--record", action="store_true")
    p.add_argument("--profile", default="full")
    p.set_defaults(func=cmd_challenge)
    p = sp.add_parser("sensitivity")
    p.add_argument("action", choices=["run", "report"])
    p.add_argument("--profile", default="sensitivity")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.set_defaults(func=cmd_sensitivity)
    return ap


def main(argv: list[str] | None = None) -> None:
    a = build_parser().parse_args(argv)
    a.func(a)


def fetch_main() -> None:
    main(["fetch", *sys.argv[1:]])


def reproduce_main() -> None:
    main(["reproduce", *sys.argv[1:]])
