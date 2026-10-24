#!/bin/sh
# Candidate v10 (oct24). Reads the adopted v9 lane and the four source lanes; writes only this lane.
# Item 25 (land) is on only when V10_LAND_LANE names a lane with derived/land_by_line.csv.
set -eu
LANE=infra/immigration-fiscal/main_case_2026_10_24
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
export NODE_OPTIONS="--max-old-space-size=1536"
mkdir -p "$LANE/_cache"
node "$LANE/test_lane.cjs"
node "$LANE/main_case.cjs"
uv run --no-project python3 "$LANE/write_result.py"
