#!/usr/bin/env bash
# Rebuild the generation split end to end in dependency order; every script asserts its own gates,
# so the run stops at the first failure. About ten minutes, seven of them in stack_split.py's ten
# hot-deck runs. The last step re-runs the adopted main case, which must still pass and leave its
# lane byte-identical (check `git status` on main_case_2026_09_24 afterwards).
#   bash infra/immigration-fiscal/generation_account_2026_09_24/run_all.sh
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
py() { uv run --no-project python3 "$@"; }
step() { echo; echo "[$1]"; }

step "0 masks";        py -m pytest "$LANE/test_masks.py" -q -p no:cacheprovider
step "0 parents";      py "$LANE/parents_check.py"
step "0 mixed units";  py "$LANE/mixed_units.py"
step "1 keys";         py "$LANE/keys.py"
step "3 production";   py "$LANE/production.py"
step "2 models";       py "$LANE/build_models.py"
step "4 stack";        py "$LANE/stack_split.py"
step "4 external";     uv run --no-project --with openpyxl python3 "$LANE/external_split.py"
step "4 rules";        py "$LANE/correction_rules.py"
step "5 generations";  node "$LANE/run_generations.cjs"
step "6 ledger";       py "$LANE/compare_ledger.py"
step "main case";      node "$LANE/../main_case_2026_09_24/main_case.cjs"
