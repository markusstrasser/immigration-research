#!/usr/bin/env bash
# Rebuild immigration_context.duckdb (aggregates). Requires acquire/setup.sh first.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=acquire/lib.sh
source "$ROOT/acquire/lib.sh"
immigration_fiscal_load_config
export PNY_DATA_ROOT DERIVED_ROOT DUCKDB_PATH CORPUS_ROOT
echo "DuckDB target: $DUCKDB_PATH"
echo "Data root:     $PNY_DATA_ROOT"
echo "Derived:       $DERIVED_ROOT"
uv run --with duckdb,pandas,openpyxl python "$ROOT/build/build_immigration_warehouse.py"
echo "=== scenario compose ==="
uv run --with duckdb python "$ROOT/build/compose_scenario_ledger.py"
