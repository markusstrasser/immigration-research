"""Black-share and Hispanic-share coefficients in the guard_labor_2026_09_16 state regressions.

Reads that lane's panel.csv unchanged and repeats its OLS specification (classical SEs,
controls = log median HH income, poverty, urban share, Black share, 2019 violent crime rate).
Reports the coefficient on the Black-share control, plus variants that drop the crime
control (crime is the channel this lane prices, so controlling for it removes the channel)
and that drop the casino/tourism/capital outliers (NV, HI, DC).
"""
from pathlib import Path

import pandas as pd
import statsmodels.api as sm

LANE = Path(__file__).resolve().parent
PANEL = LANE.parent / "guard_labor_2026_09_16" / "panel.csv"
OUT = LANE / "derived" / "guard_share_coefficients.csv"

BASE = ["log_medinc", "poverty", "urban"]


def fit(d, y, xs):
    m = sm.OLS(d[y], sm.add_constant(d[xs])).fit()
    return m


def main():
    d = pd.read_csv(PANEL, dtype={"state": str})
    rows = []
    specs = {
        "lane spec: fb + base + black + crime": ["fb_share"] + BASE + ["black_share", "crime"],
        "lane spec: hisp + base + black + crime": ["hisp_share"] + BASE + ["black_share", "crime"],
        "black + base + crime (no fb)": ["black_share"] + BASE + ["crime"],
        "black + base, no crime control": ["black_share"] + BASE,
        "black + fb + base, no crime control": ["black_share", "fb_share"] + BASE,
        "hisp + base, no crime control": ["hisp_share"] + BASE,
        "black bivariate": ["black_share"],
        "hisp bivariate": ["hisp_share"],
    }
    samples = {
        "all 51": d,
        "drop NV HI DC": d[~d["NAME"].isin(["Nevada", "Hawaii", "District of Columbia"])],
    }
    for sname, sd in samples.items():
        sd = sd.reset_index(drop=True)
        for label, xs in specs.items():
            m = fit(sd, "guard_share", xs)
            for term in ("black_share", "hisp_share", "fb_share"):
                if term in xs:
                    rows.append({
                        "sample": sname, "spec": label, "term": term,
                        "b_pp_per_pp": m.params[term], "se": m.bse[term],
                        "p": m.pvalues[term], "r2": m.rsquared, "n": int(m.nobs),
                    })
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False, lineterminator="\n", float_format="%.6f")
    # Check: the lane reports fb_share b=0.0196 (0.0070) with controls, all 51.
    chk = out[(out["sample"] == "all 51") & (out["spec"] == "lane spec: fb + base + black + crime")
              & (out["term"] == "fb_share")].iloc[0]
    print(f"replication check fb_share: b={chk.b_pp_per_pp:.4f} se={chk.se:.4f} (lane: 0.0196, 0.0070)")
    print(out.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    # Descriptive national anchors from the panel (population-weighted)
    w = d["pop"]
    print("\npop-weighted guard share (% of employed):", round((d["guard_share"] * w).sum() / w.sum(), 4))
    print("pop-weighted black share (%):", round((d["black_share"] * w).sum() / w.sum(), 3))
    print("pop-weighted hisp share (%):", round((d["hisp_share"] * w).sum() / w.sum(), 3))
    print("total employed:", int(d["employed"].sum()), " PUMS guards (OCCP 3930):", int(d["guards"].sum()))


if __name__ == "__main__":
    main()
