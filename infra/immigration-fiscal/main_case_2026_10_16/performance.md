# Measured v9 execution cost

The source lanes are immutable under this brief. New per-phase timers in main_case.cjs locate each companion, arm and inherited-range block; transient Node CPU profiles stay under ignored _cache/.

2026-10-15T03:29:12Z profile receipt: an explicit current-source item13 medical-arm probe initialized the package in18.451s and constructed/priced the arm in8.729s (case construction6.802s). It was run with Node --cpu-prof and --max-old-space-size=3072; the profile is _cache/item_arm.cpuprofile.

Exclusive sampled CPU in that complete init+arm probe: v8 package JSON clone10.824s; engine JSON clone5.778s; source added-band clone0.749s; v7 clone0.660s; source age-mix clone0.652s; new v9 package clone0.379s; own coverage integration0.299s; garbage collection1.014s. These are one observed probe under concurrent work, not a normalized speedup estimate.

The largest hotspot is repeated immutable source payload/model cloning while delivered builders recover their source exposure/generation parts. A complete main build enumerates every new-item arm, so total runtime can exceed two minutes even though a single arm is bounded. Changing protected producer/v8 modules would violate this task. Follow-up for the parent: cache an immutable source API payload inside its owning source builder, preserve cash/set identity and generation conventions, and gate every source arm byte-for-byte before adoption. This issue is filed rather than altering protected code here.

The G3 investigation initially used the wrong memory metric. The canonical scripts/memory_budget.py requires lifetime peak physical footprint, not RSS. memory_guard.cjs now asks a live Python helper that imports the canonical structure/limit; RSS remains a diagnostic. Heap-cap OOM experiments and optional uncached route remain evidence, not a successful optimization claim.
