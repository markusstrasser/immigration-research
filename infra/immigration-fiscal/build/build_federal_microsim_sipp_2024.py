#!/usr/bin/env python3
"""SIPP 2024 federal donor cells + ACS origin-household microsim join.

Replaces broken CPS HHINC donor (research/immigration-verified-findings-report-2026-04-10.md).
Uses monthly TPEARN / TPTOTINC and transfer amounts — not income recodes as dollars.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from pathlib import Path

from public_mvp_io import (
    PROTO,
    SIPP_SCHEMA,
    SIPP_ZIP,
    earnings_band_annual,
    sipp_eeduc_bucket,
    weighted_mean,
    write_meta,
)

DONOR_OUT = PROTO / "sipp_household_donor_cells_2024.csv"
DONOR_META = PROTO / "sipp_household_donor_cells_2024.meta.json"

COLS = (
    "SSUID",
    "ERESIDENCEID",
    "MONTHCODE",
    "WPFINWGT",
    "TAGE",
    "EBORNUS",
    "EEDUC",
    "TPEARN",
    "TPTOTINC",
    "TSNAP_AMT",
    "TTANF_AMT",
    "TSSI_AMT",
)


def _load_indices() -> dict[str, int]:
    schema = json.loads(SIPP_SCHEMA.read_text())
    names = [r["name"] for r in schema]
    return {c: names.index(c) for c in COLS}


def _num(raw: str) -> float | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        v = float(raw)
    except ValueError:
        return None
    return v if v >= 0 else None


def _acs_age_band(age: int) -> str | None:
    if 25 <= age <= 34:
        return "25-34"
    if 35 <= age <= 44:
        return "35-44"
    if 45 <= age <= 54:
        return "45-54"
    if 55 <= age <= 64:
        return "55-64"
    return None


def _sipp_to_acs_education(code: int) -> str:
    bucket = sipp_eeduc_bucket(code)
    if bucket == "1_lt_hs":
        return "<HS"
    if bucket == "2_hs_ged":
        return "HS / GED"
    if bucket in ("3_some_college", "4_associate"):
        return "some college / associate"
    return "other"


def build_donor_cells() -> list[dict]:
    idx = _load_indices()
    # household-month -> aggregated metrics
    hh: dict[tuple, dict] = {}
    n_rows = 0

    with zipfile.ZipFile(SIPP_ZIP) as zf:
        with zf.open("pu2024.csv") as fh:
            rdr = csv.reader(io.TextIOWrapper(fh, encoding="latin-1", newline=""), delimiter="|")
            for row in rdr:
                n_rows += 1
                if len(row) < max(idx.values()) + 1:
                    continue
                if row[idx["EBORNUS"]].strip() != "2":
                    continue
                age = _num(row[idx["TAGE"]])
                wt = _num(row[idx["WPFINWGT"]])
                if age is None or wt is None or wt <= 0:
                    continue
                age_i = int(age)
                ab = _acs_age_band(age_i)
                if ab is None:
                    continue
                ed = row[idx["EEDUC"]].strip()
                try:
                    edu = _sipp_to_acs_education(int(float(ed)))
                except ValueError:
                    continue
                ssuid = row[idx["SSUID"]].strip()
                eres = row[idx["ERESIDENCEID"]].strip()
                month = row[idx["MONTHCODE"]].strip()
                key = (ssuid, eres, month)
                h = hh.setdefault(
                    key,
                    {
                        "household_weight": 0.0,
                        "education_bucket": edu,
                        "age_band": ab,
                        "sum_tpearn": 0.0,
                        "sum_tptotinc": 0.0,
                        "sum_tsnap": 0.0,
                        "sum_ttanf": 0.0,
                        "sum_tssi": 0.0,
                        "members": 0,
                    },
                )
                h["household_weight"] = max(h["household_weight"], wt)
                h["members"] += 1
                for field, slot in (
                    ("TPEARN", "sum_tpearn"),
                    ("TPTOTINC", "sum_tptotinc"),
                    ("TSNAP_AMT", "sum_tsnap"),
                    ("TTANF_AMT", "sum_ttanf"),
                    ("TSSI_AMT", "sum_tssi"),
                ):
                    v = _num(row[idx[field]])
                    if v is not None:
                        h[slot] += v

    cells: dict[tuple, dict] = {}
    for h in hh.values():
        annual_inc = h["sum_tptotinc"] * 12
        eb = earnings_band_annual(annual_inc)
        key = (h["education_bucket"], h["age_band"], eb)
        c = cells.setdefault(
            key,
            {
                "education_bucket": h["education_bucket"],
                "age_band": h["age_band"],
                "earnings_band": eb,
                "household_weight_sum": 0.0,
                "household_month_count": 0,
                "sum_monthly_tpearn": 0.0,
                "sum_monthly_tptotinc": 0.0,
                "sum_monthly_tsnap": 0.0,
                "sum_monthly_ttanf": 0.0,
                "sum_monthly_tssi": 0.0,
            },
        )
        w = h["household_weight"]
        c["household_weight_sum"] += w
        c["household_month_count"] += 1
        c["sum_monthly_tpearn"] += h["sum_tpearn"] * w
        c["sum_monthly_tptotinc"] += h["sum_tptotinc"] * w
        c["sum_monthly_tsnap"] += h["sum_tsnap"] * w
        c["sum_monthly_ttanf"] += h["sum_ttanf"] * w
        c["sum_monthly_tssi"] += h["sum_tssi"] * w

    rows = []
    for _, c in sorted(cells.items()):
        w = c["household_weight_sum"]
        mean_earn = weighted_mean(c["sum_monthly_tpearn"], w) or 0.0
        annual_earn = mean_earn * 12
        payroll = min(annual_earn, 168_600) * 0.0765
        transfers = (
            (weighted_mean(c["sum_monthly_tsnap"], w) or 0)
            + (weighted_mean(c["sum_monthly_ttanf"], w) or 0)
            + (weighted_mean(c["sum_monthly_tssi"], w) or 0)
        ) * 12
        rows.append(
            {
                **c,
                "mean_monthly_hh_tpearn": mean_earn,
                "mean_monthly_hh_tptotinc": weighted_mean(c["sum_monthly_tptotinc"], w),
                "mean_monthly_hh_tsnap": weighted_mean(c["sum_monthly_tsnap"], w),
                "mean_monthly_hh_ttanf": weighted_mean(c["sum_monthly_ttanf"], w),
                "mean_monthly_hh_tssi": weighted_mean(c["sum_monthly_tssi"], w),
                "payroll_tax_proxy_annual": payroll,
                "transfer_outflow_proxy_annual": transfers,
                "federal_net_proxy_annual": payroll - transfers,
            }
        )

    write_meta(
        DONOR_META,
        {
            "builder": "build_federal_microsim_sipp_2024.py",
            "person_month_rows_scanned": n_rows,
            "household_months": len(hh),
            "donor_cells": len(rows),
            "income_basis": "monthly TPTOTINC summed within household-month, annualized ×12 for bands",
            "notes": "Proxy only — SIPP lacks verified federal tax liability fields in this build.",
        },
    )
    print(f"Donor cells: {len(rows)} from {len(hh):,} foreign-born household-months")
    return rows


def load_federal_microsim_into_duckdb(con, donor_rows: list[dict]) -> None:
    """Requires acs_person_raw in an open warehouse build connection."""
    import pandas as pd

    con.register("_donor_rows", pd.DataFrame(donor_rows))
    con.execute(
        "CREATE OR REPLACE TABLE sipp_household_donor_cells_2024 AS SELECT * FROM _donor_rows"
    )

    con.execute("""
        CREATE OR REPLACE TABLE acs_origin_household_federal_microsim_2023 AS
        WITH person_cells AS (
          SELECT
            COALESCE(d.origin_label, CAST(p.POBP AS VARCHAR)) AS origin_label,
            CASE
              WHEN TRY_CAST(p.SCHL AS INTEGER) < 16 THEN '<HS'
              WHEN TRY_CAST(p.SCHL AS INTEGER) IN (16, 17) THEN 'HS / GED'
              WHEN TRY_CAST(p.SCHL AS INTEGER) IN (18, 19, 20) THEN 'some college / associate'
              ELSE 'other'
            END AS education_bucket,
            CASE
              WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 25 AND 34 THEN '25-34'
              WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 35 AND 44 THEN '35-44'
              WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 45 AND 54 THEN '45-54'
              WHEN TRY_CAST(p.AGEP AS INTEGER) BETWEEN 55 AND 64 THEN '55-64'
            END AS age_band,
            CASE
              WHEN TRY_CAST(p.PINCP AS DOUBLE) < 20000 THEN 'lt20k'
              WHEN TRY_CAST(p.PINCP AS DOUBLE) < 40000 THEN '20-40k'
              WHEN TRY_CAST(p.PINCP AS DOUBLE) < 75000 THEN '40-75k'
              WHEN TRY_CAST(p.PINCP AS DOUBLE) < 150000 THEN '75-150k'
              ELSE '150k+'
            END AS earnings_band,
            SUM(TRY_CAST(p.PWGTP AS DOUBLE)) AS weighted_adults
          FROM acs_person_raw p
          LEFT JOIN pobp_dim d
            ON LPAD(CAST(p.POBP AS VARCHAR), 4, '0') = d.pobp
            OR CAST(p.POBP AS VARCHAR) = TRIM(LEADING '0' FROM d.pobp)
          WHERE TRY_CAST(p.AGEP AS INTEGER) BETWEEN 25 AND 64
            AND CAST(p.NATIVITY AS VARCHAR) = '2'
          GROUP BY 1, 2, 3, 4
        )
        SELECT
          c.origin_label,
          c.education_bucket,
          c.age_band,
          c.earnings_band,
          c.weighted_adults,
          s.mean_monthly_hh_tpearn,
          s.payroll_tax_proxy_annual,
          s.transfer_outflow_proxy_annual,
          s.federal_net_proxy_annual,
          s.household_weight_sum AS donor_household_weight
        FROM person_cells c
        LEFT JOIN sipp_household_donor_cells_2024 s
          ON c.education_bucket = s.education_bucket
         AND c.age_band = s.age_band
         AND c.earnings_band = s.earnings_band
    """)
    n = con.execute("SELECT COUNT(*) FROM acs_origin_household_federal_microsim_2023").fetchone()[0]
    matched = con.execute(
        "SELECT COUNT(*) FROM acs_origin_household_federal_microsim_2023 WHERE donor_household_weight IS NOT NULL"
    ).fetchone()[0]
    print(f"federal microsim: {n:,} origin cells, {matched:,} with SIPP donor match")


def build() -> Path:
    PROTO.mkdir(parents=True, exist_ok=True)
    rows = build_donor_cells()
    with DONOR_OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {DONOR_OUT}")
    return DONOR_OUT


if __name__ == "__main__":
    build()
