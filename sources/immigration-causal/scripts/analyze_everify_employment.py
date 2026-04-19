"""Companion: did E-Verify reduce total low-education employment in exposed industries?

If yes (Bohn-Lofstrom-Raphael 2014), labor supply contracted as predicted but wages didn't
rise. That implies demand also adjusted: employers shifted to capital, formalized payroll
(unauthorized → cash economy elsewhere), or relocated. The Borjas substitution story
requires labor supply ↓ AND wages ↑. Falsifying the wage prediction while confirming the
quantity prediction is a meaningful update.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
OUT = DATA / "analysis"


def main():
    panel = pd.read_parquet(OUT / "qwi_everify_panel.parquet")
    panel["log_emp"] = np.log(panel["EmpS"].clip(lower=1))

    print("=" * 80)
    print("EMPLOYMENT TWFE — log(EmpS) ~ E-Verify mandate × education")
    print("(If Bohn-Lofstrom-Raphael, expect E1 employment ↓ in exposed industries)")
    print("=" * 80)
    rows = []
    for edu in ("E1", "E2", "E3", "E4"):
        for inds_label, inds in [("everify-exposed", ["11", "23", "31-33", "72"]), ("total-agg", ["00"])]:
            sub = panel[(panel["education"] == edu) & (panel["industry"].isin(inds))].dropna(subset=["log_emp", "treated", "state_fips", "year"])
            if len(sub) < 100:
                continue
            sub = sub.copy()
            # Within-transform
            sub["y_dm"] = sub["log_emp"] - sub.groupby("state_fips")["log_emp"].transform("mean")
            sub["y_dm"] = sub["y_dm"] - sub.groupby("year")["y_dm"].transform("mean")
            sub["x_dm"] = sub["treated"] - sub.groupby("state_fips")["treated"].transform("mean")
            sub["x_dm"] = sub["x_dm"] - sub.groupby("year")["x_dm"].transform("mean")
            y = sub["y_dm"].values
            x = sub["x_dm"].values
            xx = (x * x).sum()
            if xx == 0:
                continue
            beta = (x * y).sum() / xx
            resid = y - beta * x
            cluster_sums = sub.assign(xe=x * resid).groupby("state_fips")["xe"].sum().values
            meat = (cluster_sums ** 2).sum()
            n_c = len(cluster_sums)
            var_beta = (1 / xx) * meat * (1 / xx) * n_c / (n_c - 1) * (len(sub) - 1) / (len(sub) - 1)
            se = np.sqrt(var_beta)
            t = beta / se
            stars = "***" if abs(t) > 2.58 else ("**" if abs(t) > 1.96 else ("*" if abs(t) > 1.645 else ""))
            print(f"  edu={edu} ind={inds_label:18s}  β={beta:+.4f} ({(np.exp(beta)-1)*100:+.2f}%)  SE={se:.4f}  t={t:+.2f}{stars}  n={len(sub):,}")
            rows.append({"edu": edu, "ind": inds_label, "beta": beta, "se": se, "t": t, "n": len(sub)})

    pd.DataFrame(rows).to_csv(OUT / "everify_employment_twfe.csv", index=False)
    print()


if __name__ == "__main__":
    main()
