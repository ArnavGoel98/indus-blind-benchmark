"""Exploratory (post hoc, 2026-10-21): does unit-frequency agreement explain the bracket failure?

Negative result 3 offered, untested, that the real relatives' texts have different unit frequencies. This
measures, per pair and at the alphabetic level, the unigram distribution of the hidden half mapped forward
through the gold regular reflexes against the relative's text: Jensen-Shannon divergence (bits) and the
Spearman rank correlation over shared units. `harsh` uses seed 0. No statistic is tested.
Usage (repository root): python reports/v2/cd/analysis/freq_check.py -> reports/v2/cd/frequency_check.md
"""
import json
import os
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

os.environ["IBDB_SISTER_VERSION"] = "v2"
from ibdb import relative_cd as RC  # noqa: E402
from ibdb import sister_v4 as S  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "reports" / "v2" / "cd" / "frequency_check.md"
HARSH = json.loads((ROOT / "reports" / "v2" / "sister" / "harsh.json").read_text())["chosen"]
TASK_D = ROOT / "reports" / "v2" / "cd" / "results.json"


def unigram(texts):
    c = Counter(u for t in texts for u in t)
    n = sum(c.values())
    return {k: v / n for k, v in c.items()}


def jsd(p, q):
    ks = sorted(set(p) | set(q))
    P, Q = np.array([p.get(k, 0) for k in ks]), np.array([q.get(k, 0) for k in ks])
    M = (P + Q) / 2
    kl = lambda x: float(np.sum(x[x > 0] * np.log2(x[x > 0] / M[x > 0])))  # noqa: E731
    return 0.5 * (kl(P) + kl(Q))


def main():
    d = json.loads(TASK_D.read_text())["task_d"]["related"]["knight2006_em"]
    lab = {"italian": "italian", "malayalam": "malayalam", "kannada": "kannada", "harsh": "`harsh` (lower bound)"}
    L = ["# Unit-frequency agreement against Task D (exploratory, post hoc)", "",
         "Added 2026-10-21. Tests the first reason offered (untested) in `docs/v2_negative_results.md`, item 3. "
         "Alphabetic level: the hidden half mapped forward through the gold regular reflexes, against the relative's "
         "text (`harsh`: seed 0). Lower JSD and higher rank correlation mean closer unit frequencies. Task D: primary "
         "table (`results.md`), revised EM, related tier, alphabetic, seeds 0-2.", "",
         "| Hidden | Relative | Unigram JSD (bits) | Spearman rank correlation | Top 6 units, hidden mapped | Top 6 units, relative | Task D alphabetic |",
         "|---|---|---|---|---|---|---|"]
    for lang, rels in (("latin", ["italian"]), ("tamil", ["malayalam", "kannada"])):
        hidden = S.hidden_half(lang)[0]
        for name in rels + ["harsh"]:
            rel = RC.harsh_relative(lang, 0, HARSH[lang]["knobs"]) if name == "harsh" else RC.real_relative(lang, name)
            fwd = [[rel.regular.get(p, p) for w in c for p in w if rel.regular.get(p, p) is not None] for c in hidden]
            pu, qu = unigram(fwd), unigram([[p for w in c for p in w] for c in rel.clauses])
            ks = sorted(set(pu) & set(qu))
            rho = spearmanr([pu[k] for k in ks], [qu[k] for k in ks]).statistic
            top = lambda x: " ".join(k for k, _ in sorted(x.items(), key=lambda kv: -kv[1])[:6])  # noqa: E731
            td = 100 * d[lang][lab[name]]["alphabetic"]["mean"]       # results.json stores fractions
            L.append(f"| {lang} | {name} | {jsd(pu, qu):.3f} | {rho:.2f} | {top(pu)} | {top(qu)} | {td:.1f} |")
    L += ["", "**Reading.** Italian agrees with Latin in unit frequencies better than `harsh` does (lower JSD, higher rank "
          "correlation), yet scores lower on Task D. Unigram frequency agreement therefore does not explain the "
          "bracket failure for Latin. For Old Tamil the two measures disagree (Malayalam is closer by JSD, Kannada by "
          "rank order) while Task D is level for the two relatives. Three points per hidden language; nothing is "
          "tested."]
    OUT.write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
