# Which Latin American origin groups approach an established-native benchmark?

**Finding, September 17, 2026:** Yes, several observed groups have economic point estimates close to, or above, the stated benchmark. Cuban-parent US-born adults are a particularly useful example, including those with **two Cuba-born parents**. Colombian-, Ecuadorian- and Peruvian-parent groups also approach the benchmark on pooled mean earnings, although parent composition and sex matter. These are descriptive economic findings with substantial small-country uncertainty. **No country clears the prespecified, conservative all-four-outcomes noninferiority test after correcting the 20-country search.** That means precise joint parity is unestablished, not that every country is inferior. [MEASUREMENT + INFERENCE; reproducible sources and outputs below.]

The regional average is a different statement: the measured LATAM G2 aggregate has lower education and earnings than either native-parent benchmark. The evidence supports that aggregate description and substantial country heterogeneity simultaneously. It does not support a blanket country-by-country disadvantage, a civilizational ranking, or a genetic explanation. [MEASUREMENT + SCOPE]

## Data actually added and analyzed

Acquired the complete **CPS ASEC 2022 and 2023** public releases, including household/family/person files, full and 160 replicate person weights, dictionaries and weighting instructions. Reused the complete 2024–2026 releases. The combined files contain **719,984 person-period records**, including children and other people outside the analysis population; they are not 719,984 independent adults. Income refers to 2021–2025, preceding the survey year. [SOURCE: [2022 Census release](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.2022.html), [2023 official files](https://www2.census.gov/programs-surveys/cps/datasets/2023/march/), [2026 release](https://www.census.gov/data/datasets/time-series/demo/cps/cps-asec.2026.html); [acquisition and analysis code](../infra/immigration-fiscal/latam_comparison_2026_09_17/README.md), `derived/audit.json`.]

Also acquired **five Opportunity Insights aggregate data tables**, seven OI codebooks and the official release inventory. These add explicit native-mother household-income context, income-rank crosswalks, and broader race/cohort outcomes. A LAPOP US2019 codebook was acquired and rejected for this question because it lacks the required detailed origin and parental birthplace. Total new downloaded source files: **20, totaling 311,488,918 bytes**; seven are data releases/tables, the remainder documentation/inventory. No paid or restricted microdata were obtained. [SOURCE: lane `_cache/acquisition.json`, `_cache/oi/manifest.json`, `_cache/social/manifest.json`; [dataset register](immigration-dataset-register.md).]

The CPS person-to-replicate join is within year on household sequence/person position, with one-to-one coverage and weight-unit checks. Country/year/outcome definitions can harmonize grouped findings across studies; they **cannot join CPS respondents to OI, Pew, GSS or NLS people**. OI race/geography crime outcomes cannot be pasted onto country-income rows. [MEASUREMENT]

## Comparison definitions

The main benchmark is **US-born, non-Hispanic white-alone adults with both parents born in the United States**. The alternative includes **all US-born adults with two US-born parents**, irrespective of race or Hispanic identification. Country code 57 defines US birth; the broader CPS-native/territory definition is a separate sensitivity. These definitions were made explicit while the user's intended meaning of “bio-Americans” remained unconfirmed. They do not establish grandparents, genetic ancestry, or the absence of any distant immigrant ancestry. [SOURCE: CPS dictionaries; FRAMING-SENSITIVE benchmark choice.]

G1 means foreign-born citizens/noncitizens born in each named country. G2 means US-born with **at least one parent born in that country**. No Hispanic self-identification requirement is imposed on the country groups, so Brazilian/Haitian origins and G2 people who do not identify as Hispanic remain eligible. Mixed foreign-parent origins appear in both relevant country rows but once in the LATAM aggregate. Unknown parent birthplaces never become “US-born.” [MEASUREMENT]

Primary population: civilian household adults **25–54**, excluding institutional residents. All groups are standardized to the same fixed 2025 main-benchmark age/sex distribution. Earnings are gross personal annual earnings per adult, including nonworkers, zeros and valid losses, in 2025 dollars using the official BLS CPI-U annual series. Employment is current employment/population; official poverty uses `PERLIS==1` among `POV_UNIV==1`. These are distinct windows and denominators, not net fiscal contributions. [SOURCE: CPS dictionaries and held BLS series `CUUR0000SA0`; MEASUREMENT.]

The dollar conversion corrects national inflation over time, not regional living costs. State/city composition, imputed or disclosure-protected income, household resources and taxes can still affect the interpretation. We do not adjust away education because its observed distribution is one of the outcomes being compared. [METHOD / SCOPE]

## Main country results

**Point estimates**, CPS ASEC 2022–2026, standardized ages 25–54. Except the reference rows, these are US-born adults with at least one named-country-born parent. The complete fixed 20-country roster, both generations, counts and earnings intervals are in [generated results](../infra/immigration-fiscal/latam_comparison_2026_09_17/derived/RESULTS.md); [all-outcome intervals](../infra/immigration-fiscal/latam_comparison_2026_09_17/derived/contrasts.csv) and [figure](../infra/immigration-fiscal/latam_comparison_2026_09_17/derived/second_generation_comparison.pdf) show uncertainty rather than only these point estimates.

| Group | Sample records | BA+ | Employed | Poverty | Mean annual earnings | Earnings / main benchmark, conservative 95% interval |
|---|---:|---:|---:|---:|---:|---:|
| Main white US-parent benchmark | 138,701 | 46.9% | 82.6% | 6.6% | $74,435 | 1.00 by definition |
| All-race US-parent benchmark | 184,895 | 42.4% | 81.0% | 8.4% | $69,389 | 0.93 [0.92, 0.94] |
| Cuban parent | 637 | 52.7% | 81.3% | 5.5% | $87,839 | 1.18 [0.83, 1.53] |
| Colombian parent | 383 | 52.3% | 85.6% | 5.5% | $71,377 | 0.96 [0.69, 1.22] |
| Ecuadorian parent | 223 | 45.8% | 88.9% | 6.7% | $75,251 | 1.01 [0.65, 1.37] |
| Peruvian parent | 262 | 58.5% | 82.0% | 9.6% | $71,563 | 0.96 [0.59, 1.34] |
| Argentine parent | 124 | 58.9% | 83.8% | 1.3% | $87,623 | 1.18 [0.67, 1.68] |
| Brazilian parent | 110 | 63.4% | 80.7% | 5.7% | $67,086 | 0.90 [0.63, 1.17] |
| Haitian parent | 261 | 51.9% | 79.4% | 7.6% | $54,426 | 0.73 [0.52, 0.95] |
| Mexican parent | 10,525 | 24.4% | 79.0% | 9.7% | $53,267 | 0.72 [0.66, 0.77] |
| LATAM G2 aggregate, no double counting | 14,539 | 31.1% | 79.8% | 8.9% | $58,764 | 0.79 [0.73, 0.84] |

Source: `derived/levels.csv` and `contrasts.csv`, regenerated by `analyze.py`; percentages are survey-weighted, sample counts are not. Adjacent years repeat some respondents: the Cuban row contains 486 distinct exact IDs, Colombian 297, Ecuadorian 166, Peruvian 198 and Mexican 7,897. Distinct IDs are an overlap diagnostic, not longitudinal survey weights. The selected rows above illustrate the question; unfavorable and suppressed countries remain in the complete roster. [MEASUREMENT]

**What is comparatively secure:** the Mexican-parent G2 education and earnings gaps are large and precisely separated from the white benchmark: BA gap −22.45 percentage points, conservative 95% interval −24.83 to −20.08; earnings ratio 0.716, interval 0.658–0.773. Changing to the all-race native-parent benchmark reduces the point earnings gap from about 28% to 23%. This is a current population difference, not a causal estimate of what immigration does to incumbents. [MEASUREMENT + SCOPE]

**What is promising but less precise:** the Cuban, Colombian, Ecuadorian and Peruvian pooled earnings estimates are near or above the benchmark. Standardized weighted medians also approach it: $58,112, $58,304, $57,055 and $55,000, respectively, versus $56,447 for the benchmark. These median diagnostics do not have design confidence intervals. Thus the mean comparison is not merely a single spectacular earner: for Cuba the largest individual record supplies 3.7% of weighted earnings, and capping each group's upper tail at its own weighted 99th percentile leaves mean earnings about 117% of the similarly capped benchmark. [MEASUREMENT; `derived/earnings_tail_diagnostics.csv`.]

**A useful disconfirmation:** Haitian-parent G2 adults have estimated BA attainment above the benchmark but appreciably lower earnings, particularly among men. Schooling alone is not an adequate substitute for economic outcomes. Smaller Argentine/Brazilian/Venezuelan descendant cells look favorable on some estimates, but their sample sizes and sparse age/sex cells make them poor headline proof. Costa Rican and Uruguayan descendant mean earnings are especially sensitive to individual records, which contribute about 29–30% of their groups' weighted earnings totals. [MEASUREMENT + INFERENCE]

For G1, Argentina and Brazil are plausible near-benchmark economic cases: BA 54.0%/48.5%, employment 79.2%/80.3%, poverty 8.3%/8.6%, earnings $73,492/$68,324, compared with $74,435 for the main benchmark. Their respective earnings-ratio intervals are 0.64–1.33 and 0.69–1.14; Argentina has only 215 records, Brazil 845. The LATAM G1 aggregate is much lower: BA 20.4%, employment 76.3%, poverty 16.3%, earnings $41,576. These are resident cohorts, not today's arrivals or unauthorized immigrants specifically. [MEASUREMENT]

## A better family-origin classification

After the main results, an explicitly **exploratory** sensitivity separated two parents from the same country from one country-born parent plus a US-born parent. The original any-parent comparison remains primary; these extra cuts are not part of its confirmatory search. [METHOD]

| US-born group | Records | BA+ | Employed | Poverty | Mean earnings / main benchmark |
|---|---:|---:|---:|---:|---:|
| Two Cuba-born parents | 276 | 49.9% | 82.0% | 3.8% | 97% |
| One Cuba-born and one US-born parent | 218 | 60.6% | 83.7% | 3.6% | 153% |
| Two Colombia-born parents | 174 | 48.8% | 89.7% | 2.9% | 88% |
| Two Ecuador-born parents | 94 | 44.7% | 85.4% | 3.1% | 100% |
| Two Peru-born parents | 82 | 58.0% | 77.6% | 16.5% | 72% |
| Two Mexico-born parents | 7,381 | 22.6% | 79.2% | 10.0% | 70% |

Source: same `levels.csv`/`contrasts.csv`, profiles `g2_two_*` and `g2_one_us_*`. Two-Cuba-parent earnings ratio is 0.972 with conservative 95% interval **0.679–1.264**. Most other two-parent cells are smaller still; the difference between profiles is descriptive and does not identify the effect of intermarriage. This sensitivity strengthens Cuba as a candidate while weakening a blanket inference from the pooled Peruvian row. [MEASUREMENT + INFERENCE]

Use **birthplace profile**, not “genetically one-quarter Mexican”: respondent birthplace; mother birthplace; father birthplace; grandparents where measured; age at arrival; birth/arrival cohort; and separately self-identification. “One Mexican-born grandparent out of four” is a genealogical observation. It is neither a national genetic fraction nor four equally measured cultural influences. CPS supports the parental portion; it cannot recover exact G3 country ancestry. [MEASUREMENT + SCOPE]

Sex sensitivity also matters. Among Colombian-parent G2 adults, mean earnings relative to same-sex benchmark are about **79% for men and 122% for women**, despite a pooled 96%. For Cuba they are 105%/138%; Ecuador 97%/108%; Peru 93%/101%; Mexico 67%/79%. Within the two-Cuba-parent profile, the point ratios are 83% for men and 118% for women, both with wide intervals. Intervals widen within sex; these are descriptive divergences, not precise rankings. The main Cuba/Colombia/Ecuador/Peru near-benchmark point pattern persists in ages 25–64 at ratios 1.22/0.96/0.96/1.00. [MEASUREMENT]

## How certain is “close”?

The specification was fixed before calculating country outcomes: four primary endpoints, ages 25–54, both birthplace benchmarks, all 20 Latin American countries, plus descriptive supplementary countries. Practical margins were **±5 percentage points for rates and ±10% for earnings**, explicit analyst choices rather than natural constants. Two-sided equivalence, being no materially worse, and failing to detect a difference are kept distinct. [FRAMING-SENSITIVE methodology; lane README.]

The all-four noninferiority claim requires favorable one-sided bounds on every primary endpoint and corrects the 20-country search. No G1 or G2 country passes the main standardized comparison at the primary margins against either stated benchmark. Do not translate that into “none comes close.” The intervals remain compatible with economic parity for several groups, while also allowing meaningful gaps. Because the covariance across overlapping annual samples is not known, the uncertainty calculation is deliberately conservative. [MEASUREMENT]

Pooling uses weighted totals, not an average of five percentages. Each year's 160 replicate weight vectors perturb only that year's contribution to the pooled estimator; benchmark differences/ratios are recomputed inside each replicate. The sum of annual-block standard errors is a first-order upper bound allowing unknown cross-year covariance, conditional on the fixed age/sex target. The smaller independent-years SE is retained only as a diagnostic. This is not an exact finite-sample guarantee, and survey sampling errors do not cover undercoverage, nonresponse, imputation bias or origin misclassification. [METHOD]

The raw-versus-standardized, sex, age-window, benchmark and practical-margin sensitivities are saved, not silently substituted for unfavorable main results. Empty pooled/replicate cells are explicitly unavailable; no empty cell is dropped and renormalized. Noninferiority verdicts are guarded against sparse and zero-event outcomes. Replication versus linearization differs by under 0.6% for the five main near/gap comparison groups above, but is materially less stable for some tiny cells; their formal conclusions remain guarded. [VALIDATION]

## Independent linked-income context and a correction

OI Table 6a offers useful triangulation with much larger linked administrative country samples, but measures **income ranks conditional on parent income**, not CPS marginal earnings. For example, at parental income percentile 75, Cuban-origin linked sons/daughters have predicted individual ranks **64.56/57.92**, versus **62.18/52.03** for the same-table USA-parent-origin group. The Cuban pooled household rank is **61.92**, compared with **60.90** in the newly acquired white native-mother series. The latter is contextual: its estimator and sample restriction differ, so it is not a directly matched causal contrast or a white G3+ benchmark. [SOURCE: [country table](https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6a_parametric.csv), [6a codebook](https://opportunityinsights.org/wp-content/uploads/2019/08/Table6a.pdf), [national table](https://opportunityinsights.org/wp-content/uploads/2018/04/table_1.csv).]

**Correction to earlier scope:** the full paper §III.A explicitly describes a target frame of US-born or authorized childhood immigrants whose parents are citizens/authorized immigrants, using tax-dependent and Numident linkage. It should not be treated as a direct sample of unauthorized families. Tax-linked parents also need not be biological parents. The country codebooks do not explicitly establish an own-US-birth restriction, so “linked children by parental origin” remains safer than claiming exact G2. These are 1978–83 child cohorts with income measured in 2014–15, not current inflows. [SOURCE: [paper §III.A](https://opportunityinsights.org/wp-content/uploads/2018/04/race_paper.pdf); [decision](../decisions/2026-09-17-country-comparison-benchmarks.md).]

The author's SSN-based frame description is not an independently observed current-status variable in the public country table. Table 1's native-mother documentation also uses missing entry-year where the paper describes US birth; retain that discrepancy rather than silently treating the series as verified two-parent ancestry. No added OI table contains compatible country-specific crime, trust or fiscal outcomes. [SOURCE: [Table 1 codebook](https://opportunityinsights.org/wp-content/uploads/2018/04/table_1.pdf), paper and acquired field inventories.]

## What we can now say, and what would improve it

- **Supported description:** measured economic differences vary substantially by country, generation, sex and parent profile. A lower LATAM average does not establish that every country group falls below native-parent Americans.
- **Best current candidate for “close”:** Cuban-parent US-born adults, including the two-Cuba-parent profile; multiple CPS outcomes and linked-income context point in that direction. Precise all-outcome parity remains unconfirmed.
- **Strong adverse description:** large education/earnings gaps for Mexican-parent G2 adults; sizable first-generation gaps for several large Central American groups. Education alone misses Haitian-parent economic differences.
- **Leading explanatory family:** selection, cohort history, family resources, time in the US and destination conditions. The present comparison does not isolate these mechanisms or genetic causes; persistence alone does not select among them.
- **Discriminating next data:** larger parental-country samples with economic outcomes and a documented cross-year design would narrow the near-parity intervals. Basic monthly CPS can expand education/employment cells; its earnings coverage differs from ASEC and would need a separate protocol. Matched national crime/trust/ancestry data remain the more severe gap.

The held GSS detailed-origin variable yields only 15 Cuban-, 10 Salvadoran-, 10 Dominican- and 6 Colombian-identified G2 respondents with valid standard TRUST, compared with 310 Mexican-origin respondents. Those are unweighted availability counts, not trust means or effective sample sizes. Its parent questions say US/foreign birth, not exact parent country. CILS/IIMMLA have useful local cohort outcomes; NLS is a selected birth cohort; none supplies an all-country national substitute. Pew 2008 remains a gated, unverified lead; ICPSR 20862 remains membership-blocked. [SOURCE: `gss_readiness.py`, `derived/gss-readiness.json`, [register](immigration-dataset-register.md).]

The decisive falsifier for a strong parity claim would be a well-powered, comparable country/parent cohort with a clear adverse gap on a required endpoint; conversely, sufficiently narrow compatible intervals would upgrade the current candidate evidence. Neither direction can be established by relabeling income as social trust or national origin as genes. [INFERENCE]

## Reproduction and audit

All source hashes, joins, construction rules, code and complete result paths are documented in the [lane README](../infra/immigration-fiscal/latam_comparison_2026_09_17/README.md). Five raw joins pass. **76 independent raw full-weight estimates** reproduce the main G2/reference calculations, with explicit coverage equality, allowing rounding of published main weights. Independent scalar/gradient probes verify the replication arithmetic; a code review found and fixed testing-family leakage and a verifier coverage weakness. Raw inputs were preserved. [VALIDATION]

The framing risk runs in both directions: choosing a favorable descendant group can obscure the regional average, while choosing the regional average can erase successful subgroups. LLM-assisted selection and interpretation are not neutral instruments. Fixed country coverage, symmetric margins, unfavorable outcomes, missing cells and both benchmarks are retained to make those choices inspectable. [INSTRUMENT / FRAMING-SENSITIVE]
