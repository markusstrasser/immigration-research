claude-opus-5-5

**Verdict:** On the IPUMS-CPS basic monthly files, G3 non-identifiers close **c = 0.57 (SE 0.26; 5–95% bootstrap
range 0.16–0.98)** of the Mexican-origin identifiers' BA+ gap to third-plus whites, and **0.69 (0.23)** of the
years-of-schooling gap. The files cover January 1994 to August 2026 at months-in-sample 1 and 5.
- **Sample.** The estimate rests on **526 unique G3 non-identifiers aged 25+** (1,286 at 18+), against 325 in the
  ASEC. The ~540 target of carryover_identity §4 is met to within 3%. The brief's plain CPSIDV dedupe gives 539,
  but it counts 1994–95 people twice where IPUMS cannot link them.
- **Corrected step.** In §1's step at a = 0.112, **ρ\* = 0.862 (0.045)**.
- **ASEC frame (second frame).** The ASEC frame gives c 0.56 (0.29) and ρ\* 0.863. The two frames share March
  households and agree.
- **By period.** c is 0.68 (0.27) for 1994–2006, 0.23 (0.40) for 2007–21 and 1.25 (1.21) for 2022–26. Cochran's
  Q = 1.2 (df 2, p = 0.54), so one value fits all three.
- **Sensitivities.** Dedupe, link-rule and union variants give 0.55–0.65. The 2003–26 years alone give 0.72 (0.34),
  1994–2002 gives 0.28 (0.30), and the one- and two-parent frames give 0.81 (0.40) and 0.31 (0.36).
- **Gates.** All pass:
  - the ASEC frame, rebuilt through the monthly loader, reproduces `analyze.py` to 2e-12;
  - in 2022–25 the monthly frame holds 1.5–1.8× the ASEC's unique G3 adults, and 3.2–4.1× outside the ASEC's
    Hispanic oversample;
  - its 2022–25 identifier BA+ gap is −9.6, against −10.1 in the ASEC;
  - identity-loss rates agree by period (|z| ≤ 1.2).
- **c3 candidate.** Pooled with NLSY97 Table 13 by corrected_step's inverse-variance rule, it is 0.56 (0.25) on BA+
  and 0.69 (0.23) on years. The ASEC frame pooled the same way gives 0.54 (0.28) and 0.56 (0.28).
- **Memory.** Peak RSS is 1.6–2.1 GiB across seven runs.

[CALCULATION: `analyze_monthly.py` → `derived/monthly_corrected_step.csv`, `derived/monthly_counts.csv`,
`derived/monthly_period_tests.csv`, `derived/monthly_gates.csv`, `derived/monthly_asec_consistency.csv`,
`derived/c3_candidate.csv`; the ASEC frame: `analyze.py` → `derived/corrected_step.csv`]

[FRAMING-SENSITIVE: every gap is group minus third-plus non-Hispanic whites, age × sex matched in the co-resident
frame (adults 18+ living with a linked parent, mean age of G3 at 25+ ≈ 35–37). c is a proportion and is carried to
the all-adult gap by the same assumption §4 lists.]

# Pooled G3 non-identifier test, IPUMS-CPS basic monthly and ASEC 1994–2026 (2026-10-05)

Question: carryover_identity_2026_09_27 §1/§4 rests on c, the share of the Mexican-origin identifiers' gap to
third-plus whites that G3 non-identifiers close. Its value there is 0.78 (SE 0.64), from 44–55 CPS adults.
- This lane ports Design 1 of `cps_identity.py` first to the 33 ASEC samples of IPUMS extract 4 (§1–§7, the
  second frame).
- It then ports it to 391 basic monthly samples of extract 5 (Basic monthly frame, M1–M7, the lead result).

## Basic monthly frame (M1–M7)

### M1. Data, loading and dedupe

- **Extract.** IPUMS-CPS extract 5 (`extract_monthly.py`) holds 391 basic monthly samples, January 1994 to August
  2026; October 2025 was not fielded. It is case-selected to households at months-in-sample (MISH) 1 and 5.
  - MISH is in the file and takes only the values 1 and 5.
  - There are 11,990,720 person rows in 4,827,378 household-months. [DATA: `derived/monthly_audit.json`]
  - Parents' birthplace (MBPL/FBPL) is on every monthly file. The codes are those of the ASEC extract (DDI
    `_cache/monthly_mis15.xml`). [DATA]
  - No EDUC code is unmapped at 25+, and no analysis row has zero WTFINL. The code checks both and stops
    otherwise. [CALCULATION]
- **Loading.** DuckDB streams the gzipped CSV twice, with a 512 MB memory limit and 2 threads. It keeps the 697,611
  household-months (2,483,100 rows) that hold a Mexico-born parent of anyone, or a white-reference candidate.
  [DATA: `derived/monthly_audit.json`]
  - `classify()` links parents only within a household, so the filter drops no analysis person. Gate 0 checks this
    on the ASEC.
  - Peak RSS ran 1,607–2,126 MiB over seven runs (`/usr/bin/time -l`). About 1.4 GiB is reached while loading, and
    the bootstrap's multiplicity step adds about 0.3 GiB. [DATA: run logs and an instrumented scratch run]
- **Design.** It is `analyze.py`'s, imported: groups, frames, the carry-over lane's age × sex cells and the
  contrasts. Weights are WTFINL.
  - One change to `analyze.py`: `classify()` now takes the sample (year × month), because SERIAL restarts every
    month.
  - The ASEC outputs are unchanged (rerun IDENTICAL, below).
- **Dedupe.** There are 626,268 monthly analysis rows. CPSIDV is never 0, so no row lacks a usable ID.
  [DATA: `derived/monthly_audit.json`]
  - Keeping each CPSIDV's first record drops 183,117 rows (29%), 2,817 of them G3 lineage.
  - IPUMS's person IDs do not link MIS 1 months **June 1994 to August 1995** to their MIS 5 a year later. No adult
    of those months recurs, so the yearly recurrence share is 0.25 for 1994 and 0.18 for 1995, against 0.57–0.67
    in 1996–2025. [DATA: `derived/monthly_linkage.csv`; month list in `monthly_audit.json`]
  - The primary rule therefore also drops those cohorts' 12,255 MIS 5 rows, 13 of them G3 non-identifiers at 25+.
  - The brief's plain CPSIDV rule keeps them (§M3 sensitivities).
- **SEs.** A cluster bootstrap: B = 500, seed 20261006, 399,306 CPSID household clusters over the monthly and ASEC
  rows. The stratum is the cluster's first year. The bootstrap runs on (age × sex cell, cluster) totals, so no
  n × B weight matrix is built. [DATA: `derived/monthly_audit.json`]

### M2. Gates

**Gate 0, the code.** The ASEC frame, rebuilt through this loader and estimator, reproduces `analyze.py`'s published
points. The check covers seven label pairs and 216 cells; every n and reference n is identical, and the largest
gap difference is 2.4e-12. [CALCULATION: `derived/monthly_asec_consistency.csv`]

**Gate 1, 2022–25 counts and gap.** Unique persons in `cores_one`. [CALCULATION: `derived/monthly_gates.csv`,
`derived/monthly_counts.csv`]

| 2022–25 | Monthly | ASEC | Ratio | ASEC outside the oversample | Ratio |
|---|---:|---:|---:|---:|---:|
| G3 lineage, 25+ | 379 | 229 | 1.66 | 97 | 3.91 |
| G3 identifiers, 25+ | 321 | 196 | 1.64 | 79 | 4.06 |
| G3 not Mexican, 25+ | 58 | 33 | 1.76 | 18 | 3.22 |
| G3 not Mexican, 18+ | 142 | 88 | 1.61 | 42 | 3.38 |
| Third-plus whites, 25+ | 17,035 | 6,656 | 2.56 | 5,440 | 3.13 |

- **The ratios sit at the low end of the 1.5–2.5 window**, and lower for the Mexican lineage than for whites.
  - The ASEC adds a Hispanic oversample on top of its March households. IPUMS sets the first-in-sample month of
    those persons' CPSIDP to 13, and they cannot be linked to the monthly files.
  - Checked in 2002–26: 1,639,656 ASEC rows carry month 13, and none of their CPSIDPs occurs in the monthly
    extract, against 96.2% of the other ASEC rows. They are 16.8% Mexican, against 8.5%. [CALCULATION: one-off
    DuckDB check over both extracts, 2026-10-05; not written to `derived/`]
  - Oversample persons are 158 of the ASEC's 325 G3 non-identifiers at 25+ over 1994–2026. [DATA:
    `monthly_audit.json`]
  - Outside the oversample, the monthly frame holds 3.1–4.1× the ASEC's persons. [CALCULATION]
  - That is what the rotation predicts. A March sample sees only households that entered between December and
    March, a third of all entries; the monthly frame sees every household when it enters. [INFERENCE]
- **The identifier BA+ gap in 2022–25 is −9.60 (2.29) monthly**, against −10.10 (2.73) in the IPUMS ASEC without
  dedupe and −10.14 (3.07) in the Census-file design.
  - The differences are +0.50 (SE 3.22, same draws) and +0.55 (3.83), so the gate passes. [CALCULATION]
  - The monthly 2022–25 c is 1.44 (0.95), as high as the ASEC's 1.47 (1.17), which has no dedupe and comes from
    this script's draws. [CALCULATION: `monthly_corrected_step.csv`]
  - [INFERENCE] The recent windows' high value therefore does not come from the ASEC sample alone: the monthly
    frame, with 1.8× the people, shows it too. The two frames share March households.

**Gate 2, identity loss by period.** The weighted share of the G3 lineage not reporting Mexican origin, with the
monthly-minus-ASEC difference taken on the same draws. [CALCULATION: `derived/monthly_gates.csv`]

| Period | Monthly 18+ | ASEC 18+ | z | Monthly 25+ | ASEC 25+ | z |
|---|---|---|---|---|---|---|
| 1994–2006 | 17.6% | 19.2% | −1.16 | 15.7% | 15.5% | 0.12 |
| 2007–2021 | 15.6% | 15.1% | 0.57 | 15.1% | 14.4% | 0.54 |
| 2022–2026 | 15.1% | 14.5% | 0.36 | 14.7% | 12.0% | 1.00 |
| 1994–2026 | 16.1% | 16.2% | −0.14 | 15.2% | 14.3% | 0.86 |

The not-Hispanic share at 18+ is 13.5%, 10.3% and 9.6% by period, and 11.0% overall. [CALCULATION:
`derived/monthly_contrasts.csv`]

### M3. Result

`cores_one`, reference third-plus whites, primary dedupe. [CALCULATION: `derived/monthly_gaps.csv`,
`derived/monthly_contrasts.csv`]

| Measure | n not Mexican | gap identifiers (SE) | gap not Mexican (SE) | c not Mexican (SE) [5–95%] | c not Hispanic (SE) |
|---|---|---|---|---|---|
| **BA+ at 25+** | **526** | −9.00 (0.84) | −3.85 (2.25) | **0.57 (0.26)** [0.16, 0.98] | 0.50 (0.30) |
| BA+ at 22+ | 736 | −10.28 (0.72) | −3.91 (1.89) | 0.62 (0.19) [0.31, 0.94] | 0.55 (0.22) |
| Years at 25+ | 526 | −0.55 (0.05) | −0.17 (0.13) | 0.69 (0.23) [0.32, 1.05] | 0.72 (0.27) |
| Employed at 18+ | 1,286 | −4.80 (0.75) | −4.14 (1.55) | 0.14 (0.36) | −0.06 (0.44) |

Sensitivities on BA+ at 25+. [CALCULATION: `derived/monthly_corrected_step.csv`, `derived/monthly_gaps.csv`]

| Variant | n not Mexican | c (SE) | c on years (SE) |
|---|---|---|---|
| Plain CPSIDV dedupe (the brief's rule) | 539 | 0.58 (0.25) | 0.71 (0.23) |
| CPSIDP dedupe | 525 | 0.57 (0.26) | 0.69 (0.23) |
| No dedupe (person-records) | 765 | 0.57 (0.24) | 0.69 (0.21) |
| MIS 1 only (no linking) | 368 | 0.65 (0.30) | 0.64 (0.27) |
| Rule-11 parent links only | 521 | 0.60 (0.25) | 0.69 (0.23) |
| Exactly one linked parent (`cores_single`) | 205 | 0.81 (0.40) | 0.75 (0.32) |
| Two linked parents (`cores_both`) | 321 | 0.31 (0.36) | 0.49 (0.39) |
| Union with March-basic ASEC persons not in the monthly frame | 551 | 0.55 (0.25) | 0.68 (0.23) |
| Union with the ASEC oversample too (upper bound, may double count) | 709 | 0.61 (0.23) | 0.74 (0.20) |
| 2003–26 only (current HISPAN question) | 375 | 0.72 (0.34) | 0.79 (0.31) |
| 1994–2002 (old "origin or descent" question) | 151 | 0.28 (0.30) | 0.54 (0.30) |

- **Schooling.** BA+ matches the ASEC frame's 0.56. Years run a little higher here, 0.69 against 0.56, within one
  SE. [CALCULATION]
- **Employment.** The non-identifiers' employment gap equals the identifiers' (c 0.14, SE 0.36). [CALCULATION]
  [INFERENCE] In a frame of mostly 18–30-year-olds living with parents, employment mixes school enrolment with
  work, so it is a weak outcome here, as in the ASEC.
- **The frame splits** move the other way from the ASEC's (one-parent 0.40, two-parent 0.57 there). With SEs of
  0.36–0.45 neither split differs from the pooled value. The ASEC's lower one-parent value hinted at the
  step-parent bias suspected in §7; that pattern does not replicate here. [INFERENCE]
- **The union adds 25 March-basic ASEC non-identifiers at 25+.** Of the 183 ASEC non-identifiers at 25+ that it
  cannot match, 158 are oversample persons: their households were interviewed in the monthly CPS, but IPUMS cannot
  link them, so adding them may count people twice. [DATA: `monthly_audit.json`]

### M4. By period

Primary dedupe, `cores_one`, BA+ at 25+. [CALCULATION: `derived/monthly_counts.csv`, `derived/monthly_gaps.csv`,
`derived/monthly_period_tests.csv`]

| Period | G3 lineage, 25+ | Not Mexican, 25+ (18+) | gap identifiers | gap not Mexican | c BA+ (SE) | c years (SE) |
|---|---|---|---|---|---|---|
| 1994–2006 | 1,110 | 217 (486) | −11.39 (1.08) | −3.62 (2.98) | 0.68 (0.27) | 0.92 (0.24) |
| 2007–2021 | 1,376 | 240 (622) | −8.26 (1.14) | −6.39 (3.04) | 0.23 (0.40) | 0.13 (0.40) |
| 2022–2026 | 438 | 69 (178) | −7.54 (2.32) | +1.86 (7.50) | 1.25 (1.21) | 1.85 (1.32) |
| All | 2,924 | 526 (1,286) | −9.00 (0.84) | −3.85 (2.25) | 0.57 (0.26) | 0.69 (0.23) |

- **Heterogeneity tests**, on the same bootstrap draws:
  - BA+: 1994–2006 against 2007–21 is +0.46 (0.48), z = 0.95; 2007–21 against 2022–26 is −1.02 (1.29). Cochran's
    Q = 1.22 (df 2, p = 0.54).
  - Years: 1994–2006 against 2007–21 is +0.78 (0.46), z = 1.71; Q = 3.5 (p = 0.17).
  - BA+ by question period: 1994–2002 against 2003–26 is −0.44 (0.47).
- [INFERENCE] The 2007–21 dip shows in both frames: ASEC −0.02, monthly 0.23. The frames share March households, so
  the agreement is not fully independent. The dip is not significant in either frame.
- [INFERENCE] The identifier gap narrows over time, from −11.4 to −7.5 BA+ points. Later windows therefore divide
  by a smaller gap, which widens their c's SE.

### M5. Identity-loss rate

| Period | Monthly 18+ (SE) | Monthly 25+ (SE) | Not Hispanic, 18+ |
|---|---|---|---|
| 1994–2006 | 17.6% (1.0) | 15.7% (1.3) | 13.5% |
| 2007–2021 | 15.6% (0.8) | 15.1% (1.2) | 10.3% |
| 2022–2026 | 15.1% (1.4) | 14.7% (2.1) | 9.6% |
| 1994–2026 | 16.1% (0.6) | 15.2% (0.8) | 11.0% |

[CALCULATION: `derived/monthly_contrasts.csv`, contrast "share not Mexican"]
- The rates agree with the ASEC's (M2, gate 2).
- Against Duncan–Trejo's 28% for 1994–2006 *children*, adults in both frames run 15–19% over the same years. §5's
  caveat applies: co-residence selects, and the two measure different reporting.
- The decline from 17.6% to 15.1% at 18+ is within about 1.5 SE between the end periods. [CALCULATION]

### M6. Corrected step and the c3 candidate

ρ\* = 0.921 (1 − 0.112 c), with the SE from the delta method, as in §6. [CALCULATION:
`derived/monthly_corrected_step.csv`]

| c source | c (SE) | ρ\* (SE) |
|---|---|---|
| **Monthly 1994–2026, primary** | **0.572 (0.256)** | **0.862 (0.045)** |
| Monthly, plain CPSIDV dedupe | 0.579 (0.249) | 0.861 (0.045) |
| Monthly, MIS 1 only | 0.647 (0.300) | 0.854 (0.048) |
| Union with March-basic ASEC persons | 0.553 (0.249) | 0.864 (0.045) |
| c3 candidate: monthly + NLSY97 | 0.557 (0.246) | 0.864 (0.044) |
| ASEC 1994–2026 (second frame; this script's draws) | 0.563 (0.298) | 0.863 (0.048) |

**c3 candidate** (`derived/c3_candidate.csv`; columns measure, key, source, c, se, n; one row per measure and key):
- **Rule.** It applies the inverse-variance rule of carryover_identity's `corrected_step.pooled_g3`, with T13 and T2
  imported from that lane. The bootstrap SE stands in for the SDR SE, and n counts non-identifiers.
- **Raw rows** carry the SE that enters the weights, the SD of the bootstrap draws (monthly B = 500, ASEC B = 400).
- **Who reads it.** The propagation reads `cps_monthly_1994_2026_raw` and pools it in `pooled_g3()` itself. The
  pooled rows are its check. Recomputed from the CSV, they match to 0.

| key | BA+ c (SE), n | years c (SE), n |
|---|---|---|
| `cps_monthly_1994_2026_raw` | 0.572 (0.256), 526 | 0.686 (0.231), 526 |
| `nlsy97_table13` (G3 cross-section, not Hispanic) | 0.372 (0.884), 11 | 0.719 (1.361), 11 |
| `cps_monthly_1994_2026_pooled` | **0.557 (0.246)**, 537 | **0.687 (0.228)**, 537 |
| `cps_asec_1994_2026_raw` (`analyze.py`'s published c) | 0.563 (0.290), 325 | 0.558 (0.290), 325 |
| `cps_asec_1994_2026_pooled` | 0.545 (0.276), 336 | 0.565 (0.284), 336 |

[CALCULATION; SOURCE for NLSY97: IZA DP12704 Tables 2 and 13, through `corrected_step.py`]
- [INFERENCE] The monthly and ASEC frames overlap in March households and persons, so they must not be pooled as
  independent estimates. The union row is the combined-frame figure.

### M7. Limits

- **The 1994–95 linking break is handled by rule.** The 13 dropped MIS 5 non-identifiers include people never seen
  at MIS 1, such as newcomers to the household, so the primary n is a slight undercount. The plain rule gives
  0.58, and the MIS-1-only rule, which needs no linking, gives 0.65. Both stay within 0.08 of the primary 0.57.
  [CALCULATION]
- **Validated links.** In 1996–2025, CPSIDV recurs 1.7–3.7 points less often than CPSIDP each year (mean 2.5),
  because validation rejects links whose sex, race or age do not fit. Dedupe on CPSIDP changes c by +0.002.
  [DATA: `derived/monthly_linkage.csv`; CALCULATION]
- **Parent pointers** include step and adoptive parents, as in §1 and §7.
- **The HISPAN question changed in 2003**, as in §7.
- **Timing.** Monthly records measure a person at MIS 1 or 5 in any month, the ASEC in March. That is immaterial for
  schooling at 25+. [INFERENCE]
- **The recent windows remain thin.** 2022–26 holds 69 non-identifiers at 25+, so their high c (1.25, SE 1.21)
  cannot be told from the pooled 0.57. [CALCULATION]

The sections below (§1–§7) are the ASEC frame, the second frame.

## 1. Data and the port

- **Extract.** IPUMS-CPS extract 4: cps1994_03s through cps2026_03s, 5,856,362 person rows. The variables are
  in `extract.py`; the file and DDI codebook are in `_cache/`, with sha256 in `derived/audit.json`.
  [DATA: `_cache/asec_pooled.csv.gz`]
- **Codes, read from the extract's DDI** (`_cache/asec_pooled.xml`, fetched by `extract.py ddi`). [DATA]
  - HISPAN Mexican is 100, 102, 103, 104, 108 or 109. Codes 901 and 902 (pre-2003 "do not know" and "no
    response") are unknown, so those people are kept out of the G3 lineage and the white reference.
  - BPL and MBPL/FBPL: Mexico is 20000. US-born is below 15000, which covers 09900 and the territories
    10000–12090.
  - EDUC: BA+ is 111 or above. Years follow the Census A_HGA crosswalk of `cps_identity.py`.
  - EMPSTAT: employed is 10 or 12. Armed forces is 1, the civilian screen.
- **Groups** (mirrors `cps_identity.groups`). [CALCULATION]
  - Native means NATIVITY 1–4.
  - G3 lineage: native, both own parents US-born, civilian, every linked parent US-born, and at least one
    Mexico-born grandparent read from a linked parent's MBPL/FBPL.
  - Identifiers report a Mexican HISPAN code; non-identifiers report something else.
  - Reference: native, both parents US-born, HISPAN 0, RACE 100, civilian.
  - Frames: `cores_one` (≥1 linked parent), `cores_both` (two parents, four grandparents observed) and
    `cores_single` (exactly one linked parent).
- **Parent pointers.** All years use IPUMS's constructed pointers, not Census PEPAR. The brief expected
  Census-provided pointers from 2007 on. In fact, since IPUMS's 2016 revision every year's MOMLOC/POPLOC is built
  by IPUMS from RELATE, and the pointers include step and adoptive parents. [SOURCE:
  cps.ipums.org/cps-action/variables/MOMLOC, "User Caution"; …/MOMRULE, description]
  - The extract has no parent-type variable, so the Census design's biological-only restriction cannot be
    ported.
  - The pre/post-2007 rule split in the brief therefore does not exist. Its nearest analogue is the `direct`
    variant, which keeps only rule-11 links (direct relationship, unique choice). That is 96% of the main
    sample's G3 non-identifier links at 25+ (322 of 325). [DATA: `derived/counts.csv`]
- **Earnings.** INCWAGE (wages and salary) for workers with INCWAGE > 0, deflated to 2024 dollars with the CPI-U
  annual average. [DATA: `ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv`, BLS CUUR0000SA0] The
  Census design used PEARNVAL, all earnings.
- **Weights.** ASECWT. 2014 is halved, because its 3/8 and 5/8 files each sum to the population. [SOURCE:
  cps.ipums.org/cps-action/variables/ASECWT, comparability] The 2020 COVID weight ASECWTCVD is not in the extract
  and is not used; it would move one of 33 years.
- **SEs.** A cluster bootstrap with B = 400 and seed 20261005. A cluster is a CPSID household, covering both of
  its ASEC years; the stratum is the cluster's first ASEC year. Clusters are drawn with replacement within
  stratum, among the clusters holding analysis rows. The reweighting to the group's age × sex mix is redone in
  every draw. This was chosen over Taylor linearization because the age-matched gap and the ratio c are
  awkward to linearize.
- **Dedupe.** CPSIDP keeps each person's first ASEC year. That drops 76,906 analysis rows, 2,001 of them G3
  lineage at 18+. Both the deduplicated and the non-deduplicated results are reported. [DATA: `derived/audit.json`]

## 2. Gate: 2022–25 against the Census-file cells

No dedupe, as in the original. Census = `carryover_identity_2026_09_27/derived/cps_identity_gaps_CPS_ASEC_2022_2025.csv`.
[CALCULATION: `derived/gate_2022_2025.csv`]

| cores_one, BA+ at 25+ | n Census | n IPUMS | gap Census (SE) | gap IPUMS (SE) |
|---|---|---|---|---|
| G2 | 2,356 | 2,334 | −8.82 (1.38) | −8.47 (1.25) |
| G3 lineage | 333 | 345 | −8.75 (3.01) | −8.53 (2.77) |
| G3 identifiers | 289 | 298 | −10.14 (3.07) | −10.10 (2.73) |
| G3 not Mexican | 44 | 47 | +2.35 (9.15) | +4.72 (10.45) |
| G3 not Hispanic | 23 | 26 | −4.63 (13.33) | −0.80 (13.55) |
| c, not Mexican | | | 1.23 (0.94) | 1.47 (1.41) |
| Share not Mexican | | | 0.112 | 0.106 |

- **Counts pass** in the primary frame: they are within 1–7%, and 13% for the 23-person not-Hispanic cell.
- **The non-identifier gaps differ by 2.4 and 3.8 points**, against SEs of 9–13. Three extra people in a 47-person
  cell do that, so it is sampling, not coding. The years and employment cells agree similarly.
  [CALCULATION]
- **`cores_both` runs 9–57% more people** in IPUMS (G3 not Mexican: 32 against 25 at 25+). [CALCULATION]
  - [INFERENCE] IPUMS links a parent's spouse as the second parent. That pulls stepparent-headed households into
    the two-parent frame, which the Census design excludes through PEPAR type ≠ 1.
  - This frame is therefore not the primary one. The pooled c in it is 0.57 (0.36), the same as `cores_one`.
- **Bootstrap SEs run close to the SDR SEs on gaps** (2.77 against 3.01 for G3 lineage) but larger on the ratio
  c (1.41 against 0.94). The bootstrap shows the ratio's heavy tail when the identifier gap is only about 3 SE
  from zero. [CALCULATION]

## 3. Result: pooled c

Frame `cores_one`, reference third-plus whites, deduplicated unless stated. [CALCULATION: `derived/contrasts.csv`,
`derived/gaps.csv`]

| Measure | n non-identifiers | gap identifiers (SE) | gap not Mexican (SE) | c not Mexican (SE) [5–95%] | c not Hispanic (SE) |
|---|---|---|---|---|---|
| **BA+ at 25+** | **325** | −9.25 (0.90) | −4.04 (2.63) | **0.56 (0.29)** [0.08, 1.05] | 0.55 (0.36) |
| BA+ at 22+ | 467 | −9.46 (0.81) | −4.69 (2.30) | 0.50 (0.25) | 0.47 (0.29) |
| Years at 25+ | 325 | −0.54 (0.06) | −0.24 (0.15) | 0.56 (0.29) | 0.72 (0.32) |
| Employed at 18+ | 854 | −3.97 (0.92) | — | 0.45 (0.63) | −0.44 (0.89) |
| Worker wages | 559 | −2,215 (916) | +594 (2,487) | 1.27 (2.91), unstable | 1.64 (4.22) |

Sensitivities on BA+ at 25+:

| Variant | c (SE) |
|---|---|
| No dedupe (475 person-years) | 0.53 (0.30) |
| Direct links only (rule 11) | 0.59 (0.29) |
| Direct links, no dedupe | 0.55 (0.30) |
| `cores_both` | 0.57 (0.36) |
| `cores_single` | 0.40 (0.45) |
| 2003–26 only (current HISPAN question) | 0.71 (0.38) |
| 1994–2002 (old "origin or descent" question) | 0.24 (0.41) |

- **c lies between 0.4 and 0.7 in every variant.** That is above the 0.07–0.27 of the large-sample adult
  non-identifiers in §2 of carryover_identity, and below the 0.78–1.4 of the 2022–26 windows.
- **Employment and earnings cannot pin c.** In this young co-resident frame the identifiers' employment and wage
  gaps are only 2–4 SE from zero, so the ratio is unstable. That matches the original's finding.
- **Earnings use INCWAGE**, the wage concept, not PEARNVAL, so the wage row is not comparable with the Census
  design's earnings row.

## 4. By period

Deduplicated, `cores_one`, BA+ at 25+. [CALCULATION: `derived/counts.csv`, `derived/contrasts.csv`, `derived/period_tests.csv`]

| Period | G3 lineage, 25+ | Not Mexican, 25+ (18+) | gap identifiers | gap not Mexican | c (SE) |
|---|---|---|---|---|---|
| 1994–2006 | 760 | 134 (330) | −9.35 (1.37) | −0.41 (4.08) | 0.96 (0.45) |
| 2007–2021 | 937 | 146 (399) | −8.84 (1.33) | −9.02 (3.49) | −0.02 (0.42) |
| 2022–2026 | 294 | 45 (125) | −10.23 (2.71) | +4.21 (8.80) | 1.41 (1.09) |
| All | 1,991 | 325 (854) | −9.25 (0.90) | −4.04 (2.63) | 0.56 (0.29) |

- **Period differences**, on the same bootstrap draws:
  - 1994–2006 against 2007–21: +0.98 (0.64), z = 1.54;
  - 2007–21 against 2022–26: −1.43 (1.17), z = −1.22.
- [INFERENCE] The swing is consistent with noise around one value, but a real cohort or period shift cannot be
  excluded.
- [INFERENCE] The 2007–21 non-identifiers sit exactly at the identifiers' gap. That is the largest single-period
  sample, and it argues against treating 2022–26's near-parity as structural.
- **2007 is not a pointer break in IPUMS** (§1). The brief's rule-based sensitivity becomes the `direct` variant,
  which changes c by +0.02.

## 5. Identity-loss rate

Here the rate is the weighted share of G3-lineage adults in `cores_one` who do not report Mexican origin.
[CALCULATION: `derived/contrasts.csv`, contrast "share not Mexican"]

| Period | 18+ | 25+ | not Hispanic, 18+ |
|---|---|---|---|
| 1994–2006 | 19.2% (1.3) | 15.5% (1.7) | 14.6% |
| 2007–2021 | 15.1% (0.9) | 14.4% (1.4) | 9.7% |
| 2022–2026 | 14.5% (1.7) | 12.0% (2.1) | 8.2% |
| 1994–2026 | 16.2% (0.7) | 14.3% (1.0) | 10.8% |

- **2022–25 matches the Census design:** 10.6% at 25+ and 11.9% at 18+ here, against carryover_identity's 11.2%
  and 11.0%. The pooled 1994–2026 rate is higher, at 14–16%. [CALCULATION]
- **Against Duncan–Trejo's 28%.** Their figure is the share of 1994–2006 *children* with Mexico-born
  grandparents who are not identified as Mexican, mostly through parents' reports. [DATA: carryover_identity §1
  column header]
  - Adults over the same years run lower: 19.2% at 18+ and 15.5% at 25+. [CALCULATION]
  - The two do not measure the same thing. Co-residence with a parent selects young adults whose parents stayed
    in the household, and the adult answers for themselves or through a household respondent. [INFERENCE]
- **Identity reports barely change between a person's two ASEC years.** Only 17 of 1,980 G3-lineage persons seen
  twice switch, and 53 of 10,108 G2. [CALCULATION: `derived/identity_flux.csv`]
  - [INFERENCE] The CPS likely carries Hispanic origin forward from the first interview (dependent coding), so this stability is probably a
    processing artifact. It is not evidence that identity is stable or that non-identification is not
    measurement noise.

## 6. The corrected step

ρ\* = ρ (1 − a c), with the §1 inputs ρ = 0.921 (SE 0.039) and a = 0.112. The SE uses the delta method and treats
ρ and c as independent. [CALCULATION: `derived/corrected_step.csv`]

| c source | c (SE) | ρ\* (SE) |
|---|---|---|
| **Pooled 1994–2026, dedup** | **0.563 (0.290)** | **0.863 (0.047)** |
| Pooled, no dedupe | 0.532 (0.302) | 0.866 (0.048) |
| Pooled, direct links | 0.585 (0.294) | 0.861 (0.047) |
| 2003–26 | 0.708 (0.378) | 0.848 (0.053) |
| 2022–25 gate (IPUMS) | 1.467 (1.408) | 0.770 (0.149) |
| carryover_identity composite (c = 0.78) | 0.78 (0.64) | 0.841 (0.075) |

- **With the pooled adult rate as a.** At a = 0.143 (§5, 25+), ρ\* = 0.921 (1 − 0.143 × 0.563) = 0.847.
  [CALCULATION, by hand from the table inputs]
- [INFERENCE] The composite in carryover_identity §1 gives c only to the 11.2% G3-rate share. Swapping in the
  pooled 0.56 moves its BA+ central from 0.841 to about 0.863, so the G2 → G3+ step shrinks the gap by about 14%
  rather than 16%.

## 7. Limits

- **Step and adoptive links (not measured).** The IPUMS pointers cannot exclude them.
  - In 2022–25 the primary frame holds 3 more non-identifiers than the biological-only Census design (47 against
    44). [DATA: `derived/gate_2022_2025.csv`]
  - A non-Mexican adult linked to a Mexican-American stepparent would count as a "non-identifier" who looks like
    the reference, which biases c up. The single-parent frame, which excludes spouse-induced links, gives a lower
    c, 0.40 (0.45). [INFERENCE]
- **The HISPAN question changed in 2003.** Before 2003, CPS asked about "origin or descent" from a flashcard. The
  2003+ value (0.71) is the cleaner like-for-like with today's data. [SOURCE:
  cps.ipums.org/cps-action/variables/HISPAN, comparability]
- **540 not reached.** There are 325 unique non-identifiers at 25+, or 475 person-years. The SE target was close
  to met anyway (0.29 against 0.27). More would need the basic monthly files, which carry parents' birthplace
  only in ASEC months, or a restricted linked source (carryover_identity §4). [INFERENCE]
  [2026-10-05 correction: the clause about the monthly files was wrong. They carry MBPL/FBPL in every month since
  January 1994, and the Basic monthly frame above uses them to reach 526.]

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/analyze.py
# then (gate 0 reads analyze.py's derived/gaps.csv; DuckDB is in the project venv, no --with needed)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/analyze_monthly.py
```

- `scripts/rerun_lane.py … "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/analyze.py" --allow-unrun
  {lane}/extract.py` gives **IDENTICAL: 11/11, exit 0** (2026-10-05).
- With the monthly frame (2026-10-05), `scripts/rerun_lane.py infra/immigration-fiscal/g3_identity_pooled_2026_10_05
  "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/analyze.py" "OPENBLAS_NUM_THREADS=1 uv run
  --no-project python3 {lane}/analyze_monthly.py" --allow-unrun
  extract.py --allow-unrun extract_monthly.py` gives **IDENTICAL: 25/25, exit 0**. That run includes `analyze.py`'s
  outputs after the `classify()` signature change.
- `extract.py` is acquisition: `run`, or `download --number 4`, then `ddi --number 4`. It is not part of the
  rerun.
- `extract_monthly.py` is acquisition for extract 5: `download --number 5`, then `ddi --number 5`. It is not part
  of the rerun.

## Repricing the identity-loss rows (withdrawn 2026-10-05)

An earlier `reprice.py` priced the loose-ends note's rows here with c from this lane. It is withdrawn and deleted
(its last version is in 7e22ca7f): it used convention (b), which moves children's costs onto their parents; the
average resident's shared cost as the white end; and only the 0.80M third-generation attriters at the G3 rate,
where the generation-split rule also puts their descendants (1.94M on arm b). The added people are priced on v4's
rules, on the engine, in [main_case_lineage_2026_10_05](../main_case_lineage_2026_10_05/RESULT.md): arm b's 3.04M
add +$18.9 / 26.4bn.
