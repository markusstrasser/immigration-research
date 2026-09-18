"""Metro panel from the PUMA-level PUMS cells: nativity-split transfer receipt, and
wages of Mexico-born workers split by arrival cohort.

This is the panel that fixes the composition problem in the aggregate route. Section 4's
transfer outcomes count ALL households, immigrants included, so a negative coefficient can
be the mechanical effect of adding low-take-up immigrant households to the denominator.
Here the outcome is receipt among NATIVES only, so that channel is closed by construction.

Geography: PUMA -> county by Geocorr population allocation factor for the PUMA vintage in
force that year, then county -> the fixed OMB February-2013 CBSA delineation, metropolitan
areas only. Identical chain to the employment_entry lane, so the two panels are comparable.
  PUMA vintage: 2005-2011 -> puma2k, 2012-2021 -> puma12, 2022+ -> puma22.

Outcomes (natives aged 25-54 below a bachelor's degree):
  nat_epop, nat_lfp          employment and labour-force rates, points
  nat_ssi, nat_pa, nat_snap  percent receiving SSI / public assistance / SNAP
Design B outcomes (Mexico-born aged 25-54, by year of entry before/after 2000):
  mx_pre_ftfy_wage           mean annual wage of full-time full-year earners, dollars
  mx_pre_wage_pp             mean wage per person including non-earners
  mx_pre_nc_wage_pp          mean wage per person, below a bachelor's degree
  and the same for the post-2000 arrival cohort
"""
import pathlib, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
VINT = {2005: "puma2k", 2008: "puma2k", 2021: "puma12", 2024: "puma22"}
SUMS = ["2554_nc_pop", "2554_nc_emp", "2554_nc_lf", "2554_nc_ssi", "2554_nc_pa",
        "2554_nc_snap"] + [f"mx_{c}_{m}" for c in ("pre2000", "post2000")
                           for m in ("n", "emp", "wagesum", "ftfy_n", "ftfy_wagesum",
                                     "nc_n", "nc_wagesum")]


def load_xwalks():
    out = {}
    for v in ("puma2k", "puma12", "puma22"):
        df = pd.read_csv(CACHE / f"xwalk_{v}.csv", dtype=str)
        pc = [c for c in df.columns if c.lower().startswith("puma")][0]
        df = df.rename(columns={pc: "puma", "county": "cofips"})
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
    files = sorted((CACHE / "cells2").glob("cells_*.csv"))
    if not files:
        sys.exit("no cell files")
    cells = pd.concat((pd.read_csv(f, dtype={"state": str, "puma": str}) for f in files),
                      ignore_index=True)
    cells["state"] = cells["state"].str.zfill(2)
    cells["puma"] = cells["puma"].str.zfill(5)
    # A metro is only comparable across years if EVERY state it spans was pulled in EVERY
    # year kept. Rather than drop a whole year for one missing state, drop the metros that
    # touch any state missing from any kept year, and say which.
    cov = cells.groupby("year")["state"].nunique()
    full = set(cov[cov >= 45].index)
    print("state coverage by year:", cov.to_dict(), "-> keeping years", sorted(full))
    cells = cells[cells["year"].isin(full)]
    pulled = cells.groupby("year")["state"].apply(frozenset)
    common = frozenset.intersection(*pulled.tolist())
    missing = sorted(set().union(*pulled.tolist()) - common)
    if missing:
        print("states missing from at least one kept year, metros touching them dropped:",
              missing)
    cells = cells[cells["state"].isin(common)]
    cells["vint"] = cells["year"].map(VINT)
    xw = load_xwalks()
    parts = []
    for v, g in cells.groupby("vint"):
        m = g.merge(xw[v], on=["state", "puma"], how="left", indicator=True)
        print(f"  {v}: puma-county merge miss rate {(m['_merge']!='both').mean():.4f}")
        m = m[m["_merge"] == "both"].drop(columns="_merge")
        for c in SUMS:
            m[c] = m[c] * m["afact"]
        parts.append(m)
    alloc = pd.concat(parts, ignore_index=True)
    cb = load_cbsa()
    # drop every CBSA that contains a county in a state absent from any kept year
    cb_states = cb.assign(st=cb.cofips.str[:2]).groupby("cbsa")["st"].apply(frozenset)
    ok = {c for c, sts in cb_states.items() if sts <= common}
    dropped = len(cb_states) - len(ok)
    print(f"CBSAs dropped for spanning an unpulled state: {dropped}")
    cb = cb[cb.cbsa.isin(ok)]
    j = alloc.merge(cb, on="cofips", how="inner")
    p = j.groupby(["cbsa", "cbsa_title", "year"], as_index=False)[SUMS].sum()
    print("metro-year rows:", len(p), "distinct CBSAs:", p.cbsa.nunique())

    p["nat_epop"] = 100 * p["2554_nc_emp"] / p["2554_nc_pop"]
    p["nat_lfp"] = 100 * p["2554_nc_lf"] / p["2554_nc_pop"]
    p["nat_ssi"] = 100 * p["2554_nc_ssi"] / p["2554_nc_pop"]
    p["nat_pa"] = 100 * p["2554_nc_pa"] / p["2554_nc_pop"]
    p["nat_snap"] = 100 * p["2554_nc_snap"] / p["2554_nc_pop"]
    for coh, tag in (("pre2000", "pre"), ("post2000", "post")):
        p[f"mx_{tag}_ftfy_wage"] = p[f"mx_{coh}_ftfy_wagesum"] / p[f"mx_{coh}_ftfy_n"]
        p[f"mx_{tag}_wage_pp"] = p[f"mx_{coh}_wagesum"] / p[f"mx_{coh}_n"]
        p[f"mx_{tag}_nc_wage_pp"] = p[f"mx_{coh}_nc_wagesum"] / p[f"mx_{coh}_nc_n"]
        p[f"mx_{tag}_n"] = p[f"mx_{coh}_n"]
        p[f"mx_{tag}_epop"] = 100 * p[f"mx_{coh}_emp"] / p[f"mx_{coh}_n"]
    p["nat_pop"] = p["2554_nc_pop"]
    p = p.replace([np.inf, -np.inf], np.nan)
    p.to_csv(DERIVED / "pums_metro_panel.csv", index=False)
    print("wrote pums_metro_panel.csv", p.shape)
    cols = ["nat_epop", "nat_lfp", "nat_ssi", "nat_pa", "nat_snap",
            "mx_pre_ftfy_wage", "mx_pre_wage_pp", "mx_post_ftfy_wage"]
    print(p.groupby("year")[cols].mean().round(2).to_string())


if __name__ == "__main__":
    main()
