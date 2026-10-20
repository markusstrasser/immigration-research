#!/bin/sh
set -eu
LANE=infra/immigration-fiscal/main_case_decomposition_2026_09_29
run_node() {
    if [ -n "${CHAIN_CPU_PROFILE_DIR:-}" ]; then
        node --cpu-prof --cpu-prof-dir="$CHAIN_CPU_PROFILE_DIR" "$@"
    else
        node "$@"
    fi
}
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$LANE/profiles_oct16.py"
run_node "$LANE/decompose.cjs" --case oct16
run_node "$LANE/decompose.cjs" --case oct16_cash
run_node "$LANE/decompose.cjs" --case oct16 --placement identified
run_node "$LANE/decompose.cjs" --case oct16_cash --placement identified
GIT_OPTIONAL_LOCKS=0 uv run --no-project python3 -m pytest "$LANE/test_decomposition.py" -q
