"""A second instrument for the 2000-2010 foreign-born inflow: the public ancestry
push-pull prediction (Burchardi, Chaney and Hassan 2019, county x origin file from
immigrationshock.com) aggregated to the displacement lane's fixed 2013 CBSAs, run beside
that lane's pre-1990 settlement shift-share on the same metro panel and outcomes.

Reads
  displacement_transfers_2026_09_18/derived/{metro_panel,base_shares_pre1990,national_stock}.csv
  hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv
  sources/.../immigrationshock/ancestry-instruments/AncestryInstrument_County.dta
Writes
  derived/cbsa_predicted_inflow.csv   predicted 2000-2010 arrivals per CBSA, all origins and Mexico
  derived/second_instrument.csv       every estimate
  derived/summary.json                gates and headline numbers

Gate G1: the settlement-instrument first stage for 2000-2010, all foreign-born, must
reproduce the displacement lane's estimates.csv row (coefficient, SE, n) before any
second-instrument row is written.

Run from the repository root (statsmodels and scipy are not in the main venv):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
    python3 infra/immigration-fiscal/ancestry_instrument_2026_09_22/second_instrument.py
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DT = HERE.parent / "displacement_transfers_2026_09_18" / "derived"
XW = HERE.parent / "hedonic_composition_2026_09_19" / "derived" / "geo_county_cbsa_2013.csv"
DTA = (ROOT / "sources/immigration-fiscal/data/external/stage3/immigrationshock/"
       "ancestry-instruments/AncestryInstrument_County.dta")
DERIVED = HERE / "derived"
T0, T1 = 2000, 2010
MIN_POP = 100_000
OUTCOMES = [("ssi_rate", "household SSI receipt"),
            ("pa_rate", "household public assistance receipt"),
            ("nc_epop", "E/POP 25-64 below BA"),
            ("nc_lfp", "LFP 25-64 below BA"),
            ("col_epop", "E/POP 25-64 BA+ (control)")]


# ---------------------------------------------------------------- estimators
def wls(y, X, w):
    return sm.WLS(y, sm.add_constant(X), weights=w).fit(cov_type="HC1")


def tsls(y, X, Z, w, hc1=True):
    """2SLS with weights and a heteroskedasticity-robust sandwich; X and Z include a
    constant. Returns coefficients, robust SEs and Hansen's J for over-identification."""
    sw = np.sqrt(w)[:, None]
    y_, X_, Z_ = np.asarray(y)[:, None] * sw, np.asarray(X) * sw, np.asarray(Z) * sw
    n, k = X_.shape
    ZtZ_inv = np.linalg.inv(Z_.T @ Z_)
    Xhat = Z_ @ (ZtZ_inv @ (Z_.T @ X_))
    A = np.linalg.inv(Xhat.T @ X_)
    beta = A @ (Xhat.T @ y_)
    u = y_ - X_ @ beta
    meat = (Xhat * u ** 2).T @ Xhat
    V = A @ meat @ A.T * (n / (n - k) if hc1 else 1.0)
    se = np.sqrt(np.diag(V))
    L = Z_.shape[1]
    J, p = np.nan, np.nan
    if L > k:
        g = Z_.T @ u
        S = (Z_ * u ** 2).T @ Z_
        J = float((g.T @ np.linalg.inv(S) @ g)[0, 0])
        p = float(1 - stats.chi2.cdf(J, L - k))
    return beta[:, 0], se, J, p


# ---------------------------------------------------------------- data
def predicted_inflow():
    """Per-CBSA predicted 2000-2010 arrivals (persons) from the county x origin file."""
    d = pd.read_stata(DTA, convert_categoricals=False)
    d["county_fips"] = (d.CountyCode / 10).round().astype(int).astype(str).str.zfill(5)
    # the file's county codes are 1990 FIPS x 10 (10010 = 01001 Autauga, AL)
    assert d.loc[d.CountyName.eq("Autauga"), "county_fips"].iloc[0] == "01001"
    d["is_mex"] = d.CountryName.astype(str).str.strip().str.lower().eq("mexico")
    assert d.is_mex.sum() == d.county_fips.nunique(), "one Mexico row per county expected"
    xw = pd.read_csv(XW, dtype={"county_fips": str, "cbsa": str})
    m = d.merge(xw[["county_fips", "cbsa"]], on="county_fips", how="inner")
    unmatched = d.county_fips.nunique() - m.county_fips.nunique()
    g = m.groupby("cbsa")
    out = pd.DataFrame({
        "pred_2000s_all": g.PushPull_10.sum() * 1000.0,
        "pred_2000s_mex": m[m.is_mex].groupby("cbsa").PushPull_10.sum() * 1000.0,
        "pred_1990s_all": g.PushPull_9.sum() * 1000.0,
        "ancestry_2010_all": g.Ancestry.sum() * 1000.0,
        "counties": g.county_fips.nunique(),
    }).reset_index()
    out["pred_2000s_mex"] = out.pred_2000s_mex.fillna(0.0)
    meta = dict(counties_in_file=int(d.county_fips.nunique()), origins=int(d.CountryCode.nunique()),
                counties_unmatched_to_cbsa=int(unmatched),
                national_pred_2000s_all=float(d.PushPull_10.sum() * 1000),
                national_pred_2000s_mex=float(d.loc[d.is_mex, "PushPull_10"].sum() * 1000),
                national_pred_1990s_all=float(d.PushPull_9.sum() * 1000))
    return out, meta


def panel(outcome):
    """The displacement lane's 2000-2010 long difference, rebuilt from its derived files
    exactly as its estimate.py builds it for a 2000-based window (published-ACS treatment,
    pre-1990 base shares, population weights, metros of 100k+)."""
    out = pd.read_csv(DT / "metro_panel.csv", dtype={"cbsa": str})
    base = pd.read_csv(DT / "base_shares_pre1990.csv", dtype={"cbsa": str})
    natl = pd.read_csv(DT / "national_stock.csv").set_index("year")
    a = out[out.year == T0][["cbsa", outcome, "pop", "fb_share"]]
    b = out[out.year == T1][["cbsa", outcome, "fb_share"]]
    m = a.merge(b, on="cbsa", suffixes=("_0", "_1"))
    m = m.merge(base[["cbsa", "fb_base_share"]], on="cbsa", how="inner")
    m["dy"] = m[f"{outcome}_1"] - m[f"{outcome}_0"]
    m["dX"] = m["fb_share_1"] - m["fb_share_0"]
    m["y0"] = m[f"{outcome}_0"]
    shift = natl.loc[T1, "fb"] - natl.loc[T0, "fb"]
    m["Z"] = 100.0 * m["fb_base_share"] * shift / m["pop"]
    m["w"] = m["pop"]
    m = m[m["w"] >= MIN_POP]
    return m[["cbsa", "dy", "dX", "Z", "w", "y0", "pop"]].replace([np.inf, -np.inf], np.nan).dropna()


# ---------------------------------------------------------------- main
def main():
    DERIVED.mkdir(exist_ok=True)
    pred, meta = predicted_inflow()
    pred.to_csv(DERIVED / "cbsa_predicted_inflow.csv", index=False)

    # G1: reproduce the lane's settlement first stage before adding anything
    ref = pd.read_csv(DT / "estimates.csv")
    ref = ref[(ref.window == "2000-2010") & (ref.design == "1") & (ref.treat == "all foreign-born")
              & (ref.outcome == "ssi_rate") & (ref.estimator == "first-stage")].iloc[0]
    m = panel("ssi_rate")
    fs = wls(m["dX"], m[["Z"]], m["w"])
    g1 = dict(n=int(len(m)), n_ref=int(ref.n), coef=float(fs.params["Z"]), coef_ref=float(ref.coef),
              se=float(fs.bse["Z"]), se_ref=float(ref.se))
    g1["passed"] = (g1["n"] == g1["n_ref"] and abs(g1["coef"] - g1["coef_ref"]) < 1e-9
                    and abs(g1["se"] - g1["se_ref"]) < 1e-9)
    if not g1["passed"]:
        raise SystemExit(f"[BLOCKED] G1 settlement first stage not reproduced: {g1}")
    print("G1 passed: settlement first stage reproduced", g1)

    rows = []
    for outcome, label in OUTCOMES:
        m = panel(outcome).merge(pred, on="cbsa", how="inner")
        m["Z2"] = 100.0 * m.pred_2000s_all / m["pop"]
        m["Z2_mex"] = 100.0 * m.pred_2000s_mex / m["pop"]
        m["Z2_exmex"] = m.Z2 - m.Z2_mex
        m["Z2_1990s"] = 100.0 * m.pred_1990s_all / m["pop"]
        n = len(m)
        if n < 25:
            continue
        w = m["w"].to_numpy()
        base = dict(outcome=outcome, label=label, n=n)

        def add(**kw):
            rows.append({**base, **kw})

        # correlation between the two instruments (population-weighted)
        ws = w / w.sum()
        cov = np.cov(np.vstack([m.Z, m.Z2]), aweights=ws)
        corr = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
        # Rotemberg-style: share of Z2's weighted variance carried by the Mexico component
        cov_m = np.cov(np.vstack([m.Z2, m.Z2_mex]), aweights=ws)
        mex_share = cov_m[0, 1] / cov_m[0, 0]
        add(estimator="corr(Z, Z2) weighted", coef=corr, se=np.nan, lo=np.nan, hi=np.nan, F=np.nan)
        add(estimator="Mexico share of var(Z2)", coef=mex_share, se=np.nan, lo=np.nan, hi=np.nan, F=np.nan)

        for zname in ("Z", "Z2", "Z2_exmex", "Z2_mex", "Z2_1990s"):
            r = wls(m["dX"], m[[zname]], w)
            ci = r.conf_int().loc[zname]
            add(estimator=f"first-stage on {zname}", coef=r.params[zname], se=r.bse[zname],
                lo=ci[0], hi=ci[1], F=(r.params[zname] / r.bse[zname]) ** 2)
        r = wls(m["dX"], m[["Z", "Z2"]], w)
        F_joint = float(r.f_test(np.eye(3)[1:]).fvalue)
        for zname in ("Z", "Z2"):
            ci = r.conf_int().loc[zname]
            add(estimator=f"first-stage on both, coefficient on {zname}", coef=r.params[zname],
                se=r.bse[zname], lo=ci[0], hi=ci[1], F=F_joint)
        # partial F of Z2 given Z: t^2 in the joint regression
        add(estimator="partial F of Z2 given Z", coef=np.nan, se=np.nan, lo=np.nan, hi=np.nan,
            F=(r.params["Z2"] / r.bse["Z2"]) ** 2)
        # exogeneity check the lane uses: the instrument against the baseline level
        for zname in ("Z", "Z2"):
            r = wls(m["y0"], m[[zname]], w)
            ci = r.conf_int().loc[zname]
            add(estimator=f"{zname} on baseline level (exogeneity test)", coef=r.params[zname],
                se=r.bse[zname], lo=ci[0], hi=ci[1], F=np.nan)
        # OLS, then IV with each instrument and with both
        r = wls(m["dy"], m[["dX"]], w)
        ci = r.conf_int().loc["dX"]
        add(estimator="OLS", coef=r.params["dX"], se=r.bse["dX"], lo=ci[0], hi=ci[1], F=np.nan)
        X = np.column_stack([np.ones(n), m.dX])
        for zname, zcols in (("Z", ["Z"]), ("Z2", ["Z2"]), ("Z2_exmex", ["Z2_exmex"]),
                             ("Z+Z2", ["Z", "Z2"])):
            Zm = np.column_stack([np.ones(n), m[zcols].to_numpy()])
            b, se, J, p = tsls(m["dy"], X, Zm, w)
            Fz = float(rows[[i for i, x in enumerate(rows) if x["outcome"] == outcome
                             and x["estimator"] == (f"first-stage on {zname}" if zname != "Z+Z2"
                                                    else "first-stage on both, coefficient on Z")][0]]["F"])
            add(estimator=f"IV with {zname}", coef=b[1], se=se[1], lo=b[1] - 1.96 * se[1],
                hi=b[1] + 1.96 * se[1], F=Fz, hansen_J=J, hansen_p=p)
            # the lane's mean-reversion arm: the t0 level of the outcome as an exogenous control
            Xc = np.column_stack([np.ones(n), m.dX, m.y0])
            Zc = np.column_stack([np.ones(n), m[zcols].to_numpy(), m.y0])
            bc, sec, Jc, pc = tsls(m["dy"], Xc, Zc, w)
            add(estimator=f"IV with {zname} + baseline level", coef=bc[1], se=sec[1],
                lo=bc[1] - 1.96 * sec[1], hi=bc[1] + 1.96 * sec[1], F=np.nan, hansen_J=Jc, hansen_p=pc)
            if zname == "Z":
                # G2: the hand-written 2SLS must match the lane's IV coefficient
                ref_iv = pd.read_csv(DT / "estimates.csv")
                ref_iv = ref_iv[(ref_iv.window == "2000-2010") & (ref_iv.design == "1")
                                & (ref_iv.treat == "all foreign-born") & (ref_iv.outcome == outcome)
                                & (ref_iv.estimator == "IV")]
                if len(ref_iv):
                    dev = abs(float(ref_iv.iloc[0].coef) - b[1])
                    if dev > 1e-8:
                        raise SystemExit(f"[BLOCKED] G2 IV coefficient differs from lane: {dev}")
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "second_instrument.csv", index=False)
    key = est[est.outcome.eq("ssi_rate")]
    with pd.option_context("display.width", 200, "display.max_rows", 100):
        print(key[["estimator", "n", "coef", "se", "lo", "hi", "F", "hansen_p"]].to_string(index=False))
        print(est[est.estimator.str.startswith("IV")][["outcome", "estimator", "n", "coef", "se", "F", "hansen_p"]]
              .to_string(index=False))
    summary = dict(gates=dict(G1_settlement_first_stage=g1, G2_iv_reproduced=True),
                   file=meta, window=f"{T0}-{T1}", treatment="all foreign-born share, published ACS (as the lane's 2000-based windows)",
                   rows=int(len(est)))
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
