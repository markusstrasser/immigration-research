**Verdict:** Reader inventory for R3 coverage and companion repricing; these external readers were inspected, not edited.

## Reader inventory and required follow-through (no edits made)

Searched executable `*.py/*.cjs/*.js` using `rg -l`, then read the located callers. Below, “rerun” means after corrected main-case outputs exist; it does not authorize modifying frozen inputs. Files inside the worker-owned main-case/coverage lanes and `first_year_v8.cjs` are already covered by its brief.

| Reader path | Actual dependency / required update |
|---|---|
| `within_group_distribution_2026_09_29/export_lines.cjs:171-180,435-442,530-546,612-616` | Reads summary's **shared companion ends and band**, payload coverage/mixed metadata, lineage costs and principal counts. Rerun personal outputs after generation consumers; audit shared route: it unconditionally copies mixed metadata, so shared-off item11 requires its `dump`/post-engine values and generation oracle to follow the new companion rule. Counts and frozen parent measurements remain unchanged. |
| `within_group_distribution_2026_09_29/households.py:783-788,1143-1154` | Adds each generation's mixed amount per member, holds unlocated coverage in residual; rerun personal outputs. Shared runs must receive zero mixed post-engine amount and correct personal-priced coverage, rather than silently readding item11. |
| `within_group_distribution_2026_09_29/reporter_b_inputs.cjs:56` | Only requires BASE split without coverage for its initial frozen reporter-parent measurement; do not regenerate/re-freeze for this repricing. |
| `generation_account_2026_09_24/v8_split.cjs:98-110,194-195,323-342` | Scopes item11/12 generation totals and evaluates them, compares live band to summary. Rerun generation set/cash outputs; routing/count declarations do not change. |
| `generation_account_2026_09_24/run_generations_v8.cjs:146-165,181-195` | Reads coverage hash, per-generation populations/adults and scoped costs. Rerun output tables/payloads; population denominators unchanged but per-member values and case hash change. |
| `generation_account_2026_09_24/native_parent_gradients_v8.cjs:49-53` | Requires nonstub final coverage while deriving native-parent perturbations through the package. Rerun derived gradients/provenance; no new placement rule. |
| `generation_account_2026_09_24/allocation_uncertainty_v8.py:110` | Reads generation payload's item11 replicate arrays. Item11 is unchanged centrally, but refresh source hashes/checks after generation rebuild; validate the coverage layer's treatment separately. |
| `main_case_decomposition_2026_09_29/v8_attribution.cjs:27-46,57-70,90-108` | Consumes typed coverage line/capital/production decomposition and item11/12 totals; rerun oct15 decomposition so zero justice-use/capital flows and totals agree. |
| `uncertainty_propagation_2026_09_22/propagate.py:514-554,698,1730-1751` | Reads **v8 lineage companions**, item11 replicates, coverage CPS/PES source derivatives. Rerun oct15 after refreshed coverage caches/receipts; the old point/SE checks intentionally block stale caches. |
| `uncertainty_propagation_2026_09_22/coverage_cps.py:14-84,99-105` | Reconstructs coverage replicate totals from owned cache and gates point/SDR parity. Rebuild owned pricing cache/parity and rerun so removed justice pieces also leave replicate stacks. |
| `uncertainty_propagation_2026_09_22/coverage_pes.py:90-107,150-186,224` | Checks source adapter/hash and cache parity, runs producer's conditional PES derivative. Rebuild its owned pricing cache/manifest through its prescribed recipe, then rerun; do not edit a pin to bypass drift. |
| `historical_backcast_2026_09_20/v8_components.cjs:49,218-225` | Exports updated typed live source components and gates headline against summary; rerun oct15 only. |
| `historical_backcast_2026_09_20/coverage_components.py:30-65,83-107` | Reads coverage file and owned recipe, classifies its named fiscal/capital/production pieces before historical transport; rerun component trace with refreshed source caches, then backcast. |
| `historical_backcast_2026_09_20/backcast.py:832` | Reads generation coverage counts and refreshed component files. Counts unchanged, baseline/source dollars change; rerun live-case backcast outputs, preserving historical case records. |
| `distribution_weights_2026_09_23/case_ends.cjs:47-59,99-102` | Reads exact coverage hash/decomposition to separate public capital and production from the case cost; rerun exported end records before distribution calculations. |
| `distribution_weights_2026_09_23/distribute.py:1172` | Consumes the exported end record's coverage production decomposition; rerun live distribution after `case_ends`, not a source-code repricing change. |
| `debt_legacy_2026_09_23/v8_flow.py:39,353` | Reads typed coverage decomposition and adds item11+12 to current cost. Rerun oct15 flow bridge and dependent debt outputs; fiscal/capital split changes, counts do not. |
| `debt_legacy_2026_09_23/debt_legacy.py:3761` | Checks with-coverage minus without-coverage equals coverage flow; rerun downstream debt tables on refreshed oct15 flow bridge. |
| `world_ledger_2026_09_27/v8_snapshot.cjs:34-42` | Pins all live case output bytes and coverage source after saved/API equality; refresh snapshot through its producer, then rerun live world ledger; never hand-edit frozen snapshot hashes. |
| `nonresponse_bias_2026_10_07/v8_exposures.cjs:5-15,41-45` | Gates saved payload equality and current summary band; post-engine coverage remains fixed in its sensitivity. Rerun exposure export + downstream oct15 outputs. |
| `closed_budget_2026_10_06/households.py:136-137,186` | Places coverage counts proportionally inside generation as an explicit assumption. Counts unchanged; refresh upstream fiscal inputs and rerun live tables, preserving placement caveat. |
| `legacy_comparators_2026_09_30/group_lines.py:136` | Takes item11 total from current payload when building comparator bridges. Refresh inputs/derived oct15 values; no shared companion is consumed here. |
| `legacy_comparators_2026_09_30/legacy.py:200-204` | Uses with/without-coverage population for per-member comparisons. Denominators unchanged; rerun updated fiscal outputs/provenance. |
| `pension_legacy_2026_09_30/pension_legacy.py:613` | Uses case coverage population in cohort accounting; counts unchanged, refresh current case baseline/hash by rerunning oct15 outputs. |
| `sept24_propagation_2026_09_24/band_variants.cjs:353,776` | Requires nonstub oct15 payload and preserves coverage/mixed metadata in variant output; rerun live variants so additive coverage dollars come from corrected source. |
| `sept24_propagation_2026_09_24/real_costs_totals.py:919` | Reads net missing coverage people for denominator; refresh live variant inputs/results, same population count. |
| `service_response_long_run_2026_09_27/congestion.py:76` | Gates matching adopted live payload with final coverage before road sensitivity. Rerun oct15 output/provenance, no road source-key change. |
| `break_conditions_2026_09_29/engine_breaks_sept29.cjs:348-358,481-535` | Delegates live first-year calculation to owned `first_year_v8.cjs` and recomputes lineage/ancestry companions through native case module. Rerun the brief's five-command lane after companion fixes. Its text still says items10–12 held by v8 first-year rules, which should describe their revised individual rules accurately. |
| `break_conditions_2026_09_29/tables_oct15.py:267-273,375` | Reads derived first-year companion output; prose at 375 says items11/12 full post-engine and will be false after fix. Brief excludes this producer until debt/winners inputs exist: flag prose change for its owner, do not run prematurely. |

### Historical readers / nonreaders skipped

- `main_case_2026_10_14/{main_case,api_check,package,generality}.cjs` and `main_case_2026_10_07/main_case.cjs`: source references are historical v7/v6 companion production or historical regression contracts; retain bytes.
- `break_conditions_2026_09_29/tables_oct07.py`: v6 companion reader, not oct15. `engine_breaks_sept29.cjs` remains listed above because it also has an explicit v8 route.
- `white_replacement_2026_09_28/limits_oct14.py`: historical v7 companion prose; no v8 coverage/mixed reader at the match.
- `world_ledger_2026_09_27/{operator_price_bridge.py,beside_extra.py,world_ledger.py}`: “companions” matches describe archived/category-price companions rather than `summary.v8.companions`; the live dependency is mediated by `v8_snapshot.cjs`, listed above.
- `school_peer_checks_2026_09_20/analyze_2011.py`: unrelated input field named coverage.
- Tracked/generated JSON, RESULTs and research prose are output/documentation references, not executable readers; they need the parent's ordinary live-result propagation, not a new producer implementation. Tests are verification consumers and should run with each affected lane; no tests were executed by this read-only scout.


Coverage replicate consumers must call export_pricing.constructed_prices(data, audit), or apply its exact declared excluded-use arrays, after observed-account closure and before C.evaluate. Refreshing an observed-price cache alone does not apply that rule. Named companion totals now use companions.adjustedRun/firstYear; the generic raw payload/options still carry central personal-priced post-engine amounts. Shared summary readers must apply the explicit item11-off companion rule to their own metadata and split outputs.
