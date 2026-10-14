**Verdict:** The high-end mixed-offender omission is confirmed and corrected in a live-case payload: +$2.209bn on the identified union, below the $5bn review bar. Uniform DOT and life-year mortality arms now share one definition and expose matching offence-level victim harms/counts for fear. Historical central outputs remain byte-identical. Victims plus fear, lineage boundary and the full pairing require the parent's consumer integration.

## Per-fix results

| Fix, $bn/year on identified union | Low | High | Rule and review bar |
|---|---:|---:|---|
| Previous victims, row-4 weights | 30.483111 | 31.873558 | historical restatement |
| Mixed groups at both ends | 30.483111 | 34.082564 | high's own custody multiplier applies to the mixed correction; +0 / +2.209006, below $5bn |
| DOT uniform mortality, mixed groups at both ends | 35.251012 | 39.413461 | mortality-only +4.767901 / +5.330897 against corrected legacy; high exceeds $5bn before the fear reconciliation |
| Life-years, common period mortality, age-40 base, 0% | 36.718427 | 41.054149 | mortality-only +6.235316 / +6.971585, both exceed $5bn before fear |
| Arrest-based footing beside the custody high | — | 42.500518 | legacy valuation; alternative proxy, not an identified causal high |

[CALCULATION: `mortality_arms.py` → `derived/mortality_arms.csv`; `../population_basis_2026_09_29/p7_victim_correction.py` → `derived/restated_victims_oct14.csv`, `victim_correction_oct14.json`.]

The published-weight mixed/custody legacy totals are 30.927388 / 34.579302. The original custody number is 32.338100. Its correction is larger than the low's because the custody ratio multiplies all incidents, including the newly attributed mixed groups. The historical low receipt is preserved exactly after reproducing it within 1e-6bn; the intermediate source and receipt round independently. No other restatement row is modified. [DATA: historical `arms.csv`, `../population_basis_2026_09_29/basis.csv`, `derived/restated_pairing.csv`.]

## Mortality source and assumptions

The setting is `vsl_standard`, with `legacy`, `dot_uniform`, `dot_life_years`. DOT uniform parses the unique 2024 row of the primary DOT table: $13.7m in 2024 dollars. The page was accessible through web open; curl returned HTTP 403. The exact returned table lines are archived and fingerprinted, not a model transcription. [SOURCE: https://www.transportation.gov/office-policy/transportation-policy/revised-departmental-guidance-on-valuation-of-a-statistical-life-in-economic-analysis; `inputs/dot_vsl_table_web.txt`, `inputs/pins.json`.]

Life-years use the primary NVSS workbook, Table 1 for the total US population, 2024, copied from the existing longevity lane and fingerprinted. Each death is valued at DOT VSL × expected remaining years / expected remaining years at age 40. The reference is 41.000209 years at 0%, or 23.255233 at 3%. Age 40, common population mortality and the discount choice are explicit calibration assumptions, not DOT life-year guidance. No lost earnings or legacy mortality QoL is added on top of either replacement mortality price. [SOURCE: `inputs/lt2024_Table01.xlsx`, title in cell A1; CALCULATION: `vsl_standard.py` → `derived/vsl_standard.json`; ASSUMPTION: calibration.]

Victim ages are parsed in chunks directly from the pinned primary SHR76_25a.csv for 2024 criminal homicide excluding justifiable killings, solved cases with a known Hispanic first offender, by the same victim-ethnicity groups as the homicide incidence producer. The four group counts reproduce the existing homicide input exactly. Ages are observed; 100+ uses the life table's open final interval. Six of 1,085 Hispanic-victim records and one of 160 Black-victim records lack valid ages; all 204 White and 21 Other records have ages. [SOURCE: `../homicide_cost_2026_09_18/_cache/SHR76_25a.csv`; DATA: `derived/mortality_age_profile.csv`.]

Transferring that conditional age distribution to unresolved/nonreporting cases within victim ethnicity remains an assumption. Missing ages alone bound published-weight mixed/custody life-year costs at 37.194261–37.291931 / 41.586170–41.695372. At 3%, recalibrating the same age-40 base at 3%, the central totals are 36.037103 / 40.292374. These are sensitivity ranges, not confidence intervals. They do not bound nonreporting or first-offender selection. [CALCULATION: `derived/mortality_arms.csv`; ASSUMPTION: mortality/selection transfer.]

The custody footing uses ACS institutional residence as an offending multiplier. It is an institutional-residence sensitivity, not observed ordinary-crime offending: ACS cannot distinguish ICE custody or noncorrectional institutions. Arrests also are charges, not convictions or proven incidents. [SOURCE: `research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md`, reporting rule; `victim_cost.py:institutional_ratio`.]

## Parent API and envelopes

Read `derived/mortality_detail.csv`: filter `footing`, `vsl_standard`, `real_discount_rate=0`, `missing_age_arm=central`. Footings are `equal`, `mixed`, `custody`, `arrest`, `envelope_low`, `envelope_high`, `envelope_low_unmixed`, `envelope_high_unmixed`. Rows are victim group × offence; `outside_victims`, `group_victimisations`, `hispanic_victimisations`, `unit_full`, `cost_full` are matched. The name `equal` preserves the historical Hispanic-equal-rate footing; every harm here is an absolute with/without outsider harm, not an equal-population subtraction. Fear must subtract that active unit harm on the same counts. Full joint totals belong to the parent.

Use the unmixed footings to isolate the fear-arm correction before adding the mixed-offender correction. Their native historical valuation pairing is `envelope_low_unmixed` at `legacy`, and `envelope_high_unmixed` at `dot_uniform`: the historical high envelope already uses DOT. Producer gates and regression tests reproduce those historical totals at their original four-decimal output precision and verify that changing only mixed attribution leaves homicide costs and every unit price unchanged. The existing `envelope_low` / `envelope_high` remain the mixed versions.

The two envelope footings retain the original stacked incidence choices and add the mixed correction. For the 2024-only high envelope, the pooled mixed correction's victim-row multiplier transfers to 2024 Hispanic/Other cells while preserving row totals [ASSUMPTION]; it is not remeasured from a new 2024 Select extract. At legacy prices the published-weight envelopes are 16.574741 / 41.357128; at DOT 18.827365 / 47.731168; at life-years 19.144620 / 49.683551. [CALCULATION: `derived/mortality_arms.csv`.]

Python API: `vsl_standard.mortality_value(standard, remaining_years=..., reference_years=...)`; `remaining_years(age, real_discount_rate=0)`; `reference_life_years(rate=0)`; `settings()`. Unknown standards and absent life-years fail closed. `dot_vsl()` and `life_table()` verify their own source fingerprints, so other consumers need not rely on an unchecked constant. A pollution consumer must supply its actual mortality age mix or an explicit remaining-year sensitivity: there is no default pollution age.

## Gates, uncertainty and reproduction

Positive controls reproduce the original legacy and DOT arms at their original 4-dp output precision, plus the native low-Miller/high-DOT envelopes. Exact NIBRS theta is recomputed through the existing primary-input producer (not taken from the rounded six-decimal CSV), with a gate against that CSV. Mixed attribution conserves each national victim-row incident total and leaves every cell nonnegative. Age-group counts match primary homicide inputs; victim costs close to counts × units within $1e-6; original central outputs and historical restatement remain untouched. Eight tests pass, including mortality/earnings non-overlap, high's multiplier, missing-age bounds, fail-closed valuation settings and the native-envelope isolation checks.

`nonfatal_conditional_se_bn` is the existing understated NCVS generalized-variance delta-method SE, with cells treated independent, mixed correction and other inputs fixed: 2.038132bn at mixed, 2.278795bn at custody on published weights. It is not a replicate SE. Arrest and single-year high-envelope covariance is unavailable here and is explicitly blank with a scope note. Neither mortality calibration, mixed-fraction uncertainty, rotating-panel covariance nor ACS-proxy uncertainty is covered. [DATA: NCVS `matrix_pooled_2022_2024.csv`; CALCULATION: `mortality_arms.py`.]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/crime_victim_cost_2026_09_23/mortality_arms.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/population_basis_2026_09_29/p7_victim_correction.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/crime_victim_cost_2026_09_23 'uv run --no-project python3 {lane}/mortality_arms.py' 'uv run --no-project python3 {lane}/vsl_standard.py' 'uv run --no-project python3 -m pytest {lane}/test_mortality_arms.py -q'
uv run --no-project python3 scripts/rerun_lane.py --allow-unrun reeval.py infra/immigration-fiscal/population_basis_2026_09_29 'uv run --no-project python3 {lane}/p7_victim_correction.py' 'uv run --no-project python3 -m pytest {lane}/test_p7_victim_correction.py -q'
```

Log: 2026-10-14 21:36 JST (`date`): six tests pass; rerun crime IDENTICAL 38/38, population IDENTICAL 27/27, exits 0. No `--allow-unrun`; all new scripts are executed or exercised by the pytest command. Warm producer 5.623s, peak RSS 1,719,615,488 bytes; earlier cold run 12.430s, 1,311,424,512 bytes. Population producer 0.014s, 100,696,064 bytes. Timing uses `time.perf_counter` and memory uses `resource.getrusage`; no ps/sysctl/time-l. No git mutations.

Log: 2026-10-14 21:43 JST (`date`), parent follow-up: add native unmixed envelopes so the consumer isolates fear-arm and mixed-offender changes. The unmixed low at legacy is 15.409932bn and unmixed high at DOT is 45.342392bn on published weights. Eight tests pass. Both new producers finish successfully; reruns crime IDENTICAL 38/38 and population IDENTICAL 27/27, exits 0. The population rerun now explicitly allows unrun `reeval.py` because that concurrently edited social-response script is owned by the parent; it is not claimed validated here. Latest mortality producer 5.580s, RSS 1,882,243,072 bytes; population producer 0.013s, 100,483,072 bytes. Follow-up edits: `mortality_arms.py`, `test_mortality_arms.py`, `derived/mortality_arms.csv`, `derived/mortality_detail.csv`, this result, and the diagnostic log; original outputs and all peer edits preserved.

## Changed paths

`crime_victim_cost_2026_09_23/`: `p7-victim-result.md`, `mortality_arms.py`, `vsl_standard.py`, `test_mortality_arms.py`, `inputs/dot_vsl_table_web.txt`, `inputs/lt2024_Table01.xlsx`, `inputs/pins.json`, `derived/mortality_age_profile.csv`, `derived/mortality_arms.csv`, `derived/mortality_detail.csv`, `derived/vsl_standard.json`.

`population_basis_2026_09_29/`: `p7_victim_correction.py`, `test_p7_victim_correction.py`, `derived/restated_victims_oct14.csv`, `derived/victim_correction_oct14.json`.

Diagnostic output outside the lanes: `/private/tmp/p7-victim-arms.log`. Generated interpreter/pytest caches are ignored runtime artifacts.

Covered: brief items 3 and 4, plus exact per-offence/envelope API requested for parent fear integration. Skipped by ownership: fear/security producer, fiscal-plus-social total, descendant boundary, crime geography, state custody reallocation, ICE bound. The parent owns their integration and review.
