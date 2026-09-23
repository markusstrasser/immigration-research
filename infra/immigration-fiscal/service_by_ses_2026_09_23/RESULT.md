claude-opus-5-5[1m]

**Verdict:** Per head, US-born men of Asian Indian ancestry have served on active duty at about
one-sixth of the rate of US-born non-Hispanic white men. Holding age, schooling, place or
neighbourhood income fixed leaves them at about one-fifth; only reweightings that rest on a few
cells lift the ratio to a third or more. US-born Mexican-origin men have served at about
four-fifths of the white rate, and at about nine-tenths once age is held fixed. Adjusting further
for schooling and geography puts them anywhere from 0.74 to 1.46 of the white rate, depending on
whose mix of schooling and places is used, because their gap is concentrated among men born in
California and Texas. US-born Mexican-origin women serve at the white rate or above, and so do
young US-born Mexican-origin men now on active duty. The foreign-born of both origins serve far
less, and many of them cannot legally enlist.

Ever on active duty, men aged 18–49, ACS 2022–2024 pooled, with replicate standard errors
[DATA: `derived/military_rates.csv`]:

- US-born non-Hispanic white: **7.02%** (SE 0.03).
- US-born, Asian Indian ancestry: **1.11%** (0.13), ratio 0.16 (0.02). India-born: 0.78% (0.07),
  ratio 0.11 (0.01); naturalized India-born 1.37% (0.17), 0.19.
- US-born, Mexican Hispanic origin: **5.52%** (0.09), ratio 0.79 (0.01). Mexico-born: 1.36%
  (0.05), ratio 0.19 (0.01); naturalized Mexico-born 3.69% (0.17), 0.53.
- Women 18–49: white 1.29% (0.01); US-born Mexican origin 1.25% (0.04), ratio 0.97 (0.03);
  US-born Asian Indian ancestry 0.27% (0.08), ratio 0.21 (0.06).
- Now on active duty, men 18–24: white 2.39% (0.04); US-born Mexican origin 2.34% (0.07), ratio
  0.98 (0.03); US-born Asian Indian ancestry 0.52% (0.14), ratio 0.22 (0.06).

**Indian gap, men 18–49.** It survives every adjustment that uses the whole group: 0.18 (0.02)
at the same ages, 0.21 (0.02) at the same age and schooling, 0.21 (0.02) at the same age,
schooling and birth state, 0.23 (0.03) with state and metro of residence instead, and 0.21 (0.02)
against neighbourhood income (0.24 with age held too). Graduates show it as well: 1.0% (0.1) of
Indian-ancestry men aged 25–49 with a degree have served, against 6.9% of white graduates. Only
reweighting the group to the white mix of schooling or places lifts the ratio, to 0.34–0.64
(0.81, SE 0.15, at ages 25–49), and those estimates rest on a few cells: ten cells carry 61–88%
of the reweighted numerator.

**Mexican gap, men 18–49.** At the same ages the ratio is 0.88 (0.01). Holding own schooling
too gives 0.89 (0.01) at the group's own mix and 0.98 (0.02) at the white mix; birth state, 0.79
(0.01) at the own mix and 1.14 (0.04) raked to the white mix; residence, 0.75 (0.01) and 1.46
(0.04); neighbourhood income, 0.74 (0.01), or 0.83 (0.01) with age held too. The gap sits among
men born in California (0.71 of California-born whites at the same ages) and Texas (0.78), who
make up two-thirds of the group. The 18% born in the Midwest, the South Atlantic, the Middle
Atlantic and the South Central states outside Texas have served at 0.96–1.37 of whites born
there, and the raked estimates lean on them.

**Cause or outcome.** Own schooling and place of residence partly follow service, so adjustments
(a) and (b) cannot separate cause from outcome. The GI Bill pays for college, and veterans live
where they were stationed or moved afterwards: US-born men living outside their birth state have
served at 2.6 (whites) to 3.4 (Mexican origin) times the rate of those who stayed [DATA:
`derived/military_movers.csv`]. Birth state removes the residence problem for the US-born, but a
child born to parents stationed away from home still carries the family's service into the birth
state. (c) measures neighbourhood income before service on the DoD side but the group's current
tracts on ours, and it is a neighbourhood average, not family income or wealth. No wealth measure
exists in the ACS or the CPS supplement.

**"Or the like."** Per 1,000 employed people aged 18–64, police, sheriff, detective, corrections,
bailiff, fire and EMS jobs: white men 26.1 (0.2); US-born Mexican-origin men 24.3 (0.5), ratio
0.93 (0.02), and at parity for police alone (1.01); US-born Mexican-origin women 1.23 (0.05) of
white women; US-born Asian Indian-ancestry men 6.8 (1.8), 0.26 (0.07); India-born men 2.5 (0.3),
0.10 (0.01) [DATA: `derived/protective_service.csv`]. In the CPS civic supplements of 2021 and
2023, 30.7% of US-born non-Hispanic whites volunteered through an organisation and 57.2% gave more
than $25 to charity; the India-born 25.6% and 53.0%; the Mexico-born 10.9% and 29.4%; second
generation Mexican 15.1% and 28.0%; third-plus Mexican 19.7% and 38.2%. At equal age, sex,
education and family income the Mexican gaps shrink by 40–60%, to −6 to −12 points, while the
India-born gaps widen to −18 points for volunteering and −16 for giving [DATA:
`derived/cps_civic_rates.csv`, `derived/cps_civic_gaps.csv`].

[FRAMING-SENSITIVE] Service is one costly behaviour, not a measure of patriotism or attachment.
Legal eligibility, the age structure of each group, and where each group lives shape these rates,
and the tables below separate what they can.

# Military and public service by Mexican and Indian origin, per capita and at equal SES

Question (operator, 2026-09-23): "Also check how many of indians and mexican per capita serve in
militrary or the like ... also adjusted for SES/wealth". Brief: [`BRIEF.md`](BRIEF.md). This lane
extends ladder 170 ([`civic_service_by_ancestry_2026_09_21`](../civic_service_by_ancestry_2026_09_21/RESULT.md):
ACS 2024, US-born men by first ancestry, binomial SEs) to three pooled years, women, the
foreign-born, the three `MIL` answers, replicate SEs and SES adjustments, and extends ladder 152
(CPS giving and volunteering) to Mexican origin by generation.

## Data and definitions

- **ACS person PUMS 2022, 2023 and 2024 (one-year), pooled**: 8,407,036 person records aged 17
  and over, read from the local zips whose SHA-256 are in `derived/acs_inputs.json` [DATA]. Person
  weights are summed across the three years, so a pooled rate is a three-year average and
  "adults per year" is the weight sum divided by three.
- **Standard errors**: 80 successive-difference replicates. Replicate *r* of the pooled estimate
  uses the sum over years of `PWGTPr`; SE = √(4/80 · Σ(θᵣ − θ)²). Every adjusted ratio is
  recomputed on each replicate, including the raking and the standardisations.
- **Universe**: persons 18 and over, **including group quarters** (`RELSHIPP` 37–38), so service
  members in barracks count. A household-only variant is in `derived/military_rates.csv`
  (`universe = household`). People living abroad, including troops stationed overseas, are
  outside the ACS frame [TRAINING-DATA].
- **Outcomes**: `MIL` 1–2 ever on active duty; `MIL` 1 now on active duty; `MIL` 3 reserve or
  Guard training only (never on active duty) [SOURCE: `_cache/PUMS_Data_Dictionary_2023.csv`].
- **Groups** (US-born = `NATIVITY` 1, which includes births in Puerto Rico, the island areas and
  abroad to US parents):

| Group | Definition |
|---|---|
| US-born, Mexican Hispanic origin | `HISP` 2 |
| US-born, Mexican ancestry | first ancestry `ANC1P` 210 Mexican, 211 Mexican American, 212 Mexicano, 213 Chicano, 215 Mexican American Indian, 218 Mexican State, 219 Mexican Indian |
| Mexico-born, all / naturalized / arrived before 18 | `POBP` 303; `CIT` 4; age at entry from `YOEP` under 18 |
| US-born, Asian Indian ancestry | `ANC1P` 615 |
| US-born, Asian Indian race | `RAC2P` 38 (2022) or 4015 (2023–2024), Asian Indian alone |
| India-born, all / naturalized / arrived before 18 | `POBP` 210; `CIT` 4; `YOEP` |
| US-born non-Hispanic white (reference) | `HISP` 1 and `RAC1P` 1 |
| All US-born | `NATIVITY` 1 |

- **Protective service**: employed civilians (`ESR` 1–2) aged 18–64 by `OCCP`. "Public safety" =
  police and detective supervisors 3710, detectives 3820, police and sheriff's patrol officers
  3870, correctional supervisors 3700, bailiffs 3801, correctional officers and jailers 3802,
  fire supervisors 3720, firefighters 3740, fire inspectors 3750, EMTs 3401, paramedics 3402.
  Security guards (3930) and all protective service (3700–3960) are shown separately.
- **Gates** (all pass): PUMS totals of civilians 18+, civilian veterans 18+ and armed forces
  against published ACS tables B21001 and B23025 for each year, within 0.6% [DATA:
  `derived/gate_published_totals.txt`]; ladder 170's single-year rates reproduced exactly from
  the 2024 file, Mexican (`ANC1P` 210) 5.73% against 5.7% and Asian Indian 1.05% against 1.05%
  [DATA: `derived/reconcile_ladder170.txt`]; DoD tract-income quintile cut-points rebuilt within
  0.7% (below); CPS national volunteering and giving rates equal AmeriCorps' published figures
  to the published decimal, and the 2023 unweighted tallies equal Attachment 13 of the CPS
  documentation [DATA: `derived/gate_cps_published.txt`].
- **Run-to-run check**: two full runs of `service.py` and `birthplace.py` wrote byte-identical
  CSVs; the final run, which added the age and age × education specifications, reproduced every
  earlier row exactly. [Parent rerun, 2026-09-23: 15 of 16 derived files byte-identical.
  `military_birthstate.csv` was regenerated, because the stored copy predated the final
  `birthplace.py`. Two parent runs agree, and `summarize.py --fill` reproduces all 32 printed
  tables unchanged. The DoD Table B-41 counts and cut-points in `neighborhood.py` match the FY23
  PDF (p. 245) and the FY22 extract.]

## 1. Per capita

<!-- part: headline -->
**Per capita: % of each group (SE) · ratio to US-born non-Hispanic whites.** "ever" = ever on active duty (`MIL` 1–2); "now" = on active duty now (`MIL` 1)

| Group | ever, men 18–49 | ever, women 18–49 | ever, men 25–34 | ever, men 18+ born 1956+ | now, men 18–24 | now, women 18–24 | reserve/Guard only, men 18–49 |
|---|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 5.52 (0.09) · 0.79 | 1.25 (0.04) · 0.97 | 5.47 (0.12) · 0.83 | 6.70 (0.07) · 0.72 | 2.34 (0.07) · 0.98 | 0.60 (0.04) · 1.43 | 1.01 (0.03) · 0.83 |
| US-born, Mexican ancestry | 5.32 (0.10) · 0.76 | 1.15 (0.05) · 0.89 | 5.09 (0.13) · 0.77 | 6.45 (0.09) · 0.69 | 2.57 (0.09) · 1.08 | 0.66 (0.06) · 1.58 | 0.98 (0.04) · 0.81 |
| Mexico-born, all | 1.36 (0.05) · 0.19 | 0.39 (0.03) · 0.30 | 1.32 (0.10) · 0.20 | 1.56 (0.04) · 0.17 | 0.45 (0.09) · 0.19 | 0.29 (0.10) · 0.70 | 0.32 (0.03) · 0.26 |
| Mexico-born, naturalized | 3.69 (0.17) · 0.53 | 1.00 (0.11) · 0.78 | 3.95 (0.41) · 0.60 | 3.24 (0.11) · 0.35 | 2.03 (0.52) · 0.85 | 1.22 (0.58) · 2.92 | 0.79 (0.08) · 0.65 |
| Mexico-born, arrived before 18 | 2.02 (0.09) · 0.29 | 0.56 (0.05) · 0.44 | 1.75 (0.15) · 0.27 | 2.42 (0.09) · 0.26 | 0.62 (0.13) · 0.26 | 0.36 (0.13) · 0.85 | 0.47 (0.04) · 0.39 |
| US-born, Asian Indian ancestry | 1.11 (0.13) · 0.16 | 0.27 (0.08) · 0.21 | 1.07 (0.26) · 0.16 | 1.18 (0.13) · 0.13 | 0.52 (0.14) · 0.22 | 0.05 (0.10) · 0.11 | 0.37 (0.09) · 0.30 |
| US-born, Asian Indian race | 1.71 (0.18) · 0.24 | 0.48 (0.10) · 0.38 | 1.67 (0.32) · 0.25 | 1.94 (0.18) · 0.21 | 0.59 (0.13) · 0.25 | 0.16 (0.11) · 0.38 | 0.31 (0.07) · 0.26 |
| India-born, all | 0.78 (0.07) · 0.11 | 0.24 (0.04) · 0.19 | 0.68 (0.13) · 0.10 | 0.91 (0.06) · 0.10 | 0.38 (0.16) · 0.16 | 0.00 (0.00) · 0.00 | 0.23 (0.04) · 0.19 |
| India-born, naturalized | 1.37 (0.17) · 0.19 | 0.37 (0.08) · 0.29 | 1.28 (0.29) · 0.19 | 1.32 (0.11) · 0.14 | 0.78 (0.49) · 0.32 | 0.00 (0.00) · 0.00 | 0.67 (0.12) · 0.55 |
| India-born, arrived before 18 | 1.97 (0.26) · 0.28 | 0.45 (0.14) · 0.35 | 1.58 (0.44) · 0.24 | 2.42 (0.27) · 0.26 | 0.68 (0.27) · 0.29 | 0.00 (0.00) · 0.00 | 0.66 (0.17) · 0.54 |
| US-born non-Hispanic white | 7.02 (0.03) · 1.00 | 1.29 (0.01) · 1.00 | 6.60 (0.05) · 1.00 | 9.37 (0.03) · 1.00 | 2.39 (0.04) · 1.00 | 0.42 (0.02) · 1.00 | 1.22 (0.02) · 1.00 |
| All US-born | 6.74 (0.03) · 0.96 | 1.46 (0.01) · 1.14 | 6.34 (0.05) · 0.96 | 9.19 (0.02) · 0.98 | 2.33 (0.02) · 0.97 | 0.52 (0.02) · 1.23 | 1.19 (0.01) · 0.98 |
<!-- /part -->

Ratios to the white rate, raw, across the five age bands [DATA: `derived/military_rates.csv`]:

- **Indian origin.** US-born men of Asian Indian ancestry have served at 0.13–0.18 of the white
  rate in every band, women at 0.19–0.30; the race-based group is a little higher (men
  0.21–0.28). India-born men: 0.10–0.11 at ages 25 and over and 0.22 at 18–24; naturalized
  0.14–0.30; arrived before 18, 0.24–0.29. Reserve or Guard training only, men 18–49: 0.30
  (US-born, ancestry), 0.19 (India-born), 0.55 (naturalized).
- **Mexican origin.** US-born Mexican-origin men: 0.69–0.83 in the bands that include ages 25 and
  over, 0.94–1.01 at 18–24; women 0.78–1.08, and 1.36–1.39 at 18–24. Now on active duty at
  18–24: men 0.98 (Hispanic origin) and 1.08 (ancestry), women 1.43 and 1.58. Mexico-born men:
  0.17–0.22; naturalized 0.35–0.78; arrived before 18, 0.26–0.29. Reserve or Guard only, US-born
  men 18–49: 0.81–0.83.
- **Group quarters.** Barracks are in the universe. Without them the US-born Mexican-origin ratio
  for men 18–49 falls from 0.79 to 0.73, because more of its young service members live in
  barracks (62% of Mexican-origin men aged 18–24 on active duty, against 51% of whites).

## 2. At equal SES

### What each adjustment can and cannot show

Every adjusted figure is a ratio of the group's rate to a white rate. A factor can be held fixed in
two ways, and they answer different questions, so both are reported:

- **Own mix** (indirect standardisation): the white rate among whites who resemble the group
  (same age, schooling, state), and the group's rate over it. It uses the whole group sample and
  is precise, but its answer belongs to the group's own ages, schooling and places.
- **White mix** (direct standardisation; raking when several margins are matched at once): the
  group reweighted to look like whites. It extrapolates from the group members who resemble
  whites, and when those are few its answer rests on a handful of cells (see the raking
  diagnostics among the detailed tables).

The two differ whenever the group-to-white ratio varies across cells, and for both groups it does.

- **Same ages** (not an SES adjustment): "ever served" accumulates with age, and the US-born
  origin groups are younger than whites inside each band. Age cannot be a result of service, so
  this adjustment is clean.
- **(a) Own education** (less than high school, high school, some college, bachelor's or more),
  within age cells; the education-only version is in the CSV. **(a) cannot separate cause from
  outcome.** Almost no recruit lacks a high-school credential (183 of 128,867 new enlisted
  recruits in FY23, 0.14%, against 13% of civilians aged 18–24 [SOURCE: PopRep FY23 Table B-6,
  `_cache/poprep_fy23_appendix_b.pdf`]), so low schooling is partly a cause of not serving.
  GI Bill benefits raise veterans' schooling, so some college and degrees are partly results of
  serving.
- **(b) Geography**: age × education × state, metro size (four classes) and census division.
  **At residence, (b) cannot separate cause from outcome**: veterans live near the bases they
  served at or moved for work afterwards. With state of birth in place of residence (US-born
  only), the residence channel is gone, but a child born where a parent was stationed still
  carries the family's service into the birth state. For people now on active duty the military
  assigns the residence, so (b) says nothing about current enlistment.
- **(c) Neighbourhood income**: DoD enlisted accessions by the income quintile of the recruit's
  home tract, per 15–17-year-old living in each quintile, applied to each group's distribution
  across the same quintiles. It gives the ratio a group would show if only home-tract income
  mattered, and the group's rate is compared with the white rate scaled by that ratio. It is the
  closest thing to a pre-service SES measure available, but only on the DoD side: the group's
  tracts are where its members live now.

<!-- part: adjust_men_18_49 -->
**Ever on active duty, men 18–49: ratio to US-born non-Hispanic whites (SE) under each adjustment.** "own mix" = indirect standardisation (white rates in the group's own cells); "white mix" and "raked" = the group reweighted to the white distribution. (b) uses age × education × state (and metro size at residence)

| Group | raw | same ages | (a) age × educ, own mix | (a) age × educ, white mix | (b) birth state, own mix | (b) birth state, raked | (b) residence, own mix | (b) residence, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.79 (0.01) | 0.88 (0.01) | 0.89 (0.01) | 0.98 (0.02) | 0.79 (0.01) | 1.14 (0.04) | 0.75 (0.01) | 1.46 (0.04) | 0.74 (0.01) | 0.83 (0.01) |
| US-born, Mexican ancestry | 0.76 (0.01) | 0.86 (0.02) | 0.85 (0.02) | 0.95 (0.02) | 0.75 (0.02) | 1.14 (0.05) | 0.72 (0.01) | 1.52 (0.05) | 0.71 (0.01) | 0.80 (0.02) |
| Mexico-born, all | 0.19 (0.01) | 0.17 (0.01) | 0.26 (0.01) | 0.32 (0.01) | — | — | 0.24 (0.01) | 0.38 (0.04) | 0.18 (0.01) | 0.16 (0.01) |
| Mexico-born, naturalized | 0.53 (0.02) | 0.46 (0.02) | 0.55 (0.03) | 0.64 (0.03) | — | — | 0.51 (0.02) | 0.88 (0.09) | 0.48 (0.02) | 0.41 (0.02) |
| US-born, Asian Indian ancestry | 0.16 (0.02) | 0.18 (0.02) | 0.21 (0.02) | 0.35 (0.11) | 0.21 (0.02) | 0.38 (0.11) | 0.23 (0.03) | 0.64 (0.13) | 0.21 (0.02) | 0.24 (0.03) |
| US-born, Asian Indian race | 0.24 (0.02) | 0.28 (0.03) | 0.32 (0.03) | 0.39 (0.07) | 0.33 (0.03) | 0.37 (0.07) | 0.36 (0.04) | 0.57 (0.11) | 0.32 (0.03) | 0.37 (0.04) |
| India-born, all | 0.11 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.21 (0.03) | — | — | 0.12 (0.01) | 0.34 (0.07) | 0.15 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 0.19 (0.02) | 0.17 (0.02) | 0.18 (0.02) | 0.25 (0.05) | — | — | 0.20 (0.02) | 0.58 (0.10) | 0.26 (0.03) | 0.23 (0.03) |
<!-- /part -->

<!-- part: adjust_men_25_49 -->
**Ever on active duty, men 25–49: ratio to US-born non-Hispanic whites (SE) under each adjustment.** "own mix" = indirect standardisation (white rates in the group's own cells); "white mix" and "raked" = the group reweighted to the white distribution. (b) uses age × education × state (and metro size at residence)

| Group | raw | same ages | (a) age × educ, own mix | (a) age × educ, white mix | (b) birth state, own mix | (b) birth state, raked | (b) residence, own mix | (b) residence, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.83 (0.01) | 0.86 (0.01) | 0.88 (0.01) | 0.99 (0.02) | 0.78 (0.01) | 1.15 (0.05) | 0.77 (0.01) | 1.45 (0.04) | 0.77 (0.01) | 0.81 (0.01) |
| US-born, Mexican ancestry | 0.78 (0.02) | 0.81 (0.02) | 0.82 (0.02) | 0.95 (0.02) | 0.73 (0.02) | 1.14 (0.06) | 0.72 (0.02) | 1.50 (0.06) | 0.73 (0.02) | 0.76 (0.02) |
| Mexico-born, all | 0.18 (0.01) | 0.17 (0.01) | 0.26 (0.01) | 0.33 (0.02) | — | — | 0.25 (0.01) | 0.38 (0.04) | 0.16 (0.01) | 0.16 (0.01) |
| Mexico-born, naturalized | 0.47 (0.02) | 0.45 (0.02) | 0.54 (0.03) | 0.64 (0.04) | — | — | 0.51 (0.03) | 0.88 (0.09) | 0.43 (0.02) | 0.41 (0.02) |
| US-born, Asian Indian ancestry | 0.17 (0.02) | 0.18 (0.02) | 0.20 (0.03) | 0.36 (0.12) | 0.21 (0.03) | 0.38 (0.12) | 0.23 (0.03) | 0.81 (0.15) | 0.23 (0.03) | 0.24 (0.03) |
| US-born, Asian Indian race | 0.28 (0.04) | 0.30 (0.04) | 0.33 (0.04) | 0.40 (0.08) | 0.34 (0.04) | 0.39 (0.07) | 0.38 (0.05) | 0.61 (0.12) | 0.37 (0.05) | 0.39 (0.05) |
| India-born, all | 0.10 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.19 (0.03) | — | — | 0.12 (0.01) | 0.30 (0.07) | 0.13 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 0.17 (0.02) | 0.16 (0.02) | 0.17 (0.02) | 0.23 (0.04) | — | — | 0.19 (0.02) | 0.54 (0.10) | 0.23 (0.03) | 0.22 (0.03) |
<!-- /part -->

<!-- part: adjust_women_18_49 -->
**Ever on active duty, women 18–49: ratio to US-born non-Hispanic whites (SE) under each adjustment.** "own mix" = indirect standardisation (white rates in the group's own cells); "white mix" and "raked" = the group reweighted to the white distribution. (b) uses age × education × state (and metro size at residence)

| Group | raw | same ages | (a) age × educ, own mix | (a) age × educ, white mix | (b) birth state, own mix | (b) birth state, raked | (b) residence, own mix | (b) residence, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.97 (0.03) | 1.10 (0.03) | 1.12 (0.03) | 1.22 (0.05) | 0.94 (0.03) | 1.42 (0.11) | 0.88 (0.03) | 2.14 (0.11) | 0.91 (0.03) | 1.03 (0.03) |
| US-born, Mexican ancestry | 0.89 (0.04) | 1.01 (0.04) | 1.02 (0.04) | 1.12 (0.06) | 0.86 (0.04) | 1.17 (0.12) | 0.79 (0.04) | 2.10 (0.14) | 0.83 (0.03) | 0.94 (0.04) |
| Mexico-born, all | 0.30 (0.02) | 0.27 (0.02) | 0.40 (0.03) | 0.48 (0.05) | — | — | 0.34 (0.03) | 0.70 (0.12) | 0.27 (0.02) | 0.24 (0.02) |
| Mexico-born, naturalized | 0.78 (0.08) | 0.67 (0.07) | 0.83 (0.09) | 0.92 (0.12) | — | — | 0.71 (0.08) | 1.63 (0.37) | 0.70 (0.08) | 0.61 (0.07) |
| US-born, Asian Indian ancestry | 0.21 (0.06) | 0.25 (0.07) | 0.26 (0.07) | 0.29 (0.14) | 0.25 (0.07) | 0.48 (0.19) | 0.27 (0.08) | 0.55 (0.36) | 0.28 (0.08) | 0.32 (0.09) |
| US-born, Asian Indian race | 0.38 (0.08) | 0.44 (0.09) | 0.46 (0.09) | 0.34 (0.08) | 0.44 (0.09) | 0.40 (0.10) | 0.49 (0.10) | 0.41 (0.20) | 0.49 (0.10) | 0.58 (0.12) |
| India-born, all | 0.19 (0.03) | 0.17 (0.03) | 0.17 (0.03) | 0.31 (0.10) | — | — | 0.18 (0.03) | 0.51 (0.22) | 0.25 (0.04) | 0.23 (0.04) |
| India-born, naturalized | 0.29 (0.06) | 0.25 (0.05) | 0.24 (0.05) | 0.47 (0.17) | — | — | 0.26 (0.05) | 0.70 (0.27) | 0.39 (0.08) | 0.33 (0.07) |
<!-- /part -->

### Does the Indian gap survive?

Yes, under every adjustment that uses the whole group. For US-born men of Asian Indian ancestry
aged 18–49 the ratio to whites is:

- 0.16 (0.02) raw and 0.18 (0.02) at the same ages;
- 0.21 (0.02) at the same age and schooling (own mix) and 0.35 (0.11) at the white mix;
- 0.21 (0.02) at the same age, schooling and birth state, and 0.23 (0.03) at the same age,
  schooling, state and metro size of residence (own mix);
- 0.21 (0.02) against neighbourhood income, 0.24 (0.03) with age held as well.

Schooling does not explain it. Among men aged 25–49 with a bachelor's degree, 1.0% (0.1) of the
US-born of Indian ancestry and 0.6% (0.1) of the India-born have served, against 6.9% (0.0) of
white graduates. Nor does place: at the same ages, the ratio is below 0.45 in every region of
birth, including the Middle Atlantic (0.29, where a quarter of the group was born) and California
(0.14). The only adjustments that lift the ratio far are the rakings to the white mix of places
(0.27–0.81 across bands; 0.35–0.36 for the white mix of schooling), and those rest on a few
cells: at ages 25–49, ten cells hold 54–88% of the raked numerator for men and the Kish effective
samples are 272–653. With birth state in place of residence the same raking gives 0.38 (0.11) for
men 18–49.

The India-born serve at 0.11 (0.01) raw and 0.10–0.21 adjusted (0.34 raked to white places).
Many hold temporary visas and cannot enlist, but the naturalized, who can, serve at 0.19 (0.02)
raw and 0.17–0.26 adjusted (0.58 raked), and those who arrived before 18 at 0.28 (0.04) raw.

### Does the Mexican gap survive?

Partly, and the answer depends on whose mix is used. For US-born men of Mexican Hispanic origin
aged 18–49 the ratio to whites is:

- 0.79 (0.01) raw and 0.88 (0.01) at the same ages. Their raw rate is held down by their youth:
  34% of them are under 25, against 22% of white men aged 18–49 [DATA: `adults_per_year` in
  `derived/military_rates.csv`].
- (a) at the same age and schooling: 0.89 (0.01) at their own schooling mix and 0.98 (0.02) at the
  white mix. At ages 25–49, Mexican-origin men with a degree serve above the white rate (8.3%
  against 6.9%), while those with some college (9.6% against 11.6%) or a high-school diploma
  (4.6% against 6.9%) serve below it; the white mix weights degree holders more. How much of the
  graduates' service is the GI Bill's doing cannot be told from a cross-section.
- (b) at the same age, schooling and birth state: 0.79 (0.01) at their own mix and 1.14 (0.04)
  raked to the white mix; with residence in place of birth state, 0.75 (0.01) and 1.46 (0.04).
  Residence contaminates both: veterans who settled in Texas raise the white comparison rate
  where Mexican-origin men live (9.5% of white men living in Texas have served, against 8.6% of
  Texas-born white men), and Mexican-origin veterans who moved out of the Southwest carry the
  raked estimate.
- (c) 0.74 (0.01) against neighbourhood income and 0.83 (0.01) with age held too. Mexican-origin
  neighbourhoods predict slightly more enlistment than white ones, so (c) widens the gap.

**Where the gap sits.** At the same ages, men born in California have served at 0.71 (0.02) of
California-born white men, in Texas at 0.78 (0.03), in the Mountain states at 0.85 (0.04); with
the Pacific states, New England and births outside the states, 82% of the group was born where
the ratio is 0.55–0.87. The other 18%, born in the Midwest, the South Atlantic, the Middle
Atlantic and the South Central divisions outside Texas, have served at 0.96–1.37 of whites born
there. Raking to the white mix of birth states weights that 18% heavily, which is why it
reverses the sign. By region of residence the spread is wider still, from 0.54 in California to
1.61 in the South Atlantic states and 2.22 in New England (801 records), as expected if veterans
settle near bases.

**Women and current enlistment.** US-born Mexican-origin women serve at 0.97 (0.03) of white
women raw and 1.10 (0.03) at the same ages. Men aged 18–24 now on active duty: 0.98 (0.03) raw
and 0.99 (0.03) at the same ages. For current service members (b) is not meaningful, because
the military assigns their residence.

The Mexico-born serve at 0.19 (0.01) raw and 0.16–0.32 adjusted (0.38 raked); the naturalized
at 0.53 (0.02) raw and 0.41–0.64 adjusted (0.88 raked); those who arrived before 18 at 0.29
(0.01) raw.

<!-- part: regions_mex_men_birth -->
**US-born, Mexican Hispanic origin, ever on active duty, men, ages 18_49, by birth region** — against US-born NH whites of the same birth region

| birth region | records | % of group | rate % (SE) | white rate % (SE) | ratio (SE) | at same ages (SE) |
|---|---:|---:|---:|---:|---:|---:|
| all | 157,635 | 100.0 | 5.52 (0.09) | 7.02 (0.03) | 0.79 (0.01) | 0.88 (0.01) |
| california | 66,130 | 39.5 | 4.97 (0.12) | 7.83 (0.12) | 0.63 (0.02) | 0.71 (0.02) |
| texas | 39,703 | 26.0 | 6.15 (0.18) | 8.63 (0.12) | 0.71 (0.02) | 0.78 (0.03) |
| mountain | 16,751 | 11.2 | 5.65 (0.21) | 7.53 (0.14) | 0.75 (0.03) | 0.85 (0.04) |
| east north central | 11,783 | 8.2 | 5.25 (0.28) | 6.31 (0.07) | 0.83 (0.04) | 0.96 (0.05) |
| south atlantic | 6,301 | 3.9 | 5.91 (0.39) | 7.92 (0.08) | 0.75 (0.05) | 0.96 (0.06) |
| pacific ex california | 4,188 | 2.7 | 6.02 (0.40) | 8.34 (0.18) | 0.72 (0.05) | 0.87 (0.06) |
| west north central | 3,091 | 2.2 | 5.37 (0.39) | 6.56 (0.10) | 0.82 (0.06) | 1.03 (0.08) |
| middle atlantic | 2,919 | 2.0 | 6.05 (0.62) | 5.69 (0.09) | 1.06 (0.11) | 1.37 (0.15) |
| outside states | 3,149 | 2.0 | 5.63 (0.54) | 11.07 (0.39) | 0.51 (0.05) | 0.55 (0.05) |
| west south central ex texas | 1,706 | 1.1 | 7.69 (0.99) | 7.81 (0.15) | 0.98 (0.13) | 1.20 (0.16) |
| east south central | 1,132 | 0.7 | 5.64 (0.90) | 6.86 (0.10) | 0.82 (0.13) | 1.13 (0.18) |
| new england | 782 | 0.6 | 4.60 (1.11) | 5.83 (0.11) | 0.79 (0.19) | 0.80 (0.19) |
<!-- /part -->

<!-- part: regions_mex_men_residence -->
**US-born, Mexican Hispanic origin, ever on active duty, men, ages 18_49, by residence region** — against US-born NH whites of the same residence region

| residence region | records | % of group | rate % (SE) | white rate % (SE) | ratio (SE) | at same ages (SE) |
|---|---:|---:|---:|---:|---:|---:|
| all | 157,635 | 100.0 | 5.52 (0.09) | 7.02 (0.03) | 0.79 (0.01) | 0.88 (0.01) |
| california | 58,516 | 34.1 | 3.74 (0.11) | 7.15 (0.12) | 0.52 (0.02) | 0.54 (0.02) |
| texas | 40,373 | 26.7 | 5.38 (0.14) | 9.52 (0.14) | 0.57 (0.02) | 0.62 (0.02) |
| mountain | 20,428 | 14.0 | 5.78 (0.18) | 8.03 (0.11) | 0.72 (0.02) | 0.80 (0.03) |
| east north central | 11,275 | 8.0 | 3.85 (0.24) | 4.86 (0.06) | 0.79 (0.05) | 0.97 (0.06) |
| south atlantic | 9,150 | 5.4 | 13.59 (0.41) | 9.75 (0.08) | 1.39 (0.04) | 1.61 (0.05) |
| pacific ex california | 5,933 | 3.7 | 9.91 (0.40) | 10.24 (0.15) | 0.97 (0.04) | 1.03 (0.05) |
| west north central | 3,917 | 2.9 | 6.93 (0.42) | 5.91 (0.10) | 1.17 (0.08) | 1.45 (0.09) |
| middle atlantic | 2,939 | 2.0 | 5.38 (0.50) | 4.06 (0.08) | 1.33 (0.13) | 1.74 (0.16) |
| west south central ex texas | 2,435 | 1.6 | 7.15 (0.62) | 7.94 (0.15) | 0.90 (0.08) | 1.11 (0.10) |
| east south central | 1,868 | 1.1 | 10.60 (0.94) | 7.16 (0.12) | 1.48 (0.14) | 1.91 (0.17) |
| new england | 801 | 0.5 | 9.32 (1.18) | 4.67 (0.12) | 1.99 (0.26) | 2.22 (0.30) |
<!-- /part -->

<!-- part: birthstate_men_18_49 -->
**Residence versus birth state, ever on active duty, men, ages 18_49** — ratio to US-born NH whites (SE)

| Group | raw | same ages | (b) full indirect, residence | (b) full indirect, birth state | (b) full raked, residence | (b) full raked, birth state | (b) geo raked, birth state | living outside birth state | ever-served % stayers / movers | ratio stayers / movers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.79 (0.01) | 0.88 (0.01) | 0.75 (0.01) | 0.79 (0.01) | 1.46 (0.04) | 1.14 (0.04) | 1.05 (0.04) | 22% | 3.6 / 12.2 | 0.81 (0.02) / 1.06 (0.02) |
| US-born, Mexican ancestry | 0.76 (0.01) | 0.86 (0.02) | 0.72 (0.01) | 0.75 (0.02) | 1.52 (0.05) | 1.14 (0.05) | 1.06 (0.05) | 21% | 3.4 / 12.8 | 0.76 (0.02) / 1.10 (0.03) |
| US-born, Asian Indian ancestry | 0.16 (0.02) | 0.18 (0.02) | 0.23 (0.03) | 0.21 (0.02) | 0.64 (0.13) | 0.38 (0.11) | 0.24 (0.07) | 50% | 0.4 / 1.8 | 0.08 (0.02) / 0.16 (0.02) |
| US-born, Asian Indian race | 0.24 (0.02) | 0.28 (0.03) | 0.36 (0.04) | 0.33 (0.03) | 0.57 (0.11) | 0.37 (0.07) | 0.29 (0.05) | 48% | 1.3 / 2.1 | 0.30 (0.05) / 0.19 (0.02) |
| All US-born | 0.96 (0.00) | 0.99 (0.00) | 0.96 (0.00) | 0.96 (0.00) | 0.99 (0.00) | 0.98 (0.00) | 0.97 (0.00) | 35% | 4.1 / 11.6 | 0.93 (0.00) / 1.00 (0.00) |
| US-born non-Hispanic white | 1.00 |  |  |  |  |  |  | 36% | 4.4 / 11.6 | 1.00 / 1.00 |
<!-- /part -->

### (c) Neighbourhood income: the DoD table

The brief asked for accessions by home-ZIP income quintile. The DoD table is by **census tract**:
*Population Representation in the Military Services*, FY23, Appendix B, Table B-41 counts
non-prior-service active-component enlisted accessions by the median household income of the
home-of-record tract, in quintiles that split US households into fifths on ACS 2019–2023 data
[SOURCE: `_cache/poprep_fy23_appendix_b.pdf`, PDF page 245; the FY22 table is in
`_cache/poprep_fy22_b41.pdf`]. FY23 accessions by quintile, poorest first: 22,636; 35,526;
30,573; 25,097; 12,746 (17.9%, 28.1%, 24.2%, 19.8%, 10.1%). Rebuilding the cut-points from ACS
2019–2023 tract data gives $54,850, $70,417, $87,267 and $113,961 against DoD's $54,754,
$70,266, $86,937 and $113,181, 0.2–0.7% higher [CALCULATION: `neighborhood.py`].

Per 15–17-year-old living in each quintile, relative enlistment is 0.96, 1.49, 1.25, 1.01 and
0.43 (poorest to richest fifth). The second and third fifths enlist most and the richest fifth
least. Of the India-born, 55% live in richest-fifth tracts, and 53% of US-born Asian Indians,
against 24% of non-Hispanic whites; 24% of US-born Mexican-origin people live in the poorest
fifth and 14% in the richest. Neighbourhood income alone therefore predicts that Indian-origin
groups enlist at 0.74–0.84 of the white rate and Mexican-origin groups at 1.02–1.13, across the
three denominators (15–17-year-olds, the primary one; 18–24-year-olds; households) and both
years. Group counts are for all ages, because the tract tables have no age detail by Mexican or
Indian origin; the teenage versions for Hispanic and Asian 15–17-year-olds (1.06 and 0.81) are
close to the all-age ones. The DoD counts cover enlisted accessions only. Officers come
disproportionately from richer places, so including them would move the Indian expected ratio
towards 1 and the Indian (c) ratio towards the raw ratio [INFERENCE].

<!-- part: neighborhood -->
**(c) Expected ratio to US-born NH whites if only home-tract income mattered**

| Group (tract counts) | FY23 per 15–17 | FY23 per 18–24 | FY23 per household | FY22 per 15–17 | FY22 per 18–24 | FY22 per household |
|---|---:|---:|---:|---:|---:|---:|
| us_born_nh_white | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| us_born_all | 1.013 | 0.994 | 1.009 | 1.023 | 1.000 | 1.019 |
| us_born_mexican_origin | 1.069 | 1.022 | 1.056 | 1.088 | 1.035 | 1.074 |
| mexico_born | 1.106 | 1.040 | 1.087 | 1.129 | 1.057 | 1.109 |
| us_born_asian_indian | 0.762 | 0.834 | 0.793 | 0.764 | 0.838 | 0.795 |
| india_born | 0.744 | 0.829 | 0.779 | 0.741 | 0.829 | 0.776 |
| teen_15_17_nh_white | 0.968 | 0.983 | 0.973 | 0.965 | 0.981 | 0.970 |
| teen_15_17_hispanic | 1.060 | 1.014 | 1.048 | 1.079 | 1.027 | 1.066 |
| teen_15_17_asian | 0.809 | 0.872 | 0.835 | 0.807 | 0.872 | 0.833 |

**Relative accession propensity by tract-income quintile (1 = poorest)**

| basis | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---:|---:|---:|---:|---:|
| FY23 per_teen_15_17 | 0.96 | 1.49 | 1.25 | 1.01 | 0.43 |
| FY23 per_youth_18_24 | 0.68 | 1.40 | 1.28 | 1.12 | 0.59 |
| FY23 per_household | 0.90 | 1.41 | 1.21 | 1.00 | 0.49 |
| FY22 per_teen_15_17 | 1.10 | 1.46 | 1.22 | 1.01 | 0.45 |
| FY22 per_youth_18_24 | 0.76 | 1.34 | 1.24 | 1.10 | 0.61 |
| FY22 per_household | 1.03 | 1.38 | 1.18 | 0.98 | 0.52 |

**Population shares by FY23 tract-income quintile, %**

| group | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---:|---:|---:|---:|---:|
| all_population | 19.2 | 19.4 | 19.7 | 20.1 | 21.6 |
| us_born_all | 19.4 | 19.6 | 19.8 | 20.1 | 21.0 |
| us_born_nh_white | 14.5 | 19.3 | 20.7 | 21.6 | 23.9 |
| mexican_origin_all | 24.8 | 22.9 | 21.3 | 18.6 | 12.4 |
| mexico_born | 26.6 | 24.8 | 21.9 | 17.1 | 9.5 |
| us_born_mexican_origin | 24.0 | 22.2 | 21.0 | 19.2 | 13.6 |
| india_born | 5.2 | 7.4 | 11.4 | 20.8 | 55.3 |
| asian_indian_all | 5.9 | 7.4 | 11.6 | 20.1 | 55.0 |
| us_born_asian_indian | 7.5 | 8.0 | 12.4 | 19.2 | 52.9 |
| youth_18_24_all | 26.2 | 20.1 | 18.9 | 17.6 | 17.2 |
| youth_18_24_nh_white | 22.9 | 19.8 | 19.4 | 18.5 | 19.5 |
| youth_18_24_hispanic | 26.7 | 22.4 | 20.6 | 17.7 | 12.5 |
| youth_18_24_asian | 9.6 | 8.9 | 12.7 | 19.9 | 48.9 |
| teen_15_17_all | 18.7 | 18.8 | 19.3 | 19.6 | 23.5 |
| teen_15_17_nh_white | 12.1 | 17.9 | 20.1 | 21.6 | 28.3 |
| teen_15_17_hispanic | 24.0 | 21.9 | 20.8 | 18.4 | 14.9 |
| teen_15_17_asian | 7.7 | 10.2 | 14.2 | 20.6 | 47.3 |
| households | 19.9 | 19.9 | 19.9 | 19.9 | 20.4 |
| dod_nps_accessions | 17.9 | 28.1 | 24.2 | 19.8 | 10.1 |
<!-- /part -->

## 3. "Or the like": police, corrections, fire and EMS

Public-safety jobs are the civilian counterpart the brief asked for. They are not independent of
military service: veterans get hiring preference in most public employment [TRAINING-DATA], and
many police departments require citizenship [UNVERIFIED], which lowers the foreign-born rates.

- **US-born Mexican origin**: men hold public-safety jobs at 0.93 (0.02) of the white rate per
  worker and 0.89 (0.02) per adult; at the same ages, the same age and schooling, or the same
  places (own mix) the ratio stays at 0.92–0.94 per worker and 0.89–0.95 per adult. Police alone:
  1.01 (0.03) per worker, and above whites once age and schooling are held (1.04 (0.03) at the
  same ages, 1.17 (0.04) at the same age and schooling, 1.21 (0.05) at the same places). Women:
  1.23 (0.05) of white women for public safety and 1.46 (0.10) for police.
- **US-born Asian Indian ancestry**: men 0.26 (0.07) per worker and 0.24 (0.06) per adult;
  every adjustment leaves it at 0.24–0.28 per worker. Women 0.84 (0.22), a small sample.
- **India-born**: men 0.10 (0.01) per worker, women 0.17 (0.06); **Mexico-born** men 0.19
  (0.01), women 0.34 (0.04).
- **Security guards**, not counted as public safety: US-born Mexican-origin men 2.07 (0.08) of the
  white rate; US-born Indian-ancestry men 0.82 (0.22).

<!-- part: protective_public_safety_workers -->
**public_safety_total, per 1,000 employed aged 18–64** — ratio to US-born NH whites (SE)

| Group | men: per 1,000 (SE) | men: ratio raw | men: same ages | men: (a) age × educ | men: (b) full indirect | men: (b) full raked | women: per 1,000 (SE) | women: ratio raw | women: same ages | women: (a) age × educ | women: (b) full indirect | women: (b) full raked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 24.3 (0.5) | 0.93 (0.02) | 0.92 (0.02) | 0.94 (0.02) | 0.93 (0.02) | 0.99 (0.06) | 6.7 (0.3) | 1.23 (0.05) | 1.10 (0.05) | 1.05 (0.05) | 1.21 (0.07) | 1.14 (0.11) |
| US-born, Mexican ancestry | 24.8 (0.7) | 0.95 (0.02) | 0.94 (0.02) | 0.95 (0.02) | 0.93 (0.03) | 1.01 (0.08) | 6.8 (0.3) | 1.24 (0.06) | 1.11 (0.06) | 1.05 (0.06) | 1.22 (0.08) | 1.34 (0.16) |
| Mexico-born, all | 4.9 (0.3) | 0.19 (0.01) | 0.18 (0.01) | 0.30 (0.02) | 0.30 (0.02) | 0.31 (0.04) | 1.8 (0.2) | 0.34 (0.04) | 0.34 (0.04) | 0.39 (0.05) | 0.44 (0.05) | 0.39 (0.08) |
| Mexico-born, naturalized | 10.7 (0.7) | 0.41 (0.03) | 0.42 (0.03) | 0.56 (0.04) | 0.55 (0.04) | 0.42 (0.05) | 2.6 (0.4) | 0.47 (0.07) | 0.51 (0.07) | 0.53 (0.08) | 0.56 (0.08) | 0.48 (0.16) |
| Mexico-born, arrived before 18 | 8.5 (0.5) | 0.33 (0.02) | 0.30 (0.02) | 0.45 (0.03) | 0.44 (0.03) | 0.53 (0.08) | 2.8 (0.4) | 0.51 (0.07) | 0.48 (0.07) | 0.50 (0.08) | 0.58 (0.09) | 0.39 (0.11) |
| US-born, Asian Indian ancestry | 6.8 (1.8) | 0.26 (0.07) | 0.24 (0.06) | 0.28 (0.07) | 0.28 (0.07) | 0.27 (0.10) | 4.6 (1.2) | 0.84 (0.22) | 0.72 (0.19) | 0.83 (0.22) | 0.84 (0.22) | 0.77 (0.30) |
| US-born, Asian Indian race | 6.0 (1.0) | 0.23 (0.04) | 0.22 (0.04) | 0.25 (0.04) | 0.25 (0.04) | 0.26 (0.09) | 3.6 (0.8) | 0.66 (0.14) | 0.56 (0.12) | 0.65 (0.14) | 0.67 (0.14) | 0.86 (0.43) |
| India-born, all | 2.5 (0.3) | 0.10 (0.01) | 0.09 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.19 (0.05) | 0.9 (0.3) | 0.17 (0.06) | 0.16 (0.05) | 0.19 (0.07) | 0.19 (0.07) | 0.29 (0.19) |
| India-born, naturalized | 4.0 (0.6) | 0.15 (0.02) | 0.15 (0.02) | 0.17 (0.03) | 0.16 (0.03) | 0.29 (0.09) | 1.1 (0.5) | 0.20 (0.09) | 0.21 (0.10) | 0.25 (0.11) | 0.24 (0.11) | 0.37 (0.26) |
| India-born, arrived before 18 | 7.0 (1.5) | 0.27 (0.06) | 0.25 (0.05) | 0.28 (0.06) | 0.27 (0.06) | 0.15 (0.05) | 0.6 (0.4) | 0.10 (0.07) | 0.09 (0.06) | 0.10 (0.07) | 0.10 (0.07) | 0.16 (0.19) |
| US-born non-Hispanic white | 26.1 (0.2) | 1.00 (0.00) |  |  |  |  | 5.5 (0.1) | 1.00 (0.00) |  |  |  |  |
| All US-born | 25.1 (0.2) | 0.96 (0.00) | 0.96 (0.00) | 0.96 (0.00) | 0.95 (0.00) | 0.96 (0.00) | 6.2 (0.1) | 1.14 (0.01) | 1.11 (0.01) | 1.10 (0.01) | 1.11 (0.01) | 1.10 (0.01) |
<!-- /part -->

<!-- part: protective_police_workers -->
**police_sheriff_detective, per 1,000 employed aged 18–64** — ratio to US-born NH whites (SE)

| Group | men: per 1,000 (SE) | men: ratio raw | men: same ages | men: (a) age × educ | men: (b) full indirect | men: (b) full raked | women: per 1,000 (SE) | women: ratio raw | women: same ages | women: (a) age × educ | women: (b) full indirect | women: (b) full raked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 13.2 (0.4) | 1.01 (0.03) | 1.04 (0.03) | 1.17 (0.04) | 1.21 (0.05) | 1.24 (0.09) | 3.3 (0.2) | 1.46 (0.10) | 1.43 (0.10) | 1.60 (0.12) | 1.72 (0.16) | 1.41 (0.20) |
| US-born, Mexican ancestry | 13.9 (0.5) | 1.06 (0.04) | 1.10 (0.04) | 1.22 (0.04) | 1.25 (0.05) | 1.25 (0.12) | 3.5 (0.3) | 1.54 (0.13) | 1.51 (0.13) | 1.66 (0.14) | 1.80 (0.20) | 1.84 (0.30) |
| Mexico-born, all | 2.5 (0.2) | 0.19 (0.01) | 0.18 (0.01) | 0.35 (0.03) | 0.33 (0.03) | 0.29 (0.04) | 0.8 (0.1) | 0.36 (0.06) | 0.34 (0.05) | 0.56 (0.09) | 0.60 (0.10) | 0.42 (0.12) |
| Mexico-born, naturalized | 6.0 (0.5) | 0.46 (0.04) | 0.45 (0.04) | 0.67 (0.05) | 0.66 (0.06) | 0.47 (0.07) | 1.1 (0.2) | 0.48 (0.11) | 0.48 (0.11) | 0.64 (0.14) | 0.63 (0.15) | 0.61 (0.32) |
| Mexico-born, arrived before 18 | 4.4 (0.4) | 0.33 (0.03) | 0.31 (0.03) | 0.53 (0.04) | 0.53 (0.05) | 0.64 (0.10) | 1.2 (0.3) | 0.52 (0.12) | 0.48 (0.11) | 0.70 (0.16) | 0.74 (0.18) | 0.45 (0.17) |
| US-born, Asian Indian ancestry | 2.6 (0.8) | 0.20 (0.06) | 0.19 (0.06) | 0.18 (0.06) | 0.18 (0.06) | 0.38 (0.18) | 1.6 (0.7) | 0.70 (0.29) | 0.65 (0.27) | 0.58 (0.24) | 0.55 (0.23) | 1.02 (0.60) |
| US-born, Asian Indian race | 3.5 (0.8) | 0.27 (0.06) | 0.26 (0.06) | 0.25 (0.06) | 0.25 (0.06) | 0.38 (0.17) | 0.7 (0.3) | 0.30 (0.13) | 0.28 (0.12) | 0.25 (0.11) | 0.24 (0.10) | 0.45 (0.41) |
| India-born, all | 1.7 (0.3) | 0.13 (0.02) | 0.12 (0.02) | 0.11 (0.02) | 0.11 (0.02) | 0.21 (0.08) | 0.2 (0.1) | 0.10 (0.04) | 0.09 (0.04) | 0.09 (0.04) | 0.09 (0.04) | 0.07 (0.04) |
| India-born, naturalized | 2.4 (0.5) | 0.18 (0.04) | 0.17 (0.04) | 0.16 (0.04) | 0.15 (0.03) | 0.28 (0.13) | 0.3 (0.2) | 0.15 (0.08) | 0.14 (0.07) | 0.13 (0.07) | 0.13 (0.07) | 0.09 (0.06) |
| India-born, arrived before 18 | 3.6 (1.2) | 0.27 (0.09) | 0.26 (0.09) | 0.25 (0.08) | 0.24 (0.08) | 0.13 (0.05) | 0.5 (0.3) | 0.20 (0.15) | 0.18 (0.14) | 0.17 (0.13) | 0.16 (0.12) | 0.04 (0.03) |
| US-born non-Hispanic white | 13.1 (0.1) | 1.00 (0.00) |  |  |  |  | 2.3 (0.1) | 1.00 (0.00) |  |  |  |  |
| All US-born | 12.8 (0.1) | 0.98 (0.01) | 0.98 (0.01) | 1.00 (0.01) | 0.99 (0.01) | 1.00 (0.01) | 2.7 (0.1) | 1.17 (0.02) | 1.16 (0.02) | 1.18 (0.02) | 1.16 (0.02) | 1.13 (0.02) |
<!-- /part -->

<!-- part: protective_public_safety_adults -->
**public_safety_total, per 1,000 adults aged 18–64** — ratio to US-born NH whites (SE)

| Group | men: per 1,000 (SE) | men: ratio raw | men: same ages | men: (a) age × educ | men: (b) full indirect | men: (b) full raked | women: per 1,000 (SE) | women: ratio raw | women: same ages | women: (a) age × educ | women: (b) full indirect | women: (b) full raked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 18.4 (0.4) | 0.89 (0.02) | 0.89 (0.02) | 0.94 (0.02) | 0.95 (0.02) | 0.97 (0.06) | 4.7 (0.2) | 1.18 (0.05) | 1.05 (0.05) | 1.05 (0.05) | 1.24 (0.07) | 1.13 (0.11) |
| US-born, Mexican ancestry | 18.8 (0.5) | 0.91 (0.02) | 0.91 (0.02) | 0.95 (0.02) | 0.96 (0.03) | 0.99 (0.08) | 4.8 (0.2) | 1.21 (0.06) | 1.07 (0.06) | 1.06 (0.06) | 1.25 (0.08) | 1.35 (0.16) |
| Mexico-born, all | 4.2 (0.2) | 0.20 (0.01) | 0.19 (0.01) | 0.34 (0.02) | 0.33 (0.02) | 0.33 (0.04) | 1.1 (0.1) | 0.27 (0.03) | 0.27 (0.03) | 0.37 (0.04) | 0.45 (0.05) | 0.36 (0.07) |
| Mexico-born, naturalized | 9.2 (0.6) | 0.45 (0.03) | 0.44 (0.03) | 0.62 (0.04) | 0.61 (0.04) | 0.45 (0.06) | 1.7 (0.2) | 0.43 (0.06) | 0.46 (0.07) | 0.55 (0.08) | 0.62 (0.09) | 0.47 (0.15) |
| Mexico-born, arrived before 18 | 7.2 (0.4) | 0.35 (0.02) | 0.32 (0.02) | 0.49 (0.03) | 0.49 (0.03) | 0.55 (0.07) | 1.8 (0.3) | 0.45 (0.07) | 0.40 (0.06) | 0.50 (0.07) | 0.61 (0.09) | 0.39 (0.10) |
| US-born, Asian Indian ancestry | 4.9 (1.3) | 0.24 (0.06) | 0.24 (0.06) | 0.25 (0.07) | 0.26 (0.07) | 0.39 (0.18) | 3.2 (0.8) | 0.79 (0.21) | 0.68 (0.18) | 0.72 (0.19) | 0.76 (0.20) | 1.27 (0.73) |
| US-born, Asian Indian race | 4.2 (0.7) | 0.21 (0.04) | 0.21 (0.04) | 0.22 (0.04) | 0.23 (0.04) | 0.29 (0.12) | 2.4 (0.5) | 0.61 (0.13) | 0.53 (0.11) | 0.56 (0.12) | 0.60 (0.13) | 0.84 (0.46) |
| India-born, all | 2.3 (0.3) | 0.11 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.11 (0.01) | 0.17 (0.04) | 0.6 (0.2) | 0.16 (0.05) | 0.14 (0.05) | 0.16 (0.06) | 0.17 (0.06) | 0.38 (0.30) |
| India-born, naturalized | 3.6 (0.6) | 0.17 (0.03) | 0.16 (0.03) | 0.17 (0.03) | 0.17 (0.03) | 0.28 (0.09) | 0.8 (0.4) | 0.21 (0.10) | 0.21 (0.10) | 0.24 (0.11) | 0.24 (0.11) | 0.27 (0.18) |
| India-born, arrived before 18 | 5.6 (1.2) | 0.27 (0.06) | 0.26 (0.05) | 0.27 (0.06) | 0.27 (0.06) | 0.12 (0.03) | 0.4 (0.3) | 0.10 (0.07) | 0.09 (0.06) | 0.09 (0.06) | 0.10 (0.06) | 0.14 (0.20) |
| US-born non-Hispanic white | 20.6 (0.1) | 1.00 (0.00) |  |  |  |  | 4.0 (0.1) | 1.00 (0.00) |  |  |  |  |
| All US-born | 19.1 (0.1) | 0.93 (0.00) | 0.92 (0.00) | 0.93 (0.00) | 0.93 (0.00) | 0.94 (0.00) | 4.5 (0.1) | 1.12 (0.01) | 1.09 (0.01) | 1.09 (0.01) | 1.10 (0.01) | 1.10 (0.01) |
<!-- /part -->

## 4. Volunteering, giving and veteran status by generation (CPS)

Source: CPS September Civic Engagement and Volunteering supplements, 2021 and 2023 pooled, public-use
CSVs with the 160 successive-difference replicate weights of the supplement weight [SOURCE:
www2.census.gov/programs-surveys/cps/datasets/{2021,2023}/supp/, cached in `_cache/cps/`]. Adults
18+ with a supplement interview. "Volunteered" is the published formal-volunteering measure
(`PRSUPVOL`); "gave" is money or goods worth more than $25 to a charity, school, religious or other
non-political organisation (`PES18`); "veteran" is ever on active duty (`PEAFEVER`) among civilian
men born 1956 or later, the only military measure with parents' birthplace. Generations: Mexico-born
and India-born; second generation = US-born with a parent born in Mexico (or India); third-plus
Mexican = US-born, both parents born in the US or its areas, Hispanic origin Mexican. No
third-plus Indian group is identifiable. Adjusted gaps are weighted linear-probability
coefficients against US-born non-Hispanic whites with age band, sex, education (five levels),
family income (six brackets) and survey year, then adding state and metro status.

- **Mexican origin.** Volunteering rises by generation, 10.9% → 15.1% → 19.7%, and giving from
  29.4% (first) and 28.0% (second) to 38.2% (third-plus), all below whites (30.7% and 57.2%).
  Age, sex, education and family income account for 40–60% of each gap: third-plus −11.2
  points raw and −6.0 adjusted for volunteering, −19.0 and −7.6 for giving.
- **India-born.** Close to whites raw (−5.2 and −4.2 points), well below them at equal age,
  sex, education and income (−18.3 and −15.6), because 92% of India-born respondents hold a
  degree and white graduates volunteer at 43.8% and give at 72.7%. Ladder 152 found the same gap
  of about 20 points among graduates.
- **Indian second generation** (170 respondents): indistinguishable from whites raw (−0.5 and
  −1.1 points, SE 4–5); adjusted, −8.3 (4.6) for volunteering and −0.6 (5.4) for giving.
- **Veteran status.** The CPS reproduces the ACS ordering: Mexican third-plus 6.7% against 8.7%
  for white men, −2.0 points (1.0) raw and −0.6 (1.0) at equal age, education and family
  income; second
  generation −3.9 (0.8) and −1.3 (0.8). For this outcome education and family income are partly
  results of service, so **the adjusted veteran gaps cannot separate cause from outcome**. No
  Indian second-generation man in the sample (0 of 84) is a veteran; the replicate SE of a zero
  count is not meaningful.

<!-- part: cps -->
**CPS September 2021+2023, rates % (SE)**

| Group | volunteered, 18+ | gave >$25, 18+ | volunteered, BA+ | gave >$25, BA+ | veteran, men born 1956+ |
|---|---:|---:|---:|---:|---:|
| Mexico-born | 10.9 (0.8) n=2,699 | 29.4 (1.1) n=2,565 | 21.6 (2.8) n=260 | 42.4 (3.7) n=245 | 0.8 (0.3) n=1,191 |
| Mexico-born citizens | 12.1 (1.1) n=1,012 | 37.1 (1.9) n=966 | 27.4 (4.0) n=143 | 52.5 (4.9) n=137 | 2.4 (0.8) n=378 |
| Mexican second generation | 15.1 (1.0) n=1,895 | 28.0 (1.3) n=1,805 | 28.8 (2.9) n=364 | 44.1 (3.0) n=345 | 4.8 (0.8) n=849 |
| Mexican third-plus | 19.7 (1.1) n=1,981 | 38.2 (1.6) n=1,841 | 36.2 (2.8) n=415 | 59.1 (2.8) n=389 | 6.7 (1.0) n=815 |
| India-born | 25.6 (2.0) n=824 | 53.0 (2.5) n=773 | 26.7 (2.1) n=760 | 55.9 (2.6) n=711 | 0.2 (0.2) n=415 |
| India-born citizens | 30.5 (2.9) n=357 | 63.6 (3.9) n=333 | 34.6 (3.1) n=315 | 70.2 (3.6) n=291 | 0.4 (0.4) n=163 |
| Indian second generation | 30.1 (4.5) n=170 | 56.1 (5.4) n=159 | 27.5 (4.3) n=136 | 60.5 (6.1) n=130 | 0.0 (0.0) n=84 |
| US-born Asian Indian (self-ID) | 25.5 (4.3) n=180 | 53.4 (5.1) n=161 | 24.7 (4.4) n=138 | 62.1 (5.5) n=127 | 1.5 (1.5) n=92 |
| US-born NH white | 30.7 (0.3) n=64,922 | 57.2 (0.3) n=61,083 | 43.8 (0.4) n=26,193 | 72.7 (0.4) n=24,847 | 8.7 (0.2) n=21,800 |
| All US-born | 27.6 (0.2) n=82,477 | 51.6 (0.3) n=77,438 | 41.5 (0.4) n=31,125 | 69.2 (0.4) n=29,455 | 8.5 (0.2) n=28,542 |

**Gap to US-born NH whites, percentage points (SE)**

| measure | group | raw | SES-adjusted | SES + state + metro |
|---|---:|---:|---:|---:|
| volunteered | Mexico-born | -19.8 (0.9) | -10.2 (1.0) | -9.2 (1.0) |
| volunteered | Mexican second generation | -15.8 (1.0) | -9.1 (1.0) | -8.0 (1.1) |
| volunteered | Mexican third-plus | -11.2 (1.1) | -6.0 (1.1) | -5.2 (1.1) |
| volunteered | India-born | -5.2 (2.0) | -18.3 (2.1) | -17.0 (2.1) |
| volunteered | Indian second generation | -0.5 (4.4) | -8.3 (4.6) | -6.6 (4.5) |
| gave_over_25 | Mexico-born | -27.8 (1.2) | -11.1 (1.3) | -8.6 (1.4) |
| gave_over_25 | Mexican second generation | -29.1 (1.3) | -12.3 (1.3) | -9.4 (1.4) |
| gave_over_25 | Mexican third-plus | -19.0 (1.6) | -7.6 (1.5) | -5.6 (1.4) |
| gave_over_25 | India-born | -4.2 (2.5) | -15.6 (2.3) | -14.9 (2.3) |
| gave_over_25 | Indian second generation | -1.1 (5.4) | -0.6 (5.4) | +0.6 (5.3) |
| veteran | Mexico-born | -7.9 (0.3) | -6.3 (0.4) | -6.2 (0.5) |
| veteran | Mexican second generation | -3.9 (0.8) | -1.3 (0.8) | -1.0 (0.9) |
| veteran | Mexican third-plus | -2.0 (1.0) | -0.6 (1.0) | -0.8 (1.1) |
| veteran | India-born | -8.5 (0.3) | -6.7 (0.4) | -6.5 (0.5) |
| veteran | Indian second generation | -8.7 (0.2) | -4.5 (0.6) | -4.2 (0.7) |
| volunteered_pes16 | Mexico-born | -20.2 (0.7) | -9.8 (0.8) | -8.8 (0.9) |
| volunteered_pes16 | Mexican second generation | -15.5 (1.0) | -8.5 (1.0) | -7.3 (1.1) |
| volunteered_pes16 | Mexican third-plus | -11.7 (1.1) | -6.1 (1.0) | -5.1 (1.1) |
| volunteered_pes16 | India-born | -5.6 (2.0) | -17.1 (2.1) | -16.0 (2.1) |
| volunteered_pes16 | Indian second generation | +2.7 (4.7) | -5.0 (4.9) | -3.7 (4.9) |
<!-- /part -->

## Every specification computed

Every number below is in a CSV under `derived/`; the tables in this file are printed from them by
`summarize.py`.

- `military_rates.csv`: 12 groups × 2 sexes × 5 age bands (18–24, 18–49, 25–49, 25–34, 18+ born
  1956 or later) × 3 outcomes × 2 universes (all, households only): rate, SE, ratio to whites and
  its SE, records, adults per year, share in group quarters.
- `military_by_education.csv`: the same by own education (four levels), all universe.
- `military_adjusted.csv`: for each group, sex, band and outcome, the ratio and its SE under
  `raw`; `age_direct`, `age_indirect`; `a_education_direct`, `a_education_indirect`;
  `a_age_education_direct`, `a_age_education_indirect`; `b_raked_geo`, `b_raked_full`,
  `b_indirect_geo`, `b_indirect_full`; `c_neighborhood_` and `c_age_neighborhood_` ×
  `per_teen_15_17`, `per_youth_18_24`, `per_household`; with raking diagnostics (Kish effective
  sample, top-10-cell share of the numerator, largest factor over the median, white weight off
  common support, margins used, replicate fallbacks) and the share of each indirect
  standardisation resolved at its finest cell.
- `military_birthstate.csv`, `military_movers.csv`: US-born groups; `b_birthstate_raked_geo`,
  `b_birthstate_raked_full`, `b_birthstate_indirect_geo`, `b_birthstate_indirect_full`; share
  living outside the birth state, and rates and ratios of stayers and movers.
- `military_by_region.csv`: four US-born groups × 2 sexes × 2 bands × birth region and residence
  region (12 regions), raw and age-standardised ratios.
- `protective_service.csv`: 7 occupation sets × 12 groups × 2 sexes × per 1,000 employed and per
  1,000 adults aged 18–64, under the same specifications except (c).
- `neighborhood_quintiles.csv`, `neighborhood_expected.csv`: FY23 and FY22, three denominators.
- `cps_civic_rates.csv`: 11 groups × 6 samples (adults, degree holders, family income $100k+,
  men 18–49, women 18–49, men born 1956+) × 4 measures; `cps_civic_gaps.csv`: 5 groups × 4
  measures (the two volunteering definitions, giving, veteran) × raw, SES, SES plus geography.

The CSVs hold more than this file prints: the adjusted ratios for every outcome, band and sex
(the tables show ever on active duty for five group-band cuts and now on active duty for men
18–24), all seven occupation sets per worker and per adult, and the household-only rates.

## Deviations from the brief

- **(c) is by census tract, not ZIP.** The DoD table the brief pointed to groups home-of-record
  addresses by tract median income. FY23 (latest) is the primary; FY22 is a check.
- **Age held fixed as its own step.** Inside each age band the US-born origin groups are younger
  than whites (34–39% of the men aged 18–49 are under 25, against 22%) and the foreign-born
  older (9–10%), and "ever served" accumulates with age, so the raw ratios understate the US-born
  groups' rates at equal ages and overstate the foreign-born's. Age is not SES; it is shown
  before the SES adjustments, and (a) and (c) are also shown with age held fixed.
- **Indirect standardisation beside raking.** Raking to the white mix of states and metros relies
  on the few group members who live where whites do (see the diagnostics), so each (b) is also
  computed the other way round.
- **Added checks**: birth state and region of birth for the US-born; a race-based Indian group
  (`RAC2P`), Mexican ancestry beside Hispanic origin, the foreign-born who arrived before 18; a
  household-only universe; veteran status in the CPS.
- **Metro size** comes from Geocorr 2022 PUMA-to-CBSA population shares and the OMB July 2023
  delineation, in four classes (5 million+, 1–5 million, under 1 million, non-metro); 8.8% of the
  population lives in PUMAs whose class covers less than 80% of the PUMA [DATA: `_cache/metro.log`].
- **Wealth** is not measured in the ACS person file or the CPS supplement. Home value and tenure
  exist in the ACS but for adults they follow their own careers, service included, so they were
  not used.

## Judgement calls and their direction

Each call below moves a group's adjusted ratio; the direction is listed so the lean can be checked
(symmetry rules, `notes/quant-bias-checklist.md`).

| Call | Mexican-origin (US-born men 18–49) | Indian-origin (US-born men 18–49) |
|---|---|---|
| Hold age fixed before any SES adjustment | raises the ratio, 0.79 → 0.88 | raises it, 0.16 → 0.18 |
| Treat raking to white places as less credible than own-mix standardisation | lowers it (raked 1.14–1.46 against own mix 0.75–0.79) | lowers it (raked 0.34–0.64 against own mix 0.20–0.23) |
| Birth state in place of residence | raises the own-mix ratio (0.75 → 0.79), lowers the raked (1.46 → 1.14) | lowers both (own mix 0.23 → 0.21; raked 0.64 → 0.38) |
| Report (a) at both mixes and call it unable to separate cause from outcome | keeps 0.98 (white mix) beside 0.89 (own mix) | keeps 0.35 (white mix, SE 0.11) beside 0.21 (own mix) |
| Use (c) at all | lowers it (0.79 → 0.74), since Mexican-origin tracts predict more enlistment | raises it (0.16 → 0.21) |

The calls cut both ways for each group.

## Limits

- **Eligibility.** Enlistment is open only to US nationals, lawful permanent residents and
  citizens of the Freely Associated States, unless a Secretary makes a critical-skills exception
  [SOURCE: 10 U.S.C. § 504(b)]. "Mexico-born, all" and "India-born, all" include many
  unauthorized residents and temporary-visa holders who cannot enlist, so their ratios mix
  eligibility with choice. The arrived-before-18 rows are closer to a like-for-like comparison.
- **Naturalization partly follows service.** Honourable service during designated periods of
  hostilities allows naturalization without the usual residence and physical-presence periods
  [SOURCE: 8 U.S.C. § 1440(a)–(b)], and the period since September 2001 is designated
  [TRAINING-DATA: Executive Order 13269]. The naturalized ratios therefore overstate propensity.
- **Stock, not flow.** "Ever served" at 18–49 sums enlistment decisions made since about
  1990. "Now on active duty" at 18–24 is the nearest to current enlistment, and it covers only
  service members stationed in the US.
- **Identity.** Hispanic origin and ancestry are self-reported and the US-born Mexican-origin
  groups differ: the seven ancestry codes capture 267,148 adult records against 423,075 with
  Mexican Hispanic origin. US-born Asian Indian ancestry is a small sample (6,340 men aged 18–49
  in three years), hence the SEs of 0.02–0.03 on its ratios.
- **(c) uses the group's current tracts at all ages** against pre-service tracts on the DoD side,
  and enlisted accessions only.
- **The CPS** has 170 Indian second-generation respondents and 84 men among them born 1956 or
  later.
- **Unexplained heterogeneity.** Why US-born Mexican-origin men born outside the Southwest serve at
  or above the white rate of their birth region is not identified here; children born to parents
  stationed there, mixed parentage and different family selection are all possible, and the ACS
  has no parental service to test the first.

## For the parent to check

1. **Which Mexican geography answer to carry.** At the same ages, schooling and birth state, the
   own-mix ratio is 0.79 (0.01) and the white-mix (raked) ratio 1.14 (0.04). The region table
   shows why: 82% of US-born Mexican-origin men were born in regions where they serve below whites
   born there, and the raked answer leans on the other 18%. Whether those 18% are selected (children of
   service members born near bases, mixed parentage) is untested. Quote both or neither.
2. **Do not quote the Indian raked ratios as "the adjusted gap".** For the US-born at ages
   25–49, ten cells carry 54–96% of their numerator (men and women; Kish effective samples
   206–653); the birth-state version of the same raking gives 0.38 (0.11) for men 18–49.
3. **Table B-41 was transcribed by hand** into `neighborhood.py` (`POPREP`) from the FY23 PDF
   (page 245) and the FY22 extract; spot-check the ten accession counts and eight cut-points.
4. **The CPS veteran cell for the Indian second generation is 0 of 84**; its SE is not
   meaningful, and the adjusted veteran gaps cannot separate cause from outcome.
5. **Foreign-born "all" and naturalized ratios are not propensities**: eligibility (10 U.S.C.
   § 504(b)) and naturalization through service (8 U.S.C. § 1440) move them.
6. **Ladder wording**: keep "per capita" (raw) and "at equal age" apart from "at equal SES", and
   say which adjustment a number comes from. Nothing in this lane is committed.

## Reproduce

From the repository root. `neighborhood.py` and `gate.py` call the Census API; the key is read from
the environment and never printed. Raw pulls and Parquet files go to the ignored `_cache/`.

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
L=infra/immigration-fiscal/service_by_ses_2026_09_23
run() { OPENBLAS_NUM_THREADS=1 uv run --no-project python3 "$L/$1" "${@:2}"; }
run extract_acs.py            # local ACS zips -> _cache/acs{2022,2023,2024}_persons.parquet
run metro.py                  # Geocorr PUMA -> CBSA shares, OMB 2023 list -> derived/puma_metro_size.csv
run neighborhood.py           # ACS 2019-2023 tract pulls; DoD Table B-41 -> derived/neighborhood_*.csv
run gate.py                   # PUMS totals against published B21001 and B23025
run reconcile_ladder170.py    # ladder 170's 2024 rates from the same files
run service.py                # about 15 minutes: military and protective tables, all specifications
run birthplace.py             # about 3 minutes: birth-state versions of (b), stayers and movers
run birth_region.py           # region of birth and residence, raw and age-standardised
run cps_civic.py              # downloads the CPS files once; volunteering, giving, veteran status
run summarize.py --fill "$L/RESULT.md"   # refreshes every table in this file from derived/
```

There is no separate test suite. `gate.py` and `reconcile_ladder170.py` exit non-zero on a failed
gate; `service.py` stops if any person record lacks a metro class, `metro.py` if a CBSA is missing
from the OMB list, `cps_civic.py` on a tally, replicate-weight, code or rank failure, and
`neighborhood.py` and `gate.py` if a cached file contains the key. The DoD cut-point and CPS
published-rate comparisons are printed, not asserted.

## Detailed tables

<!-- part: military_men_18_49 -->
**ever_active_duty, men, ages 18_49** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 157,635 | 5.52 (0.09) | 0.79 (0.01) | 0.88 (0.01) | 0.82 (0.01) | 0.89 (0.01) | 0.74 (0.01) | 0.75 (0.01) | 1.34 (0.03) | 1.46 (0.04) | 0.74 (0.01) | 0.83 (0.01) |
| US-born, Mexican ancestry | 98,986 | 5.32 (0.10) | 0.76 (0.01) | 0.86 (0.02) | 0.79 (0.02) | 0.85 (0.02) | 0.71 (0.02) | 0.72 (0.01) | 1.40 (0.05) | 1.52 (0.05) | 0.71 (0.01) | 0.80 (0.02) |
| Mexico-born, all | 72,464 | 1.36 (0.05) | 0.19 (0.01) | 0.17 (0.01) | 0.29 (0.01) | 0.26 (0.01) | 0.17 (0.01) | 0.24 (0.01) | 0.22 (0.02) | 0.38 (0.04) | 0.18 (0.01) | 0.16 (0.01) |
| Mexico-born, naturalized | 16,331 | 3.69 (0.17) | 0.53 (0.02) | 0.46 (0.02) | 0.63 (0.03) | 0.55 (0.03) | 0.43 (0.02) | 0.51 (0.02) | 0.67 (0.08) | 0.88 (0.09) | 0.48 (0.02) | 0.41 (0.02) |
| Mexico-born, arrived before 18 | 35,116 | 2.02 (0.09) | 0.29 (0.01) | 0.27 (0.01) | 0.39 (0.02) | 0.36 (0.02) | 0.26 (0.01) | 0.34 (0.02) | 0.36 (0.04) | 0.74 (0.08) | 0.26 (0.01) | 0.25 (0.01) |
| US-born, Asian Indian ancestry | 6,340 | 1.11 (0.13) | 0.16 (0.02) | 0.18 (0.02) | 0.16 (0.02) | 0.21 (0.02) | 0.20 (0.02) | 0.23 (0.03) | 0.34 (0.06) | 0.64 (0.13) | 0.21 (0.02) | 0.24 (0.03) |
| US-born, Asian Indian race | 8,671 | 1.71 (0.18) | 0.24 (0.02) | 0.28 (0.03) | 0.25 (0.03) | 0.32 (0.03) | 0.31 (0.03) | 0.36 (0.04) | 0.41 (0.07) | 0.57 (0.11) | 0.32 (0.03) | 0.37 (0.04) |
| India-born, all | 25,466 | 0.78 (0.07) | 0.11 (0.01) | 0.10 (0.01) | 0.12 (0.01) | 0.11 (0.01) | 0.11 (0.01) | 0.12 (0.01) | 0.16 (0.04) | 0.34 (0.07) | 0.15 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 8,516 | 1.37 (0.17) | 0.19 (0.02) | 0.17 (0.02) | 0.21 (0.03) | 0.18 (0.02) | 0.18 (0.02) | 0.20 (0.02) | 0.45 (0.10) | 0.58 (0.10) | 0.26 (0.03) | 0.23 (0.03) |
| India-born, arrived before 18 | 4,269 | 1.97 (0.26) | 0.28 (0.04) | 0.30 (0.04) | 0.29 (0.04) | 0.33 (0.04) | 0.33 (0.04) | 0.36 (0.05) | 0.50 (0.11) | 0.54 (0.11) | 0.38 (0.05) | 0.40 (0.05) |
| US-born non-Hispanic white | 1,100,982 | 7.02 (0.03) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 1,677,791 | 6.74 (0.03) | 0.96 (0.00) | 0.99 (0.00) | 0.97 (0.00) | 0.99 (0.00) | 0.95 (0.00) | 0.96 (0.00) | 0.98 (0.00) | 0.99 (0.00) | 0.95 (0.00) | 0.97 (0.00) |
<!-- /part -->

<!-- part: variants_men_18_49 -->
**Direct and indirect versions and other (c) bases, ever_active_duty, men, ages 18_49** — ratio to US-born NH whites (SE)

| Group | age, direct | age, indirect | educ, direct | educ, indirect | age × educ, direct | age × educ, indirect | (c) per 18–24 | (c) per household | (c) + ages, per 18–24 | (c) + ages, per household |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.88 (0.01) | 0.88 (0.01) | 0.90 (0.01) | 0.82 (0.01) | 0.98 (0.02) | 0.89 (0.01) | 0.77 (0.01) | 0.74 (0.01) | 0.86 (0.01) | 0.84 (0.01) |
| US-born, Mexican ancestry | 0.84 (0.02) | 0.86 (0.02) | 0.87 (0.02) | 0.79 (0.02) | 0.95 (0.02) | 0.85 (0.02) | 0.74 (0.01) | 0.72 (0.01) | 0.84 (0.02) | 0.81 (0.02) |
| Mexico-born, all | 0.18 (0.01) | 0.17 (0.01) | 0.35 (0.02) | 0.29 (0.01) | 0.32 (0.01) | 0.26 (0.01) | 0.19 (0.01) | 0.18 (0.01) | 0.17 (0.01) | 0.16 (0.01) |
| Mexico-born, naturalized | 0.51 (0.03) | 0.46 (0.02) | 0.69 (0.04) | 0.63 (0.03) | 0.64 (0.03) | 0.55 (0.03) | 0.51 (0.02) | 0.48 (0.02) | 0.44 (0.02) | 0.42 (0.02) |
| Mexico-born, arrived before 18 | 0.28 (0.01) | 0.27 (0.01) | 0.51 (0.03) | 0.39 (0.02) | 0.53 (0.03) | 0.36 (0.02) | 0.28 (0.01) | 0.27 (0.01) | 0.26 (0.01) | 0.25 (0.01) |
| US-born, Asian Indian ancestry | 0.19 (0.02) | 0.18 (0.02) | 0.18 (0.03) | 0.16 (0.02) | 0.35 (0.11) | 0.21 (0.02) | 0.19 (0.02) | 0.20 (0.02) | 0.22 (0.03) | 0.23 (0.03) |
| US-born, Asian Indian race | 0.29 (0.03) | 0.28 (0.03) | 0.25 (0.03) | 0.25 (0.03) | 0.39 (0.07) | 0.32 (0.03) | 0.29 (0.03) | 0.31 (0.03) | 0.34 (0.03) | 0.36 (0.04) |
| India-born, all | 0.11 (0.01) | 0.10 (0.01) | 0.20 (0.03) | 0.12 (0.01) | 0.21 (0.03) | 0.11 (0.01) | 0.13 (0.01) | 0.14 (0.01) | 0.12 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 0.20 (0.03) | 0.17 (0.02) | 0.25 (0.04) | 0.21 (0.03) | 0.25 (0.05) | 0.18 (0.02) | 0.24 (0.03) | 0.25 (0.03) | 0.20 (0.03) | 0.22 (0.03) |
| India-born, arrived before 18 | 0.31 (0.04) | 0.30 (0.04) | 0.29 (0.05) | 0.29 (0.04) | 0.34 (0.06) | 0.33 (0.04) | 0.34 (0.04) | 0.36 (0.05) | 0.36 (0.05) | 0.38 (0.05) |
| All US-born | 0.99 (0.00) | 0.99 (0.00) | 0.98 (0.00) | 0.97 (0.00) | 1.00 (0.00) | 0.99 (0.00) | 0.97 (0.00) | 0.95 (0.00) | 0.99 (0.00) | 0.98 (0.00) |
<!-- /part -->

<!-- part: military_men_25_49 -->
**ever_active_duty, men, ages 25_49** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 104,249 | 6.60 (0.11) | 0.83 (0.01) | 0.86 (0.01) | 0.85 (0.01) | 0.88 (0.01) | 0.75 (0.01) | 0.77 (0.01) | 1.30 (0.04) | 1.45 (0.04) | 0.77 (0.01) | 0.81 (0.01) |
| US-born, Mexican ancestry | 65,218 | 6.21 (0.13) | 0.78 (0.02) | 0.81 (0.02) | 0.79 (0.02) | 0.82 (0.02) | 0.71 (0.02) | 0.72 (0.02) | 1.34 (0.05) | 1.50 (0.06) | 0.73 (0.02) | 0.76 (0.02) |
| Mexico-born, all | 64,968 | 1.42 (0.06) | 0.18 (0.01) | 0.17 (0.01) | 0.27 (0.01) | 0.26 (0.01) | 0.17 (0.01) | 0.25 (0.01) | 0.21 (0.02) | 0.38 (0.04) | 0.16 (0.01) | 0.16 (0.01) |
| Mexico-born, naturalized | 15,175 | 3.76 (0.19) | 0.47 (0.02) | 0.45 (0.02) | 0.56 (0.03) | 0.54 (0.03) | 0.43 (0.02) | 0.51 (0.03) | 0.62 (0.07) | 0.88 (0.09) | 0.43 (0.02) | 0.41 (0.02) |
| Mexico-born, arrived before 18 | 29,770 | 2.20 (0.11) | 0.28 (0.01) | 0.27 (0.01) | 0.37 (0.02) | 0.37 (0.02) | 0.27 (0.01) | 0.36 (0.02) | 0.36 (0.04) | 0.78 (0.09) | 0.25 (0.01) | 0.25 (0.01) |
| US-born, Asian Indian ancestry | 3,707 | 1.39 (0.19) | 0.17 (0.02) | 0.18 (0.02) | 0.19 (0.03) | 0.20 (0.03) | 0.20 (0.03) | 0.23 (0.03) | 0.34 (0.08) | 0.81 (0.15) | 0.23 (0.03) | 0.24 (0.03) |
| US-born, Asian Indian race | 4,995 | 2.27 (0.29) | 0.28 (0.04) | 0.30 (0.04) | 0.31 (0.04) | 0.33 (0.04) | 0.34 (0.04) | 0.38 (0.05) | 0.42 (0.08) | 0.61 (0.12) | 0.37 (0.05) | 0.39 (0.05) |
| India-born, all | 22,998 | 0.78 (0.07) | 0.10 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.11 (0.01) | 0.10 (0.01) | 0.12 (0.01) | 0.14 (0.03) | 0.30 (0.07) | 0.13 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 7,873 | 1.39 (0.18) | 0.17 (0.02) | 0.16 (0.02) | 0.19 (0.02) | 0.17 (0.02) | 0.18 (0.02) | 0.19 (0.02) | 0.36 (0.09) | 0.54 (0.10) | 0.23 (0.03) | 0.22 (0.03) |
| India-born, arrived before 18 | 3,034 | 2.34 (0.33) | 0.29 (0.04) | 0.30 (0.04) | 0.31 (0.04) | 0.33 (0.05) | 0.34 (0.05) | 0.36 (0.05) | 0.47 (0.08) | 0.46 (0.08) | 0.39 (0.06) | 0.40 (0.06) |
| US-born non-Hispanic white | 866,511 | 7.97 (0.03) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 1,271,928 | 7.80 (0.03) | 0.98 (0.00) | 0.99 (0.00) | 0.98 (0.00) | 0.99 (0.00) | 0.96 (0.00) | 0.97 (0.00) | 0.98 (0.00) | 0.99 (0.00) | 0.97 (0.00) | 0.97 (0.00) |
<!-- /part -->

<!-- part: military_men_25_34 -->
**ever_active_duty, men, ages 25_34** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 55,158 | 5.47 (0.12) | 0.83 (0.02) | 0.84 (0.02) | 0.79 (0.02) | 0.80 (0.02) | 0.70 (0.02) | 0.68 (0.02) | 1.25 (0.04) | 1.31 (0.04) | 0.78 (0.02) | 0.78 (0.02) |
| US-born, Mexican ancestry | 34,543 | 5.09 (0.13) | 0.77 (0.02) | 0.78 (0.02) | 0.73 (0.02) | 0.74 (0.02) | 0.65 (0.02) | 0.63 (0.02) | 1.21 (0.05) | 1.26 (0.06) | 0.72 (0.02) | 0.73 (0.02) |
| Mexico-born, all | 20,217 | 1.32 (0.10) | 0.20 (0.01) | 0.20 (0.01) | 0.25 (0.02) | 0.25 (0.02) | 0.18 (0.01) | 0.22 (0.02) | 0.26 (0.04) | 0.41 (0.07) | 0.18 (0.01) | 0.18 (0.01) |
| Mexico-born, naturalized | 3,799 | 3.95 (0.41) | 0.60 (0.06) | 0.59 (0.06) | 0.62 (0.06) | 0.62 (0.06) | 0.52 (0.06) | 0.54 (0.06) | 0.94 (0.15) | 1.21 (0.17) | 0.54 (0.06) | 0.54 (0.06) |
| Mexico-born, arrived before 18 | 11,474 | 1.75 (0.15) | 0.27 (0.02) | 0.26 (0.02) | 0.30 (0.03) | 0.30 (0.03) | 0.24 (0.02) | 0.27 (0.02) | 0.39 (0.08) | 0.69 (0.12) | 0.24 (0.02) | 0.24 (0.02) |
| US-born, Asian Indian ancestry | 1,864 | 1.07 (0.26) | 0.16 (0.04) | 0.16 (0.04) | 0.20 (0.05) | 0.21 (0.05) | 0.18 (0.04) | 0.22 (0.06) | 0.27 (0.10) | 0.57 (0.19) | 0.21 (0.05) | 0.21 (0.05) |
| US-born, Asian Indian race | 2,621 | 1.67 (0.32) | 0.25 (0.05) | 0.25 (0.05) | 0.31 (0.06) | 0.31 (0.06) | 0.29 (0.05) | 0.36 (0.07) | 0.29 (0.08) | 0.46 (0.11) | 0.33 (0.06) | 0.33 (0.06) |
| India-born, all | 7,248 | 0.68 (0.13) | 0.10 (0.02) | 0.10 (0.02) | 0.14 (0.03) | 0.13 (0.02) | 0.11 (0.02) | 0.14 (0.03) | 0.16 (0.05) | 0.49 (0.14) | 0.14 (0.03) | 0.14 (0.03) |
| India-born, naturalized | 1,563 | 1.28 (0.29) | 0.19 (0.04) | 0.19 (0.04) | 0.23 (0.05) | 0.23 (0.05) | 0.21 (0.05) | 0.25 (0.06) | 0.31 (0.10) | 0.82 (0.24) | 0.26 (0.06) | 0.26 (0.06) |
| India-born, arrived before 18 | 1,441 | 1.58 (0.44) | 0.24 (0.07) | 0.24 (0.07) | 0.28 (0.08) | 0.29 (0.08) | 0.26 (0.07) | 0.31 (0.09) | 0.38 (0.16) | 0.81 (0.26) | 0.32 (0.09) | 0.32 (0.09) |
| US-born non-Hispanic white | 340,233 | 6.60 (0.05) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 532,486 | 6.34 (0.05) | 0.96 (0.00) | 0.96 (0.01) | 0.95 (0.01) | 0.95 (0.01) | 0.93 (0.01) | 0.92 (0.01) | 0.96 (0.01) | 0.95 (0.01) | 0.95 (0.00) | 0.95 (0.00) |
<!-- /part -->

<!-- part: military_men_born_1956_on -->
**ever_active_duty, men, ages 18_plus_born_1956_on** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 193,168 | 6.70 (0.07) | 0.72 (0.01) | 0.91 (0.01) | 0.73 (0.01) | 0.93 (0.01) | 0.79 (0.01) | 0.81 (0.01) | 1.35 (0.03) | 1.49 (0.03) | 0.67 (0.01) | 0.85 (0.01) |
| US-born, Mexican ancestry | 121,091 | 6.45 (0.09) | 0.69 (0.01) | 0.88 (0.01) | 0.70 (0.01) | 0.89 (0.01) | 0.76 (0.01) | 0.77 (0.01) | 1.40 (0.04) | 1.56 (0.04) | 0.64 (0.01) | 0.83 (0.01) |
| Mexico-born, all | 118,099 | 1.56 (0.04) | 0.17 (0.00) | 0.16 (0.00) | 0.24 (0.01) | 0.24 (0.01) | 0.16 (0.00) | 0.23 (0.01) | 0.19 (0.01) | 0.34 (0.02) | 0.15 (0.00) | 0.15 (0.00) |
| Mexico-born, naturalized | 37,592 | 3.24 (0.11) | 0.35 (0.01) | 0.30 (0.01) | 0.44 (0.02) | 0.38 (0.01) | 0.31 (0.01) | 0.38 (0.01) | 0.42 (0.04) | 0.60 (0.06) | 0.31 (0.01) | 0.27 (0.01) |
| Mexico-born, arrived before 18 | 49,290 | 2.42 (0.09) | 0.26 (0.01) | 0.27 (0.01) | 0.33 (0.01) | 0.37 (0.01) | 0.27 (0.01) | 0.36 (0.01) | 0.38 (0.03) | 0.71 (0.07) | 0.23 (0.01) | 0.25 (0.01) |
| US-born, Asian Indian ancestry | 6,793 | 1.18 (0.13) | 0.13 (0.01) | 0.18 (0.02) | 0.13 (0.01) | 0.21 (0.02) | 0.20 (0.02) | 0.23 (0.03) | 0.31 (0.06) | 0.50 (0.10) | 0.17 (0.02) | 0.24 (0.03) |
| US-born, Asian Indian race | 9,338 | 1.94 (0.18) | 0.21 (0.02) | 0.30 (0.03) | 0.21 (0.02) | 0.34 (0.03) | 0.33 (0.03) | 0.38 (0.03) | 0.59 (0.09) | 0.73 (0.11) | 0.27 (0.02) | 0.39 (0.04) |
| India-born, all | 35,872 | 0.91 (0.06) | 0.10 (0.01) | 0.10 (0.01) | 0.11 (0.01) | 0.11 (0.01) | 0.11 (0.01) | 0.13 (0.01) | 0.16 (0.03) | 0.24 (0.04) | 0.13 (0.01) | 0.13 (0.01) |
| India-born, naturalized | 17,030 | 1.32 (0.11) | 0.14 (0.01) | 0.13 (0.01) | 0.15 (0.01) | 0.14 (0.01) | 0.14 (0.01) | 0.16 (0.01) | 0.29 (0.06) | 0.36 (0.07) | 0.19 (0.02) | 0.17 (0.01) |
| India-born, arrived before 18 | 5,195 | 2.42 (0.27) | 0.26 (0.03) | 0.32 (0.04) | 0.27 (0.03) | 0.36 (0.04) | 0.35 (0.04) | 0.39 (0.04) | 0.71 (0.12) | 0.61 (0.12) | 0.35 (0.04) | 0.43 (0.05) |
| US-born non-Hispanic white | 1,903,774 | 9.37 (0.03) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 2,694,541 | 9.19 (0.02) | 0.98 (0.00) | 1.03 (0.00) | 0.99 (0.00) | 1.03 (0.00) | 1.01 (0.00) | 1.02 (0.00) | 1.03 (0.00) | 1.04 (0.00) | 0.97 (0.00) | 1.02 (0.00) |
<!-- /part -->

<!-- part: military_women_18_49 -->
**ever_active_duty, women, ages 18_49** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 152,925 | 1.25 (0.04) | 0.97 (0.03) | 1.10 (0.03) | 1.05 (0.03) | 1.12 (0.03) | 0.84 (0.03) | 0.88 (0.03) | 1.89 (0.10) | 2.14 (0.11) | 0.91 (0.03) | 1.03 (0.03) |
| US-born, Mexican ancestry | 97,045 | 1.15 (0.05) | 0.89 (0.04) | 1.01 (0.04) | 0.95 (0.04) | 1.02 (0.04) | 0.78 (0.03) | 0.79 (0.04) | 1.86 (0.12) | 2.10 (0.14) | 0.83 (0.03) | 0.94 (0.04) |
| Mexico-born, all | 65,041 | 0.39 (0.03) | 0.30 (0.02) | 0.27 (0.02) | 0.44 (0.04) | 0.40 (0.03) | 0.24 (0.02) | 0.34 (0.03) | 0.43 (0.07) | 0.70 (0.12) | 0.27 (0.02) | 0.24 (0.02) |
| Mexico-born, naturalized | 18,555 | 1.00 (0.11) | 0.78 (0.08) | 0.67 (0.07) | 0.93 (0.10) | 0.83 (0.09) | 0.59 (0.06) | 0.71 (0.08) | 1.33 (0.31) | 1.63 (0.37) | 0.70 (0.08) | 0.61 (0.07) |
| Mexico-born, arrived before 18 | 32,140 | 0.56 (0.05) | 0.44 (0.04) | 0.42 (0.04) | 0.58 (0.05) | 0.55 (0.05) | 0.37 (0.03) | 0.47 (0.05) | 0.84 (0.19) | 1.56 (0.40) | 0.39 (0.04) | 0.38 (0.04) |
| US-born, Asian Indian ancestry | 6,035 | 0.27 (0.08) | 0.21 (0.06) | 0.25 (0.07) | 0.20 (0.06) | 0.26 (0.07) | 0.25 (0.07) | 0.27 (0.08) | 0.55 (0.16) | 0.55 (0.36) | 0.28 (0.08) | 0.32 (0.09) |
| US-born, Asian Indian race | 8,340 | 0.48 (0.10) | 0.38 (0.08) | 0.44 (0.09) | 0.37 (0.07) | 0.46 (0.09) | 0.45 (0.09) | 0.49 (0.10) | 0.39 (0.10) | 0.41 (0.20) | 0.49 (0.10) | 0.58 (0.12) |
| India-born, all | 24,172 | 0.24 (0.04) | 0.19 (0.03) | 0.17 (0.03) | 0.18 (0.03) | 0.17 (0.03) | 0.17 (0.03) | 0.18 (0.03) | 0.24 (0.08) | 0.51 (0.22) | 0.25 (0.04) | 0.23 (0.04) |
| India-born, naturalized | 9,921 | 0.37 (0.08) | 0.29 (0.06) | 0.25 (0.05) | 0.28 (0.06) | 0.24 (0.05) | 0.25 (0.05) | 0.26 (0.05) | 0.55 (0.26) | 0.70 (0.27) | 0.39 (0.08) | 0.33 (0.07) |
| India-born, arrived before 18 | 4,199 | 0.45 (0.14) | 0.35 (0.11) | 0.36 (0.11) | 0.34 (0.10) | 0.37 (0.11) | 0.38 (0.12) | 0.40 (0.12) | 0.38 (0.13) | 0.42 (0.17) | 0.47 (0.14) | 0.49 (0.15) |
| US-born non-Hispanic white | 1,064,013 | 1.29 (0.01) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 1,614,610 | 1.46 (0.01) | 1.14 (0.01) | 1.17 (0.01) | 1.16 (0.01) | 1.17 (0.01) | 1.10 (0.01) | 1.12 (0.01) | 1.13 (0.01) | 1.14 (0.01) | 1.12 (0.01) | 1.15 (0.01) |
<!-- /part -->

<!-- part: variants_women_18_49 -->
**Direct and indirect versions and other (c) bases, ever_active_duty, women, ages 18_49** — ratio to US-born NH whites (SE)

| Group | age, direct | age, indirect | educ, direct | educ, indirect | age × educ, direct | age × educ, indirect | (c) per 18–24 | (c) per household | (c) + ages, per 18–24 | (c) + ages, per household |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 1.05 (0.03) | 1.10 (0.03) | 1.12 (0.04) | 1.05 (0.03) | 1.22 (0.05) | 1.12 (0.03) | 0.95 (0.03) | 0.92 (0.03) | 1.07 (0.03) | 1.04 (0.03) |
| US-born, Mexican ancestry | 0.95 (0.04) | 1.01 (0.04) | 1.03 (0.05) | 0.95 (0.04) | 1.12 (0.06) | 1.02 (0.04) | 0.87 (0.04) | 0.84 (0.03) | 0.99 (0.04) | 0.95 (0.04) |
| Mexico-born, all | 0.30 (0.03) | 0.27 (0.02) | 0.51 (0.05) | 0.44 (0.04) | 0.48 (0.05) | 0.40 (0.03) | 0.29 (0.02) | 0.28 (0.02) | 0.26 (0.02) | 0.25 (0.02) |
| Mexico-born, naturalized | 0.83 (0.12) | 0.67 (0.07) | 0.96 (0.11) | 0.93 (0.10) | 0.92 (0.12) | 0.83 (0.09) | 0.75 (0.08) | 0.71 (0.08) | 0.64 (0.07) | 0.62 (0.07) |
| Mexico-born, arrived before 18 | 0.43 (0.04) | 0.42 (0.04) | 0.65 (0.07) | 0.58 (0.05) | 0.66 (0.07) | 0.55 (0.05) | 0.42 (0.04) | 0.40 (0.04) | 0.40 (0.04) | 0.38 (0.04) |
| US-born, Asian Indian ancestry | 0.27 (0.08) | 0.25 (0.07) | 0.20 (0.08) | 0.20 (0.06) | 0.29 (0.14) | 0.26 (0.07) | 0.25 (0.07) | 0.27 (0.08) | 0.30 (0.09) | 0.31 (0.09) |
| US-born, Asian Indian race | 0.36 (0.07) | 0.44 (0.09) | 0.38 (0.09) | 0.37 (0.07) | 0.34 (0.08) | 0.46 (0.09) | 0.45 (0.09) | 0.47 (0.10) | 0.53 (0.11) | 0.55 (0.11) |
| India-born, all | 0.19 (0.04) | 0.17 (0.03) | 0.30 (0.09) | 0.18 (0.03) | 0.31 (0.10) | 0.17 (0.03) | 0.23 (0.04) | 0.24 (0.04) | 0.20 (0.04) | 0.22 (0.04) |
| India-born, naturalized | 0.33 (0.08) | 0.25 (0.05) | 0.39 (0.13) | 0.28 (0.06) | 0.47 (0.17) | 0.24 (0.05) | 0.35 (0.07) | 0.37 (0.08) | 0.30 (0.06) | 0.32 (0.07) |
| India-born, arrived before 18 | 0.35 (0.11) | 0.36 (0.11) | 0.37 (0.14) | 0.34 (0.10) | 0.46 (0.19) | 0.37 (0.11) | 0.42 (0.13) | 0.45 (0.14) | 0.44 (0.13) | 0.47 (0.14) |
| All US-born | 1.16 (0.01) | 1.17 (0.01) | 1.16 (0.01) | 1.16 (0.01) | 1.18 (0.01) | 1.17 (0.01) | 1.14 (0.01) | 1.13 (0.01) | 1.17 (0.01) | 1.15 (0.01) |
<!-- /part -->

<!-- part: military_women_25_49 -->
**ever_active_duty, women, ages 25_49** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 102,440 | 1.42 (0.04) | 0.98 (0.03) | 1.03 (0.03) | 1.04 (0.03) | 1.08 (0.04) | 0.83 (0.03) | 0.89 (0.04) | 1.76 (0.11) | 2.08 (0.13) | 0.92 (0.03) | 0.96 (0.03) |
| US-born, Mexican ancestry | 64,702 | 1.25 (0.06) | 0.86 (0.04) | 0.91 (0.04) | 0.91 (0.04) | 0.94 (0.04) | 0.74 (0.04) | 0.77 (0.04) | 1.67 (0.12) | 1.99 (0.16) | 0.81 (0.04) | 0.85 (0.04) |
| Mexico-born, all | 59,136 | 0.38 (0.03) | 0.26 (0.02) | 0.25 (0.02) | 0.40 (0.03) | 0.39 (0.03) | 0.23 (0.02) | 0.34 (0.03) | 0.34 (0.05) | 0.65 (0.11) | 0.24 (0.02) | 0.23 (0.02) |
| Mexico-born, naturalized | 17,483 | 0.96 (0.11) | 0.66 (0.07) | 0.63 (0.07) | 0.80 (0.09) | 0.78 (0.09) | 0.56 (0.06) | 0.67 (0.08) | 1.16 (0.26) | 1.56 (0.36) | 0.60 (0.07) | 0.57 (0.06) |
| Mexico-born, arrived before 18 | 27,327 | 0.57 (0.06) | 0.40 (0.04) | 0.39 (0.04) | 0.53 (0.05) | 0.54 (0.05) | 0.36 (0.04) | 0.47 (0.05) | 0.78 (0.20) | 1.61 (0.43) | 0.36 (0.03) | 0.36 (0.03) |
| US-born, Asian Indian ancestry | 3,460 | 0.31 (0.08) | 0.22 (0.05) | 0.23 (0.06) | 0.21 (0.05) | 0.23 (0.06) | 0.24 (0.06) | 0.25 (0.06) | 0.54 (0.16) | 0.37 (0.15) | 0.28 (0.07) | 0.30 (0.07) |
| US-born, Asian Indian race | 4,838 | 0.41 (0.08) | 0.28 (0.06) | 0.30 (0.06) | 0.28 (0.06) | 0.30 (0.06) | 0.32 (0.06) | 0.33 (0.07) | 0.35 (0.11) | 0.25 (0.08) | 0.37 (0.08) | 0.39 (0.08) |
| India-born, all | 22,328 | 0.24 (0.04) | 0.17 (0.03) | 0.16 (0.03) | 0.17 (0.03) | 0.16 (0.03) | 0.17 (0.03) | 0.17 (0.03) | 0.23 (0.08) | 0.52 (0.23) | 0.23 (0.04) | 0.22 (0.04) |
| India-born, naturalized | 9,327 | 0.40 (0.08) | 0.27 (0.06) | 0.25 (0.05) | 0.28 (0.06) | 0.25 (0.05) | 0.26 (0.05) | 0.26 (0.06) | 0.55 (0.24) | 0.75 (0.28) | 0.37 (0.08) | 0.34 (0.07) |
| India-born, arrived before 18 | 3,075 | 0.56 (0.18) | 0.38 (0.12) | 0.39 (0.12) | 0.39 (0.12) | 0.40 (0.12) | 0.41 (0.13) | 0.43 (0.13) | 0.37 (0.13) | 0.41 (0.18) | 0.52 (0.16) | 0.53 (0.16) |
| US-born non-Hispanic white | 840,998 | 1.45 (0.01) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 1,230,099 | 1.66 (0.01) | 1.15 (0.01) | 1.16 (0.01) | 1.16 (0.01) | 1.17 (0.01) | 1.11 (0.01) | 1.13 (0.01) | 1.13 (0.01) | 1.14 (0.01) | 1.13 (0.01) | 1.14 (0.01) |
<!-- /part -->

<!-- part: military_now_men_18_24 -->
**now_active_duty, men, ages 18_24** — ratio to US-born non-Hispanic whites (SE)

| Group | records | rate % (SE) | raw | same ages | (a) educ | (a) age × educ | (b) geo, indirect | (b) full, indirect | (b) geo, raked | (b) full, raked | (c) tract income | (c) + same ages |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 53,386 | 2.34 (0.07) | 0.98 (0.03) | 0.99 (0.03) | 0.96 (0.03) | 0.96 (0.03) | 0.63 (0.02) | 0.62 (0.02) | 1.85 (0.08) | 1.83 (0.08) | 0.91 (0.03) | 0.93 (0.03) |
| US-born, Mexican ancestry | 33,768 | 2.57 (0.09) | 1.08 (0.04) | 1.09 (0.04) | 1.06 (0.04) | 1.05 (0.04) | 0.69 (0.03) | 0.67 (0.03) | 2.04 (0.12) | 1.97 (0.11) | 1.01 (0.04) | 1.02 (0.04) |
| Mexico-born, all | 7,496 | 0.45 (0.09) | 0.19 (0.04) | 0.18 (0.04) | 0.21 (0.04) | 0.20 (0.04) | 0.13 (0.03) | 0.14 (0.03) | 0.41 (0.10) | 0.54 (0.14) | 0.17 (0.03) | 0.16 (0.03) |
| Mexico-born, naturalized | 1,156 | 2.03 (0.52) | 0.85 (0.22) | 0.82 (0.21) | 0.86 (0.22) | 0.82 (0.21) | 0.54 (0.14) | 0.53 (0.14) | 0.98 (0.30) | 0.92 (0.28) | 0.77 (0.20) | 0.74 (0.19) |
| Mexico-born, arrived before 18 | 5,346 | 0.62 (0.13) | 0.26 (0.05) | 0.25 (0.05) | 0.27 (0.06) | 0.26 (0.05) | 0.18 (0.04) | 0.18 (0.04) | 0.55 (0.14) | 0.71 (0.17) | 0.23 (0.05) | 0.23 (0.05) |
| US-born, Asian Indian ancestry | 2,633 | 0.52 (0.14) | 0.22 (0.06) | 0.22 (0.06) | 0.23 (0.06) | 0.25 (0.07) | 0.20 (0.06) | 0.24 (0.07) | 0.34 (0.10) | 0.42 (0.14) | 0.28 (0.08) | 0.29 (0.08) |
| US-born, Asian Indian race | 3,676 | 0.59 (0.13) | 0.25 (0.06) | 0.25 (0.06) | 0.26 (0.06) | 0.29 (0.06) | 0.23 (0.06) | 0.28 (0.07) | 0.50 (0.15) | 0.64 (0.21) | 0.33 (0.07) | 0.33 (0.07) |
| India-born, all | 2,468 | 0.38 (0.16) | 0.16 (0.07) | 0.15 (0.06) | 0.18 (0.08) | 0.19 (0.08) | 0.16 (0.07) | 0.20 (0.08) | 0.35 (0.22) | 0.69 (0.37) | 0.22 (0.09) | 0.20 (0.08) |
| India-born, naturalized | 643 | 0.78 (0.49) | 0.32 (0.21) | 0.32 (0.20) | 0.36 (0.23) | 0.38 (0.24) | 0.31 (0.19) | 0.40 (0.25) | 0.40 (0.30) | 1.82 (1.45) | 0.44 (0.28) | 0.43 (0.27) |
| India-born, arrived before 18 | 1,235 | 0.68 (0.27) | 0.29 (0.11) | 0.29 (0.11) | 0.31 (0.12) | 0.34 (0.13) | 0.27 (0.11) | 0.34 (0.13) | 0.87 (0.49) | 1.27 (0.66) | 0.38 (0.15) | 0.39 (0.15) |
| US-born non-Hispanic white | 234,471 | 2.39 (0.04) | 1.00 (0.00) |  | 1.00 (0.00) |  |  |  |  |  | 1.00 (0.00) | 1.00 (0.00) |
| All US-born | 405,863 | 2.33 (0.02) | 0.97 (0.01) | 0.98 (0.01) | 0.98 (0.01) | 0.98 (0.01) | 0.83 (0.01) | 0.84 (0.01) | 0.91 (0.01) | 0.91 (0.01) | 0.96 (0.01) | 0.97 (0.01) |
<!-- /part -->

<!-- part: other_outcomes -->
**Other outcomes** — rate % (SE); ratio to US-born NH whites

| Group | now active duty, men 18–24 | now active duty, women 18–24 | reserve/Guard only, men 18–49 | ever active, men 18–49, households only | ever active, men 18+ born 1956+ | share of men 18–24 on active duty living in group quarters |
|---|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 2.34 (0.07); 0.98 | 0.60 (0.04); 1.43 | 1.01 (0.03); 0.83 | 5.06 (0.08); 0.73 | 6.70 (0.07); 0.72 | 62% |
| US-born, Mexican ancestry | 2.57 (0.09); 1.08 | 0.66 (0.06); 1.58 | 0.98 (0.04); 0.81 | 4.77 (0.10); 0.69 | 6.45 (0.09); 0.69 | 65% |
| Mexico-born, all | 0.45 (0.09); 0.19 | 0.29 (0.10); 0.70 | 0.32 (0.03); 0.26 | 1.34 (0.06); 0.19 | 1.56 (0.04); 0.17 | 48% |
| Mexico-born, naturalized | 2.03 (0.52); 0.85 | 1.22 (0.58); 2.92 | 0.79 (0.08); 0.65 | 3.66 (0.18); 0.53 | 3.24 (0.11); 0.35 | 34% |
| Mexico-born, arrived before 18 | 0.62 (0.13); 0.26 | 0.36 (0.13); 0.85 | 0.47 (0.04); 0.39 | 1.98 (0.10); 0.29 | 2.42 (0.09); 0.26 | 48% |
| US-born, Asian Indian ancestry | 0.52 (0.14); 0.22 | 0.05 (0.10); 0.11 | 0.37 (0.09); 0.30 | 0.91 (0.13); 0.13 | 1.18 (0.13); 0.13 | 79% |
| US-born, Asian Indian race | 0.59 (0.13); 0.25 | 0.16 (0.11); 0.38 | 0.31 (0.07); 0.26 | 1.62 (0.20); 0.24 | 1.94 (0.18); 0.21 | 51% |
| India-born, all | 0.38 (0.16); 0.16 | 0.00 (0.00); 0.00 | 0.23 (0.04); 0.19 | 0.76 (0.07); 0.11 | 0.91 (0.06); 0.10 | 94% |
| India-born, naturalized | 0.78 (0.49); 0.32 | 0.00 (0.00); 0.00 | 0.67 (0.12); 0.55 | 1.32 (0.17); 0.19 | 1.32 (0.11); 0.14 | 100% |
| India-born, arrived before 18 | 0.68 (0.27); 0.29 | 0.00 (0.00); 0.00 | 0.66 (0.17); 0.54 | 1.86 (0.26); 0.27 | 2.42 (0.27); 0.26 | 100% |
| US-born non-Hispanic white | 2.39 (0.04); 1.00 | 0.42 (0.02); 1.00 | 1.22 (0.02); 1.00 | 6.89 (0.03); 1.00 | 9.37 (0.03); 1.00 | 51% |
| All US-born | 2.33 (0.02); 0.97 | 0.52 (0.02); 1.23 | 1.19 (0.01); 0.98 | 6.58 (0.03); 0.96 | 9.19 (0.02); 0.98 | 56% |
<!-- /part -->

<!-- part: education_men_25_49 -->
**Ever on active duty by own education, men, ages 25_49** — rate % (SE), records

| Group | less than HS | HS diploma | some college | BA+ |
|---|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 1.7 (0.1) n=14,345 | 4.6 (0.2) n=35,074 | 9.6 (0.2) n=32,984 | 8.3 (0.2) n=21,846 |
| US-born, Mexican ancestry | 0.4 (0.1) n=8,560 | 4.1 (0.2) n=22,146 | 9.5 (0.3) n=20,995 | 8.2 (0.3) n=13,517 |
| Mexico-born, all | 0.5 (0.0) n=28,098 | 1.2 (0.1) n=19,956 | 3.5 (0.3) n=9,604 | 3.3 (0.2) n=7,310 |
| Mexico-born, naturalized | 1.1 (0.2) n=3,828 | 2.6 (0.3) n=4,848 | 6.5 (0.6) n=3,627 | 6.4 (0.6) n=2,872 |
| Mexico-born, arrived before 18 | 0.7 (0.1) n=10,607 | 1.5 (0.2) n=9,925 | 4.6 (0.4) n=6,001 | 5.7 (0.5) n=3,237 |
| US-born, Asian Indian ancestry | 0.0 (0.0) n=62 | 3.9 (2.3) n=149 | 3.6 (1.1) n=361 | 1.0 (0.1) n=3,135 |
| US-born, Asian Indian race | 1.7 (1.3) n=145 | 3.5 (1.5) n=284 | 5.3 (1.4) n=548 | 1.8 (0.3) n=4,018 |
| India-born, all | 0.8 (0.4) n=570 | 1.9 (0.5) n=779 | 2.7 (0.6) n=1,081 | 0.6 (0.1) n=20,568 |
| India-born, naturalized | 1.2 (0.8) n=269 | 1.5 (0.6) n=405 | 2.9 (0.6) n=732 | 1.2 (0.2) n=6,467 |
| India-born, arrived before 18 | 0.4 (0.5) n=131 | 2.2 (1.0) n=238 | 3.3 (0.8) n=446 | 2.3 (0.4) n=2,219 |
| US-born non-Hispanic white | 1.9 (0.1) n=50,305 | 6.9 (0.1) n=224,520 | 11.6 (0.1) n=242,778 | 6.9 (0.0) n=348,908 |
| All US-born | 1.8 (0.1) n=99,352 | 6.2 (0.1) n=350,383 | 11.4 (0.1) n=361,564 | 7.3 (0.0) n=460,629 |
<!-- /part -->

<!-- part: education_women_25_49 -->
**Ever on active duty by own education, women, ages 25_49** — rate % (SE), records

| Group | less than HS | HS diploma | some college | BA+ |
|---|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.4 (0.1) n=9,487 | 0.8 (0.1) n=26,865 | 1.8 (0.1) n=35,474 | 2.0 (0.1) n=30,614 |
| US-born, Mexican ancestry | 0.0 (0.0) n=5,074 | 0.6 (0.1) n=16,209 | 1.6 (0.1) n=22,959 | 1.9 (0.1) n=20,460 |
| Mexico-born, all | 0.1 (0.0) n=21,746 | 0.2 (0.0) n=17,858 | 1.0 (0.1) n=10,590 | 0.7 (0.1) n=8,942 |
| Mexico-born, naturalized | 0.4 (0.2) n=3,402 | 0.4 (0.1) n=5,114 | 1.7 (0.3) n=4,820 | 1.3 (0.2) n=4,147 |
| Mexico-born, arrived before 18 | 0.2 (0.1) n=7,474 | 0.3 (0.1) n=8,873 | 1.2 (0.2) n=6,854 | 1.1 (0.2) n=4,126 |
| US-born, Asian Indian ancestry | 0.0 (0.0) n=23 | 0.0 (0.0) n=66 | 0.5 (0.3) n=231 | 0.3 (0.1) n=3,140 |
| US-born, Asian Indian race | 1.8 (1.6) n=109 | 0.2 (0.2) n=203 | 0.1 (0.1) n=401 | 0.4 (0.1) n=4,125 |
| India-born, all | 0.1 (0.1) n=588 | 0.9 (0.5) n=797 | 0.6 (0.3) n=1,234 | 0.2 (0.0) n=19,709 |
| India-born, naturalized | 0.0 (0.0) n=282 | 1.2 (0.8) n=488 | 0.6 (0.4) n=781 | 0.3 (0.1) n=7,776 |
| India-born, arrived before 18 | 0.0 (0.0) n=90 | 0.9 (0.8) n=201 | 0.9 (0.8) n=351 | 0.5 (0.2) n=2,433 |
| US-born non-Hispanic white | 0.5 (0.0) n=32,023 | 0.8 (0.0) n=145,247 | 1.9 (0.0) n=234,410 | 1.5 (0.0) n=429,318 |
| All US-born | 0.6 (0.0) n=60,122 | 0.9 (0.0) n=231,398 | 2.2 (0.0) n=358,170 | 1.8 (0.0) n=580,409 |
<!-- /part -->

<!-- part: birthstate_men_25_49 -->
**Residence versus birth state, ever on active duty, men, ages 25_49** — ratio to US-born NH whites (SE)

| Group | raw | same ages | (b) full indirect, residence | (b) full indirect, birth state | (b) full raked, residence | (b) full raked, birth state | (b) geo raked, birth state | living outside birth state | ever-served % stayers / movers | ratio stayers / movers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.83 (0.01) | 0.86 (0.01) | 0.77 (0.01) | 0.78 (0.01) | 1.45 (0.04) | 1.15 (0.05) | 1.04 (0.05) | 25% | 4.8 / 12.1 | 0.88 (0.02) / 1.01 (0.02) |
| US-born, Mexican ancestry | 0.78 (0.02) | 0.81 (0.02) | 0.72 (0.02) | 0.73 (0.02) | 1.50 (0.06) | 1.14 (0.06) | 1.04 (0.06) | 23% | 4.5 / 12.0 | 0.83 (0.02) / 0.99 (0.03) |
| US-born, Asian Indian ancestry | 0.17 (0.02) | 0.18 (0.02) | 0.23 (0.03) | 0.21 (0.03) | 0.81 (0.15) | 0.38 (0.12) | 0.19 (0.05) | 55% | 0.3 / 2.3 | 0.06 (0.02) / 0.19 (0.03) |
| US-born, Asian Indian race | 0.28 (0.04) | 0.30 (0.04) | 0.38 (0.05) | 0.34 (0.04) | 0.61 (0.12) | 0.39 (0.07) | 0.30 (0.05) | 52% | 1.8 / 2.7 | 0.34 (0.07) / 0.22 (0.03) |
| All US-born | 0.98 (0.00) | 0.99 (0.00) | 0.97 (0.00) | 0.97 (0.00) | 0.99 (0.00) | 0.98 (0.00) | 0.97 (0.00) | 37% | 5.2 / 12.2 | 0.96 (0.00) / 1.01 (0.00) |
| US-born non-Hispanic white | 1.00 |  |  |  |  |  |  | 38% | 5.4 / 12.1 | 1.00 / 1.00 |
<!-- /part -->

<!-- part: birthstate_women_18_49 -->
**Residence versus birth state, ever on active duty, women, ages 18_49** — ratio to US-born NH whites (SE)

| Group | raw | same ages | (b) full indirect, residence | (b) full indirect, birth state | (b) full raked, residence | (b) full raked, birth state | (b) geo raked, birth state | living outside birth state | ever-served % stayers / movers | ratio stayers / movers |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 0.97 (0.03) | 1.10 (0.03) | 0.88 (0.03) | 0.94 (0.03) | 2.14 (0.11) | 1.42 (0.11) | 1.26 (0.09) | 23% | 0.7 / 3.2 | 0.98 (0.04) / 1.40 (0.05) |
| US-born, Mexican ancestry | 0.89 (0.04) | 1.01 (0.04) | 0.79 (0.04) | 0.86 (0.04) | 2.10 (0.14) | 1.17 (0.12) | 1.08 (0.10) | 21% | 0.6 / 3.4 | 0.82 (0.05) / 1.46 (0.07) |
| US-born, Asian Indian ancestry | 0.21 (0.06) | 0.25 (0.07) | 0.27 (0.08) | 0.25 (0.07) | 0.55 (0.36) | 0.48 (0.19) | 0.43 (0.15) | 52% | 0.1 / 0.4 | 0.18 (0.14) / 0.17 (0.06) |
| US-born, Asian Indian race | 0.38 (0.08) | 0.44 (0.09) | 0.49 (0.10) | 0.44 (0.09) | 0.41 (0.20) | 0.40 (0.10) | 0.46 (0.11) | 50% | 0.4 / 0.6 | 0.52 (0.16) / 0.26 (0.07) |
| All US-born | 1.14 (0.01) | 1.17 (0.01) | 1.12 (0.01) | 1.12 (0.01) | 1.14 (0.01) | 1.13 (0.01) | 1.12 (0.01) | 35% | 0.8 / 2.7 | 1.13 (0.01) / 1.18 (0.01) |
| US-born non-Hispanic white | 1.00 |  |  |  |  |  |  | 37% | 0.7 / 2.3 | 1.00 / 1.00 |
<!-- /part -->

<!-- part: regions_mex_women_birth -->
**US-born, Mexican Hispanic origin, ever on active duty, women, ages 18_49, by birth region** — against US-born NH whites of the same birth region

| birth region | records | % of group | rate % (SE) | white rate % (SE) | ratio (SE) | at same ages (SE) |
|---|---:|---:|---:|---:|---:|---:|
| all | 152,925 | 100.0 | 1.25 (0.04) | 1.29 (0.01) | 0.97 (0.03) | 1.10 (0.03) |
| california | 65,199 | 40.4 | 1.11 (0.05) | 1.65 (0.06) | 0.67 (0.04) | 0.74 (0.04) |
| texas | 38,178 | 25.4 | 1.40 (0.08) | 1.56 (0.07) | 0.90 (0.07) | 0.99 (0.07) |
| mountain | 15,982 | 11.2 | 1.38 (0.10) | 1.43 (0.06) | 0.96 (0.08) | 1.09 (0.10) |
| east north central | 11,432 | 8.2 | 1.01 (0.11) | 1.16 (0.03) | 0.87 (0.10) | 1.01 (0.12) |
| south atlantic | 6,126 | 4.0 | 1.64 (0.20) | 1.40 (0.04) | 1.17 (0.15) | 1.45 (0.19) |
| pacific ex california | 4,051 | 2.8 | 1.67 (0.27) | 1.67 (0.07) | 1.00 (0.17) | 1.23 (0.22) |
| west north central | 2,961 | 2.2 | 1.56 (0.26) | 1.25 (0.05) | 1.25 (0.22) | 1.50 (0.27) |
| outside states | 2,914 | 1.9 | 1.13 (0.22) | 2.79 (0.21) | 0.41 (0.09) | 0.46 (0.10) |
| middle atlantic | 2,680 | 1.8 | 1.16 (0.23) | 1.06 (0.04) | 1.10 (0.22) | 1.42 (0.28) |
| west south central ex texas | 1,666 | 1.1 | 1.51 (0.37) | 1.18 (0.05) | 1.27 (0.31) | 1.52 (0.38) |
| east south central | 1,059 | 0.6 | 1.01 (0.29) | 0.91 (0.05) | 1.10 (0.33) | 1.42 (0.41) |
| new england | 677 | 0.5 | 0.45 (0.29) | 1.12 (0.05) | 0.40 (0.27) | 0.40 (0.27) |
<!-- /part -->

<!-- part: regions_indian_men_birth -->
**US-born, Asian Indian ancestry, ever on active duty, men, ages 18_49, by birth region** — against US-born NH whites of the same birth region

| birth region | records | % of group | rate % (SE) | white rate % (SE) | ratio (SE) | at same ages (SE) |
|---|---:|---:|---:|---:|---:|---:|
| all | 6,340 | 100.0 | 1.11 (0.13) | 7.02 (0.03) | 0.16 (0.02) | 0.18 (0.02) |
| middle atlantic | 1,647 | 25.5 | 1.40 (0.35) | 5.69 (0.09) | 0.25 (0.06) | 0.29 (0.07) |
| east north central | 1,062 | 18.2 | 0.44 (0.17) | 6.31 (0.07) | 0.07 (0.03) | 0.08 (0.03) |
| california | 1,159 | 17.4 | 0.90 (0.25) | 7.83 (0.12) | 0.11 (0.03) | 0.14 (0.04) |
| south atlantic | 900 | 14.3 | 1.40 (0.35) | 7.92 (0.08) | 0.18 (0.04) | 0.21 (0.05) |
| texas | 482 | 7.2 | 0.65 (0.36) | 8.63 (0.12) | 0.08 (0.04) | 0.09 (0.05) |
| new england | 294 | 4.5 | 0.67 (0.65) | 5.83 (0.11) | 0.11 (0.11) | 0.14 (0.14) |
| outside states | 195 | 3.4 | 3.02 (1.17) | 11.07 (0.39) | 0.27 (0.11) | 0.30 (0.12) |
| west north central | 166 | 2.7 | 1.89 (1.41) | 6.56 (0.10) | 0.29 (0.21) | 0.36 (0.28) |
| east south central | 125 | 1.9 | 1.21 (1.30) | 6.86 (0.10) | 0.18 (0.19) | 0.19 (0.20) |
| mountain | 112 | 1.7 | 2.67 (1.76) | 7.53 (0.14) | 0.35 (0.23) | 0.42 (0.28) |
| pacific ex california | 114 | 1.6 | 0.00 (0.00) | 8.34 (0.18) | 0.00 (0.00) | 0.00 (0.00) |
| west south central ex texas | 84 | 1.5 | 0.90 (0.95) | 7.81 (0.15) | 0.12 (0.12) | 0.13 (0.14) |
<!-- /part -->

<!-- part: raking_men_25_49 -->
**Raking diagnostics, men, ages 25_49**

| Group | spec | records | Kish n_eff | top-10 cells' share of numerator | max/median factor | white weight off support | margins | replicate fallbacks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | b_raked_geo | 104,249 | 11,293 | 7% | 12 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Mexican Hispanic origin | b_raked_full | 104,249 | 10,076 | 8% | 19 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Mexican ancestry | b_raked_geo | 65,218 | 6,452 | 10% | 19 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Mexican ancestry | b_raked_full | 65,218 | 5,862 | 10% | 30 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, all | b_raked_geo | 64,968 | 7,336 | 26% | 61 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, all | b_raked_full | 64,968 | 4,808 | 26% | 129 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, naturalized | b_raked_geo | 15,175 | 1,627 | 37% | 31 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, naturalized | b_raked_full | 15,175 | 1,449 | 38% | 41 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, arrived before 18 | b_raked_geo | 29,770 | 3,056 | 36% | 43 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, arrived before 18 | b_raked_full | 29,770 | 1,825 | 35% | 78 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Asian Indian ancestry | b_raked_geo | 3,707 | 512 | 66% | 24 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Asian Indian ancestry | b_raked_full | 3,707 | 272 | 88% | 75 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Asian Indian race | b_raked_geo | 4,995 | 653 | 54% | 108 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Asian Indian race | b_raked_full | 4,995 | 393 | 72% | 225 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, all | b_raked_geo | 22,998 | 3,059 | 49% | 33 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, all | b_raked_full | 22,998 | 1,273 | 65% | 73 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, naturalized | b_raked_geo | 7,873 | 853 | 62% | 39 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, naturalized | b_raked_full | 7,873 | 560 | 73% | 58 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, arrived before 18 | b_raked_geo | 3,034 | 520 | 63% | 41 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, arrived before 18 | b_raked_full | 3,034 | 390 | 63% | 155 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| All US-born | b_raked_geo | 1,271,928 | 658,911 | 3% | 1 | 0.0% | age, state, division x metro (min 20) | 0 |
| All US-born | b_raked_full | 1,271,928 | 658,780 | 3% | 2 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
<!-- /part -->

<!-- part: raking_women_25_49 -->
**Raking diagnostics, women, ages 25_49**

| Group | spec | records | Kish n_eff | top-10 cells' share of numerator | max/median factor | white weight off support | margins | replicate fallbacks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | b_raked_geo | 102,440 | 10,493 | 12% | 10 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Mexican Hispanic origin | b_raked_full | 102,440 | 9,263 | 14% | 19 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Mexican ancestry | b_raked_geo | 64,702 | 6,132 | 15% | 13 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Mexican ancestry | b_raked_full | 64,702 | 5,588 | 19% | 21 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, all | b_raked_geo | 59,136 | 6,057 | 37% | 70 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, all | b_raked_full | 59,136 | 3,488 | 40% | 99 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, naturalized | b_raked_geo | 17,483 | 1,850 | 55% | 36 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, naturalized | b_raked_full | 17,483 | 1,470 | 54% | 47 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| Mexico-born, arrived before 18 | b_raked_geo | 27,327 | 2,054 | 53% | 287 | 0.0% | age, state, division x metro (min 20) | 0 |
| Mexico-born, arrived before 18 | b_raked_full | 27,327 | 1,263 | 64% | 504 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Asian Indian ancestry | b_raked_geo | 3,460 | 406 | 94% | 214 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Asian Indian ancestry | b_raked_full | 3,460 | 206 | 96% | 201 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| US-born, Asian Indian race | b_raked_geo | 4,838 | 543 | 87% | 56 | 0.0% | age, state, division x metro (min 20) | 0 |
| US-born, Asian Indian race | b_raked_full | 4,838 | 371 | 85% | 280 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, all | b_raked_geo | 22,328 | 2,620 | 73% | 33 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, all | b_raked_full | 22,328 | 1,627 | 87% | 60 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, naturalized | b_raked_geo | 9,327 | 1,059 | 90% | 62 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, naturalized | b_raked_full | 9,327 | 826 | 93% | 84 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| India-born, arrived before 18 | b_raked_geo | 3,075 | 600 | 91% | 53 | 0.0% | age, state, division x metro (min 20) | 0 |
| India-born, arrived before 18 | b_raked_full | 3,075 | 463 | 90% | 74 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
| All US-born | b_raked_geo | 1,230,099 | 647,458 | 5% | 1 | 0.0% | age, state, division x metro (min 20) | 0 |
| All US-born | b_raked_full | 1,230,099 | 650,831 | 5% | 2 | 0.0% | age x educ, state, metro x educ, division x metro (min 20) | 0 |
<!-- /part -->

<!-- part: protective_soc33_workers -->
**all_protective_service_soc33, per 1,000 employed aged 18–64** — ratio to US-born NH whites (SE)

| Group | men: per 1,000 (SE) | men: ratio raw | men: same ages | men: (a) age × educ | men: (b) full indirect | men: (b) full raked | women: per 1,000 (SE) | women: ratio raw | women: same ages | women: (a) age × educ | women: (b) full indirect | women: (b) full raked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 37.6 (0.7) | 1.16 (0.02) | 1.14 (0.02) | 1.14 (0.02) | 1.06 (0.03) | 1.05 (0.05) | 11.9 (0.4) | 1.49 (0.05) | 1.35 (0.05) | 1.28 (0.05) | 1.34 (0.06) | 1.17 (0.09) |
| US-born, Mexican ancestry | 38.2 (0.8) | 1.18 (0.03) | 1.16 (0.03) | 1.15 (0.03) | 1.06 (0.03) | 1.07 (0.07) | 12.2 (0.5) | 1.53 (0.06) | 1.39 (0.06) | 1.31 (0.06) | 1.38 (0.07) | 1.26 (0.12) |
| Mexico-born, all | 8.8 (0.3) | 0.27 (0.01) | 0.26 (0.01) | 0.39 (0.02) | 0.34 (0.02) | 0.33 (0.03) | 4.7 (0.4) | 0.59 (0.04) | 0.62 (0.05) | 0.60 (0.05) | 0.60 (0.05) | 0.48 (0.07) |
| Mexico-born, naturalized | 16.3 (0.8) | 0.50 (0.02) | 0.51 (0.02) | 0.64 (0.03) | 0.56 (0.03) | 0.47 (0.06) | 6.0 (0.6) | 0.75 (0.07) | 0.81 (0.08) | 0.77 (0.07) | 0.73 (0.07) | 0.57 (0.12) |
| Mexico-born, arrived before 18 | 14.5 (0.6) | 0.45 (0.02) | 0.43 (0.02) | 0.57 (0.02) | 0.50 (0.02) | 0.54 (0.07) | 6.6 (0.6) | 0.83 (0.07) | 0.83 (0.07) | 0.78 (0.07) | 0.81 (0.08) | 0.52 (0.10) |
| US-born, Asian Indian ancestry | 12.1 (2.3) | 0.37 (0.07) | 0.36 (0.07) | 0.42 (0.08) | 0.42 (0.08) | 0.45 (0.12) | 4.7 (1.0) | 0.59 (0.13) | 0.54 (0.12) | 0.62 (0.13) | 0.62 (0.13) | 0.80 (0.32) |
| US-born, Asian Indian race | 12.1 (1.7) | 0.37 (0.05) | 0.36 (0.05) | 0.41 (0.06) | 0.41 (0.06) | 0.39 (0.09) | 4.1 (0.7) | 0.51 (0.09) | 0.47 (0.08) | 0.53 (0.09) | 0.53 (0.09) | 1.01 (0.30) |
| India-born, all | 4.6 (0.5) | 0.14 (0.02) | 0.13 (0.01) | 0.16 (0.02) | 0.16 (0.02) | 0.27 (0.07) | 2.1 (0.5) | 0.26 (0.06) | 0.27 (0.06) | 0.32 (0.07) | 0.32 (0.07) | 0.28 (0.10) |
| India-born, naturalized | 5.9 (0.9) | 0.18 (0.03) | 0.18 (0.03) | 0.21 (0.03) | 0.20 (0.03) | 0.40 (0.12) | 3.3 (0.8) | 0.41 (0.11) | 0.44 (0.11) | 0.51 (0.13) | 0.49 (0.12) | 0.35 (0.10) |
| India-born, arrived before 18 | 9.0 (1.9) | 0.28 (0.06) | 0.27 (0.05) | 0.30 (0.06) | 0.29 (0.06) | 0.45 (0.17) | 3.2 (1.0) | 0.40 (0.13) | 0.39 (0.13) | 0.43 (0.14) | 0.43 (0.14) | 0.13 (0.05) |
| US-born non-Hispanic white | 32.4 (0.2) | 1.00 (0.00) |  |  |  |  | 8.0 (0.1) | 1.00 (0.00) |  |  |  |  |
| All US-born | 35.1 (0.2) | 1.08 (0.00) | 1.08 (0.00) | 1.07 (0.00) | 1.06 (0.00) | 1.05 (0.00) | 10.8 (0.1) | 1.35 (0.01) | 1.33 (0.01) | 1.31 (0.01) | 1.31 (0.01) | 1.25 (0.01) |
<!-- /part -->

<!-- part: protective_security_guards -->
**security_guard, per 1,000 employed aged 18–64** — ratio to US-born NH whites (SE)

| Group | men: per 1,000 (SE) | men: ratio raw | men: same ages | men: (a) age × educ | men: (b) full indirect | men: (b) full raked | women: per 1,000 (SE) | women: ratio raw | women: same ages | women: (a) age × educ | women: (b) full indirect | women: (b) full raked |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| US-born, Mexican Hispanic origin | 11.8 (0.4) | 2.07 (0.08) | 2.00 (0.08) | 1.74 (0.07) | 1.32 (0.07) | 1.29 (0.10) | 3.6 (0.2) | 2.13 (0.15) | 2.05 (0.15) | 1.66 (0.12) | 1.68 (0.14) | 1.19 (0.17) |
| US-born, Mexican ancestry | 12.2 (0.5) | 2.14 (0.09) | 2.05 (0.09) | 1.77 (0.08) | 1.34 (0.08) | 1.26 (0.14) | 3.8 (0.3) | 2.24 (0.19) | 2.15 (0.18) | 1.75 (0.15) | 1.80 (0.18) | 1.18 (0.20) |
| Mexico-born, all | 3.2 (0.2) | 0.57 (0.04) | 0.61 (0.04) | 0.57 (0.04) | 0.40 (0.04) | 0.39 (0.05) | 1.5 (0.2) | 0.91 (0.12) | 0.95 (0.12) | 0.65 (0.10) | 0.60 (0.11) | 0.57 (0.13) |
| Mexico-born, naturalized | 4.2 (0.4) | 0.74 (0.07) | 0.77 (0.07) | 0.75 (0.08) | 0.53 (0.06) | 0.53 (0.12) | 1.9 (0.3) | 1.11 (0.20) | 1.16 (0.21) | 0.86 (0.16) | 0.76 (0.16) | 0.67 (0.22) |
| Mexico-born, arrived before 18 | 5.3 (0.5) | 0.93 (0.08) | 0.97 (0.09) | 0.85 (0.08) | 0.61 (0.06) | 0.45 (0.07) | 2.2 (0.4) | 1.29 (0.21) | 1.34 (0.22) | 0.91 (0.16) | 0.87 (0.17) | 0.80 (0.27) |
| US-born, Asian Indian ancestry | 4.7 (1.2) | 0.82 (0.22) | 0.81 (0.22) | 1.34 (0.35) | 1.30 (0.35) | 1.32 (0.59) | 0.7 (0.5) | 0.39 (0.29) | 0.38 (0.29) | 0.62 (0.47) | 0.66 (0.50) | 0.14 (0.09) |
| US-born, Asian Indian race | 4.4 (1.0) | 0.77 (0.18) | 0.75 (0.17) | 1.16 (0.27) | 1.10 (0.27) | 0.93 (0.33) | 1.0 (0.4) | 0.61 (0.27) | 0.60 (0.26) | 0.90 (0.39) | 0.92 (0.41) | 2.40 (0.86) |
| India-born, all | 2.0 (0.3) | 0.35 (0.06) | 0.38 (0.07) | 0.65 (0.11) | 0.61 (0.11) | 0.58 (0.22) | 0.5 (0.1) | 0.29 (0.08) | 0.32 (0.09) | 0.52 (0.15) | 0.50 (0.14) | 0.51 (0.36) |
| India-born, naturalized | 2.4 (0.6) | 0.42 (0.10) | 0.46 (0.11) | 0.68 (0.16) | 0.64 (0.15) | 0.58 (0.23) | 0.8 (0.2) | 0.45 (0.14) | 0.48 (0.15) | 0.73 (0.23) | 0.69 (0.23) | 0.34 (0.16) |
| India-born, arrived before 18 | 3.3 (1.2) | 0.57 (0.21) | 0.57 (0.21) | 0.80 (0.29) | 0.73 (0.27) | 0.90 (0.50) | 0.9 (0.5) | 0.52 (0.27) | 0.53 (0.27) | 0.74 (0.38) | 0.76 (0.40) | 0.17 (0.12) |
| US-born non-Hispanic white | 5.7 (0.1) | 1.00 (0.00) |  |  |  |  | 1.7 (0.0) | 1.00 (0.00) |  |  |  |  |
| All US-born | 8.9 (0.1) | 1.56 (0.02) | 1.55 (0.02) | 1.51 (0.02) | 1.44 (0.02) | 1.38 (0.02) | 3.3 (0.1) | 1.93 (0.05) | 1.92 (0.05) | 1.83 (0.05) | 1.86 (0.05) | 1.63 (0.04) |
<!-- /part -->
