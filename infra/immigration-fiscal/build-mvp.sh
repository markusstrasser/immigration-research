#!/usr/bin/env bash
# Rebuild public MVP modules (MEPS, SIPP, bridge, federal microsim).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACQUIRE="$ROOT/acquire"
if [[ -f "$ACQUIRE/config.local.env" ]]; then
    source "$ACQUIRE/config.local.env"
elif [[ -f "$ACQUIRE/config.env" ]]; then
    source "$ACQUIRE/config.env"
else
    source "$ACQUIRE/config.env.example"
fi
export PNY_DATA_ROOT DERIVED_ROOT DUCKDB_PATH
cd "$ROOT/build"
echo "=== public MVP rebuild ==="
uv run --with duckdb python build_public_mvp_meps_module.py
uv run --with duckdb python build_public_mvp_sipp_module_2024.py
uv run --with duckdb python build_public_mvp_sipp_meps_bridge_2024.py
uv run --with duckdb python build_federal_microsim_sipp_2024.py
echo "=== done ==="
ls -la "$DERIVED_ROOT/stage3_proto/"*.csv 2>/dev/null | tail -10
