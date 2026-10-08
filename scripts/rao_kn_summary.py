"""Summarise reports/rao_kn/records.jsonl -> reports/rao_kn/indus_point.md (post hoc)."""
import json
from collections import defaultdict

import numpy as np

from ibdb.paths import reports_dir

D = reports_dir() / "rao_kn"
rows = [json.loads(l) for l in open(D / "records.jsonl")]
L = ["# Headline 1 with Rao et al.'s (2009) estimator (post hoc)", "",
     "Relative conditional entropy C / ln N, modified Kneser-Ney bigrams (`ibdb.rao_kn`). Indus point: 2,906 texts,",
     "mean 4.6 signs. All 324 regenerated corpora match their stored records. The plug-in conditional-to-unigram",
     "ratio (top-100 merge, the frozen method's score) is shown for comparison.", ""]
for stat, lab in (("rel_all", "all signs"), ("rel_417", "417 most frequent signs")):
    L += [f"## Relative conditional entropy, {lab}", "",
          "| Run / regime | Synthetic languages: mean (10th-90th pct; min-max) | i.i.d. random control (3) | Rigid control | Other built controls (min-max) | Languages below i.i.d. min | AUC lang vs i.i.d. |",
          "|---|---|---|---|---|---|---|"]
    for prof in ("full", "replication"):
        for reg in ("full", "holdout"):
            g = [r for r in rows if r["profile"] == prof and r["regime"] == reg]
            lang = np.array([r[stat] for r in g if r["kind"] == "language"])
            iid = np.array([r[stat] for r in g if r["source"] == "rao_type2"])
            rig = np.array([r[stat] for r in g if r["source"] == "rao_type1"])
            oth = np.array([r[stat] for r in g if r["kind"] != "language" and r["source"] not in ("rao_type1", "rao_type2", "kamon")])
            auc = float(np.mean([[1.0 if l < i else 0.5 if l == i else 0.0 for i in iid] for l in lang]))
            L.append(f"| {prof} / {reg} | {lang.mean():.3f} ({np.percentile(lang,10):.3f}-{np.percentile(lang,90):.3f}; {lang.min():.3f}-{lang.max():.3f}) | "
                     f"{iid.mean():.3f} ({iid.min():.3f}-{iid.max():.3f}) | {rig.mean():.3f} | {oth.min():.3f}-{oth.max():.3f} | "
                     f"{int((lang < iid.min()).sum())}/{len(lang)} | {auc:.2f} |")
    L.append("")
    sp = [r for r in rows if r["profile"] == "sproat"]
    by = defaultdict(list)
    for r in sp:
        by[(r["source"], "native" if r["regime"] == "native" else "2,906-text samples")].append(r[stat])
    L += ["Sproat's attested systems:", "", "| System | Size | Relative |", "|---|---|---|"]
    for (s, tag), v in by.items():
        L.append(f"| {s} | {tag} | {np.mean(v):.3f}" + (f" ({min(v):.3f}-{max(v):.3f})" if len(v) > 1 else "") + " |")
    L.append("")
g = [r for r in rows if r["profile"] == "full" and r["regime"] == "full"]
lang = [r["plugin_ratio_top100"] for r in g if r["kind"] == "language"]
iid = [r["plugin_ratio_top100"] for r in g if r["source"] == "rao_type2"]
L += [f"For comparison, plug-in ratio (top-100 merge), full/full: languages {np.mean(lang):.3f}, i.i.d. random control {np.mean(iid):.3f}.", ""]
(D / "indus_point.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
