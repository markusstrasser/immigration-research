#!/usr/bin/env python3
"""Project the future adult Indian G2 from the parents of today's children, and price the shift.

Inputs (read, never typed):
  selection_curve_2026_09_27/derived/origin_curve.csv  India row of spec g1_1994_2004__g2_2015_2025:
      G1 1994-2004 (the parents' generation of today's adult G2) and the observed G2 2015-2025
  selection_curve_2026_09_27/derived/slopes.csv        G1->G2 slopes, all origins and without Mexico
  selection_curve_2026_09_27/_cache/ledger_persons.csv.gz  the Indian ledger's person-level fiscal
      net (CPS ASEC 2025, equal_all_members, extended balance after health, 160 SDR replicates)
  derived/acs_future_g2_parents.csv, derived/acs_calibration.csv  (acs_cohorts.py)
  the CPS frame (common.cps_prepared) for the India G1 2021-2025 mean

Projection: future G2 = observed G2 + b * (x_future - x_then), with b the cross-origin slope
(all origins; without Mexico) or India's own observed step k = (G2 - 50) / (G1 - 50) applied to
the distance from 50. Two x_future measures:
  (a) all India-born adults 25-64 in CPS 2021-2025 (like-for-like with x_then, an all-G1 mean)
  (b) the India-born parents of US-born children 0-17 (ACS), change 2005 -> 2023/24 on one
      instrument; the ACS 2005 children are 21-38 in 2026, the leading edge of the adult G2
Fiscal translation [INFERENCE]: the slope of the ledger's per-adult fiscal net on the adult's own
earnings (education) percentile, all civilian adults 25-64 in the ledger, times the percentile
shift. The percentile uses the ledger file's own third-plus NH white reference (same five-year
bands as the selection curve; wage and salary for earnings, A_HGA for education).

Outputs: derived/projection.csv, derived/fiscal_gradient.csv
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb --with pyarrow python3 \
      infra/immigration-fiscal/indian_cohort_selection_2026_09_29/project_g2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

cps_curve = C.cps_curve
LEDGER = C.SC / "_cache" / "ledger_persons.csv.gz"


def sdr(v: np.ndarray) -> tuple[float, float]:
    return float(v[0]), float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def fiscal_gradient() -> list[dict]:
    d = pd.read_csv(LEDGER)
    W = d[[f"w{j}" for j in range(161)]].to_numpy()
    band = C.band_of(d.age.to_numpy())
    ref = d.g_third_plus_nh_white.to_numpy() == 1
    pct = {}
    for var, col in (("earn", "wsal"), ("edu", "a_hga")):
        p = np.full(len(d), np.nan)
        y = d[col].to_numpy(float)
        for b in range(len(C.AGE_EDGES) - 1):
            m = band == b
            r = m & ref
            p[m] = cps_curve.midrank_pct(y[r], W[r, 0], y[m])
        pct[var] = p
    net = d.net.to_numpy()
    rows = []
    for var, p in pct.items():
        for sample, m in (("all adults 25-64", np.ones(len(d), bool)),
                          ("India-born and India G2", (d.g_india_born.to_numpy() == 1)
                           | (d.g_india_second_gen.to_numpy() == 1)),
                          ("pct 50-90, all adults", (p >= 50) & (p <= 90))):
            slopes = []
            for j in range(161):
                w = W[m, j]
                X = np.column_stack([np.ones(m.sum()), p[m]])
                beta = np.linalg.solve(X.T @ (X * w[:, None]), X.T @ (w * net[m]))
                slopes.append(beta[1])
            est, se = sdr(np.array(slopes))
            rows.append({"percentile": var, "sample": sample, "n": int(m.sum()),
                         "dollars_per_point": est, "se": se})
        # calibration: slope x (group mean percentile - 50) vs the ledger's gap for that group
        for g in ("india_born", "india_second_gen"):
            gm = d[f"g_{g}"].to_numpy() == 1
            mp = float(np.average(p[gm], weights=W[gm, 0]))
            gap = float(np.average(net[gm], weights=W[gm, 0]) - np.average(net[ref], weights=W[ref, 0]))
            rows.append({"percentile": var, "sample": f"calibration {g}: mean pct / ledger gap", "n": int(gm.sum()),
                         "dollars_per_point": mp, "se": gap})
    return rows


def main() -> int:
    oc = pd.read_csv(C.SC / "derived" / "origin_curve.csv")
    india = oc[(oc.spec == "g1_1994_2004__g2_2015_2025") & (oc.origin_code == C.INDIA_CPS)].iloc[0]
    sl = pd.read_csv(C.SC / "derived" / "slopes.csv").set_index("spec")
    slopes = {"edu": {"all origins (0.52)": sl.loc["G1->G2 education, main", "slope"],
                      "without Mexico": sl.loc["G1->G2 education, without Mexico", "slope"]},
              "earn": {"all origins": sl.loc["G1->G2 earnings, main", "slope"],
                       "without Mexico": sl.loc["G1->G2 earnings, without Mexico", "slope"]}}
    then = {"edu": india.g1_p_edu, "earn": india.g1_p_earn}
    g2_now = {"edu": india.g2_p_edu, "earn": india.g2_p_earn}

    # (a) India-born adults 25-64, CPS 2021-2025, white-reference age mix (selection-curve rule)
    df = C.cps_prepared()
    d = df[df.year >= 2021]
    r = d.ref.to_numpy()
    rs = d.loc[r].groupby("band").w.sum() / d.loc[r].w.sum()
    x_a = {}
    for var, col, ok in (("edu", "p_edu", "educ_ok"), ("earn", "p_earn", "earn_ok")):
        m = ((d.gen == 1) & (d.origin == C.INDIA_CPS) & d[ok]).to_numpy() & np.isfinite(d[col].to_numpy())
        x_a[var] = cps_curve.wmean_se(d.loc[m, col].to_numpy(), cps_curve.std_weights(d, m, rs))

    # (b) parents of US-born children, ACS; 2023-24 pooled vs 2005
    fut = pd.read_csv(C.DER / "acs_future_g2_parents.csv")
    us = fut[fut.children.str.startswith("US-born")].set_index("survey_year")
    cal = pd.read_csv(C.DER / "acs_calibration.csv")
    shift = {"edu": -cal[(cal.years == "2015-2024") & (cal.outcome == "p_edu")].acs_minus_cps.iloc[0],
             "earn": -cal[(cal.years == "2015-2024") & (cal.outcome == "p_earn")].acs_minus_cps.iloc[0]}

    def par(var, years):
        s = us.loc[years]
        return float(np.average(s[f"parent_p_{var}"], weights=s.weighted))

    rows = []
    for var in ("edu", "earn"):
        xb_now = par(var, [2023, 2024])
        xb_2005 = par(var, [2005])
        measures = {
            "(a) all India-born 25-64, CPS 2021-25 vs 1994-2004": (then[var], x_a[var][0]),
            "(b) parents of US-born children, ACS 2023-24 vs 2005": (xb_2005, xb_now),
        }
        k = (g2_now[var] - 50) / (then[var] - 50)
        for mname, (x0, x1) in measures.items():
            dx = x1 - x0
            base = {"outcome": "education" if var == "edu" else "wage earnings", "measure": mname,
                    "x_then": x0, "x_now": x1, "dx": dx, "g2_now_observed": g2_now[var],
                    "acs_to_cps_shift": shift[var] if mname.startswith("(b)") else 0.0}
            for sname, b in slopes[var].items():
                rows.append({**base, "arm": f"cross-origin slope, {sname}", "slope_or_step": b,
                             "d_g2": b * dx, "g2_future": g2_now[var] + b * dx})
            rows.append({**base, "arm": "India's observed step k=(G2-50)/(G1-50)", "slope_or_step": k,
                         "d_g2": k * dx, "g2_future": g2_now[var] + k * dx})
    C.write_csv(C.DER / "projection.csv", rows)
    fg = fiscal_gradient()
    C.write_csv(C.DER / "fiscal_gradient.csv", fg)
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
    print(pd.DataFrame(fg).round(2).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
