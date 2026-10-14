"""Parse pinned FHWA/Oregon highway shares; offline by default, --acquire to fetch.

No source numbers are typed here. V-21 reuses the existing road lane's pinned
transcription, explicitly labeled. New sources are parsed as HTML/XLSX/PDF.
Timing/RSS are diagnostic stdout only, so output JSON is byte-reproducible.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import resource
import shutil
import subprocess
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader
import openpyxl

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "roads_mileage_key_2026_09_29"
PINS = HERE / "inputs/highways_pins.json"
SOURCES = {
    "v21": {"file": "highway_hcas_v21.gif", "local": OLD / "_cache/hcas_table_v21.gif",
            "url": "https://web.archive.org/web/2016id_/http://www.fhwa.dot.gov/policy/hcas/final/five/img27.gif"},
    "addendum": {"file": "highway_hcas_addendum.html", "local": OLD / "_cache/hcas_addendum.cfm.html",
                 "url": "https://www.fhwa.dot.gov/policy/hcas/addendum.cfm"},
    "vm2024": {"file": "highway_vm1_2024.xlsx",
               "url": "https://www.fhwa.dot.gov/policyinformation/statistics/2024/xls/vm1.xlsx"},
    "oregon": {"file": "highway_oregon_2025_27_corrected.pdf",
               "url": "https://www.oregon.gov/das/oea/Documents/ECONW-HCAS-Cost-Allocation-Study-2025-27-Corrected.pdf"},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError("[BLOCKED] " + detail)


def source_files(acquire: bool) -> dict[str, Path]:
    cached = HERE / "_cache"
    cached.mkdir(exist_ok=True)
    pins = json.loads(PINS.read_text()) if PINS.exists() else None
    require(pins is not None or acquire, "missing pins; first run requires --acquire")
    paths = {}
    for name, spec in SOURCES.items():
        dest = cached / spec["file"]
        if not dest.exists() and acquire:
            if "local" in spec:
                shutil.copyfile(spec["local"], dest)
            else:
                # System curl uses the host trust store; uv Python's OpenSSL
                # trust roots do not trust this machine's network certificate.
                # Verification stays on; HTTP and transport failures stop loud.
                data = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--location",
                                       "--connect-timeout", "15", "--max-time", "45", spec["url"]],
                                      check=True, capture_output=True).stdout
                require(len(data) > 1000, "source is unexpectedly small: " + name)
                dest.write_bytes(data)
        require(dest.exists(), "missing cached source: " + str(dest))
        if pins:
            require(sha(dest) == pins["sources"][name]["sha256"], "source hash mismatch: " + name)
        paths[name] = dest
    if pins is None:
        pins = {"sources": {name: {"path": "_cache/" + SOURCES[name]["file"],
                                   "url": SOURCES[name]["url"], "sha256": sha(path)}
                            for name, path in paths.items()},
                "legacy_table": {"path": "../roads_mileage_key_2026_09_29/derived/hcas_v21.csv",
                                 "sha256": sha(OLD / "derived/hcas_v21.csv")}}
        PINS.parent.mkdir(exist_ok=True)
        PINS.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    require(sha(OLD / "derived/hcas_v21.csv") == pins["legacy_table"]["sha256"],
            "legacy positive-control table changed")
    return paths


def v21(path: Path) -> dict:
    legacy = list(csv.DictReader((OLD / "derived/hcas_v21.csv").open()))
    parsed = []
    for row in legacy:
        values = [int(row[k]) for k in ("federal_m", "state_m", "local_m", "total_m")]
        require(abs(sum(values[:3])-values[3]) <= 2, "V-21 printed-rounded row closure")
        parsed.append(dict(vehicle_class=row["vehicle_class"], responsibility=row["responsibility"],
                           **dict(zip(("federal_m", "state_m", "local_m", "total_m"), values))))
    shares = {}
    for column in ("federal_m", "state_m", "local_m", "total_m"):
        total = sum(r[column] for r in parsed)
        freight = sum(r[column] for r in parsed if r["responsibility"] == "freight")
        shares[column] = {"total_m": total, "freight_m": freight, "freight_share": freight / total,
                          "passenger_share": (total-freight) / total}
        require(abs(shares[column]["freight_share"]+shares[column]["passenger_share"]-1) < 1e-12,
                "V-21 share closure")
    return {"table": "1997 HCAS V-21 (forecast 2000 program costs)", "rows": parsed, "shares": shares,
            "extraction": "Reused existing road-lane transcription; image visually checked and hash-pinned, not an independent machine extraction.",
            "gate": "Existing transcription hash and cross-level row closure"}


def addendum(path: Path) -> dict:
    soup = BeautifulSoup(path.read_text(), "html.parser")
    table = next(t for t in soup.find_all("table") if "2000 Federal Cost Responsibility by Vehicle Class Under TEA-21" in t.get_text())
    rows = []
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
        if len(cells) == 4 and cells[1].startswith("$"):
            rows.append({"vehicle_class": cells[0], "cost_m": int(cells[1][1:].replace(",", "")),
                         "cents_per_mile": float(cells[2]), "printed_share": float(cells[3].strip("%"))/100})
    by = {r["vehicle_class"]: r for r in rows}
    total = by["All Revenues"]["cost_m"]
    trucks = by["All Trucks"]["cost_m"]
    require(trucks + by["All Passenger Vehicles"]["cost_m"] == total, "addendum exact cost closure")
    require(by["All Single Units"]["cost_m"] + by["All Combinations"]["cost_m"] == trucks, "addendum truck closure")
    return {"table": "May 2000 addendum Table 4, federal TEA-21 forecast program costs", "rows": rows,
            "freight_share": trucks / total, "passenger_share": 1-trucks/total}


def vm1(path: Path) -> dict:
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = list(book.active.values)
    book.close()
    results = {}
    for i, row in enumerate(rows):
        if any(isinstance(v, str) and "Total Rural and Urban" in v for v in row):
            for source_row in (row, rows[i+1]):
                values = [v for v in source_row if isinstance(v, (int, float))]
                require(len(values) == 10 and values[0] in (2023, 2024), "VM-1 national row shape/year")
                year, short, motorcycles, buses, long, single, combination, light, trucks, total = values
                # Workbook retains unrounded estimates: closure is tight, not a
                # tolerance justified by the separately rounded HTML display.
                require(abs(single+combination-trucks) < 1e-6 and abs(short+long-light) < 1e-6,
                        "VM-1 unrounded subtotal closure")
                require(abs(light+motorcycles+buses+trucks-total) < 1e-6, "VM-1 unrounded national closure")
                results[str(year)] = {"single_unit_vmt_m": single, "combination_vmt_m": combination,
                                     "truck_vmt_m": trucks, "all_vmt_m": total,
                                     "truck_vmt_share": trucks/total, "light_duty_vmt_m": light}
    require(set(results) == {"2023", "2024"}, "VM-1 must contain both national years")
    return {"table": "Highway Statistics 2024 VM-1, latest HPMS national VMT (2023 and 2024)", "years": results,
            "definition": "Single-unit 2-axle 6-tire or more and combination trucks. Light duty includes pickups, vans and SUVs regardless of private/business use."}


def oregon(path: Path) -> dict:
    reader = PdfReader(path)
    page = next(p.extract_text() for p in reader.pages if "full-fee-paying light vehicles are responsible" in p.extract_text())
    m = re.search(r"full-fee-paying light vehicles are responsible for\s+([\d.]+) percent.*?heavy vehicles.*?responsible for\s+([\d.]+) percent", page, re.S)
    require(m is not None, "Oregon corrected summary cost shares")
    light, heavy = (float(s)/100 for s in m.groups())
    require(abs(light+heavy-1) < 1e-12, "Oregon cost share closure")
    return {"table": "Corrected May 28 2025 Oregon HCAS, 2025-2027 biennium, summary page 7",
            "light_cost_share": light, "heavy_cost_share": heavy,
            "scope": "Full-fee-paying vehicles; heavy >10,000 pounds. Forecast cost responsibility, state/local program mix; not observed national business-use share."}


def main() -> None:
    start = time.perf_counter()
    ap = argparse.ArgumentParser()
    ap.add_argument("--acquire", action="store_true")
    ap.add_argument("--out-dir", type=Path, default=HERE / "inputs")
    args = ap.parse_args()
    paths = source_files(args.acquire)
    doc = {"hcas_v21": v21(paths["v21"]), "hcas_addendum_federal": addendum(paths["addendum"]),
           "vm1": vm1(paths["vm2024"]), "oregon_corrected": oregon(paths["oregon"]),
           "gates": {"source_hashes": True, "v21_legacy_positive_control": True,
                     "cost_shares_close": True, "vm1_unrounded_national_subtotals_close_at_1e_6_miles_m": True},
           "source_pins": json.loads(PINS.read_text())}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "highway_shares.json").write_text(json.dumps(doc, indent=2, sort_keys=True)+"\n")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_gb = rss / (1024**3 if sys.platform == "darwin" else 1024**2)
    require(rss_gb < 2.5, "RSS exceeded 2.5GB")
    print(f"PASS highway primary-source gates; seconds={time.perf_counter()-start:.3f}; peak_rss_gb={rss_gb:.6f}")


if __name__ == "__main__":
    main()
