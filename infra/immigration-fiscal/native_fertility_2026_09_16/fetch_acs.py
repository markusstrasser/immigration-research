"""Fetch ACS 1-year CBSA-level tables for the native-fertility crowd-out test.

B13008 gives women 15-50 with/without a birth in the past 12 months by nativity --
the native birth rate numerator and denominator at metro geography, which the PUMS
`tabulate` endpoint refuses (it accepts only state and PUMA hierarchies).
"""
import json, os, pathlib, time, urllib.request, urllib.error

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")
CBSA = "metropolitan%20statistical%20area/micropolitan%20statistical%20area:*"

GROUPS = {
    2023: ["B13008", "B05012", "B25064", "B19013", "B03002", "B25003", "B01001",
           "B15003", "B05004", "B05006"],
    2010: ["B13008", "B05012", "B25064", "B19013", "B03002", "B25003", "B01001",
           "B15002", "B05004", "B05006"],
}


def fetch(year: str, dataset: str, group: str, geo: str = CBSA, tag: str = "cbsa"):
    out = CACHE / f"{dataset.replace('/','_')}_{year}_{group}_{tag}.json"
    if out.exists():
        return json.loads(out.read_text())
    url = (f"https://api.census.gov/data/{year}/{dataset}"
           f"?get=NAME,group({group})&for={geo}&key={KEY}")
    for attempt in range(4):
        try:
            raw = urllib.request.urlopen(url, timeout=300).read()
            break
        except (urllib.error.HTTPError, urllib.error.URLError, ConnectionError, OSError) as e:
            if attempt == 3:
                raise
            print(f"  retry {attempt+1} after {type(e).__name__}")
            time.sleep(8 * (attempt + 1))
    out.write_bytes(raw)
    print(f"  fetched {out.name} ({len(raw)/1e6:.1f} MB)")
    return json.loads(raw)


if __name__ == "__main__":
    for year, groups in GROUPS.items():
        for g in groups:
            print(f"{year} {g}")
            d = fetch(str(year), "acs/acs1", g)
            print(f"  rows={len(d)-1} cols={len(d[0])}")
            time.sleep(1)
    # national validation pulls
    for year in (2010, 2023):
        for g in ("B13008", "B05012"):
            fetch(str(year), "acs/acs1", g, geo="us:1", tag="us")
    print("done")
