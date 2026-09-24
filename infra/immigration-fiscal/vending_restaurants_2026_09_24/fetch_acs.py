"""Pre-2018 exposure measures by county and by ZCTA (ACS 2013-2017), plus the Hispanic share of food
preparation and serving workers by county (ACS EEO Tabulation 2014-2018, residence geography).

ACS 2013-2017 five-year (api.census.gov/data/2017/acs/acs5), counties and California ZCTAs:
  B03002_001E total population, B03002_012E Hispanic or Latino, B03001_004E Mexican origin,
  B05006_139E born in Mexico, B05002_013E foreign born, B19301_001E per-capita income.
EEO Tabulation 2014-2018, table EEOALL1R (detailed census occupation by race/ethnicity, residence):
  column C01 = all races, C02 = Hispanic or Latino; line 001 = count. Food preparation and serving
  related occupations are EEO occupation codes 4000-4160 (the tabulation publishes 4000, 4020, 4040,
  4055, 4110, 4130, 4150 nationally). Detailed occupations are published for EEO county sets (groups
  of counties with 50,000+ residents; a large county is its own set), not for single counties, so each
  county takes its set's share through the Census county-set crosswalk. The 2014-2018 window's last
  year, 2018, precedes SB 946's 1 Jan 2019 start.

Writes _cache/acs/*.json (raw) and derived/exposure_county.csv, derived/exposure_zcta_ca.csv.
Run from the repository root with CENSUS_API_KEY set (see fetch_cbp.py).
"""
import csv
import gzip
import io

import pandas as pd

from lib import CACHE, DERIVED, census_json, curl

ACS = "https://api.census.gov/data/2017/acs/acs5"
VARS = ["B03002_001E", "B03002_012E", "B03001_004E", "B05006_139E", "B05002_013E", "B19301_001E"]
EEO_URL = ("https://www2.census.gov/EEO_2014_2018/EEO_Tables_By_All_Areas/ASCII-Files/"
           "acseeo5y2018-eeoall1r.dat.gz")
SETS_URL = ("https://www2.census.gov/EEO_2014_2018/EEO_FTP_Site_Documentation/2018_County_Set_Documentation/"
            "2018-EEO-County-Sets%2003.04.21.xlsx")


def is_food(code: str) -> bool:
    return code.isdigit() and 4000 <= int(code) <= 4160


def acs(geo: str, tag: str) -> pd.DataFrame:
    rows = census_json(f"{ACS}?get=NAME,{','.join(VARS)}&for={geo}", CACHE / "acs" / f"acs5_2017_{tag}.json",
                       need_cols=tuple(VARS))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for v in VARS:
        df[v] = pd.to_numeric(df[v], errors="coerce")
        df.loc[df[v] < 0, v] = float("nan")  # Census sentinel values (-666666666 etc.)
    df["pop"] = df["B03002_001E"]
    df["hisp_share"] = df["B03002_012E"] / df["pop"]
    df["mex_share"] = df["B03001_004E"] / df["pop"]
    df["mexborn_share"] = df["B05006_139E"] / df["pop"]
    df["fb_share"] = df["B05002_013E"] / df["pop"]
    df["pc_income"] = df["B19301_001E"]
    return df


def eeo_food_prep() -> pd.DataFrame:
    path = CACHE / "eeo" / "acseeo5y2018-eeoall1r.dat.gz"
    if not path.exists():
        curl(EEO_URL, path)
    sets_path = CACHE / "eeo" / "county_sets_2018.xlsx"
    if not sets_path.exists():
        curl(SETS_URL, sets_path)
    tot, hisp = {}, {}
    with gzip.open(path, "rt", encoding="latin-1") as fh:
        rdr = csv.reader(fh, delimiter="|")
        head = next(rdr)
        head[0] = head[0].lstrip("#")
        i_geo, i_eeo = head.index("GEO_ID"), head.index("EEO")
        i_all, i_his = head.index("EEOALL1R_C01_001E"), head.index("EEOALL1R_C02_001E")
        for r in rdr:
            g = r[i_geo]
            if not g.startswith("9020000US") or not is_food(r[i_eeo]):
                continue
            cs = g[len("9020000US"):]
            a = float(r[i_all]) if r[i_all] not in ("", "N", "(X)") else 0.0
            h = float(r[i_his]) if r[i_his] not in ("", "N", "(X)") else 0.0
            tot[cs] = tot.get(cs, 0.0) + a
            hisp[cs] = hisp.get(cs, 0.0) + h
    sets = pd.read_excel(sets_path, sheet_name="Counties 50,000+", dtype=str)
    code_col = [c for c in sets.columns if "County Set" in c and "Code" in c][0]
    sets["cs"] = sets[code_col].ffill()
    sets["fips"] = sets["FIPS State Code"].str.zfill(2) + sets["FIPS County Code"].str.zfill(3)
    sets = sets.dropna(subset=["FIPS County Code"])
    df = sets[["fips", "cs"]].copy()
    df["foodprep_workers_set"] = df["cs"].map(tot)
    df["foodprep_hisp_share"] = df["cs"].map(lambda k: hisp.get(k, 0.0) / tot[k] if tot.get(k) else float("nan"))
    return df


def main() -> None:
    c = acs("county:*", "county")
    c["fips"] = c["state"] + c["county"]
    c = c[c["state"] != "72"]
    if len(c) < 3100:
        raise SystemExit(f"[FAILED] ACS county rows {len(c)}")
    e = eeo_food_prep()
    if len(e) < 3100 or e["foodprep_hisp_share"].isna().mean() > 0.01:
        raise SystemExit(f"[FAILED] EEO county-set crosswalk: {len(e)} counties, "
                         f"{e['foodprep_hisp_share'].isna().sum()} without a food-prep share")
    out = c.merge(e, on="fips", how="left")
    sets = out.drop_duplicates("cs")
    us = (sets["foodprep_hisp_share"] * sets["foodprep_workers_set"]).sum() / sets["foodprep_workers_set"].sum()
    print(f"  counties {len(out)}; county sets {len(sets)}; food-prep workers {sets['foodprep_workers_set'].sum():,.0f};"
          f" Hispanic share {us:.3f}")
    keep = ["fips", "NAME", "pop", "hisp_share", "mex_share", "mexborn_share", "fb_share", "pc_income",
            "cs", "foodprep_workers_set", "foodprep_hisp_share"]
    DERIVED.mkdir(exist_ok=True)
    out[keep].to_csv(DERIVED / "exposure_county.csv", index=False, lineterminator="\n", float_format="%.6g")
    z = acs("zip%20code%20tabulation%20area:*&in=state:06", "zcta_ca")
    z = z.rename(columns={"zip code tabulation area": "zcta"})
    if len(z) < 1700:
        raise SystemExit(f"[FAILED] ACS CA ZCTA rows {len(z)}")
    z[["zcta", "pop", "hisp_share", "mex_share", "mexborn_share", "fb_share", "pc_income"]].to_csv(
        DERIVED / "exposure_zcta_ca.csv", index=False, lineterminator="\n", float_format="%.6g")
    print(f"  CA ZCTAs {len(z)}")


if __name__ == "__main__":
    main()
