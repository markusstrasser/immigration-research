# Conditional fiscal and economic-benefit integration

The generator replays every existing matched CES scenario and extends its already
declared capital-ownership endpoints across the full grid. It supplies the missing
accounting bridge, not an automatic subtraction of a fiscal allocation from income.

Run from a repository environment with numpy/pandas/openpyxl/pyreadstat/duckdb:

```sh
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with numpy --with pandas --with openpyxl --with pyreadstat --with duckdb python3 builder.py --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with numpy --with pandas python3 -m unittest discover -s . -p 'test_*.py'
```

`--out` selects an ignored output directory. `--fiscal-response FILE.csv` executes
the conditional fiscal combination using explicit component assumptions from the
parent full-account model. No default response is silently inferred. Every build
replays the upstream generator against its actual raw inputs, checks all1,296
point estimates, and reproduces all18 pre-existing ownership scenarios.

## Beneficiaries, direction and equations

Beneficiaries are other US residents outside the canonical40.896574m observed
Mexican-origin civilian-household population, all ages and education. The model
compares stationary economies with versus without target labor. It does not
identify a historical no-immigration path, incremental admissions, removal or
descendant lifetime costs. The fiscal-response assumptions must describe that
same comparison. Incidence allocation does not prove revenue disappearance.

All changes below are **with target minus without target**, in2024$bn/year:

```text
A = direct target receipt response - target/service spending response
P = other residents' private after-tax money-metric WTP from CES
F = CES change in current labor/capital tax receipts
M = reduction in transfers to other residents from wage changes
O = tax revenue already inside A and also inside F
beta = value/recycling of an extra fiscal dollar to included residents
Z = other nonoverlapping, same-counterfactual benefits (left unpriced)

budget change = A + F + M - O
private change = P - M
conditional welfare = P - M + beta*(A + F + M - O) + Z
beta=1: conditional welfare = P + F + A - O + Z
beta=1 break-even: A - O + Z = -(P + F)
```

The main conditional interpretation uses beta=1; beta=0 is a valuation endpoint,
not an empirical estimate. Included taxpayers' transfers cancel at beta=1.
`M` is separately switchable as none/source2017. Adding M only to the budget
would double count a transfer. Gross private income plus F also double counts
taxes: use P and F, or their already-conserved sum. Beta0 has no fiscal-response
break-even; only private outcomes and Z can change its sign.

The same model permits excluded capital-owner shares0/.5/1. Zero is the core
assumption: all initial capital belongs to included other US residents. The
other two are unestimated ownership endpoints (target-group or foreign owners),
not a measured range. Retention0/.5/1 concerns taxes on the alternative capital
return; opportunity income is already deducted. With excluded owners, the
included group can retain tax revenue while excluding those owners' private
loss; that distributional convention explains large positive sensitivities.

## Fiscal interface and low-overlap branch

`fiscal_response_template.csv` names required columns:
`fiscal_case,component,receipt_change_bn,spending_change_bn,tax_overlap_bn,`
`fiscal_recycling_weight,transfer_phaseout,source_rule`.
Each case has unique components, one beta0/1 and one transfer rule `none` or
`source_2017`. All changes and rules must be supplied; negative spending offsets
remain signed. `source_rule` must document why the component changes in the
counterfactual. Aggregate declarations may enter as explicitly named components,
but the builder does not validate their empirical plausibility.

For a lower-overlap response branch, exclude incidence-allocated corporate C,
production/business-property and government asset-income pools from A before
using the CES capital-tax channel. Treat owner housing separately: the source
capital-tax adjustment distinguishes imputed owner housing, but our GDP-normalized
CES has no separate housing sector, so no exact property-overlap claim is made.
Personal income tax mixes labor and capital; if
included, preserve an explicit O_personal_capital sensitivity. A stricter payroll
and consumption-only branch can avoid assigning all personal income taxes, but
is incomplete and not a preferred complete fiscal estimate. Current CPS FICA,
employer proxies and tax breakdowns are exported; they remain modeled liabilities.
The capital-tax rate.246 excludes sales, not every other possible tax overlap.
Consumption can be financed by capital income, so a consumption-tax response
still needs its own behavioral assumption; this is no clean measured branch.
No tax-incidence scenario by itself establishes a direct government response.

Cost response is separately required: private transfers might disappear, school
costs may adjust with pupils and capacity, and defense/debt need not change.
Shared services, pensions, institutions, capital and grants need their own
response rules. Preserve fee grossups symmetrically and negative lunch offsets.
The component interface retains current amounts without filling response shares.
Budget-normalized relative contribution D is a useful descriptive comparison;
it never enters this welfare equation as if it were a budget response.

## Outputs and limitations

- `benefit_scenarios.csv`:3,888 point scenarios, all upstream CES/tax parameters,
  source and alternative education splits, cash/GDP normalization, capital/hours
  responses and ownership endpoints. Core original joint161-weight SE is retained;
  new ownership rows have no invented covariance or sampling interval.
- `benefit_grid_summary.csv`: extrema grouped by normalization, ownership,
  capital and hours response. These are grid extrema, not bounds on all benefits.
- `current_component_contract.csv` and `current_tax_details.csv`: current school-
  revised fiscal amounts and measured tax-field partition; no automatic response.
- `conditional_combination.csv`, only with supplied response CSV: all scenario
  combinations, budget/private effects and additional nonfiscal benefit needed
  for zero. A negative threshold means no positive residual benefit is needed.
- `audit.json`: exact source/code/output hashes, formula and exclusions.

`mechanism_contracts.json` records why existing crime, service-price, hedonic and
cultural evidence cannot be appended to this beneficiary/population/counterfactual
account. Those mechanisms remain an unpriced Z; absence from the sum is not zero
effect. Fiscal and benefit grids exclude model/transport uncertainty, innovation,
trade, housing supply, endogenous education, and transition/removal costs.
