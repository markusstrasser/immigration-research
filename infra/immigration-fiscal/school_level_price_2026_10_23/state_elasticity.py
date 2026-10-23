#!/usr/bin/env python3
"""State-specific within-district school spending elasticity.

The scaling lane estimates one national response (1.004 across districts, 0.836
within). This script asks whether the within-district response differs by state:
log(current expenditures) on log(membership) with district fixed effects, run
separately for each state on the SLFS FY2022 x CCD 2021-22 school merge.

Output: derived/state_elasticity.csv. Small states are noisy; the top states by
group pupils are the usable cells.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"


def fit(g: pd.DataFrame, weighted: bool) -> dict | None:
    """Within-district slope by weighted demeaning (equivalent to district dummies)."""
    g = g.loc[g["member"].gt(0) & g["tcur"].gt(0)].copy()
    if len(g) < 30 or g["LEAID"].nunique() < 3:
        return None
    y = np.log(g["tcur"].to_numpy(float))
    x = np.log(g["member"].to_numpy(float))
    w = np.sqrt(g["member"].to_numpy(float)) if weighted else np.ones(len(g))
    frame = pd.DataFrame({"y": y, "x": x, "w": w, "lea": g["LEAID"].to_numpy()})
    def wmean(col: str) -> np.ndarray:
        return (
            (frame[col] * frame["w"]).groupby(frame["lea"]).transform("sum")
            / frame["w"].groupby(frame["lea"]).transform("sum")
        ).to_numpy()
    xw = (x - wmean("x")) * w
    yw = (y - wmean("y")) * w
    denom = float(xw @ xw)
    if denom <= 0:
        return None
    beta = float((xw @ yw) / denom)
    e = yw - beta * xw
    clusters = g["LEAID"].to_numpy()
    unique = np.unique(clusters)
    G = len(unique)
    scores = np.array([float(xw[clusters == c] @ e[clusters == c]) for c in unique])
    n = len(g)
    k = 1 + G  # slope + absorbed district intercepts
    V = (scores @ scores) / denom**2 * (G / (G - 1)) * ((n - 1) / (n - k))
    se = float(np.sqrt(V))
    return {
        "beta": beta,
        "se": se,
        "ci_low": beta - 1.96 * se,
        "ci_high": beta + 1.96 * se,
        "schools": int(n),
        "districts": int(G),
        "members": int(g["member"].sum()),
        "hispanic": int(g["hispanic"].sum()),
        "hispanic_share": float(g["hispanic"].sum() / g["member"].sum()),
    }


def main() -> None:
    df = pd.read_csv(CACHE / "school_merge.csv", dtype={"NCESSCH": str, "LEAID": str})
    rows = []
    for state, g in df.groupby("STABR"):
        for weighted, label in ((True, "pupil_weighted"), (False, "unweighted")):
            r = fit(g, weighted)
            if r is None:
                continue
            rows.append({"state": state, "weighting": label, **r})
    out = pd.DataFrame(rows).sort_values(["weighting", "hispanic"], ascending=[True, False])
    out.to_csv(OUT / "state_elasticity.csv", index=False)

    national = fit(df, True)
    pw = out.loc[out.weighting.eq("pupil_weighted")].copy()
    w = pw["hispanic"].clip(lower=0)
    summary = {
        "national_pupil_weighted_beta": national["beta"] if national else None,
        "national_se": national["se"] if national else None,
        "hispanic_weighted_state_beta": float((w * pw["beta"]).sum() / w.sum()),
        "states": int(len(pw)),
        "note": "within-district, district FE, SLFS FY2022; state cells are noisy for small states",
    }
    (OUT / "state_elasticity_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(pw.head(15).to_string(index=False))
    print(summary)


if __name__ == "__main__":
    main()
