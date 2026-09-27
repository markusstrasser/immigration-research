claude-opus-5-5

# Civic attachment and group dissolution by generation, Mexican origin (2026-09-27)

**Verdict:** Civic convergence is partial and slower than full assimilation would need. Each
generation keeps roughly two-thirds to four-fifths of the previous generation's raw civic gap
against US-born non-Hispanic whites. At equal age, sex, schooling, income and state, the voting
gap stops shrinking after the second generation. Citizens voted at 42.6% (naturalized Mexico-born),
43.2% (G2) and 47.4% (G3+), against 66.7% for whites (mean of 2020, 2022 and 2024). The raw gaps
are −24.1, −23.5 and −19.3 points; at equal SES and state they are −12.7, −9.8 and −9.4
(ρ G2→G3+ 0.96). CPS over-reports Hispanic turnout more than white turnout, so the true gaps are
larger. In-marriage falls steadily. The share with a Mexican-origin spouse is 90.2%, 72.3% and
55.9% among married people aged 25–54. The excess over random matching within the state is 68, 47
and 31 points (ρ 0.69 and 0.67 raw; 0.79 and 0.71 at equal schooling and state). Children of
Mexican-origin × non-Hispanic couples are reported Hispanic 83.6% of the time. Weighted by couple
type, the loss per generation at birth is 9.0% (Hispanic) or 12.0% (Mexican) for children of G3+
parents. Identity keeps decaying after G3, so the lineage model's 0.888 at G4+ is too high. Volunteering and giving gaps shrink by 40–60% at
equal SES and still persist at G3+: volunteering −6.0 and giving −7.6 points, with ρ G2→G3+ about
0.6–0.7 both raw and adjusted. The veteran gap among men is a first-generation eligibility gap.
It is gone at equal SES by G2, and US-born women and young US-born men now serving are at parity.
On the same code, India-born spousal endogamy is 96.3% (Mexico-born 90.2%). It falls to 65.5% in
the Indian second generation, against 72.3% in the Mexican second generation.
[DATA] [CALCULATION] [INFERENCE] [SOURCE]

Brief: [`BRIEF.md`](BRIEF.md). Scripts: `voting.py`, `asec_intermarriage.py`, `carryover.py`, `identity_loss.py`,
`verify.py` (all gates pass: Sept volunteering 10.9/15.1/19.7 reproduced; turnout within 0.05
points of P20 Table 1 each year; spouse linkage 100%; carry-over table reproduces from its source
CSVs). A full rerun of all three builders wrote byte-identical `derived/` files.

## 1. Voting and registration (CPS November 2020, 2022, 2024) [DATA] [CALCULATION] [SOURCE]

Script `voting.py`; outputs `derived/voting.csv`, `derived/voting_nonresponse.csv`,
`derived/gate_turnout_published.txt`. Inputs: Census public-use fixed-width files `novYYpub.dat`
read at the positions in the technical documentation `cpsnovYY.pdf` (PES1/PES2 sit two bytes
earlier in 2020), checked against the documentation's unweighted tallies of PES1 and PES2 each year.
Replicate weights `nov22rep.dat`, `nov24rep.dat` (160 SDR replicates) joined on QSTNUM + OCCURNUM;
Census ships none for 2020, so 2020 SEs are the sandwich SE times the mean replicate/sandwich ratio
of the same cell in 2022 and 2024. November samples two years apart share no households (4-8-4
rotation), so the pooled rows (equal-weight mean of the three elections) carry
SE = √Σvar / 3.

**Gate (passes).** All citizens 18+, Census convention: 2020 voted 66.77 vs published 66.8,
registered 72.67 vs 72.7; 2022 52.20 vs 52.2 and 69.12 vs 69.1; 2024 65.35 vs 65.3 and 73.62 vs
73.6 [SOURCE: P20 Table 1, https://www2.census.gov/programs-surveys/cps/tables/p20/585/table01.xlsx,
https://www2.census.gov/programs-surveys/cps/tables/p20/586/vote01_2022.xlsx,
https://www2.census.gov/programs-surveys/cps/tables/p20/587/vote01_2024.xlsx]. Weighted citizen
totals equal the published 231,593k / 233,546k / 236,138k.

**Rates, citizens 18+, % (SE).** G1 here is naturalized Mexico-born citizens only.

| Group | n (3 yrs) | voted 2020 | 2022 | 2024 | voted, mean of 3 | registered, mean of 3 |
|---|---:|---:|---:|---:|---:|---:|
| Mexico-born naturalized (G1) | 2,953 | 49.7 (1.9) | 33.7 (1.9) | 44.5 (1.8) | **42.6** (1.1) | 54.8 (1.2) |
| Mexican G2 | 5,834 | 51.7 (1.4) | 32.4 (1.4) | 45.5 (1.3) | **43.2** (0.8) | 57.3 (0.8) |
| Mexican G3+ | 5,932 | 52.7 (1.5) | 39.2 (1.4) | 50.4 (1.6) | **47.4** (0.9) | 60.2 (0.9) |
| US-born NH white | 159,945 | 71.2 (0.3) | 58.0 (0.3) | 70.8 (0.4) | **66.7** (0.2) | 76.1 (0.2) |
| India-born naturalized | 1,034 | 78.7 (2.8) | 47.0 (3.5) | 76.4 (3.2) | 67.4 (1.8) | 79.5 (1.8) |
| Indian G2 | 544 | 63.8 (4.1) | 48.1 (4.5) | 59.9 (4.3) | 57.3 (2.5) | 67.9 (2.6) |

**Gaps vs US-born NH whites, points (SE), mean of three elections:**

| Measure | Adjustment | G1 nat. | G2 | G3+ |
|---|---|---:|---:|---:|
| Voted | raw | −24.1 (1.1) | −23.5 (0.8) | −19.3 (0.9) |
| Voted | age, sex, education, family income | −11.5 (1.1) | −8.8 (0.8) | −8.9 (0.8) |
| Voted | + state, metro | −12.7 (1.1) | −9.8 (0.8) | −9.4 (0.9) |
| Registered | raw | −21.3 (1.2) | −18.8 (0.8) | −15.9 (0.9) |
| Registered | age, sex, education, family income | −10.0 (1.1) | −7.8 (0.8) | −8.0 (0.9) |
| Registered | + state, metro | −10.2 (1.2) | −8.0 (0.9) | −8.1 (0.9) |
| Voted, responders only (Hur–Achen) | raw | −26.3 (1.2) | −24.1 (0.9) | −19.0 (0.9) |
| Voted, responders only | + state, metro | −13.7 (1.3) | −9.7 (0.9) | −8.4 (0.8) |

Presidential years only (2020, 2024): voted raw −23.9 / −22.4 / −19.5, at equal SES −11.1 / −9.4
/ −10.2. Per-year rows are in `derived/voting.csv`.

**Reading.** Turnout converges slowly and only partly. About half of the G3+ gap is composition
(−19 raw, −9 at equal age, sex, schooling, income and state), and the equal-SES gap does not
shrink from G2 to G3+ at all (−8.8 → −8.9; registration −7.8 → −8.0). Mexican-origin citizens whose
parents and grandparents were born here still vote about 9 points less than whites who look like
them on paper. The India-born, by contrast, vote at the white rate raw (+0.7) and 10 points below
at equal SES — the same equal-SES gap as the Mexico-born, reached from the opposite composition.

**Over-report.** CPS turnout is self-reported and exceeds official counts. It is *not* common
across groups: validated against voter files 2008–2018, "the CPS overestimates black and Hispanic
turnout relative to non-Hispanic whites" and sampling error and standard adjustments do not
remove it [SOURCE: Ansolabehere, Fraga & Schaffner, "The Current Population Survey Voting and
Registration Supplement Overstates Minority Turnout", *Journal of Politics* 84(3), 2022,
doi:10.1086/717260]. The Mexican-origin gaps above are therefore **lower bounds** on the true
Hispanic–white turnout gap. Whether the over-report differs by generation is not known
[UNVERIFIED]. The Census convention counts item non-response as not voting; non-response is
17–19% for the Mexican groups against 13–15% for whites (`derived/voting_nonresponse.csv`), but
the responders-only convention gives the same gaps within a point at G3+, so the convention does
not drive the result.

## 2. Intermarriage by generation (CPS ASEC 2022–2025) [DATA] [CALCULATION]

Script `asec_intermarriage.py`; outputs `derived/intermarriage.csv`, `derived/child_identification.csv`,
`derived/gate_spouse_linkage.txt`. Inputs are the four local Census public-use ASEC archives, each
checked against its register SHA-256; persons joined to the 160 replicate weights on
(PH_SEQ, PPPOS), `pwwgt0` = `MARSUPWT/100` asserted.

**Universe and definitions.** Married, spouse present (`A_MARITL` 1–2), ages 25–54, spouse found
through `A_SPOUSE` in the same household. 131,639 married persons; every one has a spouse record
(100.00%, and every spouse pointer is reciprocal), so the ≥ 99% gate passes. 1,828 same-sex couples
dropped. Spouse origin: *Mexican origin* = born in Mexico, a Mexico-born parent, or Hispanic origin
Mexican; *other Hispanic*; *non-Hispanic*. Ego generations are the canonical masks (G1 Mexico-born
foreign-born; G2 US-born with a Mexico-born parent; G3+ US-born, both parents US-born, self-identified
Mexican). *Random matching*: the weighted Mexican-origin share among opposite-sex married persons
25–54 in the ego's state and year — what endogamy would be if people married at random within their
state. SEs: pooled replicates (`se`) and, because adjacent ASECs share about half their households,
the annual-average SE (`se_conservative`, the SE if the four years were perfectly correlated).

**Spouse's origin, married persons 25–54, % (SE, conservative SE in brackets):**

| Ego | n | Mexican-origin spouse | other Hispanic | non-Hispanic | of which NH white | random-matching Mexican share | excess over random |
|---|---:|---:|---:|---:|---:|---:|---:|
| Mexico-born (G1) | 8,819 | **90.2** (0.5) [0.7] | 4.1 | 5.7 (0.4) | 4.7 | 21.8 | 68.4 |
| G2 | 3,685 | **72.3** (1.1) [1.8] | 7.0 | 20.6 (0.9) | 16.8 | 25.2 | 47.1 |
| G3+ (self-identified) | 3,912 | **55.9** (1.3) [2.1] | 3.9 | 40.2 (1.2) | 33.4 | 24.4 | 31.5 |
| US-born NH white (reference) | 76,093 | 2.8 | 2.1 | 95.1 | 90.9 | 9.5 | −6.7 |

By sex the Mexican-origin spouse share is men 90.7 / 71.1 / 56.7 and women 89.7 / 73.3 / 55.1 for
G1 / G2 / G3+ — no sex difference.

**Retention ratios** (share at G n+1 over G n): Mexican-origin spouse 0.80 (G1→G2) and 0.77
(G2→G3+); excess endogamy over random matching 0.69 and 0.67. Each generation keeps about
two-thirds to four-fifths of its parents' in-marriage. [CALCULATION]

**At equal age, sex, education and state** (weighted LPM with centred controls, generation
effects evaluated at the pooled Mexican-origin married profile; replicate SEs):

| Outcome | Spec | G1 | G2 | G3+ |
|---|---|---:|---:|---:|
| Mexican-origin spouse | age, sex, educ, year | 86.9 (0.6) | 75.6 (1.1) | 60.3 (1.3) |
| Mexican-origin spouse | + state | 87.7 (0.5) | 74.4 (1.1) | 59.4 (1.3) |
| Non-Hispanic spouse | + state | 8.0 (0.4) | 18.9 (0.9) | 36.9 (1.2) |
| Excess over random | + state | 64.5 (0.6) | 51.2 (1.1) | 36.3 (1.3) |

Education and geography explain little of the generational decline: at a common profile
the Mexican-origin spouse share still falls 87.7 → 74.4 → 59.4 (ratios 0.85, 0.80; raw 0.80, 0.77).
Schooling does not drive out-marriage much once state is held: the equal-SES G1 share is lower
than raw (the G1 group's low schooling predicts endogamy), the G3+ share higher. Family income
is left out because it is jointly determined with the spouse.

**G3 vs G4+.** The generation-split grandparent linkage needs a co-resident biological parent,
which married 25–54-year-olds rarely have: 24 observed G3 and 17 observed G4+ married persons
(Mexican-origin spouse 72% and 58%, SEs 12–14 points). Unusable; reported in the CSV only.

**Caveat on G3+ (the direction of the bias).** G3+ is defined by *self-identification* as Mexican.
Among US-born people with US-born parents, those who married out are plausibly less likely to
still report Mexican origin (and the household respondent may be the non-Hispanic spouse), so
the measured G3+ endogamy of 56% is an upper bound on the endogamy of all G3+ descendants of
Mexican immigrants. [INFERENCE]

### Indian origin on the same code

| Ego | n | Indian-origin spouse | India-born spouse | non-Indian spouse |
|---|---:|---:|---:|---:|
| India-born (G1) | 3,120 | **96.3** (0.4) | 93.0 (0.6) | 3.7 |
| Indian G2 (US-born, India-born parent) | 345 | **65.5** (3.6) | 30.9 (3.8) | 34.5 |

Indian-origin spouse = India-born, India-born parent, or Asian Indian (`PRDASIAN` 1). The India-born
first generation is more endogamous than the Mexico-born (96 vs 90%), and the G1→G2 retention is
lower (0.68 vs 0.80); by G2 the two groups sit at similar levels (65.5 vs 72.3%). The Indian memo's
88.4% (ACS 2024, India-born married persons of all ages, spouse India-born) and 52.4% (US-born of
Indian ancestry, which mixes G2 and later) are a different instrument and age window; on the CPS
25–54 window the India-born-spouse share is 93.0%.

## 3. Children of mixed couples: the Duncan–Trejo mechanism [DATA] [CALCULATION]

Children under 18 living with both parents (both linked through `PEPAR1`/`PEPAR2`, both biological
unless stated). Outcome: the child is reported Hispanic (`PEHSPNON` 1), and reported Mexican
(`PRDTHSP` 1). The household respondent, usually a parent, answers for the child.

| Couple (both biological parents) | n children | reported Hispanic | reported Mexican |
|---|---:|---:|---:|
| Both parents Mexican origin | 10,022 | 98.9 (0.2) | 97.0 (0.3) |
| Mexican origin × non-Hispanic | 4,085 | **83.6** (1.1) | **80.4** (1.2) |
| Mexican origin × other Hispanic | 1,190 | 97.2 (0.8) | 55.0 (2.6) |

Any parent type (step and adoptive included): mixed Mexican × non-Hispanic 82.1 (1.1) Hispanic, 79.0 (1.1) Mexican, n 4,679.

Mexican-origin × non-Hispanic couples by the Mexican parent's generation (reported Hispanic, %):
G1 parent 83.5 (2.6), n 644; G2 parent 82.0 (2.3), n 1,114; G3+ parent **84.4** (1.4), n 2,206
— the identification loss among children of mixed couples is 16–18% and does not grow with the
Mexican parent's generation. With a Mexican-origin father 85.8% of G3+-parent children are reported
Hispanic, with a Mexican-origin mother 83.2%; with a NH-white other parent 85.1%.

**Loss per generation at the child stage** (revised 2026-09-27; `identity_loss.py` →
`derived/identity_loss.csv`). Children are the unit. If q is the share of married Mexican-origin
*people* with a non-Hispanic spouse, then under equal fertility per couple the share of
Mexican-origin-parented *children* born to mixed couples is 2q/(1+q). That is 0.57 at G3+
(q = 0.40), not 0.40. With other-Hispanic spouses as a third couple type the shares are
m/2 : h : q. Loss = Σ (child share × share of that couple type's children not identified).
Mexican and Hispanic identification differ: children of Mexican × other-Hispanic couples are
reported Hispanic 97.2% of the time but Mexican only 55.0% of the time.

| Mexican parent's generation | children from Mexican × non-Hispanic couples | not reported Hispanic | not reported Mexican |
|---|---:|---:|---:|
| G1 | 10.5% | 2.8 (0.3) | 7.8 (0.6) |
| G2 | 32.3% | 6.8 (0.8) | 15.1 (1.0) |
| G3+ | 55.8% | **9.0** (0.8) | **12.0** (0.9) |

These use the three couple types. With the audit's two-type formula 2q/(1+q), G3+ gives 9.1 and
9.9, and G2 gives 6.9 and 11.0. SEs come from the delta method on independent components. The
other parent in an endogamous couple is assumed to be of the same generation.
[CALCULATION: `derived/identity_loss.csv`]

**Against the lineage model: not consistent at G4+.** `lineage_cost_2026_09_19` uses 0.8881 for
the fourth-plus identification rate. That is the measured *third*-generation rate
(`mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv`), and the model
applies it on the assumption that identification stops decaying after the third generation. The
table says it does not stop. Children of self-identified G3+ parents lose another 12.0%
(Mexican) or 9.0% (Hispanic) at birth. Carrying the G3 rate forward one more step gives
0.888 × (1 − 0.120) ≈ **0.78** for G4 on the Mexican measure, before any adult switching, and
later generations fall further. That puts the rate between the lineage's central 0.888 and
Duncan–Trejo's 0.708. The G2-parent step here, 15.1% not Mexican, is also larger than the
objective third-generation loss of about 11% in the population lane. That lane counts actual
children, so this lane's equal-fertility synthetic probably overstates the step (mixed couples
may have fewer children). The central 0.888 is therefore too high for G4+; the 0.708 arm is
closer. [CALCULATION, INFERENCE]

## 4. One civic table with carry-over [DATA] [CALCULATION]

`carryover.py` → `derived/civic_carryover.csv`. Every figure is read from a derived CSV of its
lane, none retyped: `service_by_ses_2026_09_23/derived/cps_civic_{rates,gaps}.csv`, this lane's
`voting.csv` and `intermarriage.csv`, `norms_gen_2026_09_18/derived/{gss,anes}_adjusted.csv`, and
`service_by_ses_2026_09_23/derived/military_rates.csv`. The gap is the group minus US-born NH
whites. For endogamy it is the excess over random matching, because whites are no comparator for
in-marriage. ρ(n→n+1) = gap(G n+1) / gap(G n). The delta-method SE treats the two gaps as
independent, which overstates it because they share the white reference. ρ is blank when the
earlier gap is within 2 SE of zero.

| Measure (source) | Adjustment | G1 gap | G2 gap | G3+ gap | ρ G1→G2 | ρ G2→G3+ | ρ G1→G3+ |
|---|---|---:|---:|---:|---:|---:|---:|
| Voted, citizens (CPS Nov; G1 naturalized) | raw | −24.1 (1.1) | −23.5 (0.8) | −19.3 (0.9) | 0.98 (0.06) | 0.82 (0.05) | 0.80 |
| | equal SES + state | −12.7 (1.1) | −9.8 (0.8) | −9.4 (0.9) | 0.77 (0.09) | 0.96 (0.12) | 0.74 |
| Registered | raw | −21.3 (1.2) | −18.8 (0.9) | −15.9 (0.9) | 0.88 (0.06) | 0.85 (0.06) | 0.75 |
| | equal SES + state | −10.2 (1.2) | −8.0 (0.9) | −8.1 (0.9) | 0.78 (0.12) | 1.01 (0.16) | 0.79 |
| Volunteered (CPS Sept) | raw | −19.8 (0.9) | −15.8 (1.0) | −11.2 (1.1) | 0.80 (0.06) | 0.71 (0.08) | 0.56 |
| | equal SES | −10.2 (1.0) | −9.1 (1.0) | −6.0 (1.1) | 0.89 (0.13) | 0.66 (0.14) | 0.58 |
| | equal SES + state | −9.2 (1.0) | −8.0 (1.1) | −5.2 (1.1) | 0.86 (0.16) | 0.66 (0.17) | 0.57 |
| Gave > $25 (CPS Sept) | raw | −27.8 (1.2) | −29.1 (1.3) | −19.0 (1.6) | 1.05 (0.06) | 0.65 (0.06) | 0.68 |
| | equal SES | −11.1 (1.3) | −12.3 (1.3) | −7.6 (1.5) | 1.11 (0.18) | 0.62 (0.14) | 0.69 |
| | equal SES + state | −8.6 (1.4) | −9.5 (1.4) | −5.6 (1.4) | 1.10 (0.24) | 0.59 (0.18) | 0.65 |
| Veteran, men born 1956+ (CPS Sept) | raw | −7.9 (0.3) | −3.9 (0.8) | −2.0 (1.0) | 0.49 (0.11) | 0.52 (0.28) | 0.25 |
| | equal SES | −6.4 (0.4) | −1.3 (0.8) | −0.6 (1.0) | 0.21 (0.13) | — | 0.09 |
| Endogamy, excess over random (CPS ASEC) | raw | 68.4 (0.5) | 47.1 (1.1) | 31.5 (1.3) | 0.69 (0.02) | 0.67 (0.03) | 0.46 |
| | equal age, sex, educ, state | 64.5 (0.6) | 51.2 (1.1) | 36.3 (1.3) | 0.79 (0.02) | 0.71 (0.03) | 0.56 |
| Civil-liberties tolerance, Stouffer 15 (GSS, scale pts) | equal SES | −1.37 (0.27) | −1.42 (0.26) | −0.34 (0.23) | 1.04 (0.28) | 0.24 (0.17) | 0.25 |
| Confidence, 13 institutions (GSS, 1–3) | equal SES | +0.13 (0.02) | +0.02 (0.02) | +0.03 (0.02) | 0.16 (0.19) | — | 0.23 |
| "Great deal" of confidence in the military (GSS, pts) | equal SES | −15.3 (2.7) | −11.4 (3.2) | −7.8 (2.9) | 0.74 (0.25) | 0.69 (0.32) | 0.51 |
| Government should reduce income differences (GSS, 7-pt) | equal SES | +0.59 (0.11) | +0.58 (0.11) | +0.32 (0.10) | 0.98 (0.26) | 0.55 (0.20) | 0.54 |
| Obedience a top-2 child value (GSS, pts) | equal SES | +16.1 (2.7) | +2.6 (2.4) | +4.4 (2.4) | 0.16 (0.15) | — | 0.28 |
| Political violence at least "a little" justified (ANES, pts) | equal SES | +20.3 (4.7) | +9.5 (4.2) | +13.7 (4.6) | 0.47 (0.23) | 1.44 (0.80) | 0.68 |

"Equal SES" means different controls in each source. CPS Sept: age, sex, education, family
income and year. CPS November: age, sex, education and family income. GSS/ANES (the `adj_mex`
model of the norms lane): age, age², years of education, log family income and year. The norms
lane reports raw contrasts for G1 and G3+ only; they are in the CSV. Each norms item is cited to
[the norms memo](../../../research/immigration-institutions-and-liberal-norms-by-generation-2026-09-18.md),
including its caveats on response style and on the political-violence item.

**What the table says.** Behavioural civic measures that cost time or money carry over at
ρ ≈ 0.6–0.8 per generation raw. Two generations leave 55–80% of the first-generation gap on
voting, volunteering and giving (ρ G1→G3+ 0.56–0.80). In-marriage dissolves at a similar
per-generation rate (0.67–0.69 raw). The two measures split at equal SES. For volunteering and
giving, adjustment removes about half the gap at every generation and the G2→G3+ step stays at
0.6–0.7. For voting and registration, adjustment removes half the gap and what is left does not
move between G2 and G3+ (ρ 0.96–1.01). Attitudes converge faster where there was a large G1 gap
(tolerance 0.25, obedience 0.28, institutional confidence goes from premium to parity). Preferences
for redistribution (0.54) and confidence in the military (0.51) close about half-way. Political
violence does not close measurably, and the lane that measured it flags it as the item with the
worst measurement. [INFERENCE] The economic side of this comparison belongs to the sister lane
`generation_carryover_2026_09_27`. This lane computed no economic ρ and makes no claim on which
side converges faster.

## 5. Disconfirmation [DATA] [INFERENCE]

- **Where the gap is SES composition.** Veteran status is the clear case. At equal SES the male
  G2 and G3+ gaps are −1.3 (0.8) and −0.6 (1.0) points, neither distinguishable from zero. The G1
  gap (−6.4) reflects legal eligibility to enlist. Roughly half of each G3+ gap is composition:
  voting (−19.3 → −9.4), registration (−15.9 → −8.1), volunteering (−11.2 → −5.2 with state) and
  giving (−19.0 → −5.6).
- **Where it persists at equal SES.** Voting and registration keep a 8–10-point gap at G3+ that is
  flat from G2 (−9.8 → −9.4). Volunteering keeps −5 to −6 points and giving −6 to −8. Endogamy is not
  SES at all: at equal schooling and state the G3+ excess over random matching rises from 31.5 to
  36.3. Their state random-matching benchmark is no lower than G2's (24.4 against 25.2), so this is
  not a geography effect. The likely driver is schooling: the G3+ are better educated than the
  pooled profile, and more schooling goes with out-marriage. [INFERENCE]
- **Military, men vs women and young cohorts** (ACS 2022–2024, US-born Mexican Hispanic origin,
  ratio to US-born NH whites of the same sex [DATA: `service_by_ses_2026_09_23/derived/military_rates.csv`]):
  - Ever on active duty, ages 18–49: men 0.79 (0.01), women 0.98 (0.03).
  - Now on active duty, ages 18–24: men 0.98 (0.03), women 1.43 (0.13).
  - Ever on active duty, men 18–24: 0.94 (0.03).

  The male shortfall belongs to older cohorts. US-born women serve at the white rate, and young
  US-born men now serve at it. The Mexico-born are at 0.19 (men) and 0.30 (women) because many
  cannot legally enlist.
- **Over-report.** CPS overstates Hispanic turnout relative to white turnout (Ansolabehere–Fraga–
  Schaffner 2022), so the turnout gaps are lower bounds. No evidence was found on whether the bias
  differs by generation; if it is larger for the foreign-born, the measured G1→G2 ρ is too high.
  [UNVERIFIED]
- **Ethnic attrition biases G3+ toward the less assimilated.** G3+ is self-identified Mexican.
  The children of G3+ parents lose 9.0% (Hispanic) to 12.0% (Mexican) of identification at birth,
  because 56% of their Mexican-origin-parented children come from mixed couples (section 3,
  revised). Those who drop out are drawn from the out-married, and out-married households plausibly
  vote and volunteer more. Measured G3+ civic gaps therefore overstate the gap of all descendants,
  and measured ρ understates convergence. The effect is modest per generation but compounds. It is
  larger than the lineage model's central 0.888 at G4+ assumes (section 3).
  [INFERENCE, CALCULATION]
- **Cross-sections are not lineages.** Today's G3+ descend from pre-1970 migration cohorts, not
  from today's G1. ρ compares groups alive now; it is not a transmission rate for a family.
  [INFERENCE]
- **G3 vs G4+** could not be separated for married adults. The co-resident grandparent linkage
  finds 24 and 17 people (section 2).

## Files covered and skipped

Covered:
- `service_by_ses_2026_09_23` (`cps_civic.py` read; `cps_civic_rates.csv`, `cps_civic_gaps.csv`,
  `military_rates.csv`, RESULT.md §4 used in the gate).
- `norms_gen_2026_09_18/derived/{gss,anes}_adjusted.csv` and the norms memo.
- `generation_split_2026_09_20/analyze_cps.py` (grandparent classifier copied into
  `asec_intermarriage.py`).
- `indian_civic_cps_2026_09_18` (group definitions, the 2020 gate, the cached P20-585 Table 1).
- `indian_ledger_2026_09_18/acs_profile.py` and the Indian memo (the 88.4% definition).
- `lineage_cost_2026_09_19` README/RESULT (0.888 identification rate, the `intermarried_half`
  rule).
- The four ASEC archives (SHA-256 checked).
- November 2020/2022/2024 public and replicate files, cached in `_cache/cps/` with the technical
  documentation and the P20 tables.

Skipped:
- `civic_service_by_ancestry_2026_09_21` (ladder 170). `service_by_ses_2026_09_23` extends and
  reproduces it.
- The November public-use CSVs. The server delivered about 1.4 MB/min, so the lane read the
  fixed-width `.dat` files, gated against the documentation tallies and the published totals, and
  deleted a partial CSV.
- Identification of children of mixed Indian couples. The Asian-Indian flag applies only to
  single-race Asian respondents (`PRDASIAN` universe `PRDTRACE` 4), so a mixed-race child cannot be
  classified on the same terms.
- Re-running the lineage model with measured intermarriage. That lies outside this lane's
  directory and its brief.

## Revisions

- **2026-09-27 (audit).** Section 3 and the attrition bullet in section 5 had computed the loss per
  generation as 0.40 × 0.16 ≈ 6–7% and called it consistent with the lineage model's 0.888. That
  multiplied a share of married *people* (q) by a share of *children*. The share of children from
  mixed couples is 2q/(1+q), about 0.57 at G3+. Recomputed by the Mexican parent's generation for
  both identification measures in `derived/identity_loss.csv` (`identity_loss.py`). G3+ parents lose
  9.0% (Hispanic) or 12.0% (Mexican) per generation. The comparison now reads **not consistent**:
  identification keeps decaying after G3, so the lineage's central G4+ rate of 0.888 is too high
  (≈ 0.78 after one more step). The verdict sentence was updated to match. No other number moved.
