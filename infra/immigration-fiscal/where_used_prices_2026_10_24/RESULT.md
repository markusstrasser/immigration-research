**Verdict:** The complete national where-used correction is **not identified**. K-12 operating and college instruction/support where-enrolled pricing are already in oct16. Matched municipal parks give a conditional **−$0.175/−$0.205bn** correction; the covered-college gross-book-asset proxy gives **−$0.452bn** at both ends, but leaves material assets unallocated. With the brief's stipulated K-12 capital input, their partial sum is **+$0.728/+$0.698bn**. Correcting that sibling's denominator for the already-adopted K-12 factor makes the same partial sum a diagnostic **−$0.085/−$0.115bn**. Neither is a complete national estimate or an adopted change. Oct16 stays **$368.030–436.562bn**. [CALCULATION: `derived/case_scenarios.csv`, `case_prices.cjs`; DATA: `college_finance_coverage.csv`]

Dollars below are 2024 $bn per year on the income-year-2024 account, specifications
16/11, mean of both imputation methods, unless explicitly labeled raw FY2022.
These prices do not estimate removal responses. Perspective: cost to other
residents under the adopted account. [FRAMING-SENSITIVE]
Capital-return changes are imputed resource costs, not debt flows or cash savings.

## Incremental components

| Component | Factor against existing key | Δ low / high, $bn | Status |
|---|---:|---:|---|
| K-12 operating, requested k≈1.034 | Existing **1.0341917412** | **0 / 0** new | Already adopted |
| College instruction/support operating | **1.000000** new; current cost/FTE relative **0.907140** | **0 / 0** new | Primary key reproduced |
| College gross depreciable book assets | **0.844693** | **−0.452 / −0.452** | Covered-unit proxy |
| College responsive-assets expense proxy | **0.892784** | **−0.312 / −0.312** | Functional-allocation assumption |
| College net-depreciable book assets | **0.851742** | **−0.432 / −0.432** | Alternative book valuation |
| Matched municipal parks operations | **0.920220**, case state weights | **−0.175 / −0.205** | Conditional fiscal bridge |
| National park capital | **Not identified** | No measured point correction | Missing monetary stock |

[CALCULATION: `college_factors.csv`, `parks.json`, `case_scenarios.csv`]

## K-12: two baseline overlaps

`main_case_2026_09_24/package.cjs` sets `CENTRAL.k='preferred'` and applies the
school lane's preferred price. The adopted `user_fee_allocation_2026_10_07/fee_lines.py`
recovers **k=1.0341917412164008** directly from those edits. Another factor 1.034
would repeat it. A source-school-only neutral control through `evaluateFull`
isolates **$3.791930/$4.586191bn** of already-included operating pricing on the
original union; this is not a new increment or a total for all additions.
[SOURCE: those primary callers; CALCULATION: `case_prices.json`
`existing_k12_original_union_operating_price_bn`]

Toggling `spec.school` is not a valid school-price control: it rescales the whole
folded education line, including postsecondary, libraries and tuition. The lane
uses the source school-only edit. [SOURCE: September 24 `stateFor`, `educationShifts`]

The capital sibling's stipulated **+$1.355720bn** uses denominator **0.9541966043**.
The original-union capital key already contains the preferred price:
`0.1638524451 × 1.0341917412 = 0.1694548455` after the fee rekey. Its corresponding
current-price denominator is **0.9868222477**. Dividing the sibling's factors by
the embedded k gives **+$0.542615bn** (return **+$0.450560bn**, depreciation
**+$0.092055bn**). The original-union overlap is established; transporting that
denominator adjustment to all additions remains an assumption. The sibling is
untouched, and both readings are retained. [DATA: adopted fee bridge and
`school_capital_where_enrolled_2026_10_24/derived/summary.json`; CALCULATION: `case_prices.json`]

## Colleges

Primary HD/EF/FLAGS/F1A and ACS records reproduce the existing E&R share
**0.11506996999009124** exactly; its union-frame share is **0.11589579410930383**.
The existing key costs **9.286% less** than a simple cost-adjusted FTE allocation
(graduate weight 2). A second community-college discount counts that composition
twice. [CALCULATION: `build.py`, `colleges.json`; DATA: adopted `fee_lines.json`;
ASSUMPTION: Hispanic/ACS translation and graduate cost weight]

Item15's **0.8857748497** response distinguishes responsive instruction/support
from fixed public service; research is excluded centrally and tuition/Pell keep
their keys. The matched responsive-gross factor **1.006700** gives a conditional
**+$0.287bn** with existing tuition dollars fixed. Reweighting the conditional net
budget instead gives **1.175123**, **+$4.990bn**. Only **87.66%** of that net budget
has assigned students, with 30 negative institution net amounts. The latter is a
construction sensitivity, not evidence for adopting a $4.99bn increase.
[SOURCE: `spending_keys_r5_2026_10_15/{college.py,items.cjs}`;
CALCULATION: `college_factors.csv`, `college_finance_coverage.csv`, `case_scenarios.csv`]

Asset coverage is the consequential limit:

- GASB covers **98.25% of public FTE**, **99.83% of group FTE**, but matched
  student-bearing units hold only **88.12% of gross depreciable assets**.
- **$96.009bn** lacks student weights, including **$68.020bn** at the University
  of California system office. It is not silently assigned zero group use.
- The 18 fall/annual-state-raked × graduate-weight × asset-concept arms reduce
  the case **$0.243–0.503bn on the covered-unit construction**.
- Allocating the unknown gross-book assets from zero to fully to the group gives
  a conditional **−$0.745 to +$2.262bn** correction. Across gross, responsive-proxy
  and net-depreciable concepts the envelope is **−$0.830 to +$3.227bn**. Its sign
  is not identified. These are allocation bounds, not confidence intervals.

[DATA/CALCULATION: `college_unallocated_finance.csv`, `college_finance_coverage.csv`, `case_scenarios.csv`]

Historic-cost whole-campus assets include research, hospital and auxiliary uses;
they do not identify replacement-cost instructional stock. Four negative
constructed net-plant values fail the asset screen. Public FASB units remain
separate. The case's library share is held; the higher-education fraction is
`kappa × U / U_capital`. Applying its factor to additions/coverage/count is explicit
transport. [CALCULATION: `build.py`, `case_prices.cjs`; DATA: `college_public_fasb.csv`]

## Parks

The primary CoG/PID–ACS join prices **19,367 municipalities**, **$20.800922bn**
of FY2022 current operations: **98.65%** of municipal E61 and **51.12%** of all
state/local E61. Their boundaries hold **62.59%** of US residents and **77.78%**
of Mexican-origin residents. This is provision by residence, not visitation.
[DATA/CALCULATION: `park_municipalities.csv`, `parks.json`]

The covered-city factor is **0.933010**; versus a national municipal-per-resident
baseline it is **1.159374**, because more group members live inside municipalities.
Against state municipal prices it is **0.916256** with ACS state weights, **0.920220**
with case state weights. None prices every recreation/culture line.
[CALCULATION: `parks.py`, `park_states.csv`]

The case already uses state E61+F61+E52+F52 prices. Its primary reconstructed index
is **1.0746786530**. Replacing only each state's matched municipal E61 fraction
changes that index by **−0.0316058872**, yielding **−$0.175/−$0.205bn** on oct16.
Federal, library, nonmunicipal and capital prices stay held. FY2022-to-FY2024,
cash-to-NIPA, residents-to-users and population-addition transport are assumptions;
this is not an observed fiscal saving. [CALCULATION: `parks.py`, `case_prices.cjs`]

Best bounds from these sources remain wide:

- The 34 unmatched municipalities hold **$0.283701bn**. Their raw FY2022 price
  change is bounded by **[−$0.009655bn, +$0.274046bn]** versus the ACS state baseline.
- All unpriced E61 totals **$19.888839bn**; its raw allocation change is bounded
  by **[−$2.166357bn, +$17.722482bn]**. These are not oct16 estimates.
- Holding stock and response fixed, allocating zero to all of the state/local
  recreation stock to the group gives model changes **[−$1.115bn, +$7.302bn]** at
  low, **[−$1.172bn, +$7.674bn]** at high, with federal capital held. No inspected
  geographic replacement-value data identifies a narrower capital price.

[DATA/CALCULATION: `parks.json`, `case_scenarios.csv`; ASSUMPTION: nonnegative allocation, held responses]

TPL's 89 exact-FIPS places corroborate a lower operating price (**0.903811**);
acreage (**0.662899**) and construction flow (**0.663765**) are separate measures.
PS-prefixed regional systems are excluded and Des Moines is included: this is
not the full top-100 universe. Acreage, ParkServe and PAD-US polygons do not price
capital, so a large polygon pull would not resolve the monetary-stock gap.
[SOURCE: primary TPL tables/methodology; CALCULATION: `park_tpl_cities.csv`; INFERENCE: identification limit]

## Combined readings

| Partial package, incremental to current oct16 | Δ low / high, $bn |
|---|---:|
| Stipulated K-12 capital + matched municipal parks; other unknowns held | **+1.180 / +1.151** |
| Above + covered-college gross-book capital proxy | **+0.728 / +0.698** |
| Same proxies, with K-12 corrected-denominator diagnostic | **−0.085 / −0.115** |
| Stipulated book-proxy package + net-responsive college construction sensitivity | **+5.718 / +5.688** |

[CALCULATION: `case_scenarios.csv`. All original dynamic posts use `evaluateFull`;
both already-included operating refinements add zero.]

There is no verified complete national item to adopt. Missing asset allocations,
functional replacement values, other governments' geographic prices and the
cash-to-NIPA bridge can change the sign. No central-case edit, stage, merge or
commit was performed. [INFERENCE from measured coverage]

LLM directional bias remains an instrument risk (`notes/llm-bias-caveat.md`).
Mitigations are symmetric primary reconstruction, both price directions,
unidentified signs retained, and independent repo-access review. Model review does
not verify the empirical bridges.

## Execution and validation log

- 2026-10-23T16:46:30Z — Wrote required verdict stub; read brief, CLAUDE and current conventions.
- 2026-10-23T16:53:12Z — Traced institution-weighted college key and college/library split; began geographic construction.
- 2026-10-23T17:05:18Z — External source disk unavailable; recovered five identical-hash public inputs into the lane cache.
- 2026-10-23T17:14:14Z — Fourteen acquired source/codebook files; full build exited 0 in 29.74 s, 374,800,384 bytes max parent RSS. Case adapter passed 897 gates; 15 pytest tests passed.
- Independent read-only diff review covered all five source files including `.cjs`, principal callers and outputs; found no material implementation defect and independently passed all 15 tests. Empirical bridges remain unresolved.
- 2026-10-23T17:20:54Z — Required offline `rerun_lane.py` exited **0**: acquisition, full primary build and pytest each exited **0**, **IDENTICAL: 28/28 files unchanged**. All **15 tests** and **897 case gates** passed. Dataset-register diff passed whitespace checks. No Git metadata was changed; peer directories were preserved.
