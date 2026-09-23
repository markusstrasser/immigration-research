"""Borjas (2001, BPEA) two-region efficiency gain: reproduce Table 8, then restate for 2024.

Model (Borjas 2001, eqs. 23-35): two regions with Q = A L^beta, delta = 1 - beta; N natives, a share
lambda < 0.5 in the high-wage region 1; M = m N immigrants settle once, a share theta in region 1,
M1 = theta k (1 - 2 lambda) N, M2 = (1 - theta) k (1 - 2 lambda) N; natives adjust with
ln(L1/L2)_{t+1} - ln(L1/L2)_t = sigma (ln w1 - ln w2)_t; R_t natives move at quadratic cost
phi R_t^2, phi set so the average cost at 1 million movers equals c x income per worker. Natives'
income is output less immigrants' wages less migration costs; the efficiency gain is
r x [max_sigma PV(theta = 1) - max_sigma PV(theta = lambda)] (eq. 34), "prohibitive" cost = sigma 0.

Three implementation choices, each fixed by reproducing the printed table rather than assumed:
- the present value runs over t = 0..99 (an infinite horizon puts the prohibitive cells 5% high);
- movers are the exact change in region-1 employment, R_t = L1_t - L1_{t-1} (eq. 32's linear
  approximation puts the sizable-gap cells 2.3-3.4bn high);
- sigma is searched on a 0.1 grid, the precision of the printed optima.
Gate: 11 of 12 printed gains within 0.1bn; the remaining cell (sizable gap, high cost, printed
12.4) must lie between the 0.1-grid and 0.01-grid optima; else exit non-zero before any 2024 row.

Writes derived/borjas_table8_reproduction.csv and derived/borjas_2024.csv.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
T = 100  # periods t = 0..99: reproduces the prohibitive-cost cells exactly (infinite horizon runs 5% high)

TABLE8 = {  # (lambda, k): {cost: (gain_bn, sigma1, sigma_lambda)}; prohibitive has no sigmas
    (0.45, 1.00): {"low": (2.7, 0.0, 0.3), "medium": (3.5, 0.0, 0.2), "high": (4.6, 0.0, 0.1), "prohibitive": (10.3,)},
    (0.40, 0.50): {"low": (4.7, 0.6, 0.3), "medium": (6.1, 0.4, 0.2), "high": (7.9, 0.3, 0.1), "prohibitive": (13.2,)},
    (0.30, 0.25): {"low": (6.9, 0.4, 0.3), "medium": (9.0, 0.3, 0.2), "high": (12.4, 0.2, 0.1), "prohibitive": (22.0,)},
}
COST_MULT = {"low": 0.5, "medium": 1.0, "high": 2.0}


def native_income_pv(theta, sigma, lam, k, N, gdp0, beta=0.7, r=0.03, cost_mult=1.0):
    delta = 1 - beta
    A = gdp0 / ((lam * N) ** beta + ((1 - lam) * N) ** beta)
    M1, M2 = theta * k * (1 - 2 * lam) * N, (1 - theta) * k * (1 - 2 * lam) * N
    M = M1 + M2
    x0 = np.log((lam + theta * k * (1 - 2 * lam)) / ((1 - lam) + (1 - theta) * k * (1 - 2 * lam)))
    t = np.arange(T)
    lr = (1 - delta * sigma) ** t * x0                       # ln(L1/L2), eq. 29
    L1 = (N + M) * np.exp(lr) / (1 + np.exp(lr))
    L2 = (N + M) - L1
    w1, w2 = beta * A * L1 ** (beta - 1), beta * A * L2 ** (beta - 1)
    R = np.concatenate([[0.0], np.diff(L1)])                 # natives moving into region 1
    income_per_worker = beta * gdp0 / N
    phi = cost_mult * income_per_worker / 1e6                # average cost phi*R at R = 1m movers
    flow = A * L1 ** beta + A * L2 ** beta - w1 * M1 - w2 * M2 - phi * R ** 2
    return float(np.sum(flow / (1 + r) ** t))


def gain(lam, k, cost, N=100e6, gdp0=10e12, beta=0.7, r=0.03, step=0.1, theta=1.0):
    """Borjas's eq. 34 with theta = 1; other theta gives the gain of the observed sorting."""
    if cost == "prohibitive":
        a = native_income_pv(theta, 0.0, lam, k, N, gdp0, beta, r)
        b = native_income_pv(lam, 0.0, lam, k, N, gdp0, beta, r)
        return r * (a - b) / 1e9, 0.0, 0.0
    grid = np.round(np.arange(0.0, 1 / (1 - beta) - 1e-6, step), 4)
    cm = COST_MULT[cost]
    v1 = [native_income_pv(theta, s, lam, k, N, gdp0, beta, r, cm) for s in grid]
    vl = [native_income_pv(lam, s, lam, k, N, gdp0, beta, r, cm) for s in grid]
    i1, il = int(np.argmax(v1)), int(np.argmax(vl))
    return r * (v1[i1] - vl[il]) / 1e9, float(grid[i1]), float(grid[il])


def reproduce():
    rows, worst = [], 0.0
    for (lam, k), cells in TABLE8.items():
        for cost, printed in cells.items():
            g, s1, sl = gain(lam, k, cost)
            g_fine = gain(lam, k, cost, step=0.01)[0]
            row = {"lambda": lam, "k": k, "cost": cost, "gain_bn": g, "gain_bn_fine_grid": g_fine,
                   "printed_gain_bn": printed[0], "sigma1": s1, "sigma_lambda": sl}
            if len(printed) == 3:
                row.update(printed_sigma1=printed[1], printed_sigma_lambda=printed[2])
                worst = max(worst, abs(s1 - printed[1]) / 0.05 * 0.1, abs(sl - printed[2]) / 0.05 * 0.1)
            worst = max(worst, abs(g - printed[0]))
            rows.append(row)
    df = pd.DataFrame(rows)
    DERIVED.mkdir(exist_ok=True)
    df.to_csv(DERIVED / "borjas_table8_reproduction.csv", index=False)
    print(df.round(3).to_string(index=False))
    return df, worst


def main():
    df, worst = reproduce()
    dev = (df["gain_bn"] - df["printed_gain_bn"]).abs()
    off = df[dev > 0.1 + 1e-9]
    lo, hi = off[["gain_bn", "gain_bn_fine_grid"]].min(axis=1), off[["gain_bn", "gain_bn_fine_grid"]].max(axis=1)
    ok = len(off) <= 1 and bool(((off["printed_gain_bn"] >= lo) & (off["printed_gain_bn"] <= hi)).all())
    if not ok:
        raise SystemExit("[FAILED] Table 8 not reproduced; no 2024 rows written")
    print("  ✓ Table 8 reproduced")
    inputs = json.loads((DERIVED / "borjas_2024_inputs.json").read_text())
    rows = []
    for scen in inputs["scenarios"]:
        m = scen["m"]
        for lam in (0.45, 0.40, 0.30):
            k = m / (1 - 2 * lam)
            srt = inputs["sorting"][str(lam)]
            theta_obs = srt["theta_mexfb_recent"] if "arrived" in scen["name"] else srt["theta_mexfb"]
            for sorting_case, theta in (("full_sorting_theta_1", 1.0), ("observed_sorting_2024", theta_obs)):
              for cost in ("low", "medium", "high", "prohibitive"):
                g, s1, sl = gain(lam, k, cost, N=inputs["native_workers"], gdp0=inputs["gdp_2024"], theta=theta)
                g_fine = gain(lam, k, cost, N=inputs["native_workers"], gdp0=inputs["gdp_2024"], step=0.01, theta=theta)[0]
                rows.append({"scenario": scen["name"], "m": m, "lambda": lam, "sorting": sorting_case,
                             "theta": theta, "initial_gap": 0.3 * np.log((1 - lam) / lam), "k": k, "cost": cost,
                             "gain_bn_2024": g, "gain_bn_2024_fine_grid": g_fine,
                             "sigma1": s1, "sigma_lambda": sl,
                             "share_of_gdp_pct": 100 * g * 1e9 / inputs["gdp_2024"]})
    pd.DataFrame(rows).to_csv(DERIVED / "borjas_2024.csv", index=False)
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
