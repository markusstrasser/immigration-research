"""Rebuild period-profile scenarios; the former pronatal policy budget is withdrawn.

Native-First: route the existing command to the annual ledger's lifecycle consumer.
Historical lifetime_equivalence.csv is superseded and is never consumed here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ledger_absolute_2026_09_17"))
from lifetime import main

if __name__ == "__main__":
    main()
