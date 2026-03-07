#!/usr/bin/env python3
"""First locked empirical pass for NLSY79 raw gaps and sibling comparisons."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from build_nlsy79_sibling_pairs import load_rows, to_int
from stage0_config import NLSY79


MISSING = {"", ".", "-1", "-2", "-3", "-4", "-5"}


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def weighted_mean(points: list[tuple[float, float]]) -> float:
    total_weight = sum(weight for _, weight in points)
    return sum(value * weight for value, weight in points) / total_weight


def weighted_variance(points: list[tuple[float, float]]) -> float:
    mu = weighted_mean(points)
    total_weight = sum(weight for _, weight in points)
    return sum(weight * (value - mu) ** 2 for value, weight in points) / total_weight


def weighted_pooled_sd(
    female: list[tuple[float, float]], male: list[tuple[float, float]]
) -> float | None:
    if len(female) < 2 or len(male) < 2:
        return None
    wf = sum(weight for _, weight in female)
    wm = sum(weight for _, weight in male)
    if wf <= 0 or wm <= 0:
        return None
    vf = weighted_variance(female)
    vm = weighted_variance(male)
    pooled = ((wf * vf) + (wm * vm)) / (wf + wm)
    if pooled <= 0:
        return None
    return math.sqrt(pooled)


def inverse_matrix(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    augmented = [row[:] + [1.0 if i == j else 0.0 for j in range(size)] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda idx: abs(augmented[idx][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("Singular matrix")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        factor = augmented[col][col]
        augmented[col] = [value / factor for value in augmented[col]]
        for row_idx in range(size):
            if row_idx == col:
                continue
            factor = augmented[row_idx][col]
            augmented[row_idx] = [
                current - factor * pivot_value
                for current, pivot_value in zip(augmented[row_idx], augmented[col])
            ]
    return [row[size:] for row in augmented]


def matrix_vector_multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(value * coefficient for value, coefficient in zip(row, vector)) for row in matrix]


def fit_ols(y: list[float], x_rows: list[list[float]]) -> tuple[float, float, float]:
    xtx = [[0.0 for _ in range(len(x_rows[0]))] for _ in range(len(x_rows[0]))]
    xty = [0.0 for _ in range(len(x_rows[0]))]
    for x_row, target in zip(x_rows, y):
        for i, xi in enumerate(x_row):
            xty[i] += xi * target
            for j, xj in enumerate(x_row):
                xtx[i][j] += xi * xj
    xtx_inv = inverse_matrix(xtx)
    beta = matrix_vector_multiply(xtx_inv, xty)
    residuals = [
        target - sum(coef * value for coef, value in zip(beta, x_row))
        for x_row, target in zip(x_rows, y)
    ]
    dof = len(y) - len(beta)
    sigma2 = sum(residual**2 for residual in residuals) / dof if dof > 0 else 0.0
    se = math.sqrt(max(sigma2 * xtx_inv[0][0], 0.0))
    return beta[0], beta[1] if len(beta) > 1 else 0.0, se


def valid_numeric(value: str) -> float | None:
    if value in MISSING:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def valid_weight(value: str) -> float | None:
    weight = valid_numeric(value)
    if weight is None or weight <= 0:
        return None
    return weight


def raw_subtest_surface(rows: dict[int, dict[str, str]]) -> dict[str, dict[str, object]]:
    weight_code = NLSY79["weights"]["asvab_1981"]["code"]
    sex_code = NLSY79["sex"]["code"]
    result: dict[str, dict[str, object]] = {}
    for subtest, metadata in NLSY79["primary_subtests"].items():
        female: list[tuple[float, float]] = []
        male: list[tuple[float, float]] = []
        for values in rows.values():
            score = valid_numeric(values[metadata["code"]])
            weight = valid_weight(values[weight_code])
            sex = to_int(values[sex_code])
            if score is None or weight is None or sex not in {1, 2}:
                continue
            if sex == 2:
                female.append((score, weight))
            elif sex == 1:
                male.append((score, weight))
        pooled = weighted_pooled_sd(female, male)
        if pooled is None:
            continue
        female_mean = weighted_mean(female)
        male_mean = weighted_mean(male)
        all_points = female + male
        overall_mean = weighted_mean(all_points)
        raw_gap = (female_mean - male_mean) / pooled
        result[subtest] = {
            "pooled_sd": pooled,
            "overall_mean": overall_mean,
            "raw_gap": raw_gap,
            "n_female": len(female),
            "n_male": len(male),
        }
    return result


def standardized_person_scores(
    rows: dict[int, dict[str, str]], raw_surface: dict[str, dict[str, object]]
) -> dict[int, dict[str, float]]:
    standardized: dict[int, dict[str, float]] = {}
    for caseid, values in rows.items():
        person_scores: dict[str, float] = {}
        for subtest, metadata in NLSY79["primary_subtests"].items():
            if subtest not in raw_surface:
                continue
            score = valid_numeric(values[metadata["code"]])
            if score is None:
                continue
            person_scores[subtest] = (
                score - float(raw_surface[subtest]["overall_mean"])
            ) / float(raw_surface[subtest]["pooled_sd"])
        standardized[caseid] = person_scores

    for domain, components in NLSY79["domain_composites"].items():
        domain_values_f: list[float] = []
        domain_values_m: list[float] = []
        for caseid, values in rows.items():
            sex = to_int(values[NLSY79["sex"]["code"]])
            if sex not in {1, 2}:
                continue
            scores = standardized[caseid]
            if not all(component in scores for component in components):
                continue
            composite = mean([scores[component] for component in components])
            standardized[caseid][domain] = composite
            if sex == 2:
                domain_values_f.append(composite)
            else:
                domain_values_m.append(composite)
        if len(domain_values_f) >= 2 and len(domain_values_m) >= 2:
            domain_sd = math.sqrt(
                (
                    ((len(domain_values_f) - 1) * variance(domain_values_f))
                    + ((len(domain_values_m) - 1) * variance(domain_values_m))
                )
                / (len(domain_values_f) + len(domain_values_m) - 2)
            )
            if domain_sd > 0:
                for caseid in standardized:
                    if domain in standardized[caseid]:
                        standardized[caseid][domain] /= domain_sd
    return standardized


def variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    return sum((value - mu) ** 2 for value in values) / (len(values) - 1)


def raw_domain_surface(
    rows: dict[int, dict[str, str]], standardized: dict[int, dict[str, float]]
) -> dict[str, dict[str, object]]:
    weight_code = NLSY79["weights"]["asvab_1981"]["code"]
    sex_code = NLSY79["sex"]["code"]
    surface: dict[str, dict[str, object]] = {}
    for domain in NLSY79["domain_composites"]:
        female: list[tuple[float, float]] = []
        male: list[tuple[float, float]] = []
        for caseid, person_scores in standardized.items():
            if domain not in person_scores:
                continue
            weight = valid_weight(rows[caseid][weight_code])
            sex = to_int(rows[caseid][sex_code])
            if weight is None or sex not in {1, 2}:
                continue
            if sex == 2:
                female.append((person_scores[domain], weight))
            else:
                male.append((person_scores[domain], weight))
        if len(female) < 2 or len(male) < 2:
            continue
        surface[domain] = {
            "raw_gap": weighted_mean(female) - weighted_mean(male),
            "n_female": len(female),
            "n_male": len(male),
        }
    return surface


def load_pairs(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def pair_surface(
    pairs: list[dict[str, str]],
    rows: dict[int, dict[str, str]],
    standardized: dict[int, dict[str, float]],
    score_names: list[str],
    strict_explicit_only: bool,
) -> list[dict[str, str | float | int]]:
    age_code = NLSY79["age"]["asvab_proxy"]["code"]
    age_fallback = NLSY79["age"]["baseline"]["code"]
    older_code = NLSY79["birth_order_proxy"]["code"]
    outputs = []
    for score_name in score_names:
        y: list[float] = []
        x_rows: list[list[float]] = []
        for pair in pairs:
            if strict_explicit_only and not (
                pair["relation_low"] in {"6", "7"} and pair["relation_high"] in {"6", "7"}
            ):
                continue
            female_id = int(pair["female_caseid"])
            male_id = int(pair["male_caseid"])
            female_score = standardized[female_id].get(score_name)
            male_score = standardized[male_id].get(score_name)
            if female_score is None or male_score is None:
                continue
            female_age = to_int(rows[female_id][age_code]) or to_int(rows[female_id][age_fallback])
            male_age = to_int(rows[male_id][age_code]) or to_int(rows[male_id][age_fallback])
            female_older = to_int(rows[female_id][older_code])
            male_older = to_int(rows[male_id][older_code])
            if female_age is None or male_age is None or female_older is None or male_older is None:
                continue
            y.append(female_score - male_score)
            x_rows.append([1.0, float(female_age - male_age), float(female_older - male_older)])
        if len(y) < 10:
            continue
        intercept, _, se = fit_ols(y, x_rows)
        outputs.append(
            {
                "score_name": score_name,
                "n_pairs": len(y),
                "beta_sd": round(intercept, 6),
                "ci_low": round(intercept - 1.96 * se, 6),
                "ci_high": round(intercept + 1.96 * se, 6),
            }
        )
    return outputs


def main() -> int:
    rows = load_rows()
    raw_surface = raw_subtest_surface(rows)
    standardized = standardized_person_scores(rows, raw_surface)
    raw_domains = raw_domain_surface(rows, standardized)
    pairs = load_pairs(
        Path("sources/iq-sex-diff/data/nlsy/nlsy79_opposite_sex_sibling_pairs.tsv")
    )

    output_rows = []
    for score_name, info in sorted(raw_surface.items()):
        output_rows.append(
            {
                "surface": "raw_weighted",
                "score_type": "subtest",
                "score_name": score_name,
                "n_female": info["n_female"],
                "n_male": info["n_male"],
                "estimate_sd": round(float(info["raw_gap"]), 6),
                "ci_low": "",
                "ci_high": "",
                "share_retained_vs_raw": "",
            }
        )
    for score_name, info in sorted(raw_domains.items()):
        output_rows.append(
            {
                "surface": "raw_weighted",
                "score_type": "domain",
                "score_name": score_name,
                "n_female": info["n_female"],
                "n_male": info["n_male"],
                "estimate_sd": round(float(info["raw_gap"]), 6),
                "ci_low": "",
                "ci_high": "",
                "share_retained_vs_raw": "",
            }
        )

    raw_lookup = {
        ("subtest", name): float(info["raw_gap"])
        for name, info in raw_surface.items()
    }
    raw_lookup.update(
        {
            ("domain", name): float(info["raw_gap"])
            for name, info in raw_domains.items()
        }
    )

    pair_primary = pair_surface(
        pairs,
        rows,
        standardized,
        list(raw_surface) + list(raw_domains),
        strict_explicit_only=False,
    )
    pair_strict = pair_surface(
        pairs,
        rows,
        standardized,
        list(raw_surface) + list(raw_domains),
        strict_explicit_only=True,
    )

    for surface_name, results in [
        ("pair_fe_primary", pair_primary),
        ("pair_fe_explicit_67_only", pair_strict),
    ]:
        for row in results:
            score_type = "domain" if row["score_name"] in raw_domains else "subtest"
            raw_gap = raw_lookup[(score_type, row["score_name"])]
            share = row["beta_sd"] / raw_gap if abs(raw_gap) > 1e-12 else None
            output_rows.append(
                {
                    "surface": surface_name,
                    "score_type": score_type,
                    "score_name": row["score_name"],
                    "n_female": row["n_pairs"],
                    "n_male": "",
                    "estimate_sd": row["beta_sd"],
                    "ci_low": row["ci_low"],
                    "ci_high": row["ci_high"],
                    "share_retained_vs_raw": ""
                    if share is None
                    else round(share, 6),
                }
            )

    output_path = Path("sources/iq-sex-diff/data/nlsy/nlsy79_first_pass.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "surface",
                "score_type",
                "score_name",
                "n_female",
                "n_male",
                "estimate_sd",
                "ci_low",
                "ci_high",
                "share_retained_vs_raw",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    print("NLSY79 first pass")
    print("Negative estimate = male advantage | Positive estimate = female advantage")
    for row in output_rows:
        if row["surface"] != "raw_weighted":
            print(
                f"{row['surface']:<24} {row['score_name']:<24} "
                f"n={row['n_female']:<5} est={row['estimate_sd']}"
            )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
