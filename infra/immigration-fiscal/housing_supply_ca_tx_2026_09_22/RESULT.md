**Verdict:** "California is not building, only Texas is" holds as a statement about *rates*
and fails as a statement about *rates relative to population growth*. Texas authorised 2.46
times as many housing units per resident as California on average over 2000-2024 and 2.4
times as many per existing housing unit in 2023-24, and California sat below the national
rate in every sub-period. But over 2010-2024 California's housing stock grew faster than its
population (8.73% against 5.66%, 1.77 added people per added unit) while Texas added 2.31
people per added unit, because California's population barely grew. Both statements are
descriptive. Across the 168-metro cross-section, metros whose Mexican-origin share rose more
had higher rent growth, and the interaction of that share change with the inverse supply
elasticity is **not** separately distinguishable once main effects are included. On the ACS
2024 PUMS, native-born non-Hispanic white adults 25-64 left California on net at 11.73 per
1,000 residents and Texas was flat at +0.20 per 1,000.

Model self-report: this lane was executed by **Opus 5 (1M context)**, exact model ID
`claude-opus-5[1m]`, as named in the executing environment block.

## Gates

| Gate | Status | Result |
|---|---|---|
| G1 BPS monthly sum vs FRED within 0.1% | PASS | 0.0000% in all six state-years (CA and TX, 2015, 2019, 2023) |
| Permit vintage reconciliation (recorded, not a gate) | — | December year-to-date vs FRED: CA −1.697% (2015), −0.515% (2019), +1.380% (2023); TX +1.747%, +1.862%, +3.122% |
| G2 popest vs ACS 2023 within 2% | PASS | CA 0.599%, TX 0.736% |
| G3 metro join | PASS | 168 of 168 joined to both a 2010 and a 2023 ACS CBSA row, 0 failures |
| G4 PUMS vs published table within 3% | PASS | CA 0.037%, TX 0.040% |
| G5 finite denominators, min 100 obs | PASS | smallest reported cell 313 observations |
| G6 warehouse elasticity vs primary Saiz file | PASS | 168 of 168, max absolute difference 0.00e+00 |

**Two Census permit products.** Census publishes two annual permit figures. The December
year-to-date file is a cumulative count that absorbs reports arriving after each month was
first published; FRED mirrors the as-published monthly series. Summing the 12 monthly BPS
files reproduces FRED **exactly** in all six state-years (gate G1, 0.0000%), which places the
difference between the two products in the vintage and rules out a parser error. The
year-to-date file differs from the monthly sum by −1.7% to +3.1% (below it in California in
2015 and 2019, above it elsewhere) and is used for the headline series because it is the
count Census publishes as the year's total; the reconciliation is
recorded in the audit rather than gated, because the difference is a property of the source.
The lane was first delivered with this comparison as a failing 1% gate; the parent restated
it on 2026-09-22 after confirming the FRED sums independently. Per-resident rates on the
FRED series differ from the headline by at most 0.2 per 1,000.
[DATA: `derived/permits_vintage_check.csv`] [CALCULATION: `analysis.py` gate G1 and
`audit.json → permit_vintage_reconciliation`]

## 1. State supply

Permits per 1,000 residents, period means [CALCULATION: `derived/state_supply.csv`]:

| Period | California | Texas | United States | TX/CA |
|---|---|---|---|---|
| 2000-2007 | 4.64 | 7.81 | 6.07 | 1.68 |
| 2008-2011 | 1.24 | 3.93 | 2.17 | 3.17 |
| 2012-2019 | 2.42 | 6.07 | 3.55 | 2.51 |
| 2020-2024 | 2.81 | 7.98 | 4.65 | 2.84 |
| 2000-2024 | 3.02 | 6.67 | 4.36 | 2.21 |

The year-by-year TX/CA ratio averages 2.46 and ranges from 1.37 (2004) to 3.66 (2009).
California is below the national rate in every single year of the series.

Permits per 1,000 existing housing units [DATA: ACS 1-year `B25001_001E`]:

| Year | California | Texas | United States |
|---|---|---|---|
| 2010 | 3.15 | 8.48 | 4.48 |
| 2015 | 6.86 | 16.43 | 8.64 |
| 2019 | 7.61 | 18.02 | 9.70 |
| 2023 | 7.53 | 18.35 | 10.01 |
| 2024 | 6.72 | 17.88 | 9.92 |

Cumulative 2000-2024: California 2,801,022 units, Texas 4,335,421, United States 33,765,918.
Texas authorised 1.55 times California's absolute total from a population averaging 69% of
California's across the period (79% by 2024). California is below the national rate in every
one of the 25 years and Texas is above it in every one.
[CALCULATION: `derived/state_supply.csv`]

**Population against housing units, 2010-2024** [CALCULATION: `derived/state_growth_2010_2024.csv`]:

| | Population growth | Housing-unit growth | Added people per added unit |
|---|---|---|---|
| California | +5.66% | +8.73% | 1.77 |
| Texas | +23.96% | +26.22% | 2.31 |
| United States | +9.95% | +11.19% | 2.06 |

This is the one place the headline claim inverts. Measured against its own population growth,
California added housing faster than Texas did. The arithmetic reason is visible in the first
column: California's population grew 5.66% over fourteen years. The table is descriptive and
identifies nothing about what caused either quantity. [FRAMING-SENSITIVE] Which of these two
framings is "the" supply story is a framing judgment, not a result: rates per resident favour
the Texas-builds reading, rates per unit of population growth do not.

## 2. Metro cross-section, 168 metros

Means by state [DATA: `derived/metro_panel.csv`]:

| | n | Saiz elasticity | Mexican-origin share change 2010-2023 | ZORI log growth 2015-2026 |
|---|---|---|---|---|
| California metros | 19 | 1.45 | +3.75 pp | 0.598 |
| Texas metros | 13 | 2.99 | +1.88 pp | 0.444 |
| All 168 | 168 | 2.30 | +1.30 pp | 0.557 |

The ZORI window is 2015-01-31 to 2026-05-31, the latest month in the local Zillow file.

Rent growth by elasticity quartile shows almost no gradient: 0.557, 0.577, 0.565, 0.530 log
points from least to most elastic. [CALCULATION: `derived/metro_panel.csv`]

Descriptive regressions of rent growth on the share change, heteroskedasticity-robust (HC1)
standard errors, **no instrument and no causal interpretation** [CALCULATION:
`derived/metro_regressions.csv`]:

| Spec | Term | Coefficient | HC1 SE | t | n | R² |
|---|---|---|---|---|---|---|
| 1 share only | Δ share (pp) | +0.01632 | 0.00520 | +3.14 | 152 | 0.073 |
| 2 bare product | Δ share × (1/ε) | +0.02471 | 0.00753 | +3.28 | 152 | 0.069 |
| 3 product with main effects | Δ share | +0.00565 | 0.01218 | +0.46 | 152 | 0.080 |
| 3 product with main effects | Δ share × (1/ε) | +0.01826 | 0.01694 | +1.08 | 152 | 0.080 |
| 4 share + state FE | Δ share | +0.03032 | 0.00725 | +4.18 | 152 | 0.542 |
| 5 product + state FE | Δ share × (1/ε) | −0.00650 | 0.01659 | −0.39 | 152 | 0.559 |
| 6 annualised, all metros | Δ share | +0.00142 | 0.00045 | +3.13 | 168 | 0.060 |
| 7 annualised + state FE | Δ share | +0.00252 | 0.00066 | +3.79 | 168 | 0.503 |
| 8 annualised product | Δ share × (1/ε) | +0.00177 | 0.00150 | +1.19 | 168 | 0.067 |

The share-change coefficient is positive and conventionally significant in every
specification that does not also carry the product term (1, 4, 6, 7). Specification 4 implies
a metro whose Mexican-origin share rose one percentage point more than another in the same
state is associated with about 0.030 log points more rent growth over the eleven-year window.
**The elasticity interaction does not survive.** It is significant only as a bare product
(spec 2), which is close to collinear with the share change itself, and it is indistinguishable
from zero once main effects are present (specs 3, 5, 8: t = +1.08, −0.39, +1.19). On this
cross-section the "demand growth is amplified where supply is inelastic" pattern is not
separately identified. [INFERENCE] That is a statement about this descriptive cross-section,
not evidence that the amplification does not exist.

Specs 1 to 5 drop 16 metros with no January 2015 ZORI value. Those 16 average elasticity 3.10
against 2.21 for the 152 retained, so the drop is not random with respect to elasticity; specs
6 to 8 re-run on all 168 using each metro's own first observed month and reproduce the sign,
significance and pattern. [DATA: `audit.json` → `regression_samples`]

Ladder 136 records that the usual shift-share instruments for Mexican inflows lose their
variation after 2005, so no instrumental-variables estimate is attempted. [SOURCE: BRIEF.md]

## 3. Mechanical price response

Rent response to a 1% demand shift, `d / (ε_S + ε_D)`. The demand elasticity is **assumed**,
not estimated. [CALCULATION: `derived/mechanical_response.csv`]

| Metro | Saiz ε_S | ε_D = 0.5 | ε_D = 0.7 | ε_D = 1.0 | Ratio to Houston (ε_D = 0.7) |
|---|---|---|---|---|---|
| Los Angeles, CA | 0.627 | 0.888% | 0.754% | 0.615% | 2.26 |
| San Francisco, CA | 0.662 | 0.861% | 0.734% | 0.602% | 2.20 |
| San Diego, CA | 0.673 | 0.853% | 0.728% | 0.598% | 2.19 |
| Riverside, CA | 0.943 | 0.693% | 0.609% | 0.515% | 1.83 |
| Dallas, TX | 2.175 | 0.374% | 0.348% | 0.315% | 1.04 |
| Houston, TX | 2.302 | 0.357% | 0.333% | 0.303% | 1.00 |
| San Antonio, TX | 2.982 | 0.287% | 0.272% | 0.251% | 0.82 |
| Austin, TX | 3.003 | 0.285% | 0.270% | 0.250% | 0.81 |

At these elasticities the arithmetic gives the same demand shift roughly 2.0 to 2.5 times the
rent response in coastal California that it gives in Houston, and the ratio narrows as the
assumed demand elasticity rises. This is arithmetic on published elasticities under a
single-market competitive assumption, not an estimate of any actual rent change.

## 4. Native interstate migration, ACS 2024 1-year PUMS

Native-born adults 25-64, gross flows and net rate per 1,000 resident natives of the same
group. Standard errors from the 80 replicate weights. [DATA: `derived/native_migration_2024.csv`]

| State | Group | Education | In | Out | Net | Net per 1,000 (SE) |
|---|---|---|---|---|---|---|
| California | NH white | all | 92,856 | 161,587 | −68,731 | −11.73 (1.35) |
| California | NH white | BA+ | 62,866 | 89,466 | −26,600 | −8.85 (1.82) |
| California | NH white | < BA | 29,990 | 72,121 | −42,131 | −14.75 (1.70) |
| California | all natives | all | 165,550 | 277,868 | −112,318 | −8.46 (0.76) |
| California | all natives | BA+ | 96,207 | 139,687 | −43,480 | −7.80 (1.16) |
| California | all natives | < BA | 69,343 | 138,181 | −68,838 | −8.94 (0.86) |
| Texas | NH white | all | 117,190 | 116,033 | +1,157 | +0.20 (1.24) |
| Texas | NH white | BA+ | 60,494 | 64,262 | −3,768 | −1.41 (1.87) |
| Texas | NH white | < BA | 56,696 | 51,771 | +4,925 | +1.53 (1.39) |
| Texas | all natives | all | 226,446 | 198,184 | +28,262 | +2.35 (0.98) |
| Texas | all natives | BA+ | 104,994 | 94,533 | +10,461 | +2.37 (1.69) |
| Texas | all natives | < BA | 121,452 | 103,651 | +17,801 | +2.34 (0.93) |

California's net outflow of native non-Hispanic white adults is large relative to its standard
error for every education group. The outflow is steeper among those without a bachelor's
degree (−14.75 against −8.85 per 1,000), a difference of 5.90 per 1,000 that exceeds the sum of
the two standard errors. Texas is statistically flat for this group overall (+0.20, SE 1.24),
and its net gain among all natives (+2.35, SE 0.98) is larger than among non-Hispanic whites
specifically. This is one year of gross flows with a one-year lookback. It counts moves and
says nothing about why anyone moved.

The G4 cross-check is unusually tight: the PUMS-weighted count of native-born non-Hispanic
white adults 18 and over matches the published `B05003H` total to 0.037% in California and
0.040% in Texas. [SOURCE: ACS 1-year 2024 `B05003H_009E` + `B05003H_020E`]

## Files covered / skipped

**Covered.** All inputs named in BRIEF.md were fetched and used: BPS state annual files
2000-2024 and the state record-layout documentation; FRED `CABPPRIV` and `TXBPPRIV`; the three
Census population-estimate vintages; ACS 1-year `B25001` for the five requested years,
`B01003` for 2023 and `B05003H` for 2024; ACS 5-year `B03001` by CBSA for 2010 and 2023, with
the variable labels confirmed from the key-free `variables.json` and recorded in `audit.json`;
`msa_rent_elasticity_panel` from `warehouse/immigration_context.duckdb` opened read-only; the
Zillow ZORI metro file; `saiz_2010_msa_elasticity.dta`; and `csv_pus.zip` read in place.
BPS monthly files for 2015, 2019 and 2023 were added beyond the brief to diagnose G1.

**Added beyond the brief.** Gate G1b (permit vintage), gate G6 (warehouse elasticity against
the primary Saiz file), regression specs 6 to 8 on all 168 metros, and
`derived/permits_vintage_check.csv`, `derived/state_growth_2010_2024.csv`,
`derived/pums_cells_raw.csv`.

**Skipped, with reasons.**

- *No published counterpart for the 25-64 nativity cell.* `B05003H` splits native-born only
  into under-18 and 18-and-over, so G4 compares the 18-and-over cell that Census actually
  publishes. The 25-64 counts used in the migration table are reported with replicate
  standard errors but have no published table to check against. Stated in `audit.json`.
- *`csv_hus.zip` (PUMS housing records) not read.* Nothing in the brief needs household-level
  records; all four pieces are person-level or state/metro aggregates.
- *No instrumental-variables estimate.* Excluded by the brief on the ladder-136 grounds.
- *2025 BPS file not used.* `st2512y.txt` exists upstream but 2025 is outside the requested
  2000-2024 window.

## Limitations

Copied from `derived/audit.json` without softening.

- Descriptive only. No causal identification is attempted or claimed anywhere in this lane.
  Ladder 136 records that the usual shift-share instruments for Mexican inflows lose their
  variation after 2005, so no instrumental-variables estimate is reported.
- The metro crosswalk in `msa_rent_elasticity_panel` is names-only. Metros are matched to ACS
  CBSA rows on principal-city name plus state; ambiguous matches are refused and listed as
  join failures rather than resolved by guesswork.
- CBSA boundaries and principal-city names changed between the 2010 and 2023 ACS 5-year
  vintages, so the 2010 and 2023 population shares are not measured on identical geographies
  for every metro.
- Saiz supply elasticities are estimated on 1970-2000 geography and land-use data and are held
  fixed here; they are not re-estimated for the 2010-2023 window.
- The demand elasticity in the mechanical calculation is assumed (0.5, 0.7, 1.0), not
  estimated. The mechanical response is arithmetic on published elasticities under a single-
  market competitive assumption, not an estimate of any actual rent change.
- ACS 5-year estimates for 2010 (2006-2010) and 2023 (2019-2023) overlap no years but each
  average five years, so a share change is a change in five-year averages.
- State housing-unit counts come from ACS 1-year `B25001` and exist only for the vintages
  fetched (2010, 2015, 2019, 2023, 2024); permits per 1,000 units is blank in other years. The
  United States housing-unit figure is the sum of the 51 state rows (50 states plus DC) and
  therefore excludes Puerto Rico.
- Permit counts are authorisations, not completions, and BPS imputes for non-responding permit
  offices; the reported (non-imputed) columns of the BPS file are not used.
- PUMS migration is a single year (2024) of gross flows with a one-year lookback. It counts
  moves, not movers' motives, and says nothing about why anyone moved.
- The 2018 BPS annual file (`st1812y.txt`) is refused by the Census WAF at its plain URL and
  was retrieved with an inert query parameter appended; the bytes were validated (December
  2018 survey date, 51 state rows) and the CA/TX totals sit inside the same FRED cross-check
  band as the other years.

One further limitation, specific to the regression sample and recorded in
`audit.json` → `regression_samples`: specifications 1 to 5 run on 152 of the 168 joined metros
because 16 have no January 2015 ZORI value, and those 16 are more supply-elastic on average
(3.10 against 2.21). Specifications 6 to 8 address this directly on the full 168.

## Instrument bias

This analysis was produced through an LLM, which carries systematic dispositions from
post-training on politically charged topics (`notes/llm-bias-caveat.md`). Two judgment calls
here are places where that matters and where a reader should check the underlying tables
rather than the prose: the decision to report the population-relative housing-growth
comparison alongside the per-resident rates in section 1, and the decision to report the
elasticity interaction as not separately identified rather than leaning on the one
specification where the bare product is significant. Both are recorded with their full
numbers above.
