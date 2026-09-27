claude-opus-5-5

# System-wide school degradation: can it hide from the peer-effect measures?

**Verdict:** On absolute, low-stakes NAEP, white pupils did not lose ground where the Hispanic or
immigrant-origin share rose (+0.087 (0.027) and −0.019 (0.026) SD per 10 points, 2003–2019, 51
states). Cut scores, NAEP exclusion, graduation rates and exit exams do not move the way a
system-wide degradation requires. The English-learner share alone gives a small negative: −0.035
(0.018) SD per 10 points, which fades with region-by-year effects or state trends, and −0.070
(0.030) for grade 4 against the cohort's K–1 share, which holds with region-by-year effects and has
no lead. If causal, it is worth about $1bn of lifetime earnings per cohort of white pupils at the
observed national rise. A shift common to all states is outside any test of this kind.
[CALCULATION: §2–§8]

Lane `infra/immigration-fiscal/school_systemwide_2026_09_27/`, brief `BRIEF.md` (38c28ae), started
2026-09-27. Sections are appended as each test finishes. Every estimate is per 10 percentage points
of the share, with its standard error in parentheses, state and year fixed effects and SEs clustered
by state unless a row says otherwise.

## 0. The two positions, at their strongest

**The operator's hypothesis.** Under No Child Left Behind (2002–2015) each state set its own
proficiency cut score and had to bring every subgroup, English learners and Hispanic pupils
included, toward 100% proficiency. A state with a fast-growing English-learner population had more
subgroups at risk and the cheapest remedy was to move the bar: lower the cut score, thin the
curriculum, grade more leniently, drop the exit exam, exclude low scorers from tests. Every such
move is common to all schools in the state. The designs behind the null (Figlio et al., Diette and
Oyelere and the repo's ECLS-K checks) compare pupils within a school, a family or a state, and
most re-standardize scores within each grade and year. A statewide shift is absorbed by their fixed
effects or subtracted by the standardization, so their null cannot speak to it. Hunt's positive
result is on high-school completion, the very credential a laxer system would inflate. [INFERENCE]

**The null.** State NAEP is federally run, low-stakes for pupils and schools, and on one scale since
the 1990s (math) and 1992 (reading); a state cannot move its cut points. If schooling degraded in
the states where immigrant and English-learner shares rose, their white and non-English-learner
pupils should have lost ground on NAEP relative to other states. Lowered state standards change
the label (percent proficient), not the skill NAEP measures, and the skill is what earnings price.
The large-inflow states include some of the 2003–2013 NAEP gainers. Funding follows pupils in part
(0.45 in one year, 0.87 over 19 years within districts; dilution lane), and compensatory aid rises
with the share. [INFERENCE; SOURCE: `../school_dilution_2026_09_24/RESULT.md` §1]

**What each predicts.** The hypothesis predicts, where the share rose more: lower NAEP scores for
incumbent pupils; lower NAEP-equivalent cut scores; more exclusion from NAEP; graduation rates
rising relative to the same cohort's NAEP grade-8 scores; exit exams dropped. The null predicts
none of these. Confounders run both ways: the Sunbelt's growth and the South's NAEP gains in the
2000s would push the estimates up; the 2007–2011 housing bust and school budget cuts, heaviest in
Nevada, Arizona, Florida and California, would push them down. [INFERENCE]

## 1. Design table (Test 1)

The US table is `design_table/design_us.csv` (14 rows, built by `design_table/build_design_us.py`,
rebuilt byte-identically on 2026-09-28), with quotes and page or table locators in
`design_table/NOTES_us.md`. The European table is `design_table/design_eu.csv`, notes
`design_table/NOTES_eu.md`. [DATA]

| Study | Outcome measure | Comparison | Sees a statewide shift? |
|---|---|---|---|
| Figlio, Giuliano, Özek & Sapienza 2024 (Florida) | FCAT standardized "at the grade-year level over the entire population" | siblings, with school×year and grade×year FE | No |
| Diette & Oyelere 2014, 2017a, 2017b (North Carolina) | state test z-scores | within school across grades, school×year FE | No |
| Figlio & Özek 2019 (Haiti earthquake, Florida) | state test standardized within grade-year | within school across grades | No |
| Doan, Morales, Özek & Schwartz 2024 (Delaware) | state test standardized within grade-year | within school across grades | No |
| Ahn & Jepsen 2015 (North Carolina) | state test standardized | within student over time | No |
| Cho 2011; the repo's ECLS-K checks | ECLS-K scale re-standardized per wave | within school across classrooms | No |
| Hunt 2017 | high-school completion of natives 11–17 | between states over decades (1940 settlement IV) | Partly: sees states, but the outcome is the credential a laxer system inflates |
| Borgschulte, Cho, Lubotsky & Rothbaum 2025 | adult income rank, BA completion | across commuting zones (1980 enclave IV) | Partly: sees local systems, measures adult outcomes |
| Betts & Fairlie 2003 | private-school enrollment | across metros | Partly: flight, not learning |

[SOURCE: rows and quotes in `design_table/design_us.csv`; e.g. Figlio et al. p. 977 §2.4: "we
standardize the statewide test scores to zero mean and unit variance at the grade-year level over
the entire population of students"]

The helper found no US study that relates immigrant, English-learner or Hispanic shares to native
or white achievement between states over time on NAEP. [SOURCE: `design_table/NOTES_us.md`, search
section]

### 1b. European and other non-US designs

Eleven studies, filled from primary text by a second helper (`design_table/design_eu.csv`, notes
`design_table/NOTES_eu.md`, built by `design_table/build_design_eu.py`). I re-read the one
"Yes" row against its source. Schneeweis (Austria) is left to the `pisa_germany_2026_09_27` lane,
which verifies the same European papers. The helper stopped at its turn cap before its searches on
the German Länder and on teacher grading against external tests, so neither is covered here. [DATA]

| Study | Outcome | Comparison | Sees a system-wide shift? | Native estimate |
|---|---|---|---|---|
| Brunello & Rocco 2013 (27 countries, PISA 2000–2009) | country mean of natives, PISA scale linked across waves | countries over time, wave FE | **Yes** | −0.275% of the native score per point of first-generation share (SE 0.135%) |
| Tumen 2021 (Turkey, Syrian refugees) | PISA, standardized | regions over time, year FE | Partly: regions, not the country | +0.11 to +0.16 SD (binary) |
| Ohinata & van Ours 2013 (Netherlands) | PIRLS/TIMSS points | classes within a school, one year | No | within ±1.5 points per point |
| Geay, McNally & Telhaj 2013 (England) | KS2 percentile rank | within school over cohorts, year dummies | No | 0.002 (0.008) percentile points per point |
| Ballatore, Fort & Ichino 2018 (Italy) | INVALSI fraction correct | classes within an institution, one year | No | −0.0085 (0.0025) per native swapped |
| Tonello 2016 (Italy) | INVALSI grade-8 exam | within school, macro-area × year FE | No | −0.65% per 10 points (language) |
| Frattini & Meschi 2019 (Lombardy) | regional test z-scored per wave | within school | No | −0.046 SD per 10 points (maths) |
| Jensen & Rasmussen 2011 (Denmark) | PISA reading | between schools, county IV | No | −0.28 to −0.31 points per point (2008 WP) |
| Schilling & Hoeckel 2026 (Hamburg) | KERMIT, z-scored over all years | within school, test-year FE | No | +0.27 (0.58) per unit share |
| Hassan et al. 2023 (Denmark, refugees) | national tests z-scored per grade-year | school FE, difference in differences | No | −0.010 (0.009) SD |
| Gould, Lavy & Paserman 2009 (Israel) | matriculation pass | schools within one cohort | No | −0.28 points (t −2.0) per point |

[SOURCE: rows, quotes and locators in `design_table/design_eu.csv`; Brunello and Rocco, IZA DP 5479,
Table 2 col. 1 and p. 12: "a one percentage point increase in the share of immigrant students is
expected to reduce the average test scores of natives by 0.275 percent in the full sample"]

The one between-system design finds harm. At a native PISA mean near 500 and the OECD student SD of
100, its estimate is about −0.014 SD (0.007) per point of first-generation share. The nearest US
analogue in §2, the foreign-born share of children, gives −0.011 SD (0.007) per point with state
and year FE (p = 0.13; −0.002 (0.010) with region-by-year FE). The two agree in size. In the US the
foreign-born share of children barely moved (2007–2019 state mean −0.2 points, SD 0.9), so this
channel cannot have produced a US trend; the US inflow reached schools as second-generation
children, whose share is null in §2. [CALCULATION: 0.00275 × 500 / 100; `derived/naep_estimates.csv`,
`derived/shares_summary.csv`; INFERENCE on the PISA mean and SD]

## 2. State NAEP, absolute and low-stakes (Test 2)

**Data.** NAEP state means for grades 4 and 8, math and reading, 50 states and DC, waves 2003–2019
(nine), with 2022 and 2024 in a separate specification and the voluntary pre-period waves (math
1996 and 2000, reading 1998 and 2002) for pre-trends. Outcomes: white pupils (school-reported
race), non-English-learner pupils, white non-English-learners, and all pupils as a composition
check; standard errors and cell sizes come with each mean. [DATA: `acquire_naep.py` →
`derived/naep_state_long.csv`, NAEP Data Service API, 81,120 rows]

Shares, in percentage points: the Hispanic share of K-12 enrollment (CCD, fall of the tested school
year); English learners identified by NAEP as a percent of the tested grade (NAEP technical
appendices, EL excluded pupils included); children 6–17 with a foreign-born parent (ACS table
B05009, same calendar year). Pooled estimates stack the four grade-subject cells with state-by-cell
and cell-by-year effects and divide scores by the 2019 national student SD of each cell: 31.9 (math
4), 39.8 (math 8), 38.8 (reading 4) and 37.9 points (reading 8). [DATA: `acquire_shares.py` →
`derived/state_shares.csv`; `inclusion/derived/naep_inclusion.csv`; CALCULATION: `panel.py`]

Between the 2003 and 2019 waves the Hispanic share rose 7.8 points in the average state (SD 3.3;
West Virginia +1.4, Nevada +13.8), the NAEP-identified English-learner share of grade-8 math pupils
1.2 points (SD 2.9; Arizona −9.3, Texas +7.4) and, 2007–2019, the immigrant-origin share of children
4.2 points (SD 3.1). A 10-point change is therefore about three standard deviations of the observed
change. Nationally, weighting states by enrollment and averaging the four cells, the English-learner
share went from 8.6% to 10.4%. [CALCULATION: `analysis_naep.py` → `derived/shares_summary.csv`;
enrollment-weighted means from `panel.py`]

A fourth share, the foreign-born share of under-18s (ACS), is estimated alongside and reported in
§1b: −0.110 (0.072) per 10 points, 2005–2019, n 1,628. [CALCULATION: `derived/naep_estimates.csv`]

**Main estimates, white pupils, national student SD per 10 points of the share, 2003–2019:**

| Specification | Hispanic share | English-learner share | Immigrant-origin share (2007–2019) |
|---|---:|---:|---:|
| State and year FE (main) | **+0.087** (0.027) | **−0.035** (0.018) | **−0.019** (0.026) |
| + region × year FE | +0.074 (0.033) | −0.015 (0.021) | −0.002 (0.030) |
| weighted by enrollment | +0.093 (0.039) | −0.080 (0.014) | −0.068 (0.050) |
| + state linear trends | −0.001 (0.048) | −0.009 (0.019) | — |
| first differences | +0.051 (0.023) | −0.007 (0.015) | +0.001 (0.018) |
| long difference, first wave → 2019 | +0.123 (0.036) | −0.028 (0.029) | −0.037 (0.033) |
| + white school-lunch eligibility | +0.084 (0.027) | −0.035 (0.017) | −0.025 (0.026) |
| next wave's share (lead), current held | +0.089 (0.089) | −0.005 (0.017) | — |
| pre-period change on 2003→2019 share change | +0.022 (0.030) | +0.001 (0.020) | — |
| permutation p (2,000 state-label shuffles) | 0.012 | 0.084 | 0.474 |
| with 2022 and 2024 | +0.095 (0.036) | −0.016 (0.023) | −0.020 (0.031) |
| pandemic: 2019→2024 change | +0.155 (0.069) | +0.072 (0.035) | +0.081 (0.066) |

N is 1,818–1,830 state-cell-waves on 51 clusters for the level specifications (1,412 for the
immigrant-origin share, which starts in 2007), 198–204 state-cells for long differences and 152–156
for the pre-period test (46–47 states took part before 2003).
White non-English-learners give the same picture (main: +0.091 (0.027), −0.029 (0.018), −0.017
(0.025)). [CALCULATION: `analysis_naep.py` → `derived/naep_estimates.csv`; permutation:
`analysis_robust.py` → `derived/robust_permutation.csv`]

In NAEP points (main specification, white pupils), the Hispanic share gives +1.5 (1.5) in math 4,
+2.3 (1.3) in math 8, +4.8 (1.3) in reading 4 and +4.6 (1.1) in reading 8; the English-learner share
−0.8 (0.7), −2.1 (1.1), −0.8 (0.7) and −2.3 (1.2); the immigrant-origin share +0.3 (1.3), −1.2 (1.4),
−1.7 (1.1) and −0.5 (1.0). [CALCULATION: same file, per-cell rows]

**Reading the table.**

- *Hispanic share.* White pupils gained, not lost, where the Hispanic share grew. The event study
  shows no pre-2003 difference (pre-period coefficients −3.4 to +0.8 points, all within 1.8 SE) and
  a divergence that grows after 2003, reaching +2 to +7 points per 10 points of share by 2019. All
  pupils' means rose too (+0.066 (0.035)) although Hispanic pupils score below white pupils, so a
  positive trend common to these states sits under every estimate. State linear trends absorb it
  (−0.001 (0.048)). The positive slope is not evidence of a benefit; the absence of a negative one
  is the finding. [CALCULATION: `derived/naep_eventstudy.csv`]
- *English-learner share.* The one negative sign: −0.035 SD (95% CI −0.070 to 0.000), −0.08 with
  enrollment weights, concentrated in grade 8. It halves or vanishes with region-by-year effects,
  state trends, first or long differences, and the permutation p is 0.084. Dropping any one state
  moves it between −0.042 and −0.027. Part of the English-learner share is classification policy
  (Arizona's fell 9 points), and the all-pupil mean falls less than composition alone implies
  (−0.041 against −0.07 to −0.12 if English learners replaced non-learners one for one, given
  national EL–non-EL gaps of 0.74–1.18 SD in 2019). [CALCULATION: `derived/robust_leave_one_out.csv`;
  DATA: national public LEP means in `derived/naep_state_long.csv`; INFERENCE]
- *Immigrant-origin share.* Null in every specification; the widest interval, weighted, runs from
  −0.17 to +0.03.
- *Black pupils* show no relation to any share (Hispanic +0.070 (0.059), English learner −0.026
  (0.028), immigrant-origin +0.011 (0.038), 48 states). [CALCULATION: `derived/naep_estimates.csv`]
- *Heterogeneity.* The 10th percentile of white pupils moves more than the 90th for the
  English-learner share (−0.055 (0.024) against −0.021 (0.017)); for the Hispanic share both rise.
- *Pandemic years.* Between 2019 and 2024 white scores fell less where the shares rose. Those states
  (Texas, Florida and others) also reopened schools earlier, so this row is confounded by closure
  policy and is reported, not interpreted. [INFERENCE]

**Power.** The minimum effect detectable with 80% power in the main specification is 0.078 SD per 10
points for the Hispanic share, 0.050 for the English-learner share and 0.073 for the
immigrant-origin share. Effects of 0.1 SD per 10 points would have shown; effects of 0.02–0.03
would not. [CALCULATION: `mde80` column]

## 3. Exposure accumulated over the cohort's schooling (operator addendum, 2026-09-28)

Grade-8 scores are also related to the share when the same cohort was in grade 4 and to its mean
share over grades K–8; grade-4 scores to the share at K–1. The cohort in grade G in spring t was in
grade g in fall t−1−(G−g). Pooled over math and reading, white pupils, SD per 10 points: [CALCULATION:
`analysis_lags.py` → `derived/lag_estimates.csv`, `derived/lag_coverage.csv`; robustness
`analysis_robust.py` → `derived/robust_lag_el.csv`]

| Exposure measure | Grade | Waves (thinnest wave, states) | Estimate | Contemporaneous, same sample |
|---|---|---|---:|---:|
| Hispanic share of the cohort's own grade, 4 years earlier (CCD by grade) | 8 | 2003–2019 (34) | +0.058 (0.033) | +0.066 (0.033) |
| All-grade Hispanic share, 4 years earlier | 8 | 2003–2019 (48) | +0.072 (0.029) | +0.089 (0.026) |
| Cohort's mean Hispanic share over grades K–8 (CCD by grade) | 8 | 2007–2019 (33) | +0.017 (0.053) | +0.047 (0.049) |
| Mean all-grade Hispanic share over the cohort's K–8 years | 8 | 2005–2019 (47) | +0.065 (0.039) | +0.068 (0.032) |
| Same cohort's NAEP-identified English-learner share in grade 4 | 8 | 2007–2019 (50) | −0.038 (0.027) | −0.049 (0.034) |
| ACS immigrant-origin share of children, 4 years earlier | 8 | 2011–2019 (50) | +0.015 (0.054) | −0.011 (0.029) |
| Cohort's Hispanic share in K–1 (CCD by grade) | 4 | 2003–2019 (34) | +0.060 (0.029) | +0.069 (0.035) |
| Cohort's mean Hispanic share over K–4 (CCD by grade) | 4 | 2003–2019 (34) | +0.067 (0.033) | +0.069 (0.035) |
| All-grade CCD English-learner share in the cohort's K–1 years | 4 | 2003–2019 (26) | **−0.070 (0.030)** | −0.037 (0.016) |
| ACS immigrant-origin share of children in the K–1 years | 4 | 2011–2019 (50) | −0.033 (0.061) | −0.046 (0.037) |

Which lags the data identify: CCD reports race by grade from fall 1998 (34 states; 45 in 2000; all
later), so grade-specific Hispanic lags reach every wave but on 33–34 states in the earliest; the
all-grade share (1995 on) covers all. English learners are not counted by grade in CCD, so the
grade-8 lag uses NAEP's own grade-4 count four years earlier (waves 2007–2019) and the grade-4 K–1
lag uses the all-grade CCD count, which has state gaps: 80 of 1,122 state-years in fall 1998–2019
are missing, among them California in 2006, 2007 and 2010, Pennsylvania through 2005 and New Jersey
in six years. The ACS starts in 2005–2006, so immigrant-origin lags reach only 2011–2019, and a K–8 mean
is not identifiable for it. [DATA: `derived/state_grade_shares.csv`, `derived/state_shares.csv`]

Two results deserve a flag. The grade-4 K–1 English-learner lag is the one clearly negative estimate
in the lane: −0.070 (95% CI −0.130 to −0.011), −0.071 (0.037) with region-by-year effects, −0.068
(0.030) weighted, unchanged without Texas or California, and the next cohort's K–1 share does not
predict the current score (−0.004 (0.024)). The grade-8 English-learner lag is −0.038 (0.027), but
its lead is significant (−0.045 (0.016)), so later cohorts' shares already predict today's scores
and that estimate carries a trend, not a cohort effect. In every horse race the lag and the
contemporaneous share split one effect; the data cannot tell accumulated from current exposure.
[CALCULATION: `derived/robust_lag_el.csv`, `derived/lag_estimates.csv` horse-race rows]

## 4. Lowered standards: NAEP-equivalent cut scores (Test 3)

NCES maps each state's "proficient" cut score onto the NAEP scale (2005, 2007, 2009 from the
2005–2009 comparison study; 2011–2022 from the per-year reports). A lower value is a lower bar on an
absolute scale. The per-year 2009 tables differ from the comparison series by more than 3 points in
10 state-cells (Michigan by 17–44), so they enter only as a robustness row. [DATA: `acquire_mapping.py`
→ `derived/mapping_cut_scores.csv`, 2,048 rows from 26 NCES tables; `derived/standards_2009_overlap.csv`]

States did not lower their standards on average: the mean NAEP-equivalent cut score rose by 15–20
points between 2013 and 2015 in every cell (math 8: 273.8 → 293.3; reading 4: 205.4 → 225.7) and held
through 2022. [DATA: `derived/standards_means.csv`, unweighted means over mapped states; grade-8 math
covers only 31–35 states after 2015]

Nor did states whose shares grew more lower theirs relative to others. SD per 10 points, 2005–2019:
Hispanic share +0.162 (0.213), English-learner share +0.007 (0.100), immigrant-origin share −0.062
(0.139); none moves outside its interval with region-by-year effects, without NCES's high-error
mappings, with 2022, or on 2009–2019 alone; leads are null. In points, the lower 95% bounds are about
−10 (Hispanic), −7 (English learner) and −13 (immigrant origin) per 10 points of share, against a
2013–2015 national rise of 15–20. The test is underpowered for small moves (minimum detectable 0.28–0.61
SD per 10 points) because cut scores jump when states change tests. [CALCULATION: `analysis_standards.py`
→ `derived/standards_estimates.csv`]

## 5. Exclusion from NAEP (Test 4)

**What the rules allow.** ESSA lets a state exclude a recently arrived English learner from one
reading administration and from accountability: "With respect to recently arrived English learners
who have been enrolled in a school in one of the 50 States in the United States or the District of
Columbia for less than 12 months, a State may choose to— (i) exclude— (I) such an English learner
from one administration of the reading or language arts assessment required under paragraph (2);
and (II) such an English learner's results on any of the assessments … for the first year of the
English learner's enrollment in such a school for the purposes of the State-determined
accountability system", or (ii) assess them but count growth in year 2 and proficiency from year 3.
[SOURCE: 20 U.S.C. 6311(b)(3)(A), https://www.law.cornell.edu/uscode/text/20/6311, verbatim in
`inclusion/derived/quotes.md`] That governs state tests, not NAEP. NAEP's own rule since 2010:
"The proportion of all students excluded from any NAEP sample should not exceed 5 percent", and ELs
"in U.S. schools for less than one year should take the assessment if it is available in the
student's primary language" (reading is in English only). [SOURCE: NAGB policy adopted 2010-03-06,
https://www.nagb.gov/content/dam/nagb/en/documents/policies/naep_testandreport_studentswithdisabilities.pdf]

**What happened.** EL exclusion fell everywhere: the state mean share of identified English learners
excluded went from 19.0% (2003) to 5.0% (2019) in math grade 4 and from 31.3% to 9.9% in reading
grade 8; students with disabilities excluded fell from 2.7% to 1.3% and 4.2% to 1.4% of all pupils.
[DATA: `derived/exclusion_means.csv`, from `inclusion/derived/naep_inclusion.csv` (NAEP technical
appendices, 2,674 rows, validated in `inclusion/NOTES_inclusion.md`)]

**Against the share** (percentage points per 10 points of share, state-by-cell and cell-by-year FE):

| Outcome | English-learner share | Hispanic share | Immigrant-origin share |
|---|---:|---:|---:|
| ELs excluded, % of identified ELs | −10.7 (1.8) | −4.8 (5.4) | −6.6 (3.3) |
| ELs excluded, % of all pupils | +0.56 (0.31) | −1.11 (0.25) | +0.20 (0.21) |
| Pupils with disabilities excluded, % of all | −0.99 (0.38) | +0.22 (0.55) | −1.70 (0.61) |
| All excluded, % of all pupils | −0.62 (0.48) | −0.49 (0.59) | −1.54 (0.65) |

[CALCULATION: `analysis_exclusion.py` → `derived/exclusion_estimates.csv`; N 1,496–1,836 on 50–51
states, 2003–2019 (immigrant origin 2007–2019)]

States where English learners multiplied excluded a smaller share of them, not a larger. The small
rise in excluded ELs as a share of all pupils (+0.56) is below what a constant exclusion rate would
produce (about +0.7 at the 2019 mean rate), and exclusion of pupils with disabilities, the only kind
that touches white means, fell. Exclusion cannot mask a decline in the white or non-English-learner
means used in §2: non-learners are never EL-excluded and white English learners are few; adding the
exclusion rates as controls leaves the white estimates at −0.021 to −0.028 (EL) and +0.083 to +0.093
(Hispanic). [CALCULATION: same file, `naep_exclusion_control` rows; INFERENCE]

## 6. Credential inflation (Test 5)

**Graduation against the same cohort's grade-8 NAEP.** State adjusted cohort graduation rates (ACGR,
cohorts 2011–2022, white pupils from 2013) and averaged freshman graduation rates (AFGR, 2003–2013)
come from NCES Digest tables 219.46, 219.35 and 219.40/219.41 and the CCD AFGR table, parsed with
code; the parsed national series equals Digest Table 219.10 in every year. State ACGRs are printed as
whole percentages. [DATA: `credentials/acquire_credentials.py` → `credentials/derived/acgr_state.csv`,
`afgr_state.csv`, `validation_national.csv`] A cohort graduating in spring c sat NAEP grade 8 in
spring c−4; with odd-year waves the usable cohorts are 2011–2021 (ACGR) and 2007–2013 (AFGR). The
rate is regressed on the share with state and cohort FE and the cohort's grade-8 NAEP (mean of math
and reading, in SD) as a control, SEs clustered by state. A positive slope means graduation rose
more than measured achievement where the share rose.

Graduation-rate points per 10 points of share:

| Outcome, cohorts (n) | Hispanic share | Cohort's grade-8 EL share | Immigrant-origin share |
|---|---:|---:|---:|
| White ACGR, 2013–2019 (201–202) | +0.27 (2.95) | −0.04 (2.14) | −0.33 (2.13) |
| White ACGR, 2013–2021 (250–251) | +1.93 (2.86) | +0.16 (2.23) | −1.20 (1.39) |
| All-pupil ACGR, 2011–2019 (249–251) | −0.75 (3.29) | −0.78 (2.00) | +0.44 (1.81) |
| White AFGR, 2007–2013 (188–190) | −2.11 (4.85) | +0.31 (2.36) | −4.33 (3.25) |
| All-pupil AFGR, 2007–2013 (202–204) | +4.49 (3.37) | +0.67 (1.85) | +2.59 (4.09) |

[CALCULATION: `analysis_credentials.py` → `derived/credential_estimates.csv`; 50–51 states]

No slope differs from zero, with or without the NAEP control, and the next cohort's share (a lead)
is null in every row (largest |t| 1.4). The control does its job: the all-pupil ACGR rises 12–15
points per SD of the cohort's grade-8 NAEP (p 0.01–0.07). The test is weak. The minimum effect
detectable with 80% power is 4–9 points per 10 points of share for ACGR and 5–14 for AFGR, because
within-state share changes over four to six cohorts are small. Graduation did not outrun achievement
where the shares rose, but only an inflation above about 6 points per 10 points of share would have
shown. [CALCULATION: `mde80` and `_lead` rows, same file]

The national series shows what a between-state design cannot attribute. The national ACGR rose from
79.0 (2011) to 85.8 (2019) [SOURCE: https://nces.ed.gov/programs/digest/d24/tables/dt24_219.10.asp].
The same cohorts' public-school grade-8 NAEP rose 1.1 points in math and 3.0 in reading between 2007
and 2015, about 0.05 SD, which the panel slope turns into less than 1 point of graduation. Some 6
points of the rise are common to all states: laxer credentials, better retention or the maturing of
ACGR reporting after 2011. Because it is common to every state it carries no information on the
shares. [DATA: national public means in `derived/naep_state_long.csv`; CALCULATION; INFERENCE]

**Exit exams.** Digest Table 234.30 lists 24 states requiring an exit exam for a standard diploma in
its 2013 edition (EPE Research Center, August 2013) and 13 in its 2022 edition (ECS, February 2019).
All 13 are among the 24, so 11 dropped the requirement: AK, AL, AR, AZ, CA, GA, ID, MN, NV, OK, SC.
Texas, Florida, New Mexico, New Jersey, New York and Massachusetts kept theirs. [DATA:
`credentials/derived/exit_exam_digest_snapshots.csv`, parsed with code from
https://nces.ed.gov/programs/digest/d13/tables/dt13_234.30.asp and
https://nces.ed.gov/programs/digest/d22/tables/dt22_234.30.asp]

| Among the 24 states with an exam in 2013 | Dropped (11) | Kept (13) | Permutation p |
|---|---:|---:|---:|
| Hispanic share, fall 2012 (%) | 19.6 | 20.8 | 0.87 |
| Change in Hispanic share, 2002–2012 (points) | +5.8 | +5.9 | 0.99 |
| Change in Hispanic share, 2012–2018 (points) | +2.4 | +3.3 | 0.11 |
| NAEP-identified EL share, 2013 (%) | 7.7 | 6.7 | 0.64 |
| Change in EL share, 2003–2013 (points) | −1.3 | +0.4 | 0.37 |
| Immigrant-origin share of children, 2013 (%) | 20.1 | 22.2 | 0.68 |
| Change in immigrant-origin share, 2007–2013 (points) | +2.0 | +3.2 | 0.10 |

[CALCULATION: `analysis_credentials.py` → `derived/exit_exam_states.csv` and the `exit_exam` rows of
`derived/credential_estimates.csv`; linear probability with HC1 SEs and 2,000 label permutations]

States that dropped the exam did not have higher or faster-rising shares; the states whose shares
rose faster after 2012 tended to keep theirs. A class-by-class exit-exam panel from the CEP, ECS and
FairTest reports was begun by a helper (`credentials/NOTES_credentials.md`) but not finished, so the
timing of each drop within 2013–2019, and the adoptions before 2013, are not tested here.

## 7. District scores linked to NAEP (Test 6, SEDA 6.0)

SEDA 6.0 publishes geographic-district means pooled over grades 3–8 on a cohort-standardized scale:
"Estimates in this scale are comparable across the whole country and over time, but not across
grades or subjects." [SOURCE: SEDA 6.0 codebook, sheet `seda_geodist_annualsub_cs`, Stanford Digital
Repository https://purl.stanford.edu/xh833nn4025, downloaded without an account] Each state's test is
placed on the NAEP scale year by year: "This step uses the state NAEP data to put the estimates from
Step 5 onto a common scale", with NAEP interpolated between the odd tested years and grades 4 and 8
[SOURCE: SEDA 6.0 technical documentation, Steps 5A and 6, `_cache/seda/SEDA_documentation_6.0.pdf`].
A district's mean therefore carries its state's NAEP level. White pupils, math and reading,
2009–2019: 230,837 district-subject-years in 12,070 districts and 49 states
(Hawaii and DC are single districts and absent; Virginia has reading only). Shares come from SEDA's
CCD covariates; between 2009–10 and 2018–19 the district Hispanic share rose 4.1 points on average
(SD 4.8; 90th percentile 10.3). [DATA: `_cache/seda/`; CALCULATION: `analysis_seda.py` →
`derived/seda_estimates.csv`]

Two fixed-effect structures split the variation. District and state-by-year FE keep only change
within a state, the structure of the peer-effect designs. District and year FE also let a statewide
shift through. SD per 10 points of the district share, SEs clustered by state:

| | Hispanic, white pupils | EL, white pupils | Hispanic, all pupils | EL, all pupils |
|---|---:|---:|---:|---:|
| District + state × year FE | −0.017 (0.004) | −0.002 (0.002) | −0.042 (0.003) | −0.005 (0.003) |
| District + year FE | −0.011 (0.007) | −0.005 (0.003) | −0.033 (0.008) | −0.009 (0.004) |
| Difference: the statewide component | +0.006 | −0.003 | +0.009 | −0.004 |
| District + year FE, weighted by tests | −0.020 (0.009) | −0.001 (0.000) | −0.059 (0.009) | −0.002 (0.000) |
| Next year's share, current held (district + year FE) | −0.014 (0.004) | −0.004 (0.002) | −0.020 (0.003) | −0.007 (0.002) |
| Current share in that model | −0.002 (0.006) | −0.004 (0.003) | −0.018 (0.006) | −0.006 (0.004) |

[CALCULATION: `derived/seda_estimates.csv`; n 228,463–245,415 district-subject-years on 49 state
clusters (192,476–210,758 in the lead model, 2009–2018); district-clustered SEs in the `_cl_district`
rows]

Admitting statewide shifts makes the Hispanic estimate for white pupils less negative, not more:
the statewide component is +0.006 SD per 10 points, matching the positive state slope in §2. For the
English-learner share it is −0.003. Within states, white pupils in districts whose Hispanic share
rose lost 0.017 SD per 10 points relative to other districts, but next year's share predicts this
year's score more strongly than this year's share does (−0.014 against −0.002). The within-state
association is therefore a district trend under way before the share rises, which fits families
sorting between districts better than a peer effect. The all-pupil estimates are larger because Hispanic pupils score below
the district mean; that is composition. [INFERENCE]

## 8. Verdict

**Is there a system-wide effect on absolute measures?** Not for the Hispanic or immigrant-origin
share. On NAEP, white pupils gained relative to other states where the Hispanic share rose (+0.087
(0.027) SD per 10 points; lower 95% bound +0.032; −0.001 (0.048) with state trends) and the
immigrant-origin share is null (−0.019 (0.026); lower bound −0.071). SEDA's statewide component is
+0.006 for the Hispanic share. The English-learner share gives the one negative: −0.035 (0.018) per
10 points (p 0.052, permutation p 0.084), which falls to −0.015 (0.021) with region-by-year FE,
−0.009 (0.019) with state trends, −0.007 (0.015) in first differences and −0.028 (0.029) in long
differences. Against the cohort's K–1 share, grade 4 gives −0.070 (0.030), which holds with
region-by-year FE (−0.071 (0.037)) and has no lead. The negative sits at the white 10th percentile
(−0.055 (0.024)) and is absent for non-EL pupils as a whole (+0.016 (0.022)) and for Black pupils
(−0.026 (0.028)). [CALCULATION: §2, §3, §7]

**Do cut scores, exclusions or credentials move?** None moves in the predicted direction. NAEP-
equivalent cut scores are unrelated to the shares and rose 15–20 points nationally in 2015. EL
exclusion from NAEP fell where English learners multiplied (−10.7 (1.8) points of the EL exclusion
rate per 10 points). Graduation did not rise faster than grade-8 achievement where shares rose, but
that test only excludes inflation above about 6 points per 10 points of share. States that dropped
exit exams in 2013–2019 had no higher shares than states that kept them. [CALCULATION: §4–§6]

**Price.** The only candidate is the English-learner share, and it is priced conditionally: if the
main estimate is causal, a 10-point rise costs each white pupil 0.035 SD, $3,154 of lifetime earnings
in present value at age 12 (2024 dollars). The national rise was 1.8 points (8.6% to 10.4%, 2003–
2019), which gives 0.0064 SD, $577 per white pupil and about $1.0bn for each grade cohort of 1.81
million white pupils. The region-by-year estimate gives $0.45bn, the enrollment-weighted one $2.4bn,
the K–1 lag on the CCD share (+1.0 point, fall 2002 to fall 2018) $1.1bn, and the upper end of the
main interval $0. For scale, the adopted main case is $322–387bn a year [SOURCE:
`decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md`, line 75]. [CALCULATION: 0.12 ×
$750,886 = $90,106 per SD per pupil, from `../school_dilution_2026_09_24/derived/pricing_constants.json`
and CFR 2014b's 12% per SD as used by that lane; white pupils per grade = CCD fall 2019 white
enrollment 23.52m ÷ 13, pre-K included so an upper bound; `derived/state_shares.csv`]

**What would falsify the hypothesis, and do the data?** The hypothesis predicts, where shares rose
more: lower NAEP for incumbent pupils, lower NAEP-equivalent cut scores, more NAEP exclusion,
graduation outrunning achievement, and exit exams dropped. A null or opposite sign on all five, with
intervals narrow enough to exclude effects that matter, falsifies it. For the Hispanic and
immigrant-origin shares the data do: the NAEP intervals exclude any decline for the Hispanic share
(lower bound +0.032; −0.10 once state trends are added) and declines larger than 0.07 SD per 10
points for the immigrant-origin share; cut scores do not move, and exclusion and exit exams, if
anything, move the other way.
For the English-learner share they do not: no test excludes an effect of 0.02–0.05 SD per 10
points, and the graduation test cannot exclude moderate inflation.

**What this design cannot see.** Year fixed effects absorb any shift common to every state: a
national curriculum or grading change, or a national response to national immigration. No
between-state or between-district design can attribute such a shift to immigration. The national
record before the pandemic shows no absolute decline to attribute: public-school white NAEP rose
between 2003 and 2019 (grade 4 math +5.8 points, reading +2.2; grade 8 math +4.9, reading +0.8) while
the Hispanic share of public enrollment rose from 18.1% to 27.1% (fall 2002 to fall 2018). Graduation,
by contrast, rose about 6 points more than achievement nationally. That is consistent with the
hypothesis and with several other causes, and nothing here identifies which. [DATA: `derived/naep_state_long.csv`,
`derived/state_shares.csv`; INFERENCE]

## 9. Limits

- The English-learner share is partly classification policy: in the grade-8 math cell Arizona's
  fell 9 points (2003–2019) and California's 6.5 (2007–2019) while their Hispanic shares rose 9
  points each (fall 2002 to fall 2018) and their immigrant-origin shares of children moved by about
  one point. [DATA: `derived/shares_summary.csv`, `derived/state_shares.csv`] Identification and
  reclassification rules that move with the share would bias its slope in either direction.
- White pupils are school-reported race in public schools. Selective exit to private schools or
  other states changes who is measured; controls for white school-lunch eligibility leave the
  estimates unchanged, but parental education is available only for grade 8.
- A trend common to the fast-growing Sunbelt states pushes the Hispanic estimates up; state trends
  remove it and leave intervals of ±0.1 SD per 10 points.
- 2022 and 2024 are confounded by school-closure policy and are reported apart.
- NCES cut-score mappings change with state tests; the test has minimum detectable effects of
  0.28–0.61 SD per 10 points.
- CCD English-learner counts have state gaps (80 of 1,122 state-years in fall 1998–2019, among
  them California in 2006, 2007 and 2010), and district zeros are treated as missing in SEDA.
- NAEP is low-stakes. Low effort would lower scores everywhere; it does not explain differences that
  track shares.
- The helper's class-by-class exit-exam panel was not finished; the exit-exam test uses the two
  code-parsed Digest snapshots only.

## Reproduction

From the repository root, in this order (the Census key is read from the untracked
`infra/immigration-fiscal/acquire/config.local.env`):

```sh
L=infra/immigration-fiscal/school_systemwide_2026_09_27
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acquire_naep.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acquire_mapping.py
(set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a; \
 OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acquire_shares.py)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/acquire_grade_shares.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/inclusion/acquire_inclusion.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/credentials/acquire_credentials.py
# SEDA 6.0 files into $L/_cache/seda/ from https://stacks.stanford.edu/file/druid:xh833nn4025/<file>
for s in analysis_naep analysis_standards analysis_exclusion analysis_lags analysis_robust \
         analysis_credentials analysis_seda; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/$s.py
done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/design_table/build_design_us.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/design_table/build_design_eu.py
```
