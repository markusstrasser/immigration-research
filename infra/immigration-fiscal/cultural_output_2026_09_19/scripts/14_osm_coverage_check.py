#!/usr/bin/env python3
"""Arm D bias check: is OpenStreetMap coverage related to the Mexican-origin
share of a metro?

OSM is volunteered data. If metros with more Mexican-origin residents are
mapped more (or less) completely, the elasticity in script 11 is contaminated.
County Business Patterns is an administrative census of establishments, so
OSM restaurants / CBP establishments is a coverage ratio that does not depend
on OSM itself.

Pulls CBP 2023 establishment counts for NAICS 722511 (full-service) and 722513
(limited-service) by CBSA, joins the OSM panel, and regresses log coverage on
log Mexican-origin share. A coefficient near zero means the arm D elasticity is
not an artefact of differential mapping.

Output: derived/arm_d_osm_coverage_check.csv, derived/arm_d_coverage_fit.json
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "cbp"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)

GEO = "metropolitan statistical area/micropolitan statistical area"
NAICS = {"722511": "full_service", "722513": "limited_service"}


def fetch_cbp(key: str) -> pd.DataFrame:
    p = CACHE / "cbp_2023_restaurants_cbsa.csv"
    if p.exists():
        return pd.read_csv(p, dtype={"cbsa": str})
    frames = []
    for code, label in NAICS.items():
        try:
            r = requests.get("https://api.census.gov/data/2023/cbp",
                             params={"get": "ESTAB", "for": f"{GEO}:*",
                                     "NAICS2017": code, "key": key},
                             timeout=300)
            r.raise_for_status()
        except requests.HTTPError as exc:
            sys.exit(f"FAIL CBP request status "
                     f"{exc.response.status_code if exc.response else '?'}")
        if not r.text.lstrip().startswith("["):
            sys.exit("FAIL CBP returned a non-JSON body")
        rows = r.json()
        df = pd.DataFrame(rows[1:], columns=rows[0])
        df = df.rename(columns={GEO: "cbsa"})
        df["ESTAB"] = pd.to_numeric(df["ESTAB"], errors="coerce")
        df = df[["cbsa", "ESTAB"]].rename(columns={"ESTAB": label})
        if len(df) < 800:
            sys.exit(f"FAIL CBP {code}: only {len(df)} CBSA rows")
        frames.append(df.groupby("cbsa", as_index=False).sum())
    out = frames[0].merge(frames[1], on="cbsa", how="outer").fillna(0)
    out["cbp_restaurants"] = out["full_service"] + out["limited_service"]
    out["cbsa"] = out["cbsa"].astype(str).str.zfill(5)
    out.to_csv(p, index=False)
    print(f"CBP CBSAs={len(out)} total establishments="
          f"{out['cbp_restaurants'].sum():,.0f}", flush=True)
    return out


def main() -> None:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("CENSUS_API_KEY not set; source config.local.env")
    cbp = fetch_cbp(key)
    panel = pd.read_csv(DER / "cbsa_restaurant_panel.csv", dtype={"cbsa": str})
    panel["cbsa"] = panel["cbsa"].str.zfill(5)
    d = panel.merge(cbp, on="cbsa", how="left")
    if "all_states_fetched" in d.columns:
        d = d[d["all_states_fetched"]]
    d = d[(d["cbp_restaurants"] > 0) & (d["pop_b03001"] > 0)
          & (d["all"] > 0) & (d["median_hh_income"] > 0)].copy()
    d["osm_coverage"] = d["all"] / d["cbp_restaurants"]
    d["tagged_coverage"] = d["tagged"] / d["cbp_restaurants"]
    d["mexican_share"] = d["mexican_origin"] / d["pop_b03001"]
    d["log_share"] = np.log(d["mexican_share"].clip(lower=1e-5))

    fits = {}
    for dep in ("osm_coverage", "tagged_coverage"):
        X = sm.add_constant(pd.DataFrame({
            "log_share": d["log_share"],
            "log_pop": np.log(d["pop_b03001"]),
            "log_inc": np.log(d["median_hh_income"]),
        }))
        res = sm.OLS(np.log(d[dep].clip(lower=1e-4)), X).fit(cov_type="HC1")
        fits[dep] = {
            "n": int(res.nobs),
            "coef_log_share": round(float(res.params["log_share"]), 5),
            "se": round(float(res.bse["log_share"]), 5),
            "t": round(float(res.tvalues["log_share"]), 3),
            "mean_coverage": round(float(d[dep].mean()), 4),
            "median_coverage": round(float(d[dep].median()), 4),
        }
        print(f"{dep}: coef on log Mexican share "
              f"{fits[dep]['coef_log_share']} (SE {fits[dep]['se']}, "
              f"t {fits[dep]['t']}), median coverage "
              f"{fits[dep]['median_coverage']}", flush=True)

    d[["cbsa", "NAME", "pop_b03001", "mexican_share", "all", "tagged",
       "mexican", "cbp_restaurants", "osm_coverage", "tagged_coverage"]].round(
        6).to_csv(DER / "arm_d_osm_coverage_check.csv", index=False)
    (DER / "arm_d_coverage_fit.json").write_text(
        json.dumps(fits, indent=2) + "\n")


if __name__ == "__main__":
    main()
