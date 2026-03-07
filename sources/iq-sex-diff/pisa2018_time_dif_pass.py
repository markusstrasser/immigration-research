from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA_DIR = ROOT / "data" / "pisa"

EXTRACT_PATH = DATA_DIR / "pisa2018_math_item_extract.parquet"
ITEM_GAPS_PATH = DATA_DIR / "pisa2018_item_level_gaps.tsv"
PROXY_PATH = DATA_DIR / "pisa2018_unit_framework_proxy.tsv"
SCORE_PROCESS_PATH = DATA_DIR / "pisa2018_process_nuisance_item.tsv"

ITEM_OUT = DATA_DIR / "pisa2018_time_dif_item.tsv"
CONTENT_OUT = DATA_DIR / "pisa2018_time_dif_content_summary.tsv"
CONTEXT_OUT = DATA_DIR / "pisa2018_time_dif_context_summary.tsv"
CORR_OUT = DATA_DIR / "pisa2018_time_dif_score_time_relation.tsv"


def weighted_group_standardize(values: np.ndarray, groups: np.ndarray, weights: np.ndarray) -> np.ndarray:
    out = np.full(values.shape, np.nan, dtype=float)
    for group in pd.unique(groups):
        mask = groups == group
        x = values[mask]
        w = weights[mask]
        valid = ~np.isnan(x)
        if valid.sum() == 0:
            continue
        xv = x[valid]
        wv = w[valid]
        mean = np.average(xv, weights=wv)
        var = np.average((xv - mean) ** 2, weights=wv)
        sd = math.sqrt(var) if var > 0 else 1.0
        z = np.full(x.shape, np.nan, dtype=float)
        z[valid] = (xv - mean) / sd
        out[mask] = z
    return out


def weighted_demean(values: np.ndarray, groups: np.ndarray, weights: np.ndarray) -> np.ndarray:
    out = np.full(values.shape, np.nan, dtype=float)
    for group in pd.unique(groups):
        mask = groups == group
        x = values[mask]
        w = weights[mask]
        valid = ~np.isnan(x)
        if valid.sum() == 0:
            continue
        xv = x[valid]
        wv = w[valid]
        mean = np.average(xv, weights=wv)
        y = np.full(x.shape, np.nan, dtype=float)
        y[valid] = xv - mean
        out[mask] = y
    return out


def fit_time_model(
    log_time: np.ndarray,
    female: np.ndarray,
    match_score: np.ndarray,
    groups: np.ndarray,
    weights: np.ndarray,
) -> dict[str, float]:
    female_match = female * match_score
    y_dm = weighted_demean(log_time, groups, weights)
    female_dm = weighted_demean(female, groups, weights)
    match_dm = weighted_demean(match_score, groups, weights)
    female_match_dm = weighted_demean(female_match, groups, weights)
    valid = ~(np.isnan(y_dm) | np.isnan(female_dm) | np.isnan(match_dm) | np.isnan(female_match_dm))
    if valid.sum() == 0 or pd.Series(groups[valid]).nunique() < 10:
        return {}
    X = np.column_stack([female_dm[valid], match_dm[valid], female_match_dm[valid]])
    model = sm.WLS(y_dm[valid], X, weights=weights[valid]).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups[valid]},
    )
    return {
        "n_nonmissing": int(valid.sum()),
        "n_countries": int(pd.Series(groups[valid]).nunique()),
        "female_beta": float(model.params[0]),
        "female_se": float(model.bse[0]),
        "female_match_beta": float(model.params[2]),
        "female_match_se": float(model.bse[2]),
        "r_squared": float(model.rsquared),
    }


def summarize_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for key, sub in df.groupby(group_col, observed=True):
        weights = sub["n_nonmissing"].astype(float).to_numpy()
        rows.append(
            {
                group_col: key,
                "items": int(len(sub)),
                "units": int(sub["unit_id"].nunique()),
                "weighted_female_time_beta": float(np.average(sub["female_time_beta"], weights=weights)),
                "weighted_abs_female_time_beta": float(np.average(np.abs(sub["female_time_beta"]), weights=weights)),
                "weighted_female_match_beta": float(np.average(sub["female_match_beta"], weights=weights)),
                "female_slower_items": int((sub["female_time_beta"] > 0).sum()),
                "male_slower_items": int((sub["female_time_beta"] < 0).sum()),
            }
        )
    return pd.DataFrame(rows).sort_values(group_col).reset_index(drop=True)


def main() -> None:
    extract = pd.read_parquet(EXTRACT_PATH).copy()
    item_meta = pd.read_csv(ITEM_GAPS_PATH, sep="\t")
    proxy = pd.read_csv(PROXY_PATH, sep="\t")
    meta = item_meta.merge(proxy, on=["unit_id", "unit_label"], how="left", validate="many_to_one")
    score_process = pd.read_csv(SCORE_PROCESS_PATH, sep="\t")[["score_var", "uniform_beta_process"]]

    if "female" not in extract.columns:
        extract["female"] = extract["ST004D01T"].map({1: 1.0, 2: 0.0})

    groups = extract["CNT"].astype(str).to_numpy(dtype=object)
    weights = extract["W_FSTUWT"].to_numpy(dtype=float)
    female = extract["female"].to_numpy(dtype=float)

    score_cols = meta["score_var"].tolist()
    scores = extract[score_cols].to_numpy(dtype=float)
    observed = ~np.isnan(scores)
    zscores = np.full(scores.shape, np.nan, dtype=float)
    for j in range(scores.shape[1]):
        zscores[:, j] = weighted_group_standardize(scores[:, j], groups, weights)
    zfilled = np.where(observed, zscores, 0.0)
    total_sum = zfilled.sum(axis=1)
    total_count = observed.sum(axis=1).astype(float)

    family_lookup = meta["content_category"].fillna("unknown").to_numpy(dtype=object)
    family_masks = {family: (family_lookup == family) for family in pd.unique(family_lookup)}
    family_sum = {family: zfilled[:, mask].sum(axis=1) for family, mask in family_masks.items()}
    family_count = {family: observed[:, mask].sum(axis=1).astype(float) for family, mask in family_masks.items()}

    rows: list[dict[str, object]] = []
    for meta_row in meta.itertuples(index=False):
        family = meta_row.content_category if pd.notna(meta_row.content_category) else "unknown"
        score_count = total_count - family_count[family]
        score_out = np.full(total_sum.shape, np.nan, dtype=float)
        valid_score = score_count > 0
        score_out[valid_score] = (total_sum[valid_score] - family_sum[family][valid_score]) / score_count[valid_score]
        score_out_z = weighted_group_standardize(score_out, groups, weights)

        time_col = f"{meta_row.score_var[:-1]}TT"
        if time_col not in extract.columns:
            continue
        time_raw = extract[time_col].to_numpy(dtype=float)
        log_time = np.where(time_raw > 0, np.log1p(time_raw), np.nan)
        result = fit_time_model(log_time, female, score_out_z, groups, weights)
        if not result:
            continue
        rows.append(
            {
                "score_var": meta_row.score_var,
                "unit_id": meta_row.unit_id,
                "question_id": meta_row.question_id,
                "unit_label": meta_row.unit_label,
                "content_category": meta_row.content_category,
                "context_category": meta_row.context_category,
                "female_time_beta": result["female_beta"],
                "female_time_se": result["female_se"],
                "female_match_beta": result["female_match_beta"],
                "female_match_se": result["female_match_se"],
                "n_nonmissing": result["n_nonmissing"],
                "n_countries": result["n_countries"],
                "r_squared": result["r_squared"],
            }
        )

    item_df = pd.DataFrame(rows).merge(score_process, on="score_var", how="left", validate="one_to_one")
    item_df["score_time_sign_agree"] = np.sign(item_df["female_time_beta"]) == np.sign(item_df["uniform_beta_process"])
    item_df.to_csv(ITEM_OUT, sep="\t", index=False)

    content_df = summarize_group(item_df, "content_category")
    content_df.to_csv(CONTENT_OUT, sep="\t", index=False)

    context_df = summarize_group(item_df, "context_category")
    context_df.to_csv(CONTEXT_OUT, sep="\t", index=False)

    corr_df = pd.DataFrame(
        [
            {
                "metric_x": "female_time_beta",
                "metric_y": "uniform_beta_process",
                "pearson_corr": float(item_df["female_time_beta"].corr(item_df["uniform_beta_process"])),
                "n_items": int(len(item_df)),
                "sign_agreement_rate": float(item_df["score_time_sign_agree"].mean()),
            }
        ]
    )
    corr_df.to_csv(CORR_OUT, sep="\t", index=False)


if __name__ == "__main__":
    main()
