"""Reconcile independent fixes and conditional stacks on the preserved P7 baseline.

Native-First: existing producer CSV/JSON contracts. No shared consumer mutation.
All monetary columns are signed costs to other residents, $bn in 2024 dollars.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from respending import load_air, read_csv, spending_basis_gate, hard_gate, verify_pins, verify_bundle, publish_bundle, csv_text, dependency_snapshot
from respending import BUNDLE_DEPENDENCIES
from valuation_registry import mortality_registry

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"


def one(rows, **keys):
    xs = [r for r in rows if all(float(r[k]) == float(v) if k == "real_discount_rate" else r[k] == str(v)
                                 for k,v in keys.items())]
    hard_gate(len(xs) == 1, f"unique producer row {keys}: {len(xs)}")
    return xs[0]


def main():
    verify_pins()
    source_generation = verify_bundle("respending")
    dependencies = dependency_snapshot(OUT, BUNDLE_DEPENDENCIES["stack"])
    base = read_csv(HERE / "inputs/baseline_totals_oct14.csv")
    frozen_social = json.loads((FISCAL / "sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.json").read_text())["lineage_social_rows"]["rows"]
    def original_gross(item, end):
        row = one(frozen_social, item=item)
        return float(row[f"union_before_boundary_{end}_bn"])*(1+float(row[f"share_{end}"]))
    components = read_csv(OUT / "spending_components.csv")
    bands = read_csv(HERE / "inputs/band_variants.csv")
    case = json.loads((OUT / "case_inputs.json").read_text())
    context = json.loads((FISCAL / "air_pollution_2026_09_28/derived/mortality_context.json").read_text())
    mort = read_csv(FISCAL / "air_pollution_2026_09_28/derived/mortality_items.csv")
    crashes = read_csv(FISCAL / "road_crash_externality_2026_09_28/derived/capacity_items_oct15.csv")
    crime_mortality = read_csv(FISCAL / "social_costs_unpriced_2026_09_28/derived/oct15/mortality_pairing_rows.csv")
    volunteers = read_csv(FISCAL / "benefits_inventory_2026_09_28/derived/volunteering_flows.csv")
    taxes = read_csv(FISCAL / "benefits_inventory_2026_09_28/derived/city_tax_decomposition.csv")
    rp = {r["parameter"]:float(r["central"]) for r in read_csv(FISCAL / "disease_food_2026_09_28/derived/inputs.csv")}
    rest_base=float(one(read_csv(FISCAL / "disease_food_2026_09_28/derived/items.csv"),item="restaurant_variety_market_size",measure="absolute")["central_bn"])
    psi=rp["share_of_non_group_restaurant_access_supported_by_group"]
    sig=rp["sigma_between_restaurants"]
    rest_expenditure=-rest_base/((1-psi)**(-1/(sig-1))-1)
    cm = context["row4"]
    air = load_air()
    morb = air.ARMS["morbidity"][1]
    factor = context["lineage_fixed_boundary"]["factor"]
    old_pm = original_gross("pm25_consumption", "low")
    hard_gate(abs(old_pm-original_gross("pm25_consumption", "high"))<1e-9, "common frozen PM sender level")
    baseline = {end: float(one(base,column="pairing_on_priced_count",item=f"published pairing ({end})")["oct14"])
                for end in ["low","high"]}
    hard_gate(abs(baseline["low"]-439.435316)<1e-6 and abs(baseline["high"]-532.847640)<1e-6, "frozen baseline pairing")
    raw = one(bands,case="oct14",variant="justice_raw_coding")
    adopted = one(bands,case="oct14",variant="adopted")
    # The social pairing changes only the low end's justice footing. Justice is
    # current services, so its cost difference changes current H one for one.
    pairing_H_delta = float(raw["cost_low_bn"])-float(adopted["cost_low_bn"])
    uniform = one(mort,item="pm25_consumption_mortality",population_basis="lineage_fixed_boundary")
    fixes, stacks = [], []
    for end in ["low","high"]:
        cr = next(r for r in case["rows"] if r["population_basis"]=="lineage" and r["end"]==end)
        Hmain = cr["current_budget_saving_bn"]
        Hpair = Hmain+(pairing_H_delta if end=="low" else 0)
        for denom in ["CE","PCE"]:
            comp=one(components,population_basis="lineage",end=end,spending_denominator=denom)
            # Task 1 alone keeps the old exposure/population receiver assumption.
            task1=float(comp["pm_respending_bn"])*Hpair/Hmain+float(comp["government_mirror_bn"])
            for task,arm,delta,note in [
                ("1","respending_plus_old_government_mirror",task1,"all H spent; marginal mix unmeasured; current low-end justice footing respected"),
                ("2","mortality_self_share",float(uniform["central_bn"])-old_pm,"common NVSS age rates; ACS receiver ages; original source attribution held"),
                ("7","city_size_tax",0.0,"induced taxes already inside the adopted city earnings row"),
            ]:
                fixes.append(dict(task=task,arm=arm,end=end,spending_denominator=denom,delta_bn=delta,
                                  changed_pairing_bn=baseline[end]+delta,over_5bn=abs(delta)>5,note=note))
            # Life-year readings live only in the joint three-channel grid.
            # A PM-only change to a baseline with legacy crime/crash values is
            # not a coherent mortality valuation arm.
            for arm in ["all_density","multivehicle_only"]:
                crash=one(crashes,population="lineage_gross",arm=arm,end=end,valuation="dot_uniform",real_discount_rate=0)
                delta=float(crash["change_bn"])
                fixes.append(dict(task="4",arm=arm,end=end,spending_denominator=denom,delta_bn=delta,
                                  changed_pairing_bn=baseline[end]+delta,over_5bn=abs(delta)>5,note="fixed identified-union recipient boundary; full lineage source-road-key extrapolation"))
            for proxy,d in itertools.product(["primary_food","any_food"],["0.0","0.5","1.0"]):
                v=one(volunteers,year="2024",frame="lineage_key_extrapolation",food_task_proxy=proxy,displacement=d)
                delta=float(v[f"{end}_end_delta_bn"])
                fixes.append(dict(task="5",arm=f"{proxy}_displacement_{d}",end=end,spending_denominator=denom,delta_bn=delta,
                                  changed_pairing_bn=baseline[end]+delta,over_5bn=abs(delta)>5,note="measured household food-use share; received volunteer hours and displacement are proxies/assumptions"))
            for valuation,rate in [("uniform","0"),("VSLY","0"),("VSLY","0.03")]:
                pm=uniform if valuation=="uniform" else one(mort,item="pm25_consumption_mortality_vsly",population_basis="lineage_fixed_boundary",real_discount_rate=rate)
                basis = "dot_uniform" if valuation == "uniform" else "dot_life_years"
                crime = one(crime_mortality,end=end,valuation=basis,real_discount_rate=rate)
                pm_delta=float(pm["central_bn"])-old_pm
                # New emission source is nationally mixed. Use the national
                # remaining-receptor age distribution, not local source sigma.
                unit_key="uniform_harm_per_spending_usd" if valuation=="uniform" else f"national_other_vsly_harm_per_spending_usd_r{float(rate)}"
                unit=float(cm[unit_key])*cm["without_group_receiver_fraction_fixed_geography"]
                if denom=="PCE":
                    unit*=cm["national_ce_spending_usd"]/1e9/float(comp["national_spending_bn"])
                spending_basis_gate(comp["funding_accounting_basis"], comp["denominator_accounting_basis"],
                                    units_sensitivity=denom == "CE")
                resp=-Hpair*unit
                gov=cm["government_use_mortality_adjusted_bn"]*case["lineage"]["lineage_population"]/case["lineage"]["account_union"]
                if valuation=="VSLY":
                    # Keep morbidity dollars fixed; transform mortality only.
                    from_air=float(cm[f"mean_outsider_vsl_usd_r{float(rate)}"])
                    gov=(cm["government_use_mortality_bn"]*from_air/air.VSL_DOT_2024 +
                         cm["government_use_morbidity_bn"])*case["lineage"]["lineage_population"]/case["lineage"]["account_union"]
                for crash_arm,proxy,d,demand,boundary in itertools.product(["all_density","multivehicle_only"],["primary_food","any_food"],["0.0","0.5","1.0"],[False,True],["identified_union","lineage_exchangeable"]):
                    exchange=boundary=="lineage_exchangeable"
                    receiver_factor=context["lineage_fixed_boundary"]["exchangeable_added_receiver_factor"] if exchange else 1.0
                    crash_row=one(crashes,population="lineage" if exchange else "lineage_gross",arm=crash_arm,end=end,
                                  valuation=basis,real_discount_rate=rate)
                    registry = mortality_registry(basis,rate,dict(crime=crime,pm25=pm,road_crash=crash_row))
                    crash=float(crash_row["central_bn"])-original_gross("road_crash_externality", end)
                    pm_delta_bound=float(pm["central_bn"])*receiver_factor-old_pm
                    vol=float(one(volunteers,year="2024",frame="lineage_key_extrapolation",food_task_proxy=proxy,displacement=d)[f"{end}_end_delta_bn"])
                    # Demand response is an explicit effective-demand arm. It
                    # does not assert that spending restores absent customers.
                    rest_new=-rest_expenditure*((1-psi*(1-Hpair/float(comp["group_spending_bn"])))**(-1/(sig-1))-1)
                    demand_delta=(rest_new-rest_base+float(comp["consumer_scale_demand_arm_bn"])*Hpair/Hmain) if demand else 0
                    crime_delta=float(crime["replacement_lineage_victim_bn"])-float(crime["published_pre_round1_lineage_victim_bn"])
                    delta=pm_delta_bound+resp*receiver_factor+gov*receiver_factor+crash+vol+demand_delta+crime_delta
                    stacks.append(dict(end=end,spending_denominator=denom,mortality_valuation=valuation,real_discount_rate=rate,
                                       funding_accounting_basis=comp["funding_accounting_basis"],
                                       denominator_accounting_basis=comp["denominator_accounting_basis"],units_sensitivity=denom == "CE",
                                       crash_arm=crash_arm,volunteering_proxy=proxy,displacement=d,market_demand_arm=demand,pm_crash_recipient_boundary=boundary,
                                       mortality_registry_json=json.dumps(registry,sort_keys=True),
                                       baseline_bn=baseline[end],budget_saving_at_pairing_bn=Hpair,
                                       mortality_delta_bn=pm_delta_bound,respending_bn=resp*receiver_factor,government_mirror_bn=gov*receiver_factor,
                                       pm_gross_replacement_bn=float(pm["central_bn"])*receiver_factor,
                                       crash_replacement_bn=float(crash_row["central_bn"]),
                                       crash_delta_bn=crash,volunteering_delta_bn=vol,market_demand_delta_bn=demand_delta,
                                       crime_mortality_delta_bn=crime_delta,
                                       crime_delta_from_current_P7_bn=float(crime["lineage_victim_delta_bn"]),
                                       city_tax_increment_bn=0.0,stack_delta_bn=delta,stack_pairing_bn=baseline[end]+delta,
                                       status=f"conditional source-key lineage extension; PM/crash receiver boundary {boundary}; other channels held; not an adopted total"))
    tax=one(taxes,frame="lineage_key_extrapolation")
    hard_gate(float(tax["low_end_delta_bn"])==float(tax["high_end_delta_bn"])==0, "city taxes already included")
    for s in stacks:
        terms=[s[k] for k in ["mortality_delta_bn","respending_bn","government_mirror_bn","crash_delta_bn","volunteering_delta_bn","market_demand_delta_bn","city_tax_increment_bn","crime_mortality_delta_bn"]]
        hard_gate(abs(sum(terms)-s["stack_delta_bn"])<1e-9, "stack component closure")
        hard_gate(abs(s["stack_pairing_bn"]-s["baseline_bn"]-sum(terms))<1e-9, "stack baseline closure")
    hard_gate(source_generation==verify_bundle("respending"), "source generation stable through stack")
    integration = json.dumps(dict(
        comparator="2024 removal, frozen P7 baseline $439.435316/$532.847640bn; personal endpoints; all other social channels fixed",
        warning="No unconditional stack identified. Source-key lineage extensions have explicit PM/crash recipient-boundary arms. Parent's outside-lineage receiver corrections to other channels are separate; do not apply PM/crash correction twice.",
        components="one_fix_deltas are isolated; conditional_stacks reprice the spending/mortality interaction and replace legacy crime victims under the same three-channel basis; PM-only life-year pseudo-pairings removed; CO2 excluded; demand and displacement explicit",
        fiscal_pairing_low_current_budget_adjustment_bn=pairing_H_delta,
        funding="cash available in 2024 for both cash and accrual totals; capital and accrued pensions excluded; all-spent conditional",
        central=dict(spending_denominator="PCE",crash_arm="multivehicle_only",mortality_valuation="uniform"),
        gates=dict(baseline_pairing=True,unique_producer_keys=True,city_tax_no_double_count=True,stack_closure_1e9=True,accounting_basis_contract=True,mortality_registry=True),
        counts=dict(independent_fix_rows=len(fixes),conditional_stack_rows=len(stacks))),indent=2)+"\n"
    publish_bundle("stack", {"one_fix_deltas.csv":csv_text(fixes),"conditional_stacks.csv":csv_text(stacks),
                             "integration.json":integration}, dependencies=dependencies)
    print(f"{len(fixes)} one-fix rows; {len(stacks)} conditional stack rows; closure PASS")


if __name__=="__main__":
    main()
