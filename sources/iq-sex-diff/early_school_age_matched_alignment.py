from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA_DIR = ROOT / "data"

INPUTS = {
    "nlscya": DATA_DIR / "nlscya" / "nlscya_early_school_panel.parquet",
    "ecls_k2011": DATA_DIR / "ecls_k2011" / "eclsk2011_early_school_panel.parquet",
    "ecls_k": DATA_DIR / "ecls_k" / "eclsk_early_school_panel.parquet",
}

MATH_OUTCOME = {
    "nlscya": "piat_math_std",
    "ecls_k2011": "math_k5_scale",
    "ecls_k": "math_irt_scale",
}

READING_OUTCOME = {
    "nlscya": "piat_reading_comp_std",
    "ecls_k2011": "reading_k5_scale",
    "ecls_k": "reading_irt_scale",
}

AGE_BINS = [84, 90, 96, 102, 108, 114, 120, 126, 132]

OUT_DIR = DATA_DIR / "early_school_alignment"
PAIR_OUT = OUT_DIR / "early_school_age_matched_pairs.parquet"
GAPS_OUT = OUT_DIR / "early_school_age_matched_gaps.tsv"
MODELS_OUT = OUT_DIR / "early_school_age_matched_models.tsv"
COMPARE_OUT = OUT_DIR / "early_school_age_matched_compare.tsv"


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_standardize(values: np.ndarray, weights: np.ndarray) -> np.ndarray:
    mean = weighted_mean(values, weights)
    var = weighted_var(values, weights)
    sd = math.sqrt(var) if var > 0 else math.nan
    return (values - mean) / sd if sd and pd.notna(sd) else np.full_like(values, np.nan, dtype=float)


def weighted_d(values: np.ndarray, female: np.ndarray, weights: np.ndarray) -> tuple[float, float, float]:
    mask_f = female == 1
    mask_m = female == 0
    if mask_f.sum() == 0 or mask_m.sum() == 0:
        return math.nan, math.nan, math.nan
    vf = values[mask_f]
    vm = values[mask_m]
    wf = weights[mask_f]
    wm = weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    var_f = weighted_var(vf, wf)
    var_m = weighted_var(vm, wm)
    pooled = math.sqrt(max((var_f + var_m) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def load_pairs(dataset: str) -> pd.DataFrame:
    panel = pd.read_parquet(INPUTS[dataset]).copy()
    math_name = MATH_OUTCOME[dataset]
    reading_name = READING_OUTCOME[dataset]

    keep_cols = ["child_id", "female", "wave", "score", "weight", "age_months"]
    if "wave_label" in panel.columns:
        keep_cols.append("wave_label")

    math_df = panel.loc[panel["outcome"] == math_name, keep_cols].rename(
        columns={"score": "math_score", "weight": "math_weight", "age_months": "math_age_months"}
    )
    read_df = panel.loc[panel["outcome"] == reading_name, keep_cols].rename(
        columns={"score": "reading_score", "weight": "reading_weight", "age_months": "reading_age_months"}
    )

    merge_cols = ["child_id", "female", "wave"]
    if "wave_label" in math_df.columns and "wave_label" in read_df.columns:
        merge_cols.append("wave_label")

    pairs = math_df.merge(read_df, on=merge_cols, how="inner")
    age_gap = (pairs["math_age_months"] - pairs["reading_age_months"]).abs()
    pairs = pairs.loc[age_gap <= 0.01].copy()
    pairs["child_id"] = pairs["child_id"].astype(str).str.strip()
    pairs["age_months"] = pairs[["math_age_months", "reading_age_months"]].mean(axis=1)
    pairs["age_years"] = pairs["age_months"] / 12.0
    pairs["weight"] = pairs[["math_weight", "reading_weight"]].mean(axis=1)
    pairs["dataset"] = dataset
    pairs = pairs.loc[pairs["age_months"].between(48, 180)].copy()
    return pairs


def add_age_bins(pairs: pd.DataFrame) -> pd.DataFrame:
    labeled = pairs.copy()
    labeled["age_bin"] = pd.cut(labeled["age_months"], bins=AGE_BINS, right=False)
    labeled = labeled.loc[labeled["age_bin"].notna()].copy()
    labeled["age_bin_label"] = labeled["age_bin"].map(lambda x: f"{int(x.left)}_{int(x.right)}")
    labeled["age_bin_left"] = labeled["age_bin"].map(lambda x: int(x.left))
    labeled["age_bin_right"] = labeled["age_bin"].map(lambda x: int(x.right))
    labeled = labeled.drop(columns=["age_bin"])
    return labeled


def enrich_group(sub: pd.DataFrame) -> pd.DataFrame:
    weights = sub["weight"].to_numpy(dtype=float)
    math_values = sub["math_score"].to_numpy(dtype=float)
    reading_values = sub["reading_score"].to_numpy(dtype=float)
    out = sub.copy()
    out["math_z"] = weighted_standardize(math_values, weights)
    out["reading_z"] = weighted_standardize(reading_values, weights)
    out["math_minus_reading_z"] = out["math_z"] - out["reading_z"]
    return out


def summarize_groups(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (dataset, age_bin_label), sub in pairs.groupby(["dataset", "age_bin_label"], observed=True):
        female = sub["female"].to_numpy(dtype=int)
        weights = sub["weight"].to_numpy(dtype=float)
        for outcome in ["math_z", "reading_z", "math_minus_reading_z"]:
            values = sub[outcome].to_numpy(dtype=float)
            mean_f, mean_m, d = weighted_d(values, female, weights)
            rows.append(
                {
                    "dataset": dataset,
                    "age_bin_label": age_bin_label,
                    "n": int(len(sub)),
                    "mean_age_months": float(np.average(sub["age_months"], weights=sub["weight"])),
                    "outcome": outcome,
                    "female_mean": mean_f,
                    "male_mean": mean_m,
                    "d_female_minus_male": d,
                }
            )
    return pd.DataFrame(rows).sort_values(["dataset", "age_bin_label", "outcome"]).reset_index(drop=True)


def run_models(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (dataset, age_bin_label), sub in pairs.groupby(["dataset", "age_bin_label"], observed=True):
        if sub["female"].nunique() < 2 or len(sub) < 50:
            continue
        model = smf.wls("math_z ~ female + reading_z", data=sub, weights=sub["weight"]).fit(cov_type="HC1")
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        rows.append(
            {
                "dataset": dataset,
                "age_bin_label": age_bin_label,
                "n": int(model.nobs),
                "mean_age_months": float(np.average(sub["age_months"], weights=sub["weight"])),
                "beta": coef,
                "se": se,
                "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                "r_squared": float(model.rsquared),
            }
        )
    return pd.DataFrame(rows).sort_values(["dataset", "age_bin_label"]).reset_index(drop=True)


def compare_primary_datasets(gaps: pd.DataFrame, models: pd.DataFrame) -> pd.DataFrame:
    primary = gaps.loc[gaps["dataset"].isin(["nlscya", "ecls_k2011"])].copy()
    pivot = primary.pivot_table(
        index=["dataset", "age_bin_label"],
        columns="outcome",
        values="d_female_minus_male",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None
    pivot = pivot.merge(models[["dataset", "age_bin_label", "beta", "ci_low", "ci_high"]], on=["dataset", "age_bin_label"])
    wide = pivot.pivot(index="age_bin_label", columns="dataset")
    wide.columns = [f"{metric}_{dataset}" for metric, dataset in wide.columns]
    wide = wide.reset_index()
    for metric in ["math_z", "reading_z", "math_minus_reading_z", "beta"]:
        left = f"{metric}_nlscya"
        right = f"{metric}_ecls_k2011"
        if left in wide.columns and right in wide.columns:
            wide[f"{metric}_delta_nlscya_minus_eclsk2011"] = wide[left] - wide[right]
    return wide.sort_values("age_bin_label").reset_index(drop=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pairs = pd.concat([load_pairs(name) for name in INPUTS], ignore_index=True)
    pairs = add_age_bins(pairs)
    enriched = [enrich_group(sub) for _, sub in pairs.groupby(["dataset", "age_bin_label"], observed=True)]
    work = pd.concat(enriched, ignore_index=True)

    work.to_parquet(PAIR_OUT, index=False)
    gaps = summarize_groups(work)
    models = run_models(work)
    compare = compare_primary_datasets(gaps, models)

    gaps.to_csv(GAPS_OUT, sep="\t", index=False)
    models.to_csv(MODELS_OUT, sep="\t", index=False)
    compare.to_csv(COMPARE_OUT, sep="\t", index=False)

    print(f"wrote {PAIR_OUT}")
    print(f"wrote {GAPS_OUT}")
    print(f"wrote {MODELS_OUT}")
    print(f"wrote {COMPARE_OUT}")


if __name__ == "__main__":
    main()
