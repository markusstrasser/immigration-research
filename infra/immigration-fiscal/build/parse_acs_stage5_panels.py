#!/usr/bin/env python3
"""Single-pass ACS PUMS panels for stage5 (health + school-age)."""
from __future__ import annotations

from pathlib import Path

from acs_pums_io import person_csv_sql_glob
from paths import data_root, derived_root

PERSON_ZIP = data_root() / "census" / "acs_pums_2023_person.zip"
OUT = derived_root() / "stage5"


def build_acs_stage5_panels(out_dir: Path | None = None) -> tuple[int, int]:
    if not PERSON_ZIP.exists():
        return 0, 0
    import duckdb

    glob = person_csv_sql_glob()
    con = duckdb.connect()
    con.execute(f"""
        CREATE TABLE person AS
        SELECT * FROM read_csv_auto([{glob}], header=true, union_by_name=true, sample_size=-1)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE acs_immigrant_health_state_2023 AS
        SELECT
          LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
          CASE WHEN CAST(NATIVITY AS VARCHAR) = '2' THEN 'foreign_born' ELSE 'us_native' END AS nativity_group,
          CASE WHEN TRY_CAST(CIT AS INTEGER) = 5 THEN 'noncitizen' ELSE 'citizen' END AS citizenship_group,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weighted_adults,
          SUM(CASE WHEN TRY_CAST(HICOV AS INTEGER) = 2 THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS uninsured_weighted,
          SUM(CASE WHEN TRY_CAST(HICOV AS INTEGER) = 1 THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS insured_weighted,
          SUM(CASE WHEN TRY_CAST(PRIVCOV AS INTEGER) = 1 THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS private_weighted,
          SUM(CASE WHEN TRY_CAST(PUBCOV AS INTEGER) = 1 THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS public_weighted
        FROM person
        WHERE TRY_CAST(AGEP AS INTEGER) >= 19
        GROUP BY 1, 2, 3
    """)
    con.execute("""
        CREATE OR REPLACE TABLE acs_immigrant_health_state_summary_2023 AS
        SELECT
          state_fips,
          nativity_group,
          SUM(weighted_adults) AS weighted_adults,
          SUM(uninsured_weighted) / NULLIF(SUM(weighted_adults), 0) AS uninsured_rate,
          SUM(public_weighted) / NULLIF(SUM(weighted_adults), 0) AS public_coverage_rate,
          SUM(private_weighted) / NULLIF(SUM(weighted_adults), 0) AS private_coverage_rate,
          'acs_pums_2023_substitute_for_kff' AS source
        FROM acs_immigrant_health_state_2023
        GROUP BY 1, 2
    """)
    con.execute("""
        CREATE OR REPLACE TABLE acs_foreign_born_school_age_state_2023 AS
        SELECT
          LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS foreign_born_school_age_weighted,
          SUM(CASE WHEN TRY_CAST(SCH AS INTEGER) = 1 THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS foreign_born_enrolled_weighted,
          SUM(CASE WHEN TRY_CAST(ENG AS INTEGER) IN (3, 4) THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            AS foreign_born_limited_english_weighted,
          'acs_pums_2023_substitute_for_edfacts_el' AS source
        FROM person
        WHERE CAST(NATIVITY AS VARCHAR) = '2'
          AND TRY_CAST(AGEP AS INTEGER) BETWEEN 5 AND 17
        GROUP BY 1
    """)
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    health_n = con.execute("SELECT COUNT(*) FROM acs_immigrant_health_state_summary_2023").fetchone()[0]
    school_n = con.execute("SELECT COUNT(*) FROM acs_foreign_born_school_age_state_2023").fetchone()[0]
    con.execute(f"""
        COPY acs_immigrant_health_state_summary_2023
        TO '{out / "acs_immigrant_health_state_summary_2023.csv"}' (HEADER, DELIMITER ',')
    """)
    con.execute(f"""
        COPY acs_foreign_born_school_age_state_2023
        TO '{out / "acs_foreign_born_school_age_state_2023.csv"}' (HEADER, DELIMITER ',')
    """)
    print({"acs_health_state_rows": health_n, "acs_fb_school_age_state_rows": school_n}, flush=True)
    return int(health_n), int(school_n)


if __name__ == "__main__":
    build_acs_stage5_panels()
