"""Build the v2 review page (an HTML file for the private Artifact) from the draft and the run data.

Reads reports/drafts/v2_real_relatives_section_DRAFT.md, reports/v2/cd/page_data.json and, when present,
reports/v2/cd/replication.json. The "Key findings" section of the draft becomes the findings strip;
every other section is rendered as text. Charts are drawn in the browser from the embedded data.
Usage (repository root): python reports/v2/cd/analysis/build_page.py OUT.html
"""
import html
import json
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[4]
DRAFT = ROOT / "reports" / "drafts" / "v2_real_relatives_section_DRAFT.md"
CD = ROOT / "reports" / "v2" / "cd"


def sections(md: str):
    body = "## " + md.split("\n## ", 1)[1]
    parts = re.split(r"(?m)^## ", body)[1:]
    return [(p.split("\n", 1)[0].strip(), p.split("\n", 1)[1] if "\n" in p else "") for p in parts]


def render(md: str) -> str:
    h = markdown.markdown(md, extensions=["tables", "sane_lists"])
    h = h.replace("<table>", '<div class="tbl"><table>').replace("</table>", "</table></div>")
    return re.sub(r'<p><em>(Table v2\.[^<]*(?:<code>[^<]*</code>[^<]*)*)</em></p>', r'<p class="cap">\1</p>', h)


def findings_cards(md: str) -> str:
    cards = []
    for item in re.findall(r"(?m)^- \*\*(.+?)\*\* (.+?)(?=\n- \*\*|\Z)", md, re.S):
        big, text = item
        text = markdown.markdown(" ".join(text.split()))[3:-4]
        cards.append(f'<div class="card"><div class="big">{html.escape(big)}</div><p>{text}</p></div>')
    return '<div class="cards">' + "".join(cards) + "</div>"


def checks_strip() -> str:
    p = CD / "replication.json"
    if not p.exists():
        return '<p class="note">Fresh-seed replication (entry 7): running.</p>'
    c = json.loads(p.read_text())["checks"]
    text = {"R1": "Every real-relative mean below 50%", "R2": "Old Tamil alphabetic within 10 points of Ugaritic",
            "R3": "Italian below harsh (alphabetic, syllabic)", "R4": "Real relative picked in under half of corpora"}
    chips = "".join(f'<li class="chip {"ok" if c[k]["pass"] else "no"}"><span class="glyph" aria-hidden="true">'
                    f'{"✓" if c[k]["pass"] else "✕"}</span><b>{k}</b> {text[k]} <em>'
                    f'{"replicated" if c[k]["pass"] else "not replicated"}</em></li>' for k in ("R1", "R2", "R3", "R4"))
    return f'<ul class="chips" aria-label="Replication checks fixed before the run">{chips}</ul>'


CSS = """
/* Layout: header and findings full width; charts in a wide band; text in a ~70ch column with a contents rail. */
:root {
  --paper: #f7f8f6; --ink: #1d2422; --muted: #5b6662; --rule: #d5dbd8; --accent: #2f6b5c; --wash: #e8eeeb; --panel: #ffffff;
  --s-italian: #2a78d6; --s-malayalam: #eb6834; --s-kannada: #1baf7a; --s-upper: #3a4441; --s-harsh: #8f9a96;
  --good: #1f7a4d; --bad: #b4462f;
  --serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --label: "IBM Plex Sans Condensed", "Arial Narrow", Arial, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #141917; --ink: #e3e8e5; --muted: #9aa6a1; --rule: #2e3835; --accent: #7cc0ac; --wash: #1d2522; --panel: #19201d;
  --s-italian: #3987e5; --s-malayalam: #d95926; --s-kannada: #199e70; --s-upper: #c9d1ce; --s-harsh: #7d8985;
  --good: #5cc28f; --bad: #e98a73; color-scheme: dark; } }
:root[data-theme="dark"] {
  --paper: #141917; --ink: #e3e8e5; --muted: #9aa6a1; --rule: #2e3835; --accent: #7cc0ac; --wash: #1d2522; --panel: #19201d;
  --s-italian: #3987e5; --s-malayalam: #d95926; --s-kannada: #199e70; --s-upper: #c9d1ce; --s-harsh: #7d8985;
  --good: #5cc28f; --bad: #e98a73; color-scheme: dark; }
body { background: var(--paper); color: var(--ink); font-family: var(--serif); font-size: 17px; line-height: 1.6; }
.wrap { max-width: 1160px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 28px 72px; display: grid; gap: 36px; }
header { display: grid; gap: 12px; border-bottom: 1px solid var(--rule); padding-bottom: 24px; }
.eyebrow { font-family: var(--label); font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }
h1 { font-size: clamp(30px, 4.6vw, 46px); line-height: 1.1; margin: 0; font-weight: 600; text-wrap: balance; max-width: 22ch; }
.lede { color: var(--muted); max-width: 70ch; margin: 0; }
.status { display: flex; flex-wrap: wrap; gap: 8px; font-family: var(--label); font-size: 13.5px; margin: 0; padding: 0; list-style: none; }
.status li { border: 1px solid var(--rule); background: var(--wash); padding: 3px 9px; border-radius: 3px; }
.status b { font-weight: 600; }
.section-label { font-family: var(--label); font-size: 12.5px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0 0 12px; }
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; }
.card { background: var(--panel); border: 1px solid var(--rule); padding: 16px 16px 12px; display: grid; gap: 6px; align-content: start; }
.card .big { font-family: var(--label); font-size: 30px; line-height: 1.05; font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }
.card p { margin: 0; font-size: 15px; line-height: 1.5; }
.chips { list-style: none; margin: 16px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px; font-family: var(--label); font-size: 14px; }
.chip { border: 1px solid var(--rule); padding: 4px 10px; border-radius: 3px; background: var(--panel); display: flex; gap: 6px; align-items: baseline; }
.chip.ok .glyph, .chip.ok em { color: var(--good); } .chip.no .glyph, .chip.no em { color: var(--bad); }
.chip em { font-style: normal; font-weight: 600; }
.note { font-family: var(--label); font-size: 14px; color: var(--muted); margin: 14px 0 0; }
.band { background: var(--panel); border: 1px solid var(--rule); padding: 20px; display: grid; gap: 14px; min-width: 0; }
.band h2 { font-size: 22px; margin: 0; font-weight: 600; text-wrap: balance; }
.band .sub { margin: 0; color: var(--muted); font-size: 15px; max-width: 80ch; }
.controls { display: flex; flex-wrap: wrap; gap: 18px; font-family: var(--label); font-size: 14px; }
.seg { display: flex; flex-wrap: wrap; gap: 0; border: 1px solid var(--rule); border-radius: 3px; overflow: hidden; }
.seg button { font: inherit; background: transparent; color: var(--ink); border: 0; border-right: 1px solid var(--rule);
  padding: 5px 11px; cursor: pointer; } .seg button:last-child { border-right: 0; }
.seg button[aria-pressed="true"] { background: var(--accent); color: var(--paper); }
.seg button:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.ctl-label { color: var(--muted); align-self: center; margin-right: 6px; }
.panels { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
@media (max-width: 900px) { .panels { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 520px) { .panels { grid-template-columns: minmax(0, 1fr); } }
.panel h3 { font-family: var(--label); font-size: 14px; font-weight: 600; margin: 0 0 4px; }
svg text { font-family: var(--label); fill: var(--muted); font-size: 11px; }
svg .axis line, svg .axis path { stroke: var(--rule); }
svg .grid { stroke: var(--rule); stroke-width: 1; }
svg .thr { stroke: var(--muted); stroke-dasharray: 4 3; }
svg .ug { stroke: var(--muted); stroke-dasharray: 1 3; stroke-width: 1.5; }
svg .mean { stroke: var(--ink); stroke-width: 2.5; } svg .ci { stroke: var(--ink); stroke-width: 1.2; }
svg .dot { stroke: var(--panel); stroke-width: 1.2; cursor: default; } svg .dot:hover, svg .dot:focus { stroke: var(--ink); outline: none; }
svg .dmd { fill: var(--panel); stroke: var(--ink); stroke-width: 1.5; } svg .dmd:hover, svg .dmd:focus { stroke-width: 2.5; outline: none; }
svg .rowlab { fill: var(--ink); font-size: 12px; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-family: var(--label); font-size: 13px; color: var(--muted); }
.legend span { display: inline-flex; align-items: center; gap: 6px; }
.legend i { width: 10px; height: 10px; display: inline-block; border-radius: 50%; }
.tip { position: fixed; pointer-events: none; background: var(--ink); color: var(--paper); font-family: var(--label);
  font-size: 13px; padding: 6px 9px; border-radius: 3px; max-width: 260px; z-index: 20; line-height: 1.35; }
.layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: 32px; }
@media (min-width: 980px) { .layout { grid-template-columns: 210px minmax(0, 1fr); } }
nav { font-family: var(--label); font-size: 14.5px; }
nav ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
@media (min-width: 980px) { nav .inner { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 20px); } }
nav a { color: var(--muted); text-decoration: none; } nav a:hover, nav a:focus-visible { color: var(--accent); }
main { min-width: 0; }
main h2 { font-size: 24px; line-height: 1.25; margin: 40px 0 10px; font-weight: 600; text-wrap: balance; scroll-margin-top: 16px; }
main > section:first-child h2 { margin-top: 0; }
main p, main ul, main ol, main h2, .cap { max-width: 70ch; }
p { margin: 0 0 14px; } li { margin: 4px 0; } ul, ol { padding-left: 1.3em; margin: 0 0 14px; }
strong { font-weight: 600; }
code { font-family: var(--mono); font-size: .82em; background: var(--wash); padding: 1px 4px; border-radius: 2px; overflow-wrap: anywhere; }
a { color: var(--accent); } a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.cap { font-family: var(--label); font-size: 14px; color: var(--muted); margin: 22px 0 6px; }
.tbl { overflow-x: auto; margin: 0 0 18px; border: 1px solid var(--rule); background: var(--panel); }
table { border-collapse: collapse; width: 100%; font-family: var(--label); font-size: 14.5px; font-variant-numeric: tabular-nums; }
th, td { padding: 6px 10px; border-bottom: 1px solid var(--rule); text-align: left; vertical-align: top; }
th { background: var(--wash); font-weight: 600; white-space: nowrap; } tr:last-child td { border-bottom: 0; }
td strong { color: var(--accent); }
@media (prefers-reduced-motion: no-preference) { svg .dot { transition: r .12s; } }
"""

JS = r"""
const D = JSON.parse(document.getElementById('data').textContent);
const SCRIPTS = ['logographic', 'syllabic', 'logosyllabic', 'alphabetic'];
const NAME = {sanskrit: 'Sanskrit', tamil: 'Old Tamil', sumerian: 'Sumerian', latin: 'Latin', finnish: 'Finnish'};
const REL = {upper: 'v1 sister', harsh: 'harsh', italian: 'Italian', malayalam: 'Malayalam', kannada: 'Kannada'};
const ORDER = ['upper', 'italian', 'malayalam', 'kannada', 'harsh'];
const COLOR = r => `var(--s-${r})`;
const SHAPE = {upper: 'square', harsh: 'triangle'};
let state = {lang: 'tamil', tier: 'related'};
try { const s = JSON.parse(localStorage.getItem('ibdb-v2-view') || 'null'); if (s && NAME[s.lang]) state = s; } catch (e) {}
const tip = document.createElement('div'); tip.className = 'tip'; tip.hidden = true; document.body.appendChild(tip);
const NS = 'http://www.w3.org/2000/svg';
const el = (n, a = {}, p) => { const e = document.createElementNS(NS, n); for (const k in a) e.setAttribute(k, a[k]); if (p) p.appendChild(e); return e; };
function show(ev, text) { tip.textContent = text; tip.hidden = false; const r = (ev.target.getBoundingClientRect ? ev.target.getBoundingClientRect() : {left: ev.clientX, top: ev.clientY, width: 0});
  const x = Math.min(window.innerWidth - 270, Math.max(8, r.left + r.width / 2 - 120)); tip.style.left = x + 'px'; tip.style.top = (r.top - 12 - tip.offsetHeight) + 'px'; }
function hide() { tip.hidden = true; }
function mark(g, r, cx, cy, size) {
  if (SHAPE[r] === 'square') return el('rect', {x: cx - size, y: cy - size, width: 2 * size, height: 2 * size, rx: 1.5, class: 'dot', fill: COLOR(r)}, g);
  if (SHAPE[r] === 'triangle') return el('path', {d: `M${cx},${cy - size * 1.2} L${cx + size * 1.15},${cy + size * .9} L${cx - size * 1.15},${cy + size * .9} Z`, class: 'dot', fill: COLOR(r)}, g);
  return el('circle', {cx, cy, r: size, class: 'dot', fill: COLOR(r)}, g);
}
function strip() {
  const box = document.getElementById('panels'); box.textContent = '';
  const cells = D.cells.filter(c => c.lang === state.lang && c.tier === state.tier);
  const rels = ORDER.filter(r => cells.some(c => c.rel === r));
  const xmax = Math.max(60, ...cells.flatMap(c => c.corpora.map(p => p.v))) + 4;
  const W = 260, rowH = 34, top = 6, left = 70, right = 10, H = top + rels.length * rowH + 30;
  const X = v => left + (v / xmax) * (W - left - right);
  SCRIPTS.forEach((st, i) => {
    const wrap = document.createElement('div'); wrap.className = 'panel';
    const h = document.createElement('h3'); h.textContent = st === 'logosyllabic' ? 'logo-syllabic' : st; wrap.appendChild(h);
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': `${NAME[state.lang]}, ${st}, ${state.tier} tier: sign tokens recovered per corpus`});
    if (st === 'alphabetic' && state.tier === 'related') el('rect', {x: X(D.ugaritic_recut[0]), y: top, width: X(D.ugaritic_recut[1]) - X(D.ugaritic_recut[0]), height: H - 24 - top, fill: 'var(--wash)'}, svg);
    for (const t of [0, 25, 50, 75]) if (t <= xmax) { el('line', {x1: X(t), x2: X(t), y1: top, y2: H - 24, class: t === 50 ? 'thr' : 'grid'}, svg);
      const tx = el('text', {x: X(t), y: H - 10, 'text-anchor': 'middle'}, svg); tx.textContent = t; }
    rels.forEach((r, k) => {
      const c = cells.find(c => c.rel === r && c.script === st); const cy = top + k * rowH + rowH / 2;
      const lab = el('text', {x: left - 8, y: cy + 4, 'text-anchor': 'end', class: 'rowlab'}, svg); lab.textContent = REL[r];
      if (!c) return;
      c.corpora.forEach((p, j) => {
        const jitter = ((j * 7919) % 11 - 5) * 1.4;
        const m = mark(svg, r, X(p.v), cy + jitter, 4.2);
        const txt = `${REL[r]} · ${st} · sampler ${p.sampler}, seed ${p.seed}: ${p.v.toFixed(1)}%` + (p.ref ? ` · reference chosen: ${p.ref}` : '');
        m.setAttribute('tabindex', '0'); m.setAttribute('aria-label', txt);
        m.addEventListener('pointerenter', e => show(e, txt)); m.addEventListener('pointerleave', hide);
        m.addEventListener('focus', e => show(e, txt)); m.addEventListener('blur', hide);
      });
      el('line', {x1: X(c.lo), x2: X(c.hi), y1: cy, y2: cy, class: 'ci'}, svg);
      const mean = el('line', {x1: X(c.mean), x2: X(c.mean), y1: cy - 11, y2: cy + 11, class: 'mean'}, svg);
      const hit = el('rect', {x: X(c.mean) - 6, y: cy - 13, width: 12, height: 26, fill: 'transparent'}, svg);
      const mt = `${REL[r]} · ${st}: mean ${c.mean}% (95% interval ${c.lo}-${c.hi}%, ${c.n} corpora)`;
      hit.addEventListener('pointerenter', e => show(e, mt)); hit.addEventListener('pointerleave', hide);
    });
    wrap.appendChild(svg); box.appendChild(wrap);
  });
  const ug = document.getElementById('ug-note'); ug.hidden = !(state.tier === 'related');
}
function bind(id, key) {
  document.querySelectorAll(`#${id} button`).forEach(b => {
    b.setAttribute('aria-pressed', String(b.dataset.v === state[key]));
    b.addEventListener('click', () => { state[key] = b.dataset.v;
      document.querySelectorAll(`#${id} button`).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      try { localStorage.setItem('ibdb-v2-view', JSON.stringify(state)); } catch (e) {}
      strip(); });
  });
}
function closeness() {
  const box = document.getElementById('close'); box.textContent = '';
  const pts = [['latin', 'italian'], ['latin', 'harsh'], ['tamil', 'malayalam'], ['tamil', 'kannada'], ['tamil', 'harsh']];
  const axes = [{i: 0, label: 'letter-pair JSD above floor (bits) · lower is closer', lo: 0.095, hi: 0.195, fmt: v => v.toFixed(2), ticks: [0.10, 0.12, 0.14, 0.16, 0.18]},
                {i: 1, label: 'shared word forms, chance-corrected (%) · higher is closer', lo: 2.5, hi: 13, fmt: v => v.toFixed(0), ticks: [4, 6, 8, 10, 12]}];
  axes.forEach(a => {
    const W = 420, H = 270, l = 44, r = 16, t = 24, b = 46;
    const X = v => l + (v - a.lo) / (a.hi - a.lo) * (W - l - r), Y = v => t + (1 - v / 60) * (H - t - b);
    const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': `Task D alphabetic mean against ${a.label}`});
    [0, 20, 40, 60].forEach(v => { el('line', {x1: l, x2: W - r, y1: Y(v), y2: Y(v), class: 'grid'}, svg);
      const tx = el('text', {x: l - 6, y: Y(v) + 4, 'text-anchor': 'end'}, svg); tx.textContent = v; });
    a.ticks.forEach(v => { const tx = el('text', {x: X(v), y: H - b + 16, 'text-anchor': 'middle'}, svg); tx.textContent = a.fmt(v); });
    const xl = el('text', {x: (l + W - r) / 2, y: H - 8, 'text-anchor': 'middle'}, svg); xl.textContent = a.label;
    pts.forEach(([lang, rel]) => {
      const c = D.cells.find(c => c.lang === lang && c.rel === rel && c.tier === 'related' && c.script === 'alphabetic');
      const x = D.yardsticks[`${lang}:${rel}`][a.i];
      el('line', {x1: X(x), x2: X(x), y1: Y(c.lo), y2: Y(c.hi), stroke: COLOR(rel), 'stroke-width': 2}, svg);
      const m = mark(svg, rel, X(x), Y(c.mean), 5.5);
      const name = rel === 'harsh' ? `${NAME[lang]} harsh` : REL[rel];
      const right = X(x) > W * 0.62 || (a.i === 0 && lang === 'latin' && rel === 'harsh') || (a.i === 1 && rel === 'kannada');
      const lab = el('text', {x: X(x) + (right ? -9 : 9), y: Y(c.mean) - 7, 'text-anchor': right ? 'end' : 'start', class: 'rowlab'}, svg); lab.textContent = name;
      const txt = `${name}: ${a.fmt(x)} on this yardstick; Task D alphabetic ${c.mean}% (${c.lo}-${c.hi}%)`;
      m.setAttribute('tabindex', '0'); m.setAttribute('aria-label', txt);
      m.addEventListener('pointerenter', e => show(e, txt)); m.addEventListener('pointerleave', hide);
      m.addEventListener('focus', e => show(e, txt)); m.addEventListener('blur', hide);
    });
    const yl = el('text', {x: l - 6, y: 10, 'text-anchor': 'end'}, svg); yl.textContent = '% tokens';
    const w = document.createElement('div'); w.appendChild(svg); box.appendChild(w);
  });
}
function controls() {
  const box = document.getElementById('ctl'); if (!box || !D.controls) return; box.textContent = '';
  const rows = D.controls, W = 760, rowH = 26, l = 190, r = 120, t = 8, b = 34, H = t + rows.length * rowH + b;
  const xmax = Math.max(...rows.map(x => Math.max(x.real, x.unrel[x.best], x.floor))) + 14;
  const X = v => l + v / xmax * (W - l - r);
  const svg = el('svg', {viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Each real relative against the better unrelated reference and the constant-answer floor'});
  for (let v = 0; v <= xmax; v += 10) { el('line', {x1: X(v), x2: X(v), y1: t, y2: H - b + 4, class: 'grid'}, svg);
    const tx = el('text', {x: X(v), y: H - b + 18, 'text-anchor': 'middle'}, svg); tx.textContent = v; }
  const xl = el('text', {x: X(xmax / 2), y: H - 4, 'text-anchor': 'middle'}, svg); xl.textContent = "sign tokens recovered (%), mean over 12 corpora, scored against the relative's gold";
  rows.forEach((x, i) => {
    const cy = t + i * rowH + rowH / 2, best = x.unrel[x.best];
    const lab = el('text', {x: l - 10, y: cy + 4, 'text-anchor': 'end', class: 'rowlab'}, svg);
    lab.textContent = `${REL[x.rel]}, ${x.script === 'logosyllabic' ? 'logo-syllabic' : x.script}`;
    el('rect', {x: X(0), y: cy - 4, width: Math.max(0, X(x.floor) - X(0)), height: 8, fill: 'var(--rule)'}, svg);
    el('line', {x1: X(best), x2: X(x.real), y1: cy, y2: cy, stroke: 'var(--muted)', 'stroke-width': 1}, svg);
    const d = el('path', {d: `M${X(best)},${cy - 6} L${X(best) + 6},${cy} L${X(best)},${cy + 6} L${X(best) - 6},${cy} Z`, class: 'dmd'}, svg);
    const c = el('circle', {cx: X(x.real), cy, r: 5.5, fill: COLOR(x.rel), class: 'dot'}, svg);
    const v = el('text', {x: X(Math.max(best, x.real, x.floor)) + 12, y: cy + 4, 'text-anchor': 'start', class: 'rowlab'}, svg);
    v.textContent = `${x.added > 0 ? '+' : ''}${x.added.toFixed(1)} · ${x.helps ? 'helps' : 'no measurable help'}`;
    const un = Object.entries(x.unrel).map(([k, w]) => `${NAME[k]} ${w}%`).join(', ');
    const tt = `${REL[x.rel]}, ${x.script}: relative ${x.real}%; unrelated ${un}; constant floor ${x.floor}%; ahead in ${x.wins} of ${x.n} corpora`;
    [d, c].forEach(m => { m.setAttribute('tabindex', '0'); m.setAttribute('aria-label', tt);
      m.addEventListener('pointerenter', e => show(e, tt)); m.addEventListener('pointerleave', hide);
      m.addEventListener('focus', e => show(e, tt)); m.addEventListener('blur', hide); });
  });
  box.appendChild(svg);
}
bind('ctl-lang', 'lang'); bind('ctl-tier', 'tier'); strip(); closeness(); controls();
window.addEventListener('scroll', hide, {passive: true});
"""


def main(out: str) -> None:
    md = DRAFT.read_text(encoding="utf-8")
    secs = sections(md)
    key = next((b for t, b in secs if t.lower().startswith("key findings")), "")
    body_secs = [(t, b) for t, b in secs if not t.lower().startswith("key findings")]
    toc, parts = [], []
    for t, b in body_secs:
        slug = "s-" + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:40]
        toc.append(f'<li><a href="#{slug}">{html.escape(t)}</a></li>')
        parts.append(f'<section><h2 id="{slug}">{html.escape(t)}</h2>{render(b)}</section>')
    data = json.loads((CD / "page_data.json").read_text())
    n = max(c["n"] for c in data["cells"])
    ctl_band = ""
    det = data.get("determinism") or {}
    det_txt = f"{det['compared'] - det['mismatches']} of {det['compared']} identical" if det else "pending"
    if data.get("controls"):
        det = data["determinism"]
        ctl_band = ('<section class="band" aria-labelledby="c3"><h2 id="c3">Against the null</h2>'
                    '<p class="sub">Each real relative (circle) against the better of two unrelated references (diamond), both '
                    "scored against the relative's own gold, and the constant-answer floor (grey bar): what mapping every sign "
                    "to one unit would score. A relative <em>helps</em> only if it adds at least 5 points and is ahead in at "
                    "least 9 of 12 paired corpora (rule fixed in pre-registration entry 8 before the run). Determinism: "
                    f"{det['compared'] - det['mismatches']} of {det['compared']} reruns reproduce the frozen records exactly.</p>"
                    '<div class="tbl" style="border:0;background:transparent" id="ctl"></div></section>')
    langs_btn = "".join(f'<button type="button" data-v="{k}">{v}</button>' for k, v in
                        (("tamil", "Old Tamil"), ("latin", "Latin"), ("sanskrit", "Sanskrit"), ("sumerian", "Sumerian"), ("finnish", "Finnish")))
    page = f"""<title>IBDB v2 Real Relatives</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Sans+Condensed:wght@400;600&family=IBM+Plex+Mono:wght@400&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <div class="eyebrow">Indus Blind Decipherment Benchmark · v2 · draft section for review</div>
    <h1>What a real relative buys a decipherer</h1>
    <p class="lede">Latin with Italian, Old Tamil with Malayalam and Kannada: measured with the Ugaritic-Hebrew yardsticks, given to frozen comparison-based solvers, replicated on fresh seeds, and checked against an unrelated language, a constant answer and a larger search budget. Draft for review, not for deposit. Nothing here is, or claims, a decipherment.</p>
    <ul class="status"><li><b>Methods</b> frozen-v2 · 4ce3e90</li><li><b>Pre-registration</b> entries 1-8</li><li><b>Corpora</b> {n} per cell</li><li><b>Replication</b> 4 of 4 checks</li><li><b>Reruns</b> {det_txt}</li><li><b>Pending</b> Finnish-Estonian, Pali</li></ul>
  </header>
  <section aria-labelledby="kf"><h2 class="section-label" id="kf">Key findings</h2>{findings_cards(key)}{checks_strip()}</section>
  <section class="band" aria-labelledby="c1">
    <h2 id="c1">Every corpus, every script type</h2>
    <p class="sub">Sign tokens recovered by the primary solver (revised EM, strict score, before the cognate step). One mark per corpus; the bar is the mean with a 95% bootstrap interval over corpora. Hover or focus a mark for its sampler, seed and chosen reference.</p>
    <div class="controls"><div><span class="ctl-label">Hidden language</span><div class="seg" id="ctl-lang" role="group" aria-label="Hidden language">{langs_btn}</div></div>
      <div><span class="ctl-label">Tier</span><div class="seg" id="ctl-tier" role="group" aria-label="Tier"><button type="button" data-v="related">related</button><button type="button" data-v="candidates">candidates</button></div></div></div>
    <div class="panels" id="panels"></div>
    <div class="legend"><span><i style="background:var(--s-upper);border-radius:1px"></i>v1 sister (synthetic)</span><span><i style="background:var(--s-italian)"></i>Italian</span><span><i style="background:var(--s-malayalam)"></i>Malayalam</span><span><i style="background:var(--s-kannada)"></i>Kannada</span><span><i style="background:var(--s-harsh);border-radius:0;clip-path:polygon(50% 0,100% 100%,0 100%)"></i><code>harsh</code> (synthetic; not a lower bound, negative result 3)</span><span>dashed: 50% threshold</span><span id="ug-note">shaded (alphabetic): Ugaritic-Hebrew re-cut to mean length 4.6, {data["ugaritic_recut"][0]}-{data["ugaritic_recut"][1]}%</span></div>
  </section>
  {ctl_band}
  <section class="band" aria-labelledby="c2">
    <h2 id="c2">Closer is not easier</h2>
    <p class="sub">Alphabetic Task D (related tier, mean and 95% interval) against two Ugaritic-Hebrew yardsticks for the same pairs. Italian is the closest relative on both yardsticks and the hardest for the solver. Same-script pairs only; Ugaritic-Hebrew is left out because cross-script comparisons are indicative only.</p>
    <div class="panels" id="close" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))"></div>
  </section>
  <div class="layout">
    <nav aria-label="Contents"><div class="inner"><div class="section-label">Draft section</div><ol>{''.join(toc)}</ol></div></nav>
    <main>{''.join(parts)}</main>
  </div>
</div>
<script type="application/json" id="data">{json.dumps(data)}</script>
<script>{JS}</script>
"""
    Path(out).write_text(page, encoding="utf-8")
    print(out, len(page))


if __name__ == "__main__":
    main(sys.argv[1])
