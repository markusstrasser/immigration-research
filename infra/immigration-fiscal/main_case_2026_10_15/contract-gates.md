**Verdict:** Final live case G2 and G3 PASS; sign17/lineage9 gates PASS. Final integrated G5 reproduces45/45 files, exit0 (`_cache/g5_final.log`). The initial failure below is historical and resolved; subsequent evidence is retained in chronological sections.

## Historical initial verdict (superseded)

G3 PASS (STUB module initialization, all v8 items OFF in the tested case); G2 currently FAIL because
the base summary omits v7's `without_capital_return` key. The root owner of main_case.cjs has been notified.

Initial marker: PROBE-IN-PROGRESS.

Contract (G2/G3) and generality checks are being implemented. Outputs are not yet validated.

## Initial checks

**Verdict:** G3 passed on the first probe: v7's own unmodified main_case.cjs, sign_reversal.cjs and lineage_addition.cjs
passed 128 / 24 / 56 gates. All 10 v7 derived output files reproduced byte for byte. The updated resource-reporting
and optional profiling path is now running. G2 awaits the completed v8 derived output set.

G2 fixture probes passed: candidate adopted null and added keys/columns accepted; a missing row, reordered rows and
an undocumented JSON type change each fail with exit 1. Node syntax checks pass for contract.cjs and generality.cjs.

The first G3 run took long enough to trigger the slow-tool rule. The next run uses `G3_PROFILE=1`, placing each
child's CPU profile alongside its logs under this lane's `_cache/g3/`. Timings and RSS are printed, never put into
the deterministic derived gate records. No v7 script is modified; its source SHA-256 is recorded in generality.json.

## Current checks

- G3: 128 / 24 / 56 gates pass; 10/10 files byte-identical. Profiling run: Python `perf_counter` 59.364 seconds,
  `resource.getrusage(RUSAGE_CHILDREN).ru_maxrss` 700,858,368 bytes. Node maxima: main case 684,432 KiB,
  sign reversal 276,736 KiB, lineage addition 491,424 KiB. All are below the 2.5 GB budget.
- The CPU profiles put 63.39% of main-case samples and 54.64% of lineage-addition samples in the inherited
  engine.js:50 `clone`. The measured full G3 rerun is under two minutes; changing the inherited engine lies outside
  this task's lane-only edit boundary. Optional `G3_PROFILE=1` retains a reproducible profiling route.
- G2: all 10 v7 data files, CSV columns and rows preserved. Both adopted-null type changes are documented; additions
  are exhaustively listed in `derived/contract.json`. The sole failure is the absent summary key stated above.
- Gate records exclude only the existing per-lane OWN names. New output files, columns, rows and every JSON added
  key path are listed. No v7 history-key relocation is allowed. G3 preserves exactly v7's original module export keys,
  with v7's own registry / CANDIDATE / NEW_IDS / identity and the new package's guarded caseOf route.
- Covered: contract.cjs, generality.cjs, their deterministic derived records; v7's three scripts and ten outputs as
  read-only references. Skipped: main_case.cjs, package.cjs and item implementations, owned by peers; no review run.

## For the parent

Restore and compute summary.json `without_capital_return` in main_case.cjs; rerun G1 then G2. This is a producer
defect detected by the contract, not a contract exception. Final coverage-on outputs need a fresh G2; G3 tests all
v8 items OFF, so its compared outputs remain v7's. `[STUB]` flags are present whenever coverage stub initialization
is encountered. No old lane is written.

## Every changed path (this agent)

- `infra/immigration-fiscal/main_case_2026_10_15/contract.cjs`
- `infra/immigration-fiscal/main_case_2026_10_15/generality.cjs`
- `infra/immigration-fiscal/main_case_2026_10_15/contract-gates.md`
- `infra/immigration-fiscal/main_case_2026_10_15/derived/contract.json`
- `infra/immigration-fiscal/main_case_2026_10_15/derived/generality.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/contract_fixture.py`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/components.csv`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/corrections.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/corrections_cash.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/lineage_addition.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/lineage_payload.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/lineage_payload_cash.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/main_case_bands.csv`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/per_spec.csv`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/sign_reversal.csv`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/derived/summary.json`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/lineage_addition.cjs.cpuprofile`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/lineage_addition.cjs.log`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/main_case.cjs.cpuprofile`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/main_case.cjs.log`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/sign_reversal.cjs.cpuprofile`
- `infra/immigration-fiscal/main_case_2026_10_15/_cache/g3/sign_reversal.cjs.log`

## v8 companion outputs in progress

**Verdict:** sign_reversal.cjs base PASS (14 gates; old cells preserved; appended oct15 columns). lineage_addition.cjs
implemented; its first full reconstruction confirmed current v8 totals but found $8,452 of non-affinity, so the
final code reports the measured interaction and uses a zero-descendant limit with an explicit 1e-9bn convergence
check and a two-factor Shapley split. It retains all v7 schema paths as explicitly marked history and puts every
current value under v8. The observed nonreporter crossing-credit increment is the source's central-plus-observed
minus one-US-parent-only measurement; carrier welfare effects are negated to report costs.

Current final-run blocker: a peer item_union.cjs optionRates adapter forces cash pension options through the set
API when the source price builder loops both sets. The root has the failing stack and the per-set-default repair
recommendation. No edit outside assigned sign_reversal.cjs/lineage_addition.cjs or this result file was made.

## v8 companion outputs final base check

**Verdict:** PASS, coverage OFF base. The peer's per-set pension-default fix resolved the adapter failure above.

- sign_reversal.cjs: 14 gates pass on the fixed current package. Every v7 CSV cell remains unchanged; `oct15_low`
  and `oct15_high` follow all old columns. Services=1 agrees with minus full v8 proportional-reference cost at all
  64 specifications (max difference 7.39e-13bn), capital and post terms agree exactly, and 96 service-linearity
  checks have max gap 2.56e-13bn. Node maxRSS 276,736 KiB.
- lineage_addition.cjs: seven gates pass. The custom both-count route matches current v8 in both sets exactly.
  The inherited package blocks literally zero descendants; the result states the 1e-5 / 0.5e-5-person limit and
  extrapolation explicitly. Observed convergence is at most 4.64e-11bn (under $0.05), well inside its 1e-9bn gate.
  Original later/G3-rate costs use a two-factor Shapley split; their measured interaction and the old affine
  assumption's disagreement are reported. Newly observed nonreporter source carriers and their incremental
  crossing-credit source amount are separate. All parts and population counts close. The completed reporting-union
  amount is explicitly at case responses with adopted mixed-unit and coverage constructions held, not a fresh
  union response/source run. All old JSON paths remain v7 history, marked in meta; current quantities live in v8.
- Lineage run: Python perf_counter 51.165 seconds; resource.getrusage child maxRSS 566,624,256 bytes;
  Node process.resourceUsage maxRSS 553,344 KiB. Both sources syntax-check successfully. No review run.
- Coverage-on outputs require a rerun after the parent supplies its live coverage file; both scripts print [STUB]
  if using temporary coverage prices.

Additional changed paths in this companion task:

- `infra/immigration-fiscal/main_case_2026_10_15/sign_reversal.cjs`
- `infra/immigration-fiscal/main_case_2026_10_15/lineage_addition.cjs`
- `infra/immigration-fiscal/main_case_2026_10_15/derived/sign_reversal.csv`
- `infra/immigration-fiscal/main_case_2026_10_15/derived/lineage_addition.json`
- `infra/immigration-fiscal/main_case_2026_10_15/contract-gates.md`

## Subsequent timing observation

The provenance-only lineage rerun became slower after the item-10 worker's fresh companion unit-price routing
changed. Each custom-count variant runs item_union.optionRates and the source full unit-band engine route again;
the earlier same decomposition took 51.165 seconds. Root notified before another rerun. This source helper is
owned by the item-10 worker/root, so its cache-key/profiling change is deferred there; no old-lane engine or source
is changed by this companion task. This timing note does not supersede a correctness gate.

**Verdict:** Final provenance-complete base lineage rerun PASS: all seven gates; same totals and zero-limit convergence; maxRSS 568,800 KiB. Both v8 companion outputs are ready for parent integration.

## Native observed-child representation correction

**Verdict:** Sign PASS (17 gates); initial native lineage PASS (nine gates). An optimized-package lineage parity
rerun is in progress. These checks supersede the earlier endpoint-child results above.

`sign_reversal.cjs` exports one `removeObservedChildren` helper used by `lineage_addition.cjs`. It reverses the
314 native observed-nonreporter cell parts named by item10's meta.items record and subtracts that record's actual
P/F production arrays. It retains joint membership-credit edits. Lineage child costs are full cost minus this
removed-child model, including the public-capital difference; the crossing-credit increment remains separate.
No missing endpoint carrier can silently produce a zero child cost.

The sign regression directly prices child removal at services 0 and 0.37, over 32 combinations: native fiscal
cell effects plus P/F less public capital match the sign-route welfare difference within 2.57e-13bn. The child
contribution changes by as much as 0.331bn across those service responses. The services=1 full-cost check and 96
linearity checks also pass. This tests the reviewer-reported fixed-child-charge defect away from the endpoints.

Root identified repeated carrier-by-row scans. The sign wrapper now caches the carrier entries once and builds
receipt/spending maps per first evaluation; direct-native test row lookups use maps too. Optimized sign output
is byte-identical to the previous native run. Wall times were 112.748s before and 67.849s after, with concurrent
work (not a controlled speedup estimate); optimized Node maxRSS 279,056 KiB. The root applied the same map change
in package.cjs. The initial native lineage run passed in 255.351s with Node maxRSS 807,840 KiB; Python's child
resource peak was 939,835,392 bytes. A new parity run checks the optimized package.

## Final native verdict and remaining profile

**Verdict:** PASS for both owned companion outputs on COVERAGE=0. Sign: 17 gates. Lineage: nine gates.
The map changes preserve both output files byte for byte. Optimized lineage elapsed 128.722s, Node maxRSS
1,041,456 KiB; Python resource child peak 1,066,450,944 bytes. All old v7 JSON values were independently checked
unchanged as marked history. Integrated G5 and coverage-on replay belong to the parent.

The remaining >2-minute lineage route was profiled, not guessed. Profile run: 326.017s under concurrent parent
work, Node maxRSS 945,200 KiB, all nine gates pass. Its cache output is byte-identical to the authoritative output.
Self-samples grouped by function/file/line: inherited engine.js:50 clone 21.14%; source added_band_prices.cjs:10
clone 13.96%; v6 item_age_mix.cjs:55 clone 10.30%; v7 package.cjs:75 clone 10.05% (55.45% together). These old
lanes are read-only in this task. New-lane child_records.build takes 4.88%, its add helper 2.62%; item_union.cjs:380
partsAt callback takes 3.99%, with Object.entries(parts).filter repeated per edit. Root notified: preindexing part
entries by edit and caching repeated raw-child constructions are bounded follow-ups for those owners, while the
old-lane clone route requires its own authorized scope. No additional source change or output regeneration is planned.

Final changed paths for this native-child correction (all under main_case_2026_10_15):

- `sign_reversal.cjs`
- `lineage_addition.cjs`
- `derived/sign_reversal.csv`
- `derived/lineage_addition.json`
- `contract-gates.md`
- `_cache/lineage-profile/lineage.cpuprofile`
- `_cache/lineage-profile/lineage_addition.json`
