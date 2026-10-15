"""Pin FRED 2024 TIPS observations; reproduce annual means without network by default."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import resource
import re
import time
import urllib.request
import sys

LANE = Path(__file__).resolve().parent
INPUT = LANE / "inputs"
sys.path.insert(0, str(LANE.parent / "scripts"))
from memory_budget import require_within_budget


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    INPUT.mkdir(exist_ok=True)
    manifest = INPUT / "market_sources.json"
    sources = json.loads(manifest.read_text()) if manifest.exists() else {}
    rows = []
    for series, years in (("DFII10", 10), ("DFII30", 30)):
        url = f"https://fred.stlouisfed.org/graph/?g=1&id={series}&cosd=2024-01-01&coed=2024-12-31"
        download = f"https://fred.stlouisfed.org/data/{series}.txt"
        file = INPUT / f"market_{series}_2024.csv"
        if args.refresh:
            raw = urllib.request.urlopen(download, timeout=45).read()
            # FRED now redirects .txt to an HTML table with its full data in
            # #DATE|VALUE records. graph.csv returns HTTP404 in this environment.
            selected = re.findall(r"#(2024-\d{2}-\d{2})\|\s*([.\d-]+)", raw.decode())
            if len(selected) != 262:
                raise SystemExit(f"[BLOCKED] FRED data-table format or coverage changed {series}: {len(selected)}")
            with file.open("w", newline="") as out:
                writer = csv.writer(out, lineterminator="\n")
                writer.writerow(["date", series])
                writer.writerows(selected)
            sources[series] = {
                "series_url": f"https://fred.stlouisfed.org/series/{series}",
                "download_url": download, "graph_url": url,
                "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
            }
        if not file.exists() or series not in sources:
            raise SystemExit("[BLOCKED] missing pinned market input; run --refresh explicitly")
        if hashlib.sha256(file.read_bytes()).hexdigest() != sources[series]["sha256"]:
            raise SystemExit(f"[BLOCKED] market input hash mismatch {series}")
        data = list(csv.DictReader(file.open()))
        if not data or any(not r["date"].startswith("2024-") for r in data):
            raise SystemExit(f"[BLOCKED] market year mismatch {series}")
        values = [float(r[series]) for r in data if r[series] not in ("", ".")]
        if len(values) < 240 or len({r["date"] for r in data}) != len(data):
            raise SystemExit(f"[BLOCKED] market observation coverage {series}")
        rows.append({"series": series, "maturity_years": years, "year": 2024,
                     "observations": len(values), "annual_average_percent": sum(values) / len(values),
                     **sources[series]})
    if args.refresh:
        manifest.write_text(json.dumps(sources, indent=2) + "\n")
    trustees = json.loads((LANE.parent / "one_rate_2026_10_15/derived/rates.json").read_text())["trustees_capital"]
    output = {"method": "Arithmetic mean of available daily 2024 observations; missing holidays excluded.",
              "units": "percent per year, real", "market": rows,
              "trustees_flat_equivalent_percent": 100 * trustees["flat_real_equivalent"],
              "interpretation": "Market TIPS yields are beside the Trustees' projected new-issue path; maturity, liquidity and inflation-risk conventions differ.",
              "external_booked_rates": {
                  "source": "one_rate_2026_10_15/inventory.md", "unchanged_imported_valuations": True,
                  "bea_state_local_pension_method": "Moody's AAA corporate-bond based; exact 2024 normal-cost parameter unavailable",
                  "bea_pension_interest_stock_diagnostic_nominal_percent": {"state_local": 4.9433335, "federal": 3.9428500},
                  "financial_report_fy2024_pension_nominal_percent": {"FERS": 3.0, "CSRS": 2.5, "military": 3.0},
                  "financial_report_fy2024_opeb_nominal_percent": {"civilian": 3.2, "military": 3.0},
                  "state_opeb": "GASB75 blended funded-plan return and high-quality municipal yield; aggregate rate unavailable",
                  "qualification": "Interest/stock diagnostics and federal Financial Report cross-checks are not exact BEA normal-cost discount schedules; no re-discounting claimed."}}
    out = LANE / "derived/market_check.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"market": rows, "elapsed_seconds": time.perf_counter()-started,
                      "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "peak_physical_footprint_bytes": require_within_budget("v9 market check")}))


if __name__ == "__main__":
    main()
