# Replay failures

2026-10-20: the final pin capture depended on a worker-session adoption marker. It now
requires the repository's matching `live_case.json` declaration and the consumed package's
adopted exports through the shared adoption gate. Pins record the adoption date and decision
path rather than an unavailable future commit hash. The pin-capture regression verifies
refusal before writing and the captured repository identity. Historical pin files remain
unchanged; explicit final pin derivation still follows successful source replay.

The first full route stopped at an old Node assertion: the preflight now distinguishes an
unverified adoption stamp from a stale case/generation identity, while the test still expected
the old combined message. The regression now checks both refusals separately; the 80-space
brute-force search and 41-arm controls continue to pass before the expensive engine runs.

2026-10-21: four stops found once the oct16 engine first ran past item-arm pricing.
- C1's exact minimal-crossing search did not finish: 22 downward groups (oct15: 15), sizes 1-7 took 82.7M
  evaluations and 203,729 minimal crossings, about five times more per size; the run was stopped after 19 minutes in
  the search. The oct16 search is now complete through `--c1-max-size` arms (default 5) and its receipt and the C1
  table say larger minimal crossings are not enumerated [SCOPE]. Capped searches match brute force in 120 fixtures.
- The payload-identity gate failed on the default uncached case route (`V9_CASE_CACHE=0`): that route's
  `correctionsPayload()` differs from `main_case_2026_10_16/derived/corrections{,_cash}.json` in item 13's part
  metadata for three veterans lines (costs and totals equal). The gate was right. The engine now refuses
  `V9_CASE_CACHE=0` and uses the canonical cached route, whose memory (2.7 GB in one process) is held by pricing
  the item arms in bounded child processes (`item_arm_prices.cjs`). The route difference is the case lane's to fix.
- C6's generation service sweep passed `generationParts` a specification without normalization or line responses,
  and with `long_run: true` where the v8 evaluator needs a variant name. It now takes the case's own specification
  at that reading, allocation and normalization (all 8 matching specifications must agree on line responses), with
  the sweep's service, government, care, rate and enterprise fields.
- Review 2026-10-20 (MED): C6 replayed the generation producer against its own output, and the first-year response
  closure was an identity. C6 now also prices each generation by the payload's declared consumer rule; the
  first-year report rebuilds the engine change from receipt amounts and responses and checks the multipliers.
- C4 read the oct15 real-costs schema: `tables_oct16.py` subtracted `hispanic`/`custody` "fiscal main case" rows,
  which the oct16 `real_costs_totals.csv` no longer publishes (since v8 the pairing's fiscal row is the case at both
  ends), and read `social_item_*` span rows the oct16 file also dropped. C4 now takes the published "social rows after
  environmental replacements", requires pairing minus social to equal the live band (1e-9; it closes at 6e-14), and
  reads the item spans and normalized values from the oct16 document's `inherited_oct15` record-basis block, labelled
  as such. The oct15 table subtracted the raw-coded Hispanic footing at the low end while that pairing used the case
  (116.56 vs the published 111.86bn); the oct15 output stays as computed.
- `tables_oct16_pins.json` was 40.7 MB because `indent=2` put each pinned cell on separate lines; pins now write one
  line per input (16.0 MB tables, 1.7 MB engine) and must round-trip to the same record.
