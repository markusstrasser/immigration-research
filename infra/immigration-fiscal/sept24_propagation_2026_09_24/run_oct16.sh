#!/bin/sh
# Native-First: use the lane dispatchers and native comparator regression checks.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
LANE=infra/immigration-fiscal/sept24_propagation_2026_09_24
node "$LANE/band_variants.cjs" --case oct16
uv run --no-project python3 "$LANE/real_costs_totals.py" --case oct16
uv run --no-project python3 -m pytest "$LANE/test_v9_transport.py" "$LANE/test_average_social_oct16.py" -q --import-mode=importlib
