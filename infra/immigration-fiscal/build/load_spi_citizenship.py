#!/usr/bin/env python3
"""Build 2016 SPI citizenship aggregates using the official RV0004 analysis recode.

Rates require an explicitly matched 2016 national adult denominator. Set
SPI_DENOMINATOR_CSV or stage external/crime_frontier/spi/acs2016_adult_citizenship.csv.
Use --counts-only to build weighted prison counts while explicitly withdrawing rates.
No latest-year ACS fallback or citizenship-to-birthplace inference is permitted.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd

from paths import data_root, derived_root, duckdb_path
from build_status_crosswalk import status_class_for

PRISON_YEAR = 2016
DENOM_UNIVERSE = "US residents age 18+ including institutional group quarters"


def summarize_spi(df: pd.DataFrame) -> pd.DataFrame:
    required = {"RV0001", "RV0004", "V1585"}
    if not required.issubset(df.columns):
        raise ValueError(f"SPI lacks required official fields: {required - set(df.columns)}")
    if not np.isfinite(df["RV0001"]).all() or (df["RV0001"] < 18).any():
        raise ValueError("SPI adult universe requires observed RV0001 ages of at least 18")
    if not np.isfinite(df["V1585"]).all() or (df["V1585"] < 0).any():
        raise ValueError("SPI weights must be finite and nonnegative")
    codes = set(df["RV0004"].dropna().unique())
    if not codes.issubset({1, 2, 8, -9}):
        raise ValueError(f"Unexpected RV0004 codes: {codes}")
    total = float(df["V1585"].sum())
    if total <= 0:
        raise ValueError("SPI weighted population is not positive")
    groups = [
        ("us_citizen", df["RV0004"].eq(1), status_class_for("BJS_SPI", "RV0004_1")),
        ("noncitizen", df["RV0004"].eq(2), status_class_for("BJS_SPI", "RV0004_2")),
        ("ambiguous", ~df["RV0004"].isin([1, 2]), None),
    ]
    return pd.DataFrame([
        {"survey_year": PRISON_YEAR, "prison_population_total": total,
         "citizenship_status": name, "status_class": status,
         "weighted_inmates": float(df.loc[mask, "V1585"].sum()),
         "sample_n": int(mask.sum()),
         "share_of_prison_pop": float(df.loc[mask, "V1585"].sum() / total),
         "note": "Official RV0004 citizenship recode; citizenship alone does not determine birthplace"}
        for name, mask, status in groups
    ])


def matched_rates(summary: pd.DataFrame, denominator: pd.DataFrame) -> pd.DataFrame:
    required = {"year", "geography", "universe", "citizenship_status", "population", "source"}
    if not required.issubset(denominator.columns):
        raise ValueError(f"Denominator lacks metadata: {required - set(denominator.columns)}")
    if not denominator["year"].eq(PRISON_YEAR).all():
        raise ValueError("SPI 2016 requires a 2016 denominator; latest ACS is not a fallback")
    if not denominator["geography"].eq("US").all() or not denominator["universe"].eq(DENOM_UNIVERSE).all():
        raise ValueError("Denominator must cover national residents age 18+, including institutional group quarters")
    if len(denominator) != 2 or set(denominator["citizenship_status"]) != {"us_citizen", "noncitizen"}:
        raise ValueError("Require exactly one citizen and one noncitizen denominator")
    if not np.isfinite(denominator["population"]).all() or (denominator["population"] <= 0).any():
        raise ValueError("Denominator populations must be finite and positive")
    if denominator["source"].isna().any() or denominator["source"].str.strip().eq("").any():
        raise ValueError("Each denominator needs a source")
    numerator = summary.loc[summary["citizenship_status"].isin(["us_citizen", "noncitizen"])]
    result = numerator.merge(denominator, on="citizenship_status", validate="one_to_one")
    result["prison_year"] = PRISON_YEAR
    result["acs_adult_year"] = result["year"]
    result["prisoners"] = result["weighted_inmates"]
    result["adults_18plus"] = result["population"]
    result["per_100k_adults"] = result["prisoners"] / result["adults_18plus"] * 1e5
    result["measure"] = "2016 state/federal prison prevalence, not all custody or offending"
    return result


def build(*, counts_only: bool = False) -> None:
    import duckdb
    import pyreadstat

    base = data_root() / "external" / "crime_frontier" / "spi"
    dta = base / "ICPSR_37692" / "DS0001" / "37692-0001-Data.dta"
    if not dta.exists():
        raise SystemExit(f"SPI data absent: {dta}")
    denominator = None
    if not counts_only:
        denom_path = Path(os.environ.get("SPI_DENOMINATOR_CSV", str(base / "acs2016_adult_citizenship.csv")))
        if not denom_path.is_file():
            raise SystemExit(f"Matched 2016 SPI denominator absent: {denom_path}. Supply it or explicitly use --counts-only.")
        denominator = pd.read_csv(denom_path)
    df, _ = pyreadstat.read_dta(str(dta), usecols=["RV0001", "RV0004", "V1585"])
    summary = summarize_spi(df)
    rates = matched_rates(summary, denominator) if denominator is not None else None
    db = duckdb_path()
    if not db.exists():
        raise SystemExit(f"Missing {db}; initialize the intended context database first")
    out = derived_root() / "crime"
    out.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db)) as con:
        con.register("_spi", summary)
        con.execute("CREATE OR REPLACE TABLE crime_spi_inmates_by_citizenship AS SELECT * FROM _spi")
        summary.to_csv(out / "spi_inmates_by_citizenship_2016.csv", index=False)
        if rates is not None:
            con.register("_rates", rates)
            con.execute("CREATE OR REPLACE TABLE crime_spi_incarceration_rate AS SELECT * FROM _rates")
            rates.to_csv(out / "spi_incarceration_rate.csv", index=False)
        else:
            con.execute("DROP TABLE IF EXISTS crime_spi_incarceration_rate")
            (out / "spi_incarceration_rate.csv").unlink(missing_ok=True)
            print("[COUNTS ONLY] No incarceration rate: matched denominator not requested; stale rate output withdrawn.")
    print(summary[["citizenship_status", "sample_n", "weighted_inmates"]].to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--counts-only", action="store_true")
    build(counts_only=parser.parse_args().counts_only)
