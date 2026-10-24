**Verdict:** On the acquisition-cost price rule, land under every public capital line the v9 case charges costs the
group **$19.74 / 23.68bn a year** at the case's 2.0810698764% rate (cited-factor range $11.38 / 13.74bn to
$28.13 / 33.45bn), and **$22.94 / 27.53bn** at the θ-paired rates (federal 3.20%, state and local 2.42%). Roads are
$10.35 / 13.98bn, parks $4.84 / 5.08bn, K-12 $2.85bn, airports $1.09bn, colleges $0.35bn and toll facilities
$0.22bn. Against public_land's arm B ($32.93 / 39.61bn on the same records), rural acres move from $12.73 / 15.40bn
to $0.49 / 0.60bn at county farmland value, and state fallbacks from $3.39 / 4.40bn to $0.06 / 0.08bn, while urban
acres rise from $16.81 / 19.81bn to $19.19 / 23.00bn under across-the-fence pricing. The estimate passes the
precision, stability and data-quality screens. It **fails the influence screen** as written: dropping the five
counties with the largest charges (Los Angeles, New York, Orange, San Diego, Santa Clara) moves the total 33%. By
the constitution's rule it is therefore reported as **not identified**. Re-pricing those five counties at their
county-average urban price instead moves it 3% ($19.17 / 23.01bn). Whether that test replaces the drop-five rule
for a sum of measured values is an analysis-protocol choice left to the operator. [CALCULATION:
`derived/summary.json`, `derived/land_by_line.csv`, `derived/factors.csv`; FRAMING-SENSITIVE]

## What the rule is

The price is what land of each kind costs to obtain where it lies, the saving a long-run budget response makes when
a smaller stock is never built (FTA, *Valuation of Railroad Right of Way*, rev. 2018, p.13; UASFLA "Yellow Book"
2016 market-value standard; OECD–Eurostat *Compilation Guide on Land Estimation* 2015, para 8.100). The factors,
with pages and quotes, are in `research_factors.md` and `derived/factors.csv`:

| Land | Rule | Central | Range |
|---|---|---:|---|
| Urban interstates to minor arterials (HPMS 1–4) | across-the-fence (ATF) residential land, bought from existing parcels | 1.0 × ATF | 0.65–1.16 (FTA's corridor-sale median 1.158) |
| Urban collectors and local streets (HPMS 5–7); urban parks, airports, plants, built-up sites over two acres | raw land per gross acre, dedicated at subdivision | 0.65 × ATF (NAHB via Gyourko–Krimmel 2021) | 0.35–1.0 |
| Built-up sites of two acres or less | small-site share | 0.80 × ATF | 0.43–1.0 |
| Rural acres of every line | county farmland value (Census of Agriculture 2022 × state land-only share × NASS 2022→2024 change) | 1.0 | 1.0–1.16 |

K-12 keeps the school lane's values. The urban ATF price is FHFA's 2024 as-is residential land price.

The rule is not the only defensible one. The Yellow Book values land under an existing dedicated road at a nominal
amount (§4.11.3.1, p.195), and Australia's current-use fair value implies about 0.10 × ATF. Those answer what the
existing road would sell for as a road. The case's long-run removal asks what the budget saves when the road is never
acquired, which is its acquisition cost. [INFERENCE; FRAMING-SENSITIVE]

## Checks

- Guerra, Duranton & Ma (2024, NBER w32824, pp.13–16) value roadway in 316 PMSAs at $4.1tr at FHFA 2015 prices.
  This lane's urban roads at the same price level are $3.95tr (ratio 0.96; scopes differ). Passes.
- Highway land to BEA highway structures: 1.27 central (0.76–1.70). BEA publishes no highway land, so this is
  reported, not tested.
- Rural park land averages $6,180 an acre, against NCREIF timberland's $2,162 (which includes standing timber).
  Pricing rural parks at pasture moves the high end to $23.54bn.
- Value per centerline mile: $58,074 rural, $4.91m urban.
- Fallback-priced share of the charge: 0.39%. Unpriced: 12,771 acres (201 records).

## Screen (`scripts/estimate_screen.py` thresholds)

| Test | Result |
|---|---|
| Precision: cited-factor half-width ÷ central | 0.42 / 0.42, passes |
| Stability: pre-specified constructions, max ÷ min ≤ 1.5 | passes (county-average urban price $22.19bn, rural parks at pasture $23.54bn, high end) |
| Data quality: fallback share ≤ 5% | 0.39%, passes |
| Influence: drop the five largest counties, move ≤ 25% | 33.3% / 32.9%, **fails** |
| Influence, beside: re-price the five at county-average urban price | 2.9% / 2.8% |

The five counties carry about a third of the charge because the group lives where urban land is dearest. The
drop-five rule was written for scaling elasticities, where one influential unit can carry a fit. Here dropping the
counties deletes measured cost rather than testing a fit. [INFERENCE]

## Reproduction

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/land_price_rule_2026_10_24/classify.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/land_price_rule_2026_10_24/build.py

7 lane tests pass. `rerun_lane.py` with both commands: IDENTICAL 12/12, exit 0. Raw downloads (NASS, Census of
Agriculture, FHWA, source PDFs) are in the ignored `_cache/` (1.0 GB), with `_cache/acquire_manifest.json`.

## Log
- 2026-10-24 13:44 JST — lane started (Claude Opus 5.5 worker; the Codex plan limit had stopped the Sol dispatch).
- 2026-10-24 14:22 JST — worker stopped at the subscription's weekly limit after writing the research, build and
  outputs, before the RESULT.
- 2026-10-24 14:29 JST — parent fixed the input-provenance path (`relative_to(ROOT)`; the screen script sits outside
  `infra/immigration-fiscal`), reran the build, verified the reproduction and wrote this RESULT.

## Screen revision (2026-10-24)

The operator adopted the repricing influence test for sums
([decision](../../../decisions/2026-10-24-influence-test-for-sums.md)). Under it the estimate moves 2.9% / 2.8% and
passes every screen, so **$19.74 / 23.68bn at the case rate is identified** and enters candidate main case v10. The
drop-five result above (33%) stays as recorded.
