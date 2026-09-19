#!/usr/bin/env python3
"""Independent-outcome arm: Zillow ZIP indices against ZCTA composition.

Zillow is built from listings and transactions, so its sampling error is
independent of the ACS sample that measures neighbourhood composition. If the
within-metro composition gradient is an artefact of correlated ACS sampling
error, it should vanish here.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estim, prep
from analyze2 import fitrow

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE, DERIVED = LANE / "_cache", LANE / "derived"
# ACS 5-year period midpoints
MID = {2013: 2011, 2018: 2016, 2023: 2021}
CTRL = ["d_own_rate", "d_vac_rate", "d_sfdet_share", "d_medyrbuilt",
        "own_rate_0", "vac_rate_0", "sfdet_share_0", "medyrbuilt_0",
        "log_inc_0", "ba_share_0", "log_dens_0", "nhwhite_share_0"]


def zillow_annual(path, years):
    d = pd.read_csv(path, dtype={"RegionName": str}, low_memory=False)
    d["zip"] = d["RegionName"].str.zfill(5)
    out = pd.DataFrame({"zip": d["zip"]})
    for y in years:
        cols = [c for c in d.columns if c.startswith(f"{y}-")]
        out[f"z{y}"] = d[cols].mean(axis=1) if cols else np.nan
    return out.groupby("zip", as_index=False).mean()


def zcta_year(y):
    rows = json.load(open(CACHE / "zcta" / f"{y}.json"))
    d = pd.DataFrame(rows[1:], columns=rows[0])
    zc = [c for c in d.columns if "zip" in c.lower()][0]
    d["zcta"] = d[zc].str.zfill(5)
    for c in d.columns:
        if c[0] == "B":
            d[c] = pd.to_numeric(d[c], errors="coerce")
            d.loc[d[c] < -1e8, c] = np.nan
    d = d.drop_duplicates("zcta")
    pop = d["B03002_001E"]
    o = pd.DataFrame({"zcta": d["zcta"], "pop": pop})
    o["hisp_share"] = d["B03002_012E"] / pop.where(pop > 0)
    o["nhwhite_share"] = d["B03002_003E"] / pop.where(pop > 0)
    o["mex_share"] = d["B03001_004E"] / pop.where(pop > 0)
    nat = d["B05002_001E"]
    o["fb_share"] = d["B05002_013E"] / nat.where(nat > 0)
    hh = d["B25003_001E"]
    o["own_units"], o["rent_units"], o["hh"] = d["B25003_002E"], d["B25003_003E"], hh
    o["own_rate"] = d["B25003_002E"] / hh.where(hh > 0)
    hu = d["B25002_001E"]
    o["vac_rate"] = d["B25002_003E"] / hu.where(hu > 0)
    su = d["B25024_001E"]
    o["sfdet_share"] = d["B25024_002E"] / su.where(su > 0)
    ed = d["B15003_001E"]
    o["ba_share"] = d[["B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]
                      ].sum(axis=1, min_count=1) / ed.where(ed > 0)
    o["medyrbuilt"] = (d["B25035_001E"] - 1970.0) / 10.0
    o["med_rent"], o["med_value"] = d["B25064_001E"], d["B25077_001E"]
    o["med_inc"] = d["B19013_001E"]
    return o


def main():
    rel = pd.read_csv(CACHE / "zcta_county_rel_10.txt",
                      dtype={"ZCTA5": str, "STATE": str, "COUNTY": str})
    rel["zcta"] = rel["ZCTA5"].str.zfill(5)
    rel["county_fips"] = rel["STATE"].str.zfill(2) + rel["COUNTY"].str.zfill(3)
    rel = rel.sort_values(["zcta", "POPPT"], ascending=[True, False])
    dom = rel.groupby("zcta", as_index=False).first()[["zcta", "county_fips",
                                                       "ZAREALAND"]]
    cb = pd.read_csv(DERIVED / "geo_county_cbsa_2013.csv",
                     dtype={"county_fips": str, "cbsa": str})
    dom = dom.merge(cb, on="county_fips", how="left")
    dom["aland_sqmi"] = dom["ZAREALAND"] / 2589988.11

    acs = {y: zcta_year(y) for y in MID}
    zhvi = zillow_annual(CACHE / "zillow" / "zip_zhvi.csv", sorted(set(MID.values())))
    zori = zillow_annual(CACHE / "zillow" / "zip_zori.csv", sorted(set(MID.values())))
    print(f"[zillow] zhvi zips={len(zhvi)} zori zips={len(zori)}", flush=True)

    rows, notes = [], []
    for per, t0, t1 in [("A", 2013, 2018), ("B", 2018, 2023)]:
        a = acs[t0].add_suffix("_0").rename(columns={"zcta_0": "zcta"})
        b = acs[t1].add_suffix("_1").rename(columns={"zcta_1": "zcta"})
        m = a.merge(b, on="zcta").merge(dom, on="zcta", how="left")
        m = m[m["is_metro"] == 1].copy()
        m["period"] = per
        m["cbsa_period"] = m["cbsa"] + "_" + per
        for v in ["hisp_share", "fb_share", "mex_share", "nhwhite_share", "own_rate",
                  "vac_rate", "sfdet_share", "medyrbuilt"]:
            m[f"d_{v}"] = m[f"{v}_1"] - m[f"{v}_0"]
        m["log_inc_0"] = np.log(m["med_inc_0"].where(m["med_inc_0"] > 0))
        m["log_dens_0"] = np.log((m["pop_0"] /
                                  m["aland_sqmi"].where(m["aland_sqmi"] > 0))
                                 .where(lambda s: s > 0))
        for nm, src in [("zhvi", zhvi), ("zori", zori)]:
            m = m.merge(src.rename(columns={c: f"{nm}_{c}" for c in src.columns
                                            if c != "zip"}),
                        left_on="zcta", right_on="zip", how="left").drop(
                            columns="zip", errors="ignore")
            m[f"dlog_{nm}"] = (np.log(m[f"{nm}_z{MID[t1]}"].where(lambda s: s > 0))
                               - np.log(m[f"{nm}_z{MID[t0]}"].where(lambda s: s > 0)))
        m["dlog_acsvalue"] = (np.log(m["med_value_1"].where(m["med_value_1"] > 0))
                              - np.log(m["med_value_0"].where(m["med_value_0"] > 0)))
        m["dlog_acsrent"] = (np.log(m["med_rent_1"].where(m["med_rent_1"] > 0))
                             - np.log(m["med_rent_0"].where(m["med_rent_0"] > 0)))
        rows.append(m)
    M = pd.concat(rows, ignore_index=True)
    M = M[(M["pop_0"] >= 500) & (M["pop_1"] >= 500)].copy()
    z = prep.standardize(M, CTRL)
    for c in z.columns:
        M[c + "_z"] = z[c]
    C = [c + "_z" for c in CTRL]
    M.to_csv(DERIVED / "zcta_panel.csv", index=False, float_format="%.6g")

    res = []
    for y, wcol, lab in [("dlog_zhvi", "own_units_0", "Zillow ZHVI (independent)"),
                         ("dlog_acsvalue", "own_units_0", "ACS median value (same sample)"),
                         ("dlog_zori", "rent_units_0", "Zillow ZORI (independent)"),
                         ("dlog_acsrent", "rent_units_0", "ACS median rent (same sample)")]:
        M["_w"] = M[wcol]
        for grp in ["fb", "hisp", "mex"]:
            for per in ["pooled", "A", "B"]:
                sel = M if per == "pooled" else M[M["period"] == per]
                r = fitrow(sel, y, f"d_{grp}_share", C, "_w", "cbsa_period")
                if r:
                    res.append({"outcome": y, "label": lab, "treat": grp,
                                "period": per,
                                "coef": r[f"d_{grp}_share__coef"],
                                "se": r[f"d_{grp}_share__se"],
                                "t": r[f"d_{grp}_share__t"], "n": r["n"],
                                "cbsa_periods": r["cbsa_periods"]})
    # Matched-sample head-to-head: identical rows, only the outcome source differs.
    for zcol, acol, wcol, tag in [("dlog_zhvi", "dlog_acsvalue", "own_units_0", "value"),
                                  ("dlog_zori", "dlog_acsrent", "rent_units_0", "rent")]:
        MM = M[M[zcol].notna() & M[acol].notna()].copy()
        MM["_w"] = MM[wcol]
        for grp in ["fb", "hisp", "mex"]:
            for per in ["pooled", "A", "B"]:
                sel = MM if per == "pooled" else MM[MM["period"] == per]
                for y, lab in [(zcol, f"MATCHED Zillow ({tag})"),
                               (acol, f"MATCHED ACS ({tag})")]:
                    r = fitrow(sel, y, f"d_{grp}_share", C, "_w", "cbsa_period")
                    if r:
                        res.append({"outcome": y, "label": lab, "treat": grp,
                                    "period": per,
                                    "coef": r[f"d_{grp}_share__coef"],
                                    "se": r[f"d_{grp}_share__se"],
                                    "t": r[f"d_{grp}_share__t"], "n": r["n"],
                                    "cbsa_periods": r["cbsa_periods"]})
    R = pd.DataFrame(res)
    R.to_csv(DERIVED / "results_zillow.csv", index=False, float_format="%.6g")
    print(R.to_string(index=False))
    print(f"[zillow] ZCTA panel rows={len(M)} "
          f"zhvi non-missing={M['dlog_zhvi'].notna().sum()} "
          f"zori non-missing={M['dlog_zori'].notna().sum()}")


if __name__ == "__main__":
    main()
