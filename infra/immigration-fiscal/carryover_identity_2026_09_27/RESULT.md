claude-opus-5-5

**Verdict:** Partly an artifact, worth about a tenth of the ratio; the rest of the stall is real at this
resolution. With the hidden third-plus put back, G2 → G3+ carries over about **0.84 of the BA+ gap** and
**0.82 of the earnings and partial-ledger gaps**, against 0.92 / 0.90 / 0.90 on self-identified CPS data
(SE 0.07–0.09, including the uncertainty in how the hidden compare). The gap to third-plus non-Hispanic whites
then shrinks by about a sixth from G2 to G3+, not a tenth.
- **Where the correction comes from.** A same-sample CPS design (adults living with a parent, G3 defined by a
  Mexico-born grandparent whatever they report) finds 11% of G3 adults do not report Mexican origin, and those
  who do not sit near white parity. The extra losses after G3 that the propagation lane adds (17.5–23% hidden
  instead of 11%) do not move the ratio further. Adults who drop the identity one generation later (the parent
  reports Mexican, the adult child does not) are not ahead of those who keep it; they earn $11–12k less.
- **Bounds.** If every hidden member looked like identifiers, the ratio stays 0.92. If all 17.5–23% looked like
  whites, it falls to 0.71–0.76 on BA+ and 0.69–0.75 on dollars (0.65–0.66 at 28%). No attriter value makes the
  gap vanish.
- **The two attriter conventions describe different people** (§2). The 54–72% dollar share is not a dollar
  measurement of anyone: it is a years-of-schooling share for non-*Hispanic* second-generation adults
  (2003–13), divided by the third-plus gap. At G2, where the same 669 adults are measured on every outcome,
  non-identifiers close 0.17–0.27 of the BA+, years, earnings and ledger gaps alike. The ledger should use a generation-split measured rule (§2).
- **Cohort matters about as much as identity.** The all-ages ratio pools a stall at ages 45–64 (1.06–1.12) with a
  real step at 25–44 (0.87–0.91) and in the NLSY97 birth cohort (0.82–0.83). Cohort explains more of the CPS
  (0.92) against NLSY97 (0.76) difference than attrition does: 0.09 against 0.05 of the 0.16.
- **What remains open.** The central number rests on one noisy input: how G3 non-identifiers compare with
  whites. The pooled estimate closes 0.78–0.91 of the identifiers' gap (SE 0.61–0.64), from 44–55 CPS adults and
  11 NLSY97 adults. About 540 would settle it (§4).

[FRAMING-SENSITIVE: every gap is group minus third-plus non-Hispanic whites, age × sex matched in the same frame;
the dollar measures are worker earnings and the September 5 partial annual ledger, not the adopted account,
which has no white reference. Hidden shares and the composite are [MODEL] inputs; see §4.]

# Is the Mexican-origin stall after G2 real once identity loss is corrected? (2026-09-27)

Brief: [`BRIEF.md`](BRIEF.md) (cf4bc30). Inputs, read-only:
- `../generation_carryover_2026_09_27/` (its CPS code is imported, and its published cells are reproduced
  exactly);
- `../identity_loss_propagation_2026_09_27/derived/population_arms.csv`;
- `../mexican_origin_population_total_2026_09_19/` (arm 3/5 tables, DT papers);
- IZA DP 12704 (NLSY97, via the carry-over lane's `_cache`);
- CPS ASEC 2022–2026;
- ACS 2024 1-year PUMS.

Ratio notation: ρ = gap(G3+) / gap(G2). A value below 1 means the gap shrinks. "Closing share" c is the share of
the identifiers' gap that non-identifiers close: c = 1 − gap(non-identifiers) / gap(identifiers). c = 0 means
like identifiers and c = 1 like whites.

## 1. The corrected step

**Only the G3+ side needs correcting.** The CPS G2 is defined by a Mexico-born parent, with no identification test
(`generation_split_2026_09_20/analyze_cps.py`, `population_masks`). Its non-identifiers are already inside it:
7.0% (SE 0.4) of G2 adults 25–64 do not report Mexican origin, and 2.6% (0.2) do not report Hispanic origin.
[CALCULATION: `cps_identity.py` → `derived/cps_identity_contrasts_CPS_ASEC_2022_2025.csv`]

The brief's "G2 hidden share 1 − 0.9246" therefore adds nobody. Including those people moves the G2 gap by +0.36
BA+ points (SE 0.18) and +$140 (73) on the ledger. Removing them instead gives an identifiers-on-both-sides ratio
of 0.905 (BA+), 0.889 (earnings) and 0.886 (ledger), which is slightly *below* the published ratio. [CALCULATION]

With a the hidden share of the G3+ lineage and c the hidden members' closing share, the lineage G3+ gap is
g3 (1 − a c), so **ρ\* = ρ (1 − a c)**. SEs are 160-replicate SDR, joint across the published gaps and every
CPS-measured c. External c's (ACS, NLSY97) add their own variance by the delta method. Pew and MASP have no SE
and enter as brackets. [CALCULATION: `corrected_step.py` → `derived/corrected_step.csv`]

**CPS ASEC 2022–25, adults 25–64.** Columns are the hidden share a: the CPS G3 rate, propagation (b),
propagation (c) and Duncan–Trejo 1994–2006. [CALCULATION; a values are DATA from the lanes named in the
brief]

| BA+ (published 0.921, SE 0.039) | c (SE) | a 11.2% | 17.5% | 23.0% | 28.2% |
|---|---|---|---|---|---|
| Like identifiers | 0 | 0.921 | 0.921 | 0.921 | 0.921 |
| Measured: CPS G2 adults, not Mexican | 0.24 (0.11) | 0.896 | 0.882 (0.040) | 0.871 (0.042) | 0.859 |
| Measured: ACS Mexican-ancestry write-ins, not Mexican | 0.07 (0.04) | 0.914 | 0.910 | 0.907 | 0.903 |
| Measured: CPS co-resident G3 adults, not Mexican | 1.23 (0.94) | 0.794 | 0.722 (0.154) | 0.660 (0.200) | 0.600 |
| Measured: NLSY97 G3, not Hispanic (n 11) | 0.37 (0.88) | 0.882 | 0.861 (0.147) | 0.842 (0.190) | 0.824 |
| Measured, Pew / MASP (brackets) | 0.13 / 0.03 | 0.908 / 0.917 | 0.900 / 0.916 | 0.894 / 0.914 | 0.887 / 0.912 |
| **Composite**: G3-rate share at the pooled same-sample G3 value (0.78, SE 0.64), later losses like identifiers | — | — | **0.841 (0.075)** | **0.841 (0.075)** | 0.841 |
| Composite, later losses at the measured one-step G4 value | — | — | 0.868 (0.083) | 0.911 (0.144) | 0.953 |
| Like whites | 1 | 0.818 | 0.760 (0.032) | 0.709 (0.030) | 0.661 |

| Worker earnings (published 0.899, SE 0.069) | c (SE) | a 11.2% | 17.5% | 23.0% | 28.2% |
|---|---|---|---|---|---|
| Like identifiers | 0 | 0.899 | 0.899 | 0.899 | 0.899 |
| Measured: CPS G2 adults | 0.17 (0.15) | 0.882 | 0.873 (0.073) | 0.865 (0.076) | 0.857 |
| Measured: ACS write-ins | 0.14 (0.08) | 0.885 | 0.877 | 0.871 | 0.864 |
| Years convention under review, 0.543 / 0.724 | fixed | 0.844 / 0.826 | 0.814 / 0.785 | 0.787 / 0.750 | 0.761 / 0.715 |
| **Composite** (as above; the BA+ pooled G3 value stands in for dollars) | — | — | **0.821 (0.091)** | **0.821 (0.091)** | 0.821 |
| Like whites | 1 | 0.799 | 0.742 (0.057) | 0.693 (0.053) | 0.645 |

| Partial ledger (published 0.902, SE 0.048) | c (SE) | a 11.2% | 17.5% | 23.0% | 28.2% |
|---|---|---|---|---|---|
| Like identifiers | 0 | 0.902 | 0.902 | 0.902 | 0.902 |
| Measured: CPS G2 adults | 0.27 (0.14) | 0.875 | 0.860 (0.049) | 0.847 (0.051) | 0.834 |
| Measured: ACS write-ins (personal income) | 0.18 (0.08) | 0.884 | 0.874 | 0.866 | 0.857 |
| Measured: CPS co-resident G3 (household ledger) | 2.06 (1.10) | 0.694 | 0.577 (0.176) | 0.475 (0.229) | 0.377 |
| Years convention under review, 0.543 / 0.724 | fixed | 0.848 / 0.829 | 0.817 / 0.788 | 0.790 / 0.752 | 0.764 / 0.718 |
| **Composite** | — | — | **0.824 (0.079)** | **0.824 (0.079)** | 0.824 |
| Composite, later losses at the measured one-step G4 value | — | — | 0.784 (0.050) | 0.769 (0.066) | 0.755 |
| Like whites | 1 | 0.801 | 0.745 (0.040) | 0.695 (0.037) | 0.647 |

**Reading the three attriter values.**
- *Like identifiers.* The published 0.92 / 0.90 / 0.90 stands.
- *Measured.* The answer depends on which non-identifiers stand in for the hidden:
  - The adults observed in large samples (CPS G2, ACS write-ins) close 0.07–0.27 and leave the ratio at
    0.86–0.91.
  - The G3 adults observed in the same-sample designs close 0.4–1.4. Pooled, that is 0.78 (SE 0.64). The
    composite gives this value to the G3-rate share of the hidden, the 11.2% that are third-generation or
    descend from third-generation attriters.
  - It gives the extra later losses the identifiers' value, which is what the one-step G4 measurement shows
    (§2). That yields 0.84 / 0.82 / 0.82 at any propagation hidden share, because only the G3-rate share
    moves.
- *Like whites.* 0.71–0.76 on BA+ and 0.69–0.75 on dollars at 17.5–23%.

The co-resident G3 dollar c's are not used as central values. The earnings share is unstable, because
identifiers' earnings among co-resident young workers sit only $5.8k below whites. The ledger in that frame is
the parents' household. [CALCULATION; INFERENCE for the choice]

In levels, the composite puts the lineage G3+ gap at −18.1 BA+ points and −$6,041 on the ledger. The identifier
gaps are −19.8 and −$6,615. [CALCULATION]

**Sensitivity, CPS 2022–26.** Published ratios are 0.936 / 0.933 / 0.926. The composite gives 0.841 / 0.839 /
0.832 (SE 0.070–0.084). Like whites at 17.5–23% gives 0.77–0.72, 0.77–0.72 and 0.76–0.71. The CPS G2 c falls to
0.16 / 0.05 / 0.19, and the co-resident G3 c on BA+ rises to 1.40 (0.85). [CALCULATION:
`derived/corrected_step.csv`, source `CPS_ASEC_2022_2026`]

**Age and cohort, identifiers only** (2022–25 [2022–26]). BA+ ρ is 0.875 (0.042) [0.914 (0.036)] at ages 25–44
and 1.117 (0.098) [1.055 (0.076)] at 45–64. For people born 1979–85 (the NLSY97 cohort ± 1) it is 0.829 (0.079)
[0.824 (0.068)].

Earnings and the ledger follow the same pattern. At 25–44 the ratios are 0.81 and 0.86; at 45–64, 0.99 and 1.01;
for the 1979–85 cohort, 0.67 and 0.80.

At 45–64 the second generation is closer to whites (−17.4 BA+ points, against −22.9 at 25–44), while G3+ sits
near −19.4 to −20.0 at every age. The older-age stall is therefore a comparison with an unusually close
second generation. [CALCULATION: `cps_identity_contrasts_*.csv`, frames `pop_25_44`, `pop_45_64`,
`pop_cohort`; INFERENCE for the reading]

## 2. Which attriter advantage is right

**Traced to source.** [SOURCE/DATA as cited; CALCULATION for the c column]

| Convention in the carry-over lane | Number | Who | Non-identifier definition | Measures | c equivalent |
|---|---|---|---|---|---|
| BA+ δ (`summarize.py` DELTA) | +0.63 pts | MASP adult children, LA/San Antonio families, 1998–2002, n 24 vs 692 | names only Anglo/American | BA+ directly | 0.03 of the CPS G3+ gap |
| | +2.54 pts | Pew 2015–16, US-born of US-born parents 25+, n 34 vs 139 | Hispanic ancestry, separate survey of non-identifiers | BA+ directly | 0.13 |
| | +6.16 pts | NLSY97 G3 cross-section, n 11 vs 65 (Table 13 p.57) | not Hispanic in 1997 | BA+ directly | 0.37 of its own gap |
| Dollar share (`summarize.py` CLOSE) | 54.3% | DT 2017 Table 8: parents of G3 children, CPS 2003–13 | not Hispanic | parents' years (+0.57) ÷ CPS 2025 G3+ adult years gap (1.049) | 0.54 |
| | 72.4% | DT 2017 Table 8: G2 adults, conditional on controls | not Hispanic | own years (+0.76) ÷ 1.049 | 0.72 |

The dollar convention is built in `mexican_origin_population_total_2026_09_19/bounds_coverage_fiscal.py` (arm 5).
That lane applies the years share to its all-age ledger. The carry-over lane then applies the same share to the
partial ledger one for one.
- DT 2017's Table 8 Mexico row reads 12.75 / 0.76 / 0.43 / 13.07 / 0.57 / 0.90. [SOURCE: `dt2017_ilr.txt`
  lines 1189–1228; checked in `verify.py`]
- The 1.049 is the unadjusted gap for self-identified G3+ adults 25+ in CPS 2025.
  [DATA: `arm5_education_selectivity.csv`]

**The same people measured on every outcome.** Non-identifiers are "not Mexican" unless noted. [CALCULATION:
`derived/cps_identity_contrasts_*.csv`, `acs_ancestry_contrasts.csv`; SOURCE for NLSY97]

| Source (non-identifiers) | Generation | BA+ | Years | Earnings | Ledger / income |
|---|---|---|---|---|---|
| CPS G2 adults 25–64, 2022–25 (n 669) | G2 | 0.24 (0.11) | 0.25 (0.13) | 0.17 (0.15) | 0.27 (0.14) |
| same, 2022–26 (n 825) | G2 | 0.16 (0.10) | 0.17 (0.12) | 0.05 (0.13) | 0.19 (0.11) |
| CPS G2, not Hispanic, 2022–25 (n 210) | G2 | 0.37 (0.20) | 0.40 (0.18) | 0.04 (0.19) | 0.29 (0.25) |
| ACS 2024, Mexican ancestry written, US-born 25–64 (n 3,349) | G2 + G3+ | 0.07 (0.04) | 0.14 (0.04) | 0.14 (0.08) | income 0.18 (0.08) |
| CPS co-resident G3, 2022–25 (n 44 at 25+, 97 at 18+) | G3 | 1.23 (0.94) | 0.73 (0.78) | unstable | household 2.06 (1.10) |
| same, 2022–26 (n 55 / 131) | G3 | 1.40 (0.85) | 1.12 (0.76) | unstable | household 1.16 (0.74) |
| CPS co-resident G4, one step, 2022–25 (n 35 / 79) | G4 | −0.86 (1.28) | unstable | −$10.9k (5.2k) vs identifiers | household 0.30 (0.50) |
| same, 2022–26 (n 44 / 99) | G4 | −0.35 (0.57) | −0.26 (0.86) | −$11.8k (4.4k) | household 0.31 (0.39) |
| NLSY97 G3 cross-section, not Hispanic (n 11) | G3 | 0.37 (0.88) | 0.72 (1.36) | — | — |

**Who the non-identifiers are.** [CALCULATION: `derived/cps_identity_composition_*.csv`]
- *G2.* 63% report another Hispanic origin. G2 non-identification is mostly a Mexican parent paired with
  another Hispanic origin, which is why it is weakly selected.
- *Co-resident G3.* 65% have one Mexico-born grandparent, against 37% of G3 identifiers (mean 1.5 against 2.0).
  This is Duncan and Trejo's intermarriage gradient, reproduced on adults.
- *One-step G4.* 91% report not Hispanic and 84% white only, against 89% white only among G4 identifiers. They
  are 6% Black only, against 0.6% of identifiers. Race does not explain their lower earnings. [INFERENCE]

**Answer.** The two conventions cannot describe the same people, and the evidence says which way.
- At G2 the same 669 adults can be measured on BA+, years, earnings and the ledger at once. They close about the
  same share of each gap, 0.17–0.27. The dollar share does not run at two to three times the BA+ share there.
- So 54–72% is not a dollar share of anybody. It is a years advantage of a more selected group, divided by a
  smaller gap:
  - in CPS 2022–25, not-Hispanic G2 adults close 0.40 of the years gap, against 0.25 for not-Mexican ones;
  - DT's +0.76 over the G2 identifiers' own 1.23-year gap would be 0.62, not 0.72.
- The BA+ convention's magnitude (0.03–0.37) matches the direct dollar measurements of adult non-identifiers
  (0.14–0.27).
- It is too low for hidden third-generation members, whom both same-sample designs put higher (pooled 0.78–0.91).

**What the ledger should use.** A generation-split measured rule, not a single share:
- *Third-generation hidden members and descendants of G3 attriters* (the 11.2% G3-rate share): the pooled
  same-sample G3 value, 0.78–0.91, SE about 0.6. [CALCULATION]
- *Later losses* (the extra hidden share the propagation lane adds): the identifiers' values, c ≈ 0. The only
  direct measurement of such adults gives c −0.35 to −0.86 on BA+ and earnings $11–12k below identifiers.
  [CALCULATION]
- Averaged over the whole hidden third-plus, that is an effective c of 0.50 at 17.5% hidden and 0.38 at 23%.
  [CALCULATION: `closing_share` of the pooled composite rows]
- If the ledger keeps one number, it should be a measured one. For adult non-identifiers that is 0.2–0.3; for
  the hidden third-plus as a whole, 0.4–0.5.
- The 54–72% should not be cited as a measurement. It happens to land near the composite's effective value at
  17.5%, but only because two errors offset.

**Consequence for the consumer lanes** (not edited). In the population total's arm 5, the central arm's 1.81M
attriters are all at the G3 rate. Under the split rule that arm moves to its own "fully converged" row: −$6,804
per person and −$290.6bn, against −$6,864 and −$293.2bn with DT selectivity. [DATA: `arm5_fiscal_implication.csv`]

Under propagation (b), the 1.24M later losses would carry the identifiers' −$5,143 each. That gives about
−$297.0bn and −$6,757 per person, against −$294.9bn and −$6,711. [CALCULATION on the arm 5 and population_arms
inputs; FRAMING-SENSITIVE: all-age ledger against third-plus whites]

The lineage cost's arm 2a, 0.4–0.8% of its central, stays within that order. [INFERENCE from the propagation
lane's range]

## 3. A same-sample test

**Design 1: CPS co-resident parent pointers.** The frame is adults 18+ living with at least one linked biological
parent, 2022–25 [2022–26].
- The parent's record gives the grandparents' birthplaces. G3 is defined by a Mexico-born grandparent, whatever
  the adult reports.
- In the same sample the frame contains that G3 lineage, G3 identifiers only (the carry-over lane's G3_obs,
  reproduced exactly), the G2 and third-plus white young adults.
- Whites with an observed Mexico-born grandparent or a Mexican-identifying parent are dropped in a sensitivity
  reference. It moves nothing beyond the third decimal.
- The frame also measures adult attrition directly. 11.0–12.3% [10.6–12.4%] of G3 adults do not report Mexican
  origin, the same as the population lane's 11.2% for children. Adult children whose parent reports Mexican
  origin lose it at 8.1–10.2% per step, close to the civic lane's 12.0% at birth.
- [CALCULATION: `cps_identity.py`, gate 68/68 carry-over cells]

| Same sample, co-resident adults | ρ G2 → G3 lineage | ρ G2 → G3 identifiers | Attrition component (SE) |
|---|---|---|---|
| BA+ at 25+ | 0.99 [0.88] | 1.15 [1.03] | −0.16 (0.13) [−0.15 (0.10)] |
| BA+ at 22+ | 0.74 [0.68] | 0.85 [0.79] | −0.11 (0.10) [−0.11 (0.08)] |
| Years of schooling at 25+ | 1.01 [0.84] | 1.10 [0.95] | −0.09 (0.11) [−0.11 (0.09)] |
| Household partial ledger | 0.40 [0.48] | 0.52 [0.55] | −0.12 (0.06) [−0.07 (0.05)] |

**Design 2: NLSY97 cross-section, from published tables.** The cross-sectional sample did not screen on
Hispanic identification.
- G3 all (24.28% BA+, 13.70 years) against G3 identifiers (23.01, 13.58) moves the G2 → G3 ratio by −0.05 (SE
  0.12) on BA+ and −0.08 (0.17) on years. [SOURCE: DP12704 Tables 2, 12, 13 pp.45, 56–57; CALCULATION:
  `derived/nlsy97_same_sample.csv`]
- On the full sample, removing its 13.0% of non-identifiers gives 0.814 (0.140). Published is 0.762; restoring
  the full 20.6% gives 0.731. [CALCULATION]

In ratio units the attrition component is ρ × a × c. Both designs measure a ≈ 0.11–0.21 directly, so they imply
c ≈ 1.2–1.4 (CPS) and 0.37 (NLSY97). Those feed the pooled value in §1. [CALCULATION]

**NLSY97 microdata: not feasible for this test, account or not.** DGLT's G3 needs the grandparents' country of
birth, which comes from the NLSY97 geocode variables (Appendix A2, footnote 23). The public release records only
whether each grandparent was US-born. [SOURCE: `dp12704.txt`, appendix] Geocode files are released under a
license agreement. [TRAINING-DATA]

**How much of CPS 0.92 against NLSY97 0.76 is attrition** (BA+; SEs in `derived/cps_nlsy_decomposition.csv`):

| Step | ρ | Change |
|---|---|---|
| CPS 2022–25, all ages 25–64, identifiers | 0.921 (0.039) | |
| CPS, born 1979–85 (the NLSY97 cohort) | 0.829 (0.079) | −0.09: cohort |
| NLSY97, G3 identifiers only | 0.814 (0.140) | −0.02: survey and G3 against G3+ |
| NLSY97 as published (13.0% non-identifiers) | 0.762 (0.138) | −0.05: attrition |
| NLSY97, lineage-complete (20.6%) | 0.731 (0.137) | −0.03 more |

About a third of the 0.16 difference is attrition and more than half is cohort. The SEs make these shares
indicative only. NLSY97's own G3+ pooling barely matters on BA+ (0.746). [CALCULATION]

## 4. Verdict, inputs and what would settle it

**The stall at its strongest, stated before testing.**
1. Attrition has fallen by more than half since Duncan and Trejo's data: 11% at G3 now. [DATA: population lane]
2. MASP follows families whatever their identity and finds no G3 progress. [DATA: carry-over lane]
3. DGLT report "very similar patterns" when they rerun their analysis on the attrition-free cross-section alone.
   [SOURCE: DP12704 pp.28–29]
4. In parent-to-child terms, NLSY97's G3 carries 0.91 of their G2 parents' schooling gap. [DATA: carry-over lane,
   `carryover.csv`]

**What survived.**
- Claim 1 holds for adults: the co-resident rates equal the children's.
- Claims 2 and 3 fit a small effect: the attrition components run −0.05 to −0.16.
- Claim 4 is untouched here.
- The stall's weak point is the third generation's non-identifiers, who in the only same-sample adult data sit
  near white parity.
- Its strong point is that later losses are not positively selected.

**Measured inputs:**
- G2 and G3+ identifier gaps, with SDR SEs;
- G2 non-identifier shares and closing shares;
- adult non-identification rates at G3 (co-resident, 11%) and one step past G3 (8.1–10.2%), and their closing
  shares (small n);
- ACS write-in closing shares;
- NLSY97 Tables 2, 12 and 13.

**Assumed inputs:**
- The hidden share of adult G3+. The propagation lane's 17.5–23% extrapolates a birth-stage loss; 11.2% and
  28.2% are brackets.
- The hidden resemble the non-identifiers these windows see: G3 co-resident young adults and NLSY97 30-year-olds
  for the G3-rate share, and one-step G4 adults for later losses.
- A closing share measured in one frame carries to adults 25–64 as a proportion of the gap.
- The composite's split: the first 11.2% of the hidden share is G3-type and the rest is later losses.
- The BA+ pooled G3 value stands in for dollars.

**What would settle it.**
- About 540–550 G3 non-identifiers aged 25+ in a design that finds G3 by grandparents' birthplace. That brings
  SE(c) to 0.27, enough to tell c = 0.25 from c = 1 at 80% power. Today there are 44–55, and ASEC adds about 11
  a year. [CALCULATION]
- Candidate sources:
  - CPS basic monthly files, if they carry the same parent pointers and parents' birthplace (not verified here).
    They would supply schooling and employment but no ledger.
  - IPUMS-CPS ASEC 1994–2025 re-extracted with MOMLOC/POPLOC. The staged `cps_2ndgen` extract has no pointers,
    and the extract needs the operator's IPUMS login.
  - The NLSY97 geocode file, licensed and small (79 at G3).
  - Restricted census-administrative linkages.
- For the later losses, a larger one-step G4 sample from the same designs.

## Limits

- The co-resident frames hold young adults living with a parent. The comparison is symmetric, because whites
  are drawn from the same frame, but it does not represent all adults. Their ledger is the household's, mostly
  the parents'.
- Identity in CPS is usually reported by the household respondent. The hidden-share measurements use the same
  report.
- Pooled ASEC years share households, so n counts person-years. SEs use a common replicate index, and
  classification error is not in them.
- "Mexico-born" parents and grandparents include a small non-Mexican-ethnic minority, such as US citizens born in
  Mexico. They can sit in the non-identifier cells. [INFERENCE]
- ACS has no parents' birthplace, so the write-ins' generation is unknown. Its reference is US-born non-Hispanic
  white alone, which includes second-generation whites. It reveals only non-identifiers who still write a
  Mexican ancestry.
- NLSY97 SEs treat published gaps as independent. The full-sample reconstruction assumes every non-identifier is
  in the cross-section at its mean.
- The CPS G3+ includes G4+, and the propagation's hidden shares are all-age population shares applied to adults.

## Files

Covered:
- `cps_identity.py`: CPS gaps, contrasts and composition, with a gate against the carry-over lane's published
  cells.
- `acs_ancestry.py`: ACS write-ins.
- `corrected_step.py`: corrected ratios, the NLSY97 reconstruction and the decomposition.
- `verify.py`: 32 checks; PASS, rc 0.
- Outputs in `derived/`:
  - `cps_identity_{gaps,contrasts,composition,audit}_CPS_ASEC_2022_202{5,6}.*`
  - `acs_ancestry_{gaps,contrasts,audit}.*`
  - `corrected_step.csv`, `nlsy97_same_sample.csv`, `cps_nlsy_decomposition.csv`
- Logs are in `logs/`.

Skipped:
- NLSY97 microdata, for the reason in §3.
- IPUMS-CPS and the CPS basic monthly files, which need an extract revision or an acquisition lane.
- GSS: it screens every generation on Mexican identification and has only a generic grandparent count, so it
  cannot hold the sample fixed.
- Re-running the consumer lanes, which the brief puts out of scope.

Judgment calls:
- The CPS G2 is not corrected, for the reason in §1.
- The composite's split of the hidden share.
- The BA+ pooled G3 value stands in for dollars.
- The co-resident dollar c's are excluded from the central value.
- NLSY97's not-Hispanic definition enters the pooled value alongside CPS's not-Mexican one.
- 2022–25 is primary, to match the published ratios.

Reproduce, from the repository root (about 10 minutes; the first ACS run extracts 1.10M records from the
PUMS zip to `_cache/`):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_identity_2026_09_27/cps_identity.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_identity_2026_09_27/cps_identity.py --years 2022,2023,2024,2025,2026 --label CPS_ASEC_2022_2026
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_identity_2026_09_27/acs_ancestry.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_identity_2026_09_27/corrected_step.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/carryover_identity_2026_09_27/verify.py
```

Two full runs leave `derived/` byte-identical: the SHA-256 lists differ in nothing. Imports from other lanes set
`sys.dont_write_bytecode`, so no upstream file is written.

## Progress log (appended as computed)

- Brief premise checked. The CPS G2 is native with a Mexico-born parent, with no identification test. Its
  non-identifiers are already inside it: 7.0% (SE 0.4) of G2 adults 25–64 do not report Mexican origin and 2.6%
  do not report Hispanic origin (CPS ASEC 2022–25).
  [CALCULATION: `cps_identity.py` → `derived/cps_identity_contrasts_CPS_ASEC_2022_2025.csv`]
  - Only the G3+ side of the step needs the hidden share.
  - Removing G2's non-identifiers instead gives the identifiers-on-both-sides ratio, 0.905 on BA+ (published
    0.921). [CALCULATION]
- Gate: `cps_identity.py` reproduces all 68 gap/SE/n cells the carry-over lane published for its groups (pop and
  both co-resident frames), to 1e-9. [CALCULATION: `derived/cps_identity_audit_*.json`]
- The two attriter conventions traced to source (detail in section 2):
  - BA+: +0.63 (MASP, n 24), +2.54 (Pew, n 34) and +6.16 (NLSY97 Table 13, n 11) points, measured directly on
    non-identifiers. [SOURCE/DATA as cited in `generation_carryover_2026_09_27/summarize.py` DELTA]
  - Dollars, 54.3–72.4%: no dollar measurement. `mexican_origin_population_total_2026_09_19/
    bounds_coverage_fiscal.py` (arm 5) divides Duncan–Trejo 2017's years-of-schooling advantage of
    non-*Hispanic* identifiers by the CPS 2025 G3+ adult years gap (1.049, not age-matched). The advantage is
    +0.76 for G2 adults and +0.57 for G3 children's parents (CPS 2003–2013, conditional on controls; Table 8
    p.23). The carry-over lane applies that years share to dollars one for one. [SOURCE: `dt2017_ilr.txt` lines
    1189–1228; DATA: `arm5_education_selectivity.csv`]
- First direct dollar measurements of the same people (the share of the identifiers' gap the non-identifiers
  close, "not Mexican"):
  - CPS G2 adults 25–64 (n 669): BA+ 0.24 (0.11), years 0.25 (0.13), worker earnings 0.17 (0.15), partial
    ledger 0.27 (0.14). With 2026 added: 0.16, 0.17, 0.05 and 0.19. [CALCULATION]
  - ACS 2024, US-born adults 25–64 who write a Mexican ancestry but do not report Mexican origin (n 3,349; 5.0%
    of Mexican-ancestry US-born): BA+ 0.07 (0.04), years 0.14 (0.04), earnings 0.14 (0.08), personal income
    0.18 (0.08). [CALCULATION: `acs_ancestry.py` → `derived/acs_ancestry_contrasts.csv`]
  - CPS co-resident G3 (grandparent born in Mexico, own report ignored; adults 18+ living with a parent;
    n 44–97): 10.6–12.4% do not report Mexican origin, the same as the children's 11.2%. They close 1.2–1.4 of
    the gap on BA+ (SE 0.85–0.94), at or above white parity. [CALCULATION]
- Extended the same-sample design one generation, using the NLSY97 definition of G4+: four US-born
  grandparents, and the person or a linked parent reports Mexican origin. 8.1–10.2% of such adult children do
  not report Mexican origin. They are not ahead of G4 identifiers: BA+ −4.7 to −8.7 points (SE 6.7–7.4), worker
  earnings −$10.9k to −$11.8k (SE 4.4–5.2k). [CALCULATION]
- Age split and cohort. The identifiers' BA+ ratio is 0.87 at 25–44 and 1.12 at 45–64, and 0.83 for people born
  1979–85. [CALCULATION]
- Composite with the pooled same-sample G3 value (inverse-variance CPS co-resident + NLSY97: 0.78, SE 0.64):
  0.841 BA+, 0.821 earnings, 0.824 ledger (2022–25). [CALCULATION]
- Two full reruns byte-identical; `verify.py` PASS. [CALCULATION]
