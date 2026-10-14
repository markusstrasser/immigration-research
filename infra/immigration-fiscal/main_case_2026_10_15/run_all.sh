#!/bin/sh
set -eu
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
lane=infra/immigration-fiscal/main_case_2026_10_15
uv run --no-project python3 "$lane/export_union_people.py"
uv run --no-project python3 "$lane/export_union_credit_parts.py" --check-existing
uv run --no-project python3 "$lane/mixed_overlap.py"
node "$lane/item_union.cjs"
node "$lane/coverage_check.cjs"
node "$lane/main_case.cjs"
node "$lane/sign_reversal.cjs"
node "$lane/lineage_addition.cjs"
node "$lane/api_check.cjs"
node "$lane/contract.cjs"
node "$lane/generality.cjs"
# Imported modules, validated by the commands above:
# package.cjs item_foreign.cjs item_mixed.cjs coverage.cjs companions.cjs child_records.cjs
# measure_run.py is the outer resource-measurement command, not a producer.
