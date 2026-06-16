#!/usr/bin/env bash
# Build lifetime evidence catalog DuckDB + union query views.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACQUIRE="$ROOT/acquire"
if [[ -f "$ACQUIRE/config.local.env" ]]; then
    # shellcheck source=config.local.env
    source "$ACQUIRE/config.local.env"
elif [[ -f "$ACQUIRE/config.env" ]]; then
    source "$ACQUIRE/config.env"
else
    source "$ACQUIRE/config.env.example"
fi
export PNY_DATA_ROOT DERIVED_ROOT DUCKDB_PATH
export LIFETIME_DUCKDB_PATH="${LIFETIME_DUCKDB_PATH:-$HOME/Projects/research/warehouse/immigration_lifetime_evidence.duckdb}"
export FISCAL_UNION_DUCKDB_PATH="${FISCAL_UNION_DUCKDB_PATH:-$HOME/Projects/research/warehouse/immigration_fiscal_union.duckdb}"
echo "Lifetime DuckDB: $LIFETIME_DUCKDB_PATH"
echo "Union DuckDB:    $FISCAL_UNION_DUCKDB_PATH"
uv run --with duckdb,pandas,openpyxl python "$ROOT/build/mine_restrictionist_full_claims.py"
bash "$ROOT/acquire/setup-restrictionist-panels.sh"
bash "$ROOT/acquire/setup-tier-a-labor-demography.sh"
uv run --with duckdb,pandas,openpyxl python "$ROOT/build/build_lifetime_evidence_warehouse.py"
uv run --with duckdb,pandas python "$ROOT/build/load_tier_a_context_panels.py"
if [[ -f "$DUCKDB_PATH" ]]; then
    uv run --with duckdb,pandas,openpyxl python "$ROOT/build/build_country_fiscal_tensor.py"
else
    echo "WARN: skip country fiscal tensor — $DUCKDB_PATH missing (run rebuild.sh)"
fi
