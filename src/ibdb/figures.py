"""Figures. Static PNG + SVG via matplotlib (palette: fixed categorical order, thin marks)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from .paths import ensure, reports_dir  # noqa: E402

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, INK2, GRID, BAND = "#0b0b0b", "#52514e", "#e4e3df", "#d9d8d3"

A_NAMES = ["rao2009_entropy", "yadav2010_markov", "fuls_positional", "lee2010_tree", "ling_classifier_lr"]
B_NAMES = ["script_type_inventory_rule", "script_type_lr", "segmentation_branching"]
D_NAMES = ["baseline_frequency_rank", "knight2006_em", "knight2006_em_original", "em_cognate_matcher"]
LABEL = {
    "rao2009_entropy": "Rao 2009 entropy", "yadav2010_markov": "Yadav 2010 n-gram", "fuls_positional": "Positional",
    "lee2010_tree": "Lee 2010 tree", "ling_classifier_lr": "Multi-feature LR",
    "script_type_inventory_rule": "Inventory rule", "script_type_lr": "Inventory/freq. LR",
    "segmentation_branching": "Segment length",
    "baseline_frequency_rank": "Frequency-rank baseline", "knight2006_em": "Knight-style EM (revised rule)",
    "knight2006_em_original": "Knight-style EM (original rule)", "em_cognate_matcher": "EM cognate-matcher",
}
COLOR = {n: SERIES[i % len(SERIES)] for i, n in enumerate(A_NAMES)}
COLOR.update({n: SERIES[i] for i, n in enumerate(B_NAMES)})
COLOR.update({n: SERIES[i] for i, n in enumerate(D_NAMES)})


def _style(ax, xlabel: str, ylabel: str, title: str):
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=8)
    ax.set_xlabel(xlabel, fontsize=9, color=INK2)
    ax.set_ylabel(ylabel, fontsize=9, color=INK2)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8)


def _series(points: list[dict], sweep: str, getter) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    xs, ys, lo, hi = [], [], [], []
    for p in points:
        v = getter(p["tables"])
        if v is None:
            continue
        xs.append(p["n_texts"] if sweep == "size" else p["mean_length"])
        ys.append(v[0])
        lo.append(v[1])
        hi.append(v[2])
    o = np.argsort(xs)
    return np.array(xs)[o], np.array(ys)[o], np.array(lo)[o], np.array(hi)[o]


def _get(path: list[str], rate_key: str = "rate"):
    def g(t):
        cur: Any = t
        for k in path:
            if not isinstance(cur, dict) or k not in cur:
                return None
            cur = cur[k]
        if rate_key == "balanced":
            return (cur["balanced_acc"], np.nan, np.nan)
        if rate_key == "token":
            return (cur["mean_token_acc"], cur["ci_lo"], cur["ci_hi"])
        if rate_key == "success50":
            c = cur["success50"]
            return (c["rate"], c["ci_lo"], c["ci_hi"])
        return (cur["rate"], cur["ci_lo"], cur["ci_hi"])
    return g


def _get_balanced(n):
    """Balanced accuracy; interval = mean of the per-class Wilson bounds (approximate)."""
    def g(t):
        a = t.get("A", {}).get(n)
        if a is None:
            return None
        r, s = a["ling_recall"], a["nonling_specificity"]
        return (a["balanced_acc"], 0.5 * (r["ci_lo"] + s["ci_lo"]), 0.5 * (r["ci_hi"] + s["ci_hi"]))
    return g


SIZE_TICKS = [500, 1000, 2000, 5000, 10000, 20000, 50000]


def _size_axis(ax):
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(SIZE_TICKS))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v >= 1000 else f"{v:g}"))


def _indus_label(ax, x):
    ax.text(x, 0.985, " Indus (M77)", transform=ax.get_xaxis_transform(), fontsize=7.5, color=INK2,
            va="top", ha="left", bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.85), zorder=4)


def _indus(ax, sweep: str, ip: dict, band: tuple[float, float]):
    if sweep == "size":
        ax.axvspan(band[0], band[1], color=BAND, alpha=0.6, lw=0, zorder=0)
        ax.axvline(ip["n_texts"], color=INK2, lw=1, ls="--", zorder=1)
        _indus_label(ax, ip["n_texts"])
        _size_axis(ax)
    else:
        ax.axvline(ip["mean_length"], color=INK2, lw=1, ls="--", zorder=1)
        _indus_label(ax, ip["mean_length"])


def _panel(ax, points, sweep, names, getter_fn, title, ylabel, chance=None, ip=None, band=None):
    for n in names:
        xs, ys, lo, hi = _series(points, sweep, getter_fn(n))
        if len(xs) == 0:
            continue
        ax.plot(xs, ys, color=COLOR[n], lw=2, marker="o", ms=4.5, label=LABEL[n], zorder=3)
        if np.isfinite(lo).all():
            ax.fill_between(xs, lo, hi, color=COLOR[n], alpha=0.10, lw=0, zorder=2)
    if chance is not None:
        ax.axhline(chance, color=INK2, lw=1, ls=":", zorder=1)
        ax.text(0.01, chance, " chance", transform=ax.get_yaxis_transform(),
                fontsize=7.5, color=INK2, va="bottom")
    ax.set_ylim(-0.02, 1.05)
    _indus(ax, sweep, ip, band)
    _style(ax, "texts in corpus (log scale)" if sweep == "size" else "mean signs per text", ylabel, title)
    # Colours repeat across panels (fixed categorical order per panel), so each panel has its own legend.
    ax.legend(frameon=False, fontsize=7.5, loc="best" if not title.startswith("D") else "upper left")


def decipherability(agg: dict, profile: dict, out_dir: Path | None = None) -> list[Path]:
    out_dir = ensure(out_dir or reports_dir() / "figures")
    ip = profile["indus_point"]
    band = (1548, 5500)
    pts = list(agg["points"].values())
    size_pts = [p for p in pts if p["sweep"] == "size" and p["regime"] == "full"]
    indus_pt = [p for p in size_pts if p["n_texts"] == ip["n_texts"]]
    len_pts = [p for p in pts if p["sweep"] == "length" and p["regime"] == "full"] + indus_pt
    paths = []
    for sweep, points in (("size", size_pts), ("length", len_pts)):
        fig, axes = plt.subplots(2, 3, figsize=(15, 8.6), dpi=150)
        _panel(axes[0, 0], points, sweep, A_NAMES, _get_balanced,
               "A  Language vs non-language (UNRESOLVED)", "balanced accuracy", 0.5, ip, band)
        _panel(axes[0, 1], points, sweep, B_NAMES, lambda n: _get(["B", n]), "B  Script type", "accuracy", 0.25, ip, band)
        _panel(axes[0, 2], points, sweep, D_NAMES, lambda n: _get(["C", "candidates", n]),
               "C  Language family (candidates tier)", "accuracy", _chance(points, "candidates"), ip, band)
        for ax, tier, ttl in zip(axes[1], ("related", "candidates", "none"),
                                 ("D  Sign values, close relative known\n(UPPER BOUND; not the Indus situation)",
                                  "D  Sign values, candidate languages\n(Indus-relevant)",
                                  "D  Sign values, no relative among candidates\n(Indus-relevant)")):
            _panel(ax, points, sweep, D_NAMES, lambda n, tier=tier: _get(["D", tier, n], "token"), ttl,
                   "share of sign tokens read correctly", None, ip, band)
        what = (f"corpus size (mean length {ip['mean_length']} signs)" if sweep == "size"
                else f"mean text length ({ip['n_texts']:,} texts)")
        fig.suptitle(f"Decipherability vs {what}. Shaded: 95% CI. Dashed line: Mahadevan (1977) corpus, {ip['n_texts']:,} texts. "
                     "Gray band: 1,548 (EBUDS) to ~5,500 texts.",
                     x=0.01, ha="left", fontsize=11, color=INK)
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        for ext in ("png", "svg"):
            p = out_dir / f"decipherability_{sweep}.{ext}"
            fig.savefig(p, facecolor="white")
            paths.append(p)
        plt.close(fig)
    return paths


def _chance(points, tier):
    for p in points:
        c = p["tables"].get("C", {}).get(tier, {})
        for v in c.values():
            return v.get("chance")
    return None


def headline(agg: dict, profile: dict, out_dir: Path | None = None, tier: str = "candidates") -> Path:
    """README figure: Task D in an Indus-relevant tier, one line per method (no best-of selection).

    Left: vs corpus size at Indus mean length. Middle: vs mean text length at Indus corpus size.
    Right: vs total sign tokens, both sweeps overlaid, so "more text" can be separated from
    "longer texts".
    """
    out_dir = ensure(out_dir or reports_dir() / "figures")
    ip = profile["indus_point"]
    pts = list(agg["points"].values())
    size_pts = sorted([p for p in pts if p["sweep"] == "size" and p["regime"] == "full"], key=lambda p: p["n_texts"])
    indus = [p for p in size_pts if p["n_texts"] == ip["n_texts"]]
    len_pts = sorted([p for p in pts if p["sweep"] == "length" and p["regime"] == "full"] + indus, key=lambda p: p["mean_length"])
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.9), dpi=150)
    for n in D_NAMES:
        for ax, points, xkey in ((axes[0], size_pts, "n_texts"), (axes[1], len_pts, "mean_length")):
            got = [(p[xkey], p["tables"]["D"].get(tier, {}).get(n)) for p in points]
            got = [(x, d) for x, d in got if d]
            if not got:
                continue
            xs = np.array([x for x, _ in got], float)
            ax.plot(xs, [d["mean_token_acc"] for _, d in got], color=COLOR[n], lw=2, marker="o", ms=4.5, label=LABEL[n], zorder=3)
            ax.fill_between(xs, [d["ci_lo"] for _, d in got], [d["ci_hi"] for _, d in got], color=COLOR[n], alpha=0.10, lw=0)
        for points, ls, mk in ((size_pts, "-", "o"), (len_pts, "--", "s")):
            got = [(p["n_texts"] * p["mean_length"], p["tables"]["D"].get(tier, {}).get(n)) for p in points]
            got = sorted([(x, d) for x, d in got if d], key=lambda v: v[0])
            if got:
                axes[2].plot([x for x, _ in got], [d["mean_token_acc"] for _, d in got], color=COLOR[n], lw=2, ls=ls,
                             marker=mk, ms=4.5, zorder=3)
    his = [d["ci_hi"] for p in size_pts + len_pts for d in p["tables"]["D"].get(tier, {}).values()
           if np.isfinite(d.get("ci_hi", np.nan))]
    top = min(1.02, max([0.6] + his) + 0.05)
    for ax in axes:
        ax.set_ylim(-0.01, top)
    axes[0].axvspan(1548, 5500, color=BAND, alpha=0.6, lw=0, zorder=0)
    axes[0].axvline(ip["n_texts"], color=INK2, lw=1, ls="--")
    _indus_label(axes[0], ip["n_texts"])
    _size_axis(axes[0])
    axes[1].axvline(ip["mean_length"], color=INK2, lw=1, ls="--")
    _indus_label(axes[1], ip["mean_length"])
    axes[2].set_xscale("log")
    _style(axes[0], "texts in corpus (log; mean %s signs/text)" % ip["mean_length"], "share of sign tokens read correctly",
           "More texts of Indus length")
    _style(axes[1], "mean signs per text (%s texts)" % f"{ip['n_texts']:,}", "", "Longer texts, same number")
    _style(axes[2], "total sign tokens in corpus (log)", "", "Same tokens: longer texts win?")
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    from matplotlib.lines import Line2D
    axes[2].legend([Line2D([], [], color=INK2, lw=2, ls="-", marker="o"), Line2D([], [], color=INK2, lw=2, ls="--", marker="s")],
                   ["size sweep (4.6 signs/text)", "length sweep (2,906 texts)"], frameon=False, fontsize=7.5, loc="upper left")
    fig.suptitle(f"Task D, `{tier}` knowledge tier (a relative is among the candidate languages; script type given). "
                 "One line per method; 95% cluster-bootstrap CI.", x=0.01, ha="left", fontsize=10.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    p = out_dir / "decipherability_headline.png"
    fig.savefig(p, facecolor="white")
    fig.savefig(out_dir / "decipherability_headline.svg", facecolor="white")
    plt.close(fig)
    return p


def entropy_bias(records: list[dict], out_dir: Path | None = None, ip_n: int = 2906) -> Path | None:
    """Plug-in H(X2|X1)/H(X1): i.i.d. control (true value 1) vs synthetic languages, by corpus size."""
    out_dir = ensure(out_dir or reports_dir() / "figures")
    from collections import defaultdict
    series = {"i.i.d. control (Rao type 2), full sign set": defaultdict(list),
              "i.i.d. control, Rao top-100 merge": defaultdict(list),
              "synthetic languages, full sign set": defaultdict(list),
              "synthetic languages, Rao top-100 merge": defaultdict(list)}
    keys = list(series)
    for r in records:
        if "error" in r or r["job"]["sweep"] != "size" or r["job"]["regime"] != "full" or not r.get("B"):
            continue
        n = r["job"]["n_texts"]
        full = r["B"]["script_type_lr"]["features"]["cond_ratio_full"]
        top = r["A"]["rao2009_entropy"]["features"]["rao_ratio"]
        if r["truth"]["source"] == "rao_type2":
            series[keys[0]][n].append(full)
            series[keys[1]][n].append(top)
        elif r["truth"]["kind"] == "language":
            series[keys[2]][n].append(full)
            series[keys[3]][n].append(top)
    if not series[keys[0]]:
        return None
    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
    styles = [(SERIES[1], "-"), (SERIES[1], "--"), (SERIES[0], "-"), (SERIES[0], "--")]
    for (lab, d), (c, ls) in zip(series.items(), styles):
        xs = sorted(d)
        m = [np.mean(d[x]) for x in xs]
        lo = [np.percentile(d[x], 10) for x in xs]
        hi = [np.percentile(d[x], 90) for x in xs]
        ax.plot(xs, m, color=c, lw=2, ls=ls, marker="o", ms=4.5, label=lab)
        if "languages" in lab:
            ax.fill_between(xs, lo, hi, color=c, alpha=0.10, lw=0)
    ax.axhline(1.0, color=INK2, lw=1, ls=":")
    ax.text(0.01, 1.0, " true value for the i.i.d. control", transform=ax.get_yaxis_transform(), fontsize=7.5,
            color=INK2, va="bottom")
    ax.axvline(ip_n, color=INK2, lw=1, ls="--")
    _indus_label(ax, ip_n)
    _size_axis(ax)
    ax.set_ylim(0, 1.08)
    _style(ax, "texts in corpus (log; mean 4.6 signs/text)", "plug-in H(X2|X1) / H(X1)",
           "Entropy ratio: random signs vs synthetic languages (band: 10th-90th percentile of languages)")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.tight_layout()
    p = out_dir / "entropy_bias.png"
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    return p


def control_fp(agg: dict, profile: dict, out_dir: Path | None = None) -> Path:
    """Share of each corpus family called 'linguistic' at the Indus point (Sproat's concern)."""
    out_dir = ensure(out_dir or reports_dir() / "figures")
    ip = profile["indus_point"]
    pt = next(p for p in agg["points"].values() if p["sweep"] == "size" and p["regime"] == "full" and p["n_texts"] == ip["n_texts"])
    kinds = ["language", "heraldry", "admin_tags", "emblem_markov", "adversarial", "rao_type1", "rao_type2", "kamon"]
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    width = 0.8 / len(A_NAMES)
    for i, n in enumerate(A_NAMES):
        d = pt["tables"]["A_by_kind"].get(n, {})
        ys = [d.get(k, {}).get("rate", np.nan) for k in kinds]
        xs = np.arange(len(kinds)) + (i - (len(A_NAMES) - 1) / 2) * width
        ax.bar(xs, ys, width=width * 0.92, color=COLOR[n], label=LABEL[n], zorder=3)
    ax.set_xticks(np.arange(len(kinds)))
    ax.set_xticklabels(["languages\n(want 1)", "heraldry", "admin tags", "Markov\nemblems", "adversarial\n(entropy-matched)",
                        "Rao type 1", "Rao type 2", "kamon text\n(NL-derived)"], fontsize=8)
    ax.set_ylim(0, 1.05)
    _style(ax, "", "share classified as 'linguistic'",
           "Language detection (Task A) is UNRESOLVED: false-positive rate per control family at the Indus point")
    ax.legend(frameon=False, fontsize=8, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.18))
    fig.tight_layout()
    p = out_dir / "taskA_by_family.png"
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    return p


def save_json(obj: Any, path: Path) -> None:
    path.write_text(json.dumps(obj, indent=1, default=float))


def sister_sweep(agg: dict, out_dir: Path | None = None) -> Path | None:
    """Task D token accuracy vs sister-language distance (reviewer fix 1)."""
    out_dir = ensure(out_dir or reports_dir() / "figures")
    levels = sorted(agg.get("sister", {}).values(), key=lambda v: v["sound_change_rate"])
    if not levels:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), dpi=150)
    xs = np.arange(len(levels))
    labels = [f"{v['sound_change_rate']:.2f} / {v['lexical_replacement']:.2f}" for v in levels]
    for ax, tier, ttl in zip(axes, ("related", "candidates"),
                             ("Close relative known (upper bound)", "Relative among candidates (Indus-relevant)")):
        for n in D_NAMES:
            ys = [v["tables"]["D"].get(tier, {}).get(n, {}).get("mean_token_acc", np.nan) for v in levels]
            lo = [v["tables"]["D"].get(tier, {}).get(n, {}).get("ci_lo", np.nan) for v in levels]
            hi = [v["tables"]["D"].get(tier, {}).get(n, {}).get("ci_hi", np.nan) for v in levels]
            ax.plot(xs, ys, color=COLOR[n], lw=2, marker="o", ms=5, label=LABEL[n])
            ax.fill_between(xs, lo, hi, color=COLOR[n], alpha=0.10, lw=0)
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_ylim(-0.02, 1.05)
        _style(ax, "sister distance: sound-change rate / lexical replacement", "share of sign tokens read correctly", ttl)
        ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    fig.suptitle("Task D at the Indus point depends on how close the known relative is "
                 "(95% cluster-bootstrap CI over source languages)", x=0.01, ha="left", fontsize=10.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    p = out_dir / "taskD_sister_distance.png"
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    return p


# --------------------------------------------------------------------------- sensitivity map

def _ref_points() -> dict:
    from . import config
    return config.targets().get("reference_points", {})


REF_ABBR = {"Parpola 1994": "P94", "Mahadevan 1977": "M77", "Wells 2006": "W06", "Wells 2015": "W15",
            "Fuls 2023 (>700, unverified)": "F23?", "M77 raw (Yadav 2010 Fig. 2)": "M77",
            "M77 without 4 outlier texts": "M77-4", "ICIT (Nair 2026, preprint)": "ICIT?"}


def _grouped_ticks(items: list[dict], min_gap: float) -> tuple[list[float], list[str]]:
    """Merge reference values closer than min_gap into one tick so labels never overlap."""
    groups: list[list[dict]] = []
    for r in sorted(items, key=lambda r: r["value"]):
        if groups and r["value"] - groups[-1][-1]["value"] < min_gap:
            groups[-1].append(r)
        else:
            groups.append([r])
    pos = [float(np.mean([r["value"] for r in g])) for g in groups]
    lab = [",".join(REF_ABBR.get(r["label"], r["label"]) for r in g) for g in groups]
    return pos, lab


def _ref_lines(ax, refs: dict, label: bool):
    """Published duplicate rates (horizontal) and sign-list sizes (vertical); solid = verified,
    dotted = unverified. Labels go on secondary axes, never inside the data area."""
    for r in refs.get("duplicate_text_fraction", []):
        ax.axhline(r["value"], color=INK, lw=0.7, ls="-" if r.get("verified") is True else ":", alpha=0.7, zorder=2)
    for r in refs.get("sign_inventory", []):
        ax.axvline(r["value"], color=INK, lw=0.7, ls=":" if r.get("verified") is False else "-", alpha=0.7, zorder=2)
    if not label:
        return
    xp, xl = _grouped_ticks(refs.get("sign_inventory", []), 45)
    top = ax.secondary_xaxis("top")
    top.set_xticks(xp, xl, fontsize=6, color=INK2)
    top.tick_params(length=2, pad=1)
    yp, yl = _grouped_ticks(refs.get("duplicate_text_fraction", []), 0.03)
    right = ax.secondary_yaxis("right")
    right.set_yticks(yp, yl, fontsize=6, color=INK2)
    right.tick_params(length=2, pad=1)


ALLOGRAPH_NOTE = ("LIMITATION: inventory is raised only by adding allographs (graphic variants of one value), and no "
                  "tested method merges allographs. High-inventory cells therefore measure these solvers' failure to "
                  "merge variants, not decipherability in general.")
SUBSET_COLOR = {"S": "#1baf7a", "T": "#eb6834", "P": "#4a3aa7"}
PREDICTION = "prediction, not measurement"
SUBSET_NOTE = ("Hatched regions S, T, P: PREDICTION, NOT MEASUREMENT. Predicted positions of archaeological subsets, "
               "all estimates (config/indus_targets.yaml): "
               "S seals only, duplicates 0-0.05 (seals 'almost all unique', Kenoyer & Meadow 2010); "
               "T tablets only, duplicates >= 0.354 (derived lower bound; copies and same-mold duplicates, ibid.); "
               "P single period, inventory below 400-450 ('considerably less', Kenoyer 2020b), off the measured grid. "
               "Subsets also have fewer than 2,906 texts; the map holds N fixed.")


def _subset_overlay(ax, refs: dict, letters: bool = True):
    """Hatched regions for the archaeological subsets. Drawn above the heatmap, below the numbers."""
    xl, yl = ax.get_xlim(), ax.get_ylim()
    for s in refs.get("archaeological_subsets", []):
        dr, ir = s.get("dup_range"), s.get("inventory_range")
        y0, y1 = (dr if dr else yl)
        x0, x1 = ((ir[0] if ir[0] is not None else xl[0], ir[1]) if ir else xl)
        y0, y1 = max(y0, yl[0]), min(y1 if s["letter"] != "T" else yl[1], yl[1])
        x0, x1 = max(x0, xl[0]), min(x1, xl[1])
        if y1 <= y0 or x1 <= x0:
            continue   # region lies outside this panel
        col = SUBSET_COLOR.get(s["letter"], INK)
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, hatch="////", edgecolor=col,
                                   lw=0.8, alpha=0.55, zorder=2.5))
        if letters:
            # Every region carries its full label, horizontally, in a gap between rows of cell numbers
            # (rows sit at multiples of 0.1): S on its top edge, T just above its bottom edge, P in the
            # gap above the lowest row, with an arrow-like "<-" pointing at its strip on the left.
            name = {"S": "seals only", "T": "tablets only", "P": "single period"}.get(s["letter"], "")
            txt = f'{"<- " if s["letter"] == "P" else ""}{s["letter"]} {name}: {PREDICTION}'
            kw = dict(fontsize=5.5, fontweight="bold", color=col, zorder=4,
                      bbox=dict(boxstyle="round,pad=0.12", fc="white", ec=col, lw=0.5, alpha=0.9))
            span = yl[1] - yl[0]
            ty = {"S": y1, "T": y0 + 0.023 * span / 0.6, "P": yl[0] + span / 3}[s["letter"]]
            if yl[0] < ty < yl[1]:
                ax.text(0.5 * (xl[0] + xl[1]), ty, txt, ha="center", va="center", **kw)
    ax.set_xlim(xl)
    ax.set_ylim(yl)


def sensitivity_maps(agg: dict, out_dir: Path | None = None) -> list[Path]:
    d = ensure(out_dir or reports_dir() / "sensitivity")
    refs = _ref_points()
    paths = []
    for panel in ("balanced", "box", "all"):
        cells = {(c["dup"], c["inventory"]): c for c in agg["panels"][panel]}
        dups = sorted({d for d, _ in cells})
        invs = sorted({i for _, i in cells})
        dx = (invs[1] - invs[0]) / 2 if len(invs) > 1 else 50
        dy = (dups[1] - dups[0]) / 2 if len(dups) > 1 else 0.05
        extent = (invs[0] - dx, invs[-1] + dx, dups[0] - dy, dups[-1] + dy)
        tiers, methods = agg["tiers"], agg["methods"]
        vmax = max([c[f"{t}:{m}"]["mean"] for c in cells.values() if c["n"] for t in tiers for m in methods] + [0.05])
        fig, axes = plt.subplots(len(tiers), len(methods), figsize=(3.3 * len(methods), 3.0 * len(tiers) + 0.6),
                                 sharex=True, sharey=True, squeeze=False)
        for i, t in enumerate(tiers):
            for j, m in enumerate(methods):
                ax = axes[i][j]
                z = np.full((len(dups), len(invs)), np.nan)
                for a, dv in enumerate(dups):
                    for b, iv in enumerate(invs):
                        c = cells.get((float(dv), int(iv)))
                        if c and c["n"]:
                            z[a, b] = c[f"{t}:{m}"]["mean"]
                im = ax.imshow(z, origin="lower", extent=extent, aspect="auto", cmap="Blues", vmin=0, vmax=vmax,
                               interpolation="nearest")
                for a, dv in enumerate(dups):
                    for b, iv in enumerate(invs):
                        if not np.isnan(z[a, b]):
                            ax.text(iv, dv, f"{100 * z[a, b]:.1f}", ha="center", va="center", fontsize=7,
                                    color=INK, zorder=3,
                                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
                _ref_lines(ax, refs, label=True)
                _subset_overlay(ax, refs)
                ax.set_title(f"{LABEL[m]}\n{'candidates' if t == 'candidates' else 'no relative'} tier",
                             loc="left", fontsize=8.5, color=INK, pad=14)
                if i == len(tiers) - 1:
                    ax.set_xlabel("sign inventory (types observed)", fontsize=8, color=INK2)
                if j == 0:
                    ax.set_ylabel("duplicate-text fraction", fontsize=8, color=INK2)
                ax.tick_params(labelsize=7)
        fig.subplots_adjust(hspace=0.5, wspace=0.35)
        fig.colorbar(im, ax=axes, shrink=0.6, label="Task D token accuracy (cell mean)")
        n_combo = {"balanced": len(agg["balanced_combos"]), "box": len(agg["box_combos"])}.get(panel, len(agg["combos"]))
        fig.suptitle(f"Decipherability map at the Indus point (2,906 texts x 4.6 signs), methods frozen. "
                     f"Numbers: % tokens. Panel: {panel} ({n_combo} language x script combinations). "
                     f"Lines: published values (solid verified, dotted unverified).\n"
                     f"Top: sign lists P94 Parpola 386, M77 Mahadevan 417, W06/W15 Wells 676/694, F23? Fuls >700. "
                     f"Right: duplicate rate, M77 raw 0.354, M77-4 without 4 outlier texts 0.281, "
                     f"ICIT? preprint 0.237. Empty cell: unreachable.\n{_score_label(agg)}", fontsize=8.5, x=0.01,
                     ha="left", y=1.05)
        fig.text(0.01, -0.02, ALLOGRAPH_NOTE, fontsize=8.5, color="#a3271f", ha="left", va="top", wrap=True)
        fig.text(0.01, -0.075, SUBSET_NOTE, fontsize=8, color=INK2, ha="left", va="top", wrap=True)
        p = d / f"sensitivity_map_{panel}.png"
        fig.savefig(p, dpi=150, bbox_inches="tight")
        fig.savefig(p.with_suffix(".svg"), bbox_inches="tight")
        plt.close(fig)
        paths.append(p)
    # Slices with clustered CIs (balanced panel): accuracy vs duplicates, one line per inventory level.
    dups, invs = agg["dup_grid"], agg["inventory_grid"]
    cells = {(c["dup"], c["inventory"]): c for c in agg["panels"]["balanced"]}
    fig, axes = plt.subplots(len(agg["tiers"]), 2, figsize=(10, 3.3 * len(agg["tiers"])), squeeze=False)
    m = "knight2006_em"
    cmap = plt.get_cmap("viridis")
    for i, t in enumerate(agg["tiers"]):
        for k, (xs, other, xlabel) in enumerate(((dups, invs, "duplicate-text fraction"),
                                                 (invs, dups, "sign inventory"))):
            ax = axes[i][k]
            for q, ov in enumerate(other):
                pts = [(x, cells.get((float(x), int(ov)) if k == 0 else (float(ov), int(x)))) for x in xs]
                pts = [(x, c[f"{t}:{m}"]) for x, c in pts if c and c["n"]]
                if not pts:
                    continue
                xv = np.array([p[0] for p in pts], float) + (q - len(other) / 2) * (0.004 if k == 0 else 4)
                mv = np.array([p[1]["mean"] for p in pts])
                lo = np.array([p[1]["ci_lo"] for p in pts])
                hi = np.array([p[1]["ci_hi"] for p in pts])
                ax.errorbar(xv, mv, yerr=[mv - lo, hi - mv], marker="o", ms=3, lw=1, capsize=2,
                            color=cmap(q / max(len(other) - 1, 1)),
                            label=(f"inventory {ov}" if k == 0 else f"duplicates {ov:.1f}"))
            _style(ax, xlabel, "token accuracy",
                   f"{LABEL[m]}, {t} tier (95% cluster CI), strict panel ({len(agg['balanced_combos'])} combos)")
            if ax.get_legend_handles_labels()[0]:
                ax.legend(fontsize=6.5, frameon=False, ncol=2)
            for r in refs.get("duplicate_text_fraction" if k == 0 else "sign_inventory", []):
                ax.axvline(r["value"], color=INK, lw=0.7, ls=":" if r.get("verified") is False else "-", alpha=0.5)
    fig.tight_layout()
    fig.text(0.01, -0.01, ALLOGRAPH_NOTE, fontsize=8, color="#a3271f", ha="left", va="top", wrap=True)
    fig.text(0.01, -0.07, _score_label(agg), fontsize=8, color=INK2, ha="left", va="top")
    p = d / "sensitivity_slices.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    fig.savefig(p.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)
    paths.append(p)
    paths.append(archaeology_map(agg, refs, d))
    return paths


def _score_label(agg: dict) -> str:
    from .sensitivity import score_label
    return score_label(agg)


def archaeology_map(agg: dict, refs: dict, d: Path) -> Path:
    """Revised EM on the 'all' panel, with the archaeological subsets labelled in full. The x-axis
    extends below the grid to show where the single-period region lies (not measured)."""
    cells = {(c["dup"], c["inventory"]): c for c in agg["panels"]["all"]}
    dups, invs = agg["dup_grid"], agg["inventory_grid"]
    dx, dy = (invs[1] - invs[0]) / 2, (dups[1] - dups[0]) / 2
    m = "knight2006_em"
    vmax = max(c[f"{t}:{m}"]["mean"] for c in cells.values() if c["n"] for t in agg["tiers"])
    fig, axes = plt.subplots(1, len(agg["tiers"]), figsize=(7.2 * len(agg["tiers"]), 5.4), squeeze=False)
    for j, t in enumerate(agg["tiers"]):
        ax = axes[0][j]
        z = np.full((len(dups), len(invs)), np.nan)
        for a, dv in enumerate(dups):
            for b, iv in enumerate(invs):
                c = cells.get((float(dv), int(iv)))
                if c and c["n"]:
                    z[a, b] = c[f"{t}:{m}"]["mean"]
        im = ax.imshow(z, origin="lower", extent=(invs[0] - dx, invs[-1] + dx, dups[0] - dy, dups[-1] + dy),
                       aspect="auto", cmap="Blues", vmin=0, vmax=vmax, interpolation="nearest")
        for a, dv in enumerate(dups):
            for b, iv in enumerate(invs):
                if not np.isnan(z[a, b]):
                    ax.text(iv, dv, f"{100 * z[a, b]:.1f}", ha="center", va="center", fontsize=8, color=INK, zorder=3,
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
        ax.set_xlim(invs[0] - dx - 150, invs[-1] + dx)   # room for the unmeasured single-period region
        ax.set_ylim(dups[0] - dy, dups[-1] + dy)
        ax.axvspan(invs[0] - dx - 150, invs[0] - dx, color=GRID, alpha=0.6, zorder=1)
        ax.text(invs[0] - dx - 75, dups[0] - dy + 0.02, "not measured\n(< 350 types)", ha="center", va="bottom",
                fontsize=7.5, color=INK2, zorder=4)
        _ref_lines(ax, refs, label=True)
        _subset_overlay(ax, refs, letters=False)
        for s in refs.get("archaeological_subsets", []):
            col = SUBSET_COLOR.get(s["letter"], INK)
            if s["letter"] == "P":
                ax.text(invs[0] - dx - 75, 0.25, "P: single\nperiod\n< 400-450\nprediction,\nnot\nmeasurement", ha="center",
                        va="center", fontsize=7, color=col, fontweight="bold", zorder=5,
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=col, lw=0.7))
            else:
                ymid = 0.5 * (s["dup_range"][0] + min(s["dup_range"][1], dups[-1] + dy))
                short = {"S": "S: seals only\nprediction,\nnot measurement",
                         "T": "T: tablets only\nprediction,\nnot measurement"}[s["letter"]]
                ax.annotate(short, xy=(1.0, ymid), xycoords=("axes fraction", "data"),
                            xytext=(1.03, ymid), textcoords=("axes fraction", "data"), ha="left", va="center",
                            fontsize=7, color=col, fontweight="bold",
                            arrowprops=dict(arrowstyle="-", color=col, lw=0.8))
        ax.set_title(f"{LABEL[m]}\n{'candidates' if t == 'candidates' else 'no relative'} tier, all corpora (% tokens)",
                     loc="left", fontsize=10, color=INK, pad=16)
        ax.set_xlabel("sign inventory (types observed)", fontsize=9, color=INK2)
        ax.set_ylabel("duplicate-text fraction", fontsize=9, color=INK2)
    fig.subplots_adjust(wspace=0.5)
    fig.colorbar(im, ax=axes, shrink=0.7, pad=0.16, label="Task D token accuracy")
    fig.text(0.01, -0.02, ALLOGRAPH_NOTE, fontsize=8.5, color="#a3271f", ha="left", va="top", wrap=True)
    fig.text(0.01, -0.09, SUBSET_NOTE, fontsize=8, color=INK2, ha="left", va="top", wrap=True)
    fig.text(0.01, -0.15, _score_label(agg), fontsize=8, color=INK2, ha="left", va="top")
    p = d / "sensitivity_archaeology.png"
    fig.savefig(p, dpi=150, bbox_inches="tight")
    fig.savefig(p.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)
    return p
