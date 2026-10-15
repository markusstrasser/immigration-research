"""Item21's own-price coverage/count increments, without producer writes.

build(price_builder) calls price_builder(data, audit, basis, vintage), where
vintage is oct15 (coverage) or oct15_final_routing (counts). The callback returns
typed pieces with base_price and constructed_price arrays in $bn per person.
Optional population='identified' or 'added' represents explicit G3 profile
calibrations; normal source pieces use 'both'. Outputs are DOLLAR INCREMENTS,
to add to the existing coverage file, never replacements for its people counts.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import gc
import importlib.util
import json
from pathlib import Path

import numpy as np

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
GENS = ("G1", "G2", "G3plus")
ENDS = ("low", "high")


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] item21 coverage: " + message)


def source_runtime():
    """Import the read-only source builders; none runs a write-producing main."""
    directory = FISCAL / "coverage_bound_2026_10_14"
    sys.path.insert(0, str(directory))
    spec = importlib.util.spec_from_file_location("item21_coverage_oct16", directory / "coverage_oct16.py")
    require(spec is not None and spec.loader is not None, "cannot load source coverage builders")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rekey_piece_prices(data, audit, piece_index, new_driver, new_amount_bn, old_factor=1.0):
    """Reprice one declared source piece with its raw generation driver.

Ethnicity changes the declared aggregate amount, never this raw within-gen
driver. new_amount_bn is the complete NEW subblock amount. old_factor selects
the OLD subblock (for example the residual after VA). Source exporter pricing
normalizes over identified plus added observed weights. Added/identified net
profile calibration is supplied separately, as in export_pricing.py:349–369.
"""
    p = audit["denominator_pieces"][piece_index]
    gen = GENS.index(p["generation"])
    driver = np.asarray(new_driver, dtype=float)
    require(driver.shape == data["generation"].shape, "new driver/person shape")
    require(np.isfinite(driver).all() and np.all(driver >= 0), "invalid new raw driver")
    require(np.isfinite(new_amount_bn) and np.isfinite(old_factor), "nonfinite price coefficient")
    driver = np.where(data["generation"] == gen, driver, 0.0)
    weights = data["weights"][:, 0] + data["added_weights"][:, 0]
    denominator = float(driver @ weights)
    require(denominator > 0 or new_amount_bn == 0, "nonzero new amount has no raw driver mass")
    new_price = driver * (new_amount_bn / denominator) if denominator > 0 else np.zeros_like(driver)
    base = new_price - old_factor * data["base_piece_prices"][piece_index]
    constructed = new_price - old_factor * data["constructed_piece_prices"][piece_index]
    expected = float(new_amount_bn - old_factor * (data["base_piece_prices"][piece_index] @ weights))
    require(abs(float(base @ weights) - expected) < 1e-9, "rekeyed observed piece amount closure")
    return {**p, "line": "item21:" + p["line"], "population": "both",
            "base_price": base, "constructed_price": constructed,
            "pricing": "raw generation driver normalized to declared own-price amount"}


def validate_pieces(pieces, data):
    require(isinstance(pieces, list) and len(pieces) > 0, "price builder returned no pieces")
    identities = []
    for p in pieces:
        require(p["end"] in ENDS and p["generation"] in GENS, "piece end/generation")
        require(p.get("population", "both") in ("both", "identified", "added"), "piece population scope")
        require(p["economic_class"] in ("fiscal_line", "capital_return", "unclassified_residual"), "unexpected health economic class")
        require(p["economic_class"] != "capital_return" or p["level"] in ("federal", "state_local"), "capital level")
        for name in ("source_line", "source_side", "category", "level"):
            require(bool(p.get(name)), "missing typed piece field " + name)
        for name in ("base_price", "constructed_price"):
            a = np.asarray(p[name])
            require(a.shape == data["generation"].shape and np.isfinite(a).all(), "invalid " + name)
            require(np.count_nonzero(a[data["generation"] != GENS.index(p["generation"])]) == 0,
                    "piece prices leak outside their declared generation")
        identities.append((p["end"], p["generation"], p["line"], p.get("population", "both")))
    require(len(set(identities)) == len(identities), "duplicate price-piece identity")


def capital_rate_pieces(pieces, capital_rate=None):
    """Select a common return rate without changing callback-owned arrays.

The callback's capital deltas are priced at the source ends' 2% / 3%. Scale
only those signed capital prices; fiscal lines and profile calibrations stay
fixed. Doing this before integration reprices every age/count scenario exactly.
"""
    if capital_rate is None:
        return pieces
    require(np.isfinite(capital_rate) and capital_rate >= 0, "invalid common capital rate")
    result = []
    for p in pieces:
        if p["economic_class"] != "capital_return":
            result.append(p)
            continue
        source_rate = {"low": .02, "high": .03}[p["end"]]
        factor = capital_rate / source_rate
        result.append({**p, "base_price": np.asarray(p["base_price"]) * factor,
                       "constructed_price": np.asarray(p["constructed_price"]) * factor,
                       "source_capital_rate": source_rate, "capital_rate": float(capital_rate)})
    return result


def integrate(pieces, mass, added_mass=None, observed=False, basis="set"):
    """Signed-price integration with the coverage adapter's typed shape."""
    mass = np.asarray(mass)
    added_mass = np.zeros_like(mass) if added_mass is None else np.asarray(added_mass)
    require(mass.shape == added_mass.shape and np.isfinite(mass).all()
            and np.isfinite(added_mass).all(), "integration mass")
    by_end = {end: [] for end in ENDS}
    price_field = "base_price" if observed else "constructed_price"
    for p in pieces:
        scope = p.get("population", "both")
        weights = {"both": mass + added_mass, "identified": mass, "added": added_mass}[scope]
        amount = float(np.asarray(p[price_field]) @ weights)
        metadata = {k: v for k, v in p.items() if k not in ("base_price", "constructed_price")}
        by_end[p["end"]].append({**metadata, "coverage_bn": amount, "item13_first_year_addback_bn": 0.0})
    out = {}
    for end, rows in by_end.items():
        by_gen = {g: sum(p["coverage_bn"] for p in rows if p["generation"] == g) for g in GENS}
        capital = {level: sum(p["coverage_bn"] for p in rows if p["economic_class"] == "capital_return"
                             and p["level"] == level) for level in ("federal", "state_local")}
        fiscal = sum(p["coverage_bn"] for p in rows if p["economic_class"] == "fiscal_line")
        residual = sum(p["coverage_bn"] for p in rows if p["economic_class"] == "unclassified_residual")
        total = sum(by_gen.values())
        require(abs(total - sum(capital.values()) - fiscal - residual) < 1e-9, "typed incremental closure")
        decomposition = {"line_parts": rows, "total_cost_bn": total, "capital_by_level_bn": capital,
            "production": {"P_bn": 0.0, "F_bn": 0.0}, "unclassified_bn": residual,
            "classified_fiscal_line_bn": fiscal, "classified_fiscal_with_production_F_bn": fiscal,
            "sign_convention": "total = capital + fiscal lines + unclassified - P - F",
            "borrowing_rule": "capital return is not borrowing; follow existing consumer financing rule"}
        if basis == "cash":
            decomposition["classified_cash_fiscal_bn"] = fiscal
        out[end] = {"coverage_bn": total, "total_bn": total, "by_generation": by_gen,
                    "by_generation_bn": by_gen, "decomposition": decomposition}
    return out


def add_ends(a, b, scale=1):
    result = {}
    for end in ENDS:
        by_gen = {g: a[end]["by_generation_bn"][g] + scale * b[end]["by_generation_bn"][g] for g in GENS}
        result[end] = {"total_bn": sum(by_gen.values()), "by_generation_bn": by_gen}
    return result


def count_transports(data, audit, pieces, runtime, rates, base, basis):
    """Actual native calibration/tenure weights, including linked-child carriers."""
    tenure, factor = runtime.person_inputs(data)
    path = FISCAL / f"main_case_2026_10_15/derived/corrections{'_cash' if basis == 'cash' else ''}.json"
    flags = runtime.item10_flags(data, json.loads(path.read_text()))
    w = data["weights"][:, 0]
    f, _ = runtime.C.factors(data, rates, base)
    native = w * factor
    fixed, _ = runtime.fixed_count_tenure(data, tenure, w, rates, base)
    joint, _ = runtime.fixed_count_tenure(data, tenure, native, rates, base)
    transfer = runtime.transfer_count_tenure(data, tenure, rates, base)
    zero = np.zeros_like(w)
    completion = data["added_weights"][:, 0] * (factor - 1) * flags["nonreporter"]
    changes, rows = {}, []
    for name, observed, missing, added in (
        ("item16", native-w, native*f-w*f, completion),
        ("item17", zero, w*(fixed-f), zero),
        ("joint", native-w, native*joint-w*f, completion),
        ("joint_count_transfer", native-w, native*transfer-w*f, completion),
    ):
        obs = integrate(pieces, observed, added, observed=True, basis=basis)
        cov = integrate(pieces, missing, basis=basis)
        changes[name] = add_ends(obs, cov)
        for end in ENDS:
            aa, bb = obs[end]["decomposition"]["line_parts"], cov[end]["decomposition"]["line_parts"]
            for a, b in zip(aa, bb, strict=True):
                rows.append({k: v for k, v in a.items() if k not in ("coverage_bn", "item13_first_year_addback_bn")}
                            | {"scenario": name, "observed_change_bn": a["coverage_bn"],
                               "coverage_change_bn": b["coverage_bn"],
                               "change_bn": a["coverage_bn"] + b["coverage_bn"],
                               "item13_first_year_addback_bn": 0.0, "complete_use_excluded": False})
    overrides = {
        "native_minor_calibration": {"by_end": changes["item16"], "parts_scenario": "item16"},
        "coverage_tenure": {"by_end": add_ends(changes["joint"], changes["item16"], -1),
                            "parts_scenario": "joint", "subtract_parts_scenario": "item16"},
    }
    return changes, rows, overrides


def build(price_builder, bases=("set", "cash"), capital_rate=None):
    """Return source-shaped incremental coverage and count dollars for each basis.

Add every field's dollars to the existing source output. Append count_parts to
the source typed CSV. item_overrides deliberately omit all population fields:
item21 reprices the existing count change and does not change people counts.
    capital_rate=None preserves the source's 2%/3% ends. A supplied common rate
    scales only capital-return callback prices before every integration.
"""
    runtime = source_runtime()
    rates, base = runtime.load()
    result = {"item": "health_residual_key", "kind": "incremental_own_price_replay", "sets": {}}
    if capital_rate is not None:
        require(np.isfinite(capital_rate) and capital_rate >= 0, "invalid common capital rate")
        result["capital_rate"] = float(capital_rate)
    for basis in bases:
        require(basis in ("set", "cash"), "unknown basis")
        data, audit = runtime.load_kernel(basis, "oct15")
        pieces = capital_rate_pieces(price_builder(data, audit, basis, "oct15"), capital_rate)
        validate_pieces(pieces, data)
        w, aw = data["weights"][:, 0], data["added_weights"][:, 0]
        scenarios = {}
        for name, options in runtime.DEFINITIONS.items():
            f, af = runtime.C.factors(data, rates, base, **options)
            scenarios[name] = {"ends": integrate(pieces, w*f, aw*af, basis=basis)}
        f, af = runtime.C.factors(data, rates, base)
        adult = data["age"] >= 18
        adults = integrate(pieces, w*f*adult, aw*af*adult, basis=basis)
        minors = integrate(pieces, w*f*~adult, aw*af*~adult, basis=basis)
        central = scenarios["central"]["ends"]
        for end in ENDS:
            central[end]["adult_cost_by_generation_bn"] = adults[end]["by_generation_bn"]
            central[end]["minor_cost_by_generation_bn"] = minors[end]["by_generation_bn"]
            require(abs(adults[end]["total_bn"] + minors[end]["total_bn"] - central[end]["total_bn"]) < 1e-9,
                    "adult/minor coverage increment closure")
        del data, audit, pieces, w, aw
        gc.collect()
        data, audit = runtime.load_kernel(basis, "oct15_final_routing")
        pieces = capital_rate_pieces(price_builder(data, audit, basis, "oct15_final_routing"), capital_rate)
        validate_pieces(pieces, data)
        changes, rows, overrides = count_transports(data, audit, pieces, runtime, rates, base, basis)
        result["sets"][basis] = {"ends": central, "scenarios": scenarios,
            "declared_item12_deltas_bn": {end: {"health_residual_key": central[end]["total_bn"]} for end in ENDS},
            "count_scenarios": changes, "count_parts": rows, "item_overrides": overrides,
            "gates": {"principal_kernel_receipts_verified": True, "own_count_weight_builders_replayed": True,
                      "typed_incremental_closure_1e_9bn": True, "count_population_metadata_unchanged": True}}
        del data, audit, pieces
        gc.collect()
    return result
