**Verdict:** The school line is slightly too low, not too high. The account already charges the
group's pupils at their own states' average spending per pupil (it embeds R = 0.954), so the brief's
R (0.981 with Mexican-origin district weights) must not multiply the line: that would cut it by
$1.6–2.1bn for a gap the key already holds. What the account misses is where the pupils sit inside
their states: their districts spend 2.5% more than their state averages (Los Angeles, New York City,
Chicago, Dallas, Fresno), their schools 0.6% more than their districts, and the administrative state
mix adds 0.3%, so the key's school component should rise by k = 1.034 (low 1.020, high 1.047). The
corrected school line is **$89.9–117.6bn (+$2.8–3.7bn)**, the main case **$206.6–252.7bn** (+$3.4bn
at the low end, +$3.0bn at the high end) and the audit package **$205.7–253.8bn** (+$2.5–3.0bn). The
direction holds in every Mexican-origin specification (k 1.010–1.072); the size is moderately sure and
rests mostly on FY2024 spending, which carries COVID relief: the pre-COVID district pattern gives
k = 1.020.
[CALCULATION: lines.py → derived/per_pupil_weighting.csv; weighting.py → derived/r_by_spec.csv;
within_district.py → derived/within_district.json; checks.py → derived/top_districts.csv]

Lane `school_cost_where_enrolled_2026_09_24`, 2026-09-24, run by claude-opus-5-5[1m]. The lane adopts
nothing; everything below is a proposed change.

## Proposed changes

Low end = shared allocation, high end = personal allocation, as in the published bands.

| Package | School line, $bn | Change, $bn | Total, $bn | Change, $bn |
|---|---|---|---|---|
| Adopted main case, published | 87.14–113.96 | — | 203.21–249.64 | — |
| Main case, preferred (k 1.0342) | **89.94–117.62** | +2.79 / +3.67 | **206.59–252.67** | +3.38 / +3.03 |
| Main case, low (k 1.0197) | 88.76–116.07 | +1.61 / +2.12 | 205.16–251.39 | +1.95 / +1.75 |
| Main case, high (k 1.0474) | 91.01–119.03 | +3.87 / +5.08 | 207.89–253.84 | +4.68 / +4.20 |
| Audit package, preferred (row 6 at w 0.77 / 0.82) | 87.74–114.20 / 88.43–115.26 | +2.31 / +3.03 and +2.46 / +3.23 over row 6's school line | **205.70–253.61 / 205.88–253.77** | +2.80 / +2.51 and +2.98 / +2.67 |
| Audit package, low (k 1.0197) | 86.77–112.92 / 87.39–113.90 | +1.34 / +1.75 and +1.42 / +1.86 | 204.52–252.55 / 204.62–252.64 | +1.62 / +1.45 and +1.72 / +1.54 |
| Audit package, high (k 1.0474) | 88.64–115.37 / 89.38–116.50 | +3.21 / +4.20 and +3.41 / +4.47 | 206.78–254.57 / 207.03–254.80 | +3.88 / +3.47 and +4.13 / +3.70 |

[CALCULATION: lines.py → derived/per_pupil_weighting.csv, key_treatment `blend` (main case) and
`row6_w0.77`/`row6_w0.82` (audit package); audit totals add the change in main-case band ends to the
audit's published $202.9bn and $251.1bn (`dataset_integrity_2026_09_23/README.md`, net table)]

How it enters: k multiplies the school component of the explorer's `education_mix` key, giving key
share (k·T_s + T_p)/(N_s + N_p), and only the school step takes the re-priced key. In the audit
package the same k goes inside row 6's re-blended key, w·k·T_s/N_s + (1 − w)·T_p/N_p.

Two alternatives, not proposed:
- **One key for the whole education line**, as the explorer holds it: the colleges step moves too, and
  the main case becomes $207.42–254.50bn (+4.22 / +4.86); in the audit package $206.39–255.12bn
  (w 0.77) to $206.62–255.38bn (w 0.82). The colleges step is postsecondary spending, so a K-12 price
  has no claim on it; it moves only because the key blends the two, which is what the audit's row 6
  already corrects. [CALCULATION: per_pupil_weighting.csv, key_treatment `blend_whole_line`,
  `row6_w*_whole_line`]
- **The school step keyed by the school component alone** (k·T_s/N_s): school line $90.89–119.09bn,
  main case $207.75–253.88bn (+4.54 / +4.24). Of that, +0.90 / +0.99 is the key change itself at k = 1,
  which overlaps with the audit's row 6, so the two must not be stacked. [CALCULATION:
  per_pupil_weighting.csv, spec `preferred_district_and_school_level` and `school_key_only`, key
  `school`]

## Why the brief's R cannot multiply the line

The published school step is school share × response (0.63–0.66) × the education line × the
`education_mix` key share. The key's school component
(`school_enrollment_2026_09_20/derived/updated_account_components.csv`) prices each of the group's
8.487m transported pupils at its state's ASSF FY2024 Table 8 current spending per pupil: $16,860 per
group pupil against $17,669 for all 48.551m pupils, **R_embedded = 0.9542** (personal allocation)
[CALCULATION: account_pupils.py → derived/account_embedded_price.json; it rebuilds the canonical
component to 1e-6, test_lane.py]. The brief's R (group-weighted spending per pupil ÷ national) already
contains that state-mix part, because Texas and Arizona are cheap states. Multiplying the line by
R = 0.9812 counts it twice: school line $85.51–111.82bn (−1.63 / −2.14), main case
$201.23–247.87bn; with the F-33 prices of family C (R 0.9668) the cut is −2.89 / −3.78 [CALCULATION:
per_pupil_weighting.csv, specs `literal_R_times_line:*`]. The correction that belongs in the account
is k = R ÷ R_embedded on the key's school component.

## Method

1. **Positive control.** `engine_school.cjs` loads the explorer's engine and model
   (`assumption_explorer_2026_09_21`) and rebuilds the staircase's "schools" step and the adopted main
   band on the 64-spec grid (allocation × normalization × school share 0.715/0.865 × school response
   0.63/0.66 × general-government response 0.59/0.84 × uncompensated-care key, justice by use). It
   reproduces the school step **$87.1414–113.9558bn** (low end: shared allocation, share 0.715,
   response 0.63; high end: personal, 0.865, 0.66) and the main case **$203.207–249.640bn** of
   `figures_2026_09_22/src/generated/figures.json`; the step equals share × response × key target in
   every spec. A re-priced key enters as a synthetic line at the school response only, and a linearity
   gate checks it. [CALCULATION: engine_school.cjs; test_lane.py]
2. **District linkage.** CCD LEA membership 2023-24 (K-12 = kindergarten, grades 1–12 and ungraded;
   all pupils and Hispanic) joined to Census F-33 FY2024 on the NCES LEA ID, with New York City's 32
   geographic districts merged into F-33's single unit 3620580. Spending per pupil is TCURSPND ÷ ENROLL,
   kept within $3,000–80,000. Of 18,298 CCD LEAs (50 states and DC), 13,639 match an F-33 unit and
   13,148 carry a valid price; they hold 93.6% of K-12 pupils, 92.0% of Hispanic pupils and 91.4% of the
   group's pupils. Of the 0.741m uncovered group pupils, 0.684m are in independent charter districts
   (CCD LEA type 7), which F-33 excludes: "Charter schools whose charters are held by nongovernmental
   entities are deemed to be out of scope". Uncovered pupils take their state's group mean.
   [DATA: derived/linkage.json; SOURCE: ASSF FY2024 `elsec24_sumtables.xlsx`, Table 8 note,
   https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/elsec24_sumtables.xlsx]
3. **Weightings.** (i) Hispanic K-12 pupils. (ii) Hispanic × the state's Mexican share of Hispanic
   public K-12 pupils from the ACS 2024 1-year PUMS (US 0.614, SE 0.002; California 0.822, Texas 0.812,
   Arizona 0.867, Illinois 0.770) [CALCULATION: acs_mexican_share.py → derived/acs_state_pupils.csv].
   (iii) Hispanic × a district Mexican share: ACS 2020–2024 B03001 Mexican ÷ Hispanic residents of the
   district's own Census school-district geography when it has at least 100 Hispanic residents (7.89m
   group pupils), else its county (0.06m), else the state (0.69m, mostly charter districts), scaled
   from all ages to children by the state's PUMS child/all-age ratio, capped at 1, and raked within each
   state to the PUMS pupil share [CALCULATION: weighting.py → derived/linkage.json]. Variants: the
   broad Mexican definition, unraked shares, all-age shares.
4. **Three families of R**, all current spending per pupil:
   - **B (preferred):** the group's state mix from CCD × the account's own ASSF Table 8 state prices ×
     a within-state factor f_s (group-weighted F-33 district spending ÷ all-pupil-weighted, same state).
     It keeps the account's price concept and changes only where the pupils are.
   - **A:** the account's CPS state mix × Table 8 × f_s, the within-state effect alone.
   - **C:** the brief's literal R, F-33 district prices in both numerator and denominator. It also
     swaps the price source: F-33 district sums exceed Table 8 by 0.8% in Texas, 2.3% in California,
     2.6% in Arizona and 3.1% nationally, so the group's states look cheaper [CALCULATION: checks.py →
     derived/price_source_check.csv]. Table 8 excludes payments to other school systems and
     nonelementary-secondary programs and divides by fall-2022 CCD memberships that Census adjusts
     [SOURCE: Table 8 note, above].

   k = R ÷ R_embedded on the same price concept. For family A, weightings (i) and (ii) coincide,
   because a state-level share does not change the within-state factor.
5. **Schools within districts.** NCES School-Level Finance Survey (SLFS) FY2022: TCURELSCS (all funds)
   and TCURELSCSE, which excludes "expenditures paid from federal funds other than federal funds
   intended to replace local tax revenues" [SOURCE: NCES 2025-047r, p. 11 and p. 22,
   https://ies.ed.gov/sites/default/files/data-asset/ccd-common-core-data/2025/09/documentation-nces-common-core-data-school-level-finance-survey-slfs-school-year-2021-22-fiscal-year/2025047r.zip].
   For each district with at least two schools: Hispanic-weighted school spending per pupil (CCD 2021-22
   school membership) ÷ the pupil-weighted mean, with districtwide records spread equally; districts are
   weighted by the group's 2023-24 pupils, and uncovered districts count as 1 [CALCULATION:
   within_district.py].
6. **English learners.** District spending per pupil regressed on EL share (CCD 2018-19, the last
   district EL file held), child-poverty share (SAIPE) and log enrollment, with state fixed effects,
   weighted by pupils, state-clustered standard errors [CALCULATION: el_check.py].
7. **Lines.** Each k re-prices the key's school component and runs through the engine [CALCULATION:
   lines.py → engine_school.cjs].

## Results

### R under each weighting

| Weighting | B (preferred) | C (brief's literal) | A (account's state mix) |
|---|---:|---:|---:|
| Hispanic | 1.0395 | 1.0387 | 0.9789 |
| Mexican, state share | 0.9828 | 0.9683 | 0.9789 |
| **Mexican, district share** | **0.9812** | 0.9668 | 0.9773 |
| k = R ÷ 0.9542, same rows | 1.0894 / 1.0300 / **1.0284** | 1.0886 / 1.0148 / 1.0132 | 1.0259 / 1.0259 / 1.0242 |

[CALCULATION: weighting.py → derived/r_by_spec.csv]

Hispanic weights overstate the group's cost: non-Mexican Hispanic pupils sit in dearer states, which
lifts the state-mix factor to 1.056 against 1.003 for the Mexican weights. The variants,
unraked district shares (k 1.0270), all-age district shares (1.0262) and the broad Mexican
definition on state shares (1.0298), sit within 0.3 points of 1.0284 [CALCULATION: r_by_spec.csv].

### Where k comes from

k (B, Mexican district) = state mix 1.0026 × within-state 1.0247 × national denominator 1.0010 (CCD
rather than CPS pupil weights) = 1.0284; × schools within districts 1.0057 = **1.0342**
[CALCULATION: r_by_spec.csv, within_district.json, lines_summary.json].

The within-state lift is a big-city effect. Districts above their state mean add 7.28 points and
those below subtract 4.81, a net 2.47 points; the 25 largest group districts carry 2.34 of them
[CALCULATION: checks.py → derived/top_districts.csv].

| District | Group pupils | Spending per pupil | ÷ state mean | Share of the lift |
|---|---:|---:|---:|---:|
| Los Angeles Unified | 204,439 | $26,033 | 1.288 | 38.2% |
| New York City | 62,832 | $41,359 | 1.198 | 12.3% |
| Chicago | 104,438 | $25,001 | 1.158 | 10.0% |
| Dallas ISD | 74,617 | $15,300 | 1.196 | 5.7% |
| Fresno Unified | 44,806 | $23,774 | 1.176 | 5.1% |
| Santa Ana Unified | 33,559 | $24,729 | 1.223 | 4.9% |
| San Bernardino City Unified | 32,406 | $24,564 | 1.215 | 4.5% |
| Clark County | 101,522 | $14,832 | 0.998 | −0.1% |
| Northside ISD | 53,783 | $12,297 | 0.961 | −0.8% |
| Socorro ISD | 38,361 | $11,846 | 0.926 | −1.1% |
| Cypress-Fairbanks ISD | 31,722 | $11,162 | 0.872 | −1.6% |

[CALCULATION: derived/top_districts.csv; spending is F-33 FY2024 TCURSPND ÷ ENROLL, the state mean is
all-pupil-weighted over valid districts]

Growing suburban and border districts in Texas pull the other way. Dropping Los Angeles Unified
entirely leaves k unchanged (+0.0005): its spending also lifts the California mean that the other
districts are compared with, and the rest of the group's California districts sit above the rest of
the state by a similar margin [CALCULATION: derived/robustness.csv].

| State | Group pupils, admin (account) | Table 8 per pupil | Within-state factor | Group per pupil | Contribution to R |
|---|---:|---:|---:|---:|---:|
| California | 2.689m (2.446m) | $20,791 | 1.024 | $21,283 | 0.375 |
| Texas | 2.253m (2.000m) | $12,895 | 1.033 | $13,320 | 0.197 |
| Illinois | 0.381m (0.369m) | $21,776 | 1.051 | $22,896 | 0.057 |
| Arizona | 0.459m (0.550m) | $12,003 | 1.004 | $12,046 | 0.036 |
| New York | 0.120m (0.127m) | $31,918 | 1.095 | $34,946 | 0.028 |
| Washington | 0.215m (0.272m) | $18,564 | 0.994 | $18,462 | 0.026 |
| Colorado | 0.221m (0.218m) | $15,908 | 1.020 | $16,220 | 0.023 |
| All 50 states and DC | 8.643m (8.487m) | | | $17,320 | 0.981 |

[CALCULATION: weighting.py → derived/state_breakdown.csv; contributions sum to R_B, gated; Table 8
values match `_cache/elsec24_sumtables.xlsx`]

The administrative mix puts more of the group in California (31.1% against the account's 28.8%) and
Texas (26.1% against 23.6%), and less in Arizona, Washington and North Carolina; net +0.26% [DATA:
derived/state_breakdown.csv].

### School lines by specification (main case)

| Specification | k | School line, $bn | Main case, $bn |
|---|---:|---|---|
| Published | 1 | 87.14–113.96 | 203.21–249.64 |
| B, Mexican district shares | 1.0284 | 89.46–117.00 | 206.01–252.15 |
| **Preferred: B × school level** | **1.0342** | **89.94–117.62** | **206.59–252.67** |
| Low: FY2019 within-state pattern × state-and-local school level | 1.0197 | 88.76–116.07 | 205.16–251.39 |
| High: preferred × EL upper bound | 1.0474 | 91.01–119.03 | 207.89–253.84 |
| C, Mexican district shares | 1.0132 | 88.22–115.37 | 204.51–250.81 |
| B, FY2024 net of COVID relief | 1.0218 | 88.92–116.29 | 205.36–251.57 |
| Preferred, instruction and support only | 1.0285 | 89.48–117.02 | 206.03–252.17 |
| Preferred, depreciation keyed by capital outlay | 1.0474 | 91.01–119.03 | 207.89–253.84 |
| Preferred, depreciation keyed by interest | 1.0724 | 93.06–121.72 | 210.37–256.06 |
| Preferred × administrative pupil count | 1.0532 | 91.49–119.66 | 208.46–254.35 |
| B, Hispanic weights | 1.0894 | 94.45–123.54 | 212.04–257.56 |
| Literal R × line (B) | 0.9812 | 85.51–111.82 | 201.23–247.87 |

[CALCULATION: lines.py → derived/per_pupil_weighting.csv, key_treatment `blend`]

### Schools within districts

SLFS FY2022 has 106,961 records, 5,460 of them districtwide; 94.4% of the school records match a CCD
school.
Factors exist for 11,230 districts (86,591 schools) holding 93.5% of the group's pupils. The group's
pupils attend schools that spend 0.61% more than their district's average (0.57% with uncovered
districts at 1): California 1.0073, Texas 1.0054, Arizona 1.0090, Illinois 0.9901. With state and local
funds only, the factor is 1.0040, so federal money (Title I, IDEA and, in FY2022, COVID relief) carries
0.17 of the 0.57 points [CALCULATION: within_district.py → derived/within_district.json,
derived/within_district_by_state.csv]. The school level adds $0.5–0.6bn to the line (B at 1.0284
against the preferred 1.0342) [CALCULATION: per_pupil_weighting.csv].

### English learners

| Spending year | EL counts | EL coefficient, $ per pupil (SE) | ÷ mean spending | Poverty coefficient (SE) | Districts |
|---|---|---:|---:|---:|---:|
| FY2019 | 2018-19 (matched) | 3,807 (1,287) | 29.7% of $12,829 | 4,060 (1,553) | 9,909 |
| FY2024 | 2018-19 (lagged) | 7,317 (1,862) | 42.5% of $17,213 | 11,304 (1,541) | 9,895 |

[CALCULATION: el_check.py → derived/el_regression.csv, model `el_poverty`; state fixed effects, 50
states]

At equal poverty, districts with more English learners spend more per pupil. Between districts that is
already in the district weighting: the group's districts are 17.7% EL against 9.9% for all pupils.
Within districts, the group's pupils are more often EL than their districts' average: an estimated
20.7%, from ACS "speaks English less than very well" rates (Mexican-origin pupils 11.2%, all pupils
5.4%) × 9.9%. Charging the whole coefficient to that 3.0-point gap adds $221 per group pupil (+1.27%)
at FY2024, or $115 (0.9% of that year's mean) at FY2019. The lane uses it only as the upper bound
(k 1.047), because a district coefficient also carries costs that follow EL concentration without
going to EL pupils [CALCULATION: el_check.py → derived/el_within_district.json; INFERENCE on the
upper-bound reading].

### BEA mapping, capital outlay and interest

The account's education line is BEA's 2024 education consumption, $1,221.159bn [SOURCE: BEA NIPA
Table 3.17 line 9, https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx], allocated by
a Census current-spending key. Census current spending is instruction + support services + other
non-instructional spending (F-33 TCURSPND equals the three in every row [CALCULATION: checks.py →
derived/price_source_check.csv, `tcurspnd_equals_components_share`]). It covers salaries, benefits, purchased services and
supplies and excludes "capital outlay, interest on school debt, payments to other schools and LEAs"
[SOURCE: NCES 2025-047r, p. 26]. BEA consumption also includes consumption of fixed capital
(depreciation): $312.559bn of $2,550.362bn state and local consumption, 12.26% [SOURCE: NIPA Table
3.10.5 lines 51 and 47]. Capital outlay sits in gross investment ($182.969bn for education [SOURCE:
NIPA Table 3.17 line 113]), outside the account's consumption line, and interest is in neither. So the
current-spending key fits the 87.7% of the line that is current spending, and the 12.3% depreciation
belongs with the capital stock, for which capital outlay and interest per pupil are proxies.

The group's districts spend more on both: capital outlay $2,588 per pupil against $2,425 nationally
(R 1.067), interest $629 against $499 (R 1.258) [CALCULATION: weighting.py →
derived/r_other_concepts.csv, family C, Mexican district shares]. Keying the depreciation share by
capital outlay raises k to 1.0474 (school line $91.0–119.0bn); keying it by interest raises k to 1.0724
($93.1–121.7bn) [CALCULATION: per_pupil_weighting.csv]. Neither is in the preferred figure. Capital
outlay follows enrollment growth more than the stock in place, and 12.3% is a state-and-local share,
not an education-specific one [INFERENCE]. Capital outlay and interest are reported here separately and
never added to the consumption line. Counting instruction and support only, without food services and
enterprise operations, lowers k by 0.55% [CALCULATION: r_other_concepts.csv, `pp_core`].

### Pupil counts

| Count | Group pupils |
|---|---:|
| Account (CPS October rates transported to March 2025 CPS) | 8.487m |
| CCD Hispanic K-12 (14.09m) × Mexican district shares | 8.643m (+1.8%) |
| CPS October 2024, direct | 8.634m (SE 0.222m) |
| ACS 2024 PUMS, public K-12, Mexican origin | 8.201m |

[DATA: derived/account_embedded_price.json, derived/linkage.json,
`school_enrollment_2026_09_20/derived/october_counts.csv`; CALCULATION: acs_mexican_share.py]

CCD's Hispanic K-12 count exceeds ACS's 13.35m Hispanic public K-12 pupils by 5.5% [CALCULATION:
linkage.json, acs_state_pupils.csv]. Replacing the account's count with the administrative one would
add another 1.8% (k 1.0532, school line $91.5–119.7bn). That is a count question for the enrollment
lane, so it is not in the proposal.

## Disconfirmation and robustness

The brief's premise is that the account charges the national average per pupil, so the group's
concentration in Texas and Arizona would make the line too high. The account charges state averages
instead: the state part is already in the key, and the within-state part goes the other way. Checks
that could have reversed or shrunk the result:

| Check on B, Mexican district shares | k | Change |
|---|---:|---:|
| Baseline | 1.02835 | — |
| Drop Los Angeles Unified | 1.02887 | +0.00052 |
| Drop the five largest group districts | 1.02849 | +0.00014 |
| Spending over CCD fall-2023 membership | 1.02838 | +0.00003 |
| Per-pupil band $5,000–50,000 | 1.02830 | −0.00005 |
| Uncovered pupils at 0.85 × state all-pupil mean | 1.02617 | −0.00218 |
| Uncovered pupils at 1.00 × state all-pupil mean | 1.02620 | −0.00215 |
| State share where no own district geography | 1.02820 | −0.00015 |

[CALCULATION: checks.py → derived/robustness.csv]

- **Spending year.** FY2024 district spending contains COVID-relief current spending (F-33 item AE1,
  "Current expenditures paid from COVID-19 Federal Assistance Funds" [SOURCE: F-33 2024 form, Part
  XIII item 1, p. 6, https://www2.census.gov/programs-surveys/school-finances/information/2024/f33_2024_508.pdf]):
  3.41% of current spending nationally, 4.43% in California, 4.21% in Texas, 4.68% in Arizona, 3.94% in
  Illinois, none reported in New York [CALCULATION: checks.py → derived/price_source_check.csv]. Net of
  relief, the within-state factor falls from 1.0247 to 1.0181 (k 1.0218); on FY2019 spending it falls to
  1.0120 (k 1.0157) [CALCULATION: r_by_spec.csv]. This is the largest threat to the size.
- **Price source.** Family C, with F-33 district prices throughout, gives k 1.0132, still above 1.
- **Weights.** No Mexican-origin weighting in any family gives k below 1.010 [CALCULATION:
  r_by_spec.csv].

## Related finding: the audit's row 6

The audit adds −3.5bn (−4.8 to −2.2) at both band ends for re-weighting the education key toward
BEA's K-12 split of 77–82% (`dataset_integrity_2026_09_23/README.md` row 6; `spending.md` #5). This
lane's re-blend reproduces the audit's key shares (personal 0.1610–0.1623 against its 0.1605–0.1622)
[CALCULATION: lines.py key gates; derived/per_pupil_weighting.csv]. Run through the engine on the whole
education line, it moves the main case −1.8 to −2.6bn at the low end and −2.6 to −3.7bn at the high end
[CALCULATION: per_pupil_weighting.csv, specs `audit_row6_w0.77_whole_line`, `audit_row6_w0.82_whole_line`].
The audit's range is close to the change in the line's allocation before the education response
(−2.6 to −4.9bn here [CALCULATION: lines.py → derived/lines_summary.json,
`row6_allocation_change_bn`]); `spending.md` gives the key shares but no engine run [INFERENCE]. If so, row 6
overstates the reduction by about $1.3bn at the low end and $0.4bn at the high end, at the midpoint of
w. Keying each step by its own component (schools by K-12 pupils, colleges by postsecondary students)
would move the main case −2.1bn / −7.1bn before this lane's correction and +1.6bn / −3.8bn with it
[CALCULATION: per_pupil_weighting.csv, specs `split_both_keys`, `split_both_keys_preferred`]. These
belong to the audit's owner; this lane changes nothing there.

## What would change the answer

- **Spending after COVID relief.** If district spending in 2024-25 returns to the FY2019 within-state
  pattern, k falls toward 1.020 and the addition to about +$1.6–2.1bn.
- **Charter pupils.** 0.684m group pupils in independent charter districts are priced at their state's
  group mean. Charter spending at the state all-pupil mean lowers k by 0.002.
- **A measured EL cost per EL pupil** within districts would replace the EL upper bound.
- **Education-specific depreciation and capital stock by district** would settle the BEA mapping,
  which spans k 1.034–1.072.
- **Pupil identification.** District Mexican shares describe residents of all ages, scaled to children
  by a state ratio. They do not follow pupils across district lines, into charters or across the
  district's age mix.

## Limits

- Time frames are mixed: ACS 2020–2024 shares, CCD 2023-24 counts, F-33 FY2024 spending over fall-2022
  enrollment, SLFS FY2022, EL counts 2018-19.
- SLFS FY2022 is a provisional file from a COVID-relief year.
- Family B takes Table 8 as each state's price and F-33 only for within-state ratios. F-33 sums and
  Table 8 diverge by state (New York +8.4%, Texas +0.8%), and the reason is not traced
  [UNVERIFIED].
- The response (63–66%) and the education line are untouched. The correction assumes spending per
  pupil follows the pupil, as the account's key already does.

## Blocked and substitutions

Nothing was hard-blocked. Substitutions:
- School-level spending comes from NCES SLFS FY2022, the official school-level file. NERD$ was not
  used.
- District EL counts after 2018-19 are not in the CCD files held, so the 2018-19 counts are used,
  lagged for FY2024.
- The ACS has no Mexican-origin-by-age table for school districts, so the child share is scaled from
  all ages by the state PUMS ratio.
- F-33 omits charters held by nongovernmental entities, so their pupils take the state's group mean.

## Derived files and their specification columns

Rows that run against the leading reading are named in each entry.

- `per_pupil_weighting.csv` (93 rows; `spec` × `key_treatment` in blend, school, blend_whole_line,
  split_both, row6_w0.77, row6_w0.82, row6_w0.77_whole_line, row6_w0.82_whole_line): `published`,
  `school_key_only`; `{A,B,C}_current_{hispanic, mexican_state_share, mexican_state_share_broad,
  mexican_district_share, mexican_district_share_unraked, mexican_district_share_all_ages}`;
  `{A,B}_current_ex_covid_relief_{hispanic, mexican_state_share, mexican_district_share}`;
  `{A,B}_current_within_state_factor_fy2019_{same three}`; `preferred_district_and_school_level`
  (leading); `low_fy2019_factor_state_local_school_level`; `high_preferred_plus_el_upper_bound`;
  `preferred_bea_depreciation_by_capital_outlay`; `preferred_bea_depreciation_by_interest`;
  `preferred_instruction_support_only`; `preferred_admin_pupil_count`. Against the leading reading:
  `literal_R_times_line:B_current_mexican_district_share` and `…:C_…` (lower the line);
  `split_both_keys`, `split_both_keys_preferred` (main case lower at the high end); `audit_row6_w0.77`,
  `audit_row6_w0.82` and their `_whole_line` rows (the audit's own row 6, negative, the bases for the
  audit deltas); the low row under row 6 at w 0.77 (school line below published).
- `r_by_spec.csv` (30 rows): `{family}_{concept}_{weighting}`, families A, B, C (C for current only),
  concepts current, current_ex_covid_relief, current_within_state_factor_fy2019. Against: none below
  k = 1 for Mexican weights; the smallest are C all-age 1.0103 and A FY2019 district 1.0117.
- `r_other_concepts.csv` (18 rows): `concept` (pp, pp_ex_covid, pp_core, pp_capout, pp_interest,
  pp_fy2019) × `weighting` (hispanic, mexican_state_share, mexican_district_share), family C. Against:
  pp_core, pp_ex_covid and pp_fy2019 sit below pp.
- `robustness.csv` (8 rows): `check`, as in the table above. Against: both uncovered-pupil rows, the
  narrower band, the state-share row.
- `el_regression.csv` (10 rows): `spending_year` × `model` (el_only, el_poverty) × `term` (el_share,
  pov_share, log_enroll). Against: the FY2019 EL coefficient is half the FY2024 one.
- `state_breakdown.csv` (51 rows): `state`. Against: states with a within-state factor below 1
  (Washington, Georgia, New Mexico, Nevada and others).
- `top_districts.csv` (25 rows): `LEAID`. Against: Clark County, Northside, Socorro, United,
  Albuquerque, Cypress-Fairbanks, Gwinnett.
- `within_district_by_state.csv` (95 rows): `fips` × `spend` (TCURELSCS, TCURELSCSE). Against:
  Illinois 0.9901.
- `price_source_check.csv` (52 rows): `fips` (0 = United States).
- `district_match_by_state.csv`, `account_pupils_by_state.csv`, `acs_state_pupils.csv`: one row per
  state (`state_fips` 0 = United States in the ACS file); `engine_school_lines.csv`: `variant`, the
  engine's output behind per_pupil_weighting.csv.

## Reproduce

Inputs held locally: F-33 FY2024 `elsec24t.txt` and `elsec24.txt`
(https://www2.census.gov/programs-surveys/school-finances/tables/2024/secondary-education-finance/),
CCD LEA 2023-24 membership and directory (https://nces.ed.gov/ccd/Data/zip/ccd_lea_052_2324_l_1a_073124.zip,
`ccd_lea_029_2324_w_1a_073124.zip`), CCD LEA 2018-19 EL (`ccd_lea_141_1819_l_1a_091019.zip`), SAIPE 2023
districts, the ACS 2024 1-year PUMS and the BEA Section 3 workbook, all under `~/research-data` or
`sources/immigration-fiscal/data/external/`.

```sh
# from the repository root, in bash or zsh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a   # CENSUS_API_KEY; never print it
L=infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24
run() { OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pandas --with numpy python3 "$@"; }
run $L/acquire.py        # ACS B03001 by district and county, SLFS FY2022, F-33 FY2019 → _cache/
run $L/pdownload.py https://nces.ed.gov/ccd/Data/zip/ccd_sch_052_2122_l_1a_071722.zip \
  $L/_cache/ccd_sch_052_2122_l_1a_071722.zip --parts 32
curl -sS --fail -o $L/_cache/ussd18.txt \
  https://www2.census.gov/programs-surveys/saipe/datasets/2018/2018-school-districts/ussd18.txt
run $L/account_pupils.py
run $L/acs_mexican_share.py
run $L/ccd.py
run $L/weighting.py
run $L/within_district.py
run $L/el_check.py
run $L/lines.py          # writes the variants and runs node engine_school.cjs
run $L/checks.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pandas --with numpy \
  --with pytest python3 -m pytest -p no:cacheprovider $L/test_lane.py -q     # 4 passed
```

`test_lane.py` checks the engine reproduction of the published step and main case, the rebuilt school
component against the canonical key, Texas by hand from raw F-33 and raw CCD, and the preferred line
against its closed-form formula.
