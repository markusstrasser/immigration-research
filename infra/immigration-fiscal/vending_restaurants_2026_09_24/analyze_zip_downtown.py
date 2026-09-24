"""Sensitivity added after seeing results: the arrest-exposure ZIP design without downtown Los Angeles.

The one pro-harm pattern in design (b) is full-service restaurants in the City of LA ZIPs with the most
2010-2016 vending arrests, below their pre-2018 trend in 2022-2023. Several of those ZIPs are downtown,
which lost office workers and visitors after 2020. This re-runs the same event study and trend-adjusted
fit (analyze_zip.fit, analyze_zip.fit_trend) on City of LA ZIPs without the downtown set below
(the ZCTAs of the Central City and Central City North area as commonly drawn; a choice, not a
published boundary). 90057 Westlake-MacArthur Park, the most-arrested ZIP, stays in. Each row also
converts the event-study coefficient into establishments against an arrest-free ZIP,
b * sum_z(x_z * establishments_z in 2018), with the 95% interval for 2019.

Writes derived/zip_arrests_no_downtown.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_zip_downtown.py
"""
import numpy as np
import pandas as pd

from analyze_zip import CODES, REF, YEARS, fit, fit_trend, la_city_zctas
from lib import CACHE, DERIVED

DOWNTOWN = {"90012", "90013", "90014", "90015", "90017", "90021", "90071"}


def main() -> None:
    z = pd.read_csv(CACHE / "zbp_la_panel.csv", dtype={"zip": str, "naics": str})
    ex = pd.read_csv(DERIVED / "exposure_zcta_ca.csv", dtype={"zcta": str}).set_index("zcta")
    arr = pd.read_csv(DERIVED / "lapd_vending_arrests_zcta.csv", dtype={"zcta": str}).set_index("zcta")
    city = la_city_zctas()
    rows = []
    for code in CODES:
        d0 = z[z["naics"] == code].copy()
        n = d0.groupby("zip")["year"].nunique()
        d0 = d0[d0["zip"].isin(n[n == len(YEARS)].index) & (d0["estab"] > 0)]
        d0 = d0.join(ex[["pop"]], on="zip")
        d0 = d0[(d0["pop"] >= 1000) & d0["zip"].isin(city)]
        d0["x"] = np.log1p(d0["zip"].map(arr["arrests_2010_2016"]).fillna(0))
        d0["ly"] = np.log(d0["estab"])
        for sample, d in (("all City ZIPs", d0), ("without downtown", d0[~d0["zip"].isin(DOWNTOWN)])):
            dropped = sorted(set(d0["zip"]) & DOWNTOWN) if sample == "without downtown" else []
            for yvar, model in (("ly", "ols"), ("estab", "poisson")):
                co, p_pre = fit(d, yvar, model)
                c = co.set_index("year")
                t = fit_trend(d, yvar, model).set_index("term")
                r = {"naics": code, "sample": sample, "outcome": "log_estab" if yvar == "ly" else "estab_poisson",
                     "n_zips": d["zip"].nunique(), "downtown_zips_dropped": " ".join(dropped),
                     "arrests_share_kept": round(float(
                         arr.loc[arr.index.isin(d["zip"].unique()), "arrests_2010_2016"].sum()
                         / arr.loc[arr.index.isin(d0["zip"].unique()), "arrests_2010_2016"].sum()), 3),
                     "b2019": c.loc[2019, "coef"], "se2019": c.loc[2019, "se"],
                     "b2022_23": c.loc[[2022, 2023], "coef"].mean(), "p_pretrend": p_pre,
                     "pre_trend_per_year": t.loc["xtrend", "coef"], "pre_trend_se": t.loc["xtrend", "se"],
                     "dev2019": t.loc["x2019", "coef"], "dev2019_se": t.loc["x2019", "se"],
                     "dev2022_23": (t.loc["x2022", "coef"] + t.loc["x2023", "coef"]) / 2,
                     "dev2022_se": t.loc["x2022", "se"], "dev2023_se": t.loc["x2023", "se"]}
                # implied establishments against an arrest-free ZIP: b * sum_z x_z * estab_z(2018)
                base18 = d[d["year"] == REF]
                lever = float((base18["x"] * base18["estab"]).sum())
                r.update(estab_2018=int(base18["estab"].sum()), implied_estab_2019=r["b2019"] * lever,
                         implied_estab_2019_lo=(r["b2019"] - 1.96 * r["se2019"]) * lever,
                         implied_estab_2019_hi=(r["b2019"] + 1.96 * r["se2019"]) * lever,
                         implied_estab_2022_23=r["b2022_23"] * lever)
                rows.append(r)
                print(f"  {code} {sample} {r['outcome']}: {r['n_zips']} ZIPs (arrests kept {r['arrests_share_kept']:.0%}); "
                      f"b2019 {r['b2019']:+.4f} ({r['se2019']:.4f}); dev2022-23 {r['dev2022_23']:+.4f} "
                      f"({r['dev2022_se']:.4f}, {r['dev2023_se']:.4f})", flush=True)
    pd.DataFrame(rows).to_csv(DERIVED / "zip_arrests_no_downtown.csv", index=False, lineterminator="\n",
                              float_format="%.6g")


if __name__ == "__main__":
    main()
