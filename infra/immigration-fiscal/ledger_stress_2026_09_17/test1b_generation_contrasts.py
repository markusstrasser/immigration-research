"""Paired generation contrasts under the joint state x age standard.

The essay's "cross-sectional narrowing" claim rests on later-minus-earlier
common-age contrasts. RESULT.md reports that the 32-cell standard shrinks the
third-plus-minus-first difference; this computes the paired replicate intervals
for that difference, retaining donor covariance, for both scenarios and both
standards, so the two can be compared on equal footing.
"""
import numpy as np
import pandas as pd

import common
from common import COEFFICIENTS, HERE, REFERENCES, TARGETS, standardized_gap, sufficient, sum_cells, summarize

PAIRS = [(TARGETS[1], TARGETS[0]), (TARGETS[2], TARGETS[1]), (TARGETS[2], TARGETS[0])]


def main():
    env = common.setup()
    d, weights, health, means, cov = env["d"], env["weights"], env["health"], env["means"], env["covariance"]
    groups, bands = env["groups"], env["bands"]
    joint = common.state_codes(d) * 8 + bands
    rows = []
    for scenario, allocation in [("all_age_shared", "shared"), ("personal_sources", "personal")]:
        matrix = env[allocation]
        for label, cells, count in [("age_8", bands, 8), ("state_x_age_32", joint, 32)]:
            stats = sufficient(matrix, health, weights, groups, cells, count,
                               population_weights=weights, health_weights=weights)
            stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
            totals = np.bincount(cells[groups[REFERENCES[0]]], weights=weights[groups[REFERENCES[0]], 0], minlength=count)
            shares = totals / totals.sum()
            std = {t: standardized_gap(stats[t], stats[REFERENCES[0]], COEFFICIENTS, means, shares) for t in TARGETS[:3]}
            for later, earlier in PAIRS:
                v = std[later][0] - std[earlier][0]
                q = std[later][1] - std[earlier][1]
                rows.append(dict(scenario=scenario, standard=label, later=later, earlier=earlier,
                                 **summarize(v, q, cov)))
    table = pd.DataFrame(rows)
    table.to_csv(HERE / "derived/generation_contrasts_by_standard.csv", index=False)
    # Anchor: the 8-band contrasts must reproduce the source lane's stored file.
    stored = pd.read_csv(common.SOURCE_LANE / "derived/generation_contrasts.csv")
    worst = 0.0
    for _, r in table[table.standard.eq("age_8")].iterrows():
        s = stored[stored.scenario.eq(r.scenario) & stored.later.eq(r.later) & stored.earlier.eq(r.earlier)]
        if len(s) != 1:
            raise ValueError(f"Missing stored contrast {r.scenario}/{r.later}/{r.earlier}")
        worst = max(worst, abs(float(s.estimate.iloc[0]) - r.estimate), abs(float(s.se_joint.iloc[0]) - r.se_joint))
    if worst > 1e-3:
        raise ValueError(f"8-band contrasts do not reproduce stored file: max residual {worst}")
    print(table[["scenario", "standard", "later", "earlier", "estimate", "ci95_low", "ci95_high"]].round(0).to_string(index=False))
    print(f"PASS: 8-band contrasts reproduce stored generation_contrasts.csv (max residual {worst:.2e})")


if __name__ == "__main__":
    main()
