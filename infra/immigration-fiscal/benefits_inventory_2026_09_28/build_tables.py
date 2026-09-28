"""Builds derived/items.csv (priced items, cost convention: a benefit is a negative cost) and derived/inventory.csv.

Inputs: derived/capital_surplus_grid.csv (price_capital_surplus.py), the account's production model
(matched_benefits_2026_09_19/model.py) for the foreign-owner sensitivity, the union counts, and the
primary figures below (each with its source). Run from the repo root after price_capital_surplus.py.
"""
import csv
import importlib.util
import pathlib

LANE = pathlib.Path(__file__).resolve().parent
FISCAL = LANE.parent
spec = importlib.util.spec_from_file_location("mb_model", FISCAL / "matched_benefits_2026_09_19/model.py")
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

pop = {r["group"]: r for r in csv.DictReader(open(FISCAL / "crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"))}
N = float(pop["union"]["all_ages"])
ADULT16 = float(pop["union"]["age_18_plus"]) + float(pop["union"]["age_12_17"]) / 3  # ages 16-17 = 2 of 6 years [ASSUMPTION: flat ages]
grid = [r for r in csv.DictReader(open(LANE / "derived/capital_surplus_grid.csv"))
        if r["proxy"] == "PEARNVAL" and r["split"] == "hs_or_less"]
KEYS = ("normalization", "labor_share", "sigma")


def cells(adj, who):
    return {tuple(r[k] for k in KEYS): float(r["increment_PF_over_full_bn"])
            for r in grid if r["who"] == who and float(r["capital_adjustment"]) == adj}


def band(values, ref):
    return min(values), ref, max(values)


items = []


def item(name, measure, lo, c, hi, evidence, dc, note):
    lo, hi = min(lo, hi), max(lo, hi)
    items.append(dict(item=name, group="mexican_origin", measure=measure, low_bn=f"{lo:.4f}", central_bn=f"{c:.4f}",
                      high_bn=f"{hi:.4f}", per_member_usd=f"{c * 1e9 / N:.2f}", evidence_level=evidence,
                      double_count_with=dc, method_note=note))


REF = [("cash", "0.650000", "2.000000"), ("gdp", "0.650000", "2.000000")]  # the grid CSV writes floats as %.6f
DC_CAP = ("production term P+F (the full-adjustment version, inside the account); consumer prices side view (198); "
          "cheaper construction (200); alternatives to each other and to the corporate-tax row")
for adj, name, why in ((0., "capital_owner_surplus_fixed_capital", "capital fixed (short run)"),
                       (.5, "capital_owner_surplus_half_adjustment", "capital half adjusted")):
    u, a = cells(adj, "union"), cells(adj, "average_residents")
    ref = sum(u[k] for k in REF) / 2
    lo, c, hi = band([-v for v in u.values()], -ref)
    item(name, "absolute", lo, c, hi, "modelled: account's own CES model; NAS 2017 formula agrees; frame-inconsistent with the long-run case",
         DC_CAP, f"increment of P+F at capital adjustment {adj} over the adopted 1.0; all capital owned by other residents "
         "(NAS convention); low/high = grid over labour share .60-.70, sigma 1.5-2.5, cash and GDP; central = mean of the two reference cells")
    norm = {k: -u[k] + a[k] for k in u}
    lo, c, hi = band(list(norm.values()), sum(norm[k] for k in REF) / 2)
    item(name, "normalized", lo, c, hi, "modelled", DC_CAP,
         f"absolute less the same increment for as many average residents (12.15% of every earnings pool; {why}); "
         "positive = the union supplies less surplus than average residents")
item("capital_owner_surplus_long_run", "absolute", 0, 0, 0, "theory: NAS 2017 ch. 4 (surplus disappears once K/L is restored)",
     "inside the account at capital adjustment 1.0", "net capital gain is exactly 0 at full adjustment (model.py:50-56); already the account's case")
item("capital_owner_surplus_long_run", "normalized", 0, 0, 0, "theory", "inside the account", "0 for both groups")

# Foreign owners: the fixed-capital gain net of the owners outside the beneficiary set (model's excluded_owner_share).
shares_cells = {}
for r in csv.DictReader(open(FISCAL / "matched_benefits_2026_09_19/derived/skill_composition.csv")):
    if r["proxy"] == "PEARNVAL" and r["split"] == "hs_or_less":
        shares_cells[(r["group"], int(r["skill"]))] = float(r["estimate"])
nat = [shares_cells[("target", k)] + shares_cells[("outside_target", k)] for k in (0, 1)]
sh = [x / sum(nat) for x in nat]
tg = [shares_cells[("target", k)] / nat[k] for k in (0, 1)]
fo = {}
for norm, scale in (("cash", sum(nat) / 1e9 / .65), ("gdp", 29298.)):
    full = mb.fiscal_and_private(mb.equilibrium(sh, tg, 2., .65, 1.), [.384, .426], .246, 1., 0.)
    for x in (0., .10, .20, .40):
        fp = mb.fiscal_and_private(mb.equilibrium(sh, tg, 2., .65, 0.), [.384, .426], .246, 1., x)
        fo[(norm, x)] = (float(fp["private_plus_receipts"]) - float(full["private_plus_receipts"])) * scale
        avg = [N / float(pop["cps_all_civilian"]["all_ages"])] * 2
        fa = mb.fiscal_and_private(mb.equilibrium(sh, avg, 2., .65, 0.), [.384, .426], .246, 1., x)
        fo[("avg_" + norm, x)] = float(fa["private_plus_receipts"]) * scale  # average residents: full-adjustment term is 0
breakeven = {n: fo[(n, 0.)] / (fo[(n, 0.)] - fo[(n, .40)]) * .40 for n in ("cash", "gdp")}
mid = lambda x: (fo[("cash", x)] + fo[("gdp", x)]) / 2
nmid = lambda x: (-fo[("cash", x)] + fo[("avg_cash", x)] - fo[("gdp", x)] + fo[("avg_gdp", x)]) / 2
item("capital_owner_surplus_fixed_capital_net_of_foreign_owners", "normalized", nmid(.10), nmid(.20), nmid(.40),
     "modelled: same assumed foreign shares", "as absolute",
     "absolute less as many average residents' fixed-capital increment at the same excluded owner share")
item("capital_owner_surplus_fixed_capital_net_of_foreign_owners", "absolute", -mid(.10), -mid(.20), -mid(.40),
     "modelled: foreign share of the model's capital income ASSUMED 0.10-0.40 (anchor: foreigners hold ~40% of US corporate equity, Rosenthal-Burke 2020)",
     "capital_owner_surplus_fixed_capital (replaces it when owners abroad are excluded)",
     f"fixed-capital increment with excluded_owner_share 0.10/0.20/0.40 (reference cell, mean of cash and GDP); "
     f"break-even excluded share {breakeven['cash']:.3f} cash / {breakeven['gdp']:.3f} GDP; central 0.20 = 40% of corporate equity x an assumed half of capital income")

# Corporate tax on foreign-owned capital serving the group's jobs, lost when that capital leaves (full adjustment).
CORP = 663.69            # model.json corporate_capital + corporate_labor national, $bn (receipt_side_long_run RESULT line 235)
WAGE_KEY = (.0802, .0748)  # capital serving the group's jobs keyed by its wage share at 48 / 11 (receipt_side_long_run RESULT)
FOREIGN = .40            # Rosenthal & Burke (2020): foreigners hold about 40% of total US equity (2019)
POP_SHARE = N / float(pop["cps_all_civilian"]["all_ages"])
ends = [-CORP * k * FOREIGN for k in WAGE_KEY]
lo, hi = min(ends), 0.
c = sum(ends) / 2 * .5
item("corporate_tax_foreign_owned_capital_serving_group_jobs", "absolute", lo, c, hi,
     "modelled: foreign share measured (40%); US tax retention on relocated capital UNMEASURED (0-1)",
     "receipt_side_long_run_2026_09_28 item 4 (-86.85/-80.98 all owners, lost outright); capital_owner_surplus rows (alternative capital regime)",
     "corporate receipts x the group's wage key (8.02%/7.48% at 48/11) x foreign share 0.40 x (1 - retention); low = retention 0, central = 0.5, high = 1 (the account's rule)")
item("corporate_tax_foreign_owned_capital_serving_group_jobs", "normalized", lo * (1 - POP_SHARE / (sum(WAGE_KEY) / 2)),
     c * (1 - POP_SHARE / (sum(WAGE_KEY) / 2)), 0., "modelled", "as absolute",
     "absolute x (1 - population share 0.1215 / the group's wage key): average residents' jobs carry more capital")

# Formal volunteering reaching residents outside the group.
RATE_H, RATE_ALL = .169, .283          # CEV 2023 formal volunteering, Hispanic / all 16+ (AmeriCorps open data bhmf-84dy; census.gov release)
HOURS, VOLS, VALUE = 4.99e9, 75.7e6, 167.2e9   # americorps.gov 2023: 4.99bn hours by 75.7m volunteers, $167.2bn
gross = ADULT16 * RATE_H * HOURS / VOLS * VALUE / HOURS / 1e9
vol = {s: -gross * s for s in (.4, .55, .7)}   # share of the output reaching non-group residents [ASSUMPTION]
item("formal_volunteering_outside_group", "absolute", vol[.7], vol[.55], vol[.4],
     "speculative: rates measured (CEV 2023); hours per volunteer, $/hour and beneficiary share assumed",
     "none in the account (unpaid work is outside every receipt and spending line)",
     f"union 16+ {ADULT16/1e6:.2f}m x 16.9% x 65.9 h (national mean) x $33.51/h (AmeriCorps value) = ${gross:.2f}bn gross; x non-group share 0.4/0.55/0.7")
f = RATE_ALL / RATE_H - 1
item("formal_volunteering_outside_group", "normalized", -vol[.7] * f, -vol[.55] * f, -vol[.4] * f, "speculative", "as absolute",
     "average residents volunteer at 28.3%: normalized = absolute x (1 - 0.283/0.169), same hours, value and beneficiary share")

cols = ["item", "group", "measure", "low_bn", "central_bn", "high_bn", "per_member_usd", "evidence_level", "double_count_with", "method_note"]
with open(LANE / "derived/items.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(items)
for r in items:
    print(f"{r['item'][:58]:58s} {r['measure']:10s} {r['low_bn']:>9s} {r['central_bn']:>9s} {r['high_bn']:>9s} {r['per_member_usd']:>9s}")
print("foreign-owner cells", {k: round(v, 2) for k, v in fo.items()}, "breakeven", breakeven, "volunteer gross", round(gross, 3), "adult16", ADULT16)

# ---- inventory: every channel, where the account carries it (in_account), evidence and recommendation ----
INV = [
    ("Direct taxes the group pays (income, payroll, sales, excise, customs, motor vehicle, social contributions)", "inside",
     "engine.js:41-44,152-157 (direct_receipt_response 1); model.json receipt cells direct=True", "federal income $128.2bn, payroll $150.6bn, sales $48.8bn (personal allocation)", "measured keys", "nothing: counted"),
    ("Public-good cost sharing: the group's taxes toward defense and existing interest", "inside (implicit credit)",
     "engine.js defaultState public_goods_response 0, interest_response 0, subsidy_response 0; corrections.json meta.responses overrides none of them",
     "defense $854.8bn + interest $1,397.7bn national; at the population share 0.1202 about $270.8bn a year the group is never charged", "convention (CBO category rule); FAQ entry 2", "nothing: already credited; the largest benefit the account carries"),
    ("Complementarity production gain, two skill cells (P) and its induced taxes (F)", "inside",
     "matched_benefits_2026_09_19/model.py:7-106; engine.js:176-183; reference cell in model.json", "P+F $8.8bn cash / $13.3bn GDP (P about -0.2, F +9.0/+13.6)", "modelled, sourced sigma 1.5-2.5", "nothing: counted"),
    ("Imperfect native-immigrant substitution inside cells (nest)", "beside, proposed",
     "ladder 176, 181; winners_losers_2026_09_24 channel table", "+$6.7bn central (5.3-8.0) at eps 3; smaller at the estimated 8.7-17.9", "contested elasticity", "beside: unadopted"),
    ("Capital owners' surplus, capital fixed (short run)", "not inside (grid cell exists, unadopted)",
     "this lane: derived/capital_surplus_grid.csv; model.json dims.capital_adjustment [0,.5,1]", "gain $13.8-26.1bn (central $20.4bn); $22.8bn less than as many average residents; a net loss once over 5.7% of capital income is foreign-owned", "modelled; NAS formula agrees", "beside as an arm only; frame is long run"),
    ("Capital owners' surplus, capital half adjusted", "not inside", "this lane", "gain $3.4-6.4bn (central $5.0bn)", "modelled", "beside"),
    ("Capital owners' surplus, capital adjusted (long run)", "inside at 0", "model.py:50-56; model.json reference capital_adjustment 1.0",
     "0 by construction (released capital earns its rental rate elsewhere)", "theory: NAS 2017 ch. 4", "nothing"),
    ("Corporate and business-property taxes on capital serving the group's jobs (Clemens capital-tax channel)", "beside (response 0)",
     "full_account_2026_09_20/welfare.py:28-31 capital_category; receipt_side_long_run_2026_09_28 item 4",
     "lane 253: gain $81/87bn if lost outright; foreign-owned corporate part gain $0-21.3bn (central $10.3bn at retention 0.5)", "contested: retention unmeasured; foreign share 40% measured", "beside; measure retention before any adoption"),
    ("Group's own capital income and business ownership", "inside for its personal taxes; capital-keyed taxes at 0",
     "model.json: federal_income_tax direct; self-employment earnings in PEARNVAL and self_employment_oasdi_hi; corporate_capital $15.5bn and property on the capital key (3.11%) at response 0; production model excluded_owner_share 0",
     "capital key 3.11% vs population 12.1%", "measured shares", "nothing: no gain to others beyond taxes already counted"),
    ("Property taxes the group pays (owner-occupied, tenant-occupied through rent, personal property)", "candidate (lane 253)",
     "receipt_side_long_run_2026_09_28 items 2-5", "gain $19.05bn owner, $6.81bn tenant, $1.33bn personal property at 48/11", "modelled responses 0.763/0.708", "in progress: do not duplicate"),
    ("Cheaper immigrant-intensive services to consumers (Cortes prices)", "inside P (side view)", "care_household_services_2026_09_23/derived/summary.csv; ladder 198",
     "$21.8bn gross, $11.9bn net of native low-skill wage gains", "measured price elasticities; overlap unreconciled", "nothing: never add beside P"),
    ("Cheaper construction", "inside P", "ladder 200", "costs 0.75% lower (0.53-1.17%); $0 added", "measured job shares, model prices", "nothing"),
    ("Care: taxes on native women's extra hours", "inside (fiscal)", "ladder 198; care lane summary.csv row 1", "+$2.69bn (1.80-5.76)", "measured effect, transported", "nothing: counted"),
    ("Family elder care (fewer Medicaid nursing-facility stays)", "inside (fiscal)", "care lane summary.csv row 3", "+$1.49bn (1.20-7.62)", "modelled", "nothing: counted"),
    ("Housing: landlords' rent gain less renters' loss (long run)", "beside (social item)", "real-costs memo section 3; ladder 190", "+$3.5bn central (-0.4 to +9.4)", "modelled", "nothing: adopted"),
    ("City size and schooling mix (scale)", "being adopted", "scale_spillovers_2026_09_23; ladder 201", "+$13.9bn (-56.6 to +84.4)", "one regression (CRY)", "add (in adoption)"),
    ("Restaurant variety, market size", "being adopted", "disease_food_2026_09_28/derived/items.csv", "gain $6.8bn (1.1-19.2); $1.2bn less than average residents", "modelled", "add (in adoption)"),
    ("Restaurant variety, cuisine composition", "beside", "disease_food_2026_09_28/derived/items.csv", "+$0.6bn central, sign uncertain (-4.7 to +15.4)", "modelled", "beside"),
    ("Mobility: local-shock insurance", "beside", "ladder 203", "+$0.65bn (0.18-2.46)", "measured rates, modelled value", "beside: small"),
    ("Innovation and idea production (patents; Jones semi-endogenous level effect)", "not added", "ladder 201; scale_spillovers_2026_09_23/derived/innovation_bchtt.csv",
     "patent term +$37-57bn inside a +-$490bn interval", "identified interval too wide", "nothing beyond the scenario"),
    ("Fertility and future population", "outside the annual frame", "only income-year 2024 is measured; generation account ladder 224", "n/a", "-", "nothing: lifetime and generation accounts carry it"),
    ("Trade networks (goods; services such as visits by relatives if the lane covers them)", "in progress", "trade_networks_2026_09_28", "in progress", "-", "await the lane"),
    ("Consumer-side scale: variety-adjusted prices, network utilities, media variety", "in progress", "consumer_scale_2026_09_28", "in progress", "-", "await the lane"),
    ("Cultural output", "no dollar line; variety goes to consumer_scale", "ladder 156; cultural_output_2026_09_19",
     "creative labour per head 0.72-0.74 of whites' at matched age, education, sex", "measured", "nothing beyond consumer_scale"),
    ("Military service", "outside the frame", "target_population_cps2025.csv is the CPS civilian universe; active-duty members are not removed", "0", "-", "nothing"),
    ("Charitable giving", "not priced", "BLS CE 2024 cash contributions $911 per Hispanic CU vs $2,292 all (FRED CXUCASHCONTLB1002M, CXUCASHCONTLB0101M); CEV 2023 giving rate 30.9% vs 52.4% non-Hispanic",
     "beneficiary split unmeasured; charity the group receives is an unpriced counter-flow", "measured rates, unmeasured flows", "nothing: net sign unknown, normalized a relative cost"),
    ("Formal volunteering reaching other residents", "beside (priced here)", "this lane derived/items.csv; CEV 2023", "gain $6.2bn (4.5-7.9); $4.2bn less than average residents", "speculative", "beside: do not add"),
    ("Informal helping of neighbours", "not priced", "CEV 2023: 43.3% vs 56.6% non-Hispanic", "no hours measured", "measured rates", "nothing"),
    ("Pay-as-you-go support: payroll taxes financing current retirees", "inside (cash); accrual arm nets future benefits", "ladder 257; pension_accrual_2026_09_28", "payroll receipts $150.6bn; accrual +$73.6-77.3bn cost", "measured", "nothing"),
    ("Payroll taxes of unauthorized workers never claimed", "inside, scaled to on-books share", "ladder 254; payroll_compliance_2026_09_28", "nets about 0 at 48/11", "modelled", "nothing: 254 carries it"),
    ("Government enterprises' surplus, including public housing", "inside (option D)", "main_case_long_run_2026_09_27 RESULT", "+$5.56bn at response 1", "measured", "nothing"),
    ("Cheaper public purchases of group-intensive work (public construction, contracted services)", "inside P by aggregation", "ladder 200 logic (one-good output)", "public share of the 0.75%", "modelled", "nothing"),
    ("Remittances", "neither cost nor benefit", "real-costs memo section 8", "-", "-", "nothing"),
]
with open(LANE / "derived/inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["channel", "in_account", "where", "size", "evidence", "recommendation"])
    w.writerows(INV)
print("inventory rows", len(INV))
