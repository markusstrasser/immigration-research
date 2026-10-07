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
run "$L/g2_premium.py" --basis row4
run "$L/g2_premium.py" --basis lineage
run "$L/weights.py"
run "$L/weights.py" --basis row4
run "$L/weights.py" --basis lineage
for c in "${@:-sept26_schools}"; do
  node "$L/generation_lines.cjs" --case "$c"
  run "$L/split_residual.py" --case "$c"
done
run "$L/state_price_quantity.py"
run "$L/valuation.py"
for c in "${@:-sept26_schools}"; do
  run "$L/world_ledger.py" --case "$c"
  # The other population basis beside the case's own (population_basis.py): Sept 27 restated on the account's row-4
  # count, sept29 on the published CPS count it replaces, and oct05 and oct07 on row 4, without the added people in
  # their person-based rows.
  case "$c" in
    sept27) run "$L/world_ledger.py" --case "$c" --basis row4 ;;
    sept29) run "$L/world_ledger.py" --case "$c" --basis cps ;;
    oct05|oct07) run "$L/world_ledger.py" --case "$c" --basis row4 ;;
  esac
done
# The beside arms run on main case v6 alone, after its world ledger; acquire_beside.py stages their sources, as
# acquire.py does the rest.
case " $* " in
  *" oct07 "*) run "$L/beside_arms.py"; run "$L/beside_extra.py" ;;
esac
