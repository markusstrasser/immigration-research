#!/usr/bin/env python3
"""Correct the composition coefficients for ACS sampling error in the regressor.

ACS 5-year tract shares carry large sampling error. Classical measurement error
in the regressor attenuates the coefficient toward zero by the reliability ratio
lambda = [Var(ds~) - Var(e)] / Var(ds~), where ds~ is the change in share after
the fixed effects and controls are partialled out and Var(e) is the sampling
variance implied by the published margins of error. Corrected beta = beta/lambda.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import estim, prep
from prep import QUAL_D, LEV0

CACHE, DERIVED = prep.CACHE if hasattr(prep, "CACHE") else \
    pathlib.Path(__file__).resolve().parent.parent / "_cache", prep.DERIVED
PAIRS = {"hisp": ("B03002_012", "B03002_001"),
         "fb": ("B05002_013", "B05002_001"),
         "mex": ("B03001_004", "B03002_001")}


def se_prop(num_e, num_m, den_e, den_m):
    """Census derived-proportion standard error (ACS handbook formula)."""
    p = num_e / den_e.where(den_e > 0)
    sn, sd = num_m / 1.645, den_m / 1.645
    rad = sn ** 2 - (p ** 2) * (sd ** 2)
    alt = sn ** 2 + (p ** 2) * (sd ** 2)          # handbook fallback when rad < 0
    use = np.where(rad > 0, rad, alt)
    return np.sqrt(use) / den_e.where(den_e > 0)


def load_moe(year):
    frames = []
    for path in sorted((CACHE / "moe" / str(year)).glob("*.json")):
        rows = json.load(open(path))
        frames.append(pd.DataFrame(rows[1:], columns=rows[0]))
    d = pd.concat(frames, ignore_index=True)
    d["geoid"] = (d["state"].str.zfill(2) + d["county"].str.zfill(3)
                  + d["tract"].str.zfill(6))
    for c in d.columns:
        if c[0] == "B":
            d[c] = pd.to_numeric(d[c], errors="coerce")
            d.loc[d[c] < -1e8, c] = np.nan
    out = pd.DataFrame({"geoid": d["geoid"]})
    for g, (num, den) in PAIRS.items():
        out[f"se_{g}"] = se_prop(d[f"{num}E"], d[f"{num}M"],
                                 d[f"{den}E"], d[f"{den}M"])
    return out


def load_zcta_moe(year):
    rows = json.load(open(CACHE / "zcta_moe" / f"{year}.json"))
    d = pd.DataFrame(rows[1:], columns=rows[0])
    zc = [c for c in d.columns if "zip" in c.lower()][0]
    d["zcta"] = d[zc].str.zfill(5)
    for c in d.columns:
        if c[0] == "B":
            d[c] = pd.to_numeric(d[c], errors="coerce")
            d.loc[d[c] < -1e8, c] = np.nan
    d = d.drop_duplicates("zcta")
    out = pd.DataFrame({"zcta": d["zcta"]})
    for g, (num, den) in PAIRS.items():
        out[f"se_{g}"] = se_prop(d[f"{num}E"], d[f"{num}M"], d[f"{den}E"], d[f"{den}M"])
    return out


def zcta_arm():
    """Same correction on the ZCTA panel, where the outcome can be independent."""
    from zillow import CTRL
    moe = {y: load_zcta_moe(y) for y in [2013, 2018, 2023]}
    M = pd.read_csv(DERIVED / "zcta_panel.csv", dtype={"zcta": str, "cbsa": str})
    for lab, t0, t1 in [("A", 2013, 2018), ("B", 2018, 2023)]:
        sel = M["period"] == lab
        for g in PAIRS:
            m0 = moe[t0].rename(columns={f"se_{g}": "_a"})[["zcta", "_a"]]
            m1 = moe[t1].rename(columns={f"se_{g}": "_b"})[["zcta", "_b"]]
            j = M.loc[sel, ["zcta"]].merge(m0, on="zcta", how="left").merge(
                m1, on="zcta", how="left")
            M.loc[sel, f"var_e_{g}"] = (j["_a"] ** 2 + j["_b"] ** 2).to_numpy()
    C = [c + "_z" for c in CTRL]
    rows = []
    for y, wcol, src in [("dlog_zhvi", "own_units_0", "Zillow ZHVI (independent)"),
                         ("dlog_acsvalue", "own_units_0", "ACS value (same survey)"),
                         ("dlog_zori", "rent_units_0", "Zillow ZORI (independent)"),
                         ("dlog_acsrent", "rent_units_0", "ACS rent (same survey)")]:
        for g in PAIRS:
            tv = f"d_{g}_share"
            sub = M[[y, tv, f"var_e_{g}", wcol, "cbsa_period"] + C].dropna()
            n = sub.groupby("cbsa_period")[y].transform("size")
            sub = sub[n >= 10]
            if len(sub) < 200:
                continue
            w = sub[wcol]
            dm = estim.wdemean(sub, [y, tv] + C, sub["cbsa_period"], w)
            rx = estim.wls(dm[tv], dm[C], w, sub["cbsa_period"].str[:5], C)
            xres = dm[tv].to_numpy() - dm[C].to_numpy() @ rx["beta"]
            wv = w.to_numpy(float)
            var_x = np.average(xres ** 2, weights=wv)
            var_e = np.average(sub[f"var_e_{g}"].to_numpy(), weights=wv)
            lam = (var_x - var_e) / var_x
            mn = estim.wls(dm[y], dm[[tv] + C], w, sub["cbsa_period"].str[:5],
                           [tv] + C, k_absorbed=sub["cbsa_period"].nunique())
            b = estim.row(mn, tv)
            rows.append({"outcome": y, "source": src, "treat": g, "n": len(sub),
                         "coef_ols": b["coef"], "se_ols": b["se"],
                         "reliability_lambda": lam,
                         "coef_corrected": b["coef"] / lam if lam > 0 else np.nan,
                         "se_corrected": b["se"] / lam if lam > 0 else np.nan})
    R = pd.DataFrame(rows)
    R.to_csv(DERIVED / "results_attenuation_zcta.csv", index=False, float_format="%.6g")
    print("\n[ZCTA-level, corrected for sampling error in the regressor]")
    print(R.to_string(index=False))


def main():
    moe = {y: load_moe(y) for y in [2013, 2018, 2023]}
    p = prep.load()
    rows = []
    for outcome in ["rent", "value"]:
        d = prep.valid(p, outcome)
        z = prep.standardize(d, QUAL_D + LEV0)
        for c in z.columns:
            d[c + "_z"] = z[c]
        C = [c + "_z" for c in QUAL_D + LEV0]
        # attach the sampling SE at both endpoints of each period
        for lab, t0, t1 in [("A", 2013, 2018), ("B", 2018, 2023)]:
            for g in PAIRS:
                m0 = moe[t0].rename(columns={f"se_{g}": f"_s0_{g}"})[["geoid", f"_s0_{g}"]]
                m1 = moe[t1].rename(columns={f"se_{g}": f"_s1_{g}"})[["geoid", f"_s1_{g}"]]
                sel = d["period"] == lab
                d.loc[sel, f"var_e_{g}"] = (
                    d.loc[sel, ["geoid"]].merge(m0, on="geoid", how="left")
                     .merge(m1, on="geoid", how="left")
                     .eval(f"_s0_{g}**2 + _s1_{g}**2").to_numpy())
        y = f"dlog_{outcome}"
        for g in PAIRS:
            tv = f"d_{g}_share"
            sub = d[[y, tv, f"var_e_{g}", "_w", "cbsa_period"] + C].dropna()
            n = sub.groupby("cbsa_period")[y].transform("size")
            sub = sub[n >= 10]
            dm = estim.wdemean(sub, [y, tv] + C, sub["cbsa_period"], sub["_w"])
            # residualise the regressor on the controls (weighted) to get ds~
            res_x = estim.wls(dm[tv], dm[C], sub["_w"], sub["cbsa_period"].str[:5], C)
            w = sub["_w"].to_numpy(float)
            xres = dm[tv].to_numpy() - dm[C].to_numpy() @ res_x["beta"]
            var_x = np.average(xres ** 2, weights=w)
            var_e = np.average(sub[f"var_e_{g}"].to_numpy(), weights=w)
            lam = (var_x - var_e) / var_x
            main = estim.wls(dm[y], dm[[tv] + C], sub["_w"],
                             sub["cbsa_period"].str[:5], [tv] + C,
                             k_absorbed=sub["cbsa_period"].nunique())
            b = estim.row(main, tv)
            rows.append({"outcome": outcome, "treat": g, "n": len(sub),
                         "coef_ols": b["coef"], "se_ols": b["se"],
                         "var_resid_x": var_x, "var_sampling_err": var_e,
                         "reliability_lambda": lam,
                         "coef_corrected": b["coef"] / lam if lam > 0 else np.nan,
                         "se_corrected": b["se"] / lam if lam > 0 else np.nan})
    R = pd.DataFrame(rows)
    R.to_csv(DERIVED / "results_attenuation.csv", index=False, float_format="%.6g")
    print("[tract-level, ACS outcome only]")
    print(R.to_string(index=False))
    if (CACHE / "zcta_moe" / "2023.json").exists():
        zcta_arm()
    else:
        print("\n[skip] ZCTA margins of error not cached; ZCTA correction not run")


if __name__ == "__main__":
    main()
