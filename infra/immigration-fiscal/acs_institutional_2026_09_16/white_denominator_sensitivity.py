"""White-denominator sensitivity for the US-born Mexican-origin / white institutionalization ratio.

Sabol, Johnson & Lynch 2025 (doi:10.1007/s12103-025-09810-1) show the 2023 ACS race redesign moved
multi-race reporting sharply; single-race coding could understate the 2023 white rate. This script
re-pulls native non-Hispanic white men 18-39 under two definitions, RAC1P=1 (white alone, the memo's
definition) and RACWHT=1 (white alone or in combination), for 2019 and 2023, and recomputes the ratio
against the Mexican-origin native rate already in acs_institutional_rates.csv.
"""
import csv, json, os, pathlib, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
KEY = os.environ.get("CENSUS_API_KEY", "")
YEARS = {"2019": "TYPE", "2023": "TYPEHUGQ"}
DEFS = {"RAC1P=1": "white alone", "RACWHT=1": "white alone or in combination"}


def fetch(yr, gq, pred):
    out = HERE / f"w{yr}_{pred.split('=')[0]}.json"
    if not out.exists():
        url = (f"https://api.census.gov/data/{yr}/acs/acs1/pums?tabulate=weight(PWGTP)&col+{gq}"
               f"&row+NATIVITY&{pred}&HISP=01&SEX=1&AGEP=18:39&key={KEY}")
        out.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return json.loads(out.read_text())


def native_inst_rate(tab, gq):
    hdr = tab[0]
    cols = {list(c.values())[0]: i for i, c in enumerate(hdr[:-1])}
    row = next(r for r in tab[1:] if r[-1] == "1")
    total = sum(row[i] for i in cols.values())
    return row[cols["2"]] / total * 100


def mexican_native(yr):
    with open(HERE / "acs_institutional_rates.csv") as f:
        for r in csv.DictReader(f):
            if r["year"] == yr and r["group"] == "Mexican" and r["nativity"] == "native":
                return float(r["pct"])
    raise KeyError(yr)


rows = []
for yr, gq in YEARS.items():
    mex = mexican_native(yr)
    for pred, label in DEFS.items():
        w = native_inst_rate(fetch(yr, gq, pred), gq)
        rows.append((yr, label, round(w, 3), mex, round(mex / w, 3)))
print(f"{'year':6}{'white definition':34}{'white_native_%':>15}{'mex_native_%':>13}{'ratio':>7}")
for r in rows:
    print(f"{r[0]:6}{r[1]:34}{r[2]:15.3f}{r[3]:13.2f}{r[4]:7.3f}")
with open(HERE / "white_denominator_sensitivity.csv", "w", newline="") as f:
    wtr = csv.writer(f); wtr.writerow(["year", "white_definition", "white_native_inst_pct", "mexican_native_inst_pct", "ratio"])
    wtr.writerows(rows)
