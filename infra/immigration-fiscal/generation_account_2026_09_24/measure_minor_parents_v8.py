"""Measure observed parent routing beside the historical modeled descendant pool.

OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/measure_minor_parents_v8.py
Reads the principal pinned CPS zip directly, never writes an upstream cache.
SDR uncertainty is conditional on the modeled age denominator and membership
definitions; it excludes misreporting, coverage and loss-model uncertainty.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import json
import resource
import subprocess
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget
import frame as F

GENS = F.GENS
GATES = []


def gate(name, ok, **detail):
    if not ok:
        raise RuntimeError(f"[BLOCKED] {name}: {detail}")
    GATES.append(dict(name=name, passed=True, **detail))


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sdr(values):
    v = np.asarray(values, float)
    if v.shape != (161,) or not np.isfinite(v).all():
        raise ValueError("[BLOCKED] SDR requires central plus 160 finite replicates")
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def record(values):
    v = np.asarray(values, float)
    return dict(estimate=float(v[0]), sampling_se=sdr(v), replicates=v.tolist())


def weighted(mask, weights, fractions=None):
    selected = weights[mask]
    if fractions is not None:
        selected = selected * np.asarray(fractions)[mask, None]
    return selected.sum(axis=0)


def principal_frame():
    fields = ["PH_SEQ", "PPPOS", "SPM_ID", "PRPERTYP", "A_AGE", "PRCITSHP", "PENATVTY",
              "PEMNTVTY", "PEFNTVTY", "PRDTHSP", "PEHSPNON", "A_LINENO", "PEPAR1", "PEPAR2",
              "PEPAR1TYP", "PEPAR2TYP", "PF_SEQ", "MARSUPWT"]
    with zipfile.ZipFile(F.CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"])
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", *F.REPS])
    d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    gate("all principal person weights linked", not d[F.REPS].isna().any().any())
    gate("central weights equal published person weights", (d.MARSUPWT / 100 - d.pwwgt0).abs().max() < .01,
         tolerance_people=.01)
    d = d.merge(hh, left_on="PH_SEQ", right_on="H_SEQ", validate="many_to_one", how="left")
    gate("every principal person has household", not d.H_SEQ.isna().any())
    d = d.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    weights = d[F.REPS].to_numpy(float)
    return d.drop(columns=F.REPS[1:]), weights


def row4_weights(d, weights, civilian, union):
    # Load the authoritative scale_cell implementation rather than duplicating
    # its columnwise reweight. ACS targets are the principal case's saved row4.
    L = load_module(FISCAL / "cps_imputation_keys_2026_09_23/combine_onbooks_lane.py", "minor_weight_builder")
    ref = json.loads((FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json").read_text())
    result = weights
    moved = np.zeros(len(d), bool)
    factors = {}
    for name, status in (("naturalized", 4), ("noncitizen", 5)):
        mask = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.eq(status).to_numpy() & ~d.GESTFIPS.isin(L.CA_TX).to_numpy()
        r = ref["row4_factors"][name]
        total = weights[mask, 0].sum()
        gate(f"principal row4 {name} mask and factor", int(mask.sum()) == r["records"]
             and abs(total - r["cps_population"]) < 1e-6
             and abs(r["acs_population"] / total - r["factor"]) < 1e-12,
             count_tolerance_people=1e-6, factor_tolerance=1e-12)
        result, factor = L.scale_cell(result, mask, r["acs_population"])
        factors[name] = factor.tolist()
        moved |= mask
    gate("row4 changes only canonical union civilians", not (moved & civilian & ~union).any())
    gate("principal row4 population closes", abs(result[union, 0].sum() - ref["populations"]["row4"]) < 1e-6,
         tolerance_people=1e-6)
    gate("native weights unchanged in every replicate", np.array_equal(result[~moved], weights[~moved]))
    return result, factors


def expanded_assignments(d, civilian, union, gens, added):
    updated = {g: m.copy() for g, m in gens.items()}
    gate("observed addition outside canonical union", not (added & union).any())
    updated["G3plus"] |= added
    enlarged = union | added
    om, rules, parents = F.assignments(d, civilian, enlarged, updated)
    return enlarged, updated, om, rules, parents


def rule_breakdown(d, union, gens, omega, rules, parents, weights, linked_union_override=None):
    age = d.A_AGE.to_numpy()
    linked_union = ((parents >= 0) & union[np.maximum(parents, 0)]).any(axis=1)
    if linked_union_override is not None:
        linked_union = linked_union_override
    out = {}
    for j, g in enumerate(GENS):
        by = {}
        adult = union & (age >= 18)
        minor = union & (age < 18)
        by["adults_own_generation"] = record(weighted(adult, weights, omega["b"][:, j]))
        by["minors_with_union_parent"] = record(weighted(minor & linked_union, weights, omega["b"][:, j]))
        by["minors_without_union_parent"] = record(weighted(minor & ~linked_union, weights, omega["b"][:, j]))
        by["population_a"] = record(weighted(gens[g], weights))
        by["population_b"] = record(weighted(union, weights, omega["b"][:, j]))
        by["own_generation_minors_without_union_parent"] = dict(
            records=int((minor & gens[g] & ~linked_union).sum()),
            **record(weighted(minor & gens[g] & ~linked_union, weights)))
        by["adult_records"] = int((adult & gens[g]).sum())
        by["by_rule"] = {r: dict(records=int((minor & (rules == r) & (omega["b"][:, j] > 0)).sum()),
                                  **record(weighted(minor & (rules == r), weights, omega["b"][:, j])))
                          for r in sorted(set(rules[minor]))}
        by["minor_origin_by_rule"] = {origin: {
            r: dict(records=int((minor & gens[origin] & (rules == r) & (omega["b"][:, j] > 0)).sum()),
                    **record(weighted(minor & gens[origin] & (rules == r), weights, omega["b"][:, j])))
            for r in sorted(set(rules[minor]))} for origin in GENS}
        pieces = sum(np.asarray(by[k]["replicates"]) for k in
                     ("adults_own_generation", "minors_with_union_parent", "minors_without_union_parent"))
        gap = float(np.abs(pieces - by["population_b"]["replicates"]).max())
        gate(f"{g} rule numerator closes all 161 columns", gap < 1e-6, max_gap_people=gap, tolerance_people=1e-6)
        out[g] = by
    return out


def modeled_minor_denominator():
    script = """
const fs=require('fs'),V6=require('./v6_split.cjs');
const lin=JSON.parse(fs.readFileSync('../main_case_2026_10_14/derived/corrections.json')).meta.lineage;
const H=JSON.parse(fs.readFileSync('./derived/v4_inputs.json')).headcount.a.G3plus;
const adults=V6.addedAdults(lin,H.adults/H.population);
console.log(JSON.stringify({minor_count:lin.counts.at_g3_rate-adults.by_part.g3_rate,
 counts:lin.counts,age_reading:lin.age_mix.reading,adults}));
"""
    run = subprocess.run(["node", "-e", script], cwd=HERE, text=True, capture_output=True, check=True)
    result = json.loads(run.stdout)
    gate("modeled age denominator positive", result["minor_count"] > 0)
    return result


def completed_assignment_trace(d, union, gens, old_omega, old_rules, completed,
                               completed_gens, new_omega, new_rules, parents,
                               reporters, children, weights):
    """Exact NAS replay changes; demographic own generation is a separate label.

    Membership expansion changes the eligible parent/oldest-relative universe,
    so existing minors can change even though their own generation is unchanged.
    """
    old_label, new_label = F.label(gens, len(d)), F.label(completed_gens, len(d))
    age = d.A_AGE.to_numpy()
    changed = union & np.any(old_omega["b"] != new_omega["b"], axis=1)
    gate("completion changes no canonical adult assignment", not (changed & (age >= 18)).any())
    def person(i):
        return dict(PH_SEQ=int(d.PH_SEQ.iloc[i]), PPPOS=int(d.PPPOS.iloc[i]), A_AGE=int(age[i]))
    def oldest(i, membership):
        family = (d.PH_SEQ.eq(d.PH_SEQ.iloc[i]) & d.PF_SEQ.eq(d.PF_SEQ.iloc[i])).to_numpy()
        candidates = np.flatnonzero(family & membership & (age >= 18))
        if not len(candidates):
            return None
        row = max(candidates, key=lambda j:(age[j], -j))
        return dict(**person(row), row=int(row))
    def row_record(i):
        links = []
        for slot, p in enumerate(parents[i], 1):
            if p < 0:
                continue
            links.append(dict(slot=slot, **person(p), parent_type=int(d[f"PEPAR{slot}TYP"].iloc[i]),
                              old_union=bool(union[p]), completed_union=bool(completed[p]),
                              new_reporter=bool(reporters[p]), native_nonreporter=bool(children[p]),
                              old_own_generation=GENS[old_label[p]] if union[p] else None,
                              completed_own_generation=GENS[new_label[p]] if completed[p] else None))
        return dict(**person(i), people=float(weights[i, 0]), replicate_weights=weights[i].tolist(),
                    omega=new_omega["b"][i].tolist(), old_omega=old_omega["b"][i].tolist(),
                    old_rule=str(old_rules[i]), rule=str(new_rules[i]), parent_links=links)
    reporter_rows = [row_record(i) for i in np.flatnonzero(reporters)]
    changes = []
    causes = {}
    for i in np.flatnonzero(changed):
        linked = parents[i][parents[i] >= 0]
        if any(completed[p] and not union[p] for p in linked):
            cause = "newly_included_parent"
        elif not len(linked) and (old_rules[i] == "oldest_union_relative" or new_rules[i] == "oldest_union_relative"):
            cause = "newly_included_oldest_union_relative"
        else:
            raise RuntimeError(f"[BLOCKED] unexplained completed-frame change at principal row {i}")
        row = row_record(i)
        row.update(cause=cause, own_generation=GENS[old_label[i]])
        if not len(linked):
            row.update(old_oldest_union_relative=oldest(i, union),
                       completed_oldest_union_relative=oldest(i, completed))
        changes.append(row)
        causes.setdefault(cause, []).append(i)
    cause_counts = {}
    for cause, rows in causes.items():
        mask = np.zeros(len(d), bool)
        mask[rows] = True
        delta = {g:record(weighted(mask, weights, new_omega["b"][:,j] - old_omega["b"][:,j]))
                 for j,g in enumerate(GENS)}
        cause_counts[cause] = dict(records=len(rows), persons=record(weighted(mask, weights)),
                                   net_assignment_people=delta,
                                   old_to_new_rules={f"{old} -> {new}":int((mask & (old_rules == old) & (new_rules == new)).sum())
                                       for old,new in sorted({(str(old_rules[i]),str(new_rules[i])) for i in rows})})
    reporter_destination = {g:record(weighted(reporters, weights, new_omega["b"][:,j])) for j,g in enumerate(GENS)}
    reporter_delta = {g:record(weighted(reporters, weights, new_omega["b"][:,j] - (1 if g == "G3plus" else 0)))
                      for j,g in enumerate(GENS)}
    existing_delta = {g:record(weighted(changed, weights, new_omega["b"][:,j] - old_omega["b"][:,j]))
                      for j,g in enumerate(GENS)}
    for j,g in enumerate(GENS):
        original = weighted(union, weights, old_omega["b"][:,j])
        additions = weighted(reporters | children, weights, new_omega["b"][:,j])
        actual = weighted(completed, weights, new_omega["b"][:,j])
        delta = np.asarray(existing_delta[g]["replicates"])
        gap = float(np.abs(original + additions + delta - actual).max())
        gate(f"completed NAS b {g} row change reconstruction161", gap < 1e-6, max_gap_people=gap, tolerance_people=1e-6)
    return dict(reporter_assignment_b=reporter_rows, existing_union_assignment_changes=changes,
                completed_assignment_effects=dict(
                    rule="Same frame.py convention(b), evaluated on completed observed membership; own demographic generation of all added records remains G3plus",
                    reporter_destination_people=reporter_destination,
                    reporter_minus_all_G3plus_people=reporter_delta,
                    reporter_rule_records={r:int((reporters & (new_rules == r)).sum()) for r in sorted(set(new_rules[reporters]))},
                    existing_union_delta_people=existing_delta, existing_union_changes_by_cause=cause_counts))


def propagated_assignment(older_union, old_omega, old_rules, new_omega, new_rules):
    """Explicit frozen-P7 prefix plus NAS-on-completed-membership new records."""
    return {"a":new_omega["a"],
            "b":np.where(older_union[:,None],old_omega["b"],new_omega["b"])}, np.where(older_union,old_rules,new_rules)


def measure():
    sources = [Path(__file__), HERE / "frame.py", F.CPS_ZIP,
               FISCAL / "cps_imputation_keys_2026_09_23/common.py",
               FISCAL / "cps_imputation_keys_2026_09_23/combine_onbooks_lane.py",
               FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json",
               HERE / "v6_split.cjs", HERE / "derived/v4_inputs.json",
               FISCAL / "main_case_2026_10_14/derived/corrections.json",
               FISCAL / "union_completion_2026_10_14/completion.py",
               FISCAL / "mexican_origin_population_total_2026_09_19/dt_replication.py",
               FISCAL / "mexican_origin_population_total_2026_09_19/bounds_coverage_fiscal.py",
               FISCAL / "main_case_lineage_2026_10_05/population.py",
               FISCAL / "identity_loss_propagation_2026_09_27/propagate.py",
               FISCAL / "added_age_mix_2026_10_07/measure_loss.py",
               FISCAL / "added_age_mix_2026_10_07/age_mix.py",
               FISCAL / "g3_identity_pooled_2026_10_05/analyze.py"]
    hashes = {str(p.relative_to(FISCAL)): sha(p) for p in sources}
    gate("principal CPS zip pinned", sha(F.CPS_ZIP) == F.CPS_SHA)
    d, published = principal_frame()
    civilian, union, gens = F.masks(d)
    weights, factors = row4_weights(d, published, civilian, union)
    del published
    om, rules, parents = F.assignments(d, civilian, union, gens)
    canonical = rule_breakdown(d, union, gens, om, rules, parents, weights)
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    minor = d.A_AGE.lt(18).to_numpy()
    us_m = d.PEMNTVTY.isin(F.US_AREAS).to_numpy()
    us_f = d.PEFNTVTY.isin(F.US_AREAS).to_numpy()
    mex = d.PRDTHSP.eq(1).to_numpy()
    union_g2_parent = ((parents >= 0) & gens["G2"][np.maximum(parents, 0)]).any(axis=1)
    hidden = civilian & native & minor & us_m & us_f & ~mex & ~union & union_g2_parent
    _, _, homega, hrules, _ = expanded_assignments(d, civilian, union, gens, hidden)
    persons = weighted(hidden, weights)
    equivalent = weighted(hidden, weights, homega["b"][:, 1])
    denominator = modeled_minor_denominator()
    shares = equivalent / denominator["minor_count"]
    gate("historical linked share within probability bounds in all columns", bool(((shares >= 0) & (shares <= 1)).all()))
    historical = dict(records=int(hidden.sum()), observed_persons=record(persons),
                      g2_equivalents=record(equivalent), modeled_denominator=denominator,
                      parent_rule_records={r: int((hidden & (hrules == r)).sum()) for r in sorted(set(hrules[hidden]))})
    # Check competing literal interpretations without selecting a mask to match
    # the reviewer's count. frame.py uses citizenship 1-3 as native and does not
    # require biological links for convention (b).
    parent_index = np.maximum(parents, 0)
    g2_slots = (parents >= 0) & gens["G2"][parent_index]
    both_present = (parents >= 0).all(axis=1)
    biological = np.column_stack([d.PEPAR1TYP.eq(1), d.PEPAR2TYP.eq(1)])
    parent_us = np.isin(d.PENATVTY.to_numpy()[parent_index], F.US_AREAS)
    arms = {"native_citizenship_1_or_2": d.PRCITSHP.isin([1, 2]).to_numpy(),
            "linked_G2_parent_US_area_birth": (g2_slots & parent_us).any(axis=1),
            "linked_G2_parent_biological": (g2_slots & biological).any(axis=1),
            "two_biological_US_area_born_parents": both_present & biological.all(axis=1) & parent_us.all(axis=1)}
    historical["definition_checks"] = {name: dict(records=int((hidden & mask).sum()),
        persons=record(weighted(hidden & mask, weights)),
        g2_equivalents=record(weighted(hidden & mask, weights, homega["b"][:, 1])))
        for name, mask in arms.items()}
    # The review probe conditions on linked parents' *own* birthplaces rather
    # than the child's recorded parental birthplaces. Replay that difference.
    linked = parents >= 0
    linked_us = np.where(linked, parent_us, True).all(axis=1) & linked.any(axis=1)
    review_mex = d.PEHSPNON.eq(1).to_numpy() & mex
    review_hidden = civilian & native & minor & ~review_mex & ~union & linked_us & union_g2_parent
    _, _, romega, rrules, _ = expanded_assignments(d, civilian, union, gens, review_hidden)
    review_equivalent = weighted(review_hidden, weights, romega["b"][:, 1])
    historical["reviewer_definition_replay"] = dict(
        definition="All present linked parents US-area-born; at least one canonical union G2 parent; native civilian minor outside union; not PEHSPNON=1 and PRDTHSP=1. Does not require own recorded parental birthplaces US-area-born.",
        records=int(review_hidden.sum()), persons=record(weighted(review_hidden, weights)),
        g2_equivalents=record(review_equivalent),
        selected_only_by_reviewer=dict(records=int((review_hidden & ~hidden).sum()),
                                      persons=record(weighted(review_hidden & ~hidden, weights))),
        selected_only_by_canonical_birthplace_rule=dict(records=int((hidden & ~review_hidden).sum()),
                                                       persons=record(weighted(hidden & ~review_hidden, weights))))
    strict = hidden & review_hidden
    historical["age_source_consistency_screen"] = dict(
        definition="Both child-recorded parental birthplace fields US-area-born AND every present linked parent's own birthplace US-area-born (measure_loss.py/classify screen).",
        records=int(strict.sum()), persons=record(weighted(strict, weights)),
        g2_equivalents=record(weighted(strict, weights, homega["b"][:, 1])))
    historical["source_definition_trace"] = dict(
        count="population.py -> identity_loss_propagation/propagate.py pop_p3 -> bounds_coverage_fiscal.py -> dt_replication.py: linked parent own birthplace plus grandparent birthplace; calibration two biological parents",
        age="age_mix.py -> measure_loss.py CLASSIFY_SQL -> g3_identity_pooled/analyze.py classify: both own parental birthplaces US and present linked parents US",
        interpretation="Central follows the count caller's principal linked-parent own birthplace for directly observed ancestry. The stricter age caller intersection and child-recorded birthplace-only definition are misreporting sensitivities. All present linked parent types participate in NAS convention(b), whose routing comes unchanged from frame.py; the count calibration's two-biological-parent restriction is not a routing restriction.")
    historical["child_recorded_birthplace_screen"] = dict(records=historical["records"],
        persons=historical["observed_persons"], g2_equivalents=historical["g2_equivalents"],
        parent_rule_records=historical["parent_rule_records"])
    historical.update(records=int(review_hidden.sum()), observed_persons=record(weighted(review_hidden, weights)),
                      g2_equivalents=record(review_equivalent),
                      parent_rule_records={r: int((review_hidden & (rrules == r)).sum()) for r in sorted(set(rrules[review_hidden]))})
    shares = review_equivalent / denominator["minor_count"]
    gate("central linked-parent historical share within bounds in all columns", bool(((shares >= 0) & (shares <= 1)).all()))
    # Replay the existing item10 caller's biological/consistent parent mask.
    sys.path.insert(0, str(FISCAL / "union_completion_2026_10_14"))
    completion = load_module(FISCAL / "union_completion_2026_10_14/completion.py", "minor_completion_source")
    _, _, _, _, reporters, _, _ = completion.masks(d, F)
    arms, source_mex, source_parents = completion.siblings(d, F, civilian, union)
    children = arms["biological"] & ~source_mex
    gate("historical and native observed minors disjoint", not (hidden & children).any())
    completed, completed_gens, comega, crules, cparents = expanded_assignments(
        d, civilian, union, gens, reporters | children)
    completed_breakdown = rule_breakdown(d, completed, completed_gens, comega, crules, cparents, weights)
    assignment_trace = completed_assignment_trace(d, union, gens, om, rules, completed,
        completed_gens, comega, crules, cparents, reporters, children, weights)
    propagated, prules = propagated_assignment(union, om, rules, comega, crules)
    old_parent = ((parents >= 0) & union[np.maximum(parents,0)]).any(axis=1)
    new_parent = ((parents >= 0) & completed[np.maximum(parents,0)]).any(axis=1)
    propagated_breakdown = rule_breakdown(d, completed, completed_gens, propagated, prules,
        cparents, weights, linked_union_override=np.where(union,old_parent,new_parent))
    old_headcount = json.loads((HERE / "derived/v4_inputs.json").read_text())["headcount"]["b"]
    for j,g in enumerate(GENS):
        old = weighted(union,weights,om["b"][:,j])
        gate(f"{g} principal old P7 b population matches saved headcount", abs(old[0]-old_headcount[g]["population"])<1e-6,
             tolerance_people=1e-6)
        additions = weighted(reporters | children,weights,comega["b"][:,j])
        actual = np.asarray(propagated_breakdown[g]["population_b"]["replicates"])
        gap = float(np.abs(old+additions-actual).max())
        gate(f"{g} propagated old-P7 plus new-NAS b closes161",gap<1e-6,max_gap_people=gap,tolerance_people=1e-6)
        gate(f"{g} propagated adult denominator unchanged161", propagated_breakdown[g]["adults_own_generation"]["replicates"]
             ==completed_breakdown[g]["adults_own_generation"]["replicates"])
    source_sensitivities = {}
    for name, stats in (("child_report", historical["child_recorded_birthplace_screen"]),
                        ("strict_intersection", historical["age_source_consistency_screen"])):
        values = np.asarray(stats["g2_equivalents"]["replicates"]) / denominator["minor_count"]
        source_sensitivities[name] = dict(share=float(values[0]), replicate_shares=values.tolist(),
                                         sampling_se=sdr(values), records=stats["records"])
    born = d.PENATVTY.to_numpy()
    a, b = np.maximum(source_parents[:, 0], 0), np.maximum(source_parents[:, 1], 0)
    mexican_parent = np.where(np.isin(born[a], F.US_AREAS) & source_mex[a], a, b)
    grandparent = (d.PEFNTVTY.eq(303).to_numpy() | d.PEMNTVTY.eq(303).to_numpy())[mexican_parent]
    bands = np.minimum(d.A_AGE.to_numpy() // 5, 16)
    native_by = {}
    for name, rate_mask in (("g3_rate", grandparent), ("later", ~grandparent)):
        here = children & rate_mask
        native_by[name] = dict(records=int(here.sum()), persons=record(weighted(here, weights)),
            g2_equivalents=record(weighted(here, weights, comega["b"][:, 1])),
            by_age_band=[dict(band=b, records=int((here & (bands == b)).sum()),
                             persons=record(weighted(here & (bands == b), weights)),
                             g2_equivalents=record(weighted(here & (bands == b), weights, comega["b"][:, 1])))
                         for b in range(17)])
    gate("source inputs unchanged through measurement", hashes == {str(p.relative_to(FISCAL)): sha(p) for p in sources})
    require_within_budget("minor parent measurement")
    return dict(contract="oct15 observed parent routing v1", provenance="[WORKTREE INPUT] exact source hashes",
                source_sha256=hashes, central_share=float(shares[0]), replicate_shares=shares.tolist(), sampling_se=sdr(shares),
                replicate_order=F.REPS, convention="frame.py (b), actual union parents split equally; parent slots outside union stay own; no slots use oldest union adult relative, else own",
                uncertainty="SDR sampling only; modeled age denominator held fixed. Excludes misreporting, coverage, loss model, age-mix uncertainty and the policy for the modeled unlinked remainder.",
                unlinked_historical_rule="The modeled remainder stays G3plus; no parental observation is invented.",
                historical_observed_definition="Civilian native (PRCITSHP 1-3) under 18, outside canonical union, not (PEHSPNON=1 and PRDTHSP=1), with at least one linked canonical-union G2 parent; every present linked parent's own PENATVTY in US_AREAS. All parent types, as frame.py (b).",
                principal_records=len(d), row4_factors=factors, historical=historical,
                source_definition_sensitivities=source_sensitivities,
                adult_population_replicates={g: x["adults_own_generation"]["replicates"]
                                             for g, x in completed_breakdown.items()},
                canonical_rule_breakdown=canonical, completed_observed_rule_breakdown=completed_breakdown,
                propagated_observed_rule_breakdown=propagated_breakdown,
                existing_union_parent_vintage="P7_frozen",
                propagated_rule="Original canonical union retains frozen P7 parent/state/credit routing; new reporters/native children take frame.py(b) on completed observed membership. This is a declared composite vintage, not a full completed-frame replay.",
                existing_union_rebuild_deferral="Six original minor assignments change under a full completed frame; their exact rows/161 weights/net changes are retained beside. Parent defers coordinated parent/state/credit rebuild to preserve frozen P7 inputs.",
                observed_reporters=dict(records=int(reporters.sum()), adults=record(weighted(reporters & ~minor, weights)),
                                        persons=record(weighted(reporters, weights))),
                native_observed_children=dict(records=int(children.sum()), by_rate_class=native_by,
                                              persons=record(weighted(children, weights)),
                                              g2_equivalents=record(weighted(children, weights, comega["b"][:, 1]))),
                source_completion_gates=completion.GATES, gates=GATES, **assignment_trace)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "inputs/minor_parent_measurement_oct15.json")
    args = parser.parse_args()
    started = time.perf_counter()
    result = measure()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(dict(output=str(args.out), central_share=result["central_share"],
                          sampling_se=result["sampling_se"], seconds=time.perf_counter()-started,
                          peak_footprint_bytes=require_within_budget("minor parent measurement publication"),
                          maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == "__main__":
    main()
