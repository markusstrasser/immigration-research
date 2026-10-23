"""Normalize primary ownership inventories; facility points are not parcel boundaries.

Native-First: stdlib CSV/JSON normalization, with no imputation of acreage.
Run: uv run --no-project python3 -I {lane}/universes.py
"""
from __future__ import annotations

import collections
import csv
import json
import resource
import sys
import time
import urllib.parse
import subprocess
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from acquire_universes import airport_dictionary

CACHE = HERE / "_cache" / "universes"
OUT = HERE / "derived"
IP = HERE.parent / "affirmative_action_cost_2026_09_24" / "_cache" / "ipeds" / "HD2023.csv"
FIELDS = ["record_id", "class", "name", "lat", "lon", "public", "ownership", "county_fips", "state", "source_date",
          "acreage", "status", "site_type", "geocode_quality", "scattered_site", "source", "case_scope", "scope_evidence"]
STATES = {"AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"}
FEDERAL_COLLEGES = {
    "119678": ("Naval Postgraduate School", "scope_nps_about.html"),
    "128328": ("United States Air Force Academy", "scope_service_academies_gao.html"),
    "130624": ("United States Coast Guard Academy", "scope_service_academies_gao.html"),
    "155140": ("Haskell Indian Nations University", "scope_bie_colleges.html"),
    "164155": ("United States Naval Academy", "scope_service_academies_gao.html"),
    "187745": ("Institute of American Indian and Alaska Native Culture and Arts Development", "scope_iaia_4412.html"),
    "188216": ("Southwestern Indian Polytechnic Institute", "scope_bie_colleges.html"),
    "197027": ("United States Merchant Marine Academy", "scope_service_academies_gao.html"),
    "197036": ("United States Military Academy", "scope_service_academies_gao.html"),
    "200697": ("Air Force Institute of Technology-Graduate School of Engineering & Management", "scope_afit_about.html"),
}


class PrimaryText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.words = []

    def handle_data(self, data):
        self.words.append(data)


def scope_authorities():
    """Verify the declarations behind explicit federal institution ID exclusions."""
    checks = {
        "scope_service_academies_gao.html": ["The U.S. has five tuition-free", "Secretary of Transportation", "Secretary of the Department of Homeland Security",
                                               "United States Military Academy", "United States Naval Academy", "United States Air Force Academy",
                                               "United States Coast Guard Academy", "United States Merchant Marine Academy"],
        "scope_nps_about.html": ["Naval Postgraduate School is a Naval command"],
        "scope_afit_about.html": ["Department of the Air Force", "Air Education and Training Command"],
        "scope_bie_colleges.html": ["BIE operates Haskell Indian Nations University", "Southwestern Indian Polytechnic Institute", "operating two postsecondary schools"],
        "scope_iaia_4411.html": ["Institute of American Indian and Alaska Native Culture and Arts Development", "direction and control of a Board of Trustees"],
        "scope_iaia_4412.html": ["voting members shall be appointed by the President of the United States"],
    }
    for filename, phrases in checks.items():
        parser = PrimaryText()
        parser.feed((CACHE / filename).read_text())
        text = " ".join(" ".join(parser.words).split())
        for phrase in phrases:
            if phrase not in text:
                raise RuntimeError(f"[BLOCKED] federal scope authority changed: {filename}: {phrase}")
    tribal_text = subprocess.run(["pdftotext", "-raw", str(CACHE / "scope_bea_tribal_gce2005.pdf"), "-"], capture_output=True, text=True, check=True).stdout
    (CACHE / "scope_bea_tribal_gce2005.txt").write_text(tribal_text)
    if "Tribal governments are now treated as local governments" not in " ".join(tribal_text.split()):
        raise RuntimeError("[BLOCKED] BEA primary tribal-government classification not found")
    return {unitid: {"name": name, "authority_file": file} for unitid, (name, file) in FEDERAL_COLLEGES.items()}


def hospital_scope(owner, site_type, source_url):
    """HIFLD MILITARY includes VA; only source agency identifies defense vs VA."""
    host = (urllib.parse.urlparse(source_url or "").hostname or "").lower()
    is_host = lambda domain: host == domain or host.endswith("." + domain)
    if is_host("tricare.mil") or is_host("health.mil"):
        return "defense_excluded", "DoD/TRICARE treatment-facility source; includes possible joint sites, with no nondefense land split"
    if owner == "VETERANS HEALTH ADMINISTRATION" or is_host("va.gov") or is_host("ihs.gov"):
        return "eligible", "identified nondefense federal agency: " + (host or owner)
    if owner in {"GOVERNMENT - LOCAL", "GOVERNMENT - STATE", "GOVERNMENT - DISTRICT/AUTHORITY"}:
        return "eligible", "explicit state/local/district ownership"
    if owner == "GOVERNMENT - FEDERAL" or site_type == "MILITARY":
        return "federal_scope_unresolved", "federal or HIFLD MILITARY class without explicit VA/IHS/DoD source agency; held"
    return "not_public", "ownership not established as public"


def load_geo(name: str) -> list[dict]:
    data = json.loads((CACHE / f"{name}.geojson").read_text())
    if not data.get("features"):
        raise RuntimeError(f"[BLOCKED] empty universe {name}")
    return data["features"]


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def row(**kwargs):
    return {k: kwargs.get(k, "") for k in FIELDS}


def normalize():
    rows = []
    with IP.open(encoding="utf-8-sig", newline="") as handle:
        for p in csv.DictReader(handle):
            if p["STABBR"] not in STATES or p["ACT"] != "A":
                continue
            if p["UNITID"] in FEDERAL_COLLEGES and p["INSTNM"] != FEDERAL_COLLEGES[p["UNITID"]][0]:
                raise RuntimeError(f"[BLOCKED] federal institution ID/name drift: {p['UNITID']} {p['INSTNM']}")
            rows.append(row(record_id="ipeds:" + p["UNITID"], **{"class": "college"}, name=p["INSTNM"],
                            lat=p["LATITUDE"], lon=p["LONGITUD"], public="1" if p["CONTROL"] == "1" else "0",
                            ownership={"1": "public", "2": "private nonprofit", "3": "private for profit"}.get(p["CONTROL"], "unknown"),
                            county_fips=p["COUNTYCD"].zfill(5), state=p["STABBR"], source_date="2023-24",
                            status=p["ACT"], site_type=p["ICLEVEL"], source="NCES IPEDS HD2023",
                            case_scope="federal_education_excluded" if p["UNITID"] in FEDERAL_COLLEGES else ("eligible" if p["CONTROL"] == "1" else "not_public"),
                            scope_evidence=FEDERAL_COLLEGES[p["UNITID"]][1] if p["UNITID"] in FEDERAL_COLLEGES else "IPEDS control; no explicit federal institution exclusion"))
    for feat in load_geo("hifld_hospitals"):
        p = feat["properties"]
        if p["STATE"] not in STATES:
            continue
        owner = p["OWNER"] or "NOT AVAILABLE"
        public = "1" if owner.startswith("GOVERNMENT") or owner == "VETERANS HEALTH ADMINISTRATION" else ("" if owner == "NOT AVAILABLE" else "0")
        scope, evidence = hospital_scope(owner, p["TYPE"], p["SOURCE"])
        rows.append(row(record_id="hifld:" + str(p["ID"]), **{"class": "hospital"}, name=p["NAME"], lat=p["LATITUDE"], lon=p["LONGITUDE"],
                        public=public, ownership=owner, county_fips=str(p["COUNTYFIPS"] or "").zfill(5), state=p["STATE"],
                        source_date=p["SOURCEDATE"], status=p["STATUS"], site_type=p["TYPE"], source="FEMA HIFLD July 2025; " + str(p["SOURCE"]),
                        case_scope=scope, scope_evidence=evidence))
    for feat in load_geo("hud_developments"):
        p = feat["properties"]
        if p["STD_ST"] not in STATES:
            continue
        rows.append(row(record_id="hud:" + str(p["DEVELOPMENT_CODE"]), **{"class": "housing"}, name=p["PROJECT_NAME"],
                        lat=p["LAT"], lon=p["LON"], public="1", ownership="public housing development (HUD)",
                        county_fips=str(p["CURCNTY"] or p["CNTY2KX"] or "").zfill(5), state=p["STD_ST"], source_date=p["LAST_UPDT_DTTM"],
                        status=p["PD_STATUS_TYPE_CODE"], geocode_quality=p["LVL2KX"], scattered_site=p["SCATTERED_SITE_IND"],
                        source="HUD Public Housing Developments", case_scope="eligible", scope_evidence="HUD public housing development inventory"))
    for feat in load_geo("faa_bts_airports"):
        p = feat["properties"]
        if p["STATE_CODE"] not in STATES:
            continue
        # SITE_NO is reused across site types in the primary file (one TX A/H pair).
        rows.append(row(record_id="faa:" + str(p["SITE_NO"]) + ":" + p["SITE_TYPE_CODE"], **{"class": "airport"}, name=p["ARPT_NAME"],
                        lat=p["LAT_DECIMAL"], lon=p["LONG_DECIMAL"], public="1" if p["OWNERSHIP_TYPE_CODE"] == "PU" else "0",
                        ownership=p["OWNERSHIP_TYPE_CODE"], state=p["STATE_CODE"], source_date=p["EFF_DATE"],
                        acreage=p["ACREAGE"] if (num(p["ACREAGE"]) or 0) > 0 else "", status=p["ARPT_STATUS"],
                        site_type=p["SITE_TYPE_CODE"], source="FAA NASR via USDOT BTS NTAD",
                        case_scope="eligible" if p["OWNERSHIP_TYPE_CODE"] == "PU" else ("defense_excluded" if p["OWNERSHIP_TYPE_CODE"] in {"CG", "MA", "MN", "MR"} else "not_public"),
                        scope_evidence="primary FAA ownership code " + p["OWNERSHIP_TYPE_CODE"]))
    ids = [r["record_id"] for r in rows]
    duplicate_ids = [k for k, n in collections.Counter(ids).items() if n > 1]
    if duplicate_ids:
        raise RuntimeError(f"[BLOCKED] duplicate source IDs: {duplicate_ids[:10]}")
    if not set("ipeds:" + uid for uid in FEDERAL_COLLEGES) <= set(ids):
        raise RuntimeError("[BLOCKED] source-verified federal college absent from selected IPEDS universe")
    return sorted(rows, key=lambda r: (r["class"], r["record_id"]))


def airport_inventory_checks(rows):
    """Expose acreage missingness and duplication without extrapolating airports."""
    air = [r for r in rows if r["class"] == "airport" and r["public"] == "1"
           and r["status"] == "O" and r["site_type"] == "A"]
    have = [r for r in air if r["acreage"]]
    missing = [r for r in air if not r["acreage"]]
    coords, names = collections.defaultdict(list), collections.defaultdict(list)
    for r in air:
        coords[(round(float(r["lat"]), 5), round(float(r["lon"]), 5))].append(r)
        names[(r["name"], r["state"])].append(r)
    top = sorted(have, key=lambda r: float(r["acreage"]), reverse=True)[:20]
    raw = load_geo("faa_bts_airports")
    result = {
        "public_open_airports": len(air), "positive_acreage": len(have), "missing_acreage": len(missing),
        "positive_acres": sum(float(r["acreage"]) for r in have),
        "missing_by_state": dict(sorted(collections.Counter(r["state"] for r in missing).items())),
        "missing_examples": missing[:15],
        "top20": [{k: r[k] for k in ["record_id", "name", "state", "acreage", "lat", "lon"]} for r in top],
        "top10_acres_share": sum(float(r["acreage"]) for r in top[:10]) / sum(float(r["acreage"]) for r in have),
        "duplicate_coords_5dp": [rr for rr in coords.values() if len(rr) > 1],
        "duplicate_names_in_state": [rr for rr in names.values() if len(rr) > 1],
        "outside_US_bounds": [r for r in air if not (18 < float(r["lat"]) < 73 and -180 < float(r["lon"]) < -65)],
        "integer_degree_coordinates": [r for r in air if float(r["lat"]).is_integer() or float(r["lon"]).is_integer()],
        "sub_acre_records": [r for r in have if float(r["acreage"]) < 1],
        "territories_excluded": dict(sorted(collections.Counter(f["properties"]["STATE_CODE"] for f in raw if f["properties"]["STATE_CODE"] not in STATES).items())),
        "coordinate_disagreement_primary_fields_vs_geometry": sum(
            abs(f["geometry"]["coordinates"][0] - float(f["properties"]["LONG_DECIMAL"])) > 1e-6
            or abs(f["geometry"]["coordinates"][1] - float(f["properties"]["LAT_DECIMAL"])) > 1e-6 for f in raw),
        "location_rule": "state is the FAA associated-city state (Dulles lists DC despite coordinates in VA); use point-in-tract geography for pricing",
    }
    (OUT / "universe_airport_checks.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    return result


def main():
    start = time.perf_counter()
    authorities = scope_authorities()
    rows = normalize()
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "universe_records.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "universe_scope_exclusions.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(r for r in rows if r["case_scope"] in {"defense_excluded", "federal_education_excluded", "federal_scope_unresolved"})
    summary = {}
    dictionary = airport_dictionary()
    for cls in sorted({r["class"] for r in rows}):
        rr = [r for r in rows if r["class"] == cls]
        public = [r for r in rr if r["public"] == "1"]
        summary[cls] = {"records": len(rr), "public_records": len(public), "unknown_ownership": sum(r["public"] == "" for r in rr),
                        "public_valid_geocodes": sum(-180 < (num(r["lon"]) or -999) < 0 and 15 < (num(r["lat"]) or -999) < 75 for r in public),
                        "public_acreage_recorded": sum(bool(r["acreage"]) for r in public),
                        "case_scope_counts": dict(sorted(collections.Counter(r["case_scope"] for r in rr).items())),
                        "public_case_scope_counts": dict(sorted(collections.Counter(r["case_scope"] for r in public).items())),
                        "ownership_counts": dict(sorted(collections.Counter(r["ownership"] for r in rr).items())),
                        "source_dates": sorted({str(r["source_date"]) for r in rr})}
    # CMS contemporary ownership crosscheck is a separate universe: it has no point geometry.
    with (CACHE / "cms_hospital_general.csv").open(encoding="utf-8-sig", newline="") as handle:
        cms = [r for r in csv.DictReader(handle) if r["State"] in STATES]
    summary["cms_hospitals"] = {"records": len(cms), "government_records": sum(r["Hospital Ownership"].startswith("Government") for r in cms),
                                 "ownership_counts": dict(sorted(collections.Counter(r["Hospital Ownership"] for r in cms).items())),
                                 "limitation": "CMS Medicare universe differs from HIFLD and contains no coordinates; not an acreage or ownership-share imputation"}
    summary["airport"]["primary_dictionary"] = dictionary
    summary["college"]["federal_scope_authorities"] = authorities
    summary["college"]["federal_control_field"] = "HD CONTROL=1 does not distinguish federal; F1SYSTYP/F1SYSNAM identify no system for these ten; explicit primary-source institution IDs excluded"
    summary["college"]["tribal_scope_rule"] = "Tribal control/federal grants do not imply federal ownership: BEA SCB October2005 printedp8 treats tribal governments as local governments; explicit federal institutions still excluded"
    summary["hospital"]["federal_scope_rule"] = "SOURCE host TRICARE/health.mil excluded as defense/joint; VA/IHS source or VHA owner nondefense; other federal/MILITARY unresolved; TYPE=MILITARY alone never decides"
    airports = airport_inventory_checks(rows)
    summary["airport"]["open_public_airport_acreage_coverage"] = {
        k: airports[k] for k in ["public_open_airports", "positive_acreage", "missing_acreage", "positive_acres"]}
    (OUT / "universe_coverage.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    for cls, values in summary.items():
        print(cls, {k: v for k, v in values.items() if k not in {"source_dates", "ownership_counts"}})
    print(json.dumps({"seconds": round(time.perf_counter() - start, 3), "maxrss": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
