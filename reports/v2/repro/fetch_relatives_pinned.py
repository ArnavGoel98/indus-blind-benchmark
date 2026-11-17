"""Re-fetch the Wikisource relative texts exactly as they stood on the original fetch date.

The original fetchers (scripts/v2/fetch_dravidian_wikisource.py and the Kalevipoeg fetch) took the
*current* revision of each page and kept the manifest in data/ (git-ignored), so a later fetch could get
edited text. This fetcher asks the MediaWiki API for the revision current at CUTOFF (end of 2026-10-15
UTC, the fetch date in config/sources.yaml), writes the same files in the same order, and writes
the manifest (title, revision id, timestamp, SHA-256) that `reports/v2/repro/relatives_manifest.json`
pins in the repository. Pages edited after CUTOFF are listed, not used.

Usage (repository root): python reports/v2/repro/fetch_relatives_pinned.py [--check-only | --resume]
  --check-only compares data/raw/relatives with the committed pin and fetches nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import signal
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from ibdb.data import dravidian as D
from ibdb.data import relatives as R
from ibdb.paths import raw_dir

CUTOFF = "2026-10-15T23:59:59Z"
UA = "IBDB-research/0.1 (reproducibility re-fetch)"
OUT = raw_dir() / "relatives"
PIN = Path(__file__).resolve().parent / "relatives_manifest.json"
PARVAS = ["ಆದಿಪರ್ವ", "ಸಭಾಪರ್ವ", "ಅರಣ್ಯಪರ್ವ", "ವಿರಾಟಪರ್ವ", "ಉದ್ಯೋಗಪರ್ವ", "ಭೀಷ್ಮಪರ್ವ", "ದ್ರೋಣಪರ್ವ", "ಕರ್ಣಪರ್ವ",
          "ಶಲ್ಯಪರ್ವ", "ಗದಾಪರ್ವ"]


def api(site: str, **params) -> dict:
    url = f"https://{site}.wikisource.org/w/api.php"
    body = urllib.parse.urlencode(params | {"format": "json", "formatversion": "2"}).encode()
    wait = 30
    for _ in range(8):
        time.sleep(1.5)
        signal.alarm(120)                                  # a stalled read can outlive the socket timeout
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=body, headers={"User-Agent": UA}), timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504):
                raise
            print(f"  [{site}] HTTP {e.code}; retrying in {wait}s", flush=True)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:     # proxy or network hiccup, or a stall
            print(f"  [{site}] {e!r}; retrying in {wait}s", flush=True)
        finally:
            signal.alarm(0)
        time.sleep(wait)
        wait *= 2
    raise RuntimeError("rate limited too long")


def revision_at(site: str, title: str) -> tuple[dict, int]:
    """The revision current at CUTOFF, and the number of later revisions."""
    q = api(site, action="query", prop="revisions", titles=title, rvprop="ids|timestamp|content", rvslots="main",
            rvlimit="1", rvstart=CUTOFF, rvdir="older")
    pg = q["query"]["pages"][0]
    if not pg.get("revisions"):
        return None, 0                                     # missing page, or created after CUTOFF
    rev = pg["revisions"][0]
    later = api(site, action="query", prop="revisions", titles=title, rvprop="ids", rvlimit="50", rvstart=CUTOFF,
                rvdir="newer")
    n_later = len([r for r in later["query"]["pages"][0].get("revisions", []) if r["revid"] != rev["revid"]])
    return rev, n_later


def _stalled(*_):
    raise TimeoutError("request stalled")


def fetch(site: str, titles: list[str], name=lambda i, t: f"{i:04d}.wiki", resume: bool = False,
          folder: str | None = None) -> dict:
    d = OUT / (folder or site)
    if resume and (d / "manifest.json").exists():          # a site finished by an earlier, interrupted run
        man = json.loads((d / "manifest.json").read_text())
        print(f"[{site}] resumed: {len(man)} pages from the saved manifest", flush=True)
        return man
    d.mkdir(parents=True, exist_ok=True)
    man, absent = {}, []
    i = 0
    for t in titles:
        rev, n_later = revision_at(site, t)
        if rev is None:
            absent.append(t)
            print(f"[{site}] {t}: no revision at cutoff (absent)", flush=True)
            continue
        text = rev["slots"]["main"]["content"]
        f = name(i, t)
        (d / f).write_text(text, encoding="utf-8")
        man[t] = {"title": t, "revid": rev["revid"], "timestamp": rev["timestamp"], "file": f,
                  "sha256": hashlib.sha256(text.encode()).hexdigest(), "edited_after_cutoff": n_later}
        print(f"[{site}] {i + 1}/{len(titles)} {t} rev {rev['revid']}{' (edited later)' if n_later else ''}", flush=True)
        i += 1
    (d / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    if absent:
        (d / "absent_at_cutoff.json").write_text(json.dumps(absent, ensure_ascii=False, indent=1))
    return man


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--resume", action="store_true", help="keep sites whose manifest an interrupted run already wrote")
    a = ap.parse_args()
    signal.signal(signal.SIGALRM, _stalled)
    if a.check_only:
        pin = json.loads(PIN.read_text())
        bad = []
        for site, pages in pin["pages"].items():
            for t, m in pages.items():
                p = OUT / ("" if site == "et" else site) / m["file"]
                if not p.exists() or hashlib.sha256(p.read_text(encoding="utf-8").encode()).hexdigest() != m["sha256"]:
                    bad.append(f"{site} {t}")
        print(f"{sum(len(v) for v in pin['pages'].values())} pages pinned; {len(bad)} differ: {bad[:5]}")
        sys.exit(1 if bad else 0)
    pages = {}
    done = lambda site: a.resume and (OUT / site / "manifest.json").exists()  # noqa: E731
    ml = [] if done("ml") else [p["title"] for p in api("ml", action="query", list="allpages",
                                apprefix="അദ്ധ്യാത്മരാമായണം കിളിപ്പാട്ട്/", aplimit="500")["query"]["allpages"]]
    pages["ml"] = fetch("ml", [t for t in ml if t.count("/") == 2], resume=a.resume)
    kn = [] if done("kn") else [l["title"] for p in api("kn", action="query", titles="|".join(PARVAS), prop="links",
                                                        pllimit="500")["query"]["pages"] for l in p.get("links", [])]
    pages["kn"] = fetch("kn", [t for t in sorted(set(kn)) if D.KN_SANDHI.match(t) and "ಸಟೀಕಾ" not in t], resume=a.resume)
    et = fetch("et", [f"Kalevipoeg/{c}" for c in R.KALEVIPOEG_CANTOS], name=lambda i, t: f"kalevipoeg_{t.split('/')[1]}.wiki",
               resume=a.resume, folder="et_tmp")
    for m in et.values():                                   # relatives.py reads them from data/raw/relatives/
        (OUT / m["file"]).write_bytes((OUT / "et_tmp" / m["file"]).read_bytes())
    pages["et"] = et
    PIN.parent.mkdir(parents=True, exist_ok=True)
    PIN.write_text(json.dumps({"cutoff": CUTOFF, "pages": pages}, ensure_ascii=False, indent=1))
    print("edited after cutoff:", sum(m["edited_after_cutoff"] > 0 for v in pages.values() for m in v.values()))


if __name__ == "__main__":
    main()
