#!/usr/bin/env python3
"""Disconfirmation check for Test C: is the negative association between the group's share and
covered average wages what composition alone predicts?

QCEW's average weekly wage covers every on-books job, including the group's own on-books workers,
who earn less than the other workers in the same industry. A rising group share lowers the covered
average with no wage cut to anyone. For each focus cell and year (2012-2023, one year at a time,
then averaged) the ACS gives the group's share m of private wage and salary workers and its mean
annual pay relative to the others, r. With a fraction f = 1 - b of the group on the books (b is the
uncovered-share slope from uncovered.py, central across-state estimate, clipped to [0, 1]), the
covered average is W(m) = ((1 - m) w_o + m f w_u) / ((1 - m) + m f), and the composition-only
slope is d ln W / d m at the year's m. The script sets it beside the long-difference and
first-difference estimates of panel_c.py for the focus cells, and beside a long difference
estimated one focus cell at a time across states, net of the state's low-exposure cells (added
after the pooled comparison: the pooled estimate mixes cells whose composition slopes differ in
sign).

Output: derived/composition_check.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/compliance_gap_2026_09_24/composition.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cells import CELLS, FOCUS  # noqa: E402

DER = HERE / "derived"
YEARS = (2012, 2023)


def ln_w(m: float, f: float, w_u: float, w_o: float) -> float:
    return float(np.log(((1 - m) * w_o + m * f * w_u) / ((1 - m) + m * f)))


def per_cell_long_differences() -> pd.DataFrame:
    """Long difference 2012-13 to 2022-23 of ln covered average weekly wage, one focus cell at a
    time across states, net of the same change in the state's low-exposure cells (weighted by ACS
    sample count), on the change in the group's share. Weighted least squares with the start
    sample count, heteroskedasticity-robust (HC1) standard errors."""
    p = pd.read_parquet(HERE / "_cache" / "panel" / "panel.parquet")
    ends = {"start": (2012, 2013), "end": (2022, 2023)}
    parts = []
    for name, yrs in ends.items():
        d = p[p.year.isin(yrs) & p.ok].groupby(["st", "cell"]).agg(
            q_emp=("q_emp", "mean"), q_wages=("q_wages", "mean"), m=("m_unauth", "mean"),
            n=("n_ws_all", "sum"), years=("year", "nunique"), low=("low_exposure", "first"))
        parts.append(d[d.years == 2].add_suffix(f"_{name}"))
    ld = parts[0].join(parts[1], how="inner").reset_index()
    ld["dy"] = np.log((ld.q_wages_end / ld.q_emp_end) / (ld.q_wages_start / ld.q_emp_start))
    ld["dm"] = ld.m_end - ld.m_start
    low = ld[ld.low_start.astype(bool)].assign(wy=lambda f: f.dy * f.n_start).groupby("st")[["wy", "n_start"]].sum()
    ld = ld.merge((low.wy / low.n_start).rename("dy_low").reset_index(), on="st", how="inner")
    ld["dy_rel"] = ld.dy - ld.dy_low
    rows = []
    for c in FOCUS:
        d = ld[(ld.cell == c)].replace([np.inf, -np.inf], np.nan).dropna(subset=["dy_rel", "dm"])
        if len(d) < 15:
            rows.append({"cell": c, "ld_states": len(d)})
            continue
        X = np.column_stack([np.ones(len(d)), d.dm.to_numpy()])
        w = d.n_start.to_numpy(dtype=float)
        y = d.dy_rel.to_numpy()
        XtW = X.T * w
        beta = np.linalg.solve(XtW @ X, XtW @ y)
        e = y - X @ beta
        bread = np.linalg.inv(XtW @ X)
        meat = (X.T * (w * e) ** 2) @ X
        V = bread @ meat @ bread * len(d) / (len(d) - 2)
        rows.append({"cell": c, "ld_coef": beta[1], "ld_se": float(np.sqrt(V[1, 1])), "ld_states": len(d)})
    return pd.DataFrame(rows)


def main() -> None:
    con = duckdb.connect()
    a = con.execute(f"""SELECT year, cell, sum(ws) AS ws, sum(ws_unauth) AS wu, sum(ws_wagebill) AS bill,
        sum(ws_wagebill_unauth) AS bill_u FROM '{HERE}/_cache/panel/acs_cells.parquet'
        WHERE half = 'all' AND year BETWEEN {YEARS[0]} AND {YEARS[1]} GROUP BY 1, 2""").df()
    s = pd.read_csv(DER / "uncovered_slopes.csv")
    rows = []
    for c in FOCUS:
        sc = s[(s["sample"] == c) & (s.x == "m_unauth") & s.spec.str.endswith(", across states")]
        if sc.empty:  # farm support (c115): uncovered.py estimates no slope; see its docstring
            print(f"  ! {c}: no uncovered-share slope; left out")
            continue
        b = min(max(float(sc.coef.iloc[0]), 0.0), 1.0)
        for _, r in a[a.cell == c].sort_values("year").iterrows():
            m = r.wu / r.ws
            w_u, w_o = r.bill_u / r.wu, (r.bill - r.bill_u) / (r.ws - r.wu)
            h = 1e-4
            slope = (ln_w(m + h, 1 - b, w_u, w_o) - ln_w(m - h, 1 - b, w_u, w_o)) / (2 * h)
            rows.append({"cell": c, "industry": CELLS[c]["label"], "year": int(r.year), "m_unauth": m,
                         "pay_ratio_group_to_others": w_u / w_o, "b_offbooks": b, "composition_slope": slope,
                         "ws": r.ws})
    y = pd.DataFrame(rows)
    per_cell = y.groupby(["cell", "industry"]).agg(m_unauth=("m_unauth", "mean"),
                                                   pay_ratio=("pay_ratio_group_to_others", "mean"),
                                                   b_offbooks=("b_offbooks", "first"),
                                                   composition_slope=("composition_slope", "mean"),
                                                   ws_m=("ws", lambda v: v.mean() / 1e6)).reset_index()
    pooled = pd.DataFrame([{"cell": "focus (worker-weighted)", "industry": "all focus cells",
                            "m_unauth": np.average(per_cell.m_unauth, weights=per_cell.ws_m),
                            "pay_ratio": np.average(per_cell.pay_ratio, weights=per_cell.ws_m),
                            "b_offbooks": np.nan,
                            "composition_slope": np.average(per_cell.composition_slope, weights=per_cell.ws_m),
                            "ws_m": per_cell.ws_m.sum()}])
    out = pd.concat([per_cell, pooled], ignore_index=True)
    out = out.merge(per_cell_long_differences(), on="cell", how="left")
    p = pd.read_csv(DER / "panel_c.csv")
    est = p[(p["sample"] == "focus cells") & (p.y.isin(["dy_wkwage", "d_ln_wkwage"])) &
            (p.x.isin(["dm_unauth", "d_m_unauth", "d_m_unauth_lag"]))][["design", "x", "coef", "se"]]
    out.to_csv(DER / "composition_check.csv", index=False, lineterminator="\n", float_format="%.5g")
    pd.set_option("display.width", 200)
    print(out.to_string(index=False, float_format="%.4f"))
    print("panel_c.py estimates for the focus cells (ln covered weekly wage on the group's share):")
    print(est.to_string(index=False, float_format="%.4f"))


if __name__ == "__main__":
    main()
