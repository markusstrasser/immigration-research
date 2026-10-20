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

## Oct16 source consumption, 2026-10-20

- A literal case-key change failed before computation because no v9 pins existed. The explicitly authorized worktree source epoch now has selected SHA256 inputs and before/after verification. Missing reviewed upstream outputs block capture; selected-source tampering fails a negative regression.
- The live distribution frame now arrives with calibrated ranking weights. Applying row4 to them failed its principal population gate. The adapter checks the declared raw/calibrated relationship, restores raw production weights, passes row4, then applies the selected case factor once. The published CPS diagnostic also uses those raw production weights. Synthetic latent G3+ proxy mass stays fixed while actual reporting/completion minors change. Final denominators use population_v9 and the joint coverage_tenure count block, rather than the pre16 coverage counts.
- Count CSVs omit capital response fields. The consumer obtains each response from the actual source generation capital component, including the declared college response; it never treats an empty response as a zero or an arbitrary one. All source cash/set cells close at1e-9bn.
- A shared producer edit correctly invalidated historical donor receipts. The historical coverage producer was restored byte for byte and v9 transport placed in its own module. The frozen oct15 recipient output verifies its original adapter blob at7dfb4c66; it is not regenerated or repinned through v9. Numeric native source hashes and output hashes remain checked.
- Treating every new typed post as omitted-person coverage would remove observed calibration corrections from ScopeB. Count atoms now retain separate observed/constructed source amounts; native zero-response recipient changes do too. The scalar source contract carries recipient_scope, and only constructed pieces leave the counted-member companion.
- Expanded row validation repeatedly built a singleton DataFrame. The profiled scalar finite gate preserves all three field checks; nonfinite regressions and all cell/source closure gates remain active. See performance.md.

### Final v9 source review and regression repairs

- A normal donor build could enroll the current builder/kernel hashes without checking that those bytes belonged to the reviewed source epoch. The traced call chain is `v9_transport.export` → `coverage_oct16.load_kernel` → `coverage_bound.validate_cache_receipt`, then `source_tables.load`, `measure.person_inputs`, `tenure.fixed_count_tenure` and `coverage_bound.factors`. The explicit snapshot now includes the donor adapters, count builder modules and person/factor inputs, coverage import modules, source-table pins and parsed files, both final-routing kernels/audits/manifests and each manifest dependency. Donor export checks admission before importing the source and verifies the same epoch after calculation, before writing outputs. Regressions reject an undeclared required source and a changed algorithm both before and during export; no normal build captures a new source epoch.
- `households.py` retains actual record weights as `w_id` before placing synthetic descendants in `w0`. The recipient-only calibration incorrectly multiplied `w0` by the native-minor factor. It now changes `w_id` only; the existing denominator still prices the original complete service allocation. A regression checks `identified + latent + correction = identified × factor + latent`, so latent descendants remain fixed.
- New capital post rows used response1, which understated public-good attributed value when the actual capital response was below1. Each post now carries its exact source component response, including reporter-parent resolution. The regression checks both general-government components, all generations/ends/sets: base attributed capital plus rate delta equals the same capital at the live rate, while every fiscal delta remains exactly the source generation part.
- The first full v9 regression run found an eager optional recipient-scope lookup on an explicit residual component fixture. Scope metadata is consulted when present; explicit component expansion remains independent of that optional row, while non-component source-parent lookup remains strict. The existing component-expansion regression preserves fiscal and recipient closure.
- The first complete route reached the cash adapter and stopped at the unchanged capped-program source-key gate. Global filtered-row positions in new count IDs differed between set/cash when pension-only rows vanished. Count IDs now use all nonnumeric source semantics and recipient scope; duplicate source declarations retain their within-semantic source-record occurrence, assigned before zero filtering. This occurrence records source order, not a measured unique identity. Noncount IDs use their declared source semantics, including college operating versus fee-offset capital parents, and reject duplicates. Tests insert unrelated zero/pension rows without changing capped IDs, and gate real set/cash capped-program cardinalities and dollars. Every source atom remains separate; no fiscal tolerance changed.
- The source-ID-corrected route passed the actual cash adapter but failed at the economic-frame lifetime guard:10.409GB physical peak. The expansion retained each residual's complete JSON text in every scalar record until after DataFrame construction; pandas/Arrow materialized5,754,954,396 repeated JSON bytes before dropping the column. The adapter now pops that text before scalar expansion. The exact source JSON stays in the pinned artifact and source valuation contract. A constructor-boundary regression rejects nested JSON in scalar records; the actual63,693-row phase then passed at276,579,216 physical bytes with fiscal difference−9.094947017729282e-13bn. A lane-wide decoder/constructor sweep found no second production expansion of this kind. The original failure log/route are retained in `_cache/oct16_stage_09_memory_failure.log` and `_cache/oct16_route_memory_failure.json`; the2.5GB limit is unchanged. Affected stages resume from actual successful source-stable receipts; only the later full normal-route replay establishes whole-lane reproduction.
- The repaired reading passed its economic-frame guard at1,225,934,624 physical bytes, then Scope B rejected an actual2.183-million-dollar end difference in a source-mix employer component. The old exception depended on any `coverage_` prefix, which Scope B intentionally removes. Expansion now carries a marker only from canonical `cls=proportional_mix` source rows. Employer compensation partitions marked and direct subtotals within each generation: both remain finite, direct low/high equality stays1e-6bn, and only the declared source mix can vary by selected end. Regressions cover both recipient scopes, arbitrary JSON without the source class, and a hybrid valid mix plus drifting direct receipts that must still fail. The failed log remains `_cache/oct16_stage_09_employer_failure.log`.

- Temporary session paths in captured historical adoption narratives were
  mistaken for durable dependencies. The narratives and coverage manifest now
  live as byte-preserved Markdown records. Historical source graphs keep their
  original digests and resolve the declared generation-receipt relocation via
  the shared `historical_record_paths.json` map. Frozen native routing checks
  captured receipt bytes; fresh capture uses the live declaration/package
  adoption gate. No historical input is re-enrolled merely because it moved.

- Snapshot setup filtered missing historical dependencies out of its new graph.
  A declared relocation could therefore disappear silently if no resolver were
  applied. Capture now blocks on every missing historical or selected input,
  and source custody includes the validator itself. The case-selection
  regression proves that an absent historical input stops before publication.

- A hardcoded current case plus source hashes did not establish current
  adoption. The normal world route and fresh snapshot/artifact capture now
  call the shared live-key/package gate; frozen verification keeps its captured
  source authority. The fresh-capture regression rejects a stale live key.

- Loading the current receipt-relocation adapter before the historical oct14
  package polluted its frozen module-dependency check: the adapter did not
  exist at the historical commit, so the external-output probe correctly
  stopped. The adapter now loads only inside the later-case branch that uses
  it. Historical package dependency-byte checks remain intact; the existing
  external-output/replay regression passes, and selected-source tampering and
  undeclared-donor controls still fail closed. The runner is absent from all
  four current source/routing/artifact custody records; those records verify
  after the repair without recapture.

- 2026-10-20 review fixes. (1) `reading_cells_cash_oct16.csv` was 259.5 MB, over
  GitHub's 100 MiB limit, and `inputs/pension_cash_cells_oct16.json` 57 MB. The
  cells' growth (7.1 times oct15's rows) is a widened grid, not duplication: the
  same 72 scenarios and 449 lines, with v9's count/tenure coverage components
  carried across every recipient line. Both now ship as deterministic gzip
  (`gz_io.py`); the artifact pin hashes the JSON content, so it did not change.
  `scripts/rerun_lane.py` now stops on a file over 95 MiB. (2) `v9_cells.cjs`
  split count/tenure production into P and F with an unpinned oct14
  union_completion cache; it now keeps those parts in A, as the winners lane
  does, and gates set-basis A/P/F against winners' `fiscal_specs.csv` at 1e-9.
  (3) Tests valuing the oct15 cells rewrote six tracked oct15 coverage files in
  place; `valuation.write_case_csv` now never writes a superseded case's file in
  `derived/` and stops if its recomputed bytes differ.
