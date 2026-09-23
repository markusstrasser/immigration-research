"""Metro x year cells from the compact ACS extracts, on fixed 2013 OMB metropolitan areas.

Each person's weight is split across counties by the Geocorr PUMA->county allocation factor of the
PUMA vintage in force that year (2000 PUMAs to 2011, 2010 PUMAs 2012-2021, 2020 PUMAs from 2022),
then counties are summed into 2013 metropolitan CBSAs. Connecticut's 2022+ planning regions come
from the shared county file once it carries them; until then CT_REGIONS maps each to the 2013
metro holding most of its population, and the run says so.

Inputs (read-only):
  _cache/acs/p{year}.parquet                     from acs_extract.py
  ../employment_entry_2026_09_18/_cache/xwalk_{puma2k,puma12,puma22}.csv   Geocorr factors
      (regenerate with that lane's fetch_crosswalks.py); copied to _cache/xwalk/ with hashes
  ../hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv       county -> 2013 CBSA
Outputs:
  derived/metro_cells.csv   metro x year x group x education x sex: population and employment in
                            Cadena-Kovak's sample, effective sample counts, real wage bill
  derived/metro_sector.csv  metro x year x NAICS sector: employed persons (all groups)
  derived/xwalk_manifest.json
"""
import functools
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
XW_SRC = FISCAL / "employment_entry_2026_09_18" / "_cache"
CBSA_SRC = FISCAL / "hedonic_composition_2026_09_19" / "derived" / "geo_county_cbsa_2013.csv"

# Connecticut planning regions (2022 county-equivalents) -> 2013 metro holding most of their people
CT_REGIONS = {"09110": "25540", "09120": "14860", "09130": "25540", "09140": "35300",
              "09150": "49340", "09170": "35300", "09180": "35980", "09190": "14860"}


def vintage(year: int) -> str:
    return "puma2k" if year <= 2011 else ("puma12" if year <= 2021 else "puma22")


def load_xwalks() -> dict:
    (CACHE / "xwalk").mkdir(parents=True, exist_ok=True)
    manifest, out = {}, {}
    for v in ("puma2k", "puma12", "puma22"):
        src, dst = XW_SRC / f"xwalk_{v}.csv", CACHE / "xwalk" / f"xwalk_{v}.csv"
        if not dst.exists():
            if not src.exists():
                raise SystemExit(f"[BLOCKED] missing {src}; run employment_entry_2026_09_18/fetch_crosswalks.py")
            shutil.copy2(src, dst)
        manifest[dst.name] = hashlib.sha256(dst.read_bytes()).hexdigest()
        df = pd.read_csv(dst, dtype=str)
        pc = [c for c in df.columns if c.lower().startswith("puma")][0]
        df = df.rename(columns={pc: "puma", "county": "cofips"})
        df["state"] = df["state"].str.zfill(2)
        df["puma"] = df["puma"].str.zfill(5)
        df["cofips"] = df["cofips"].str.zfill(5)
        df["afact"] = pd.to_numeric(df["afact"], errors="coerce")
        out[v] = df[["state", "puma", "cofips", "afact"]].dropna()
    manifest["geo_county_cbsa_2013.csv"] = hashlib.sha256(CBSA_SRC.read_bytes()).hexdigest()
    (DERIVED / "xwalk_manifest.json").write_text(json.dumps(manifest, indent=2))
    return out


@functools.lru_cache(maxsize=1)
def county_cbsa() -> pd.DataFrame:
    """Metro counties -> 2013 CBSA from the shared file (read once per run; callers must not mutate). Connecticut planning regions the file lacks
    come from CT_REGIONS, reported as degraded; rows the file has always win, so no county repeats."""
    c = pd.read_csv(CBSA_SRC, dtype=str)
    have = c.set_index("county_fips")["cbsa"]
    missing = [k for k in CT_REGIONS if k not in have.index]
    m = c[c["is_metro"] == "1"][["county_fips", "cbsa", "cbsa_title"]].rename(columns={"county_fips": "cofips"})
    if missing:
        titles = m.drop_duplicates("cbsa").set_index("cbsa")["cbsa_title"]
        ct = pd.DataFrame({"cofips": missing, "cbsa": [CT_REGIONS[k] for k in missing]})
        ct["cbsa_title"] = ct["cbsa"].map(titles)
        print(f"  ! [DEGRADED] shared county->CBSA file lacks {len(missing)} Connecticut planning regions; lane mapping used")
        m = pd.concat([m, ct], ignore_index=True)
    else:
        diff = {k: (have[k], v) for k, v in CT_REGIONS.items() if have[k] != v}
        print(f"  ✓ Connecticut planning regions from the shared file; differs from the lane mapping at {diff or 'none'}")
    if m["cofips"].duplicated().any():
        raise SystemExit("[FAILED] a county appears twice in the county->CBSA mapping")
    return m


def load_cbsa() -> pd.DataFrame:
    return county_cbsa()


def cells_for_year(year: int, xw: dict, cbsa: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    p = pd.read_parquet(CACHE / "acs" / f"p{year}.parquet")
    p = p[(~p["gq"]) & (~p["inschool"])].copy()
    p["state"] = p["st"].astype(str).str.zfill(2)
    p["emp_w"] = p["pwgtp"] * p["employed"]
    p["wagebill"] = p["pwgtp"] * p["wage_real"]
    p["one"] = 1.0
    p["emp_one"] = p["employed"].astype(float)
    p["w2"] = p["pwgtp"].astype(float) ** 2
    p["w2_emp"] = p["w2"] * p["employed"]
    keys = ["state", "puma", "group", "lowed", "sex"]
    pc = p.groupby(keys, as_index=False).agg(pop=("pwgtp", "sum"), emp=("emp_w", "sum"),
                                              n=("one", "sum"), n_emp=("emp_one", "sum"),
                                              wagebill=("wagebill", "sum"), w2=("w2", "sum"),
                                              w2_emp=("w2_emp", "sum"))
    ps = (p[p["employed"]].groupby(["state", "puma", "sector"], as_index=False)
          .agg(emp=("pwgtp", "sum"), n=("one", "sum")))
    # PUMA -> metro factor: county allocation factors summed within each 2013 metro
    x = (xw[vintage(year)].merge(cbsa, on="cofips", how="inner")
         .groupby(["state", "puma", "cbsa", "cbsa_title"], as_index=False)["afact"].sum())
    out = []
    for frame, vals, gkeys in ((pc, ["pop", "emp", "n", "n_emp", "wagebill", "w2", "w2_emp"],
                                ["group", "lowed", "sex"]),
                               (ps, ["emp", "n"], ["sector"])):
        m = frame.merge(x, on=["state", "puma"], how="inner")
        for v in vals:
            # sampling variance terms (sums of squared weights) scale with the factor squared
            m[v] = m[v] * (m["afact"] ** 2 if v.startswith("w2") else m["afact"])
        g = m.groupby(["cbsa", "cbsa_title"] + gkeys, as_index=False)[vals].sum()
        g.insert(2, "year", year)
        out.append(g)
    unmatched = set(zip(pc["state"], pc["puma"])) - set(zip(xw[vintage(year)]["state"], xw[vintage(year)]["puma"]))
    if len(unmatched) > 5:
        raise SystemExit(f"[FAILED] {year}: {len(unmatched)} PUMAs absent from {vintage(year)} crosswalk")
    return out[0], out[1]


def main() -> None:
    years = [int(a) for a in sys.argv[1:]] or [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                                                 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024]
    DERIVED.mkdir(exist_ok=True)
    xw, cbsa = load_xwalks(), load_cbsa()
    cells, sectors = zip(*(cells_for_year(y, xw, cbsa) for y in years))
    pd.concat(cells, ignore_index=True).to_csv(DERIVED / "metro_cells.csv", index=False)
    pd.concat(sectors, ignore_index=True).to_csv(DERIVED / "metro_sector.csv", index=False)
    print(f"metro cells for {years}: {sum(len(c) for c in cells)} rows")


if __name__ == "__main__":
    main()
