"""Taxable sales: did food-service sales fall where vending exposure is high, after 2018?

CDTFA taxable sales, 2015-2025 annual (sum of four quarters), California only, so the comparison is
across places inside California by pre-2018 exposure (there is no out-of-state taxable-sales series):
  county level  58 counties;  city level  the 88 incorporated cities of Los Angeles County.
Outcomes: log taxable sales of food services and drinking places (C08, NAICS 722), of food and
beverage stores (C04, the placebo), their difference, and log C08 seller's permits in Q4 (cities:
outlets). C08 includes permitted sidewalk vendors and food trucks, so a shift from restaurants to
permitted vendors does not show here; a shift to unpermitted vendors does.
Model: outcome = unit FE + year FE + sum_k b_k * X * 1[year = k], k != 2018; X = Hispanic share
(ACS 2013-2017, per 10 points) or Mexico-born share; clustered by unit; unweighted and
population-weighted. Cities with a disclosure flag in any year are dropped.

Writes derived/sales_event_coefs.csv, derived/sales_event_summary.csv, derived/la_city_c08_sales.csv.
Run from the repository root with CENSUS_API_KEY set:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_sales.py
"""
import warnings

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

from lib import CACHE, DERIVED, census_json

warnings.filterwarnings("ignore")
REF = 2018
YEARS = list(range(2015, 2026))
ACS = "https://api.census.gov/data/2017/acs/acs5"


def places() -> pd.DataFrame:
    v = ["B03002_001E", "B03002_012E", "B05006_139E"]
    rows = census_json(f"{ACS}?get=NAME,{','.join(v)}&for=place:*&in=state:06", CACHE / "acs" / "acs5_2017_place_ca.json",
                       need_cols=tuple(v))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    for c in v:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["name"] = (df["NAME"].str.replace(r" (city|town|CDP), California$", "", regex=True)
                  .str.replace("ñ", "n").str.replace("La Canada Flintridge", "La Canada-Flintridge"))
    df = df[df["NAME"].str.contains(r" (city|town), California$")]
    df["pop"] = df["B03002_001E"]
    df["hisp_share"] = df["B03002_012E"] / df["pop"]
    df["mexborn_share"] = df["B05006_139E"] / df["pop"]
    return df.set_index("name")[["pop", "hisp_share", "mexborn_share"]]


def panel(level: str) -> pd.DataFrame:
    f = CACHE / f"cdtfa_{level}_annual.csv"
    d = pd.read_csv(f)
    if level == "county":  # the county file repeats the county name in its second column
        d = d.loc[:, ~d.columns.duplicated()].copy()
    d = d[d["year"].isin(YEARS) & (d["quarters"] == 4)]
    unit = level
    keys = [unit, "year"] if level == "county" else [unit, "county", "year"]
    w = d.pivot_table(index=keys, columns="group", values=["taxable", "permits_q4"], aggfunc="first")
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index().rename(columns={unit: "unit"})
    if level == "county":
        w["county"] = w["unit"]
    flagged = set(d.loc[d["flag"].notna() & (d["flag"] != ""), level])
    w = w[~w["unit"].isin(flagged)]
    w = w[(w["taxable_C08"] > 0) & (w["taxable_C04"] > 0)]
    n = w.groupby("unit")["year"].nunique()
    w = w[w["unit"].isin(n[n == len(YEARS)].index)].copy()
    w["l_c08"] = np.log(w["taxable_C08"])
    w["l_c04"] = np.log(w["taxable_C04"])
    w["l_diff"] = w["l_c08"] - w["l_c04"]
    w["l_permits"] = np.log(w["permits_q4_C08"].astype(float))
    return w


def fit(d: pd.DataFrame, yvar: str, weight: str | None) -> tuple[pd.DataFrame, float]:
    d = d.copy()
    names = []
    for k in YEARS:
        if k == REF:
            continue
        d[f"x{k}"] = d["x"] * (d["year"] == k)
        names.append(f"x{k}")
    m = pf.feols(f"{yvar} ~ " + " + ".join(names) + " | unit + year", data=d, weights=weight,
                 vcov={"CRV1": "unit"})
    b, se = m.coef(), m.se()
    co = pd.DataFrame({"year": [int(n[1:]) for n in names], "coef": b[names].values, "se": se[names].values})
    pre = [n for n in names if int(n[1:]) < REF]
    idx = [list(b.index).index(n) for n in pre]
    V = m._vcov
    W = float(b[pre].values @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ b[pre].values)
    return co, float(1 - stats.chi2.cdf(W, len(pre)))


def main() -> None:
    ex_c = pd.read_csv(DERIVED / "exposure_county.csv", dtype={"fips": str})
    ex_c = ex_c[ex_c["fips"].str.startswith("06")].copy()
    ex_c["unit"] = ex_c["NAME"].str.replace(" County, California", "", regex=False).str.upper()
    ex_c = ex_c.set_index("unit")[["pop", "hisp_share", "mexborn_share"]]
    ex_p = places()
    coef_rows, summ_rows = [], []
    for level, ex in (("county", ex_c), ("city", ex_p)):
        d0 = panel(level)
        if level == "city":
            d0 = d0[d0["county"] == "LOS ANGELES"]
        d0 = d0.join(ex, on="unit")
        missing = sorted(d0.loc[d0["hisp_share"].isna(), "unit"].unique())
        if missing:
            print(f"  {level}: no ACS match for {missing}")
        d0 = d0.dropna(subset=["hisp_share"])
        for xname in ("hisp_share", "mexborn_share"):
            d = d0.copy()
            d["x"] = d[xname] * 10
            for yvar in ("l_c08", "l_c04", "l_diff", "l_permits"):
                for wname in ("none", "pop"):
                    co, p_pre = fit(d, yvar, "pop" if wname == "pop" else None)
                    c = co.set_index("year")
                    tag = dict(level=level, exposure=xname, outcome=yvar, weight=wname, n_units=d["unit"].nunique())
                    coef_rows += [{**tag, **r} for r in co.to_dict("records")]
                    s = {**tag, "b2019": c.loc[2019, "coef"], "se2019": c.loc[2019, "se"],
                         "b2022_23": c.loc[[2022, 2023], "coef"].mean(), "b2024_25": c.loc[[2024, 2025], "coef"].mean(),
                         "b2020_21": c.loc[[2020, 2021], "coef"].mean(), "p_pretrend": p_pre}
                    summ_rows.append(s)
                    print(f"  {level} {xname} {yvar} {wname}: {tag['n_units']} units; b2019 {s['b2019']:+.4f} "
                          f"({s['se2019']:.4f}); b2022-23 {s['b2022_23']:+.4f}; pre p {p_pre:.3f}", flush=True)
    pd.DataFrame(coef_rows).to_csv(DERIVED / "sales_event_coefs.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")
    pd.DataFrame(summ_rows).to_csv(DERIVED / "sales_event_summary.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")
    c = pd.read_csv(CACHE / "cdtfa_city_annual.csv")
    la = c[(c["city"] == "Los Angeles") & (c["group"] == "C08") & (c["quarters"] == 4)][["year", "taxable", "permits_q4"]]
    cty = pd.read_csv(CACHE / "cdtfa_county_annual.csv")
    lac = cty[(cty["county"] == "LOS ANGELES") & (cty["group"] == "C08") & (cty["quarters"] == 4)][["year", "taxable", "permits_q4"]]
    out = la.merge(lac, on="year", suffixes=("_la_city", "_la_county"))
    out.to_csv(DERIVED / "la_city_c08_sales.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    main()
