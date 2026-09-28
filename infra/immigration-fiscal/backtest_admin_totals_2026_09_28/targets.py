#!/usr/bin/env python3
"""Phase 2, step 1: the administrative targets, parsed from the raw files in _cache/ exactly as PREDICTIONS.md defines
them. Reads no prediction.

Sources (fetched 2026-09-28, after the parent's go; how each was fetched is in derived/sources.json):
  IRS SOI      _cache/23in55cmcsv.csv                  tax year 2023, all states; rows AGI_STUB = 0 are state totals
  SSA          _cache/ssa_supplement2025_7b.xlsx       Annual Statistical Supplement 2025, Table 7.B7: federally
                                                       administered SSI payments by state, calendar 2024
  SSA          _cache/ssa_ssi_asr24.xlsx               SSI Annual Statistical Report 2024, Tables 10 and 11: recipients
                                                       and average payment by state, December 2024 (a cross-check)
  SSA          _cache/ssa_oasdi_sc24.xlsx              OASDI Beneficiaries by State and County 2024, Table 3: benefits in
                                                       current-payment status by state, December 2024
  CDC WONDER   _cache/wonder_2024_*.tsv                Natality 2016-2024 expanded (D149), year 2024, mother's residence

Writes:
  derived/targets.csv          target x state: value and the state's share of the 50-state + DC total
  derived/target_national.csv  national figures: birth counts, Medicaid-paid shares, SOI and SSA totals
  derived/sources.json         every raw file with its sha256, size, origin and retrieval route

Run from the repository root:
  uv run --no-project --with openpyxl python3 infra/immigration-fiscal/backtest_admin_totals_2026_09_28/targets.py
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
NAMES = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
         "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
         "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
         "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
         "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
         "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
         "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
         "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
         "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
         "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
STATES = sorted(NAMES.values())
SOURCES = {
    "23in55cmcsv.csv": ("https://www.irs.gov/pub/irs-soi/23in55cmcsv.csv", "curl, generic user agent"),
    "soi_23incmdocguide.doc": ("https://www.irs.gov/pub/irs-soi/23incmdocguide.doc", "curl, generic user agent"),
    "ssa_supplement2025_7b.xlsx": ("https://www.ssa.gov/policy/docs/statcomps/supplement/2025/7b.xlsx",
                                   "browser download (SSA refuses scripted requests)"),
    "ssa_ssi_asr24.xlsx": ("https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/ssi_asr24.xlsx",
                           "browser download (SSA refuses scripted requests)"),
    "ssa_oasdi_sc24.xlsx": ("https://www.ssa.gov/policy/docs/statcomps/oasdi_sc/2024/oasdi_sc24.xlsx",
                            "browser download (SSA refuses scripted requests)"),
    "wonder_2024_state_all.tsv": ("https://wonder.cdc.gov/controller/datarequest/D149",
                                  "WONDER web form export; see the query block at the file's end"),
    "wonder_2024_state_x_origin.tsv": ("https://wonder.cdc.gov/controller/datarequest/D149",
                                       "WONDER web form export; see the query block at the file's end"),
    "wonder_2024_state_x_mexico_born.tsv": ("https://wonder.cdc.gov/controller/datarequest/D149",
                                            "WONDER web form export; see the query block at the file's end"),
    "wonder_2024_payer_x_origin.tsv": ("https://wonder.cdc.gov/controller/datarequest/D149",
                                       "WONDER web form export; see the query block at the file's end"),
    "wonder_2024_payer_mexico_born.tsv": ("https://wonder.cdc.gov/controller/datarequest/D149",
                                          "WONDER web form export; see the query block at the file's end"),
    "wonder_natality_expanded_help.html": ("https://wonder.cdc.gov/wonder/help/natality-expanded.html",
                                           "curl, generic user agent (definitions only)"),
}


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def number(x) -> float:
    """A table cell as a number: SSA's '. . .' (not applicable) and WONDER's 'Suppressed' count as 0."""
    if x is None:
        return np.nan
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s in (". . .", "Suppressed", ""):
        return 0.0
    return float(s.replace(",", ""))


def soi() -> tuple[dict[str, pd.Series], dict[str, float]]:
    d = pd.read_csv(CACHE / "23in55cmcsv.csv", usecols=["STATE", "AGI_STUB", "A59660", "A59720", "A11070"],
                    dtype=str)
    d = d[d.AGI_STUB.eq("0")].set_index("STATE")
    num = d[["A59660", "A59720", "A11070"]].map(number)
    if sorted(set(num.index) - {"US", "PR", "OA"}) != STATES:
        raise SystemExit("[BLOCKED] SOI file does not hold the 50 states and DC")
    s = num.loc[STATES] * 1e3  # the file reports amounts in thousands of dollars
    series = {"soi_credits_total": s.A59660 + s.A11070, "soi_credits_refundable": s.A59720 + s.A11070,
              "soi_eitc_total": s.A59660, "soi_eitc_refundable": s.A59720, "soi_actc": s.A11070}
    us = num.loc["US"] * 1e3
    national = {"soi_us_eitc_total": us.A59660, "soi_us_eitc_refundable": us.A59720, "soi_us_actc": us.A11070,
                "soi_51_eitc_total": s.A59660.sum(), "soi_51_actc": s.A11070.sum()}
    return series, national


def sheet_rows(path: Path, sheet: str) -> dict[str, tuple]:
    """State rows of an SSA table: the state name sits in the first column."""
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = {}
    for r in ws.iter_rows(values_only=True):
        name = r[0].strip() if isinstance(r[0], str) else None
        if name in NAMES and name not in rows:
            rows[name] = r
    if sorted(NAMES[n] for n in rows) != STATES:
        raise SystemExit(f"[BLOCKED] {path.name} {sheet} does not hold the 50 states and DC")
    return rows


def ssa() -> tuple[dict[str, pd.Series], dict[str, float]]:
    b7 = sheet_rows(CACHE / "ssa_supplement2025_7b.xlsx", "7.B7")  # State or area | | | Total | Federal | Supplement
    t10 = sheet_rows(CACHE / "ssa_ssi_asr24.xlsx", "Table 10")      # recipients, December 2024: column 3 is total
    t11 = sheet_rows(CACHE / "ssa_ssi_asr24.xlsx", "Table 11")      # average monthly payment: column 3 is total
    t3 = sheet_rows(CACHE / "ssa_oasdi_sc24.xlsx", "Table 3")       # December 2024 benefits: column 3 is total
    by = lambda rows, col, scale=1.0: pd.Series({NAMES[n]: number(r[col]) * scale for n, r in rows.items()}).loc[STATES]
    series = {"ssa_ssi_fed_admin_2024": by(b7, 3, 1e3), "ssa_ssi_federal_2024": by(b7, 4, 1e3),
              "ssa_ssi_supplement_2024": by(b7, 5, 1e3),
              "ssa_ssi_fed_admin_dec2024": by(t10, 3) * by(t11, 3),
              "ssa_oasdi_dec2024": by(t3, 3, 1e3)}
    gap = (series["ssa_ssi_federal_2024"] + series["ssa_ssi_supplement_2024"] - series["ssa_ssi_fed_admin_2024"]).abs()
    if gap.max() > 1e3:  # one thousand dollars: the table's rounding unit
        raise SystemExit("[BLOCKED] SSA Table 7.B7: federal plus supplement does not equal the total")
    return series, {k: float(v.sum()) for k, v in series.items()}


def wonder(name: str) -> pd.DataFrame:
    """A WONDER export's data rows (the block before the first '---'); 'Suppressed' counts as 0."""
    text = (CACHE / name).read_text()
    table = text.split('"---"')[0]
    rows = [line.split("\t") for line in table.strip().splitlines()]
    head = [h.strip('"') for h in rows[0]]
    body = [dict(zip(head, [c.strip('"') for c in r])) for r in rows[1:] if r[0].strip('"') != "Total"]
    frame = pd.DataFrame(body)
    frame["Births"] = frame.Births.map(number)
    query = re.findall(r'^"(Year: [^"]*|Group By: [^"]*|Mother\'s Birth Country: [^"]*)"$', text, flags=re.M)
    if "Year: 2024" not in query:
        raise SystemExit(f"[BLOCKED] {name} is not a 2024 query")
    return frame


def births() -> tuple[dict[str, pd.Series], dict[str, float]]:
    fips_to_state = {}
    series = {}
    for key, name, keep in (("wonder_births_all", "wonder_2024_state_all.tsv", None),
                            ("wonder_births_mex_origin", "wonder_2024_state_x_origin.tsv", "Mexican"),
                            ("wonder_births_mexico_born", "wonder_2024_state_x_mexico_born.tsv", None)):
        f = wonder(name)
        if keep is not None:
            f = f[f["Mother's Expanded Hispanic Origin"].eq(keep)]
        f = f.assign(state=f["State of Residence"].map(NAMES))
        if f.state.isna().any() or sorted(f.state) != STATES:
            raise SystemExit(f"[BLOCKED] {name} does not hold the 50 states and DC once each")
        fips_to_state.update(dict(zip(f["State of Residence Code"], f.state)))
        series[key] = f.set_index("state").Births.loc[STATES]
    national = {k: float(v.sum()) for k, v in series.items()}
    national["wonder_births_mex_origin_suppressed_states"] = float(
        (wonder("wonder_2024_state_x_origin.tsv").pipe(
            lambda f: f[f["Mother's Expanded Hispanic Origin"].eq("Mexican") & f.Births.eq(0)]).shape[0]))

    pay = wonder("wonder_2024_payer_x_origin.tsv")
    pay_mx = wonder("wonder_2024_payer_mexico_born.tsv")
    col = "Source of Payment for Delivery"
    known = lambda f: f[~f[col].eq("Unknown or Not Stated")]
    for group, f in (("all", pay), ("mex_origin", pay[pay["Mother's Expanded Hispanic Origin"].eq("Mexican")]),
                     ("mexico_born", pay_mx)):
        national[f"wonder_births_{group}_payer_known"] = float(known(f).Births.sum())
        national[f"wonder_births_{group}_medicaid"] = float(f[f[col].eq("Medicaid")].Births.sum())
        national[f"wonder_births_{group}_payer_unknown"] = float(f[f[col].eq("Unknown or Not Stated")].Births.sum())
        national[f"wonder_medicaid_share_{group}"] = (national[f"wonder_births_{group}_medicaid"]
                                                      / national[f"wonder_births_{group}_payer_known"])
    for group in ("mex_origin", "mexico_born"):
        national[f"wonder_medicaid_ratio_{group}"] = (national[f"wonder_medicaid_share_{group}"]
                                                      / national["wonder_medicaid_share_all"])
        national[f"wonder_medicaid_group_share_{group}"] = (national[f"wonder_births_{group}_medicaid"]
                                                            / national["wonder_births_all_medicaid"])
    # the payer tables are national; their totals must match the state tables' sums
    for group, f in (("all", pay), ("mex_origin", pay[pay["Mother's Expanded Hispanic Origin"].eq("Mexican")]),
                     ("mexico_born", pay_mx)):
        national[f"wonder_births_{group}_payer_table_total"] = float(f.Births.sum())
    return series, national


def main() -> None:
    parts = [soi(), ssa(), births()]
    rows, national = [], {}
    for series, nat in parts:
        national.update(nat)
        for target, s in series.items():
            share = s / s.sum()
            rows += [dict(target=target, state=st, value=s[st], share=share[st]) for st in STATES]
    pd.DataFrame(rows).to_csv(OUT / "targets.csv", index=False, float_format="%.12g", lineterminator="\n")
    pd.DataFrame([dict(quantity=k, value=v) for k, v in national.items()]).to_csv(
        OUT / "target_national.csv", index=False, float_format="%.12g", lineterminator="\n")
    sources = {name: {"url": url, "route": route, "sha256": sha(CACHE / name), "bytes": (CACHE / name).stat().st_size,
                      "retrieved": "2026-09-28"}
               for name, (url, route) in SOURCES.items()}
    (OUT / "sources.json").write_text(json.dumps(sources, indent=1, sort_keys=True) + "\n")
    for key in ("wonder_births_mex_origin", "wonder_births_all", "soi_51_eitc_total"):
        print(f"  ✓ {key}: {national[key]:,.0f}")


if __name__ == "__main__":
    main()
