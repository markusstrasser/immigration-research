"""Metro commute panel, 2000 and 2010, from the summary tables pulled by fetch_commute.py.

2000 endpoint: Census 2000 SF3 county tables summed to the February-2013 CBSA delineation
(metropolitan areas only), the displacement lane's 2000 geography.
2010 endpoint, two versions:
  published  ACS 2010 1-year at the CBSA published that year (2009 delineation), matched by code,
             which is how the displacement panel builds its 2010 row (see RESULT.md finding F1)
  fixed      ACS 2008-2012 5-year county tables summed to the same 2013 CBSAs as 2000
Population change for the log-population design: Census 2000 and 2010 SF1 counts by county,
summed to 2013 CBSAs (fixed geography by construction).

Mean one-way commute = aggregate minutes / workers who did not work at home
  2000  P033001 / P031002
  2010  B08013_001 / B08303_001
Non-transit mean removes public transport from both terms (2000 public transport includes taxicab,
the ACS series excludes it; taxicab is about 0.1% of commuters).

Writes derived/commute_metro.csv (one row per 2013 CBSA; published-2010 columns where the code
matches) and prints the positive checks.
"""
import json
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CEN = HERE / "_cache" / "census"
DT = HERE.parent / "displacement_transfers_2026_09_18"
DERIVED = HERE / "derived"


def load_cbsa():
    d = pd.read_excel(DT / "_cache" / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return d[["cofips", "cbsa", "CBSA Title"]].rename(columns={"CBSA Title": "cbsa_title"})


def county_frame(name):
    d = json.loads((CEN / f"{name}.json").read_text())
    f = pd.DataFrame.from_dict(d, orient="index")
    f.index.name = "cofips"
    return f.reset_index().drop(columns=["NAME"], errors="ignore")


def to_cbsa(f, cb):
    """Sum counties into CBSAs; a CBSA sum is missing unless every one of its counties reports.
    ACS 2008-2012 suppresses B08136 (aggregate minutes by mode) in about half of all counties,
    so a partial sum would silently drop counties from the numerator."""
    j = f.merge(cb, on="cofips", how="inner")
    num = [c for c in f.columns if c != "cofips"]
    g = j.groupby("cbsa")[num]
    s = g.sum(min_count=1)
    s = s.where(g.count().eq(g.size(), axis=0))
    return s.reset_index(), j.cofips.nunique()


def main():
    cb = load_cbsa()
    # ---- 2000, SF3 county -> 2013 CBSA
    sf3, n3 = to_cbsa(county_frame("sf3_2000_county"), cb)
    t0 = pd.DataFrame({"cbsa": sf3.cbsa})
    pub = sf3[["P033003", "P033006", "P033009", "P033012"]].sum(axis=1)
    t0["workers_0"] = sf3.P030001
    t0["commuters_0"] = sf3.P031002
    t0["agg_min_0"] = sf3.P033001
    t0["commute_0"] = sf3.P033001 / sf3.P031002
    t0["commute_nontransit_0"] = (sf3.P033001 - pub) / (sf3.P031002 - sf3.P030005)
    t0["commute_transit_0"] = pub / sf3.P030005
    t0["sh_transit_0"] = 100 * sf3.P030005 / sf3.P030001
    t0["sh_alone_0"] = 100 * sf3.P030003 / sf3.P030001
    t0["sh_carpool_0"] = 100 * sf3.P030004 / sf3.P030001
    t0["sh_home_0"] = 100 * sf3.P030016 / sf3.P030001
    # identity checks on the 2000 tables: P030 total = P031 total; P031002 + home = total
    c = county_frame("sf3_2000_county")
    gap1 = (c.P030001 - c.P031001).abs().max()
    gap2 = (c.P031001 - c.P031002 - c.P030016).abs().max()
    print(f"2000 SF3: counties in CBSAs {n3}; max |P030001-P031001| {gap1}; "
          f"max |P031001-P031002-P030016| {gap2}")
    # ---- populations, SF1 2000 and 2010 by county -> 2013 CBSA
    p0, _ = to_cbsa(county_frame("sf1_2000_county").rename(columns={"P001001": "pop_sf1_0"}), cb)
    p1, _ = to_cbsa(county_frame("sf1_2010_county").rename(columns={"P001001": "pop_sf1_1"}), cb)
    # ---- 2010 fixed geography, ACS 2008-2012 county -> 2013 CBSA
    a5, n5 = to_cbsa(county_frame("acs5_2012_county"), cb)
    t1 = pd.DataFrame({"cbsa": a5.cbsa})
    t1["commute_1f"] = a5.B08013_001E / a5.B08303_001E
    t1["commute_nontransit_1f"] = ((a5.B08136_001E - a5.B08136_007E)
                                   / (a5.B08303_001E - a5.B08301_010E))
    t1["commute_transit_1f"] = a5.B08136_007E / a5.B08301_010E
    t1["commute_alone_1f"] = a5.B08136_003E / a5.B08301_003E
    t1["sh_transit_1f"] = 100 * a5.B08301_010E / a5.B08301_001E
    t1["sh_alone_1f"] = 100 * a5.B08301_003E / a5.B08301_001E
    t1["sh_carpool_1f"] = 100 * a5.B08301_004E / a5.B08301_001E
    t1["sh_home_1f"] = 100 * a5.B08301_021E / a5.B08301_001E
    t1["fb_share_1f"] = 100 * a5.B05002_013E / a5.B05002_001E
    t1["mex_share_1f"] = 100 * a5.B05006_137E / a5.B05002_001E
    t1["ssi_rate_1f"] = 100 * a5.B19056_002E / a5.B19056_001E
    t1["pa_rate_1f"] = 100 * a5.B19057_002E / a5.B19057_001E
    t1["pop_acs5_1"] = a5.B01003_001E
    print(f"2010 ACS 5-year: counties in CBSAs {n5}")
    # ---- 2010 published CBSA (2009 delineation), ACS 1-year
    a1 = pd.DataFrame.from_dict(json.loads((CEN / "acs1_2010_cbsa.json").read_text()), orient="index")
    a1.index.name = "cbsa"
    a1 = a1.reset_index()
    tp = pd.DataFrame({"cbsa": a1.cbsa, "cbsa_title_2010": a1.NAME})
    tp["commute_1p"] = a1.B08013_001E / a1.B08303_001E
    tp["commute_nontransit_1p"] = ((a1.B08136_001E - a1.B08136_007E)
                                   / (a1.B08303_001E - a1.B08301_010E))
    tp["commute_alone_1p"] = a1.B08136_003E / a1.B08301_003E
    tp["sh_transit_1p"] = 100 * a1.B08301_010E / a1.B08301_001E
    tp["sh_alone_1p"] = 100 * a1.B08301_003E / a1.B08301_001E
    tp["sh_carpool_1p"] = 100 * a1.B08301_004E / a1.B08301_001E
    tp["sh_home_1p"] = 100 * a1.B08301_021E / a1.B08301_001E
    tp["pop_acs1_1"] = a1.B01003_001E
    tp["fb_share_1p"] = 100 * a1.B05002_013E / a1.B05002_001E
    out = (t0.merge(p0, on="cbsa", how="left").merge(p1, on="cbsa", how="left")
           .merge(t1, on="cbsa", how="left").merge(tp, on="cbsa", how="left"))
    out = out.merge(cb.drop_duplicates("cbsa")[["cbsa", "cbsa_title"]], on="cbsa", how="left")
    out["dlnpop_sf1"] = np.log(out.pop_sf1_1) - np.log(out.pop_sf1_0)
    out = out.replace([np.inf, -np.inf], np.nan)
    # positive control: the published 2010 fb share for matched codes must agree with the panel's
    panel = pd.read_csv(DT / "derived" / "metro_panel.csv", dtype={"cbsa": str})
    p10 = panel[panel.year == 2010][["cbsa", "fb_share"]].merge(tp[["cbsa", "fb_share_1p"]], on="cbsa")
    dev = (p10.fb_share - p10.fb_share_1p).abs().max()
    print(f"published 2010 fb share vs displacement panel: {len(p10)} codes, max |diff| {dev:.2e}")
    if dev > 1e-6:
        raise SystemExit("[BLOCKED] 2010 published fb share does not match the displacement panel")
    DERIVED.mkdir(exist_ok=True)
    out.to_csv(DERIVED / "commute_metro.csv", index=False)
    w = out.pop_sf1_0.fillna(0)
    print(f"wrote commute_metro.csv {out.shape}; population-weighted means:")
    for c in ["commute_0", "commute_1f", "commute_1p", "commute_nontransit_0", "commute_nontransit_1f",
              "sh_transit_0", "sh_transit_1f", "sh_home_0", "sh_home_1f", "dlnpop_sf1"]:
        m = out[c].notna() & (w > 0)
        print(f"  {c:24s} {np.average(out.loc[m, c], weights=w[m]):8.3f}  (n {m.sum()})")


if __name__ == "__main__":
    main()
