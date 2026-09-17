"""Metro-level matched fiscal gaps for the all-age Mexican-origin account.

Three standards at a common 4-band age resolution (0-17, 18-44, 45-64, 65+):
age only, state group x age, and metro group x age. Same estimator, weights,
donor model, coefficients and reporting domain as the source lane; only the
cell definition changes. Nothing outside this lane directory is written.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import geo  # noqa: E402
import common  # noqa: E402
from common import (COEFFICIENTS, REFERENCES, SOURCE_LANE, TARGETS, contrast,
                    standardized_gap, sufficient, sum_cells, summarize)

SCENARIOS = {"all_age_shared": "shared", "personal_sources": "personal"}
GROUP_ORDER = TARGETS[:3] + ["all_native", "third_plus_nh_white"]
KEY_GROUPS = TARGETS[:3] + REFERENCES[:2]
PAIRS = [(TARGETS[1], TARGETS[0]), (TARGETS[2], TARGETS[1]), (TARGETS[2], TARGETS[0])]
SINGLE_METROS = ["los_angeles", "riverside", "houston", "dallas", "chicago", "phoenix"]
STORED = SOURCE_LANE / "derived/estimates.csv"
OUT = HERE / "derived"


def build_stats(matrix, health, weights, groups, cellcodes, count):
    stats = sufficient(matrix, health, weights, groups, cellcodes, count,
                       population_weights=weights, health_weights=weights)
    stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
    return stats


def shares_from(mask, weights, cellcodes, count):
    totals = np.bincount(cellcodes[np.asarray(mask)],
                         weights=weights[np.asarray(mask), 0], minlength=count)
    return totals / totals.sum()


def cell_report(groups, weights, cellcodes, count):
    """Minimum population over all 161 weight vectors and minimum record count."""
    out = {}
    for name in KEY_GROUPS:
        mask = np.asarray(groups[name])
        worst_pop, worst_rec = np.inf, np.inf
        for c in range(count):
            sel = mask & (cellcodes == c)
            n = weights[sel].sum(axis=0) if sel.any() else np.zeros(weights.shape[1])
            worst_pop = min(worst_pop, float(n.min()))
            worst_rec = min(worst_rec, int(sel.sum()))
        out[name] = dict(min_population_over_161=worst_pop, min_records=int(worst_rec))
    return out


def emit(rows, scenario, standard, target, reference, stats, shares, cov, means):
    cell = stats[target]
    n = cell["n"].sum(axis=0)
    ref = stats[reference]
    v, grad = contrast(cell, ref, COEFFICIENTS, means, True)
    for metric, vec, gradient in [("gap_total", v, grad), ("gap_per_person", v / n, grad / n[0])]:
        rows.append(dict(scenario=scenario, cells=standard, target=target, reference=reference,
                         metric=metric, population=float(n[0]), **summarize(vec, gradient, cov)))
    std, qs = standardized_gap(cell, ref, COEFFICIENTS, means, shares)
    rows.append(dict(scenario=scenario, cells=standard, target=target, reference=reference,
                     metric="standardized_gap_per_person", population=float(n[0]),
                     **summarize(std, qs, cov)))
    return std, qs


def main():
    OUT.mkdir(exist_ok=True)
    env = common.setup()
    d, weights, health, means, cov = (env["d"], env["weights"], env["health"],
                                      env["means"], env["covariance"])
    groups = {g: env["groups"][g] for g in KEY_GROUPS}
    bands8 = env["bands"]
    bands = geo.bands4(d)
    if set(np.unique(bands)) != {0, 1, 2, 3}:
        raise ValueError("4-band age standard is not fully populated")
    raw, cbsa = geo.raw_codes(d)
    audit = dict(inputs=common.audit_inputs() + [
        dict(path=str(p), sha256=common.ext.base.sha(p))
        for p in [HERE / "geo.py", HERE / "metro_tests.py"]], gates={}, notes={})
    audit["notes"]["identified_metro_record_share"] = float((cbsa > 0).mean())

    # ---- geography: merge sparse metro groups upward -----------------------
    # Primary rule is the brief's gate: every key group x cell positive in all
    # 161 weight vectors. A stricter 5-sample-record floor is carried as a
    # robustness arm because a few retained cells rest on 1-4 CPS records.
    alive, codes, merges = geo.resolve_groups(raw, bands, groups, weights, KEY_GROUPS,
                                              record_floor=1)
    alive5, codes5, merges5 = geo.resolve_groups(raw, bands, groups, weights, KEY_GROUPS,
                                                 record_floor=geo.RECORD_FLOOR)
    n_metro = len(alive)
    joint = codes * 4 + bands
    joint5 = codes5 * 4 + bands
    audit["gates"]["metro_groups"] = dict(
        defined=geo.NAMES,
        primary=dict(rule="positive population in all 161 weight vectors",
                     retained=alive, merges=merges),
        robustness=dict(rule=f"positivity plus >={geo.RECORD_FLOOR} sample records per cell",
                        retained=alive5, merges=merges5))
    print(f"[geo] {len(geo.NAMES)} defined -> {n_metro} retained "
          f"(merged: {[m['merged'] for m in merges] or 'none'}); "
          f"robustness arm retains {len(alive5)}")

    # ---- populations table (raw rules and retained groups) -----------------
    pop_rows = []
    for stage, assign, names in [("as_defined", raw, geo.NAMES), ("retained", codes, alive)]:
        for k, mname in enumerate(names):
            for gname in GROUP_ORDER + [TARGETS[-1]]:
                mask = (np.asarray(groups[gname]) if gname in groups
                        else np.asarray(sum(groups[t].astype(int) for t in TARGETS[:3]) > 0))
                sel = mask & (assign == k)
                cells = [mask & (assign == k) & (bands == b) for b in range(4)]
                pops = [weights[c].sum(axis=0) if c.any() else np.zeros(161) for c in cells]
                pop_rows.append(dict(
                    stage=stage, metro_group=mname, state_group=geo.state_group_of(mname),
                    group=gname, records=int(sel.sum()), population=float(weights[sel, 0].sum()),
                    min_cell_records=int(min(int(c.sum()) for c in cells)),
                    min_cell_population_full_weight=float(min(p[0] for p in pops)),
                    min_cell_population_over_161=float(min(p.min() for p in pops))))
    pd.DataFrame(pop_rows).to_csv(OUT / "metro_populations.csv", index=False)

    # ---- gate (a): cell floors under each standard -------------------------
    state_joint = common.state_codes(d) * 4 + bands
    STANDARDS = [("age_4", bands, 4), ("state_x_age_4", state_joint, 16),
                 ("metro_x_age_4", joint, n_metro * 4),
                 ("metro_x_age_4_rf5", joint5, len(alive5) * 4)]
    floors = {label: cell_report(groups, weights, cc, n) for label, cc, n in STANDARDS}
    audit["gates"]["cell_floors"] = floors
    for label, rep in floors.items():
        if min(v["min_population_over_161"] for v in rep.values()) <= 0:
            raise ValueError(f"Nonpositive cell population under {label}: {rep}")
    print("[gate a]", json.dumps(floors["metro_x_age_4"], indent=1))

    rows, contrast_rows = [], []
    collapse, self_ref, union_totals = {}, {}, {}
    for scenario, allocation in SCENARIOS.items():
        matrix = env[allocation]

        # ---- the three standards at 4 bands ------------------------------
        for label, cellcodes, count in STANDARDS:
            stats = build_stats(matrix, health, weights, groups, cellcodes, count)
            shares = shares_from(groups[REFERENCES[0]], weights, cellcodes, count)
            std = {}
            for target in TARGETS:
                for reference in REFERENCES[:2]:
                    value, grad = emit(rows, scenario, label, target, reference,
                                       stats, shares, cov, means)
                    if reference == REFERENCES[0]:
                        std[target] = (value, grad)
            for later, earlier in PAIRS:
                v = std[later][0] - std[earlier][0]
                q = std[later][1] - std[earlier][1]
                contrast_rows.append(dict(scenario=scenario, standard=label, later=later,
                                          earlier=earlier, reference=REFERENCES[0],
                                          **summarize(v, q, cov)))
            if label == "age_4":
                u, _ = contrast(stats[TARGETS[-1]], stats[REFERENCES[0]], COEFFICIENTS, means, True)
                u2, _ = contrast(stats[TARGETS[-1]], stats[REFERENCES[1]], COEFFICIENTS, means, True)
                union_totals[scenario] = {REFERENCES[0]: float(u[0]), REFERENCES[1]: float(u2[0])}
            if label == "metro_x_age_4":
                z, qz = contrast(stats[REFERENCES[0]], stats[REFERENCES[0]], COEFFICIENTS, means)
                self_ref[scenario] = dict(max_abs_gap=float(np.max(np.abs(z))),
                                          max_abs_gradient=float(np.max(np.abs(qz))))
                if np.max(np.abs(z)) > .01 or np.max(np.abs(qz)) > 1e-5:
                    raise ValueError("Self-reference does not cancel on the metro cells")

        # ---- single-metro restrictions, own white age shares --------------
        for mname in SINGLE_METROS:
            if mname not in alive:
                continue
            a = alive.index(mname)
            sub = {g: np.asarray(m) & (codes == a) for g, m in groups.items()}
            stats = build_stats(matrix, health, weights, sub, bands, 4)
            shares = shares_from(sub[REFERENCES[0]], weights, bands, 4)
            for target in TARGETS:
                for reference in REFERENCES[:2]:
                    emit(rows, scenario, f"{mname}_age_4", target, reference,
                         stats, shares, cov, means)

        # ---- gate (b): collapse to one geography group, ORIGINAL 8 bands --
        stored = pd.read_csv(STORED)
        one = np.zeros(len(d), dtype=int) * 8 + bands8
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
            audit["notes"].setdefault("stored_8band_union_gap_total", {}).setdefault(
                scenario, {})[reference] = float(want.iloc[0])
            for target in TARGETS:
                std, _ = standardized_gap(statsc[target], statsc[reference], COEFFICIENTS,
                                          means, cshares)
                w2 = stored[stored.scenario.eq(scenario) & stored.target.eq(target)
                            & stored.reference.eq(reference)
                            & stored.metric.eq("standardized_gap_per_person")].estimate
                if len(w2) != 1:
                    raise ValueError(f"Missing stored anchor: {scenario}/{target}/{reference}/std")
                residuals[f"std|{target}|{reference}"] = float(abs(std[0] - w2.iloc[0]))
        collapse[scenario] = residuals
        bad = [k for k, v in residuals.items()
               if (v > 1.0 if k.startswith("gap_total") else v > 1e-3)]
        if bad:
            raise ValueError(f"Collapse check failed for {scenario}: {bad} {residuals}")

    # ---- (d) 4-band vs 8-band age-only union total: reported, not gated ----
    band_shift = {}
    for scenario, byref in union_totals.items():
        band_shift[scenario] = {
            ref: dict(age_4=byref[ref],
                      age_8=audit["notes"]["stored_8band_union_gap_total"][scenario][ref],
                      difference=byref[ref] - audit["notes"]["stored_8band_union_gap_total"][scenario][ref])
            for ref in byref}
    audit["gates"]["age_band_resolution_shift"] = dict(
        values=band_shift,
        gated=False,
        explanation=("A matched gap_total re-weights the reference inside every cell by the "
                     "target's own cell population, so it is only invariant to refining the "
                     "partition when the reference's per-person balance is constant inside each "
                     "coarse cell. It is not, so the 4-band and 8-band age-only totals differ; "
                     "the difference is the within-coarse-band age composition the 4-band "
                     "standard cannot see."))

    table = pd.DataFrame(rows)
    table.to_csv(OUT / "metro_matched.csv", index=False)
    contrasts = pd.DataFrame(contrast_rows)
    contrasts.to_csv(OUT / "metro_generation_contrasts.csv", index=False)
    audit["gates"]["collapse_to_single_geography_8_bands"] = collapse
    audit["gates"]["self_reference_metro_cells"] = self_ref
    audit["gates"]["tolerances"] = dict(gap_total_dollars=1.0, standardized_dollars=1e-3,
                                        self_reference_gap=.01, self_reference_gradient=1e-5)
    audit["rows"] = dict(metro_matched=len(table), metro_generation_contrasts=len(contrasts),
                         metro_populations=len(pop_rows))
    (OUT / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")

    show = table[table.metric.eq("standardized_gap_per_person")
                 & table.cells.isin([s[0] for s in STANDARDS])]
    print(show[["scenario", "cells", "target", "reference", "estimate",
                "ci95_low", "ci95_high"]].round(0).to_string(index=False))
    print(contrasts[["scenario", "standard", "later", "earlier", "estimate",
                     "ci95_low", "ci95_high"]].round(0).to_string(index=False))
    print(f"PASS: {len(table)} matched rows, {len(contrasts)} contrast rows; gates a-c passed")


if __name__ == "__main__":
    main()
