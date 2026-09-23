# Who is hurt by non-fatal violence: the NCVS victim–offender matrix against the homicide one

## Current correction — September 19, 2026

**Verdict:** The September 19 arithmetic repair reproduces: the Hispanic inter-group CJS scenario is $90.91 per resident-year age 12+, and the Hispanic intra-group share is 0.40444. But CJS spending is financed by taxpayers, not assigned to the victim's ethnicity. The dollar table is an imputed cost of incidents involving out-group victims, not a fiscal transfer onto that group. It applies each victim group's mean severity to every offender group within that row; pair-specific offense severity is not observed. The $65–128 endpoints vary simple-assault prices only and are not bounds on total uncertainty. [SOURCE: lane analysis.py and derived tables; independent arithmetic in the audit]

The 0.79 adjusted Hispanic offender ratio uses a victim-age curve as a proxy; it is not actual offender-age standardization. Keep the raw 0.937 ratio with its population and missing-ethnicity limits. In-group concentration relative to population share is descriptive association, not proof of targeting preferences without a contact-opportunity comparison. No nativity or generation conclusion follows from these all-Hispanic tables. [INFERENCE from the documented design]

This correction governs conflicting claims in the retained assessment below. Evidence and scope: [five-day cross-check](immigration-five-day-cross-check-2026-09-19.md).

## Retained assessment and evidence

**Verdict:** Off the murder margin the matrix looks nothing like the homicide one. Pooling the National Crime Victimization Survey's published 2022–2024 tables, the share of each offender group's violent incidents that falls on a victim of the same group is 0.760 for white offenders, 0.404 for Hispanic and 0.345 for Black, against 0.809, 0.717 and 0.813 on cleared homicide (ladder 143). A Hispanic offender's victim is as likely to be white (0.402) as Hispanic. The two minority diagonals roughly halve; the white one barely moves. Part of the gap is a real severity gradient (the Hispanic intra-group share rises from 0.350 on simple assault to 0.460 on serious violence in the one year with both tables) and part is the clearance selection the homicide lane flagged; the published tables cannot separate them. On the offender side, violent incidents per 1,000 residents 12 and over run 36.7 where the perceived offender is Black, 14.9 white and 13.9 Hispanic, and age composition predicts a Hispanic rate 18% above white, so the age-adjusted Hispanic ratio is 0.79. The inter-group criminal-justice cost a Hispanic offender population imposes on victims outside it is $91 per Hispanic resident-year (bounds $65 to $128), against $263 for Black ($188 to $373) and $40 for white ($29 to $56); the central figure prices a simple assault at $25,526 (criminal-justice component $5,120) derived from Miller et al. 2021, and the bounds price it at zero and at the McCollister aggravated-assault cost. These replace figures first published three times too high (see Revisions). Offender ethnicity is the victim's perception and 18.3% of incidents carry none. [SOURCE: `infra/immigration-fiscal/ncvs_victim_offender_2026_09_18/derived/cv_matrix_violent.csv`, `comparison_with_homicide_all_cells.csv`, `inter_group_cost_transfer.csv`]

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

McCollister unit costs (2024$: rape and sexual assault $350,802, robbery $61,644, aggravated assault $155,924; criminal-justice components $38,579, $20,145, $12,590) on each victim group's offence mix from N-DASH. Simple assault has no McCollister cost and is 55 to 64% of victimizations. The central arm prices it at $25,526 (tangible $8,601, of which criminal-justice $5,120; lost quality of life $16,925), obtained by splitting Miller et al. 2021's pooled assault price of $37,530 (84% simple assault by count) at an aggravated-to-simple cost ratio of 3.96, the geometric mean of the 1996 NIJ injury relativity (1.52) and a residual against McCollister (10.3); the price runs $12,900 to $34,800 over ratios 13 to 1.5 (`derived/simple_assault_sensitivity_to_k.csv`). The zero and aggravated-assault arms are kept as bounds. On the criminal-justice side the low Miller arm coincides with the central one and the high Miller arm with the aggravated bound, because the 1996 source carries no adjudication line and the derived bracket is capped at McCollister's aggravated figure. The inter-group transfer, what each offender group's violence costs victims outside the group per resident-year of the offender group: *[Qualified 2026-09-23, `infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md`: the $155,924 aggravated-assault price is 76% risk-of-homicide premium, which counts deaths already counted as murders; the assault split's upper anchor k = 10.31 uses that price and falls to about 1 without it, so only the survey floor (1.88–1.93) bounds k.]*

| arm | White | Black | Hispanic | Other |
|---|---|---|---|---|
| social cost, simple central | 296 | 1,984 | 695 | 1,079 |
| social cost, simple at zero | 242 | 1,608 | 567 | 876 |
| social cost, simple at aggravated | 576 | 3,907 | 1,351 | 2,114 |
| criminal-justice, simple central | 40 | 263 | 91 | 142 |
| criminal-justice, simple at zero | 29 | 188 | 65 | 102 |
| criminal-justice, simple at aggravated | 56 | 373 | 128 | 202 |

Totals including the intra-group cost, central arm, criminal-justice pricing: $161 white, $408 Black, $153 Hispanic, $176 Other per resident-year.

The Black-offender transfer is about 2.9 times the Hispanic one at every pricing and the Hispanic about 2.2 to 2.4 times the white. Per event non-fatal violence never approaches a homicide ($10,693 to $11,658 of criminal-justice cost per incident on the central arm, $7,551 to $16,405 across the bounds, against $1.5–1.8M); per capita it is of the same order as several ledger lines because there are six million violent incidents a year against 23,000 homicides. [CALCULATION: `derived/inter_group_cost_transfer.csv`]

## 5. Disconfirmation

Twelve arms. Reallocating the unknown-offender cell proportionally moves the Hispanic diagonal from 0.404 to 0.405; the absurd bound in which every unknown is in-group reaches 0.534, still 0.18 below the homicide figure. 2018 and 2019 on their own conventions give 0.441 and 0.397 against a 2022–2024 three-group baseline of 0.448, so the window is not the result. Two arms disagree and the lane cannot resolve them: injury-only incidents (2012–15) lower the Hispanic diagonal from 0.425 to 0.380 while raising the white and Black ones, whereas serious-violent-only (2019) raises it from 0.397 to 0.460. Hispanic offenders are concentrated in multiple-offender incidents (24.2% of multiple-offender violence against 12.5% of single-offender, 2012–15), so the SHR's single-offender universe under-represents Hispanic-attributed violence on volume, with unknown direction on the matrix. [SOURCE: `derived/disconfirmation_arms.csv`; NCJ 250747 table 2]

## 6. Limits

Perceived offender ethnicity, not a record; multiple-offender incidents coded by the whole group from 2021 (mixed groups fall to "Other"); Hispanic only, no Mexican origin (the homicide lane's ACS bridge, 53 to 75% of Hispanic prisoners Mexican-origin, is the only crosswalk); incidents rather than victimizations for the matrix (1.06 to 1.09 victimizations per incident, uniform across groups); the 2016 redesign break precedes the window; no simple-assault unit cost. Resident groups, not admission categories. [SOURCE: RESULT.md §Limits]

The one thing to carry: the homicide lane's intra-group shares and these cannot both be read as "how much violence stays inside the group". Any repo claim about assortative victimization must name the margin; the concentration ratio against population share is the quantity that travels.

## Sources

BJS Criminal Victimization 2018, 2019, 2021, 2022, 2023, 2024 data tables; BJS NCJ 250747 (Morgan 2017); BJS N-DASH exports; McCollister, French and Fang 2010; Miller, Cohen, Swedler, Ali and Hendrie 2021 (Journal of Benefit-Cost Analysis 12(1), tables 4, 5 and 8, PDF pinned by sha256 in the lane); Miller, Cohen and Wiersema 1996 (NIJ NCJ 155282, table 2); ACS 2023 1-year PUMS via api.census.gov; BLS CPI-U. Instrument note: LLM-assisted; every number reproduced by the lane scripts; sha256 of every source in `derived/source_manifest.csv`.

## Revisions

- **2026-09-19.** Two changes to §4 and the verdict. (1) The per-resident-year cost transfer published on 2026-09-18 was three times too high: `analysis.py` divided the pooled 2022–2024 cost by pooled person-years, which is already annual, and then multiplied by three. Found while computing yearly totals for Hispanic-offender violence; confirmed by the lane against a year-by-year reassembly (agreement to a part in a billion) and against the victim-side annual rate (Hispanic offender-side total $110 at criminal-justice pricing with simple assault at zero, against $330 published). Group ratios are unchanged. (2) Simple assault is now priced: central $25,526 from Miller et al. 2021 (which prices assault as one category; the split parameter is the lane's), with the zero and aggravated arms kept as bounds. Claim change: the inter-group criminal-justice transfer is $91 per Hispanic resident-year, not $195–385; ladder 148 and the INDEX row corrected the same day.


## Revisions — September 19, 2026

Corrected the interpretation at the point of reuse; original calculations and evidence are retained. See the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md) and linked audit for the claim-specific reason.
- 2026-09-23: aggravated-assault price and the k anchor qualified for McCollister's risk-of-homicide premium (double counts deaths); see `crime_victim_cost_2026_09_23`.
