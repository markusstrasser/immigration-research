# World-ledger execution failures

## Oct15 carrier and capital adapter, 2026-10-15

- Trigger: evaluate corrected and uncorrected generation cells through v8's evaluator.
- Failure: the scenario reader used an unpadded uncorrected model, so its declared completion response named an absent line.
- Repair: pad the uncorrected model with zero synthetic lines. Generation costs still gate against the uncorrected source table; no correction is applied to those zero carriers.
- Second failure: `Consumer.capitalOf` returns `id/key/response/return_bn`, while the old adapter read a nonexistent `stock_charged_bn` from that result, yielding NaN.
- Repair/guard: join stock and the reading's rate from the authoritative capital registry by exact component id; reject missing/duplicate/nonfinite components and require amount × response = return at 1e-9bn.
- Third failure: completion capital carriers can point to a user-fee offset. Those inherit the original capital component's class through `ITEM_CLASS`; they are not missing parent services.
- Regression: `test_phase_c.py` verifies exact-id capital mapping, zero response, nonfinite rejection and offset inheritance; full set/cash core verifies every actual line, generation and band end.

## Missing scientific inputs are distinct from adapter errors

The retained Phase B full-accrual pension gate requires actual histories and a service-cost bridge. A v7 cash artifact cannot authorize an oct15 cash reading. Net-missing coverage has modeled counts and source fiscal prices, but no located household income/Mexico-pay counterfactual. Unknown recipient value is not zero.

The oct15 debt flow closes the corrected case while keeping unlocated federal/state financing as NaN. `debt_current.py` gates total source parts against the principal summary at 1e-6bn and rejects undeclared missing government shares. `test_phase_c.py` checks both failures. Beside theta/MCPF/capital/R&D recipes report `[BLOCKED: no oct15 federal split]`; no oct14 fallback or partial recipe enters a total.

The scoped review reproduced an additional gap: a renamed finite financing category could disappear from the recipe mapping. The mapper now rejects every category outside the producer's six declared kinds and checks each classified federal + state part against its responsive amount. Negative regressions cover category drift and finite-but-wrong government shares.

Coverage source contract: exact authoritative `(end, index, generation, line)` declarations identify known receipt/service/capital parents before any valuation. Its nonzero residual/calibration rows stop with their specific keys and amounts; a source-classified tax is not the scientific blocker. The regression preserves that distinction and writes no value for the unknown residual.

## Phase C step 3 corrections, 2026-10-15

- The parent authorized canonical donor transport and a signed proportional component mix. These supersede the earlier coverage-income/residual stops; full accrual and missing federal financing remain blocked beside. Unknown receipt parents and missing receipt cells still stop (`test_residual_mix.py`, `test_cash_readings.py`).
- The current distribution reader previously checked historical unkeyed log bins against completed-case channels. It now requires completed-case keyed log bins/reference metadata; the original bin-mass gate remains.
- Zero fiscal response cannot identify zero recipient value for public goods. A native donor export now transports defense and applicable road recipient values without changing fiscal costs. Inactive alternative completion carriers receive no recipient value; genuine active zero-response goods retain it (`test_coverage_recipient_values.py`).
- Endpoint hospital-care provider and recipient quantities were mismatched. Both row builders now use the selected end's quantity before V/G; the unit-V/G regression closes each pair exactly.
- The first cash-cell serializer repeated full nested component JSON on each already-expanded row, producing a 3.8GB CSV and failing the peak physical guard at 5.585GB. The scalar runtime drops nested JSON; exact source JSON and the component contract remain separately pinned. `test_component_expansion_has_one_scalar_receipt_per_component` guards closure and bounded scalar representation. Only a later successful full rerun is an admissible result.
- Scope B is the memo's partial counted-member group position beside complete-lineage effects on others. It has no complete-world total/break-even, retains all other-party numeric PPP receipts from s=1, and discloses excluded sender debits. A coverage-off account is a different question.
- A later scalar-output replay still failed at 2.597GB. The same primary IPUMS parent-table construction ran three times in one process. The driver now shares its one small result across both population scopes and constructs it before the wide completed microframe; phase-level physical guards run before publication. The budget remains 2.5GB.
- Parent-table sharing alone did not fix the memory failure (2.638GB in a phase probe). The final repair precomputes and shares the fixed Mexico reference before the US frame and narrows the retained frame to the declared economic columns. The standalone run passed at 2.377GB and preserved every reading byte; complete reproduction must pass independently before completion. Phase guards and the final guard remain mandatory.
- Exact-cash replay caught snapshot contamination from six concurrently created oct16 generation outputs. All numerical cells/checks were identical; only the source list changed. The snapshot now declares the selected case's corrections/results/summaries and models instead of globbing every generation output. Admitted source manifests and loaded module hashes remain mandatory. `test_snapshot_scope.py` proves unrelated-case changes have no effect, selected-source changes do, and missing selected inputs fail loudly. The exact-cash artifact is rebuilt and repinned after this source-scope correction.
- The selector follow-up found date-bound economic filenames, generation-line loading and native recipient-routing paths. Completed-frame output paths now use the case key; exact package set lines feed the cash loader directly; routing manifests, adoption markers and source receipts are selected and hash-checked for that case. Missing future native support fails; no older case is relabelled. `test_case_selection.py` checks preservation of existing outputs, selected native identity, source drift and absent-case failure. A missing module-name qualification caught by its first focused run was corrected before replay.
