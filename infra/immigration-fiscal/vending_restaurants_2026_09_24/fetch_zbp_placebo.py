"""ZIP Business Patterns and ACS exposure for placebo counties: large high-Hispanic counties in states
that did not legalize sidewalk vending statewide.

Counties: Harris TX (48201), Dallas TX (48113), Bexar TX (48029), Maricopa AZ (04013), Cook IL
(17031), Miami-Dade FL (12086). Local rules differ (Chicago licensed food carts in 2015; Florida
preempted local regulation of licensed food trucks in 2020), which the report notes; none had a
statewide sidewalk-vending legalization in 2018-2019.

Same construction as fetch_zbp.py: 2010 ZCTAs with at least half their population in the county;
2012-2017 read from the cached national ZIP files, 2018-2023 queried by ZIP chunks. ACS 2013-2017
ZCTA shares come from the same variables as fetch_acs.py.

Writes _cache/zbp_placebo_panel.csv and derived/exposure_zcta_placebo.csv. Run from the repository
root with CENSUS_API_KEY set.
"""
import csv

import pandas as pd

from fetch_acs import acs
from fetch_zbp import CODES, MID, YEARS, pull
from lib import CACHE, DERIVED

COUNTIES = {"48201": "harris", "48113": "dallas", "48029": "bexar", "04013": "maricopa", "17031": "cook",
            "12086": "miamidade"}
ZBP_CODES = [c for c in CODES if c != "722330"]


def county_zips() -> dict:
    out = {f: set() for f in COUNTIES}
    with (CACHE / "zcta_county_rel_10.txt").open() as fh:
        for r in csv.DictReader(fh):
            f = r["STATE"] + r["COUNTY"]
            if f in out and float(r["ZPOPPCT"]) >= 50:
                out[f].add(r["ZCTA5"])
    return out


def main() -> None:
    cz = county_zips()
    rows = []
    for fips, tag in COUNTIES.items():
        zips = cz[fips]
        for y in YEARS:
            for c in ZBP_CODES:
                data = pull(y, c, zips, tag=tag)
                h = data[0]
                iz, ie, isz = h.index("zip code"), h.index("ESTAB"), h.index("EMPSZES")
                for r in data[1:]:
                    if r[iz] in zips and r[isz] == "001":
                        rows.append({"county": fips, "year": y, "naics": c, "zip": r[iz], "estab": int(r[ie])})
        n = sum(1 for r in rows if r["county"] == fips)
        print(f"  {tag}: {len(zips)} ZCTAs, {n} ZIP-code-year rows", flush=True)
    out = CACHE / "zbp_placebo_panel.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    ex = []
    for st in sorted({f[:2] for f in COUNTIES}):
        z = acs(f"zip%20code%20tabulation%20area:*&in=state:{st}", f"zcta_{st}")
        ex.append(z.rename(columns={"zip code tabulation area": "zcta"})[["zcta", "pop", "hisp_share", "mex_share",
                                                                         "mexborn_share"]])
    pd.concat(ex).to_csv(DERIVED / "exposure_zcta_placebo.csv", index=False, lineterminator="\n",
                         float_format="%.6g")
    print(f"wrote {out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
