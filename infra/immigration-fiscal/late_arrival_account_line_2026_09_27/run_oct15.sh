#!/usr/bin/env bash
# Live case only, explicit final-generation SHA256 snapshot; no old outputs rebuilt.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/production.py" --check-grid-order
uv run --no-project python3 "$LANE/reporter_fine_routes.py"
for reading in central lower upper; do
  LATE_DEF="$reading" uv run --no-project python3 "$LANE/job_wages.py"
  node "$LANE/run_cells.cjs" --case oct15 --def "$reading"
  node "$LANE/run_cells.cjs" --case oct15_cash --def "$reading"
done
uv run --no-project python3 "$LANE/build_line.py" --set oct15
uv run --no-project python3 "$LANE/medicaid_check.py" --set oct15
uv run --no-project python3 "$LANE/verify.py" --set oct15
