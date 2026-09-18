---

## 2. Data and designs

Everything below is built in `infra/immigration-fiscal/school_flight_2026_09_18/`; scripts
are listed in the RESULT file with runnable commands.

**(a) Metro panel of child school type.** ACS 1-year PUMS, children aged 5–17, one cell
per PUMA × race/ethnicity × nativity × school level, for 2005, 2008, 2010, 2015 and 2023
(`pull_kids.py`). The 2013 and 2018 waves were dropped mid-run for throughput; the
remaining five span the whole window and every long difference used below ends on one of
them. PUMA counts are allocated to counties by the MCDC Geocorr
population allocation factor for the PUMA vintage in force that year and summed into the
fixed OMB February-2013 metropolitan delineation — the same geography construction as
`employment_entry_2026_09_18/build_panel.py`, whose crosswalk files are reused
(`build_metro.py`). The outcome is the private share among US-born non-Hispanic white
children, private / (private + public).

The treatment is the Hispanic (or foreign-born) share of **all enrolled children**, public
and private together, not of public enrolment. This matters. If white families leave the
public schools, the Hispanic share *of public enrolment* rises mechanically, so regressing
the white private share on it builds in a positive coefficient by construction. Betts &
Fairlie use the immigrant share of the public-school population and handle this through
their first-differenced structure; the all-enrolled denominator used here removes the
mechanical channel directly, at the cost of not being the identical object.

Two measurement caveats, both material:

- ACS `SCH` = 3 is "private school, private college, **or home school**." The private
  share therefore includes home-schooled children and rises mechanically with the growth
  of home schooling, which accelerated sharply after 2020. Comparisons that straddle 2020
  are contaminated by this and are labelled where they appear.
- Nativity is the *child's*, not the parents'. "US-born non-Hispanic white" is a proxy for
  Betts & Fairlie's "native"; it is close, because almost all non-Hispanic white children
  are US-born, but it is not identical to their definition.

**(b) District finance panel.** NCES Common Core of Data district membership by race,
the CCD directory (county, CBSA, English-learner counts), and the Census F-33 district
finance file, for 2000, 2005, 2010 and 2019, pulled district-by-state-by-year from the
Urban Institute Education Data Portal (`pull_districts.py`, `build_districts.py`). The
last wave is 2019 rather than 2020 because Urban's CCD enrolment year 2020 is the autumn
of 2020, when enrolment fell sharply for pandemic reasons unrelated to anything here.
Per-pupil denominators use the F-33's own membership count for the finance year, not the
CCD count, because the two are offset by a school year; CCD counts are used only for the
race shares, where the offset is immaterial.
The F-33 is the same source the repo reads locally for FY2024 in
`ledger_absolute_2026_09_17/district_differential.py`; Urban is used only because the
panel needs 2000–2020 and only the FY2024 file is staged locally. Urban's F-33
redistribution stops at 2020 — 2021 and later return zero rows, checked 2026-09-18, so
the panel cannot be carried to the FY2024 file the repo holds locally.
Money is deflated to 2020 dollars with the FRED CPI-U annual average. Screens: regular
operating districts, non-charter, at least 100 pupils, per-pupil current spending inside
$3,000–$80,000, the same plausibility band the repo's FY2024 loader uses. County elderly
share and median household income come from Census 2000 SF1 and the ACS 5-year
(`pull_county_controls.py`) for the Poterba-style control.

**(c) California ballot measures.** Every school-district bond and parcel-tax measure in
the California Elections Data Archive, the Secretary of State / CSU Sacramento joint
archive, taken from the `justindbk/ceda` mirror of the CSUS portal (`ceda_bonds.py`).
The outcome is the yes vote share, which is threshold-independent, plus a pass indicator
with the required-majority category as a control — Proposition 39 (November 2000) cut the
school-bond threshold from two-thirds to 55%, so a raw pass rate is not comparable across
that date. Districts are matched from the ballot-measure place name to the CCD district
name; the match rate is reported and unmatched measures are listed.

**What the repo already had.** `school_angle_2026_09_16` found no measured cost to
incumbent students from immigrant or English-learner concentration in US data, and priced
the classroom channel at $0 per pupil-year. `ledger_absolute_2026_09_17` found that
Hispanic pupils attend districts spending **$474 per pupil above** their state's mean
while white pupils attend districts **$624 below** it. That cross-sectional fact is the
first warning against expecting spending to fall with the Hispanic share: in levels, it
is higher.

