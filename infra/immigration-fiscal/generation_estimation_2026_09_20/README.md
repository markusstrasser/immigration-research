# Aggregate later-generation estimation

Analysis specification recorded before the standardized estimates, 2026-09-20.
No fiscal reallocation or individual ancestry assignment.

## Target and assumptions

Target: CPS2025 civilian-household Mexican-identifying adults who are native
with two US-area-born parents, the existing adult G3+ group. Estimate the number
with four US-born grandparents (generic G4+), not exact Mexican G4 or G5+.
Survey identification can differ from observed ancestral country.

Primary donor: GSS2016–2024, WTSSNRPS, original pooled weight mass. Sensitivities:
2021–2024, WTSSPS, and equal mass per full survey year before the domain subset.
Poststratify to four CPS age groups: 18–24, 25–44, 45–64, 65+. Keep the primary
frame and all design cells, with zero influence outside the analysis domain.

The central scenario assumes missing grandparent reports are exchangeable with
observed reports within age, and that the source's within-age shares transfer
to the target period/frame. It uses known-age respondents. Neither assumption
is a measurement. Show separate all-non-G4/all-G4 missing-grandparent endpoints.

Missing-age records cannot simply disappear: retain their counts/mass and also
construct conservative outer endpoints by allowing their G3/G4/unknown mass to
enter each age cell in the direction that minimizes/maximizes that cell's G4
share. These endpoints need not be jointly achievable and are not sharp bounds.
They still assume source-to-target transport within age. They are not bounds on
all coverage, identity or response errors.

Use the existing GSS stratified-PSU linearization and all 160 CPS SDR replicates.
Report source variances separately, zero-covariance approximation, and the
unknown-covariance upper SE (sum of source SEs). Sampling intervals are
conditional on each scenario; model sensitivity is displayed separately.
Retain observed CPS G3/G4 portions and check compatibility without forcing the
survey estimate to agree. Children receive no adult-share imputation: any
all-age envelope adds their observed G4 lower count and unresolved upper count.

Pew and NLSY are external checks with their own period, cohort, identity and
coverage definitions. Do not average their percentages into one pooled result.
PSID exact G4/G5 requires actual ancestor-birthplace completeness, not panel
duration or the existence of family mapping alone.

Additional source-driven sensitivity, specified before its execution: exclude
2021 from the 2016–2024 pool. NORC's 2021 primer documents a mode/frame change;
this is a period-composition check, not an estimated causal effect of mode.

## Reproduction

```sh
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --with scipy==1.18.1 python3 infra/immigration-fiscal/generation_estimation_2026_09_20/estimate.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --with scipy==1.18.1 python3 infra/immigration-fiscal/generation_estimation_2026_09_20/historical_inputs.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --with scipy==1.18.1 python3 infra/immigration-fiscal/generation_estimation_2026_09_20/compare_surveys.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --with scipy==1.18.1 python3 infra/immigration-fiscal/generation_estimation_2026_09_20/verify.py
```

Requires the existing numpy/pandas/pyreadstat environment plus SciPy. The pinned
`--with` dependency avoids silently relying on SciPy being globally installed.
After first resolution, `--offline` is supported. Source inputs are read-only;
new standalone scripts write only ignored `derived/`. No existing public
interfaces or canonical generation/fiscal outputs change.

Inputs: the locked CPS2025 and GSS R3a archives and Pew SAVs documented in
[the preceding lane](../generation_split_2026_09_20/README.md); existing
`new_datasets_2026_09_17/derived/nlsy_family/family_analysis_rows.csv`,
`.../nlsy/full_selected_data.csv`, and the previously acquired design extract
`frontier_execution_2026_09_17/derived/nlsy/selected.csv`. Scripts pin input
SHA-256 hashes; manifests retain hashes and codebook labels. No new microdata
are redistributed or external services required to recompute.

## Estimator and uncertainty

For age cell h with CPS population N_h, GSS weights w, known G4 mass A_h,
known G3 mass B_h and unknown-grandparent mass C_h:

- Central: p_h = A_h / (A_h + B_h), a missing-at-random scenario within age.
- Known-age unknown-GP endpoints: A_h / D_h and (A_h + C_h) / D_h,
  where D_h = A_h + B_h + C_h.
- With unknown-age masses A_0/B_0/C_0, outer endpoints are
  A_h / (D_h + B_0 + C_0) and
  (A_h + C_h + A_0 + C_0) / (D_h + A_0 + C_0).

Adult count = sum_h N_h p_h. Adult share divides by sum_h N_h. Reusing the
unknown-age mass in each cell relaxes joint feasibility, making the endpoints
conservative rather than sharp. It does not resolve source-to-target transport.

Full-frame ratio influence is w_i*(numerator_i - p_h*denominator_i)/sum(w*denominator).
The existing `norms_gen_2026_09_18/norms_lib.py:Design` retains all stratum/PSU
cells and the covariance between ages. GSS VSTRAT is already round-unique;
2021 has multiple PSUs per stratum, so no two-PSU shortcut is imposed.
NORC recommends [these design variables](https://gss.norc.org/content/dam/gss/get-documentation/pdf/other/GSS%20design%20variables.pdf)
and WTSSNRPS in the held R3a codebook, pp.40,56–57.

CPS count/share formulas are recomputed over all 160 released replicates,
using 4/160 squared deviations. All-age endpoints add the child counts inside
the same replicate, preserving adult–child sampling covariance. `se_zero_cov`
is the first-order zero-source-covariance approximation. The interval uses
`se_cov_upper = se_GSS + se_CPS`, bounding their unknown covariance contribution
at that approximation; it is not a bound on systematic error. Approximate
t intervals use occupied-domain PSUs minus occupied-domain strata, capped at
160. See [Stata's subpopulation manual](https://www.stata.com/manuals/svysubpopulationestimation.pdf),
pp.4–6. Intervals across scenarios are not simultaneous or assumption-free.

GSS this-country birthplace and the CPS US-area/citizenship convention are not
perfectly matched. Public missing ages remain missing even though NORC imputes
some ages internally for constructing weights. The central scenario assumes
that this age missingness is ignorable for within-age shares. Period/frame,
identity and reporting differences are additional transport assumptions.

## Outputs and checks

- `standardized_scenarios.csv`: 144 scenario/metric rows across 12 period,
  weighting and pooling specifications. Separate central, GP-unknown and
  age-unknown endpoints; conditional count/share intervals.
- `cps_age_target.csv`, `cps_target_replicates.npz`: current adult margins,
  observed classification anchors and replicate vectors.
- `donor_cells.csv`, `missingness.csv`, `audit.json`: denominator support,
  missing mass, domain dfs, sources, and any observed-CPS-anchor conflicts.
- `historical/`: raw descriptive source tables, age-standardized Pew shares,
  NLSY/GSS birth-cohort comparisons, boundary sensitivities and source audits.

Pew lacks sufficient released design information for a claimed design-correct
subgroup CI; none is generated. Its two unresolved-age identifier cases remain
reported and are excluded from its four-cell standardization. Nonidentifiers
are a separate population. NLSY uses all 8,984 design rows and its official
117-stratum/234-PSU variance benchmark, then reports the retained cohort
domain with current round21 weights; original identity missingness remains.
Some narrow GSS cohort comparisons have zero domain df and explicitly missing
domain intervals. Unbounded approximate intervals are not clipped into false
precision. None of these historical results is pooled into the main estimate.

Validation: numerical ratio derivatives; exhaustive 256-completion missing
age/ancestry envelope check; many-PSU and zero-domain-PSU variance boundaries;
official NLSY variance benchmark; input locks and unique-ID joins. Independent
review reproduced central CPS/GSS estimates and SEs, and checked 512 further
complete-data assignments plus all 24 all-age covariance rows.

Findings: [later-generation estimates](../../../research/immigration-later-generation-estimates-2026-09-20.md).
