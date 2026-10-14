#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/corporate_rents_2026_10_14
export OPENBLAS_NUM_THREADS=1
uv run --no-project python3 "$LANE/acquire.py"
node "$LANE/case_inputs.cjs"
uv run --no-project python3 "$LANE/rents.py"
uv run --no-project python3 "$LANE/write_result.py"
uv run --no-project python3 -m pytest -q -o cache_dir="$LANE/_cache/pytest" "$LANE/test_rents.py"
