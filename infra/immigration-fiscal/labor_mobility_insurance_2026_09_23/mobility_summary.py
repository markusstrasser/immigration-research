"""Present-day mobility by nativity (brief task 3), and the groups' employment cyclicality.

Reads derived/mobility_national.csv (acs_extract.py; ACS 1-year person files, SDR replicate SEs) and
averages each rate over 2006-2010 (Cadena-Kovak's window) and 2019-2024 (no 2020 file); a period
mean's SE assumes independent years, sqrt(sum se^2) / n. Employment-to-population ratios of men with
high school or less, 18-64, not in school or group quarters, come from the person extracts in
_cache/acs/ (2006, 2010, 2019, 2021, 2024), with SDR replicate SEs.

Writes derived/mobility_summary.csv and derived/employment_cyclicality.csv.
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
PERIODS = {"2006_2010": range(2006, 2011), "2019_2024": [2019, 2021, 2022, 2023, 2024], "2024": [2024]}


def mobility():
    m = pd.read_csv(DERIVED / "mobility_national.csv")
    rows = []
    for (grp, low, sex, meas), d in m.groupby(["group", "lowed", "sex", "measure"]):
        for per, yrs in PERIODS.items():
            x = d[d["year"].isin(list(yrs))]
            if len(x) != len(list(yrs)):
                continue
            rows.append({"group": grp, "lowed": low, "sex": sex, "measure": meas, "period": per,
                         "rate_pct": 100 * x["rate"].mean(),
                         "se_pct": 100 * np.sqrt((x["se"] ** 2).sum()) / len(x), "years": len(x)})
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "mobility_summary.csv", index=False)
    return out


def emp_rates():
    """E/P by group; the extracts keep no replicate weights, so the SE uses Kish's effective n."""
    rows = []
    for y in (2006, 2010, 2019, 2021, 2024):
        p = pd.read_parquet(HERE / "_cache" / "acs" / f"p{y}.parquet",
                            columns=["pwgtp", "employed", "group", "gq", "inschool", "lowed", "sex"])
        p = p[(~p["gq"]) & (~p["inschool"]) & p["lowed"] & (p["sex"] == 1)]
        for g in ("mex_fb", "mex_nb", "oth_nb", "oth_fb"):
            x = p[p["group"] == g]
            w, e = x["pwgtp"].to_numpy(float), x["employed"].to_numpy(float)
            est = np.average(e, weights=w)
            n_eff = w.sum() ** 2 / (w ** 2).sum()
            rows.append({"year": y, "group": g, "ep": est, "se": np.sqrt(est * (1 - est) / n_eff), "n": len(x)})
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "employment_cyclicality.csv", index=False)
    return out


def main():
    mob = mobility()
    show = mob[(mob["lowed"] == "hs_or_less") & (mob["sex"] == "men")
               & mob["measure"].isin(["moved_abroad", "moved_interstate", "long_distance"])]
    print(show.pivot_table(index=["measure", "group"], columns="period", values="rate_pct").round(2).to_string())
    print(show.pivot_table(index=["measure", "group"], columns="period", values="se_pct").round(3).to_string())
    alled = mob[(mob["lowed"] == "all") & (mob["sex"] == "all") & (mob["measure"] == "long_distance")]
    print(alled.pivot_table(index="group", columns="period", values="rate_pct").round(2).to_string())
    ep = emp_rates()
    print(ep.pivot_table(index="group", columns="year", values="ep").mul(100).round(1).to_string())
    print(ep.pivot_table(index="group", columns="year", values="se").mul(100).round(2).to_string())


if __name__ == "__main__":
    main()
