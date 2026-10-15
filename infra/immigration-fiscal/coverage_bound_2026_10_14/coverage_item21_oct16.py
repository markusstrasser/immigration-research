"""Add source-owned item21 dollar increments; preserve every people field.

The producer supplies separate signed-weight integrations for every health arm
at the common v9 rate. Never scale these exports a second time.
"""
import copy
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "spending_keys_r5_2026_10_15/derived"
GENS = ("G1", "G2", "G3plus")


def add_end(base, delta):
    out = dict(base)
    for key in ("coverage_bn", "total_bn"):
        if key in out:
            out[key] += delta.get(key, delta["total_bn"])
    for key in ("by_generation", "by_generation_bn", "adult_cost_by_generation_bn", "minor_cost_by_generation_bn"):
        if key in out and key in delta:
            # The existing integrator aliases its two generation views. Replace
            # each view rather than incrementing the same dictionary twice.
            out[key] = {g: base[key][g]+delta[key][g] for g in GENS}
    if "decomposition" in out:
        d, inc = dict(base["decomposition"]), delta["decomposition"]
        out["decomposition"] = d
        d["line_parts"] = base["decomposition"]["line_parts"] + inc["line_parts"]
        for key in ("total_cost_bn", "unclassified_bn", "classified_fiscal_line_bn",
                    "classified_fiscal_with_production_F_bn", "classified_cash_fiscal_bn"):
            if key in d:
                d[key] += inc.get(key, 0.)
        d["capital_by_level_bn"] = {level: base["decomposition"]["capital_by_level_bn"][level]
            + inc["capital_by_level_bn"][level] for level in ("federal", "state_local")}
        if abs(sum(p["coverage_bn"] for p in d["line_parts"])-out["total_bn"]) > 1e-9:
            raise ValueError("[BLOCKED] item21 appended coverage line closure")
    if abs(sum(out["by_generation_bn"].values())-out["total_bn"]) > 1e-9:
        raise ValueError("[BLOCKED] item21 appended generation closure")
    return out


def attach(base, basis, rate):
    source = json.loads((SOURCE / "item21_v9_coverage.json").read_text())
    old_prices = json.loads((SOURCE / "item21_coverage.json").read_text())
    if abs(source["capital_rate"]-rate) > 1e-15:
        raise ValueError("[BLOCKED] item21 common-rate source mismatch")
    base_file = HERE / f"derived/line_parts_oct16_{basis}.csv"
    with base_file.open(newline="") as stream:
        base_rows = list(csv.DictReader(stream))
    variants = {}
    for arm, block in source["arms"].items():
        inc = block["sets"][basis]
        # Typed source rows are immutable. Copy only the small edited containers;
        # duplicating all five complete kernels exceeds the physical budget.
        out = {**base, "scenarios": {name: {**q, "ends": dict(q["ends"])} for name, q in base["scenarios"].items()},
               "count_scenarios": {name: dict(q) for name, q in base["count_scenarios"].items()},
               "item_overrides": copy.deepcopy(base["item_overrides"]),
               "declared_item12_deltas_bn": copy.deepcopy(base["declared_item12_deltas_bn"]),
               "interactions": copy.deepcopy(base["interactions"])}
        for name, scenario in out["scenarios"].items():
            for end in ("low", "high"):
                scenario["ends"][end] = add_end(scenario["ends"][end], inc["scenarios"][name]["ends"][end])
        out["ends"] = out["scenarios"]["central"]["ends"]
        for name, scenario in out["count_scenarios"].items():
            for end in ("low", "high"):
                scenario[end] = add_end(scenario[end], inc["count_scenarios"][name][end])
        for end in ("low", "high"):
            # Record the standalone source-rate increment and its exact20x21 cross.
            declared = old_prices["arms"][arm]["sets"][basis]["ends"][end]["total_bn"]
            cross = inc["ends"][end]["total_bn"]-declared
            out["declared_item12_deltas_bn"][end]["health_residual_key"] = declared
            z = out["interactions"][end]
            z["coverage_change_bn"] += inc["ends"][end]["total_bn"]
            z["declared_sum_bn"] += declared
            z["interaction_bn"] += cross
            z["item21_x_item20_bn"] = cross
            z["unexplained_gap_bn"] = z["coverage_change_bn"]-z["declared_sum_bn"]-z["item15_x_item20_bn"]-cross
            if abs(z["unexplained_gap_bn"]) > 1e-9:
                raise ValueError("[BLOCKED] item21 coverage interaction closure")
        file = base_file if arm == "central" else HERE / f"derived/line_parts_oct16_{basis}_health_{arm}.csv"
        for item in ("native_minor_calibration", "coverage_tenure"):
            entry = out["item_overrides"][item]
            for end in ("low", "high"):
                entry["by_end"][end] = add_end(entry["by_end"][end], inc["item_overrides"][item]["by_end"][end])
            entry["parts_file"] = str(file.relative_to(HERE.parent))
            entry["pricing"] += f"; additive own item21 {arm} source dollars at the common rate"
        rows = base_rows + inc["count_parts"]
        columns = list(dict.fromkeys(k for row in rows for k in row))
        with file.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        out["item21_arm"] = arm
        variants[arm] = out
    off = {**base, "item_overrides": copy.deepcopy(base["item_overrides"])}
    off_file = HERE / f"derived/line_parts_oct16_{basis}_health_off.csv"
    with off_file.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, base_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(base_rows)
    for entry in off["item_overrides"].values():
        entry["parts_file"] = str(off_file.relative_to(HERE.parent))
    central = variants.pop("central")
    def export(name, block):
        target = HERE / f"derived/coverage_bound_oct16_{basis}_health_{name}.json"
        target.write_text(json.dumps(block, indent=2, allow_nan=False)+"\n")
        return {"file": str(target.relative_to(HERE.parent)),
                "sha256": hashlib.file_digest(target.open("rb"), "sha256").hexdigest()}
    central["without_item21"] = export("off", off)
    central["item21_arm_overrides"] = {name: export(name, block) for name, block in variants.items()}
    return central
