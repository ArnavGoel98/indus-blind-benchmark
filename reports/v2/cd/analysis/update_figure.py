"""Figure for the one-page update (Arnav_Goel_Indus_Update_Real_Relatives.pdf): recovery by script type,
real relative against the synthetic relatives. Every value is copied from a v2 report (pooled over seeds 0-5,
revised EM, strict, `related` tier) and checked against that report's text before plotting.
Usage (repository root): python reports/v2/cd/analysis/update_figure.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
POOLED = (ROOT / "reports/v2/cd/pooled.md").read_text()
EST = (ROOT / "reports/v2/cd/estonian.md").read_text()
OUT = ROOT / "reports/drafts/figures/fig_update_real_relatives.png"
SCRIPTS = ["syllabic", "logo-syllabic", "alphabetic"]
# (hidden, label, kind, [syllabic, logo-syllabic, alphabetic], source)
ROWS = [("Latin", "Italian", "real", ["4.2 (1.8-6.9)", "2.3 (1.2-3.9)", "20.3 (9.6-32.6)"], POOLED),
        ("Latin", "harsh", "harsh", ["16.9 (9.3-25.4)", "3.6 (1.8-5.6)", "31.5 (24.0-38.9)"], POOLED),
        ("Latin", "v1", "v1", ["29.3 (16.2-43.1)", "9.7 (5.8-14.4)", "46.3 (37.6-55.3)"], POOLED),
        ("Old Tamil", "Malayalam", "real", ["10.7 (6.9-15.7)", "6.6 (3.9-9.7)", "30.5 (16.9-44.2)"], POOLED),
        ("Old Tamil", "Kannada", "real", ["4.0 (2.5-5.8)", "3.9 (2.0-6.2)", "34.4 (28.8-41.2)"], POOLED),
        ("Old Tamil", "harsh", "harsh", ["8.1 (4.3-12.4)", "6.3 (3.0-9.8)", "12.9 (7.0-19.2)"], POOLED),
        ("Old Tamil", "v1", "v1", ["29.3 (21.9-38.1)", "21.3 (11.1-32.3)", "43.5 (34.4-53.4)"], POOLED),
        ("Finnish", "Estonian", "real", ["8.1 [4.4, 12.3]", "3.6 [2.1, 5.1]", "31.1 [25.1, 36.3]"], EST),
        ("Finnish", "harsh", "harsh", ["23.0 (17.8-28.5)", "11.3 (7.6-15.9)", "41.2 (34.5-48.2)"], POOLED),
        ("Finnish", "v1", "v1", ["43.4 (33.8-53.4)", "18.6 (9.4-28.4)", "64.9 (58.8-69.9)"], POOLED)]
for *_, vals, src in ROWS:
    for v in vals:
        assert v in src, v                       # provenance: the exact string is in the report
STYLE = {"real": dict(marker="o", s=26, color="#1f6fb4", zorder=3), "harsh": dict(marker="^", s=24, color="#8c8c8c", zorder=2),
         "v1": dict(marker="s", s=18, color="#ffffff", edgecolors="#333333", linewidths=0.9, zorder=2)}
TAG = {"Italian": "I", "Malayalam": "M", "Kannada": "K", "Estonian": "E"}
LANGS = ["Latin", "Old Tamil", "Finnish"]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})
fig, axes = plt.subplots(3, 1, figsize=(2.75, 2.85), sharex=True)
for ax, (j, st) in zip(axes, enumerate(SCRIPTS)):
    for hidden, label, kind, vals, _ in ROWS:
        y = 2 - LANGS.index(hidden)
        x = float(vals[j].split()[0])
        ax.scatter([x], [y], **STYLE[kind])
        if kind == "real":
            dy = -0.52 if label in ("Kannada", "Estonian") else 0.5
            ax.annotate(TAG[label], (x, y + dy), ha="center", va="center", fontsize=5.3, color="#1f6fb4", fontweight="bold")
    ax.set_yticks([2, 1, 0], LANGS)
    ax.set_ylim(-0.8, 2.8)
    ax.set_xlim(0, 70)
    ax.axvline(50, color="#bbbbbb", lw=0.6, ls="--", zorder=0)
    ax.set_title(st, fontsize=7, loc="left", pad=1.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=2, pad=1.5)
axes[-1].set_xlabel("signs recovered (%), average of 12 collections", fontsize=6.2)
h = [plt.scatter([], [], **STYLE[k]) for k in ("real", "harsh", "v1")]
fig.legend(h, ["real relative", "harshest synthetic", "original synthetic"], loc="lower center", ncol=3,
           fontsize=5.6, frameon=False, handletextpad=0.15, columnspacing=0.6, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(h_pad=0.4, rect=(0, 0.06, 1, 1))
fig.savefig(OUT, dpi=300, bbox_inches="tight", pad_inches=0.02)
print(OUT)
