"""Extract pinned IRS owner-income distributions and allocated AGI-bin tax rates.

uv run --no-project --with xlrd python3 {lane}/owner_tax_sources.py [--acquire]
The default is offline and fail-loud on missing/stale primary files. No microdata,
ownership allocation, behavioral response, or normal-return share is estimated here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import shutil
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE / "inputs"
CACHE = HERE / "_cache" / "owner"
SOURCES = {
    **{f"{y}in{t}.xls": f"https://www.irs.gov/pub/irs-soi/{y}in{t}.xls"
       for y in (22, 23) for t in ("12ms", "14ar")},
    "p514--2024.pdf": "https://www.irs.gov/pub/irs-prior/p514--2024.pdf",
    "i8992--2024.pdf": "https://www.irs.gov/pub/irs-prior/i8992--2024.pdf",
    "i8993--2024.pdf": "https://www.irs.gov/pub/irs-prior/i8993--2024.pdf",
    # The December 2023 instructions explicitly use the December 2022 form.
    # No 2024 revision exists; inventing a tax-year suffix gives HTTP 404.
    "i1118--2023.pdf": "https://www.irs.gov/pub/irs-prior/i1118--2023.pdf",
    "f1118--2022.pdf": "https://www.irs.gov/pub/irs-prior/f1118--2022.pdf",
    "treasury_wp104.pdf": "https://home.treasury.gov/system/files/131/wp-104.pdf",
    "smith_capitalists.pdf": "https://eml.berkeley.edu/~yagan/Capitalists.pdf",
    "ca_pte.html": "https://www.ftb.ca.gov/file/business/credits/pass-through-entity-elective-tax/index.html",
    "ca_3804_2024.pdf": "https://www.ftb.ca.gov/forms/2024/2024-3804-instructions.pdf",
    "f1120--2024.pdf": "https://www.irs.gov/pub/irs-prior/f1120--2024.pdf",
    "irs_notice2020_75.pdf": "https://www.irs.gov/pub/irs-drop/n-20-75.pdf",
    "fed_h15_annual_10y.html": "https://www.federalreserve.gov/datadownload/Preview.aspx?pi=400&preview=H15%2FH15%2FRIFLGFCY10_N.A&rel=H15",
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def ensure_sources(acquire: bool = False) -> dict:
    pins_path = INPUTS / "owner_source_pins.json"
    pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    if not pins and not acquire:
        raise RuntimeError("[BLOCKED] missing owner_source_pins.json")
    CACHE.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        path = CACHE / name
        if not path.exists() and acquire:
            cached_bytes = sum(p.stat().st_size for p in HERE.glob("_cache/**/*") if p.is_file())
            if cached_bytes >= 10_000_000_000:
                raise RuntimeError("[BLOCKED] lane cache exceeds 10 GB")
            if shutil.disk_usage(HERE).free < 100_000_000:
                raise RuntimeError("[BLOCKED] less than 100 MB disk free")
            old = HERE.parent / "same_year_tax_2026_09_20" / "_cache" / name
            if old.exists():
                shutil.copyfile(old, path)
            else:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=90) as r:
                    content = r.read(30_000_001)
                if len(content) > 30_000_000:
                    raise RuntimeError(f"[BLOCKED] unexpected size {name}")
                path.write_bytes(content)
        if not path.exists():
            raise RuntimeError(f"[BLOCKED] missing primary file {path}; use --acquire")
        b = path.read_bytes()
        if name.endswith(".pdf") and not b.startswith(b"%PDF-"):
            raise RuntimeError(f"[BLOCKED] expected PDF, got other content: {name}")
        if name.endswith(".xls") and not b.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
            raise RuntimeError(f"[BLOCKED] expected OLE workbook: {name}")
        actual = {"url": url, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
        if name in pins and actual != pins[name]:
            raise RuntimeError(f"[BLOCKED] stale source {name}")
        if name not in pins:
            if not acquire:
                raise RuntimeError(f"[BLOCKED] unpinned source {name}")
            pins[name] = actual
            write_json(pins_path, pins)
    return pins


def extract_year(year: int) -> dict:
    import xlrd

    income = xlrd.open_workbook(str(CACHE / f"{year % 100}in14ar.xls")).sheet_by_index(0)
    tax = xlrd.open_workbook(str(CACHE / f"{year % 100}in12ms.xls")).sheet_by_index(0)
    assert "Business or profession" in income.cell_value(2, 31)
    assert income.cell_value(2, 67).strip() == "Partnership"
    assert income.cell_value(2, 71).strip() == "S corporation"
    assert tax.cell_value(3, 9).replace("\n", " ") == "Income tax after credits"
    assert tax.cell_value(3, 11).replace("\n", " ") == "Total income tax"
    assert str(year) in income.cell_value(0, 0) and str(year) in tax.cell_value(0, 0)
    rows = []
    columns = {"schedule_c": (32, 34), "partnership": (68, 70), "s_corporation": (72, 74)}
    # Rows 9..27 are the 19 exhaustive AGI bins; row 28 begins taxable-only returns.
    for r in range(9, 28):
        assert tax.cell_value(r, 2) == income.cell_value(r, 2)
        label = income.cell_value(r, 0).strip()
        assert label.startswith(("No adjusted", "$"))
        agi = float(tax.cell_value(r, 2))
        row = {"agi_bin": label, "excel_row": r + 1, "returns": tax.cell_value(r, 1),
               "agi_thousand_usd": agi,
               "income_tax_after_credits_thousand_usd": tax.cell_value(r, 10),
               "total_income_tax_thousand_usd": tax.cell_value(r, 12),
               "allocated_tax_after_credits_per_agi": tax.cell_value(r, 10) / agi if agi > 0 else None,
               "allocated_total_income_tax_per_agi": tax.cell_value(r, 12) / agi if agi > 0 else None}
        for form, (positive, loss) in columns.items():
            row[form] = {"positive_income_thousand_usd": income.cell_value(r, positive),
                         "loss_thousand_usd": income.cell_value(r, loss)}
        rows.append(row)
    aggregate = {}
    for form, (positive, loss) in columns.items():
        # Independent additive source-total guard; dollar-thousand rounding permits 10 units.
        for c in (positive, loss):
            assert abs(sum(income.cell_value(r, c) for r in range(9, 28)) - income.cell_value(8, c)) <= 10
        totals = {}
        valid = [row for row in rows if row["agi_thousand_usd"] > 0]
        for measure in ("tax_after_credits", "total_income_tax"):
            rate_key = "allocated_" + measure + "_per_agi"
            for weight in ("positive", "signed_net"):
                def amount(row: dict) -> float:
                    x = row[form]
                    return x["positive_income_thousand_usd"] - (x["loss_thousand_usd"] if weight == "signed_net" else 0)
                denom = sum(amount(row) for row in valid)
                totals[f"{weight}_{measure}_rate_positive_agi_only"] = sum(amount(row) * row[rate_key] for row in valid) / denom
        totals["no_agi_positive_income_thousand_usd"] = rows[0][form]["positive_income_thousand_usd"]
        totals["no_agi_loss_thousand_usd"] = rows[0][form]["loss_thousand_usd"]
        totals["all_agi_positive_income_thousand_usd"] = income.cell_value(8, positive)
        totals["all_agi_loss_thousand_usd"] = income.cell_value(8, loss)
        aggregate[form] = totals
    return {"year": year, "money_unit": "thousand USD nominal", "bins": rows, "by_form": aggregate}


def extract_normal_yield() -> dict:
    """Read the Board's annual series directly, avoiding monthly-average rounding."""
    class TableRows(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.rows = []
            self.row = []
            self.cell = None

        def handle_starttag(self, tag: str, attrs: list) -> None:
            if tag == "tr":
                self.row = []
            elif tag in ("td", "th"):
                self.cell = []

        def handle_data(self, data: str) -> None:
            if self.cell is not None:
                self.cell.append(data)

        def handle_endtag(self, tag: str) -> None:
            if tag in ("td", "th") and self.cell is not None:
                self.row.append(" ".join("".join(self.cell).split()))
                self.cell = None
            elif tag == "tr" and self.row:
                self.rows.append(self.row)
                self.row = []

    parser = TableRows()
    parser.feed((CACHE / "fed_h15_annual_10y.html").read_text())
    obs = []
    for year in (2022, 2023, 2024):
        matches = [r for r in parser.rows if f"{year}-12-31" in r]
        if len(matches) != 1:
            raise RuntimeError(f"[BLOCKED] expected one H15 annual observation for {year}, got {len(matches)}")
        row = matches[0]
        assert row[0] == "H15/H15/RIFLGFCY10_N.A", row
        obs.append({"year": year, "reported_percent": float(row[-1]), "rate": float(row[-1]) / 100,
                    "source_cells": row})
    return {"series": "H15/H15/RIFLGFCY10_N.A", "source": SOURCES["fed_h15_annual_10y.html"],
            "description": "Market yield on US Treasury securities at10-year constant maturity, quoted on investment basis",
            "unit": "percent per year", "frequency": "annual", "observations": obs,
            "high_end_rule": "For S/P only, normal taxable-income proxy=min(max(capital_profit,0), r*max(book_net_equity,0)); exclude ScheduleC if net equity unavailable",
            "rule_status": "conditional tax-book proxy; observed nominal Treasury yield is not an identified normal taxable-profit share",
            "timing": "Use2022 yield with TY2022 income/assets;2024 yield alongside frozen2022 inputs is a sensitivity, not a matched2024 measurement",
            "limits": ["booknetequity differs from market-value reproducible capital", "yearend assets versus annual profit timing", "depreciation and expensing differ between tax and economics", "risk and intangibles excluded by nominal riskfree convention", "equity basis avoids charging debt normal return twice but bookequity can mismeasure true equity"]}


def direct_replacement_loss(source_income: float, us_rate: float, domestic_share: float,
                            foreign_credit_fraction: float, foreign_income_ratio: float) -> float:
    """Conditional US loss, domestic identical taxable income/rate; foreign ratio explicit.

    FTC fraction is the share of tentative US tax on foreign replacement extinguished,
    not a foreign tax rate. For unchanged foreign pre-tax income pass ratio=1. This
    convention does not generally preserve owners' worldwide after-tax income.
    Signed income preserves an explicit proportional tax-shield arm on losses;
    this is not a claim that loss carryovers are usable on a complete return.
    """
    for x in (us_rate, domestic_share, foreign_credit_fraction):
        if not 0 <= x <= 1:
            raise ValueError("rate/share outside [0,1]")
    if foreign_income_ratio < 0:
        raise ValueError("negative income ratio")
    return source_income * us_rate * (1 - domestic_share) * (1 - foreign_income_ratio * (1 - foreign_credit_fraction))


def direct_equal_after_tax_loss(source_income: float, us_rate: float, domestic_share: float,
                                foreign_tax_rate: float) -> float:
    """Equal worldwide after-tax return; same US rate, full available direct FTC.

    Simple proportional-tax arm: taxes on an identical base, no deductions, all FTC
    usable up to tentative US tax, no treaty/FEIE/SALT/NIIT/carryovers or source shifts.
    """
    if not 0 <= foreign_tax_rate < 1 or not 0 < us_rate < 1:
        raise ValueError("requires foreign rate in [0,1), US rate in (0,1)")
    combined = max(us_rate, foreign_tax_rate)
    ratio = (1 - us_rate) / (1 - combined)
    credit_fraction = min(1.0, foreign_tax_rate / us_rate)
    return direct_replacement_loss(source_income, us_rate, domestic_share, credit_fraction, ratio)


def gilti_current_us_tax(tested_income: float, gilti_inclusion: float,
                         tested_foreign_taxes: float, *, section250_share: float = 0.5,
                         corporate_rate: float = 0.21, credit_share: float = 0.8,
                         additional_ftc_limit: float | None = None) -> dict:
    """Illustrative 2024 corporation/962 current inclusion tax, not a full return.

    GILTI inclusion must come from Form8992 (net tested income less net DTIR);
    tested income is the sum of positive CFC tested incomes, after foreign tax,
    from Form1118 SchD I col5. Include tests/losses/QBAI before calling. SchD II
    col3/full gross-up and col4/80% credit are deliberately separate.
    """
    if min(tested_income, gilti_inclusion, tested_foreign_taxes) < 0:
        raise ValueError("negative input")
    if gilti_inclusion > tested_income:
        raise ValueError("GILTI inclusion exceeds positive tested income")
    if any(not 0 <= x <= 1 for x in (section250_share, corporate_rate, credit_share)):
        raise ValueError("rate/share outside [0,1]")
    if additional_ftc_limit is not None and additional_ftc_limit < 0:
        raise ValueError("negative FTC limit")
    inclusion_percentage = gilti_inclusion / tested_income if tested_income else 0.0
    gross_up = tested_foreign_taxes * inclusion_percentage
    tentative = corporate_rate * (1 - section250_share) * (gilti_inclusion + gross_up)
    available_credit = credit_share * gross_up
    allowed_credit = min(available_credit, tentative,
                         additional_ftc_limit if additional_ftc_limit is not None else tentative)
    return {"inclusion_percentage": inclusion_percentage, "section78_gross_up": gross_up,
            "tentative_us_tax": tentative, "available_credit": available_credit,
            "allowed_credit": allowed_credit, "current_us_residual": tentative - allowed_credit}


def build(acquire: bool = False) -> dict:
    ensure_sources(acquire)
    result = {"schema_version": 1,
              "estimand": "Income-source-weighted all-return AGI-bin tax/AGI allocation; not linked-owner source tax or marginal rate",
              "default_central_rate": None,
              "status": "conditional proxy arms only",
              "no_agi_rule": "Exclude nonpositive-AGI bin from both weighted numerator and denominator; disclose its income and losses separately; no fabricated zero tax rate",
              "loss_rule": "Positive-income weights and signed-net weights are separate arms; signed-net loss offsets assume same allocated rate within AGI bin",
              "exclusions": ["self-employment tax", "state taxes", "owner labor/capital split", "pass-through-to-nonindividual-owner adjustment", "industry-specific owner tax rates"],
              "years": [extract_year(2022), extract_year(2023)]}
    write_json(INPUTS / "owner_agi_rates.json", result)
    write_json(INPUTS / "owner_normal_yield.json", extract_normal_yield())
    # Independently sourced historical source-income removal tax, not a 2024 update.
    write_json(INPUTS / "owner_historical_rates.json", {
        "source": SOURCES["treasury_wp104.pdf"], "source_year": 2011,
        "locator": "printed p4 / PDF p5; Figures 7-9 and sections3-4",
        "estimand": "Federal tax change when removing sector income holding other income fixed; includes owner-type tracing/assumptions",
        "rates": {"partnership": 0.159, "s_corporation": 0.249, "schedule_c": 0.136},
        "status": "historical sensitivity only; predates TCJA/199A; partnership base includes preferred income and nonindividual owners",
        "not_comparable_without_adjustment": "Industry operating profit after owner labor differs from the paper's all income base"})
    write_json(INPUTS / "owner_replacement_bridge.json", {
        "law_year": 2024, "central_replacement_domestic_share": None,
        "central_foreign_credit_fraction": None, "central_normal_return_share": None,
        "domestic_share_arms": [0, 1], "foreign_credit_fraction_arms": [0, 1],
        "normal_return_share_of_capital_arms": [0, 1],
        "arms_status": "structural endpoints; no probability weights or identified central split",
        "source_tax_loss_positive_lowers_case_cost": True,
        "direct_formula": "I*tau*(1-d)*(1-q*(1-c)); d domestic share, c fraction of foreign tentative US tax offset, q foreign pre-tax replacement/source income",
        "direct_q1_status": "same pre-tax income arm; not generally equal worldwide after-tax return",
        "equal_after_tax_formula": "q=(1-tau)/(1-max(tau,f)); c=min(1,f/tau), with foreign tax rate f; proportional identical-base full-available-FTC arm",
        "domestic_identical_tax_cancellation": 0,
        "gilti_2024": {"section250_deduction_share": 0.5, "corporate_rate": 0.21,
                       "section960d_credit_share": 0.8,
                       "formula": "a=G/T; H=a*F; U=.21*(1-.5)*(G+H); credit=min(.8*H,U,applicable904limit); residual=U-credit",
                       "sources": [SOURCES["i8992--2024.pdf"], SOURCES["i8993--2024.pdf"], SOURCES["i1118--2023.pdf"], SOURCES["f1118--2022.pdf"], SOURCES["f1120--2024.pdf"]],
                       "inputs": "T sum positive pro-rata tested incomes after foreign tax; G actual8992 inclusion after QBAI/tested losses/interest; F pro-rata tested foreign taxes",
                       "warning": "Only current inclusion tax for C corporation/962 electing individual; exclude distribution/residence taxes from automatic current correction; no measured CFC routing or QBAI values"},
        "state": {"national_source_rate": None, "zero_additional_state_arm": 0,
                  "zero_status": "state correction withheld because unidentified, not measured zero liability",
                  "ca_elective_pte_rate": 0.093, "ca_status": "2024 legal example only; not a national upper bound or additive new tax",
                  "sources": [SOURCES["ca_3804_2024.pdf"], SOURCES["irs_notice2020_75.pdf"]]},
        "human_capital": {"source": SOURCES["smith_capitalists.pdf"], "labor_calibration": 0.75,
                          "six_estimate_average": 0.768, "locator": "TableIV; discussion printed pp46-47 / PDFpp46-47",
                          "status": "top-owner S corporation/partnership historical labor arm; not a normal-return fraction or ScheduleC estimate"}})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquire", action="store_true")
    args = parser.parse_args()
    start = time.perf_counter()
    result = build(args.acquire)
    for year in result["years"]:
        print(year["year"], {k: v["positive_tax_after_credits_rate_positive_agi_only"] for k, v in year["by_form"].items()})
    print(json.dumps({"elapsed_seconds": time.perf_counter() - start,
                      "ru_maxrss_platform_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
