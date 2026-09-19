# Saiz–Wachter specification check and modern-data bridge

Original-data replay status: **pending original archive download**. The published main paper and online appendix have been read. ICPSR sign-in succeeded; accepting the displayed download terms still requires the operator's confirmation. No original `.dta` or `.do` has been acquired, and no old-data reproduction is claimed.

Completed work: source specification extraction, frozen-input modern comparisons, independent full-dummy WLS/2SLS/first-stage checks. [Evidence and results](../../../research/immigration-hedonic-replay-2026-09-19.md).

## Reproduce completed comparisons

From the repository root, using existing inputs from the modern lane:

```sh
uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/modern_bridge.py
uv run --with scipy --with statsmodels --with linearmodels python3 infra/immigration-fiscal/hedonic_replay_2026_09_19/src/verify_modern.py
```

Outputs in ignored `derived/`: `modern_bridge.csv` (22 estimates, row/matrix hashes), `modern_bridge_manifest.json` (input/code hashes and package versions), `ten_year_metro_selection.csv`, and `verification.json`. The original lane's inputs and estimates are read-only. The independent verification uses statsmodels WLS and linearmodels IV2SLS with explicit metro-period dummy variables, rather than the lane's within transformation.

`table1_targets.json` records the original published coefficient, SE, N and diagnostic targets. It is a contract for the pending reproduction, not evidence of passing it. Use the authors' actual code for variable definitions, missingness, gravity construction and Stata finite-sample conventions once acquired. No Stata executable was found on this machine; any Python translation must be labeled as such.

## Sources

- Saiz, Albert, and Susan Wachter (2011), *Immigration and the Neighborhood*, AEJ: Economic Policy 3(2),169–188. [Article and materials](https://www.aeaweb.org/articles?id=10.1257/pol.3.2.169). Main paper already cached in the modern lane.
- [Online appendix](https://www.aeaweb.org/articles/materials/1124), acquired 2026-09-19 into `_cache/online_appendix.pdf`; SHA-256 `306598d84c13cd48c003f49590d59fb58991300980e61627fe4e8b7cd676c21d`. `pdftotext -layout` produces its adjacent `.txt`.
- [Original replication archive, V1](https://www.openicpsr.org/openicpsr/project/114757/version/V1/view), DOI10.3886/E114757V1. Metadata observed; download pending terms acceptance. Original data will remain in ignored `_cache/` with hashes and a dataset-register entry after successful acquisition.

## Limits

Modern comparisons still use ACS medians, 12 controls, modern metro definitions and modern survey windows. Period A uses native 2010 boundaries; the ten-year 2013–2023 comparison inherits the old lane's dominant-parent 2020-to-2010 mapping and weighted averages of child medians. It is not a boundary-only or era-only experiment. The fixed5% ten-year sample has only13 metro clusters; report it as a descriptive sensitivity comparison. Overidentification statistics are not validated or reported by this bridge.
