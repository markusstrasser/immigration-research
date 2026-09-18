**Verdict:** NO EVIDENCE of native displacement onto transfers on the margins this lane could
measure, and the margin most likely to carry it (SSDI) was unreachable. On 2000–2010, where the
shift-share instrument is alive, household SSI and public-assistance receipt move **down** with
foreign-born inflow, not up; every interval excludes a positive transfer response of the
Autor–Dorn–Hanson sign; the negative sign survives restricting the outcome to natives only, so it
is not a composition artifact. It is equally not evidence that immigration reduces transfer
receipt: the instrument fails a direct exogeneity test in 61 of 100 arms and 42 of 59 placebos
are significant. Native employment and participation are null throughout, which is what
Dustmann–Schönberg–Stuhler predict. The 2021–2024 surge cannot be studied with this instrument
at all (first-stage F 0.002) because the inflow did not follow the pre-1990 settlement pattern.
Design B is uninformative but its point estimate lands on the figure in question.

Model self-report: `claude-opus-5[1m]` (verbatim from the environment-info block).

Memo: `research/immigration-native-displacement-to-transfers-2026-09-18.md` (871 lines).

## Headline coefficients

Units throughout: change in the outcome in percentage points per 1 percentage-point rise in the
immigrant share of the metro population. HC1 robust standard errors, population-weighted.

### Design A, transfers, 2000-based windows (instrument alive, pre-1990 predetermined base)

| Window | Outcome | n | F | IV | 95% interval | IV + mean-reversion ctl | 95% interval |
|---|---|---:|---:|---:|---|---:|---|
| 2000–2007 | household SSI receipt | 333 | 21.5 | **−0.405** | [−0.661, −0.149] | −0.293 | [−0.488, −0.099] |
| 2000–2007 | household public assistance | 333 | 21.5 | **−1.226** | [−1.888, −0.565] | −0.488 | [−0.804, −0.172] |
| 2000–2005 | household SSI receipt | 332 | 18.7 | −0.297 | [−0.476, −0.118] | −0.219 | [−0.364, −0.073] |
| 2000–2008 | household SSI receipt | 333 | 16.3 | −0.361 | [−0.672, −0.050] | −0.102 | [−0.241, +0.038] |
| 2000–2010 | household SSI receipt | 334 | 29.1 | −0.442 | [−0.635, −0.250] | −0.424 | [−0.596, −0.253] |

### Design A, natives only (the composition check), 2005–2008, fixed-2013 geography

| Outcome | n | F | reduced form on Z | 95% interval | IV | 95% interval |
|---|---:|---:|---:|---|---:|---|
| native no-college SSI receipt | 348 | 13.0 | **+0.174** | [+0.013, +0.335] | **−0.490** | [−0.977, −0.003] |
| native no-college public assistance | 348 | 13.0 | +0.005 | [−0.146, +0.155] | −0.013 | [−0.432, +0.406] |
| native no-college E/POP | 348 | 13.0 | −0.132 | [−0.538, +0.275] | +0.370 | [−0.687, +1.428] |
| native no-college LFP | 348 | 13.0 | +0.109 | [−0.158, +0.375] | −0.306 | [−1.093, +0.482] |

First stage is **negative** (−0.355, SE 0.098), so the reduced form is the object identified.

### Design A, employment and the college control, fixed-2013 geography

| Window | Treatment | F | no-college E/POP | BA+ E/POP (control) | SSI receipt |
|---|---|---:|---|---|---|
| 2005–2008 | all foreign-born | 15.6 | −1.83 [−3.99, +0.34] | **−1.08 [−2.03, −0.13]** | +0.07 [−0.25, +0.39] |
| 2005–2015 | Mexico-born | 55.2 | −0.60 [−1.30, +0.10] | **+0.49 [+0.03, +0.95]** | −0.01 [−0.14, +0.13] |
| 2008–2018 | Mexico-born | 44.1 | −0.59 [−1.02, −0.17] | **+0.42 [+0.10, +0.74]** | **+0.21 [+0.08, +0.34]** |
| 2013–2023 | Mexico-born | 74.0 | −0.34 [−0.82, +0.14] | −0.02 [−0.42, +0.38] | +0.12 [−0.01, +0.26] |
| 2018–2023 | Mexico-born | 82.3 | +0.16 [−0.33, +0.66] | +0.17 [−0.22, +0.56] | −0.01 [−0.16, +0.13] |

The Mexican SSI sign tracks the sign of the national shift, not metros: negative or zero in all
four positive-shift windows, positive in four of five negative-shift windows.

### Design 2, the 2021–2024 shock (NOT IDENTIFIED)

First stage F **0.002** (2021–2024) and **0.370** (2021–2023). IV coefficients are noise
(SSI +11.2 [−494, +517]). OLS associations, 350 metros: SSI +0.018 [−0.067, +0.103];
SNAP **−0.370 [−0.669, −0.071]**; no-college E/POP +0.055 [−0.185, +0.295]. Five of six placebos
significant. The post-COVID recovery control moves nothing by more than one standard error.

### Design B, wages of earlier Mexico-born workers, 2005–2008, F 13.0

| Outcome | n | OLS | IV | 95% interval |
|---|---:|---:|---:|---|
| earlier Mexico-born (arrived pre-2000), wage per person | 292 | −0.01 | **−7.18%** | [−23.83, +9.46] |
| earlier Mexico-born, below BA, wage per person | 288 | +0.85 | +0.52% | [−14.56, +15.60] |
| earlier Mexico-born, E/POP (pp) | 299 | −0.15 | −2.08 | [−12.23, +8.08] |
| 2000-and-later arrivals, wage per person | 240 | +3.15 | −13.36% | [−39.43, +12.72] |

Mexican second generation at metro level is **impossible from ACS** — no parental-birthplace
variable since 1970.

### Elasticity-transfer bound (arithmetic, not estimation)

Mexico-born wage bill 2024 **$352.0 bn** (12.23 M people); Mexican second generation
**$325.5 bn** (14.35 M). Annual fiscal cost of wage incidence:
**$1–3 bn** scoring the actual 2021–24 inflow (4.96 M = 2.95% of the labour force) with Borjas's
−3 to −4% per 10% supply; **$4–26 bn** scoring a 1990s-scale inflow with Ottaviano–Peri, where
the factor-of-three width is the unresolved −6.7% (brief, **[UNVERIFIED]**) versus −19.8%
(verified, NBER w12497 Table 7) question.

### Benchmarks, pinned before estimating

ADH 2013 Table 8 panel B, per $1,000/worker of import exposure: total transfers **+$57.73**
(SE 18.41), SSDI **+$8.40** (SE 2.21), federal income assistance **+$7.20** (SE 2.35); log
versions +1.01, +1.96, +3.04, all significant at 1%. **SSDI is not measured in this lane** —
SSA county files returned HTTP 403.

## Verification commands

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/displacement_transfers_2026_09_18
R="uv run --no-project --with pandas>=2 --with numpy>=2 --with linearmodels --with statsmodels python3"

# 1. panels (need xlrd+openpyxl for the OMB delineation .xls)
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 build_panel.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 build_2000.py
uv run --no-project --with "pandas>=2" --with "numpy>=2" --with xlrd --with openpyxl python3 build_pums_panel.py

# 2. estimates (both reproduce byte-identical)
$R estimate.py        # -> derived/estimates.csv       2004 rows
$R estimate_pums.py   # -> derived/estimates_pums.csv   158 rows

# 3. wage bills and the bound (no network)
uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 wage_bills.py
uv run --no-project --with "pandas>=2" python3 elasticity_bound.py

# 4. spot-check the headline row
uv run --no-project --with "pandas>=2" python3 -c "
import pandas as pd
d=pd.read_csv('derived/estimates.csv')
print(d[(d.window=='2000-2007')&(d.outcome=='ssi_rate')&(d.treat=='all foreign-born')
        &(d.estimator.isin(['IV','first-stage','Z-ON-BASELINE-LEVEL (exogeneity test)']))]
      [['estimator','n','coef','se','lo','hi','first_stage_F']].round(3).to_string(index=False))"

# 5. re-fetch anything (needs the key; sourcing it is required, printing it is not)
set -a; . ../acquire/config.local.env; set +a
uv run --no-project python3 fetch_metro.py       # ACS metro tables, resumable
uv run --no-project python3 fetch_sf3_slim.py    # Census 2000 SF3, resumable
PUMS_YEARS=2005,2008,2021,2024 WORKERS=10 uv run --no-project python3 pull_pums.py  # resumable
```

`estimates.csv` sha256 begins `f8cddb955504b280`; `estimates_pums.csv` begins `57d91563d2b9c2d7`.

## Files covered

| File | What it is |
|---|---|
| `BRIEF.md` | the dispatch brief, verbatim |
| `fetch_metro.py` | ACS 1-year summary tables at CBSA level, 13 years |
| `fetch_sf3_slim.py` | Census 2000 SF3 county pull, 10 columns, one request per state |
| `fetch_sf3.py` | the abandoned full-table version, kept with its reason in the docstring |
| `pull_pums.py` | ACS PUMS PUMA cells: natives 25–54 below BA, and Mexico-born 25–54 by arrival cohort |
| `build_panel.py` | the ACS metro aggregate panel |
| `build_2000.py` | the Census 2000 endpoint and the pre-1990 base shares |
| `build_pums_panel.py` | PUMA → county → fixed 2013 CBSA, with the footprint guard |
| `estimate.py` | OLS / IV / reduced form / first stage / placebo / exogeneity test / level control |
| `estimate_pums.py` | Design B and the nativity-split Design A |
| `wage_bills.py` | wage bills by Mexican-origin generation from CPS ASEC 2025 |
| `elasticity_bound.py` | the Ottaviano–Peri and Borjas transfer, as a range |
| `derived/estimates.csv` | 2,004 rows, every aggregate arm |
| `derived/estimates_pums.csv` | 158 rows, Design B and the nativity split |
| `derived/metro_panel.csv` | 7,097 metro-years, 2000–2024 |
| `derived/pums_metro_panel.csv` | 1,516 metro-years, 380 CBSAs, 4 years |
| `derived/base_shares_pre1990.csv` | pre-1990 entry-cohort base shares, 381 CBSAs |
| `derived/national_stock.csv` | national population, foreign-born and Mexico-born, 2000–2024 |
| `derived/wage_bills.csv` | 5 groups × 2 age bands, persons, wage bill, tax rate |
| `derived/elasticity_bound.csv` | 30 rows, every elasticity × group × tax-rate combination |
| `_cache/adh2013.pdf`, `_cache/op_nber_w12497.pdf`, `_cache/borjas2003.pdf` | benchmark primary texts |
| `_cache/NST-EST2025-ALLDATA.csv` | Census Vintage 2025 components of change |

## Files and sources skipped, with reasons

| Skipped | Reason |
|---|---|
| SSA "OASDI Beneficiaries by State and County" | HTTP 403 on every request, with and without a browser user-agent. **SSDI is therefore unmeasured — the single most important gap** |
| BEA CAINC35 county transfer receipts | bulk zip last-modified 2023-11-16, so it cannot reach 2023; no BEA API key available |
| CBO January 2025 demographic outlook | cbo.gov HTTP 403 |
| Census 1990 STF3 (a 1990 base) | `api.census.gov/data/1990/sf3` returns 404, endpoints retired; no NHGIS or IPUMS key in this environment. Replaced by the pre-1990 entry cohort from Census 2000 P022/PCT020 |
| Census 2000 education × employment at county | SF3 P038 is the 16–19 population; no 25–64 cross-tab exists. Employment outcomes therefore start in 2005 |
| Published JEEA 2012 Ottaviano–Peri | paywalled on Oxford Academic, Wiley and EconPapers. The brief's −6.7% stays **[UNVERIFIED]**; the NBER working paper was read instead |
| Mexican second generation at metro level | ACS has no parental-birthplace variable since 1970; only CPS has it, and not at 372-metro resolution |
| ACS 2005 full-time-full-year cells | `WKW` is continuous 1–52 in 2005 and bracketed from 2008, so the pull's `wkw == 1` test selected people who worked one week. Discarded; full-time windows start 2008 |
| ACS 2005 SNAP cells | the ACS SNAP question begins in 2008; 2005 cells read 0.01%. Discarded |
| Vermont 2005 PUMS | not pulled; the 8 metros spanning it are dropped from every year so no metro changes footprint |
| City shelter-intake design for 2021–24 | five treated metros is a case study, not a 350-metro regression. New York's counts are staged in `frontier_execution_2026_09_17/local/` for a successor |
| Local IPUMS 44M-row panel | state-level geography only, no sub-state codes — same finding as ladder 136 |
| `ledger-underreport` adjustment factors | not applied to the survey receipt rates used here |

## Note on a shared-resource finding

Mid-run, a peer lane (`tiebout_sorting_2026_09_18/pull_pums_migration.py`) was pulling ACS PUMS
over the same api.census.gov link and sustained throughput fell to roughly 500 B/s. The PUMS pull
here was re-scoped in response (natives narrowed to 25–54 below a bachelor's, with both the
nativity and education selections pushed onto the server) and completed. Any future lane planning
a national PUMS pull should check for a concurrent one first.
