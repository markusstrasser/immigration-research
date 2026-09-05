**Verdict:** Missing people, unobserved immigration status, unreported conduct, selective enforcement and race/ethnicity coding require different corrections. Documented institutional failures make blanket dismissal of underrecording unwarranted. They do not supply a national immigration-status correction factor. We can calculate what assumptions would change a result; the available data cannot identify every missing outcome or guarantee a universal crime/fiscal ranking. [SOURCE: primary audits below; INFERENCE]

# Missing residents, selective recording and unidentified effects

The frame is measurement of U.S. resident fiscal components and specific justice outcomes, as of September5,2026. The strongest institutional-failure hypothesis is that overwhelmed or politically constrained agencies fail to investigate particular conduct, missingness differs by group, and the resulting low official count is then mistaken for low underlying harm. The strongest counter is that anecdotes are selected, enforcement can also target immigrants more intensively, and observed offending and detection cannot be separately recovered from one administrative count. Both mechanisms remain testable; neither is assumed away. [INFERENCE; FRAMING]

## 1. Unauthorized does not mean absent from the survey

ACS/CPS aim to include unauthorized residents but do not observe current status in public records. The lawful-population residual and probabilistic assignments estimate that latent status; they are not a new population to add wholesale to the survey. SIPP2025 first-arrival Permanent/Other also cannot identify current unauthorized status. [SOURCE: [Census foreign-born definition](https://www.census.gov/topics/population/foreign-born/about.html), [admission/undercount source audit](immigration-admission-work-access-2026-09-05.md)]

For residual missing share `q` of the **true target population after existing survey weighting**:

`N_true = N_observed / (1−q)`

`mean_true = (1−q) × mean_observed + q × mean_missing`.

This differs from treating q as missing people per observed person. It is also separate from misreported earnings or benefits among included respondents. Status imputation that uses occupation, earnings or benefit eligibility can mechanically influence a subsequent comparison of those same outcomes. Replicate-weight uncertainty does not cover that assignment model. [ALGEBRA; INFERENCE]

In the equal-adult, insurance-conditioned fiscal example **before school spending**, native balance is $9,829 and Mexico-born balance $1,160. If 10% of the true Mexico-born target population remains absent and that missing group averages −$10,000 on the same partial ledger, the corrected Mexico mean is **$44**. To raise its mean to the native level while holding the native estimate fixed, the missing group would need to average **+$87,858**. These are tipping calculations, not estimated undercount or claims about unauthorized people. With the average-school construction, the corresponding tipping mean is **+$100,824**. [CALCULATION: `missing_population_tipping_points.csv`]

Native coverage is uncertain too. A separate two-sided grid varies native missing shares0/5/10%, Mexico-born0/5/10/20%, and each missing group's balance−$10k/$0/+$20k. A distinct tax grid varies positive-liability collection separately from refunds. These chosen stress grids preserve the native-minus-Mexico ranking; they are not exhaustive bounds or fitted probability distributions. The algebra permits other combinations to reverse a ranking. [CALCULATION; FRAMING-SENSITIVE]

The source-specific adjustments are different objects: DHS's 13% is an assumed undercount for the newest unauthorized arrival-year cohort in its older residual model, declining with tenure; CBO2026's 15% uplift concerns observed gotaways, not Census coverage. Their populations, vintage and denominators are retained in the [admission memo](immigration-admission-work-access-2026-09-05.md). Averaging residual estimators that share ACS inputs would not create independent corroboration. [SOURCE; INFERENCE]

## 2. Crime needs an observation chain

For victim-reported conduct, distinguish incident, disclosure, police recording, investigation/arrest, filing and conviction. Police-initiated offenses follow another entry route. Conviction also depends on disposition timing; prison stock depends on sentence duration, releases and removals. Media coverage is yet another selected outcome, not a direct crime numerator. Conditional transitions may depend on each earlier stage; multiplying unrelated marginal rates assumes independence without evidence. [MEASUREMENT MODEL]

The [repaired Texas2018 result](immigration-conduct-denominators-2026-09-05.md) is a **violent-felony arrest-charge ratio of0.4571**, unauthorized/native. Let `a` be expected recorded charges per comparable underlying offense and `d` the published/true population ratio. Then:

`R_true = R_recorded × (d_unauthorized/d_native) / (a_unauthorized/a_native)`.

Charge multiplicity means `a` need not be a probability. With relative denominator coverage held at1, equality occurs at **relative recording intensity0.4571**; at0.5, the conditional underlying ratio is **0.9143**. If the unauthorized denominator were overestimated by20% relative to native while recording intensity were0.5, the underlying ratio would be **1.0971**. Conversely, undercounting that denominator alone inflates the recorded rate. [ALGEBRA; CALCULATION: `crime_ascertainment_stress.csv`]

These are conditional historical thresholds, not detection estimates or results for 2022–2025 arrivals. Prosecutors declining to file cannot mechanically erase arrest charges already recorded, although anticipated declinations, recording rules or policy feedback can change upstream enforcement. A fraud-control failure is evidence about that program; it cannot numerically correct a violent-offense rate. Immigrant victims' reporting rates cannot directly identify immigrant offenders' detection when the groups differ. [INFERENCE]

## 3. There is actual evidence of institutional failure

The [Casey audit](https://www.gov.uk/government/publications/national-audit-on-group-based-child-sexual-exploitation-and-abuse/national-audit-on-group-based-child-sexual-exploitation-and-abuse-accessible) documents avoidance of ethnicity questions and deficient data being used to dismiss concerns about Asian/Pakistani group-based exploitation. In its broad national contact-group abuse table, **4,404 of6,670 records lack declared ethnicity**. White records are **28.25% of all entries but83.14% of those with known ethnicity**. The known-only percentage does not settle the missing group's profile. The table includes family and institutional settings; it is not exclusively street grooming, a U.S. status comparison, or a religious classification. [SOURCE; CALCULATION]

Minnesota's [2024 legislative audit](https://www.auditor.leg.state.mn.us/sreview/2024/mdefof.htm) finds that inadequate MDE oversight created opportunities for Feeding Our Future fraud and that warnings and complaints were mishandled. This substantiates agency failure. It does not establish Governor Walz's personal motive or estimate fraud per Somali, refugee or unauthorized resident. The [case ledger](immigration-conduct-denominators-2026-09-05.md) distinguishes alleged from admitted conduct, program payments from recoveries, and case/provider/recipient denominators. [SOURCE]

Thus the specific concern deserves measurement, including when institutional incentives are politically uncomfortable. A general claim that liberals, media or police systematically suppress most crimes by unauthorized people remains unmeasured here. Deliberate protection, insufficient capacity, bad definitions, low reporting and case-selection rules are distinct explanations requiring different evidence. [INFERENCE]

## 4. Race, Hispanic ethnicity, nativity and status are separate dimensions

A Hispanic person can be coded White on a race field without a data-entry error; ignoring the separate Hispanic field is an analysis error when claiming to measure non-Hispanic Whites. Nor does White imply US-born. The new [wage strata](immigration-wage-race-strata-2026-09-05.md) separate native/foreign-born Black adults and use mutually exclusive Hispanic-any-race and non-Hispanic race categories. The [crime strata](immigration-crime-race-ethnicity-2026-09-05.md) retain official recodes, uncertain ethnicity and the limits of available joint fields. [SOURCE: Census, FBI and SPI definitions in those memos]

When classification is uncertain, the recorded vector of group counts is conceptually `recorded = classification_matrix × detected_true_counts`. Without validated joint categories the matrix is unknown, and a race-only table cannot recover status-by-race rates. Unknown categories should remain visible; reassigning all unknowns to a preferred group is a stress endpoint, not an estimate. [MEASUREMENT MODEL]

## 5. Known gaps and ways to reduce them

| Uncertainty | Principal evidence needed | Current treatment |
|---|---|---|
| Current status and population coverage | Same-date residual stock-flow reconciliation with lawful transitions, deaths and exits | Source-vintage comparison, latent-status warning, one- and two-sided coverage stress |
| Unreported income/benefits | Linked administrative records or validated reporting studies by relevant population | Remains unmodeled among respondents; the separate collection/refund grids hold reported transfers and service use fixed |
| Selective investigation/prosecution | Linked incident-to-disposition cohorts, including screened-out cases and comparable agency coverage | Explicit observation stages; no conviction/arrest fraction from mismatched cumulative totals |
| Unreported serious harm | Independent victimization, hospital/death or service records with usable group definitions | Triangulation proposed; victim records do not automatically identify offender status |
| Hidden program fraud | Representative payment/provider audits, paid-loss and recovery reconciliation | Known cases retained; enforcement-selected cases are not prevalence samples |
| School/shelter crowding | Matched person/student-days, incremental resources and a no-arrival counterfactual | [NYC financing](immigration-local-cost-incidence-2026-09-05.md) and actual school exposure; no unsupported marginal cost |
| Institutional or rare severe harms | Prespecified observable outcomes, comparison populations and policy timing | Unidentified; no numerical posterior or generic “unknown unknown” surcharge |

More reported offenses after an audit or policy change can mean improved detection, more underlying crime, or both. Lists with shared detection mechanisms also violate naive capture–recapture independence. These ceilings explain why we stop short of fitting a precise hidden-crime total to the available proxies. [INFERENCE]

The response to unknown unknowns is an explicit omitted-ledger register, break-even calculations, independent source checks and revisable conclusions. Arbitrary priors or an unexplained ±10% would manufacture precision. The project’s LLM may itself favor familiar narratives; both substantive institutional failures and limits on group-level inference are therefore preserved. [FRAMING; [instrument note](../notes/llm-bias-caveat.md)]

## Reproduction

```sh
uv run --script infra/immigration-fiscal/build/analyze_immigration_uncertainty.py \
  --fiscal .scratch/clarity-next-20260905/fiscal/cps-health \
  --schools .scratch/clarity-next-20260905/fiscal/schools \
  --tx-comparisons .scratch/clarity-next-20260905/conduct/analysis/tx_comparisons.csv \
  --output .scratch/clarity-next-20260905/uncertainty
```

Five CSVs distinguish school scope, missing-population tipping points, two-sided selection, liability/refund stress and crime recording scenarios. Their manifest pins the input outputs. Assumed grids are not confidence intervals; survey variances exclude systematic missingness. [CALCULATION; source-code and arithmetic review]
