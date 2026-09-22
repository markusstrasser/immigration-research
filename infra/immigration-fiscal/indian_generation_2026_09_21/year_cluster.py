#!/usr/bin/env python3
"""Year-cluster SEs and stacked age-band gaps from analyze_cps.py outputs."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
BANDS = [(25, 34), (35, 44), (45, 54), (55, 64)]


def year_cluster(frame, group, col):
    v = frame.loc[frame.group == group, col].to_numpy(float)
    v = v[np.isfinite(v)]
    if len(v) < 2:
        return float("nan"), float("nan"), len(v)
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v))), len(v)


def main():
    years = pd.read_csv(OUT / "cps_generation_years.csv")
    adult = years.query("universe == 'adults_25_64'").copy()
    white = adult[adult.group == "white_g3plus"]
    rows = []
    for g in ["india_g1", "india_g2", "india_g3plus_race", "india_g2_diaspora",
              "asian_indian_native_selfid"]:
        for col in ["earnings", "tax_minus_cash", "ba_share",
                    "age_std_earnings", "age_std_tax_minus_cash", "age_std_ba"]:
            m, se, n = year_cluster(adult, g, col)
            wm, wse, _ = year_cluster(adult, "white_g3plus", col)
            gap = m - wm
            gap_se = float(np.hypot(se, wse)) if np.isfinite(se) else float("nan")
            rows.append({"group": g, "metric": col, "mean": m, "se_year": se,
                         "white": wm, "gap": gap, "gap_se_year": gap_se, "n_years": n})
            print(f"{g:28} {col:24} {m:10,.4f}  se {se:8,.4f}  gap {gap:10,.4f} ({gap_se:,.4f})")
    pd.DataFrame(rows).to_csv(OUT / "cps_generation_year_cluster.csv", index=False, float_format="%.6f")

    print("\n== year-by-year G3 tax-minus-cash vs white ==", flush=True)
    g3 = adult[adult.group == "india_g3plus_race"][["year", "n", "tax_minus_cash", "earnings", "ba_share"]]
    w = white.set_index("year")
    for _, r in g3.iterrows():
        y = int(r.year)
        print(f"  {y} n={int(r.n):3d}  G3 net={r.tax_minus_cash:8,.0f}  "
              f"white={w.loc[y,'tax_minus_cash']:8,.0f}  "
              f"gap={r.tax_minus_cash-w.loc[y,'tax_minus_cash']:8,.0f}  "
              f"BA={r.ba_share:.1%}  earn={r.earnings:,.0f}", flush=True)


if __name__ == "__main__":
    main()
