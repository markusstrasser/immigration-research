#!/bin/sh
# One live case parameter. Historical keyed outputs are never rebuilt.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
L=infra/immigration-fiscal/world_ledger_2026_09_27
if [ "$#" -eq 0 ]; then set -- oct15; fi
if [ "$#" -ne 1 ]; then
  echo '[BLOCKED] pass one live case key' >&2
  exit 1
fi
case "$1" in sept*|oct05|oct07|oct14)
  echo '[BLOCKED] historical outputs are preserved' >&2; exit 1 ;;
esac
uv run --no-project python3 "$L/run_oct15.py" --case "$1"
