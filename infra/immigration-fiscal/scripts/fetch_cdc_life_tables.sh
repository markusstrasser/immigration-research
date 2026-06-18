#!/usr/bin/env bash
# Fetch CDC NVSR 72-12 period life table xlsx files (SSA table4c6 substitute).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../acquire/lib.sh
source "$HERE/../acquire/lib.sh"
immigration_fiscal_load_config

DEST="$PNY_DATA_ROOT/external/lifetime/cdc/nvsr72_12"
mkdir -p "$DEST"
BASE="https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/NVSR/72-12"

for i in $(seq -w 1 18); do
  url="$BASE/Table${i}.xlsx"
  out="$DEST/Table${i}.xlsx"
  [[ -s "$out" ]] && { echo "ok exists $out"; continue; }
  echo "fetch $url"
  curl -sSL --fail -o "$out.part" "$url"
  mv "$out.part" "$out"
  echo "ok $out ($(wc -c < "$out" | tr -d ' ') bytes)"
done

if command -v uv >/dev/null 2>&1; then
  uv run --with pandas,openpyxl python "$HERE/../build/parse_cdc_life_tables.py"
elif command -v python3 >/dev/null 2>&1; then
  PYTHONPATH="$HERE/../build" python3 "$HERE/../build/parse_cdc_life_tables.py"
fi
