# The real size of the Mexican-origin population across generations

**Verdict:** 40 million is a little too low, not badly too low. The CPS ASEC 2025 self-identification union reproduces at 40.97M ± 0.38M (12.23M Mexico-born, 14.35M US-born with a Mexico-born parent, 14.38M US-born with two US-born parents identifying as Mexican); the Census Bureau's own construction on the same file gives 40.69M and its published 2024 table 39.0M. Two thirds of that total is fixed by birthplace and cannot attrite. The ACS ancestry write-in gives a smaller population (27.7M against 38.9M for self-identification, union 40.5M), so a second self-report does not recover hidden millions. Ethnic attrition reproduced with Duncan and Trejo's design on the 2025 CPS, linking children to co-resident parents so that grandparents' birthplaces are observed: the second generation reproduces their 92.4% identification to the decimal (92.46%), and the third generation identifies as Mexican at 88.8% against their 71.8% for 1994–2006 and as Hispanic at 93.7% against their 81.7% for 2003–2013. Attrition is monotone in Mexico-born grandparents (2.1% with four, 22.0% with one) and survives an imputation check. The correction is therefore +0.80M measured (third-generation attriters), +1.8M central (fourth-plus at the measured third-generation rate), +4.1M if the unobservable fourth-plus still attrites at 1990s rates; coverage adds between zero and 7.6%, and dividing by the CPS Hispanic coverage ratio of 0.82 is a double count of the weighting. Defensible total 42–45M, floor 41.8M. Adding attriters back, who are 0.76 years better schooled, narrows the per-person gap to third-plus whites from −$7,105 to −$6,864 on the central arm and moves the aggregate from −$290.6bn to between −$290.6bn and −$301.2bn. Ladder 67's "17% of third-generation children" is a stale pan-Hispanic 2003–2013 figure. [SOURCE: `infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/RESULT.md`, `derived/`] [FRAMING-SENSITIVE: attrition on children is extrapolated to adults; fourth-plus attrition is unobservable; whole-person vs fractional counting is a convention]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/`.

## 1. Counts by definition

| Definition | Population | Source |
|---|---|---|
| G1 Mexico-born, foreign-born | 12.231M (SE 0.248) | CPS ASEC 2025 |
| G2 native, at least one Mexico-born parent | 14.354M (0.284) | CPS ASEC 2025 |
| G3+ native, two US-area parents, self-ID Mexican | 14.383M (0.309) | CPS ASEC 2025 |
| Union, repo definition | 40.968M (0.379) | CPS ASEC 2025 |
| Union, Census Bureau construction | 40.688M | CPS ASEC 2025 |
| Published 2024 generation table | 39.0M | Census Bureau |
| Self-ID Mexican or Mexico-born | 39.430M | ACS 2024 |
| Mexican ancestry write-in | 27.686M | ACS 2024 |
| Union of both ACS self-reports | 40.544M | ACS 2024 |
| Floor: third-generation attriters added | 41.770M | CALCULATION |
| Central: fourth-plus identifies at the measured third-generation rate | 42.780M | CALCULATION |
| Fourth-plus at Duncan–Trejo's 1994–2006 rate | 45.077M | CALCULATION |
| 1970 reinterview bound (27 observations, not an estimate) | 51.812M | CALCULATION |
| Coverage: PES 4.99% on everyone | ×1.053 | CALCULATION |
| Coverage: PES plus CMS 5/37 on the unauthorized Mexico-born | ×1.076 | CALCULATION |
| Central attrition plus PES coverage | 45.0M | CALCULATION |
| Fractional counting (quarter per Mexico-born grandparent) | third generation ×0.59 | convention |

[SOURCE: `derived/arm1_counts_cps.csv`, `arm2_ancestry_totals.csv`, `arm3_correction_bounds.csv`, `arm4_coverage_grid.csv`, `arm3_fractional_counting.csv`]

## 2. Attrition, reproduced

Share of objectively Mexican-descent children not identified as Mexican, CPS ASEC 2025: second generation 6.32% (SE 0.68), 3.46% with both parents of Mexican descent and 10.74% with one; third generation 9.19% (1.00), 2.10% / 7.13% / 11.78% / 21.99% with four, three, two, one Mexico-born grandparents; flat across age bands. Strict Duncan–Trejo Table 8 replication: second generation 92.46% identify (theirs 92.4%), third 88.81% (71.8%), fourth-plus 88.28% (70.8%). Decomposition of the 28.25% → 11.19% fall: composition (more Mexico-born grandparents today) takes it to 20.09%, rates alone to 15.25%, both to 11.19%. Restricting to wholly unallocated records moves the third-generation rate down (9.19% → 8.17%), so imputation is not producing it. [SOURCE: `derived/arm3_attrition_children.csv`, `arm3_dt_table8_replication.csv`, `arm3_dt_decomposition.csv`, `arm3_allocation_check.csv`; Duncan and Trejo 2011 JOLE 29(2), Table 8; 2017 ILR Review 71(5), Table 1; 2025 AEA P&P 115, Tables 1 and 3, all from the PDFs] [CALCULATION]

## 3. Coverage

CPS weights are poststratified to population controls by age, sex and Hispanic origin, so the pre-poststratification Hispanic coverage ratio of 0.81–0.83 is already corrected and must not be applied again. What remains is error in the controls, bounded by the 2020 PES Hispanic net undercount of 4.99% (a partly absorbed upper bound). Schemes: controls right ×1.000; PES on everyone ×1.053; PES plus DHS decay on the unauthorized ×1.057; PES plus CMS on the unauthorized ×1.076; unauthorized only ×1.030. The unauthorized Mexico-born (4.567M, 37% of the Mexico-born) come from the parallel lane. [SOURCE: CPS March 2025 technical documentation pp. 4–10; 2020 PES Table B; `derived/arm4_coverage_grid.csv`] [CALCULATION]

## 4. Fiscal implication

Attriters average +0.76 years of schooling (Duncan and Trejo 2017), which closes 72% of the Mexican third-plus's 1.05-year gap to third-plus whites, so the middle arm assigns them 28% of the third-plus gap. Per-person gap vs third-plus whites (all-age ledger, shared allocation): standing −$7,105; floor +0.80M: −$6,969 / −$6,996 / −$7,018 (fully converged / Duncan–Trejo / halfway); central +1.81M: −$6,804 / −$6,864 / −$6,913; +4.11M: −$6,457 / −$6,586 / −$6,692. Aggregate −$290.6bn under full convergence by construction, otherwise −$291.7bn to −$301.2bn across the measured and central arms. Adding attriters narrows the average and slightly widens the total. [SOURCE: `derived/arm5_fiscal_implication.csv`, `arm5_education_selectivity.csv`, `all_age_ledger_2026_09_17/derived/estimates.csv`] [CALCULATION]

## 5. Limits

Attrition is measured on co-resident children, reported by the household respondent, and extrapolated to adults; fourth-plus attrition is unobservable in the CPS and is the largest uncertainty; ancestry is a self-report with 8.0M non-response among self-identified Mexicans; coverage multipliers are assumptions built for other populations; Emeka and Vallejo 2011 was not obtained (its 6% is [UNVERIFIED]; the ACS 2024 rebuild gives 2.09% of Latin-American-ancestry respondents answering not Hispanic); the ACS and CPS disagree by 1.43M on the self-identifying Mexican population. Resident stock, not admission; no policy advice.

## Sources

CPS ASEC 2025 person file with 160 replicate weights; ACS 2024 1-year PUMS with 80 replicate weights; Census Bureau 2024 CPS generation table 4; CPS March 2025 technical documentation; 2020 Post-Enumeration Survey coverage tables; Duncan and Trejo 2011, 2017, 2025 (primary PDFs); 1970 Census Content Reinterview Study via Duncan and Trejo 2011 Table 2; `all_age_ledger_2026_09_17`; `unauthorized_population_size_2026_09_19`; ladder 67, 85, 123, 157.
