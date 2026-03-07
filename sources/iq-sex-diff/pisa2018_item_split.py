from __future__ import annotations

import math
import re
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "pisa"
DOCS_DIR = DATA_DIR / "docs"
OUTPUT_DIR = DATA_DIR

QQQ_ZIP = DATA_DIR / "SPSS_STU_QQQ.zip"
COG_ZIP = DATA_DIR / "SPSS_STU_COG.zip"
TTM_ZIP = DATA_DIR / "SPSS_STU_TTM.zip"
CODEBOOK_XLSX = DOCS_DIR / "PISA2018_CODEBOOK.xlsx"

ITEM_FAMILY_OUT = OUTPUT_DIR / "pisa2018_item_family_gaps.tsv"
PROCESS_OUT = OUTPUT_DIR / "pisa2018_process_gaps.tsv"
MODEL_OUT = OUTPUT_DIR / "pisa2018_item_models.tsv"
ITEM_OUT = OUTPUT_DIR / "pisa2018_item_level_gaps.tsv"
EXTRACT_OUT = OUTPUT_DIR / "pisa2018_math_item_extract.parquet"

ID_COLS = ["CNT", "CNTSCHID", "CNTSTUID"]
QQQ_COLS = ID_COLS + ["ST004D01T", "W_FSTUWT"] + [f"PV{i}MATH" for i in range(1, 11)]


def read_codebook(sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(CODEBOOK_XLSX, sheet_name=sheet_name)
    df.columns = ["name", "varlabel", "type", "format", "varnum", "minmax", "val", "label", "count", "percent"]
    return df[df["name"].notna()].copy()


def parse_item_metadata() -> pd.DataFrame:
    cog = read_codebook("CY07_MSU_STU_COG")
    ttm = read_codebook("CY07_MSU_STU_TTM")

    score_rows = cog[cog["name"].astype(str).str.match(r"^CM\d+Q\d+S$")].copy()
    time_rows = ttm[ttm["name"].astype(str).str.match(r"^CM\d+Q\d+TT$")].copy()
    visit_rows = ttm[ttm["name"].astype(str).str.match(r"^CM\d+Q\d+V$")].copy()

    score_rows["item_key"] = score_rows["name"].str.replace("S$", "", regex=True)
    time_rows["item_key"] = time_rows["name"].str.replace("TT$", "", regex=True)
    visit_rows["item_key"] = visit_rows["name"].str.replace("V$", "", regex=True)

    score_rows["unit_id"] = score_rows["name"].str.extract(r"^(CM\d+)Q")
    score_rows["question_id"] = score_rows["name"].str.extract(r"(Q\d+)S$")
    score_rows["unit_label"] = score_rows["varlabel"].str.replace(r" - Q\d+ \(Scored Response\)$", "", regex=True)
    score_rows["max_score"] = score_rows["minmax"].astype(str).str.extract(r"-([0-9]+(?:\.[0-9]+)?)$").astype(float)
    score_rows["score_family"] = np.where(score_rows["max_score"].fillna(1.0) > 1.0, "partial_credit", "binary")

    merged = (
        score_rows[["name", "item_key", "unit_id", "question_id", "unit_label", "max_score", "score_family"]]
        .rename(columns={"name": "score_var"})
        .merge(
            time_rows[["name", "item_key"]].rename(columns={"name": "time_var"}),
            on="item_key",
            how="left",
        )
        .merge(
            visit_rows[["name", "item_key"]].rename(columns={"name": "visit_var"}),
            on="item_key",
            how="left",
        )
    )

    unit_size = merged.groupby("unit_id")["score_var"].transform("size")
    merged["unit_size"] = unit_size
    merged["unit_family"] = np.where(unit_size > 1, "multi_item_unit", "single_item_unit")
    return merged.sort_values(["unit_id", "question_id"]).reset_index(drop=True)


def extract_member(zip_path: Path, td: str) -> Path:
    with zipfile.ZipFile(zip_path) as zf:
        member = next(name for name in zf.namelist() if name.lower().endswith(".sav"))
        zf.extract(member, td)
        return Path(td) / member


def read_sav_selected(zip_path: Path, columns: list[str]) -> pd.DataFrame:
    with tempfile.TemporaryDirectory() as td:
        sav_path = extract_member(zip_path, td)
        df, _meta = pyreadstat.read_sav(str(sav_path), usecols=columns)
    return df


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.average(values, weights=weights))


def weighted_var(values: np.ndarray, weights: np.ndarray) -> float:
    mean = weighted_mean(values, weights)
    return float(np.average((values - mean) ** 2, weights=weights))


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


def clean_numeric(df: pd.DataFrame, protected: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if col in protected:
            continue
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].where(out[col] >= 0)
    return out


def item_country_summary(df: pd.DataFrame, item: str, female_col: str, weight_col: str, country_col: str) -> tuple[float, int]:
    tmp = df[[country_col, female_col, weight_col, item]].dropna()
    if tmp.empty:
        return math.nan, 0

    rows: list[tuple[float, float]] = []
    for _, sub in tmp.groupby(country_col, observed=True):
        female = sub[female_col].to_numpy()
        values = sub[item].to_numpy(dtype=float)
        weights = sub[weight_col].to_numpy(dtype=float)
        if female.min() == female.max():
            continue
        _, _, d = weighted_d(values, female, weights)
        if not math.isnan(d):
            rows.append((d, weights.sum()))

    if not rows:
        return math.nan, 0
    ds = np.array([r[0] for r in rows], dtype=float)
    ws = np.array([r[1] for r in rows], dtype=float)
    return float(np.average(ds, weights=ws)), len(rows)


def run_models(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["math_avg"] = work[[f"PV{i}MATH" for i in range(1, 11)]].mean(axis=1)
    work = work.dropna(subset=["math_avg", "female", "W_FSTUWT", "process_item_count", "avg_item_time", "avg_item_visits", "CNT"])

    for col in ["math_avg", "process_item_count", "avg_item_time", "avg_item_visits"]:
        std = work[col].std(ddof=0)
        work[f"z_{col}"] = (work[col] - work[col].mean()) / std if std and not math.isnan(std) else 0.0

    work["log_avg_item_time"] = np.log1p(work["avg_item_time"])
    work["log_avg_item_visits"] = np.log1p(work["avg_item_visits"])
    for col in ["log_avg_item_time", "log_avg_item_visits"]:
        std = work[col].std(ddof=0)
        work[f"z_{col}"] = (work[col] - work[col].mean()) / std if std and not math.isnan(std) else 0.0

    specs = [
        ("base_country_fe", "z_math_avg ~ female + C(CNT)"),
        (
            "process_stress_country_fe",
            "z_math_avg ~ female + z_process_item_count + z_log_avg_item_time + z_log_avg_item_visits + C(CNT)",
        ),
    ]

    rows = []
    for name, formula in specs:
        model = smf.wls(formula, data=work, weights=work["W_FSTUWT"]).fit()
        coef = model.params.get("female", math.nan)
        se = model.bse.get("female", math.nan)
        rows.append(
            {
                "model": name,
                "n": int(model.nobs),
                "female_beta": coef,
                "female_se": se,
                "female_ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                "female_ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                "r_squared": float(model.rsquared),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    item_meta = parse_item_metadata()
    score_cols = item_meta["score_var"].tolist()
    time_cols = item_meta["time_var"].dropna().tolist()
    visit_cols = item_meta["visit_var"].dropna().tolist()

    qqq = read_sav_selected(QQQ_ZIP, QQQ_COLS)
    cog = read_sav_selected(COG_ZIP, ID_COLS + score_cols)
    ttm = read_sav_selected(TTM_ZIP, ID_COLS + time_cols + visit_cols)

    qqq = clean_numeric(qqq, protected=ID_COLS + ["ST004D01T"])
    cog = clean_numeric(cog, protected=ID_COLS)
    ttm = clean_numeric(ttm, protected=ID_COLS)

    merged = qqq.merge(cog, on=ID_COLS, how="inner").merge(ttm, on=ID_COLS, how="inner")
    merged["female"] = merged["ST004D01T"].map({1: 1, 2: 0})
    merged = merged.dropna(subset=["female", "W_FSTUWT"]).copy()
    merged["CNT"] = merged["CNT"].astype(str)

    score_present = merged[score_cols].notna()
    merged["process_item_count"] = score_present.sum(axis=1)

    time_matrix = merged[time_cols] if time_cols else pd.DataFrame(index=merged.index)
    visit_matrix = merged[visit_cols] if visit_cols else pd.DataFrame(index=merged.index)
    merged["avg_item_time"] = time_matrix.mean(axis=1)
    merged["avg_item_visits"] = visit_matrix.mean(axis=1)

    merged.to_parquet(EXTRACT_OUT, index=False)

    item_rows = []
    for row in item_meta.itertuples(index=False):
        cols = [row.score_var]
        if pd.notna(row.time_var):
            cols.append(row.time_var)
        if pd.notna(row.visit_var):
            cols.append(row.visit_var)

        tmp = merged[["CNT", "female", "W_FSTUWT"] + cols].dropna(subset=[row.score_var]).copy()
        if tmp.empty:
            continue
        values = tmp[row.score_var].to_numpy(dtype=float)
        female = tmp["female"].to_numpy(dtype=int)
        weights = tmp["W_FSTUWT"].to_numpy(dtype=float)
        mean_f, mean_m, d = weighted_d(values, female, weights)
        country_d, n_countries = item_country_summary(tmp, row.score_var, "female", "W_FSTUWT", "CNT")

        time_f = time_m = visits_f = visits_m = math.nan
        if pd.notna(row.time_var) and row.time_var in tmp:
            tt = tmp[row.time_var].to_numpy(dtype=float)
            tt_mask = ~np.isnan(tt)
            if tt_mask.any():
                time_f = weighted_mean(tt[(female == 1) & tt_mask], weights[(female == 1) & tt_mask]) if ((female == 1) & tt_mask).any() else math.nan
                time_m = weighted_mean(tt[(female == 0) & tt_mask], weights[(female == 0) & tt_mask]) if ((female == 0) & tt_mask).any() else math.nan
        if pd.notna(row.visit_var) and row.visit_var in tmp:
            vv = tmp[row.visit_var].to_numpy(dtype=float)
            vv_mask = ~np.isnan(vv)
            if vv_mask.any():
                visits_f = weighted_mean(vv[(female == 1) & vv_mask], weights[(female == 1) & vv_mask]) if ((female == 1) & vv_mask).any() else math.nan
                visits_m = weighted_mean(vv[(female == 0) & vv_mask], weights[(female == 0) & vv_mask]) if ((female == 0) & vv_mask).any() else math.nan

        item_rows.append(
            {
                "score_var": row.score_var,
                "unit_id": row.unit_id,
                "question_id": row.question_id,
                "unit_label": row.unit_label,
                "unit_size": row.unit_size,
                "unit_family": row.unit_family,
                "score_family": row.score_family,
                "max_score": row.max_score,
                "n_nonmissing": len(tmp),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
                "country_weighted_mean_d": country_d,
                "n_countries": n_countries,
                "female_avg_total_time": time_f,
                "male_avg_total_time": time_m,
                "female_avg_visits": visits_f,
                "male_avg_visits": visits_m,
            }
        )

    item_df = pd.DataFrame(item_rows)
    item_df["overall_avg_total_time"] = item_df[["female_avg_total_time", "male_avg_total_time"]].mean(axis=1)
    item_df["overall_avg_visits"] = item_df[["female_avg_visits", "male_avg_visits"]].mean(axis=1)
    item_df["burden_index"] = (
        np.log1p(item_df["overall_avg_total_time"].fillna(item_df["overall_avg_total_time"].median()))
        + np.log1p(item_df["overall_avg_visits"].fillna(item_df["overall_avg_visits"].median()))
    )
    item_df["burden_quartile"] = pd.qcut(item_df["burden_index"], 4, labels=["q1_low", "q2_midlow", "q3_midhigh", "q4_high"])
    item_df = item_df.sort_values(["country_weighted_mean_d", "d_female_minus_male", "unit_label", "question_id"]).reset_index(drop=True)
    item_df.to_csv(ITEM_OUT, sep="\t", index=False)

    family_rows = []
    family_specs = {
        "score_family": "score_family",
        "unit_family": "unit_family",
        "burden_quartile": "burden_quartile",
    }
    for family_name, col in family_specs.items():
        for group, sub in item_df.groupby(col, observed=True):
            family_rows.append(
                {
                    "family_type": family_name,
                    "family_value": group,
                    "n_items": int(len(sub)),
                    "mean_item_d": sub["country_weighted_mean_d"].mean(),
                    "median_item_d": sub["country_weighted_mean_d"].median(),
                    "mean_female_total_time": sub["female_avg_total_time"].mean(),
                    "mean_male_total_time": sub["male_avg_total_time"].mean(),
                    "mean_female_visits": sub["female_avg_visits"].mean(),
                    "mean_male_visits": sub["male_avg_visits"].mean(),
                }
            )
    family_df = pd.DataFrame(family_rows).sort_values(["family_type", "family_value"]).reset_index(drop=True)
    family_df.to_csv(ITEM_FAMILY_OUT, sep="\t", index=False)

    process_df = item_df[
        [
            "score_var",
            "unit_label",
            "score_family",
            "unit_family",
            "burden_quartile",
            "female_avg_total_time",
            "male_avg_total_time",
            "female_avg_visits",
            "male_avg_visits",
            "country_weighted_mean_d",
        ]
    ].copy()
    process_df["time_gap_female_minus_male"] = process_df["female_avg_total_time"] - process_df["male_avg_total_time"]
    process_df["visit_gap_female_minus_male"] = process_df["female_avg_visits"] - process_df["male_avg_visits"]
    process_df.to_csv(PROCESS_OUT, sep="\t", index=False)

    model_df = run_models(merged)
    model_df.to_csv(MODEL_OUT, sep="\t", index=False)


if __name__ == "__main__":
    main()
