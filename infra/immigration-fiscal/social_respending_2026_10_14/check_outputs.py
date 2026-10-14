"""Independent conservation and cross-calibration checks on emitted tables.

Native-First: csv/json, source-derived controls; no stochastic test fixtures.
"""
import json
import math
from pathlib import Path

from respending import read_csv, spending_basis_gate, hard_gate, verify_pins, verify_bundle
from stack import one
from valuation_registry import mortality_registry

HERE=Path(__file__).resolve().parent
D=HERE/"derived"
verify_pins()
respending_generation=verify_bundle("respending")
stack_generation=verify_bundle("stack")
case=json.loads((D/"case_inputs.json").read_text())
rows=read_csv(D/"items.csv")
components=read_csv(D/"spending_components.csv")
carbon=read_csv(D/"co2_beside.csv")
stacks=read_csv(D/"conditional_stacks.csv")
n=0

def check(ok,label):
    global n
    hard_gate(ok,label)
    n+=1

for r in case["rows"]:
    check(abs(r["current_budget_saving_bn"]-(r["cash_set_cost_bn"]-r["capital_return_bn"]+r["private_wtp_bn"]))<1e-9,"cash funding identity")
    check(r["capital_return_bn"]>0 and r["current_budget_saving_bn"]<r["cash_set_cost_bn"],"imputed capital does not finance respending")
for basis in ["lineage","identified_union_at_case_responses"]:
    for end in ["low","high"]:
        cs={d:one(components,population_basis=basis,end=end,spending_denominator=d) for d in ["CE","PCE"]}
        # Changing a spending denominator must preserve the national harm
        # numerator and recipient fraction, rather than changing two quantities.
        a,b=[float(cs[d]["pm_harm_bn_per_bn_spent"])*float(cs[d]["national_spending_bn"]) for d in ["CE","PCE"]]
        check(abs(a-b)<1e-9,"CE/PCE numerator invariance")
        for denom,c in cs.items():
            spending_basis_gate(c["funding_accounting_basis"], c["denominator_accounting_basis"],
                                units_sensitivity=c["units_sensitivity"] == "True")
            check(denom == "PCE" or c["units_sensitivity"] == "True", "CE labelled units sensitivity")
            key=dict(population_basis=basis,end=end,spending_denominator=denom)
            r=one(rows,item="pm25_respending",**key)
            g=one(rows,item="pm25_government_mirror_legacy_response",**key)
            j=one(rows,item="pm25_joint_respending_government",**key)
            check(abs(float(j["central_bn"])-float(r["central_bn"])-float(g["central_bn"]))<1e-9,"joint row is components once")
            check(float(r["central_bn"])<0 and float(g["central_bn"])>0,"opposing emission signs")
for r in carbon:
    net=float(r["gross_mt"])-float(r["origin_mexico_mt"])+float(r["remittance_mt"])-float(r["respending_mt"])
    check(abs(net-float(r["net_mt"]))<1e-9,"CO2 emissions closure")
    check(abs(net*float(r["scc_2024usd"])/1000-float(r["global_damage_bn"]))<1e-9,"CO2 Mt-to-billion valuation")
    check(abs(float(r["global_damage_bn"])*float(r["us_damage_share"])*float(r["other_us_income_share"])-float(r["other_us_damage_bn"]))<1e-9,"CO2 beneficiary partition")
for s in stacks:
    vals=[float(s[k]) for k in ["mortality_delta_bn","respending_bn","government_mirror_bn","crash_delta_bn","volunteering_delta_bn","market_demand_delta_bn","city_tax_increment_bn","crime_mortality_delta_bn"]]
    registry=json.loads(s["mortality_registry_json"])
    mortality_registry(registry["valuation"],registry["real_discount_rate"],registry["channels"])
    check(abs(math.fsum(vals)+float(s["baseline_bn"])-float(s["stack_pairing_bn"]))<1e-9,"stack signed closure")
    check(float(s["city_tax_increment_bn"])==0,"no duplicate city tax")
    check("conditional" in s["status"],"counterfactual not relabelled observed")
for r in rows:
    check(float(r["low_bn"])<=float(r["central_bn"])<=float(r["high_bn"]),"ordered deterministic point arms")
    check(all(r[k] for k in ["comparator","beneficiary","valuation","overlap"]),"row declaration complete")
check(respending_generation==verify_bundle("respending"),"stable respending generation")
check(stack_generation==verify_bundle("stack"),"stable stack generation")
print(f"PASS {n} accounting/calibration/declaration checks")
