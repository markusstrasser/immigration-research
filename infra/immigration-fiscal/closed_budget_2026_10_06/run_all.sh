#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/closed_budget_2026_10_06
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$LANE/households.py" --case oct16
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 "$LANE/trust_funds.py"
uv run --no-project python3 "$LANE/pin_oct16.py"
uv run --no-project python3 "$LANE/closed_budget.py" --case oct16
uv run --no-project python3 "$LANE/closed_budget.py" --case oct16 --v9-mixed-baskets net-unlocated --out-dir "$LANE/derived/oct16_net_unlocated"
uv run --no-project python3 -m pytest "$LANE/test_closed_budget.py" "$LANE/test_calibrated_frame.py" -q
