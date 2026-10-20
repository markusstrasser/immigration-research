#!/usr/bin/env bash
# Live-case propagation only; historical models and oct15 files are frozen inputs.
# This route writes only oct16 and oct16_cash outputs.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
node "$LANE/../scripts/adoption_gate.cjs" oct16
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v9.cjs" --case oct16
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v9.cjs" --case oct16_cash
node --test "$LANE/test_routing.cjs" "$LANE/test_native_parent_gradients_v8.cjs"
uv run --no-project python3 "$LANE/check_tests_v8.py" \
  "$LANE/test_masks.py" "$LANE/test_credit_routing.py" \
  "$LANE/test_credit_replicates_v8.py" "$LANE/test_minor_parent_measurement_v8.py" \
  "$LANE/test_union_credit_age_v8.py" "$LANE/test_direct_adults_v8.py"
