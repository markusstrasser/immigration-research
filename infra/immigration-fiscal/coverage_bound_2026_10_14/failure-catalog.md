# Coverage execution failures

## 2026-10-15: profiler hides a failed physical-memory guard

The standard `python -m cProfile` entry returned exit 0 after pricing's physical-footprint guard raised `SystemExit`. Old scientific artifacts therefore existed despite a failed launch. A successful launcher status and unchanged artifacts did not prove the guarded run succeeded. The preserved profile is `_cache/stdlib_masked_exit.prof`. [CALCULATION: observed guarded export and status probes]

`export_pricing.py --cpu-profile` now enables profiling inside a `try/finally`, writes the profile, and lets the original exception propagate. `test_oct15.py:test_cpu_profile_cannot_mask_failed_gate` asserts status 7 is retained while its profile is written. `coverage_oct15.py` additionally requires the audit's `gates.physical_footprint_within_2_5GB` flag, and the exporter writes that audit only after the memory helper passes. The calculator negative probe on the retained failed-footprint receipts stopped with `[BLOCKED] pricing process did not pass physical-footprint gate`. [CALCULATION: regression and negative-control execution]

## 2026-10-15: separate profiles retained the whole construction

The raw household snapshot and temporary combined prices remained live when both net profile copies were allocated. That phase crossed 2.5 GB although all scientific gates passed. The export now releases the snapshot first and transfers ownership of the combined profile to the identified profile, allocating only the added copy. All price, source-driver and replicate gates remain active. The measured repaired profiled set export used 21.354 seconds and 2,481.5 MB peak physical footprint. [CALCULATION: phase profiling, shared memory helper]

## 2026-10-15: nominal G3 age factors applied to entirely identified generations

The final state-price adapter initially used `1/f_rec` as the identified fraction everywhere. `age_band_factors` returns a nominal age factor on the whole frame, but the original constructor multiplies weights only on original G3+ rows. Thus this formula imposed an age-dependent factor on fully identified G1/G2 people while generation-dollar closure still passed. The corrected fraction is one outside original G3+, `1/f_rec` within original G3+, with the latent fraction its complement and native observed children separate. [DATA: household constructor's weight placement and identified-weight construction]

The coverage national-driver adapter independently reconstructs this exact population fraction and the principal P7 category driver. `test_oct15.py:test_final_identified_G1_rejects_nominal_G3_age_factor_on_entire_frame` rejects the old cross-generation factor even when the declared piece cost is unchanged. The justice category tests also retain the source per-head/use split and reject a changed category coefficient. [CALCULATION: source-driver regressions]

## 2026-10-15: fixed added target can erase a declared state reallocation

Joint state centering conserves total identified+latent+native cost; the latent+native subtotal can be nonzero. Reusing the old principal added target would then calibrate away that allocation change. Final metadata separately declares the principal source cost, active added-state reallocation, and their sum. The final adapter verifies all three against the frozen BASE source and principal active state parts at 1e-9bn. `test_oct15.py:test_final_calibration_cannot_erase_nonzero_added_state_amount` rejects an unchanged target when that declared added-state subtotal is nonzero. BASE inputs and its target stay unchanged. [CALCULATION: principal target contract, negative regression]

## 2026-10-15: complete adult target included the unlocated coverage block

The first coverage-on constructor compared 9,792,850.6 placed G3+ adults against 10,367,766.3: their difference was the separate 574,915.64098685 coverage adults. The exporter now preserves `complete_generation_g3plus` and declares the exact coverage exclusion in the observed `generation_g3plus` target. The original observed-placement gate stays unchanged. The failed frozen epoch is archived before an explicit refresh; `validate_observed_target_revision` requires the exact principal missing population/adults, unchanged complete target, matching coverage hash, and unchanged dollar amounts and unrelated declarations. Its regression rejects both the old adult target and an unrelated amount change. [CALCULATION: actual final constructor failure; `test_oct15.py:test_final_target_refresh_preserves_complete_population_and_all_dollars`]

## 2026-10-15: final piece temporaries exceeded the physical cap

The final set passed its scientific gates but initially crossed the 2.5GB cap at 2.516GB. Processing masked age-summary weights one generation at a time removes simultaneous redundant full replicate copies. The robust profile then located the remaining 2.510GB peak in piece pricing: the previous full per-person matrix remained alive while the next multiplication/division buffers were allocated. The loop now releases that temporary after its central-column copy. No price arithmetic, precision or guard changed; full BASE NPZ/CSV byte comparison and final physical receipt are required before acceptance. [CALCULATION: `_cache/export_oct15_final_routing_set.prof`; profile phase receipts]

The fresh frozen-source profile still reached 2.537GB in piece pricing because completed low-end source drivers remained live beside captured national/central arrays while pricing the high end. After each end's independent source and replicate gates pass and its metadata is captured, that end's source piece list is now released. The repaired robust final-set export passed at 2,206.5MB in 30.586s. The cap and all price arithmetic remain unchanged. [CALCULATION: `_cache/export_oct15_final_routing_set_profile.log`; current physical-PASS audit]
