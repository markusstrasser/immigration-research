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
    """Default inputs must exist; a missing local tree is an error, not a target.

    The 2026-09-16 recovery probe found that with DERIVED_ROOT unset this module silently
    resolved to a dead symlink, which is how a lost data tree went unnoticed.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"{what} {path} does not exist; restore the project-local dataset or "
            f"set {env_var} (see acquire/config.env.example) or run via reproduce.sh"
        )
    return path


def data_root(*, require_exists: bool = True) -> Path:
    """Resolve raw data; defer validation only when constructing unused defaults."""
    if v := os.environ.get("PNY_DATA_ROOT") or os.environ.get("IMMIGRATION_DATA_ROOT"):
        return Path(v)
    target = _REPO_ROOT / "sources" / "immigration-fiscal" / "data"
    return _existing_fallback(target, "local data root", "PNY_DATA_ROOT") if require_exists else target


def derived_root(*, require_exists: bool = True) -> Path:
    if v := os.environ.get("DERIVED_ROOT") or os.environ.get("IMMIGRATION_DERIVED_ROOT"):
        return Path(v)
    raw_override = os.environ.get("PNY_DATA_ROOT") or os.environ.get("IMMIGRATION_DATA_ROOT")
    target = (Path(raw_override) / "derived" if raw_override else
              _REPO_ROOT / "sources" / "immigration-fiscal" / "derived")
    return _existing_fallback(target, "local derived root", "DERIVED_ROOT") if require_exists else target


def corpus_root() -> Path:
    """Optional mirrors; individual callers must check their required source file."""
    value = os.environ.get("CORPUS_ROOT") or os.environ.get("IMMIGRATION_CORPUS_ROOT")
    return Path(value) if value else _REPO_ROOT / "sources" / "corpus"


def itep_table_path() -> Path:
    """Select the ITEP source; IMMIGRATION_FISCAL_ROOT denotes code, not data."""
    if value := os.environ.get("ITEP_TABLE_PATH"):
        return Path(value)
    return data_root(require_exists=False) / "itep/itep_table_5.tsv"


def reused_surveys_root(*, require_exists: bool = True) -> Path:
    if value := os.environ.get("REUSED_SURVEYS_ROOT"):
        return Path(value)
    target = _REPO_ROOT / "sources" / "reused-surveys"
    return _existing_fallback(target, "local reused survey root", "REUSED_SURVEYS_ROOT") if require_exists else target


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


def microdata_duckdb_path(*, require_exists: bool = True) -> Path:
    """Local-only raw microdata (IPUMS PUMS etc.). NOT redistributable — never part of the
    unified release; isolated from the aggregate warehouses for size + licensing.
    Defaults to the project-local derived root, separate from aggregate warehouse/."""
    if v := os.environ.get("MICRODATA_DUCKDB_PATH"):
        return Path(v)
    return derived_root(require_exists=require_exists) / "immigration_microdata.duckdb"
