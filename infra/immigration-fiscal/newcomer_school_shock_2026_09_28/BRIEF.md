# Lane brief: schools after a credible population shock, the 2022–2024 newcomer surge

Date 2026-09-28, 03:40 JST. Parent session immigration-research-1c. Follows the validation memo
(`research/immigration-validation-and-backtesting-2026-09-28.md` §3, "What is still open": "district spending,
capacity and achievement following a credible population shock").

## Why this episode

- In 2022–2024 New York City, Chicago and Denver schools absorbed tens of thousands of newly arrived students
  within two school years. The arrivals were routed by shelter placement, not by where families chose to live.
- That gives a sharp, dated inflow with school-level data before and after. It tests the school line's two
  open questions:
  - do spending and staffing follow pupils up, and how fast;
  - what happens to the achievement of other students in receiving schools.

## Read first

- `school_systemwide_2026_09_27/`, owned by another worker: its design table and NAEP panel. Do not duplicate
  its system-level tests; this lane is school- and district-level.
- `migrant_shelter_costs_2026_09_23/`: the shelter cost lane, for the placement data.
- `validation_schools_2026_09_28/RESULT.md`: the district finance back-test.

## Tasks

1. **Exposure.** Newcomer or new-ELL counts by school and year, 2019–20 to 2024–25, for NYC (NYSED report
   cards, NYC DOE demographic snapshots, NYC's newcomer/"Project Open Arms" counts) and for Chicago and Denver
   where available.
2. **Resources.** School-level per-pupil expenditure (the ESSA school-level reports), teacher FTE, class size
   and any mid-year budget adjustments by year. Test whether receiving schools' spending and staff rose with
   their pupils, and with what lag.
3. **Achievement of other students.** Grade 3–8 state test results for never-ELL or non-ELL students by school
   and year. Use a school fixed-effects design on exposure, with pre-trends from 2018–19 (the tests were not
   given in 2019–20).
   - Report points or SD per 10 percentage points of newcomer share, with SEs clustered by school.
   - Report the pre-trend coefficients.
4. **What it identifies.** Say what this design identifies: local exposure within a district. Say what it
   cannot: district-wide effects such as budget reallocation.

## Rules

- A new lane in this directory. Scripts write to `derived/`; raw pulls go in `_cache/`. Two runs must be
  byte-identical.
- Quote every source in `reads/`; tag every number. Direct HTTP with a generic User-Agent; Exa for search.
- Check download sizes first, and stop and report above 10 GB.
- Write `RESULT.md` first with `**Verdict:** pending`, and append after each task. No commits, staging or stash.
- Final message: the RESULT path and at most ten lines.
