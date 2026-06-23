#!/usr/bin/env python3
"""Emit a Markdown data dictionary for the unified immigration.duckdb.

Reads main._catalog + per-column types and writes a human-readable dictionary:
one section per schema, a table per object with columns, types, row counts,
provenance, and any conflict/duplicate notes. Self-documenting — regenerate
whenever the warehouse changes.

Run: uv run --with duckdb python emit_data_dictionary.py [OUT.md]
"""
from __future__ import annotations

import sys
from pathlib import Path

from paths import unified_duckdb_path

SCHEMA_BLURB = {
    "context": "ACS / county / PUMA / zip context — population stock, education, housing, "
    "rent (SAFMR), Medicaid, school poverty (SAIPE), court backlog (EOIR), immigrant health.",
    "lifetime": "Lifetime fiscal evidence — NPV benchmarks, CDC life tables, IRS migration, "
    "ITEP undocumented tax, MEPS health, OMB outlays, SIPP scenario cells, source provenance.",
    "fiscal": "Cross-domain fiscal union — country fiscal tensor, NPV bridge grid, CBO objects, "
    "GE wage scenarios, and the materialized cross-domain join views (v_*).",
}


def build(out_path: Path) -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("duckdb not installed — run via: uv run --with duckdb python emit_data_dictionary.py")

    db = unified_duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — build it first: reproduce.sh build unified")
    con = duckdb.connect(str(db), read_only=True)

    cat = con.execute(
        "SELECT schema_name, table_name, source_warehouse, kind, n_rows, in_main, note "
        "FROM main._catalog ORDER BY schema_name, n_rows DESC, table_name"
    ).fetchall()
    schemas = con.execute("SELECT * FROM main._schemas").fetchall()
    total_rows = sum(r[4] for r in cat)

    lines: list[str] = []
    w = lines.append
    w("# Immigration data — data dictionary")
    w("")
    w(f"Single warehouse `immigration.duckdb` — **{len(cat)} objects, {total_rows:,} rows** across "
      f"{len(schemas)} provenance schemas. Generated from `main._catalog` (self-describing).")
    w("")
    w("## How to query")
    w("")
    w("```bash")
    w("duckdb immigration.duckdb \"SELECT * FROM _catalog ORDER BY n_rows DESC\"   # inventory")
    w("duckdb immigration.duckdb \"SELECT * FROM acs_origin_national_2023\"          # unqualified (main view)")
    w("duckdb immigration.duckdb \"SELECT * FROM context.safmr_zip_2025\"            # schema-qualified")
    w("duckdb immigration.duckdb \"COPY (SELECT * FROM v_three_layer_annual) TO 'out.csv'\"  # export any table")
    w("```")
    w("")
    w("Every base table is exposed unqualified in `main` for the query pack. Where a name exists "
      "in two warehouses, `main` points at the canonical copy (see notes); query the schema-qualified "
      "name (`context.x` / `lifetime.x`) for the other.")
    w("")
    w("## Schemas")
    w("")
    w("| Schema | Objects | Rows | Contents |")
    w("|--------|--------:|-----:|----------|")
    for s, n_obj, rows in schemas:
        w(f"| `{s}` | {n_obj} | {rows:,} | {SCHEMA_BLURB.get(s, '')} |")
    w("")

    # group catalog by schema
    by_schema: dict[str, list] = {}
    for r in cat:
        by_schema.setdefault(r[0], []).append(r)

    for schema in sorted(by_schema):
        w(f"## `{schema}`")
        w("")
        w(f"{SCHEMA_BLURB.get(schema, '')}")
        w("")
        for (sch, name, src, kind, n_rows, in_main, note) in by_schema[schema]:
            cols = con.execute(
                "SELECT column_name, data_type FROM duckdb_columns() "
                "WHERE schema_name=? AND table_name=? ORDER BY column_index", [sch, name]
            ).fetchall()
            flags = []
            if kind == "materialized_view":
                flags.append("materialized cross-domain view")
            if not in_main:
                flags.append("not in `main` (schema-qualify)")
            flag_str = f" — _{'; '.join(flags)}_" if flags else ""
            w(f"### `{name}`  ·  {n_rows:,} rows{flag_str}")
            if note:
                w(f"> {note}")
            w("")
            w("| Column | Type |")
            w("|--------|------|")
            for cname, ctype in cols:
                w(f"| `{cname}` | {ctype} |")
            w("")

    con.close()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"  ✓ wrote {out_path} ({len(cat)} objects documented)")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else (unified_duckdb_path().parent / "DATA_DICTIONARY.md")
    build(out)
