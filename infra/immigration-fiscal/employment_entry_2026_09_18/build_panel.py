"""Assemble the metro x year panel from PUMA cells + PUMA->county->CBSA crosswalks.

Metro definition is held fixed across all years: the OMB Feb-2013 delineation
(list1.xls), Metropolitan Statistical Areas only. PUMA-level weighted counts are
allocated to counties by the Geocorr population allocation factor for the PUMA
vintage in force that year, then summed into the fixed 2013 CBSA.

PUMA vintage by ACS year: 2005-2011 -> puma2k, 2012-2021 -> puma12, 2022-2023 -> puma22.
"""
import pathlib, sys
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

VINTAGE = {y: ("puma2k" if y <= 2011 else "puma12" if y <= 2021 else "puma22")
           for y in range(2005, 2024)}

MEASURES = ["pop1829", "emp1829", "cemp1829", "lf1829",
            "pop1624", "emp1624", "cemp1624", "lf1624",
            "pop1864", "mex1864", "fb1864"]


def load_xwalks():
    out = {}
    for v in ("puma2k", "puma12", "puma22"):
        df = pd.read_csv(CACHE / f"xwalk_{v}.csv", dtype=str)
        pc = [c for c in df.columns if c.lower().startswith("puma")][0]
        df = df.rename(columns={pc: "puma", "county": "cofips", "afact": "afact"})
        df["state"] = df["state"].str.zfill(2)
        df["puma"] = df["puma"].str.zfill(5)
        df["cofips"] = df["cofips"].str.zfill(5)
        df["afact"] = pd.to_numeric(df["afact"], errors="coerce")
        out[v] = df[["state", "puma", "cofips", "afact"]].dropna()
    return out


def load_cbsa():
    d = pd.read_excel(CACHE / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return d[["cofips", "cbsa", "CBSA Title"]].rename(columns={"CBSA Title": "cbsa_title"})


def main():
    xw = load_xwalks()
    cbsa = load_cbsa()
    files = sorted((CACHE / "cells3").glob("cells_*.csv"))
    if not files:
        sys.exit("no cell files")
    cells = pd.concat((pd.read_csv(f, dtype={"state": str, "puma": str, "sex": str})
                       for f in files), ignore_index=True)
    # keep only the fully-pulled endpoint years; stray part-coverage years from earlier
    # attempts would otherwise enter the panel with a handful of states per metro
    keep_years = {2005, 2008, 2010, 2013, 2015, 2018, 2023}
    dropped = sorted(set(cells["year"]) - keep_years)
    if dropped:
        print("dropping part-coverage years:", dropped)
    cells = cells[cells["year"].isin(keep_years)]
    cells["state"] = cells["state"].str.zfill(2)
    cells["puma"] = cells["puma"].str.zfill(5)
    cells["vint"] = cells["year"].map(VINTAGE)

    parts = []
    for v, g in cells.groupby("vint"):
        m = g.merge(xw[v], on=["state", "puma"], how="left", indicator=True)
        miss = (m["_merge"] != "both").mean()
        print(f"{v}: puma-county merge miss rate {miss:.4f}  rows {len(m)}")
        m = m[m["_merge"] == "both"].drop(columns="_merge")
        for c in MEASURES:
            m[c] = m[c] * m["afact"]
        parts.append(m)
    alloc = pd.concat(parts, ignore_index=True)

    j = alloc.merge(cbsa, on="cofips", how="inner")
    print("rows in metro counties:", len(j), "distinct cbsa:", j["cbsa"].nunique())

    # sex-specific outcomes: sex in {1,2}; the 30-64 treatment block is in sex=='T'
    out_by_sex = (j[j["sex"].isin(["1", "2"])]
                  .groupby(["cbsa", "cbsa_title", "year", "sex"], as_index=False)[MEASURES].sum())
    treat = (j.groupby(["cbsa", "year"], as_index=False)[["pop1864", "mex1864", "fb1864"]].sum()
             .rename(columns={"pop1864": "t_pop1864", "mex1864": "t_mex1864", "fb1864": "t_fb1864"}))

    # college-educated native 18-29 control group, same allocation chain
    coll_files = sorted((CACHE / "cells_coll").glob("coll_*.csv"))
    coll = None
    if coll_files:
        cc = pd.concat((pd.read_csv(f, dtype={"state": str, "puma": str, "sex": str})
                        for f in coll_files), ignore_index=True)
        cc["state"] = cc["state"].str.zfill(2)
        cc["puma"] = cc["puma"].str.zfill(5)
        cc["vint"] = cc["year"].map(VINTAGE)
        cparts = []
        for v, g in cc.groupby("vint"):
            mm = g.merge(xw[v], on=["state", "puma"], how="inner")
            for c in ("popc", "empc", "lfc"):
                mm[c] = mm[c] * mm["afact"]
            cparts.append(mm)
        ca = pd.concat(cparts, ignore_index=True).merge(cbsa, on="cofips", how="inner")
        coll = (ca.groupby(["cbsa", "year", "sex"], as_index=False)[["popc", "empc", "lfc"]].sum())
        print("college control rows", len(coll))

    panel = out_by_sex.merge(treat, on=["cbsa", "year"], how="left")
    if coll is not None:
        panel = panel.merge(coll, on=["cbsa", "year", "sex"], how="left")
        panel["epopc1829"] = 100.0 * panel["empc"] / panel["popc"]
        panel["lfpc1829"] = 100.0 * panel["lfc"] / panel["popc"]
    panel["mex_share"] = 100.0 * panel["t_mex1864"] / panel["t_pop1864"]
    panel["fb_share"] = 100.0 * panel["t_fb1864"] / panel["t_pop1864"]
    for band in ("1829", "1624"):
        panel[f"epop{band}"] = 100.0 * panel[f"emp{band}"] / panel[f"pop{band}"]
        panel[f"cepop{band}"] = 100.0 * panel[f"cemp{band}"] / panel[f"pop{band}"]
        panel[f"lfp{band}"] = 100.0 * panel[f"lf{band}"] / panel[f"pop{band}"]
    panel.to_csv(DERIVED / "metro_year_panel.csv", index=False)
    print("panel rows", len(panel), "years", sorted(panel.year.unique()))

    # base-year (2000) Mexico-born stock by metro, for the shift-share instrument
    import json
    raw = json.load(open(CACHE / "sf3_2000_county_pob.json"))
    sf = pd.DataFrame(raw[1:], columns=raw[0])
    sf["cofips"] = sf["state"].str.zfill(2) + sf["county"].str.zfill(3)
    sf["mex2000"] = pd.to_numeric(sf["PCT019103"])
    sf["fb2000"] = pd.to_numeric(sf["PCT019001"])
    sf["pop2000"] = pd.to_numeric(sf["P001001"])
    natl_mex2000 = sf["mex2000"].sum()
    base = (sf.merge(cbsa, on="cofips", how="inner")
              .groupby("cbsa", as_index=False)[["mex2000", "fb2000", "pop2000"]].sum())
    base["mex_base_share_natl"] = base["mex2000"] / natl_mex2000
    base["fb_base_share_natl"] = base["fb2000"] / sf["fb2000"].sum()
    base.to_csv(DERIVED / "metro_base_2000.csv", index=False)
    print("base metros", len(base), "natl mex 2000", natl_mex2000)


if __name__ == "__main__":
    main()
