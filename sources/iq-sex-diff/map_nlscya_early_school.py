#!/usr/bin/env python3
"""Build a focused early-school variable map for the NLSCYA public release."""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from pathlib import Path


LABEL_RE = re.compile(r'^\s*label\s+([A-Z0-9]+)\s*=\s*"([^"]*)";')
ALIAS_RE = re.compile(r"^\s*([A-Z0-9]+)\s*=\s*'([^']+)'n")


def infer_year(label: str) -> str:
    match = re.search(r"(19\d{2}|20\d{2})$", label)
    if match:
        return match.group(1)
    match = re.search(r"(\d{2})$", label)
    if match:
        yy = int(match.group(1))
        return f"19{yy:02d}" if yy >= 79 else f"20{yy:02d}"
    return ""


def classify_label(label: str) -> str | None:
    upper = label.upper()
    if upper == "ID CODE OF CHILD":
        return "child_id"
    if upper == "SEX OF CHILD":
        return "sex"
    if upper.startswith("DATE OF BIRTH OF CHILD - YEAR"):
        return "birth_year"
    if upper.startswith("1ST SURVEY YEAR FOLLOWING BIRTH OF CHILD"):
        return "first_survey_year"
    if upper.startswith("CHILD AGE AT CHILD SUPP ASSESS DATE"):
        return "assessment_age_months"
    if upper.startswith("CHILD GRADE - CHILD SUPP ASSESS DATE"):
        return "assessment_grade"
    if upper.startswith("ASSESSMENT STATUS OF CHILD"):
        return "assessment_status"
    if upper.startswith("CHILD SAMPLING WEIGHT"):
        return "child_sampling_weight"
    if upper.startswith("PIAT MATH: RAW SCORE"):
        return "piat_math_raw"
    if upper.startswith("PIAT MATH: TOTAL STD SCORE"):
        return "piat_math_std"
    if upper.startswith("PIAT MATH: TOTAL PCTILE SCORE"):
        return "piat_math_percentile"
    if upper.startswith("PIAT READING RECOG: RAW SCORE"):
        return "piat_reading_recog_raw"
    if upper.startswith("PIAT READING COMP: RAW SCORE"):
        return "piat_reading_comp_raw"
    if upper.startswith("PIAT READ COMP: TOTAL STD SCORE"):
        return "piat_reading_comp_std"
    if upper.startswith("PPVT: TOTAL RAW SCORE"):
        return "ppvt_raw"
    if upper.startswith("PPVT: TOTAL STD SCORE"):
        return "ppvt_std"
    if upper.startswith("PPVT: TOTAL PCTILE SCORE"):
        return "ppvt_percentile"
    return None


def parse_sas(zip_path: Path, sas_member: str) -> tuple[dict[str, str], dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        text = zf.read(sas_member).decode("latin1", errors="ignore").splitlines()

    labels: dict[str, str] = {}
    aliases: dict[str, str] = {}

    for line in text:
        label_match = LABEL_RE.match(line)
        if label_match:
            code, label = label_match.groups()
            labels[code] = label
            continue
        alias_match = ALIAS_RE.match(line)
        if alias_match:
            code, alias = alias_match.groups()
            aliases[code] = alias

    return labels, aliases


def build_rows(labels: dict[str, str], aliases: dict[str, str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for code, label in labels.items():
        group = classify_label(label)
        if not group:
            continue
        rows.append(
            {
                "group": group,
                "year": infer_year(label),
                "code": code,
                "alias": aliases.get(code, ""),
                "label": label,
            }
        )

    rows.sort(key=lambda row: (row["group"], row["year"], row["code"]))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--zip-path",
        type=Path,
        default=Path("sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip"),
    )
    parser.add_argument(
        "--sas-member",
        default="nlscya_all_1979-2020.sas",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv"),
    )
    args = parser.parse_args()

    labels, aliases = parse_sas(args.zip_path, args.sas_member)
    rows = build_rows(labels, aliases)

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    with args.output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["group", "year", "code", "alias", "label"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {args.output_path}")


if __name__ == "__main__":
    main()
