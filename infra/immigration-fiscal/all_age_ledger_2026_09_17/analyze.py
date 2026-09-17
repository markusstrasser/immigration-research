"""All-age partial accounts: consistent domains, components and uncertainty.

Native-First: reuse held parsers and unit component builders; NumPy sufficient
totals retain every CPS replicate and the complete MEPS donor covariance.
"""
from pathlib import Path
import argparse
import json
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(FISCAL / "build"))
import extend_ledger as ext
from meps_health_transport_2024 import donor_model, read_meps
from estimator import account, contrast, sufficient, sum_cells, summarize, standardized_gap

COMPONENTS = ["tax", "cash", "noncash", "employer", "sales", "owner_property", "school", "lunch"]
COEFFICIENTS = np.array([1, -1, -1, 1, 1, 1, -1, 1], dtype=float)
BASE_COEFFICIENTS = np.array([1, -1, -1, 0, 0, 0, 0, 0], dtype=float)
TARGETS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid", "mexican_observed_total"]
REFERENCES = ["third_plus_nh_white", "all_native", "native_two_us_parents", "other_natives"]


def matrices(state):
    d, index, totals = state["d"], state["index"], state["totals"]
    share = lambda x: ext.allocate(x, index, np.ones(len(d), bool), state["n_units"])
    unit = [totals[k] for k in ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
                               "employer_payroll", "sales_tax_share35", "property_tax_owner"]]
    unit += [ext.PUPIL_RATIO_NATIVE_ACS * totals["k12_cost_at_full_attendance"], totals["school_lunch"]]
    shared = np.column_stack([share(x) for x in unit])
    personal = shared.copy()
    personal[:, 0] = d[["FICA", "FEDTAX_AC", "STATETAX_A"]].sum(axis=1)
    personal[:, 1] = d[list(ext.CASH.values())].sum(axis=1)
    wage = d.WSAL_VAL.clip(lower=0).to_numpy()
    personal[:, 3] = ext.OASDI_RATE * np.minimum(wage, ext.OASDI_CAP_2024) + ext.HI_RATE * wage
    personal[:, 6] = (d.A_AGE.between(5, 17) * d.GESTFIPS.map(state["params"].per_pupil_current_spending)
                      * ext.PUPIL_RATIO_NATIVE_ACS).to_numpy()
    for k, total in enumerate(unit):
        for name, matrix in [("shared", shared), ("personal", personal)]:
            actual = np.bincount(index, weights=matrix[:, k], minlength=state["n_units"])
            if not np.allclose(actual, total, rtol=1e-10, atol=1e-5):
                raise ValueError(f"Unit conservation failed for {name}/{COMPONENTS[k]}")
    return shared, personal, share(totals["property_tax_renter_proxy"])


def adult_component_anchor(state, shared, source):
    """Reproduce the held adult component release before expanding its domain."""
    prior = pd.read_csv(source)
    prior = prior[prior.allocation.eq("equal_all_members") & prior.weighting.eq("person")]
    names = ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
             "employer_payroll", "sales_tax_share35", "property_tax_owner",
             "k12_charged_acs_native"]
    count, max_residual = 0, 0.0
    for group in TARGETS[:3] + REFERENCES[:2]:
        use = state["group"][group] & state["adults_25_64"]
        w = state["person_weights"][use]
        estimates = shared[use, :7].T @ w / w.sum(axis=0)
        for k, metric in enumerate(names):
            row = prior[prior.group.eq(group) & prior.metric.eq(metric)]
            if len(row) != 1:
                raise ValueError(f"Missing/duplicate adult anchor: {group}/{metric}")
            residual = abs(estimates[k, 0] - row.estimate.iloc[0])
            se = np.sqrt(4/160 * np.square(estimates[k, 1:]-estimates[k, 0]).sum())
            se_residual = abs(se - row.se_sdr.iloc[0])
            if max(residual, se_residual) > 1e-6:
                raise ValueError(f"Adult component anchor failed: {group}/{metric}")
            max_residual = max(max_residual, residual, se_residual)
            count += 1
    return dict(rows=count, means_and_standard_errors=True, max_residual=max_residual)


def generate():
    cps = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    medical_zip = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    medical_sas = medical_zip.with_name("h256su.txt")
    state = ext.build(argparse.Namespace(cps_zip=cps))
    d = state["d"]
    weights = state["person_weights"]
    heads = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID")
    head_weights = heads[ext.base.REPS].to_numpy()[state["index"]]
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {name: state["group"][name] & civilian for name in TARGETS[:3] + REFERENCES[:2]}
    member_count = sum(groups[name].astype(int) for name in TARGETS[:3])
    if member_count.max() > 1:
        raise ValueError("Target categories overlap")
    us = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us)
    groups["native_two_us_parents"] = groups["all_native"] & parents_us.to_numpy()
    groups["other_natives"] = groups["all_native"] & (member_count == 0)
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    shared, personal, renter = matrices(state)
    adult_source = ext.HERE / "extended_ledger_by_generation.csv"
    adult_check = adult_component_anchor(state, shared, adult_source)
    medical, anchors = read_meps(medical_zip, medical_sas)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    if (d.loc[~exposure, "A_AGE"] > 0).any():
        raise ValueError("Post-reference-year exclusion contains noninfant")
    if (d.PENATVTY <= 0).any():
        raise ValueError("Unknown birthplace cannot select a medical donor")
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    sources = [cps, medical_zip, medical_sas, ext.HERE / "state_parameters.csv",
               adult_source, Path(ext.__file__), Path(ext.base.__file__),
               Path(sys.modules[donor_model.__module__].__file__), Path(__file__), HERE / "estimator.py"]
    audit = dict(inputs=[dict(path=str(p), sha256=ext.base.sha(p)) for p in sources],
                 validation=state["validation"], medical_anchors=anchors, scenarios={}, checks={})
    audit["checks"]["adult_component_anchor"] = adult_check
    rows, comp_rows, band_rows, rep_saved, grad_saved = [], [], [], {}, {}
    # Exactly conserve all unit-component dollars under reallocation, in EVERY
    # replicate. This includes records outside the later civilian reporting domain.
    fixed_shared = shared.T @ head_weights
    fixed_personal = personal.T @ head_weights
    if not np.allclose(fixed_shared, fixed_personal, atol=.02, rtol=1e-10):
        raise ValueError("Fixed-head-weight attribution changed the national budget")
    person_shared, person_personal = shared.T @ weights, personal.T @ weights
    audit["checks"]["fixed_head_budget_max_residual"] = float(np.max(np.abs(fixed_shared-fixed_personal)))
    audit["person_weight_reallocation_dollar_changes"] = dict(zip(COMPONENTS, (person_personal-person_shared)[:, 0].tolist()))
    scenarios = {
        "baseline": ("shared", "person", False, BASE_COEFFICIENTS),
        "all_age_shared": ("shared", "person", False, COEFFICIENTS),
        "personal_sources": ("personal", "person", False, COEFFICIENTS),
        "unit_head_weighted": ("shared", "head", False, COEFFICIENTS),
        "personal_head_weighted": ("personal", "head", False, COEFFICIENTS),
        "finer_child_age": ("shared", "person", False, COEFFICIENTS),
        "insurance_health": ("shared", "person", True, COEFFICIENTS),
        "no_health": ("shared", "person", False, COEFFICIENTS),
        "retain_lunch_overlap": ("shared", "person", False, COEFFICIENTS * [1, 1, 1, 1, 1, 1, 1, 0]),
        "sales25": ("shared", "person", False, COEFFICIENTS * [1, 1, 1, 1, 25/35, 1, 1, 1]),
        "sales45": ("shared", "person", False, COEFFICIENTS * [1, 1, 1, 1, 45/35, 1, 1, 1]),
        "pupil90": ("shared", "person", False, COEFFICIENTS * [1, 1, 1, 1, 1, 1, .90/ext.PUPIL_RATIO_NATIVE_ACS, 1]),
        "renter_property": ("renter", "person", False, COEFFICIENTS),
    }
    cache = {}
    for label, (allocation, weighting, insured, coefficients) in scenarios.items():
        print(f"[scenario] {label}", flush=True)
        scenario_bands = np.digitize(d.A_AGE, [5, 12, 18, 25, 35, 45, 55, 65, 75]) if label == "finer_child_age" else bands
        band_count = 10 if label == "finer_child_age" else 8
        cache_key = (allocation, weighting, insured, band_count)
        if cache_key not in cache:
            cells, codes, covariance = donor_model(medical, d, insured)
            means = cells.mean_public_paid.to_numpy()
            health = np.eye(len(cells))[codes] * exposure[:, None]
            matrix = personal if allocation == "personal" else shared
            if allocation == "renter":
                matrix = shared.copy()
                matrix[:, 5] += renter
            w = weights if weighting == "person" else head_weights
            # Head-dollar arms change the dollar estimator for the reallocated
            # unit components only; population and direct medical stay person-weighted.
            stats = sufficient(matrix, health, w, groups, scenario_bands, band_count,
                               population_weights=weights, health_weights=weights)
            stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
            cache[cache_key] = stats, means, covariance
            cells.to_csv(out / f"donor_cells_{'insurance' if insured else 'age_birth'}.csv", index=False)
        stats, means, covariance = cache[cache_key]
        if label == "no_health":
            means, covariance = np.zeros_like(means), np.zeros_like(covariance)
        audit["scenarios"][label] = dict(allocation=allocation, weighting=weighting, health_insurance=insured,
                                         population_weighting="person", direct_health_weighting="person",
                                         band_count=band_count, medical_included=label != "no_health", coefficients=coefficients.tolist())
        # Use person-weighted white age shares for every allocation/weight arm.
        # These are fixed targets; their own estimation error is not propagated.
        age_totals = np.bincount(scenario_bands[groups[REFERENCES[0]]], weights=weights[groups[REFERENCES[0]], 0], minlength=band_count)
        age_shares = age_totals / age_totals.sum()
        for target in TARGETS:
            cell = stats[target]
            n = cell["n"].sum(axis=0)
            y = account(cell, coefficients, means).sum(axis=0)
            q = -cell["h"][:, :, 0].sum(axis=0)
            for metric, v, grad in [("absolute_total", y, q), ("absolute_per_person", y/n, q/n[0])]:
                rows.append(dict(scenario=label, target=target, reference="", matching="", metric=metric,
                                 population=float(n[0]), **summarize(v, grad, covariance)))
                rep_saved[f"{label}|{target}|{metric}"] = v
                grad_saved[f"{label}|{target}|{metric}"] = grad
            for reference in REFERENCES:
                ref = stats[reference]
                std, qs = standardized_gap(cell, ref, coefficients, means, age_shares)
                rows.append(dict(scenario=label, target=target, reference=reference, matching="common_age",
                                 metric="standardized_gap_per_person", population=float(n[0]),
                                 **summarize(std, qs, covariance)))
                rep_saved[f"{label}|{target}|{reference}|common_age"] = std
                grad_saved[f"{label}|{target}|{reference}|common_age"] = qs
                for matched in [True, False]:
                    v, grad = contrast(cell, ref, coefficients, means, matched)
                    match = "age_band" if matched else "crude"
                    for metric, vec, gradient in [("gap_total", v, grad), ("gap_per_person", v/n, grad/n[0])]:
                        rows.append(dict(scenario=label, target=target, reference=reference, matching=match,
                                         metric=metric, population=float(n[0]), **summarize(vec, gradient, covariance)))
                    rep_saved[f"{label}|{target}|{reference}|{match}"] = v
                    grad_saved[f"{label}|{target}|{reference}|{match}"] = grad
                    if matched:
                        ratio = cell["n"] / ref["n"]
                        components = (cell["y"] - ratio[:, None, :] * ref["y"]).sum(axis=0)
                        component_gaps = coefficients[:, None] * components
                        medical_gap = -(np.einsum("bjr,j->br", cell["h"], means)
                                        - ratio * np.einsum("bjr,j->br", ref["h"], means)).sum(axis=0)
                        if not np.allclose(component_gaps.sum(axis=0) + medical_gap, v, atol=.02, rtol=1e-10):
                            raise ValueError("Composite differs from summed components")
                        if label in ["baseline", "all_age_shared", "personal_sources", "unit_head_weighted", "personal_head_weighted"]:
                            for k, name in enumerate(COMPONENTS):
                                comp_rows.append(dict(scenario=label, target=target, reference=reference,
                                                      component=name, gap=float(component_gaps[k, 0])))
                            comp_rows.append(dict(scenario=label, target=target, reference=reference,
                                                  component="medical", gap=float(medical_gap[0])))
            if label in ["baseline", "all_age_shared", "personal_sources"]:
                for b in range(band_count):
                    band_rows.append(dict(scenario=label, target=target, band=b,
                                          population=float(cell["n"][b, 0]),
                                          balance_per_person=float(account(cell, coefficients, means)[b, 0]/cell["n"][b, 0])))
        # Same-reference contrast must vanish including donor covariance.
        z, qz = contrast(stats[REFERENCES[0]], stats[REFERENCES[0]], coefficients, means)
        if np.max(np.abs(z)) > .01 or np.max(np.abs(qz)) > 1e-5:
            raise ValueError("Self-reference does not cancel")
        # A common $1000 per-person charge cannot change any age-matched gap.
        target, ref = stats[TARGETS[-1]], stats[REFERENCES[0]]
        ratio = target["n"] / ref["n"]
        charged = ((account(target, coefficients, means) - 1000*target["n"])
                   - ratio*(account(ref, coefficients, means) - 1000*ref["n"])).sum(axis=0)
        v, grad = contrast(target, ref, coefficients, means)
        if not np.allclose(charged, v, atol=.02, rtol=1e-10):
            raise ValueError("Common charge failed cancellation")
        for j in range(len(means)):
            moved = means.copy()
            moved[j] += 1
            vv, _ = contrast(target, ref, coefficients, moved)
            if not np.isclose(vv[0] - v[0], grad[j], atol=.001, rtol=1e-8):
                raise ValueError("Medical donor gradient failed")
        audit["checks"][label] = dict(component_sum=True, self_reference=True,
                                      common_charge=True, donor_gradient=True)
    table = pd.DataFrame(rows)
    paired = []
    donor_covariance = cache[("shared", "head", False, 8)][2]
    for target in TARGETS:
        for suffix in ["absolute_total"] + [f"{ref}|age_band" for ref in REFERENCES]:
            a, b = f"personal_head_weighted|{target}|{suffix}", f"unit_head_weighted|{target}|{suffix}"
            paired.append(dict(target=target, contrast=suffix,
                               **summarize(rep_saved[a]-rep_saved[b], grad_saved[a]-grad_saved[b], donor_covariance)))
    pd.DataFrame(paired).to_csv(out / "fixed_budget_attribution.csv", index=False)
    generation_rows = []
    for label in ["all_age_shared", "personal_sources", "unit_head_weighted", "personal_head_weighted"]:
        for later, earlier in [(TARGETS[1], TARGETS[0]), (TARGETS[2], TARGETS[1]), (TARGETS[2], TARGETS[0])]:
            # The identical standardized reference cancels. These compare
            # different cross-sectional populations, not linked family change.
            a, b = f"{label}|{later}|{REFERENCES[0]}|common_age", f"{label}|{earlier}|{REFERENCES[0]}|common_age"
            generation_rows.append(dict(scenario=label, later=later, earlier=earlier,
                                       **summarize(rep_saved[a]-rep_saved[b], grad_saved[a]-grad_saved[b], donor_covariance)))
    pd.DataFrame(generation_rows).to_csv(out / "generation_contrasts.csv", index=False)
    transfers = []
    transfer_masks = {g: groups[g] for g in TARGETS[:3]}
    transfer_masks["all_other_records"] = member_count == 0
    signed_change = (personal-shared) * COEFFICIENTS
    transfer_sum = np.zeros((len(COMPONENTS), 161))
    for group, mask in transfer_masks.items():
        change = signed_change[mask].T @ head_weights[mask]
        transfer_sum += change
        for k, name in enumerate(COMPONENTS):
            transfers.append(dict(group=group, component=name,
                                  **summarize(change[k], np.zeros(1), np.zeros((1, 1)))))
    if np.max(np.abs(transfer_sum)) > .02:
        raise ValueError("Fixed-budget transfers fail exhaustive signed cancellation")
    pd.DataFrame(transfers).to_csv(out / "fixed_budget_transfers.csv", index=False)
    attribution_components = []
    source_stats = cache[("personal", "head", False, 8)][0]
    shared_stats = cache[("shared", "head", False, 8)][0]
    for target in TARGETS:
        for ref in REFERENCES:
            delta_target = (source_stats[target]["y"]-shared_stats[target]["y"]).sum(axis=0) * COEFFICIENTS[:, None]
            ratio = source_stats[target]["n"] / source_stats[ref]["n"]
            delta_reference = (ratio[:, None, :] * (source_stats[ref]["y"]-shared_stats[ref]["y"])).sum(axis=0) * COEFFICIENTS[:, None]
            for k, name in enumerate(COMPONENTS):
                attribution_components.append(dict(target=target, reference=ref, component=name,
                                                    target_dollar_change=float(delta_target[k, 0]),
                                                    reference_benchmark_change=float(delta_reference[k, 0]),
                                                    gap_change=float(delta_target[k, 0]-delta_reference[k, 0])))
    pd.DataFrame(attribution_components).to_csv(out / "fixed_budget_gap_decomposition.csv", index=False)
    # The observed union must equal the sum of the three disjoint target totals.
    for label in scenarios:
        total = sum(rep_saved[f"{label}|{g}|absolute_total"] for g in TARGETS[:3])
        if not np.allclose(total, rep_saved[f"{label}|{TARGETS[-1]}|absolute_total"], atol=.02, rtol=1e-10):
            raise ValueError("Combined target absolute total mismatch")
        for ref in REFERENCES:
            total = sum(rep_saved[f"{label}|{g}|{ref}|age_band"] for g in TARGETS[:3])
            if not np.allclose(total, rep_saved[f"{label}|{TARGETS[-1]}|{ref}|age_band"], atol=.02, rtol=1e-10):
                raise ValueError("Combined target benchmark gap mismatch")
    old_path = FISCAL / "aggregate_audit_2026_09_17/derived/audit.json"
    if not old_path.exists():
        raise ValueError("Independent full-weight baseline audit is required")
    old = json.loads(old_path.read_text())["totals"]
    base = table[table.scenario.eq("baseline") & table.target.eq(TARGETS[-1])]
    observed = float(base.loc[base.metric.eq("absolute_total"), "estimate"].iloc[0])
    rounding_difference = observed - old["absolute_balance"]
    if abs(rounding_difference) > 1e6:
        raise ValueError(f"Baseline differs beyond main-weight rounding: {rounding_difference}")
    audit["checks"]["baseline_absolute_rounding_difference"] = rounding_difference
    for ref, key in [("third_plus_nh_white", "gap_white_balance"), ("all_native", "gap_native_balance")]:
        new = float(base.loc[base.metric.eq("gap_total") & base.reference.eq(ref) & base.matching.eq("age_band"), "estimate"].iloc[0])
        if abs(new-old[key]) > 1e6:
            raise ValueError("Baseline reference gap failed independent audit anchor")
        audit["checks"][f"baseline_{ref}_rounding_difference"] = new-old[key]
    table.to_csv(out / "estimates.csv", index=False)
    pd.DataFrame(comp_rows).to_csv(out / "component_gaps.csv", index=False)
    pd.DataFrame(band_rows).to_csv(out / "age_profiles.csv", index=False)
    np.savez_compressed(out / "replicates.npz", **rep_saved)
    (out / "audit.json").write_text(json.dumps(audit, indent=2, allow_nan=False) + "\n")
    print(table[table.target.eq(TARGETS[-1]) & (table.metric.eq("absolute_total") | (table.metric.eq("gap_total") & table.matching.eq("age_band")))][["scenario", "reference", "metric", "estimate", "se_joint"]].to_string(index=False))
    print(f"PASS: {len(table)} estimates; all scenario identities and audit anchors passed")


if __name__ == "__main__":
    generate()
