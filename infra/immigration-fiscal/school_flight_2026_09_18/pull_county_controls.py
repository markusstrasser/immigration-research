"""County elderly share and median household income for the Poterba-style control.

2000 from Census 2000 SF1 (P012, age-sex counts); 2010/2015/2019/2020 from the ACS
5-year subject table S0101 (age) and B19013 (median household income). County is the
finest geography that covers every district year in the panel; districts are mapped
to counties by the CCD directory's county_code.
"""
import json, os, pathlib, urllib.parse, urllib.request, csv, time

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
CACHE.mkdir(exist_ok=True)
KEY = os.environ.get("CENSUS_API_KEY", "")


def api(url, tries=4):
    last = None
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=180) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            last = e
            time.sleep(4)
    raise RuntimeError(f"{url[:140]} :: {last}")


def q(base, get, extra=None):
    d = {"get": get, "for": "county:*", "in": "state:*"}
    d.update(extra or {})
    if KEY:
        d["key"] = KEY
    return api(base + "?" + urllib.parse.urlencode(d))


def acs5(year):
    """65+ share and median household income from ACS 5-year."""
    # B01001: total 001; male 65+ = 020..025; female 65+ = 044..049
    old = [f"B01001_{i:03d}E" for i in list(range(20, 26)) + list(range(44, 50))]
    cols = ["B01001_001E"] + old + ["B19013_001E"]
    d = q(f"https://api.census.gov/data/{year}/acs/acs5", ",".join(cols))
    hdr, rows = d[0], d[1:]
    ix = {c: i for i, c in enumerate(hdr)}
    out = []
    for r in rows:
        def n(c):
            try:
                v = float(r[ix[c]])
                return v if v > -1e8 else None
            except (TypeError, ValueError):
                return None
        tot = n("B01001_001E")
        vals = [n(c) for c in old]
        e65 = None if any(v is None for v in vals) else sum(vals)
        mhi = n("B19013_001E")
        cof = r[ix["state"]].zfill(2) + r[ix["county"]].zfill(3)
        out.append({"year": year, "cofips": cof, "pop": tot,
                    "pop65": e65,
                    "share65": (e65 / tot) if (tot and e65 is not None and tot > 0) else None,
                    "mhi": mhi})
    return out


def sf1_2000():
    old_m = [f"P012{i:03d}" for i in range(20, 26)]
    old_f = [f"P012{i:03d}" for i in range(44, 50)]
    cols = ["P012001"] + old_m + old_f
    d = q("https://api.census.gov/data/2000/dec/sf1", ",".join(cols))
    hdr, rows = d[0], d[1:]
    ix = {c: i for i, c in enumerate(hdr)}
    out = []
    for r in rows:
        f = lambda c: float(r[ix[c]])
        tot = f("P012001")
        e65 = sum(f(c) for c in old_m + old_f)
        cof = r[ix["state"]].zfill(2) + r[ix["county"]].zfill(3)
        out.append({"year": 2000, "cofips": cof, "pop": tot, "pop65": e65,
                    "share65": e65 / tot if tot else None, "mhi": None})
    return out


def main():
    rows = sf1_2000()
    print("2000 sf1 counties", len(rows), flush=True)
    for y in (2010, 2015, 2019, 2020):
        r = acs5(y)
        print(y, "acs5 counties", len(r), flush=True)
        rows += r
    # 2005 has no ACS 5-year; the 2000 SF1 value is carried for the 2005 wave and flagged
    for r in [dict(x, year=2005, carried_from_2000=1) for x in rows if x["year"] == 2000]:
        rows.append(r)
    cols = ["year", "cofips", "pop", "pop65", "share65", "mhi", "carried_from_2000"]
    with (CACHE / "county_controls.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)
    print("wrote county_controls.csv", len(rows))


if __name__ == "__main__":
    main()
