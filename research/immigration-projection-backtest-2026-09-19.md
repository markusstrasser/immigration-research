# Lifetime projection checks: historical assumptions and observed composition

**Verdict:** The NRC 1997 baseline's fiscal-policy assumption did not occur: federal debt held by the public rose from 76.0% of GDP in 2016 to 97.4% in 2024 instead of remaining fixed. Its own no-adjustment scenario had an all-origin immigrant-and-descendants NPV of −$15,000, versus +$80,000 in the baseline, in 1996 dollars. That is a material failed policy assumption, not a demonstrated failure of immigrant educational assimilation. A new, narrower GSS schooling-transition back-test does **not** show broad optimistic bias. Current Mexican-origin period-profile projections also move materially with recent arrivals' education, parental nativity and return-migration assumptions. None of these checks establishes an observed lifetime cost of admission. [SOURCE: NRC chapter 7 table 7.6; OMB table 7.1; CALCULATION: lane outputs below.]

**Scope:** Fiscal receipts less attributed spending, from the perspective of US government budgets. Current calculations use 2024 dollars, common 2024 mortality, zero real profile growth and explicit discount rates. No IQ argument, economic-benefit additions, crime valuation or narrative essay. These are expanded **partial** accounts; “complete” in the earlier lineage memo does not establish complete government coverage. [FRAMING-SENSITIVE]

Generator and definitions: [projection back-test lane](../infra/immigration-fiscal/projection_backtest_2026_09_19/README.md). Reproduction uses read-only original data and writes 12 derived tables with source/code hashes.

**Account version:** Composition and exit sensitivities hold the original repaired
age profiles fixed. The [Census2024 annual refresh](immigration-macro-reconciliation-2026-09-19.md)
is a separate release, not a flat adjustment to these lifetimes. This isolates
the education/parentage/exit comparisons.

## 1. What can actually be back-tested from 1997?

[SOURCE] The [NRC's published baseline](https://www.nationalacademies.org/read/5779/chapter/9), pp. 324–325, fixes debt/GDP from 2016 through equal contributions from tax increases and benefit cuts. Table 7.6 explicitly publishes the alternative without adjustment. These were conditional scenarios; the report disclosed their sensitivity. It did not publish a Mexican-specific realized fiscal panel.

[MEASUREMENT] [OMB FY2027 historical table 7.1](https://www.whitehouse.gov/wp-content/uploads/2026/04/hist07z1_fy2027.xlsx), same revision and fiscal-year convention throughout:

| Fiscal year | Federal debt held by public / GDP | Difference from frozen 2016 ratio |
|---|---:|---:|
| 2016 | 76.0% | — |
| 2019 | 78.9% | +2.9 percentage points |
| 2020 | 98.5% | +22.5 points |
| 2024 | 97.4% | +21.4 points |

The miss predates COVID and widens sharply during it. Gross debt is exported separately; changing the debt definition is unnecessary to establish that stabilization did not occur. Today's path is **not** identical to the NRC's perpetual no-adjustment scenario. Therefore its −$15,000 is an original model sensitivity, not the now-observed true lifetime result.

[SOURCE / IDENTIFICATION LIMIT] Appendix 7.A estimates educational transitions from GSS parent-child pairs, with origin/generation adjustments. The published chapter does not supply the complete matrices, implementation, original ethnic weights or a linked forecast-cohort registry. Its 300-year total cannot yet be observed. A strict numerical validation of that fiscal forecast would require those inputs, contemporaneous reconstruction of its tax-benefit accounts, and linked origin/parentage histories. The following is a newly executed, narrower temporal test of the transition method.

## 2. Held-out schooling outcomes: no general optimistic bias established

[CALCULATION] GSS 1972–2024 release 3a. Train on respondents born 1961–1971, observed through 1996; test later, disjoint birth cohorts from 1972 onward, observed 1998–2024. Both samples are aged 25–34. Fit each generation's three-category education transition separately, then apply the old transition probabilities to the held-out parental schooling mix. Every answered parent-child link receives the respondent's survey weight. This estimates a parent-link-weighted outcome, not a unique-child mean.

Primary frame: English interviews, because Spanish entered the GSS sample in 2006. Use NORC's cross-year [WTSSPS recommendation](https://gss.norc.org/faq.html). The old WTSSALL variable is absent in 2021–2024; an initial exploratory run exposed that omission, and the released generator now rejects missing weights and exports the actual included years.

| Group, English interviews | Training / held-out respondents with parent data | Predicted schooling above 12 years | Observed | Observed minus predicted |
|---|---:|---:|---:|---:|
| All-origin G2 | 120 / 595 | 68.25% | 72.85% | +4.59 points |
| All-origin G3 | 378 / 591 | 69.63% | 68.43% | −1.20 points |
| All-origin G4+ | 1,299 / 3,226 | 64.18% | 67.57% | +3.39 points |

The pre-2021 English arm gives G2 +2.49 points and G3 +0.74; the full-period all-language arm gives G2 +3.66 and G3 −1.23. The G3 below-12-years share is underpredicted by 2.80 points in the primary frame, so matching the above-12 share does not validate the entire distribution. School years above 12 do not mean a bachelor's degree.

Mexican-family-origin G2 has **13** usable training respondents. It fails the declared minimum of 30 distinct respondents per parental education category; the generator publishes coverage and refuses a Mexican-specific prediction. No design-correct confidence intervals or statistical rejection of forecast bias is claimed. Respondent nonresponse, remembered parental education, changing origins and survey mode remain limitations. The evidence supports neither blanket validation of the NRC nor the claim that its schooling mechanism was generally unrealistically optimistic.

## 3. A fixed Mexican birth-and-entry group followed across surveys

[CALCULATION] Local IPUMS census/ACS microdata: Mexico-born residents entering 1975–1980 with birth-year proxy 1956–1965. Follow the same birth-and-entry definition in 1990, 2000, 2010 and 2023. Fix the within-cohort birth-year mix to its 1990 target weights; compare with US-born residents of all races with those same birth proxies in each survey. Exclude group quarters.

| Survey | Ages | Target observations | Below-HS share | Log total-income gap among currently employed positive-income respondents |
|---|---|---:|---:|---:|
| 1990 | 25–34 | 24,778 | 77.63% | −0.415 |
| 2000 | 35–44 | 24,503 | 76.48% | −0.456 |
| 2010 | 45–54 | 3,922 | 69.31% | −0.498 |
| 2023 | 58–67 | 3,093 | 67.12% | −0.419 |

The endpoint relative-income gap barely changes after the group already had at least ten years in the US; it widens in the intermediate surveys. The older birth window, 1946–1955, changes from −0.627 in 1990 to −0.659 in 2010. This does not support assuming large additional convergence for these surviving groups, but it cannot identify individual income growth or the contribution of selective emigration.

**Measurement limit:** the extract lacks wage income and sex, and its weeks-worked variable is entirely missing in 2010. The released outcome is explicitly annual **total personal income among currently employed people**, not wages or full-year earnings. The source income and current employment windows differ. Education coding uses 1990+ diploma definitions, avoiding the 1980 grade-12 crosswalk. Repeated cross-sections do not link individuals; survival, return migration, coverage and retirement selection can change the observed group.

## 4. Three material current-model sensitivities

These are conditional period-profile calculations, not confidence bounds or forecasts. They cannot be added to one another: the dimensions overlap and their joint distribution is not identified.

**Recent arrivals' education.** Among Mexico-born residents aged 25–54, the 2016–2025 arrival group has 32.39% below HS and 23.83% BA+, versus 37.79% and 12.26% in the stock. Transport only this education mix to the same supported current age-25–64 fiscal profiles, holding the senior profile common. The age-25 NPV at 3% changes from **−$48,545 to −$8,195**, a +$40,350 difference. At zero discount the corresponding balances are −$359,884 and −$296,656; at 5% they are +$755 and +$32,544. N and extra F are excluded. Education-specific old-age cells are sparse, so their apparent all-age sign reversal remains a labeled diagnostic, not the primary result. Current attainment and surviving arrival stock do not identify education at admission or an admission forecast.

**Parental nativity.** CPS 2025 divides Mexican G2 into 9.223m with two Mexico-born parents, 4.352m with one Mexico-born and one US/territory-born parent, and 0.759m with another or unresolved parent. Replace only working-age fiscal profiles, holding the group's childhood, senior and institutional costs fixed. At birth and a 3% discount, NPV is **−$288,347** under the two-Mexico-born-parent profile and **−$266,206** under the mixed-nativity profile, a $22,141 difference. This is observed association, not an effect of intermarriage. The US-born parent may also be ethnically Mexican.

**Return migration.** Use the NRC's historical 30% all-origin return assumption only as an illustration, with departure in year 5, 10, 20 or 40. Current Mexican exit rates, legal status and destination histories are not inferred from that number. [SSA rules](https://www.ssa.gov/international/payments.html) allow some benefits to continue abroad, so the model separately carries zero or 100% of the founder's current Social Security profile after departure; that is a sensitivity, not an earned-entitlement estimate.

At 3%, 30% departure in year 10 improves the founder's NPV by **$11,804–26,146**, depending on retained SS. For a 100-calendar-interval lineage using existing low fertility, generation length 29, neutral per-capita attribution and no imputed unauthorized-status penalty, the no-exit balance is **−$318,370**. If dependent children leave with the founder, the year-10 exit balance is **−$252,957 to −$238,615**, an improvement of $65,413–79,755. If children remain, the improvement is only the founder's amount. Costs before exit remain counted; adult descendants are not automatically removed. All non-SS overseas fiscal flows, return to the US, selective exit and future policy change remain outside this illustration.

At 5%, early founder-only exit with full SS retained can slightly **worsen** the balance. Thus even the direction of an exit adjustment is not universally guaranteed. The original lineage code also uses 101 calendar intervals, numbered 0–100. This lane exports both a literal 100-interval century and the 101-interval compatibility arm; that timing correction is small beside the substantive assumptions.

## 5. Consequence for the existing conclusion

[INFERENCE] The current annual resident disadvantage is not disproved by these checks. The unsupported step is turning it into one timeless admission or lineage price. The biggest tested historical failure concerns future fiscal adjustment. The schooling test supplies counter-evidence to a general “assimilation projections were too optimistic” assertion. Better recent education, parental composition and migration can move lifetime scenarios by tens of thousands per person or lineage even before macroeconomic responses.

Leading interpretation: profile transport and fiscal-policy assumptions are material, while a fully observed century-long result is unavailable. Main alternative: some observed cohort improvement is selected survival or reporting change. Discriminating evidence would be original NRC matrices plus linked cohort tax/transfer, parentage and overseas-residence records. Decision impact: retain annual account results and conditional lifetime tables; do not label the old century headline empirically validated.

Validation: six unit tests, source-table/header checks, disjoint GSS birth cohorts, explicit survey-year coverage, complete birth-window matching, parentage and education conservation, and reproduction of three canonical personal age profiles within $0.0016 on billion-dollar totals. Model uncertainty is not a sampling interval. The LLM-generated implementation and interpretation remain subject to the same source and disconfirmation requirements as the earlier report.
