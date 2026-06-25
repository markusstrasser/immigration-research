#!/usr/bin/env bash
# Urban housing-panel datasets (frontier 2026-06-25): the MSA rent × foreign-born-share ×
# supply-elasticity panel the repo lacked (only a 2022 Saiz cross-section existed). Spec'd in
# research/immigration-urbanism-frontier-2026-06-25.md; feeds E-cluster theories E-001..E-008 and
# replicates Wilson & Zhou (2026, Dallas Fed WP2607) causal magnitudes (+2.2% prices / +1.4% rents).
#
# Auto-fetches the verified-live public files (Zillow ZORI/ZHVI). The supply-side moderators that
# need a one-time download or an on-demand generator (WRLURI2018, Geocorr PUMA↔CBSA crosswalk, LODES)
# are documented in MANUAL_ACQUIRE.md with exact pointers + the Geocorr query spec.
#
# Idempotent + non-fatal: re-running skips valid files; a dead URL warns and continues.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$HERE/config.local.env" ]]; then source "$HERE/config.local.env"
elif [[ -f "$HERE/config.env" ]]; then source "$HERE/config.env"
else source "$HERE/config.env.example"; fi

UH="${PNY_DATA_ROOT:-$HOME/research-data/immigration-fiscal/data}/external/urban_housing"
LOG="$HERE/setup.log"
_log()  { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }
_ok()   { _log "  ok   $*"; }
_warn() { _log "  warn $*"; }

_validate_file() {
    local dest="$1" min_bytes="${2:-512}" sz
    sz=$(wc -c < "$dest" | tr -d ' ')
    [[ "$sz" -ge "$min_bytes" ]] || { rm -f "$dest"; return 1; }
    # a real Zillow CSV starts with the RegionID header, not an HTML error page
    [[ "$dest" != *.csv ]] || head -c 200 "$dest" | grep -qiE 'RegionID|RegionName' || { rm -f "$dest"; return 1; }
}

_fetch() {  # curl with validation; idempotent + non-fatal
    local url="$1" dest="$2" min="${3:-512}"
    mkdir -p "$(dirname "$dest")"
    [[ -s "$dest" ]] && _validate_file "$dest" "$min" && { _ok "exists $dest"; return 0; }
    _log "fetch $url"
    if curl -sSL --fail --max-time 600 -A "Mozilla/5.0 (research-reproduce)" \
            -o "$dest.part" "$url" && _validate_file "$dest.part" "$min"; then
        mv "$dest.part" "$dest"; _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes)"; return 0
    fi
    rm -f "$dest.part" "$dest"; _warn "skip $dest (URL moved? see MANUAL_ACQUIRE.md)"; return 0
}

_log "=== urban housing-panel datasets (frontier 2026-06-25) ==="
mkdir -p "$UH"/{zillow,wrluri,geocorr,lodes}

# --- Tier A: rent / price outcome (the dependent variable) — Zillow, verified live 2026-06-25 ---
# ZORI = Observed Rent Index (repeat-rent, ACS-stock-weighted, $); the Wilson-Zhou (2026) outcome var.
_fetch "https://files.zillowstatic.com/research/public_csvs/zori/Metro_zori_uc_sfrcondomfr_sm_month.csv" \
       "$UH/zillow/metro_zori_sfrcondomfr_sm_month.csv" 100000
# ZHVI = Home Value Index (middle-tier, smoothed, seasonally-adjusted) — owner-side incidence.
_fetch "https://files.zillowstatic.com/research/public_csvs/zhvi/Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv" \
       "$UH/zillow/metro_zhvi_sfrcondo_tier_sm_sa_month.csv" 100000

# --- Supply-side moderators + geography spine: one-time DL / on-demand generator → MANUAL ---
cat > "$UH/MANUAL_ACQUIRE.md" <<'EOF'
# Urban housing panel — manual / on-demand acquisition

The Zillow ZORI/ZHVI metro panels auto-fetch above. These three need a one-time download or an
on-demand generator (no stable direct CSV URL); pull each and drop into the shown dir.

## WRLURI 2018 — Wharton Residential Land Use Regulatory Index (Gyourko-Hartley-Krimmel 2021 JUE)
- The 2018 wave + the 2006→2018 change panel (the only consistent national change-in-regulation measure).
- Canonical: https://real-faculty.wharton.upenn.edu/gyourko/land-use-survey/
- Author mirror (direct files): http://www.jonathanhartley.net/data  ("Gyourko, Hartley, and Krimmel (2021) WRLURI 2018 Data files")
- 2,472 communities; 2,333 aggregable to CBSA; aggregate index mean 0 / SD 1. Drop into `urban_housing/wrluri/`.

## Geocorr 2022 — PUMA ↔ CBSA crosswalk (the join key for the warehouse PUMA rent layer)
- On-demand generator (no static URL): https://mcdc.missouri.edu/applications/geocorr2022.html
- Query spec: State = (all); Source geography = **PUMA (2020)** [use 2010 PUMA only for pre-2022 microdata];
  Target geography = **Core-based statistical area (CBSA)**; Weighting variable = **housing units** (HU2020)
  for a rent panel, or population (POP2020) for person-weighting. Output = CSV with AFACT allocation factors.
- Resolves the Saiz-memo Limitation 4 (MSA Saiz/WRLURI/Zillow ↔ PUMA warehouse unit-mismatch). Drop into `urban_housing/geocorr/`.
- Quirk: Geocorr cannot crosswalk ACROSS decades (blocks change) — match the PUMA vintage to the ACS year.

## LODES / LEHD — workplace×residence employment flows (spatial-mismatch axis, new)
- https://lehd.ces.census.gov/data/  (Origin-Destination Employment Statistics; WAC/RAC). Block-level → aggregate
  to CBSA/PUMA. Heavy; pull per-state OD files for the metros of interest. Drop into `urban_housing/lodes/`.

## ACS housing-by-nativity (the treatment + outcome levels) — pulled by the build, not here
- Census API, no file stage needed: B05002 (foreign-born), B25064 (median gross rent), B25003 (tenure),
  B25070 (rent-as-%-income), B19013 (income), at CBSA + PUMA, 2010→2023. B25127 is the file Zillow weights to.
EOF
_ok "wrote $UH/MANUAL_ACQUIRE.md"

_log "=== urban housing-panel done ==="
