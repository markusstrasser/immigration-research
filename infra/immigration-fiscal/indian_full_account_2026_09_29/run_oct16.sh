#!/bin/sh
# Independent Indian fiscal route. Social/combined publication has its own gate.
set -eu
LANE=infra/immigration-fiscal/indian_full_account_2026_09_29
export OPENBLAS_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/job_capital_factors.py" --foreign-source-removed
if [ -n "${INDIAN_ACCRUAL_PROFILE:-}" ]; then
    uv run --no-project python3 -m cProfile -o "$INDIAN_ACCRUAL_PROFILE" "$LANE/accrual_indian.py" --case oct16
else
    uv run --no-project python3 "$LANE/accrual_indian.py" --case oct16
fi
if [ -n "${INDIAN_FISCAL_PROFILE:-}" ]; then
    uv run --no-project python3 -m cProfile -o "$INDIAN_FISCAL_PROFILE" "$LANE/rekey_indian.py" --case oct16
else
    uv run --no-project python3 "$LANE/rekey_indian.py" --case oct16
fi
uv run --no-project python3 -m pytest -p no:cacheprovider "$LANE/test_social_engine.py" "$LANE/test_job_source_scope.py" "$LANE/test_v9_exports.py" -q
