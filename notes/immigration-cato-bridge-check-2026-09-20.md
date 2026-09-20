**Verdict:** Our negative number is a conditional 2024 Mexican-origin model, not an estimate comparable directly with an all-immigrant historical account. Its arithmetic reconciles; its causal response assumptions remain unestimated. No evidence about Cato dishonesty follows from this discrepancy. [INFERENCE from verified local code, CSVs and the Cato methods below.]

## Exact local arithmetic

All amounts below are billions of nominal 2024 dollars; order is shared/personal household-resource attribution. [SOURCE: `infra/immigration-fiscal/full_account_2026_09_20/derived/accounts.csv`, lines 24–25 and 29–30; `derived/response_pools.csv`, lines 3 and 5.]

| Step | Shared | Personal |
|---|---:|---:|
| All assigned receipts | 545.118771 | 517.100248 |
| Assigned spending with defense/general government/legacy domestic interest excluded | 738.271575 | 732.314498 |
| Assigned fiscal balance | −193.152804 | −215.214250 |
| Remove incidence receipts given zero direct causal response | −100.305017 | −92.577911 |
| Remove spending on business subsidies held fixed | +10.323310 | +10.285902 |
| Direct fiscal response A | **−283.134510** | **−297.506259** |

The direct calculation agrees independently: shared `444.813755 − 374.736103 − 353.212162 = −283.134510`; personal `424.522337 − 364.269254 − 357.759342 = −297.506259`. Terms are direct receipts, household transfers and ordinary services. [DERIVATION from `response_pools.csv`, lines 3/5; implementation `welfare.py:77–78`.]

The public-cost exclusion itself is **285.610114** in both allocations: defense/general public services 151.071826 plus legacy domestic interest 134.538288. It changes the allocation convention, not measured use or the national deficit. [SOURCE: same response pools; account rows above; `research/immigration-complete-annual-account-2026-09-20.md:53–61`.]

## Receipts removed before the production bridge

The code retains only `personal_income` and `household_direct`, then explicitly excludes both corporate incidence categories and all property categories. It also excludes other-business and public-asset flows. [SOURCE: `infra/immigration-fiscal/full_account_2026_09_20/welfare.py:19–32`.]

| Excluded category | Shared | Personal |
|---|---:|---:|
| Corporate capital incidence | 18.501729 | 15.495291 |
| Corporate labor incidence | 14.571831 | 13.810357 |
| Owner property | 24.970043 | 24.970043 |
| Remaining production property | 13.280196 | 11.122230 |
| Personal property tax | 0.482760 | 0.404314 |
| Other production taxes | 5.399196 | 4.521854 |
| Business current transfers | 5.202866 | 4.357426 |
| Government asset income | 23.602970 | 23.602970 |
| Enterprise surplus | −5.706818 | −5.706818 |
| Source rounding | 0.000243 | 0.000243 |
| **Total** | **100.305017** | **92.577911** |

[SOURCE: `infra/immigration-fiscal/full_account_receipts_2026_09_20/derived/category_allocations.csv`, default `cbo_collective`, shared lines 20–46, personal lines 308–334.]

This subtraction prevents treating assigned tax incidence as automatically disappearing causal revenue. The production model then adds private benefits plus induced taxes: +8.79 cash-scaled or +13.32 GDP-scaled in source-centered cases. Those totals are **not** evidence that the above category-specific exclusions have each been empirically identified or individually replaced. [SOURCE: complete annual account, lines 70–112. INFERENCE: distinction between response assumptions and identified effects.]

In particular, owner property taxes are excluded in the integration, while the benefit model has no separate housing sector and explicitly makes no exact property-overlap claim. This is an unresolved limitation of our causal bridge, not evidence that the entire excluded property-tax amount would necessarily disappear or persist. [SOURCE: `infra/immigration-fiscal/full_account_benefits_2026_09_20/README.md:73–77`; integration response mapping above.]

## Assumptions and comparison boundaries that matter

- Population: 40.896574m observed Mexican-origin residents, including native-born descendants identified by own/parent birthplace or Mexican identification with US-born parents; all ages and education, not all immigrants or exclusively low-skilled immigrants. This includes later observed generations while missing unidentified distant descendants. [SOURCE: annual account lines 16–29.]
- Time/unit: one year's nominal 2024 current account and stationary labor counterfactual; not a 1994–2023 cumulative history, lifetime NPV, admission effect or removal saving. [SOURCE: annual account lines 16–25; integration README lines 3–14.]
- Revenue and spending are survey-proxy allocations of BEA national totals, not administrative origin-linked tax/benefit records. National accounting closure is not causal identification. [SOURCE: annual account lines 27–29; receipt README lines 15–23 and 44.]
- Main causal choice: household benefits and **100% of assigned ordinary services** respond; defense/general government, legacy interest and subsidies are fixed. Full service response remains unestimated. With fully adjusted private capital, reported preferred-case break-even occurs at only 18.5–22.7% personal / 21.5–25.8% shared service response. Thus our sign depends strongly on incremental public costs. [SOURCE: annual account lines 70–83, 160–183.]
- Welfare benefits accrue to other residents (including other immigrants), excluding target members' own welfare. Core capital ownership is entirely other residents; capital adjusts fully; fiscal dollars valued at one; overlap O=0. These are declared assumptions, not jointly estimated parameters. [SOURCE: annual account lines 21–25 and 70–93.]
- The $262–357bn grid is neither a confidence interval nor all possible error. The largest pessimistic spending change replaces expected Medicaid dollars with coverage headcounts, adding $68.70bn in the illustrated endpoint. The source-centered result is $270–289bn, still conditional. [SOURCE: annual account lines 106–163.]

## Cato comparison checked against the primary report

Cato's first-plus-second-generation result is +$7.9 trillion including modeled interest savings over 1994–2023, in real 2024 dollars, across government levels. It pools origins and education and excludes G3+. It is not a Mexican-origin annual balance or an estimate of welfare accruing to other residents. The combined result includes both G2 revenue and expenditure; the accusation that this result simply omits children is not supported. [SOURCE: [Cato report](https://www.cato.org/white-paper/immigrants-recent-effects-government-budgets-1994-2023), Table 13; local corrected audit `research/immigration-dismantle-cato-2026-06-25.md:28–38`.]

Cato assigns no pure-public-goods costs to immigrants/G2, credits indirect property-tax revenue, and uses 70% labor / 30% capital corporate-tax incidence. Our latest welfare headline also holds defense/general government and legacy interest fixed, so that exclusion alone cannot explain the opposing signs. Population, period, allocation rules and causal-response treatment remain unmatched. [SOURCE: Cato sections Government Spending and Government Revenues; local account lines 70–83. INFERENCE: comparison boundary.]

Cato calls its model a lower bound because of omitted positive spillovers. That conclusion needs bounds on uncertain allocations and omitted adverse effects too. Our negative result likewise cannot be promoted to a measured causal loss: full ordinary-service response is assumed, and the housing receipt bridge is incomplete. Neither criticism establishes intentional falsification. [SOURCE: Cato Static model discussion; local model qualifications above. INFERENCE / FRAMING-SENSITIVE.]

Coverage: checked annual account, integration and receipt READMEs, actual response mapping, account/response/category CSV rows, benefit-interface qualifications and Cato's primary report. Did not rerun raw CPS or apply both models to an identical population/year. Consequently no numerical attribution of the full Cato-versus-our-result gap is established. No model code or numerical outputs changed.
