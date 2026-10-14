"""P7 task 4: crash density response on the congestion case's long-run network.

The historical crash_model.py and every original output stay unchanged. This
producer reproduces its full grid, then applies its density elasticities to
residual VMT/lane after the same uniform capacity cuts as the congestion row.
Composition, liability and single-vehicle losses stay fixed. This transfers a
traffic elasticity to road density [ASSUMPTION], not an estimated capacity effect.
"""
from __future__ import annotations

import csv
import ast
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
OUT = HERE / "derived"
GATES = []


def read_json(path):
    return json.loads(path.read_text())


def read_csv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def gate(name, passed, detail=""):
    GATES.append(dict(gate=name, passed=bool(passed), detail=str(detail)))
    if not passed:
        raise SystemExit(f"[BLOCKED] {name}: {detail}; no new outputs written")


def load_crash():
    spec = importlib.util.spec_from_file_location("historical_crash", HERE / "crash_model.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def q_for_count(target, rho):
    """Reproduce arms.py scaled/build_exposure on its archived raw ACS cells.

    Raw group-minute weights are unchanged by a common scale in this ratio.
    Reclassification conserves group + other minutes separately in every area.
    """
    acs = read_json(FISCAL / "congestion_2026_09_23/derived/pums_commute_checks.json")["group_persons_acs"]
    scale = target / acs
    numerator = denominator = error = 0.0
    for row in read_csv(FISCAL / "congestion_2026_09_23/derived/ua_exposure.csv"):
        try:
            g, o = (float(row[k]) for k in ("acs_group_vehicle_minutes", "acs_other_vehicle_minutes"))
        except ValueError:
            continue
        if not math.isfinite(g + o) or g + o <= 0:
            continue
        gs, os = scale * g, o - (scale - 1) * g
        gate(f"nonnegative scaled traffic weights {row['name']}", gs >= 0 and os >= 0)
        error = max(error, abs(gs + os - g - o) / max(g + o, 1))
        phi = rho * gs / (rho * gs + os)
        numerator += g * phi
        denominator += g
    gate("traffic weights conserved per area", error < 1e-12, error)
    return numerator / denominator


def density_parts(crash, parameters, result):
    """Only the x/beta volume terms; excludes the original composition terms."""
    s, q = result["s"], result["q"]
    h = crash.HISP_PED * crash.MEX_OF_HISP
    nm_scale = s * (1 - q) / (1 - s) * (1 - h)
    b_nf, b_f = parameters["beta"]
    return dict(
        mv_nonfatal=result["m_mv_nonfatal"] * s * (1 - q) * crash.BASE["mv_nonfatal"] * parameters["x_nonfatal"],
        mv_fatal=result["m_fatal"] * s * (1 - q) * crash.BASE["mv_fatal"] * parameters["x_fatal"],
        nm_nonfatal=result["m_nm_nonfatal"] * nm_scale * b_nf * crash.BASE["nm_nonfatal"],
        nm_fatal=result["m_fatal"] * nm_scale * b_f * crash.BASE["nm_fatal"],
    )


def residual_share(traffic_share, lane_cut):
    """One minus without/with VMT per lane, holding outsiders' VMT fixed.

    Do not clip negative density relief: a capacity cut larger than the traffic
    removed raises density, and the signed crash response must reflect that.
    """
    return 1 - (1 - traffic_share) / (1 - lane_cut)


def main():
    started = time.perf_counter()
    pins = read_json(HERE / "inputs/pins.json")
    for rel, expected in pins["sha256"].items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        gate(f"pinned dependency {rel}", actual == expected, actual)
    crash = load_crash()
    levels = {**crash.FACTORS, **crash.x_levels_evidence(), "r_nf": crash.ccrs_nonfatal_or()}
    cells = [dict(zip(levels, idx)) for idx in itertools.product(range(3), repeat=len(levels))]
    middle = next(i for i, cell in enumerate(cells) if all(v == 1 for v in cell.values()))

    def evaluate(cell):
        p = {k: levels[k][i] for k, i in cell.items()}
        result = crash.evaluate_split(*[p[k] for k in crash.FACTORS], r_nf=p["r_nf"], composition=True)
        density = density_parts(crash, p, result)
        return p, result, density

    positive = [evaluate(cell)[1] for cell in cells]
    model = read_json(OUT / "model.json")
    original_span = [min(r["total"] for r in positive), positive[middle]["total"], max(r["total"] for r in positive)]
    gate("original full-grid span reproduces model.json", max(abs(a - b) for a, b in zip(original_span, model["spans"]["total"])) < 1e-12, original_span)
    gate("original published values reproduce before changes", [round(v, 2) for v in original_span] == [-57.68, 11.05, 74.34])
    gate("full factorial count", len(cells) == 3 ** 9)
    gate("national crash components close", abs(sum(crash.BASE[k] for k in ("mv_fatal", "mv_nonfatal", "sv", "nm_fatal", "nm_nonfatal")) - crash.BASE["total_kept"]) < 1e-9)

    counts = {r["count"]: r for r in read_csv(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv")}
    n0, n4 = (float(counts["union|all"][k]) for k in ("published", "row4"))
    civ4 = float(counts["cps_all_civilian|all"]["row4"])
    ratios = read_csv(FISCAL / "congestion_2026_09_23/derived/nhts_ratios.csv")
    rho = float(next(r for r in ratios if r["survey"] == "2017" and r["cut"] == "southwest")["rho_all_over_commute_H_vs_N"])
    arms_tree = ast.parse((FISCAL / "congestion_2026_09_23/arms.py").read_text())
    target_nodes = [node.value for node in arms_tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "TARGET" for t in node.targets)]
    gate("one authoritative congestion TARGET declaration", len(target_nodes) == 1)
    congestion_target = ast.literal_eval(target_nodes[0])
    gate("congestion TARGET matches published rounded union", abs(congestion_target - n0) < 0.5)
    gate("original traffic self-share reproduced", abs(q_for_count(congestion_target, rho) - crash.Q_METRO) < 1e-12)
    crash.N_GROUP, crash.N_ALL = n4, civ4
    crash.P_SHARE = n4 / civ4
    crash.Q_METRO = q_for_count(n4, rho)
    crash.MEX_OF_HISP = float(counts["union_hispanic|all"]["row4"]) / float(counts["cps_hispanic_civilian|all"]["row4"])
    reeval = {r["row"]: float(r["row4_bn"]) for r in read_csv(FISCAL / "population_basis_2026_09_29/derived/reeval.csv")}
    gate("row-4 fixed-network central reproduced", abs(evaluate(cells[middle])[1]["total"] - reeval["road_crash_externality"]) < 5e-10)
    ages = [r for r in read_csv(FISCAL / "main_case_decomposition_2026_09_29/derived/age_bins.csv") if r["weights"] == "row4" and r["key"] == "extra|pop"]
    all_g, all_n = (sum(float(r[k]) for r in ages) for k in ("union", "national"))
    u5_g, u5_n = (sum(float(r[k]) for r in ages if int(r["bin"]) < 5) for k in ("union", "national"))
    gate("age weights conserve row-4 populations", abs(all_g - n4) < 1e-3 and abs(all_n - civ4) < 1e-3)
    crash.P_SHARE = (all_g - u5_g) / (all_n - u5_n)
    fixed = [evaluate(cell) for cell in cells]
    gate("live fixed-network 5+ central reproduced", abs(fixed[middle][1]["total"] - reeval["road_crash_externality_5plus"]) < 5e-10)
    printed_spans = [r for r in read_csv(FISCAL / "social_spans_priced_count_2026_09_29/derived/priced_spans.csv") if r["item"] == "road_crash_externality" and r["measure"] == "absolute"]
    fixed_span = [min(r[1]["total"] for r in fixed), fixed[middle][1]["total"], max(r[1]["total"] for r in fixed)]
    gate("live fixed-network full span reproduced", max(abs(v - float(next(r for r in printed_spans if r["statistic"] == stat)["priced"])) for stat, v in zip(("low", "central", "high"), fixed_span)) < 5e-10)

    long_run = FISCAL / "service_response_long_run_2026_09_27/derived"
    net = read_json(long_run / "net_change.json")
    ea = read_json(long_run / "responses.json")["lines"]["economic_affairs_services"]
    candidate = read_json(long_run / "candidate_band.json")
    highways = [r for r in ea["subfunctions"] if r["subfunction"] == "Highways"]
    band = read_json(FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.json")
    lineage = band["lineage"]["counts"]
    gate("lineage count closes", abs(lineage["account_union"] - n4) < 1e-3 and abs(lineage["lineage_population"] - n4 - lineage["added"]) < 1e-6)
    recipient_share = lineage["added"] / (civ4 - n4)
    rows, components, extrema, ends = [], [], [], {}
    overlap = ["mortality", "road_congestion"]
    for end in ("low", "high"):
        response = sum(r["national_bn"] * r["response"][end] for r in highways) / sum(r["national_bn"] for r in highways)
        key = candidate["group_amounts_at_end_specifications_bn"][end]["economic_affairs_services"] / ea["national_bn"]
        cut = response * key
        gate(f"{end}: same capacity cut as congestion case", abs(cut - net["by_band_end"][end]["lane_cut"]) < 1e-12)
        gate(f"{end}: valid capacity fraction", 0 <= cut < 1)
        road_key = band["lineage_social_keys"][f"{end}_end"]["road"]
        gate(f"{end}: personal end specification", band["lineage_social_keys"][f"{end}_end"]["allocation"] == "personal" and band["lineage_social_keys"][f"{end}_end"]["specification"] == {"low": 16, "high": 11}[end])
        ends[end] = dict(lane_cut=cut, highway_response=response, key=key, added_road_share=road_key)
        for arm in ("all_density", "multivehicle_only"):
            adjusted = []
            grid = []
            max_close = max_comp = max_zero = 0.0
            for index, (p, result, density) in enumerate(fixed):
                s = result["s"]
                residual = residual_share(s, cut)
                multiplier = residual / s
                selected = sum(v for k, v in density.items() if arm == "all_density" or k.startswith("mv_"))
                total = result["total"] + (multiplier - 1) * selected
                new_components = {k: result[k] for k in ("mv_nonfatal", "mv_fatal", "nonmotorist", "single_vehicle")}
                for k in ("mv_nonfatal", "mv_fatal"):
                    new_components[k] += (multiplier - 1) * density[k]
                if arm == "all_density":
                    new_components["nonmotorist"] += (multiplier - 1) * (density["nm_nonfatal"] + density["nm_fatal"])
                max_close = max(max_close, abs(sum(new_components.values()) - total))
                max_comp = max(max_comp, abs((total - selected * multiplier) - (result["total"] - selected)))
                max_zero = max(max_zero, abs(residual_share(s, 0) / s - 1))
                adjusted.append(total)
                grid.append(dict(end=end, arm=arm, cell=index, **cells[index], traffic_share=s, lane_cut=cut, residual_density_share=residual, density_multiplier=multiplier, fixed_total_bn=result["total"], density_fixed_bn=selected, total_bn=total))
                if index == middle:
                    components.append(dict(end=end, arm=arm, **new_components, composition_bn=result["composition"], density_fixed_bn=selected, density_after_bn=selected * multiplier, other_held_bn=result["total"] - selected, residual_density_share=residual, multiplier=multiplier))
            gate(f"{end} {arm}: component closure", max_close < 1e-9, max_close)
            gate(f"{end} {arm}: all nondensity terms conserved", max_comp < 1e-9, max_comp)
            gate(f"{end} {arm}: zero capacity cut reproduces fixed network", max_zero < 1e-12, max_zero)
            gate(f"{end} {arm}: capacity matching traffic removes density term", abs(residual_share(fixed[middle][1]["s"], fixed[middle][1]["s"])) < 1e-12)
            span = [min(adjusted), adjusted[middle], max(adjusted)]
            for statistic, index in (("low", adjusted.index(span[0])), ("central", middle), ("high", adjusted.index(span[2]))):
                extrema.append(dict(statistic=statistic, **grid[index]))
            for population, factor, n in (("union", 1.0, n4), ("lineage_gross", 1 + road_key, lineage["lineage_population"]), ("lineage", (1 + road_key) * (1 - recipient_share), lineage["lineage_population"])):
                declaration = dict(comparator="with_without", beneficiary_population="residents_outside_union" if population == "union" else "residents_outside_lineage" if population == "lineage" else "residents_outside_union_including_added_descendants", valuation_basis="crash_resource_and_harm", overlap_set=json.dumps(overlap))
                rows.append(dict(item="road_crash_externality_capacity_response", group="mexican_origin" if population == "union" else "mexican_immigrant_lineage", measure="absolute", low_bn=span[0] * factor, central_bn=span[1] * factor, high_bn=span[2] * factor, per_member_usd=span[1] * factor * 1e9 / n, evidence_level="existing crash grid plus assumed density-capacity transfer", double_count_with="replace road_crash_externality; congestion and EMS excluded; fault-based row alternative", method_note="composition/liability/single vehicle held; no VMT fill-in; " + ("x and beta on density" if arm == "all_density" else "x on density; beta stays on traffic volume") + "; lineage road-key scaling assumed", end=end, arm=arm, population=population, baseline_central_bn=fixed_span[1] * factor, change_bn=(span[1] - fixed_span[1]) * factor, change_from_gross_live_bn=span[1] * factor - fixed_span[1] * (1 if population == "union" else 1 + road_key), scale_from_union=factor, population_n=n, **declaration))
    gate("no duplicate row keys", len({(r["end"], r["arm"], r["population"]) for r in rows}) == len(rows))
    for name, records in (("capacity_items.csv", rows), ("capacity_components.csv", components), ("capacity_extrema.csv", extrema)):
        with (OUT / name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(records)
    document = dict(case="oct14", original_positive_control=original_span, fixed_network_priced_span=fixed_span, ends=ends, recipient_share=recipient_share, lineage_rule="existing v7 added-people road-key extrapolation; lineage removes exchangeable added recipients; lineage_gross retains them for boundary-independent comparison [ASSUMPTION]", capacity_rule="remaining VMT/lane = (1-s)/(1-cut); ratio of finite density reduction to original s multiplies density terms only [ASSUMPTION]", replicate_se="not available: full factorial sensitivity span, no joint replicate inputs for crash/capacity parameters", all_passed=True, gates=GATES, input_pins=pins)
    (OUT / "capacity_model.json").write_text(json.dumps(document, indent=2) + "\n")
    for row in rows:
        if row["arm"] == "all_density":
            print(f"{row['end']} {row['population']}: {row['central_bn']:.6f} ({row['low_bn']:.6f}, {row['high_bn']:.6f}); change {row['change_bn']:+.6f}")
    print(f"PASS {len(GATES)} gates; elapsed_s={time.perf_counter()-started:.3f}; maxrss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
