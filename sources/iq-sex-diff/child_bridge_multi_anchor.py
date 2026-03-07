#!/usr/bin/env python3
"""Multi-anchor child bridge sensitivity across public cohorts."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "child_bridge_multi_anchor"

SUMMARY_OUT = OUT_DIR / "child_bridge_multi_anchor_summary.tsv"
FE_OUT = OUT_DIR / "child_bridge_multi_anchor_family_fe.tsv"
COMPARE_OUT = OUT_DIR / "child_bridge_multi_anchor_compare.tsv"
MODELS_OUT = OUT_DIR / "child_bridge_multi_anchor_models.tsv"


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
    vf = values[mask_f]
    vm = values[mask_m]
    wf = weights[mask_f]
    wm = weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    pooled = math.sqrt(max((weighted_var(vf, wf) + weighted_var(vm, wm)) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def safe_mean(frame: pd.DataFrame, cols: list[str]) -> pd.Series:
    subset = frame[cols].copy()
    return subset.mean(axis=1, skipna=True)


def clean_score(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    values = values.where(values >= 0)
    return values.where(values < 900)


def summarize_frame(
    frame: pd.DataFrame,
    dataset: str,
    stage: str,
    anchor: str,
    outcome: str,
    value_col: str,
    weight_col: str,
) -> dict[str, object]:
    sub = frame.dropna(subset=[value_col, "female", weight_col]).copy()
    values = sub[value_col].to_numpy(dtype=float)
    female = sub["female"].to_numpy(dtype=int)
    weights = sub[weight_col].to_numpy(dtype=float)
    mean_f, mean_m, d = weighted_gap(values, female, weights)
    out: dict[str, object] = {
        "dataset": dataset,
        "stage": stage,
        "anchor": anchor,
        "outcome": outcome,
        "n": int(len(sub)),
        "female_mean": mean_f,
        "male_mean": mean_m,
        "d_female_minus_male": d,
    }
    if "family_id68" in sub.columns:
        out["families"] = int(sub["family_id68"].nunique())
    return out


def build_psid() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(DATA_DIR / "psid" / "psid_cds_panel.parquet").copy()
    df = df.rename(columns={"child_weight": "weight"})
    df["weight"] = clean_score(df["weight"]).fillna(1.0)
    df["age_years"] = clean_score(df["age_years"])
    for col in [
        "applied_problems_std",
        "broad_reading_std",
        "letter_word_std",
        "passage_comp_std",
    ]:
        df[col] = clean_score(df[col])
    df["math_minus_broad_reading"] = df["applied_problems_std"] - df["broad_reading_std"]
    df["math_minus_letter_word"] = df["applied_problems_std"] - df["letter_word_std"]
    df["math_minus_passage"] = df["applied_problems_std"] - df["passage_comp_std"]
    df["mean_verbal_std"] = safe_mean(df, ["letter_word_std", "passage_comp_std"])
    df["math_minus_mean_verbal"] = df["applied_problems_std"] - df["mean_verbal_std"]

    rows: list[dict[str, object]] = []
    anchor_map = {
        "broad_reading": "math_minus_broad_reading",
        "letter_word": "math_minus_letter_word",
        "passage": "math_minus_passage",
        "mean_verbal": "math_minus_mean_verbal",
    }
    for wave, sub in df.groupby("wave", observed=True):
        for anchor, col in anchor_map.items():
            rows.append(
                summarize_frame(
                    sub,
                    dataset="psid_cds",
                    stage=str(wave),
                    anchor=anchor,
                    outcome="applied_minus_anchor",
                    value_col=col,
                    weight_col="weight",
                )
            )
    rows.append(
        summarize_frame(
            df,
            dataset="psid_cds",
            stage="pooled",
            anchor="broad_reading",
            outcome="math_minus_broad_reading",
            value_col="math_minus_broad_reading",
            weight_col="weight",
        )
    )
    rows.append(
        summarize_frame(
            df,
            dataset="psid_cds",
            stage="pooled",
            anchor="letter_word",
            outcome="math_minus_letter_word",
            value_col="math_minus_letter_word",
            weight_col="weight",
        )
    )
    rows.append(
        summarize_frame(
            df,
            dataset="psid_cds",
            stage="pooled",
            anchor="passage",
            outcome="math_minus_passage",
            value_col="math_minus_passage",
            weight_col="weight",
        )
    )
    rows.append(
        summarize_frame(
            df,
            dataset="psid_cds",
            stage="pooled",
            anchor="mean_verbal",
            outcome="math_minus_mean_verbal",
            value_col="math_minus_mean_verbal",
            weight_col="weight",
        )
    )

    fe_rows: list[dict[str, object]] = []
    for anchor, col in anchor_map.items():
        work = df.dropna(subset=[col, "female", "family_id68", "age_years", "weight"]).copy()
        family_counts = work.groupby("family_id68")["pair_id68"].nunique()
        keep_families = family_counts[family_counts >= 2].index
        work = work[work["family_id68"].isin(keep_families)].copy()
        if work.empty:
            continue
        work["score"] = work[col]
        model = smf.wls(
            "score ~ female + age_years + C(wave) + C(family_id68)",
            data=work,
            weights=work["weight"],
        ).fit(cov_type="cluster", cov_kwds={"groups": work["family_id68"]})
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        fe_rows.append(
            {
                "dataset": "psid_cds",
                "anchor": anchor,
                "outcome": "applied_minus_anchor",
                "n": int(model.nobs),
                "families": int(work["family_id68"].nunique()),
                "beta_female": coef,
                "se": se,
                "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                "r_squared": float(model.rsquared),
            }
        )

    joint = df.dropna(
        subset=[
            "applied_problems_std",
            "letter_word_std",
            "passage_comp_std",
            "female",
            "family_id68",
            "age_years",
            "weight",
        ]
    ).copy()
    family_counts = joint.groupby("family_id68")["pair_id68"].nunique()
    joint = joint[joint["family_id68"].isin(family_counts[family_counts >= 2].index)].copy()
    joint_model = smf.wls(
        "applied_problems_std ~ female + letter_word_std + passage_comp_std + age_years + C(wave) + C(family_id68)",
        data=joint,
        weights=joint["weight"],
    ).fit(cov_type="cluster", cov_kwds={"groups": joint["family_id68"]})
    coef = joint_model.params.get("female", math.nan)
    se = joint_model.bse.get("female", math.nan)
    fe_rows.append(
        {
            "dataset": "psid_cds",
            "anchor": "joint_letter_passage",
            "outcome": "applied_on_joint_verbal",
            "n": int(joint_model.nobs),
            "families": int(joint["family_id68"].nunique()),
            "beta_female": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(joint_model.rsquared),
        }
    )

    return pd.DataFrame(rows), pd.DataFrame(fe_rows)


def build_nlscya() -> pd.DataFrame:
    panel = pd.read_parquet(DATA_DIR / "nlscya" / "nlscya_early_school_panel.parquet").copy()
    wide = (
        panel.pivot_table(
            index=["child_id", "wave", "female", "age_months", "weight", "age_bin"],
            columns="outcome",
            values="score",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    wide["math_minus_reading"] = wide["piat_math_std"] - wide["piat_reading_comp_std"]
    wide["math_minus_ppvt"] = wide["piat_math_std"] - wide["ppvt_std"]
    wide["mean_verbal_std"] = safe_mean(wide, ["piat_reading_comp_std", "ppvt_std"])
    wide["math_minus_mean_verbal"] = wide["piat_math_std"] - wide["mean_verbal_std"]

    rows: list[dict[str, object]] = []
    anchor_map = {
        "reading": "math_minus_reading",
        "ppvt": "math_minus_ppvt",
        "mean_verbal": "math_minus_mean_verbal",
    }
    for age_bin, sub in wide.groupby("age_bin", observed=True):
        for anchor, col in anchor_map.items():
            rows.append(
                summarize_frame(
                    sub,
                    dataset="nlscya",
                    stage=str(age_bin),
                    anchor=anchor,
                    outcome="math_minus_anchor",
                    value_col=col,
                    weight_col="weight",
                )
            )
    for anchor, col in anchor_map.items():
        rows.append(
            summarize_frame(
                wide,
                dataset="nlscya",
                stage="pooled",
                anchor=anchor,
                outcome="math_minus_anchor",
                value_col=col,
                weight_col="weight",
            )
        )
    ppvt_overlap = wide.dropna(subset=["ppvt_std"]).copy()
    for anchor, col in {"reading": "math_minus_reading", "mean_verbal": "math_minus_mean_verbal"}.items():
        rows.append(
            summarize_frame(
                ppvt_overlap,
                dataset="nlscya",
                stage="pooled_ppvt_overlap",
                anchor=anchor,
                outcome="math_minus_anchor",
                value_col=col,
                weight_col="weight",
            )
        )
    return pd.DataFrame(rows)


def build_ffcws() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "ffcws" / "ffcws_achievement_extract.parquet").copy()
    rows = [
        summarize_frame(
            df,
            dataset="ffcws",
            stage="year9",
            anchor="passage",
            outcome="math_minus_anchor",
            value_col="applied_minus_passage",
            weight_col="p5natwt",
        ),
        summarize_frame(
            df,
            dataset="ffcws",
            stage="year9",
            anchor="ppvt",
            outcome="math_minus_anchor",
            value_col="applied_minus_ppvt",
            weight_col="p5natwt",
        ),
        summarize_frame(
            df,
            dataset="ffcws",
            stage="year9",
            anchor="mean_verbal",
            outcome="math_minus_anchor",
            value_col="applied_minus_mean_verbal",
            weight_col="p5natwt",
        ),
    ]
    return pd.DataFrame(rows)


def build_joint_models() -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    nlscya = pd.read_parquet(DATA_DIR / "nlscya" / "nlscya_early_school_panel.parquet").copy()
    nlscya_wide = (
        nlscya.pivot_table(
            index=["child_id", "wave", "female", "age_months", "weight", "age_bin"],
            columns="outcome",
            values="score",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    nlscya_joint = nlscya_wide.dropna(subset=["piat_math_std", "piat_reading_comp_std", "ppvt_std", "female", "weight", "age_bin"]).copy()
    nlscya_joint_model = smf.wls(
        "piat_math_std ~ female + piat_reading_comp_std + ppvt_std + C(age_bin)",
        data=nlscya_joint,
        weights=nlscya_joint["weight"],
    ).fit(cov_type="HC1")
    coef = nlscya_joint_model.params.get("female", math.nan)
    se = nlscya_joint_model.bse.get("female", math.nan)
    rows.append(
        {
            "dataset": "nlscya",
            "model_name": "math_on_joint_verbal",
            "n": int(nlscya_joint_model.nobs),
            "beta_female": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(nlscya_joint_model.rsquared),
        }
    )
    nlscya_wide["mean_verbal_std"] = safe_mean(nlscya_wide, ["piat_reading_comp_std", "ppvt_std"])
    nlscya_mean = nlscya_wide.dropna(subset=["piat_math_std", "mean_verbal_std", "female", "weight", "age_bin"]).copy()
    nlscya_mean_model = smf.wls(
        "piat_math_std ~ female + mean_verbal_std + C(age_bin)",
        data=nlscya_mean,
        weights=nlscya_mean["weight"],
    ).fit(cov_type="HC1")
    coef = nlscya_mean_model.params.get("female", math.nan)
    se = nlscya_mean_model.bse.get("female", math.nan)
    rows.append(
        {
            "dataset": "nlscya",
            "model_name": "math_on_mean_verbal",
            "n": int(nlscya_mean_model.nobs),
            "beta_female": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(nlscya_mean_model.rsquared),
        }
    )

    ffcws = pd.read_parquet(DATA_DIR / "ffcws" / "ffcws_achievement_extract.parquet").copy()
    ffcws_joint = ffcws.dropna(
        subset=[
            "ch5wj10_z",
            "ch5wj9_z",
            "ch5ppvt_z",
            "female",
            "ch5age_years",
            "cm1inpov",
            "mother_education_cat",
            "mother_race_cat",
            "family_structure",
        ]
    ).copy()
    ffcws_joint_model = smf.wls(
        "ch5wj10_z ~ female + ch5wj9_z + ch5ppvt_z + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure)",
        data=ffcws_joint,
        weights=ffcws_joint["p5natwt"],
    ).fit(cov_type="HC1")
    coef = ffcws_joint_model.params.get("female", math.nan)
    se = ffcws_joint_model.bse.get("female", math.nan)
    rows.append(
        {
            "dataset": "ffcws",
            "model_name": "applied_on_joint_verbal",
            "n": int(ffcws_joint_model.nobs),
            "beta_female": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(ffcws_joint_model.rsquared),
        }
    )
    ffcws["mean_verbal_z"] = safe_mean(ffcws, ["ch5wj9_z", "ch5ppvt_z"])
    ffcws_mean = ffcws.dropna(
        subset=[
            "ch5wj10_z",
            "mean_verbal_z",
            "female",
            "ch5age_years",
            "cm1inpov",
            "mother_education_cat",
            "mother_race_cat",
            "family_structure",
        ]
    ).copy()
    ffcws_mean_model = smf.wls(
        "ch5wj10_z ~ female + mean_verbal_z + ch5age_years + cm1inpov + C(mother_education_cat) + C(mother_race_cat) + C(family_structure)",
        data=ffcws_mean,
        weights=ffcws_mean["p5natwt"],
    ).fit(cov_type="HC1")
    coef = ffcws_mean_model.params.get("female", math.nan)
    se = ffcws_mean_model.bse.get("female", math.nan)
    rows.append(
        {
            "dataset": "ffcws",
            "model_name": "applied_on_mean_verbal",
            "n": int(ffcws_mean_model.nobs),
            "beta_female": coef,
            "se": se,
            "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
            "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
            "r_squared": float(ffcws_mean_model.rsquared),
        }
    )

    return pd.DataFrame(rows)


def build_compare(summary: pd.DataFrame, fe: pd.DataFrame) -> pd.DataFrame:
    pooled = summary.loc[summary["stage"] == "pooled"].copy()
    pooled["sign"] = np.sign(pooled["d_female_minus_male"]).map({-1.0: "male", 0.0: "zero", 1.0: "female"})
    pooled = pooled[["dataset", "anchor", "d_female_minus_male", "sign", "n"]]
    compare = pooled.pivot(index="anchor", columns="dataset", values="d_female_minus_male").reset_index()
    if not fe.empty:
        fe_small = fe[["anchor", "beta_female"]].rename(columns={"beta_female": "psid_family_fe_beta"})
        compare = compare.merge(fe_small, on="anchor", how="left")
    return compare.sort_values("anchor").reset_index(drop=True)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    psid_summary, psid_fe = build_psid()
    nlscya_summary = build_nlscya()
    ffcws_summary = build_ffcws()
    models = build_joint_models()

    summary = pd.concat([psid_summary, nlscya_summary, ffcws_summary], ignore_index=True)
    compare = build_compare(summary, psid_fe)

    summary.to_csv(SUMMARY_OUT, sep="\t", index=False)
    psid_fe.to_csv(FE_OUT, sep="\t", index=False)
    compare.to_csv(COMPARE_OUT, sep="\t", index=False)
    models.to_csv(MODELS_OUT, sep="\t", index=False)

    print(f"wrote {SUMMARY_OUT}")
    print(f"wrote {FE_OUT}")
    print(f"wrote {COMPARE_OUT}")
    print(f"wrote {MODELS_OUT}")


if __name__ == "__main__":
    main()
