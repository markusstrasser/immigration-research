#!/bin/sh
# Rebuild only this item lane. Native-First: commands, no upstream lane writes.
set -eu
ITEM18_LANE=infra/immigration-fiscal/consumption_tax_bases_r5_2026_10_15
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" node "$ITEM18_LANE/case_snapshot.cjs"
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" uv run --no-project python3 "$ITEM18_LANE/business_bases.py" --out "$ITEM18_LANE/inputs/business_bridge.json"
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" uv run --no-project python3 "$ITEM18_LANE/household.py"
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" uv run --no-project python3 "$ITEM18_LANE/companion.py"
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" uv run --no-project python3 "$ITEM18_LANE/assemble.py"
uv run --no-project python3 "$ITEM18_LANE/measure_run.py" node "$ITEM18_LANE/evaluate.cjs"
