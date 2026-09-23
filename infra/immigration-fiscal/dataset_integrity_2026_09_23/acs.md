**Verdict:** The largest ACS defect is a group-quarters coding regime in 2021–2023: 25–30% of
Mexico-born institutional residents (identified by birthplace) were coded generic "Other Hispanic",
against 2.5% in 2019, 5.4% in 2024 and about 1% in households; among native Hispanic institutional
residents the generic share doubled to 25–27% (F4).
The main case uses the clean 2024 file and already reallocates the generic excess, so it is
unaffected; used raw, the justice key would fall by $1.9bn, and the ledger's raw item N is short by
about $1.8bn (per `crime.md`). The second is the incarceration memo's comparison: Central American
and Dominican cells are read raw against native whites while the Mexican cell is quoted
coding-adjusted, so "Guatemalans and Dominicans at or below whites" does not survive the same
correction (0.99–1.26×, 1.02–1.30×) (F5). The two do not share a sign. Raw coding (F4) flatters the
group. The raw comparators (F5) make Mexican-origin look worse relative to other Latin American
origins. Other defects are small: ACS earnings allocation lifts the Mexico-born/white earnings ratio
from 0.572 to 0.589 (F3, flatters); the 2020 "no schooling" jump costs Latin American immigrants
0.25 years of measured schooling but leaves every category at or above high school unchanged (F6,
hurts, already priced in ladder 197). In group quarters, half the PUMS records are unflagged donor
copies (F1). ACS birthplace allocation in institutions is mildly US-tilted and moves about $0.08bn
between nativity columns (F2). [DATA/CALCULATION: scripts and `derived/acs_*.csv` in this directory]

# ACS / IPUMS USA integrity audit (2026-09-23)

## Files traced

The complete account's target and most keys are CPS ASEC 2025 (not this family). ACS/IPUMS USA
enter the headline numbers at these points [DATA: scripts named]:

| ACS/IPUMS input | Script that reads it | Repo number it feeds |
|---|---|---|
| ACS 2024 1-yr PUMS, institutional (TYPEHUGQ=2) × HISP × NATIVITY, 18–64; ACS 2020–24 5-yr | `cj_use_allocation_2026_09_23/acs_pull.py`, `allocate.py` | Main case: prisons custody key (+$2.63bn) and the m/p Hispanic→Mexican scaling in the police/courts arrest key (+$3.22bn); total +$5.94bn |
| ACS 2024 1-yr PUMS via API, TYPEHUGQ × SEX × age band for mexico_born (POBP=303), usborn_mexican (HISP=02), native NH white (RAC1P=1) | `institutional_bound_2026_09_17/pull_acs.py` → `derived/acs_cells.csv` | Generation split (`ledger_absolute_2026_09_17/absolute_ledger.py` institutional add, $18.4–19.8bn for the target) |
| ACS 2024 1-yr PUMS local, SCH/SCHG pupils per child | `build/measure_acs_school_exposure_2024.py` → `PUPIL_RATIO_*_ACS` in `gen_ledger_extension_2026_09_16/extend_ledger.py` | Generation split K-12 charge; the complete account replaced it with CPS October 2024 (`school_enrollment_2026_09_20`) |
| ACS 2023 1-yr tables B25103/B25077/B25064 | `gen_ledger_extension_2026_09_16/stage_inputs.py` | Generation split property tax / rent parameters |
| ACS 2024 1-yr PUMS (commuting, PUMA22) | `congestion_2026_09_23/tabulate.py` | Social item beside the headline ($19bn) |
| ACS PUMS, custody by year/cohort; IPUMS USA census 1980–2000 + ACS 2006–24 extracts 4–6, 9, 14, 15 | `acs_institutional_2026_09_16/*`, `crime_selection_cohorts_2026_09_23/*` | Crime/custody comparisons (institutional ratios by nativity and cohort) |
| IPUMS USA extracts 3, 12, 13 (Mexico-born education, QEDUC) | `schooling_selection_position_2026_09_23/*` | Ladder 197 (arrival selection rank) |

## Findings log (appended as confirmed)

**F1. Group-quarters records: half are whole-person donor copies with no flag.** Census's PUMS
accuracy document: "the number of imputed records was similar to the number of interviews";
imputed records copy an interviewed donor's whole vector and get "new values for the geography and
GQ type fields"; PUMS "does not carry variables that identify" them. [SOURCE: [2023 PUMS Accuracy
of the Data, pp. 5–7](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2023AccuracyPUMS.pdf);
IPUMS forum confirms no flag.] So the item flags on GQ records are the donors' flags, and the
justice lane's open question ("whether records imputed whole into group quarters carry the flag")
resolves to: they carry no whole-record flag at all. Consistent with that, records with 5+ core
items allocated are 4–5% of institutional Mexican-origin adults vs 12% in households: no cluster.
Effect: no sign bias expected (donors are drawn at random within GQ type and area), but the
effective institutional sample is about half its record count, so any SE computed from record
counts is too small by about √2. [DATA: `derived/acs_alloc_rates_2024.csv`; INFERENCE]

**F2. Birthplace allocation in ACS institutions is small and mildly US-tilted** (confirms
`crime.md` item 2 independently). Mexican-coded institutional 18–64: FPOBP=1 for 9.6% (2024) /
7.9% (2023); foreign-born share 22.2% among allocated vs 27.3% among reported (2023: 17.2% vs
21.0%). Spreading allocated birthplaces in the reported mix moves the Mexico-born share of
Mexican-coded institutional residents from 26.8% to 27.3% (2023: 20.7% → 21.0%). Effect on the
justice central: the total custody key is unchanged to <0.001 (CPS/ACS scaling is similar across
nativity); ≈ $0.08bn of the $17.2bn prisons charge moves from the US-born to the Mexico-born
column. Grade C, measured. Sign: flatters the Mexico-born, hurts the US-born, net ≈ 0.
[CALCULATION: `acs_alloc.py` → `derived/acs_custody_sensitivity_{2023,2024}.csv`]

**F3. ACS earnings allocation lifts Mexico-born earnings toward the reference.** Household
residents 25–54 with earnings: PERNP allocated for 34.7% of the Mexico-born, 30.6% of US-born
Mexican-origin and 19.7% of native NH whites (2024). Within education cells, allocated Mexico-born
earnings exceed reported ones by 9.2% (less than high school) and 6.9% (high school); for whites
the same cells differ by +4.6% and −0.6%. The Mexico-born/white earnings ratio is 0.589 with
allocated records and 0.572 on reported records only (2023: 0.586 vs 0.564); for the US-born
Mexican-origin it is 0.723 vs 0.732. Consistent with donors not matched on nativity [INFERENCE;
the ACS earnings donor-matching variables were not verified]. Effect: ACS-based Mexico-born
earnings and tax cross-checks (`tax_rerun_acs_2026_09_17`, `acs_earnings_replication_2026_09_17`,
screens) are ~3% (relative) too favourable; the account's earnings come from CPS (see `cps.md`), so
the main case is untouched. Grade C, measured. Sign: flatters the Mexico-born.
[CALCULATION: `acs_earn_alloc.py` → `derived/acs_earn_alloc_{2023,2024}.csv`]

**F4. 2021–2023 ACS institutional records lost their Hispanic detail; 2024 mostly recovered.**
Mexico-born (by birthplace, POBP=303) institutional residents 18–64 are stable at 65–77k in
every year, but the share of them coded generic "Other Hispanic" (HISP 24) runs 2.5% (2019),
24.7% (2021), 29.8% (2023), 5.4% (2024); in households it stays 1.1–1.4%. Among native Hispanic
institutional adults the HISP 24 share is 13.9%, 26.5%, 25.2%, 18.6% (households 4.8–5.9%).
[CALCULATION: `acs_mexborn_inst_hisp.py`, `acs_hisp24_series.py` → `derived/acs_mexborn_inst_hisp.csv`,
`acs_hisp24_series.csv`] So any raw HISP=02 institutional count from ACS 2021–2023, or from the
2020–2024 5-year file, understates Mexican-coded custody by about a quarter; the raw 5-year
justice key (0.1150 vs 0.1264 1-year) is this swing. Prior coverage: the repo already reallocates
the generic excess for the Mexican cell (justice lane central, incarceration memo §2, crime.md
3b) and cites Glassman 2025 on synthetic GQ records; the 2024 1-year file the main case uses is
the cleanest post-2019 year. What was not shown before: the swing is institution-specific and
year-specific (a GQ processing regime, not self-identification), and birthplace proves the
generic-coded records include Mexico-born people. Grade A in the raw file; on the main case the
central is already adjusted (the raw arm would be −$1.9bn). Sign: raw coding flatters the group.

**F5. The memo's "Central Americans at or below native whites" reading rests on raw Hispanic
cells.** `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md` (§ 5-year
table, line 111) reads Salvadorans 0.67×, Guatemalans 0.83×, Dominicans 0.87× native NH whites
from the 2020–2024 5-year file and calls the "at or below native whites" reading "no longer a
small-cell result". The table is raw for every origin, so the between-origin ordering is fair, but
the white cell is untouched by Hispanic coding while every Hispanic cell loses its share of the
generic-coded inmates (F4); elsewhere the memo and ladder 65 quote the Mexican cell coding-adjusted
(2.1×). Pooling 1-year 2021–2024 (native men 18–39; reproduces the 5-year raw ratios within
small-cell noise: Mexican 1.69 vs 1.68, Salvadoran 0.69 vs 0.67, Honduran 1.13 vs 1.15) and
spreading the HISP 24 excess over named origins by institutional share:

| Origin | Raw 2021–24 | Generic excess spread | 2019 raw / spread |
|---|---:|---:|---:|
| Mexican | 1.69 | 2.13 | 1.91 / 2.10 |
| Salvadoran | 0.69 | 0.88 | 1.19 / 1.31 |
| Guatemalan | 0.99 | 1.26 | 1.22 / 1.35 |
| Dominican | 1.02 | 1.30 | 1.80 / 1.98 |
| Honduran | 1.13 | 1.43 | 1.68 / 1.86 |
| Puerto Rican | 1.62 | 2.04 | 2.25 / 2.48 |

[CALCULATION: `acs_origin_inst_recode.py` → `derived/acs_origin_inst_recode.csv`] The ordering
(Mexican above the Central Americans) holds under either coding; "Guatemalans and Dominicans at or
below whites" does not survive the correction the memo applies to the Mexican cell (0.99–1.26 and
1.02–1.30 across the two codings), and Salvadorans move to 0.69–0.88. Quoting the adjusted Mexican
2.1× beside raw comparators overstates the Mexican/Central American contrast by about 25–30%.
Spreading by institutional share is one assumption; giving the whole excess to Mexicans would leave
the comparators raw, so the ranges above are the bounds. Grade B, measured. Sign: raw comparators
make the other Latin American origins look better, so the Mexican cell looks relatively worse
(no effect on the $ account).

**F6. The 2020 "no schooling" break is a reshuffle below high school, it hits Central Americans
too, and it leaves natives alone.** Fixed Mexico-born population (arrived 1975–2009 at 20+, aged
25+, households, education reported): "no schooling completed" 8.2% (2017), 8.5%, 9.2% (2019),
then 13.6% (2021), 13.6%, 13.9%, 14.6% (2024). Grades 1–6 fall from 27.8% to 23.4–24.5%. The
less-than-high-school share stays 61–62% in every year, and mean years of schooling drop by about
0.25 (8.74 → 8.47–8.56). The same jump appears among the Central American-born 25+ (7.5–7.9% →
11.0–11.5%) and in both English-ability groups of the Mexico-born (+4.3 and +4.4 points); natives
65+ stay at 0.8–0.9%. [CALCULATION: `acs_break_probe.py`, `acs_break_lths.py` →
`derived/acs_noschool_break.csv`, `acs_break_lths.csv`] Cause not identified (no mode variable
in PUMS; the questionnaire item did not change to our knowledge) [UNVERIFIED]. Effect: none on
any category at or above the high-school line (the account and ledger use CPS education, and ACS
lanes use < HS / HS / college bins); years-of-schooling and rank measures from ACS 2020+ read
Latin American immigrants about 0.25 years too low. Ladder 197 already prices it; any cross-year
ACS comparison of years of schooling across 2019/2020, or a post-2020 comparison between Latin
American and other immigrants, inherits it. Grade B (real, measured, already priced where used).
Sign: makes the group look worse in 2020+ files.

**F7. The 2020 race coding change moves 5m native non-Hispanic whites out of "white alone".**
Native non-Hispanic white alone: 189.0m (2019), 185.1m (2021), 183.6m (2024); white in combination
with another race: 6.9m → 12.0m → 13.0m. The movers are young (mean age 29 vs 43) and slightly
less educated (BA+ 39.5% vs 43.0% at 25–64, 2024); their institutional rate at 18–64 is 1.25% vs
0.73%, mostly an age effect. [CALCULATION: `acs_school_race.py` → `derived/acs_race_{2019,2021,2023,2024}.csv`]
Prior coverage: `acs_institutional_2026_09_16/white_denominator_sensitivity.py` shows the
white-alone vs alone-or-in-combination choice moves the custody ratio by 3% in both 2019 and 2023.
Effect on the ledger's institutional add for native NH white (RAC1P=1): white-alone lowers the
white institutional rate by about 5% (crude), about $20 per white person at 18–64 against a
per-person gap of about −$5,400: <0.5%. Grade D, measured. Sign: slightly hurts the group
(reference looks better). The CPS race coding that defines the ledger's white G3+ is `cps.md`'s.

**F8. School attendance is allocated for one child in six, slightly more for Mexican-origin
children.** Children 5–17 in households, ACS 2024: SCH allocated for 17.6% of HISP=02 children
and 15.7% of native NH white children (2019 white: 10.6%, so allocation rose after 2020).
Allocated Mexican-origin children are 1.7 points less often public K–12 (86.8% vs 88.5%) and more
often private or home school (8.7% vs 6.3%); the white gap is 0.9 points. Net effect on the
Mexican-origin public share: 88.2% vs 88.5% reported-only (−0.3 points, −0.34%). ACS public K–12
pupils of all ages, 47.1m, is within 2% of CPS October's 47.95m and NCES fall enrollment.
[CALCULATION: `acs_school_race.py`, `acs_sch_alloc.py` → `derived/acs_school_*.csv`, `acs_sch_alloc.csv`]
Effect: the generation split's ACS pupil ratio for Mexican-origin households (0.905) is about 0.3%
low: ≈ $0.5bn on a K–12 charge of about $152bn (8.63m pupils × $17,619) [CALCULATION]; the main case
uses CPS October and is untouched. Grade D, measured. Sign: flatters the group. Note: ACS SCH=3
is "private school, private college, or home school", so ACS "private" includes home schooling.

**F9. Code-level checks: ADJINC, top-codes, sentinels, PUMA vintages, 2020 weights.**
- ADJINC is one constant per 1-year file (1.019518 in 2023, 1.015250 in 2024) [DATA: held
  PUMS]. Scripts that omit it (`high_skill_origin_screen_2026_09_21/acs_screen.py` and
  `admission_route_2026_09_21/acs_outcomes.py` income ≥ $100k thresholds,
  `arrival_cohorts_2026_09_18/acs_cohorts.py` log wages, `displacement_transfers_2026_09_18/pull_pums.py`)
  are 1.5–2% off in dollar level only; group ratios within a year are unaffected. Grade D.
- Top-codes: WAGP maximum $907,000 (2024), 0.05% of records at the state top-code, replaced by
  state means above the threshold, so means are preserved; Mexican-origin exposure is negligible.
  Grade D, no effect.
- IPUMS sentinels: every script that reads INCTOT/INCWAGE and computes a statistic excludes
  9999999/9999998 or 999999/999998 (`build_borjas_supply_shock_panel.py`,
  `projection_backtest_2026_09_19/cohorts.py`, `ancestry_iv_congestion_wages_2026_09_23/build_pums.py`,
  `scale_spillovers_2026_09_23/sample_weights.py`, `arrival_cohorts` scripts); the remaining hits
  are extract requests or the store organiser. Not found.
- PUMA vintages: lanes that pool across 2021/2022 switch crosswalks by year
  (`labor_mobility_insurance_2026_09_23/metro_panel.py` 2000/2010/2020 PUMAs, Connecticut
  planning regions mapped); the congestion lane uses 2024 only with the puma22 crosswalk. The
  Connecticut CBSA crosswalk is `ct-xwalk`'s. Not found.
- ACS 2020 experimental weights: no headline input uses the 2020 1-year file (IPUMS extract 5
  excludes 2020; the schooling lane shows it as one spec). The 2020–2024 5-year custody key is a
  sensitivity arm only and its problem is F4, not the weights. Grade D.

**F10. Found 2026-09-23, fixed (7a44b69): 1990/2000 "institutional" is not correctional.** The
1990 and 2000 5% census files code every institutional record only as "institution" (IPUMS
GQTYPED 100), while the repo described Rumbaut's 2000 figures as correctional-only. Consequence:
the 2000 figures and the ACS series share one universe (all institutions); what breaks the
2000-to-ACS comparison is the 2000 birthplace allocation (ladder 196) and ICE detention, not
institution type. Corrected in FAQ 12 and
`research/immigration-mexican-origin-generation-incarceration-2026-09-16.md`. Sign: the old label
made the 2000 baseline look like a narrower (correctional) universe than the ACS rates it was
compared with; the corrected comparison is like-for-like on universe. Not re-derived here.
Residual wording found by a search of `research/` for 1980–2000 census "incarcerated/prison/
correctional" outside institution language: `immigration-crime-statistics-bias-mechanisms-2026-09-16.md`
line 25 ("Rumbaut 2007 ... (4.55% incarcerated)", Rumbaut's label carried as ours) and ladder 66,
which calls the 2000 and 2023 institutional rates a "native crime benchmark" (same universe in both
years, so the comparison holds; the word "crime" is the author's gloss). The other hits are external
studies' own proxies (Borjas–Grogger–Hanson, Butcher–Piehl, Moehling–Piehl). No other repo number
treats 1990/2000 institutional residence as incarceration. Grade D, measured (search).

**F11. Census 1980–2000 allocation in institutions, from the IPUMS store's `usa_00004_q` view**
(men 18–40; any nonzero Q code). [CALCULATION: `acs_census_qflags.py` → `derived/acs_census_qflags.csv`]

| Institutional men 18–40 | Birthplace 1980 / 1990 / 2000 | Education 1980 / 1990 / 2000 |
|---|---|---|
| US-born Mexican-origin (HISPAN) | 20.8% / 28.8% / 76.2% | 28.9% / 21.5% / 74.7% |
| Native NH white | 20.7% / 23.3% / 51.4% | 25.8% / 19.4% / 50.9% |
| Mexico-born | 0% / 0% / 7.9% | 11.4% / 8.2% / 32.8% |

Household rates are 1–11% for birthplace and 4–14% for education. The group-vs-reference gap in
2000 is +25 points on both items (birthplace: ladder 196's defect, covered by the crime-selection
lane). New here is education. In 1990 and 2000, allocated inmates' education looks like reported
inmates' (2000, ages 25–40: less than high school 30% allocated vs 27% reported for whites, 42% vs
41% for Mexican-origin), so donors were institutional and the education cells are usable. In 1980
it does not: allocated white inmates have 28% below high school and 18% BA+ against 55% and 3% for
reported ones, a household-like donor pattern (US-born Mexican-origin: 57% vs 64% below high
school). [CALCULATION: same view, `EDUC` by `QEDUC`] Effect: the 1980 "age × education held" rows of the
crime-selection lane's mover comparison (§3a, +0.16 all US-born, +0.12 NH white, +0.07 Hispanic)
place about a quarter of white inmates in education cells that are too high, which inflates
institutional rates in the higher cells. Direction on the mover gap is not determined without the
re-run; the age-only rows are unaffected. Grade C, real, effect on the 1980 education-held row
unmeasured. The ACS analogue is F1 plus FSCHLP 17–24% for institutional residents in 2024
(`derived/acs_alloc_rates_2024.csv`), which `institutional_education_2026_09_19`'s education ×
origin institutional stocks inherit (allocation flags not used there).

## Defect table

| File | Item | Check | Finding | Grade | Effect on a repo number | Status |
|---|---|---|---|---|---|---|
| ACS PUMS 2021–2023 1-yr, 2020–24 5-yr | HISP in institutional GQ | categories, year jumps | Generic "Other Hispanic" absorbs 25–30% of Mexico-born and ~25% of native Hispanic inmates; 2024 near 2019 levels (F4) | A (raw) | Main case: none (2024 file, reallocated central); raw arm −$1.9bn; ledger item N short ~$1.8bn (crime.md) | measured |
| Incarceration memo 5-yr origin table | Comparator coding | double standard | Central American/Dominican cells raw vs whites; Mexican quoted adjusted (F5) | B | Guatemalan 0.83→0.99–1.26×, Dominican 0.87→1.02–1.30×, Salvadoran 0.67→0.69–0.88× | measured |
| ACS PUMS 2020+ | SCHL for Latin American-born | year jumps | "No schooling" +4.4 pts, −0.25 mean years; < HS unchanged (F6) | B | Ladder 197 (priced); none on account | measured |
| ACS PUMS 2023–24 | PERNP allocation | allocation, donor rule | 35% Mexico-born vs 20% white allocated; allocation lifts Mexico-born/white ratio 0.572→0.589 (F3) | C | ACS earnings/tax cross-checks ~3% favourable; account uses CPS | measured |
| ACS PUMS 2023–24 | POBP in institutional GQ | allocation | 8–10% allocated; 22% vs 27% foreign-born among allocated vs reported (F2; confirms crime.md) | C | ~$0.08bn between nativity columns of the justice key; total unchanged | measured |
| ACS PUMS GQ records | whole-person GQ imputation | imputation | ~half of GQ PUMS records are unflagged donor copies (F1) | C | No sign bias; record-count SEs too small by ~√2 | source-documented |
| ACS PUMS 2019→2021+ | RAC1P white alone | categories | 5m natives move from white alone to multiracial white (F7) | D | <0.5% of the ledger per-person gap; 3% on custody ratios (prior) | measured |
| ACS PUMS 2024 | SCH allocation, children | allocation | 17.6% vs 15.7% allocated; allocated Mexican children less public (F8) | D | Generation-split K–12 charge ~$0.5bn low; main case uses CPS October | measured |
| Census 1990/2000 5% files | GQ type | categories | "institution" only; repo called 2000 "correctional" (F10) | — | found 2026-09-23, fixed 7a44b69; residual wording in bias-mechanisms memo line 25 | fixed |
| IPUMS census 1980 | QEDUC in institutions | allocation, donor rule | 26–29% of inmates allocated with household-like education (F11) | C | 1980 education-held mover rows; unmeasured | real, unmeasured |
| Lane scripts | ADJINC | units | omitted in 4 scripts; constant per file (F9) | D | 1.5–2% level only | measured |
| ACS PUMS | WAGP/PINCP top-codes | top-codes | 0.05% of records; mean-preserving (F9) | D | none | measured |
| IPUMS scripts | INCTOT/INCWAGE sentinels | sentinels | all computing scripts exclude them (F9) | — | none | not found |
| PUMA-pooling scripts | PUMA vintage | vintage | vintage-specific crosswalks used (F9) | — | none | not found |

## What prior audits covered

- **Institutional birthplace and Hispanic coding:** the justice lane's reallocation and FHISP
  check (`cj_use_allocation_2026_09_23/RESULT.md`), the incarceration memo's coding adjustment and
  white-denominator sensitivity, Glassman 2025 on synthetic GQ records (ladder 65), and `crime.md`
  items 2–3b (the ACS 2024 birthplace flags and the ledger item N correction). F2 confirms their
  numbers independently; F4 adds the year-by-year swing and the birthplace proof; F5 is new.
- **1990/2000 institution type:** fixed in 7a44b69 (F10).
- **Census 1980–2000 birthplace allocation** (QBPL, QCITIZEN, QYRIMM):
  `crime_selection_cohorts_2026_09_23/RESULT.md` §2b and ladder 196. Not redone.
- **ACS year-of-entry allocation for institutional Mexico-born men** (28–82% in 2021–24): same
  lane, "Allocation in the ACS". My 2023/2024 rates (54.5%, 35.5% at 18–64) agree.
- **2020 schooling break and QEDUC allocation:** `schooling_selection_position_2026_09_23` §3b–3c.
  F6 adds the Central American and native controls and the unchanged < HS share.
- **CPS vs ACS origin totals:** `cps.md` (`derived/cps_vs_acs_origin.csv`).

## Not checked, and why

- **QHISPAN in the 1980–2000 censuses.** No held IPUMS extract carries it; the census-era
  Mexican-origin denominators and Rumbaut's 2000 ratio rest on unflagged HISPAN in institutions,
  where the 2020 census had facilities fail to report Hispanic status for over a quarter of
  residents (memo, measurement check 3, Prison Gerrymandering Project 2024). Real but unmeasured; needs an IPUMS extract with QHISPAN for GQ records.
- **Housing-unit file items** (rent, value, FRNTP/FVALP) behind the housing-transfer and
  construction lanes, and **commute items** (FJWMNP, FJWTRNSP) behind the congestion lane. These
  are social items beside the headline; they were not extracted in this pass.
- **ACS 2023 published state medians** (B25103, B25077, B25064) in the generation split's
  property-tax and rent parameters: published tables, not audited against microdata.
- **ACS 2020 1-year microdata.** Not held locally; nothing headline-bearing uses it.
- **Cause of the 2020 schooling break.** PUMS has no response-mode variable.
- **Earnings donor rule.** The inference that ACS earnings donors are not matched on nativity rests
  on the allocated-vs-reported pattern, not on Census's edit specifications.

## Scripts and outputs

`acs_extract.py` (slim parquet of held 1-year PUMS 2017–2019, 2021–2024 in `_cache/`),
`acs_alloc.py`, `acs_earn_alloc.py`, `acs_school_race.py`, `acs_sch_alloc.py`,
`acs_break_probe.py`, `acs_break_lths.py`, `acs_hisp24_series.py`, `acs_mexborn_inst_hisp.py`,
`acs_origin_inst_recode.py`, `acs_census_qflags.py` (reads the IPUMS store view) → `derived/acs_*.csv`. Run each as
`OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow python3 <script> <years>`
from the repository root.

Model self-report: `claude-opus-5-5[1m]`
