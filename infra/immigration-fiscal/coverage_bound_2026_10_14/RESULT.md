**Verdict:** Replace the earlier one-sided label with a **coverage sensitivity**. The central construction adds **$11.1bn / $14.8bn**, giving **$350.6–438.5bn** at personal specifications 16 / 11. Its construction envelope is **-15.9 to +22.6bn** at the low end and **-16.2 to +26.4bn** at the high end, not a confidence interval. Recommend **no coverage addition to the next main case's central yet**; keep this construction and range beside it. DA/PES choices alone move the result over the $5bn bar. [CALCULATION: `coverage_bound.py` → `derived/coverage_bound.json`] [INFERENCE: recommendation]

## Frame and central rule

**Pricing epoch:** the original v7 generation split at commit `1a02fbbb`, archived as `inputs/generation_results_original.csv` and byte-verified against the initial source pin, with the matching original household pricing cache. During the final reproduction a concurrent P7 worker changed generation outputs while that lane's source pins and derived summary were still being rebuilt. The stale-input guard stopped the run. This calculation deliberately freezes the original split rather than adopting an unfinished revision. Its dependency manifest continues to verify every source actually used; the concurrent generation/credit/state routing changes are not included. Reprice coverage after those changes are validated before transferring this sensitivity into a revised case. [DATA: original committed CSV, pinned household inputs] [LIMITATION: version scope]

Income-year 2024 annual complete-account resource cost to other US residents, using v7's accrual and imputed public-capital return. This is a fixed-price coverage sensitivity, with no reference group and no debt/cash interpretation. The national budgets, national key masses and case response factors stay fixed in the central. The model inputs below are measured; Hispanic-to-Mexican-origin and household-to-resident transfers, cohort timing, missed members' prices, and the G3+ placement are assumptions. This is LLM-assisted work on a politically charged question; source wording and tables were independently checked, and signed corrections in both directions are retained. [DATA: frozen v7 `summary.json`; `pricing_audit.json`] [ASSUMPTION]

Central rates: DA Table 1C middle residual relative to the Vintage 2024 base for those aged 0–4 in April 2020, then the 2020 PES Hispanic age-sex rates for ages 5+, divided by the corresponding sex-specific base/Census ratio. DA low/middle/high through age 29 are separate constructions. No DA increment is stacked on a PES increment for the same person. [CALCULATION: `source_tables.py`, `inputs/controls/compare_base.py`, `coverage_bound.py:rate_at`]

## 1. What the controls did

- **2025 ASEC:** the exact original-weight source is Census SEHSD-WP2025-13, PDF p.2: “weighted to the March 2025 value from the Vintage 2024 population estimates.” The [BLS January 2025 notice](https://www.bls.gov/cps/notices/2025/population-controls.htm) confirms the basic-CPS update; its pinned file is explicitly a web-tool extraction after original-host HTTP 403. [SOURCE: https://www2.census.gov/library/working-papers/2025/demo/sehsd-wp2025-13.pdf, PDF pp.1–2; `inputs/controls/`]
- **2024 ACS 1-year:** “The 2024 1-year ACS was controlled to the Vintage 2024 housing and population estimates.” [SOURCE: https://www.census.gov/content/dam/Census/programs-surveys/acs/tech-doc/user-notes/2024-acs-1-year-research-note.pdf, PDF p.1]
- **Origin versus age margins:** “age and sex detail is drawn from 2020 DA” while “Hispanic origin detail comes from the 2020 Census.” The blended design rakes V2020 detail to DA national age-sex cells and retains protected Census Hispanic resident margins. [SOURCE: https://www2.census.gov/programs-surveys/popest/technical-documentation/methodology/2020-2024/methods-statement-v2024.pdf, PDF pp.3–4]
- **No new US base method in V2024:** “The Vintage 2024 blended base for the United States did not feature changes relative to Vintage 2023.” The release's NIM, vital-statistics and Puerto Rico changes are distinct. [SOURCE: https://www2.census.gov/programs-surveys/popest/technical-documentation/methodology/2020-2024/2024-est-relnotes.pdf, PDF pp.1–2]
- **PAA paper:** V2023 added “Hispanic or Latino resident population totals from the 2020 Census” (PDF p.13); the PES design was “deemed inconducive to valid, reliable adjustments to the estimates base” (p.8). But DA blending changed children's age cells. [SOURCE: https://www.census.gov/content/dam/Census/newsroom/press-kits/2024/paa/paa2024-paper-modernizing-popestimates-base.pdf]

**Disconfirmation of an entirely unabsorbed age-specific error:** Census's [June 2023 account](https://www.census.gov/library/stories/2023/06/blended-base-methodology.html) explicitly documents increased Hispanic child counts through DA age blending; its [December 2023 recommendation](https://www.census.gov/newsroom/blogs/random-samplings/2023/12/recommendations-2020-pes-coverage-results-in-vintage-2023-pop-estimates.html) explains that this indirectly mitigates young-child undercounts. The national V2024 base below tests the later vintage directly. Near-unchanged Hispanic all-age margins coexist with sizable redistribution over age. Thus both “the entire age-specific omission remains” and “absorption cannot be checked” fail. [SOURCE: pinned primary documents] [CALCULATION: base comparison]

| April 2020 Hispanic resident age | Census DHC | V2024 base | Base change | DA middle residual to base |
|---|---:|---:|---:|---:|
| 0–4 | 4,635,698 | 5,044,695 | +8.823% | +0.541% |
| 5–9 | 5,135,533 | 5,236,266 | +1.961% | +1.866% |
| 10–17 | 8,986,021 | 8,841,248 | -1.611% | +3.865% |
| 18–29 | 12,324,769 | 11,850,626 | -3.847% | +0.003% |
| 30–49 | 17,244,729 | 17,566,503 | +1.866% | not available |
| 50–100 | 13,753,294 | 13,535,823 | -1.581% | not available |
| 0–100 | 62,080,044 | 62,075,161 | -0.008% | not available |

[DATA: NC-EST2024 R-file `YEAR=2020, MONTH=4.2`, `H_MALE+H_FEMALE`; 2020 DHC P12H; DA Table 1C in thousands] [CALCULATION: `inputs/controls/compare_base.py` → both-sex and sex-specific tables; exact Census/base sex closures] The fiscal calculation uses sex-specific cells, not this both-sex display. DA original-series rounded age sums are retained; they can differ from rounded printed totals.

## 2. Parsed undercount rates, including standard errors

The reviewer's **7.34% is PES, not DA**: Table C of the 2020 PES cross-classification report, PDF p.9 (printed p.10). The young Hispanic row and its SE are parsed directly below. DA Table 1C instead supplies low/middle/high count series; `derived/da_coverage.csv` shows their net error against DHC and their remaining difference from the blended base. DA's range is methodological, not an SE or CI. [SOURCE: https://www2.census.gov/programs-surveys/decennial/coverage-measurement/pes/net-coverage-error-and-components-of-coverage-by-race-hispanic-origin.pdf; https://www2.census.gov/programs-surveys/popest/tables/2020/2020-demographic-analysis-estimates/table-1c.xlsx]

| PES group / April 2020 age-sex | Net coverage error, % | SE, percentage points |
|---|---:|---:|
| hispanic / all | -4.99 | 0.53 |
| hispanic / 0 to 4 | -7.34 | 1.33 |
| hispanic / 5 to 9 | -3.96 | 1.10 |
| hispanic / 10 to 17 | -4.81 | 0.92 |
| hispanic / 18 to 29 males | -7.84 | 1.25 |
| hispanic / 18 to 29 females | -8.07 | 1.11 |
| hispanic / 30 to 49 males | -9.32 | 0.73 |
| hispanic / 30 to 49 females | -4.10 | 0.76 |
| hispanic / 50 and over males | +0.44 | 0.82 |
| hispanic / 50 and over females | +0.59 | 0.73 |
| nonhispanic_white / all | +1.64 | 0.21 |
| total / all | -0.24 | 0.25 |

[CALCULATION: `source_tables.py` → `coverage_rates.csv`; national-report Table 4 origin marginal positive control] Negative NCE means an undercount. The national PES total is statistically consistent with zero, not measured as exactly zero. Opposing subgroup errors largely offset. PES excludes group quarters and remote Alaska; DA and the R-file are resident populations. The rate transfer therefore remains an assumption. National age-only DA Table 2 is pinned for context; it is not substituted for the Hispanic Table 1C series.

The PES residual factor is `1 / ((1 + signed_NCE) × base/Census) − 1`; the DA residual is `DA/base − 1`. This subtracts existing base adjustment multiplicatively and retains net overcounts. The two are alternative doses, never additive corrections. [CALCULATION]

## 3. Eligible cohorts and populations

Only residents alive on April 1, 2020 can inherit that Census enumeration error. Later births take zero, as requested; this does not assert perfect vital-record origin classification. March 2025 public-use ages do not expose birthdays: the central uses uniform birthdays at the case's March 15 frame date (17/365 at the older April-2020 age); the two endpoints are arms. The public-use arrival variable combines 2020–21 (code 27): the central assigns 3/24 to arrivals before April 2020 under uniform arrival months, with none/all arms. Code 28 is post-2020 and takes zero centrally. Earlier G1 residents are included: audit row 4's ACS rake shares the Vintage 2024 controls and does not repair their Census error. [SOURCE: Census ASEC 2025 public-use dictionary, `PEINUSYR`, `PRDTHSP`, `A_AGE`, `A_SEX`; `world_ledger_2026_09_27/population_basis.py`] [ASSUMPTION: within-band cohort timing, carry-forward among survivors]

The identified union's non-Hispanic-reporting members take zero centrally, even where parental nativity identifies them. Identified G3+ report Hispanic origin. As specified by this brief, the added descendants are assigned to non-Hispanic controls: zero central, an NH-white net-overcount arm. Their Hispanic-control assignment is a model premise; no person-level link to these latent descendants is observed. Survival/emigration of missed 2020 residents is not separately estimated. [DATA: case counts and CPS origin fields] [ASSUMPTION]

| Component | Current priced population, millions | Hispanic reporting, millions | Central net people added, millions | Low coverage, bn | High coverage, bn |
|---|---:|---:|---:|---:|---:|
| G1 | 11.036701 | 10.883768 | 0.446105 | 1.936701 | 2.787535 |
| G2 | 14.333218 | 13.923881 | 0.824191 | 5.441409 | 7.013719 |
| G3plus | 14.342575 | 14.342575 | 0.667195 | 3.715316 | 5.029170 |
| added | 3.039720 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

[CALCULATION: case consumer price/weight projection → `age_prices.csv`; `coverage_bound.json` populations/parts] The correction is identical on the identified union and lineage centrally because the added people take zero. The two underlying accounts differ by their added people's cost; they must not be called the same account.

## 4. Price by age, at the case's own ends

`export_pricing.py` reuses the pinned `within_group_distribution_2026_09_29/households.py` **actual piece construction**, cut at a uniquely asserted AST boundary without editing upstream code. It preserves and checks all accumulated upstream gates. Each piece uses its existing vector and generation amount; flat pension accrual is on the case's own tax keys. The unassigned lane constants receive an explicit per-head allocation inside their generation. All generation totals and both case ends close in every replicate at 1e-6bn. Five-year March-2025 age prices and per-member costs are inspectable in `derived/age_prices.csv`. This uses the main-case account, not the generation ledger's white-reference balances. [DATA: consumer construction, `pricing_audit.json`, `age_prices.csv`] [ASSUMPTION: residual per-head placement]

The household route blends added and identified G3+ prices. Split its weights by the case's own measured age placement, then calibrate each net profile per head to the frozen **exact added cost** and combined G3+ total. This is an age/sex distribution assumption, not a recovered observed added-person profile. The opposite calibration amounts conserve the case's combined total, and the added totals independently close to `lineage_addition.json`. The source's alternate ancestry-route generation attribution differs slightly; this lane retains the existing generation-account/household convention for its positive control and does not mix the attributions. [CALCULATION: `export_pricing.py`] [ASSUMPTION]

## 5. National denominators

Central national budgets and key masses stay fixed. The PES national near-zero error supports an offsetting-error reading but does not identify every fiscal key's net error. The arm adds positive omissions to national key masses **without removing overcounts**. `national_keys.py` follows each actual declared driver, including pension receipt composites, benefit-tax offsets, routes, roads, production cells and public-capital parents, and requires its generation restriction to reproduce the priced vector at 1e-12 relative. The union-only tenant driver uses the principal national `states.csv` sum of `all_rent`, not its group-only mass. All nonzero pieces are covered; no generic population fallback is permitted. [DATA: actual consumer declarations, `denominator-evidence.md`, `denominators.csv`] [ASSUMPTION: fixed composite coefficients and responses]

This is the denominator arm of the exported price construction, **not a full engine rerun** of group-size elasticities or production general equilibrium. Its changes versus fixed masses and $5bn classification are in the next table. The income-tax/benefit split, parent keys and capital parents remain distinct; national spending and receipt budget inputs are unchanged. [CALCULATION: `coverage_bound.py:denominator_arm`]

## 6. Range and each construction's change from central

All numbers are bn per year, personal specs 16 / 11; each row holds the other central choices fixed except the explicitly labeled joint legacy construction. CPS successive-difference replicate SE is conditional on the rate transfer and fixed case line totals. The coherent PES ±1-SE rows are scenarios, not a confidence interval for the fiscal total: PES cross-cell covariance is unavailable. DA range, age-pricing choice and PES sampling uncertainty stay distinct; the envelope is a sensitivity range, not a guarantee.

| Construction | Low increment | High increment | Change from central, low / high | At least $5bn change? low / high |
|---|---:|---:|---:|---:|
| Central: DA middle 0–4; PES 5+, each residual to the blended base | 11.093426 | 14.830424 | +0.000000 / +0.000000 | no / no |
| PES also for ages 0–4, residual to base | 9.988392 | 13.661255 | -1.105034 / -1.169169 | no / no |
| DA low series for all supported ages 0–29; PES older | -15.861445 | -16.219566 | -26.954871 / -31.049990 | yes / yes |
| DA middle for ages 0–29; PES older | 5.957325 | 7.782186 | -5.136101 / -7.048237 | yes / yes |
| DA high series for ages 0–29; PES older | 22.644616 | 26.390116 | +11.551190 / +11.559692 | yes / yes |
| PES age-sex NCE minus 1 SE, coherent shift | 13.399476 | 17.808942 | +2.306050 / +2.978519 | no / no |
| PES age-sex NCE plus 1 SE, coherent shift | 8.835591 | 11.913265 | -2.257835 / -2.917159 | no / no |
| Same central doses, generation-average prices | 15.992086 | 19.782590 | +4.898660 / +4.952167 | no / no |
| All-age PES rate, actual age prices | 15.156027 | 18.922896 | +4.062600 / +4.092473 | no / no |
| All-age rate × generation-average prices (joint legacy construction) | 14.669663 | 18.263137 | +3.576237 / +3.432713 | no / no |
| Post-April-2020 G1 arrivals also take the Hispanic rate | 11.340178 | 15.263597 | +0.246752 / +0.433173 | no / no |
| No 2020–21 arrival-band members present before April 2020 | 11.068911 | 14.796506 | -0.024515 / -0.033917 | no / no |
| All 2020–21 arrival-band members present before April 2020 | 11.265032 | 15.067846 | +0.171605 / +0.237422 | no / no |
| Added descendants take the NH-white all-age net overcount | 10.761065 | 14.407190 | -0.332361 / -0.423234 | no / no |
| All birthdays at younger April-2020 age | 11.038464 | 14.775349 | -0.054962 / -0.055075 | no / no |
| All birthdays at older April-2020 age | 12.218530 | 15.957834 | +1.125104 / +1.127410 | no / no |
| Add omissions to national denominators, retain overcounts | 7.793153 | 11.090479 | -3.300273 / -3.739945 | no / no |

[CALCULATION: `derived/coverage_bound.json` scenarios and denominator arm; CSV gives per-generation pieces] Central CPS replicate SEs are **0.430 / 0.409bn**. They exclude the unobserved transfer and construction uncertainties. The central increment itself exceeds $5bn at both ends; replacing the old calculation moves each end by less than $5bn, but **flips the stated one-sided claim** and changes the population/cohort rule.

## 7. Interface, consumers and fail-closed checks

Live fields are `coverage_bn` and `case_with_coverage_bn`; the historical directory/script/output basenames remain stable. The old `factor` is no longer a live correction: it appears only through the archived positive-control arithmetic. Consumer search: `rg -n --no-ignore 'bound_bn|case_with_bound_bn' research infra` plus all references to this lane/output basename. The complete raw exact-name inventory is `consumer-names.txt`.

Verified migration consumers: `number_drift_audit_2026_09_29/source_map.csv` rows 280–282 and 978–980 (the last group also uses old `factor`); its generated `derived/number_audit.csv` rows 383–385 and 938–940; research INDEX, confidence ladder entry 303 and v6 assumption-review note; the root CLAUDE companion text. Parent owns those migrations and reruns the number audit. Unrelated rental-overlap/legacy LTSS fields with the same bare name are different quantities and are unchanged. This lane's archived inputs and positive-control reader legitimately retain the old names; tests assert they are absent from the live JSON. [DATA: traced source-map paths and documents; consumer inventory] No runtime consumer outside the drift source-map route was found in the searched code paths.

Input failures stop with `[BLOCKED]`: duplicate generation rows, non-finite values, non-positive populations, case/allocation/spec metadata mismatch, non-closing costs, ambiguous national drivers, stale source/code/cache, or new unpinned pricing reads. `pricing_dependencies.json` records the actual transitive research-module/table reads and numerical runtime. Every normal export checks those hashes **before scientific execution**, and the manifest digest is bound to the cache receipt. This prevents an upstream key change from silently altering age costs while totals still close. [CALCULATION: negative tests, `pricing_audit.json`]

## 8. Recommendation and evidence that would change it

Recommend **zero additional coverage item in the next main central**, with the **+11.1 / +14.8bn** construction and full sensitivity envelope beside it. This is a judgment about measurement adequacy, not evidence that the true coverage adjustment is zero. The Census controls preserve Hispanic all-age totals, but directly observed age blending removes most of the young-child DA gap. Mexican-origin, nativity, state, survivor and fiscal-key omissions are not observed here; the DA middle through age 29 and PES adulthood constructions disagree over the bar. A single transferable all-age dose cannot resolve that disagreement. [INFERENCE]

Revisit on origin/nativity-specific coverage linked to the blended controls and survivor cohorts, an identified Hispanic-origin series resolving the DA/PES young-adult difference, and an engine rerun of the changed group size. The current denominator arm is already below the $5bn bar as a change from central; that does not prove all omitted engine interactions are below it. [INFERENCE]

## Reproduce and verification log

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/acquire.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/inputs/controls/compare_base.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/source_tables.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_bound.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/coverage_bound_2026_10_14/test_coverage.py infra/immigration-fiscal/coverage_bound_2026_10_14/test_national_keys.py infra/immigration-fiscal/coverage_bound_2026_10_14/test_dependencies.py -q -p no:cacheprovider
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/write_result.py
```

Initial acquisition uses `acquire.py --download`; raw primary control snapshots are tracked with URLs/hashes. `export_pricing.py --capture-dependencies` is the explicit initial dependency-discovery command, not the normal reproduction command. `dependency_manifest.py` and `national_keys.py` are imported modules exercised by export and tests; the final lane rerun uses `--allow-unrun` for those two modules only. No runnable script is omitted.

- 2026-10-14 20:49 JST (`date` receipt in controls evidence): source quote/page checks and the original control comparison passed; subsequent sex-specific comparison reproduced three files identically.
- 2026-10-14 21:08 JST (`date`): case pricing and first coverage arms computed. A retained NumPy column view caused excess memory; copied central columns release each 161-column temporary. Repaired pricing passed the 2.5GB guard. No national-key tolerance was loosened.
- 2026-10-14 21:25 JST (`date`): transitive provenance gap from the code review repaired with actual-read manifests and cache digest binding; 52 tests passed, including same-size upstream changes and new-read negative controls. The latest observed capture export used 15.707s / 1716.0MB peak RSS; coverage used 4.356s / 567.7MB. These are Python `perf_counter`/`getrusage` observations, not `/usr/bin/time -l` measurements. Final all-file rerun receipt is appended after completion.
- 2026-10-14 21:44 JST (`date`): all-file rerun stopped on a concurrent generation CSV change. Preserved the original committed split inside this lane with its unchanged original digest and explicit epoch scope; recaptured actual dependencies, retaining all source/cache guards. This is a version freeze, not verification of the peer's pending routing changes.
- Final frozen-epoch preparation: 56 tests passed; export used 11.529s / 2013.3MB peak RSS; calculator used 2.550s / 587.5MB. Final byte-comparison receipt is recorded in the external parent handoff so verification does not mutate an artifact under comparison.

**Source/artifact coverage:** controls and PES/DA source files; cohort and generation pricing; all declared denominator pieces; old-name consumers; negative tests and cache/provenance guards. **Not changed:** the frozen case and every other lane, research documents and the drift source-map (parent ownership), raw upstream data, Git metadata. **Not computed:** cash-set/debt implications, person-linked missed-resident survival, or a general-equilibrium/group-size engine rerun; these are outside this coverage-price construction and remain explicit limits.

## Revisions

2026-10-14 P7 re-derivation: source control/age evidence disconfirmed the earlier absorption and population-scope claims. The original result is preserved verbatim as `inputs/legacy_result.md`, with original code and output positive control beside it; its one-sided wording is **superseded**. Current results are the tables above.

## 2026-10-15 oct15 base repricing

The live route is `coverage_oct15.py`, priced separately on the oct15 accrual set and cash set. The preceding commands and oct14 result describe the preserved earlier epoch; the live commands below never regenerate its outputs. Discovery freezes the coverage-off case payloads, generation CSVs and their full-precision summaries, and the household lines under `inputs/oct15_base/`. The receipt hashes each exact source byte sequence. Generation full-precision and household splits must close to each base end at 1e-9bn before freezing. Later case/consumer coverage-on files do not replace these base inputs. [CALCULATION: `coverage_oct15.py:freeze_base`, `inputs/oct15_base/manifest.json`]

The read-only adapter retains the uniquely asserted household AST boundary and every accumulated construction gate. Completed reporters and observed nonreporting children stay on their own person records. Original household pieces use their original member masks; completion pieces follow their declared parents; the mixed-unit amount uses its declared generation total per member. Added people are separated using the household construction's explicit weights and calibrated to `meta.coverage_added_cost_bn`, sourced from the case's exact all-nonreporting-descendant total. Constants remain per head within generation. All 161 replicate totals retain the existing 1e-6bn price-closure tolerance. Both sets use their own price kernel; cash never inherits accrual dollars. Peak physical footprint gates the pricing process via the existing shared helper. [DATA: frozen `lines{,_cash}.json`; `pricing_audit_oct15_{set,cash}.json`] [ASSUMPTION: within-generation residual and net-profile calibration]

Observed nonreporting children are priced from the case's native own-age unit cells, public-capital changes and production; their exact driver is checked independently against `meta.child_pricing.records` and their PH_SEQ/PPPOS IDs. Original G3+ parents retain the `before_native_children` line/road/pension declarations. The exact added calibration target is independently checked against the frozen `lineage_addition.json` v8 set/cash `all_nonreporting_descendants.cost_bn`. [CALCULATION: `national_keys.py:full_key`, `coverage_oct15.py:freeze_base`]

Every original construction and arm remains in `sets.{set,cash}.scenarios`. April-2020 cohort eligibility, sex-specific controls and zero central correction on added descendants are unchanged. Central and arm generation costs add at 1e-9bn. `implied_net_missing_people_by_age_band` reports signed people by generation and March-2025 five-year band; `adults_by_generation` uses exact observed age >=18. `by_generation_age_band` includes each band's exact coverage cost and implied per-person price at both ends, so household consumers can carry a separate block of people the survey misses without spreading it over observed households. The price is a signed net-cohort average, not an observed missing-person estimate. [CALCULATION: `coverage_oct15.py:calculate`, `missing_age_prices`]

One-time discovery, only after actual upstream base gates pass:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_oct15.py --freeze-base
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis set --capture-dependencies
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis cash --capture-dependencies
```

Live reproduction commands:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis set
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis cash
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_oct15.py --production-split generation_ratio
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/coverage_bound_2026_10_14/test_coverage.py infra/immigration-fiscal/coverage_bound_2026_10_14/test_national_keys.py infra/immigration-fiscal/coverage_bound_2026_10_14/test_dependencies.py infra/immigration-fiscal/coverage_bound_2026_10_14/test_oct15.py -q -p no:cacheprovider
```

The all-file rerun uses `--allow-unrun coverage_bound.py --allow-unrun dependency_manifest.py --allow-unrun national_keys.py`: these are imported and tested shared modules; `coverage_bound.py`'s standalone entry is the archived oct14 writer. The live calculator uses its one authoritative construction table and cohort/pricing/denominator helpers. The old source outputs, frozen original generation input and positive-control result stay untouched.

Central `ends.<end>.decomposition` traces each existing price piece with the same signed missing-person weights. Public-capital cost is split by its declared federal/state-local level. Fiscal line amounts retain their true source side and parent, including reporter carriers. Residuals, mixed-unit post-engine amounts and net-profile calibration are explicitly unclassified; no borrowing interpretation is attached to those amounts. Production has only a combined earnings-key person profile in the household kernel. The recommended explicit `--production-split generation_ratio` applies that generation/end's declared private-WTP and induced-receipt ratio to its existing combined pieces, preserving signed P+F exactly; it is an allocation approximation, not independent person-level P/F measurement. `--production-split unclassified` exposes the alternative. Costs and imputed capital are signed net costs; P/F are signed gains. The gate is `capital + fiscal lines + unclassified - P - F = total coverage` at 1e-9bn. Cash additionally exposes the classified cash fiscal amount `fiscal lines - F`; it excludes imputed capital, private P and every unclassified amount. [CALCULATION: `export_pricing.py:component_metadata`, `coverage_oct15.py:decompose`] [ASSUMPTION: production allocation]

Central ends also expose `adult_cost_by_generation_bn` and `minor_cost_by_generation_bn`, priced on the exact observed age >=18 partition and the same sex/cohort-specific missing-person factors. Their generation sums close to central coverage at 1e-9bn. These missing-count assumptions have construction sensitivities, not an estimated missing-count SE. The conditional CPS replicate uncertainty is separate. The NPZ retains exact `age`, `generation` (0=G1, 1=G2, 2=G3plus), `person_rows`, `person_ph_seq`, and `person_pppos`; `net_id[end,person,replicate]` is signed per-person cost in bn and `weights[person,replicate]` is the identified population weight. [CALCULATION: `coverage_oct15.py:calculate`, `export_pricing.py:main`]

The principal generation source declares a G1 count reconciliation of +0.0000120997428894 people with zero dollars. Observed pricing weights plus that declaration close at the original 1e-6-person population gate. It has no invented person record, age or coverage exposure. Every superseded base-line receipt remains beside the current frozen inputs; a line-only refresh requires every other frozen BASE source byte to stay identical. [DATA: `inputs/oct15_base/generation_summary.json.population_rounding`, `lines.json.meta.population_rounding`]

Reporter own-job national driver masses come from the principal producer's national tax closure multiplied by its exact scalar G3 fill-in factor, not a reporter-only denominator. The reporter tenant-property full-frame extension uses the principal completion lane's G3 age-specific tenant rates as an explicitly scoped age proxy; its priced reporter restriction must reproduce the actual vector. Native school and other-education components are independently traced to principal own-age category amounts whose sum equals their education row cost. No generic driver fallback is used. [CALCULATION: `national_keys.py:full_key`] [ASSUMPTION: reporter tenant-property national extension]

2026-10-15 physical-memory repair: the pricing process releases the raw household construction before allocating separate identified/added net profiles, transfers ownership of the original profile, and copies only the added profile. A profiled set export passed at 2,481.5 MB physical peak in 21.354 seconds. These are measured physical peak and Python elapsed time; the output guard remains 2.5 GB. Failed initial receipts are retained under `_cache/failed_footprint`, and the calculator's negative probe refused their publication. The profiling launcher now preserves `SystemExit`, including failed physical gates; the stdlib CLI was observed to return zero after such a failure. The exact regression and repair are in `failure-catalog.md` and `test_oct15.py:test_cpu_profile_cannot_mask_failed_gate`. [CALCULATION: explicit profiling run and negative gate probes]

2026-10-15 gated publication: `derived/coverage_bound_oct15.json` central accrual increments are **12.001818463568476 / 15.859877306531986bn**; own cash increments are **3.950844257775926 / 7.8089031007393bn**. Central signed missing counts are G1 **446,105.1075376299**, G2 **824,190.8641341948**, G3+ **690,117.6475083351**, added **zero**; these are modelled counts conditional on the source-rate transfer. The construction envelopes are accrual low **[-16.452275756584886, 23.704153740596823]**, high **[-16.91162933053944, 27.6068239193491]**, cash low **[-16.48883669637207, 18.226159636585592]**, high **[-16.948190270326588, 22.128829815337795]** bn, not confidence intervals. Final source capture exports exited 0 at physical **2,483.8 / 2,349.2MB**, elapsed **19.982 / 17.424s**, set/cash respectively; the calculator exited 0 at **730.7MB / 3.865s**. [DATA: `sets.{set,cash}.ends`, `.implied_net_missing_people`, `.range_bn`; exact export/calculator terminal receipts]

The final provenance refresh retained complete prior ten-file BASE snapshots and receipts. It requires engine edit/declaration and convention-a numerical identity at a 1e-12 floating-roundoff ceiling, exact CSV strings and record IDs/shapes; native child rows retain identical original amounts with independently closing education category fields. An exact-byte initial probe stopped on 1e-16-scale edit roundoff in the upstream provenance rebuild; the source principal 1e-9bn and pricing 1e-6bn guards were not loosened. Case/end/count identities and every existing frozen-source integrity guard remain active. [CALCULATION: `coverage_oct15.py:validate_base_revision`, append-only `inputs/oct15_base/superseded_*` receipts]

The four live BASE reproduction commands completed with exit 0 and **IDENTICAL: 100/100 files unchanged**; the published suite had **69 passed**, including source drift, missing/stale cache, native pricing, decomposition and profiler controls. The oct14 source artifacts remain untouched. [CALCULATION: `_cache/rerun_oct15.log`, status-preserving lane harness]

## 2026-10-15 phase2 final-routing consistency

The separate final-routing replay freezes actual coverage-on household lines under `inputs/oct15_final_routing/`. It runs every existing household construction gate before subtracting only the declared coverage post-engine residual from generation and union costs. Coverage remains a separate missing-person block; it is excluded from every observed person's price kernel. The resulting NPZ and audit are tagged `oct15_final_routing`, preserving the original BASE price records. Its central source-rate/cohort factors are identical to the BASE construction; the same observed frame, identified/added populations, all 161 weights and exact person identifiers must agree. The signed repricing delta in each set/end must be <=0.5bn; a larger delta writes its receipt and stops the parent. [CALCULATION: `coverage_final_routing.py`, `export_pricing.py --final-routing`]

Convention-b minor-parent scaling changes neither the convention-a coverage price channel nor its own counts. Final state and credit routing changes that apply to convention a require the separate measured price replay. This is a conditional consistency check, not a new coverage estimate or missing-resident measurement. [CALCULATION: principal `v7_split.cjs`/`v8_split.cjs` convention selectors; final replay]

Current-source BASE replay after adding the final-routing adapter is byte-identical for both entire pricing NPZs, both age-price CSVs and the published coverage JSON. Actual read manifests contain no live oct15 generation-summary/corrections read in the household pricing prefix; its frozen lines hold the adult target. Only its existing historical key/model/stack inputs are read. No unused context parameter or relaxed dependency guard is needed. After the constructor gates, the exporter releases redundant full-frame replicate columns while retaining all 161 union-row weights and the full-frame central column used for national/pension drivers. Measured set/cash physical peaks were **2,430.1 / 2,344.1MB**, elapsed **24.744 / 16.239s**; the identical coverage replay used **730.8MB / 5.476s**. [CALCULATION: source captures, exact hash comparisons and calculator receipt]

Final state pieces are checked against each principal `added_state_prices` source cell, edit, charge declaration, selected key, subgroup dollar amount and category share. Identified/latent fractions follow the actual weight placement: one/zero outside original G3+, `1/f_rec`/its complement within original G3+. Native children use their own source amounts and IDs. P7 justice per-head/use and school/other-education shares remain distinct. A cross-generation regression rejects the earlier nominal G3 factor on G1, which could change age allocation while totals still closed. [CALCULATION: `national_keys.py:full_key`, `test_oct15.py` state-driver tests]

The authoritative final target preserves `meta.coverage_added_source_cost_bn`, declares the signed active latent/native state subtotal in `coverage_added_state_reallocation_bn`, and sets `coverage_added_cost_bn` to their sum. The adapter checks the source against frozen BASE and the delta against all active principal state parts at 1e-9bn before calibration. This recognizes a changed subpopulation allocation within a conserved headline; it prevents calibration from silently erasing the state correction. [CALCULATION: final household exporter target contract, `coverage_final_routing.py:observed_snapshot`, negative regression]

Final-routing discovery after the actual final household gates:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_final_routing.py --freeze-final --case-final /private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/CASE_FINAL
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis set --final-routing --capture-dependencies
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis cash --final-routing --capture-dependencies
```

Additional live replay commands, after that freeze:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis set --final-routing
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py --case oct15 --basis cash --final-routing
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_final_routing.py
```

2026-10-15 final-routing check: all four set/end differences pass the $0.5bn threshold. Final accrual coverage is **12.01834723176309 / 15.876526158661639bn**, versus preserved BASE **12.001818463568476 / 15.859877306531986bn**; deltas are **+0.016528768194614685 / +0.01664885212965217bn**. Final cash coverage is **3.967373025970561 / 7.8255519528689215bn**, versus preserved BASE **3.950844257775926 / 7.8089031007393bn**; deltas are **+0.016528768194635113 / +0.016648852129621083bn**. The adopted case keeps its original coverage file. [DATA: `derived/coverage_final_routing_check.json.sets.{set,cash}.ends.{low,high}`, `.pass=true`, `.threshold_bn=0.5`]

Both final pricing receipts pass every constructor, source-driver, population, generation and 161-replicate price gate. Their audits exclude the missing-person block from observed prices and set `gates.physical_footprint_within_2_5GB=true`. Measured physical peaks were **2,206.5 / 2,240.9MB**, elapsed **30.586 / 24.958s**, set/cash; the set run uses the status-preserving profiler. The final consistency calculator passed at **733.7MB / 4.709s**. Completed-end source piece drivers now release only after that end's gates and metadata capture; no precision, arithmetic or tolerance changed. [DATA: `derived/pricing_audit_oct15_final_routing_{set,cash}.json`; profile and export terminal receipts]

The first frozen final epoch is retained under `inputs/oct15_final_routing/superseded_*`. Its complete generation adult target incorrectly included the separate missing-adult block. The narrowly checked refresh preserves the complete source target, declares the exact coverage population/adult exclusion, and requires every dollar and unrelated field to remain identical. The original observed-adult gate stays unchanged. `failure-catalog.md` retains this failure and the physical-buffer failures; the targeted regression rejects both an uncorrected target and an unrelated amount change. [CALCULATION: `coverage_final_routing.py:validate_observed_target_revision`, `test_oct15.py:test_final_target_refresh_preserves_complete_population_and_all_dollars`]

2026-10-15 final stable-source verification: BASE set/cash captures passed at **2,207.5 / 2,142.0MB**, **18.381 / 17.121s**; the BASE calculator passed at **730.7MB / 4.124s**. Both entire BASE pricing NPZs, both age-price CSVs and the published coverage JSON remain byte-identical to the retained pre-final-routing records, including after the full rerun. The original coverage SHA256 is `9843ba1db05666d11fc70008f6183b3562e805de8cb2b152ba7286d06092e367`. The preserved oct14 artifacts show no git diff. [CALCULATION: `_cache/check_base_bytes.py`, `_cache/base_identity_after_final_source.json`, final source-capture receipts]

All seven live commands above completed with exit **0**, and the lane harness ended **IDENTICAL: 91/91 files unchanged**. The complete focused suite has **77 passed**. Discovery/archive commands are one-time operations; the live harness imports/tests the shared modules and never invokes the historical oct14 writer. Every changed path, including frozen epochs and ignored price/profiling/proof artifacts, is listed in `changed-paths.txt`; parent owns holistic diff review and git adoption. [CALCULATION: `_cache/rerun_oct15_final.log`, focused pytest run, changed-path manifest]

2026-10-15 atomic-source epoch correction: the preceding 91/91 replay predates the household owner's atomic-publication source edits. A read-only audit found exactly two stale dependencies in every actual-read manifest: `completion_jobs.json` and `completion_keys.py`; all four principal guards stopped, while frozen inputs and the coverage cache/checksum guards remained valid. The independently admitted reporter/exporter atomic source files were absent from the coverage prefix's actual-read manifests. No hash was manually changed. [CALCULATION: all four `dependency_manifest.validate_manifest` guards and complete mismatch inventory]

With the parent's explicit replay authorization, all four actual-read pricing routes were recaptured through their original scientific and physical gates. The preceding four NPZs, four age CSVs, four audits, four manifests and both coverage JSONs are retained in `_cache/pre_atomic_source_epoch/`. The updated four principal guards and the household producer's three source pins pass. Four NPZs, four age CSVs and both coverage JSONs remain exact **10/10**; both calculators exit 0 with unchanged four repricing deltas. Current BASE set/cash exports passed at **2,190.4 / 2,142.7MB** and final set/cash at **2,285.1 / 2,237.6MB**; the exact route terminal receipts remain in the archived capture logs. [CALCULATION: `_cache/recapture_atomic_epoch.py`, preserved source epoch/capture logs, principal guard checks]

The **current atomic-source epoch** seven-command harness exited **0**, every command exited **0**, and comparison ended **IDENTICAL: 91/91 files unchanged**. It used the protected absolute `TMPDIR=/Users/alien/Projects/immigration-research/infra/immigration-fiscal/coverage_bound_2026_10_14/_cache/repro-temp`. Its authoritative log is `_cache/rerun_oct15_atomic_source.log`; `_cache/rerun_oct15_final.log` is the preceding epoch. The unchanged focused suite has 77 tests. Final prose is applied after the comparison; source/data bytes are unchanged. [CALCULATION: current atomic-source harness status and log]

## R3 coverage correction — 2026-10-15 04:50:30 JST

**Verdict:** Corrected coverage pricing; central and every construction use zero on administratively complete justice-use drivers and their capital descendants. Observed base prices, union-completion carriers, counts, frozen BASE/final inputs, key `oct15`, and source epochs are preserved. [CALCULATION: export_pricing.py, coverage_oct15.py, coverage_final_routing.py]

The four administrative justice-use components total **3.154827692bn** (public-order 2.880455117, state correction 0.274372575, including reporters). These are not the capital components. The matched justice-use capital descendants add **0.044176308bn low / 0.066264462bn high**. The complete rule therefore lowers every set by **3.199004000 / 3.221092154bn**, rather than the review lead of a uniform 3.155. Per-head justice and its capital descendants stay. [DATA: before/after `coverage_bound_oct15.json` line_parts; principal key/capital declarations in national_keys.py]

| Item 12, bn low / high | Before | Corrected | Change |
|---|---:|---:|---:|
| set | 12.001818 / 15.859877 | 8.802814 / 12.638785 | -3.199004 / -3.221092 |
| cash | 3.950844 / 7.808903 | 0.751840 / 4.587811 | -3.199004 / -3.221092 |

| Item 12 by generation, bn low / high | Before | Corrected |
|---|---:|---:|
| set, G1 | 1.419816 / 2.278465 | 0.852209 / 1.707003 |
| set, G2 | 5.970629 / 7.569746 | 4.471476 / 6.060463 |
| set, G3plus | 4.611374 / 6.011666 | 3.479129 / 4.871319 |
| cash, G1 | 0.013893 / 0.872543 | -0.553714 / 0.301080 |
| cash, G2 | 2.332943 / 3.932059 | 0.833789 / 2.422777 |
| cash, G3plus | 1.604009 / 3.004301 | 0.471764 / 1.863954 |

### All constructions, repriced

The pre-fix values for the two newly named DA boundaries are reconstructed on the preserved observed base price arrays; every previously published construction reproduces its actual pre-fix value within 1e-9bn before this comparison. [CALCULATION: parent scratch r3fix_document.py; preserved before JSON]

| Construction | Set before | Set corrected | Cash before | Cash corrected |
|---|---:|---:|---:|---:|
| central | 12.001818 / 15.859877 | 8.802814 / 12.638785 | 3.950844 / 7.808903 | 0.751840 / 4.587811 |
| pes_only | 10.856935 / 14.645240 | 7.657931 / 11.424148 | 2.805464 / 6.593769 | -0.393540 / 3.372677 |
| da_low | -16.452276 / -16.911629 | -16.421971 / -16.881120 | -16.488837 / -16.948190 | -16.458532 / -16.917680 |
| da_middle | 6.259687 / 8.124688 | 5.041197 / 6.897782 | 3.620898 / 5.485898 | 2.402407 / 4.258993 |
| da_high | 23.704154 / 27.606824 | 21.218328 / 25.103833 | 18.226160 / 22.128830 | 15.740334 / 19.625839 |
| pes_nce_minus_1se | 14.441393 / 18.989787 | 10.782084 / 15.305212 | 5.534846 / 10.083241 | 1.875537 / 6.398666 |
| pes_nce_plus_1se | 9.613340 / 12.794612 | 6.865218 / 10.027514 | 2.398117 / 5.579389 | -0.350006 / 2.812291 |
| proportional_pricing | 16.855003 / 20.760706 | 14.624047 / 18.514379 | 13.291146 / 17.196849 | 11.060190 / 14.950522 |
| age_priced_all_age_rate | 15.909792 / 19.774327 | 13.640995 / 17.489866 | 12.422093 / 16.286628 | 10.153295 / 14.002166 |
| proportional | 15.372701 / 19.071215 | 13.287420 / 16.971552 | 12.120688 / 15.819202 | 10.035407 / 13.719539 |
| post_arrival_rate | 12.159989 / 16.206252 | 8.846629 / 12.870027 | 3.768418 / 7.814681 | 0.455058 / 4.478456 |
| arrival27_none_pre2020 | 11.981733 / 15.830278 | 8.788656 / 12.615153 | 3.947164 / 7.795709 | 0.754086 / 4.580583 |
| arrival27_all_pre2020 | 12.142413 / 16.067070 | 8.901922 / 12.804209 | 3.976608 / 7.901265 | 0.736117 / 4.638404 |
| added_white | 11.635487 / 15.403852 | 8.484177 / 12.230796 | 3.675666 / 7.444032 | 0.524357 / 4.270976 |
| birthday_younger | 11.944049 / 15.801694 | 8.743762 / 12.579310 | 3.880104 / 7.737749 | 0.679817 / 4.515365 |
| birthday_older | 13.184392 / 17.050922 | 10.011660 / 13.856282 | 5.398937 / 9.265467 | 2.226205 / 6.070828 |
| da_middle_0_9 | 11.754459 / 15.597135 | 8.555455 / 12.376043 | 3.703391 / 7.546067 | 0.504387 / 4.324975 |
| da_middle_0_17 | 9.170987 / 12.740958 | 6.181589 / 9.730919 | 1.290417 / 4.860389 | -1.698981 / 1.850350 |

### National Hispanic coverage implied by each DA boundary

| Construction | Constructed true population | Implied all-age net coverage error | Difference from PES, in PES SE |
|---|---:|---:|---:|
| central | 65,431,223 | -5.1217% | -0.248 |
| da_middle_0_9 | 65,416,937 | -5.1010% | -0.209 |
| da_middle_0_17 | 65,160,848 | -4.7280% | +0.494 |
| da_middle | 63,622,261 | -2.4240% | +4.841 |

The PES national comparator is **−4.99%, SE 0.53 percentage points**. The table computes Census enumerated / constructed truth − 1, not blended base / truth − 1. The age-sex truth is blended-base population × (1 + the selected residual factor), using `inputs/controls/base_adjustments_sex.csv` and the pinned PES rates also exported in `derived/coverage_rates.csv`. [CALCULATION: coverage_oct15.py:national_constructions; SOURCE: pinned Census tables parsed by source_tables.py]

Boundary criterion: use DA where it agrees with PES or PES understates young-child omissions (0–4); at 5–9 the estimates agree within about 0.2 PES SE, while they diverge at 10–17 by about 2.9 SE and at 18–29 by about 9.6 SE. PES is the direct measurement with an SE where the two diverge. DA through 9 and through 17 are named arms beside the retained DA-through-4 central; the all-age PES total alone cannot distinguish those three nearby totals. [DATA: derived/da_coverage.csv, coverage_rates.csv; INFERENCE: declared boundary criterion, not an identified optimal splice]

The corrected cash low end is **negative under PES-only and some DA constructions**. Any earlier statement that every construction except DA-low is positive is superseded separately for each set by this table. These are modeled coverage transfers, not observations of the missing people; the construction envelope remains a sensitivity envelope, not a confidence interval. [CALCULATION: sets.cash.scenarios]

### Key classification and source trace

| Source lines / categories | Classification and coverage rule | Principal evidence |
|---|---|---|
| `public_order_safety` (`justice_use`) | Administrative group-use total; constructed coverage people take zero. Prisons: ACS institutional count/household-count rate; arrests: FBI ethnicity share plus custody scaling; ICE: administrative interior custody estimate. | `generation_account_2026_09_24/keys.py:207-241`; `cj_use_allocation_2026_09_23/RESULT.md:64-76,95-99`; `within_group_distribution_2026_09_29/households.py:879-888` |
| `state_price_public_order_safety` (`justice_use`) | Same administrative use driver as parent; zero. | `households.py:211-213,845-849`; `national_keys.py:102-114` |
| `pos_fed`, `pos_sl` (`capital`, custody-driver piece) | Administrative-use parent; zero. Excluding only `justice_use` would miss these pieces. | `households.py:1004-1028`; `national_keys.py:291-313`; principal capital declarations in `coverage_bound_2026_10_14/inputs/oct15_base/lines.json`: `rule.numerator_lines=[public_order_safety]` |
| Same four source lines, per-head driver (`justice_per_head`, or `capital`) | Per head; retain. Police/fire/courts/border allocations not use-keyed remain in this part. | `keys.py:219-224`; `households.py:636-648,882-888`; `national_keys.py:102-108` |
| `federal_income_tax`, `state_local_income_tax`, `other_personal_tax` (`taxes`) | Survey tax-model liability keys; retain. Federal benefit-tax offset is separately keyed on survey SS benefits in set, absent from cash. | `cps_imputation_keys_2026_09_23/common.py:128-154`; `households.py:870-874`; `national_keys.py:124-125` |
| `employee_oasdi`, `employer_oasdi`, `employee_hi`, `employer_hi`, `self_employment_oasdi_hi`, `other_domestic_social_contributions` (`taxes`) | Survey wage/capped wage/self-employment/FICA-worker keys; retain. | `common.py:130-139`; `households.py:560-577`; `keys.py:149-161` |
| `corporate_capital`, `corporate_labor`, `personal_property_tax`, `remaining_production_property`, `other_production_taxes` (`taxes`) | Survey capital/wage keys; retain. Completion reporter carriers for the three production taxes follow declared own-job principal receipts instead of the ordinary capital vector; still survey records, not administratively complete group-use totals. | `common.py:130-145`; `households.py:932-942`; `national_keys.py:245-252` |
| `general_sales_tax`, `excise_selective_sales`, `customs_duties`, `personal_current_transfers` (`taxes`) | Survey SPM-resources consumption key; retain. | `common.py:145`; `households.py:560-577` |
| `personal_motor_vehicle` (`taxes`) | Per adult aged 18+; retain. | `common.py:137`; source row `personal_motor_vehicle.key=adults` in frozen `lines.json` |
| `modeled_owner_property` (`taxes`) | Survey household tenure/value × state rate / household size, SPM-shared; retain as modeled survey key, not an administrative property-tax group total. | `keys.py:50-57`; `households.py:579-586` |
| `tenant_occupied_property` (`taxes`) | Survey tenant-headcounts by state, normalized to modeled group rent; retain. Reporter completion uses declared G3 age-price proxy. | `households.py:221-246,943-947`; `national_keys.py:253-261` |
| `medicare_supplementary_premiums` (`taxes`) | Survey Medicare coverage indicator; retain. | `common.py:135,146`; `keys.py:149-161` |
| `enterprise_surplus` (`enterprise`) | Per resident head; retain. | `households.py:570`; frozen source row key `resident_population` |
| `housing_enterprise_surplus` (`transfers`, native child `taxes`) | Survey housing-assistance key; retain. Native child's category label differs, source parent remains the same. | `households.py:584,875-876`; native source verification `national_keys.py:199-235` |
| `medicaid_and_chip_other_medical` (`health`, native child `transfers_per_head`) | Two survey parts: MEPS mean Medicaid paid dollars by age/US birth transported to CPS exposure, plus survey uninsured person-years. Retain both. No Medicaid administrative enrollment/use numerator is used here. | `keys.py:60-82,252-280`; `households.py:564-566,889-892`; `national_keys.py:109-111` |
| `medicare` (`health`) | MEPS age/birth donor payer mean × CPS exposure; retain. Set includes separately priced HI accrual below. | `keys.py:60-82`; `households.py:864-869` |
| `military_medical`, `veterans_other`, `health_services`, `state_price_health_services` (`health`, native `other_shared`) | MEPS TRICARE, VA and other-public payer donor means × CPS exposure; retain. State-price correction inherits parent key. | `keys.py:60-82`; `households.py:564,572,845-849` |
| `social_security`, `medicare` (`pension_accrual`, set only) | Survey receipts-derived composite (OASDI / HI, with SE shares), fixed generation coefficients; retain. Completion reporters instead use the declared person-pension profile. These are modeled claims, not administrative current-use totals. | `households.py:835-843,858-869,952-955`; `national_keys.py:76-95,264-266` |
| `social_security` (cash `transfers`), `railroad_retirement`, `ssi`, `unemployment`, `income_security_services`, `family_and_general_assistance`, `veterans_life_insurance`, `veterans_pension_disability`, `veterans_readjustment`, `workers_compensation`, `black_lung`, `temporary_disability`, `other_federal_benefits` (`transfers`) | Survey benefit dollar keys (SS, SSI, unemployment, cash assistance, veterans, workers comp, all cash); retain. `other_federal_benefits` also has routed Pell school/P pieces. | `common.py:157-182`; `households.py:820-830,902-912` |
| `snap`, `energy_assistance`, `other_state_welfare`, `housing_subsidies` (`transfers`) | Survey SPM-unit SNAP, energy, WIC and housing-assistance dollars split per member; retain. | `common.py:160-172`; `households.py:560-577` |
| `refundable_tax_credits` (`transfers`) | Survey modeled EITC + ACTC, with the case's declared item routing; retain. | `common.py:168`; `households.py:902-912` |
| `education_services`, `school_reprice`, `college_rekey`, routed school/P parts of `other_federal_benefits` (`schools`, `education_other`) | School part: survey October CPS public K–12 enrollment rates × state pupil spending. P part: state finance per population. Retain both; P is per-head state pricing, not a complete observed group enrollment total. Routed corrections inherit these components. | `keys.py:85-107`; `school_enrollment_2026_09_20/measurement.py:105-143`; `households.py:823-829,902-912` |
| `education_benefits` (`transfers_per_head`) | State item-P per-population key; retain. | `keys.py:96-107`; `households.py:574-576`; frozen row key `postsecondary` |
| `employment_training`, `other_state_benefits`, `pension_guaranty` (`transfers_per_head`) | Per working-age head, all heads, age65+ head respectively; retain. | `common.py:173-176`; frozen rows' selected keys `working_age`, `population`, `age65plus` |
| `general_public_services` (`general_government`), `housing_community_services` (`other_shared`), `recreation_culture`, `state_price_recreation_culture` (`roads_parks`, native `other_shared`) | Per head; retain, with declared service responses. | `common.py:173`; `households.py:649-666,845-849` |
| `economic_affairs_services` (`roads_parks`) | Survey SPM resources; retain. | `common.py:172`; frozen row key `resources` |
| `roads_vmt_fed`, `roads_vmt_sl` (`roads_parks`, native `other_shared`) | Mixture of age5+ per-head miles driver and survey consumption/resources freight/old key; retain. National miles calibrate the rule, not an administratively observed group miles total. | `households.py:850-857`; `national_keys.py:115-119` |
| `k12`, `college`, `k12_user_fees`, `college_user_fees` (`capital`) | Inherit survey school and state-P per-head parents, including routes; retain. | `households.py:1004-1028`; `national_keys.py:291-313` |
| `health_fed`, `health_sl`, `health_fed_user_fees`, `health_sl_user_fees` (`capital`) | Inherit MEPS health parent; retain. | Same capital parent code; principal rules name `health_services` |
| `gps_fed`, `gps_sl`, `rec_fed`, `rec_sl` (`capital`) | Per-head general-service/recreation parent; retain. | Same capital parent code; principal rules name `general_public_services` / `recreation_culture` |
| `hwy_fed`, `hwy_sl`, `air_fed` (`capital`) | Roads/resources parent mixture (air: resources); retain. | `households.py:1016-1028`; `national_keys.py:302-313` |
| `ent_housing_sl` (`capital`) | Survey housing-support parent; retain. | `households.py:1023-1028`; principal numerator `housing_subsidies` |
| `ent_transit_sl`, `ent_airports_sl`, `ent_ports_sl`, `ent_power_sl`, `ent_water_sl`, `ent_sewer_sl`, `ent_tolls_sl`, `ent_power_fed`, `ent_other_sl`, `ent_other_fed` (`capital`) | Enterprise-surplus per-head parent; retain. | `households.py:1006-1014`; `national_keys.py:295-301` |
| `production` (`production`) | Survey earnings × skill cell, generation production totals solved from the case; retain, labeled modeled production transport. | `households.py:669-700,1029-1031`; `national_keys.py:287-290` |
| `mixed_unit_removal` (`other_shared`) | Explicit generation per-member distribution assumption of a post-engine modeled amount; not an administrative-use total. Retain in coverage prices under current authorized personal pricing, while shared companion must omit item11 itself. | `households.py:1143-1151`; `national_keys.py:236-239` |
| `lane_constants`, `lane_residual`, `net_profile_calibration` (`other_shared` / separate net correction) | Unassigned/model residuals explicitly spread per generation head; retain with assumption label, not misclassified as observed use. | `households.py:948-949,990-992`; `export_pricing.py:250-257,279-299` |

### Material qualifications

- Schools are survey-keyed **for group use**, although national/state dollar costs and national controls are administrative. Public K–12 rates are October CPS weighted enrollment / weighted population (`measurement.py:128-143`), then transported to March person cells (`keys.py:85-107`); there is no administrative group pupil-count numerator that cancels a corrected group count.
- Medicaid is **MEPS payer-mean transport**, not CPS self-reported Medicaid dollars and not administrative Medicaid group use (`keys.py:60-82`). MEPS exposure excludes only uncovered infants, guarded at `:70-72`. Its survey bias and transport assumptions survive the repricing.
- Uninsured care uses CPS `NOCOV_CYR` full/half uninsured person-years and offsets from MEPS/program allocation keys (`keys.py:252-280`). AHA national uncompensated-care totals price that exposure; they do not observe the missing group's total use. Administrative national dollars alone therefore do not justify zeroing it.
- Administrative-use justice is still a modeled attribution: institutional residence is not correctional custody; arrest/Hispanic-to-Mexican and nativity splits use proxies; ICE interior share uses length-of-stay assumptions; years differ (`cj_use_allocation.../RESULT.md:74,97-99,113-121`). The exclusion means the existing administrative numerator already covers the missed people under the adopted model, not that every numerator perfectly observes their true use.
- Reporter and observed native-child completion pieces are a separate population route. Reporters retain all declared justice carriers (`households.py:932-988`). Native children verify their own-age principal costs (`national_keys.py:199-235`), rather than matching arbitrary adult custody vectors. Current observed children are minors; do not infer a generic exemption for future adult-native carriers.
- Zero-response lines never enter the nonzero-price inventory (`export_pricing.py:227-228`): defense, existing interest, excluded subsidies/external flows, and zero receipt carriers do not require a new coverage charge.

### Export and frozen-routing guards

`net_id` / `net_added` and `base_piece_prices` preserve observed-account price closure. `excluded_use_prices` records the exact 161-replicate administrative-use prices; `constructed_piece_prices` is zero on those drivers. Call `export_pricing.constructed_prices(data, audit)` after observed closure checks and before coverage evaluation. It rejects any nonzero constructed administrative-use price, requires identical prices elsewhere and checks excluded central prices against the traced pieces. Both BASE and final-routing calculators use it; the omissions-denominator arm also holds these complete administrative pools fixed. Other readers that evaluate constructed people must select this rule too. [CALCULATION: export_pricing.py:constructed_prices; negative tests in test_oct15.py]

Frozen final routing refers to its exact original coverage SHA `9843ba1db05666d11fc70008f6183b3562e805de8cb2b152ba7286d06092e367`. That original source is preserved byte for byte at `inputs/final_routing_coverage_source.json`; the AST adapter substitutes only that source-read path after a unique-boundary and receipt-hash check. All original upstream coverage/age/generation gates then run; observed_snapshot removes the old coverage block before corrected prices are evaluated. No existing frozen input or hash was changed. [CALCULATION: export_pricing.py:construction, frozen_coverage_source; test_frozen_final_routing_requires_its_exact_original_coverage_receipt]

Replay receipts are appended after the final stable-code harness. The original v7 and earlier oct15 prose above remains an execution/history record.

### R3 final receipt — 2026-10-15 04:59:09 JST

All seven specified live commands exit 0; **IDENTICAL 88/88, exit 0**, **79.797s** wall. All four person-price producers pass their own 2.5GB physical-footprint gates; the wrapper's diagnostic child RSS peaks at **2,894,954,496 bytes**, a macOS RSS over-read that is not the physical-footprint gate. The focused suite has **85 tests**. Final routing remains within 0.5bn of BASE: **+0.016270768 / +0.016390852bn** in both sets. Existing frozen input bytes and earlier-case outputs are separately checked against the worker's entry hashes. No source pin was changed, and no historical writer was run. [CALCULATION: _cache/r3fix_stable_replay.log; pricing_audit_oct15_*.json.gates; coverage_final_routing_check.json]

Preparation replay records are also retained: the first compared changed adapter/audit bytes; the next differed on two old adapter-hash audit receipts; the final stable-code replay above is authoritative. Prose receipts and changed-path manifests are appended after comparison; scientific outputs stay unchanged. [CALCULATION: _cache/r3fix_prepare_replay.log, r3fix_final_replay.log, r3fix_stable_replay.log]

### 2026-10-20 captured adoption records and current replay

Fresh oct15 final-input capture now requires `live_case.json` to declare oct15
and its package to export matching adopted metadata. It therefore stops under
the adopted oct16 case. Historical snapshot validation checks its captured
receipt's exact bytes without consulting a temporary session directory. The
original final-routing manifest and adoption narrative were relocated byte for
byte to `inputs/oct15_final_routing/manifest.md` and `adoption_receipt.md`.
The old source-directory text remains provenance inside those records.

The oct16 source custody now also includes the readiness validator and its
captured item13 receipt. Current replay preserves all historical outputs:

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/coverage_bound_2026_10_14 \
  "uv run --no-project python3 {lane}/coverage_oct16.py" \
  "uv run --no-project python3 -m pytest {lane}/test_coverage.py {lane}/test_national_keys.py {lane}/test_dependencies.py {lane}/test_oct15.py -q -p no:cacheprovider"
```

The 2026-10-20 replay above passed with **IDENTICAL 113/113**, exit0,
22.862s wall; diagnostic child maxRSS1,757,904,896bytes. Every source producer
and test command returned0, with no uncovered-script exemptions. Receipt prose
is appended after comparison. [CALCULATION: `/private/tmp/scratchfix-coverage-replay.log`]
