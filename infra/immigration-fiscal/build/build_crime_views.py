#!/usr/bin/env python3
"""Crime-domain cross-views — JOIN the crime layer to the fiscal layer (INT-03+).

Creates views in the context warehouse (flow into the unified release) that wire the
newly-represented crime tables to the existing fiscal/state-local context. Currently:

  v_crime_scaap_x_state_fiscal  — SCAAP criminal-alien incarceration burden ($ + inmate-days)
                                  joined to state immigrant-cost context (Medicaid/SNAP/EL/RPP)
                                  on state_fips. The one admin line connecting crime ↔ fiscal.
  v_status_class_sources        — the INT-06 spine as a query-ready harmonization reference
                                  (every status-keyed crime join loads this, never re-maps).

Extend here as INT-01/02/04/05 crime nodes are ingested. Run after parse_scaap_awards.py +
build_status_crosswalk.py. Skips any view whose inputs are absent.

Run: uv run --with duckdb python build_crime_views.py
"""
from __future__ import annotations

import sys

from paths import duckdb_path


def build() -> None:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python build_crime_views.py")

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build context first")
    con = duckdb.connect(str(db))

    have = {r[0] for r in con.execute("SELECT table_name FROM duckdb_tables()").fetchall()}
    made = []

    # INT-03 — SCAAP criminal-alien burden × state immigrant-cost context
    if {"crime_scaap_state_2023", "state_stage5_context_2023"} <= have:
        con.execute("""
            CREATE OR REPLACE VIEW v_crime_scaap_x_state_fiscal AS
            SELECT s.state_fips,
                   f.state_name,
                   s.criminal_alien_inmate_days,
                   s.unknown_status_days,
                   s.total_inmate_days,
                   s.scaap_award_usd,
                   round(s.criminal_alien_inmate_days
                         / nullif(s.total_inmate_days, 0), 4)      AS criminal_alien_share_of_days,
                   round(s.scaap_award_usd
                         / nullif(s.criminal_alien_inmate_days, 0), 2) AS award_per_criminal_alien_day,
                   f.medicaid_total_computable,
                   f.snap_benefits_usd,
                   f.lep_count_reported,
                   f.rpp_all_items_2023
            FROM crime_scaap_state_2023 s
            LEFT JOIN state_stage5_context_2023 f USING (state_fips)
            ORDER BY s.criminal_alien_inmate_days DESC NULLS LAST
        """)
        made.append("v_crime_scaap_x_state_fiscal")

    # INT-01 — Light TX crime rate by status, expressed as a ratio to the native-born rate
    if "crime_tx_arrests_by_status" in have:
        con.execute("""
            CREATE OR REPLACE VIEW v_crime_tx_status_ratio AS
            WITH nat AS (
                SELECT year, crime_category, denom_source, crime_rate_per_100k AS citizen_rate_per_100k
                FROM crime_tx_arrests_by_status WHERE status_class = 'native_born'
            )
            SELECT b.year, b.crime_category, b.denom_source,
                   b.light_status, b.status_class,
                   b.crime_rate_per_100k, n.citizen_rate_per_100k,
                   round(b.crime_rate_per_100k / nullif(n.citizen_rate_per_100k, 0), 3) AS rate_vs_citizen
            FROM crime_tx_arrests_by_status b
            JOIN nat n USING (year, crime_category, denom_source)
            WHERE b.status_class <> 'native_born'
            ORDER BY b.year DESC, b.crime_category, b.status_class
        """)
        made.append("v_crime_tx_status_ratio")

        # SPECIFICATION CURVE / multiverse — the undocumented-vs-comparator rate ratio across
        # EVERY defensible analytic choice (denom_source × comparator class × offense × year).
        # Makes the red-team's "the headline depends on which construction" a measured DISTRIBUTION,
        # not a caveat: how often, and by how much, is undocumented crime below the comparator —
        # and in exactly which specifications is it NOT (the robustness-breakers)?
        con.execute("""
            CREATE OR REPLACE VIEW v_crime_spec_curve AS
            WITH undoc AS (
                SELECT year, crime_category, denom_source, crime_rate_per_100k AS undoc_rate
                FROM crime_tx_arrests_by_status WHERE status_class = 'unauthorized'
            ), comp AS (
                SELECT year, crime_category, denom_source,
                       status_class AS comparator_class, crime_rate_per_100k AS comp_rate
                FROM crime_tx_arrests_by_status WHERE status_class <> 'unauthorized'
            )
            SELECT u.denom_source, c.comparator_class, u.crime_category, u.year,
                   round(u.undoc_rate, 1) AS undoc_rate_per_100k,
                   round(c.comp_rate, 1)  AS comparator_rate_per_100k,
                   round(u.undoc_rate / nullif(c.comp_rate, 0), 3) AS undoc_vs_comparator,
                   (u.undoc_rate < c.comp_rate) AS undoc_lower
            FROM undoc u JOIN comp c USING (year, crime_category, denom_source)
            ORDER BY undoc_vs_comparator DESC
        """)
        made.append("v_crime_spec_curve")

    # INT-06 — status harmonization spine, query-ready (canonical class joined to source mappings)
    if {"status_class_crosswalk", "status_class_def"} <= have:
        con.execute("""
            CREATE OR REPLACE VIEW v_status_class_sources AS
            SELECT x.source, x.native_code, x.native_label,
                   x.status_class, d.nativity_rollup, d.is_citizen,
                   x.lossy_flag, x.verified, x.note
            FROM status_class_crosswalk x
            JOIN status_class_def d USING (status_class)
            ORDER BY x.source, x.native_code
        """)
        made.append("v_status_class_sources")

    if not made:
        print("  ! no crime views built — inputs missing (run parse_scaap_awards + build_status_crosswalk)")
        con.close()
        return

    # validate the headline join
    if "v_crime_scaap_x_state_fiscal" in made:
        n, joined = con.execute(
            "SELECT count(*), count(medicaid_total_computable) FROM v_crime_scaap_x_state_fiscal").fetchone()
        print(f"  ✓ v_crime_scaap_x_state_fiscal: {n} states ({joined} matched to fiscal context)")
        top = con.execute("""SELECT state_name, criminal_alien_share_of_days, scaap_award_usd
                             FROM v_crime_scaap_x_state_fiscal
                             WHERE state_name IS NOT NULL LIMIT 3""").fetchall()
        for sn, sh, aw in top:
            print(f"      {sn}: {sh:.1%} of inmate-days criminal-alien, ${aw:,.0f} SCAAP")
    if "v_status_class_sources" in made:
        print(f"  ✓ v_status_class_sources: status spine query-ready")
    if "v_crime_spec_curve" in made:
        n, lower, med, mx = con.execute("""
            SELECT count(*), sum(CASE WHEN undoc_lower THEN 1 ELSE 0 END),
                   round(median(undoc_vs_comparator), 3), round(max(undoc_vs_comparator), 3)
            FROM v_crime_spec_curve""").fetchone()
        print(f"  ✓ v_crime_spec_curve: {n} specifications (denom × comparator × offense × year)")
        print(f"      undocumented BELOW comparator in {lower}/{n} ({lower/n:.0%}); "
              f"median ratio {med}, worst-case {mx}")
        breakers = con.execute(
            "SELECT denom_source, comparator_class, crime_category, year, undoc_vs_comparator "
            "FROM v_crime_spec_curve WHERE NOT undoc_lower ORDER BY undoc_vs_comparator DESC LIMIT 6").fetchall()
        if breakers:
            print(f"      robustness-breakers (undoc ≥ comparator):")
            for d, cc, cat, y, r in breakers:
                print(f"        {r:>5} — {cat}/{y} vs {cc} ({d})")
        else:
            print("      no robustness-breakers — undocumented below EVERY comparator in EVERY spec")
    con.close()


if __name__ == "__main__":
    build()
