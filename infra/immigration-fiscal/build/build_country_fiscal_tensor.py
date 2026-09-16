#!/usr/bin/env python3
"""Country fiscal tensor: cell × ledger × effect-order rollups (no scalar exports).

Writes tables into immigration_fiscal_union.duckdb. Requires context + lifetime DBs.
"""
from __future__ import annotations

import sys
from pathlib import Path

from paths import (
    commit_output,
    data_root,
    derived_root,
    duckdb_path,
    fiscal_union_duckdb_path,
    lifetime_duckdb_path,
    staged_output,
)

LT = data_root() / "external" / "lifetime"
PROTO = derived_root() / "stage3_proto"
UNION_PATH = fiscal_union_duckdb_path()
CTX_PATH = duckdb_path()
LIFE_PATH = lifetime_duckdb_path()

# Published budget changes; a negative deficit change is a budget improvement.
# https://www.cbo.gov/publication/60165 (July 2024), report 61256 (June 2025).
CBO_OBJECTS = [
    ("cbo_surge_federal", "federal_cumulative_2024_2034", 3, "surge_2024_2034", -897_000_000_000, "CBO 60165 cumulative 2024-2034 federal deficit change; negative means deficit reduction"),
    ("cbo_surge_state_local_direct", "state_local", 3, "surge_2023", 9_200_000_000, "CBO 61256 direct state/local"),
    ("cbo_surge_state_local_potential", "state_local", 3, "surge_2023", 9_800_000_000, "CBO 61256 potential net"),
]

ANNUITY_YEARS = 75
DISCOUNT_RATES = (0.02, 0.03, 0.04)

# Czechoslovakia maps wholly to EU members; Yugoslavia spans EU/non-EU successors.
# Share the same observed birthplace coverage between payroll and school scenarios.
EU27_ACS_ORIGINS = (
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark',
    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy',
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal',
    'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Czechoslovakia',
)
EU27_ORIGINS_SQL = ", ".join(f"'{origin}'" for origin in EU27_ACS_ORIGINS)


def _require_duckdb():
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("duckdb not installed", file=sys.stderr)
        sys.exit(1)


def _annuity_factor(rate: float, years: int = ANNUITY_YEARS) -> float:
    if rate <= 0:
        return float(years)
    return (1 - (1 + rate) ** (-years)) / rate


def _load_lpr_mexico_weights(con) -> int:
    import pandas as pd

    xlsx = LT / "dhs" / "plcy_lpr_by_country_of_birth_fy2005_2022.xlsx"
    rows: list[dict] = []
    if xlsx.exists():
        try:
            df = pd.read_excel(xlsx, sheet_name=0, header=None)
            for _, row in df.iterrows():
                text = " ".join(str(x) for x in row.values if pd.notna(x))
                if "mexico" not in text.lower():
                    continue
                nums = [float(x) for x in row.values if isinstance(x, (int, float)) and x > 0]
                if nums:
                    rows.append({"raw_row": text[:120], "row_sum": sum(nums)})
        except Exception as exc:
            print(f"WARN: LPR xlsx skipped: {exc}", file=sys.stderr)
    out = pd.DataFrame(rows or [{"raw_row": "[UNVERIFIED: LPR xlsx missing]", "row_sum": None}])
    con.register("_lpr_mex", out)
    con.execute("CREATE OR REPLACE TABLE lpr_mexico_row_sketch AS SELECT * FROM _lpr_mex")
    return len(rows)


def build() -> None:
    _require_duckdb()
    import duckdb
    import pandas as pd

    if not CTX_PATH.exists():
        sys.exit(f"missing {CTX_PATH}")
    if not LIFE_PATH.exists():
        sys.exit(f"missing {LIFE_PATH}")

    PROTO.mkdir(parents=True, exist_ok=True)
    tmp = staged_output(UNION_PATH)

    con = duckdb.connect(str(tmp))
    con.execute(f"ATTACH '{CTX_PATH}' AS ctx (READ_ONLY)")
    con.execute(f"ATTACH '{LIFE_PATH}' AS life (READ_ONLY)")

    # --- CBO objects ---
    con.execute(
        """
        CREATE TABLE cbo_fiscal_objects (
          object_id VARCHAR, fiscal_layer VARCHAR, effect_order INTEGER,
          cohort_tag VARCHAR, value_usd_total DOUBLE, notes VARCHAR
        )
        """
    )
    con.executemany("INSERT INTO cbo_fiscal_objects VALUES (?, ?, ?, ?, ?, ?)", CBO_OBJECTS)

    # Illustrative payroll multipliers, not estimates of equilibrium wage effects.
    con.execute(
        """
        CREATE TABLE mechanical_payroll_multiplier_scenarios AS
        SELECT * FROM (VALUES
          ('illustrative_payroll_minus4pct', '<HS', 2, 0.96, 'payroll_multiplier'),
          ('illustrative_payroll_plus2pct', '<HS', 2, 1.02, 'payroll_multiplier'),
          ('illustrative_hs_payroll_plus2pct', 'HS / GED', 2, 1.02, 'payroll_multiplier')
        ) AS t(scenario_id, education_bucket, effect_order, payroll_multiplier, multiplier_type)
        """
    )

    # --- Annual ↔ NPV bridge grid ---
    con.execute(f"""
        CREATE TABLE annual_npv_bridge_grid AS
        WITH npv AS (
          SELECT acs_education_bucket AS education_bucket, individual_npv_2012_usd AS npv_usd
          FROM life.npv_education_benchmarks
          WHERE study = 'NAS 2017' AND adjustment = 'baseline_public_goods'
            AND age_at_arrival = 25 AND NOT includes_descendants
        ),
        annual AS (
          SELECT education_bucket,
                 SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults)
                   / NULLIF(SUM(weighted_adults), 0) AS avg_payroll_transfer_annual
          FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
          WHERE donor_person_weight IS NOT NULL
          GROUP BY 1
        ),
        rates AS (
          SELECT r AS discount_rate FROM (VALUES {", ".join(f"({r})" for r in DISCOUNT_RATES)}) AS t(r)
        )
        SELECT
          n.education_bucket,
          n.npv_usd AS nas_age25_lifetime_npv_2012_usd,
          2012 AS nas_price_year,
          'USD_2012_per_age25_arrival_lifetime' AS nas_unit,
          a.avg_payroll_transfer_annual AS current_stock_payroll_transfer_2023_usd,
          2023 AS payroll_transfer_price_year,
          'USD_2023_per_current_adult_year' AS payroll_transfer_unit,
          rt.discount_rate,
          {ANNUITY_YEARS} AS illustrative_annuity_years,
          n.npv_usd / ((1 - pow(1 + rt.discount_rate, -{ANNUITY_YEARS})) / rt.discount_rate) AS nas_constant_annuity_2012_usd,
          'not_comparable_without_scope_and_price_alignment' AS comparison_status,
          'NAS arrival-cohort lifetime all-government ledger versus current-stock employee payroll and selected transfers; annuity is a level-payment illustration, not an observed annual flow' AS scope_notes
        FROM npv n
        LEFT JOIN annual a ON n.education_bucket = a.education_bucket
        CROSS JOIN rates rt
    """)

    # --- Population federal cells: FB stock, Mexico, NH white (if native table exists) ---
    has_native = con.execute("""
        SELECT COUNT(*) FROM duckdb_tables()
        WHERE database_name = 'ctx' AND table_name = 'acs_nh_white_person_payroll_transfer_microsim_2023'
    """).fetchone()[0]

    pop_sql_parts = [
        """
        SELECT 'us_foreign_born_stock' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL
        GROUP BY 1, 2
        """,
        """
        SELECT 'mexico_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL AND origin_label = 'Mexico'
        GROUP BY 1, 2
        """,
    ]
    if has_native:
        pop_sql_parts.append("""
        SELECT 'nh_white_usborn' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_nh_white_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL
        GROUP BY 1, 2
        """)

    # Low-skill / cluster slices
    pop_sql_parts.extend(
        [
            """
        SELECT 'fb_lt_hs' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL AND education_bucket = '<HS'
        GROUP BY 1, 2
        """,
            """
        SELECT 'mx_ca_cluster' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL
          AND origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
        GROUP BY 1, 2
        """,
            f"""
        SELECT 'eu27_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL
          AND origin_label IN ({EU27_ORIGINS_SQL})
        GROUP BY 1, 2
        """,
            """
        SELECT 'uk_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
        WHERE donor_person_weight IS NOT NULL
          AND origin_label IN (
            'United Kingdom, not specified','England','Scotland','Northern Ireland','Wales'
          )
        GROUP BY 1, 2
        """,
        ]
    )

    has_nh_nat = con.execute("""
        SELECT COUNT(*) FROM duckdb_tables()
        WHERE database_name = 'ctx' AND table_name = 'acs_nh_white_education_by_nativity_2023'
    """).fetchone()[0]
    if has_nh_nat:
        pop_sql_parts.extend(
            [
                """
        SELECT 'nh_white_fborn' AS population_group, e.education_bucket,
               SUM(e.weighted_adults) AS weight_adults,
               MAX(f.fed_net_per_adult) AS fed_net_per_adult,
               MAX(f.payroll_per_adult) AS payroll_per_adult,
               MAX(f.transfers_per_adult) AS transfers_per_adult
        FROM ctx.acs_nh_white_education_by_nativity_2023 e
        JOIN (
          SELECT education_bucket,
                 SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                 SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                 SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
          FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
          WHERE donor_person_weight IS NOT NULL
          GROUP BY 1
        ) f ON e.education_bucket = f.education_bucket
        WHERE e.nativity = 2
        GROUP BY 1, 2
        """,
                """
        SELECT 'nh_white_all' AS population_group, education_bucket,
               SUM(weight_adults) AS weight_adults,
               SUM(fed_net_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0),
               SUM(payroll_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0),
               SUM(transfers_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0)
        FROM (
          SELECT education_bucket, SUM(weighted_adults) AS weight_adults,
                 SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                 SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                 SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
          FROM ctx.acs_nh_white_person_payroll_transfer_microsim_2023
          WHERE donor_person_weight IS NOT NULL
          GROUP BY 1
          UNION ALL
          SELECT e.education_bucket, SUM(e.weighted_adults),
                 MAX(f.fed_net_per_adult), MAX(f.payroll_per_adult), MAX(f.transfers_per_adult)
          FROM ctx.acs_nh_white_education_by_nativity_2023 e
          JOIN (
            SELECT education_bucket,
                   SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                   SUM(employee_oasdi_hi_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                   SUM(allocated_snap_tanf_ssi_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
            FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
            WHERE donor_person_weight IS NOT NULL
            GROUP BY 1
          ) f ON e.education_bucket = f.education_bucket
          WHERE e.nativity = 2
          GROUP BY 1
        ) u
        GROUP BY 1, 2
        """,
            ]
        )
    else:
        print(
            "WARN: acs_nh_white_education_by_nativity_2023 missing — nh_white_all/fborn skipped",
            file=sys.stderr,
        )

    con.execute(
        "CREATE TEMP TABLE _pop_fed AS " + " UNION ALL ".join(pop_sql_parts)
    )
    con.execute("""
        CREATE TEMP TABLE _pop_fed_rollup AS
        SELECT population_group,
               SUM(weight_adults) AS weight_adults,
               SUM(fed_net_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0) AS fed_per_adult
        FROM _pop_fed
        GROUP BY 1
    """)

    # --- Synthetic age-25 NPV benchmarks by population (ACS weights; NAS cells) ---
    con.execute("""
        CREATE TEMP TABLE _pop_npv AS
        SELECT 'us_foreign_born_stock' AS population_group, e.education_bucket,
               SUM(e.weighted_adults) AS weight_adults,
               MAX(b.individual_npv_2012_usd) AS npv_per_adult,
               MAX(b.study) AS study, MAX(b.adjustment) AS adjustment
        FROM ctx.acs_foreign_born_education_bucket_totals_2023 e
        JOIN life.npv_education_benchmarks b ON e.education_bucket = b.acs_education_bucket
        WHERE b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
        UNION ALL
        SELECT 'us_foreign_born_stock', e.education_bucket, SUM(e.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_foreign_born_education_bucket_totals_2023 e
        JOIN life.npv_education_benchmarks b ON e.education_bucket = b.acs_education_bucket
        WHERE b.study = 'Clemens 2023' AND b.adjustment = 'capital_tax_adjustment' AND b.age_at_arrival = 25
        GROUP BY 1, 2
        UNION ALL
        SELECT 'mexico_origin', m.education_bucket,
               SUM(m.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.origin_label = 'Mexico' AND m.donor_person_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
        UNION ALL
        SELECT 'fb_lt_hs', m.education_bucket, SUM(m.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.education_bucket = '<HS' AND m.donor_person_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
        UNION ALL
        SELECT 'mx_ca_cluster', m.education_bucket, SUM(m.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_origin_person_payroll_transfer_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
          AND m.donor_person_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
    """)

    # --- Local / school burden per origin (full-stock same-universe ACS household linkage) ---
    school_table = None
    for candidate in (
        "origin_puma_household_fullstock_stage5_context_2023",
        "origin_puma_household_fullstock_stage2_context_2023",
    ):
        exists = con.execute(
            """
            SELECT COUNT(*) FROM duckdb_tables()
            WHERE database_name = 'ctx' AND table_name = ?
            """,
            [candidate],
        ).fetchone()[0]
        if exists:
            school_table = candidate
            break

    if school_table:
        con.execute(f"""
            CREATE TEMP TABLE _origin_school AS
            WITH origin_school AS (
              SELECT
                origin_label,
                SUM(person_weighted_adults) AS school_person_adults,
                SUM(linked_household_wgt) AS linked_household_wgt,
                SUM(linked_mean_hh_school_age_children * linked_household_wgt)
                  AS allocated_school_age_children,
                SUM(CASE WHEN area_wtd_current_spend_per_pupil IS NOT NULL
                         THEN linked_household_wgt ELSE 0 END)
                  / NULLIF(SUM(linked_household_wgt), 0) AS spend_coverage,
                SUM(area_wtd_current_spend_per_pupil
                    * linked_mean_hh_school_age_children
                    * linked_household_wgt) AS school_cost_numerator
              FROM ctx.{school_table}
              GROUP BY 1
            ),
            micro AS (
              SELECT origin_label, SUM(weighted_adults) AS micro_adults
              FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
              WHERE donor_person_weight IS NOT NULL
              GROUP BY 1
            )
            SELECT
              o.origin_label,
              m.micro_adults AS weight_adults,
              o.school_person_adults,
              o.linked_household_wgt,
              o.allocated_school_age_children,
              o.spend_coverage,
              CASE
                WHEN ABS(m.micro_adults - o.school_person_adults) <= 0.05 * m.micro_adults
                 AND o.spend_coverage >= 0.95
                THEN o.school_cost_numerator / NULLIF(m.micro_adults, 0)
                ELSE NULL
              END AS school_burden_per_adult
            FROM origin_school o
            JOIN micro m USING (origin_label)
            WHERE o.linked_household_wgt > 0 AND m.micro_adults > 0
        """)
    else:
        con.execute("""
            CREATE TEMP TABLE _origin_school (
              origin_label VARCHAR,
              weight_adults DOUBLE,
              school_person_adults DOUBLE,
              linked_household_wgt DOUBLE,
              allocated_school_age_children DOUBLE,
              spend_coverage DOUBLE,
              school_burden_per_adult DOUBLE
            )
        """)

    con.execute(f"""
        CREATE TEMP TABLE _pop_school AS
        SELECT 'mexico_origin' AS population_group,
               SUM(weight_adults) AS weight_adults,
               CASE WHEN COUNT(*) = COUNT(school_burden_per_adult)
                    THEN SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0)
                    ELSE NULL
               END AS school_per_adult
        FROM _origin_school WHERE origin_label = 'Mexico'
        UNION ALL
        SELECT 'eu27_origin',
               SUM(weight_adults),
               CASE WHEN COUNT(*) = COUNT(school_burden_per_adult)
                    THEN SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0)
                    ELSE NULL
               END
        FROM _origin_school
        WHERE origin_label IN ({EU27_ORIGINS_SQL})
        UNION ALL
        SELECT 'uk_origin', SUM(weight_adults),
               CASE WHEN COUNT(*) = COUNT(school_burden_per_adult)
                    THEN SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0)
                    ELSE NULL
               END
        FROM _origin_school
        WHERE origin_label IN (
          'United Kingdom, not specified','England','Scotland','Northern Ireland','Wales'
        )
        UNION ALL
        SELECT 'mx_ca_cluster', SUM(weight_adults),
               CASE WHEN COUNT(*) = COUNT(school_burden_per_adult)
                    THEN SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0)
                    ELSE NULL
               END
        FROM _origin_school
        WHERE origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
    """)

    # --- Assemble country_fiscal_tensor ---
    con.execute("""
        CREATE TABLE country_fiscal_tensor AS
        SELECT population_group, education_bucket, fiscal_layer, effect_order,
               weight_adults, value_per_adult, value_total_usd, unit, source_ref, notes
        FROM (
          SELECT population_group, education_bucket, 'payroll_transfer_annual' AS fiscal_layer, 1 AS effect_order,
                 weight_adults, fed_net_per_adult AS value_per_adult,
                 weight_adults * fed_net_per_adult AS value_total_usd,
                 'USD_per_adult_per_year' AS unit,
                 CASE WHEN population_group = 'nh_white_usborn'
                      THEN 'acs_nh_white_person_payroll_transfer_microsim_2023'
                      ELSE 'acs_origin_person_payroll_transfer_microsim_2023'
                 END AS source_ref,
                 'Person-year employee OASDI/HI proxy minus allocated SNAP/TANF and individual SSI; adult-only selected ledger, not federal net revenue' ||
                 CASE WHEN population_group IN ('nh_white_fborn', 'nh_white_all')
                      THEN '; Foreign-born-white component assumes the all-FB ACS mean within education, without matching its age/income distribution; compositional scenario only'
                      WHEN population_group = 'nh_white_usborn'
                      THEN '; Assumes all-US-born SIPP donor means transport to native-white recipients conditional on age, income and education'
                      ELSE '; Assumes all-FB SIPP donor means transport to each origin conditional on age, income and education'
                 END AS notes
          FROM _pop_fed
          UNION ALL
          SELECT population_group, education_bucket, 'lifetime_npv', 1, weight_adults, npv_per_adult,
                 weight_adults * npv_per_adult, 'USD_npv_per_adult', study || '/' || adjustment,
                 'Synthetic age-at-arrival-25 NPV benchmark applied to current ACS stock education weights; not actual current-stock lifetime NPV'
          FROM _pop_npv WHERE adjustment = 'baseline_public_goods'
          UNION ALL
          SELECT population_group, education_bucket, 'lifetime_npv', 2, weight_adults, npv_per_adult,
                 weight_adults * npv_per_adult, 'USD_npv_per_adult', study,
                 'Partial-equilibrium capital-tax adjustment on synthetic age-at-arrival-25 NPV benchmark; not an estimated GE effect'
          FROM _pop_npv WHERE adjustment = 'capital_tax_adjustment'
        ) u
    """)

    # --- Household school exposure and explicit crude scenario arithmetic ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT population_group, NULL AS education_bucket,
               'school_burden_per_adult' AS fiscal_layer, 1 AS effect_order,
               weight_adults, school_per_adult AS value_per_adult,
               weight_adults * school_per_adult AS value_total_usd,
               'USD_per_adult_per_year' AS unit,
               'origin_puma_household_fullstock_context_2023' AS source_ref,
               'Exposure scenario: every household child age 5-17 treated as a public pupil; entire household exposure allocated across FB adults 25-64 by origin, including mixed-nativity households. Average pupil cost can be above or below marginal cost.' AS notes
        FROM _pop_school
        UNION ALL
        SELECT population_group, NULL,
               'crude_payroll_transfer_minus_school', 1,
               ps.weight_adults, pf.fed_per_adult - ps.school_per_adult,
               ps.weight_adults * (pf.fed_per_adult - ps.school_per_adult),
               'USD_per_adult_per_year', 'derived_crude',
               'Scenario arithmetic: adult employee payroll/selected-benefit proxy minus allocated household child school exposure; not actual spending, full fiscal impact or NAS lifetime; no descendant taxes'
        FROM _pop_school ps
        JOIN _pop_fed_rollup pf USING (population_group)
    """)

    # Mechanical payroll scenarios with fixed transfers; no causal GE claim.
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT
          'mexico_origin' AS population_group,
          g.education_bucket,
          'payroll_transfer_annual' AS fiscal_layer,
          2 AS effect_order,
          p.weight_adults,
          p.payroll_per_adult * g.payroll_multiplier - p.transfers_per_adult AS value_per_adult,
          p.weight_adults * (p.payroll_per_adult * g.payroll_multiplier - p.transfers_per_adult) AS value_total_usd,
          'USD_per_adult_per_year' AS unit,
          g.scenario_id AS source_ref,
          'Mechanical payroll multiplier with fixed transfers; not estimated GE or exact wage-response tax liability under payroll caps' AS notes
        FROM _pop_fed p
        JOIN mechanical_payroll_multiplier_scenarios g ON p.education_bucket = g.education_bucket
        WHERE p.population_group = 'mexico_origin'
    """)

    # --- CBO surge objects (3rd order, country-level not per-cell) ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT 'cbo_surge_cohort' AS population_group, NULL AS education_bucket,
               fiscal_layer, effect_order, NULL AS weight_adults,
               NULL AS value_per_adult, value_usd_total AS value_total_usd,
               'USD_total' AS unit, object_id AS source_ref, notes
        FROM cbo_fiscal_objects
    """)

    # --- Selected city/state episodic costs (3rd order), mixed FY2024 records ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT 'receiver_cities_episodic', NULL, 'local_episodic', 3, NULL, NULL,
               SUM(TRY_CAST(total_spending_usd_M AS DOUBLE)) * 1e6,
               'USD_total', 'receiver_city_migrant_costs',
               'Selected city/state gross shelter/asylum amounts; mixed budgets and actuals, not a national total or net attributable fiscal cost'
        FROM life.receiver_city_migrant_costs
        WHERE fiscal_year IN ('FY2024', '2024')
    """)
    print("Native school/net withheld: no validated population-comparable exposure construction")

    # --- Rollup view ---
    con.execute("""
        CREATE VIEW v_country_fiscal_rollup AS
        WITH scoped AS (
          SELECT *, CASE
            WHEN population_group = 'cbo_surge_cohort'
              OR (fiscal_layer = 'payroll_transfer_annual' AND effect_order = 2)
              THEN source_ref ELSE 'baseline' END AS scenario_id
          FROM country_fiscal_tensor
        )
        SELECT population_group, fiscal_layer, effect_order, scenario_id, unit,
               SUM(weight_adults) AS weight_adults,
               SUM(value_total_usd) / NULLIF(SUM(weight_adults), 0) AS value_per_adult_weighted,
               SUM(value_total_usd) AS value_total_usd,
               COUNT(*) AS n_cells
        FROM scoped
        WHERE weight_adults IS NOT NULL AND value_per_adult IS NOT NULL
        GROUP BY 1, 2, 3, 4, 5
        UNION ALL
        SELECT population_group, fiscal_layer, effect_order, scenario_id, unit,
               NULL, NULL, SUM(value_total_usd), COUNT(*)
        FROM scoped
        WHERE value_per_adult IS NULL AND value_total_usd IS NOT NULL
        GROUP BY 1, 2, 3, 4, 5
    """)

    con.execute("""
        CREATE VIEW v_country_fiscal_compare AS
        SELECT
          a.population_group AS group_a,
          b.population_group AS group_b,
          a.fiscal_layer,
          a.effect_order,
          a.scenario_id,
          a.unit,
          a.value_per_adult_weighted AS per_adult_a,
          b.value_per_adult_weighted AS per_adult_b,
          a.value_per_adult_weighted / NULLIF(b.value_per_adult_weighted, 0) AS ratio_a_to_b,
          a.value_total_usd AS total_a,
          b.value_total_usd AS total_b
        FROM v_country_fiscal_rollup a
        JOIN v_country_fiscal_rollup b
          ON a.fiscal_layer = b.fiscal_layer AND a.effect_order = b.effect_order
          AND a.scenario_id = b.scenario_id AND a.unit = b.unit
        WHERE (a.population_group, b.population_group) IN (
          ('nh_white_usborn', 'mexico_origin'),
          ('nh_white_all', 'fb_lt_hs'),
          ('nh_white_all', 'mexico_origin'),
          ('nh_white_fborn', 'nh_white_usborn'),
          ('eu27_origin', 'mexico_origin'),
          ('eu27_origin', 'nh_white_usborn'),
          ('uk_origin', 'nh_white_usborn')
        )
    """)

    con.execute("""
        CREATE TABLE education_matched_payroll_transfer AS
        WITH white AS (
          SELECT education_bucket,
                 SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_transfer_white,
                 SUM(weighted_adults) AS n_white
          FROM ctx.acs_nh_white_person_payroll_transfer_microsim_2023
          WHERE donor_person_weight IS NOT NULL
          GROUP BY 1
        ),
        mex AS (
          SELECT education_bucket,
                 SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_transfer_mex,
                 SUM(weighted_adults) AS n_mex
          FROM ctx.acs_origin_person_payroll_transfer_microsim_2023
          WHERE donor_person_weight IS NOT NULL AND origin_label = 'Mexico'
          GROUP BY 1
        )
        SELECT
          w.education_bucket,
          w.n_white,
          m.n_mex,
          w.payroll_transfer_white,
          m.payroll_transfer_mex,
          'Descriptive conditional transport: all-US-born and all-FB SIPP donor pools respectively; not ethnicity-specific observations or a causal comparison; no survey uncertainty estimated' AS comparison_notes
        FROM white w
        JOIN mex m USING (education_bucket)
    """)
    con.execute("""
        CREATE VIEW v_education_matched_payroll_transfer AS SELECT * FROM education_matched_payroll_transfer
    """)

    con.execute("""
        UPDATE country_fiscal_tensor
        SET notes = notes || '; EU coverage excludes ambiguous Yugoslavia birthplace; includes Czechoslovakia, whose successors are both EU members'
        WHERE population_group = 'eu27_origin'
    """)

    con.execute("""
        CREATE VIEW v_three_layer_annual AS
        SELECT
          population_group,
          MAX(CASE WHEN fiscal_layer = 'payroll_transfer_annual' THEN value_per_adult_weighted END) AS payroll_transfer_per_adult,
          MAX(CASE WHEN fiscal_layer = 'school_burden_per_adult' THEN value_per_adult_weighted END) AS school_per_adult,
          MAX(CASE WHEN fiscal_layer = 'crude_payroll_transfer_minus_school' THEN value_per_adult_weighted END) AS net_crude_per_adult,
          MAX(CASE WHEN fiscal_layer = 'payroll_transfer_annual' THEN weight_adults END) AS weight_adults
        FROM v_country_fiscal_rollup
        WHERE effect_order = 1
          AND fiscal_layer IN ('payroll_transfer_annual', 'school_burden_per_adult', 'crude_payroll_transfer_minus_school')
        GROUP BY 1
        HAVING MAX(CASE WHEN fiscal_layer = 'payroll_transfer_annual' THEN value_per_adult_weighted END) IS NOT NULL
    """)

    lpr_n = _load_lpr_mexico_weights(con)

    from build_fiscal_union_views import create_common_views
    create_common_views(con)
    try:
        con.execute("CREATE VIEW v_gould_episodic_ledger AS SELECT * FROM life.v_gould_episodic_ledger")
    except Exception as exc:
        print(f"WARN: v_gould_episodic_ledger skipped: {exc}", file=sys.stderr)
    con.execute("""
        CREATE VIEW v_country_fiscal_tensor AS SELECT * FROM country_fiscal_tensor
    """)

    # Export rollup CSV
    rollup = con.execute("SELECT * FROM v_country_fiscal_rollup ORDER BY 1, 2, 3").df()
    out_csv = PROTO / "country_fiscal_rollup_2023.csv"
    rollup.to_csv(out_csv, index=False)

    bridge = con.execute("SELECT * FROM annual_npv_bridge_grid ORDER BY 1, 3").df()
    bridge.to_csv(PROTO / "annual_npv_bridge_grid.csv", index=False)

    three_layer = con.execute("SELECT * FROM v_three_layer_annual ORDER BY 1").df()
    three_layer_csv = PROTO / "three_layer_annual_2023.csv"
    three_layer.to_csv(three_layer_csv, index=False)

    tensor_n = con.execute("SELECT COUNT(*) FROM country_fiscal_tensor").fetchone()[0]
    views = con.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='main'"
    ).fetchall()
    con.close()
    commit_output(tmp, UNION_PATH)

    print(f"Wrote {UNION_PATH} ({UNION_PATH.stat().st_size} bytes)")
    print(f"  country_fiscal_tensor rows: {tensor_n}")
    print(f"  lpr_mexico_row_sketch rows: {lpr_n}")
    print(f"  exported {out_csv}")
    print(f"  exported {three_layer_csv}")
    for v in views:
        print(f"  {v[0]}")


if __name__ == "__main__":
    build()
