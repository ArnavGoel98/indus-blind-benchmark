"""Filesystem layout. Everything is relative to the project root (the folder holding config/)."""

from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("IBDB_ROOT")
    if env:
        return Path(env).resolve()
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / "config" / "indus_targets.yaml").exists():
            return p
    # Fall back to the source checkout this module lives in.
    return Path(__file__).resolve().parents[2]


def config_dir() -> Path:
    return project_root() / "config"


def raw_dir() -> Path:
    return project_root() / "data" / "raw"


def segments_dir() -> Path:
    return project_root() / "data" / "segments"


def private_dir() -> Path:
    """Answer keys. Git-ignored. Never publish."""
    return project_root() / "private"


def runs_dir() -> Path:
    return project_root() / "runs"


def reports_dir() -> Path:
    return project_root() / "reports"


def ensure(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p
