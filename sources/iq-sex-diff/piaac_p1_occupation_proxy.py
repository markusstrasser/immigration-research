#!/usr/bin/env python3
"""PIAAC p1 occupation-skill proxy surface using ISCOSKIL4."""

from __future__ import annotations

import csv
import math

import numpy as np
import pandas as pd

from piaac_p1_stratified import DOMAIN_PVS, DATA_DIR, load_file, replicate_factor, weighted_effect


ISCO_SKILL_LABELS = {
    "1": "Skilled occupations",
    "2": "Semi-skilled white-collar",
    "3": "Semi-skilled blue-collar",
    "4": "Elementary occupations",
}


def estimate_cell(
    df: pd.DataFrame,
    meta: dict[str, str | int | float],
    domain: str,
    level: str,
) -> dict[str, object] | None:
    subset = df.loc[df["ISCOSKIL4"] == level].copy()
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
        "occupation_level": level,
        "occupation_label": ISCO_SKILL_LABELS[level],
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
    for domain, domain_df in results.groupby("domain"):
        for level, level_df in domain_df.groupby("occupation_level"):
            rows.append(
                {
                    "domain": domain,
                    "occupation_level": level,
                    "occupation_label": level_df["occupation_label"].iloc[0],
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
        for level in ISCO_SKILL_LABELS:
            for domain in DOMAIN_PVS:
                row = estimate_cell(df, meta, domain, level)
                if row is not None:
                    outputs.append(row)

    results = pd.DataFrame(outputs).sort_values(["domain", "occupation_level", "country_wave"])
    summary = summarize_results(results)

    output_path = DATA_DIR / "piaac_p1_iscoskil4_gaps.tsv"
    summary_path = DATA_DIR / "piaac_p1_iscoskil4_summary.tsv"
    results.to_csv(output_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)
    summary.to_csv(summary_path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)

    print(f"Wrote {output_path}")
    print(f"Wrote {summary_path}")
    print("Occupation proxy summary:")
    for domain in ["literacy", "numeracy", "problem_solving"]:
        domain_df = summary[summary["domain"] == domain]
        means = domain_df.set_index("occupation_level")["mean_gap_d"].to_dict()
        print(
            f"{domain:<16} "
            f"skilled={means.get('1', float('nan')):+.3f} "
            f"white={means.get('2', float('nan')):+.3f} "
            f"blue={means.get('3', float('nan')):+.3f} "
            f"elementary={means.get('4', float('nan')):+.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
