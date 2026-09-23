"""What the Mexico component of Z2 measures: the ancestry file's Mexico rows against where
Mexican immigrants actually were and went.

Z2_mex (the ancestry lane's) sums the file's PushPull_10 over a CBSA's counties for Mexico only.
The file builds each origin's push-pull term from the origin's national outflow and the
destination's pull from other origins (ancestry lane RESULT.md, "What the instrument is"), so the
Mexico term follows where non-Mexican immigrants settle. The file's Ancestry column (predicted
2010 ancestry) is set beside it. Each is scaled per 100 people of 2000 population and compared,
by population-weighted R^2 across the FG metros, with the Mexico-born share of employment in 2000
and its 2000-2010 change (derived/pums_metro.csv).

Writes derived/mexico_component_check.csv (the comparisons) and
derived/mexico_component_top_metros.csv (the 15 metros with the largest Z2_mex).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
    python3 infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/check_mexico_component.py
"""
import numpy as np
import pandas as pd

from common import ANC, DERIVED, HERE, sample_fg, wls

DTA = (HERE.parents[2] / "sources/immigration-fiscal/data/external/stage3/immigrationshock/"
       "ancestry-instruments/AncestryInstrument_County.dta")
XW = HERE.parent / "hedonic_composition_2026_09_19" / "derived" / "geo_county_cbsa_2013.csv"


def mexico_by_cbsa() -> pd.DataFrame:
    d = pd.read_stata(DTA, convert_categoricals=False, columns=["CountyCode", "CountryName", "PushPull_10",
                                                                "PushPull_9", "Ancestry"])
    d["county_fips"] = (d.CountyCode / 10).round().astype(int).astype(str).str.zfill(5)
    d = d[d.CountryName.astype(str).str.strip().str.lower().eq("mexico")]
    xw = pd.read_csv(XW, dtype={"county_fips": str, "cbsa": str})
    g = d.merge(xw[["county_fips", "cbsa"]], on="county_fips", how="inner").groupby("cbsa")
    out = (g[["PushPull_10", "PushPull_9", "Ancestry"]].sum() * 1000.0).reset_index()
    # positive control: the Mexico PushPull_10 sum reproduces the ancestry lane's pred_2000s_mex
    ref = pd.read_csv(ANC / "derived" / "cbsa_predicted_inflow.csv", dtype={"cbsa": str})
    j = out.merge(ref[["cbsa", "pred_2000s_mex"]], on="cbsa", how="inner")
    gap = float((j.PushPull_10 - j.pred_2000s_mex).abs().max())
    if gap > 1e-6:
        raise SystemExit(f"[BLOCKED] Mexico PushPull_10 does not reproduce pred_2000s_mex (max gap {gap})")
    return out


def main():
    p = pd.read_csv(DERIVED / "pums_metro.csv", dtype={"cbsa": str})
    s0 = p[p["sample"] == 200001].set_index("cbsa")
    s1 = p[p["sample"] == 201001].set_index("cbsa")
    mex = pd.DataFrame({"mexemp_0": 100 * s0.emp_mex / s0.emp,
                        "d_mexemp": 100 * s1.emp_mex / s1.emp - 100 * s0.emp_mex / s0.emp,
                        "inflow_mex": 100 * (s1.emp_mex - s0.emp_mex) / s0.emp}).reset_index()
    m = sample_fg().merge(mexico_by_cbsa(), on="cbsa", how="left").merge(mex, on="cbsa", how="left")
    for c in ("PushPull_10", "PushPull_9", "Ancestry"):
        m[f"{c}_pc"] = 100.0 * m[c].fillna(0.0) / m["pop"]
    m = m.dropna(subset=["mexemp_0", "d_mexemp", "w"])
    rows = []
    for x, lab in (("PushPull_10_pc", "Z2_mex: Mexico PushPull_10 per 100 residents (the lane's instrument)"),
                   ("PushPull_9_pc", "Mexico PushPull_9 per 100 residents (1990s wave)"),
                   ("Ancestry_pc", "Mexico predicted 2010 ancestry per 100 residents (file's Ancestry column)")):
        for y, ylab in (("mexemp_0", "Mexico-born share of employment 2000, points"),
                        ("d_mexemp", "change in that share 2000-2010, points"),
                        ("inflow_mex", "Mexico-born employment growth 2000-2010 / 2000 employment, points")):
            r = wls(m[y], m[[x]], m.w)
            rows.append({"regressor": lab, "outcome": ylab, "n": len(m), "coef": r.params[x], "se": r.bse[x],
                         "weighted_r2": r.rsquared})
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "mexico_component_check.csv", index=False)
    top = m.sort_values("PushPull_10_pc", ascending=False).head(15)[
        ["cbsa", "cbsa_title", "pop", "PushPull_10_pc", "Ancestry_pc", "mexemp_0", "d_mexemp"]]
    top.to_csv(DERIVED / "mexico_component_top_metros.csv", index=False)
    with pd.option_context("display.width", 220, "display.max_colwidth", 80):
        print(out.round(4).to_string(index=False))
        print(top.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
