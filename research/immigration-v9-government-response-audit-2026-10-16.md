# V9: audit of the general-government cost response

**2026-10-16. Verdict: no new material correction established.** The link is
population → long-run general-public-services cost. The original finance data
reproduce v9's calibration, and separately collected employee counts support
its broad scale pattern. Neither identifies the costs that would disappear
with a smaller national population. Retain this as a consequential assumption,
with sensitivity in both directions. [INFERENCE from the evidence below]

The frozen object is **candidate v9 at `a24d2468`**: an annual net fiscal cost
to other US residents of **$368.0–436.6bn in 2024 dollars**, including earned
benefit accrual and an imputed public-capital return. Its cash-accounting
companion is $284.4–352.9bn and also includes that imputation; neither is a debt
flow or an observed removal outcome. This audit changes one response, holding
population, other fiscal responses and valuation rules fixed.
[CALCULATION: [full-account receipt](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/fiscal_sensitivity.json)]

I selected this after the school audit because it combines substantial fiscal
exposure with a weakly identified step from state-size differences to national
costs. Setting this response to zero removes **$34.4–48.8bn** from v9; zero is
an exposure bound, not an estimate. The predeclared materiality threshold was a
defensible revision moving either endpoint by $5bn, or a demonstrated failure
of the source-to-parameter bridge. Selection is a judgment about consequence
and evidence, not proof that every remaining assumption is stronger.
[CALCULATION: same receipt; DATA: [design](../infra/immigration-fiscal/government_response_audit_2026_10_16/README.md)]

The strongest case for v9 is straightforward: administering more people uses
more staff, buildings and supplies, while shared overhead permits economies
of scale. The strongest objection is that larger states also differ in prices,
geography, service choices and organization. A spending association could be
misread as the quantity of resources saved. I tested that objection using
original Census finance, population and employment files, with independent
parsing and regression code. [INFERENCE; SOURCE: receipts below]

The finance reconstruction starts with Census FY2022 Table1, lines106–109:
financial administration, judicial/legal, general public buildings and other
administration. These are direct expenditures including current and capital
spending. Each national amount equals its state/DC sum; every combined amount
equals state plus local. The 2024 BEA component mix also reconciles, including
the federal-grant consolidation. No consequential source or arithmetic error
emerged.
[SOURCE: [original Census workbook](https://www2.census.gov/programs-surveys/gov-finances/tables/2022/22slsstab1.xlsx);
CALCULATION: [cell mappings and identities](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/finance_mapping_checks.json),
[source hashes](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/finance_sources.json)]

All slopes below regress log outcome on log population and an intercept across
the same 50 states in 2022. Intervals are HC3/t regression intervals; they omit
causal and transport uncertainty. A slope of one means proportional association.

| Outcome | Equal-state slope (95% interval) | Population-weighted slope (95% interval) |
|---|---:|---:|
| Administration expenditure, original basket | 0.842 (0.749–0.936) | 0.997 (0.802–1.192) |
| Same, excluding judiciary | 0.800 (0.709–0.892) | 0.951 (0.768–1.135) |
| Full-time employees, finance + other administration | **0.836 (0.771–0.902)** | **0.932 (0.795–1.068)** |
| March payroll, same employee basket | 0.883 (0.784–0.981) | 1.022 (0.784–1.259) |

[CALCULATION: [finance fits](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/finance_fits.csv),
[employment fits](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/employment_fits.csv)]

The payroll decomposition is exact: the equal-state slope is 0.836 for employee
counts plus 0.046 for payroll per employee; population weighting gives
0.932 + 0.090. Financial administration alone gives employee slopes of
0.847 and 0.952. Excluding Alaska/Hawaii gives 0.856 and 0.939 for the combined
employee basket. Thus the pattern is not just higher pay in larger states.
Average payroll is not a constant-quality wage index, and these are published
reported/edited/imputed counts, not individual payroll microrecords.
[CALCULATION: [decomposition](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/employment_decomposition.csv);
INFERENCE on the price-only explanation]

The employment check has real limits. Census excludes contractors; imputation
can use population-scaled donors. Its full-time-equivalent series has been
modeled since 2019, so actual full-time counts are primary here and FTE is
secondary. Buildings cannot be separately matched in employment, while BEA
classifies courts outside general public services. The staffing basket is
therefore a narrower check, not a replacement measure of all resource cost.
The original 2022 published extracts were acquired on October16, 2026; revised
source values and all computed specifications are pinned and retained.
[SOURCE: [Census methodology, pp.1–4](https://www2.census.gov/programs-surveys/apes/technical-documentation/methodology/22_methodology.pdf),
[classification manual, functions23/29/89](https://www2.census.gov/govs/class06/2006_classification_manual.pdf),
[BEA Government Transactions, Appendix I](https://www.bea.gov/sites/default/files/methodologies/mp5.pdf);
DATA: [employment receipts](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/employment_sources.json)]

The full v9 evaluator transports the response through operating costs,
completion carriers, public capital, coverage and count corrections. It
reselects endpoints and reproduces the frozen baseline exactly. The inherited
power-cost curve is `r = [1 − (1 − s)^β] / s`, with `s = 0.129182`.
The low end applies separate slopes to the BEA components and holds federal
executive/legislative cost fixed; the high end applies the administration slope
throughout. Both the curve and federal transport are assumptions.

| Single-link scenario | Annual account, $bn | Change from low / high endpoint, $bn |
|---|---:|---:|
| V9 response 0.601 / 0.851 | 368.0–436.6 | — |
| Original basket, independently reconstructed | 368.0–436.6 | +0.01 / +0.02 |
| Exclude judiciary, equal-state fit | 366.6–434.3 | −1.4 / −2.3 |
| Original basket, population-weighted fit | 374.0–444.9 | +6.0 / +8.4 |
| Exclude judiciary, population-weighted fit | 372.5–442.5 | +4.4 / +5.9 |
| Proportional response everywhere | 390.9–445.1 | +22.9 / +8.5 |
| Zero response, mechanical bound | 333.6–387.8 | −34.4 / −48.8 |

[CALCULATION: [fiscal scenarios](../infra/immigration-fiscal/government_response_audit_2026_10_16/derived/fiscal_sensitivity.json).
These are conditional model bands, not confidence intervals. Both accounting
bases are in the receipt; the half-response row is a linearity check.]

The narrower basket does not produce a material correction. Weighting produces
a material upward sensitivity, but gives no causal reason to replace the
current coefficient. The same evidential standard applies to both directions.
Finance fits excluding Alaska/Hawaii and including DC, and secondary FTE fits,
are retained in the linked tables; none is selected as a fiscal estimate.
[INFERENCE]

The unresolved link is causal. The earlier within-state and county-IV work
already found insufficient precision to distinguish the competing responses.
Its documented finance reporting break is not a newly discovered flaw in the
published Table1 used here. This audit does not recycle that result as a new
finding. It independently checks the measurement and a specific price-based
objection; it does not measure national removal.
[DATA: [administration panel and dated correction](immigration-administration-response-test-2026-09-20.md),
[completed county-IV results](../infra/immigration-fiscal/gg_response_county_iv_2026_09_23/RESULT.md)]

What would change the verdict is a credible persistent population change with
comparable service obligations, input prices and outsourcing, identifying the
response of this same resource pool. In the current account, about **0.087**
of response changes an endpoint by $5bn. Published totals, independent
estimator agreement and frozen-case replay can establish that this audit's
calculation is right; they cannot establish that its counterfactual is right.
No case parameter is changed. [CALCULATION: receipt; INFERENCE]

Instrument note: this is an LLM-assisted audit of a politically charged claim.
The predeclared threshold, retained opposing specifications and primary-source
checks constrain selective interpretation; they do not remove it.
[INFERENCE; [project caveat](../notes/llm-bias-caveat.md)]
