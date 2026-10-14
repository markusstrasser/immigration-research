**Verdict:** The v7 programme route exists in `debt_legacy.py`, but its fiscal-gap output is not the full real-cost headline. Yearly K-12 age-share measurement is available for 2005–2024; Medicaid coverage and full-sample replicate weights are available locally for income years 2019–2024 only. [DATA: files and fields traced below]

Read-only scout; implementation and final checks belong to the parent. Investigation in progress.

## Completed investigation — 2026-10-14

The interim status above is superseded. `debt_legacy.py:1731-1872` supplies the older programme/fiscal-gap method, but those totals omit charged public capital and displaced-beneficiary costs. P7 instead evaluates the complete live v7 package, then uses `case_components_oct14.json`'s authoritative union/lineage attribution. Full-cost source mappings and closure are in `p7_backcast.py` and `programme_inputs.cjs`.

The pinned pooled IPUMS extract (`g3_identity_pooled_2026_10_05/_cache/asec_pooled.csv.gz`) has AGE, YEAR, ASECFLAG, ASECWT, BPL, MBPL, FBPL and HISPAN for 2006–2025 surveys: 2005–2024 on this lane's income-year convention. It supplies school-age central keys; the extract lacks full-sample replicate weights and historical Medicaid fields. The six public-use ASEC zip files pinned in `backcast_pandemic_measured_2026_09_28/measure_shares.py` supply MCAID and 160 replicates for survey years 2020–2025, coverage years 2019–2024. `historical_use.py` measures those available grids without filling absent years; hashes, source paths, timing and limits are in `derived/p7/use_source_manifest.json`.
