**Verdict:** Among community-dwelling Medicare beneficiaries aged 65+ in the 2023 MCBS Cost Supplement PUF, public medical payments per beneficiary run **1.265× higher for Hispanic than for non-Hispanic white beneficiaries (SE 0.152, 95% CI 0.966–1.564)**, a difference of **+$3,276 per beneficiary per year (SE $1,806)** that does not clear 95% significance [CALCULATION: `mcbs_elderly.py`; DATA: `derived/ratios.csv`]. Total medical payments from *all* sources are indistinguishable between the two groups (ratio 0.994, SE 0.101) [DATA: `derived/ratios.csv`]: what differs is almost entirely **who pays**. Hispanic 65+ beneficiaries draw 9.2× the Medicaid dollars (SE 3.2) and 35.8% of them have any Medicaid payment against 5.1% of white beneficiaries (SE 0.025 and 0.004), while paying 0.42× as much out of pocket and 0.32× as much through private insurance [DATA: `derived/ratios.csv`]. So a ratio near 1 is **not** what the data show for the public share, but the point estimate is a 27% excess with a confidence interval that still touches parity, and it is driven by income composition rather than by ethnicity: within the low-income category the ratio is 1.538 (95% CI 1.023–2.053) and within the higher-income category it **reverses to 0.704** (95% CI 0.484–0.923) [DATA: `derived/ratios.csv`]. Half the Hispanic 65+ population sits in the under-$25,000 household-income category against 14% of the white [CALCULATION: `mcbs_elderly.py` inputs, weighted shares 0.513 vs 0.136]. Read as a bound on the ledger's 65+ public-medical transport, this says the transport could be understating public medical cost for a Hispanic-heavy 65+ population by up to roughly a quarter to a half, or overstating it if that population is not poor; it does **not** license a flat ethnicity multiplier. **Hispanic here is not Mexican-origin** — `CSP_RACE=3` pools Mexican, Puerto Rican, Cuban, Central and South American and Spanish origin, and the file carries no country of birth [DATA: `2023MCBSSummaryofChangesCSPUF.pdf` footnote 4].

Method and variable map: [README.md](README.md). Gates, hashes and quotes: `derived/audit.json`.

## Anchor: published weighted counts reproduce exactly

No published mean or total **cost** appears in the acquired documents, so the spending
estimates below are unanchored. The weighting and the age × ethnicity classifiers *are*
anchored: all eighteen cells of Exhibit 3.3 reproduce to the dollar, as do the overall and
four race totals of Exhibit 3.2.3 [DATA: `2023MCBSSummaryofChangesCSPUF.pdf` pp.4–5;
CALCULATION: `derived/anchor_reproduction.csv`].

| Age group | Published n / weighted | Computed n / weighted | Hispanic published | Hispanic computed |
|---|---|---|---|---|
| Under 65 | 1,058 / 6,779,654 | 1,058 / 6,779,654 | 121 / 749,890 | 121 / 749,890 |
| 65–74 | 2,463 / 31,805,081 | 2,463 / 31,805,081 | 266 / 2,698,696 | 266 / 2,698,696 |
| 75+ | 3,399 / 22,784,842 | 3,399 / 22,784,842 | 366 / 1,643,244 | 366 / 1,643,244 |
| Total | 6,920 / 61,369,577 | 6,920 / 61,369,577 | 753 / 5,091,829 | 753 / 5,091,829 |

## 65+ weighted mean payments per beneficiary, 2023 dollars

Hispanic n = 632 (weighted 4,341,939); non-Hispanic white n = 4,454 (weighted 42,382,258).
Standard errors are BRR with Fay's adjustment ρ = 0.3 over the 100 supplied replicate weights
[DATA: `derived/elderly_cost_by_race.csv`; CALCULATION: `mcbs_elderly.py`].

| Payer | Hispanic | SE | NH white | SE | NH black | Other |
|---|---|---|---|---|---|---|
| **Public** (Medicare + MA + Medicaid) | **15,638** | 1,694 | **12,362** | 593 | 11,983 | 10,825 |
| Medicare | 8,716 | 1,197 | 7,898 | 419 | 7,819 | 6,597 |
| Medicare MCO/HMO | 4,542 | 533 | 4,204 | 367 | 2,793 | 3,231 |
| Medicaid | 2,379 | 572 | 260 | 48 | 1,371 | 997 |
| Out of pocket | 1,263 | 128 | 3,012 | 80 | 1,554 | 1,869 |
| Private insurance | 463 | 134 | 1,443 | 82 | 1,093 | 765 |
| Other (incl. VA) | 234 | 49 | 598 | 50 | 504 | 589 |
| **Total, all sources** | **17,805** | 1,634 | **17,918** | 691 | 15,930 | 14,340 |

## Hispanic / non-Hispanic white ratios, 65+

The ratio is formed inside every replicate and the same Fay formula applied to the 100
replicate ratios, so the two groups stay correlated through the shared replicate structure
[CALCULATION: `mcbs_elderly.py`, `build_ratios`; DATA: `derived/ratios.csv`].

| Measure | Ratio | SE | 95% CI | Excludes 1 |
|---|---|---|---|---|
| **Public** | **1.265** | 0.152 | 0.966 – 1.564 | no |
| Total, all sources | 0.994 | 0.101 | 0.795 – 1.192 | no |
| Medicare | 1.104 | 0.166 | 0.779 – 1.428 | no |
| Medicare MCO/HMO | 1.081 | 0.161 | 0.765 – 1.396 | no |
| Medicaid | 9.155 | 3.227 | 2.831 – 15.480 | yes |
| Out of pocket | 0.419 | 0.043 | 0.334 – 0.505 | yes |
| Private insurance | 0.321 | 0.094 | 0.136 – 0.506 | yes |
| Other (incl. VA) | 0.391 | 0.089 | 0.216 – 0.565 | yes |
| Share with any Medicaid payment | 7.024 | 0.722 | 5.609 – 8.438 | yes |
| Share with any MCO/HMO payment | 1.469 | 0.067 | 1.339 – 1.600 | yes |

Absolute public-payment gap: **+$3,276 per beneficiary-year (SE $1,806, 95% CI −$265 to
+$6,816)** [DATA: `derived/ratios.csv`].

## By age band and by income category

Age splits the sample without changing the story. Income reverses it
[DATA: `derived/ratios.csv`].

| Domain | Hispanic public | SE | NH white public | SE | Ratio | SE | 95% CI | Hispanic n |
|---|---|---|---|---|---|---|---|---|
| 65–74 | 14,669 | 2,164 | 11,052 | 834 | 1.327 | 0.232 | 0.872 – 1.782 | 266 |
| 75+ | 17,229 | 1,984 | 14,129 | 645 | 1.219 | 0.146 | 0.933 – 1.505 | 366 |
| 65+, household income <$25,000 | 22,458 | 2,899 | 14,604 | 1,356 | **1.538** | 0.263 | **1.023 – 2.053** | 373 |
| 65+, household income ≥$25,000 | 8,450 | 1,272 | 12,008 | 642 | **0.704** | 0.112 | **0.484 – 0.923** | 259 |

Both income-stratum confidence intervals exclude 1, in opposite directions. The pooled 1.265
lies between them because 51.3% of the Hispanic 65+ weighted population falls in the
under-$25,000 category against 13.6% of the white [CALCULATION: `mcbs_elderly.py` inputs].
Total all-source payments show the same reversal (1.311 low income, 0.666 high income), so the
divergence is not purely a payer-mix artefact: higher-income Hispanic 65+ beneficiaries in this
file use less medical care in dollar terms, not merely less public money.

## What this bounds for the ledger

The ledger assigns public medical cost by age and US birth with no ethnicity dimension. This
lane says that at 65+, in a Medicare-specific survey, the ethnicity dimension is worth roughly
**−$3,000 to +$8,000 per beneficiary-year depending on income stratum**, and close to zero
unconditionally once income is held fixed in the direction the pooled figure would suggest.
A transport that already conditions on income or on Medicaid status will absorb most of this;
one that conditions on age alone will misstate the 65+ public medical cell for a Hispanic-heavy
population in whichever direction that population's income distribution points. The 95% CI on
the pooled public ratio, 0.966–1.564, is the honest bound: **an ethnicity adjustment at 65+ of
more than about +56% or any reduction at all is inconsistent with this file**, and a null
adjustment is not excluded.

## Limits

- **Community-dwelling, full year only.** The file "includes only beneficiaries living in the
  community the entire year" and "excludes beneficiaries who had a Facility interview during
  the year or who incurred any facility, hospice, or institutional events or costs during the
  year" [DATA: `MCBSMicrodataPUFDataUsersGuide.pdf` §3.3, p.4]. Long-term institutional care is
  Medicaid's largest 65+ outlay and is **definitionally absent here**, so nothing in this lane
  bounds the institutional public-medical cell.
- **Top-coding.** "All of the service- and payer-specific costs and events variables are
  top-coded at the 99.5 percent level" with top values replaced by the mean of the top 0.5%
  [DATA: same PDF §3.4, p.6]. This compresses the right tail for both groups and shrinks
  differences driven by catastrophic cases.
- **Hispanic is not Mexican-origin.** `CSP_RACE=3` pools all Hispanic origins; the file has no
  country of birth, no nativity, no generation and no immigration status
  [DATA: `CSPUF2023_Codebook.txt`; `mcbs_validation.json` `origin_field_review`]. Mexican-origin
  65+ beneficiaries are a subset with a different income and coverage distribution, and this
  lane cannot isolate them.
- **2023 calendar year**, ever-enrolled population, one cross-section. No trend, no cohort, no
  link to any other file: the PUF ID "changes each year" and cannot be linked to the Survey PUF
  or to claims [DATA: `MCBSMicrodataPUFDataUsersGuide.pdf` Exhibit 3.3.1.b].
- **Medicare Advantage accounting.** `PAMTMADV` is what the MCO/HMO paid for events, not the
  capitation CMS paid the plan. Hispanic 65+ beneficiaries are far likelier to be in MA (62.8%
  vs 42.7% with any MCO/HMO payment) [DATA: `derived/elderly_cost_by_race.csv`], so `PUBLIC`
  here is payments-for-services, not government outlay. If plan-paid claims run below
  capitation, this **understates** the true government cost more for the Hispanic group.
- **Dual-eligibility is a proxy.** There is no enrolment or dual-status variable on the file;
  `PAMTCAID > 0` misses partial-benefit duals whose Medicaid pays premiums or cost-sharing
  without producing a service payment here.
- **Small Hispanic cells.** 632 unweighted observations at 65+, 259 of them in the higher-income
  stratum. Every standard error above is a Fay BRR estimate, not an asymptotic one, and the
  income-stratum ratios rest on a few hundred observations each.
- **Variance formula is the documented method, not a documented equation.** The acquired user
  guide prescribes BRR with Fay 0.3 and gives SAS, Stata and R specifications; it never writes
  the algebra. The equation used is the standard definition of those options and is labelled
  as such in `derived/audit.json` under `variance.formula_status`. Centering on the replicate
  mean instead of the full-sample estimate moves the headline SE from 0.152 to 0.147.
