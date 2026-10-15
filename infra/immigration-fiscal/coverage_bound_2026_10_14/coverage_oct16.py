"""Oct16 coverage replay on preserved signed v8 person kernels.

Only oct16 outputs are written. Source item builders supply the response,
receipt and capital changes. Native calibration and tenure use the count lane's
actual builders and person weights. No national or generic per-head scaling.
"""
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import coverage_bound as C
from coverage_oct15 import DEFINITIONS, national_constructions
from source_tables import load

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget
sys.path.insert(0, str(FISCAL / "count_composition_r5_2026_10_15"))
from measure import person_inputs
from tenure import fixed_count_tenure, tenure_rates, transfer_count_tenure
from mixed_interaction import item10_flags

GENS, ENDS = C.GENS, C.ENDS


def read(path):
    return json.loads(path.read_text())


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def load_kernel(basis, vintage):
    audit_path = LANE / f"derived/pricing_audit_{vintage}_{basis}.json"
    audit = read(audit_path)
    manifest = LANE / f"inputs/pricing_dependencies_{vintage}_{basis}.json"
    cache = LANE / f"_cache/{vintage}/{basis}/pricing.npz"
    C.validate_cache_receipt(audit, manifest, cache)
    with np.load(cache) as stored:
        data = {k: stored[k] for k in ("weights", "added_weights", "generation", "age", "sex", "arrival", "hispanic",
                "person_ph_seq", "person_pppos", "base_piece_prices", "constructed_piece_prices", "other_piece_prices")}
    C.require(audit["basis"] == basis and audit["case"] == "oct15", "oct16 source kernel identity")
    return data, audit


def transform(data, audit, snapshot, basis):
    """Exact linear transforms on the declared source drivers, not totals."""
    meta = snapshot["sets"][basis]
    military = snapshot["military"]
    posts = meta["posts"]
    admin = read(FISCAL / "spending_keys_r5_2026_10_15/derived/item14.json")
    college = read(FISCAL / "spending_keys_r5_2026_10_15/derived/item15.json")
    basket = read(FISCAL / "consumption_tax_bases_r5_2026_10_15/derived/item.json")["arms"]["household_joint"]["receipt_ratios"]
    ratios = {military["line"]: military["response"],
              "income_security_services": admin["central"]["by_allocation"]["personal"]["share_ratio"]}
    extension = military.get("extension", {})
    for src in extension.get("lines", []):
        fraction = src["fraction"]
        if fraction != 1:
            # Same principal national bridge used by source deltaParts.
            parts = posts["veterans_compensation"]["by_end"]["low"]["parts"]
            candidates = [p for p in parts if p.get("source_line") == src["line"] and p.get("part") == src.get("part", "extension")]
            C.require(bool(candidates), "military extension source fraction absent")
            fraction = candidates[0]["fraction"]
        ratios[src["line"]] = 1-fraction
    traces = []
    new_pieces, new_base, new_constructed = [], [], []
    for i, piece in enumerate(audit["denominator_pieces"]):
        end, line = piece["end"], piece["source_line"]
        old_rate = .02 if end == "low" else .03
        factor, rules = 1., []
        if piece["source_side"] == "spending" and line in ratios:
            factor *= ratios[line]
            rules.append("13" if line != "income_security_services" else "14")
        if piece["source_side"] == "receipt" and line in basket:
            factor *= basket[line]
            rules.append("18")
        if piece["source_side"] == "capital":
            factor *= snapshot["rate"]/old_rate
            rules.append("20")
            if line in ("college", "college_user_fees"):
                factor *= college["central_response"]
                rules.append("15_capital")
                component = next(c for c in meta["ends"][end]["capital"] if c["id"] == "college")
                coefficient = college["national_exposure_bn"]/(component["stock_charged_bn"]*old_rate)*(college["central_response"]-1)
                operating = {**piece, "line": f"oct16_college_operating:{piece['line']}", "source_line": "education_services",
                    "source_side": "spending", "category": "education", "economic_class": "fiscal_line",
                    "source_response": 1, "source_key": "education_mix",
                    "oct16_rule": "item15 additions' source capital-use proxy; tuition and Pell held"}
                new_pieces.append(operating)
                new_base.append(data["base_piece_prices"][i].copy()*coefficient)
                new_constructed.append(data["constructed_piece_prices"][i].copy()*coefficient)
        if rules:
            traces.append({"piece": i, "end": end, "generation": piece["generation"], "line": line,
                           "rules": rules, "multiplicative_factor": factor})
            observed_factor = factor
            if (os.environ.get("ITEM18_CARRIER_MODE", "source_evaluator") == "source_evaluator"
                    and piece["source_side"] == "receipt" and line in basket
                    and piece["line"].startswith("union_completion_")):
                observed_factor /= basket[line]
            data["base_piece_prices"][i] *= observed_factor
            data["constructed_piece_prices"][i] *= factor
    if new_pieces:
        audit["denominator_pieces"].extend(new_pieces)
        data["base_piece_prices"] = np.concatenate((data["base_piece_prices"], np.asarray(new_base)))
        data["constructed_piece_prices"] = np.concatenate((data["constructed_piece_prices"], np.asarray(new_constructed)))
    return traces


def integrate(data, audit, mass, added_mass=None, observed=False):
    added_mass = np.zeros_like(mass) if added_mass is None else added_mass
    matrix = data["base_piece_prices" if observed else "constructed_piece_prices"]
    lines = {end: [] for end in ENDS}
    for i, p in enumerate(audit["denominator_pieces"]):
        value = float(matrix[i] @ (mass+added_mass))
        lines[p["end"]].append({**p, "coverage_bn": value})
    for i, p in enumerate(audit["other_pieces"]):
        weights = {"both": mass+added_mass, "identified": mass, "added": added_mass}[p["population"]]
        value = float(data["other_piece_prices"][i] @ weights)
        lines[p["end"]].append({**p, "source_line": p["line"], "source_side": "post_engine",
            "economic_class": "unclassified_residual", "level": "unclassified", "coverage_bn": value})
    out = {}
    for end in ENDS:
        private = induced = fiscal = unclassified = 0.
        capital = {lev: 0. for lev in ("federal", "state_local")}
        for p in lines[end]:
            kind, cost = p["economic_class"], p["coverage_bn"]
            if kind == "capital_return":
                capital[p["level"]] += cost
            elif kind == "production":
                src = p["source_production"]
                C.require(abs(src["cost_bn"]) > 1e-12 or cost == 0, "oct16 production denominator")
                p["P_bn"] = cost*src["private_wtp_bn"]/src["cost_bn"] if src["cost_bn"] else 0.
                p["F_bn"] = cost*src["fiscal_weight"]*src["induced_receipts_bn"]/src["cost_bn"] if src["cost_bn"] else 0.
                private += p["P_bn"]
                induced += p["F_bn"]
            elif kind == "fiscal_line":
                fiscal += cost
            else:
                unclassified += cost
        by_gen = {g: sum(p["coverage_bn"] for p in lines[end] if p["generation"] == g) for g in GENS}
        total = sum(by_gen.values())
        C.require(abs(sum(capital.values())+fiscal+unclassified-private-induced-total) < 1e-9, "oct16 typed economic coverage closure")
        decomposition = {"line_parts": lines[end], "total_cost_bn": total, "capital_by_level_bn": capital,
            "production": {"P_bn": private, "F_bn": induced, "allocation_rule": "generation_ratio", "approximation": True,
                "scope": "preserved source generation-end P/F ratios on the source earnings-key pieces"},
            "unclassified_bn": unclassified, "classified_fiscal_line_bn": fiscal,
            "classified_fiscal_with_production_F_bn": fiscal-induced,
            "sign_convention": "total = capital + fiscal lines + unclassified - P - F",
            "borrowing_rule": "capital return and private P are not borrowing; unclassified parts require the consumer's financing rule"}
        if audit["basis"] == "cash":
            decomposition["classified_cash_fiscal_bn"] = fiscal-induced
        out[end] = {"coverage_bn": total, "total_bn": total, "by_generation": by_gen,
            "by_generation_bn": by_gen, "decomposition": decomposition}
    return out


def add_ends(a, b, scale=1):
    out = {}
    for end in ENDS:
        parts = {g: a[end]["by_generation_bn"][g]+scale*b[end]["by_generation_bn"][g] for g in GENS}
        out[end] = {"total_bn": sum(parts.values()), "by_generation_bn": parts}
    return out


def calculate(basis, snapshot):
    data, audit = load_kernel(basis, "oct15")
    rates, base = load()
    traces = transform(data, audit, snapshot, basis)
    w, aw = data["weights"][:, 0], data["added_weights"][:, 0]
    scenarios = {}
    for name, options in DEFINITIONS.items():
        f, af = C.factors(data, rates, base, **options)
        ends = integrate(data, audit, w*f, aw*af)
        counts = {g: float((w*f)[data["generation"] == i].sum()) for i, g in enumerate(GENS)}
        counts["added"] = float((aw*af).sum())
        adults = {g: float((w*f)[(data["generation"] == i) & (data["age"] >= 18)].sum()) for i, g in enumerate(GENS)}
        adults["G3plus"] += float((aw*af)[data["age"] >= 18].sum())
        scenarios[name] = {"ends": ends, "implied_net_missing_people": counts, "adults_by_generation": adults}
    old = read(LANE / "derived/coverage_bound_oct15.json")["sets"][basis]
    central_f, central_af = C.factors(data, rates, base)
    adult_mask = data["age"] >= 18
    adult_cost = integrate(data, audit, w*central_f*adult_mask, aw*central_af*adult_mask)
    minor_cost = integrate(data, audit, w*central_f*~adult_mask, aw*central_af*~adult_mask)
    for end in ENDS:
        z = scenarios["central"]["ends"][end]
        z["adult_cost_by_generation_bn"] = adult_cost[end]["by_generation_bn"]
        z["minor_cost_by_generation_bn"] = minor_cost[end]["by_generation_bn"]
        z["adult_minor_uncertainty_rule"] = "own oct16 exact-age partition; no new missing-count SE measured"
        z["cps_replicate_se_bn"] = old["ends"][end]["cps_replicate_se_bn"]
        z["cps_replicate_se_pricing"] = "carried v8 own-price conditional SE; oct16 all-replicate price coefficients not rebuilt"
    declared, interactions = {}, {}
    for end in ENDS:
        p = snapshot["sets"][basis]["posts"]
        by_item = {}
        for name in ("veterans_compensation", "income_security_administration", "public_college_response"):
            if name in p:
                by_item[name] = sum(q["delta_bn"] for q in p[name]["by_end"][end]["parts"] if q["population"] == "coverage")
        if "veterans_compensation" not in p:
            by_item["veterans_compensation"] = sum(q["coverage_bn"]*(snapshot["military"]["response"]-1)
                for q in old["ends"][end]["decomposition"]["line_parts"] if q.get("source_side") == "spending"
                and q.get("source_line") == snapshot["military"]["line"])
        by_item["consumption_tax_bases"] = p["consumption_tax_bases"]["by_end"][end]["total_bn"]
        by_item["one_rate"] = sum(old["ends"][end]["decomposition"]["capital_by_level_bn"].values())*(snapshot["rate"]/(.02 if end == "low" else .03)-1)
        declared[end] = by_item
        change = scenarios["central"]["ends"][end]["total_bn"]-old["ends"][end]["total_bn"]
        college = read(FISCAL / "spending_keys_r5_2026_10_15/derived/item15.json")
        capital_cross = sum(p["coverage_bn"] for p in old["ends"][end]["decomposition"]["line_parts"]
            if p.get("source_side") == "capital" and p.get("source_line") in ("college", "college_user_fees"))
        capital_cross *= (college["central_response"]-1)*(snapshot["rate"]/(.02 if end == "low" else .03)-1)
        C.require(abs(change-sum(by_item.values())-capital_cross) < 1e-9, "oct16 item12 declared deltas plus exact 15x20 interaction")
        interactions[end] = {"coverage_change_bn": change, "declared_sum_bn": sum(by_item.values()),
                             "interaction_bn": change-sum(by_item.values()), "item15_x_item20_bn": capital_cross,
                             "unexplained_gap_bn": change-sum(by_item.values())-capital_cross}
    del data
    # Count lane's own final-routing provenance, repriced without altering its outputs.
    data, audit = load_kernel(basis, "oct15_final_routing")
    transform(data, audit, snapshot, basis)
    tenure, factor = person_inputs(data)
    payload = read(FISCAL / f"main_case_2026_10_15/derived/corrections{'_cash' if basis == 'cash' else ''}.json")
    flags = item10_flags(data, payload)
    w = data["weights"][:, 0]
    f, _ = C.factors(data, rates, base)
    native = w*factor
    fixed, _ = fixed_count_tenure(data, tenure, w, rates, base)
    joint, _ = fixed_count_tenure(data, tenure, native, rates, base)
    transfer = transfer_count_tenure(data, tenure, rates, base)
    zero = np.zeros_like(w)
    completion_delta = data["added_weights"][:, 0]*(factor-1)*flags["nonreporter"]
    changes, count_parts = {}, []
    for name, observed, missing, added in (
        ("item16", native-w, native*f-w*f, completion_delta),
        ("item17", zero, w*(fixed-f), zero),
        ("joint", native-w, native*joint-w*f, completion_delta),
        ("joint_count_transfer", native-w, native*transfer-w*f, completion_delta)):
        obs = integrate(data, audit, observed, added, observed=True)
        cov = integrate(data, audit, missing)
        changes[name] = add_ends(obs, cov)
        for end in ENDS:
            aa, bb = obs[end]["decomposition"]["line_parts"], cov[end]["decomposition"]["line_parts"]
            C.require(len(aa) == len(bb), "own-price count part shape")
            for a, b in zip(aa, bb, strict=True):
                count_parts.append({"scenario": name, "end": end, "generation": a["generation"],
                    "line": a["line"], "source_line": a["source_line"], "source_side": a["source_side"],
                    "category": a.get("category", "residual"), "economic_class": a["economic_class"], "level": a["level"],
                    "source_response": a.get("source_response"), "source_key": a.get("source_key"),
                    "observed_change_bn": a["coverage_bn"], "coverage_change_bn": b["coverage_bn"],
                    "change_bn": a["coverage_bn"]+b["coverage_bn"], "complete_use_excluded": a.get("administratively_complete_use", False)})
    original_items = read(FISCAL / "count_composition_r5_2026_10_15/derived/items.json")["sets"][basis]
    count16 = copy.deepcopy(original_items["item16"])
    count17 = copy.deepcopy(original_items["joint"])
    count16["by_end"] = changes["item16"]
    count17["by_end"] = add_ends(changes["joint"], changes["item16"], -1)
    count17["population_change"] -= original_items["item16"]["population_change"]
    count17["observed_people_change_by_generation"] = {g: 0. for g in GENS}
    count17["coverage_people_change_by_generation"] = {g: original_items["joint"]["coverage_people_change_by_generation"][g]
        - original_items["item16"]["coverage_people_change_by_generation"][g] for g in GENS}
    count17["conditional_on_item16"] = True
    for entry in (count16, count17):
        entry["pricing"] = "oct16 exact signed-driver response replay; item15 observed recalibration transports the additions' capital-use proxy"
        entry["parts_file"] = f"coverage_bound_2026_10_14/derived/line_parts_oct16_{basis}.csv"
    count16["parts_scenario"] = "item16"
    count17["parts_scenario"], count17["subtract_parts_scenario"] = "joint", "item16"
    with (LANE / f"derived/line_parts_oct16_{basis}.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, count_parts[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(count_parts)
    tax_arm = os.environ.get("ITEM19_ARM", "foreign_full_ftc_individual_tangible_normal")
    tax = read(FISCAL / "passthrough_source_tax_r5_2026_10_15/derived/item.json")["arms"][tax_arm]
    counts = read(FISCAL / f"generation_account_2026_09_24/derived/generation_summary_oct15{'_cash' if basis == 'cash' else ''}.json")
    screen = {end: sum(tax["by_end"][end]["by_generation_bn"][g]/counts["conventions"]["a"][g]["population"]
        *scenarios["central"]["implied_net_missing_people"][g] for g in GENS) for end in ENDS}
    fee = read(FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json")["higher_ed"]
    college = read(FISCAL / "spending_keys_r5_2026_10_15/derived/item15.json")
    proxy = {"own_item16_operating_proxy_effect_bn": {end: sum(p["observed_change_bn"] for p in count_parts
        if p["scenario"] == "item16" and p["end"] == end and p["line"].startswith("oct16_college_operating:")) for end in ENDS},
        "whole_union_U_capital_minus_U_cost_bn": (fee["U_capital"]-fee["U"])*college["national_exposure_bn"]*(college["central_response"]-1),
        "interpretation": "full original-union key-offset scale, not an error bound on native calibration; its person allocation is unidentified"}
    return {"ends": scenarios["central"]["ends"], "scenarios": scenarios,
        "implied_net_missing_people": scenarios["central"]["implied_net_missing_people"],
        "adults_by_generation": scenarios["central"]["adults_by_generation"],
        "declared_item12_deltas_bn": declared, "interactions": interactions,
        "item_overrides": {"native_minor_calibration": count16, "coverage_tenure": count17},
        "count_scenarios": changes, "transform_trace": traces, "college_observed_calibration_proxy": proxy,
        "item19_coverage": {"status": "withheld", "reason": "lane has no source-tax price vector for constructed omitted people; existing v8 coverage contains no pass-through tax source to transform",
            "generation_mean_size_screen_bn": screen, "arm": tax_arm,
            "screen_rule": "existing source19 generation tax / complete generation population times missing generation count; diagnostic only, no age/sex/industry identification; not a bound"}}


def main():
    start = time.perf_counter()
    command = ["node", str(FISCAL / "main_case_2026_10_16/coverage_snapshot.cjs")]
    completed = subprocess.run(command, check=False, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(f"[BLOCKED] source item snapshot exited {completed.returncode}: {completed.stderr}")
    snapshot = json.loads(completed.stdout)
    result = {"key": "oct16", "case": "main_case_2026_10_16", "allocation": "personal",
        "specifications": [16, 11], "stub13": snapshot["stub13"],
        "item18_carrier_mode": os.environ.get("ITEM18_CARRIER_MODE", "source_evaluator"),
        "coverage_scope": "item12 before item16/17; add own-price item_overrides once",
        "sets": {basis: calculate(basis, snapshot) for basis in ("set", "cash")},
        "gates": {"principal_kernels_hash_verified": True, "own_price_count_builder_replayed": True},
        "limitations": ["No new behavioral or production solve; observed roster and driver coefficients held.",
            "Item15 observed item16 interaction transports the source additions' capital-use proxy; original-union U-capital offset has no declared person vector.",
            "Item19 omitted-person tax increment withheld; source lane supplies no constructed-person price kernel."]}
    rates, base = load()
    result["national_hispanic_constructions"] = national_constructions(rates, base)
    dependencies = [FISCAL / p for p in (
        "spending_keys_r5_2026_10_15/derived/item13.json", "spending_keys_r5_2026_10_15/derived/item14.json",
        "spending_keys_r5_2026_10_15/derived/item15.json", "consumption_tax_bases_r5_2026_10_15/derived/item.json",
        "passthrough_source_tax_r5_2026_10_15/derived/item.json", "one_rate_2026_10_15/derived/rates.json",
        "spending_keys_r5_2026_10_15/items.cjs", "count_composition_r5_2026_10_15/measure.py",
        "count_composition_r5_2026_10_15/tenure.py", "count_composition_r5_2026_10_15/derived/native_person_factors.parquet",
        "main_case_2026_10_16/coverage_snapshot.cjs", "coverage_bound_2026_10_14/coverage_oct16.py")]
    result["source_sha256"] = {str(p.relative_to(FISCAL)): digest(p) for p in dependencies}
    target = LANE / "derived/coverage_bound_oct16.json"
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    C.require(peak < 2_500_000_000, "oct16 coverage RSS above 2.5GB")
    physical = require_within_budget("oct16 signed person-price replay")
    temporary.replace(target)
    for basis, block in result["sets"].items():
        print(basis, {end: block["ends"][end]["total_bn"] for end in ENDS}, block["interactions"])
    print(f"OCT16 coverage PASS elapsed {time.perf_counter()-start:.3f}s peakRSS {peak/1e6:.1f}MB physical {physical/1e6:.1f}MB")


if __name__ == "__main__":
    main()
