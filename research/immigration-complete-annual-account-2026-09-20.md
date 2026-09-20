# Complete annual account: calculation record

Date:2026-09-20. [MODEL / FRAMING-SENSITIVE] Evidence and calculations only;
narrative authorship remains operator-owned.

**Result:** The source-centered model gives **$165–197bn/year of conditional net
cost to other US residents** when CBO-informed school and delayed-service budget
responses replace full proportional spending, holding other model terms fixed.
An additional fixed-non-school-education sensitivity gives **$121–160bn/year**.
The full proportional-service benchmark remains **$270–289bn/year** after
production benefits. These are different response constructions, not a confidence
interval or competing measurements of a causal ethnic cost. CBO did not estimate
these Mexican-origin totals; its short-run evidence is transported here as a
sensitivity with production held fully adjusted. Fully fixed-service cases can
be positive. The wider **$262–357bn** proportional-service grid includes weaker
proxy stress tests with unequal empirical support. See the executed category
comparison below before reusing any single headline.

## Units, population and comparison

- Money: billions of nominal2024 dollars per year; government **current** accounts.
- Target:40.896574m observed CPS ASEC2025 Mexican-origin civilian-household residents,
  including all ages, schooling and observed descendants. The canonical union uses
  own/parent Mexican birthplace plus Mexican identification with US-born parents.
  It does not observe every distant descendant or cover only low-skill people.
- Beneficiaries: other US residents, including other immigrants. The result is
  not aggregate welfare of everyone, since target members' own welfare is excluded.
- Production counterfactual: stationary economies with and without the target's
  labor, plus separately declared fiscal responses. No historical reconstruction,
  removal-policy transition or lifetime projection is claimed.
- Full resident denominator:340.110988m; observed CPS civilian total336.727803m.
  Outside-CPS residents stay in the complement. Spending assigns their pool using
  an explicit equal-cost population rule; most receipt keys transport domestic
  totals onto observed household proxies. Neither is administrative origin linkage.

[SOURCE: [reproduction, source hashes and scope](../infra/immigration-fiscal/full_account_2026_09_20/README.md),
[receipt keys](../infra/immigration-fiscal/full_account_receipts_2026_09_20/README.md),
[spending keys](../infra/immigration-fiscal/full_account_spending_2026_09_20/README.md).]

## Complete accounting, before any causal interpretation

[OFFICIAL TOTALS] The pinned BEA2024 consolidated government account contains
$8,008.290bn current receipts and$10,061.458bn current expenditure, a−$2,053.168bn
balance. Every completed arm reconciles exactly. Consumption is net of sales
and includes depreciation; federal grants are not counted again as state spending.
Gross investment and capital transfers belong to a different account basis.
[SOURCE: [BEA Section3 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx),
Tables3.1/3.4/3.5/3.6/3.12/3.13/3.17, pinned August2026 vintage;
[BEA government methodology](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf).]

[MODEL] Default receipt and preferred service keys:

| Annual assignment, $bn | Shared within resource unit | Personal |
|---|---:|---:|
| Receipts | 545.12 | 517.10 |
| Current spending, shared government costs per capita | 1,023.88 | 1,017.92 |
| Assigned balance | −478.76 | −500.82 |
| Balance when defense, general government and old domestic interest receive zero target assignment | −193.15 | −215.21 |
| Gap versus the same domestic account's average resident, per-capita-cost convention | −274.23 | −296.29 |

The$285.61bn difference between the two absolute-balance conventions is an
assignment of common costs. The zero-target arm puts those costs on others; it
does not erase them. It is consequently inappropriate to use that arm's changed
relative gap as evidence that earnings or program use improved. A genuinely
uniform per-person flow cancels from a comparison using the same account and
denominator. Identified foreign flows and unknown residuals remain separate.
[DERIVATION: `derived/accounts.csv`; normalization tests.]

The older$259.38/$283.20bn partial balances remain reproducible but are superseded
for **complete current accounting**. This is a change in coverage, fiscal basis
and incidence rules, not a new survey observation proving an ethnic cost increased.

## Benefits joined to an explicit fiscal response

[ASSUMPTIONS] Primary long-run case:

1. Direct household payroll, income, consumption and similar receipts respond
   fully. Corporate/property incidence, other-business receipts and public-asset
   income receive zero direct response; the production model handles induced
   capital taxes. Residual personal/capital-financed tax overlap is exposed as O.
2. Household benefits and ordinary government services respond fully. Defense,
   general public services, existing interest and business subsidies stay fixed.
   Subsidies accruing to included owners cannot become a net cost without counting
   the corresponding private receipt.
3. Private capital fully adjusts, and all capital is initially owned by included
   other residents. Released capital earns its opportunity return elsewhere.
4. Each net fiscal dollar is returned to these beneficiaries with weight1.
   O=0 is the favorable overlap endpoint; additional duplication only lowers W.

[MODEL] Let A be direct receipts minus responsive expenditure, P outside private
after-tax welfare, F induced tax receipts, M matched outside transfer savings,
and Z omitted net effects. With fiscal-dollar weight beta:

`W = P - M + beta*(A + F + M - O) + Z`

At beta=1, transfers cancel and `W=A+P+F-O+Z`. Extra capital taxes are not free
income: their private counterpart is already in P. Consumer-price savings that
overlap these factor-income gains are not added again.
[SOURCE: [benefit equations and source replay](../infra/immigration-fiscal/full_account_benefits_2026_09_20/README.md);
[National Academies conceptual framework](https://www.nationalacademies.org/read/23550/chapter/12);
[Clemens capital-tax adjustment](https://docs.iza.org/dp15592.pdf).]

| Source-centered long-run case, $bn/year | Shared | Personal |
|---|---:|---:|
| Direct fiscal response A | −283.13 | −297.51 |
| Production plus induced receipts, cash scaling | +8.79 | +8.79 |
| Net with cash scaling | −274.34 | −288.72 |
| Production plus induced receipts, GDP scaling | +13.32 | +13.32 |
| Net with GDP scaling | −269.81 | −284.18 |

[MODEL] Across the named receipt alternatives, two spending-key bundles, both
sharing conventions, earnings/education proxies, CES parameters and hours
responses, the primary long-run net is−$356.84bn to−$262.05bn. Receipt arms vary
one assumption at a time; this is not the envelope of every possible joint
error. Core long-run production gains range$5.98–12.92bn cash/$8.77–21.08bn GDP.
Tax and ownership parameters are transported or unestimated assumptions, not
newly measured2024 elasticities. [SOURCE: `welfare_summary.csv`, `headline_cases.csv`,
`headline_summary.json`; linked benefit source notes.]

## Executed category-specific service responses

[MODEL / TRANSFERRED EVIDENCE] `report.py` now produces this comparison every run;
it is part of the annual account, not an unexecuted proposal. The same four central
personal/shared and cash/GDP production cases are used. Taxes, household benefits,
ownership, fully adjusted private capital, fixed defense/general government/old
interest and O=Z=0 remain unchanged. Only ordinary-service responses vary.

| Service construction | Conditional net cost, $bn/year | Evidential role |
|---|---:|---|
| Full proportional services | 269.8–288.7 | Original benchmark |
| CBO school response; all other services proportional | 207.9–240.2 | Isolates school response |
| CBO school response; economic affairs/recreation budgets fixed; other services proportional | **165.1–197.4** | Main CBO-informed comparison |
| Same, also fixing non-school education budgets | **120.8–160.3** | Additional favorable budget assumption |
| All education and economic affairs/recreation fixed; remaining services proportional | 33.7–46.4 | Removes school-composition dependence; diagnostic only |

[SOURCE: `derived/service_response_cases.csv`, `service_response_components.csv`,
`service_response_summary.csv` and the source/cell receipt `service_response_audit.json`.]

**Where the coefficients come from.** CBO's state-panel school analysis associates
+1 percentage point of enrollment growth with−0.37 points of per-pupil spending
growth; the decline-side association is−0.34. Total spending equals enrollment
times spending per pupil, giving first-order responses of63%/66%. These are two
directional sensitivity values, not a confidence interval or fitted response for
our population. CBO holds some near-term service budgets fixed and assumes
proportional response for safety, housing/community, health and income-security
services. The main comparison follows that category distinction and retains the
old full response for non-school education. It lowers the paired benchmark loss
by **$89.8–106.7bn/year**, rather than multiplying the whole fiscal deficit by63%.
[SOURCE: [CBO June2025 analysis, General Services and Appendix A](https://www.cbo.gov/publication/61464),
checked2026-09-20; DERIVATION: component exports.]

**Education construction check.** Our assigned education services are$193.37bn
shared/$199.57bn personal. They include higher education and other education;
the old school-plus-postsecondary allocation-key mix is not a measured expenditure
split. In the pinned BEA workbook, Table3.15.5 reports$1,404.129bn education
consumption plus investment, including$1,056.499bn elementary/secondary. Table3.17
reports$1,221.159bn education consumption and$182.969bn gross investment, with
$0.001bn rounding discrepancy. Assigning the implied investment residual wholly
to schools versus elsewhere bounds the national school **current-consumption**
share at71.5–86.5%, assuming nonnegative component investment. Gross investment
is never added to our current-service bill. [SOURCE: pinned workbook cells
T31505-A:29–32 and T31700-A:9,113, extracted by `service_response.py`.]

Applying this national share to target education spending is an explicit
**common-composition assumption**, not a bound on measured Mexican-origin school
spending. Non-school education's response is varied separately. The unrestricted
zero/full-education diagnostics expose dependence on the composition assumption;
they are not empirical bounds on all uncertainty. Our preceding conversational
calculation applying63% to the entire education row was too coarse for integration.
[INFERENCE; [construction evidence](../notes/immigration-service-response-external-evidence-2026-09-20.md).]

**What survives.** Within these constructions, realistic budget lags can materially
reduce the magnitude without overturning the negative sign. Even zero education
response leaves$33.7–46.4bn conditional loss **if** the other CBO-style responsive
categories stay proportional. Those category responses are assumptions too;
reducing them further can still reverse the sign. The roughly20% break-even value
remains a threshold, not an estimate to substitute into the calculation.
[MODEL / INFERENCE]

**What this does not establish.** CBO studies short-run, state/local changes and
small enrollment fluctuations. Our counterfactual covers an established all-age
population and all government levels; current consumption differs from school
finance's spending basis. Holding long-run production fixed isolates the service
channel but does not create an estimated adjustment path. Surge-specific private
school displacement and English-learner surcharges are not imported into the
all-generation population. Fixed budgets can cause crowding or quality losses;
no dollar value is invented for those harms. The property-receipt bridge and
other omitted effects remain unresolved. [INFERENCE / FRAMING-SENSITIVE]

Decision: [category-specific response integration](../decisions/2026-09-20-category-service-response.md).
The next discriminating evidence is matched category/horizon response and actual
subgroup current-education composition, not another arbitrary uniform percentage.

[EXECUTED] The added producer generated60 response cases and240 component rows;
all four original central results reconcile to their prior values. Eleven
integration tests pass. An independent in-session review found no blocking
calculation defect; its reference-shape/finite-value hardening was implemented
with a regression check. The review emphasized the composition and horizon
transfer limitations retained above.

## The $356.84bn endpoint and its evidential weight

[EXACT MODEL ROW] Personal allocation; high-AGI federal receipt-gap allocation;
alternative spending keys; wage-only earnings; below-BA/BA-plus split; cash
normalization; labor share.60; substitution elasticity2.5; fully adjusted capital;
fixed hours; alternative capital-tax retention.5. Fiscal-dollar weight1, all
capital owners among other residents, ordinary-service response1, defense/general
government response0, and overlap O=0. Capital-tax retention reallocates P versus F
but does not change P+F for these included owners at weight1.

| Endpoint annual arithmetic, $bn | Amount |
|---|---:|
| Household benefit expenditure assumed responsive | 420.21 |
| Ordinary service expenditure assumed responsive | 357.54 |
| Direct receipt response credited | −414.93 |
| Production plus induced-tax benefit | −5.98 |
| Conditional net cost | **356.84** |

Relative to the$288.72bn personal/cash source-centered case, changed responsive
spending adds$55.73bn, high-AGI tax-gap allocation adds$9.59bn, and smaller modeled
production benefits add$2.81bn. Total spending changes by$53.06bn because some
changed business subsidies are held fixed in the welfare response.

[MODEL / ASSESSMENT] The largest spending move is Medicaid/CHIP/other medical:
$116.91bn becomes$185.61bn, **+$68.70bn**, when reported coverage headcounts replace
age/birth-specific expected payer dollars. That implicitly allocates equal annual
dollars per covered person despite different ages, eligibility and coverage
duration. Other upward substitutions include Social Security dollars→age65+
(+$13.81bn) and veterans benefit dollars→all adults (+$10.46bn). Downward changes,
including refundable credits−$23.46bn and Medicare−$7.83bn, partly offset them.
[SOURCE: matched personal rows of spending `derived/allocations.csv`; endpoint
in `welfare_scenarios.csv` and fiscal pool in `response_pools.csv`.]

[PRIMARY CHECK] CMS reports that children represented35.9% of Medicaid beneficiary
years but15.6% of spending in2023, while disability-eligible beneficiaries represented
9.9% of beneficiary years and29.1% of spending. This does not identify the target's
true cost, but confirms that headcounts and spending shares are different objects.
[SOURCE: [CMS2026 Beneficiary Profile, pp13–15](https://www.medicaid.gov/medicaid/quality-of-care/downloads/beneficiary-profile-2026.pdf).]

[JUDGMENT] Keep$356.84bn as a disclosed pessimistic stress test; do not give it
the same evidential weight as the preferred spending allocation. Coverage and
age proxies can expose underreporting/transport sensitivity, but replacing veteran
recipients with all adults or spending weights with headcounts is weaker evidence
of actual expenditure. Preferred MEPS age/birth transport also has origin and
institutional coverage limitations; this critique does not validate it as truth.
The high-AGI receipt allocation is better motivated by the separate tax-tail check.
Full service-cost response is plausible as a long-run assumption but remains
unestimated. No additional victim-harm, defense or legacy-interest charge creates
this endpoint. Numerical results are unchanged; their evidential weighting is clarified.

## What can reverse the sign?

[DISCONFIRMATION / MODEL SENSITIVITY]

| Declared capacity path; core ownership, fixed defense/general government | Net outside effect, $bn/year |
|---|---:|
| Ordinary service budget fixed; private capital fixed | −41.53 to +112.67 |
| Half of assigned service costs respond; intermediate private capital | −203.55 to −81.73 |
| All assigned service costs respond; private capital fully adjusts | −356.84 to −262.05 |

Service response and private capital adjustment are independent economic
parameters. Pairing them here is an illustrative capacity path, not an estimated
timeline. The export also solves the service-response break-even separately at
every production setting.

- **Lower incremental service costs:** with preferred receipt/spending keys and
  fully adjusted capital, break-even requires only18.5–22.7% of assigned service
  costs to be incremental under personal allocation, or21.5–25.8% under shared
  allocation. Household benefits still respond fully in this threshold.
- **Additional net benefits:** retaining the primary long-run assumptions requires
  a further$262–357bn/year of matched net benefits. This is a hurdle, not evidence
  those omitted benefits are zero or cannot exist. Missing harms have the opposite sign.
- **Capital ownership:** extending excluded-owner shares to50%/100%, with full
  capital adjustment, can shrink the modeled loss to$21.31bn in the most favorable
  tested case; it does not flip this particular long-run grid. Those endpoints
  are not empirical ownership estimates or universal bounds.
- **Different beneficiaries or fiscal valuation:** beta=0 changes the question to
  outside private welfare alone. Including target residents' own welfare also
  changes the welfare objective; neither is a statistical refutation of beta=1.

Crime, housing amenities, innovation, institutions, transition costs and a
historical replacement population are not priced here. Existing crime/price/
hedonic estimates do not yet match this beneficiary set and counterfactual.
Their omission is not a finding of zero. Lifetime results require their own
future-profile rebuild and cannot be obtained by multiplying these annual values.

## Verification and disposition

**Executed scaling check:** [school and state-service tests](immigration-service-scaling-test-2026-09-20.md)
find school spending elasticities of .735 unweighted/.836 pupil-weighted within
districts, versus .945/1.004 across districts. A proportional model predicts held-out
district costs better than universal 3/4 or 5/6. All ten full-panel within-state
service intervals include 1. These descriptive associations cannot distinguish
efficiency from quality loss, budget delay, prices or composition. Under an assumed
power law, the exact finite-removal response is `[1−(1−s)^b]/s`; 5/6 at the national
illustrative target share implies 84.21% response and a uniform theory-only
$214–232bn conditional cost. That geographical/category transfer is not estimated
for our target. The CBO-informed comparison remains unchanged; no additional
scaling discount is stacked onto it. [MODEL / INFERENCE;
[calibration decision](../decisions/2026-09-20-service-scaling-calibration.md)]

[EXECUTED] Three source builders and both integration builders ran from the
canonical checkout with verified input/output hashes.27 tests pass. All1,296
production scenarios were replayed;18 old ownership cases reconciled;3,888
ownership-expanded cases yield497,664 conditional welfare rows. Independent
native reviews examined distinct receipt, spending and integration code; the
integration reviewer independently checked62,208 real-data rows. Two review-found
validation gaps were repaired with regressions: missing receipt keys now fail,
and spending verifies the school export's upstream manifest inputs. Neither repair
changes the current numerical result. No restricted
data, external publication, new raw download or narrative essay was produced.

[INFERENCE] We can establish a complete, reproducible conditional estimate and
its sign-reversal requirements. We cannot call the entire conditional range an
observed ethnic burden. The next uncertainty is largely the economic response
and incidence assumptions, rather than an unaccounted national-dollar residual.

[INSTRUMENT] LLM-assisted allocation and synthesis can favor a framing. Source
totals, assumptions and disconfirming cases remain separately inspectable.
Method decision: [complete account and fiscal response](../decisions/2026-09-20-complete-account-and-fiscal-response.md).

## Revisions

2026-09-20, scaling test: added the executed school/state comparisons and exact
finite-cost derivation. Descriptive sublinear school spending supports heterogeneous
responses, but not a universal complexity exponent or additional causal savings.
Existing fiscal values are preserved. [Decision](../decisions/2026-09-20-service-scaling-calibration.md).

2026-09-20, category response integration: incorporated CBO-informed school and
delayed-service responses into the report producer, replacing the single prominent
proportional-service figure with the structured comparison above. The negative
sign survives the new assumptions, while the magnitude falls materially. The
original model outputs are preserved. [Decision](../decisions/2026-09-20-category-service-response.md).

2026-09-20, detention scope: [the measurement/accounting rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md)
keeps actual custody costs while separating them from ordinary offending. A
detention breakout must reconcile to this account's existing government totals;
no new expenditure or ethnic attribution is added by this clarification.
[Decision](../decisions/2026-09-20-separate-detention-offenses-and-spending.md).

2026-09-20, endpoint audit: decomposed the$356.84bn row and distinguished the weaker
headcount/age spending substitutions from preferred program-dollar proxies.
The broad grid is retained as sensitivity, not an equally supported uncertainty
interval. See the [method decision's interpretation update](../decisions/2026-09-20-complete-account-and-fiscal-response.md).
