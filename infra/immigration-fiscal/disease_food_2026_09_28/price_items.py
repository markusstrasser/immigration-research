"""Price the infectious-disease and food channels of the Mexican-origin union (2024 $).

Every input is declared once in PARAMS with its low / central / high value and a source tag;
items.csv is derived from them, inputs.csv records them.  Absolute = with the group against
without it; normalized = against the same number of average residents (definition per item in
the method_note).  Costs are positive, benefits negative.
"""
import csv
import math
from pathlib import Path

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
OUT = LANE / "derived"

# ---------------------------------------------------------------- shared constants
POP = {r["group"]: float(r["all_ages"]) for r in csv.DictReader(
    open(FISCAL / "crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"))}
N_G = POP["union"]                      # 40,896,574
N_US = POP["cps_all_civilian"]          # 336,727,803
POP_SHARE = N_G / N_US
VSL = 13.7e6                            # US DOT 2024, as in crime_victim_cost_2026_09_23
VSLY = VSL / sum(1.03 ** -t for t in range(1, 41))   # 40-year annuity at 3%
CPI = {2014: 236.736, 2020: 258.811, 2023: 304.702, 2024: 313.689}  # BLS CUUR0000SA0 annual

INPUTS = []


def p(name, low, central, high, tag):
    INPUTS.append((name, low, central, high, tag))
    return {"low": low, "central": central, "high": high}


# ---------------------------------------------------------------- TB
tb = dict(
    mexborn_cases=p("tb_mexico_born_cases_2024", 1307, 1307, 1307, "[SOURCE] CDC TB in the US 2024, top-30 birth countries"),
    usb_hisp_cases=p("tb_us_born_hispanic_cases_2024", 663, 663, 663, "[SOURCE] CDC TB in the US 2024, race-ethnicity US-born"),
    mex_share_usb_hisp=p("mexican_origin_share_of_us_born_hispanic_cases", 0.60,
                         (POP["mexican_second_gen"] + POP["mexican_third_plus_selfid"]) / (663 / 1.6e-5), 0.80,
                         "[CALCULATION] CPS US-born Mexican-origin / (663 cases / 1.6 per 100k); range [INFERENCE]"),
    k_foreign=p("secondary_per_case_mexico_born", 0.054, 0.075, 0.136,
                "[SOURCE] Yuen 2016 Table 1: foreign-born limited 5.4%, all recent 7.5%; high = Hispanic 13.6%"),
    k_usborn=p("secondary_per_case_us_born_hispanic", 0.150, 0.274, 0.274,
               "[SOURCE] Yuen 2016 Table 1: US-born limited 15.0%, all recent 27.4%"),
    phi_out=p("share_of_secondary_cases_outside_group", 0.10, 0.20, 0.35,
              "[INFERENCE] assortative mixing (Yuen aPRs; mixed-cluster shares MA 2002, RI 2011); not measured"),
    rho=p("later_reactivation_per_recent_case", 0.10, 0.25, 0.50,
          "[INFERENCE] most progression within 2 years of infection (Behr et al. 2018 BMJ) [TRAINING-DATA]"),
    mdr_share=p("mdr_share_of_cases", 0.0, 0.015, 0.03, "[INFERENCE] US MDR ~1% of culture-confirmed cases"),
    prod_nonfatal=p("nonfatal_productivity_loss_usd", 3000, 3000 * CPI[2024] / CPI[2014], 6000,
                    "[SOURCE] Castro 2016: societal excl. death $20k - direct $17k (2014$)"),
    qaly_loss=p("qaly_loss_per_surviving_case", 0.10, 0.25, 0.50,
                "[INFERENCE] acute + post-TB sequelae; Menzies 2021 Lancet GH [TRAINING-DATA]"),
    cfr=p("tb_attributable_case_fatality", 0.03, 0.05, 0.065,
          "[SOURCE] Castro 2016: 6.48% = 72% x 9%; secondary cases younger -> lower [INFERENCE]"),
    national_cases=p("tb_all_cases_2024", 10388, 10388, 10388, "[SOURCE] CDC TB in the US 2024, origin-birth"),
    national_k=p("recent_transmission_share_all_cases", 0.14, 0.14, 0.14, "[SOURCE] Yuen 2016"),
)
DS_2020, MDR_2020 = 20000, 182000        # [SOURCE] CDC 'Costly Burden of DR TB' (2020 $) direct cost


def tb_arm(a):
    v = {k: d[a] for k, d in tb.items()}
    g_cases = v["mexborn_cases"] + v["mex_share_usb_hisp"] * v["usb_hisp_cases"]
    secondary = (v["mexborn_cases"] * v["k_foreign"]
                 + v["mex_share_usb_hisp"] * v["usb_hisp_cases"] * v["k_usborn"])
    out_cases = secondary * v["phi_out"] * (1 + v["rho"])
    medical = ((1 - v["mdr_share"]) * DS_2020 + v["mdr_share"] * MDR_2020) * CPI[2024] / CPI[2020]
    per_case = (medical + v["prod_nonfatal"] + (1 - v["cfr"]) * v["qaly_loss"] * VSLY + v["cfr"] * VSL)
    absolute = out_cases * per_case
    # normalized: same mixing, source intensity per head of the group vs the average resident
    src_g = secondary / N_G
    src_avg = v["national_cases"] * v["national_k"] / N_US
    return dict(group_cases=g_cases, secondary=secondary, out_cases=out_cases, per_case=per_case,
                medical=medical, absolute=absolute, normalized=absolute * (1 - src_avg / src_g),
                norm_factor=1 - src_avg / src_g)


TB = {a: tb_arm(a) for a in ("low", "central", "high")}

# ---------------------------------------------------------------- measles, hepatitis A, Chagas, NCC
me = dict(
    imports=p("measles_importations_from_mexico_per_year", 2, 5, 20,
              "[SOURCE] MMWR 74(14): 7 of 48 Jan-Apr 2025 importations from Mexico; annualised range [INFERENCE]"),
    spread=p("share_of_importations_with_secondary_cases", 0.31, 0.31, 0.31, "[SOURCE] MMWR 74(14): 15 of 48"),
    sec=p("secondary_cases_per_spreading_importation", 1, 3, 5, "[INFERENCE]"),
    out=p("measles_share_outside_group", 0.2, 0.3, 0.5, "[INFERENCE] contacts mostly household/community"),
    cost=p("measles_cost_per_case_usd", 30000, 50000, 80000,
           "[INFERENCE] medical + 1-3/1,000 deaths x VSL; public-health response is fiscal"),
)
ha = dict(
    travel=p("hepA_travel_cases_per_year", 157, 250, 350,
             "[SOURCE] CDC surv. manual ch.3: 21% of 748 cases with info (2023); upper [INFERENCE]"),
    mex=p("hepA_share_travel_to_mexico", 0.3, 0.5, 0.7,
          "[SOURCE] CDC SS 2007: 85% Mexico+Central/South America; Mexico alone [INFERENCE]"),
    grp=p("hepA_share_travellers_in_group", 0.4, 0.6, 0.8, "[INFERENCE] visiting friends and relatives"),
    sec=p("hepA_secondary_non_group_per_case", 0.02, 0.05, 0.10, "[INFERENCE] household spread; vaccinated cohorts"),
    cost=p("hepA_cost_per_case_usd", 30000, 60000, 120000, "[INFERENCE] hospitalisation ~40-60%, CFR <1%"),
)
ch = dict(
    tests=p("first_time_donor_tests_per_year", 1.5e6, 2.0e6, 2.5e6,
            "[SOURCE] 9.1m first-time donations 2007-15 in the ARC-led study (Transfusion 2019); national [INFERENCE]"),
    price=p("tcruzi_test_cost_usd", 4, 7, 10, "[INFERENCE] reagent + labour + supplemental testing"),
    attrib=p("share_of_screening_attributable_to_group", 0.0, 0.5, 1.0,
             "[SOURCE] Custer 2012: Mexico-born 32/89 confirmed positives, US-born 25/89; attribution [INFERENCE]"),
    grp_pos=p("group_share_of_seropositive_donors", 0.5, 0.5, 0.5, "[INFERENCE] 36% Mexico-born + half of US-born"),
)
ncc = dict(
    new=p("ncc_new_cases_per_year", 1320, 2500, 5050, "[SOURCE] Serpa & White 2014 review (PMC4005108)"),
    local=p("ncc_share_locally_acquired", 0.05, 0.07, 0.10, "[SOURCE] LA County 10/138 = 7%; 7-10% (Oregon EID 2011)"),
    nonhisp=p("ncc_share_of_local_cases_not_hispanic", 0.3, 0.3, 0.3, "[SOURCE] LA County: 70% Hispanic"),
    src=p("ncc_share_of_carriers_in_group", 0.4, 0.55, 0.7, "[INFERENCE] Mexico share of Latin American-born"),
    cost=p("ncc_cost_per_case_usd", 100000, 250000, 500000,
           "[SOURCE] mean charge $48.9k (EID 21(6)); QoL (epilepsy) + rare death [INFERENCE]"),
)


def simple(arms, f):
    return {a: f({k: d[a] for k, d in arms.items()}) for a in ("low", "central", "high")}


MEASLES = simple(me, lambda v: v["imports"] * v["spread"] * v["sec"] * v["out"] * v["cost"])
HEPA = simple(ha, lambda v: v["travel"] * v["mex"] * v["grp"] * v["sec"] * v["cost"])
CHAGAS = simple(ch, lambda v: v["tests"] * v["price"] * v["attrib"])
NCC = simple(ncc, lambda v: v["new"] * v["local"] * v["nonhisp"] * v["src"] * v["cost"])
S_TB = p("public_tb_control_spending_usd", 135e6, 400e6, 700e6,
         "[SOURCE] CDC domestic TB $135m (FY2019-21); state/local share [INFERENCE]")
CASE_SHARE = TB["central"]["group_cases"] / 10388

# ---------------------------------------------------------------- food safety
cooks = {r["group"]: float(r["share"]) for r in csv.DictReader(
    open(FISCAL / "cultural_output_2026_09_19/derived/arm_d_cooks_shares.csv"))
    if r["state"] == "US" and r["occupation"] == "all_food_prep_serving"}
grp_kitchen = cooks["MEXBORN"] + cooks["USMEX"]
fs = dict(
    burden=p("foodborne_illness_cost_2024_usd", 74.7e9 * CPI[2024] / CPI[2023], 74.7e9 * CPI[2024] / CPI[2023],
             74.7e9 * CPI[2024] / CPI[2023], "[SOURCE] USDA ERS 2025 update, $74.7bn (2023$)"),
    rest=p("restaurant_share_of_burden", 0.25, 0.40, 0.55,
           "[INFERENCE] 56% of outbreaks restaurant (Angelo 2017); sporadic share unknown"),
    diners=p("non_group_share_of_restaurant_meals", 0.90, 0.90, 0.90, "[INFERENCE] group ~9-10% of FAFH"),
    lam=p("group_share_of_kitchen_labour", 0.12, grp_kitchen, 0.205,
          "[DATA] cultural_output arm_d_cooks_shares (ACS): all food prep 16.9%; chefs & cooks 20.5%"),
    e=p("excess_illness_risk_in_group_staffed_kitchens", 0.0, 0.05, 0.20,
        "[INFERENCE] 0 = Jones 2004 null; 0.20 = whole LA grade-card effect (Jin-Leslie); violations x1.56 (Kwon 2010)"),
)
FOOD = simple(fs, lambda v: v["burden"] * v["rest"] * v["diners"] * v["lam"] * v["e"])

# ---------------------------------------------------------------- variety
dec = list(csv.DictReader(open(FISCAL / "cultural_output_2026_09_19/derived/arm_d_share_deciles.csv")))
pop_cov = sum(float(r["pop_total"]) for r in dec)
D1 = sum(float(r["mex_rest_total"]) for r in dec) / pop_cov * 1e5
N_ALL = sum(float(r["all_per_100k_pooled"]) * float(r["pop_total"]) for r in dec) / pop_cov
D_LOWEST = float(dec[0]["mex_per_100k_pooled"])
E_722 = p("restaurant_sales_2024_usd", 1144e9, 1144e9, 1144e9,
          "[SOURCE] Census advance monthly retail, NAICS 722 total 2024 = $1,144.4bn")
E_CEX = p("household_fafh_cex_2024_usd", 3944.94 * 134.6e6, 3944.94 * 134.6e6, 3944.94 * 134.6e6,
          "[SOURCE] CEX 2024 FAFH $3,944.94/CU (consumer-price memo) x 134.6m CUs [TRAINING-DATA count]")
SPEND_SHARE = p("group_share_of_restaurant_spending", 0.09, 0.10, 0.11, "[INFERENCE] lower income, larger CUs; UNVERIFIED")
sig = p("sigma_between_restaurants", 10.0, 8.8, 6.1, "[SOURCE] Couture 2016 8.8; Su (MPRA 113158) 6.1-8.7")
m_ng = p("non_group_mexican_share_of_restaurant_spend", 0.05, 0.07, 0.09, "[INFERENCE] Mexican ~11% of OSM restaurants")
d0 = p("mexican_restaurants_per_100k_without_group", D_LOWEST, 4.0, 2.0,
       "[DATA] lowest-decile metros 6.93/100k; 2.0 if the national Mexican-origin cook supply is also removed [INFERENCE]")
psi = p("share_of_non_group_restaurant_access_supported_by_group", 0.02, 0.05, 0.09,
        "[INFERENCE] group spending share 0.10 discounted for consumption segregation")


def composition(m, D0, s, E):
    g = (m * math.log(D1 / D0) + (1 - m) * math.log((N_ALL - D1) / (N_ALL - D0))) / (s - 1)
    return -(math.exp(g) - 1) * E        # benefit to others -> negative cost


grid = [composition(m, D0, s, E)
        for m in (0.05, 0.07, 0.09) for D0 in (D_LOWEST, 5.466, 4.0, 2.0)
        for s in (6.1, 8.8, 10.0) for E in (0.9 * E_CEX["central"], 0.9 * E_722["central"])]
COMP = {"central": composition(m_ng["central"], d0["central"], sig["central"], 0.9 * E_722["central"]),
        "low": min(grid), "high": max(grid)}   # low = largest benefit (most negative cost)


def scale(ps, s, E):
    return -((1 - ps) ** (-1 / (s - 1)) - 1) * E


SCALE = {"low": scale(psi["high"], sig["high"], 0.9 * E_722["central"]),
         "central": scale(psi["central"], sig["central"], 0.9 * E_722["central"]),
         "high": scale(psi["low"], sig["low"], 0.9 * E_CEX["central"])}
SCALE_NORM = SPEND_SHARE["central"] / POP_SHARE - 1   # vs average residents' restaurant spending

# ---------------------------------------------------------------- write
rows = []


def add(item, measure, lo, ce, hi, ev, dc, note):
    if not math.isnan(lo):
        lo, hi = min(lo, hi), max(lo, hi)     # a negative normalizing factor flips the arms
    rows.append(dict(item=item, group="mexican_origin", measure=measure,
                     low_bn=f"{lo / 1e9:.4f}", central_bn=f"{ce / 1e9:.4f}", high_bn=f"{hi / 1e9:.4f}",
                     per_member_usd=f"{ce / N_G:.2f}", evidence_level=ev, double_count_with=dc, method_note=note))


def both(item, d, nf, ev, dc, note_a, note_n):
    add(item, "absolute", d["low"], d["central"], d["high"], ev, dc, note_a)
    add(item, "normalized", d["low"] * nf, d["central"] * nf, d["high"] * nf, ev, dc, note_n)


tb_ev = "modelled: measured case counts x assumed cross-group transmission share; contested"
tb_dc = "fiscal account medical keys (group's own treatment); crime victim cost (none)"
add("tb_secondary_cases_outside_group", "absolute", TB["low"]["absolute"], TB["central"]["absolute"],
    TB["high"]["absolute"], tb_ev, tb_dc,
    f"(Mexico-born + Mexican-origin US-born Hispanic cases) x recent-transmission yield x outside share x "
    f"(1+later reactivation) x (medical + productivity + QoL x VSLY + CFR x VSL); central "
    f"{TB['central']['out_cases']:.0f} outside cases/yr at ${TB['central']['per_case']:,.0f}")
add("tb_secondary_cases_outside_group", "normalized", TB["low"]["normalized"], TB["central"]["normalized"],
    TB["high"]["normalized"], tb_ev, tb_dc,
    f"absolute x (1 - average resident's per-head source intensity / group's), same mixing; factor "
    f"{TB['central']['norm_factor']:.3f}")
both("measles_importation_spread", MEASLES, 0.5, "measured importation counts; negligible",
     "public-health response (fiscal)", "Mexico-sourced importations x spread x outside share x cost/case",
     "absolute x 0.5 [INFERENCE: no evidence the group lowers measles immunity]")
both("hepatitis_a_travel_secondary", HEPA, 0.7, "measured travel share; negligible", "food safety (handler cases)",
     "travel cases x Mexico share x group share x non-group secondary x cost/case",
     "absolute x 0.7 [INFERENCE]; imported-produce outbreaks excluded (trade, not residents)")
both("chagas_blood_screening", CHAGAS, 1 - POP_SHARE / 0.5, "modelled: assumed volume, price and attribution",
     "none (blood-centre cost passed to hospitals and patients)",
     "one-time donor tests x price x attribution (0 if screening would exist anyway)",
     "absolute x (1 - population share / group share of positive donors 0.5)")
both("neurocysticercosis_local_transmission", NCC, 1 - 0.65 / 2.5, "modelled: surveillance shares; negligible",
     "fiscal medical keys (group's own cases)", "new NCC cases x locally acquired x non-Hispanic x group carrier x cost",
     "absolute x (1 - all-population/Hispanic hospitalisation rate 0.65/2.5)")
add("covid19", "absolute", float("nan"), float("nan"), float("nan"), "not priced: unidentified",
    "every health item", "each 1% of other residents' 2020-22 COVID deaths = ~7,800 deaths = ~$107bn one-off; sign unknown")
both("food_safety_group_staffed_kitchens", FOOD, 1 - grp_kitchen, "speculative: violations do not map to illness",
     "hepatitis A (handler cases); consumer-price channel (none)",
     "ERS burden x restaurant share x non-group diners x group kitchen-labour share x excess risk",
     "absolute x (1 - group share of kitchen labour): excess over the average kitchen")
add("restaurant_variety_composition", "absolute", COMP["low"], COMP["central"], COMP["high"],
    "modelled: published sigma, assumed nest shares; sign uncertain",
    "consumer-price channel (prices, not variety); cultural_output_2026_09_19 (no dollar line)",
    f"nested CES, Cobb-Douglas across cuisine: Mexican density {D1:.2f}->D0 per 100k, others crowd in (total "
    f"{N_ALL:.1f}/100k fixed, placebo); low/high = min/max of 72-cell grid")
add("restaurant_variety_composition", "normalized", COMP["low"], COMP["central"], COMP["high"],
    "modelled: published sigma, assumed nest shares; sign uncertain",
    "consumer-price channel (prices, not variety); cultural_output_2026_09_19 (no dollar line)",
    "equal to absolute: average residents bring the average cuisine mix")
add("restaurant_variety_market_size", "absolute", SCALE["low"], SCALE["central"], SCALE["high"],
    "modelled: published sigma, assumed access share; generic scale effect",
    "scale_spillovers_2026_09_23 (production side); congestion_2026_09_23 (cost side of density)",
    "CES variety loss for non-group diners if the group's restaurant demand vanished: E x ((1-psi)^(-1/(sigma-1))-1)")
add("restaurant_variety_market_size", "normalized", SCALE["low"] * SCALE_NORM, SCALE["central"] * SCALE_NORM,
    SCALE["high"] * SCALE_NORM, "modelled: generic scale effect", "as absolute",
    f"absolute x (group spending share / population share - 1) = x{SCALE_NORM:.3f}: fewer restaurants per head")
add("food_prices", "absolute", 0, 0, 0, "cross-check only", "research/immigration-consumer-price-and-native-hours-2026-09-18.md",
    "already in the consumer-price channel (food away from home in scope A) and the production term; not added")
add("produce_quality_farm_labour", "absolute", 0, 0, 0, "no evidence found", "consumer-price channel; production term",
    "no study links farm labour supply to produce quality; Bracero exclusion moved crop mix and mechanisation")
add("tb_control_key_correction", "absolute", CASE_SHARE * S_TB["low"], CASE_SHARE * S_TB["central"],
    CASE_SHARE * S_TB["high"], "measured case share x assumed spending", "FISCAL, not a social item",
    f"group share of TB cases {CASE_SHARE:.3f} x public TB-control spending")
add("tb_control_key_correction", "normalized", (CASE_SHARE - POP_SHARE) * S_TB["low"],
    (CASE_SHARE - POP_SHARE) * S_TB["central"], (CASE_SHARE - POP_SHARE) * S_TB["high"],
    "measured case share x assumed spending", "FISCAL, not a social item",
    f"candidate key correction: (case share {CASE_SHARE:.3f} - population share {POP_SHARE:.3f}) x spending")

OUT.mkdir(exist_ok=True)
with open(OUT / "items.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: ("" if v == "nan" or v == "-nan" else v) for k, v in r.items()})
with open(OUT / "inputs.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["parameter", "low", "central", "high", "tag_source"])
    w.writerows(INPUTS)
with open(OUT / "tb_detail.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["arm", "group_cases", "secondary_cases_all", "outside_cases", "medical_usd", "per_case_usd",
                "absolute_bn", "normalized_bn"])
    for a, d in TB.items():
        w.writerow([a, f"{d['group_cases']:.1f}", f"{d['secondary']:.1f}", f"{d['out_cases']:.1f}",
                    f"{d['medical']:.0f}", f"{d['per_case']:.0f}", f"{d['absolute'] / 1e9:.4f}",
                    f"{d['normalized'] / 1e9:.4f}"])

COSTS = ("tb_secondary_cases_outside_group", "measles_importation_spread", "hepatitis_a_travel_secondary",
         "chagas_blood_screening", "neurocysticercosis_local_transmission", "food_safety_group_staffed_kitchens")
DISEASE = COSTS[:5]
with open(OUT / "totals.csv", "w", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["total", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd", "note"])
    for name, members in (("disease", DISEASE), ("disease_plus_food_safety", COSTS)):
        for meas in ("absolute", "normalized"):
            sel = [r for r in rows if r["item"] in members and r["measure"] == meas]
            s = [sum(float(r[c]) for r in sel) for c in ("low_bn", "central_bn", "high_bn")]
            w.writerow([name, meas, f"{s[0]:.4f}", f"{s[1]:.4f}", f"{s[2]:.4f}", f"{s[1] * 1e9 / N_G:.2f}",
                        "sum of arms (stacked lows / highs, not a confidence interval); excludes variety, "
                        "prices, COVID-19 and the fiscal key correction"])
            print(f"TOTAL {name:26s} {meas:10s} {s[0]:.4f} {s[1]:.4f} {s[2]:.4f} ${s[1] * 1e9 / N_G:.2f}")

print(f"N_G={N_G:,.0f} pop_share={POP_SHARE:.4f} VSLY={VSLY:,.0f} D1={D1:.2f} N_ALL={N_ALL:.1f} "
      f"D_lowest={D_LOWEST:.2f} kitchen={grp_kitchen:.3f} case_share={CASE_SHARE:.3f}")
for r in rows:
    print(f"{r['item']:40s} {r['measure']:10s} {r['low_bn']:>9s} {r['central_bn']:>9s} {r['high_bn']:>9s} "
          f"${r['per_member_usd']:>8s}")
