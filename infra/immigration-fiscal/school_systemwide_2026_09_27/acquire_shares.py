"""State enrollment shares: Hispanic and English-learner shares of public-school enrollment (CCD, via
the Urban Institute Education Data API), and immigrant shares of school-age children (ACS 1-year).

Writes derived/state_shares.csv (one row per state × fall year). Raw pulls are cached in _cache/.

CCD (Urban Institute Education Data Portal, public API, no key):
  school-districts/ccd/enrollment/summaries (sum of district membership by FIPS and race, grade 99)
  school-districts/ccd/directory/summaries (sum of district English-learner counts by FIPS)
ACS 1-year (api.census.gov; key read from CENSUS_API_KEY, never printed):
  B05003 under-18 population by nativity; B05009 own children 6–17 by own and parents' nativity.
  fb_share_617 counts foreign-born children of foreign-born parents (the 2006–07 layout does not
  split children of one native and one foreign-born parent by the child's nativity).

Run from the repository root (the key file is untracked):
    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/school_systemwide_2026_09_27/acquire_shares.py
"""
import csv
import json
import os
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "shares"
OUT = HERE / "derived" / "state_shares.csv"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"}
URBAN = "https://educationdata.urban.org/api/v1/school-districts/ccd/"
CCD_YEARS = range(1995, 2024)       # fall of the school year (2018 = 2018–19)
ACS_YEARS = [y for y in range(2005, 2025) if y != 2020]  # no standard 2020 1-year release
FIPS = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA",
        15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD",
        25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
        35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC",
        46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}
# ACS variable codes move between years (B05009 changed layout in 2008), so variables are found
# by their label path, colons stripped: {name: label path under "Estimate!!"}
LABELS = {
    "B05003": {"m_u18": "Total!!Male!!Under 18 years", "m_u18_fb": "Total!!Male!!Under 18 years!!Foreign born",
               "f_u18": "Total!!Female!!Under 18 years", "f_u18_fb": "Total!!Female!!Under 18 years!!Foreign born"},
    "B05009": {"c617": "Total!!6 to 17 years",
               "both_fb": "Total!!6 to 17 years!!Living with two parents!!Both parents foreign born",
               "both_fb_cfb": "Total!!6 to 17 years!!Living with two parents!!Both parents foreign born!!Child is foreign born",
               "mixed": "Total!!6 to 17 years!!Living with two parents!!One native and one foreign-born parent",
               "one_fb": "Total!!6 to 17 years!!Living with one parent!!Foreign-born parent",
               "one_fb_cfb": "Total!!6 to 17 years!!Living with one parent!!Foreign-born parent!!Child is foreign born"},
}
FIELDS = ["state", "fall_year", "ccd_total", "ccd_known_race", "ccd_hispanic", "ccd_white", "hisp_share",
          "white_share", "ccd_el", "el_share_ccd", "acs_year", "acs_u18", "acs_u18_fb", "fb_share_u18",
          "acs_c617", "acs_c617_fb", "acs_c617_imm_parent", "fb_share_617", "imm_origin_share_617"]


def cached_json(name, fetch):
    path = CACHE / name
    if not path.exists():
        for attempt in range(5):
            try:
                data = fetch()
                break
            except (requests.RequestException, ValueError) as e:
                print("retry", name, type(e).__name__)
                time.sleep(10 * (attempt + 1))
        else:
            raise RuntimeError(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, sort_keys=True))
    return json.loads(path.read_text())


def urban(endpoint, params):
    def fetch():
        r = requests.get(URBAN + endpoint, params=params, headers=UA, timeout=300)
        r.raise_for_status()
        d = r.json()
        assert d.get("next") is None, "paged summary"
        return d["results"]
    return fetch


def acs_codes(year, group):
    """Map LABELS[group] names to this year's variable codes via the public group metadata."""
    def fetch():
        r = requests.get(f"https://api.census.gov/data/{year}/acs/acs1/groups/{group}.json", headers=UA, timeout=300)
        r.raise_for_status()
        return r.json()
    meta = cached_json(f"acs_meta_{group}_{year}.json", fetch)["variables"]
    def norm(label):  # 2023 onward writes "Foreign-born" where earlier years write "Foreign born"
        return label.replace("Estimate!!", "").replace(":", "").replace("-", " ").lower()
    by_label = {norm(v["label"]): k for k, v in meta.items() if k.endswith("E")}
    return {name: by_label[norm(path)] for name, path in LABELS[group].items()}


def census(year, group):
    codes = acs_codes(year, group)

    def fetch():
        r = requests.get(f"https://api.census.gov/data/{year}/acs/acs1",
                         params={"get": ",".join(codes.values()), "for": "state:*", "key": os.environ["CENSUS_API_KEY"]},
                         headers=UA, timeout=300)
        if r.status_code != 200:  # never echo the request URL: it carries the key
            raise requests.RequestException(f"status {r.status_code}")
        return r.json()
    data = cached_json(f"acs_{group.lower()}_{year}.json", fetch)
    head, recs = data[0], data[1:]
    inv = {v: k for k, v in codes.items()}
    # suppressed cells come back null (e.g. Montana's 2007 B05009); keep them as None
    return [{**{inv[h]: (None if v is None else int(v)) for h, v in zip(head, rec) if h in inv},
             "state": int(rec[head.index("state")])} for rec in recs]


def main():
    rows = {}
    for y in CCD_YEARS:
        race = cached_json(f"ccd_race_{y}.json", urban("enrollment/summaries",
                           {"var": "enrollment", "stat": "sum", "by": "fips,race", "grade": 99, "year": y}))
        el = cached_json(f"ccd_el_{y}.json", urban("directory/summaries",
                         {"var": "english_language_learners", "stat": "sum", "by": "fips", "year": y}))
        by = {}
        for x in race:
            if x["fips"] in FIPS and x["enrollment"] is not None and x["enrollment"] >= 0:
                by.setdefault(x["fips"], {})[x["race"]] = x["enrollment"]
        elc = {x["fips"]: x["english_language_learners"] for x in el
               if x["fips"] in FIPS and x["english_language_learners"] is not None and x["english_language_learners"] > 0}
        for f, d in by.items():
            known = sum(v for k, v in d.items() if k in (1, 2, 3, 4, 5, 6, 7))
            total = d.get(99)
            if not total or not known:
                continue
            r = rows.setdefault((FIPS[f], y), {"state": FIPS[f], "fall_year": y})
            r.update(ccd_total=total, ccd_known_race=known, ccd_hispanic=d.get(3, 0), ccd_white=d.get(1, 0),
                     hisp_share=round(100 * d.get(3, 0) / known, 4), white_share=round(100 * d.get(1, 0) / known, 4))
            if f in elc:
                r.update(ccd_el=elc[f], el_share_ccd=round(100 * elc[f] / total, 4))
    for y in ACS_YEARS:
        for d in census(y, "B05003"):
            if d["state"] not in FIPS or any(v is None for v in d.values()):
                continue
            u18, fb = d["m_u18"] + d["f_u18"], d["m_u18_fb"] + d["f_u18_fb"]
            r = rows.setdefault((FIPS[d["state"]], y), {"state": FIPS[d["state"]], "fall_year": y})
            r.update(acs_year=y, acs_u18=u18, acs_u18_fb=fb, fb_share_u18=round(100 * fb / u18, 4))
        if y < 2006:  # B05009 starts in 2006
            continue
        for d in census(y, "B05009"):
            if d["state"] not in FIPS or any(v is None for v in d.values()):
                continue
            fb = d["both_fb_cfb"] + d["one_fb_cfb"]  # foreign-born children of foreign-born parents
            imm = d["both_fb"] + d["mixed"] + d["one_fb"]  # at least one foreign-born parent
            rows[(FIPS[d["state"]], y)].update(
                acs_c617=d["c617"], acs_c617_fb=fb, acs_c617_imm_parent=imm,
                fb_share_617=round(100 * fb / d["c617"], 4), imm_origin_share_617=round(100 * imm / d["c617"], 4))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])
    print(f"wrote {OUT} rows={len(rows)}")


if __name__ == "__main__":
    main()
