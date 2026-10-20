#!/usr/bin/env bash
# Live outputs only; v8 source construction is inherited in memory, never published.
# Native-First: the existing shell/Node/Python lane entry points.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/production.py" --check-grid-order
for reading in central lower upper; do
  node "$LANE/run_cells.cjs" --case oct16 --def "$reading"
  node "$LANE/run_cells.cjs" --case oct16_cash --def "$reading"
done
uv run --no-project python3 "$LANE/build_line.py" --set oct16
uv run --no-project python3 "$LANE/medicaid_check.py" --set oct16
uv run --no-project python3 "$LANE/oct16_diagnostics.py"
uv run --no-project python3 "$LANE/verify.py" --set oct16
