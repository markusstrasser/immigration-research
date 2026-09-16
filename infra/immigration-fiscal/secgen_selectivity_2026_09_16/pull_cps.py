#!/usr/bin/env python3
"""Pull CPS ASEC microdata (record-level) from the Census API, 2019-2024.
Pull A: ages 25-64, full variable set -> cps_asec_2564_{year}.csv
Pull B: all ages, minimal vars        -> cps_asec_allages_{year}.csv
Every URL logged (key redacted) to urls.log
"""
import json, os, sys, time, urllib.request, urllib.error, csv

BASE = "https://api.census.gov/data/{y}/cps/asec/mar"
HERE = os.path.dirname(os.path.abspath(__file__))
KEY = None
for line in open(os.path.join(HERE, "..", "acquire", "config.local.env")):
    if "CENSUS_API_KEY" in line and "=" in line:
        KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
assert KEY, "no key"

VARS_A = ["A_AGE","A_SEX","PENATVTY","PEFNTVTY","PEMNTVTY","PRCITSHP","A_HGA",
          "PEARNVAL","WSAL_VAL","MARSUPWT","PRDTHSP","PEHSPNON","PRDTRACE",
          "PEINUSYR","A_WKSTAT","WKSWORK","HRSWK"]
VARS_B = ["A_AGE","PENATVTY","PEFNTVTY","PEMNTVTY","PRCITSHP","MARSUPWT","PEHSPNON","PRDTHSP"]
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
URLLOG = open(os.path.join(HERE, "urls.log"), "a")


def fetch(year, getvars, agelo, agehi, tries=8):
    url = (BASE.format(y=year) + "?get=" + ",".join(getvars)
           + f"&A_AGE={agelo}:{agehi}&key={KEY}")
    URLLOG.write(url.replace(KEY, "<KEY>") + "\n"); URLLOG.flush()
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            sys.stderr.write(f"  retry {t+1} {year} {agelo}-{agehi}: {e}\n")
            time.sleep(8 * (t + 1))
    raise RuntimeError(f"failed {year} {agelo}-{agehi}")


def pull(tag, getvars, lo, hi, step):
    for year in YEARS:
        out = os.path.join(HERE, f"cps_asec_{tag}_{year}.csv")
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            print(f"skip {out}"); continue
        rows, header = [], None
        for a in range(lo, hi + 1, step):
            b = min(a + step - 1, hi)
            d = fetch(year, getvars, a, b)
            h = d[0]
            # API appends the predicate var again at the end; keep first len(getvars)
            idx = [h.index(v) for v in getvars]
            if header is None:
                header = getvars
            for r in d[1:]:
                rows.append([r[i] for i in idx])
            print(f"  {year} {tag} {a}-{b}: {len(d)-1} recs", flush=True)
            time.sleep(0.4)
        with open(out, "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(rows)
        print(f"WROTE {out} rows={len(rows)}", flush=True)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("A", "both"):
        pull("2564", VARS_A, 25, 64, 5)
    if which in ("B", "both"):
        pull("allages", VARS_B, 0, 85, 10)
