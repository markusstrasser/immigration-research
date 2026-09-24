"""Placebo for design (b): the same within-county ZIP event study in six large high-Hispanic counties of
states without statewide vending legalization (Harris, Dallas, Bexar, Maricopa, Cook, Miami-Dade).

If Los Angeles's post-2018 gradient by Hispanic share looks like theirs, the Los Angeles result
reflects something common to Hispanic neighbourhoods of big metros, not vending law.
Same specification as analyze_zip.py (log establishments on ZIPs present every year, ZIPs with at
least 1,000 residents, ZIP and year fixed effects, exposure x year, 2018 omitted, clustered by ZIP).

Writes derived/zip_placebo_summary.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_zip_placebo.py
"""
import warnings

import numpy as np
import pandas as pd

from analyze_zip import YEARS, fit
from fetch_zbp_placebo import COUNTIES
from lib import CACHE, DERIVED

warnings.filterwarnings("ignore")
CODES = ["722511", "722513", "722", "445110"]


def panels() -> dict:
    la = pd.read_csv(CACHE / "zbp_la_panel.csv", dtype={"zip": str, "naics": str})
    la_ex = pd.read_csv(DERIVED / "exposure_zcta_ca.csv", dtype={"zcta": str}).set_index("zcta")
    out = {"06037 los angeles": (la, la_ex)}
    pl = pd.read_csv(CACHE / "zbp_placebo_panel.csv", dtype={"zip": str, "naics": str, "county": str})
    pl_ex = pd.read_csv(DERIVED / "exposure_zcta_placebo.csv", dtype={"zcta": str}).set_index("zcta")
    for fips, tag in COUNTIES.items():
        out[f"{fips} {tag}"] = (pl[pl["county"] == fips], pl_ex)
    return out


def main() -> None:
    rows = []
    for area, (z, ex) in panels().items():
        for code in CODES:
            d0 = z[z["naics"] == code].copy()
            n = d0.groupby("zip")["year"].nunique()
            d0 = d0[d0["zip"].isin(n[n == len(YEARS)].index) & (d0["estab"] > 0)]
            d0 = d0.join(ex[["pop", "hisp_share", "mexborn_share"]], on="zip")
            d0 = d0[d0["pop"] >= 1000]
            d0["ly"] = np.log(d0["estab"])
            for xname in ("hisp_share", "mexborn_share"):
                d = d0.dropna(subset=[xname]).copy()
                d["x"] = d[xname] * 10
                if d["zip"].nunique() < 30:
                    continue
                for yvar, model in (("ly", "ols"), ("estab", "poisson")):
                    co, p_pre = fit(d, yvar, model)
                    c = co.set_index("year")
                    rows.append({"area": area, "naics": code, "exposure": xname,
                                 "outcome": "log_estab" if yvar == "ly" else "estab_poisson",
                                 "n_zips": d["zip"].nunique(), "b2019": c.loc[2019, "coef"], "se2019": c.loc[2019, "se"],
                                 "b2022_23": c.loc[[2022, 2023], "coef"].mean(),
                                 "b2012": c.loc[2012, "coef"], "p_pretrend": p_pre})
            print(f"  {area} {code}: done", flush=True)
    r = pd.DataFrame(rows)
    r.to_csv(DERIVED / "zip_placebo_summary.csv", index=False, lineterminator="\n", float_format="%.6g")
    main_rows = r[(r["exposure"] == "hisp_share") & (r["outcome"] == "log_estab")]
    print(main_rows.pivot_table(index="area", columns="naics", values=["b2019", "b2022_23"]).round(4).to_string())


if __name__ == "__main__":
    main()
