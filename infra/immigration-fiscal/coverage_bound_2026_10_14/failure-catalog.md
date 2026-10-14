# Coverage execution failures

## 2026-10-15: profiler hides a failed physical-memory guard

The standard `python -m cProfile` entry returned exit 0 after pricing's physical-footprint guard raised `SystemExit`. Old scientific artifacts therefore existed despite a failed launch. A successful launcher status and unchanged artifacts did not prove the guarded run succeeded. The preserved profile is `_cache/stdlib_masked_exit.prof`. [CALCULATION: observed guarded export and status probes]

`export_pricing.py --cpu-profile` now enables profiling inside a `try/finally`, writes the profile, and lets the original exception propagate. `test_oct15.py:test_cpu_profile_cannot_mask_failed_gate` asserts status 7 is retained while its profile is written. `coverage_oct15.py` additionally requires the audit's `gates.physical_footprint_within_2_5GB` flag, and the exporter writes that audit only after the memory helper passes. The calculator negative probe on the retained failed-footprint receipts stopped with `[BLOCKED] pricing process did not pass physical-footprint gate`. [CALCULATION: regression and negative-control execution]

## 2026-10-15: separate profiles retained the whole construction

The raw household snapshot and temporary combined prices remained live when both net profile copies were allocated. That phase crossed 2.5 GB although all scientific gates passed. The export now releases the snapshot first and transfers ownership of the combined profile to the identified profile, allocating only the added copy. All price, source-driver and replicate gates remain active. The measured repaired profiled set export used 21.354 seconds and 2,481.5 MB peak physical footprint. [CALCULATION: phase profiling, shared memory helper]
