#!/usr/bin/env python3
"""Arm 1 step 4: does county Mexican-origin share move the Democratic two-party
share and turnout?  Every outcome and regressor is in percentage points, so a
coefficient reads "points of outcome per point of Mexican-origin population share".

Specifications (the last four exist to reverse the headline, and are reported
whether or not they do):
  S1  two-way FE: county + state x year, population weighted, SE clustered by state
  S2  same with national year FE instead of state x year (shows what states absorb)
  S3  long difference 2000 -> 2024, state FE, weighted by 2000 population
  S4  shift-share IV: 2000 settlement share x national Mexican-origin growth
  S5  drop the four border states AZ, CA, NM, TX
  S6  2016-2024 only (the years the Hispanic vote moved right)
  S7  placebo: 2000->2008 change in vote on the 2008->2024 change in composition
  S8  horse race against the non-Mexican Hispanic share
  T1  turnout on citizen voting-age population, 2008-2024, county + state x year
  R   the Rio Grande Valley counties by name, 2020 -> 2024

Output: derived/regressions.csv, derived/regressions.txt, derived/rgv_swing.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fe import absorb, tsls_cluster, wls_cluster  # noqa: E402

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"
BORDER = {"04", "06", "35", "48"}
ROWS: list[dict] = []
TXT: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    TXT.append(s)


def report(name: str, desc: str, res: dict, term: str, extra: str = "") -> None:
    b, se, t = res["beta"][0] * 1.0, res["se"][0], res["t"][0]
    lo, hi = b - 1.96 * se, b + 1.96 * se
    ROWS.append({"spec": name, "description": desc, "term": term,
                 "coef": b, "se": se, "t": t, "ci_lo": lo, "ci_hi": hi,
                 "n": res["n"], "clusters": res["clusters"], "note": extra})
    say(f"{name:14s} {term:28s} b={b:+.4f}  se={se:.4f}  t={t:+.2f}  "
        f"95% CI [{lo:+.4f}, {hi:+.4f}]  n={res['n']:,} clusters={res['clusters']}"
        + (f"  {extra}" if extra else ""))


def panel_fe(df: pd.DataFrame, yvar: str, xvars: list[str], fes: list[str],
             name: str, desc: str, absorbed: int) -> dict:
    d = df.dropna(subset=[yvar] + xvars + fes + ["pop"]).copy()
    w = d["pop"].to_numpy(dtype=float)
    dm = absorb(d, [yvar] + xvars, fes, w)
    res = wls_cluster(dm[yvar].to_numpy(), dm[xvars].to_numpy(), w,
                      d["state"].to_numpy(), absorbed=absorbed)
    report(name, desc, res, xvars[0])
    for j, xv in enumerate(xvars[1:], start=1):
        say(f"{'':14s} {xv:28s} b={res['beta'][j]:+.4f}  se={res['se'][j]:.4f}  "
            f"t={res['t'][j]:+.2f}")
        ROWS.append({"spec": name, "description": desc, "term": xv,
                     "coef": res["beta"][j], "se": res["se"][j], "t": res["t"][j],
                     "ci_lo": res["beta"][j] - 1.96 * res["se"][j],
                     "ci_hi": res["beta"][j] + 1.96 * res["se"][j],
                     "n": res["n"], "clusters": res["clusters"], "note": "covariate"})
    return res


def main() -> int:
    p = pd.read_csv(DER / "county_panel.csv", dtype={"fips": str, "state": str})
    p["dem2p_pp"] = p.dem2p * 100
    p["mex_pp"] = p.mex_share * 100
    p["hisp_pp"] = p.hisp_share * 100
    p["nonmex_hisp_pp"] = (p.hisp_share - p.mex_share) * 100
    p["turnout_pp"] = p.turnout_cvap * 100
    p["state_year"] = p.state + "_" + p.year.astype(str)
    say(f"panel: {p.fips.nunique():,} counties x {p.year.nunique()} years = "
        f"{len(p):,} rows; outcomes and regressors in percentage points")
    say()

    say("=== presidential two-party Democratic share ===")
    nfe1 = p.fips.nunique() + p.state_year.nunique()
    panel_fe(p, "dem2p_pp", ["mex_pp"], ["fips", "state_year"], "S1",
             "county FE + state x year FE, pop weighted", nfe1)
    p["year_s"] = p.year.astype(str)
    panel_fe(p, "dem2p_pp", ["mex_pp"], ["fips", "year_s"], "S2",
             "county FE + national year FE", p.fips.nunique() + p.year.nunique())

    # S3 long difference 2000 -> 2024
    w0 = p[p.year == 2000].set_index("fips")
    w1 = p[p.year == 2024].set_index("fips")
    ld = pd.DataFrame({
        "d_dem2p": w1.dem2p_pp - w0.dem2p_pp,
        "d_mex": w1.mex_pp - w0.mex_pp,
        "mex0": w0.mex_pp, "pop": w0["pop"], "state": w0.state}).dropna()
    dm = absorb(ld, ["d_dem2p", "d_mex"], ["state"], ld["pop"].to_numpy(float))
    res = wls_cluster(dm.d_dem2p.to_numpy(), dm[["d_mex"]].to_numpy(),
                      ld["pop"].to_numpy(float), ld.state.to_numpy(),
                      absorbed=ld.state.nunique())
    report("S3", "long difference 2000-2024, state FE, weight pop2000", res, "d_mex")

    # S4 shift-share IV on the same long difference
    nat0 = p[p.year == 2000].mex.sum()
    nat1 = p[p.year == 2024].mex.sum()
    g = nat1 / nat0 - 1.0
    ld["z"] = ld.mex0 * g
    say(f"  [S4 instrument] national Mexican-origin growth 2000-2024 in-panel "
        f"= {g*100:.1f}%; z_i = mex_share_i,2000 x g")
    dmz = absorb(ld, ["d_dem2p", "d_mex", "z"], ["state"], ld["pop"].to_numpy(float))
    iv = tsls_cluster(dmz.d_dem2p.to_numpy(), dmz[["d_mex"]].to_numpy(),
                      dmz[["z"]].to_numpy(), ld["pop"].to_numpy(float),
                      ld.state.to_numpy(), absorbed=ld.state.nunique())
    ROWS.append({"spec": "S4", "description": "shift-share IV, long difference",
                 "term": "d_mex (instrumented)", "coef": iv["beta"][0],
                 "se": iv["se"][0], "t": iv["t"][0],
                 "ci_lo": iv["beta"][0] - 1.96 * iv["se"][0],
                 "ci_hi": iv["beta"][0] + 1.96 * iv["se"][0],
                 "n": iv["n"], "clusters": iv["clusters"],
                 "note": f"first stage b={iv['first_stage_beta']:.3f} "
                         f"se={iv['first_stage_se']:.3f} F={iv['first_stage_F']:.1f}"})
    say(f"{'S4':14s} {'d_mex (instrumented)':28s} b={iv['beta'][0]:+.4f}  "
        f"se={iv['se'][0]:.4f}  t={iv['t'][0]:+.2f}  n={iv['n']:,}  "
        f"first-stage F={iv['first_stage_F']:.1f}")

    # S5 drop border states
    panel_fe(p[~p.state.isin(BORDER)], "dem2p_pp", ["mex_pp"],
             ["fips", "state_year"], "S5", "S1 without AZ, CA, NM, TX",
             p[~p.state.isin(BORDER)].fips.nunique()
             + p[~p.state.isin(BORDER)].state_year.nunique())

    # S6 2016-2024 only
    late = p[p.year >= 2016]
    panel_fe(late, "dem2p_pp", ["mex_pp"], ["fips", "state_year"], "S6",
             "S1 on 2016, 2020, 2024 only",
             late.fips.nunique() + late.state_year.nunique())

    # S7 placebo / pre-trend
    w08 = p[p.year == 2008].set_index("fips")
    pl = pd.DataFrame({"d_dem_early": w08.dem2p_pp - w0.dem2p_pp,
                       "d_mex_late": w1.mex_pp - w08.mex_pp,
                       "pop": w0["pop"], "state": w0.state}).dropna()
    dmp = absorb(pl, ["d_dem_early", "d_mex_late"], ["state"],
                 pl["pop"].to_numpy(float))
    res = wls_cluster(dmp.d_dem_early.to_numpy(), dmp[["d_mex_late"]].to_numpy(),
                      pl["pop"].to_numpy(float), pl.state.to_numpy(),
                      absorbed=pl.state.nunique())
    report("S7", "PLACEBO: 2000-2008 vote change on 2008-2024 composition change",
           res, "d_mex_late")

    # S8 horse race with non-Mexican Hispanic share
    panel_fe(p, "dem2p_pp", ["mex_pp", "nonmex_hisp_pp"], ["fips", "state_year"],
             "S8", "S1 plus the non-Mexican Hispanic share", nfe1)

    # S9 single-source years only (MEDSL 2000-2016) - tests the vote-file splice
    early = p[p.year <= 2016]
    panel_fe(early, "dem2p_pp", ["mex_pp"], ["fips", "state_year"], "S9",
             "S1 on 2000-2016 only (one vote source, MEDSL)",
             early.fips.nunique() + early.state_year.nunique())

    # S10 total Hispanic share instead of Mexican origin
    panel_fe(p, "dem2p_pp", ["hisp_pp"], ["fips", "state_year"], "S10",
             "S1 with the total Hispanic share", nfe1)

    # how much within-county variation the FE design is actually using
    wcv = absorb(p, ["mex_pp"], ["fips", "state_year"], p["pop"].to_numpy(float))
    say(f"  [scale] raw sd(mex_pp)={p.mex_pp.std():.2f}pp; after county and "
        f"state x year FE the residual sd is {wcv.mex_pp.std():.2f}pp; "
        f"within-county 2000->2024 change: median "
        f"{(w1.mex_pp - w0.mex_pp).median():.2f}pp, p90 "
        f"{(w1.mex_pp - w0.mex_pp).quantile(.9):.2f}pp")

    say()
    say("=== turnout (total votes / citizen voting-age population), 2008-2024 ===")
    t = p[p.year >= 2008].dropna(subset=["turnout_pp"])
    panel_fe(t, "turnout_pp", ["mex_pp"], ["fips", "state_year"], "T1",
             "county FE + state x year FE, pop weighted",
             t.fips.nunique() + t.state_year.nunique())
    panel_fe(t, "turnout_pp", ["mex_pp"], ["fips", "year_s"], "T2",
             "county FE + national year FE",
             t.fips.nunique() + t.year.nunique())

    say()
    say("=== Rio Grande Valley and South Texas border counties, 2020 -> 2024 ===")
    rgv = {"48061": "Cameron", "48215": "Hidalgo", "48427": "Starr",
           "48489": "Willacy", "48479": "Webb", "48505": "Zapata",
           "48323": "Maverick", "48131": "Duval", "48247": "Jim Hogg",
           "48273": "Kleberg", "48355": "Nueces", "48465": "Val Verde"}
    r = p[p.fips.isin(rgv)].pivot(index="fips", columns="year",
                                  values=["dem2p_pp", "mex_pp", "total_votes"])
    out = pd.DataFrame({"county": [rgv[f] for f in r.index],
                        "mex_share_pp_2024": r[("mex_pp", 2024)].round(1),
                        "dem2p_2012": r[("dem2p_pp", 2012)].round(1),
                        "dem2p_2016": r[("dem2p_pp", 2016)].round(1),
                        "dem2p_2020": r[("dem2p_pp", 2020)].round(1),
                        "dem2p_2024": r[("dem2p_pp", 2024)].round(1)})
    out["swing_2020_2024"] = (out.dem2p_2024 - out.dem2p_2020).round(1)
    out["swing_2012_2024"] = (out.dem2p_2024 - out.dem2p_2012).round(1)
    out["votes_2024"] = r[("total_votes", 2024)].astype(int)
    out = out.sort_values("mex_share_pp_2024", ascending=False)
    say(out.to_string())
    vw = np.average(out.swing_2020_2024, weights=out.votes_2024)
    say(f"vote-weighted 2020->2024 swing across these counties: {vw:+.1f} points")
    out.to_csv(DER / "rgv_swing.csv")

    # national comparison: all counties over 50% Mexican origin
    maj = p[(p.year == 2024) & (p.mex_pp >= 50)].fips
    mm = p[p.fips.isin(maj)].pivot(index="fips", columns="year", values="dem2p_pp")
    tv = p[(p.year == 2024) & p.fips.isin(maj)].set_index("fips").total_votes
    say(f"all {len(maj)} counties at or above 50% Mexican origin in 2024: "
        f"vote-weighted Dem two-party share "
        f"{np.average(mm[2012], weights=tv):.1f} (2012) -> "
        f"{np.average(mm[2016], weights=tv):.1f} (2016) -> "
        f"{np.average(mm[2020], weights=tv):.1f} (2020) -> "
        f"{np.average(mm[2024], weights=tv):.1f} (2024)")

    pd.DataFrame(ROWS).to_csv(DER / "regressions.csv", index=False)
    (DER / "regressions.txt").write_text("\n".join(TXT) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
