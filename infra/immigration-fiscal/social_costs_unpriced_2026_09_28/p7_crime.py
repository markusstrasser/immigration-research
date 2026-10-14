"""P7 crime corrections on the frozen v7 fiscal endpoints; no other producer writes.

Native-First: CSV readers and existing lane functions; no new data warehouse.
The baseline inputs are the executed, gated pre-P7 live run, preserved as records.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
INPUTS = HERE / "inputs"
STATS = ("low", "central", "high")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path, table):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(table)


def population_factor():
    frame = rows(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv")
    n = {r["count"]: r for r in frame}
    return (float(n["union|12_plus"]["row4"]) / float(n["cps_hispanic_civilian|12_plus"]["row4"])
            / (float(n["union|12_plus"]["published"]) / float(n["cps_hispanic_civilian|12_plus"]["published"])))


def response(spending, offence_share, outside_victim_share, payment_share):
    """One with/without crime-response rule, with named forward/reverse flows.

    Residential spending attributable to offending against outsiders has no
    population subtraction. Commercial costs pass through to purchasers: outsiders
    bear their share of group-attributable costs; removal also loses the group's
    contribution to security against other offenders. [ASSUMPTION] proportional
    spending response to the indicated offending and victim shares.
    """
    if not all(0 <= x <= 1 for x in (offence_share, outside_victim_share, payment_share)):
        raise ValueError("[BLOCKED] invalid crime response share")
    attributable = offence_share * outside_victim_share
    residential = spending["residential"] * attributable
    commercial_forward = spending["commercial"] * attributable * (1 - payment_share)
    reverse = spending["commercial"] * payment_share * (1 - offence_share)
    return dict(residential_forward_bn=residential, commercial_forward_bn=commercial_forward,
                commercial_reverse_bn=reverse, total_bn=residential + commercial_forward - reverse)


def security_spending(sc, source, arm):
    i = STATS.index(arm)
    _, lines = sc.s_total(i)
    codes = {"guards": "561612", "systems": "561621", "locksmiths": "561622",
             "armored": "561613", "investigation": "561611"}
    result = dict(residential=0.0, commercial=0.0, government=0.0)
    detail = []
    for line, amount in lines.items():
        if line in codes:
            amount = sc.to2024(source[codes[line]]["revenue_m_2022"] / 1e3, 2022)
        # Equipment has no primary payer split. Use the measured security-system
        # customer mix as an explicit proxy. In-house private guards are commercial.
        shares = source[codes.get(line, "561621")]
        crime = amount * sc.CRIME_SHARE[line][i]
        for payer in result:
            result[payer] += crime * shares[f"{payer}_share"]
        detail.append(dict(arm=arm, line=line, crime_driven_bn=crime,
                           residential_bn=crime * shares["residential_share"],
                           commercial_bn=crime * shares["commercial_share"],
                           government_bn=crime * shares["government_share"],
                           split_basis="security-system customer proxy [ASSUMPTION]" if line == "equipment" else "Census customer classes"))
    inhouse = sc.inhouse_bn * sc.CRIME_SHARE["guards"][i]
    result["commercial"] += inhouse
    detail.append(dict(arm=arm, line="inhouse_private_guards", crime_driven_bn=inhouse,
                       residential_bn=0.0, commercial_bn=inhouse, government_bn=0.0,
                       split_basis="private in-house employment [ASSUMPTION]"))
    national = sc.s_total(i)[0]
    if abs(sum(result.values()) - national) > 1e-6:
        raise ValueError("[BLOCKED] security payer split fails national closure")
    return result, detail


def active_detail(footing, standard):
    path = FISCAL / "crime_victim_cost_2026_09_23/derived/mortality_detail.csv"
    selected = [r for r in rows(path) if r["footing"] == footing and r["vsl_standard"] == standard
                and float(r["real_discount_rate"]) == 0 and r["missing_age_arm"] == "central"]
    if not selected:
        raise ValueError(f"[BLOCKED] no active victim arm: {footing}/{standard}")
    return selected


def crime_responses(sc, source, footing="mixed", standard="legacy", arm="central", factor=1.0,
                    payment_share=None, subtract_security=False, recipient_share=0.0):
    """Victims, security and fear evaluated together on one victim arm.

    The fear residual removes the same arm's victim unit harm from WTP. When
    subtract_security is on, *positive forward* security spending is removed before
    phi, never the net reverse-payment credit. Thus no security spending is priced
    a second time as fear. Negative fear is floored at zero [ASSUMPTION].
    """
    detail = active_detail(footing, standard)
    national = sc.NAT_VIOLENT_BN
    group_harm = sum(float(r["group_victimisations"]) * sc.UNIT_FULL[r["offence"]] / 1e9 for r in detail)
    outsider_harm = sum(float(r["outside_victims"]) * sc.UNIT_FULL[r["offence"]] / 1e9 for r in detail) * (1-recipient_share)
    violent_share = group_harm * factor / national
    violent_outside = outsider_harm / group_harm
    prop = [r for r in rows(sc.VICTIM / "property_proxy.csv") if r["price_set"] == "miller2021"]
    prop_share = sc.mex_prop_count if arm == "low" else sc.mex_prop_cost
    prop_all = sum(float(r["group_offences"]) * float(r["unit_victim_cost"]) for r in prop)
    prop_out = sum(float(r["outside_offences"]) * float(r["unit_victim_cost"]) for r in prop)
    offence_share = sc.W_PROP * prop_share * factor + (1 - sc.W_PROP) * violent_share
    attributable = (sc.W_PROP * prop_share * factor * prop_out / prop_all
                    + (1 - sc.W_PROP) * violent_share * violent_outside)
    # Property recipients are moved to the same outside-lineage boundary.
    attributable -= sc.W_PROP * prop_share * factor * prop_out / prop_all * recipient_share
    outside_share = attributable / offence_share
    if payment_share is None:
        # A population or offending sensitivity never changes this payment key.
        payment_share = json.loads((OUT / "payment_keys.json").read_text())["low"]["union_share"]
    spending, spend_detail = security_spending(sc, source, arm)
    security = response(spending, offence_share, outside_share, payment_share)
    victims = sum(float(r["cost_full"]) / 1e9 for r in detail) * factor * (1-recipient_share)
    wtp_residual = 0.0
    for r in detail:
        o, unit = r["offence"], float(r["unit_full"])
        n = float(r["outside_victims"]) * factor * (1-recipient_share)
        if o in ("Murder", "Rape/sexual assault", "Aggravated assault"):
            residual_unit = max(0.0, sc.to2024(sc.WTP2000[o], 2000) - unit)
        elif o == "Robbery":
            residual_unit = max(0.0, sc.ARMED_SHARE * (sc.to2024(sc.WTP2000["Armed robbery"], 2000) - unit))
            if arm != "high":
                residual_unit = min(residual_unit, unit)
        elif o == "Simple assault":
            residual_unit = max(0.0, sc.excess["Aggravated assault"] * unit) if arm == "high" else 0.0
        else:
            raise ValueError(f"[BLOCKED] undeclared fear offence {o}")
        wtp_residual += n * residual_unit / 1e9
    forward = security["residential_forward_bn"] + security["commercial_forward_bn"]
    residual = max(0.0, wtp_residual - (forward if subtract_security else 0.0))
    return dict(victims=victims, fear=sc.PHI[arm] * residual, security=security["total_bn"],
                wtp_minus_active_victims_bn=wtp_residual, security_forward_bn=forward,
                security_reverse_bn=security["commercial_reverse_bn"],
                national_spending=spending, spending_rows=spend_detail,
                offending_share=offence_share, outside_share=outside_share, payment_share=payment_share)


def full_span_components(doc, union_rows, bands, priced_spans):
    """Reconstruct the frozen published span first, then price its rows on row4.

    Air/crash ends use their executed full grids. Other noncrime endpoints keep
    the existing central row's population factor [APPROXIMATION]; no new rows
    from the pollution/crash/benefits worker are read here.
    """
    c = doc["channels"]
    published, row4, fiscal = {}, {}, {}
    for i, end in enumerate(("low", "high")):
        variant = "justice_grid_low_and_uncompensated_use_0.7" if end == "low" else "justice_grid_high"
        b = next(r for r in bands if r["case"] == "oct14" and r["variant"] == variant)
        fiscal[end] = float(b[f"cost_{end}_bn"])
        published[end] = dict(victims=c[f"victims_envelope_{end}"], property_crime=c[f"property_{end}"],
                              unreimbursed_care=c["unreimbursed_07_low" if end == "low" else "unreimbursed_high"],
                              congestion=doc["congestion_by_band_end_bn"]["full_span"]["low_end_lowest" if end == "low" else "high_end_highest"],
                              housing_gain=-c["housing_gain_max" if end == "low" else "housing_gain_min"])
        for r in doc["social_items_in_the_social_rows"]["items"]:
            published[end][r["item"]] = r[f"{end}_bn"]
        central = {r["item"]: r for r in rows(INPUTS / "baseline_restated_pairing.csv") if r["section"] == "row" and r["end"] in (end, "both")}
        row4[end] = {item: value * float(central[item]["factor"]) for item, value in published[end].items()}
        for item in ("pm25_consumption", "road_crash_externality"):
            r = next(r for r in priced_spans if r["item"] == item and r["measure"] == "absolute" and r["statistic"] == end)
            row4[end][item] = float(r["priced"])
    return published, row4, fiscal


def main():
    pins = json.loads((INPUTS / "pins.json").read_text())
    for r in pins["files"]:
        path = FISCAL.parent.parent / r["path"]
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != r["sha256"]:
            raise ValueError(f"[BLOCKED] missing or stale P7 baseline: {r['path']}")
    sc = load("p7_social_items", HERE / "items.py")
    src = load("p7_security_inputs", HERE / "security_inputs.py").load_security_inputs()
    totals = load("p7_totals", FISCAL / "sept24_propagation_2026_09_24/real_costs_totals.py")
    baseline = rows(INPUTS / "baseline_totals_oct14.csv")
    doc = json.loads((INPUTS / "baseline_totals_oct14.json").read_text())
    restated = rows(INPUTS / "baseline_restated_pairing.csv")
    bands_meta = json.loads((FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.json").read_text())
    lineage = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())["meta"]["lineage"]
    frame = {r["count"]: float(r["row4"]) for r in rows(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv")}
    frame_pub = {r["count"]: float(r["published"]) for r in rows(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv")}
    factor = (frame["union|12_plus"] / frame["cps_hispanic_civilian|12_plus"]
              / (frame_pub["union|12_plus"] / frame_pub["cps_hispanic_civilian|12_plus"]))
    keys = bands_meta["lineage_social_keys"]
    payment_keys = json.loads((OUT / "payment_keys.json").read_text())
    recipients = totals.lineage_recipient_shares(lineage, FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv")
    union_rows = {}
    for r in restated:
        if r["section"] == "row" and r["item"] != "fiscal":
            for e in (("low", "high") if r["end"] == "both" else (r["end"],)):
                union_rows[r["item"], e] = float(r["restated"])
    for r in restated:
        if r["section"] == "row_5plus":
            for e in (("low", "high") if r["end"] == "both" else (r["end"],)):
                union_rows[r["item"], e] = float(r["restated"])
    baseline_pair = [float(next(r["oct14"] for r in baseline if r["column"] == "pairing_on_priced_count"
                                and r["item"] == f"published pairing ({e})")) for e in ("low", "high")]
    baseline_span = [float(next(r["oct14"] for r in baseline if r["column"] == "full_span"
                                and r["item"] == f"{e} end")) for e in ("low", "high")]
    span_published, span_row4, span_fiscal = full_span_components(doc, union_rows,
        rows(FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.csv"),
        rows(INPUTS / "baseline_priced_spans.csv"))
    gates = []
    def gate(label, ok, detail=""):
        gates.append(dict(gate=label, result="PASS" if ok else "FAIL", detail=detail))
        if not ok:
            raise ValueError(f"[BLOCKED] {label}: {detail}")
    for i, end in enumerate(("low", "high")):
        rebuilt = span_fiscal[end] + sum(span_published[end].values())
        gate(f"published full span positive control {end}", abs(rebuilt-baseline_span[i]) < 1e-6,
             f"{rebuilt:.9f} / {baseline_span[i]:.9f}")
        rebuilt_pair = sum(union_rows[item, end] * (1 + (0.0 if totals.LINEAGE_ROW_KEYS[item][i] is None else
            keys["head_count"] if totals.LINEAGE_ROW_KEYS[item][i] == "head_count" else
            keys[f"{end}_end"][totals.LINEAGE_ROW_KEYS[item][i]])) for item in totals.LINEAGE_ROW_KEYS)
        fiscal = next(r for r in baseline if r["column"] == ("hispanic" if end == "low" else "custody") and r["item"] == f"fiscal main case ({end})")
        # Baseline rows are independently rounded at 6dp, so use the original
        # JSON lineage totals for the tighter population control.
        gate(f"baseline pairing positive control {end}", abs(float(fiscal["oct14"]) + rebuilt_pair - baseline_pair[i]) < 2e-6)
    old_fear = crime_responses(sc, src, "equal", "legacy")["fear"]
    gate("fear positive control reproduces former Miller arm", abs(old_fear - sc.historical_fear("mexican_origin", "central")) < 1e-6,
         f"{old_fear:.9f}")
    base_crime = {(item, e): union_rows[item, e] for item in ("victims", "fear_avoidance", "private_security") for e in ("low", "high")}
    configs = {
        "baseline": dict(),
        "security_comparator": dict(security=True),
        "fear_active_arm": dict(active=True),
        "uniform_dot": dict(standard="dot_uniform", active=True),
        "life_years_crime_only": dict(standard="dot_life_years", active=True),
        "mixed_both_ends": dict(mixed=True),
        "lineage_boundary": dict(boundary=True),
        "stacked_legacy": dict(security=True, active=True, mixed=True, boundary=True),
        "stacked_dot": dict(security=True, active=True, mixed=True, boundary=True, standard="dot_uniform"),
        "stacked_dot_recipient_zero": dict(security=True, active=True, mixed=True, boundary=True, standard="dot_uniform", recipient_mult=0.0),
        "stacked_dot_recipient_twice": dict(security=True, active=True, mixed=True, boundary=True, standard="dot_uniform", recipient_mult=2.0),
        "stacked_life_years_crime_only": dict(security=True, active=True, mixed=True, boundary=True, standard="dot_life_years"),
        "arrest_high_beside": dict(security=True, active=True, mixed=True, boundary=True, standard="dot_uniform", arrest=True),
    }
    result, changed_rows, joint_values = [], [], []
    adopted = None
    adopted_outside, adopted_lineage, adopted_lineage_before, adopted_parameters = {}, {}, {}, {}
    spending_rows = None
    for scenario, cfg in configs.items():
        scenario_recipients = {item: value * cfg.get("recipient_mult", 1.0) for item,value in recipients.items()}
        pairing, span = list(baseline_pair), [0.0, 0.0]
        union_pair, union_span = [0.0, 0.0], [0.0, 0.0]
        for i, end in enumerate(("low", "high")):
            footing = "mixed" if end == "low" else (
                "arrest" if cfg.get("arrest") else "custody")
            # Mixed-group correction travels to custody with the same active arm.
            if end == "high" and not cfg.get("mixed"):
                footing = "custody_unmixed"
            standard = cfg.get("standard", "legacy")
            # Producer footings include corrected custody. For the uncorrected
            # historical control use the equal arm times its stored custody ratio.
            unmixed = footing == "custody_unmixed"
            active = "equal" if unmixed else footing
            custody_ratio = doc["channels"]["victims_custody"] / doc["channels"]["victims_equal"] if unmixed else 1.0
            live = crime_responses(sc, src, active, standard, factor=factor * custody_ratio,
                                   payment_share=payment_keys[end]["union_share"],
                                   subtract_security=bool(cfg.get("security")))
            crime_key = totals.LINEAGE_ROW_KEYS["victims"][i]
            added_offending = keys[f"{end}_end"][crime_key]
            recipient = scenario_recipients["victims"] if cfg.get("boundary") else 0.0
            union_out = crime_responses(sc, src, active, standard, factor=factor * custody_ratio,
                payment_share=payment_keys[end]["union_share"], subtract_security=bool(cfg.get("security")), recipient_share=recipient)
            lineage_out = crime_responses(sc, src, active, standard, factor=factor * custody_ratio * (1+added_offending),
                payment_share=payment_keys[end]["lineage_share"], subtract_security=bool(cfg.get("security")), recipient_share=recipient)
            current = {k: base_crime[k, end] for k in ("victims", "fear_avoidance", "private_security")}
            if cfg.get("mixed") or "standard" in cfg or cfg.get("arrest"):
                current["victims"] = live["victims"]
            if cfg.get("active"):
                current["fear_avoidance"] = live["fear"]
            if cfg.get("security"):
                current["private_security"] = live["security"]
                # Reconcile WTP against forward security even for the isolated
                # comparator change, holding its former victim arm fixed.
                if not cfg.get("active"):
                    current["fear_avoidance"] = max(0.0, current["fear_avoidance"] - sc.PHI["central"] * live["security_forward_bn"])
            current_out = {item: value * (1-recipient) for item, value in current.items()}
            lineage_current = {item: value * (1+added_offending) * (1-recipient) for item, value in current.items()}
            if cfg.get("active"):
                current_out["fear_avoidance"], lineage_current["fear_avoidance"] = union_out["fear"], lineage_out["fear"]
            if cfg.get("security"):
                current_out["private_security"], lineage_current["private_security"] = union_out["security"], lineage_out["security"]
                if not cfg.get("active"):
                    current_out["fear_avoidance"] = max(0.0, base_crime["fear_avoidance",end]*(1-recipient) - sc.PHI["central"]*union_out["security_forward_bn"])
                    lineage_current["fear_avoidance"] = max(0.0, base_crime["fear_avoidance",end]*(1+added_offending)*(1-recipient) - sc.PHI["central"]*lineage_out["security_forward_bn"])
            delta = sum(value-base_crime[item,end]*(1+added_offending) for item,value in lineage_current.items())
            if cfg.get("boundary"):
                delta -= sum(value * (1 + (0.0 if totals.LINEAGE_ROW_KEYS[item][i] is None else
                    keys["head_count"] if totals.LINEAGE_ROW_KEYS[item][i] == "head_count" else
                    keys[f"{end}_end"][totals.LINEAGE_ROW_KEYS[item][i]])) * scenario_recipients[item]
                    for (item, e), value in union_rows.items() if e == end and item not in current)
            pairing[i] += delta
            if scenario in ("stacked_dot", "stacked_life_years_crime_only"):
                for population, values in (("39.71M union → outside lineage", current_out), ("42.75M lineage → outsiders", lineage_current)):
                    joint_values.append(dict(scenario=scenario, end=end, population=population, vsl_standard=standard,
                                             victims_bn=values["victims"], fear_bn=values["fear_avoidance"],
                                             victims_plus_fear_bn=values["victims"]+values["fear_avoidance"],
                                             security_bn=values["private_security"],
                                             mortality_scope="crime only; pollution age mix not identified here" if standard=="dot_life_years" else "DOT uniform mortality"))
            union_social = {item: current_out.get(item, value * (1-scenario_recipients[item] if cfg.get("boundary") else 1))
                            for (item, e), value in union_rows.items() if e == end}
            # The fiscal v7 band already contains D; the union-only report holds
            # that same fiscal row fixed and removes only D's social sender rows.
            fiscal_live = baseline_pair[i] - sum(value * (1 + (0.0 if totals.LINEAGE_ROW_KEYS[item][i] is None else
                keys["head_count"] if totals.LINEAGE_ROW_KEYS[item][i] == "head_count" else
                keys[f"{end}_end"][totals.LINEAGE_ROW_KEYS[item][i]])) for (item,e),value in union_rows.items() if e == end)
            union_pair[i] = fiscal_live + sum(union_social.values())
            changed_rows.extend(dict(scenario=scenario, end=end, item=item, baseline_union_bn=base_crime[item, end],
                                     union_bn=value, delta_union_bn=value-base_crime[item, end]) for item, value in current.items())
            # Full span: keep the historical span's footing and every noncrime
            # component fixed; recompute crime and fear at its envelope arm.
            span_arm = "low" if end == "low" else "high"
            envelope_footing = f"envelope_{end}" + ("" if cfg.get("mixed") else "_unmixed")
            envelope_standard = cfg.get("standard", "legacy" if end == "low" else "dot_uniform")
            envelope = crime_responses(sc, src, envelope_footing, envelope_standard, arm=span_arm, factor=factor,
                                       payment_share=payment_keys[end]["union_share"],
                                       subtract_security=bool(cfg.get("security")))
            envelope_union = crime_responses(sc, src, envelope_footing, envelope_standard, arm=span_arm, factor=factor,
                payment_share=payment_keys[end]["union_share"], subtract_security=bool(cfg.get("security")), recipient_share=recipient)
            envelope_lineage = crime_responses(sc, src, envelope_footing, envelope_standard, arm=span_arm, factor=factor*(1+added_offending),
                payment_share=payment_keys[end]["lineage_share"], subtract_security=bool(cfg.get("security")), recipient_share=recipient)
            components = dict(span_row4[end])
            if "standard" in cfg or cfg.get("mixed"):
                components["victims"] = envelope["victims"]
            if cfg.get("active"):
                components["fear_avoidance"] = envelope["fear"]
            if cfg.get("security"):
                components["private_security"] = envelope["security"]
                if not cfg.get("active"):
                    components["fear_avoidance"] = max(0.0, components["fear_avoidance"] - sc.PHI[span_arm] * envelope["security_forward_bn"])
            for item, value in components.items():
                key = totals.LINEAGE_ROW_KEYS[item][i]
                share = 0.0 if key is None else keys["head_count"] if key == "head_count" else keys[f"{end}_end"][key]
                recipient = scenario_recipients[item] if cfg.get("boundary") else 0.0
                lv, uv = value * (1+share)*(1-recipient), value*(1-recipient)
                label = {"victims":"victims", "fear_avoidance":"fear", "private_security":"security"}.get(item)
                changed = ((item == "victims" and ("standard" in cfg or cfg.get("mixed"))) or
                           (item == "fear_avoidance" and cfg.get("active")) or
                           (item == "private_security" and cfg.get("security")))
                if changed:
                    lv, uv = envelope_lineage[label], envelope_union[label]
                if item == "fear_avoidance" and cfg.get("security") and not cfg.get("active"):
                    lv = max(0, span_row4[end][item]*(1+share)*(1-recipient) - sc.PHI[span_arm]*envelope_lineage["security_forward_bn"])
                    uv = max(0, span_row4[end][item]*(1-recipient) - sc.PHI[span_arm]*envelope_union["security_forward_bn"])
                span[i] += lv
                union_span[i] += uv
                if item not in ("victims", "fear_avoidance", "private_security"):
                    gate(f"noncrime union span unchanged {scenario}/{end}/{item}", value == span_row4[end][item])
            span[i] += span_fiscal[end]
            union_span[i] += span_fiscal[end]
            if scenario == "stacked_dot":
                if adopted is None:
                    adopted = {}
                adopted[end] = current
                adopted_outside[end], adopted_lineage[end] = current_out, lineage_current
                adopted_parameters[end] = dict(offending_share_union=live["offending_share"],
                    outside_share_before_boundary=live["outside_share"], recipient_share=recipient,
                    added_offending_share=added_offending, payment_share_union=payment_keys[end]["union_share"],
                    payment_share_lineage=payment_keys[end]["lineage_share"], national_spending=live["national_spending"])
                before = crime_responses(sc, src, active, standard, factor=factor*custody_ratio*(1+added_offending),
                    payment_share=payment_keys[end]["lineage_share"], subtract_security=True)
                adopted_lineage_before[end] = {"victims":before["victims"], "fear_avoidance":before["fear"], "private_security":before["security"]}
                spending_rows = live["spending_rows"]
        result.append(dict(scenario=scenario, pairing_low_bn=pairing[0], pairing_high_bn=pairing[1],
                           delta_low_bn=pairing[0]-baseline_pair[0], delta_high_bn=pairing[1]-baseline_pair[1],
                           full_span_low_bn=span[0], full_span_high_bn=span[1],
                           union_social_only_pairing_low_bn=union_pair[0], union_social_only_pairing_high_bn=union_pair[1],
                           union_social_only_full_span_low_bn=union_span[0], union_social_only_full_span_high_bn=union_span[1],
                           delta_union_low_bn=0.0 if not result else union_pair[0]-result[0]["union_social_only_pairing_low_bn"],
                           delta_union_high_bn=0.0 if not result else union_pair[1]-result[0]["union_social_only_pairing_high_bn"],
                           review_bar_5bn="clears" if max(abs(pairing[i]-baseline_pair[i]) for i in range(2)) >= 5 else "below",
                           mortality_scope="crime-only life-year sensitivity; pollution/crash DOT held; not a uniform life-year total" if cfg.get("standard")=="dot_life_years" else "noncrime valuations held; DOT uniform in stacked_dot",
                           span_basis="row4; PM/crash full grids, other noncrime ends at existing population factors [APPROXIMATION]; D at sender keys"))
    selected = next(r for r in result if r["scenario"] == "stacked_dot")
    payload = dict(case="oct14", vsl_standard="dot_uniform", baseline_pairing_bn=baseline_pair,
                   pairing_bn=[selected[f"pairing_{e}_bn"] for e in ("low", "high")],
                   full_span_bn=[selected[f"full_span_{e}_bn"] for e in ("low", "high")],
                   union_crime_rows=adopted, recipient_shares=recipients,
                   union_crime_rows_outside_lineage=adopted_outside, lineage_crime_rows=adopted_lineage,
                   lineage_crime_rows_before_boundary=adopted_lineage_before,
                   response_parameters=adopted_parameters,
                   assumptions=["security response proportional to offending against outsiders",
                                "business and nonprofit security passes through via consumption",
                                "equipment payer mix equals security-system customer mix",
                                "WTP residual excludes forward security before phi",
                                "added descendants have average outsider exposure within recipient age range"],
                   uncertainty="No joint replicate SE: national source series and victim-arm uncertainty are not jointly replicated.")
    p7_items = []
    for item, (_, valuation, overlaps) in totals.SOCIAL_CONTRACTS.items():
        if item not in ("fear_avoidance", "private_security"):
            continue
        for end in ("low", "high"):
            central = adopted[end][item]
            estimates = [crime_responses(sc, src, "mixed" if end == "low" else "custody", "dot_uniform", arm=a,
                                        factor=factor, payment_share=payment_keys[end]["union_share"],
                                        subtract_security=True)["fear" if item == "fear_avoidance" else "security"] for a in STATS]
            p7_items.append(dict(item=item, group="mexican_origin", end=end, measure="absolute", comparator="with_without",
                                 beneficiary_population="residents_outside_union", valuation_basis=valuation,
                                 overlap_set=json.dumps(list(overlaps)), low_bn=min(estimates), central_bn=central,
                                 high_bn=max(estimates), vsl_standard="dot_uniform"))
    sampling_rows = []
    payment_source = next(r for r in rows(FISCAL / "consumption_key_2026_09_24/derived/key_specs.csv") if r["spec"] == "both_corridor_net_h2")
    p, sd = float(payment_source["key_share"]), float(payment_source["key_share_se_cps"])
    for footing in ("mixed", "custody"):
        def security_fear(q):
            r = crime_responses(sc, src, footing, "dot_uniform", payment_share=q, subtract_security=True)
            return r["security"]+r["fear"]
        centre, plus, minus = security_fear(p), security_fear(p+sd), security_fear(p-sd)
        derivative = (plus-minus)/(2*sd)
        gate(f"conditional payment response is affine over 8 reported CPS SDR SEs {footing}",
             abs(security_fear(p+8*sd)-centre-derivative*8*sd) < 1e-10)
        sampling_rows.append(dict(component="security+fear", footing=footing, population="published CPS union; other inputs held",
                                  se_bn=abs(derivative)*sd,
                                  scope="Exact linear propagation of the source's 160-replicate CPS SDR payment-key SE; not a joint or row4 replicate SE"))
        victim_se = next(r for r in rows(FISCAL / "crime_victim_cost_2026_09_23/derived/mortality_arms.csv")
                         if r["footing"]==footing and r["vsl_standard"]=="dot_uniform" and float(r["real_discount_rate"])==0 and r["missing_age_arm"]=="central")
        sampling_rows.append(dict(component="nonfatal_victims", footing=footing, population="row4 union",
                                  se_bn=float(victim_se["nonfatal_conditional_se_bn"])*factor,
                                  scope="Understated source NCVS independent-cell GVP delta method; not a replicate SE or joint crime SE"))
    write_csv(OUT / "p7_sampling.csv", sampling_rows)
    write_csv(OUT / "p7_joint_valuation.csv", joint_values)
    write_csv(OUT / "p7_items.csv", p7_items)
    write_csv(OUT / "p7_changes.csv", result)
    write_csv(OUT / "p7_crime_rows.csv", changed_rows)
    write_csv(OUT / "p7_security_spending.csv", spending_rows)
    write_csv(OUT / "p7_gates.csv", gates)
    source_paths = [INPUTS / "pins.json", INPUTS / "security_pins.json", INPUTS / "report_checks_pins.json",
                    OUT / "p7_items.csv", OUT / "security_inputs.json", OUT / "payment_keys.json", HERE / "payment_keys.cjs", HERE / "items.py", HERE / "p7_crime.py",
                    HERE / "security_inputs.py", FISCAL / "crime_victim_cost_2026_09_23/derived/mortality_detail.csv",
                    FISCAL / "crime_victim_cost_2026_09_23/derived/mortality_arms.csv",
                    FISCAL / "crime_victim_cost_2026_09_23/derived/vsl_standard.json",
                    FISCAL / "crime_victim_cost_2026_09_23/inputs/pins.json",
                    FISCAL / "main_case_2026_10_14/derived/corrections.json",
                    FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.json"]
    source_paths += [FISCAL.parent.parent / r["path"] for r in pins["files"]]
    payload["sources_sha256"] = {str(path.relative_to(FISCAL.parent.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in source_paths}
    (OUT / "p7_payload.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(selected, indent=2))


if __name__ == "__main__":
    main()
