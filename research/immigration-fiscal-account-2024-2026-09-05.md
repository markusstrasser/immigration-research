**Verdict:** The broader 2024 accounting comparison still gives a higher balance for the all-native group than for Mexico-born adults. The native-minus-Mexico difference is **$6,703–$8,969 per adult** for modeled personal payroll and federal/state income taxes less selected transfers, across four allocation/weighting constructions. Adding transported public medical spending preserves the ranking. Adding an average-cost school scenario makes the Mexico-born balance negative in the displayed constructions. None is a complete fiscal balance or an identified effect of admitting an additional immigrant. [CALCULATION: generators and outputs below; FRAMING-SENSITIVE]

# Broader annual fiscal account, reference year 2024

The target is civilian adults aged 25–64 in the 2025 CPS ASEC, grouped by Census nativity and Mexico birthplace. This compares the resident stock, including earlier arrivals; it is not a 2021–2024 entry-cohort or unauthorized-status estimate. Amounts are annual 2024 dollars allocated from current resource units. The instruments, source periods and allocation choices remain visible because they change what the number means. [SOURCE: [CPS2025 data and dictionary](https://www2.census.gov/programs-surveys/cps/datasets/2025/march/)]

## What is counted

The core ledger uses Census-modeled personal payroll tax, federal income tax after refundable credits, state income tax after credits, Social Security, SSI, public assistance, unemployment and veterans' cash benefits; SPM SNAP, energy, WIC, school-lunch and broadband resources enter once per resource unit. The capped housing resource is reported separately because it is not a government expenditure measure. Mixed public/private income categories are omitted instead of labeling them wholly public. [SOURCE: CPS dictionary and [tax-model documentation](https://www.census.gov/topics/income-poverty/income/guidance/tax-model.html)]

The observed identity is `FEDTAX_AC = FEDTAX_BC − ACTC_CRD − EIT_CRED`. Nonrefundable CTC has already reduced the before-refundable liability, so subtracting it again is wrong. The FICA field includes the model's self-employment rules; it is not a flat wage multiplier or an IRS receipt. Tax compliance and exact credit eligibility are modeled, not validated from payment records. Positive liability and refunds are retained separately for sensitivity analysis. [SOURCE: dictionary; [2024 tax-model note](https://www2.census.gov/programs-surveys/demo/guidance/income-poverty/user-note/TY2024-tax-model-external-user-notes.pdf); CALCULATION: all 142,125 records satisfy the identity]

All 58,147 SPM resource units conserve their dollars before selecting groups. Two allocation rules divide each total across all members or all adults aged 18+; mixed-origin families follow the same rule as other families. Head weights conserve estimated unit totals; person weights provide a distinct population-incidence construction. The native aggregate includes native Black, White, Hispanic and other adults. [CALCULATION; see the separate [race-stratified wage analysis](immigration-wage-race-strata-2026-09-05.md)]

## Results and construction sensitivity

One inspectable construction uses **person weights and equal shares among all resource-unit adults**. There are 55,652 sampled native adults and 4,318 Mexico-born adults. These are allocated amounts per selected adult, not individual tax returns. [CALCULATION]

| Annual component | All native | Mexico-born |
|---|---:|---:|
| Modeled taxes in the stated ledger | $15,711 | $5,519 |
| Selected cash transfers | $2,713 | $1,046 |
| Selected noncash resources | $328 | $451 |
| **Taxes less those transfers** | **$12,669** | **$4,023** |
| Transported public health spending, age/birth/insurance | $2,840 | $2,863 |
| **Balance after that health scenario** | **$9,829** | **$1,160** |

The difference in this last row is **$8,670**, with a conditional two-survey 95% sampling interval of **$7,690–$9,649**. Across both allocation rules, both weighting choices and both health transports, the gap stays positive; the range across constructions is more informative than treating one interval as covering every uncertainty. Transport, coverage, tax collection and omitted components are outside these intervals. [CALCULATION: `contrasts.csv`; INFERENCE: uncertainty scope]

[MEPS2024 HC-256](https://meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-256), released August 2026, supplies payments from Medicare, Medicaid, VA, TRICARE, other federal and state/local payers. The model uses age × US/not-US birth, with or without insurance. **It does not directly measure Mexico-specific spending.** Military coverage is matched to MEPS's private-equivalent category using CPS `MIL` and `CHAMPVA`, as its dictionary requires. Institutional care and budget administration are outside the MEPS household expenditure universe. [SOURCE: [MEPS documentation](https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h256/h256doc.pdf)]

### Schools: actual enrollment exposure, assumed spending

The 2024 ACS calculation counts public K–12 attendance in the prior three months among household children aged 5–17, then shares that exposure across all household members or all adults. It counts **0.215535 public pupils per native adult and 0.326609 per Mexico-born adult** under adult allocation. Those are household exposure shares, not every parent's own children or annual student-years. [SOURCE: ACS2024 PUMS `SCH`, `SCHG`, `AGEP`; CALCULATION: two passes over 3,422,888 records]

At the [Census FY2024 national average of $17,619 per pupil](https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html), the combinations below result. **Average expenditure is not marginal expenditure.** CPS SPM units differ from ACS households; combining their group means is an explicit cross-survey construction. [FRAMING-SENSITIVE]

| Person-weighted allocation | Health transport | Native balance | Mexico-born balance | Difference |
|---|---|---:|---:|---:|
| All members | Age/birth | $6,222 | −$799 | $7,021 |
| All members | Age/birth/insurance | $6,421 | −$1,056 | $7,477 |
| All adults | Age/birth | $5,867 | −$3,895 | $9,763 |
| All adults | Age/birth/insurance | $6,139 | −$4,382 | $10,521 |

Current operating school spending includes food services but excludes capital outlays and debt service. These school combinations therefore **remove the SPM lunch resource before subtracting current school spending**; the original no-school account above retains it. The domains do not match exactly, so private-school and out-of-age-domain lunch is omitted in the combined construction. This fixes double counting without pretending the overlap is observed person by person; it does not include every school-system cost. [SOURCE: [Census glossary](https://www.census.gov/programs-surveys/school-finances/about/glossary.html); CALCULATION]

## What this does and does not resolve

The native-minus-Mexico ranking survives the tested constructions; the group's positive/negative sign depends on the included ledger. Employer payroll, sales, property, excise and corporate taxes, other public pensions, institutional care, administration and public goods remain outside the model. Missing taxes and costs can move results in opposite directions. Insurance conditioning also does not identify a causal eligibility effect. No lifetime or marginal-policy sign follows from these annual stock accounts. [INFERENCE]

The independently calculated [SIPP2025 benefits](immigration-sipp-2024-benefits-2026-09-05.md) supply a useful check: allocated SNAP/TANF/SSI averages for calendar2024 are **$456 native and $250 foreign-born** for December adults25–64. They do not cover the CPS ledger's full programs or define the same population. Lower selected benefit receipt is compatible with a lower tax-minus-spending balance when earnings and modeled taxes are lower. [SOURCE: SIPP memo; INFERENCE]

## Reproduction and validation

Raw files remain on the SSD. The [source pin catalog](../infra/immigration-fiscal/acquire/fiscal_2024_sources.tsv) records 16 official input/document files, exact URLs, sizes, SHA256 and reference periods; admission sources have a separate catalog. A failed partial MEPS codebook is excluded. The corrected CPS CSV headers avoid the February2026 warning about ASCII household positions. No raw file or earlier 2023 scenario was overwritten. [PROVENANCE]

```sh
uv run --script infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py \
  --cps-zip /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip \
  --meps-zip /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip \
  --meps-sas /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt \
  --output .scratch/clarity-next-20260905/fiscal/cps-health
uv run --script infra/immigration-fiscal/build/measure_acs_school_exposure_2024.py \
  --acs-zip /Volumes/2TBPNY/corpus/census_acs_2024_1yr/csv_pus.zip \
  --output .scratch/clarity-next-20260905/fiscal/schools
```

Outputs contain replicate vectors and input hashes. CPS uses all160 SDR replicates, including negative weights; ACS uses80. MEPS population anchors reproduce within one person; 10/26 donor-cell covariance matrices retain shared strata/PSUs. The independent review verified raw tax identities, unit conservation, covariance and combined first-order variances and found the two corrected insurance/lunch defects. The smallest insurance donor cell has27 people. Systematic uncertainty is treated separately in the [missingness analysis](immigration-measurement-uncertainty-2026-09-05.md), not hidden inside a sampling interval. [CALCULATION; review: `.scratch/clarity-next-20260905/fiscal/independent_review.md`]

The calculations are descriptive and produced through a fallible LLM workflow; the source comparisons and independent arithmetic checks, rather than an asserted ideological position, support the claims. [FRAMING; [instrument note](../notes/llm-bias-caveat.md)]

## Revisions

- **2026-09-16 — pointer, no change to the September 5 results.** `analyze_cps_fiscal_2025.py` now also emits generation groups (all second generation, all third-plus, Mexican second generation, self-identified Mexican third-plus, third-plus non-Hispanic white); the original five groups and their estimates are unchanged. Results and contrasts: [Mexican-origin by generation](immigration-mexican-origin-by-generation-2026-09-16.md) §5.
