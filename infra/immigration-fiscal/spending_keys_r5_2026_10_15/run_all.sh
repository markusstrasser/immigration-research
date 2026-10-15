#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/spending_keys_r5_2026_10_15
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/build.py"
uv run --no-project python3 "$LANE/income_security.py"
uv run --no-project python3 "$LANE/college.py"
node "$LANE/evaluate.cjs"
node "$LANE/health_snapshot.cjs"
uv run --no-project python3 "$LANE/health_residual.py"
node "$LANE/health_evaluate.cjs" --out-dir "$LANE/derived"
node --test "$LANE/test_health_item.cjs"
uv run --no-project python3 -m pytest "$LANE/test_college.py" "$LANE/test_income_security.py" "$LANE/test_items.py" "$LANE/test_health_ratios.py" "$LANE/test_health_coverage.py" "$LANE/test_health_residual.py" -q
