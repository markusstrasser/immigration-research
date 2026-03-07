from __future__ import annotations

import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlscya"

EXTRACT_PATH = DATA_DIR / "nlscya_early_school_extract.tsv.gz"
ZIP_PATH = DATA_DIR / "nlscya_all_1979-2020.zip"
VARIABLE_MAP_PATH = DATA_DIR / "nlscya_early_school_variable_map.tsv"

OVERALL_OUT = DATA_DIR / "nlscya_early_school_surface_gaps.tsv"
AGEBIN_OUT = DATA_DIR / "nlscya_early_school_agebin_gaps.tsv"
MODEL_OUT = DATA_DIR / "nlscya_early_school_models.tsv"
PANEL_OUT = DATA_DIR / "nlscya_early_school_panel.parquet"

YEARS = [1986, 1988, 1990]
AGE_BIN_LABELS = ["4-5", "6-7", "8-9", "10-11", "12-13"]
AGE_BIN_EDGES = [48, 72, 96, 120, 144, 168]

OUTCOMES = {
    "piat_math_std": "PIAT math standard score",
    "piat_reading_comp_std": "PIAT reading comprehension standard score",
    "ppvt_std": "PPVT standard score",
}

REQUIRED_GROUPS = {
    "child_id",
    "sex",
    "assessment_age_months",
    "child_sampling_weight",
    "piat_math_std",
    "piat_reading_comp_std",
    "ppvt_std",
}


def clean_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.where(numeric >= 0)


def pick_weight_column(df: pd.DataFrame, year: int) -> str | None:
    revised = f"CSAMWT{year}_REV_{year}"
    regular = f"CSAMWT{year}_{year}"
    if revised in df.columns:
        return revised
    if regular in df.columns:
        return regular
    return None


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


def build_panel(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    child_id = pd.to_numeric(df["CPUBID_XRND"], errors="coerce")
    sex = pd.to_numeric(df["CSEX_XRND"], errors="coerce")
    female = sex.map({2: 1, 1: 0})

    for outcome_key in OUTCOMES:
        prefix = {
            "piat_math_std": "MATHZ",
            "piat_reading_comp_std": "COMPZ",
            "ppvt_std": "PPVTZ",
        }[outcome_key]

        for year in YEARS:
            score_col = f"{prefix}{year}_{year}"
            age_col = f"CSAGE{year}_{year}"
            if score_col not in df.columns or age_col not in df.columns:
                continue
            weight_col = pick_weight_column(df, year)
            if not weight_col:
                continue

            frame = pd.DataFrame(
                {
                    "child_id": child_id,
                    "female": female,
                    "wave": year,
                    "outcome": outcome_key,
                    "score": clean_numeric(df[score_col]),
                    "age_months": clean_numeric(df[age_col]),
                    "weight": clean_numeric(df[weight_col]),
                }
            )
            rows.append(frame)

    panel = pd.concat(rows, ignore_index=True)
    panel = panel.dropna(subset=["child_id", "female", "score", "age_months"]).copy()
    panel["weight"] = panel["weight"].fillna(1.0)
    panel["age_years"] = panel["age_months"] / 12.0
    panel["age_years_centered"] = panel["age_years"] - 7.0
    panel["age_bin"] = pd.cut(
        panel["age_months"],
        bins=AGE_BIN_EDGES,
        labels=AGE_BIN_LABELS,
        right=False,
        include_lowest=True,
    )
    return panel


def load_from_source_zip() -> pd.DataFrame:
    variable_map = pd.read_csv(VARIABLE_MAP_PATH, sep="\t")
    variable_map = variable_map[variable_map["group"].isin(REQUIRED_GROUPS)].copy()
    usecols = sorted(variable_map["alias"].dropna().unique().tolist())

    with zipfile.ZipFile(ZIP_PATH) as zf:
        member = next(name for name in zf.namelist() if name.endswith(".csv"))
        with zf.open(member) as raw:
            df = pd.read_csv(raw, usecols=usecols, low_memory=False)
    return df


def load_frame() -> pd.DataFrame:
    try:
        return pd.read_csv(EXTRACT_PATH, sep="\t", compression="gzip", low_memory=False)
    except (EOFError, OSError, pd.errors.ParserError):
        return load_from_source_zip()


def summarize_gaps(panel: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, sub in panel.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)

        values = sub["score"].to_numpy(dtype=float)
        female = sub["female"].to_numpy(dtype=int)
        weights = sub["weight"].to_numpy(dtype=float)
        mean_f, mean_m, d = weighted_d(values, female, weights)

        row = {
            col: key for col, key in zip(group_cols, keys, strict=True)
        }
        row.update(
            {
                "n": int(len(sub)),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
                "mean_age_years": float(np.average(sub["age_years"], weights=sub["weight"])),
            }
        )
        rows.append(row)

    return pd.DataFrame(rows).sort_values(group_cols).reset_index(drop=True)


def run_models(panel: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome, sub in panel.groupby("outcome", observed=True):
        work = sub[(sub["age_months"] >= 48) & (sub["age_months"] < 168)].copy()
        if work.empty:
            continue

        model = smf.wls(
            "score ~ female + age_years_centered + female:age_years_centered + C(wave)",
            data=work,
            weights=work["weight"],
        ).fit(cov_type="cluster", cov_kwds={"groups": work["child_id"]})

        for term in ["female", "female:age_years_centered"]:
            coef = model.params.get(term, math.nan)
            se = model.bse.get(term, math.nan)
            rows.append(
                {
                    "outcome": outcome,
                    "term": term,
                    "n": int(model.nobs),
                    "beta": coef,
                    "se": se,
                    "ci_low": coef - 1.96 * se if pd.notna(se) else math.nan,
                    "ci_high": coef + 1.96 * se if pd.notna(se) else math.nan,
                    "r_squared": float(model.rsquared),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    df = load_frame()
    panel = build_panel(df)
    panel.to_parquet(PANEL_OUT, index=False)

    overall = summarize_gaps(panel, ["outcome", "wave"])
    agebin = summarize_gaps(panel.dropna(subset=["age_bin"]), ["outcome", "age_bin"])
    models = run_models(panel)

    overall.to_csv(OVERALL_OUT, sep="\t", index=False)
    agebin.to_csv(AGEBIN_OUT, sep="\t", index=False)
    models.to_csv(MODEL_OUT, sep="\t", index=False)

    print(f"wrote {PANEL_OUT}")
    print(f"wrote {OVERALL_OUT}")
    print(f"wrote {AGEBIN_OUT}")
    print(f"wrote {MODEL_OUT}")


if __name__ == "__main__":
    main()
