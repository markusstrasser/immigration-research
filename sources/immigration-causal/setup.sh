#!/usr/bin/env bash
# setup.sh — re-acquire all external datasets for immigration-causal.
#
# Idempotent: skips files that already exist with non-zero size.
# Writes data/<subdir>/.checksum (sha256) for each successful download.
# Exits non-zero if any REQUIRED dataset fails. WRLURI is marked optional and
# logged as a known-dead skip.
#
# Run from sources/immigration-causal/. No arguments.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA="$HERE/data"
LOG="$HERE/setup.log"

: > "$LOG"

_log()  { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }
_ok()   { _log "  ok   $*"; }
_warn() { _log "  warn $*"; }
_fail() { _log "  FAIL $*"; }

# sha256 helper that works on macOS (shasum) and Linux (sha256sum)
_sha256() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    else
        shasum -a 256 "$1" | awk '{print $1}'
    fi
}

# head_check URL → 0 if 2xx/3xx, 1 otherwise
_head_check() {
    local url="$1"
    local code
    code=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 30 -I "$url" || echo "000")
    case "$code" in
        2*|3*) return 0 ;;
        *) _warn "HEAD $url → HTTP $code"; return 1 ;;
    esac
}

# fetch URL DEST [--required|--optional]
_fetch() {
    local url="$1" dest="$2" required="${3:---required}"
    mkdir -p "$(dirname "$dest")"
    if [[ -s "$dest" ]]; then
        _ok "exists $dest"
        _sha256 "$dest" > "$(dirname "$dest")/.checksum"
        return 0
    fi
    _log "fetch $url → $dest"
    if ! _head_check "$url"; then
        if [[ "$required" == "--required" ]]; then
            _fail "$dest (HEAD check failed)"
            return 1
        else
            _warn "$dest skipped (optional, source unreachable)"
            return 0
        fi
    fi
    if curl -sSL --fail --max-time 600 -o "$dest.part" "$url"; then
        mv "$dest.part" "$dest"
        local sum; sum=$(_sha256 "$dest")
        echo "$sum  $(basename "$dest")" > "$(dirname "$dest")/.checksum"
        _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes, sha256=${sum:0:12}…)"
        return 0
    else
        rm -f "$dest.part"
        if [[ "$required" == "--required" ]]; then
            _fail "$dest (download failed)"
            return 1
        else
            _warn "$dest skipped (optional, download failed)"
            return 0
        fi
    fi
}

ERRORS=0

_log "=== immigration-causal setup ==="
_log "data root: $DATA"

# 1. Saiz 2010 MSA elasticity
_fetch "https://web.mit.edu/asaiz/www/data/saiz_2010_msa_elasticity.dta" \
       "$DATA/saiz/saiz_2010_msa_elasticity.dta" --required \
    || ERRORS=$((ERRORS+1))

# 2. BEA Supply-Use bundle (zip), then extract the two xlsx targets we need
BEA_ZIP="$DATA/bea_io/AllTablesSUP.zip"
_fetch "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesSUP.zip" \
       "$BEA_ZIP" --required \
    || ERRORS=$((ERRORS+1))

if [[ -s "$BEA_ZIP" ]]; then
    if [[ ! -s "$DATA/bea_io/Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx" ]]; then
        if unzip -o -j "$BEA_ZIP" \
            "Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx" \
            -d "$DATA/bea_io/" >>"$LOG" 2>&1; then
            _ok "extracted Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx"
        else
            _fail "could not extract Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx (BEA may have renamed)"
            ERRORS=$((ERRORS+1))
        fi
    fi
    if [[ ! -s "$DATA/bea_io/Use_SUT_Framework_2017_DET.xlsx" ]]; then
        if unzip -o -j "$BEA_ZIP" \
            "Use_SUT_Framework_2017_DET.xlsx" \
            -d "$DATA/bea_io/" >>"$LOG" 2>&1; then
            _ok "extracted Use_SUT_Framework_2017_DET.xlsx"
        else
            _warn "could not extract Use_SUT_Framework_2017_DET.xlsx (optional, used by future detail decomposition)"
        fi
    fi
fi

# 3. IRS SOI county-to-county migration 2022-23
_fetch "https://www.irs.gov/pub/irs-soi/countyinflow2223.csv" \
       "$DATA/internal_migration/county_inflow_2022_23.csv" --required \
    || ERRORS=$((ERRORS+1))
_fetch "https://www.irs.gov/pub/irs-soi/countyoutflow2223.csv" \
       "$DATA/internal_migration/county_outflow_2022_23.csv" --required \
    || ERRORS=$((ERRORS+1))

# 4. Clemens 2011 JEP PDF (reference; calibration script doesn't need it)
_fetch "https://www.aeaweb.org/articles/pdf/doi/10.1257/jep.25.3.83" \
       "$DATA/clemens/clemens_2011.pdf" --optional

# 5. WRLURI 2018 — known dead since early 2025
_log "skip  WRLURI 2018 (Wharton link dead since early 2025; Saiz .dta ships"
_log "      2008 WRLURI which is what saiz_decomposition.py actually uses)"

# 6. Sanity-check hand-compiled panels are present (in repo, not downloaded)
for f in "$DATA/everify/everify_state_mandates.csv" \
         "$DATA/sanctuary/sanctuary_state_panel.csv" \
         "$DATA/daca/daca_timeline_and_design.md" \
         "$DATA/clemens/open_borders_calibration_baseline.json"; do
    if [[ -s "$f" ]]; then
        _ok "in-repo $f"
    else
        _warn "in-repo missing: $f (should be checked into git; see MANIFEST.md)"
    fi
done

_log ""
if (( ERRORS == 0 )); then
    _log "=== setup OK ==="
    exit 0
else
    _log "=== setup FAILED ($ERRORS required dataset(s) missing) ==="
    exit 1
fi
