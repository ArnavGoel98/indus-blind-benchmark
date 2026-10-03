"""Config loading."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from .paths import config_dir


@lru_cache(maxsize=None)
def load(name: str) -> dict[str, Any]:
    with open(config_dir() / f"{name}.yaml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def targets() -> dict[str, Any]:
    return load("indus_targets")


def sources() -> dict[str, Any]:
    return load("sources")


def experiment() -> dict[str, Any]:
    return load("experiment")


def regime_targets(regime: str) -> dict[str, dict[str, Any]]:
    """Target specs active under a calibration regime, with overrides applied."""
    cfg = targets()
    reg = cfg["regimes"][regime]
    out: dict[str, dict[str, Any]] = {}
    for name in reg["targets"]:
        spec = dict(cfg["targets"][name])
        spec.update(reg.get("overrides", {}).get(name, {}))
        out[name] = spec
    return out
