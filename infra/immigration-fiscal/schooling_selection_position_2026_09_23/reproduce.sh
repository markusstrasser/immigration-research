#!/bin/sh
# Rebuild every table in derived/ from the cached inputs (INEGI files, IPUMS extracts #3/#12/#13,
# the repository's ACS 2015 PUMS and CPS extract). Run from the repository root.
set -e
L=infra/immigration-fiscal/schooling_selection_position_2026_09_23
for s in fetch_inegi origin_inegi position cps_check acs_pums_check instrument_checks; do
  echo "== $s"
  OPENBLAS_NUM_THREADS=1 PYTHONUNBUFFERED=1 uv run --no-project --with xlrd python3 "$L/$s.py"
done
