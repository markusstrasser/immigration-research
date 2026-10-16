# Local analysis failure checks

- Input schema: the reconnaissance requested nonexistent TCBIRTH but did not use
  it. The new extractor fails on a missing requested field. Removed that unused
  request after checking the original schema; no invented birthplace fallback.
- Cache lifecycle: downstream scripts verify the source/extractor receipt before
  using an extract. Start downstream work only after the producer exits zero.
- Event screening latency: a first pass materialized full rows for every adult
  month and exceeded two minutes. Interrupted stack showed the Type-2 slot loop.
  Restrict full-row inspection to a vectorized candidate screen; preserve exact
  identity-set checks for those candidates. Independent event counts and the
  deterministic rerun guard against changing the sample while optimizing.
- Replicate coverage: the December person file contains 18 records with no
  replicate record and no positive full weight. An initial total-row equality
  assertion was too strong. The corrected gate requires every positive-weight
  record to match and checks matching full/replicate weights numerically; missing
  positive weights remain a fatal error.
- Benchmark latency: the first complete run repeatedly reweighted more than
  70,000 control anchors per bootstrap draw. Aggregate sums/counts by sample unit
  and matching stratum once, then multiply the identical Poisson draws. Compare
  every result to the saved row-loop calculation before adopting the optimization.
- Code-review checks: a malformed relationship ID/value pair must fail rather
  than imitate a disappearance; an unsupported comparison must emit an explicit
  non-estimable row rather than disappear from output. Both have targeted tests.
