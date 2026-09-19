#!/usr/bin/env python3
"""Shared sample construction, controls and instruments for the hedonic lane."""
import pathlib
import numpy as np
import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent.parent
DERIVED = LANE / "derived"

QUAL_D = ["d_own_rate", "d_vac_rate", "d_sfdet_share", "d_medyrbuilt"]
LEV0 = ["own_rate_0", "vac_rate_0", "sfdet_share_0", "medyrbuilt_0",
        "log_inc_0", "ba_share_0", "log_dens_0", "nhwhite_share_0"]
ORIGINS = ["afr", "asia", "carib", "camer", "eur", "mex", "namer", "oce", "samer"]
TREATS = {"fb": "d_fb_share", "hisp": "d_hisp_share", "mex": "d_mex_share"}


def load():
    p = pd.read_csv(DERIVED / "tract_panel.csv",
                    dtype={"geoid": str, "cbsa": str, "county_fips": str})
    p = p[(p["is_metro"] == 1) & p["cbsa"].notna()].copy()

    for v in ["hisp_share", "fb_share", "mex_share", "nhwhite_share", "own_rate",
              "vac_rate", "sfdet_share", "ba_share", "log_dens", "medyrbuilt"]:
        p[f"d_{v}"] = p[f"{v}_1"] - p[f"{v}_0"]
        p[f"{v}_0"] = p[f"{v}_0"]
    p["d_medyrbuilt"] = p["d_medyrbuilt"] / 10.0
    p["medyrbuilt_0"] = (p["medyrbuilt_0"] - 1970.0) / 10.0
    p["log_inc_0"] = np.log(p["med_inc_0"].where(p["med_inc_0"] > 0))
    p["log_inc_1"] = np.log(p["med_inc_1"].where(p["med_inc_1"] > 0))
    p["d_log_inc"] = p["log_inc_1"] - p["log_inc_0"]
    for out in ["rent", "value"]:
        a = p[f"med_{out}_0"].where(p[f"med_{out}_0"] > 0)
        b = p[f"med_{out}_1"].where(p[f"med_{out}_1"] > 0)
        p[f"log_{out}_0"] = np.log(a)
        p[f"dlog_{out}"] = np.log(b) - np.log(a)
    p["cbsa_period"] = p["cbsa"] + "_" + p["period"]

    # CBSA-period immigration intensity (Saiz-Wachter sample rule, 5-year analogue)
    g = p.groupby("cbsa_period")
    agg = g.agg(fb0=("fb_count_0", "sum"), fb1=("fb_count_1", "sum"),
                pop0=("pop_0", "sum"), pop1=("pop_1", "sum"))
    agg["msa_imm_pc"] = (agg["fb1"] - agg["fb0"]) / agg["pop0"].where(agg["pop0"] > 0)
    # Saiz-Wachter select MSAs whose decennial foreign-born increase was >=5% of
    # prior MSA population; in 2000 that kept 67 MSAs holding 76.5% of metro
    # immigration. Immigration in 2013-2023 is far smaller relative to population,
    # so a fixed 5% (or its 2.5% five-year analogue) keeps almost nothing. We keep
    # the paper's COVERAGE target instead of its threshold: the lowest cutoff whose
    # selected CBSA-periods hold >=76.5% of metro foreign-born growth.
    growth = (agg["fb1"] - agg["fb0"]).clip(lower=0)
    total = growth.sum()
    order = agg["msa_imm_pc"].sort_values(ascending=False)
    cum = growth.reindex(order.index).cumsum() / total if total > 0 else growth * 0
    hit = cum[cum >= 0.765]
    cut = float(order.loc[hit.index[0]]) if len(hit) else float(order.min())
    agg["sw_sample"] = (agg["msa_imm_pc"] >= cut).astype(int)
    agg.attrs["sw_cut"] = cut
    p = p.merge(agg[["msa_imm_pc", "sw_sample"]], left_on="cbsa_period", right_index=True)
    p.attrs["sw_cut"] = agg.attrs["sw_cut"]
    p.attrs["sw_n"] = int(agg["sw_sample"].sum())
    p.attrs["sw_total"] = int(len(agg))
    return p


def valid(p, outcome):
    w = "own_units_0" if outcome == "value" else "rent_units_0"
    need = (["dlog_" + outcome, f"log_{outcome}_0", "d_fb_share", "d_hisp_share",
             "d_mex_share", "fb_share_0", "hisp_share_0", "msa_imm_pc", w]
            + QUAL_D + LEV0)
    m = p[need].notna().all(axis=1)
    m &= (p["pop_0"] >= 500) & (p["pop_1"] >= 500) & (p[w] >= 50)
    d = p[m].copy()
    d["_w"] = d[w].astype(float)
    # keep only CBSA-periods with at least 10 usable tracts (FE needs within variation)
    n = d.groupby("cbsa_period")["_w"].transform("size")
    return d[n >= 10].copy()


def haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.7613
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def gravity_pull(d, share_col, beta, min_miles=0.25):
    """Saiz-Wachter Pull_i = sum_{j != i} share_j,T-5 * Area_j / d_ij^beta.

    Computed within CBSA-period, which is the level the fixed effects absorb.
    """
    out = pd.Series(np.nan, index=d.index)
    for key, blk in d.groupby("cbsa_period", sort=True):
        lat = blk["lat_0"].to_numpy(float); lon = blk["lon_0"].to_numpy(float)
        sh = blk[share_col].to_numpy(float)
        ar = blk["aland_sqmi_0"].to_numpy(float)
        ok = np.isfinite(lat) & np.isfinite(lon) & np.isfinite(sh) & np.isfinite(ar)
        n = len(blk)
        vals = np.full(n, np.nan)
        idx = np.where(ok)[0]
        if len(idx) >= 2:
            la, lo = lat[idx], lon[idx]
            D = haversine_miles(la[:, None], lo[:, None], la[None, :], lo[None, :])
            np.fill_diagonal(D, np.inf)
            D = np.maximum(D, min_miles)
            W = 1.0 / D ** beta
            vals[idx] = W @ (sh[idx] * ar[idx])
        out.loc[blk.index] = vals
    return out / 1000.0


def shift_share(d):
    """Card-style exposure instrument: base origin shares x national origin growth."""
    nat0 = {o: d[f"fb_{o}_0"].sum() for o in ORIGINS}
    nat1 = {o: d[f"fb_{o}_1"].sum() for o in ORIGINS}
    g = {o: (nat1[o] - nat0[o]) / nat0[o] if nat0[o] > 0 else 0.0 for o in ORIGINS}
    pop0 = d["pop_0"].where(d["pop_0"] > 0)
    shares = {o: (d[f"fb_{o}_0"] / pop0).fillna(0.0) for o in ORIGINS}
    bartik = sum(shares[o] * g[o] for o in ORIGINS)
    return bartik, g, shares


def standardize(d, cols):
    z = pd.DataFrame(index=d.index)
    for c in cols:
        v = d[c].astype(float)
        s = v.std()
        z[c] = (v - v.mean()) / (s if s and np.isfinite(s) and s > 0 else 1.0)
    return z
