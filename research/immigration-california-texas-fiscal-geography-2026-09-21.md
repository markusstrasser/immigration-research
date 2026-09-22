# California and Texas: same Mexican-origin share, different white-reference gaps

Date: 2026-09-21. [ROUTING] Pair the two large settlement states. Numbers are 2024 dollars
per standardized person per year unless noted. This is the older **shared all-age partial
ledger**, not the $165–197bn complete account and not the generation-ledger −$6k to −$8k.
Do not scale one onto the other. [FRAMING-SENSITIVE]

## Verdict

California and Texas already have the **same** Mexican-origin population share (~32%).
Matched to **local** third-plus non-Hispanic whites at common ages, California is about
**1.6×** Texas (−$12,133 vs −$7,479). Los Angeles is about **2.3×** Houston (−$17,196 vs
−$7,493). Share of residents does not produce the coastal dollar gap. New-destination
metros in the published table look like Texas, not Los Angeles. Nominal dollars; no
regional price parity. [INFERENCE from the tables below]

## Same share

Texas 31.7–33.5% Mexican-origin, California 31.8–32.5%, ACS state series used in the
sorting memo. [SOURCE: [native sorting](immigration-native-sorting-tiebout-2026-09-18.md)]

2020 Census Detailed DHC-A, POPGROUP 4015 “Mexican”: California 12.20m of 39.58m residents
(30.8%); Texas 9.03m of 29.18m (31.0%). Together **59%** of the 35.84m US Mexican-origin
count. New York 0.50m (1.4% of that US total) — not a Mexican destination.
[SOURCE: `infra/immigration-fiscal/apportionment_2026_09_18/derived/arm_2020_mexican_origin.csv`;
[apportionment](immigration-apportionment-seats-attributable-2026-09-18.md)]

## Gaps vs local whites (and vs all local natives)

CPS ASEC 2025, income year 2024, shared all-age account, each place’s own white age shares.
[DATA: `infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched.csv`;
`infra/immigration-fiscal/metro_match_2026_09_17/derived/metro_matched.csv`]

| Place | vs 3rd+ NH whites | vs all natives | Mexican-origin people |
|---|---:|---:|---:|
| California | **−$12,133** [−14,068, −10,198] | −$7,219 | (state) |
| Texas | **−$7,479** [−9,253, −5,705] | −$4,525 | (state) |
| Los Angeles | **−$17,196** [−21,144, −13,249] | −$8,028 | 4.50m |
| Chicago | −$11,838 | −$8,344 | 1.74m |
| Dallas–Fort Worth | −$9,823 | −$6,016 | 1.88m |
| Riverside–San Bernardino | −$8,621 | −$3,684 | 2.41m |
| Houston | −$7,493 | −$4,293 | 2.05m |
| Phoenix | −$6,721 | −$4,089 | 1.41m |
| National, age only | −$5,734 | −$4,204 | 40.90m |

Every named union interval is adverse. [SOURCE: [stress RESULT](../infra/immigration-fiscal/ledger_stress_2026_09_17/RESULT.md) CA/TX table;
[metro RESULT](../infra/immigration-fiscal/metro_match_2026_09_17/RESULT.md) §5–6]

**San Francisco** metro was built as a group (0.79m Mexican-origin) and **not** given a
single-metro gap. It sits inside the California −$12,133. **New York** was never a metro
group; it is inside `rest_metro` (8.76m — the largest CPS bin, all other identified metros).
[DATA: `metro_populations.csv`; `metro_tests.py` `SINGLE_METROS`]

## What the national match does and does not do

Matching on state or metro **does not** shrink the per-person national gap toward zero
(−$5,734 age-only → −$5,797 metro×age vs whites). It **widens** the national *total*
(−$291bn → −$412bn vs whites) because Mexican-origin residents are concentrated where the
local white benchmark is higher. [SOURCE: same stress and metro RESULTS]

The vs-white jump in LA/CA is partly a **richer white comparison**, not only a worse
Mexican-origin balance. Vs all natives, LA (−$8,028) is close to Chicago (−$8,344).
[INFERENCE]

## “Once the South and Midwest catch up”

If that means **headcount share** toward 32%: Texas is already there and is not Los Angeles.
Dallas, Houston and Phoenix are **−$7k to −$10k** vs local whites.

If that means **CA-like wages, school spending and white earnings** without Mexican-origin
earnings catching up: the **nominal** local vs-white gap can widen. That is a price and
fiscal-capacity story. This lane does not apply regional price parities, so coastal
nominal gaps overstate real-resource gaps and cheaper metros understate them.
[SOURCE: metro RESULT, scope limits]

US-born Mexican-origin fertility is at or below the white level; the Mexican-origin share
of Texans under 30 fell 41.1% → 38.0% from 2010 to 2023. Automatic share catch-up is not
in that demography. [SOURCE: ladder 88; generation incarceration memo §4]

Native high-AGI out-migration tracks state tax rates, not Mexican-origin share; Texas has
an AGI **inflow**. [SOURCE: [Tiebout](immigration-native-sorting-tiebout-2026-09-18.md)]

Political CA–TX divergence at the **same** Mexican-origin share is conversion of the
electorate, not composition. [SOURCE: [county vote panel](immigration-political-trajectory-county-panel-2026-09-19.md)]

## Limits

Partial account (modeled taxes, MEPS medical, mixed-year state parameters). Not an admission
effect. Thin CPS cells in some metros; the published six were chosen in the brief. Traffic
congestion unpriced. Complete-account state splits were not rerun here. Do not mix these
per-person gaps with the superseded $8,498 / $5,177 per native-headed household in California
and Texas ([who pays](immigration-fiscal-gap-incidence-who-pays-2026-09-18.md), September 19
correction).

## Instrument

LLM-assisted routing of executed tables. Consult `notes/llm-bias-caveat.md`.
