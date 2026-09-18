"""Independent check on the arm-4 child ratio using CPS ASEC parent birthplace.

CPS carries mother's and father's country of birth (PEMNTVTY / PEFNTVTY, Mexico = 303), so
'US-born child under 18 of a Mexico-born parent' is exact, with no household proxy. Pooled over
several ASEC years for state-level sample; state cells stay thin, so the national ratio is the
number that matters for the cross-check.
"""
import json
import os
import time
import urllib.request
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
KEY = os.environ["CENSUS_API_KEY"]
YEARS = (2019,)  # one ASEC year: the Census CPS endpoint is slow, and 2019 is the
                 # pre-COVID year closest to the April 2020 apportionment
MEXICO = "303"
FIPS = [f"{i:02d}" for i in
        [1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
         29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51,
         53, 54, 55, 56]]
VARS = "A_AGE,PENATVTY,PEMNTVTY,PEFNTVTY,MARSUPWT,GESTFIPS"


def fetch(year, st):
    p = CACHE / f"asec_{year}_{st}.json"
    if not p.exists():
        url = (f"https://api.census.gov/data/{year}/cps/asec/mar?get={VARS}"
               f"&for=state:{st}&key={KEY}")
        for attempt in range(5):
            try:
                with urllib.request.urlopen(url, timeout=180) as r:
                    p.write_bytes(r.read())
                break
            except Exception as e:  # noqa: BLE001
                print(f"    retry {attempt} {year}/{st}: {e}", flush=True)
                time.sleep(2 * (attempt + 1))
        else:
            raise RuntimeError(f"failed {year}/{st}")
    return json.loads(p.read_text())


if __name__ == "__main__":
    frames = []
    for year in YEARS:
        for i, st in enumerate(FIPS):
            rows = fetch(year, st)
            d = pd.DataFrame(rows[1:], columns=rows[0])
            d["year"] = year
            frames.append(d)
            if i % 10 == 0:
                print(f"  {year} {i}/{len(FIPS)}", flush=True)
    d = pd.concat(frames, ignore_index=True)
    for c in ("A_AGE", "MARSUPWT"):
        d[c] = pd.to_numeric(d[c])
    d["MARSUPWT"] /= 100.0  # ASEC supplement weight carries two implied decimals
    d["mex_born"] = d["PENATVTY"] == MEXICO
    d["us_born"] = d["PENATVTY"].isin(["57", "60", "66", "69", "73", "78", "96"])
    d["mex_parent"] = (d["PEMNTVTY"] == MEXICO) | (d["PEFNTVTY"] == MEXICO)
    g = d.groupby(["GESTFIPS"])
    out = pd.DataFrame({
        "mexico_born_cps": g.apply(lambda x: x.loc[x.mex_born, "MARSUPWT"].sum() / len(YEARS),
                                   include_groups=False),
        "us_born_kids_mexparent_cps": g.apply(
            lambda x: x.loc[x.us_born & (x.A_AGE < 18) & x.mex_parent, "MARSUPWT"].sum() / len(YEARS),
            include_groups=False),
    }).reset_index()
    out["kids_per_mexborn_cps"] = out.us_born_kids_mexparent_cps / out.mexico_born_cps
    out.to_csv(DERIVED / "kids_cps_ratio.csv", index=False)
    tot_m = out.mexico_born_cps.sum()
    tot_k = out.us_born_kids_mexparent_cps.sum()
    print(f"CPS ASEC {YEARS[0]}-{YEARS[-1]} pooled, annual averages:")
    print(f"  Mexico-born: {tot_m:,.0f}")
    print(f"  US-born under 18 with a Mexico-born parent: {tot_k:,.0f}")
    print(f"  national ratio: {tot_k / tot_m:.3f}")
