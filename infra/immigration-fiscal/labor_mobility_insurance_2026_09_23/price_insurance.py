"""Price the local-shock insurance that Mexican-born mobility gives other residents (brief task 2).

Cadena & Kovak (2016) find that the employment rates of native men with high school or less track
local payroll shocks less where Mexican-born workers are a larger share of the less-skilled
population, because Mexican-born workers leave, or do not enter, the hardest-hit metros. This
script turns that smoothing into job-years and earnings of other natives (the account's other
residents), metro by metro, with and without the group:

  with minus without, metro j:   d ln(E/P)_j = g * x_j * s_j
  s_j  QCEW payroll shock less its employment-weighted mean (moving between metros cannot smooth
       the common national shock)
  x_j  the metro's Mexican-born share: of the less-skilled population (eta, the paper's split
       variable) for the empirical gradients; of less-skilled employment by sex (phi) for the
       paper's structural eq. 7
  g    the change in natives' slope per unit x (negative = smoothing)

Jobs_j = g x_j s_j E_j, with E_j the base-year employed other natives (US-born, not of Mexican
origin) of the same sex with high school or less. Protection sums metros with s_j < 0 (jobs kept
where the shock was worst), crowding those with s_j > 0 (jobs not gained where it was mild); the
net is the sum. A job is valued at the metro's base-year annual wage of the same workers in 2024
dollars (CPI-U).

Annualised over a cycle: episode value x D job-years per endpoint job / cycle length L. Beside the
first-order net: convexity (a job crowded out where the shock was mild is worth rho of one kept
where it was severe) and a metro risk premium 0.5 gamma dVar x earnings (an upper bound: it treats
the metro change as everyone's consumption change). Fiscal part: the account's low-skill marginal
tax rate on the earnings. Present-day scaling from derived/mobility_national.csv and ENADID.

Writes derived/insurance_episode.csv, derived/insurance_annual.csv, derived/insurance_summary.json.

Usage, from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/price_insurance.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ck_tests import GROUPS, PERIODS, cellsum, load  # noqa: E402

FISCAL = HERE.parent
DERIVED = HERE / "derived"
ENADID = FISCAL / "enadid_return_selectivity_2026_09_22" / "derived" / "return_migrants_by_schooling.csv"
CPI_CHECK = FISCAL / "ncvs_victim_offender_2026_09_18" / "_cache"

# BLS CPI-U, U.S. city average, all items (CUUR0000SA0), annual averages
CPI = {2006: 201.6, 2010: 218.056, 2012: 229.594, 2016: 240.007, 2019: 255.657, 2021: 270.970,
       2022: 292.655, 2023: 304.702, 2024: 313.689}
GROUP_MEMBERS = 40_896_574          # CPS Mexican-origin residents (brief)
OTHER_RESIDENTS = 295_831_228.85    # CPS ASEC 2025 civilians outside the group (distribution_weights_2026_09_23)
TAU_LOW = 0.384                     # account's low-skill marginal rate, federal + state + payroll
                                    # (matched_benefits_2026_09_19: Colas-Sachs Table 1, 2017 components)
D_GRID = {"low": 2.5, "central": 5.0, "high": 7.5}   # job-years per endpoint job: 2007-10 build-up
                                                     # (2.5), plus 0 / 2.5 / 5 years after 2010
L_GRID = {"low": 12.0, "central": 10.0, "high": 8.0}  # years per cycle (peaks 1990, 2001, 2007, 2020)
RHO = (1.0, 0.75, 0.5, 0.0)        # value of a crowded-out job relative to a protected one
GAMMA = (1.0, 2.0, 3.0)            # relative risk aversion for the risk-premium bound
CK_RETURN_2005_10 = 0.023          # CK Table 1: emigration to Mexico, men HS or less, per year


def check_cpi() -> None:
    """Fail loud if the hard-coded CPI differs from the BLS pull cached by the NCVS lane."""
    seen = {}
    for f in sorted(CPI_CHECK.glob("cpi_*.json")) if CPI_CHECK.exists() else []:
        for x in json.loads(f.read_text())["Results"]["series"][0]["data"]:
            if x["period"] == "M13":
                seen[int(x["year"])] = float(x["value"])
    bad = {y: (v, seen[y]) for y, v in CPI.items() if y in seen and abs(seen[y] - v) > 1e-6}
    if bad:
        raise SystemExit(f"[FAILED] CPI-U mismatch against BLS pull: {bad}")
    print(f"  ✓ CPI-U: {len(set(CPI) & set(seen))} of {len(CPI)} years match the cached BLS pull")


def metro_frame(c, qm, t0, t1):
    """Per metro in base year t0: payroll shock t0->t1, Mexican-born shares, beneficiaries."""
    low = cellsum(c, t0, GROUPS["all"], True)
    d = pd.DataFrame({"eta": cellsum(c, t0, ["mex_fb"], True)["pop"] / low["pop"]})
    for sx, lab in ((1, "men"), (2, "women")):
        allx = cellsum(c, t0, GROUPS["all"], True, sx)
        d[f"phi_{lab}"] = cellsum(c, t0, ["mex_fb"], True, sx)["emp"] / allx["emp"]
        for g in ("oth_nb", "oth_fb"):
            f = cellsum(c, t0, [g], True, sx)
            d[f"E_{g}_{lab}"] = f["emp"]
            d[f"W_{g}_{lab}"] = f["wagebill"] * CPI[2024] / CPI[t0]   # annual wage bill, 2024 $
    d["shock"] = np.log(qm[t1] / qm[t0]).reindex(d.index)
    return d.replace([np.inf, -np.inf], np.nan)


def smoothing_rows():
    sm = pd.read_csv(DERIVED / "ck_smoothing.csv")

    def get(period, panel, spec, sample):
        r = sm[(sm["period"] == period) & (sm["panel"] == panel) & (sm["spec"] == spec) & (sm["sample"] == sample)]
        if len(r) != 1:
            raise SystemExit(f"[FAILED] smoothing row missing: {period} {panel} {spec} {sample}")
        return r.iloc[0]
    return get


def specs(get):
    """(name, period, sex, x, g, se, b0, source). b0 is the natives' slope at x = 0."""
    gr = "GR_2006_2010"
    lo, hi = get(gr, "b_native_lowed_men", "ols", "below_median"), get(gr, "b_native_lowed_men", "ols", "above_median")
    d_eta = hi["mean_eta"] - lo["mean_eta"]            # the paper does not print its halves' means
    out = []
    for name, diff, se, blo, src in (
            ("CK_T5b_IV", -0.448, 0.155, 0.731, "Cadena-Kovak Table 5(b): native men HS or less, Bartik IV, 94 metros, 2006-10"),
            ("CK_T5c_IV_native_shock", -0.431, 0.152, 0.736, "Cadena-Kovak Table 5(c): shock with natives' industry weights")):
        g = diff / d_eta
        out.append((name, gr, "men", "eta", g, se / d_eta, blo - g * lo["mean_eta"], src))
    # eq. 7: slope gap = (phi_a - phi_b) x (native minus Mexican-born population elasticity);
    # 1.206 (0.300) footnote 52, natives 0.007 (0.090) Table 4
    out.append(("CK_eq7_structural", gr, "men", "phi_men", 0.007 - 1.206, float(np.hypot(0.300, 0.090)),
                1 - 0.007, "Cadena-Kovak eq. 7 with footnote 52 and Table 4 elasticities"))
    out.append(("CK_T3_structural_women", gr, "women", "phi_women", 0.166 - 0.743, float(np.hypot(0.157, 0.202)),
                1 - 0.166, "eq. 7 with Cadena-Kovak Table 3 OLS elasticities, women HS or less (paper prices men only)"))
    own = [("own_GR_OLS_natives", gr, "b_native_lowed_men", "ols", "men"),
           ("own_GR_OLS_other_natives", gr, "b1_oth_nb_lowed_men", "ols", "men"),
           ("own_GR_IV_natives", gr, "b_native_lowed_men", "bartik_qcew", "men"),
           ("own_GR_OLS_native_women", gr, "b3_native_lowed_women", "ols", "women"),
           ("own_COVID21_OLS_natives", "COVID_2019_2021", "b_native_lowed_men", "ols", "men"),
           ("own_COVID22_OLS_natives", "COVID_2019_2022", "b_native_lowed_men", "ols", "men"),
           ("own_COVID23_OLS_natives", "COVID_2019_2023", "b_native_lowed_men", "ols", "men"),
           ("own_BOOM_OLS_natives", "BOOM_2012_2016", "b_native_lowed_men", "ols", "men")]
    for name, per, panel, spec, sex in own:
        gr_ = get(per, panel, spec, "slope_gradient_per_unit_eta")
        at = get(per, panel, spec, "slope_at_mean_eta")
        out.append((name, per, sex, "eta", gr_["coef"], gr_["se"], at["coef"] - gr_["coef"] * at["mean_eta"],
                    f"this lane, ck_tests.py: {panel}, {spec}, continuous interaction, QCEW shock"))
    # split version of our GR OLS, same conversion as the paper's
    diff = get(gr, "b_native_lowed_men", "ols", "difference")
    g = diff["coef"] / d_eta
    out.append(("own_GR_OLS_natives_split", gr, "men", "eta", g, diff["se"] / d_eta, lo["coef"] - g * lo["mean_eta"],
                "this lane: below/above-median OLS difference over the halves' eta gap"))
    return out, d_eta


def episode(d, g, xcol, E, W, b0):
    """Jobs and 2024 $ of one episode (per year of the endpoint gap), with minus without the group."""
    m = d[[xcol, E, W, "shock"]].dropna()
    m = m[(m[E] > 0) & (m[W] > 0)]
    e, x, w = m[E].to_numpy(), m[xcol].to_numpy(), m[W].to_numpy()
    s = m["shock"].to_numpy() - np.average(m["shock"], weights=e)
    jobs = g * x * s * e
    wage = w / e
    usd = jobs * wage
    bust, boom = s < 0, s > 0
    v_without = np.average((b0 * s) ** 2, weights=e) - np.average(b0 * s, weights=e) ** 2
    v_with = np.average(((b0 + g * x) * s) ** 2, weights=e) - np.average((b0 + g * x) * s, weights=e) ** 2
    return {"n_metros": len(m), "beneficiaries_employed": e.sum(), "beneficiary_wagebill_bn": w.sum() / 1e9,
            "sd_shock": float(np.sqrt(np.average(s ** 2, weights=e))), "mean_x": float(np.average(x, weights=e)),
            "protection_jobs": jobs[bust].sum(), "crowding_jobs": -jobs[boom].sum(), "net_jobs": jobs.sum(),
            "protection_bn": usd[bust].sum() / 1e9, "crowding_bn": -usd[boom].sum() / 1e9, "net_bn": usd.sum() / 1e9,
            "var_without": v_without, "var_with": v_with}


def return_rates():
    """Annual return rate to Mexico, Mexico-born men with high school or less: ENADID over ACS t-5."""
    en = pd.read_csv(ENADID)
    out = {}
    for wave in sorted(en["wave"].unique()):
        r = en[(en["wave"] == wave) & (en["slice"] == "sex:men") & (en["group"] == "returnee_from_us")]
        if r.empty:
            continue
        pop = float(r["weighted_pop"].iloc[0])
        tert = float(r.loc[r["measure"] == "tertiary", "estimate"].iloc[0])
        base = wave - 5
        p = pd.read_parquet(HERE / "_cache" / "acs" / f"p{base}.parquet",
                            columns=["pwgtp", "agep", "sex", "lowed", "group", "gq"])
        den = p.loc[(p["group"] == "mex_fb") & (p["sex"] == 1) & p["lowed"] & ~p["gq"]
                    & p["agep"].between(18, 59), "pwgtp"].sum()
        out[int(wave)] = {"returnees_5yr_men": pop, "share_hs_or_less": 1 - tert, "acs_base_year": base,
                          "acs_mexfb_men_hs_or_less_18_59": float(den),
                          "annual_rate": pop * (1 - tert) / 5 / float(den)}
    return out


def present_day_factors(ret):
    mob = pd.read_csv(DERIVED / "mobility_national.csv")
    x = mob[(mob["lowed"] == "hs_or_less") & (mob["sex"] == "men") & (mob["measure"] == "long_distance")
            & (mob["group"] == "mex_fb_minus_oth_nb")].set_index("year")["rate"]
    ld_then, ld_now = x.loc[2006:2010].mean(), x.loc[2019:2024].mean()
    ret_now = ret[max(ret)]["annual_rate"]
    rate_ratio = (ld_now + ret_now) / (ld_then + CK_RETURN_2005_10)
    pop = pd.read_csv(DERIVED / "ck_population.csv")

    def gap(period):
        q = pop[(pop["period"] == period) & (pop["sex"] == "men") & (pop["educ"] == "hs_or_less")
                & (pop["spec"] == "OLS_qcew_mexshare_control")].set_index("group")["coef"]
        return q["mex_fb"] - q["natives"]
    gaps = {p: gap(p) for p in ("GR_2006_2010", "COVID_2019_2021", "COVID_2019_2022", "COVID_2019_2023", "BOOM_2012_2016")}
    return {"long_distance_excess_2006_10": ld_then, "long_distance_excess_2019_24": ld_now,
            "return_rate_now": ret_now, "return_rate_ck_2005_10": CK_RETURN_2005_10,
            "rate_ratio": rate_ratio,
            "elasticity_gap_mexfb_minus_natives_ols": gaps,
            "elasticity_ratio_covid21_over_gr": gaps["COVID_2019_2021"] / gaps["GR_2006_2010"],
            "factor_low": 0.0, "factor_central": max(rate_ratio, 0.0),
            "factor_high": max(gaps["COVID_2019_2021"] / gaps["GR_2006_2010"], rate_ratio, 0.0)}


def main():
    check_cpi()
    c, _s, qm, _ns = load()
    get = smoothing_rows()
    spec_list, d_eta = specs(get)
    samples = pd.read_csv(DERIVED / "ck_metro_sample.csv", dtype={"cbsa": str})
    frames = {p: metro_frame(c, qm, *PERIODS[p]) for p in sorted({s[1] for s in spec_list})}
    rows = []
    for name, per, sex, xcol, g, se, b0, src in spec_list:
        d_all = frames[per]
        sets = {"all_metros": d_all, "ck_sample": d_all.reindex(samples.loc[samples["period"] == per, "cbsa"])}
        scopes = {"other_natives": ([f"E_oth_nb_{sex}"], [f"W_oth_nb_{sex}"]),
                  "other_natives_and_other_foreign_born": ([f"E_oth_nb_{sex}", f"E_oth_fb_{sex}"],
                                                           [f"W_oth_nb_{sex}", f"W_oth_fb_{sex}"])}
        for set_name, d in sets.items():
            for scope, (ecols, wcols) in scopes.items():
                dd = d.copy()
                dd["_E"], dd["_W"] = dd[ecols].sum(axis=1, min_count=1), dd[wcols].sum(axis=1, min_count=1)
                r = episode(dd, g, xcol, "_E", "_W", b0)
                rows.append({"spec": name, "period": per, "sex": sex, "x": xcol, "g": g, "g_se": se, "b0": b0,
                             "metros": set_name, "beneficiaries": scope, "source": src, **r})
    ep = pd.DataFrame(rows)
    rel = (ep["g_se"] / ep["g"].abs()).replace(np.inf, np.nan)
    for k in ("protection_bn", "crowding_bn", "net_bn"):
        ep[k.replace("_bn", "_bn_se")] = ep[k].abs() * rel
    ep.to_csv(DERIVED / "insurance_episode.csv", index=False)

    # annualised grid: episode $ per year of gap x D / L; welfare with rho; risk premium; fiscal part
    ann = []
    for _, r in ep.iterrows():
        for dl, D in D_GRID.items():
            for ll, L in L_GRID.items():
                f = D / L
                row = {k: r[k] for k in ("spec", "period", "sex", "metros", "beneficiaries")}
                row.update(D=D, L=L, D_case=dl, L_case=ll, protection_bn=r["protection_bn"] * f,
                           crowding_bn=r["crowding_bn"] * f, net_bn=r["net_bn"] * f,
                           net_bn_se=r["net_bn_se"] * f, fiscal_net_bn=TAU_LOW * r["net_bn"] * f,
                           fiscal_protection_bn=TAU_LOW * r["protection_bn"] * f)
                for rho in RHO:
                    row[f"welfare_rho_{rho}_bn"] = (r["protection_bn"] - rho * r["crowding_bn"]) * f
                for gm in GAMMA:
                    row[f"risk_premium_gamma_{gm:g}_bn"] = 0.5 * gm * (r["var_without"] - r["var_with"]) * r["beneficiary_wagebill_bn"] * f
                ann.append(row)
    an = pd.DataFrame(ann)
    an.to_csv(DERIVED / "insurance_annual.csv", index=False)

    ret = return_rates()
    pdf = present_day_factors(ret)
    # CK's own check of eq. 7: predicted slope gap -0.29 with their phi gap; ours from the GR sample
    gr = frames["GR_2006_2010"].reindex(samples.loc[samples["period"] == "GR_2006_2010", "cbsa"])
    hi = gr["eta"] > gr["eta"].median()
    phi_gap = gr.loc[hi, "phi_men"].mean() - gr.loc[~hi, "phi_men"].mean()

    def pick(spec, metros="all_metros", scope="other_natives", D="central", L="central"):
        return an[(an["spec"] == spec) & (an["metros"] == metros) & (an["beneficiaries"] == scope)
                  & (an["D_case"] == D) & (an["L_case"] == L)].iloc[0]
    cen = pick("CK_T5b_IV")
    ck_men = ["CK_T5b_IV", "CK_T5c_IV_native_shock", "CK_eq7_structural"]
    sets = ("all_metros", "ck_sample")
    # CK-era insurance welfare: central rho 0.75 (midpoint of linear and the Davis-von Wachter ratio);
    # low = rho 1 at the short gap and long cycle over the paper's men specs and both metro sets;
    # high = rho 0.5 at the long gap and short cycle, other natives and other foreign-born, men plus
    # the eq. 7 women's term
    low = min(pick(s, m, D="low", L="low")["welfare_rho_1.0_bn"] for s in ck_men for m in sets)
    high = max(pick(s, m, "other_natives_and_other_foreign_born", "high", "high")["welfare_rho_0.5_bn"]
               + pick("CK_T3_structural_women", m, "other_natives_and_other_foreign_born", "high", "high")["welfare_rho_0.5_bn"]
               for s in ck_men for m in sets)
    ck_era = {"low": low, "central": cen["welfare_rho_0.75_bn"], "high": high}
    present = {"low": ck_era["low"] * pdf["factor_low"], "central": ck_era["central"] * pdf["factor_central"],
               "high": ck_era["high"] * pdf["factor_high"]}
    bj = pd.read_csv(DERIVED / "borjas_2024.csv")
    bj = bj[bj["scenario"] == "mexico_born_all"]
    full, obs = bj[bj["sorting"] == "full_sorting_theta_1"], bj[bj["sorting"] == "observed_sorting_2024"]
    cell = (bj["lambda"] == 0.40) & (bj["cost"] == "medium")
    borjas = {"as_defined_full_sorting": {"low": full["gain_bn_2024_fine_grid"].min(),
                                          "central": float(full.loc[cell, "gain_bn_2024_fine_grid"].iloc[0]),
                                          "high": full["gain_bn_2024_fine_grid"].max()},
              "observed_2024_sorting": {"low": obs["gain_bn_2024_fine_grid"].min(),
                                        "central": float(obs.loc[cell, "gain_bn_2024_fine_grid"].iloc[0]),
                                        "high": obs["gain_bn_2024_fine_grid"].max()}}
    lane = {k: present[k] + borjas["observed_2024_sorting"][k] for k in ("low", "central", "high")}
    summary = {
        "frame": "annual, 2024 dollars, other residents",
        "d_eta_gr_halves": d_eta, "phi_gap_gr_halves": phi_gap,
        "eq7_predicted_gap_ours": (0.007 - 1.206) * phi_gap, "eq7_predicted_gap_paper": -0.29,
        "central_spec": "CK_T5b_IV, all metros, other-native men, D 5, L 10",
        "ck_era_central_components_bn": {k: cen[k] for k in (
            "protection_bn", "crowding_bn", "net_bn", "net_bn_se", "welfare_rho_1.0_bn", "welfare_rho_0.75_bn",
            "welfare_rho_0.5_bn", "welfare_rho_0.0_bn", "risk_premium_gamma_1_bn", "risk_premium_gamma_2_bn",
            "risk_premium_gamma_3_bn", "fiscal_net_bn", "fiscal_protection_bn")},
        "insurance_ck_era_bn": ck_era, "present_day": pdf, "insurance_present_bn": present,
        "borjas_bn": borjas, "lane_total_present_bn": lane,
        "per_group_member_usd": {k: v * 1e9 / GROUP_MEMBERS for k, v in lane.items()},
        "per_other_resident_usd": {k: v * 1e9 / OTHER_RESIDENTS for k, v in lane.items()},
        "insurance_ck_era_per_member_usd": {k: v * 1e9 / GROUP_MEMBERS for k, v in ck_era.items()},
        "denominators": {"group_members": GROUP_MEMBERS, "other_residents": OTHER_RESIDENTS},
        "enadid_return_rates": ret,
    }
    (DERIVED / "insurance_summary.json").write_text(json.dumps(summary, indent=2, default=float))

    show = ep[(ep["beneficiaries"] == "other_natives")][
        ["spec", "period", "metros", "n_metros", "g", "g_se", "mean_x", "sd_shock", "protection_jobs",
         "crowding_jobs", "net_jobs", "protection_bn", "crowding_bn", "net_bn", "net_bn_se"]]
    print(show.round(3).to_string(index=False))
    print(json.dumps({k: v for k, v in summary.items() if k not in ("enadid_return_rates",)}, indent=1, default=float))


if __name__ == "__main__":
    main()
