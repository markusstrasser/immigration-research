#!/usr/bin/env bash
# Rebuild the generation split end to end in dependency order; every script asserts its own gates,
# so the run stops at the first failure. Steps 0-6 took about a minute on 2026-09-27 (ten minutes when
# first written, seven of them in stack_split.py's ten hot-deck runs). The outputs are the main case of
# 2026-09-27 (--case sept27, main_case_long_run_2026_09_27: long-run road and park responses, rental
# assistance, the return on public capital, the government enterprises). The last three steps re-run the
# September 26 case, the schools case and the September 27 case, which must still pass and leave their
# lanes byte-identical (check `git status` on all three afterwards); they write outside this lane.
# Step 7 is the main case adopted on 2026-09-29 (candidate v4's set; v4_split.cjs names its lane): the row-4
# and tax-key inputs, then --case sept29 and sept29_cash, which read step 5's outputs and write only
# *_sept29* files beside them.
# Step 8 is the main case adopted on 2026-10-05 (v5, main_case_2026_10_05: the September 29 case plus the lineage of
# descendants who no longer report Mexican origin): --case oct05 and oct05_cash read step 7's *_sept29* outputs
# (v5_split.cjs) and write only *_oct05* files beside them.
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
step "7 v4 inputs";    py "$LANE/v4_inputs.py"
step "7 v4 tax key";   uv run --no-project --with openpyxl --with xlrd python3 "$LANE/tax_key_split.py"
step "7 v4 case";      node "$LANE/run_generations_v4.cjs" --case sept29
step "7 v4 cash set";  node "$LANE/run_generations_v4.cjs" --case sept29_cash
step "8 v5 case";      node "$LANE/run_generations_v5.cjs" --case oct05
step "8 v5 cash set";  node "$LANE/run_generations_v5.cjs" --case oct05_cash
step "main case, one-year scenario"; node "$LANE/../main_case_2026_09_26/main_case.cjs"
step "main case, schools"; node "$LANE/../main_case_schools_full_2026_09_26/main_case.cjs"
step "main case";      node "$LANE/../main_case_long_run_2026_09_27/main_case.cjs"
