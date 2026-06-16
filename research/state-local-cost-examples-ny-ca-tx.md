# State and Local Cost Examples — New York, California, Texas

**Question:** What do local costs look like for concrete states if we use the CBO state/local framework and push it as far as the available evidence allows?  
**Date:** 2026-03-13  
**Scope:** Direct 2023 state/local budget effects for the `2021+` immigration surge, using CBO's framework plus a transparent state-allocation method for categories where CBO does not publish full state tables.

## Bottom Line

Using CBO's `2023` surge-population state shares and CBO's direct state/local spending totals, the most defensible illustrative direct local net-cost examples are:

| State | Gross direct local spending | Illustrative local revenue | Illustrative net local cost | Net local cost per surge resident |
|---|---:|---:|---:|---:|
| `NY` | `$3.531B` | `$0.949B` | `$2.582B` | `$8,579` |
| `CA` | `$1.478B` | `$1.130B` | `$0.348B` | `$735` |
| `TX` | `$4.495B` | `$1.159B` | `$3.336B` | `$5,173` |

[SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

Those are **illustrative direct-budget ledgers**, not official CBO state tables. They are built from a mix of:

1. **hard state-specific CBO numbers** for shelter and border security, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. **CBO national direct category totals** allocated by each state's share of the surge population, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. **illustrative state/local revenue allocation** using CBO's national direct revenue per surge resident, scaled by each state's ITEP tax-per-undocumented-resident factor. [SOURCE: `sources/immigration-fiscal/data/itep/itep_table_2.tsv`] [SOURCE: `sources/immigration-fiscal/data/itep/itep_table_6.tsv`]

## What Is Directly Measured vs Allocated

### Hard measured state-specific categories

From CBO's June `2025` state/local report:

- `NY`: `$2.6B` shelter and related services in `2023`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- `TX`: `$2.5B` border-security spending in `2023`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- `CA`: `$15M` border-security spending in `2023`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

These alone imply a hard **explicit response floor** of:

| State | Explicit response floor | Per surge resident |
|---|---:|---:|
| `NY` | `$2.600B` | `$8,638` |
| `CA` | `$0.015B` | `$31.71` |
| `TX` | `$2.500B` | `$3,876` |

[SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

### National direct categories allocated by state share

CBO's `2023` direct state/local totals for the surge were:

- revenues: `$10.1B`, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- spending: `$19.3B`, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- direct net cost: `$9.2B`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

Key direct spending categories:

- public primary and secondary education: `$5.7B`, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- health insurance and income security programs: about `$1.0B`, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- shelter and related services: `$3.3B`, [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- border security: `$2.7B`. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

The remaining direct spending, about `$6.6B`, is the residual "other direct local spending" bucket:

```text
$19.3B - $5.7B - $1.0B - $3.3B - $2.7B = $6.6B
```

That residual covers general services and other categories CBO counts directly but does not fully state-tabulate in the report. [INFERENCE from CBO totals]

For the examples below, I allocated:

- education,
- health/income-security,
- residual other direct spending,

by each state's CBO share of the `2023` surge population:

- `NY 7%`
- `CA 11%`
- `TX 15%`

[SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

## Revenue Allocation Method

CBO does **not** publish full state tables for the `$10.1B` in direct state/local revenues. So I used an illustrative method:

1. national direct local revenue per surge resident:

```text
$10.1B / 4.3M = about $2,349 per surge resident
```

2. state adjustment factor from ITEP:

```text
state ITEP taxes per undocumented resident / national ITEP taxes per undocumented resident
```

Which yields:

- `NY`: `1.342x` national
- `CA`: `1.018x`
- `TX`: `0.765x`

[SOURCE: `sources/immigration-fiscal/data/itep/itep_table_2.tsv`] [SOURCE: `sources/immigration-fiscal/data/itep/itep_table_6.tsv`] [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

This is not a claim that the surge population has the same tax profile as the established undocumented population. It is a tax-structure proxy that is better than assuming equal revenue yield across New York, California, and Texas. [INFERENCE]

## Example Ledgers

### New York

Estimated `2023` surge residents:

```text
4.3M * 7% = about 301,000
```

Ledger:

- shelter and related services: `$2.600B` [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- allocated education: `$0.399B` [INFERENCE from CBO category total × NY share]
- allocated health/income-security: `$0.070B` [INFERENCE]
- allocated other direct spending: `$0.462B` [INFERENCE]
- gross direct local spending: `$3.531B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative local revenue: `$0.949B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative net local cost: `$2.582B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

Per surge resident:

- explicit response floor: `$8,638`
- illustrative net local cost: `$8,579`

Interpretation: in `NY`, the named shelter burden is so large that it almost entirely determines the state example. [INFERENCE]

### California

Estimated `2023` surge residents:

```text
4.3M * 11% = about 473,000
```

Ledger:

- border security: `$0.015B` [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- allocated education: `$0.627B` [INFERENCE]
- allocated health/income-security: `$0.110B` [INFERENCE]
- allocated other direct spending: `$0.726B` [INFERENCE]
- gross direct local spending: `$1.478B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative local revenue: `$1.130B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative net local cost: `$0.348B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

Per surge resident:

- explicit response floor: `$31.71`
- illustrative net local cost: `$735`

Interpretation: California looks far less locally costly in the measured direct-response categories than New York or Texas. The gap is driven by the absence, in the current CBO evidence set, of a New York-style shelter line item or a Texas-style border-security line item. [INFERENCE]

### Texas

Estimated `2023` surge residents:

```text
4.3M * 15% = about 645,000
```

Ledger:

- border security: `$2.500B` [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
- allocated education: `$0.855B` [INFERENCE]
- allocated health/income-security: `$0.150B` [INFERENCE]
- allocated other direct spending: `$0.990B` [INFERENCE]
- gross direct local spending: `$4.495B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative local revenue: `$1.159B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- illustrative net local cost: `$3.336B` [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

Per surge resident:

- explicit response floor: `$3,876`
- illustrative net local cost: `$5,173`

Interpretation: Texas's example is dominated by discretionary border-security spending, especially Operation Lone Star. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [INFERENCE]

## What This Does and Does Not Mean

### What it means

1. Local cost is **not** well represented by one national average.
2. `NY` and `TX` can look expensive for very different reasons:
   shelter law and emergency housing in `NY`,
   border-security policy in `TX`.
3. `CA` can have a large surge population share and still show a much smaller direct local burden in the measured CBO categories.

### What it does not mean

1. These are **not official CBO state net-cost estimates**.
2. They do **not** capture all local nonbudgetary pressures, such as crowding, wait times, and housing quality degradation.
3. They do **not** identify pure illegal-only effects; the underlying CBO surge population is mixed-status, though heavily composed of people without durable legal status.
4. They do **not** mean California has no local burden. They mean the current report does not show New York/Texas-style explicit line items for California.

## Best Current Judgment

If you want a thorough but honest state/local answer from the current evidence set, it is:

- `NY` looks locally very expensive, around **`$2.6B` to `$3.5B`** in direct `2023` local burden depending on whether you count only named response spending or the fuller illustrative direct ledger. [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- `TX` also looks locally very expensive, around **`$2.5B` to `$4.5B`** gross direct burden, with illustrative net local cost around **`$3.3B`**. [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]
- `CA` looks materially lower in the current direct-budget evidence, around **`$1.5B` gross** and **`$0.35B` net** in the illustrative ledger. [SOURCE: `sources/immigration-fiscal/data/derived/state_local_example_ledgers.csv`]

That is the main factual result: **local costs are real, but they are not evenly distributed and they are strongly shaped by state policy and institutional response.** [INFERENCE]
