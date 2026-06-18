#!/usr/bin/env bash
# Lifetime fiscal stack: benchmarks, mortality/discount anchors, linkage docs, application-gated refs.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMMIGRATION_FISCAL_ROOT="$(cd "$HERE/.." && pwd)"
if [[ -f "$HERE/config.local.env" ]]; then
    # shellcheck source=config.local.env
    source "$HERE/config.local.env"
elif [[ -f "$HERE/config.env" ]]; then
    # shellcheck source=config.env
    source "$HERE/config.env"
else
    # shellcheck source=config.env.example
    source "$HERE/config.env.example"
fi

LT="$PNY_DATA_ROOT/external/lifetime"
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
    [[ "$dest" != *.pdf ]] || head -c 5 "$dest" | grep -q '%PDF'
    [[ "$dest" != *.json ]] || python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$dest" 2>/dev/null
    [[ "$dest" != *.xlsx ]] || unzip -tqq "$dest" 2>/dev/null
}

_fetch() {
    local url="$1" dest="$2" min="${3:-10000}"
    mkdir -p "$(dirname "$dest")"
    if [[ -s "$dest" ]] && _validate_file "$dest" "$min"; then
        _ok "exists $dest"
        return 0
    fi
    _log "fetch(lifetime) $url"
    if curl -sSL --fail --max-time 900 -o "$dest.part" "$url" \
        && _validate_file "$dest.part" "$min"; then
        mv "$dest.part" "$dest"
        _ok "$dest ($(wc -c < "$dest" | tr -d ' ') bytes)"
        return 0
    fi
    rm -f "$dest.part" "$dest"
    _warn "skip $dest"
    return 0
}

_log "=== lifetime fiscal evidence datasets ==="
mkdir -p "$LT"/{nas,nrc,nap,dallasfed,census,irs,nber,fed,applications,imf,iza,worldbank,bea,cms,aer,cdc,cgdev}

# --- Benchmark lifetime NPV (education cells, not nationality) ---
_fetch "https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf" \
       "$LT/nas/nas_2017_immigration_economic_fiscal_full.pdf" 1000000
_fetch "https://www.nap.edu/catalog/23550/download/pdf" \
       "$LT/nas/nas_2017_nap_download.pdf" 1000000
_fetch "https://www.nap.edu/catalog/5779/download/pdf" \
       "$LT/nrc/nrc_1997_new_americans.pdf" 500000
_fetch "https://www.dallasfed.org/-/media/documents/research/papers/2017/wp1704.pdf" \
       "$LT/dallasfed/orrenius_nas_fiscal_sensitivity_wp1704.pdf" 50000

# --- Heterogeneity / critique papers ---
_fetch "https://www.nber.org/system/files/working_papers/w9489/w9489.pdf" \
       "$LT/nber/storesletten_2003_fiscal_heterogeneity_w9489.pdf" 50000
_fetch "https://www.federalreserve.gov/econres/feds/files/2020001pap.pdf" \
       "$LT/fed/feds_2020001_immigration_fiscal.pdf" 50000

# --- Linkage / restricted-data road map ---
_fetch "https://www2.census.gov/library/working-papers/2024/demo/sehsd-wp2024-01.pdf" \
       "$LT/census/sehsd_wp2024_01_sipp_research_files.pdf" 100000
_fetch "https://www2.census.gov/about/linkage/data-file-inventory.pdf" \
       "$LT/census/census_linkage_data_file_inventory.pdf" 100000

# --- Federal tax microsim anchors ---
_fetch "https://www.irs.gov/pub/irs-soi/06resconf.pdf" \
       "$LT/irs/irs_soi_puf_limitations_06resconf.pdf" 100000

# --- Synthetic SIPP + application-only products (HTML landing, not microdata) ---
_fetch "https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html" \
       "$LT/applications/synthetic_sipp_beta_landing.html" 5000
_fetch "https://www.census.gov/programs-surveys/sipp/guidance/research-guidance/synthetic_sipp.html" \
       "$LT/applications/synthetic_sipp_research_guidance.html" 5000

# --- Round 2: macro frame, remittances, generational accounting, earnings paths ---
_fetch "https://www.imf.org/-/media/files/research/imf-and-g20/2025/g20-background-note-on-aging-and-migration.pdf" \
       "$LT/imf/g20_2025_aging_and_migration.pdf" 100000
_fetch "https://docs.iza.org/dp18218.pdf" \
       "$LT/iza/iza_dp18218_agi_soon_migration.pdf" 500000
_fetch "https://api.worldbank.org/v2/country/MEX/indicator/BX.TRF.PWKR.CD.DT?format=json&per_page=70" \
       "$LT/worldbank/mexico_worker_remittances_bx_trf_pwkr_cd_dt.json" 1000
_fetch "https://www.nap.edu/catalog/5985/download/pdf" \
       "$LT/nap/nap_1998_immigration_debate_fiscal_effects.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w7041/w7041.pdf" \
       "$LT/nber/lee_miller_1998_generational_accounting_immigration_w7041.pdf" 50000
_fetch "https://www.nber.org/system/files/chapters/c10849/c10849.pdf" \
       "$LT/nber/auerbach_oreopoulos_2000_generational_accounting_immigration.pdf" 50000
_fetch "https://www.aeaweb.org/content/file?id=7134" \
       "$LT/aer/lee_miller_2000_immigration_social_security_fiscal_aer.pdf" 10000
_fetch "https://www.nber.org/system/files/working_papers/w22102/w22102.pdf" \
       "$LT/nber/borjas_2016_undocumented_labor_supply_w22102.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w11547/w11547.pdf" \
       "$LT/nber/card_2005_is_new_immigration_really_so_bad_w11547.pdf" 50000
_fetch "https://apps.bea.gov/regional/zip/SPI_state_summary_2023.zip" \
       "$LT/bea/spi_state_summary_2023.zip" 5000
_fetch "https://www.cms.gov/files/document/2024-medicare-trustees-report.pdf" \
       "$LT/cms/medicare_trustees_report_2024.pdf" 500000

# --- Round 3: mortality by Hispanic origin, Clemens fiscal critique, redistribution ---
_fetch "https://www.cdc.gov/nchs/data/nvsr/nvsr72/nvsr72-12.pdf" \
       "$LT/cdc/nvsr72_12_us_life_tables_2021_hispanic_origin.pdf" 500000
_fetch "https://www.cgdev.org/sites/default/files/fiscal-effect-immigration-reducing-bias-influential-estimates.pdf" \
       "$LT/cgdev/clemens_2023_fiscal_effect_capital_tax_adjustment.pdf" 50000
_fetch "https://www.cgdev.org/sites/default/files/CGD-Working-Paper-423-Clemens-Pritchett-New-Econ-Case-Migration_0.pdf" \
       "$LT/cgdev/clemens_pritchett_2016_migration_restrictions_wp423.pdf" 50000
_fetch "https://www.cgdev.org/sites/default/files/economic-and-fiscal-effects-granting-refugees-formal-labor-market-access.pdf" \
       "$LT/cgdev/clemens_huang_graham_2018_refugee_labor_market_access_wp496.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w24733/w24733.pdf" \
       "$LT/nber/alesina_miano_stantcheva_2018_immigration_redistribution_w24733.pdf" 50000

# CBO immigration reports — copy from main data/ if setup.sh got them; else try browser UA
mkdir -p "$LT/cbo"
for pair in \
  "$PNY_DATA_ROOT/cbo/60569-immigration-federal.pdf:cbo_60165_immigration_federal_macro.pdf" \
  "$PNY_DATA_ROOT/cbo/61256-immigration-state-local.pdf:cbo_61256_immigration_state_local.pdf"; do
  src="${pair%%:*}"; dest="$LT/cbo/${pair#*:}"
  if [[ -s "$dest" ]]; then _ok "exists $dest"; continue; fi
  if [[ -s "$src" ]]; then cp "$src" "$dest" && _ok "copied $dest"; continue; fi
  _warn "skip $dest (run main setup.sh or browser-acquire CBO PDF)"
done

# --- Round 4: welfare trajectory, descendant pessimism, OMB outlays, remittance inflows ---
mkdir -p "$LT"/{omb,borjas}
_fetch "https://www.nber.org/system/files/chapters/c6051/c6051.pdf" \
       "$LT/borjas/borjas_2000_handbook_issues_economics_immigration_intro_c6051.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w4872/w4872.pdf" \
       "$LT/borjas/borjas_1994_immigration_welfare_1970_1990_w4872.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w24394/w24394.pdf" \
       "$LT/nber/duncan_trejo_2018_socioeconomic_integration_second_gen_w24394.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w24315/w24315.pdf" \
       "$LT/nber/kuka_shenhav_shih_2018_daca_education_returns_w24315.pdf" 50000
_fetch "https://api.worldbank.org/v2/country/USA/indicator/BX.TRF.PWKR.CD.DT?format=json&per_page=70" \
       "$LT/worldbank/usa_worker_remittances_bx_trf_pwkr_cd_dt.json" 1000
_fetch "https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-3-1.xlsx" \
       "$LT/omb/budget_fy2025_table_3_1_outlays_by_function.xlsx" 5000
_fetch "https://www.govinfo.gov/content/pkg/BUDGET-2025-TAB/xls/BUDGET-2025-TAB-12-1.xlsx" \
       "$LT/omb/budget_fy2025_table_12_1_federal_grants_state_local.xlsx" 5000

# --- Round 5: UK comparator, assimilation/mobility, fiscal accounting, redistribution EU ---
mkdir -p "$LT"/{cream,methodology}
_fetch "https://www.cream-migration.org/publ_uploads/CDP_22_13.pdf" \
       "$LT/cream/dustmann_frattini_2013_fiscal_effects_immigration_uk_cdp_22_13.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w22381/w22381.pdf" \
       "$LT/nber/abramitzky_boustan_eriksson_2016_cultural_assimilation_mass_migration_w22381.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w26408/w26408.pdf" \
       "$LT/nber/abramitzky_boustan_2019_intergenerational_mobility_immigrants_w26408.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w25562/w25562.pdf" \
       "$LT/nber/alesina_murard_rapoport_2019_immigration_redistribution_europe_w25562.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w12344/w12344.pdf" \
       "$LT/methodology/green_kotlikoff_2006_relativity_fiscal_language_w12344.pdf" 50000

# --- Round 6: indirect fiscal offsets, local shock-load, safety-net magnets, congestion ---
mkdir -p "$LT"/{econstor,aei,brookings,frbsf,banqueducanada}
_fetch "https://www.econstor.eu/bitstream/10419/282044/1/352.pdf" \
       "$LT/econstor/colas_sachs_2024_indirect_fiscal_benefits_low_skill.pdf" 500000
_fetch "https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf" \
       "$LT/aei/orrenius_viard_zavodny_2025_fiscal_impact_update.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w33655/w33655.pdf" \
       "$LT/nber/gould_2024_asylum_seekers_homelessness_w33655.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w33961/w33961.pdf" \
       "$LT/nber/akers_boustan_2024_immigration_inequality_next_generation_w33961.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w17667/w17667.pdf" \
       "$LT/nber/bitler_hoynes_2012_immigrants_welfare_safety_net_w17667.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w30589/w30589.pdf" \
       "$LT/nber/clemens_lewis_2022_low_skill_immigration_restrictions_w30589.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w17515/w17515.pdf" \
       "$LT/nber/razin_wahba_2012_welfare_magnet_immigration_w17515.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w26454/w26454.pdf" \
       "$LT/nber/landais_posch_muller_2017_welfare_magnet_denmark_w26454.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w18515/w18515.pdf" \
       "$LT/nber/blau_kahn_2012_immigration_distribution_incomes_w18515.pdf" 50000
_fetch "https://www.brookings.edu/wp-content/uploads/2017/06/jpube-vmt-paper.pdf" \
       "$LT/brookings/vmt_external_cost_congestion_jpube_2017.pdf" 100000
_fetch "https://www.frbsf.org/research-and-insights/publications/economic-letter/2023/07/why-immigration-is-an-urban-phenomenon/" \
       "$LT/frbsf/econ_letter_2023_immigration_urban_phenomenon.html" 50000
_fetch "https://www.banqueducanada.ca/wp-content/uploads/2023/11/swp2023-57.pdf" \
       "$LT/banqueducanada/swp2023_57_immigration_fiscal_capacity.pdf" 500000

# --- Round 7: earnings-path calibration, Borjas-Peri debate, transfer layers, methodology ---
mkdir -p "$LT"/{card,nces,census}
_fetch "https://www.nber.org/system/files/working_papers/w19315/w19315.pdf" \
       "$LT/nber/foged_peri_2016_immigrants_effect_native_workers_w19315.pdf" 100000
_fetch "https://docs.iza.org/dp8961.pdf" \
       "$LT/iza/iza_dp8961_foged_peri_immigrants_native_workers.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w14188/w14188.pdf" \
       "$LT/nber/peri_ottaviano_2008_immigration_national_wages_w14188.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w11672/w11672.pdf" \
       "$LT/nber/peri_ottaviano_2005_rethinking_gains_immigration_w11672.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w32389/w32389.pdf" \
       "$LT/nber/card_peri_2024_immigration_wages_2000_2022_w32389.pdf" 100000
_fetch "https://davidcard.berkeley.edu/papers/card-peri-jel-april-6-2016.pdf" \
       "$LT/card/card_peri_2016_jel_review_borjas_immigration_economics.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w23504/w23504.pdf" \
       "$LT/nber/borjas_2017_still_more_mariel_role_race_w23504.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w6195/w6195.pdf" \
       "$LT/nber/shapiro_2003_immigration_quality_jobs_w6195.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w6175/w6175.pdf" \
       "$LT/nber/borjas_1997_ethnicity_intergenerational_welfare_w6175.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w6229/w6229.pdf" \
       "$LT/nber/abel_1997_immigrants_children_pension_transition_w6229.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w6067/w6067.pdf" \
       "$LT/nber/butchart_1998_recent_immigrants_crime_incarceration_w6067.pdf" 100000
_fetch "https://www.brookings.edu/articles/macroeconomic-implications-of-immigration-flows-in-2025-and-2026-january-2026-update/" \
       "$LT/brookings/edelberg_veuger_watson_2026_cps_foreign_born_controls_warning.html" 50000
_fetch "https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2024_SIPP_Users_Guide.pdf" \
       "$LT/census/sipp_2024_users_guide.pdf" 500000
_fetch "https://nces.ed.gov/programs/digest/d23/tables/dt23_236.20.asp" \
       "$LT/nces/digest_dt23_236_20_current_expenditure_per_pupil.html" 50000

# --- Round 8: composition/attrition, Mariel debate stack, Dustmann survey, task specialization ---
_fetch "https://www.nber.org/system/files/working_papers/w16736/w16736.pdf" \
       "$LT/nber/dustmann_2014_economic_impacts_immigration_survey_w16736.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w15597/w15597.pdf" \
       "$LT/nber/razin_sadka_swagel_2011_migration_welfare_state_w15597.pdf" 50000
_fetch "https://www.nber.org/system/files/working_papers/w23753/w23753.pdf" \
       "$LT/nber/hanson_liu_mcgee_2018_rise_fall_us_low_skilled_immigration_w23753.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w23756/w23756.pdf" \
       "$LT/nber/borjas_monras_2018_hurricanes_migrant_networks_immigration_w23756.pdf" 500000
_fetch "https://www.nber.org/system/files/working_papers/w9755/w9755.pdf" \
       "$LT/nber/borjas_2003_labor_demand_curve_immigration_w9755.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w11610/w11610.pdf" \
       "$LT/nber/borjas_2005_native_internal_migration_immigration_w11610.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w3069/w3069.pdf" \
       "$LT/nber/card_1989_mariel_boatlift_miami_labor_market_w3069.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w21850/w21850.pdf" \
       "$LT/nber/borjas_2016_wage_impact_marielitos_additional_evidence_w21850.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w13389/w13389.pdf" \
       "$LT/nber/peri_sparber_2007_task_specialization_immigration_wages_w13389.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w12518/w12518.pdf" \
       "$LT/nber/borjas_grogger_hanson_2006_immigration_african_american_employment_w12518.pdf" 100000

# --- Round 9: housing elasticity, H-1B/high-skill, legal-status tax floor, border selection, refugee politics ---
_fetch "https://www.nber.org/system/files/working_papers/w12497/w12497.pdf" \
       "$LT/nber/ottaviano_peri_2006_rethinking_immigration_wages_w12497.pdf" 100000
_fetch "https://www.nber.org/system/files/working_papers/w23153/w23153.pdf" \
       "$LT/nber/bound_khanna_morales_2017_h1b_economic_impact_w23153.pdf" 500000
_fetch "https://docs.iza.org/dp4898.pdf" \
       "$LT/iza/iza_dp4898_lozano_lopez_border_enforcement_mexican_selection.pdf" 100000
_fetch "https://docs.iza.org/dp452.pdf" \
       "$LT/iza/iza_dp452_immigrant_occupational_mobility_longitudinal.pdf" 100000
_fetch "https://docs.iza.org/dp10234.pdf" \
       "$LT/iza/iza_dp10234_economics_politics_refugee_migration.pdf" 500000
_fetch "https://www.cdc.gov/nchs/data/nvsr/nvsr72/nvsr72-12.pdf" \
       "$LT/cdc/nvsr72_12_us_life_tables_2021_all_races.pdf" 500000
_fetch "https://www2.census.gov/programs-surveys/popproj/tables/2023/2023-summary-tables/np2023-t1.xlsx" \
       "$LT/census/np2023_t1_population_projections_summary.xlsx" 5000

# Copies from main fiscal stack (no new download)
SAIZ_SRC="$PNY_DATA_ROOT/../immigration-causal/data/saiz/saiz_2010_msa_elasticity.dta"
[[ -f "$SAIZ_SRC" ]] || SAIZ_SRC="$(cd "$IMMIGRATION_FISCAL_ROOT/../../sources/immigration-causal/data/saiz" 2>/dev/null && pwd)/saiz_2010_msa_elasticity.dta"
if [[ -f "$SAIZ_SRC" ]]; then
    mkdir -p "$LT/saiz"
    cp -f "$SAIZ_SRC" "$LT/saiz/saiz_2010_msa_elasticity.dta"
    _ok "copy $LT/saiz/saiz_2010_msa_elasticity.dta"
else
    _warn "skip Saiz elasticity — not at immigration-causal/data/saiz/"
fi
for _pair in \
    "itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf:itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf" \
    "itep/itep_2024_tax_contributions.json:itep/itep_2024_tax_contributions.json" \
    "pew/pew-unauthorized-immigrants-2025.pdf:pew/pew-unauthorized-immigrants-2025.pdf" \
    "cbo/60569-immigration-federal.pdf:cbo/cbo_60569_immigration_federal_macro_alt.pdf" \
    "cbo/61256-immigration-state-local.pdf:cbo/cbo_61256_immigration_state_local_alt.pdf"; do
    _src="${_pair%%:*}"; _dst="${_pair##*:}"
    if [[ -f "$PNY_DATA_ROOT/$_src" ]]; then
        mkdir -p "$LT/$(dirname "$_dst")"
        cp -f "$PNY_DATA_ROOT/$_src" "$LT/$_dst"
        _ok "copy $LT/$_dst"
    fi
done
DERIVED_STAGE3="${DERIVED_ROOT:-$PNY_DATA_ROOT/derived}/stage3_proto"
if [[ -d "$DERIVED_STAGE3" ]]; then
    mkdir -p "$LT/derived/stage3_proto"
    for _f in origin_fiscal_scenario_2023.csv sipp_scenario_ledger_2024.csv scenario_ledger_2024.meta.json; do
        [[ -f "$DERIVED_STAGE3/$_f" ]] && cp -f "$DERIVED_STAGE3/$_f" "$LT/derived/stage3_proto/$_f" && _ok "copy $LT/derived/stage3_proto/$_f"
    done
else
    _warn "skip scenario ledger copy — $DERIVED_STAGE3 missing (run rebuild.sh + compose)"
fi

# --- Round 10: return-migration/assimilation, OECD flows, derived incidence bridge, admin costs ---
_fetch "https://www.nber.org/system/files/working_papers/w14833/w14833.pdf" \
       "$LT/nber/ortega_peri_2009_causes_effects_international_migrations_w14833.pdf" 100000
_fetch "https://docs.iza.org/dp631.pdf" \
       "$LT/iza/iza_dp631_duleep_regets_immigrant_quality_human_capital.pdf" 100000
_fetch "https://docs.iza.org/dp8628.pdf" \
       "$LT/iza/iza_dp8628_duleep_regets_country_origin_earnings_return_migration.pdf" 500000
_fetch "https://docs.iza.org/dp331.pdf" \
       "$LT/iza/iza_dp331_winkelmann_international_employer_recruitment.pdf" 100000
# Fed FEDS note slug 404 as of 2026-06; MPR Mar 2024 covers immigration/labor supply.
_fetch "https://www.federalreserve.gov/publications/files/20240301_mprfullreport.pdf" \
       "$LT/fed/fed_mpr_20240301_immigration_labor_supply.pdf" 500000

# Derived incidence + health bridge (from DERIVED_ROOT / main stack)
DERIVED_BASE="${DERIVED_ROOT:-$PNY_DATA_ROOT/derived}"
if [[ -d "$DERIVED_BASE" ]]; then
    for _pair in \
        "stage2/school_finance_county_2023.csv:derived/stage2/school_finance_county_2023.csv" \
        "stage2/chas_county_housing_stress_2018_2022.csv:derived/stage2/chas_county_housing_stress_2018_2022.csv" \
        "stage2/irs_migration_county_2022_2023.csv:derived/stage2/irs_migration_county_2022_2023.csv" \
        "stage2/puma_county_area_xwalk_2023.csv:derived/stage2/puma_county_area_xwalk_2023.csv" \
        "stage5/state_stage5_context_2023.csv:derived/stage5/state_stage5_context_2023.csv" \
        "stage5/receiver_city_migrant_costs.csv:derived/stage5/receiver_city_migrant_costs.csv" \
        "stage3_proto/meps_health_cost_module_2023.csv:derived/stage3_proto/meps_health_cost_module_2023.csv" \
        "stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv:derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv" \
        "stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv:derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv" \
        "stage3_proto/sipp_public_mvp_cells_2024.csv:derived/stage3_proto/sipp_public_mvp_cells_2024.csv"; do
        _src="${_pair%%:*}"; _dst="${_pair##*:}"
        if [[ -f "$DERIVED_BASE/$_src" ]]; then
            mkdir -p "$LT/$(dirname "$_dst")"
            cp -f "$DERIVED_BASE/$_src" "$LT/$_dst"
            _ok "copy $LT/$_dst"
        fi
    done
else
    _warn "skip derived bridge copy — $DERIVED_BASE missing"
fi
for _pair in \
    "dhs/cbp_fy25_budget_justification.pdf:admin/cbp_fy25_budget_justification.pdf" \
    "dhs/ice_fy25_budget_justification.pdf:admin/ice_fy25_budget_justification.pdf" \
    "dhs/cbp_fy26_budget_justification.pdf:admin/cbp_fy26_budget_justification.pdf" \
    "dhs/ice_fy26_budget_justification.pdf:admin/ice_fy26_budget_justification.pdf"; do
    _src="${_pair%%:*}"; _dst="${_pair##*:}"
    if [[ -f "$PNY_DATA_ROOT/$_src" ]]; then
        mkdir -p "$LT/$(dirname "$_dst")"
        cp -f "$PNY_DATA_ROOT/$_src" "$LT/$_dst"
        _ok "copy $LT/$_dst"
    fi
done
if [[ -f "$PNY_DATA_ROOT/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx" ]]; then
    mkdir -p "$LT/dhs"
    cp -f "$PNY_DATA_ROOT/external/origin/ohss/lpr_country_birth_major_class_2005_2022.xlsx" \
          "$LT/dhs/plcy_lpr_by_country_of_birth_fy2005_2022.xlsx"
    _ok "copy $LT/dhs/plcy_lpr_by_country_of_birth_fy2005_2022.xlsx"
elif [[ -f "$PNY_DATA_ROOT/external/origin/plcy_lpr_by_country_of_birth_by_major_class_fy2005-2022_d.xlsx" ]]; then
    mkdir -p "$LT/dhs"
    cp -f "$PNY_DATA_ROOT/external/origin/plcy_lpr_by_country_of_birth_by_major_class_fy2005-2022_d.xlsx" \
          "$LT/dhs/plcy_lpr_by_country_of_birth_fy2005_2022.xlsx"
    _ok "copy $LT/dhs/plcy_lpr_by_country_of_birth_fy2005_2022.xlsx"
fi

# --- Round 11: unit-fix propagation note; no new PDF hunts (NBER ID probes w2748/w15248/w24721 rejected) ---
# Storesletten fiscal heterogeneity: w9489 is WRONG PAPER (Blomström/Kokko FDI) — do not re-fetch.
# Correct Storesletten (2000) Cleveland Fed WP — browser/manual; parameters via Colas-Sachs (2024).
# Scenario ledger + school_finance county refreshed after F-33 *1000 fix in build_stage2_incidence_context.py
_log "round 11: rely on derived/stage2+stage3_proto copies; mis-staged storesletten w9489 flagged in cluster A"

cat > "$LT/applications/MANUAL_ACQUIRE.md" <<'EOF'
# Lifetime stack — manual / application-only

| Product | Role in lifetime model | Access |
|---------|------------------------|--------|
| Synthetic SIPP Beta | Admin-like earnings histories (public) | Apply via [SSB product page](https://www.census.gov/programs-surveys/sipp/guidance/sipp-synthetic-beta-data-product.html) |
| IRS SOI individual PUF | Federal tax-liability mapping | [IRS PUF page](https://www.irs.gov/statistics/soi-tax-stats-individual-public-use-microdata-files) — application, no direct zip |
| PSID | Descendant / intergenerational params | [psidonline.isr.umich.edu](https://psidonline.isr.umich.edu/) — registration |
| FSRDC SIPP-SSA-IRS | Gold-standard earnings + tax linkage | Census restricted; see `census/sehsd_wp2024_01_sipp_research_files.pdf` |
| FSRDC LEHD | Employer-employee earnings panel | Census restricted |
| SSA period life tables | Mortality for NPV | [ssa.gov/oact/STATS](https://www.ssa.gov/oact/STATS/life_tables.html) — bot-blocked on curl; browser |
| SSA Trustees Report | Discount-rate anchor (NAS uses 2–3%) | [ssa.gov/oact/tr](https://www.ssa.gov/oact/tr/) — browser |
| Urban TRIM immigration module | Transfer microsim benchmark | [urban.org TRIM](https://www.urban.org/research/data-methods/data-analysis/quantitative-data-analysis/microsimulation/transfer-income-model-trim) |
| EDFacts FS141 | Current district EL | [eddataexpress.ed.gov](https://eddataexpress.ed.gov/) — interactive export |
| SSA period life tables | Mortality (curl 403) | Browser: [ssa.gov/oact/STATS/table4c6.xlsx](https://www.ssa.gov/oact/STATS/table4c6.xlsx) |
| CBO immigration PDFs | Macro offset / state-local split | Browser if curl 403; some copies in `external/` via main `setup.sh` |
| Urban TRIM paper | Transfer microsim benchmark | Browser (403 on direct PDF) |
| Tax Policy Center Who Pays | Tax incidence calibration | Browser (403) |
| Census F33 district finance zip | School spend by district | URL churn — use `elsec23.txt` in main `setup.sh` |
| CBO 60165 / 61256 | Federal macro + state-local immigration | Browser if missing; copy from `data/cbo/` after main `setup.sh` |
EOF

cat > "$LT/ACQUIRED.md" <<EOF
# Lifetime external staging

Generated by \`acquire/setup-lifetime.sh\` on $(date -u +%Y-%m-%dT%H:%MZ).

See \`applications/MANUAL_ACQUIRE.md\` for application-gated products.
EOF

_log "=== lifetime done ==="
