#!/usr/bin/env python3
"""Test C, pre-registration P2: do covered (compliant) establishments lose ground where uncovered
work grows? Associations only; see RESULT.md for the design limits.

Unit: state x industry cell x year, 2012-2023 (panel.parquet from uncovered.py). Outcomes from QCEW:
ln establishments, ln employment, ln average weekly wage (wages / employment / 52). Regressors:
the uncovered share U (contains QCEW employment, so U against employment is mechanical and shown
only for completeness) and the ACS-only Mexico-born noncitizen share m and imputed unauthorized
share. Every regression has state x year and cell x year fixed effects, is weighted by the ACS
unweighted sample count, and clusters by state.

Specifications (all written to derived/panel_c.csv):
  first differences, contemporaneous and one-year-lagged regressor;
  samples: focus cells, low-exposure placebo cells, all cells, all cells with a focus interaction;
  long differences 2012-13 to 2022-23 (state x cell averages), state and cell fixed effects;
  focus detail outcomes (specialty trades 2381-2389, janitorial 561720, restaurants 7225) on the
  parent cell's regressor, with year fixed effects only, and the same outcomes net of the state's
  low-exposure cells that year (added after the year-FE results).

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/panel_c.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import pyfixest as pf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import FOCUS  # noqa: E402

PANEL = HERE / "_cache" / "panel"
DER = HERE / "derived"
YEARS = (2012, 2023)
ROWS: list[dict] = []


def record(model, x: str, **meta) -> None:
    t = model.tidy().loc[x]
    ROWS.append({**meta, "x": x, "coef": t["Estimate"], "se": t["Std. Error"], "ci_low": t["2.5%"],
                 "ci_high": t["97.5%"], "p": t["Pr(>|t|)"], "n": int(model._N)})


def prepare() -> pd.DataFrame:
    p = pd.read_parquet(PANEL / "panel.parquet")
    p = p[p.year.between(YEARS[0] - 1, YEARS[1])].copy()
    p["ln_estabs"] = np.log(p.estabs.where(p.estabs > 0))
    p["ln_emp"] = np.log(p.q_emp.where(p.q_emp > 0))
    p["ln_wkwage"] = np.log((p.q_wages / p.q_emp / 52).where(p.q_emp > 0))
    p = p.sort_values(["st", "cell", "year"])
    g = p.groupby(["st", "cell"])
    for v in ("ln_estabs", "ln_emp", "ln_wkwage", "U", "m_mexnc", "m_unauth"):
        p[f"d_{v}"] = g[v].diff()
        # a difference needs consecutive years and usable cells at both ends
        ok = (g.year.diff() == 1) & p.ok & g.ok.shift(1).fillna(False).astype(bool)
        p.loc[~ok, f"d_{v}"] = np.nan
    for v in ("d_U", "d_m_mexnc", "d_m_unauth"):
        p[f"{v}_lag"] = g[v].shift(1)
    return p[p.year.between(*YEARS)]


def first_differences(p: pd.DataFrame) -> None:
    samples = {"focus cells": p[p.focus], "low-exposure placebo cells": p[p.low_exposure], "all cells": p}
    for sname, d in samples.items():
        for y in ("d_ln_estabs", "d_ln_emp", "d_ln_wkwage"):
            for x in ("d_U", "d_U_lag", "d_m_mexnc", "d_m_mexnc_lag", "d_m_unauth", "d_m_unauth_lag"):
                dd = d.dropna(subset=[y, x, "n_ws_all"])
                if len(dd) < 50:
                    continue
                m = pf.feols(f"{y} ~ {x} | st_year + cell_year", data=dd, weights="n_ws_all",
                             vcov={"CRV1": "st"})
                note = "mechanical: U contains QCEW employment" if (y == "d_ln_emp" and x == "d_U") else ""
                record(m, x, design="first differences", sample=sname, y=y, note=note)
    # all cells, focus interaction: does the association differ in the focus cells?
    p = p.assign(focus_i=p.focus.astype(int))
    for y in ("d_ln_estabs", "d_ln_emp", "d_ln_wkwage"):
        for x in ("d_U_lag", "d_m_mexnc_lag", "d_m_unauth_lag"):
            dd = p.dropna(subset=[y, x]).copy()
            dd["x_focus"] = dd[x] * dd.focus_i
            m = pf.feols(f"{y} ~ {x} + x_focus | st_year + cell_year", data=dd, weights="n_ws_all",
                         vcov={"CRV1": "st"})
            record(m, "x_focus", design="first differences, focus interaction", sample="all cells", y=y,
                   note=f"difference focus minus other cells, regressor {x}")


def long_differences(p: pd.DataFrame) -> None:
    ends = {"start": (2012, 2013), "end": (2022, 2023)}
    parts = []
    for name, yrs in ends.items():
        d = p[p.year.isin(yrs) & p.ok].groupby(["st", "cell"]).agg(
            estabs=("estabs", "mean"), q_emp=("q_emp", "mean"), q_wages=("q_wages", "mean"),
            U=("U", "mean"), m_mexnc=("m_mexnc", "mean"), m_unauth=("m_unauth", "mean"),
            n=("n_ws_all", "sum"), years=("year", "nunique"))
        d = d[d.years == 2]
        parts.append(d.add_suffix(f"_{name}"))
    ld = parts[0].join(parts[1], how="inner").reset_index()
    ld["dy_estabs"] = np.log(ld.estabs_end / ld.estabs_start)
    ld["dy_emp"] = np.log(ld.q_emp_end / ld.q_emp_start)
    ld["dy_wkwage"] = np.log((ld.q_wages_end / ld.q_emp_end) / (ld.q_wages_start / ld.q_emp_start))
    ld["dU"] = ld.U_end - ld.U_start
    ld["dm_mexnc"] = ld.m_mexnc_end - ld.m_mexnc_start
    ld["dm_unauth"] = ld.m_unauth_end - ld.m_unauth_start
    ld["w"] = ld.n_start
    ld["focus"] = ld.cell.isin(FOCUS)
    low = set(p.loc[p.low_exposure, "cell"])
    for sname, d in {"focus cells": ld[ld.focus], "low-exposure placebo cells": ld[ld.cell.isin(low)],
                     "all cells": ld}.items():
        for y in ("dy_estabs", "dy_emp", "dy_wkwage"):
            for x in ("dU", "dm_mexnc", "dm_unauth"):
                dd = d.replace([np.inf, -np.inf], np.nan).dropna(subset=[y, x])
                m = pf.feols(f"{y} ~ {x} | st + cell", data=dd, weights="w", vcov={"CRV1": "st"})
                note = "mechanical: U contains QCEW employment" if (y == "dy_emp" and x == "dU") else ""
                record(m, x, design="long difference 2012-13 to 2022-23", sample=sname, y=y, note=note)


def detail_outcomes(p: pd.DataFrame) -> None:
    con = duckdb.connect()
    q = con.execute(f"""SELECT year, st, cell AS series, estabs, emp, wages, suppressed
        FROM '{PANEL}/qcew_cells.parquet' WHERE cell LIKE 'q%' AND st > 0""").df()
    # restaurants: 7225 from NAICS 2012 on (the window starts in 2012)
    parent = {"q238": "c23", "q2381": "c23", "q2382": "c23", "q2383": "c23", "q2389": "c23",
              "q561720": "c5617z", "q7225": "c722z"}
    q = q[q.series.isin(parent) & ~q.suppressed.astype(bool) & (q.estabs > 0) & (q.emp > 0)]
    q["parent"] = q.series.map(parent)
    q = q.sort_values(["st", "series", "year"])
    g = q.groupby(["st", "series"])
    for v, col in (("ln_estabs", "estabs"), ("ln_emp", "emp")):
        q[v] = np.log(q[col])
        q[f"d_{v}"] = g[v].diff().where(g.year.diff() == 1)
    q["ln_wkwage"] = np.log(q.wages / q.emp / 52)
    q["d_ln_wkwage"] = g["ln_wkwage"].diff().where(g.year.diff() == 1)
    reg = p[["st", "year", "cell", "d_U_lag", "d_m_mexnc_lag", "d_m_unauth_lag", "n_ws_all"]].rename(columns={"cell": "parent"})
    d = q.merge(reg, on=["st", "year", "parent"], how="inner")
    d["st_year"] = d.st.astype(str) + "_" + d.year.astype(str)
    # the same series net of the state's low-exposure cells that year (weighted mean change), which
    # removes the state-year shocks the year-FE version cannot (added after the year-FE results)
    low = p[p.low_exposure]
    for v in ("d_ln_estabs", "d_ln_emp", "d_ln_wkwage"):
        t = low.dropna(subset=[v, "n_ws_all"]).assign(wv=lambda f: f[v] * f.n_ws_all)
        g = t.groupby(["st", "year"])[["wv", "n_ws_all"]].sum()
        d = d.merge((g.wv / g.n_ws_all).rename(f"{v}_low").reset_index(), on=["st", "year"], how="left")
        d[f"{v}_rel"] = d[v] - d[f"{v}_low"]
    for s in parent:
        ds = d[d.series == s]
        for y in ("d_ln_estabs", "d_ln_emp", "d_ln_wkwage"):
            for x in ("d_U_lag", "d_m_mexnc_lag"):
                dd = ds.dropna(subset=[y, x, "n_ws_all"])
                if dd.st.nunique() < 20:
                    continue
                m = pf.feols(f"{y} ~ {x} | year", data=dd, weights="n_ws_all", vcov={"CRV1": "st"})
                record(m, x, design="first differences, detail series (year FE only)", sample=s, y=y, note="")
                yr = f"{y}_rel"
                dd = ds.dropna(subset=[yr, x, "n_ws_all"])
                m = pf.feols(f"{yr} ~ {x} | year", data=dd, weights="n_ws_all", vcov={"CRV1": "st"})
                record(m, x, design="first differences, detail series net of the state's low-exposure cells",
                       sample=s, y=y, note="outcome minus the weighted mean change of the state's low-exposure "
                                           "cells that year; added after the year-FE results")


def main() -> None:
    p = prepare()
    first_differences(p)
    long_differences(p)
    detail_outcomes(p)
    out = pd.DataFrame(ROWS)
    out.to_csv(DER / "panel_c.csv", index=False, lineterminator="\n", float_format="%.5f")
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 400)
    print(out[["design", "sample", "y", "x", "coef", "se", "p", "n", "note"]].to_string(index=False, float_format="%.4f"))


if __name__ == "__main__":
    main()
