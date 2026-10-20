# Failure catalog

## 2026-10-20: keep the shared loader's calibration declaration intact

The shared `population_basis.reweight()` validates that the incoming display
weights match their declared production weights and calibration factors, then
restores production weights before row4. An earlier local reset of `pw` became
invalid when that shared guard was added during propagation. The caller now passes
the declared frame intact. Own located-count and national-count gates in `main()`
verify the resulting frame against the adopted payload and decomposition; the
social lane's live-frame regression covers the same shared transition. Coverage
remains unlocated rather than being inserted into applicant or tax-unit cells.

## 2026-10-20: customs vintage selector disagreed with the named companion

The prepared policy export selected `customs_historical_pinned_bea`, the August26
vintage (-16.603798220bn), while the brief and source RESULT name the September30
`customs_historical_current_bea` sensitivity (-16.934117151bn). The selector now
requires the current named source part, one low and one high row, and equal end
amounts. Output records the source part and BEA vintage explicitly. Its regression
mixes both vintages and rejects missing or duplicated named ends. Neither fiscal
year2028 expensing nor this historical calendar-year2025 sensitivity is summed.

## 2026-10-20: per-unit Python filer loop dominates owned tax-unit setup

The successful CPU-profiled tax run took311.939s. `units()` consumed87.627s;
76,652 per-group filer-status lambdas consumed72.253s, within a groupby apply
costing86.206s. A grouped `all()` on nondependent filers preserves the rule that
any authorized filer qualifies the unit; it fails loudly if a requested tax unit
has no nondependent filer. A mixed-status/dependent/order regression compares the
old formula with the new formula, and full tax output hashes are compared before
accepting the optimization. National Tax-Calculator setup96.497s and repeated
Policy/Calculator setup remain external package costs; modifying that pinned
library or adding persistent result caches is outside this migration.

Final proof: both `tax_rows.csv` and `tax_summary.json` retain their exact
pre-optimization SHA256 values (`policy-tax-vectorization-parity.json`). The
complete optimized wrapper exits0 in159.296s; full official replay exits0,
IDENTICAL20/20 in182.427s. The311.939s profile is instrumented, so these timings
are not asserted as a matched speedup ratio. The current-vintage output is
-16.9341171511101bn, with its September30 source declaration exported.
