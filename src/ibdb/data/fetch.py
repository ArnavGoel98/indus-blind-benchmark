"""Download raw sources listed in config/sources.yaml into data/raw/.

Guard rail: any single download whose size is known (or turns out) to exceed
``max_download_mb`` is refused. Pass ``allow_large=True`` only after the operator agrees.
Each download writes a ``.meta.json`` next to the file with the URL, size, SHA-256, license and
time, so data provenance is recorded.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any

from .. import config
from ..paths import ensure, raw_dir


class TooLarge(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _write_meta(path: Path, url: str, license_: str, extra: dict[str, Any] | None = None) -> None:
    meta = {
        "url": url,
        "bytes": path.stat().st_size if path.is_file() else None,
        "sha256": _sha256(path) if path.is_file() else None,
        "license": license_,
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if extra:
        meta.update(extra)
    Path(str(path) + ".meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))


def http_get(url: str, dest: Path, license_: str, max_mb: float, allow_large: bool = False,
             retries: int = 4) -> Path:
    """Download with a size guard and exponential-backoff retries on network errors."""
    for attempt in range(retries + 1):
        try:
            return _http_get_once(url, dest, license_, max_mb, allow_large)
        except TooLarge:
            raise
        except OSError:
            if attempt == retries:
                raise
            time.sleep(2 ** (attempt + 1))
    raise AssertionError("unreachable")


def _http_get_once(url: str, dest: Path, license_: str, max_mb: float, allow_large: bool) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    ensure(dest.parent)
    limit = max_mb * 1024 * 1024
    req = urllib.request.Request(url, headers={"User-Agent": "ibdb-fetch/0.1 (research benchmark)"})
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(req, timeout=120) as resp:
        size = resp.headers.get("Content-Length")
        if size is not None and int(size) > limit and not allow_large:
            raise TooLarge(f"{url} is {int(size) / 2**20:.0f} MB > {max_mb} MB; rerun with --allow-large after approval")
        read = 0
        with open(tmp, "wb") as out:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                read += len(chunk)
                if read > limit and not allow_large:
                    out.close()
                    tmp.unlink(missing_ok=True)
                    raise TooLarge(f"{url} exceeded {max_mb} MB while streaming; aborted")
                out.write(chunk)
    tmp.rename(dest)
    _write_meta(dest, url, license_)
    return dest


def git_sparse(url: str, path_in_repo: str, dest: Path, license_: str) -> Path:
    """Blob-less sparse clone of one directory (keeps the transfer to what we use)."""
    if (dest / ".done").exists():
        return dest
    if shutil.which("git") is None:
        raise RuntimeError("git is required to fetch this source")
    if dest.exists():
        shutil.rmtree(dest)
    ensure(dest.parent)
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", url, str(dest)], check=True)
    subprocess.run(["git", "-C", str(dest), "sparse-checkout", "set", "--no-cone", path_in_repo], check=True)
    rev = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    (dest / ".done").write_text(rev)
    meta_path = dest.parent / (dest.name + ".meta.json")
    meta_path.write_text(json.dumps({"url": url, "path": path_in_repo, "commit": rev, "license": license_,
                                     "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, indent=2, ensure_ascii=False))
    return dest


def fetch(names: list[str] | None = None, allow_large: bool = False, log=print) -> dict[str, Path]:
    cfg = config.sources()
    max_mb = float(cfg.get("max_download_mb", 500))
    entries = {**cfg["languages"], **{k: v for k, v in cfg["controls"].items() if v.get("method")}}
    out: dict[str, Path] = {}
    for name, spec in entries.items():
        if names and name not in names:
            continue
        lic = spec["license"]
        base = raw_dir() / name
        log(f"[fetch] {name}: {spec['source']}  ({lic})")
        if spec["method"] == "git-sparse":
            out[name] = git_sparse(spec["url"], spec["path_in_repo"], base / "repo", lic)
        elif "files" in spec:
            for f in spec["files"]:
                http_get(spec["url_pattern"].format(file=f), base / f"{f}.html", lic, max_mb, allow_large)
            out[name] = base
        elif "ids" in spec:
            for i in spec["ids"]:
                http_get(spec["url_pattern"].format(id=i), base / f"pg{i}.txt", lic, max_mb, allow_large)
            out[name] = base
        else:
            fname = spec["file_url"].rsplit("/", 1)[-1]
            out[name] = http_get(spec["file_url"], base / fname, lic, max_mb, allow_large)
    return out
