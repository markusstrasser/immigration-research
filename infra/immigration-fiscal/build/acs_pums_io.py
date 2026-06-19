"""Shared ACS 2023 PUMS person CSV paths (reuse warehouse extracts)."""
from __future__ import annotations

import zipfile
from pathlib import Path

from paths import data_root, derived_root

PERSON_ZIP = data_root() / "census" / "acs_pums_2023_person.zip"


def person_csv_paths() -> list[str]:
    tmp = derived_root() / "_tmp"
    for pattern in ("person_psam_pus*.csv", "health_person/psam_pus*.csv", "school_age_person/psam_pus*.csv"):
        found = sorted(tmp.glob(pattern))
        if found:
            return [str(p) for p in found]
    if not PERSON_ZIP.exists():
        return []
    out_dir = tmp / "acs_person"
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    with zipfile.ZipFile(PERSON_ZIP) as zf:
        for name in sorted(n for n in zf.namelist() if n.lower().endswith(".csv")):
            out = out_dir / name.split("/")[-1]
            if not out.exists() or out.stat().st_size == 0:
                out.write_bytes(zf.read(name))
            paths.append(str(out))
    return paths


def person_csv_sql_glob() -> str:
    paths = person_csv_paths()
    if not paths:
        raise FileNotFoundError(f"missing ACS person CSVs — run setup.sh ({PERSON_ZIP})")
    return ",".join(f"'{p}'" for p in paths)
