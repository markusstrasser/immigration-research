"""Current social producer adapter; each recipient vector retains its own source total.

Native-First: adapt the authoritative JSON to the existing incidence allocator.
Budget counterflows are separate ledger rows with the same mortality recipient key.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np

import p7_frames as p7

SOURCE_REL = "sept24_propagation_2026_09_24/derived/oct15/real_costs_totals.json"
PM_ROWS = ("pm25_consumption", "pm25_respending", "pm25_government_side")


def source(wl):
    data = json.loads(p7.pin(wl.FISCAL / SOURCE_REL, wl).read_text())
    env = data["v8_social_environment"]
    extra = env["v8_added_social"]
    p7.require("item11_social_consumption_shift", abs(extra["item11_consumption_factor"] +
        extra["item11_m5_consumption_bn"] / extra["union_consumption_keyed_receipts_bn"]) < 1e-12)
    for end in ("low", "high"):
        for item in ("victims", "property_crime", "fear_avoidance", "private_security"):
            row = env["variants"]["central"]["parts"][end]["v8_added_by_item"][item]
            p7.require(f"no_added_crime_sender_{end}_{item}", row["share"] == 0 and row["added_people_bn"] == 0)
    return data


def amounts(data, variant="central"):
    env = data["v8_social_environment"]
    rows = {r["item"]: dict(r["total_by_end_bn"]) for r in env["current_social_rows"]}
    central = env["variants"]["central"]
    # The producer's PM row already contains re-spending. Separate it once.
    rows["pm25_respending"] = {e: central["parts"][e]["terms"]["pm_respending"] for e in ("low", "high")}
    rows["pm25_consumption"] = {e: rows["pm25_consumption"][e] - rows["pm25_respending"][e] for e in ("low", "high")}
    if variant != "central":
        selected = env["variants"][variant]
        for end in ("low", "high"):
            old, new = central["parts"][end], selected["parts"][end]
            budget_delta = 0.
            for term, item in (("pm_respending", "pm25_respending"), ("government_side", "pm25_government_side")):
                replacement = new["terms"].get(term, 0)
                if term == "government_side":
                    replacement += new["terms"].get("government_legacy_response", 0)
                change = replacement - old["terms"].get(term, 0)
                rows[item][end] += change
                budget_delta += change
            remaining = selected["pairing_bn"][end] - central["pairing_bn"][end] - budget_delta
            # Named variants can also change crime/volunteering/timing. The
            # caller reports their complete aggregate delta explicitly, rather
            # than pretend an unlocated change is an observed victim identity.
            if abs(remaining) > 1e-9:
                name = "variant_fiscal_justice" if variant == "matched_justice_footing" else "variant_unlocated"
                rows.setdefault(name, dict(low=0., high=0.))[end] = remaining
    return rows


def normalized(data):
    out = copy.deepcopy(data)
    values = amounts(data)
    primary = out["lineage_social_rows"]
    primary["rows"] = [dict(item=k, **{f"union_{e}_bn": v[e] for e in ("low", "high")},
                            added_low_bn=0., added_high_bn=0.) for k, v in values.items()]
    primary["union_social_bn"] = dict(data["v8_social_environment"]["current_social_by_end_bn"])
    primary["added_social_bn"] = dict(low=0., high=0.)
    return out


def allocate(wl, d, I, ch, meta, weights, rule, ctx, notes):
    data = source(wl)
    arrays, values, table = p7.social_channels(wl, d, I, ch, meta, weights,
        "lineage", rule, ctx, notes=notes, source_data=normalized(data))
    for end in ("low", "high"):
        target = data["v8_social_environment"]["current_social_by_end_bn"][end]
        p7.check_total(f"round3_social_ledger_{end}", sum(a[end] for a in arrays.values()), weights, -target)
    return arrays, values, table


def uncertainty_ratio(data, item, setting, channels, weights):
    if setting == "central" or item == "source_rounding":
        return 1.
    if item in ("pm25_respending", "pm25_government_side"):
        # The live JSON exports point counterflows at each fiscal endpoint.
        # Historical consumer-exposure bounds do not create uncertainty in the
        # producer's separately declared funding/purchase amounts.
        return 1.
    producer_item = "pm25_consumption" if item in PM_ROWS else item
    producers = {r["item"]: r for r in data["social_items_in_the_social_rows"]["items"]}
    if producer_item in producers:
        row = producers[producer_item]
        p7.require(f"live_social_range_{item}", row["low_bn"] <= row["central_bn"] <= row["high_bn"])
        return row[f"{setting}_bn"] / row["central_bn"]
    channel = {"victims": "crime_victims", "property_crime": "property_crime",
               "unreimbursed_care": "unreimbursed_care", "congestion": "congestion"}.get(item)
    if channel:
        return p7.total(channels[channel][setting], weights) / p7.total(channels[channel]["central"], weights)
    if item == "housing_gain":
        return p7.total(channels["renters"][setting] + channels["landlords"][setting], weights) / p7.total(
            channels["renters"]["central"] + channels["landlords"]["central"], weights)
    raise RuntimeError(f"[BLOCKED] live social uncertainty missing: {item}")
