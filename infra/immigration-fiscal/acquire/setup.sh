#!/usr/bin/env bash
# setup.sh — re-acquire immigration-fiscal public datasets (canonical copy in git).
# Idempotent: skips valid non-empty files. Configure paths in acquire/config.local.env.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$HERE/lib.sh"
immigration_fiscal_load_config
DATA="$PNY_DATA_ROOT"
LOG="$HERE/setup.log"
SCRIPTS="$IMMIGRATION_FISCAL_ROOT/scripts"
: > "$LOG"

_log()  { printf '[%(%H:%M:%S)T] %s\n' -1 "$*" | tee -a "$LOG"; }
_ok()   { _log "  ok   $*"; }
_warn() { _log "  warn $*"; }
_fail() { _log "  FAIL $*"; }

_sha256() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | awk '{print $1}'
    else
        shasum -a 256 "$1" | awk '{print $1}'
    fi
}

# Reject WAF/HTML traps: empty files, tiny payloads, broken zips.
_validate_file() {
    local dest="$1" min_bytes="${2:-512}"
    local sz
    sz=$(wc -c < "$dest" | tr -d ' ')
    if [[ "$sz" -lt "$min_bytes" ]]; then
        _warn "reject $dest (${sz}B < ${min_bytes}B min — likely WAF/HTML trap)"
        rm -f "$dest"
        return 1
    fi
    if [[ "$dest" == *.zip ]]; then
        if ! unzip -tqq "$dest" 2>/dev/null; then
            _warn "reject $dest (invalid zip)"
            rm -f "$dest"
            return 1
        fi
    fi
    if [[ "$dest" == *.xlsx ]]; then
        if ! unzip -tqq "$dest" 2>/dev/null; then
            _warn "reject $dest (invalid xlsx)"
            rm -f "$dest"
            return 1
        fi
    fi
    return 0
}

_head_ok() {
    local url="$1"
    local code
    code=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 30 -I "$url" 2>/dev/null || echo "000")
    case "$code" in 2*|3*) return 0 ;; *) return 1 ;; esac
}

_fetch() {
    local url="$1" dest="$2" required="${3:---required}" max_time="${4:-900}"
    mkdir -p "$(dirname "$dest")"
    if [[ -s "$dest" ]]; then
        _ok "exists $dest"
        return 0
    fi
    _log "fetch $url"
    if ! _head_ok "$url"; then
        _warn "HEAD failed for $url — trying GET"
    fi
    if curl -sSL --fail --max-time "$max_time" -o "$dest.part" "$url"; then
        mv "$dest.part" "$dest"
        if _validate_file "$dest"; then
            _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes)"
            return 0
        fi
    fi
    rm -f "$dest.part" "$dest"
    [[ "$required" == "--required" ]] && { _fail "$dest"; return 1; }
    _warn "skip $dest (optional, download failed)"; return 0
}

# APIs and HUD/MEPS endpoints often reject HEAD; always GET.
_fetch_get() {
    _fetch "$1" "$2" "${3:---optional}" "${4:-3600}"
}

# HUD CHAS — WAF blocks curl; try Playwright if available, else skip.
_fetch_hud_chas() {
    local url="$1" dest="$2"
    mkdir -p "$(dirname "$dest")"
    if [[ -s "$dest" ]] && _validate_file "$dest" 10240; then
        _ok "exists $dest"
        return 0
    fi
    rm -f "$dest"
    _log "fetch(HUD) $url"
    if curl -sSL --fail --max-time 120 -A "Mozilla/5.0" \
        -H "Referer: https://www.huduser.gov/portal/datasets/chas.html" \
        -o "$dest.part" "$url" \
        && _validate_file "$dest.part" 10240; then
        mv "$dest.part" "$dest"
        _ok "$dest"
        return 0
    fi
    rm -f "$dest.part"
    if command -v uv >/dev/null 2>&1 && [[ -f "$SCRIPTS/fetch_hud_chas.py" ]]; then
        _log "HUD curl failed — trying Playwright"
        if uv run --with playwright python "$SCRIPTS/fetch_hud_chas.py" "$url" "$dest"; then
            if _validate_file "$dest" 10240; then
                _ok "$dest (playwright)"
                return 0
            fi
            rm -f "$dest"
        fi
    fi
    _warn "skip $dest (HUD — download manually from https://www.huduser.gov/portal/datasets/cp.html or install playwright)"
    return 0
}

ERRORS=0
_log "=== immigration-fiscal setup ==="
_log "PNY data root: $DATA"
_log "corpus root:   $CORPUS_ROOT"

# --- MANIFEST base (Mar 2026) ---
_fetch "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pus.zip" \
       "$DATA/census/acs_pums_2023_person.zip" --required || ERRORS=$((ERRORS+1))
_fetch "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_hus.zip" \
       "$DATA/census/acs_pums_2023_household.zip" --required || ERRORS=$((ERRORS+1))
_fetch "https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asecpub24csv.zip" \
       "$DATA/census/cps_asec_2024_march.zip" --required || ERRORS=$((ERRORS+1))

if [[ "${REPRODUCE_TIER:-standard}" == "minimal" ]]; then
    _log "REPRODUCE_TIER=minimal — skipping optional downloads"
    if (( ERRORS == 0 )); then
        _log "=== setup OK (minimal tier) ==="
        exit 0
    fi
    _log "=== setup FAILED ($ERRORS required download(s) missing) ==="
    exit 1
fi

_fetch "https://data.bls.gov/cew/data/files/2023/csv/2023_annual_by_industry.zip" \
       "$DATA/bls/qcew_2023_annual_by_industry.zip" --optional
_fetch "https://www.dhs.gov/sites/default/files/2024-04/2024_0314_us_customs_and_border_protection.pdf" \
       "$DATA/dhs/cbp_fy25_budget_justification.pdf" --optional
_fetch "https://www.dhs.gov/sites/default/files/2025-06/25_0613_cbp_fy26-congressional-budget-justificatin.pdf" \
       "$DATA/dhs/cbp_fy26_budget_justification.pdf" --optional
_fetch "https://www.dhs.gov/sites/default/files/2024-04/2024_0308_us_immigration_and_customs_enforcement.pdf" \
       "$DATA/dhs/ice_fy25_budget_justification.pdf" --optional
_fetch "https://www.dhs.gov/sites/default/files/2025-06/25_0613_ice_fy26-congressional-budget-justificatin.pdf" \
       "$DATA/dhs/ice_fy26_budget_justification.pdf" --optional
_fetch "https://www.irs.gov/pub/irs-soi/24dbs01t02nr.xlsx" \
       "$DATA/irs/24dbs01t02nr.xlsx" --optional
_fetch "https://sfo2.digitaloceanspaces.com/itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf" \
       "$DATA/itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf" --optional
_fetch "https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf" \
       "$DATA/cbo/60569-immigration-federal.pdf" --optional
_fetch "https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf" \
       "$DATA/cbo/61256-immigration-state-local.pdf" --optional
_fetch "https://nces.ed.gov/programs/digest/d23/tables/xls/tabn236.10.xlsx" \
       "$DATA/nces/tabn236.10.xlsx" --optional
_fetch "https://www.pewresearch.org/wp-content/uploads/sites/20/2025/08/RE_2025.08.21_Unauthorized-Immigrants_REPORT.pdf" \
       "$DATA/pew/pew-unauthorized-immigrants-2025.pdf" --optional
_fetch "https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_state.txt" \
       "$DATA/external/fhfa_hpi_po_state.txt" --optional

# Census school finance 2023 (district + summary tables)
_fetch_get "https://www2.census.gov/programs-surveys/school-finances/tables/2023/secondary-education-finance/elsec23.txt" \
       "$DATA/external/census_school_finance_2023.txt" --optional
_fetch_get "https://www2.census.gov/programs-surveys/school-finances/tables/2023/secondary-education-finance/elsec23t.txt" \
       "$DATA/external/census_school_finance_2023_summary.txt" --optional

# --- Origin layer (immigration-origin-data-stack) ---
_fetch "https://api.worldbank.org/v2/country?format=json&per_page=400" \
       "$DATA/external/origin/worldbank_country_metadata.json" --optional
_fetch "https://api.census.gov/data/2023/acs/acs1/groups/B05006.json" \
       "$DATA/external/origin/census_acs1_2023_B05006_metadata.json" --optional
_fetch "https://api.census.gov/data/2023/acs/acs1?get=NAME,group(B05006)&for=state:*" \
       "$DATA/external/origin/census_acs1_2023_B05006_state_origin.json" --optional
_fetch "https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2023_ACSSubjectDefinitions.pdf" \
       "$DATA/external/origin/census_2023_subject_definitions.pdf" --optional
_fetch "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/code_lists/ACSPUMS2019_2023CodeLists.xlsx" \
       "$DATA/external/origin/ACSPUMS2019_2023CodeLists.xlsx" --optional
_fetch "https://api.census.gov/data/2023/acs/acs1?get=NAME,B25064_001E&for=state:*" \
       "$DATA/external/origin/census_acs1_2023_state_median_gross_rent.json" --optional
_fetch "https://ohss.dhs.gov/sites/default/files/2023-12/plcy_lpr_by_country_of_birth_by_major_class_fy2005-2022_d.xlsx" \
       "$DATA/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx" --optional
_fetch "https://ohss.dhs.gov/sites/default/files/2023-12/plcy_lpr_counties_top_200_fy2022_d.xlsx" \
       "$DATA/external/origin/ohss/lpr_counties_top_200_fy2022.xlsx" --optional
mkdir -p "$DATA/external/origin/ohss"

# PUMA median rent (ACS API dump for local-burden layer)
_fetch_get "https://api.census.gov/data/2023/acs/acs1?get=NAME,B25064_001E&for=public%20use%20microdata%20area:*" \
       "$DATA/external/origin/census_acs1_2023_puma_median_gross_rent.json" --optional

# --- Stage 2 county bridge ---
_fetch "https://www2.census.gov/programs-surveys/sipp/data/datasets/2023/pu2023_csv.zip" \
       "$DATA/external/stage2/census/sipp/pu2023_csv.zip" --optional
_fetch "https://www.irs.gov/pub/irs-soi/countyinflow2223.csv" \
       "$DATA/external/stage2/irs/countyinflow2223.csv" --optional
_fetch "https://www.irs.gov/pub/irs-soi/countyoutflow2223.csv" \
       "$DATA/external/stage2/irs/countyoutflow2223.csv" --optional
_fetch "https://www.irs.gov/pub/irs-soi/stateinflow2223.csv" \
       "$DATA/external/stage2/irs/stateinflow2223.csv" --optional
_fetch "https://www.irs.gov/pub/irs-soi/stateoutflow2223.csv" \
       "$DATA/external/stage2/irs/stateoutflow2223.csv" --optional
_fetch_hud_chas "https://www.huduser.gov/portal/datasets/cp/2018thru2022-050-csv.zip" \
       "$DATA/external/stage2/hud/chas/2018thru2022-050-csv.zip"
_fetch_hud_chas "https://www.huduser.gov/portal/datasets/cp/2018thru2022-040-csv.zip" \
       "$DATA/external/stage2/hud/chas/2018thru2022-040-csv.zip"
_fetch_hud_chas "https://www.huduser.gov/portal/datasets/cp/2018thru2022-140-csv.zip" \
       "$DATA/external/stage2/hud/chas/2018thru2022-140-csv.zip"
_fetch_hud_chas "https://www.huduser.gov/portal/datasets/cp/CHAS-data-dictionary-18-22.xlsx" \
       "$DATA/external/stage2/hud/chas/CHAS-data-dictionary-18-22.xlsx"
_fetch_get "https://nces.ed.gov/ccd/Data/zip/ccd_lea_029_2324_w_1a_073124.zip" \
       "$DATA/external/stage2/nces/ccd_lea_029_2324_w_1a_073124.zip" --optional
_fetch_get "https://nces.ed.gov/ccd/Data/zip/ccd_sch_029_2324_w_1a_073124.zip" \
       "$DATA/external/stage2/nces/ccd_sch_029_2324_w_1a_073124.zip" --optional
# PUMA ↔ county-subdivision crosswalk (stage2 county bridge)
_fetch_get "https://www2.census.gov/geo/docs/maps-data/data/rel2020/puma520/tab20_puma520_cousub20_natl.txt" \
       "$DATA/external/stage2/census/geo/tab20_puma520_cousub20_natl.txt" --optional
_fetch_get "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt" \
       "$DATA/external/stage2/census/geo/tab20_zcta520_county20_natl.txt" --optional

# --- Stage 3 public MVP (SIPP + MEPS) ---
_fetch "https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_csv.zip" \
       "$DATA/external/stage3/census/sipp/pu2024_csv.zip" --optional
_fetch_get "https://www2.census.gov/programs-surveys/sipp/data/datasets/2024/pu2024_schema.json" \
       "$DATA/external/stage3/census/sipp/pu2024_schema.json" --optional
_fetch "https://www2.census.gov/programs-surveys/sipp/tech-documentation/2024/2024_SIPP_Release_Notes.pdf" \
       "$DATA/external/stage3/census/sipp/2024_SIPP_Release_Notes.pdf" --optional
_fetch "https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf" \
       "$DATA/external/stage3/census/sipp/2024_SIPP_Users_Guide.pdf" --optional
_fetch "https://www2.census.gov/programs-surveys/sipp/SIPP_Data_Primer_MAY24.pdf" \
       "$DATA/external/stage3/census/sipp/SIPP_Data_Primer_MAY24.pdf" --optional
_fetch_get "https://www.census.gov/programs-surveys/sipp/guidance/research-guidance/synthetic_sipp.html" \
       "$DATA/external/stage3/census/sipp/synthetic_sipp_landing.html" --optional
MEPS_DOC="https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h251"
MEPS_ZIP="https://meps.ahrq.gov/mepsweb/data_files/pufs/h251"
for pair in \
    "h251doc.pdf:$MEPS_DOC" \
    "h251cb.pdf:$MEPS_DOC" \
    "h251su.txt:$MEPS_DOC" \
    "h251spu.txt:$MEPS_DOC" \
    "h251stu.txt:$MEPS_DOC" \
    "h251ru.txt:$MEPS_DOC" \
    "h251dat.zip:$MEPS_ZIP" \
    "h251ssp.zip:$MEPS_ZIP" \
    "h251v9.zip:$MEPS_ZIP" \
    "h251dta.zip:$MEPS_ZIP" \
    "h251xlsx.zip:$MEPS_ZIP"; do
    f="${pair%%:*}"; base="${pair#*:}"
    _fetch_get "${base}/${f}" "$DATA/external/stage3/ahrq/meps/${f}" --optional 7200
done

# --- Stage 4 school / courts ---
_fetch "https://www2.census.gov/programs-surveys/saipe/datasets/2023/2023-school-districts/ussd23.txt" \
       "$DATA/external/stage4/saipe/ussd23.txt" --optional
_fetch "https://www2.census.gov/programs-surveys/saipe/datasets/2023/2023-school-districts/ussd23.xls" \
       "$DATA/external/stage4/saipe/ussd23.xls" --optional
_fetch "https://www2.census.gov/programs-surveys/saipe/technical-documentation/file-layouts/school-district/2023-district-layout.txt" \
       "$DATA/external/stage4/saipe/2023-district-layout.txt" --optional
_fetch "https://languageaccess.courts.ca.gov/system/files/2025-07/2025%20Language%20Need%20and%20Interpreter%20Use%20Study.pdf" \
       "$DATA/external/stage4/courts/ca_language_need_interpreter_use_2025.pdf" --optional
_fetch "https://www.courts.wa.gov/content/Financial%20Services/documents/2025_2027/Biennial/BD%20Stabilize%20Interpreter%20Reimbursement%20Program.pdf" \
       "$DATA/external/stage4/courts/wa_interpreter_reimbursement_2025_2027.pdf" --optional
_fetch "https://www.nyc.gov/assets/immigrants/downloads/pdf/Local-Law-6-Report_MOIA_2024.pdf" \
       "$DATA/external/stage4/courts/nyc_local_law_6_report_2024.pdf" --optional
_fetch_get "https://nces.ed.gov/ccd/datatables/api/File/2/5/38/7/10/38" \
       "$DATA/external/stage4/nces/nces_ccd_file_tool_lea_2023_2024_v1a.json" --optional
_fetch "https://nces.ed.gov/ccd/doc/SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx" \
       "$DATA/external/stage4/nces/SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx" --optional
_fetch "https://nces.ed.gov/ccd/xls/SY_2023-24_Final_1a_Data_Notes.xlsx" \
       "$DATA/external/stage4/nces/SY_2023-24_Final_1a_Data_Notes.xlsx" --optional
_fetch "https://nces.ed.gov/ccd/xls/SY_2023-24_LEA_Membership_Companion_2024-252.xlsx" \
       "$DATA/external/stage4/nces/SY_2023-24_LEA_Membership_Companion_2024-252.xlsx" --optional

# Corpus ACS zip (large mirror — skip if present)
if [[ ! -s "$CORPUS_ROOT/census_acs/csv_pus.zip" ]]; then
    _fetch "https://www2.census.gov/programs-surveys/acs/data/pums/2023/1-Year/csv_pus.zip" \
           "$CORPUS_ROOT/census_acs/csv_pus.zip" --optional 7200
fi

# --- Corpus: IRS SOI county migration panel (2011–12 … 2021–22) ---
IRS_MIG="$CORPUS_ROOT/irs_soi/migration"
mkdir -p "$IRS_MIG"
for y in 1112 1213 1314 1415 1516 1617 1718 1819 1920 2021 2122; do
    for kind in countyinflow countyoutflow stateinflow stateoutflow; do
        _fetch_get "https://www.irs.gov/pub/irs-soi/${kind}${y}.csv" \
                   "$IRS_MIG/${kind}${y}.csv" --optional
    done
done

# --- BLS LAUS county unemployment (monthly panel seed) ---
LAUS="$DATA/external/stage2/bls/laus"
mkdir -p "$LAUS"
_laus_fetch() {
    local f="$1"
    local dest="$LAUS/$f"
    [[ -s "$dest" ]] && { _ok "exists $dest"; return 0; }
    _log "fetch(LAUS) $f"
    if curl -sSL --fail --max-time 600 -A "Mozilla/5.0" \
        -o "$dest.part" "https://download.bls.gov/pub/time.series/la/${f}"; then
        mv "$dest.part" "$dest"
        _ok "$dest"
    else
        rm -f "$dest.part"
        _warn "skip $dest (LAUS download failed)"
    fi
}
for f in la.series la.measure la.area la.data.64.County; do
    _laus_fetch "$f"
done

# --- State immigration / refugee arrivals (OHSS; replaces dead ACF ORR CSV) ---
_fetch "https://ohss.dhs.gov/sites/default/files/2025-05/state_data_2013-2023_20250514_3.csv" \
       "$DATA/external/origin/ohss/state_immigration_data_2013_2023.csv" --optional
# Legacy ORR path (404 as of 2026-06); kept for manifest compat — OHSS file is canonical.
_fetch_get "https://acf.gov/sites/default/files/orr/ry2023_arrivals_by_state.csv" \
       "$DATA/external/origin/orr/ry2023_arrivals_by_state.csv" --optional

# --- CBP southwest encounters CSV (needs browser UA) ---
CAUSAL="${IMMIGRATION_CAUSAL_DATA:-$(cd "$HERE/../../.." && pwd)/sources/immigration-causal/data}"
mkdir -p "$CAUSAL/cbp/raw"
_cbp_fetch() {
    local url="$1" dest="$2"
    if [[ -s "$dest" ]]; then _ok "exists $dest"; return 0; fi
    _log "fetch(CBP) $url"
    if curl -sSL --fail --max-time 120 -A "Mozilla/5.0" -o "$dest.part" "$url"; then
        mv "$dest.part" "$dest"
        _ok "$dest"
    else
        rm -f "$dest.part"
        _warn "skip $dest (CBP download failed)"
    fi
}
_cbp_fetch "https://www.cbp.gov/sites/default/files/2025-11/sbo-encounters-fy22-fy25.csv" \
           "$CAUSAL/cbp/raw/sbo_encounters_fy22_fy25.csv"
_cbp_fetch "https://www.cbp.gov/sites/default/files/2026-05/sbo-encounters-fy23-fy26-apr.csv" \
           "$CAUSAL/cbp/raw/sbo_encounters_fy23_fy26_apr.csv"

# --- EOIR workload stats (PDFs; scrape media IDs from stats page) ---
mkdir -p "$DATA/external/stage4/courts/eoir"
_fetch_eoir_pdf() {
    local id="$1" slug="$2"
    local dest="$DATA/external/stage4/courts/eoir/${slug}.pdf"
    local url="https://www.justice.gov/eoir/media/${id}/dl"
    [[ -s "$dest" ]] && _validate_file "$dest" 5000 && { _ok "exists $dest"; return 0; }
    _log "fetch(EOIR) $slug"
    if curl -sSL --fail --max-time 120 -A "Mozilla/5.0" -o "$dest.part" "$url" \
        && _validate_file "$dest.part" 5000; then
        mv "$dest.part" "$dest"
        _ok "$dest"
        return 0
    fi
    rm -f "$dest.part" "$dest"
    _warn "skip $dest"
    return 0
}
EOIR_PAGE=$(curl -sSL -A "Mozilla/5.0" "https://www.justice.gov/eoir/workload-and-adjudication-statistics" 2>/dev/null || true)
if [[ -n "$EOIR_PAGE" ]]; then
    printf '%s' "$EOIR_PAGE" | grep -oE '/eoir/media/[0-9]+/dl' | sort -u > "$DATA/external/stage4/courts/eoir/eoir_media_urls.txt" || true
    _ok "indexed $(wc -l < "$DATA/external/stage4/courts/eoir/eoir_media_urls.txt" | tr -d ' ') EOIR media URLs"
fi
for _eoir in \
    "1344791:pending_cases_new_completions" \
    "1344801:new_cases_completions_historical" \
    "1419886:amnesty_cases_by_state" \
    "1344956:unaccompanied_alien_child_statistics"; do
    _fetch_eoir_pdf "${_eoir%%:*}" "${_eoir##*:}"
done
if command -v uv >/dev/null 2>&1 && [[ -f "$IMMIGRATION_FISCAL_ROOT/build/parse_eoir_court_pdfs.py" ]]; then
    PNY_DATA_ROOT="$DATA" DERIVED_ROOT="${DERIVED_ROOT:-$DATA/derived}" \
        uv run --with pdfplumber,pandas python "$IMMIGRATION_FISCAL_ROOT/build/parse_eoir_court_pdfs.py" || true
fi

# --- FRED macro anchors (CSV graph export) ---
mkdir -p "$DATA/external/fred"
for pair in \
    "UNRATE:unemployment_rate" \
    "CPIAUCSL:cpi_all_urban" \
    "HOUST:housing_starts" \
    "CSUSHPINSA:case_shiller_national"; do
    sid="${pair%%:*}"; name="${pair#*:}"
    _fetch_get "https://fred.stlouisfed.org/graph/fredgraph.csv?id=${sid}" \
               "$DATA/external/fred/${name}.csv" --optional
done

# --- Extract QCEW if only zip present ---
QCEW_ZIP="$DATA/bls/qcew_2023_annual_by_industry.zip"
QCEW_DIR="$DATA/bls/qcew_2023_annual_by_industry"
if [[ -s "$QCEW_ZIP" && ! -d "$QCEW_DIR" ]]; then
    _log "extract $QCEW_ZIP"
    mkdir -p "$QCEW_DIR"
    if unzip -q -o "$QCEW_ZIP" -d "$QCEW_DIR"; then _ok "extracted QCEW"; else _warn "QCEW extract failed"; fi
fi

_log ""
if (( ERRORS == 0 )); then
    _log "=== setup OK (required census zips present) ==="
else
    _log "=== setup FAILED ($ERRORS required download(s) missing) ==="
fi

# Stage-5 fiscal / local-cost evidence (optional pass; skipped on minimal tier)
if [[ "${REPRODUCE_TIER:-standard}" != "minimal" && -f "$HERE/setup-net-negative.sh" ]]; then
    IMMIGRATION_FISCAL_ROOT="$IMMIGRATION_FISCAL_ROOT" bash "$HERE/setup-net-negative.sh" || true
fi

# Lifetime benchmarks + linkage docs (optional pass; skipped on minimal tier)
if [[ "${REPRODUCE_TIER:-standard}" != "minimal" && -f "$HERE/setup-lifetime.sh" ]]; then
    IMMIGRATION_FISCAL_ROOT="$IMMIGRATION_FISCAL_ROOT" bash "$HERE/setup-lifetime.sh" || true
fi

# Crime + frontier datasets (roadmap 2026-06-24; optional pass; skipped on minimal tier)
if [[ "${REPRODUCE_TIER:-standard}" != "minimal" && -f "$HERE/setup-crime-frontier.sh" ]]; then
    IMMIGRATION_FISCAL_ROOT="$IMMIGRATION_FISCAL_ROOT" bash "$HERE/setup-crime-frontier.sh" || true
fi

if (( ERRORS == 0 )); then
    exit 0
else
    exit 1
fi
