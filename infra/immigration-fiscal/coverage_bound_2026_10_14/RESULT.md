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
