#!/usr/bin/env bash
# run_all.sh — execute the immigration-causal analysis pipeline end-to-end.
#
# Each script is invoked via `uv run --with <deps> python3 …` so dependencies
# resolve per-script with no ambient pip install. Scripts are run in
# dependency order (data acquisition → merges → analyses).
#
# Logs to run_all.log. Exits non-zero on the first failure.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS="$HERE/scripts"
LOG="$HERE/run_all.log"
: > "$LOG"

PYTHONUNBUFFERED=1
export PYTHONUNBUFFERED

# Common dependency set used by every analysis script. Per-script overrides
# could be tighter but a single set keeps the runner simple and the deps list
# matches the constraint in README/MANIFEST.
DEPS=(numpy pandas requests pyarrow openpyxl pdfplumber)
WITH_FLAGS=()
for d in "${DEPS[@]}"; do WITH_FLAGS+=(--with "$d"); done

_log() { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }

_run() {
    local script="$1"
    _log "▸ $script"
    if uv run --quiet "${WITH_FLAGS[@]}" python3 "$SCRIPTS/$script" >>"$LOG" 2>&1; then
        _log "  ✓ $script"
    else
        _log "  ✗ $script (see $LOG)"
        exit 1
    fi
}

_log "=== immigration-causal run_all ==="
_log "scripts: $SCRIPTS"
_log "deps:    ${DEPS[*]}"

# --- 1. data acquisition (live Census pulls) ---
_run pull_acs_state_immigrant_share.py
_run pull_qwi_state_panel.py

# --- 2. merges ---
_run merge_saiz_rent_immigrant.py

# --- 3. cross-section analyses ---
_run saiz_decomposition.py
_run analyze_everify_wages.py
_run analyze_everify_employment.py
_run analyze_sanctuary_wages.py

# --- 4. calibrations ---
_run mass_deportation_sim.py
_run open_borders_baseline.py

# --- 5. cross-cut ---
_run analyze_internal_vs_immigrant_newcomers.py

_log "=== run_all OK ==="
_log "outputs in data/analysis/"
