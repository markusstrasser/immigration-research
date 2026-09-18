# Who is hurt by non-fatal violence: the NCVS victim–offender matrix against the homicide one

**Verdict:** Off the murder margin the matrix looks nothing like the homicide one. Pooling the National Crime Victimization Survey's published 2022–2024 tables, the share of each offender group's violent incidents that falls on a victim of the same group is 0.760 for white offenders, 0.404 for Hispanic and 0.345 for Black, against 0.809, 0.717 and 0.813 on cleared homicide (ladder 143). A Hispanic offender's victim is as likely to be white (0.402) as Hispanic. The two minority diagonals roughly halve; the white one barely moves. Part of the gap is a real severity gradient (the Hispanic intra-group share rises from 0.350 on simple assault to 0.460 on serious violence in the one year with both tables) and part is the clearance selection the homicide lane flagged; the published tables cannot separate them. On the offender side, violent incidents per 1,000 residents 12 and over run 36.7 where the perceived offender is Black, 14.9 white and 13.9 Hispanic, and age composition predicts a Hispanic rate 18% above white, so the age-adjusted Hispanic ratio is 0.79. The inter-group criminal-justice cost a Hispanic offender population imposes on victims outside it is $195 to $385 per Hispanic resident-year, against $563 to $1,119 for Black and $88 to $169 for white, the range being simple assault priced at zero or at aggravated assault because McCollister publishes no simple-assault cost and it is 55 to 64% of the volume. Offender ethnicity is the victim's perception and 18.3% of incidents carry none. [SOURCE: `infra/immigration-fiscal/ncvs_victim_offender_2026_09_18/derived/cv_matrix_violent.csv`, `comparison_with_homicide_all_cells.csv`, `inter_group_cost_transfer.csv`]

Date: 2026-09-18. Lane: `infra/immigration-fiscal/ncvs_victim_offender_2026_09_18/` (four scripts, 31 derived files, reproduced byte-identically by the parent with the cache warm; the lane also reproduced them cold). Extends ladder 143 and qualifies its intra-group shares, which are a homicide-margin quantity.

## 1. Where the matrix lives, and why the window is 2022–2024

The ICPSR microdata (38963) sits behind a login wall and no account was created; BJS's N-DASH dashboard carries no offender characteristic at all. The victim-by-offender cross-tab is published in the annual Criminal Victimization data tables (table 13 in 2021–2024, with generalized-variance standard errors in appendix table 14) and, for 2012–15 with single-offender, reported-to-police and injury splits, in NCJ 250747. Two definitional breaks set the window: 2019 codes a multiple-offender group as Hispanic if any offender is perceived Hispanic while 2021 onward requires all of them, and 2021 publishes no "Other" victim row, so its rows cover 90.7% of incidents. 2022–2024 is the widest window with one convention and a complete victim universe. [SOURCE: CV2018–CV2024 data tables; NCJ 250747; `derived/icpsr_route_probe.csv`]

Column sums of the published matrix reproduce BJS's separately published offender marginal to within 10 incidents in each of the three years, and all 133 values transcribed from NCJ 250747 appear verbatim in the PDF text. [SOURCE: `derived/analysis_log.txt`]

## 2. The matrix

Pooled 2022–2024, 18,240,550 violent incidents. Column shares with the unknown-offender column dropped (the victim distribution of each offender group, the quantity the homicide memo tabulates):

| victim / offender | White | Black | Hispanic | Other |
|---|---|---|---|---|
| White | 0.760 | 0.382 | 0.402 | 0.592 |
| Black | 0.036 | 0.345 | 0.096 | 0.082 |
| Hispanic | 0.125 | 0.167 | 0.404 | 0.146 |
| Other | 0.079 | 0.105 | 0.098 | 0.180 |

Against cleared homicide: white→white 0.809 to 0.760; Black→Black 0.813 to 0.345; Hispanic→Hispanic 0.717 to 0.404; Hispanic→white 0.156 to 0.402; Black→white 0.112 to 0.382. Every diagonal is lower off the murder margin. Normalised by the victim group's population share (white 60.2%, Black 12.2%, Hispanic 18.3% of residents 12 and over), the concentration ratios are 1.26 white, 2.83 Black, 2.21 Hispanic: every group targets its own more than chance, white offenders least, and that ordering holds on both margins while the magnitudes collapse. [CALCULATION: `derived/cv_matrix_violent.csv`; pooled standard errors are BJS generalized-variance figures summed in quadrature and understate the truth because the NCVS panel is correlated across years]

## 3. Rates and age

Victimization rates per 1,000 residents 12 and over are nearly flat across victim groups (20.9 to 22.7). Offending rates are not: 36.7 Black, 16.0 Other, 14.9 white, 13.9 Hispanic, all lower bounds because the 18.3% of incidents with unknown offender ethnicity leave the numerators. NCVS never crosses offender age with ethnicity, so a direct standardisation is not identified; applying the published fine-grid victimization-age curve (a 4.6× gradient from 18–24 to 65+) to each group's ACS 2023 age structure predicts indices of 1.000 white, 1.110 Black, 1.181 Hispanic, against observed 1.000, 2.474, 0.937. Age runs against the Hispanic result. [CALCULATION: `derived/age_arm_observed_vs_expected.csv`; the victim-age curve stands in for the offender-age curve, which is the weak step]

## 4. Cost

McCollister unit costs (2024$: rape and sexual assault $350,802, robbery $61,644, aggravated assault $155,924; criminal-justice components $38,579, $20,145, $12,590) on each victim group's offence mix from N-DASH. Simple assault has no published cost and is 55 to 64% of victimizations, so every figure is bounded: at zero and at the aggravated-assault price. The inter-group transfer, what each offender group's violence costs victims outside the group per resident-year of the offender group:

| arm | White | Black | Hispanic | Other |
|---|---|---|---|---|
| social cost, simple at zero | 725 | 4,823 | 1,701 | 2,628 |
| social cost, simple at aggravated | 1,729 | 11,720 | 4,053 | 6,343 |
| criminal-justice, simple at zero | 88 | 563 | 195 | 305 |
| criminal-justice, simple at aggravated | 169 | 1,119 | 385 | 605 |

The Black-offender transfer is about 2.9 times the Hispanic one at every pricing and the Hispanic about 2.2 to 2.4 times the white. Per event non-fatal violence never approaches a homicide ($7,551 to $16,405 of criminal-justice cost per incident against $1.5–1.8M); per capita it is of the same order as several ledger lines because there are six million violent incidents a year against 23,000 homicides. [CALCULATION: `derived/inter_group_cost_transfer.csv`]

## 5. Disconfirmation

Twelve arms. Reallocating the unknown-offender cell proportionally moves the Hispanic diagonal from 0.404 to 0.405; the absurd bound in which every unknown is in-group reaches 0.534, still 0.18 below the homicide figure. 2018 and 2019 on their own conventions give 0.441 and 0.397 against a 2022–2024 three-group baseline of 0.448, so the window is not the result. Two arms disagree and the lane cannot resolve them: injury-only incidents (2012–15) lower the Hispanic diagonal from 0.425 to 0.380 while raising the white and Black ones, whereas serious-violent-only (2019) raises it from 0.397 to 0.460. Hispanic offenders are concentrated in multiple-offender incidents (24.2% of multiple-offender violence against 12.5% of single-offender, 2012–15), so the SHR's single-offender universe under-represents Hispanic-attributed violence on volume, with unknown direction on the matrix. [SOURCE: `derived/disconfirmation_arms.csv`; NCJ 250747 table 2]

## 6. Limits

Perceived offender ethnicity, not a record; multiple-offender incidents coded by the whole group from 2021 (mixed groups fall to "Other"); Hispanic only, no Mexican origin (the homicide lane's ACS bridge, 53 to 75% of Hispanic prisoners Mexican-origin, is the only crosswalk); incidents rather than victimizations for the matrix (1.06 to 1.09 victimizations per incident, uniform across groups); the 2016 redesign break precedes the window; no simple-assault unit cost. Resident groups, not admission categories. [SOURCE: RESULT.md §Limits]

The one thing to carry: the homicide lane's intra-group shares and these cannot both be read as "how much violence stays inside the group". Any repo claim about assortative victimization must name the margin; the concentration ratio against population share is the quantity that travels.

## Sources

BJS Criminal Victimization 2018, 2019, 2021, 2022, 2023, 2024 data tables; BJS NCJ 250747 (Morgan 2017); BJS N-DASH exports; McCollister, French and Fang 2010; ACS 2023 1-year PUMS via api.census.gov; BLS CPI-U. Instrument note: LLM-assisted; every number reproduced by the lane scripts; sha256 of every source in `derived/source_manifest.csv`.
