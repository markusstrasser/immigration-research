# Immigration confidence ladder — current corrections

**Current layers: 2026-09-05 (52–64) and 2026-09-16 (65–76).** Entries below supersede the specified prior ratings. The dated earlier ladder is preserved in the historical section. A primary citation verifies a source claim; it does not automatically validate our causal inference, its transfer to another population or a local implementation. [SOURCE: [material audit](immigration-conceptual-audit-2026-09-05.md)] [SOURCE: [repair decision](../decisions/2026-09-05-material-inference-repair.md)]

52. **Old SIPP fiscal outputs are invalid; person-level replacement rebuilt — replaces 12 and 41.** Confirmed implementation errors mixed household donor totals with person recipients and misclassified education and nativity. Withdraw +$1,519/adult for Mexico, +$2,746 native and their downstream calculations. The corrected 2023 raw-data build gives about +$2,371 per Mexico-born adult and +$4,033 per native NH-white adult aged 25–64, ratio 1.70, under globally coarsened donor matching. These are synthetic employee-payroll-minus-allocated-SNAP/TANF/SSI estimates, not full federal incidence or observed tax returns. Transport and sparse-cell precision remain limits. Rating: **strong implementation correction; descriptive partial-accounting result with explicit assumptions**. [SOURCE: [audit](immigration-conceptual-audit-2026-09-05.md), [rebuild and sensitivity](immigration-material-repair-report-2026-09-05.md)]

53. **QWI policy results do not identify native wages — replaces 17 and 21, removes the QWI component from 19 and qualifies 40.** The education/sex QWI product has no nativity/citizenship field; EarnS is average monthly earnings of stable/full-quarter employment. Policy effects can change worker composition and hours as well as pay. The reported log coefficient 0.0051 with SE 0.0081 gives a normal-approximation interval of about −1.07% to +2.12% after exponentiation, for the fitted outcome under the stated variance assumptions. That is not a confidence bound on native hourly-wage effects, on a standardized immigrant labor-supply shock, or on the Borjas model. Static staggered TWFE and unmeasured compliance add identification limits. Non-significance is not equivalence. Published Card/Foged–Peri evidence stands or falls on its own designs. Rating: **strong variable-definition correction; causal native-wage interpretation withdrawn**. [SOURCE: [Census QWI variables](https://api.census.gov/data/timeseries/qwi/se/variables.html)] [SOURCE: [E-Verify memo](immigration-causal-everify-card-vs-borjas.md)]

54. **Colas–Sachs supplies a positive modeled channel, not a universal upper-bound theorem — replaces 45.** Its indirect fiscal benefit can shrink or reverse direct costs in specified scenarios. It does not prove every omitted general-equilibrium effect is beneficial, that NAS estimates bound all possible costs, or that the same amount can be added to CBO estimates already containing macro effects. Annual flows and lifetime NPVs require a common price year, horizon and population. Rating: **published model evidence, conditional scope**. [SOURCE: [Colas–Sachs](https://doi.org/10.1257/pol.20220176)]

55. **The CBO federal result is a projection with defined coverage — replaces 46 and qualifies 5.** July 2024 CBO projects about $897B less federal deficit over 2024–2034 for its above-baseline “other foreign nationals” scenario. The scored budget includes revenues, mandatory spending and interest; discretionary appropriations are outside that total. Its illustrative population-proportional discretionary increase is about $0.2T. The projected $8.9T cumulative nominal GDP gain is a different, overlapping economic outcome and cannot be added to budget savings. The 8.7M category change is not a count of all unique border entrants. Rating: **strong source attribution; uncertain model projection, not realized causal estimate**. [SOURCE: [CBO July report](https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf)]

56. **Nativity, race, generation and justice outcome must remain distinct — replaces 51 and narrows 42/48.** The first-generation Texas arrest or conviction comparison is a descriptive result for its source populations. A white-only comparator changes the target group; it is not automatically a correction for misclassification or a matched causal comparison. Since `rN = a*r2 + (1-a)*r3+`, the effect of including the second generation depends on r2 versus r3+, not r2 versus first-generation immigrants. An ecological null for unauthorized share does not negate an individual status-rate difference. Homicide is relatively well recorded, but convictions still depend on clearance, prosecution, timing and population measurement. The CPS earnings/education loader cannot settle crime by generation. Rating: **source-specific descriptive findings; general direction of comparator adjustment unidentified**. [SOURCE: [crime memo](immigration-crime-rates-unauthorized-vs-native-born.md)] [INFERENCE: mixture identity and estimands]

57. **A housing IV estimate is conditional identification, not proof of a unique mechanism — qualifies 18/20/38/50.** Local foreign-born-share/rent/elasticity correlations are descriptive. A published instrumental-variable estimate requires its exclusion and relevance assumptions; a statistically insignificant supply/permit response alone does not establish zero response or prove the mechanism. Report the paper's treatment denominator, price outcome, period and uncertainty when quoting its effect. U.S. or local housing evidence does not establish a world multi-decade migration ceiling. Rating: **design-specific evidence; mechanism and extrapolation limited**. [SOURCE: [housing frontier](immigration-urbanism-frontier-2026-06-25.md)] [INFERENCE]

58. **Cross-sectional controls and passed placebos do not independently identify causality.** The eight-state cost regression, threshold interactions and receiver contrasts need their stated sampling and identification assumptions. High p-values do not rule out economically meaningful effects without a powered equivalence test. Institutional hypotheses cannot receive numerical posterior probabilities without an explicit likelihood and evidentiary model. Conditioning on a policy response, permits or observed service use may block effects or select on outcomes. Rating: **descriptive / hypothesis-generating where no credible counterfactual is established**. [SOURCE: [cost analysis](immigration-costs-causal-analysis.md)] [SOURCE: [threshold memo](immigration-threshold-causal-levers-2026-04-21.md)]

59. **Published version and conditioning matter — corrects the literature synthesis behind 19/44.** Ottaviano–Peri's published 2012 headline is +0.6% average natives / −6.7% prior immigrants for 1990–2006; the −19% headline is an earlier draft. Conditional child mobility at the same parental rank is not mechanically explained by lower parental rank. These corrections do not settle all wage effects or prove causal immigrant ancestry effects. Rating: **strong correction to source version and logic**. [SOURCE: [OP published abstract](https://academic.oup.com/jeea/article-abstract/10/1/152/2182016)] [SOURCE: [mobility correction](immigration-dismantle-streets-of-gold-2026-06-25.md)]

60. **A runnable calculation is not automatically a theory test.** The earlier three empirical FAILs included an assumed exit multiplier, an absent innovation tag and an invalid annual fiscal input compared with a different lifetime estimand. The aggregate verified/falsified tally is withdrawn. Rating: **strong re-adjudication; individual empirical questions remain untested**. [SOURCE: [corrected scorecard](immigration-theory-verdicts-2026-06-25.md)]

61. **The Texas native denominator and SPI rate require further concrete corrections — supersedes the local numerical evidence in42.** Light's baseline is already native-born; CMS_nat splits naturalized people from legal immigrants. The old loader subtracted naturalized counts and people twice. Correct2018 violent charges are103.52 versus226.45 per100,000, unauthorized/native, ratio0.4571. The old231.20 comparator is invalid. SPI's official RV0004 changes112 classifications; 100 remain ambiguous. The prior0.86 ratio mixed2016 prisoners with a later population and is withdrawn from context/unified tables and the current export. Counts remain; current-status/race offending is unidentified. Rating: **verified source/code correction; historical recorded-outcome comparison only**. [SOURCE: [conduct audit](immigration-conduct-denominators-2026-09-05.md)]

62. **The broader2024 account preserves the native/Mexico ranking within explicit constructions.** Modeled taxes less selected transfers give a $6,703–$8,969 native-minus-Mexico gap per adult25–64 across allocation/weighting choices. Medical and average-current-school scenarios retain that ordering; the latter makes displayed Mexico balances negative. Omitted taxes/costs, allocation and marginal-cost assumptions prevent a complete fiscal sign. Rating: **reproduced descriptive accounting, conditional scope**. [SOURCE: [fiscal account](immigration-fiscal-account-2024-2026-09-05.md)]

63. **Separate race/ethnicity and nativity are now measured, not inferred from one another.** ACS2019/2024 wage profiles separate native and foreign-born non-Hispanic Black adults, other disjoint groups and Black-any-race sensitivity. BJS2022/2023 race-specific imprisonment rates and SPI2016 joint prisoner composition remain distinct from Texas status rates. No held Texas table supplies race-specific status numerators and denominators. Rating: **verified descriptive strata; causal/race-adjusted status claim unsupported**. [SOURCE: [wages](immigration-wage-race-strata-2026-09-05.md), [crime strata](immigration-crime-race-ethnicity-2026-09-05.md)]

64. **Documented recording failures require sensitivity; they do not identify a universal correction factor.** Casey and Minnesota audits establish specific institutional failures. Missing residents, unobserved status, outcome reporting, classification and filing are separate mechanisms. Texas2018 equality occurs at relative recording intensity0.4571 under equal relative population coverage; that intensity is not estimated. Fiscal one-/two-sided coverage and collection grids are assumptions, not priors for unauthorized people. Rating: **documented failures and exact conditional algebra; national magnitude unidentified**. [SOURCE: [uncertainty analysis](immigration-measurement-uncertainty-2026-09-05.md)]

**Layer 2026-09-16.** Entries 65–75 add the generational, offence-composition and European-registry findings of 2026-09-16. Memo: [Mexican-origin generation and incarceration](immigration-mexican-origin-generation-incarceration-2026-09-16.md); mechanisms: [generational crime mechanisms](immigration-generational-crime-mechanisms-2026-09-16.md).

65. **The "Mexican second generation 3.5× native whites" figure is a 2000 pooled-generation number; it is 1.7–2.1× in 2023 — narrows 48 and the coding-bias entry.** Rumbaut's 5.90% vs 1.71% (men 18–39, 2000 census) pools second and third-plus generations by self-identification. ACS PUMS institutional group quarters give 2.56× (2010), 1.91× (2019), 1.72× (2023) raw, about 2.1× after reallocating generically coded "other Hispanic" prison records. Ethnic attrition biases the self-ID cell upward, ICE detention inflates foreign-born rows. Sensitivity (2026-09-16 audit): the 2023 ACS race redesign (Sabol, Johnson & Lynch 2025) moves the ratio only 3% under a white-alone-or-in-combination denominator (1.719→1.668 in 2023, 1.905→1.848 in 2019), so the convergence stands; 45% of the 2023 incarcerated ACS cell is synthetic on administrative sex/age/race/ethnicity/citizenship (Glassman 2025), which these cross-tabs use and nothing else. Rating: **verified source and re-measurement; robust to the 2023 race-coding break; behavioural interpretation of the residual unidentified**. [SOURCE: memo §1–2; `infra/immigration-fiscal/acs_institutional_2026_09_16/`]

66. **Counting Mexican-Americans as "native" no longer inflates the native crime benchmark.** By the mixture identity, inclusion raises the benchmark only if their rate exceeds other natives'. In 2000 it did (removal: 3.51% → 3.38%); in 2023 US-born Mexican-origin men institutionalize at 1.92% against an all-native 2.05%, and removal moves the benchmark to 2.07%. The first-generation-specific nature of the immigrant advantage stands; the benchmark-inflation argument does not. Rating: **arithmetic on measured cells; strong for 2019–2023**. [SOURCE: memo §3]

67. **Mexican-origin population by generation, 2024: 12.1M / 13.8M / 13.1M (31/35/34%), 39.0M total; third-plus is understated by attrition.** CPS ASEC Table 4; 2005 was 40/31/29. Duncan–Trejo: 17% of third-generation Mexican-ancestry children do not identify as Hispanic, positively selected. Duncan & Trejo 2025 (AEA P&P 115:451–56; IZA DP 17579): second-generation adult attrition is only 2–3%, and intermarriage is 86% of the explained attrition channel, so the 17% does no work at the second generation and the third-plus understatement runs through mixed parentage. Rating: **official survey count; attrition adjustment unquantified here**. [SOURCE: memo §4]

68. **The 2010–2023 convergence in the Mexican-origin/white institutionalization ratio is not California decarceration.** Within California the ratio is flat (2.19× → 2.30×, both groups halved); convergence is in Texas (2.19× → 1.69×) and the other states (2.76× → 1.50×), where white rates fell a third and Mexican-American rates two-thirds; the US-born Mexican population outside CA/TX nearly doubled. Rating: **measured decomposition; drivers (opioid-era white incarceration, new-destination composition) are candidates, not tested**. [SOURCE: memo §7]

69. **Detection technology did not drive the crime decline; the opportunity form of the technology hypothesis has 1990s causal support.** FBI clearance fell (violent 47.5% → 36.7%, 2000–2022; homicide 93% → 54%, 1962–2020), so "cameras and algorithms catch more" fails at the arrest margin. Cell-tower build-out (Edlund–Machado), vehicle immobilizers (Farrell et al.) and DNA databases (Doleac) reduced the profit or risk of street-crime types, with effects concentrated among young Black and Hispanic men. Rating: **clearance trend verified; opportunity mechanisms published quasi-experimental, 1990s–2000s only**. [SOURCE: memo §7]

70. **The 2009–2021 incarceration decline was property and drug for both groups, Hispanics fell faster on every category per capita, and drug possession is 3–5% of prisoners.** On BJS's consistent estimation basis (Prisoners in 2011 restates 2009 Hispanic violent as 159,800, not the 117,800 in the 2010 report; administrative records under-record Hispanic origin by about a quarter), Hispanic per-capita change 2009–2021 is total −40%, violent −22%, property −66%, drug −65%; white −28%, −21%, −46%, −27%. The Hispanic violent share rose 56% → 71% because non-violent stock drained (mean time served 1.8 vs 4.7 years), not because violent stock grew; ageing lowered the Hispanic male rate 6%; Texas, which codes Hispanic origin directly, shows Hispanic per-capita −39% vs white −18%. An earlier same-day reading of a Hispanic violent rise was a basis artefact and is withdrawn. Rating: **official tabulations on a verified consistent basis; behavioural direction is downward convergence**. [SOURCE: memo §8; `infra/immigration-fiscal/hisp_violent_stock_2026_09_16/`]

71. **Europe's origin tables come from population registers, not political will; the US leads on legal status and lags on ancestry.** Register linkage (personal ID, parental birthplace) is what lets Rockwool 2026 run five-country full-population decompositions; the US Census dropped parental birthplace after 1970 and has no register. Texas DPS/DHS fingerprint matching gives the US the only large legal-status crime dataset; Nordic registers do not observe undocumented status. UK MoJ is appealing an ICO order (June–July 2026) to release convictions by nationality. Rating: **structural claim documented; political-valence claims labelled inference**. [SOURCE: memo §9]

72. **In the Rockwool 2026 five-country decomposition the immigrant gap is mostly composition and the descendant gap is not.** About 70% of the non-Western immigrant gap in male convictions (15–30) is own education, employment and income; in Denmark and Norway 2017 the adjusted immigrant gap is negligible; the descendant gap survives at over 200% in Denmark and the Netherlands; New Zealand's non-Western groups convict below the majority; Southeast Asian origin in Denmark matches ethnic Danes since 2007–08 while MENAPT descendants stay about 3× after controls. Rating: **published full-population register study; summaries read, full paper not**. [SOURCE: memo §9; https://en.rockwoolfonden.dk/publications/a-statistical-decomposition-of-nativity-gaps-in-criminal-convictions-using-full-population-data-from-five-developed-democracies/]

73. **The Pueyo European compilation reproduces in ordering but not in its headline magnitudes.** Fifteen of sixteen charts rebuilt from Statistics Denmark, BKA/Destatis, Brå, SSB, INE, ISTAT, Met FOI and Eurostat. Denmark, Sweden, Norway, Spain and Eurostat match to the pixel. Germany's top ratios include immigration-law offences (aggregate 3.38× → 2.78× without them) and non-resident suspects; Norway's chart is Oslo men 15–24 over four years; London's denominators are APS nationality rounded to 1,000 (Afghanistan 11.4× → 2.1× on census country of birth, truth between); Finland does not reproduce; the profiling chart is cumulative conviction prevalence; "Palestine" and "Ex-Yugoslavia" are undisclosed relabellings. Rating: **reproduction verified per chart with scripts; ordering strong, magnitudes source-specific**. [SOURCE: memo §10; `infra/immigration-fiscal/pueyo_repro_2026_09_16/`]

74. **Low-skill origin groups differ sharply on second-generation outcomes, and the ranking is parents' education transmitted at about 0.8 points of BA share per point.** US-born institutionalization 2000 → 2023: Mexican 5.90 → 1.92, Salvadoran/Guatemalan 3.01 → 0.89/1.01, Vietnamese 5.60 → 0.30, Chinese 0.65 → 0.12, Cambodian/Laotian/Hmong 7.26 → 1.35/1.60/0.84 (white 1.71 → 1.12). CPS 2019–24 second-gen BA+ at 25–44: India 85%, China 78%, Vietnam 63%, Philippines 55%, Cuba 48%, Dominican 37%, El Salvador 31%, Guatemala 28%, Mexico 22%; third-plus white 47%. Rating: **descriptive across verified sources; small Asian-detail cells noisy**. [SOURCE: memo §5, §11]

75. **Mexican-American second-generation attainment is what the least-selected large stream predicts; the Vietnamese case is the one unexplained over-performance.** Across 29 parental origins, second-gen BA share on a Feliciano-style selectivity index (first-gen US BA minus origin-country BA) gives R² 0.91, slope 0.81; Mexico's residual is −1.7 points and Mexico is the only large origin with negative selectivity (9.9% vs 17.0%). Vietnam over-performs by 17–26 points; refugee origins as a class do not. The index is only narrowly separable from first-generation education level (origin-country attainment alone has no predictive power). Mechanisms with individual-level identification: parental unauthorized status (1.24 years, IRCA-instrumented, Mexican/Central American only) and parental English (origin-blind); ethnic capital and refugee resettlement have no identified estimate; ethnic attrition biases the Asian–Latino gap upward from both ends but the computed correction is about 0.1 years; family-structure runs the wrong way. Rating: **group-level association verified on CPS with Census benchmarks; individual mechanisms graded B to A− in the literature memo; the Vietnamese residual unexplained**. [SOURCE: memo §11; [mechanisms memo](immigration-secgen-origin-divergence-mechanisms-2026-09-16.md); `infra/immigration-fiscal/secgen_selectivity_2026_09_16/`]

76. **The "partial ledger" caveat on the Mexican second generation does not rescue it: adding employer payroll, sales, property and K-12 widens the gap from −$6,066 to −$8,286 per adult per year.** Same CPS ASEC 2025 generator, baseline reproduced to $0.17; IRS 2024 payroll rates, Tax Foundation 2024 sales rates, ACS 2023 effective property rates, Census FY2024 per-pupil spending. Employer payroll −946, property −548, K-12 −460, sales −266; eight sensitivity arms −8,123 to −8,555; adults-only allocation −10,633. All-origin second generation stays level with third-plus whites (−327, se 488). Residual items priced the same evening (Pell, ACA credits, uncompensated care, CCDF, Head Start, higher-ed appropriations, institutional care): −8,286 → −8,564, and −8,901 charging state and local general services per capita (adults-only allocation −12,374 with federal public goods per capita); no single item exceeds $200 for the Mexican second generation, and institutional care narrows the gap by $48 in the base arm because whites' institutional bill is mostly nursing homes. Still outside: corporate tax incidence, accrued entitlements, general equilibrium; minority contracting preferences are unpriceable to persons. Rating: **measured on the same microdata for payroll and K-12 child counts; sales and property modeled from aggregate rates; sign robust, level partial**. [SOURCE: memo §12; `infra/immigration-fiscal/gen_ledger_extension_2026_09_16/`]

**Main remaining distinction:** An error can be repaired by calculating the correct object or withdrawing the inference it cannot support. Missing identification remains a research limit; it does not license a contrary conclusion or a numerical confidence certificate. Current implementation and verification status is recorded in the [integrated update](immigration-clarity-update-2026-09-05.md).

## Revisions

- **2026-09-05:** Added current corrections 52–60 under the [material inference repair decision](../decisions/2026-09-05-material-inference-repair.md). Historical entry numbers remain available for prior links and provenance.
- **2026-09-05, expanded audit:** Added61–64 after raw crime-codebook verification, broader fiscal accounting and the requested race/measurement splits. The [measurement decision](../decisions/2026-09-05-measurement-and-ledger-boundaries.md) records the additional corrections; historical text remains intact.

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Dated historical confidence ladder — current corrections above govern</summary>

# Immigration confidence ladder

Date: 2026-04-10

Scale:
1. `strong`
2. `medium`
3. `weak`
4. `contextual-only`

Rule:
A metric can be statistically clean and still be only `contextual-only` for the question we are asking.

## Strong

1. `ACS origin / education / recency composition counts`
Rating: `strong`
Reason: these are direct weighted ACS summaries, not inferred fiscal objects. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_origins.sql]

2. `PUMA-level median gross rent as destination cost exposure`
Rating: `strong`
Reason: official ACS geography, directly observed, useful as exposure context. It is not a welfare scalar. [SOURCE: sources/immigration-fiscal/data/derived/extend_immigration_context_with_pumas.sql]

3. `Household-normalized school-age child metrics after WGTP correction`
Rating: `strong`
Reason: the prior proxy was wrong; the corrected household join is materially better and uses the right unit for linked-household child exposure. Do not export this as a current full-stock school-burden-per-adult or origin fiscal-net row; June 2026 tensor work withholds origin school/net rows until the school numerator and federal adult denominator use the same universe. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-school-burden-per-adult-2026-06-15.md]

4. `Claim that the Clark “agree” papers are scope-limited rather than obviously false`
Rating: `strong`
Reason: that conclusion survives repeated paper review and is consistent with the actual paper scopes. [SOURCE: research/immigration-economist-effects-matrix.md]

## Medium

5. `Federal versus state/local incidence split as a research frame`
Rating: `medium`
Reason: official sources strongly support the split, but our own warehouse only partially models the federal side. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

6. `County CHAS housing-stress shares`
Rating: `medium`
Reason: good background stress metric, but not immigrant-attributable marginal burden. [SOURCE: sources/immigration-fiscal/data/derived/build_stage2_incidence_context.py]

7. `State school-spending per pupil as school-pressure context`
Rating: `medium`
Reason: official and clean, but too coarse for marginal burden or district-specific claims. [SOURCE: sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql]

8. `Housing-heavy versus school-heavy origin-group typology`
Rating: `medium`
Reason: useful descriptive shorthand for destination exposure, but still proxy-based and sensitive to geography choice. [SOURCE: research/immigration-local-burden-puma-layer.md]

9. `Descendant upside as a real channel`
Rating: `medium`
Reason: the long-run literature supports it, but sign and magnitude are heterogeneous and horizon-dependent. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] [SOURCE: https://www.nber.org/system/files/working_papers/w33961/w33961.pdf]

## Weak

10. `Area-weighted PUMA-to-county bridge`
Rating: `weak`
Reason: land area is not people, renters, students, or immigrant households. This is a convenience bridge, not a precise exposure model. [SOURCE: sources/immigration-fiscal/data/derived/build_puma_county_crosswalk.py]

11. `IRS county migration balance as burden evidence`
Rating: `weak`
Reason: at best it is contextual mobility climate. It is not immigrant-specific and not causal. [SOURCE: research/immigration-stage2-county-bridge-batch.md]

12. `Old ACS income/benefit proxy origin rankings`
Rating: `weak`
Reason: the April ACS income/benefit shortcut was not a tax-transfer microsimulation. It remains useful only as a weak historical screen, superseded for current narrow federal annual proxy work by the SIPP-style FICA-minus-SNAP/TANF/SSI build. [SOURCE: research/immigration-low-skill-origin-incidence-memo.md] [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md]

13. `Magnitude claims for local school burden from current warehouse`
Rating: `weak`
Reason: district assignment, ELL intensity, migrant composition, and marginal cost are not modeled well enough yet. [SOURCE: research/immigration-adversarial-review.md]

## Contextual-only

14. `County CHAS plus rent plus school-spend combined into one local burden scalar`
Rating: `contextual-only`
Reason: combining context layers does not make a causal burden estimate.

15. `Average citizen better off / worse off`
Rating: `contextual-only`
Reason: too much depends on weights over renters, employers, taxpayers, future descendants, and politics.

16. `Bad for the country`
Rating: `contextual-only`
Reason: without explicit horizon and counterfactuals, the phrase has almost no analytical content.

## Causal-design layer added 2026-04-18

17. `Large Borjas-style native wage gains under observed E-Verify mandates`
Rating: `strong against large gains in this design`
Reason: TWFE on QWI 2003-2023, 9 treated states (AZ, MS, SC, UT, GA, AL, NC, TN, FL), 42 controls. Coefficient on E1 in E-Verify-exposed industries: +0.51% (SE 0.81%, n=16,736); the 95% CI excludes gains above about +2.1%, with MDE roughly 2-3% before compliance sensitivity. This cuts against large Borjas-style magnitudes for the observed static-TWFE mandate margin, while small effects, scaled-shock benchmarks, surge regimes, and heterogeneity-robust staggered-DiD checks remain unresolved. Aligns with Card direction; not a direct replication, clean ATT, or global wage-family rejection. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]

18. `Immigrants concentrate in inelastic-supply MSAs (renter-incidence warning)`
Rating: `strong (descriptive)`
Reason: top FB-share quintile median Saiz 2010 elasticity = 1.51, bottom = 3.40. n=237 MSAs, ACS 2018-22. Implication: rent exposure in inelastic destination markets is a stronger renter-incidence warning than the adversarial review allowed; aggregate welfare loss remains unmeasured. [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

19. `Card-side bounded native-wage-impact evidence for observed low-skill shocks`
Rating: `medium-strong`
Reason: convergent evidence — Card 1990 Mariel, Foged-Peri 2016 Denmark dispersal-policy quasi-experiment, this cycle's E-Verify TWFE 2003-2023 — points against large native low-skill wage losses/gains in these designs. This is a cross-design external-validity pattern, not one pooled U.S. estimate. It does not identify one shared complementarity mechanism. Borjas 2017 restricted-Mariel magnitude should not be mechanically extrapolated to broader staggered designs. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md, multiple papers]

## Paradigm-escape layer added 2026-04-18 (evening)

20. `Saiz elasticity-immigrant correlation is stronger for regulatory index than topographic unavailability` — **QUALIFIED by entry 38**
Rating: `strong descriptive`
Reason: log(FB share) ~ unaval (β=+0.12, t=0.58, n.s.) + WRLURI (β=+0.33, t=6.29***) + log_pop. WRLURI is the stronger correlate in this cross-section; this does not identify zoning as the causal driver or prove zoning reform would reduce immigrant renter burden. Treat zoning reform as a plausible policy hypothesis, not a verified lever. [SOURCE: scripts/saiz_decomposition.py]

21. `Sanctuary policy variation shows no statistically significant E1 QWI wage change`
Rating: `no significant E1 wage change observed in this design`
Reason: TWFE on QWI 2003-2023 with 12 pro-sanctuary + 9 anti-sanctuary states; all E1 specifications |t|<1.0. This is an additional QWI policy-margin check consistent with the bounded Card-side reading for observed marginal policy variation, but it is not an equivalence-tested zero. [SOURCE: scripts/analyze_sanctuary_wages.py]

22. `Domestic newcomer counts are much larger than moved-from-abroad counts at median county`
Rating: `medium`
Reason: IRS SOI `Total Migration-US` 2022-23 and ACS `B07001_081E` point in the same descriptive direction, but they are not like-for-like universes. The current median county comparison is roughly `4.59%` vs `0.21%`, with a ratio of medians around `21.7x` and a median county-level ratio around `20.5x`, so the safe claim is order-of-magnitude disparity, not a precise burden ratio. [SOURCE: research/immigration-causal-internal-vs-immigrant-newcomers.md]

23. `Open-borders welfare verdict is welfare-weight-sensitive under current empirical inputs` — **QUALIFIED by entry 39**
Rating: `strong (framing claim)`
Reason: At immigrant-welfare-weight w=0 (current repo's implicit framing): negative by construction. At w≥0.25 under 25%-of-gross-gains native-cost benchmark: positive. At w=1.0 even under harsh 50%-cost benchmark: positive. Empirical evidence cannot choose the value weight, but native-cost, fiscal, housing/capacity, and sending-country inputs can move break-even thresholds. Honest framing must name both the weight and the empirical calibration. [SOURCE: data/clemens/gpt54_calibration_review.md, GPT-5.4 sensitivity analysis]

24. `Mass deportation of 7M unauthorized → ~$1.45T first-order output shock (~5% GDP); Type-II endpoint is sensitivity only` — **presentation qualified by entry 32**
Rating: `medium (calibration not estimate)`
Reason: BEA Use Table 2023 partial-equilibrium with industry FB-share assumptions from Pew/CMS. First-order $1.45T; a Type-II multiplier (~1.6) gives a $2.32T sensitivity, not a headline estimate. Per-removed-worker loss $207K first-order and $332K under Type-II sensitivity. Most affected: Construction (-5.9%), Other services / cleaning (-8.8%), Agriculture (-4.3%). The E-Verify employment result is, at most, a weak plausibility check for employment response under one marginal enforcement setting; it does not validate the mass-deportation calibration or its industry loss magnitudes. [SOURCE: scripts/mass_deportation_sim.py] [SOURCE: research/immigration-causal-everify-card-vs-borjas.md]

## Surge layer added 2026-04-18 (late evening)

25. `Title 42 lift timing did not match surge onset; surge was a regime shift starting Dec 2022` — **EVIDENCE SUPERSEDED by entry 35**
Rating: `medium`
Reason: SWB encounters peaked Jan-Mar 2023 at 50K+/month BEFORE Title 42 lift (May 2023). Lift coincided with April-May lull, then gradual rebuild to surge levels. Pre/post comparison is composition-driven, not policy-causal. [SOURCE: research/immigration-causal-surge-2021-2024.md]

26. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
Rating: `strong`
Reason: TWFE β=+3.29 (t=4.78) on CHNV nationality vs control after Jan 2023. Encounters from CHNV nationalities ROSE 787% post-program, not fell. Refutes the stated rationale that legal pathway would reduce irregular migration. [SOURCE: data/cbp/swb_encounters_by_citizenship_monthly.parquet]

27. `Receiver-city local fiscal load was real and concentrated` — **scope qualified by entry 33**
Rating: `strong (administrative data)`
Reason: NYC FY24 $3.7B (3.5% of operating budget); MA FY24 $1B; Chicago $228M peak; Denver $89M (with cuts to other services). Combined ~$5B+/yr peak across major receivers. Receiver-load stress has empirical bite, but these are gross outlays; entry 33 supplies the net-burden caveat. [SOURCE: data/bused_cities/receiver_city_costs.csv]

28. `Receiver cities swung +4.41 pp more Republican in 2024 than comparable non-receivers` — **QUALIFIED by entries 31 and 36; final causal-implausibility sentence superseded**
Rating: `medium (correlation, multiple confounders)`
Reason: Multivariate OLS with state FE: receiver_city β=+0.024 (t=6.96***). Top receivers (Bronx +11pp, Queens +11pp, Hidalgo +10pp, Cameron +10pp, El Paso +10pp, Miami-Dade +9pp) swung massively toward Trump. Confounders include national Hispanic realignment, inflation, and policy-endogenous busing destinations. Magnitude implausibly large for non-immigration causes alone. **Do not reuse the final sentence; entries 31 and 36 supersede it with the controlled +2.4pp upper-bound framing.** [SOURCE: research/immigration-causal-surge-2021-2024.md]

29. `Static-cycle Card-side wage finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation`
Rating: `meta-update on prior entries 17, 19, 21`
Reason: Prior entries over-compressed the E-Verify/sanctuary wage results as a "decisive Card-side win for U.S. policy variation." The safer reading is strong Card-side evidence for observed 2008-2021 marginal policy variation. The 2021-2024 surge is a regime shift outside that variation. Linear extrapolation is not warranted. Surge-period wage estimates remain to be done (require ACS PUMS 2023). [SOURCE: research/immigration-causal-surge-2021-2024.md]

## Bias-audit layer added 2026-06-11

Trigger: mirror-test against the criticisms of the Cato 2026 fiscal study ("did we commit its biases?"). Full audit and the general checklist live in [notes/quant-bias-checklist.md](../notes/quant-bias-checklist.md). Prior entries are not rewritten (append-only); these supersede where they conflict.

30. `CHNV parole did not substitute legal flow for illegal flow; it added on top` — **INVALIDATED by entry 34; historical only, do not quote**
Reason: interim downgrade before the OHSS parser correction. The source memo itself listed reverse causation as a live mechanism, but entry 34 later reversed the descriptive reading too: the "+787%" rise was the program's lawful OFO channel on a scrambled clock, while corrected USBP between-port crossings fell sharply. Do not reuse the "substitution did not happen" language or the `+787%` figure except as an error trace. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]

31. `Receiver-city 2024 GOP swing` (entry 28) — **grade unchanged (medium), headline language corrected**
The phrase "magnitude implausibly large for non-immigration causes alone" is a plausibility assertion doing causal work and should not be reused. The top swing counties (Bronx, Queens, Miami-Dade, Hidalgo, El Paso) are among the most Hispanic-populous counties in the country; the national 2024 Hispanic realignment is near-collinear with "receiver city" in that list, and the multivariate pass controls FB share but not Hispanic share. Entry 36 later runs this Hispanic-share control and keeps the controlled estimate at about +2.4pp; use entry 36 for the current scoped reading rather than the raw +4.41pp gap or the stale open-work framing. [SOURCE: research/immigration-causal-surge-2021-2024.md] [SOURCE: notes/quant-bias-checklist.md item 25]

32. `Mass deportation output shock` (entry 24) — **grade unchanged (medium, calibration), presentation rule added**
Lead with the first-order figure (`~$1.45T`, ~5% GDP); the `$2.32T` Type-II-multiplier endpoint appears only as labeled sensitivity, never inside a headline range. Stacking the modeled amplifier into the headline is the same move as Cato's `$3.9T` interest-savings add-on (27% of their `$14.5T`), in the opposite political direction. The calibration also freezes replacement hiring, wage response, and capital reallocation at zero — state this when quoting. [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] [SOURCE: notes/quant-bias-checklist.md items 4, 15]

33. `Receiver-city fiscal load` (entry 27) — **grade unchanged (strong, administrative data), scope annotation**
The figures are **gross city outlays**, not net burden: federal Shelter and Services Program reimbursements and the counterfactual baseline growth of homeless-services spending are not netted out. "NYC spent $3.7B in FY24" is strong; "the surge cost NYC $3.7B net" is not yet supported. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv] [SOURCE: notes/quant-bias-checklist.md item 10]

## Data-correction layer added 2026-06-11 (evening)

Trigger: the morning layer's two open kill-tests were run against local data and exposed two bugs in the OHSS encounter parser (fiscal-index dates; agency-block overwrite that made the series OFO-ports-only). Full trace: [decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md](../decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md). These entries supersede 25, 26, and 30 where they conflict.

34. `CHNV substituted lawful port flow for irregular crossings in its initial year` — **reversal of entry 26**
Rating: `strong (initial period); medium beyond ~12 months`
Reason: corrected USBP (between-ports) event study with staggered dates and flat pre-trends: Cuba −95.3%, Nicaragua −96.2%, Venezuela −57.5% (initial, decaying by τ+11 — Darién rebound), Haiti structurally ~0 between ports. Mean τ[0,+3] = −2.17 log points. The old "+787% — added on top" figure was the program's own lawful OFO channel on a scrambled clock; corrected total-CBP DiD is null (β=+0.45, t=1.29). Ledger discipline: lawful parole inflow (~530K) still lands in receiver cities — substitution-of-channel, not reduction-of-arrivals. [SOURCE: sources/immigration-causal/data/outcomes/analysis/chnv_pretrends/results.json]

35. `Corrected timing does not support Title 42 lift as proximate surge onset` — **replaces entry 25 evidence and narrows conclusion**
Rating: `medium`
Reason: the entry's timing facts were artifacts. Corrected series: Dec-2022 local peak 252K → Jan-Feb 2023 trough (CHNV substitution visible) → April-May 2023 anticipation spike (212K/207K) → June post-lift crash (−30%) → Dec 2023 record 301,980. Post-lift 6-month mean −14.5% vs pre-lift. This timing result refutes the old simple post-lift jump story, not every possible Title 42 effect through anticipation, routing, composition, or later-equilibrium channels. [SOURCE: scripts/analyze_surge_title42_chnv.py rerun 2026-06-11]

36. `Receiver-city 2024 GOP swing survives the Hispanic-realignment control` — **closes entry 31's open work**
Rating: `medium (correlation; robust to the named rival channel)`
Reason: pre-registered kill-test with 2020 county Hispanic share (popest baseline): receiver β +0.0256 → +0.0238 (t≈7.2) with the control in; Hispanic share itself β=+0.062 (t=17.2); within top-Hispanic-quintile, receivers +4.3pp raw vs comparable counties. Hispanic-share robustness gate passed. Still cross-sectional; busing destinations policy-endogenous; use the controlled +2.4pp. [SOURCE: sources/immigration-causal/data/outcomes/analysis/swing_hispanic_control/results.json]

37. `OHSS-derived series require an external-anchor check before regression`
Rating: `strong (process rule)`
Reason: one known published value per series (e.g., Dec 2023 = 302K) would have caught both bugs at build time; the bugs survived 7 weeks and three ladder entries because year-boundary cuts masked them. [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md]

38. `Saiz WRLURI result is descriptive, not identified zoning causation` — **scope correction to entry 20**
Rating: `strong descriptive regression; causal lever unverified`
Reason: WRLURI is a much stronger correlate of foreign-born share than topographic unavailability in the Saiz decomposition, but the cross-section does not prove that zoning causes immigrant concentration, that zoning reform would reduce immigrant renter burden, or that immigration restriction is dominated as a policy response. Treat zoning reform as a plausible policy hypothesis pending panel/IV evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: research/immigration-causal-saiz-elasticity-rent.md]

39. `Open-borders verdict has a normative weight and empirical-input components`
Rating: `strong framing correction`
Reason: The immigrant-welfare weight is a value parameter; empirical evidence cannot choose it. But native-cost benchmarks, fiscal ledgers, housing/capacity constraints, and sending-country effects remain empirical inputs that can move scenario break-evens. Treat entry 23 as a weight-sensitivity claim under the then-current GPT-5.4/Clemens calibration, not as a reason to stop collecting cost or feasibility evidence. [SOURCE: research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md] [SOURCE: data/clemens/gpt54_calibration_review.md]

40. `E-Verify employment does not validate mass-deportation calibration`
Rating: `strong scope correction`
Reason: E-Verify observed mandate variation is a marginal enforcement design with partial compliance and QWI W-2 measurement. The BEA mass-deportation run is a partial-equilibrium calibration that freezes replacement hiring, wage response, and capital reallocation. Similar directional employment pressure is not validation of the calibration's national shock size or industry-loss magnitudes. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py]

## Fiscal-tensor layer added 2026-06-16

41. `SIPP-style federal annual proxy is a narrow cash-flow layer, not all-in federal liability`
Rating: `medium-strong descriptive for the named ledger; weak for all-in federal`
Reason: the current built proxy estimates annual payroll/FICA minus SNAP, TANF, and SSI by origin/education cells. It is materially stronger than the old ACS income/benefit shortcut for that ledger, but it omits income tax, Medicare/Medicaid, EITC mechanics, capital/corporate tax, household filing, and lifetime NPV. Mexico-origin adults are about `$1,519` per adult per year and NH white US-born adults about `$2,746` on this narrow proxy; those figures must not be laundered into all-federal or all-government net claims. [SOURCE: research/immigration-federal-distribution-findings-2026-06-15.md] [SOURCE: research/immigration-country-fiscal-tensor-2026-06-15.md]

## Crime layer added 2026-06-24 (data now in-warehouse, no longer literature-only)

42. `Immigrants are NOT higher-crime than native-born — DIRECTION robust; MAGNITUDE and GENERALIZATION are NOT`
Rating: `DIRECTION strong; MAGNITUDE + GENERALIZATION weak (comparison-group, origin, detection caveats)`
Reason: The DIRECTION (immigrants do not out-offend natives) is strong — Light TX arrests **and** convictions, both CMS/Pew denominators, plus SPI incarceration (`0.86×`), all surviving the adversarial pass. Raw 2018 violent gradient /100k (`crime_tx_arrests_by_status`, denom `CMS_nat`): undocumented `104` < naturalized `170` < legal `193` < native-born `231`. BUT the MAGNITUDE (undoc ≈`0.45×` native) and GENERALIZATION are **not** robust: **(a) comparison-group composition** — splitting naturalized out of "citizen" barely moves it (native-born 231 vs all-citizen 226), but the native group is *racially* heterogeneous; a race-matched comparison (vs non-Hispanic-white native) roughly **halves** the violent gap (~50%→~25-30%, Cato PA994) — Light has no race-by-citizenship, so it's flagged not removed. **(b) origin mix** — the undocumented group is majority **Mexican** (TX-heavy); may be favorably selected, not generalizable to all LATAM / all low-skill. **(c) detection bias** — arrest/incarceration data measures *detected* crime; differential reporting/detection by status biases it (direction contested). **Use the sign, not the multiplier; don't extrapolate past TX-Mexican-heavy.** [SOURCE: `crime_tx_arrests_by_status`, openICPSR 124923] [SOURCE: `crime_spi_incarceration_rate`, ICPSR 37692]

43. `SCAAP measures criminal-alien custody/reimbursement, NOT offending or cost`
Rating: `strong as a custody-stock signal; must NOT be read as a crime rate or a cost`
Reason: `crime_scaap_state_2023` is a participating-jurisdictions-only floor — DHS-confirmed criminal-alien inmate-days (7.8M FY23; CA+TX dominate) and DOJ reimbursement ($210M). Inmate-days are a custody STOCK with no population denominator (not a rate); reimbursement $ is a fraction of actual cost. State-concentration signal only. [SOURCE: `crime_scaap_state_2023`; `v_crime_scaap_x_state_fiscal`]

## Frontier-expansion layer added 2026-06-25 (5-domain research+acquisition pass)

Trigger: parallel sociology / urbanism / policy / economics-disconfirmer / crime scout pass (see [research/immigration-research-coverage-matrix-2026-06-25.md](immigration-research-coverage-matrix-2026-06-25.md)). Every load-bearing citation below was primary-verified (`resolve_doi` exact match; effect sizes from fetched full text). **Instrument-bias flag (mandatory): every entry here moves credence toward "less costly/harmful than the restrictionist prior," which is the documented direction of the LLM instrument's tilt — they were therefore held to a primary-source bar, and each carries its disconfirming caveat. Append-only; these supersede/qualify prior entries where noted.**

44. `The Mariel "10-30% low-skill wage harm" is artifact-fragile` — **sharpens entries 19, 29**
Rating: `the large-harm reading is contested-likely-artifact; the question is not closed`
Reason: Clemens-Hunt 2019 (ILR, full text) shows Borjas 2017's 10-30% decline survives only under a 4-way knife-cut (non-Hispanic men 25-59, dropouts) that discards 91% of low-skill Miami workers, leaving **~17 obs/yr**, and rides a **55pp black-share jump** (1980 Haitian-refugee arrival + a March-1981 CPS sampling-frame change); a schooling-as-outcome falsification (boatlift spuriously "causes" −0.444 yr) confirms compositional contamination. Broadened sample → effect ≈ zero; Peri-Yasenov synthetic control agrees (~null). Borjas 2019 "Role of Race" rebuttal kept as **live counter** — weight moved against the large effect, but the profession has not formally closed it. Does NOT refute the broader CES/Borjas national framework — removes Mariel as a *strong* datum for large low-skill harm. [SOURCE: 10.3386/w23433] [SOURCE: 10.3386/w21588] [SOURCE: 10.3368/jhr.54.2.0217.8561R1]

45. `The static NAS per-capita net-cost is an UPPER BOUND on cost; GE complementarity shrinks/flips it`
Rating: `medium-strong (published GE model); sign-flip is scenario-dependent, not universal`
Reason: Colas-Sachs 2024 (AEJ:Policy, full text) — one average low-skilled immigrant generates an **indirect fiscal benefit ≈ $750/yr** (WP range $770-2,100), of the same order as the direct fiscal cost and opposite sign, via raising complementary native high-skill wages/labor-supply → natives pay more tax — a channel the static NAS per-capita accounting omits by construction. Flips the total to surplus in NAS's more optimistic scenarios, shrinks the cost in all. CAVEAT: does NOT flip in every scenario; the residual net-negative concentrates in state/local education (a federalism-allocation effect, see entry 46). [SOURCE: 10.1257/pol.20220176]

46. `The realized 2021-2026 immigration surge is fiscally POSITIVE at the federal level` — **extends entry 5's split frame to a magnitude**
Rating: `strong (CBO, the official nonpartisan scorekeeper); FEDERAL ledger only`
Reason: CBO 2024 (pub 60165): the surge (net +8.7M above baseline) **lowers federal deficits ≈ $0.9T over 2024-2034** (+$1.2T revenue vs +$0.3T spending+interest), boosts cumulative GDP +$8.9T; ~$285B of the deficit reduction is the GE/economy-wide channel (echoes entry 45 at national-accounts scale). CAVEAT [FRAMING-SENSITIVE]: FEDERAL only — CBO explicitly excludes state/local budgets, where NAS finds the cost concentrates (education). Federal-positive and state/local-negative are different ledgers, not a contradiction; the aggregate depends on the federalism split. [SOURCE: https://www.cbo.gov/publication/60165]

47. `Fiscal sign = f(welfare generosity × cohort participation/skill), NOT a constant of low-skill immigration`
Rating: `medium (reframing, two-bracket evidence)`
Reason: Dustmann-Frattini 2014 (Economic Journal, full text) — recent UK EEA immigrants (2001-2011) paid **34% more than they took out** (+£22.1bn) precisely while natives ran −11%; non-EEA ≈ native ≈ negative. Brackets against Hansen-Schultz-Nielsen-Tranæs (DK, corpus): generous welfare + non-Western low-skill → net-negative even with descendants. The pair establishes the sign is regime- and composition-specific; retire any framing that treats low-skill immigration as fiscally negative *by nature*. CAVEAT: the UK-positive result is concentrated in high-participation EEA migrants — composition is doing the work, transfer to a differently-composed US inflow is conditional. [SOURCE: 10.1111/ecoj.12181]

48. `Immigrant-low-crime finding holds on conviction margin, but is FIRST-GEN and AUTHORIZED-carried` — **sharpens entry 42**
Rating: `DIRECTION strong (now incl. convictions); but documentation-status-heterogeneous + generationally-decaying`
Reason: Conviction-margin UPGRADE — Cato/Nowrasteh TX 2013-2022 (TX DPS conviction counts, the same primary data as Light): illegal-immigrant homicide-conviction rate 2.2 vs 3.0/100k native (**−26%**), homicide being near-fully-reported and detection-resistant; closes the "arrests ≠ guilt" objection [FRAMING-SENSITIVE: cite TX DPS counts, attribute Cato's rate framing]. New CAVEATS that bound generalization: (a) **documentation-status heterogeneity** — NIJ/RTI 2024 synthetic-population finds UNAUTHORIZED share is a NULL ecological arrest predictor once controlled; the protective signal is carried by AUTHORIZED immigrants (undocumented ≈ null, not negative, ecologically). (b) **generational decay** — first-gen advantage shrinks toward native rates by the 2nd generation (RTI 2024; El Paso acculturation). (c) the one reversing study (Lott AZ +142%) rests on a status-variable coding error AZ DOC itself confirms. Marie-Pinotti 2024 (JEP) reconciles EU offender-overrepresentation with null causal rate effect. [SOURCE: 10.1257/jep.38.1.181] [SOURCE: Cato PA 2013-2022 TX convictions] [SOURCE: NIJ 310356]

49. `Legalization REDUCES crime via the labor-market (jobs) channel; enforcement ≈ NULL on crime` — new causal layer
Rating: `medium-strong (multiple quasi-experiments converge); mechanism-contingent`
Reason: A coherent causal literature the corpus lacked. Legalization↓crime: Baker (IRCA, −3-5%, property) [SOURCE: 10.1257/aer.p20151041]; Pinotti (Italy click-day RD, halves serious crime — best-identified) [SOURCE: 10.1257/aer.20150355]; Freedman-Owens-Bohn (IRCA's dual structure — job access ↑ for legalized → crime↓, but employer-sanctions side cut job access for recent arrivals → crime↑) [SOURCE: 10.1257/pol.20150165]. Enforcement≈null on crime: Miles-Cox Secure Communities (landmark) [SOURCE: 10.1086/680935]; Hausman sanctuary (no crime effect). CAVEAT (cuts against a naive pro-legalization read): the channel is JOBS, not legal status per se — a legalization without real labor-market access, or enforcement that strips work access, can be *criminogenic* (Freedman-Owens-Bohn). US evidence rests largely on IRCA 1986; external validity to a future, differently-composed legalization is open.

50. `Immigrant inflow has a CAUSAL but secondary housing-cost effect, concentrated in inelastic/high-regulation metros` — **supplies the magnitude entries 18, 20, 38 lacked**
Rating: `medium-strong (first causal post-2020 estimate); real but a minority share of recent housing inflation`
Reason: Wilson & Zhou 2026 (Dallas Fed WP2607, full text, byline primary-verified) — unauthorized inflow = 1% of initial employment → **+2.2% house prices, +1.4% rents**, with supply/permit response statistically null (confirming the inelastic-supply mechanism entry 18 could only infer); explains ~30% of house-price / ~20% of rent growth in the average MSA over the boom; magnitudes ≈ Saiz (2007). CAVEATS (disconfirmation, weighted higher): timing/geography don't line up at the aggregate (Harvard JCHS, Yale Budget Lab — rents surged 2021 when inflows were modest); aggregate contribution small (Cabral-Steingress ~1.3% of a 17% rise); sign can flip negative where high-income natives out-migrate (Sá UK). The binding policy variable on both the rent cost AND the foregone agglomeration benefit is housing-supply elasticity/regulation (Hsieh-Moretti), not immigration per se. [SOURCE: 10.24149/wp2607] [SOURCE: corpus W3121954821 Saiz 2007]

51. `The data-CAPTURE is itself biased: classification confounds deflate the crime-advantage magnitude and hide its first-gen-only nature` — **sharpens entry 48 (operator-raised 2026-06-25)**
Rating: `direction survives; MAGNITUDE overstated + advantage is first-generation-only — a real, largely-unmeasured confound`
Reason: Two coding-level (not analysis-level) biases in the source data. **(a) Hispanic→"white" miscoding** (UCR/state systems fold Hispanics into "white") inflates the native/white comparator — bites the race-matched comparison (already deflated, entry 42/Cato PA994 ~halves the gap), less the status comparison. **(b) 2nd-generation coded as "native"** (birthright citizenship is structural): the US-born children of immigrants are filed under "native"/"citizen" in EVERY nativity dataset. This is **direction-dependent** — for CRIME it inflates the native baseline (2nd-gen converge/exceed 3rd+-gen, RTI 2024) so the 1st-gen advantage is **overstated and first-gen-specific, not persistent**; for FISCAL it credits the 2nd-gen upside (Abramitzky mobility) to "native," **understating** the immigrant dynastic contribution. The pro-immigration case exploits the asymmetry — first-gen framing for crime, dynastic framing for fiscal (coordinate-switching at the generational level). **Bound:** likely does NOT reverse the crime direction (selection + deportation-deterrence; homicide convictions are detection-resistant) but deflates magnitude. Light-TX has no generation variable → **unaddressable in current crime data**; the pending CPS 2nd-gen test (`load_cps_second_gen.py`, parental-birthplace-keyed) is what settles it. [SOURCE: operator instrument-skepticism; RTI/NIJ 310356 2024; entry 48]

## Two weakest assumptions

1. `Federal-side proxy ledger`
Current state: the old shortcut inferred federal incidence from ACS income plus selected benefit flags; the current built proxy improves this to a SIPP-style annual FICA-minus-SNAP/TANF/SSI ledger.
Why weak: even the current proxy omits income tax, Medicare/Medicaid, EITC mechanics, capital/corporate tax, household filing, and lifetime NPV.

2. `Coarse local burden bridge`
Current shortcut: state school-spend plus PUMA rent plus area-weighted county overlays.
Why weak: local service burden depends on actual district context, renter mix, crowding, tract population, and school-age distribution, not land area.

## Practical reading rule

If a conclusion depends mainly on items `10` through `16`, present it as a hypothesis or descriptive tendency, not a settled result. If it depends on item `41`, name the exact federal cash-flow ledger and do not combine it with origin school rows until the school numerator and adult denominator use the same universe.

<!-- knowledge-index
generated: 2026-06-16T12:05:35Z
hash: manual-june-ds-refresh

cross_refs: research/immigration-adversarial-review.md, research/immigration-causal-everify-card-vs-borjas.md, research/immigration-causal-internal-vs-immigrant-newcomers.md, research/immigration-causal-saiz-elasticity-rent.md, research/immigration-causal-surge-2021-2024.md, research/immigration-economist-effects-matrix.md, research/immigration-federal-distribution-findings-2026-06-15.md, research/immigration-household-weighted-correction.md, research/immigration-local-burden-puma-layer.md, research/immigration-low-skill-origin-incidence-memo.md, research/immigration-school-burden-per-adult-2026-06-15.md, research/immigration-stage2-county-bridge-batch.md

end-knowledge-index -->

</details>
