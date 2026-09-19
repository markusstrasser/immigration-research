#!/usr/bin/env python3
"""Collect the four acs_residual.py rule-list variants into one table.

Run acs_residual.py with each flag combination first; this script only reads the
summary JSON each run leaves behind.

Output: derived/rule_sensitivity.csv
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")
DERIVED = Path(__file__).resolve().parent / "derived"

VARIANTS = [
    ("acs2024_summary_cuba.json", "Borjas as published (Cuba only, occupation rule on)"),
    ("acs2024_summary_cuba_noocc.json", "occupation rule (h) dropped"),
    ("acs2024_summary_wide.json", "wide refugee-origin list for rule (g)"),
    ("acs2024_summary_wide_noocc.json", "wide refugee list and no occupation rule"),
]


def main() -> int:
    rows = []
    for fname, label in VARIANTS:
        p = DERIVED / fname
        if not p.exists():
            print(f"  ! missing {fname} — run acs_residual.py with that flag first")
            continue
        s = json.loads(p.read_text())
        rows.append({"rule_variant": label,
                     "residual_counted": s["borjas_residual_unadjusted"],
                     "se": s["borjas_residual_se"],
                     "residual_dhs_coverage": s["borjas_residual_ohss_coverage"]})
    if not rows:
        return 1
    t = pd.DataFrame(rows)
    base = t.residual_counted.iloc[0]
    t["pct_vs_published_rules"] = ((t.residual_counted / base - 1) * 100).round(2)
    t.to_csv(DERIVED / "rule_sensitivity.csv", index=False)
    print(t.to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
