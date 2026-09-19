#!/usr/bin/env python3
"""Arm 4: stock-flow accounting from the DHS January 2022 stock forward.

Two independent reconciliations, both starting from the same published stock:

  A. CBO's other-foreign-national (OFN) net-immigration series, which is itself a
     stock-flow accounting over DHS administrative data.  Add it to the DHS
     January 2022 residual and compare the implied stock with survey residuals.

  B. A bottom-up accounting from CBP's own disposition table: releases, paroles,
     transfers to HHS and gotaways in, repatriations and modelled exits out, with
     the residency share of encounters as the free parameter.  This exposes how
     much of the answer that one parameter is carrying.

Inputs (all cached under _cache/sources/, all fetched from the issuing agency):
  ohss_monthly_nov2024.xlsx  DHS OHSS, Immigration Enforcement and Legal Processes
                             Monthly Tables, November 2024 (the last edition
                             published; the series stops there)
  sources.json               CBO OFN series and the DHS/Pew/CMS/MPI/CIS estimates,
                             each quoted from its primary document

Output: derived/stock_flow_cbo.csv
        derived/stock_flow_dispositions.csv
        derived/stock_flow_sensitivity.csv
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")

HERE = Path(__file__).resolve().parent
SRC = HERE / "_cache" / "sources"
DERIVED = HERE / "derived"
XLSX = SRC / "ohss_monthly_nov2024.xlsx"

# Known gotaways, US House Committee on Homeland Security, "September 2024 Border
# Report", Part 7.  Quoted: "Through June of FY24, CBP had recorded 194,000
# gotaways. In FY23, CBP recorded 694,685 gotaways, 737,244 in FY22, and 389,155
# in FY21. The approximately two million known gotaways since FY21 far exceeds the
# 1.29 million recorded from FY10-20 combined."
# Provenance is uneven and is reported with the number: the FY21 figure traces to a
# DHS Border Security Metrics Report, FY22 to an ICE budget justification, FY24 to
# a journalist's posting of unpublished CBP data.  [UNVERIFIED] for FY24.
GOTAWAYS = {2021: 389155, 2022: 737244, 2023: 694685, 2024: 194000}
GOTAWAY_NOTE = {2021: "DHS Border Security Metrics Report (via House report)",
                2022: "ICE FY2025 Congressional Justification (via House report)",
                2023: "House report, CBP data",
                2024: "[UNVERIFIED] through June FY24 only; journalist posting of internal CBP data"}


def fy_totals(sheet: str, header_row: int = 3) -> pd.DataFrame:
    """Fiscal-year total rows from an OHSS monthly-table sheet."""
    d = pd.read_excel(XLSX, sheet_name=sheet, header=None)
    cols = d.iloc[header_row].tolist()
    body = d.iloc[header_row + 1:].copy()
    body.columns = [str(c) for c in cols]
    body = body[body.iloc[:, 1].astype(str).str.strip().eq("Total")]
    body = body.rename(columns={body.columns[0]: "fiscal_year"})
    body["fiscal_year"] = pd.to_numeric(body["fiscal_year"], errors="coerce")
    body = body.dropna(subset=["fiscal_year"])
    body["fiscal_year"] = body["fiscal_year"].astype(int)
    return body.reset_index(drop=True)


def num(v):
    """OHSS writes 'X' for not-applicable and '-' for zero."""
    if isinstance(v, str):
        v = v.strip()
        if v in {"X", "-", "", "D"}:
            return 0.0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    DERIVED.mkdir(exist_ok=True)
    s = json.loads((HERE / "sources.json").read_text())
    cbo = s["cbo_ofn_net_immigration"]["net_by_year"]
    dhs_jan2022 = s["dhs_residual_components_jan2022"]["unauthorized_jan2022"]

    # ---------------- A. CBO OFN reconciliation ------------------------------
    print("[1/4] CBO other-foreign-national reconciliation")
    rows = []
    stock = float(dhs_jan2022)
    rows.append({"as_of": "2022-01-01", "opening_stock": None,
                 "cbo_ofn_net": None, "closing_stock": round(stock),
                 "note": "DHS OHSS published residual, January 1 2022"})
    for year in [2022, 2023, 2024, 2025]:
        net = float(cbo[str(year)])
        opening = stock
        stock = opening + net
        rows.append({"as_of": f"{year + 1}-01-01", "opening_stock": round(opening),
                     "cbo_ofn_net": round(net), "closing_stock": round(stock),
                     "note": "CBO calendar-year net immigration, OFN category"})
    cbo_tab = pd.DataFrame(rows)
    cbo_tab.to_csv(DERIVED / "stock_flow_cbo.csv", index=False)
    print(cbo_tab.to_string(index=False))

    # ---------------- B. CBP disposition accounting --------------------------
    print("\n[2/4] CBP southwest-border encounter dispositions, FY2021-FY2025")
    book = fy_totals("CBP SWB Book-Outs by Agency")
    keep = ["Total Encounters", "T8 repatriations1", "T42 expulsions2",
            "Migrant Protection Protocols3", "Transfers to ICE4",
            "Transfers to HHS5", "USBP Releases6", "OFO Paroles7", "Other outcomes8"]
    # The sheet repeats the column block for Total CBP, USBP and OFO; the first
    # occurrence of each label is the Total CBP block.
    first = {}
    for i, c in enumerate(book.columns):
        if c in keep and c not in first:
            first[c] = i
    disp = pd.DataFrame({"fiscal_year": book.fiscal_year})
    for c in keep:
        disp[c] = book.iloc[:, first[c]].map(num).values
    disp = disp[disp.fiscal_year.between(2021, 2025)].reset_index(drop=True)
    disp["known_gotaways"] = disp.fiscal_year.map(GOTAWAYS).fillna(0.0)
    disp["gotaway_source"] = disp.fiscal_year.map(GOTAWAY_NOTE).fillna("not published")
    # Releases into the interior that DHS itself books out as such.
    disp["released_or_paroled"] = (disp["USBP Releases6"] + disp["OFO Paroles7"]
                                   + disp["Transfers to HHS5"])
    disp.to_csv(DERIVED / "stock_flow_dispositions.csv", index=False)
    print(disp.to_string(index=False))
    print("  note: FY2025 covers October-November 2024 only; the OHSS monthly "
          "series stops with the November 2024 edition.")

    # ---------------- C. sensitivity to the residency share ------------------
    print("\n[3/4] sensitivity: what share of border releases and gotaways stayed")
    rep = fy_totals("DHS Repats by Type")
    rep_first = {}
    for i, c in enumerate(rep.columns):
        if c not in rep_first:
            rep_first[c] = i
    removals = {}
    for _, r in rep.iterrows():
        fy = int(r["fiscal_year"])
        removals[fy] = num(r.iloc[rep_first["Total Removals"]])
    # Window: calendar 2022 through 2024, approximated by FY2022-FY2024, the
    # period both the encounter table and the CBO series cover in full.
    window = [2022, 2023, 2024]
    releases = float(disp[disp.fiscal_year.isin(window)]["released_or_paroled"].sum())
    gotaways = float(disp[disp.fiscal_year.isin(window)]["known_gotaways"].sum())
    removals_w = float(sum(removals.get(y, 0.0) for y in window))
    print(f"  releases+paroles+HHS transfers FY22-24: {releases:,.0f}")
    print(f"  known gotaways FY22-24 (FY24 partial):  {gotaways:,.0f}")
    print(f"  DHS removals FY22-24:                   {removals_w:,.0f}")

    cbo_window = sum(float(cbo[str(y)]) for y in window)
    rows = []
    for share in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        added = share * (releases + gotaways)
        implied_other = cbo_window - added  # overstays etc. minus all exits
        rows.append({
            "residency_share_of_releases_and_gotaways": share,
            "implied_additions_fy22_24": round(added),
            "cbo_ofn_net_2022_2024": round(cbo_window),
            "residual_other_flows": round(implied_other),
            "stock_jan2025_if_only_these_flows": round(dhs_jan2022 + added),
        })
    sens = pd.DataFrame(rows)
    sens.to_csv(DERIVED / "stock_flow_sensitivity.csv", index=False)
    print(sens.to_string(index=False))

    print("\n[4/4] comparison with the survey residuals")
    implied_jan2026 = float(cbo_tab.closing_stock.iloc[-1])
    implied_jan2025 = float(cbo_tab[cbo_tab.as_of == "2025-01-01"].closing_stock.iloc[0])
    comp = pd.DataFrame([
        {"estimate": "Stock-flow: DHS Jan-2022 + CBO OFN net 2022-2024",
         "as_of": "2025-01-01", "value": round(implied_jan2025)},
        {"estimate": "Stock-flow: DHS Jan-2022 + CBO OFN net 2022-2025",
         "as_of": "2026-01-01", "value": round(implied_jan2026)},
        {"estimate": "CIS CPS residual, coverage-adjusted", "as_of": "2025-01-01",
         "value": 15800000},
        {"estimate": "CIS CPS residual, coverage-adjusted", "as_of": "2026-07-01",
         "value": 13500000},
        {"estimate": "MPI ACS residual", "as_of": "2024-07-01", "value": 15754000},
        {"estimate": "CMS ACS residual", "as_of": "2024-07-01", "value": 14610000},
        {"estimate": "This lane, CPS ASEC 2025 Borjas residual, no coverage adj.",
         "as_of": "2025-03-01", "value": 14896401},
        {"estimate": "This lane, ACS 2024 Borjas residual, no coverage adj.",
         "as_of": "2024-07-01", "value": 12973901},
    ])
    comp.to_csv(DERIVED / "stock_flow_comparison.csv", index=False)
    print(comp.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
