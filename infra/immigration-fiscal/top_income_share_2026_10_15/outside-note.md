**Verdict:** The SCF checks support treating the CPS $1M+ share as uncertain and allowing materially lower arms. They do not identify the Mexican-origin union's income-tax share. The conditional SCF-to-CPS diagnostic is 1.36% in SCF2019 and 0.93% in SCF2022 at $1M+, against the case's approximately 3.5%. The SCF tail remains sparse: only 14 and 15 distinct Hispanic families, respectively. Published Akee–Jones–Porter numerical tables remain **[UNVERIFIED]**; no numerical result from that paper enters this lane's calculations.

## Exact objects and results

The primary SCF object is the share of **gross family income** belonging to families whose respondent identifies as Hispanic of any race (`X7004=1` or `X6809=3`, matching the Fed macro's `H_RACE=3`). Its companion is the share of **family counts** in the same income band. These are family objects, whereas CPS AGI carriers and personal income-tax allocations are different objects. The SCF file does not establish tax liabilities, Mexican origin, parental origins, or the v8 nonreporting descendants. [SOURCE: Federal Reserve `bulletin.macro.txt`; DATA: `derived/outside_sources.csv`]

All thresholds below are real 2023 dollars, applied to SCF gross income, rather than SCF AGI. Entries are percentages; family counts are distinct survey families across all five implicates, never implicate rows. [CALCULATION: `derived/outside_scf.csv`]

| SCF survey (income year) | Income band | Hispanic share of family counts | Hispanic share of gross income | Distinct Hispanic families appearing in band |
|---|---:|---:|---:|---:|
| 2019 (2018) | $200–500k | 5.71 | 5.14 | 45 |
| 2019 (2018) | $500k–1M | 3.05 | 3.00 | 11 |
| 2019 (2018) | $1M+ | 2.95 | 3.06 | 14 |
| 2022 (2021) | $200–500k | 7.56 | 7.09 | 64 |
| 2022 (2021) | $500k–1M | 7.08 | 6.12 | 19 |
| 2022 (2021) | $1M+ | 1.70 | 2.09 | 15 |

The bridge uses the all-year CPS pool's **union share of Hispanic personal federal-income-tax dollars**, 49.800% at $200–500k, 46.237% at $500k–1M and 44.407% at $1M+. Multiplying the SCF Hispanic gross-income share by this tax bridge gives the following **conditional diagnostic**, not observed union taxes. It assumes the SCF Hispanic income share transfers to the Hispanic share of tax, and the CPS union/Hispanic personal tax ratio transfers across survey units and years. Matched survey-year bridges are also preserved, rather than silently substituted for the pool. [CALCULATION: `derived/cps_hispanic_bridge.csv`, `derived/outside_bridge.csv`]

| SCF year | $200–500k conditional proxy | $500k–1M conditional proxy | $1M+ conditional proxy |
|---|---:|---:|---:|
| 2019 | 2.56% | 1.39% | 1.36% |
| 2022 | 3.53% | 2.83% | 0.93% |

The alternative bridge multiplies SCF family-count share by CPS union/Hispanic **carrier-weight** share. At $1M+ it gives 1.30% and 0.75%. That alternative still crosses family and filer units; it is another diagnostic, not a confidence interval. A mixed family can be classified by its respondent while its tax belongs partly to a non-Hispanic partner. No national receipt total, stack factor or v8 ledger line is changed by these outside-check calculations. [CALCULATION: `derived/outside_bridge.csv`]

## Prices, imputation and independent validation

`outside_checks.py` reads only 26 fields from the full nominal SCF public files. Following the Fed macro, gross income is `max(0,X5729)` plus annualized IRA and pension-account withdrawals. It uses **previous-calendar-year nominal income** and directly multiplies by BLS CPI-U annual average `304.702 / 251.107` for SCF2019 and `304.702 / 270.970` for SCF2022. These are the same CPI-U series and real-2023 basis as the CPS pool. It does not treat survey-year SCF income as nominal income earned in that year. [SOURCE: Fed macro `INCOME`, `PENACCTWD`, `MCONV`; BLS `CUUR0000SA0`, `M13`; DATA: `derived/outside_scf_audit.csv`]

This avoids a source-version trap: the downloaded Federal Reserve pages now label summary extracts in **2025 dollars**, while the preexisting local 2022 extract is in **2022 dollars**. All nominal raw-file transformations are explicit. The reconstructed 2022 incomes were matched one-to-one by `Y1` against that official summary extract, allowing a single common price multiplier: `1.0809118236472945`. Maximum relative discrepancy is below `3e-16`; summary weights equal raw `X42001/5` exactly. The official extract therefore independently validates the reconstructed income fields and frequency conversions. [CALCULATION: `derived/outside_reconstruction.csv`; regression in `test_outside_checks.py`]

There are 5,777 public families/28,885 implicate rows in 2019 and 4,595/22,975 in 2022. Each family must have implicates 1–5 or the script stops. Within an implicate, `X42001` expands to the family population. Reported shares are the average of five separate weighted ratio estimates; reported family totals average the five expanded totals. Averages do not count five imputed copies as independent families. The output includes each implicate, min/max counts and shares, and Kish effective sizes. **No SCF sampling standard error is estimated**: bootstrap replicate weights were not acquired, and the between-implicate range must not be read as a sampling interval. [CALCULATION: `derived/outside_scf_implicates.csv`, `derived/outside_scf_audit.csv`]

## Disconfirmation and limits

The outside checks do not establish a monotonic decline. SCF2019's Hispanic gross-income share is nearly flat between $500k–1M and $1M+; SCF2022 declines, but its $5M+ share rebounds to 3.39%, from 2.09% for all $1M+. That $5M+ estimate rests on only five distinct Hispanic families. SCF2019's $5M+ share is 0.96%, also five families. Variation within the SCF and across years is material disconfirming evidence against treating a fitted monotonic curve as observed truth. [CALCULATION: `derived/outside_scf.csv`]

The SCF oversamples wealthier families, giving a useful design contrast to CPS; public disclosure protection, sparse ethnicity cells, gross-income/AGI differences, income year and respondent classification remain. The secondary `fed_racecl4_hispanic` definition (`X6809=3`, `X6810=5`) is retained in every SCF output to show sensitivity to the Fed's conventional mutually exclusive race grouping. The broad ethnicity definition used for the bridge is stated explicitly. The outside checks alone cannot select a unique top-tax rule. [SOURCE: Federal Reserve survey documentation archived in `_cache/outside/scf_2019.html` and `scf_2022.html`; INFERENCE]

## Akee, Jones and Porter: verified identity, unavailable published tables

The publisher verifies **Randall Akee, Maggie R. Jones and Sonya R. Porter**, “Race Matters: Income Shares, Income Inequality, and Income Mobility for All U.S. Races,” *Demography* **56(3), 999–1021 (2019)**, DOI **10.1007/s13524-019-00773-7**. The abstract describes linked IRS filers and Census/ACS race and ethnicity for 2000–2014. [SOURCE: https://read.dukeupress.edu/demography/article/56/3/999/167998/Race-Matters-Income-Shares-Income-Inequality-and]

The publisher full-text URL redirects to an abstract; its PDF returns 403 through curl, and the Springer PDF was inaccessible. **[UNVERIFIED]** Numerical values in the final published tables could not be opened and are not used. The UCLA repository's DOI2019 cover sheet is misleading for version matching: its attached PDF begins **NBER Working Paper 23733, August 2017**. It is an earlier primary working paper, not verification of the final published tables. It also studies individual working-age filers and equivalized AGI, rather than all-age families or this lineage. [SOURCE: https://escholarship.org/content/qt5vp9q702/qt5vp9q702.pdf, PDF pages 1–2 and 8–9; no numerical result adopted]

ACS PUMS was considered and skipped: the local 2023 person file exists, but matching reported personal-income thresholds would measure another object, and identifying genuinely top-coded persons would require the state-specific top/bottom-code rules rather than labelling everyone above an income threshold top-coded. It would not provide the union's parents, nonreporting descendants or income taxes. This is a scoped omission, not a claim that ACS data are absent.

## Reproduction and paths

Run `uv run --no-project python3 infra/immigration-fiscal/top_income_share_2026_10_15/outside_checks.py` after `cps_pool.py`. It writes only `derived/outside_*.csv`; `--out-dir` permits scratch reproduction. Input absence, incorrect implicate structure, missing CPI years, bridge ambiguity and official-summary reconstruction mismatch fail loudly. Raw2019 acquisition used `curl -L --fail -A 'Mozilla/5.0' https://www.federalreserve.gov/econres/files/scf2019s.zip`; urllib's default user agent received 403. The downloaded archive is 10.1 MB, well below the 10 GB boundary. [DATA: local input manifest `derived/outside_sources.csv`]

Validation: eight tests passed in 2.06 seconds. They cover the five-implicate denominator, income year, pension-frequency calculation, raw/summary parity, CPI source, sparse-family reporting, bridge-bin selection and missing-implicate failure. The final compute run with keyed parity took 4.303 seconds and peaked at 0.139 GiB. A separate scratch rerun took 5.691 seconds, peaked at 0.142 GiB and reproduced all six CSV files byte for byte. Timing uses `time.perf_counter` and `resource.getrusage`; derived outputs contain no volatile timing values. The parent owns the complete lane's `rerun_lane.py` invocation because other lane scripts have separate owners.

Paths written by this worker, relative to this lane unless absolute:

- `outside_checks.py`
- `test_outside_checks.py`
- `outside-note.md`
- `derived/outside_bridge.csv`
- `derived/outside_reconstruction.csv`
- `derived/outside_scf.csv`
- `derived/outside_scf_audit.csv`
- `derived/outside_scf_implicates.csv`
- `derived/outside_sources.csv`
- `_cache/outside/scf2019s.zip`
- `_cache/outside/scf2019/p19i6.dta`
- `_cache/outside/bulletin.macro.txt`
- `_cache/outside/scf_2019.html`
- `_cache/outside/scf_2022.html`
- `_cache/outside/akee_access.json`
- `/private/tmp/toptax-outside-repro/outside_bridge.csv`
- `/private/tmp/toptax-outside-repro/outside_reconstruction.csv`
- `/private/tmp/toptax-outside-repro/outside_scf.csv`
- `/private/tmp/toptax-outside-repro/outside_scf_audit.csv`
- `/private/tmp/toptax-outside-repro/outside_scf_implicates.csv`
- `/private/tmp/toptax-outside-repro/outside_sources.csv`

No other lane was edited. Existing 2022 SCF and BLS sources were read only. The failed zero-byte initial Akee download was removed. Python/pytest may also create ignored bytecode and test caches.
