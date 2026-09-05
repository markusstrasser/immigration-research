#!/usr/bin/env python3
"""Describe measured SPI race/ethnicity, birthplace and citizenship jointly.

Native-First: direct pandas/pyreadstat tabulation of the held source; no database.
Outputs are prisoner composition, never population offending/incarceration rates.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

import numpy as np
import pandas as pd
import pyreadstat


RACE = {1: "non_hispanic_white", 2: "non_hispanic_black", 3: "hispanic_any_race",
        4: "non_hispanic_aian", 5: "non_hispanic_asian_nhpi",
        6: "non_hispanic_multiracial", 8: "non_hispanic_other",
        9: "race_ethnicity_unresolved", -9: "race_ethnicity_unresolved"}
COLUMNS = ["RV0001", "RV0003", "RV0004", "V0945", "V0951", "V1951",
           "V1952", "V1953", "V1954", "V1955", "V1956", "V1957", "V1585"]
MISSING = {-9, -8, -2, -1}


def classify(frame: pd.DataFrame) -> pd.DataFrame:
    absent = set(COLUMNS) - set(frame)
    if absent:
        raise ValueError(f"Missing required SPI fields: {sorted(absent)}")
    df = frame.copy()
    for field, valid in [("RV0003", set(RACE)), ("RV0004", {1, 2, 8, -9}),
                         ("V0945", {1, 2} | MISSING)]:
        invalid = set(df[field].dropna().unique()) - valid
        if invalid:
            raise ValueError(f"Undocumented codes in {field}: {sorted(invalid)}")
    for field in ["V1951", "V1952", "V1953", "V1954", "V1955", "V1956", "V1957"]:
        if not df[field].dropna().isin({1, 2} | MISSING).all():
            raise ValueError(f"Undocumented response codes in {field}")
    if not np.isfinite(df.V1585).all() or (df.V1585 < 0).any() or df.V1585.sum() <= 0:
        raise ValueError("Weights must be finite, nonnegative and have a positive total")
    if not np.isfinite(df.RV0001).all() or (df.RV0001 < 18).any():
        raise ValueError("Source must contain the SPI adult respondent universe")
    if ((df.V1951 == 1) & (df.RV0003 != 3)).any() or ((df.V1951 == 2) & (df.RV0003 == 3)).any():
        raise ValueError("Official recode contradicts a known Hispanic response")
    # BJS source syntax lines 60-80: Hispanic takes precedence; then 2+ races.
    race_count = df[["V1952", "V1953", "V1954", "V1955", "V1956", "V1957"]].eq(1).sum(axis=1)
    reconstructed = np.select(
        [df.V1951.eq(1), race_count.ge(2), df.V1952.eq(1), df.V1953.eq(1),
         df.V1954.eq(1), df.V1955.eq(1), df.V1956.eq(1), df.V1957.eq(1)],
        [3, 6, 1, 2, 4, 5, 5, 8], default=9)
    if not np.array_equal(reconstructed, df.RV0003.to_numpy()):
        raise ValueError("RV0003 differs from the archived BJS reconstruction syntax")
    df["race_official"] = df.RV0003.map(RACE).fillna("race_ethnicity_unresolved")
    df["ethnicity_observed"] = df.V1951.isin([1, 2])
    df["race_explicit_ethnicity"] = df.race_official.where(df.ethnicity_observed, "ethnicity_unresolved")
    df["birthplace"] = df.V0945.map({1: "reported_us", 2: "reported_other_country"}).fillna("birthplace_unresolved")
    df["citizenship"] = df.RV0004.map({1: "us_citizen", 2: "noncitizen"}).fillna("citizenship_unresolved")
    return df


def composition(df: pd.DataFrame) -> pd.DataFrame:
    pieces = []
    masks = {"all_prisoners": pd.Series(True, index=df.index)}
    for field in ["birthplace", "citizenship"]:
        masks.update({f"{field}:{group}": df[field].eq(group) for group in sorted(df[field].unique())})
    for universe, mask in masks.items():
        subset = df.loc[mask]
        total = float(subset.V1585.sum())
        for basis in ["race_official", "race_explicit_ethnicity"]:
            table = subset.groupby(basis, dropna=False).agg(sample_n=("V1585", "size"), weighted_prisoners=("V1585", "sum")).reset_index(names="race_ethnicity")
            table["classification_basis"] = basis
            table["prisoner_universe"] = universe
            table["prisoner_denominator"] = total
            table["share_of_prisoner_universe_pct"] = table.weighted_prisoners / total * 100
            pieces.append(table)
    return pd.concat(pieces, ignore_index=True)


def ethnicity_bounds(df: pd.DataFrame) -> pd.DataFrame:
    unknown = ~df.ethnicity_observed
    total = float(df.V1585.sum())
    definitions = {
        "hispanic_any_race": (df.V1951.eq(1), unknown),
        "non_hispanic_black_any_race_indicator": (df.V1951.eq(2) & df.V1953.eq(1), unknown & df.V1953.eq(1)),
        "non_hispanic_white_any_race_indicator": (df.V1951.eq(2) & df.V1952.eq(1), unknown & df.V1952.eq(1)),
        "non_hispanic_black_official_single_race": (df.V1951.eq(2) & df.RV0003.eq(2), unknown & df.RV0003.eq(2)),
        "non_hispanic_white_official_single_race": (df.V1951.eq(2) & df.RV0003.eq(1), unknown & df.RV0003.eq(1)),
    }
    rows = []
    for group, (known, extra) in definitions.items():
        low, extra_weight = float(df.loc[known, "V1585"].sum()), float(df.loc[extra, "V1585"].sum())
        rows.append({"group": group, "known_sample_n": int(known.sum()), "unknown_ethnicity_sample_n": int(extra.sum()),
                     "weighted_lower": low, "weighted_upper": low + extra_weight,
                     "lower_share_of_all_prisoners_pct": low / total * 100,
                     "upper_share_of_all_prisoners_pct": (low + extra_weight) / total * 100})
    return pd.DataFrame(rows)


def file_hash(path: Path) -> dict:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest}


def published_adult_rates(report: Path) -> pd.DataFrame:
    """Read the official Table 6; do not splice it into the SPI microdata."""
    text = subprocess.run(["pdftotext", "-f", "14", "-l", "14", "-layout", str(report), "-"],
                          check=True, capture_output=True, text=True).stdout
    if "TABLE 6" not in text or "adult U.S. residents" not in text:
        raise ValueError("BJS report page does not match the expected adult-rate table")
    rows = []
    for line in text.splitlines():
        tokens = line.split()
        if tokens and tokens[0] in {str(year) for year in range(2013, 2024)}:
            if len(tokens) != 11:
                raise ValueError(f"BJS Table 6 schema changed: {line}")
            rows.append([int(token.replace(",", "")) for token in tokens])
    columns = ["year", "total", "federal", "state", "male", "female", "non_hispanic_white",
               "non_hispanic_black", "hispanic_any_race", "non_hispanic_aian", "non_hispanic_asian_nhpi"]
    table = pd.DataFrame(rows, columns=columns)
    if table.year.tolist() != list(range(2013, 2024)):
        raise ValueError("BJS adult-rate years missing, duplicated or out of order")
    return table


def analyze(data_root: Path, output: Path, bjs_report: Path | None = None) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    root = data_root / "external/crime_frontier"
    spi_path = root / "spi/ICPSR_37692/DS0001/37692-0001-Data.dta"
    raw, metadata = pyreadstat.read_dta(str(spi_path), usecols=COLUMNS)
    df = classify(raw)
    tables = composition(df)
    tables.to_csv(output / "spi_race_composition.csv", index=False)
    for basis in ["race_official", "race_explicit_ethnicity"]:
        joint = df.groupby([basis, "birthplace", "citizenship"], dropna=False).agg(sample_n=("V1585", "size"), weighted_prisoners=("V1585", "sum")).reset_index()
        joint.to_csv(output / f"spi_joint_{basis}.csv", index=False)
    bounds = ethnicity_bounds(df)
    bounds.to_csv(output / "spi_unknown_ethnicity_bounds.csv", index=False)
    pd.crosstab(df.RV0003, df.V1951, dropna=False).to_csv(output / "spi_recode_ethnicity_audit.csv")
    indicator = []
    for name, mask in {"black_any_race_any_ethnicity": df.V1953.eq(1),
                       "white_any_race_any_ethnicity": df.V1952.eq(1),
                       "black_and_hispanic": df.V1953.eq(1) & df.V1951.eq(1),
                       "white_and_hispanic": df.V1952.eq(1) & df.V1951.eq(1),
                       "black_and_white_indicators": df.V1953.eq(1) & df.V1952.eq(1)}.items():
        indicator.append({"group": name, "sample_n": int(mask.sum()), "weighted_prisoners": float(df.loc[mask, "V1585"].sum())})
    pd.DataFrame(indicator).to_csv(output / "spi_overlapping_race_indicators.csv", index=False)
    light_schema = {}
    light_zip = root / "light_texas/124923-V1.zip"
    with zipfile.ZipFile(light_zip) as archive:
        for name in archive.namelist():
            if name.endswith(".dta"):
                data = pd.read_stata(io.BytesIO(archive.read(name)), convert_categoricals=False)
                light_schema[name] = {"rows": len(data), "columns": list(data.columns)}
    unknown = ~df.ethnicity_observed
    summary = {
        "survey_year": 2016, "release_version_date": "2024-03-28",
        "sample_n": len(df), "weighted_prisoners": float(df.V1585.sum()),
        "ethnicity_unknown_n": int(unknown.sum()),
        "ethnicity_unknown_weighted": float(df.loc[unknown, "V1585"].sum()),
        "ethnicity_unknown_assigned_official_nh_n": int((unknown & df.RV0003.isin([1, 2, 4, 5, 6, 8])).sum()),
        "official_race_reconstruction_matches": True,
        "official_classification": tables.loc[(tables.classification_basis == "race_official") & (tables.prisoner_universe == "all_prisoners")].to_dict("records"),
        "unknown_ethnicity_bounds": bounds.to_dict("records"),
        "overlapping_indicators": indicator,
        "spi_population_rates": "NOT ESTIMATED: no matched population denominator",
        "nativity_limit": "V0945 records US versus other-country birthplace; citizenship at birth is unavailable, so this is not Census nativity",
        "status_limit": "RV0004 records current citizenship, not authorized/unauthorized or admission status",
        "uncertainty": "Weighted point descriptions; sampling/design uncertainty not computed; ethnicity bounds are deterministic, not confidence intervals",
        "source_hashes": [file_hash(p) for p in [spi_path, spi_path.with_name("37692-0001-Codebook.pdf"), light_zip]],
    }
    if bjs_report is not None:
        adult = published_adult_rates(bjs_report)
        adult.to_csv(output / "bjs_p23st_table6_adult_rates.csv", index=False)
        summary["bjs_recent_adult_imprisonment_rates"] = {
            "publication_date": "2025-09-30", "source": "https://bjs.ojp.gov/document/p23st.pdf",
            "unit": "sentenced prisoners age18+ with sentence >1 year per 100,000 adults in the same race/ethnicity group",
            "population_reference": "Census residents January 1 of following year; prisoner stock December 31",
            "rows": adult.loc[adult.year.ge(2022)].to_dict("records"),
            "limit": "Official adjusted race-only rates; no nativity or citizenship decomposition; not age/sex standardized",
        }
        summary["source_hashes"].append(file_hash(bjs_report))
    (output / "numerical-results.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    (output / "source-schema.json").write_text(json.dumps({"spi_fields": metadata.column_names_to_labels, "light_all_dta": light_schema}, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bjs-report", type=Path)
    args = parser.parse_args()
    result = analyze(args.data_root, args.output, args.bjs_report)
    print(json.dumps({k: v for k, v in result.items() if k not in ["source_hashes", "official_classification", "unknown_ethnicity_bounds", "overlapping_indicators"]}, indent=2, allow_nan=False))
