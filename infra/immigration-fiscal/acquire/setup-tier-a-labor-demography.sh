#!/usr/bin/env bash
# Tier A #4-6: OECD SOCX, UN WPP, WB GDP, IPUMS staging hook, Razin-Wahba table extracts.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
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

OECD_DIR="$PNY_DATA_ROOT/external/oecd"
UN_DIR="$PNY_DATA_ROOT/external/un_wpp"
IPUMS_DIR="$PNY_DATA_ROOT/external/ipums"
mkdir -p "$OECD_DIR" "$UN_DIR" "$IPUMS_DIR/staging"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'

# OECD SOCX aggregated social expenditure (% GDP, public total) 1980-1995
OECD_JSON="$OECD_DIR/socx_agg_pct_gdp_1980_1995.json"
if [[ ! -s "$OECD_JSON" ]]; then
    echo "Fetching OECD SOCX (stats.oecd.org SDMX)..."
    curl -sL --max-time 120 -A "$UA" \
        "https://stats.oecd.org/SDMX-JSON/data/SOCX_AGG/TOT.PUB..PT_B1GQ/all?startTime=1980&endTime=1995" \
        -o "$OECD_JSON.part" || true
    if [[ -s "$OECD_JSON.part" ]] && python3 -c "import json; json.load(open('$OECD_JSON.part'))" 2>/dev/null; then
        mv "$OECD_JSON.part" "$OECD_JSON"
    else
        rm -f "$OECD_JSON.part"
        echo "WARN: OECD SOCX fetch failed — builder uses Razin-Wahba Table 1 anchors"
    fi
fi

# UN WPP location index + population series (Hanson Latin America panel)
LOC_JSON="$UN_DIR/locations.json"
if [[ ! -s "$LOC_JSON" ]]; then
    curl -sL --max-time 60 -A "$UA" \
        "https://population.un.org/dataportalapi/api/v1/locations?pagingInHeader=false&pageSize=500" \
        -o "$LOC_JSON"
fi

# IPUMS USA decennial extract — drop-in path (registration required for full 1960-2000 panel)
if [[ ! -f "$IPUMS_DIR/README.md" ]]; then
    cat >"$IPUMS_DIR/README.md" <<'EOF'
# IPUMS USA — Borjas/BGH decennial panel (Tier A #4)

Place harmonized IPUMS USA extract(s) here after `extract` request:
  `external/ipums/usa_extract/usa_00001.dat` (or `.dat.gz`)

Variables: YEAR, STATEFIP, EDUC, AGE, RACE, EMPSTAT, WKSWORK, GQ, PERWT, INCTOT, RACED

Until extract lands, builders use **ACS 2023 PUMS** person files for
`borjas_supply_shock_cell_2023` / `bgh_outcomes_cell_2023` (structure anchor only).

Request: https://usa.ipums.org/usa-action/samples
EOF
fi

uv run --with duckdb,pandas,requests python "$ROOT/build/build_tier_a_context_panels.py"
echo "Tier A panels staged under $DERIVED_ROOT/stage6/"
