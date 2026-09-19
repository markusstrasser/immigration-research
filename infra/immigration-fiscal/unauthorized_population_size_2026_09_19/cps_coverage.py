#!/usr/bin/env python3
"""Apply the published coverage schemes to the CPS ASEC 2025 residual.

The repo's ledger carries the CPS residual with NO coverage adjustment, while
every published estimate applies one.  This puts the two on the same footing.

The CPS arrival variable PEINUSYR is banded, so the 2020-2021 band has to be
split to line up with CMS's 2021 boundary; it is split in half and the
sensitivity to that split is reported.

Input : derived/cps2025_residual_by_yrsince.csv
Output: derived/cps2025_coverage_grid.csv
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

os.environ.setdefault("PYTHONUNBUFFERED", "1")
DERIVED = Path(__file__).resolve().parent / "derived"

# rate for arrivals from 2021 on, rate for earlier arrivals
SCHEMES = {
    "none": (0.0, 0.0),
    "cis_2.25pct_flat": (0.0225, 0.0225),
    "cms_5_37": (0.37, 0.05),
    "cms_high_5_65": (0.65, 0.05),
}


def main() -> int:
    d = pd.read_csv(DERIVED / "cps2025_residual_by_yrsince.csv")
    post2021_full = float(d.loc[d.peinusyr_code >= 28, "residual_unadjusted"].sum())
    band_2020_21 = float(d.loc[d.peinusyr_code == 28 - 1, "residual_unadjusted"].sum())
    pre2021_full = float(d.loc[d.peinusyr_code <= 26, "residual_unadjusted"].sum())
    total = post2021_full + band_2020_21 + pre2021_full

    rows = []
    for split in [0.0, 0.5, 1.0]:
        recent = post2021_full + split * band_2020_21
        older = pre2021_full + (1 - split) * band_2020_21
        for name, (r_recent, r_old) in SCHEMES.items():
            adj = recent / (1 - r_recent) + older / (1 - r_old)
            rows.append({
                "share_of_2020_2021_band_treated_as_2021_arrivals": split,
                "coverage_scheme": name,
                "counted_residual": round(total),
                "adjusted_residual": round(adj),
                "implied_overall_multiplier": round(adj / total, 4),
            })
    t = pd.DataFrame(rows)
    t.to_csv(DERIVED / "cps2025_coverage_grid.csv", index=False)
    print(t.to_string(index=False))
    print("\nCaution: the ASEC 2025 weights already use the Vintage 2024 population "
          "estimates, which the Census Bureau revised upward in December 2024 to "
          "capture the 2021-24 arrivals. Applying an ACS-calibrated undercount rate "
          "on top of that risks counting the same correction twice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
