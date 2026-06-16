#!/usr/bin/env bash
# Tier-A restrictionist panels: HUD PIT CoC + Gould Table 1 staging.
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
export PNY_DATA_ROOT DERIVED_ROOT

HUD_DIR="$PNY_DATA_ROOT/external/hud"
XLSB="$HUD_DIR/2007-2024-PIT-Counts-by-CoC.xlsb"
mkdir -p "$HUD_DIR"

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'
REF='https://www.huduser.gov/portal/datasets/ahar/2024-ahar-part-1-pit-estimates-of-homelessness-in-the-us.html'
URL='https://www.huduser.gov/portal/sites/default/files/xls/2007-2024-PIT-Counts-by-CoC.xlsb'

if [[ ! -f "$XLSB" ]] || [[ $(stat -f%z "$XLSB" 2>/dev/null || stat -c%s "$XLSB") -lt 1000000 ]]; then
    echo "Downloading HUD PIT by CoC workbook..."
    curl -sL --max-time 180 -A "$UA" -H "Referer: $REF" -o "$XLSB" "$URL"
fi

uv run --with duckdb,pandas,pyxlsb python "$ROOT/build/build_restrictionist_panels.py"
echo "Restrictionist panels staged under $DERIVED_ROOT/stage5/"
