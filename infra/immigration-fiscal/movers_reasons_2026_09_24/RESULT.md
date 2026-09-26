**Verdict:** US-born adults who leave California almost never give "wanted better neighborhood/less crime" as their main reason: 1.47% (SE 0.25) of them in ASEC 2005–2025. That is about 4,200 people a year at the CPS level and 3,600–7,000 at the ACS level, or 0.2–0.3 per 1,000 US-born adults living in California. The share is slightly below the 1.90% (0.12) among other states' leavers. They leave for jobs (38%), family (27%) and housing (19%). Housing is the California-specific reason: leavers cite cheaper housing 2.2 times as often as other states' leavers, and housing reasons more often in every race, education, income and age group, Mexican-origin leavers included. Across origin states the neighborhood/crime share falls, not rises, as the origin's Mexican-origin share rises: −0.28 to −0.36 pp per 10 pp (t −2.8 to −3.6), a descriptive result, and the within-state change cannot be estimated precisely. California-to-Texas filers had lower AGI per return than California stayers in the 2011–12 to 2018–19 pairs (0.82–0.96 times), higher AGI in 2019–20 to 2021–22 (1.04–1.32 times) and lower again in 2022–23 (0.93). Each year's net cohort takes $0.13–0.22bn of California state and local tax to Texas, where $0.06–0.17bn is collected: a transfer between states, gross of the spending that moves with the people. The neighborhood/crime leavers' moving costs total $11–89M a year. That is an upper bound for moves whose stated main reason is ethnic composition, not for every move composition may influence. [FRAMING-SENSITIVE]

Model: claude-opus-5-5[1m] (lane worker, 2026-09-24/25). Two literature subagents on the same model wrote `lit/`.

## What was asked and what the data can say

The operator asked whether Californians leave "a failed state with 32% hispanics that is rotten", and about moves from California to Austin. This lane measures what movers say and where they go. The CPS asks each mover for one main reason for moving. The Census labels the answer "Wanted better neighborhood" (code 11, 2019 file) and "wanted better neighborhood/less crime" (code 12, 2025 file), and IPUMS codes both as WHYMOVE 11 [SOURCE: https://api.census.gov/data/2019/cps/asec/mar/variables/NXTRES.json and …/2025/…; cached `_cache/census_meta/`]. The category mixes crime, schools, disorder and neighbors, and has no separate answer for composition. The lane does not price preferences over neighbors' ethnicity; that is the operator's call. [FRAMING-SENSITIVE]

Rebuild instructions are in [README.md](README.md). A full re-run from the cached inputs on 2026-09-25 reproduced every tracked output byte for byte, apart from the files this session changed on purpose. [CALCULATION: scratchpad hash diff of `derived/`]

## Gates

| Gate | Test | Result |
|---|---|---|
| G1 | IPUMS codebook (DDI) against the data | **Pass.** Codebook variables equal the CSV header: 35 in extract 2 and 178 in extract 3. The main extract has 5,027,101 rows. For the 16 samples whose counts IPUMS publishes, rows per sample, every MIGRATE1 count (96 year-code cells) and every WHYMOVE count (322 cells) equal the published figures. The replicate-weight extract equals the main extract's interstate movers for 2005–2025: 59,734 rows, all joined, weights identical. [DATA: `derived/gate_extract.csv`] |
| G2a | IPUMS coding against the Census public ASEC files | **Pass.** Records and reason codes are identical in 18 year-by-group comparisons (2014 3/8 file, 2015, 2019–2025), after both Census NXTRES schemes are mapped onto WHYMOVE. Weighted shares differ by at most 0.556 pp, and only in 2020–21, where the two files carry different weight vintages. [DATA: `derived/gate_census_check.csv`] |
| G2b | National interstate movers against Census CPS Table A-1 | **Pass** in all 25 published years, 1999–2023: within 0.3% in every year and within 0.012% in 23 of them (2004 differs by 0.28%, 2014 by 0.12%). [DATA: `derived/gate_movers_count.csv`; SOURCE: census.gov `hst_mig_a_1.xlsx`] |
| G2c | California out-movers against the published ACS state-to-state tables | **Fails as a level check.** The CPS is within the combined margin in 2 of 12 years. Quoted year: ASEC 2024 (moves in 2023–24) gives 430,050 CPS leavers (SE 61,408). The ACS gives 661,205 (MOE 21,844) for 2024, as published ("Out-Movers Estimate", `tool_input` sheet), and 690,127 (MOE 23,379) for 2023, summed from the 2023 table's California column with the MOE by root sum of squares; their mean is 675,666. The CPS finds 0.62–0.87 of the ACS level for California and 0.57–0.72 nationally. The shortfall belongs to the survey, not to California or to IPUMS coding, since G2a and G2b pass. The lane therefore takes shares from the CPS and levels from the ACS. [SOURCE: https://www2.census.gov/programs-surveys/demo/tables/geographic-mobility/2024/state-to-state-migration/State_to_State_Migration_Table_2024_T13.xlsx; DATA: `derived/gate_movers_count.csv`] |
| G3 | IRS SOI California outflows against the published state file | **Pass.** In all 12 tax-year pairs, 2011–12 to 2022–23: California's outflow row to Texas equals Texas's inflow row from California; destination rows sum to "Total Migration-US"; the other states' inflow files sum to the same total; no cell is suppressed. All 56 California rows of the 2022–23 outflow CSV equal the "State Outflow" sheet of the published workbook `2223ca.xlsx`: Total Migration-US 353,260 returns, 590,247 individuals, $36,074,839 thousand AGI; Texas 44,417 / 82,481 / $4,764,727 thousand. [SOURCE: https://www.irs.gov/pub/irs-soi/2223ca.xlsx; DATA: `derived/gate_irs.csv`] |
| G4 | Every computed specification appears here | Each table below names its specification. Where only some outcome columns are shown, the rest are in the named CSV. |

## Question 1: why US-born adults leave California

Population: US-born adults (18+) whose residence a year earlier was California and who now live in another state. Standard errors use the 160 successive-difference replicate weights from 2005. For 1999–2004, which has no replicate weights, a household-cluster variance is scaled by a design factor of 1.047: the median ratio of replicate to cluster standard errors over seven reason shares in 2005–2025. [DATA: `derived/design_factor.json`]

**Main reasons, pooled** (% of leavers, SE in pp) [DATA: `derived/reasons_ca_leavers.csv`]

| Reason group (WHYMOVE codes) | 2005–2025 | 1999–2025 | 1999–2004 |
|---|---|---|---|
| Jobs (4, 5, 6, 8) | 38.11 (1.29) | 37.68 (1.10) | 36.38 (2.07) |
| Family (1, 2, 3, 20) | 27.22 (1.26) | 27.36 (1.05) | 27.77 (1.83) |
| Housing (9, 10, 12, 13, 19) | 18.98 (1.19) | 18.97 (0.99) | 18.94 (1.74) |
| — cheaper housing (12) | 7.73 (0.79) | 7.07 (0.65) | 5.05 (1.03) |
| — new or better housing (10) | 3.18 (0.48) | 3.77 (0.43) | 5.56 (0.93) |
| — own home (9) | 2.44 (0.43) | 2.74 (0.39) | 3.62 (0.86) |
| Other (14, 16, 17, 18) | 11.02 (0.84) | 11.20 (0.72) | 11.76 (1.37) |
| Retirement (7) | 2.29 (0.29) | 2.16 (0.26) | 1.78 (0.55) |
| **Better neighborhood/less crime (11)** | **1.47 (0.25)** | **1.62 (0.24)** | **2.08 (0.59)** |
| Climate (15) | 0.90 (0.20) | 1.00 (0.19) | 1.28 (0.46) |
| Sample (persons) | 3,586 | 5,092 | 1,506 |
| Leavers a year, CPS level | 286,526 | 296,571 | 331,730 |

Variants of the 2005–2025 neighborhood/crime share:
- Excluding ASEC 2012–2015 (the code anomaly below): 1.58 (0.29), n = 2,875.
- Excluding records whose migration status or origin state was allocated: 1.52 (0.28), n = 2,901.
- Housing in the same two variants: 17.94 (1.41) and 17.06 (1.25).
- Jobs: 36.34 (1.56) and 40.36 (1.32).
- Every other reason in both variants is in the CSV.

Detailed codes, 2005–2025 (%):

| Code | Share | Code | Share |
|---|---|---|---|
| 01 marital status | 3.90 | 11 better neighborhood/less crime | 1.47 |
| 02 establish own household | 4.24 | 12 cheaper housing | 7.73 |
| 03 other family | 18.05 | 13 other housing | 5.53 |
| 20 unmarried partner | 1.03 | 19 foreclosure or eviction | 0.10 |
| 04 new job or transfer | 27.93 | 14 college | 4.85 |
| 05 look for work or lost job | 4.97 | 15 climate | 0.90 |
| 06 easier commute | 1.93 | 16 health | 1.71 |
| 08 other job-related | 3.29 | 17 other | 4.44 |
| 07 retired | 2.29 | 18 natural disaster | 0.03 |
| 09 own home | 2.44 | 10 new or better housing | 3.18 |

**Against other states' leavers and movers into Texas, 2005–2025** (% (SE)) [DATA: `derived/reasons_compare.csv`]

| US-born adult group | n | Neighborhood/crime | Housing | Cheaper housing | Jobs | Family | Climate |
|---|---|---|---|---|---|---|---|
| California leavers | 3,586 | 1.47 (0.25) | 18.98 (1.19) | 7.73 (0.79) | 38.11 (1.29) | 27.22 (1.26) | 0.90 (0.20) |
| Leavers of all other states | 33,434 | 1.90 (0.12) | 14.70 (0.32) | 3.51 (0.17) | 40.41 (0.47) | 26.37 (0.39) | 2.39 (0.15) |
| New York leavers | 1,725 | 2.47 (0.66) | 19.63 (1.63) | 6.87 (1.01) | 36.71 (1.82) | 22.47 (1.64) | 2.94 (0.62) |
| Illinois leavers | 1,143 | 2.94 (0.68) | 15.21 (1.74) | 4.04 (1.00) | 40.57 (2.18) | 23.81 (1.74) | 3.20 (0.90) |
| New Jersey leavers | 718 | 1.53 (0.73) | 17.74 (2.38) | 4.72 (1.21) | 36.29 (3.04) | 27.86 (2.67) | 4.01 (1.50) |
| Massachusetts leavers | 1,071 | 2.10 (0.71) | 16.35 (1.83) | 3.92 (1.02) | 36.89 (2.38) | 25.85 (2.81) | 3.62 (1.13) |
| Washington leavers | 1,156 | 1.93 (0.75) | 11.92 (1.66) | 3.63 (1.06) | 44.22 (2.43) | 27.45 (1.98) | 1.87 (0.60) |
| Texas leavers | 2,184 | 1.23 (0.39) | 13.64 (1.41) | 2.99 (0.63) | 42.34 (1.80) | 27.72 (1.37) | 1.86 (0.55) |
| Florida leavers | 1,922 | 1.93 (0.47) | 14.71 (1.31) | 5.12 (0.82) | 34.20 (1.73) | 30.04 (1.59) | 2.01 (0.45) |
| Arizona leavers | 1,003 | 2.06 (0.72) | 13.31 (1.65) | 2.54 (0.66) | 33.34 (2.51) | 35.50 (2.69) | 3.12 (0.87) |
| Nevada leavers | 522 | 1.07 (0.58) | 15.22 (2.64) | 3.75 (1.25) | 40.02 (4.18) | 32.25 (4.14) | 0.22 (0.16) |
| New Mexico leavers | 336 | 0.00 (none cited) | 15.76 (3.59) | 3.01 (1.15) | 34.62 (4.67) | 29.87 (4.38) | 3.19 (1.26) |
| Movers into Texas, all origins | 1,504 | 2.02 (0.47) | 13.37 (1.26) | 3.29 (0.63) | 44.58 (1.95) | 25.70 (1.51) | 2.31 (0.56) |
| Movers into Texas from outside California | 1,312 | 2.14 (0.52) | 13.02 (1.37) | 2.61 (0.63) | 45.04 (2.18) | 25.17 (1.64) | 2.32 (0.59) |
| California to Texas | 192 | 1.11 (0.87) | 15.92 (3.51) | 8.27 (2.45) | 41.26 (4.35) | 29.52 (4.86) | 2.26 (1.44) |
| California to other states | 3,394 | 1.51 (0.28) | 19.30 (1.26) | 7.68 (0.82) | 37.79 (1.41) | 26.99 (1.27) | 0.76 (0.16) |

California minus each group, in pp with SE computed jointly from the replicates:

| California minus | Neighborhood/crime | Housing | Cheaper housing | Jobs | Climate |
|---|---|---|---|---|---|
| All other states | −0.43 (0.26) | +4.28 (1.24) | +4.22 (0.83) | −2.30 (1.34) | −1.49 (0.24) |
| New York | −0.99 (0.71) | −0.64 (2.09) | +0.86 (1.32) | +1.40 (2.24) | −2.04 (0.65) |
| Illinois | −1.47 (0.72) | +3.77 (2.06) | +3.69 (1.24) | −2.46 (2.46) | −2.30 (0.92) |
| New Jersey | −0.05 (0.79) | +1.24 (2.75) | +3.01 (1.47) | +1.82 (3.37) | −3.11 (1.47) |
| Massachusetts | −0.63 (0.73) | +2.63 (2.11) | +3.82 (1.30) | +1.22 (2.72) | −2.71 (1.14) |
| Washington | −0.45 (0.78) | +7.06 (2.05) | +4.11 (1.21) | −6.11 (2.61) | −0.97 (0.62) |
| Texas | +0.24 (0.44) | +5.34 (1.83) | +4.74 (1.00) | −4.22 (2.03) | −0.96 (0.58) |
| Florida | −0.46 (0.53) | +4.27 (1.77) | +2.61 (1.12) | +3.91 (2.25) | −1.11 (0.48) |
| Arizona | −0.59 (0.77) | +5.67 (1.99) | +5.19 (0.98) | +4.77 (2.95) | −2.22 (0.88) |
| Nevada | +0.41 (0.63) | +3.77 (2.90) | +3.98 (1.52) | −1.90 (4.33) | +0.68 (0.24) |
| New Mexico | +1.47 (0.25; no NM case, SE understated) | +3.22 (3.78) | +4.72 (1.41) | +3.49 (4.87) | −2.29 (1.27) |
| Movers into Texas, all origins | −0.55 (0.49) | +5.61 (1.67) | +4.44 (0.95) | −6.47 (2.27) | −1.41 (0.54) |
| Movers into Texas, not from California | −0.67 (0.54) | +5.96 (1.83) | +5.13 (1.04) | −6.93 (2.51) | −1.41 (0.62) |

The pooled 1999–2025 comparison tells the same story. California leavers cite neighborhood/crime at 1.62%, against 1.98% for all other states (difference −0.36, SE 0.25), 3.32% for New York (−1.69, SE 0.64) and 2.51% for Illinois. They cite housing at 18.97% against 16.53% (+2.45, SE 1.03) and cheaper housing at 7.07% against 3.35% (+3.71, SE 0.67). Every group's 1999–2025 row is in the CSV.

**By period** (% (SE); CA = US-born adult California leavers, others = leavers of all other states) [DATA: `derived/reasons_ca_by_year.csv`]

| ASEC years | CA n | CA neighborhood/crime | Others | CA housing | Others | CA cheaper housing | Others |
|---|---|---|---|---|---|---|---|
| 1999–2005 | 1,788 | 2.40 (0.60) | 2.12 (0.16) | 19.00 (1.56) | 20.36 (0.49) | 5.22 (0.94) | 3.01 (0.20) |
| 2006–2011 | 1,090 | 1.39 (0.43) | 2.16 (0.24) | 14.48 (1.79) | 10.12 (0.48) | 7.29 (1.13) | 2.79 (0.24) |
| 2012–2015 | 711 | 1.02 (0.39) | 1.40 (0.21) | 23.36 (2.18) | 20.74 (0.81) | 3.83 (0.93) | 3.40 (0.48) |
| 2016–2019 | 660 | 1.00 (0.49) | 1.11 (0.18) | 16.00 (2.17) | 13.33 (0.72) | 6.04 (1.35) | 3.20 (0.37) |
| 2020–2025 | 843 | 1.62 (0.48) | 2.56 (0.29) | 22.00 (2.72) | 15.03 (0.73) | 12.03 (1.94) | 4.72 (0.42) |

Jobs, family, climate and the other groups by period are in the CSV.

Single years for California. The neighborhood/crime share is shown with its SE; the second number in each cell is the cheaper-housing share. Years with no neighborhood case have no usable SE.

| ASEC | Neighborhood (SE), cheaper housing | ASEC | Neighborhood (SE), cheaper housing | ASEC | Neighborhood (SE), cheaper housing |
|---|---|---|---|---|---|
| 1999 | 3.44 (1.95), 5.43 | 2008 | 2.27 (1.67), 7.50 | 2017 | 0.00, 6.62 |
| 2000 | 4.81 (2.58), 4.15 | 2009 | 3.00 (1.91), 6.03 | 2018 | 1.71 (1.52), 7.38 |
| 2001 | 1.93 (1.06), 6.26 | 2010 | 0.00, 7.16 | 2019 | 1.17 (0.69), 3.98 |
| 2002 | 0.51 (0.39), 3.95 | 2011 | 0.10 (0.10), 4.11 | 2020 | 1.22 (0.92), 15.00 |
| 2003 | 0.43 (0.28), 6.22 | 2012 | 1.46 (0.93), 7.45 | 2021 | 4.39 (1.97), 13.23 |
| 2004 | 1.39 (0.97), 4.22 | 2013 | 0.00, 2.08 | 2022 | 1.17 (0.91), 9.10 |
| 2005 | 4.20 (2.15), 6.21 | 2014 | 1.35 (0.94), 4.92 | 2023 | 0.74 (0.73), 17.08 |
| 2006 | 1.94 (1.20), 7.90 | 2015 | 1.12 (0.67), 1.45 | 2024 | 0.57 (0.57), 6.81 |
| 2007 | 0.95 (0.71), 11.51 | 2016 | 0.92 (0.92), 6.17 | 2025 | 1.27 (1.05), 9.58 |

Samples run from 82 (2025) to 315 (2004) leavers a year. Single years are noisy. The only neighborhood reading above 4% since 2006 is ASEC 2021 (moves in 2020–21), at 4.39 (SE 1.97). The per-year shares for every reason are in the CSV.

**By subgroup, 2005–2025, California against other states' leavers** (% (SE); differences in pp) [DATA: `derived/reasons_ca_by_subgroup.csv`]

| Subgroup | CA n | Neighborhood/crime, CA | Other states | Housing, CA − others | Cheaper housing, CA − others | Jobs, CA − others |
|---|---|---|---|---|---|---|
| Non-Hispanic white | 2,385 | 1.54 (0.32) | 1.70 (0.14) | +3.08 (1.29) | +3.81 (0.87) | −2.13 (1.55) |
| Hispanic, Mexican-origin | 408 | 1.97 (0.72) | 2.11 (0.57) | +6.15 (3.70) | +7.39 (2.82) | +1.22 (4.06) |
| Hispanic, other | 154 | 0.79 (0.56) | 1.69 (0.72) | +7.97 (5.49) | −0.39 (3.18) | +3.68 (5.93) |
| Non-Hispanic Black | 300 | 0.78 (0.57) | 3.38 (0.43) | +8.26 (4.22) | +6.73 (2.97) | −3.92 (4.58) |
| Non-Hispanic Asian or Pacific Islander | 159 | 0.91 (0.81) | 0.45 (0.25) | +6.21 (4.79) | −0.86 (1.83) | −13.14 (5.37) |
| Non-Hispanic other or multiple | 180 | 2.11 (1.55) | 1.55 (0.45) | +3.14 (3.47) | +4.63 (2.68) | −9.57 (6.25) |
| Less than high school | 208 | 4.05 (1.42) | 3.75 (0.55) | +4.36 (4.75) | +3.20 (2.79) | +5.87 (4.49) |
| High school | 884 | 1.55 (0.48) | 2.10 (0.21) | +2.43 (2.06) | +4.63 (1.51) | +1.48 (2.46) |
| Some college or associate | 1,185 | 1.41 (0.36) | 2.17 (0.22) | +6.37 (1.77) | +5.01 (1.26) | −3.36 (2.09) |
| Bachelor's or more | 1,309 | 1.12 (0.33) | 1.24 (0.13) | +3.98 (1.67) | +3.49 (0.97) | −5.44 (2.27) |
| Household income under $50k (2024$) | 963 | 1.30 (0.42) | 2.09 (0.19) | +4.70 (2.19) | +5.10 (1.45) | −0.32 (2.36) |
| $50k–100k | 1,019 | 1.82 (0.53) | 2.10 (0.24) | +2.29 (2.10) | +2.55 (1.37) | −2.82 (2.43) |
| $100k–150k | 624 | 1.88 (0.87) | 1.59 (0.25) | +4.60 (2.56) | +2.45 (1.37) | −4.56 (3.85) |
| $150k or more | 980 | 1.05 (0.39) | 1.67 (0.23) | +5.71 (2.66) | +6.23 (1.74) | −3.27 (3.19) |
| Age 18–34 | 1,798 | 1.15 (0.32) | 1.67 (0.14) | +4.18 (1.41) | +4.51 (1.04) | −3.17 (1.69) |
| 35–54 | 1,088 | 1.77 (0.47) | 2.30 (0.22) | +2.32 (1.94) | +2.79 (1.11) | −2.63 (2.41) |
| 55–64 | 377 | 2.27 (1.03) | 2.32 (0.36) | +6.68 (3.49) | +6.43 (2.05) | +0.83 (3.57) |
| 65+ | 323 | 1.50 (0.65) | 1.61 (0.32) | +6.99 (3.40) | +4.14 (1.94) | +5.83 (3.35) |

Family, climate and retirement by subgroup are in the CSV.

These rows test the claim directly. [2026-09-25: they test whether stated reasons differ by group. Reason shares among leavers cannot measure leaving rates among residents, and a composition effect working through housing costs or schools would be reported as housing or schools by both groups; see Revisions.] If California's white natives left to get away from Mexican-origin neighbors, white leavers should differ from Mexican-origin leavers. They do not. On neighborhood/crime, California minus other states is −0.17 (0.35) for non-Hispanic whites and −0.14 (0.89) for Mexican-origin US-born adults. The housing excess is larger for Mexican-origin leavers (+6.2) and Black leavers (+8.3) than for white leavers (+3.1). [INFERENCE]

**Income-weighted shares, ASEC 2005–2025.** Householders of any nativity are weighted by household income in 2024 dollars, to show where leavers' income goes. Shares in %. [DATA: `derived/income_weighted_shares.csv`]

| Householders | n | Mean household income | Neighborhood/crime | Housing | Jobs | Family |
|---|---|---|---|---|---|---|
| Leaving California | 2,134 | $108,916 | 2.30 (0.84) | 16.82 (1.56) | 45.88 (1.92) | 23.06 (1.80) |
| Moving into California | 909 | $120,828 | 0.85 (0.29) | 6.99 (0.90) | 61.07 (2.73) | 17.21 (1.80) |
| California to Texas | 137 | $108,010 | 1.29 (1.05) | 18.54 (4.33) | 51.58 (6.15) | 19.36 (5.78) |
| Texas to California | 67 | $100,307 | 0.11 (0.11) | 5.05 (2.93) | 63.96 (7.06) | 23.27 (6.49) |

Retirement, climate and other are in the CSV.

**Outside check against PPIC.** PPIC reports that adults who left California in the 2010s "cited jobs (49%), housing (23%), or family (20%) as the primary reason (according to the Current Population Survey)" [SOURCE: Hans Johnson, PPIC blog, 2021-05-06, https://www.ppic.org/blog/whos-leaving-california-and-whos-moving-in/, p. 3/3]. The same population here (adults of any nativity leaving California, ASEC 2011–2020, n = 2,055) gives jobs 45.99 (1.47), housing 19.15 (1.19), family 23.12 (1.50), neighborhood/crime 0.94 (0.26), other 7.72, retirement 2.35 and climate 0.73. ASEC 2010–2019 gives 45.12 / 18.55 / 24.19. With neighborhood counted as housing, as IPUMS groups it, housing is 20.1. PPIC does not define its grouping. Each of the three shares lands within 3–4 pp of PPIC's. [DATA: `derived/ppic_crosscheck.csv`]

**Census allocation flags**, from the public files IPUMS does not reproduce (US-born adult California leavers, 2019–2025, n = 1,018). The Census hot-deck matrix allocated the reason for 13.1% of leavers (weighted), and 8.7% took it from another household member. No leaver's supplement was wholly imputed. The neighborhood/crime share is 1.56% with allocated reasons and 1.80% without them (n = 867). By year the allocated share runs from 10.2% to 15.2%. [DATA: `derived/census_allocation_flags.csv`]

**Data traps found**
1. The 2014 ASEC contains two files (HFLAG 0, the 5/8 file, and HFLAG 1, the 3/8 file). Each is weighted to the full population, so pooling them counts 2014 twice. The 2014 weights are multiplied by each file's share of 2014 records, 0.6986 and 0.3014.
2. Weighted interstate movers fall from 7.35–8.43 million a year in ASEC 1999–2005 to 4.19–5.68 million in 2006–2025. The published Table A-1 shows the same break (G2b). Kaplan and Schulhofer-Wohl (2012, *Demography*) attribute it to the Census hot-deck imputation. [TRAINING-DATA; not read in this lane] The main window, 2005–2025, therefore contains one year from before the break, and the 1999–2004 shares are reported separately.
3. In ASEC 2012–2015 the college, climate, health and other codes (14–17) collapse. Unweighted counts of code 17 drop from 814 in 2011 to 183 in 2012, and code 13, "other housing", swells from 1,793 to 2,738. Code 11 stays smooth (732, 674, 616, 564, 585). The neighborhood/crime share is robust to dropping those years. Housing in 2012–2015 is inflated. [DATA: `derived/whymove_counts_by_year.csv`]

## Question 2: does the neighborhood/crime share track the Mexican-origin share where movers lived?

**What the data allow.** The CPS identifies an interstate mover's origin only to the state. IPUMS's ASEC migration group carries MIGRATE1, MIGSTA1, MIGRATE5, MIGSTA5, MIG5 variables, COUNTRY and WHYMOVE, with no county or metro of residence a year ago [SOURCE: https://cps.ipums.org/cps-action/variables/group/asec_mig, read 2026-09-24]. The Census public file carries only the previous state (MIG_ST). The brief's origin-county design is therefore not possible with public data. Two designs stand in for it.

- **Design A, origin state.** US-born adult interstate movers, ASEC 2006–2025: 33,951 persons in 51 origin states, clustered by state. Composition comes from the ACS 5-year release ending the year before the survey. Rent, home value and income controls come from the ACS 1-year release for the year before.
- **Design B, same county.** US-born adults who moved within their county, in the 368 counties the CPS identifies from its own code (COUNTYERR = 1): 51,016 persons, clustered by county. County composition and controls come from the ACS 5-year release.

Outcomes are 0/100 indicators, so coefficients are in pp. "per 10 pp" means per 10 percentage points of the Mexican-origin (or Hispanic) share of the population. All models are weighted linear probability models with year fixed effects. [DATA: `derived/q2_regressions.csv`, every term and control]

**Design A: origin state** (mean neighborhood/crime share 1.848%)

| Spec | Specification | Main term: coefficient, pp (SE) | t | n |
|---|---|---|---|---|
| A1 | Mexican-origin share, year FE | −0.283 (0.102) per 10 pp | −2.79 | 33,951 |
| A2 | + origin log rent, log home value, log income | −0.332 (0.107) | −3.11 | 33,951 |
| A3 | A2 + individual controls (log household income, sex) | −0.323 (0.113) | −2.86 | 33,951 |
| A4 | A3 + origin-state FE (change within a state) | +0.953 (2.523) | 0.38 | 33,951 |
| A5 | A3, non-Hispanic whites only | −0.138 (0.098) | −1.41 | 25,191 |
| A6 | A3, Hispanics only | −0.631 (0.440) | −1.44 | 2,982 |
| A7 | A3 with the Hispanic share instead | −0.390 (0.125) per 10 pp | −3.12 | 33,951 |
| A8 | A3 excluding allocated records | −0.363 (0.102) | −3.55 | 27,463 |
| A9 | A3 + California-origin indicator | −0.255 (0.155); California −0.523 (0.529) | −1.65 | 33,951 |
| A10 | A3 excluding California as origin | −0.253 (0.157) | −1.61 | 30,647 |
| A11 | Positive control: cheaper housing on A3's terms | log rent +4.017 (2.417); Mexican share +0.077 (0.217) | 1.66 | 33,951 |
| A12 | Placebo outcome: job reasons | Mexican share +0.619 (0.495) | 1.25 | 33,951 |
| A13 | Positive control: cheaper housing on origin log rent alone | +6.429 (1.513) | 4.25 | 33,951 |
| A14 | Positive control: climate on a cold-region origin | +2.045 (0.399) | 5.13 | 33,951 |

In A2–A3 the rent, value and income controls are individually insignificant; for example, A3 log rent is +0.027 (1.502). Neighborhood/crime share by band of the origin state's Mexican-origin share [DATA: `derived/q2_bins.csv`]:

| Origin Mexican-origin share | States | n | Neighborhood/crime % (SE) | Cheaper housing % (SE) |
|---|---|---|---|---|
| under 2% | 19 | 7,402 | 2.17 (0.27) | 3.23 (0.33) |
| 2–5% | 26 | 11,544 | 2.09 (0.22) | 3.96 (0.29) |
| 5–10% | 14 | 4,884 | 1.09 (0.24) | 2.79 (0.41) |
| 10–20% | 8 | 3,206 | 2.59 (0.44) | 4.51 (0.87) |
| 20% or more | 5 | 6,915 | 1.27 (0.19) | 5.25 (0.46) |

Selected origin states (neighborhood/crime %, SE, mean Mexican-origin share): California 1.31 (0.25), 31.5%; Texas 1.14 (0.40), 32.4%; Arizona 1.99 (0.73), 27.0%; Nevada 1.15 (0.62), 20.9%; New Mexico 0.00 (n = 297), 29.2%; Illinois 3.08 (0.73), 12.9%; New York 2.70 (0.72), 2.3%; Pennsylvania 4.73 (1.13), 1.1%. All 51 states are in `derived/q2_state_scatter.csv`.

Reading. Design A recovers both known drivers: cheaper housing rises with origin rent (t 4.3), and climate reasons rise from cold origins (t 5.1). It can therefore detect a real gradient. Leavers of high-Mexican-share states cite neighborhood/crime less often, not more. The gradient weakens and loses significance for whites alone (A5) and without California (A10). Within a state over time (A4) the interval runs from −4.0 to +5.9 pp per 10 pp, which is uninformative. This is a cross-state association that does not identify any causal effect. [INFERENCE]

**Design B: same-county movers** (mean share 4.400%)

| Spec | Specification | Main term: coefficient, pp (SE) | t | n |
|---|---|---|---|---|
| B1 | County Mexican-origin share, year and state FE | +0.246 (0.176) per 10 pp | 1.40 | 51,016 |
| B2 | + county log rent, log home value, log income | +0.149 (0.182) | 0.82 | 51,016 |
| B3 | B2 + individual controls | +0.155 (0.181) | 0.86 | 51,016 |
| B4 | B3 with county FE (change within a county) | +0.792 (2.253) | 0.35 | 51,016 |
| B5 | B3, non-Hispanic whites only | +0.434 (0.240) | 1.81 | 30,386 |
| B6 | B3, Hispanics only | +0.582 (0.253) | 2.30 | 8,471 |
| B7 | B3 with the Hispanic share instead | +0.135 (0.140) | 0.97 | 51,016 |
| B8 | B3, California counties only (31) | +0.482 (0.279) | 1.73 | 9,066 |
| B9 | Positive control: cheaper housing on B3's terms | log rent −0.197 (3.697); Mexican share −0.304 (0.332) | −0.05 | 51,016 |
| B10 | B3 without state FE | +0.164 (0.106) | 1.54 | 51,016 |
| B11 | Positive control: cheaper housing on county log rent alone | −0.500 (0.979) | −0.51 | 51,016 |

In B2–B3 county log income enters at −3.98 (1.17) and −3.86 (1.20). Same-county movers' neighborhood/crime share [DATA: `derived/q2_same_county_descriptive.csv`]:
- California counties 4.82% (0.39); Texas counties 4.57% (0.68); all other identified counties 4.27% (0.20).
- By county Mexican-origin share (all / non-Hispanic white): under 2%, 4.06 / 3.72; 2–5%, 4.35 / 4.27; 5–10%, 4.11 / 4.06; 10–20%, 3.13 / 1.93; 20% or more, 5.07 / 5.20.

Reading. Design B fails its positive control: cheaper-housing moves do not rise with county rent (B11), so the design cannot detect a known driver and its coefficients are weak evidence either way. Its positive slopes are at least as steep for Hispanic movers (+0.58) as for white movers (+0.43). That points to local conditions correlated with the Mexican-origin share, which Hispanics also move away from, more than to aversion to Mexican-origin neighbors. [INFERENCE]

**Limits.**
- Origin is known only to the state.
- One self-reported main reason is recorded, with no second reason and no follow-up.
- The category mixes crime, schools, disorder and neighbors.
- Social desirability would push composition motives into "other", housing or family answers.
- The CPS offers no taxes, politics, homelessness or composition answer.
- County identifiers cover large counties only.
- Every model is descriptive.

## Question 3: who leaves California for Texas (IRS SOI)

Returns and AGI come from the SOI state migration files. AGI is from the year-2 return, in nominal dollars. "Stayers" are California's non-migrant returns in the same pair. [DATA: `derived/irs_ca_tx.csv`; SOURCE: https://www.irs.gov/pub/irs-soi/stateoutflow{yy}{yy}.csv and stateinflow files]

| Pair (AGI year) | CA→TX returns | CA→TX AGI, $bn | AGI per return, CA→TX | AGI per return, CA stayers | Ratio | AGI per return, TX→CA | Net returns CA→TX | Net AGI CA→TX, $bn | Net AGI CA→all states, $bn |
|---|---|---|---|---|---|---|---|---|---|
| 2011–12 (2011) | 27,381 | 1.694 | $61,861 | $72,538 | 0.853 | $59,705 | 5,553 | 0.391 | −0.306 |
| 2012–13 (2012) | 30,771 | 2.369 | $77,003 | $80,344 | 0.958 | $70,383 | 8,498 | 0.802 | 3.299 |
| 2013–14 (2013) | 33,626 | 2.188 | $65,069 | $78,936 | 0.824 | $73,065 | 12,235 | 0.625 | 0.782 |
| 2014–15 (2014) | 25,288 | 1.805 | $71,362 | $84,519 | 0.844 | $60,743 | 4,765 | 0.558 | 2.013 |
| 2015–16 (2015) | 30,052 | 2.353 | $78,299 | $88,355 | 0.886 | $75,914 | 5,795 | 0.512 | 2.006 |
| 2016–17 (2016) | 41,707 | 3.549 | $85,102 | $90,330 | 0.942 | $73,314 | 12,337 | 1.396 | 6.875 |
| 2017–18 (2017) | 34,526 | 3.144 | $91,062 | $96,052 | 0.948 | $68,911 | 11,110 | 1.530 | 7.984 |
| 2018–19 (2018) | 36,103 | 3.448 | $95,516 | $101,162 | 0.944 | $85,393 | 14,242 | 1.582 | 8.809 |
| 2019–20 (2019) | 42,892 | 4.570 | $106,535 | $102,016 | 1.044 | $79,499 | 21,321 | 2.855 | 17.815 |
| 2020–21 (2020) | 52,816 | 7.222 | $136,736 | $103,279 | 1.324 | $75,394 | 31,713 | 5.631 | 29.071 |
| 2021–22 (2021) | 54,136 | 7.902 | $145,960 | $123,448 | 1.182 | $106,197 | 30,820 | 5.426 | 23.792 |
| 2022–23 (2022) | 44,417 | 4.765 | $107,273 | $115,771 | 0.927 | $95,486 | 19,447 | 2.380 | 11.921 |

Before the 2019–20 pair, California-to-Texas filers had less income than California's stayers. From 2019–20 through 2021–22 they had more, then fell back below in 2022–23. Texas-to-California filers had less income than those going the other way in every pair except 2013–14. Caveats from the IRS users' guide:
- "Minor updates were made to the method for matching returns across years. This change results in about a 5 percent increase in the number of returns included in the data" (2022–23).
- Processing changes against identity theft "may have an impact on the migration data and should be considered when comparing the data across years".
- The address is a mailing address.

[SOURCE: https://www.irs.gov/pub/irs-soi/2223inpublicmigdoc.pdf, section B and section C] The 2014–15 pair is low in both directions; its cause was not found. [UNVERIFIED]

**Austin.** Returns moving from California counties to the Austin–Round Rock counties (Travis, Williamson, Hays, Bastrop, Caldwell). County cells under 20 returns are suppressed, so these are floors. [DATA: `derived/irs_ca_austin.csv`]

| Pair | Returns | Individuals | AGI, $bn | AGI per return | Share of all CA→TX returns (state file) | Share of unsuppressed county rows |
|---|---|---|---|---|---|---|
| 2018–19 | 6,707 | 12,510 | 0.965 | $143,932 | 18.6% | 24.0% |
| 2019–20 | 8,373 | 15,802 | 1.402 | $167,438 | 19.5% | 24.5% |
| 2020–21 | 10,524 | 19,304 | 2.491 | $236,676 | 19.9% | 24.2% |
| 2021–22 | 9,380 | 16,489 | 1.906 | $203,187 | 17.3% | 21.1% |
| 2022–23 | 7,126 | 11,932 | 1.213 | $170,170 | 16.0% | 19.9% |

Movers to Austin are the high-income end of the California-to-Texas flow: $144k–237k AGI per return, against $96k–146k for all California-to-Texas returns in the same pairs.

**Tax those leavers took with them.** Net AGI is multiplied by ITEP's state and local tax shares for the fourth income quintile (2024 law, 2023 incomes, non-elderly). The fourth quintile is $86,100–145,900 in California and $73,900–134,200 in Texas, matching the movers' AGI per return. Three cases:
- Low: personal income tax plus individual sales and excise taxes. California 3.3 + 3.3 = 6.6%; Texas 0 + 3.2 = 3.2%.
- Central: total taxes less property taxes, since the vacated home stays on the roll. California 7.8%; Texas 5.2%.
- High: total taxes. California 11.0%; Texas 8.8%.

California's total share is flat across income groups, 10.3–12.0%, so its high case holds for any income mix. Its income-tax share rises from 3.3% in the fourth quintile to 8.8% for the top 1%, so the low and central cases understate California's loss on a top-heavy flow. Texas's total share falls from 8.8% in the fourth quintile to 4.6% for the top 1%, so on a top-heavy flow Texas gains less than the cases shown. [SOURCE: https://itep.org/whopays/california/ and https://itep.org/whopays/texas/, Who Pays? 7th edition tables; DATA: `derived/tax_transfer.csv`]

| Window | Net AGI CA→TX, $bn/yr | California loses, $bn/yr (low/central/high) | Texas gains, $bn/yr | Net AGI CA→all states, $bn/yr | California loses on it, $bn/yr | Part moved by households citing neighborhood/crime: net AGI → California's loss, $bn/yr |
|---|---|---|---|---|---|---|
| Mean of 12 pairs, 2011–12 to 2022–23 | 1.974 | 0.130 / 0.154 / 0.217 | 0.063 / 0.103 / 0.174 | 9.505 | 0.627 / 0.741 / 1.046 | 0.505 → 0.033 / 0.039 / 0.056 |
| Mean of 4 pairs, 2019–20 to 2022–23 | 4.073 | 0.269 / 0.318 / 0.448 | 0.130 / 0.212 / 0.358 | 20.650 | 1.363 / 1.611 / 2.271 | 0.817 → 0.054 / 0.064 / 0.090 |
| Stock: sum of the 12 net cohorts, as of 2022–23 | 23.688 | 1.563 / 1.848 / 2.606 | 0.758 / 1.232 / 2.085 | 114.061 | 7.528 / 8.897 / 12.547 | 6.065 → 0.400 / 0.473 / 0.667 |

Net individuals CA→TX: 34,629 a year (mean), 415,553 in the stock. Net individuals CA→all states: 153,885 a year, 1,846,615 in the stock.

The neighborhood/crime part applies the income-weighted CPS shares above (2.30% of leavers' household income, 0.85% of in-movers') to the IRS gross flows in each pair. The stock row sums each net cohort at its move-year AGI. It assumes no income growth, no deaths and no later moves, and it overlaps the per-cohort rows.

Every dollar here is a transfer between states, not a national loss. California also stops paying for the services those residents used, and Texas starts. That spending side is **unpriced** here. The reason is structural: the ITEP shares count only taxes families bear, so netting them against average spending per resident would need the account's incidence and response rules (`engine.js`) to be done on the same footing. The tax rows are therefore gross budget effects. Neither state's net budget sign is known from this lane. [INFERENCE]

## Question 4: how many leave for neighborhood/crime, and what those moves cost

**Counts, computed one year at a time** [DATA: `derived/q4_counts.csv`, `derived/q4_counts_by_year.csv`]

| ASEC window | All US-born adult CA leavers a year, CPS (SE) | Citing neighborhood/crime, persons a year, CPS (SE) | Households, CPS | Persons, ACS level (own-ratio years only) | Households, ACS level (own-ratio years only) | Per 1,000 US-born adults in CA a year earlier, CPS / ACS level |
|---|---|---|---|---|---|---|
| 2005–2025 | 286,526 (7,719) | 4,221 (720) | 2,816 | 5,957 (3,622) | 4,009 (2,625) | 0.226 / 0.319 |
| 2016–2025 | 291,645 (13,722) | 4,010 (1,051) | 2,876 | 5,749 (4,033) | 4,159 (3,248) | 0.198 / 0.284 |
| 2020–2025 | 297,036 (18,743) | 4,802 (1,456) | 3,361 | 6,981 (4,210) | 4,891 (3,496) | 0.236 / 0.343 |

Method notes:
- The ACS level multiplies each year's CPS count by that year's ACS-to-CPS ratio for all California leavers, which is 1.14–1.61 in the 12 years with a published ACS pair. Other years use the mean ratio, 1.436. The "own-ratio years only" column averages just the 12 years with their own ratio.
- The pooled CPS count equals the mean of the single years; the script checks this.
- All US-born adult leavers run at 15.15 per 1,000 a year (CPS level, 2005–2025).
- Nationally, 58,813 US-born adult interstate movers a year (SE 3,718) cite neighborhood/crime, in 36,800 households.
- Into California, 1,725 a year (SE 637) cite it, in 1,402 households. California's net loss of neighborhood/crime movers is about 2,500 a year at the CPS level. [CALCULATION]

**Cost per household**, read and quoted in `lit/moving_costs_and_surveys.md`:
- **Low: $4,137** (2024 dollars). IRS SOI Table 1.4, "Moving expenses adjustment", all returns, TY2014–2017: $3,053, $3,256, $3,128 and $3,203 nominal per return. This counts deductible goods and travel for job moves of 50+ miles only. [SOURCE: https://www.irs.gov/pub/irs-soi/14in14ar.xls … 17in14ar.xls; DATA: `derived/irs_moving_expenses.csv`]
- **Central: $6,292.** AMSA: "Average cost of an interstate household move: About $4,300, based on an average weight of 7,400 pounds and average distance of 1,225 miles (2009)". Inflated from 2009 with CPI99. [SOURCE: AMSA Industry Fact Sheet, reprint at https://getmiboxsystem.com/the-market/industry_fact_sheet, p. 2]
- **High: $18,285.** Bayer and Juessen: "The estimated migration costs are US$ 18,285" (SE 2,211). This is a structural estimate that includes non-pecuniary costs; the dollar year is not stated, so the figure is used as printed. [SOURCE: IZA DP 3330, p. 19, Table 2]

Owners who sell also pay a broker's commission, which the three costs above leave out. The FTC and DOJ report "national average commission rates appear to have fallen from 5.5 percent to 5 percent" of the sale price over 1998–2005 [SOURCE: FTC/DOJ, *Competition in the Real Estate Brokerage Industry*, 2007, p. 30]. The CPS records tenure only at the destination, so the number of owners among the neighborhood/crime leavers is unknown and this cost is unpriced.

Kennan and Walker's $312,146 is not used. It prices a hypothetical move to an arbitrary state for young white men; the same paper puts the average realized move at −$80,768 (Table V). [SOURCE: *Econometrica* 79(1), 2011, pp. 232–236]

**Total cost, $M a year** [DATA: `derived/q4_costs.csv`]

| Cost per household | Low count (2,625 households) | Central count (4,009) | High count (4,891) |
|---|---|---|---|
| IRS SOI $4,137 | **10.86** | 16.59 | 20.24 |
| AMSA $6,292 | 16.52 | **25.22** | 30.77 |
| Bayer–Juessen $18,285 | 48.00 | 73.30 | **89.43** |

The headline range is $10.9M, $25.2M and $89.4M a year: the bold cells, with cost and count cases paired. This is an upper bound for moves whose stated main reason is ethnic composition, because the category also holds crime, schools, disorder and neighborhood quality. It is not a ceiling on every move composition influenced. Movers who dislike their neighbors' ethnicity may give housing, family or "other" as the main reason, and the CPS records only one reason (`lit/composition_literature.md` §1.4). [INFERENCE]

## Who wins and who loses

All rows are in `derived/winners_losers_rows.csv`, $bn a year. "Overlaps" marks rows that the ledger must not add to the row they name.

| Group | Channel | Direction | Low / central / high | Basis | Relation |
|---|---|---|---|---|---|
| US-born adults leaving California for neighborhood/crime (0.006M) | Moving costs | loss | 0.011 / 0.025 / 0.089 | modelled | beside |
| Same | The conditions they report leaving, and the California location given up | loss | unpriced | unpriced | beside |
| Same | Gain from the destination, against staying with those conditions | gain | unpriced; revealed preference puts it at least at the moving cost | unpriced | beside |
| California state and local budgets | Taxes on net income moved to all other states (one cohort) | loss | 0.627 / 0.741 / 1.046 | modelled | beside |
| Same | The part moved to Texas | loss | 0.130 / 0.154 / 0.217 | modelled | overlaps the all-states row |
| Same | The part moved by households citing neighborhood/crime | loss | 0.033 / 0.039 / 0.056 | modelled | overlaps the all-states row |
| Same | Stock: taxes on net income moved out 2011–12 to 2022–23, as of 2022–23 | loss | 7.53 / 8.90 / 12.55 | modelled | overlaps the all-states row |
| Same | Spending no longer needed for the net movers | gain | unpriced | unpriced | beside |
| Texas state and local budgets | Taxes on the net income from California (one cohort) | gain | 0.063 / 0.103 / 0.174 | modelled | beside |
| Same | Stock, as of 2022–23 | gain | 0.76 / 1.23 / 2.09 | modelled | overlaps the one-cohort row |
| Same | Spending to serve the net movers | loss | unpriced | unpriced | beside |
| Natives who stay in California | Housing-cost relief from lower demand | gain | unpriced | unpriced | beside |
| California owners and landlords | The other side of that relief | loss | unpriced | unpriced | overlaps the relief row |
| Texas residents | Housing costs and congestion from in-movers (renters lose, owners gain) | loss | unpriced | unpriced | beside |

The rows cover two counterfactuals, and each row names its own. The moving-cost row compares against California without the conditions the movers cite; the "gain from the destination" row compares against staying with them.

## Surveys of why Californians consider leaving (context)

Detail and verbatim quotes are in `lit/moving_costs_and_surveys.md` Task 2.

- **Berkeley IGS Poll #2019-08.** Online, 4,527 registered voters, September 13–18, 2019. 52% were considering leaving: 24% seriously, 28% somewhat. Among them, with more than one answer allowed, the reasons were:
  - high cost of housing 71%
  - high taxes 58%
  - the state's political culture 47% (46% in the text)
  - "Overcrowding/too many people" 38%
  - family 14%
  - lack of job opportunities 13%

  Republicans named political culture at 85% and taxes at 77%. White non-Hispanic considerers named overcrowding at 39% and Latino considerers at 38%. The list offered no crime, homelessness, neighborhood, immigration or ethnic-change option. [SOURCE: https://escholarship.org/content/qt96j2704t/qt96j2704t.pdf, Tables 1–2, pp. 3, 5]
- **PPIC Statewide Survey, February 2023.** 1,539 adults. 34% said housing costs made them seriously consider moving out of the state, and 11% elsewhere in California. Crime appears only as a local problem ("30% big problem"), never as a reason to move. [SOURCE: https://www.ppic.org/publication/ppic-statewide-survey-californians-and-their-government-february-2023/, Q35, Q39]
- **PPIC blogs, 2021 and 2023**, reporting CPS reasons. 2021: jobs 49%, housing 23%, family 20%. 2023: "Since 2015, California has experienced net losses of over 500,000 adults who cite housing as the primary reason". Also: "California has been losing lower- and middle-income residents to other states for some time while continuing to gain higher-income adults" (2021). [SOURCE: https://www.ppic.org/blog/whos-leaving-california-and-whos-moving-in/; the 2023 text was read from the rendered PDF pages]

Stated consideration is not a move, and no survey read here asked about neighbors' ethnicity.

## Steel-man and disconfirmation

**The strongest case for the operator's hypothesis.** Natives leave places as immigrant or minority shares rise, and stated reasons hide it:
- White flight shows tipping at 5–20% minority share, with discontinuities of −7.3 to −13.6% of tract population by decade, 1970–2000 (SEs 1.5–2.7). The tipping point tracks white racial attitudes after crime controls. [Card, Mas & Rothstein, NBER w13052, Table 3; grade A for tipping]
- PSID natives' odds of leaving a tract rise 11.2% per SD of the foreign-born share. [Crowder, Hall & Tolnay 2011; grade B]
- Frey (1995) describes "an immigration-induced 'flight' that exports lower income and less-educated Californians" to nearby states. [abstract only; grade C]
- A randomized vignette in Houston, holding crime, schools and property values fixed, finds whites rate neighborhoods lower as the Hispanic share rises. [Lewis, Emerson & Klineberg 2011; abstract only; grade A for design]
- The CPS records one self-reported reason, so a composition motive can hide behind "cheaper housing", "family" or "other".
- Voters considering leaving name the state's political culture (47%) and overcrowding (38%) often.

**What cuts against it.**
- Here, California's US-born leavers cite neighborhood/crime less often than other states' leavers do (−0.43 pp, SE 0.26).
- White and Mexican-origin California leavers give the same neighborhood share relative to other states' leavers, and both show the housing excess, larger if anything for Mexican-origin leavers.
- Across states the neighborhood share falls as the Mexican-origin share rises (design A, which detects both positive controls).
- Where studies separate the Hispanic or Mexican-origin share from the immigrant or Black share, it adds little:
  - Hall and Crowder: whites' odds of leaving the tract move by −7% to +5% per 10 pp of Mexican-origin share, holding the foreign-born share. [PSID 1980–2009; grade B]
  - Pais, South and Crowder: the Latino share, for Anglos, gives an odds ratio of 1.04 (95% CI 0.98–1.10) per 10 pp. [PSID 1990–95; grade B]
  - Emerson, Yancey and Chai: a national randomized vignette finds "Asian and Hispanic neighborhood composition do not matter to whites". [2001; abstract only; grade A for design]
  - Wright, Ellis and Reibel: native net migration to large metros is "either positively related or unrelated to immigration". [1997; abstract only; grade C]
- Every tract-level study concerns moves within a metro; none links California's interstate out-migration to its Hispanic share.

**Balance.** A general minority and foreign-born effect on neighborhood exits is well supported (grade B, several PSID studies). A Hispanic-specific effect is contested: two randomized designs disagree by place and period, and two PSID studies find it small or null. For California's interstate leavers, the stated-reason record points to housing, jobs and family. It cannot rule out composition motives hidden behind those answers, but nothing in it points to one. [INFERENCE]

**Evidence-symmetry rules** (`notes/quant-bias-checklist.md`)
1. External causal estimates are quoted with interval or SE and population where the source gives them. Frey, Wright et al., Emerson et al. and Lewis et al. were read as abstracts only, and no numbers are taken from them.
2. The stated-reason flaw applies on both sides. The CPS shares that weigh against the hypothesis and the IGS answers that could support it (political culture, overcrowding) are both stated, both self-selected and both unable to name composition. Frey (supports) and Wright et al. (against) share the same aggregate-flow flaw and get the same grade, C. Emerson et al. (null) and Lewis et al. (negative) have the same design, both are graded A for design, and both are marked abstract-only.
3. No affiliation enters any grade.
4. Lean of the graded literature: 10 studies. Six support composition-linked exits in general: Card, Mas and Rothstein; Crowder, Hall and Tolnay; Crowder and South; Krysan et al.; Frey; Lewis et al. Three weigh against a Hispanic-specific effect: Hall and Crowder; Emerson et al.; Wright et al. Pais et al. is inconclusive. Each grade level holds studies on both sides.
5. Costs and benefits are priced alike where evidence allows. The movers' moving costs are priced. Their gain is unpriced, but revealed preference puts it at or above the cost. California's lost taxes and Texas's gained taxes are priced. Both states' matching spending is unpriced for the stated reason, so the budget rows are flagged as gross. This is a known gap, not a symmetric pricing.

## [FRAMING-SENSITIVE] notes

- Whether a voluntary move away from disliked neighborhood conditions counts as a harm depends on the counterfactual. Against staying with those conditions, the mover gains. Against a California without them, the mover loses at least the moving cost. The table carries both, labeled.
- "Failed state" and "rotten" are the operator's words. This lane tests stated reasons and moves, not those judgments.
- Ranking housing costs above composition rests on self-reports.

## Would change it

Any of these would change the conclusion:
- A survey of actual leavers that offers crime, schools, homelessness and neighbors' ethnicity as separate reasons, or a list experiment that gets around social desirability, finding composition behind more than about 5% of US-born California leavers.
- ACS PUMS migration PUMAs (MIGPUMA) showing US-born adults leaving California PUMAs at rates that rise with the PUMA's Mexican-origin share, after rent, income and crime controls. This is revealed behavior, with no reasons, and is the natural next lane.
- The restricted CPS with origin county reversing design A's sign.
- For question 3, pricing the spending that moves with the net movers could flip either state's net budget sign.

## Coverage

**Covered:** every data item in the brief (IPUMS-CPS ASEC 1999–2025 with replicate weights; Census public ASEC 2014, 2015 and 2019–2025; IRS SOI state files 2011–12 to 2022–23 and county files 2018–19 to 2022–23; ACS 1-year and 5-year controls), all four questions, and every gate.

**Skipped or blocked, with reasons:**
- Origin county or metro for interstate movers: absent from IPUMS and the public Census file. Replaced by designs A and B.
- ACS state-to-state tables for 2005–2009: they use a multi-block layout that was not parsed. Their years take the mean ACS/CPS ratio.
- Full texts not obtained: Emerson et al. 2001, Lewis et al. 2011, Frey 1995/1996, Wright et al. 1997 (abstracts only); Krysan 2002, Kritz & Gurak 2001, White & Liang 1998 (not covered); Bayer–Juessen 2012's published dollar figure (paywalled).
- Surveys not read: Berkeley IGS 2021 (not found), UCSD 2021, LAO, California Policy Lab.
- The PPIC 2023 blog's text layer is garbled; it was read from rendered pages.

The repo context named in the brief was used only through the housing lane's figure, verified in `../housing_supply_ca_tx_2026_09_22/RESULT.md` line 11: native-born non-Hispanic white adults aged 25–64 left California on net at 11.73 per 1,000 in ACS 2024. That is a net rate for one group. The 0.23–0.32 per 1,000 here is a gross rate of US-born adults citing one reason. The two are not comparable as a ratio. [DATA]

## Shared files

No shared file needs a change for these results. Proposed, not applied: a dataset-register entry for the two new IPUMS extracts. Diff against `research/immigration-dataset-register.md`, to insert after the `IPUMS_CPS_ASEC_1994_2025_2NDGEN` entry:

```diff
+### IPUMS_CPS_ASEC_1999_2025_MOVERS — reason for moving, migration, replicate weights (extracts 2 and 3)
+
+- Source/acquired: IPUMS CPS extracts 2 and 3 on the operator's account, submitted by `infra/immigration-fiscal/movers_reasons_2026_09_24/fetch_ipums.py` on September 24, 2026 and downloaded by the parent session with the same script (23:21 CEST).
+- Local/codebook/size: lane cache `infra/immigration-fiscal/movers_reasons_2026_09_24/_cache/ipums/` (ignored). `cps_main.csv.gz`, 113,716,045 bytes, SHA256 `948c590b0fcf49c3…`, DDI `cps_main.xml` (35 variables), 5,027,101 person rows, ASEC 1999–2025. `cps_repwt.csv.gz`, 34,279,160 bytes, SHA256 `ee28a211cb585…`, DDI `cps_repwt.xml` (178 variables), 59,734 interstate movers (MIGRATE1 = 5), ASEC 2005–2025. Manifest `manifest.json` beside them.
+- Key variables: `WHYMOVE` (main reason for moving, 20 codes), `MIGRATE1`, `MIGSTA1`, `STATEFIP`, `COUNTY`/`COUNTYERR`, `METFIPS`, `NATIVITY`, `BPL`, `CITIZEN`, `HISPAN`, `RACE`, `AGE`, `SEX`, `EDUC`, `INCTOT`, `HHINCOME`, `OWNERSHP`, `RELATE`, `HFLAG`, `ASECWT`, `CPI99`; `REPWTP1`–`REPWTP160` in extract 3.
+- Quirks/use: no county or metro of residence one year ago exists in IPUMS ASEC; the 2014 ASEC's two files are each weighted to the full population (scale by 0.6986/0.3014); in ASEC 2012–2015 reason codes 14–17 nearly vanish while code 13 swells; the CPS finds 0.62–0.87 of the ACS level of California out-movers. Consumed by the movers lane (`build_cps.py` and after).
```

## Instrument note

This lane was run by an LLM. Post-training may dispose it toward findings that play down ethnic-composition motives (`notes/llm-bias-caveat.md`). Four steps guard against that:
- Positive controls decide whether a null or negative gradient is informative.
- Every specification is reported, including the ones that point toward the hypothesis: B5, B6 and B8, and the Houston vignette.
- The literature on both sides is graded on one scale.
- The test that could have favored the hypothesis, white against Mexican-origin leavers, is reported whatever its result.

## Revisions

- 2026-09-25 (weekly conceptual audit §9): the descriptive finding stands: few leavers name
  neighborhood or crime, and housing is California's distinctive reason. "These rows test the claim
  directly" is narrowed. Reason shares among leavers cannot measure leaving rates, and if
  immigration raises housing costs or changes schools, movers who answer "housing" are reporting
  the channel, not ruling it out. The test that discriminates is reason-specific leaving rates per
  origin population against an independent counterfactual.
  [Decision](../../../decisions/2026-09-25-weekly-audit-corrections.md).
