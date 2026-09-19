# Which discrepancies justify adjustment, and which data improve the account?

**Executed September20:** [Four fiscal checks](immigration-four-fiscal-checks-2026-09-20.md)
apply the enrollment correction and report the national, same-year tax and health
results. The earlier IRS anchors below reproduce2022, despite their source's2023
heading; the new check uses pinned2023 detailed tables.

**Verdict:** Some discrepancies identify weaknesses in our construction; others
compare different populations or accounting concepts. Better public data remain
available. The highest-value work is national accounting coverage, directly
measured pupil exposure, and matched-year earnings/tax distributions. No new
uniform ethnic adjustment is identified by the aggregate residuals. [INFERENCE]

Checked 2026-09-19. Follow-up to the [executed administrative checks](immigration-administrative-checks-2026-09-19.md).
The model population remains the observed Mexican-origin union of all ages and
education levels, not low-skill immigrants alone or a complete genealogical
lineage. This note diagnoses discrepancies and verifies data access; it does not
recalibrate the annual account. LLM-assisted source selection and interpretation
remain subject to the project's [instrument caveat](../notes/llm-bias-caveat.md).

## What should change?

| Discrepancy | What the evidence establishes | Appropriate adjustment |
|---|---|---|
| Public pupils below direct survey counts | Transporting one 80.27% enrollment factor explains much of the discrepancy; decomposition below | Improve our pupil-exposure model, including K–12 students outside ages 5–17 |
| OASDI taxable-base proxy 6.87% above SSA | The check assumes all wages are covered; wage and self-employment components err in opposite directions | Repair the check's coverage assumptions first; this does not prove canonical CPS FICA is overstated by 6.87% |
| CPS federal tax compared with IRS | The existing comparison mixes income 2024 and 2023, with different units and concepts | Replace our comparison with matched years, tax units, credits and income bands |
| Benefit totals below administrative payments | Residuals combine reporting, timing and population coverage | Narrow the comparator to the survey population before interpreting the remainder as underreporting |
| National model does not close to government accounts | Important categories and accounting boundaries remain outside the model | Reconcile categories explicitly; do not distribute the unexplained residual by ethnic population share |

These are rules for interpreting the existing measurements, not a presumption
that surveys or administrators are always correct. An adjustment needs an
identified definition difference, measured coverage error or better observation.
Forced agreement with a calibration target is not independent validation. [INFERENCE]

## Executed explanation of the school discrepancy

[CALCULATION] Let `C0` and `r0` be modeled child count and public-enrollment rate,
and `C1`, `r1` the corresponding direct ACS quantities. The exact symmetric
decomposition is:

```
modeled pupils − ACS pupils = child-count term + enrollment-rate term
child-count term = (C0 − C1) × (r0 + r1) / 2
enrollment-rate term = (r0 − r1) × (C0 + C1) / 2
```

Using the existing [school generator](../infra/immigration-fiscal/admin_school_checks_2026_09_19/README.md)
output `derived/pupil_comparison.csv`, recover `C0 = model / model_public_share`
and `C1 = acs / acs_direct_public_share`. Both terms sum to the observed difference
within 0.000001 pupil in every row. Counts below are thousands; rounding can
affect displayed sums.

| Area and group | Total discrepancy | Child-count term | Enrollment-rate term |
|---|---:|---:|---:|
| US, all | −635.1 | +37.4 | −672.5 |
| US, Hispanic | −926.1 | +2.5 | −928.5 |
| California, all | −464.9 | −171.4 | −293.5 |
| California, Hispanic | −430.3 | −139.2 | −291.1 |
| Texas, all | −408.5 | −146.4 | −262.1 |
| Texas, Hispanic | −331.5 | −92.4 | −239.0 |

[INFERENCE] About 63–64% of the all-child CA/TX gap comes arithmetically from the
fixed rate; almost the entire national Hispanic gap does. The remaining state
child-count differences still require a survey-population/timing explanation.
This decomposition does not identify whether nonresponse, weighting or timing
caused those count differences. Its point estimates hold the modeled rate fixed;
these percentages are not causal shares or confidence intervals.

[SOURCE / FEASIBILITY] The public [October 2024 CPS School Enrollment supplement](https://www.census.gov/data/datasets/2024/demo/cps/cps-school-enrollment.html)
contains actual public/private enrollment and grade, Mexican self-identification,
own and parental birthplace, and separately downloadable replicate weights.
The [technical dictionary](https://www2.census.gov/programs-surveys/cps/techdocs/cpsoct24.pdf)
specifies `PEPUBLIC` for the older-student branch, `PECHPUB` for children, and
`PWSUPWGT` as the supplement weight. The age-specific question branches must be
combined; `PESCHENR` alone misses younger children. This file was
located and its schema checked, but no new enrollment estimate was run here.

[INFERENCE] It permits a closer match to the CPS origin definition than a broad
Hispanic ACS rate. Estimate supported age/origin/state cells, pool where samples
are thin, and validate against unused ACS/administrative grade counts. It cannot
recover unobserved distant ancestry. Actual K–12 enrollment should define pupil
exposure across ages; age 5–17 alone omits 2.618m pupils in the existing national
ACS extraction. The current $11–12bn Hispanic-rate scenario remains a proxy,
not the identified Mexican-origin correction.

## Better earnings and tax checks available publicly

[SOURCE / FEASIBILITY] [CPS ASEC 2024](https://www2.census.gov/programs-surveys/cps/datasets/2024/march/asecpub24csv.zip)
measures income 2023. It can be compared with [IRS 2023 income/return tables](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-returns-complete-report-publication-1304-basic-tables-part-1)
and [SSA 2023 state OASDI/Medicare earnings, Tables 4.B10/4.B12](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/4b.html).
Compare tax-unit counts, earnings and tax liability by income band. Separate
nonfilers, credits, wages versus self-employment, OASDI versus Medicare coverage,
and 50 states/DC versus other geography. SSA's state tables are preliminary
1% sample estimates, with residence/employer-location and multi-employer-refund
qualifications; they are not a flawless administrative census.

[SOURCE / INFERENCE] OASDI exemptions are real: SSA reports approximately
72% coverage among [state/local public employees](https://www.ssa.gov/benefits/retirement/social-security-fairness-act.html).
The exemption's dollar contribution to this model discrepancy is unmeasured.
A [linked CPS–SSA earnings study](https://www.ssa.gov/policy/docs/rsnotes/rsn2024-01.html)
also finds heterogeneous reporting errors. Neither fact supplies a uniform
Mexican-origin tax correction. Split existing CPS results by earnings band,
reported/imputed income and employment class to test each proposed explanation.

[SOURCE / FEASIBILITY] [ACS 2024 PUMS](https://www.census.gov/programs-surveys/acs/microdata/access.html)
offers a second earnings distribution: matched civilian household scope,
Mexican self-ID and Mexico birthplace, age, wages, work and replicate weights.
Use income adjustment factors and acknowledge rolling past-12-month income.
ACS lacks the full CPS parental-origin definition. Agreement on matched groups'
recipient shares, medians and wage bands would corroborate the earnings gap;
it would not directly validate taxes or its causal explanation.

## Benefit scope: two explanations tested, one direct-data route verified

[SOURCE / CALCULATION] The [USDA historical workbook archive](https://www.fns.usda.gov/sites/default/files/resource-files/snap-zip-fy69tocurrent-9.zip),
release September 11, 2026, contains FY24/FY25 monthly state data excluding
P-EBT/Other. Summing January–December 2024 gives USVI $70,166,694 and Guam
$120,069,331. The same-series US total is $95,036,822,311; excluding both
territories leaves **$94.846586bn**, versus adjusted shared CPS **$86.821834bn**.
The **$8.024752bn** residual is not explained by those territories. This
workbook's national sum is $78.419369m below the broader national-monthly series
used in the original check; the two definitions are kept separate.

For reproduction, sum column D in FY24 NERO rows 117–125 plus FY25 rows 114–116
for USVI, FY24 WRO rows 57–65 plus FY25 rows 54–56 for Guam, and FY24 US Summary
rows 12–20 plus FY25 rows 9–11 for the US. The source month labels were checked.
Archive SHA256: `ce676f4628993881f3f4dd26d923c060fbb8473c12a1c47a23748ea81e1ce857`.

[SOURCE / SCALE CHECK] [SSA SSI Table 6](https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/sect02.html#table6)
reports 102,538 Medicaid-institution residents with an average monthly payment
of $35.14 in December 2024. Multiplying that snapshot by 12 gives roughly
$43m, far below the $5.498bn SSI discrepancy. This is not an observed annual
total or an exhaustive institutional adjustment; it does rule out treating this
particular recipient category as an obvious multibillion-dollar explanation.
Payment date versus month due and state supplements still need matching.

[SOURCE / FEASIBILITY] Direct [DOL ETA downloads](https://oui.doleta.gov/unemploy/DataDownloads.asp)
provide [monthly ETA 5159](https://oui.doleta.gov/unemploy/csv/ar5159.csv).
The downloaded file contains 636 state/month rows for 2024, including territories.
The [field map](https://oui.doleta.gov/dmstree/handbooks/402/402_4/4024c6/4024c6.pdf)
separates regular-state benefits (`c45`) and UCFE/UCX (`c48`, whose components must
not be added again). Extended benefits and other programs require separate
reconciliation before calling any sum all UI. [DOL's notes](https://oui.doleta.gov/unemploy/FRSnotes.asp)
exclude disaster/Trade Act benefits from its convenience all-program statistic;
the downloaded convenience CSVs were stale, ending in 2014/2017. No matched
2024 all-UI total was computed. This remains a useful disconfirmation test because
the historical multiplier raises CPS above the existing BEA comparator.

## Health and the larger accounting gap

[SOURCE / FEASIBILITY] Medicaid's [state/eligibility spending methodology](https://www.medicaid.gov/state-overviews/scorecard/content/scorecard-rel/PerCapitaExpendDataMethod-2025.pdf)
supports a stronger test than matching a single total: recipients, member-months
and costs across five eligibility categories. First compare children, adults,
aged and disabled groups at state level. Claims service-year spending and
CMS-64 cash accounts need an explicit bridge; its illustrative Table III.2 is
not an observed state dataset. Existing education/insurance matching sensitivity
has already been run; this would add administrative eligibility validation.

[SOURCE / LIMIT] [CMS's MEPS reconciliation](https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/meps-reconciliation)
requires population, service and measurement adjustments. Institutional care
cannot simply be added to an already expanded total. [MCBS](https://www.cms.gov/data-research/research/medicare-current-beneficiary-survey)
offers public survey/cost files through 2023 and more detailed limited datasets;
the public survey file covers community residents. The CMS page still lists
2024 cost files as forthcoming. [ResDAC](https://www.resdac.org/file-availability)
lists TAF through 2023 and preliminary 2024, with state/year availability
qualifications and restricted access. These improve health-cost measurement,
not complete Mexican genealogies.

[CALCULATION / PRIORITY] The [current national bridge](immigration-macro-reconciliation-2026-09-19.md)
still has roughly $2.07–2.14tn fewer modeled receipts and $3.36–3.37tn fewer
modeled expenditures than BEA current accounts. These are mixed-scope residuals,
not all errors or missing costs attributable to immigrants. In the shared
receipt diagnostic, production/import taxes account for $913bn of the difference
and other current receipts for $479bn. Category coverage, current/capital
boundaries, service fees and intergovernmental transfers must be reconciled
before making a complete-government headline. This matters more to completeness
than polishing a $5–7bn conditional benefit adjustment.

## Restricted data and the stopping boundary

[SOURCE / ACCESS] Census's [August 2026 linkage inventory](https://www2.census.gov/about/linkage/data-file-inventory.pdf)
lists CPS-linked earnings records, but explicitly warns that not all holdings
are available through research centers. Public records cannot simply be joined
to confidential tax histories. [Current access rules](https://www.census.gov/topics/research/guidance/restricted-use-microdata/standard-application-process.html)
require an approved project, Special Sworn Status/background checks, US-based
institutional affiliation and residence conditions; overseas work is prohibited.
No application, contact, purchase or access grant occurred in this check.

[INFERENCE] Public school, matched-year tax and national-coverage checks remain
worth doing. A correction should also predict unused state, age or income cells;
calibrating every cell and reporting agreement would hide failure. Better linked
data can reduce reporting error, but unknown ancestry, public-good attribution
and the response to an immigration policy remain distinct problems. Increasing
statistical complexity cannot identify them from absent observations.

## Revisions

2026-09-20: [Measured enrollment and residual boundaries](../decisions/2026-09-20-measured-enrollment-and-residual-boundaries.md)
records execution of the recommended checks. The IRS comparison's original
source year was wrong; pinned detailed tables replace that anchor. The live CMS
methodology URL is corrected; exact state eligibility matching is still unavailable.
