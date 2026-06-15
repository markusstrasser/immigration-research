"""Shared paths and helpers for public MVP module builders."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from paths import data_root, derived_root, duckdb_path

ROOT = data_root().parent  # immigration-fiscal data parent (legacy)
DATA = data_root()
DERIVED = derived_root()
PROTO = DERIVED / "stage3_proto"

SIPP_ZIP = DATA / "external" / "stage3" / "census" / "sipp" / "pu2024_csv.zip"
SIPP_SCHEMA = DATA / "external" / "stage3" / "census" / "sipp" / "pu2024_schema.json"
MEPS_DAT_ZIP = DATA / "external" / "stage3" / "ahrq" / "meps" / "h251dat.zip"
MEPS_SU = DATA / "external" / "stage3" / "ahrq" / "meps" / "h251su.txt"
DUCKDB_PATH = duckdb_path()


def write_meta(path: Path, payload: dict) -> None:
    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    path.write_text(json.dumps(meta, indent=2) + "\n")


def sipp_working_age_band(age: int) -> str | None:
    if 25 <= age <= 29:
        return "25-29"
    if 30 <= age <= 34:
        return "30-34"
    if 35 <= age <= 39:
        return "35-39"
    if 40 <= age <= 44:
        return "40-44"
    if 45 <= age <= 49:
        return "45-49"
    if 50 <= age <= 54:
        return "50-54"
    if 55 <= age <= 64:
        return "55-64"
    return None


def meps_age_band(age: int) -> str:
    if age < 18:
        return "0-17"
    if age < 25:
        return "18-24"
    if age < 35:
        return "25-34"
    if age < 45:
        return "35-44"
    if age < 55:
        return "45-54"
    if age < 65:
        return "55-64"
    if age < 75:
        return "65-74"
    if age < 85:
        return "75-84"
    return "85+"


def sipp_eeduc_bucket(code: int) -> str:
    if code <= 33:
        return "1_lt_hs"
    if code <= 35:
        return "2_hs_ged"
    if code <= 37:
        return "3_some_college"
    if code <= 39:
        return "4_associate"
    if code <= 41:
        return "5_bachelors"
    if code <= 43:
        return "6_masters"
    return "7_professional_plus"


def acs_education_bucket(schl: int) -> str:
    if schl < 16:
        return "<HS"
    if schl in (16, 17):
        return "HS / GED"
    if schl in (18, 19, 20):
        return "some college / associate"
    return "other"


def earnings_band_annual(annual: float) -> str:
    if annual < 20_000:
        return "lt20k"
    if annual < 40_000:
        return "20-40k"
    if annual < 75_000:
        return "40-75k"
    if annual < 150_000:
        return "75-150k"
    return "150k+"


def meps_insurance_group(code: int, age: int) -> str:
    if age < 65:
        return {1: "any private", 2: "public only", 3: "uninsured"}.get(code, "other_u65")
    if code == 4:
        return "65+ medicare only"
    if code == 5:
        return "65+ medicare and private"
    if code in (6, 8):
        return "65+ medicare and public"
    if code == 7:
        return "65+ uninsured"
    return "65+ other"


def nativity_group(code: str) -> str:
    return "us_born" if str(code).strip() in ("1", "1.0") else "foreign_born"


def parse_meps_sas_fields(su_path: Path) -> dict[str, tuple[int, int]]:
    import re

    fields: dict[str, tuple[int, int]] = {}
    for line in su_path.read_text(encoding="latin-1", errors="replace").splitlines():
        m = re.match(r"\s*@(\d+)\s+(\w+)\s+([\d.]+)", line)
        if not m:
            continue
        start = int(m.group(1)) - 1
        name = m.group(2)
        width = int(float(m.group(3)))
        fields[name] = (start, width)
    return fields


def weighted_mean(sum_wx: float, w: float) -> float | None:
    return sum_wx / w if w > 0 else None
