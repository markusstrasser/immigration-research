"""Native wages against the 2000-2010 inflow, instrumented by the ancestry prediction.

Outcomes (derived/pums_metro.csv from build_pums.py; percent = 100 x log points)
  adj_week_<g>   composition-adjusted log weekly wage, natives 25-64, full-time full-year
  adj_hour_<g>   composition-adjusted log hourly wage, natives 25-64, all wage workers
  raw_week_<g>   the unadjusted mean log weekly wage
  rel_week       adj_week_noba - adj_week_ba (the relative wage of natives without a BA)
  groups g: noba (no BA), ba (BA+), hsl (high school or less), somecol (some college)
Treatments
  d_fbemp    change in the foreign-born share of employment 16-64, points (the brief's)
  d_mexemp   change in the Mexico-born share of employment, points
  inflow     Card's inflow rate: change in foreign-born employment / 2000 employment, points
  d_lnLH     change in log(employment 25-64 without a BA / with a BA), all nativities, percent;
             with rel_week as the outcome its IV coefficient is -1/sigma, the inverse
             elasticity of substitution between the two skill groups that the account calibrates
2010 endpoint: the ACS 2010 one-year sample (primary) and the ACS 2009-2011 three-year sample.
Samples: FG (fixed 2013 geography, all 100k+ metros), FG_noLA (the same without Los Angeles),
PC (the ancestry lane's 334 metros, treatment still from the microdata).

Writes derived/estimates_wages.csv and derived/wage_implications.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with scipy \
    python3 infra/immigration-fiscal/ancestry_iv_congestion_wages_2026_09_23/estimate_wages.py
"""
import json

import numpy as np
import pandas as pd

from common import DERIVED, HERE, gates, menu, sample_fg, sample_pc

SAMPLES = {"0": 200001, "1": 201001, "3": 201103}
ENDPOINT = {"1": "2010 ACS", "3": "2009-11 ACS"}
GROUPS = ("noba", "ba", "hsl", "somecol")
NEST = HERE.parent / "production_nativity_nest_2026_09_22" / "derived" / "branch_composition.csv"
WAGE = HERE.parent / "wage_distribution_2026_09_23" / "derived" / "wage_distribution_long_run_default.csv"


def metro_vars() -> pd.DataFrame:
    p = pd.read_csv(DERIVED / "pums_metro.csv", dtype={"cbsa": str})
    out = []
    for tag, samp in SAMPLES.items():
        s = p[p["sample"] == samp].set_index("cbsa")
        v = pd.DataFrame(index=s.index)
        for g in GROUPS:
            for kind in ("week", "hour"):
                v[f"adj_{kind}_{g}_{tag}"] = 100 * s[f"r_{kind}_{g}"] / s[f"n_{kind}_{g}"]
                v[f"raw_{kind}_{g}_{tag}"] = 100 * s[f"raw_{kind}_{g}"] / s[f"n_{kind}_{g}"]
                v[f"obs_{kind}_{g}_{tag}"] = s[f"obs_{kind}_{g}"]
        for kind in ("week", "hour"):
            v[f"rel_{kind}_{tag}"] = v[f"adj_{kind}_noba_{tag}"] - v[f"adj_{kind}_ba_{tag}"]
            v[f"relhs_{kind}_{tag}"] = v[f"adj_{kind}_hsl_{tag}"] - v[f"adj_{kind}_ba_{tag}"]
        v[f"fbemp_{tag}"] = 100 * s.emp_fb / s.emp
        v[f"mexemp_{tag}"] = 100 * s.emp_mex / s.emp
        v[f"lnLH_{tag}"] = 100 * np.log(s.emp2564_noba / s.emp2564_ba)
        v[f"lnLH_hrs_{tag}"] = 100 * np.log(s.hrs2564_noba / s.hrs2564_ba)
        v[f"lnLH_hsl_{tag}"] = 100 * np.log(s.emp2564_hsl / s.emp2564_ba)
        for c in ("emp", "emp_fb", "emp_mex", "emp2564_nat", "emp2564_noba", "emp2564_ba"):
            v[f"{c}_{tag}"] = s[c]
        v[f"pums_pop_{tag}"] = s["pop"]
        v[f"pcommute_all_{tag}"] = s.commute_min / s.commuters
        out.append(v)
    return pd.concat(out, axis=1).reset_index()


def changes(m: pd.DataFrame, e: str) -> pd.DataFrame:
    m = m.copy()
    for g in GROUPS:
        for kind in ("week", "hour"):
            for pre in ("adj", "raw"):
                m[f"d_{pre}_{kind}_{g}"] = m[f"{pre}_{kind}_{g}_{e}"] - m[f"{pre}_{kind}_{g}_0"]
    for kind in ("week", "hour"):
        m[f"d_rel_{kind}"] = m[f"rel_{kind}_{e}"] - m[f"rel_{kind}_0"]
        m[f"d_relhs_{kind}"] = m[f"relhs_{kind}_{e}"] - m[f"relhs_{kind}_0"]
    m["d_fbemp"] = m[f"fbemp_{e}"] - m.fbemp_0
    m["d_mexemp"] = m[f"mexemp_{e}"] - m.mexemp_0
    m["inflow"] = 100 * (m[f"emp_fb_{e}"] - m.emp_fb_0) / m.emp_0
    m["inflow_mex"] = 100 * (m[f"emp_mex_{e}"] - m.emp_mex_0) / m.emp_0
    m["d_lnLH"] = m[f"lnLH_{e}"] - m.lnLH_0
    m["d_lnLH_hrs"] = m[f"lnLH_hrs_{e}"] - m.lnLH_hrs_0
    m["d_lnLH_hsl"] = m[f"lnLH_hsl_{e}"] - m.lnLH_hsl_0
    m["d_ln_natemp"] = 100 * np.log(m[f"emp2564_nat_{e}"] / m.emp2564_nat_0)
    m["lnpop0"] = np.log(m["pop"])
    return m.replace([np.inf, -np.inf], np.nan)


def designs():
    fg = sample_fg()
    yield "FG", fg
    yield "FG_noLA", fg[fg.cbsa != "31080"]
    yield "PC", sample_pc()


def presence():
    """The Mexican-origin union's share of 2024 earners, from the CES account's own CPS branch
    file (positive earners, PEARNVAL proxy): the scale the calibration removes."""
    b = pd.read_csv(NEST)
    b = b[(b.proxy == "PEARNVAL")]
    out = {}
    for split in ("below_ba", "hs_or_less"):
        s = b[b.split == split]
        tot = s.positive_earners.sum()
        uni = s[s.branch.str.startswith("union")].positive_earners.sum()
        mex = s[s.branch == "union_mexico_born"].positive_earners.sum()
        fb = s[s.branch.isin(["union_mexico_born", "other_foreign_born"])].positive_earners.sum()
        low = s[s.skill == 0]
        hi = s[s.skill == 1]
        u_low = low[low.branch.str.startswith("union")].positive_earners.sum()
        u_hi = hi[hi.branch.str.startswith("union")].positive_earners.sum()
        dlnLH = 100 * (np.log(low.positive_earners.sum() / hi.positive_earners.sum())
                       - np.log((low.positive_earners.sum() - u_low) / (hi.positive_earners.sum() - u_hi)))
        nat_low_earn = low[low.branch == "native_non_union"].earnings_estimate.sum() / 1e9
        nat_hi_earn = hi[hi.branch == "native_non_union"].earnings_estimate.sum() / 1e9
        out[split] = dict(union_pp=100 * uni / tot, mexico_born_pp=100 * mex / tot, foreign_born_pp=100 * fb / tot,
                          union_dlnLH_pct=dlnLH, native_lower_earnings_bn=nat_low_earn,
                          native_upper_earnings_bn=nat_hi_earn)
    return out


def main():
    g = gates()
    print("gates passed:", {k: g[k] for k in ("n", "fs", "iv")})
    mv = metro_vars()
    rows = []
    for design, frame in designs():
        base_m = frame.merge(mv, on="cbsa", how="left")
        for e, elab in ENDPOINT.items():
            m = changes(base_m, e)
            b = {"design": design, "endpoint": elab}
            outcomes = ([f"adj_week_{g_}" for g_ in GROUPS] + [f"adj_hour_{g_}" for g_ in GROUPS]
                        + ["raw_week_noba", "raw_week_ba"])
            for oc in outcomes:
                for x in ("d_fbemp", "d_mexemp", "inflow"):
                    menu(rows, m, f"d_{oc}", x, {**b, "outcome": oc}, y0=f"{oc}_0",
                         placebo_extra=["lnpop0"])
            for oc in ("rel_week", "rel_hour", "relhs_week"):
                for x in ("d_fbemp", "d_mexemp", "d_lnLH", "d_lnLH_hrs", "d_lnLH_hsl"):
                    menu(rows, m, f"d_{oc}", x, {**b, "outcome": oc}, y0=f"{oc}_0")
            for oc in ("adj_week_noba", "adj_week_ba", "adj_week_hsl"):
                menu(rows, m, f"d_{oc}", "d_lnLH", {**b, "outcome": oc}, y0=f"{oc}_0")
            # the local labour-supply response behind the wage estimate
            for x in ("d_fbemp", "inflow"):
                menu(rows, m, "d_ln_natemp", x, {**b, "outcome": "native employment 25-64, log change"})
            for x in ("d_fbemp", "d_mexemp"):
                menu(rows, m, "d_lnLH", x, {**b, "outcome": "log(L/H) employment 25-64"})
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "estimates_wages.csv", index=False)

    # ---- implications against the CES calibration
    pres = presence()
    ces = pd.read_csv(WAGE)

    def pick(design, endpoint, outcome, x, estimator):
        r = est[(est.design == design) & (est.endpoint == endpoint) & (est.outcome == outcome)
                & (est.x == x) & (est.estimator == estimator)]
        return r.iloc[0].to_dict() if len(r) else None

    imp = {"presence": pres, "ces_calibration": ces.to_dict(orient="records"), "share_design": [], "sigma_design": []}
    for design in ("FG", "FG_noLA", "PC"):
        for endpoint in ENDPOINT.values():
            for oc, split in (("adj_week_noba", "below_ba"), ("adj_week_ba", "below_ba"),
                              ("adj_week_hsl", "hs_or_less"), ("adj_hour_noba", "below_ba"),
                              ("adj_hour_ba", "below_ba")):
                for x, scale_key in (("d_fbemp", "union_pp"), ("d_mexemp", "union_pp"), ("inflow", "union_pp")):
                    for estimator in ("OLS", "IV with Z2", "IV with Z2_exmex", "IV with Z2_mex", "IV with Z"):
                        r = pick(design, endpoint, oc, x, estimator)
                        if r is None:
                            continue
                        s = pres[split][scale_key]
                        per_pt = pres[split]["native_upper_earnings_bn" if oc.endswith("_ba") else
                                             "native_lower_earnings_bn"] / 100
                        imp["share_design"].append(dict(
                            design=design, endpoint=endpoint, outcome=oc, x=x, estimator=estimator,
                            beta=r["coef"], se=r["se"], ar_lo=r["ar_lo"], ar_hi=r["ar_hi"], ar_kind=r["ar_kind"],
                            scale_pp=s, implied_pct=r["coef"] * s, implied_lo=(r["coef"] - 1.96 * r["se"]) * s,
                            implied_hi=(r["coef"] + 1.96 * r["se"]) * s,
                            implied_bn=r["coef"] * s * per_pt, bn_per_pct=per_pt))
            for oc in ("rel_week", "rel_hour"):
                for x in ("d_lnLH", "d_lnLH_hrs"):
                    for estimator in ("OLS", "IV with Z2", "IV with Z2_exmex", "IV with Z2_mex", "IV with Z"):
                        r = pick(design, endpoint, oc, x, estimator)
                        if r is None:
                            continue
                        beta = r["coef"]  # percent relative wage per percent relative supply = -1/sigma
                        imp["sigma_design"].append(dict(
                            design=design, endpoint=endpoint, outcome=oc, x=x, estimator=estimator,
                            inv_sigma=-beta, se=r["se"], sigma=(-1 / beta) if beta < 0 else np.inf,
                            ar_lo=r["ar_lo"], ar_hi=r["ar_hi"], ar_kind=r["ar_kind"],
                            union_rel_wage_pct=beta * pres["below_ba"]["union_dlnLH_pct"],
                            union_rel_wage_lo=(beta - 1.96 * r["se"]) * pres["below_ba"]["union_dlnLH_pct"],
                            union_rel_wage_hi=(beta + 1.96 * r["se"]) * pres["below_ba"]["union_dlnLH_pct"]))
    (DERIVED / "wage_implications.json").write_text(json.dumps(imp, indent=1, default=float))
    with pd.option_context("display.width", 260, "display.max_rows", 500):
        key = est[est.estimator.isin(["first stage on Z2", "OLS", "reduced form on Z2", "IV with Z2",
                                      "IV with Z2_exmex", "IV with Z", "level placebo: Z2 on 2000 level"])
                  & est.endpoint.eq("2010 ACS")
                  & est.outcome.isin(["adj_week_noba", "adj_week_ba", "rel_week"])
                  & est.x.isin(["d_fbemp", "d_lnLH"])]
        print(key[["design", "outcome", "x", "estimator", "n", "coef", "se", "F", "ar_lo", "ar_hi", "ar_kind"]]
              .round(4).to_string(index=False))
        print(json.dumps(pres, indent=1))


if __name__ == "__main__":
    main()
