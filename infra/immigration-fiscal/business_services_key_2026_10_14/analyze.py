#!/usr/bin/env python3
"""Business-serving sensitivities of the frozen oct14 case; no case edits.

All arms are one change from the same baseline. Incident fractions are explicitly
assumed spending fractions. National budgets, household keys, receipt responses,
production and the existing capital stocks hold. SDR errors condition on them.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import resource
import time
import numpy as np

HERE = Path(__file__).resolve().parent
GATES = []


def read(path):
    return json.loads((HERE / path).read_text())


def gate(name, ok, detail=None):
    GATES.append({"name": name, "pass": bool(ok), "detail": detail})
    if not ok:
        raise RuntimeError(f"[BLOCKED] {name}: {detail}")


def sdr(x):
    x = np.asarray(x)
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def write_csv(path, rows):
    with (HERE / path).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    start = time.perf_counter()
    inventory = read("derived/inventory.json")
    activity = read("derived/activity_keys.json")
    shares = read("inputs/spending_shares.json")
    incidents = read("inputs/incident_shares.json")
    highways = read("inputs/highway_shares.json")
    gate("upstream inventory all gates", all(x["pass"] for x in inventory["gates"]))
    gate("activity gate schema", all("passed" in x for x in activity["gates"]))
    gate("activity all gates", all(x["passed"] for x in activity["gates"]))
    gate("activity population matches inventory union", abs(activity["meta"]["population"] - inventory["frame"]["union"]) < 1e-3)
    keys = activity["keys"]
    for name, key in keys.items():
        g = key["groups"]
        gate(f"{name} generations conserve union", abs(sum(g[x]["share"] for x in ["G1", "G2", "G3plus"]) - g["union"]["share"]) < 1e-12)
        gate(f"{name} replicate SE", abs(sdr(g["union"]["replicates"]) - g["union"]["se"]) < 1e-12)
    # The hybrid retains mining's old service allocation. It never assigns fixed mining zero service.
    def business(name, frame, baseline, replicate=False):
        key = keys[name]
        g = key["groups"]
        mine = key["mining_output_fraction"] if name.endswith("mining_fixed") else 0
        if replicate:
            value = np.asarray(g["union"]["replicates"])
        else:
            value = g["union"]["share"]
        if frame == "lineage":
            wages = inventory["added_wage_shares"]
            # Same addition rule as item 6: added members' case wage share times their group's factor.
            value = value + wages["g3plus"]["personal"] * g["G3plus"]["factor"] + wages["whites"]["personal"] * g["white_nh"]["factor"]
        return value + mine * baseline

    fractions = shares["fractions"]
    police = incidents["police"]["2024"]["narrow_share"]
    fire = incidents["fire"]["narrow_share"]
    arms = [
        {"arm": "unchanged_recommended", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": None},
        {"arm": "incident_proxy", "activity": "business_output_mining_fixed", "police": police, "fire": fire, "freight": None},
        {"arm": "incident_proxy_plain_wage", "activity": "plain_wage", "police": police, "fire": fire, "freight": None},
        {"arm": "incident_proxy_mining_moves", "activity": "business_output_full", "police": police, "fire": fire, "freight": None},
        {"arm": "police_2023_proxy", "activity": "business_output_mining_fixed", "police": incidents["police"]["2023"]["narrow_share"], "fire": 0, "freight": None},
        {"arm": "police_2024_proxy", "activity": "business_output_mining_fixed", "police": police, "fire": 0, "freight": None},
        {"arm": "fire_all_runs_proxy", "activity": "business_output_mining_fixed", "police": 0, "fire": fire, "freight": None},
        {"arm": "broader_location_proxy", "activity": "business_output_mining_fixed", "police": incidents["police"]["2024"]["broad_share"], "fire": incidents["fire"]["nonresidential_structure_share"], "freight": None},
        {"arm": "pos_capital_expenditure_mix_proxy", "activity": "business_output_mining_fixed", "police": police, "fire": fire, "freight": None, "pos_capital": True},
        {"arm": "freight_demand_control", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "demand"},
        {"arm": "freight_goods_output", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "freight_output_mining_fixed"},
        {"arm": "freight_goods_output_mining_moves", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "freight_output_full"},
        {"arm": "freight_plain_wage", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "plain_wage"},
        {"arm": "oregon_cost_share_demand", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "demand", "freight_share": highways["oregon_corrected"]["heavy_cost_share"]},
        {"arm": "federal_cost_share_demand", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "demand", "freight_share": highways["hcas_addendum_federal"]["freight_share"]},
        {"arm": "truck_vmt_2023_demand", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "demand", "freight_share": highways["vm1"]["years"]["2023"]["truck_vmt_share"]},
        {"arm": "truck_vmt_2024_demand", "activity": "business_output_mining_fixed", "police": 0, "fire": 0, "freight": "demand", "freight_share": highways["vm1"]["years"]["2024"]["truck_vmt_share"]},
        {"arm": "combined_incidents_goods_output", "activity": "business_output_mining_fixed", "police": police, "fire": fire, "freight": "freight_output_mining_fixed"},
    ]
    rows, details, thresholds = [], [], []
    passenger = inventory["meta"]["roads_mileage_key"]["passenger_share"]
    freight_fraction = 1 - passenger
    gate("HCAS freight share reproduces inherited roads", abs(highways["hcas_v21"]["shares"]["total_m"]["freight_share"] - freight_fraction) < 1e-12)
    for arm in arms:
        for end in ["low", "high"]:
            for frame in ["union", "lineage"]:
                pieces = []
                for run in [x for x in inventory["runs"] if x["end"] == end]:
                    spending = {x["id"]: x for x in run["spending"]}
                    capital = {x["id"]: x for x in run["capital"]}
                    receipts = {x["id"]: x for x in run["receipts"]}
                    field = "union_amount_bn" if frame == "union" else "amount_bn"
                    kfield = "union_key" if frame == "union" else "key"
                    pop = spending["general_public_services"][field] / spending["general_public_services"]["national_bn"]
                    order = spending["public_order_safety"]
                    # Preserve the current state-pricing correction as a common intensity factor.
                    state_index = (order[field] + spending["state_price_public_order_safety"][field]) / order[field]
                    police_national = order["national_bn"] * fractions["Police"] - shares["excluded_border_and_custody_bn"]
                    protective = shares["police_protective_fraction"]
                    police_weight = police_national * protective * arm["police"] * state_index
                    fire_weight = order["national_bn"] * fractions["Fire"] * arm["fire"] * state_index
                    business_key = business(arm["activity"], frame, pop)
                    police_delta = police_weight * (business_key - pop)
                    fire_delta = fire_weight * (business_key - pop)
                    new_order_target = order[field] + spending["state_price_public_order_safety"][field] + police_delta + fire_delta
                    new_order_other = order["national_bn"] - new_order_target
                    gate("rekeyed safety target+other closes national at 1e-9bn", new_order_target >= 0 and new_order_other >= 0 and abs(new_order_target+new_order_other-order["national_bn"]) < 1e-9)
                    gate("safety subfunctions and excluded pools close national", abs(police_national + shares["excluded_border_and_custody_bn"] + order["national_bn"] * sum(fractions[k] for k in ["Fire", "Law courts", "Prisons"]) - order["national_bn"]) < 1e-9)
                    mine = keys[arm["activity"]]["mining_output_fraction"] if arm["activity"].endswith("mining_fixed") else 0
                    # Population shares measured on row4 national household weights are mapped
                    # to the frozen case amount key. The mapped baseline and intensity hold fixed.
                    pop_reps = np.asarray(keys["population"]["groups"]["union"]["replicates"])
                    pop_reps = pop_reps * pop / pop_reps[0]
                    replicas = (police_weight + fire_weight) * (business(arm["activity"], "union", pop_reps, True) - pop_reps)
                    cap_delta = 0
                    if arm.get("pos_capital"):
                        # Unmeasured crosswalk: same expense mix applied to safety structures;
                        # courts/capitol office stock remains unchanged. This is only an arm.
                        capital_share = (police_weight + fire_weight) / (order["national_bn"] * state_index)
                        for cid in ["pos_sl", "pos_fed"]:
                            c = capital[cid]
                            old = c[kfield]
                            new = business(arm["activity"], frame, old)
                            cap_delta += c["stock_charged_bn"] * run["spec"]["rate"] * c["response"] * capital_share * (new - old)
                            replicas += c["stock_charged_bn"] * run["spec"]["rate"] * c["response"] * capital_share * (business(arm["activity"], "union", old, True) - old)
                    road_delta = 0
                    current_road = capital["hwy_sl"][kfield]
                    gate("SL and federal highway key agree", abs(current_road - capital["hwy_fed"][kfield]) < 1e-10)
                    excise = receipts["excise_selective_sales"]
                    excise_key = excise[field] / excise["national_bn"]
                    gasoline_fraction = inventory["meta"]["roads_mileage_key"]["gasoline_bn"] / excise["national_bn"]
                    # Invert the existing two keys: road=p*passenger+(1-p)*consumption;
                    # excise=gas_fraction*passenger+(1-gas_fraction)*consumption.
                    freight_key = (passenger * excise_key - gasoline_fraction * current_road) / (passenger - gasoline_fraction)
                    passenger_key = (current_road - freight_fraction * freight_key) / passenger
                    gate("road/excise two-key reconstruction", abs(passenger * passenger_key + freight_fraction * freight_key - current_road) < 1e-12 and abs(gasoline_fraction * passenger_key + (1-gasoline_fraction) * freight_key - excise_key) < 1e-12)
                    if frame == "union":
                        direct = run["direct_union_road_keys"]
                        gate("union freight/passenger principal positive control", abs(freight_key-direct["k_cons"]) < 1e-12 and abs(passenger_key-direct["s_vmt"]) < 1e-12)
                        freight_key, passenger_key = direct["k_cons"], direct["s_vmt"]
                    road_coefficient = 0
                    if arm["freight"]:
                        arm_freight_share = arm.get("freight_share", freight_fraction)
                        new_freight = freight_key if arm["freight"] == "demand" else business(arm["freight"], frame, freight_key)
                        for part in ["sl", "fed"]:
                            correction = spending[f"roads_vmt_{part}"]
                            national = inventory["meta"]["roads_mileage_key"]["highway_national_bn"][part]
                            c = capital[f"hwy_{part}"]
                            coefficient = national * correction["response"] + c["stock_charged_bn"] * run["spec"]["rate"] * c["response"]
                            road_coefficient += coefficient
                        new_road = (1-arm_freight_share) * passenger_key + arm_freight_share * new_freight
                        gate("changed road key target+other conserves weight", 0 <= new_road <= 1 and abs(new_road+(1-new_road)-1) < 1e-12)
                        road_delta = road_coefficient * (new_road-current_road)
                        if arm["freight"] != "demand":
                            replicas += road_coefficient * arm_freight_share * (business(arm["freight"], "union", freight_key, True) - freight_key)
                    delta = police_delta + fire_delta + cap_delta + road_delta
                    baseline = run["union_at_case_responses_bn"] if frame == "union" else run["cost_bn"]
                    gate("new allocation conserves national budget", 0 <= business_key <= 1 and 0 <= pop <= 1)
                    if arm["arm"] in ["unchanged_recommended", "freight_demand_control"]:
                        gate("unchanged positive control delta", abs(delta) < 1e-12)
                    pieces.append({"delta": delta, "baseline": baseline, "replicas": replicas})
                    details.append({"arm": arm["arm"], "frame": frame, "end": end, "method": run["method"], "police_delta_bn": police_delta, "fire_delta_bn": fire_delta, "pos_capital_delta_bn": cap_delta, "highway_delta_bn": road_delta, "total_delta_bn": delta, "population_key": pop, "business_key": business_key, "passenger_key": passenger_key, "freight_demand_key": freight_key, "state_price_index": state_index, "new_safety_target_bn": new_order_target, "new_safety_other_bn": new_order_other, "safety_national_bn": order["national_bn"]})
                    if arm["arm"] == "unchanged_recommended":
                        # What share would be required to change the headline by $5bn?
                        for label, coefficient in [("general_administration", spending["general_public_services"]["national_bn"] * spending["general_public_services"]["response"] + sum(capital[c]["stock_charged_bn"] * run["spec"]["rate"] * capital[c]["response"] for c in ["gps_sl", "gps_fed"])), ("municipal_enterprise_capital", sum(c["stock_charged_bn"] * run["spec"]["rate"] * c["response"] for c in capital.values() if c["id"].startswith("ent_") and c["id"] != "ent_housing_sl"))]:
                            per_full_share = coefficient * (business_key - pop)
                            thresholds.append({"component": label, "frame": frame, "end": end, "method": run["method"], "delta_if_all_business_bn": per_full_share, "business_share_for_5bn": 5 / abs(per_full_share) if per_full_share else None, "status": "ASSUMPTION diagnostic, not adopted; enterprise receipts held fixed"})
                delta = sum(x["delta"] for x in pieces) / len(pieces)
                baseline = sum(x["baseline"] for x in pieces) / len(pieces)
                # Preserve covariance across methods and keys: average vectors first.
                reps = sum(x["replicas"] for x in pieces) / len(pieces)
                rows.append({"arm": arm["arm"], "frame": frame, "end": end, "baseline_bn": baseline, "change_bn": delta, "result_bn": baseline + delta, "conditional_union_key_se_bn": sdr(reps) if frame == "union" else None, "above_5bn_bar": abs(delta) >= 5, "members": inventory["frame"][frame], "freight_basis": "[DEGRADED] effective split inferred after independent age-mix reprofile; not literal measured consumption" if frame == "lineage" and arm["freight"] is not None and arm["arm"] != "freight_demand_control" else "principal union keys / unchanged demand control"})
    inputs = ["derived/inventory.json", "derived/activity_keys.json", "inputs/spending_shares.json", "inputs/incident_shares.json", "inputs/highway_shares.json"]
    hashes = {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in inputs}
    write_csv("derived/arms.csv", rows)
    write_csv("derived/line_changes.csv", details)
    write_csv("derived/break_shares.csv", thresholds)
    result = {"case": "oct14", "unit": "billions of 2024 dollars per year, net-cost change for other residents", "recommendation": "retain central, zero rekeying until spending/stock shares measured; proxy arms beside", "arms": arms, "rows": rows, "gates": GATES, "input_sha256": hashes, "holds_fixed": "personal end specifications 16/11; national budgets/stocks; service responses; household part; receipts; production; group frame; state-price intensity", "se_scope": "union CPS SDR, conditional on national shares, output vector, pooling, averaged fillin factors, mapped baseline and state index; road consumption and capital mix held fixed. Lineage SE unavailable: added members not observed in CPS and correlated model factors not propagated."}
    (HERE / "derived/summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS {len(GATES)} gates; {len(rows)} arm/frame/end rows; seconds={time.perf_counter()-start:.3f}; maxrss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
    for row in rows:
        if row["frame"] == "lineage":
            print(f'{row["arm"]} {row["end"]}: {row["change_bn"]:+.6f}bn -> {row["result_bn"]:.6f}bn')


if __name__ == "__main__":
    main()
