# Saiz–Wachter original-data replay and modern comparisons

**Status:** Original V1 archive acquired and verified. A Python translation of the archived Stata commands recovers all six Table1 coefficients and standard errors at printed precision; columns5–6 also recover first-stage F and Hansen J p-values. Column1 sample size and column4 first-stage F differ from the printed table. This is not native Stata execution or a rebuild of upstream Geolytics/gravity inputs. [Results and limits](../../../research/immigration-hedonic-replay-2026-09-19.md) · [Source record](ACQUIRED.md).

## Original-data replay

After downloading the complete V1 ZIP through ICPSR:

```bash
uv run python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/stage_original.py /path/to/114757-V1.zip
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/original_replay.py
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/verify_original.py
```

Staging rejects partial downloads, wrong archive bytes and differing existing raw files. The archive and extracted files remain in ignored `_cache/`; generated outputs remain in ignored `derived/`:

- `source_manifest.json`: archive/member hashes and byte counts.
- `original_results.csv`: six main-table columns plus dropout-control, land-use and matched-row mean/median comparisons; row/matrix hashes and covariance convention.
- `original_first_stages.csv`: clustered and classical first-stage diagnostics on main-estimation and supplemental-command samples.
- `original_manifest.json`: input/code hashes,43 expanded controls, package versions and printed-target matches.
- `original_verification.json`: independent full-dummy statsmodels WLS/linearmodels2SLS checks for all six columns and matched mean/median; independent full-instrument two-step GMM Hansen J checks for columns5–6.

`table1_targets.json` preserves the published targets and records source discrepancies. The archived commands govern the translation, including the strict `immicapmsa > .05` cutoff and the extra land-use controls in column3. For `areg`/`ivreg`, SEs use the finite-sample correction; columns5–6 use asymptotic clustered SEs because `ivreg2` lacks `small`. Both conventions are retained as labeled output fields. The first-stage F always uses the OLS finite-sample convention.

Hansen J uses efficient two-step GMM with a clustered moment covariance estimated from2SLS residuals, including explicit fixed effects. A manual matrix calculation agrees with `linearmodels.IVGMM`. The older lane's direct2SLS-residual quadratic statistic is now disabled: the estimator returns missing J plus explicit `J_status`, with regression checks. Its historical overidentification claims remain unverified. [ivreg2 authors' derivation,§4.3](https://www.stata.com/meeting/2nasug/wp545.pdf).

## Completed modern bridge

```bash
uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/modern_bridge.py
uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/verify_modern.py
```

Outputs: `modern_bridge.csv` (22 estimates and row/matrix hashes), `modern_bridge_manifest.json`, `ten_year_metro_selection.csv`, and `verification.json`. The original modern lane's inputs and estimates remain unchanged. Independent verification uses explicit fixed-effect dummies for WLS,2SLS and first-stage F.

Modern comparisons use ACS medians,12 controls, modern metro definitions and survey windows. PeriodA uses native2010 boundaries;2013–2023 inherits the older lane's dominant-parent2020→2010 mapping and weighted averages of child medians. This does not isolate era or boundary effects. The fixed5% ten-year sample has only13 metro clusters. No modern overidentification claim is validated by this bridge.

## Other primary sources

- Saiz and Wachter(2011), [article and materials](https://www.aeaweb.org/articles?id=10.1257/pol.3.2.169); main paper cached in the modern lane.
- [Online appendix](https://www.aeaweb.org/articles/materials/1124), `_cache/online_appendix.pdf`; SHA256 `306598d84c13cd48c003f49590d59fb58991300980e61627fe4e8b7cd676c21d`.
