#!/usr/bin/env bash
# Live-case propagation only; historical models and September 29 split files
# are frozen inputs. This route writes only oct14 and oct14_cash outputs.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
uv run --no-project python3 "$LANE/credit_routing.py"
uv run --no-project python3 "$LANE/state_price_routing.py"
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v7.cjs" --case oct14
uv run --no-project python3 "$LANE/measured_run.py" node "$LANE/run_generations_v7.cjs" --case oct14_cash
uv run --no-project python3 "$LANE/routing_audit.py"
node --test "$LANE/test_routing.cjs"
uv run --no-project python3 -m pytest "$LANE" -q -o "cache_dir=$LANE/_cache/pytest"
