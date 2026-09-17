# ACS 2024 earnings replication of the CPS ledger gaps — September 17, 2026

Independent-survey check on the earnings and income gaps that drive the CPS-based
all-age fiscal ledger (`../all_age_ledger_2026_09_17/`). Reviewers asked whether
CPS earnings measurement drives the modeled income/payroll tax component. This
lane recomputes the *earnings and income gaps* on ACS 2024 1-year PUMS and places
them beside the CPS gaps computed with the ledger's own group definitions.

Both surveys are self-reported. This tests survey-specific measurement design,
sampling and editing, **not** self-report bias in general; an error common to both
instruments would not show up here.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/acs_earnings_replication_2026_09_17
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "numpy>=2" --with "pandas>=2" python3 cps_gaps.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --with "numpy>=2" --with "pandas>=2" python3 acs_gaps.py
```

`cps_gaps.py` imports the held builder `../gen_ledger_extension_2026_09_16/extend_ledger.py`
and reads the held CPS ASEC 2025 ZIP; nothing outside this directory is written.
`acs_gaps.py` reads
`/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`
(ACS 2024 1-year person PUMS, all four parts). Gate 3 needs `CENSUS_API_KEY` in
`../acquire/config.local.env`.

## Outputs (`derived/`, ignored)

| File | Contents |
|---|---|
| `acs_gaps.csv` | ACS common-age per-person and age-matched aggregate gaps vs native NH whites, national/CA/TX |
| `acs_cells.csv` | ACS group x age-band populations, mean WAGP/PINCP/PERNP, employment rate 16+ |
| `cps_gaps.csv` | CPS gaps against both the ACS-aligned and the ledger reference |
| `cps_cells.csv` | CPS group x age-band populations and mean WSAL_VAL/PTOTVAL |
| `audit.json`, `cps_audit.json` | source hashes, group definitions, gate results |

Findings and caveats: `RESULT.md`.
