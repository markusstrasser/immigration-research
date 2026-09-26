# Returnees vs US stayers (ENADID × ACS PUMS), 2018 and 2023

Compares Mexico-born adults who lived in the US five years before an ENADID survey and are back in
Mexico with Mexico-born adults who were in the US at the start of the same window and are still
there (ACS one-year person PUMS of the same year). Findings: [RESULT.md](RESULT.md). Brief:
[BRIEF.md](BRIEF.md).

## Run

From the repository root:

```sh
bash infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/verify_acs_2023.sh   # once; about a minute
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/compare.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/return_vs_us_stayers_2026_09_26/ -q
```

`compare.py` takes about 40 seconds and stops with `GateFailure` if any gate fails: input sha256s,
the ENADID numbers against `enadid_return_selectivity_2026_09_22/RESULT.md`, the SCHL band map
against the brief, and the B05006 Mexico-born anchor within 0.5%. Two runs on 2026-09-26 wrote
byte-identical `derived/` files.

## Inputs (read-only)

| Input | Path | Pin |
|---|---|---|
| ENADID returnees | `enadid_return_selectivity_2026_09_22/derived/return_migrants_by_schooling.csv` | gated against that lane's RESULT.md |
| ENADID departures | `enadid_return_selectivity_2026_09_22/derived/departures_by_schooling.csv` | same |
| ACS 2018 person PUMS | `sources/immigration-fiscal/data/external/acs_pums_years/csv_pus_2018.zip` | sha256 from `download.log` |
| ACS 2023 person PUMS | `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip` | sha256 from `service_by_ses_2026_09_23/derived/acs_inputs.json`; `verify_acs_2023.sh` |
| IPUMS USA extract 3 | `sources/immigration-fiscal/derived/ipums_usa/usa_00003_…_mexborn.parquet` | sha256 in `compare.py`; used only for the 2019/2020 break series |
| SCHL map and years | `schooling_selection_position_2026_09_23/acs_pums_check.py`, `levels.py` | imported |
| B05006 Mexico row | data.census.gov table API, URL in `derived/anchor.csv` | values in `compare.py`; responses in `_cache/` (ignored) |

The brief asked for a fresh 2023 download into `acs_pums_years/csv_pus_2023.zip`. The repository
already holds that release at `census/acs_pums_2023_person.zip` (fetched by `acquire/setup.sh` from
the same URL), and the Census server delivered 27 kB/s on 2026-09-26, so the download was stopped and
its partial file removed. `verify_acs_2023.sh` instead checks the held copy against the served file:
equal Content-Length, the zip central directory and sixteen 16 KiB ranges byte-identical to HTTP
range reads, `unzip -tqq`, and the recorded sha256. No file was added to `acs_pums_years/`
and no line to its `download.log`.

## Outputs (`derived/`)

- `stayers_by_schooling.csv`: ACS stayer estimates by wave, spec, slice and standardization, with
  replicate SEs.
- `comparison.csv`: returnee, stayer, difference (returnee minus stayer) and SE for every slice and
  spec, plus the short-stay rows.
- `anchor.csv`: PUMS Mexico-born foreign-born total against B05006, with the URL and the gap.
- `acs_no_schooling_break.csv`: ACS no-schooling share among Mexico-born 20–64 by survey year,
  2008–2024 (IPUMS).
- `audit.json`: input hashes, record counts, universe profile (GQ share, allocated share, arrival
  age), ENADID gates passed, 2023 break parameters, short-stay context, stock-shift arithmetic.
