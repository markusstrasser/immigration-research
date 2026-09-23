"""CMS-64 Financial Management Report (FMR) FY2023-2024: LTSS service lines by state.

The FMR is CMS's net-expenditure report from state CMS-64 claims, the administrative source
behind BEA's Medicaid line. Fee-for-service LTSS lines are reported separately; managed LTSS
sits inside capitation ("Medicaid - MCO") and cannot be split here. The lane uses the FMR for
two things: California's In-Home Supportive Services (personal care, 1915(j), 1915(k) Community
First Choice), which T-MSIS TAF does not carry for California in any year 2019-2023, and a scale
check of TAF against CMS-64. Total computable (federal + nonfederal) dollars.
Writes derived/fmr_ltss_lines.csv (long) and prints the national and California rows.
Run from the repo root after fetch_sources.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
      infra/immigration-fiscal/ltss_share_2026_09_23/fmr.py
"""
import hashlib
import io
import json
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
WAYBACK = HERE / "_cache/wayback"
BOOKS = {2023: ("financial-management-report-fy2023.zip", "FY 2023 FMR NET EXPENDITURES.xlsx"),
         2024: ("financial-management-report-fy2024.zip", "FY 2024 FMR NET EXPENDITURES.xlsx")}
LINES = {  # FMR service category -> LTSS group
    "Nursing Facility Services - Reg. Payments": "nf",
    "Nursing Facility Services - Sup. Payments": "nf",
    "Intermediate Care Facility - Public": "icf",
    "Intermediate Care - Private": "icf",
    "Intermediate Care Facility - Individuals with Intellectual Disabilities (ICF/IID): Supplemental Payments": "icf",
    "Mental Health Facility Services - Reg. Payments": "mhf",
    "Mental Health Facility - DSH": "mhf_dsh",
    "Home & Community-Based Services - Regular Payment (1915(c) Waiver)": "hcbs_1915c",
    "Home & Community-Based Services - St. Plan 1915(i) Only Pay.": "hcbs_other",
    "Home & Community-Based Services - St. Plan 1915(j) Only Pay.": "hcbs_pc_cfc",
    "Home & Community Based Services State Plan 1915(k) Community First Choice": "hcbs_pc_cfc",
    "Medicaid MCO - Community First Choice": "hcbs_pc_cfc",
    "Personal Care Services - Reg. Payments": "hcbs_pc_cfc",
    "Personal Care Services - SDS 1915(j)": "hcbs_pc_cfc",
    "All-Inclusive Care Elderly": "hcbs_other",
    "Home Health Services": "hcbs_other",
    "Private Duty Nursing": "hcbs_other",
    "Rehabilitative Services (non-school-based)": "hcbs_other",
    "Targeted Case Management Services - Com. Case-Man.": "hcbs_other",
    "Case Management - State Wide": "hcbs_other",
    "Medicaid - MCO": "mco_capitation",
    "Balance": "map_total",
    "Collections": "collections",
}


def read(year):
    zname, member = BOOKS[year]
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    raw = (WAYBACK / zname).read_bytes()
    if hashlib.sha256(raw).hexdigest() != pins[zname]["sha256"]:
        raise SystemExit(f"[BLOCKED] {zname} changed")
    book = openpyxl.load_workbook(io.BytesIO(zipfile.ZipFile(io.BytesIO(raw)).read(member)),
                                  read_only=True, data_only=True)
    out = []
    for sheet in book.sheetnames:
        if not sheet.startswith("MAP - "):
            continue
        rows = list(book[sheet].values)
        state = rows[2][0]
        head = [i for i, r in enumerate(rows) if r[0] == "Service Category"]
        if len(head) != 1 or rows[head[0]][1] is None or "Total" not in rows[head[0]][1]:
            raise SystemExit(f"[BLOCKED] {sheet}: header")
        seen = set()
        for r in rows[head[0] + 1:]:
            if r[0] in LINES and r[0] not in seen:
                seen.add(r[0])
                out.append(dict(fiscal_year=year, state=state, line=r[0], group=LINES[r[0]],
                                total_computable=float(r[1] or 0)))
        if seen != set(LINES):
            raise SystemExit(f"[BLOCKED] {sheet}: missing {set(LINES) - seen}")
    return out


def main():
    d = pd.DataFrame(read(2023) + read(2024))
    (HERE / "derived").mkdir(exist_ok=True)
    d.to_csv(HERE / "derived/fmr_ltss_lines.csv", index=False)
    g = d.groupby(["state", "group", "fiscal_year"]).total_computable.sum().unstack("fiscal_year") / 1e9
    pd.set_option("display.width", 200)
    for st in ("National Totals", "California", "New York", "Texas"):
        print(st)
        print(g.loc[st].round(3).to_string())
    states = g.drop(index="National Totals", level=0)
    check = states.groupby(level="group").sum() - g.loc["National Totals"]
    print("  ✓ max |sum of states - national| ($bn):", float(check.abs().max().max().round(3)))


if __name__ == "__main__":
    main()
