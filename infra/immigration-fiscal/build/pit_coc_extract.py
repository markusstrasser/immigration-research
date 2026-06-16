#!/usr/bin/env python3
"""Per-CoC PIT totals (overall / sheltered / unsheltered) from HUD AHAR xlsb.

Adapted from SSDALab/CoCHomeless data-raw/pit_coc_extract.py
"""
from __future__ import annotations

import re
import sys

import pandas as pd


def extract(infile: str, outfile: str) -> int:
    xl = pd.ExcelFile(infile, engine="pyxlsb")
    rows: list[pd.DataFrame] = []
    for s in [s for s in xl.sheet_names if re.fullmatch(r"\d{4}", str(s))]:
        df = pd.read_excel(xl, sheet_name=s)
        coc = next(c for c in df.columns if "CoC Number" in str(c))

        def pick(name: str):
            return next((c for c in df.columns if str(c).strip() == name), None)

        ct, csh, cun = (
            pick("Overall Homeless"),
            pick("Sheltered Total Homeless"),
            pick("Unsheltered Homeless"),
        )
        name_col = next((c for c in df.columns if "CoC Name" in str(c)), None)
        cols = [coc, ct, csh, cun] + ([name_col] if name_col else [])
        sub = df[cols].copy()
        sub.columns = ["coc_id", "total", "sheltered", "unsheltered"] + (
            ["coc_name"] if name_col else []
        )
        sub["coc_id"] = sub["coc_id"].astype(str).str.strip()
        sub = sub[sub["coc_id"].str.match(r"^[A-Z]{2}-[0-9A-Za-z]{3}$", na=False)]
        for c in ["total", "sheltered", "unsheltered"]:
            sub[c] = pd.to_numeric(sub[c], errors="coerce")
        sub = sub.dropna(subset=["total"])
        sub["year"] = int(s)
        rows.append(sub)
    out = pd.concat(rows, ignore_index=True).sort_values(["coc_id", "year"])
    keep = ["coc_id", "year", "total", "sheltered", "unsheltered"]
    if "coc_name" in out.columns:
        keep.append("coc_name")
    out = out[keep]
    out.to_csv(outfile, index=False)
    print(
        f"wrote {len(out)} rows, {out.coc_id.nunique()} CoCs, "
        f"years {out.year.min()}-{out.year.max()} -> {outfile}"
    )
    return len(out)


if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2])
