"""Pinned primary security inputs; Census credentials never appear in diagnostics."""

import argparse
import csv
import hashlib
import json
import os
import resource
import shutil
import tempfile
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
INPUTS = LANE / "inputs"
DERIVED = LANE / "derived"
INDUSTRIES = ("561611", "561612", "561613", "561621", "561622")
CUSTOMER_CODES = {
    "residential_share": "5045", "business_share": "514",
    "nonprofit_share": "570", "federal_share": "515", "state_local_share": "516",
}
PRODUCT_CODES = {
    "residential": ("7000550000", "7000575000"),
    "nonresidential": ("7007475000", "7007500000"),
}
QUERIES = {
    "ecnclcust": {
        "get": "NAICS2022,NAICS2022_LABEL,TYPOP,TAXSTAT,CLASSCUST,CLASSCUST_LABEL,RCPTOT,RCPTOT_F,RCPTOT_DIST,RCPTOT_DIST_F,CLASSCUST_COV,CLASSCUST_COV_F",
        "for": "us:1", "CLASSCUST": "*", "TAXSTAT": "00",
    },
    "ecnnapcsind": {
        "get": "NAICS2022,NAICS2022_LABEL,TAXSTAT,NAPCS2022,NAPCS2022_LABEL,NAPCSDOL,NAPCSDOL_F,NAPCSDOL_CV,NAPCSDOL_IMP,LINEALL_PCT,LINEALL_PCT_SE",
        "for": "us:1", "NAPCS2022": "*", "TAXSTAT": "00",
    },
}


def census_key():
    value = os.environ.get("CENSUS_API_KEY") or os.environ.get("CENSUS_KEY")
    if value:
        return value
    config = LANE.parent / "acquire" / "config.local.env"
    for line in config.read_text().splitlines():
        key, _, val = line.removeprefix("export ").partition("=")
        if key.strip() in ("CENSUS_API_KEY", "CENSUS_KEY"):
            return val.strip().strip("\"'")
    raise RuntimeError("[BLOCKED] Census key unavailable")


def fetch_json(url, target, query=None):
    """Write only valid JSON; never propagate an exception containing a key URL."""
    request_url = url
    if query is not None:
        request_url += "?" + urllib.parse.urlencode(dict(query, key=census_key()))
    try:
        with urllib.request.urlopen(request_url, timeout=50) as response:
            data = response.read()
            status = response.status
        parsed = json.loads(data)
    except Exception as exc:
        hint = f"; status={status}; bytes={len(data)}" if isinstance(exc, json.JSONDecodeError) else ""
        raise RuntimeError(f"[BLOCKED] Census fetch failed: {target.name} ({type(exc).__name__}){hint}; URL/error redacted") from None
    if query is not None:
        if not isinstance(parsed, list) or len(parsed) < 2 or not isinstance(parsed[0], list):
            raise RuntimeError(f"[BLOCKED] Census table schema invalid: {target.name}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return parsed


def probe():
    for dataset in ("ecnclcust", "ecnnapcsind"):
        variables = fetch_json(
            f"https://api.census.gov/data/2022/{dataset}/variables.json",
            CACHE / f"security_{dataset}_variables.json",
        )["variables"]
        print(dataset, {k: v.get("label") for k, v in variables.items()})


def acquire():
    def run(item):
        dataset, naics = item
        query = dict(QUERIES[dataset], NAICS2022=naics)
        parsed = fetch_json(f"https://api.census.gov/data/2022/{dataset}", CACHE / f"security_{dataset}_{naics}_2022.json", query)
        print(dataset, "rows", len(parsed) - 1, "schema", parsed[0])
    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(run, [(dataset, naics) for dataset in QUERIES for naics in INDUSTRIES]))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin_inputs():
    """Explicit acquisition step; normal computation cannot bless changed bytes."""
    INPUTS.mkdir(parents=True, exist_ok=True)
    sources = []
    for dataset in QUERIES:
        names = [f"security_{dataset}_variables.json"] + [f"security_{dataset}_{naics}_2022.json" for naics in INDUSTRIES]
        for name in names:
            source, target = CACHE / name, INPUTS / name
            json.loads(source.read_text())
            shutil.copyfile(source, target)
            metadata = name.endswith("variables.json")
            record = {"path": str(target.relative_to(LANE)), "sha256": digest(target),
                      "source": f"https://api.census.gov/data/2022/{dataset}" + ("/variables.json" if metadata else "")}
            if not metadata:
                record["query_without_key"] = dict(QUERIES[dataset], NAICS2022=name.split("_")[-2])
            sources.append(record)
    for naics in INDUSTRIES:
        source = CACHE / f"fred_REVEF{naics}ALLEST.csv"
        target = INPUTS / f"security_fred_REVEF{naics}ALLEST.csv"
        shutil.copyfile(source, target)
        sources.append({"path": str(target.relative_to(LANE)), "sha256": digest(target),
                        "source": f"https://fred.stlouisfed.org/graph/?g=&id=REVEF{naics}ALLEST",
                        "publisher": "Census Service Annual Survey, distributed by FRED",
                        "source_series": f"REVEF{naics}ALLEST", "selected_observation": "2022-01-01"})
    manifest = {"schema": "security-inputs-v1", "sources": sources}
    (INPUTS / "security_pins.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def verify_pins():
    path = INPUTS / "security_pins.json"
    if not path.exists():
        raise RuntimeError("[BLOCKED] security input pins missing; run explicit acquisition/pin step")
    manifest = json.loads(path.read_text())
    if manifest.get("schema") != "security-inputs-v1" or len(manifest.get("sources", [])) != 17:
        raise RuntimeError("[BLOCKED] security pin manifest schema/coverage mismatch")
    expected = {f"inputs/security_{dataset}_variables.json" for dataset in QUERIES}
    expected |= {f"inputs/security_{dataset}_{n}_2022.json" for dataset in QUERIES for n in INDUSTRIES}
    expected |= {f"inputs/security_fred_REVEF{n}ALLEST.csv" for n in INDUSTRIES}
    actual = [r["path"] for r in manifest["sources"]]
    if set(actual) != expected or len(set(actual)) != len(actual):
        raise RuntimeError("[BLOCKED] security pin source set mismatch")
    for record in manifest["sources"]:
        source = LANE / record["path"]
        if not source.is_file() or digest(source) != record["sha256"]:
            raise RuntimeError(f"[BLOCKED] missing or stale security source: {record['path']}")
    return manifest


def table_rows(path, naics, required):
    try:
        table = json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise RuntimeError(f"[BLOCKED] not a Census JSON table: {path.name}") from None
    if not isinstance(table, list) or len(table) < 2 or not isinstance(table[0], list):
        raise RuntimeError(f"[BLOCKED] Census JSON table schema invalid: {path.name}")
    header = table[0]
    if not set(required).issubset(header):
        raise RuntimeError(f"[BLOCKED] Census fields missing: {path.name}")
    rows = []
    for values in table[1:]:
        if len(values) != len(header):
            raise RuntimeError(f"[BLOCKED] Census row width invalid: {path.name}")
        row = {}
        for key, value in zip(header, values):
            if key in row and row[key] != value:
                raise RuntimeError(f"[BLOCKED] Census duplicate field disagrees: {path.name}/{key}")
            row[key] = value
        if row["NAICS2022"] != naics or row["TAXSTAT"] != "00" or row["us"] != "1":
            raise RuntimeError(f"[BLOCKED] Census industry/tax/geography mismatch: {path.name}")
        rows.append(row)
    return rows


def number(row, field, *, allow_small=False):
    flag = row.get(field + "_F")
    allowed = (None, "", "s") if allow_small else (None, "")
    if flag not in allowed:
        raise RuntimeError(f"[BLOCKED] unusable Census estimate: {field}, flag={flag}")
    value = float(row[field])
    if not 0 <= value < float("inf"):
        raise RuntimeError(f"[BLOCKED] invalid Census estimate: {field}")
    return value


def sas_revenue(naics):
    with (INPUTS / f"security_fred_REVEF{naics}ALLEST.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    selected = [r for r in rows if r["observation_date"] == "2022-01-01"]
    if len(selected) != 1:
        raise RuntimeError(f"[BLOCKED] missing/duplicate SAS 2022 observation: {naics}")
    value = float(selected[0][f"REVEF{naics}ALLEST"])
    if not 0 < value < float("inf"):
        raise RuntimeError(f"[BLOCKED] invalid SAS revenue: {naics}")
    return value


def load_security_inputs():
    """Return NAICS-keyed inputs. Shares use ALL customer receipts as denominator.

    residential_share is household/individual PAYER, not residential-building share.
    commercial_share includes firms and nonprofits; nonprofit pass-through is an
    assumption. government_share is retained separately for closure and exclusion.
    SAS revenues are retained to isolate the comparator fix from a source revision.
    """
    verify_pins()
    result = {}
    for naics in INDUSTRIES:
        rows = table_rows(INPUTS / f"security_ecnclcust_{naics}_2022.json", naics,
                          ("CLASSCUST", "RCPTOT", "RCPTOT_DIST", "TYPOP", "CLASSCUST_COV_F"))
        by_code = {r["CLASSCUST"]: r for r in rows}
        if len(by_code) != len(rows) or set(by_code) != {"001", *CUSTOMER_CODES.values()}:
            raise RuntimeError(f"[BLOCKED] class-of-customer categories missing/duplicated: {naics}")
        if any(r["TYPOP"] != "00" for r in rows):
            raise RuntimeError(f"[BLOCKED] unexpected type of operation: {naics}")
        total = by_code["001"]
        record = {"naics": naics, "label": total["NAICS2022_LABEL"],
                  "revenue_m_2022": sas_revenue(naics),
                  "ec_revenue_m_2022": number(total, "RCPTOT") / 1000,
                  "customer_coverage_flag": total["CLASSCUST_COV_F"],
                  "customer_coverage_pct": None if total["CLASSCUST_COV_F"] else number(total, "CLASSCUST_COV")}
        for field, code in CUSTOMER_CODES.items():
            record[field] = number(by_code[code], "RCPTOT_DIST") / 100
        share_sum = sum(record[field] for field in CUSTOMER_CODES)
        if abs(share_sum - 1) > 1e-12:
            raise RuntimeError(f"[BLOCKED] rounded customer shares do not close exactly: {naics}")
        record["commercial_share"] = record["business_share"] + record["nonprofit_share"]
        record["government_share"] = record["federal_share"] + record["state_local_share"]
        record["private_share"] = record["residential_share"] + record["commercial_share"]
        record["commercial_nonprofit_pass_through"] = "[ASSUMPTION] nonprofit purchases pass through like business purchases; nonprofit_share also provided separately"
        record["residential_semantics"] = "[SOURCE] household consumers and individuals by payer; individually owned businesses classified as firms"
        record["revenue_split_semantics"] = "[ASSUMPTION] apply 2022 Economic Census customer shares to retained 2022 SAS/FRED revenue total"
        for category in ("residential", "commercial", "government"):
            record[f"{category}_revenue_m_2022"] = record["revenue_m_2022"] * record[f"{category}_share"]
        split = sum(record[f"{c}_revenue_m_2022"] for c in ("residential", "commercial", "government"))
        if abs(split - record["revenue_m_2022"]) / 1000 > 1e-6:
            raise RuntimeError(f"[BLOCKED] security revenue split does not conserve national total: {naics}")
        products = table_rows(INPUTS / f"security_ecnnapcsind_{naics}_2022.json", naics,
                              ("NAPCS2022", "NAPCSDOL", "NAPCSDOL_F", "NAPCSDOL_CV", "LINEALL_PCT"))
        by_product = {r["NAPCS2022"]: r for r in products}
        if len(by_product) != len(products) or "0000000000" not in by_product:
            raise RuntimeError(f"[BLOCKED] missing/duplicate NAPCS total: {naics}")
        product_total = number(by_product["0000000000"], "NAPCSDOL")
        if abs(product_total / 1000 - record["ec_revenue_m_2022"]) > 1e-9:
            raise RuntimeError(f"[BLOCKED] customer and product industry totals disagree: {naics}")
        for category, codes in PRODUCT_CODES.items():
            present = [by_product[c] for c in codes if c in by_product]
            value = sum(number(r, "NAPCSDOL", allow_small=True) for r in present)
            record[f"{category}_product_m_2022"] = value / 1000
            record[f"{category}_product_share"] = value / product_total
            record[f"{category}_product_codes_published"] = [r["NAPCS2022"] for r in present]
        record["product_unclassified_share"] = 1 - record["residential_product_share"] - record["nonresidential_product_share"]
        record["product_semantics"] = "[SOURCE] building security monitoring/install/repair only; unclassified remainder is not assigned a building type; products are not customer classes"
        if record["product_unclassified_share"] < -1e-12:
            raise RuntimeError(f"[BLOCKED] residential/nonresidential products exceed industry total: {naics}")
        result[naics] = record
    return result


def write_outputs():
    data = load_security_inputs()
    DERIVED.mkdir(parents=True, exist_ok=True)
    payload = {"schema": "security-inputs-v1", "year": 2022, "units": "million nominal 2022 USD",
               "industries": data,
               "unidentified_splits": {
                   "inhouse_guards": "[ASSUMPTION REQUIRED] customer table covers contracted services, not guards employed in other industries; business vs household payer split unidentified",
                   "direct_equipment": "[ASSUMPTION REQUIRED] revenue/product table does not identify household versus business direct equipment purchases; total and split remain assumptions",
               }}
    (DERIVED / "security_inputs.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    fields = ["naics", "label", "revenue_m_2022", "ec_revenue_m_2022", *CUSTOMER_CODES,
              "commercial_share", "government_share", "private_share", "residential_revenue_m_2022",
              "commercial_revenue_m_2022", "government_revenue_m_2022", "customer_coverage_flag",
              "residential_product_m_2022", "nonresidential_product_m_2022", "residential_product_share",
              "nonresidential_product_share", "product_unclassified_share"]
    with (DERIVED / "security_inputs.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data.values())
    for dataset in QUERIES:
        combined = []
        for naics in INDUSTRIES:
            path = INPUTS / f"security_{dataset}_{naics}_2022.json"
            combined.extend(table_rows(path, naics, ("NAICS2022", "TAXSTAT", "us")))
        columns = list(combined[0])
        with (DERIVED / f"security_inputs_{dataset}.csv").open("w", newline="") as stream:
            writer = csv.DictWriter(stream, columns, lineterminator="\n")
            writer.writeheader()
            writer.writerows(combined)
    print(f"Security source pins verified; {len(data)} industries; customer/product total closure passed")


def check_failures():
    """Regression catalog for HTML pretending to be JSON, unsafe flags, and bad rows."""
    checks = 0
    with tempfile.TemporaryDirectory(prefix="security_input_checks_") as dirname:
        path = Path(dirname) / "security_bad_table.json"
        cases = [
            "<!DOCTYPE html><html>API error</html>",
            json.dumps({"error": "not a data table"}),
            json.dumps([["NAICS2022", "TAXSTAT", "us"], ["561612", "00"]]),
            json.dumps([["NAICS2022", "NAICS2022", "TAXSTAT", "us"], ["561612", "561621", "00", "1"]]),
            json.dumps([["NAICS2022", "TAXSTAT", "us"], ["561621", "00", "1"]]),
        ]
        for case in cases:
            path.write_text(case)
            try:
                table_rows(path, "561612", ("NAICS2022", "TAXSTAT", "us"))
            except RuntimeError as exc:
                assert "[BLOCKED]" in str(exc)
                checks += 1
            else:
                raise AssertionError("malformed/wrong Census table was accepted")
        for flag in ("X", "D", "N"):
            try:
                number({"RCPTOT": "0", "RCPTOT_F": flag}, "RCPTOT")
            except RuntimeError:
                checks += 1
            else:
                raise AssertionError("suppressed/not-applicable estimate was accepted")
        assert number({"NAPCSDOL": "41", "NAPCSDOL_F": "s"}, "NAPCSDOL", allow_small=True) == 41
        checks += 1
        # Pin checks operate on disposable copies; primary source files stay read-only.
        global LANE, INPUTS
        original_lane, original_inputs = LANE, INPUTS
        scratch = Path(dirname) / "pin_copy"
        shutil.copytree(INPUTS, scratch / "inputs")
        try:
            LANE, INPUTS = scratch, scratch / "inputs"
            manifest = verify_pins()
            target = LANE / manifest["sources"][0]["path"]
            target.write_bytes(target.read_bytes() + b"\n")
            try:
                verify_pins()
            except RuntimeError as exc:
                assert "missing or stale" in str(exc)
                checks += 1
            else:
                raise AssertionError("stale primary input was accepted")
        finally:
            LANE, INPUTS = original_lane, original_inputs
    print(f"Security input failure regressions passed: {checks}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--pin-inputs", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    start = time.perf_counter()
    if args.probe:
        probe()
    if args.acquire:
        acquire()
    if args.pin_inputs:
        pin_inputs()
    if not args.probe:
        write_outputs()
    if args.check:
        check_failures()
    print(json.dumps({"elapsed_s": round(time.perf_counter() - start, 3), "maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
