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
import re
import json
import time
import urllib.parse
import urllib.request

from ibdb.paths import raw_dir

UA = "IBDB-research/0.1 (arnavgoel@woodstock.ac.in)"
OUT = raw_dir() / "relatives"
EXCLUDE = "ಸಟೀಕಾ"
PARVAS = ["ಆದಿಪರ್ವ", "ಸಭಾಪರ್ವ", "ಅರಣ್ಯಪರ್ವ", "ವಿರಾಟಪರ್ವ", "ಉದ್ಯೋಗಪರ್ವ", "ಭೀಷ್ಮಪರ್ವ", "ದ್ರೋಣಪರ್ವ", "ಕರ್ಣಪರ್ವ",
          "ಶಲ್ಯಪರ್ವ", "ಗದಾಪರ್ವ"]
SANDHI = re.compile(r"^(" + "|".join(PARVAS) + r"): *[೦-೯0-9]+\..*ಸಂಧಿ")


def get(url: str, params: dict) -> bytes:
    """POST (titles in batches make GET URLs too long), polite pacing, back-off on 429."""
    body = urllib.parse.urlencode(params).encode()
    wait = 30
    for _ in range(8):
        time.sleep(4)
        try:
            req = urllib.request.Request(url, data=body, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
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


def fetch(site: str, titles: list[str], batch: int = 50) -> None:
    """Fetch the current revision of every title through Special:Export (one request per `batch` pages;
    the API was rate-limited from this environment)."""
    import xml.etree.ElementTree as ET
    ns = "{http://www.mediawiki.org/xml/export-0.11/}"
    d = OUT / site
    d.mkdir(parents=True, exist_ok=True)
    man_path = d / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    todo = [t for t in titles if t not in man]
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        xml = get(f"https://{site}.wikisource.org/w/index.php",
                  {"title": "Special:Export", "pages": "\n".join(chunk), "curonly": "1", "action": "submit"})
        for pg in ET.fromstring(xml).iter(f"{ns}page"):
            title = pg.find(f"{ns}title").text
            rev = pg.find(f"{ns}revision")
            text = rev.find(f"{ns}text").text or ""
            f = f"{len(man):04d}.wiki"
            (d / f).write_text(text, encoding="utf-8")
            man[title] = {"title": title, "revid": int(rev.find(f"{ns}id").text), "timestamp": rev.find(f"{ns}timestamp").text,
                          "sha256": hashlib.sha256(text.encode()).hexdigest(), "file": f}
        man_path.write_text(json.dumps(man, ensure_ascii=False, indent=1))
        print(f"[{site}] {len(man)}/{len(titles)}", flush=True)
    missing = [t for t in titles if t not in man]
    print(f"[{site}] done: {len(man)} pages; missing {len(missing)}: {missing[:5]}", flush=True)


def main() -> None:
    ml = api("ml", action="query", list="allpages", apprefix="അദ്ധ്യാത്മരാമായണം കിളിപ്പാട്ട്/", aplimit="500")
    ml_titles = [p["title"] for p in ml["query"]["allpages"] if p["title"].count("/") == 2]
    fetch("ml", ml_titles)
    # Kannada: the index page links the ten parva pages (and unrelated works); each parva page links
    # its sandhis. Keep only sandhi pages of the ten parvas, never the ಸಟೀಕಾ commentary pages.
    kn = api("kn", action="query", titles="|".join(PARVAS), prop="links", pllimit="500")
    links = sorted({l["title"] for p in kn["query"]["pages"].values() for l in p.get("links", [])})
    sandhi = [t for t in links if SANDHI.match(t) and EXCLUDE not in t]
    (OUT / "kn_sandhi_titles.json").write_text(json.dumps({"parva_links": links, "sandhi": sandhi,
                                                           "excluded_satika": [t for t in links if EXCLUDE in t]},
                                                          ensure_ascii=False, indent=1))
    fetch("kn", sandhi)


if __name__ == "__main__":
    main()
