#!/usr/bin/env python3
"""PIAAC p1 education-stratified sex-gap surface with plausible values and replicate weights."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "piaac"

DOMAIN_PVS = {
    "literacy": [f"PVLIT{i}" for i in range(1, 11)],
    "numeracy": [f"PVNUM{i}" for i in range(1, 11)],
    "problem_solving": [f"PVPSL{i}" for i in range(1, 11)],
}

EDCAT6_LABELS = {
    "1": "Lower secondary or less",
    "2": "Upper secondary",
    "3": "Post-secondary non-tertiary",
    "4": "Tertiary professional",
    "5": "Tertiary bachelor",
    "6": "Tertiary master/research",
}

ED3_MAP = {
    "1": "low",
    "2": "middle",
    "3": "middle",
    "4": "high",
    "5": "high",
    "6": "high",
}

ED3_LABELS = {
    "low": "Lower secondary or less",
    "middle": "Upper/post-secondary non-tertiary",
    "high": "Any tertiary",
}

ALL_LABELS = {"all": "All education levels"}

FILE_LABELS = {
    "prgdeup1.csv": ("Germany", "DEU"),
    "prgfinp1.csv": ("Finland", "FIN"),
    "prgitap1.csv": ("Italy", "ITA"),
    "prgjpnp1.csv": ("Japan", "JPN"),
    "prgnldp1.csv": ("Netherlands", "NLD"),
    "prgusap1_2012.csv": ("USA 2012", "USA"),
    "prgusap1_2017.csv": ("USA 2017", "USA"),
}

MISSING_CODES = {"", ".", "-1", "-2", "-3", "-4", "-5", "N"}
MIN_N_PER_SEX = 30


def infer_delimiter(path: Path) -> str:
    with path.open("r", encoding="latin-1", newline="") as handle:
        first = handle.readline()
    if "|" in first:
        return "|"
    if ";" in first:
        return ";"
    return ","


def load_file(path: Path) -> tuple[pd.DataFrame, dict[str, str | int | float]]:
    usecols = [
        "CNTRYID_E",
        "CNTRY_E",
        "GENDER_R",
        "EDCAT6",
        "AGEG10LFS_T",
        "ISCOSKIL4",
        "ISCO1C",
        "ISCO2C",
        "ISIC1C",
        "ISIC2C",
        "VEMETHOD",
        "VEFAYFAC",
        "VENREPS",
        "SPFWT0",
    ]
    usecols.extend([f"SPFWT{i}" for i in range(1, 81)])
    for columns in DOMAIN_PVS.values():
        usecols.extend(columns)

    delimiter = infer_delimiter(path)
    df = pd.read_csv(
        path,
        sep=delimiter,
        usecols=lambda c: c in set(usecols),
        encoding="latin-1",
        dtype=str,
        low_memory=False,
    )

    meta = {
        "file_name": path.name,
        "country_label": FILE_LABELS[path.name][0],
        "country_code": FILE_LABELS[path.name][1],
        "delimiter": delimiter,
        "method": str(df["VEMETHOD"].dropna().mode().iloc[0]),
        "fay": float(pd.to_numeric(df["VEFAYFAC"], errors="coerce").dropna().iloc[0]),
        "n_reps": int(pd.to_numeric(df["VENREPS"], errors="coerce").dropna().iloc[0]),
    }

    numeric_cols = [col for col in df.columns if col.startswith("PV") or col.startswith("SPFWT")]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["GENDER_R"] = df["GENDER_R"].where(~df["GENDER_R"].isin(MISSING_CODES))
    df["EDCAT6"] = df["EDCAT6"].where(~df["EDCAT6"].isin(MISSING_CODES))
    if "AGEG10LFS_T" in df.columns:
        df["AGEG10LFS_T"] = df["AGEG10LFS_T"].where(~df["AGEG10LFS_T"].isin(MISSING_CODES))
    for col in ["ISCOSKIL4", "ISCO1C", "ISCO2C", "ISIC1C", "ISIC2C"]:
        if col in df.columns:
            df[col] = df[col].where(~df[col].isin(MISSING_CODES))
    df = df.copy()
    df["ED3"] = df["EDCAT6"].map(ED3_MAP)
    return df, meta


def weighted_effect(values: np.ndarray, weights: np.ndarray, sex: np.ndarray) -> tuple[float, int, int] | None:
    female_mask = sex == "2"
    male_mask = sex == "1"
    valid = np.isfinite(values) & np.isfinite(weights) & (weights > 0) & (female_mask | male_mask)
    if not valid.any():
        return None
    female = valid & female_mask
    male = valid & male_mask
    n_female = int(female.sum())
    n_male = int(male.sum())
    if n_female < MIN_N_PER_SEX or n_male < MIN_N_PER_SEX:
        return None

    female_values = values[female]
    male_values = values[male]
    female_weights = weights[female]
    male_weights = weights[male]
    mu_f = np.average(female_values, weights=female_weights)
    mu_m = np.average(male_values, weights=male_weights)
    var_f = np.average((female_values - mu_f) ** 2, weights=female_weights)
    var_m = np.average((male_values - mu_m) ** 2, weights=male_weights)
    pooled = (
        female_weights.sum() * var_f + male_weights.sum() * var_m
    ) / (female_weights.sum() + male_weights.sum())
    if pooled <= 0:
        return None
    d = (mu_f - mu_m) / math.sqrt(pooled)
    return float(d), n_female, n_male


def replicate_factor(method: str, n_reps: int, fay: float) -> float:
    if method == "JK2":
        return 1.0
    if method == "JK1":
        return (n_reps - 1) / n_reps
    if method == "BRR":
        return 1.0 / n_reps
    if method == "FAY":
        return 1.0 / (n_reps * (1.0 - fay) ** 2)
    raise ValueError(f"Unsupported replication method: {method}")


def estimate_cell(
    df: pd.DataFrame,
    meta: dict[str, str | int | float],
    domain: str,
    scheme: str,
    level: str,
) -> dict[str, object] | None:
    if scheme == "edcat6":
        mask = df["EDCAT6"] == level
        level_label = EDCAT6_LABELS[level]
    elif scheme == "ed3":
        mask = df["ED3"] == level
        level_label = ED3_LABELS[level]
    elif scheme == "all":
        mask = df["EDCAT6"].notna()
        level_label = ALL_LABELS[level]
    else:
        raise ValueError(f"Unknown scheme {scheme}")

    subset = df.loc[mask].copy()
    if subset.empty:
        return None

    estimates: list[float] = []
    sampling_vars: list[float] = []
    n_female = n_male = 0
    rep_factor = replicate_factor(str(meta["method"]), int(meta["n_reps"]), float(meta["fay"]))
    rep_cols = [f"SPFWT{i}" for i in range(1, int(meta["n_reps"]) + 1)]
    sex = subset["GENDER_R"].to_numpy()

    for i, pv_col in enumerate(DOMAIN_PVS[domain], start=1):
        values = subset[pv_col].to_numpy(dtype=float)
        full = weighted_effect(values, subset["SPFWT0"].to_numpy(dtype=float), sex)
        if full is None:
            continue
        q, nf, nm = full
        if i == 1:
            n_female, n_male = nf, nm
        rep_estimates = []
        for rep_col in rep_cols:
            qr = weighted_effect(values, subset[rep_col].to_numpy(dtype=float), sex)
            if qr is None:
                continue
            rep_estimates.append(qr[0])
        if len(rep_estimates) != len(rep_cols):
            continue
        estimates.append(q)
        sampling_vars.append(rep_factor * float(np.sum((np.array(rep_estimates) - q) ** 2)))

    if len(estimates) < 2:
        return None

    point = float(np.mean(estimates))
    sampling_var = float(np.mean(sampling_vars))
    imputation_var = float((1.0 + 1.0 / len(estimates)) * np.var(estimates, ddof=1))
    total_var = sampling_var + imputation_var
    se = math.sqrt(total_var)
    return {
        "country_wave": meta["country_label"],
        "country_code": meta["country_code"],
        "file_name": meta["file_name"],
        "scheme": scheme,
        "education_level": level,
        "education_label": level_label,
        "domain": domain,
        "n_female": n_female,
        "n_male": n_male,
        "point_estimate_d": point,
        "se_d": se,
        "ci_low": point - 1.96 * se,
        "ci_high": point + 1.96 * se,
        "sampling_var": sampling_var,
        "imputation_var": imputation_var,
        "total_var": total_var,
        "method": meta["method"],
        "fay_factor": meta["fay"],
        "n_reps": meta["n_reps"],
        "n_pvs_used": len(estimates),
    }


def summarize_results(results: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = results[results["scheme"] == "ed3"]
    for domain, domain_df in grouped.groupby("domain"):
        for level, level_df in domain_df.groupby("education_level"):
            rows.append(
                {
                    "domain": domain,
                    "education_level": level,
                    "education_label": level_df["education_label"].iloc[0],
                    "country_wave_count": len(level_df),
                    "mean_gap_d": level_df["point_estimate_d"].mean(),
                    "min_gap_d": level_df["point_estimate_d"].min(),
                    "max_gap_d": level_df["point_estimate_d"].max(),
                    "range_gap_d": level_df["point_estimate_d"].max()
                    - level_df["point_estimate_d"].min(),
                    "sign_flip_present": (
                        (level_df["ci_low"] > 0).any() and (level_df["ci_high"] < 0).any()
                    ),
                }
            )
    return pd.DataFrame(rows)


def main() -> int:
    outputs: list[dict[str, object]] = []
    for path in sorted(DATA_DIR.glob("prg*p1*.csv")):
        print(f"Processing {path.name}...")
        df, meta = load_file(path)
        for scheme, levels in {
            "all": list(ALL_LABELS.keys()),
            "edcat6": list(EDCAT6_LABELS.keys()),
            "ed3": list(ED3_LABELS.keys()),
        }.items():
            for level in levels:
                for domain in DOMAIN_PVS:
                    row = estimate_cell(df, meta, domain, scheme, level)
                    if row is not None:
                        outputs.append(row)

    results = pd.DataFrame(outputs).sort_values(
        ["scheme", "domain", "education_level", "country_wave"]
    )
    summary = summarize_results(results)

    output_path = DATA_DIR / "piaac_p1_stratified_gaps.tsv"
    summary_path = DATA_DIR / "piaac_p1_grouped_summary.tsv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(output_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    summary.to_csv(summary_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)

    print(f"Wrote {output_path}")
    print(f"Wrote {summary_path}")
    print("Grouped education summary:")
    focus = results[results["scheme"] == "ed3"]
    for domain in ["literacy", "numeracy", "problem_solving"]:
        domain_df = focus[focus["domain"] == domain]
        means = domain_df.groupby("education_level")["point_estimate_d"].mean().to_dict()
        print(
            f"{domain:<16} "
            f"low={means.get('low', float('nan')):+.3f} "
            f"middle={means.get('middle', float('nan')):+.3f} "
            f"high={means.get('high', float('nan')):+.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
