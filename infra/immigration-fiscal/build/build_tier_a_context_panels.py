#!/usr/bin/env python3
"""Stage Tier A #4-6 panels: OECD SOCX, Docquier/Razin-Wahba, UN WPP, ACS labor cells."""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

from paths import data_root, derived_root, duckdb_path

DATA = data_root()
DERIVED = derived_root()
OUT = DERIVED / "stage6"
OECD_JSON = DATA / "external" / "oecd" / "socx_agg_pct_gdp_1980_1995.json"
UN_LOC = DATA / "external" / "un_wpp" / "locations.json"
PERSON_ZIP = DATA / "census" / "acs_pums_2023_person.zip"

# Razin-Wahba Table 1 [SOURCE: corpus sha_15b1f196f1207bc6 Table 1]
RAZIN_T1 = [
    ("Austria", "EUR", 47.5, 12.7, 24.10),
    ("Belgium", "EUR", 65.7, 18.3, 25.18),
    ("Denmark", "EUR", 44.8, 17.3, 25.51),
    ("Finland", "EUR", 48.7, 23.8, 23.96),
    ("France", "EUR", 74.6, 16.4, 25.03),
    ("Germany", "EUR", 65.9, 21.8, 23.28),
    ("Greece", "EUR", 44.5, 15.0, 15.01),
    ("Ireland", "EUR", 13.6, 41.1, 17.14),
    ("Italy", "EUR", 52.9, 15.4, 19.66),
    ("Netherlands", "EUR", 50.2, 22.0, 24.88),
    ("Norway", "EUR", 22.0, 28.7, 20.05),
    ("Portugal", "EUR", 59.7, 18.6, 12.25),
    ("Spain", "EUR", 28.7, 18.5, 18.67),
    ("Sweden", "EUR", 34.1, 25.7, 29.73),
    ("Switzerland", "EUR", 54.9, 18.6, 14.85),
    ("UK", "EUR", 34.1, 34.9, 18.16),
    ("Australia", "RESTRICTED", 35.3, 40.3, 12.93),
    ("Canada", "RESTRICTED", 29.6, 58.8, 16.91),
    ("USA", "RESTRICTED", 37.9, 42.7, 17.50),
]

# Table 2 skill-diff by host × source regime [SOURCE: corpus Table 2]
RAZIN_T2 = [
    ("Sweden", "EUR", -30.62, 28.80, 5124),
    ("Sweden", "non_EUR_DC", 4.32, 28.80, 5124),
    ("Sweden", "LDC", 67.67, 28.80, 5124),
    ("Netherlands", "EUR", -3.89, 25.40, 3767),
    ("Netherlands", "non_EUR_DC", 6.38, 25.40, 3767),
    ("Netherlands", "LDC", 49.32, 25.40, 3767),
    ("UK", "EUR", 36.81, 18.23, 1567),
    ("UK", "non_EUR_DC", 70.03, 18.23, 1567),
    ("UK", "LDC", 91.74, 18.23, 1567),
    ("Spain", "EUR", 47.91, 17.47, 1475),
    ("Spain", "non_EUR_DC", 68.86, 17.47, 1475),
    ("Spain", "LDC", 63.69, 17.47, 1475),
    ("EUR", "EUR", 15.77, 20.56, 3072),
    ("EUR", "non_EUR_DC", 59.36, 20.56, 3072),
    ("EUR", "LDC", 65.60, 20.56, 3072),
]

HANSON_ORIGINS = ("MEX", "SLV", "GTM", "HND", "DOM", "COL", "PER", "ECU", "NIC", "CRI", "PAN", "BRA", "ARG", "CHL", "URY", "PRY", "BOL", "VEN", "CUB", "HTI", "JAM")


def _write_razin_tables() -> None:
    import pandas as pd

    OUT.mkdir(parents=True, exist_ok=True)
    t1 = pd.DataFrame(
        RAZIN_T1,
        columns=[
            "host_country",
            "mobility_regime",
            "low_edu_share_immigration_2000",
            "high_edu_share_immigration_2000",
            "socx_pct_gdp_avg_1980_1995",
        ],
    )
    t1["source"] = "razin_wahba_w17515_table1"
    t1.to_csv(OUT / "razin_wahba_host_immigration_socx_2000.csv", index=False)

    t2 = pd.DataFrame(
        RAZIN_T2,
        columns=[
            "host_country",
            "source_regime",
            "skill_diff_migration_rate_2000_pct",
            "socx_pct_gdp_avg_1980_1990",
            "socx_per_capita_ppp_usd_1974_1990",
        ],
    )
    t2["mobility_regime_free"] = t2["source_regime"].eq("EUR")
    t2["source"] = "razin_wahba_w17515_table2_docquier_derived"
    t2.to_csv(OUT / "bilateral_migration_skill_panel.csv", index=False)
    print(f"Wrote Razin-Wahba tables ({len(t1)} hosts, {len(t2)} host×regime rows)")


def _parse_oecd_socx() -> None:
    import pandas as pd

    if not OECD_JSON.exists():
        print("WARN: skip OECD parse — no JSON", file=sys.stderr)
        return
    try:
        d = json.loads(OECD_JSON.read_text())
    except json.JSONDecodeError as exc:
        print(f"WARN: OECD JSON invalid: {exc}", file=sys.stderr)
        return
    struct = d["data"]["structures"][0]
    sd = struct["dimensions"]["series"]
    od = struct["dimensions"]["observation"]
    ids = [x["id"] for x in sd]
    ui, ri = ids.index("UNIT_MEASURE"), ids.index("REF_AREA")
    rows: list[dict] = []
    for sk, s in d["data"]["dataSets"][0]["series"].items():
        idx = [int(x) for x in sk.split(":")]
        if sd[ui]["values"][idx[ui]]["id"] != "PT_B1GQ":
            continue
        country = sd[ri]["values"][idx[ri]]["id"]
        for ok, val in s.get("observations", {}).items():
            year = int(od[0]["values"][int(ok)]["id"])
            rows.append({"country_code": country, "year": year, "socx_pct_gdp": val[0]})
    if not rows:
        print("WARN: OECD parse yielded 0 rows", file=sys.stderr)
        return
    df = pd.DataFrame(rows)
    avg = (
        df[df["year"].between(1980, 1995)]
        .groupby("country_code", as_index=False)["socx_pct_gdp"]
        .mean()
        .rename(columns={"socx_pct_gdp": "socx_pct_gdp_avg_1980_1995"})
    )
    avg["source"] = "oecd_socx_agg_sdmx"
    avg.to_csv(OUT / "oecd_social_spending_host.csv", index=False)
    print(f"Wrote oecd_social_spending_host.csv ({len(avg)} countries)")


def _un_location_map() -> dict[str, int]:
    if not UN_LOC.exists():
        return {}
    d = json.loads(UN_LOC.read_text())
    items = d.get("data", d) if isinstance(d, dict) else []
    return {x["iso3"]: x["id"] for x in items if x.get("iso3")}


def _extend_population_projections(df) -> "pd.DataFrame":
    """Extend OWID historical population to 2040 via 2010–2023 log trend [INFERENCE]."""
    import math
    import pandas as pd

    out = [df]
    for iso3, g in df.groupby("iso3"):
        g = g.sort_values("year")
        hist = g[g["year"].between(2010, 2023)]
        if len(hist) < 5:
            continue
        y0, y1 = int(hist["year"].iloc[0]), int(hist["year"].iloc[-1])
        p0, p1 = float(hist["total_population"].iloc[0]), float(hist["total_population"].iloc[-1])
        if p0 <= 0 or p1 <= 0 or y1 <= y0:
            continue
        growth = (math.log(p1) - math.log(p0)) / (y1 - y0)
        last_year = int(g["year"].max())
        last_pop = float(g.loc[g["year"] == last_year, "total_population"].iloc[0])
        proj_rows = []
        for year in range(last_year + 1, 2041):
            last_pop = last_pop * math.exp(growth)
            proj_rows.append(
                {
                    "iso3": iso3,
                    "year": year,
                    "total_population": last_pop,
                    "source": "owid_hist_log_extrap_2040",
                }
            )
        if proj_rows:
            out.append(pd.DataFrame(proj_rows))
    return pd.concat(out, ignore_index=True).drop_duplicates(subset=["iso3", "year"], keep="first")


def _fetch_owid_wpp() -> None:
    """UN WPP via Our World in Data (historical; extrapolated to 2040)."""
    import pandas as pd

    url = (
        "https://ourworldindata.org/grapher/population-unwpp.csv"
        "?v=1&csvType=full&useColumnShortNames=false"
    )
    try:
        df = pd.read_csv(url, storage_options={"User-Agent": "research-immigration-fiscal/1.0"})
    except Exception as exc:
        print(f"WARN: OWID WPP fetch failed: {exc}", file=sys.stderr)
        return
    code_col = "Code" if "Code" in df.columns else "iso_code"
    year_col = "Year" if "Year" in df.columns else "year"
    pop_col = next((c for c in df.columns if "population" in c.lower()), None)
    if not pop_col:
        print("WARN: OWID WPP missing population column", file=sys.stderr)
        return
    keep = df[df[code_col].isin(("MEX", "USA") + HANSON_ORIGINS)].copy()
    keep = keep.rename(columns={code_col: "iso3", year_col: "year", pop_col: "total_population"})
    keep = keep[["iso3", "year", "total_population"]]
    keep["source"] = "owid_un_wpp2024"
    keep = _extend_population_projections(keep)
    keep.to_csv(OUT / "un_wpp_total_population_forecast.csv", index=False)
    print(f"Wrote un_wpp_total_population_forecast.csv ({len(keep)} rows) [OWID + extrap to 2040]")


def _fetch_wb_population() -> None:
    """WB historical population — fallback if OWID fails."""
    import pandas as pd
    import requests

    if (OUT / "un_wpp_total_population_forecast.csv").exists():
        return
    rows: list[dict] = []
    for iso3 in ("MEX", "USA") + HANSON_ORIGINS:
        url = (
            f"https://api.worldbank.org/v2/country/{iso3}/indicator/SP.POP.TOTL"
            f"?format=json&per_page=70"
        )
        try:
            data = requests.get(url, timeout=30).json()
            if not isinstance(data, list) or len(data) < 2:
                continue
            for item in data[1]:
                if item["value"] is None:
                    continue
                rows.append(
                    {
                        "iso3": iso3,
                        "year": int(item["date"]),
                        "total_population": item["value"],
                        "source": "worldbank_sp_pop_totl",
                    }
                )
        except Exception as exc:
            print(f"WARN: WB pop {iso3}: {exc}", file=sys.stderr)
    if rows:
        df = pd.DataFrame(rows)
        df.to_csv(OUT / "un_wpp_total_population_forecast.csv", index=False)
        print(f"Wrote un_wpp_total_population_forecast.csv ({len(df)} rows) [WB SP.POP.TOTL]")


def _fetch_un_wpp() -> None:
    """Optional UN Data Portal overlay when API responds."""
    import pandas as pd
    import requests

    loc_map = _un_location_map()
    if not loc_map:
        return
    rows: list[dict] = []
    sess = requests.Session()
    sess.headers["User-Agent"] = "research-immigration-fiscal/1.0"
    for iso3 in HANSON_ORIGINS[:5]:
        loc_id = loc_map.get(iso3)
        if not loc_id:
            continue
        url = (
            f"https://population.un.org/dataportalapi/api/v1/population/indicators/49"
            f"/locations/{loc_id}/start/1980/end/2040?format=json"
        )
        try:
            r = sess.get(url, timeout=30)
            if r.status_code != 200:
                continue
            for item in r.json().get("data", []):
                rows.append(
                    {
                        "iso3": iso3,
                        "location_id": loc_id,
                        "year": item["timeLabel"],
                        "total_population": item["value"],
                        "variant": item.get("variant", "Medium"),
                        "source": "un_dataportal",
                    }
                )
        except Exception:
            continue
    if rows:
        pd.DataFrame(rows).to_csv(OUT / "un_wpp_dataportal_overlay.csv", index=False)
        print(f"Wrote un_wpp_dataportal_overlay.csv ({len(rows)} rows)")


def _fetch_wb_gdp() -> None:
    import pandas as pd
    import requests

    rows: list[dict] = []
    for iso3 in ("MEX", "USA") + HANSON_ORIGINS:
        url = (
            f"https://api.worldbank.org/v2/country/{iso3}/indicator/NY.GDP.PCAP.KD"
            f"?format=json&per_page=70"
        )
        try:
            data = requests.get(url, timeout=30).json()
            if not isinstance(data, list) or len(data) < 2:
                continue
            for item in data[1]:
                rows.append(
                    {
                        "iso3": iso3,
                        "year": int(item["date"]),
                        "gdp_per_capita_constant_2015_usd": item["value"],
                    }
                )
        except Exception as exc:
            print(f"WARN: WB GDP {iso3}: {exc}", file=sys.stderr)
    if rows:
        df = pd.DataFrame(rows).dropna(subset=["gdp_per_capita_constant_2015_usd"])
        df = df.drop_duplicates(subset=["iso3", "year"], keep="first")
        df.to_csv(OUT / "imf_gdp_per_capita_panel.csv", index=False)
        print(f"Wrote imf_gdp_per_capita_panel.csv ({len(df)} rows)")


def _build_demographic_push_forecast() -> None:
    import pandas as pd

    pop = OUT / "un_wpp_total_population_forecast.csv"
    gdp = OUT / "imf_gdp_per_capita_panel.csv"
    if not pop.exists():
        return
    p = pd.read_csv(pop)
    p["year"] = p["year"].astype(int)
    p = p.groupby(["iso3", "year"], as_index=False)["total_population"].mean()
    base = p[p["year"] == 1980].set_index("iso3")["total_population"]
    us = p[p["iso3"] == "USA"].set_index("year")["total_population"]
    rows = []
    for iso3, g in p.groupby("iso3"):
        if iso3 == "USA":
            continue
        for year, row in g.iterrows():
            y = int(row["year"])
            if y not in us.index or iso3 not in base.index:
                continue
            rows.append(
                {
                    "origin_iso3": iso3,
                    "year": y,
                    "origin_population": row["total_population"],
                    "us_population": us.loc[y],
                    "origin_pop_rel_us_1980": (row["total_population"] / us.loc[y])
                    / (base[iso3] / us.loc[1980]),
                    "source": "un_wpp_indicator_49_vs_us",
                }
            )
    if rows:
        df = pd.DataFrame(rows)
        if gdp.exists():
            g = pd.read_csv(gdp)
            df = df.merge(
                g.rename(columns={"gdp_per_capita_constant_2015_usd": "origin_gdp_pc"}),
                left_on=["origin_iso3", "year"],
                right_on=["iso3", "year"],
                how="left",
            ).drop(columns=["iso3"], errors="ignore")
            usg = g[g["iso3"] == "USA"][["year", "gdp_per_capita_constant_2015_usd"]].rename(
                columns={"gdp_per_capita_constant_2015_usd": "us_gdp_pc"}
            )
            df = df.merge(usg, on="year", how="left")
            df["log_gdp_pc_ratio_us_origin"] = (df["us_gdp_pc"] / df["origin_gdp_pc"]).apply(
                lambda x: __import__("math").log(x) if x and x > 0 else None
            )
        df.to_csv(OUT / "demographic_push_forecast.csv", index=False)
        print(f"Wrote demographic_push_forecast.csv ({len(df)} rows)")


def _edu_bucket(schl: int | None) -> str | None:
    if schl is None:
        return None
    if schl < 12:
        return "dropout"
    if schl < 16:
        return "hs"
    return "college"


def _exp_group(age: int | None, schl: int | None) -> str | None:
    if age is None or schl is None:
        return None
    exp = max(0, age - schl - 6)
    if exp <= 5:
        return "0-5"
    if exp <= 10:
        return "6-10"
    if exp <= 20:
        return "11-20"
    return "21-30"


def _build_acs_labor_cells() -> None:
    import pandas as pd

    if not PERSON_ZIP.exists():
        print(f"WARN: skip ACS labor cells — missing {PERSON_ZIP}", file=sys.stderr)
        return
    tmp = DERIVED / "_tmp_tiera"
    tmp.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    with zipfile.ZipFile(PERSON_ZIP) as zf:
        for name in sorted(n for n in zf.namelist() if n.lower().endswith(".csv")):
            out = tmp / name.split("/")[-1]
            if not out.exists():
                out.write_bytes(zf.read(name))
            paths.append(str(out))
    import duckdb

    con = duckdb.connect()
    glob = ",".join(f"'{p}'" for p in paths)
    con.execute(f"""
        CREATE OR REPLACE TABLE p AS
        SELECT * FROM read_csv_auto([{glob}], header=true, union_by_name=true, sample_size=-1)
    """)
    con.execute("""
        CREATE OR REPLACE TABLE cell AS
        SELECT
          CASE
            WHEN TRY_CAST(SCHL AS INTEGER) < 12 THEN 'dropout'
            WHEN TRY_CAST(SCHL AS INTEGER) < 16 THEN 'hs'
            ELSE 'college'
          END AS education_bucket,
          CASE
            WHEN GREATEST(0, TRY_CAST(AGEP AS INTEGER) - TRY_CAST(SCHL AS INTEGER) - 6) <= 5 THEN '0-5'
            WHEN GREATEST(0, TRY_CAST(AGEP AS INTEGER) - TRY_CAST(SCHL AS INTEGER) - 6) <= 10 THEN '6-10'
            WHEN GREATEST(0, TRY_CAST(AGEP AS INTEGER) - TRY_CAST(SCHL AS INTEGER) - 6) <= 20 THEN '11-20'
            ELSE '21-30'
          END AS experience_group,
          CAST(NATIVITY AS VARCHAR) = '2' AS is_foreign_born,
          TRY_CAST(RAC1P AS INTEGER) AS race_code,
          SUM(TRY_CAST(PWGTP AS DOUBLE)) AS weight,
          SUM(CASE WHEN TRY_CAST(ESR AS INTEGER) IN (1,2,4,5) THEN TRY_CAST(PWGTP AS DOUBLE) ELSE 0 END)
            / NULLIF(SUM(TRY_CAST(PWGTP AS DOUBLE)), 0) AS employment_rate,
          SUM(TRY_CAST(PERNP AS DOUBLE) * TRY_CAST(PWGTP AS DOUBLE))
            / NULLIF(SUM(TRY_CAST(PWGTP AS DOUBLE)), 0) AS avg_earnings_weighted
        FROM p
        WHERE TRY_CAST(AGEP AS INTEGER) BETWEEN 18 AND 64
          AND TRY_CAST(SEX AS INTEGER) = 1
        GROUP BY 1, 2, 3, 4
    """)
    borjas = con.execute("""
        SELECT
          education_bucket,
          experience_group,
          SUM(CASE WHEN is_foreign_born THEN weight ELSE 0 END) AS immigrant_weight,
          SUM(CASE WHEN NOT is_foreign_born THEN weight ELSE 0 END) AS native_weight,
          SUM(CASE WHEN is_foreign_born THEN weight ELSE 0 END)
            / NULLIF(SUM(weight), 0) AS immigrant_share,
          SUM(avg_earnings_weighted * weight) / NULLIF(SUM(weight), 0) AS avg_earnings
        FROM cell
        GROUP BY 1, 2
        ORDER BY 1, 2
    """).df()
    borjas["year"] = 2023
    borjas["source"] = "acs_pums_2023_anchor"
    borjas.to_csv(OUT / "borjas_supply_shock_cell_2023.csv", index=False)

    bgh = con.execute("""
        SELECT
          education_bucket,
          experience_group,
          CASE WHEN race_code = 2 THEN 'black' WHEN race_code = 1 THEN 'white' ELSE 'other' END AS race_group,
          is_foreign_born,
          SUM(weight) AS weight,
          SUM(employment_rate * weight) / NULLIF(SUM(weight), 0) AS employment_rate,
          SUM(avg_earnings_weighted * weight) / NULLIF(SUM(weight), 0) AS avg_earnings
        FROM cell
        WHERE race_code IN (1, 2)
        GROUP BY 1, 2, 3, 4
        ORDER BY 1, 2, 3, 4
    """).df()
    bgh["year"] = 2023
    bgh["incarceration_rate"] = None
    bgh["source"] = "acs_pums_2023_anchor"
    bgh["notes"] = "incarceration requires IPUMS GQTYPE/decennial — ACS anchor only"
    bgh.to_csv(OUT / "bgh_outcomes_cell_2023.csv", index=False)
    con.close()
    print(f"Wrote borjas ({len(borjas)}) + bgh ({len(bgh)}) ACS 2023 cells")


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _write_razin_tables()
    _parse_oecd_socx()
    _fetch_owid_wpp()
    _fetch_wb_population()
    _fetch_un_wpp()
    _fetch_wb_gdp()
    _build_demographic_push_forecast()
    _build_acs_labor_cells()


if __name__ == "__main__":
    build()
