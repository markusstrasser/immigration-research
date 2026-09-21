# Does Mexican-origin composition move political outcomes? A county panel with the California–Texas contrast

**Verdict:** Growth in a county's Mexican-origin population share does not move its presidential vote or its turnout once each state's own year shock is absorbed: −0.02 points of Democratic two-party share per point of share (SE 0.15, 95% CI −0.31 to +0.27) over 3,103 counties and seven elections, 2000–2024, and −0.09 ± 0.28 on citizen-VAP turnout. A shift-share instrument on 2000 settlement puts the point estimate on the Republican side (−0.42 ± 0.36, first-stage F 22.9), the same sign as Mayda, Peri and Steingress but a tenth the size and not significant. The positive association that appears with national year effects is a between-state pattern, and conditional on both Hispanic components it attaches to the non-Mexican Hispanic share (+0.71) rather than the Mexican one (+0.20, not distinguishable from zero). Nationally the Mexican-origin share of voters nearly doubled 2004–2024 (3.34% → 6.04%) with a citizen turnout gap of about 20 points that does not close; that doubling is worth +0.29 points of the national Democratic two-party share over twenty years, while the group's own 2012–2024 swing is worth −2.80 points. Counties at least half Mexican-origin went 54.7 → 45.4 Democratic between 2012 and 2024, the South Texas border counties −9.0 points in one cycle. California and Texas have Mexican-origin shares within half a point (32.25 vs 32.20 in 2024) and an 18.4-point average Democratic gap that decomposes +0.2 composition, +18.2 conversion; in counties under 10% Mexican origin the two states vote 66.0 and 23.1 Democratic, a gap that widened while their compositions converged. "Bubbling up" survives only narrowly: in-state tuition for the unauthorized tracks the group's size (logit z +1.86) not the rest of the electorate (z +0.57), while the net restrictive-law count tracks the rest of the electorate (Spearman −0.615) and not the group (+0.056). The one arm that reverses the headline is the 2016–2024 window alone (+0.60, t 3.38), which identifies off small within-county movements that are partly ACS vintage noise; dropping the four border states also flips the sign, insignificantly; the placebo of future composition on past vote change is null. [SOURCE: `infra/immigration-fiscal/political_trajectory_county_2026_09_19/RESULT.md`, `derived/`] [FRAMING-SENSITIVE: ecological regressions do not identify individual votes; 2024 may be a level shift or a cycle; a 24-year panel bounds the level effect and says nothing about a sixty-year growth-rate claim]

Date: 2026-09-19. Lane: `infra/immigration-fiscal/political_trajectory_county_2026_09_19/`. Supersedes the measured-input side of ladder 97/102: the resident-group version of the political externality is small in level and its sign is not established.

## 1. County panel specifications (Democratic two-party share, points per point of Mexican-origin share)

| Spec | Design | Coefficient (SE) |
|---|---|---|
| S1 | county FE + state×year FE, population-weighted, clustered by state | −0.021 (0.149) |
| S2 | county FE + national year FE | +0.489 (0.144) |
| S3 | long difference 2000→2024, state FE | −0.121 (0.261) |
| S4 | shift-share IV on the long difference, first-stage F 22.9 | −0.424 (0.365) |
| S5 | S1 without AZ, CA, NM, TX | +0.451 (0.352) |
| S6 | S1 on 2016–2024 only | +0.597 (0.177) |
| S7 | placebo: 2000→2008 vote change on 2008→2024 composition change | −0.222 (0.251) |
| S8 | S1 with non-Mexican Hispanic share | Mexican +0.202 (0.148); non-Mexican Hispanic +0.711 (0.181) |
| S9 | S1 on 2000–2016, one vote source | +0.129 (0.145) |
| S10 | S1 with the total Hispanic share in place of the Mexican-origin share (row added 2026-09-21) | +0.445 (0.180) |
| T1 | turnout on citizen VAP, 2008–2024, county + state×year FE | −0.088 (0.283) |

Residual SD of the regressor after both fixed effects is 1.55 points (raw 11.31); median county gain 2000–2024 is 1.56 points, 90th percentile 7.79. Votes: MEDSL GitHub mirror 2000–2016, tonmcg 2020–2024 (Dataverse refuses scripted download); splice measured on the 2016 overlap at a median 0.016 points. [SOURCE: `derived/regressions.csv`, `county_panel.csv`] [CALCULATION]

## 2. Composition versus conversion, national Democratic two-party share (points)

| Window | Total | Composition | Conversion | Interaction |
|---|---|---|---|---|
| 2004→2024 | +0.49 | +0.29 | +0.32 | −0.12 |
| 2012→2024 | −2.71 | +0.52 | −2.80 | −0.43 |

Shares of voters from the CPS November supplements 2004–2024 (weighted citizen turnout reproduces the Bureau's published figures to the decimal); partisanship from Roper-archived exit polls with Pew validated voters alongside (Pew restated its 2020 Hispanic figure from 59/38 to 61/36 in 2025). [SOURCE: `derived/cps_voting_national.csv`, `decomposition.csv`, `partisanship_series.csv`]

## 3. California and Texas

| | CA | TX |
|---|---|---|
| Mexican-origin share of population, 2024 | 32.25% | 32.20% |
| Democratic two-party share, 2024 | 60.4 | 43.1 |
| Hispanic share of voters, 2024 (CPS) | 27.7% | 23.2% |
| Democratic share in counties under 10% Mexican origin, 2000 → 2024 | 56.6 → 72.2 | 31.3 → 16.6 |

Backed-out non-Hispanic Democratic two-party share averages 61.1 in California and 37.6 in Texas. [SOURCE: `derived/ca_tx_series.csv`, `ca_tx_gap_decomposition.csv`, `ca_tx.txt`]

## 4. Laws

Correlates of State Policy v2.2, n = 48 states, ordering tests only. In-state tuition (19 adopters, 2001–2014): adoption 0.00 / 0.31 / 0.46 / 0.73 across low-share-Republican, low-share-Democratic, high-share-Republican, high-share-Democratic cells. Driver's licences, E-Verify, sanctuary statutes and 287(g) are absent from the file and were not filled from memory. [SOURCE: `derived/state_law_table.csv`, `state_laws.txt`]

## 5. Limits

Ecological; survey-based partisanship on a different frame from the CPS shares; state laws few and endogenous; 2024 composition uses the 2019–2023 ACS (midpoint 2021); 2000 CPS not on the API; Alaska and Connecticut dropped for geography. Ladder 147 holds the apportionment effect (24 seats) and is not redone. No policy advice.

Added 2026-09-21. State-by-year effects absorb every channel that works at the state level, including statewide realignment and any reaction of low-share counties to statewide change, so S1 measures the within-state county gradient only (residual SD of the regressor 1.55 points against 11.31 raw). The largest movement in the data sits in that absorbed part: counties under 10% Mexican origin went 56.6 → 72.2 Democratic in California and 31.3 → 16.6 in Texas (§3), and this design cannot say whether statewide composition caused either. S2 keeps that variation and cannot separate it from other state trends. Within the S1 design the total Hispanic share does load (S10: +0.44, t 2.5), through its non-Mexican component (S8). The verdict is therefore a statement about the Mexican-origin share's county gradient over 2000–2024, with one reversing window (S6); it is not a finding that composition has no political effect. [SOURCE: `derived/regressions.csv`] [INFERENCE for the last sentence]

## Sources

MEDSL county returns (GitHub mirror), tonmcg 2020/2024; Census API dec/sf1 2000 and 2010 (PCT011004), ACS 5-year 2009–2023 (B03001, B03002, B05003, B05003I, B19013); CPS November Voting and Registration Supplement 2004–2024 via Census API; Roper Center exit polls; Pew validated-voter reports 2021 and 2025; MSU IPPSR Correlates of State Policy v2.2; Mayda, Peri and Steingress 2022; ladder 87, 97, 102, 104, 147.

## Revisions

- 2026-09-21. Added specification S10, which the lane had computed and the memo omitted, and a limits paragraph on what state-by-year effects absorb. A second agent's summary had read S1 as "share growth does not move votes"; the estimates are unchanged and the verdict is now scoped to the county gradient. Ladder 160.
