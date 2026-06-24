#!/usr/bin/env bash
# Crime + frontier datasets (roadmap 2026-06-24): make the new acquisition targets
# reproducible on a fresh machine. Directly-public admin files are curl'd; WAF-blocked
# sources fall back to Playwright; registration/DUA-gated sources (ICPSR/openICPSR) are
# documented in MANUAL_ACQUIRE.md with exact study IDs + DOIs.
#
# Idempotent + non-fatal: re-running skips valid files; a dead URL warns and continues.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMMIGRATION_FISCAL_ROOT="$(cd "$HERE/.." && pwd)"
if [[ -f "$HERE/config.local.env" ]]; then source "$HERE/config.local.env"
elif [[ -f "$HERE/config.env" ]]; then source "$HERE/config.env"
else source "$HERE/config.env.example"; fi

CF="${PNY_DATA_ROOT:-$HOME/research-data/immigration-fiscal/data}/external/crime_frontier"
SCRIPTS="$(cd "$HERE/../scripts" && pwd)"
LOG="$HERE/setup.log"
_log()  { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }
_ok()   { _log "  ok   $*"; }
_warn() { _log "  warn $*"; }

_validate_file() {
    local dest="$1" min_bytes="${2:-512}" sz
    sz=$(wc -c < "$dest" | tr -d ' ')
    [[ "$sz" -ge "$min_bytes" ]] || { rm -f "$dest"; return 1; }
    # reject HTML error pages masquerading as PDFs
    [[ "$dest" != *.pdf ]] || head -c 5 "$dest" | grep -q '%PDF' || { rm -f "$dest"; return 1; }
    [[ "$dest" != *.zip ]] || unzip -tqq "$dest" 2>/dev/null
}

_fetch() {  # curl with validation; idempotent + non-fatal
    local url="$1" dest="$2" min="${3:-512}"
    mkdir -p "$(dirname "$dest")"
    [[ -s "$dest" ]] && _validate_file "$dest" "$min" && { _ok "exists $dest"; return 0; }
    _log "fetch $url"
    if curl -sSL --fail --max-time 600 \
            -A "Mozilla/5.0 (research-reproduce)" \
            -o "$dest.part" "$url" && _validate_file "$dest.part" "$min"; then
        mv "$dest.part" "$dest"; _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes)"; return 0
    fi
    rm -f "$dest.part" "$dest"; _warn "skip $dest (try MANUAL_ACQUIRE or Playwright)"; return 0
}

_fetch_browser() {  # Playwright fallback for WAF/403 sources (CBO, OECD, ORR)
    local url="$1" dest="$2" referer="${3:-}"
    mkdir -p "$(dirname "$dest")"
    [[ -s "$dest" ]] && _validate_file "$dest" 1024 && { _ok "exists $dest"; return 0; }
    if command -v uv >/dev/null 2>&1 && [[ -f "$SCRIPTS/fetch_browser.py" ]]; then
        _log "fetch(browser) $url"
        if uv run --with playwright python "$SCRIPTS/fetch_browser.py" "$url" "$dest" "$referer" \
            && _validate_file "$dest" 1024; then _ok "$dest"; return 0; fi
    fi
    _warn "skip $dest — WAF-blocked; install playwright or see MANUAL_ACQUIRE.md"
}

_log "=== crime + frontier datasets (roadmap 2026-06-24) ==="
mkdir -p "$CF"/{scaap,ice,cbo,orr,oecd,abs}

# --- Cluster A: crime — directly-public admin files (verified live 2026-06-24) ---
_fetch "https://bja.ojp.gov/funding/scaap-fy23-awards.pdf" \
       "$CF/scaap/scaap_fy23_awards.pdf" 100000           # DOJ SCAAP per-jurisdiction inmate-days + $
_fetch "https://www.ojp.gov/funding/docs/bja-2025-172612.pdf" \
       "$CF/scaap/scaap_fy25_solicitation.pdf" 100000     # SCAAP data elements / ICE country codes

# --- Cluster B: enforcement & cost — ICE ERO annual reports (removals by criminality) ---
_fetch "https://www.ice.gov/doclib/eoy/iceAnnualReportFY2024.pdf" \
       "$CF/ice/ice_ero_annual_fy2024.pdf" 500000
_fetch "https://www.ice.gov/doclib/eoy/iceAnnualReportFY2023.pdf" \
       "$CF/ice/ice_ero_annual_fy2023.pdf" 500000

# --- WAF-blocked (403/JS) → Playwright, else MANUAL ---
_fetch_browser "https://www.cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf" \
               "$CF/cbo/cbo_emergency_medicaid_noncitizens_2017_2023.pdf" "https://www.cbo.gov/"
_fetch_browser "https://www.govinfo.gov/content/pkg/CMR-HE25-00191253/pdf/CMR-HE25-00191253.pdf" \
               "$CF/orr/orr_annual_report_to_congress_fy2021.pdf" "https://www.govinfo.gov/"
_fetch_browser "https://www.oecd.org/en/publications/international-migration-outlook-2021_29f23e9d-en/full-report/component-8.html" \
               "$CF/oecd/oecd_imo2021_ch4_fiscal_impact.html" "https://www.oecd.org/"

# --- Census Annual Business Survey: owner nativity (USBORN) — API, needs DATA_GOV_API_KEY ---
if [[ -n "${DATA_GOV_API_KEY:-}" ]]; then
    _fetch "https://api.census.gov/data/2023/abscbo?get=NAME,NAICS2022_LABEL,OWNCHAR_LABEL,OWNPDEMP&QDESC_LABEL=USBORN&for=state:*&key=${DATA_GOV_API_KEY}" \
           "$CF/abs/abs_2023_owner_usborn_by_state.json" 1000
else
    _warn "ABS owner-nativity skipped — set DATA_GOV_API_KEY (see acquire/config.env.example)"
fi

# --- Health: NHIS sample-adult (nativity + insurance + utilization) — small, public, verified ---
mkdir -p "$CF/nhis"
_fetch "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2024/adult24csv.zip" \
       "$CF/nhis/nhis_2024_sample_adult.zip" 1000000
_fetch "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2023/adult23csv.zip" \
       "$CF/nhis/nhis_2023_sample_adult.zip" 1000000

# --- Registration / DUA-gated + large sources: precise pointers (not auto-fetched) ---
cat > "$CF/MANUAL_ACQUIRE.md" <<'EOF'
# Crime + frontier — manual / gated acquisition

These are NOT auto-fetchable: ICPSR/openICPSR require a free login + a Data Use Agreement
click-through (no stable direct URL). Download the listed file, drop it under the shown
`crime_frontier/<dir>/`, then it joins the build like the curl'd files.

## openICPSR (free registration, no institutional affiliation needed)
| Dataset | Study / DOI | Drop into |
|---------|-------------|-----------|
| Light/He/Robey — Texas arrest by immigration status, 2012–18 | openICPSR 124923 · DOI 10.3886/E124923V1 · https://www.openicpsr.org/openicpsr/project/124923 | `crime_frontier/light_texas/` |
| Abramitzky-Boustan-Jácome-Pérez — intergenerational mobility 1880–2015 | openICPSR 120490 · DOI 10.3886/E120490V1 · https://www.openicpsr.org/openicpsr/project/120490 | `crime_frontier/abjp_mobility/` |

## ICPSR / NACJD (login + Restricted/Public DUA; DS1 public-use files are general-access)
| Dataset | Study | Drop into |
|---------|-------|-----------|
| BJS Survey of Prison Inmates 2016 (DS1 public-use — citizenship of inmates) | ICPSR 37692 · https://www.icpsr.umich.edu/web/NACJD/studies/37692 | `crime_frontier/bjs_spi/` |
| BJS NCRP 1991–2021 (selected vars — corrections flow) | ICPSR 39234 · https://www.icpsr.umich.edu/web/NACJD/studies/39234 | `crime_frontier/bjs_ncrp/` |
| Immigration status, crime, victimization — Arizona 2007–23 | ICPSR 39107 · https://www.icpsr.umich.edu/web/NACJD/studies/39107 | `crime_frontier/az_crime/` |
| New Immigrant Survey R1/R2 (public-use added 2024) | ICPSR 38031 / 38061 · https://www.icpsr.umich.edu/web/DSDR/studies/38031 | `crime_frontier/nis/` |

## Direct-download pages (stable site, but page-driven / large — pull the year you need)
| Dataset | Page | Drop into |
|---------|------|-----------|
| US Sentencing Commission Individual Offender datafiles (citizenship var) | https://www.ussc.gov/research/datafiles/commission-datafiles | `crime_frontier/ussc/` |
| FBI NIBRS / Crime Data Explorer bulk (county + incident) | https://cde.ucr.cjis.gov | `crime_frontier/fbi_nibrs/` |
| SSA Earnings Public-Use File (1% CWHS earnings 1951–2006) | https://www.ssa.gov/policy/docs/data/index.html | `crime_frontier/ssa_epuf/` |
| Opportunity Atlas — 2nd-gen immigrant income ranks by origin | https://opportunityinsights.org/data | `crime_frontier/opp_atlas/` |
| AHS 2023 National PUF (housing burden/crowding; nativity sparse) — 129 MB, verified direct | https://www2.census.gov/programs-surveys/ahs/2023/AHS%202023%20National%20PUF%20v1.1%20CSV.zip | `crime_frontier/ahs/` |
| StatCan IMDB econ-outcomes table 43-10-0026 (admission-category × source-country fiscal) — 698 MB, verified direct | https://www150.statcan.gc.ca/n1/tbl/csv/43100026-eng.zip | `crime_frontier/statcan_imdb/` |
| NAWS Public Access Data (farmworker work-authorization status) | https://www.dol.gov/agencies/eta/national-agricultural-workers-survey/data/files-excel-csv | `crime_frontier/naws/` |
| DOL OFLC disclosure (H-1B/PERM/H-2A wages by occupation/state) | https://www.dol.gov/agencies/eta/foreign-labor/performance | `crime_frontier/oflc/` |

If a `_fetch_browser` PDF above still failed (CBO / OECD / ORR), grab it from the URL in
`setup-crime-frontier.sh` in a normal browser and drop it into the matching `crime_frontier/<dir>/`.
EOF
_ok "wrote $CF/MANUAL_ACQUIRE.md"

_log "=== crime + frontier done ==="
