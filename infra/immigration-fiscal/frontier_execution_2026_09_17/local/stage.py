"""Snapshot public sources used in the NYC incidence case; never overwrite raw files."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = "https://comptroller.nyc.gov/"
SHEET = "https://docs.google.com/spreadsheets/d/1e2bmhqWGl2XYyFCqb7OHDNv5tD9jtiqAW4PRpzys4gM/gviz/tq"
SOURCES = {
    "census.html": BASE + "services/for-the-public/accounting-for-asylum-seeker-services/asylum-seeker-census/",
    "fiscal.html": BASE + "services/for-the-public/accounting-for-asylum-seeker-services/fiscal-impacts/",
    "executive_fy2027.html": BASE + "reports/comments-on-new-york-citys-executive-budget-for-fiscal-year-2027-and-financial-plan-for-fiscal-years-2026-2030/",
    "shelter_rule.html": BASE + "reports/report-on-the-investigation-of-the-implementation-of-the-60-day-rule-for-asylum-seeker-families/",
    "meyer_wyse_williams_2026.pdf": "https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/a/3122/files/2026/02/Meyer-Wyse-Williams-JPubE-2026.pdf",
}
for sheet in ("AsylumSeekersbyShelterTypeStackedBar", "AsylumSeekersbyShelterType", "InCityCare", "OutsideNYC", "WeeklyExit", "totalStudentsNumber", "newStudentsbyDistrict", "byDistMostRecent"):
    SOURCES[sheet + ".csv"] = SHEET + "?sheet=" + sheet + "&headers=1&tqx=out:csv"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane-dir", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    raw = args.lane_dir / "raw" / "local"
    raw.mkdir(parents=True, exist_ok=True)
    manifest_path = raw / "source_manifest.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    manifest = {r["filename"]: r for r in previous}
    for name, url in SOURCES.items():
        path = raw / name
        if path.exists():
            assert name in manifest, f"Unregistered existing input: {path}"
            assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[name]["sha256"]
            continue
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        content = response.content
        if name.endswith(".pdf"):
            assert content.startswith(b"%PDF"), "Rejected HTML masquerading as PDF"
        if name.endswith(".csv"):
            assert b"<html" not in content[:1000].lower(), "Rejected non-data response"
        path.write_bytes(content)
        manifest[name] = {"filename": name, "url": url, "final_url": response.url,
                          "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                          "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
                          "content_type": response.headers.get("Content-Type")}
        manifest_path.write_text(json.dumps(list(manifest.values()), indent=2) + "\n")
        print(name, len(content))


if __name__ == "__main__":
    main()
