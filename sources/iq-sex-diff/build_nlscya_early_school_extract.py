#!/usr/bin/env python3
"""Build a compact early-school extract from the NLSCYA public CSV."""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import zipfile
from pathlib import Path


KEEP_GROUPS = {
    "child_id",
    "sex",
    "birth_year",
    "first_survey_year",
    "assessment_age_months",
    "assessment_grade",
    "assessment_status",
    "child_sampling_weight",
    "piat_math_raw",
    "piat_math_std",
    "piat_math_percentile",
    "piat_reading_recog_raw",
    "piat_reading_comp_raw",
    "piat_reading_comp_std",
    "ppvt_raw",
    "ppvt_std",
    "ppvt_percentile",
}


def load_variable_map(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    rows = [row for row in rows if row["group"] in KEEP_GROUPS]

    def row_priority(row: dict[str, str]) -> tuple[int, int]:
        alias = row["alias"].upper()
        label = row["label"].upper()
        revised = 1 if ("REV" in alias or "REVISED" in label) else 0
        has_alias = 1 if alias else 0
        return (revised, has_alias)

    deduped: list[dict[str, str]] = []
    seen_non_year_groups: set[str] = set()
    seen_group_year: set[tuple[str, str]] = set()

    by_group_year: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = (row["group"], row["year"])
        best = by_group_year.get(key)
        if best is None or row_priority(row) > row_priority(best):
            by_group_year[key] = row

    rows = sorted(by_group_year.values(), key=lambda row: (row["group"], row["year"], row["code"]))
    for row in rows:
        if row["group"] in {"child_id", "sex", "birth_year", "first_survey_year"}:
            if row["group"] in seen_non_year_groups:
                continue
            seen_non_year_groups.add(row["group"])
        else:
            key = (row["group"], row["year"])
            if key in seen_group_year:
                continue
            seen_group_year.add(key)
        deduped.append(row)
    return deduped


def sanitize_header(value: str) -> str:
    return value.strip().strip('"')


def column_name(row: dict[str, str]) -> str:
    alias = row["alias"].strip()
    return alias if alias else row["code"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--zip-path",
        type=Path,
        default=Path("sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip"),
    )
    parser.add_argument(
        "--csv-member",
        default="nlscya_all_1979-2020.csv",
    )
    parser.add_argument(
        "--variable-map",
        type=Path,
        default=Path("sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv"),
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz"),
    )
    args = parser.parse_args()

    rows = load_variable_map(args.variable_map)
    selected_codes = [row["code"] for row in rows]

    with zipfile.ZipFile(args.zip_path) as zf:
        with zf.open(args.csv_member) as raw_fh:
            text_fh = io.TextIOWrapper(raw_fh, encoding="utf-8", errors="ignore", newline="")
            reader = csv.reader(text_fh)
            header = [sanitize_header(value) for value in next(reader)]
            index = {name: idx for idx, name in enumerate(header)}

            missing = [code for code in selected_codes if code not in index]
            if missing:
                raise KeyError(f"missing columns in csv header: {missing}")

            args.output_path.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(args.output_path, "wt", encoding="utf-8", newline="") as out_fh:
                writer = csv.writer(out_fh, delimiter="\t")
                writer.writerow([column_name(row) for row in rows])

                count = 0
                for record in reader:
                    writer.writerow([record[index[row["code"]]] for row in rows])
                    count += 1

    print(f"wrote {count} rows to {args.output_path}")


if __name__ == "__main__":
    main()
