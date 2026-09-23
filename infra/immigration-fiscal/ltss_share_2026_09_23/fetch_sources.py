"""Fetch the archived CMS LTSS files this lane reads (medicaid.gov returns 403 to scripts).

Bytes come from Wayback `id_` snapshots of the medicaid.gov originals and land in the ignored
`_cache/wayback/`. The first run writes SOURCE_PINS.json (url, snapshot, sha256, bytes); later
runs verify against it and stop on any change.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ltss_share_2026_09_23/fetch_sources.py
"""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "_cache/wayback"
PINS = HERE / "SOURCE_PINS.json"
BASE = "https://www.medicaid.gov/medicaid/long-term-services-supports/downloads/"
FMR = "https://www.medicaid.gov/medicaid/financial-management/downloads/"
FILES = [  # (Wayback snapshot, file name[, base URL])
    ("20241129153342", "ltss-expenditures-user-data-2022.zip"),
    ("20240927124641", "ltss-expenditures-user-data-2019-2021.zip"),
    ("20260403063600", "ltss-user-character-brief-2023.pdf"),
    ("20241205151552", "ltss-user-character-brief-2022.pdf"),
    ("20240502200029", "ltssexpenditures2020.pdf"),
    ("20240928013615", "ltssexpenditures2020-app-d.xlsx"),
    ("20240927081644", "ltssexpenditures2020-app-e.xlsx"),
    ("20260123020751", "ltss-users-taf-method-2023.pdf"),
    ("20240929145348", "financial-management-report-fy2023.zip", FMR),
    ("20251002175227", "financial-management-report-fy2024.zip", FMR),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    for snap, name, *base in FILES:
        base = base[0] if base else BASE
        path = OUT / name
        if not path.exists():
            url = f"https://web.archive.org/web/{snap}id_/{base}{name}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research"})
            with urllib.request.urlopen(req, timeout=180) as r:
                path.write_bytes(r.read())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rec = dict(url=base + name, wayback_snapshot=snap, sha256=digest, bytes=path.stat().st_size)
        if name in pins and pins[name]["sha256"] != digest:
            sys.exit(f"[BLOCKED] {name} changed: {digest}")
        pins[name] = rec
        print(f"  ✓ {name} {rec['bytes']:,} bytes {digest[:12]}")
    PINS.write_text(json.dumps(pins, indent=1) + "\n")


if __name__ == "__main__":
    main()
