# Zhao licensing and fatal crashes: public-package reproduction

Question: can the public cleaned panels reproduce the headline licensing estimate and its mechanism claims, and does the result change the repo's existing crash charge?

Sources: Zhao, *The impact of granting undocumented immigrants driver's licenses on fatal crashes*, JPAM (2025), [publisher identifier](https://doi.org/10.1002/pam.70053), [SSRN working-paper record](https://ssrn.com/abstract=4744097); author's [OSF project](https://osf.io/x3u7y/) and [files view](https://osf.io/x3u7y/files/osfstorage). Only the replication package is inspected here. Paper text is unavailable. The supplied brief provides the abstract comparison targets; this offline run does not independently retrieve either abstract.

Inputs are already downloaded under ignored `_cache/osf/`. No downloaded code is executed. `.dta` reads use `pyreadstat` only. `reproduce.py` verifies every listed hash before estimation; the complete machine-readable inventory is [derived/input_hashes.csv](derived/input_hashes.csv). The URLs above identify the OSF package, not reconstructed file-specific download IDs.

| OSF package filename | SHA256 from supplied SHA256SUMS |
|---|---|
| additional_estimates_clean.dta | 6a4dc8bf67c0a580345f9d21b9407f30fd608587d3161f56e9152791ed567740 |
| appendix.do | 25ce9b9028e5c89b73499d2c47b6bb568336cd365114f143c5366d5748e68a48 |
| control_variables_clean.dta | 5fc8dcb3816a77ff2f45d3fcd2241324239448341f213bf2bc3bcb9d6c710ab4 |
| county_crash_data_clean.dta | 308f1a9e7754a45a00038a07bef1c52b76093681ec93b5abb8dc0d3a14cd06d4 |
| figures.do | 29497074dd644824988c91aec76748320dd76ccfa5d7186cdc6aa2c0b11fa5d4 |
| full_sample_clean.dta | 9f37bd5f8a7a0e752e2bf3fb4404115e0ab58f620c17a69add4daa52c488bcc8 |
| interstate_and_noninterstate_clean.dta | f10d9675e9408009baf0a6215e77b579e5c9e9e514ac3b3b1705338e3bc1066c |
| licensed_driver_clean.dta | 88d64552763dabb98a2bfcd45a68aec3edc04e02833aad3c2f7c73efd90c2b74 |
| main_results.do | 6946255f8988e67a99f86d4a26826e4633d67548283b9bfe7b34af30525ce4ef |
| master.do | da5ffff8e0b393a6e00c746cb8b0d0947049dda6d1c49b3457e6365a408485a8 |
| README.pdf | 6d0a7cbe63389086e56e70e91559fefac2b97b7774d063176dc5bb8332d9de66 |
| state_crash_data_clean.dta | c194f6f3db227d7998d233488f7e7bf73a33cf5fc984920245ee78f9a20e93ff |
| state_vmt.dta | bb3b1f9483da3d88b4b0ada245e56d1bba6506c43b0f344b61bf17c74bb6ef4a |
| vehicles_involved_clean.dta | 6e785fb8d7ed77a637dd7572965404b8dbcb85f21254df17a1f5bd7325922c5f |

Filename mapping: `data/county_level_crash_clean.dta` in the do-files maps to `county_crash_data_clean.dta`; `data/addtional_estimates_clean.dta` maps to `additional_estimates_clean.dta`. Do not alter the downloads. [derived/do_file_inputs.csv](derived/do_file_inputs.csv) inventories all active quoted `use`/`merge` references in all four do-files, including missing inputs and hardcoded author-machine paths. Generated placebo intermediates are distinguished in RESULT from unavailable source datasets.

Working command, from repository root, using the checkout's existing environment:

```sh
UV_OFFLINE=1 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/zhao_licenses_crashes_2026_10_20/reproduce.py
```

Verification command:

```sh
UV_OFFLINE=1 uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/zhao_licenses_crashes_2026_10_20 "uv run --no-project python3 {lane}/reproduce.py"
```

**[DEGRADED] dependency substitution:** the brief's requested `uv run --no-project --with pandas --with pyreadstat --with pyfixest python3 …` cannot resolve offline. pyfixest is absent from the cache; the cached pandas registry metadata also blocks the unconstrained request. No packages were downloaded. This lane explicitly uses NumPy OLS with alternating county/year demeaning, independently checked against county demeaning plus explicit year indicators. Installed versions are in [derived/software.csv](derived/software.csv). It does not claim a pyfixest run or Stata parity.

Estimation: unweighted county-year OLS, county and year effects; controls `log(pop)`, `unemployment`, `log(fuel)`, `log(regularhighway)`, `log(police)`; cluster scores summed by encoded state. Nonpositive logarithm inputs become missing, as in Stata, and missing rows are dropped per specification. County identifiers remain as supplied. The source's persistent state drops are retained for the mechanism subset, IHS robustness and event studies. Time-of-day estimates use the original main-results sample; the master script instead runs them after the drops.

CR0 is the unscaled state-cluster sandwich. The reported CR1 convention multiplies it by `G/(G-1) * (N-1)/(N-K)`, where K counts slopes and year effects including the constant, excluding county effects nested in state clusters. Confidence intervals use Student t with G−1 degrees of freedom, numerically integrated. Both CR0 and CR1 SEs are exposed. There is no Stata log to verify the finite-sample adjustment against, and no claim of matching published SEs.

The staggered-adoption port fits cohort-by-relative-time interactions for the exact finite event list in `eventstudyinteract`, with never-treated units as the control cohort, then aggregates by observed cohort shares at each event time. It preserves unlisted leads/lags as part of the omitted category; no tail binning is invented. **Its interaction-weighted point estimates are a port, not Stata-verified replication. Its reported covariance conditions on cohort shares and does not implement eventstudyinteract's estimated-share uncertainty.** No `csdid` or `did_imputation` command appears in the supplied do-files.

Outputs:

- [regressions.csv](derived/regressions.csv): headline, hit/non-hit, pedestrian partitions, time of day, risky-driving outcomes, IHS and full-sample robustness, with SEs, intervals and exact samples.
- [event_studies.csv](derived/event_studies.csv), [sa_cohort_weights.csv](derived/sa_cohort_weights.csv): TWFE and interaction-weighted event results; conditional uncertainty limitation above.
- [abstract_comparison.csv](derived/abstract_comparison.csv): abstract targets, percentage transforms and alternative explicitly descriptive level conversions.
- [sample_audit.csv](derived/sample_audit.csv), [sample_states.csv](derived/sample_states.csv): unbalanced-panel coverage, missing controls, zeros, states and adoption dates. State labels come from county prefixes rather than guessed FIPS codes.
- [integration_delta.csv](derived/integration_delta.csv): zero incremental charge applied to the current case by this task, with the matching rationale. This is a modelling decision, not a newly measured zero policy effect.

Limits: no raw FIRST reconstruction, no paper tables, no full Stata execution; other appendix specifications and PPML/negative-binomial/trend-adjusted/placebo/VMT regressions are not ported. Missing `usa_00008.dta` prevents the ACS migration-proxy and travel-behavior analyses; absent mediation input files independently prevent the supplied mediation regressions. The risky-driving categories can overlap and are not a partition. No published risky-driving attribution share is reproduced. See [RESULT.md](RESULT.md) for findings, scope and the proposed correction to the crash lane; it has not been applied elsewhere.

README.pdf was read with `UV_OFFLINE=1 uv run --no-project --with pypdf python3` and `pypdf.PdfReader(...).pages[*].extract_text()`. All source do-files were read as text. Runtime and peak memory are printed with Python `time.perf_counter` and `resource.getrusage`; variable timings are not written into tracked outputs. Failures and guards are recorded in [failure-catalog.md](failure-catalog.md).
