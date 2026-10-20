#!/bin/sh
# Native-First: preserve the source estimators and their explicit policy vintages.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
LANE=infra/immigration-fiscal/post2024_law_2026_10_07
uv run --no-project python3 "$LANE/post2024_law.py"
uv run --no-project --with taxcalc==6.8.4 python3 "$LANE/tax_side.py"
uv run --no-project python3 "$LANE/policy_scope.py"
uv run --no-project --with taxcalc==6.8.4 python3 -m pytest "$LANE/test_live_scope.py" -q --import-mode=importlib
