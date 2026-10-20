"""Current group-side context with the public eight-column reader schema.

Native-First: existing source calculations plus the pinned generation/payload
parts. Missing coverage people have no invented household earnings or victims.
"""
from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd


COLUMNS = ["item", "kind", "bn_low", "bn_central", "bn_high", "usd_per_member_central", "basis", "note"]
SPLIT_KIND = "the account's split by generation"


def coverage_components(metadata, case, gate):
    """Return matching complete coverage counts and signed coverage costs.

    The v9 item12 block is priced before count items16/17. Their own coverage
    parts enter here once; item17 is joint minus16, never standalone17.
    """
    coverage = metadata["coverage"]
    counts = dict(coverage.get("counts_by_generation_folded", coverage["counts_by_generation"]))
    costs = {end: dict(coverage["by_end"][end]["by_generation"]) for end in ("low", "high")}
    totals = {end: float(coverage["by_end"][end]["total_bn"]) for end in costs}
    if case != "oct16":
        return counts, costs, totals
    for item in ("native_minor_calibration", "coverage_tenure"):
        meta = metadata[item]
        for group, delta in meta["coverage_people_change_by_generation"].items():
            counts[group] += delta
        parts = pd.read_csv(Path(__file__).resolve().parent.parent / meta["parts_file"])
        selected = parts[parts.scenario.eq(meta["parts_scenario"])].copy()
        if meta.get("subtract_parts_scenario"):
            subtracted = parts[parts.scenario.eq(meta["subtract_parts_scenario"])].copy()
            subtracted[["coverage_change_bn", "change_bn"]] *= -1
            selected = pd.concat([selected, subtracted], ignore_index=True)
        gate(f"oct16_group_frame_{item}_parts_present", not selected.empty)
        for end in costs:
            rows = selected[selected.end.eq(end)]
            gate(f"oct16_group_frame_{item}_source_closure_{end}",
                 abs(float(rows.change_bn.sum()) - meta["by_end"][end]["total_bn"]) < 1e-9)
            for group in counts:
                gate(f"oct16_group_frame_{item}_source_generation_{end}_{group}",
                     abs(float(rows.loc[rows.generation.eq(group), "change_bn"].sum())
                         - meta["by_end"][end]["by_generation_bn"][group]) < 1e-9)
                delta = float(rows.loc[rows.generation.eq(group), "coverage_change_bn"].sum())
                costs[end][group] += delta
                totals[end] += delta
    return counts, costs, totals


def build_group_frame(model):
    wl = model.wl
    case = wl.CASE.get("case", "oct15")
    table, _, info = wl.group_frame(model.B, model.d, model.I, model.fin, pw=model.mw)
    wl.gate("oct15_group_frame_public_schema", list(table.columns) == COLUMNS)
    table = table.copy()
    metadata = model.payload["meta"]
    population = metadata[wl.CASE.get("population_key", "population_v8")]
    total_people = population["with_coverage"]
    generation = pd.read_csv(io.BytesIO(wl.read_input("generations")))
    generation = generation.set_index(["convention", "generation", "band_end"])
    rows = table.index[table.kind.eq(SPLIT_KIND)].tolist()
    wl.gate("oct15_group_frame_three_generation_rows", len(rows) == len(wl.GENERATIONS))
    source = f"[DATA: generation_results_{case}.csv at {wl.CASE['gen']}; corrected {case} payload]"
    for index, (group, _) in zip(rows, wl.GENERATIONS, strict=True):
        low, high = [float(generation.loc[("b", group, end), "cost_bn"]) for end in ("low", "high")]
        people = float(generation.loc[("b", group, "low"), "population"])
        wl.gate(f"{case}_group_frame_generation_population_{group}", people > 0 and
                abs(people - float(generation.loc[("b", group, "high"), "population"])) < 1e-6)
        table.loc[index, "item"] = f"generation account {group} (NAS parent allocation)"
        table.loc[index, ["bn_low", "bn_central", "bn_high", "usd_per_member_central"]] = [
            low, (low + high) / 2, high, (low + high) / 2 * 1e9 / people]
        table.loc[index, "basis"] = source
        table.loc[index, "note"] = ("Convention b: NAS parent allocation, including children assigned with their parents; "
            "this is not the birthplace-only convention a. Complete current generation, including its declared coverage people and dollars. "
            "This is cost to other residents, with no reference population; not a gain received by the group. "
            "Coverage subset rows below are already included and must not be added again.")
    endpoints = model.fin[wl.CASE["model"]]["ends"]
    generation_people = sum(float(generation.loc[("b", group, "low"), "population"]) for group, _ in wl.GENERATIONS)
    wl.gate(f"{case}_group_frame_generation_population_closure", abs(generation_people - total_people) < 1e-6)
    for end in ("low", "high"):
        actual = float(table.loc[rows, f"bn_{end}"].sum())
        wl.gate(f"oct15_group_frame_generation_closure_{end}", abs(actual - endpoints[end]["cost_bn"]) < 1e-6,
                generations_bn=actual, case_bn=endpoints[end]["cost_bn"])
    direct = table.index[table.item.str.startswith("direct fiscal transfer received:")]
    wl.gate("oct15_group_frame_one_direct_A", len(direct) == 1)
    index = direct[0]
    low, high = [-endpoints[end]["A_bn"] for end in ("low", "high")]
    table.loc[index, ["bn_low", "bn_central", "bn_high", "usd_per_member_central"]] = [
        low, (low + high) / 2, high, (low + high) / 2 * 1e9 / total_people]
    table.loc[index, "basis"] = f"[CALCULATION: exact {case} fiscal_specs A_bn, sign flipped; full coverage denominator]"
    table.loc[index, "note"] = ("Accounting response A, including imputed capital and post-engine components. "
        "It is not all cash received by group members: item11 contains effects on non-members who stay. "
        "Private production P and induced receipts F are excluded; all complete-lineage members enter the denominator.")
    own_wages = table.item.str.startswith(("wage competition among the group's own workers", "wage gain of the group's own workers"))
    table.loc[own_wages, "usd_per_member_central"] = table.loc[own_wages, "bn_central"] * 1e9 / total_people
    table.loc[own_wages, "note"] += (" Earnings effects cover source-located records and the declared original descendant proxy; "
        "coverage people's unlocated earnings effects are not imputed. Per-member value divides that measured/modelled "
        "contribution by the complete lineage population, coverage included.")
    place = table.item.str.startswith("first generation (born in Mexico): market gain")
    g1_population = float(generation.loc[("a", "G1", "low"), "population"])
    table.loc[place, "usd_per_member_central"] = table.loc[place, "bn_central"] * 1e9 / g1_population
    table.loc[place, "note"] += (" This is the source-located earnings contribution; missing G1 members' earnings are unmeasured. "
        "Its per-member denominator is the complete G1 population, coverage included.")
    counts, coverage_costs, coverage_totals = coverage_components(metadata, case, wl.gate)
    appended = []
    for group, _ in wl.GENERATIONS:
        low, high = [float(coverage_costs[end][group]) for end in ("low", "high")]
        people = float(counts[group])
        appended.append(dict(item=f"coverage subset already included in the {group} account", kind="coverage decomposition, already included",
            bn_low=low, bn_central=(low + high) / 2, bn_high=high,
            usd_per_member_central=(low + high) / 2 * 1e9 / people if people else np.nan,
            basis=f"[DATA: corrected {case} meta.coverage and own coverage parts of count items16/17]" if case == "oct16"
                  else f"[DATA: corrected {case} meta.coverage.by_end and counts_by_generation]",
            note=f"{people:.8f} net-missing group members; unlocated in CPS households, excluded from the payer pool. "
                  "Source-generation attribution; these are not the NAS parent-assigned generation memberships. "
                  "Modelled correction, already included in the complete generation and main case; never add this subset again."))
    for end in ("low", "high"):
        wl.gate(f"oct15_group_frame_coverage_closure_{end}", abs(sum(row[f"bn_{end}"] for row in appended)
                - coverage_totals[end]) < 1e-9)
    wl.gate("oct15_group_frame_coverage_count", abs(sum(counts.values())
            - population["coverage"]) < 1e-6)
    original_victim = table.item.str.contains("victims inside", regex=False)
    table.loc[original_victim, "note"] += (" Preserved primary equal-footing identified-union estimate; "
        "coverage adds no sender crime incidents. This row is not a new DOT-price estimate for all completed members.")
    from p8_social import environment
    for row in environment(model.source)["current_social_rows"]:
        if row["item"] != "victims":
            continue
        parts = row["v8_added_by_end_bn"]
        # These people were recipients outside the lineage before item10.
        # Their now in-group harm moves across that boundary, rather than
        # creating an additional crime-sender total.
        low, high = [float(parts[end]["completion_receivers_bn"]) for end in ("low", "high")]
        appended.append(dict(item="completion members' victim harm transferred from the outside-recipient boundary",
            kind="recipient-boundary subset, already transferred", bn_low=low, bn_central=(low + high) / 2, bn_high=high,
            usd_per_member_central=(low + high) / 2 * 1e9 / population["completion"],
            basis="[DATA: live social current_social_rows victims v8_added_by_end_bn.completion_receivers_bn]",
            note="Negative harm on observed completion recipients; the outside social row already removes it. "
                  "Per-member value uses the source completion-recipient count carried in population metadata, "
                  "not a newly identified calibrated recipient denominator. "
                 "DOT valuation; shown separately from the preserved NCVS in-group source footing, never summed silently."))
    table = pd.concat([table, pd.DataFrame(appended, columns=COLUMNS)], ignore_index=True)
    coverage_context = dict.fromkeys(COLUMNS, np.nan)
    coverage_context.update(item="unlocated coverage members: household earnings and migration counterfactual unmeasured",
        kind="unpriced group context", basis=f"[DATA: meta.{wl.CASE.get('population_key', 'population_v8')}.coverage]",
        note="Coverage people enter fiscal/generation denominators. Their household resources and Mexico-counterfactual "
             "earnings are unlocated; no individual earnings, place premium or household sharing is invented.")
    table = pd.concat([table, pd.DataFrame([coverage_context], columns=COLUMNS)], ignore_index=True)
    wl.gate("oct15_group_frame_unique_items", table.item.is_unique)
    info.update(complete_members_m=total_people / 1e6, coverage_unlocated_m=population["coverage"] / 1e6,
                observed_completion_m=population["completion"] / 1e6)
    return table[COLUMNS], info


def produce_group_frame(model, out):
    table, info = build_group_frame(model)
    path = Path(out) / "group_frame.csv"
    table.to_csv(path, index=False, lineterminator="\n", float_format="%.12g")
    return table, info
