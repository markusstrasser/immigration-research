#!/usr/bin/env bash
# Live case only. Frozen inputs and earlier case outputs are read, never rebuilt.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for reading in central lower upper; do
  LATE_DEF="$reading" uv run --no-project python3 "$LANE/job_wages.py"
  node "$LANE/run_cells.cjs" --case oct14 --def "$reading"
  node "$LANE/run_cells.cjs" --case oct14_cash --def "$reading"
done
uv run --no-project python3 "$LANE/build_line.py" --set oct14
uv run --no-project python3 "$LANE/medicaid_check.py" --set oct14
uv run --no-project python3 "$LANE/verify.py" --set oct14
