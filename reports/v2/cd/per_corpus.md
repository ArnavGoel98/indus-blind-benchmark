# v2 Task D per corpus: real relatives and `harsh` (post-hoc, descriptive)

Added 2026-10-20 after the final run (`reports/v2/cd/results.md`); not pre-registered. Revised EM (primary), `related` tier, strict score, % of sign tokens, per corpus (sampler A or B, seed 0-2). Written because the means in `results.md` hide a wide spread between corpora. No statistic is tested.

### latin

| Script | Tier | A s0 | A s1 | A s2 | B s0 | B s1 | B s2 | min-max | real below `harsh` |
|---|---|---|---|---|---|---|---|---|---|
| logographic | italian | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0-0.0 | 2/6 |
| logographic | harsh | 0.0 | 0.0 | 0.0 | 0.0 | 4.8 | 4.2 | 0.0-4.8 |  |
| syllabic | italian | 4.2 | 0.7 | 4.0 | 14.6 | 0.2 | 12.2 | 0.2-14.6 | 4/6 |
| syllabic | harsh | 1.3 | 27.5 | 3.2 | 43.5 | 35.7 | 34.9 | 1.3-43.5 |  |
| logosyllabic | italian | 1.3 | 1.7 | 2.9 | 1.7 | 0.0 | 1.7 | 0.0-2.9 | 4/6 |
| logosyllabic | harsh | 11.5 | 7.9 | 0.8 | 3.6 | 1.8 | 1.6 | 0.8-11.5 |  |
| alphabetic | italian | 0.2 | 6.1 | 1.1 | 53.2 | 13.0 | 27.5 | 0.2-53.2 | 5/6 |
| alphabetic | harsh | 25.9 | 54.8 | 44.4 | 15.2 | 32.0 | 44.2 | 15.2-54.8 |  |

### tamil

| Script | Tier | A s0 | A s1 | A s2 | B s0 | B s1 | B s2 | min-max | real below `harsh` |
|---|---|---|---|---|---|---|---|---|---|
| logographic | malayalam | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0-0.0 | 1/6 |
| logographic | kannada | 0.0 | 0.0 | 0.0 | 0.1 | 0.0 | 0.1 | 0.0-0.1 | 1/6 |
| logographic | harsh | 0.0 | 0.0 | 0.0 | 0.0 | 0.3 | 0.0 | 0.0-0.3 |  |
| syllabic | malayalam | 3.4 | 8.7 | 4.3 | 4.6 | 5.4 | 10.8 | 3.4-10.8 | 2/6 |
| syllabic | kannada | 0.8 | 4.8 | 1.0 | 5.0 | 5.5 | 2.3 | 0.8-5.5 | 5/6 |
| syllabic | harsh | 2.4 | 0.8 | 1.3 | 8.7 | 18.0 | 5.9 | 0.8-18.0 |  |
| logosyllabic | malayalam | 2.0 | 1.6 | 2.6 | 3.9 | 18.3 | 7.1 | 1.6-18.3 | 2/6 |
| logosyllabic | kannada | 0.8 | 0.4 | 0.0 | 6.0 | 4.5 | 5.4 | 0.0-6.0 | 5/6 |
| logosyllabic | harsh | 4.9 | 4.3 | 1.9 | 0.6 | 18.1 | 5.7 | 0.6-18.1 |  |
| alphabetic | malayalam | 0.1 | 43.9 | 0.0 | 56.0 | 49.6 | 32.8 | 0.0-56.0 | 1/6 |
| alphabetic | kannada | 28.0 | 24.5 | 23.9 | 40.0 | 40.6 | 36.0 | 23.9-40.6 | 0/6 |
| alphabetic | harsh | 0.0 | 24.2 | 1.1 | 25.9 | 28.8 | 18.2 | 0.0-28.8 |  |

Generated from `runs/results/v2_cd/records.jsonl` by this code (kept here so the frozen scripts stay unchanged):

```python
import json
recs = [json.loads(l) for l in open("runs/results/v2_cd/records.jsonl")]
M = "knight2006_em"
SCRIPTS = ["logographic", "syllabic", "logosyllabic", "alphabetic"]
L = []
for lang, reals in (("latin", ["real:italian"]), ("tamil", ["real:malayalam", "real:kannada"])):
    L += [f"### {lang}", "", "| Script | Tier | A s0 | A s1 | A s2 | B s0 | B s1 | B s2 | min-max | real below `harsh` |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for st in SCRIPTS:
        rows = sorted([r for r in recs if r["lang"] == lang and r["script_type"] == st], key=lambda r: (r["sampler"], r["seed"]))
        h = [100 * r["tiers"]["related_harsh"][M]["strict"] for r in rows]
        for tier in reals + ["harsh"]:
            v = [100 * r["tiers"][f"related_{tier}"][M]["strict"] for r in rows]
            below = f"{sum(a < b for a, b in zip(v, h))}/6" if tier != "harsh" else ""
            L.append(f"| {st} | {tier.replace('real:', '')} | " + " | ".join(f"{x:.1f}" for x in v)
                     + f" | {min(v):.1f}-{max(v):.1f} | {below} |")
    L.append("")
print("\n".join(L))
```
