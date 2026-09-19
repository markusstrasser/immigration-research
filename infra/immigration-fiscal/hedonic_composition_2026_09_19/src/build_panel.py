#!/usr/bin/env python3
"""Assemble the tract long-difference panel on fixed 2010 tract definitions.

Periods: A = ACS 2009-2013 -> 2014-2018 (both native 2010 tracts, no crosswalk)
         B = ACS 2014-2018 -> 2019-2023 (2023 aggregated to 2010 parents)

Writes derived/tract_panel.csv and derived/build_panel_report.txt.
"""
import json, pathlib
import numpy as np
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent.parent
CACHE, DERIVED = LANE / "_cache", LANE / "derived"
YEARS = [2013, 2018, 2023]
MISSING = [-666666666, -999999999, -888888888, -222222222, -333333333, -555555555]

COUNT_VARS = ["B03002_001E", "B03002_003E", "B03002_012E", "B05002_001E", "B05002_013E",
              "B25003_001E", "B25003_002E", "B25003_003E", "B15003_001E", "B15003_022E",
              "B15003_023E", "B15003_024E", "B15003_025E", "B25002_001E", "B25002_003E",
              "B25024_001E", "B25024_002E", "B03001_004E"]
# median -> weight column used when aggregating 2020 tracts into 2010 parents
MEDIAN_WEIGHT = {"B25064_001E": "B25003_003E", "B25077_001E": "B25003_002E",
                 "B19013_001E": "B25003_001E", "B25035_001E": "B25002_001E"}
ORIGINS = ["afr", "asia", "carib", "camer", "eur", "mex", "namer", "oce", "samer"]


def load_year(year, b05map):
    frames = []
    for path in sorted((CACHE / "acs" / str(year)).glob("*.json")):
        rows = json.load(open(path))
        frames.append(pd.DataFrame(rows[1:], columns=rows[0]))
    d = pd.concat(frames, ignore_index=True)
    d["geoid"] = (d["state"].str.zfill(2) + d["county"].str.zfill(3)
                  + d["tract"].str.zfill(6))
    keep = COUNT_VARS + list(MEDIAN_WEIGHT)
    rename = {}
    for o in ORIGINS:
        vid = b05map[str(year)][o]
        keep.append(vid)
        rename[vid] = f"fb_{o}"
    out = d[["geoid"] + keep].copy()
    for c in keep:
        out[c] = pd.to_numeric(out[c], errors="coerce")
        out.loc[out[c].isin(MISSING), c] = np.nan
    return out.rename(columns=rename)


def to_tract10(d, xwalk):
    """Aggregate 2020-tract rows into their dominant 2010 parent."""
    m = d.merge(xwalk, left_on="geoid", right_on="tract20", how="inner")
    counts = [c for c in m.columns if c in COUNT_VARS or c.startswith("fb_")]
    agg = m.groupby("tract10")[counts].sum(min_count=1)
    for med, wcol in MEDIAN_WEIGHT.items():
        w = m[wcol].fillna(0).where(m[med].notna(), 0)
        num = (m[med].fillna(0) * w).groupby(m["tract10"]).sum()
        den = w.groupby(m["tract10"]).sum()
        agg[med] = (num / den.where(den > 0)).round(2)
    return agg.reset_index().rename(columns={"tract10": "geoid"})


def derive(d, geo):
    d = d.merge(geo, left_on="geoid", right_on="tract10", how="left").drop(columns="tract10")
    pop = d["B03002_001E"]
    out = pd.DataFrame({"geoid": d["geoid"]})
    out["pop"] = pop
    out["hisp_share"] = d["B03002_012E"] / pop.where(pop > 0)
    out["nhwhite_share"] = d["B03002_003E"] / pop.where(pop > 0)
    out["mex_share"] = d["B03001_004E"] / pop.where(pop > 0)
    nat = d["B05002_001E"]
    out["fb_share"] = d["B05002_013E"] / nat.where(nat > 0)
    out["fb_count"] = d["B05002_013E"]
    hh = d["B25003_001E"]
    out["own_units"] = d["B25003_002E"]
    out["rent_units"] = d["B25003_003E"]
    out["hh"] = hh
    out["own_rate"] = d["B25003_002E"] / hh.where(hh > 0)
    hu = d["B25002_001E"]
    out["vac_rate"] = d["B25002_003E"] / hu.where(hu > 0)
    su = d["B25024_001E"]
    out["sfdet_share"] = d["B25024_002E"] / su.where(su > 0)
    ed = d["B15003_001E"]
    out["ba_share"] = (d[["B15003_022E", "B15003_023E", "B15003_024E", "B15003_025E"]]
                       .sum(axis=1, min_count=1) / ed.where(ed > 0))
    out["medyrbuilt"] = d["B25035_001E"]
    out["med_rent"] = d["B25064_001E"]
    out["med_value"] = d["B25077_001E"]
    out["med_inc"] = d["B19013_001E"]
    out["aland_sqmi"] = d["aland_sqmi"]
    out["lat"], out["lon"] = d["lat"], d["lon"]
    out["log_dens"] = np.log((pop / d["aland_sqmi"].where(d["aland_sqmi"] > 0))
                             .where(lambda s: s > 0))
    for o in ORIGINS:
        out[f"fb_{o}"] = d[f"fb_{o}"]
    return out


def topcode_mask(s, name, log):
    """Flag values sitting at a repeated series maximum (ACS top code)."""
    v = s.dropna()
    if v.empty:
        return pd.Series(False, index=s.index)
    hi = v.max()
    n = int((v == hi).sum())
    if n >= 20:
        log.append(f"  top code {name}: {hi:.0f} on {n} tracts (dropped)")
        return s == hi
    return pd.Series(False, index=s.index)


def main():
    log = []
    b05map = json.load(open(CACHE / "b05006_manifest.json"))
    geo = pd.read_csv(DERIVED / "geo_tract2010.csv", dtype={"tract10": str})
    xwalk = pd.read_csv(DERIVED / "geo_tract20_to_tract10.csv",
                        dtype={"tract20": str, "tract10": str})
    cbsa = pd.read_csv(DERIVED / "geo_county_cbsa_2013.csv", dtype={"county_fips": str,
                                                                   "cbsa": str})
    wide = {}
    for y in YEARS:
        raw = load_year(y, b05map)
        log.append(f"[{y}] raw rows={len(raw)}")
        if y == 2023:
            raw = to_tract10(raw, xwalk)
            log.append(f"[{y}] aggregated to 2010 parents: {len(raw)}")
        d = derive(raw, geo)
        for col, nm in [("med_rent", f"rent{y}"), ("med_value", f"value{y}")]:
            d.loc[topcode_mask(d[col], nm, log), col] = np.nan
        wide[y] = d
        log.append(f"[{y}] tracts with geo={d['aland_sqmi'].notna().sum()}")

    panel = []
    for label, t0, t1 in [("A", 2013, 2018), ("B", 2018, 2023)]:
        a = wide[t0].add_suffix("_0").rename(columns={"geoid_0": "geoid"})
        b = wide[t1].add_suffix("_1").rename(columns={"geoid_1": "geoid"})
        m = a.merge(b, on="geoid", how="inner")
        m["period"] = label
        m["t0"], m["t1"] = t0, t1
        panel.append(m)
        log.append(f"[period {label}] merged tracts={len(m)}")
    p = pd.concat(panel, ignore_index=True)
    p["county_fips"] = p["geoid"].str[:5]
    p = p.merge(cbsa, on="county_fips", how="left")
    log.append(f"[panel] rows={len(p)} in-CBSA={p['cbsa'].notna().sum()} "
               f"metro={int((p['is_metro'] == 1).sum())}")
    p = p.sort_values(["period", "geoid"]).reset_index(drop=True)
    p.to_csv(DERIVED / "tract_panel.csv", index=False, float_format="%.6g")
    (DERIVED / "build_panel_report.txt").write_text("\n".join(log) + "\n")
    print("\n".join(log), flush=True)
    print(f"[panel] written rows={len(p)} cols={p.shape[1]}", flush=True)


if __name__ == "__main__":
    main()
