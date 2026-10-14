#!/bin/sh
# Rebuild the live case and case-independent inputs from cache, preserving historical keyed outputs.
# Run from the repository root: sh infra/immigration-fiscal/world_ledger_2026_09_27/run_all.sh [oct14]
# generation_lines.cjs and split_residual.py take the committed generation split; valuation.py also needs winners;
# world_ledger.py needs distribution; beside_extra.py needs the debt lane's oct14 federal split.
set -eu
L=infra/immigration-fiscal/world_ledger_2026_09_27
if [ "$#" -eq 0 ]; then set -- oct14; fi
if [ "$#" -ne 1 ] || [ "$1" != oct14 ]; then
  echo '[BLOCKED] run_all.sh computes only the live oct14 case; historical outputs are preserved' >&2
  exit 1
fi
run() { OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$@"; }
run "$L/mexico.py"
run "$L/g2_premium.py"
run "$L/g2_premium.py" --basis row4
run "$L/g2_premium.py" --basis lineage
run "$L/weights.py"
run "$L/weights.py" --basis row4
run "$L/weights.py" --basis lineage
node "$L/generation_lines.cjs" --case oct14
run "$L/split_residual.py" --case oct14
run "$L/state_price_quantity.py"
run "$L/valuation.py" --case oct14
run "$L/world_ledger.py" --case oct14
# The row-4 companion excludes the added people from its person-based rows, as before.
run "$L/world_ledger.py" --case oct14 --basis row4
run "$L/beside_arms.py"
run "$L/beside_extra.py"
