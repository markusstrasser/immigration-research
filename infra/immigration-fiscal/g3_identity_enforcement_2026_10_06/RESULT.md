claude-opus-5-5

**Verdict:** No drop. Fresh CPS reports of Mexican origin among third-generation (G3) people did not fall when the
2025 enforcement drive began. At MIS 1, the only rotation whose origin report is new, February 2025 – August 2026
against 2022–24 is **−0.6 pp (SE 1.7)** unweighted, −0.1 (1.7) state-mean-weighted and +1.0 (1.7) final-weighted.
February–April 2025 alone is −1.7 (3.4). The Hadah–Denteh frame (White children, any Hispanic origin) gives +0.1
(1.5). Against a 2019–24 linear trend, which rises 0.6 pp a year partly on 2024's series high, the long window is
−2.6 (2.1), at the 13th percentile of the placebo years.
- **Detectable size.** A drop larger than 3.9 pp is excluded at 95% (6.7 pp against the trend). The detectable drop
  (2.8 SE) is 4.8 pp. Power against Hadah–Denteh's 5.9 pp is 0.94 (0.80 against the trend). The February–April 2025
  window alone detects only drops of about 9–12 pp.
- **The ASEC 2025 is insulated by design.** The CPS asks Hispanic origin once, at a household's first interview, and
  carries it forward. In the data, 0.7% of linked G3 persons change Mexican identification between MIS 1 and MIS 5.
  - Only 16–28% of the ASEC 2025's weighted G3 lineage carries a report made after the 20 January 2025 inauguration.
    The rest was reported between May 2023 and January 2025.
  - Its G3 identification is 89.4%, +3.1 pp (SE 1.5) above 2022–24.
  - The ASEC 2026, whose reports are about 70% post-drive, is +2.9 (1.9).
- **For the account.** The point estimate implies 16–29k fewer G3+ identifiers in the ASEC 2025 frame. At ladder
  281's $6,309–8,790 per added person, that is $0.10–0.26bn a year.
  - The 95% bound implies 106–192k fewer identifiers and $0.67–1.69bn. Against the trend the bound is $1.1–2.9bn. On
    February–April 2025 alone, the months whose fresh reports enter the ASEC 2025, it is $1.4–3.5bn. The largest is
    0.8% of the $390–461bn case.
  - p3 is measured on the same file, so arm b would add most such losses back and reprice them, at about half these
    sums.
  - In 2025 the final weights give each G3+ Mexican record 5.5% more weight, relative to G3+ non-Hispanics, than in
    2022–24. That shift is worth about 0.75M people in the frame, more than any identity loss the test allows.
    Whether the shift is right is a separate question (§8).
- **Placebos.** The 2006–24 in-time placebos are calibrated for the long window (SD of z 0.95), and 2025 sits at their
  28th percentile. G2, which the account keys by birthplace, moved −0.4 (0.6). G3 with an Asia-born grandparent
  moved +2.8 (3.1) on Asian race.
- **Gates.** All 35 pass, including an exact reproduction of the pooled lane's published counts. Peak RSS is 0.9 GiB.

[CALCULATION: `analyze.py` → `derived/tests.csv`, `power.csv`, `placebo_summary.csv`, `asec_tests.csv`,
`asec_vintage.csv`, `asec_raking_shares.csv`, `carry_forward.csv`, `sizing.csv`; `stage.py` → `_cache/`]

[FRAMING-SENSITIVE: the dollar sizing reads a fresh-report drop as applying to every G3+ person, and prices it two
ways (§9). The test itself is a before-and-after comparison, not a causal design. A drop would have measured the
drive together with anything else that changed in 2025.]

# Did the 2025 enforcement drive lower Mexican-origin identification among the CPS third generation? (2026-10-07)

Brief (team lead, 2026-10-06). Hadah & Denteh find that Secure Communities lowered parent-reported Hispanic identity
of third-generation White children of Latin-American heritage by 5.9 pp, a 7.4% decline. Their data are the CPS
2004–13, children under 18 in intact families, and the effect is larger among college-educated families. [SOURCE:
hussainhadah.com/research/working-papers/hadah-denteh/immigration_enforcement_hispanic.pdf, April 2026, SSRN 6226541;
the p = 0.002, SE ≈ 0.019 and the −24 pp college figure are the brief's, not checked against the tables] The
account (income year 2024) runs on the CPS ASEC 2025, fielded February–April 2025. The question is whether the drive
lowered Mexican identification in the CPS from February 2025, and whether the ASEC 2025 frame misses G3+ identifiers
as a result.

## 1. Data, groups and timing

- **Data.** No new download was needed. `stage.py` reads the pooled lane's cached IPUMS-CPS extracts. [DATA:
  `g3_identity_pooled_2026_10_05/_cache/`, sha256 in `derived/audit.json`]
  - Extract 5: basic monthly, MIS 1 and 5, January 1994 – August 2026. October 2025 was not fielded.
  - Extract 4: the ASEC 1994–2026.
  - `stage.py` keeps 2003 on, the current Hispanic-origin question. It keeps whole every household that holds a person
    whose mother or father was born in Mexico, Latin America or South/East Asia. That is 494,594 of 3,487,406
    household-months (1,555,716 rows) and 1,021,769 ASEC rows.
  - It also writes three aggregates over all rows (state cells, sample composition, ASEC composition).
  - It ran in 33 s with a peak RSS of 0.8 GB.
- **All MIS.** The cache holds MIS 1 and 5 only. Because origin is carried forward (below), an all-MIS extract would
  add mostly duplicate reports. The ASEC, which holds all eight March rotations, is analysed instead (§7). No new
  extract was requested.
- **G3.** The rule is the pooled lane's `analyze.classify`, imported unchanged: US-born, both own parents US-born,
  civilian, every linked co-resident parent US-born, and a Mexico-born grandparent read from a linked parent's
  MBPL/FBPL.
  - The group covers all ages. The frames are under 18; 18+; White children (Hadah–Denteh); White children with two
    linked parents; and children with and without a BA+ parent.
  - The outcomes are a Mexican HISPAN code, and any Hispanic code.
- **Comparison groups.** The same rule is applied with the parents' birthplace codes recoded before `classify`:
  - G3 with an Asia-born grandparent and no Latin American one; the outcome is any Asian race code.
  - G3 with a Spanish-speaking Latin American grandparent, Mexico included; the outcome is any Hispanic origin.
  - G2: US-born with a Mexico-born parent. [CALCULATION]
- **Timing: origin is asked once.** CPS Technical Paper 77, Table 3-2.7, lists the MIS 5 demographic items: roster
  checks, an education check and a "has anything changed" screen. Race and origin are not re-asked. [SOURCE:
  www2.census.gov/programs-surveys/cps/methodology/CPS-Tech-Paper-77.pdf] The interviewing manual says: "In
  subsequent months you only collect missing information." [SOURCE:
  www2.census.gov/programs-surveys/cps/methodology/intman/CPS_Manual_April2015.pdf]
  - In the data, 85 of 12,657 G3-lineage persons linked from MIS 1 to MIS 5 by CPSIDV change Mexican identification
    (0.67%, 2003–25). Among G2 it is 416 of 78,110. [DATA: `derived/carry_forward.csv`]
  - The 2024 MIS 1 cohort, seen again in 2025, changed 0 of 543. The 2025 cohort changed 5 of 370, and 4 of those
    changed to Mexican.
  - So an MIS 1 record is a fresh report, dated by its interview month. An MIS 5 record from February 2025 to January
    2026 mostly repeats a report made a year earlier, before the drive.
- **Windows.**
  - February–April 2025: ASEC fieldwork, the first months wholly after the 20 January inauguration. [TRAINING-DATA]
    The CPS interviews in the week containing the 19th [SOURCE: NCES Handbook of Survey Methods, CPS,
    nces.ed.gov/statprog/handbook/cps_surveydesign.asp], which in January 2025 was 19–25 January, so January's
    interviews straddle the inauguration.
  - February 2025 – August 2026: 18 fielded months.
  - Baselines: the 2022–24 mean, the same months of 2022–24, and a 2019–24 linear trend. The trend is fitted on the
    baseline alone, and the window gets its own intercept and slope.
- **Weights.**
  - Unweighted.
  - State-mean: summed WTFINL over all persons in the year × month × MIS × state cell. This stands in for the base
    weight, which the extract does not carry (its weights are WTFINL and HWTFINL). [DATA: DDI]
  - Final: WTFINL, raked to national Hispanic totals by age and sex.
- **SEs.** CR1 cluster-robust standard errors, with the CPSID household as cluster. A household's MIS 1 and MIS 5
  records share a cluster.

## 2. Gates

All 35 pass, and the run stops on any failure. [CALCULATION: `derived/gates.csv`]
- **Pooled lane's monthly counts.** The staged rows through `classify` reproduce the pooled lane's published
  `monthly_counts.csv` exactly. The check covers the no-dedupe and MIS 1 rows, 2022–25 and 2022–26, at 18+ and 25+,
  for the lineage, identifiers and non-identifiers. Example: 1,380 / 1,187 / 193 at 18+, 2022–25.
- **Pooled lane's ASEC counts.** The ASEC rows reproduce `counts.csv` for 2022–26 with no dedupe (1,198 / 1,035 / 163
  at 18+).
- **Data checks.**
  - Months are complete from 2003-01, with only October 2025 absent (283 samples).
  - MISH takes only the values 1 and 5.
  - No analysis row has a nonpositive weight, a missing state-mean weight or a missing CPSID.
- **pytest** (`test_enforcement.py`, 9 tests). The positive controls:
  - a planted 6 pp household-level drop is recovered and detected, against both the mean and the trend baselines;
  - the trend design returns a planted −4 pp exactly;
  - the CR1 variance matches the hand formula;
  - the published counts are reproduced;
  - March 2025 of the monthly series is rebuilt from the staged rows.

## 3. Main test: fresh reports (MIS 1)

G3, Mexican origin unless stated. Estimates are window minus baseline in pp, with household-clustered SEs. Counts are
records, then non-identifiers, then households. [CALCULATION: `derived/tests.csv`]

| Frame, weight | Feb–Apr 2025 vs 2022–24 | Feb 2025–Aug 2026 vs 2022–24 | Feb 2025–Aug 2026 vs 2019–24 trend | Window n (not; hh) | 2022–24 n (not; hh), share |
|---|---|---|---|---|---|
| All ages, unweighted | −1.66 (3.36) | **−0.60 (1.70)** | −2.59 (2.10) | 1,429 (208; 739) | 2,895 (404; 1,502), 86.0% |
| All ages, state-mean | −1.52 (3.31) | −0.07 (1.66) | −2.20 (2.10) | | |
| All ages, final | +0.01 (3.12) | +0.99 (1.68) | −0.33 (2.16) | | |
| Under 18, unweighted | −2.53 (3.77) | −0.08 (1.86) | −2.38 (2.32) | 1,137 (160; 606) | 2,365 (331; 1,229), 86.0% |
| Under 18, final | +0.16 (3.34) | +1.72 (1.82) | +0.30 (2.37) | | |
| White children, any Hispanic, unweighted | −3.15 (3.37) | **+0.09 (1.46)** | −1.55 (1.83) | 1,026 (73; 545) | 2,151 (155; 1,118), 92.8% |
| White children, any Hispanic, final | −1.85 (2.78) | +0.35 (1.26) | −0.57 (1.71) | | |

The February–April 2025 window holds 301 records (47 not identifying, 147 households), 242 of them children.

- **Sensitivities, all ages, unweighted, February 2025 – August 2026.**
  - Age × sex and state-group adjustment: +0.13 (1.67); final-weighted +1.68 (1.67).
  - Trend without March–December 2020: −2.67 (2.11).
  - February–April 2025 against the same months of 2022–24: +1.03 (3.89).
- **Subgroups, unweighted, February 2025 – August 2026.**
  - Adults 18+: −2.67 (3.41), 292 records.
  - White children with two linked parents: +1.89 (2.30) on Mexican origin, +0.08 (1.86) on any Hispanic.
  - Children with a BA+ parent: +1.62 (3.92) on Mexican origin and +0.74 (3.29) on any Hispanic (349 records). The
    95% lower bounds, −6.1 and −5.7, exclude the brief's −24 pp college effect.
  - Children without a BA+ parent: −0.46 (2.04).
- **The trend baseline.** Its slope is 0.62 pp a year on 2019–24 and 0.44 on 2019–23. [CALCULATION, by hand: a
  record-weighted fit to `series_monthly.csv`, the same fit as the design's baseline]
  - February 2024 – January 2025 is the highest 12-month MIS 1 rate since 2003, 89.1% (SE 1.4), against 80.3–87.2% in
    the other years. February 2025 – January 2026 is 85.0% (1.8), in the middle of the post-2010 range. [DATA:
    `derived/series_annual.csv`]
  - So the trend test asks whether 2025–26 fell short of a continued rise. Its −2.6 sits at the 13th percentile of the
    placebo years (§5).
- **Final weights.** The final-weighted estimates run 1.6–2.7 pp above the unweighted ones on Mexican origin, and
  0.3–1.3 pp above on the White children's any-Hispanic frame.
  - In the monthly MIS 1 files, the Hispanic to non-Hispanic mean-weight ratio was 1.31 in 2022–24, 1.28 in 2024,
    1.37 in 2025 and 1.42 in 2026. [DATA: `derived/composition_monthly.csv`, means of monthly values]
  - The unweighted Hispanic share of the sample fell from 15.8% (2024) to 15.6% and 15.4%. The weighted share, which
    follows the population controls, rose from 19.3% to 20.2% and 20.5%.
  - Identifiers sit in Hispanic raking cells. A 5–9% rise in their relative weight lifts an 86% share by 0.5–1.0 pp,
    about half the gap. [CALCULATION, by hand] The rest would come from weight differences within the lineage, such
    as by state. [INFERENCE]
  - The unweighted and state-mean tests are therefore the cleaner measures of reporting.

## 4. MIS 5, pooled, and the MIS 1 − MIS 5 contrast

All ages, Mexican origin, unweighted. [CALCULATION: `derived/tests.csv`]

| Records | Window | Estimate (SE) | n (hh) |
|---|---|---|---|
| MIS 5 (reports a year old) | Feb–Apr 2025 | +6.38 (2.65) | 216 (115) |
| MIS 5 | Feb 2025–Jan 2026 (reports from Feb 2024–Jan 2025) | +4.51 (1.66) | 852 (443) |
| MIS 5 | Feb–Aug 2026 (reports from Feb–Aug 2025) | −2.39 (2.58) | 565 (297) |
| MIS 1 + 5 | Feb 2025–Aug 2026 | +0.57 (1.32) | 2,846 (1,302) |
| MIS 1 change minus MIS 5 change | Feb 2025–Jan 2026 | −5.57 (2.56) | 1,764 (911) |

- **MIS 5 in 2025 repeats the 2024 high.** The MIS 5 window of February 2025 – January 2026 is 90.3%. That is the
  February 2024 – January 2025 MIS 1 cohort (89.1%) seen again a year later.
- **What the contrast measures.** The MIS 1 − MIS 5 contrast compares 2025's fresh reports with the 2024 cohort's,
  the series high, not with a stable control.
  - The 12-month MIS 1 rate fell 4.1 pp from 2024 to 2025. That is the largest one-year move since 2003, close to the
    falls of 3.9 pp in 2018 and 3.8 pp in 2022. Moves of 3 pp or more occurred seven times in 2004–24.
    [DATA: `series_annual.csv`]
  - The fall follows the series high and leaves 2025 at an ordinary level (§3). It is not read as a drive effect.
    [INFERENCE]
- **MIS 5 in 2026.** MIS 5 in February–August 2026 carries the reports made in February–August 2025, and it shows no
  significant fall.

## 5. Placebos

**In-time placebos.** The same tests run in every earlier year: February–April of Y, and February of Y through the
window's length, each against Y−3..Y−1, and the long window also against a Y−6..Y−1 trend. [CALCULATION:
`derived/placebo_years.csv`, `placebo_summary.csv`]

| MIS 1, all ages, unweighted | Placebo years | SD of placebo estimates | Mean SE | SD of z | 2025 estimate | Share of placebos ≤ 2025 |
|---|---|---|---|---|---|---|
| Feb–Apr vs mean | 2006–24 | 4.30 | 3.79 | 1.24 | −1.66 | 0.42 |
| Long window vs mean | 2006–23 | 1.63 | 1.75 | 0.95 | −0.60 | 0.28 |
| Long window vs trend | 2009–23 | 1.80 | 2.23 | 0.82 | −2.59 | 0.13 |

- **SE calibration.** The clustered SEs are calibrated for the long window. For three-month windows they run about a
  quarter too small, so the February–April tests are weaker than their SEs suggest.
- **G2.** The account keys G2 by birthplace, so its identification does not enter the count. Hadah–Denteh predict a
  rise ("reactive ethnicity"). On MIS 1, February 2025 – August 2026, the change is −0.38 (0.58), 6,219 records, with
  a 95% interval of −1.5 to +0.8. Its long-window placebo SD of z is 1.09.
- **G3 with a Spanish-speaking Latin American grandparent** (Hadah–Denteh's population). Three quarters of it is the
  Mexican lineage: 1,429 of its 1,906 window records. On any Hispanic origin the change is −0.90 (1.37), and −3.27
  (1.75) against the trend. The trend estimate sits at the 13th percentile of 15 placebo years. White children:
  +0.76 (1.54).
- **G3 with an Asia-born grandparent** (outcome: an Asian race code). The long window is +2.79 (3.14). February–April
  2025 is +19.8 (5.3), above all 19 placebo years.
  - That window rests on 72 records in 43 households, against about 70 households in a typical three months of
    2022–24 (836 in 36 months).
  - It is a small-cell outlier, upward, and it does not suggest a general fall in minority identification.

## 6. Power and the detectable drop

[CALCULATION: `derived/power.csv`; B = 200 planted draws, seed 20261007]

| MIS 1, unweighted | SE | 95% bound on a drop | Detectable (2.8 SE) | Power vs 5.9 pp |
|---|---|---|---|---|
| All ages, Feb 2025–Aug 2026, vs 2022–24 | 1.70 | 3.9 | 4.8 | 0.94 |
| All ages, same, vs trend | 2.10 | 6.7 | 5.9 | 0.80 |
| Under 18, Feb 2025–Aug 2026, vs 2022–24 | 1.86 | 3.7 | 5.2 | 0.89 |
| White children, any Hispanic, vs 2022–24 | 1.46 | 2.8 | 4.1 | 0.98 |
| All ages, Feb–Apr 2025, vs 2022–24 | 3.36 | 8.3 | 9.4 (12 at the placebo SD) | 0.42 (about 0.3 at the placebo SD) |

- **Power** is Φ(5.9/SE − 1.96).
- **Planted drops.** A planted household-level drop of 5.9 pp moves the estimate by −5.7 to −6.1 pp in every
  specification. The design recovers it.
- **Pooling MIS 1 and 5.** The pooled rows have an SE of 1.32, but in 2025 they mix pre-drive reports into the window,
  so they are not the test.
- **Which window bounds the ASEC.** The ASEC 2025's fresh reports were made in February–April 2025, so that window is
  the exact match, and it is weak. The long window has the power but averages 18 months. It bounds a February–April
  effect only if the effect persisted. Hadah–Denteh's did. In their full sample of all generations, effects "occur
  within the first year of implementation, with point estimates becoming more negative over subsequent event-time
  horizons". [SOURCE: Hadah–Denteh, discussion of Figure 2] §9 sizes both windows.

## 7. The ASEC frame

[CALCULATION: `derived/asec_by_year.csv`, `asec_tests.csv`, `asec_vintage.csv`]

- **G3 identification, final-weighted.**

  | Frame | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|
  | All ages | 85.3% | 84.4% | 89.0% | 89.4% | 89.1% |
  | Children | 85.1% | 83.9% | 88.8% | 89.4% | 90.5% |

  - ASEC 2025 minus 2022–24: +3.09 (1.53) at all ages and +3.43 (1.70) for children.
  - ASEC 2026 minus 2022–24: +2.85 (1.88) and +4.55 (1.88).
  - On any Hispanic origin, all ages: +1.50 (1.18) in 2025 and +0.81 (1.34) in 2026.
  - Adults alone (n 254) in 2025: +1.64 (2.97) on Mexican origin, −2.51 (2.53) on any Hispanic.
  - The children's 2025 rate, 89.4% (SE 1.4), sits beside the population lane's p3 of 88.81%, built on the Census
    file with a slightly different rule.
- **When the ASEC 2025's identities were reported** (household's first-in-sample month, from CPSIDP; G3 lineage,
  ASECWT shares).

  | Group | Share of weight | Identification |
  |---|---|---|
  | March MIS 1–2, reports Feb–Mar 2025 | 15.5% | 89.7% |
  | MIS 3, January 2025 | 4.5% | 92.8% |
  | MIS 4–8, December 2023 – December 2024 | 23.9% | 89.3% |
  | Oversample, month coded 13 by IPUMS | 56.1% | 89.0% |

  - **The oversample.** It comes from other months' households. [SOURCE: Technical Paper 77, ASEC sample]
    - For Hispanic households: all eight November rotation groups, and April MIS 1 and 5.
    - For non-Hispanic non-White households and non-Hispanic White households with children: August–October MIS 8,
      November MIS 1 and 5, and April MIS 1 and 5.
    - Only April MIS 1 households, first interviewed in April 2025, report after the drive. They are 1 of 10 Hispanic
      groups and 1 of 7 for the others. The rest first answered between May 2023 and November 2024 (April MIS 5 in
      April 2024).
  - **What the codes show.** IPUMS sets the oversample's month digits to 13 and its year digits to the first ASEC
    whose oversample held the record. [SOURCE: IPUMS CPS Working Paper 2025-01,
    cps.ipums.org/cps/resources/linking/ipums_wp_2025-01.pdf] So the data cannot pick out the April 2025 MIS 1 group.
    - 231 of the 767 G3 oversample records carry 2024: second-year households, whose reports date from 2023–24.
      [DATA: `derived/audit.json`, `records_by_first`] The design makes 41% of oversample households second-year
      (half of the Hispanic groups) [SOURCE: same paper], so some of them failed to link and carry 2025 instead.
      [INFERENCE]
  - **The post-drive share s.** It is 15.5% (low), 21.1% (central, adding one tenth of the oversample) and 28.0% (high,
    adding January and one seventh of the oversample).
- **Within the ASEC 2025.** March MIS 1–2 records against MIS 4–8 records, 2025 against 2022–24, unweighted, give
  +0.75 (5.15) on Mexican origin and −3.52 (4.38) on any Hispanic (189 post records). This is too thin to bound
  anything.
- **ASEC 2026.** About 70% of its reports post-date the drive: 42.5% from March MIS 1–6, plus about six tenths of the
  49.7% oversample (November 2025 MIS 1–4, April 2026 MIS 1 and 5). Its rate is not below 2022–24.

## 8. What the final weights do

**Raking works on totals.** It cannot see a fall in identification within the lineage. It can only re-spread lost
Hispanic weight over the Hispanics who remain. The ASEC and CPS rake to national Hispanic totals by age and sex.
[CALCULATION: `derived/asec_raking_shares.csv`]

- **A switch out of Hispanic identity.** The lost weight is re-spread over all Hispanics in the age × sex cell. In
  the ASEC 2025:
  - 20.9% of it goes back to G3+ Mexican identifiers (31.2% under 18, 16.8% at 18+);
  - 38.0% goes to G1–G2 Mexicans, whom the account counts at their own costs (G1 is reweighted by audit row 4 anyway);
  - the rest goes to other Hispanics.
- **A switch from Mexican to another Hispanic origin** is not offset at all, since there is no Mexican-origin control.
- **The 2025 weights moved for other reasons, and by more.** The mean-weight ratio of G3+ Mexican to G3+ non-Hispanic
  ASEC records was:

  | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|---|---|
  | 0.899 | 0.966 | 0.933 | 0.914 | 0.908 | 0.899 | 0.957 | 0.980 |

  - The weighted IPUMS G3+ Mexican count rose from 13.08M (2024) to 14.34M (2025), +9.6%, on 6,290 and 6,351 records
    (+1.0%).
  - At the 2022–24 mean ratio (0.907), the 2025 count would be about 0.75M lower. [CALCULATION, by hand from the CSV]
  - In the monthly MIS 1 files, the Mexico-born share of sample persons fell from 3.11% (2024) to 2.67% (2025). The
    US-born with a Mexico-born parent fell from 3.38% to 3.06%. The G3 lineage did not fall: 6.89 per 1,000 sample
    persons in 2024, 7.16 in 2025. [DATA: `derived/composition_monthly.csv`]
  - [INFERENCE] One reading is that the raking spread Vintage 2024's larger Hispanic totals, together with the shortfall
    of responding Mexican-born households, over the Hispanics who did respond, US-born G3+ among them. The 2020 ratio
    (0.966), when Hispanic response also fell, fits that reading.
  - This lane does not separate the controls from differential nonresponse. The
    [nonresponse lane](../nonresponse_bias_2026_10_07/RESULT.md) works on ASEC 2025 income bias, a different
    quantity.
- **Answer to the brief.** The final weights would offset about a fifth of an identity loss in the G3+ count (nearly a
  third among children). In 2025 they more than offset it, for reasons unrelated to identity.

## 9. Sizing for the account

A drop d in fresh reports moves the ASEC 2025 identification rate by s × d. It lowers the self-identified G3+ count by
N = s × d × L, with L = 17.43M, arm b's corrected third-plus on the CPS frame. [DATA:
`identity_loss_propagation_2026_09_27/derived/population_arms.csv`] Prices are ladder 281's arm b. [DATA:
`main_case_lineage_2026_10_05/derived/v5_summary.json`] [CALCULATION: `derived/sizing.csv`; central s = 21.1%]

| Drop in fresh reports | d (pp) | ASEC 2025 rate | Identifiers missed (s low–high) | Missing, set ($bn) | Self-corrected, set ($bn) |
|---|---|---|---|---|---|
| Point, long window vs 2022–24 | 0.6 | −0.13 pp | 22k (16–29k) | 0.14–0.19 | 0.08–0.10 |
| Point, long window vs trend | 2.6 | −0.55 pp | 95k (70–127k) | 0.60–0.84 | 0.33–0.44 |
| Point, Feb–Apr 2025 vs 2022–24 | 1.7 | −0.35 pp | 61k (45–81k) | 0.39–0.54 | 0.21–0.28 |
| 95% bound, long window vs 2022–24 | 3.9 | −0.83 pp | 145k (106–192k) | 0.91–1.27 | 0.50–0.67 |
| 95% bound, long window vs trend | 6.7 | −1.42 pp | 247k (181–328k) | 1.56–2.17 | 0.86–1.14 |
| 95% bound, Feb–Apr 2025 vs 2022–24 | 8.3 | −1.74 pp | 304k (223–403k) | 1.92–2.67 | 1.06–1.40 |
| Hadah–Denteh size | 5.9 | −1.25 pp | 217k (160–288k) | 1.37–1.91 | 0.76–1.00 |

The dollar columns are at the central s. The cash columns, and every s, are in `sizing.csv`; cash is 0.68 of the set's
"missing" figures at the low end and 0.82 at the high end.

- **Missing (the brief's first order).** The N fall out of the count and each costs what an average arm-b added person
  costs: $6,309–8,790 on the set, $4,268–7,207 in cash. Assumed:
  - the G3 drop applies to all G3+, including G4+ and adults;
  - no offset from raking;
  - no correction through p3;
  - the missed people sit at the identified G3+ age mix, like arm b's added people.
- **Self-corrected.** p3 = 0.888 is measured on the ASEC 2025's own children, so a frame-wide drop lowers p3 too. Arm b
  then re-adds the N as G3-rate attriters, and the corrected lineage barely moves.
  - What remains is their price: an attriter is priced at (1 − C3) G3+ + C3 W, an identified member at G3+.
  - The difference is $3,489–4,598 a person on the set ($3,101–4,607 in cash).
  - This holds if drive-induced non-identifiers are not selected on schooling, unlike ordinary attriters. [INFERENCE]
  - If the drop fell on children more than adults, p3 would over-correct. If it fell on adults, p3 would
    under-correct.
- **Scale.** Across the s range, the point estimates give $0.1–0.3bn against 2022–24 and $0.4–1.1bn against the trend.
  The weakest bound, February–April's 95% bound at the high s, gives $2.5–3.5bn, at most 0.8% of the $390.3–461.2bn
  case, each end against its own. Section 8's weight shift runs the other way and is larger in people: about 0.75M,
  against at most 0.4M.

## 10. Limits

- **The test.** It compares 2025–26 with earlier years. It is not a causal design, and Hadah–Denteh's 5.9 pp
  (Secure Communities, years after activation) is a reference size, not a prediction for 2025.
- **Who is seen.** Only responding households are seen. Had drive-affected G3 households stopped responding, the test
  would measure responders.
  - The G3 lineage's share of the MIS 1 sample did not fall, so that channel is not visible.
  - The Mexico-born share did fall (§8).
  - Parents' birthplaces are also collected once and could themselves be under-reported. That is not testable here.
- **What is not seen.** The lineage is read through co-resident parents' birthplaces. G3 adults living apart from their
  parents, and all G4+, are not seen. The sizing extends the G3 result to them.
- **Timing of reports.** Reports from people who join a household between MIS 2 and MIS 4 or MIS 6 and MIS 8 are not
  in the extract. The post-drive share of the ASEC oversample comes from the rotation design, not from the data (§7).
  Three ASEC 2025 G3 records carry a first-in-sample month of June 2024, which the 4-8-4 rotation does not produce for
  a March household; they are counted as pre-drive. [DATA: `derived/audit.json`]
- **Base weight.** The state-mean weight stands in for the base weight. It removes the within-state demographic
  raking but keeps the state-level nonresponse and coverage adjustment.

## Reproduction

```sh
uv run --no-project python3 infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/stage.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/analyze.py
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest -p no:cacheprovider \
  infra/immigration-fiscal/g3_identity_enforcement_2026_10_06/test_enforcement.py -q
```

- `stage.py` skips its work when the source sha256 and its SQL sha256 match the recorded ones. `analyze.py` calls it
  first.
- Rerun: see the log.

Derived files:

| File | Contents |
|---|---|
| `tests.csv` | every group × frame × outcome × MIS set × weight × test, with counts |
| `series_monthly.csv` | G3 monthly series, 2019-01 – 2026-08 |
| `series_quarterly.csv` | all groups, quarterly |
| `series_annual.csv` | February–January windows, 2003–25 |
| `placebo_years.csv`, `placebo_summary.csv` | in-time placebos |
| `power.csv` | power and planted drops |
| `carry_forward.csv` | MIS 1 → MIS 5 identity changes |
| `asec_by_year.csv`, `asec_tests.csv`, `asec_vintage.csv` | the ASEC frame |
| `asec_raking_shares.csv` | ASEC weight shares and ratios |
| `composition_monthly.csv` | sample composition and weight ratios by month and MIS |
| `sizing.csv` | §9 |
| `gates.csv`, `audit.json` | gates and run audit, with the ASEC records by first-in-sample code |

## Log

- 2026-10-07: stub written. The cached extracts reach August 2026, so no new IPUMS extract is needed for MIS 1/5.
- 2026-10-07 01:37 JST: `stage.py` writes the lineage households 2003–2026 (monthly 1,555,716 rows in 494,594 of
  3,487,406 household-months; ASEC 1,021,769 rows) and three aggregates to `_cache/`. It took 33 s, with a peak RSS of
  0.8 GB.
- Positive control (a scratch run, since moved into the lane as gates): `analyze.classify` on the staged households
  reproduces the pooled lane's `monthly_counts.csv` row `monthly_nodedup, 2022_2025, 18+` exactly: 1,380 G3 lineage
  and 1,187 identifiers; MIS 1 701; 25+ 550 (MIS 1 290).
- Hispanic origin is collected once per person (sources in §1).
  - The scratch run counted 89 changes in 12,817 linked G3 persons.
  - The lane's `carry_forward.csv` counts 85 in 12,657, because it keeps one MIS 5 record per ID among analysis rows.
    §1 uses the lane's figures.
- 2026-10-07: `analyze.py` and `test_enforcement.py` are written. All 35 gates and 9 tests pass.
- 2026-10-07 02:14 JST: every number in this file checked against `derived/`. Corrections made in the draft:
  - the Latin American lineage is three quarters Mexican, not 87%;
  - the ASEC adults' −2.51 is the any-Hispanic figure;
  - the off-rotation first-in-sample months are 3 G3 records (the draft's 60 counted every staged ASEC 2025 record);
  - moves of 3 pp or more occurred seven times since 2004, not "five times in 2017–24";
  - the trend slope is 0.62 pp a year (0.44 without 2024), not "almost none";
  - the self-corrected bound is 0.50–0.67, and the February–April rows were added to §9.
  - The oversample's year digits (IPUMS Working Paper 2025-01) were added to `audit.json` as `records_by_first`.
    The analysis rerun took 10.4 s, with a peak RSS of 895 MiB.
- 2026-10-07 02:22 JST: reproduction checked twice with `scripts/rerun_lane.py` and the three commands above (stage,
  analyze, pytest). Both runs exited 0 and ended `IDENTICAL: 20/20 files unchanged`.
  - The first run used the staged cache, which `stage.py` skipped on matching hashes.
  - The second rebuilt `_cache/` from the pooled lane's extracts after the old cache was moved aside. The staged
    household files came out byte-identical. The three aggregate files differ only in the last bits of their weight
    sums (at most 1.3e-14 relative, DuckDB's parallel summation), and every derived file is unchanged.
  - pytest: 9 passed. Run without `PYTHONDONTWRITEBYTECODE=1`, pytest writes a `__pycache__/` into the lane; it was
    removed.

## Parent review (2026-10-07)

- The brief's Hadah–Denteh figures are now checked against the paper's images: Figure 2(d) prints "Post avg =
  −0.0590, Pct change = −7.36%, p-value = 0.002", and Figure 4(d) prints "No College Parent: −0.044 (p=0.000) |
  College Parent: −0.240 (p=0.000)". The §3 bound on the college effect stands.
- Rerun by the parent: `scripts/rerun_lane.py` with the three commands above, exit 0, `IDENTICAL: 20/20`.
- §8's weight shift (G3+ Mexican records +5.5% relative weight in the ASEC 2025, about 0.75M people) bears on the
  frame the account prices, not on identification; it is followed up separately.
