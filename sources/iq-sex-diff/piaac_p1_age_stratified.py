#!/usr/bin/env python3
"""PIAAC p1 age-stratified sex-gap surface with plausible values and replicate weights."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
import pandas as pd

from piaac_p1_stratified import DOMAIN_PVS, DATA_DIR, load_file, replicate_factor, weighted_effect


AGE10_LABELS = {
    "1": "24 or less",
    "2": "25-34",
    "3": "35-44",
    "4": "45-54",
    "5": "55 plus",
    "B": "66 plus",
}

AGE3_MAP = {
    "1": "young",
    "2": "young",
    "3": "middle",
    "4": "middle",
    "5": "older",
    "B": "older",
}

AGE3_LABELS = {
    "young": "24-34 or less",
    "middle": "35-54",
    "older": "55 plus",
}


def estimate_cell(
    df: pd.DataFrame,
    meta: dict[str, str | int | float],
    domain: str,
    scheme: str,
    level: str,
) -> dict[str, object] | None:
    if scheme == "age10":
        mask = df["AGEG10LFS_T"] == level
        level_label = AGE10_LABELS[level]
    elif scheme == "age3":
        mask = df["AGE3"] == level
        level_label = AGE3_LABELS[level]
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
        "age_level": level,
        "age_label": level_label,
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
    grouped = results[results["scheme"] == "age3"]
    for domain, domain_df in grouped.groupby("domain"):
        for level, level_df in domain_df.groupby("age_level"):
            rows.append(
                {
                    "domain": domain,
                    "age_level": level,
                    "age_label": level_df["age_label"].iloc[0],
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
        df = df.copy()
        df["AGE3"] = df["AGEG10LFS_T"].map(AGE3_MAP)
        for scheme, levels in {
            "age10": [key for key in AGE10_LABELS if key != "B"],
            "age3": list(AGE3_LABELS.keys()),
        }.items():
            for level in levels:
                for domain in DOMAIN_PVS:
                    row = estimate_cell(df, meta, domain, scheme, level)
                    if row is not None:
                        outputs.append(row)

    results = pd.DataFrame(outputs).sort_values(
        ["scheme", "domain", "age_level", "country_wave"]
    )
    summary = summarize_results(results)

    output_path = DATA_DIR / "piaac_p1_age_stratified_gaps.tsv"
    summary_path = DATA_DIR / "piaac_p1_age_grouped_summary.tsv"
    results.to_csv(output_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    summary.to_csv(summary_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)

    print(f"Wrote {output_path}")
    print(f"Wrote {summary_path}")
    print("Grouped age summary:")
    focus = results[results["scheme"] == "age3"]
    for domain in ["literacy", "numeracy", "problem_solving"]:
        domain_df = focus[focus["domain"] == domain]
        means = domain_df.groupby("age_level")["point_estimate_d"].mean().to_dict()
        print(
            f"{domain:<16} "
            f"young={means.get('young', float('nan')):+.3f} "
            f"middle={means.get('middle', float('nan')):+.3f} "
            f"older={means.get('older', float('nan')):+.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
