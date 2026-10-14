**Verdict:** The measured wage-cell reconstruction passes the existing item-6 positive controls. Its modeled private-output share is 8.1794% (replicate SE 0.1862 percentage points); the goods-output share is 9.0098% (SE 0.5213 points). These are activity proxies, not measurements of public-service consumption. [CALCULATION: `activity_keys.py` → `derived/activity_keys.json`]

Ownership: `activity_keys.py`, `derived/activity_keys.json`, this evidence file. Existing job-capital code and inputs are read-only. No git mutation.

The intended business key weights each industry's corrected, smoothed personal CPS wage share by its BEA gross output. The freight supply arm restricts this vector to agriculture (including forestry/fishing), mining and manufacturing; construction is excluded. Mining-fixed keys retain the full national denominator but remove mining's attributed numerator. The full-output arms show mining responding with other industries. [ASSUMPTION]

## Inputs and traced rule

The primary BEA file is already archived and pinned: [SOURCE: https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip], upstream `_cache/bea_SUPPLY-USE.zip`, sha256 `3f16466e11eef0ed562d3663907f4a4a65856c134aa9f8baf7da6460bd11987d`. The 2024 `Use_Summary.xlsx` row T018 is **Total industry output (basic prices)**, millions of dollars. `national.read_use` parses it; `national.SUT_TO_CELL` maps the pension/fund cell into 523 and the government cells into GOVF/GOVSL. Gross output includes intermediate transactions, so its sum is larger than GDP. The business vector excludes housing HS and government, retaining other private activity including private nonprofits. [DATA: pinned workbook; `job_capital_taxes_2026_10_14/national.py:177,201`]

The source's industry cells sum to $49,511,318mn, versus $49,511,321mn in its official T001 total. The source-rounding gate permits at most half a million per source cell; a common multiplier normalizes the vector to the official total. Closure after normalization is below 1e-6bn; the common multiplier cancels in every share. The business vector sums to $40,749.056469bn and the freight vector $8,382.264508bn. [CALCULATION: `activity_keys.py` → `meta.output_rounding`, `keys.*.national_output_bn`]

The CPS construction imports `job_capital.load_frame`, `masks`, `row4_weights`, `cell_of`, `cell_wages`, `checked` and `se` read-only. It traces the upstream personal construction: WSAL_VAL clipped at zero, civilian household population, industry of longest job, government workers separated, Mexico-born outside CA/TX raked separately by citizenship in all 161 weight columns; top wages at or above $1M redistributed as national top wages; cells with fewer than 100 earners pooled to sector, or private total if the sector is thin. Its main fill-in correction averages the case's two methods, with generation splits from `stack_by_generation.json`, exactly as item 6. Unauthorized off-books wages are retained, as in item 6, because output at jobs follows all labor. [DATA: `job_capital_taxes_2026_10_14/job_capital.py:163-245,280-400`]

## Keys and uncertainty

| Personal union key | Share | SDR SE, percentage points |
|---|---:|---:|
| All private output | 8.1794064% | 0.1861703 |
| Nonmining numerator / all private output | 7.9683005% | 0.1813352 |
| Goods output | 9.0097812% | 0.5212941 |
| Nonmining goods numerator / all goods output | 7.9835231% | 0.4321796 |
| Plain wage share | 7.8791453% | 0.1428537 |
| Row-4 population share | 11.8352664% | 0.1054815 |

[CALCULATION: `activity_keys.py` → `derived/activity_keys.json`, `keys`]

Mining's output fractions are 1.6771432% of private output and 8.1531672% of goods output. A central that preserves mining's prior household/demand service allocation uses **partial nonmining share + mining_output_fraction × baseline household/consumption share**. Treating the partial share as the entire business key instead would silently erase mining services; the JSON documents the hybrid explicitly. [CALCULATION: `keys.*.mining_output_fraction`; ASSUMPTION: mining fixed as main-case item 6]

Every key exposes all 161 CPS estimates for union, G1, G2, G3plus and white_nh, and SEs from `4/160 × sum((replicate-main)^2)`. `union_covariance` preserves covariance among business, freight, plain wages and population. Therefore a business-minus-population change can use its joint replicate vector. Population's point estimate is the CPS row-4 frame, not the frozen case's household key; preserve the case baseline and state any ratio used to map its deviations. A freight-minus-consumption SE must hold the frozen consumption baseline fixed unless the parent obtains its own matched replicate vector. [CALCULATION; ASSUMPTION]

SEs condition on BEA output and the main-estimate generation fill-in factors, top pooling and thin-cell rule. They omit uncertainty in business-serving fractions, the causal response, BEA estimates, fill-in estimates and lineage composition. Added-lineage uncertainty is not identified by independently adding the reported group SEs. [INFERENCE]

`factor` divides each union/generation output share by its share of the case wage key; white_nh divides by its plain lane wage share. `factor_over_lane_plain` is also available for every group. Multiply the frozen case's added G3plus and white wage parts by the matching factor rather than treating their output share as an added population. For the full business key G3plus's factor is 0.930096385 and white_nh's 1.019078886; the partial nonmining factors are 0.899459678 and 1.000569315. [DATA: `derived/activity_keys.json`, `keys.*.groups.*.factor`; ASSUMPTION: added people take those groups' industry profiles]

## Gates and reproduction

36 gates pass, including published-weight builder totals/share/SE; row-4 mask, factors and population; generation and top-wage conservation in every weight column; exact reproduction of upstream wage bills at its CSV's six-decimal precision; upstream industry key shares and SEs at 1e-9; BEA source pin/title/year/units and output normalization; national vector closure at 1e-6bn; positive wages for all positive-output cells; every generation contribution summing to union at 1e-12. Imported code and derived controls are pinned in the script, and inherited CPS/fill-in/row-4 inputs use the upstream pins. Any stale source or failed gate exits before writing. [DATA: `activity_keys.py`, `derived/activity_keys.json:gates`]

Command: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/business_services_key_2026_10_14/activity_keys.py`. `--out-dir <scratch>` permits a byte comparison without writing upstream or peer outputs. The parent runs the final lane-wide `rerun_lane.py` after integrating the other owners' scripts.

2026-10-14 20:42 JST: first successful build, 17.220 seconds, peak 1,239.8MB. 20:44 JST: rebuilt after removing nondeterministic memory details from the derived gate record, 14.469 seconds, peak 1,091.0MB. Timing uses `time.perf_counter`, memory `resource.getrusage`; runtime measurements stay in this evidence log and stdout. Syntax compile passed with bytecode directed to `/private/tmp`. [CALCULATION]

2026-10-14 20:44:37 JST (`date`): independent scratch build exited 0, 3.848 seconds, peak 1,598.7MB; `cmp` exited 0, byte-identical `activity_keys.json`, sha256 `d66428525a110902f7ab94f98026d5b5a14dcb4853957a1655bd9fe16a5ca4ad`. Covered: personal business/output/freight/plain/population keys, generation and white factors, replicate covariance, inherited controls and source hashes. Skipped: service-use fractions and final spending changes (other owners), corrected consumption replicate key and lineage SE (not measured here), shared allocation (brief requests personal), lane-wide rerun (parent integrates peer scripts first). [CALCULATION]
