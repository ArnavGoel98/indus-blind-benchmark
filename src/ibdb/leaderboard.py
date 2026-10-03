"""Static leaderboard page (plain HTML + inline JSON, no backend) and reference baseline submissions."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

import numpy as np

from . import config, ml
from .corpus import Corpus
from .evaluate import load_records
from .knowledge import build_reference
from .methods.base import Knowledge
from .methods.decipher import KnightEM
from .methods.structural import MultiFeatureClassifier, ScriptTypeLR
from .paths import ensure, project_root

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IBDB Leaderboard</title>
<style>
:root {
  --bg: #fcfcfb; --surface: #ffffff; --ink: #0b0b0b; --ink2: #52514e; --muted: #8a8984;
  --line: #e4e3df; --accent: #2a78d6; --warn-bg: #fff4e0; --warn-ink: #6b4500;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #141413; --surface: #1a1a19; --ink: #ffffff; --ink2: #c3c2b7; --muted: #8f8e86;
    --line: #2e2e2b; --accent: #3987e5; --warn-bg: #3a2c10; --warn-ink: #f3d79b;
  }
}
:root[data-theme="dark"] {
  --bg: #141413; --surface: #1a1a19; --ink: #ffffff; --ink2: #c3c2b7; --muted: #8f8e86;
  --line: #2e2e2b; --accent: #3987e5; --warn-bg: #3a2c10; --warn-ink: #f3d79b;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 15px/1.5 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 1080px; margin: 0 auto; padding: 32px 16px 64px; }
h1 { font-size: 26px; margin: 0 0 4px; letter-spacing: -0.01em; }
.sub { color: var(--ink2); margin: 0 0 20px; }
.note { background: var(--warn-bg); color: var(--warn-ink); border-radius: 8px; padding: 12px 14px; margin: 0 0 20px; font-size: 14px; }
.controls { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 12px; }
.controls button { font: inherit; font-size: 13px; padding: 6px 12px; border-radius: 999px; border: 1px solid var(--line);
                   background: var(--surface); color: var(--ink2); cursor: pointer; }
.controls button[aria-pressed="true"] { border-color: var(--accent); color: var(--ink); }
.wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }
table { border-collapse: collapse; width: 100%; min-width: 760px; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--line); white-space: nowrap; }
th { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); cursor: pointer; user-select: none; }
td.num, th.num { text-align: right; }
tr.chance td { color: var(--muted); font-style: italic; }
tr:last-child td { border-bottom: 0; }
.tag { font-size: 11px; padding: 2px 6px; border-radius: 4px; border: 1px solid var(--line); color: var(--ink2); }
.claim { border-color: var(--warn-ink); color: var(--warn-ink); }
section { margin-top: 32px; }
h2 { font-size: 18px; margin: 0 0 8px; }
p, li { color: var(--ink2); }
code { font-size: 13px; }
</style>
</head>
<body>
<main>
<h1>Indus Blind Decipherment Benchmark</h1>
<p class="sub">Leaderboard for synthetic, Indus-calibrated corpora with hidden answer keys. Scores are on synthetic scripts only.</p>
<p class="note">A high score here shows that a method recovers hidden information from Indus-<em>like</em> data. It is
<strong>not</strong> evidence for any reading of the actual Indus script, and IBDB claims no decipherment.</p>
<div class="controls" role="group" aria-label="Filter by tier">
  <button data-tier="hidden" aria-pressed="true">Hidden tier</button>
  <button data-tier="public" aria-pressed="false">Public tier (keys released)</button>
</div>
<div class="wrap"><table id="lb">
<thead><tr>
<th data-k="team">Team</th><th data-k="method">Method</th><th data-k="round">Round</th>
<th class="num" data-k="A_balanced_acc" title="Language vs non-language, balanced accuracy">A lang.</th>
<th class="num" data-k="B_acc" title="Script type accuracy">B script</th>
<th class="num" data-k="C_acc" title="Language family accuracy">C family</th>
<th class="num" data-k="D_token_acc" title="Share of sign tokens read correctly">D values</th>
<th data-k="scored_utc">Scored</th></tr></thead>
<tbody></tbody></table></div>
<section>
<h2>How to submit</h2>
<ol>
<li>Download a round from <code>challenge/hidden/&lt;round&gt;/corpora/</code>. Each file lists sign-ID sequences in physical order, plus the reading direction.</li>
<li>Write one JSON file: <code>{"team": ..., "method": ..., "url": ..., "claims_indus_decipherment": true|false, "predictions": {corpus_id: {"is_linguistic": bool, "script_type": ..., "family": ..., "sign_values": {sign_id: value}}}}</code>. Any task may be omitted.</li>
<li>Send it to the maintainer, who runs <code>ibdb-score submission.json --round &lt;round&gt; --tier hidden --record</code> offline. One scored submission per team per hidden round.</li>
<li>Answer keys are fixed in advance: their SHA-256 hashes are published in <code>commitments.json</code> and checked at scoring time.</li>
</ol>
<p>Rows tagged <span class="tag claim">claims Indus decipherment</span> come from authors who say their method has deciphered the real script. Seeing how such a method does on data with a known answer is the point of this board.</p>
</section>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const data = JSON.parse(document.getElementById('data').textContent);
const chance = data.chance;
let tier = 'hidden', sortKey = 'D_token_acc', dir = -1;
const fmt = v => (v === null || v === undefined || Number.isNaN(v)) ? '–' : Number(v).toFixed(3);
function esc(s) { const d = document.createElement('div'); d.textContent = s ?? ''; return d.innerHTML; }
function render() {
  const rows = data.entries.filter(e => e.tier === tier).slice().sort((a, b) => {
    const x = a[sortKey], y = b[sortKey];
    if (typeof x === 'number' || typeof y === 'number') return dir * ((x ?? -1) - (y ?? -1));
    return dir * String(x ?? '').localeCompare(String(y ?? ''));
  });
  const tb = document.querySelector('#lb tbody');
  tb.innerHTML = rows.map(e => `<tr><td>${esc(e.team)} ${e.claims_indus_decipherment ? '<span class="tag claim">claims Indus decipherment</span>' : ''}</td>
    <td>${e.url ? `<a href="${esc(e.url)}">${esc(e.method)}</a>` : esc(e.method)}</td><td>${esc(e.round)}</td>
    <td class="num">${fmt(e.A_balanced_acc)}</td><td class="num">${fmt(e.B_acc)}</td><td class="num">${fmt(e.C_acc)}</td>
    <td class="num">${fmt(e.D_token_acc)}</td><td>${esc((e.scored_utc || '').slice(0, 10))}</td></tr>`).join('')
    + `<tr class="chance"><td>chance</td><td>random guessing</td><td></td><td class="num">${fmt(chance.A)}</td>
       <td class="num">${fmt(chance.B)}</td><td class="num">${fmt(chance.C)}</td><td class="num">≈0</td><td></td></tr>`;
}
document.querySelectorAll('.controls button').forEach(b => b.addEventListener('click', () => {
  tier = b.dataset.tier;
  document.querySelectorAll('.controls button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
  render();
}));
document.querySelectorAll('th[data-k]').forEach(th => th.addEventListener('click', () => {
  const k = th.dataset.k; dir = (k === sortKey) ? -dir : -1; sortKey = k; render();
}));
render();
</script>
</body>
</html>
"""


def build_page(out: Path | None = None) -> Path:
    data_p = project_root() / "leaderboard" / "data.json"
    data = json.loads(data_p.read_text()) if data_p.exists() else {"entries": []}
    data["chance"] = {"A": 0.5, "B": 0.25, "C": 0.25}
    out = out or ensure(project_root() / "leaderboard") / "index.html"
    blob = json.dumps(data).replace("</", "<\\/")
    out.write_text(PAGE.replace("__DATA__", blob))
    return out


def _train_models(profile_name: str):
    prof = config.experiment()["profiles"][profile_name]
    ip = prof["indus_point"]
    recs = [r for r in load_records(profile_name) if "error" not in r and r["job"]["sweep"] == "size"
            and r["job"]["n_texts"] == ip["n_texts"] and r["job"]["regime"] == "full"]
    a = [r for r in recs if r["truth"]["kind"] in ("language", "structural", "adversarial", "trivial")]
    lr = ml.fit_logreg(np.array([r["A"]["ling_classifier_lr"]["vector"] for r in a], float),
                       np.array([r["truth"]["is_linguistic"] for r in a]))
    b = [r for r in recs if r["truth"]["kind"] == "language"]
    f = lambda r: [float(r["B"]["script_type_lr"]["features"][k]) for k in sorted(r["B"]["script_type_lr"]["features"])]  # noqa: E731
    sm = ml.fit_softmax(np.array([f(r) for r in b]), [r["truth"]["script_type"] for r in b])
    return lr, sm


def baseline_submission(round_id: str, tier: str, profile_name: str = "full", log=print) -> dict:
    """Reference entry: our pipeline with NO oracle (script type predicted, public languages as candidates)."""
    lr, sm = _train_models(profile_name)
    root = project_root() / "challenge" / tier / round_id / "corpora"
    langs = config.experiment()["profiles"][profile_name]["languages"]
    preds = {}
    for p in sorted(root.glob("*.json.gz")):
        c = Corpus.load(p)
        cid = c.corpus_id
        v = MultiFeatureClassifier().analyze(c).extra["vector"]
        is_ling = bool(ml.predict_logreg(lr, np.array([v], float))[0] > 0.5)
        feats = ScriptTypeLR().analyze(c).script_features
        st = ml.predict_softmax(sm, np.array([[float(feats[k]) for k in sorted(feats)]]))[0]
        kn = Knowledge(tier="candidates", script_type=st,
                       references=[build_reference(l, st, False, 0) for l in langs])
        em = KnightEM().analyze(c, kn)
        preds[cid] = {"is_linguistic": is_ling, "script_type": st, "family": em.family,
                      "sign_values": {str(k): v for k, v in (em.sign_values or {}).items()}}
        log(f"[baseline] {cid}: ling={is_ling} script={st} family={em.family}")
    return {"team": "IBDB reference baselines", "method": "multi-feature LR + inventory/frequency LR + Knight-style EM (no oracle)",
            "url": "", "claims_indus_decipherment": False, "predictions": preds}
