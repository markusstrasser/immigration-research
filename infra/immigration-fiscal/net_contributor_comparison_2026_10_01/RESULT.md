**Verdict:** [MODEL OUTPUT; FRAMING-SENSITIVE] On the September 29 annual accrual case, **33.1–35.7%** of the white reference population and **13.7–16.9%** of Mexican-origin residents live in net-contributor households. These are resident-weighted shares at actual ages, including children and retirees. White household amounts are a new distribution of the existing rough comparator; the Mexican distribution is the existing person-accrual/on-books-payroll central. The comparison does not identify lifetime-positive shares or individual fiscal outcomes. [CALCULATION: `compare.py` → `derived/shares.csv`]

# Annual fiscal distribution: white and Mexican-origin residents

Income year 2024. Positive means receipts and production gains attributable to the household exceed its allocated responsive spending, pension accrual and capital return, under the adopted account's conventions. A member of a mixed household carries only the group's allocated portion. White means US-born, non-Hispanic, white alone, with both parents born in the US or the account's US-area categories. Mexican origin is the account's first-, second- and third-plus-generation union. Neither is a birth cohort. [DATA: `white_replacement_2026_09_28/rekey_white.py` masks; `within_group_distribution_2026_09_29/households.py`]

| Group | Lower-cost setting: residents in positive households | Higher-cost setting | Median annual household balance per group member, lower / higher |
|---|---:|---:|---:|
| White reference | 35.74% | 33.07% | −$5,186 / −$6,226 |
| Mexican origin | 16.87% | 13.71% | −$10,345 / −$11,714 |

[CALCULATION: `derived/shares.csv`; specification 48 / 11, respectively. These are paired model settings, not confidence bounds. No new sampling confidence interval was computed.]

The **household-weighted** positive shares are different: whites 38.45% / 36.28%, Mexican origin 24.61% / 20.31%. The figures answer the resident question: larger households count more because more people live in them. Each resident is placed at their group's household balance divided by its number of members, using their person survey weight. [CALCULATION: `derived/shares.csv`; behavioral tests in `test_comparison.py`]

## Construction

`compare.py` imports the current white comparator read-only. Its `setup()` verifies the adopted case, the predecessor release, population correction and pension rule. The white scenario is `A1_third_plus_nh_white`, actual ages. Its uniform scaling to the Mexican account's 39.71 million members cancels from individual dollar amounts and positive shares; the charts use the white residents' own survey weights, representing 173.05 million residents in 33,503 sampled households. Mexican origin represents 39.71 million residents in 7,106 sampled households. [DATA: `derived/shares.csv`]

Every evaluated white receipt/spending line and capital component is allocated to CPS persons by its own normalized key, then pooled within households. The lower-cost setting shares direct person keys within SPM units; the higher-cost setting keeps personal attribution. Income taxes retain the comparator's tax-unit sharing. Composite keys preserve the amounts of their components: schools/college, refundable credits/per-head component, Medicaid/long-term care, justice/per-head use, roads/passenger-freight and the removed old road key. The script fails on a nonzero line without a key, missing medical age cells or any failure to conserve line totals. [CALCULATION: `compare.py`, `derived/white_allocation.csv`]

Social Security uses the existing cached person model's **gross** accrual and benefit-tax timing, with the white comparator's own future benefit-tax rate. The cached nonmember net rate is not reused. Its weighted gross ratio and timing must reproduce the saved own-white pension table. Part A is spread by covered-worker age/sex present values and normalized to the white comparator's own aggregate accrual. For this all-native white domain, qualification and expected covered years are group-common scalars that cancel; explicit guards check the required domain. Medicare's remaining current benefits stay on medical age cells. Removed tax on current Social Security benefits follows benefit recipients, separately from income tax. [DATA: `white_replacement_2026_09_28/accrual_white.py`; `within_group_distribution_2026_09_29/person_accrual.py`; `derived/audit.json`]

The allocated white totals reproduce the existing comparator's **$24.2382bn / $74.0620bn** costs for the 39.71M slice, to its published precision; exact internal reconciliation is tighter than $10. Mexican household balances reproduce the established positive shares to the release's six-decimal precision. The Mexican household allocation leaves about $5.2bn of beneficial lane constants unassigned, as the existing release does; no white or Mexican total is silently shifted to force a particular positive share. [CALCULATION: `compare.py`; DATA: `white_replacement_2026_09_28/derived/rekey_summary_sept29.csv`, `within_group_distribution_2026_09_29/derived/sept29/control_person_onbooks.csv`]

## Limits and disconfirmation

- **White remains a rough comparator.** It lacks exact counterparts to the Mexican IRS/compliance and school/college corrections. CPS income tax keeps the survey's missing top tail unassigned. Thus the difference between the plotted shares is not established as solely a difference in group composition. [DATA: `white_replacement_2026_09_28/rekey_sept29.py`, rules 1–5]
- **Household dispersion is modeled.** White medical spending uses native-white MEPS means by five-year age band; MEPS cannot identify parental birthplace. Long-term care is spread to ages 65+. Justice uses per-head and age-risk components, not observed household offending. Mexican medical and justice allocations have different cell definitions. These rules can move households across zero despite unchanged aggregate totals. [INFERENCE; implementation in `white_keys()`]
- **One year's earnings are used in pension accrual.** The model's progressivity, current family type and eligibility assumptions do not establish a person's actual future benefits. [DATA: existing person-accrual lane, limitations]
- **Actual age and family composition matter.** Negative balances for families with children and retirees do not establish negative lifetime balances. Household allocation also does not classify each person's own contribution. No new lifetime estimate is made. [INFERENCE]
- **Checks against misleading displays.** The histogram uses common $2,000 bins and common axes. Its area is a fraction of all residents, not only the displayed subset. Both omitted tails are labeled and the probabilities must sum to one. The threshold curves use every household, preserve strict `>0`, and must reproduce the positive shares exactly. Both model settings are visible. [CALCULATION: `plot.py`]

The numerical household-share gap would change if linked tax/benefit records or a harmonized medical/justice allocation materially changed balances around zero. The current charts establish what these two maintained accounting implementations imply, conditional on their allocation rules. [INFERENCE]

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/net_contributor_comparison_2026_10_01/compare.py
uv run --no-project --with matplotlib python3 infra/immigration-fiscal/net_contributor_comparison_2026_10_01/plot.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/net_contributor_comparison_2026_10_01 -q
```

Inputs are the existing local CPS/MEPS sources and current white/Mexican releases. `derived/` contains shares, allocation reconciliation, plot data and source hashes; `_cache/households.parquet` retains the rederivable household table; ignored `plots/` contains PNG, SVG and PDF versions. Plot titles and all percentages consume the same computed share table.

## Validation

- Six behavioral tests pass: household classification before resident weighting, unequal member weights, strict zero threshold, mixed-group households, conservation under population scaling, and rejection of invalid/empty keys. The live build separately gates each fiscal component and the released aggregate totals.
- `scripts/rerun_lane.py` ran calculation, plotting and tests with exit zero and `IDENTICAL: 10/10` files. Source hashes include the raw CPS/MEPS inputs, medical/justice calibration, pension cache and existing account releases.
- Visual inspection corrected title/subtitle spacing. A blind reader, twice, recovered the resident weighting, annual horizon, two share ranges and larger white upper tail: 10/10 graded chart answers. The two readers quoted the rounded headline ranges; the initial 0.2-point grading tolerance was corrected to 0.5 to accommodate the title's whole-percent precision, then saved answers were regraded without rerunning the reader. Prose alone answered 8/10 and could not identify the unreported tail. Evidence is in `_cache/blind-read/`.
- The Cursor plot-code review identified no material current-result error. Its median-sign issue was repaired for positive future medians; casing and output-directory comments were not defects. The calculation scout returned nonconforming, style-only findings and failed its output-contract guard; it is not counted as a successful independent correctness review.
- Native read-only triage subsequently traced signs, population scaling, resident weighting, mixed-household pooling, pension reuse, composite allocations and capital against their upstream interfaces and found no material defect. The rough-comparator limitations above remain.
