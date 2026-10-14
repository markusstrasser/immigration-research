"""Acquire small official coverage tables, then pin their actual bytes.

Native-First: direct Census downloads; existing CPS inputs are reused read-only.
Run with --download only to acquire; normal runs verify the existing pins.
"""
import argparse
import hashlib
import json
from pathlib import Path

import requests

LANE = Path(__file__).resolve().parent
FILES = {
    "pes_cross.pdf": "https://www2.census.gov/programs-surveys/decennial/coverage-measurement/pes/net-coverage-error-and-components-of-coverage-by-race-hispanic-origin.pdf",
    "pes_national.pdf": "https://www2.census.gov/programs-surveys/decennial/coverage-measurement/pes/national-census-coverage-estimates-by-demographic-characteristics.pdf",
    "da_hispanic.xlsx": "https://www2.census.gov/programs-surveys/popest/tables/2020/2020-demographic-analysis-estimates/table-1c.xlsx",
    "da_age.xlsx": "https://www2.census.gov/programs-surveys/popest/tables/2020/2020-demographic-analysis-estimates/Table-2_5YA-sex.xlsx",
}


def main(download=False):
    dest = LANE / "inputs"
    dest.mkdir(exist_ok=True)
    pins_path = dest / "pins.json"
    pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    for name, url in FILES.items():
        path = dest / name
        if not path.exists() and download:
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            prefix = b"%PDF" if name.endswith(".pdf") else b"PK"
            if not response.content.startswith(prefix):
                raise SystemExit(f"[BLOCKED] {name}: expected primary PDF/XLSX, received another format")
            path.write_bytes(response.content)
        if not path.exists():
            raise SystemExit(f"[BLOCKED] missing {path}; run acquire.py --download")
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        if name in pins and pins[name]["sha256"] != sha:
            raise SystemExit(f"[BLOCKED] changed source {name}")
        if name not in pins:
            if not download:
                raise SystemExit(f"[BLOCKED] unpinned source {name}")
            pins[name] = {"url": url, "sha256": sha, "bytes": path.stat().st_size}
        print(f"verified {name}: {sha[:16]} {path.stat().st_size} bytes")
    if download:
        pins_path.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    main(parser.parse_args().download)
