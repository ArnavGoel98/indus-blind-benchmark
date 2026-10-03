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
