# Causal execution, 20 September 2026

This lane records executed designs and their limits. It does not turn population
accounting differences into effects of admission or removal. Raw data and generated
tables remain ignored; source locks, code, and evidence notes are versioned.

Results: [causal execution](../../../research/immigration-causal-execution-2026-09-20.md)
and [school-capacity harms](../../../research/immigration-school-capacity-harms-2026-09-20.md).
The [Mariel subfolder](mariel/README.md) contains the public fiscal reconstruction.
`school_spillovers.py` reproduces published-table arithmetic and conditional
resource scenarios; it is not new student microdata estimation.

## Mexican-inflow crime model

Chalfin (2015), [official replication](https://doi.org/10.3886/E113382V1).
The operator's existing `113382-V1.zip` was found and verified locally. No new
download agreement was accepted in this run. The archive supplies BSD-3-Clause
code and CC-BY-4.0 data; its full license is retained with the raw files.

```sh
uv run python3 infra/immigration-fiscal/causal_execution_2026_09_20/acquire_chalfin.py --archive /path/to/113382-V1.zip
uv run python3 infra/immigration-fiscal/causal_execution_2026_09_20/replay_chalfin.py --data infra/immigration-fiscal/causal_execution_2026_09_20/raw/chalfin/data/chalfin_data.dta --out infra/immigration-fiscal/causal_execution_2026_09_20/derived/chalfin
uv run --with scipy python3 infra/immigration-fiscal/causal_execution_2026_09_20/verify_chalfin.py --results infra/immigration-fiscal/causal_execution_2026_09_20/derived/chalfin/chalfin_replay.json
```

Dependencies: project numpy/pandas, scipy for independent pivoted QR. On this
machine the commands also use `UV_CACHE_DIR=/private/tmp/codex-uv-cache`; use
`--offline` when rerunning with cached dependencies and unavailable networking.

1. **Comparison:** a one-unit change in archived `dmexfb_alt`, equal numerically to
   one percentage point of change in `mexfba`; 92 metropolitan areas, 1980–2000.
   The exact age definition still needs upstream documentation.
2. **Variation:** supplied Mexican-cohort/network instrument `dins`. The archive
   contains the prepared instrument, not the complete source-cohort build.
3. **Outcomes:** seven recorded offense changes. Crucially, supplied `dlogpc_*`
   equals change in log counts, despite rate-suggesting names. A separate analysis
   reconstructs changes in the supplied contemporaneous log-rate levels.
4. **Checks:** input hash/dimensions; original command's controls, weights and
   cluster CR0 covariance; first stages; original falsifications; 644 MSA
   exclusions; fewer-controls sensitivity; weak-IV AR sets; independent full-matrix
   coefficients, covariance and AR test inversions; raw variable identities.

This is a Python translation of archived commands, not native Stata execution or
a verified match to the final article's tables. Numerical rank/omission differences
remain a cross-software limitation. AR inference uses asymptotic cluster tests;
it does not repair instrument invalidity, correlated origin shocks or influential
clusters. Intervals are per outcome, not simultaneous across seven outcomes.

The geography of crime reporting and Census exposure has not been reconciled.
There is no per-arrival or national victim-dollar conversion. No offense is
assigned a victim cost merely because it is an immigration-status violation.

## Source lock

- Archive: 138,701 bytes, SHA-256
  `d7cfaf74028b1dc74ea87e4dea4075e941909317403014fad1da24958fbd0fa9`.
- Stata data: 259,427 bytes, SHA-256
  `d41b4882f615cfe8063f16ee6dcd0e26f3cf43873f661529234518174d1b567d`.
- Original Stata code: 1,776 bytes, SHA-256
  `63d899762eeed4a96b108881015ce97e861acaa418937838580fe04af18ccfdf`.
- License: 14,974 bytes, SHA-256
  `df9617509f34b9cbe7e8112356cb9f2a3152daeea5921c6c31df17b98518c0c2`.

The acquisition script checks the archive hash, exact member set and all CRCs,
preserves existing identical raw bytes and refuses changed inputs. The independent
verifier rejects missing/duplicate endpoints, altered coefficients/covariances,
incorrect AR sets and mismatched input provenance. It checks all 1,282 nonmissing
offense changes and 184 exposure changes, rather than accepting an empty match.
Its independent numerical certification covers the seven baseline models; other
sensitivity blocks are executed by the generator and are not separately certified
by that verifier. `test_checks.py` reproduces corruption probes under `python -O`
and checks all 21 saved fiscal models and placebo paths against their panels.

Two independent native code reviews identified defects in saved-inference checks
and placebo donor selection; both were fixed and the affected analyses rerun.
The operator-authorized Cursor review could not run because the CLI lacked an
authenticated session. No external review result is claimed.
