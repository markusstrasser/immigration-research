# V9: audit of the long-run school-cost response

**2026-10-15. Verdict: no new material correction established.** The assumption
examined is that, in the long-run comparison, the group's pupils carry the full
average K–12 cost. An independent reconstruction supports roughly proportional
spending across districts after controlling for local wages. Changes within
districts over nineteen years give a lower response, close to the alternative
already shown beside v9. Retain that sensitivity. Full cost remains an explicit
counterfactual assumption; this audit does not verify it as an exact causal effect.
[INFERENCE from the calculations and primary sources below]

I selected this link because the existing school alternative moves the proposed
annual account by about $27–30bn and the step from observed spending to the
long-run counterfactual is weakly identified. This is a leverage-and-evidence
judgment, not a proof that every other assumption is better supported. The audit
holds the population, other fiscal responses and accounting basis fixed. Its
materiality rule, written before the reconstruction, was a defensible change
capable of moving the annual account by $5bn.
[DATA: audit [design and scope](../infra/immigration-fiscal/school_response_audit_2026_10_15/README.md)]

The frozen object is **proposed v9 at `fb822a95`**, whose complete annual cost to
other US residents is $344.0–412.6bn in 2024 dollars, including benefit accrual
and the imputed capital return. The cash-accounting companion is
$260.4–328.9bn; it still contains the imputed capital return and is not a debt
flow. Neither is an observed removal outcome. Later candidate edits are outside
this dated audit.
[CALCULATION: [full-account receipt](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/fiscal_sensitivity.json)]

The reconstruction starts from Census's original district-level F-33 files for
FY2000, FY2010 and FY2019, their dictionaries and national summary workbooks.
It uses its own parser and estimator, rather than importing the repository's
school estimates. The concrete attack is that large districts may spend more
because local labor is more expensive: a slope near one could conceal economies
of scale. To test that, I joined the original FY2019 records to NCES's published
Comparable Wage Index for Teachers (CWIFT), an estimate of comparable wages
outside teaching. This is an input-price control, not an instrument or raw
individual wage records.
[SOURCE: [Census files and hashes](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/raw_sources.json),
[NCES archive](https://nces.ed.gov/programs/edge/data/EDGE_ACS_CWIFT2019.zip),
[CWIFT documentation](https://nces.ed.gov/programs/edge/docs/EDGE_ACS_CWIFT_FILEDOC.pdf)]

All rows below regress log current expenditure on log pupils, with state
intercepts; long differences use changes in both logs. Standard errors cluster
by state. Pupil weights are current enrollment for the cross-section and initial
enrollment for changes. The wage comparison uses exactly the same districts
before and after adjustment. A slope of one means proportional spending in that
regression, not proof of proportional savings from removing this population.

| Original-data comparison | Districts | Pupil-weighted slope | 95% regression interval |
|---|---:|---:|---:|
| FY2019, wage-index matched, no wage control | 12,207 | 1.017 | 1.000–1.034 |
| Same districts, controlling for local wages | 12,207 | **1.004** | **0.987–1.020** |
| FY2000–FY2019 long difference | 11,991 | **0.846** | **0.788–0.904** |
| Same long difference, stable Census ID and school level | 11,861 | 0.846 | 0.787–0.905 |
| Long difference excluding California | 11,197 | 0.838 | 0.775–0.901 |

[CALCULATION: [raw estimates](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/raw_estimates.csv),
[wage estimates](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/wage_estimates.csv)]

**The wage attack did not overturn proportionality.** Matching retains 99.6% of
the starting sample's pupils. The lower longitudinal result also survives
straightforward checks: restricting absolute enrollment changes to less than a
doubling/halving gives 0.854. Excluding California was a post-result check prompted
by Census's documentation of charter reclassification; it changes little.
Weighting matters: giving each district equal weight produces 0.934 in the
wage-adjusted cross-section and 0.791 in the long difference. All specifications
are retained. Pupil weights do not identify the response for Mexican-lineage
pupils specifically.
[CALCULATION: estimates above and [match receipt](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/wage_receipt.json);
SOURCE: [Census FY2019 documentation, Appendix B](https://www2.census.gov/programs-surveys/school-finances/tables/2019/secondary-education-finance/school19doc.doc)]

The strongest opposing evidence is persistent spending after enrollment falls.
Lee and Scafidi's original twenty-year results show nearly proportional current
spending with growth, but appreciably stickier spending with decline. Their
twenty-year specification is cross-district OLS, not a district fixed-effects
causal experiment. It estimates percentage changes in spending per pupil, not
a constant-elasticity total-cost curve. This supports retaining the uncertainty;
neither growth nor decline coefficients alone identify v9's national comparison.
Stationarity by itself does not prove a reversible cost function.
[SOURCE: [Lee and Scafidi, methods pp. 17–19, Table 4](https://edworkingpapers.com/sites/default/files/ai25-1266.pdf);
INFERENCE on transport to v9]

CBO's original education analysis addresses the immigration surge's immediate
budget effect using annual state enrollment/spending changes. It supports
separating immediate outlays from a full-cost comparison; it does not settle
this long-run parameter. Neither that paper nor these district regressions
measures a national removal effect with geography, tax bases, pupil needs and
school quality held appropriately comparable.
[SOURCE: [CBO, June 2025, pp. 10, 28–30](https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf);
INFERENCE]

To size the link, the full v9 evaluator changes only the school response,
propagates it through the post-engine components, and reselects the low and high
specifications in both methods. The existing finite-change mapping is
`r = [1 − (1 − s)^β] / s`, with inherited pupil share `s = 0.174806`.
Here β is an assumed elasticity and r the share of full average cost charged.
This curve is a scenario assumption; the regressions do not identify it.

| School scenario | Response r | Annual account, $bn | Change from v9's low / high end, $bn |
|---|---:|---:|---:|
| V9 full average cost | 1.000 | 344.0–412.6 | — |
| Existing alternative, β = 0.836 | 0.849 | 313.9–385.7 | −30.1 / −26.9 |
| Rounded longitudinal estimate, β = 0.85 | 0.862 | 316.6–387.9 | −27.5 / −24.6 |
| Rounded wage-adjusted estimate, β = 1.004 | 1.004 | 344.6–413.3 | +0.6 / +0.7 |

[CALCULATION: [fiscal sensitivity](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/fiscal_sensitivity.json).
These are conditional scenario bands, not confidence intervals. They use one
consistent population and account; no reference-group ledger is scaled into them.]

The independently reconstructed lower response is therefore already represented
by the existing sensitivity. Even setting this K–12 response to zero leaves a positive
$139.8–239.6bn annual account ($56.1–156.0bn on the cash companion), with every
other assumption fixed. That is an extreme mechanical bound, not a plausible
school estimate or a validation of the rest of the model.
[CALCULATION: same receipt]

Checks external to the conclusion constrain what can be claimed. Original-file
spending components reconcile exactly in all three years; an independent
statsmodels fit agrees with the custom estimator and its clustered uncertainty.
Published Census national per-pupil totals are close but **not exact matches**:
raw current expenditure per pupil is 1.01% below Table 8 in 2010 and 0.034% below
in 2019. Published denominator/expenditure adjustments differ; the residuals
were disclosed rather than calibrated away, and their exact decomposition was
not established. The long panel covers 97.9% of baseline and 98.5% of endpoint
sample pupils. These checks support the reconstruction, not causal identification.
[CALCULATION: [coverage](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/raw_coverage.json),
[published benchmarks](../infra/immigration-fiscal/school_response_audit_2026_10_15/derived/raw_benchmarks.json),
[tests](../infra/immigration-fiscal/school_response_audit_2026_10_15/test_raw_audit.py)]

What would change the verdict is evidence identifying persistent enrollment
changes and their long-run expenditure response, with credible comparisons for
funding, local prices and pupil composition. For a budget claim, persistent lower
spending matters even if quality changes; any asserted quality loss needs separate
measurement and valuation. Constant-quality resource costs are a distinct claim.
The present observational estimates cannot choose between these counterfactuals.
The regression intervals omit identification, wage-index estimation and
transport uncertainty. This LLM-assisted audit can favor a convenient interpretation;
retaining the contrary longitudinal evidence and applying the same $5bn rule in
both directions limits, but does not eliminate, that risk. [INFERENCE]

**Disposition:** keep full cost labelled as an assumption and keep the lower
school scenario visible. No new school correction, no change to v9, and no
claim that the full account was validated. The [audit lane](../infra/immigration-fiscal/school_response_audit_2026_10_15/README.md)
contains the original-source receipts, every computed specification, source-read
log, tests and reproduction command. [INFERENCE]
