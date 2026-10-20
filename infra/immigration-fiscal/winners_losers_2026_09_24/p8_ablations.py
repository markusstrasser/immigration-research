"""Controlled source-item and social-row decompositions on the live person frame.

Source fiscal increments are isolated from v7; current incidence keys are held
fixed so the table does not conflate a fiscal item with unrelated key changes.
"""
from __future__ import annotations

import copy
import itertools
import json

import numpy as np
import pandas as pd

import p7_frames as p7
from p8_social import amounts, environment


def summaries(model, name, rule, frame, level, vector, future, base, rows):
    for sharing, values in (("person", vector), ("pooled", model.pool(vector))):
        row = p7.summary_row(model.d, model.weights, values, scenario=name, financing=rule,
            frame=frame, level=level, sharing=sharing, future_bn=-future)
        row.update(delta_total_bn=row["total_bn"] - base[sharing]["total_bn"],
                   delta_ahead_pp=100*(row["winners_share"]-base[sharing]["winners_share"]))
        rows.append(row)


def component_vector(model, cx, pieces, rule, frame, level, effect):
    """Allocate one source-isolated item with explicit fiscal class transport."""
    wl, d, w = model.wl, model.dd, model.weights
    f = effect["financing"]
    share = model.meta["deficit"]["share"]
    cf, cs = f["cash_bn"]["fed"], f["cash_bn"]["sl"]
    rf, rs = f["resource_cost_bn"]["fed"], f["resource_cost_bn"]["sl"]
    accrual, unlocated = f["accrual_bn"], f["unlocated_bn"]
    today = cf * (1-share) + rf
    borrow = cf * share
    future = borrow + accrual
    out = -wl.alloc(d, cx["kf"], today)
    state_dollars = model.state_cache[level]
    state_total = sum(state_dollars.values())
    out -= wl.alloc_states(d, cx["ks"], {s:(cs+rs)*v/state_total for s,v in state_dollars.items()},
                          notes=model.notes, label="isolated-item fixed current state geography")
    out -= wl.alloc(d, np.ones(len(d)), unlocated)
    from p7_cohorts import payroll_key
    if frame == "stationary":
        out -= wl.alloc(d, cx["kf"], borrow)
        out -= wl.alloc(d, payroll_key(d, model.trust[level]["hi_payout_fraction"]), accrual)
        future = 0.
    else:
        ck = model.cohort_new[True]
        horizon = "borrowing30" if frame == "cohort30" else "borrowing10"
        bs, ts = ck["living_shares"][horizon], ck["living_shares"]["trust"]
        out -= wl.alloc(d, ck["keys"][horizon], borrow*bs)
        out -= wl.alloc(d, ck["keys"]["trust"], accrual*ts)
        future = borrow*(1-bs)+accrual*(1-ts)
    # The source's private-production delta is signed as a fiscal cost. The
    # wages use the source live wage vector as a declared distribution proxy.
    private = f["private_production_bn"]
    wage = pieces["wages_positive"] + pieces["wages_negative"]
    den = p7.total(wage, w)
    out += wage * (-private/den) if den else wl.alloc(d, d.earn.to_numpy(), -private)
    out -= wl.alloc(d, np.ones(len(d)), f["displaced_bn"])
    residual = -effect["cost_bn"] + future - p7.total(out, w)
    p7.require("isolated_item_unclassified_only", abs(residual) < 1e-6, residual_bn=residual)
    out += wl.alloc(d, np.ones(len(d)), residual)
    return out, future


def social_item_vector(model, pieces, end, item):
    env = model.source["v8_social_environment"]
    config = env["v8_added_social"]
    out = np.zeros(len(model.d))
    for row, part in env["variants"]["central"]["parts"][end]["v8_added_by_item"].items():
        amount = 0.
        if item == "mixed_unit_removal":
            amount = part["item11_consumption_bn"]
        elif item in ("union_completion", "coverage"):
            key = part["key"]
            if key == "consumption":
                counts = config["consumption_receipts_bn"][end]
                fraction = counts["completion_bn"] / (counts["completion_bn"] + counts["coverage_bn"])
            else:
                scope = {"head_count":"all", "uninsured_use":"all", "road":"5_plus", "pupils":"5_17", "adults":"18_plus"}.get(key)
                if scope:
                    c = config["people"]["completion_by_scope"][scope]
                    v = config["people"]["coverage_by_scope"][scope]
                    fraction = c / (c+v)
                else:
                    fraction = 0.
            amount = part["added_people_bn"] * (fraction if item=="union_completion" else 1-fraction)
            if item == "union_completion":
                amount += part["completion_receivers_bn"]
        total = p7.total(pieces[row], model.weights)
        if amount:
            p7.require("social_item_recipient_seed_"+row, total != 0.)
            out += pieces[row] * (-amount/total)
    return out


def measure(model, out, write):
    effects = json.loads(p7.pin(out / "p8_item_effects.json", model.wl).read_text())
    rows, channel_rows = [], []
    env = model.source["v8_social_environment"]
    social_names = {"round3_government_side": "government_side", "round3_added_people": "v8_added_people",
                    "round3_item11_consumption": "item11_consumption", "round3_completion_receivers": "completion_receivers"}
    for rule, frame, level in itertools.product(("a", "b", "c"), ("stationary", "cohort30", "cohort10"), ("low", "high")):
        p7.GATE_SCOPE = f"ablations/{rule}/{frame}/{level}"
        share, pieces, future, _ = model.evaluate(rule, frame, level)
        base = {s: p7.summary_row(model.d, model.weights, share[s]) for s in ("person", "pooled")}
        cx = model.context(rule)
        joint, joint_future = component_vector(model, cx, pieces, rule, frame, level, effects["joint"]["set"][level])
        actual_stayers = sum(v for k,v in pieces.items() if k.startswith("item11_stayers_"))
        legacy_stayers = model.credits["by_end_attribution"][level].get("item5b_replaced_once",np.zeros(len(model.d)))
        stayer_increment = actual_stayers - legacy_stayers
        social_items = {item:social_item_vector(model,pieces,level,item) for item in effects["items"]}
        all_off = share["person"] - joint - stayer_increment - sum(social_items.values())
        all_off_future = future-joint_future
        all_off_base = {s:p7.summary_row(model.d,model.weights,v) for s,v in
                       (("person",all_off),("pooled",model.pool(all_off)))}
        summaries(model,"v8_all_off_fixed_keys",rule,frame,level,all_off,all_off_future,base,rows)
        for item, by_basis in effects["items"].items():
            effect = by_basis["set"][level]
            delta, f = component_vector(model, cx, pieces, rule, frame, level, effect)
            source_isolated = all_off + delta + social_items[item]
            if item == "mixed_unit_removal":
                source_isolated += stayer_increment
            summaries(model,"isolated_"+item,rule,frame,level,source_isolated,all_off_future+f,all_off_base,rows)
            # Leave-one-out changes identify the isolated source-item increment
            # at fixed current keys; the exact source all-off level is exported.
            vector = share["person"] - delta
            vector -= social_items[item]
            if item == "mixed_unit_removal":
                vector -= stayer_increment
            summaries(model, "without_" + item, rule, frame, level, vector, future-f, base, rows)
            channel_rows.append(dict(scenario=item, financing=rule, frame=frame, level=level,
                isolated_source_cost_bn=effect["cost_bn"], current_incidence_delta_bn=p7.total(delta, model.weights),
                future_delta_bn=-f, allocation_rule=effect["financing"]["rule"]))
        for name, term in social_names.items():
            delta = np.zeros(len(model.d))
            if term == "government_side":
                delta = pieces["pm25_government_side"]
            else:
                field = {"v8_added_people": "added_people_bn", "item11_consumption": "item11_consumption_bn",
                         "completion_receivers": "completion_receivers_bn"}[term]
                for item, part in env["variants"]["central"]["parts"][level]["v8_added_by_item"].items():
                    if item not in pieces:
                        raise RuntimeError("[BLOCKED] social ablation lacks recipient row " + item)
                    denominator = p7.total(pieces[item], model.weights)
                    delta += pieces[item] * (-part[field]/denominator) if denominator else 0.
            summaries(model, "without_"+name, rule, frame, level, share["person"]-delta, future, base, rows)
            channel_rows.append(dict(scenario=name, financing=rule, frame=frame, level=level,
                current_incidence_delta_bn=p7.total(delta,model.weights),future_delta_bn=0.))
        central = amounts(model.source)
        for variant in ("government_legacy_response", "respending_without_government_side", "neither_budget_side", "matched_justice_footing"):
            selected = amounts(model.source, variant)
            delta = np.zeros(len(model.d))
            for item, totals in selected.items():
                change = totals[level] - central.get(item, {}).get(level, 0.)
                if not change:
                    continue
                if item == "variant_fiscal_justice":
                    state_dollars = model.state_cache[level]
                    total = sum(state_dollars.values())
                    delta -= model.wl.alloc_states(model.dd, cx["ks"], {s:change*v/total for s,v in state_dollars.items()},
                        notes=model.notes,label="matched justice budget footing")
                elif item in pieces and p7.total(pieces[item], model.weights):
                    delta += pieces[item] * (-change / p7.total(pieces[item], model.weights))
                else:
                    delta -= model.wl.alloc(model.dd, np.ones(len(model.d)), change)
            summaries(model, variant, rule, frame, level, share["person"]+delta, future, base, rows)
        # The average FY2024 deficit share remains central. Zero/full borrowing
        # are explicit financing readings, with no change to the case total.
        original_share = model.meta["deficit"]["share"]
        original_fiscal = copy.deepcopy(model.meta["fiscal"])
        try:
            for borrowing_share in (0., 1.):
                model.meta["deficit"]["share"] = borrowing_share
                for L, f in model.meta["fiscal"].items():
                    f["federal_today"] = (1-borrowing_share)*f["cash_federal"] + f["resource_federal"]
                    f["future_borrowing"] = borrowing_share*f["cash_federal"]
                    f["future"] = f["future_borrowing"] + f["accrual"]
                alternate, _, deferred, _ = model.evaluate(rule, frame, level)
                summaries(model, "borrowing_"+str(int(borrowing_share)), rule, frame, level,
                    alternate["person"], deferred, base, rows)
        finally:
            model.meta["deficit"]["share"] = original_share
            model.meta["fiscal"] = original_fiscal
    write(pd.DataFrame(rows), "p8_ablations.csv", out)
    write(pd.DataFrame(channel_rows), "p8_isolated_channels.csv", out)


def ledger(model, out, write):
    """Both pension sets close using the debt producer's typed current flows."""
    source = model.wl.PATHS["debt_source_parts"]
    table = pd.read_csv(p7.pin(source,model.wl))
    rows = []
    for basis, end in itertools.product(("set", "cash"), ("low", "high")):
        chosen = table[table.basis.eq(basis) & table.end.eq(end) & table.convention.eq("central")]
        fiscal = -float(chosen.responsive_bn.sum())
        case_summary = json.loads((model.wl.FISCAL / model.wl.CASE["lane"] / "derived/summary.json").read_text())
        block = case_summary[model.wl.CASE.get("summary_key", "v8")]
        expected = -block["band_bn" if basis == "set" else "cash_set_bn"][("low", "high").index(end)]
        p7.require(f"both_sets_fiscal_{basis}_{end}", abs(fiscal-expected) < 1e-6, actual=fiscal,expected=expected)
        for record in chosen.to_dict("records"):
            rows.append(dict(basis=basis,end=end,channel="fiscal/"+record["financing"]+"/"+record["side"]+"/"+str(record["id"]),
                total_bn=-record["responsive_bn"], federal_bn=-record["federal_bn"], state_local_bn=-record["state_local_bn"],
                debt_eligible=record["financing"] == "cash"))
        social = 0.
        for item, values in amounts(model.source).items():
            value = -values[end]
            social += value
            rows.append(dict(basis=basis,end=end,channel="social/"+item,total_bn=value,federal_bn=0.,state_local_bn=0.,debt_eligible=False))
        target = -environment(model.source)["variants"]["central"]["pairing_bn"][end] if basis == "set" else expected + social
        p7.require(f"both_sets_full_channel_ledger_{basis}_{end}", abs(fiscal+social-target) < 1e-6)
    write(pd.DataFrame(rows), "p8_channel_ledger.csv", out)
