# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb", "numpy", "pandas"]
# ///
"""Compare generated ACS profiles without rerunning raw-data processing.

Native-First: NumPy arithmetic on saved full/replicate estimates; JSON/CSV outputs.
Within-year differences retain survey covariance. Between-year uncertainty assumes
independent 2019/2024 samples; this is a descriptive comparison, not a policy effect.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_arrival_cohorts import sdr_estimate


def metric_units(metric: str) -> str:
    if "dollars" in metric:
        return "2024 dollars"
    return "share" if "share" in metric or metric == "employment_population" else "years"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", required=True, type=Path)
    parser.add_argument("--inflation", required=True, type=Path)
    args = parser.parse_args()
    root = args.analysis
    inflation = json.loads(args.inflation.read_text())
    reps = {year: {k: np.array(v) for k, v in json.loads(
        (root / f"replicate_estimates_{year}.json").read_text()).items()}
        for year in (2019, 2023, 2024)}
    universe = "civilian_noninstitutional_25_64"
    factor = inflation["factors"]["2019_to_2024"]["factor"]

    def vector(year, group, metric, selected_universe=universe):
        result = reps[year][f"{group}|{selected_universe}|{metric}"]
        return result * (factor if year == 2019 and "dollars" in metric else 1)

    checks = []
    for year in (2019, 2024):
        manifest = json.loads((root / f"manifest_{year}.json").read_text())
        official = inflation["calibration"][str(year)]
        assert manifest["smoke_nrows_per_part"] is None, "Cannot summarize a smoke as national data"
        assert manifest["rows_read"] == official["official_national_person_records"]
        population = vector(year, "native", "population", "all_ages") + vector(
            year, "foreign_born/stock", "population", "all_ages")
        computed = sdr_estimate(population)
        anchor = official["anchors"]["Total population"]
        assert computed["estimate"] == anchor["estimate"]
        assert abs(computed["acs_sdr_se"] - anchor["sdr_se_published_rounded"]) <= 0.5
        checks.append({"year": year, "check": "official PUMS records, population and rounded SDR SE", **computed})

    metrics = ["employment_population", "earnings_mean_survey_dollars", "less_than_hs_share",
               "ba_plus_share", "limited_english_share", "male_share", "mean_age"]
    groups = ["native", "foreign_born/entry_0_3", "foreign_born/entry_1_3",
              "mexico_born/entry_0_3", "mexico_born/entry_1_3", "mexico_born/stock",
              "somalia_born/stock"]
    comparisons, gaps = [], []
    for group in groups:
        for metric in metrics:
            before, after = vector(2019, group, metric), vector(2024, group, metric)
            b, a = sdr_estimate(before), sdr_estimate(after)
            delta, se = a["estimate"] - b["estimate"], np.hypot(a["acs_sdr_se"], b["acs_sdr_se"])
            comparisons.append({"group": group, "metric": metric, "units": metric_units(metric),
                "estimate_2019": b["estimate"], "estimate_2024": a["estimate"],
                "difference_2024_minus_2019": delta, "se_assuming_cross_year_independence": se,
                "ci95_low": delta - 1.96 * se, "ci95_high": delta + 1.96 * se})
            if group != "native":
                native_gap = {y: vector(y, group, metric) - vector(y, "native", metric)
                              for y in (2019, 2024)}
                for year, estimates in native_gap.items():
                    gaps.append({"year": year, "group": group, "metric": metric,
                                 "units": metric_units(metric),
                                 "definition": "group minus native, same survey", **sdr_estimate(estimates)})

    fiscal = pd.read_csv(root / "fiscal_comparison_2023.csv")
    fiscal_gaps = []
    for selected_universe in fiscal.universe.unique():
        f = fiscal[fiscal.universe.eq(selected_universe)]
        for comparator in ("native", "native_nhwhite"):
            table = f.pivot(index="group", columns="metric", values="estimate")
            native = table.loc[comparator]
            mexico = table.loc["mexico_born/stock"]
            partial_gap = native.projected_partial_balance - mexico.projected_partial_balance
            direct_gap = vector(2023, comparator, "direct_acs_employee_payroll", selected_universe) - vector(
                2023, "mexico_born/stock", "direct_acs_employee_payroll", selected_universe)
            fiscal_gaps.append({"universe": selected_universe, "comparator": comparator,
                "native_partial_balance": native.projected_partial_balance,
                "mexico_partial_balance": mexico.projected_partial_balance,
                "projected_payroll_gap": native.projected_employee_payroll - mexico.projected_employee_payroll,
                "projected_transfer_gap_native_minus_mexico": native.projected_selected_transfers - mexico.projected_selected_transfers,
                "projected_partial_gap": partial_gap,
                "partial_ratio": native.projected_partial_balance / mexico.projected_partial_balance,
                "omitted_net_contribution_advantage_mexico_needed_to_reverse_ranking": partial_gap,
                "direct_payroll_gap": sdr_estimate(direct_gap)})
    pd.DataFrame(comparisons).to_csv(root / "cohort_comparison.csv", index=False)
    pd.DataFrame(gaps).to_csv(root / "within_year_native_gaps.csv", index=False)
    somali_share = vector(2024, "somalia_born/entry_0_3", "population") / vector(
        2024, "foreign_born/entry_0_3", "population")
    summary = {"checks": checks, "fiscal_gaps": fiscal_gaps,
               "somalia_born_share_of_recent_cni_adults": sdr_estimate(somali_share),
               "max_direct_recent_epop_composition_swing_pp_at_fixed_share": float(100 * somali_share[0]),
               "inflation_factor_2019_to_2024": factor,
               "limitations": ["ACS survey intervals exclude nonresponse, coverage and transport error",
                 "Partial fiscal model has no total uncertainty interval or full-government ledger",
                 "Between-year SE assumes independence; before/after is not causal attribution",
                 "No age/sex standardization here; see separate fixed-weight sensitivity"]}
    (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
