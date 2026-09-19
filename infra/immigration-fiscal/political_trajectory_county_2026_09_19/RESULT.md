# Mexican-origin composition and county political trajectory, 2000-2024

[DATA] county returns, Census API tables, CPS microdata · [SOURCE] MEDSL, tonmcg,
Census API, Roper Center, Pew Research, MSU IPPSR · [INFERENCE] every verdict,
regression and decomposition below · [CALCULATION] every number tagged as such ·
[TRAINING-DATA] only the published national vote and turnout constants used as
validation bands, each marked in place

**Verdict:** growth in a county's Mexican-origin share does not move the county's
presidential vote or its turnout once state-by-year shocks are absorbed. The
two-way fixed-effect estimate is **−0.02 points of Democratic two-party share per
point of Mexican-origin population share, standard error 0.15, 95% CI −0.31 to
+0.27** [CALCULATION: `derived/regressions.csv` S1], and turnout on citizen
voting-age population is **−0.09 ± 0.28** [S1/T1]. A shift-share instrument on the
2000-2024 long difference puts the point estimate on the *Republican* side
(−0.42 ± 0.36 in Democratic points, first-stage F 22.9) without significance
[S4]. Nationally, the Mexican-origin share of voters nearly doubled, 3.34% to
6.04% of all voters from 2004 to 2024 [CPS], and that rise is worth **+0.29
points** of the national Democratic two-party share across twenty years against
**−2.80 points** from the group's own partisanship moving between 2012 and 2024
[`derived/decomposition.csv`]. The California-Texas gap is **not** composition: the
two states' Mexican-origin population shares are within a point of each other in
every election (24.96 vs 24.32 in 2000, 32.25 vs 32.20 in 2024), the average
Democratic gap is +18.4 points, and the split is **+0.2 composition against +18.2
conversion**; in counties below 10% Mexican origin the Democratic two-party share
averages 66.0 in California and 23.1 in Texas [`derived/ca_tx.txt`]. The
"bubbling up" claim survives only in a narrow form: the one accommodating law
measurable here tracks the group's size, while the restrictive-law count tracks
the rest of the electorate's politics.

---

## Arm 1 — county vote panel, 2000-2024

**Panel.** 3,103 counties × 7 presidential elections = 21,721 rows, balanced
[`derived/county_panel.csv`]. Votes: MEDSL's own GitHub mirror for 2000-2016, the
tonmcg mirror for 2020 and 2024. The MIT file on Harvard Dataverse
(doi:10.7910/DVN/VOQCHQ) refuses scripted download with HTTP 400, "You may not
download this file without the required Guestbook response for guestbookID 458",
with and without `gbrecs=true`; that is the source route actually used and it is
recorded in `_cache/SOURCE_USED.txt`. Both sources carry 2016, so the splice error
is measured rather than assumed: over 3,112 matched counties the two-party
Democratic share differs by a median of **0.016 points**, mean 0.123, with 2.0% of
counties above one point [CALCULATION: script 01]. Composition comes from the 2000
and 2010 decennial SF1 (PCT011004) and ACS 5-year releases matched to each election
year at the window midpoint. National reproductions: the panel returns a Democratic
two-party share of 0.5019 / 0.4867 / 0.5359 / 0.5192 / 0.5103 / 0.5219 / 0.4908 for
2000-2024 and citizen turnout of 66.5% in 2020, both inside the published values.

| Spec | What it does | Coefficient (points of Dem two-party share per point of Mexican-origin share) |
|---|---|---|
| S1 | county FE + state×year FE, population weighted, SE clustered by state | **−0.021** (se 0.149, t −0.14) |
| S2 | county FE + national year FE | +0.489 (se 0.144, t +3.40) |
| S3 | long difference 2000→2024, state FE | −0.121 (se 0.261) |
| S4 | shift-share IV on the long difference, first-stage F 22.9 | −0.424 (se 0.365) |
| S5 | S1 without AZ, CA, NM, TX | +0.451 (se 0.352) |
| S6 | S1 on 2016, 2020, 2024 only | +0.597 (se 0.177, t +3.38) |
| S7 | placebo: 2000→2008 vote change on 2008→2024 composition change | −0.222 (se 0.251) |
| S8 | S1 plus the non-Mexican Hispanic share | Mexican +0.202 (se 0.148); non-Mexican Hispanic **+0.711** (se 0.181) |
| S9 | S1 on 2000-2016 only, one vote source | +0.129 (se 0.145) |
| S10 | S1 with the total Hispanic share | +0.445 (se 0.180) |
| T1 | turnout on citizen VAP, 2008-2024, county + state×year FE | −0.088 (se 0.283) |
| T2 | same with national year FE | −0.195 (se 0.217) |

All coefficients: [CALCULATION: `derived/regressions.csv`].

**What the design is using.** Raw cross-county standard deviation of the
Mexican-origin share is 11.31 points; after county and state×year fixed effects the
residual standard deviation is 1.55 points, and the median county gained 1.56
points of Mexican-origin share between 2000 and 2024, the 90th percentile 7.79
points. So S1 is a tight null over a real but modest shock, not a null from an
absent regressor.

**The disconfirmation arms, reported whether or not they help.** S5 (drop the four
border states) and S6 (2016-2024 only) both flip the sign positive, S6
significantly. S6 identifies off 2016→2024 changes in a window where the national
Mexican-origin share barely moved (11.32% to 11.39%), so it leans on small
within-county movements that are partly ACS vintage noise; it is the one arm that
would reverse the headline and it is stated as such. S7, the placebo, is null:
future composition change does not predict past vote change, which is what an
honest identification needs. S9 shows the null is not a splice artifact.

**S1 against S2 is the finding.** The positive association between Mexican-origin
share and the Democratic vote lives *between* states and disappears when each
state's own year shock is removed. S8 sharpens it: conditional on both, the
Democratic association attaches to the **non-Mexican** Hispanic share (+0.71), not
the Mexican one (+0.20, not distinguishable from zero).

**Against ladder 97.** Mayda, Peri and Steingress 2022 report 4.6 Republican points
per point of low-skill immigrant share. The closest analogue here, the shift-share
IV long difference, implies **+0.42 Republican points per point** of Mexican-origin
population share, 95% CI −0.31 to +1.14 — same sign, about a tenth the size, and
not significant. Different regressor (resident Mexican-origin population, not
low-skill immigrant share) and different window, so this bounds rather than
refutes; it does say that the resident-group version of the effect is small.

**Rio Grande Valley, by name** [`derived/rgv_swing.csv`]. Democratic two-party
share, 2020 → 2024: Starr 52.5 → 42.0 (−10.5), Maverick 54.8 → 40.7 (−14.1), Webb
61.8 → 48.9 (−12.9), Hidalgo 58.6 → 48.6 (−10.0), Cameron 56.6 → 47.1 (−9.5),
Zapata 47.3 → 38.7 (−8.6), Willacy 56.0 → 48.3 (−7.7). Vote-weighted across the
twelve South Texas counties listed: **−9.0 points in one cycle**. Across all 72
counties at or above 50% Mexican origin in 2024, the vote-weighted Democratic
two-party share runs 54.7 (2012) → 56.5 (2016) → 52.5 (2020) → **45.4 (2024)**.

## Arm 2 — composition versus conversion

Group shares of actual voters from the CPS November Voting and Registration
Supplement, 2004-2024 (2000 is not on the Census API); the weighted citizen
turnout reproduces the Census Bureau's own published CPS figure to the decimal in
every year (63.8 / 63.6 / 61.8 / 61.4 / 66.8). Group Democratic two-party shares
from the national exit polls as archived by the Roper Center, with Pew validated
voters alongside.

| | 2004 | 2024 |
|---|---|---|
| Mexican-origin share of all voters | 3.34% | 6.04% |
| Mexican-origin share of citizen voting-age population | 4.94% | 8.36% |
| Mexican-origin citizen turnout | 43.2% | 47.2% |
| Non-Hispanic citizen turnout | 65.3% | 67.7% |

[CALCULATION: `derived/cps_voting_national.csv`]. The turnout gap runs 17.3 to 22.1
points, averaging 20.0, and does not close over the window.

Decomposition of the national Democratic two-party share
[`derived/decomposition.csv`], in points:

| Window | Total | Composition | Conversion | Interaction |
|---|---|---|---|---|
| 2004→2024 | +0.49 | **+0.29** | **+0.32** | −0.12 |
| 2012→2024 | −2.71 | +0.52 | **−2.80** | −0.43 |
| 2004→2012 | +3.20 | +0.15 | +2.67 | +0.38 |

Holding the group's partisanship at its 2004 level, the Mexican-origin share rise
alone is worth **+0.17 points** of the national Democratic two-party share against
the non-Hispanic voters it displaces. A sensitivity run making Mexican-origin
voters 5 points more Republican than other Hispanic voters leaves it at +0.28
composition / +0.32 conversion. Twenty years of near-doubling in the group's share
of the electorate is worth a third of a point; four cycles of the group's own
movement is worth almost three points in the other direction.

**A restatement to carry forward.** Pew's Hispanic vote for 2020 is 59% Democratic
/ 38% Republican in its 2021 validated-voter report and **61% / 36%** when restated
in its 2025 report, which says verbatim: "His support among Hispanic voters was 12
points higher than in 2020 (48% in 2024, 36% in 2020). And the share voting for the
Democratic candidate fell from 61% to 51%." [SOURCE:
pewresearch.org/politics/2025/06/26/voting-patterns-in-the-2024-election/]. Both
are carried in `derived/partisanship_series.csv`; the decomposition uses the exit
polls for continuity to 2004.

## Arm 3 — California and Texas

The two states are a natural control: Mexican-origin share of population 24.96
(CA) vs 24.32 (TX) in 2000 and **32.25 vs 32.20 in 2024**, within a point in every
election in between [`derived/ca_tx_series.csv`].

| | CA | TX |
|---|---|---|
| Democratic two-party share, 2024 | 60.4 | 43.1 |
| Hispanic share of voters, 2024 (CPS) | 27.7% | 23.2% |
| Democratic share in counties under 10% Mexican origin, 2000 | 56.6 | 31.3 |
| the same, 2024 | 72.2 | 16.6 |

Splitting the average +18.4-point California-minus-Texas gap over six elections
[`derived/ca_tx_gap_decomposition.csv`]: **composition +0.2, conversion +18.2**.
The backed-out non-Hispanic Democratic two-party share averages 61.1 in California
and 37.6 in Texas. The survey-free cross-check agrees and is larger: in counties
below 10% Mexican origin — where there are no Hispanic voters of consequence in
either state — the Democratic two-party share averages 66.0 in California against
23.1 in Texas, a 42.9-point gap. Those counties still carry 4.7% of California's
and 2.6% of Texas's 2024 votes, so they are thin but real.

The divergence is a white-vote effect, not a composition effect, and it is
*widening*: California's low-Mexican counties moved from 56.6 to 72.2 Democratic
while Texas's moved from 31.3 to 16.6, over a period when the two states'
Mexican-origin shares converged to within half a point.

## Arm 4 — laws that bubble up

Correlates of State Policy Project v2.2 (MSU IPPSR). Predictors built inside the
lane: the state's Mexican-origin population share, and the Democratic two-party
share in that state's counties below 10% Mexican origin in 2008 as a survey-free
stand-in for the rest of the electorate. n is 48 states, so these are ordering
tests, not identified effects.

**In-state tuition for unauthorized immigrants** (binary, 2001-2014; 19 states ever
coded 1). Adopters' mean Mexican-origin share 8.2% against non-adopters' 3.8%;
adopters' mean non-Hispanic-county Democratic share 51.1 against 51.0. Logit:
Mexican-origin share **+0.101, z +1.86**; non-Hispanic-county Democratic share
+0.015, z +0.57, with both in. The 2×2 at the medians shows both dimensions
carrying signal: adoption rate 0.00 (low share, Republican-leaning rest) / 0.31
(low share, Democratic-leaning) / 0.46 (high share, Republican-leaning) / **0.73**
(high share, Democratic-leaning), cells of 11 to 13 states.

**Net restrictive minus accommodating immigration laws, 2005-2012.** Spearman with
the Mexican-origin share **+0.056**; with the non-Hispanic-county Democratic share
**−0.615**. The count variables are missing for many state-years inside the window
(Texas is absent in every even year), so this is the weakest arm and is reported as
an ordering only.

Read together: the accommodating law that directly benefits the group tracks the
group's size; the restrictive-law count tracks how the rest of the state votes.
That is a narrow, conditional version of "bubbling up", not a general one.

## Arm 5 — apportionment

Not redone. Ladder 147 has it: counting the Mexican-origin population where it
lives moves 24 of 435 House seats in the 2020 apportionment (CA −12, TX −8), with
no arm flipping the 2020 or 2024 presidential outcome.

## What was skipped and why

- **The MIT file itself.** Harvard Dataverse requires a guestbook response
  (HTTP 400, guestbookID 458). Filling it needs a name and email submitted to an
  external service, which this lane does not do; the MEDSL GitHub mirror is the
  same construction for 2000-2016 and the splice is measured.
- **Driver's licences for the unauthorized, E-Verify mandates, sanctuary and
  anti-sanctuary statutes, 287(g).** Not present in Correlates of State Policy
  v2.2. They are not filled from memory. The lane covers in-state tuition and the
  NCSL-derived law counts instead, and the gap is named.
- **Gubernatorial margins and post-2011 legislative control.** Correlates ends its
  party-control variables in 2011; no substitute was fetched inside this lane.
- **2000 CPS November supplement.** Not on the Census API (HTTP 400 for every
  variable set tried). The CPS series starts in 2004.
- **Alaska and Connecticut.** Dropped, with the reasons in `README.md`.
- **2024 composition** uses the ACS 2019-2023 release, midpoint 2021. A real lag.

## Limits

Ecological regressions on counties do not identify individual votes; nothing here
says how a Mexican-origin citizen voted. The partisanship series is survey-based,
and the exit-poll Hispanic electorate share (13% in 2020) exceeds the CPS
self-reported share (10.6%), so the two inputs to the decomposition are not on one
frame; the decomposition uses CPS for shares and exit polls for partisanship and
says so. State laws are few and endogenous to the same politics they are regressed
on. 2024 may be a level shift or a cycle: one election cannot tell. The brief's
"vortex" is a growth-rate claim over sixty years, and a 24-year panel bounds the
level effect only.

## Draft memo section the parent can lift

> **Composition did not move the counties.** Over seven presidential elections and
> 3,103 counties, growth in a county's Mexican-origin population share has no
> detectable effect on its Democratic two-party share once each state's own year
> shock is absorbed: −0.02 points per point, standard error 0.15, with the 95%
> interval ruling out anything larger than a third of a point in either direction.
> Turnout on citizen voting-age population is the same null, −0.09 ± 0.28. A
> shift-share instrument built on 2000 settlement puts the point estimate on the
> Republican side. The positive association that appears with national year effects
> instead of state-by-year effects is a between-state pattern, and conditional on
> both Hispanic components it attaches to the non-Mexican Hispanic share, not the
> Mexican one.
>
> **The group's own movement dwarfs its growth.** The Mexican-origin share of
> voters nearly doubled between 2004 and 2024, from 3.34% to 6.04%, while the
> group's citizen turnout stayed roughly twenty points below the non-Hispanic rate
> throughout. That doubling is worth +0.29 points of the national Democratic
> two-party share over twenty years. Between 2012 and 2024 the Hispanic vote's own
> swing is worth −2.80 points, nearly six times as much in the other direction. In
> the 72 counties at least half Mexican-origin, the Democratic two-party share fell
> from 54.7 in 2012 to 45.4 in 2024, and the South Texas border counties moved 9.0
> points right in the single cycle from 2020 to 2024.
>
> **California and Texas settle the framing question.** Their Mexican-origin
> population shares are within half a point of each other in 2024, 32.25 against
> 32.20, and were within a point in 2000. Their Democratic two-party shares differ
> by 17 points. Decomposing the average 18.4-point gap gives +0.2 to the difference
> in Hispanic electorate share and +18.2 to everyone else voting differently. The
> cleanest version uses no survey at all: in counties below 10% Mexican origin,
> California votes 66.0 Democratic and Texas 23.1, and that gap has widened while
> the two states' compositions converged. Whatever separates California from Texas,
> it is not how many Mexican-origin residents each has.

## Verification

All eight scripts re-run end to end over the existing `_cache/` (no new network
fetches), and `diff -rq` against a copy of `derived/` taken before the re-run
reports **no differences across all 15 files**. Per-file sha256 is recorded in
`logs/rerun_*.log` alongside each script's output. Content checks that gate the
pipeline and passed on both runs: MEDSL reproduces the published national
two-party Democratic share for 2000-2016 and tonmcg for 2020 and 2024, each
within 0.05 points; the Census API Mexican-origin national totals land at 20.7M
(2000), 31.8M (2010) and 37.4M (ACS 2019-2023); and the CPS weighted citizen
turnout reproduces the Census Bureau's own published CPS figure to the decimal in
every year from 2004 to 2020.
