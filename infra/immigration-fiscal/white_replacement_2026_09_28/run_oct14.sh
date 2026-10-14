#!/bin/sh
# Compute only the live case. Earlier keyed outputs are preserved inputs.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
L=infra/immigration-fiscal/white_replacement_2026_09_28
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
uv run --no-project python3 "$L/rekey_sept29.py" --case oct14 --preflight
uv run --no-project python3 "$L/accrual_white.py" --case oct14
uv run --no-project python3 "$B/accrual_black.py" --case oct14
for c in oct14 oct14_cash oct14_union oct14_union_cash; do
    node "$L/engine_lines.cjs" "$c"
done
uv run --no-project python3 "$L/check_dumps_oct14.py"
uv run --no-project python3 "$L/export_keys_oct14.py"
uv run --no-project python3 "$L/rekey_sept29.py" --case oct14
uv run --no-project python3 "$L/limits_oct14.py"
uv run --no-project python3 "$L/income_tax_parts.py" --case oct14
uv run --no-project python3 "$L/local_whites_fragility.py" --case oct14
uv run --no-project python3 -I "$L/local_whites_soi.py" --case oct14
# Symmetric comparators (2026-10-14 critique round): own production, mortality, status keys.
node "$L/production_state_oct14.cjs"
uv run --no-project python3 "$L/accrual_white.py" --mortality
uv run --no-project python3 "$B/accrual_black.py" --mortality
uv run --no-project python3 "$L/status_keys_oct14.py"
uv run --no-project python3 "$L/symmetric_comparators_oct14.py"
uv run --no-project python3 "$L/render_symmetric_result.py"
uv run --no-project python3 -m pytest -p no:cacheprovider "$L/test_job_policy_oct14.py" \
    "$L/test_scalar_policy_oct14.py" "$L/test_status_keys_oct14.py" "$L/test_mortality_comparators.py" \
    "$L/test_symmetric_tables_oct14.py" "$L/test_production_comparators_oct14.py" -q
