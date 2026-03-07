#!/usr/bin/env python3
"""TIMSS Advanced 2015 sex-gap surface for advanced mathematics."""

from __future__ import annotations

import csv
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from timss_common import ROOT, coerce_numeric, load_sav_from_zip, member_country_code, plausible_value_summary


DATA_DIR = ROOT / "data"
ADV_ZIP = DATA_DIR / "timss_advanced" / "TA15_SPSSData.zip"

CORE_COLS = ["ITSEX", "TOTWGT", "JKZONE", "JKREP"]

DOMAIN_PVS = {
    "overall_advanced_math": [f"MSMMAT{i:02d}" for i in range(1, 6)],
    "algebra": [f"MSMALG{i:02d}" for i in range(1, 6)],
    "calculus": [f"MSMCAL{i:02d}" for i in range(1, 6)],
    "geometry": [f"MSMGEO{i:02d}" for i in range(1, 6)],
    "knowing": [f"MSMKNO{i:02d}" for i in range(1, 6)],
    "applying": [f"MSMAPP{i:02d}" for i in range(1, 6)],
    "reasoning": [f"MSMREA{i:02d}" for i in range(1, 6)],
}


def member_list(zip_path: Path) -> list[str]:
    with ZipFile(zip_path) as archive:
        return sorted(
            member
            for member in archive.namelist()
            if member.lower().endswith(".sav") and member.upper().startswith("MAT/MSA")
        )


def summarize_results(results: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for domain, group in results.groupby("domain", sort=True):
        rows.append(
            {
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
    return pd.DataFrame(rows).sort_values("domain").reset_index(drop=True)


def write_tsv(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, sep="\t", index=False, quoting=csv.QUOTE_MINIMAL)


def main() -> int:
    members = member_list(ADV_ZIP)
    usecols = CORE_COLS + sorted({column for columns in DOMAIN_PVS.values() for column in columns})

    rows: list[dict[str, object]] = []
    for index, member in enumerate(members, start=1):
        country_code = member_country_code(member)
        print(f"[TIMSS Advanced] {index}/{len(members)} {country_code} {member}")
        frame = coerce_numeric(load_sav_from_zip(ADV_ZIP, member, usecols))
        for domain, pv_columns in DOMAIN_PVS.items():
            summary = plausible_value_summary(frame, pv_columns)
            if summary is None:
                continue
            rows.append(
                {
                    "country_code": country_code,
                    "member": member,
                    "domain": domain,
                    **summary,
                }
            )

    results = pd.DataFrame(rows).sort_values(["domain", "country_code"]).reset_index(drop=True)
    summary = summarize_results(results)

    output_dir = DATA_DIR / "timss_advanced"
    write_tsv(output_dir / "timss_advanced_2015_gaps.tsv", results)
    write_tsv(output_dir / "timss_advanced_2015_summary.tsv", summary)

    print()
    print("TIMSS Advanced summary:")
    for row in summary.itertuples(index=False):
        print(
            f"{row.domain:<22} mean_d={row.mean_gap_d:+.3f} "
            f"countries={row.country_count:>2d} "
            f"sig_female={row.significant_female_count:>2d} "
            f"sig_male={row.significant_male_count:>2d}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
