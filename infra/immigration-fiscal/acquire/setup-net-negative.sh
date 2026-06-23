#!/usr/bin/env bash
# Stage-5: datasets that tighten fiscal / local-cost tests (net-negative hypothesis).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMMIGRATION_FISCAL_ROOT="$(cd "$HERE/.." && pwd)"
if [[ -f "$HERE/config.local.env" ]]; then
    source "$HERE/config.local.env"
elif [[ -f "$HERE/config.env" ]]; then
    source "$HERE/config.env"
else
    source "$HERE/config.env.example"
fi

S5="$PNY_DATA_ROOT/external/stage5_net_negative"
SCRIPTS="$(cd "$HERE/../scripts" && pwd)"
LOG="$HERE/setup.log"
_log()  { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }
_ok()   { _log "  ok   $*"; }
_warn() { _log "  warn $*"; }

_validate_file() {
    local dest="$1" min_bytes="${2:-512}"
    local sz
    sz=$(wc -c < "$dest" | tr -d ' ')
    [[ "$sz" -ge "$min_bytes" ]] || { rm -f "$dest"; return 1; }
    [[ "$dest" != *.zip ]] || unzip -tqq "$dest" 2>/dev/null
}

_fetch() {
    local url="$1" dest="$2" min="${3:-512}"
    mkdir -p "$(dirname "$dest")"
    [[ -s "$dest" ]] && _validate_file "$dest" "$min" && { _ok "exists $dest"; return 0; }
    _log "fetch(stage5) $url"
    if curl -sSL --fail --max-time 600 -o "$dest.part" "$url" \
        && _validate_file "$dest.part" "$min"; then
        mv "$dest.part" "$dest"
        _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes)"
        return 0
    fi
    rm -f "$dest.part" "$dest"
    _warn "skip $dest"
    return 0
}

_log "=== stage5 net-negative evidence datasets ==="
mkdir -p "$S5"/{cms,bea,nces,receiver,kff_refs,census,usda}

_fetch "https://data.medicaid.gov/api/1/datastore/query/5b19d1d4-ae43-5fcd-ba14-3cecd99f473f/0/download?format=csv" \
       "$S5/cms/medicaid_financial_management.csv" 100000
_fetch "https://www.bea.gov/sites/default/files/2024-12/rpp1224.xlsx" \
       "$S5/bea/rpp_state_metro_2024.xlsx" 10000
_fetch "https://apps.bea.gov/regional/zip/rpp_2023.zip" \
       "$S5/bea/rpp_2023.zip" 10000
_fetch "https://nces.ed.gov/ccd/Data/zip/ccd_lea_141_1819_l_1a_091019.zip" \
       "$S5/nces/ccd_lea_141_1819_english_learners.zip" 100000
_fetch "https://nces.ed.gov/ccd/Data/zip/ccd_lea_141_1718_l_1a_083118.zip" \
       "$S5/nces/ccd_lea_141_1718_english_learners.zip" 100000
_fetch "https://www2.census.gov/programs-surveys/gov-finances/tables/2022/2022_Individual_Unit_File.zip" \
       "$S5/census/gov_finances_2022_individual_unit.zip" 100000
_fetch "https://fns-prod.azureedge.us/sites/default/files/resource-files/snap-zip-fy69tocurrent-6.zip" \
       "$S5/usda/snap-zip-fy69tocurrent-6.zip" 500000

_fetch_hud_safmr() {
    local url="$1" dest="$2"
    mkdir -p "$(dirname "$dest")"
    [[ -s "$dest" ]] && _validate_file "$dest" 100000 && { _ok "exists $dest"; return 0; }
    _log "fetch(SAFMR) $url"
    if command -v uv >/dev/null 2>&1 && [[ -f "$SCRIPTS/fetch_browser.py" ]]; then
        if uv run --with playwright python "$SCRIPTS/fetch_browser.py" "$url" "$dest" \
            "https://www.huduser.gov/portal/datasets/fmr.html"; then
            _ok "$dest"
            return 0
        fi
    fi
    _warn "skip $dest (install playwright: uv run --with playwright python -m playwright install chromium)"
}
mkdir -p "$S5/hud"
_fetch_hud_safmr "https://www.huduser.gov/portal/datasets/fmr/fmr2025/fy2025_safmrs_revised.xlsx" \
                 "$S5/hud/fy2025_safmrs_revised.xlsx"

CAUSAL="${IMMIGRATION_CAUSAL_DATA:-$(cd "$HERE/../../.." && pwd)/sources/immigration-causal/data}"
CAUSAL_RC="$CAUSAL/bused_cities/receiver_city_costs.csv"
FIXTURE_RC="$IMMIGRATION_FISCAL_ROOT/fixtures/receiver_city_migrant_costs.csv"
if [[ -s "$CAUSAL_RC" ]]; then
    cp "$CAUSAL_RC" "$S5/receiver/receiver_city_migrant_costs.csv"
    _ok "copied receiver_city_migrant_costs.csv from immigration-causal"
elif [[ -s "$FIXTURE_RC" ]]; then
    cp "$FIXTURE_RC" "$S5/receiver/receiver_city_migrant_costs.csv"
    _ok "copied receiver_city_migrant_costs.csv from fixtures/"
else
    _warn "receiver_city_costs.csv missing at $CAUSAL_RC and $FIXTURE_RC"
fi

cat > "$S5/kff_refs/MANUAL_ACQUIRE.md" <<'EOF'
# Manual / browser acquisition (WAF or interactive export)

| Dataset | Why | URL |
|---------|-----|-----|
| KFF total Medicaid by state | State cost denominator | Automated substitute: `derived/stage5/cms_medicaid_state_panel.csv` (CMS data.medicaid.gov) |
| KFF immigrant health coverage facts | Disconfirms naive Medicaid drain | Automated substitute: `derived/stage5/acs_immigrant_health_state_summary_2023.csv` (ACS PUMS 2023) |
| CBO Emergency Medicaid FY17-23 | Emergency spend on noncitizens | https://www.cbo.gov/ |
| HUD CHAS Table 11 | County housing stress | Automated via `setup.sh` + Playwright (`2018thru2022-050-csv.zip`) |
| HUD SAFMR 2025 | Zip-level rent caps | Automated via `setup-net-negative.sh` + Playwright (`fy2025_safmrs_revised.xlsx`) |
| USDA SNAP state summaries | Transfer program scale | Automated via `setup-net-negative.sh` (`snap-zip-fy69tocurrent-6.zip` → FY23 panel) |
| TRAC immigration court backlog | Court-system cost proxy | EOIR PDFs → `eoir_pending_cases_fy.csv` (`context_09`) |
| NAS 2017 fiscal tables | Benchmark NPV by education | Automated: cloudfront PDF in `setup-lifetime.sh` |
| EDFacts FS141 district EL 2022-23 | Current district EL counts | ACS foreign-born school-age proxy + CCD 2018-19; Ed Data Express 403 from bots |
EOF

_log "=== stage5 done ==="
