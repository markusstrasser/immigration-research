"""Declared item-11 allocation diagnostic, not a nonlinear household rerun.

The case assigns its generation-level mixed-unit totals per member in the
household kernel. This module exposes exactly that rule and a whole-component
allocation sensitivity. Net component totals do not bound gross household
effects: the sensitivity must never be described as a conservative bound.
"""
from __future__ import annotations

import numpy as np

GENERATION_NAMES = ("G1", "G2", "G3plus")


def _require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] mixed allocation diagnostic: " + message)


def item10_flags(data, corrections):
    """Identify completion reporters/nonreporters by the source person keys.

    This is a diagnostic mask only. Nonreporting children remain lineage
    members when a Mexican-report classification weight is recalibrated;
    their membership cannot be inferred by applying their parent's factor.
    """
    ids = list(zip(data["person_ph_seq"].tolist(), data["person_pppos"].tolist()))
    _require(len(set(ids)) == len(ids), "duplicate pricing person identity")
    positions = {tuple(map(int, identity)): i for i, identity in enumerate(ids)}
    reporter = np.zeros(len(ids), dtype=bool)
    nonreporter = np.zeros(len(ids), dtype=bool)
    records = corrections["meta"]["union_completion"]["observed_records"]
    for record in records:
        key = (int(record["PH_SEQ"]), int(record["PPPOS"]))
        _require(key in positions, "item10 person missing from pricing cache")
        target = nonreporter if record["observed_nonreporter"] else reporter
        target[positions[key]] = True
    _require(not (reporter & nonreporter).any(), "completion populations overlap")
    return {"reporter": reporter, "nonreporter": nonreporter}


def mixed_allocation(data, audit, factors, affected=None):
    """Evaluate item11's declared per-member rule under person reweighting.

    ``factors`` is one factor per pricing person, or a person x 161 matrix.
    ``affected`` optionally marks persons subject to a changed classification;
    by default it means a central factor differs from one. Inputs are not
    mutated. Dollar units are billions and signs follow net fiscal cost.

    The whole-component sensitivity asks what happens if between none and
    all of each affected generation's *net* item11 component changes. It is
    an arbitrary allocation stress, not a statistical interval or a bound
    on taxes, benefits or claimants after changed membership.
    """
    weights = np.asarray(data["weights"], dtype=float)
    added = np.asarray(data["added_weights"], dtype=float)
    _require(weights.shape == added.shape and weights.ndim == 2,
             "identified/added weight shape")
    factor = np.asarray(factors, dtype=float)
    if factor.ndim == 1:
        factor = factor[:, None]
    _require(factor.shape in ((len(weights), 1), weights.shape), "factor shape")
    _require(np.isfinite(factor).all() and (factor >= 0).all(), "invalid factors")
    old = weights + added
    difference = old * (factor - 1.0)
    active = factor[:, 0] != 1 if affected is None else np.asarray(affected, dtype=bool)
    _require(active.shape == (len(weights),), "affected-person shape")
    generation = np.asarray(data["generation"])
    prices = np.asarray(data["base_piece_prices"])
    pieces = audit["denominator_pieces"]
    _require(prices.shape == (len(pieces), len(weights)), "price-piece shape")
    by_end = {}
    for end in ("low", "high"):
        components = []
        total_delta = np.zeros(weights.shape[1])
        for gi, name in enumerate(GENERATION_NAMES):
            indices = [i for i, part in enumerate(pieces)
                       if part["end"] == end and part["generation"] == name
                       and part["line"] == "mixed_unit_removal"]
            _require(len(indices) == 1, "expected one mixed piece per generation/end")
            i = indices[0]
            _require(pieces[i]["economic_class"] == "unclassified_post_engine",
                     "mixed piece economic class changed")
            baseline = float(prices[i] @ old[:, 0])
            delta = prices[i] @ difference
            total_delta += delta
            has_affected = bool((active & (generation == gi)).any())
            whole = -baseline if has_affected else 0.0
            components.append({
                "generation": name,
                "baseline_item11_bn": baseline,
                "affected_before_people": float(old[active & (generation == gi), 0].sum()),
                "declared_per_member_delta_bn": float(delta[0]),
                "declared_per_member_replicates_bn": delta.tolist(),
                "whole_net_component_allocation_sensitivity_delta_bn":
                    [min(0.0, whole), max(0.0, whole)],
            })
        sensitivity = [sum(v["whole_net_component_allocation_sensitivity_delta_bn"][j]
                           for v in components) for j in (0, 1)]
        by_end[end] = {"by_generation": components,
                       "declared_per_member_delta_bn": float(total_delta[0]),
                       "declared_per_member_replicates_bn": total_delta.tolist(),
                       "whole_net_component_allocation_sensitivity_delta_bn": sensitivity}
    return {
        "rule": "existing generation-total per-member distribution in households.py:1143-1151",
        "nonlinear_membership_interaction_measured": False,
        "sensitivity_is_rigorous_bound": False,
        "limitation": "Net generation totals can cancel gross household effects. Changed child membership requires a declared household configuration mixture and new survivor tax/benefit solves.",
        "by_end": by_end,
    }
