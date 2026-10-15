#!/usr/bin/env python3
"""Package conditional item-18 arms; unidentified central values stay null.

Native-First: existing BEA/CPS tables, JSON edit declarations and adopted evaluator.
The source reports cannot identify the requested complete 2024 tax-base bridge.
These arms measure implications of stated transports, never fill missing cells silently.
"""
from pathlib import Path
import csv
import importlib.util
import json
import sys

import numpy as np
import pandas as pd

import business_bases

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] item18: " + message)


def basket_factor(table, taxes, arm, snap_source="cps_reported"):
    """Fixed state collection pools; normalize member and nonmember taxable baskets.

    This is a relative correction to the adopted line, not a replacement estimate of
    its level. State-law proxy rates do not resolve county-level local exemptions.
    """
    def total(name):
        rows = table[(table.arm == name) & (table.snap_source == snap_source)
                     & table.group.eq("union_completed") & table.state_fips.ne(0)].set_index("state_fips")
        require(set(taxes.index) == set(rows.index), "basket states differ from collection states")
        share = rows.group_share_state.reindex(taxes.index)
        require(np.isfinite(share).all(), "missing state basket share")
        return float((taxes * share).sum())
    return total(arm) / total("full")


def producer_share(weights, wages, snapshot):
    """Industry-key arm, mining zero; national state composition transported.

    Use the item-6 union normalization and its two latent-lineage wage parts.
    Completion/coverage purchaser mix is not observed and remains a stated transport.
    """
    w = wages[wages.allocation.eq("personal")].set_index("cell")
    require(w.index.is_unique, "duplicate wage cells")
    missing = sorted({r["key"] for r in weights if r["kind"] == "intermediate" and r["key"] not in w.index})
    require(not missing, "unmapped purchaser industries must be declared unresolved: " + repr(missing))
    shares = {}
    for group, column in [("union", "union_share"), ("G3plus", "G3plus_share"), ("white", "white_share")]:
        shares[group] = sum(float(r["share_of_total_duties"]) * float(w.loc[r["key"], column])
                            * float(w.loc[r["key"], "responds"])
                            for r in weights if r["kind"] == "intermediate")
    plain = {g: float((w.national_wages_bn * w[c]).sum() / w.national_wages_bn.sum())
             for g, c in [("G3plus", "G3plus_share"), ("white", "white_share")]}
    meta = snapshot["baseline"]["set"]["item6"]
    source_item = json.loads((FISCAL / "job_capital_taxes_2026_10_14/derived/item.json").read_text())
    normalization = (source_item["lines"]["other_production_taxes"]["plain_wage_share"]["personal"]
                     / source_item["lines"]["other_production_taxes"]["lane_plain_wage_share"]["personal"])
    wage_parts = meta["lineage"]["wage_share"]
    adjusted = shares["union"] * normalization
    adjusted += wage_parts["g3plus"]["personal"] * shares["G3plus"] / plain["G3plus"]
    adjusted += wage_parts["whites"]["personal"] * shares["white"] / plain["white"]
    return {"share": adjusted, "union_normalization": normalization, "raw_group_shares": shares,
            "raw_plain_wage_shares": plain, "latent_wage_parts": wage_parts,
            "state_rule": "national item6 state/industry composition transported; not measured purchaser state",
            "completion_rule": "additional item10 and coverage mix not re-estimated"}


def assemble():
    snapshot = json.loads((HERE / "derived/case_snapshot.json").read_text())
    business = business_bases.build_bridge()
    baskets = pd.read_csv(HERE / "derived/household_state_factors.csv")
    state = load(FISCAL / "state_priced_services_2026_09_29/state_price.py", "item18_state_prices")
    # Same primary finance reader as the adopted state-pricing lane; never write it.
    taxes = state.read_finance(2024).reindex(sorted(state.STATES)).T09.astype(float)
    require(taxes.sum() > 0 and taxes.notna().all(), "state T09 collections absent")
    taxes = taxes / taxes.sum()
    factors = {arm: basket_factor(baskets, taxes, arm) for arm in ["grocery", "snap", "joint"]}
    ce_factors = {arm: basket_factor(baskets, taxes, arm, "ce_rank")
                  for arm in ["grocery", "snap", "joint"]}
    wages = pd.read_csv(FISCAL / "job_capital_taxes_2026_10_14/derived/wages_by_industry.csv")
    customs = business["customs_proportional_arm"]
    production = producer_share(customs["purchaser_weights"], wages, snapshot)
    old_customs_share = snapshot["lines"]["set"]["customs_duties"]["engine_share"]
    pce = customs["conditional_household_share"]
    final = sum(r["share_of_total_duties"] for r in customs["purchaser_weights"]
                if r["kind"] not in ["household", "intermediate"])
    # Unkeyed final use is carried explicitly in one arm and bounded in two others.
    customs_shares = {"carried": pce * old_customs_share + production["share"] + final * old_customs_share,
                      "final_zero": pce * old_customs_share + production["share"],
                      "final_one": pce * old_customs_share + production["share"] + final}
    job_share = snapshot["baseline"]["set"]["job_production_share"]
    sales_share = snapshot["lines"]["set"]["general_sales_tax"]["engine_share"]
    # Explicit crosscheck scenario. This is not a measured national 2024 business share.
    b = business["crosscheck_only"]["business_fraction_of_general_sales_tax"]
    sales_business_ratio = ((1-b)*sales_share + b*job_share)/sales_share
    common_limits = ["State-law proxy omits exact county/city grocery rates and item exceptions.",
                     "CE food/nonfood grocery split requires the documented BLS decile calibration.",
                     "A basket ratio is transported to latent, completion and missed-person line prices.",
                     "Item11 mixed-household consumption removal is held; its basket-specific response is unidentified.",
                     "The excise business bridge is unmeasured and held, not estimated as zero.",
                     "Industry/state purchaser composition of investment/government final use is missing."]
    arms = {}

    def add(name, label, ratios, assumptions):
        arms[name] = {"label": label, "status": "CONDITIONAL_ARM_ONLY", "receipt_ratios": ratios,
                      "coverage_transport": "same line ratio, each end/set/source generation separately",
                      "item11": "held fixed, not recomputed", "assumptions": assumptions,
                      "limits": common_limits}

    add("off", "v8 unchanged identity control", {}, [])
    arms["off"]["status"]="IDENTITY_CONTROL"
    for arm in ["grocery", "snap", "joint"]:
        add("household_"+arm, "state-law household basket: "+arm,
            {"general_sales_tax": factors[arm]}, ["All collections remain on the current household proxy; business purchases held."])
    sales_assumptions = ["COST/EY business share is a crosscheck parameter, not a central source.",
                        "Purchaser industry/state weights transported from item6 other-production taxes.",
                        "Business-base denominator excludes residential taxes and mining; purchaser mix remains unmeasured."]
    add("business_sales_crosscheck", "41.8% national sales share crosscheck at item6 business-base key",
        {"general_sales_tax": sales_business_ratio},
        sales_assumptions)
    old_job_share = snapshot["baseline"]["set"]["whole_line_share_superseded"]
    add("whole_line_share_superseded", "SUPERSEDED diagnostic: whole-OTP-line share in business sales",
        {"general_sales_tax": ((1-b)*sales_share + b*old_job_share)/sales_share},
        sales_assumptions[:2]+["Superseded diagnostic divides the business-only OTP target by the whole OTP line; denominator mismatch retained only to reproduce the old arm."])
    arms["whole_line_share_superseded"]["status"] = "SUPERSEDED_DIAGNOSTIC"
    for name, share in customs_shares.items():
        add("business_customs_"+name, "BEA proportional customs purchaser arm: "+name,
            {"customs_duties": share/old_customs_share},
            customs["assumptions"]+["Final-demand key "+("carried at old household key" if name=="carried" else name),
                                      "National state composition transported from item6."])
    ratios={"general_sales_tax":sales_business_ratio,"customs_duties":customs_shares["carried"]/old_customs_share}
    add("business_sales_customs", "sales crosscheck + conditional customs; excise held", ratios,
        arms["business_sales_crosscheck"]["assumptions"]+arms["business_customs_carried"]["assumptions"])
    mining_shares = {}
    for percent in (5, 8):
        mining = percent/100
        share = (1-mining)*job_share
        mining_shares[str(percent)] = {"taxable_business_purchase_fraction": mining,
                                      "mining_response": 0, "effective_production_share": share}
        name = "business_sales_mining_"+str(percent)
        label = f"[ASSUMPTION] mining {percent}% of taxable business purchases; mining response zero"
        assumptions = sales_assumptions+[label, "Nonmining purchases retain the item6 business-base mix."]
        sales_ratio = ((1-b)*sales_share + b*share)/sales_share
        add(name, label, {"general_sales_tax": sales_ratio}, assumptions)
        add(name+"_customs", label+" + conditional customs; excise held",
            {"general_sales_tax": sales_ratio, "customs_duties": ratios["customs_duties"]},
            assumptions+arms["business_customs_carried"]["assumptions"])
    joint=dict(ratios)
    joint["general_sales_tax"] = ((1-b)*sales_share*factors["joint"] + b*job_share)/sales_share
    add("joint_sales_customs_household", "conditional business + joint food/SNAP basket; excise held", joint,
        arms["business_sales_customs"]["assumptions"]+["Household basket applies to household sales share only; business part is not grocery-exempted twice."])
    out={"item_id":"consumption_tax_bases","item_number":18,"kind":"post_engine",
         "identification_status":"WITHHOLD_FULL_ITEM","central":None,"arms":arms,
         "baseline":snapshot["baseline"],"population":snapshot["population"],
         "measurement":{"basket_factors":factors,"ce_basket_factors":ce_factors,"sales_crosscheck_business_fraction":b,
                        "sales_production_share":job_share,"sales_mining_assumptions":mining_shares,
                        "customs_producer":production,"customs_shares":customs_shares,
                        "customs_unresolved_purchaser_fraction":final},
         "unresolved":business["required_for_central"]+common_limits,
         "national_collection_rule":"Receipt cell target shifts against other; each national total remains fixed.",
         "item9":"Corporate foreign-source correction held; none of the three consumption receipts is corporate tax.",
         "item10":"Every receipt scenario and its signed reporter carriers move; observed-child receipts already inside cells.",
         "item11":"held explicitly; full item must replace M5 on one joint mixed-unit basket before adoption",
         "item12":"coverage receipt source parts transported by matching line ratios, not copied from set to cash",
         "round5":"W14 tenure changes basket prices; joint tenure repricing required. W16 is a separate future-law companion; tariff base changes are not added to this 2024-law item."}
    (HERE / "derived/item.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    with (HERE / "derived/state_collection_weights.csv").open("w",newline="") as f:
        writer=csv.writer(f,lineterminator="\n")
        writer.writerow(["state_fips","tax_code","year","collection_fraction"])
        writer.writerows((int(k),"T09",2024,float(v)) for k,v in taxes.items())
    print("item18 central WITHHELD; packaged "+str(len(arms))+" explicit conditional arms")
    return out


if __name__ == "__main__":
    assemble()
