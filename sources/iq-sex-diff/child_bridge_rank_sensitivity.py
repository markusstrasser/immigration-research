#!/usr/bin/env python3
"""Rank-based child bridge sensitivity across public cohorts."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA_DIR = ROOT / "data"
OUT_DIR = DATA_DIR / "child_bridge_rank"

SUMMARY_OUT = OUT_DIR / "child_bridge_rank_summary.tsv"
FE_OUT = OUT_DIR / "child_bridge_rank_family_fe.tsv"


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
    vf = values[mask_f]
    vm = values[mask_m]
    wf = weights[mask_f]
    wm = weights[mask_m]
    mean_f = weighted_mean(vf, wf)
    mean_m = weighted_mean(vm, wm)
    pooled = math.sqrt(max((weighted_var(vf, wf) + weighted_var(vm, wm)) / 2.0, 0.0))
    d = (mean_f - mean_m) / pooled if pooled > 0 else math.nan
    return mean_f, mean_m, d


def weighted_percentile_rank(values: pd.Series, weights: pd.Series) -> pd.Series:
    work = pd.DataFrame({"value": values, "weight": weights}).dropna().copy()
    if work.empty:
        return pd.Series(np.nan, index=values.index, dtype=float)
    work = work.sort_values(["value", "weight"]).reset_index()
    total = work["weight"].sum()
    work["cum"] = work["weight"].cumsum()
    work["rank"] = (work["cum"] - 0.5 * work["weight"]) / total
    out = pd.Series(np.nan, index=values.index, dtype=float)
    out.loc[work["index"]] = work["rank"].to_numpy(dtype=float)
    return out


def safe_mean(frame: pd.DataFrame, cols: list[str]) -> pd.Series:
    return frame[cols].mean(axis=1, skipna=True)


def summarize(frame: pd.DataFrame, dataset: str, stage: str, anchor: str) -> dict[str, object]:
    sub = frame.dropna(subset=["rank_gap", "female", "weight"]).copy()
    f, m, d = weighted_gap(
        sub["rank_gap"].to_numpy(dtype=float),
        sub["female"].to_numpy(dtype=int),
        sub["weight"].to_numpy(dtype=float),
    )
    out: dict[str, object] = {
        "dataset": dataset,
        "stage": stage,
        "anchor": anchor,
        "n": int(len(sub)),
        "female_mean": f,
        "male_mean": m,
        "d_female_minus_male": d,
    }
    if "family_id68" in sub.columns:
        out["families"] = int(sub["family_id68"].nunique())
    return out


def psid_rank() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(DATA_DIR / "psid" / "psid_cds_panel.parquet").copy()
    df["weight"] = clean_score(df["child_weight"]).fillna(1.0)
    df["age_years"] = clean_score(df["age_years"])
    for col in ["applied_problems_std", "broad_reading_std", "letter_word_std", "passage_comp_std"]:
        df[col] = clean_score(df[col])
    df["mean_verbal_std"] = safe_mean(df, ["letter_word_std", "passage_comp_std"])
    anchor_map = {
        "broad_reading": "broad_reading_std",
        "letter_word": "letter_word_std",
        "passage": "passage_comp_std",
        "mean_verbal": "mean_verbal_std",
    }

    rows: list[dict[str, object]] = []
    fe_rows: list[dict[str, object]] = []

    pooled_frames: list[pd.DataFrame] = []
    for wave, wave_df in df.groupby("wave", observed=True):
        for anchor, anchor_col in anchor_map.items():
            sub = wave_df.dropna(subset=["applied_problems_std", anchor_col, "female", "weight"]).copy()
            if sub.empty:
                continue
            sub["math_rank"] = weighted_percentile_rank(sub["applied_problems_std"], sub["weight"])
            sub["anchor_rank"] = weighted_percentile_rank(sub[anchor_col], sub["weight"])
            sub["rank_gap"] = sub["math_rank"] - sub["anchor_rank"]
            sub["anchor"] = anchor
            rows.append(summarize(sub, "psid_cds", str(wave), anchor))
            pooled_frames.append(sub[["family_id68", "pair_id68", "female", "weight", "age_years", "rank_gap", "anchor", "wave"]].copy())

    pooled = pd.concat(pooled_frames, ignore_index=True)
    for anchor, sub in pooled.groupby("anchor", observed=True):
        rows.append(summarize(sub, "psid_cds", "pooled", anchor))
        work = sub.dropna(subset=["family_id68", "age_years"]).copy()
        family_counts = work.groupby("family_id68")["pair_id68"].nunique()
        work = work[work["family_id68"].isin(family_counts[family_counts >= 2].index)].copy()
        model = smf.wls(
            "rank_gap ~ female + age_years + C(wave) + C(family_id68)",
            data=work,
            weights=work["weight"],
        ).fit(cov_type="cluster", cov_kwds={"groups": work["family_id68"]})
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        fe_rows.append(
            {
                "dataset": "psid_cds",
                "anchor": anchor,
                "n": int(model.nobs),
                "families": int(work["family_id68"].nunique()),
                "beta_female": coef,
                "se": se,
                "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                "r_squared": float(model.rsquared),
            }
        )

    return pd.DataFrame(rows), pd.DataFrame(fe_rows)


def nlscya_rank() -> pd.DataFrame:
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
    wide["mean_verbal_std"] = safe_mean(wide, ["piat_reading_comp_std", "ppvt_std"])
    anchor_map = {
        "reading": "piat_reading_comp_std",
        "ppvt": "ppvt_std",
        "mean_verbal": "mean_verbal_std",
    }

    rows: list[dict[str, object]] = []
    pooled_frames: list[pd.DataFrame] = []
    for age_bin, age_df in wide.groupby("age_bin", observed=True):
        for anchor, anchor_col in anchor_map.items():
            sub = age_df.dropna(subset=["piat_math_std", anchor_col, "female", "weight"]).copy()
            if sub.empty:
                continue
            sub["math_rank"] = weighted_percentile_rank(sub["piat_math_std"], sub["weight"])
            sub["anchor_rank"] = weighted_percentile_rank(sub[anchor_col], sub["weight"])
            sub["rank_gap"] = sub["math_rank"] - sub["anchor_rank"]
            sub["anchor"] = anchor
            rows.append(summarize(sub, "nlscya", str(age_bin), anchor))
            pooled_frames.append(sub[["female", "weight", "rank_gap", "anchor"]].copy())

    pooled = pd.concat(pooled_frames, ignore_index=True)
    for anchor, sub in pooled.groupby("anchor", observed=True):
        rows.append(summarize(sub, "nlscya", "pooled", anchor))
    return pd.DataFrame(rows)


def ffcws_rank() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "ffcws" / "ffcws_achievement_extract.parquet").copy()
    df["mean_verbal_z"] = safe_mean(df, ["ch5wj9_z", "ch5ppvt_z"])
    anchor_map = {
        "passage": "ch5wj9_z",
        "ppvt": "ch5ppvt_z",
        "mean_verbal": "mean_verbal_z",
    }
    rows: list[dict[str, object]] = []
    for anchor, anchor_col in anchor_map.items():
        sub = df.dropna(subset=["ch5wj10_z", anchor_col, "female", "p5natwt"]).copy()
        sub["weight"] = sub["p5natwt"]
        sub["math_rank"] = weighted_percentile_rank(sub["ch5wj10_z"], sub["weight"])
        sub["anchor_rank"] = weighted_percentile_rank(sub[anchor_col], sub["weight"])
        sub["rank_gap"] = sub["math_rank"] - sub["anchor_rank"]
        rows.append(summarize(sub, "ffcws", "year9", anchor))
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    psid_summary, psid_fe = psid_rank()
    nlscya_summary = nlscya_rank()
    ffcws_summary = ffcws_rank()
    summary = pd.concat([psid_summary, nlscya_summary, ffcws_summary], ignore_index=True)
    summary.to_csv(SUMMARY_OUT, sep="\t", index=False)
    psid_fe.to_csv(FE_OUT, sep="\t", index=False)
    print(f"wrote {SUMMARY_OUT}")
    print(f"wrote {FE_OUT}")


if __name__ == "__main__":
    main()
