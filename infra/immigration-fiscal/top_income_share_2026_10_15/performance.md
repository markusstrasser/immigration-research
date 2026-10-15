# CPS regeneration profile

The first complete lane build on 2026-10-15 took 121.03 seconds inside the CPS
step (122.05 seconds including interpreter startup), triggering profiling before
the final reproduction. It passed all checks and peaked at 581.1 MiB RSS.
The seven-year step reads only the required person fields and chunked replicate
weights; it does not read the full person files into memory.

A one-year cProfile probe, ASEC 2019, measured 21.555 seconds total: 12.182 in
`load_year`, 9.371 in `stats`, of which 9.251 seconds were the seven repeated
`aggregate` calls. Those operations scanned replicate columns of a C-order
161-column matrix, repeatedly walking a wide row stride.

`load_year` now allocates the matrix in Fortran order and `row4_weights` preserves
that order. The identical one-year probe measured 12.717 seconds total: 11.363 in
`load_year`, 1.352 in `stats`, 1.056 in `aggregate`. These are two observed probes
on a shared machine, not a controlled whole-lane speedup estimate. CSV parsing
remains the largest cost; no new caching layer is justified for this bounded run.

The final `rerun_lane.py` check compares every persisted result byte after the
layout change and reruns the scientific tests. Profile code and pstats stay in
ignored `_cache/`; no primary source or mathematical operation was changed.
