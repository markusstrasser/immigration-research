#!/usr/bin/env python3
"""Stage-2 county bridge: school finance, housing stress, IRS migration, PUMA crosswalk.

Spec: research/immigration-stage2-county-bridge-batch.md
"""
from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

ROOT = data_root().parent
DATA = data_root()
DERIVED = derived_root()
STAGE2 = DERIVED / "stage2"

SCHOOL_FINANCE = DATA / "external" / "census_school_finance_2023_summary.txt"
PUMA_REL = DATA / "external" / "stage2" / "census" / "geo" / "tab20_puma520_cousub20_natl.txt"
CHAS_ZIP = DATA / "external" / "stage2" / "hud" / "chas" / "2018thru2022-140-csv.zip"
IRS_IN = DATA / "external" / "stage2" / "irs" / "countyinflow2223.csv"
IRS_OUT = DATA / "external" / "stage2" / "irs" / "countyoutflow2223.csv"
HH_ZIP = DATA / "census" / "acs_pums_2023_household.zip"


def _extract_csvs(zpath: Path) -> list[str]:
    tmp = DERIVED / "_tmp"
    tmp.mkdir(exist_ok=True)
    paths: list[str] = []
    with zipfile.ZipFile(zpath) as zf:
        for name in sorted(n for n in zf.namelist() if n.lower().endswith(".csv")):
            out = tmp / f"hh_{name.split('/')[-1]}"
            if not out.exists() or out.stat().st_size == 0:
                out.write_bytes(zf.read(name))
            paths.append(str(out))
    return paths


def _county_fips(st: str, co: str) -> str:
    return f"{int(st):02d}{int(co):03d}"


def build_puma_county_crosswalk() -> tuple[pd.DataFrame, dict]:
    rel = pd.read_csv(PUMA_REL, sep="|", dtype=str, encoding="utf-8-sig")
    rel = rel[rel["GEOID_PUMA5_20"].notna() & rel["GEOID_PUMA5_20"].str.len().gt(0)].copy()
    rel["state_fips"] = rel["GEOID_PUMA5_20"].str[:2]
    rel["puma_code"] = rel["GEOID_PUMA5_20"].str[2:].str.zfill(5)
    rel["county_fips"] = rel["GEOID_COUSUB_20"].str[:5]
    for col in ("AREALAND_PART", "AREAWATER_PART"):
        rel[col] = pd.to_numeric(rel[col], errors="coerce").fillna(0)
    rel["area_part"] = rel["AREALAND_PART"] + rel["AREAWATER_PART"]
    xwalk = (
        rel.groupby(["state_fips", "puma_code", "county_fips"], as_index=False)["area_part"]
        .sum()
        .rename(columns={"area_part": "overlap_area"})
    )
    puma_tot = xwalk.groupby(["state_fips", "puma_code"])["overlap_area"].transform("sum")
    xwalk["area_weight"] = xwalk["overlap_area"] / puma_tot.replace(0, pd.NA)
    xwalk = xwalk[xwalk["area_weight"].notna() & xwalk["area_weight"].gt(0)]
    summary = {
        "rows": int(len(xwalk)),
        "pumas": int(xwalk[["state_fips", "puma_code"]].drop_duplicates().shape[0]),
        "counties": int(xwalk["county_fips"].nunique()),
    }
    return xwalk, summary


def build_school_finance_county() -> pd.DataFrame:
    df = pd.read_csv(SCHOOL_FINANCE, dtype=str, low_memory=False)
    df["county_fips"] = df["CONUM"].str.zfill(5)
    spend_cols = ["TCURSSTA", "TCURSGEN", "TCURSSCH", "TCURSOTH", "TCURINST", "TCURSSVC", "TCURONON"]
    for c in ["ENROLL", *spend_cols]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["current_spend"] = df[spend_cols].sum(axis=1)
    # F-33 expenditure columns are thousands of dollars; ENROLL is pupil count.
    county = (
        df.groupby("county_fips", as_index=False)
        .agg(enrollment=("ENROLL", "sum"), current_spend=("current_spend", "sum"))
        .assign(
            current_spend_per_pupil=lambda d: (
                d["current_spend"] * 1000 / d["enrollment"].replace(0, pd.NA)
            )
        )
    )
    return county


def build_irs_migration_county() -> pd.DataFrame:
    inf = pd.read_csv(IRS_IN, dtype=str, encoding="latin-1")
    outf = pd.read_csv(IRS_OUT, dtype=str, encoding="latin-1")
    inf["county_fips"] = inf.apply(lambda r: _county_fips(r["y2_statefips"], r["y2_countyfips"]), axis=1)
    outf["county_fips"] = outf.apply(lambda r: _county_fips(r["y1_statefips"], r["y1_countyfips"]), axis=1)
    inf["n1"] = pd.to_numeric(inf["n1"], errors="coerce").fillna(0)
    outf["n2"] = pd.to_numeric(outf["n2"], errors="coerce").fillna(0)
    inflow = inf.groupby("county_fips", as_index=False)["n1"].sum().rename(columns={"n1": "inflow_returns"})
    outflow = outf.groupby("county_fips", as_index=False)["n2"].sum().rename(columns={"n2": "outflow_returns"})
    mig = inflow.merge(outflow, on="county_fips", how="outer").fillna(0)
    mig["net_returns"] = mig["inflow_returns"] - mig["outflow_returns"]
    denom = mig["inflow_returns"] + mig["outflow_returns"]
    mig["netflow_balance_pct"] = 100.0 * mig["net_returns"] / denom.where(denom > 0)
    return mig


def _parse_chas_table11(zip_path: Path) -> pd.DataFrame | None:
    if not zip_path.exists() or zip_path.stat().st_size < 10_240:
        return None
    with zipfile.ZipFile(zip_path) as zf:
        names = [n for n in zf.namelist() if "table11" in n.lower() and n.lower().endswith(".csv")]
        if not names:
            names = [n for n in zf.namelist() if n.lower().endswith(".csv")]
        if not names:
            return None
        raw = zf.read(names[0])
    df = pd.read_csv(BytesIO(raw), dtype=str, low_memory=False)
    cols = {c.lower(): c for c in df.columns}
    fips_col = next((cols[k] for k in cols if "fips" in k and "county" in k), None)
    if fips_col is None:
        fips_col = next((cols[k] for k in cols if k in ("geoid", "geoid10", "geoid20")), None)
    prob_col = next(
        (
            cols[k]
            for k in cols
            if "prob" in k or "problem" in k or "four" in k or "oneplus" in k.replace("_", "")
        ),
        None,
    )
    if fips_col is None or prob_col is None:
        numeric = [c for c in df.columns if pd.to_numeric(df[c], errors="coerce").notna().any()]
        if len(numeric) >= 2:
            prob_col = numeric[-1]
            fips_col = df.columns[0]
        else:
            return None
    out = pd.DataFrame(
        {
            "county_fips": df[fips_col].astype(str).str.replace(r"\D", "", regex=True).str.zfill(5),
            "share_one_plus_housing_problems_pct": pd.to_numeric(df[prob_col], errors="coerce"),
            "source": "chas_table11",
        }
    )
    return out.groupby("county_fips", as_index=False)["share_one_plus_housing_problems_pct"].mean()


def build_acs_housing_stress_proxy(xwalk: pd.DataFrame) -> pd.DataFrame:
    """ACS 2023 PUMA proxy when HUD CHAS is unavailable (WAF-blocked)."""
    import duckdb

    hh_glob = ",".join(repr(p) for p in _extract_csvs(HH_ZIP))
    con = duckdb.connect()
    con.execute(f"""
        CREATE TABLE hh AS
        SELECT * FROM read_csv_auto([{hh_glob}], header=true, union_by_name=true, sample_size=-1)
    """)
    puma = con.execute("""
        SELECT
          LPAD(CAST(STATE AS VARCHAR), 2, '0') AS state_fips,
          LPAD(CAST(PUMA AS VARCHAR), 5, '0') AS puma_code,
          100.0 * SUM(CASE
            WHEN TRY_CAST(GRPIP AS DOUBLE) >= 30
              OR TRY_CAST(NP AS DOUBLE) / NULLIF(TRY_CAST(RMSP AS DOUBLE), 0) > 1
            THEN TRY_CAST(WGTP AS DOUBLE) ELSE 0 END)
            / NULLIF(SUM(TRY_CAST(WGTP AS DOUBLE)), 0) AS share_one_plus_housing_problems_pct
        FROM hh
        GROUP BY 1, 2
    """).df()
    con.close()
    merged = xwalk.merge(puma, on=["state_fips", "puma_code"], how="left")
    merged["w_stress"] = merged["share_one_plus_housing_problems_pct"] * merged["area_weight"]
    county = (
        merged.groupby("county_fips", as_index=False)
        .agg(share_one_plus_housing_problems_pct=("w_stress", "sum"))
        .assign(source="acs_2023_puma_proxy")
    )
    return county


def build_chas_or_proxy(xwalk: pd.DataFrame) -> pd.DataFrame:
    chas = _parse_chas_table11(CHAS_ZIP)
    if chas is not None and len(chas) > 500:
        return chas.assign(source="chas_table11")
    print("WARN: CHAS zip missing — using ACS 2023 PUMA housing-stress proxy", flush=True)
    return build_acs_housing_stress_proxy(xwalk)


def load_stage2_into_duckdb(con, stage2_dir: Path) -> None:
    """Attach stage-2 CSVs and build join tables in an open duckdb connection."""
    paths = {
        "school_finance_county_2023": stage2_dir / "school_finance_county_2023.csv",
        "chas_county_housing_stress_2018_2022": stage2_dir / "chas_county_housing_stress_2018_2022.csv",
        "irs_migration_county_2022_2023": stage2_dir / "irs_migration_county_2022_2023.csv",
        "puma_county_area_xwalk_2023": stage2_dir / "puma_county_area_xwalk_2023.csv",
    }
    for table, path in paths.items():
        if path.exists():
            con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{path}', header=true)")

    con.execute("""
        CREATE OR REPLACE TABLE county_stage2_context_2023 AS
        SELECT
          COALESCE(s.county_fips, h.county_fips, m.county_fips) AS county_fips,
          s.enrollment,
          s.current_spend,
          s.current_spend_per_pupil,
          h.share_one_plus_housing_problems_pct,
          h.source AS housing_stress_source,
          m.inflow_returns,
          m.outflow_returns,
          m.net_returns,
          m.netflow_balance_pct
        FROM school_finance_county_2023 s
        FULL OUTER JOIN chas_county_housing_stress_2018_2022 h USING (county_fips)
        FULL OUTER JOIN irs_migration_county_2022_2023 m USING (county_fips)
    """)

    con.execute("""
        CREATE OR REPLACE TABLE puma_county_context_2023 AS
        SELECT
          x.state_fips,
          x.puma_code,
          x.county_fips,
          x.area_weight,
          c.current_spend_per_pupil,
          c.share_one_plus_housing_problems_pct,
          c.netflow_balance_pct
        FROM puma_county_area_xwalk_2023 x
        LEFT JOIN county_stage2_context_2023 c USING (county_fips)
    """)

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_context_2023'"
    ).fetchone()[0]:
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_stage2_context_2023 AS
            SELECT
              o.origin_label,
              o.state_fips,
              o.puma_code,
              o.linked_household_wgt,
              o.linked_mean_hh_school_age_children,
              o.linked_share_households_with_school_age_children_pct,
              SUM(p.area_weight * c.current_spend_per_pupil) AS area_wtd_current_spend_per_pupil,
              SUM(p.area_weight * c.share_one_plus_housing_problems_pct) AS area_wtd_housing_stress_pct,
              SUM(p.area_weight * c.netflow_balance_pct) AS area_wtd_netflow_balance_pct
            FROM origin_puma_household_context_2023 o
            JOIN puma_county_area_xwalk_2023 p
              ON o.state_fips = p.state_fips AND o.puma_code = p.puma_code
            LEFT JOIN county_stage2_context_2023 c ON p.county_fips = c.county_fips
            GROUP BY 1, 2, 3, 4, 5, 6
        """)

    if con.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='origin_puma_household_fullstock_context_2023'"
    ).fetchone()[0]:
        con.execute("""
            CREATE OR REPLACE TABLE origin_puma_household_fullstock_stage2_context_2023 AS
            SELECT
              o.origin_label,
              o.state_fips,
              o.puma_code,
              o.person_weighted_adults,
              o.linked_household_wgt,
              o.linked_mean_hh_school_age_children,
              o.linked_share_households_with_school_age_children_pct,
              SUM(p.area_weight * c.current_spend_per_pupil) AS area_wtd_current_spend_per_pupil,
              SUM(p.area_weight * c.share_one_plus_housing_problems_pct) AS area_wtd_housing_stress_pct,
              SUM(p.area_weight * c.netflow_balance_pct) AS area_wtd_netflow_balance_pct
            FROM origin_puma_household_fullstock_context_2023 o
            JOIN puma_county_area_xwalk_2023 p
              ON o.state_fips = p.state_fips AND o.puma_code = p.puma_code
            LEFT JOIN county_stage2_context_2023 c ON p.county_fips = c.county_fips
            GROUP BY 1, 2, 3, 4, 5, 6, 7
        """)


def build_stage2(out_dir: Path | None = None) -> dict:
    out = out_dir or STAGE2
    out.mkdir(parents=True, exist_ok=True)

    xwalk, xwalk_summary = build_puma_county_crosswalk()
    school = build_school_finance_county()
    irs = build_irs_migration_county()
    housing = build_chas_or_proxy(xwalk)

    xwalk.to_csv(out / "puma_county_area_xwalk_2023.csv", index=False)
    (out / "puma_county_area_xwalk_2023_summary.json").write_text(json.dumps(xwalk_summary, indent=2))
    school.to_csv(out / "school_finance_county_2023.csv", index=False)
    irs.to_csv(out / "irs_migration_county_2022_2023.csv", index=False)
    housing.to_csv(out / "chas_county_housing_stress_2018_2022.csv", index=False)

    meta = {
        "school_finance_county_rows": len(school),
        "chas_rows": len(housing),
        "chas_source": housing["source"].iloc[0] if len(housing) else None,
        "irs_migration_rows": len(irs),
        "puma_county_xwalk_rows": len(xwalk),
        **xwalk_summary,
    }
    (out / "stage2_outputs.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))
    return meta


if __name__ == "__main__":
    build_stage2()
