#!/usr/bin/env python3
"""Country fiscal tensor: cell × ledger × effect-order rollups (no scalar exports).

Writes tables into immigration_fiscal_union.duckdb. Requires context + lifetime DBs.
"""
from __future__ import annotations

import sys
from pathlib import Path

from paths import data_root, derived_root, duckdb_path, fiscal_union_duckdb_path, lifetime_duckdb_path

LT = data_root() / "external" / "lifetime"
PROTO = derived_root() / "stage3_proto"
UNION_PATH = fiscal_union_duckdb_path()
CTX_PATH = duckdb_path()
LIFE_PATH = lifetime_duckdb_path()

# Published anchors [SOURCE: research memos citing CBO 60569/61256]
CBO_OBJECTS = [
    ("cbo_surge_federal", "federal_annual", 3, "surge_2024_2034", -897_000_000_000, "CBO 60569 deficit reduction vs no-surge"),
    ("cbo_surge_state_local_direct", "state_local", 3, "surge_2023", 9_200_000_000, "CBO 61256 direct state/local"),
    ("cbo_surge_state_local_potential", "state_local", 3, "surge_2023", 9_800_000_000, "CBO 61256 potential net"),
]

GE_FAN = [
    ("borjas_pessimist", "<HS", 2, 0.96, -0.04, "10% supply → ~4% wage ↓ on competing cells"),
    ("card_peri_baseline", "<HS", 2, 1.02, 0.02, "Complementarity band 2000-2019"),
    ("clemens_capital_tax", "<HS", 2, None, None, "NPV sign flip via capital-tax adj — use NAS Clemens row"),
]

ANNUITY_YEARS = 75
DISCOUNT_RATES = (0.02, 0.03, 0.04)


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
    if UNION_PATH.exists():
        UNION_PATH.unlink()
    UNION_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(UNION_PATH))
    con.execute(f"ATTACH '{CTX_PATH}' AS ctx (READ_ONLY)")
    con.execute(f"ATTACH '{LIFE_PATH}' AS life (READ_ONLY)")

    # --- CBO objects ---
    con.execute(
        """
        CREATE TABLE cbo_fiscal_objects AS
        SELECT * FROM (VALUES
          ('cbo_surge_federal', 'federal_annual', 3, 'surge_2024_2034', -897000000000.0,
           'CBO 60569 cumulative federal deficit vs no-surge [SOURCE: fiscal-impact memo]'),
          ('cbo_surge_state_local_direct', 'state_local', 3, 'surge_2023', 9200000000.0,
           'CBO 61256 direct state/local [SOURCE: claims evolution ledger]'),
          ('cbo_surge_state_local_potential', 'state_local', 3, 'surge_2023', 9800000000.0,
           'CBO 61256 potential net state/local')
        ) AS t(object_id, fiscal_layer, effect_order, cohort_tag, value_usd_total, notes)
        """
    )

    # --- GE wage fan (earnings multipliers on 1st-order payroll path) ---
    con.execute(
        """
        CREATE TABLE ge_wage_fan_scenarios AS
        SELECT * FROM (VALUES
          ('borjas_pessimist', '<HS', 2, 0.96, 'wage_multiplier'),
          ('card_peri_baseline', '<HS', 2, 1.02, 'wage_multiplier'),
          ('peri_complementarity_hs', 'HS / GED', 2, 1.02, 'wage_multiplier')
        ) AS t(scenario_id, education_bucket, effect_order, earnings_multiplier, multiplier_type)
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
                 SUM(federal_net_proxy_annual * weighted_adults)
                   / NULLIF(SUM(weighted_adults), 0) AS avg_federal_annual
          FROM ctx.acs_origin_household_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL
          GROUP BY 1
        ),
        rates AS (
          SELECT r AS discount_rate FROM (VALUES {", ".join(f"({r})" for r in DISCOUNT_RATES)}) AS t(r)
        )
        SELECT
          n.education_bucket,
          n.npv_usd,
          a.avg_federal_annual,
          rt.discount_rate,
          n.npv_usd / {_annuity_factor(0.03)} AS npv_annuitized_3pct_only,
          n.npv_usd / ((1 - pow(1 + rt.discount_rate, -{ANNUITY_YEARS})) / rt.discount_rate) AS npv_annuitized,
          a.avg_federal_annual - n.npv_usd / ((1 - pow(1 + rt.discount_rate, -{ANNUITY_YEARS})) / rt.discount_rate) AS annual_gap,
          CASE
            WHEN abs(a.avg_federal_annual - n.npv_usd / ((1 - pow(1 + rt.discount_rate, -{ANNUITY_YEARS})) / rt.discount_rate)) < 500
            THEN 'near_match'
            ELSE 'scope_mismatch'
          END AS bridge_verdict
        FROM npv n
        LEFT JOIN annual a ON n.education_bucket = a.education_bucket
        CROSS JOIN rates rt
    """)

    # --- Population federal cells: FB stock, Mexico, NH white (if native table exists) ---
    has_native = con.execute("""
        SELECT COUNT(*) FROM duckdb_tables()
        WHERE database_name = 'ctx' AND table_name = 'acs_nh_white_federal_microsim_2023'
    """).fetchone()[0]

    pop_sql_parts = [
        """
        SELECT 'us_foreign_born_stock' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
        GROUP BY 1, 2
        """,
        """
        SELECT 'mexico_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL AND origin_label = 'Mexico'
        GROUP BY 1, 2
        """,
    ]
    if has_native:
        pop_sql_parts.append("""
        SELECT 'nh_white_usborn' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_nh_white_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
        GROUP BY 1, 2
        """)

    # Low-skill / cluster slices
    pop_sql_parts.extend(
        [
            """
        SELECT 'fb_lt_hs' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL AND education_bucket = '<HS'
        GROUP BY 1, 2
        """,
            """
        SELECT 'mx_ca_cluster' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
          AND origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
        GROUP BY 1, 2
        """,
            """
        SELECT 'eu27_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
          AND origin_label IN (
            'Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
            'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy',
            'Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal',
            'Romania','Slovakia','Slovenia','Spain','Sweden','Czechoslovakia','Yugoslavia'
          )
        GROUP BY 1, 2
        """,
            """
        SELECT 'uk_origin' AS population_group, education_bucket,
               SUM(weighted_adults) AS weight_adults,
               SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0),
               SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023
        WHERE donor_household_weight IS NOT NULL
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
                 SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                 SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                 SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
          FROM ctx.acs_origin_household_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL
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
                 SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                 SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                 SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
          FROM ctx.acs_nh_white_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL
          GROUP BY 1
          UNION ALL
          SELECT e.education_bucket, SUM(e.weighted_adults),
                 MAX(f.fed_net_per_adult), MAX(f.payroll_per_adult), MAX(f.transfers_per_adult)
          FROM ctx.acs_nh_white_education_by_nativity_2023 e
          JOIN (
            SELECT education_bucket,
                   SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_net_per_adult,
                   SUM(payroll_tax_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS payroll_per_adult,
                   SUM(transfer_outflow_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS transfers_per_adult
            FROM ctx.acs_origin_household_federal_microsim_2023
            WHERE donor_household_weight IS NOT NULL
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

    # --- Lifetime NPV by population (weights from ACS; NPV from NAS cells) ---
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
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.origin_label = 'Mexico' AND m.donor_household_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
        UNION ALL
        SELECT 'fb_lt_hs', m.education_bucket, SUM(m.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.education_bucket = '<HS' AND m.donor_household_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
        UNION ALL
        SELECT 'mx_ca_cluster', m.education_bucket, SUM(m.weighted_adults),
               MAX(b.individual_npv_2012_usd), MAX(b.study), MAX(b.adjustment)
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        JOIN life.npv_education_benchmarks b ON m.education_bucket = b.acs_education_bucket
        WHERE m.origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
          AND m.donor_household_weight IS NOT NULL
          AND b.study = 'NAS 2017' AND b.adjustment = 'baseline_public_goods'
          AND b.age_at_arrival = 25 AND NOT b.includes_descendants
        GROUP BY 1, 2
    """)

    # --- Local / school burden per origin (scenario ledger) ---
    con.execute("""
        CREATE TEMP TABLE _origin_school AS
        SELECT
          s.origin_label,
          m.micro_adults AS weight_adults,
          h.linked_household_wgt,
          h.linked_mean_hh_school_age_children,
          s.area_wtd_current_spend_per_pupil,
          s.avg_federal_net,
          s.area_wtd_current_spend_per_pupil * h.linked_mean_hh_school_age_children
            * h.linked_household_wgt / NULLIF(m.micro_adults, 0) AS school_burden_per_adult
        FROM life.origin_fiscal_scenario_2023 s
        JOIN ctx.acs_origin_household_national_2023 h USING (origin_label)
        JOIN (
          SELECT origin_label, SUM(weighted_adults) AS micro_adults
          FROM ctx.acs_origin_household_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL
          GROUP BY 1
        ) m USING (origin_label)
        WHERE h.linked_household_wgt > 0 AND m.micro_adults > 0
    """)

    con.execute("""
        CREATE TEMP TABLE _pop_school AS
        SELECT 'mexico_origin' AS population_group,
               SUM(weight_adults) AS weight_adults,
               SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0) AS school_per_adult,
               SUM(avg_federal_net * weight_adults) / NULLIF(SUM(weight_adults), 0) AS fed_per_adult
        FROM _origin_school WHERE origin_label = 'Mexico'
        UNION ALL
        SELECT 'eu27_origin',
               SUM(weight_adults),
               SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0),
               SUM(avg_federal_net * weight_adults) / NULLIF(SUM(weight_adults), 0)
        FROM _origin_school
        WHERE origin_label IN (
          'Austria','Belgium','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark',
          'Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy',
          'Latvia','Lithuania','Luxembourg','Malta','Netherlands','Poland','Portugal',
          'Romania','Slovakia','Slovenia','Spain','Sweden','Czechoslovakia','Yugoslavia'
        )
        UNION ALL
        SELECT 'uk_origin', SUM(weight_adults),
               SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0),
               SUM(avg_federal_net * weight_adults) / NULLIF(SUM(weight_adults), 0)
        FROM _origin_school
        WHERE origin_label IN (
          'United Kingdom, not specified','England','Scotland','Northern Ireland','Wales'
        )
        UNION ALL
        SELECT 'mx_ca_cluster', SUM(weight_adults),
               SUM(school_burden_per_adult * weight_adults) / NULLIF(SUM(weight_adults), 0),
               SUM(avg_federal_net * weight_adults) / NULLIF(SUM(weight_adults), 0)
        FROM _origin_school
        WHERE origin_label IN ('Mexico', 'El Salvador', 'Guatemala', 'Honduras')
        UNION ALL
        SELECT 'fb_lt_hs',
               SUM(m.weighted_adults),
               SUM(s.school_burden_per_adult * m.weighted_adults) / NULLIF(SUM(m.weighted_adults), 0),
               SUM(m.federal_net_proxy_annual * m.weighted_adults) / NULLIF(SUM(m.weighted_adults), 0)
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        JOIN _origin_school s ON m.origin_label = s.origin_label
        WHERE m.donor_household_weight IS NOT NULL AND m.education_bucket = '<HS'
    """)

    # --- Local flow: per-pupil from scenario (Mexico + FB weighted via origins) ---
    con.execute("""
        CREATE TEMP TABLE _local_flow AS
        SELECT 'mexico_origin' AS population_group,
               weighted_adults AS weight_adults,
               area_wtd_current_spend_per_pupil AS local_per_pupil_annual,
               linked_mean_hh_school_age_children AS school_age_children_per_hh
        FROM life.origin_fiscal_scenario_2023
        WHERE origin_label = 'Mexico'
    """)

    # --- Assemble country_fiscal_tensor ---
    con.execute("""
        CREATE TABLE country_fiscal_tensor AS
        SELECT population_group, education_bucket, fiscal_layer, effect_order,
               weight_adults, value_per_adult, value_total_usd, unit, source_ref, notes
        FROM (
          SELECT population_group, education_bucket, 'federal_annual' AS fiscal_layer, 1 AS effect_order,
                 weight_adults, fed_net_per_adult AS value_per_adult,
                 weight_adults * fed_net_per_adult AS value_total_usd,
                 'USD_per_adult_per_year' AS unit,
                 'acs_origin_household_federal_microsim_2023' AS source_ref,
                 'SIPP donor payroll − SNAP/TANF/SSI' AS notes
          FROM _pop_fed
          UNION ALL
          SELECT population_group, education_bucket, 'lifetime_npv', 1, weight_adults, npv_per_adult,
                 weight_adults * npv_per_adult, 'USD_npv_per_adult', study || '/' || adjustment, 'NAS education cell'
          FROM _pop_npv WHERE adjustment = 'baseline_public_goods'
          UNION ALL
          SELECT population_group, education_bucket, 'lifetime_npv', 2, weight_adults, npv_per_adult,
                 weight_adults * npv_per_adult, 'USD_npv_per_adult', study, 'GE capital-tax overlay'
          FROM _pop_npv WHERE adjustment = 'capital_tax_adjustment'
          UNION ALL
          SELECT population_group, NULL, 'local_flow', 1, weight_adults,
                 local_per_pupil_annual, weight_adults * local_per_pupil_annual,
                 'USD_per_pupil_current', 'origin_fiscal_scenario_2023',
                 'Area-weighted F-33; not marginal immigrant pupil'
          FROM _local_flow
        ) u
    """)

    # --- School burden per adult + crude net (federal − school); NOT lifetime NPV ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT population_group, NULL AS education_bucket,
               'school_burden_per_adult' AS fiscal_layer, 1 AS effect_order,
               weight_adults, school_per_adult AS value_per_adult,
               weight_adults * school_per_adult AS value_total_usd,
               'USD_per_adult_per_year' AS unit,
               'origin_fiscal_scenario_2023' AS source_ref,
               'per_pupil × school_age_kids/HH ÷ adults/HH; average not marginal; citizen children in HH' AS notes
        FROM _pop_school
        UNION ALL
        SELECT population_group, NULL,
               'net_crude_federal_minus_school', 1,
               weight_adults, fed_per_adult - school_per_adult,
               weight_adults * (fed_per_adult - school_per_adult),
               'USD_per_adult_per_year', 'derived_crude',
               'CRUDE static: federal proxy minus average school burden; no descendant taxes; not NAS lifetime'
        FROM _pop_school
    """)

    # --- GE fan applied to Mexico <HS federal annual (2nd order) ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT
          'mexico_origin' AS population_group,
          g.education_bucket,
          'federal_annual' AS fiscal_layer,
          2 AS effect_order,
          p.weight_adults,
          p.fed_net_per_adult * g.earnings_multiplier AS value_per_adult,
          p.weight_adults * p.fed_net_per_adult * g.earnings_multiplier AS value_total_usd,
          'USD_per_adult_per_year' AS unit,
          g.scenario_id AS source_ref,
          'Payroll path scaled by GE wage fan' AS notes
        FROM _pop_fed p
        JOIN ge_wage_fan_scenarios g ON p.education_bucket = g.education_bucket
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

    # --- Episodic local (3rd order): receiver cities FY2024 ---
    con.execute("""
        INSERT INTO country_fiscal_tensor
        SELECT 'receiver_cities_episodic', NULL, 'local_episodic', 3, NULL, NULL,
               SUM(TRY_CAST(total_spending_usd_M AS DOUBLE)) * 1e6,
               'USD_total', 'receiver_city_migrant_costs', 'Gross city shelter/asylum FY rows'
        FROM life.receiver_city_migrant_costs
        WHERE fiscal_year IN ('FY2024', '2024')
    """)

    # --- NH white school burden (ACS household linkage if person CSVs staged) ---
    acs_a = Path("/tmp/acs_person_psam_pusa.csv")
    acs_b = Path("/tmp/acs_person_psam_pusb.csv")
    if acs_a.exists() and acs_b.exists():
        county_pupil = con.execute("""
            SELECT MEDIAN(current_spend_per_pupil) FROM life.school_finance_county_2023
            WHERE current_spend_per_pupil IS NOT NULL AND current_spend_per_pupil > 1000
        """).fetchone()[0]
        nh = con.execute(f"""
            WITH persons AS (
              SELECT SERIALNO, CAST(PWGTP AS DOUBLE) w, CAST(AGEP AS INT) age,
                (LPAD(CAST(HISP AS VARCHAR),2,'0')='01' AND CAST(RAC1P AS INT)=1) nh,
                CAST(NATIVITY AS INT) nativity
              FROM read_csv_auto('{acs_a}', header=true)
              UNION ALL
              SELECT SERIALNO, CAST(PWGTP AS DOUBLE), CAST(AGEP AS INT),
                (LPAD(CAST(HISP AS VARCHAR),2,'0')='01' AND CAST(RAC1P AS INT)=1),
                CAST(NATIVITY AS INT)
              FROM read_csv_auto('{acs_b}', header=true)
            ),
            hh AS (
              SELECT SERIALNO,
                MAX(CASE WHEN nh AND age BETWEEN 25 AND 64 THEN w ELSE 0 END) adult_w,
                SUM(CASE WHEN nh AND age BETWEEN 25 AND 64 THEN w ELSE 0 END) adult_w_sum,
                SUM(CASE WHEN age BETWEEN 5 AND 17 THEN w ELSE 0 END) kid_w
              FROM persons GROUP BY 1
              HAVING adult_w_sum > 0
            ),
            nat AS (
              SELECT p.SERIALNO, MAX(p.nativity) AS nativity, SUM(CASE WHEN p.nh AND p.age BETWEEN 25 AND 64 THEN p.w ELSE 0 END) w
              FROM persons p WHERE p.nh AND p.age BETWEEN 25 AND 64 GROUP BY 1
            ),
            roll AS (
              SELECT n.nativity,
                SUM(n.w) adults,
                SUM(h.kid_w * n.w / NULLIF(h.adult_w_sum, 0)) kids_adj
              FROM nat n JOIN hh h ON n.SERIALNO = h.SERIALNO
              GROUP BY 1
            )
            SELECT nativity, adults, kids_adj / NULLIF(adults, 0) AS kids_per_adult FROM roll
        """).fetchall()
        fed_usb = con.execute("""
            SELECT SUM(federal_net_proxy_annual*weighted_adults)/SUM(weighted_adults)
            FROM ctx.acs_nh_white_federal_microsim_2023 WHERE donor_household_weight IS NOT NULL
        """).fetchone()[0]
        fed_fb = con.execute("""
            SELECT SUM(federal_net_proxy_annual*weighted_adults)/SUM(weighted_adults)
            FROM ctx.acs_origin_household_federal_microsim_2023 WHERE donor_household_weight IS NOT NULL
        """).fetchone()[0]
        for nativity, adults, kids_per_adult in nh:
            if not kids_per_adult or not adults:
                continue
            school = county_pupil * kids_per_adult
            fed = fed_usb if nativity == 1 else fed_fb
            grp = "nh_white_usborn" if nativity == 1 else "nh_white_fborn"
            con.execute(
                """
                INSERT INTO country_fiscal_tensor VALUES
                (?, NULL, 'school_burden_per_adult', 1, ?, ?, ?, 'USD_per_adult_per_year',
                 'acs_hh_linkage_county_median_pupil', ?),
                (?, NULL, 'net_crude_federal_minus_school', 1, ?, ?, ?, 'USD_per_adult_per_year',
                 'derived_crude', ?)
                """,
                [
                    grp, adults, school, adults * school,
                    f"median county per_pupil ${county_pupil:,.0f} × {kids_per_adult:.3f} kids/adult",
                    grp, adults, fed - school, adults * (fed - school),
                    "CRUDE NH white: federal minus school; FB white uses FB donor cells",
                ],
            )
        all_adults = sum(r[1] for r in nh)
        all_kids = sum(r[1] * r[2] for r in nh)
        if all_adults:
            kpa = all_kids / all_adults
            school_all = county_pupil * kpa
            fed_w = sum((fed_usb if r[0] == 1 else fed_fb) * r[1] for r in nh) / all_adults
            con.execute(
                """
                INSERT INTO country_fiscal_tensor VALUES
                ('nh_white_all', NULL, 'school_burden_per_adult', 1, ?, ?, ?, 'USD_per_adult_per_year',
                 'acs_hh_linkage_county_median_pupil', ?),
                ('nh_white_all', NULL, 'net_crude_federal_minus_school', 1, ?, ?, ?, 'USD_per_adult_per_year',
                 'derived_crude', ?)
                """,
                [
                    all_adults, school_all, all_adults * school_all,
                    f"all NH white kids/adult={kpa:.3f}",
                    all_adults, fed_w - school_all, all_adults * (fed_w - school_all),
                    "CRUDE NH white all nativity",
                ],
            )
            print(f"NH white school burden: kids/adult={kpa:.3f}, school/adult=${school_all:,.0f}")
    else:
        print("WARN: ACS person CSVs not in /tmp — nh_white school_burden skipped", file=sys.stderr)

    # --- Rollup view ---
    con.execute("""
        CREATE VIEW v_country_fiscal_rollup AS
        SELECT population_group, fiscal_layer, effect_order,
               SUM(weight_adults) AS weight_adults,
               SUM(value_total_usd) / NULLIF(SUM(weight_adults), 0) AS value_per_adult_weighted,
               SUM(value_total_usd) AS value_total_usd,
               COUNT(*) AS n_cells
        FROM country_fiscal_tensor
        WHERE weight_adults IS NOT NULL AND value_per_adult IS NOT NULL
        GROUP BY 1, 2, 3
        UNION ALL
        SELECT population_group, fiscal_layer, effect_order,
               NULL, NULL, SUM(value_total_usd), COUNT(*)
        FROM country_fiscal_tensor
        WHERE value_per_adult IS NULL AND value_total_usd IS NOT NULL
        GROUP BY 1, 2, 3
    """)

    con.execute("""
        CREATE VIEW v_country_fiscal_compare AS
        SELECT
          a.population_group AS group_a,
          b.population_group AS group_b,
          a.fiscal_layer,
          a.effect_order,
          a.value_per_adult_weighted AS per_adult_a,
          b.value_per_adult_weighted AS per_adult_b,
          a.value_per_adult_weighted / NULLIF(b.value_per_adult_weighted, 0) AS ratio_a_to_b,
          a.value_total_usd AS total_a,
          b.value_total_usd AS total_b
        FROM v_country_fiscal_rollup a
        JOIN v_country_fiscal_rollup b
          ON a.fiscal_layer = b.fiscal_layer AND a.effect_order = b.effect_order
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
        CREATE TABLE education_matched_federal AS
        WITH white AS (
          SELECT education_bucket,
                 SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_white,
                 SUM(weighted_adults) AS n_white
          FROM ctx.acs_nh_white_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL
          GROUP BY 1
        ),
        mex AS (
          SELECT education_bucket,
                 SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed_mex,
                 SUM(weighted_adults) AS n_mex
          FROM ctx.acs_origin_household_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL AND origin_label = 'Mexico'
          GROUP BY 1
        ),
        fb_lt AS (
          SELECT SUM(federal_net_proxy_annual * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS fed
          FROM ctx.acs_origin_household_federal_microsim_2023
          WHERE donor_household_weight IS NOT NULL AND education_bucket = '<HS'
        )
        SELECT
          w.education_bucket,
          w.n_white,
          m.n_mex,
          w.fed_white,
          m.fed_mex,
          CASE WHEN w.education_bucket = '<HS' THEN (SELECT fed FROM fb_lt) ELSE w.fed_white END AS fed_white_adj,
          m.fed_mex / NULLIF(
            CASE WHEN w.education_bucket = '<HS' THEN (SELECT fed FROM fb_lt) ELSE w.fed_white END, 0
          ) AS ratio_mex_to_white_adj,
          CASE
            WHEN w.education_bucket = '<HS' THEN 'white_lt_hs_sipp_noise_use_fb_donor'
            WHEN m.fed_mex > w.fed_white THEN 'mex_higher'
            ELSE 'white_higher'
          END AS cell_verdict
        FROM white w
        JOIN mex m USING (education_bucket)
        WHERE m.n_mex > 100000
    """)
    con.execute("""
        CREATE VIEW v_education_matched_federal AS SELECT * FROM education_matched_federal
    """)

    con.execute("""
        CREATE VIEW v_three_layer_annual AS
        SELECT
          population_group,
          MAX(CASE WHEN fiscal_layer = 'federal_annual' THEN value_per_adult_weighted END) AS federal_per_adult,
          MAX(CASE WHEN fiscal_layer = 'school_burden_per_adult' THEN value_per_adult_weighted END) AS school_per_adult,
          MAX(CASE WHEN fiscal_layer = 'net_crude_federal_minus_school' THEN value_per_adult_weighted END) AS net_crude_per_adult,
          MAX(CASE WHEN fiscal_layer = 'federal_annual' THEN weight_adults END) AS weight_adults
        FROM v_country_fiscal_rollup
        WHERE effect_order = 1
          AND fiscal_layer IN ('federal_annual', 'school_burden_per_adult', 'net_crude_federal_minus_school')
        GROUP BY 1
        HAVING MAX(CASE WHEN fiscal_layer = 'federal_annual' THEN value_per_adult_weighted END) IS NOT NULL
    """)

    lpr_n = _load_lpr_mexico_weights(con)

    # Legacy cross-domain views
    con.execute("""
        CREATE VIEW v_education_stock_with_npv AS
        SELECT e.education_bucket, e.weighted_adults, b.study, b.individual_npv_2012_usd,
               b.adjustment, b.notes AS npv_notes
        FROM ctx.acs_foreign_born_education_bucket_totals_2023 e
        LEFT JOIN life.npv_education_benchmarks b ON e.education_bucket = b.acs_education_bucket
    """)
    con.execute("""
        CREATE VIEW v_origin_federal_with_education_npv AS
        SELECT m.origin_label, m.education_bucket, m.weighted_adults, m.federal_net_proxy_annual,
               b.study AS npv_study, b.individual_npv_2012_usd, b.adjustment AS npv_adjustment
        FROM ctx.acs_origin_household_federal_microsim_2023 m
        LEFT JOIN life.npv_education_benchmarks b
          ON m.education_bucket = b.acs_education_bucket AND b.age_at_arrival = 25
          AND b.adjustment IN ('baseline_public_goods', 'capital_tax_adjustment')
    """)
    con.execute("""
        CREATE VIEW v_mexico_scenario_npv_band AS
        SELECT s.origin_label, s.weighted_adults, s.avg_federal_net, s.area_wtd_current_spend_per_pupil,
               b.study, b.acs_education_bucket, b.individual_npv_2012_usd, b.adjustment
        FROM life.origin_fiscal_scenario_2023 s
        CROSS JOIN life.npv_education_benchmarks b
        WHERE s.origin_label = 'Mexico' AND b.acs_education_bucket = '<HS'
          AND b.adjustment IN ('baseline_public_goods', 'capital_tax_adjustment')
    """)
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

    print(f"Wrote {UNION_PATH} ({UNION_PATH.stat().st_size} bytes)")
    print(f"  country_fiscal_tensor rows: {tensor_n}")
    print(f"  lpr_mexico_row_sketch rows: {lpr_n}")
    print(f"  exported {out_csv}")
    print(f"  exported {three_layer_csv}")
    for v in views:
        print(f"  {v[0]}")


if __name__ == "__main__":
    build()
