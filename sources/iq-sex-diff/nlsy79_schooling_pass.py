#!/usr/bin/env python3
"""NLSY79 descriptive attenuation pass using the frozen pre-test schooling block."""

from __future__ import annotations

import csv
from pathlib import Path

from build_nlsy79_sibling_pairs import load_rows, to_int
from nlsy79_first_pass import (
    fit_ols,
    load_pairs,
    raw_subtest_surface,
    standardized_person_scores,
)


BASE_COVARIATES = [
    ("age_1981", "R0410500"),
    ("older_sibs_1979", "R0009300"),
]

SCHOOLING_BLOCK = [
    ("hs_grade_status_1981", "R0614900"),
    ("mother_hgc_1979", "R0006500"),
    ("father_hgc_1979", "R0007900"),
    ("urban_rural_14", "R0001800"),
]

TARGET_SCORES = [
    "coding_speed",
    "numerical_operations",
    "clerical_speed",
    "paragraph_comprehension",
    "verbal",
    "arithmetic_reasoning",
    "math_knowledge",
    "quantitative",
    "auto_shop",
    "mechanical_comprehension",
    "electronic_information",
    "mechanical",
    "mechanical_plus_electronic",
]


def pair_difference(rows: dict[int, dict[str, str]], pair: dict[str, str], code: str) -> float | None:
    female_id = int(pair["female_caseid"])
    male_id = int(pair["male_caseid"])
    female_value = to_int(rows[female_id][code])
    male_value = to_int(rows[male_id][code])
    if female_value is None or male_value is None:
        return None
    return float(female_value - male_value)


def model_for_score(
    rows: dict[int, dict[str, str]],
    pairs: list[dict[str, str]],
    standardized: dict[int, dict[str, float]],
    score_name: str,
    include_schooling: bool,
) -> dict[str, float | int] | None:
    y = []
    x_rows = []
    covariates = BASE_COVARIATES + (SCHOOLING_BLOCK if include_schooling else [])
    for pair in pairs:
        female_id = int(pair["female_caseid"])
        male_id = int(pair["male_caseid"])
        female_score = standardized[female_id].get(score_name)
        male_score = standardized[male_id].get(score_name)
        if female_score is None or male_score is None:
            continue
        diffs = []
        okay = True
        for _, code in covariates:
            diff = pair_difference(rows, pair, code)
            if diff is None:
                okay = False
                break
            diffs.append(diff)
        if not okay:
            continue
        y.append(female_score - male_score)
        x_rows.append([1.0] + diffs)
    if len(y) < 20:
        return None
    intercept, _, se = fit_ols(y, x_rows)
    return {
        "n_pairs": len(y),
        "beta_sd": round(intercept, 6),
        "ci_low": round(intercept - 1.96 * se, 6),
        "ci_high": round(intercept + 1.96 * se, 6),
    }


def main() -> int:
    rows = load_rows()
    raw_surface = raw_subtest_surface(rows)
    standardized = standardized_person_scores(rows, raw_surface)
    pairs = load_pairs(
        Path("sources/iq-sex-diff/data/nlsy/nlsy79_opposite_sex_sibling_pairs.tsv")
    )

    output_rows = []
    for score_name in TARGET_SCORES:
        base = model_for_score(rows, pairs, standardized, score_name, include_schooling=False)
        full = model_for_score(rows, pairs, standardized, score_name, include_schooling=True)
        if base is None or full is None:
            continue
        beta0 = float(base["beta_sd"])
        beta1 = float(full["beta_sd"])
        attenuation = "" if abs(beta0) < 1e-12 else round(1.0 - (beta1 / beta0), 6)
        output_rows.append(
            {
                "score_name": score_name,
                "n_pairs_base": base["n_pairs"],
                "beta_base_sd": base["beta_sd"],
                "ci_low_base": base["ci_low"],
                "ci_high_base": base["ci_high"],
                "n_pairs_schooling": full["n_pairs"],
                "beta_schooling_sd": full["beta_sd"],
                "ci_low_schooling": full["ci_low"],
                "ci_high_schooling": full["ci_high"],
                "attenuation_share": attenuation,
            }
        )

    output_path = Path("sources/iq-sex-diff/data/nlsy/nlsy79_schooling_pass.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "score_name",
                "n_pairs_base",
                "beta_base_sd",
                "ci_low_base",
                "ci_high_base",
                "n_pairs_schooling",
                "beta_schooling_sd",
                "ci_low_schooling",
                "ci_high_schooling",
                "attenuation_share",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print("NLSY79 schooling pass")
    print("Positive attenuation = coefficient shrinks after frozen schooling block")
    for row in output_rows:
        print(
            f"{row['score_name']:<24} "
            f"base={row['beta_base_sd']:<9} "
            f"school={row['beta_schooling_sd']:<9} "
            f"atten={row['attenuation_share']}"
        )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
