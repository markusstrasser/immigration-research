#!/bin/sh
# Phase 2 generation core. Full world valuation needs winners/distribution/debt.
set -eu
L=infra/immigration-fiscal/world_ledger_2026_09_27
# core_contract.py imports valuation.py and executes its incidence declarations.
# check_tests.py covers test_live_contract.py and test_oct15_core.py in the full suite.
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for set in set cash; do
  uv run --no-project python3 "$L/measured_run.py" node "$L/generation_lines.cjs" --case oct15 --set "$set"
  uv run --no-project python3 "$L/measured_run.py" uv run --no-project python3 "$L/split_residual.py" --case oct15 --set "$set"
done
uv run --no-project python3 "$L/measured_run.py" uv run --no-project python3 "$L/core_contract.py"
