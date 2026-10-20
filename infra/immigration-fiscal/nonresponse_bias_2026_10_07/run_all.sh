#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/nonresponse_bias_2026_10_07
node "$LANE/v9_exposures.cjs"
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$LANE/reweight.py"
