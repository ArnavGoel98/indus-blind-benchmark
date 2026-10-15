"""Fetch the Malayalam and Kannada Wikisource texts for rank 6b (pre-registration entry 5).

Malayalam: Adhyatma Ramayanam Kilippattu, ml.wikisource.org, every section page
  (title/kanda/section). Kannada: Kumaravyasa Bharata, kn.wikisource.org, every page linked from
  the index page, EXCLUDING pages whose title contains "ಸಟೀಕಾ" (a modern commentary).
Both CC BY-SA 4.0 (site licence), texts public domain by age; source edition unstated on either
site (accepted as clean by the project owner, 2026-10-15). Raw wikitext is saved under
data/raw/relatives/{ml,kn}/ with a manifest (title, revision id, timestamp, SHA-256). Polite: one
request every 4 s, exponential back-off on HTTP 429.

Usage: python scripts/v2/fetch_dravidian_wikisource.py
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
import urllib.request

from ibdb.paths import raw_dir

UA = "IBDB-research/0.1 (arnavgoel@woodstock.ac.in)"
OUT = raw_dir() / "relatives"
EXCLUDE = "ಸಟೀಕಾ"


def get(url: str, params: dict) -> bytes:
    q = url + "?" + urllib.parse.urlencode(params)
    wait = 30
    for _ in range(8):
        time.sleep(4)
        try:
            with urllib.request.urlopen(urllib.request.Request(q, headers={"User-Agent": UA}), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            print(f"429, waiting {wait}s", flush=True)
            time.sleep(wait)
            wait *= 2
    raise RuntimeError("rate limited too long")


def api(site: str, **params) -> dict:
    params |= {"format": "json"}
    return json.loads(get(f"https://{site}.wikisource.org/w/api.php", params))


def page(site: str, title: str) -> dict:
    d = api(site, action="query", titles=title, prop="revisions", rvprop="ids|timestamp|content", rvslots="main")
    p = next(iter(d["query"]["pages"].values()))
    r = p["revisions"][0]
    text = r["slots"]["main"]["*"]
    return {"title": title, "revid": r["revid"], "timestamp": r["timestamp"], "text": text,
            "sha256": hashlib.sha256(text.encode()).hexdigest()}


def fetch(site: str, titles: list[str]) -> None:
    d = OUT / site
    d.mkdir(parents=True, exist_ok=True)
    man_path = d / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    for i, t in enumerate(titles):
        if t in man:
            continue
        p = page(site, t)
        f = f"{len(man):04d}.wiki"
        (d / f).write_text(p.pop("text"), encoding="utf-8")
        man[t] = p | {"file": f}
        man_path.write_text(json.dumps(man, ensure_ascii=False, indent=1))
        if (i + 1) % 20 == 0:
            print(f"[{site}] {i + 1}/{len(titles)}", flush=True)
    print(f"[{site}] done: {len(man)} pages", flush=True)


def main() -> None:
    ml = api("ml", action="query", list="allpages", apprefix="അദ്ധ്യാത്മരാമായണം കിളിപ്പാട്ട്/", aplimit="500")
    ml_titles = [p["title"] for p in ml["query"]["allpages"] if p["title"].count("/") == 2]
    fetch("ml", ml_titles)
    kn = api("kn", action="query", titles="ಕುಮಾರವ್ಯಾಸ ಭಾರತ", prop="links", pllimit="500")
    links = [l["title"] for p in kn["query"]["pages"].values() for l in p.get("links", [])]
    kn_titles = [t for t in links if EXCLUDE not in t]
    (OUT / "kn_index_links.json").write_text(json.dumps({"all": links, "excluded_satika": [t for t in links if EXCLUDE in t]},
                                                         ensure_ascii=False, indent=1))
    fetch("kn", kn_titles)


if __name__ == "__main__":
    main()
