#!/usr/bin/env bash
# Live-case propagation only; historical models and September 29 split files
# are frozen inputs. This route writes only oct15 and oct15_cash outputs.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/measure_minor_parents_v8.py"
uv run --no-project python3 "$LANE/credit_routing.py" --export-oct15-replicates
uv run --no-project python3 "$LANE/union_credit_age_v8.py"
uv run --no-project python3 "$LANE/state_price_routing.py"
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v8.cjs" --case oct15
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v8.cjs" --case oct15_cash
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/native_parent_gradients_v8.cjs" --case-final "$LANE/inputs/case_final_oct15.txt"
uv run --no-project python3 "$LANE/routing_audit.py"
uv run --no-project python3 "$LANE/direct_adults_v8.py"
uv run --no-project python3 "$LANE/allocation_uncertainty_v8.py"
node --test "$LANE/test_routing.cjs" "$LANE/test_native_parent_gradients_v8.cjs"
uv run --no-project python3 "$LANE/check_tests_v8.py" \
  "$LANE/test_masks.py" "$LANE/test_credit_routing.py" \
  "$LANE/test_credit_replicates_v8.py" "$LANE/test_minor_parent_measurement_v8.py" \
  "$LANE/test_union_credit_age_v8.py" "$LANE/test_direct_adults_v8.py"
