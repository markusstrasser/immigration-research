#!/usr/bin/env python3
"""Stage Gould Table 1 + HUD PIT CoC panel CSVs for lifetime warehouse load."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from paths import data_root, derived_root

HUD_XLSB = data_root() / "external" / "hud" / "2007-2024-PIT-Counts-by-CoC.xlsb"
PIT_CSV = derived_root() / "stage5" / "hud_pit_coc_annual.csv"
GOULD_CSV = derived_root() / "stage5" / "gould_asylum_shelter_attribution_2022_2024.csv"

GOULD_ROWS = [
    # locality, coc_label, sheltered_change_22_24, pct_change, direct_asylum, direct_share, indirect_asylum, indirect_share
    ("New York City", "NY-600", 77352, 1.3249, 66700, 0.8623, 51099, 0.6606),
    ("Chicago", "IL-510", 14590, 5.5858, 13679, 0.9376, 13629, 0.9341),
    ("Massachusetts", "MA-ALL", 13353, 0.9291, 7821, 0.5857, 7821, 0.5857),
    ("Metropolitan Denver", "CO-503", 6556, 1.3641, 4300, 0.6559, 4727, 0.7210),
    ("Top Four Combined", "TOP4", 111851, 1.3951, 92500, 0.8270, 77149, 0.6897),
    ("All Other Localities", "OTHER", 36775, 0.1370, None, None, 6120, 0.1664),
    ("Nationwide", "US", 148626, 0.4263, 92500, 0.6224, 87611, 0.5895),
]


def _write_gould() -> None:
    import pandas as pd

    GOULD_CSV.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        GOULD_ROWS,
        columns=[
            "locality",
            "coc_label",
            "sheltered_change_2022_2024",
            "sheltered_pct_change_2022_2024",
            "direct_asylum_seekers_2024_pit",
            "direct_asylum_share_of_change",
            "indirect_asylum_seekers_2024_pit",
            "indirect_asylum_share_of_change",
        ],
    )
    df["source"] = "gould_w33655_table1"
    df["extract_date"] = "2026-06-15"
    df.to_csv(GOULD_CSV, index=False)
    print(f"Wrote {GOULD_CSV} ({len(df)} rows)")


def _extract_hud() -> None:
    if not HUD_XLSB.exists():
        print(f"WARN: missing {HUD_XLSB} — run acquire/setup-restrictionist-panels.sh", file=sys.stderr)
        return
    PIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    script = Path(__file__).resolve().parent / "pit_coc_extract.py"
    subprocess.check_call(
        [sys.executable, str(script), str(HUD_XLSB), str(PIT_CSV)],
    )


def build() -> None:
    _write_gould()
    try:
        _extract_hud()
    except Exception as exc:
        print(f"WARN: HUD PIT extract failed: {exc}", file=sys.stderr)


if __name__ == "__main__":
    build()
