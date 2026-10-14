"""Pin the primary daily DFII10 file and the reused BEA pandemic table.

Native-First: urllib downloads; all subsequent runs verify immutable source bytes.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFII10&cosd=2005-01-01&coed=2024-12-31"


def main():
    cache = HERE / "_cache"
    cache.mkdir(exist_ok=True)
    path = cache / "DFII10.csv"
    if not path.exists():
        req = urllib.request.Request(CSV_URL, headers={"User-Agent": "Mozilla/5.0 research"})
        with urllib.request.urlopen(req, timeout=60) as response:
            path.write_bytes(response.read())
    pdf = cache / "bea_pandemic_2022q4_3rd.pdf"
    if not pdf.exists():
        shutil.copyfile(HERE.parent / "backcast_pandemic_measured_2026_09_28/_cache" / pdf.name, pdf)
    sources = {path.name: CSV_URL, pdf.name: "https://www.bea.gov/sites/default/files/2023-03/"
               "effects-of-selected-federal-pandemic-response-programs-on-personal-income-2022q4-3rd.pdf"}
    pins = {n: {"path": f"_cache/{n}", "url": u,
                "sha256": hashlib.sha256((cache / n).read_bytes()).hexdigest()} for n, u in sources.items()}
    destination = HERE / "inputs/pins.json"
    if destination.exists() and json.loads(destination.read_text()) != pins:
        raise SystemExit("[BLOCKED] P7 primary sources differ from inputs/pins.json")
    if pins[pdf.name]["sha256"] != "c0d92a9c6e6bfbcd8d22cc12af4f49675d95f4d9e0fa74e793a3b1b0058490fd":
        raise SystemExit("[BLOCKED] pandemic primary PDF differs from its source lane's pin")
    destination.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    print("PASS primary source pins")


if __name__ == "__main__":
    main()
