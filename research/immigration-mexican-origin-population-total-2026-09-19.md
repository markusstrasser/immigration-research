# The real size of the Mexican-origin population across generations

**Verdict:** 40 million is a little too low, not badly too low. The CPS ASEC 2025 self-identification union reproduces at 40.97M ± 0.38M (12.23M Mexico-born, 14.35M US-born with a Mexico-born parent, 14.38M US-born with two US-born parents identifying as Mexican); the Census Bureau's own construction on the same file gives 40.69M and its published 2024 table 39.0M. Two thirds of that total is fixed by birthplace and cannot attrite. The ACS ancestry write-in gives a smaller population (27.7M against 38.9M for self-identification, union 40.5M), so a second self-report does not recover hidden millions. Ethnic attrition reproduced with Duncan and Trejo's design on the 2025 CPS, linking children to co-resident parents so that grandparents' birthplaces are observed: the second generation reproduces their 92.4% identification to the decimal (92.46%), and the third generation identifies as Mexican at 88.8% against their 71.8% for 1994–2006 and as Hispanic at 93.7% against their 81.7% for 2003–2013. Attrition is monotone in Mexico-born grandparents (2.1% with four, 22.0% with one) and survives an imputation check. The correction is therefore +0.80M measured (third-generation attriters), +1.8M central (fourth-plus at the measured third-generation rate), +4.1M if the unobservable fourth-plus still attrites at 1990s rates; coverage adds between zero and 7.6%, and dividing by the CPS Hispanic coverage ratio of 0.82 is a double count of the weighting. Defensible total 42–45M, floor 41.8M. Adding attriters back, who are 0.76 years better schooled, narrows the per-person gap to third-plus whites by about $240, from −$8,218 to −$7,981 on the central arm (the measured generation split, with the income tax the survey misses, placed on the main case's keys, item T), and moves the aggregate from −$336.1bn to −$340.9bn (−$338.2bn to −$353.7bn from the floor to the 1990s-rate arm). Ladder 67's "17% of third-generation children" is a stale pan-Hispanic 2003–2013 figure. [SOURCE: `infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/RESULT.md`, `derived/`] [FRAMING-SENSITIVE: attrition on children is extrapolated to adults; fourth-plus attrition is unobservable; whole-person vs fractional counting is a convention]

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

Attriters average +0.76 years of schooling (Duncan and Trejo 2017), which closes 72% of the Mexican third-plus's 1.05-year gap to third-plus whites. The central rule is the measured generation split ([carryover lane](../infra/immigration-fiscal/carryover_identity_2026_09_27/RESULT.md) §2, §5): attriters lost at the third-generation rate close a share C3 = 0.557 (SE 0.246) of their gap, measured on the CPS basic monthly files 1994–2026 pooled with NLSY97, and later losses close none. Per-person gap vs third-plus whites (all-age ledger, shared allocation, with item T's age-matched increment), with the aggregate: standing −$8,218 and −$336.1bn; floor +0.80M, −$8,111 and −$338.2bn; central +1.81M, −$7,981 and −$340.9bn; +4.11M (fourth-plus at the 1994–2006 rate), −$7,859 and −$353.7bn; fourth-plus at the 1970 rate, −$7,564 and −$391.4bn. Adding attriters narrows the average and widens the total, the wider bounds most, because their extra attriters keep the whole gap. [DATA: `derived/arm5_generation_split_T.csv`] [CALCULATION]

The years convention, the earlier central rule, gives attriters a share of the third-plus gap from the schooling difference alone (28% in its Duncan–Trejo arm): floor +0.80M: −$8,060 / −$8,091 / −$8,117 (fully converged / Duncan–Trejo / halfway); +1.81M: −$7,869 / −$7,939 / −$7,996; +4.11M: −$7,467 / −$7,617 / −$7,740. Aggregate −$336.1bn under full convergence by construction, otherwise −$337.4bn to −$348.3bn across the measured and central arms. [SOURCE: `derived/arm5_fiscal_implication_T.csv`, `arm5_education_selectivity.csv`, `all_age_ledger_2026_09_17/derived/estimates.csv`, item T from `ledger_absolute_2026_09_17/derived/complete_gaps_by_item.csv`] [CALCULATION]

## 5. Limits

Attrition is measured on co-resident children, reported by the household respondent, and extrapolated to adults; fourth-plus attrition is unobservable in the CPS and is the largest uncertainty; ancestry is a self-report with 8.0M non-response among self-identified Mexicans; coverage multipliers are assumptions built for other populations; Emeka and Vallejo 2011 was not obtained (its 6% is [UNVERIFIED]; the ACS 2024 rebuild gives 2.09% of Latin-American-ancestry respondents answering not Hispanic); the ACS and CPS disagree by 1.43M on the self-identifying Mexican population. Resident stock, not admission; no policy advice.

## Sources

CPS ASEC 2025 person file with 160 replicate weights; ACS 2024 1-year PUMS with 80 replicate weights; Census Bureau 2024 CPS generation table 4; CPS March 2025 technical documentation; 2020 Post-Enumeration Survey coverage tables; Duncan and Trejo 2011, 2017, 2025 (primary PDFs); 1970 Census Content Reinterview Study via Duncan and Trejo 2011 Table 2; `all_age_ledger_2026_09_17`; `unauthorized_population_size_2026_09_19`; ladder 67, 85, 123, 157.

## Revisions

- 2026-09-27: arm 3's premise that the fourth-plus generation identifies at the measured third-generation rate does not hold; loss of Mexican identification at birth keeps growing past G3 ([civic lane](../infra/immigration-fiscal/civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv)). Re-run as labelled arms in [`identity_loss_propagation_2026_09_27`](../infra/immigration-fiscal/identity_loss_propagation_2026_09_27/RESULT.md): 42.78M becomes 44.0M with one more step (0.781) and 45.3M compounding (44.4–47.7M); the published 42–45M becomes 44.0–46.3M; the hidden share of the third-plus rises from 11.2% to 17.5–23.0%. These are [MODEL] extrapolations of a birth-stage loss. Ladder 158 bracketed.
- 2026-09-28: arm 5 takes the measured generation split as its central rule (4e9c2e2): only attriters lost at the third-generation rate close part of the gap (C3 0.7758), so the central is −$6,853 per person and −$292.7bn, and the wider bounds rise to −$303.5bn and −$335.1bn. Ladder 158 bracketed.
- 2026-10-05: C3, the share of the self-identified gap that attriters lost at the third-generation rate close, is now measured on the CPS basic monthly files 1994–2026 (526 unique G3 non-identifiers at 25+) pooled with NLSY97: 0.557 (SE 0.246), in place of 0.7758 ([g3_identity_pooled_2026_10_05](../infra/immigration-fiscal/g3_identity_pooled_2026_10_05/RESULT.md), monthly frame). The arm 5 central is −$6,901 per person and −$294.7bn, and the wider bounds are −$305.8bn and −$338.3bn. Ladder 158 bracketed.
- 2026-10-08: the verdict and §4 restate arm 5 with item T, because the white-reference ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T; [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)) and the lane writes the comparison against whites with that key (`derived/arm5_*_T.csv`). The standing gap −$7,105 → −$8,218 per person and −$290.6bn → −$336.1bn; the generation split's central −$6,901 → −$7,981 and −$294.7bn → −$340.9bn; its wider bounds −$305.8bn → −$353.7bn and −$338.3bn → −$391.4bn. The verdict quotes that central, about $240 narrower than standing, where it quoted the years convention's −$6,864 (−$7,939 with item T). Concept affected: the fiscal implication of ethnic attrition (ladder 158).
- 2026-10-08, later: §4 rewritten to its current state. The measured generation split leads as the central rule, the years convention follows as the earlier rule, and the two dated brackets (2026-09-28, 2026-10-08) are folded in (their earlier figures are in the entries above and in git). No figure changes. Concept affected: none; the presentation of arm 5.
