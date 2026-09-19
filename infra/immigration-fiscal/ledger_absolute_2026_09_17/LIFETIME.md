# Period-profile fiscal scenarios

Run the annual builder first. `lifetime.py` requires its `age_profiles.csv`,
`age_profile_components.csv`, and audited file/input hashes. It refuses old exports
and stale sources. Personal-source expanded balances are primary; shared allocation
and partial coverage remain explicit sensitivities.

```sh
UV_CACHE_DIR=/private/tmp/uv-fiscal-audit OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ledger_absolute_2026_09_17/lifetime.py --root /Users/alien/Projects/immigration-research
```

`--root` selects annual inputs; `--life-table-root` can select a separate read-only
repo holding the NVSS cache. `--out-dir` changes the destination (default annual
lane `derived/lifetime`). Outputs are `period_profiles.csv` and
`period_profile_audit.json`. Consumers use `load_period_profiles` to verify freshness.

Each scenario sums actual age-band balances, survival-weighted conditionally from
age 0 or 25 and discounted to time zero at a real rate of 0%, 2%, 3%, or 5%.
Social Security cash is already included. No MWR accrual adjustment is added.
Amounts hold the annual account at its 2024 price level with no real growth,
outmigration, fertility or descendants. Current residents aged 25 are not an arrival
cohort. These are period-profile scenarios, not identified admission/birth costs.

Common US-total survival isolates fiscal-profile differences. The alternative uses
pooled Hispanic mortality for Mexican-origin groups, NH-white for the white reference,
US-total for all-native; these are proxies. Fiscal75+ amounts are flat through the
open100+ interval, whose remaining exposure is discounted at100. A sensitivity stops
after82. External institutional allocations and denominators follow the annual export.

Pronatal/longevity commands now invoke this calculation. Their old lifetime-equivalence,
age-reference, longevity and combined CSVs are superseded evidence, not current inputs.
SS timing and combination commands explicitly stop: whole-career money's-worth ratios
do not identify annual marginal accrual, and previous cash removal was inconsistent.

`npv_with_F_per_capita` adds the alternative per-resident defense, interest and
general-government allocation, net of already-priced TRICARE, at the same survival
and discount weights. This is an allocation sensitivity, not full account coverage.

Debt now reads current annual components and reports explicit real-rate year-end
financing scenarios. Deficit shares are assumptions; obsolete federal fractions and
unequal-date per-person future values are removed. Homicide fiscal components use
current personal profiles and conditional survival; family-benefit timing remains
approximate and the result does not identify expected cost per homicide.

Validate with `uv run --no-project python3 -m pytest infra/immigration-fiscal/ledger_absolute_2026_09_17/test_lifetime.py -q`.
