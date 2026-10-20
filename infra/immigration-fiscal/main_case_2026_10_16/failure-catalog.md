# Candidate v9 failure patterns

2026-10-20: worker-session files were runtime readiness/adoption authorities; absent item13 prose
silently weakened the completion marker. Captured `inputs/item13_ready.json` and
`inputs/item21_ready.json` now fail closed on missing/stale custody; the package and coverage
snapshot share the item13 check. Consumer adoption uses `live_case.json` plus package adopted
status/date/decision. `test_readiness.cjs`, `scripts/test_adoption_gate.py` and the replay source
scan in `scripts/rerun_lane.py` cover missing/weak/stale receipts, stale live keys and candidate
packages, and prevent source/data from reintroducing session-only paths.
The initial adoption CLI eagerly built the entire v9 package for each Python caller (a failed
preflight alone took 8.95s, with successful full loads substantially slower under concurrent
replays). The package now exports its same declaration through `FISCAL_ADOPTION_ONLY=1` before
scientific construction, in a separate child process to avoid contaminating a consumer's module
cache. G4 compares this projection to the full package's `V9` exports; normal consumers still
validate source custody and build the unchanged scientific account.
The independent review also proved that a mismatched package could pass when a stale live
declaration paired another lane with the requested key. The shared gate now checks exported
`CASE_KEY` and `LANE` as well as status/date/decision; dedicated wrong-case and wrong-lane
controls reject both configurations.

2026-10-20 replay timing: the G1 builder took 664.62s under the concurrent lane workload;
the isolated original v8 `main_case.cjs` G3 producer took 173.953s and passed all 1,776 gates.
The existing phase log locates repeated source-arm/companion pricing, while the retained
G3 bounded-runtime repair above preserves clone isolation and source-byte parity. These
are stage timings, not a sampled new hotspot or a measured speedup. Further scientific
runtime changes are deferred from this portability repair; the full required replay remains
mandatory. Exact command receipts are in the scratchfix handoff, using Python timing/RSS
and the in-process physical-footprint guards.

| Failure | Root cause / repair | Regression |
|---|---|---|
| Inherited viaCandidate rejects new spec fields | v5 checks exact specification identity. Preserve its source-price coordinates; carry effective economic rate in item20 metadata and post-engine revaluation. | api_check retained viaCandidate patterns and raw payload closure |
| Reporter edits differ between model and payload | v8 modelFor leaves corrections metadata empty; item18's source editsAt discovers carriers through that metadata. Route the declared carrier index consistently, then explicitly select source_evaluator (held reporter edits, matching source oracle) or declared_carriers. | G1 source18 oracle; G4 payload/method-mean and shared option parity |
| Brief19's arm name and numeric pair disagree | Delivered immediate_individual has both ends −3.368bn; individual_tangible_normal is −3.368/−0.674bn. Use numeric-intent arm with explicit ITEM19_ARM alternative. | G1 source19 pair and G4 actual default arm |
| Source13 generation builder fails custom lineage | Producer reads canonical v8 generation files. Build its original measurement, reprice its source deltaParts against the variant, disclose canonical source-generation transport; v9 generation evaluator routes its own lines. | lineage addition and lineage companion runs |
| Capital-off college lookup fails | Source15 requires capital components to recover operating use. Reconstruct reference-rate capital on the actual fiscal evaluation to price operating use, then set capital parts to zero. | first-year companion and capital:false option |
| Quoted completion marker clears stub | Substring check also matched a parent's instruction quoting a future DONE marker. Require an exact standalone completion line. | coverage_check marker fixture and package STUB13 |
| G3 exceeded physical footprint despite unchanged source | Full v8 route retains raw pricing arrays through both keyedRatesCache and capture Module.children. In an isolated source-byte runtime, evict raw memo entries above two and unlink only the module whose unitModels is the exact evicted array; preserve scalar memo and active references. Enforce the canonical2.5GB lifetime peak physical-footprint limit; RSS is diagnostic. | guarded source anchors, exact scoped set/cash payload probes and full G3 byte comparisons |
| FRED graph.csv unavailable | HTTP404; canonical /data/DFII*.txt exposes full dated observations. Pin 2024 rows, dates and source hashes; offline replay is default. | market_check.py validates262 weekday rows and250 nonmissing observations |
| Existing generation replay blocked by peer pin | Peer edits to world_ledger population_basis.py invalidate an unrelated actual-credit source pin. Do not alter peer source/pins; preserve failure receipt and rerun after parent reconciles custody. | existing generation run_all replay receipt; new oct16 split closure separately |
| Count-transfer totals referenced the central parts | Coverage override changed dollar totals but retained parts_scenario=joint. Select joint_count_transfer and subtract item16 consistently. | coverage_check full count-transfer typed-parts closure |
| Nondefault source arms looked like complete kernel rebuilds | Own central coverage/count prices were carried while direct source arms changed. Expose structured per-arm transport, source-price exposure and V9_ARM_TRANSPORT=require_own guard; never label these as fresh own-price full counterfactuals. | coverage_check carry/require-own negative probe; summary arm_transports |
| Node memory caller used the wrong helper export | New shared helper exports requireWithinBudget; four callers initially named check. Migrate every Node producer to the actual shared export. | actual source/base/full producer executions, not only syntax |
| A registered beside item leaked into central routes | Selecting all NEW_IDS kept item19 central; coverage also required this optional item and custom lineage rebuilt every registry id. Default ITEM19=0, filter the central selection, make coverage depend only on its seven pricing items, and route custom lineage through the selected ids. Preserve item19 source-alone and explicit beside generation probes. | G1 central changes/21 pairs; G4 absent central block, explicit beside route and identical coverage source; lineage canonical-count closure |
| Coverage adapter dropped an inherited count key | Folding added descendants into G3plus replaced the four-part source count object and removed its added key. Preserve counts_by_generation exactly on its four-part source semantics; expose counts_by_generation_folded separately and migrate the count-transfer consumers. | G2 missing-key negative control; coverage_check four-part closure and folded identity |
| First-year companion retained steady-state replacement veterans | Source item13 does not distinguish horizons; specs encode a long_run:false request as null. Disable its subtraction without a long-run horizon and preserve signed pre-item13 kernel prices to restore all six benefit/medical subblocks, including zeroed prices. | G4 first-year item13 zero and actual response1; coverage military addback closes to the negative source13 coverage delta; per-atom signed-kernel conservation |
| Population coverage metadata remained on the pre-calibration count | with/without totals incorporated16/17 but the inherited coverage field did not. Set coverage to their difference while preserving population_v8 and the inherited four-part coverage construction. | G1 and G4 population parts add exactly to the denominator |
| First-year restoration diagnostic counted an already-responsive pension fraction | The combined compensation line retains means-tested pension in steady state. Preserve negative original delta as first_year_restored_bn before zeroing the military subtraction; sum that field rather than the entire before amount. Actual costs were unaffected. | G4 restoration equals the source's removed noncoverage subblocks |
- Round6 item21 append: the integrator's by_generation and by_generation_bn dictionaries alias one object. In-place additions doubled only the generation attribution; the1e-9 end/generation guard blocked the first build. Replace each view from unchanged source values. The existing typed generation closure remains fail-loud; a focused aliased-input regression checks the helper.
- Round6 item21 memory: complete per-arm kernel copies plus dense military addback matrices exceeded the unchanged2.5GB budget (physical2.604GB, then RSS2.566GB, then physical2.526GB). Keep source rows immutable/share them, export noncentral arm kernels separately with hashes, and store addbacks only on their nonzero military rows. Final coverage replay passed physical1.7786GB; the canonical guard and RSS diagnostic remain.
- Round6 newly typed capital rows: a zero military addback still evaluated a spending response lookup for health_sl. Skip zero addbacks before lookup and reject non-spending nonzero addbacks. G4 exercises first-year item21 spending/capital, and the six-subblock restoration/coverage gates remain.
- Round6 API horizon probe: first-year specs require their matching first-year model, including roads/property identity. Build modelFor with the same options for both methods; compare each to its own military source parts. The full G4 first-year checks exercise this route.
- Round6 horizon class: sign_reversal's hand-built post specification used long_run:null for a steady-state service-response sweep. Item13 correctly interprets inherited null as the first-year horizon, so the full-cost reference gate exposed a20.995337353bn discrepancy. Declare long_run:true for that steady-state sweep; keep its continuous capital/service coordinates unchanged. All64 reference, preserved v8 columns and linearity/native-child gates then pass. Real first-year specs still come from specsFor(long_run:false), with matching models in G4.
