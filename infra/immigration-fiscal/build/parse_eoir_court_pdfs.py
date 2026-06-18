#!/usr/bin/env python3
"""Parse curated EOIR adjudication PDFs into CSV panels."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pdfplumber

from paths import data_root, derived_root

EOIR = data_root() / "external" / "stage4" / "courts" / "eoir"
OUT = derived_root() / "stage4" / "eoir"


def _pdf_text(name: str) -> str:
    path = EOIR / name
    if not path.exists():
        return ""
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def parse_historical() -> pd.DataFrame:
    text = _pdf_text("new_cases_completions_historical.pdf")
    rows = []
    for m in re.finditer(
        r"^(19\d{2}|20\d{2}) (\d[\d,]*) (\d[\d,]*) (\d[\d,]*) (\d[\d,]*)",
        text,
        re.M,
    ):
        fy, init_r, init_pm, comp, comp_pm = m.groups()
        rows.append(
            {
                "fiscal_year": int(fy),
                "initial_receipts": int(init_r.replace(",", "")),
                "initial_receipts_per_month": int(init_pm.replace(",", "")),
                "total_completions": int(comp.replace(",", "")),
                "total_completions_per_month": int(comp_pm.replace(",", "")),
                "source": "eoir_new_cases_completions_historical",
            }
        )
    return pd.DataFrame(rows)


def parse_pending() -> pd.DataFrame:
    text = _pdf_text("pending_cases_new_completions.pdf")
    rows = []
    for m in re.finditer(
        r"(20\d{2})(?: \(Second\s+Quarter\))? (\d[\d,]*) (\d[\d,]*) (\d[\d,]*)",
        text,
    ):
        fy, pending, receipts, completions = m.groups()
        rows.append(
            {
                "fiscal_year": int(fy),
                "pending_cases": int(pending.replace(",", "")),
                "initial_receipts": int(receipts.replace(",", "")),
                "total_completions": int(completions.replace(",", "")),
                "source": "eoir_pending_cases_new_completions",
            }
        )
    return pd.DataFrame(rows)


def parse_amnesty_by_state() -> pd.DataFrame:
    text = _pdf_text("amnesty_cases_by_state.pdf")
    rows = []
    for m in re.finditer(
        r"^([A-Z][A-Z .]+?) (\d[\d,]*) (\d[\d,]*)\s*$",
        text,
        re.M,
    ):
        state, open_cases, terminated = m.groups()
        if state.startswith("EXECUTIVE") or state.startswith("ADJUDICATION"):
            continue
        rows.append(
            {
                "state_or_location": state.strip(),
                "amnesty_cases_open": int(open_cases.replace(",", "")),
                "terminated_or_dismissed_by_ij": int(terminated.replace(",", "")),
                "source": "eoir_amnesty_cases_by_state",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panels = {
        "eoir_court_workload_historical_fy.csv": parse_historical(),
        "eoir_pending_cases_fy.csv": parse_pending(),
        "eoir_amnesty_cases_by_state.csv": parse_amnesty_by_state(),
    }
    for name, df in panels.items():
        if df.empty:
            print(f"WARN: no rows for {name}", flush=True)
            continue
        path = OUT / name
        df.to_csv(path, index=False)
        print(f"Wrote {path} ({len(df)} rows)", flush=True)


if __name__ == "__main__":
    main()
