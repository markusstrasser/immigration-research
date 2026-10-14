**Verdict:** The case already assigns 28.3191% of highway costs to freight at the group's consumption key. A demand-side freight arm therefore reproduces its current road key. The corrected Oregon comparison assigns 29.1% of costs to heavy vehicles; modern national truck VMT is about 10%, which is a mileage statistic and cannot replace cost responsibility without an explicit sensitivity assumption. [DATA: `inputs/highway_shares.json`; `../roads_mileage_key_2026_09_29/RESULT.md`, Method/Keys]

## Parsed and pinned inputs

| Input | Freight/heavy share | What it measures | Extraction |
|---|---:|---|---|
| FHWA HCAS V-21, all levels | 28.3190501% | Forecast 2000 highway program cost responsibility | Parse existing pinned CSV transcription; independent visual comparison to the pinned primary GIF |
| FHWA HCAS V-21, federal | 39.6265704% | Same forecast, federal column | Same |
| FHWA HCAS V-21, state | 24.8987125% | Same forecast, state column | Same |
| FHWA HCAS V-21, local | 25.0443633% | Same forecast, local column | Same |
| FHWA May 2000 addendum, Table 4 | 40.2972949% | Forecast federal TEA-21 program cost responsibility | Primary HTML table, full vehicle-class rows |
| FHWA Highway Statistics 2024 VM-1: 2023 | 10.1594393% | National single-unit and combination-truck VMT / all VMT | Primary XLSX unrounded cells |
| FHWA Highway Statistics 2024 VM-1: 2024 | 10.0059745% | Same | Same |
| Oregon corrected 2025–27 study | 29.1% | Forecast full-fee-paying heavy-vehicle cost responsibility | Primary corrected PDF summary, printed page 7 |

[CALCULATION: `acquire_highways.py` → `inputs/highway_shares.json`; SOURCE: [FHWA V-21 chapter](https://www.fhwa.dot.gov/policy/hcas/final/five.cfm), [FHWA addendum](https://www.fhwa.dot.gov/policy/hcas/addendum.cfm), [FHWA VM-1](https://www.fhwa.dot.gov/policyinformation/statistics/2024/vm1.cfm), [Oregon corrected study](https://www.oregon.gov/das/oea/Documents/ECONW-HCAS-Cost-Allocation-Study-2025-27-Corrected.pdf)]

Each original is pinned by SHA256 in `inputs/highways_pins.json`. The V-21 image and addendum reuse the road lane's cached primary sources. The VM-1 workbook and Oregon corrected PDF are downloaded into this lane. No source quantities are typed in the parser.

## Existing case and classification

The existing road lane uses `passenger_share × driver_VMT_key + freight_share × consumption_key`, with the all-government V-21 passenger share. Its spending and public road capital use that blend. Trucks are therefore already included in the key, though their allocation is household goods demand rather than the group's industry output. Re-keying freight once changes the existing freight contribution; adding a second truck contribution would count it twice. [DATA: `../roads_mileage_key_2026_09_29/RESULT.md`, lines 63–66 and 76–79; INFERENCE]

V-21 groups autos, pickups/vans and buses as passenger vehicles; its freight group consists of single-unit and combination trucks. That classification is not a measurement of private versus commercial use. VM-1 likewise puts passenger cars, light trucks, vans and SUVs in light duty, irrespective of use. Single-unit means single-frame trucks with at least six tires or GVWR above 10,000 pounds. Oregon's heavy class is above 10,000 pounds and its quoted share covers full-fee-paying vehicles. None gives a measured national commercial-use fraction for light pickups or vans. [SOURCE: FHWA VM-1 footnotes 2–3; Oregon corrected summary; DATA: V-21 source image]

Cost-allocation studies attribute agency program costs using cost-occasioned models and forecast expenditures; their shares are modeled allocations using traffic, engineering and budget inputs, not observed business-use costs. Freight mileage is much smaller than freight cost responsibility because the engineering allocation accounts for heavier loads. FHWA's addendum allocates projected program obligations, not this account's annual consumption and capital return separately. Oregon is a comparison with a different geography, road mix and financing treatment. Its corrected edition changes the expenditure accounting, so the superseded January report is not used. [SOURCE: FHWA addendum, Allocation of 2000 Federal Highway Program Costs; Oregon corrected study, printed pages 9–10; INFERENCE]

Recommendation: retain the existing all-level 28.3191% share when testing a freight output key, with goods demand as the unchanged positive control. The federal share, Oregon's 29.1% and current truck VMT may be separate sensitivity arms. Do not treat their range as statistical uncertainty or replace a national cost share with Oregon's forecast without stating that transfer assumption. [INFERENCE]

## Independent V-21 visual check

Viewed the original pinned `highway_hcas_v21.gif` at native resolution and compared every federal/state/local/total value against the existing `roads_mileage_key_2026_09_29/derived/hcas_v21.csv`: all 44 cells agree. Coverage: Autos; Pickups and Vans; Buses; the three Single Unit Truck weight rows; the five Combination Truck weight rows. The passenger and single-unit subtotal rows also agree with the sums of their corresponding individual rows. The image contains no all-vehicle total, so that total is computed from its rows. Cross-level values have the source's integer-$million rounding (up to $2m difference per row). This is an independent visual source check followed by reuse of the existing transcription, **not fresh OCR extraction**. [SOURCE: pinned V-21 image; DATA: existing transcription and `inputs/highway_shares.json`]

Automatic whole-cell OCR was rejected because adjacent small digits were unreliable. No OCR quantity reaches the final inputs. The image hash and transcription hash are separately pinned, so either source changing stops the offline run. [CALCULATION: parser's source hash gates; DATA: `inputs/highways_pins.json`]

## Gates and reproduction

- Source SHA256 checks pass for all four originals and the prior V-21 transcription.
- V-21's printed-rounded cross-level rows and all computed passenger/freight shares close.
- The federal addendum passenger plus truck totals close exactly, as do single-unit plus combination trucks.
- Both national VM-1 years close from their unrounded XLSX component cells within `1e-6` million miles; no display-rounding tolerance is substituted.
- Oregon's light/heavy cost percentages close to one.
- Python compile check passes. Offline extraction exits 0 in 0.212 seconds, peak self RSS 0.075562 GB (Python `resource.getrusage`). No shell `time`, `ps` or `sysctl` is used.
- A separate offline run to `_cache/highway_rerun/` exits 0; its only output is byte-identical to the default input (`IDENTICAL: 1/1`). The parent runs the whole-lane `rerun_lane.py` once concurrent builders are complete; this subtask does not claim that check covers peer scripts still being edited.

Run from repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/business_services_key_2026_10_14/acquire_highways.py
```

Add `--acquire` to reconstruct missing source caches. Existing pinned hashes must still match. The first acquisition uses system curl with TLS verification enabled; uv Python's OpenSSL certificate store rejected this machine's network certificate, while host curl validates it. Transport/HTTP failures and malformed source tables stop the run. The only output of the normal offline command is `inputs/highway_shares.json`; timing remains on stdout for deterministic output bytes.

## Gaps and scope

[GAP] No current nationwide all-government cost-allocation study or measured private/business light-vehicle share was obtained. This lane supplies the measured/source-model comparisons above; it does not estimate the final fiscal delta, goods-output key, survey replicate SEs, or the rest of the business-services inventory (owned by parent).

Covered: the prior highway sources and road-key method, FHWA federal vehicle-class costs, latest VM-1 national truck VMT, one corrected state comparison. Skipped: a second state, because the brief says one or two state comparisons suffice and Oregon supplies the current explicit comparison; receipts, because this subtask owns spending shares only; raw NHTS and freight input-output attribution, owned by parent.

## Log

- 2026-10-14 20:50:49 JST (from `date`): primary acquisitions pinned, source-model distinctions written, all-cell V-21 visual comparison recorded, compile check and independent offline byte comparison pass. No git write operations performed.
