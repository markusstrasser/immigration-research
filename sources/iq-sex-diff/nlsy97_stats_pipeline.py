#!/usr/bin/env python3
"""Weighted NLSY97 CAT-ASVAB descriptive replication with signed-score diagnostics."""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from stage0_config import NLSY97


MISSING_CODES = {"", ".", "-1", "-2", "-3", "-4", "-5"}
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

DOMAINS = {
    "clerical_speed": ["numerical_operations", "coding_speed"],
    "verbal": ["word_knowledge", "paragraph_comprehension"],
    "quantitative": ["arithmetic_reasoning", "math_knowledge"],
    "mechanical": ["auto_information", "shop_information", "mechanical_comprehension"],
}


def parse_numeric(value: str) -> float | None:
    if value in MISSING_CODES:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def load_frame(
    extra_fields: dict[str, dict[str, str]] | None = None,
) -> tuple[pd.DataFrame, list[dict[str, int | str]]]:
    zipped = Path(NLSY97["path"])
    member = NLSY97["zip_member"]
    wanted = [
        NLSY97["id"]["code"],
        NLSY97["sex"]["code"],
        NLSY97["weights"]["cross_section_1997"]["code"],
        NLSY97["summary_scores"]["math_verbal_percentile"]["code"],
    ]
    for pair in NLSY97["ability_scores"].values():
        wanted.extend([pair["pos"], pair["neg"]])
    extra_fields = extra_fields or {}
    for field in extra_fields.values():
        wanted.append(field["code"])

    records: list[dict[str, float | int | None]] = []
    diagnostics: list[dict[str, int | str]] = []
    print("Loading frozen NLSY97 rows...")
    with zipfile.ZipFile(zipped) as archive:
        with archive.open(member) as raw:
            reader = csv.reader((line.decode("latin-1") for line in raw))
            header = next(reader)
            index = {column: header.index(column) for column in wanted}
            for row in reader:
                caseid = parse_numeric(row[index[NLSY97["id"]["code"]]])
                if caseid is None:
                    continue
                record: dict[str, float | int | None] = {
                    "caseid": int(caseid),
                    "sex": parse_numeric(row[index[NLSY97["sex"]["code"]]]),
                    "weight_1997": parse_numeric(
                        row[index[NLSY97["weights"]["cross_section_1997"]["code"]]]
                    ),
                    "math_verbal_percentile": parse_numeric(
                        row[index[NLSY97["summary_scores"]["math_verbal_percentile"]["code"]]]
                    ),
                }
                for name, pair in NLSY97["ability_scores"].items():
                    pos = parse_numeric(row[index[pair["pos"]]])
                    neg = parse_numeric(row[index[pair["neg"]]])
                    if pos is not None and neg is None:
                        value = pos
                        status = "pos_only"
                    elif neg is not None and pos is None:
                        value = -neg
                        status = "neg_only"
                    elif pos is not None and neg is not None:
                        value = pos - neg
                        status = "both_nonmissing"
                    else:
                        value = np.nan
                        status = "missing"
                    record[name] = value
                    diagnostics.append({"score_name": name, "status": status, "caseid": int(caseid)})
                for name, field in extra_fields.items():
                    record[name] = parse_numeric(row[index[field["code"]]])
                records.append(record)
    print(f"Loaded {len(records):,} respondents")
    return pd.DataFrame.from_records(records).set_index("caseid").sort_index(), diagnostics


def pooled_weighted_sd(values: pd.Series, weights: pd.Series, female_mask: pd.Series) -> float | None:
    male_mask = ~female_mask
    female_values = values[female_mask]
    female_weights = weights[female_mask]
    male_values = values[male_mask]
    male_weights = weights[male_mask]
    if female_values.empty or male_values.empty:
        return None

    female_mean = np.average(female_values, weights=female_weights)
    male_mean = np.average(male_values, weights=male_weights)
    female_var = np.average((female_values - female_mean) ** 2, weights=female_weights)
    male_var = np.average((male_values - male_mean) ** 2, weights=male_weights)
    pooled = (
        female_weights.sum() * female_var + male_weights.sum() * male_var
    ) / (female_weights.sum() + male_weights.sum())
    if pooled <= 0:
        return None
    return float(np.sqrt(pooled))


def standardize_scores(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    frame = frame.copy()
    female_mask = frame["sex"].eq(NLSY97["sex"]["female"])
    sex_valid = frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
    weight_valid = frame["weight_1997"].gt(0)
    standardized: list[str] = []

    score_names = list(NLSY97["ability_scores"]) + ["math_verbal_percentile"]
    for name in score_names:
        valid = sex_valid & weight_valid & frame[name].notna()
        if valid.sum() < 30:
            continue
        pooled_sd = pooled_weighted_sd(
            frame.loc[valid, name],
            frame.loc[valid, "weight_1997"],
            female_mask[valid],
        )
        if pooled_sd is None:
            continue
        overall_mean = float(np.average(frame.loc[valid, name], weights=frame.loc[valid, "weight_1997"]))
        z_name = f"{name}_z"
        frame[z_name] = (frame[name] - overall_mean) / pooled_sd
        standardized.append(z_name)

    for domain, components in DOMAINS.items():
        raw_name = f"{domain}_raw"
        z_name = f"{domain}_z"
        frame[raw_name] = frame[components].mean(axis=1, skipna=False)
        valid = sex_valid & weight_valid & frame[raw_name].notna()
        if valid.sum() < 30:
            continue
        pooled_sd = pooled_weighted_sd(
            frame.loc[valid, raw_name],
            frame.loc[valid, "weight_1997"],
            female_mask[valid],
        )
        if pooled_sd is None:
            continue
        overall_mean = float(np.average(frame.loc[valid, raw_name], weights=frame.loc[valid, "weight_1997"]))
        frame[z_name] = (frame[raw_name] - overall_mean) / pooled_sd
        standardized.append(z_name)
    return frame, standardized


def fit_weighted_gap(frame: pd.DataFrame, outcome: str) -> dict[str, float | int | str] | None:
    valid = (
        frame["sex"].isin([NLSY97["sex"]["male"], NLSY97["sex"]["female"]])
        & frame["weight_1997"].gt(0)
        & frame[outcome].notna()
    )
    sample = frame.loc[valid, ["sex", "weight_1997", outcome]].copy()
    if len(sample) < 30:
        return None
    sample["female"] = sample["sex"].eq(NLSY97["sex"]["female"]).astype(float)
    design = sm.add_constant(sample[["female"]], has_constant="add")
    fit = sm.WLS(sample[outcome], design, weights=sample["weight_1997"]).fit(cov_type="HC1")
    low, high = fit.conf_int().loc["female"]
    return {
        "analysis_family": "descriptive",
        "model_name": "weighted_gap",
        "score_name": outcome.removesuffix("_z"),
        "n_obs": int(fit.nobs),
        "beta_sd": float(fit.params["female"]),
        "se_sd": float(fit.bse["female"]),
        "ci_low": float(low),
        "ci_high": float(high),
        "p_value": float(fit.pvalues["female"]),
    }


def write_diagnostics(diagnostics: list[dict[str, int | str]]) -> Path:
    counts: dict[tuple[str, str], int] = {}
    for row in diagnostics:
        key = (str(row["score_name"]), str(row["status"]))
        counts[key] = counts.get(key, 0) + 1

    output_path = DATA_DIR / "nlsy" / "nlsy97_signed_score_diagnostics.tsv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["score_name", "status", "n_rows"],
            delimiter="\t",
        )
        writer.writeheader()
        for (score_name, status), n_rows in sorted(counts.items()):
            writer.writerow({"score_name": score_name, "status": status, "n_rows": n_rows})
    return output_path


def main() -> int:
    frame, diagnostics = load_frame()
    diagnostic_path = write_diagnostics(diagnostics)
    print("Standardizing CAT-ASVAB surfaces...")
    frame, standardized = standardize_scores(frame)
    print("Fitting weighted sex gaps...")
    rows = [
        result
        for result in (fit_weighted_gap(frame, column) for column in standardized)
        if result is not None
    ]

    output_path = DATA_DIR / "nlsy" / "nlsy97_stats_pipeline.tsv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "analysis_family",
                "model_name",
                "score_name",
                "n_obs",
                "beta_sd",
                "se_sd",
                "ci_low",
                "ci_high",
                "p_value",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")
    print(f"Wrote {diagnostic_path}")
    for score in [
        "clerical_speed",
        "verbal",
        "quantitative",
        "mechanical",
        "math_verbal_percentile",
        "assembling_objects",
    ]:
        matched = [row for row in rows if row["score_name"] == score]
        if not matched:
            continue
        row = matched[0]
        print(
            f"{score:<24} beta={row['beta_sd']:+.3f} "
            f"ci=({row['ci_low']:+.3f},{row['ci_high']:+.3f}) n={row['n_obs']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
