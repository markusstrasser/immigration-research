#!/usr/bin/env python3
"""ACS 2023 PUMS state health coverage by nativity/citizenship (KFF chart substitute)."""
from __future__ import annotations

import zipfile
from pathlib import Path

from paths import data_root, derived_root

PERSON_ZIP = data_root() / "census" / "acs_pums_2023_person.zip"
OUT = derived_root() / "stage5"


def build_acs_immigrant_health_state_panel(out_dir: Path | None = None) -> int:
    if not PERSON_ZIP.exists():
        return 0
    import duckdb

    tmp = derived_root() / "_tmp" / "health_person"
    tmp.mkdir(parents=True, exist_ok=True)
    csvs: list[str] = []
    with zipfile.ZipFile(PERSON_ZIP) as zf:
        for name in sorted(n for n in zf.namelist() if n.lower().endswith(".csv")):
            out = tmp / name.split("/")[-1]
            if not out.exists():
                out.write_bytes(zf.read(name))
            csvs.append(str(out))
    glob = ",".join(f"'{p}'" for p in csvs)
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
    out = out_dir or OUT
    out.mkdir(parents=True, exist_ok=True)
    n = con.execute("SELECT COUNT(*) FROM acs_immigrant_health_state_summary_2023").fetchone()[0]
    con.execute(f"""
        COPY acs_immigrant_health_state_summary_2023
        TO '{out / "acs_immigrant_health_state_summary_2023.csv"}' (HEADER, DELIMITER ',')
    """)
    print({"acs_health_state_rows": n}, flush=True)
    return int(n)


if __name__ == "__main__":
    build_acs_immigrant_health_state_panel()
