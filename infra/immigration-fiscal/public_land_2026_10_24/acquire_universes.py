"""Acquire ownership inventories, with bounded ArcGIS paging and source hashes.

Native-First: curl downloads and ArcGIS REST paging; no browser or new dependency.
Run: uv run --no-project python3 -I {lane}/acquire_universes.py
"""
from __future__ import annotations

import hashlib
import json
import resource
import subprocess
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "universes"
OUT = HERE / "derived"
ROOT = HERE.parents[2]
LOCAL_IPEDS = HERE.parent / "affirmative_action_cost_2026_09_24" / "_cache" / "ipeds" / "HD2023.csv"
SERVICES = {
    "hifld_hospitals": (
        "https://services.arcgis.com/XG15cJAlne2vxtgt/arcgis/rest/services/Hospitals_RAPT/FeatureServer/6",
        "FID", "ID,NAME,STATE,COUNTYFIPS,LATITUDE,LONGITUDE,OWNER,TYPE,STATUS,SOURCE,SOURCEDATE,VAL_DATE,BEDS",
    ),
    "hud_developments": (
        "https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/Public_Housing_Developments/FeatureServer/0",
        "OBJECTID", "DEVELOPMENT_CODE,PROJECT_NAME,SCATTERED_SITE_IND,PD_STATUS_TYPE_CODE,TOTAL_UNITS,LAT,LON,LVL2KX,STATE2KX,CNTY2KX,CURCNTY,STD_ST,LAST_UPDT_DTTM",
    ),
    "faa_bts_airports": (
        "https://services.arcgis.com/xOi1kZaI0eWDREZv/ArcGIS/rest/services/NTAD_Aviation_Facilities/FeatureServer/0",
        "OBJECTID", "SITE_NO,EFF_DATE,SITE_TYPE_CODE,STATE_CODE,ARPT_ID,ARPT_NAME,OWNERSHIP_TYPE_CODE,FACILITY_USE_CODE,LAT_DECIMAL,LONG_DECIMAL,ACREAGE,ARPT_STATUS,COUNTY_NAME,COUNTRY_CODE",
    ),
}
FILES = {
    "cms_hospital_general.csv": "https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0/download?format=csv",
    "cms_hospital_dictionary.pdf": "https://data.cms.gov/provider-data/sites/default/files/data_dictionaries/HospitalCompare-DataDictionary.pdf",
    "ipeds_hd2023_dictionary.zip": "https://nces.ed.gov/ipeds/datacenter/data/HD2023_Dict.zip",
    "faa_txt_csv_mapping.pdf": "https://nfdc.faa.gov/webContent/28DaySub/TXT_to_CSV_Mapping.pdf",
    "faa_bts_dictionary.xlsx": "https://doi.org/10.21949/1529011",
    "faa_bts_metadata.xml": "https://www.arcgis.com/sharing/rest/content/items/1551114f78e34d8395fd77bf41cd8a80/info/metadata/metadata.xml",
    "hud_item.json": "https://www.arcgis.com/sharing/rest/content/items/5c96143f79c940a0a8cedae99a1ac562?f=json",
    "hifld_fema_item.json": "https://www.arcgis.com/sharing/rest/content/items/c4b621eb03ca4f78a05d9063629e98bf?f=json",
    "scope_service_academies_gao.html": "https://files.gao.gov/reports/GAO-26-107049/index.html",
    "scope_nps_about.html": "https://nps.edu/web/guest/about",
    "scope_afit_about.html": "https://www.afit.edu/ABOUT/",
    "scope_bie_colleges.html": "https://www.bie.edu/news-article/bureau-indian-education-offers-postsecondary-opportunities",
    "scope_iaia_4411.html": "https://www.govinfo.gov/content/pkg/USCODE-2024-title20/html/USCODE-2024-title20-chap56-subchapI-sec4411.htm",
    "scope_iaia_4412.html": "https://www.govinfo.gov/content/pkg/USCODE-2024-title20/html/USCODE-2024-title20-chap56-subchapI-sec4412.htm",
    "scope_bea_tribal_gce2005.pdf": "https://apps.bea.gov/scb/pdf/2005/10October/1005_gce.pdf",
}


def airport_dictionary():
    """Read the BTS primary XLSX, guarding ownership/use confusion and acreage units."""
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(CACHE / "faa_bts_dictionary.xlsx") as book:
        strings = ["".join(x.itertext()) for x in ET.fromstring(book.read("xl/sharedStrings.xml")).findall("s:si", ns)]
        table = []
        for r in ET.fromstring(book.read("xl/worksheets/sheet1.xml")).findall("s:sheetData/s:row", ns):
            cells = {}
            for c in r.findall("s:c", ns):
                v = c.find("s:v", ns)
                if v is not None and v.text is not None:
                    cells["".join(ch for ch in c.attrib["r"] if ch.isalpha())] = strings[int(v.text)] if c.get("t") == "s" else v.text
            table.append(cells)
    current = ""
    ownership = {}
    units = ""
    for r in table:
        if r.get("A", "").strip():
            current = r["A"]
        if current == "OWNERSHIP_TYPE_CODE" and r.get("E", "").strip():
            ownership[r["E"]] = r.get("F", "")
        if current == "ACREAGE":
            units = r.get("L", "")
    if ownership.get("PU") != "Publicly owned" or units != "acre":
        raise RuntimeError(f"[BLOCKED] airport primary codebook drift: {ownership}, acreage unit={units!r}")
    return {"ownership_codes": ownership, "acreage_unit": units,
            "airport_public_flag": "civil publicly owned PU only; military codes retained in ownership field and excluded from airport-enterprise acreage"}


def fetch(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(path.suffix + ".part")
    try:
        subprocess.run(["curl", "-sSL", "--fail", "--retry", "2", "--max-time", "120", "-o", str(part), url], check=True)
    except subprocess.CalledProcessError as exc:
        if exc.returncode != 35:
            raise
        # macOS curl uses LibreSSL; some primary .edu servers reject its TLS handshake.
        # Retry the identical primary URL using uv Python's OpenSSL, never another source.
        print(f"[DEGRADED] curl TLS handshake failed; Python OpenSSL retries exact primary source {url}")
        with urllib.request.urlopen(url, timeout=60) as response:
            part.write_bytes(response.read())
    if not part.stat().st_size:
        raise RuntimeError(f"[BLOCKED] empty source {url}")
    part.replace(path)


def get_json(url: str) -> dict:
    result = subprocess.run(["curl", "-sSL", "--fail", "--retry", "2", "--max-time", "60", url], capture_output=True, check=True)
    body = json.loads(result.stdout)
    if "error" in body:
        raise RuntimeError(f"[BLOCKED] ArcGIS returned {body['error']} at {url}")
    return body


def paged(name: str, service: str, oid: str, fields: str) -> list[tuple[str, Path]]:
    meta_path = CACHE / f"{name}_metadata.json"
    fetch(service + "?f=json", meta_path)
    meta = json.loads(meta_path.read_text())
    declared = {f["name"] for f in meta.get("fields", [])}
    if not set(fields.split(",")) <= declared:
        raise RuntimeError(f"[BLOCKED] schema drift: {name} {set(fields.split(',')) - declared}")
    dest = CACHE / f"{name}.geojson"
    url = service + "/query"
    if not dest.exists():
        count = get_json(url + "?" + urllib.parse.urlencode({"where": "1=1", "returnCountOnly": "true", "f": "json"}))["count"]
        feats = []
        offset = 0
        page_size = min(int(meta.get("maxRecordCount", 1000)), 2000)
        while offset < count:
            params = {"where": "1=1", "outFields": fields, "outSR": 4326, "f": "geojson", "orderByFields": oid,
                      "resultOffset": offset, "resultRecordCount": page_size}
            page = get_json(url + "?" + urllib.parse.urlencode(params))
            rows = page.get("features", [])
            if not rows:
                raise RuntimeError(f"[BLOCKED] truncated {name}: {offset}/{count}")
            feats.extend(rows)
            offset += len(rows)
        if len(feats) != count:
            raise RuntimeError(f"[BLOCKED] count changed during {name}: {len(feats)}/{count}")
        dest.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, sort_keys=True) + "\n")
        print(f"{name}: {count} records")
    return [(service + "?f=json", meta_path), (url, dest)]


def main() -> None:
    start = time.perf_counter()
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    sources = []
    for name, (service, oid, fields) in SERVICES.items():
        sources.extend(paged(name, service, oid, fields))
    # Required files fail loudly. FAA mapping is supplementary and can be server-blocked.
    for name, url in FILES.items():
        dest = CACHE / name
        try:
            fetch(url, dest)
        except subprocess.CalledProcessError:
            if name != "faa_txt_csv_mapping.pdf":
                raise
            print("[DEGRADED] FAA mapping PDF blocked; BTS metadata retained, ownership codes require primary codebook verification")
            continue
        sources.append((url, dest))
    if not LOCAL_IPEDS.exists():
        raise RuntimeError("[BLOCKED] local primary HD2023.csv absent; acquire NCES HD2023.zip")
    sources.append(("https://nces.ed.gov/ipeds/datacenter/data/HD2023.zip", LOCAL_IPEDS))
    dictionary = airport_dictionary()
    print(f"FAA primary dictionary verified: PU={dictionary['ownership_codes']['PU']}, ACREAGE={dictionary['acreage_unit']}")
    records = [{"url": u, "path": str(p.relative_to(HERE.parent)), "bytes": p.stat().st_size,
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for u, p in sources]
    (OUT / "universe_sources.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"seconds": round(time.perf_counter() - start, 3), "maxrss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
