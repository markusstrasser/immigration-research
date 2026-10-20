#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/main_case_2026_10_16
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
export NODE_OPTIONS="--max-old-space-size=1536"
# Runtime dependencies invoked by producers below (also the rerun inventory):
# memory_for_pid.py via memory_guard.cjs; coverage_snapshot.cjs via coverage_oct16.py.
mkdir -p "$LANE/_cache"
node "$LANE/test_readiness.cjs"
node "$LANE/source_check.cjs"
uv run --no-project python3 "$LANE/market_check.py"
uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_oct16.py
node "$LANE/coverage_check.cjs"
node "$LANE/rate_check.cjs"
node "$LANE/main_case.cjs"
node "$LANE/sign_reversal.cjs"
node "$LANE/lineage_addition.cjs"
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v9.cjs --case oct16
node infra/immigration-fiscal/generation_account_2026_09_24/run_generations_v9.cjs --case oct16_cash
node "$LANE/api_check.cjs"
node "$LANE/generality.cjs"
node "$LANE/contract.cjs"
uv run --no-project python3 "$LANE/write_result.py"
