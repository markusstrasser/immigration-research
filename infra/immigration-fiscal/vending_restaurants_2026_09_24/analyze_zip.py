"""Design (b): within Los Angeles County, ZIPs ordered by pre-2018 vending exposure.

outcome_zt = ZIP FE + year FE + sum_k b_k * X_z * 1[year = k], k != 2018, clustered by ZIP.
Exposures X (fixed before outcomes were seen):
  hisp_share, mexborn_share  ACS 2013-2017 ZCTA shares, per 10 percentage points;
  arrests                    log(1 + LAPD vending arrests 2010-2016) in ZCTAs at least half inside
                             the City of Los Angeles (the only direct pre-law vending measure).
Outcomes (ZIP Business Patterns, 2012-2023): establishments of 722511 full-service, 722513
limited-service, 722 all food services and drinking places, and 445110 grocery (placebo), as
log(establishments) on ZIPs present in all twelve years, as a Poisson count model (same ZIPs), and
as log of the size-class employment index. The index turned out invalid: from 2017 ZBP publishes a
size-class row only when it is not suppressed (2019: class counts sum to the total in 64 of 263 LA
full-service ZIPs), so it breaks between 2016 and 2017; its rows are kept and flagged. Mobile food (722330) is too sparse at ZIP level after the
2017 publication change (12-31 ZIPs a year) and is reported as counts only.
ZIPs with fewer than 1,000 residents are dropped (downtown business ZIPs have tiny denominators).

Gate: LA-ZIP establishment sums for 722511 and 722513 within 3% of the CBP county 06037 totals in
2012 and 2019.

A trend-adjusted sensitivity (exposure x linear trend from 2012-2018, post-2018 deviations) was added
after the pre-trend tests failed; it is labelled as such.

Writes derived/zip_event_coefs.csv, derived/zip_event_summary.csv, derived/zip_trend_adjusted.csv,
derived/zip_gate.json, derived/zip_722330_counts.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pyfixest python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/analyze_zip.py
"""
import csv
import json
import warnings

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats

from lib import CACHE, DERIVED

warnings.filterwarnings("ignore")
REF = 2018
YEARS = list(range(2012, 2024))
CODES = ["722511", "722513", "722", "445110"]


def la_city_zctas() -> set:
    out = set()
    with (CACHE / "zcta_place_rel_10.txt").open() as fh:
        for r in csv.DictReader(fh):
            if r["STATE"] == "06" and r["PLACE"] == "44000" and float(r["ZPOPPCT"]) >= 50:
                out.add(r["ZCTA5"])
    return out


def fit(d: pd.DataFrame, yvar: str, model: str) -> tuple[pd.DataFrame, float]:
    d = d.copy()
    names = []
    for k in YEARS:
        if k == REF:
            continue
        d[f"x{k}"] = d["x"] * (d["year"] == k)
        names.append(f"x{k}")
    fml = f"{yvar} ~ " + " + ".join(names) + " | zip + year"
    m = (pf.fepois if model == "poisson" else pf.feols)(fml, data=d, vcov={"CRV1": "zip"})
    b, se = m.coef(), m.se()
    co = pd.DataFrame({"year": [int(n[1:]) for n in names], "coef": b[names].values, "se": se[names].values})
    pre = [n for n in names if int(n[1:]) < REF]
    idx = [list(b.index).index(n) for n in pre]
    V = m._vcov
    W = float(b[pre].values @ np.linalg.pinv(V[np.ix_(idx, idx)]) @ b[pre].values)
    return co, float(1 - stats.chi2.cdf(W, len(pre)))


def fit_trend(d: pd.DataFrame, yvar: str, model: str) -> pd.DataFrame:
    """Trend-adjusted version: exposure x linear trend (identified from 2012-2018) plus exposure x year
    dummies for 2019-2023 only, so each post coefficient is the deviation from the extrapolated
    pre-2019 trend. Added after the pre-trend tests failed; reported as a sensitivity."""
    d = d.copy()
    d["xtrend"] = d["x"] * (d["year"] - REF)
    names = []
    for k in YEARS:
        if k > REF:
            d[f"x{k}"] = d["x"] * (d["year"] == k)
            names.append(f"x{k}")
    fml = f"{yvar} ~ xtrend + " + " + ".join(names) + " | zip + year"
    m = (pf.fepois if model == "poisson" else pf.feols)(fml, data=d, vcov={"CRV1": "zip"})
    b, se = m.coef(), m.se()
    return pd.DataFrame({"term": ["xtrend"] + names, "coef": b[["xtrend"] + names].values,
                         "se": se[["xtrend"] + names].values})


def main() -> None:
    z = pd.read_csv(CACHE / "zbp_la_panel.csv", dtype={"zip": str, "naics": str})
    ex = pd.read_csv(DERIVED / "exposure_zcta_ca.csv", dtype={"zcta": str}).set_index("zcta")
    arr = pd.read_csv(DERIVED / "lapd_vending_arrests_zcta.csv", dtype={"zcta": str}).set_index("zcta")
    city = la_city_zctas()
    cbp = pd.read_csv(CACHE / "cbp_county_panel.csv", dtype={"fips": str, "naics": str})
    gate = {}
    for code in ("722511", "722513"):
        for y in (2012, 2019):
            zs = int(z[(z["naics"] == code) & (z["year"] == y)]["estab"].sum())
            cs = int(cbp[(cbp["fips"] == "06037") & (cbp["naics"] == code) & (cbp["year"] == y)]["estab"].iloc[0])
            gate[f"{code}_{y}"] = {"la_zip_sum": zs, "cbp_county": cs, "pct": round(100 * (zs / cs - 1), 2)}
    (DERIVED / "zip_gate.json").write_text(json.dumps(gate, indent=1) + "\n")
    if any(abs(g["pct"]) > 3 for g in gate.values()):
        raise SystemExit(f"[FAILED] ZIP sums vs county totals: {gate}")
    print("  gate: " + "; ".join(f"{k} {v['pct']:+.2f}%" for k, v in gate.items()))

    coef_rows, summ_rows = [], []
    for code in CODES:
        d0 = z[z["naics"] == code].copy()
        n = d0.groupby("zip")["year"].nunique()
        d0 = d0[d0["zip"].isin(n[n == len(YEARS)].index) & (d0["estab"] > 0)]
        d0 = d0.join(ex[["pop", "hisp_share", "mexborn_share"]], on="zip")
        d0 = d0[d0["pop"] >= 1000]
        d0["ly"] = np.log(d0["estab"])
        d0["lemp"] = np.log(d0["emp_index"].clip(lower=1))
        for xname in ("hisp_share", "mexborn_share", "arrests"):
            d = d0.copy()
            if xname == "arrests":
                d = d[d["zip"].isin(city)]
                d["x"] = np.log1p(d["zip"].map(arr["arrests_2010_2016"]).fillna(0))
            else:
                d["x"] = d[xname] * 10
            d = d.dropna(subset=["x"])
            for yvar, model in (("ly", "ols"), ("estab", "poisson"), ("lemp", "ols")):
                co, p_pre = fit(d, yvar, model)
                c = co.set_index("year")
                tag = dict(naics=code, exposure=xname, outcome={"ly": "log_estab", "estab": "estab_poisson",
                                                                "lemp": "log_emp_index"}[yvar],
                           note=("invalid: from 2017 ZBP omits suppressed size classes, so the index breaks"
                                 if yvar == "lemp" else ""),
                           n_zips=d["zip"].nunique(), x_mean=round(float(d.drop_duplicates("zip")["x"].mean()), 4),
                           x_sd=round(float(d.drop_duplicates("zip")["x"].std()), 4))
                coef_rows += [{**tag, **r} for r in co.to_dict("records")]
                summ_rows.append({**tag, "b2019": c.loc[2019, "coef"], "se2019": c.loc[2019, "se"],
                                  "b2022_23": c.loc[[2022, 2023], "coef"].mean(),
                                  "se2022": c.loc[2022, "se"], "se2023": c.loc[2023, "se"],
                                  "b2020_21": c.loc[[2020, 2021], "coef"].mean(),
                                  "pre_max_abs": c.loc[c.index < REF, "coef"].abs().max(), "p_pretrend": p_pre})
                s = summ_rows[-1]
                print(f"  {code} {xname} {tag['outcome']}: {tag['n_zips']} ZIPs; b2019 {s['b2019']:+.4f} "
                      f"({s['se2019']:.4f}); b2022-23 {s['b2022_23']:+.4f}; pre-trend p {p_pre:.3f}", flush=True)
    pd.DataFrame(coef_rows).to_csv(DERIVED / "zip_event_coefs.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")
    trend_rows = []
    for code in CODES:
        d0 = z[z["naics"] == code].copy()
        n = d0.groupby("zip")["year"].nunique()
        d0 = d0[d0["zip"].isin(n[n == len(YEARS)].index) & (d0["estab"] > 0)]
        d0 = d0.join(ex[["pop", "hisp_share", "mexborn_share"]], on="zip")
        d0 = d0[d0["pop"] >= 1000]
        d0["ly"] = np.log(d0["estab"])
        for xname in ("hisp_share", "mexborn_share", "arrests"):
            d = d0.copy()
            if xname == "arrests":
                d = d[d["zip"].isin(city)]
                d["x"] = np.log1p(d["zip"].map(arr["arrests_2010_2016"]).fillna(0))
            else:
                d["x"] = d[xname] * 10
            d = d.dropna(subset=["x"])
            for yvar, model in (("ly", "ols"), ("estab", "poisson")):
                t = fit_trend(d, yvar, model).set_index("term")
                trend_rows.append({"naics": code, "exposure": xname,
                                   "outcome": "log_estab" if yvar == "ly" else "estab_poisson",
                                   "n_zips": d["zip"].nunique(), "pre_trend_per_year": t.loc["xtrend", "coef"],
                                   "pre_trend_se": t.loc["xtrend", "se"], "dev2019": t.loc["x2019", "coef"],
                                   "dev2019_se": t.loc["x2019", "se"],
                                   "dev2022_23": (t.loc["x2022", "coef"] + t.loc["x2023", "coef"]) / 2,
                                   "dev2022_se": t.loc["x2022", "se"], "dev2023_se": t.loc["x2023", "se"]})
                r = trend_rows[-1]
                print(f"  trend-adjusted {code} {xname} {r['outcome']}: trend {r['pre_trend_per_year']:+.4f}/yr; "
                      f"dev2019 {r['dev2019']:+.4f} ({r['dev2019_se']:.4f}); dev2022-23 {r['dev2022_23']:+.4f}",
                      flush=True)
    pd.DataFrame(trend_rows).to_csv(DERIVED / "zip_trend_adjusted.csv", index=False, lineterminator="\n",
                                    float_format="%.6g")
    pd.DataFrame(summ_rows).to_csv(DERIVED / "zip_event_summary.csv", index=False, lineterminator="\n",
                                   float_format="%.6g")
    mf = z[z["naics"] == "722330"].groupby("year").agg(zips=("zip", "nunique"), estab=("estab", "sum"))
    mf.to_csv(DERIVED / "zip_722330_counts.csv", lineterminator="\n")


if __name__ == "__main__":
    main()
