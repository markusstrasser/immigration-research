"""Formula-chain audit, arm-versus-sampling comparison, epsilon sensitivity and SE catalog.

Reads published derived CSVs only (plus this lane's propagate.py outputs). The
headline recomputation deliberately does not use the full account's
response_pools.csv or service_response.py: it rebuilds the pools from the
receipt and spending category tables and the BEA education cells.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
FA = FISCAL / "full_account_2026_09_20/derived"
CAPITAL_CATEGORIES = {"corporate_capital", "corporate_labor", "modeled_owner_property",
                      "remaining_production_property", "personal_property_tax"}
DELAYED = {"economic_affairs_services", "recreation_culture"}
EPSILONS = [5.0, 7.0]


def sdr(values):
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


# --------------------------------------------------------------------------
# 1. Ledger replicate aggregation
# --------------------------------------------------------------------------
LIVE_LEDGER_ARMS = ["base", "G|deflated2024", "K|central", "P|net_of_item_G", "D|central", "U|central",
                    "I|central", "M|central", "E|zero", "C|wage25_capital75", "X|per_capita", "R|central",
                    "F|zero", "S|all_inside_meps"]
STALE_LEDGER_ARMS = ["base", "G|deflated2024", "K|central", "U|central", "I|central", "M|central",
                     "E|stock", "C|wage25_capital75", "X|per_capita", "R|central", "F|zero",
                     "S|half_inside_meps"]


def ledger_endpoint(arms, group="mexican_observed_total"):
    z = np.load(FISCAL / "ledger_absolute_2026_09_17/derived/replicates.npz")
    total = sum(z[f"{a}|{group}"] for a in arms)
    return total / 1e9


def ledger_check():
    wf = pd.read_csv(FISCAL / "ledger_absolute_2026_09_17/derived/waterfall.csv").query(
        "group == 'mexican_observed_total'")
    n_item = wf.query("item == 'N'").item_bn.iloc[0]  # external add, no replicate
    live = ledger_endpoint(LIVE_LEDGER_ARMS)
    base = ledger_endpoint(["base"])
    stale = ledger_endpoint(STALE_LEDGER_ARMS)
    rows = [
        dict(quantity="base partial account", published_bn=50.238214, published_se_bn=7.473981,
             published_where="ledger RESULT.md line 262 and live waterfall.csv step 0",
             rebuilt_bn=base[0], rebuilt_se_bn=sdr(base)),
        dict(quantity="live union complete endpoint (D,P on; E zero)", published_bn=wf.cumulative_bn.iloc[-1],
             published_se_bn=wf.se_bn.iloc[-1], published_where="live waterfall.csv step 14",
             rebuilt_bn=live[0] + n_item, rebuilt_se_bn=sdr(live)),
        dict(quantity="Sept 17 union endpoint (stale vintage; D,P off; E stock; S half)",
             published_bn=-253.93, published_se_bn=8.81,
             published_where="ledger RESULT.md line 262 (superseded by Sept 18-19 rebuilds)",
             rebuilt_bn=stale[0] + n_item, rebuilt_se_bn=sdr(stale)),
    ]
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# 2. Independent headline recomputation
# --------------------------------------------------------------------------
def pools():
    rec = pd.read_csv(FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv")
    spe = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv")
    rows = []
    for (rs, alloc), r in rec.groupby(["scenario_id", "allocation"]):
        if rs == "evidence_only" or "external" in rs:
            continue
        direct = r.loc[r.response_class.isin(["personal_income", "household_direct"])
                       & ~r.category.isin(CAPITAL_CATEGORIES), "target_bn"].sum()
        for ss in ["complete_preferred_F_per_capita", "complete_alternative_keys_F_per_capita"]:
            s = spe.query("scenario_id == @ss and allocation == @alloc")
            rows.append(dict(receipt_scenario=rs, spending_scenario=ss, allocation=alloc, direct=direct,
                             transfers=s.query("response_class == 'household_transfer'").target_bn.sum(),
                             services=s.query("response_class == 'service'").target_bn.sum(),
                             public_goods=s.query("response_class == 'public_goods'").target_bn.sum()))
    return pd.DataFrame(rows), spe


def school_bounds():
    cells = json.loads((FA / "service_response_audit.json").read_text())["bea_cells"]
    v = {k: x["bn"] for k, x in cells.items()}
    gross, school, current = v["T31505-A:29"], v["T31505-A:30"], v["T31700-A:9"]
    return max(0., school - (gross - current)) / current, min(1., school / current)


def case_specs():
    lo, hi = school_bounds()
    specs = [("proportional_reference", lo, 1., 1., 1.)]
    for share in (lo, hi):
        for sr in (.63, .66):
            specs.append(("school_response_only", share, sr, 1., 1.))
            for other in (0., 1.):
                specs.append(("cbo_category_lag_non_school_full" if other else "cbo_category_lag_non_school_fixed",
                              share, sr, other, 0.))
    specs += [("education_fixed_diagnostic", 0., 0., 0., 0.), ("education_full_diagnostic", 0., 1., 1., 0.)]
    return specs


def recompute_cases(pf):
    """pf: {normalization: private_plus_receipts_bn}. Returns 60 rows keyed like service_response_cases."""
    pool, spe = pools()
    rows = []
    for alloc in ["personal", "shared"]:
        p = pool.query("receipt_scenario == 'cbo_collective' and spending_scenario == 'complete_preferred_F_per_capita' and allocation == @alloc").iloc[0]
        svc = spe.query("scenario_id == 'complete_preferred_F_per_capita' and allocation == @alloc and response_class == 'service'").set_index("category").target_bn
        for number, (profile, share, sr, other, delayed) in enumerate(case_specs()):
            responsive = 0.
            for cat, amount in svc.items():
                if cat == "education_services":
                    responsive += amount * (share * sr + (1 - share) * other)
                else:
                    responsive += amount * (delayed if cat in DELAYED else 1.)
            for norm, value in pf.items():
                welfare = p.direct - p.transfers - responsive + value
                rows.append(dict(case_id=f"{alloc}_{number}", allocation=alloc, normalization=norm, profile=profile,
                                 direct_receipts_bn=p.direct, transfers_bn=p.transfers,
                                 responsive_services_bn=responsive, production_term_bn=value,
                                 welfare_bn=welfare))
    return pd.DataFrame(rows)


def formula_audit():
    bens = pd.read_csv(FISCAL / "full_account_benefits_2026_09_20/derived/benefit_scenarios.csv")
    head = bens.query("scenario_id in ['ces_0086_owner000', 'ces_0248_owner000']").set_index("normalization")
    pf = head.private_plus_receipts_bn.to_dict()
    mine = recompute_cases(pf)
    pub = pd.read_csv(FA / "service_response_cases.csv")
    m = mine.merge(pub[["case_id", "normalization", "welfare_bn"]], on=["case_id", "normalization"],
                   suffixes=("_recomputed", "_published"), validate="one_to_one")
    m["abs_diff_bn"] = (m.welfare_bn_recomputed - m.welfare_bn_published).abs()
    m["object"] = "service_response_case"
    # Four headline_cases rows.
    hc = pd.read_csv(FA / "headline_cases.csv")
    ref = mine.query("profile == 'proportional_reference'")
    h = ref.merge(hc[["allocation", "normalization", "welfare_bn"]], on=["allocation", "normalization"],
                  suffixes=("_recomputed", "_published"))
    h["abs_diff_bn"] = (h.welfare_bn_recomputed - h.welfare_bn_published).abs()
    h["object"] = "headline_cases"
    # Core long-run grid and capacity path, from rebuilt pools x all 3,888 benefit scenarios.
    pool, _ = pools()
    summary = json.loads((FA / "headline_summary.json").read_text())
    extra = []
    b = bens.copy()
    grid = []
    for p in pool.itertuples():
        w = p.direct - p.transfers - b.capital_adjustment * p.services + b.private_plus_receipts_bn
        grid.append(pd.DataFrame(dict(welfare=w, owner=b.excluded_capital_owner_share, cap=b.capital_adjustment)))
    grid = pd.concat(grid)
    core = grid.query("owner == 0 and cap == 1").welfare
    extra.append(("core long-run grid min", core.min(), summary["longrun_core_grid_welfare_bn"][0]))
    extra.append(("core long-run grid max", core.max(), summary["longrun_core_grid_welfare_bn"][1]))
    allown = grid.query("cap == 1").welfare
    extra.append(("full capital, all ownership, max", allown.max(), summary["full_capital_all_ownership_endpoints_welfare_bn"][1]))
    for cap in ["0.0", "0.5", "1.0"]:
        v = grid.loc[(grid.owner == 0) & (grid.cap == float(cap)), "welfare"]
        extra.append((f"capacity path {cap} min", v.min(), summary["core_capacity_path"][cap]["min"]))
        extra.append((f"capacity path {cap} max", v.max(), summary["core_capacity_path"][cap]["max"]))
    e = pd.DataFrame(extra, columns=["case_id", "welfare_bn_recomputed", "welfare_bn_published"])
    e["abs_diff_bn"] = (e.welfare_bn_recomputed - e.welfare_bn_published).abs()
    e["object"] = "headline_summary"
    cols = ["object", "case_id", "allocation", "normalization", "profile", "welfare_bn_recomputed",
            "welfare_bn_published", "abs_diff_bn"]
    return pd.concat([m.reindex(columns=cols), h.reindex(columns=cols), e.reindex(columns=cols)], ignore_index=True), mine


# --------------------------------------------------------------------------
# 3. Epsilon sensitivity (sensitivity rows only; no headline changed)
# --------------------------------------------------------------------------
def epsilon_rows(unc):
    nest = pd.read_csv(FISCAL / "production_nativity_nest_2026_09_22/derived/nest_headline.csv")
    nest = nest.query("nest_option == 'A_by_nativity' and excluded_capital_owner_share == 0")
    rows = []
    base = nest.query("sigma_NI == inf").set_index("normalization")
    for eps in [np.inf, *EPSILONS]:
        n = nest.loc[np.isclose(nest.sigma_NI, eps) | ((eps == np.inf) & np.isinf(nest.sigma_NI))].set_index("normalization")
        for u in unc.itertuples():
            delta = n.loc[u.normalization, "private_plus_receipts_bn"] - base.loc[u.normalization, "private_plus_receipts_bn"]
            se_pf = n.loc[u.normalization, "private_plus_receipts_se_sampling_bn"]
            se = np.sqrt(u.se_cps_fiscal_keys_bn ** 2 + se_pf ** 2 + u.se_school_correction_bn ** 2 + u.se_meps_donor_bn ** 2)
            rows.append(dict(epsilon=eps, epsilon_sourced=bool(n.loc[u.normalization, "sigma_NI_sourced"]),
                             case_id=u.case_id, allocation=u.allocation, normalization=u.normalization,
                             profile=u.profile, production_term_bn=n.loc[u.normalization, "private_plus_receipts_bn"],
                             net_cost_bn=u.net_cost_bn - delta, change_vs_headline_bn=-delta,
                             se_combined_independent_bn=se))
    frame = pd.DataFrame(rows)
    band = frame.groupby(["epsilon", "profile"]).agg(
        net_cost_min_bn=("net_cost_bn", "min"), net_cost_max_bn=("net_cost_bn", "max"),
        change_min_bn=("change_vs_headline_bn", "min"), change_max_bn=("change_vs_headline_bn", "max"),
        se_max_bn=("se_combined_independent_bn", "max")).reset_index()
    return frame, band


# --------------------------------------------------------------------------
# 4. Arms versus sampling
# --------------------------------------------------------------------------
def arms_vs_sampling(unc, formula):
    summary = json.loads((FA / "headline_summary.json").read_text())
    se_ind = unc.se_combined_independent_bn.max()
    se_env = unc.se_all_positive_correlation_bn.max()
    se_cps = unc.se_cps_fiscal_keys_bn.max()
    spans = []
    for profile, label in [("cbo_category_lag_non_school_full", "main CBO-informed band, 16 cases"),
                           ("cbo_category_lag_non_school_fixed", "education-fixed band, 16 cases"),
                           ("proportional_reference", "full proportional-service benchmark, 4 cases")]:
        v = unc.query("profile == @profile").net_cost_bn
        spans.append((label, v.min(), v.max()))
    spans.append(("all 60 executed service-response cases", unc.net_cost_bn.min(), unc.net_cost_bn.max()))
    spans.append(("three headline constructions together (121-289)",
                  unc.query("profile in ['cbo_category_lag_non_school_full', 'cbo_category_lag_non_school_fixed', 'proportional_reference']").net_cost_bn.min(),
                  unc.query("profile in ['cbo_category_lag_non_school_full', 'cbo_category_lag_non_school_fixed', 'proportional_reference']").net_cost_bn.max()))
    g = summary["longrun_core_grid_welfare_bn"]
    spans.append(("proportional-service core grid (receipt/spending/production arms)", -g[1], -g[0]))
    own = summary["full_capital_all_ownership_endpoints_welfare_bn"]
    spans.append(("full capital, all ownership endpoints", -own[1], -own[0]))
    cp = summary["core_capacity_path"]
    spans.append(("capacity path, services 0/.5/1 with capital 0/.5/1", -cp["0.0"]["max"], -cp["1.0"]["min"]))
    rows = []
    for label, lo, hi in spans:
        span = hi - lo
        rows.append(dict(arm_set=label, net_cost_low_bn=lo, net_cost_high_bn=hi, span_bn=span,
                         se_cps_only_bn=se_cps, se_combined_independent_bn=se_ind,
                         se_all_positive_correlation_bn=se_env,
                         span_over_se_combined=span / se_ind,
                         span_over_ci95_width_independent=span / (2 * 1.96 * se_ind),
                         span_over_ci95_width_envelope=span / (2 * 1.96 * se_env)))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# 5. Published-SE catalog
# --------------------------------------------------------------------------
def catalog(unc, ledger):
    meta = json.loads((OUT / "propagation_meta.json").read_text())
    est = pd.read_csv(FISCAL / "all_age_ledger_2026_09_17/derived/estimates.csv").query(
        "scenario == 'baseline' and target == 'mexican_observed_total' and metric == 'absolute_total'").iloc[0]
    items = pd.read_csv(FISCAL / "ledger_absolute_2026_09_17/derived/items_by_group.csv")
    m_item = items.query("item == 'M' and group == 'mexican_observed_total'")
    comp = pd.read_csv(OUT / "component_sampling.csv")
    meps = pd.read_csv(OUT / "meps_donor_contribution.csv")
    rows = [
        dict(source="ledger_absolute_2026_09_17 replicate SDR, union complete endpoint",
             published_se_bn=ledger.published_se_bn.iloc[1], object="partial-plus-priced-items ledger, CPS-level dollars",
             used_in_headline_interval=False,
             reason="Different account: ledger dollars come from CPS microdata; the complete account fixes national BEA totals, so its CPS error is rebuilt directly on the key shares (row 'CPS fiscal keys')."),
        dict(source="all_age_ledger_2026_09_17 estimates.csv se_meps, union absolute_total",
             published_se_bn=est.se_meps / 1e9, object="all-age partial ledger; MEPS donor means set medical dollar levels",
             used_in_headline_interval=False,
             reason="In the complete account BEA program totals are fixed and MEPS means only split them between groups; the donor error is recomputed on that share (row 'MEPS donor, key shares')."),
        dict(source="all_age_ledger_2026_09_17 estimates.csv se_cps, union absolute_total",
             published_se_bn=est.se_cps / 1e9, object="all-age partial ledger", used_in_headline_interval=False,
             reason="Same as above; superseded for this object by the direct key-share replicate rebuild."),
        dict(source="ledger item M (MEPS-to-NHEA coverage scaling) replicate SE",
             published_se_bn=float(m_item.se_bn.iloc[0]) if "se_bn" in m_item and len(m_item) else np.nan,
             object="ledger item M", used_in_headline_interval=False,
             reason="No item M in the complete account: medical programs enter at BEA Table 3.12 totals; the scaling ratio it corrects does not exist here. Item M's own donor error was never published."),
        dict(source="lineage_cost_2026_09_19 via all_age estimates.csv se_cps/se_meps",
             published_se_bn=np.nan, object="lifetime/lineage projections", used_in_headline_interval=False,
             reason="Lifetime object, not the annual complete account."),
        dict(source="period_uncertainty_2026_09_19 period profiles", published_se_bn=np.nan,
             object="adult lifetime period profiles", used_in_headline_interval=False,
             reason="Lifetime object, not the annual complete account."),
        dict(source="full_account_receipts allocation_keys.csv target_share_sampling_se",
             published_se_bn=np.nan, object="complete-account receipt key shares", used_in_headline_interval=True,
             reason="Reproduced exactly from 161 weights; used jointly (with covariance) inside 'CPS fiscal keys'."),
        dict(source="full_account_benefits benefit_scenarios.csv private_plus_receipts_se_sampling_bn",
             published_se_bn=np.nan, object="production term P+F (GDP 1.12 / cash 0.74)", used_in_headline_interval=True,
             reason="Carried as its own term; replicate vectors not exported, so covariance with the fiscal keys is unknown (independence plus a rho=+1 envelope)."),
        dict(source="school_enrollment_2026_09_20 correction_effects.csv school SE (October+March CPS)",
             published_se_bn=meta["school_relative_se"]["personal"]["se_upper_bn"],
             object="enrollment correction to target school spending only", used_in_headline_interval=True,
             reason="Only the correction's sampling error is published; it is applied as a relative error on the education key. The base school incidence key has no published replicate error (partial coverage)."),
        dict(source="production_nativity_nest nest_headline.csv SE", published_se_bn=np.nan,
             object="nested production term at each epsilon", used_in_headline_interval=False,
             reason="Used only in the epsilon sensitivity rows."),
        dict(source="ledger_recut g_composition.csv elasticity_se", published_se_bn=np.nan,
             object="cross-state service elasticities for ledger item G", used_in_headline_interval=False,
             reason="Headline uses CBO's 0.37/0.34 coefficients as two arms; their standard errors are not in the repository."),
    ]
    for a in ["personal", "shared"]:
        rows.append(dict(source=f"THIS LANE: CPS fiscal keys, {a} (161-weight rebuild)",
                         published_se_bn=float(unc.query("allocation == @a").se_cps_fiscal_keys_bn.max()),
                         object="direct receipts, transfers and services jointly", used_in_headline_interval=True,
                         reason="Receipts SE " + f"{comp.query('allocation == @a and component == \"direct_receipts\"').se_cps_bn.iloc[0]:.2f}"
                                + ", transfers " + f"{comp.query('allocation == @a and component == \"transfers\"').se_cps_bn.iloc[0]:.2f}"
                                + "; positively correlated, so the net SE is below their quadrature sum."))
        rows.append(dict(source=f"THIS LANE: MEPS donor, key shares, {a}",
                         published_se_bn=float(meps.query("allocation == @a and key == 'ALL_MEDICAL_JOINT'").se_meps_key_only_bn.iloc[0]),
                         object="Medicare, Medicaid, VA, TRICARE and health-services key shares",
                         used_in_headline_interval=True,
                         reason="Stratified-PSU Taylor covariance over 5 payer means x 10 age/birth cells, estimator checked against donor_model."))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------
# 6. General services: ledger versus complete account
# --------------------------------------------------------------------------
def general_services():
    spe = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv").query(
        "scenario_id == 'complete_preferred_F_per_capita'")
    wf = pd.read_csv(FISCAL / "ledger_absolute_2026_09_17/derived/waterfall.csv").query("group == 'mexican_observed_total'")
    gc = pd.read_csv(FISCAL / "ledger_recut_2026_09_22/derived/g_composition.csv")
    g_bn = wf.query("item == 'G'").item_bn.iloc[0]
    admin = gc.query("function in ['financial administration', 'general public buildings', 'other governmental administration']").share.sum()
    interest = gc.query("function == 'interest on general debt'").share.sum()
    rows = []
    for alloc in ["personal", "shared"]:
        s = spe.query("allocation == @alloc").set_index("category").target_bn
        rows.append(dict(object="complete account", allocation=alloc, line="general_public_services (all levels)",
                         assigned_bn=s["general_public_services"], headline_response=0.,
                         charged_in_headline_bn=0., sign_convention="welfare_bn negative = cost to others"))
        rows.append(dict(object="complete account", allocation=alloc, line="domestic_interest (all levels)",
                         assigned_bn=s["domestic_interest"], headline_response=0.,
                         charged_in_headline_bn=0., sign_convention="welfare_bn negative = cost to others"))
        rows.append(dict(object="complete account", allocation=alloc, line="ordinary services in the G-like functions (public order, economic affairs, housing, recreation)",
                         assigned_bn=s[["public_order_safety", "economic_affairs_services", "housing_community_services", "recreation_culture"]].sum(),
                         headline_response=np.nan, charged_in_headline_bn=np.nan,
                         sign_convention="response 1 in the proportional reference; economic affairs and recreation 0 in the CBO-lag profiles"))
    rows.append(dict(object="ledger (live, shared)", allocation="shared", line="item G state-local general services, fee-netted",
                     assigned_bn=-g_bn, headline_response=1., charged_in_headline_bn=-g_bn,
                     sign_convention="balance negative = cost; charged at m=1 in the central arm"))
    rows.append(dict(object="ledger (live, shared)", allocation="shared",
                     line="of which state-local general administration (financial admin, public buildings, other admin), gross-share transport",
                     assigned_bn=-g_bn * admin, headline_response=1., charged_in_headline_bn=-g_bn * admin,
                     sign_convention=f"share {admin:.4f} of 2022 gross G applied to net G [INFERENCE]"))
    rows.append(dict(object="ledger (live, shared)", allocation="shared",
                     line="of which state-local interest on general debt, gross-share transport",
                     assigned_bn=-g_bn * interest, headline_response=1., charged_in_headline_bn=-g_bn * interest,
                     sign_convention=f"share {interest:.4f} of 2022 gross G applied to net G [INFERENCE]"))
    rows.append(dict(object="ledger (live, shared)", allocation="shared", line="item F federal defense, net interest, general government",
                     assigned_bn=0., headline_response=0., charged_in_headline_bn=0.,
                     sign_convention="central arm zero, same treatment as the complete account"))
    return pd.DataFrame(rows)


def main():
    unc = pd.read_csv(OUT / "case_uncertainty.csv")
    ledger = ledger_check()
    ledger.to_csv(OUT / "ledger_replicate_check.csv", index=False)
    audit, mine = formula_audit()
    audit.to_csv(OUT / "formula_audit.csv", index=False)
    mine.to_csv(OUT / "headline_recomputed.csv", index=False)
    eps, band = epsilon_rows(unc)
    eps.to_csv(OUT / "epsilon_cases.csv", index=False)
    band.to_csv(OUT / "epsilon_bands.csv", index=False)
    arms = arms_vs_sampling(unc, audit)
    arms.to_csv(OUT / "arms_vs_sampling.csv", index=False)
    catalog(unc, ledger).to_csv(OUT / "se_catalog.csv", index=False)
    general_services().to_csv(OUT / "general_services.csv", index=False)
    contrib = unc.assign(
        var_cps=unc.se_cps_fiscal_keys_bn ** 2, var_pf=unc.se_production_term_bn ** 2,
        var_school=unc.se_school_correction_bn ** 2, var_meps=unc.se_meps_donor_bn ** 2)
    contrib["var_total"] = contrib[["var_cps", "var_pf", "var_school", "var_meps"]].sum(axis=1)
    for k in ["cps", "pf", "school", "meps"]:
        contrib[f"share_{k}"] = contrib[f"var_{k}"] / contrib.var_total
    contrib.groupby("profile")[[c for c in contrib if c.startswith("share_")]].mean().to_csv(OUT / "variance_shares.csv")
    pd.set_option("display.width", 250)
    print(ledger.to_string(index=False))
    print("max formula diff", audit.abs_diff_bn.max())
    print(band.to_string(index=False))
    print(arms.to_string(index=False))


if __name__ == "__main__":
    main()
