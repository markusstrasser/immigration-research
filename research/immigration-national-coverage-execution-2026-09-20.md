# Executed national receipt and expenditure coverage checks

**Verdict:** Much of the national discrepancy can be located in named categories.
The large remainder is still a mixed-accounting residual, not a measured ethnic
cost. The model's existing public-goods allocation alternative adds about $1.74tn
to national attributed spending. Seven further gross function pools are not
treated as additional spending because grant ownership remains unresolved.
Missing general sales/property coverage
and other revenue categories also matter. Neither side should be silently
distributed by population share. [CALCULATION / INFERENCE]

This executes the national-coverage part of the [September 19 diagnosis](immigration-gap-diagnosis-and-data-2026-09-19.md).
Amounts below are annual national billions of dollars, source/model income year
2024; BEA vintage August 26, 2026. The fiscal model retains household-shared and
personal-source alternatives and is not an identified immigration-policy effect.

## Receipt discrepancy, now exhaustively partitioned

[SOURCE / CALCULATION] The [BEA section 3 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx)
tables 3.1/3.4/3.5/3.6 are compared with verified component exports from the
current resident model. No new source total is used to calibrate ethnic shares.
The following uses household-shared allocation; the generator exports both.
Positive differences mean BEA exceeds the modeled amount, not necessarily
underreporting or missing household tax payments.

| Receipt category | BEA less model, $bn | Main comparison limitation |
|---|---:|---|
| Federal personal income tax | +384.80 | Tax liabilities, collection timing, credits and survey population |
| State/local income tax | +42.79 | State simulation versus state/local receipts |
| Other personal taxes | +48.83 | Licenses and other taxes not explicitly modeled |
| Employee/self-employed OASDI and HI | −21.55 | Tax simulation, coverage and population |
| Employer OASDI and HI | −44.56 | Model's all-covered wage proxy |
| Medicare supplementary premiums | +145.12 | Not represented in modeled payroll receipts |
| Other domestic social contributions | +93.35 | UI, railroad, workers compensation and other funds |
| Corporate income tax | −42.55 | FY pool versus calendar-year accounts |
| General sales taxes | +312.44 | Consumption proxy versus total including business purchases |
| Production/property taxes | +357.29 | Owner-housing proxy versus wider property base |
| Excise/selective sales taxes | +14.87 | Fiscal/calendar timing and definitions |
| Customs duties | +83.59 | No explicit tariff incidence in the model |
| Other production taxes | +145.26 | Licenses, assessments and other product/production taxes |
| Rest-of-world taxes/contributions | +45.31 | Outside domestic household frame |
| Government asset income | +196.29 | Interest, rents, royalties and dividends |
| Current transfer receipts | +284.38 | Fines, settlements and other transfers |
| Enterprise operating surplus | −47.46 | Net enterprise losses, not ordinary household taxes |

The full table includes a $0.002bn published-rounding row. Every modeled receipt
is accounted for once, and the differences sum to the total residual. [CHECK]

[CALCULATION] Reclassifying modeled EITC/ACTC from negative receipts to spending
raises both sides by $66.90bn shared/$64.87bn personal and changes neither net
balance. After that presentation adjustment, the receipt residual is about
$2.00tn shared/$2.07tn personal. This is not evidence that all official refundable
credits or income-tax receipt concepts have been matched.

## Expenditure: explicit exclusions versus unresolved remainder

| National spending bridge, $bn | Shared | Personal |
|---|---:|---:|
| Raw model-to-BEA current-spending difference | 3,355.45 | 3,374.72 |
| After moving the modeled credits to spending | 3,288.55 | 3,309.85 |
| After the existing F average-cost arm | 1,545.88 | 1,567.19 |

[CALCULATION / FRAMING-SENSITIVE] The F alternative represents $1,742.66bn across
the modeled civilian household population. Seven zeroed functions have gross
pools of $320.78bn on the same population ratio. They are international affairs,
science/space, energy, natural resources/environment, agriculture, commerce/housing
credit and community/regional development. They are actual source categories
that the central federal residual module assigns zero. **Their gross pools are
not additional consolidated spending:** federal grants can finance final
state/local services already counted in G/P. This step was removed during review;
the separate export flags unresolved ownership and cannot reduce the residual.
Public-good allocation remains a convention; these amounts are not avoidable
immigration-policy costs. Their FY2024 source values are not perfectly matched
to NIPA calendar-year current spending, so the waterfall is not a completed
NIPA expenditure reconciliation.

[SOURCE / LIMIT] BEA current spending includes consumption of fixed capital;
the total-account bridge adds gross investment and other capital transactions
and subtracts that consumption. Government enterprises and service sales also
have specific boundaries. See [BEA's government-account methodology](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf).
The current model combines FY/CY inputs, some capital and institutional costs,
and survey allocations. The remaining $1.55–1.57tn cannot be relabeled a single
missing expenditure category or allocated ethnically without more evidence.

## Reproduction and consequence

The [generator and boundary tests](../infra/immigration-fiscal/national_coverage_2026_09_20/README.md)
verify source hashes, source-year/units, the receipt partition, every existing
modeled receipt, credit reclassification neutrality and the official capital
identities. The full build and four boundary tests pass. The change adds a
diagnostic crosswalk; no group-specific tax or spending correction is applied.

[INFERENCE] This narrows the explanation: the aggregate spending shortfall is
partly an explicit attribution choice, while the receipt shortfall includes
categories that the household construction never attempted to measure fully.
The findings do not establish either a positive complete balance or a validated
negative complete balance for the Mexican-origin population. The next revisions
must use the actual school/tax/health checks, preserving their population and
measurement boundaries. The project's LLM instrument caveat applies; arithmetic
and source definitions, not agreement with a desired sign, govern inclusion.
