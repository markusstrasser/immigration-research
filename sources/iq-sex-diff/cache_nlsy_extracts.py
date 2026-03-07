#!/usr/bin/env python3
"""Cache narrow NLSY79/NLSY97 analysis extracts as Parquet for fast reruns."""

from __future__ import annotations

from pathlib import Path
from time import perf_counter

from build_nlsy79_sibling_pairs import load_rows
from nlsy79_stats_pipeline import rows_to_frame
from nlsy97_stats_pipeline import load_frame


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "nlsy"


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    t0 = perf_counter()
    rows79 = load_rows()
    frame79 = rows_to_frame(rows79).reset_index()
    path79 = DATA_DIR / "nlsy79_analysis_extract.parquet"
    frame79.to_parquet(path79, index=False)
    print(f"Wrote {path79} ({len(frame79):,} rows) in {perf_counter() - t0:.1f}s")

    t1 = perf_counter()
    frame97, _ = load_frame()
    frame97 = frame97.reset_index()
    path97 = DATA_DIR / "nlsy97_analysis_extract.parquet"
    frame97.to_parquet(path97, index=False)
    print(f"Wrote {path97} ({len(frame97):,} rows) in {perf_counter() - t1:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
