claude-opus-5-5

**Verdict:** On the account's own CPS records the lineage carries **42.6%** of the 2026 public-charge rule's transfer reduction, dollar-weighted. At DHS's 10.3% midpoint that is **$5.0bn a year** less paid to the lineage ($3.2bn federal) of $11.75bn, and $1.6–8.4bn across DHS's 3.3–17.3% rates. On DHS's printed $13.05bn the figure is $5.6bn. This replaces the October 6 memo's 30–45% assumption, which it confirms at its upper end. The rule took effect on 2026-09-18, so it belongs beside a current-law statement about now, never in the 2024 account.

Written 2026-10-07 01:39 JST.

## Shares by programme

DHS's population: recipients in households with at least one noncitizen (citizens included). CPS ASEC 2025, audit row 4 denominator, lineage weights in the numerator (row-4 numerator beside it).

| Programme | Unit | Records | Population (row 4) | Lineage share | Row-4 numerator | DHS federal at 10.3% |
|---|---|---|---|---|---|---|
| Medicaid | person | 5,478 | 12.80M | 43.8% | 43.2% | $5.705bn |
| CHIP | person | 170 | 0.40M | 51.2% | 50.4% | $0.116bn |
| WIC | person | 331 | 0.72M | 42.2% | 41.8% | $0.030bn |
| SNAP | person | 3,016 | 7.20M | 39.0% | 38.3% | $1.018bn |
| TANF | person | 115 | 0.29M | 27.5% | 26.9% | $0.027bn |
| SSI | person | 170 | 0.45M | 29.7% | 28.6% | $0.482bn |
| Rental assistance | household | 791 | 0.69M | 31.2% | 31.0% | $0.330bn |

The lineage is 33.7% of everyone in a noncitizen household, and more of the Medicaid and CHIP recipients there, so its dollar-weighted share (42.6%) exceeds its head-count share.

## Inputs: measured and assumed

Measured or published:
- DHS's federal dollars by programme and rate: RIA Table IV.13, checked against the staged images ER20JY26.020/.021. The script gates that the lines add to DHS's printed totals.
- The state match: DHS's 59% average FMAP on Medicaid and CHIP, the text's $4.05bn.
- Receipt: CPS ASEC 2025 flags (MCAID, PCHIP, WICYN, PAW_YN, SSI_YN; household SNAP value HFDVAL; public housing or a government rent subsidy HPUBLIC/HLORENT).

Assumed:
- DHS's uniform disenrollment rate across groups. A chilling effect concentrated in mixed-status Hispanic families would raise the lineage's part; one that falls mostly on recent green-card applicants from elsewhere would lower it.
- CPS under-reports benefit receipt; only differential under-reporting moves a share.
- The CPS finds 12.8M Medicaid enrollees in noncitizen households, against DHS's 6.09M. DHS builds its count as programme households × the noncitizen population share × foreign-born household size, not from microdata. The share here takes DHS's dollars as given and uses the CPS only to split them.

## What this is not

- A cost saving in the 2024 account: receipt in 2024 was judged under the 2022 rule.
- A net figure. DHS lists more uncompensated care among the indirect effects. The account charges uncompensated care by use, so part of a Medicaid drop would reappear there.

## Reproduce

From the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/public_charge_share_2026_10_07/public_charge_share.py
