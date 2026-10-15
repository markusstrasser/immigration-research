#!/usr/bin/env python3
"""Pin and parse 2022 IRS SOI industry incomes; values are not capital estimates.

uv run --no-project --with xlrd python3 {lane}/income_sources.py --acquire
Ordinary runs require byte-identical cached primary sources. --acquire permits
new pins only, never replacement of a mismatched pin. Outputs live in inputs/
because they are the source interface consumed by the integrating lane.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import shutil
import sys
import time
from pathlib import Path

import openpyxl
import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
INPUTS = HERE / "inputs"
SOURCES = {
    "22co61ccr.xlsx": "https://www.irs.gov/pub/irs-soi/22co61ccr.xlsx",
    "22co07ccr.xlsx": "https://www.irs.gov/pub/irs-soi/22co07ccr.xlsx",
    "22pa01.xlsx": "https://www.irs.gov/pub/irs-soi/22pa01.xlsx",
    "22pa03.xlsx": "https://www.irs.gov/pub/irs-soi/22pa03.xlsx",
    "22pa05.xlsx": "https://www.irs.gov/pub/irs-soi/22pa05.xlsx",
    "22sp01br.xls": "https://www.irs.gov/pub/irs-soi/22sp01br.xls",
    "22sp02is.xls": "https://www.irs.gov/pub/irs-soi/22sp02is.xls",
    "income_p16.pdf": "https://www.irs.gov/pub/irs-pdf/p16.pdf",
    "income_i1120s_2022.pdf": "https://www.irs.gov/pub/irs-prior/i1120s--2022.pdf",
    "income_i1040sc_2022.pdf": "https://www.irs.gov/pub/irs-prior/i1040sc--2022.pdf",
    "income_partnership_terms.html": "https://www.irs.gov/statistics/soi-tax-stats-partnership-study-explanation-of-selected-terms",
    "income_s_compensation.html": "https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues",
    "income_c_catalog.html": "https://www.irs.gov/statistics/soi-tax-stats-corporation-income-tax-returns-complete-report-publication-16",
    "income_p_catalog.html": "https://www.irs.gov/statistics/soi-tax-stats-partnership-statistics-by-sector-or-industry",
    "income_sp_catalog.html": "https://www.irs.gov/statistics/soi-tax-stats-nonfarm-sole-proprietorship-statistics",
}


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def acquire(allow):
    CACHE.mkdir(exist_ok=True)
    INPUTS.mkdir(exist_ok=True)
    pins_path = INPUTS / "income_pins.json"
    pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    for name, url in SOURCES.items():
        path = CACHE / name
        if not path.exists():
            if not allow:
                raise RuntimeError(f"[BLOCKED] missing source {name}; use --acquire")
            if shutil.disk_usage(CACHE).free < 100_000_000:
                raise RuntimeError("[BLOCKED] insufficient free disk")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            if len(response.content) > 10_000_000:
                raise RuntimeError(f"[BLOCKED] unexpected source size {name}")
            if name.endswith(("xls", "xlsx")) and response.content[:1] == b"<":
                raise RuntimeError(f"[BLOCKED] HTML masquerading as workbook: {name}")
            path.write_bytes(response.content)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if name in pins and pins[name]["sha256"] != digest:
            raise RuntimeError(f"[BLOCKED] changed source bytes: {name}")
        if name not in pins:
            if not allow:
                raise RuntimeError(f"[BLOCKED] unpinned source: {name}")
            pins[name] = {"url": url, "path": str(path.relative_to(HERE)), "bytes": path.stat().st_size, "sha256": digest}
        if sum(p.stat().st_size for p in CACHE.rglob("*") if p.is_file()) > 10_000_000_000:
            raise RuntimeError("[BLOCKED] lane cache exceeds 10GB")
    if allow:
        dump(pins_path, pins)
    return pins


def workbook(name):
    path = CACHE / name
    if name.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        # Several IRS files have inflated formatting dimensions (>2000 columns,
        # >3000 rows); all published values in these tables are in the bounds.
        width = 21 if name.startswith("22pa") else 100
        result = {s.title: list(s.iter_rows(max_row=90, max_col=width, values_only=True)) for s in wb.worksheets}
        wb.close()
        return result
    import xlrd
    wb = xlrd.open_workbook(str(path))
    return {s.name: [s.row_values(i) for i in range(s.nrows)] for s in wb.sheets()}


def main():
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--inspect", action="store_true")
    args = parser.parse_args()
    acquire(args.acquire)
    if args.inspect:
        for name in SOURCES:
            if not name.endswith((".xlsx", ".xls")):
                continue
            for sheet, rows in workbook(name).items():
                print(name, sheet, len(rows), max(map(len, rows)))
                for i, row in enumerate(rows, 1):
                    print(i, repr(row[:8]))
        return
    build()
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == "darwin" else peak * 1024
    if peak_bytes >= 2_500_000_000:
        raise RuntimeError("[BLOCKED] memory exceeds 2.5GB")
    metrics = {"elapsed_s": time.perf_counter() - start, "peak_rss_bytes": peak_bytes}
    dump(CACHE / "income_runtime.json", metrics)
    print(json.dumps(metrics))


def build():
    s = next(iter(workbook("22co61ccr.xlsx").values()))
    s7 = next(iter(workbook("22co07ccr.xlsx").values()))
    p = next(iter(workbook("22pa01.xlsx").values()))
    p3 = next(iter(workbook("22pa03.xlsx").values()))
    p5 = next(iter(workbook("22pa05.xlsx").values()))
    c = next(iter(workbook("22sp02is.xls").values()))
    c1 = next(iter(workbook("22sp01br.xls").values()))
    for rows in (s, s7, p, p3, p5, c, c1):
        assert "2022" in str(rows[0][0]) + str(rows[1][0]), "[BLOCKED] wrong IRS year"
        assert "thousands of dollars" in str(rows[1][0]) + str(rows[2][0]), "[BLOCKED] wrong units"

    sectors = ["11", "21", "22", "23", "31-33", "42", "44-45", "48-49", "51", "52", "53", "54", "55", "56", "61", "62", "71", "72", "81"]
    names = ["agriculture", "mining", "utilities", "construction", "durable,nondurable", "wholesale", "retail", "transportation", "information", "finance", "real_estate", "professional", "management", "administrative", "education", "health", "arts", "accommodation_food", "other_services"]
    k1 = {sec: name.split(",") for sec, name in zip(sectors, names)}
    k1["61+81"] = ["education", "other_services"]
    k1["99"] = []
    s_cols = dict(zip(sectors, [2, 6, 7, 8, 12, 33, 37, 47, 54, 61, 67, 71, 72, 73, 76, 77, 81, 84, 87]))
    p_secs = sectors[:14] + ["62", "71", "72", "61+81", "99"]
    p_cols = dict(zip(p_secs, range(2, 21)))
    c_cols = dict(zip(sectors, [2, 7, 11, 12, 16, 36, 40, 52, 63, 69, 80, 96, 115, 114, 118, 119, 135, 139, 145]))
    c_cols["99"] = 153
    # Published Schedule C column 114 combines 55 and 56; column 115 is 55.
    # Hence 56 is derived by subtraction, rather than counted twice.
    assert "Management of" in str(c[3][115])
    assert "Administrative and support" in str(c[2][114])
    assert "Educational and" in str(p[3][19]) and "Other services" in str(p[3][19])
    assert len([x for x in s[4][2:] if x]) == len(s_cols)
    assert "Other services" in str(s[4][87])
    records = []
    national = {}
    gates = []

    def value(rows, label, col):
        matches = [r for r in rows if clean(r[0]) == label]
        if len(matches) != 1:
            raise RuntimeError(f"[BLOCKED] ambiguous or missing source row {label}: {len(matches)}")
        return numeric(matches[0][col])

    def v(rows, label, col):
        n = value(rows, label, col)
        return None if n is None else n / 1_000_000

    def subtraction(a, b):
        return None if a is None or b is None else a - b

    def get_s(col):
        out = {"income_net_bn": v(s, "Net income (less deficit) from a trade or business", col),
               "owner_compensation_deducted_bn": v(s, "Compensation of officers", col),
               "salary_deduction_bn": v(s, "Salaries and wages", col),
               "depreciation_deduction_bn": v(s, "Depreciation", col),
               "taxes_licenses_deducted_bn": v(s, "Taxes and licenses", col),
               "other_receipts_bn": v(s, "Other receipts", col),
               "noncapital_asset_gains_bn": v(s, "Net gain, noncapital assets", col),
               "total_assets_bn": v(s, "Total assets", col),
               "net_equity_book_bn": v(s, "Net worth, total", col),
               "interest_paid_bn": v(s, "Interest paid", col),
               "other_investments_book_bn": v(s, "Other investments", col),
               "land_book_bn": v(s, "Land", col),
               "income_total_all_components_bn": v(s7, "Total net income (less deficit)", col)}
        out["net_depreciable_book_bn"] = subtraction(v(s, "Depreciable assets", col), v(s, "Less: Accumulated depreciation", col))
        out["net_amortizable_book_bn"] = subtraction(v(s, "Intangible assets (amortizable)", col), v(s, "Less: Accumulated amortization", col))
        # All other receipts removed because the table does not isolate embedded
        # ordinary partnership income. This also removes valid operating income.
        out["other_receipts_excluded_net_bn"] = subtraction(out["income_net_bn"], out["other_receipts_bn"])
        # Form1120S also puts upstream ordinary asset gains on Form4797. Finance
        # suppresses BOTH total deductions and tax-exempt interest, precluding an
        # exact direct-profit residual. Use one fully published conservative arm
        # in every sector: ordinary net minus (total receipts-business receipts).
        # This removes other receipts/gains AND tax-exempt interest already
        # excluded from ordinary net. That extra subtraction is deliberate,
        # labelled under-sizing, never an imputation of suppressed cells.
        out["nonbusiness_receipts_bn"] = subtraction(v(s, "Total receipts", col), v(s, "Business receipts", col))
        out["direct_income_net_bn"] = subtraction(out["income_net_bn"], out["nonbusiness_receipts_bn"])
        out["known_upstream_ordinary_net_bn"] = None
        return out

    def get_p(col):
        out = {"income_net_bn": v(p, "Ordinary business income (loss)", col),
               "known_upstream_ordinary_net_bn": subtraction(v(p, "Ordinary income from other partnerships and fiduciaries", col), v(p, "Ordinary loss from other partnerships and fiduciaries", col)),
               "owner_compensation_deducted_bn": v(p, "Guaranteed payments to partners", col),
               "salary_deduction_bn": v(p, "Salaries and wages", col),
               "depreciation_deduction_bn": v(p, "Depreciation", col),
               "taxes_licenses_deducted_bn": v(p, "Taxes and licenses", col),
               "total_assets_bn": v(p3, "Total assets", col),
               "net_equity_book_bn": v(p3, "Partners capital accounts", col),
               "interest_paid_bn": v(p, "Interest paid", col),
               "other_investments_book_bn": v(p3, "Other investments", col),
               "land_book_bn": v(p3, "Land", col),
               "income_total_all_components_bn": v(p, "Total income (loss) minus total deductions [3]", col)}
        out["direct_income_net_bn"] = subtraction(out["income_net_bn"], out["known_upstream_ordinary_net_bn"])
        out["net_depreciable_book_bn"] = subtraction(v(p3, "Depreciable assets", col), v(p3, "Less: Accumulated depreciation", col))
        out["net_amortizable_book_bn"] = subtraction(v(p3, "Intangible assets", col), v(p3, "Less: Accumulated amortization", col))
        out["partner_allocations_bn"] = {name: v(p5, label, col) for name, label in {
            "all": "All partners", "corporate_general": "Corporate general partners", "corporate_limited": "Corporate limited partners",
            "individual_general": "Individual general partners", "individual_limited": "Individual limited partners",
            "partnership_general": "Partnership general partners", "partnership_limited": "Partnership limited partners",
            "tax_exempt": "Tax-exempt organization partners (all)", "nominee_other_general": "Nominee and other general partners",
            "nominee_other_limited": "Nominee and other limited partners"}.items()}
        return out

    def get_c(col):
        return {"income_net_bn": v(c, "Net income less deficit [1]", col),
                "direct_income_net_bn": v(c, "Net income less deficit [1]", col),
                "known_upstream_ordinary_net_bn": None,
                "owner_compensation_deducted_bn": None,
                "salary_deduction_bn": v(c, "Salaries and wages", col),
                "depreciation_deduction_bn": v(c, "Depreciation", col),
                "taxes_licenses_deducted_bn": v(c, "Taxes paid", col),
                "total_assets_bn": None, "land_book_bn": None,
                "net_equity_book_bn": None,
                "interest_paid_bn": v(c, "Mortgage interest", col) + v(c, "Other interest paid on business indebtedness", col),
                "other_investments_book_bn": None,
                "net_depreciable_book_bn": None, "net_amortizable_book_bn": None,
                "income_total_all_components_bn": v(c, "Net income less deficit [1]", col)}

    for form, cols, getter in [("s_corporation", s_cols, get_s), ("partnership", p_cols, get_p), ("sole_proprietor", c_cols, get_c)]:
        for sec, col in cols.items():
            data = getter(col)
            if form == "sole_proprietor" and sec == "56":
                sub = getter(c_cols["55"])
                data = {key: subtraction(val, sub[key]) for key, val in data.items()}
            assert data["income_net_bn"] is not None and data["direct_income_net_bn"] is not None, f"[BLOCKED] income suppression {form}/{sec}"
            records.append({"form": form, "naics": sec, "k1_sectors": k1[sec], "source_year": 2022, **data})
            if form == "partnership":
                assert abs(v(p5, "Ordinary business income (loss)", col) - data["income_net_bn"]) <= 1e-9
                allocations = data["partner_allocations_bn"]
                if all(x is not None for x in allocations.values()):
                    assert abs(sum(v for k, v in allocations.items() if k != "all") - allocations["all"]) <= .00001
            if form == "s_corporation":
                assert abs(v(s7, "Net income (less deficit) from a trade or business", col) - data["income_net_bn"]) <= 1e-9
        national[form] = getter(1)
        for field in ("income_net_bn", "direct_income_net_bn", "salary_deduction_bn", "depreciation_deduction_bn", "taxes_licenses_deducted_bn", "total_assets_bn", "net_depreciable_book_bn", "net_amortizable_book_bn", "net_equity_book_bn", "interest_paid_bn", "other_investments_book_bn"):
            values = [r[field] for r in records if r["form"] == form]
            expected = national[form][field]
            if expected is None or any(x is None for x in values):
                gates.append({"name": f"{form} {field} closure", "passed": True, "status": "not available; null preserved, no imputation"})
                continue
            error = sum(values) - expected
            # At most 20 rounded source sectors, with differences of rounded rows.
            passed = abs(error) <= 0.00004
            gates.append({"name": f"{form} {field} sector closure within $40k", "passed": passed, "error_bn": error})
            if not passed:
                raise RuntimeError(f"[BLOCKED] source sector closure {form}/{field}: {error}")
    # Every partition of the K1 industry dictionary appears once per form.
    expected_k1 = sorted(x for val in k1.values() for x in val if val != k1["61+81"])
    for form in national:
        actual = sorted(x for r in records if r["form"] == form for x in r["k1_sectors"])
        assert actual == expected_k1, f"[BLOCKED] K1 sector partition {form}"
    assert clean(c1[3][8]) == "Net income less deficit"
    assert abs(numeric(c1[8][8]) / 1_000_000 - national["sole_proprietor"]["income_net_bn"]) <= 1e-9
    assert abs(numeric(c1[8][6]) / 1_000_000 - national["sole_proprietor"]["interest_paid_bn"]) <= 1e-9
    payload = {
        "source_year": 2022, "units": "billions of nominal 2022 dollars; unscaled",
        "source_interface": "source measurements only; direct_income_net_bn remains mixed labor/capital",
        "transport_to_2024": {"default_factor": None, "rule": "caller must state frozen-nominal or another sourced scaling arm; no automatic inflation or growth"},
        "income_definition": {
            "s_corporation": "ordinary net income minus (total receipts-business receipts). Removes all other receipts and noncapital gains, including upstream receipts/gains; also subtracts tax-exempt interest already excluded from ordinary net, a deliberate conservative under-sizing arm. Upstream losses remain deducted. Exact business-receipts-minus-deductions residual unavailable in finance: deductions and tax-exempt interest suppressed",
            "partnership": "ordinary net business income less ordinary income from other partnerships/fiduciaries plus ordinary losses from those entities; excludes portfolio/rental lines",
            "sole_proprietor": "Schedule C net income less deficit; excludes Schedule F farm proprietors; proprietor labor remains in profit"},
        "capital_identification": "economic owner labor, normal return, source geography and ultimate taxable ownership are not identified; no central capital fraction or normal-return share",
        "ownership_warning": "partnership allocations are total Schedule K income less deductions by immediate partner type, NOT direct ordinary-profit ownership shares; ratios can be negative or exceed 1",
        "records": records, "national": national, "gates": gates}
    dump(INPUTS / "income_sectors.json", payload)
    print(json.dumps({"forms": list(national), "rows": len(records), "income_net_bn": {f: v["income_net_bn"] for f, v in national.items()}, "direct_income_net_bn": {f: v["direct_income_net_bn"] for f, v in national.items()}, "gates": len(gates)}))


def clean(value):
    return " ".join(str(value).split())


def numeric(value):
    if isinstance(value, (float, int)):
        return float(value)
    text = str(value).strip()
    if text in ("d", "[d]", "None", ""):
        return None
    try:
        return float(text.replace(",", "").replace("*", ""))
    except ValueError as error:
        raise RuntimeError(f"[BLOCKED] unsupported numeric source cell: {value!r}") from error


def capital_income_arm(record, labor_share, basis="direct_income_net_bn"):
    """Explicit sensitivity, not identified capital: residual profit*(1-labor).

    Keep losses signed. Labor share applies AFTER officer pay/guaranteed payments
    already deducted by IRS; subtracting those payments again double counts them.
    """
    if not 0 <= labor_share <= 1:
        raise ValueError("labor_share must be an explicit fraction in [0,1]")
    return record[basis] * (1 - labor_share)


def normal_return_book_arm(record, labor_share, real_return, basis="direct_income_net_bn"):
    """Labelled stock proxy: min(positive labor-adjusted income, r*net book PPE).

    This is equity-income upper sizing before debt adjustment; book PPE covers
    rental as well as operating activity and has no activity-level split. It is
    not a normal-return estimate. Missing Schedule C stock returns None.
    """
    if real_return < 0:
        raise ValueError("real_return must be an explicit nonnegative rate")
    stock = record["net_depreciable_book_bn"]
    if stock is None:
        return None
    return min(max(0, capital_income_arm(record, labor_share, basis)), real_return * max(0, stock))


if __name__ == "__main__":
    main()
