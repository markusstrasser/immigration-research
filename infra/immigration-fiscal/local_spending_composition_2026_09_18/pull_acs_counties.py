#!/usr/bin/env python3
"""County ACS 5-year shares (Hispanic, foreign born, Mexico born) + 2000 Census pre-period.

Writes one CSV per wave into _cache/acs/ and a tidy combined file
derived/county_shares.csv with columns
  fips, wave, pop, hisp, fb, mex, pop_u19, pop_65p, medhhinc

B05006's Mexico cell moves across years (138 in 2009, 137 in 2012, 139 in 2017,
160 in 2022), so it is resolved from each year's group metadata by label.
"""
import csv
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache", "acs")
DERIVED = os.path.join(HERE, "derived")
KEY = os.environ.get("CENSUS_API_KEY", "")
API = "https://api.census.gov/data"

ACS_WAVES = [2009, 2012, 2017, 2022]

# B01001 sex-by-age cells summing to population under 19 and 65+.
U19 = [f"B01001_{n:03d}E" for n in (3, 4, 5, 6, 7)] + [f"B01001_{n:03d}E" for n in (27, 28, 29, 30, 31)]
P65 = [f"B01001_{n:03d}E" for n in (20, 21, 22, 23, 24, 25)] + [f"B01001_{n:03d}E" for n in (44, 45, 46, 47, 48, 49)]


def get_json(url, tries=5):
    last = None
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            last = exc
            print(f"  [warn] attempt {attempt}: {exc}", flush=True)
            time.sleep(4 * attempt)
    raise RuntimeError(f"failed after {tries}: {last}")


def mexico_var(year):
    g = get_json(f"{API}/{year}/acs/acs5/groups/B05006.json")["variables"]
    hits = [k for k, v in g.items()
            if k.endswith("E") and v.get("label", "").rstrip("!:").endswith("Mexico")]
    if len(hits) != 1:
        raise RuntimeError(f"{year}: expected 1 Mexico cell, got {hits}")
    return hits[0]


def fetch_acs(year):
    dest = os.path.join(CACHE, f"acs5_{year}.json")
    if os.path.exists(dest):
        print(f"[skip] acs {year}", flush=True)
        return json.load(open(dest))
    mex = mexico_var(year)
    print(f"[get ] acs {year} mexico={mex}", flush=True)
    base = ["B03003_001E", "B03003_003E", "B05002_001E", "B05002_013E",
            "B05006_001E", mex, "B19013_001E"]
    out = {}
    # the API caps get= at 50 variables per call
    for chunk in (base, U19, P65):
        varlist = ",".join(chunk)
        url = f"{API}/{year}/acs/acs5?get={varlist}&for=county:*&key={KEY}"
        rows = get_json(url)
        hdr = rows[0]
        si, ci = hdr.index("state"), hdr.index("county")
        for row in rows[1:]:
            fips = row[si] + row[ci]
            rec = out.setdefault(fips, {})
            for name, val in zip(hdr, row):
                if name in ("state", "county"):
                    continue
                rec[name] = val
        time.sleep(1)
    payload = {"mexico_var": mex, "rows": out}
    os.makedirs(CACHE, exist_ok=True)
    json.dump(payload, open(dest, "w"))
    print(f"[ok  ] acs {year} {len(out)} counties", flush=True)
    return payload


def fetch_2000():
    dest = os.path.join(CACHE, "dec2000.json")
    if os.path.exists(dest):
        print("[skip] 2000", flush=True)
        return json.load(open(dest))
    print("[get ] 2000 sf1 + sf3", flush=True)
    out = {}
    sf1 = get_json(f"{API}/2000/dec/sf1?get=P008001,P008010&for=county:*&key={KEY}")
    hdr = sf1[0]
    si, ci = hdr.index("state"), hdr.index("county")
    for row in sf1[1:]:
        out[row[si] + row[ci]] = {"pop": row[hdr.index("P008001")],
                                  "hisp": row[hdr.index("P008010")]}
    time.sleep(1)
    sf3 = get_json(f"{API}/2000/dec/sf3?get=P021001,P021013&for=county:*&key={KEY}")
    hdr = sf3[0]
    si, ci = hdr.index("state"), hdr.index("county")
    for row in sf3[1:]:
        rec = out.setdefault(row[si] + row[ci], {})
        rec["pop_sf3"] = row[hdr.index("P021001")]
        rec["fb"] = row[hdr.index("P021013")]
    os.makedirs(CACHE, exist_ok=True)
    json.dump(out, open(dest, "w"))
    print(f"[ok  ] 2000 {len(out)} counties", flush=True)
    return out


def num(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x <= -666666666 else x


def main():
    if not KEY:
        print("CENSUS_API_KEY not set", file=sys.stderr)
        return 2
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(DERIVED, exist_ok=True)
    rows = []
    for year in ACS_WAVES:
        payload = fetch_acs(year)
        mex = payload["mexico_var"]
        for fips, rec in payload["rows"].items():
            u19 = sum(num(rec.get(v)) or 0 for v in U19)
            p65 = sum(num(rec.get(v)) or 0 for v in P65)
            rows.append({
                "fips": fips, "wave": year,
                "pop": num(rec.get("B03003_001E")),
                "hisp": num(rec.get("B03003_003E")),
                "fb": num(rec.get("B05002_013E")),
                "mex": num(rec.get(mex)),
                "pop_u19": u19, "pop_65p": p65,
                "medhhinc": num(rec.get("B19013_001E")),
            })
    dec = fetch_2000()
    for fips, rec in dec.items():
        rows.append({
            "fips": fips, "wave": 2000,
            "pop": num(rec.get("pop")), "hisp": num(rec.get("hisp")),
            "fb": num(rec.get("fb")), "mex": None,
            "pop_u19": None, "pop_65p": None, "medhhinc": None,
        })
    rows.sort(key=lambda r: (r["fips"], r["wave"]))
    out = os.path.join(DERIVED, "county_shares.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[done] {out} {len(rows)} rows", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
