"""Resolve data paths from env (portable across machines)."""
from __future__ import annotations

import os
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_INFRA_ROOT = _PKG.parent
# Repo root: .../immigration-research/infra/immigration-fiscal -> .../immigration-research
_REPO_ROOT = _INFRA_ROOT.parents[1]
_WAREHOUSE = _REPO_ROOT / "warehouse"


def data_root() -> Path:
    if v := os.environ.get("PNY_DATA_ROOT"):
        return Path(v)
    # Legacy: sources/immigration-fiscal/data on symlinked SSD layout
    return _INFRA_ROOT.parent / "sources" / "immigration-fiscal" / "data"


def derived_root() -> Path:
    if v := os.environ.get("DERIVED_ROOT"):
        return Path(v)
    return data_root() / "derived"


def duckdb_path() -> Path:
    if v := os.environ.get("DUCKDB_PATH"):
        return Path(v)
    return _WAREHOUSE / "immigration_context.duckdb"


def lifetime_duckdb_path() -> Path:
    if v := os.environ.get("LIFETIME_DUCKDB_PATH"):
        return Path(v)
    return _WAREHOUSE / "immigration_lifetime_evidence.duckdb"


def fiscal_union_duckdb_path() -> Path:
    if v := os.environ.get("FISCAL_UNION_DUCKDB_PATH"):
        return Path(v)
    return _WAREHOUSE / "immigration_fiscal_union.duckdb"


def unified_duckdb_path() -> Path:
    """Single self-contained warehouse: context + lifetime + fiscal union, schema-namespaced."""
    if v := os.environ.get("UNIFIED_DUCKDB_PATH"):
        return Path(v)
    return _WAREHOUSE / "immigration.duckdb"
