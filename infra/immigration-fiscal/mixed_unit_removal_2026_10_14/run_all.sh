#!/bin/sh
# Native-First: one full deterministic lane replay, no Git mutations.
# removal.py executes round2.py, resource_keys.py, membership.py, pensions.py,
# tax_corrections.py, health.py and snap_arm.py on the shared canonical frame.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
lane=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
node "$lane/case_inputs.cjs"
uv run --no-project python3 "$lane/state_tax.py" --run
# The historical standalone snapshots and original controls remain live.
uv run --no-project python3 "$lane/benefits.py"
# Shared tax outputs are serialized by tax_corrections.write_results here;
# no duplicate 64-second standalone CPS/IRS account reconstruction is needed.
uv run --no-project python3 "$lane/removal.py"
uv run --no-project python3 -m pytest -p no:cacheprovider "$lane/test_removal.py" "$lane/test_state_tax.py" "$lane/test_benefits.py" "$lane/test_tax_corrections.py" "$lane/test_snap_arm.py" "$lane/test_resource_keys.py" "$lane/test_membership.py" "$lane/test_pensions.py" "$lane/test_health.py" "$lane/test_round2.py" -q
