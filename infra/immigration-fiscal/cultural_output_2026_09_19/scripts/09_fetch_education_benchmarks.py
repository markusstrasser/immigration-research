#!/usr/bin/env python3
"""Arm B step 2: the population benchmark the awards share is judged against.

For each ACS 1-year vintage, the Hispanic share of (a) the population 25 and
over and (b) the population 25 and over holding a bachelor's degree or higher.
Variable ids are never typed from memory: the script downloads the vintage's
variables.json and selects by label text, printing what it matched.

Tables: C15002I (Hispanic 25+, by sex x attainment) and B15002 (all 25+).
Output: derived/education_benchmarks.csv
"""
import json
import os
import sys
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "census_meta"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)
DER.mkdir(exist_ok=True)

YEARS = [2005, 2010, 2015, 2019, 2023, 2024]
BA_WORDS = ("bachelor's degree", "master's degree", "professional school",
            "doctorate degree")


def variables(year: int) -> dict:
    p = CACHE / f"variables_{year}.json"
    if p.exists():
        return json.loads(p.read_text())
    url = f"https://api.census.gov/data/{year}/acs/acs1/variables.json"
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    if not r.text.lstrip().startswith("{"):
        sys.exit(f"FAIL non-JSON variables.json for {year}")
    data = r.json()["variables"]
    p.write_text(json.dumps(data))
    return data


def pick(vars_: dict, table: str, want_ba: bool) -> list:
    """Estimate variables in `table` whose label is a BA-or-higher category
    (want_ba) or the table total (not want_ba)."""
    out = []
    for name, meta in vars_.items():
        if not name.startswith(table + "_") or not name.endswith("E"):
            continue
        label = meta.get("label", "").lower()
        if want_ba:
            if any(w in label for w in BA_WORDS):
                out.append(name)
        else:
            if label.rstrip("!:").endswith("total") or label in (
                    "estimate!!total:", "estimate!!total"):
                out.append(name)
    return sorted(out)


def fetch(year: int, names: list, key: str) -> dict:
    url = f"https://api.census.gov/data/{year}/acs/acs1"
    got = {}
    for i in range(0, len(names), 45):
        chunk = names[i:i + 45]
        r = requests.get(url, params={"get": ",".join(chunk), "for": "us:1",
                                      "key": key}, timeout=180)
        r.raise_for_status()
        if not r.text.lstrip().startswith("["):
            sys.exit(f"FAIL non-JSON body for {year}: {r.text[:200]!r}")
        rows = r.json()
        got.update({k: v for k, v in zip(rows[0], rows[1]) if k in chunk})
    return got


def main() -> None:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("CENSUS_API_KEY not set; source config.local.env")
    recs = []
    for year in YEARS:
        try:
            vars_ = variables(year)
        except Exception as exc:  # noqa: BLE001
            print(f"{year}: variables fetch failed {exc!r}", flush=True)
            continue
        hisp_ba = pick(vars_, "C15002I", True)
        hisp_tot = pick(vars_, "C15002I", False)
        all_ba = pick(vars_, "B15002", True)
        all_tot = pick(vars_, "B15002", False)
        if not (hisp_ba and hisp_tot and all_ba and all_tot):
            print(f"{year}: table variables not found "
                  f"(hisp_ba={len(hisp_ba)} all_ba={len(all_ba)})", flush=True)
            continue
        vals = fetch(year, hisp_ba + hisp_tot + all_ba + all_tot, key)
        num = {k: float(v) for k, v in vals.items() if v is not None}
        rec = {
            "year": year,
            "hispanic_25plus": sum(num[v] for v in hisp_tot),
            "hispanic_ba_plus": sum(num[v] for v in hisp_ba),
            "all_25plus": sum(num[v] for v in all_tot),
            "all_ba_plus": sum(num[v] for v in all_ba),
            "hisp_ba_vars": len(hisp_ba),
            "all_ba_vars": len(all_ba),
        }
        rec["hispanic_share_25plus"] = rec["hispanic_25plus"] / rec["all_25plus"]
        rec["hispanic_share_ba_plus"] = (rec["hispanic_ba_plus"]
                                         / rec["all_ba_plus"])
        # content validation against a known anchor: the Hispanic share of US
        # adults 25+ runs from roughly 11% (2005) to 19% (2024)
        if not (0.08 < rec["hispanic_share_25plus"] < 0.24):
            sys.exit(f"FAIL {year} hispanic adult share "
                     f"{rec['hispanic_share_25plus']:.3f} implausible")
        recs.append(rec)
        print(f"{year}: hispanic 25+ {rec['hispanic_share_25plus']:.3f}, "
              f"of BA+ {rec['hispanic_share_ba_plus']:.3f} "
              f"({len(hisp_ba)} hisp BA vars, {len(all_ba)} all BA vars)",
              flush=True)
    if not recs:
        sys.exit("FAIL no benchmark years recovered")
    pd.DataFrame(recs).to_csv(DER / "education_benchmarks.csv", index=False)
    print(f"wrote {DER/'education_benchmarks.csv'}", flush=True)


if __name__ == "__main__":
    main()
