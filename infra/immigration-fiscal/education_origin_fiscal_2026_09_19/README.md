# Education and origin fiscal accounts

Descriptive annual balances for civilian household residents, using the repaired
September 19 account and current education. The main comparison is ages 25–64.
Age schedules also cover 65–74 and 75+ for explicitly modeled remaining-lifetime
consumers. These are resident accounts, not causal admission effects.

Run from the repository root:

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with numpy --with pandas --with openpyxl python3 infra/immigration-fiscal/education_origin_fiscal_2026_09_19/builder.py
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project --with numpy --with pandas python3 -m unittest discover -s infra/immigration-fiscal/education_origin_fiscal_2026_09_19 -p 'test_*.py'
```

In a managed worktree without raw data, supply `--source-root /absolute/path/to/canonical/repo`.
`--health-helper` accepts an explicit path to the sibling healthcare builder;
the default is `health_transport_sensitivity_2026_09_19/builder.py` under the source root.
Inputs are read-only. Outputs default to this lane's ignored `derived/` directory.

## Definitions and coverage

The [2025 full CPS technical documentation](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf)
defines A_HGA 31–38 as below high school, 39 as high school diploma or equivalent,
40–42 as some college/associate degree, and 43–46 as bachelor's or above. Children
are never classified by their unfinished education. Adult missing/reserved codes
fail the build. The four attainment categories partition `all` in every replicate.

Origins are foreign-born (`PRCITSHP` 4/5) and the exact Appendix J birthplace codes
in `ORIGIN_CODES`. Caribbean includes English-speaking countries; South America
includes Guyana and unspecified South America. Southeast Asia is heterogeneous
and excludes Brunei/Timor-Leste because no separate public birthplace codes exist.
The all-native reference uses citizenship groups 1/2/3, including native persons
born in territories or abroad to US parents. The white reference additionally
requires two US/territory-born parents, non-Hispanic ethnicity, and white race.

`recent_2016_2025` uses PEINUSYR 25–28. It means surviving current residents who
report arrival in 2016 through the March 2025 interview, not gross admission counts.
The full technical documentation gives entry code 28 as 2022–2025; the separately
published `asec2025_ddl_pub_full.pdf` retains a stale 2022–2024 label. Current
attainment is not education at arrival. No recent-entry lifetime forecast is licensed.

Accounts:

- `partial`: the original eight signed base components plus raw public medical.
- `expanded_excluding_N`: every repaired central fiscal item except the external
  ACS institutional item N. Central F is zero; its average-cost increment is separate.
- `expanded_excluding_N_D`: the same account with district differential D set to zero.

D is generalized to the actual observed Hispanic and non-Hispanic white pupils
whose ethnicity matches the source cost coefficients. This is a state/ethnicity
proxy, not an observed origin-specific school cost. Before that change, the old
Mexican-only D rule reproduces all six Mexico-born adult age totals under both
allocations. N must come from a matching external ACS domain sensitivity; zero N
does not mean institutional costs are known to be zero.

The personal allocation uses direct taxes/cash/payroll and assigns schooling to
pupils; unit-level benefits and indirect receipts retain their source allocations.
Shared allocates those person-source items over household resource-unit members.
Neither convention attaches all descendants' costs to a parent's immigration cohort.

## Uncertainty and support

Each cell preserves full weight plus all 160 CPS SDR replicates. Medical means for
raw public spending, calibrated public spending, and TRICARE are fitted jointly
with the full MEPS stratum/PSU design retained. Their cross-outcome/cross-cell
covariance is carried into balances and differences; it is not added as if every
subgroup used independent donors. Expanded medical uses the calibrated outcome,
so the Medicaid/Medicare M increment is included exactly once with its uncertainty.

Intervals condition on fixed fiscal parameters, fitted CPS allocation/calibration
coefficients, donor transport, and the fixed point-estimate age standard. They do
not cover mismeasurement, nonresponse/undercount, transport error, policy change,
or all calibration uncertainty. F's netting of CPS-transported TRICARE is recomputed
in each CPS replicate and has its correlated MEPS gradient preserved.

Common-age comparisons use all-native/all-education 25–64 age shares. A band is
supported when raw n ≥30, Kish weight ESS ≥20, and every replicate has positive
population. These are declared analytical reporting thresholds, not an agency
standard. Missing/sparse bands are visible; support-restricted comparisons report
the surviving standard mass and renormalize explicitly. Unstandardized annual
totals retain every eligible person and report sparse age-band counts.

## Export contract

`profiles.csv` row order is the `profile_id` index in `uncertainty.npz`.
Profile keys are allocation/account/origin/education/entry. Age dimension is
25–34, 35–44, 45–54, 55–64, 65–74, 75+. Arrays:

| Array | Dimensions | Meaning |
|---|---|---|
| `age_net_replicates` | P ×6 ×161 | Signed net total dollars, full weight then replicates |
| `age_population_replicates` | P ×6 ×161 | Matching populations |
| `age_medical_gradients` | P ×6 ×30 | Derivative of total net dollars against joint donor means |
| `medical_covariance` | 30 ×30 | Joint donor covariance |
| `donor_means` | 10 ×3 | Cell-major raw public/calibrated public/TRICARE |
| `age_F_replicates` | P ×6 ×161 | Signed incremental average public-goods balance |
| `age_F_medical_gradients` | P ×6 ×30 | F total-dollar medical derivative |
| `age_supported`, `raw_n`, `weight_ess` | P ×6 | Support metadata |

Divide total-dollar gradients by full-weight population for per-person gradients.
Retain off-diagonal age and donor covariance when integrating lifetime profiles.
`annual_estimates.csv`, `comparisons.csv`, `age_profiles.csv`, `age_components.csv`,
`support.csv`, and `medical_donor_cells.csv` are readable tables. The manifest binds
inputs, source implementation, and every exported file by SHA-256.

Validation includes canonical Mexico adult reproduction, source codebook/header
verification, upstream resource-unit conservation, education conservation in every
replicate, medical increment reconstruction, and F point reconstruction. Synthetic
tests cover domains, missing-code failure, sparse support, replicate conservation,
correlated medical variance, and shared-reference cancellation.
