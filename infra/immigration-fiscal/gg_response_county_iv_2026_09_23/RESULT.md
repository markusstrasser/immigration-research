**Verdict:** The county IV design can't estimate this parameter precisely enough to test the adopted
0.59–0.84. It doesn't contradict the range either, so the decision's revisit trigger is not met, and
this lane proposes no change to the main case ($203.2–249.6bn).

- **Windows without the broken 2022 wave.** The industry-mix instrument gives population-weighted
  elasticities of 0.28–1.49 across 17 specifications, for example 0.91 (SE 0.93, effective F 40.7).
  Every Anderson-Rubin 95% set contains 0, 0.59, 0.84 and 1; a typical one runs from −0.94 to 2.88.
- **The brief's main window (2012→2022).** Its negative weighted estimates (−2.16 and −3.26) come
  from a reporting break. In the July 2026 re-release of the 2022 Census unit file, local financial
  administration doubles to $39.9bn. The rise sits in NYC, Cook County, Philadelphia and Florida;
  the published 2022 table shows $23.7bn.
- **The immigrant settlement instrument fails here.** It has no first stage before 2017. After
  that, its first stage has the wrong sign.

[CALCULATION: `derived/estimates.csv`, `derived/estimates_summary.json`]

Model: claude-opus-5-5[1m]. Date: 2026-09-23. Lane: `infra/immigration-fiscal/gg_response_county_iv_2026_09_23/`.

## What was estimated

Unit: 3,098 county areas. Local current operations on financial administration, central staff and
general public buildings (Census E23+E29+E31) are summed over every local government in the area.

Model: Δ ln real spending on Δ ln population, with state fixed effects (state × period when stacked)
and base-year log population. Standard errors are clustered by state (48 clusters, CR1).

Inference: the Montiel Olea–Pflueger effective F (τ = 10% critical value 23.1) and the
Anderson-Rubin 95% set (AR), exact for one instrument and on a 0.001 grid for two.

Instruments:
- **(a) Bartik:** base-year County Business Patterns shares by 3-digit NAICS times national
  leave-one-out employment growth.
- **(b) Immigrant settlement:** 2000 Census county shares by origin times the national leave-one-out
  change in each origin's foreign-born stock. The changes come from ACS 5-year windows centred on
  the end years; the instrument is divided by base-year population.

The tables below cover the primary outcome over all counties. `derived/estimates.csv` holds all 780
rows, including 308 IV specifications for the primary outcome.

**Population-weighted** (β, SE; effective F; AR 95% set):

| Window | OLS | (a) Bartik | (b) Immigrant | (a)+(b), Hansen J p |
|---|---|---|---|---|
| 2012→2022 (brief main) | 0.27 (0.38) | −2.16 (1.71); F 59.0; [−5.82, 1.14] | −5.06 (7.50); F 27.8; [−25.5, 7.23]; first stage **−0.74** | −3.26 (3.55); F 40.9; [−5.09, 1.25]; p 0.61 |
| Stacked 2012→17, 2017→22 (brief) | −0.42 (0.80) | −1.11 (1.85); F 44.6; [−5.44, 2.19] | −5.66 (6.71); F 32.1; first stage **−0.80** | −3.74 (4.18); F 35.2; [−4.59, 3.16]; p 0.36 |
| 2007→2017 | 0.49 (0.18) | 0.91 (0.82); F 15.2; [−0.84, 2.90] | F 1.0; whole line | 0.37 (1.20); F 7.5; [−1.28, 2.98]; p 0.57 |
| Stacked 2007→12, 2012→17 (added) | 0.58 (0.17) | **0.91 (0.93); F 40.7; [−0.94, 2.88]** | F 0.5; whole line | 0.58 (0.93); F 12.2; [−1.42, 2.91]; p 0.56 |
| 2012→2017 | 0.85 (0.32) | 0.50 (0.96); F 64.9; [−1.60, 2.31] | F 0.02; whole line | 0.47 (0.94); F 15.0; [−2.20, 2.56]; p 0.78 |
| 2007→2012 | 0.28 (0.23) | F 0.08; whole line | F 2.6; whole line | F 1.9; unbounded |

**Unweighted**:

| Window | OLS | (a) Bartik | (a)+(b) |
|---|---|---|---|
| 2012→2022 | 0.66 (0.12) | 1.20 (0.53); F 47.4; [0.19, 2.38] | 0.63 (0.59); F 30.5; [0.03, 2.05]; p 0.12 |
| Stacked 2012→17, 2017→22 | 0.47 (0.13) | 1.80 (1.74); F 32.7; [−1.38, 5.95] | 0.38 (1.46); F 22.4; [−1.69, 3.07]; p 0.07 |
| 2007→2017 | 0.62 (0.17) | F 2.2; whole line | F 2.4; unbounded |
| Stacked 2007→12, 2012→17 | 0.47 (0.13) | 2.24 (1.79); F 21.8; [−0.52, 7.65] | 1.05 (1.34); F 9.9; [−1.01, 5.37]; p 0.12 |

[CALCULATION: `derived/estimates.csv`; `verify.py` recomputes the key rows with full dummy matrices
and a direct cluster sandwich, and confirms the stacked AR bounds give statistics of 3.8415]

**Tally of AR sets.** Across the 17 weighted Bartik specifications in windows without the 2022 wave
or the 2007–2012 recession window, no AR set excludes 0, 0.59, 0.84 or 1. Across all 78 Bartik
specifications for the primary outcome, none excludes 0.59 and two exclude 0.84; both are 2012→2022
weighted variants carrying the break. Across all 308 IV sets, 49 exclude 0.59; nearly all involve
the failed immigrant instrument or the 2007–2012 window. [CALCULATION: `estimates_summary.json`,
"Anderson-Rubin tally"]

**Power.** The best standard error in a window without the break is about 0.8–1.0. Telling 0.59
from zero with 80% power at the 5% level needs a standard error of about 0.21, so this design
falls short by a factor of four. [CALCULATION]

## Why the brief's main window can't be read

**The 2022 wave carries a reporting break.** The Census's national aggregates for local current
operations on financial administration read $16.7bn (2012), $18.9bn (2017) and $39.9bn (2022).
[DATA: `12/17/22statetypepu.txt`, level 3] State governments show the same jump, from $28.1bn to
$57.4bn.

In the county build, the 2017→2022 rise of $16.7bn in 2022 dollars sits almost entirely in a few
places:
- NYC: +$9.4bn. Its reported E23 went from $566m to $10.1bn (record flag "R") with no offsetting
  fall in its other items;
- Cook County: +$2.0bn;
- Philadelphia: +$0.9bn;
- Florida counties: +$3.9bn.

[DATA: `2022FinEstDAT_07152026modp.txt`]

The published 2022 Table 1 (`22slsstab1.xlsx`, the file behind `scaling_check.py`) shows financial
administration of $70.7bn for state and local together and $23.7bn for local. The re-released
state-type file sums to $98.6bn (items E, F and G). [SOURCE: both files] The 2022 unit data are
therefore a later vintage that adds about $28bn to financial administration.

The Census disclaimer shipped with the file says unit data "should not be viewed as an accurate time
series for any individual unit". The size of each jump resembles those governments' employer
pension contributions. [INFERENCE, unverified]

The weighted 2012→2022 Bartik estimate is driven by the largest counties:
- dropping the 25 largest gives −0.07 (AR −1.02 to 1.10);
- dropping county areas without a county government gives −0.24;
- trimming the 1% tails gives −0.58;
- the E29+E31 outcome, which leaves out the broken E23, gives −0.12 (AR −1.15 to 1.29).

The unweighted estimate of 1.20 falls to 0.07 once the 1% tails are trimmed. [CALCULATION]

**The immigrant settlement instrument doesn't measure immigrant inflows here.**
- On the foreign-born share, its first stage is 0.10 (SE 0.06) weighted for 2012→2022 and 0.02
  (SE 0.10) for 2007→2017.
- On population, it is zero before 2017: 0.15 (SE 0.15) for 2007→2017 and −0.04 (SE 0.31) for
  2012→2017.
- It is negative in any window that includes 2017→2022: −0.74 (SE 0.14) for 2012→2022.
- It also predicts slower population growth in 2002→2012: −0.55 (SE 0.16).

Its "strength" therefore reflects the persistent relative decline of the 2000 gateway counties, not
immigrant arrivals. Dropping Mexico changes nothing. Nationally, Mexico's foreign-born stock
changes by −0.71m between windows centred on 2012 and 2022, against +6.29m for all origins, as
ladder 136 said. [DATA: `build_audit.json`; CALCULATION]

## The added stacked design without the 2022 wave

This design wasn't in the brief. It was added after the 2022 break was logged (see the history) and
after the 2012→2022 and 2007→2017 estimates had been read. It stacks 2007→2012 and 2012→2017, uses
2007 industry shares for both periods and has state × period effects. Its identification comes from
2012→2017: the 2007→2012 Bartik has no first stage (F 0.08) because the housing-bust industry mix
didn't move population.

Weighted Bartik checks, each against the base of 0.91 (0.93; AR −0.94 to 2.88):

| Check | β (SE) | AR 95% |
|---|---|---|
| Drop 25 largest | 0.76 (1.08) | [−1.25, 3.36] |
| Drop county areas without a county government | 1.49 (0.89) | [−0.14, 3.59] |
| Trim 1% tails | 0.73 (0.88) | [−1.06, 2.58] |
| Control for industry-mix pay-per-worker shock | 0.70 (0.96) | [−1.22, 2.69] |
| Control for actual income growth (bad control) | 0.84 (0.98) | [−1.04, 3.04] |
| Start-of-period shares | 1.30 (1.10) | [−1.03, 3.49] |
| Outcome + judicial (E25) | 1.04 (0.67) | [−0.24, 2.52] |
| Direct expenditure 23+29+31 | 2.14 (0.84) | [0.53, 3.99] |
| Direct expenditure + judicial | 1.90 (0.66) | [0.70, 3.43] |
| E29+E31 only | 0.80 (1.10) | [−1.24, 3.32] |

**Placebo.** Each period's instrument predicts the *preceding* five-year change in spending
negatively: −0.45 (SE 0.29) weighted and −0.43 (SE 0.17) unweighted. The main-period reduced form is
+0.33 (SE 0.34), so mean reversion could account for it. If it does, the response is below 0.91.
The instrument doesn't predict the preceding population change (0.004, SE 0.066). [CALCULATION]

## Instrument checks for the brief's specifications

**Rotemberg weights.** For 2012→2022 weighted, the five largest are:

| NAICS | Industry | α | β_k |
|---|---|---|---|
| 238 | Specialty trade contractors | 0.23 | −1.81 |
| 493 | Warehousing | 0.17 | −0.93 |
| 722 | Restaurants | 0.17 | 0.82 |
| 622 | Hospitals | 0.09 | −0.81 |
| 212 | Mining | 0.08 | −1.11 |

Negative weights sum to −0.37. For 2007→2017 weighted, restaurants (722) lead with α 0.28; negative
weights sum to −1.12.

Dropping the top five industries:
- 2012→2022: −5.79 (4.99), F 7.9;
- 2007→2017: 1.29 (1.14), F 19.3, AR [−1.21, 3.80];
- 2007→2017 with a control for the kept shares: 1.16, F 23.1.

[CALCULATION: `derived/rotemberg.csv`]

**Pre-trend placebos.**
- The 2012→2022 Bartik against the 2002→2012 spending change: 0.38 (SE 0.46) weighted, 0.29 (SE 0.17)
  unweighted.
- The same instrument against the 2002→2012 population change: 0.94 (SE 0.12). The growth it
  predicts is persistent, so part of the first stage is earlier growth.
- The 2007→2017 Bartik against the 1997→2007 spending change: 0.36 (SE 0.40).
- The 2007→2012 Bartik against 1997→2007 spending: −1.62 (SE 0.59), a housing-boom reversal.

[CALCULATION]

**Hansen J.** No two-instrument specification with a usable first stage rejects at 5%: p is 0.61
(2012→2022), 0.36 (stacked late) and 0.56 (stacked early). Two unweighted variants return an empty AR
set (J p 0.05 and 0.01), meaning the two instruments disagree.

**Exclusion threats, reported rather than assumed away.** An industry-mix shock raises incomes as
well as population. Controlling for the industry-mix pay-per-worker shock leaves the estimates where
they were. Controlling for actual income growth is a potentially bad control because income is an
outcome of the same shock; in 2012→2022 it moves the weighted estimate to −0.68. Both are shown.
Reduced forms are in every IV row of `estimates.csv`.

## Cross-section in levels, compared with 0.842

| Level | 2002 | 2007 | 2012 | 2017 | 2022 |
|---|---|---|---|---|---|
| Counties, weighted, state effects (E23+E29+E31) | 0.99 | 0.98 | 0.97 | 0.98 | 1.09 |
| Counties, unweighted, state effects | 0.86 | 0.86 | 0.83 | 0.84 | 0.88 |
| State sums of county areas, local only | 1.00 | 0.99 | 0.96 | 0.96 | 1.05 |
| States, state and local combined, direct 23+25+29+31 | — | — | 0.873 | 0.843 | 0.891 |

[CALCULATION: `derived/cross_section.csv`; state rows from the Census state-type files, SEs about 0.04]

Weighted by population, local administration shows no scale economies across counties or states
(elasticity about 1.0). Unweighted, the many small counties show some (0.83–0.88). The combined
state-and-local elasticity of 0.84–0.89 is stable across census years. The 2022 row on the
re-released data is 0.891, against 0.842 on the published table. Scale economies therefore sit in
state governments, which county data don't observe. Local units are 56% of state-and-local current
operations on these functions ($76.4bn of $135.6bn in 2017). [DATA: `17statetypepu.txt`]

## Steel-man of both views

**Zero response.**
- Budget scoring holds appropriations fixed in the window.
- Legislatures, executive offices, auditors and tax systems exist whatever the marginal resident count.
- Every within-place estimate so far fails to reject zero: the state panel's 0.47 (−0.72 to 1.66), and
  the break-free AR sets here all include zero.
- Within-county OLS changes (0.27–0.85) sit below the county cross-section (about 1.0), which is the
  pattern if marginal residents are absorbed by existing staff.

**Cross-state.**
- The account compares a stationary US with 41m fewer residents; that is a long run in which
  everything adjusts.
- Levels across places are the natural evidence for that comparison, and they are tight: 0.84–0.89
  for state and local in each census year, about 1.0 for local government.
- Five- and ten-year within-place changes are biased toward zero by adjustment lags and budget
  rigidities that don't bind in a stationary comparison.

**Judgment.** [FRAMING-SENSITIVE: stationary versus scoring-window response] This lane was the
within-place causal test that could have favoured zero. It returned nothing precise. The cross-state
range rests on its own evidence, which this lane neither contradicts nor strengthens. Every point
estimate without the break sits near or above the adopted range, and none is significantly below it:
Bartik 0.28–1.49, OLS 0.49–0.85, county levels about 0.98.

## Map to the adopted main case (proposal only; the operator adopts)

`main_case_map.js` rebuilds `scaling_check.py`'s composite with the lane's elasticity b in place of
the state-local 0.842:
- low = (state-local $301.3bn × b + federal tax collection $36.6bn × 0.789) / $475.8bn;
- high = b.

It then evaluates the adopted main case on the explorer engine, as `main_case.js` builds it. The band
moves $48.29bn per unit of response. [CALCULATION: `derived/main_case_map.csv`]

| Elasticity used | Composite low–high | Main case, $bn a year |
|---|---|---|
| Adopted (0.59/0.84) | 0.59–0.84 | 203.2–249.6 |
| General government fixed | 0–0 | 174.7–209.1 |
| Stacked 2007→12, 2012→17 Bartik, point 0.91 | 0.64–0.91 | 205.4–252.9 |
| Same, AR lower end −0.94 | −0.53 to −0.94 | 148.9–163.7 |
| Same, AR upper end 2.88 | 1.89–2.88 | 265.8–348.3 |
| 2007→2017 Bartik, point 0.91 (AR −0.84 to 2.90) | 0.64–0.91 | 205.4–253.0 (envelope 152.0–349.1) |
| Brief main, 2012→2022 (a)+(b), −3.26 (AR −5.09 to 1.25) | −2.00 to −3.26 | 51.8–78.0 (envelope −36.7 to 269.6) |
| Stacked 2007→12, 2012→17 OLS 0.58 (95% 0.24–0.92) | 0.43–0.58 | 195.4–237.1 |
| County cross-section 2017, 0.98 (not causal) | 0.68–0.98 | 207.6–256.3 |

Negative elasticities are mapped unclamped, as the administration lane's rule requires; they have no
economic reading here.

The AR-consistent range around the best estimate spans roughly $149–348bn. So the lane gives no
ground to move the adopted $203.2–249.6bn either way. Using the point estimate would add $2.2–3.3bn.

## Gates

All passed before any new number was computed (`derived/gates.json`, `derived/main_case_gates.json`):
- **`scaling_check.py` composite:** 0.5942 and 0.8424, rounding to 0.59 and 0.84; all nine
  cross-state elasticities match.
- **Administration lane:** its state panel reproduces 0.4708 (CR1 SE 0.606), n=350.
- **Composition lane's county totals:** administration (direct) and judicial reproduce exactly for
  every county: 3,138 counties and $50.845bn in 2012, 3,139 counties and $91.992bn in 2022.
- **Government Finance Database:** current operations on E23+E29+E31 equal the Census unit files
  exactly in 2012 and 2022. In 2017 they differ by 0.11%, a 2023 re-release.
- **`main_case.js`:** reports "all gates passed" under a preload that blocks writes. The files it
  would write equal those on disk byte for byte.
- **Lane evaluator:** reproduces $203.207–249.640bn at 0.59/0.84.

## Data notes and limits

- **Geography.** New York City's five boroughs are one unit, because the city files under New York
  County. Alaska, Connecticut, DC, Kalawao and Broomfield are dropped, which leaves 48 states.
  Shannon/Oglala Lakota and Bedford city are recoded.
- **Business Patterns suppression.** 53% (2007) and 55% (2012) of county 3-digit cells are suppressed;
  the share is 9% in 2017 and 0% in 2022. Suppressed cells are imputed from establishment size
  classes, clipped to the flag's employment range and scaled to the reported parent total.
- **Population.** Estimates are intercensal for 2002, 2007, 2012 and 2017, and vintage 2023 for 2022.
- **Coverage.** State governments' administration, about 44% of these functions, isn't observed at
  county level. The brief's mapping applies the local elasticity to the whole state-local term; that
  is an [INFERENCE] the data don't test.
- **Instrument bias.** This is a politically charged account, and the result here leaves a
  cost-raising adopted parameter in place. The 2022 break was logged before any estimate was run.
  The added stacked design was chosen after seeing other windows, and its point estimate (0.91)
  equals the pre-existing 2007→2017 estimate.

## Reproduce

```bash
cd /Users/alien/Projects/immigration-research
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
L=infra/immigration-fiscal/gg_response_county_iv_2026_09_23
r() { OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 "$@"; }
r $L/fetch.py 2>&1 | sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'
r $L/gfd_stream.py && r $L/gates.py && node $L/main_case_map.js
r $L/build_panel.py && r $L/estimate.py && r $L/verify.py && node $L/main_case_map.js
```

**Rerun check (2026-09-23).** All nine `derived/` files, `_cache/gfd_admin_county.csv` and the Bartik
component caches were deleted, and the block above was run from `fetch.py` (cached) onward. All nine
`derived/` files came back byte-identical (sha256), and `verify.py` passed. No `--with` wheels are
needed. Nothing outside the lane was written; `git status` shows no change in other lanes.

## History

- 2026-09-23, before estimation: wrote the stub, passed the gates and built the panel. Found the
  2022 E23 break in the Census aggregates and the unit files, and logged it here before running
  `estimate.py`.
- 2026-09-23, after estimation: added the stacked 2007→2012 / 2012→2017 design. Found the gap between
  the 2022 published table and the re-released files ($70.7bn against $98.6bn). Ran the rerun check.
