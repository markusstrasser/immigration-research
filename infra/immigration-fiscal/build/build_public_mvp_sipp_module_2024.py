#!/usr/bin/env python3
"""Build descriptive SIPP 2024 person-month cells (98-cell target grid).

These are pooled monthly levels, not estimated transitions or annual person
counts. Benefit units are allocated before selecting working-age adults.
"""
from __future__ import annotations

import csv
from pathlib import Path

from public_mvp_io import (
    PROTO, SIPP_BENEFIT_ALLOCATION, SIPP_NATIVITY_BASIS, SIPP_DICTIONARY_URL, SIPP_REFERENCE_YEAR,
    SIPP_SCHEMA, SIPP_ZIP, iter_sipp_allocated_sample_units, sipp_eeduc_bucket,
    sipp_working_age_band, write_meta,
)

OUT = PROTO / "sipp_public_mvp_cells_2024.csv"


def build(
    *, schema_path: Path = SIPP_SCHEMA, zip_path: Path = SIPP_ZIP,
    output_dir: Path = PROTO,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    cells: dict[tuple, dict] = {}
    n_rows = 0
    for sample in iter_sipp_allocated_sample_units(schema_path, zip_path):
        for person in sample:
            n_rows += 1
            if not person.in_universe or person.weight <= 0 or person.age is None:
                continue
            band = sipp_working_age_band(person.age)
            if band is None:
                continue
            if person.nativity not in (1, 2):
                raise ValueError(f"Invalid SIPP adult nativity: {person.nativity!r}")
            education = sipp_eeduc_bucket(person.education_code)
            key = (band, person.nativity, education)
            cell = cells.setdefault(key, {
                "age_band": band, "nativity_code": str(person.nativity),
                "nativity_label": "1 native (ACS definition)" if person.nativity == 1 else "2 foreign-born",
                "education_bucket": education,
                "sipp_person_month_weight_sum": 0.0, "person_month_rows": 0,
                "sum_tpearn": 0.0, "sum_tptotinc": 0.0,
                "sum_allocated_snap": 0.0, "sum_allocated_tanf": 0.0, "sum_person_ssi": 0.0,
                "positive_allocated_snap_weight": 0.0,
                "positive_allocated_tanf_weight": 0.0, "positive_person_ssi_weight": 0.0,
                "recent_arrival_weight": 0.0,
            })
            weight = person.weight
            cell["sipp_person_month_weight_sum"] += weight
            cell["person_month_rows"] += 1
            cell["sum_tpearn"] += person.earnings * weight
            cell["sum_tptotinc"] += person.income * weight
            for program, amount in (
                ("allocated_snap", person.allocated_snap),
                ("allocated_tanf", person.allocated_tanf), ("person_ssi", person.ssi),
            ):
                cell[f"sum_{program}"] += amount * weight
                if amount > 0:
                    cell[f"positive_{program}_weight"] += weight
            if person.nativity == 2 and person.entry_year is not None and person.entry_year >= 2014:
                cell["recent_arrival_weight"] += weight

    rows = []
    for _, cell in sorted(cells.items()):
        weight = cell["sipp_person_month_weight_sum"]
        rows.append({
            **{field: cell[field] for field in (
                "age_band", "nativity_code", "nativity_label", "education_bucket",
                "sipp_person_month_weight_sum", "person_month_rows",
            )},
            "mean_monthly_person_tpearn": cell["sum_tpearn"] / weight,
            "mean_monthly_person_tptotinc": cell["sum_tptotinc"] / weight,
            **{f"mean_monthly_{program}": cell[f"sum_{program}"] / weight
               for program in ("allocated_snap", "allocated_tanf", "person_ssi")},
            **{f"share_positive_{program}_pct": 100 * cell[f"positive_{program}_weight"] / weight
               for program in ("allocated_snap", "allocated_tanf", "person_ssi")},
            "share_recent_arrival_foreign_pct": 100 * cell["recent_arrival_weight"] / weight
                if cell["nativity_code"] == "2" else None,
        })
    if not rows:
        raise ValueError("No working-age SIPP person-month cells")
    out = output_dir / OUT.name
    with out.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_meta(output_dir / "sipp_public_mvp_cells_2024.meta.json", {
        "builder": "build_public_mvp_sipp_module_2024.py",
        "source_zip": str(zip_path), "dictionary": SIPP_DICTIONARY_URL,
        "reference_year": SIPP_REFERENCE_YEAR, "person_month_rows_scanned": n_rows,
        "cells_written": len(rows), "target_cells": 98, "output_csv": str(out),
        "grid": "7 age bands x 2 nativity x 7 education buckets; working age 25-64",
        "age_basis": "Monthly TAGE_EHC; education is December EEDUC",
        "weight_basis": "Monthly WPFINWGT; pooled weights count person-months, not unique adults",
        "benefit_allocation": SIPP_BENEFIT_ALLOCATION,
        "nativity_basis": SIPP_NATIVITY_BASIS,
        "notes": "Descriptive monthly levels, not observed transition rates; no citizenship-specific estimate",
    })
    print(f"Wrote {out} ({len(rows)} cells from {n_rows:,} person-month rows)")
    return out


if __name__ == "__main__":
    build()
