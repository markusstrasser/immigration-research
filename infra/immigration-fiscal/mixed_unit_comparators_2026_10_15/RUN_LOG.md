**Verdict:** PASS. Full executable/numeric replay is IDENTICAL 20/20, exit 0; seven tests pass. No Git writes. The final receipt and path inventories are human bookkeeping added after that replay.

- 2026-10-15 02:19:55 JST: source lineage adapter control PASS with zero discrepancy for every part/SE and all signed replicate values. Runtime 73.856s; peak physical footprint 2.329GB. Source policy children match archived union/latent arrays. [CALCULATION: `derived/positive_control.json`; `_cache/timing.jsonl`]
- Comparator preparation stopped on a concurrently invalidated mortality dependency manifest, then passed after the owning lane rebuilt it. No pin was overridden. [CALCULATION: preparation logs]
- The white comparator created four new nonfiler claimant returns, exposing the original state kernel's aligned-registry limit. The adapter uses gated zero-income absent-before rows and canonical actual after-returns; an independent fixture rejects a nonzero booked before liability. [DATA: `derived/white_summary.json` `federal.new_nonfiler_claimants`] [CALCULATION: `test_adapter.py`]
- Comparator own counts use their exact MARSUPWT convention and live row-4 factors. This fixed an actual own-count gate failure without loosening its 0.001-person tolerance; source replicate columns remain unchanged. [DATA: `derived/comparator_weight_rule.json`] [CALCULATION: `adapter.py`]
- The first assembled replay stopped in the finalizer because `adopted` names several response profiles. The finalizer now selects the authoritative profile/variant pair and gates against both exact JSON totals and rounded CSV rows. [CALCULATION: `finalize.py`; `failure-catalog.md`]
- 2026-10-15 02:34 JST: both comparator component and paired-replicate checks pass; six initial regression tests pass. Whites −35.394141 / −17.804446bn, SE 12.075098 / 11.996529bn; Black −2.333671 / +0.646664bn, SE 2.208058 / 2.237184bn, at own counts. Source bytes remain unchanged. [CALCULATION: `derived/{white,black}_summary.json`; test receipt]
- Source integration profiling completed with the full lineage control still exactly identical. The measured hotspot and bounded exact-input replay repair are recorded in `performance-issue.md`; validation of that repair precedes the final rerun. [CALCULATION: `_cache/source_integration_profile.txt`]
- 2026-10-15 02:48:36 JST: full wrapper rc 0 and seven tests pass, but the byte comparison correctly exits 1 (19/20 identical). Only `black_summary.json` differs: a pre-cache state diagnostic 434.6646501739425 vs cached 434.66465017394273bn (about $0.00023); every fiscal amount, SE and replicate file remains byte-identical. No tolerance is changed. The completed producer establishes the cached diagnostic baseline; the full replay is repeated below. Source control still has zero discrepancy across all 122 result rows and all replicate cells, all 119 source files remain unchanged, and the observed peak footprint is 2.476GB. [CALCULATION: `/private/tmp/mixedcomp-rerun.log`; rerun backup diff; `derived/positive_control.json`; `_cache/timing.jsonl`]
- 2026-10-15 02:55:34 JST: complete replay `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/mixed_unit_comparators_2026_10_15 'sh {lane}/run_all.sh'` ends **IDENTICAL 20/20, exit 0**, with no unrun exemptions or EOL exceptions. Seven tests pass. Source positive control still exactly matches all 122 result rows and every replicate cell; all 119 frozen source files are unchanged, and 68 source input pins pass. Final replay peak physical footprint 2.473GB; highest observed producer peak across this task 2.476GB. Both set/cash case sides and the complete denominator close to the exact live JSON at 1e-9 and the rounded adopted/cash_set CSV rows at 5.01e-5bn. [CALCULATION: `/private/tmp/mixedcomp-rerun-final.log`; `derived/{positive_control,source_pin_check}.json`; `_cache/timing.jsonl`; `finalize.py`]

## 2026-10-15 09:57:35 JST, round 4 first full measured pass

All ten new/current own-mask routes completed; finalizer exit 0; 20 tests pass. The original source control retains 122 byte-identical rows and exact numeric/SE/replicate equality. No source pins, original source bytes or Git metadata were changed. [CALCULATION: `derived/positive_control.json`; `_cache/c4_finalize.log`]

Timing hotspot checked before the reproducibility replay: the existing profile in `performance-issue.md` identifies TAXSIM, and exact-input in-process reuse remains enabled. Cold policy processes stay separate to respect the memory limit. Times below are observed individual process elapsed times under concurrent machine work; they are not a matched speedup estimate. [CALCULATION: `_cache/timing.jsonl`; `_cache/*/kernel_cache.json`]

| Tax solve | Seconds | Peak physical bytes | Kernel hits / misses | Retained bytes |
|---|---:|---:|---:|---:|
| lineage | 106.164 | 2250640024 | 4 / 11 | 56124672 |
| white | 45.000 | 2203814672 | 0 / 5 | 43628940 |
| black | 44.729 | 2250574656 | 1 / 4 | 52720380 |
| white_children | 43.065 | 1981287088 | 1 / 4 | 43604316 |
| black_children | 38.623 | 2252294952 | 1 / 4 | 52722540 |
| white_children_round3 | 42.337 | 2030111456 | 1 / 4 | 43593084 |
| black_children_round3 | 42.420 | 2260355904 | 1 / 4 | 52716060 |
| lineage_current | 38.574 | 2243414872 | 1 / 4 | 52825356 |
| lineage_children | 34.760 | 2124139304 | 1 / 4 | 52800732 |
| lineage_without_white_overlap | 41.074 | 2145815408 | 0 / 5 | 52812828 |
| lineage_without_black_overlap | 39.099 | 2240777072 | 0 / 5 | 52806780 |

The full expanded lineage shift, after subtracting item 10's already-booked crossing-credit vector once, is +4.205459738 / +3.795855348bn, conditional paired SE 0.596509658 / 0.590026249bn. This includes the completed reporter mask and repairs source-union-only M5 allocation against latent/expanded departure. The source item 11 plus delta is 14.945476011 / 18.327545546bn, SE 4.411083137 / 4.402606901bn. [CALCULATION: `derived/lineage_children_delta_summary.json`]

Central comparator overlap gates are zero records and zero survey-weighted persons against the authoritative completed lineage. The round-3 membership and both-side half-overlap endpoint interpolation remain beside. Half-gap rows are count/item11-pairing metadata only: direct whole-gap costs belong to the white producer, which applies district prices, coverage and mortality together. [CALCULATION: `derived/{white,black}_children_summary.json`; `derived/gaps.csv`]

## R4C4 final replay receipt — 2026-10-15 10:38:53 JST (`date`)

Full `run_all.sh` under `rerun_lane.py`: **IDENTICAL 52/52, exit 0**, all 22 tests pass; 36 adapter processes, 921.098437333s wrapper elapsed, maximum physical footprint 2,456,914,800 bytes (below 2.5GB). All 122 original complete source result records remain exactly equal; the full 555-row replicate CSV is byte-identical. All 119 frozen source files and 68 source pins pass. Expanded-lineage incremental item11 is +4.205459738 / +3.795855348bn after subtracting the already-booked completion-credit interaction once. Final half-count provenance pins members SHA `638f92a85ba2e21cbd4eabe42976bbdf0c96ff63c296c7ccc8923db3a637898b`. [CALCULATION: scratch prop8/c4fix-mixed-rerun.log, c4fix-mixed-rerun-receipt.json; derived/positive_control.json, source_pin_check.json]
