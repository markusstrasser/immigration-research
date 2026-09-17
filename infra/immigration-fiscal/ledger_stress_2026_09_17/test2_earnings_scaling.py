"""Test 2: earnings/tax measurement sensitivity for the Mexican-origin targets.

Employee taxes (component 0) and employer payroll (component 3) are multiplied by
(1+delta) on every record in the three target groups; references and all other
records are untouched. Every reported quantity is exactly linear in delta, so the
break-even delta* that zeroes a matched gap is read off the line and verified.
"""
import json

import numpy as np
import pandas as pd

import common
from common import (COEFFICIENTS, HERE, REFERENCES, TARGETS, account, contrast,
                    standardized_gap, sufficient, sum_cells, summarize)

DELTAS = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50]
SCALED = [0, 3]  # tax, employer payroll
FRED = HERE / "derived/fred_A576RC1.csv"


def stats_for(matrix, env, delta, target_mask):
    scaled = matrix.copy()
    if delta:
        scaled[np.ix_(target_mask, SCALED)] *= (1.0 + delta)
    stats = sufficient(scaled, env["health"], env["weights"], env["groups"],
                       env["bands"], 8, population_weights=env["weights"],
                       health_weights=env["weights"])
    stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
    return stats


def main():
    env = common.setup()
    weights, means, cov = env["weights"], env["means"], env["covariance"]
    groups = env["groups"]
    target_mask = np.zeros(len(env["d"]), bool)
    for g in TARGETS[:3]:
        target_mask |= np.asarray(groups[g])
    white_shares = np.bincount(env["bands"][groups[REFERENCES[0]]],
                               weights=weights[groups[REFERENCES[0]], 0], minlength=8)
    white_shares = white_shares / white_shares.sum()

    rows, points = [], {}
    for scenario, allocation in [("personal_sources", "personal"), ("all_age_shared", "shared")]:
        matrix = env[allocation]
        for delta in DELTAS:
            stats = stats_for(matrix, env, delta, target_mask)
            union = stats[TARGETS[-1]]
            n_union = union["n"].sum(axis=0)
            y = account(union, COEFFICIENTS, means).sum(axis=0)
            q = -union["h"][:, :, 0].sum(axis=0)
            rows.append(dict(scenario=scenario, delta=delta, target=TARGETS[-1], reference="",
                             metric="absolute_total", population=float(n_union[0]),
                             **summarize(y, q, cov)))
            points[(scenario, "absolute_total", TARGETS[-1], "")] = \
                points.get((scenario, "absolute_total", TARGETS[-1], ""), {}) | {delta: float(y[0])}
            for target in TARGETS:
                cell = stats[target]
                n = cell["n"].sum(axis=0)
                for reference in REFERENCES[:2]:
                    ref = stats[reference]
                    v, grad = contrast(cell, ref, COEFFICIENTS, means, True)
                    rows.append(dict(scenario=scenario, delta=delta, target=target,
                                     reference=reference, metric="gap_total",
                                     population=float(n[0]), **summarize(v, grad, cov)))
                    key = (scenario, "gap_total", target, reference)
                    points[key] = points.get(key, {}) | {delta: float(v[0])}
                    std, qs = standardized_gap(cell, ref, COEFFICIENTS, means, white_shares)
                    rows.append(dict(scenario=scenario, delta=delta, target=target,
                                     reference=reference, metric="standardized_gap_per_person",
                                     population=float(n[0]), **summarize(std, qs, cov)))
                    key = (scenario, "standardized_gap_per_person", target, reference)
                    points[key] = points.get(key, {}) | {delta: float(std[0])}

    # Linearity and break-even from the line through delta = 0 and delta = 0.50.
    linearity, breakeven = {}, []
    for (scenario, metric, target, reference), series in points.items():
        base, far = series[0.0], series[0.50]
        slope = (far - base) / 0.50
        worst = 0.0
        for probe in (0.10, 0.20):
            predicted = base + slope * probe
            scale = max(abs(series[probe]), abs(predicted), 1.0)
            worst = max(worst, abs(series[probe] - predicted) / scale)
        linearity[f"{scenario}|{metric}|{target}|{reference}"] = worst
        star = float("nan") if slope == 0 else -base / slope
        breakeven.append(dict(scenario=scenario, metric=metric, target=target,
                              reference=reference, value_at_delta0=base,
                              slope_per_unit_delta=slope, breakeven_delta=star,
                              max_relative_linearity_residual=worst))
        rows.append(dict(scenario=scenario, delta=float("nan"), target=target,
                         reference=reference, metric=f"{metric}__breakeven_delta",
                         population=float("nan"), estimate=star, se_cps=float("nan"),
                         se_meps=float("nan"), se_joint=float("nan"),
                         ci95_low=float("nan"), ci95_high=float("nan")))
    worst_linearity = max(linearity.values())
    if worst_linearity > 1e-6:
        raise ValueError(f"Nonlinear in delta: max relative residual {worst_linearity}")

    table = pd.DataFrame(rows)
    table.to_csv(HERE / "derived/earnings_scaling.csv", index=False)
    pd.DataFrame(breakeven).to_csv(HERE / "derived/breakeven.csv", index=False)

    # Context only: CPS aggregate wage and salary income vs the BEA/NIPA total.
    cps_wages = float((env["d"].WSAL_VAL.to_numpy() * weights[:, 0]).sum())
    context = dict(cps_wsal_val_full_weight_total_usd=cps_wages, fetch_date="2026-09-17")
    if FRED.exists():
        fred = pd.read_csv(FRED)
        fred["observation_date"] = pd.to_datetime(fred.observation_date)
        y2024 = fred[fred.observation_date.dt.year.eq(2024)]
        if len(y2024) != 12:
            raise ValueError(f"FRED A576RC1 returned {len(y2024)} months for 2024")
        bea = float(y2024.A576RC1.astype(float).mean()) * 1e9
        context.update(bea_wages_and_salaries_2024_usd=bea,
                       bea_series="FRED A576RC1, monthly SAAR billions, 2024 average",
                       cps_over_nipa_ratio=cps_wages / bea,
                       bea_source="https://fred.stlouisfed.org/graph/fredgraph.csv?id=A576RC1")
    else:
        context["bea_fetch"] = "FAILED — not substituted"

    audit = dict(inputs=common.audit_inputs(), deltas=DELTAS,
                 scaled_components=[common.COMPONENTS[k] for k in SCALED],
                 scaled_records=int(target_mask.sum()),
                 max_relative_linearity_residual=worst_linearity,
                 linearity_tolerance=1e-6, context=context, rows=len(table))
    (HERE / "derived/audit_test2.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(pd.DataFrame(breakeven)[lambda t: t.metric.eq("gap_total")]
          [["scenario", "target", "reference", "value_at_delta0", "breakeven_delta"]].to_string(index=False))
    print(json.dumps(context, indent=2))
    print(f"PASS: {len(table)} rows; linearity residual {worst_linearity:.3e}")


if __name__ == "__main__":
    main()
