# Complete current-receipt attribution, 2026-09-20

**Result:** The complete default accounting arm assigns **$545.119bn shared / $517.100bn personal** in calendar2024 receipts to the observed40.896574m Mexican-origin population. The corresponding current partial ledger, after removing neutral fee grossups and presenting federal refundable credits as spending, assigns **$434.450bn / $411.512bn**. The difference is **+$110.668bn / +$105.588bn** in conditional receipt attribution. It is not an identified fiscal benefit or money that disappears under an admission/removal policy. The parent analysis owns spending and combined fiscal conclusions. [CALCULATION: `derived/scenario_totals.csv`, `credit_presentation.csv`]

All rows exhaust **$8,008.290bn BEA2024 current receipts**. Each row satisfies national = target + other + external + unallocated. The evidence-only diagnostic retains signed unallocated residuals; the ten conditional complete arms have none. BEA rest-world taxes, contributions and transfers supply **$48.652bn** identified external receipts. No unknown residual is renamed foreign. Negative enterprise surplus remains negative. Government user fees are not added again: BEA consumption is already net of sales. Capital transfers are outside this current account. [SOURCE: [BEA Section3 workbook](https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx), Tables3.1/3.4/3.5/3.6, August26,2026 vintage; pinned bytes and direct parent-line checks]

## Population and allocation

The target includes all ages/educational levels in the existing observed Mexican-origin union. It is not a low-skill-only population. `shared` allocates source amounts equally within the existing SPM resource unit before weighted group aggregation; `personal` follows the source person's amount. Existing owner-property amounts preserve the canonical convention in both arms. Consumption is already a unit resource allocation. Survey dates and income years are distinct: CPS ASEC2025 incomes are2024.

The household denominator is336.727803m. Complete tax pools are transported to household allocation keys; the other-resident bucket includes excluded domestic residents with implicitly zero direct allocation from these keys. That is a closure assumption, not evidence of zero taxes outside CPS. Collective public assets instead use the pinned Census July2024 resident denominator340.110988m: target share12.02448%, with the remaining population in other. No target institutional/territorial lineage is imputed. The tax-base public-asset alternative uses the household tax proxy. All public-asset and enterprise rows have causal response fixed at0, whichever ownership convention applies. [SOURCE: pinned [Census population file](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/state/totals/NST-EST2024-ALLDATA.csv); CALCULATION: allocation_keys]

## Fixed incidence rules

- Income taxes: positive modeled federal liability; positive after-credit state liability. Negative state after-credit observations remain in the evidence-only account, but cannot serve as nonnegative allocation weights. The refundable/nonrefundable state-credit split is unavailable. The alternative federal arm retains observed group dollars and allocates only the positive national gap through observed tax liability on AGI≥$500,000. The matched2023 check motivates investigating the high tail; it does not validate this2024 group transport.
- OASDI and HI: separate capped/uncapped wage keys; self-employment uses the statutory combined proxy with the shared wage cap and threshold. Actual coverage exemptions remain unresolved. Employer payroll is assigned to labor, following the incidence convention; this is separate from corporate labor incidence.
- Corporate:75% positive interest/dividend/net-rent income and25% wages. The [CBO AppendixA method](https://www.cbo.gov/publication/60706) additionally uses adjusted capital gains, absent here; this proxy is incomplete. CBO's consumption-excise and employer-payroll conventions guide those rows, without reproducing its CEX model.
- The [Treasury summary](https://home.treasury.gov/system/files/131/Summary-of-OTA-Distribution-Methodology-05102021.pdf), footnote4, gives81.5%capital/18.5%labor at2022 income levels. Our arm is that historical illustration, not a new2024 Treasury estimate. Treasury's full excise method is not replicated.
- The [NAS Annex8-2](https://www.nationalacademies.org/read/23550/chapter/13), pp473–477, uses80%dividend/interest and20%wages, Medicare recipients for supplementary contributions and positive-FICA workers for UI. Our NAS arm changes corporate incidence only. We explicitly extrapolate the worker key to the heterogeneous other-contribution residual. We do not apply old first-generation remittance assumptions to descendants.
- General sales, excises, customs and personal transfers use positive SPM resources as a consumption proxy. This does not observe consumption or its capital/labor financing. Personal vehicle taxes use adult exposure; personal property uses asset income; other personal taxes use the state-tax proxy.
- The existing owner-property model is retained once; only the difference to the BEA production-property total is allocated to capital, or to consumption in a separate pass-through stress. This residual contains both rental and business property. Other production taxes and net business current transfers use capital. These are explicit assumptions, not measured Mexican tax incidence.

Individual income-tax liabilities cannot be separated into marginal capital and labor tax from these public fields. `income_tax_source.csv` therefore leaves identified capital tax missing and the complete target liability `source_unknown`; observed asset-income shares are separate proxy columns. This prevents a false capital-tax subtraction or double counting in the parent's welfare calculation.

## One-at-a-time sensitivities

Each row changes one rule from `cbo_collective`; these are **not joint uncertainty bounds**. Amounts are target receipts in billions, shared/personal:

| Scenario | Shared | Personal |
|---|---:|---:|
| cbo_collective |545.119|517.100|
| federal_gap_high_agi |535.635|507.511|
| treasury_815 |542.934|514.852|
| nas_80 |543.309|515.802|
| corporate_all_capital |536.714|508.455|
| property_residual_consumption |560.793|534.933|
| public_assets_tax_base |535.765|507.144|
| capital_external_50 |523.927|499.352|
| capital_external_100 |502.735|481.603|
| medicare_income_weighted |541.181|513.091|

Foreign capital fractions0/.5/1 are mathematical sensitivities, not observed ownership shares or confidence limits. They affect corporate capital, residual property, other production and business transfers. Medicare's alternative weights enrolled recipients by positive AGI+1; it stresses income-related premiums, without simulating statutory IRMAA. Source-based corporate conventions and accounting alternatives were fixed before combined fiscal results. The inherited ledger's larger/smaller sign was not a selection criterion.

**Disconfirmation and limits:** Missing gains and survey high-income undercoverage can alter both capital shares and tax allocations; national controls cannot identify ethnic incidence. The target wage share8.32–8.78%, capital share3.11–3.72% and federal liability share5.33–5.74% differ substantially from its12.15% household population share. A universal population rake is contradicted by the held microdata. Conversely, these proxy contrasts do not establish who ultimately bears each business tax. Replicate SEs describe sampling error for keys, not model uncertainty or a fiscal confidence interval. National control closure deliberately replaces incomplete revenue coverage by an explicit model; it does not turn that model into a causal result.

## Reproduce and integrate

From the canonical repository working directory, with its runtime:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with pandas --with numpy --with openpyxl --with pyreadstat --with duckdb python3 /ABS/PATH/full_account_receipts_2026_09_20/builder.py --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with pandas --with numpy --with openpyxl python3 -m unittest discover -s /ABS/PATH/full_account_receipts_2026_09_20 -p test_builder.py -v
```

`category_allocations.csv` supplies scenario/allocation/category, the four disjoint buckets, proxy share, source locator, response class, capital fraction, scope and identification metadata. Corporate labor/capital, owner/remaining property and product taxes stay separate. `response_class` describes incidence; the parent must explicitly choose policy responses. It must not infer disappearing receipts from the class name. `credit_presentation.csv` moves EITC+ACTC to spending once and strips neutral fee grossups from both sides. Never add the receipt uplift without that presentation bridge. `audit.json` binds code, dictionaries, all used input bytes and five exported CSVs. Derived outputs are ignored; no raw sources are changed.

Validation: seven boundary/conservation tests, including absent-proxy rejection; all161 CPS replicate group partitions; a separate pandas weighted-wage oracle; signed row/global identities; direct BEA personal/social/production/corporate/transfer parent identities; current receipt, tax-credit and school receipt invariance checks; source hashes. Unresolved measurement and incidence assumptions are described above and in sources.json. This is a calculation memo, not a publication narrative.
