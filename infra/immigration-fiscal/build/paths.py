"""Resolve data paths from env (portable across machines)."""
from __future__ import annotations

import os
from pathlib import Path

_PKG = Path(__file__).resolve().parent
_INFRA_ROOT = _PKG.parent
# Repo root: .../immigration-research/infra/immigration-fiscal -> .../immigration-research
_REPO_ROOT = _INFRA_ROOT.parents[1]
_WAREHOUSE = _REPO_ROOT / "warehouse"


def staged_output(path: Path) -> Path:
    """Return a scratch path to build ``path`` into; commit with :func:`commit_output`.

    Builders used to delete the existing warehouse before rebuilding, so a build that failed
    on missing inputs left nothing behind (2026-09-16 recovery probe: a context rebuild with
    the causal tree gone would have replaced an intact 70-table warehouse). Building beside
    the artefact and replacing it only on success keeps the last good file until then.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".building")
    if tmp.exists():
        tmp.unlink()
    return tmp


def commit_output(tmp: Path, path: Path) -> Path:
    """Atomically replace ``path`` with the finished ``tmp`` build (same filesystem)."""
    os.replace(tmp, path)
    return path


def _existing_fallback(path: Path, what: str, env_var: str) -> Path:
    """Legacy fallbacks must exist; a dangling symlink or unmounted SSD is an error, not a target.

    The 2026-09-16 recovery probe found that with DERIVED_ROOT unset this module silently
    resolved to a dead symlink, which is how a lost data tree went unnoticed.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"{what} {path} does not exist (dangling symlink or SSD not mounted); "
            f"set {env_var} (see acquire/config.env.example) or run via reproduce.sh"
        )
    return path


def data_root() -> Path:
    if v := os.environ.get("PNY_DATA_ROOT"):
        return Path(v)
    # Legacy: sources/immigration-fiscal/data on symlinked SSD layout
    return _existing_fallback(
        _REPO_ROOT / "sources" / "immigration-fiscal" / "data", "legacy data root", "PNY_DATA_ROOT"
    )


def derived_root() -> Path:
    if v := os.environ.get("DERIVED_ROOT"):
        return Path(v)
    return _existing_fallback(data_root() / "derived", "legacy derived root", "DERIVED_ROOT")


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


def microdata_duckdb_path() -> Path:
    """Local-only raw microdata (IPUMS PUMS etc.). NOT redistributable — never part of the
    unified release; isolated from the aggregate warehouses for size + licensing.
    Defaults to the (large, SSD-backed) derived root, not the repo warehouse/ on the main disk."""
    if v := os.environ.get("MICRODATA_DUCKDB_PATH"):
        return Path(v)
    return derived_root() / "immigration_microdata.duckdb"
