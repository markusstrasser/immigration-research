# California and Texas: same Mexican-origin share, different white-reference gaps

Date: 2026-09-21. [ROUTING] Pair the two large settlement states. Numbers are 2024 dollars
per standardized person per year unless noted. This is the older **shared all-age partial
ledger**, not the $389–461bn complete account and not the generation-ledger −$7k to −$9k.
Do not scale one onto the other. [FRAMING-SENSITIVE]

## Verdict

California and Texas already have the **same** Mexican-origin population share (~32%).
Matched to **local** third-plus non-Hispanic whites at common ages, with the income tax the
survey misses placed on the main case's keys (item T), California is about **1.6×** Texas
(−$15,228 vs −$9,267) and Los Angeles about **2.3×** Houston (−$21,083 vs −$8,977). With
taxes as the survey reports them the ratios hold (−$12,133 vs −$7,479; −$17,196 vs −$7,493).
The added tax rests on few records: the ten largest white households carry 67% of whites'
added tax in California and 98% in Texas. Share of residents does not produce the coastal
dollar gap. No other published metro reaches Los Angeles: Houston −$8,977, Phoenix −$10,945,
Chicago −$11,949 and Dallas–Fort Worth −$14,744, the last between Texas and Los Angeles, near
California's level, on an interval that reaches Texas's. Nominal dollars; no regional price parity. [INFERENCE from the
tables below]

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
The two gap columns add the income tax the survey misses (item T); the survey-tax column keeps
taxes as the survey reports them; the share column is the ten largest white SPM units'
(households') share of the place's white T.
[DATA: `infra/immigration-fiscal/ledger_stress_2026_09_17/derived/state_matched_T.csv` and
`state_matched.csv`; `infra/immigration-fiscal/metro_match_2026_09_17/derived/metro_matched_T.csv`
and `metro_matched.csv`; both lanes' `derived/t_concentration.csv`]

| Place | vs 3rd+ NH whites | vs all natives | Survey taxes: vs whites / natives | Top ten units' share of white T | Mexican-origin people |
|---|---:|---:|---:|---:|---:|
| California | **−$15,228** [−18,291, −12,164] | −$8,912 | −$12,133 / −$7,219 | 67% | (state) |
| Texas | **−$9,267** [−12,530, −6,004] | −$5,290 | −$7,479 / −$4,525 | 98% | (state) |
| Los Angeles | **−$21,083** [−27,783, −14,383] | −$10,077 | −$17,196 / −$8,028 | 91% | 4.50m |
| Chicago | −$11,949 | −$8,481 | −$11,838 / −$8,344 | 440% | 1.74m |
| Dallas–Fort Worth | −$14,744 [−22,027, −7,461] | −$8,467 | −$9,823 / −$6,016 | 120% | 1.88m |
| Riverside–San Bernardino | −$11,944 [−23,967, +79] | −$5,004 | −$8,621 / −$3,684 | 118% | 2.41m |
| Houston | −$8,977 | −$5,127 | −$7,493 / −$4,293 | 147% | 2.05m |
| Phoenix | −$10,945 | −$6,880 | −$6,721 / −$4,089 | 114% | 1.41m |
| National, age only | −$6,910 | −$5,170 | −$5,734 / −$4,204 | 19% | 40.90m |

A share above 100% means the place's other white records carry a negative T on net; nationally
the top ten carry 19%. With the income tax the survey misses every named union interval is
adverse except Riverside's, which reaches +$79 against whites and +$119 against all natives;
with taxes as the survey reports them all are adverse. The national key's split across states
is itself uncertain; re-raked on IRS state data it widens the California–Texas difference. [SOURCE: [stress RESULT](../infra/immigration-fiscal/ledger_stress_2026_09_17/RESULT.md) CA/TX table and its item-T revision;
[metro RESULT](../infra/immigration-fiscal/metro_match_2026_09_17/RESULT.md) §5–6 and its item-T revision]

**San Francisco** metro was built as a group (0.79m Mexican-origin) and **not** given a
single-metro gap. It sits inside the California −$15,228 (−$12,133 with taxes as the survey
reports them). **New York** was never a metro
group; it is inside `rest_metro` (8.76m — the largest CPS bin, all other identified metros).
[DATA: `metro_populations.csv`; `metro_tests.py` `SINGLE_METROS`]

## What the national match does and does not do

Matching on state or metro **barely moves** the per-person national gap: with the income tax
the survey misses it is −$6,910 age-only and −$6,818 metro×age vs whites, $92 narrower
(−$5,734 and −$5,797 with taxes as the survey reports them); both moves sit inside one
standard error. It **widens** the national *total*, from −$339bn age-only to −$492bn
metro×age vs whites (−$291bn to −$413bn with taxes as the survey reports them), because
Mexican-origin residents are concentrated where the local white benchmark is higher.
[SOURCE: same stress and metro RESULTS]

The vs-white jump in LA/CA is partly a **richer white comparison**, not only a worse
Mexican-origin balance. Against whites Los Angeles sits far below Chicago (−$21,083 vs
−$11,949); against all natives the two are within $1.6k (−$10,077 vs −$8,481) and their
intervals overlap. With taxes as the survey reports them LA (−$8,028) is close to Chicago
(−$8,344) against natives. [INFERENCE]

## “Once the South and Midwest catch up”

If that means **headcount share** toward 32%: Texas is already there and is not Los Angeles.
Dallas, Houston and Phoenix are **−$9k to −$15k** vs local whites with the income tax the
survey misses and −$7k to −$10k with taxes as the survey reports them; Los Angeles is −$21k
(−$17k).

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

Partial account (modeled taxes, MEPS medical, mixed-year state parameters). The income tax
the survey misses is placed by the main case's national key; inside one state or metro a
handful of top-income white households carry most of it, and the intervals cover their
sampling, not the key's transport to one place. Not an admission
effect. Thin CPS cells in some metros; the published six were chosen in the brief. Traffic
congestion unpriced. Complete-account state splits were not rerun here. Do not mix these
per-person gaps with the superseded $8,498 / $5,177 per native-headed household in California
and Texas ([who pays](immigration-fiscal-gap-incidence-who-pays-2026-09-18.md), September 19
correction).

## Instrument

LLM-assisted routing of executed tables. Consult `notes/llm-bias-caveat.md`.

## Revisions

- 2026-10-08: restated the state and metro gaps with the income tax the survey misses, put the survey-tax figures and the few-records caveat beside them, and named the live complete account, because the white-reference ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T; [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)) and the state and metro lanes print it beside the survey's taxes: California −$12,133 → −$15,228, Texas −$7,479 → −$9,267, Los Angeles −$17,196 → −$21,083, Houston −$7,493 → −$8,977, Dallas–Fort Worth −$9,823 → −$14,744; Riverside's interval now reaches +$79, so not every named interval is adverse; metro matching narrows the national per-person gap by $92 instead of widening it by $63; the generation-ledger range −$6k to −$8k → −$7k to −$9k; the complete account $165–197bn → $389–461bn. Concept affected: state and metro geography of the white-reference gap.
