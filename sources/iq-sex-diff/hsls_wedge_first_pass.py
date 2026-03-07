#!/usr/bin/env python3
"""First-pass HSLS grade-test wedge analysis."""

from __future__ import annotations

import io
import zipfile
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat
import statsmodels.formula.api as smf


DATA_DIR = Path(__file__).resolve().parent / "data" / "hsls"
ZIP_PATH = DATA_DIR / "HSLS_2017_PETS_SR_v1_0_SPSS_Datasets.zip"
SAV_MEMBER = "hsls_17_student_pets_sr_v1_0.sav"

USECOLS = [
    "X1SEX",
    "X1TXMTSCOR",
    "X2TXMTSCOR",
    "X3TCOVERAGE",
    "X3THIMATH",
    "X3TCREDMAT",
    "X3TCREDAPMTH",
    "X3TGPAMAT",
    "X3TGPAHIMTH",
    "X3TGPAWGT",
    "W3W1W2STUTR",
]

LADDER_KEEP_MIN_N = 200


def weighted_mean(x: pd.Series, w: pd.Series) -> float:
    return float(np.sum(x * w) / np.sum(w))


def weighted_var(x: pd.Series, w: pd.Series) -> float:
    mean = weighted_mean(x, w)
    return float(np.sum(w * (x - mean) ** 2) / np.sum(w))


def weighted_d(sub: pd.DataFrame, column: str) -> tuple[float, float, float]:
    female = sub[sub["female"] == 1]
    male = sub[sub["female"] == 0]
    mf = weighted_mean(female[column], female["w"])
    mm = weighted_mean(male[column], male["w"])
    vf = weighted_var(female[column], female["w"])
    vm = weighted_var(male[column], male["w"])
    pooled = sqrt((vf + vm) / 2.0)
    return (mf - mm) / pooled, mf, mm


def recode_missing(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in USECOLS:
        if col == "X1SEX":
            out.loc[~out[col].isin([1, 2]), col] = np.nan
        else:
            out.loc[out[col] < 0, col] = np.nan
    return out


def load_hsls() -> tuple[pd.DataFrame, dict[int, str]]:
    with zipfile.ZipFile(ZIP_PATH) as zf:
        data = io.BytesIO(zf.read(SAV_MEMBER))
    df, meta = pyreadstat.read_sav(data, usecols=USECOLS)
    df = recode_missing(df)
    labelset = meta.variable_to_label["X3THIMATH"]
    ladder_labels = {
        int(code): label
        for code, label in meta.value_labels[labelset].items()
        if code >= 0
    }
    return df, ladder_labels


def build_extract(df: pd.DataFrame, ladder_labels: dict[int, str]) -> pd.DataFrame:
    core = df[df["X1SEX"].isin([1, 2])].copy()
    core["female"] = (core["X1SEX"] == 2).astype(int)
    core["sex_label"] = core["female"].map({0: "male", 1: "female"})
    core["w"] = core["W3W1W2STUTR"]
    core = core[
        (core["w"] > 0)
        & (core["X3TCOVERAGE"] == 1)
        & core[
            [
                "X1TXMTSCOR",
                "X2TXMTSCOR",
                "X3THIMATH",
                "X3TCREDMAT",
                "X3TCREDAPMTH",
                "X3TGPAMAT",
                "X3TGPAHIMTH",
                "X3TGPAWGT",
            ]
        ].notna().all(axis=1)
    ].copy()
    core["highest_math_label"] = core["X3THIMATH"].astype(int).map(ladder_labels)
    core["precalc_plus"] = core["X3THIMATH"].isin([10, 11, 12, 13]).astype(int)

    for col in [
        "X1TXMTSCOR",
        "X2TXMTSCOR",
        "X3TGPAMAT",
        "X3TGPAHIMTH",
        "X3TGPAWGT",
        "X3TCREDMAT",
        "X3TCREDAPMTH",
    ]:
        mean = weighted_mean(core[col], core["w"])
        std = sqrt(weighted_var(core[col], core["w"]))
        core[f"{col}_z"] = (core[col] - mean) / std

    return core


def build_overall_table(core: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "X1TXMTSCOR",
        "X2TXMTSCOR",
        "X3TGPAMAT",
        "X3TGPAHIMTH",
        "X3TGPAWGT",
        "X3TCREDMAT",
        "X3TCREDAPMTH",
    ]
    rows = []
    for metric in metrics:
        sub = core[core[metric].notna()]
        d, female_mean, male_mean = weighted_d(sub, metric)
        rows.append(
            {
                "metric": metric,
                "n": len(sub),
                "weighted_d_female_minus_male": d,
                "female_mean": female_mean,
                "male_mean": male_mean,
                "female_minus_male": female_mean - male_mean,
            }
        )
    return pd.DataFrame(rows)


def build_ladder_table(core: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for level, sub in core.groupby("X3THIMATH", sort=True):
        if len(sub) < LADDER_KEEP_MIN_N:
            continue
        weighted_n = float(sub["w"].sum())
        d_test, female_test, male_test = weighted_d(sub, "X2TXMTSCOR")
        d_gpa, female_gpa, male_gpa = weighted_d(sub, "X3TGPAMAT")
        rows.append(
            {
                "highest_math_level": int(level),
                "highest_math_label": sub["highest_math_label"].iloc[0],
                "n": len(sub),
                "weighted_n": weighted_n,
                "test_d_female_minus_male": d_test,
                "test_female_mean": female_test,
                "test_male_mean": male_test,
                "test_female_minus_male": female_test - male_test,
                "gpa_d_female_minus_male": d_gpa,
                "gpa_female_mean": female_gpa,
                "gpa_male_mean": male_gpa,
                "gpa_female_minus_male": female_gpa - male_gpa,
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values("weighted_n", ascending=False).reset_index(drop=True)


def build_model_table(core: pd.DataFrame) -> pd.DataFrame:
    specs = {
        "x2_base": "X2TXMTSCOR_z ~ female",
        "x2_plus_x1": "X2TXMTSCOR_z ~ female + X1TXMTSCOR_z",
        "x2_plus_x1_ladder": "X2TXMTSCOR_z ~ female + X1TXMTSCOR_z + C(X3THIMATH)",
        "x2_plus_x1_ladder_credits": (
            "X2TXMTSCOR_z ~ female + X1TXMTSCOR_z + C(X3THIMATH) "
            "+ X3TCREDMAT_z + X3TCREDAPMTH_z"
        ),
        "gpa_base": "X3TGPAMAT_z ~ female",
        "gpa_plus_scores": "X3TGPAMAT_z ~ female + X1TXMTSCOR_z + X2TXMTSCOR_z",
        "gpa_plus_scores_ladder": (
            "X3TGPAMAT_z ~ female + X1TXMTSCOR_z + X2TXMTSCOR_z + C(X3THIMATH) "
            "+ X3TCREDMAT_z + X3TCREDAPMTH_z"
        ),
        "high_gpa_plus_scores_ladder": (
            "X3TGPAHIMTH_z ~ female + X1TXMTSCOR_z + X2TXMTSCOR_z + C(X3THIMATH) "
            "+ X3TCREDMAT_z + X3TCREDAPMTH_z"
        ),
        "precalc_plus": "precalc_plus ~ female + X1TXMTSCOR_z",
    }
    rows = []
    for name, formula in specs.items():
        fit = smf.wls(formula, data=core, weights=core["w"]).fit(cov_type="HC1")
        beta = float(fit.params["female"])
        se = float(fit.bse["female"])
        rows.append(
            {
                "model": name,
                "outcome": formula.split("~", 1)[0].strip(),
                "formula": formula,
                "n": int(fit.nobs),
                "beta_female": beta,
                "se_female": se,
                "ci95_low": beta - 1.96 * se,
                "ci95_high": beta + 1.96 * se,
                "r_squared": float(getattr(fit, "rsquared", np.nan)),
            }
        )
    return pd.DataFrame(rows)


def write_outputs(core: pd.DataFrame, overall: pd.DataFrame, ladder: pd.DataFrame, models: pd.DataFrame) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    core.to_parquet(DATA_DIR / "hsls_wedge_extract.parquet", index=False)
    sample_cols = [
        "sex_label",
        "X1TXMTSCOR",
        "X2TXMTSCOR",
        "X3THIMATH",
        "highest_math_label",
        "X3TCREDMAT",
        "X3TCREDAPMTH",
        "X3TGPAMAT",
        "X3TGPAHIMTH",
        "X3TGPAWGT",
        "precalc_plus",
        "w",
    ]
    core[sample_cols].sample(n=min(250, len(core)), random_state=42).to_csv(
        DATA_DIR / "hsls_wedge_frontier_sample.tsv",
        sep="\t",
        index=False,
    )
    overall.to_csv(DATA_DIR / "hsls_wedge_overall.tsv", sep="\t", index=False)
    ladder.to_csv(DATA_DIR / "hsls_wedge_by_ladder.tsv", sep="\t", index=False)
    models.to_csv(DATA_DIR / "hsls_wedge_models.tsv", sep="\t", index=False)


def main() -> int:
    raw, ladder_labels = load_hsls()
    core = build_extract(raw, ladder_labels)
    overall = build_overall_table(core)
    ladder = build_ladder_table(core)
    models = build_model_table(core)
    write_outputs(core, overall, ladder, models)
    print(f"core_n={len(core)}")
    print(overall.to_string(index=False))
    print(models[["model", "beta_female", "ci95_low", "ci95_high"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
