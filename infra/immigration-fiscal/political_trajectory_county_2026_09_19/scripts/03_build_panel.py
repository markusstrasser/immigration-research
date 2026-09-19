#!/usr/bin/env python3
"""Arm 1 step 3: build the balanced county x election-year panel 2000-2024.

Votes:   MEDSL 2000-2016 (its own GitHub mirror) + tonmcg 2020, 2024.
Compo.:  decennial 2000 and 2010 SF1; ACS 5-year 2009/2014/2018/2022/2023 matched
         to the election year at the 5-year window's midpoint.
         2004 is interpolated between the two decennials (weight 0.4).

Geography harmonisation, all stated rather than silently applied:
  - Alaska (FIPS 02) dropped: the returns are reported by state house district,
    not by borough, in both vote sources.
  - Connecticut (FIPS 09) dropped: ACS 5-year 2022 and 2023 report the nine
    planning regions (09110-09190) while the election returns still use the eight
    old counties (09001-09015); there is no clean crosswalk inside this lane.
  - 46102 Oglala Lakota (post-2015) mapped to 46113 Shannon (pre-2015).
  - 51515 Bedford city (independent until 2013) summed into 51019 Bedford County
    in every year and every data source.
  - The panel is then restricted to counties observed in all 7 election years and
    all composition vintages (balanced), so entry/exit cannot drive a trend.

Output: derived/county_panel.csv, derived/panel_build_log.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache"
DER = LANE / "derived"

ELECTIONS = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
ACS_FOR_ELECTION = {2008: 2009, 2012: 2014, 2016: 2018, 2020: 2022, 2024: 2023}
DROP_STATES = {"02", "09"}
FIPS_MAP = {"46102": "46113", "51515": "51019"}
LOG: list[str] = []


def log(msg: str) -> None:
    print(msg, flush=True)
    LOG.append(msg)


def harmonise(fips: pd.Series) -> pd.Series:
    return fips.replace(FIPS_MAP)


def load_votes() -> pd.DataFrame:
    med = pd.read_csv(CACHE / "countypres_2000-2016.csv", low_memory=False)
    med = med[med.FIPS.notna()].copy()
    med["fips"] = med.FIPS.astype(int).astype(str).str.zfill(5)
    med = med[med.party.isin(["democrat", "republican"])]
    votes = (med.groupby(["year", "fips", "party"]).candidatevotes.sum()
             .unstack().rename(columns={"democrat": "dem", "republican": "rep"}))
    tot = med.groupby(["year", "fips"]).totalvotes.max()
    a = votes.join(tot).reset_index()
    a = a.rename(columns={"totalvotes": "total_votes"})

    parts = [a]
    for y in (2020, 2024):
        t = pd.read_csv(CACHE / f"tonmcg_{y}.csv", dtype=str)
        if "county_fips" not in t.columns:
            t = t.rename(columns={"combined_fips": "county_fips"})
        t["fips"] = t.county_fips.str.split(".").str[0].str.zfill(5)
        for c in ("votes_dem", "votes_gop", "total_votes"):
            t[c] = pd.to_numeric(t[c], errors="coerce")
        parts.append(pd.DataFrame({"year": y, "fips": t.fips, "dem": t.votes_dem,
                                   "rep": t.votes_gop,
                                   "total_votes": t.total_votes}))
    v = pd.concat(parts, ignore_index=True)
    v["fips"] = harmonise(v.fips)
    v = v[~v.fips.str[:2].isin(DROP_STATES)]
    v = v.groupby(["year", "fips"], as_index=False)[["dem", "rep", "total_votes"]].sum()
    log(f"votes: {len(v):,} county-year rows, "
        + ", ".join(f"{y}:{(v.year == y).sum()}" for y in ELECTIONS))
    return v


def acs_frame(y: int) -> pd.DataFrame:
    a = pd.read_csv(CACHE / f"census_county_acs5_{y}.csv", dtype={"fips": str})
    out = pd.DataFrame({"fips": a.fips})
    out["pop"] = a["B03002_001E"]
    out["mex"] = a["B03001_004E"]
    out["hisp"] = a["B03002_012E"]
    out["nhwhite"] = a["B03002_003E"]
    out["vap"] = a["B05003_008E"] + a["B05003_019E"]
    out["cvap"] = (a["B05003_009E"] + a["B05003_011E"]
                   + a["B05003_020E"] + a["B05003_022E"])
    if "B05003I_008E" in a.columns:
        out["hisp_vap"] = a["B05003I_008E"] + a["B05003I_019E"]
        out["hisp_cvap"] = (a["B05003I_009E"] + a["B05003I_011E"]
                            + a["B05003I_020E"] + a["B05003I_022E"])
    else:
        out["hisp_vap"] = np.nan
        out["hisp_cvap"] = np.nan
    out["med_income"] = a["B19013_001E"]
    return out


def dec_frame(y: int) -> pd.DataFrame:
    d = pd.read_csv(CACHE / f"census_county_dec_{y}.csv", dtype={"fips": str})
    hisp_col = "P004002" if y == 2000 else "P004003"
    return pd.DataFrame({"fips": d.fips, "pop": d["P001001"],
                         "mex": d["PCT011004"], "hisp": d[hisp_col]})


def collapse(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fips"] = harmonise(df.fips)
    df = df[~df.fips.str[:2].isin(DROP_STATES)]
    num = [c for c in df.columns if c not in ("fips", "med_income")]
    g = df.groupby("fips", as_index=False)[num].sum(min_count=1)
    if "med_income" in df.columns:          # population-weighted for the merged pair
        w = df.assign(w=df["pop"].fillna(0) * df["med_income"].fillna(0))
        mi = (w.groupby("fips").w.sum()
              / w.groupby("fips")["pop"].sum().replace(0, np.nan))
        g = g.merge(mi.rename("med_income"), on="fips", how="left")
    return g


def load_composition() -> pd.DataFrame:
    d00, d10 = collapse(dec_frame(2000)), collapse(dec_frame(2010))
    frames = []
    for y in ELECTIONS:
        if y == 2000:
            c = d00.copy()
            c["source"] = "dec2000"
        elif y == 2004:
            j = d00.merge(d10, on="fips", suffixes=("_00", "_10"))
            c = pd.DataFrame({"fips": j.fips})
            for v in ("pop", "mex", "hisp"):
                c[v] = 0.6 * j[f"{v}_00"] + 0.4 * j[f"{v}_10"]
            c["source"] = "interp dec2000/dec2010"
        else:
            c = collapse(acs_frame(ACS_FOR_ELECTION[y]))
            c["source"] = f"acs5_{ACS_FOR_ELECTION[y]}"
        c["year"] = y
        frames.append(c)
    comp = pd.concat(frames, ignore_index=True)
    log("composition rows by year: "
        + ", ".join(f"{y}:{(comp.year == y).sum()}" for y in ELECTIONS))
    return comp


def main() -> int:
    DER.mkdir(exist_ok=True)
    v, comp = load_votes(), load_composition()
    p = v.merge(comp, on=["year", "fips"], how="inner")
    log(f"merged: {len(p):,} rows before balancing")

    counts = p.groupby("fips").year.nunique()
    keep = set(counts[counts == len(ELECTIONS)].index)
    dropped = sorted(set(p.fips) - keep)
    log(f"balanced panel: {len(keep):,} counties x {len(ELECTIONS)} years; "
        f"{len(dropped)} counties dropped for incomplete coverage")
    log("  dropped (first 25): " + ", ".join(dropped[:25]))
    p = p[p.fips.isin(keep)].copy()

    # a county with no votes or no population in any year cannot be used
    bad = p[(p[["dem", "rep"]].sum(axis=1) <= 0) | (p["pop"].isna()) | (p["pop"] <= 0)]
    if len(bad):
        log(f"  dropping {bad.fips.nunique()} counties with a zero-vote or "
            f"zero-population year: {sorted(bad.fips.unique())[:15]}")
        p = p[~p.fips.isin(set(bad.fips))]

    p["state"] = p.fips.str[:2]
    p["dem2p"] = p.dem / (p.dem + p.rep)
    p["mex_share"] = p.mex / p["pop"]
    p["hisp_share"] = p.hisp / p["pop"]
    p["turnout_cvap"] = np.where(p.cvap > 0, p.total_votes / p.cvap, np.nan)
    p["votes_per_pop"] = p.total_votes / p["pop"]
    p["nhwhite_share"] = p.nhwhite / p["pop"]
    p["mex_share_of_hisp"] = np.where(p.hisp > 0, p.mex / p.hisp, np.nan)
    p = p.sort_values(["fips", "year"]).reset_index(drop=True)

    log(f"final panel: {p.fips.nunique():,} counties, {len(p):,} rows")
    nat = p.groupby("year").apply(
        lambda d: pd.Series({
            "dem2p_pw": d.dem.sum() / (d.dem.sum() + d.rep.sum()),
            "mex_share_pw": d.mex.sum() / d["pop"].sum(),
            "turnout_cvap_pw": (d.total_votes.sum() / d.cvap.sum()
                                if d.cvap.notna().any() else np.nan)}),
        include_groups=False)
    log("panel-wide (population-weighted) series:\n" + nat.round(4).to_string())

    p.to_csv(DER / "county_panel.csv", index=False, float_format="%.6g")
    size = (DER / "county_panel.csv").stat().st_size / 1e6
    log(f"wrote derived/county_panel.csv ({size:.2f} MB)")
    if size > 5:
        sys.exit("FAIL panel over the 5 MB lane limit")
    (DER / "panel_build_log.txt").write_text("\n".join(LOG) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
