"""Construction cost shares from BEA industry accounts (files in _cache/bea/, fetched by fetch.py).

1. 2017 benchmark detail Use table (before redefinitions, producers' prices): intermediate
   inputs, compensation, taxes and gross operating surplus as shares of industry output for the
   residential construction industries.
2. Construction (NAICS 23) in 2017 and 2024: gross output (GDP-by-industry TGO105), value added
   and its components (TVA113), nonfarm proprietors' income (NIPA 6.12D) and compensation
   (NIPA 6.2D, a cross-check on TVA113).
Labour's share of gross output counts compensation plus a fraction lambda of proprietors'
income (the self-employed's labour); lambda 0.5 / 0.67 / 1.0.

Output: derived/inputs_bea.csv (one row per item, with its source cell description).
Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/inputs.py
"""
from __future__ import annotations

import pathlib
import zipfile

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
BEA = HERE / "_cache/bea"
DERIVED = HERE / "derived"
DETAIL = "IOUse_Before_Redefinitions_PRO_2017_Detail.xlsx"
RESIDENTIAL = {"233411": "single_family", "233412": "multifamily", "2334A0": "other_residential",
               "230302": "residential_repair"}
LAMBDA = {"low": 0.5, "central": 2 / 3, "high": 1.0}


def detail_shares():
    if not (BEA / DETAIL).exists():
        with zipfile.ZipFile(BEA / "AllTablesIO.zip") as z:
            z.extract(DETAIL, BEA)
    df = pd.read_excel(BEA / DETAIL, sheet_name="2017", header=None)
    codes = [str(c) for c in df.iloc[5].tolist()]
    rows = [str(c) for c in df[0].tolist()]
    cell = lambda r, c: float(df.iat[rows.index(r), codes.index(c)])
    out = []
    for code, name in RESIDENTIAL.items():
        total = cell("T008", code)
        for item, label in (("T005", "intermediate"), ("V00100", "compensation"),
                            ("V00200", "taxes_on_production"), ("V00300", "gross_operating_surplus")):
            out.append({"item": f"{name}_{label}_share_2017", "value": cell(item, code) / total,
                        "source": f"BEA 2017 detail Use, before redefinitions, row {item}, column {code}"})
        out.append({"item": f"{name}_output_2017_bn", "value": total / 1e3,
                    "source": f"BEA 2017 detail Use, row T008, column {code}"})
    return out


def year_row(path, sheet, label, header_row=7):
    df = pd.read_excel(path, sheet_name=sheet, header=None)
    years = [str(v).split(".")[0] for v in df.iloc[header_row].tolist()]
    hits = [r for r in range(len(df)) if str(df.iat[r, 1]).strip() == label]
    return df, years, hits


def construction_totals():
    out = []
    # Gross output by industry, current dollars.
    df, years, hits = year_row(BEA / "GrossOutput.xlsx", "TGO105-A", "Construction")
    if len(hits) != 1:
        raise ValueError(f"TGO105 construction rows: {hits}")
    for y in ("2017", "2024"):
        out.append({"item": f"construction_gross_output_{y}_bn",
                    "value": float(df.iat[hits[0], years.index(y)]) / 1e3,
                    "source": "BEA GDP by industry TGO105-A, Construction"})
    # Components of value added: the three rows directly below the Construction line.
    df, years, hits = year_row(BEA / "ValueAdded.xlsx", "TVA113-A", "Construction")
    if len(hits) != 1:
        raise ValueError(f"TVA113 construction rows: {hits}")
    r = hits[0]
    labels = {r: "value_added", r + 1: "compensation", r + 2: "taxes_on_production",
              r + 3: "gross_operating_surplus"}
    expected = {r + 1: "Compensation of employees", r + 2: "Taxes on production and imports less subsidies",
                r + 3: "Gross operating surplus"}
    for row, text in expected.items():
        if str(df.iat[row, 1]).strip() != text:
            raise ValueError(f"TVA113 layout changed at row {row}")
    for row, name in labels.items():
        for y in ("2017", "2024"):
            out.append({"item": f"construction_{name}_{y}_bn",
                        "value": float(df.iat[row, years.index(y)]) / 1e3,
                        "source": "BEA GDP by industry TVA113-A, Construction"})
    for sheet, name in (("T61200D-A", "proprietors_income"), ("T60200D-A", "compensation_nipa")):
        df = pd.read_excel(BEA / "Section6All_xls.xlsx", sheet_name=sheet, header=None)
        years = [str(v).split(".")[0] for v in df.iloc[7].tolist()]
        hits = [i for i in range(len(df)) if str(df.iat[i, 1]).strip() == "Construction"]
        if len(hits) != 1:
            raise ValueError(f"{sheet} construction rows: {hits}")
        for y in ("2017", "2024"):
            out.append({"item": f"construction_{name}_{y}_bn",
                        "value": float(df.iat[hits[0], years.index(y)]) / 1e3,
                        "source": f"BEA NIPA {sheet.split('-')[0]}, Construction"})
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    rows = detail_shares() + construction_totals()
    v = {r["item"]: r["value"] for r in rows}
    for y in ("2017", "2024"):
        if abs(v[f"construction_compensation_{y}_bn"] - v[f"construction_compensation_nipa_{y}_bn"]) > 0.5:
            raise ValueError(f"TVA113 and NIPA 6.2D compensation disagree in {y}")
        go = v[f"construction_gross_output_{y}_bn"]
        rows.append({"item": f"construction_intermediate_share_{y}",
                     "value": 1 - v[f"construction_value_added_{y}_bn"] / go,
                     "source": "1 - value added / gross output [CALCULATION]"})
        rows.append({"item": f"construction_proprietors_income_share_{y}",
                     "value": v[f"construction_proprietors_income_{y}_bn"] / go,
                     "source": "proprietors' income / gross output [CALCULATION]"})
        for level, lam in LAMBDA.items():
            rows.append({"item": f"construction_labour_share_{y}_{level}",
                         "value": (v[f"construction_compensation_{y}_bn"]
                                   + lam * v[f"construction_proprietors_income_{y}_bn"]) / go,
                         "source": f"(compensation + {lam:.2f} x proprietors' income) / gross output [CALCULATION]"})
    # Single-family residential: detail compensation share plus the industry-wide proprietors'
    # income share of output scaled by lambda (the detail table does not split GOS).
    v = {r["item"]: r["value"] for r in rows}
    for level, lam in LAMBDA.items():
        rows.append({"item": f"single_family_labour_share_2017_{level}",
                     "value": v["single_family_compensation_share_2017"]
                     + lam * v["construction_proprietors_income_share_2017"],
                     "source": "detail compensation share + lambda x construction-wide proprietors' "
                               "income share of output, 2017 [CALCULATION]"})
    pd.DataFrame(rows).to_csv(DERIVED / "inputs_bea.csv", index=False)
    for r in rows:
        print(f"{r['item']:52s} {r['value']:12.4f}")


if __name__ == "__main__":
    main()
