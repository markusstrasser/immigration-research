"""Check published-table arithmetic; this is not microdata replication."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    source = root / "estimates.csv"
    with source.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 10:
        raise ValueError("Expected ten prespecified primary-table rows")
    keys = [(r["study"], r["outcome"], r["population"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate study/outcome/population")
    checked = []
    for row in rows:
        b = float(row["estimate"])
        if not math.isfinite(b):
            raise ValueError("Nonfinite estimate")
        item = dict(row, estimate=b)
        if row["se"]:
            se = float(row["se"])
            if not math.isfinite(se) or se <= 0:
                raise ValueError("Invalid standard error")
            item["normal_95_interval"] = [b - 1.96 * se, b + 1.96 * se]
            item["interval_status"] = "normal approximation from rounded published values"
        else:
            p = float(row["permutation_p"])
            if not 0 <= p <= 1:
                raise ValueError("Invalid permutation p value")
            item["normal_95_interval"] = None
            item["interval_status"] = "no SE supplied; permutation p is not an interval"
        if row["unit"] == "log_points":
            item["geometric_percent_change"] = 100 * math.expm1(b)
            item["conversion_limit"] = "geometric transformation, not arithmetic mean effect"
        elif row["unit"] == "percentage_points_person_month":
            item["victimized_person_months_per_1000_person_years"] = b * 120
            item["conversion_limit"] = "not distinct annual victims or crime incident counts"
        elif row["unit"] != "percentage_points_incidents":
            raise ValueError(f"Unknown unit: {row['unit']}")
        checked.append(item)
    report = {
        "kind": "primary_table_arithmetic_not_microdata_replication",
        "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "rows_checked": len(checked),
        "national_stock_dollars_estimated": False,
        "immigration_only_offense_victim_harm": 0,
        "harm_rule": "Actual additional resources or victim harm only; no price per legal violation",
        "rows": checked,
    }
    out = root / "derived"
    out.mkdir(exist_ok=True)
    (out / "table_arithmetic.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"checked": len(checked), "kind": report["kind"]}))


if __name__ == "__main__":
    main()
