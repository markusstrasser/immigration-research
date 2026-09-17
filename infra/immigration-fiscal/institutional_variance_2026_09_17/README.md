# Replicate variance on the institutional cost bound — September 17, 2026

Puts SDR sampling intervals on the Δ quantities of `../institutional_bound_2026_09_17/`, which
priced ACS institutional group-quarters counts at sourced costs but had no interval because the
Census API tabulate endpoint returns point estimates only. Findings: [RESULT.md](RESULT.md).

## Reproduce

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "numpy>=2" --with "pandas>=2" \
  python3 infra/immigration-fiscal/institutional_variance_2026_09_17/inst_variance.py
```

Reads the staged ACS 2024 1-year person PUMS at
`/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`
(both parts, in chunks) plus the bound lane's `derived/acs_cells.csv`,
`derived/institutional_bound.csv` and `derived/audit.json` for the two gates. Cost constants are
exec'd out of the bound lane's `compute_bound.py` source rather than imported, so that lane's
script never re-runs and none of its numbers are restated here. Writes only inside this
directory, into `derived/` (git-ignored). Runtime is a few minutes, dominated by the CSV read.
