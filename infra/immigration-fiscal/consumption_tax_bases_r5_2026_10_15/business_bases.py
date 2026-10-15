"""Primary business-purchase evidence and explicitly conditional customs bridge.

No nationwide 2024 business share is silently filled from COST/EY, an old state
study, total sales by selling industry, or BEA's combined tax-on-products column.
The customs arm distributes duties proportionally across positive domestic uses
within each summary commodity. This is a modeling assumption, not observed tax
liability by purchaser. Investment/government final demand keeps its own bucket
because its purchaser-industry response is not identified by these tables.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import zipfile

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILE = HERE / "inputs/business_sources.json"
STATES = "01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56".split()
SUT_TO_CELL = {"525": "523", "GFGD": "GOVF", "GFGN": "GOVF", "GFE": "GOVF", "GSLG": "GOVSL", "GSLE": "GOVSL"}
MINING = {"211", "212", "213"}
FINAL_NAMES = {"F010": "household_pce", "F02S": "private_investment_structures", "F02E": "private_investment_equipment", "F02N": "private_investment_intellectual_property", "F02R": "private_residential_investment", "F06C": "defense_consumption", "F06S": "defense_investment_structures", "F06E": "defense_investment_equipment", "F06N": "defense_investment_intellectual_property", "F07C": "federal_nondefense_consumption", "F07S": "federal_nondefense_investment_structures", "F07E": "federal_nondefense_investment_equipment", "F07N": "federal_nondefense_investment_intellectual_property", "F10C": "state_local_consumption", "F10S": "state_local_investment_structures", "F10E": "state_local_investment_equipment", "F10N": "state_local_investment_intellectual_property"}
TX_LABELS = {"agriculture": "Agriculture", "mining": "Mining", "utilities_transportation": "Utilities & Transportation", "construction": "Construction", "manufacturing": "Manufacturing", "trade": "Retail & Wholesale Trade", "information": "Information", "finance_insurance_real_estate": "Finance, Insurance & Real Estate", "other_services": "Other Services"}


def require(ok, message):
    if not ok:
        raise ValueError(f"[BLOCKED] business bases: {message}")


def verify_sources(data):
    for sid, source in data["sources"].items():
        path = ROOT / source["repo_path"] if "repo_path" in source else HERE / source["path"]
        require(path.is_file(), f"missing source {sid}: {path}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], f"source hash changed: {sid}")
    # Check transcribed tabular values against the pinned original PDFs. Cached
    # pdftotext sidecars are not authoritative and cannot bypass this check.
    text = {}
    for sid in ("tx2025", "tx2023", "mn2026", "mn2024"):
        path = HERE / data["sources"][sid]["path"]
        text[sid] = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, check=True).stdout.decode()
    verify_estimate_rows(data["state_source_estimates"], text)


def verify_estimate_rows(estimates, text):
    """Match each principal value on its own table row, not elsewhere in a PDF."""
    for row in estimates:
        body = text[row["source_id"]]
        if row.get("industry_million"):
            block = body.split("Initial Distribution and Final Incidence of Total Limited Sales and Use Tax Revenue", 1)[1]
            block = block.split("Final Incidence of Tax - By Household", 1)[0]
            for sector, value in row["industry_million"].items():
                match = re.search(r"^\s*" + re.escape(TX_LABELS[sector]) + r"\s+\$?([\d,.]+)", block, re.M)
                require(match is not None and float(match[1].replace(",", "")) == value, f"TX industry row mismatch: {sector}")
            subtotal = re.search(r"Subtotal\s+\$?([\d,.]+)\s+([\d.]+)%", block)
            require(subtotal is not None and float(subtotal[1].replace(",", "")) == row["business_million"]
                    and float(subtotal[2]) == row["published_business_percent"], "TX business subtotal mismatch")
            total = re.search(r"^\s*Total\s+\$?([\d,.]+)\s+100\.0%", block, re.M)
            require(total is not None and float(total[1].replace(",", "")) == row["total_million"], "TX tax denominator mismatch")
            require(abs(sum(row["industry_million"].values()) - row["business_million"]) < 0.25,
                    "TX rounded industry cells do not close to business subtotal")
        else:
            label = r"General sales/use tax" if row["denominator"].startswith("state") else r"Local Sales Taxes\s*7"
            match = re.search(r"^\s*" + label + r"\s+([\d,]+)\s+([\d.]+)%\s+([\d.]+)%\s+([\d.]+)%\s+([\d.]+)%\s+100\.0%", body, re.M)
            require(match is not None and float(match[1].replace(",", "")) == row["total_million"]
                    and float(match[5]) == row["published_business_percent"], f"MN tax row mismatch: {row['denominator']}")


def numeric(value):
    if value is None or value == "...":
        return 0.0
    require(isinstance(value, (int, float)), f"unexpected BEA numeric cell {value!r}")
    return float(value)


def bea_tables(data):
    path = ROOT / data["sources"]["bea2024"]["repo_path"]
    tables = {}
    with zipfile.ZipFile(path) as archive:
        for name in ("Supply_Summary.xlsx", "Use_Summary.xlsx"):
            book = openpyxl.load_workbook(io.BytesIO(archive.read(name)), read_only=True, data_only=True)
            rows = list(book["2024"].values)
            require(rows[1][0] == "(Millions of dollars)" and rows[3][0] == "2024", "BEA year/units mismatch")
            require(rows[0][0].startswith("The Domestic Supply" if name.startswith("Supply") else "The Use"), "BEA table title mismatch")
            headers = rows[5]
            tables[name] = ({str(row[0]): {str(h): numeric(row[j]) for j, h in enumerate(headers) if j >= 2 and h is not None}
                             for row in rows[7:] if row[0] is not None}, headers)
            book.close()
    return tables


def customs_arm(data):
    tables = bea_tables(data)
    supply, _ = tables["Supply_Summary.xlsx"]
    use, headers = tables["Use_Summary.xlsx"]
    industries = list(headers[2:headers.index("T001")])
    purchasers = industries + list(FINAL_NAMES)
    allocated = {code: 0.0 for code in purchasers}
    commodities = []
    total_duty = supply["T017"]["MDTY"]
    total_top = supply["T017"]["TOP"]
    duty_sum = 0.0
    for commodity, vals in supply.items():
        if commodity == "T017":
            continue
        duty = vals["MDTY"]
        require(duty >= 0, f"negative commodity import duties: {commodity}")
        if not duty:
            continue
        require(commodity in use, f"dutiable commodity missing in use: {commodity}")
        u = use[commodity]
        # Exports F040 and changes in inventory F030 do not enter domestic
        # absorption. Positive-use clipping is explicit for negative adjustments.
        demand = {code: max(0.0, u[code]) for code in purchasers}
        denom = sum(demand.values())
        require(denom > 0, f"dutiable commodity has no domestic uses: {commodity}")
        cell = {code: duty * value / denom for code, value in demand.items()}
        for code, value in cell.items():
            allocated[code] += value
        commodities.append({"commodity": commodity, "import_duties_million": duty,
                            "domestic_positive_use_million": denom,
                            "pce_fraction_conditional": demand["F010"] / denom,
                            "clipped_negative_uses_million": sum(-u[c] for c in purchasers if u[c] < 0),
                            "exports_excluded_million": u["F040"], "inventories_excluded_million": u["F030"]})
        duty_sum += duty
    # Published integer-million commodity cells need not sum exactly to their
    # separately rounded total. Normalize to that authoritative total, preserving
    # the national collections passed by the caller, rather than altering it.
    require(abs(duty_sum - total_duty) <= len(commodities) * 0.5, "commodity duties do not close within source rounding")
    require(abs(sum(allocated.values()) - duty_sum) < 1e-7, "customs allocation does not conserve duty sum")
    rows = []
    for code, value in allocated.items():
        kind = ("unkeyed_intermediate" if code == "HS" else "intermediate") if code in industries else ("household" if code == "F010" else "unkeyed_final_demand")
        rows.append({"io_code": code, "key": SUT_TO_CELL.get(code, code), "kind": kind,
                     "name": FINAL_NAMES.get(code, code), "share_of_total_duties": value / duty_sum,
                     "conditional_duties_bn": total_duty / 1000 * value / duty_sum,
                     "production_response": 0.0 if code in MINING else None,
                     "response_status": ("mining zero by parent rule" if code in MINING else
                                         "existing household consumption key" if code == "F010" else
                                         "housing has no item6 wage purchaser key; response unidentified" if code == "HS" else
                                         "caller supplies item6 purchaser response" if kind == "intermediate" else
                                         "final-demand purchaser industry unidentified")})
    pce = allocated["F010"] / duty_sum
    inter = sum(allocated[c] for c in industries) / duty_sum
    return {"identification_status": "CONDITIONAL_PROPORTIONAL_ARM_ONLY", "central_business_share": None,
            "source_id": "bea2024", "measured_total_import_duties_bn": total_duty / 1000,
            "sum_rounded_commodity_duties_bn": duty_sum / 1000,
            "measured_all_tax_on_products_bn": total_top / 1000,
            "conditional_household_share": pce, "conditional_intermediate_share": inter,
            "conditional_nonhousehold_share": 1 - pce,
            "conditional_unkeyed_final_demand_share": 1 - pce - inter,
            "assumptions": ["uniform duty intensity across positive domestic uses within each BEA summary commodity",
                            "exclude direct exports and changes in inventories from duty allocation; inputs used by exporters remain in intermediate purchases",
                            "PCE is household; investment and government final demand are separate nonhousehold buckets",
                            "source total rescales summed rounded commodity cells; caller keeps the case national customs total fixed"],
            "conditional_unkeyed_intermediate_share": allocated["HS"] / duty_sum,
            "missing": ["actual tariff rates/product composition within commodity by purchaser", "purchaser industry and state for final investment/government uses", "HS housing intermediate purchaser response: no item6 wage key", "state mix for national industry intermediate customs purchases"],
            "purchaser_weights": rows, "commodities": commodities}


def build_bridge(source_file=SOURCE_FILE):
    data = json.loads(Path(source_file).read_text())
    verify_sources(data)
    state_rows = []
    for state in STATES:
        evidence = []
        for original in data["state_source_estimates"]:
            if original["state_fips"] != state:
                continue
            row = dict(original)
            row["business_share"] = (row["business_million"] / row["total_million"]
                                      if row["business_million"] is not None else row["published_business_percent"] / 100)
            if "industry_million" in row:
                # Use the industry cells' own denominator to remove published
                # 0.1m rounding residuals; the state business share uses subtotal.
                denom = sum(row["industry_million"].values())
                row["conditional_business_industry_weights"] = {k: v / denom for k, v in row["industry_million"].items()}
                row["mining_business_fraction"] = row["industry_million"]["mining"] / denom
                row["industry_mapping_status"] = "broad sectors only; within-sector item6 cell mix must be supplied, never inferred from seller industry"
            evidence.append(row)
        state_rows.append({"state_fips": state, "central_2024_business_share": None,
                           "identification_status": "DATED_SOURCE_ESTIMATE_ONLY" if evidence else "NOT_IDENTIFIED",
                           "share_lower": 0.0, "share_upper": 1.0,
                           "bound_status": "logical identification bounds, not confidence interval",
                           "dated_source_estimates": evidence})
    return {"schema_version": 1, "case_year": 2024, "identification_status": "INCOMPLETE_BUSINESS_BRIDGE",
            "state_sales": state_rows,
            "national_taxes": {tax: {"central_business_share": None, "share_lower": 0.0, "share_upper": 1.0,
                                      "identification_status": "NOT_IDENTIFIED"}
                               for tax in ("general_sales_tax", "excise_selective_sales", "customs_duties")},
            "customs_proportional_arm": customs_arm(data),
            "excise_gap": "Supply TOP combines general sales, excise and other product taxes. A tax-category-by-commodity/purchaser crosswalk is missing; TOP must not substitute for excise_selective_sales.",
            "crosscheck_only": data["crosscheck_only"], "sources": data["sources"],
            "methodology_sources": data["methodology_sources"],
            "required_for_central": ["2024 tax-matched state/local collection weights and business shares", "purchaser industry/state mix", "excise-category-specific bridge", "explicit final-demand production response"]}


def require_identified_central(bridge):
    missing = [tax for tax, row in bridge["national_taxes"].items() if row["central_business_share"] is None]
    require(not missing, "central unavailable for " + ", ".join(missing))


def customs_group_share(bridge, household_share, purchaser_responses):
    """Evaluate only the conditional arm, rejecting incomplete response vectors.

    Responses are group-induced output-removal fractions in [0,1], already
    including the caller's lineage/industry/state rule. They are keyed by the
    normalized item6 code or the explicit final-use code. The household share
    remains on its existing consumption key. Mining is held at zero.
    """
    require(0 <= household_share <= 1, "household share outside [0,1]")
    total = 0.0
    missing = []
    for row in bridge["customs_proportional_arm"]["purchaser_weights"]:
        weight = row["share_of_total_duties"]
        if not weight:
            continue
        if row["kind"] == "household":
            response = household_share
        elif row["production_response"] == 0:
            response = 0.0
        elif row["key"] not in purchaser_responses:
            missing.append(row["key"])
            continue
        else:
            response = purchaser_responses[row["key"]]
            require(isinstance(response, (int, float)) and 0 <= response <= 1,
                    f"invalid purchaser response {row['key']}: {response!r}")
        total += weight * response
    require(not missing, "customs purchaser responses missing: " + ", ".join(sorted(set(missing))))
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="write stable JSON; default stdout")
    parser.add_argument("--require-central", action="store_true")
    args = parser.parse_args()
    start = time.perf_counter()
    bridge = build_bridge()
    if args.require_central:
        require_identified_central(bridge)
    text = json.dumps(bridge, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    else:
        print(text, end="")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    mib = rss / (1024 * 1024 if sys.platform == "darwin" else 1024)
    print(f"business bridge elapsed_s={time.perf_counter()-start:.3f} peak_mib={mib:.2f}", file=sys.stderr)


if __name__ == "__main__":
    main()
