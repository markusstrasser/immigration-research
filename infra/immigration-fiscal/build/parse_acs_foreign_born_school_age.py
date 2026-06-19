#!/usr/bin/env python3
"""ACS 2023 foreign-born school-age children by state (EL fiscal pressure proxy)."""
from __future__ import annotations

from acs_pums_io import person_csv_sql_glob
from paths import data_root, derived_root

PERSON_ZIP = data_root() / "census" / "acs_pums_2023_person.zip"
OUT = derived_root() / "stage5"


def build_acs_foreign_born_school_age_panel(out_dir: Path | None = None) -> int:
    if not PERSON_ZIP.exists():
        return 0
    import duckdb

    glob = person_csv_sql_glob()
    con = duckdb.connect()
    con.execute(f"""
        CREATE TABLE person AS
        SELECT * FROM read_csv_auto([{glob}], header=true, union_by_name=true, sample_size=-1)
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
    n = con.execute("SELECT COUNT(*) FROM acs_foreign_born_school_age_state_2023").fetchone()[0]
    con.execute(f"""
        COPY acs_foreign_born_school_age_state_2023
        TO '{out / "acs_foreign_born_school_age_state_2023.csv"}' (HEADER, DELIMITER ',')
    """)
    print({"acs_fb_school_age_state_rows": n}, flush=True)
    return int(n)


if __name__ == "__main__":
    build_acs_foreign_born_school_age_panel()
