#!/usr/bin/env python3
"""Arm D step 5: does Mexican-cuisine variety scale with the Mexican-origin
share of a metro, or flatten?

Primary specification is a Poisson QMLE count model with an offset of log
population, which keeps the CBSAs that have zero tagged Mexican restaurants
instead of dropping them the way a log-OLS would:

    E[mexican_restaurants] = exp(a + b*log(mexican_share) + controls) * pop

b is the elasticity of Mexican restaurants per capita with respect to the
Mexican-origin population share. b = 1 means variety scales one-for-one with
group size (no saturation); b < 1 means each additional member of the group
adds less variety than the one before; b near 0 means variety is already there
at very low shares, which is the operator's hypothesis.

A quadratic in log(share) tests curvature, and decile means show where the
curve flattens. Placebos: all restaurants and other ethnic cuisines, which
should not load on the Mexican-origin share.

Input : derived/cbsa_restaurant_panel.csv
Output: derived/arm_d_elasticity.csv, derived/arm_d_share_deciles.csv
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"

REGION = {
    "CT": "NE", "ME": "NE", "MA": "NE", "NH": "NE", "RI": "NE", "VT": "NE",
    "NJ": "NE", "NY": "NE", "PA": "NE",
    "IL": "MW", "IN": "MW", "MI": "MW", "OH": "MW", "WI": "MW", "IA": "MW",
    "KS": "MW", "MN": "MW", "MO": "MW", "NE": "MW", "ND": "MW", "SD": "MW",
    "DE": "S", "DC": "S", "FL": "S", "GA": "S", "MD": "S", "NC": "S",
    "SC": "S", "VA": "S", "WV": "S", "AL": "S", "KY": "S", "MS": "S",
    "TN": "S", "AR": "S", "LA": "S", "OK": "S", "TX": "S",
    "AZ": "W", "CO": "W", "ID": "W", "MT": "W", "NV": "W", "NM": "W",
    "UT": "W", "WY": "W", "AK": "W", "CA": "W", "HI": "W", "OR": "W",
    "WA": "W", "PR": "PR",
}
CUISINES = ["mexican", "chinese", "italian", "indian", "thai", "japanese",
            "vietnamese", "korean", "american"]


def prep() -> pd.DataFrame:
    df = pd.read_csv(DER / "cbsa_restaurant_panel.csv", dtype={"cbsa": str})
    df["state1"] = df["NAME"].apply(
        lambda s: re.search(r",\s*([A-Z]{2})", str(s)).group(1)
        if re.search(r",\s*([A-Z]{2})", str(s)) else "")
    df["region"] = df["state1"].map(REGION).fillna("other")
    df = df[(df["pop_b03001"] > 0) & (df["median_hh_income"] > 0)].copy()
    df["mexican_share"] = df["mexican_origin"] / df["pop_b03001"]
    # a CBSA with literally zero Mexican-origin residents cannot enter a log
    # specification; there are few, and they are reported not silently dropped
    df["log_share"] = np.log(df["mexican_share"].clip(lower=1e-5))
    df["log_pop"] = np.log(df["pop_b03001"])
    df["log_inc"] = np.log(df["median_hh_income"])
    df["mex_per_100k"] = df["mexican"] / df["pop_b03001"] * 1e5
    df["all_per_100k"] = df["all"] / df["pop_b03001"] * 1e5
    return df


def poisson(df: pd.DataFrame, dep: str, quad: bool, label: str,
            offset_col: str = "pop_b03001") -> dict:
    """offset_col = pop_b03001 gives restaurants per capita; offset_col =
    tagged gives the Mexican share of cuisine-tagged restaurants, which is
    immune to a metro simply having more OSM contributors."""
    X = pd.DataFrame({
        "log_share": df["log_share"],
        "log_pop": df["log_pop"],
        "log_inc": df["log_inc"],
    })
    if quad:
        X["log_share_sq"] = df["log_share"] ** 2
    for r in sorted(df["region"].unique())[1:]:
        X[f"region_{r}"] = (df["region"] == r).astype(float)
    X = sm.add_constant(X)
    sub = df[df[offset_col] > 0]
    X = X.loc[sub.index]
    # drop dummies that are constant inside this subset, then check rank:
    # a rank-deficient fit returns parameters that are not identified and
    # statsmodels only warns about it
    dropped = [c for c in X.columns
               if c != "const" and X[c].nunique() <= 1]
    X = X.drop(columns=dropped)
    if np.linalg.matrix_rank(X.values) < X.shape[1]:
        keep, cur = [], np.empty((len(X), 0))
        for c in X.columns:
            trial = np.column_stack([cur, X[c].values])
            if np.linalg.matrix_rank(trial) > cur.shape[1]:
                keep.append(c)
                cur = trial
            else:
                dropped.append(c)
        X = X[keep]
    model = sm.GLM(sub[dep], X, family=sm.families.Poisson(),
                   offset=np.log(sub[offset_col]))
    res = model.fit(cov_type="HC1")
    out = {"spec": label, "dep": dep, "offset": offset_col, "n": int(res.nobs),
           "quadratic": quad,
           "elasticity_log_share": float(res.params["log_share"]),
           "se": float(res.bse["log_share"]),
           "z_vs_zero": float(res.params["log_share"] / res.bse["log_share"]),
           "z_vs_one": float((res.params["log_share"] - 1) / res.bse["log_share"]),
           "log_pop_coef": float(res.params["log_pop"]),
           "log_inc_coef": float(res.params["log_inc"]),
           "dep_total": float(sub[dep].sum()),
           "dep_zero_cbsas": int((sub[dep] == 0).sum()),
           "dropped_collinear": "|".join(dropped)}
    if quad:
        out["quad_coef"] = float(res.params["log_share_sq"])
        out["quad_se"] = float(res.bse["log_share_sq"])
        out["quad_z"] = float(res.params["log_share_sq"]
                              / res.bse["log_share_sq"])
    return out


def prediction_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Predicted Mexican restaurants per 100,000 residents across a grid of
    Mexican-origin shares, holding population, income and region at the sample
    mean. This is the direct answer to "where does variety stop growing".
    """
    X = pd.DataFrame({
        "log_share": df["log_share"],
        "log_pop": df["log_pop"],
        "log_inc": df["log_inc"],
    })
    X["log_share_sq"] = df["log_share"] ** 2
    for r in sorted(df["region"].unique())[1:]:
        X[f"region_{r}"] = (df["region"] == r).astype(float)
    X = sm.add_constant(X)
    res = sm.GLM(df["mexican"], X, family=sm.families.Poisson(),
                 offset=np.log(df["pop_b03001"])).fit(cov_type="HC1")
    grid = [0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.35, 0.50]
    base = X.mean()
    rows = []
    for g in grid:
        x = base.copy()
        x["log_share"] = np.log(g)
        x["log_share_sq"] = np.log(g) ** 2
        mu = float(np.exp(np.dot(x.values, res.params.values)))
        rows.append({"mexican_share": g,
                     "pred_mex_per_100k": round(mu * 1e5, 3)})
    out = pd.DataFrame(rows)
    out["pct_of_value_at_50pct"] = (
        out["pred_mex_per_100k"] / out["pred_mex_per_100k"].iloc[-1]).round(4)
    return out


def main() -> None:
    df = prep()
    metro = df[df["NAME"].str.contains("Metro Area", na=False)]
    complete = df[df.get("all_states_fetched", True) == True]  # noqa: E712
    rows = []
    specs = [("all_cbsas", df), ("metro_only", metro)]
    # tiny micropolitan areas carry 1-5 tagged restaurants each; this spec
    # checks the flatness is not a small-count artefact
    big = complete[complete["pop_b03001"] >= 250_000]
    if len(big) >= 60:
        specs.append(("pop_250k_plus", big))
    if len(complete) < len(df):
        # insurance while the OSM sweep is incomplete: CBSAs whose every state
        # has been fetched give an unbiased estimate on a smaller sample
        specs.append(("complete_states_only", complete))
    for label, sub in specs:
        rows.append(poisson(sub, "mexican", False, label))
        rows.append(poisson(sub, "mexican", True, label))
        # independent classifier: restaurant NAME rather than cuisine tag
        rows.append(poisson(sub, "mexican_by_name", False,
                            f"{label}_name_classifier"))
        rows.append(poisson(sub, "mexican_by_name", True,
                            f"{label}_name_classifier"))
        rows.append(poisson(sub, "mexican", False, f"{label}_tagged_offset",
                            offset_col="tagged"))
        rows.append(poisson(sub, "mexican", True, f"{label}_tagged_offset",
                            offset_col="tagged"))
        for placebo in ["all", "chinese", "italian", "indian", "american"]:
            rows.append(poisson(sub, placebo, False, f"{label}_placebo"))
    out = pd.DataFrame(rows).round(5)
    out.to_csv(DER / "arm_d_elasticity.csv", index=False)

    # decile profile and predicted-density profile are built on the CBSAs
    # whose every state has been fetched: a partially fetched state would
    # otherwise show up as a metro with artificially few restaurants
    d = complete.copy()
    d["decile"] = pd.qcut(d["mexican_share"], 10, labels=False,
                          duplicates="drop")
    prof = d.groupby("decile").apply(lambda g: pd.Series({
        "n_cbsa": len(g),
        "mexican_share_mean": g["mexican_share"].mean(),
        "mexican_share_min": g["mexican_share"].min(),
        "mexican_share_max": g["mexican_share"].max(),
        "pop_total": g["pop_b03001"].sum(),
        "mex_rest_total": g["mexican"].sum(),
        "mex_per_100k_pooled": g["mexican"].sum() / g["pop_b03001"].sum() * 1e5,
        "all_per_100k_pooled": g["all"].sum() / g["pop_b03001"].sum() * 1e5,
        "mex_share_of_tagged": (g["mexican"].sum()
                                / max(1, g["tagged"].sum())),
        "cbsas_with_any_mexican": (g["mexican"] > 0).mean(),
        "mex_per_100k_median": g["mex_per_100k"].median(),
    }), include_groups=False).reset_index().round(6)
    prof.to_csv(DER / "arm_d_share_deciles.csv", index=False)
    pred = prediction_profile(complete)
    pred.to_csv(DER / "arm_d_predicted_density.csv", index=False)
    print("\npredicted Mexican restaurants per 100k by share "
          "(quadratic fit, other covariates at the mean):", flush=True)
    print(pred.to_string(index=False), flush=True)

    print(out[["spec", "dep", "offset", "n", "quadratic",
               "elasticity_log_share", "se",
               "z_vs_one", "dep_zero_cbsas"]].to_string(index=False), flush=True)
    print("\ndecile profile:", flush=True)
    print(prof[["decile", "n_cbsa", "mexican_share_mean", "mex_per_100k_pooled",
                "all_per_100k_pooled", "mex_share_of_tagged",
                "cbsas_with_any_mexican"]].to_string(index=False), flush=True)
    primary = [r for r in rows
               if r["spec"] == ("complete_states_only" if len(complete) < len(df)
                                else "all_cbsas")
               and r["dep"] == "mexican" and not r["quadratic"]][0]
    summary = {
        "primary_spec": primary["spec"],
        "primary_elasticity": primary["elasticity_log_share"],
        "primary_se": primary["se"],
        "primary_n_cbsa": primary["n"],
        "cbsas_fully_covered": int(len(complete)),
        "cbsas_total": int(len(df)),
        "all_cbsas_elasticity": rows[0]["elasticity_log_share"],
        "all_cbsas_se": rows[0]["se"],
        "interpretation": (
            "b<1 means Mexican-cuisine variety per capita grows less than "
            "proportionally with the Mexican-origin share"),
    }
    (DER / "arm_d_summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
