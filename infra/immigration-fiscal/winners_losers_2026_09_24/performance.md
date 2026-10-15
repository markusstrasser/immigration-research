**Verdict:** The P7 cut aggregation hotspot was repaired; the external congestion setup remains outside this lane's authorized edit scope.

The first full P7 profile spent 188.758s in repeated demographic filters (315.265s total). The replacement caches group codes and uses NumPy grouped sums. The next full profile spent 25.079s in cut aggregation (114.133s total), with the same national conservation gates and a grouped-sum regression test. [CALCULATION: ignored `_cache/p7_profile.pstat` and `_cache/p7_profile_fixed.pstat`; `inputs/run_receipts.json`]

The base lane's dynamically imported `congestion.py:setup` → `arms.py:match_umr` takes 20–26s per profile. Its repeated `Series.map` callbacks traverse DataFrame attributes for each candidate area. Editing that source is prohibited by this task's lane boundary. A later ordinary run took 185.690s, so wall-time variation is not explained solely by the repaired local hotspot; no CPU-contention cause is claimed. `measured_run.py` now records child user/system CPU alongside wall time to distinguish that on the final rerun. [CALCULATION: `_cache/p7_profile_fixed.pstat`; `_cache/timings.jsonl`]

Follow-up for the owner of `congestion_2026_09_23`: profile `match_umr`, precompute normalized candidate columns once, and demonstrate identical urban-area matches and congestion allocations before adopting a speed claim. No other lane was edited here. [INFERENCE]

## Peak-memory failure and guard

The first byte-reproduction attempt completed the child calculation but failed the 2500 MiB guard at 2652.531 MiB. The guard correctly propagated failure; no byte-identity claim was made. The prevalence calculation retained full floating-point priced arrays although it only needs their signs, and cut rows retained Python dictionaries until final DataFrame construction. The repair stores boolean signs and each cut batch as a DataFrame. The expanded two-payer-pool run is validated under the same unmodified peak-memory guard. [CALCULATION: `_cache/timings.jsonl`; `p7_frames.py`]

The complete-channel run passed at 2159.641 MiB, but took 257.774s (129.160s user CPU). The follow-up full profile passed at 1779.266 MiB, 165.193s; all 163 computational/report artifacts reproduced byte for byte. Its only harness mismatch was the runner source, changed during the run to move pytest's cache inside the lane. The runner is now fixed before the final check. [CALCULATION: `_cache/final_profile.pstat`; `_cache/rerun.log` before final overwrite; `inputs/run_receipts.json`]

That profile spent 42.469s in `cut_rows` across 1305 calls and 23.113s in the out-of-scope `match_umr`. The cut loop repeated identical boolean person slices, winner/loss products and the national dot product for every cut. Those operations are now hoisted once per scenario without changing arithmetic or tolerances. The existing weighted-cut regression and final full byte check validate the repair; no additional speedup is asserted before its final timing receipt. Earlier default pytest calls refreshed the ignored repository `nodeids` cache; the final runner uses `_cache/pytest_cache` within this lane. [CALCULATION: `test_p7_frames.py`; `_cache/final_profile.pstat`; `run_all.sh`]

A later repeat still failed peak RSS at 2546.828 MiB. The primary replicate CSV is now joined in chunks into the same person-major matrix, rather than holding its parser, full source frame and joined copy simultaneously; full-source ID uniqueness and requested-order coverage remain gated. Completed base report tables and Arrow's unused buffers are released before P7. The subsequent expanded build, including conditional SEs at both ends and central, passed at 1986.016 MiB in 154.124s (1049 P7 gates, 511 original gates, 29 tests). The regression covers shuffled joins across chunks and an unrequested duplicate ID. Replicate population denominators are now computed once per payer pool rather than per winner mask; the final full byte check compares all 1305 conditional SEs as well. [CALCULATION: `_cache/timings.jsonl`; `test_p7_frames.py`; `p7_frames.py`]

## Literature-epsilon additions, 2026-10-14

The expanded calculation has 1845 net rows and 280440 cut rows. Its successful build took 150.576s, 117.408s user CPU and 1734.047 MiB peak RSS. An earlier profile took 161.006s and 2070.219 MiB but failed the new preservation gate: it compared unrounded values to a ten-significant-digit CSV. The preservation check now requires exact serialized bytes for all 1305 original rows, including conditional SEs; accounting gates retain 1e-9bn. The prior failure is retained rather than labelled successful. [CALCULATION: `_cache/nest_profile.pstat`; `_cache/nest_build_verified.log`; `_cache/timings.jsonl`]

The profile's cut aggregation is 43.228s for 1845 scenarios, using the existing cached grouping; the already-filed external congestion setup is 22.750s. No new solver bottleneck appeared. New finite-epsilon payer transport uses grouped sums and preserves each state/nativity/skill/signed increment rather than materializing additional microdata frames. [CALCULATION: `_cache/nest_profile.pstat`; `p7_nest.py`; `test_p7_frames.py`]


## Round-2 Phase A, 2026-10-15

The initial 298.616s profile failed fix10's state-price coverage; it exposed missing jurisdiction-exported synthetic lines and a prison geography defect. Repaired source-defined keys, responded spending and explicit degraded school geometry. It spent 59.845s on repeated state allocations and 40.923s on state wage maps. The corrected route caches those within each fixed-payer scenario and still gates each scenario's state totals. [CALCULATION: scratch winners/presence_corrected/phase_a_profile.pstat]

The next 275.608s run failed the original frozen-control gate. Final code review traced an in-place landlord adjustment into cached housing source vectors; an out-of-place sum plus actual-evaluate order-invariance regression repaired the defect. Those two runs are rejected, with failure evidence retained. [CALCULATION: winners/final_phase_a_run.log; winners-code-review.md; test_p8_incidence.py]

The successful final full grid took 239.512s, 204.353s user and 3.072s system CPU; lifetime physical footprint 2.201GB. Source and original 108-row frozen-control gates pass; original tolerances unchanged. RSS remains descriptive; calculation and crossing-credit subprocess enforce the shared physical-footprint helper. [CALCULATION: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_validated/phase_a_timing.json`, `phase_a_gates.json`]


Final source-field refresh at 2026-10-14 17:00:20 UTC: available DIS_SC codes replace the incomplete/broad incidence mapping. Routing regression added. Full profile 234.956s (211.755s user, 3.611s system), lifetime physical footprint 2.199GB; all gates pass. Isolated outputs outside fix2/joint reproduce the interim run, so the cache repair and other incidence fixes remain verified. [CALCULATION: `/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/prop8/winners/phase_a_complete/phase_a_timing.json`; finalizer cross-run comparison]


## Phase B oct15 — 2026-10-15 01:14:56 UTC

Complete byte harness: 121.278s. Its pricing command: 107.346s wall, 67.752s user, 4.534s system; lifetime physical footprint 1.954728GB. [rerun] IDENTICAL: 221/221 files unchanged (backup removed), exit0. RSS is descriptive only. [CALCULATION: _cache/oct15_timings.jsonl; _cache/oct15_rerun.log]

The scoped-gate failure exposed net set/cash timing used as fund accrual. The principal current-flow source places the difference in coverage profile calibration; exporter and negative-control regression now separate these concepts. The unchanged external congestion setup hotspot remains assigned to its source owner. [CALCULATION: test_oct15_core.py; p7_trust_inputs.json timing_bridge; prior performance entries]
