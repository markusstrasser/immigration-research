Model self-report: claude-opus-5-5
**Verdict:** All 18 lanes and tests/ read. Only scale_spillovers scores years on 2020+ ACS (ACS 2024 SCHL: none = 0, grades 1-8 = 1-8), and only in side specs and the unadded innovation arm, not the central +$13.9bn. projection_backtest (IPUMS 1990-2023) and figures (hand-typed arrival less-than-HS series, 1980-2023) compare years across 2019/2020, but only at the less-than-HS boundary. mexican_origin_population_total scores years on CPS 2025, not ACS. The rest use coarse bands (lowest cut: 12th grade no diploma vs diploma) on ACS 2024 alone, use CPS, or have no schooling. Pointer outside scope: build/build_tier_a_context_panels.py, run by acquire, uses the raw SCHL code as years in AGEP−SCHL−6 on ACS 2023.

[UNVERIFIED] Fact collection for the ACS/IPUMS 2020+ no-schooling break triage. Read-only probe of the lanes listed below; no scripts were run. Each section cites file:line. All listed lanes have a section; none could not be determined.

Lanes in scope (infra/immigration-fiscal/): acquire, ancestry_iv_congestion_wages_2026_09_23, care_household_services_2026_09_23, civic_service_by_ancestry_2026_09_21, construction_housing_supply_2026_09_23, consumer_price_benefit_2026_09_18, cps_generation_welfare_2026_09_16, cps_imputation_keys_2026_09_23, cultural_output_2026_09_19, institutional_education_2026_09_19, mexican_origin_population_total_2026_09_19, mr_leads_papers_2026_09_21, projection_backtest_2026_09_19, scale_spillovers_2026_09_23, second_generation_by_origin_2026_09_22, congestion_2026_09_23, mr_archive_2026_09_18, figures_2026_09_22, tests/.


## acquire

- Source: download/staging only; no schooling mapping in this lane. It fetches the 2023 ACS 1-year person PUMS (`acquire/setup.sh:108-109`), submits an IPUMS-CPS ASEC 1994+ extract whose variables include `EDUC` (`acquire/ipums_cps_second_gen.py:32-36`; CPS, not ACS), pulls LEHD QWI with education E1 <HS / E2 HS / E3 some college / E4 BA+ (`acquire/pull_qwi_state_panel.py:69-70`), and copies a built file `stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv` (`acquire/setup-lifetime.sh:318`).
- Mapping lives downstream, in `build/` (outside this list): the copied bucket file is `SCHL<16` '<HS', 16-17 'HS / GED', 18-20 'some college / associate' on ACS 2023, age 25-64 foreign-born (`build/build_immigration_warehouse.py:320-333`) — coarse bands only.
- Pointer for the `build/` triage: `acquire/setup-tier-a-labor-demography.sh:63` runs `build/build_tier_a_context_panels.py`, which on the 2023 ACS PUMS bands `SCHL<12` 'dropout' (grade 8 or less incl. none) / `<16` 'hs' / else 'college' (`build/build_tier_a_context_panels.py:451-454`) and scores potential experience as `AGEP − SCHL − 6`, using the raw SCHL code as years (`:456-460`). A no-schooling report (SCHL 1) therefore gets 3-10 more "experience" years than the same person reporting grades 1-8 (SCHL 4-11). Outputs `borjas_supply_shock_cell_2023.csv`, `bgh_outcomes_cell_2023.csv` (`:489`, `:509`); single year 2023, no 2019/2020 comparison.
- The IPUMS USA decennial README asks for 1960-2000 samples only (`acquire/setup-tier-a-labor-demography.sh:46-59`).
- Exposure facts for this lane itself: no boundary, scoring, ranking or year comparison.

## ancestry_iv_congestion_wages_2026_09_23

- Source: IPUMS USA samples `us2000a`, `us2010a`, `us2011c` (ACS 2009-2011 3-year) and `us1990a` (`ipums_extract.py:39`, `:45`; `estimate_wages.py:32` SAMPLES 200001/201001/201103). No survey year after 2011.
- Mapping (`build_pums.py:46-52`): EDUCD 2-61 → 0 (less than HS; lumps no schooling, grades 1-8, grade 9 and 12th-no-diploma 61), 62-64 → 1 HS/GED, 65-100 → 2 some college/associate, 101 → 3 BA, 110+ → 4 graduate; EDUCD 0-1 → −1 and dropped from the wage sample (`build_pums.py:67-68`). Lowest boundary is 61/62 (no diploma vs diploma). No years scoring, no ranking.
- Use: cell key for composition adjustment (age5 × sex × edu5, `build_pums.py:18-21`, `:79-88`) and group masks noba/ba/hsl (`build_pums.py:99`).
- The "2024 presence" scaling reads CPS, not ACS: `production_nativity_nest_2026_09_22/derived/branch_composition.csv`, PEARNVAL proxy, splits `below_ba` / `hs_or_less` (`estimate_wages.py:35`, `:92-97`).
- Headlines (RESULT.md:17-25): natives without a BA −0.11% (0.32) per point of immigrant employment share; −1.2% or −$47bn at 2024 presence; relative wage of less-educated natives −0.64% (0.22), σ̂ 2.3.
- Exposure facts: no 2020+ ACS/IPUMS data; coarse bands only.

## care_household_services_2026_09_23

- Source: ACS 2024 1-year person PUMS only (`acs_extract.py:2`, `:40` ZIP `acs_pums_2024_1yr/csv_pus.zip`). No other survey year; no 2019/2020 comparison or pooling.
- Mapping: "no diploma" = `SCHL<=15` (`acs_extract.py:20`, `:121`), used for the Cortés–Tessada low-skill share, the Cortés (2008) share and `likely_undoc` care workers (`:172`, foreign-born Hispanic `SCHL<=15`); Butcher–Moran–Watson "less than one year of college" = `SCHL<=18` (`:23`, `:139-141`, `:175`); college = `SCHL>=21` for the women populations (`:309`). Lowest boundary is 15/16, i.e. 12th grade no diploma vs diploma. No boundary below grade 10, no years scoring; the only ranking is of women by hourly wage (p75 cut, `:295-307`), not by schooling.
- Headlines: additive channels $4.15bn ($2.60–13.35bn) (`derived/summary.csv` TOTAL row; RESULT.md:7); taxes on native women's extra hours $2.69bn, which rests on the fall in ℒ = ln[(no-diploma immigrants + natives)/LF] of 0.283 (RESULT.md:73-75: group holds 35.8% of no-diploma labour 16-64, 50.7% of no-diploma immigrants in the civilian LF).
- Exposure facts: coarse bands only, single year 2024. The 15/16 (no-diploma vs diploma) boundary is load-bearing for ℒ.

## civic_service_by_ancestry_2026_09_21

- Source: ACS 2024 1-year PUMS through the Census tabulate API (`service.py:1`, `:4-6`; RESULT.md:17-19). Single year; no 2019/2020 comparison.
- Mapping: the only schooling use is a filter `SCHL=21:24` (bachelor's or higher) for the degree-holder universes `men_25_49_ba` and `men_25_34_ba` (`service.py:28`, `:31`). Other universes have no schooling filter (`:27`, `:30`). No boundary below BA, no years scoring, no ranking.
- Headline (RESULT.md:5-12): US-born men ever on active duty, Asian Indian 1.05% vs 6.6–7.8% for English/German/Irish at 18–49; among degree holders 25–49, 0.79% vs 6.7–6.9%; Mexican-ancestry degree holders 8.2% (`derived/military_service_by_ancestry.csv`).
- Exposure facts: none of the four conditions applies.

## construction_housing_supply_2026_09_23

- Source: ACS 2024 1-year person PUMS only (`tabulate.py:1`, `:45` `acs_pums_2024_1yr`). No other survey year; no 2019/2020 comparison.
- Mapping (`tabulate.py:136-137`): `SCHL<=17` → hs_or_less (diploma/GED or less, incl. none and 12th-no-diploma), `<=20` → some_college, else ba_plus; sets `below_ba` = first two (`tabulate.py:81-87`; docstring `:21-22`). Lowest boundary 17/18 (HS/GED vs some college). No split inside less-than-HS, no years scoring, no ranking.
- Use: `ell_hs_or_less` 0.472 and `ell_below_ba` 0.761, shares of construction-industry earnings (`supply.py:305-306`; `derived/supply_parameters.csv:5-6`), and the Monras sensitivity dose = Mexico-born / hs_or_less employed (`supply.py:261-268`).
- Headline (RESULT.md:1-12): construction costs 0.75% lower (0.53–1.17%); offset $3.6bn/yr to other renters' $33.5bn ($2.2–5.8bn); judged inside P, not added.
- Exposure facts: coarse bands only, single year 2024.

## consumer_price_benefit_2026_09_18

- Source: ACS 2024 1-year person PUMS only (`acs_extract.py:2`, `:34-36`; `acs_native_lowskill.py:23`). No other survey year; no 2019/2020 comparison.
- Mapping: `dropout = schl <= 15` (less than a diploma, incl. 12th-no-diploma), `nocollege = schl <= 19`, `college = schl >= 21` (`acs_extract.py:119-121`; same cuts `acs_native_lowskill.py:41-42`). Lowest boundary 15/16. No boundary below grade 10, no years scoring; the only ranking is women's hourly wage (p75, `acs_extract.py:196-203`), not schooling.
- Headline (RESULT.md:3, :9): shock = foreign-born dropouts 3.781% of the civilian LF (6,635,078 / 175,478,713), Mexico-born 1.804%, Δln −0.6303 (`derived/lowskill_share.csv` rows US fb_dropout / mexborn_dropout); consumer surplus $23.8bn/yr, hours tax $8.7bn/yr, native-dropout wage offset $10.7bn/yr. (The $8.7bn hours tax was later corrected to $2.7bn by care_household_services_2026_09_23, RESULT.md:13 there.)
- Exposure facts: coarse bands only, single year 2024. The 15/16 boundary defines the treatment share.

## cps_generation_welfare_2026_09_16

- Source: CPS ASEC 2024 and 2025 through the Census API, variable `A_HGA` (`pull_cps_asec.sh:16`, default YEARS 2025 2024 at `:18`). No ACS or IPUMS USA.
- Mapping: adults 25-64, `lt_hs = A_HGA<=38` (through 12th grade no diploma), `hs_only = A_HGA==39`, `ba_plus = A_HGA>=43` (`mexican_origin_by_generation.py:61-64`); household reference person `lowed = A_HGA<=39` (HS or less) as a subgroup filter (`asec_generation_welfare.py:103`, `:123`, `:128`). Lowest boundary 38/39 (12th no diploma vs diploma). No boundary below grade 10, no years scoring, no ranking.
- Headline schooling output: descriptive shares in `mexican_origin_result_2025.txt` (e.g. adults 25-64 lt_hs 41.1% Mexico-born, 9.6% Mexican 2nd gen, 3.7% gen3+ NH white); each ASEC year tabulated separately, no pooling.
- Exposure facts: CPS only (outside the ACS break); coarse bands.

## cps_imputation_keys_2026_09_23

- Source: CPS ASEC 2025 public-use file only (`common.py:3`, `:23` `asecpub25csv.zip`), variable `A_HGA` (`common.py:32`). No ACS or IPUMS USA.
- Mapping (`common.py:351-352`): `edu5` = A_HGA 0 → 0 (not in universe), ≤38 → 1 (less than HS through 12th no diploma), 39 → 2 HS, ≤42 → 3 some college/associate, 43 → 4 BA, else 5; `edu4` collapses BA+. Lowest boundary 38/39 (12th no diploma vs diploma). No boundary below grade 10, no years scoring, no ranking.
- Use: cell key only — hot-deck donor cells (`hotdeck.py:51-63`), IPW reweighting cells age × sex × edu5 × nativity × union (`ipw.py:19-24`), match-bias and weekly-validation cells (`matchbias.py:19`, `validate_weekly.py:131`).
- Headline (RESULT.md:3-14): account understates the union's net cost by about $9–15bn/yr (range $5–18bn); corrections (a) +$13.0/+16.5bn, (b) +$9.2/+11.4bn.
- Exposure facts: CPS only (outside the ACS break); coarse cell keys.

## cultural_output_2026_09_19

- Source: ACS 2024 1-year person PUMS (`scripts/01_build_pums_parquet.py:2`, `:22`); ACS 1-year tables B15002/C15002I for 2010, 2015, 2019, 2023, 2024 (BA+ counts only; `scripts/09_fetch_education_benchmarks.py:3-10`, `derived/education_benchmarks.csv`); CPS `A_HGA>=43` (BA+) in the generation check (`scripts/13_arm_a_cps_generation_check.py:41`, `:128`).
- Mapping (`scripts/02_arm_a_creative_labour.py:101-105`): `SCHL<=15` 1_lths, `<=17` 2_hs, `<=20` 3_somecoll, `=21` 4_ba, else 5_grad; `ba` = `SCHL>=21` (`:89-91`). Lowest boundary 15/16. No boundary below grade 10, no years scoring, no ranking.
- Use: cells for direct standardisation to the US-born NH-white age × educ × sex distribution (`:15`, `:143`, `:214-218`, `:280`). The benchmark series compares years across 2019/2023/2024 but only for the Hispanic share of BA+ holders.
- Headline (RESULT.md:3-6, :41-46): creative labour per head at matched age × educ × sex, ratio to white 0.742 (SE 0.059) Mexico-born, 0.723 (0.034) US-born Mexican-origin; age × educ only 0.736 / 0.719 (RESULT.md:48-50). Awards benchmark: Hispanic share of BA+ 9.6% (2023 ACS) vs 6.2% (2010 ACS) (RESULT.md:8-9; years picked at `scripts/15_fill_result.py:124-125`).
- Exposure facts: coarse bands, single ACS PUMS year 2024; the 2019-2024 comparison is of BA+ only.

## institutional_education_2026_09_19

- Source: ACS 2024 1-year person PUMS only (`institutional_counts.py:26`, `:205`, `:211`; README.md:3). No other survey year; no 2019/2020 comparison.
- Mapping (`institutional_counts.py:88-91`; README.md:20): `SCHL 1..15` lt_hs, `16,17` hs_only, `18..20` some_college, `21..24` ba_plus, ages 25+. SCHL outside 1-24 for an adult raises an error (`:83-85`); no-schooling (SCHL 1) is kept inside lt_hs, not dropped. Lowest boundary 15/16. No boundary below grade 10, no years scoring, no ranking.
- Output: stock counts by education × origin × age with 80 replicates (`derived/counts.npz`, `derived/counts.csv`); headline table (RESULT.md:5-15) is all-education (e.g. Mexico foreign-born institutional residents 25+ 80,327). Price scenarios are uncalibrated (RESULT.md:23).
- Exposure facts: coarse bands only, single year 2024.

## mexican_origin_population_total_2026_09_19

- Sources: ACS 2024 1-year PUMS is extracted with `SCHL` among its columns (`extract_acs.py:2`, `:29-30`), but no script uses SCHL (rg for `SCHL|schl` over `acs_ancestry.py`, `allocation_check.py`, `dt_replication.py`, `cps_counts.py`, `bounds_coverage_fiscal.py` returns nothing). The schooling measure comes from CPS ASEC 2025 `A_HGA` (`extract_cps.py:2-9`).
- Years scoring on CPS (`bounds_coverage_fiscal.py:51-52`): `HGA_YEARS = {0: 0, 31: 0, 32: 2.5, 33: 5.5, 34: 7.5, 35: 9, 36: 10, 37: 11, 38: 12, 39: 12, ...}` — less-than-1st-grade scored 0, grades 1-4 2.5, 5-6 5.5, 7-8 7.5, grade 9 9; 12th-no-diploma (38) and diploma (39) both 12. Mean years for adults 25+ (`:218-228`).
- Headline (RESULT.md:302-308; `derived/arm5_education_selectivity.csv`): Mexican third-plus self-ID 13.335 years vs third-plus NH white 14.384, gap 1.049; Duncan–Trejo +0.76 closes 72.4%, giving the middle arm's attriter gap −$1,418 per person (`derived/arm5_fiscal_implication.csv`). Single CPS year; no pooling or 2019/2020 comparison.
- Exposure facts: years are scored (below grade 10), but on CPS 2025, not ACS/IPUMS USA; the two groups compared are US-born third-plus. No ACS schooling output.

## mr_leads_papers_2026_09_21

- Source: ACS 1-year PUMS 2024 through the Census tabulate API (`pull_acs_care.py:17-18`, `ACS_YEAR` default 2024; README.md:14). No other year; no 2019/2020 comparison.
- Mapping: filters only — `SCHL=01:17` (high school/GED or less) for the labour-force queries (`pull_acs_care.py:30-31`) and `SCHL=01:18` (less than one year of college, the Butcher–Moran–Watson treatment) for working-age queries (`:34-37`). Lowest boundary 17/18. No boundary below grade 10, no years scoring, no ranking. The `lowed_lf_*` queries are not read by `elder_care_bound.py` (no match for `lowed_lf` there).
- Headline: nursing-home channel bound $2.3–14.6bn/yr Medicaid (README.md:3-5), from `share_mex = wa_lowed_mexico_born / wa_pop` (`elder_care_bound.py:54-63`); `derived/elder_care_bound.csv` preferred/labour_share 265,328 fewer institutionalized, Medicaid $14.61bn.
- The `notes/` files are paper readings (education mentions refer to the papers' own controls), not data work.
- Exposure facts: coarse filters only, single year 2024.

## projection_backtest_2026_09_19

- IPUMS USA (2020+ present): `ipums_usa_borjas_panel` rows with `YEAR IN (1990,2000,2010,2023)` (`cohorts.py:101-106`); 2023 is `us2023a`, the ACS 2023 1-year (`sources/immigration-fiscal/data/external/ipums/usa_extract/CATALOG.md:13`). Mapping `edu3 = 0 if EDUCD<62, 1 if 62-64, else 2` (`cohorts.py:113`): lowest boundary 61/62 (12th no diploma vs diploma); no split below grade 10, no years scoring, no ranking.
- That output compares survey years across 2019/2020: Mexico-born 1975-80 arrivals vs US-born, same birth proxies, below-HS and above-HS shares per survey year 1990/2000/2010/2023 (`cohorts.py:115-143` → `derived/fixed_birth_entry_cohorts.csv`), e.g. target_below_hs 0.693 (2010) → 0.671 (2023) for births 1956-65. Education is only reported, not a control; the headline column `relative_log_total_income` / `change_..._from_1990` (−0.005 in 2023) standardises by birth proxy only (`cohorts.py:127-146`).
- CPS 2025 (no ACS): recent-arrival education mix uses `education_origin_fiscal_2026_09_19/builder.py:33-43` masks, A_HGA 31-38 lt_hs / 39 / 40-42 / 43-46 (`sensitivities.py:144-160` → `derived/recent_arrival_education_mix.csv`: lt_hs 0.378 stock vs 0.324 recent 2016-2025) feeding `arrival_mix_lifetime_sensitivity.csv` (`:161-178`).
- GSS (no ACS): years `educ`, `maeduc`, `paeduc` banded <12 / =12 / >12 (`cohorts.py:9-12`, `:29`, `:52`), training through 1996 vs holdout 1998-2024 (`:31-35`) → `gss_transition_cells.csv`, `gss_temporal_prediction.csv`.
- Exposure facts: one IPUMS USA 2023 comparison across 2019/2020, at the <HS (EDUCD 61/62) boundary only.

## scale_spillovers_2026_09_23

- Source: ACS 2024 1-year person PUMS (`tabulate.py:1`, `:39`); IPUMS USA 1980/1990/2000 census shares for Moretti-period weights (`sample_weights.py:30-38`, `EDUCD<=61` lths from 1990; no 2020+ there). Single ACS year; no 2019/2020 comparison or pooling.
- **Years are scored** (`tabulate.py:46-47`): SCHL 1-3 (none, nursery, K) → 0, SCHL 4-11 (grades 1-8) → 1-8, 12 → 9, 13 → 10, 14 → 11, 15 (12th no diploma) → 11.5, 16-17 → 12, 18 → 12.5, 19 → 13.5, 20 → 14, 21 → 16, 22-24 → 18-20. Items `workers_yrs`, `adults25_yrs`, `workers_hsyrs = min(yrs,12)`, `workers_collyrs` (`:78-83`). Bands too: lths SCHL 1-15 (plus SCHL 0), hs 16-17, sc 18-20, ba 21, grad 22-24 (`:48`, `:90-95`).
- Years-based outputs (all non-central): workers' mean-years change dYRS +0.255 (`arms.py:209`; RESULT.md:71) → Ciccone–Peri / Acemoglu–Angrist average-schooling specs −$47bn to +$28bn (`arms.py:350-358`; RESULT.md:26-27, :154-159) and Ciccone–Peri joint +$116–169bn (`arms.py:480`; RESULT.md:32, :215-217); Iranzo–Peri HS-years dIPHS −0.250 with college +0.505 (`arms.py:213-219`, `:364`) → −$392bn to −$716bn (RESULT.md:29, :162-164); dHSY "years beyond 12" → −$92.1bn (`arms.py:366`; RESULT.md:165); BCHTT innovation at Mexico-born mean years 9.71 (adults 25+; `derived/pums_national.csv:34`) vs BCHTT's 10.88 (`arms.py:529-545`) → patents −$24.1bn, wages +$50.3bn (`derived/innovation_bchtt.csv` via `arms.py:668-669`, `derived/summary.csv`; RESULT.md:36-39, :237-245), "not added".
- Central headline does not score years: joint +$13.9bn (−$56.6 to +$84.4bn), scale +$38.6bn, composition −$24.9bn (RESULT.md:1-23; `derived/summary.csv`) use the some-college-or-more share dSC and earnings split lths+hs vs sc+ (`arms.py:195-208`), boundary 17/18.
- Exposure facts: years scoring with none = 0 vs grades 1-8 = 1-8 on ACS 2024, feeding side specs and the innovation arm; central CRY specs use coarse bands.

## second_generation_by_origin_2026_09_22

- Source: IPUMS-CPS ASEC, 32 samples 1994–2025 (`BRIEF.md:4`; RESULT.md:1, :13). Harmonised CPS `EDUC`, not ACS/IPUMS USA.
- Mapping (`analysis.py:55-57`, `:553-556`): `less_than_hs = 2 <= EDUC <= 71` (71 = 12th grade no diploma), `college_plus = EDUC >= 111`; NIU codes 0, 1, 999 excluded (`:541`). Lowest boundary 71/73 (no credential vs diploma). No split below grade 10, no years scoring ("no years-of-schooling scale is imputed", `analysis.py:1008`; RESULT.md:237, :277). A loader-reproduction gate averages the raw EDUC code (`mean_educ`, `analysis.py:221`), used only to match a committed CSV (`gate_g2`, `:238-244`).
- Pools survey years 1994–2025 (across 2019/2020) with age band × sex × survey-year adjustment (RESULT.md:13-17); `derived/period_trends.csv` gives period trends.
- Headline (RESULT.md:26-31): Mexico closing ratios, no-HS credential 0.762 (0.0044), BA+ 0.310 (0.0077) (`derived/closing_ratios.csv`).
- Exposure facts: CPS only (outside the ACS break); coarse bands.

## congestion_2026_09_23

- No schooling variable anywhere in the lane: the rg pattern returns 0 matches outside `_cache/`, and a case-insensitive search for `skill|college|diploma|hs_or|below_ba|SCHL|EDUC|grade` finds only place names in derived CSVs.
- ACS 2024 1-year PUMS columns read: STATE, PUMA, PWGTP, HISP, POBP, JWTRNS, JWMNP, JWDP, JWRIP, PINCP, ADJINC + replicates (`tabulate.py:1`, `:107-108`); NHTS 2017/2022 person and trip columns carry no education (`nhts.py:64-68`). Inputs from other lanes are geography crosswalks only (`arms.py:54-56`).
- Headline (RESULT.md:1-3): about $19bn a year (B1; range $8–35bn), no schooling dependence.

## mr_archive_2026_09_18

- No microdata and no schooling variable: the lane archives Marginal Revolution posts and extracts verbatim claims (RESULT.md:5-9). The only code match is a regex keyword list for tagging claims as "low-skill" (`extract_claims.py:64`, `less[- ]educated|high school dropout`); all other matches are post text in `derived/mr_posts*.{csv,jsonl}`, `mr_claims.csv`, and quoted claims in RESULT.md:161, :185.
- Exposure facts: none of the four conditions applies (no ACS/IPUMS read).

## figures_2026_09_22

- No microdata; the page reads other lanes' derived files (`build_data.cjs:145-330`) and hand-typed arrays in `src/data.js`. Most rg hits are "reduce" or education *spending* (schools/colleges dials, e.g. `account.cjs:99-109`, `proto/dots.cjs:92-100`), not attainment.
- Schooling inputs: (1) `high_skill_origin_screen_2026_09_21/derived/origin_screen.csv`, rows `education == "all"`, column `ba_plus_share_25_64` (`build_data.cjs:277-280`, `:295`); that file is CPS ASEC 2025 (`high_skill_origin_screen_2026_09_21/screen.py:1`, `:106`), education values `all`/`ba_plus` only. (2) Hand-typed Mexico-born 25-64 gaps within schooling level, below HS +$2,263, HS only −$2,286, below HS vs all natives −$13,502 (`src/data.js:86-91`, drawn in `src/lib/Skills.svelte:117-154`), cited to `education_origin_fiscal` comparisons.csv, a CPS/MEPS build (`education_origin_fiscal_2026_09_19/builder.py:1-4`, bands A_HGA 31-38 / 39 / 40-42 / 43-46 at `:33-43`).
- (3) Cross-2019/2020 series from IPUMS USA: hand-typed recent Mexico-born arrivals (25-54, within five years) less-than-HS share 82.5% (1980), 66.4, 61.5, 51.7% (2010), 33.3% (2023 ACS) (`src/data.js:53-60`), shown in `src/lib/Sentences.svelte:20-23`, `:74-81` ("fell from 82.5% to 33.3%"). Source: arrival-cohort memo (`research/immigration-mexican-arrival-cohorts-2026-09-18.md:6-7`, `:92-96`), whose lths is harmonised `EDUC <= 5` (grade 11 or less, incl. EDUC 0 "N/A or no schooling") in `arrival_cohorts_2026_09_18/entry_quality.py:35-37`; the 2023 value is `arrival_cohorts_2026_09_18/derived/entry_quality_fixed_duration_ipums.csv:10` (2018-2023, n 4,913, lths 0.3325). Coarse band; the none vs grades 1-8 split is inside it.
- No years scoring, ranking or sub-grade-10 boundary in this lane.

## tests/ (repo-level)

- Tests produce no outputs; they exercise `build/` modules with fixtures. None pins a boundary below grade 10, a years scale, a ranking or a 2019/2020 comparison.
- `test_sipp_person_donors.py:76-90` pins SIPP `EEDUC` buckets (31-38 → 1_lt_hs, 39 → 2_hs_ged, 40-41 some college, 42 associate, 43 BA, ...; SIPP, not ACS). The same file runs `build_federal_microsim_sipp_2024.build_acs_recipient_cells` on fixture ACS rows with `SCHL='16'` only (`:126-130`, `:219-226`); the module's ACS mapping is SCHL 1-15 '<HS', 16-17 'HS / GED', 18-20 'some college / associate', 21-24 'other' (`build/build_federal_microsim_sipp_2024.py:192-196`).
- `test_wage_race.py:16-17` uses a fixture default `SCHL=16`; the module under test reads SCHL only as BA+ (`>=21`) and a 1-24 validity check (`build/analyze_wage_race.py:99`, `:106`).
- `test_arrival_cohorts.py` tests ratios, SDR variance and entry windows only (`:13-42`); the module it imports uses ACS `SCHL 1-15` and `21-24` shares and donor education buckets (`build/analyze_arrival_cohorts.py:198-199`, `:219-222`) — no test covers that mapping.
- `test_lifetime_evidence_units.py:22`, `:100` check NPV-benchmark units and the presence of the ACS 2023 education-bucket table; `test_sipp_2025.py:28`, `:64` use EEDUC fixtures.
