from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "pisa"

EXTRACT_PATH = DATA_DIR / "pisa2018_math_item_extract.parquet"
ITEM_GAPS_PATH = DATA_DIR / "pisa2018_item_level_gaps.tsv"
PROXY_PATH = DATA_DIR / "pisa2018_unit_framework_proxy.tsv"
LEAVEOUT_CONTENT_PATH = DATA_DIR / "pisa2018_dif_leaveout_content_summary.tsv"

ITEM_OUT = DATA_DIR / "pisa2018_process_nuisance_item.tsv"
CONTENT_OUT = DATA_DIR / "pisa2018_process_nuisance_content_summary.tsv"
CONTEXT_OUT = DATA_DIR / "pisa2018_process_nuisance_context_summary.tsv"


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    values = values[order]
    weights = weights[order]
    cum_weights = np.cumsum(weights)
    cutoff = quantile * weights.sum()
    idx = np.searchsorted(cum_weights, cutoff, side="left")
    idx = min(max(idx, 0), len(values) - 1)
    return float(values[idx])


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


def fit_item_model(
    y: np.ndarray,
    female: np.ndarray,
    match_score: np.ndarray,
    groups: np.ndarray,
    weights: np.ndarray,
    process_time: np.ndarray | None = None,
    process_visit: np.ndarray | None = None,
    process_count: np.ndarray | None = None,
) -> dict[str, float]:
    female_match = female * match_score
    y_dm = weighted_demean(y, groups, weights)
    female_dm = weighted_demean(female, groups, weights)
    match_dm = weighted_demean(match_score, groups, weights)
    female_match_dm = weighted_demean(female_match, groups, weights)

    design = [female_dm, match_dm, female_match_dm]
    names = ["female", "match", "female_match"]

    if process_time is not None:
        female_time = female * process_time
        female_visit = female * process_visit
        design.extend(
            [
                weighted_demean(process_time, groups, weights),
                weighted_demean(process_visit, groups, weights),
                weighted_demean(process_count, groups, weights),
                weighted_demean(female_time, groups, weights),
                weighted_demean(female_visit, groups, weights),
            ]
        )
        names.extend(["process_time", "process_visit", "process_count", "female_time", "female_visit"])

    valid = ~np.isnan(y_dm)
    for col in design:
        valid &= ~np.isnan(col)
    if valid.sum() == 0 or pd.Series(groups[valid]).nunique() < 10:
        return {}

    X = np.column_stack([col[valid] for col in design])
    model = sm.WLS(y_dm[valid], X, weights=weights[valid]).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups[valid]},
    )

    out: dict[str, float] = {
        "n_nonmissing": int(valid.sum()),
        "n_countries": int(pd.Series(groups[valid]).nunique()),
        "r_squared": float(model.rsquared),
    }
    for idx, name in enumerate(names):
        out[f"{name}_beta"] = float(model.params[idx])
        out[f"{name}_se"] = float(model.bse[idx])
    return out


def summarize_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for key, sub in df.groupby(group_col, observed=True):
        weights = sub["n_nonmissing_same_sample"].astype(float).to_numpy()
        abs_base = np.abs(sub["uniform_beta_base_same_sample"].to_numpy(dtype=float))
        abs_process = np.abs(sub["uniform_beta_process"].to_numpy(dtype=float))
        reduction = abs_base - abs_process
        row = {
            group_col: key,
            "items": int(len(sub)),
            "units": int(sub["unit_id"].nunique()),
            "weighted_raw_gap_d": float(np.average(sub["country_weighted_mean_d"], weights=weights)),
            "weighted_uniform_beta_base_same_sample": float(
                np.average(sub["uniform_beta_base_same_sample"], weights=weights)
            ),
            "weighted_uniform_beta_process": float(np.average(sub["uniform_beta_process"], weights=weights)),
            "weighted_uniform_beta_process_trimmed": float(
                np.average(sub["uniform_beta_process_trimmed"], weights=weights)
            ),
            "weighted_abs_base": float(np.average(abs_base, weights=weights)),
            "weighted_abs_process": float(np.average(abs_process, weights=weights)),
            "weighted_abs_reduction": float(np.average(reduction, weights=weights)),
            "items_reduced_abs_gap": int((reduction > 0).sum()),
            "items_increased_abs_gap": int((reduction < 0).sum()),
        }
        rows.append(row)
    return pd.DataFrame(rows).sort_values(group_col).reset_index(drop=True)


def main() -> None:
    extract = pd.read_parquet(EXTRACT_PATH).copy()
    item_meta = pd.read_csv(ITEM_GAPS_PATH, sep="\t")
    proxy = pd.read_csv(PROXY_PATH, sep="\t")
    meta = item_meta.merge(proxy, on=["unit_id", "unit_label"], how="left", validate="many_to_one")

    if "female" not in extract.columns:
        extract["female"] = extract["ST004D01T"].map({1: 1.0, 2: 0.0})

    extract["CNT"] = extract["CNT"].astype(str)
    groups = extract["CNT"].to_numpy(dtype=object)
    weights = extract["W_FSTUWT"].to_numpy(dtype=float)
    female = extract["female"].to_numpy(dtype=float)

    score_cols = meta["score_var"].tolist()
    score_idx = {c: i for i, c in enumerate(score_cols)}
    scores = extract[score_cols].to_numpy(dtype=float)
    observed_score = ~np.isnan(scores)
    zscores = np.full(scores.shape, np.nan, dtype=float)
    for j in range(scores.shape[1]):
        zscores[:, j] = weighted_group_standardize(scores[:, j], groups, weights)
    zfilled = np.where(observed_score, zscores, 0.0)
    total_score_sum = zfilled.sum(axis=1)
    total_score_count = observed_score.sum(axis=1).astype(float)

    time_cols = [f"{c[:-1]}TT" for c in score_cols]
    visit_cols = [f"{c[:-1]}V" for c in score_cols]
    times_raw = extract[time_cols].to_numpy(dtype=float)
    visits_raw = extract[visit_cols].to_numpy(dtype=float)

    time_log = np.where(times_raw > 0, np.log1p(times_raw), np.nan)
    time_z = np.full(time_log.shape, np.nan, dtype=float)
    visit_z = np.full(visits_raw.shape, np.nan, dtype=float)
    for j in range(time_log.shape[1]):
        time_z[:, j] = weighted_group_standardize(time_log[:, j], groups, weights)
        visit_z[:, j] = weighted_group_standardize(visits_raw[:, j], groups, weights)

    observed_time = ~np.isnan(time_z)
    observed_visit = ~np.isnan(visit_z)
    time_filled = np.where(observed_time, time_z, 0.0)
    visit_filled = np.where(observed_visit, visit_z, 0.0)
    total_time_sum = time_filled.sum(axis=1)
    total_time_count = observed_time.sum(axis=1).astype(float)
    total_visit_sum = visit_filled.sum(axis=1)
    total_visit_count = observed_visit.sum(axis=1).astype(float)

    family_lookup = meta["content_category"].fillna("unknown").to_numpy(dtype=object)
    family_masks = {family: (family_lookup == family) for family in pd.unique(family_lookup)}

    family_score_sum = {family: zfilled[:, mask].sum(axis=1) for family, mask in family_masks.items()}
    family_score_count = {family: observed_score[:, mask].sum(axis=1).astype(float) for family, mask in family_masks.items()}
    family_time_sum = {family: time_filled[:, mask].sum(axis=1) for family, mask in family_masks.items()}
    family_time_count = {family: observed_time[:, mask].sum(axis=1).astype(float) for family, mask in family_masks.items()}
    family_visit_sum = {family: visit_filled[:, mask].sum(axis=1) for family, mask in family_masks.items()}
    family_visit_count = {family: observed_visit[:, mask].sum(axis=1).astype(float) for family, mask in family_masks.items()}

    rows: list[dict[str, object]] = []
    for meta_row in meta.itertuples(index=False):
        j = score_idx[meta_row.score_var]
        family = meta_row.content_category if pd.notna(meta_row.content_category) else "unknown"

        y = scores[:, j]
        score_out = np.full(total_score_sum.shape, np.nan, dtype=float)
        score_count = total_score_count - family_score_count[family]
        valid_score = score_count > 0
        score_out[valid_score] = (total_score_sum[valid_score] - family_score_sum[family][valid_score]) / score_count[valid_score]
        score_out_z = weighted_group_standardize(score_out, groups, weights)

        time_out = np.full(total_time_sum.shape, np.nan, dtype=float)
        time_count = total_time_count - family_time_count[family]
        valid_time = time_count > 0
        time_out[valid_time] = (total_time_sum[valid_time] - family_time_sum[family][valid_time]) / time_count[valid_time]
        time_out_z = weighted_group_standardize(time_out, groups, weights)

        visit_out = np.full(total_visit_sum.shape, np.nan, dtype=float)
        visit_count = total_visit_count - family_visit_count[family]
        valid_visit = visit_count > 0
        visit_out[valid_visit] = (total_visit_sum[valid_visit] - family_visit_sum[family][valid_visit]) / visit_count[valid_visit]
        visit_out_z = weighted_group_standardize(visit_out, groups, weights)

        count_out_z = weighted_group_standardize(score_count, groups, weights)

        same_sample = ~(np.isnan(y) | np.isnan(score_out_z) | np.isnan(time_out_z) | np.isnan(visit_out_z) | np.isnan(count_out_z))
        base_same_sample = fit_item_model(
            y[same_sample],
            female[same_sample],
            score_out_z[same_sample],
            groups[same_sample],
            weights[same_sample],
        )
        process_model = fit_item_model(
            y[same_sample],
            female[same_sample],
            score_out_z[same_sample],
            groups[same_sample],
            weights[same_sample],
            process_time=time_out_z[same_sample],
            process_visit=visit_out_z[same_sample],
            process_count=count_out_z[same_sample],
        )

        time_col = f"{meta_row.score_var[:-1]}TT"
        trim_keep = same_sample.copy()
        if time_col in extract.columns:
            focal_time = extract[time_col].to_numpy(dtype=float)
            focal_valid = same_sample & (~np.isnan(focal_time)) & (focal_time > 0)
            if focal_valid.sum() >= 500:
                cutoff = weighted_quantile(focal_time[focal_valid], weights[focal_valid], 0.10)
                trim_keep &= (np.isnan(focal_time) | (focal_time >= cutoff))
        process_trimmed = fit_item_model(
            y[trim_keep],
            female[trim_keep],
            score_out_z[trim_keep],
            groups[trim_keep],
            weights[trim_keep],
            process_time=time_out_z[trim_keep],
            process_visit=visit_out_z[trim_keep],
            process_count=count_out_z[trim_keep],
        )

        rows.append(
            {
                "score_var": meta_row.score_var,
                "unit_id": meta_row.unit_id,
                "question_id": meta_row.question_id,
                "unit_label": meta_row.unit_label,
                "content_category": meta_row.content_category,
                "context_category": meta_row.context_category,
                "unit_family": meta_row.unit_family,
                "score_family": meta_row.score_family,
                "max_score": meta_row.max_score,
                "country_weighted_mean_d": float(meta_row.country_weighted_mean_d),
                "n_nonmissing_same_sample": base_same_sample.get("n_nonmissing", 0),
                "n_countries_same_sample": base_same_sample.get("n_countries", 0),
                "uniform_beta_base_same_sample": base_same_sample.get("female_beta", np.nan),
                "uniform_se_base_same_sample": base_same_sample.get("female_se", np.nan),
                "uniform_beta_process": process_model.get("female_beta", np.nan),
                "uniform_se_process": process_model.get("female_se", np.nan),
                "uniform_beta_process_trimmed": process_trimmed.get("female_beta", np.nan),
                "uniform_se_process_trimmed": process_trimmed.get("female_se", np.nan),
                "female_match_beta_process": process_model.get("female_match_beta", np.nan),
                "female_time_beta_process": process_model.get("female_time_beta", np.nan),
                "female_visit_beta_process": process_model.get("female_visit_beta", np.nan),
                "time_beta_process": process_model.get("process_time_beta", np.nan),
                "visit_beta_process": process_model.get("process_visit_beta", np.nan),
                "count_beta_process": process_model.get("process_count_beta", np.nan),
                "r_squared_base_same_sample": base_same_sample.get("r_squared", np.nan),
                "r_squared_process": process_model.get("r_squared", np.nan),
                "abs_gap_reduction": (
                    abs(base_same_sample.get("female_beta", np.nan)) - abs(process_model.get("female_beta", np.nan))
                    if base_same_sample and process_model
                    else np.nan
                ),
            }
        )

    item_df = pd.DataFrame(rows)
    item_df.to_csv(ITEM_OUT, sep="\t", index=False)

    content_df = summarize_group(item_df.dropna(subset=["uniform_beta_base_same_sample", "uniform_beta_process"]), "content_category")
    content_df.to_csv(CONTENT_OUT, sep="\t", index=False)

    context_df = summarize_group(item_df.dropna(subset=["uniform_beta_base_same_sample", "uniform_beta_process"]), "context_category")
    context_df.to_csv(CONTEXT_OUT, sep="\t", index=False)


if __name__ == "__main__":
    main()
