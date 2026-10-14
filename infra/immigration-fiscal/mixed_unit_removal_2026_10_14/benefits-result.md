**Verdict:** Withhold M4 from the adopted stack. Conditional SNAP changes are −$1.070bn (SE $0.168bn) with existing participation and zero shelter deduction, and −$0.069bn (SE $0.136bn) at the shelter deduction limit. A full-takeup proxy reaches −$5.606bn; that assumption is unmeasured. Medicaid/CHIP spending changes and ACA premium-credit changes remain unidentified. Report the parent's adopted stack as partial. [CALCULATION: `benefits.py` → `derived/benefit_results.json`] [INFERENCE]

## Conditional results against v7

Positive raises removal net cost. SNAP transfers respond at 1, so each listed adjustment applies equally at both personal end specifications and in the set and cash set. These are alternatives, not additive components. [DATA: `assumption_explorer_2026_09_21/derived/model.json`, SNAP `response_class=household_transfer`; `engine.js:40,165`] [ASSUMPTION: everything else in v7 held]

| SNAP scenario, $bn | Both ends | SE | G1 | G2 | G3+ | $5bn review bar |
|---|---:|---:|---:|---:|---:|---|
| Existing participation, zero shelter deduction | −1.069501 | 0.167594 | −0.222760 | −0.312886 | −0.533855 | Below |
| Existing participation, maximum shelter deduction | −0.069010 | 0.136142 | −0.140887 | +0.045511 | +0.026367 | Below |
| Full-takeup proxy, zero shelter deduction | −5.605722 | 0.430881 | −1.252932 | −1.906079 | −2.446711 | Above, conditional |
| Full-takeup proxy, maximum shelter deduction | −3.648852 | 0.374516 | −0.964076 | −1.250873 | −1.433903 | Below |
| Broad program-value envelope, lower end | −46.060718 | 1.541386 | −6.216669 | −14.383465 | −25.460585 | Inconclusive envelope |
| Broad program-value envelope, upper end | +2.046602 | 0.228351 | +0.152161 | +0.854607 | +1.039834 | Inconclusive envelope |

[CALCULATION: `derived/benefit_results.json` `summaries`; 160 SDR replicates, SE of the summed generation vector, not sum of generation SEs]

These results cover 2,252 all-civilian mixed SPM units outside Alaska, with 6.936M surviving people. The complete frame has 2,331 mixed units: 26 Alaska units and 58 units containing non-civilians are excluded from priced scenarios, with five units overlapping those exclusions. Alaska's urban/rural SNAP schedule cannot be located in CPS. Medicaid diagnostics cover all-civilian mixed units including Alaska. No mixed-unit observations locate the 3.04M added descendants; the whole 42.75M lineage adjustment is therefore unidentified, not extrapolated from G3+. [DATA: `derived/benefit_results.json` `frame`] [INFERENCE]

## Rules and calibration

The script parses the pinned USDA FY2024 and FY2025 income, allotment, deduction and minimum-benefit tables. Calendar 2024 uses nine months of FY2024 and three of FY2025. Formula rates and the medical-expense floor come from the 2024 CFR, not typed tables. [SOURCE: URLs and SHA256 in `inputs/benefit_pins.json`; USDA files linked in `inputs/benefit_sources.json`; 7 CFR 273.9, 273.10]

For each SPM unit the modeled gross income is `SPM_TOTVAL`. Removing members subtracts their own `PTOTVAL` and retains the SPM-versus-person income residual. Earned income is wages plus business/farm income. Standard and earned-income deductions follow the sources; medical deductions apply only to elderly/disability-proxy units. SPM child-care, medical and child-support expenses are prorated by persons remaining. Shelter is varied between zero deduction and the maximum allowable deduction (uncapped elderly units use all remaining net income). These are explicit assumptions about missing costs, not observed deductions. [DATA: CPS ASEC 2025 fields in `PERSON_COLUMNS`] [ASSUMPTION]

Before-removal reported annual benefits are preserved exactly by adding the CPS residual to the schedule change: `after = max(0, reported + rule_after − rule_before)`, capped at the surviving unit's calendar-year maximum. Existing-participation scenarios permit benefits only in units reporting SNAP before removal; full-takeup proxies permit modeled increases in units without reported benefits. The retained residual can keep some benefits where the coarse annual-income rule alone finds no eligibility; this is residual calibration, not a claim of statutory eligibility. [CALCULATION: `benefits.py::compute`] [ASSUMPTION]

The raw national proxy is a poor receipt model. Of $45.904bn reported SNAP on wholly civilian SPM units, $17.201bn fails the zero-shelter proxy income test; $7.296bn fails the maximum-shelter proxy test. Raw zero-shelter scheduled benefits are $77.164bn; the maximum-shelter case reaches $509.283bn. These are diagnostic simulations of entitlement before takeup, not valid forecasts of spending. Residual calibration reconciles reported levels; it does not validate the counterfactual changes. [DATA: `derived/benefit_results.json` `calibration.baseline_fit`] [INFERENCE]

The account's SNAP key is `SPM_SNAPSUB / SPM_NUMPER`, the same under both allocations. Its national total on row-4 weights is $45.956bn and its published-weight member share reproduces `model.json` at 0.148149839694, within 5e-9. The $97.391bn national account line, multiplied by the stored household fraction and divided by each replicate's original national key, converts CPS flows to account flows; full-weight conversion is 2.098143 account dollars per CPS dollar. This is the fixed original key translation; a counterfactual is not renormalized to preserve national benefits. [CALCULATION: `benefits.py::compute`] [DATA: `full_account_spending_2026_09_20/builder.py:198–207`; `model.json`; `backtest_admin_totals_2026_09_28/derived/prediction_audit.json`]

Each unit retains its original mean person weight as its event weight. Survivor person weights are unchanged. The post-removal benefit is divided across surviving people to conserve that event-weighted unit total independently for the full sample and every replicate. The adjustment equals original spending attributed to nonmembers minus spending after removal; original member costs already in v7 are thereby excluded. Generations receive the adjustment by removed members' weight shares within the unit, independently per replicate. Neither SPM head nor tax head determines the total. [CALCULATION: `benefits.py::attribute`] [ASSUMPTION: attribution convention]

The broad SNAP envelope allows the surviving unit's benefit to lie between zero and its statutory maximum. It does not impose the annual-income proxies or assume participation. It remains conditional on SPM assistance-unit membership, the unit event-weight convention and original account scaling; it is not an identified confidence interval or a bound on all of M4. [CALCULATION: `benefits.py::compute`] [ASSUMPTION]

## Medicaid, CHIP and ACA

The CMS table is the principal MAGI income-threshold snapshot as of December 1, 2023, held across 2024. Thresholds, the five-percentage-point MAGI disregard and 2024 FPL tables are parsed from the primary files. Child Medicaid plus separate CHIP thresholds vary by state and age band, including California and Minnesota's statewide infant footnotes. Adult thresholds use the higher of expansion and parent thresholds; the parent proxy is an adult sharing an SPM unit with a child. Minnesota and New York's BHP range is not priced as Medicaid. [SOURCE: `inputs/benefit_medicaid.html`, `benefit_magi_law.xml`, `benefit_fpl24_fr.pdf`] [ASSUMPTION: frozen snapshot, SPM-income household proxy]

| Income-eligibility proxy, surviving nonmembers | Adults | Children |
|---|---:|---:|
| Newly eligible, persons | 353,167 | 330,073 |
| SE, persons | 33,928 | 46,838 |
| Lose eligibility, persons | 65,980 | 35,703 |
| SE, persons | 13,755 | 11,478 |
| Reported coverage before, persons | 638,139 | 619,196 |
| Reported covered but proxy-ineligible before, persons | 493,684 | 186,501 |

[CALCULATION: `derived/benefit_results.json` `Medicaid_CHIP.groups`]

These are income-test proxy transitions, not legal eligibility determinations or enrollment changes. The adult baseline mismatch alone prevents adopting them as predicted benefit changes. Legal MAGI family composition, income exclusions, monthly income, immigration qualification, pregnancy, non-MAGI routes, state changes during 2024, special CHIP counties, age-19/20 and demonstration routes, and continuous eligibility are not fully observed here. Seniors/disability-route proxies are excluded from the transition calculation: 1.004M surviving people remain unsupported. [DATA: `derived/benefit_results.json` `Medicaid_CHIP`] [SOURCE: 42 CFR 435.603, CMS table notes] [INFERENCE]

The existing Medicaid/CHIP spending key is the fixed MEPS Medicaid payer mean by age and US birth, transported to every matching CPS person with reference exposure. It is not a function of CPS `MCAID`, income or simulated eligibility. The preferred `medicaid` key differs from the alternative `medicaid_covered` count. Therefore Medicaid/CHIP spending is held numerically, and its actual counterfactual change is explicitly unmeasured. No multiplication of newly eligible people by average enrollment cost is adopted. [DATA: `full_account_spending_2026_09_20/builder.py:212–227`; `admin_benefit_keys_2026_09_24/cps_keys.py:95–109`; `model.json` `medicaid_and_chip_other_medical`] [INFERENCE]

ACA PTC cannot be recomputed: CPS lacks the Form 1095-A enrollment premiums, second-lowest-cost silver-plan premium, APTC paid and monthly marketplace enrollment, as well as complete employer-coverage affordability and legal tax-family MAGI. Form 8962 requires those policy-month inputs. ACA spending is held and the missing effect is labeled unidentifiable. [SOURCE: `inputs/benefit_ptc24.pdf`, IRS 2024 Form 8962 instructions] [DATA: inspected `pppub25.csv` and `hhpub25.csv` schema] [INFERENCE]

## Gates, validation and reproduction

15 tests pass: source-hash failure, primary-table dimensions, statewide infant footnotes, zero-income maximum, sizes above eight, gross/net boundaries, elderly net test, shelter monotonicity, small-unit minimum, 160-replicate contract, generation conservation and row permutation, nonconstant-unit-field guard, partial-stack disclosure/envelopes and baseline-share positive control. The source includes 132 negative SDR replicate weights; they are preserved, not clipped, and a regression test covers signed moments. [CALCULATION: `test_benefits.py`]

Baseline national member-plus-other closure is 4.12e-13bn. Every scenario's generation vectors close to its national change within 1e-6bn. The source CPS SHA256, replica joining, row-4 population/raking and the original account SNAP share are checked before simulation. No tolerance was loosened. Compile checks pass. [CALCULATION: `benefits.py` and the reused `credits.py` frame gates]

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_removal_2026_10_14/benefits.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_removal_2026_10_14/test_benefits.py -q
```

The parent runs the combined `rerun_lane.py` gate after peer scripts stop changing. Standalone output is the owned `derived/benefit_results.json`; performance is printed separately to keep it deterministic. [CALCULATION]

## Covered and skipped

Covered: primary-source rules and pins; all mixed SPM units classified; SNAP schedule/deduction/takeup sensitivities; full and 160-replicate generation arrays; reported-value calibration diagnostics; Medicaid/CHIP income-test proxies and reported-coverage mismatch; the account's key translations and no-double-count sign.

Skipped with reason: Alaska SNAP pricing (urban/rural geography absent), units with non-civilians (out of this all-civilian unit counterfactual), exact SNAP household/status/assets/BBCE/ABAWD/student policy and shelter costs (CPS lacks legal or monthly inputs), exact MAGI and takeup changes (missing family/status/coverage histories), ACA PTC dollars (missing policy-month premiums), added-lineage extrapolation (no linked mixed units). M1–M3/M5–M6 and shared driver/result are owned by peers, not edited here.

## Log

- 2026-10-14: old USDA memo URLs returned 404 and the eCFR API returned 406. Resolved actual table URLs from USDA's live COLA page and used the official 2024 govinfo CFR files. No inferred constants substituted.
- 2026-10-14: Census geography request returned an HTML “Missing Key” response. Reused the existing archived primary ACS 2020 response for stable state-name/FIPS joins; the archive is copied and hashed locally. Schema guards reject malformed data, and the source-hash test rejects substituted error pages.
- 2026-10-14 20:39:36 JST: full execution exit 0, 11.119 seconds wall, peak RSS 1.981GB by `time.perf_counter` and `resource.getrusage`; 14 tests pass, 0.73 seconds. Earlier clean execution was 9.480 seconds, 2.010GB. No `/usr/bin/time`, `ps` or `sysctl` used.
- 2026-10-14: added source-parsed elderly/senior age constants and the statewide infant footnotes. Final full execution exit 0, 24.179 seconds, 1.583GB; 15 tests pass, 0.71 seconds. SNAP unchanged; newly income-eligible child proxy updated to 330,073.

## Every path changed by this worker

All paths below are relative to `infra/immigration-fiscal/mixed_unit_removal_2026_10_14/`:

- `benefits.py`
- `test_benefits.py`
- `benefits-result.md`
- `derived/benefit_results.json`
- `_cache/benefit_results.json` (earlier diagnostic output; ignored)
- `inputs/benefit_sources.json`
- `inputs/benefit_pins.json`
- `inputs/benefit_states.json`
- `inputs/benefit_snap24_max.pdf`
- `inputs/benefit_snap24_max.txt`
- `inputs/benefit_snap24_income.pdf`
- `inputs/benefit_snap24_income.txt`
- `inputs/benefit_snap24_min.pdf`
- `inputs/benefit_snap24_min.txt`
- `inputs/benefit_snap25_max.pdf`
- `inputs/benefit_snap25_max.txt`
- `inputs/benefit_snap25_income.pdf`
- `inputs/benefit_snap25_income.txt`
- `inputs/benefit_snap25_min.pdf`
- `inputs/benefit_snap25_min.txt`
- `inputs/benefit_medicaid.html`
- `inputs/benefit_magi_law.xml`
- `inputs/benefit_fpl24.pdf`
- `inputs/benefit_fpl24.txt`
- `inputs/benefit_fpl24_fr.pdf`
- `inputs/benefit_fpl24_fr.txt`
- `inputs/benefit_ptc24.pdf`
- `inputs/benefit_ptc24.txt`
- `inputs/benefit_snap_benefits.xml`
- `inputs/benefit_snap_deductions.xml`

No git metadata changed. No edits to frozen case files, other lanes, shared driver/result or peer files.
