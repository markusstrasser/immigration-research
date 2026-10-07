# How far selection carries: Mexican-origin and Indian-origin descendants, G1 to G4+

**Verdict:** Across 78 origins, the first US-born generation keeps about half of its parents'
distance from the white mean: the G1→G2 rank slope is 0.52 on education and 0.55 on earnings
(entry 236). India sits above that line; its G2 is at the same education percentile as its G1 (73).
The Mexican-origin gap stalls after G2 rather than continuing to converge. The Indian G3 cell is
too thin to say the same (+$11.8k, se 8.2k; [Indian later generations](immigration-indian-later-generation-fiscal-2026-09-21.md)). For Mexican origin the G2 step is large at the bottom and small at the top. Then
the gap stalls: G2→G3+ carries about 0.9 of the gap on BA, earnings and the partial ledger, and
no source shows G4+ better than G3 (entry 232). With the hidden third generation put back, at the
closing share measured on 526 G3 non-identifiers in the CPS basic monthly files 1994–2026, the step is
about 0.86 on BA and 0.84–0.85 on earnings and the ledger (SE 0.04–0.07): identity loss explains about
6% of the ratio, and age cohort at least as much (§1). The civic record follows the same shape. Turnout
at equal SES is −10 for G2 and −9 for G3+, and spousal endogamy falls 90 → 72 → 56%. Attachment
to Mexico itself fades fast: "very connected" drops from 50% to 7% by G3+, and votes cast from
abroad are under 2% of Mexico-born adults (entries 233–234). The Indian advantage is a shift of
the whole upper three-quarters of the distribution, not a top-1% effect. It sits at US
percentile 73 in both G1 and G2 on education. A Mexican parent admitted late through the IR-5
route is a remaining-lifetime net cost of $267–285k at 3%, and Mexico sends a quarter of these
admissions (entry 235). [CALCULATION: the five lanes below; INFERENCE for the synthesis]

September 27, 2026. Frame: descriptive generation comparisons in repeated cross-sections, each
against third-plus-generation non-Hispanic whites of the same age. These are synthetic cohorts,
not the same families followed over time. Nothing here identifies why the gaps persist. On this
politically charged topic, the instrument's bias caveat applies (`notes/llm-bias-caveat.md`).
In the Indian coordination lane, the first verdict erred in the benign direction.

Lanes, each re-run by the parent with byte-identical outputs:
[`generation_carryover_2026_09_27`](../infra/immigration-fiscal/generation_carryover_2026_09_27/RESULT.md) (e2eeb0d),
[`civic_trajectory_mexican_2026_09_27`](../infra/immigration-fiscal/civic_trajectory_mexican_2026_09_27/RESULT.md) (2fbc8d9),
[`origin_attachment_mexico_2026_09_27`](../infra/immigration-fiscal/origin_attachment_mexico_2026_09_27/RESULT.md) (3f873b6),
[`late_arrival_tail_2026_09_27`](../infra/immigration-fiscal/late_arrival_tail_2026_09_27/RESULT.md) (95fec31),
[`selection_curve_2026_09_27`](../infra/immigration-fiscal/selection_curve_2026_09_27/RESULT.md) (97bd021).

## 1. Carry-over of the Mexican-origin gap, generation to generation

ρ is the next generation's gap divided by the previous one's. 0 means fully closed and 1 means
no progress. CPS ASEC 2022–2025, adults 25–64, same-age white reference; GSS 2000–2024; NLSY97
from Duncan, Grogger, Leon & Trejo (IZA DP12704, Table 2 p.45; figures checked against the PDF
text). [DATA: `generation_carryover_2026_09_27/derived/carryover.csv`]

| Measure | G1→G2 | G2→G3+ | G3→G4+ (BA) |
|---|---|---|---|
| Less than high school, CPS | 0.17 | — | G4+ worse in NLSY97 and GSS |
| BA+, CPS / GSS / NLSY97 | 0.64 / 0.68 / 0.83 | 0.92 / 1.02 / 0.76 | 1.04 (CPS co-resident) / 1.10 / 0.97 |
| Worker earnings, CPS | 0.39–0.45 | 0.88–0.90 | — |
| Partial ledger per adult, CPS | 0.65 | 0.90 | — |

The partial-ledger gap for G3+ is −$6,615 per adult a year. That object is the CPS partial
ledger (modelled taxes minus selected transfers), not the complete account. The adopted
account's own split (entry 224) has no reference group; on the September 27 case its absolute
ratios under the NAS convention are 0.72/0.65 (G1→G2) and 0.94/1.16 (G2→G3+) at the low and high
ends (0.66/0.56 and 0.88/1.16 on the schools case). The two must not be combined (FAQ,
"Before combining numbers").

NLSY97 is the one source that separates G3 by grandparents' birthplace. It shows real progress
from G2 to G3 in that birth cohort (G3 high-school completion 84.3% against 86.1% for whites),
then a fall at G4+ (68.1%). Counting a GED as completion closes the G3 gap entirely.

**Disconfirmation.** The stall survives dropping New Mexico and Colorado, matching whites by
state or region, and splitting by age and survey period. Two explanations are not excluded.
Vintage: today's adult G4+ descend from pre-1930s, Texas-heavy migration, and their parents had
0.2–0.4 fewer years of schooling; NLSY97 controls cut the G4+ deficit by 37%. Identity loss is
tested on the same sample (`carryover_identity_2026_09_27`, entry 232), with the closing share
measured on the CPS basic monthly files (`g3_identity_pooled_2026_10_05`, monthly frame):
- *The G2 side.* It needs no correction: CPS G2 is defined by a parent's birthplace, and 7.0% of it
  already does not report Mexican origin.
- *Third-generation non-identifiers.* In CPS adults living with a parent, G3 is defined by a
  Mexico-born grandparent, and 11% do not report Mexican origin. The CPS basic monthly files
  1994–2026 (MIS 1 and 5) find 526 unique G3 non-identifiers at 25+. They close 0.57 (SE 0.26) of the
  BA+ gap, and 0.56 (0.25) pooled with NLSY97. The design called for about 540, so the sample is
  close to that, but the SE stays wide.
- *Later leavers.* Adults who drop the identity one generation later are not ahead of identifiers:
  earnings are $11–12k lower (n 35–44). Losses past G3 therefore move nothing, whether 17.5% or 23%
  are hidden. Valued by this split rule (406a2d4), identity loss is a one-time level shift of about
  6% from G3 on, not a per-generation fade, and the G3→G4+ ratio is 0.86–1.10 (NLSY97 0.91) if the
  hidden look like the measured non-identifiers. If they look exactly like whites, it is 0.69–0.87
  at 29% attrition and 0.43–0.61 at 56%, bounds that lose their best support because the later
  leavers measure no better than identifiers.
- *Corrected G2→G3+.* About 0.86 on BA+ and 0.84 / 0.85 on earnings and the ledger (SE 0.04–0.07),
  against 0.92 / 0.90 / 0.90 among identifiers, so the gap shrinks by 14–16% from G2 to G3+. The
  bounds run from 0.92 (hidden like identifiers) to 0.69–0.76 (all hidden like whites).
- *Cohort.* It explains at least as much as identity: the identifiers' BA+ ratio is 0.87 at 25–44,
  0.83 for the 1979–85 birth cohort and 1.06–1.12 at 45–64, where G2 sits unusually close to whites.
  Of the 0.16 between CPS (0.92) and NLSY97 (0.76), about 0.09 is cohort and 0.05 attrition within
  NLSY97.
- *The attriters' dollar convention.* A 54–72% dollar closing share is a years-of-schooling ratio.
  On the same 669 G2 adults, non-identifiers close 0.17–0.27 of the BA+, years, earnings and ledger
  gaps alike.

The observed G3/G4+ adults in CPS are young and living with their parents (n 151 and 302 for BA at
25+).

**Tension with the literature.** Published group-level carry-over is 0.4–0.6 per generation
(Borjas 1992–94; Card, DiNardo & Estes; Ward 2020 gives 0.57–0.74 for G2→G3). The Mexican G2→G3+
value of about 0.9 sits well above that range. The historical estimates come mostly from European
groups that later married out and stopped identifying. Which of the two describes today's
Mexican-origin lineages is open. [SOURCE: `selection_curve_2026_09_27/literature_reads.md`, table
and page per figure]

**Projection** [MODEL]: with attriters valued by the measured split rule (406a2d4) at the
monthly-frame closing share, the central is −$6.3k at G4 and −$6.4k at G5 per lineage descendant a
year on the partial ledger, from a lineage G3+ gap of −$6,203. The band runs from −$3.7k / −$2.1k
(the gap regresses toward the white mean at the literature's rate) to −$6.6k / −$6.6k (full stall).
Only 1970-level identity loss with white-like leavers pushes G5 near zero.

## 2. Civic attachment and marriage by generation, Mexican origin

CPS November 2020/22/24 (turnout within 0.05 points of Census's published tables), CPS ASEC
2022–25 spouse linkage (100% of spouse records found), CPS September 2021/23 for volunteering
and giving. [DATA: `civic_trajectory_mexican_2026_09_27/derived/`]

| Gap vs NH whites, points | G1 (naturalized) | G2 | G3+ |
|---|---|---|---|
| Turnout, raw | −24.1 | −23.5 | −19.3 |
| Turnout, equal age, sex, schooling, income, state | −12.7 | −9.8 | −9.4 |
| Spouse is Mexican-origin (share, not a gap) | 90.2% | 72.3% | 55.9% |
| Same, excess over random matching within state | 68 | 47 | 31 |

- **Turnout.** CPS overstates Hispanic turnout more than white turnout (Ansolabehere, Fraga &
  Schaffner, *JOP* 84(3), 2022), so these gaps are lower bounds.
- **Composition.** About half of each G3+ civic gap is SES composition. What persists at equal
  SES is turnout −9, volunteering −5 to −6 and giving −6 to −8. Endogamy does not shrink with SES.
- **Military.** The veteran gap among Mexican-origin men disappears at equal SES from G2. Women
  (0.98) and young men now on active duty (0.98) serve at the white rate. This differs from Indian
  ancestry, whose 0.16× survives every SES control (ladder 205).
- **Identification.** Children of a Mexican-origin and a non-Hispanic parent are reported Hispanic
  84% of the time. At the level of all children with a Mexican-origin parent, the loss at birth
  grows with the parent's generation: not reported Hispanic 2.8 / 6.8 / 9.0% and not reported
  Mexican 7.8 / 15.1 / 12.0% for G1 / G2 / G3+ parents. The lineage model's 0.888 identification
  for G4+ assumes the loss stops after G3; one more step gives about 0.78.
  [CALCULATION: `civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv`; corrected
  2026-09-27 after audit 3db388d]
- **Indian comparison, same code.** India-born spousal endogamy is 96.3%, falling to 65.5% in the
  Indian G2. In raw share, Indian G2 marry out more than Mexican G2. Relative to a pool that is about
  1.5% of residents, they remain the more endogamous group.

## 3. Attachment to Mexico

- **Law.** Under Art. 37 A of the Mexican constitution, no Mexican by birth can lose that
  nationality. Since the 17 May 2021 reform of Art. 30 A II, anyone born abroad to a Mexican
  parent is Mexican by birth, so nationality by descent runs every generation. Before the reform
  it stopped at the migrant's US-born child. India ends citizenship on naturalization (Citizenship
  Act s.9), and OCI holders cannot register to vote. [SOURCE: SCJN article history PDF; indiacode;
  archived in the lane's `sources/`]
- **Uptake is small.** Votes cast from abroad worldwide were 184,326 in 2024, under 2% of the 10.69M
  Mexico-born adults in the US. 61.9% of eligible Mexican green-card holders have naturalized,
  against 74.5% for all origins and 84.5% for India (ACS 2024 over OHSS Table 2b). In Pew's 2012
  survey, none of 415 Mexican noncitizens gave keeping Mexican citizenship as the reason they had
  not naturalized.
- **By generation** (Pew NSL 2011–2018, self-identified Hispanics only; those who stop identifying
  are missing, which flatters attachment in later generations):
  - Calling themselves by the origin-country term falls from 66–71% to 21–32%.
  - Calling themselves "American" rises from 3–7% to 46–55%.
  - Feeling very connected to Mexico falls from 50% to 7%.
  - Following Mexican news very closely falls from 42% to 16%.
- **Not measured.** Registrations of US-born people as Mexican nationals, and matrícula counts (the
  Mexican foreign ministry's open-data files blocked the fetch).

## 4. The late-arrival tail: sponsored parents

- **Flow.** Mexico sent 36,652 IR-5 parents a year over FY2015–2024 and 63,050 in FY2024, about a
  quarter of all such admissions and three times India (18,910). The flow doubled after 2019.
  [SOURCE: OHSS country × class workbook; gates against Yearbook Table 6, 128/128 pass]
- **Receipt.** 13.6% of Mexico-born people 65+ arrived at 50 or older. Against Mexico-born seniors
  who arrived younger, they report:
  - Medicaid 40 vs 32%
  - SSI 10.2 vs 8.7%
  - Social Security 47 vs 73%
  - Not a citizen 70%
  - Living as the householder's parent 48%

  India's late arrivals show wider Medicaid (38.7 vs 13.0%) and SSI gaps. [DATA: ACS 2019–2023;
  B05006 gates within 0.6%]
- **Value per admission.** Admitted at 55 / 60 / 65, a Mexican parent is a remaining-lifetime net
  cost of $267k / $273k / $285k at 3% (range $252–337k), close to Australia's official A$335–410k.
  Against a same-age white resident's remaining lifetime, the parent costs more at 55 and less at
  65, because white retirees draw earned Social Security and Medicare. One FY2024 cohort carries
  about $16bn at 3%. This is a flow valuation; the annual account already contains these residents.
  Most Mexican immediate relatives now adjust status inside the US (107k of 149k in FY2024;
  33% of Mexican IR-5 parents in NIS-2003). For a parent who already lived here, the admission
  changes eligibility rather than adding a person, so these values are upper bounds for that share.
  The five-year bar and sponsor-income deeming were applied from the lane's recollection of the
  statutes, not a re-read text [UNVERIFIED citation]; the 0.65 Medicare weight is an assumption
  (0.55–0.75 in the low and high cases).
- **Offset.** The childcare offset is real in sign and small: about $120–380 a year in taxes per
  co-resident parent, during preschool years only. The mother's earnings are an assumption.
  [SOURCE: Hu 2018 Table 3; Compton & Pollak; Productivity Commission 2016, `reads/offset_reads.md`]

- **Fraud or birth cohorts? (entry 242).** The FY2019–24 doubling (34k → 63k) matches every other
  country (+84% vs +79%); it is post-COVID processing. The level follows US births to Mexico-born
  mothers 21 years earlier. Mexico converts births into parent green cards at a lower rate than
  other origins, as the law predicts for parents who crossed without inspection. No parent-petition
  fraud rate has ever been measured; a fraud wave is excluded, a steady low rate is not.

### 4a. Sponsored parents inside the annual account and the lineage (entries 240–241)

- **Annual account.** Mexico-born residents who arrived at 50+ (399k; 227k now 65+) cost other residents
  $5.66–5.80bn a year on the September 27 case, 1.5–1.8% of it. Per head at 65+ they cost less than
  Mexico-born seniors who came younger ($19.6–21.6k vs $21.7–24.3k): in a one-year account, the
  earlier arrivals' earned Social Security outweighs the late arrivals' lower taxes. "Did not pay in"
  shows in the lifetime view (entry 235), not the annual one. Medicare is overcharged to them by the
  pooled keying (−$0.31bn proposed).
- **Lineage.** At the calibrated petition rate the channel adds $24.4k per founder undiscounted,
  1.7% of the century lineage gap (2.1% at 3%). A US-born child's petition legalizing the founder
  adds −$386k undiscounted against a founder who stays unauthorized under statutory rules. That is
  the priced chain from birthright citizenship to a parent's green card. [DATA:
  `lineage_sponsored_parents_2026_09_27/derived/arms.csv`] The 1.7% is a scenario, not an observed
  lifetime rate (conceptual audit, second pass §D):
  - The 0.619 naturalization probability is today's naturalized share of the eligible stock, not
    the chance that a newly admitted founder ever naturalizes.
  - The two petition-rate estimators share their admissions numerator, so their 9% agreement
    (1.089) is a scale check, not validation.
  - Timing alone moves the channel. At fixed probabilities, the audit found that admitting the
    parent in founder-year 10 or 16 instead of 6 lowers it from $24.5k to $22.0k or $15.7k per
    founder, undiscounted, before item T, which moves the year-6 value to $24.4k.
  - The channel can stay small under these assumptions, but its size needs cohort naturalization
    and petition hazards, which no source here measures.

## 5. The selection curve, and whether the Indian advantage is a tail

- **Not a tail.** Capping everyone's earnings at the white p99 keeps 92% of the India-born
  earnings gap. Dropping everyone above the white p99 keeps 94% of the partial fiscal gap
  (+$10,086 of +$10,732). The India-born median earnings percentile is 70 against the white 50,
  and p75 is 91 against 75. On education the whole distribution above p10 is shifted. China is
  the exception: its advantage sits above the white p90, and its median is below the white median.
  The public CPS topcodes the extreme tail, so "without the top 1%" means without the top 1% the
  survey can see.
- **G1→G2 across 78 origins.** The slope is 0.52 on education (0.29–0.59 over origins) and 0.55 on
  earnings, on top of a common uplift of about 5 points. Without Mexico, the high-leverage point,
  the slopes are 0.36 and 0.30. Mexico's G2 sits 8 points below the line the other 77 draw.
  The point estimates are steeper below the white median than above it (education 0.68 vs 0.31),
  but a paired origin bootstrap cannot distinguish them from a straight line (difference 0.374,
  −0.116 to 0.825). Unweighted across origins the slopes are 0.45 and 0.47; leave-one-out moves
  them much only for Mexico.
- **Selection within the origin country** (Barro-Lee, Wittgenstein) works through where adult
  arrivals land. Among G1 who arrived at 25 or older, their percentile at home predicts their US
  position (slope 1.19, 0.45–1.75, R² 0.28 without Mexico); child arrivals, whose schooling may be
  US-acquired, carry no signal (R² 0.00), which is what diluted the pooled figure (R² 0.10–0.12).
  Given the G1's US position, selection adds nothing distinguishable to G2 (0.12, −0.22 to 0.38).
  [CALCULATION: `selection_curve_2026_09_27/derived/selection_arms.csv`; corrected 2026-09-27 after
  audit 3db388d]
- **G2→G3.** GSS gives 0.72 on education (0.56 without Mexico); the literature gives 0.46–0.53. The
  curve [MODEL]: India 95 → 73 → 73 → about 67; Mexico 59 → 16 → 36 → about 40. Mexico's observed G3
  stalls near its G2, so the model overstates its convergence.

## 6. What this does and does not settle

Settled at the descriptive level:
- The G2 step is large and the post-G2 path is flat for Mexican origin on every source that
  separates G3 from G4+.
- Attachment to Mexico fades by G3.
- The remaining civic gaps are half class composition.
- The Indian advantage is broad, not tail-driven.

Not settled:
- Why the Mexican path stalls: vintage, identity loss, ethnic capital, or discrimination. Identity
  loss is sized at about 6% of the G2→G3+ ratio and cohort at least as much (§1); vintage, ethnic
  capital and discrimination remain unseparated.
- Whether the historical 0.5 carry-over or today's 0.9 will describe the next two generations.
- The within-India selection step: caste is not recorded in US surveys.
- What the Indian G2 who marry out marry into, which decides how long the Indian level holds.

## Revisions

- 2026-09-27: created from five lanes; ladder entries 232–236.
- 2026-09-27, later: §4a added from entries 240–241 (late arrivals in the account; the lineage channel).
- 2026-09-27, late: corrected after the conceptual audit (3db388d): selection within origin is measured on adult arrivals, the slope asymmetry is not significant, and identity loss grows with the parent's generation (lineage 0.888 too high for G4+).
- 2026-09-27, late: §4 gained the IR-5 fraud-versus-cohort test (entry 242).
- 2026-09-27, late: §4a's lineage figure is narrowed after the conceptual audit's second pass (§D): the 1.9% is a calibrated scenario, not an observed lifetime petition rate, and timing alone moves the channel. Concept affected: the sponsored-parent channel's size.
- 2026-09-28: §1 gained the identity-loss test of the G2 stall (`carryover_identity_2026_09_27`, entry 232): G2→G3+ is about 0.84 / 0.82 with the hidden third generation put back, cohort matters about as much, and the attriters' 54–72% dollar convention is a years-of-schooling ratio. Concept affected: Mexican-origin carry-over after G2.
- 2026-09-28, later: §1's G3→G4+ range and projection central follow the carry-over lane's measured split rule for attriters (406a2d4): 0.81–1.10, central −$6.1k at G4 and G5. Concept affected: identity loss in the Mexican-origin projection.
- 2026-10-05: §1's identity-loss figures follow C3 measured on the CPS basic monthly files 1994–2026 (526 unique G3 non-identifiers at 25+) pooled with NLSY97, 0.557 (SE 0.246) in place of 0.78 ([g3_identity_pooled_2026_10_05](../infra/immigration-fiscal/g3_identity_pooled_2026_10_05/RESULT.md), monthly frame): G2→G3+ is 0.86 / 0.84 / 0.85 with the hidden third generation put back, identity loss explains about 6% of the ratio, NLSY97's split G3→G4+ is 0.91, and the projection central is −$6.3k at G4 and −$6.4k at G5. Concept affected: Mexican-origin carry-over after G2.
- 2026-10-08: restated the IR-5 parent's value per admission and the sponsored-parent channel's share of the lineage gap, because the white-reference ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T; [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)) and the late-arrival and lineage lanes' profiles carry it: at 3%, admitted at 55 / 60 / 65, $270k / $275k / $286k → $267k / $273k / $285k (range $254–339k → $252–337k); the calibrated channel 1.9% → 1.7% of the lineage gap, nearly unchanged in dollars. The comparison with a same-age white resident keeps its direction (the parent costs more at 55 and less at 65) and the FY2024 cohort stays about $16bn at 3%; §1's partial-ledger projection does not move. Concept affected: the sponsored-parent channel's size.
- 2026-10-08, later: rewrote the verdict, §1, the projection, §4a and §6 to their current state. Their twelve dated brackets (2026-09-27 late, 2026-09-28, 2026-10-05 and 2026-10-08) became current text, and the superseded values are deleted: the 0.78 closing share, the 0.84 / 0.82 step, the "tenth" and "sixth", the 0.79–1.10 and 0.81–1.10 ranges with the 9% level shift, the −$6.5k / −$6.3k per-adult and −$6.1k centrals, and the 1.9% channel. The entries above and git keep them. No current figure changes; the timing bullet in §4a is labelled as the audit's values before item T. Concept affected: none; the trajectory's presentation.
