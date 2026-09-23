#!/usr/bin/env python3
"""Fetch the DHCS enrollment benchmarks into _cache/ and record what was fetched.

DHCS's own site (www.dhcs.ca.gov) answers curl with an Incapsula 403, so its PDFs come from the
Internet Archive's unmodified copy (`id_` URLs) at the capture named below; the CalHHS open-data
portal serves the DHCS enrollment tables directly. Python urllib fails TLS on this machine, so every
download is `curl` via subprocess. Writes derived/sources.json (URL, capture, bytes, sha256).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
        infra/immigration-fiscal/california_medical_status_2026_09_23/fetch_sources.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
WB = "https://web.archive.org/web/{ts}id_/{url}"
CHHS = "https://data.chhs.ca.gov/dataset/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"

SOURCES = {
    # DHCS enrollment in the status-blind full-scope expansions, monthly, by county (MEDS).
    "sb75_children_under19.csv": CHHS + "fbf46fd8-63ca-441f-954c-e2ffb007c34f/resource/"
    "8d27e04c-a706-4721-9aa5-5d1c57c09878/download/sb-75_06-2026_suprsd_odp.csv",
    "yae_19_25.csv": CHHS + "9615f1b1-8329-4dbc-88cf-bb7ddfde8a71/resource/"
    "09a0fa21-bc20-4d2e-acb4-ce1ab9b8e224/download/yae-suprsd-06_2026_odp.csv",
    "ae_26_49.csv": CHHS + "9615f1b1-8329-4dbc-88cf-bb7ddfde8a71/resource/"
    "a08f6d35-ca23-485b-bfe4-9348859ab68f/download/26-49-ae-county-06-2026_suprsd_odp.csv",
    "oae_50plus.csv": CHHS + "9615f1b1-8329-4dbc-88cf-bb7ddfde8a71/resource/"
    "9ea18162-1361-4df6-8624-5a4e718d7fd5/download/oae-06-2026-suprsd-data_odp.csv",
    "chhs_pkg_adult_expansion.json": "https://data.chhs.ca.gov/api/3/action/package_show?id=medi-cal-adult-expansion",
    "chhs_pkg_sb75.json": "https://data.chhs.ca.gov/api/3/action/package_show?id="
    "sb-75-full-scope-medi-cal-for-all-children-enrollment",
    # All Medi-Cal certified eligibles by county, age group and sex (DHCS via CalHHS), for the
    # survey-vs-administrative reporting rate.
    "t1_eligibility_by_age_group_sex_201001_202609.csv": CHHS + "8c897320-ba87-4574-bc37-bae974191c35/"
    "resource/cc08b60f-393f-4e37-9b3e-976d7a9f2a72/download/t1_eligibility_by_age_group_sex_201001_202609.csv",
    # Medi-Cal Local Assistance Estimates (DHCS), Internet Archive captures.
    "M25-Medi-Cal-Local-Assistance-Estimate.pdf": WB.format(
        ts="20250622001304", url="https://www.dhcs.ca.gov/dataandstats/reports/mcestimates/Documents/"
        "2025_May_Estimate/MAY-2025-Medi-Cal-Local-Assistance-Estimate.pdf"),
    "N25-Medi-Cal-Local-Assistance-Estimate.pdf": WB.format(
        ts="20260302191958", url="https://www.dhcs.ca.gov/dataandstats/reports/mcestimates/Documents/"
        "2025_November_Estimate/N25-Medi-Cal-Local-Assistance-Estimate.pdf"),
    # State programs covering people regardless of immigration status (section 4 of RESULT.md).
    "kff_more-states-are-providing-fully-state-funded-health-coverage-to-some-individuals-regardless-"
    "of-immigration-status.html": "https://www.kff.org/racial-equity-and-health-policy/more-states-are-"
    "providing-fully-state-funded-health-coverage-to-some-individuals-regardless-of-immigration-status/",
    "kff_state-health-coverage-for-immigrants-and-implications-for-health-coverage-and-care.html":
    "https://www.kff.org/racial-equity-and-health-policy/state-health-coverage-for-immigrants-and-"
    "implications-for-health-coverage-and-care/",
    "dw_KfNPA_8.csv": "https://datawrapper.dwcdn.net/KfNPA/8/dataset.csv",   # KFF 2026 adult map
    "dw_kM1HV_8.csv": "https://datawrapper.dwcdn.net/kM1HV/8/dataset.csv",   # KFF 2026 child map
    "oha_healthier_oregon.html": "https://www.oregon.gov/oha/hsd/ohp/pages/healthier-oregon.aspx",
    "nydoh_23inf-02.pdf": "https://www.health.ny.gov/health_care/medicaid/publications/docs/inf/23inf-02.pdf",
    # Census finance function definitions (public welfare, B79).
    "census_2006_classification_manual.pdf":
    "https://www2.census.gov/govs/pubs/classification/2006_classification_manual.pdf",
}


def fetch(name: str, url: str) -> dict:
    out = CACHE / name
    if not out.exists() or out.stat().st_size == 0:
        subprocess.run(["curl", "-sSL", "--fail", "--retry", "3", "--max-time", "600", "-A", UA,
                        "-o", str(out), url], check=True)
    blob = out.read_bytes()
    if b"Incapsula" in blob[:3000] or (name.endswith((".pdf", ".csv")) and blob[:15].lower().startswith(b"<html")):
        raise ValueError(f"{name}: got an HTML block page, not the document")
    return {"file": f"_cache/{name}", "url": url, "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest()}


def main():
    CACHE.mkdir(exist_ok=True)
    rows = [fetch(n, u) for n, u in SOURCES.items()]
    for pdf in [r for r in rows if r["file"].endswith(".pdf")]:
        txt = HERE / (pdf["file"][:-4] + ".txt")
        if not txt.exists():
            subprocess.run(["pdftotext", "-layout", str(HERE / pdf["file"]), str(txt)], check=True)
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived/sources.json").write_text(json.dumps(rows, indent=2))
    for r in rows:
        print(f"{r['bytes']:>10,}  {r['sha256'][:12]}  {r['file']}")


if __name__ == "__main__":
    main()
