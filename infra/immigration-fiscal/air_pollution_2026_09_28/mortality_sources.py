"""Acquire and pin P7 primary mortality/cap evidence; existing files are never refreshed silently."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCES = {
    "db548.html": "https://www.cdc.gov/nchs/products/databriefs/db548.htm",
    "lt2024_Table01.xlsx": "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/NVSR/75-05/Table01.xlsx",
    "arp2024_auction.html": "https://www.epa.gov/power-sector/2024-so2-allowance-auction",
    "epa_market_activity.html": "https://www.epa.gov/power-sector/progress-report-program-compliance-and-market-activity",
    "csapr2024_bank_2025_rule.pdf": "https://www.govinfo.gov/content/pkg/FR-2025-05-20/pdf/2025-08964.pdf",
    "csapr2024_feb_prices.pdf": "https://19january2025snapshot.epa.gov/system/files/documents/2024-03/basis-for-partial-denial-of-petitions-for-reconsideration-of-good-neighbo.pdf",
    "acs2024_dictionary.pdf": "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf",
    "epa_allowance_data.html": "https://www.epa.gov/power-sector/allowance-data",
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    start = time.perf_counter()
    (HERE / "inputs").mkdir(exist_ok=True)
    pinpath = HERE / "inputs/pins.json"
    pins = json.loads(pinpath.read_text()) if pinpath.exists() else {"files": []}
    held = {entry["path"]: entry for entry in pins["files"]}
    old_consumer = "infra/immigration-fiscal/sept24_propagation_2026_09_24/derived/oct14/band_variants.json"
    if old_consumer in held:
        snapshot = HERE / "inputs/band_variants_oct14_positive_control.json"
        if digest(snapshot) != held[old_consumer]["sha256"]:
            raise ValueError("[BLOCKED] consumer snapshot differs from original pinned bytes")
        pins["snapshot_origin"] = held.pop(old_consumer)
    for name, url in SOURCES.items():
        path = HERE / "_cache" / name
        rel = str(path.relative_to(ROOT))
        if not path.exists():
            # CDC's edge rejects urllib's TLS/client fingerprint (403), while
            # curl reaches the identical official URL. Fail on HTTP errors.
            tmp = path.with_suffix(path.suffix + ".download")
            subprocess.run(["curl", "-fLsS", "--retry", "2", "--max-time", "60", url, "-o", str(tmp)], check=True)
            if tmp.stat().st_size < 1000:
                raise ValueError(f"[BLOCKED] empty/truncated primary source: {url}")
            tmp.replace(path)
        sha = digest(path)
        if rel in held and held[rel]["sha256"] != sha:
            raise ValueError(f"[BLOCKED] pinned source changed: {rel}")
        held[rel] = dict(path=rel, sha256=sha, url=url, kind="primary")
    # These are preserved primary inputs; the pin records their exact live bytes.
    for path, kind in [
        (ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip", "Census ACS 2024 one-year PUMS"),
        (HERE.parent / "congestion_2026_09_23/_cache/xwalk_puma22_ua20.csv", "Missouri Census Data Center PUMA2022-UA2020 allocation"),
        (HERE / "_cache/bekbulat_marshall200.pdf", "Bekbulat author primary PDF"),
        (HERE.parent / "main_case_2026_10_14/derived/corrections.json", "frozen case declaration"),
        (HERE / "inputs/band_variants_oct14_positive_control.json", "2026-10-14 consumer snapshot; source sept24_propagation_2026_09_24/derived/oct14/band_variants.json before P7 edits"),
        (HERE.parent / "population_basis_2026_09_29/derived/frame_counts.csv", "current source population frame"),
        (HERE.parent / "population_basis_2026_09_29/derived/reeval.csv", "current row4 PM positive control"),
    ]:
        rel = str(path.relative_to(ROOT))
        sha = digest(path)
        if rel in held and held[rel]["sha256"] != sha:
            raise ValueError(f"[BLOCKED] pinned input changed: {rel}")
        held[rel] = dict(path=rel, sha256=sha, kind=kind)
    pins["files"] = [held[key] for key in sorted(held)]
    pinpath.write_text(json.dumps(pins, indent=2) + "\n")
    print(json.dumps(dict(seconds=time.perf_counter() - start,
                          max_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))


if __name__ == "__main__":
    main()
