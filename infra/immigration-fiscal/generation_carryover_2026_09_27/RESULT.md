claude-opus-5-5

# Generation carry-over: does the Mexican-origin gap fade, stall or persist? (G1 → G4+)

**Verdict:** The first native-born step closes most of the gap; after that the gap stalls, and no
source shows the fourth-plus generation ahead of the third.
- **G1 → G2 carries over 17–68% of the gap**, depending on the measure (CPS 2022–25, adults
  25–64): 17% on less-than-high-school, 39–45% on worker earnings, 64% on BA+ and 65% on the
  partial tax-minus-transfer ledger.
- **G2 → G3+ carries over 85–92%** (BA+ 0.92, ledger 0.90, earnings 0.88–0.90). Where G3 is
  defined by the grandparents' birthplace (NLSY97), the step is larger: 0.76 on BA+ and 0.64 on
  years of schooling. On the lineage (parents' schooling gap → child's), NLSY97 still carries
  over 0.91.
- **G3 → G4+: no improvement in any source.** BA+ ratios run 0.97 (NLSY97), 1.04 (CPS, adults
  living with both parents), 1.10 (GSS) and 1.8 (MASP, n 38). On years of schooling, employment,
  AFQT and less-than-high-school, G4+ is worse (NLSY97 years 1.82, GSS years 1.34).
- **Attrition-bounded projection [MODEL].** Correcting for G4+ attriters at measured
  non-identifier values lowers the G3 → G4+ ratio only to 0.79–1.10 (central 0.88–1.03). Starting
  from the G3+ partial-ledger gap (−$6,615 per adult a year), the central projection puts G4 at
  −$6.5k and G5 at −$6.3k. The band runs from −$3.7k and −$2.1k (gap regresses to the white mean at
  the NLSY97 parent–child slope of 0.56) to −$6.6k and −$6.6k (full stall). Only the extreme case,
  in which half or more of G4+ descendants stop identifying and look exactly like whites, cuts the
  G5 gap below −$1k.
  [2026-09-28: the central above is superseded. Attriters are now valued by the generation-split
  measured rule of `carryover_identity_2026_09_27` §2: people lost at G3, and their descendants, close
  0.78 of the identifiers' gap (SE 0.64; 0.91 with CPS 2026 pooled in); people lost later close
  nothing. Identity loss then lowers every generation's lineage gap by the same 9% from G3 on. The
  CPS and GSS G3 → G4+ ratios stay at their observed 1.04 and 1.10; NLSY97's, whose G3 already
  includes its non-identifiers, falls to 0.89. The range is 0.81–1.10 (0.79–1.10 with the 2026
  value). The central projection, per lineage descendant, starts from a G3+
  lineage gap of −$6.0k and puts G4 at −$6.1k and G5 at −$6.1k. The band does not move. The old
  central (0.98 a step) gave every attriter NLSY97's +6.16 BA points and, through a filter, averaged
  CPS and GSS only; with NLSY97 included it is 0.94, kept as a sensitivity. The worst case now starts
  from its own lineage base: G5 −$0.37k, was −$0.42k. Mapping and numbers: §3 and §4.]
  [2026-10-05: C3 is now 0.56 (SE 0.25), the IPUMS-CPS basic monthly frame 1994–2026 pooled with
  NLSY97, in place of 0.78 (0.64). Identity loss lowers the lineage gap by 6% from G3 on, not 9%.
  NLSY97's split ratio is 0.91, and the range is 0.86–1.10 (0.79–1.10 with the 2026 value). The
  central projection starts from a lineage gap of −$6.2k and puts G4 at −$6.3k and G5 at −$6.4k.
  (g3_identity_pooled_2026_10_05, monthly frame)]

The main reason not to call this a permanent stall is vintage. Today's adult G4+ descend from
pre-1930s migrants, many in Texas. NLSY97 shows their parents were less schooled than the parents
of today's G3, and California roots explain part of the G4+ deficit. So today's G4+ is not a clean
forecast of the G4 that today's G3 will produce.
[FRAMING-SENSITIVE: "gap" is against third-plus non-Hispanic whites; the dollar measure is the
partial annual ledger, not the adopted account, which has no white reference]

For comparison, the operator's Indian-origin premium roughly halves from G2 to G3. The Mexican-origin
deficit shrinks by about a tenth from G2 to G3+ on standard data, and by a quarter to a third on
NLSY97's grandparent-defined G3.

## 1. Outcome gaps by generation

All gaps are group minus third-plus non-Hispanic whites, with whites reweighted to the group's
age × sex mix in the same frame. SEs are CPS 160-replicate SDR (4/160, pooled with a common
replicate index), a GSS year × stratum × PSU cluster bootstrap (400 draws), a MASP family bootstrap
(1,000 draws) or the published SEs. Full rows, including every frame and the 2022–2026
sensitivity: `derived/gaps_by_generation.csv`.
[CALCULATION: `analyze_cps.py`, `analyze_gss.py`, `analyze_masp.py`, `summarize.py`]

**A. CPS ASEC 2022–2025 pooled, all civilian household adults 25–64** (income years 2021–24,
2024 dollars; G3+ = US-born of US-born parents, identifying as Mexican):

| Gap to whites (SE) | G1 | G2 | G3+ (all) | G3+ unresolved |
|---|---|---|---|---|
| n (person-years) | 18,271 | 9,468 | 10,040 | 9,460 |
| Mean age | 45.1 | 37.8 | 41.3 | 41.7 |
| BA+, points | −33.9 (0.4) | −21.5 (0.6) | −19.8 (0.8) | −19.5 (0.8) |
| Less than HS, points | +39.0 (0.6) | +6.7 (0.4) | +5.7 (0.5) | +5.7 (0.5) |
| Employed, points | −7.1 (0.4) | −3.2 (0.5) | −4.1 (0.6) | −3.2 (0.6) |
| Worker earnings, mean $ | −43,732 (718) | −19,787 (1,039) | −17,791 (1,060) | −16,867 (1,019) |
| Worker earnings, median $ | −30,473 (656) | −11,766 (586) | −10,295 (316) | −9,677 (455) |
| Partial ledger, $ per adult | −11,230 (227) | −7,331 (270) | −6,615 (317) | −6,342 (305) |

The partial ledger follows the September 5 generator. SPM-unit payroll, federal-after-credit and
state taxes, minus SS, SSI, TANF/GA, UI, veterans' benefits, SNAP, energy, WIC, school lunch and
broadband, are shared equally among the unit's adults. [CALCULATION]

**B. CPS 2022–2025, adults 18+ living with both biological parents.** This is the only frame
where observed G3 (a Mexico-born grandparent) and observed G4+ (four US-born grandparents) are
both classifiable. Whites are drawn from the same frame.

| Gap to co-resident whites (SE) | G2 | G3 observed | G4+ observed | G4+ − G3 (SE) |
|---|---|---|---|---|
| n / mean age (all 18+) | 3,514 / 24.6 | 409 / 26.4 | 771 / 25.6 | |
| BA+ at 25+, points (n 1,242/151/302) | −13.9 (2.0) | −9.7 (4.6) | −10.1 (3.9) | −0.4 (5.4) |
| BA+ at 22+, points | −15.3 (1.6) | −5.6 (4.2) | −11.6 (3.1) | −6.0 (4.7) |
| Less than HS at 25+, points | +2.2 (1.2) | +0.7 (2.9) | +0.3 (2.1) | −0.4 (3.5) |
| Employed, points | +4.7 (1.2) | −0.8 (3.3) | −1.7 (2.5) | −0.9 (4.4) |
| Worker earnings, mean $ | +384 (1,240) | −3,750 (2,530) | +2,711 (4,083) | +6,461 (4,591) |
| Household ledger share, $ per adult | −8,145 (413) | −3,201 (1,496) | −5,341 (735) | −2,140 (1,639) |

The observed G3 and G4+ are young adults who still live with their parents. The ledger in this
frame is mostly the parents' (G1, G2 and G3+ respectively) household ledger. With 2026 added
(2022–2026), G4+ − G3 on BA+ at 25+ is −3.5 (4.6) and on the ledger −$2,272 (1,382).
[CALCULATION: `derived/cps_gaps_CPS_ASEC_2022_2026.csv`]

**C. GSS 2000–2024, Mexican identifiers aged 25–64** (G3/G4+ from GRANBORN; a G3 grandparent can
be foreign-born in any country). Whites are US-born with US-born parents.

| Gap (bootstrap SE) | G1 | G2 | G3 | G4+ |
|---|---|---|---|---|
| n | 829 | 502 | 275 | 240 |
| BA+, points | −25.2 (0.9) | −17.1 (1.6) | −17.4 (1.9) | −19.0 (1.9) |
| Less than HS, points | +45.5 (1.5) | +12.7 (1.9) | +5.4 (2.0) | +14.1 (3.5) |
| Years of schooling | −4.04 (0.13) | −1.23 (0.12) | −1.00 (0.15) | −1.34 (0.17) |
| Employed, points | −6.5 (1.4) | −2.3 (1.9) | −4.0 (2.5) | −14.3 (3.1) |
| Log respondent income (REALRINC) | −0.59 (0.04) | −0.19 (0.05) | −0.22 (0.06) | −0.32 (0.06) |
| Occupational prestige (PRESTG10) | −8.8 (0.4) | −3.8 (0.5) | −3.7 (0.6) | −3.8 (0.8) |

Against white G4+ only (GRANBORN = 0), every gap moves by 0.3 or less (`derived/gss_gaps.csv`).

**D. NLSY97 (1980–84 birth cohort, age 25+ at the last round to 2015–16), published.** Gaps
are to white 4th+. [SOURCE: Duncan, Grogger, Leon & Trejo, IZA DP 12704, Table 2 PDF p.45;
Tables 8–11 col (1) PDF pp.52–55; Table 5 p.48]

| Gap (SE) | G1.5 | G2 | G3 | G4+ | G3+ pooled |
|---|---|---|---|---|---|
| n (schooling) | 189 | 378 | 151 | 274 | 425 |
| Years of schooling | −2.53 | −1.46 | −0.93 | −1.69 | −1.45 |
| High-school diploma, points | −24.3 | −9.2 | −1.8 | −18.0 | −12.7 |
| BA+, points | −30.6 (2.3) | −25.4 (2.0) | −19.4 (3.4) | −18.8 (2.6) | −19.0 (2.2) |
| AFQT percentile | −31.8 (2.5) | −25.0 (1.8) | −17.7 (2.5) | −25.6 (1.9) | |
| Log annual earnings, 30+ | −0.48 (0.11) | −0.23 (0.07) | −0.08 (0.07) | −0.20 (0.08) | |
| Log hourly wage, 30+ | −0.31 (0.06) | −0.16 (0.04) | −0.12 (0.06) | −0.16 (0.05) | |
| Parents' mean schooling | −6.52 | −5.00 | −1.03 | −1.32 | |

**E. MASP (Telles–Ortiz), adult children interviewed 1998–2002, Los Angeles and San Antonio
origin families.** These are levels with a family-bootstrap SE. The gap uses an external GSS
2000–2004 white benchmark at the same ages.

| | G2 (n 204) | G3 (n 245) | G4+ (n 38) |
|---|---|---|---|
| BA+, % | 19.1 (3.4) | 20.0 (2.7) | 13.2 (5.5) |
| BA+ gap to GSS whites, points | −9.1 | −8.4 | −15.5 |
| Grade under 12, % | 8.3 | 11.8 | 18.4 |
| Couple income under $30k, % | 28.6 | 28.1 | 26.3 |
| Any SSI/AFDC/food stamps, % | 6.4 | 8.7 | 7.9 |

## 2. Carry-over ratios ρ(n → n+1) = gap(n+1) / gap(n)

Values below 1 mean the gap shrinks. SE is by replicate, bootstrap or delta method; the
percentile interval is in the CSV. A ratio whose denominator gap is within 2 SE of zero is
flagged unstable in `derived/carryover.csv`. In that case read `change_in_gap` instead.

| Measure | Source / frame | G1→G2 | G2→G3(+) | G3→G4+ |
|---|---|---|---|---|
| BA+ | CPS pop 25–64 | 0.64 (0.02) | 0.92 (0.04) [G3+] | n/a |
| BA+ | CPS both parents | | 0.70 (0.33) | 1.04 (0.70) |
| BA+ | GSS | 0.68 (0.06) | 1.02 (0.14) | 1.10 (0.16) |
| BA+ | NLSY97 | 0.83 (0.09) [G1.5] | 0.76 (0.15) | 0.97 (0.22) |
| BA+ | MASP | | 0.92 (unstable) | 1.84 (interval 0.68–4.39) |
| Less than HS | CPS pop | 0.17 (0.01) | 0.85 (0.09) [G3+] | |
| Less than HS | GSS | 0.28 (0.04) | 0.43 (0.17) | 2.59 (interval 1.24–6.0) |
| Years of schooling | GSS | 0.30 (0.03) | 0.81 (0.14) | 1.34 (0.28) |
| Years of schooling | NLSY97 | 0.58 (0.07) | 0.64 (0.17) | 1.82 (0.51) |
| Years, parent → child lineage | NLSY97 Tables 5+2 | 0.29 (0.03) | 0.91 (0.28) | 1.29 (0.20) |
| Employment | CPS pop | 0.46 (0.08) | 1.27 (0.29) | |
| Worker earnings, mean | CPS pop | 0.45 (0.02) | 0.90 (0.07) | |
| Worker earnings, median | CPS pop | 0.39 (0.02) | 0.88 (0.05) | |
| Log income / earnings | GSS / NLSY97 | 0.33 / 0.47 | 1.15 / 0.35 | 1.43 / 2.5 (unstable) |
| AFQT | NLSY97 | 0.79 (0.08) | 0.71 (0.11) | 1.45 (0.23) |
| Occupational prestige | GSS | 0.43 (0.06) | 0.97 (0.21) | 1.03 (0.28) |
| Partial ledger $ | CPS pop | 0.65 (0.02) | 0.90 (0.05) [G3+] | |
| Household ledger $ | CPS both parents | | 0.39 (0.18) | 1.67 (1.00) |

**Adopted account ($ net cost to other residents per adult).** Ratios are read from
`generation_account_2026_09_24/derived/generation_results.csv`, whose case is named in
`generation_summary.json` and carried in the `source` column (`adopted_account_<case>`). These are
absolute costs measured against zero, not gaps to whites; the account has no reference group.

| Convention | G1→G2 | G2→G3+ |
|---|---|---|
| (b) minors with parents, low / high end — September 27 case (8654a0c) | 0.72 / 0.65 | 0.94 / 1.16 |
| (a) own generation, low / high end — September 27 case | 1.78 / 2.56 | 0.86 / 1.11 |
| (b), schools case of September 26 (the first run of this lane) | 0.66 / 0.56 | 0.88 / 1.16 |
| (a), schools case of September 26 | 1.77 / 2.70 | 0.79 / 1.09 |

[2026-09-27, 23:30: re-run on the September 27 case after the generation lane moved to it (8654a0c);
the source label now reads the case instead of a fixed string.]

Under (b), the NAS convention, the dollar ratios match the partial-ledger gap ratios: roughly
0.6 for the first step and 0.9–1.2 for the second. Under (a), G2 carries its own children's
schooling, so its "carry-over" exceeds 1 by construction.

**Does G4+ improve on G3?** No. On schooling (BA+, years, less-than-HS), across three national
sources and MASP, the G4+ − G3 difference is never positive beyond noise, and it is negative in
most specifications. The CPS BA+ point estimate is −0.4 (SE 5.4). GSS is −1.7 (2.5) on BA+,
−0.34 (0.22) on years and −10.3 (3.9) on employment. NLSY97 is −0.76 years and −16 points on a
high-school diploma. Two measures lean the other way: NLSY97 BA+ (+0.6 points) and CPS worker
earnings (+$6.5k, SE 4.6k), in a young frame where most G4+ workers are 18–30.

## 3. Identity attrition bounds

The lineage gap equals (1 − a) × the identifiers' gap plus a × the attriters' gap, where a is the
share of Mexican-descent people who do not identify. `derived/attrition_bounds.csv` has every
combination; `attrition_corrected_rho.csv` has the implied G3 → G4+ ratios.

Rates [DATA/SOURCE, as labelled in the CSV]:
- **G3:** 11.2%, from CPS 2025 co-resident children with a Mexico-born grandparent (88.81%
  identify; population-total lane); 20.6% from NLSY97 cross-section (Table 12 p.56); 28.2% from
  Duncan–Trejo 1994–2006.
- **G4+:** measured on the lineage by no survey. Scenarios use the G3 rate (11.2%), Duncan–Trejo's
  1994–2006 fourth-plus rate (29.2%) and the 1970 Census reinterview fourth generation (55.6%,
  n 27).
- **NLSY97 G3** is defined by the grandparents' birthplace and already includes non-identifiers,
  so it takes no G3 correction.

How much better the attriters do [SOURCE/DATA]:
- **BA+:** +0.63 points (MASP), +2.54 (Pew 2015–16) and +6.16 (NLSY97 Table 13 p.57, n 11).
- **Years of schooling:** +0.64 (NLSY97) and +0.76 (Duncan–Trejo 2017).
- **Dollar gaps:** the population-total lane's convention, under which attriters close 54–72% of
  the gap.
- [2026-09-28: the dollar convention is a years-of-schooling share, not a dollar measurement
  (`carryover_identity_2026_09_27` §2). It stays as sensitivity rows, scenario
  `sensitivity_years_share_convention`. The BA+ and years advantages stay as
  `attriters_at_measured_nonidentifier_values` rows, but they give one value to every generation's
  attriters and are no longer central. The central rule is the generation split below.]

| Gap | Observed (identifiers) | Attriters like identifiers | At measured non-identifier values | Attriters like whites |
|---|---|---|---|---|
| CPS G3+ BA+, points | −19.8 | −19.8 | −19.7 to −16.4 | −17.6 to −8.8 |
| CPS G3+ partial ledger, $ | −6,615 | −6,615 | −6,213 to −3,951 (years convention; superseded 2026-09-28) | −5,875 to −2,937 |
| CPS G3 obs. BA+ (both parents) | −9.7 | −9.7 | −9.6 to −8.0 | −8.6 to −7.0 |
| CPS G4+ obs. BA+ (both parents) | −10.1 | −10.1 | −10.0 to −6.7 | −9.0 to −4.5 |
| GSS G3 / G4+ BA+ | −17.4 / −19.0 | same | −17.3 to −15.6 / −19.0 to −15.6 | −15.4 to −12.5 / −16.9 to −8.5 |
| NLSY97 G3 / G4+ BA+ | −19.4 / −18.8 | same | −19.4 / −18.7 to −15.3 | −19.4 / −16.7 to −8.3 |
| NLSY97 G3 / G4+ years | −0.93 / −1.69 | same | −0.93 / −1.62 to −1.27 | −0.93 / −1.50 to −0.75 |

The CPS G3+ ranges apply the G3 and the G4+ rates to the whole G3+ cell. Their upper ends (the
55.6% rate) are extremes.

Attrition-corrected G3 → G4+ BA+ ratio:
- At measured non-identifier values, the ratio is 0.79–1.10 across sources and rate pairs. The
  central case is 0.92 (CPS), 1.03 (GSS) and 0.88 (NLSY97), using the CPS G3 rate, the
  Duncan–Trejo G4+ rate and NLSY97's +6.16.
  [2026-09-28: superseded as central; these are the flat advantages. Under the generation split
  (below) the ratio is 0.81–1.10, and the central case is 1.04 (CPS), 1.10 (GSS) and 0.89 (NLSY97).]
  [2026-10-05: at the monthly-frame C3, 0.86–1.10 and NLSY97 0.91. (g3_identity_pooled_2026_10_05, monthly
  frame)]
- If attriters look exactly like whites, the ratio falls to 0.69–0.87 at 29% G4+ attrition and
  0.43–0.61 at 56%.
  [2026-09-28: unchanged. It rests on the lane's convention that NLSY97's G3 needs no correction.
  Counting the 13.0% non-identifiers already in NLSY97's published G3, its 56% value is 0.47, not 0.43.]

The measured non-identifier advantage is small (0.6–6 BA points). Attrition therefore moves the
ratio materially only if many more G4+ descendants leave than any modern survey measures and
those who leave look like whites.
[2026-09-28: the split rule sharpens this. Later leavers close nothing, so the G4+ attrition rate
drops out of the ratio. Only the like-whites bound still moves it, and the one direct measurement
of later leavers (`carryover_identity_2026_09_27` §2: earnings $11–12k below identifiers, n 35–44)
cuts against that bound.]

**[2026-09-28] The generation-split rule, now central.** It comes from `carryover_identity_2026_09_27`
§2. [CALCULATION: `summarize.py` → `attrition_bounds.csv`, `attrition_corrected_rho.csv`, scenario
`attriters_generation_split_measured`; C3 is DATA copied from
`carryover_identity_2026_09_27/derived/corrected_step.csv`, and `verify.py` checks it for drift]

How it maps onto this lane, with a3 the G3-rate share of the hidden and C3 its closing share:
- *G3 cells:* lineage gap = gap × (1 − a3 C3), with a3 the row's G3 rate (central 11.2%).
- *G4+ cells:* the G4+ lineage holds the descendants of G3 attriters (share a3, at C3) and later
  losses (a4 − a3, which close nothing). The lineage gap is therefore gap × (1 − a3 C3), and the G4+
  attrition rate a4 drops out.
- *CPS pooled G3+:* gap × (1 − a3 C3), the level in `carryover_identity_2026_09_27` §1.
- *NLSY97 G3:* no correction, as in every other scenario, because its G3 is defined by the
  grandparents' birthplace. See Limits for the sensitivity.
- *C3:* the pooled same-sample G3 value, 0.776 (SE 0.644) on BA+ and 0.729 (0.677) on years. With
  CPS 2026 pooled in, it is 0.907 (0.612) and 1.023 (0.664). The ledger takes the BA+ value, because
  no G3 dollar measurement exists. [2026-10-05: the central is now 0.557 (SE 0.246) on BA+ and 0.687
  (0.228) on years: the IPUMS-CPS basic monthly frame 1994–2026 (526 unique G3 non-identifiers at 25+)
  pooled with NLSY97. The 2026 sensitivity is unchanged. (g3_identity_pooled_2026_10_05, monthly frame)]
- *Pairs:* the G3 → G4+ ratios keep the lane's rate pairs; the G4+ lineage takes the pair's G3 rate.

| Lineage gap under the split rule (SE) | Observed | G3 rate 11.2% | 20.6% / 28.2% | C3 with 2026, 11.2% |
|---|---|---|---|---|
| CPS G3+ BA+, points | −19.8 | −18.1 (1.6) | −16.6 / −15.5 | −17.8 |
| CPS G3+ partial ledger, $ | −6,615 | −6,041 (557) | −5,557 / −5,168 | −5,944 |
| CPS G3 / G4+ obs. BA+ (both parents) | −9.7 / −10.1 | −8.9 / −9.2 | −8.2 / −8.5, −7.6 / −7.9 | −8.7 / −9.1 |
| GSS G3 / G4+ BA+ | −17.4 / −19.0 | −15.9 / −17.4 | −14.6 / −16.0, −13.6 / −14.9 | −15.6 / −17.1 |
| NLSY97 G3 / G4+ BA+ | −19.4 / −18.8 | −19.4 / −17.1 | −19.4 / −15.8, −19.4 / −14.7 | −19.4 / −16.9 |
| NLSY97 G3 / G4+ years | −0.93 / −1.69 | −0.93 / −1.55 | −0.93 / −1.44, −0.93 / −1.34 | −0.93 / −1.50 |

[2026-10-05: at the monthly-frame C3 the 11.2% column reads −18.6 (0.9), −6,203 (348), −9.1 / −9.5,
−16.3 / −17.9, −19.4 / −17.6 and −0.93 / −1.56. The 20.6% / 28.2% column reads −17.5 / −16.7, −5,856 / −5,577,
−8.6 / −9.0 and −8.2 / −8.5, −15.4 / −16.9 and −14.7 / −16.0, −19.4 / −16.6 and −19.4 / −15.8, and −0.93 / −1.45
and −0.93 / −1.36. The 2026 column does not move. (g3_identity_pooled_2026_10_05, monthly frame;
`attrition_bounds.csv`)]

| G3 → G4+ ratio under the split rule | BA+ | Years | Household ledger |
|---|---|---|---|
| CPS, both parents | 1.04 at every rate pair | | 1.67 at every rate pair |
| GSS | 1.10 at every rate pair | 1.34 | |
| NLSY97, G3 rate 11.2% / 20.6% | 0.89 / 0.81 (0.87 / 0.79 with the 2026 C3) | 1.67 / 1.54 | |
| NLSY97, G3 as published (13.0% non-identifiers), any rate | 0.87 (0.85) | 1.64 (1.58) | |

[2026-10-05: at the monthly-frame C3 NLSY97 gives 0.91 / 0.86 on BA+ and 1.68 / 1.56 on years. As published
it gives 0.90 and 1.65. CPS, GSS and the 2026 values do not move. (g3_identity_pooled_2026_10_05, monthly frame;
`attrition_corrected_rho.csv`)]

Reading. Under the split rule, identity loss is a one-time level shift at G3: about 9% off the gap
(−$574 on the CPS G3+ ledger, SE $476 from C3 alone) at every generation from G3 on. It is not a
per-generation fade. CPS and GSS keep their observed G3 → G4+ ratios, because both cells scale
alike. NLSY97's ratio falls, because its G3 already contains its non-identifiers and only its G4+
takes the factor. The years convention gives the CPS household ledger 1.17–1.67
(`sensitivity_years_share_convention`); the flat BA+ advantages give 0.79–1.10.
[CALCULATION; INFERENCE for the reading]
[2026-10-05: at the monthly-frame C3 the shift is about 6% (−$412 on the CPS G3+ ledger, SE $182 from C3
alone). (g3_identity_pooled_2026_10_05, monthly frame)]

## 4. Projection to G4 and G5 [MODEL]

Measured inputs:
- CPS 2022–25 G3+ gaps: BA+ −19.8 points (SE 0.75) and partial ledger −$6,615 per adult (SE 317).
- NLSY97 G3 gap: −0.93 years.
- The observed ratios in section 2.
- The NLSY97 parent–child slope, β = 0.56 (Table 6 col 2, p.49: 0.28 mother + 0.28 father), and
  the conditional group residuals, δ = −0.31 (G3) and −0.87 (G4+).

Assumed inputs:
- Each path's ratio holds for G4 → G5.
- G4+/G5 attrition rates, which no survey measures.
- The fiscal gap scales with the schooling gap.
- G3+ stands in for G3. It already contains G4+, which is conservative for the stall path.
- [2026-09-28] Under the split rule, the descendants of G3 attriters keep C3 at every later
  generation, and later losses close nothing. The split paths and the worst case start from the
  lineage G3+ gap, not the identifiers'; the other paths remain per identifying descendant.

| Path (rho per step) | BA+ G4 / G5, points | Ledger G4 / G5, $ per adult | Years G4 / G5 |
|---|---|---|---|
| Measured base, G3+ | −19.8 | −6,615 | −0.93 |
| Stall, identifiers as observed (1.00) | −19.8 / −19.8 | −6,615 / −6,615 | −0.93 / −0.93 |
| Attrition-corrected central (0.98) [superseded 2026-09-28] | −19.3 / −18.9 | −6,468 / −6,323 | −0.91 / −0.89 |
| [2026-09-28] Generation split, central (1.01), per lineage descendant; lineage G3+ −18.1 / −$6,041 (SE 557) / −0.93 | −18.2 / −18.4 | −6,087 / −6,134 | −0.94 / −0.94 |
| [2026-09-28] Generation split, C3 with CPS 2026 (1.00); lineage G3+ −17.8 / −$5,944 / −0.93 | −17.8 / −17.9 | −5,961 / −5,979 | −0.93 / −0.94 |
| [2026-09-28] Flat NLSY97 advantage with NLSY97 included (0.94), sensitivity, identifiers' base | −18.7 / −17.6 | −6,245 / −5,895 | −0.88 / −0.83 |
| Recursion, G3 residual (0.89, 0.93) | −17.7 / −16.5 | −5,910 / −5,515 | −0.83 / −0.78; fixed point −0.70 |
| Resume NLSY97's G2→G3 step (0.76) | −15.1 / −11.5 | −5,038 / −3,837 | −0.71 / −0.54 |
| Recursion, no group residual (0.56) | −11.1 / −6.2 | −3,705 / −2,075 | −0.52 / −0.29 |
| Worst case for the stall reading: 1970 attrition (55.6%, 94.4%), attriters like whites (0.50, 0.13) [superseded 2026-09-28] | −9.9 / −1.2 | −3,307 / −417 | −0.46 / −0.06 |
| [2026-09-28] Same worst case from its lineage G3+ base (−17.6 / −$5,875 / −0.93) | −8.8 / −1.1 | −2,937 / −370 | −0.46 / −0.06 |
| Recursion, G4+ residual (1.50, 1.19), upper bound | −29.6 / −35.1 | −9,893 / −11,729 | −1.39 / −1.65; fixed point −1.98 |

[2026-10-05: at the monthly-frame C3 the generation-split central steps 1.02 a generation from a lineage G3+ of
−18.6 / −$6,203 (SE 348) / −0.93. It reads −18.8 / −19.1 on BA+, −6,300 / −6,398 on the ledger and
−0.94 / −0.96 in years. The other rows do not move. (g3_identity_pooled_2026_10_05, monthly frame;
`projection.csv`)]

[2026-09-28: two defects fixed with the split rule. (1) The attrition-corrected step selected
`attrition_G3 = 0.112`, which dropped NLSY97, whose G3 rows carry 0 by the lane's convention. So
its 0.98 was the mean of CPS 0.92 and GSS 1.03, although its label named NLSY97 too. With NLSY97
it is 0.94. `summarize.py` now selects the rate pair by its G4+ rate and asserts that all three
sources are present. (2) The worst case's basis defines the lineage gap as (1 − attrition) ×
identifiers' gap, but its steps ran from the identifiers' base, which put G4 at 0.500 × −$6,615
instead of 0.444 × −$6,615. It now starts from its lineage base. Years are unchanged, because the
NLSY97 base already counts its non-identifiers. `verify.py` gates both fixes.]

Reading. The paths consistent with the observed G4+ data (stall, attrition-corrected, G3
residual) put G4 at −$5.9k to −$6.6k and G5 at −$5.5k to −$6.6k.
[2026-09-28: unchanged with the split central (−$6.1k and −$6.1k per lineage descendant) in place
of the attrition-corrected path.] [2026-10-05: −$6.3k and −$6.4k at the monthly-frame C3, still inside
the range. (g3_identity_pooled_2026_10_05, monthly frame)] Only paths that assume
convergence the data do not show halve the gap by G5: pure regression to the mean, or attriters
who are exactly white in 1970-size numbers. The recursion's fixed point is the clearest way to
state it. With parents' schooling passed on at 0.56 and a persistent group residual of −0.31 to
−0.87 years, the gap settles at −0.7 to −2.0 years and does not go to zero.

This is per identifying (or lineage) descendant. Intermarriage dilutes Mexican ancestry per
descendant (27% of CPS G3 children have one Mexico-born grandparent), so these are gaps of
people counted as Mexican-origin, not of Mexican ancestry. [INFERENCE]

## 5. Disconfirmation: is the stall an artifact?

`disconfirm.py` → `derived/disconfirmation.csv`, `disconfirmation_composition.csv`.

| Candidate artifact | Test | Result |
|---|---|---|
| NM/CO Hispano (pre-1848/1920s) G4+ | CPS both-parents frame: G4+ in NM+CO 6.1% vs G3 2.2%; exclude NM and CO | G4+ − G3 on BA+ −1.7 (5.5); ledger −$2,123 (1,673); unchanged |
| Region / state composition | CPS: whites matched on age × sex × state group (CA, TX, NM, CO, AZ, rest). GSS: matched on census region | CPS BA+ −1.8 (6.0). GSS BA+ −2.0 (2.6), years −0.35 (0.22), employed −10.4 (4.0). Survives |
| Texas vs California | CPS within-state | Texas: G4+ ahead on BA+ (+9.5, SE 11). California: G4+ behind (−11.9, SE 8.2). Direction matches NLSY97's California-roots finding; neither is significant |
| Age | All gaps age × sex matched; GSS split 25–44 / 45–64 | BA+ G4+ − G3 −3.5 (3.5) young, +2.2 (4.3) old; less-than-HS worse in both halves |
| Period | GSS 2000–12 vs 2014–24 | Equal in 2000–12 (BA+ +0.8); G4+ worse in 2014–24 (BA+ −3.8, less-than-HS +17.6) |
| Co-residence selection | CPS compares only adults living with both parents, whites likewise | Symmetric by construction; G3 and G4+ ages 26.4/25.6 |
| Vintage / cohort of arrival | NLSY97 Tables 5, 15, 16 (pp.48, 59, 60) | Parents of G4+ have 0.2–0.4 fewer years than parents of G3. G4+ has California roots 10% vs 36%. Controls cut the G4+ deficit from −0.83 to −0.52 years (−37%), not to zero [SOURCE] |
| Attrition | Section 3 | Only at 1970-level G4+ attrition with white-like leavers does G4+ come out ahead of G3 |

What survives:
- No test turns up a G4+ advantage over G3. The stall is not a New Mexico/Colorado Hispano
  artifact and not a state-mix artifact.
- What cannot be excluded:
  - vintage: today's G4+ descends from pre-1930s, Texas-heavy migration with less-schooled
    parents;
  - G4+ attrition beyond anything measured today.
- Both would make the observed G4+ a pessimistic guide to the future G4 of today's G3. Neither can
  be tested with public data. [INFERENCE]

## Limits

- CPS observed G3/G4+ are adults aged 18–40 living with their parents. That frame is
  symmetric but not representative; 88% of G3+ adults (66% at all ages) stay unresolved (lane
  `generation_split_2026_09_20`).
- Pooled CPS years share households across adjacent ASECs, so n counts person-years. The SE uses
  a common replicate index; classification error is not in the SE.
- In GSS, G3 means a foreign grandparent of any country.
- MASP has no white sample. Its external GSS benchmark covers the nation, not LA and San Antonio,
  and is held fixed in the bootstrap.
- NLSY97 ratio SEs treat the gaps as independent despite the shared white reference.
- The partial ledger omits health, schools, other taxes and public goods. The adopted account's
  ratios are absolute, not gaps.
- [2026-09-28] NLSY97's full-sample G3 carries 13.0% non-identifiers, not its cross-section's
  20.6%, because the supplemental sample screened them out (Table 12 p.56, combined sample; the
  identity lane's §3). The lane keeps its convention of no NLSY97 G3 correction in every scenario.
  Counting those people by each scenario's own rule at NLSY97's own G3 rate gives a split-rule BA+
  ratio of 0.87 (0.85 with the 2026 C3) instead of 0.81–0.89 (0.79–0.87), and a like-whites 56% ratio of 0.47
  instead of 0.43 (`attrition_corrected_rho.csv`, scenario `sensitivity_nlsy97_g3_as_published`).
  [2026-10-05: at the monthly-frame C3, 0.90 instead of 0.86–0.91. (g3_identity_pooled_2026_10_05, monthly
  frame)]
- [2026-09-28] The split rule's C3 rests on 44–55 CPS adults and 11 NLSY97 adults (SE 0.61–0.64).
  It moves the lineage levels, not the CPS and GSS ratios. [2026-10-05: it now rests on 526 unique G3
  non-identifiers at 25+ in the CPS basic monthly files 1994–2026 and the same 11 NLSY97 adults (SE 0.25).
  (g3_identity_pooled_2026_10_05, monthly frame)]

## Files

Covered:
- Scripts: `analyze_cps.py` (imports `generation_split_2026_09_20/analyze_cps.py` masks and
  classifier; gate reproduced), `analyze_gss.py`, `analyze_masp.py` (copies the
  `masp_2026_09_20` reconstruction; gate on its principal counts), `disconfirm.py`,
  `summarize.py`, `verify.py`.
- Derived tables: `derived/gaps_by_generation.csv`, `carryover.csv`, `attrition_bounds.csv`,
  `attrition_corrected_rho.csv`, `projection.csv`, per-source CSVs, `disconfirmation*.csv`,
  `cps_audit_*.json`.
- Inputs: CPS ASEC 2022–2026 archives (existing lane caches), GSS 1972–2024 R3a, MASP combined
  file, Pew outcomes (pew_outcomes lane), population-total lane attrition tables, adopted-account
  CSV, and IZA DP12704 (fetched to `_cache/`, sha256 5e65103e6c2456bb2e60f116fbd135c970db4f17238f467bbd67cd92bd5fa9fb).
- [2026-09-28] `summarize.py` gained the generation-split rule, the NLSY97 sensitivity and the two
  projection fixes. The split rule's C3 values are constants copied from
  `carryover_identity_2026_09_27/derived/corrected_step.csv`. They are never read at build time,
  because that lane imports this one's `summarize.py` and `analyze_cps.py`. `verify.py` gained
  gates 7–9: a drift test of the constants against that CSV (tolerance 1e-4), the relabelled years
  convention, the split identities, the NLSY97 inclusion in the central step and the lineage bases.
  Table 12's combined-sample shares join the on-page check. New columns: `attrition_bounds.csv` has
  `lineage_gap_se`, `g3_rate_share`, `closing_share_g3` and `closing_share_g3_se`;
  `attrition_corrected_rho.csv` has `g3_rate_share_G4plus`.

Skipped:
- NLSY97 microdata re-estimation. The published tables answer the question, and the public file
  lacks exact grandparent-country fields (fourth-generation scope memo).
- PSID, excluded by `decisions/2026-09-20-ancestry-outcome-data-ceiling.md`.
- The MASP informant-code sensitivity, which rests on an unverified code mapping.
- A GSS NM/CO split, which is impossible because the public release codes four regions only.
- Adopted-account dollar projection, because the account has no white reference.

Reproduce, from the repo root (about 3 minutes total):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/analyze_cps.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/analyze_cps.py --years 2022,2023,2024,2025,2026 --label CPS_ASEC_2022_2026
uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/analyze_gss.py
uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/analyze_masp.py
uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/disconfirm.py
uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/summarize.py
uv run --no-project python3 infra/immigration-fiscal/generation_carryover_2026_09_27/verify.py   # all gates pass
```

The IZA PDF is fetched to `_cache/dp12704.pdf` (`curl -sS --fail -L https://docs.iza.org/dp12704.pdf`)
and converted with `pdftotext -layout`; `verify.py` reads the text.


## Progress log (appended as computed)

- 15:20 CPS gate passed: 2025 reported-linkage G3/G4+ weighted counts 2,869,946 / 2,073,497
  reproduce `generation_split_2026_09_20/derived/cps_generation_split.csv` (2.870m / 2.073m).
  [CALCULATION: `analyze_cps.py` → `derived/cps_audit_CPS_ASEC_2022_2025.json`]
- 15:25 CPS 2022–2025 pooled gaps computed (`derived/cps_gaps_CPS_ASEC_2022_2025.csv`,
  `cps_carryover_…csv`), plus 2022–2026 sensitivity. Interim reading: in the frame where G3 and
  G4+ are both observable (adults living with both biological parents, mean age 25–35), G4+ does
  not improve on G3 on BA+ (−10.1 vs −9.7 points against age/sex-matched co-resident whites), and
  sits lower on the household partial ledger; earnings differences are within noise.
- 15:30 NLSY97 read (IZA DP12704, PDF sha256 5e65103e…): Table 2 p.45 shows G4+ below G3 on every
  schooling measure except BA (20.81 vs 20.22).
- 15:45 GSS 2000–2024 (GRANBORN, generic foreign grandparent) computed with a 400-draw
  year×stratum×PSU cluster bootstrap (`derived/gss_gaps.csv`, `gss_carryover.csv`): G4+ trails G3
  on BA+ (−19.0 vs −17.4), less-than-HS (+14.1 vs +5.4), years (−1.34 vs −1.00), employment
  (−14.3 vs −4.0) and income; equal on occupational prestige.
- 15:50 MASP (1998–2002 adult children, family bootstrap, external GSS 2000–2004 white benchmark)
  computed (`derived/masp_gaps.csv`): BA+ G2 19.1%, G3 20.0%, G4+ 13.2% (n 38).
- 16:05 Disconfirmation run (`disconfirm.py` → `derived/disconfirmation.csv`,
  `disconfirmation_composition.csv`). CPS: G3 and G4+ have similar state mixes (CA 41/34%,
  TX 31/29%, NM+CO 2.2/6.1%); excluding NM/CO or matching whites on state leaves G4+ − G3 on BA+ at
  −1.7/−1.8 points (SE 5.5/6.0). GSS: region matching, South-only, period and age splits never
  show G4+ ahead of G3 on schooling; public GSS codes only four census regions, so NM/CO cannot be
  isolated there.
- 16:40 Attrition bounds, projection and verify.py gates complete; all gates pass.
- 2026-09-28 01:20 Generation-split rule made central (from `carryover_identity_2026_09_27` §2); the
  years convention kept as labelled sensitivity rows; the NLSY97 filter and the worst-case base fixed;
  the NLSY97 as-published sensitivity added. `scripts/rerun_lane.py` with the seven reproduce
  commands, run 1: every command rc 0 and verify passing (39 checks), with exactly
  `attrition_bounds.csv`, `attrition_corrected_rho.csv` and `projection.csv` CHANGED against HEAD
  (16/19 unchanged). Run 2: every command rc 0, IDENTICAL 19/19. The identity lane, which imports
  this `summarize.py`, still reproduces 14/14 (`corrected_step.py`, `verify.py`).
- 2026-10-05 16:35 C3 moved to the IPUMS-CPS basic monthly frame 1994–2026 pooled with NLSY97
  (g3_identity_pooled_2026_10_05, monthly frame): `SPLIT_C3` is keyed "pooled with CPS monthly 1994-2026
  (central)", BA+ 0.5567 (0.2457), years 0.6867 (0.2281), after `corrected_step.py` reran. The projection's
  path names now render C3 from `SPLIT_C3`. `verify.py` looks C3 up by label instead of parsing it from
  `delta_source`. All 39 checks pass. Only `attrition_bounds.csv`, `attrition_corrected_rho.csv` and
  `projection.csv` changed. `scripts/rerun_lane.py` (`summarize.py`, `verify.py`): IDENTICAL 28/28.

## Revisions — item T, October 8, 2026

`analyze_cps.py --income-tax-key` adds the measure `ledger_partial_plus_T_per_adult`: the partial
ledger plus the white-reference ledger's item T (added to `ledger_absolute_2026_09_17` on October 7),
which moves each record's survey income tax onto the main case's income-tax keys. T is taken at the
record from that lane's own `income_tax_keys` and `income_tax_item`, then shared among the unit's
adults like the other components. The keys exist for ASEC 2025 records only, so the flag refuses any
other years and the pooled frames above keep taxes as the survey reports them; they are unchanged.
The new run is `--years 2025 --label CPS_ASEC_2025 --income-tax-key`, which writes both ledger
measures on the 2025 frame. [DATA: `derived/cps_gaps_CPS_ASEC_2025.csv`,
`derived/cps_carryover_CPS_ASEC_2025.csv`]

Partial ledger gap per adult against age/sex-matched third-plus non-Hispanic whites, adults 25–64,
2024 dollars a year (SE):

| | pooled 2022–25, as published | 2025, survey taxes | 2025, with T |
|---|---:|---:|---:|
| G1 | −11,230 (227) | −10,911 (395) | −13,262 (726) |
| G2 | −7,331 (270) | −7,566 (466) | −9,119 (881) |
| G3+ | −6,615 (317) | −6,396 (526) | −7,637 (993) |
| ρ G1 → G2 | 0.653 (0.023) | 0.693 (0.039) | 0.688 (0.061) |
| ρ G2 → G3+ | 0.902 (0.048) | 0.845 (0.074) | 0.837 (0.115) |

On the same frame T widens every generation's gap, by $1.2–2.4k a year, and leaves the carry-over
ratios where they were. So the projection's steps hold and its starting level widens: the G3+ gap is
19% wider with T on 2025. The co-resident frames' small cells (observed G3, 117–210 records) carry T
on a few records, and their standard errors with T reach 5,841–9,895, so those rows say nothing.

At the record, T is $468.4bn nationally (federal $422.9bn, state $45.4bn). The ledger's shared
allocation gives $422.9bn in all (federal $385.6bn, state $37.2bn). The lines are the same; the
survey base differs, because equal splits within SPM units, weighted by members' unequal person
weights, raise the survey's federal tax before refundable credits from $1,981.1bn to $2,018.4bn.
[DATA: `derived/cps_audit_CPS_ASEC_2025.json` → `item_T` → `national_parts`;
`ledger_absolute_2026_09_17/derived/audit.json` → `item_metadata` → `T|central`]

Reproduce: `scripts/rerun_lane.py` over the seven commands above plus
`"uv run --no-project python3 {lane}/analyze_cps.py --years 2025 --label CPS_ASEC_2025 --income-tax-key"`
(third) ends `IDENTICAL: 32/32`.
