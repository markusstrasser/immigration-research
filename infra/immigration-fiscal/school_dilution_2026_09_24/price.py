"""Task 3-5: price the instructional dilution borne by other residents' pupils, beside the account.

1. Instruction dollars that do not follow the group's pupils, district by district:
       loss_d = (1 - b_I) * instruction per pupil_d * group pupils_d
   summed over districts, this is what other pupils forgo relative to the group's absence (to first
   order, the account's own linear treatment). b_I comes from one of:
     account      the account's response r = 0.63 / 0.66 for current spending, with instruction's share
                  of the non-response from the district one-year decomposition (CBO's horizon):
                  b_I = 1 - phi * (1 - r) / w_I                                   [central]
     long_run     within-district 19-year difference, b_I = 0.924                 [persistent part]
     and every other district horizon (1, 3, 4-5 years, all-horizon FE) as rows; the account rows again
     with instruction's share taken from the 3-year and 4-5-year splits; and the state-level panels
     (CBO's design unweighted and pupil-weighted, the 2000-2019 state long difference).
   A power-law variant, other-pupil loss = O_d * I_d * [(1 - s_d)^(b - 1) - 1], is reported too, and
   a full-funding split: against spending that fully follows enrollment at current district sizes,
   every pupil in district d is short (1 - b) * s_d * I_d, so other pupils bear (1 - s_d) of loss_d and
   the group's pupils s_d. The linear rule extrapolates where the group is a majority of the district.
2. Test scores: Jackson-Mackevicius (2024), 0.0316 sd per $1,000 (2018 dollars) per pupil sustained
   four years; 90% prediction interval -0.004 to 0.067 [SOURCE: AEJ Applied 16(1), p.413 and p.424,
   Table 2 col 1]. Per pupil-year: divide by four [ASSUMPTION: linear accumulation].
3. Earnings: +12% per sd of test score at age 28, with student and class controls [SOURCE:
   Chetty-Friedman-Rockoff 2014b, NBER WP 19424, p.19; Appendix Table 3, col 3, row 2: $2,585 on a
   mean of $21,622]; sensitivity 1.34% / 0.13 = 10.3% (their value-added estimate, same page).
   Present value of lifetime earnings at age 12, $522,000 in 2010 dollars at a 3% real rate [SOURCE:
   same, p.19 and fn 27], carried to 2024 dollars with CPI-U.
4. Composition (task 2 and symmetry rule 5): within districts, instruction per pupil moves by
   gamma dollars per unit of Hispanic share, enrollment held (compensatory.py panel FY2001-2020).
   The group's presence changes other pupils' instruction by gamma * (h_d - h_d without the group).
5. Class size (teachers) is shown as the same resource loss in another unit and never added.

Group pupils by district: the school-cost lane's Mexican-origin district weights (w_mex_dist, CCD
2023-24 K-12), scaled to the account's 8.487m. Instruction per pupil: F-33 FY2024 (FY2019 in 2024
dollars as a pre-COVID check); districts F-33 does not cover (mostly independent charters) take their
state's group-weighted mean. Writes derived/pricing_*.csv and derived/winners_losers_rows.csv.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/price.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent / "school_cost_where_enrolled_2026_09_24"))
import district_covariates as dc  # noqa: E402
import weighting  # noqa: E402  (school-cost lane: district group-pupil weights; read-only)

OUT = HERE / "derived"
ACCOUNT_GROUP_PUPILS = 8.487e6            # account's transported CPS count (school-cost lane, derived/account_embedded_price.json)
ACCOUNT_RESPONSE = (0.63, 0.66)           # CBO-informed school response, low / high end of the adopted band
ACCOUNT_SCHOOL_LINE_BN = (87.1414, 113.9558)   # adopted main case school step (school-cost lane, engine_school.cjs)
JM = {"low": -0.004, "central": 0.0316, "high": 0.067}   # sd per $1,000 (2018$) per pupil, sustained 4 years
JM_YEARS = 4
CFR_PCT_PER_SD = 0.12
CFR_PCT_PER_SD_VA = 0.0134 / 0.13
CFR_PV_2010 = 522_000.0
PP_BAND = (4_000.0, 80_000.0)
TAX_SHARE = (0.25, 0.35)                  # [ASSUMPTION] combined tax rate on the lost earnings, illustrative
REGION = {**{f: "Northeast" for f in (9, 23, 25, 33, 34, 36, 42, 44, 50)},
          **{f: "Midwest" for f in (17, 18, 19, 20, 26, 27, 29, 31, 38, 39, 46, 55)},
          **{f: "South" for f in (1, 5, 10, 11, 12, 13, 21, 22, 24, 28, 37, 40, 45, 47, 48, 51, 54)},
          **{f: "West" for f in (2, 4, 6, 8, 15, 16, 30, 32, 35, 41, 49, 53, 56)}}


def cpi_calendar():
    c = pd.read_csv(HERE / "_cache" / "cpiaucsl_monthly.csv", parse_dates=["observation_date"])
    return c.groupby(c.observation_date.dt.year).CPIAUCSL.mean()


def pv_per_dollar(jm, pct_per_sd, cpi):
    """PV (2024$, at age 12) of lifetime earnings per 2024 dollar of instruction per pupil-year."""
    sd_per_dollar_2018 = jm / JM_YEARS / 1000.0
    dollars_2018_per_2024 = cpi[2018] / cpi[2024]
    pv_2024 = CFR_PV_2010 * cpi[2024] / cpi[2010]
    return sd_per_dollar_2018 * dollars_2018_per_2024 * pct_per_sd * pv_2024


def districts():
    d, _ = weighting.build()
    d = d.rename(columns={"LEAID": "leaid"})
    d = d[d.k12_all.gt(0)].copy()
    d["G"] = d.w_mex_dist * ACCOUNT_GROUP_PUPILS / d.w_mex_dist.sum()
    d["N"] = d.k12_all
    d["G"] = np.minimum(d.G, 0.99 * d.N)
    d["O"] = d.N - d.G
    d["s"] = d.G / d.N
    d["H"] = np.maximum(d.k12_hisp, d.G)
    p = pd.read_parquet(HERE / "_cache" / "panel.parquet")
    for fy, tag in [(2024, ""), (2019, "_fy19")]:
        q = p[p.year.eq(fy) & p.leaid.ne("") & p.V33.gt(0)].groupby("leaid", as_index=False).first()
        q["instr_support"] = q.pupil_support + q.instr_staff
        for c in ["instruction", "instr_support", "current"]:
            q[c + "_pp" + tag] = q[c] * q.defl_2024 / q.V33
        q = q[(q["current_pp" + tag]).between(*PP_BAND)]
        d = d.merge(q[["leaid"] + [c + "_pp" + tag for c in ["instruction", "instr_support", "current"]]],
                    on="leaid", how="left")
    # uncovered districts take their state's group-weighted mean
    for c in [c for c in d.columns if c.endswith("_pp") or c.endswith("_pp_fy19")]:
        have = d[c].notna()
        state_mean = (d[have].assign(x=d[c] * d.G).groupby("fips").x.sum() / d[have].groupby("fips").G.sum())
        d[c + "_imputed"] = ~have
        d[c] = d[c].fillna(d.fips.map(state_mean))
    pov = dc.saipe(2023)
    d = d.join(pov[["pov_rate"]], on="leaid")
    d["pov_rate"] = d.pov_rate.fillna(d.fips.map(d.groupby("fips").apply(
        lambda g: np.average(g.pov_rate.dropna(), weights=g.N[g.pov_rate.notna()]) if g.pov_rate.notna().any() else np.nan)))
    # national pupil-weighted quintiles of child poverty: Q1 = least poor
    order = d.sort_values("pov_rate")
    cum = order.N.cumsum() / order.N.sum()
    d.loc[order.index, "income_quintile"] = np.minimum(5, (cum * 5).apply(np.ceil)).astype(int)
    d["income_group"] = d.income_quintile.map({1: "Q1 least poor", 2: "Q2", 3: "Q3", 4: "Q4", 5: "Q5 poorest"})
    d["region"] = d.fips.map(REGION)
    return d


def horizons():
    e = pd.read_csv(OUT / "function_elasticities.csv")
    summ = pd.read_csv(OUT / "nonresponse_summary.csv").set_index("spec")
    shares = json.loads((OUT / "function_sample.json").read_text())["fy2000_2019"]["shares_of_current"]
    w_i = shares["instruction"]

    def b(spec, term, func="instruction", col="beta"):
        r = e[e.spec.eq(spec) & e.weight.eq("pupils") & e.term.eq(term) & e.function.eq(func)].iloc[0]
        return float(r[col])

    h = {}
    for split, suffix in [("fd_fy2000_2019", ""), ("dl3_fy2000_2019", "_phi_3yr"), ("ld_stacked_fy2000_2019", "_phi_4_5yr")]:
        phi = float(summ.loc[split, "dilution_share_of_parts"])
        phi_broad = float(summ.loc[split, "dilution_broad_share_of_parts"])
        for tag, r in zip(("account_low_end", "account_high_end"), ACCOUNT_RESPONSE):
            h[tag + suffix] = {"b_instruction": 1 - phi * (1 - r) / w_i, "phi": phi, "response_current": r,
                               "b_instr_support": 1 - (phi_broad - phi) * (1 - r) / shares["instr_support"],
                               "basis": f"account response {r} x instruction share {phi:.3f} of non-response ({split})"}
    for tag, spec, term in [("district_1yr", "fd_fy2000_2019", "dlnN"), ("district_3yr", "dl3_fy2000_2019", "cumulative_3yr"),
                            ("district_4_5yr", "ld_stacked_fy2000_2019", "dlnN"), ("district_19yr", "ld19_2000_2019", "dlnN"),
                            ("district_fe_log", "fe_log_fy2000_2019", "lnN")]:
        h[tag] = {"b_instruction": b(spec, term), "b_instruction_ci_low": b(spec, term, col="ci_low"),
                  "b_instruction_ci_high": b(spec, term, col="ci_high"), "b_instr_support": b(spec, term, "instr_support"),
                  "response_current": b(spec, term, "current"), "basis": f"{spec} pupil-weighted"}
    lv = e[e.spec.eq("fe_level_fy2000_2019") & e.weight.eq("pupils")].set_index("function")
    h["district_fe_level"] = {"b_instruction": float(lv.loc["instruction", "response_ratio"]),
                              "b_instr_support": float(lv.loc["instr_support", "response_ratio"]),
                              "response_current": float(lv.loc["current", "response_ratio"]),
                              "basis": "fe_level_fy2000_2019 response ratio"}
    # state level (CBO's unit; state-year shocks are not absorbed), responses by function
    for tag, spec, term, weight in [("state_cbo_unweighted", "state_cbo_2019", "x", "unweighted"),
                                    ("state_cbo_pupils", "state_cbo_2019", "x", "pupils"),
                                    ("state_ld_19yr", "state_ld_2000_2019", "dlnN", "unweighted")]:
        s = e[e.spec.eq(spec) & e.weight.eq(weight) & e.term.eq(term)].set_index("function").implied_total_response
        h[tag] = {"b_instruction": float(s["instruction"]), "b_instr_support": float(s["instr_support"]),
                  "response_current": float(s["current"]), "basis": f"{spec} {weight} (state panel)"}
    return h


def main():
    cpi = cpi_calendar()
    v = {k: pv_per_dollar(j, CFR_PCT_PER_SD, cpi) for k, j in JM.items()}
    v_va = pv_per_dollar(JM["central"], CFR_PCT_PER_SD_VA, cpi)
    d = districts()
    h = horizons()
    comp = pd.read_csv(OUT / "compensatory_estimates.csv")
    g = comp[comp.design.eq("panel_fy2001_2020") & comp.spec.eq("levels_hisp_lnN") & comp.outcome.eq("instruction")].iloc[0]
    gamma = {"central": float(g.coef_usd_per_pupil_per_unit_share), "low": float(g.ci_low), "high": float(g.ci_high)}

    rows, geo = [], []
    for tag, hz in h.items():
        for price_year, col in [("fy2024", "instruction_pp"), ("fy2019_in_2024usd", "instruction_pp_fy19")]:
            bI = hz["b_instruction"]
            loss_d = (1 - bI) * d[col] * d.G                          # against absence, the account's linear rule
            pow_d = d.O * d[col] * ((1 - d.s) ** (bI - 1) - 1)        # against absence, constant elasticity
            share_d = loss_d * (1 - d.s)                              # against full funding: others' share
            broad_d = (1 - hz["b_instr_support"]) * d[col.replace("instruction", "instr_support")] * d.G
            r = {"horizon": tag, "price_year": price_year, "basis": hz["basis"], "b_instruction": bI,
                 "b_instr_support": hz["b_instr_support"], "response_current": hz["response_current"],
                 "instruction_dilution_bn": loss_d.sum() / 1e9, "instruction_dilution_power_law_bn": pow_d.sum() / 1e9,
                 "instruction_dilution_full_funding_others_bn": share_d.sum() / 1e9,
                 "instruction_dilution_full_funding_group_bn": (loss_d * d.s).sum() / 1e9,
                 "loss_share_in_group_majority_districts": loss_d[d.s > 0.5].sum() / loss_d.sum(),
                 "instr_support_dilution_bn": broad_d.sum() / 1e9,
                 "other_pupils_in_group_districts_m": d.O[d.G > 0].sum() / 1e6,
                 "per_other_pupil_in_group_districts_usd": loss_d.sum() / d.O[d.G > 0].sum(),
                 "per_other_pupil_national_usd": loss_d.sum() / d.O.sum()}
            for k in JM:
                r[f"pv_earnings_bn_jm_{k}"] = loss_d.sum() * v[k] / 1e9
            r["pv_earnings_bn_jm_central_cfr_va"] = loss_d.sum() * v_va / 1e9
            r["pv_earnings_bn_jm_central_power_law"] = pow_d.sum() * v["central"] / 1e9
            r["pv_earnings_bn_jm_central_full_funding_others"] = share_d.sum() * v["central"] / 1e9
            r["pv_per_other_pupil_year_usd_jm_central"] = loss_d.sum() * v["central"] / d.O[d.G > 0].sum()
            rows.append(r)
            if price_year == "fy2024" and tag in ("account_low_end", "account_high_end", "district_19yr"):
                for dim in ("region", "income_group"):
                    for key, grp in d.assign(loss=loss_d, share=share_d).groupby(dim):
                        geo.append({"horizon": tag, "dimension": dim, "group": key,
                                    "other_pupils_m": grp.O.sum() / 1e6, "group_pupils_m": grp.G.sum() / 1e6,
                                    "group_share_of_pupils": grp.G.sum() / grp.N.sum(),
                                    "instruction_dilution_bn": grp.loss.sum() / 1e9,
                                    "per_other_pupil_usd": grp.loss.sum() / grp.O.sum(),
                                    "pv_bn_jm_central": grp.loss.sum() * v["central"] / 1e9,
                                    "pv_bn_jm_low": grp.loss.sum() * v["low"] / 1e9,
                                    "pv_bn_jm_high": grp.loss.sum() * v["high"] / 1e9,
                                    "pv_per_other_pupil_usd_jm_central": grp.loss.sum() * v["central"] / grp.O.sum(),
                                    "pv_bn_jm_central_full_funding_others": grp.share.sum() * v["central"] / 1e9,
                                    "pv_per_other_pupil_usd_full_funding": grp.share.sum() * v["central"] / grp.O.sum()})
    res = pd.DataFrame(rows)
    geo = pd.DataFrame(geo)

    # composition channel: gamma dollars of instruction per pupil per unit Hispanic share
    h_with = d.H / d.N
    h_without = (d.H - d.G) / (d.N - d.G)
    dh = h_with - h_without
    comp_rows = []
    for k, gm in gamma.items():
        change = d.O * gm * dh                     # other pupils' instruction change due to the group's presence
        comp_rows.append({"gamma_case": k, "gamma_usd_per_unit_share": gm, "others_instruction_change_bn": change.sum() / 1e9,
                          "pv_bn_jm_central": change.sum() * v["central"] / 1e9,
                          "pv_bn_jm_low": change.sum() * v["low"] / 1e9, "pv_bn_jm_high": change.sum() * v["high"] / 1e9})
    comp_res = pd.DataFrame(comp_rows)

    # class size: teachers follow pupils with elasticity bT; others' pupil-teacher ratio rises by
    # PTR * [1 - (1 - s)^(1 - bT)]; JM's own benchmark: $1,000 for four years ~ 1.8 fewer pupils per class
    cs = pd.read_csv(OUT / "class_size_elasticities.csv")
    ptr = 16.14                                      # pupil-weighted fall-2018 PTR of the class-size sample
    cls_rows = []
    for _, c in cs[cs.weight.eq("pupils")].iterrows():
        bT = float(c.teacher_elasticity)
        d_ptr = ptr * (1 - (1 - d.s) ** (1 - bT))
        eq_dollars_2018 = d_ptr / 1.8 * 1000.0      # JM p.427-428 equivalence, test scores
        pv = (d.O * eq_dollars_2018 / 1000.0 * JM["central"] / JM_YEARS * CFR_PCT_PER_SD *
              CFR_PV_2010 * cpi[2024] / cpi[2010]).sum()
        cls_rows.append({"spec": c.spec, "teacher_elasticity": bT,
                         "others_ptr_rise_pupils_weighted_mean": float((d.O * d_ptr).sum() / d.O[d.G > 0].sum()),
                         "pv_bn_jm_central_via_class_size": pv / 1e9})
    cls_res = pd.DataFrame(cls_rows)

    OUT.mkdir(exist_ok=True)
    res.to_csv(OUT / "pricing_by_horizon.csv", index=False, lineterminator="\n", float_format="%.6f")
    geo.to_csv(OUT / "pricing_by_region_income.csv", index=False, lineterminator="\n", float_format="%.6f")
    comp_res.to_csv(OUT / "pricing_composition.csv", index=False, lineterminator="\n", float_format="%.6f")
    cls_res.to_csv(OUT / "pricing_class_size.csv", index=False, lineterminator="\n", float_format="%.6f")
    consts = {"pv_per_dollar": v, "pv_per_dollar_cfr_va": v_va, "cpi": {k: float(cpi[k]) for k in (2010, 2018, 2024)},
              "pv_lifetime_earnings_2024usd": CFR_PV_2010 * cpi[2024] / cpi[2010],
              "group_pupils_m": float(d.G.sum() / 1e6), "all_pupils_m": float(d.N.sum() / 1e6),
              "other_pupils_m": float(d.O.sum() / 1e6),
              "group_weighted_instruction_pp_fy2024": float((d.instruction_pp * d.G).sum() / d.G.sum()),
              "group_weighted_current_pp_fy2024": float((d.current_pp * d.G).sum() / d.G.sum()),
              "group_pupils_imputed_price_share": float(d.G[d.instruction_pp_imputed].sum() / d.G.sum()),
              "gamma": gamma}
    (OUT / "pricing_constants.json").write_text(json.dumps(consts, indent=1) + "\n")
    print(json.dumps(consts, indent=1))
    print(res[res.price_year.eq("fy2024")][["horizon", "b_instruction", "instruction_dilution_bn",
                                             "instruction_dilution_power_law_bn", "instr_support_dilution_bn",
                                             "per_other_pupil_in_group_districts_usd", "pv_earnings_bn_jm_low",
                                             "pv_earnings_bn_jm_central", "pv_earnings_bn_jm_high"]].to_string(index=False))
    print(geo.to_string(index=False))
    print(comp_res.to_string(index=False))
    print(cls_res.to_string(index=False))
    wl = winners_losers(d, res, geo, comp_res, cls_res, consts, comp, h, v, dh)
    wl.to_csv(OUT / "winners_losers_rows.csv", index=False, lineterminator="\n", float_format="%.4f")
    print(wl[["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "per_person_usd",
              "relation_to_account"]].to_string(index=False))
    return d, res, geo, comp_res, cls_res, consts


def winners_losers(d, res, geo, comp_res, cls_res, consts, comp, h, v, dh):
    """One row per group x channel; money in $bn a year (present value of lifetime earnings where the
    channel is a human-capital loss). Positive numbers are the stated direction; a negative low end
    means the interval crosses into the opposite direction."""
    src = "infra/immigration-fiscal/school_dilution_2026_09_24/"
    r24 = res[res.price_year.eq("fy2024")].set_index("horizon")
    acc = r24.loc[["account_low_end", "account_high_end"]]
    others = consts["other_pupils_m"]
    rows = []

    def add(group, channel, direction, lo, mid, hi, pop, basis, rel, cf, source):
        rows.append({"group": group, "channel": channel, "direction": direction, "bn_low": lo, "bn_central": mid,
                     "bn_high": hi, "population_m": pop, "per_person_usd": mid * 1e9 / (pop * 1e6) if pop else np.nan,
                     "basis": basis, "relation_to_account": rel, "counterfactual": cf, "source": source})

    cf_acc = ("group's pupils absent; school spending responds at the account's 0.63-0.66 (its linear rule), "
              f"instruction carrying {h['account_low_end']['phi']:.0%} of the non-response (district one-year split); "
              f"{acc.loss_share_in_group_majority_districts.mean():.0%} of it falls in districts where the group is a "
              "majority, where the rule is extrapolated")
    add("other_residents_pupils", "instruction_dilution_account", "loss",
        acc.pv_earnings_bn_jm_low.min(), acc.pv_earnings_bn_jm_central.mean(), acc.pv_earnings_bn_jm_high.max(),
        others, "modelled", "beside", cf_acc,
        src + "price.py -> derived/pricing_by_horizon.csv; JM 2024 p.413/424; CFR 2014b WP p.19, App. Table 3")
    lr = r24.loc["district_19yr"]
    add("other_residents_pupils", "instruction_dilution_long_run", "loss", lr.pv_earnings_bn_jm_low,
        lr.pv_earnings_bn_jm_central, lr.pv_earnings_bn_jm_high, others, "modelled",
        "overlaps:instruction_dilution_account",
        "group's pupils absent; instruction follows pupils at the 19-year within-district response 0.924",
        src + "price.py -> derived/pricing_by_horizon.csv (district_19yr)")
    for dim, label in [("region", "region"), ("income_group", "district child-poverty quintile")]:
        g = geo[geo.dimension.eq(dim) & geo.horizon.isin(["account_low_end", "account_high_end"])]
        for key, grp in g.groupby("group"):
            add(f"other_residents_pupils:{label}={key}", "instruction_dilution_account", "loss", grp.pv_bn_jm_low.min(),
                grp.pv_bn_jm_central.mean(), grp.pv_bn_jm_high.max(), grp.other_pupils_m.iloc[0], "modelled",
                "overlaps:instruction_dilution_account", cf_acc, src + "price.py -> derived/pricing_by_region_income.csv")
    sup = acc.instr_support_dilution_bn
    add("other_residents_pupils", "support_services_dilution_account", "loss", sup.min() * v["low"],
        sup.mean() * v["central"], sup.max() * v["high"], others, "modelled", "beside",
        cf_acc + "; pupil support and instructional staff support, outside the brief's instructional-dollar measure",
        src + "price.py -> derived/pricing_by_horizon.csv (instr_support_dilution_bn)")
    c = comp_res.set_index("gamma_case")
    add("other_residents_pupils", "compensatory_composition", "loss", -c.loc["high", "pv_bn_jm_central"],
        -c.loc["central", "pv_bn_jm_central"], -c.loc["low", "pv_bn_jm_central"], others, "measured",
        "overlaps:instruction_dilution_account",
        "group's pupils absent, enrollment held: within-district effect of Hispanic share on instruction "
        "per pupil (compensatory state and federal money net of the local revenue that falls with it); the "
        "account's response is estimated on enrollment growth that was mostly Hispanic, so it already carries "
        "this; the interval is gamma's 95% CI at JM central",
        src + "compensatory.py -> derived/compensatory_estimates.csv (panel_fy2001_2020); price.py")
    cl = cls_res.set_index("spec")
    add("other_residents_pupils", "class_size_same_resource", "loss", np.nan, cl.loc["ld_2000_2018", "pv_bn_jm_central_via_class_size"],
        cl.loc["ld_2018_2023", "pv_bn_jm_central_via_class_size"], others, "modelled",
        "overlaps:instruction_dilution_account",
        "teachers follow pupils at 0.931 (2000-18) or 0.756 (2018-23); JM's equivalence $1,000 x 4 years = 1.8 pupils per class; never added",
        src + "class_size.py -> derived/class_size_elasticities.csv; price.py -> derived/pricing_class_size.csv")
    add("other_residents_pupils", "peer_effects", "loss", np.nan, np.nan, np.nan, others, "unpriced", "beside",
        "no measured negative US estimate of peer exposure (capacity memo table); Italy's -1.58 pp language score "
        "(CI -3.09 to -0.07, weak first stage) is not transported", "research/immigration-school-capacity-harms-2026-09-20.md")
    # bounded alternatives for other pupils: the constant-elasticity form, and the full-funding split
    add("other_residents_pupils", "instruction_dilution_account_power_law", "loss",
        acc.instruction_dilution_power_law_bn.min() * v["low"], acc.pv_earnings_bn_jm_central_power_law.mean(),
        acc.instruction_dilution_power_law_bn.max() * v["high"], others, "modelled",
        "overlaps:instruction_dilution_account",
        "group's pupils absent; instruction per pupil follows the constant-elasticity form of the same response",
        src + "price.py -> derived/pricing_by_horizon.csv (power law)")
    add("other_residents_pupils", "instruction_dilution_full_funding_share", "loss",
        acc.instruction_dilution_full_funding_others_bn.min() * v["low"],
        acc.pv_earnings_bn_jm_central_full_funding_others.mean(),
        acc.instruction_dilution_full_funding_others_bn.max() * v["high"], others, "modelled",
        "overlaps:instruction_dilution_account",
        "spending that fully follows enrollment at the current district sizes; other pupils bear their district "
        "share (1 - s) of the unfunded instruction", src + "price.py -> derived/pricing_by_horizon.csv (full funding)")
    # the group's own pupils share the same classrooms: against full funding each pupil in a district is short
    # (1 - b) * s * I, so the group's pupils bear share s of the unfunded instruction and other pupils 1 - s
    own = acc.instruction_dilution_full_funding_group_bn
    add("group_pupils", "instruction_dilution_shared", "loss", own.min() * v["low"], own.mean() * v["central"],
        own.max() * v["high"], consts["group_pupils_m"], "modelled", "overlaps:instruction_dilution_account",
        "spending that fully follows enrollment (not the account's counterfactual of absence); the group's pupils "
        "bear their district share s of the unfunded instruction, the same dollars the other-pupil row prices "
        "against absence", src + "price.py -> derived/pricing_by_horizon.csv (full funding)")
    free = [ACCOUNT_SCHOOL_LINE_BN[0] * (1 - ACCOUNT_RESPONSE[0]) / ACCOUNT_RESPONSE[0],
            ACCOUNT_SCHOOL_LINE_BN[1] * (1 - ACCOUNT_RESPONSE[1]) / ACCOUNT_RESPONSE[1]]
    summ = pd.read_csv(OUT / "nonresponse_summary.csv").set_index("spec").loc["fd_fy2000_2019"]
    phi, broad = float(summ["dilution_share_of_parts"]), float(summ["dilution_broad_share_of_parts"])
    for channel, share in [("unfunded_instruction", phi), ("unfunded_instructional_support", broad - phi),
                           ("scale_economies_admin_plant_transport_food", 1 - broad)]:
        add("taxpayers", channel, "gain", min(free) * share, np.mean(free) * share, max(free) * share, np.nan,
            "modelled", "inside",
            f"the account's free 34-37% of the school step (${min(free):.1f}-{max(free):.1f}bn, BEA basis) split by "
            "the district one-year decomposition", src + "decompose.py -> derived/nonresponse_summary.csv")
    panel = comp[comp.design.eq("panel_fy2001_2020") & comp.spec.eq("levels_hisp_lnN")].set_index("outcome")
    val = lambda coef: float((d.N * coef * dh).sum() / 1e9)  # noqa: E731
    for grp, outcome in [("state_taxpayers", "rev_state"), ("federal_taxpayers", "rev_federal")]:
        row = panel.loc[outcome]
        lo, hi = sorted([val(row.ci_low), val(row.ci_high)])
        add(grp, "compensatory_financing", "loss", lo, val(row.coef_usd_per_pupil_per_unit_share), hi, np.nan,
            "measured", "inside",
            "group's pupils absent, enrollment held: within-district change in that revenue per pupil with Hispanic "
            "share; a split by payer of school spending the account already charges, not an addition",
            src + "compensatory.py -> derived/compensatory_estimates.csv")
    loc = panel.loc["rev_local"]
    add("local_taxpayers_in_group_districts", "compensatory_financing", "gain", np.nan, np.nan, np.nan, np.nan,
        "unpriced", "inside",
        f"local revenue per pupil falls {-loc.coef_usd_per_pupil_per_unit_share:,.0f} dollars per unit Hispanic share "
        f"(SE {loc.se:,.0f}), {-val(loc.coef_usd_per_pupil_per_unit_share):.1f}bn at the group's share; lower tax rates "
        "(a gain to local taxpayers) and a smaller tax base per pupil (no gain) are not separable in F-33",
        src + "compensatory.py -> derived/compensatory_estimates.csv")
    base = rows[0]
    add("future_taxpayers", "lower_tax_on_other_pupils_earnings", "loss", base["bn_low"] * TAX_SHARE[0],
        base["bn_central"] * np.mean(TAX_SHARE), base["bn_high"] * TAX_SHARE[1], np.nan, "assumed",
        "overlaps:instruction_dilution_account",
        "decades later, when the affected cohorts work; illustrative 25-35% combined tax rate; the taxes are part of "
        "the gross earnings loss above, and are not added to the annual account", src + "price.py (TAX_SHARE assumption)")
    return pd.DataFrame(rows)


if __name__ == "__main__":
    main()
