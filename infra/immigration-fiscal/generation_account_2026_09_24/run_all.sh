#!/usr/bin/env bash
# Live-case propagation only; historical models and September 29 split files
# are frozen inputs. This route writes only oct14 and oct14_cash outputs.
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
cd "$LANE/../../.."
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
node "$LANE/run_generations_v7.cjs" --case oct14
node "$LANE/run_generations_v7.cjs" --case oct14_cash
