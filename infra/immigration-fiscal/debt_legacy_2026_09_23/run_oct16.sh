#!/bin/sh
# Native-First: execute the live source bridge and its existing regression checks.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
LANE=infra/immigration-fiscal/debt_legacy_2026_09_23
uv run --no-project python3 "$LANE/debt_legacy.py" --case oct16 --current-flow-only
uv run --no-project python3 "$LANE/military_history_oct16.py"
uv run --no-project python3 -m pytest "$LANE/test_v9_flow.py" "$LANE/test_v8_flow.py" -q --import-mode=importlib
