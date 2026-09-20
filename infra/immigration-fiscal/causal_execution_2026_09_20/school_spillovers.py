"""Published-estimate arithmetic only; not raw causal replication or a meta-analysis."""
import json
import argparse
from pathlib import Path

CASES = [
    ("Florida_white_math_10pp_cumulative_exposure", .128, .107, .10, "pupil test-score SD", "published Table 5 column 5"),
    ("Hamburg_German_born_1pp_refugee_share_no_prep_offer", .27, .58, .01, "KERMIT test-score SD", "Table 10 panel B column 4; conditional on prep offer=0"),
    ("Denmark_any_refugee_arrival_Danish", -.010, .009, 1, "pupil test-score SD", "Table 3 panel A column 3 Grade x Refugee"),
    ("Denmark_any_refugee_arrival_math", -.010, .010, 1, "pupil test-score SD", "Table 3 panel B column 3 Grade x Refugee"),
    ("Italy_one_immigrant_replaces_native_language", -.0158, .0077, 1, "fraction of correct answers", "February 2018 author manuscript Table 2 column 1"),
    ("US_white_school_spending_cut_1000_2015_dollars", .0267, .00566, -1, "NAEP score SD", "Jackson-Wigger-Xiong 2021 Table 6 column 3; white, not native-born-only"),
]

def calculate():
    rows = []
    for name, beta, se, change, units, source in CASES:
        if se < 0 or change == 0:
            raise ValueError(name)
        effect = beta * change
        scaled_se = se * abs(change)
        rows.append({"name": name, "coefficient": beta, "standard_error": se,
                     "exposure_change": change, "effect": effect,
                     "approx_normal_95_ci": [effect - 1.96 * scaled_se, effect + 1.96 * scaled_se],
                     "units": units, "source_locator": source})
    dilution = []
    for response in (0, .5, 1):
        ratio = (1 + response * .10) / 1.10
        spending_change = 15000 * (ratio - 1)
        multiplier = spending_change / 1000
        dilution.append({
            "enrollment_growth": .10,
            "fraction_of_enrollment_growth_matched_by_funding_and_teachers": response,
            "spending_per_pupil_ratio": ratio,
            "pupil_teacher_ratio_change": 1 / ratio - 1,
            "illustrative_baseline_annual_spending_2018_dollars": 15000,
            "annual_per_pupil_spending_change_2018_dollars": spending_change,
            "assumed_duration_years": 4,
            "test_score_effect_at_meta_average": multiplier * .0316,
            "scaled_published_average_effect_95_ci": sorted([multiplier * .021, multiplier * .043]),
            "scaled_published_between_context_90_prediction_range": sorted([multiplier * -.004, multiplier * .067]),
            "status": "conditional illustration: assumed locally linear and reversible resource effect, equal pupil needs, same staffing response, and transport from US all-pupil spending studies; not an immigration estimate or native-white CI"
        })
    return {"status": "published-table arithmetic, not raw replication",
            "interval_method": "beta +/- 1.96*SE; marginal intervals, no multiplicity adjustment; identifying assumptions not priced",
            "estimates": rows,
            "resource_dilution_scenarios": dilution,
            "Germany_composition_illustration": {
                "immigrant_share_2012": .13, "immigrant_share_2022": .26,
                "math_gap_2022_points": 59,
                "mixture_change_holding_group_means_fixed": -(.26 - .13) * 59,
                "status": "noncausal composition arithmetic using rounded OECD country-note inputs; no CI"}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).parent / "derived/school_spillovers.json")
    target = parser.parse_args().out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(calculate(), indent=2) + "\n")
    print(target)
    for row in calculate()["estimates"]:
        print(row["name"], row["effect"], row["approx_normal_95_ci"], row["units"])
