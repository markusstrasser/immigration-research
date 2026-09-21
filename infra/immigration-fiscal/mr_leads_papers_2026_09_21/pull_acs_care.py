"""ACS PUMS tabulations for the elder-care channel: who staffs direct care, who is institutionalized.

Reads CENSUS_API_KEY from the environment and never prints it. Writes raw JSON to `_cache/` and
one tidy table to `derived/acs_care_inputs.csv`.
"""
import csv
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE, DERIVED = LANE / "_cache", LANE / "derived"
YEAR = os.environ.get("ACS_YEAR", "2024")
BASE = f"https://api.census.gov/data/{YEAR}/acs/acs1/pums?tabulate=weight(PWGTP)"
# 2018 Census occupation codes: home health aides, personal care aides, nursing assistants, orderlies.
CARE = "&OCCP=3601&OCCP=3602&OCCP=3603&OCCP=3605"  # a filtered variable repeats; commas fail
EMPLOYED = "1,2"
LABOR_FORCE = "1,2,3"

QUERIES = {
    # direct-care workers, employed
    "care_by_nativity": f"&col+NATIVITY&row+SEX{CARE}&ESR={EMPLOYED}",
    "care_mexico_born": f"&col+NATIVITY&row+SEX{CARE}&ESR={EMPLOYED}&POBP=303",
    "care_mexican_origin": f"&col+NATIVITY&row+SEX{CARE}&ESR={EMPLOYED}&HISP=02",
    # civilian labour force with high school or less, 16+
    "lowed_lf_by_nativity": f"&col+NATIVITY&row+SEX&SCHL=01:17&AGEP=16:99&ESR={LABOR_FORCE}",
    "lowed_lf_mexico_born": f"&col+NATIVITY&row+SEX&SCHL=01:17&AGEP=16:99&ESR={LABOR_FORCE}&POBP=303",
    "all_lf_by_nativity": f"&col+NATIVITY&row+SEX&AGEP=16:99&ESR={LABOR_FORCE}",
    # Butcher–Moran–Watson treatment: working-age (16–64) population, foreign-born with less than
    # one year of college (SCHL 01–18), as a share of the whole working-age population
    "wa_pop_by_nativity": "&col+NATIVITY&row+SEX&AGEP=16:64",
    "wa_lowed_by_nativity": "&col+NATIVITY&row+SEX&AGEP=16:64&SCHL=01:18",
    "wa_lowed_mexico_born": "&col+NATIVITY&row+SEX&AGEP=16:64&SCHL=01:18&POBP=303",
    # the Mexican-origin population's own elderly
    "age65_mexican_origin": "&col+NATIVITY&row+TYPEHUGQ&AGEP=65:99&HISP=02",
    # elderly by housing type (1 housing unit, 2 institutional group quarters, 3 other group quarters)
    "age65_by_gq_nativity": "&col+NATIVITY&row+TYPEHUGQ&AGEP=65:99",
    "age80_by_gq_nativity": "&col+NATIVITY&row+TYPEHUGQ&AGEP=80:99",
}


def fetch(tag, query):
    target = CACHE / f"acs{YEAR}_{tag}.json"
    if target.exists():
        return json.loads(target.read_text())
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise SystemExit("[BLOCKED] CENSUS_API_KEY is not set")
    url = f"{BASE}{query}&key={key}"  # national PUMS tabulations take no geography clause
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                payload = json.loads(response.read().decode())
            target.write_text(json.dumps(payload))
            return payload
        except Exception as error:  # the message can carry the key: report the class only
            print(f"  ! {tag}: {type(error).__name__} (attempt {attempt + 1})")
            time.sleep(3)
    raise SystemExit(f"[BLOCKED] {tag}: request failed three times")


def cells(payload):
    """Flatten a tabulate response: header = column dicts then row names; body = weights then row values."""
    header, *body = payload
    columns = [item for item in header if isinstance(item, dict)]
    names = [item for item in header if not isinstance(item, dict)]
    out = {}
    for line in body:
        weights, values = line[:len(columns)], line[len(columns):]
        for column, weight in zip(columns, weights):
            key = dict(column, **dict(zip(names, values)))
            out[tuple(sorted(key.items()))] = float(weight)
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    rows = []
    for tag, query in QUERIES.items():
        table = cells(fetch(tag, query))
        for key, weight in sorted(table.items()):
            rows.append({"year": YEAR, "query": tag, "cell": ";".join(f"{k}={v}" for k, v in key), "weight": round(weight)})
        print(f"  ✓ {tag}: {len(table)} cells, total {sum(table.values()):,.0f}")
    with open(DERIVED / "acs_care_inputs.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["year", "query", "cell", "weight"])
        writer.writeheader()
        writer.writerows(rows)
    leaked = [p.name for p in CACHE.glob(f"acs{YEAR}_*.json") if re.search(r"key=", p.read_text())]
    assert not leaked, leaked


if __name__ == "__main__":
    sys.exit(main())
