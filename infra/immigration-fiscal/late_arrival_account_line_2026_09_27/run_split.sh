#!/usr/bin/env bash
# The generation lane's split steps (generation_account_2026_09_24/run_all.sh, copied at 0f22f0c) with the G1
# cells of frame.py, for one age-at-arrival reading. Every script asserts its own gates; the run stops at the
# first failure. Outputs: _cache/split_<reading>/.
# The v4 steps (the sept29 case) run the generation lane's two input scripts on this lane's frame (V4_LANE_DIR):
# v4_inputs.json (row-4 production, tenant shares, row-4 headcounts) and tax_key_by_generation.json.
#   LATE_DEF=central bash infra/immigration-fiscal/late_arrival_account_line_2026_09_27/run_split.sh
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
GEN="$(cd "$LANE/../generation_account_2026_09_24" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LATE_DEF="${LATE_DEF:-central}"
py() { uv run --no-project python3 "$@"; }
step() { echo; echo "[$1 · $LATE_DEF]"; }
step "1 keys";         py "$LANE/keys.py"
step "3 production";   py "$LANE/production.py"
step "2 models";       py "$LANE/build_models.py"
step "4 stack";        py "$LANE/stack_split.py"
step "4 external";     uv run --no-project --with openpyxl python3 "$LANE/external_split.py"
step "4 rules";        py "$LANE/correction_rules.py"
step "4 consumption";  uv run --no-project --with openpyxl python3 "$LANE/consumption_split.py"
step "7 v4 inputs";    V4_LANE_DIR="$LANE" uv run --no-project python3 "$GEN/v4_inputs.py"
step "7 v4 tax key";   V4_LANE_DIR="$LANE" uv run --no-project --with openpyxl --with xlrd python3 "$GEN/tax_key_split.py"
echo "[done · $LATE_DEF]"
