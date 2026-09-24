#!/usr/bin/env python3
"""Test B: work outside UI coverage by state x industry x year, ACS workers against QCEW jobs.

Uncovered share U = 1 - QCEW private employment / ACS private wage and salary workers (state of
work), 2005-2024; the brief's window is 2012-2023. Known definitional gaps: QCEW counts jobs at the
workplace, the ACS counts people (main job) at their workplace state; multiple job holding
(153.1m covered jobs against 147.3m workers in 2023, BLS), incorporated self-employed, reference
periods, and industry coding (temp-help and PEO workers sit in NAICS 5613 in QCEW). So U is read
three ways:

1. raw, and with incorporated self-employed added to the ACS side;
2. calibrated: relative to the same state-year's low-exposure cells, U_cal = 1 - (QCEW/ACS)_cell /
   (QCEW/ACS)_low, which removes state-year gaps (commuting, coverage, ACS response);
3. as a slope: within cell-year and state-year, how U moves with the share of the cell's ACS
   workers who are Mexico-born noncitizens (or imputed unauthorized). The slope is the extra
   uncovered rate of those workers relative to their coworkers, if the definitional gap does not
   move with that share. The split-sample version takes U from one half of the ACS households and
   the share from the other, so sampling error in the shared ACS count cannot create the slope.

Outputs: derived/uncovered_national_by_cell_year.csv, derived/uncovered_summary_by_cell.csv,
derived/uncovered_slopes.csv, derived/low_exposure_cells.csv; _cache/panel/panel.parquet.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/uncovered.py
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
from cells import CELLS, FOCUS  # noqa: E402

PANEL = HERE / "_cache" / "panel"
DER = HERE / "derived"
MIN_N = 50          # ACS unweighted private wage and salary records per state x cell x year
YEARS_B = (2012, 2023)


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    con = duckdb.connect()
    acs = con.execute(f"SELECT * FROM '{PANEL}/acs_cells.parquet'").df()
    q = con.execute(f"SELECT year, st, cell, estabs, emp AS q_emp, wages AS q_wages, suppressed "
                    f"FROM '{PANEL}/qcew_cells.parquet'").df()
    return acs, q


def low_exposure_cells(acs: pd.DataFrame) -> list[str]:
    a = acs[(acs.half == "all") & acs.year.between(2005, 2007)]
    nat = a.groupby("cell")[["ws", "ws_mexnc"]].sum()
    nat["share"] = nat.ws_mexnc / nat.ws
    other = nat.drop(index=[c for c in FOCUS if c in nat.index]).sort_values("share")
    k = round(len(other) / 3)
    low = list(other.index[:k])
    out = other.assign(low_exposure=other.index.isin(low), label=[CELLS[c]["label"] for c in other.index])
    out.reset_index().to_csv(DER / "low_exposure_cells.csv", index=False, lineterminator="\n",
                             float_format="%.5f")
    return low


def national_table(acs: pd.DataFrame, q: pd.DataFrame, low: list[str]) -> pd.DataFrame:
    a = acs[acs.half == "all"].groupby(["year", "cell"], as_index=False)[
        ["ws", "se_inc", "se_uninc", "ws_mexnc", "ws_unauth", "ws_fbnc", "n_ws", "ws_wagebill"]].sum(min_count=1)
    nat = a.merge(q[q.st == 0][["year", "cell", "q_emp", "estabs", "q_wages"]], on=["year", "cell"])
    nat["U_raw"] = 1 - nat.q_emp / nat.ws
    nat["U_inc"] = 1 - nat.q_emp / (nat.ws + nat.se_inc.fillna(0))
    r0 = (nat[nat.cell.isin(low)].groupby("year")[["q_emp", "ws"]].sum()
          .assign(r0=lambda d: d.q_emp / d.ws)["r0"])
    nat = nat.merge(r0.rename("r0_low"), left_on="year", right_index=True)
    nat["U_cal"] = 1 - (nat.q_emp / nat.ws) / nat.r0_low
    nat["share_mexnc"] = nat.ws_mexnc / nat.ws
    nat["share_unauth"] = nat.ws_unauth / nat.ws
    nat["uncovered_jobs_cal"] = nat.U_cal * nat.ws
    nat["acs_pay_per_worker"] = nat.ws_wagebill / nat.ws
    nat["qcew_pay_per_job"] = nat.q_wages / nat.q_emp
    nat["label"] = nat.cell.map(lambda c: CELLS[c]["label"])
    nat["focus"] = nat.cell.isin(FOCUS)
    nat["low_exposure"] = nat.cell.isin(low)
    nat.sort_values(["cell", "year"]).to_csv(DER / "uncovered_national_by_cell_year.csv", index=False,
                                             lineterminator="\n", float_format="%.6g")
    return nat


def summary(nat: pd.DataFrame) -> pd.DataFrame:
    b = nat[nat.year.between(*YEARS_B)]
    # each year computed on its own, then averaged over years (not pooled)
    g = b.groupby(["cell", "label", "focus", "low_exposure"])
    s = g.agg(acs_ws_m=("ws", lambda x: x.mean() / 1e6), qcew_emp_m=("q_emp", lambda x: x.mean() / 1e6),
              U_raw=("U_raw", "mean"), U_raw_min=("U_raw", "min"), U_raw_max=("U_raw", "max"),
              U_inc=("U_inc", "mean"), U_cal=("U_cal", "mean"), U_cal_min=("U_cal", "min"),
              U_cal_max=("U_cal", "max"), share_mexnc=("share_mexnc", "mean"),
              share_unauth=("share_unauth", "mean"), uncovered_jobs_cal_m=("uncovered_jobs_cal", lambda x: x.mean() / 1e6),
              acs_pay=("acs_pay_per_worker", "mean"), qcew_pay=("qcew_pay_per_job", "mean")).reset_index()
    s = s.sort_values("share_mexnc", ascending=False)
    s.to_csv(DER / "uncovered_summary_by_cell.csv", index=False, lineterminator="\n", float_format="%.5g")
    return s


def build_panel(acs: pd.DataFrame, q: pd.DataFrame, low: list[str]) -> pd.DataFrame:
    wide = acs.pivot_table(index=["year", "st", "cell"], columns="half",
                           values=["ws", "n_ws", "ws_mexnc", "ws_unauth", "ws_unauth_noba", "se_inc",
                                   "se_uninc_mexnc", "ws_fbnc"], aggfunc="sum")
    wide.columns = [f"{v}_{h}" for v, h in wide.columns]
    p = wide.reset_index().merge(q[(q.st > 0) & q.cell.str.startswith("c")], on=["year", "st", "cell"], how="left")
    p["U"] = 1 - p.q_emp / p.ws_all
    p["U_inc"] = 1 - p.q_emp / (p.ws_all + p.se_inc_all.fillna(0))
    for h, o in (("0", "1"), ("1", "0")):
        p[f"U_h{h}"] = 1 - p.q_emp / (2 * p[f"ws_{h}"])
        p[f"m_mexnc_h{o}"] = p[f"ws_mexnc_{o}"].fillna(0) / p[f"ws_{o}"]
        p[f"m_unauth_h{o}"] = p[f"ws_unauth_{o}"] / p[f"ws_{o}"]
    p["m_mexnc"] = p.ws_mexnc_all.fillna(0) / p.ws_all
    p["m_unauth"] = p.ws_unauth_all / p.ws_all
    p["m_unauth_noba"] = p.ws_unauth_noba_all / p.ws_all
    p["m_fbnc"] = p.ws_fbnc_all.fillna(0) / p.ws_all
    p["se_mexnc_per_ws"] = p.se_uninc_mexnc_all.fillna(0) / p.ws_all
    p["focus"] = p.cell.isin(FOCUS)
    p["low_exposure"] = p.cell.isin(low)
    p["ok"] = (p.n_ws_all >= MIN_N) & (p.suppressed == False) & (p.q_emp > 0)  # noqa: E712
    p["st_year"] = p.st.astype(str) + "_" + p.year.astype(str)
    p["cell_year"] = p.cell + "_" + p.year.astype(str)
    p.to_parquet(PANEL / "panel.parquet", index=False)
    return p


def slopes(p: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base = p[p.ok & p.year.between(*YEARS_B)].copy()

    def fit(df, y, x, label, sample, weights="n_ws_all"):
        d = df.dropna(subset=[y, x, weights])
        d = d[np.isfinite(d[y]) & np.isfinite(d[x])]
        m = pf.feols(f"{y} ~ {x} | st_year + cell_year", data=d, weights=weights, vcov={"CRV1": "st"})
        t = m.tidy().loc[x]
        rows.append({"spec": label, "sample": sample, "y": y, "x": x, "coef": t["Estimate"],
                     "se": t["Std. Error"], "ci_low": t["2.5%"], "ci_high": t["97.5%"], "n": int(m._N),
                     "clusters": int(d.st.nunique())})

    fit(base, "U", "m_mexnc", "raw U on Mexico-born noncitizen share", "all cells 2012-2023")
    fit(base, "U", "m_unauth", "raw U on imputed unauthorized share", "all cells 2012-2023")
    fit(base, "U", "m_unauth_noba", "raw U on imputed unauthorized share without a bachelor's degree",
        "all cells 2012-2023")
    fit(base, "U", "m_fbnc", "raw U on foreign-born noncitizen share", "all cells 2012-2023")
    fit(base, "U_inc", "m_mexnc", "U with incorporated self-employed on Mexico-born noncitizen share",
        "all cells 2012-2023")
    # split sample: U from one half of households, the share from the other
    halves = []
    for h, o in (("0", "1"), ("1", "0")):
        d = base[["st", "st_year", "cell_year", "cell", "year", "n_ws_all", f"U_h{h}", f"m_mexnc_h{o}",
                  f"m_unauth_h{o}"]].copy()
        d.columns = ["st", "st_year", "cell_year", "cell", "year", "n_ws_all", "U_split", "m_mexnc_split",
                     "m_unauth_split"]
        halves.append(d)
    split = pd.concat(halves, ignore_index=True)
    fit(split, "U_split", "m_mexnc_split", "split-sample U on Mexico-born noncitizen share", "all cells 2012-2023")
    fit(split, "U_split", "m_unauth_split", "split-sample U on imputed unauthorized share", "all cells 2012-2023")
    variants = [  # (name, fixed effects, drop California and Texas, weighted)
        ("across states", "year", False, True),
        ("within state over time", "st + year", False, True),
        ("across states, without California and Texas", "year", True, True),
        ("across states, unweighted", "year", False, False),
    ]
    for c in FOCUS:
        sub = base[base.cell == c]
        if sub.st.nunique() < 20:
            continue
        for x in ("m_mexnc", "m_unauth"):
            for name, fe, drop, wtd in variants:
                d = sub.dropna(subset=["U", x])
                if drop:
                    d = d[~d.st.isin([6, 48])]
                m = pf.feols(f"U ~ {x} | {fe}", data=d, weights="n_ws_all" if wtd else None,
                             vcov={"CRV1": "st"})
                t = m.tidy().loc[x]
                rows.append({"spec": f"{CELLS[c]['label']}: U on {x}, {name}", "sample": c,
                             "y": "U", "x": x, "coef": t["Estimate"], "se": t["Std. Error"],
                             "ci_low": t["2.5%"], "ci_high": t["97.5%"], "n": int(m._N),
                             "clusters": int(d.st.nunique())})
    low = base[base.low_exposure]
    fit(low, "U", "m_mexnc", "placebo: low-exposure cells only", "low-exposure cells 2012-2023")
    no_ag = base[~base.cell.isin(["c111", "c112", "c115", "c11r"])]
    fit(no_ag, "U", "m_unauth", "raw U on imputed unauthorized share, agriculture excluded (own UI coverage rules)",
        "all cells except agriculture 2012-2023")
    fit(no_ag, "U", "m_mexnc", "raw U on Mexico-born noncitizen share, agriculture excluded",
        "all cells except agriculture 2012-2023")
    fit(no_ag, "U", "m_unauth_noba", "raw U on imputed unauthorized share without a bachelor's degree, "
        "agriculture excluded", "all cells except agriculture 2012-2023")
    # temp-help check: if staffing agencies (QCEW 5613, inside c56r) carried construction workers in
    # immigrant-heavy states, c56r's U would fall as construction's unauthorized share rises
    w = base.pivot_table(index=["st", "year"], columns="cell", values=["U", "m_unauth"])
    d = pd.DataFrame({"U56r": w["U"]["c56r"], "m23": w["m_unauth"]["c23"]}).dropna().reset_index()
    m = pf.feols("U56r ~ m23 | year", data=d, vcov={"CRV1": "st"})
    t = m.tidy().loc["m23"]
    rows.append({"spec": "check: U of other admin and support (temp help) on construction's unauthorized share",
                 "sample": "c56r", "y": "U", "x": "m_unauth of c23", "coef": t["Estimate"],
                 "se": t["Std. Error"], "ci_low": t["2.5%"], "ci_high": t["97.5%"], "n": int(m._N),
                 "clusters": int(d.st.nunique())})
    out = pd.DataFrame(rows)
    out.to_csv(DER / "uncovered_slopes.csv", index=False, lineterminator="\n", float_format="%.5f")
    return out


def main() -> None:
    DER.mkdir(exist_ok=True)
    acs, q = load()
    low = low_exposure_cells(acs)
    nat = national_table(acs, q, low)
    s = summary(nat)
    p = build_panel(acs, q, low)
    sl = slopes(p)
    pd.set_option("display.width", 220)
    print("low-exposure cells:", low)
    print(s[["cell", "acs_ws_m", "qcew_emp_m", "U_raw", "U_inc", "U_cal", "U_cal_min", "U_cal_max",
             "share_mexnc", "share_unauth", "uncovered_jobs_cal_m"]].to_string(index=False, float_format="%.3f"))
    print(sl[["spec", "sample", "coef", "se", "ci_low", "ci_high", "n", "clusters"]].to_string(index=False, float_format="%.3f"))
    print(f"panel rows {len(p):,}; usable 2012-2023 {int((p.ok & p.year.between(*YEARS_B)).sum()):,}")


if __name__ == "__main__":
    main()
