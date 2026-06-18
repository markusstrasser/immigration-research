#!/usr/bin/env python3
"""Rebuild immigration_context.duckdb (aggregated tables only).

Uses both ACS 2023 PUMS person files (pusa+pusb) for correct national weights.
Older memos that cite pusa-only counts (~half) are superseded — see README note.

Spec: research/immigration-verified-findings-report-2026-04-10.md
      research/immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from paths import data_root, derived_root, duckdb_path

DATA = data_root()
DERIVED = derived_root()
DUCKDB_PATH = duckdb_path()
PERSON_ZIP = DATA / "census" / "acs_pums_2023_person.zip"
HH_ZIP = DATA / "census" / "acs_pums_2023_household.zip"
POBP_XLSX = DATA / "external" / "origin" / "ACSPUMS2019_2023CodeLists.xlsx"


def _require_duckdb():
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("duckdb not installed; run: uv run --with duckdb python ...", file=sys.stderr)
        sys.exit(1)


def _extract_zip_csvs(zpath: Path, prefix: str) -> list[str]:
    tmp = DERIVED / "_tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    with zipfile.ZipFile(zpath) as zf:
        names = sorted(n for n in zf.namelist() if n.lower().endswith(".csv"))
        if not names:
            raise FileNotFoundError(f"no CSV in {zpath}")
        for name in names:
            out = tmp / f"{prefix}_{name.split('/')[-1]}"
            if not out.exists() or out.stat().st_size == 0:
                out.write_bytes(zf.read(name))
            paths.append(str(out))
    return paths


def _load_pobp_dim(con) -> None:
    if not POBP_XLSX.exists():
        con.execute("""
            CREATE OR REPLACE TABLE pobp_dim AS
            SELECT DISTINCT LPAD(CAST(POBP AS VARCHAR), 4, '0') AS pobp,
                   CAST(POBP AS VARCHAR) AS origin_label
            FROM acs_person_raw WHERE POBP IS NOT NULL
        """)
        return
    import pandas as pd

    df = pd.read_excel(POBP_XLSX, sheet_name="POBP", skiprows=1)
    df = df.rename(columns={df.columns[0]: "pobp", df.columns[1]: "origin_label"})
    df = df[["pobp", "origin_label"]].dropna()
    df["pobp"] = df["pobp"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(4)
    con.register("_pobp_df", df)
    con.execute("CREATE OR REPLACE TABLE pobp_dim AS SELECT * FROM _pobp_df")


def _load_puma_rent(con, *, from_household: bool) -> None:
    if from_household:
        con.execute("""
            CREATE OR REPLACE TABLE puma_median_gross_rent_2023 AS
            SELECT
              LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
              LPAD(CAST(PUMA AS VARCHAR), 5, '0') AS puma_code,
              SUM(TRY_CAST(GRNTP AS DOUBLE) * TRY_CAST(WGTP AS DOUBLE))
                / NULLIF(SUM(TRY_CAST(WGTP AS DOUBLE)), 0) AS median_gross_rent
            FROM acs_household_raw
            WHERE TRY_CAST(GRNTP AS DOUBLE) > 0
            GROUP BY 1, 2
        """)
        return
    con.execute("""
        CREATE OR REPLACE TABLE puma_median_gross_rent_2023 (
            state_fips VARCHAR, puma_code VARCHAR, median_gross_rent DOUBLE
        )
    """)


def build() -> None:
    _require_duckdb()
    import duckdb

    if not PERSON_ZIP.exists():
        sys.exit(f"missing {PERSON_ZIP} — run bash setup.sh")

    person_csvs = _extract_zip_csvs(PERSON_ZIP, "person")
    hh_csvs = _extract_zip_csvs(HH_ZIP, "hh") if HH_ZIP.exists() else []

    if DUCKDB_PATH.exists():
        DUCKDB_PATH.unlink()

    con = duckdb.connect(str(DUCKDB_PATH))
    person_glob = ",".join(f"'{p}'" for p in person_csvs)
    con.execute(f"""
        CREATE TABLE acs_person_raw AS
        SELECT * FROM read_csv_auto([{person_glob}], header=true, union_by_name=true, sample_size=-1)
    """)
    if hh_csvs:
        hh_glob = ",".join(f"'{p}'" for p in hh_csvs)
        con.execute(f"""
            CREATE TABLE acs_household_raw AS
            SELECT * FROM read_csv_auto([{hh_glob}], header=true, union_by_name=true, sample_size=-1)
        """)

    _load_pobp_dim(con)

    # Recent low-skill foreign-born adults 25-64: NATIVITY=2, SCHL<16, YOEP>=2014
    con.execute("""
        CREATE OR REPLACE VIEW qual_person AS
        SELECT
          p.*,
          d.origin_label,
          LPAD(CAST(p.STATE AS VARCHAR), 2, '0') AS state_fips,
          LPAD(CAST(p.PUMA AS VARCHAR), 5, '0') AS puma_code
        FROM acs_person_raw p
        LEFT JOIN pobp_dim d
          ON LPAD(CAST(p.POBP AS VARCHAR), 4, '0') = d.pobp
          OR CAST(p.POBP AS VARCHAR) = TRIM(LEADING '0' FROM d.pobp)
        WHERE TRY_CAST(p.AGEP AS INTEGER) BETWEEN 25 AND 64
          AND CAST(p.NATIVITY AS VARCHAR) = '2'
          AND TRY_CAST(p.SCHL AS INTEGER) < 16
          AND TRY_CAST(p.YOEP AS INTEGER) >= 2014
          AND TRY_CAST(p.YOEP AS INTEGER) < 9999
    """)

    con.execute("""
        CREATE OR REPLACE TABLE acs_origin_national_2023 AS
        SELECT
          COALESCE(origin_label, CAST(POBP AS VARCHAR)) AS origin_label,
          CAST(POBP AS VARCHAR) AS pobp,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults
        FROM qual_person
        GROUP BY 1, 2
        ORDER BY weighted_adults DESC
    """)

    con.execute("""
        CREATE OR REPLACE TABLE acs_origin_puma_2023 AS
        SELECT
          COALESCE(origin_label, CAST(POBP AS VARCHAR)) AS origin_label,
          state_fips,
          puma_code,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults
        FROM qual_person
        GROUP BY 1, 2, 3
    """)

    _load_puma_rent(con, from_household=bool(hh_csvs))

    con.execute("""
        CREATE OR REPLACE TABLE origin_puma_context_2023 AS
        SELECT
          a.origin_label,
          a.state_fips,
          a.puma_code,
          a.weighted_adults,
          r.median_gross_rent
        FROM acs_origin_puma_2023 a
        LEFT JOIN puma_median_gross_rent_2023 r
          ON a.state_fips = r.state_fips AND a.puma_code = r.puma_code
    """)

    if hh_csvs:
        con.execute("""
            CREATE OR REPLACE TABLE hh_person_child AS
            SELECT
              SERIALNO,
              SUM(CASE WHEN TRY_CAST(AGEP AS INTEGER) BETWEEN 5 AND 17 THEN 1 ELSE 0 END) AS school_age_children,
              SUM(CASE WHEN TRY_CAST(AGEP AS INTEGER) BETWEEN 0 AND 4 THEN 1 ELSE 0 END) AS preschool_children,
              MAX(CASE WHEN TRY_CAST(AGEP AS INTEGER) BETWEEN 5 AND 17 THEN 1 ELSE 0 END) AS has_school_age
            FROM acs_person_raw
            GROUP BY SERIALNO
        """)
        con.execute("""
            CREATE OR REPLACE TABLE qual_per_serial AS
            SELECT
              SERIALNO,
              COALESCE(origin_label, CAST(POBP AS VARCHAR)) AS origin_label,
              state_fips,
              puma_code,
              COUNT(*) AS qual_adults_in_hh,
              SUM(TRY_CAST(PWGTP AS DOUBLE)) AS qual_adult_wgt
            FROM qual_person
            GROUP BY 1, 2, 3, 4
        """)
        con.execute("""
            CREATE OR REPLACE TABLE acs_origin_puma_household_2023 AS
            SELECT
              q.origin_label,
              q.state_fips,
              q.puma_code,
              q.SERIALNO,
              q.qual_adults_in_hh,
              TRY_CAST(h.WGTP AS DOUBLE) AS household_wgt,
              c.school_age_children,
              c.preschool_children,
              c.has_school_age
            FROM qual_per_serial q
            JOIN acs_household_raw h ON q.SERIALNO = h.SERIALNO
            LEFT JOIN hh_person_child c ON q.SERIALNO = c.SERIALNO
        """)
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_context_2023 AS
            SELECT
              origin_label,
              state_fips,
              puma_code,
              SUM(household_wgt / qual_adults_in_hh) AS linked_household_wgt,
              SUM((household_wgt / qual_adults_in_hh) * school_age_children)
                / NULLIF(SUM(household_wgt / qual_adults_in_hh), 0) AS linked_mean_hh_school_age_children,
              100.0 * SUM(CASE WHEN has_school_age = 1 THEN household_wgt / qual_adults_in_hh ELSE 0 END)
                / NULLIF(SUM(household_wgt / qual_adults_in_hh), 0) AS linked_share_households_with_school_age_children_pct
            FROM acs_origin_puma_household_2023
            GROUP BY 1, 2, 3
        """)
        con.execute("""
            CREATE OR REPLACE TABLE acs_origin_household_national_2023 AS
            SELECT
              origin_label,
              SUM(linked_household_wgt) AS linked_household_wgt,
              SUM(linked_mean_hh_school_age_children * linked_household_wgt)
                / NULLIF(SUM(linked_household_wgt), 0) AS linked_mean_hh_school_age_children,
              SUM(linked_share_households_with_school_age_children_pct * linked_household_wgt)
                / NULLIF(SUM(linked_household_wgt), 0) AS linked_share_households_with_school_age_children_pct
            FROM origin_puma_household_context_2023
            GROUP BY 1
        """)

        # Full-stock household context for fiscal tensor school rows.
        # Universe: all foreign-born adults 25-64, matching the ACS side of the
        # SIPP federal microsim denominator. Household child burden is allocated
        # across origin groups by qualifying adult counts within each household.
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_fullstock_context_2023 AS
            WITH full_person AS (
              SELECT
                SERIALNO,
                COALESCE(d.origin_label, CAST(p.POBP AS VARCHAR)) AS origin_label,
                LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
                LPAD(CAST(PUMA AS VARCHAR), 5, '0') AS puma_code,
                TRY_CAST(PWGTP AS DOUBLE) AS person_wgt
              FROM acs_person_raw p
              LEFT JOIN pobp_dim d
                ON LPAD(CAST(p.POBP AS VARCHAR), 4, '0') = d.pobp
                OR CAST(p.POBP AS VARCHAR) = TRIM(LEADING '0' FROM d.pobp)
              WHERE TRY_CAST(AGEP AS INTEGER) BETWEEN 25 AND 64
                AND CAST(NATIVITY AS VARCHAR) = '2'
            ),
            origin_serial AS (
              SELECT
                SERIALNO,
                origin_label,
                state_fips,
                puma_code,
                COUNT(*) AS origin_adults_in_hh,
                SUM(person_wgt) AS person_weighted_adults
              FROM full_person
              GROUP BY 1, 2, 3, 4
            ),
            serial_totals AS (
              SELECT SERIALNO, SUM(origin_adults_in_hh) AS total_fb_adults_in_hh
              FROM origin_serial
              GROUP BY 1
            ),
            linked AS (
              SELECT
                o.origin_label,
                o.state_fips,
                o.puma_code,
                o.person_weighted_adults,
                TRY_CAST(h.WGTP AS DOUBLE) * o.origin_adults_in_hh
                  / NULLIF(t.total_fb_adults_in_hh, 0) AS allocated_household_wgt,
                COALESCE(c.school_age_children, 0) AS school_age_children,
                COALESCE(c.has_school_age, 0) AS has_school_age
              FROM origin_serial o
              JOIN serial_totals t USING (SERIALNO)
              JOIN acs_household_raw h USING (SERIALNO)
              LEFT JOIN hh_person_child c USING (SERIALNO)
            )
            SELECT
              origin_label,
              state_fips,
              puma_code,
              SUM(person_weighted_adults) AS person_weighted_adults,
              SUM(allocated_household_wgt) AS linked_household_wgt,
              SUM(allocated_household_wgt * school_age_children)
                / NULLIF(SUM(allocated_household_wgt), 0) AS linked_mean_hh_school_age_children,
              100.0 * SUM(CASE WHEN has_school_age = 1 THEN allocated_household_wgt ELSE 0 END)
                / NULLIF(SUM(allocated_household_wgt), 0) AS linked_share_households_with_school_age_children_pct
            FROM linked
            GROUP BY 1, 2, 3
        """)
        con.execute("""
            CREATE OR REPLACE TABLE acs_origin_household_fullstock_national_2023 AS
            SELECT
              origin_label,
              SUM(person_weighted_adults) AS person_weighted_adults,
              SUM(linked_household_wgt) AS linked_household_wgt,
              SUM(linked_mean_hh_school_age_children * linked_household_wgt)
                / NULLIF(SUM(linked_household_wgt), 0) AS linked_mean_hh_school_age_children,
              SUM(linked_share_households_with_school_age_children_pct * linked_household_wgt)
                / NULLIF(SUM(linked_household_wgt), 0) AS linked_share_households_with_school_age_children_pct
            FROM origin_puma_household_fullstock_context_2023
            GROUP BY 1
        """)

    con.execute("""
        CREATE OR REPLACE TABLE acs_foreign_born_education_bucket_totals_2023 AS
        SELECT
          CASE
            WHEN TRY_CAST(SCHL AS INTEGER) < 16 THEN '<HS'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (16, 17) THEN 'HS / GED'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (18, 19, 20) THEN 'some college / associate'
            ELSE 'other'
          END AS education_bucket,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults
        FROM acs_person_raw
        WHERE TRY_CAST(AGEP AS INTEGER) BETWEEN 25 AND 64
          AND CAST(NATIVITY AS VARCHAR) = '2'
        GROUP BY 1
    """)

    con.execute("""
        CREATE OR REPLACE TABLE acs_nh_white_education_by_nativity_2023 AS
        SELECT
          TRY_CAST(NATIVITY AS INTEGER) AS nativity,
          CASE
            WHEN TRY_CAST(SCHL AS INTEGER) < 16 THEN '<HS'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (16, 17) THEN 'HS / GED'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (18, 19, 20) THEN 'some college / associate'
            ELSE 'other'
          END AS education_bucket,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults
        FROM acs_person_raw
        WHERE TRY_CAST(AGEP AS INTEGER) BETWEEN 25 AND 64
          AND LPAD(CAST(HISP AS VARCHAR), 2, '0') = '01'
          AND TRY_CAST(RAC1P AS INTEGER) = 1
        GROUP BY 1, 2
    """)

    con.execute("""
        CREATE OR REPLACE TABLE acs_foreign_born_education_state_shares_2023 AS
        SELECT
          LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
          CASE
            WHEN TRY_CAST(SCHL AS INTEGER) < 16 THEN '<HS'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (16, 17) THEN 'HS / GED'
            WHEN TRY_CAST(SCHL AS INTEGER) IN (18, 19, 20) THEN 'some college / associate'
            ELSE 'other'
          END AS education_bucket,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults
        FROM acs_person_raw
        WHERE TRY_CAST(AGEP AS INTEGER) BETWEEN 25 AND 64
          AND CAST(NATIVITY AS VARCHAR) = '2'
        GROUP BY 1, 2
    """)

    proto = DERIVED / "stage3_proto"
    proto.mkdir(parents=True, exist_ok=True)
    for tbl in (
        "acs_foreign_born_education_bucket_totals_2023",
        "acs_foreign_born_education_state_shares_2023",
        "acs_nh_white_education_by_nativity_2023",
    ):
        con.execute(f"COPY {tbl} TO '{proto / (tbl + '.csv')}' (HEADER, DELIMITER ',')")

    # Stage 2 county bridge (school finance, housing, IRS migration, PUMA crosswalk)
    from build_stage2_incidence_context import build_stage2, load_stage2_into_duckdb

    stage2_dir = DERIVED / "stage2"
    build_stage2(stage2_dir)
    load_stage2_into_duckdb(con, stage2_dir)

    # Stage 5 local-cost context (EL anchor, RPP, Medicaid, receiver cities)
    from build_stage5_local_cost_context import build_stage5, load_stage5_into_duckdb

    stage5_dir = DERIVED / "stage5"
    build_stage5(stage5_dir)
    load_stage5_into_duckdb(con, stage5_dir)

    # SIPP federal donor cells (replaces broken CPS HHINC prototype)
    try:
        from build_federal_microsim_sipp_2024 import build_all_donor_cells, load_federal_microsim_into_duckdb

        fb_rows, usb_rows = build_all_donor_cells()
        load_federal_microsim_into_duckdb(con, fb_rows, ebornus="2")
        load_federal_microsim_into_duckdb(con, usb_rows, ebornus="1")
        proto.mkdir(parents=True, exist_ok=True)
        import csv as _csv

        for path, rows in (
            (proto / "sipp_household_donor_cells_2024.csv", fb_rows),
            (proto / "sipp_household_donor_cells_usborn_2024.csv", usb_rows),
        ):
            with path.open("w", newline="") as f:
                w = _csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            print(f"Wrote {path} ({len(rows)} donor cells)")
    except Exception as exc:
        print(f"WARN: federal microsim skipped: {exc}", file=sys.stderr)

    keep = [
        "pobp_dim",
        "acs_origin_national_2023",
        "acs_origin_puma_2023",
        "puma_median_gross_rent_2023",
        "origin_puma_context_2023",
        "origin_puma_household_context_2023",
        "acs_origin_household_national_2023",
        "origin_puma_household_fullstock_context_2023",
        "acs_origin_household_fullstock_national_2023",
        "acs_foreign_born_education_bucket_totals_2023",
        "acs_foreign_born_education_state_shares_2023",
        "acs_nh_white_education_by_nativity_2023",
        "school_finance_county_2023",
        "chas_county_housing_stress_2018_2022",
        "irs_migration_county_2022_2023",
        "puma_county_area_xwalk_2023",
        "county_stage2_context_2023",
        "puma_county_context_2023",
        "origin_puma_household_stage2_context_2023",
        "origin_puma_household_fullstock_stage2_context_2023",
        "sipp_household_donor_cells_2024",
        "sipp_household_donor_cells_usborn_2024",
        "acs_origin_household_federal_microsim_2023",
        "acs_nh_white_federal_microsim_2023",
        "state_stage5_context_2023",
        "state_el_lep_2018",
        "receiver_city_migrant_costs",
        "origin_puma_household_stage5_context_2023",
        "origin_puma_household_fullstock_stage5_context_2023",
    ]
    slim = DUCKDB_PATH.with_suffix(".build.duckdb")
    if slim.exists():
        slim.unlink()
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"ATTACH '{slim}' AS slimdb")
    for t in keep:
        n = con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='main' AND table_name=?",
            [t],
        ).fetchone()[0]
        if n:
            con.execute(f"CREATE TABLE slimdb.{t} AS SELECT * FROM main.{t}")
    con.execute("DETACH slimdb")
    con.close()
    if DUCKDB_PATH.exists():
        DUCKDB_PATH.unlink()
    slim.rename(DUCKDB_PATH)
    # symlink for repo-relative paths in memos
    link = DERIVED / "immigration_context.duckdb"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(DUCKDB_PATH)
    size_mb = DUCKDB_PATH.stat().st_size / (1024 * 1024)
    print(f"Wrote {DUCKDB_PATH} ({size_mb:.1f} MB)")
    vcon = duckdb.connect(str(DUCKDB_PATH), read_only=False)
    _validate(vcon)
    vcon.close()


def _validate(con) -> None:
    print("\n--- validation (full US = pusa+pusb) ---")
    mex = con.execute(
        "SELECT weighted_adults FROM acs_origin_national_2023 WHERE origin_label = 'Mexico'"
    ).fetchone()
    if mex:
        val, target, tol = mex[0], 437_819, 0.03
        ok = abs(val - target) / target <= tol
        print(f"Mexico recent low-skill: {val:,.0f} (target {target:,}, {'OK' if ok else 'WARN'})")
        print("  (memo 225,180 was pusa-only — half the US)")

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'origin_puma_household_context_2023'"
    ).fetchone()[0]:
        h = con.execute("""
            SELECT SUM(linked_mean_hh_school_age_children * linked_household_wgt)
                   / NULLIF(SUM(linked_household_wgt), 0)
            FROM origin_puma_household_context_2023 WHERE origin_label = 'Honduras'
        """).fetchone()
        if h and h[0] is not None:
            val, target, tol = h[0], 1.2855, 0.15
            ok = abs(val - target) / target <= tol
            print(f"Honduras school-age/hh: {val:.4f} (pusa-only memo {target}, {'OK' if ok else 'WARN'})")

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'acs_origin_household_fullstock_national_2023'"
    ).fetchone()[0]:
        row = con.execute("""
            SELECT person_weighted_adults,
                   linked_household_wgt,
                   linked_mean_hh_school_age_children
            FROM acs_origin_household_fullstock_national_2023
            WHERE origin_label = 'Mexico'
        """).fetchone()
        if row:
            print(
                "Mexico full-stock household context: "
                f"{row[0]:,.0f} adults, {row[1]:,.0f} linked HH, {row[2]:.3f} kids/HH"
            )

    targets = {
        "<HS": 8_606_906,
        "HS / GED": 8_231_926,
        "some college / associate": 6_978_452,
    }
    buckets = con.execute("""
        SELECT education_bucket, weighted_adults
        FROM acs_foreign_born_education_bucket_totals_2023
        WHERE education_bucket IN ('<HS', 'HS / GED', 'some college / associate')
        ORDER BY education_bucket
    """).fetchall()
    for row in buckets:
        t = targets.get(row[0])
        flag = ""
        if t:
            flag = " OK" if abs(row[1] - t) / t < 0.03 else " WARN"
            print(f"  bucket {row[0]}: {row[1]:,.0f} (target ~{t:,}{flag})")
        else:
            print(f"  bucket {row[0]}: {row[1]:,.0f}")

    stage2_checks = [
        ("school_finance_county_2023", 3000),
        ("chas_county_housing_stress_2018_2022", 2500),
        ("irs_migration_county_2022_2023", 3000),
        ("puma_county_area_xwalk_2023", 14000),
        ("county_stage2_context_2023", 3000),
        ("origin_puma_household_fullstock_stage2_context_2023", 5000),
    ]
    print("\n--- stage2 ---")
    for tbl, target in stage2_checks:
        n = con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name=?", [tbl]
        ).fetchone()[0]
        if n:
            cnt = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            flag = " OK" if cnt >= target else " WARN"
            print(f"  {tbl}: {cnt:,} (target >={target:,}{flag})")


    print("\n--- stage5 ---")
    for tbl, target in [
        ("state_stage5_context_2023", 50),
        ("origin_puma_household_stage5_context_2023", 5000),
        ("origin_puma_household_fullstock_stage5_context_2023", 5000),
    ]:
        n = con.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_name=?", [tbl]
        ).fetchone()[0]
        if n:
            cnt = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            flag = " OK" if cnt >= target else " WARN"
            print(f"  {tbl}: {cnt:,} (target >={target:,}{flag})")


if __name__ == "__main__":
    build()
