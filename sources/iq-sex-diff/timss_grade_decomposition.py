#!/usr/bin/env python3
"""TIMSS 2019 grade-surface sex-gap decomposition for Grade 4 and Grade 8."""

from __future__ import annotations

import csv
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from timss_common import ROOT, coerce_numeric, load_sav_from_zip, member_country_code, plausible_value_summary


DATA_DIR = ROOT / "data"
G4_ZIP = DATA_DIR / "timss_grade4" / "T19_G4_SPSS%20Data.zip"
G8_ZIP = DATA_DIR / "timss" / "T19_G8_SPSS%20Data.zip"

CORE_COLS = ["ITSEX", "TOTWGT", "JKZONE", "JKREP"]

GRADE_CONFIGS = {
    "Grade 4": {
        "zip_path": G4_ZIP,
        "member_prefix": "asa",
        "domains": {
            "overall_math": [f"ASMMAT{i:02d}" for i in range(1, 6)],
            "overall_science": [f"ASSSCI{i:02d}" for i in range(1, 6)],
            "number": [f"ASMNUM{i:02d}" for i in range(1, 6)],
            "geometry": [f"ASMGEO{i:02d}" for i in range(1, 6)],
            "data": [f"ASMDAT{i:02d}" for i in range(1, 6)],
            "knowing": [f"ASMKNO{i:02d}" for i in range(1, 6)],
            "applying": [f"ASMAPP{i:02d}" for i in range(1, 6)],
            "reasoning": [f"ASMREA{i:02d}" for i in range(1, 6)],
        },
    },
    "Grade 8": {
        "zip_path": G8_ZIP,
        "member_prefix": "bsa",
        "domains": {
            "overall_math": [f"BSMMAT{i:02d}" for i in range(1, 6)],
            "overall_science": [f"BSSSCI{i:02d}" for i in range(1, 6)],
            "number": [f"BSMNUM{i:02d}" for i in range(1, 6)],
            "algebra": [f"BSMALG{i:02d}" for i in range(1, 6)],
            "geometry": [f"BSMGEO{i:02d}" for i in range(1, 6)],
            "data_probability": [f"BSMDAT{i:02d}" for i in range(1, 6)],
            "knowing": [f"BSMKNO{i:02d}" for i in range(1, 6)],
            "applying": [f"BSMAPP{i:02d}" for i in range(1, 6)],
            "reasoning": [f"BSMREA{i:02d}" for i in range(1, 6)],
        },
    },
}

COMMON_COMPARE_DOMAINS = [
    "overall_math",
    "overall_science",
    "number",
    "geometry",
    "knowing",
    "applying",
    "reasoning",
]


def member_list(zip_path: Path, prefix: str) -> list[str]:
    with ZipFile(zip_path) as archive:
        return sorted(
            member
            for member in archive.namelist()
            if member.lower().endswith("m7.sav")
            and "/" not in member
            and Path(member).name.lower().startswith(prefix)
        )


def process_grade(grade_label: str, config: dict[str, object]) -> list[dict[str, object]]:
    zip_path = Path(config["zip_path"])
    domains = dict(config["domains"])
    members = member_list(zip_path, str(config["member_prefix"]))
    usecols = CORE_COLS + sorted({column for cols in domains.values() for column in cols})

    rows: list[dict[str, object]] = []
    for index, member in enumerate(members, start=1):
        country_code = member_country_code(member)
        print(f"[{grade_label}] {index}/{len(members)} {country_code} {member}")
        frame = coerce_numeric(load_sav_from_zip(zip_path, member, usecols))
        for domain, pv_columns in domains.items():
            summary = plausible_value_summary(frame, pv_columns)
            if summary is None:
                continue
            rows.append(
                {
                    "grade": grade_label,
                    "country_code": country_code,
                    "member": member,
                    "domain": domain,
                    **summary,
                }
            )
    return rows


def summarize_by_grade(results: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for (grade, domain), group in results.groupby(["grade", "domain"], sort=True):
        rows.append(
            {
                "grade": grade,
                "domain": domain,
                "country_count": int(len(group)),
                "mean_gap_d": float(group["point_estimate_d"].mean()),
                "median_gap_d": float(group["point_estimate_d"].median()),
                "min_gap_d": float(group["point_estimate_d"].min()),
                "max_gap_d": float(group["point_estimate_d"].max()),
                "range_gap_d": float(group["point_estimate_d"].max() - group["point_estimate_d"].min()),
                "positive_count": int((group["point_estimate_d"] > 0).sum()),
                "negative_count": int((group["point_estimate_d"] < 0).sum()),
                "significant_female_count": int((group["ci_low"] > 0).sum()),
                "significant_male_count": int((group["ci_high"] < 0).sum()),
            }
        )
    return pd.DataFrame(rows).sort_values(["domain", "grade"]).reset_index(drop=True)


def paired_deltas(results: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    grade4 = results[results["grade"] == "Grade 4"].copy()
    grade8 = results[results["grade"] == "Grade 8"].copy()
    left = grade4[grade4["domain"].isin(COMMON_COMPARE_DOMAINS)][
        ["country_code", "domain", "point_estimate_d", "se_d", "ci_low", "ci_high"]
    ].rename(
        columns={
            "point_estimate_d": "grade4_d",
            "se_d": "grade4_se",
            "ci_low": "grade4_ci_low",
            "ci_high": "grade4_ci_high",
        }
    )
    right = grade8[grade8["domain"].isin(COMMON_COMPARE_DOMAINS)][
        ["country_code", "domain", "point_estimate_d", "se_d", "ci_low", "ci_high"]
    ].rename(
        columns={
            "point_estimate_d": "grade8_d",
            "se_d": "grade8_se",
            "ci_low": "grade8_ci_low",
            "ci_high": "grade8_ci_high",
        }
    )
    paired = left.merge(right, on=["country_code", "domain"], how="inner")
    paired["delta_g8_minus_g4_d"] = paired["grade8_d"] - paired["grade4_d"]

    summary_rows: list[dict[str, object]] = []
    for domain, group in paired.groupby("domain", sort=True):
        summary_rows.append(
            {
                "domain": domain,
                "country_count": int(len(group)),
                "mean_grade4_d": float(group["grade4_d"].mean()),
                "mean_grade8_d": float(group["grade8_d"].mean()),
                "mean_delta_g8_minus_g4_d": float(group["delta_g8_minus_g4_d"].mean()),
                "median_delta_g8_minus_g4_d": float(group["delta_g8_minus_g4_d"].median()),
                "min_delta_g8_minus_g4_d": float(group["delta_g8_minus_g4_d"].min()),
                "max_delta_g8_minus_g4_d": float(group["delta_g8_minus_g4_d"].max()),
                "more_male_at_grade8_count": int((group["delta_g8_minus_g4_d"] < 0).sum()),
                "more_female_at_grade8_count": int((group["delta_g8_minus_g4_d"] > 0).sum()),
            }
        )
    summary = pd.DataFrame(summary_rows).sort_values("domain").reset_index(drop=True)
    return paired.sort_values(["domain", "country_code"]).reset_index(drop=True), summary


def write_tsv(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)


def main() -> int:
    all_rows: list[dict[str, object]] = []
    for grade_label, config in GRADE_CONFIGS.items():
        all_rows.extend(process_grade(grade_label, config))

    results = pd.DataFrame(all_rows).sort_values(["grade", "domain", "country_code"]).reset_index(drop=True)
    summary = summarize_by_grade(results)
    paired, paired_summary = paired_deltas(results)

    output_dir = DATA_DIR / "timss_grade_compare"
    write_tsv(output_dir / "timss_2019_grade_gaps.tsv", results)
    write_tsv(output_dir / "timss_2019_grade_summary.tsv", summary)
    write_tsv(output_dir / "timss_2019_grade_paired_deltas.tsv", paired)
    write_tsv(output_dir / "timss_2019_grade_paired_summary.tsv", paired_summary)

    print()
    print("Grade-level summary:")
    for row in summary.itertuples(index=False):
        print(
            f"{row.domain:<16} {row.grade:<8} "
            f"mean_d={row.mean_gap_d:+.3f} "
            f"countries={row.country_count:>3d} "
            f"sig_female={row.significant_female_count:>3d} "
            f"sig_male={row.significant_male_count:>3d}"
        )
    print()
    print("Paired grade-8 minus grade-4 deltas:")
    for row in paired_summary.itertuples(index=False):
        print(
            f"{row.domain:<16} mean_delta={row.mean_delta_g8_minus_g4_d:+.3f} "
            f"countries={row.country_count:>3d} "
            f"more_male_g8={row.more_male_at_grade8_count:>3d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
