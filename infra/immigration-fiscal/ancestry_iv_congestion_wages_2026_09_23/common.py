"""Shared pieces: the ancestry lane's estimators and instrument, the reproduction gates, the two
metro samples and the specification menu. Imported by estimate_commute.py and estimate_wages.py.

The instrument is the ancestry lane's, unchanged: its `panel()` builds the displacement lane's
2000-2010 long difference (published-ACS foreign-born share, pre-1990 settlement instrument Z,
2000 population weights, metros of 100k+) and Z2 = 100 x predicted 2000s arrivals / 2000
population from its derived/cbsa_predicted_inflow.csv. Its weighted 2SLS with the HC1 sandwich
(`tsls`) and its WLS (`wls`) are imported from second_instrument.py, not re-implemented.

Samples
  PC  panel-consistent: the ancestry lane's n = 334 CBSAs, dX from its panel (2010 endpoint on
      the 2009 delineation, matched by code; RESULT.md finding F1)
  FG  fixed geography: every 2013 metro of 100k+ in 2000 with an instrument, 2010 endpoint
      summed from counties (ACS 2008-2012) or PUMAs (IPUMS) onto the same 2013 footprint
"""
import importlib.util
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ANC = HERE.parent / "ancestry_instrument_2026_09_22"
DT = HERE.parent / "displacement_transfers_2026_09_18" / "derived"
DERIVED = HERE / "derived"

sys.dont_write_bytecode = True  # importing another lane's script must not write into its directory
_spec = importlib.util.spec_from_file_location("second_instrument", ANC / "second_instrument.py")
si = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(si)
wls, tsls = si.wls, si.tsls
INSTRUMENTS = {"Z2": ["Z2"], "Z2_exmex": ["Z2_exmex"], "Z2_mex": ["Z2_mex"], "Z": ["Z"], "Z+Z2": ["Z", "Z2"]}


def add_instruments(m: pd.DataFrame) -> pd.DataFrame:
    pred = pd.read_csv(ANC / "derived" / "cbsa_predicted_inflow.csv", dtype={"cbsa": str})
    m = m.merge(pred, on="cbsa", how="inner")
    m["Z2"] = 100.0 * m.pred_2000s_all / m["pop"]
    m["Z2_mex"] = 100.0 * m.pred_2000s_mex / m["pop"]
    m["Z2_exmex"] = m.Z2 - m.Z2_mex
    return m


def gates() -> dict:
    """G1/G2: the ancestry lane's Z2 first stage and IV on SSI receipt, to 1e-9, before any new row."""
    ref = pd.read_csv(ANC / "derived" / "second_instrument.csv")
    ref = ref[ref.outcome.eq("ssi_rate")].set_index("estimator")
    m = add_instruments(si.panel("ssi_rate"))
    fs = wls(m.dX, m[["Z2"]], m.w)
    X = np.column_stack([np.ones(len(m)), m.dX])
    b, se, _, _ = tsls(m.dy, X, np.column_stack([np.ones(len(m)), m.Z2]), m.w.to_numpy())
    g = dict(n=len(m), n_ref=int(ref.loc["first-stage on Z2", "n"]),
             fs=float(fs.params["Z2"]), fs_ref=float(ref.loc["first-stage on Z2", "coef"]),
             fs_se=float(fs.bse["Z2"]), fs_se_ref=float(ref.loc["first-stage on Z2", "se"]),
             iv=float(b[1]), iv_ref=float(ref.loc["IV with Z2", "coef"]),
             iv_se=float(se[1]), iv_se_ref=float(ref.loc["IV with Z2", "se"]))
    g["passed"] = (g["n"] == g["n_ref"] and abs(g["fs"] - g["fs_ref"]) < 1e-9
                   and abs(g["fs_se"] - g["fs_se_ref"]) < 1e-9 and abs(g["iv"] - g["iv_ref"]) < 1e-9
                   and abs(g["iv_se"] - g["iv_se_ref"]) < 1e-9)
    if not g["passed"]:
        raise SystemExit(f"[BLOCKED] ancestry-lane reproduction failed: {g}")
    return g


def sample_pc() -> pd.DataFrame:
    """The ancestry lane's 334 metros with its dX, Z, weights and Z2."""
    m = add_instruments(si.panel("ssi_rate"))
    return m[["cbsa", "dX", "Z", "w", "pop", "Z2", "Z2_mex", "Z2_exmex"]].copy()


def sample_fg() -> pd.DataFrame:
    """2013 metros of 100k+ in 2000 with both instruments; 2000 values from the displacement panel."""
    out = pd.read_csv(DT / "metro_panel.csv", dtype={"cbsa": str})
    base = pd.read_csv(DT / "base_shares_pre1990.csv", dtype={"cbsa": str})
    natl = pd.read_csv(DT / "national_stock.csv").set_index("year")
    a = out[out.year == 2000][["cbsa", "cbsa_title", "pop", "fb_share", "mex_share", "ssi_rate", "pa_rate"]]
    m = a.merge(base[["cbsa", "fb_base_share"]], on="cbsa", how="inner")
    m["Z"] = 100.0 * m.fb_base_share * (natl.loc[2010, "fb"] - natl.loc[2000, "fb"]) / m["pop"]
    m["w"] = m["pop"]
    m = m[m.w >= si.MIN_POP]
    return add_instruments(m)


def ar_interval(y, x, z, C, w, crit=3.841458820694124):
    """Anderson-Rubin 95% set for one endogenous regressor and one instrument, HC1, weighted.
    For each b the AR statistic is the HC1 t^2 on z in the regression of y - b*x on [1, z, C];
    its residuals are u_y - b*u_x, so the set solves a quadratic in b. Returns (lo, hi, kind):
    kind 'bounded', 'unbounded-gap' (the real line minus (lo, hi)) or 'unbounded' (every b)."""
    n = len(y)
    sw = np.sqrt(w)
    Z = np.column_stack([np.ones(n), z, C]) * sw[:, None]
    A = np.linalg.inv(Z.T @ Z)
    ys, xs = np.asarray(y) * sw, np.asarray(x) * sw
    py, px = A @ (Z.T @ ys), A @ (Z.T @ xs)
    uy, ux = ys - Z @ py, xs - Z @ px
    k = Z.shape[1]
    adj = n / (n - k)

    def V(a, b):
        return (A @ ((Z * (a * b)[:, None]).T @ Z) @ A)[1, 1] * adj

    Vyy, Vxx, Vyx = V(uy, uy), V(ux, ux), V(uy, ux)
    qa = px[1] ** 2 - crit * Vxx
    qb = -2.0 * (py[1] * px[1] - crit * Vyx)
    qc = py[1] ** 2 - crit * Vyy
    disc = qb ** 2 - 4 * qa * qc
    if qa > 0:
        r = np.sqrt(max(disc, 0.0))
        return (-qb - r) / (2 * qa), (-qb + r) / (2 * qa), "bounded"
    if disc > 0:
        r = np.sqrt(disc)
        lo, hi = sorted([(-qb - r) / (2 * qa), (-qb + r) / (2 * qa)])
        return lo, hi, "unbounded-gap"
    return -np.inf, np.inf, "unbounded"


def _row(rows, base, estimator, coef=np.nan, se=np.nan, F=np.nan, J=np.nan, p=np.nan, n=None,
         ar=(np.nan, np.nan, "")):
    rows.append({**base, "estimator": estimator, "n": n, "coef": coef, "se": se,
                 "lo": coef - 1.96 * se if np.isfinite(se) else np.nan,
                 "hi": coef + 1.96 * se if np.isfinite(se) else np.nan,
                 "F": F, "hansen_J": J, "hansen_p": p,
                 "ar_lo": ar[0], "ar_hi": ar[1], "ar_kind": ar[2]})


def menu(rows: list, m: pd.DataFrame, y: str, x: str, base: dict, y0: str | None = None,
         controls: list | None = None, instruments: dict | None = None, placebo_extra: list | None = None):
    """First stages, OLS, reduced forms, 2SLS for each instrument, the lane's baseline-level arm,
    optional exogenous controls, and the level placebo. Population weights, HC1 throughout."""
    need = [y, x, "w"] + (controls or []) + ([y0] if y0 else [])
    instruments = instruments or INSTRUMENTS
    zcols = sorted({c for v in instruments.values() for c in v})
    d = m.dropna(subset=need + zcols).copy()
    n, w = len(d), d.w.to_numpy()
    if n < 25:
        return
    base = {**base, "y": y, "x": x, "controls": "+".join(controls or []) or "none"}
    C = d[controls].to_numpy() if controls else np.empty((n, 0))
    for name, zc in instruments.items():
        r = wls(d[x], d[zc + (controls or [])], w)
        if len(zc) == 1:
            F = float((r.params[zc[0]] / r.bse[zc[0]]) ** 2)
            _row(rows, base, f"first stage on {name}", r.params[zc[0]], r.bse[zc[0]], F, n=n)
        else:
            k = len(zc)
            R = np.zeros((k, 1 + k + C.shape[1]))
            for i in range(k):
                R[i, 1 + i] = 1.0
            F = float(r.f_test(R).fvalue)
            for c in zc:
                _row(rows, base, f"first stage on {name}, coefficient on {c}", r.params[c], r.bse[c], F, n=n)
    r = wls(d[y], d[[x] + (controls or [])], w)
    _row(rows, base, "OLS", r.params[x], r.bse[x], n=n)
    for name in ("Z2", "Z2_exmex"):
        if name in instruments:
            r = wls(d[y], d[instruments[name] + (controls or [])], w)
            _row(rows, base, f"reduced form on {name}", r.params[name], r.bse[name], n=n)
    X = np.column_stack([np.ones(n), d[x], C])
    for name, zc in instruments.items():
        Z = np.column_stack([np.ones(n), d[zc].to_numpy(), C])
        b, se, J, p = tsls(d[y], X, Z, w)
        ar = (ar_interval(d[y].to_numpy(), d[x].to_numpy(), d[zc[0]].to_numpy(), C, w)
              if len(zc) == 1 else (np.nan, np.nan, ""))
        _row(rows, base, f"IV with {name}", b[1], se[1], J=J, p=p, n=n, ar=ar)
        if y0:
            Xc = np.column_stack([X, d[y0]])
            Zc = np.column_stack([Z, d[y0]])
            b, se, J, p = tsls(d[y], Xc, Zc, w)
            _row(rows, base, f"IV with {name} + baseline level", b[1], se[1], J=J, p=p, n=n)
    if y0:
        for name in ("Z2", "Z2_exmex", "Z"):
            if name in instruments:
                r = wls(d[y0], d[instruments[name]], w)
                _row(rows, base, f"level placebo: {name} on 2000 level", r.params[name], r.bse[name], n=n)
        for extra in placebo_extra or []:
            r = wls(d[y0], d[["Z2", extra]], w)
            _row(rows, base, f"level placebo: Z2 on 2000 level given {extra}", r.params["Z2"], r.bse["Z2"], n=n)
