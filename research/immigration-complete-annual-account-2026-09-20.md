# Complete annual account: calculation record

Date:2026-09-20. [MODEL / FRAMING-SENSITIVE] Evidence and calculations only;
narrative authorship remains operator-owned.

**Result:** Under the declared long-run response assumptions, the model gives
**$270–289bn/year of net cost to other US residents** in source-centered cases
after production benefits. The wider **$262–357bn** grid includes weaker proxy
stress tests; its endpoints do not have equal empirical support. These are conditional model results,
not a measured causal cost of ethnicity, an admission estimate, or a confidence
interval. The fixed-service-budget cases include positive results, so an
unconditional claim of a proven annual net cost is not established.

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

2026-09-20, detention scope: [the measurement/accounting rule](immigration-detention-crime-and-fiscal-scope-2026-09-20.md)
keeps actual custody costs while separating them from ordinary offending. A
detention breakout must reconcile to this account's existing government totals;
no new expenditure or ethnic attribution is added by this clarification.
[Decision](../decisions/2026-09-20-separate-detention-offenses-and-spending.md).

2026-09-20, endpoint audit: decomposed the$356.84bn row and distinguished the weaker
headcount/age spending substitutions from preferred program-dollar proxies.
The broad grid is retained as sensitivity, not an equally supported uncertainty
interval. See the [method decision's interpretation update](../decisions/2026-09-20-complete-account-and-fiscal-response.md).
