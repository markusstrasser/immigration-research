"""Cadena-Kovak population-response and smoothing regressions on ACS metro cells.

Replicates the design of Cadena & Kovak (2016, AEJ Applied), Tables 2, 4 and 5, for the Great
Recession (2006-2010, the anchor against their published estimates) and applies it unchanged to
the COVID shock (2019-2021; 2019-2022 and 2019-2023 for persistence) and to a boom (2012-2016).

Shock measures (all periods):
- qcew: change in log BLS QCEW payroll employment of the metro (place of work, all ownerships),
  the analogue of the paper's County Business Patterns measure (its Table A-6 "general" shock);
- acs: change in log employment of the metro's residents 18-64 (a residence-based check).
Instruments: Bartik predictions, base-year ACS NAICS-sector shares of the metro's employed
residents (all, or low-educated men for the smoothing tables) times national log sector changes
from QCEW (bartik_qcew, preferred) or ACS (bartik_acs; ACS sector coding shifts across vintages).
Sample as in the paper: >= 100,000 adults 18-64 not in school or group quarters, >= 60 sampled
Mexican-born adults in the base year, non-empty cells both years. Weights are inverse sampling
variances of the dependent variable (sums of squared person weights); SEs are HC1. The control is
the base-year Mexican-born share of adults (the paper uses the 2000 share and policy dummies).

Writes derived/ck_population.csv, derived/ck_smoothing.csv, derived/ck_metro_sample.csv.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from metro_panel import county_cbsa  # noqa: E402  one county->CBSA definition for the lane

FISCAL = HERE.parent
DERIVED = HERE / "derived"
PERIODS = {"GR_2006_2010": (2006, 2010), "COVID_2019_2021": (2019, 2021),
           "COVID_2019_2022": (2019, 2022), "COVID_2019_2023": (2019, 2023),
           "BOOM_2012_2016": (2012, 2016)}
PLACEBO = {"COVID_2019_2021": (2016, 2019), "COVID_2019_2022": (2016, 2019)}
GROUPS = {"all": ["mex_fb", "mex_nb", "oth_nb", "oth_fb"], "natives": ["mex_nb", "oth_nb"],
          "mex_fb": ["mex_fb"], "mex_nb": ["mex_nb"], "oth_nb": ["oth_nb"], "oth_fb": ["oth_fb"],
          "foreign": ["mex_fb", "oth_fb"]}
CELLS = [("men", 1, True), ("women", 2, True), ("men", 1, False), ("women", 2, False)]


# ---------------------------------------------------------------- estimation helpers
def _hc1(Xh, e, w, bread):
    n, k = Xh.shape
    s = Xh * (w * e)[:, None]
    return bread @ (s.T @ s) @ bread * n / (n - k)


def wls(y, X, w):
    W = w / w.mean()
    bread = np.linalg.inv(X.T @ (X * W[:, None]))
    b = bread @ (X.T @ (W * y))
    return b, np.sqrt(np.diag(_hc1(X, y - X @ b, W, bread)))


def iv(y, exog, endog, excl, w):
    """Weighted 2SLS with HC1 SEs; coefficients ordered [endog..., exog...]; robust first-stage F."""
    W = w / w.mean()
    Z = np.column_stack([excl, exog])
    X = np.column_stack([endog, exog])
    Pi = np.linalg.inv(Z.T @ (Z * W[:, None])) @ (Z.T @ (X * W[:, None]))
    Xh = Z @ Pi
    bread = np.linalg.inv(Xh.T @ (X * W[:, None]))
    b = bread @ (Xh.T @ (W * y))
    V = _hc1(Xh, y - X @ b, W, bread)
    nx, fs = excl.shape[1], []
    for j in range(endog.shape[1]):
        bj, sej = wls(endog[:, j], Z, w)
        fs.append(float(np.mean((bj[:nx] / sej[:nx]) ** 2)))
    return b, np.sqrt(np.diag(V)), fs


# ---------------------------------------------------------------- data
def load():
    c = pd.read_csv(DERIVED / "metro_cells.csv", dtype={"cbsa": str})
    s = pd.read_csv(DERIVED / "metro_sector.csv", dtype={"cbsa": str, "sector": str})
    s = s[s["sector"].notna() & ~s["sector"].isin(["", "MIL"])]
    q = pd.read_csv(DERIVED / "qcew_county_total.csv", dtype={"area_fips": str})
    cb = county_cbsa()[["cofips", "cbsa"]]
    q = q.merge(cb, left_on="area_fips", right_on="cofips", how="inner")
    qm = q.groupby(["cbsa", "year"])["annual_avg_emplvl"].sum().unstack("year")
    ns = pd.read_csv(DERIVED / "qcew_national_sector.csv", dtype={"industry_code": str})
    ns = ns.pivot_table(index="industry_code", columns="year", values="annual_avg_emplvl", aggfunc="sum")
    return c, s, qm, ns


def cellsum(c, year, groups, lowed=None, sex=None):
    m = (c["year"] == year) & c["group"].isin(groups)
    if lowed is not None:
        m &= c["lowed"] == lowed
    if sex is not None:
        m &= c["sex"] == sex
    return c[m].groupby("cbsa")[["pop", "emp", "n", "w2", "w2_emp", "wagebill"]].sum()


def sector_shares(s, t0, cells=None):
    base = s[s["year"] == t0].pivot_table(index="cbsa", columns="sector", values="emp", aggfunc="sum").fillna(0)
    return base.div(base.sum(axis=1), axis=0)


def national_change_acs(s, t0, t1):
    n0 = s[s["year"] == t0].groupby("sector")["emp"].sum()
    n1 = s[s["year"] == t1].groupby("sector")["emp"].sum()
    return np.log(n1 / n0)


def national_change_qcew(ns, t0, t1):
    g = np.log(ns[t1] / ns[t0])
    return g.replace([np.inf, -np.inf], np.nan).dropna()


def lowmen_shares(t0):
    """Base-year sector shares of employed low-educated men, from the person extract."""
    p = pd.read_parquet(HERE / "_cache" / "acs" / f"p{t0}.parquet",
                        columns=["st", "puma", "pwgtp", "lowed", "sex", "employed", "gq", "inschool", "sector"])
    p = p[(~p["gq"]) & (~p["inschool"]) & p["employed"] & p["lowed"] & (p["sex"] == 1)
          & ~p["sector"].isin(["", "MIL"])]
    p["state"] = p["st"].astype(str).str.zfill(2)
    x = pd.read_csv(HERE / "_cache" / "xwalk" / ("xwalk_puma2k.csv" if t0 <= 2011 else
                                                 ("xwalk_puma12.csv" if t0 <= 2021 else "xwalk_puma22.csv")), dtype=str)
    pc = [col for col in x.columns if col.lower().startswith("puma")][0]
    x = x.rename(columns={pc: "puma", "county": "cofips"})
    x["state"], x["puma"], x["cofips"] = x["state"].str.zfill(2), x["puma"].str.zfill(5), x["cofips"].str.zfill(5)
    x["afact"] = pd.to_numeric(x["afact"], errors="coerce")
    cb = county_cbsa()[["cofips", "cbsa"]]
    x = x.merge(cb, on="cofips").groupby(["state", "puma", "cbsa"], as_index=False)["afact"].sum()
    g = p.groupby(["state", "puma", "sector"], as_index=False)["pwgtp"].sum().merge(x, on=["state", "puma"])
    g["emp"] = g["pwgtp"] * g["afact"]
    base = g.pivot_table(index="cbsa", columns="sector", values="emp", aggfunc="sum").fillna(0)
    return base.div(base.sum(axis=1), axis=0)


def metro_sample(c, t0, t1, qm):
    adults0 = cellsum(c, t0, GROUPS["all"])
    mex0 = cellsum(c, t0, ["mex_fb"])
    keep = adults0.index[adults0["pop"] >= 100_000]
    keep = keep[mex0.reindex(keep)["n"].fillna(0) >= 60]
    for _, sx, ed in CELLS:
        for g in ("natives", "mex_fb", "oth_fb"):
            for t in (t0, t1):
                keep = keep[cellsum(c, t, GROUPS[g], ed, sx).reindex(keep)["pop"].fillna(0) > 0]
    ok_q = qm.reindex(keep)[[t0, t1]].notna().all(axis=1) & (qm.reindex(keep)[[t0, t1]] > 0).all(axis=1)
    return keep[ok_q.to_numpy()]


def dlog_pop(c, t0, t1, gl, ed, sx, k):
    f0, f1 = cellsum(c, t0, gl, ed, sx).reindex(k), cellsum(c, t1, gl, ed, sx).reindex(k)
    y = np.log(f1["pop"] / f0["pop"]).to_numpy()
    w = 1 / (f0["w2"] / f0["pop"] ** 2 + f1["w2"] / f1["pop"] ** 2).to_numpy()
    return y, w, f0, f1


def run_period(c, s, qm, ns, name, t0, t1, rows_pop, rows_sm, samples):
    k = metro_sample(c, t0, t1, qm)
    tot0, tot1 = cellsum(c, t0, GROUPS["all"]), cellsum(c, t1, GROUPS["all"])
    shocks = {"qcew": np.log(qm[t1] / qm[t0]).reindex(k).to_numpy(),
              "acs": np.log(tot1["emp"] / tot0["emp"]).reindex(k).to_numpy()}
    sh_all = sector_shares(s, t0).reindex(k).fillna(0)
    sh_low = lowmen_shares(t0).reindex(k).fillna(0)
    g_q = national_change_qcew(ns, t0, t1)
    g_a = national_change_acs(s, t0, t1)
    inst = {"bartik_qcew": (sh_all[g_q.index.intersection(sh_all.columns)] * g_q).sum(axis=1).to_numpy(),
            "bartik_acs": (sh_all * g_a.reindex(sh_all.columns).fillna(0)).sum(axis=1).to_numpy(),
            "bartik_qcew_lowmen": (sh_low[g_q.index.intersection(sh_low.columns)] * g_q).sum(axis=1).to_numpy()}
    mexshare = (cellsum(c, t0, ["mex_fb"])["pop"] / tot0["pop"]).reindex(k).to_numpy()
    low0 = cellsum(c, t0, GROUPS["all"], True)
    eta = (cellsum(c, t0, ["mex_fb"], True)["pop"] / low0["pop"]).reindex(k).to_numpy()
    lm0, lm1 = cellsum(c, t0, GROUPS["all"], True, 1), cellsum(c, t1, GROUPS["all"], True, 1)
    samples.append(pd.DataFrame({"period": name, "cbsa": k, **{f"shock_{a}": v for a, v in shocks.items()},
                                 **inst, "mexshare_adults": mexshare, "mexshare_low": eta,
                                 "adults_base": tot0["pop"].reindex(k).to_numpy(),
                                 "lowmen_emp_change_acs": np.log(lm1["emp"] / lm0["emp"]).reindex(k).to_numpy()}))
    ctrl = np.column_stack([np.ones(len(k)), mexshare])
    for label, sx, ed in CELLS:
        for gname, gl in GROUPS.items():
            y, w, _, _ = dlog_pop(c, t0, t1, gl, ed, sx, k)
            ok = np.isfinite(y) & np.isfinite(w)
            base = dict(period=name, t0=t0, t1=t1, group=gname, sex=label,
                        educ="hs_or_less" if ed else "some_college_plus", n_metros=int(ok.sum()))
            for ctl, X0 in (("mexshare_control", ctrl), ("no_control", ctrl[:, :1])):
                for src, x in shocks.items():
                    b, se = wls(y[ok], np.column_stack([x[ok], X0[ok]]), w[ok])
                    rows_pop.append({**base, "spec": f"OLS_{src}_{ctl}", "coef": b[0], "se": se[0]})
                for iname in ("bartik_qcew", "bartik_acs"):
                    z = inst[iname]
                    b, se = wls(y[ok], np.column_stack([z[ok], X0[ok]]), w[ok])
                    rows_pop.append({**base, "spec": f"RF_{iname}_{ctl}", "coef": b[0], "se": se[0]})
                    b, se, fs = iv(y[ok], X0[ok], shocks["qcew"][ok][:, None], z[ok][:, None], w[ok])
                    rows_pop.append({**base, "spec": f"IV_qcew_by_{iname}_{ctl}", "coef": b[0], "se": se[0],
                                     "first_stage_F": fs[0]})
    if name in PLACEBO:
        p0, p1 = PLACEBO[name]
        for gname in ("natives", "mex_fb", "mex_nb", "oth_fb"):
            y, w, _, _ = dlog_pop(c, p0, p1, GROUPS[gname], True, 1, k)
            ok = np.isfinite(y) & np.isfinite(w)
            for src, x in (("qcew", shocks["qcew"]), ("bartik_qcew", inst["bartik_qcew"])):
                b, se = wls(y[ok], np.column_stack([x[ok], ctrl[ok]]), w[ok])
                rows_pop.append(dict(period=name, t0=p0, t1=p1, group=gname, sex="men", educ="hs_or_less",
                                     n_metros=int(ok.sum()), spec=f"PLACEBO_prechange_on_{src}", coef=b[0], se=se[0]))
    # smoothing (paper's Table 5): change in log E/P on the payroll shock, by Mexican share of low-educated
    hi = eta > np.nanmedian(eta)
    panels = {"a_all_lowed_men": (GROUPS["all"], True, 1), "b_native_lowed_men": (GROUPS["natives"], True, 1),
              "b1_oth_nb_lowed_men": (GROUPS["oth_nb"], True, 1), "b2_mex_nb_lowed_men": (GROUPS["mex_nb"], True, 1),
              "b3_native_lowed_women": (GROUPS["natives"], True, 2), "d_native_highed_men": (GROUPS["natives"], False, 1)}
    for pname, (gl, ed, sx) in panels.items():
        f0, f1 = cellsum(c, t0, gl, ed, sx).reindex(k), cellsum(c, t1, gl, ed, sx).reindex(k)
        y = (np.log(f1["emp"] / f1["pop"]) - np.log(f0["emp"] / f0["pop"])).to_numpy()
        w = 1 / (f0["w2"] / f0["pop"] ** 2 + f1["w2"] / f1["pop"] ** 2).to_numpy()
        x = shocks["qcew"]
        for iname in ("bartik_qcew_lowmen", "bartik_qcew", "ols"):
            ok = np.isfinite(y) & np.isfinite(w) & np.isfinite(x)
            res = {}
            for half, m in (("below_median", ~hi), ("above_median", hi)):
                mm = ok & m
                if iname == "ols":
                    b, se = wls(y[mm], np.column_stack([x[mm], np.ones(mm.sum())]), w[mm]); fs = [np.nan]
                else:
                    b, se, fs = iv(y[mm], np.ones((mm.sum(), 1)), x[mm][:, None], inst[iname][mm][:, None], w[mm])
                res[half] = (b[0], se[0])
                rows_sm.append(dict(period=name, panel=pname, spec=iname, sample=half, coef=b[0], se=se[0],
                                    first_stage_F=fs[0], n_metros=int(mm.sum()),
                                    mean_eta=float(np.nanmean(eta[mm]))))
            rows_sm.append(dict(period=name, panel=pname, spec=iname, sample="difference",
                                coef=res["above_median"][0] - res["below_median"][0],
                                se=float(np.hypot(res["above_median"][1], res["below_median"][1])),
                                n_metros=int(ok.sum())))
            # continuous version: slope(eta) = b0 + b1 (eta - mean eta)
            ec = eta - np.nanmean(eta[ok])
            if iname == "ols":
                b, se = wls(y[ok], np.column_stack([x[ok], (x * ec)[ok], np.ones(ok.sum()), ec[ok]]), w[ok]); fs = [np.nan, np.nan]
            else:
                z = inst[iname]
                b, se, fs = iv(y[ok], np.column_stack([np.ones(ok.sum()), ec[ok]]),
                               np.column_stack([x, x * ec])[ok], np.column_stack([z, z * ec])[ok], w[ok])
            for j, lab in ((0, "slope_at_mean_eta"), (1, "slope_gradient_per_unit_eta")):
                rows_sm.append(dict(period=name, panel=pname, spec=iname, sample=lab, coef=b[j], se=se[j],
                                    first_stage_F=fs[j], n_metros=int(ok.sum()), mean_eta=float(np.nanmean(eta[ok]))))


def main():
    c, s, qm, ns = load()
    rows_pop, rows_sm, samples = [], [], []
    for name, (t0, t1) in PERIODS.items():
        if not ({t0, t1} <= set(c["year"].unique()) and {t0, t1} <= set(qm.columns)):
            print(f"  ! skip {name}: years missing")
            continue
        run_period(c, s, qm, ns, name, t0, t1, rows_pop, rows_sm, samples)
        print(f"  ✓ {name}: {len(samples[-1])} metros")
    pd.DataFrame(rows_pop).to_csv(DERIVED / "ck_population.csv", index=False)
    pd.DataFrame(rows_sm).to_csv(DERIVED / "ck_smoothing.csv", index=False)
    pd.concat(samples).to_csv(DERIVED / "ck_metro_sample.csv", index=False)


if __name__ == "__main__":
    main()
