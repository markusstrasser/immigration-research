#!/bin/sh
# Only oct15 outputs are computed. Oct14 filenames below are shared modules.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
L=infra/immigration-fiscal/white_replacement_2026_09_28
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
# Round 3 (C3 fix 4): every group's K-12 key; rekey_sept29.py reads it on oct15.
uv run --no-project python3 "$L/school_key_oct15.py"
uv run --no-project python3 "$L/accrual_white.py" --case oct15
uv run --no-project python3 "$B/accrual_black.py" --case oct15
node infra/immigration-fiscal/white_replacement_2026_09_28/dump_oct15.cjs
node "$L/test_dump_selection.cjs"
uv run --no-project python3 "$L/check_dumps_oct14.py"
uv run --no-project python3 "$L/export_keys_oct14.py"
uv run --no-project python3 "$L/rekey_sept29.py" --case oct15
uv run --no-project python3 "$B/rekey_sept29.py" --case oct15
uv run --no-project python3 -m pytest -p no:cacheprovider "$B/test_benefit_totals.py" "$B/test_v8_programs.py" -q
uv run --no-project python3 "$L/limits_oct14.py"
uv run --no-project python3 "$L/income_tax_parts.py" --case oct15
uv run --no-project python3 "$L/local_whites_fragility.py" --case oct15
uv run --no-project python3 -I "$L/local_whites_soi.py" --case oct15
node "$L/production_state_oct14.cjs"
uv run --no-project python3 "$L/accrual_white.py" --case oct15 --mortality
uv run --no-project python3 "$B/accrual_black.py" --case oct15 --mortality
# Round 3 (C3 fix 3a): the lineage's own-mortality ratios under the comparators' left-out-share mix.
uv run --no-project python3 "$L/lineage_mortality_mix_oct15.py"
uv run --no-project python3 "$L/status_keys_oct14.py"
# Round 3 (C3 fixes 1, 2): comparator coverage and the children rule; the mixed-unit lane reads its children targets.
uv run --no-project python3 "$L/members_coverage_oct15.py"
if [ "${PIN_COMPARATOR_INPUTS:-0}" = 1 ]; then
    uv run --no-project python3 "$L/symmetric_comparators_oct14.py" --pin
else
    uv run --no-project python3 "$L/symmetric_comparators_oct14.py"
fi
# Black rekey rewrites its income-tax key CSV; publish the source receipt only
# after both writers complete, so the held-out consumer checks those exact bytes.
uv run --no-project python3 "$L/export_keys_oct14.py"
uv run --no-project python3 "$L/render_oct15_result.py"
uv run --no-project python3 -m pytest -p no:cacheprovider "$L/test_job_policy_oct14.py" \
    "$L/test_scalar_policy_oct14.py" "$L/test_status_keys_oct14.py" "$L/test_mortality_comparators.py" \
    "$L/test_symmetric_tables_oct14.py" "$L/test_production_comparators_oct14.py" "$L/test_v8_transport.py" \
    "$L/test_mortality_conventions.py" "$L/test_comparison_contract.py" -q
