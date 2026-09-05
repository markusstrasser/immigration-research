#!/usr/bin/env python3
"""SIPP person-year payroll/allocated-benefit donors matched to ACS adults.

The ledger is employee-rate OASDI/HI on annual TPEARN minus allocated SNAP/TANF
and individual SSI. It is not net federal revenue: employer taxes, income taxes,
health spending, pensions and other public costs are absent; TANF/SSI amounts can
include state funding. 2024 SIPP measures calendar 2023.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from public_mvp_io import (
    PROTO, SIPP_BENEFIT_ALLOCATION, SIPP_NATIVITY_BASIS, SIPP_DICTIONARY_URL, SIPP_EDUCATION_TO_ACS,
    SIPP_GUIDE_URL, SIPP_REFERENCE_YEAR, SIPP_SCHEMA, SIPP_ZIP,
    income_band_annual, income_band_sql, iter_sipp_allocated_sample_units, sipp_eeduc_bucket, write_meta,
)

DONOR_OUT_FB = PROTO / "sipp_person_donor_cells_2024.csv"
DONOR_OUT_USB = PROTO / "sipp_person_donor_cells_usborn_2024.csv"
OASDI_CAP_2023 = 160_200.0
PAYROLL_SOURCE = "https://www.ssa.gov/policy/docs/statcomps/eedata_sc/2023/intro.html"


def employee_oasdi_hi_proxy(annual_earnings: float) -> float:
    """2023 employee base rates; cap OASDI per person, never Medicare HI.

    TPEARN includes net business income: wage rates are a proxy, not simulated
    liability. Self-employment rules, exempt jobs, Additional Medicare Tax and
    the employer share are excluded.
    """
    positive_earnings = max(0.0, annual_earnings)
    return 0.062 * min(positive_earnings, OASDI_CAP_2023) + 0.0145 * positive_earnings


def _acs_age_band(age: int | None) -> str | None:
    if age is None or not 25 <= age <= 64:
        return None
    lower = 25 + 10 * ((age - 25) // 10)
    return f"{lower}-{lower + 9}"


def build_all_donor_cells(
    *, schema_path: Path = SIPP_SCHEMA, zip_path: Path = SIPP_ZIP,
    output_dir: Path = PROTO,
) -> tuple[list[dict], list[dict]]:
    """Allocate once, then form individually weighted annual donor cells.

    SIPP Guide Table 7-1/section 7.3.4 specify December WPFINWGT for annual
    estimates. Age is December TAGE_EHC; EEDUC is December attainment. Sum
    observed monthly amounts within person before matching or capping. Do not
    multiply partial-year or volatile monthly earnings into invented annual pay.
    """
    cells: dict[tuple, dict] = {}
    scanned_rows = scanned_units = selected_people = 0
    all_benefits = {"snap": 0.0, "tanf": 0.0, "ssi": 0.0}
    adult_benefits = {"snap": 0.0, "tanf": 0.0, "ssi": 0.0}
    for sample in iter_sipp_allocated_sample_units(schema_path, zip_path):
        scanned_units += 1
        scanned_rows += len(sample)
        persons = defaultdict(list)
        for month in sample:
            persons[month.person_number].append(month)
            all_benefits["snap"] += month.allocated_snap
            all_benefits["tanf"] += month.allocated_tanf
            all_benefits["ssi"] += month.ssi
        for months in persons.values():
            december = next((month for month in months if month.month == 12), None)
            if december is None or not december.in_universe or december.weight <= 0:
                continue
            age_band = _acs_age_band(december.age)
            if age_band is None:
                continue
            if december.nativity not in (1, 2):
                raise ValueError(f"Invalid SIPP adult nativity: {december.nativity!r}")
            education = SIPP_EDUCATION_TO_ACS[sipp_eeduc_bucket(december.education_code)]
            income = sum(month.income for month in months)
            earnings = sum(month.earnings for month in months)
            snap = sum(month.allocated_snap for month in months)
            tanf = sum(month.allocated_tanf for month in months)
            ssi = sum(month.ssi for month in months)
            payroll = employee_oasdi_hi_proxy(earnings)
            key = (december.nativity, education, age_band, income_band_annual(income))
            cell = cells.setdefault(key, {
                "nativity_code": str(december.nativity), "education_bucket": education,
                "age_band": age_band, "income_band": key[-1],
                "person_weight_sum": 0.0, "person_year_count": 0, "person_month_count": 0,
                "sum_annual_tpearn": 0.0, "sum_annual_tptotinc": 0.0,
                "sum_annual_allocated_snap": 0.0, "sum_annual_allocated_tanf": 0.0,
                "sum_annual_tssi": 0.0, "sum_employee_oasdi_hi_proxy_annual": 0.0,
            })
            weight = december.weight
            cell["person_weight_sum"] += weight
            cell["person_year_count"] += 1
            cell["person_month_count"] += len(months)
            for field, amount in (
                ("sum_annual_tpearn", earnings), ("sum_annual_tptotinc", income),
                ("sum_annual_allocated_snap", snap), ("sum_annual_allocated_tanf", tanf),
                ("sum_annual_tssi", ssi), ("sum_employee_oasdi_hi_proxy_annual", payroll),
            ):
                cell[field] += weight * amount
            selected_people += 1
            for program, amount in (("snap", snap), ("tanf", tanf), ("ssi", ssi)):
                adult_benefits[program] += amount

    by_nativity = {"1": [], "2": []}
    for _, cell in sorted(cells.items()):
        weight = cell["person_weight_sum"]
        payroll = cell["sum_employee_oasdi_hi_proxy_annual"] / weight
        transfers = sum(cell[f"sum_annual_{field}"] for field in
                        ("allocated_snap", "allocated_tanf", "tssi")) / weight
        by_nativity[cell["nativity_code"]].append({
            **cell, "reference_year": SIPP_REFERENCE_YEAR,
            "mean_annual_person_tpearn": cell["sum_annual_tpearn"] / weight,
            "mean_annual_person_tptotinc": cell["sum_annual_tptotinc"] / weight,
            "mean_annual_allocated_snap": cell["sum_annual_allocated_snap"] / weight,
            "mean_annual_allocated_tanf": cell["sum_annual_allocated_tanf"] / weight,
            "mean_annual_person_tssi": cell["sum_annual_tssi"] / weight,
            "employee_oasdi_hi_proxy_annual": payroll,
            "allocated_snap_tanf_ssi_annual": transfers,
            "payroll_less_allocated_benefits_proxy_annual": payroll - transfers,
        })

    output_dir.mkdir(parents=True, exist_ok=True)
    for nativity, suffix in (("2", ""), ("1", "_usborn")):
        rows = by_nativity[nativity]
        if rows:
            with (output_dir / f"sipp_person_donor_cells{suffix}_2024.csv").open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
        write_meta(output_dir / f"sipp_person_donor_cells{suffix}_2024.meta.json", {
            "builder": "build_federal_microsim_sipp_2024.py", "reference_year": SIPP_REFERENCE_YEAR,
            "source_zip": str(zip_path), "source_schema": str(schema_path),
            "dictionary": SIPP_DICTIONARY_URL, "weights_source": SIPP_GUIDE_URL,
            "payroll_source": PAYROLL_SOURCE, "nativity_code": nativity,
            "nativity_basis": SIPP_NATIVITY_BASIS,
            "person_month_rows_scanned": scanned_rows, "sample_units_scanned": scanned_units,
            "selected_adults_both_nativities": selected_people, "donor_cells": len(rows),
            "person_years": sum(row["person_year_count"] for row in rows),
            "weight_basis": "December WPFINWGT once per person-year; ages 25-64 in December",
            "income_basis": "Sum of personal monthly TPTOTINC in 2023, including losses",
            "payroll_basis": "Per-person max(annual TPEARN,0): 6.2% up to $160200 plus uncapped 1.45%; then weighted mean",
            "benefit_allocation": SIPP_BENEFIT_ALLOCATION,
            "unweighted_source_benefits_all_people": all_benefits,
            "unweighted_source_benefits_selected_adults_both_nativities": adult_benefits,
            "unweighted_benefits_outside_adult_donor_universe": {
                program: all_benefits[program] - adult_benefits[program] for program in all_benefits
            },
            "limitations": [
                "Named payroll/benefit ledger only; not net federal or total fiscal impact.",
                "Net business income uses employee wage rates as a proxy, not liability.",
                "No employer share, Additional Medicare Tax, income tax, health or pension spending.",
                "TANF/SSI amounts do not isolate federal funding.",
                "ACS trailing-year and SIPP calendar-year income are distinct survey measures.",
                "Transport assumes comparability within nativity/education/age/personal-income cells.",
                "Native donors pool races; the NH-white target is a transported proxy.",
                "Point estimates only; no survey replicate-weight uncertainty is estimated.",
                "Income matching pools all personal income >=$75000 to avoid an unsupported fine cell; finer income heterogeneity remains unmodeled.",
            ],
        })
        print(f"Person donor cells (nativity {nativity}): {len(rows)}")
    return by_nativity["2"], by_nativity["1"]


def build_acs_recipient_cells(con, *, from_source_zip: bool = False) -> None:
    """Persist donor-independent ACS person-cell counts from acs_person_raw.

    Missing/invalid ACS education or income stays unmatched, never in the top
    bucket. Without raw ACS, recipient counts must be imported explicitly with
    provenance; there is no fallback to previously imputed fiscal values.
    """
    if from_source_zip:
        from acs_pums_io import person_csv_paths

        paths = person_csv_paths()
        if len(paths) != 2 or not all(any(part in Path(path).name for path in paths)
                                      for part in ("psam_pusa", "psam_pusb")):
            raise ValueError("National ACS recipients require both official pusa and pusb files")
        con.execute("CREATE OR REPLACE TEMP TABLE acs_person_raw AS SELECT "
                    "POBP, NATIVITY, HISP, RAC1P, SCHL, AGEP, PINCP, ADJINC, PWGTP "
                    "FROM read_csv(?, header=true, union_by_name=true, all_varchar=true)", [paths])
    # ACS 2023 PUMS User Guide: PINCP * ADJINC / 1e6 gives 2023 dollars.
    income_case = income_band_sql("TRY_CAST(p.PINCP AS DOUBLE) * TRY_CAST(p.ADJINC AS DOUBLE) / 1000000")
    cells = f"""
        SELECT COALESCE(d.origin_label, CAST(p.POBP AS VARCHAR)) AS origin_label,
          TRY_CAST(p.NATIVITY AS INTEGER) AS nativity,
          LPAD(CAST(p.HISP AS VARCHAR), 2, '0') = '01'
            AND TRY_CAST(p.RAC1P AS INTEGER) = 1 AS nh_white,
          CASE
            WHEN TRY_CAST(p.SCHL AS INTEGER) BETWEEN 1 AND 15 THEN '<HS'
            WHEN TRY_CAST(p.SCHL AS INTEGER) IN (16, 17) THEN 'HS / GED'
            WHEN TRY_CAST(p.SCHL AS INTEGER) IN (18, 19, 20) THEN 'some college / associate'
            WHEN TRY_CAST(p.SCHL AS INTEGER) BETWEEN 21 AND 24 THEN 'other'
          END AS education_bucket,
          CASE
            WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 25 AND 34 THEN '25-34'
            WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 35 AND 44 THEN '35-44'
            WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 45 AND 54 THEN '45-54'
            WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 55 AND 64 THEN '55-64'
          END AS age_band,
          {income_case} AS income_band,
          TRY_CAST(p.PWGTP AS DOUBLE) AS person_weight
        FROM acs_person_raw p
        LEFT JOIN pobp_dim d ON LPAD(CAST(p.POBP AS VARCHAR), 4, '0') = d.pobp
        WHERE TRY_CAST(p.AGEP AS INTEGER) BETWEEN 25 AND 64
          AND TRY_CAST(p.PWGTP AS DOUBLE) > 0
    """
    con.execute(f"""
        CREATE OR REPLACE TABLE acs_origin_person_recipient_cells_2023 AS
        WITH persons AS ({cells})
        SELECT origin_label, education_bucket, age_band, income_band,
               SUM(person_weight) AS weighted_adults
        FROM persons WHERE nativity = 2 GROUP BY 1, 2, 3, 4
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE acs_nh_white_person_recipient_cells_2023 AS
        WITH persons AS ({cells})
        SELECT 'nh_white_usborn' AS population_group, education_bucket, age_band,
               income_band, SUM(person_weight) AS weighted_adults
        FROM persons WHERE nativity = 1 AND nh_white GROUP BY 1, 2, 3, 4
    """)
    if from_source_zip:
        con.execute("DROP TABLE acs_person_raw")


def load_federal_microsim_into_duckdb(con, donor_rows: list[dict], ebornus: str = "2") -> None:
    """Join person donors to explicit donor-independent ACS recipient cells."""
    import pandas as pd

    if ebornus not in ("1", "2"):
        raise ValueError(f"Invalid donor nativity: {ebornus!r}")
    if not donor_rows:
        raise ValueError("Cannot load empty SIPP donor cells")
    keys = [(row["education_bucket"], row["age_band"], row["income_band"]) for row in donor_rows]
    if len(set(keys)) != len(keys) or any(row["nativity_code"] != ebornus for row in donor_rows):
        raise ValueError("Duplicate or wrong-nativity SIPP donor cells")
    if any(row["person_weight_sum"] <= 0 for row in donor_rows):
        raise ValueError("Nonpositive SIPP donor weight")
    donor_table = "sipp_person_donor_cells_2024" if ebornus == "2" else "sipp_person_donor_cells_usborn_2024"
    population = "origin" if ebornus == "2" else "nh_white"
    recipient_table = f"acs_{population}_person_recipient_cells_2023"
    output_table = f"acs_{population}_person_payroll_transfer_microsim_2023"
    population_column = "origin_label" if ebornus == "2" else "population_group"
    if not con.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = ?", [recipient_table]).fetchone()[0]:
        raise ValueError(f"Missing {recipient_table}; build or explicitly import ACS recipient counts first")
    con.register("_sipp_person_donors", pd.DataFrame(donor_rows))
    try:
        unmatched = con.execute(f"""
            SELECT COUNT(*), SUM(c.weighted_adults)
            FROM {recipient_table} c LEFT JOIN _sipp_person_donors s
              ON c.education_bucket = s.education_bucket
             AND c.age_band = s.age_band AND c.income_band = s.income_band
            WHERE s.person_weight_sum IS NULL
        """).fetchone()
        if unmatched[0]:
            raise ValueError(f"Unmatched ACS recipients: {unmatched[0]} cells, {unmatched[1]} adults; refusing a partial population estimate")
        con.execute(f"CREATE OR REPLACE TABLE {donor_table} AS SELECT * FROM _sipp_person_donors")
    finally:
        con.unregister("_sipp_person_donors")
    con.execute(f"""
        CREATE OR REPLACE TABLE {output_table} AS
        SELECT c.{population_column}, c.education_bucket, c.age_band, c.income_band,
               c.weighted_adults, s.mean_annual_person_tpearn,
               s.employee_oasdi_hi_proxy_annual, s.allocated_snap_tanf_ssi_annual,
               s.payroll_less_allocated_benefits_proxy_annual,
               s.person_weight_sum AS donor_person_weight,
               s.person_year_count AS donor_person_count
        FROM {recipient_table} c LEFT JOIN {donor_table} s
          ON c.education_bucket = s.education_bucket
         AND c.age_band = s.age_band AND c.income_band = s.income_band
    """)
    rows, matched = con.execute(f"SELECT COUNT(*), COUNT(donor_person_weight) FROM {output_table}").fetchone()
    # Retire invalid generated tables only after the replacement join succeeds.
    retired = (
        ("acs_origin_household_federal_microsim_2023", "sipp_household_donor_cells_2024")
        if ebornus == "2" else
        ("acs_nh_white_federal_microsim_2023", "sipp_household_donor_cells_usborn_2024")
    )
    for table in retired:
        con.execute(f"DROP TABLE IF EXISTS {table}")
    print(f"Person payroll/transfer microsim ({population}): {rows:,} cells, {matched:,} matched")


def build() -> Path:
    fb_rows, usb_rows = build_all_donor_cells()
    for path, rows in ((DONOR_OUT_FB, fb_rows), (DONOR_OUT_USB, usb_rows)):
        if not rows:
            raise ValueError(f"No donor cells for {path.name}")
        print(f"Wrote {path}")
    return DONOR_OUT_FB


if __name__ == "__main__":
    build()
