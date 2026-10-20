#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/public_charge_share_2026_10_07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$LANE/public_charge_share.py"
