"""County-area sums of local administration spending from the Census individual-unit files.

Reuses the record layouts and helpers of local_spending_composition_2026_09_18/build_county_panel.py
(imported read-only): 2012 IDs are 14 characters with FIPS from Fin_GID_2012.txt; 2017 and later
IDs are 12 characters with FIPS state in 1-2 and FIPS county in 4-6. Local units are every unit
whose type digit (ID position 3) is not 0 (state), as in that lane.

Per county and year (thousands of dollars):
  e23, e29, e31, e25  current operations (item prefix E) for financial administration, central
                      staff, general public buildings, judicial and legal;
  d23, d29, d31, d25  direct expenditure on the same functions (prefixes E, F, G, J), the
                      composition lane's definition.
"""
import importlib.util
import io
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMP = HERE.parent / "local_spending_composition_2026_09_18"
_spec = importlib.util.spec_from_file_location("build_county_panel", COMP / "build_county_panel.py")
bcp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bcp)

CODES = ("23", "29", "31", "25")
DIRECT = ("E", "F", "G", "J")


def _zip(year):
    return COMP / "_cache" / f"indunit_{year}.zip"


def read_indunit(year):
    lay = bcp.layout(year)
    out = defaultdict(lambda: defaultdict(float))
    types = defaultdict(Counter)
    units = defaultdict(set)
    with zipfile.ZipFile(_zip(year)) as zf:
        dat = bcp.member(zf, "finestdat")
        gid = bcp.gid_fips_map(zf, year) if year <= 2012 else None
        with zf.open(dat) as fh:
            for raw in io.TextIOWrapper(fh, encoding="latin-1"):
                line = raw.rstrip("\n")
                if len(line) < lay["yr"][1]:
                    continue
                uid = line[lay["id"][0]:lay["id"][1]]
                if uid[2] == "0":
                    continue
                if gid is not None:
                    fips = gid.get(uid)
                    if fips is None or not fips.strip() or not fips.isdigit():
                        continue
                else:
                    fips = uid[0:2] + uid[3:6]
                    if not fips.isdigit():
                        continue
                item = line[lay["item"][0]:lay["item"][1]]
                try:
                    amt = float(line[lay["amt"][0]:lay["amt"][1]])
                except ValueError:
                    continue
                if uid not in units[fips]:
                    units[fips].add(uid)
                    types[fips][uid[2]] += 1
                prefix, func = item[0], item[1:3]
                if func in CODES:
                    if prefix == "E":
                        out[fips][f"e{func}"] += amt
                    if prefix in DIRECT:
                        out[fips][f"d{func}"] += amt
    result = {}
    for fips in units:
        rec = {k: out[fips].get(k, 0.0) for k in [f"e{c}" for c in CODES] + [f"d{c}" for c in CODES]}
        rec["n_units"] = len(units[fips])
        rec["n_county_govt"] = types[fips]["1"]
        rec["n_municipal"] = types[fips]["2"]
        rec["n_township"] = types[fips]["3"]
        result[fips] = rec
    return result


def unit_directory(year):
    """(fips, type digit, name) for every local unit in the year's directory file."""
    rows = []
    with zipfile.ZipFile(_zip(year)) as zf:
        if year <= 2012:
            name = bcp.member(zf, "fin_gid", ".txt")
            with zf.open(name) as fh:
                for raw in io.TextIOWrapper(fh, encoding="latin-1"):
                    line = raw.rstrip("\n")
                    if len(line) < 118 or line[2] == "0":
                        continue
                    fips = line[113:115] + line[115:118]
                    if fips.isdigit():
                        rows.append((fips, line[2], line[14:78].strip()))
        else:
            name = bcp.member(zf, "fin_pid", ".txt")
            with zf.open(name) as fh:
                for raw in io.TextIOWrapper(fh, encoding="latin-1"):
                    line = raw.rstrip("\n")
                    if len(line) < 76 or line[2] == "0":
                        continue
                    fips = line[0:2] + line[3:6]
                    if fips.isdigit():
                        rows.append((fips, line[2], line[12:76].strip()))
    return rows
