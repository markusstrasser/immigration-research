**Verdict:** IRS industry profits are reproducibly extracted, but their economic capital share and ultimate individual ownership are unidentified. Use the measured table with explicit labor, ownership, replacement and 2024-transport arms. Do not label total pass-through profits capital income.

## Primary measurements and reproducibility

`income_sources.py` downloads only with `--acquire`, then verifies SHA-256 pins in `inputs/income_pins.json`. Ordinary runs read cached sources and regenerate `inputs/income_sectors.json`. Reproduce:

```sh
uv run --no-project --with xlrd python3 infra/immigration-fiscal/passthrough_source_tax_r5_2026_10_15/income_sources.py --acquire
# Thereafter omit --acquire; source changes fail closed, even with --acquire.
```

The extra `xlrd` wheel reads legacy IRS `.xls` files; no repository dependency changes. The JSON has 58 form-sector records. Money is **nominal 2022 $bn**, converted from each workbook's thousands-of-dollars units by division by 1,000,000. No inflation or growth factor is silently applied. [CALCULATION: `income_sources.py`; DATA: `inputs/income_sectors.json`]

| Form | Source | Net ordinary business income | Narrow residual used by `direct_income_net_bn` | Officer pay / guaranteed payments already deducted |
|---|---|---:|---:|---:|
| S corporation | [2022 Table 6.1](https://www.irs.gov/pub/irs-soi/22co61ccr.xlsx), [Table 7](https://www.irs.gov/pub/irs-soi/22co07ccr.xlsx) | 763.268999 | 503.340901 | 349.956774 |
| Partnership | [2022 Table 1](https://www.irs.gov/pub/irs-soi/22pa01.xlsx) | 847.619582 | 629.265801 | 81.949505 |
| Nonfarm sole proprietor | [2022 Table 2](https://www.irs.gov/pub/irs-soi/22sp02is.xls), cross-reference [Table 1](https://www.irs.gov/pub/irs-soi/22sp01br.xls) | 410.664065 | 410.664065 | Not an owner-labor deduction |

These are business-level source totals, **not** a sum of capital income, a 2024 tax estimate, or individual-owner taxable income. The source pins include official catalog and definition pages, [2022 Corporation Income Tax Returns report](https://www.irs.gov/pub/irs-pdf/p16.pdf), and year-specific form instructions. The S workbook is the same official file used by the existing K1 legal-form cross-check. [DATA: `inputs/income_pins.json`]

The table's source-derived values close by form across sectors within $40,000, accommodating rounded sector sums and differences. The script also compares S ordinary income between Tables 6.1 and 7, and partnership ordinary income between Tables 1 and 5; published partner-type components close to their allocation total. Suppressed cells stay null, including S-sector land and finance's asset gains. [CALCULATION: extraction gates]

## Income boundary and tiering

For partnerships, `direct_income_net_bn` subtracts ordinary income from other partnerships/fiduciaries and adds back ordinary losses from those entities. The removed net is $218.353781bn. Portfolio income, separately stated rental income and asset gains allocated on Schedule K are not added. The remaining ordinary line still includes mixed owner labor and direct business asset gains. Guaranteed payments deducted on the ordinary-business page are $81.949505bn; Schedule K guaranteed payments are $102.409433bn. These are different bases, so substituting the latter into the ordinary-profit calculation would mix units. [SOURCE: Tables 1 and 5]

For S corporations, ordinary upstream partnership income/loss enters Other Income (2022 instructions printed p.15), and upstream ordinary asset gains enter Form 4797 (pp.14–15). The industry table does not isolate these amounts. Finance additionally suppresses total deductions, noncapital gains and tax-exempt interest. Therefore an exact upstream-free ordinary-profit measure is unavailable. [SOURCE: [2022 Form 1120-S instructions](https://www.irs.gov/pub/irs-prior/i1120s--2022.pdf)]

The S narrow residual is **ordinary net income minus (total receipts minus business receipts)**. This removes all other receipts and noncapital gains, including valid direct business activity, while upstream losses remain deducted. It also subtracts tax-exempt interest already absent from ordinary income: an intentional $1.923911bn national undersizing. It is a transparent conservative sizing arm, **not a proved lower bound on taxable capital income**. The less restrictive receipt-only residual, ordinary net less all other receipts, remains separately available as `other_receipts_excluded_net_bn` ($542.778583bn). Raw ordinary income is retained for a broad-base sensitivity. [CALCULATION: `get_s`; SOURCE: Tables 6.1/7 and Form 1120-S instructions]

Schedule C excludes farm proprietors reporting on Schedule F; its small NAICS 11 sector is therefore not all agricultural proprietorships. Its profit still pays the proprietor for work. The Schedule C instructions disallow deducting amounts paid to oneself as wages (printed p.C-7). [SOURCE: [2022 Schedule C instructions](https://www.irs.gov/pub/irs-prior/i1040sc--2022.pdf); IRS nonfarm catalog]

## Ownership and owner labor

[Partnership Table 5](https://www.irs.gov/pub/irs-soi/22pa05.xlsx) supplies allocations by immediate partner type and sector. National allocations are $2,551.713803bn: individuals $636.097466bn, corporate partners $552.647127bn, partnership partners $1,018.390562bn, exempt organizations $138.566576bn, and nominees/others $206.012072bn. These allocations cover total Schedule K income less deductions; they are **not ownership shares of direct ordinary profits**. Sector ratios can be negative or exceed one because allocation amounts are net of losses. No automatic clipping, normalization or ownership factor is built into the source interface. [DATA: `national.partnership.partner_allocations_bn`]

Applying the national individual allocation ratio (about 24.93%) to direct ordinary income can be an explicit allocation proxy. It does not identify the share ultimately taxed to individuals: partnership-owned chains may end in taxable persons, corporations or exempt owners; the corporate category does not separate C from S. Charging all partnership income at individual rates would count corporate-owned income again and mishandle exempt/foreign owners. An individual-only immediate-owner arm excludes those chains but still requires proportional allocation across income components. [INFERENCE based on Table 5's differing bases]

Officer compensation and ordinary-page guaranteed payments are **already deducted** from reported profits. Do not subtract them a second time. S officer compensation is a measured personal-services deduction; it is not proof that all economic owner work has been fully compensated. IRS reasonable-compensation guidance distinguishes shareholder services, employees' services, and capital/equipment, and permits reclassification of distributions. [SOURCE: [IRS S compensation guidance](https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues); 2022 Corporation report printed p.16]

`capital_income_arm(record, labor_share, basis=...)` requires an explicit 0–1 residual-profit labor fraction and retains losses signed. A 75% owner-labor / 25% remaining-profit arm can use the separately pinned Smith et al. evidence supplied by the owner-tax worker. That is a transported calibration across years, firms and sectors, especially for Schedule C, and its remaining 25% contains rents as well as normal returns. No central fraction is supplied here. [MODELLING RULE; see the owner-tax evidence file for that paper's population]

## Normal-return stock arm

| Form | Net depreciable book assets | Net amortizable book assets | Book equity / partners' capital | Other investments |
|---|---:|---:|---:|---:|
| S corporation | 888.056327 | 162.485778 | 2,365.868262 | 775.727651 |
| Partnership | 6,968.658998 | 1,805.516192 | 32,204.573785 | 29,859.293129 |

[SOURCE: S Table 6.1; [Partnership Table 3](https://www.irs.gov/pub/irs-soi/22pa03.xlsx)]

These are book/tax-reporting amounts, not replacement-cost capital stocks. Partnership balance sheets omit exempt small filers; no missing assets are imputed. Stocks cover rental and operating activities together while the income arm excludes separately stated rentals. Borrowing finances some depreciable assets, so gross owned assets cannot all earn equity returns. Partnership capital and investments also contain enormous tiered financial holdings. Thus neither `r * book equity` nor `r * net depreciable assets` identifies a normal equity return at current jobs. [SOURCE: Table 3 footnote 1; INFERENCE on stock/income alignment]

The optional helper `normal_return_book_arm` reports `min(max(0, labor-adjusted residual profit), r * max(0, net book depreciable assets))`; it is explicitly **upper sizing before financing adjustment**, excludes land/financial holdings, and returns null for Schedule C. The caller can instead cap stock by positive book equity, or allocate equity financing proportionally to total assets, but each is an extra modelling rule. The caller must choose and cite `r` (the case's 2%/3% real-return assumptions can be arms), transport the stock/income to 2024 explicitly, and account for excluded rentals and financing. A flat 0.37 normal-share parameter is not supported by this source extraction. [MODELLING RULE]

## Mapping and coverage

`naics` and `k1_sectors` map to the existing K1 names; manufacturing pools durable/nondurable, and partnership `61+81` pools education/other services because IRS combines them. Schedule C's source administrative column combines management with administration: the separately published management subcolumn is extracted as 55 and subtracted from 56, preventing duplication. Unclassified 99 has no fabricated K1 mapping. Farm proprietors on Schedule F, source geography, foreign-tax-credit treatment, ultimate-owner tax rates, replacement destinations and case interactions are outside this source worker's coverage. Parent integration owns them. [CALCULATION: mapping assertions; SOURCE: workbook headers/footnotes]

## Verification log

2026-10-15: acquired under 10MB per file after disk check; total income-source cache under 10GB. Extraction completed with exit 0; the measured parsing run took about 1 second and used about 59MB peak RSS. Timing and RSS are measured by `time.perf_counter` and `resource.getrusage`, with platform-specific RSS units, and written only to ignored `_cache/income_runtime.json`. A deterministic rerun and independent edge checks are recorded in the worker result.
