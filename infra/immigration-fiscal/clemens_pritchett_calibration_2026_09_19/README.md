# Lane: Clemens–Pritchett calibration with the repo's Mexican-origin generation data

Re-solves the Clemens–Pritchett (2019 JDE, working paper IZA DP 9730) "epidemiological case"
model with the assimilation rate `a` and transmission rate `tau` set from this repo's own
Mexican-origin measurements instead of the paper's pooled poor-country census figures.

## Run

```bash
cd infra/immigration-fiscal/clemens_pritchett_calibration_2026_09_19
bash run.sh
```

`run.sh` is idempotent: a second run leaves `derived/` byte-identical
(verified with `cp -R derived /tmp/run1 && bash run.sh && diff -r /tmp/run1 derived`).

Individual steps, each runnable on its own in this order:

```bash
UV="uv run --no-project --with pandas>=2 --with numpy>=2 --with scipy --with openpyxl python3"
PYTHONUNBUFFERED=1 $UV parse_paper.py     # Table 1 + constants out of the pinned PDF text
PYTHONUNBUFFERED=1 $UV gate.py            # reproduction gate, exits non-zero on any failure
PYTHONUNBUFFERED=1 $UV repo_inputs.py     # repo-measured a and tau
PYTHONUNBUFFERED=1 $UV observed_rate.py   # observed Mexican migration rate and stock
PYTHONUNBUFFERED=1 $UV mstar.py           # eq. (8) over the parameter grid
PYTHONUNBUFFERED=1 $UV arms.py            # disconfirmation arms
PYTHONUNBUFFERED=1 $UV make_tables.py     # derived/tables.md
```

## Inputs

### Pinned external sources (`_cache/`, gitignored; sha256 in `_cache/SHA256SUMS.txt`)

| File | What | Retrieved from |
|---|---|---|
| `dp9730.pdf` / `.txt` | Clemens & Pritchett, *The New Economic Case for Migration Restrictions: An Assessment*, IZA DP 9730, Feb 2016 | `https://docs.iza.org/dp9730.pdf`; text via `pdftotext -layout` |
| `dhs_lpr_fy2024.xlsx` | DHS OHSS Yearbook of Immigration Statistics FY2024, Table 3 (LPR by country of birth) | `https://ohss.dhs.gov/topics/immigration/yearbook/2024/table3` |
| `NA-EST2024-POP.xlsx` | Census Bureau monthly national population estimates, Vintage 2024 | `https://www2.census.gov/programs-surveys/popest/tables/2020-2024/national/totals/` |

The published Journal of Development Economics version (doi:10.1016/j.jdeveco.2018.12.003) was
resolved through the research MCP for title and authorship but is paywalled; all equations,
Table 1 coefficients and stated ranges come from the open working paper, parsed from its own
text, never from memory.

### Repo inputs, read-only

| Path | Used for |
|---|---|
| `research/immigration-mexican-origin-by-generation-2026-09-16.md` | mean and median earnings by generation; ethnic-attrition share; white vs all-native reference shift |
| `research/immigration-confidence-ladder.md` | entry 110 adjusted generalized-trust gaps |
| `acs_earnings_replication_2026_09_17/derived/cps_gaps.csv` | common-age wage and income gaps vs third-plus non-Hispanic whites |
| `all_age_ledger_2026_09_17/derived/estimates.csv` | fiscal balance gaps at the age-only standard; Mexican-origin population counts |
| `ledger_stress_2026_09_17/derived/state_matched.csv` | fiscal balance gaps at the joint state × age standard (ladder 125) |
| `norms_gen_2026_09_18/derived/mex_synth_table.md` | Mexican-origin attitude and institutional items by generation (ladder 135) |
| `arrival_cohorts_2026_09_18/derived/acs_wage_residual_by_ysm_band.csv` | education- and age-conditional log-wage residual by years since arrival, the paper's own `delta` object |
| `arrival_cohorts_2026_09_18/derived/ipums_wage_residual_by_ysm_band.csv` | the same residual on the 1980–2023 census panel |

Nothing under `research/` is written. Nothing is committed.

## Outputs (`derived/`)

| File | Contents |
|---|---|
| `paper_table1.csv` | the paper's Table 1 regression coefficients and its own derived rows, parsed from the PDF text |
| `paper_constants.json` | gamma, beta, alpha, rho, m0 and the stated ranges, each located by its own sentence |
| `gate_log.txt` | the reproduction gate, seven checks, human-readable |
| `gate.csv` | per-country reproduction numbers and the phi = m*/a diagnostic |
| `parameters.csv` | 21 repo outcomes with G1/G2/G3+ gaps and the implied `a` at three generation lengths |
| `tau_repo.csv` | 9 transmission-rate constructions for Mexico |
| `observed_migration.csv` | observed Mexican migration rate and stock shares, with sources |
| `mstar_by_outcome.csv` | eq. (8) for every usable outcome × tau × congestion rate |
| `mstar_grid.csv` | the (a, tau, c) surface on a regular grid |
| `sign_flip.csv` | where eq. (8) crosses zero in each parameter |
| `arms.csv` | 21 disconfirmation arms |
| `tables.md` | all of the above rendered as tables |

## Files

`cpmodel.py` holds the model (equations 2, 3, 8, 9, 12 and the fixed-precision formatter that
makes reruns byte-identical). Everything else is a step in `run.sh`.
