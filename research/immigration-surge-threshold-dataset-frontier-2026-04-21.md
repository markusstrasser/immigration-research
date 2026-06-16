# Immigration surge/threshold frontier: datasets and research design

**Question:** What datasets and research would actually settle the user's surge and threshold questions, rather than just restating older average-effect immigration papers?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The repo already concluded that the recent literature is better on surge realism than the old Card/Borjas frame, but still weak on explicit nonlinear thresholds. This note maps the concrete data stack needed to settle that gap. [SOURCE: research/immigration-recent-literature-surge-threshold-audit-2026-04-21.md] [SOURCE: research/immigration-causal-surge-2021-2024.md]

## Bottom line

1. **Yes, the needed datasets mostly exist.** A serious public-data panel can settle much more of the question than the current literature has settled. [INFERENCE]
2. **No, one dataset will not do it.** This requires a joined panel across labor, housing, homelessness/shelter, schools, arrivals, and politics. [INFERENCE]
3. **The biggest public-data gap is not wages.** It is **local arrival assignment** and **shelter-system saturation** at the city / CoC / county / district level. [INFERENCE]
4. **Hugging Face is not the frontier here.** I checked the Hub dataset surface and did not find high-value canonical repositories for the decisive U.S. admin sources; the useful assets for this question remain official Census, HUD, DHS, EOIR, NCES, BLS, and election sources. [DATA]
5. **The best immediate build is a county-month or metro-month panel from `2018–2026` with explicit nonlinear estimators** rather than another linear average-effect literature summary. [INFERENCE]

## What exactly needs to be settled?

The unresolved questions are not one thing. They split into five estimands:

1. `labor`: do natives in affected places see wage, employment, or per-capita-output losses during and after a surge?
2. `housing`: when do rents, overcrowding, shelter demand, and permit shortfalls become convex rather than linear?
3. `public systems`: when do schools, shelters, courts, and local budgets cross capacity thresholds?
4. `politics`: are there nonlinear backlash thresholds once inflows become visible and concentrated?
5. `migration accounting`: what was the actual local shock size by place and month?

Older papers mostly answered only (1), and usually on average. [SOURCE: research/immigration-recent-literature-surge-threshold-audit-2026-04-21.md]

## The minimum serious data stack

### 1) Local shock measurement

These datasets identify where and when the surge actually hit.

1. `CBP Southwest Land Border Encounters`
   - already partly staged in the causal stack. [SOURCE: sources/immigration-causal/data/cbp/swb_encounters_by_citizenship_monthly.parquet]
   - official source: [SOURCE: https://www.cbp.gov/document/stats/southwest-land-border-encounters]
   - value: national and nationality-specific timing of the border shock
   - limit: does **not** tell you final settlement location

2. `OHSS enforcement / annual immigration tables`
   - repo already has an OHSS workbook. [SOURCE: sources/immigration-causal/data/cbp/ohss_enforcement_nov2024.xlsx]
   - official source: [SOURCE: https://ohss.dhs.gov/]
   - value: broader enforcement and legal-process context
   - limit: weak on local destination assignment

3. `EOIR workload and adjudication statistics`
   - official source: [SOURCE: https://www.justice.gov/eoir/workload-and-adjudication-statistics]
   - value: local court-pressure proxy, judge backlog, asylum docket intensity
   - limit: court venue is not the same thing as residence

4. `Local receiver-city administrative counts`
   - repo already has a narrow receiver-city cost file. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv]
   - value: the closest thing to actual assigned local shock size for NYC, Chicago, Denver, Boston, etc.
   - limit: fragmented, city-specific, not national

**Verdict:** public shock measurement is good enough for national timing, but still weak on exact local assignment. That is the first problem to solve. [INFERENCE]

### 2) Labor-market outcomes

These datasets settle the “does local labor deteriorate?” side better than another abstract literature review.

1. `QWI`
   - repo already has a state panel and scripts. [SOURCE: sources/immigration-causal/data/lehd/qwi_state_panel.parquet] [SOURCE: sources/immigration-causal/scripts/pull_qwi_state_panel.py]
   - official API/docs: [SOURCE: https://api.census.gov/data/timeseries/qwi/se] [SOURCE: https://ledextract.ces.census.gov/static/data.html]
   - value: quarterly earnings and employment by industry × education × geography
   - limit: current repo pull is state-level; threshold work needs county or metro extension

2. `QCEW`
   - repo already has annual sector files. [SOURCE: research/immigration-dataset-register.md]
   - official source: [SOURCE: https://www.bls.gov/cew/data-overview.htm] [SOURCE: https://www.bls.gov/cew/downloadable-data-files.htm]
   - value: county-industry employment and wages, high coverage
   - limit: not immigrant-specific; average wage, not native-only wage

3. `LAUS`
   - official source: [SOURCE: https://www.bls.gov/lau/data-overview.htm]
   - value: county and metro unemployment / labor force monthly panel
   - limit: coarse labor-market outcome only

4. `ACS 1-year PUMS`
   - repo already has 2023. [SOURCE: research/immigration-dataset-register.md]
   - official source: [SOURCE: https://www.census.gov/programs-surveys/acs/microdata.html] [SOURCE: https://www.census.gov/programs-surveys/acs/microdata/documentation/2024.html]
   - value: nativity, education, occupation, rent, overcrowding, commuting, household composition
   - limit: PUMA geography only, not county; weaker for acute month-level shocks

**Verdict:** the labor side is very solvable with public data if we extend `QWI` below the state level and join it to actual surge exposure. [INFERENCE]

### 3) Housing and shelter capacity

This is where the threshold question becomes real.

1. `Building Permits Survey`
   - official source: [SOURCE: https://www.census.gov/construction/bps/index.html]
   - value: county / CBSA permit flow, the cleanest public supply-response margin
   - limit: permits are not completions, and they lag acute shelter pressure

2. `ACS rent / overcrowding / renter burden`
   - official source: [SOURCE: https://www.census.gov/programs-surveys/acs/microdata.html]
   - value: housing stress and crowding at PUMA resolution
   - limit: not monthly

3. `HUD AHAR / PIT / HIC`
   - official source: [SOURCE: https://www.huduser.gov/portal/datasets/ahar.html]
   - value: CoC-level homelessness and shelter-inventory measures since 2007
   - limit: annual, and public files are thinner than raw HMIS

4. `HMIS / LSA`
   - official standards/docs: [SOURCE: https://files.hudexchange.info/resources/documents/HMIS-Data-Standards.pdf] [SOURCE: https://files.hudexchange.info/resources/documents/LSA-Programming-Specifications-2023.pdf]
   - value: the closest thing to client-flow shelter saturation data
   - limit: hard to get in clean public nationwide form; often community-admin or restricted

5. `AHS / HADS / CHAS`
   - official source: [SOURCE: https://www.huduser.gov/portal/datasets/ahs.html] [SOURCE: https://www.huduser.gov/portal/datasets/hads/hads.html] [SOURCE: https://www.huduser.gov/portal/datasets/cp.html]
   - value: deeper affordability and housing-condition context
   - limit: weak for acute surge timing

**Verdict:** a public `AHAR/PIT/HIC + BPS + ACS` stack gets close, but a real shelter-threshold answer improves a lot if local `HMIS/LSA` extracts can be acquired. [INFERENCE]

### 4) School and local public-service capacity

1. `Census Annual Survey of School System Finances`
   - official source: [SOURCE: https://www.census.gov/programs-surveys/school-finances/data.html]
   - repo already stages school-finance assets. [SOURCE: research/immigration-dataset-register.md]
   - value: district finance, spending, revenue, debt
   - limit: finance only, not directly immigrant-serving load

2. `SAIPE school district files`
   - already staged locally. [SOURCE: research/immigration-frontier-data-acquisition-2026-04-11.md]
   - value: district child-count and poverty overlays
   - limit: not immigrant-specific

3. `NCES CCD`
   - official source: [SOURCE: https://nces.ed.gov/ccd/]
   - repo already staged current LEA file-tool artifacts. [SOURCE: research/immigration-frontier-data-acquisition-2026-04-11.md]
   - value: district directory, enrollment, staffing, membership
   - limit: current direct public route to district-level `EL` counts remains partially unresolved in the repo

4. `EDFacts / Title III / ELSi`
   - needed for English-learner load if available through a stable current route
   - limit: this was already flagged as an unresolved acquisition path / HTML trap in the repo. [SOURCE: research/immigration-frontier-data-acquisition-2026-04-11.md]

**Verdict:** the district capacity panel is feasible now for finance and child load, but still incomplete without a better current `EL` route. [INFERENCE]

### 5) Political backlash

1. `MIT Election Lab county returns`
   - official source: [SOURCE: https://electionlab.mit.edu/data]
   - value: county presidential returns through 2024
   - limit: county outcome only; not enough by itself

2. `ACS / county demographics`
   - value: immigrant stock, education, tenure, urbanicity, baseline composition
   - limit: repeated cross-sections

3. `Receiver-city / bus-routing / local arrival data`
   - value: visible exposure intensity
   - limit: fragmented and partly hand-built

**Verdict:** the politics question is very tractable once the local-shock panel is improved. [INFERENCE]

## What should actually be acquired next?

If the goal is to settle the threshold question rather than just expand the warehouse, the top public acquisitions are:

1. `county or metro QWI extension`
   - why: current repo result is state-level and averages away within-state threshold dynamics
   - source: [SOURCE: https://api.census.gov/data/timeseries/qwi/se]

2. `BPS county / CBSA annual and monthly panels`
   - why: needed to measure whether housing supply response differs sharply once inflows rise
   - source: [SOURCE: https://www.census.gov/construction/bps/index.html]

3. `HUD AHAR PIT/HIC CoC panel`
   - why: the cleanest public shelter-capacity series
   - source: [SOURCE: https://www.huduser.gov/portal/datasets/ahar.html]

4. `EOIR local workload panel`
   - why: local court / asylum-system pressure is part of the actual destination burden
   - source: [SOURCE: https://www.justice.gov/eoir/workload-and-adjudication-statistics]

5. `MIT Election Lab county returns 2000–2024`
   - why: needed for backlash-threshold estimation
   - source: [SOURCE: https://electionlab.mit.edu/data]

6. `current NCES district EL path`
   - why: school-load threshold estimation is incomplete without it
   - source family: [SOURCE: https://nces.ed.gov/ccd/]

7. `ACS 2024 PUMS`
   - why: gets the repo past the pre-surge composition ceiling
   - source: [SOURCE: https://www.census.gov/programs-surveys/acs/microdata/documentation/2024.html]

## What research design would settle the question?

### Design A — county/month or metro/month stacked event study

Build a panel `2018–2026` with:

1. treatment = surge exposure intensity by place-month
2. outcomes = wages, employment, unemployment, rents, permits, homelessness, school load, vote swing
3. controls = baseline housing elasticity, prior immigrant share, pretrend labor conditions

This settles:

1. whether the surge was actually different from normal variation
2. whether effects are temporary or persistent
3. whether exposed places diverged before the surge

### Design B — explicit nonlinear threshold model

Estimate:

1. spline models
2. threshold regressions
3. bin-scatter / local-projection event studies by exposure decile
4. interactions with housing elasticity and baseline vacancy

The threshold variable should not only be `foreign-born share`.

It should also include:

1. `new arrivals / existing population`
2. `new arrivals / renter households`
3. `new arrivals / shelter inventory`
4. `new arrivals / school-age population`

That is closer to the user's actual question than “county went from 6% to 10% foreign-born.” [INFERENCE]

### Design C — receiver-city synthetic controls

Run synthetic controls for:

1. NYC
2. Chicago
3. Denver
4. Boston / Massachusetts
5. selected Texas border metros

with outcomes:

1. homelessness / shelter occupancy
2. rent growth
3. permits and completions
4. school service load
5. local budget stress
6. political shift

This directly tests whether a few visible surge destinations crossed convex cost thresholds.

### Design D — school-service panel

District-year panel with:

1. finance
2. total enrollment
3. English learner load
4. poverty / child counts
5. local surge exposure

This would settle whether school burden is linear, absorbable, or thresholded.

## What would still remain unresolved?

Even after this build, two things would still be hard:

1. exact undocumented / asylum assignment to final residence at national scale
2. full shelter-system microflows without local HMIS cooperation

So the honest answer is:

1. **public data can settle a lot more than the literature currently has**
2. **the last 20% requires local HMIS / administrative cooperation or city-specific deep dives**

## Recommended execution order

1. extend `QWI` to county or metro
2. stage `BPS`
3. stage `AHAR PIT/HIC`
4. build `2018–2026` county / metro panel
5. estimate explicit nonlinear threshold models
6. only then decide whether the threshold story is real, weak, or mainly a receiver-city phenomenon

## Blunt answer

`Can we find datasets and research that would settle these questions?`

Yes.

But the answer is not “find one more immigration paper.”

It is:

1. build a multi-system panel
2. use explicit nonlinear estimators
3. stop asking average-effect papers to answer a capacity-threshold question
