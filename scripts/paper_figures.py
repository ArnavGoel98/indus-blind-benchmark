"""The three figures embedded in the paper (from saved records and aggregates; analysis only).
fig3_sensitivity_map.png  primary sensitivity map, sampler A, plausible box and published reference points
fig2_length_vs_size.png   longer vs more inscriptions at equal tokens, both samplers, primary, 95% intervals
fig1_entropy_ratio.png    entropy ratio at the Indus point, synthetic languages vs i.i.d. control
Usage: python scripts/paper_figures.py
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from ibdb import sensitivity as S  # noqa: E402
from sister_compare import ci, load, point_keys, vals  # noqa: E402

OUT = Path("reports/drafts/figures")
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#d9d8d4", "#fcfcfb"
BLUE, ORANGE = "#2a78d6", "#eb6834"
SEQ = LinearSegmentedColormap.from_list("blue", ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"])
O = "knight2006_em_original"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "axes.facecolor": "white"})


def fig1():
    agg = S.aggregate("sensitivity_sister_v2", before_cognate=True)
    dups, invs = agg["dup_grid"], agg["inventory_grid"]
    cells = {(c["dup"], c["inventory"]): c for c in agg["panels"]["all"]}
    M = np.full((len(dups), len(invs)), np.nan)
    for i, d in enumerate(dups):
        for j, v in enumerate(invs):
            c = cells.get((d, v))
            if c and c["n"]:
                M[i, j] = 100 * c[f"candidates:{O}"]["mean"]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    im = ax.imshow(M, origin="lower", cmap=SEQ, vmin=0, vmax=np.nanmax(M), aspect="auto",
                   extent=(invs[0] - 50, invs[-1] + 50, dups[0] - 0.05, dups[-1] + 0.05))
    for i, d in enumerate(dups):
        for j, v in enumerate(invs):
            if not np.isnan(M[i, j]):
                ax.text(v, d, f"{M[i, j]:.1f}", ha="center", va="center", fontsize=8,
                        color="white" if M[i, j] > 0.6 * np.nanmax(M) else INK)
            else:
                ax.text(v, d, "n/a", ha="center", va="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle((350, 0.15), 400, 0.3, fill=False, lw=2, ec=ORANGE))
    ax.text(355, 0.455, "plausible box", color=ORANGE, fontsize=8, va="bottom", fontweight="bold")
    for x, lab, ls in ((386, "Parpola 386", ":"), (417, "Mahadevan 417", "-"), (676, "Wells 676", ":"), (694, "Wells 694", ":")):
        ax.axvline(x, color=INK2, lw=0.8, ls=ls)
        ax.text(x, dups[-1] + 0.06, lab, rotation=90, fontsize=6.5, color=INK2, ha="center", va="bottom")
    for y, lab, ls in ((0.354, "M77 0.354", "-"), (0.281, "M77 w/o 4 outliers 0.281", "-"), (0.237, "ICIT 0.237 (preprint)", ":")):
        ax.axhline(y, color=INK2, lw=0.8, ls=ls)
        ax.text(invs[-1] + 55, y, lab, fontsize=6.5, color=INK2, va="center")
    ax.set_xticks(invs); ax.set_yticks(dups)
    ax.set_xlabel("sign inventory (types observed; raised by allographs only)")
    ax.set_ylabel("duplicate-text rate")
    cb = fig.colorbar(im, ax=ax, pad=0.28, shrink=0.85)
    cb.set_label("% sign tokens recovered", color=INK)
    fig.savefig(OUT / "fig3_sensitivity_map.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    groups = (("Sampler A", "sister_v2_main", "sister_v2_eqtok_gen1"), ("Sampler B", "sister_v2_gen2", "sister_v2_eqtok_gen2"))
    w = 0.34
    for g, (lab, a, b) in enumerate(groups):
        r = {**load(a), **load(b)}
        L = ci(vals(r, point_keys(r, "length", 2906, 10.0), "candidates", O, True))
        Sz = ci(vals(r, point_keys(r, "size", 6317, 4.6), "candidates", O, True))
        for k, (c, col, name) in enumerate(((L, BLUE, "Longer: 2,906 texts x 10 signs"), (Sz, ORANGE, "More: 6,317 texts x 4.6 signs"))):
            x = g + (k - 0.5) * (w + 0.03)
            ax.bar(x, c[0], width=w, color=col, label=name if g == 0 else None, zorder=2)
            ax.errorbar(x, c[0], yerr=[[c[0] - c[1]], [c[2] - c[0]]], color=INK, lw=1, capsize=3, zorder=3)
            ax.text(x, c[2] + 1.2, f"{c[0]:.1f}", ha="center", fontsize=8, color=INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels([g[0] for g in groups])
    ax.set_ylabel("% sign tokens recovered"); ax.set_ylim(0, 55)
    ax.yaxis.grid(True, color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.savefig(OUT / "fig2_length_vs_size.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def fig3():
    rows = [json.loads(l) for l in open("runs/results/full/records.jsonl")]
    pt = [r for r in rows if "error" not in r and r["job"]["sweep"] == "size" and r["job"]["n_texts"] == 2906
          and r["job"]["regime"] == "full" and not r["job"]["pred_script"] and r.get("B")]
    lang = [r for r in pt if r["truth"]["kind"] == "language"]
    iid = [r for r in pt if r["truth"]["source"] == "rao_type2"]
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0), sharey=False)
    rng = np.random.default_rng(0)
    for ax, (title, get) in zip(axes, (("Full sign set", lambda r: r["B"]["script_type_lr"]["features"]["cond_ratio_full"]),
                                       ("Rao's merge to top 100 signs", lambda r: r["A"]["rao2009_entropy"]["features"]["rao_ratio"]))):
        for x, rs, col, name in ((0, lang, BLUE, f"synthetic languages (n={len(lang)})"), (1, iid, ORANGE, f"i.i.d. control (n={len(iid)})")):
            ys = np.array([get(r) for r in rs])
            ax.scatter(x + rng.uniform(-0.12, 0.12, len(ys)), ys, s=14, color=col, alpha=0.75, edgecolor=SURF, lw=0.5, zorder=3)
            ax.hlines(ys.mean(), x - 0.25, x + 0.25, color=INK, lw=2, zorder=4)
            ax.text(x + 0.28, ys.mean(), f"{ys.mean():.3f}", va="center", fontsize=8, color=INK)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["synthetic\nlanguages", "i.i.d.\ncontrol"])
        ax.set_xlim(-0.5, 1.7); ax.set_title(title, fontsize=9, color=INK)
        ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    axes[0].set_ylabel("H(X2|X1) / H(X1)")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_entropy_ratio.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    fig1(); fig2(); fig3()
    print("ok")
