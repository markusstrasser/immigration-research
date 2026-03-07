#!/usr/bin/env python3
"""First-pass PSID TAS transition summaries."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "psid"
PANEL_PATH = DATA_DIR / "psid_tas_panel.parquet"

WAVE_OUT = DATA_DIR / "psid_tas_wave_surface_gaps.tsv"
BEST_OUT = DATA_DIR / "psid_tas_best_surface_gaps.tsv"
ALIGNED_OUT = DATA_DIR / "psid_tas_aligned_gaps.tsv"
FAMILY_OUT = DATA_DIR / "psid_tas_family_fe.tsv"


def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").where(lambda s: s >= 0)


def within(series: pd.Series, lo: float, hi: float) -> pd.Series:
    values = clean_numeric(series)
    return values.where((values >= lo) & (values <= hi))


def load_panel() -> pd.DataFrame:
    df = pd.read_parquet(PANEL_PATH).copy()
    df["female"] = clean_numeric(df["female"])
    df["cross_weight"] = clean_numeric(df["cross_weight"])
    df["prior_cds_tas_weight"] = clean_numeric(df["prior_cds_tas_weight"])
    df["analysis_weight"] = df["cross_weight"].where(df["cross_weight"] > 0)
    df["analysis_weight"] = df["analysis_weight"].fillna(
        df["prior_cds_tas_weight"].where(df["prior_cds_tas_weight"] > 0)
    )
    df["age_years"] = within(df["age_years"], 15, 40)
    df["hs_grad"] = clean_numeric(df["hs_grad"])
    df["took_sat_act"] = clean_numeric(df["took_sat_act"])
    df["hs_gpa"] = within(df["hs_gpa"], 0, 20)
    df["hs_gpa_max"] = within(df["hs_gpa_max"], 1, 20)
    df["sat_math"] = within(df["sat_math"], 100, 800)
    df["sat_reading"] = within(df["sat_reading"], 100, 800)
    df["act_composite"] = within(df["act_composite"], 1, 36)
    df["college_gpa_actual"] = clean_numeric(df["college_gpa_y"]).fillna(clean_numeric(df["college_gpa_k"]))
    df["college_gpa_max"] = clean_numeric(df["college_gpa_max_z"]).fillna(clean_numeric(df["college_gpa_max_m"]))
    df["college_gpa_actual"] = df["college_gpa_actual"].where(lambda s: (s >= 0) & (s <= 20))
    df["college_gpa_max"] = df["college_gpa_max"].where(lambda s: (s >= 1) & (s <= 20))
    df["hs_gpa_norm"] = (df["hs_gpa"] / df["hs_gpa_max"]).where(df["hs_gpa_max"] > 0)
    df["college_gpa_norm"] = (df["college_gpa_actual"] / df["college_gpa_max"]).where(df["college_gpa_max"] > 0)
    return df


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


def weighted_gap(values: np.ndarray, female: np.ndarray, weights: np.ndarray) -> tuple[float, float, float]:
    positive = weights > 0
    values = values[positive]
    female = female[positive]
    weights = weights[positive]
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


def summarize(df: pd.DataFrame, group_cols: list[str], outcomes: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, sub in df.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        base = {col: key for col, key in zip(group_cols, keys, strict=True)}
        for outcome in outcomes:
            work = sub.dropna(subset=[outcome, "female", "analysis_weight"]).copy()
            work = work[work["analysis_weight"] > 0].copy()
            if work.empty:
                continue
            values = work[outcome].to_numpy(dtype=float)
            female = work["female"].to_numpy(dtype=int)
            weights = work["analysis_weight"].to_numpy(dtype=float)
            mean_f, mean_m, d = weighted_gap(values, female, weights)
            row = dict(base)
            row.update(
                {
                    "outcome": outcome,
                    "n": int(len(work)),
                    "families68": int(work["family_id68"].nunique()),
                    "female_mean": mean_f,
                    "male_mean": mean_m,
                    "d_female_minus_male": d,
                    "mean_age_years": float(np.average(work["age_years"], weights=work["analysis_weight"])),
                }
            )
            rows.append(row)
    return pd.DataFrame(rows)


def latest_best(df: pd.DataFrame, outcomes: list[str]) -> pd.DataFrame:
    base = (
        df.sort_values(["pair_id68", "wave"])
        .dropna(subset=["pair_id68"])
        .groupby("pair_id68", as_index=False)
        .tail(1)
        .copy()
    )
    base = base[
        ["pair_id68", "family_id68", "person_id68", "female", "age_years", "analysis_weight", "wave"]
    ].rename(
        columns={"wave": "latest_wave"}
    )
    for outcome in outcomes:
        temp = (
            df.dropna(subset=[outcome, "pair_id68"])
            .sort_values(["pair_id68", "wave"])
            .groupby("pair_id68", as_index=False)
            .tail(1)[["pair_id68", "wave", outcome]]
            .rename(columns={"wave": f"{outcome}_wave"})
        )
        base = base.merge(temp, on="pair_id68", how="left")
    return base


def weighted_z(series: pd.Series, weights: pd.Series) -> pd.Series:
    work = pd.DataFrame({"x": series, "w": weights}).dropna()
    work = work[work["w"] > 0]
    if work.empty:
        return pd.Series(index=series.index, dtype=float)
    mean = weighted_mean(work["x"].to_numpy(dtype=float), work["w"].to_numpy(dtype=float))
    var = weighted_var(work["x"].to_numpy(dtype=float), work["w"].to_numpy(dtype=float))
    sd = math.sqrt(var) if var > 0 else math.nan
    if not math.isfinite(sd) or sd == 0:
        return pd.Series(index=series.index, dtype=float)
    return (series - mean) / sd


def build_aligned(best: pd.DataFrame) -> pd.DataFrame:
    out = best.copy()
    out["hs_gpa_norm_z"] = weighted_z(out["hs_gpa_norm"], out["analysis_weight"])
    out["college_gpa_norm_z"] = weighted_z(out["college_gpa_norm"], out["analysis_weight"])
    out["sat_math_z"] = weighted_z(out["sat_math"], out["analysis_weight"])
    out["sat_reading_z"] = weighted_z(out["sat_reading"], out["analysis_weight"])
    out["hs_gpa_minus_sat_math_z"] = out["hs_gpa_norm_z"] - out["sat_math_z"]
    out["college_gpa_minus_sat_math_z"] = out["college_gpa_norm_z"] - out["sat_math_z"]
    out["sat_math_minus_reading_z"] = out["sat_math_z"] - out["sat_reading_z"]
    return out


def family_fe(best: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome in ["hs_gpa_minus_sat_math_z", "college_gpa_minus_sat_math_z", "sat_math_minus_reading_z"]:
        work = best.dropna(subset=[outcome, "family_id68", "female", "age_years", "analysis_weight"]).copy()
        work = work[work["analysis_weight"] > 0].copy()
        family_counts = work.groupby("family_id68")["person_id68"].nunique()
        work = work[work["family_id68"].isin(family_counts[family_counts >= 2].index)].copy()
        if work.empty:
            continue
        model = smf.wls(
            f"{outcome} ~ female + age_years + C(family_id68)",
            data=work,
            weights=work["analysis_weight"],
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
    raw_outcomes = ["hs_gpa_norm", "sat_math", "sat_reading", "act_composite", "college_gpa_norm"]
    df = load_panel()
    wave_summary = summarize(df, ["wave"], raw_outcomes).sort_values(["wave", "outcome"])

    best = latest_best(df, raw_outcomes)
    best_summary = summarize(best.assign(panel="best"), ["panel"], raw_outcomes).sort_values(["panel", "outcome"])

    aligned = build_aligned(best)
    aligned_summary = summarize(
        aligned.assign(panel="best"),
        ["panel"],
        ["hs_gpa_minus_sat_math_z", "college_gpa_minus_sat_math_z", "sat_math_minus_reading_z"],
    ).sort_values(["panel", "outcome"])
    family = family_fe(aligned)

    wave_summary.to_csv(WAVE_OUT, sep="\t", index=False)
    best_summary.to_csv(BEST_OUT, sep="\t", index=False)
    aligned_summary.to_csv(ALIGNED_OUT, sep="\t", index=False)
    family.to_csv(FAMILY_OUT, sep="\t", index=False)

    print(f"wrote {WAVE_OUT}")
    print(f"wrote {BEST_OUT}")
    print(f"wrote {ALIGNED_OUT}")
    print(f"wrote {FAMILY_OUT}")


if __name__ == "__main__":
    main()
