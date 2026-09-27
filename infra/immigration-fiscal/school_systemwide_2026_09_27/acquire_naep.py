"""Pull state NAEP results (grades 4 and 8, math and reading) from the NAEP Data Service API.

Raw responses are cached in _cache/naep/ and never re-fetched once present; the tidy panel is
written to derived/naep_state_long.csv. Public API, generic User-Agent, no identifier.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/acquire_naep.py
"""
import csv
import json
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "naep"
OUT = HERE / "derived" / "naep_state_long.csv"
API = "https://www.nationsreportcard.gov/Dataservice/GetAdhocData.aspx"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"}

STATES = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH "
          "NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split()
JURIS = STATES + ["NP"]
COMMON = [2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017, 2019, 2022, 2024]
YEARS = {"mathematics": [1996, 2000] + COMMON, "reading": [1998, 2002] + COMMON}
SUBSCALE = {"mathematics": "MRPCM", "reading": "RRPCM"}

# (variable, stattype, grades, category index or None)
QUERIES = [
    ("TOTAL", "MN:MN", (4, 8), None),
    ("SDRACE", "MN:MN", (4, 8), None),
    ("LEP", "MN:MN", (4, 8), None),
    ("SDRACE+LEP", "MN:MN", (4, 8), "1+1,1+2,3+1,3+2"),
    ("SDRACE", "RP:RP", (4, 8), None),
    ("LEP", "RP:RP", (4, 8), None),
    ("SDRACE", "PC:P1", (4, 8), "1"),
    ("SDRACE", "PC:P9", (4, 8), "1"),
    ("TOTAL", "SD:SD", (4, 8), None),
    ("SDRACE", "SD:SD", (4, 8), "1"),
    # composition of white students: the SECOND variable is the base of a crosstab row percent, so
    # SLUNCH3+SDRACE 1+1 is the percent of white students eligible for the school lunch program
    ("SLUNCH3+SDRACE", "RP:RP", (4, 8), "1+1,2+1,3+1"),
    ("PARED+SDRACE", "RP:RP", (8,), "1+1,2+1,3+1,4+1,7+1"),
]

FIELDS = ["subject", "grade", "year", "jurisdiction", "variable", "var_value", "var_label", "stattype",
          "value", "std_error", "cell_n", "displayable", "error_flag"]


def jobs():
    for subject in ("mathematics", "reading"):
        for variable, stattype, grades, cats in QUERIES:
            for grade in grades:
                yield subject, grade, variable, stattype, cats


def cache_path(subject, grade, variable, stattype, cats):
    tag = f"{subject}_g{grade}_{variable}_{stattype}_{cats or 'all'}"
    return CACHE / (tag.replace(":", "-").replace("+", "x").replace(",", "_") + ".json")


def fetch(job):
    subject, grade, variable, stattype, cats = job
    path = cache_path(*job)
    if path.exists():
        return path
    params = {
        "type": "data", "subject": subject, "grade": grade, "subscale": SUBSCALE[subject],
        "variable": variable, "jurisdiction": ",".join(JURIS), "stattype": stattype,
        "Year": ",".join(f"{y}R3" for y in YEARS[subject]), "QCData": "true",
    }
    if cats:
        params["categoryindex"] = cats
    url = API + "?" + urllib.parse.urlencode(params, safe=",:")
    for attempt in range(5):
        try:
            r = requests.get(url, headers=UA, timeout=600)
            d = r.json()
            if r.status_code == 200 and d.get("status") == 200 and isinstance(d.get("result"), list):
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_suffix(".tmp")
                tmp.write_text(json.dumps({"url": url, "response": d}, sort_keys=True))
                tmp.rename(path)
                return path
            print("bad response", path.name, r.status_code, str(d)[:200])
        except (requests.RequestException, ValueError) as e:
            print("retry", path.name, type(e).__name__, e)
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"failed: {path.name}")


def rows():
    out = []
    for job in jobs():
        payload = json.loads(cache_path(*job).read_text())
        for x in payload["response"]["result"]:
            out.append({
                "subject": job[0], "grade": x["grade"], "year": x["year"], "jurisdiction": x["jurisdiction"],
                "variable": x["variable"], "var_value": x["varValue"], "var_label": x["varValueLabel"],
                "stattype": x["stattype"],
                "value": "" if not x["isStatDisplayable"] else repr(round(float(x["value"]), 6)),
                "std_error": "" if not x["isStatDisplayable"] or x.get("stdError", -1) in (None, -1)
                else repr(round(float(x["stdError"]), 6)),
                "cell_n": "" if x.get("cellN") in (None, -1) else int(x["cellN"]),
                "displayable": int(x["isStatDisplayable"]), "error_flag": x.get("errorFlag"),
            })
    key = lambda r: (r["subject"], r["grade"], r["variable"], r["stattype"], r["var_value"], r["jurisdiction"], r["year"])
    return sorted(out, key=key)


def main():
    todo = [j for j in jobs() if not cache_path(*j).exists()]
    print(f"{len(todo)} of {len(list(jobs()))} queries to fetch")
    with ThreadPoolExecutor(max_workers=3) as ex:
        for p in ex.map(fetch, todo):
            print("cached", p.name)
    data = rows()
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(data)
    print(f"wrote {OUT} rows={len(data)}")


if __name__ == "__main__":
    main()
