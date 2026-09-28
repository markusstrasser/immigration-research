# IRS SOI, Historic Table 2, tax year 2023: quoted definitions and totals

Files (hashes in `derived/sources.json`):

- `_cache/23in55cmcsv.csv`, from `https://www.irs.gov/pub/irs-soi/23in55cmcsv.csv`, fetched 2026-09-28;
- `_cache/soi_23incmdocguide.doc`, from `https://www.irs.gov/pub/irs-soi/23incmdocguide.doc`, fetched in phase 1 for
  definitions. `_cache/soi_23incmdocguide.txt` is its text (macOS `textutil`); line numbers below refer to it.

## Definitions (documentation guide)

> State Data
> Tax Year 2023 Documentation Guide

(lines 1–2)

> State totals may not be comparable to state totals published elsewhere by SOI.[2]
>
> State data are based on population data that was filed and processed by the IRS during the 2024 calendar year.
>
> Data do not represent the full U.S. population because many individuals are not required to file an individual
> income tax return.
>
> The address shown on the tax return may differ from the taxpayer’s actual residence.

(§C, "Population Definitions and Tax Return Addresses", lines 52–60)

> For all the files, the money amounts are reported in thousands of dollars.

(line 79)

> AGI_STUB — Size of adjusted gross income — 0 = No AGI Stub

(lines 91–93; the rows with AGI_STUB 0 are the state totals)

> A59660 — Earned income credit amount [12]
>
> A59720 — Excess earned income credit (refundable) amount [13]
>
> A11070 — Additional child tax credit amount

(lines 655, 695, 703; all three are from Form 1040 lines 27–28)

> [12] Earned income credit includes both the refundable and non-refundable portions. The non-refundable portion
> could reduce income tax and certain related taxes to zero. The earned income credit amounts in excess of total tax
> liability, or amounts when there was no tax liability at all, were refundable. See footnote below for explanation
> of the refundable portion of the earned income credit.
>
> [13] The refundable portion of the earned income credit equals total income tax minus the earned income credit. If
> the result is negative, this amount is considered the refundable portion. No other refundable credits were taken
> into account for this calculation.

(lines 811–812)

> The Refundable child tax credit or additional child tax credit was renamed Additional child tax credit (N11070 and
> A11070),

(line 24)

> [2] The income and tax items included within Historic Table 2 (state data) reflect the most complete and accurate
> totals by state. Due to various disclosure protection procedures, State totals included in SOI’s ZIP Code and
> county data may not be comparable to those from Table 2.

(line 791)

## Totals quoted from the CSV (AGI_STUB 0, $ thousands)

The file holds 54 rows at AGI_STUB 0: `US`, the 50 states and DC, `OA` (other areas) and `PR`.

| STATE | N59660 | A59660 | A59720 | N11070 | A11070 |
|---|---|---|---|---|---|
| US | 23,923,110 | 65,006,308 | 54,853,654 | 17,207,180 | 33,740,750 |
| CA | | 6,386,832 | 5,210,978 | | 3,546,573 |
| TX | | 8,087,978 | 6,737,330 | | 4,187,936 |
| OA | | 21,345 | 20,622 | | 178,708 |
| PR | | 5,517 | 4,552 | | 27,049 |

The 51-area sums are A59660 64,979,446 and A11070 33,534,993 [DATA: derived/target_national.csv]; US equals the
51 areas plus OA and PR.
