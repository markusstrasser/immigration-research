claude-opus-5-5

**Verdict:** Pooling IPUMS-CPS ASEC 1994–2026 puts the G3 non-identifiers' closing share at **c = 0.56 (SE 0.29;
5–95% bootstrap range 0.08–1.05)** on BA+ at 25+. That is 325 unique G3 non-identifiers aged 25+ (475 person-years;
854 unique at 18+), so the ~540 target is **not reached** on unique persons. The SE still lands near §4's 0.27,
because the pooled identifier gap is tight. The 2022–26 recent-year value (0.78–1.4 in carryover_identity) was high
partly by chance: the period values are 0.96 (0.45) for 1994–2006, −0.02 (0.42) for 2007–21 and 1.41 (1.09) for
2022–26. The period differences are not significant (largest z = 1.5).
Years of schooling gives the same c, 0.56 (0.29). Plugged into §1's step at a = 0.112, **ρ\* = 0.863 (0.047)**,
against the composite's 0.841 at c = 0.78. The 2022–25 gate reproduces the Census-file cells closely on the
primary frame (n within 3–7%, identifier gap −10.10 against −10.14). [CALCULATION: `analyze.py` →
`derived/corrected_step.csv`, `derived/counts.csv`, `derived/period_tests.csv`, `derived/gate_2022_2025.csv`]

[FRAMING-SENSITIVE: every gap is group minus third-plus non-Hispanic whites, age × sex matched in the co-resident
frame (adults 18+ living with a linked parent, mean age of G3 at 25+ ≈ 37). c is a proportion and is carried to
the all-adult gap by the same assumption §4 lists.]

# Pooled G3 non-identifier test, IPUMS-CPS ASEC 1994–2026 (2026-10-05)

Question: carryover_identity_2026_09_27 §1/§4 rests on c, the share of the Mexican-origin identifiers' gap to
third-plus whites that G3 non-identifiers close. Its value there is 0.78 (SE 0.64), from 44–55 CPS adults. This
lane ports Design 1 of `cps_identity.py` to the 33 ASEC samples of IPUMS extract 4.

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

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/analyze.py
```

- `scripts/rerun_lane.py … "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/analyze.py" --allow-unrun
  {lane}/extract.py` gives **IDENTICAL: 11/11, exit 0** (2026-10-05).
- `extract.py` is acquisition: `run`, or `download --number 4`, then `ddi --number 4`. It is not part of the
  rerun.

## Repricing the identity-loss rows (parent, 2026-10-05)

`reprice.py` reprices the four rows of the [loose-ends note](../../../notes/immigration-dataset-loose-ends-2026-09-30.md)
by the measured rule: the 0.80M attriters lost at the G3 rate close c = 0.56 of the gap between an identified
G3+ member ($7,724 / $9,771) and the average resident ($2,581 / $3,847); later losses close none. The note had
priced every row at the average resident's cost, using the Duncan–Trejo schooling convention that §2 of
carryover_identity rejects for later losses. [CALCULATION: `reprice.py` → `derived/attriter_pricing.csv`]

| Added people | Count | Note (average cost) | Measured rule | Excess over as many average residents | Per member |
|---|---:|---|---|---|---|
| Third-plus attriters, floor | 0.80M | +$2.1 / 3.1bn | +$3.9 / 5.2bn | +$1.8 / 2.1bn | $9,263 / $10,860 |
| Third-plus attriters, central | 1.81M | +$4.7 / 7.0bn | **+$11.7 / 15.0bn** | +$7.0 / 8.1bn | $9,225 / $10,833 |
| Identity loss past G3, low | 3.03M | +$7.8 / 11.7bn | +$21.1 / 26.9bn | +$13.3 / 15.3bn | $9,183 / $10,803 |
| Identity loss past G3, high | 5.33M | +$13.8 / 20.5bn | +$38.9 / 49.4bn | +$25.1 / 28.9bn | $9,108 / $10,750 |

The added cost is a relabel: these people already sit in the national total, among "everyone else". The rows
answer a lineage question beside the account's birthplace-plus-identification frame, never a correction to it.
The average resident stands in for the white end of c, which is measured against third-plus whites; whites cost
less than the average resident, so the G3-rate rows lean high by a small amount. The 3.03–5.33M rows rest on
unobservable fourth-plus losses and are bounds.
