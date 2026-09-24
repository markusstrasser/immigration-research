"""Parse the BLS Consumer Expenditure Survey tables this lane uses (published xlsx, 2024 and 2023-24).

Each published table lists an item label and then its 'Mean' (and 'Share', 'SE', 'RSE') rows, or,
for characteristics and the cross-tabs, the values on the label row itself. parse() returns
{label: [values by column]} for the first occurrence of each label, plus the column headers.
"""
from __future__ import annotations

import warnings
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "_cache" / "sources"
STATS = {"Mean", "Share", "SE", "RSE", "Percent reporting"}

# Consumption concepts built from the published major categories.
CONSUMPTION_DROP = ["Personal insurance and pensions", "Cash contributions"]
BROAD_TAXABLE_DROP = CONSUMPTION_DROP + ["Shelter", "Healthcare", "Education"]


def _num(x):
    if isinstance(x, (int, float)):
        return float(x)
    return None


def parse(name: str) -> dict:
    import openpyxl
    warnings.filterwarnings("ignore")
    ws = openpyxl.load_workbook(SRC / name, read_only=True, data_only=True).worksheets[0]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    title = str(rows[0][0])
    at = next(i for i, r in enumerate(rows) if r and r[0] == "Item")
    count = next(r for r in rows if r and str(r[0]).startswith("Number of consumer units"))
    ncol = sum(1 for c in count[1:] if _num(c) is not None)
    # Headers can span two rows (Table 2200 splits 'Not Hispanic or Latino' into three columns).
    top, sub = rows[at][1:1 + ncol], rows[at + 1][1:1 + ncol] if rows[at + 1][0] is None else [None] * ncol
    columns = [" ".join(str(x).replace("\n", " ") for x in (a, b) if x is not None) for a, b in zip(top, sub)]
    out, label = {}, None
    for r in rows:
        if not r or r[0] is None:
            continue
        first = str(r[0]).strip()
        values = [_num(c) for c in r[1:1 + ncol]]
        has = any(v is not None for v in values)
        if first in STATS:
            if first == "Mean" and label is not None and label not in out:
                out[label] = values
            continue
        label = first.rstrip(" a/").strip() if first.startswith("Number of consumer units") else first
        if has and label not in out:
            out[label] = values
    out["_columns"] = columns
    out["_title"] = title
    return out


def concepts(t: dict) -> dict:
    """Expenditure concepts per column: total, consumption, broad taxable-type consumption."""
    total = t["Average annual expenditures"]
    def minus(drop):
        return [e - sum(t[k][i] for k in drop) for i, e in enumerate(total)]
    return {"total": total, "consumption": minus(CONSUMPTION_DROP), "taxable_broad": minus(BROAD_TAXABLE_DROP)}


if __name__ == "__main__":
    for f in ["cu-income-deciles-before-taxes-2024.xlsx", "reference-person-latino-2024.xlsx"]:
        t = parse(f)
        print(t["_title"])
        print(t["_columns"])
        for k in ["Income before taxes", "Average annual expenditures", "Personal insurance and pensions",
                  "Cash contributions", "Shelter", "Healthcare", "Education", "People", "Hispanic or Latino"]:
            print(f"  {k:32}", t.get(k))
        c = concepts(t)
        print("  E/Y total      ", [round(e / y, 3) for e, y in zip(c["total"], t["Income before taxes"])])
        print("  C/Y consumption", [round(e / y, 3) for e, y in zip(c["consumption"], t["Income before taxes"])])
        print("  T/Y taxable    ", [round(e / y, 3) for e, y in zip(c["taxable_broad"], t["Income before taxes"])])
