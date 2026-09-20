**Verdict:** The service-response fraction is the incremental public-service expense divided by our assigned service spending. It is an assumption, not the percentage of immigrants receiving benefits. The 19–26% figures are model break-even thresholds, not estimates of the actual response. Education dominates the pool; education alone can exceed the threshold. Evidence against immediate proportional spending does not establish low long-run costs or zero congestion harm. [MODEL / INFERENCE]

**Integrated follow-up, same date:** The [main annual account](../research/immigration-complete-annual-account-2026-09-20.md#executed-category-specific-service-responses) now executes category-specific CBO-informed responses, with separate school/non-school education and current/investment accounting. It gives $165–197bn/year conditional net cost, or $121–160bn with non-school education budgets fixed as well. The uniform percentages below remain diagnostic, not the latest evidence-informed comparison. [MODEL]

## Definition and scope

Date: 2026-09-20. All local amounts are billions of nominal 2024 dollars per year. Population: 40.896574m observed Mexican-origin civilian-household residents, all ages and schooling including observed descendants. Welfare beneficiaries: other US residents. These are conditional stationary-counterfactual calculations, not observed removal savings or lifetime balances. [SOURCE: `research/immigration-complete-annual-account-2026-09-20.md:14–29`.]

For category j, define `r_j = (spending_with_target - spending_without_target) / assigned_target_spending_j`. Then `W = direct_receipts - household_transfers + private_plus_induced_receipts - sum(r_j * assigned_services_j)`, at fiscal weight 1, no public-goods response and zero additional overlap/omitted effects. Uniform r is a simplifying restriction. Nothing guarantees the actual ratio lies in [0,1]: capacity expansion or additional needs can make incremental cost exceed average assignment. [DERIVATION / INFERENCE; SOURCE: `infra/immigration-fiscal/full_account_2026_09_20/welfare.py:77–102`.]

100% treats all assigned service dollars as incremental. 50% treats half as incremental. 0% fixes those budgets; it does not establish unchanged service quality. Direct receipts and household benefits (including Medicaid/Medicare payments) remain fully responsive in this sensitivity. Defense/general government and old domestic interest stay fixed. [SOURCE: same response function and response pools.]

## What the service pool contains

| Category | Personal | Shared |
|---|---:|---:|
| Education services | 199.57 | 193.37 |
| Public order and safety | 62.43 | 62.43 |
| Economic affairs services | 36.26 | 36.26 |
| Income-security services | 27.69 | 29.34 |
| Government health services | 23.53 | 23.53 |
| Recreation and culture | 6.53 | 6.53 |
| Housing/community services | 1.75 | 1.75 |
| **Total** | **357.76** | **353.21** |

[SOURCE: `infra/immigration-fiscal/full_account_spending_2026_09_20/derived/allocations.csv`, scenario `complete_preferred_F_per_capita`, `response_class=service`; sums independently matched `response_pools.csv`. Government-produced health services are distinct from medical-benefit purchases. Education mixes school and postsecondary proxies, not a separately observed K–12 spending total.]

## Vary service response alone

Keep private capital fully adjusted, ownership among other residents, the preferred spending/receipt keys and all other assumptions unchanged. Range is across four central cases (personal/shared and cash/GDP production normalization); it is not a confidence interval. This deliberately avoids the older grid's pairing of capital adjustment and service response. [MODEL]

| Uniform service response | Net effect on other residents, $bn/year |
|---|---:|
| 0% | +69.0 to +83.4 |
| 20% | −2.5 to +12.8 |
| 25% | −20.4 to −4.9 |
| 50% | −109.8 to −93.2 |
| 75% | −199.3 to −181.5 |
| 100% | −288.7 to −269.8 |

[DERIVATION: for each row of `infra/immigration-fiscal/full_account_2026_09_20/derived/headline_cases.csv`, `W(r)=welfare_bn+(1-r)*services_bn`; match `services_bn` from `response_pools.csv` using allocation, receipt scenario `cbo_collective`, spending scenario `complete_preferred_F_per_capita`. Central roots are 19.30%,20.57%,22.33%,23.61%; the broader preferred-case parameter envelope quoted in the main account is 18.5–25.8%.]

If every other service were held fixed, education alone reaches break-even at **34.6–43.1%** of its assigned cost. Education at 50%, with all other service responses zero, gives **−$30.7bn to −$13.3bn/year**. This is a diagnostic threshold, not an empirically fitted education response. [DERIVATION: `(W(1)+services_bn)/education_services_bn`; then `W(1)+services_bn-0.5*education_services_bn`, using the same four cases.]

## External evidence and interpretation

CBO's June 2025 analysis uses a 1999–2000 to 2019–20 state school-finance panel. Enrollment growth +1 percentage point is associated with per-student spending growth −0.37 points (the decline-side coefficient is −0.34). First-order total-spending response is therefore approximately 63–66% of average cost. This is short-run association, not a long-run Mexican-origin effect. The $5.7bn direct versus $9.4bn potential education totals also reflect pupil displacement and English-learner adjustments, so their ratio is not a clean marginal-cost coefficient. [SOURCE: [CBO, Appendix A, Spending on Education](https://www.cbo.gov/publication/61464), checked 2026-09-20. DERIVATION: total spending = pupils × spending per pupil.]

CBO uses proportional response for public safety, housing/community, health and income-security services, but no immediate response for economic affairs and recreation/culture. Those are category assumptions, not causal estimates. It expressly distinguishes unchanged budgets from crowding. Its recent surge, state/local scope and service definitions differ from our all-level established-population account. Do not transplant these coefficients as a measured weighted r. [SOURCE: same CBO report, General Services and uncertainty sections.]

Cato also allocates its congestible-public-goods spending at full per-capita cost. Consequently our 100% service assumption is not itself a demonstrated explanation of the Cato-versus-our-result sign difference. The category boundaries and allocation proxies still differ. [SOURCE: [Cato report](https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023), All other spending and methodological Congestible public goods sections.]

[ASSESSMENT] Short-run spare capacity and budget rigidity argue against assuming immediate 100% everywhere. Long-run staffing/capacity adjustment and education's large weight argue against treating an overall response below roughly 20–24% as an equally evidenced default. Neither point identifies a replacement national scalar. A fixed budget may shift costs into crowding, workload or private purchases; such effects require separate evidence and cannot be priced as the entire missing budget amount by definition.

Next discriminating evidence: category-specific spending responses at the relevant horizon and population scale, especially a separate K–12/higher-education allocation and enrollment-to-spending response. No headline model parameter is changed by this note. Other assumptions, including the property-revenue bridge, remain unresolved. [INFERENCE]

See the [external evidence review](immigration-service-response-external-evidence-2026-09-20.md) for NASEM/GAO capacity distinctions and a Mariel synthetic-control study. Those sources support category/horizon distinctions, not a fitted universal percentage; the Mariel draft/published multiplier discrepancy prevents quantitative reuse of its marginal-cost multiplier.

Instrument check: this assessment is an LLM synthesis. The direct-response coefficients, threshold arithmetic and scope restrictions above are explicit so the conclusion can be checked independently; neither institution's framing substitutes for identification.
