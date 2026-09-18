# Native Employment at Labor-Market Entry and Low-Skill Immigration — US Metro Replication

Model self-report: `claude-opus-5[1m]` (verbatim from the environment-info block).

**Verdict:** PROBE IN PROGRESS [UNVERIFIED] — data build running, estimates not yet computed.

Purpose: replicate on US data the estimand that Jaeger, Ruist & Stuhler (2018) and Dustmann,
Schönberg & Stuhler (2017) identify as the durable margin of low-skill immigration — native
employment at labor-market entry — and test whether the JRS multiple-instrumentation correction
moves the short-run coefficient.

## Status log

- 2026-09-18 — [UNVERIFIED] data build started. Crosswalks fetched, ACS PUMS pull in flight.
- 2026-09-18 — [VERIFIED from primary text] two corrections to the brief's framing, recorded
  before estimates exist so they are not read back as post-hoc. (i) The employment-entry result
  is **Dustmann–Schönberg–Stuhler's**, not JRS's; JRS's own corrected estimates are for **wages**
  (a 1% inflow reduces average wages by about 0.7 log points, "substantially more negative" than
  the conventional IV). (ii) JRS report their own correction is underidentified outside the 1970s,
  which is the period this panel sits outside of.

---

## 1. The data the brief assumed does not exist, and what replaced it

The dispatch brief specified the local IPUMS panel
(`$DERIVED_ROOT/immigration_microdata.duckdb`, table `ipums_usa_borjas_panel`) as the source,
described as holding "ACS 1-year 2005–2023 and Census 2000/1990 samples with `MET2013` or
`PUMA`/`CZ` geography and person weights." **That description is wrong on three counts**, verified
by reading the table directly (44,393,133 rows):

| Brief assumed | Panel actually has |
|---|---|
| ACS 1-year 2005–2023 | Five samples only: 1980, 1990, 2000 (5% census), 2010, 2023 (ACS) |
| `MET2013` or `PUMA`/`CZ` geography | `STATEFIP` only — no sub-state geography of any kind |
| sex-specific analysis possible | no `SEX` variable in the extract |

[SOURCE: `describe ipums_usa_borjas_panel`, run 2026-09-18; columns are YEAR SAMPLE SERIAL
CBSERIAL HHWT CLUSTER STATEFIP STRATA GQ PERNUM PERWT AGE RACE RACED BPL BPLD CITIZEN YRIMMIG
EDUC EDUCD EMPSTAT EMPSTATD WKSWORK1 INCTOT]

The project memory file the brief pointed to already records the sample list and the "all-sex"
caveat, so the gap is between the brief and the memory, not inside the memory. The panel was
therefore **not used**, and **not modified**.

Replacement source: the **Census Bureau ACS 1-year PUMS API** (`api.census.gov/data/{year}/acs/acs1/pums`),
pulled fresh. The 2020 ACS 1-year standard release was cancelled, so the API has no 2020 1-year
PUMS and that year cannot appear in any panel.
[SOURCE: HTTP 404 on `api.census.gov/data/2020/acs/acs1/pums`, probed 2026-09-18]

**Years pulled: 2005, 2008, 2010, 2013, 2015, 2018, 2023 — the window endpoints only, not an
annual panel.** The link to the Census servers sustained roughly 90–200 KB/s during the build
and reset large responses mid-transfer, which made a full 18-year national pull impractical
inside this run. Every 5-year and 10-year difference in the design ends on one of these seven
years, so the estimates are unaffected; what is lost is the ability to inspect year-by-year
paths between endpoints, and the option of alternative window definitions without a further
pull. The bulk PUMS zip releases were checked as an alternative and rejected: at roughly 600 MB
per year they are far worse over this link.

Selection is pushed onto the server for the same reason — the outcome call requests only
natives below a bachelor's aged 16–29, and the treatment call only the foreign-born aged 18–64 —
and the 18–64 denominator comes from the published PUMA-level table B01001 rather than from
microdata. The reduced pull was verified to reproduce the unfiltered pull's cell counts exactly
on a test state-year before it was adopted (Rhode Island 2015, every field identical).

## 2. Design

**Unit.** Metropolitan statistical area × year. ACS PUMS carries no metro code in any vintage
(verified: no MSA/CBSA/METRO-named variable in the 2007 or 2023 variable dictionaries), so metros
are constructed. Chain:

```
PUMA (vintage in force that year)  --Geocorr population allocation factors-->  county
county  --OMB February-2013 delineation, metropolitan areas only-->  CBSA
```

The county→CBSA step uses **one fixed delineation for every year**, which is what makes the metro
boundaries stable across the three PUMA vintages the ACS uses (2000-definition PUMAs for
2005–2011, 2010-definition for 2012–2021, 2020-definition for 2022–2023). A person's weight is
split across counties by the Geocorr allocation factor, then summed into the fixed CBSA. Metros are
metropolitan statistical areas only; micropolitan areas and non-metro counties are dropped.
[SOURCE: MCDC Geocorr 2014 and 2022, `mcdc.missouri.edu/cgi-bin/broker`; OMB delineation
`www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2013/delineation-files/list1.xls`]

**Outcomes.** Native-born (`NATIVITY == 1`), below bachelor's degree, employment-to-population
ratio and labour-force participation, in percentage points.

- Education code: `SCHL <= 12` for 2005–2007 (17-code scheme, bachelor's = 13) and `SCHL <= 20`
  for 2008 onward (25-code scheme, bachelor's = 21). The recode break at 2008 is real and is
  handled per year. [SOURCE: `acs1/pums/variables.json` for 2005, 2007, 2008, fetched 2026-09-18]
- Employed: `ESR` in {1, 2, 4, 5} (includes armed forces). Civilian-only {1, 2} stored alongside.
- In labour force: `ESR` in {1, 2, 3, 4, 5}.
- Age bands: 18–29 separately for men and women, and a pooled 16–24 arm.
- Institutional group quarters (`TYPE`/`TYPEHUGQ == 2`) excluded from every numerator and
  denominator, so prison populations do not enter the entry-age denominator.

**Treatment.** Change in the Mexico-born (`POBP == 303`) share of the metro population aged 18–64,
in percentage points; and the same for all foreign-born (`NATIVITY == 2`).

**Instruments.** Past-settlement shift-share. The base share is metro *m*'s share of the **national
Mexico-born (or foreign-born) stock in Census 2000**, built from SF3 table PCT019 at county level
and aggregated into the same fixed 2013 CBSAs (PCT019103 = born in Mexico; national total
9,180,186, which matches the published Census 2000 figure). Predicted inflow over a window is
that base share times the national change in the stock over the window, divided by the metro's
base-year population aged 18–64.
[SOURCE: `api.census.gov/data/2000/dec/sf3`, group PCT019, fetched 2026-09-18]

**Estimators.** For each outcome × sex × treatment × window:

- **OLS** in long differences, 5-year and 10-year.
- **IV**, the conventional single shift-share instrument.
- **IV-JRS**, the Jaeger–Ruist–Stuhler correction: the current *and* the previous window's
  immigration change both enter as endogenous regressors, instrumented by the current and lagged
  predicted inflows. The reported coefficient is the one on the current change. This is the test
  of whether the conventional estimate is contaminated by ongoing adjustment to earlier shocks.

  This arm requires a **multi-origin** instrument and cannot be run with a single origin group.
  With one group the current and lagged predicted inflows are both the same metro base share
  times a national scalar, so they are collinear across metros and the two-endogenous system is
  not identified. The identifying variation JRS exploit is the change in the *national origin
  mix*. The instrument here is therefore built from all 100 leaf birthplace categories of Census
  2000 SF3 table PCT019, each metro's base share of the national 2000 stock of that origin
  interacted with that origin's national stock change over the window, summed across origins.
  [SOURCE: JRS 2018 p.17ff, "multiple instrumentation", NBER w24285 full text]

  **JRS themselves report that this procedure is underidentified in every US decade after the
  1970s.** Verbatim: "only in the 1970s do we reject the null hypothesis of underidentification
  with the Kleinbergen-Paap statistic. The rest of our analysis is therefore focused on
  estimating the impact of immigration" in that decade, and they note that "looking at the first
  stage regressions individually would not necessarily lead one to conclude that there are
  identification problems in the 1990s and 2000s, as the first stage F statistics are reasonably
  large." [SOURCE: NBER w24285 full text, fetched 2026-09-18] The sample here is 2005–2023,
  squarely inside the region where they found the correction fails. Every IV row therefore
  reports **Shea's partial R-squared** alongside the first-stage F, because Shea's measure is the
  one that collapses when two instruments are near-collinear while individual F statistics stay
  large. A large F with a near-zero Shea R-squared in the JRS arm is the signature of the
  failure JRS describe, not evidence of a well-identified estimate.
- **IV-placebo**, the current instrument against the outcome change in the window *before* the
  shock.

Weights: the metro's base-year native no-college population in the relevant age band.
Standard errors: heteroskedasticity-robust, clustered by metro. Metros below 25,000 weighted
native no-college persons in the base year are dropped.

### The shift half of the shift-share nearly vanishes for Mexico in this period

Measured from ACS table B05006 at the national level, the Mexico-born stock changes over the
estimation windows as follows, against the change in the stock of all origins matched to the
Census 2000 base.

| window | Mexico-born national change | all matched origins |
|---|---:|---:|
| 2005–2010 | +0.74 M | +4.20 M |
| 2008–2013 | +0.17 M | +3.23 M |
| 2010–2015 | −0.07 M | +3.25 M |
| 2013–2018 | −0.41 M | +3.40 M |

[SOURCE: `api.census.gov` ACS 1-year table B05006, US total, fetched 2026-09-18]

A shift-share instrument is a metro base share multiplied by a national shift. When the
national shift is −0.07 million, the predicted inflow is near zero for every metro and the
instrument has almost nothing left to explain. **The conventional single-origin Mexican
instrument is therefore close to powerless over most of 2005–2023 by construction, not by bad
luck.** This is a different problem from the one JRS identify, and it compounds it: their
critique is that the instrument conflates short- and long-run responses, while here the shift it
depends on has gone to zero and then reversed sign. The multi-origin instrument keeps its power
because the other origins continued to grow by roughly 3 million per window throughout.

## 3. Estimates

[UNVERIFIED] — pending. Will be written to `derived/estimates.csv`.

### Benchmarks, in this memo's units

Both comparison papers report effects in units that are not percentage points of an
employment-to-population rate, so the conversion is stated here before any estimate exists.

**Dustmann–Schönberg–Stuhler (2017).** Verbatim from the paper: "By 1993, a 1 percentage point
increase in the inflow of Czech workers relative to employment in the baseline has led to about
a 0.13 percent decrease in native wages, a 0.93 percent decrease in native local employment, and
a 0.07 (1-0.93) percent increase in total (including Czech) local employment." Their Table IV
reports −0.926 for all natives and **−1.371 for unskilled natives**, the closest group to the
population studied here. [SOURCE: IZA DP 10114 full text, fetched 2026-09-18; the published
version is QJE 132(1)]

Their −0.93 is a percent change in the native employment *count*. A native employment-to-population
ratio near 65% converts it to roughly **−0.6 percentage points** of E/POP per 1-point rise in the
immigrant share, and the unskilled −1.37 to roughly **−0.9 points**. The conversion holds the
native population fixed, which is exactly the margin DSS show is not fixed, so treat it as an
order-of-magnitude target rather than a like-for-like number. The useful question for this memo
is whether the confidence intervals here are tight enough to *exclude* an effect that size.

**Card (2001).** Verbatim: "The results imply that immigrant inflows over the 1980s reduced wages
and employment rates of low-skilled natives in traditional gateway cities like Miami and Los
Angeles by 1–3 percentage points." [SOURCE: 10.1086/209979, verified against the publisher page
2026-09-18] That is a *total* effect over a decade in the highest-inflow cities, not a
per-point coefficient, so the comparison runs the other way: multiply the coefficient estimated
here by the decade-long share change actually observed in a gateway metro.

## 4. What this design does and does not identify

**Does not identify legal status.** ACS records birthplace and citizenship, not authorisation.
The Mexico-born treatment mixes naturalised citizens, lawful permanent residents, temporary
visa holders and unauthorised residents. No arm here speaks to any policy that distinguishes
them.

**Does not identify person-level displacement.** The unit is the metro. A negative coefficient
is consistent with a native losing a job to an immigrant, with a native never being hired, and
with a native leaving the metro. Dustmann–Schönberg–Stuhler could separate these because they
had linked employment records; ACS cross-sections cannot. The native-outflow channel is the
live alternative here: Card (2001) reports native mobility is insensitive to inflows, Borjas
(2006) reports 40–60% offset, and the repo rates the Borjas direction as granted but the
magnitude as specification-sensitive. If natives do move, the surviving denominator is selected
and the coefficient is biased toward zero.

**Does not identify wages.** The ACS wage variables were not pulled. JRS's own corrected
estimates are wage estimates, so the closest quantitative comparison in this memo is to DSS's
employment result, not to JRS's headline.

**ACS, not CPS or administrative data.** The employment measure is the ACS `ESR` recode from a
single annual cross-section, not a monthly labour-force series and not an employer record.
Metro cells for smaller areas rest on a few hundred unweighted observations, which is why the
main specification imposes a base-year population floor and weights by native population.

**Metro-year shares are measured with sampling error**, in both endpoints of every long
difference. That is classical measurement error in the regressor, so OLS is attenuated by
construction and the IV estimates should be larger in absolute value than OLS for that reason
alone, independent of any endogeneity argument. An IV/OLS gap is therefore not by itself
evidence that sorting was biasing OLS upward.

**Metro boundaries are constructed, not observed.** PUMAs are allocated to counties by
population factors, so a PUMA straddling a metro edge has its residents split. This attenuates
the treatment toward the national mean for metros with ragged boundaries.

## 5. Disconfirmation

Six tests, all specified before the estimates were read.

1. **Pre-window placebo.** The instrument for window (t, t+5) is run against the outcome change
   over (t−5, t). A significant coefficient means the instrument tracks pre-existing local
   trends rather than the shock.
2. **College-educated control group.** Native 18–29 year olds with a bachelor's degree or above
   share the local demand shock but compete far less directly with low-skill immigrants. If the
   instrument moves their employment rate as much as it moves the no-college rate, the design is
   measuring metro demand, not skill-specific competition. This required a separate ACS pull.
3. **Identification strength.** Every IV row carries the first-stage F and Shea's partial
   R-squared. JRS's own finding is that their correction is underidentified in the US after the
   1970s while individual first-stage F statistics still look large, so a large F alone is not
   evidence of a usable estimate.
4. **Sign stability across windows.** A causal parameter should not flip sign between adjacent
   five-year windows. Window-by-window estimates are reported rather than only the pooled ones.
5. **Mexico-born versus all foreign-born.** All-foreign-born mixes high-skill inflows that
   follow local labour demand. If the two arms disagree in sign, the foreign-born arm is the more
   likely to be capturing demand.
6. **Can the data even detect the benchmark effect?** Each headline confidence interval is
   compared against the DSS-equivalent magnitude of roughly −0.6 points (−0.9 for unskilled).
   A confidence interval that contains both zero and the benchmark rules out nothing, and must
   be reported as uninformative rather than as a null.

## 6. Byproduct

The build produces `derived/metro_year_panel.csv`, a metro × year panel of foreign-born and
Mexico-born population shares for 2005–2019 and 2021–2023 on fixed 2013 CBSA boundaries. The
repo's MSA rent-elasticity memo records its causal result as GATED on exactly this series
("needs metro foreign-born share over" time, with only 2023 staged). This panel closes that
input. [SOURCE: `research/immigration-msa-rent-elasticity-panel-2026-06-25.md` §What's built vs
gated]

## 7. Sources

- Jaeger, D., Ruist, J. & Stuhler, J. (2018), *Shift-Share Instruments and the Impact of
  Immigration*, NBER Working Paper 24285.
- Dustmann, C., Schönberg, U. & Stuhler, J. (2017), *Labor Supply Shocks, Native Wages, and the
  Adjustment of Local Employment*, QJE 132(1).
- Card, D. (2001), *Immigrant Inflows, Native Outflows, and the Local Labor Market Impacts of
  Higher Immigration*, JOLE 19(1). doi:10.1086/209979.
- US Census Bureau, American Community Survey 1-year PUMS, 2005–2019 and 2021–2023, via the
  Census Data API.
- US Census Bureau, Census 2000 Summary File 3, table PCT019, county level, via the Census Data API.
- Missouri Census Data Center, Geocorr 2014 and Geocorr 2022, PUMA→county allocation factors.
- US Office of Management and Budget, February 2013 metropolitan area delineation (list1).
- Repo: `research/immigration-canon-citation-audit-2026-09-17.md` §P1, §C7, §C8.

## 8. Analysis code

`infra/immigration-fiscal/employment_entry_2026_09_18/` — `fetch_crosswalks.py`, `pull_pums.py`,
`build_panel.py`, `estimate.py`, with the verbatim dispatch brief in `BRIEF.md`.
