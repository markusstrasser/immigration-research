**Verdict:** The code omits 659,301 native civilian Mexican-origin reporters (SE 58,440), including 456,936 with one US-area-born parent (SE 48,569). The requested one-US-parent candidate, including 60,500 directly identified nonreporting children, adds **$2.893 / 3.755bn** to v7's set and **$2.031 / 2.893bn** to its cash set. Both set endpoints are below the review's $5bn bar. The all-reporters arm with those children adds **$5.560 / 6.750bn**: both set endpoints exceed it. These are conditional prices at the current case's responses, not an adopted rebase. [DATA: `derived/counts.csv`; CALCULATION: `candidate.py` → `derived/candidate.csv`]

## Rules and population

| Fix/rule | Count or change | Gates/files |
|---|---|---|
| Native civilian Mexican-origin reports outside the canonical union | 283 records; 659,301 persons, SE 58,440 | `counts.csv`; all 160 replicates; native weights unchanged by row 4 |
| Central: exactly one US-area-born parent, classified G3+ | 204 records; 456,936 persons, SE 48,569 | `completion.py`; disjoint from G1/G2/existing G3+ |
| Neither parent US-area-born, broad arm only | 79 records; 202,365 persons, SE 33,142 | `parent_birthplaces.csv`; Mexican-origin report observed, ancestry route unresolved |
| Biological co-resident parent-pair nonreporters | 27 records; 60,500 persons, SE 20,476 | linked parent records and child birthplace fields agree; outside the two-US-parent loss universe |
| All-age loss extrapolation, beside | 288,579 additional nonreporters, SE 117,238 | child loss-to-identifier ratio × all-age central reporters; explicitly assumed transport |
| Item 5b, reporting additions only | +0.139bn central / +0.259bn broad | exact return-level rebuild; 18 original parts reproduce within 1e-9bn |
| Item 5b, reporting additions plus observed nonreporters | +0.325bn central / +0.445bn broad | both below $0.5bn; original lineage term fixed |

[CALCULATION: `completion.py`, `credits_interaction.py`, `candidate.py` → `derived/`]

The native restriction is CPS PRCITSHP 1–3, not PENATVTY 57 alone; civilians are PRPERTYP 2 or under 15. Mexican origin is PRDTHSP 1. The existing union is the unchanged `frame.masks()` definition: foreign-born Mexico-born; native with a Mexico-born parent; native Mexican-origin reporter with both parents born in US areas. The omitted reporters have no Mexico-born parent and fail the last parent-birthplace condition. “One US parent” means exactly one birthplace in 57, 60, 66, 69, 73, 78. [SOURCE: Census CPS ASEC 2025 public-use person/household/replicate files, pinned `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`; DATA: `generation_account_2026_09_24/frame.py`]

| Parent-birthplace type | Records | Persons | Replicate SE |
|---|---:|---:|---:|
| Father US-area-born, mother elsewhere | 93 | 196,285 | 26,139 |
| Mother US-area-born, father elsewhere | 111 | 260,651 | 40,252 |
| Neither US-area-born | 79 | 202,365 | 33,142 |
| All omitted | 283 | 659,301 | 58,440 |

All 17 five-year bands, ending 80+, are in `counts.csv`. Of the omitted reporters, 310,792 are under 18 (SE 46,923); 288,243 have a co-resident union-member parent (SE 43,069). Counts reproduce the parent's probe, with no rounding target imposed. Row 4 reweights only specified Mexico-born citizenship/state cells; these native records retain their published weights in every replicate. [CALCULATION: `completion.py` → `summary.json`, `counts.csv`]

The central membership rule is the requested ancestry interpretation: Mexican origin carried through the US-born parent. That is an inference for unlinked adults; parent birthplaces plus the person's origin report do not observe the parent's ancestry. The neither-US-parent group has two third-country/other-coded parent birthplaces and a Mexican-origin report, not a Mexico-born parent. The records cannot establish that its Mexican ancestry runs through an earlier Mexican immigrant rather than an origin-reporting/coding discrepancy. Include it in the broad report-based arm; do not silently infer a Mexican grandparent. The current code consequently fails the unqualified prose definition “the US-born who report Mexican origin.” [INFERENCE; DATA: `parent_birthplaces.csv`; SOURCE: `decisions/2026-10-05-main-case-v5.md` Context]

## Annual pricing, one change from v7

Each entry is net annual cost to other residents in income year 2024 under the case's static removal account. Personal specifications 16 / 11, national amounts, finite-removal responses, capital-return parameters, original 3.04M addition and C3 stay fixed. The cash set switches pension benefits to payment timing; it still contains the case's imputed capital return. Dollar amounts are model output from observed survey keys and the case's assumptions, not observed marginal bills or causal ancestry effects. [ASSUMPTION; CALCULATION: `candidate.py`]

| Candidate increment, $bn low / high | Set | SE, set | Cash set | SE, cash |
|---|---:|---:|---:|---:|
| Central reporters only | 1.875 / 2.665 | 1.711 / 1.707 | 1.015 / 1.804 | 1.813 / 1.803 |
| **Central reporters + observed nonreporters** | **2.893 / 3.755** | **1.694 / 1.691** | **2.031 / 2.893** | **1.798 / 1.789** |
| All reporters only | 4.542 / 5.660 | 1.890 / 1.908 | 3.418 / 4.536 | 2.019 / 2.026 |
| All reporters + observed nonreporters | 5.560 / 6.750 | 1.873 / 1.893 | 4.434 / 5.624 | 2.003 / 2.012 |
| Central reporters + all-age extrapolated loss | 3.939 / 5.285 | 1.881 / 1.933 | 2.711 / 4.057 | 1.980 / 1.998 |
| All reporters + same central-universe extrapolated loss | 6.606 / 8.280 | 2.043 / 2.109 | 5.114 / 6.789 | 2.167 / 2.198 |

[CALCULATION: `derived/candidate.csv`; full paired replicate vectors in `candidate.json`]

The central observed candidate's conditional counterpart is **$342.445 / 427.404bn**, cash **$266.457 / 351.415bn**. Its reporting union has **40,169,429** people; its lineage including observed losses has **43,269,649**. The broad observed arm has **40,371,795** reporting-union people and **43,472,014** lineage people; counterpart **$345.112 / 430.399bn**, cash **$268.860 / 354.147bn**. The central all-age extrapolation implies **43,497,728** lineage people. Baseline counts are fixed for these increment SEs. [CALCULATION: `candidate.json`]

The central observed correction misses the $5bn bar at both endpoints. The broad reporters-only set passes at its high end; the broad observed set passes at both, and its cash set at the high end. The central all-age extrapolation passes at the set's high end only. These are point-estimate comparisons, not confidence statements that the true correction exceeds $5bn; SEs are substantial. All 24 endpoint/arm rows carry the explicit Boolean test. [CALCULATION: `candidate.csv` `passes_5bn_bar`]

## Own-record method and controls

`person_adapter.py` imports the unchanged household distribution kernel and uses AST syntax anchors to stop after it constructs priced pieces. It retains each omitted person's unmasked key before the kernel restricts its vector to members. All pre-boundary original gates run unchanged. It uses the current member machinery's person pension/on-books arm and recalibrates every within-generation denominator for each replicate. The positive control first reproduced the current set and cash totals in all 161 weight columns, with maximum error **1.65e-12bn**, against the required **1e-6bn**. [CALCULATION: `derived/gates.json`]

This is an extension of the current member distribution prices. Ordinary receipt, transfer, school, household, age and medical keys use the omitted records themselves. The source kernel distributes corrected G3+ totals, including the placed original lineage, over G3+ records; this carries its existing within-generation pooling assumptions. Its pension vectors reuse the existing September 29 cached person model, including the nonmember reference rules documented in `person_accrual.py`, while keeping current v7 generation pension totals. Justice use is the source's age-18–64 proxy; MEPS health is transported payer/age/nativity cell use, not these persons' medical bills. These limitations remain explicit. [DATA: `within_group_distribution_2026_09_29/households.py`, `person_accrual.py`; ASSUMPTION]

Two lines cannot use the omitted records in that machinery: the tenant-property key is masked to the existing union, and lane constants have no person key. They take **pure G3+ per-person costs by five-year band from the case's added-people engine route**. `fallback_lines.csv` lists both lines at all endpoints/sets; no zero fallback is silently substituted. Production and capital pieces use the source member rules. [CALCULATION: `added_band_prices.cjs` → `added_band_prices.json`; `completion.py` → `fallback_lines.csv`]

The v7 job-capital rule needs a separate extension: the old household allocation spreads those receipt totals on incidence keys. `job_record_key.py` instead evaluates the omitted workers' own wages/industry records under the live source's industry map, thin-cell pools, $1M wage pooling, mining exclusion and G3+ fill-in factor 0.9906598510. It removes the inherited incidence-based projection on the four job-tax receipt lines before inserting the exact three source job-tax quantities. The original G3+ source tax amounts reproduce within **4.98e-14bn**, and national line totals close in every replicate within **4.55e-13bn**, against 1e-6bn gates. No production capital-tax term is added. [CALCULATION: `gates.json`, `pricing_lines.csv`; DATA: `job_capital_taxes_2026_10_14/derived/item.json`]

## Nonreporting children and extrapolation

The biological central sample is 73 native civilian children under 18 with both parents linked, exactly one US-area-born Mexican-origin parent and the other born outside US areas and Mexico. Their own parent-birthplace fields must agree with that universe. It contains 46 reporting children (95,796 weighted) and 27 nonreporters (60,500 weighted): **38.71% loss, SE 10.15 percentage points**. The nonreporter-to-reporter ratio is **0.63155, SE 0.27484**. Including step/adoptive parents gives 40.25%, SE 9.96pp, and 65,098 nonreporters. [CALCULATION: `summary.json` `identity_loss`]

There are **zero nonreporters sharing a linked parent pair with a reporting child** in this sample. Thus this measures children of the specified parent pairs, not directly observed discordant sibling pairs. The sample excludes absent parents, inconsistent birthplace fields and adults. It establishes identity loss within that observed universe, not an all-age national attrition rate. [DATA: `summary.json` `nonreporter_with_reporting_sibling`; INFERENCE]

Fifteen nonreporters (38,589 weighted) have a native reporting parent with a Mexico-born parent: price them at the case's third-generation loss blend, (1−C3) G3+ + C3 white, C3=0.5567. Twelve (21,911 weighted) have no measured Mexico-born grandparent through that native parent: price them as later losses, G3+. They retain their **observed child ages**. This applies the case's existing model to this newly observed class; the transfer of C3 is an assumption, not a new measurement of their economic selectivity. [CALCULATION: `count_replicates.json`, `added_band_prices.json`; ASSUMPTION]

`added_band_prices.cjs` prices 17 unit age bands through the current full engine and reproduces the original later and third-generation-rate lineage parts at both ends and sets within **4.13e-13bn**, tolerance 1e-6bn. Four white state-index products are nonadditive across unit bands: their raw original-mix control differs by **+$0.003902bn**. They are attributed proportionately over the raw profiles to conserve each original-mix line total, with that calibration frozen for new ages [ASSUMPTION]. Raw and calibrated rates remain in the output. Its effect on the observed new children is **−$0.000063bn**, far below the $5bn review bar. [CALCULATION: `added_band_prices.json` metadata; `candidate.json`]

Applying the child loss-to-identifier ratio to the 456,936 central all-age reporters implies **288,579** nonreporters, SE 117,238. That arm uses the reporters' measured age distribution as a proxy for the unobserved population's ages and the observed loss sample's ancestry-class share for its blend. It does **not** add the observed 60,500 again. This is a stationary transport assumption; cohort history, parent survival/co-residence and unidentified adult ancestry could invalidate it. No loss is extrapolated from the neither-US-parent group. Keep this arm beside the candidate until those assumptions have evidence. [ASSUMPTION; CALCULATION: `candidate.py`]

## Household interactions and no double counting

Item 5 is the allocation choice, with no cell edits. Personal allocation remains fixed; ordinary source person pricing already applies it. Adding members does not change the source's SPM unit composition or its per-person sharing vectors; we do not claim a newly measured hypothetical shared-minus-personal band. Item 5b is a membership-dependent credit correction and is rebuilt jointly on the expanded union, including existing members' returns affected by the new boundary. [DATA: v7 package/item contracts; CALCULATION: `credits_interaction.py`]

The canonical item 5b net is **$4.298545385bn**. The exact joint corrections are +$0.139296bn (SE 0.101176) for central reporters, +$0.259073bn (SE 0.127891) for all reporters; with observed nonreporters, +$0.325484bn (SE 0.129746), +$0.445261bn (SE 0.144589). The latter alter 60 / 79 sampled households' credit interactions. All are **below $0.5bn**. [CALCULATION: `credits_interaction.json`]

The inherited R6 projection is removed from the omitted reporters' FIT/refundable-credit prices before the exact joint delta is added. Observed nonreporters' G3+ age prices also exclude R6's fixed $213.97 per member before the exact joint credit delta enters; the white-priced part originally carries zero. The unidentifiable all-age extrapolation instead retains the case's imputed per-G3-person credit rule and adds only the exact reporting-union delta. The original 3.04M credit term stays fixed. [CALCULATION: `completion.py`, `candidate.py`]

Original union members and new records are disjoint. New reporters and new observed nonreporters are disjoint by PRDTHSP. New records have fewer than two US-area-born parents, whereas the original addition's multiplier universe requires two: none is counted again there. The existing 3.04M is a modeled population, not a list of CPS person IDs; this is a **definition-level disjointness gate**, not a purported linkage to invisible individuals. All replicate weights conserve under membership reassignment; compensated national sums preserve the 1e-6-person gate without relaxing it. [DATA: pinned `dt_replication.py` multiplier universe; CALCULATION: `gates.json`, tests]

## Recommendation and verification

Offer the **one-US-parent reporters plus directly observed biological nonreporters** as the bounded central completion; retain the all-reporters arm as the written broad union rule and the all-age extrapolation beside both. Repair the membership definition even though the bounded central prices are below $5bn: the claimed coverage currently omits an observable class. Do not present the all-age transport as observed. Adoption would need a parent-owned case rebase and its group-size response/consumer checks; this lane freezes those responses to isolate the candidate's person/key effect and does not edit the frozen case or builders. [INFERENCE; FRAMING-SENSITIVE]

The leading explanation is the two-US-parent code restriction; the strongest alternative for the neither-US group is unresolved ancestry/report coding. Larger linked-parent/grandparent evidence and age-specific adult nonreporting measurements would discriminate. The LLM's framing dispositions remain a limitation; the counts, arithmetic, gates and source pins are inspectable rather than inferred from prose. [DATA: source masks; INFERENCE; SOURCE: `notes/llm-bias-caveat.md`]

Reproduction, from the repo root (all commands write only this lane):

```sh
node infra/immigration-fiscal/union_completion_2026_10_14/snapshot.cjs
node infra/immigration-fiscal/union_completion_2026_10_14/added_band_prices.cjs --out infra/immigration-fiscal/union_completion_2026_10_14/derived/added_band_prices.json
uv run --no-project python3 infra/immigration-fiscal/union_completion_2026_10_14/verify_inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/union_completion_2026_10_14/completion.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/union_completion_2026_10_14/credits_interaction.py --include-siblings
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/union_completion_2026_10_14/candidate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/union_completion_2026_10_14/test_completion.py -q
```

`inputs/pins.json` pins 60 source/cache/primary-file hashes. New code is rederivable from those inputs; no download or source mutation was needed. `person_adapter.py` and `job_record_key.py` are imported libraries, executed by `completion.py`, and receive `--allow-unrun` only because `rerun_lane.py` detects scripts by command-string names rather than import tracing.

Log (UTC from `date -u`; timings and memory from Python `perf_counter`/`getrusage`, not `/usr/bin/time -l`):

- 2026-10-14T11:51:13Z: own-record controls completed; job source control integrated.
- 2026-10-14T11:59:24Z: exact added-person age control read; four gates pass.
- Last directly timed completion build: exit 0, 16.34s, peak 2.25GiB; final 122 gates pass, including line-export closure. Credits build: exit 0, 12.68s, peak 2.15GiB. These measurements are execution evidence, not fingerprinted derived bytes.
- 2026-10-14T12:13Z: final `rerun_lane.py` finished **IDENTICAL: 24/24**, all seven commands exit 0, five tests pass. Wrapper measurement: 104.06s; child peak RSS 1,539,440,640 bytes. Log: `_cache/rerun.log`. The two `--allow-unrun` names are `person_adapter.py`, `job_record_key.py`, both imported and exercised by the completion command. No source changes followed this rerun; only this execution receipt and the scratch handoff were finalized.
