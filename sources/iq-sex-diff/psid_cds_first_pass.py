#!/usr/bin/env python3
"""First-pass PSID CDS summaries for child math/reading surfaces."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "psid"
PANEL_PATH = DATA_DIR / "psid_cds_panel.parquet"

OVERALL_OUT = DATA_DIR / "psid_cds_surface_gaps.tsv"
ALIGNED_OUT = DATA_DIR / "psid_cds_aligned_gaps.tsv"
FAMILY_OUT = DATA_DIR / "psid_cds_family_fe.tsv"


def clean_score(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    values = values.where(values >= 0)
    return values.where(values < 900)


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_gap(values: np.ndarray, female: np.ndarray, weights: np.ndarray) -> tuple[float, float, float]:
    mask_f = female == 1
    mask_m = female == 0
    if mask_f.sum() == 0 or mask_m.sum() == 0:
        return math.nan, math.nan, math.nan

    vf, vm = values[mask_f], values[mask_m]
    wf, wm = weights[mask_f], weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    pooled = math.sqrt(max((weighted_var(vf, wf) + weighted_var(vm, wm)) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL_PATH)
    df["female"] = pd.to_numeric(df["female"], errors="coerce")
    df["child_weight"] = clean_score(df["child_weight"]).fillna(1.0)
    df["age_months"] = clean_score(df["age_months"]).where(lambda s: s <= 300)
    df["age_years"] = df["age_months"] / 12.0
    df["grade_in_school"] = clean_score(df["grade_in_school"]).where(lambda s: s <= 20)
    for column in [
        "letter_word_std",
        "passage_comp_std",
        "broad_reading_std",
        "calculation_std",
        "applied_problems_std",
        "broad_math_std",
    ]:
        if column in df.columns:
            df[column] = clean_score(df[column])
    return df


def build_long_scores(df: pd.DataFrame) -> pd.DataFrame:
    specs = [
        ("letter_word_std", "letter_word"),
        ("passage_comp_std", "passage_comp"),
        ("broad_reading_std", "broad_reading"),
        ("calculation_std", "calculation"),
        ("applied_problems_std", "applied_problems"),
        ("broad_math_std", "broad_math"),
    ]

    frames: list[pd.DataFrame] = []
    keep = ["source", "wave", "family_id68", "person_id68", "pair_id68", "female", "child_weight", "age_years"]
    for column, outcome in specs:
        if column not in df.columns:
            continue
        frame = df[keep + [column]].copy()
        frame.rename(columns={column: "score"}, inplace=True)
        frame["outcome"] = outcome
        frames.append(frame)

    long_df = pd.concat(frames, ignore_index=True)
    return long_df.dropna(subset=["score", "female"]).copy()


def summarize(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, sub in df.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        values = sub["score"].to_numpy(dtype=float)
        female = sub["female"].to_numpy(dtype=int)
        weights = sub["child_weight"].to_numpy(dtype=float)
        mean_f, mean_m, d = weighted_gap(values, female, weights)
        row = {col: key for col, key in zip(group_cols, keys, strict=True)}
        row.update(
            {
                "n": int(len(sub)),
                "families68": int(sub["family_id68"].nunique()),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
                "mean_age_years": float(np.average(sub["age_years"], weights=sub["child_weight"])),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(group_cols).reset_index(drop=True)


def build_aligned(df: pd.DataFrame) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    common = ["source", "wave", "family_id68", "person_id68", "pair_id68", "female", "child_weight", "age_years"]

    pairs = [
        ("applied_problems_std", "broad_reading_std", "applied_minus_reading"),
        ("calculation_std", "broad_reading_std", "calculation_minus_reading"),
        ("broad_math_std", "broad_reading_std", "broad_math_minus_reading"),
    ]
    for math_col, read_col, label in pairs:
        if math_col not in df.columns or read_col not in df.columns:
            continue
        frame = df[common + [math_col, read_col]].copy()
        frame["score"] = frame[math_col] - frame[read_col]
        frame["outcome"] = label
        frame = frame.drop(columns=[math_col, read_col])
        frames.append(frame)

    aligned = pd.concat(frames, ignore_index=True)
    return aligned.dropna(subset=["score", "female"]).copy()


def family_fe(aligned: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome, sub in aligned.groupby("outcome", observed=True):
        work = sub.dropna(subset=["family_id68", "age_years"]).copy()
        family_counts = work.groupby("family_id68")["pair_id68"].nunique()
        work = work[work["family_id68"].isin(family_counts[family_counts >= 2].index)].copy()
        if work.empty:
            continue

        model = smf.wls(
            "score ~ female + age_years + C(wave) + C(family_id68)",
            data=work,
            weights=work["child_weight"],
        ).fit(cov_type="cluster", cov_kwds={"groups": work["family_id68"]})
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        rows.append(
            {
                "outcome": outcome,
                "n": int(model.nobs),
                "families68": int(work["family_id68"].nunique()),
                "beta_female": coef,
                "se": se,
                "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                "r_squared": float(model.rsquared),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    df = load_panel()
    long_df = build_long_scores(df)
    overall = summarize(long_df, ["wave", "outcome"])
    aligned = build_aligned(df)
    aligned_summary = summarize(aligned, ["wave", "outcome"])
    family = family_fe(aligned)

    overall.to_csv(OVERALL_OUT, sep="\t", index=False)
    aligned_summary.to_csv(ALIGNED_OUT, sep="\t", index=False)
    family.to_csv(FAMILY_OUT, sep="\t", index=False)

    print(f"wrote {OVERALL_OUT}")
    print(f"wrote {ALIGNED_OUT}")
    print(f"wrote {FAMILY_OUT}")


if __name__ == "__main__":
    main()
