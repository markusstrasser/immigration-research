#!/usr/bin/env python3
"""Focused TIMSS cognitive/content split summary for the NLSY97 anomaly check."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
GRADE_GAPS = DATA_DIR / "timss_grade_compare" / "timss_2019_grade_gaps.tsv"
GRADE_SUMMARY = DATA_DIR / "timss_grade_compare" / "timss_2019_grade_summary.tsv"
PAIRED = DATA_DIR / "timss_grade_compare" / "timss_2019_grade_paired_deltas.tsv"
ADV_GAPS = DATA_DIR / "timss_advanced" / "timss_advanced_2015_gaps.tsv"
ADV_SUMMARY = DATA_DIR / "timss_advanced" / "timss_advanced_2015_summary.tsv"

FOCUS_GRADE_DOMAINS = [
    "overall_math",
    "number",
    "algebra",
    "geometry",
    "knowing",
    "applying",
    "reasoning",
]

FOCUS_ADV_DOMAINS = [
    "overall_advanced_math",
    "algebra",
    "calculus",
    "geometry",
    "knowing",
    "applying",
    "reasoning",
]


def write_tsv(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)


def build_domain_contrasts(grade_gaps: pd.DataFrame) -> pd.DataFrame:
    pivot = grade_gaps.pivot_table(
        index=["grade", "country_code"],
        columns="domain",
        values="point_estimate_d",
    ).reset_index()
    rows: list[dict[str, object]] = []
    for grade, group in pivot.groupby("grade", sort=True):
        for left, right in [("knowing", "applying"), ("knowing", "reasoning"), ("applying", "reasoning")]:
            valid = group[[left, right]].dropna()
            if valid.empty:
                continue
            delta = valid[left] - valid[right]
            rows.append(
                {
                    "grade": grade,
                    "contrast": f"{left}_minus_{right}",
                    "country_count": int(len(valid)),
                    "mean_delta_d": float(delta.mean()),
                    "median_delta_d": float(delta.median()),
                    "min_delta_d": float(delta.min()),
                    "max_delta_d": float(delta.max()),
                    "positive_count": int((delta > 0).sum()),
                    "negative_count": int((delta < 0).sum()),
                }
            )
    return pd.DataFrame(rows).sort_values(["grade", "contrast"]).reset_index(drop=True)


def build_advanced_contrasts(adv_gaps: pd.DataFrame) -> pd.DataFrame:
    pivot = adv_gaps.pivot_table(index="country_code", columns="domain", values="point_estimate_d").reset_index()
    rows: list[dict[str, object]] = []
    for left, right in [("knowing", "applying"), ("knowing", "reasoning"), ("applying", "reasoning")]:
        valid = pivot[[left, right]].dropna()
        if valid.empty:
            continue
        delta = valid[left] - valid[right]
        rows.append(
            {
                "contrast": f"{left}_minus_{right}",
                "country_count": int(len(valid)),
                "mean_delta_d": float(delta.mean()),
                "median_delta_d": float(delta.median()),
                "min_delta_d": float(delta.min()),
                "max_delta_d": float(delta.max()),
                "positive_count": int((delta > 0).sum()),
                "negative_count": int((delta < 0).sum()),
            }
        )
    return pd.DataFrame(rows).sort_values("contrast").reset_index(drop=True)


def main() -> int:
    grade_gaps = pd.read_csv(GRADE_GAPS, sep="\t")
    grade_summary = pd.read_csv(GRADE_SUMMARY, sep="\t")
    paired = pd.read_csv(PAIRED, sep="\t")
    adv_gaps = pd.read_csv(ADV_GAPS, sep="\t")
    adv_summary = pd.read_csv(ADV_SUMMARY, sep="\t")

    focus_grade_summary = grade_summary[grade_summary["domain"].isin(FOCUS_GRADE_DOMAINS)].copy()
    focus_grade_paired = paired[paired["domain"].isin([d for d in FOCUS_GRADE_DOMAINS if d not in {"algebra"}])].copy()
    focus_adv_summary = adv_summary[adv_summary["domain"].isin(FOCUS_ADV_DOMAINS)].copy()

    grade_contrasts = build_domain_contrasts(grade_gaps[grade_gaps["domain"].isin(["knowing", "applying", "reasoning"])].copy())
    advanced_contrasts = build_advanced_contrasts(
        adv_gaps[adv_gaps["domain"].isin(["knowing", "applying", "reasoning"])].copy()
    )

    output_dir = DATA_DIR / "timss_cognitive_split"
    write_tsv(output_dir / "timss_cognitive_grade_summary.tsv", focus_grade_summary)
    write_tsv(output_dir / "timss_cognitive_grade_paired.tsv", focus_grade_paired)
    write_tsv(output_dir / "timss_cognitive_grade_contrasts.tsv", grade_contrasts)
    write_tsv(output_dir / "timss_cognitive_advanced_summary.tsv", focus_adv_summary)
    write_tsv(output_dir / "timss_cognitive_advanced_contrasts.tsv", advanced_contrasts)

    print("TIMSS cognitive split summary")
    for row in focus_grade_summary.itertuples(index=False):
        print(
            f"{row.grade:<8} {row.domain:<16} "
            f"mean_d={row.mean_gap_d:+.3f} countries={row.country_count:>3d}"
        )
    print()
    print("Grade contrast summary")
    for row in grade_contrasts.itertuples(index=False):
        print(
            f"{row.grade:<8} {row.contrast:<24} "
            f"mean_delta={row.mean_delta_d:+.3f} countries={row.country_count:>3d}"
        )
    print()
    print("TIMSS Advanced contrast summary")
    for row in advanced_contrasts.itertuples(index=False):
        print(
            f"{row.contrast:<24} mean_delta={row.mean_delta_d:+.3f} countries={row.country_count:>3d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
