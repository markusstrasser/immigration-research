"""Acquire small primary HPMS aggregates, county summaries and ROW design sources.

Native-First: query Socrata's published SQL aggregation endpoint; no national
geometry download or road polygons. Existing response files are kept unchanged.

    uv run --no-project python3 -I {lane}/acquire_roads.py
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "roads"
OUT = HERE / "derived"
BASE = "https://data.transportation.gov"
SECTIONS = "42um-tgh5"
COUNTY = "eq35-vm98"
STATE_CODES = (1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20,
               21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
               37, 38, 39, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56)
FILES = {
    "hpms_county_2024.csv": f"{BASE}/resource/{COUNTY}.csv?$limit=1000000",
    "hpms_county_metadata.json": f"{BASE}/api/views/{COUNTY}.json",
    "hpms_sections_metadata.json": f"{BASE}/api/views/{SECTIONS}.json",
    "hm20.xlsx": "https://www.fhwa.dot.gov/policyinformation/statistics/2024/xls/hm20.xlsx",
    "hpms_2024_readme.md": "https://raw.githubusercontent.com/FHWA/HPMS/2024-HPMS/README_2024_HPMS_All.md",
    "hpms_field_manual04.html": "https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/page04.cfm",
    "hpms_field_manual2024.pdf": "https://www.reginfo.gov/public/do/DownloadDocument?objectID=144173101",
    "ncdot_row.pdf": "https://connect.ncdot.gov/projects/Roadway/Roadway%20Design%20Manual/09.%20Right%20of%20Way.pdf",
    "fhwa_traffic_calming1999.pdf": "https://rosap.ntl.bts.gov/view/dot/42943/dot_42943_DS1.pdf",
}


def fetch(url, dest):
    if not dest.exists():
        tmp = dest.with_suffix(dest.suffix + ".part")
        subprocess.run(["curl", "-sSL", "--fail", "--retry", "3", "--max-time", "115", "-o", str(tmp), url],
                       check=True)
        tmp.rename(dest)
    if dest.stat().st_size == 0 or dest.stat().st_size > 1_000_000_000:
        raise RuntimeError(f"[BLOCKED] invalid road input size: {dest}")
    if dest.suffix == ".pdf" and not dest.read_bytes()[:4] == b"%PDF":
        raise RuntimeError(f"[BLOCKED] expected PDF: {dest}")
    if dest.suffix == ".xlsx" and not dest.read_bytes()[:2] == b"PK":
        raise RuntimeError(f"[BLOCKED] expected XLSX: {dest}")
    return {"path": str(dest.relative_to(HERE)), "url": url, "bytes": dest.stat().st_size,
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}


def acquire_state(code):
    # The county summary supplies all local roads and rural minor collectors.
    # Mainline types 1/2 avoid dual-carriageway non-inventory directions and ramps.
    # Same filters as the FHWA 2024 export README; no geometry in this request.
    query = {
        "$select": "stateid,county_id,f_system,urban_id,ownership,toll_id,through_lanes,"
                   "sum(sectionlength) as miles,count(*) as n",
        "$where": f"stateid={code} AND facility_type in (1,2) AND urban_id>0 "
                  "AND is_restricted is null AND (f_system in (1,2,3,4,5) "
                  "OR (f_system=6 AND urban_id<>99999))",
        "$group": "stateid,county_id,f_system,urban_id,ownership,toll_id,through_lanes",
        "$order": "stateid,county_id,f_system,urban_id,ownership,toll_id,through_lanes",
        "$limit": 100000,
    }
    url = f"{BASE}/resource/{SECTIONS}.json?{urlencode(query)}"
    dest = CACHE / f"sections_{code:02d}_2024.json"
    row = fetch(url, dest)
    data = json.loads(dest.read_text())
    if not isinstance(data, list) or not data or len(data) >= query["$limit"]:
        raise RuntimeError(f"[BLOCKED] missing/truncated state {code}: {str(data)[:200]}")
    if any(not all(k in x for k in ("stateid", "f_system", "miles")) for x in data):
        raise RuntimeError(f"[BLOCKED] malformed state {code}")
    print(f"roads: state {code:02d}: {len(data):,} groups, "
          f"{sum(float(x['miles']) for x in data):,.1f} mainline miles", flush=True)
    return row


def main():
    start = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    sources = [fetch(url, CACHE / name) for name, url in FILES.items()]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(acquire_state, code): code for code in STATE_CODES}
        for future in as_completed(futures):
            sources.append(future.result())
    sources.sort(key=lambda x: x["path"])
    (OUT / "roads_sources.json").write_text(json.dumps(sources, indent=2, sort_keys=True) + "\n")
    if sum(p.stat().st_size for p in CACHE.rglob("*") if p.is_file()) > 1_000_000_000:
        raise RuntimeError("[BLOCKED] roads cache exceeds 1 GB")
    print(f"roads acquired: {len(sources)} primary files; {time.perf_counter()-start:.1f}s; "
          f"maxrss_raw={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
