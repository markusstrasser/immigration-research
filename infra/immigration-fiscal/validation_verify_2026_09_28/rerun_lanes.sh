#!/usr/bin/env bash
# Rerun one of the five validation lanes with scripts/rerun_lane.py, then its tests.
# Usage, from the repository root: bash infra/immigration-fiscal/validation_verify_2026_09_28/rerun_lanes.sh <key>
# Keys: audit schools medical fiscal mariel. Commands are the lanes' documented ones (README or RESULT),
# with `-p no:cacheprovider` added to pytest so a test run writes nothing into the lane.
set -uo pipefail
L=infra/immigration-fiscal
R="uv run --no-project python3 scripts/rerun_lane.py"
A="UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache"
V="UV_CACHE_DIR=/private/tmp/immigration-validation-uv-cache"
Y="UV_CACHE_DIR=/private/tmp/immigration-years-uv"
MW="--with scipy --with pandas --with numpy"
case "$1" in
  audit)
    $R $L/validation_audit_2026_09_28 \
      "$A uv run --no-project python3 {lane}/gss_baseline.py" \
      "OPENBLAS_NUM_THREADS=1 $A uv run --no-project python3 {lane}/snap_loso.py"
    echo "rerun_rc=$?"; echo "tests: none in this lane" ;;
  schools)
    $R $L/validation_schools_2026_09_28 \
      "OPENBLAS_NUM_THREADS=1 $V uv run --no-project python3 {lane}/validate.py --source-root $PWD"
    echo "rerun_rc=$?"
    env ${V} uv run --no-project python3 -m unittest discover -s $L/validation_schools_2026_09_28 -p 'test_*.py' -v 2>&1
    echo "test_rc=$?" ;;
  medical)
    $R $L/validation_medical_2026_09_28 \
      "$A uv run --no-project python3 {lane}/acquire.py" \
      "$A OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/analysis.py"
    echo "rerun_rc=$?"
    env ${A} uv run --no-project python3 -m pytest -q -p no:cacheprovider $L/validation_medical_2026_09_28/test_analysis.py 2>&1
    echo "test_rc=$?" ;;
  fiscal)
    $R $L/validation_fiscal_years_2026_09_28 \
      "$Y OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 {lane}/analysis.py --source-root $PWD"
    echo "rerun_rc=$?"
    env ${Y} OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest -q -p no:cacheprovider \
      $L/validation_fiscal_years_2026_09_28/test_analysis.py 2>&1
    echo "test_rc=$?" ;;
  mariel)
    $R $L/validation_mariel_2026_09_28 \
      "OPENBLAS_NUM_THREADS=1 $V uv run --no-project $MW python3 {lane}/joint_budget.py"
    echo "rerun_rc=$?"
    env ${V} OPENBLAS_NUM_THREADS=1 uv run --no-project $MW python3 -m unittest discover \
      -s $L/validation_mariel_2026_09_28 -p 'test_*.py' -v 2>&1
    echo "test_rc=$?" ;;
  *) echo "unknown key: $1" >&2; exit 2 ;;
esac
