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
echo "=== INT-06 status/citizenship harmonization spine ==="
uv run --with duckdb,pandas python "$ROOT/build/build_status_crosswalk.py"
echo "=== crime domain: represent SCAAP (INT-03) + Light TX (INT-01) + cross-views ==="
uv run --with duckdb,pandas,pdfplumber python "$ROOT/build/parse_scaap_awards.py"
uv run --with duckdb,pandas python "$ROOT/build/load_light_tx_crime.py"
uv run --with duckdb,pandas,pyreadstat python "$ROOT/build/load_spi_citizenship.py"
uv run --with duckdb python "$ROOT/build/build_crime_views.py"
echo "=== first-gen assimilation profile by origin x years-in-US (synthetic cohorts; skips if IPUMS microdata absent) ==="
uv run --with duckdb python "$ROOT/build/build_immigrant_assimilation_profile.py"
echo "=== cluster-V V02: 2nd-gen-by-origin cultural-transmission test (skips if gated IPUMS-CPS extract absent) ==="
uv run --with duckdb python "$ROOT/build/load_cps_second_gen.py"
