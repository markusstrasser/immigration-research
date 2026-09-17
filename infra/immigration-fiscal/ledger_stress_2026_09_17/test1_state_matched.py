"""Test 1: within-state matched and standardized gaps.

Joint cells are state_group x age band (32 cells). The same estimator, weights,
donor model and coefficients as the source lane are reused; only the cell
definition changes. A collapse to a single state group must reproduce the
stored 8-band results exactly.
"""
import json

import numpy as np
import pandas as pd

import common
from common import (COEFFICIENTS, HERE, REFERENCES, SOURCE_LANE, TARGETS, account,
                    contrast, standardized_gap, sufficient, sum_cells, summarize)

SCENARIOS = {"all_age_shared": "shared", "personal_sources": "personal"}
GROUP_ORDER = TARGETS[:3] + ["all_native", "third_plus_nh_white"]
STORED = SOURCE_LANE / "derived/estimates.csv"


def build_stats(matrix, health, weights, groups, cellcodes, count):
    stats = sufficient(matrix, health, weights, groups, cellcodes, count,
                       population_weights=weights, health_weights=weights)
    stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
    return stats


def shares_from(mask, weights, cellcodes, count):
    totals = np.bincount(cellcodes[mask], weights=weights[mask, 0], minlength=count)
    return totals / totals.sum()


def cell_population_floor(groups, weights, cellcodes, count):
    """Minimum population over groups x cells x all 161 weight vectors."""
    report = {}
    for name, mask in groups.items():
        worst = np.inf
        for c in range(count):
            sel = np.asarray(mask) & (cellcodes == c)
            n = weights[sel].sum(axis=0) if sel.any() else np.zeros(161)
            worst = min(worst, float(n.min()))
        report[name] = worst
    return report


def main():
    env = common.setup()
    d, weights, health, means, cov = (env["d"], env["weights"], env["health"],
                                      env["means"], env["covariance"])
    groups, bands = env["groups"], env["bands"]
    codes = common.state_codes(d)
    joint = codes * 8 + bands
    stored = pd.read_csv(STORED)
    audit = dict(inputs=common.audit_inputs(), gates={})

    # Gate 1 diagnostics before the estimator's own positivity check.
    floors = {}
    for scenario_groups, label, cellcodes, count in [(groups, "state_x_age", joint, 32)]:
        floors[label] = cell_population_floor(
            {g: scenario_groups[g] for g in GROUP_ORDER}, weights, cellcodes, count)
    print("[gate1] min group x cell population over 161 vectors:", json.dumps(floors, indent=2))
    audit["gates"]["cell_population_floor"] = floors
    if min(floors["state_x_age"].values()) <= 0:
        raise ValueError(f"Nonpositive 32-cell population: {floors}")

    # state_populations.csv: full-weight population by group x state group.
    pop_rows = []
    for name in GROUP_ORDER + [TARGETS[-1]]:
        mask = groups[name] if name in groups else env["member_count"] > 0
        for s, sname in enumerate(common.STATE_GROUP_NAMES):
            sel = np.asarray(mask) & (codes == s)
            pop_rows.append(dict(group=name, state_group=sname,
                                 records=int(sel.sum()),
                                 population=float(weights[sel, 0].sum()),
                                 min_cell_population_full_weight=float(min(
                                     weights[np.asarray(mask) & (joint == s * 8 + b), 0].sum()
                                     for b in range(8)))))
    pd.DataFrame(pop_rows).to_csv(HERE / "derived/state_populations.csv", index=False)

    rows = []
    collapse_checks, self_ref = {}, {}
    for scenario, allocation in SCENARIOS.items():
        matrix = env[allocation]
        stats32 = build_stats(matrix, health, weights, groups, joint, 32)
        white_shares32 = shares_from(groups[REFERENCES[0]], weights, joint, 32)
        for target in TARGETS:
            cell = stats32[target]
            n = cell["n"].sum(axis=0)
            for reference in REFERENCES[:2]:
                ref = stats32[reference]
                v, grad = contrast(cell, ref, COEFFICIENTS, means, True)
                for metric, vec, gradient in [("gap_total", v, grad),
                                              ("gap_per_person", v / n, grad / n[0])]:
                    rows.append(dict(scenario=scenario, target=target, reference=reference,
                                     cells="state_x_age", metric=metric, population=float(n[0]),
                                     **summarize(vec, gradient, cov)))
                std, qs = standardized_gap(cell, ref, COEFFICIENTS, means, white_shares32)
                rows.append(dict(scenario=scenario, target=target, reference=reference,
                                 cells="state_x_age", metric="standardized_gap_per_person",
                                 population=float(n[0]), **summarize(std, qs, cov)))
        # Gate 3: self-reference on the 32 cells.
        z, qz = contrast(stats32[REFERENCES[0]], stats32[REFERENCES[0]], COEFFICIENTS, means)
        self_ref[scenario] = dict(max_abs_gap=float(np.max(np.abs(z))),
                                  max_abs_gradient=float(np.max(np.abs(qz))))
        if np.max(np.abs(z)) > .01 or np.max(np.abs(qz)) > 1e-5:
            raise ValueError("Self-reference does not cancel on 32 cells")

        # Single-state restrictions: 8 age bands inside one state.
        for s, sname in [(0, "CA"), (1, "TX")]:
            sub = {g: np.asarray(m) & (codes == s) for g, m in groups.items()}
            stats8 = build_stats(matrix, health, weights, sub, bands, 8)
            sub_shares = shares_from(sub[REFERENCES[0]], weights, bands, 8)
            for target in TARGETS:
                cell = stats8[target]
                n = cell["n"].sum(axis=0)
                for reference in REFERENCES[:2]:
                    std, qs = standardized_gap(cell, stats8[reference], COEFFICIENTS, means, sub_shares)
                    rows.append(dict(scenario=scenario, target=target, reference=reference,
                                     cells=f"{sname}_age", metric="standardized_gap_per_person",
                                     population=float(n[0]), **summarize(std, qs, cov)))
                    v, grad = contrast(cell, stats8[reference], COEFFICIENTS, means, True)
                    for metric, vec, gradient in [("gap_total", v, grad),
                                                  ("gap_per_person", v / n, grad / n[0])]:
                        rows.append(dict(scenario=scenario, target=target, reference=reference,
                                         cells=f"{sname}_age", metric=metric, population=float(n[0]),
                                         **summarize(vec, gradient, cov)))

        # Gate 2: collapse to one state group -> the stored 8-band results.
        one = np.zeros(len(d), dtype=int) * 8 + bands
        statsc = build_stats(matrix, health, weights, groups, one, 8)
        cshares = shares_from(groups[REFERENCES[0]], weights, one, 8)
        residuals = {}
        for reference in REFERENCES[:2]:
            v, _ = contrast(statsc[TARGETS[-1]], statsc[reference], COEFFICIENTS, means, True)
            want = stored[stored.scenario.eq(scenario) & stored.target.eq(TARGETS[-1])
                          & stored.reference.eq(reference) & stored.matching.eq("age_band")
                          & stored.metric.eq("gap_total")].estimate
            if len(want) != 1:
                raise ValueError(f"Missing stored anchor: {scenario}/{reference}/gap_total")
            residuals[f"gap_total|{reference}"] = float(abs(v[0] - want.iloc[0]))
            for target in TARGETS:
                std, _ = standardized_gap(statsc[target], statsc[reference], COEFFICIENTS, means, cshares)
                w2 = stored[stored.scenario.eq(scenario) & stored.target.eq(target)
                            & stored.reference.eq(reference)
                            & stored.metric.eq("standardized_gap_per_person")].estimate
                if len(w2) != 1:
                    raise ValueError(f"Missing stored anchor: {scenario}/{target}/{reference}/std")
                residuals[f"std|{target}|{reference}"] = float(abs(std[0] - w2.iloc[0]))
        collapse_checks[scenario] = residuals
        bad = [k for k, v in residuals.items() if (v > 1.0 if k.startswith("gap_total") else v > 1e-3)]
        if bad:
            raise ValueError(f"Collapse check failed for {scenario}: {bad} {residuals}")

    table = pd.DataFrame(rows)
    table.to_csv(HERE / "derived/state_matched.csv", index=False)
    audit["gates"]["collapse_to_single_state"] = collapse_checks
    audit["gates"]["self_reference_32_cells"] = self_ref
    audit["gates"]["tolerances"] = dict(gap_total_dollars=1.0, standardized_dollars=1e-3,
                                        self_reference_gap=.01, self_reference_gradient=1e-5)
    audit["rows"] = len(table)
    (HERE / "derived/audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(table[table.cells.eq("state_x_age") & table.metric.eq("standardized_gap_per_person")]
          [["scenario", "target", "reference", "estimate", "se_joint"]].to_string(index=False))
    print(f"PASS: {len(table)} rows; gates 1-3 passed")


if __name__ == "__main__":
    main()
