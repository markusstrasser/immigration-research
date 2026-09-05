#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1", "pymupdf>=1.26"]
# ///
"""Acquire small primary admission sources, preserving existing raw bytes.

Run from any directory with uv run --script <this file> [NAME URL].
Native-First: curl probes and downloads; openpyxl and PyMuPDF inspect official
tables that pdftotext fragmented. No warehouse or raw-source mutation.
"""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE = ROOT / ".scratch/clarity-next-20260905/admission"
OLD = ROOT / ".scratch/cohort-clarity-20260905/availability"
LIMIT = 25_000_000  # These are tables/documents, not the large SIPP extract.
SOURCES = {
    "rpc_fy2019.xlsx": "https://www.rpc.state.gov/documents/Archives/FY%202019%20Arrivals%20by%20State%20and%20Nationality.xlsx",
    "rpc_fy2022.pdf": "https://www.rpc.state.gov/documents/FY%202022%20Arrivals%20by%20State%20and%20Nationality%20as%20of%2030%20Sep%202022.pdf",
    "rpc_fy2023.pdf": "https://www.rpc.state.gov/documents/FY%202023%20Refugee%20Arrivals%20by%20State%20and%20Nationality%20as%20of%2030%20Sep%202023.pdf",
    "rpc_fy2024.pdf": "https://www.rpc.state.gov/documents/FY%202024%20Arrivals%20by%20State%20and%20Nationality%20as%20of%2030%20Oct%202024_updated.pdf",
    "rpc_fy2025.pdf": "https://www.rpc.state.gov/documents/FY%202025%20Arrivals%20by%20State%20and%20Nationality%20as%20of%2030%20Sep%202025.pdf",
    "rpc_fy2026_july.pdf": "https://www.rpc.state.gov/documents/Refugee%20Arrivals%20by%20State%20and%20Nationality%20as%20of%20July%2031,%202026.pdf",
    "pu2025_schema.json": "https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/pu2025_schema.json",
    "ohss_2024.html": "https://ohss.dhs.gov/topics/immigration/yearbook/2024",
    "uscis_index.html": "https://www.uscis.gov/tools/reports-and-studies/immigration-and-citizenship-data",
    "ohss_lpr2024.xlsx": "https://ohss.dhs.gov/system/files/2026-06/2026_0604_ohss_yearbook_lawful_permanent_residents_fy2024.xlsx",
    "ohss_lpr2024_newadj.xlsx": "https://ohss.dhs.gov/system/files/2026-07/2026_0604_ohss_tables8-11newadj_fy2024.xlsx",
    "uscis_i765_fy2026_q2.xlsx": "https://www.uscis.gov/sites/default/files/document/data/i765_application_for_employment_fy2026_q2_v1.xlsx",
    "uscis_i765_pending_fy2026_q2.xlsx": "https://www.uscis.gov/sites/default/files/document/data/i765_p_allcat_c08_fy2026_q2_v1.xlsx",
    "sipp2025_dictionary.pdf": "https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf",
    "ohss_legal.html": "https://ohss.dhs.gov/topics/immigration/legal-immigration-and-adjustment-status-report",
    "ohss_legal_fy2025q4.xlsx": "https://ohss.dhs.gov/system/files/2026-06/2026_0604_ohss_legal-immigration-adjustment-of-status-fy-2025q4.xlsx",
    "ohss_legal_fy2019q4.xlsx": "https://ohss.dhs.gov/sites/default/files/2023-12/fy2019_q4_d_final.xlsx",
    "ohss_legal_fy2022q4.xlsx": "https://ohss.dhs.gov/sites/default/files/2023-12/2023_0308_plcy_legal_immigration_adjustment_of_status_report_fy_2022q4_final_d_0.xlsx",
    "ohss_legal_fy2023q4.xlsx": "https://ohss.dhs.gov/sites/default/files/2024-06/2024_0507_ohss_legal-immigration-adjustment-of-status-fy-2023q4.xlsx",
    "ohss_refugees2024.xlsx": "https://ohss.dhs.gov/system/files/2025-08/2025_0812_ohss_yearbook_refugees_fy2024.xlsx",
    "ohss_legal_fy2024q4.xlsx": "https://ohss.dhs.gov/sites/default/files/2025-06/2025_0624_ohss_legal-immigration-adjustment-of-status-fy-2024q4_0.xlsx",
    "pew_unauthorized_method_2025.html": "https://www.pewresearch.org/2025/08/21/unauthorized-immigrants-methodology-a-unauthorized-immigrant-estimates/",
    "dhs_unauthorized2022.pdf": "https://ohss.dhs.gov/sites/default/files/2024-06/2024_0418_ohss_estimates-of-the-unauthorized-immigrant-population-residing-in-the-united-states-january-2018%25E2%2580%2593january-2022.pdf",
}

# Verified 2026-09-05 snapshots. A changed official file requires review, not a
# silent refresh. These pins make a clean checkout independent of scratch state.
PINNED_SHA256 = {
    "rpc_fy2019.xlsx": "06487ae0cb96fb848321fe06f32d5acb8d19cb12136dd92f645ca3fec0351161",
    "rpc_fy2022.pdf": "f092480c7fc450c474b9c3bf79d8344a42199243718bb910ba827d7f36c181ca",
    "rpc_fy2023.pdf": "b2cab97b1ea1d4571b88085e24a8d83bebc45aa457e9270657de8e194454d38f",
    "rpc_fy2024.pdf": "63ae2e259cab0a5d3154efe4199f582dc41e2f4f8d2553df678dedf6ce8149cc",
    "rpc_fy2025.pdf": "15627d62903df2eac6d5e8333ef6979441978366df18dee4a8e1e3e32b5b8cab",
    "rpc_fy2026_july.pdf": "a3b989e24a20c839c24d7796866089199c5e1c67c80262b10bf357a24b3111df",
    "pu2025_schema.json": "6cdc23c537ba1431540e62994f0c05e05e62920e785384872bf5b7c23fe8c241",
    "sipp2025_dictionary.pdf": "571e53b4ec3ebb11bebddbb7190fc1084f5364b8a1ec5fbd7ca8e2f69e7cc752",
    "ohss_2024.html": "512c0713114936bc24de29402605f5488f418dc4653cd4f1cd6580710bfe0bd2",
    "ohss_lpr2024.xlsx": "19c500a6e6445e73c0a39c5bc382585e2a13fc8f52f6e4d9a3cf6a84bf9bab6a",
    "ohss_lpr2024_newadj.xlsx": "b302cc1f5eee5ac7e6f0679701ddb5ce3d5da722c9912770ceafeb0391bb757d",
    "ohss_refugees2024.xlsx": "b795560dbf1dda1df5a0023fe17da8c9e190de91264da500fadf5f459d96a2ea",
    "ohss_legal.html": "0852d6f0ddf55a68f642810755a8424422f09c12337819aeb8b3a1d8d4c84e4c",
    "ohss_legal_fy2019q4.xlsx": "21014db04a3b4fc40645ce0eb26fb1dec44afce14b6d5ec36037c4694404dd20",
    "ohss_legal_fy2022q4.xlsx": "53afe8c09addaab829136472855b268d1e17e10a2d7709e45b5baf75485e2c2e",
    "ohss_legal_fy2023q4.xlsx": "5748f20d8dfc43c2a516a6d6425176bd7a74626fc94e6e741f50a102f786b656",
    "ohss_legal_fy2024q4.xlsx": "01f223391d8d6be67104aa34316a22492e1f17fb7005e2852a4a6c48ace6c295",
    "ohss_legal_fy2025q4.xlsx": "7660a03f72bcbee2cf3ff14ab6b8c5fd759faf89e96659b83c6e894f070f58cc",
    "uscis_index.html": "5dfb7efc61241c88fcf768147b9a0f3751a3abf75b977c9bf390722bd01abc75",
    "uscis_i765_fy2026_q2.xlsx": "1679a5c1ca818a5850c420dd975f7bc914e8296a0954b6e9b3b3940ce8ceeadc",
    "uscis_i765_pending_fy2026_q2.xlsx": "74f3d6265a561f2be768ae808e0beef05e6d560969a9e4e9e08777d0a6cb5f5f",
    "pew_unauthorized_method_2025.html": "38ab7ff68e2bc42470bfb9b459beced4d4c3ad9a3b512360c8fc2c5154037e1e",
    "dhs_unauthorized2022.pdf": "ae61e88ab0b5af76684c228580ae58a275335f8ef73528399b9cbf31bf810e88",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if len(sys.argv) not in (1, 3):
        raise ValueError("Usage: acquire_admission_evidence_20260905.py [NAME URL]")
    STAGE.mkdir(parents=True, exist_ok=True)
    manifest_path = STAGE / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    sources = dict([sys.argv[1:]]) if len(sys.argv) == 3 else SOURCES
    failures = []
    for name, url in sources.items():
        if Path(name).name != name:
            raise ValueError("Source name must be a basename")
        path = OLD / name if (OLD / name).exists() else STAGE / name
        previous = manifest.get(name)
        try:
            if name in SOURCES and SOURCES[name] != url:
                raise ValueError("Named source URL differs from the pinned source")
            expected = PINNED_SHA256.get(name)
            reused = path.exists()
            headers = STAGE / (name + ".headers")
            if not reused:
                probe = subprocess.run(["curl", "-sSI", "-L", "--max-time", "12", url], capture_output=True)
                headers.write_bytes(probe.stdout)
                if probe.returncode:
                    print(f"[PROBE-INCOMPLETE] {name}: HEAD rc={probe.returncode}; bounded GET remains capped at {LIMIT} bytes", flush=True)
                codes = re.findall(r"HTTP/\S+\s+(\d+)", probe.stdout.decode(errors="replace"))
                if codes and int(codes[-1]) >= 400:
                    raise RuntimeError(f"Official HTTP probe failed: {codes[-1]}")
                lengths = re.findall(r"content-length:\s*(\d+)", probe.stdout.decode(errors="replace"), re.I)
                if lengths and int(lengths[-1]) > LIMIT:
                    raise ValueError("Source exceeds bounded download size")
                part = path.with_suffix(path.suffix + ".part")
                subprocess.run(["curl", "-sS", "-fL", "--max-time", "60", "--max-filesize", str(LIMIT), "-o", str(part), url], check=True)
                if part.stat().st_size > LIMIT:
                    raise ValueError("Source exceeds bounded download size")
                if expected and sha(part) != expected:
                    raise ValueError("Remote bytes changed from tracked snapshot pin; not promoted")
                if previous and sha(part) != previous.get("sha256"):
                    raise ValueError("Remote bytes changed from pinned manifest; not promoted")
                path.hardlink_to(part)  # Atomic no-overwrite promotion on this filesystem.
                part.unlink()
            digest = sha(path)
            if expected and digest != expected:
                raise ValueError("Existing source differs from tracked snapshot pin; left unchanged")
            if previous and previous.get("sha256") and previous["sha256"] != digest:
                raise ValueError("Existing source differs from pinned hash; left unchanged")
            record = {"url": url, "path": str(path), "bytes": path.stat().st_size,
                      "sha256": digest, "verified_at": datetime.now(timezone.utc).isoformat(),
                      "acquired_at": previous.get("acquired_at") if previous else (None if reused else datetime.now(timezone.utc).isoformat()),
                      "reused": reused,
                      "license": ("Pew Research Center copyrighted web publication; no open-data license observed"
                                  if name.startswith("pew_") else
                                  "Public US federal government data; no separately stated dataset license observed")}
            manifest[name] = record
            print(name, record["bytes"], digest, flush=True)
        except Exception as exc:
            failures.append({"file": name, "url": url, "error": str(exc)})
            print("[UNAVAILABLE]", name, str(exc), flush=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (STAGE / "last-acquisition-errors.json").write_text(json.dumps(failures, indent=2) + "\n")
    return bool(failures)


if __name__ == "__main__":
    raise SystemExit(main())
