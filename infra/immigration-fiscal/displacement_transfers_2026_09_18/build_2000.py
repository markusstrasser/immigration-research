"""Add the Census 2000 endpoint and the PRE-1990 base shares to the panel.

2000 endpoint (county -> OMB February-2013 CBSA, metropolitan areas only):
  hh SSI receipt     P063001 / P063002
  hh public assist   P064001 / P064002
  population         P001001          (from the employment_entry lane's cached PCT019 pull)
  foreign born       PCT019001        Mexico-born  PCT019103

Pre-1990 base, the whole point of this file: the metro's share of the NATIONAL stock of
foreign-born (P022004..009, entered before 1990) and Mexico-born (PCT020059 + PCT020062,
entered 1980-89 and before 1980) as observed in Census 2000. Unlike the 2000 total stock,
this base is predetermined with respect to every window estimated from 2000 onward.
"""
import json, pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
FB_PRE90 = [f"P022{i:03d}" for i in range(4, 10)]
MEX_PRE90 = ["PCT020059", "PCT020062"]


def load_cbsa():
    d = pd.read_excel(CACHE / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return d[["cofips", "cbsa", "CBSA Title"]].rename(columns={"CBSA Title": "cbsa_title"})


def main():
    slim = json.loads((CACHE / "sf3" / "slim.json").read_text())
    ssi = json.loads((CACHE / "sf3" / "p063_ssi.json").read_text())
    raw = json.loads((HERE.parent / "employment_entry_2026_09_18" / "_cache"
                      / "sf3_2000_county_pob.json").read_text())
    ph = {n: i for i, n in enumerate(raw[0])}
    pob = {r[ph["state"]].zfill(2) + r[ph["county"]].zfill(3):
           (float(r[ph["PCT019001"]]), float(r[ph["PCT019103"]]), float(r[ph["P001001"]]))
           for r in raw[1:]}
    rows = []
    for fips, rec in slim.items():
        fb, mex, pop = pob.get(fips, (np.nan, np.nan, np.nan))
        g = ssi.get(fips, {})
        rows.append({
            "cofips": fips, "pop": pop, "fb": fb, "mex": mex,
            "hh_tot": g.get("P063001"), "hh_ssi": g.get("P063002"),
            "hh_tot_pa": rec.get("P064001"), "hh_pa": rec.get("P064002"),
            "fb_pre90": sum((rec.get(c) or 0.0) for c in FB_PRE90),
            "mex_pre90": sum((rec.get(c) or 0.0) for c in MEX_PRE90),
        })
    co = pd.DataFrame(rows).merge(load_cbsa(), on="cofips", how="inner")
    num = [c for c in co.columns if c not in ("cofips", "cbsa", "cbsa_title")]
    g = co.groupby(["cbsa", "cbsa_title"], as_index=False)[num].sum(min_count=1)
    print("metro counties aggregated:", len(co), "-> CBSAs:", len(g))

    # national pre-1990 denominators come from ALL counties, not only metro ones,
    # so a metro's base share is its share of the whole national pre-1990 stock
    allco = pd.DataFrame(rows)
    natl_fb, natl_mex = allco["fb_pre90"].sum(), allco["mex_pre90"].sum()
    print("national pre-1990 stock: foreign-born %s, Mexico-born %s"
          % (format(int(natl_fb), ","), format(int(natl_mex), ",")))
    base = g[["cbsa", "fb_pre90", "mex_pre90"]].copy()
    base["fb_base_share"] = base["fb_pre90"] / natl_fb
    base["mex_base_share"] = base["mex_pre90"] / natl_mex
    base["base_vintage"] = "pre-1990-entry-cohort-observed-2000"
    base.to_csv(DERIVED / "base_shares_pre1990.csv", index=False)
    print("wrote base_shares_pre1990.csv", base.shape,
          "metro coverage of national pre-1990 stock: fb %.3f mex %.3f"
          % (base.fb_base_share.sum(), base.mex_base_share.sum()))

    panel = pd.read_csv(DERIVED / "metro_panel.csv", dtype={"cbsa": str})
    panel = panel[panel.year != 2000]
    row2000 = g.copy()
    row2000["year"] = 2000
    row2000["source"] = "sf3-2000"
    row2000["fb_share"] = 100 * row2000["fb"] / row2000["pop"]
    row2000["mex_share"] = 100 * row2000["mex"] / row2000["pop"]
    row2000["ssi_rate"] = 100 * row2000["hh_ssi"] / row2000["hh_tot"]
    row2000["pa_rate"] = 100 * row2000["hh_pa"] / row2000["hh_tot_pa"]
    out = pd.concat([panel, row2000], ignore_index=True)
    out.to_csv(DERIVED / "metro_panel.csv", index=False)
    print("panel now", out.shape, "years", sorted(out.year.unique()))
    print(row2000[["fb_share", "mex_share", "ssi_rate", "pa_rate"]].describe().round(3).to_string())


if __name__ == "__main__":
    main()
