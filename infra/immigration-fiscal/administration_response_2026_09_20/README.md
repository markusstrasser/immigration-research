# Administration response: empirical diagnostic

Specification recorded before execution on 2026-09-20.

Question: do existing US state/local current administration costs support a
fixed-versus-population-variable percentage? This is a descriptive diagnostic,
not an identified migration experiment or a federal staffing estimate.

Primary outcome: Census current operations E23 (financial administration) +
E29 (central staff) + E31 (public buildings), combined state/local level 1.
Primary model: log cost on log population, state and year fixed effects,
unweighted, state-clustered CR1 standard errors. Restrict to 50 states; exclude
DC/territories. Use all cached finance years with existing ACS1 population:
2012, 2017–2019, 2021–2023. Do not interpolate missing 2020 ACS1.

Prespecified diagnostics: population weights fixed at first observed year;
2012/2017/2022 census waves; pre-2020 only; exclude 2020–2022; state trends;
2012–2017, 2017–2022 and 2012–2022 long differences; leave-one-state-out;
financial administration and central staff separately and summed without
buildings; state-only and local-only estimates. Report all, not selected signs.
No contemporaneous income/education controls: they may be migration mediators;
omitting them does not remove confounding. Economic shocks, policy, service
quality and wages can jointly drive population and spending. Reverse migration
responses to public services also remain.

Interpretation: for C=F+vN, constant unit cost and a causal response, elasticity
equals vN/C. An observational coefficient alone does not establish that model.
Do not clamp coefficients to [0,1] or apply this selected function's estimate
to the full BEA general-services pool. No model calibration changes automatically.

Inputs are existing cached official state-by-government-level estimates in
`../local_spending_composition_2026_09_18/_cache/indunit_YEAR.zip`, population in
`../tiebout_sorting_2026_09_18/_cache/state_covariates.csv`, and the independent
2022 national API extract in `../macro_closure_2026_09_19/_cache/`.
Source routes and ZIP acquisition scripts remain in those lanes. Raw inputs are
read-only. Generated hashes, coverage diagnostics and outputs go to `derived/`.
The published aggregate estimates include weighting; annual individual-unit
county sums would not provide comparable coverage. 2012 Census state ordinal
codes are mapped to FIPS using the shipped GID file. Blank component cells are
preserved as missing; component sums require complete positive data.

National 2022 E-code amounts must equal the independently cached Census API;
state sums and state/local component conservation are checked separately.
Current costs are nominal fiscal-year dollars; year effects absorb common
national price changes, not region-specific wages. ACS population and fiscal
reporting periods are imperfectly aligned. CR1 intervals use a normal 1.96
critical value and do not include survey sampling/imputation uncertainty.

Run from repository root:

```
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/administration_response_2026_09_20/analyze.py
UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3 infra/immigration-fiscal/administration_response_2026_09_20/verify.py
```

`verify.py` independently reproduces both main coefficients and clustered
standard errors by balanced-panel double demeaning and direct cluster scores;
it does not call the estimator. It also probes rejection of an input-hash change.
