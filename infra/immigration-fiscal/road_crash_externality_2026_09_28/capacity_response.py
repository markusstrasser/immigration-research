"""P7 task 4: crash density response on the congestion case's long-run network.

The historical crash_model.py and every original output stay unchanged. This
producer reproduces its full grid, then applies its density elasticities to
residual VMT/lane after the same uniform capacity cuts as the congestion row.
Composition and liability are held during the capacity change. The separate
life-year arms change only gross mortality, including passenger losses in the
single-vehicle term. Density response transfers a traffic elasticity to road
density [ASSUMPTION], not an estimated capacity effect.
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
import sys
import time
import argparse
import os
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
OUT = HERE / "derived"
GATES = []
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget


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


def mortality_base(crash, dot_vsl):
    """Gross mortality, separate from NHTSA's net QoL/productivity accounting."""
    k = "Fatal"
    nm_fraction = (crash.PED[k] + crash.BIKE[k]) / (crash.ECON[k] + crash.QALY[k])
    killed = crash.KILLED[2023]
    deaths = {"mv_fatal": killed * (1 - nm_fraction) * crash.MV_SHARE_FATAL,
              "nm_fatal": killed * nm_fraction,
              "sv_fatal": killed * (1 - nm_fraction) * (1 - crash.MV_SHARE_FATAL)}
    gate("modeled fatal physical allocation closes", abs(sum(deaths.values()) - killed) < 1e-9)
    return {k: n * dot_vsl / 1e9 for k, n in deaths.items()}, deaths


def reprice_mortality(crash, p, result, density, gross, ratios):
    """Change gross mortality only; liability and net nonmortality stay fixed."""
    r = dict(result)
    d = dict(density)
    s, q = result["s"], result["q"]
    nm_scale = s * (1 - q) / (1 - s) * (1 - crash.HISP_PED * crash.MEX_OF_HISP)
    rc, xf = p["r_c"], p["x_fatal"]
    bf = p["beta"][1]
    comp_mv = s * (1 - q) * gross["mv_fatal"] * (rc - 1) * (1 - xf) / 2
    comp_nm = nm_scale * gross["nm_fatal"] * crash.F_DRIVER_PED * (rc - 1) * (1 - bf)
    mv = result["m_fatal"] * s * (1 - q) * gross["mv_fatal"] * xf + comp_mv
    nm = result["m_fatal"] * nm_scale * bf * gross["nm_fatal"] + comp_nm
    sv = result["m_fatal"] * s * gross["sv_fatal"] * p["e_sv"]
    deltas = {"mv_fatal": mv * (ratios["mv_fatal"] - 1),
              "nm_fatal": nm * (ratios["nm_fatal"] - 1),
              "sv_fatal": sv * (ratios["sv_fatal"] - 1)}
    r["mv_fatal"] += deltas["mv_fatal"]
    r["nonmotorist"] += deltas["nm_fatal"]
    r["single_vehicle"] += deltas["sv_fatal"]
    r["total"] += sum(deltas.values())
    r["composition"] += comp_mv * (ratios["mv_fatal"] - 1) + comp_nm * (ratios["nm_fatal"] - 1)
    d["mv_fatal"] += result["m_fatal"] * s * (1 - q) * gross["mv_fatal"] * xf * (ratios["mv_fatal"] - 1)
    d["nm_fatal"] += result["m_fatal"] * nm_scale * bf * gross["nm_fatal"] * (ratios["nm_fatal"] - 1)
    return r, d


def csv_text(records):
    import io
    handle = io.StringIO()
    writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return handle.getvalue()


def main():
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--pin-new-inputs", action="store_true", help="explicitly admit the verified oct15 road/age inputs")
    args = parser.parse_args()
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
    old_net = read_json(long_run / "net_change.json")
    net_path = long_run / "net_change_oct15.json"
    net = read_json(net_path)
    gate("live congestion source is oct15", net["case"] == "oct15")
    for rel, expected in net["source_hashes"].items():
        gate(f"live congestion source current {rel}", hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected)
    ages_path = OUT / "fars_mortality_2023.json"
    mortality = read_json(ages_path)
    for rel, expected in mortality["source_hashes"].items():
        gate(f"FARS mortality source current {rel}", hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == expected)
    gate("FARS mortality standard matches DOT-linked crash base", abs(mortality["dot_vsl_2024usd"] - crash.VSL_2024 * 1e6) < 1e-9)
    new_source_paths = [net_path, ages_path, FISCAL / "service_response_long_run_2026_09_27/congestion.py",
                        HERE / "fars_group.py", Path(__file__), FISCAL / "main_case_2026_10_15/derived/corrections.json",
                        FISCAL / "main_case_2026_10_15/derived/summary.json"]
    new_pins = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in new_source_paths}
    pin_path = HERE / "inputs/pins_oct15.json"
    gate("oct15 source pins explicitly admitted", args.pin_new_inputs or pin_path.exists())
    gate("oct15 source pins current", args.pin_new_inputs or read_json(pin_path)["sha256"] == new_pins)
    band = read_json(FISCAL / "sept24_propagation_2026_09_24/derived/oct14/band_variants.json")
    lineage = band["lineage"]["counts"]
    gate("lineage count closes", abs(lineage["account_union"] - n4) < 1e-3 and abs(lineage["lineage_population"] - n4 - lineage["added"]) < 1e-6)
    recipient_share = lineage["added"] / (civ4 - n4)
    rows, components, extrema, ends = [], [], [], {}
    gross, modeled_deaths = mortality_base(crash, mortality["dot_vsl_2024usd"])
    uniform = {}
    valuation_spans = {}
    overlap = ["mortality", "road_congestion"]
    for end in ("low", "high"):
        source = net["by_band_end"][end]
        response, key, cut = source["highway_response"], source["key_share"], source["lane_cut"]
        gate(f"{end}: same live capacity cut as congestion case", abs(cut - response * key) < 1e-12)
        gate(f"{end}: valid capacity fraction", 0 <= cut < 1)
        road_key = band["lineage_social_keys"][f"{end}_end"]["road"]
        gate(f"{end}: personal end specification", band["lineage_social_keys"][f"{end}_end"]["allocation"] == "personal" and band["lineage_social_keys"][f"{end}_end"]["specification"] == {"low": 16, "high": 11}[end])
        gate(f"{end}: actual oct15 personal specification", net["live_roads"]["ends"][end]["specification"] == {"low": 16, "high": 11}[end] and net["live_roads"]["ends"][end]["allocation"] == "personal")
        ends[end] = dict(lane_cut=cut, before_lane_cut=old_net["by_band_end"][end]["lane_cut"], highway_response=response, key=key, added_road_share=road_key)
    valuations = [("dot_uniform", "0"), ("dot_life_years", "0"), ("dot_life_years", "0.03")]
    for valuation, rate in valuations:
      ratios = {k: 1.0 if valuation == "dot_uniform" else mortality["profiles"][k]["rates"][rate]["mortality_ratio"] for k in gross}
      active = []
      max_nonfatal = max_identity = 0.0
      for p, result, density in fixed:
          r, d = reprice_mortality(crash, p, result, density, gross, ratios)
          max_nonfatal = max(max_nonfatal, abs(r["mv_nonfatal"] - result["mv_nonfatal"]), abs(d["nm_nonfatal"] - density["nm_nonfatal"]))
          identity, _ = reprice_mortality(crash, p, result, density, gross, {k: 1.0 for k in gross})
          max_identity = max(max_identity, abs(identity["total"] - result["total"]))
          active.append((p, r, d))
      gate(f"{valuation}/{rate}: nonfatal dollars held and reference-age identity", max_nonfatal < 1e-9 and max_identity < 1e-9)
      active_span = [min(r[1]["total"] for r in active), active[middle][1]["total"], max(r[1]["total"] for r in active)]
      valuation_spans[f"{valuation}|{rate}"] = active_span
      for end in ("low", "high"):
        cut = ends[end]["lane_cut"]
        road_key = ends[end]["added_road_share"]
        for arm in ("multivehicle_only", "all_density"):
            adjusted = []
            before = []
            grid = []
            max_close = max_comp = max_zero = 0.0
            for index, (p, result, density) in enumerate(active):
                s = result["s"]
                residual = residual_share(s, cut)
                multiplier = residual / s
                selected = sum(v for k, v in density.items() if arm == "all_density" or k.startswith("mv_"))
                total = result["total"] + (multiplier - 1) * selected
                before.append(result["total"] + (residual_share(s, ends[end]["before_lane_cut"]) / s - 1) * selected)
                new_components = {k: result[k] for k in ("mv_nonfatal", "mv_fatal", "nonmotorist", "single_vehicle")}
                for k in ("mv_nonfatal", "mv_fatal"):
                    new_components[k] += (multiplier - 1) * density[k]
                if arm == "all_density":
                    new_components["nonmotorist"] += (multiplier - 1) * (density["nm_nonfatal"] + density["nm_fatal"])
                max_close = max(max_close, abs(sum(new_components.values()) - total))
                max_comp = max(max_comp, abs((total - selected * multiplier) - (result["total"] - selected)))
                max_zero = max(max_zero, abs(residual_share(s, 0) / s - 1))
                adjusted.append(total)
                grid.append(dict(valuation=valuation, real_discount_rate=rate, end=end, arm=arm, cell=index, **cells[index], traffic_share=s, lane_cut=cut, residual_density_share=residual, density_multiplier=multiplier, fixed_total_bn=result["total"], density_fixed_bn=selected, total_bn=total))
                if index == middle:
                    components.append(dict(valuation=valuation, real_discount_rate=rate, end=end, arm=arm, **new_components, composition_bn=result["composition"], density_fixed_bn=selected, density_after_bn=selected * multiplier, other_held_bn=result["total"] - selected, residual_density_share=residual, multiplier=multiplier))
            gate(f"{end} {arm}: component closure", max_close < 1e-9, max_close)
            gate(f"{end} {arm}: all nondensity terms conserved", max_comp < 1e-9, max_comp)
            gate(f"{end} {arm}: zero capacity cut reproduces fixed network", max_zero < 1e-12, max_zero)
            gate(f"{end} {arm}: capacity matching traffic removes density term", abs(residual_share(active[middle][1]["s"], active[middle][1]["s"])) < 1e-12)
            span = [min(adjusted), adjusted[middle], max(adjusted)]
            for statistic, index in (("low", adjusted.index(span[0])), ("central", middle), ("high", adjusted.index(span[2]))):
                extrema.append(dict(statistic=statistic, **grid[index]))
            complete = net["live_roads"]["population"]["with_coverage"]
            for population, factor, n in (("union", 1.0, n4), ("lineage_gross", 1 + road_key, complete), ("lineage", (1 + road_key) * (1 - recipient_share), complete)):
                declaration = dict(comparator="with_without", beneficiary_population="residents_outside_union" if population == "union" else "residents_outside_lineage" if population == "lineage" else "residents_outside_union_including_added_descendants", valuation_basis="crash_resource_and_harm", overlap_set=json.dumps(overlap))
                row_key = (end, arm, population)
                if valuation == "dot_uniform":
                    uniform[row_key] = span[1] * factor
                rows.append(dict(item="road_crash_externality_capacity_response", group="mexican_origin" if population == "union" else "mexican_immigrant_lineage", measure="absolute", valuation=valuation, real_discount_rate=rate, case="oct15", source_quantity_case="oct14", low_bn=span[0] * factor, central_bn=span[1] * factor, high_bn=span[2] * factor, per_member_usd=span[1] * factor * 1e9 / n, evidence_level="transported v7 crash quantities plus assumed native oct15 density-capacity response", double_count_with="replace road_crash_externality; congestion and EMS excluded; fault-based row alternative", method_note="physical mixing/culpability held; liability and net nonmortality dollars held across valuation; no VMT fill-in; " + ("x and beta on density" if arm == "all_density" else "x on density; beta stays on traffic volume") + "; v7 lineage road-key/recipient boundary transported; FARS victim-class ages, modeled fatal allocation held", end=end, arm=arm, population=population, baseline_central_bn=active_span[1] * factor, change_bn=(span[1] - active_span[1]) * factor, before_live_key_central_bn=before[middle] * factor, live_key_delta_bn=(span[1] - before[middle]) * factor, mortality_only_delta_bn=span[1] * factor - uniform[row_key], change_from_gross_live_bn=span[1] * factor - fixed_span[1] * (1 if population == "union" else 1 + road_key), scale_from_union=factor, population_n=n, quantity_population_n=n4 if population == "union" else lineage["lineage_population"], **declaration))
    gate("no duplicate valuation/rate row keys", len({(r["valuation"], r["real_discount_rate"], r["end"], r["arm"], r["population"]) for r in rows}) == len(rows))
    document = dict(case="oct15", original_positive_control=original_span, fixed_network_priced_span=fixed_span, valuation_fixed_spans=valuation_spans, ends=ends, recipient_share=recipient_share, modeled_deaths_by_class=modeled_deaths, gross_mortality_base_bn=gross, mortality_source=mortality, mortality_rule="Gross DOT mortality changes by FARS victim-class remaining years / age-40 reference; NHTSA net QoL embeds a productivity deduction, so the net nonmortality residual and liability dollars are held. Uniform reproduces the original base; no uniform fallback in life-year rows.", lineage_rule="v7 crash/traffic quantities and added-people road-key/recipient extrapolation transported; complete oct15 only in per-member denominator [ASSUMPTION]", capacity_rule="remaining VMT/lane = (1-s)/(1-cut); actual adopted native road key/responses shared with congestion [ASSUMPTION]; post-engine resource additions have no separately measured physical capacity response", replicate_se="not available: factorial sensitivity, not a confidence interval", all_passed=True, gates=GATES, input_pins=pins, oct15_input_pins=new_pins)
    print(f"physical footprint {require_within_budget('crash capacity and mortality') / 1e9:.3f} GB")
    outputs = {"capacity_items_oct15.csv": csv_text(rows), "capacity_components_oct15.csv": csv_text(components),
               "capacity_extrema_oct15.csv": csv_text(extrema), "capacity_model_oct15.json": json.dumps(document, indent=2) + "\n"}
    with tempfile.TemporaryDirectory(dir=OUT) as stage:
        for name, text in outputs.items():
            (Path(stage) / name).write_text(text)
        if args.pin_new_inputs:
            pinned = Path(stage) / "pins_oct15.json"
            pinned.write_text(json.dumps({"rule": "Explicitly admitted verified adopted native road and observed mortality-age inputs", "sha256": new_pins}, indent=2) + "\n")
            os.replace(pinned, pin_path)
        for name in outputs:
            os.replace(Path(stage) / name, OUT / name)
    for row in rows:
        if row["arm"] == "multivehicle_only":
            print(f"{row['valuation']}/{row['real_discount_rate']} {row['end']} {row['population']}: {row['central_bn']:.6f}; capacity-key change {row['live_key_delta_bn']:+.6f}; mortality-only {row['mortality_only_delta_bn']:+.6f}")
    print(f"PASS {len(GATES)} gates; elapsed_s={time.perf_counter()-started:.3f}")


if __name__ == "__main__":
    main()
