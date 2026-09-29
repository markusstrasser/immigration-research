#!/usr/bin/env python3
"""Measured inputs the comparators' back-cast needs beyond the debt lane's; writes derived/acs_inputs.csv.

1. Relative per-capita income of non-Hispanic whites, 2008-2024: ACS 1-year Selected Population Profile (S0201),
   POPGROUP 451 "White alone, not Hispanic or Latino" against 001 "Total population" -- the same table, labels and
   resolution the back-cast uses for the Mexican group (`historical_backcast_2026_09_20/pull_acs.py`, LABELS imported),
   with median age for the age-structure bias statement. The ACS has no parent birthplace, so third-plus NH whites
   (A1, 94% of NH whites in the CPS frame) take the NH-white path; only the path relative to 2024 is used.
2. Mexican-origin counts for the pre-2005 windows: Census 2000 SF1 PCT011004 (Hispanic or Latino by specific origin,
   Mexican; 100% data) from the Census API, and 1990 from the Census Bureau's CP-3-3 "Persons of Hispanic Origin in the
   United States", Table 1, p. 4, Mexican, All persons (sample data; the 1990 SF1 is not on the API).

Raw API responses and the CP-3-3 PDF are cached in _cache/ (ignored) and reused; a missing cache file is fetched
with CENSUS_API_KEY (from the environment, else read from acquire/config.local.env; never printed). Every cached
file is pinned by sha256 after the first pull. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run python3 infra/immigration-fiscal/legacy_comparators_2026_09_30/acs_inputs.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
KEY_FILE = FISCAL / "acquire/config.local.env"
# The profile starts in 2008; 2020 has no 1-year release; the back-cast's own pull has no 2010 profile (the endpoint
# answers HTTP 500 for 2010) and interpolates it. Gate below: the back-cast's input has the same years.
YEARS = [y for y in range(2008, 2025) if y not in (2010, 2020)]
GROUPS = {"nh_white": "451", "total": "001"}
CP33_URL = "https://www2.census.gov/library/publications/decennial/1990/cp-3/cp-3-3.pdf"
CP33_SHA = "b965fde31f69e599eceb81eb0d2aac7403d2b0ecea360591edfd6c5c324b67b3"
MEX_1990 = 13_393_208        # CP-3-3 Table 1 (p. 4), Mexican, All persons; gated against the PDF's text below
PINS_FILE = HERE / "acs_inputs_pins.json"


def key() -> str:
    if os.environ.get("CENSUS_API_KEY"):
        return os.environ["CENSUS_API_KEY"]
    for line in KEY_FILE.read_text().splitlines():
        m = re.match(r"\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
        if m:
            return m.group(1)
    raise SystemExit("[BLOCKED] no CENSUS_API_KEY")


def fetch(url: str) -> bytes:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=90) as response:
                return response.read()
        except Exception as error:           # the URL carries the key: report the class only
            last = f"{type(error).__name__} {getattr(error, 'code', '')}"
            time.sleep(3)
    raise SystemExit(f"[BLOCKED] fetch failed: {last}")


def cached(name: str, url_fn) -> bytes:
    path = CACHE / name
    if not path.exists():
        body = fetch(url_fn())
        if not (name.endswith(".pdf") and body.startswith(b"%PDF")):
            try:
                json.loads(body)
            except ValueError:
                raise SystemExit(f"[BLOCKED] {name}: the response is not JSON ({len(body)} bytes); nothing cached")
        CACHE.mkdir(exist_ok=True)
        path.write_bytes(body)
    return path.read_bytes()


def labels_module():
    """pull_acs.LABELS; pull_acs reads CENSUS_API_KEY at import, so a placeholder is set for the import only."""
    sys.path.insert(0, str(FISCAL / "historical_backcast_2026_09_20"))
    had = "CENSUS_API_KEY" in os.environ
    os.environ.setdefault("CENSUS_API_KEY", "placeholder-for-import")
    try:
        import pull_acs  # noqa: E402
    finally:
        if not had:
            del os.environ["CENSUS_API_KEY"]
    return pull_acs.LABELS


def main() -> None:
    labels = labels_module()
    with open(FISCAL / "historical_backcast_2026_09_20/inputs/acs_mexican_origin.csv") as f:
        have = [int(r["year"]) for r in csv.DictReader(f) if r["per_capita_income_mexican"]]
    if have != YEARS:
        raise SystemExit(f"[BLOCKED] the back-cast's profile years {have} are not this pull's {YEARS}")
    rows, raw_files = [], {}
    for year in YEARS:
        base = f"https://api.census.gov/data/{year}/acs/acs1/spp"
        meta = json.loads(cached(f"spp_{year}_variables.json", lambda: base + "/variables.json"))
        codes = {}
        for code, entry in sorted(meta["variables"].items()):
            if re.fullmatch(r"S0201_\d+E", code):
                for name, pattern in labels.items():
                    if name not in codes and re.search(pattern, entry.get("label", ""), re.I):
                        codes[name] = code
        for name in ("per_capita_income", "median_age"):
            if name not in codes:
                raise SystemExit(f"[BLOCKED] {year}: no S0201 variable for {name}")
        popgroups = json.loads(cached(f"spp_{year}_popgroup.json", lambda: base + "/variables/POPGROUP.json"))
        items = popgroups["values"]["item"]
        if not items.get("451", "").startswith("White alone, not Hispanic or Latino") or items.get("001") != "Total population":
            raise SystemExit(f"[BLOCKED] {year}: POPGROUP 451/001 labels changed")
        row = dict(year=year)
        for tag, group in GROUPS.items():
            name = f"spp_{year}_{group}.json"
            body = json.loads(cached(name, lambda: f"{base}?get={codes['per_capita_income']},{codes['median_age']}"
                                                   f"&for=us:1&POPGROUP={group}&key={key()}"))
            raw_files[name] = hashlib.sha256((CACHE / name).read_bytes()).hexdigest()
            header, values = body
            row[f"per_capita_income_{tag}"] = float(values[header.index(codes["per_capita_income"])])
            row[f"median_age_{tag}"] = float(values[header.index(codes["median_age"])])
        row["relative_per_capita_income_nh_white"] = row["per_capita_income_nh_white"] / row["per_capita_income_total"]
        rows.append(row)
    body = json.loads(cached("sf1_2000_pct011.json",
                             lambda: f"https://api.census.gov/data/2000/dec/sf1?get=PCT011001,PCT011004&for=us:1&key={key()}"))
    raw_files["sf1_2000_pct011.json"] = hashlib.sha256((CACHE / "sf1_2000_pct011.json").read_bytes()).hexdigest()
    mex_2000 = int(body[1][body[0].index("PCT011004")])
    total_2000 = int(body[1][body[0].index("PCT011001")])
    pdf = cached("cp-3-3.pdf", lambda: CP33_URL)
    if hashlib.sha256(pdf).hexdigest() != CP33_SHA:
        raise SystemExit("[BLOCKED] _cache/cp-3-3.pdf is not the pinned CP-3-3")
    text = subprocess.run(["pdftotext", "-layout", "-f", "18", "-l", "18", str(CACHE / "cp-3-3.pdf"), "-"],
                          capture_output=True, text=True, check=True).stdout
    table = text[text.index("Mexican"):]
    got = re.search(r"All persons -+\s+([\d ]+?)\s{2,}", table)
    if not got or int(got.group(1).replace(" ", "")) != MEX_1990:
        raise SystemExit("[BLOCKED] CP-3-3 p. 4 does not give the pinned 1990 Mexican count")
    pins = json.loads(PINS_FILE.read_text()) if PINS_FILE.exists() else None
    if pins is None:
        PINS_FILE.write_text(json.dumps(raw_files, indent=1, sort_keys=True) + "\n")
    elif pins != raw_files:
        raise SystemExit("[BLOCKED] cached API responses differ from acs_inputs_pins.json")
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    fields = list(rows[0])
    with open(out / "acs_inputs.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["series", "year", "value", "source"])
        for r in rows:
            for k in fields[1:]:
                src = ("ACS 1-year S0201 POPGROUP " + (GROUPS["nh_white"] if k.endswith("nh_white") else GROUPS["total"])
                       if not k.startswith("relative") else "CALCULATION: 451 / 001")
                w.writerow([k, r["year"], f"{r[k]:.6f}", src])
        w.writerow(["mexican_origin_count", 2000, mex_2000, "Census 2000 SF1 PCT011004 (Census API)"])
        w.writerow(["total_population_census", 2000, total_2000, "Census 2000 SF1 PCT011001 (Census API)"])
        w.writerow(["mexican_origin_count", 1990, MEX_1990, "1990 CP-3-3 Table 1 (printed p. 4, PDF p. 18), Mexican, All persons (sample)"])
    for r in rows:
        print(f"  {r['year']}: NH white relative per-capita income {r['relative_per_capita_income_nh_white']:.4f}, "
              f"median age {r['median_age_nh_white']:.1f} vs {r['median_age_total']:.1f}")
    print(f"  Mexican origin: 1990 {MEX_1990:,}, 2000 {mex_2000:,}")
    print("[written] derived/acs_inputs.csv")


if __name__ == "__main__":
    main()
