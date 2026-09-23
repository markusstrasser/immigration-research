#!/usr/bin/env python3
"""Native women's induced hours, their taxes, and the consumer-price side view, union frame.

Channels (RESULT.md "Overlap ruling"):
  * taxes on native women's extra market hours: ADDS to the fiscal account (first order; the
    account's central holds native hours fixed and its 0.33 grid arm responds to own wages only)
  * the extra hours' output gain to other factors and the taxes on it: ADDS, computed in the
    account's own CES (second order; reported to show it is negligible)
  * consumer surplus on cheaper services (2026-09-18 Part A) and the native low-skill wage
    offset: INSIDE P, re-run in the union frame as a side view only

Two estimates of the hours response, alternatives (never added):
  CT  Cortés–Tessada (2011) metro IV, 1980-2000: weekly hours | H>0 of women in the top quartile
      of the female wage distribution (by census division) per unit of
      L = ln[(no-diploma immigrants + no-diploma natives) / labour force]
  EV  East–Velásquez (2024) Secure Communities: hours elasticity of US-born college mothers of
      young children with respect to the household-service price, applied to the Cortés (2008)
      price response to ln(no-diploma immigrants / labour force)

Everything is evaluated metro by metro (services are local; both papers identify off metro
variation) and, for comparison, on national totals. The group's ACS counts are scaled to the
CPS union (40,896,574) as in the housing and congestion lanes.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/hours_tax.py
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
D = HERE / "derived"
FISCAL = ROOT / "infra/immigration-fiscal"
XWALK = FISCAL / "employment_entry_2026_09_18/_cache/xwalk_puma22.csv"
COUNTY_CBSA = FISCAL / "hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv"
LANE_0918 = FISCAL / "consumer_price_benefit_2026_09_18"
MODEL = FISCAL / "matched_benefits_2026_09_19/model.py"
SKILL = FISCAL / "matched_benefits_2026_09_19/derived/skill_composition.csv"

CPS_UNION = 40_896_574
ACS_TOTAL_POP = 340_110_988
OTHERS = ACS_TOTAL_POP - CPS_UNION
FLOOR = 0.05  # a metro keeps at least 5% of its low-skill count (log-linear models break at 0)

# The account's labour tax rates (matched_benefits_2026_09_19/README.md): current federal,
# state and payroll marginal rates from Colas–Sachs Table 1 (2017 components), some college+;
# .366 nets out discounted future Social Security accrual (a different fiscal object).
TAU = {"account_current": 0.426, "account_net_future_ss": 0.366}
TAU_0918 = 0.35  # the 2026-09-18 lane's "high earner buildup", comparability only

# Cortés–Tessada 2011, AEJ Applied 3(3):88-123 (coef, SE); usual weekly hours | H>0,
# top quartile (75-100) of the female hourly-wage distribution.
CT = {
    "t7_iv_additional": (2.068, 0.754),   # Table 7, IV, additional controls
    "t7_iv_basic": (2.375, 0.735),        # Table 7, IV, basic controls
    "t10_female_x_L": (0.479, 0.106),     # Table 10 A(1): L x female, men as control group
    "t10_female_x_L_cityfe": (0.468, 0.105),  # Table 10 A(2): with city x decade effects
}
# Share of the Table 7 effect attributed to household-service prices.
MECH = {
    "all_channels": 1.0,                        # upper: every channel
    "ev_fathers_comparison": 0.90,              # East–Velásquez Table 10 B: -0.379/-0.421
    "ev_childless_women_comparison": 0.72,      # East–Velásquez Table 10 A: -0.302/-0.421
}
# East–Velásquez: hours of US-born college mothers of children under 5, SC effect -0.421
# (SE 0.169) = -1.46%; household-service wage +6.5%; elasticity -0.23 if all of the hours
# change is price-driven; C-T x Cortés equivalent -0.15 (their p.33).
# (name, elasticity, relative SE of the hours effect, ACS population, metro weight column)
EV_SPECS = [
    ("ev_mothers_all_price", -0.23, 0.169 / 0.421, "ev_college_mothers_u6_native_nonunion", "ev_earn"),
    ("ev_mothers_x0.90", -0.23 * 0.90, 0.169 / 0.421, "ev_college_mothers_u6_native_nonunion", "ev_earn"),
    ("ev_mothers_x0.72", -0.23 * 0.72, 0.169 / 0.421, "ev_college_mothers_u6_native_nonunion", "ev_earn"),
    # price proxy = wage of ALL female household-service workers (+2.0%, SE 1.3, n.s.): -1.46/2.0
    ("ev_mothers_price_all_female_wage", -1.46 / 2.0, 0.169 / 0.421,
     "ev_college_mothers_u6_native_nonunion", "ev_earn"),
    # all US-born college women 20-63: SC -0.114 (SE 0.071) = -0.34%, over +6.5%
    ("ev_all_college_women", -0.34 / 6.5, 0.071 / 0.114, "ev_college_women_all_native_nonunion",
     "ev_all_earn"),
]
# Cortés 2008 (JPE 116(3)), price of immigrant-intensive services per unit ln(LSI/LF): 10%
# more share lowers prices 2% (published) or 1.3% (2005 working paper); beta = ln(1-x)/ln(1.1),
# the 2026-09-18 lane's conversion.
CORTES_BETA = {"jpe_2008_2pct": float(np.log(0.98) / np.log(1.1)),
               "wp_2005_1.3pct": float(np.log(0.987) / np.log(1.1))}


def load_model():
    spec = importlib.util.spec_from_file_location("account_model", MODEL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def national() -> dict[str, float]:
    nat = pd.read_csv(D / "acs_national.csv")
    return dict(zip(nat["item"], nat["estimate"]))


def areas(scale: float) -> pd.DataFrame:
    """PUMA cells -> CBSA (metro) or non-metro remainder of each state, by population share."""
    if not XWALK.exists():
        raise SystemExit(f"[BLOCKED] missing {XWALK}; run employment_entry_2026_09_18/fetch_crosswalks.py")
    cells = pd.read_csv(D / "acs_puma_cells.csv", dtype={"STATE": str, "PUMA": str})
    xw = pd.read_csv(XWALK, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    geo = pd.read_csv(COUNTY_CBSA, dtype=str)
    geo = geo[geo["is_metro"] == "1"][["county_fips", "cbsa", "cbsa_title"]]
    xw = xw.merge(geo, left_on="county", right_on="county_fips", how="left")
    xw["area"] = xw["cbsa"].fillna("nonmetro_" + xw["state"])
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    merged = cells.merge(alloc, left_on=["STATE", "PUMA"], right_on=["state", "puma"], how="left",
                         validate="one_to_many")
    if merged["area"].isna().any():
        raise SystemExit("[BLOCKED] PUMAs without crosswalk rows")
    value_cols = [c for c in cells.columns if c not in ("STATE", "PUMA")]
    for c in value_cols:
        merged[c] = merged[c] * merged["afact"]
    out = merged.groupby("area")[value_cols].sum()
    for c in value_cols:
        if not np.isclose(out[c].sum(), cells[c].sum(), rtol=1e-9):
            raise SystemExit(f"[BLOCKED] allocation lost {c}")
    titles = xw.dropna(subset=["cbsa"]).drop_duplicates("cbsa").set_index("cbsa")["cbsa_title"]
    out["title"] = out.index.map(titles)

    def dlog(num, num_u, den, den_u):
        """Change in ln(num/den) when the group leaves; 0 where num is 0 (nothing to remove)."""
        num, num_u, den, den_u = (np.asarray(x, float) for x in (num, num_u, den, den_u))
        keep = np.maximum(num - scale * num_u, FLOOR * num)
        pos = num > 0
        out = np.zeros_like(num)
        out[pos] = (np.log(keep[pos] / (den[pos] - scale * den_u[pos]))
                    - np.log(num[pos] / den[pos]))
        return out, pos & ((num - scale * num_u) < FLOOR * num)

    out["dL_ct"], out["ct_floor_hit"] = dlog(out.ct_ls, out.ct_ls_union, out.ct_lf, out.ct_lf_union)
    out["dC_cortes"], out["cortes_floor_hit"] = dlog(out.c08_lsi, out.c08_lsi_union, out.c08_lf,
                                                     out.c08_lf_union)
    out["dL_ct_lf_fixed"], _ = dlog(out.ct_ls, out.ct_ls_union, out.ct_lf, 0 * out.ct_lf_union)
    out["union_share_scaled"] = scale * out.pop_union / out["pop"]
    return out


def ces_triangle(model, delta_high: float, sigma: float, adjustment: float):
    """Gain to all other factors from delta_high more high-skill efficiency labour.

    Current (with the group) economy normalised to one; the counterfactual removes the extra
    hours. Returns $bn for income and for the account's tax partition (cash normalisation).
    """
    sk = pd.read_csv(SKILL)
    sk = sk[(sk.proxy == "PEARNVAL") & (sk.split == "hs_or_less") & (sk.group == "national")]
    earn = sk.sort_values("skill")["estimate"].to_numpy(float)
    shares = earn / earn.sum()
    s = 0.65
    res = model.equilibrium(shares, np.array([0.0, delta_high]), sigma=sigma, labor_share=s,
                            adjustment=adjustment, elasticity=0.0)
    fp = model.fiscal_and_private(res, [0.384, 0.426], 0.246, 1.0)
    scale = earn.sum() / s / 1e9
    return {"gross_income_gain_bn": float(res["gross_income_gain"]) * scale,
            "labor_tax_gain_bn": float(fp["labor_tax_gain"]) * scale,
            "capital_tax_gain_bn": float(fp["capital_tax_gain"]) * scale,
            "receipts_gain_bn": float(fp["current_receipts_gain"]) * scale,
            "high_skill_earnings_bn": float(earn[1]) / 1e9}


def main() -> None:
    nat = national()
    women = pd.read_csv(D / "acs_women.csv").set_index("population")
    acs_union = nat["pop_union"]
    scale_cps = CPS_UNION / acs_union
    model = load_model()

    # ---------------------------------------------------------------- shocks
    shock_rows, area_frames = [], {}
    for scaling, k in (("cps_scaled", scale_cps), ("acs_unscaled", 1.0)):
        ar = areas(k)
        area_frames[scaling] = ar
        ls, lsu = nat["ct_ls_other_fb"] + nat["ct_ls_other_nat"] + nat["ct_ls_union_fb"] + nat["ct_ls_union_nat"], \
            nat["ct_ls_union_fb"] + nat["ct_ls_union_nat"]
        lf, lfu = nat["ct_lf_all"], nat["ct_lf_union"]
        lsi, lsiu, lf8, lf8u = nat["c08_lsi_all"], nat["c08_lsi_union"], nat["c08_lf_all"], nat["c08_lf_union"]
        rec = {
            "scaling": scaling, "scale": k,
            "ct_L_before": np.log(ls / lf),
            "ct_dL_national": np.log((ls - k * lsu) / (lf - k * lfu)) - np.log(ls / lf),
            "ct_dL_national_lf_fixed": np.log((ls - k * lsu) / ls),
            "ct_dL_metro_w_women_hours": float(np.average(ar.dL_ct, weights=ar.ct_value_hour)),
            "ct_dL_metro_w_women_hours_lf_fixed": float(np.average(ar.dL_ct_lf_fixed, weights=ar.ct_value_hour)),
            "ct_dL_metro_w_population": float(np.average(ar.dL_ct, weights=ar["pop"])),
            "cortes_share_before": lsi / lf8,
            "cortes_dC_national": np.log((lsi - k * lsiu) / (lf8 - k * lf8u)) - np.log(lsi / lf8),
            "cortes_dC_metro_w_mothers_earnings": float(np.average(ar.dC_cortes, weights=ar.ev_earn)),
            "cortes_dC_metro_w_college_women_earnings": float(np.average(ar.dC_cortes,
                                                                         weights=ar.ev_all_earn)),
            "cortes_dC_metro_w_other_population": float(np.average(
                ar.dC_cortes, weights=ar["pop"] - k * ar.pop_union)),
            "areas": len(ar), "areas_ct_floor_hit": int(ar.ct_floor_hit.sum()),
            "areas_cortes_floor_hit": int(ar.cortes_floor_hit.sum()),
            "union_ls_share_of_ls": k * lsu / ls,
            "union_lsi_share_of_lsi": k * lsiu / lsi,
        }
        shock_rows.append(rec)
    shocks = pd.DataFrame(shock_rows)
    shocks.to_csv(D / "shock_summary.csv", index=False)
    ar = area_frames["cps_scaled"]
    ar[["title", "pop", "union_share_scaled", "ct_ls", "ct_ls_union", "ct_lf", "ct_lf_union",
        "dL_ct", "c08_lsi", "c08_lsi_union", "c08_lf", "dC_cortes", "ct_value_hour", "ev_earn",
        "ct_floor_hit", "cortes_floor_hit"]].sort_values("pop", ascending=False).to_csv(
        D / "metro_shocks.csv")

    # ---------------------------------------------------------------- CT arm
    pops = {
        "native_nonunion": women.loc["ct_topq_div_native_nonunion", "value_one_weekly_hour_bn"],
        "native_plus_foreign_nonunion": (women.loc["ct_topq_div_native_nonunion", "value_one_weekly_hour_bn"]
                                         + women.loc["ct_topq_div_foreign_nonunion", "value_one_weekly_hour_bn"]),
    }
    ct_combos = [(t, m) for t in ("t7_iv_additional", "t7_iv_basic") for m in MECH] + \
        [(t, "service_channel_lower_bound") for t in ("t10_female_x_L", "t10_female_x_L_cityfe")]
    rows = []
    for _, sh in shocks.iterrows():
        shock_opts = {"metro_weighted": sh.ct_dL_metro_w_women_hours,
                      "national": sh.ct_dL_national,
                      "metro_weighted_lf_fixed": sh.ct_dL_metro_w_women_hours_lf_fixed,
                      "national_lf_fixed": sh.ct_dL_national_lf_fixed}
        for theta_name, mech_name in ct_combos:
            theta, se = CT[theta_name]
            mshare = MECH.get(mech_name, 1.0)
            for shock_name, dL in shock_opts.items():
                for pop_name, v_bn in pops.items():
                    dh = theta * mshare * dL  # weekly hours, negative on removal
                    earn = -dh * v_bn         # earnings with the group present, $bn
                    lo = -(theta - 1.96 * se) * mshare * dL * v_bn
                    hi = -(theta + 1.96 * se) * mshare * dL * v_bn
                    rec = dict(arm="CT", coefficient=theta_name, coef=theta, coef_se=se,
                               attribution=mech_name, attribution_share=mshare, shock=shock_name,
                               scaling=sh.scaling, dL=dL, population=pop_name,
                               value_one_weekly_hour_bn=v_bn, d_hours_week_on_removal=dh,
                               earnings_bn=earn, earnings_lo95_bn=lo, earnings_hi95_bn=hi)
                    for tn, t in TAU.items():
                        rec[f"tax_bn_{tn}"] = t * earn
                        rec[f"tax_lo95_bn_{tn}"] = t * lo
                        rec[f"tax_hi95_bn_{tn}"] = t * hi
                    rows.append(rec)
    # ---------------------------------------------------------------- EV arm
    for _, sh in shocks.iterrows():
        for ename, eps, rel_se, pop_name, wcol in EV_SPECS:
            ev_earn = women.loc[pop_name, "earnings_bn"]
            metro = (sh.cortes_dC_metro_w_mothers_earnings if wcol == "ev_earn"
                     else sh.cortes_dC_metro_w_college_women_earnings)
            for shock_name, dC in (("metro_weighted", metro), ("national", sh.cortes_dC_national)):
                for bname, beta in CORTES_BETA.items():
                    dlnp = beta * dC  # household-service price on removal (positive)
                    dlnh = eps * dlnp
                    earn = -(np.exp(dlnh) - 1.0) * ev_earn
                    rec = dict(arm="EV", coefficient=ename, coef=eps, coef_se=abs(eps) * rel_se,
                               attribution="in_elasticity", attribution_share=np.nan,
                               shock=shock_name, scaling=sh.scaling, dL=dC,
                               population=pop_name,
                               price_beta=bname, price_rise_on_removal=float(np.exp(dlnp) - 1),
                               value_one_weekly_hour_bn=np.nan, d_hours_week_on_removal=np.nan,
                               pct_hours_on_removal=float(np.exp(dlnh) - 1), earnings_bn=earn,
                               earnings_lo95_bn=earn * (1 - 1.96 * rel_se),
                               earnings_hi95_bn=earn * (1 + 1.96 * rel_se))
                    for tn, t in TAU.items():
                        rec[f"tax_bn_{tn}"] = t * earn
                        rec[f"tax_lo95_bn_{tn}"] = t * rec["earnings_lo95_bn"]
                        rec[f"tax_hi95_bn_{tn}"] = t * rec["earnings_hi95_bn"]
                    rows.append(rec)
    specs = pd.DataFrame(rows)
    specs["tax_per_group_member"] = specs["tax_bn_account_current"] * 1e9 / CPS_UNION
    specs["tax_per_other_resident"] = specs["tax_bn_account_current"] * 1e9 / OTHERS
    specs.to_csv(D / "hours_tax_specs.csv", index=False)

    # ---------------------------------------------------------------- CES triangle
    tri_rows = []

    def pick(**where):
        sel = specs
        for col, val in where.items():
            sel = sel[sel[col] == val]
        if len(sel) != 1:
            raise SystemExit(f"[BLOCKED] expected one spec for {where}, got {len(sel)}")
        return sel.iloc[0]

    common = dict(shock="metro_weighted", scaling="cps_scaled")
    chosen = {
        "central_ct_service_channel": pick(arm="CT", coefficient="t10_female_x_L",
                                           population="native_nonunion", **common),
        "check_ev_mothers": pick(arm="EV", coefficient="ev_mothers_x0.90", price_beta="jpe_2008_2pct",
                                 **common),
        "upper_ct_all_channels": pick(arm="CT", coefficient="t7_iv_basic", attribution="all_channels",
                                      population="native_plus_foreign_nonunion", **common),
    }
    base_high = ces_triangle(model, 0.0, 2.0, 1.0)["high_skill_earnings_bn"]
    for label, row in chosen.items():
        delta = row.earnings_bn / base_high
        for sigma in (1.5, 2.0, 2.5):
            for adj in (0.0, 0.5, 1.0):
                tri = ces_triangle(model, delta, sigma, adj)
                tri_rows.append(dict(hours_spec=label, extra_earnings_bn=row.earnings_bn,
                                     delta_high_efficiency=delta, sigma=sigma,
                                     capital_adjustment=adj, **tri))
    tri = pd.DataFrame(tri_rows)
    tri.to_csv(D / "ces_output_triangle.csv", index=False)

    # ---------------------------------------------------------------- Part A side view
    exp = pd.read_csv(LANE_0918 / "derived/expenditure_map.csv")
    aud = json.loads((LANE_0918 / "derived/compute_audit.json").read_text())
    q = ["q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest"]
    ncu = aud["native_consumer_units"]
    e_int = {c: exp.loc[exp.tier == "intensive", c].sum() for c in q}
    e_nt = {c: exp.loc[exp.tier == "nontraded", c].sum() for c in q}
    base_wage = pd.read_csv(LANE_0918 / "derived/native_lowskill_base.csv").set_index("group")
    nat_drop_earn = float(base_wage.loc["native_dropout_employed", "aggregate_earnings_bn"])
    b_wage_nat = float(np.log(1 - 0.006) / np.log(1.1))
    arows = []
    sh0 = shocks[shocks.scaling == "cps_scaled"].iloc[0]
    shock_a = {"sept18_mexborn_dropouts_lf_adjusted": aud["dln_share_lf_adjusted"],
               "union_national": sh0.cortes_dC_national,
               "union_metro_w_other_population": sh0.cortes_dC_metro_w_other_population}
    for arm, b_int in (("jpe_2008_2pct", CORTES_BETA["jpe_2008_2pct"]),
                       ("wp_2005_1.3pct", CORTES_BETA["wp_2005_1.3pct"])):
        b_nt = float(np.log(1 - 0.002) / np.log(1.1))
        for sname, dln in shock_a.items():
            pr_int, pr_nt = np.exp(b_int * dln) - 1, np.exp(b_nt * dln) - 1
            narrow = sum(e_int[c] * pr_int * ncu[c] for c in q) / 1e9
            broad = narrow + sum(e_nt[c] * pr_nt * ncu[c] for c in q) / 1e9
            wage = nat_drop_earn * (np.exp(b_wage_nat * dln) - 1)
            arows.append(dict(price_arm=arm, shock=sname, dln_share=dln,
                              price_rise_intensive=pr_int, consumer_loss_narrow_bn=narrow,
                              consumer_loss_broad_bn=broad, native_dropout_wage_gain_bn=wage,
                              net_narrow_bn=narrow - wage))
    side = pd.DataFrame(arows)
    side.to_csv(D / "partA_side_view_union_frame.csv", index=False)

    # ---------------------------------------------------------------- Sept 18 Part B, corrected
    b18 = pd.read_csv(LANE_0918 / "derived/partB_hours_results.csv")
    pub = b18[(b18.population == "topq_native_college_women") &
              (b18.arm == "hours_given_working_addl_controls") & (b18.shock == "lf_adjusted")].iloc[0]
    w18 = pd.read_csv(LANE_0918 / "derived/women_top_quartile.csv").set_index("group")
    v18 = (w18.loc["topq_native_college_women", "count"] * w18.loc["topq_native_college_women", "mean_weeks"]
           * w18.loc["topq_native_college_women", "aggregate_hourly_wage"] / 1e9)
    # the 09-18 women's population at the corrected regressor and coefficient, national shock
    dl_nat = float(sh0.ct_dL_national)
    corr = []
    corr.append(dict(step="published_2026_09_18", coef=pub.beta_hours_per_logpoint, dL=pub.dln_share,
                     value_one_weekly_hour_bn=v18, earnings_bn=pub.earnings_change_bn,
                     tax_bn=pub.tax_bn_high_earner_buildup, tax_rate=TAU_0918))
    for coef_name in ("t7_iv_additional", "t10_female_x_L"):
        theta = CT[coef_name][0]
        e = -theta * dl_nat * v18
        corr.append(dict(step=f"regressor_L_union_national_{coef_name}", coef=theta, dL=dl_nat,
                         value_one_weekly_hour_bn=v18, earnings_bn=e, tax_bn=TAU_0918 * e,
                         tax_rate=TAU_0918))
        corr.append(dict(step=f"regressor_L_union_national_{coef_name}_account_tau", coef=theta,
                         dL=dl_nat, value_one_weekly_hour_bn=v18, earnings_bn=e,
                         tax_bn=TAU["account_current"] * e, tax_rate=TAU["account_current"]))
    pd.DataFrame(corr).to_csv(D / "sept18_partB_correction.csv", index=False)

    # ---------------------------------------------------------------- console
    pd.set_option("display.width", 220)
    print("[shocks]")
    print(shocks.T.to_string())
    key = specs[(specs.scaling == "cps_scaled") & (specs.shock == "metro_weighted") &
                (specs.population.isin(["native_nonunion", "ev_college_mothers_u6_native_nonunion",
                                        "ev_college_women_all_native_nonunion"]))]
    cols = ["arm", "coefficient", "attribution", "price_beta", "dL", "earnings_bn", "earnings_lo95_bn",
            "earnings_hi95_bn", "tax_bn_account_current", "tax_lo95_bn_account_current",
            "tax_hi95_bn_account_current", "tax_bn_account_net_future_ss"]
    print("\n[hours and taxes, CPS-scaled union, metro-weighted shock]")
    print(key[cols].to_string(index=False))
    print("\n[CES output triangle]")
    print(tri.to_string(index=False))
    print("\n[Part A side view, union frame]")
    print(side.to_string(index=False))
    print("\n[Sept 18 Part B correction]")
    print(pd.DataFrame(corr).to_string(index=False))


if __name__ == "__main__":
    main()
