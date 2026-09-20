"""Locate national fiscal residuals without assigning them to an ethnic group."""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
BEA_DEFAULT = _data_paths.data_root(require_exists=False) / 'external/bea_nipa/Section3All_xls.xlsx'


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def same(actual, expected, label, tolerance=.003):
    if not np.isfinite([actual, expected]).all() or abs(actual - expected) > tolerance:
        raise ValueError(f"{label}: {actual} != {expected}")


def read_table(rows, year=2024):
    headers = [r for r in rows if r and r[0] == "Line"]
    if len(headers) != 1 or rows[1][0] != "[Millions of dollars]":
        raise ValueError("BEA header/units changed")
    cols = [i for i, value in enumerate(headers[0]) if str(value) == str(year)]
    if len(cols) != 1:
        raise ValueError("BEA year missing or ambiguous")
    out = {}
    for row in rows:
        if not str(row[0]).isdigit():
            continue
        number = int(row[0])
        if number in out:
            raise ValueError("Duplicate BEA line")
        value = row[cols[0]]
        # Suppressed/nonapplicable cells remain missing, never silently zero.
        out[number] = {"label": row[1].strip(), "amount_bn":
                       value / 1000 if isinstance(value, (int, float)) else None}
    return out


def value(tables, sheet, line):
    result = tables[sheet][line]["amount_bn"]
    if result is None or not np.isfinite(result):
        raise ValueError(f"Missing required BEA observation: {sheet}/{line}")
    return result


def verified_output(folder, name, fingerprints):
    audit_path = folder / "audit.json"
    audit = json.loads(audit_path.read_text())
    path = folder / f"{name}.csv"
    if sha(path) != audit["outputs"][name]:
        raise ValueError(f"Stale or modified upstream output: {path}")
    for source, expected in audit.get("source_hashes", {}).items():
        if sha(source) != expected:
            raise ValueError(f"Upstream dependency drift: {source}")
    fingerprints[str(audit_path)] = sha(audit_path)
    fingerprints[str(path)] = sha(path)
    return pd.read_csv(path)


def credit_presentation(receipts, spending, credits):
    """Move refundable credits from negative receipts to positive spending."""
    return receipts + credits, spending + credits


def receipt_rows(tables, raw, tax):
    v = lambda sheet, line: value(tables, sheet, line)
    a = lambda line: v("T30100-A", line)
    p = lambda line: v("T30400-A", line)
    s = lambda line: v("T30500-A", line)
    c = lambda line: v("T30600-A", line)
    entries = [
        ("federal_income_tax", p(3), tax.federal_before_refundable,
         "BEA cash/timing and CPS modeled liability differ; CPS EITC/ACTC moved to spending"),
        ("state_local_income_tax", p(9), tax.state_after_credits,
         "CPS state modeled tax versus state/local collections; credits/timing/universe differ"),
        ("other_personal_taxes", p(1)-p(3)-p(9), 0,
         "Motor vehicle licenses, personal property and other personal taxes not explicitly modeled"),
        ("employee_self_oasdi_hi", c(22), tax.fica_cps,
         "CPS tax simulation versus OASDI/HI accounts; exemptions and populations differ"),
        ("employer_oasdi_hi", c(4), raw.loc["employer", "receipts_bn"],
         "All-covered employer wage proxy; coverage assumptions need separate testing"),
        ("medicare_supplementary_premiums", c(27), 0,
         "Explicit contribution category not represented in modeled payroll receipts"),
        ("other_domestic_social_contributions", a(8)-c(22)-c(4)-c(27), 0,
         "UI, railroad, workers compensation and other funds; no ethnic incidence assigned"),
        ("corporate_income_tax", a(5), raw.loc["C", "receipts_bn"],
         "CPS incidence allocation of FY corporate pool versus calendar-year NIPA"),
        ("general_sales_tax", s(20), raw.loc["sales", "receipts_bn"],
         "Consumption-proxy tax covers part of total, including business purchases; no automatic rake"),
        ("production_property_tax", s(38), raw.loc["owner_property", "receipts_bn"],
         "Owner-housing proxy versus broader real/property tax base including business/rental property"),
        ("excise_selective_sales", s(4)+s(23), raw.loc["X", "receipts_bn"],
         "Federal and state/local FY pool versus calendar NIPA; definition/timing differences"),
        ("customs_duties", s(15), 0,
         "Absent explicit tariff incidence; residents/importers/foreign suppliers not identified"),
        ("other_production_taxes", s(1)-s(20)-s(38)-s(4)-s(23)-s(15), 0,
         "Other production/product taxes; definitions include licenses and assessments"),
        ("rest_world_tax_contributions", a(6)+a(9), 0,
         "Foreign-origin receipts are outside the resident household universe"),
        ("government_asset_income", a(10), 0,
         "Interest rents royalties dividends; household payment and benefit incidence unresolved"),
        ("current_transfer_receipts", a(15), 0,
         "Fines settlements and other transfers; household/business/foreign incidence differs"),
        ("enterprise_surplus", a(19), 0,
         "Net government enterprise operating surplus, negative in 2024"),
    ]
    rows = [dict(category=name, official_bn=official, modeled_bn=modeled,
                 difference_bn=official-modeled, interpretation=note)
            for name, official, modeled, note in entries]
    # Published rounded component tables need not sum to their rounded parent.
    rounding = a(1)-sum(r["official_bn"] for r in rows)
    if abs(rounding) > .005:
        raise ValueError(f"Receipt crosswalk is not exhaustive: {rounding}")
    rows.append(dict(category="source_rounding", official_bn=rounding, modeled_bn=0,
                     difference_bn=rounding, interpretation="Displayed BEA rounding only"))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=HERE.parents[2])
    parser.add_argument("--bea", type=Path, default=BEA_DEFAULT)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    fiscal = args.source_root.resolve() / "infra/immigration-fiscal"
    hashes = {str(Path(__file__)): sha(__file__)}
    if sha(args.bea) != BEA_SHA:
        raise ValueError("Unreviewed BEA source revision")
    hashes[str(args.bea)] = BEA_SHA
    book = openpyxl.load_workbook(args.bea, read_only=True, data_only=True)
    tables = {name: read_table(list(book[name].values))
              for name in ["T30100-A", "T30400-A", "T30500-A", "T30600-A"]}
    book.close()
    a = lambda line: value(tables, "T30100-A", line)
    same(a(1), 8008.290, "2024 receipts anchor")
    same(a(20), 10061.458, "2024 expenditure anchor")
    macro = fiscal / "macro_closure_2026_09_19/derived"
    accounts = verified_output(macro, "updated_account_components", hashes)
    f = verified_output(macro, "F_attribution", hashes)
    tax = verified_output(fiscal / "admin_tax_checks_2026_09_19/derived", "group_components", hashes)
    absolute = fiscal / "ledger_absolute_2026_09_17/derived/audit.json"
    audit = json.loads(absolute.read_text())
    hashes[str(absolute)] = sha(absolute)
    omitted = audit["item_metadata"]["R|central"]["detail"]["zero_in_central"]["dollars"]
    if set(omitted) != {"150", "250", "270", "300", "350", "370", "450"}:
        raise ValueError("Changed omitted federal function definition")
    receipt, bridges, omitted_rows, presentation = [], [], [], []
    for allocation in ["shared", "personal"]:
        raw = accounts.query("allocation == @allocation and group == 'national_civilian'").set_index("component")
        t = tax.query("allocation == @allocation and group == 'national_civilian'").set_index("metric").value / 1e9
        credits = t.eitc+t.actc
        same(t.federal_before_refundable-t.federal_after_refundable, credits, "Refundable tax identity", 1e-7)
        same(t.federal_after_refundable+t.fica_cps+t.state_after_credits, raw.loc["tax","receipts_bn"], "Canonical tax bridge", 1e-7)
        fees = raw.loc["G_fee_grossup", "receipts_bn"]
        r0 = raw.receipts_bn.sum()-fees
        e0 = raw.spending_bn.sum()-fees
        r1, e1 = credit_presentation(r0, e0, credits)
        same(r1-e1, r0-e0, "Presentation preserves net balance", 1e-7)
        rows = receipt_rows(tables, raw, t)
        same(sum(row["modeled_bn"] for row in rows), r1, "Every modeled receipt owned once", 1e-7)
        same(sum(row["difference_bn"] for row in rows), a(1)-r1, "Exhaustive receipt residual", 1e-7)
        receipt.extend(dict(allocation=allocation, **row) for row in rows)
        presentation.append(dict(allocation=allocation, credits_moved_bn=credits,
                                 old_receipts_bn=r0, old_spending_bn=e0,
                                 presented_receipts_bn=r1, presented_spending_bn=e1,
                                 balance_bn=r1-e1))
        national = f.query("allocation == @allocation and group == 'national_civilian'").iloc[0]
        population_ratio = -national.per_capita_F_charge_bn / national.administrative_F_bn
        f_amount = -national.per_capita_F_charge_bn
        # A waterfall of existing model conventions, not a NIPA reconciliation
        # correction: federal FY pools and calendar current expenditure differ.
        # Gross zeroed-function pools include grants whose final state/local
        # services may already be in G/P. Unresolved ownership cannot close a gap.
        steps = [("raw_model", 0), ("credits_on_spending_side", credits),
                 ("include_existing_F_average_cost_arm", f_amount)]
        running = e0
        for name, delta in steps:
            running += delta
            bridges.append(dict(allocation=allocation, step=name, added_spending_bn=delta,
                                cumulative_spending_bn=running, remaining_current_gap_bn=a(20)-running,
                                classification="Source/convention diagnostic only; no ethnic allocation or causal saving"))
        for code, dollars in omitted.items():
            omitted_rows.append(dict(allocation=allocation, function=code, source_fy2024_bn=dollars/1e9,
                                     household_scaled_bn=dollars/1e9*population_ratio,
                                     included_in_spending_bridge=False,
                                     status="GROSS_POOL_ONLY_GRANT_OWNERSHIP_UNRESOLVED"))
        # Gross investment is NOT simply added to current spending: CFC is there.
        same(a(37), a(20)+a(39)+a(40)+a(41)-a(42), "Current to total spending bridge")
        same(a(34), a(1)+a(36), "Current to total receipt bridge")
    frames = {"receipt_crosswalk": pd.DataFrame(receipt), "spending_conventions": pd.DataFrame(bridges),
              "omitted_federal_functions": pd.DataFrame(omitted_rows), "credit_presentation": pd.DataFrame(presentation),
              "official_cells": pd.DataFrame([dict(sheet=s, line=n, **cell) for s, lines in tables.items() for n, cell in lines.items()])}
    args.out.mkdir(parents=True, exist_ok=True)
    for name, frame in frames.items():
        frame.to_csv(args.out / f"{name}.csv", index=False)
    result = dict(source_hashes=hashes, outputs={name: sha(args.out/f"{name}.csv") for name in frames},
                  bea_url="https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx",
                  source_year=2024, source_vintage="August 26, 2026", group_correction_applied=False,
                  limitations=["No identified ethnic incidence for unexplained national receipts or expenditures",
                               "Spending waterfall mixes source concepts and is not a complete NIPA crosswalk",
                               "Seven zeroed function pools include unresolved grant overlap and do not reduce the spending residual",
                               "Public-good attribution is a convention, not measured marginal cost",
                               "Refundable-credit move is presentation only and retains existing CPS scope"])
    (args.out / "audit.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(frames["receipt_crosswalk"].query("allocation == 'shared'")[["category","difference_bn"]].to_string(index=False))
    print(frames["spending_conventions"].to_string(index=False))


if __name__ == "__main__":
    main()
