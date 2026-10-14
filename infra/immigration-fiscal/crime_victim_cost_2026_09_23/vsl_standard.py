"""One mortality valuation definition for crime, fear and pollution arms.

dot_uniform is DOT's 2024-dollar VSL. dot_life_years is an explicitly
age-dependent sensitivity, calibrated to that VSL at age 40 using the common
NVSS 2024 period life table (0% real discount; 3% is beside). Neither earnings
nor Miller's mortality QoL are added on top. Age 40 is a calibration assumption,
not a measured victim age or a DOT life-year recommendation.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REFERENCE_AGE = 40
STANDARDS = ("legacy", "dot_uniform", "dot_life_years")


def check_pins() -> None:
    for entry in json.loads((HERE / "inputs/pins.json").read_text())["files"]:
        path = ROOT / entry["path"]
        if not path.exists():
            raise ValueError(f"[BLOCKED] missing mortality source: {path}")
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != entry["sha256"]:
            raise ValueError(f"[BLOCKED] stale mortality source: {path}")


def verify_source(path: Path) -> None:
    records = json.loads((HERE / "inputs/pins.json").read_text())["files"]
    matches = [entry for entry in records if ROOT / entry["path"] == path]
    if len(matches) != 1 or not path.exists():
        raise ValueError(f"[BLOCKED] missing or unpinned mortality source: {path}")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != matches[0]["sha256"]:
        raise ValueError(f"[BLOCKED] stale mortality source: {path}")


def dot_vsl() -> float:
    path = HERE / "inputs/dot_vsl_table_web.txt"
    verify_source(path)
    text = path.read_text()
    rows = re.findall(r"^L\d+:\s*([0-9.]+)\s*\|\s*(2024)\s*$", text, re.MULTILINE)
    if len(rows) != 1:
        raise ValueError("[BLOCKED] DOT primary table lacks one unique 2024 row")
    return float(rows[0][0]) * 1e6


def life_table() -> pd.DataFrame:
    path = HERE / "inputs/lt2024_Table01.xlsx"
    verify_source(path)
    raw = pd.read_excel(path, header=None)
    rows = []
    for _, row in raw.iterrows():
        label = str(row[0]).strip().replace("–", "-").replace("—", "-")
        if label.startswith("100 and"):
            age = 100
        elif "-" in label and label[0].isdigit():
            age = int(label.split("-")[0])
        else:
            continue
        rows.append(dict(age=age, lx=float(row[2]), Lx=float(row[4])))
    result = pd.DataFrame(rows).sort_values("age").reset_index(drop=True)
    if result.age.tolist() != list(range(101)) or not np.isfinite(result.to_numpy()).all():
        raise ValueError("[BLOCKED] incomplete NVSS life table")
    if (result.lx <= 0).any() or (result.Lx < 0).any() or (result.lx.diff().dropna() > 0).any():
        raise ValueError("[BLOCKED] invalid NVSS survival/exposure")
    return result


def remaining_years(age: int, real_discount_rate: float = 0.0, table=None) -> float:
    if isinstance(age, bool) or int(age) != age or not 0 <= age <= 100:
        raise ValueError("[BLOCKED] life-year valuation requires an observed age in 0..100")
    if not np.isfinite(real_discount_rate) or real_discount_rate < 0:
        raise ValueError("[BLOCKED] invalid life-year discount rate")
    table = life_table() if table is None else table
    exposure = table.Lx.to_numpy()[age:] / table.lx.iloc[age]
    return float(exposure @ ((1 + real_discount_rate) ** -np.arange(len(exposure))))


def mortality_value(standard: str, *, remaining_years: float | None = None,
                    reference_years: float | None = None, legacy_value: float | None = None) -> float:
    if standard not in STANDARDS:
        raise ValueError(f"[BLOCKED] unknown vsl_standard {standard}")
    if standard == "legacy":
        if legacy_value is None or not np.isfinite(legacy_value) or legacy_value <= 0:
            raise ValueError("[BLOCKED] legacy valuation requires its explicit price")
        return float(legacy_value)
    if standard == "dot_uniform":
        return dot_vsl()
    if remaining_years is None or not np.isfinite(remaining_years) or remaining_years < 0:
        raise ValueError("[BLOCKED] life-year valuation requires remaining years; no age fallback")
    reference_years = reference_life_years() if reference_years is None else reference_years
    if not np.isfinite(reference_years) or reference_years <= 0:
        raise ValueError("[BLOCKED] invalid reference life-years")
    return dot_vsl() * remaining_years / reference_years


def reference_life_years(real_discount_rate: float = 0.0) -> float:
    return remaining_years(REFERENCE_AGE, real_discount_rate)


def settings() -> dict:
    table = life_table()
    return dict(setting="vsl_standard", values=list(STANDARDS), dot_vsl_2024usd=dot_vsl(),
                reference_age=REFERENCE_AGE, real_discount_rate=0.0,
                reference_remaining_years=remaining_years(REFERENCE_AGE, table=table),
                reference_remaining_years_r3=remaining_years(REFERENCE_AGE, 0.03, table),
                mortality_table="NVSS United States Life Tables 2024, Table 1, total population",
                assumptions="Age-40 calibration; common period mortality; 0% central, 3% beside; not DOT VSLY guidance",
                source="https://www.transportation.gov/office-policy/transportation-policy/revised-departmental-guidance-on-valuation-of-a-statistical-life-in-economic-analysis")


if __name__ == "__main__":
    check_pins()
    (HERE / "derived/vsl_standard.json").write_text(json.dumps(settings(), indent=2) + "\n")
