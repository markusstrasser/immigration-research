#!/usr/bin/env python3
"""Build a single self-contained warehouse: immigration.duckdb.

Merges the three real warehouses into ONE portable file so it can be downloaded
and queried standalone (the old immigration_fiscal_union.duckdb is only a thin
view-shell that ATTACHes the others by absolute path — not portable).

Layout of the unified file:
  schema `context`  — every table from immigration_context.duckdb
  schema `lifetime` — every table from immigration_lifetime_evidence.duckdb
  schema `fiscal`   — every table from immigration_fiscal_union.duckdb,
                      PLUS its cross-domain views materialized as frozen tables
  schema `main`     — unqualified VIEWs over all of the above (back-compat with the
                      query pack, which uses bare table names) + `_catalog`

Provenance is preserved by schema; `main` gives short queries. Name collisions
between context/lifetime are resolved by content-identity check (priority
context > lifetime > fiscal); a genuine conflict is left schema-qualified only
and flagged in `_catalog`.

The empty immigration_sweep.duckdb (0 rows) is intentionally excluded.

Run: uv run --with duckdb python build_unified_warehouse.py
Env: UNIFIED_DUCKDB_PATH overrides the output location.
"""
from __future__ import annotations

import sys

from paths import (
    duckdb_path,
    fiscal_union_duckdb_path,
    lifetime_duckdb_path,
    unified_duckdb_path,
)

# (attach_alias, target_schema, source_path_fn). Aliases ctx/life are REQUIRED
# names: the union views reference ctx.* / life.* internally.
SOURCES = [
    ("ctx", "context", duckdb_path),
    ("life", "lifetime", lifetime_duckdb_path),
    ("uni", "fiscal", fiscal_union_duckdb_path),
]
# main-view priority when an unqualified name appears in >1 schema
PRIORITY = ["context", "lifetime", "fiscal"]


def _ok(m):
    print(f"  ✓ {m}")


def _warn(m):
    print(f"  ! {m}")


def _header(s):
    print(f"\n[{s}]")


def _content_hash(con, schema, table):
    return con.execute(
        f'SELECT md5(string_agg(CAST(t AS VARCHAR), \'|\' ORDER BY ALL)) '
        f'FROM (SELECT * FROM "{schema}"."{table}") t'
    ).fetchone()[0]


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb not installed — run via: uv run --with duckdb python build_unified_warehouse.py")

    out = unified_duckdb_path()
    for _, _, fn in SOURCES:
        if not fn().exists():
            sys.exit(f"missing source warehouse {fn()} — build it first (reproduce.sh build all)")

    if out.exists():
        out.unlink()
    out.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(out))
    for alias, _, fn in SOURCES:
        con.execute(f"ATTACH '{fn()}' AS {alias} (READ_ONLY)")

    catalog: list[tuple] = []  # (schema, table, source_warehouse, kind, n_rows, in_main, note)
    main_owner: dict[str, tuple[str, str | None]] = {}  # unqualified_name -> (schema, content_hash)

    _header("Copy base tables + materialize views, schema-namespaced by provenance")
    for alias, schema, fn in SOURCES:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        src_name = fn().name
        # base tables
        tables = [r[0] for r in con.execute(
            "SELECT table_name FROM duckdb_tables() "
            "WHERE database_name=? AND NOT internal ORDER BY table_name", [alias]
        ).fetchall()]
        for t in tables:
            con.execute(f'CREATE TABLE "{schema}"."{t}" AS SELECT * FROM {alias}."{t}"')
            n = con.execute(f'SELECT count(*) FROM "{schema}"."{t}"').fetchone()[0]
            catalog.append((schema, t, src_name, "table", n, None, ""))
        # views: materialize as frozen tables (ctx/life are attached, so cross-domain views resolve)
        views = [r[0] for r in con.execute(
            "SELECT view_name FROM duckdb_views() "
            "WHERE database_name=? AND NOT internal ORDER BY view_name", [alias]
        ).fetchall()]
        for v in views:
            con.execute(f'CREATE TABLE "{schema}"."{v}" AS SELECT * FROM {alias}."{v}"')
            n = con.execute(f'SELECT count(*) FROM "{schema}"."{v}"').fetchone()[0]
            catalog.append((schema, v, src_name, "materialized_view", n, None, "frozen snapshot of cross-domain view"))
        _ok(f"{schema}: {len(tables)} tables + {len(views)} views  (from {src_name})")

    _header("Build unqualified main views (back-compat) with collision detection")
    conflicts = 0
    # iterate in priority order so the canonical owner wins
    by_schema = {s: [c for c in catalog if c[0] == s] for s in PRIORITY}
    for schema in PRIORITY:
        for (sch, name, src, kind, n, _, note) in by_schema[schema]:
            if name not in main_owner:
                con.execute(f'CREATE VIEW main."{name}" AS SELECT * FROM "{sch}"."{name}"')
                main_owner[name] = (sch, None)
                _set_catalog(catalog, sch, name, in_main=True)
            else:
                owner_schema = main_owner[name][0]
                h_owner = _content_hash(con, owner_schema, name)
                h_this = _content_hash(con, sch, name)
                if h_owner == h_this:
                    _set_catalog(catalog, sch, name, in_main=False,
                                 note=f"duplicate of {owner_schema}.{name} (identical) — query unqualified or {sch}.{name}")
                else:
                    conflicts += 1
                    _set_catalog(catalog, sch, name, in_main=False,
                                 note=f"NAME CONFLICT with {owner_schema}.{name} (differs) — schema-qualify to disambiguate")
                    _warn(f"conflict: {sch}.{name} differs from {owner_schema}.{name} — left schema-qualified only")
    n_main = len(main_owner)
    _ok(f"{n_main} unqualified main views" + (f"  ({conflicts} genuine conflicts left qualified)" if conflicts else "  (no genuine conflicts)"))

    _header("Write self-describing _catalog")
    con.execute("DROP TABLE IF EXISTS main._catalog")
    con.execute(
        "CREATE TABLE main._catalog ("
        "schema_name VARCHAR, table_name VARCHAR, source_warehouse VARCHAR, "
        "kind VARCHAR, n_rows BIGINT, in_main BOOLEAN, note VARCHAR)"
    )
    con.executemany(
        "INSERT INTO main._catalog VALUES (?,?,?,?,?,?,?)",
        [(s, t, src, k, n, bool(im), note) for (s, t, src, k, n, im, note) in catalog],
    )
    con.execute("CREATE OR REPLACE VIEW main._schemas AS "
                "SELECT schema_name, count(*) AS n_objects, sum(n_rows) AS total_rows "
                "FROM main._catalog GROUP BY 1 ORDER BY 1")

    # ---- verification: every source row landed ----
    _header("Verify row counts vs sources")
    ok = True
    for alias, schema, fn in SOURCES:
        # compare per-table counts
        src_tables = con.execute(
            "SELECT table_name FROM duckdb_tables() WHERE database_name=? AND NOT internal", [alias]
        ).fetchall()
        mism = 0
        for (t,) in src_tables:
            a = con.execute(f'SELECT count(*) FROM {alias}."{t}"').fetchone()[0]
            b = con.execute(f'SELECT count(*) FROM "{schema}"."{t}"').fetchone()[0]
            if a != b:
                mism += 1
                _warn(f"ROW MISMATCH {schema}.{t}: source={a} unified={b}")
        if mism == 0:
            _ok(f"{schema}: all base tables match source row counts")
        else:
            ok = False

    con.close()
    size_mb = out.stat().st_size / 1e6
    total_rows = sum(c[4] for c in catalog)
    _header("Done")
    _ok(f"wrote {out}  ({size_mb:.1f} MB, {len(catalog)} objects, {total_rows:,} rows)")
    print(f"  query it: duckdb {out} \"SELECT * FROM _catalog ORDER BY n_rows DESC LIMIT 20\"")
    if not ok:
        sys.exit("VERIFICATION FAILED — row mismatch above")


def _set_catalog(catalog, schema, name, in_main, note=None):
    for i, (s, t, src, k, n, im, nt) in enumerate(catalog):
        if s == schema and t == name:
            catalog[i] = (s, t, src, k, n, in_main, note if note is not None else nt)
            return


if __name__ == "__main__":
    build()
