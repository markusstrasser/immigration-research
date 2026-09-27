#!/bin/sh
# Rebuild every derived file of the lane from the cached inputs (acquire.py fetches them), in dependency order.
# Run from the repository root:  sh infra/immigration-fiscal/world_ledger_2026_09_27/run_all.sh [case ...]
# generation_lines.cjs evaluates the generation lane's split of each case named here, and split_residual.py
# compares it with a split by the generations' shares of each line; valuation.py values every case with a winners
# pin and stops if one of them has no generation lines.
set -eu
L=infra/immigration-fiscal/world_ledger_2026_09_27
run() { OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$@"; }
run "$L/mexico.py"
run "$L/g2_premium.py"
run "$L/weights.py"
for c in "${@:-sept26_schools}"; do
  node "$L/generation_lines.cjs" --case "$c"
  run "$L/split_residual.py" --case "$c"
done
run "$L/valuation.py"
for c in "${@:-sept26_schools}"; do run "$L/world_ledger.py" --case "$c"; done
