"""Does the Hispanic/immigrant-share slope of white NAEP scores depend on how many Black pupils a state
already had? The operator's hypothesis (2026-09-28): harm to white pupils saturates, so where the Black
share was already high the added Hispanic share shows no further loss ("priced in"). It predicts a
negative slope in states that started with few Black pupils and a flatter one where the share was high,
i.e. a positive interaction of the share with the baseline Black share.

Reuses school_systemwide_2026_09_27's panel and estimator unchanged (22fd223): pooled four grade-subject
cells, scores in 2019 national SDs, cell-by-state and cell-by-year fixed effects, SEs clustered by state,
2003-2019. Baseline shares come from that lane's cached CCD race counts for fall 2002 (NAEP 2003).

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/naep_saturation_2026_09_28/saturation.py
"""
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LANE = HERE.parent / "school_systemwide_2026_09_27"
sys.path.insert(0, str(LANE))
from acquire_shares import FIPS  # noqa: E402
from panel import MAIN_YEARS, build  # noqa: E402
from stats_util import ols, t_quantile  # noqa: E402

TREAT = {"hisp": "hisp_share", "imm": "imm_origin_share_617", "el": "el_identified_pct_all"}
OUTCOMES = ["white", "white_nonel", "white_p10"]
BASE_FALL = 2002


def baseline_shares() -> dict[str, dict[str, float]]:
    rows = json.loads((LANE / "_cache" / "shares" / f"ccd_race_{BASE_FALL}.json").read_text())
    by: dict[str, dict[int, float]] = {}
    for x in rows:
        if x["fips"] in FIPS and x["enrollment"] is not None and x["enrollment"] >= 0:
            by.setdefault(FIPS[x["fips"]], {})[x["race"]] = x["enrollment"]
    out = {}
    for state, d in by.items():
        known = sum(v for k, v in d.items() if k in (1, 2, 3, 4, 5, 6, 7))
        if known > 0:
            out[state] = {"black": 100 * d.get(2, 0) / known, "white": 100 * d.get(1, 0) / known,
                          "hisp": 100 * d.get(3, 0) / known}
    return out


def stacked(p, outcome):
    d = p[p.year.isin(MAIN_YEARS)].copy()
    d["z"] = d[outcome] / d.sd2019
    d["cell_state"] = d.cell + "|" + d.state
    d["cell_year"] = d.cell + "|" + d.year.astype(str)
    d["region_cell_year"] = d.region + "|" + d.cell_year
    return d


def with_trends(d):
    """State-by-cell linear trends, as school_systemwide_2026_09_27's `twfe(trend=True)` builds them."""
    keys = sorted(d.cell_state.unique())
    tr = pd.DataFrame({"tr_" + k: np.where(d.cell_state == k, d.year - 2003, 0.0) for k in keys}, index=d.index)
    return pd.concat([d, tr], axis=1), ["tr_" + k for k in keys[1:]]


def main() -> None:
    p = build()
    base = baseline_shares()
    p = p[p.state.isin(base)].copy()
    p["black0"] = p.state.map(lambda s: base[s]["black"])
    p["nonwhite0"] = p.state.map(lambda s: 100 - base[s]["white"])
    states = sorted(p.state.unique())
    black0 = np.array([base[s]["black"] for s in states])
    median = float(np.median(black0))
    rows = []

    def add(spec, tkey, outcome, res, name, scale=10.0, note=""):
        r = res[name]
        q = t_quantile(0.975, r["dof"])
        b, se = scale * r["coef"], scale * r["se"]
        rows.append(dict(spec=spec, treatment=tkey, outcome=outcome, term=name, beta_per10=round(b, 4),
                         se=round(se, 4), ci95_lo=round(b - q * se, 4), ci95_hi=round(b + q * se, 4),
                         p=round(r["p"], 4), n_obs=r["n"], n_states=r["clusters"], note=note))

    for tkey, col in TREAT.items():
        for outcome in OUTCOMES:
            d = stacked(p, outcome).dropna(subset=["z", col])
            fe = ["cell_state", "cell_year"]
            res = ols(d, "z", [col], fe=fe, cluster="state")
            add("twfe", tkey, outcome, res, col, note="reproduces ladder 248's specification")
            for mod, cen in (("black0", 10.0), ("nonwhite0", 20.0)):
                d["inter"] = d[col] * (d[mod] - cen)
                res = ols(d, "z", [col, "inter"], fe=fe, cluster="state")
                add(f"x_{mod}", tkey, outcome, res, col, note=f"slope where {mod} = {cen:g}%")
                # interaction: change in the per-10-point slope per 10 points of baseline share
                add(f"x_{mod}", tkey, outcome, res, "inter", scale=100.0,
                    note=f"change in slope per 10 points of {mod}; saturation predicts > 0")
            for half, keep in (("low_black", d.black0 <= median), ("high_black", d.black0 > median)):
                res = ols(d[keep], "z", [col], fe=fe, cluster="state")
                add(f"split_{half}", tkey, outcome, res, col, note=f"black0 {'<=' if half == 'low_black' else '>'} "
                                                                  f"median {median:.1f}%")
            # the lane's two robustness designs, applied to the Black-share interaction
            d["inter"] = d[col] * (d["black0"] - 10.0)
            res = ols(d, "z", [col, "inter"], fe=["cell_state", "region_cell_year"], cluster="state")
            add("x_black0_region_year", tkey, outcome, res, col, note="slope where black0 = 10%, region-by-year FE")
            add("x_black0_region_year", tkey, outcome, res, "inter", scale=100.0,
                note="change in slope per 10 points of black0, region-by-year FE")
            dt, trends = with_trends(d)
            res = ols(dt, "z", [col, "inter"] + trends, fe=fe, cluster="state")
            add("x_black0_trends", tkey, outcome, res, col, note="slope where black0 = 10%, state-by-cell trends")
            add("x_black0_trends", tkey, outcome, res, "inter", scale=100.0,
                note="change in slope per 10 points of black0, state-by-cell trends")
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    with (out / "saturation_estimates.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    with (out / "baseline_shares.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["state", "black_share_fall2002", "white_share_fall2002", "hisp_share_fall2002"])
        for s in states:
            w.writerow([s, round(base[s]["black"], 3), round(base[s]["white"], 3), round(base[s]["hisp"], 3)])
    print(f"states {len(states)}; median fall-2002 Black share {median:.1f}%")
    for r in rows:
        if r["outcome"] == "white":
            print(f"{r['treatment']:5} {r['spec']:16} {r['term']:22} {r['beta_per10']:+.4f} ({r['se']:.4f}) "
                  f"[{r['ci95_lo']:+.3f}, {r['ci95_hi']:+.3f}] n_states {r['n_states']}  {r['note']}")


if __name__ == "__main__":
    main()
