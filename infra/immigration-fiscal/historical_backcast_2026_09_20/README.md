# Historical back-cast of the 2024 fiscal concepts, 2005–2024

No year before income-year 2024 has Mexican-origin taxes, benefits or services
measured in this repository. This lane combines **measured national and population
series by year** with the **2024 relative position** from the
[complete annual account](../full_account_2026_09_20/README.md). It is a model
back-cast, not a historical account.

```sh
# inputs/acs_mexican_origin.csv (needs CENSUS_API_KEY in the environment; ~2 min)
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/pull_acs.py
# derived/backcast_annual.csv and derived/backcast_windows.csv
uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/backcast.py
```

```sh
# programme-by-programme version; run backcast.py first
cd infra/immigration-fiscal/historical_backcast_2026_09_20 && uv run --no-project python3 backcast_categories.py
```

`backcast_categories.py` carries each 2024 benefit, function and household receipt line back with its
own BEA series (the source cells in `full_account_spending_2026_09_20/derived/categories.csv`; Table 3.1
lines 3, 4, 8 and 17 for direct receipts), keeps each response case's 2024 coefficients, and fails unless
every anchor reconstructs the account's 2024 value. It writes `backcast_categories_annual.csv`,
`backcast_categories_windows.csv` (with a variant setting 2020–2021 to the 2019/2022 mean) and
`national_programme_index.csv`.

## Measured by year

| Series | Source | Pin |
|---|---|---|
| Government current receipts and expenditures | BEA Table 3.1, `sources/.../bea_nipa/Section3All_xls.xlsx` | SHA256 `69b5c7ae…615e`, published 2026-08-26 |
| GDP implicit price deflator | BEA Table 1.1.9, `Section1All_xls.xlsx` | SHA256 `238ba851…1a19` |
| Midperiod population | BEA Table 7.1, [Section7All_xls.xlsx](https://apps.bea.gov/national/Release/XLS/Survey/Section7All_xls.xlsx) in `_cache/` (ignored) | SHA256 `ce107c8c…b9ef`, 1,003,641 bytes |
| Mexican-origin count | ACS 1-year `B03001_004E`, 2005–2024 except 2020 (interpolated) | `inputs/acs_mexican_origin.csv` |
| Per-capita income and median age, Mexican group and total | ACS 1-year Selected Population Profile S0201, 2008–2024 except 2010 and 2020 | same file |

`backcast.py` refuses any BEA workbook whose hash differs and checks that the 2024
totals equal the complete account's $8,008.290bn and $10,061.458bn.

## Rules

The ACS self-identified count is scaled by 40.897m / 38.990m to the account's
own/parent-birthplace-plus-identification definition, held constant. Amounts are
2024 dollars by the GDP deflator; sums carry no interest.

- `flat`: the 2024 per-person cost is constant in real terms.
- `ratio`: the group's receipts per person stay 0.566 of national receipts per
  capita, and the spending charged to it under each response case keeps its 2024
  ratio to national current expenditure per capita.
- `income`: as `ratio`, with the receipts ratio multiplied by the group's measured
  relative per-capita income (0.519 in 2008, 0.611 in 2024; unit elasticity;
  2005–2007 held at the 2008 value, gaps interpolated).

The gap against the average resident uses a receipts shortfall less a spending
shortfall, so a deficit shared by everyone cancels. The net-cost concepts do not
cancel it: they rise in 2009–2012 and 2020–2021 with national spending.

## Limits

The spending side is never re-measured. A younger past population had more pupils
and fewer retirees per head; Medicaid expanded after 2014; pandemic business support
is inside national expenditure but was not paid in proportion to population. Total
current expenditure is a coarse scaler for the benefits and services actually charged
in the net-cost cases. Receipts need not move one for one with income. A measured
series requires rebuilding the account on each CPS ASEC file from 2005.
