"""Decompose Saiz elasticity into regulatory (WRLURI) vs topographic (unaval) channels.

The Saiz finding from the recent cycle (immigrants concentrate in inelastic MSAs)
could be driven by either:
- Topographic constraints (San Francisco's hills, Miami's water) — NOT policy-relevant
- Regulatory constraints (NIMBY zoning, growth controls) — POLICY-RELEVANT

If the immigrant-rent correlation operates through the regulatory channel,
zoning reform is a viable lever. If it operates through topography, immigration
restriction is the only lever (or nothing).
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path(__file__).parent.parent / "data"
SAIZ = DATA / "saiz" / "saiz_2010_msa_elasticity.dta"
MERGE = DATA / "analysis" / "saiz_msa_rent_immigrant_2022.parquet"
OUT = DATA / "analysis"


def main():
    saiz = pd.read_stata(SAIZ)
    merged = pd.read_parquet(MERGE)
    matched = merged[merged["NAME"].notna()].copy()
    print(f"Merged Saiz × ACS rows: {len(matched)}")

    # Saiz constructs elasticity = f(unaval, WRLURI). Decompose.
    # Higher unaval → less developable land → lower elasticity (more inelastic)
    # Higher WRLURI → tighter regulation → lower elasticity
    matched["unaval_q"] = pd.qcut(matched["unaval"], 4, labels=["U1 most-developable", "U2", "U3", "U4 least-developable"])
    matched["wrluri_q"] = pd.qcut(matched["WRLURI"], 4, labels=["W1 loosest-zoning", "W2", "W3", "W4 tightest-zoning"])

    print("\n=== FB share by topographic constraint quartile ===")
    print(matched.groupby("unaval_q", observed=True).agg(
        n=("NAME", "count"),
        median_unaval=("unaval", "median"),
        median_elasticity=("elasticity", "median"),
        median_rent=("median_rent", "median"),
        fb_share_pct=("fb_share", lambda x: x.median() * 100),
    ).to_string())

    print("\n=== FB share by regulatory constraint quartile ===")
    print(matched.groupby("wrluri_q", observed=True).agg(
        n=("NAME", "count"),
        median_wrluri=("WRLURI", "median"),
        median_elasticity=("elasticity", "median"),
        median_rent=("median_rent", "median"),
        fb_share_pct=("fb_share", lambda x: x.median() * 100),
    ).to_string())

    print("\n=== 2x2: Regulatory × Topographic ===")
    matched["unaval_lo_hi"] = pd.qcut(matched["unaval"], 2, labels=["lo_topo", "hi_topo"])
    matched["wrluri_lo_hi"] = pd.qcut(matched["WRLURI"], 2, labels=["lo_reg", "hi_reg"])
    cell = matched.groupby(["wrluri_lo_hi", "unaval_lo_hi"], observed=True).agg(
        n=("NAME", "count"),
        median_elasticity=("elasticity", "median"),
        median_rent=("median_rent", "median"),
        fb_share_pct=("fb_share", lambda x: x.median() * 100),
    )
    print(cell.to_string())

    # Regression: log_rent ~ unaval + WRLURI + log_pop + region FE — separates channels
    print("\n=== OLS: log(rent) ~ unaval + WRLURI + controls ===")
    sub = matched.dropna(subset=["median_rent", "unaval", "WRLURI", "population", "fb_share"]).copy()
    sub = sub[sub["median_rent"] > 0]
    sub["log_rent"] = np.log(sub["median_rent"])
    sub["log_pop"] = np.log(sub["population"])

    # Build design matrix
    X_cols = ["unaval", "WRLURI", "log_pop", "fb_share"]
    X = np.column_stack([np.ones(len(sub))] + [sub[c].values for c in X_cols])
    y = sub["log_rent"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sigma2 = (resid @ resid) / (len(y) - X.shape[1])
    XX_inv = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(sigma2 * XX_inv))
    t = beta / se

    names = ["intercept"] + X_cols
    print(f"  {'var':<15s}  {'beta':>10s}  {'SE':>10s}  {'t':>8s}")
    for n, b, s, ts in zip(names, beta, se, t):
        sig = "***" if abs(ts) > 2.58 else ("**" if abs(ts) > 1.96 else ("*" if abs(ts) > 1.645 else ""))
        print(f"  {n:<15s}  {b:+10.4f}  {s:10.4f}  {ts:+8.2f}{sig}")

    # Same regression with FB share as outcome
    print("\n=== OLS: log(FB share) ~ unaval + WRLURI + controls ===")
    sub2 = sub[sub["fb_share"] > 0].copy()
    sub2["log_fb"] = np.log(sub2["fb_share"])
    X2 = np.column_stack([np.ones(len(sub2))] + [sub2[c].values for c in ["unaval", "WRLURI", "log_pop"]])
    y2 = sub2["log_fb"].values
    beta2, *_ = np.linalg.lstsq(X2, y2, rcond=None)
    resid2 = y2 - X2 @ beta2
    sigma2_2 = (resid2 @ resid2) / (len(y2) - X2.shape[1])
    XX_inv2 = np.linalg.pinv(X2.T @ X2)
    se2 = np.sqrt(np.diag(sigma2_2 * XX_inv2))
    t2 = beta2 / se2

    names2 = ["intercept", "unaval", "WRLURI", "log_pop"]
    print(f"  {'var':<15s}  {'beta':>10s}  {'SE':>10s}  {'t':>8s}")
    for n, b, s, ts in zip(names2, beta2, se2, t2):
        sig = "***" if abs(ts) > 2.58 else ("**" if abs(ts) > 1.96 else ("*" if abs(ts) > 1.645 else ""))
        print(f"  {n:<15s}  {b:+10.4f}  {s:10.4f}  {ts:+8.2f}{sig}")

    # Save out
    matched.to_parquet(OUT / "saiz_decomposition.parquet", index=False)


if __name__ == "__main__":
    main()
