#!/bin/sh
# White run_oct16.sh produces the shared engine leaves and symmetric tables.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
L=infra/immigration-fiscal/white_replacement_2026_09_28
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
uv run --no-project python3 "$B/accrual_black.py" --case oct16
node infra/immigration-fiscal/white_replacement_2026_09_28/dump_oct16.cjs
uv run --no-project python3 "$L/check_dumps_oct14.py"
uv run --no-project python3 "$L/export_keys_oct14.py"
uv run --no-project python3 "$B/rekey_sept29.py" --case oct16
uv run --no-project python3 "$B/accrual_black.py" --case oct16 --mortality
uv run --no-project python3 "$L/export_keys_oct14.py"
uv run --no-project python3 -m pytest -p no:cacheprovider "$B/test_benefit_totals.py" "$B/test_v8_programs.py" -q
