#!/usr/bin/env python3
"""Translate composition coefficients into dollars, as an explicit range.

Every figure is a WITHIN-METRO RELATIVE price. A neighbourhood's relative
decline is another neighbourhood's relative gain, so these numbers are transfers
across locations inside a metro, not resource costs, and they are the price of a
bundle (schools, crime, income mix) that moves with composition, not a price of
ethnicity.
"""
import pathlib, sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import prep

DERIVED = prep.DERIVED
CAP_RATES = [0.04, 0.06]


def wmean(d, col, w):
    v, ww = d[col].to_numpy(float), d[w].to_numpy(float)
    m = np.isfinite(v) & np.isfinite(ww)
    return float(np.average(v[m], weights=ww[m]))


def main():
    rent_u = pd.read_csv(DERIVED / "est_universe_rent.csv", dtype={"cbsa": str})
    val_u = pd.read_csv(DERIVED / "est_universe_value.csv", dtype={"cbsa": str})
    base = {
        "annual_rent_per_renter_hh": 12 * wmean(rent_u, "med_rent_1", "_w"),
        "home_value_per_owner_unit": wmean(val_u, "med_value_1", "_w"),
        "pop_per_tract": wmean(val_u, "pop_1", "_w"),
        "renter_hh_per_tract": wmean(rent_u, "rent_units_1", "_w"),
        "owner_units_per_tract": wmean(val_u, "own_units_1", "_w"),
    }
    main_res = pd.read_csv(DERIVED / "results_main.csv")
    zres = pd.read_csv(DERIVED / "results_zillow.csv")

    arms = []
    for grp in ["hisp", "mex", "fb"]:
        for samp in ["full", "sw"]:
            for arm in ["ols2_baseline", "ols3_meanrev"]:
                for out in ["rent", "value"]:
                    r = main_res[(main_res.treat == grp) & (main_res["sample"] == samp)
                                 & (main_res.period == "pooled") & (main_res.arm == arm)
                                 & (main_res.outcome == out)]
                    if len(r):
                        arms.append({"source": f"ACS tract {arm} [{samp}]", "treat": grp,
                                     "outcome": out, "coef": float(r.coef.iloc[0]),
                                     "se": float(r.se.iloc[0]),
                                     "measure": "ACS (same survey as regressor)"})
    for _, r in zres[zres.label.str.startswith("MATCHED")].iterrows():
        if r.period != "pooled":
            continue
        out = "value" if "value" in r.label else "rent"
        arms.append({"source": f"ZCTA {r.label}", "treat": r.treat, "outcome": out,
                     "coef": r.coef, "se": r.se,
                     "measure": ("Zillow (independent)" if "Zillow" in r.label
                                 else "ACS (same survey as regressor)")})
    A = pd.DataFrame(arms)

    rows = []
    for _, r in A.iterrows():
        pct = np.expm1(0.10 * r.coef)          # effect of a +10pp share change
        if r.outcome == "rent":
            per_hh = base["annual_rent_per_renter_hh"] * pct
            tract_total = per_hh * base["renter_hh_per_tract"]
            per_res = tract_total / (0.10 * base["pop_per_tract"])
            rows.append({**r, "pct_change": 100 * pct,
                         "dollars_per_affected_household_year": per_hh,
                         "dollars_per_group_resident_year": per_res,
                         "capitalised_per_owner_unit": np.nan})
        else:
            per_unit = base["home_value_per_owner_unit"] * pct
            tract_total = per_unit * base["owner_units_per_tract"]
            per_res_cap = tract_total / (0.10 * base["pop_per_tract"])
            for cr in CAP_RATES:
                rows.append({**r, "pct_change": 100 * pct,
                             "dollars_per_affected_household_year": per_unit * cr,
                             "dollars_per_group_resident_year": per_res_cap * cr,
                             "capitalised_per_owner_unit": per_unit,
                             "cap_rate": cr})
    D = pd.DataFrame(rows)
    D.to_csv(DERIVED / "results_dollars.csv", index=False, float_format="%.6g")

    lines = ["BASE QUANTITIES (weighted means over the estimation universe, end of period)"]
    for k, v in base.items():
        lines.append(f"  {k}: {v:,.1f}")
    lines.append("")
    lines.append("DOLLARS PER +10 PERCENTAGE POINTS OF GROUP SHARE, per group resident-year")
    for grp in ["hisp", "mex", "fb"]:
        s = D[D.treat == grp]
        if not len(s):
            continue
        acs = s[s.measure.str.startswith("ACS")]["dollars_per_group_resident_year"]
        ind = s[s.measure.str.startswith("Zillow")]["dollars_per_group_resident_year"]
        lines.append(f"  {grp}: ACS-measured arms {acs.min():+,.0f} to {acs.max():+,.0f}"
                     f" | independent-measure arms "
                     + (f"{ind.min():+,.0f} to {ind.max():+,.0f}" if len(ind) else "n/a"))
    txt = "\n".join(lines)
    (DERIVED / "dollars_summary.txt").write_text(txt + "\n")
    print(txt)
    print()
    print(D[["source", "treat", "outcome", "coef", "pct_change",
             "dollars_per_affected_household_year",
             "dollars_per_group_resident_year"]].to_string(index=False))


if __name__ == "__main__":
    main()
