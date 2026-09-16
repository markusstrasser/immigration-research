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
# EOIR court-statistics CSVs (derived/stage4/eoir) feed three context tables. Parse them here,
# not only in acquire/setup.sh: a 2026-09-16 rebuild on a derived root without stage4/ silently
# dropped eoir_pending_cases_fy, eoir_court_workload_historical_fy and eoir_amnesty_cases_by_state.
uv run --with pdfplumber,pandas python "$ROOT/build/parse_eoir_court_pdfs.py" \
  || echo "WARN EOIR PDF parse failed — the three eoir_* context tables will be missing"
uv run --with duckdb,pandas,openpyxl python "$ROOT/build/build_immigration_warehouse.py"
echo "=== scenario compose ==="
uv run --with duckdb python "$ROOT/build/compose_scenario_ledger.py"
echo "=== INT-06 status/citizenship harmonization spine ==="
uv run --with duckdb,pandas python "$ROOT/build/build_status_crosswalk.py"
echo "=== crime domain: represent SCAAP (INT-03) + Light TX (INT-01) + cross-views ==="
uv run --with duckdb,pandas,pdfplumber python "$ROOT/build/parse_scaap_awards.py"
uv run --with duckdb,pandas python "$ROOT/build/load_light_tx_crime.py"
# The preceding warehouse initializer removes old SPI tables. Clear the two
# rederivable exports too, including when the optional raw source is unavailable.
rm -f -- "$DERIVED_ROOT/crime/spi_incarceration_rate.csv" \
  "$DERIVED_ROOT/crime/spi_inmates_by_citizenship_2016.csv"
if [[ -n "${SPI_DENOMINATOR_CSV+x}" ]]; then
  echo "SPI rates: validating the explicitly supplied matched 2016 denominator"
  uv run --with duckdb,pandas,pyreadstat python "$ROOT/build/load_spi_citizenship.py"
elif [[ -f "$PNY_DATA_ROOT/external/crime_frontier/spi/ICPSR_37692/DS0001/37692-0001-Data.dta" ]]; then
  echo "SPI counts only: incarceration rates intentionally absent without a matched 2016 denominator"
  uv run --with duckdb,pandas,pyreadstat python "$ROOT/build/load_spi_citizenship.py" --counts-only
else
  echo "[UNAVAILABLE] Optional SPI raw data not staged; SPI counts and rates absent"
fi
uv run --with duckdb python "$ROOT/build/build_crime_views.py"
echo "=== first-gen assimilation profile by origin x years-in-US (synthetic cohorts; skips if IPUMS microdata absent) ==="
uv run --with duckdb python "$ROOT/build/build_immigrant_assimilation_profile.py"
echo "=== cluster-V V02: descriptive second-generation profiles by origin (skips if gated IPUMS-CPS extract absent) ==="
uv run --with duckdb python "$ROOT/build/load_cps_second_gen.py"
