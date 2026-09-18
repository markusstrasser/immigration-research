#!/usr/bin/env python3
"""Aggregate Census individual-unit local government finances to counties.

Reads _cache/indunit_<year>.zip, keeps LOCAL units only (ID position 3 in 1-5),
assigns each unit to the county it is located in, and sums direct general
expenditure by function.

Two record layouts:
  2012 and earlier : ID 1-14 (Census state/county codes), item 15-17, amount 18-29,
                     year 30-33. FIPS state/county come from Fin_GID_<y>.txt
                     positions 114-115 and 116-118.
  2017 and later   : ID 1-12 with FIPS state in 1-2 and FIPS county in 4-6,
                     item 13-15, amount 16-27, year 28-31.

Amounts are thousands of dollars. Output derived/county_finance.csv.
"""
import csv
import io
import os
import sys
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
DERIVED = os.path.join(HERE, "derived")

YEARS = [2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# Direct-expenditure prefixes. E current operation, F construction,
# G other capital outlay, J assistance and subsidies. I89 (interest on general
# debt) is added separately; L/M/Q/S are intergovernmental and excluded.
DIRECT_PREFIXES = ("E", "F", "G", "J")
# Utility, liquor-store and insurance-trust functions are not general expenditure.
NON_GENERAL_FUNCS = {"90", "91", "92", "93", "94"}

FUNCTIONS = {
    "education": {"12", "16", "18", "21", "19"},   # elem-sec, higher ed + aux, other ed, scholarships (J19)
    "educ_elemsec": {"12"},                        # elementary and secondary only
    "police": {"62"},
    "corrections": {"04", "05"},
    "judicial": {"25"},
    "welfare": {"67", "68", "74", "75", "77", "79"},
    "health_hosp": {"32", "36"},
    "highways": {"44", "45"},
    "fire": {"24"},
    "parks": {"61"},
    "libraries": {"52"},
    "sewer_waste": {"80", "81"},
    "housing": {"50"},
    "admin": {"23", "29", "31"},
}


def layout(year):
    if year <= 2012:
        return {"id": (0, 14), "item": (14, 17), "amt": (17, 29), "yr": (29, 33)}
    return {"id": (0, 12), "item": (12, 15), "amt": (15, 27), "yr": (27, 31)}


def member(zf, *keys):
    for name in zf.namelist():
        low = name.lower()
        if all(k in low for k in keys):
            return name
    return None


def gid_fips_map(zf, year):
    """2012 and earlier: map the 14-char Census ID to a 5-digit FIPS county."""
    name = member(zf, "fin_gid", ".txt")
    if name is None:
        raise RuntimeError(f"{year}: no Fin_GID file")
    out = {}
    with zf.open(name) as fh:
        for raw in io.TextIOWrapper(fh, encoding="latin-1"):
            line = raw.rstrip("\n")
            if len(line) < 118:
                continue
            out[line[0:14]] = line[113:115] + line[115:118]
    return out


def read_year(year):
    path = os.path.join(CACHE, f"indunit_{year}.zip")
    lay = layout(year)
    with zipfile.ZipFile(path) as zf:
        dat = member(zf, "finestdat")
        if dat is None:
            raise RuntimeError(f"{year}: no FinEstDAT member in {zf.namelist()}")
        gid = gid_fips_map(zf, year) if year <= 2012 else None
        totals = defaultdict(lambda: defaultdict(float))
        seen_units = defaultdict(set)
        dropped_nofips = 0
        with zf.open(dat) as fh:
            for n, raw in enumerate(io.TextIOWrapper(fh, encoding="latin-1"), 1):
                line = raw.rstrip("\n")
                if len(line) < lay["yr"][1]:
                    continue
                uid = line[lay["id"][0]:lay["id"][1]]
                gtype = uid[2]
                if gtype == "0":          # state government
                    continue
                if gid is not None:
                    fips = gid.get(uid)
                    if fips is None or not fips.strip() or not fips.isdigit():
                        dropped_nofips += 1
                        continue
                else:
                    fips = uid[0:2] + uid[3:6]
                    if not fips.isdigit():
                        dropped_nofips += 1
                        continue
                item = line[lay["item"][0]:lay["item"][1]]
                try:
                    amt = float(line[lay["amt"][0]:lay["amt"][1]])
                except ValueError:
                    continue
                prefix, func = item[0], item[1:3]
                if prefix == "I" and func == "89":
                    totals[fips]["interest"] += amt
                    totals[fips]["total_direct"] += amt
                elif prefix in DIRECT_PREFIXES and func not in NON_GENERAL_FUNCS:
                    totals[fips]["total_direct"] += amt
                    for label, funcs in FUNCTIONS.items():
                        if func in funcs:
                            totals[fips][label] += amt
                seen_units[fips].add(uid)
                if n % 2_000_000 == 0:
                    print(f"  [{year}] {n:,} records", flush=True)
    for fips, units in seen_units.items():
        totals[fips]["n_units"] = len(units)
    print(f"[ok  ] {year}: {len(totals)} counties, {dropped_nofips:,} records dropped for missing FIPS",
          flush=True)
    return totals


# The 2007 Census of Governments has no individual-unit file on census.gov. The
# Willamette Government Finance Database supplies it; modal_gfd_2007.py aggregates
# that 2.9 GB CSV to counties in a container. Its 2012, 2017 and 2022 waves agree
# with the Census build to better than 0.25% on every function (correlation 0.99999+),
# so its 2007 wave carries the same definitions.
GFD_FILE = os.path.join(CACHE, "gfd_county_waves.csv")
GFD_MAP = {"total_direct": "total_direct", "education": "education",
           "educ_elemsec": "educ_elemsec", "police": "police",
           "corrections": "corrections", "judicial": "judicial",
           "welfare": "welfare", "highways": "highways"}


def read_gfd_2007():
    if not os.path.exists(GFD_FILE):
        print("[skip] 2007: no gfd_county_waves.csv in _cache", flush=True)
        return []
    out = []
    with open(GFD_FILE) as f:
        for r in csv.DictReader(f):
            if r["year"] != "2007":
                continue
            rec = {"fips": r["fips"], "year": 2007, "n_units": int(r["n_units"])}
            for label, col in GFD_MAP.items():
                rec[label] = float(r[col])
            rec["health_hosp"] = float(r["health"]) + float(r["hospital"])
            out.append(rec)
    print(f"[ok  ] 2007: {len(out)} counties from the Government Finance Database", flush=True)
    return out


def main():
    os.makedirs(DERIVED, exist_ok=True)
    cols = ["fips", "year", "total_direct", "interest", "n_units"] + sorted(FUNCTIONS)
    rows = []
    for rec in read_gfd_2007():
        rows.append({c: rec.get(c, "") for c in cols})
    for year in YEARS:
        if not os.path.exists(os.path.join(CACHE, f"indunit_{year}.zip")):
            print(f"[skip] {year}: no zip", flush=True)
            continue
        print(f"[read] {year}", flush=True)
        for fips, rec in sorted(read_year(year).items()):
            row = {"fips": fips, "year": year}
            for c in cols[2:]:
                row[c] = rec.get(c, 0.0)
            rows.append(row)
    out = os.path.join(DERIVED, "county_finance.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.1f}" if isinstance(v, float) else v) for k, v in r.items()})
    print(f"[done] {out} {len(rows)} rows", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
