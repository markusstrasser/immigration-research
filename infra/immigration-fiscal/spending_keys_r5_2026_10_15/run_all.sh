#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/spending_keys_r5_2026_10_15
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/build.py"
uv run --no-project python3 "$LANE/income_security.py"
uv run --no-project python3 "$LANE/college.py"
node "$LANE/evaluate.cjs"
uv run --no-project python3 -m pytest "$LANE/test_college.py" "$LANE/test_income_security.py" "$LANE/test_items.py" -q
