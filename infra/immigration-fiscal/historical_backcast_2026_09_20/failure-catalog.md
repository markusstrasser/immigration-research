# Back-cast failure checks

## Live annual-part cache integrity — 2026-10-20

The v9 typed component expansion produced a 143,803,805-byte annual CSV, too
large for this repository's 50 MB limit. Its complete evidence is rebuildable,
so the producer writes the full table to ignored `_cache/oct16/` and its
SHA-256, byte/row counts, schema and full key to a tracked manifest. It rejects
duplicate full keys. `cache_contract.verify_cached_annual()` stops `[BLOCKED]`
on a missing receipt/cache, changed contract, or mismatched bytes/hash/rows/header;
consumers may not silently fall back to another case. Regenerate with README's
live commands. `test_v9_cached_annual_pin_and_fail_loud_guards` covers duplicate
production keys, missing receipt/cache and same-size changed content;
`test_v9_live_annual_cache_matches_tracked_receipt` checks the actual live table.

## Hash-order drift in the live charged base — 2026-10-20

Summing the five separately carried programme paths through a Python set let
hash randomization change a sensitivity cell by 1e-9bn at export rounding.
The oct16 residual-base construction now sums its named programme paths in
sorted order through `ordered_programme_total`; archived-case code retains its
historical route. `test_v9_charged_programme_sum_is_hash_seed_invariant` executes
that production helper in fresh processes under three different Python hash
seeds and checks exact floating-point results. Byte-identical lane replay is
the end-to-end fail-loud gate; no fiscal tolerance was loosened.
