#!/bin/sh
# Run after the white lane's run_oct14.sh; this re-key consumes its dumps.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
B=infra/immigration-fiscal/black_comparator_rough_2026_09_28
uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/rekey_sept29.py --case oct14 --preflight
uv run --no-project python3 "$B/accrual_black.py" --case oct14
for c in oct14 oct14_cash oct14_union oct14_union_cash; do
    node "$B/engine_lines.cjs" "$c"
done
uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/check_dumps_oct14.py
uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/export_keys_oct14.py
uv run --no-project python3 "$B/rekey_sept29.py" --case oct14
