#!/usr/bin/env python3
"""Extract NLSY ASVAB/AFQT variable labels from bundled SAS syntax files.

This keeps the first pass of NLSY analysis reproducible without requiring SAS,
R, pandas, or manual inspection of the large cohort exports.
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import re
import sys
import zipfile


LABEL_RE = re.compile(r'^\s*label\s+([A-Z0-9]+)\s*=\s*"([^"]+)";')
ALIAS_RE = re.compile(r"^\s*([A-Z0-9]+)\s*=\s*'([^']+)'n")
# NLSY97 uses underscore-delimited aliases like ASVAB_GS_ABILITY_EST_POS_XRND,
# so strict word-boundary matching silently drops real CAT-ASVAB variables.
KEEP_RE = re.compile(r"(?:ASVAB|AFQT)", re.IGNORECASE)


def sas_member_name(zip_path: pathlib.Path) -> str:
    stem = zip_path.stem
    if not stem:
        raise ValueError(f"Could not infer member name from {zip_path}")
    return f"{stem}.sas"


def cohort_name(zip_path: pathlib.Path) -> str:
    name = zip_path.name.lower()
    if "nlsy79" in name:
        return "NLSY79"
    if "nlsy97" in name:
        return "NLSY97"
    return zip_path.stem


def extract_rows(zip_path: pathlib.Path) -> list[dict[str, str]]:
    labels: dict[str, str] = {}
    aliases: dict[str, str] = {}
    member = sas_member_name(zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(member) as raw:
            for line in raw:
                text = line.decode("latin-1").rstrip("\n")
                label_match = LABEL_RE.match(text)
                if label_match:
                    var, label = label_match.groups()
                    if KEEP_RE.search(label):
                        labels[var] = label
                    continue
                alias_match = ALIAS_RE.match(text)
                if alias_match:
                    var, alias = alias_match.groups()
                    if KEEP_RE.search(alias):
                        aliases[var] = alias

    variables = sorted(set(labels) | set(aliases))
    cohort = cohort_name(zip_path)
    rows = []
    for variable in variables:
        rows.append(
            {
                "cohort": cohort,
                "variable": variable,
                "alias": aliases.get(variable, ""),
                "label": labels.get(variable, ""),
            }
        )
    return rows


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_paths", nargs="+", help="NLSY cohort zip files")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output TSV path",
    )
    args = parser.parse_args(argv)

    rows: list[dict[str, str]] = []
    for zip_arg in args.zip_paths:
        rows.extend(extract_rows(pathlib.Path(zip_arg)))

    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["cohort", "variable", "alias", "label"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
