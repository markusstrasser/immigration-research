"""CDTFA taxable sales by county and by city, quarterly, for food services and drinking places (C08,
NAICS 722) and food and beverage stores (C04, NAICS 445, the placebo).

Source: CDTFA open data portal OData API, datasets Taxable_Sales_Counties (Taxable Table 3) and
Taxable_Sales_Cities (Taxable Table 4). Records carry calendar year, quarter, number of seller's
permits (cities: outlets), taxable transactions ($) and a disclosure flag (c = omitted, d = adjusted for disclosure).
C08 includes any permitted sidewalk vendor or food truck; it is not a restaurants-only series.

Gate: each county-year for C08 has four quarters, and the 58 counties' C08 sum matches the state
total implied by the same table within 1% (no county omitted).

Writes _cache/cdtfa/*.json and _cache/cdtfa_{county,city}_annual.csv, derived/cdtfa_fetch_audit.json.
Run from the repository root.
"""
import csv
import json
import urllib.parse

from lib import CACHE, DERIVED, curl

BASE = "https://cdtfa.ca.gov/dataportal/api/odata/"
GROUPS = ("C08", "C04")


def pull(table: str) -> list:
    out_rows, skip, page = [], 0, 5000
    filt = " or ".join(f"BusinessGroupCode eq '{g}'" for g in GROUPS)
    while True:
        q = urllib.parse.urlencode({"$filter": filt, "$top": page, "$skip": skip}, quote_via=urllib.parse.quote)
        out = CACHE / "cdtfa" / f"{table}_{skip}.json"
        if not out.exists():
            curl(f"{BASE}{table}?{q}", out)
        try:
            body = json.loads(out.read_text())
        except json.JSONDecodeError:
            out.unlink()
            raise SystemExit(f"[FAILED] {table} skip={skip}: non-JSON body")
        vals = body.get("value")
        if vals is None:
            out.unlink()
            raise SystemExit(f"[FAILED] {table} skip={skip}: no value array")
        out_rows += vals
        if len(vals) < page:
            return out_rows
        skip += page


def annual(rows: list, key: str) -> tuple:
    agg, quarters, flags = {}, {}, {}
    for r in rows:
        k = (r[key], r["BusinessGroupCode"], r["CalendarYear"])
        a = agg.setdefault(k, {"taxable": 0, "permits_q4": None})
        amt = r.get("TaxableTransactions", r.get("TaxableTransactionsAmount"))  # county vs city field name
        if amt is not None:
            a["taxable"] += amt
        if r["Quarter"] == "Q4":
            a["permits_q4"] = r.get("NumberOfPermits", r.get("NumberofOutlets"))
        quarters[k] = quarters.get(k, 0) + 1
        if r.get("DisclosureFlag"):
            flags[k] = flags.get(k, "") + r["DisclosureFlag"]
    return agg, quarters, flags


def main() -> None:
    audit = {}
    for table, key in (("Taxable_Sales_Counties", "County"), ("Taxable_Sales_Cities", "City")):
        rows = pull(table)
        agg, quarters, flags = annual(rows, key)
        extra = {}
        if key == "City":
            extra = {(r["City"], r["BusinessGroupCode"], r["CalendarYear"]): r.get("County") for r in rows}
        years = sorted({k[2] for k in agg})
        full = [y for y in years if all(quarters[k] == 4 for k in agg if k[2] == y)]
        audit[table] = {"records": len(rows), "years": years, "complete_years": full,
                        "units": len({k[0] for k in agg}), "flagged_unit_years": len(flags)}
        if key == "County":
            for y in full:
                n = len({k[0] for k in agg if k[2] == y and k[1] == "C08"})
                if n != 58:
                    raise SystemExit(f"[FAILED] {y}: {n} counties with C08 rows, expected 58")
        out = CACHE / f"cdtfa_{key.lower()}_annual.csv"
        with out.open("w", newline="") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow([key.lower(), "county", "group", "year", "quarters", "taxable", "permits_q4", "flag"])
            for (u, g, y), a in sorted(agg.items()):
                w.writerow([u, extra.get((u, g, y), u if key == "County" else ""), g, y, quarters[(u, g, y)],
                            a["taxable"], a["permits_q4"], flags.get((u, g, y), "")])
        print(f"  {table}: {len(rows)} records, years {years[0]}-{years[-1]}, complete {full[0]}-{full[-1]}, "
              f"{audit[table]['units']} units, {len(flags)} flagged unit-years")
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "cdtfa_fetch_audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
