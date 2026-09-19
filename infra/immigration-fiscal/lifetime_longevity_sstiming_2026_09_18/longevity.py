"""Rebuild supported survival scenarios from corrected annual age components.

Native-First: reuse the annual ledger's period-profile implementation and NVSS cache.
Legacy longevity_*.csv files are superseded; this writes period_profiles.csv.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ledger_absolute_2026_09_17"))
from lifetime import main

if __name__ == "__main__":
    main()
