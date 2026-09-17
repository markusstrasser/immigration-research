# PARAMS — external parameters for the complete absolute account

Written by the researcher lane, 2026-09-17T21:41:11+00:00. Model: `claude-opus-5[1m]`.

Every entry carries `value`, `unit`, `fiscal_year`, `source_url`, a verbatim `quote` containing the number, `fetched`, `status` and usually `notes`. Entries with `status: unverified` have `value: null` and are listed at the bottom with what blocked them; the builder fails loud on any it uses.

Quotes drawn from spreadsheets name the table, the row label and the year column rather than prose, because the source has no prose. Notes tagged `[INFERENCE]` mark arithmetic on verified numbers, never a new measurement.

Keys whose notes begin `ALIAS KEY` mirror a canonical entry under the naming and unit convention of the builder lane's `params_placeholder.json`. Every key that placeholder expects now exists here.

## omb

62 verified, 0 unverified. OMB Historical Tables, FY2027 Budget edition (same edition as the cached Table 3.1). USD millions, FY2024 actuals.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `func_050_national_defense` | 873,523.0 | USD millions | FY2024 | verified |
| `func_150_international_affairs` | 56,396.0 | USD millions | FY2024 | verified |
| `func_250_general_science` | 41,476.0 | USD millions | FY2024 | verified |
| `func_270_energy` | 13,571.0 | USD millions | FY2024 | verified |
| `func_300_natural_resources_environment` | 58,469.0 | USD millions | FY2024 | verified |
| `func_350_agriculture` | 32,841.0 | USD millions | FY2024 | verified |
| `func_370_commerce_housing_credit` | 36,032.0 | USD millions | FY2024 | verified |
| `func_400_transportation` | 136,582.0 | USD millions | FY2024 | verified |
| `func_450_community_regional_development` | 85,215.0 | USD millions | FY2024 | verified |
| `func_500_education_training_employment_social_services` | 306,370.0 | USD millions | FY2024 | verified |
| `subf_501_elementary_secondary_vocational` | 105,373.0 | USD millions | FY2024 | verified |
| `subf_502_higher_education` | 161,032.0 | USD millions | FY2024 | verified |
| `subf_503_research_general_education_aids` | 4,723.0 | USD millions | FY2024 | verified |
| `subf_504_training_employment` | 7,683.0 | USD millions | FY2024 | verified |
| `subf_505_other_labor_services` | 2,393.0 | USD millions | FY2024 | verified |
| `subf_506_social_services` | 25,166.0 | USD millions | FY2024 | verified |
| `func_550_health` | 911,290.0 | USD millions | FY2024 | verified |
| `subf_551_health_care_services` | 854,342.0 | USD millions | FY2024 | verified |
| `subf_552_health_research_training` | 50,647.0 | USD millions | FY2024 | verified |
| `subf_554_consumer_occupational_health_safety` | 6,301.0 | USD millions | FY2024 | verified |
| `subf_571_medicare` | 874,133.0 | USD millions | FY2024 | verified |
| `func_600_income_security` | 670,548.0 | USD millions | FY2024 | verified |
| `subf_601_general_retirement_disability` | 22,325.0 | USD millions | FY2024 | verified |
| `subf_602_federal_employee_retirement_disability` | 179,924.0 | USD millions | FY2024 | verified |
| `subf_603_unemployment_compensation` | 38,278.0 | USD millions | FY2024 | verified |
| `subf_604_housing_assistance` | 70,008.0 | USD millions | FY2024 | verified |
| `subf_605_food_nutrition_assistance` | 149,146.0 | USD millions | FY2024 | verified |
| `subf_609_other_income_security` | 210,867.0 | USD millions | FY2024 | verified |
| `subf_651_social_security` | 1,460,918.0 | USD millions | FY2024 | verified |
| `func_700_veterans` | 325,645.0 | USD millions | FY2024 | verified |
| `subf_701_income_security_veterans` | 161,312.0 | USD millions | FY2024 | verified |
| `subf_702_veterans_education_training` | 13,554.0 | USD millions | FY2024 | verified |
| `subf_703_hospital_medical_veterans` | 138,543.0 | USD millions | FY2024 | verified |
| `subf_704_veterans_housing` | -3,512.0 | USD millions | FY2024 | verified |
| `subf_705_other_veterans` | 15,748.0 | USD millions | FY2024 | verified |
| `func_750_administration_of_justice` | 83,793.0 | USD millions | FY2024 | verified |
| `subf_751_federal_law_enforcement` | 46,098.0 | USD millions | FY2024 | verified |
| `subf_752_federal_litigative_judicial` | 19,964.0 | USD millions | FY2024 | verified |
| `subf_753_federal_correctional` | 9,057.0 | USD millions | FY2024 | verified |
| `subf_754_criminal_justice_assistance` | 8,674.0 | USD millions | FY2024 | verified |
| `func_800_general_government` | 35,316.0 | USD millions | FY2024 | verified |
| `func_900_net_interest` | 879,879.0 | USD millions | FY2024 | verified |
| `func_920_allowances` | 0.0 | USD millions | FY2024 | verified |
| `func_950_undistributed_offsetting_receipts` | -146,736.0 | USD millions | FY2024 | verified |
| `subf_951_employer_share_employee_retirement_onbudget` | -116,417.0 | USD millions | FY2024 | verified |
| `subf_952_employer_share_employee_retirement_offbudget` | -23,299.0 | USD millions | FY2024 | verified |
| `subf_953_ocs_rents_royalties` | -7,020.0 | USD millions | FY2024 | verified |
| `total_outlays` | 6,735,261.0 | USD millions | FY2024 | verified |
| `receipts_individual_income` | 2,426,067.0 | USD millions | FY2024 | verified |
| `receipts_corporation_income` | 529,867.0 | USD millions | FY2024 | verified |
| `receipts_social_insurance_retirement` | 1,708,926.0 | USD millions | FY2024 | verified |
| `receipts_excise` | 101,426.0 | USD millions | FY2024 | verified |
| `receipts_other` | 153,598.0 | USD millions | FY2024 | verified |
| `receipts_total` | 4,919,884.0 | USD millions | FY2024 | verified |
| `receipts_estate_gift` | 31,616.0 | USD millions | FY2024 | verified |
| `receipts_customs_duties` | 77,036.0 | USD millions | FY2024 | verified |
| `receipts_miscellaneous` | 44,946.0 | USD millions | FY2024 | verified |
| `excise_alcohol` | 8,929.0 | USD millions | FY2024 | verified |
| `excise_tobacco` | 9,378.0 | USD millions | FY2024 | verified |
| `excise_transportation_fuels_federal_funds` | -7,905.0 | USD millions | FY2024 | verified |
| `excise_trust_transportation` | 42,507.0 | USD millions | FY2024 | verified |
| `excise_total` | 101,426.0 | USD millions | FY2024 | verified |

## population

3 verified, 0 unverified. Census Vintage-2024 state population estimates, July 1 reference date.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `us_resident_population_2024_07_01` | 340,110,988 | persons | July 1, 2024 | verified |
| `state_resident_population_2024_07_01` | dict, 52 keys | persons | July 1, 2024 | verified |
| `us_resident_population_2023_07_01` | 336,806,231 | persons | July 1, 2023 | verified |

## deflator

5 verified, 0 unverified. BEA NIPA Table 3.9.4, sheet T30904-A, line 33 State and local. Published 2026-08-26.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `sl_govt_cons_and_investment_price_index_2022` | 125.305 | index, 2017=100 | calendar 2022 | verified |
| `sl_govt_cons_and_investment_price_index_2024` | 130.231 | index, 2017=100 | calendar 2024 | verified |
| `sl_deflator_2022_to_2024_ratio` | 1.039312 | ratio | 2022->2024 | verified |
| `sl_govt_consumption_expenditures_price_index_2022` | 124.977 | index, 2017=100 | calendar 2022 | verified |
| `sl_govt_consumption_expenditures_price_index_2024` | 129.386 | index, 2017=100 | calendar 2024 | verified |

## enforcement

37 verified, 0 unverified. DHS FY2026 Budget in Brief and FY2026 Congressional Budget Justifications carry the FY2024 **Enacted** column. The FY2025 BIB does not — its FY2024 column is an annualized continuing resolution. DOJ from the FY2026 Budget and Performance Summary.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `ice_total_budget_authority` | 9,936,672 | USD thousands | FY2024 | verified |
| `ice_total_after_rescissions` | 9,925,218 | USD thousands | FY2024 | verified |
| `ice_net_discretionary` | 9,557,062 | USD thousands | FY2024 | verified |
| `ice_operations_and_support` | 9,501,542 | USD thousands | FY2024 | verified |
| `ice_ero_total` | 5,082,218 | USD thousands | FY2024 | verified |
| `ice_ero_custody_operations` | 3,434,952 | USD thousands | FY2024 | verified |
| `ice_ero_transportation_and_removal` | 721,417 | USD thousands | FY2024 | verified |
| `ice_ero_alternatives_to_detention` | 470,190 | USD thousands | FY2024 | verified |
| `ice_ero_fugitive_operations` | 159,134 | USD thousands | FY2024 | verified |
| `ice_ero_criminal_apprehension_program` | 296,525 | USD thousands | FY2024 | verified |
| `ice_hsi_total` | 2,459,105 | USD thousands | FY2024 | verified |
| `ice_office_principal_legal_advisor` | 441,515 | USD thousands | FY2024 | verified |
| `ice_mission_support` | 1,518,704 | USD thousands | FY2024 | verified |
| `cbp_total_budget_authority` | 22,863,623 | USD thousands | FY2024 | verified |
| `cbp_total_after_rescissions` | 22,852,905 | USD thousands | FY2024 | verified |
| `cbp_net_discretionary` | 19,666,271 | USD thousands | FY2024 | verified |
| `cbp_operations_and_support` | 18,426,870 | USD thousands | FY2024 | verified |
| `cbp_border_security_operations` | 8,469,709 | USD thousands | FY2024 | verified |
| `cbp_us_border_patrol` | 8,308,847 | USD thousands | FY2024 | verified |
| `cbp_office_of_field_operations` | 5,397,458 | USD thousands | FY2024 | verified |
| `cbp_air_and_marine_operations` | 1,064,399 | USD thousands | FY2024 | verified |
| `cbp_procurement_construction_improvements` | 850,170 | USD thousands | FY2024 | verified |
| `uscis_net_discretionary_appropriated` | 281,140 | USD thousands | FY2024 | verified |
| `uscis_operations_and_support_appropriated` | 271,140 | USD thousands | FY2024 | verified |
| `uscis_federal_assistance_appropriated` | 10,000 | USD thousands | FY2024 | verified |
| `uscis_immigration_examinations_fee_account` | 5,944,570 | USD thousands | FY2024 | verified |
| `uscis_total_budget_authority` | 6,305,682 | USD thousands | FY2024 | verified |
| `doj_eoir_appropriation` | 844,000 | USD thousands | FY2024 | verified |
| `doj_eoir_positions` | 2,850 | positions | FY2024 | verified |
| `doj_bop_total_appropriation` | 8,572,350 | USD thousands | FY2024 | verified |
| `doj_bop_se_appropriation` | 8,392,588 | USD thousands | FY2024 | verified |
| `doj_bop_bf_appropriation` | 179,762 | USD thousands | FY2024 | verified |
| `doj_bop_total_enacted_with_rescissions_transfers` | 8,545,160 | USD thousands | FY2024 | verified |
| `bop_inmates_mexican_nationals` | 12,194 | inmates | snapshot 2026-09-12 | verified |
| `bop_inmates_mexican_share_pct` | 8.0 | percent | snapshot 2026-09-12 | verified |
| `bop_inmates_us_citizens` | 128,739 | inmates | snapshot 2026-09-12 | verified |
| `bop_total_population` | 152,844 | inmates | snapshot 2026-09-12 | verified |

## unauthorized

12 verified, 0 unverified. DHS OHSS stops at January 2022, before the 2022-24 surge, so Pew's mid-2023 estimate is included and labelled secondary.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `ohss_unauthorized_total_jan2022` | 10,990,000 | persons | January 1, 2022 | verified |
| `ohss_unauthorized_mexico_jan2022` | 4,810,000 | persons | January 1, 2022 | verified |
| `ohss_unauthorized_mexico_share_jan2022` | 44 | percent | January 1, 2022 | verified |
| `ohss_unauthorized_by_state_jan2022` | dict, 12 keys | persons | January 1, 2022 | verified |
| `ohss_lpr_total_jan2024` | 12,820,000 | persons | January 1, 2024 | verified |
| `ohss_lpr_mexico_jan2024` | 2,920,000 | persons | January 1, 2024 | verified |
| `ohss_lpr_mexico_share_jan2024` | 23 | percent | January 1, 2024 | verified |
| `ohss_lpr_total_jan2023_revised` | 12,750,000 | persons | January 1, 2023 (revised) | verified |
| `pew_unauthorized_total_2023_secondary` | 14,000,000 | persons | July 2023 | verified |
| `pew_unauthorized_mexico_2023_secondary` | 4,300,000 | persons | July 2023 | verified |
| `pew_unauthorized_mexico_share_2023_secondary` | 30 | percent | July 2023 | verified |
| `pew_unauthorized_non_mexico_2023_secondary` | 9,700,000 | persons | July 2023 | verified |

## k12

14 verified, 2 unverified. State figures from the cached Census F-33 FY2024 summary tables; district-level finance and membership files newly staged.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `f33_per_pupil_current_spending_by_state` | dict, 52 keys | USD per pupil | FY2024 | verified |
| `f33_per_pupil_current_spending_us` | 17,619.39 | USD per pupil | FY2024 | verified |
| `f33_capital_outlay_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `f33_interest_on_school_debt_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `f33_capital_outlay_us` | 113,087,706 | USD thousands | FY2024 | verified |
| `f33_interest_on_school_debt_us` | 23,088,280 | USD thousands | FY2024 | verified |
| `f33_fall_membership_by_state` | dict, 52 keys | pupils | FY2024 | verified |
| `f33_fall_membership_us` | 46,370,928 | pupils | FY2024 | verified |
| `f33_district_file_join_key` | NCESID | column name | FY2024 | verified |
| `f33_district_file_columns` | dict, 17 keys | column names | FY2024 | verified |
| `ccd_lea_membership_join_key` | LEAID | column name | school year 2023-24 | verified |
| `ccd_lea_membership_race_values` | [American Indian or Alaska Native, Asian, Black or African American, Hispanic/Latino…] | RACE_ETHNICITY values | school year 2023-24 | verified |
| `ccd_lea_membership_total_indicator_values` | dict, 5 keys | TOTAL_INDICATOR values | school year 2023-24 | verified |
| `ccd_lea_membership_count_column` | STUDENT_COUNT | column name | school year 2023-24 | verified |
| `district_hispanic_differential_by_state` | **null** | dollars per pupil by state FIPS | FY2024 finance x SY2023-24 membership | unverified |
| `district_white_differential_by_state` | **null** | dollars per pupil by state FIPS | FY2024 finance x SY2023-24 membership | unverified |

## ell

12 verified, 0 unverified. California and Texas from the statutes themselves. The national premium is a range across cost studies, not a point estimate.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `ca_lcff_supplemental_grant_pct` | 20 | percent of adjusted base grant | current statute as of 2026-09-17 | verified |
| `ca_lcff_concentration_grant_pct` | 65 | percent of adjusted base grant | 2021-22 forward | verified |
| `ca_lcff_concentration_threshold_pct` | 55 | percent of total enrollment | current statute as of 2026-09-17 | verified |
| `tx_bilingual_allotment_weight_emergent_bilingual` | 0.1 | multiplier on basic allotment | current statute as of 2026-09-17 | verified |
| `tx_bilingual_allotment_weight_dual_language_immersion` | 0.15 | multiplier on basic allotment | current statute as of 2026-09-17 | verified |
| `tx_bilingual_allotment_weight_non_eb_two_way` | 0.05 | multiplier on basic allotment | current statute as of 2026-09-17 | verified |
| `tx_bilingual_allotment_spend_requirement_pct` | 55 | percent | current statute as of 2026-09-17 | verified |
| `national_el_cost_premium_weight_range_pjp` | [0.39, 2.0] | additional weight on base per-pupil funding | studies conducted 1990-2011 | verified |
| `national_el_cost_premium_evidence_based_dollar_range` | [41, 700] | USD per EL (nominal, as published) | studies conducted 1990-2011 | verified |
| `acs_pums_2024_eng_codes` | dict, 5 keys | code -> label | ACS 2024 | verified |
| `acs_pums_2024_sch_codes` | dict, 4 keys | code -> label | ACS 2024 | verified |
| `acs_pums_2024_schg_codes` | dict, 17 keys | code -> label | ACS 2024 | verified |

## state_medicaid_undocumented

16 verified, 6 unverified. The thinnest group. Programs differ in design and fiscal year across states, so these are not a comparable panel.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `il_hbia_state_cost` | 404,000,000 | USD | SFY2025 | verified |
| `il_hbis_state_cost` | 134,000,000 | USD | SFY2025 | verified |
| `il_hbia_hbis_total_state_cost` | 538,000,000 | USD | SFY2025 | verified |
| `us_emergency_medicaid_total_2023` | 3,775,000,000 | USD | FFY2023 | verified |
| `us_emergency_medicaid_total_2017_2023` | 26,554,000,000 | USD | FFY2017-2023 cumulative | verified |
| `or_healthier_oregon_gf_2025_27` | 1,100,000,000 | USD | 2025-27 biennium (Current Service Level) | verified |
| `or_healthier_oregon_gf_2023_25` | 725,500,000 | USD | 2023-25 biennium | verified |
| `wa_apple_health_expansion_service_dollars_2023_25` | 72,000,000 | USD | 2023-25 biennium | verified |
| `wa_apple_health_expansion_request_gfs_2025_27` | 84,281,000 | USD | 2025-27 biennium (agency REQUEST, not enacted) | verified |
| `ny_ep_to_medicaid_state_cost_annual` | 3,000,000,000 | USD | FY2027 NYS (annualized projection) | verified |
| `ny_ep_to_medicaid_global_cap_add_fy2027` | 2,000,000,000 | USD | FY2027 NYS | verified |
| `co_omnisalud_subsidy_spend_py2026` | 50,000,000 | USD | plan year 2026 (estimate) | verified |
| `co_cover_all_coloradans_children_state_cost` | **null** | USD |  | unverified |
| `mn_minnesotacare_undocumented_state_cost` | **null** | USD |  | unverified |
| `ma_health_safety_net_state_cost` | **null** | USD |  | unverified |
| `ca_full_scope_medical_adults_26_49_total_funds` | 3,300,000,000 | USD | SFY2024-25 | verified |
| `ca_full_scope_medical_adults_26_49_general_fund` | 2,800,000,000 | USD | SFY2024-25 | verified |
| `ca_undocumented_expansion_population_general_fund_2025_26` | 10,800,000,000 | USD | SFY2025-26 | verified |
| `ca_undocumented_expansion_caseload_2025_26` | 1,700,000 | enrollees | SFY2025-26 | verified |
| `ca_undocumented_total_general_fund_2024_25` | **null** | USD | SFY2024-25 | unverified |
| `general_fund_cost_by_state_fy2024` | **null** | dollars by state FIPS | FY2024 | unverified |
| `share_already_inside_meps` | **null** | share |  | unverified |

## corporate

17 verified, 1 unverified. Treasury Office of Tax Analysis is the incidence source; jct.gov is unreachable.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `treasury_ota_corporate_tax_share_to_labor` | 18 | percent | Treasury distributional methodology, 2012 model year forward | verified |
| `treasury_ota_corporate_tax_share_to_capital` | 82 | percent | Treasury distributional methodology, 2012 model year forward | verified |
| `jct_corporate_tax_share_to_labor` | **null** | percent |  | unverified |
| `stc_2024_corporation_net_income_tax_us` | 165,294,651 | USD thousands | FY2024 | verified |
| `stc_2024_corporation_net_income_tax_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `stc_2024_selective_sales_total_us` | 212,282,780 | USD thousands | FY2024 | verified |
| `stc_2024_selective_sales_total_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `stc_2024_motor_fuels_us` | 58,471,778 | USD thousands | FY2024 | verified |
| `stc_2024_motor_fuels_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `stc_2024_alcoholic_beverages_sales_tax_us` | 8,410,807 | USD thousands | FY2024 | verified |
| `stc_2024_alcoholic_beverages_sales_tax_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `stc_2024_tobacco_products_us` | 15,663,489 | USD thousands | FY2024 | verified |
| `stc_2024_tobacco_products_by_state` | dict, 52 keys | USD thousands | FY2024 | verified |
| `stc_2024_total_taxes_us` | 1,472,039,413 | USD thousands | FY2024 | verified |
| `stc_2024_general_sales_us` | 465,395,016 | USD thousands | FY2024 | verified |
| `stc_2024_individual_income_us` | 479,627,360 | USD thousands | FY2024 | verified |
| `state_corporate_net_income_tax_2024` | 165,294.651 | USD millions | FY2024 | verified |
| `state_selective_sales_taxes_2024` | 212,282.78 | USD millions | FY2024 | verified |

## underreporting

12 verified, 3 unverified. Both primary papers re-verified tonight; the prior repo lane's parameters match them.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `cps_asec_total_net_survey_error_dollars_pct_2017` | dict, 8 keys | percent of coverage-adjusted administrative aggregate | CPS ASEC 2018 (income year 2017) | verified |
| `cps_asec_coverage_ratio_dollars_2017` | dict, 8 keys | ratio of survey dollars to administrative aggregate | CPS ASEC 2018 (income year 2017) | verified |
| `cps_proportional_dollar_bias_2000_2012_meyer_mok_sullivan` | dict, 7 keys | proportional bias in mean program dollars | 2000-2012 average | verified |
| `cps_proportional_month_bias_2000_2012_meyer_mok_sullivan` | dict, 7 keys | proportional bias in months received | 2000-2012 average | verified |
| `housing_assistance_coverage_ratio` | **null** | ratio |  | unverified |
| `eitc_coverage_ratio` | **null** | ratio |  | unverified |
| `repo_lane_ratio_base` | dict, 6 keys | ratio of survey dollars to administrative aggregate | prior lane, 2026-09-16 | verified |
| `repo_lane_ratio_noncash_extended` | dict, 4 keys | ratio | prior lane, 2026-09-16 | verified |
| `repo_lane_ratio_w21399_variant` | dict, 4 keys | ratio | prior lane, 2026-09-16 | verified |
| `ratio_snap` | 1.8832 | admin/survey ratio | income year 2017 (w35680) / 2000-2012 average (w21399) | verified |
| `ratio_tanf` | 2.0 | admin/survey ratio | income year 2017 (w35680) / 2000-2012 average (w21399) | verified |
| `ratio_ssi` | 0.9814 | admin/survey ratio | income year 2017 (w35680) / 2000-2012 average (w21399) | verified |
| `ratio_ui` | 1.7331 | admin/survey ratio | income year 2017 (w35680) / 2000-2012 average (w21399) | verified |
| `ratio_social_security` | 1.0881 | admin/survey ratio | income year 2017 (w35680) / 2000-2012 average (w21399) | verified |
| `ratio_housing` | **null** | admin/survey ratio |  | unverified |

## improper_payments

9 verified, 0 unverified. paymentaccuracy.gov FY2024 reporting year, read through a rendering browser.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `eitc` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `additional_child_tax_credit` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `medicaid` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `medicare_ffs` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `snap` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `ssi` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `unemployment_insurance` | dict, 7 keys | USD millions and percent | FY2024 (reporting year) | verified |
| `eitc_improper_payments_fy2024` | 15,941.61 | USD millions | FY2024 (reporting year) | verified |
| `actc_improper_payments_fy2024` | 3,446.56 | USD millions | FY2024 (reporting year) | verified |

## meps_coverage

25 verified, 0 unverified. The MEPS-to-NHEA reconciliation is produced only every five years; 2012 is the latest.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `meps_phc_unadjusted` | 1,350.7 | USD billions | calendar 2012 | verified |
| `nhea_phc_unadjusted_2012` | 2,366.9 | USD billions | calendar 2012 | verified |
| `nhea_phc_adjusted_to_meps_2012` | 1,717.9 | USD billions | calendar 2012 | verified |
| `meps_share_of_adjusted_nhea_phc` | 0.7863 | ratio | calendar 2012 | verified |
| `meps_share_of_unadjusted_nhea_phc` | 0.5707 | ratio | calendar 2012 | verified |
| `meps_vs_adjusted_nhea_shortfall_by_payer_pct` | dict, 8 keys | percent of adjusted NHEA | calendar 2012 | verified |
| `nhea_components_excluded_from_meps_2012` | dict, 22 keys | USD billions | calendar 2012 | verified |
| `nhea_2023_total_national_health_expenditures` | 4,925.3 | USD billions | calendar 2023 | verified |
| `nhea_2023_medicare_total` | 1,037.3 | USD billions | calendar 2023 | verified |
| `nhea_2023_medicaid_total` | 873.7 | USD billions | calendar 2023 | verified |
| `nhea_2023_medicaid_federal` | 592.6 | USD billions | calendar 2023 | verified |
| `nhea_2023_medicaid_state_local` | 281.1 | USD billions | calendar 2023 | verified |
| `nhea_2023_private_health_insurance` | 1,511.2 | USD billions | calendar 2023 | verified |
| `nhea_2023_out_of_pocket` | 525.4 | USD billions | calendar 2023 | verified |
| `nhea_2023_personal_health_care_total` | 4,162.8 | USD billions | calendar 2023 | verified |
| `nhea_2023_phc_medicare` | 962.7 | USD billions | calendar 2023 | verified |
| `nhea_2023_phc_medicaid` | 784.2 | USD billions | calendar 2023 | verified |
| `nhea_2023_phc_private_health_insurance` | 1,342.1 | USD billions | calendar 2023 | verified |
| `nhea_2023_phc_out_of_pocket` | 525.4 | USD billions | calendar 2023 | verified |
| `nhea_2023_nursing_care_facilities_total` | 205.0 | USD billions | calendar 2023 | verified |
| `nhea_2023_nursing_care_medicaid` | 72.0 | USD billions | calendar 2023 | verified |
| `nhea_2023_nursing_care_medicare` | 44.0 | USD billions | calendar 2023 | verified |
| `nhea_2023_nursing_care_out_of_pocket` | 45.8 | USD billions | calendar 2023 | verified |
| `nhea_to_meps_ratio_medicaid` | 1.5432 | ratio (adjusted NHEA / MEPS) | calendar 2012 | verified |
| `nhea_to_meps_ratio_medicare` | 1.2804 | ratio (adjusted NHEA / MEPS) | calendar 2012 | verified |

## veterans_federal_retirement

6 verified, 0 unverified. The headline finding is a negative: CPS ASEC carries no federal-pension dollar amount.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `cps_asec_veteran_status_variable` | PEAFEVER | variable name | CPS ASEC March 2025 | verified |
| `cps_asec_veterans_payments_variables` | dict, 9 keys | variable names | CPS ASEC March 2025 | verified |
| `cps_asec_pension_source_codes` | dict, 9 keys | code -> label | CPS ASEC March 2025 | verified |
| `cps_asec_federal_pension_amount_available` | False | boolean | CPS ASEC March 2025 | verified |
| `cps_asec_pension_receipt_flag` | PEN_YN | variable name | CPS ASEC March 2025 | verified |
| `omb_602_cross_reference` | omb.subf_602_federal_employee_retirement_disability | pointer | FY2024 | verified |

## city_migrant

22 verified, 1 unverified. City fiscal years differ from each other and from the federal one. Border encounters are events, not persons.

| key | value | unit | fiscal year | status |
|---|---|---|---|---|
| `nyc_asylum_seeker_spending_fy2024_total` | 3,752,000,000 | USD | NYC FY2024 (July 2023-June 2024) | verified |
| `nyc_asylum_seeker_spending_fy2024_city_funds` | 2,323,000,000 | USD | NYC FY2024 | verified |
| `nyc_asylum_seeker_spending_fy2024_state_funds` | 1,310,000,000 | USD | NYC FY2024 | verified |
| `nyc_asylum_seeker_spending_fy2024_federal_funds` | 120,000,000 | USD | NYC FY2024 | verified |
| `nyc_asylum_seeker_spending_fy2023_total` | 1,474,000,000 | USD | NYC FY2023 | verified |
| `nyc_asylum_seeker_spending_fy2025_total` | 3,020,000,000 | USD | NYC FY2025 | verified |
| `chicago_new_arrivals_fy2024_initial_budget` | 150,000,000 | USD | City of Chicago FY2024 (calendar 2024) | verified |
| `chicago_new_arrivals_fy2024_supplemental` | 70,000,000 | USD | City of Chicago FY2024 | verified |
| `chicago_new_arrivals_fy2024_actual_spend` | **null** | USD | City of Chicago FY2024 | unverified |
| `denver_newcomer_support_2024_budget` | 90,000,000 | USD | Denver calendar 2024 | verified |
| `denver_newcomer_support_2025_budget` | 12,500,000 | USD | Denver calendar 2025 | verified |
| `ma_emergency_assistance_family_shelter_fy2024_expended` | 643,251,902 | USD | Massachusetts SFY2024 | verified |
| `ma_emergency_assistance_fy2024_appropriation` | 325,251,902 | USD | Massachusetts SFY2024 | verified |
| `ma_emergency_assistance_fy2023_expended` | 274,379,281 | USD | Massachusetts SFY2023 | verified |
| `ma_emergency_assistance_fy2025_projected` | 587,071,903 | USD | Massachusetts SFY2025 | verified |
| `cbp_sw_border_encounters_fy2024_total` | 2,135,005 | encounters | FY2024 | verified |
| `cbp_sw_border_encounters_fy2024_mexico` | 653,684 | encounters | FY2024 | verified |
| `cbp_sw_border_mexico_share_fy2024_pct` | 30.62 | percent | FY2024 | verified |
| `cbp_sw_border_usbp_only_fy2024_total` | 1,530,523 | encounters | FY2024 | verified |
| `cbp_sw_border_usbp_only_fy2024_mexico` | 502,279 | encounters | FY2024 | verified |
| `cbp_nationwide_encounters_fy2024_total` | 2,901,142 | encounters | FY2024 | verified |
| `cbp_nationwide_encounters_fy2024_mexico` | 668,088 | encounters | FY2024 | verified |
| `mexico_share_sw_encounters_fy2024` | 0.3062 | share | FY2024 | verified |

## Could not verify

Thirteen entries carry `value: null`. Each keeps its `source_url` where one exists and a note recording exactly what was tried.

| key | what blocked it |
|---|---|
| `k12.district_hispanic_differential_by_state` | DERIVED, not fetched |
| `k12.district_white_differential_by_state` | DERIVED, not fetched |
| `state_medicaid_undocumented.co_cover_all_coloradans_children_state_cost` | Program structure verified but the dollar value of the line item was not isolated |
| `state_medicaid_undocumented.mn_minnesotacare_undocumented_state_cost` | NOT VERIFIED from a primary source in this session |
| `state_medicaid_undocumented.ma_health_safety_net_state_cost` | NOT ATTEMPTED beyond a search pass — ran out of budget |
| `state_medicaid_undocumented.ca_undocumented_total_general_fund_2024_25` | COULD NOT VERIFY from a primary source tonight |
| `state_medicaid_undocumented.general_fund_cost_by_state_fy2024` | NOT AVAILABLE as an FY2024 panel |
| `state_medicaid_undocumented.share_already_inside_meps` | NOT AN EXTERNAL PARAMETER |
| `corporate.jct_corporate_tax_share_to_labor` | COULD NOT FETCH |
| `underreporting.housing_assistance_coverage_ratio` | NOT PUBLISHED in either source the brief names |
| `underreporting.eitc_coverage_ratio` | NOT PUBLISHED in either named source |
| `underreporting.ratio_housing` | NO PUBLISHED VALUE |
| `city_migrant.chicago_new_arrivals_fy2024_actual_spend` | COULD NOT VERIFY |

Five of the thirteen are genuine fetch failures: the Joint Committee on Taxation incidence assumption, California's all-undocumented General Fund total, Colorado's children's line item, Minnesota's MinnesotaCare expansion cost, and Chicago's actual new-arrivals spending. Four are things no source publishes: housing-assistance and Earned Income Tax Credit survey coverage ratios, the share of state coverage already inside the survey, and a comparable state panel. Four are quantities the builder derives rather than fetches.

## Staged files

48 files are listed under the top-level `staged_files` key with absolute path, sha256, source URL and a parsing note. They sit under `~/research-data/immigration-fiscal/data/external/`, except the two pre-existing caches the brief said to reuse.

Three notes are worth reading before the code touches the file:

- The Common Core of Data district membership CSV is long format. Summing the count column without filtering the total indicator multiple-counts every student.
- The Census school-district finance file holds dollars in thousands and has no per-pupil column.
- The DHS FY2025 Budget in Brief is staged only as a marker: its FY2024 column is an annualized continuing resolution, not enacted.

## Traps worth carrying forward

- Subfunction 551 is "Health care services", not Medicaid. The OMB functional classification has no Medicaid subfunction. Use the National Health Expenditure figures in `meps_coverage` instead.
- Homeland Security's own unauthorized-population estimates stop at January 2022, at 11.0 million. Pew's mid-2023 estimate is 14.0 million. A fiscal-2024 ledger anchored on the official series is anchored three million people low.
- Massachusetts line item 7004-0101 is the whole Emergency Assistance family shelter system, not a migrant program. Fiscal 2024 spending is double the appropriation, but attributing the increment to migrants is an inference the builder must state, not a claim the source makes.
- The Congressional Budget Office emergency-Medicaid total covers people ineligible for full Medicaid by reason of immigration status or the five-year waiting period, and the letter says outright that it cannot separate parolees and lawfully-present temporary residents from people here illegally.
- The Current Population Survey reports one pension dollar field across all sources. A federal pension can be identified but not valued.
- The placeholder's Earned Income Tax Credit figure of 21,900 is the fiscal 2025 number. Fiscal 2024 is 15,941.61.
