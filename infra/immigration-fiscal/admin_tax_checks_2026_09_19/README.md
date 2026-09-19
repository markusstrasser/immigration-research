# Administrative earnings and payroll checks, 2026-09-19

Uncalibrated diagnostics of the current CPS ASEC 2025 / income-2024 ledger. The observed Mexican-origin union is 40.896574 million people across all ages and educations. It is disjoint from other civilian residents. These national checks do not provide an administrative Mexican-origin tax total or identify an immigration policy effect. No ledger inputs are changed.

## Findings

Amounts below are billions of current dollars. Differences are model divided by source minus one; they are not estimated measurement errors after adjusting for scope.

| Metric | CPS / proxy | Primary source | Raw difference |
|---|---:|---:|---:|
| Gross wages / SSA W-2 net compensation, 2024 | 11,998.978 | 11,734.670 | +2.252% |
| Wage recipients, millions, 2024 | 165.849 | 175.073 | -5.269% |
| All-covered OASDI taxable earnings proxy, 2024 | 10,869.325 | 10,170.185 | +6.874% |
| Wage portion of taxable earnings proxy | 10,443.977 | 9,666.458 | +8.043% |
| Self-employment portion of taxable earnings proxy | 425.348 | 503.727 | -15.560% |

[SOURCE: SSA AWI underlying data](https://www.ssa.gov/oact/cola/awidevelop.html); [SSA Supplement 2025, Tables 4.B1–4.B2](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/4b.html). **The latter tables label their 2024 figures preliminary estimates based on BLS and BEA data, not completed SSA administrative records.** The AWI raw compensation average is about $67,027; the published $69,846.57 AWI index is not the raw mean. CPS yields $72,348.85 per wage recipient. These averages inherit different populations and compensation concepts.

The all-covered wage proxy deliberately applies the $168,600 cap to every person's gross wages. It cannot distinguish OASDI-exempt employment, while the SSA comparison is covered earnings. The positive gap therefore cannot be read as a measured payroll overstatement of 8.04%. The gap is equivalent to 49.61% of capped wage income of people whose longest job was government; this is only a dimensional sensitivity, not an estimated exemption share or a correction. Government employment need not be exempt; longest-job class does not classify all annual earnings. WECLW=6 was verified in the held 2025 data dictionary. [INFERENCE]

The target's personal allocation implies:

| Metric | Target | Other residents |
|---|---:|---:|
| Wages per wage recipient | $51,347.90 | $75,138.99 |
| Gross wages per resident | $24,420.81 | $37,184.20 |
| Federal income tax after refundable credits per resident | $2,219.18 | $6,170.68 |
| CPS FICA plus modeled employer payroll per resident | $3,748.41 | $5,302.21 |

Target totals are 19.450 million wage recipients, $998.728 billion gross wages, $90.757 billion federal income tax after refundable credits, and $153.297 billion CPS FICA plus modeled employer payroll. Their national shares are respectively 11.728%, 8.323%, 4.736%, and 8.903%, against 12.145% of the population. [CALCULATION: derived/group_components.csv and target_implications.csv]

The national source-tax sum is $3,301.889900 billion: $1,916.237 billion FEDTAX_AC + $900.346 billion FICA + $485.308 billion STATETAX_A. The separate modeled employer component is $821.512 billion. These reproduce the canonical ledger's tax and employer components under both personal and shared allocation. They are not total government receipts, federal tax receipts, or federal income tax alone. Shared wage and earner outputs are resource-unit attributed amounts; use personal allocation for actual group wage recipients.

## Method and boundaries

The builder imports the canonical education-origin setup, which configures the existing fiscal pipeline, then reads the pinned CPS zip and reconstructs the canonical target union and civilian mask. Replicate-weight sampling standard errors use all 160 CPS replicates. Every source dollar and additional payroll proxy is exported for target, rest, and national civilian residents; individual taxes remain the CPS imputed tax variables.

The independent statutory payroll proxy uses wage OASDI base `min(max(wages,0),168600)`. Net self-employment is `0.9235*max(business+farm profit,0)`, zero below $400, and consumes only unused OASDI cap. The employee wage rate is 6.2% OASDI plus 1.45% uncapped Medicare. Self-employment uses both sides, 12.4% plus 2.9%. Employer payroll is computed only on wages, so self-employment employer tax is not added again. [SOURCE: SSA contribution base](https://www.ssa.gov/oact/COLA/cbb.html); [2024 Schedule SE, lines 3–12](https://www.irs.gov/pub/irs-prior/f1040sse--2024.pdf).

This proxy is not observed payroll collection and does not replace FICA. It omits additional Medicare tax, detailed partnership treatment, optional Schedule SE methods, church and other exceptions, multi-employer wage overpayments, and explicit coverage flags. CPS FICA exceeds its employee/self-employment counterpart by $10.873 billion nationally; the dictionary's FICA label does not itself prove that the components are identical.

The survey covers civilian residents in its household sampling universe at survey time. Annual administrative earnings can include people outside it, such as territorial or institutional residents, Armed Forces, and people who died or left before the survey; annual gross wages and W-2 compensation also differ. Survey reporting, imputation, and disclosure treatment can affect comparisons. Do not infer the cause of the recipient discrepancy from its sign. [SOURCE: held CPS ASEC 2025 dictionary; SSA compensation definition](https://www.ssa.gov/oact/cola/netcomp.html).

**Correction, September20:** The $9,738.951bn wages and $2,098.923bn income-tax anchors originally read as2023 from Publication4801 p9 reproduce **Tax Year2022** [Table1.4](https://www.irs.gov/pub/irs-soi/22in14ar.xls) and [Table1.2](https://www.irs.gov/pub/irs-soi/22in12ms.xls) exactly. The PDF's heading is misleading. This lane retains the original amounts and raw CPS2024 differences (+23.206%/−5.613%) as explicitly superseded, mismatched-year diagnostics; source IDs/year are corrected. The [matched2023 successor](../same_year_tax_2026_09_20/README.md) uses the detailed2023 tables and actual CPS tax units. IRS liability is not FICA, withholding or collections; these sources have no administrative Mexican-origin tax total. FEDTAX_BC, before refundable credits, is the closer CPS concept.

## Disconfirmation and uncertainty

The wage-dollar result does not support a large national aggregate shortfall, but the recipient and taxable-base discrepancies defeat a claim that every underlying quantity already matches administration. Matching the national sum cannot validate the ethnicity allocation or prove the target's fiscal balance. Opposite wage/SE discrepancies defeat a uniform payroll calibration without resolving coverage and tax concepts. Sampling SEs do not quantify those modeling and measurement uncertainties. No confidence interval for ethnic fiscal attribution is inferred. [INFERENCE]

## Reproduce and validate

Run from the canonical source root so its environment is available; substitute the two absolute paths as needed:

```sh
PYTHONPYCACHEPREFIX=/private/tmp/admin-tax-pycache UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy --with openpyxl python3 infra/immigration-fiscal/admin_tax_checks_2026_09_19/builder.py --source-root /Users/alien/Projects/immigration-research
PYTHONPYCACHEPREFIX=/private/tmp/admin-tax-pycache UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy --with openpyxl python3 -m unittest discover -s infra/immigration-fiscal/admin_tax_checks_2026_09_19 -p 'test_*.py' -v
```

Four tests cover zero/negative earnings, combined wage/self-employment cap, business/farm loss offsets, and the self-employment two-sided tax without an additional employer charge. Full build checks exact canonical populations/tax/employer anchors, target/rest conservation, refundable-credit identity, 250 scalar payroll cases, an independent pandas weighted-wage aggregation, and the employer formula. The independent aggregate oracle permits floating-point summation tolerance (1e-13 relative, one cent absolute); a first overstrict tolerance failed on a six-cent difference in $11 trillion.

`sources.json` pins manually extracted primary amounts, units, publication status, dates and locators; the build performs no live fetching. `audit.json` fingerprints canonical sources, upstream implementations, this implementation, and outputs. Derived files and bytecode are ignored. Raw source files are read only; no raw data is duplicated. The result is a national consistency check, not new calibration or an essay.
