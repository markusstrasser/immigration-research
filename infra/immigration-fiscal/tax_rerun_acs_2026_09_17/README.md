# One tax calculator on two surveys — September 17, 2026

This lane runs the Policy Simulation Library
[Tax-Calculator](https://github.com/PSLmodels/Tax-Calculator) on tax units built
from the CPS ASEC 2025 (income year 2024) and from the ACS 2024 1-year PUMS, and
reports the common-age federal income-tax and payroll-tax gaps per standardized
person for the same comparison groups in both surveys. The CPS run is anchored
against the Census Bureau's own tax-model variables (`FEDTAX_AC`, `FICA`).

Findings, gates and scope limits: [RESULT.md](RESULT.md).

## Reproduce

From this directory. Tax-Calculator 6.8.2 publishes no wheel, so the first run
builds it from the source distribution and takes several minutes; the version is
pinned because an unpinned resolve over the sdist index does not terminate
quickly.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --python 3.13 \
  --with "taxcalc==6.8.2" --with "numpy>=2.4" --with "pandas>=3" python3 cps_tax.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --python 3.13 \
  --with "taxcalc==6.8.2" --with "numpy>=2.4" --with "pandas>=3" python3 acs_tax.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --python 3.13 \
  --with "numpy>=2.4" --with "pandas>=3" python3 make_tables.py
```

The ACS arm holds the full 3.2M-record person file with 81 weight vectors in
memory and runs taxcalc over 1.9M returns in chunks; allow roughly 8 GB and ten
minutes. Generated files are ignored under `derived/`.

## Inputs

| Input | Path |
|---|---|
| CPS ASEC 2025 public use file | `../gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` |
| ACS 2024 1-year person PUMS | `/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip` |
| ACS PUMS data dictionary | `_cache/PUMS_Data_Dictionary_2024.csv` |

Nothing outside this directory is written. The CPS state is built by importing
the held `extend_ledger` builder, and the group definitions and gap estimators
are imported from `../acs_earnings_replication_2026_09_17/` so that the tax gaps
and that lane's earnings gaps are produced by the same code.

## Files

| File | Role |
|---|---|
| `taxcalc_io.py` | the only calculator call; chunked `Records`/`Calculator` run, employee-share payroll derivation |
| `units.py` | survey-independent assembly of persons into returns, counts, income splitting, allocation back to persons |
| `cps_tax.py` | CPS tax units, three income mappings plus an EITC sensitivity, the Census anchor |
| `acs_tax.py` | ACS tax units from relationship, marital status, age and enrolment |
| `shared.py` | cells, common-age and age-matched gaps, anchor table |
| `make_tables.py` | assembles `derived/taxcalc_gaps.csv`, `anchor_ratios.csv`, `audit.json`, `tables.md` |

## Outputs

`derived/taxcalc_gaps.csv` (both surveys' gaps), `derived/anchor_ratios.csv`
(CPS against the Census tax model), `derived/audit.json` (hashes, taxcalc
version, mappings, unit rules, diagnostics), `derived/tables.md` (rendered
tables), plus the per-survey `cps_tax_cells.csv`, `cps_tax_gaps.csv`,
`cps_anchor.csv`, `cps_audit.json`, `acs_tax_cells.csv`, `acs_tax_gaps.csv`,
`acs_totals.csv`, `acs_audit.json`.
