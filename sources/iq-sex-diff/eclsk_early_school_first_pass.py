from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA_DIR = ROOT / "data" / "ecls_k"

EXTRACT_PATH = DATA_DIR / "eclsk_early_school_extract.tsv.gz"
PANEL_OUT = DATA_DIR / "eclsk_early_school_panel.parquet"
GAPS_OUT = DATA_DIR / "eclsk_early_school_surface_gaps.tsv"
MODELS_OUT = DATA_DIR / "eclsk_early_school_models.tsv"

WAVE_LABELS = {
    1: "fall_k",
    2: "spring_k",
    3: "fall_1",
    4: "spring_1",
    5: "spring_3",
}

WEIGHT_BY_WAVE = {
    1: "C1WEIGHT",
    2: "C2WEIGHT",
    3: "C3WEIGHT",
    4: "C4WEIGHT",
    5: "C5WEIGHT",
}

AGE_BY_WAVE = {
    1: "R1_KAGE",
    2: "R2_KAGE",
    3: "R3AGE",
    4: "R4AGE",
    5: "R5AGE",
}

OUTCOMES = {
    "math_irt_scale": ("MTHFLG", "R4MSCL"),
    "reading_irt_scale": ("RDGFLG", "R4RSCL"),
}


def clean_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.where(numeric > -8)


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
    female = clean_numeric(df["GENDER"]).map({2: 1, 1: 0})
    child_id = df["CHILDID"].astype(str).str.strip()
    rows: list[pd.DataFrame] = []

    for outcome, (flag_suffix, score_suffix) in OUTCOMES.items():
        for wave in range(1, 6):
            flag_col = f"C{wave}{flag_suffix}"
            score_col = f"C{wave}{score_suffix}"
            weight_col = WEIGHT_BY_WAVE[wave]
            age_col = AGE_BY_WAVE[wave]
            frame = pd.DataFrame(
                {
                    "child_id": child_id,
                    "female": female,
                    "wave": wave,
                    "wave_label": WAVE_LABELS[wave],
                    "outcome": outcome,
                    "flag": clean_numeric(df[flag_col]),
                    "score": clean_numeric(df[score_col]),
                    "weight": clean_numeric(df[weight_col]).where(clean_numeric(df[weight_col]) > 0),
                    "age_months": clean_numeric(df[age_col]),
                }
            )
            rows.append(frame)

    panel = pd.concat(rows, ignore_index=True)
    panel = panel.dropna(subset=["female", "score", "weight", "age_months"]).copy()
    panel = panel[panel["flag"] == 1].copy()
    panel["age_years"] = panel["age_months"] / 12.0
    panel["wave_num_centered"] = panel["wave"] - 1.0
    return panel


def summarize_gaps(panel: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (outcome, wave, wave_label), sub in panel.groupby(["outcome", "wave", "wave_label"], observed=True):
        values = sub["score"].to_numpy(dtype=float)
        female = sub["female"].to_numpy(dtype=int)
        weights = sub["weight"].to_numpy(dtype=float)
        mean_f, mean_m, d = weighted_d(values, female, weights)
        rows.append(
            {
                "outcome": outcome,
                "wave": int(wave),
                "wave_label": wave_label,
                "n": int(len(sub)),
                "female_mean": mean_f,
                "male_mean": mean_m,
                "d_female_minus_male": d,
            }
        )
    return pd.DataFrame(rows).sort_values(["outcome", "wave"]).reset_index(drop=True)


def run_models(panel: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for outcome, sub in panel.groupby("outcome", observed=True):
        base_model = smf.wls(
            "score ~ female + wave_num_centered + female:wave_num_centered + C(wave)",
            data=sub,
            weights=sub["weight"],
        )
        model = base_model.fit(cov_type="cluster", cov_kwds={"groups": sub["child_id"]})
        if any(not pd.notna(model.bse.get(term, math.nan)) for term in ["female", "female:wave_num_centered"]):
            model = base_model.fit(cov_type="HC1")

        for term in ["female", "female:wave_num_centered"]:
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
    df = pd.read_csv(EXTRACT_PATH, sep="\t", compression="gzip", low_memory=False)
    panel = build_panel(df)
    panel.to_parquet(PANEL_OUT, index=False)

    gaps = summarize_gaps(panel)
    models = run_models(panel)

    gaps.to_csv(GAPS_OUT, sep="\t", index=False)
    models.to_csv(MODELS_OUT, sep="\t", index=False)

    print(f"wrote {PANEL_OUT}")
    print(f"wrote {GAPS_OUT}")
    print(f"wrote {MODELS_OUT}")


if __name__ == "__main__":
    main()
