"""Reconcile independent fixes and conditional stacks on the preserved P7 baseline.

Native-First: existing producer CSV/JSON contracts. No shared consumer mutation.
All monetary columns are signed costs to other residents, $bn in 2024 dollars.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

from respending import load_air, read_csv, write_csv

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"


def one(rows, **keys):
    xs = [r for r in rows if all(r[k] == str(v) for k,v in keys.items())]
    assert len(xs) == 1, (keys,len(xs))
    return xs[0]


def main():
    base = read_csv(HERE / "inputs/baseline_totals_oct14.csv")
    components = read_csv(OUT / "spending_components.csv")
    bands = read_csv(HERE / "inputs/band_variants.csv")
    case = json.loads((OUT / "case_inputs.json").read_text())
    context = json.loads((FISCAL / "air_pollution_2026_09_28/derived/mortality_context.json").read_text())
    mort = read_csv(FISCAL / "air_pollution_2026_09_28/derived/mortality_items.csv")
    crashes = read_csv(FISCAL / "road_crash_externality_2026_09_28/derived/capacity_items.csv")
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
    old_pm = cm["live_original_union_bn"] * factor
    baseline = {end: float(one(base,column="pairing_on_priced_count",item=f"published pairing ({end})")["oct14"])
                for end in ["low","high"]}
    assert abs(baseline["low"]-439.435316)<1e-6 and abs(baseline["high"]-532.847640)<1e-6
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
            for rate in ["0","0.03"]:
                v=one(mort,item="pm25_consumption_mortality_vsly",population_basis="lineage_fixed_boundary",real_discount_rate=rate)
                delta=float(v["central_bn"])-old_pm
                fixes.append(dict(task="3",arm=f"VSLY_{rate}",end=end,spending_denominator=denom,delta_bn=delta,
                                  changed_pairing_bn=baseline[end]+delta,over_5bn=abs(delta)>5,note="alternative mortality valuation, never added to uniform-VSL fix"))
            for arm in ["all_density","multivehicle_only"]:
                crash=one(crashes,population="lineage_gross",arm=arm,end=end)
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
                pm_delta=float(pm["central_bn"])-old_pm
                # New emission source is nationally mixed. Use the national
                # remaining-receptor age distribution, not local source sigma.
                unit_key="uniform_harm_per_spending_usd" if valuation=="uniform" else f"national_other_vsly_harm_per_spending_usd_r{float(rate)}"
                unit=float(cm[unit_key])*cm["without_group_receiver_fraction_fixed_geography"]
                if denom=="PCE":
                    unit*=cm["national_ce_spending_usd"]/1e9/float(comp["national_spending_bn"])
                resp=-Hpair*unit
                gov=cm["government_use_mortality_adjusted_bn"]*case["lineage"]["lineage_population"]/case["lineage"]["account_union"]
                if valuation=="VSLY":
                    # Keep morbidity dollars fixed; transform mortality only.
                    from_air=float(cm[f"mean_outsider_vsl_usd_r{float(rate)}"])
                    gov*=((from_air/air.VSL_DOT_2024)+morb-1)/morb
                for crash_arm,proxy,d,demand,boundary in itertools.product(["all_density","multivehicle_only"],["primary_food","any_food"],["0.0","0.5","1.0"],[False,True],["identified_union","lineage_exchangeable"]):
                    exchange=boundary=="lineage_exchangeable"
                    receiver_factor=context["lineage_fixed_boundary"]["exchangeable_added_receiver_factor"] if exchange else 1.0
                    crash_row=one(crashes,population="lineage" if exchange else "lineage_gross",arm=crash_arm,end=end)
                    crash=float(crash_row["change_from_gross_live_bn"])
                    pm_delta_bound=float(pm["central_bn"])*receiver_factor-old_pm
                    vol=float(one(volunteers,year="2024",frame="lineage_key_extrapolation",food_task_proxy=proxy,displacement=d)[f"{end}_end_delta_bn"])
                    # Demand response is an explicit effective-demand arm. It
                    # does not assert that spending restores absent customers.
                    rest_new=-rest_expenditure*((1-psi*(1-Hpair/float(comp["group_spending_bn"])))**(-1/(sig-1))-1)
                    demand_delta=(rest_new-rest_base+float(comp["consumer_scale_demand_arm_bn"])*Hpair/Hmain) if demand else 0
                    delta=pm_delta_bound+resp*receiver_factor+gov*receiver_factor+crash+vol+demand_delta
                    stacks.append(dict(end=end,spending_denominator=denom,mortality_valuation=valuation,real_discount_rate=rate,
                                       crash_arm=crash_arm,volunteering_proxy=proxy,displacement=d,market_demand_arm=demand,pm_crash_recipient_boundary=boundary,
                                       baseline_bn=baseline[end],budget_saving_at_pairing_bn=Hpair,
                                       mortality_delta_bn=pm_delta_bound,respending_bn=resp*receiver_factor,government_mirror_bn=gov*receiver_factor,
                                       crash_delta_bn=crash,volunteering_delta_bn=vol,market_demand_delta_bn=demand_delta,
                                       city_tax_increment_bn=0.0,stack_delta_bn=delta,stack_pairing_bn=baseline[end]+delta,
                                       status=f"conditional source-key lineage extension; PM/crash receiver boundary {boundary}; other channels held; not an adopted total"))
    tax=one(taxes,frame="lineage_key_extrapolation")
    assert float(tax["low_end_delta_bn"])==float(tax["high_end_delta_bn"])==0
    for s in stacks:
        terms=[s[k] for k in ["mortality_delta_bn","respending_bn","government_mirror_bn","crash_delta_bn","volunteering_delta_bn","market_demand_delta_bn","city_tax_increment_bn"]]
        assert abs(sum(terms)-s["stack_delta_bn"])<1e-9
        assert abs(s["stack_pairing_bn"]-s["baseline_bn"]-sum(terms))<1e-9
    write_csv("one_fix_deltas.csv",fixes)
    write_csv("conditional_stacks.csv",stacks)
    (OUT/"integration.json").write_text(json.dumps(dict(
        comparator="2024 removal, frozen P7 baseline $439.435316/$532.847640bn; personal endpoints; all other social channels fixed",
        warning="No unconditional stack identified. Source-key lineage extensions have explicit PM/crash recipient-boundary arms. Parent's outside-lineage receiver corrections to other channels are separate; do not apply PM/crash correction twice.",
        components="one_fix_deltas are isolated; conditional_stacks reprice the spending/mortality interaction rather than summing task1+task2 blindly; CO2 excluded; VSL and VSLY alternatives; demand and displacement explicit",
        fiscal_pairing_low_current_budget_adjustment_bn=pairing_H_delta,
        funding="cash available in 2024 for both cash and accrual totals; capital and accrued pensions excluded; all-spent conditional",
        gates=dict(baseline_pairing=True,unique_producer_keys=True,city_tax_no_double_count=True,stack_closure_1e9=True),
        counts=dict(independent_fix_rows=len(fixes),conditional_stack_rows=len(stacks))),indent=2)+"\n")
    print(f"{len(fixes)} one-fix rows; {len(stacks)} conditional stack rows; closure PASS")


if __name__=="__main__":
    main()
