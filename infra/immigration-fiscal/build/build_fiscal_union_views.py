#!/usr/bin/env python3
"""Thin query shell: ATTACH context + lifetime DuckDBs; expose cross-domain views."""
from __future__ import annotations

import sys
from pathlib import Path

from paths import duckdb_path, fiscal_union_duckdb_path, lifetime_duckdb_path

UNION_PATH = fiscal_union_duckdb_path()
CTX_PATH = duckdb_path()
LIFE_PATH = lifetime_duckdb_path()


def _require_duckdb():
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("duckdb not installed", file=sys.stderr)
        sys.exit(1)


def build() -> None:
    _require_duckdb()
    import duckdb

    if not CTX_PATH.exists():
        sys.exit(f"missing {CTX_PATH} — run build-context.sh first")
    if not LIFE_PATH.exists():
        sys.exit(f"missing {LIFE_PATH} — run build-lifetime.sh first")

    if UNION_PATH.exists():
        UNION_PATH.unlink()
    UNION_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(UNION_PATH))
    con.execute(f"ATTACH '{CTX_PATH}' AS ctx (READ_ONLY)")
    con.execute(f"ATTACH '{LIFE_PATH}' AS life (READ_ONLY)")

    con.execute("""
        CREATE VIEW v_education_stock_with_npv AS
        SELECT
          e.education_bucket,
          e.weighted_adults,
          b.study,
          b.individual_npv_2012_usd,
          b.adjustment,
          b.notes AS npv_notes
        FROM ctx.acs_foreign_born_education_bucket_totals_2023 e
        LEFT JOIN life.npv_education_benchmarks b
          ON e.education_bucket = b.acs_education_bucket
    """)

    con.execute("""
        CREATE VIEW v_origin_federal_with_education_npv AS
        SELECT
          m.origin_label,
          m.education_bucket,
          m.weighted_adults,
          m.federal_net_proxy_annual,
          b.study AS npv_study,
          b.individual_npv_2012_usd,
          b.adjustment AS npv_adjustment
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        LEFT JOIN life.npv_education_benchmarks b
          ON m.education_bucket = b.acs_education_bucket
          AND b.age_at_arrival = 25
          AND b.adjustment IN ('baseline_public_goods', 'capital_tax_adjustment')
    """)

    con.execute("""
        CREATE VIEW v_lifetime_sources_by_topic AS
        SELECT t.topic, COUNT(*) AS n_sources,
               list_slice(list(rel_path ORDER BY rel_path), 1, 5) AS sample_paths
        FROM life.source_catalog c
        JOIN life.source_topic_tags t ON c.source_id = t.source_id
        WHERE c.exists
        GROUP BY 1
        ORDER BY n_sources DESC
    """)

    con.execute("""
        CREATE VIEW v_bridge_keys AS
        SELECT * FROM life.bridge_dimensions
    """)

    con.execute("""
        CREATE VIEW v_mexico_scenario_npv_band AS
        SELECT
          s.origin_label,
          s.weighted_adults,
          s.avg_federal_net,
          s.area_wtd_current_spend_per_pupil,
          s.area_wtd_housing_stress_pct,
          b.study,
          b.acs_education_bucket,
          b.individual_npv_2012_usd,
          b.adjustment
        FROM life.origin_fiscal_scenario_2023 s
        CROSS JOIN life.npv_education_benchmarks b
        WHERE s.origin_label = 'Mexico'
          AND b.acs_education_bucket = '<HS'
          AND b.adjustment IN ('baseline_public_goods', 'capital_tax_adjustment')
    """)

    views = con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main' AND table_type='VIEW'"
    ).fetchall()
    con.close()
    print(f"Wrote {UNION_PATH} ({UNION_PATH.stat().st_size} bytes, {len(views)} views)")
    for v in views:
        print(f"  view {v[0]}")


if __name__ == "__main__":
    build()
