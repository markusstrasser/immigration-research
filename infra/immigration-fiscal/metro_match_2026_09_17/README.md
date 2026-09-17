# Metro-level matched fiscal gaps — September 17, 2026

Metro-group × age matching on the all-age partial fiscal account, the counter the
essay names against the state-matched result in
[`ledger_stress_2026_09_17`](../ledger_stress_2026_09_17/). Three standards are
computed at a common 4-band age resolution (0–17, 18–44, 45–64, 65+) so they can be
compared: age only, state group × age, metro group × age. Results and
interpretation: [RESULT.md](RESULT.md).

Nothing outside this directory is written. The stress lane's `common.py` is imported
for its objects; the upstream `analyze.generate()` is never called.

## Reproduce

From the repository root, using the held inputs:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/metro_match_2026_09_17/metro_tests.py
```

Runs in about 10 seconds and requires NumPy and pandas. Outputs land in `derived/`,
which is ignored. The script raises rather than degrading if any gate fails.

## Layout

| File | Role |
|---|---|
| `geo.py` | Merges `GTCBSA`/`GTMETSTA` from the CPS household file onto the person frame by `PH_SEQ`; defines the 23 metro groups in the brief's priority order, the 4-band age standard, and the resolver that merges sparse groups upward into their state's "other metro" group |
| `metro_tests.py` | The three standards, the generation contrasts, the single-metro restrictions, and gates (a)–(d) |
| `derived/metro_matched.csv` | 480 rows: scenario × standard × target × reference × {`gap_total`, `gap_per_person`, `standardized_gap_per_person`} with CPS and MEPS standard errors and 95% intervals |
| `derived/metro_generation_contrasts.csv` | 24 rows: paired later-minus-earlier generation contrasts with replicate covariance, under each standard |
| `derived/metro_populations.csv` | 258 rows: records, full-weight population, minimum cell records and minimum cell population over all 161 weight vectors, per metro group × group, at both the as-defined and retained stages |
| `derived/audit.json` | Gate results with numbers, the merge log with triggers, and SHA-256 hashes of every input |

## Geography

CPS ASEC carries the CBSA code on the household record, not the person record, so
`geo.attach()` repeats the `PH_SEQ` merge `extend_ledger.build` uses for `GESTFIPS`
and asserts the two agree. `GTCBSA = 0` means non-metro or a metro Census suppresses;
24.1% of records. Those go to the state's "non-metro or unidentified" group.

Three of the 23 defined groups fail the positivity gate at 4 age bands with an
outright empty cell and are merged into their state's "other metro" group: San Jose,
California non-metro, Texas non-metro. A fourth standard, `metro_x_age_4_rf5`,
repeats the metro cells under an additional 5-sample-record floor per key group ×
cell, which retains 10 groups; it is the robustness check on the one-record cells the
primary geography keeps.

## Inputs

Held CPS ASEC 2025 ZIP (income year 2024, including `hhpub25.csv`), MEPS 2024
full-year file and SAS positions, the extension lane's state parameters, and the
source lane's stored `derived/estimates.csv` used as the collapse anchor. SHA-256
hashes of all of them, plus `geo.py` and `metro_tests.py`, are in `derived/audit.json`.
