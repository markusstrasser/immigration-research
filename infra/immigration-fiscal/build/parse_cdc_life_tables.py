#!/usr/bin/env python3
"""Parse CDC NVSR 72-12 period life tables (xlsx) into a unified mortality panel."""
from __future__ import annotations

import re
import zipfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from paths import data_root, derived_root

CDC_DIR = data_root() / "external" / "lifetime" / "cdc" / "nvsr72_12"
OUT = derived_root() / "lifetime"


def _parse_table(xlsx: bytes, table_id: str) -> pd.DataFrame:
    raw = pd.read_excel(BytesIO(xlsx), header=None)
    title = str(raw.iloc[0, 0])
    header_row = raw.iloc[2].tolist()
    data = raw.iloc[3:].copy()
    data.columns = [
        "age_interval",
        "qx",
        "lx",
        "dx",
        "lx_years",
        "tx",
        "ex",
    ]
    data = data[data["age_interval"].notna()]
    for col in data.columns[1:]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    pop_group = title
    m = re.search(r"for (.+?): United States", title, re.I)
    if m:
        pop_group = m.group(1).strip()
    data["population_group"] = pop_group
    data["table_id"] = table_id
    data["vintage_year"] = 2021
    data["source"] = "cdc_nvsr72_12"
    return data


def build_cdc_life_table_panel(cdc_dir: Path | None = None, out_dir: Path | None = None) -> pd.DataFrame:
    src = cdc_dir or CDC_DIR
    out = out_dir or OUT
    rows: list[pd.DataFrame] = []
    if not src.exists():
        return pd.DataFrame()
    for path in sorted(src.glob("Table*.xlsx")):
        rows.append(_parse_table(path.read_bytes(), path.stem))
    if not rows:
        return pd.DataFrame()
    panel = pd.concat(rows, ignore_index=True)
    out.mkdir(parents=True, exist_ok=True)
    panel.to_csv(out / "cdc_period_life_table_2021.csv", index=False)
    print({"cdc_life_rows": len(panel), "tables": panel["table_id"].nunique()}, flush=True)
    return panel


if __name__ == "__main__":
    build_cdc_life_table_panel()
