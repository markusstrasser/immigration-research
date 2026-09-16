#!/usr/bin/env bash
# Second supplement for the Mexican-origin cut: detailed Hispanic origin, earnings, labor-force status, poverty.
# Writes $PNY_DATA_ROOT/external/cps/asec/asec_<year>_supp2.json. Key never printed.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$ROOT/acquire/config.local.env"
KEY="${CENSUS_API_KEY:-}"
[[ -n "$KEY" ]] || KEY=$(rg -o '^\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*"?([^"\s#]+)"?' -r '$1' "$CFG" | head -1 || true)
[[ -n "$KEY" ]] || { echo "[DEGRADED] no CENSUS_API_KEY" >&2; exit 2; }
ROOT_DATA="${PNY_DATA_ROOT:-$(rg -o '^\s*(?:export\s+)?PNY_DATA_ROOT\s*=\s*"?([^"\s#]+)"?' -r '$1' "$CFG" | head -1 || true)}"
[[ -n "$ROOT_DATA" ]] || { echo "[DEGRADED] PNY_DATA_ROOT unset" >&2; exit 2; }
OUT="$ROOT_DATA/external/cps/asec"; mkdir -p "$OUT"
VARS=H_SEQ,PPPOS,PRDTHSP,PEARNVAL,WSAL_VAL,PEMLR,PERLIS,POVLL,SPM_POOR,A_WKSTAT
YEARS=("$@"); [[ ${#YEARS[@]} -eq 0 ]] && YEARS=(2025 2024)
for y in "${YEARS[@]}"; do
  out="$OUT/asec_${y}_supp2.json"
  if [[ -s "$out" ]] && tail -c 8 "$out" | rg -q '\]\]'; then echo "[$y/supp2] exists, keep"; continue; fi
  tmp="$out.building"
  code=$(curl -s --max-time 900 -o "$tmp" -w "%{http_code}" "https://api.census.gov/data/$y/cps/asec/mar?get=$VARS&for=state:*&key=$KEY")
  if [[ "$code" == "200" ]] && tail -c 8 "$tmp" | rg -q '\]\]'; then mv "$tmp" "$out"; echo "[$y/supp2] ok $(wc -c < "$out") bytes $(date +%H:%M:%S)"
  else echo "[DEGRADED] [$y/supp2] http=$code: $(head -c 200 "$tmp" | sed "s/$KEY/KEY/g")" >&2; rm -f "$tmp"; exit 1; fi
done
