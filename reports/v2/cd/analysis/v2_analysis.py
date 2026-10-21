"""Post-hoc analysis of the v2 Task C/D runs (pre-registration entries 6 and 7). Descriptive only.

Reads the frozen-run records (seeds 0-2: runs/results/v2_cd; replication seeds 3-5: runs/results/v2_cd_repl)
and the v1-sister upper bound from the v1 records at the Indus point (sister_v2_main, sister_v2_gen2 for
seeds 0-2; sister_v2_repl, sister_v2_gen2_repl for seeds 3-5). Writes:
- reports/v2/cd/replication.{md,json}: seeds 3-5 tables and the entry-7 checks R1-R4;
- reports/v2/cd/pooled.md: means over seeds 0-5 with bootstrap intervals over corpora (2,000 resamples);
- reports/drafts/figures/fig_v2_taskd_per_corpus.png and fig_v2_closeness.png;
- reports/v2/cd/page_data.json: per-corpus values for the review page.
Usage (repository root): python reports/v2/cd/analysis/v2_analysis.py
"""
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
RUNS = ROOT / "runs" / "results"
CD = ROOT / "reports" / "v2" / "cd"
FIG = ROOT / "reports" / "drafts" / "figures"
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
LANGS = ["sanskrit", "tamil", "sumerian", "latin", "finnish"]
NAME = {"sanskrit": "Sanskrit", "tamil": "Old Tamil", "sumerian": "Sumerian", "latin": "Latin", "finnish": "Finnish"}
REAL = {"tamil": ["malayalam", "kannada"], "latin": ["italian"]}
UNREL = {"tamil": ["latin", "finnish"], "latin": ["tamil", "finnish"]}   # entry 8, C1
RELN = {"italian": "descendant", "malayalam": "descendant", "kannada": "sister"}
EM, EMO, FR = "knight2006_em", "knight2006_em_original", "baseline_frequency_rank"
UGARITIC = 32.0          # revised EM, natural text, related tier (reports/v2/ugaritic/results.md)
UPPER = {(0, 1, 2): ("sister_v2_main", "sister_v2_gen2"), (3, 4, 5): ("sister_v2_repl", "sister_v2_gen2_repl")}
# Yardsticks, normalised (reports/v2/real_relatives/yardsticks.md): JSD above floor, shared word forms cc (%).
YARD = {("latin", "italian"): (0.104, 11.8), ("latin", "harsh"): (0.135, 7.8),
        ("tamil", "malayalam"): (0.139, 5.7), ("tamil", "kannada"): (0.180, 4.7), ("tamil", "harsh"): (0.185, 3.6)}
INK, INK2, GRID = "#1d2422", "#5b6662", "#d5dbd8"
COL = {"italian": "#2a78d6", "malayalam": "#eb6834", "kannada": "#1baf7a", "upper": "#3a4441", "harsh": "#8f9a96"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "axes.facecolor": "white"})


ARCHIVE = CD / "records"          # gzipped copies committed with the reports (used when runs/ is absent)


def _lines(name: str):
    p = RUNS / name / "records.jsonl"
    if p.exists():
        return p.read_text().splitlines()
    a = ARCHIVE / f"{name}.jsonl.gz"
    return gzip.decompress(a.read_bytes()).decode().splitlines() if a.exists() else None


def load_runs():
    """Records of the v2 runs that exist (complete 120-corpus blocks only)."""
    out = []
    for d in ("v2_cd", "v2_cd_repl"):
        lines = _lines(d)
        if lines:
            rs = [r for r in (json.loads(line) for line in lines) if "error" not in r]
            if len({(r["lang"], r["script_type"], r["seed"], r["sampler"]) for r in rs}) == 120:   # complete blocks only
                out += rs
    return out


def load_upper():
    """(lang, script, tier) -> method -> [(sampler, seed, before-cognate acc, family_correct, reference)].
    Read from the v1 records in runs/; when they are absent, from the committed extract
    (reports/v2/cd/records/v1_upper_bound.json.gz), which holds exactly the fields used here."""
    ext = ARCHIVE / "v1_upper_bound.json.gz"
    if not (RUNS / "sister_v2_main" / "records.jsonl").exists() and ext.exists():
        out = defaultdict(lambda: defaultdict(list))
        for k, ms in json.loads(gzip.decompress(ext.read_bytes())).items():
            lang, st, tier = k.split("|")
            for m, rows in ms.items():
                out[(lang, st, tier)][m] = [tuple(x) for x in rows]
        return out
    out = defaultdict(lambda: defaultdict(list))
    for seeds, profs in UPPER.items():
        for prof, smp in zip(profs, "AB"):
            for line in (RUNS / prof / "records.jsonl").read_text().splitlines():
                r = json.loads(line)
                j = r.get("job", {})
                if "error" in r or j.get("sweep") != "size" or j.get("n_texts") != 2906 or j.get("seed") not in seeds \
                        or r["truth"]["kind"] != "language":
                    continue
                for tier in ("related", "candidates"):
                    for m in (EM, EMO, FR):
                        v = r["CD"][tier][m]
                        out[(j["source"], j["script_type"], tier)][m].append(
                            (smp, j["seed"], v.get("token_acc_before_cognate", v["token_acc"]), v["family_correct"],
                             v.get("reference")))
    return out


def values(recs, upper, lang, st, kind, tier, seeds, m=EM):
    """Per-corpus strict scores (%) for one cell; tier 'upper', 'harsh' or a relative name."""
    if tier == "upper":
        return [100 * x[2] for x in upper[(lang, st, kind)][m] if x[1] in seeds]
    key = f"{kind}_harsh" if tier == "harsh" else f"{kind}_real:{tier}"
    return [100 * r["tiers"][key][m]["strict"] for r in recs
            if r["lang"] == lang and r["script_type"] == st and r["seed"] in seeds and key in r["tiers"]]


def boot(v, n=2000, seed=2026):
    if len(v) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    a = np.array(v)
    m = a[rng.integers(len(a), size=(n, len(a)))].mean(1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def tiers_for(lang):
    return ["upper"] + REAL.get(lang, []) + ["harsh"]


def label(t):
    return {"upper": "v1 sister (upper bound)", "harsh": "`harsh` (lower bound)"}.get(t, t.capitalize())


def replication(recs, upper):
    S = (3, 4, 5)
    have = {(r["lang"], r["script_type"], r["seed"], r["sampler"]) for r in recs if r["seed"] in S}
    out = {"n_corpora": len(have), "checks": {}}
    L = ["# v2 Task C/D: fresh-seed replication, seeds 3-5 (pre-registration entry 7)", "",
         f"Corpora: {len(have)} of 120 (seeds 3-5, samplers A and B), frozen code (`frozen-v2`), the same tiers. "
         "Each cell: mean % of sign tokens over 6 corpora (number at or above 50%). Revised EM, strict, unless stated. "
         "The upper bound is read from the v1 `sister_v2_repl` and `sister_v2_gen2_repl` records.", ""]
    for kind in ("related", "candidates"):
        L += [f"## Task D, `{kind}` tier", "", "| Hidden | Relative | Relationship | " + " | ".join(SCRIPTS) + " |",
              "|---|---|---|" + "---|" * 4]
        for lang in LANGS:
            for t in tiers_for(lang):
                cells = []
                for st in SCRIPTS:
                    v = values(recs, upper, lang, st, kind, t, S)
                    cells.append(f"{np.mean(v):.1f} ({sum(x >= 50 for x in v)})" if v else "-")
                L.append(f"| {NAME[lang]} | {label(t)} | {RELN.get(t, 'synthetic')} | " + " | ".join(cells) + " |")
        L.append("")
    # R1-R4.
    means = {(lang, t, st): float(np.mean(values(recs, upper, lang, st, "related", t, S)) if values(recs, upper, lang, st, "related", t, S) else np.nan)
             for lang in REAL for t in tiers_for(lang) for st in SCRIPTS}
    r1 = {f"{t}/{st}": means[(lang, t, st)] for lang in REAL for t in REAL[lang] for st in SCRIPTS}
    r2 = {t: means[("tamil", t, "alphabetic")] for t in REAL["tamil"]}
    r3 = {st: (means[("latin", "italian", st)], means[("latin", "harsh", st)]) for st in ("alphabetic", "syllabic")}
    picks = {}
    for lang in REAL:
        for t in REAL[lang]:
            refs = [r["tiers"][f"candidates_real:{t}"][EM]["reference"] for r in recs if r["seed"] in S and r["lang"] == lang]
            picks[t] = (sum(x == t for x in refs), len(refs))
    out["checks"] = {
        "R1": {"pass": all(v < 50 for v in r1.values()), "values": r1},
        "R2": {"pass": all(22.0 <= v <= 42.0 for v in r2.values()), "values": r2},
        "R3": {"pass": all(a < b for a, b in r3.values()), "values": r3},
        "R4": {"pass": all(k < n / 2 for k, n in picks.values()), "values": picks}}
    c = out["checks"]
    word = lambda ok: "**replicated**" if ok else "**not replicated**"  # noqa: E731
    L += ["## Replication checks (fixed in entry 7 before the run)", "",
          f"- R1. Every real-relative mean below 50%: {word(c['R1']['pass'])}. Highest: "
          f"{max(r1, key=r1.get)} {max(r1.values()):.1f}%.",
          f"- R2. Old Tamil alphabetic means within 22.0-42.0% (Ugaritic 32.0% ± 10): {word(c['R2']['pass'])}. "
          + ", ".join(f"{t} {v:.1f}%" for t, v in r2.items()) + ".",
          f"- R3. Italian below `harsh` for alphabetic and syllabic: {word(c['R3']['pass'])}. "
          + ", ".join(f"{st}: Italian {a:.1f}% against `harsh` {b:.1f}%" for st, (a, b) in r3.items()) + ".",
          f"- R4. Revised rule picks the real relative in fewer than half of the `candidates_real` corpora: "
          f"{word(c['R4']['pass'])}. " + ", ".join(f"{t} {k} of {n}" for t, (k, n) in picks.items()) + ".", ""]
    L += ["## Task C (`candidates`), right family, % of corpora, seeds 3-5", "",
          "| Hidden | Relative offered | EM revised | EM original | Frequency rank | Chosen by EM revised |", "|---|---|---|---|---|---|"]
    for lang in REAL:
        for t in REAL[lang]:
            rs = [r["tiers"][f"candidates_real:{t}"] for r in recs if r["seed"] in S and r["lang"] == lang]
            fc = [100 * np.mean([x[m]["family_correct"] for x in rs]) for m in (EM, EMO, FR)]
            refs = Counter(x[EM]["reference"] for x in rs)
            L.append(f"| {NAME[lang]} | {t.capitalize()} | " + " | ".join(f"{v:.0f}%" for v in fc) + " | "
                     + ", ".join(f"{k} {n}" for k, n in refs.most_common()) + " |")
    L.append("")
    (CD / "replication.md").write_text("\n".join(L) + "\n")
    (CD / "replication.json").write_text(json.dumps(out, indent=1, default=float))
    return out


def pooled(recs, upper):
    S = tuple(sorted({r['seed'] for r in recs}))   # only seed blocks the v2 runs have, for every row
    L = [f"# v2 Task D pooled over seeds {S[0]}-{S[-1]} (descriptive; entry 7)", "",
         "Revised EM, strict, % of sign tokens. Mean over all corpora per cell (12 when both seed blocks are present) "
         "with a 95% bootstrap interval over corpora (2,000 resamples). The seeds 0-2 tables "
         "(`results.md`) stay primary. No test is made.", ""]
    data = {}
    for kind in ("related", "candidates"):
        L += [f"## `{kind}` tier", "", "| Hidden | Relative | Relationship | " + " | ".join(SCRIPTS) + " |",
              "|---|---|---|" + "---|" * 4]
        for lang in LANGS:
            for t in tiers_for(lang):
                cells = []
                for st in SCRIPTS:
                    v = values(recs, upper, lang, st, kind, t, S)
                    lo, hi = boot(v)
                    data[(kind, lang, t, st)] = (float(np.mean(v)), lo, hi, len(v)) if v else None
                    cells.append(f"{np.mean(v):.1f} ({lo:.1f}-{hi:.1f}), n={len(v)}" if v else "-")
                L.append(f"| {NAME[lang]} | {label(t)} | {RELN.get(t, 'synthetic')} | " + " | ".join(cells) + " |")
        L.append("")
    (CD / "pooled.md").write_text("\n".join(L) + "\n")
    return data


def fig_per_corpus(recs, upper, pool):
    S = tuple(sorted({r['seed'] for r in recs}))   # only seed blocks the v2 runs have, for every row
    fig, axes = plt.subplots(2, 4, figsize=(7.4, 4.3), sharex=True,
                             gridspec_kw={"height_ratios": [4, 3], "hspace": 0.35, "wspace": 0.08})
    rng = np.random.default_rng(7)
    xmax = 5 + max(x for lang in ("tamil", "latin") for t in tiers_for(lang) for st in SCRIPTS
                   for x in values(recs, upper, lang, st, "related", t, S))
    for i, lang in enumerate(("tamil", "latin")):
        ts = tiers_for(lang)
        for j, st in enumerate(SCRIPTS):
            ax = axes[i, j]
            ax.axvline(50, color=INK2, lw=0.8, ls=(0, (4, 3)), zorder=1)
            if st == "alphabetic":
                ax.axvline(UGARITIC, color=INK2, lw=0.8, ls=(0, (1, 2)), zorder=1)
            for k, t in enumerate(ts):
                y = len(ts) - 1 - k
                v = values(recs, upper, lang, st, "related", t, S)
                col = COL[t if t in COL else "upper"]
                mk = {"upper": "s", "harsh": "^"}.get(t, "o")
                ax.scatter(v, y + rng.uniform(-0.18, 0.18, len(v)), s=13, marker=mk, color=col, alpha=0.85,
                           edgecolors="white", linewidths=0.4, zorder=3)
                m, lo, hi, _ = pool[("related", lang, t, st)]
                ax.plot([lo, hi], [y, y], color=INK, lw=1.0, zorder=4)
                ax.plot([m, m], [y - 0.32, y + 0.32], color=INK, lw=1.8, zorder=4)
            ax.set_ylim(-0.6, len(ts) - 0.4)
            ax.set_xlim(-3, xmax)
            ax.set_yticks(range(len(ts)))
            ax.set_yticklabels([] if j else [{"upper": "v1 sister", "harsh": "harsh"}.get(t, t.capitalize())
                                             for t in reversed(ts)])
            ax.tick_params(axis="y", length=0)
            ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
            if i == 0:
                ax.set_title(st.replace("logosyllabic", "logo-syllabic"), fontsize=8.5, color=INK)
            if j == 0:
                ax.set_ylabel(NAME[lang], fontsize=9, color=INK)
    fig.supxlabel("sign tokens recovered, % (one mark per corpus; bar = mean with 95% bootstrap interval)",
                  fontsize=8, color=INK, y=0.0)
    fig.text(0.5, -0.06, "dashed line: 50% threshold    dotted line (alphabetic): Ugaritic-Hebrew, 32%    "
             "square: v1 sister    triangle: harsh    circle: real relative", ha="center", fontsize=7, color=INK2)
    fig.savefig(FIG / "fig_v2_taskd_per_corpus.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def fig_closeness(pool):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True, gridspec_kw={"wspace": 0.12})
    for ax, idx, xl in ((axes[0], 0, "letter-pair JSD above floor (bits)\n<- closer"),
                        (axes[1], 1, "shared word forms, chance-corrected (%)\ncloser ->")):
        xs0 = [YARD[k][idx] for k in YARD]
        ax.set_xlim(min(xs0) - 0.12 * (max(xs0) - min(xs0)), max(xs0) + 0.12 * (max(xs0) - min(xs0)))
        for lang in ("latin", "tamil"):
            pts = []
            for t in REAL[lang] + ["harsh"]:
                x = YARD[(lang, t)][idx]
                m, lo, hi, _ = pool[("related", lang, t, "alphabetic")]
                col = COL[t]
                mk = "^" if t == "harsh" else "o"
                ax.plot([x, x], [lo, hi], color=col, lw=1.0, zorder=2)
                ax.scatter([x], [m], s=34, marker=mk, color=col, edgecolors="white", linewidths=0.6, zorder=3)
                name = f"{NAME[lang]} harsh" if t == "harsh" else t.capitalize()
                right = x > np.mean(ax.get_xlim()) or (idx == 1 and t == "kannada")   # keep labels apart
                ax.annotate(name, (x, m), xytext=(-5 if right else 5, 3), textcoords="offset points", fontsize=7,
                            color=INK, ha="right" if right else "left")
                pts.append((x, m))
        xs = [YARD[k][idx] for k in YARD]
        pad = 0.12 * (max(xs) - min(xs))
        ax.set_xlim(min(xs) - pad, max(xs) + pad)
        ax.set_xlabel(xl, fontsize=7.5)
        ax.grid(color=GRID, lw=0.6, zorder=0)
    axes[0].set_ylabel("Task D, alphabetic, related (%)")
    axes[0].set_ylim(0, 60)
    fig.savefig(FIG / "fig_v2_closeness.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_upper_extract(upper) -> None:
    ext = ARCHIVE / "v1_upper_bound.json.gz"
    data = {"|".join(k): {m: [list(x) for x in rows] for m, rows in ms.items()} for k, ms in upper.items()}
    ext.write_bytes(gzip.compress(json.dumps(data, sort_keys=True).encode(), mtime=0))


def load_controls():
    lines = _lines("v2_controls")
    if not lines:
        return None
    rs = [r for r in (json.loads(line) for line in lines) if "error" not in r]
    keys = {(r["lang"], r["script_type"], r["seed"], r["sampler"]) for r in rs}
    return rs if len(keys) == 96 else None                        # complete runs only (entry 8)


def controls(recs, ctrl):
    """Entry 8: C1 unrelated reference, C2 constant floor, C3 budget, C4 determinism."""
    key = lambda r: (r["lang"], r["script_type"], r["seed"], r["sampler"])  # noqa: E731
    main = {key(r): r for r in recs}
    cr = {key(r): r for r in ctrl}
    out = {"C1": [], "C2": [], "C3": [], "C4": {}, "diag": {}}
    for lang in REAL:
        for rel in REAL[lang]:
            g = f"real:{rel}"
            for st in SCRIPTS:
                ks = sorted(k for k in cr if k[0] == lang and k[1] == st and k in main)
                real = [100 * main[k]["tiers"][f"related_{g}"][EM]["strict"] for k in ks]
                un = {u: [100 * cr[k]["unrelated"][u][EM][g]["strict"] for k in ks] for u in UNREL[lang]}
                best = max(un, key=lambda u: np.mean(un[u]))
                wins = sum(a > b for a, b in zip(real, un[best]))
                added = float(np.mean(real) - np.mean(un[best]))
                fl = [100 * cr[k]["floor"][g] for k in ks]
                out["C1"].append({"lang": lang, "rel": rel, "script": st, "n": len(ks), "real": float(np.mean(real)),
                                  **{f"unrel_{u}": float(np.mean(v)) for u, v in un.items()}, "best_unrel": best,
                                  "added": added, "wins": wins, "helps": added >= 5 and wins >= 9,
                                  "freq_unrel": {u: float(np.mean([100 * cr[k]["unrelated"][u][FR][g]["strict"] for k in ks]))
                                                 for u in UNREL[lang]}})
                out["C2"].append({"lang": lang, "rel": rel, "script": st, "floor": float(np.mean(fl)),
                                  "real": float(np.mean(real)), "at_floor": float(np.mean(real)) <= float(np.mean(fl)) + 2})
        for t in REAL[lang] + ["harsh"]:
            name = "harsh" if t == "harsh" else f"real:{t}"
            for st in SCRIPTS:
                ks = sorted(k for k in cr if k[0] == lang and k[1] == st and cr[k]["budget"])
                v3 = [100 * cr[k]["budget"][name]["3"]["strict"] for k in ks]
                v10 = [100 * cr[k]["budget"][name]["10"]["strict"] for k in ks]
                d = float(np.mean(v10) - np.mean(v3))
                out["C3"].append({"lang": lang, "tier": t, "script": st, "n": len(ks), "r3": float(np.mean(v3)),
                                  "r10": float(np.mean(v10)), "delta": d, "first_order": abs(d) > 10,
                                  "changed": sum(abs(a - b) > 1e-9 for a, b in zip(v3, v10))})
    mism, n = [], 0
    for k, r in cr.items():
        for name, b in r["budget"].items():
            n += 1
            frozen = main[k]["tiers"][f"related_{name}"][EM]["strict"]
            if abs(b["3"]["strict"] - frozen) > 1e-12:
                mism.append({"corpus": k, "tier": name, "rerun": b["3"]["strict"], "frozen": frozen})
    out["C4"] = {"compared": n, "mismatches": mism}
    for lang in REAL:
        tops_real = [cr[k]["budget"][f"real:{t}"]["3"]["diag"]["top_unit_share"] for k in cr if k[0] == lang and cr[k]["budget"]
                     for t in REAL[lang]]
        tops_un = [cr[k]["unrelated"][u][EM]["diag"]["top_unit_share"] for k in cr if k[0] == lang for u in UNREL[lang]]
        out["diag"][lang] = {"top_unit_share_real": float(np.mean(tops_real)), "top_unit_share_unrel": float(np.mean(tops_un))}
    write_controls_md(out)
    (CD / "controls.json").write_text(json.dumps(out, indent=1, default=float))
    return out


def write_controls_md(c):
    f = lambda x: f"{x:.1f}"  # noqa: E731
    L = ["# v2 Task D controls (pre-registration entry 8)", "",
         "Post hoc in motivation, pre-registered in procedure; readings fixed in entry 8 before the run. Revised EM, "
         "strict score, % of sign tokens, `related` tier. Corpora: Latin and Old Tamil, four script types, seeds 0-5, "
         "samplers A and B (C3 and C4: seeds 0-2). Code: `reports/v2/cd/analysis/controls.py` (frozen functions only).", "",
         "## C1. Does the real relative beat an unrelated reference scored against the same gold?", "",
         "The unrelated reference is a v1 language given as the only reference; its predictions are scored against the "
         "real relative's gold, exactly as the relative's own run. *Helps* = added value at least 5 points and the "
         "relative ahead of the better unrelated reference in at least 9 of the 12 paired corpora.", "",
         "| Relative | Script | Relative | Unrelated: " + " / ".join(["first", "second"]) + " | Added value | Corpora ahead | Reading |",
         "|---|---|---|---|---|---|---|"]
    for r in c["C1"]:
        us = [k for k in r if k.startswith("unrel_")]
        L.append(f"| {r['rel'].capitalize()} ({NAME[r['lang']]}) | {r['script']} | {f(r['real'])} | "
                 + " / ".join(f"{NAME[k[6:]]} {f(r[k])}" for k in us)
                 + f" | {r['added']:+.1f} | {r['wins']} of {r['n']} | {'helps' if r['helps'] else 'no measurable help'} |")
    L += ["", "## C2. Constant-prediction floor", "",
          "Strict score of the best single-unit answer (every sign mapped to the most common regular reflex), mean over "
          "corpora. *At the floor* = the relative's mean is no more than 2 points above it.", "",
          "| Relative | Script | Floor | Relative | Reading |", "|---|---|---|---|---|"]
    for r in c["C2"]:
        L.append(f"| {r['rel'].capitalize()} ({NAME[r['lang']]}) | {r['script']} | {f(r['floor'])} | {f(r['real'])} | "
                 f"{'at the floor' if r['at_floor'] else 'above the floor'} |")
    L += ["", "## C3. Solver budget: 10 EM restarts against 3 (seeds 0-2)", "",
          "The first three restarts are identical; the best likelihood is kept. *First-order* = the mean moves by more "
          "than 10 points.", "", "| Hidden | Tier | Script | 3 restarts | 10 restarts | Change | Corpora changed | Reading |",
          "|---|---|---|---|---|---|---|---|"]
    for r in c["C3"]:
        L.append(f"| {NAME[r['lang']]} | {r['tier']} | {r['script']} | {f(r['r3'])} | {f(r['r10'])} | {r['delta']:+.1f} | "
                 f"{r['changed']} of {r['n']} | {'first-order' if r['first_order'] else 'second-order'} |")
    m = c["C4"]["mismatches"]
    L += ["", "## C4. Determinism", "",
          f"The 3-restart rerun was compared with the frozen-run record for {c['C4']['compared']} corpus-tier pairs: "
          + ("all identical." if not m else f"**{len(m)} mismatches** (reproducibility failure): "
             + "; ".join(f"{x['corpus']} {x['tier']}: {100 * x['rerun']:.3f} against {100 * x['frozen']:.3f}" for x in m[:10])),
          "", "## Diagnostics", "",
          "Mean share of sign tokens assigned to the single most common predicted unit (a degeneracy index; no threshold):", ""]
    for lang, d in c["diag"].items():
        L.append(f"- {NAME[lang]}: real relatives {100 * d['top_unit_share_real']:.1f}%, unrelated references "
                 f"{100 * d['top_unit_share_unrel']:.1f}%.")
    (CD / "controls.md").write_text("\n".join(L) + "\n")


def fig_controls(c):
    rows = list(c["C1"])                                   # every cell, logographic included
    fl = {(r["lang"], r["rel"], r["script"]): r["floor"] for r in c["C2"]}
    fig, ax = plt.subplots(figsize=(6.6, 0.32 * len(rows) + 0.9))
    for i, r in enumerate(rows):
        y = len(rows) - 1 - i
        best = r[f"unrel_{r['best_unrel']}"]
        f0 = fl[(r["lang"], r["rel"], r["script"])]
        ax.plot([0, f0], [y, y], color=GRID, lw=5, solid_capstyle="butt", zorder=1)
        ax.plot([best, r["real"]], [y, y], color=INK2, lw=0.8, zorder=2)
        ax.scatter([best], [y], marker="D", s=26, facecolor="white", edgecolor=INK, linewidths=0.9, zorder=3)
        ax.scatter([r["real"]], [y], marker="o", s=36, color=COL[r["rel"]], edgecolor="white", linewidths=0.6, zorder=4)
        ax.text(max(best, r["real"]) + 1.2, y, f"{r['added']:+.1f}" + (" *" if r["helps"] else ""), va="center",
                fontsize=7, color=INK)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{r['rel'].capitalize()}, {r['script'].replace('logosyllabic', 'logo-syllabic')}" for r in reversed(rows)])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, max(max(r["real"], r[f"unrel_{r['best_unrel']}"]) for r in rows) + 12)
    ax.grid(axis="x", color=GRID, lw=0.6, zorder=0)
    ax.set_xlabel("sign tokens recovered (%), mean over 12 corpora, scored against the relative's gold")
    fig.text(0.01, -0.04, "circle: the real relative    diamond: the better unrelated reference    grey bar: constant-answer "
             "floor    number: added value (* = helps by the entry-8 rule)", fontsize=6.8, color=INK2)
    fig.savefig(FIG / "fig_v2_controls.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def page_data(recs, upper, pool, ctl=None):
    cells = []
    for kind in ("related", "candidates"):
        for lang in LANGS:
            for t in tiers_for(lang):
                for st in SCRIPTS:
                    p = pool.get((kind, lang, t, st))
                    if not p:
                        continue
                    pc = []
                    for seeds in [b for b in ((0, 1, 2), (3, 4, 5)) if set(b) <= {r["seed"] for r in recs}]:
                        if t == "upper":
                            pc += [{"sampler": x[0], "seed": x[1], "v": round(100 * x[2], 1)}
                                   for x in upper[(lang, st, kind)][EM] if x[1] in seeds]
                        else:
                            key = f"{kind}_harsh" if t == "harsh" else f"{kind}_real:{t}"
                            pc += [{"sampler": r["sampler"], "seed": r["seed"],
                                    "v": round(100 * r["tiers"][key][EM]["strict"], 1),
                                    "ref": r["tiers"][key][EM]["reference"]}
                                   for r in recs if r["lang"] == lang and r["script_type"] == st and r["seed"] in seeds]
                    cells.append({"tier": kind, "lang": lang, "rel": t, "relationship": RELN.get(t, "synthetic"),
                                  "script": st, "mean": round(p[0], 1), "lo": round(p[1], 1), "hi": round(p[2], 1),
                                  "n": p[3], "corpora": pc})
    out = {"cells": cells, "ugaritic": UGARITIC, "yardsticks": {f"{a}:{b}": v for (a, b), v in YARD.items()}}
    if ctl:
        fl = {(r["lang"], r["rel"], r["script"]): r["floor"] for r in ctl["C2"]}
        out["controls"] = [{"lang": r["lang"], "rel": r["rel"], "script": r["script"], "real": round(r["real"], 1),
                            "unrel": {u[6:]: round(r[u], 1) for u in r if u.startswith("unrel_")},
                            "best": r["best_unrel"], "added": round(r["added"], 1), "wins": r["wins"], "n": r["n"],
                            "helps": r["helps"], "floor": round(fl[(r["lang"], r["rel"], r["script"])], 1)}
                           for r in ctl["C1"]]
        out["budget"] = [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items()} for r in ctl["C3"]]
        out["determinism"] = {"compared": ctl["C4"]["compared"], "mismatches": len(ctl["C4"]["mismatches"])}
    (CD / "page_data.json").write_text(json.dumps(out))


def main():
    recs = load_runs()
    upper = load_upper()
    if (RUNS / "sister_v2_main" / "records.jsonl").exists():
        write_upper_extract(upper)
    rep = replication(recs, upper) if any(r["seed"] >= 3 for r in recs) else None
    pool = pooled(recs, upper)
    fig_per_corpus(recs, upper, pool)
    fig_closeness(pool)
    ctrl = load_controls()
    ctl = controls(recs, ctrl) if ctrl and rep else None
    if ctl:
        fig_controls(ctl)
    page_data(recs, upper, pool, ctl)
    print("records:", len(recs), "replication:", None if rep is None else {k: v["pass"] for k, v in rep["checks"].items()},
          "controls:", None if ctl is None else "done")


if __name__ == "__main__":
    main()
