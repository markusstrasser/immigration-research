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

OUT_DIR = DATA_DIR / "early_school_alignment"
PAIR_OUT = OUT_DIR / "early_school_alignment_pairs.parquet"
GAPS_OUT = OUT_DIR / "early_school_alignment_gaps.tsv"
MODELS_OUT = OUT_DIR / "early_school_alignment_models.tsv"
SUMMARY_OUT = OUT_DIR / "early_school_alignment_summary.tsv"

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

    keep_cols = ["child_id", "female", "wave", "score", "weight"]
    if "wave_label" in panel.columns:
        keep_cols.append("wave_label")
    if "age_years" in panel.columns:
        keep_cols.append("age_years")
    if "age_months" in panel.columns:
        keep_cols.append("age_months")

    math_df = panel.loc[panel["outcome"] == math_name, keep_cols].rename(
        columns={"score": "math_score", "weight": "math_weight"}
    )
    read_df = panel.loc[panel["outcome"] == reading_name, keep_cols].rename(
        columns={"score": "reading_score", "weight": "reading_weight"}
    )

    merge_cols = ["child_id", "female", "wave"]
    if "wave_label" in math_df.columns and "wave_label" in read_df.columns:
        merge_cols.append("wave_label")
    if "age_years" in math_df.columns and "age_years" in read_df.columns:
        merge_cols.append("age_years")
    if "age_months" in math_df.columns and "age_months" in read_df.columns:
        merge_cols.append("age_months")

    pairs = math_df.merge(read_df, on=merge_cols, how="inner")
    pairs["child_id"] = pairs["child_id"].astype(str).str.strip()
    pairs["dataset"] = dataset
    pairs["weight"] = pairs[["math_weight", "reading_weight"]].mean(axis=1)
    return pairs


def enrich_group(sub: pd.DataFrame) -> pd.DataFrame:
    weights = sub["weight"].to_numpy(dtype=float)
    math_values = sub["math_score"].to_numpy(dtype=float)
    reading_values = sub["reading_score"].to_numpy(dtype=float)
    math_z = weighted_standardize(math_values, weights)
    reading_z = weighted_standardize(reading_values, weights)
    out = sub.copy()
    out["math_z"] = math_z
    out["reading_z"] = reading_z
    out["math_minus_reading_z"] = out["math_z"] - out["reading_z"]
    return out


def summarize_gaps(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (dataset, wave), sub in pairs.groupby(["dataset", "wave"], observed=True):
        female = sub["female"].to_numpy(dtype=int)
        weights = sub["weight"].to_numpy(dtype=float)
        for outcome in ["math_z", "reading_z", "math_minus_reading_z"]:
            values = sub[outcome].to_numpy(dtype=float)
            mean_f, mean_m, d = weighted_d(values, female, weights)
            row: dict[str, object] = {
                "dataset": dataset,
                "wave": wave,
                "outcome": outcome,
                "n": int(len(sub)),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
            }
            if "wave_label" in sub.columns:
                row["wave_label"] = sub["wave_label"].iloc[0]
            if "age_years" in sub.columns:
                row["mean_age_years"] = float(np.average(sub["age_years"], weights=sub["weight"]))
            rows.append(row)
    return pd.DataFrame(rows).sort_values(["dataset", "wave", "outcome"]).reset_index(drop=True)


def run_models(pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (dataset, wave), sub in pairs.groupby(["dataset", "wave"], observed=True):
        model = smf.wls("math_z ~ female + reading_z", data=sub, weights=sub["weight"]).fit(cov_type="HC1")
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        row: dict[str, object] = {
            "dataset": dataset,
            "wave": wave,
            "term": "female",
            "n": int(model.nobs),
            "beta": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(model.rsquared),
        }
        if "wave_label" in sub.columns:
            row["wave_label"] = sub["wave_label"].iloc[0]
        if "age_years" in sub.columns:
            row["mean_age_years"] = float(np.average(sub["age_years"], weights=sub["weight"]))
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["dataset", "wave"]).reset_index(drop=True)


def build_summary(gaps: pd.DataFrame, models: pd.DataFrame) -> pd.DataFrame:
    pivot = gaps.pivot_table(
        index=["dataset", "wave"] + (["wave_label"] if "wave_label" in gaps.columns else []),
        columns="outcome",
        values="d_female_minus_male",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None
    summary = pivot.merge(
        models[["dataset", "wave", "beta", "ci_low", "ci_high", "r_squared"]],
        on=["dataset", "wave"],
        how="left",
    )
    return summary.sort_values(["dataset", "wave"]).reset_index(drop=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_pairs = pd.concat([load_pairs(name) for name in INPUTS], ignore_index=True)
    enriched = []
    for _, sub in all_pairs.groupby(["dataset", "wave"], observed=True):
        enriched.append(enrich_group(sub))
    pairs = pd.concat(enriched, ignore_index=True)
    pairs.to_parquet(PAIR_OUT, index=False)

    gaps = summarize_gaps(pairs)
    models = run_models(pairs)
    summary = build_summary(gaps, models)

    gaps.to_csv(GAPS_OUT, sep="\t", index=False)
    models.to_csv(MODELS_OUT, sep="\t", index=False)
    summary.to_csv(SUMMARY_OUT, sep="\t", index=False)

    print(f"wrote {PAIR_OUT}")
    print(f"wrote {GAPS_OUT}")
    print(f"wrote {MODELS_OUT}")
    print(f"wrote {SUMMARY_OUT}")


if __name__ == "__main__":
    main()
