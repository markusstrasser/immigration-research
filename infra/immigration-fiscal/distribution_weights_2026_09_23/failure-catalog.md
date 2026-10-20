# Distribution lane performance records

## 2026-10-20: repeated rank-weight calculations exceed two minutes

Trigger: the first adopted-oct16 producer took 208.208s internally, 210.830s
including the Python wrapper; it passed 347 gates and used 1,544,046,704 bytes
of lifetime peak physical footprint. This was a slow successful run, not a
numerical or memory failure. [CALCULATION: producer receipt in RESULT.md]

The required replay was profiled with `python3 -m cProfile -o
_cache/oct16/distribute-profile.pstats distribute.py --payer-source ...`.
Its 3,801,084 calls took 142.591s of profiled cumulative wall time, including
scheduling: `bin_weighted`, 3,080 calls / 52.236s; `person_weights`, 4,808 calls /
34.981s; `acs_channels`, 18.630s; `load_cps`, 8.776s. Cumulative timings are
not additive when calls nest, and they are not a process-CPU benchmark.
[DATA: `_cache/oct16/distribute-profile.pstats`]

The weight functions recompute income-bin denominators and person weights
for repeated rank/eta/floor combinations. Phase timings now locate source/CPS,
fiscal/production, ACS/SCF and channel work on each invocation. A potential
repair is rank-lifetime caching of these invariant arrays; it is deferred
from this scientific migration because frame, mask and rank lifetimes must
be explicit and retained arrays must stay within the memory budget. No speedup
is claimed. [DATA: `distribute.py` person_weights/bin_weighted and main]

Regression criteria for that follow-up: preserve the current 16 distribution
files byte for byte, retain all 347 gates and nine tests, preserve frozen-key
versus calibrated-key separation, and retain the 2.5GB physical-footprint
guard. Existing byte replay and producer memory guards fail loudly on drift
or excess use. Profile and compare at matched machine load before claiming
a whole-lane speedup. [DATA: `test_distribute.py`; `distribute.py`;
CALCULATION: `scripts/rerun_lane.py`]
