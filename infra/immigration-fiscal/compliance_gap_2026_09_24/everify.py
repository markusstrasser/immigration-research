#!/usr/bin/env python3
"""Test C, pre-registration P1: state E-Verify mandates, stacked triple-difference event study.

The design is fixed in RESULT.md ("Pre-registration", P1), written before this script first ran.
One stack per treated state: the state and all control states, event time -4..+5 (the data start in
2005, so the 2008 states have -3..+5), reference -1. Units are state x industry cell x year for the
high-exposure (focus) cells and the low-exposure cells. Each outcome is regressed on event-time x
treated x high-exposure dummies with stack x state x cell, stack x cell x year and stack x state x
year fixed effects, weighted by the cell's ACS unweighted sample count at event time -1, clustered
by state. Reported per outcome and variant: every event-time coefficient, the post average (0..+5)
with its standard error, and the Wald p-value of the pre coefficients (-4..-2) jointly zero.

Outputs: derived/everify_event_study.csv (coefficients), derived/everify_summary.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/everify.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import FOCUS  # noqa: E402

PANEL = HERE / "_cache" / "panel"
DER = HERE / "derived"
FIPS = {"AZ": 4, "MS": 28, "SC": 45, "AL": 1, "GA": 13, "NC": 37, "UT": 49, "TN": 47, "FL": 12, "LA": 22}
MAIN = {"AZ": 2008, "MS": 2008, "SC": 2012, "AL": 2012, "GA": 2012, "NC": 2013}
NOT_CONTROL = set(FIPS.values())
WINDOW = range(-4, 6)
VARIANTS = {
    "main": (MAIN, True),
    "MS 2011, GA 2013": ({**MAIN, "MS": 2011, "GA": 2013}, True),
    "with Utah 2010": ({**MAIN, "UT": 2010}, True),
    "unweighted": (MAIN, False),
}
OUTCOMES = {"U": "uncovered share", "ln_estabs": "ln QCEW establishments", "ln_emp": "ln QCEW employment",
            "ln_wkwage": "ln QCEW average weekly wage", "m_mexnc": "Mexico-born noncitizen share of ACS workers",
            "se_mexnc_per_ws": "Mexico-born noncitizen unincorporated self-employed per ACS worker"}


def load() -> pd.DataFrame:
    p = pd.read_parquet(PANEL / "panel.parquet")
    p = p[(p.focus | p.low_exposure) & p.ok].copy()
    p["ln_estabs"] = np.log(p.estabs)
    p["ln_emp"] = np.log(p.q_emp)
    p["ln_wkwage"] = np.log(p.q_wages / p.q_emp / 52)
    p["high"] = p.focus.astype(int)
    return p


def load_detail() -> pd.DataFrame:
    """QCEW-only outcomes: detail series of the focus industries against the low-exposure cells."""
    con = duckdb.connect()
    q = con.execute(f"SELECT year, st, cell, estabs, emp AS q_emp, wages AS q_wages, suppressed "
                    f"FROM '{PANEL}/qcew_cells.parquet' WHERE st > 0").df()
    q = q[~q.suppressed.astype(bool) & (q.estabs > 0) & (q.q_emp > 0)]
    rest = q[((q.cell == "q7225") & (q.year >= 2012)) | ((q.cell == "q7221_2") & (q.year < 2012))].copy()
    rest["cell"] = "q_restaurants"
    keep = ["q2381", "q2382", "q2383", "q2389", "q561720"]
    low = pd.read_csv(DER / "low_exposure_cells.csv")
    low_cells = list(low.loc[low.low_exposure, "cell"])
    d = pd.concat([q[q.cell.isin(keep + low_cells)], rest], ignore_index=True)
    d["high"] = (~d.cell.isin(low_cells)).astype(int)
    d["ln_estabs"] = np.log(d.estabs)
    d["ln_emp"] = np.log(d.q_emp)
    d["ln_wkwage"] = np.log(d.q_wages / d.q_emp / 52)
    n = pd.read_parquet(PANEL / "panel.parquet", columns=["year", "st", "cell", "n_ws_all"])
    d = d.merge(n, on=["year", "st", "cell"], how="left")
    parent = {"q2381": "c23", "q2382": "c23", "q2383": "c23", "q2389": "c23", "q561720": "c5617z",
              "q_restaurants": "c722z"}
    pn = n.rename(columns={"cell": "parent", "n_ws_all": "n_parent"})
    d["parent"] = d.cell.map(parent).fillna(d.cell)
    d = d.drop(columns="n_ws_all").merge(pn, on=["year", "st", "parent"], how="left").rename(columns={"n_parent": "n_ws_all"})
    return d


def stack(p: pd.DataFrame, treat: dict[str, int], weighted: bool) -> pd.DataFrame:
    parts = []
    controls = sorted(set(p.st) - NOT_CONTROL)
    for s, e in treat.items():
        sid = FIPS[s]
        d = p[p.st.isin(controls + [sid]) & p.year.between(e + min(WINDOW), e + max(WINDOW))].copy()
        d["stack"] = s
        d["et"] = d.year - e
        d["treated"] = (d.st == sid).astype(int)
        base = d[d.et == -1][["st", "cell", "n_ws_all"]].rename(columns={"n_ws_all": "w0"})
        d = d.merge(base, on=["st", "cell"], how="inner")
        parts.append(d)
    d = pd.concat(parts, ignore_index=True)
    d["w"] = d.w0 if weighted else 1.0
    d = d[d.w > 0]
    for k in WINDOW:
        if k == -1:
            continue
        name = f"et_m{-k}" if k < 0 else f"et_p{k}"
        d[name] = ((d.et == k) & (d.treated == 1) & (d.high == 1)).astype(int)
    d["ssc"] = d["stack"] + "_" + d.st.astype(str) + "_" + d.cell
    d["scy"] = d["stack"] + "_" + d.cell + "_" + d.year.astype(str)
    d["ssy"] = d["stack"] + "_" + d.st.astype(str) + "_" + d.year.astype(str)
    return d


def estimate(d: pd.DataFrame, y: str) -> tuple[pd.DataFrame, dict]:
    names = [f"et_m{-k}" if k < 0 else f"et_p{k}" for k in WINDOW if k != -1]
    names = [n for n in names if d[n].sum() > 0]
    dd = d.dropna(subset=[y])
    dd = dd[np.isfinite(dd[y])]
    m = pf.feols(f"{y} ~ {' + '.join(names)} | ssc + scy + ssy", data=dd, weights="w", vcov={"CRV1": "st"})
    tid = m.tidy()
    coefs = tid.reset_index().rename(columns={"Coefficient": "term"})
    post = [n for n in names if n.startswith("et_p")]
    pre = [n for n in names if n.startswith("et_m") and n != "et_m1"]
    b = m.coef()
    V = m._vcov
    idx = {n: i for i, n in enumerate(m._coefnames)}
    wv = np.zeros(len(b))
    for n in post:
        wv[idx[n]] = 1 / len(post)
    post_avg = float(wv @ b.values)
    post_se = float(np.sqrt(wv @ V @ wv))
    if pre:
        ii = [idx[n] for n in pre]
        bp = b.values[ii]
        Vp = V[np.ix_(ii, ii)]
        wald = float(bp @ np.linalg.pinv(Vp) @ bp)
        G = dd.st.nunique()
        f = wald / len(pre)
        p_pre = float(1 - stats.f.cdf(f, len(pre), G - 1))
    else:
        p_pre = float("nan")
    summ = {"post_avg": post_avg, "post_se": post_se, "post_ci_low": post_avg - 1.96 * post_se,
            "post_ci_high": post_avg + 1.96 * post_se, "pre_joint_p": p_pre, "n": int(m._N),
            "clusters": int(dd.st.nunique()), "pre_terms": len(pre), "post_terms": len(post)}
    return coefs, summ


def trend_break(d: pd.DataFrame, y: str) -> dict:
    """EXPLORATORY, not pre-registered (added after the pre-trend tests failed): the same stacked
    triple difference with a linear treated x high trend over the whole window, a level shift at
    event time 0 and a slope change after it."""
    dd = d.dropna(subset=[y])
    dd = dd[np.isfinite(dd[y])].copy()
    th = (dd.treated * dd.high).astype(float)
    dd["th_trend"] = th * dd.et
    dd["th_post"] = th * (dd.et >= 0)
    dd["th_post_trend"] = th * (dd.et >= 0) * dd.et
    m = pf.feols(f"{y} ~ th_trend + th_post + th_post_trend | ssc + scy + ssy", data=dd, weights="w",
                 vcov={"CRV1": "st"})
    t = m.tidy()
    return {"pre_trend": t.loc["th_trend", "Estimate"], "pre_trend_se": t.loc["th_trend", "Std. Error"],
            "level_shift": t.loc["th_post", "Estimate"], "level_shift_se": t.loc["th_post", "Std. Error"],
            "slope_change": t.loc["th_post_trend", "Estimate"], "slope_change_se": t.loc["th_post_trend", "Std. Error"],
            "n": int(m._N)}


def main() -> None:
    p = load()
    detail = load_detail()
    all_coefs, summaries = [], []
    tb = []
    for cells_name, frame in (("focus vs low-exposure cells", p), ("detail series vs low-exposure cells", detail)):
        d = stack(frame, MAIN, True)
        for y in (OUTCOMES if cells_name.startswith("focus") else ["ln_estabs", "ln_emp", "ln_wkwage"]):
            tb.append({"cells": cells_name, "outcome": y, **trend_break(d, y)})
    tbd = pd.DataFrame(tb)
    tbd.to_csv(DER / "everify_trend_break_exploratory.csv", index=False, lineterminator="\n", float_format="%.5f")
    for vname, (treat, weighted) in VARIANTS.items():
        d = stack(p, treat, weighted)
        for y in OUTCOMES:
            coefs, s = estimate(d, y)
            coefs["variant"], coefs["outcome"], coefs["cells"] = vname, y, "focus vs low-exposure cells"
            all_coefs.append(coefs)
            summaries.append({"variant": vname, "outcome": y, "label": OUTCOMES[y],
                              "cells": "focus vs low-exposure cells", **s})
    # QCEW detail series (specialty trades, janitorial, restaurants) against the low-exposure cells
    for vname in ("main", "unweighted"):
        treat, weighted = VARIANTS[vname]
        d = stack(detail, treat, weighted)
        for y in ("ln_estabs", "ln_emp", "ln_wkwage"):
            coefs, s = estimate(d, y)
            coefs["variant"], coefs["outcome"], coefs["cells"] = vname, y, "detail series vs low-exposure cells"
            all_coefs.append(coefs)
            summaries.append({"variant": vname, "outcome": y, "label": OUTCOMES[y],
                              "cells": "detail series vs low-exposure cells", **s})
    pd.concat(all_coefs).to_csv(DER / "everify_event_study.csv", index=False, lineterminator="\n", float_format="%.5f")
    s = pd.DataFrame(summaries)
    s.to_csv(DER / "everify_summary.csv", index=False, lineterminator="\n", float_format="%.5f")
    pd.set_option("display.width", 250)
    print(s[["variant", "cells", "outcome", "post_avg", "post_se", "post_ci_low", "post_ci_high", "pre_joint_p",
             "n", "clusters"]].to_string(index=False, float_format="%.4f"))
    main_c = pd.concat(all_coefs)
    main_c = main_c[(main_c.variant == "main") & (main_c.cells == "focus vs low-exposure cells")]
    print(main_c.pivot_table(index="term", columns="outcome", values="Estimate").round(4).to_string())
    print("EXPLORATORY trend break (not pre-registered):")
    print(tbd.to_string(index=False, float_format="%.4f"))


if __name__ == "__main__":
    main()
