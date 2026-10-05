"""Sister-v1 vs sister-v2 comparison for the related and candidates tiers (analysis of saved records only).

Sister-v1 numbers come from the frozen-v1 runs and are an "upper bound (sister-v1, known overlap)".
Sister-v2 numbers come from the sister_v2_* profiles. After-cognate scores are labelled
"with oracle sound correspondences"; the before-cognate column (token_acc_before_cognate) exists only
for sister-v2 records. When the solver did not pick the sister, before = after (no cognate step ran).

Usage: python scripts/sister_compare.py > reports/sister_v2/comparison.md
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

RUNS = Path("runs/results")
PAIRS = [  # label, sister-v1 records, sister-v2 records
    ("Generator-v1, seeds 0-2", "full", "sister_v2_main"),
    ("Generator-v1, seeds 3-5", "replication", "sister_v2_repl"),
    ("Generator-v2, seeds 0-2", "generator_v2", "sister_v2_gen2"),
    ("Generator-v2, seeds 3-5", None, "sister_v2_gen2_repl"),
]
METHODS = [("knight2006_em_original", "original (frozen)"), ("knight2006_em", "revised (post hoc)")]
TIERS = ["related", "candidates"]
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]


def load(name):
    p = RUNS / str(name) / "records.jsonl"
    if not name or not p.exists():
        return {}
    out = {}
    for line in p.open():
        r = json.loads(line)
        j = r["job"]
        if j["sweep"] not in ("size", "length") or j["regime"] != "full" or j["pred_script"] or \
                r["truth"]["kind"] != "language":
            continue
        out[(j["sweep"], j["source"], j["script_type"], j["seed"], j["n_texts"], j["mean_length"])] = r
    return out


def vals(recs, keys, tier, m, before=False):
    xs = []
    for k in keys:
        d = recs[k]["CD"].get(tier, {}).get(m)
        if d is None:
            continue
        v = d.get("token_acc_before_cognate", d["token_acc"]) if before else d["token_acc"]
        xs.append((k[1], v))
    return xs


def ci(xs, n_boot=2000, seed=0):
    """Mean with a 95% interval resampling whole source languages."""
    if not xs:
        return None
    by = {}
    for lang, v in xs:
        by.setdefault(lang, []).append(v)
    langs = sorted(by)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        pick = rng.choice(len(langs), len(langs))
        boots.append(np.mean([v for i in pick for v in by[langs[i]]]))
    return 100 * np.mean([v for _, v in xs]), 100 * np.percentile(boots, 2.5), 100 * np.percentile(boots, 97.5)


def fmt(c, interval=True):
    if c is None:
        return "n/a"
    return f"{c[0]:.1f} [{c[1]:.1f}, {c[2]:.1f}]" if interval else f"{c[0]:.1f}"


def point_keys(recs, sweep, n, L):
    return sorted(k for k in recs if k[0] == sweep and k[4] == n and abs(k[5] - L) < 1e-9)


def mean_at(recs, sweep, n, L, tier, m, before=False):
    xs = vals(recs, point_keys(recs, sweep, n, L), tier, m, before)
    return 100 * np.mean([v for _, v in xs]) if xs else None


def size_interp(recs, tokens, tier, m, before=False):
    pts = sorted({(k[4], k[5]) for k in recs if k[0] == "size"})
    xy = [(np.log(n * L), mean_at(recs, "size", n, L, tier, m, before)) for n, L in pts]
    xy = [p for p in xy if p[1] is not None]
    if not xy:
        return None
    xs, ys = zip(*xy)
    return float(np.interp(np.log(tokens), xs, ys))


def main():
    print("# Sister-v1 vs sister-v2: related and candidates tiers\n")
    print("Analysis of saved records only. Methods frozen at `frozen-v1`. Task D token accuracy, %, "
          "mean over 20 corpora per seed (5 languages x 4 script types), 95% interval resampling whole "
          "languages.\n")
    print("- **sister-v1**: upper bound (sister-v1, known overlap). Clauses split by index, so identical "
          "clauses can sit in both halves.")
    print("- **sister-v2**: clauses split by a hash of their content; 0 identical clauses shared.")
    print("- **after cognate** = with oracle sound correspondences (the solver's frozen `_translate` step "
          "uses the true sister-to-hidden map). **before cognate** = the raw sister-unit prediction scored "
          "directly; equal to after cognate when the sister was not chosen. Recorded for sister-v2 only.\n")

    for label, old_name, new_name in PAIRS:
        old, new = load(old_name), load(new_name)
        if not new:
            print(f"## {label}\n\nsister-v2 records not available yet.\n")
            continue
        n_new = len(point_keys(new, "size", 2906, 4.6))
        print(f"## {label}\n")
        print(f"### Indus point (2,906 texts x 4.6 signs), {n_new} sister-v2 corpora\n")
        print("| Tier | Rule | sister-v1, upper bound (known overlap) | sister-v2, with oracle sound "
              "correspondences | sister-v2, before cognate |")
        print("|---|---|---|---|---|")
        for tier in TIERS:
            for m, rule in METHODS:
                o = ci(vals(old, point_keys(old, "size", 2906, 4.6), tier, m)) if old else None
                a = ci(vals(new, point_keys(new, "size", 2906, 4.6), tier, m))
                b = ci(vals(new, point_keys(new, "size", 2906, 4.6), tier, m, before=True))
                print(f"| {tier} | {rule} | {fmt(o) if old else 'no sister-v1 run'} | {fmt(a)} | {fmt(b)} |")
        print()

        print("### Corpus size (4.6 signs), original rule, candidates tier\n")
        sizes = sorted({k[4] for k in new if k[0] == "size"})
        print("| Texts | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |")
        print("|---|---|---|---|")
        for n in sizes:
            o = mean_at(old, "size", n, 4.6, "candidates", METHODS[0][0]) if old else None
            a = mean_at(new, "size", n, 4.6, "candidates", METHODS[0][0])
            b = mean_at(new, "size", n, 4.6, "candidates", METHODS[0][0], True)
            f = lambda x: "n/a" if x is None else f"{x:.1f}"  # noqa: E731
            print(f"| {n:,} | {f(o)} | {f(a)} | {f(b)} |")
        print()

        print("### Longer vs more inscriptions at equal tokens, original rule, candidates tier\n")
        print("Length points: 2,906 texts at the given mean length, with interval. Size: interpolated on "
              "log(tokens) between size points, no interval.\n")
        print("| Signs/text (tokens) | sister-v1: length vs size | sister-v2 oracle corr.: length vs size | "
              "sister-v2 before cognate: length vs size |")
        print("|---|---|---|---|")
        for L in (6.0, 10.0, 20.0):
            tok = 2906 * L
            cells = []
            for recs, before in ((old, False), (new, False), (new, True)):
                if not recs:
                    cells.append("no sister-v1 run")
                    continue
                c = ci(vals(recs, point_keys(recs, "length", 2906, L), "candidates", METHODS[0][0], before))
                s = size_interp(recs, tok, "candidates", METHODS[0][0], before)
                mark = "**" if c and s is not None and (c[1] > s) else ""
                cells.append(f"{mark}{fmt(c)} vs {s:.1f}{mark}" if c and s is not None else "n/a")
            print(f"| {L:g} ({tok:,.0f}) | " + " | ".join(cells) + " |")
        print("\nBold: the length interval lies above the interpolated size value.\n")

        print("### How often the sister was chosen at the Indus point (candidates tier)\n")
        for m, rule in METHODS:
            ks = point_keys(new, "size", 2906, 4.6)
            ch = [new[k]["CD"]["candidates"][m]["reference"].endswith("-sister") for k in ks]
            oc = None
            if old:
                ko = point_keys(old, "size", 2906, 4.6)
                oc = np.mean([old[k]["CD"]["candidates"][m]["reference"].endswith("-sister") for k in ko])
            print(f"- {rule}: sister-v2 {100 * np.mean(ch):.0f}% of corpora"
                  + (f"; sister-v1 {100 * oc:.0f}%" if oc is not None else ""))
        print()

        print("### Per-language, Indus point, original rule, candidates tier\n")
        print("| Language | sister-v1 upper bound | sister-v2 oracle corr. | sister-v2 before cognate |")
        print("|---|---|---|---|")
        for lang in LANGS:
            row = []
            for recs, before in ((old, False), (new, False), (new, True)):
                ks = [k for k in point_keys(recs, "size", 2906, 4.6) if k[1] == lang] if recs else []
                xs = vals(recs, ks, "candidates", METHODS[0][0], before) if ks else []
                row.append(f"{100 * np.mean([v for _, v in xs]):.1f}" if xs else "n/a")
            print(f"| {lang} | " + " | ".join(row) + " |")
        print()


if __name__ == "__main__":
    main()
