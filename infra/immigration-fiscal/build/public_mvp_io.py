"""Shared paths and helpers for public MVP module builders."""
from __future__ import annotations

import csv
import io
import json
import math
import re
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

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

SIPP_REFERENCE_YEAR = 2023
SIPP_DICTIONARY_URL = "https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2024/2024_SIPP_Data_Dictionary.pdf"
SIPP_GUIDE_URL = "https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf"
SIPP_EDUCATION_TO_ACS = {
    "1_lt_hs": "<HS",
    "2_hs_ged": "HS / GED",
    "3_some_college": "some college / associate",
    "4_associate": "some college / associate",
    "5_bachelors": "other",
    "6_masters": "other",
    "7_professional_plus": "other",
}
ANNUAL_INCOME_BANDS = (
    (20_000, "lt20k"), (40_000, "20-40k"),
    (75_000, "40-75k"),
)
# Native-definition harmonization exposed an empty fine high-income FB cell.
# Pool both upper bands globally, before outcome comparison, to retain support.
ANNUAL_INCOME_TOP_BAND = "75k+"
SIPP_PERSON_MONTH_COLS = (
    "SSUID", "PNUM", "MONTHCODE", "RIN_UNIV", "WPFINWGT", "TAGE_EHC",
    "EBORNUS", "ENATCIT", "EEDUC", "TYRENTRY", "TPEARN", "TPTOTINC",
    "RSNAP_MNYN", "ESNAP_OWN", "ESNAP_CNT", "TSNAP_AMT",
    "RTANF_MNYN", "ETANF_OWN", "TTANF_AMT", "RSSI_MNYN", "TSSI_AMT",
)
SIPP_BENEFIT_ALLOCATION = (
    "SNAP/TANF owner amounts are divided equally among people covered by the "
    "same program/SSUID/owner-PNUM/month, before age, nativity, or weight filters. "
    "An owner need not be covered. SSI stays with its individual recipient. "
    "Survey estimates use each beneficiary's own person weight. "
    "Allocation is an accounting assumption, not an estimate of within-family "
    "incidence. Child and other excluded-person shares are not assigned to adults. "
    "SNAP/TANF/SSI amounts do not isolate federal from state funding."
)
SIPP_NATIVITY_BASIS = (
    "ACS-compatible nativity: native if EBORNUS=1 or ENATCIT in (4,5); "
    "otherwise foreign born when EBORNUS=2. Includes citizens born in US "
    "island areas or abroad to US-citizen parents in the native group. "
    "Legacy _usborn table/population keys denote this native group."
)


def sipp_acs_nativity(born_in_us: int | None, citizenship_origin: int | None) -> int | None:
    """Dictionary pp.915–917: birthplace alone differs from ACS nativity."""
    if born_in_us not in (None, 1, 2) or citizenship_origin not in (None, 1, 2, 3, 4, 5):
        raise ValueError("Invalid SIPP birth/citizenship-origin code")
    if born_in_us == 1 or citizenship_origin in (4, 5):
        return 1
    return 2 if born_in_us == 2 else None


@dataclass(slots=True)
class SippPersonMonth:
    sample_id: str
    person_number: int
    month: int
    in_universe: bool
    weight: float
    age: int | None
    nativity: int | None
    education_code: int | None
    entry_year: int | None
    earnings: float
    income: float
    snap_owner: int | None
    snap_covered: bool
    snap_unit_size: int | None
    snap_owner_amount: float
    tanf_owner: int | None
    tanf_covered: bool
    tanf_owner_amount: float
    ssi: float
    allocated_snap: float = 0.0
    allocated_tanf: float = 0.0


def _sipp_number(raw: str, field: str) -> float | None:
    """Blank means out of universe; negative dollar values can be real losses."""
    if not raw.strip():
        return None
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"Invalid SIPP {field}: {raw!r}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Non-finite SIPP {field}: {raw!r}")
    return value


def _sipp_integer(raw: str, field: str) -> int | None:
    value = _sipp_number(raw, field)
    if value is None:
        return None
    if value != int(value):
        raise ValueError(f"Non-integer SIPP {field}: {raw!r}")
    return int(value)


def allocate_sipp_benefits(rows: list[SippPersonMonth]) -> None:
    """Conserve each benefit-unit amount across covered members, including children.

    SIPP 2024 dictionary: ESNAP_OWN p.2936, RSNAP_MNYN p.3011,
    TSNAP_AMT p.3015; ETANF_OWN p.3165, TTANF_AMT p.3167;
    TSSI_AMT p.3014. SSI's amount is on the recipient, including a child.
    """
    by_person_month = {}
    for row in rows:
        key = (row.sample_id, row.person_number, row.month)
        if key in by_person_month:
            raise ValueError(f"Duplicate SIPP person-month: {key}")
        by_person_month[key] = row
    for program in ("snap", "tanf"):
        beneficiaries: dict[tuple, list[SippPersonMonth]] = defaultdict(list)
        owners: dict[tuple, SippPersonMonth] = {}
        for row in rows:
            owner = getattr(row, f"{program}_owner")
            amount = getattr(row, f"{program}_owner_amount")
            if amount < 0:
                raise ValueError(f"Negative SIPP {program} benefit: {amount}")
            if owner is not None and owner == row.person_number:
                owners[(row.sample_id, owner, row.month)] = row
            elif amount != 0:
                raise ValueError(f"SIPP {program} amount on a non-owner record")
            if getattr(row, f"{program}_covered"):
                if owner is None:
                    raise ValueError(f"Covered SIPP {program} recipient has no owner link")
                beneficiaries[(row.sample_id, owner, row.month)].append(row)
        for key in owners.keys() | beneficiaries.keys():
            owner = owners.get(key)
            if owner is None:
                raise ValueError(f"Unresolved SIPP {program} benefit owner: {key}")
            members = beneficiaries.get(key, [])
            amount = getattr(owner, f"{program}_owner_amount")
            if not members:
                if amount != 0:
                    raise ValueError(f"SIPP {program} amount has no covered recipients: {key}")
                continue
            if program == "snap" and owner.snap_unit_size != len(members):
                raise ValueError(
                    f"SIPP SNAP unit size differs from linked recipients at {key}: "
                    f"reported {owner.snap_unit_size}, linked {len(members)}"
                )
            share = amount / len(members)
            for member in members:
                setattr(member, f"allocated_{program}", share)
            allocated = sum(getattr(member, f"allocated_{program}") for member in members)
            if not math.isclose(allocated, amount, rel_tol=1e-12, abs_tol=1e-9):
                raise ValueError(f"SIPP {program} allocation does not conserve amount: {key}")


def _sipp_person_csv_member(archive: zipfile.ZipFile) -> str:
    members = [name for name in archive.namelist() if re.fullmatch(r"pu[0-9]{4}\.csv", name)]
    if len(members) != 1:
        raise ValueError(f"Expected one puYYYY.csv SIPP member, found {members}")
    return members[0]


def iter_sipp_allocated_sample_units(
    schema_path: Path, zip_path: Path,
) -> Iterator[list[SippPersonMonth]]:
    """Stream complete SSUID units and allocate benefits before sample selection.

    The official file is ordered by SSUID. An out-of-order repeated SSUID fails
    loudly instead of silently splitting a benefit unit. No household weight or
    first-member demographic is substituted for an individual's own record.
    """
    names = [entry["name"] for entry in json.loads(schema_path.read_text())]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate field in SIPP schema")
    idx = {field: names.index(field) for field in SIPP_PERSON_MONTH_COLS}
    current_id = None
    closed_ids: set[str] = set()
    sample_rows: list[SippPersonMonth] = []
    with zipfile.ZipFile(zip_path) as archive, archive.open(_sipp_person_csv_member(archive)) as stream:
        reader = csv.reader(io.TextIOWrapper(stream, encoding="latin-1", newline=""), delimiter="|")
        for line, values in enumerate(reader, 1):
            if line == 1 and values == names:
                continue
            if len(values) != len(names):
                raise ValueError(f"SIPP row {line}: expected {len(names)} fields, got {len(values)}")
            row = {field: values[index].strip() for field, index in idx.items()}
            sample_id = row["SSUID"]
            if not sample_id:
                raise ValueError(f"SIPP row {line} has no SSUID")
            if sample_id != current_id:
                if current_id is not None:
                    allocate_sipp_benefits(sample_rows)
                    yield sample_rows
                    closed_ids.add(current_id)
                if sample_id in closed_ids:
                    raise ValueError(f"SIPP SSUID is not contiguous: {sample_id}")
                current_id, sample_rows = sample_id, []
            integer = lambda name: _sipp_integer(row[name], name)
            number = lambda name: _sipp_number(row[name], name)
            person_number, month = integer("PNUM"), integer("MONTHCODE")
            if person_number is None or month not in range(1, 13):
                raise ValueError(f"Invalid SIPP person/month at row {line}")
            in_universe = integer("RIN_UNIV") == 1
            age = integer("TAGE_EHC")
            weight = number("WPFINWGT") or 0.0
            if weight < 0:
                raise ValueError(f"Negative SIPP person weight at row {line}")
            income = number("TPTOTINC")
            if in_universe and age is not None and age >= 15 and income is None:
                raise ValueError(f"Missing in-universe SIPP adult income at row {line}")
            snap_amount = number("TSNAP_AMT")
            tanf_amount = number("TTANF_AMT")
            ssi_amount = number("TSSI_AMT")
            snap_owner, tanf_owner = integer("ESNAP_OWN"), integer("ETANF_OWN")
            for program, owner, amount in (
                ("SNAP", snap_owner, snap_amount), ("TANF", tanf_owner, tanf_amount),
            ):
                if owner == person_number and amount is None:
                    raise ValueError(f"SIPP {program} owner missing amount at row {line}")
            if integer("RSSI_MNYN") == 1 and ssi_amount is None:
                raise ValueError(f"SIPP SSI recipient missing amount at row {line}")
            if ssi_amount is not None and (ssi_amount < 0 or (ssi_amount > 0 and integer("RSSI_MNYN") != 1)):
                raise ValueError(f"Inconsistent SIPP SSI amount/receipt at row {line}")
            sample_rows.append(SippPersonMonth(
                sample_id=sample_id, person_number=person_number, month=month,
                in_universe=in_universe, weight=weight, age=age,
                nativity=sipp_acs_nativity(integer("EBORNUS"), integer("ENATCIT")),
                education_code=integer("EEDUC"),
                entry_year=integer("TYRENTRY"), earnings=number("TPEARN") or 0.0,
                income=income or 0.0, snap_owner=snap_owner,
                snap_covered=integer("RSNAP_MNYN") == 1,
                snap_unit_size=integer("ESNAP_CNT"), snap_owner_amount=snap_amount or 0.0,
                tanf_owner=tanf_owner, tanf_covered=integer("RTANF_MNYN") == 1,
                tanf_owner_amount=tanf_amount or 0.0, ssi=ssi_amount or 0.0,
            ))
    if sample_rows:
        allocate_sipp_benefits(sample_rows)
        yield sample_rows


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
    """2024 SIPP EEDUC, dictionary p. 889; invalid codes are not education.

    Unlike ACS SCHL, SIPP begins at 31. Codes 40 and 41 both mean some
    college without a degree; 42 is associate, 43 BA, 44 MA, and 45/46
    professional/doctoral. Never let an out-of-universe sentinel enter a cell.
    """
    if code not in range(31, 47):
        raise ValueError(f"Invalid 2024 SIPP EEDUC code: {code!r}")
    if code <= 38:
        return "1_lt_hs"
    if code == 39:
        return "2_hs_ged"
    if code in (40, 41):
        return "3_some_college"
    if code == 42:
        return "4_associate"
    if code == 43:
        return "5_bachelors"
    if code == 44:
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


def income_band_annual(annual: float) -> str:
    if not math.isfinite(annual):
        raise ValueError(f"Invalid annual income: {annual!r}")
    for upper, label in ANNUAL_INCOME_BANDS:
        if annual < upper:
            return label
    return ANNUAL_INCOME_TOP_BAND


def income_band_sql(expression: str) -> str:
    """Native SQL from the same cutoffs used by SIPP's person-year classifier."""
    cases = " ".join(f"WHEN {expression} < {upper} THEN '{label}'"
                     for upper, label in ANNUAL_INCOME_BANDS)
    return (f"CASE WHEN {expression} IS NULL OR NOT isfinite({expression}) THEN NULL "
            f"{cases} ELSE '{ANNUAL_INCOME_TOP_BAND}' END")


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
    code = str(code).strip()
    if code in ("1", "1.0"):
        return "us_born"
    if code in ("2", "2.0"):
        return "foreign_born"
    return "unknown"


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
