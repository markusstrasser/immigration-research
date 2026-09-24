#!/usr/bin/env python3
"""Question 2: does the share of movers citing "wanted better neighborhood/less crime" rise with
the Mexican-origin (or Hispanic) share where they lived? Descriptive linear probability models.

The CPS identifies an interstate mover's origin only to the state, so two designs stand in for the
brief's origin-county design:
  A. origin state: US-born adult interstate movers, ASEC 2006-2025, origin-state composition
     (ACS 5-year ending the year before the survey; 2005-2009 for surveys through 2010) and
     origin-state median gross rent, home value and household income (ACS 1-year, year before the
     survey; 2020 is the mean of 2019 and 2021). Standard errors clustered by origin state.
  B. same county: US-born adults who moved within the county they live in (MIGRATE1 = 3), in
     counties the CPS identifies from its own county code (COUNTYERR = 1), with county composition
     and controls from the ACS 5-year release ending the year before. Clustered by county.
Positive controls: "cheaper housing" on origin rent in both designs, and "change of climate" on a
cold-region origin in design A. Placebo outcome: job reasons (design A).

Writes derived/q2_regressions.csv (every specification), derived/q2_bins.csv (neighborhood share
by origin-state Mexican-origin share band), derived/q2_state_scatter.csv (one row per origin
state) and derived/q2_same_county_descriptive.csv (design B shares by state group and county
Mexican-origin share band).

Run from the repository root after reasons.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/q2_gradient.py
"""
import json

import numpy as np
import pandas as pd

from lane_common import BUILD, CACHE, GROUPS, STATES, Var, add_person_fields, con, cpi_2024, load_interstate, write_csv


def acs_table(kind: str, geo: str, year: int) -> pd.DataFrame:
    rows = json.loads((CACHE / "acs" / f"{kind}_{geo}_{year}.json").read_text())
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in df.columns:
        if c.startswith("B"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df.loc[df[c] < 0, c] = np.nan  # ACS jam values for medians
    df["fips"] = df.state.astype(int) * (1000 if geo == "county" else 1) + (df.county.astype(int) if geo == "county" else 0)
    df["mex_share"] = 100 * df.B03001_004E / df.B03001_001E
    df["hisp_share"] = 100 * df.B03001_003E / df.B03001_001E
    df["ln_rent"] = np.log(df.B25064_001E)
    df["ln_value"] = np.log(df.B25077_001E)
    df["ln_inc"] = np.log(df.B19013_001E)
    return df.set_index("fips")[["mex_share", "hisp_share", "ln_rent", "ln_value", "ln_inc", "B01003_001E"]]


def geo_panel(geo: str) -> pd.DataFrame:
    """One row per (survey year, fips): composition from ACS 5-year ending t-1 (floor 2009),
    controls from ACS 1-year t-1 for states (2020 = mean of 2019, 2021) and ACS 5-year for counties."""
    out = []
    for t in range(2006, 2026):
        v5 = min(max(2009, t - 1), 2024)
        a5 = acs_table("acs5", geo, v5)
        comp = a5[["mex_share", "hisp_share"]]
        if geo == "state":
            y1 = t - 1
            if y1 == 2020:
                a = acs_table("acs1", geo, 2019)[["ln_rent", "ln_value", "ln_inc"]]
                b = acs_table("acs1", geo, 2021)[["ln_rent", "ln_value", "ln_inc"]]
                ctl = (a + b) / 2
            else:
                ctl = acs_table("acs1", geo, y1)[["ln_rent", "ln_value", "ln_inc"]]
        else:
            ctl = a5[["ln_rent", "ln_value", "ln_inc"]]
        p = comp.join(ctl, how="left")
        p["YEAR"] = t
        p["acs5_vintage"] = v5
        out.append(p.reset_index())
    return pd.concat(out, ignore_index=True)


def demean(M: np.ndarray, groups: np.ndarray, w: np.ndarray) -> np.ndarray:
    g = pd.Series(groups)
    codes = g.astype("category").cat.codes.to_numpy()
    sw = np.bincount(codes, weights=w)
    out = np.empty_like(M)
    for j in range(M.shape[1]):
        means = np.bincount(codes, weights=w * M[:, j]) / sw
        out[:, j] = M[:, j] - means[codes]
    return out


def wls_cluster(df: pd.DataFrame, y: str, xs: list[str], fe_dummies: list[str], absorb: str | None,
                cluster: str) -> dict:
    d = df.dropna(subset=[y] + xs + ([absorb] if absorb else [])).copy()
    w = d.wt.to_numpy(float)
    w = w / w.mean()
    X = d[xs].to_numpy(float)
    for fe in fe_dummies:
        dm = pd.get_dummies(d[fe].astype(str), drop_first=True, dtype=float)
        X = np.column_stack([X, dm.to_numpy()])
    Y = d[y].to_numpy(float)
    if absorb:
        M = demean(np.column_stack([Y, X]), d[absorb].to_numpy(), w)
        Y, X = M[:, 0], M[:, 1:]
        keep = X.std(0) > 1e-12
        if not keep[:len(xs)].all():
            raise SystemExit(f"[FAILED] {[x for x, k in zip(xs, keep) if not k]} has no variation within {absorb}")
        X = X[:, keep]
    else:
        X = np.column_stack([np.ones(len(d)), X])
    XtWX = X.T @ (X * w[:, None])
    XtWX_inv = np.linalg.pinv(XtWX)
    beta = XtWX_inv @ (X.T @ (w * Y))
    u = Y - X @ beta
    cl = d[cluster].to_numpy()
    codes = pd.Series(cl).astype("category").cat.codes.to_numpy()
    G = codes.max() + 1
    S = np.zeros((G, X.shape[1]))
    np.add.at(S, codes, X * (w * u)[:, None])
    meat = S.T @ S
    n, k = X.shape
    V = XtWX_inv @ meat @ XtWX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
    idx = 0 if absorb else 1
    res = {"n": int(n), "clusters": int(G), "mean_y_pct": round(100 * float(np.average(d[y], weights=d.wt)), 3)}
    for j, x in enumerate(xs):
        b, se = beta[idx + j], np.sqrt(V[idx + j, idx + j])
        res[x] = (float(b), float(se))
    return res


def main() -> None:
    c = con()
    cpi = cpi_2024(c)
    rows = []

    # ---------------- design A: origin state
    d = load_interstate(c, cpi)
    ua = d[d.usb & d.adult & d.YEAR.between(2006, 2025) & d.MIGSTA1.between(1, 56)].copy()
    sp = geo_panel("state").rename(columns={"fips": "MIGSTA1"})
    ua = ua.merge(sp, on=["YEAR", "MIGSTA1"], how="left")
    miss = ua.mex_share.isna().mean()
    ua["ln_hhinc"] = np.log(ua.hhinc24.clip(lower=1000))
    ua["female"] = (ua.SEX == 2).astype(float)
    ua["ca_origin"] = (ua.MIGSTA1 == 6).astype(float)
    # Census Northeast and Midwest regions: the positive control for a climate motive
    cold = {9, 23, 25, 33, 44, 50, 34, 36, 42, 17, 18, 26, 39, 55, 19, 20, 27, 29, 31, 38, 46}
    ua["cold_origin"] = ua.MIGSTA1.isin(cold).astype(float)
    ua["mex10"] = ua.mex_share / 10  # coefficient per 10 percentage points
    ua["hisp10"] = ua.hisp_share / 10
    indiv_fe = ["age_band", "educ4", "race_eth"]
    specs = [
        ("A1 origin Mexican share, year FE", "neighborhood_crime", ["mex10"], ["YEAR"], None, ua),
        ("A2 + origin rent, home value, income", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc"], ["YEAR"], None, ua),
        ("A3 + individual controls", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
        ("A4 A3 + origin-state FE (within-state change)", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, "MIGSTA1", ua),
        ("A5 A3, non-Hispanic white only", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR", "age_band", "educ4"], None, ua[ua.race_eth == "non-Hispanic white"]),
        ("A6 A3, Hispanic only", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR", "age_band", "educ4"], None, ua[ua.race_eth.str.startswith("Hispanic")]),
        ("A7 A3 with Hispanic share", "neighborhood_crime", ["hisp10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
        ("A8 A3 excluding allocated records", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua[~ua.allocated]),
        ("A9 A3 + California-origin indicator", "neighborhood_crime", ["mex10", "ca_origin", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
        ("A10 A3 excluding California origin", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua[ua.MIGSTA1 != 6]),
        ("A11 positive control: cheaper housing", "cheaper_housing", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
        ("A12 placebo outcome: jobs", "jobs", ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
        ("A13 positive control: cheaper housing on origin rent alone", "cheaper_housing", ["ln_rent"], ["YEAR"], None, ua),
        ("A14 positive control: climate on cold-region origin", "climate", ["cold_origin", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, None, ua),
    ]
    for name, y, xs, fes, absorb, df in specs:
        r = wls_cluster(df, y, xs, fes, absorb, "MIGSTA1")
        for x in xs:
            rows.append({"design": "A origin state, US-born adult interstate movers 2006-2025", "spec": name,
                         "outcome": y, "term": x, "coef_pp": round(100 * r[x][0], 3), "se_pp": round(100 * r[x][1], 3),
                         "t": round(r[x][0] / r[x][1], 2) if r[x][1] > 0 else None,
                         "n": r["n"], "clusters": r["clusters"], "mean_outcome_pct": r["mean_y_pct"]})

    # descriptive bins and the state scatter
    bins = [-1, 2, 5, 10, 20, 100]
    labels = ["under 2%", "2-5%", "5-10%", "10-20%", "20% or more"]
    ua["mex_band"] = pd.cut(ua.mex_share, bins, labels=labels).astype(str)
    b_rows = []
    for lab in labels:
        dd = ua[ua.mex_band == lab]
        th, se, _, _ = Var.ratio(dd, "neighborhood_crime")
        thc, sec, _, _ = Var.ratio(dd, "cheaper_housing")
        b_rows.append({"origin_mexican_share_band": lab, "n": len(dd), "states": int(dd.MIGSTA1.nunique()),
                       "mean_mex_share": round(float(np.average(dd.mex_share, weights=dd.wt)), 2),
                       "nbhd_crime_pct": round(100 * th, 2), "nbhd_se_pp": round(100 * se, 2),
                       "cheaper_housing_pct": round(100 * thc, 2), "cheaper_se_pp": round(100 * sec, 2)})
    write_csv(pd.DataFrame(b_rows), "q2_bins.csv")
    sc = []
    for s, dd in ua.groupby("MIGSTA1"):
        th, se, _, _ = Var.ratio(dd, "neighborhood_crime")
        sc.append({"origin_state": STATES.get(int(s), s), "n": len(dd),
                   "mean_mex_share": round(float(np.average(dd.mex_share, weights=dd.wt)), 2),
                   "mean_hisp_share": round(float(np.average(dd.hisp_share, weights=dd.wt)), 2),
                   "nbhd_crime_pct": round(100 * th, 2), "se_pp": round(100 * se, 2)})
    write_csv(pd.DataFrame(sc), "q2_state_scatter.csv")

    # ---------------- design B: movers within their own county
    m = c.execute(f"""select * from read_parquet('{BUILD / 'movers.parquet'}')
                      where MIGRATE1 = 3 and COUNTY > 0 and COUNTYERR = 1 and YEAR between 2006 and 2025""").df()
    m = add_person_fields(m, cpi)
    m = m[m.usb & m.adult].copy()
    cp = geo_panel("county").rename(columns={"fips": "COUNTY"})
    m = m.merge(cp, on=["YEAR", "COUNTY"], how="left")
    miss_b = m.mex_share.isna().mean()
    m = m.dropna(subset=["mex_share", "ln_rent"])
    m["ln_hhinc"] = np.log(m.hhinc24.clip(lower=1000))
    m["female"] = (m.SEX == 2).astype(float)
    m["mex10"] = m.mex_share / 10
    m["hisp10"] = m.hisp_share / 10
    xs_full = ["mex10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"]
    specs_b = [
        ("B1 county Mexican share, year and state FE", "neighborhood_crime", ["mex10"], ["YEAR"], "STATEFIP", m),
        ("B2 + county rent, home value, income", "neighborhood_crime", ["mex10", "ln_rent", "ln_value", "ln_inc"], ["YEAR"], "STATEFIP", m),
        ("B3 + individual controls", "neighborhood_crime", xs_full, ["YEAR"] + indiv_fe, "STATEFIP", m),
        ("B4 B3 with county FE (within-county change)", "neighborhood_crime", xs_full, ["YEAR"] + indiv_fe, "COUNTY", m),
        ("B5 B3, non-Hispanic white only", "neighborhood_crime", xs_full, ["YEAR", "age_band", "educ4"], "STATEFIP", m[m.race_eth == "non-Hispanic white"]),
        ("B6 B3, Hispanic only", "neighborhood_crime", xs_full, ["YEAR", "age_band", "educ4"], "STATEFIP", m[m.race_eth.str.startswith("Hispanic")]),
        ("B7 B3 with Hispanic share", "neighborhood_crime", ["hisp10", "ln_rent", "ln_value", "ln_inc", "ln_hhinc", "female"], ["YEAR"] + indiv_fe, "STATEFIP", m),
        ("B8 B3, California counties only", "neighborhood_crime", xs_full, ["YEAR"] + indiv_fe, None, m[m.STATEFIP == 6]),
        ("B9 positive control: cheaper housing", "cheaper_housing", xs_full, ["YEAR"] + indiv_fe, "STATEFIP", m),
        ("B10 B3 without state FE", "neighborhood_crime", xs_full, ["YEAR"] + indiv_fe, None, m),
        ("B11 positive control: cheaper housing on county rent alone", "cheaper_housing", ["ln_rent"], ["YEAR"], None, m),
    ]
    for name, y, xs, fes, absorb, df in specs_b:
        r = wls_cluster(df, y, xs, fes, absorb, "COUNTY")
        for x in xs:
            rows.append({"design": "B same-county movers, US-born adults 2006-2025, CPS-identified counties",
                         "spec": name, "outcome": y, "term": x, "coef_pp": round(100 * r[x][0], 3),
                         "se_pp": round(100 * r[x][1], 3), "t": round(r[x][0] / r[x][1], 2) if r[x][1] > 0 else None,
                         "n": r["n"], "clusters": r["clusters"], "mean_outcome_pct": r["mean_y_pct"]})
    # same-county movers: neighborhood/crime share by state group and county Mexican-origin band,
    # household-cluster SEs are replaced by county-cluster SEs (county is the sampling-relevant unit here)
    def cl_mean(dd: pd.DataFrame, y: str) -> tuple[float, float]:
        w = dd.wt.to_numpy(float)
        th = float((w * dd[y]).sum() / w.sum())
        z = w * (dd[y].to_numpy(float) - th) / w.sum()
        return th, float(np.sqrt(Var._cluster_var(z, dd.COUNTY.to_numpy())))
    m["mex_band"] = pd.cut(m.mex_share, [-1, 2, 5, 10, 20, 100],
                           labels=["under 2%", "2-5%", "5-10%", "10-20%", "20% or more"]).astype(str)
    desc = []
    for lab, dd in (("California counties", m[m.STATEFIP == 6]), ("Texas counties", m[m.STATEFIP == 48]),
                    ("all other identified counties", m[~m.STATEFIP.isin([6, 48])])):
        th, se = cl_mean(dd, "neighborhood_crime")
        desc.append({"group": lab, "n": len(dd), "counties": int(dd.COUNTY.nunique()),
                     "mean_mex_share": round(float(np.average(dd.mex_share, weights=dd.wt)), 2),
                     "nbhd_crime_pct": round(100 * th, 2), "se_pp": round(100 * se, 2)})
    for lab in ["under 2%", "2-5%", "5-10%", "10-20%", "20% or more"]:
        for race, rs in (("all", m.index == m.index), ("non-Hispanic white", m.race_eth == "non-Hispanic white")):
            dd = m[(m.mex_band == lab) & rs]
            th, se = cl_mean(dd, "neighborhood_crime")
            desc.append({"group": f"county Mexican-origin share {lab}, {race}", "n": len(dd),
                         "counties": int(dd.COUNTY.nunique()),
                         "mean_mex_share": round(float(np.average(dd.mex_share, weights=dd.wt)), 2),
                         "nbhd_crime_pct": round(100 * th, 2), "se_pp": round(100 * se, 2)})
    write_csv(pd.DataFrame(desc), "q2_same_county_descriptive.csv")

    out = pd.DataFrame(rows)
    write_csv(out, "q2_regressions.csv")
    print(f"design A: {len(ua):,} movers, composition missing for {miss:.1%}; design B: {len(m):,} movers, "
          f"county composition missing for {miss_b:.1%} before drop")
    print(out[out.term.isin(["mex10", "hisp10", "ca_origin", "ln_rent", "cold_origin"])][["spec", "outcome", "term", "coef_pp", "se_pp", "t", "n", "clusters", "mean_outcome_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
