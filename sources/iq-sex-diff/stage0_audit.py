#!/usr/bin/env python3
"""Stage 0 audit for local IQ sex-differences datasets."""

from __future__ import annotations

import argparse
import csv
import json
import zipfile
from pathlib import Path

from stage0_config import ICAR, NLSY79, NLSY97, PIAAC


def count_plain_rows(path: Path) -> int:
    with path.open("rb") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def count_zip_rows(path: Path, member: str) -> int:
    with zipfile.ZipFile(path) as archive:
        with archive.open(member) as handle:
            return max(sum(1 for _ in handle) - 1, 0)


def required_presence(header: list[str], required: list[str]) -> dict[str, bool]:
    header_set = set(header)
    return {column: column in header_set for column in required}


def normalize_columns(columns: list[str]) -> list[str]:
    return [column.strip().strip('"') for column in columns]


def detect_delimiter(path: Path) -> str:
    with path.open("r", encoding="latin-1") as handle:
        line = handle.readline()
    if "|" in line:
        return "|"
    if ";" in line:
        return ";"
    return ","


def header_from_plain_csv(path: Path, delimiter: str) -> list[str]:
    with path.open("r", encoding="latin-1") as handle:
        return normalize_columns(handle.readline().rstrip("\n").split(delimiter))


def header_from_zip_csv(path: Path, member: str) -> list[str]:
    with zipfile.ZipFile(path) as archive:
        with archive.open(member) as handle:
            return normalize_columns(
                handle.readline().decode("latin-1").rstrip("\n").split(",")
            )


def audit_icar() -> dict[str, object]:
    required = ["gender", "age"] + sum(ICAR["domains"].values(), [])
    header = header_from_plain_csv(ICAR["path"], ICAR["delimiter"])
    return {
        "rows": count_plain_rows(ICAR["path"]),
        "columns": len(header),
        "required_columns_present": required_presence(header, required),
        "estimation_mode": ICAR["estimation_mode"],
    }


def audit_nlsy(dataset: dict[str, object]) -> dict[str, object]:
    required = [
        dataset["id"]["code"],
        dataset["sex"]["code"],
        dataset["age"]["baseline"]["code"] if "age" in dataset else None,
        dataset["weights"]["cross_section_1979"]["code"]
        if dataset is NLSY79
        else dataset["weights"]["cross_section_1997"]["code"],
    ]
    if dataset is NLSY79:
        required.extend(
            [
                dataset["household_id"]["code"],
                dataset["weights"]["asvab_1981"]["code"],
                *[slot["id"] for slot in dataset["pair_link_slots"]],
                *[slot["relation"] for slot in dataset["pair_link_slots"]],
                *[slot["sibling_marker"] for slot in dataset["pair_link_slots"]],
                *[
                    metadata["code"]
                    for metadata in dataset["primary_subtests"].values()
                ],
            ]
        )
    else:
        required.extend(
            score["code"] for score in dataset["summary_scores"].values()
        )
        for ability in dataset["ability_scores"].values():
            required.extend([ability["pos"], ability["neg"]])

    required = [item for item in required if item]
    header = header_from_zip_csv(dataset["path"], dataset["zip_member"])
    return {
        "rows": count_zip_rows(dataset["path"], dataset["zip_member"]),
        "columns": len(header),
        "required_columns_present": required_presence(header, required),
        "estimation_mode": dataset["estimation_mode"],
    }


def audit_piaac() -> dict[str, object]:
    files = {}
    for path in PIAAC["paths"]:
        delimiter = detect_delimiter(path)
        header = header_from_plain_csv(path, delimiter)
        required = [
            PIAAC["sex"]["code"],
            PIAAC["id"]["code"],
            *PIAAC["education"],
            *PIAAC["scores"]["literacy"],
            *PIAAC["scores"]["numeracy"],
            *PIAAC["weights"]["replicates"][:1],
            PIAAC["weights"]["full_sample"],
            PIAAC["weights"]["variance_stratum"],
            PIAAC["weights"]["variance_unit"],
        ]
        files[path.name] = {
            "rows": count_plain_rows(path),
            "columns": len(header),
            "delimiter": {"|": "pipe", ";": "semicolon"}.get(delimiter, "comma"),
            "required_columns_present": required_presence(header, required),
        }
    return {"files": files, "estimation_mode": PIAAC["estimation_mode"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        help="Optional JSON output path",
    )
    args = parser.parse_args()

    report = {
        "datasets": {
            "icar": audit_icar(),
            "nlsy79": audit_nlsy(NLSY79),
            "nlsy97": audit_nlsy(NLSY97),
            "piaac": audit_piaac(),
        }
    }

    text = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote audit to {output_path}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
