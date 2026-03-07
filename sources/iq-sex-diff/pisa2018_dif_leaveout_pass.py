from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

from pisa_utils import weighted_demean, weighted_group_standardize


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "pisa"

EXTRACT_PATH = DATA_DIR / "pisa2018_math_item_extract.parquet"
ITEM_GAPS_PATH = DATA_DIR / "pisa2018_item_level_gaps.tsv"
PROXY_PATH = DATA_DIR / "pisa2018_unit_framework_proxy.tsv"

DIF_OUT = DATA_DIR / "pisa2018_item_dif_leaveout.tsv"
CONTENT_OUT = DATA_DIR / "pisa2018_dif_leaveout_content_summary.tsv"
CONTEXT_OUT = DATA_DIR / "pisa2018_dif_leaveout_context_summary.tsv"
ANCHOR_OUT = DATA_DIR / "pisa2018_dif_leaveout_anchor_candidates.tsv"


def weighted_quantile(values: np.ndarray, weights: np.ndarray, quantile: float) -> float:
    order = np.argsort(values)
    values = values[order]
    weights = weights[order]
    cum_weights = np.cumsum(weights)
    cutoff = quantile * weights.sum()
    idx = np.searchsorted(cum_weights, cutoff, side="left")
    idx = min(max(idx, 0), len(values) - 1)
    return float(values[idx])


def classify_strength(beta: float) -> str:
    mag = abs(beta)
    if mag >= 0.08:
        return "large"
    if mag >= 0.04:
        return "moderate"
    if mag >= 0.02:
        return "small"
    return "near_zero"


def fit_item_model(
    y: np.ndarray,
    female: np.ndarray,
    match_score: np.ndarray,
    groups: np.ndarray,
    weights: np.ndarray,
) -> dict[str, float]:
    female_math = female * match_score
    y_dm = weighted_demean(y, groups, weights)
    female_dm = weighted_demean(female, groups, weights)
    match_dm = weighted_demean(match_score, groups, weights)
    female_math_dm = weighted_demean(female_math, groups, weights)

    valid = ~(np.isnan(y_dm) | np.isnan(female_dm) | np.isnan(match_dm) | np.isnan(female_math_dm))
    if valid.sum() == 0 or pd.Series(groups[valid]).nunique() < 10:
        return {}

    X = np.column_stack([female_dm[valid], match_dm[valid], female_math_dm[valid]])
    model = sm.WLS(y_dm[valid], X, weights=weights[valid]).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups[valid]},
    )
    return {
        "n_nonmissing": int(valid.sum()),
        "n_countries": int(pd.Series(groups[valid]).nunique()),
        "uniform_female_beta": float(model.params[0]),
        "uniform_female_se": float(model.bse[0]),
        "nonuniform_female_match_beta": float(model.params[2]),
        "nonuniform_female_match_se": float(model.bse[2]),
        "r_squared": float(model.rsquared),
    }


def summarize_group(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for key, sub in df.groupby(group_col, observed=True):
        weights = sub["n_nonmissing_core"].astype(float).to_numpy()
        row = {
            group_col: key,
            "items": int(len(sub)),
            "units": int(sub["unit_id"].nunique()),
            "weighted_raw_gap_d": float(np.average(sub["country_weighted_mean_d"], weights=weights)),
            "weighted_uniform_beta_item_out": float(np.average(sub["uniform_beta_item_out"], weights=weights)),
            "weighted_uniform_beta_family_out": float(np.average(sub["uniform_beta_family_out"], weights=weights)),
            "weighted_uniform_beta_family_out_trimmed": float(
                np.average(sub["uniform_beta_family_out_trimmed"], weights=weights)
            ),
            "weighted_abs_uniform_beta_item_out": float(np.average(np.abs(sub["uniform_beta_item_out"]), weights=weights)),
            "weighted_abs_uniform_beta_family_out": float(
                np.average(np.abs(sub["uniform_beta_family_out"]), weights=weights)
            ),
            "weighted_abs_uniform_beta_family_out_trimmed": float(
                np.average(np.abs(sub["uniform_beta_family_out_trimmed"]), weights=weights)
            ),
            "male_positive_item_out": int((sub["uniform_beta_item_out"] < 0).sum()),
            "male_positive_family_out": int((sub["uniform_beta_family_out"] < 0).sum()),
            "male_positive_trimmed": int((sub["uniform_beta_family_out_trimmed"] < 0).sum()),
        }
        rows.append(row)
    return pd.DataFrame(rows).sort_values(group_col).reset_index(drop=True)


def main() -> None:
    extract = pd.read_parquet(EXTRACT_PATH).copy()
    item_meta = pd.read_csv(ITEM_GAPS_PATH, sep="\t")
    proxy = pd.read_csv(PROXY_PATH, sep="\t")
    meta = item_meta.merge(proxy, on=["unit_id", "unit_label"], how="left", validate="many_to_one")

    extract["CNT"] = extract["CNT"].astype(str)
    if "female" not in extract.columns:
        extract["female"] = extract["ST004D01T"].map({1: 1.0, 2: 0.0})

    score_cols = meta["score_var"].tolist()
    scores = extract[score_cols].to_numpy(dtype=float)
    groups = extract["CNT"].to_numpy(dtype=object)
    weights = extract["W_FSTUWT"].to_numpy(dtype=float)
    female = extract["female"].to_numpy(dtype=float)

    zscores = np.full(scores.shape, np.nan, dtype=float)
    for country in pd.unique(groups):
        country_mask = groups == country
        country_scores = scores[country_mask]
        country_weights = weights[country_mask]
        for j in range(country_scores.shape[1]):
            col = country_scores[:, j]
            valid = ~np.isnan(col)
            if valid.sum() == 0:
                continue
            xv = col[valid]
            wv = country_weights[valid]
            mean = np.average(xv, weights=wv)
            var = np.average((xv - mean) ** 2, weights=wv)
            sd = math.sqrt(var) if var > 0 else 1.0
            z = np.full(col.shape, np.nan, dtype=float)
            z[valid] = (xv - mean) / sd
            zscores[country_mask, j] = z

    observed = ~np.isnan(zscores)
    zfilled = np.where(observed, zscores, 0.0)
    total_sum = zfilled.sum(axis=1)
    total_count = observed.sum(axis=1).astype(float)

    family_lookup = meta["content_category"].fillna("unknown").to_numpy(dtype=object)
    family_masks = {
        family: (family_lookup == family)
        for family in pd.unique(family_lookup)
    }

    family_sum_map = {
        family: zfilled[:, mask].sum(axis=1)
        for family, mask in family_masks.items()
    }
    family_count_map = {
        family: observed[:, mask].sum(axis=1).astype(float)
        for family, mask in family_masks.items()
    }

    rows: list[dict[str, object]] = []
    for meta_row in meta.itertuples(index=False):
        j = score_cols.index(meta_row.score_var)
        y = scores[:, j]
        item_z = zscores[:, j]
        obs_item = observed[:, j].astype(float)

        item_out = np.full(total_sum.shape, np.nan, dtype=float)
        item_out_count = total_count - obs_item
        valid_item_out = item_out_count > 0
        item_out[valid_item_out] = (total_sum[valid_item_out] - zfilled[valid_item_out, j]) / item_out_count[valid_item_out]

        family = meta_row.content_category if pd.notna(meta_row.content_category) else "unknown"
        family_out = np.full(total_sum.shape, np.nan, dtype=float)
        family_out_count = total_count - family_count_map[family]
        valid_family_out = family_out_count > 0
        family_out[valid_family_out] = (
            total_sum[valid_family_out] - family_sum_map[family][valid_family_out]
        ) / family_out_count[valid_family_out]

        item_out_z = weighted_group_standardize(item_out, groups, weights)
        family_out_z = weighted_group_standardize(family_out, groups, weights)

        core = fit_item_model(y, female, item_out_z, groups, weights)
        family_model = fit_item_model(y, female, family_out_z, groups, weights)

        time_col = f"{meta_row.score_var[:-1]}TT"
        trim_keep = np.ones(len(extract), dtype=bool)
        if time_col in extract.columns:
            times = extract[time_col].to_numpy(dtype=float)
            valid_time = (~np.isnan(times)) & (times > 0) & (~np.isnan(y))
            if valid_time.sum() >= 500:
                cutoff = weighted_quantile(times[valid_time], weights[valid_time], 0.10)
                trim_keep = (~np.isnan(y)) & ((np.isnan(times)) | (times >= cutoff))
            else:
                trim_keep = ~np.isnan(y)
        trimmed = fit_item_model(
            y[trim_keep],
            female[trim_keep],
            family_out_z[trim_keep],
            groups[trim_keep],
            weights[trim_keep],
        )

        row = {
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
            "n_nonmissing_core": core.get("n_nonmissing", 0),
            "n_countries_core": core.get("n_countries", 0),
            "uniform_beta_item_out": core.get("uniform_female_beta", np.nan),
            "uniform_se_item_out": core.get("uniform_female_se", np.nan),
            "nonuniform_beta_item_out": core.get("nonuniform_female_match_beta", np.nan),
            "nonuniform_se_item_out": core.get("nonuniform_female_match_se", np.nan),
            "uniform_strength_item_out": classify_strength(core.get("uniform_female_beta", np.nan)),
            "n_nonmissing_family_out": family_model.get("n_nonmissing", 0),
            "uniform_beta_family_out": family_model.get("uniform_female_beta", np.nan),
            "uniform_se_family_out": family_model.get("uniform_female_se", np.nan),
            "nonuniform_beta_family_out": family_model.get("nonuniform_female_match_beta", np.nan),
            "nonuniform_se_family_out": family_model.get("nonuniform_female_match_se", np.nan),
            "uniform_strength_family_out": classify_strength(family_model.get("uniform_female_beta", np.nan)),
            "n_nonmissing_trimmed": trimmed.get("n_nonmissing", 0),
            "uniform_beta_family_out_trimmed": trimmed.get("uniform_female_beta", np.nan),
            "uniform_se_family_out_trimmed": trimmed.get("uniform_female_se", np.nan),
            "nonuniform_beta_family_out_trimmed": trimmed.get("nonuniform_female_match_beta", np.nan),
            "nonuniform_se_family_out_trimmed": trimmed.get("nonuniform_female_match_se", np.nan),
            "uniform_strength_family_out_trimmed": classify_strength(trimmed.get("uniform_female_beta", np.nan)),
            "trim_share_dropped": float(1.0 - (trimmed.get("n_nonmissing", 0) / core.get("n_nonmissing", 1))),
        }
        rows.append(row)

    dif = pd.DataFrame(rows).sort_values(
        ["uniform_beta_family_out", "uniform_beta_item_out", "score_var"]
    ).reset_index(drop=True)
    dif.to_csv(DIF_OUT, sep="\t", index=False)

    summarize_group(dif, "content_category").to_csv(CONTENT_OUT, sep="\t", index=False)
    summarize_group(dif, "context_category").to_csv(CONTEXT_OUT, sep="\t", index=False)

    anchor = dif.copy()
    anchor["anchor_score_family_out"] = (
        anchor["uniform_beta_family_out"].abs() + anchor["nonuniform_beta_family_out"].abs()
    )
    anchor = anchor.sort_values(
        ["anchor_score_family_out", "n_countries_core", "n_nonmissing_core"],
        ascending=[True, False, False],
    ).reset_index(drop=True)
    anchor.head(15).to_csv(ANCHOR_OUT, sep="\t", index=False)

    print(f"wrote {DIF_OUT}")
    print(f"wrote {CONTENT_OUT}")
    print(f"wrote {CONTEXT_OUT}")
    print(f"wrote {ANCHOR_OUT}")


if __name__ == "__main__":
    main()
