# Confirmed oct16 migration failures

## Survey calibration was counted through both normalization and a delta

Observed during independent source review, 2026-10-15. Old source subtotals were held fixed by renormalizing
person prices at new weights, then the native-calibration amount was added on changed records. For original
weights 1/1 and fixed prices 100/100, new weights 0.5/1 and declared change −50 produced 33.33/133.33, while the
correct unchanged unit prices were 100/100. The weighted total alone could not detect artificial crossings.

Repair: preserve original person prices, price direct source changes on original weights, count mechanical
reweighting once, and reconcile only the remainder from the declared native source parts on changed records.
`calibration_reconciliation*.csv` exposes the mechanical and declared changes separately. Regression:
`test_pure_calibration_preserves_unit_prices_and_does_not_create_crossings` checks unchanged prices/signs and
correct weighted total; `test_source_repricing_changes_only_the_calibrated_records` checks actual repricing.

## Cached source signatures admitted changed bytes in a control snapshot

Observed in the pure control-snapshot fixture, 2026-10-15. The exporter cached a file's SHA, then the snapshot
validator asked the same cache for its supposed current SHA. Changing the file later in the same process could
therefore pass the freshness check.

Repair: snapshot validation requests a fresh byte hash for each source receipt. The fixture changes real temporary
file bytes after the initial signature and requires rejection, covering the six principal/inherited/exporter
receipts, missing receipts and invalid central snapshot identities. Tests live in `test_export_oct16.cjs`.

## College operating parts followed their display line instead of their carrier

Observed in preparation-only allocation, 2026-10-15. A college operating part names display line
`education_services:college_only` but declares `capital_source_line=union_completion_college_low`.
Looking for the display line among capital pieces failed despite the exact declared carrier being present.

Repair: both the explicit college-operating kind and the count-source college proxy locate the exact capital
carrier first. The resulting operating amount remains in education, with its declared completion population.
`test_college_operating_amount_follows_declared_capital_source_line` covers the source schema. Unknown spending
sources still stop rather than becoming unlocated residuals.

## Repeated protected source payload cloning dominates the oct16 export

Observed on the adopted case, 2026-10-20. Personal/shared source exports took 136.663/132.009 seconds under
concurrent lane work. The representative standalone-none control profile (`_cache/oct16/control-none.cpuprofile`)
recorded 96.028 sampled seconds: 43.070 in v8 package JSON cloning, 18.209 in engine cloning, and 3.552 in garbage
collection. Of the cloning, 34.807 seconds originated in the spending producer's `items.cjs:lineParts` repeatedly
requesting its source payload. This agrees with the source lane's existing `main_case_2026_10_16/performance.md`.

The source lane and engine are outside this assignment's write ownership. File the source-owner repair here:
cache the immutable source payload within the owning builder, preserve separate set/cash identities, and compare
all source arms and final consumers byte for byte before adopting it. This consumer retains physical-footprint
guards and exact subprocess exits; a slow producer never becomes a skipped control or an assumed success.
Timings are concurrent-run observations, not a normalized speed comparison.

## Final publishers depended on a temporary session marker

Observed 2026-10-20 during scratch-dependency review. The wrapper, source exporters and household publisher
admitted final execution through an absolute session marker path, so a clean clone or scratch cleanup would
block an adopted case. Final controls also copied that marker's prose as their authority.

Repair: every final entry point uses the shared repository adoption gate. The live key must match oct16, the
package case/lane identity must match, it must declare adopted status, and its date and decision must match the live declaration. Controls retain
that structured authority. Regression fixtures cover stale live keys, candidate status, adopted acceptance and
the final publisher stopping before input reads when adoption fails (`test_oct16_households.py`).

Performance follow-up: the shared Python gate launches Node and loads the protected package for each final
publisher process. During concurrent producer edits, the two rejected preflight attempts took8.953s and14.367s
before reading consumer inputs. These are failed, concurrent observations rather than a measured steady-state
overhead. The full wrapper repeats the gate across its publisher processes. Keep the required package status/date/
decision validation; profile the owning package's eager source evaluation before changing its representation.

Same-session resolution: the owning shared gate now loads the package's adoption metadata projection in an
isolated child; the package declares that metadata once and its own checks compare the projection with full
exports. A direct final gate call passed in0.164s, with diagnostic child maxRSS42,450,944bytes. The consumer keeps
the same gate contract and never bypasses a status/date/decision check. This observation does not measure the
full scientific wrapper's speed.
