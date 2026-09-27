#!/usr/bin/env bash
# Rebuild the generation split end to end in dependency order; every script asserts its own gates,
# so the run stops at the first failure. Steps 0-6 took about a minute on 2026-09-27 (ten minutes when
# first written, seven of them in stack_split.py's ten hot-deck runs). The outputs are the main case of
# 2026-09-27 (--case sept27, main_case_long_run_2026_09_27: long-run road and park responses, rental
# assistance, the return on public capital, the government enterprises). The last three steps re-run the
# September 26 case, the schools case and the September 27 case, which must still pass and leave their
# lanes byte-identical (check `git status` on all three afterwards); they write outside this lane.
#   bash infra/immigration-fiscal/generation_account_2026_09_24/run_all.sh
# The schools case (--case sept26_schools, commit 0f22f0c), the one-year scenario (--case sept26,
# main_case_2026_09_26) and the September 24 record (--case sept24, commit ba12f3c) reproduce their outputs
# byte for byte after the same steps with
#   node "$LANE/run_generations.cjs" --case sept26_schools --out-dir DIR
#   uv run --no-project python3 "$LANE/compare_ledger.py" --out-dir DIR
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
step "4 consumption";  uv run --no-project --with openpyxl python3 "$LANE/consumption_split.py"
step "5 generations";  node "$LANE/run_generations.cjs"
step "6 ledger";       py "$LANE/compare_ledger.py"
step "main case, one-year scenario"; node "$LANE/../main_case_2026_09_26/main_case.cjs"
step "main case, schools"; node "$LANE/../main_case_schools_full_2026_09_26/main_case.cjs"
step "main case";      node "$LANE/../main_case_long_run_2026_09_27/main_case.cjs"
