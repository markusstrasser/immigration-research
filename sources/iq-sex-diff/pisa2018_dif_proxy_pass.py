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

DIF_OUT = DATA_DIR / "pisa2018_item_dif_proxy.tsv"
CONTENT_OUT = DATA_DIR / "pisa2018_dif_content_summary.tsv"
CONTEXT_OUT = DATA_DIR / "pisa2018_dif_context_summary.tsv"
ANCHOR_OUT = DATA_DIR / "pisa2018_dif_anchor_candidates.tsv"


ID_COLS = ["CNT", "W_FSTUWT", "female"]
PV_COLS = [f"PV{i}MATH" for i in range(1, 11)]


def weighted_group_z(df: pd.DataFrame, value_col: str, group_col: str, weight_col: str) -> pd.Series:
    out = pd.Series(index=df.index, dtype=float)
    for key, sub in df.groupby(group_col, observed=True):
        w = sub[weight_col].to_numpy(dtype=float)
        x = sub[value_col].to_numpy(dtype=float)
        mean = np.average(x, weights=w)
        var = np.average((x - mean) ** 2, weights=w)
        sd = math.sqrt(var) if var > 0 else 1.0
        out.loc[sub.index] = (x - mean) / sd
    return out


def weighted_demean(df: pd.DataFrame, value_col: str, group_col: str, weight_col: str) -> pd.Series:
    out = pd.Series(index=df.index, dtype=float)
    for key, sub in df.groupby(group_col, observed=True):
        w = sub[weight_col].to_numpy(dtype=float)
        x = sub[value_col].to_numpy(dtype=float)
        mean = np.average(x, weights=w)
        out.loc[sub.index] = x - mean
    return out


def classify_strength(beta: float) -> str:
    mag = abs(beta)
    if mag >= 0.08:
        return "large"
    if mag >= 0.04:
        return "moderate"
    if mag >= 0.02:
        return "small"
    return "near_zero"


def summarize_group(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, sub in df.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        weights = sub["n_nonmissing"].astype(float).to_numpy()
        row = {col: key for col, key in zip(group_cols, keys, strict=True)}
        row.update(
            {
                "items": int(len(sub)),
                "units": int(sub["unit_id"].nunique()),
                "weighted_raw_gap_d": float(np.average(sub["country_weighted_mean_d"], weights=weights)),
                "weighted_uniform_beta": float(np.average(sub["uniform_female_beta"], weights=weights)),
                "weighted_abs_uniform_beta": float(np.average(np.abs(sub["uniform_female_beta"]), weights=weights)),
                "weighted_nonuniform_beta": float(np.average(sub["nonuniform_female_math_beta"], weights=weights)),
                "weighted_abs_nonuniform_beta": float(np.average(np.abs(sub["nonuniform_female_math_beta"]), weights=weights)),
                "female_positive_uniform_items": int((sub["uniform_female_beta"] > 0).sum()),
                "male_positive_uniform_items": int((sub["uniform_female_beta"] < 0).sum()),
                "near_zero_uniform_items": int((sub["uniform_strength"] == "near_zero").sum()),
            }
        )
        rows.append(row)
    return pd.DataFrame(rows).sort_values(group_cols).reset_index(drop=True)


def main() -> None:
    extract = pd.read_parquet(EXTRACT_PATH)
    item_meta = pd.read_csv(ITEM_GAPS_PATH, sep="\t")
    proxy = pd.read_csv(PROXY_PATH, sep="\t")

    extract = extract.copy()
    extract["math_avg"] = extract[PV_COLS].mean(axis=1)
    extract["math_country_z"] = weighted_group_z(extract, "math_avg", "CNT", "W_FSTUWT")

    merged_meta = item_meta.merge(proxy, on=["unit_id", "unit_label"], how="left", validate="many_to_one")
    score_vars = merged_meta["score_var"].tolist()

    rows: list[dict[str, object]] = []
    for meta in merged_meta.itertuples(index=False):
        sub = extract[["CNT", "W_FSTUWT", "female", "math_country_z", meta.score_var]].dropna().copy()
        if sub.empty or sub["CNT"].nunique() < 10:
            continue

        sub["female_math"] = sub["female"] * sub["math_country_z"]
        sub["y_dm"] = weighted_demean(sub, meta.score_var, "CNT", "W_FSTUWT")
        sub["female_dm"] = weighted_demean(sub, "female", "CNT", "W_FSTUWT")
        sub["math_dm"] = weighted_demean(sub, "math_country_z", "CNT", "W_FSTUWT")
        sub["female_math_dm"] = weighted_demean(sub, "female_math", "CNT", "W_FSTUWT")

        X = sub[["female_dm", "math_dm", "female_math_dm"]]
        y = sub["y_dm"]

        model = sm.WLS(y, X, weights=sub["W_FSTUWT"]).fit(
            cov_type="cluster",
            cov_kwds={"groups": sub["CNT"]},
        )

        uniform_beta = float(model.params["female_dm"])
        uniform_se = float(model.bse["female_dm"])
        nonuniform_beta = float(model.params["female_math_dm"])
        nonuniform_se = float(model.bse["female_math_dm"])

        rows.append(
            {
                "score_var": meta.score_var,
                "unit_id": meta.unit_id,
                "question_id": meta.question_id,
                "unit_label": meta.unit_label,
                "content_category": meta.content_category,
                "context_category": meta.context_category,
                "confidence": meta.confidence,
                "notes": meta.notes,
                "unit_family": meta.unit_family,
                "score_family": meta.score_family,
                "max_score": meta.max_score,
                "n_nonmissing": int(len(sub)),
                "n_countries": int(sub["CNT"].nunique()),
                "country_weighted_mean_d": float(meta.country_weighted_mean_d),
                "uniform_female_beta": uniform_beta,
                "uniform_female_se": uniform_se,
                "uniform_ci_low": uniform_beta - 1.96 * uniform_se,
                "uniform_ci_high": uniform_beta + 1.96 * uniform_se,
                "uniform_strength": classify_strength(uniform_beta),
                "nonuniform_female_math_beta": nonuniform_beta,
                "nonuniform_female_math_se": nonuniform_se,
                "nonuniform_ci_low": nonuniform_beta - 1.96 * nonuniform_se,
                "nonuniform_ci_high": nonuniform_beta + 1.96 * nonuniform_se,
                "nonuniform_strength": classify_strength(nonuniform_beta),
                "r_squared": float(model.rsquared),
            }
        )

    dif = pd.DataFrame(rows).sort_values(["uniform_female_beta", "nonuniform_female_math_beta", "score_var"]).reset_index(drop=True)
    dif.to_csv(DIF_OUT, sep="\t", index=False)

    summarize_group(dif, ["content_category"]).to_csv(CONTENT_OUT, sep="\t", index=False)
    summarize_group(dif, ["context_category"]).to_csv(CONTEXT_OUT, sep="\t", index=False)

    anchor = dif.copy()
    anchor["anchor_score"] = anchor["uniform_female_beta"].abs() + anchor["nonuniform_female_math_beta"].abs()
    anchor = anchor.sort_values(["anchor_score", "n_countries", "n_nonmissing"], ascending=[True, False, False]).reset_index(drop=True)
    anchor.head(15).to_csv(ANCHOR_OUT, sep="\t", index=False)

    print(f"wrote {DIF_OUT}")
    print(f"wrote {CONTENT_OUT}")
    print(f"wrote {CONTEXT_OUT}")
    print(f"wrote {ANCHOR_OUT}")


if __name__ == "__main__":
    main()
