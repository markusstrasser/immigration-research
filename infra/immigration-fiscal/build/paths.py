"""Resolve data paths from env (portable across machines)."""
from __future__ import annotations

import os
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_INFRA_ROOT = _PKG.parent


def data_root() -> Path:
    if v := os.environ.get("PNY_DATA_ROOT"):
        return Path(v)
    # Legacy: sources/immigration-fiscal/data on symlinked SSD layout
    return _INFRA_ROOT.parent / "sources" / "immigration-fiscal" / "data"


def derived_root() -> Path:
    if v := os.environ.get("DERIVED_ROOT"):
        return Path(v)
    return _PKG


def duckdb_path() -> Path:
    if v := os.environ.get("DUCKDB_PATH"):
        return Path(v)
    return Path.home() / "Projects" / "research" / "warehouse" / "immigration_context.duckdb"
