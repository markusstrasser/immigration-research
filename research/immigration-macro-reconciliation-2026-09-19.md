# National reconciliation and the updated annual fiscal account

**Verdict:** Updating available state/local inputs to observed FY2024 worsens the
Mexican-origin union's annual attributed balance by **$17.02bn**, to **−$234.34bn
under household sharing or −$256.26bn under personal-source attribution**.
These remain expanded partial fiscal accounts, not estimated policy savings or
a complete net cost to America. The national reconciliation now exposes the
remaining differences under consistent official boundaries; it does not assign
them to demographic groups. [CALCULATION; FRAMING-SENSITIVE]

Scope: the same 40.896574m CPS ASEC2025 civilian-household residents, including
all observed generations and education levels. Income year and dollar prices
are 2024. It is neither a low-education-only nor a complete genealogical count.
Reproduce with the [generator and source contract](../infra/immigration-fiscal/macro_closure_2026_09_19/README.md).

## 1. New source vintage, same attribution rules

[SOURCE] Census published its [2024 state/local finance release](https://www.census.gov/data/datasets/2024/econ/local/public-use-datasets.html)
in July 2026. The former account used 2022 general-service and capital spending
repriced to 2024. The new calculation uses actual 2024 state/DC spending, mapped
fees, 2024 population denominators, and combined state/local corporate and
selective-sales tax receipts. The old tax pools covered states only. Original
incidence and all other components are held fixed; this isolates the refresh.

| Union component | Previous signed balance, $bn | Updated, $bn | Change, $bn |
|---|---:|---:|---:|
| General services G, net of mapped fees | −142.416 | −163.186 | −20.770 |
| Nonduplicated capital P | −6.546 | −9.000 | −2.454 |
| Corporate-tax credit C | +34.550 | +35.188 | +0.638 |
| Excise/selective-sales credit X | +37.722 | +43.285 | +5.563 |
| **Net change** | | | **−17.022** |

[CALCULATION: `finance_vintage_effects.csv`.] Fees are grossed up on both sides
for receipt/outlay presentation, with no net effect. Source amounts are thousands
of dollars; independent US totals reconcile the state sums. The population
file's Puerto Rico row is outside this finance/CPS universe and is excluded.

| Allocation | Attributed receipts including fees, $bn | Attributed expenditure, $bn | Balance, $bn |
|---|---:|---:|---:|
| Household sharing | 444.422 | 678.761 | **−234.339** |
| Personal source | 422.914 | 679.178 | **−256.263** |

[CALCULATION: `finance_vintage_totals.csv`.] The two rows are allocation
conventions, not uncertainty bounds. The $17.02bn update is about 7–8% of the
former deficit. Older lifetime sensitivities deliberately retain their pinned
age-profile version; this update is not a flat per-person lifetime correction.

## 2. Which national total is being reconciled?

[SOURCE] The [BEA section 3 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx),
August 26, 2026 vintage, reports calendar-2024 government current receipts
**$8,008.290bn**, current expenditure **$10,061.458bn** and current saving
**−$2,053.168bn**. Including the capital account yields total receipts
**$8,057.709bn**, expenditure **$10,424.075bn** and net borrowing
**−$2,366.366bn**. Those balances measure different objects. See [BEA accounting definitions](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf).

Federal and state/local current receipts and spending each contain the same
**$961.474bn** intergovernmental grant flow; subtract it once when consolidating
each side. The generator verifies the identities directly from tables 3.1–3.3.
Government service sales are netted symmetrically for the BEA diagnostic. The
resident model still mixes current/capital and fiscal/calendar-year inputs.

| Updated national account, $bn | Household sharing | Personal source |
|---|---:|---:|
| Modeled receipts, symmetrically net of service fees | 5,943.179 | 5,870.879 |
| Modeled expenditure on the same presentation | 6,706.010 | 6,686.736 |
| Modeled balance | −762.831 | −815.857 |
| Difference from BEA current saving | −1,290.337 | −1,237.311 |
| Difference from BEA net borrowing | −1,603.535 | −1,550.509 |

[CALCULATION: `updated_national_bridge.csv`.] These are **unallocated
differences**, not measured omitted immigration costs. They mix omitted items,
universe, reporting, tax-incidence, price/year and current/capital definitions.
Receipt and expenditure differences are exported separately; netting alone
would conceal offsetting coverage failures. Corporate, personal/social and
production/import tax comparisons are broad diagnostics, not exact line matches.

The separate Census general-finance/OMB FY2024 comparator is **−$1,662.517bn**:
federal receipts plus state/local own revenue, less federal outlays plus direct
general expenditure net of federal grants received. This excludes enterprise and
insurance-fund accounts and combines different fiscal year ends. It is not NIPA
net borrowing or a perfectly simultaneous consolidated cash balance. BEA's
published Census-to-NIPA table 3.19 ends in 2023; a full 2024 source bridge is
therefore unavailable. [SOURCE / CALCULATION: `fiscal_year_comparators.csv`,
`official_cells.csv`; Census API and BEA workbook.]

## 3. Attribution versus spending that changes

[CONDITIONAL ARITHMETIC] Let q be the fraction of assigned gross spending that
actually disappears in a hypothetical absence of this entire population, while
all its assigned receipts disappear. Budget improvement is `q × spending − receipts`.
The calculation assigns no actual policy a value of q and includes no transition
cost, substitution or behavior. It is a diagnostic of the attribution assumption.

| Spending response q | Shared budget change, $bn | Personal-source change, $bn |
|---|---:|---:|
| 0% | −444.4 | −422.9 |
| 50% | −105.0 | −83.3 |
| 75% | +64.6 | +86.5 |
| 100% | +234.3 | +256.3 |

[CALCULATION: `updated_policy_arithmetic.csv`.] Break-even q is **65.5% or
62.3%**, respectively, under these deliberately strong receipt-loss assumptions.
Assigning average defense/interest/general-government F would add **$211.65bn**
to this population's attributed spending, but does not establish that those
budgets would fall by that amount. The optional F grid is exported separately.

## Consequence and limits

[INFERENCE] The source refresh strengthens the measured negative partial
balance. It does not close the national coverage gap or identify a policy effect.
The strongest remaining empirical requirement is component-specific recipient,
financing and expenditure-response evidence. Arbitrarily distributing the
residual would produce precision without identification.

The [matched benefits](immigration-matched-benefits-2026-09-19.md) and
[projection checks](immigration-projection-backtest-2026-09-19.md) supply the other
two requested calculations. Their capital-tax replacement arithmetic and lifetime
sensitivities use the earlier pinned account, labeled accordingly. None is
silently added to this new annual total. Crime and other social valuation are
outside this fiscal release.

Validation: source hashes; published national anchors; grants/current/capital
identities; exact target/rest/national partition; canonical release reproduction;
Census state-to-US controls; source-units, duplicate-field and geographic-universe
regressions; fee-loss endpoint; refreshed receipt-minus-spending identity. Source
survey uncertainty and structural uncertainty are not eliminated by arithmetic
checks. Interpretation remains subject to the [instrument caveat](../notes/llm-bias-caveat.md).
