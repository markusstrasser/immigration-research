# Immigration material repair report — 2026-09-05

**Assessment:** The audit found material errors in both the local fiscal calculations and the arguments drawn from published research. The person-level fiscal model has been rebuilt, the invalid conclusions have been corrected or withdrawn, and a separate recent-evidence pass has added data and competing mechanisms. Final warehouse validation is recorded below. Unidentified effects remain uncertain; successful repairs do not certify an entire literature error-free. [SOURCE: code, primary-source checks and validation artifacts linked below]

The [initial audit](immigration-conceptual-audit-2026-09-05.md) and [decision](../decisions/2026-09-05-material-inference-repair.md) define the starting findings. The [current synthesis](immigration-economist-dismantling-2026-06-25.md), [confidence ladder](immigration-confidence-ladder.md) and [theory re-adjudication](immigration-theory-verdicts-2026-06-25.md) supersede the affected historical conclusions.

## Recalculated fiscal results

The model matches **ACS 2023 adults aged 25–64** to **SIPP person-year donors for calendar 2023**. Its outcome is employee OASDI/HI payroll proxy minus allocated SNAP, TANF and individual SSI. It excludes income taxes, employer contributions, most other taxes, medical spending, pensions and most services. Selected transfers are not exclusively federal. It is a synthetic descriptive accounting projection, not observed group-specific tax returns, a complete fiscal balance or a causal welfare estimate. [SOURCE: `build_federal_microsim_sipp_2024.py`, [Census inputs and definitions](immigration-dataset-register.md)]

| ACS recipient population | Weighted adults | Partial payroll-minus-benefits proxy per adult/year, 2023 dollars |
|---|---:|---:|
| Mexico-born | 8,520,718 | **$2,371** |
| Native non-Hispanic white | 93,555,066 | **$4,033** |
| All foreign-born | 33,587,103 | $3,661 |
| Foreign-born, less than high school | 7,686,859 | $1,665 |
| EU27-origin grouping | 1,447,025 | $5,082 |
| UK-born | 422,849 | $5,705 |

[DATA: `fiscal.v_three_layer_annual` in the rebuilt unified warehouse; exact values in `three_layer_annual_2023.csv`; [checked-in query](../queries/immigration/union_01_three_layer_annual.sql). Rounding does not represent statistical precision.]

The native-white/Mexico ratio is **1.70** under this specification. The old $1,519 and $2,746 figures and their downstream totals were invalid. Correcting them is not evidence for a general ethnic fiscal ranking: foreign-born donors pool origins and native donors pool races, conditional on coarse age, education and income cells. Group-specific participation and unmeasured differences need not transport. Similar within-education means are not proof of equal wages or of education's causal contribution. [DATA; INFERENCE]

The school construction gives approximately **$11,635 per Mexico-born adult** only under a declared household exposure scenario: all household children aged 5–17 are treated as public pupils and their average school costs are allocated across foreign-born household adults aged 25–64, including mixed-nativity households. It is not actual public enrollment or marginal cost, and it attributes all those children's exposure to the selected adults. Average cost can lie above or below marginal cost. The resulting arithmetic difference, about **−$9,264**, is therefore **not a measured net fiscal cost**. A comparable native school construction is unavailable; its school/net cells remain NULL, as do EU/UK school cells failing coverage checks. [SOURCE: tensor construction and [school memo](immigration-school-burden-per-adult-2026-06-15.md)]

## Material implementation repairs

| Error | Correction and practical consequence |
|---|---|
| Household donor totals copied to individual recipients | Annual person earnings, December person weights, and once-only benefit-unit allocation. Allocate SNAP/TANF over covered members, including children, before selecting adult donors; SSI stays individual. |
| Incorrect SIPP education and nativity | Official EEDUC groups; monthly age; citizen-at-birth people born abroad/island areas classified consistently with ACS. This changes the donor population, not just labels. |
| Wrong reference-year cap and tax aggregation | Reference 2023: `0.062 × min(max(annual earnings,0),160200) + 0.0145 × max(annual earnings,0)` per person before averaging. Medicare remains uncapped; this is a wage-equivalent proxy, not actual self-employment liability. Preserve business losses in income. |
| Missing or mismatched recipients hidden by joins | Build recipients from raw ACS with ADJINC-adjusted personal income; invalid/unmatched cells fail. Retire four old household-based tables and migrate executable consumers. |
| Unsupported fine donor cell | Globally combine the two upper income bands for both populations: **64 cells each, zero unmatched recipients**. Preserve sufficient statistics and disclose sensitivity; see below. |
| Health age and population mismatch | Correct 35/45/55 boundaries; label MEPS birthplace as an imperfect proxy for ACS/SIPP nativity; unknown birthplace stays unknown. Missing health cells fail. Health profiles do not condition on SIPP education/income. |
| Alternative scenarios summed | Preserve scenario identity and price units. CBO's $9.2B direct and $9.8B potential state/local measures stay separate; they are not $19B. Alternative payroll multipliers no longer double adult counts. |
| Incompatible quantities treated as a fiscal total | Remove per-pupil dollars from per-adult rows; keep 2012-dollar NAS lifetime NPV separate from 2023 annual stock accounting. Payroll sensitivities hold transfers fixed and are not estimated GE effects. |
| Annual effect loaded as NPV | Colas–Sachs's approximately $750 **annual, 2017-dollar** result moves to its own annual table. Unverified NRC price-year seed is unavailable rather than a fabricated 2012-dollar number. |
| Receipts and assumptions presented as measured mechanisms | Preserve both Mexico and US remittance **receipts**, with country/direction guards. NAS already models emigration; extra exit multipliers are assumptions, not empirical origin estimates. Clemens's capital-tax adjustment is partial equilibrium. |
| Mined claims/proposals treated as validated findings | Preserve them as `unverified_extraction` and `unadjudicated_proposal`. Source-incentive scores are heuristics, not truth probabilities or evidence weights. |
| Local cost scope and fragile regressions | Correct millions-per-100,000 units; selected eight-state OLS gets HC3 and leave-one-out diagnostics. Mixed city/state budgets/actuals are gross selected amounts, not a national net attributable cost. Housing screens keep fixed dates, real missingness and descriptive interpretation. |
| Stale fallback replaced current data | Seven shared lifetime tables now copy canonical context sources, with state-key and completeness checks. An older 100-row state CSV with 44 missing state keys cannot replace the current 55-row table. Missing required authority fails the build. |
| Sweep generator recreated rejected assumptions | Remove assumed average-cost bounds and alleged empirical exit multipliers; label configured claims as unverified candidates. Derived diagnostics go under `DERIVED_ROOT/sweeps/`, with readable-source failures propagated, rather than appending fresh claims to a corrected historical memo. |

[SOURCE: changed builders and regression fixtures in `infra/immigration-fiscal/`; [CBO state/local report](https://www.cbo.gov/publication/61256); [lifetime generator corrections](immigration-lifetime-fiscal-generators.md).]

**Support and precision:** The harmonized SIPP sample contains 3,017 foreign-born and 14,324 native donor person-years. The unsupported fine cell covered 25,571 foreign-born ACS adults. Global coarsening changes the matching specification for 8.10M foreign-born adults. Holding the originally supported population fixed, the foreign-born mean changes from $3,608.39 to $3,657.82 and the native-white mean from $3,960.36 to $4,033.42. Mean absolute recipient reassignment is $588.05 and $736.72 respectively. Those are sensitivity diagnostics, not confidence intervals. The smallest pooled donor cells contain seven and nine people; complete coverage does not establish precision. The [support decision](../decisions/2026-09-05-person-donor-support.md) records the choice and assumptions. [DATA: [pooling validation](../.scratch/repair-validation/pooled-donors/pooling_validation.json)]

## Literature, causal and economic repairs

All seven author memos now give the strongest supported argument before correcting our earlier rebuttals. The most consequential changes are: Cato's separate descendant calculation includes both costs and taxes; a falling population mean can coexist with every incumbent gaining; constant returns does not exclude complementarity; our illustrative three-billion-mover calculation gives **20.45%, not doubling**; the published Ottaviano–Peri wage result differs from its earlier draft; conditional intergenerational mobility is not refuted by unequal starting incomes; NAS's annual generational balances are not successive lifetime returns; and inventor authorship is not spillover attribution. Exact quotations and superseded text are retained. [SOURCE: [seven-author assessment](immigration-economist-dismantling-2026-06-25.md)]

QWI has no nativity variable and its earnings outcome is not native hourly wages. Staggered-policy estimates and selected-state correlations cannot be upgraded to those effects. Nonsignificance is not equivalence; failed robustness software returning zeros is not robustness evidence. Housing supply correlations do not identify immigration demand effects. Receiver destinations, population bridges and capacity denominators need defensible geography and counterfactuals; falsified threshold patterns stay falsified. Repeated cohort cross-sections do not identify individual assimilation paths or immutable traits. [SOURCE: current [confidence ladder](immigration-confidence-ladder.md), [cost analysis](immigration-costs-causal-analysis.md), [receiver assessment](immigration-receiver-node-kill-test-2026-04-23.md), [assimilation assessment](immigration-sociology-frontier-2026-06-25.md)]

Crime comparisons retain offense, arrest/conviction/victimization outcome, denominator, place and generation. Adding second-generation people to the native comparator raises it relative to third-plus-generation natives only if the second-generation rate is higher than the latter—not merely higher than first-generation immigrants. Lower aggregate crime does not algebraically guarantee less incumbent victimization. These corrections neither establish nor reverse an empirical immigration effect by themselves. [SOURCE: [crime assessment](immigration-crime-rates-unauthorized-vs-native-born.md), [recent narrative counterexample](immigration-recent-narratives-2026-09-05.md)]

GDP, wages, profits, rents and taxes overlap. A welfare calculation must specify whose welfare, the counterfactual and horizon, then count resource changes and transfers consistently. Positive aggregate surplus does not mean everyone gains; hypothetical compensation does not mean compensation occurred. Local costs also do not refute a national benefit without completing the same ledger. [INFERENCE: accounting; [economic foundations](immigration-fiscal-welfare-ledger-map.md)]

## Recent data and competing explanations

The June 5–September 5 refresh procured BLS nativity outcomes, county building permits and an ICE detention archive, and audited existing BEA transfer data. It reviewed body-level material from **seven** primary papers/reviews or dated revisions, archived five PDFs, and examined recent essays, news and a selective official-API sample of **207 distinct X posts**. The local API tally is $1.130; vendor billing is unverified. Acquisition dates, observation periods and publication/revision dates remain distinct. [SOURCE: [datasets](immigration-dataset-proxy-refresh-2026-09-05.md), [papers](immigration-recent-papers-2026-09-05.md), [narratives](immigration-recent-narratives-2026-09-05.md)]

The [framing refresh](immigration-framing-refresh-2026-09-05.md) integrates the useful new angles: work rights and formality, investment and adjustment time, housing demand and supply together, incumbent victimization, demographic composition, and institutional policy choices. The August neighborhood crime paper reports different directions by offense, rather than uniformly null or favorable associations. Its indexed publisher text supports design and directional findings; a readable PDF and coefficient tables remain unavailable. Some paid essays are also only previews. Unverified numerical claims are not adopted. These sources support more precise questions, not a universal policy sign.

## Validation and remaining limits

**Completed:** **33** focused regression tests pass, including actual ACS joins, nonlinear annual tax caps, benefit conservation, nativity, missing-data failures, education comparators, scenario separation, annual/NPV units and source-authority regressions. All **17** checked-in headline query files pass (**19 statements**), with no optional skips, in the promoted canonical warehouse. All **nine** additional sweep diagnostic queries pass; **21** changed Python files compile. Raw ACS/SIPP, state-cost and housing inputs were used for the affected rebuilds. A code-review scout covered all 23 files in its packet; subsequent fiscal review found the alternative-scenario and source-authority defects and supplied passing regressions. [SOURCE: [test log](../.scratch/repair-validation/tests.log), [final validation](../.scratch/repair-validation/final-validation.json), [diagnostic checks](../.scratch/repair-validation/final-static-checks.json)]

**Review dispositions:** shared-view drift, unmatched-health omission and malformed-JSON skipping were fixed. The alleged birthplace padding errors were rejected after inspecting the actual dimension and recipient codes; ordinary file-open failures were not silent fallbacks. Cross-review also corrected the new BEA falsifier: program categories cannot identify recipient nativity. Cosmetic suggestions were not treated as scientific findings.

**Empirical limits retained:** no survey-design confidence intervals for the synthetic donor estimates; coarse cross-population transport; incomplete all-government fiscal accounts; school exposure instead of measured marginal enrollment costs; no newly identified national causal crime or wage effect; and no raw assimilation or MEPS re-estimation where source files could not be located. Existing MEPS spending means are retained with corrected labels and bridge scope. These are explicitly unavailable inferences, not errors concealed by a successful test suite. The LLM-assisted selection and review may still miss evidence. [INFERENCE]

## Validation closeout

Four repaired databases and 20 derived outputs have been promoted after comparing the original database hashes with preserved backups. No peer database change was overwritten. The shared state table is again the canonical 55-row state/territory table, and all shared context/lifetime table contents agree. The unified warehouse contains 120 source objects and 366,583 rows; the unrelated sweep warehouse is unchanged. [DATA: [promotion manifest and final queries](../.scratch/repair-validation/final-validation.json)]

**Current data:** `warehouse/immigration.duckdb`; SHA256 `0dcfbabf744e321554db25000b30520117339f2f4f4701092c0ebfe4b0bad6ac`. **Derived output root:** `/Volumes/2TBPNY/research-data/immigration-fiscal/derived`. **Preserved originals:** `.scratch/repair-validation/warehouse-before/`. The ignored local configuration now uses the real mounted roots; broken historical symlinks are not treated as evidence that raw data are absent.

Run the durable checks from the repository root:

```sh
uv run --with duckdb,pandas python3 -m unittest discover -s infra/immigration-fiscal/tests
queries/immigration/run-queries.sh
uv run --no-project --with openpyxl python3 infra/immigration-fiscal/acquire/refresh-frontier-20260905.py
```

The acquisition replay verifies cached source hashes and requires the declared BEA source on the SSD. Live mutable downloads may change vintage; that is not the same as reproducing the preserved snapshot. Test logs, source bytes, databases and other derived validation artifacts are gitignored; their local links require the files or regeneration in another checkout. The tracked builders, queries, tests, source references and interpretation changes remain the reproducible record.

## Revisions

- **2026-09-05:** Opened this repair record under the [material inference decision](../decisions/2026-09-05-material-inference-repair.md). No public publishing or sharing action is part of this repair.
- **2026-09-05, closeout:** Replaced the invalid fiscal estimates with validated person-level outputs, corrected the final stale-source regression, promoted the rebuilt warehouses, and integrated the recent evidence. The documented empirical limits remain outside the conclusions supported by these data.
