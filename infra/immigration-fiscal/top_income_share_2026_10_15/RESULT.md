**Verdict:** Seven ASEC years do not establish that the union's $1M+ federal income-tax share is lower than the current key. The pooled raw share is 3.466%, based on 77 positive-tax carrier record-years; its sampling SE is 0.466 percentage points under independent years, with an upper covariance bound of 1.206 points. A proposed pooled, non-increasing reading above $200k moves the federal cost by +0.254bn at each v8 end; adding a California-only state sensitivity moves it by +1.842bn. SCF checks point lower but measure different objects and have small Hispanic tail cells. These are sensitivities beside the adopted case, not an adopted replacement or a verified true top share. [CALCULATION: `derived/cps_bins.csv`, `federal_arms.json`, `arms_v8.csv`, `outside_bridge.csv`]

## Object, frame and fixed quantities

The fiscal perspective is the case's cost to other residents. A positive cost change means fewer receipts assigned to the union. The federal object is FEDTAX_BC (tax after nonrefundable, before refundable credits) carried on CPS person records under the personal allocation; these are simulated tax carriers, not independently observed IRS returns. The union is `external_benchmarks_2026_09_24/frame.py::masks`, exactly the historical key used by v8. It is Mexico-born immigrants, US-born children of a Mexico-born parent, and Mexican-origin US-born people with two US-born parents, on the civilian universe. V8's additional reporting-rule members, nonreporting descendants and missed people are separate corrections; their carried dollars stay fixed in this exercise. [SOURCE: `tax_key_heldout_2026_09_28/keys.py`; `pool_cps.py`; case payload]

The original key uses published CPS weights, then the case's tax stack carries the row-4/status correction. Applying row4 before that rake would apply the correction twice. A supplementary row4 baseline independently gates the account's 39,712,493.33 people; published 2025 union weights sum to 40.90M. Earlier surveys keep their own populations rather than being forced to 2024's count. The final sensitivity uses the case's own row4/status stack for each fill-in method. [DATA: `derived/cps_sources.csv`, `cps_metadata.json`; CALCULATION: `pool_cps.py::row4_weights`, `price_v8.cjs`]

ASEC 2019–2025 measure income years 2018–2024. AGI **and tax dollars** in the historical pool use BLS annual-average CPI-U, CUUR0000SA0/M13: factor = CPI(2023)/CPI(income year). This keeps the IRS TY2023 dollar thresholds constant and pools real tax dollars, with equal survey-year exposure and each year's own weights/population. It is a historical pooled estimate, not an identified 2024 estimate. The exact-current control retains nominal 2025 AGI to reproduce the adopted key. Source files, hashes, CPI values and factors are in `cps_sources.csv` and `cps_metadata.json`. [SOURCE: archived primary Census files and BLS response linked there]

National NIPA federal and state totals stay fixed. So do IRS TY2023 AGI margins, CBO 2022 income-group margins, below-$200k shares, case stack/status factors, all other spending/receipts, production, and the added-person/white-end, mixed-unit and coverage corrections. The result is an exact **fixed-other-corrections** sensitivity at v8's personal specifications 16/11, set and cash separately. It is not a full re-estimation of every descendant and stayer under a new person-level tax model. [CALCULATION: `price_v8.cjs`, `derived/v8_gates.json`]

## CPS measurements and replicate uncertainty

Each cell is share ± one SDR SE in percentage points, followed by the number of union positive-FEDTAX_BC carriers. Years label the ASEC survey. These are raw tax-dollar shares before CBO/IRS raking; each year's full 19-bin table is in `derived/cps_bins.csv`.

| ASEC | $200k–500k | $500k–1M | $1M+ |
|---|---:|---:|---:|
| 2019 | 2.755% ± 0.228pp (218) | 3.055% ± 0.789pp (20) | 5.102% ± 1.476pp (16) |
| 2020 | 2.977% ± 0.238pp (239) | 2.872% ± 0.756pp (26) | 0.958% ± 0.625pp (3) |
| 2021 | 3.334% ± 0.245pp (264) | 2.773% ± 0.784pp (17) | 2.905% ± 1.154pp (8) |
| 2022 | 3.185% ± 0.234pp (237) | 2.717% ± 0.620pp (23) | 3.640% ± 1.216pp (11) |
| 2023 | 3.323% ± 0.262pp (224) | 3.005% ± 0.799pp (18) | 4.170% ± 1.453pp (12) |
| 2024 | 3.775% ± 0.296pp (261) | 3.629% ± 0.984pp (23) | 3.893% ± 1.342pp (12) |
| 2025 | 3.789% ± 0.251pp (272) | 2.394% ± 0.577pp (18) | 3.686% ± 1.156pp (15) |
| Pooled | 3.323% ± 0.096pp (1715) | 2.924% ± 0.292pp (145) | 3.466% ± 0.466pp (77) |

[CALCULATION: `pool_cps.py`; DATA: `derived/cps_bins.csv`.]

Annual SEs use all 160 Census successive-difference replicates, sqrt(4/160 × sum((replicate estimate − main estimate)²)). Pooled SEs perturb one year's replicate totals at a time in the pooled numerator/denominator. The independent-year variance sums those annual perturbation variances. Adjacent CPS samples overlap; joint cross-year covariance is not identified by matching replicate column numbers. The sum of the component SEs is also supplied as a maximum-positive-covariance bound. Counts are carrier **record-years**, with potential repeat households, not 77 independent tail families. Neither SE includes disclosure edits, tax simulation error, CPI/temporal transport or the monotonicity assumption. [CALCULATION: `pool_cps.py::ratio_summary`; SOURCE: Census replicate usage documentation; `cps-note.md`]

The complete pooled IRS-bin table follows. SE columns are expressed as percentage points; missing-tax cells are explicitly undefined.

| Real-2023 AGI bin | Union share | SE, independent years | SE, covariance bound | Union carriers |
|---|---:|---:|---:|---:|
| No adjusted gross income (includes deficits) | 30.742% | 36.012pp | 50.224pp | 1 |
| $1 under $5,000 | 10.126% | 2.273pp | 5.325pp | 42 |
| $5,000 under $10,000 | 9.713% | 2.223pp | 5.389pp | 40 |
| $10,000 under $15,000 | 15.084% | 1.920pp | 4.824pp | 335 |
| $15,000 under $20,000 | 15.781% | 0.421pp | 1.099pp | 2181 |
| $20,000 under $25,000 | 15.563% | 0.359pp | 0.945pp | 2644 |
| $25,000 under $30,000 | 15.856% | 0.355pp | 0.930pp | 2658 |
| $30,000 under $40,000 | 14.849% | 0.238pp | 0.624pp | 5691 |
| $40,000 under $50,000 | 13.077% | 0.229pp | 0.604pp | 4598 |
| $50,000 under $75,000 | 10.363% | 0.152pp | 0.398pp | 8110 |
| $75,000 under $100,000 | 7.755% | 0.149pp | 0.391pp | 4594 |
| $100,000 under $200,000 | 5.393% | 0.083pp | 0.220pp | 6457 |
| $200,000 under $500,000 | 3.323% | 0.096pp | 0.251pp | 1715 |
| $500,000 under $1,000,000 | 2.924% | 0.292pp | 0.758pp | 145 |
| $1,000,000 under $1,500,000 | 4.001% | 0.538pp | 1.381pp | 72 |
| $1,500,000 under $2,000,000 | 0.000% | 0.000pp | 0.000pp | 0 |
| $2,000,000 under $5,000,000 | 3.712% | 1.827pp | 4.090pp | 5 |
| $5,000,000 under $10,000,000 | — | — | — | 0 |
| $10,000,000 or more | — | — | — | 0 |

[DATA: `derived/cps_bins.csv`; all 19 bins remain separate in measurement, while pricing pools $1M+ for public-use support.]

The nominal 2025 support check reproduces 15 union positive-tax carriers at $1M+, none at $1.5M+, and 33 all-origin carriers at $1.5M+. There are no carriers of any origin at $5M+. Census describes tax-model fields and confidentiality edits: rank-proximity swapping can retain marginal income values while changing their association with a person's ethnicity; upper-income edits and component top-codes also affect AGI. More pooled record-years do not observe the true ethnic tax split in the unsampled multimillion-dollar tail. [DATA: `derived/cps_tail_support.csv`; SOURCE: Census disclosure documentation in `cps-note.md`]

## Proposed rule and federal reconciliation

Use pooled real-2023 shares inside CBO-group × AGI cells, projected onto the case's **fixed** IRS/CBO cell masses; above $200k fit a non-increasing sequence by weighted least squares, with IRS bin masses as weights. This is a proposed regularization assumption, not an empirically established monotonic law. The pooled unconstrained upper shares on those case masses are 3.296%, 2.997%, 3.572%; the central fitted shares are 3.366%, 3.366%, 3.366%. The fit preserves the weighted upper-tail mean, so constrained and unconstrained aggregate costs coincide by construction. [CALCULATION: `federal_arms.py`; `derived/federal_arms.json`]

The final jointly raked current $500k–1M share is 2.561%; the heldout lane's **before-joint-rake** table gives 2.309%. Carrying the former to $1M+ changes federal cost by +6.164bn. Carrying the latter reproduces the brief's approximately $7.8bn calculation: +7.819bn. Both readings are shown, rather than treating the 2.3% figure as the final key's within-bin share. The 1.5% imposed-share federal arm reproduces +13.129bn. [DATA: heldout `translation_bins.csv`; CALCULATION: `federal_arms.py`, `price_v8.cjs`]

## Outside checks, with their objects named

SCF measures **primary economic-unit families' previous-calendar-year gross income**, including pension withdrawals, with the reference person's Hispanic status. It does not identify Mexican origin, parent birthplace, IRS AGI or federal/state income-tax liabilities. Both years are reconstructed from nominal raw files using the Fed's INCOME/MCONV definitions, then converted from income years 2018/2021 into 2023 CPI-U dollars. This avoids silently combining summary files with different dollar bases. Five implicates are averaged; the family count deduplicates implicates. Reconstructed 2022 gross income agrees with the official local summary up to its common price scale, and weights match its X42001/5 convention. [SOURCE: Federal Reserve raw files, official bulletin macro and archived pages in `derived/outside_sources.csv`; CALCULATION: `outside_checks.py`; `outside-note.md`]

At real-2023 $1M+, the table bridges SCF Hispanic composition to the CPS union/Hispanic **tax-carrier** split. The pooled tax-dollar bridge is 44.407%. Multiplying a gross-income share by that tax-dollar ratio additionally assumes Hispanic/non-Hispanic effective taxation is comparable at those incomes, the family/person objects transport, and CPS captures the within-Hispanic origin split. The union can include non-Hispanic members, so the bridge is not literally a Hispanic subset fraction. These products are conditional proxies, never observed union tax shares.

| SCF | Hispanic family share | Hispanic gross-income share | Unique Hispanic families | Conditional union family proxy | Conditional union tax proxy |
|---|---:|---:|---:|---:|---:|
| 2019 | 2.948% | 3.063% | 14 | 1.296% | 1.360% |
| 2022 | 1.704% | 2.087% | 15 | 0.749% | 0.927% |

[CALCULATION: `derived/outside_bridge.csv`; measured composition is in `outside_scf.csv`. SCF sampling SEs are not estimated: no bootstrap weights are used; implicate variation alone is not a sampling SE.]

Akee, Jones and Porter (2019), *Demography* 56(3):999–1021, [doi:10.1007/s13524-019-00773-7](https://doi.org/10.1007/s13524-019-00773-7), is the linked IRS/Census study of income inequality, mobility and turnover at the top by race and ethnicity. Publisher metadata establishes the identity, but the final published numerical tables could not be opened. **[UNVERIFIED] Published-table numerical checks are withheld.** A UCLA DOI landing page serves an August-2017 NBER working-paper attachment, which is not silently substituted for the 2019 final tables. No number from that paper enters any calculation. ACS PUMS is skipped: person income/top-code composition is a further different object and offers no direct AGI or tax-liability split; SCF already supplies the requested independent wealthy-sample check. See `outside-note.md` for access evidence and omitted objects.

Disconfirmation runs both ways: pooling leaves the federal top share close to current and raises California's top share, contradicting a necessary downward correction; SCF's conditional proxies are lower, contradicting a claim that CPS has validated the true multimillion-dollar share. None establishes the true tax share. [DATA: the displayed CPS/SCF tables, `derived/state_arms.json`; INFERENCE: identification limit]

## State correction and v8 arms

The state line is positive STATETAX_A. Its current national key is 5.004%. The administrative shape uses California FTB's TY2023 preliminary **resident-return total liability** table, Exhibit A-10, PDF page 15, from [DOF Spring 2025](https://publish.data.ca.gov/dataset/1555a2c4-740a-4b1c-adf1-1ab7721e90b3/resource/ee16e82e-c2cf-4900-b6c6-121ded321241/download/dof_spring_2025_odp.pdf). California's share of national CPS state-tax dollars, 18.595%, stays fixed and every other state stays raw. Federal AGI proxies California AGI; resident-return liability proxies California's CPS tax distribution; TY2023 shape transports to income-year2024. This is a covered-state sensitivity, not a nationwide measured correction. IRS federal tax and capped SALT deductions are not used as actual state tax liabilities. [SOURCE: linked FTB exhibit; DATA: `derived/state_ftb_extract.csv`; `state-note.md`]

The CA-administrative control alone moves state cost by +1.755bn. Relative to that control, pooling/regularization moves state cost by -0.166bn: the top-share change offsets part of the administrative-shape change. California's current $1M+ share is 4.370%, its pooled share 6.531%; only 2 baseline and 22 pooled union state-liability carriers support them. The federal and state shares are estimated separately. [CALCULATION: `state_correction.py`; `derived/state_arms.json`; `arms_v8.csv`]

All dollar figures below are $bn. Delta columns apply equally to **each end in both set and cash**; the final columns explicitly show low/high totals for each. `carry_500k` uses each line's current $500k–1M share; the pre-joint-rake comparison changes federal alone. `pooled_top_only` replaces only $1M+; the two pooled full arms replace $200k+ shares. Every non-current state arm includes the CA administrative shape; `current_CA_admin` isolates it.

| Arm | Federal Δcost | CA-state Δcost | Combined Δcost | Set low / high | Cash low / high |
|---|---:|---:|---:|---:|---:|
| current | +0.000 | +0.000 | +0.000 | 365.792 / 455.982 | 281.753 / 371.942 |
| carry_500k | +6.164 | +0.854 | +7.018 | 372.810 / 463.000 | 288.771 / 378.961 |
| carry_500k_pre_joint_rake | +7.819 | +0.000 | +7.819 | 373.611 / 463.801 | 289.571 / 379.761 |
| fixed_1_5pct | +13.129 | +2.608 | +15.737 | 381.529 / 471.719 | 297.489 / 387.679 |
| pooled_top_only | -0.479 | +1.112 | +0.633 | 366.425 / 456.615 | 282.386 / 372.575 |
| pooled_unconstrained | +0.254 | +1.588 | +1.842 | 367.634 / 457.824 | 283.595 / 373.784 |
| pooled_monotone_central | +0.254 | +1.588 | +1.842 | 367.634 / 457.824 | 283.595 / 373.784 |
| current_CA_admin | +0.000 | +1.755 | +1.755 | 367.546 / 457.736 | 283.507 / 373.697 |

[CALCULATION: `price_v8.cjs`; DATA: `derived/arms_v8.csv`, full arm × end × set/cash rows; `arms_v8_by_method.csv`, method factors and receipt deltas.]

`price_v8.cjs` rebuilds each fill-in method with v8's package, applies its exact row4/status stack factor × NIPA national line × pre-stack share change, expands the edits to the case's receipt incidence rules, then calls `evaluateFull` at declared personal ends 16/11. It separately matches the authoritative full-precision set and cash baselines and checks receipt/total-cost closure and unchanged national totals. Shared allocation cells are not changed; there is no claim to a shared-allocation variant or new global extrema. The current arm moves nothing. [CALCULATION: `derived/v8_gates.json`; source hashes recorded there]

## Limits and interpretation

The current top share is weakly supported, but the seven-year evidence does not identify a large downward federal correction. The lower SCF products make 1.5% a useful sensitivity, not a calibrated estimate. A national state rekey needs more states' actual PIT distributions and a suitable state/AGI bridge. This lane supplies a proposed rule and quantified arms; the parent decides whether any rule enters a future case. The displayed replicate SEs apply to raw bin ratios, not to the CBO-raked proposed shares or the final dollar changes; pricing uncertainty would require carrying replicate cell shares through the transformation. [INFERENCE; FRAMING-SENSITIVE: choice of regularization]

Tax rules, composition, public-use edits and survey participation vary across pooled years, including the pandemic. Replicate SEs describe survey-weight uncertainty conditional on those edits, not those biases. Added descendants and nonmembers in mixed units remain at their source amounts; fully propagating a new micro-level tax distribution would require a declared rule for them and a new case build. Source input hashes protect the measured route, and every empirical number here is linked to its generated table. LLM framing can favor one direction; the conflicting CPS and SCF readings and both upward/downward arms are exposed to make that choice inspectable.

## Reproduction and checks

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/top_income_share_2026_10_15/run_all.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/top_income_share_2026_10_15 "uv run --no-project python3 {lane}/run_all.py"
```

The wrapper runs every generator plus focused tests for replicate pooling, source support/frame gates, SCF income reconstruction and implicates, administrative tax extraction, both raking margins, isotonic accounting and live-v8 pricing closure. It never writes Git metadata or other lanes. New downloads live in ignored `_cache/`; reused sources remain read-only. Physical-memory checks use Python `resource.getrusage`, times use `time.perf_counter`, and timestamps invoke `date`. Rerun-dependent telemetry is kept in ignored `_cache/run_log.json` so reproducible outputs stay deterministic. See `failure-catalog.md` for the covered failure classes.

An independent repo-access review recomputed the entire IRS/CBO joint matrix, baseline and arm dot products, traced the original tax-edit route and checked the output accounting. It found no material defect in that reviewed scope. State and outside checks were inspected separately by the parent; the review does not assert independent coverage of those implementations. Its coverage and interpretation limits are in `review-note.md`.

## Run log

Recorded complete build (all exits 0); timestamps are UTC from `date`. Memory is the cumulative maximum of child peak RSS, a conservative upper bound for each individual child, measured by Python `resource.getrusage`.

| Start UTC | Step | Seconds | Child peak upper bound, GiB |
|---|---|---:|---:|
| 2026-10-15 02:05:54 UTC | pool_cps.py | 122.048 | 0.567 |
| 2026-10-15 02:07:56 UTC | outside_checks.py | 6.292 | 0.567 |
| 2026-10-15 02:08:02 UTC | federal_arms.py | 0.577 | 0.567 |
| 2026-10-15 02:08:03 UTC | state_correction.py | 0.660 | 0.567 |
| 2026-10-15 02:08:03 UTC | price_v8.cjs | 6.096 | 0.567 |
| 2026-10-15 02:08:10 UTC | 23 tests | 3.769 | 0.567 |
| 2026-10-15 02:08:13 UTC | render_result.py | 0.039 | 0.567 |

