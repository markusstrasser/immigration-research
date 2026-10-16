#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/sipp_departure_work_2026_10_16
export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 "$LANE/extract.py"
uv run --no-project python3 "$LANE/components.py"
uv run --no-project python3 "$LANE/events.py"
uv run --no-project python3 "$LANE/measure.py"
uv run --no-project python3 "$LANE/benchmark.py"
uv run --no-project --with matplotlib python3 "$LANE/artifacts.py"
uv run --no-project python3 -m pytest "$LANE/test_measurement.py" -q
