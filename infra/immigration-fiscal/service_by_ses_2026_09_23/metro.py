"""Metro-size class for each 2020-vintage PUMA, from a population-weighted Geocorr crosswalk.

ACS PUMS carries state and PUMA but no metro field. Geocorr 2022 (Missouri Census Data Center)
splits each 2020 PUMA across 2023 CBSAs by 2020 Census population; the July 2023 OMB delineation
(Census list 1) says which CBSAs are metropolitan. CBSA size is the sum of its PUMA pieces'
2020 population. Classes: metro of 5 million or more, metro of 1-5 million, metro under 1 million,
and non-metro (micropolitan or outside any CBSA). A PUMA takes the class holding most of its
population; `dominant_share` records how clean that assignment is.

Writes `_cache/xwalk_puma22_cbsa23.csv` (raw) and `derived/puma_metro_size.csv`.
"""
import csv
import io
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
BROKER = "https://mcdc.missouri.edu/cgi-bin/broker"
DELINEATION = ("https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/"
               "2023/delineation-files/list1_2023.xlsx")
STATES = ['Al01', 'Ak02', 'Az04', 'Ar05', 'Ca06', 'Co08', 'Ct09', 'De10', 'Dc11', 'Fl12', 'Ga13',
          'Hi15', 'Id16', 'Il17', 'In18', 'Ia19', 'Ks20', 'Ky21', 'La22', 'Me23', 'Md24', 'Ma25',
          'Mi26', 'Mn27', 'Ms28', 'Mo29', 'Mt30', 'Ne31', 'Nv32', 'Nh33', 'Nj34', 'Nm35', 'Ny36',
          'Nc37', 'Nd38', 'Oh39', 'Ok40', 'Or41', 'Pa42', 'Ri44', 'Sc45', 'Sd46', 'Tn47', 'Tx48',
          'Ut49', 'Vt50', 'Va51', 'Wa53', 'Wv54', 'Wi55', 'Wy56']
BLANKS = ("title", "oropt", "counties", "metros", "uaucs", "places", "latitude", "longitude",
          "locname", "distance", "nrings", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9",
          "r10", "lathi", "latlo", "longhi", "longlo")
CLASSES = ("metro_5m_plus", "metro_1m_5m", "metro_under_1m", "non_metro")


def geocorr_state(state, tries=3):
    query = {"_PROGRAM": "apps.geocorr2022.sas", "_SERVICE": "MCDC_long", "_debug": "0",
             "state": state, "g1_": "puma22", "g2_": "cbsa23", "wtvar": "pop20", "nozerob": "1",
             "csvout": "1", "fileout": "1", "filefmt": "csv", "lstfmt": "txt", "namoptf": "b",
             "namoptr": "b", "kiloms": "0", **{k: "" for k in BLANKS}}
    url = BROKER + "?" + urllib.parse.urlencode(query)
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as response:
                html = response.read().decode("utf-8", "replace")
            match = re.search(r'"\s*(/temp/geocorr\w*_[^"\s]+\.csv)\s*"', html)
            if not match:
                raise RuntimeError(f"no csv link for {state}")
            with urllib.request.urlopen("https://mcdc.missouri.edu" + match.group(1), timeout=300) as response:
                return response.read().decode("utf-8", "replace")
        except Exception as error:  # noqa: BLE001 - retried, then raised
            if attempt == tries - 1:
                raise
            print(f"  ! {state}: {type(error).__name__}, retrying", flush=True)
            time.sleep(5)


def crosswalk():
    target = CACHE / "xwalk_puma22_cbsa23.csv"
    if not target.exists():
        rows = []
        for state in STATES:
            reader = csv.DictReader(io.StringIO(geocorr_state(state)))
            next(reader)  # second header line holds labels
            rows.extend(reader)
            print(f"  . geocorr {state}: {len(rows)} rows", flush=True)
            time.sleep(1)
        with target.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    with target.open() as handle:
        return list(csv.DictReader(handle))


def metro_cbsas():
    target = CACHE / "list1_2023.xlsx"
    if not target.exists():
        urllib.request.urlretrieve(DELINEATION, target)
    sheet = openpyxl.load_workbook(target, read_only=True).active
    kinds = {}
    for row in sheet.iter_rows(min_row=4, values_only=True):
        if row[0] and row[4]:
            kinds[str(row[0])] = row[4]
    return {code for code, kind in kinds.items() if kind.startswith("Metropolitan")}, kinds


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    rows = crosswalk()
    metros, kinds = metro_cbsas()
    size = defaultdict(float)
    for row in rows:
        size[row["cbsa23"].strip()] += float(row["pop20"])
    unknown = {row["cbsa23"].strip() for row in rows} - set(kinds) - {"99999"}
    assert not unknown, f"CBSA codes missing from the delineation: {sorted(unknown)[:10]}"

    def size_class(code):
        if code not in metros:
            return "non_metro"
        return "metro_5m_plus" if size[code] >= 5e6 else "metro_1m_5m" if size[code] >= 1e6 else "metro_under_1m"

    by_puma = defaultdict(lambda: defaultdict(float))
    for row in rows:
        by_puma[(int(row["state"]), int(row["puma22"]))][size_class(row["cbsa23"].strip())] += float(row["pop20"])
    out = []
    for (state, puma), pops in sorted(by_puma.items()):
        total = sum(pops.values())
        dominant = max(CLASSES, key=lambda c: pops.get(c, 0.0))
        out.append({"st": state, "puma": puma, "metro_size": dominant, "pop20": round(total),
                    "dominant_share": round(pops[dominant] / total, 4),
                    **{f"share_{c}": round(pops.get(c, 0.0) / total, 4) for c in CLASSES}})
    with open(DERIVED / "puma_metro_size.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    total = sum(r["pop20"] for r in out)
    print(f"  ✓ {len(out)} PUMAs, 2020 population {total:,.0f}")
    for c in CLASSES:
        pop = sum(r["pop20"] for r in out if r["metro_size"] == c)
        print(f"    {c:16s} {sum(r['metro_size'] == c for r in out):5d} PUMAs {pop / total:6.1%} of population")
    mixed = sum(r["pop20"] for r in out if r["dominant_share"] < 0.8)
    print(f"    population in PUMAs whose class covers <80%: {mixed / total:.1%}")


if __name__ == "__main__":
    sys.exit(main())
