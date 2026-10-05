claude-opus-5-5

**Verdict:** Candidate main case v5 is not adopted. It is v4 plus the descendants of Mexican immigrants whom the account misses because they no longer report Mexican origin.

**Central case.** On arm b, 3.04M added people on the account's frame make a 42.75M lineage.

| | Set ($bn a year) | Change from v4 | Per member | Cash set ($bn) | Change | Cash per member |
|---|---|---|---|---|---|---|
| v4 | 371.4–434.8 | — | $9,353–10,950 | 294.7–361.8 | — | $7,421–9,111 |
| **arm b (central)** | **390.3–461.2** | **+18.9–26.4** | **$9,129–10,789** | **307.4–383.4** | **+12.7–21.6** | **$7,190–8,968** |
| arm a (1.81M added) | 380.4–447.6 | — | $9,161–10,779 | 300.2–371.7 | — | $7,231–8,952 |
| arm c (4.27M added) | 400.2–474.9 | — | $9,099–10,797 | 314.5–395.1 | — | $7,151–8,984 |

[CALCULATION: `derived/v5_summary.json`]

The cash set counts benefits when they are paid.

**Cost per added person.** On the set an added person costs others $6,309–8,790; in cash, $4,268–7,207. That is below the account's average member, so the per-member figure falls while the total rises. The parts on the set:

| Part | Set |
|---|---|
| Later losses, priced as identified G3+ members | $8,541–11,731 |
| Attriters lost at the G3 rate: (1 − C3) × G3+ + C3 × W | $5,052–7,133 |
| W, third-plus non-Hispanic white at the identified G3+'s ages | $2,274–3,472 (cash $682–1,880) |

C3 is 0.5567 (SE 0.2457), imported at run time from the "(central)" entry of `generation_carryover_2026_09_27/summarize.py`.

**Checks.** 175 gates pass. The lane's rerun is IDENTICAL (21/21 files, exit 0).

**[FRAMING-SENSITIVE] Mixed ancestry: three alternatives to whole persons.**

| Alternative (arm b) | Set ($bn) | Change from v4 | Cash ($bn) |
|---|---|---|---|
| Replacement child, r = 1 | 383.38–450.69 | +11.97–15.85 | 305.30–377.70 |
| Replacement child, r = 0.5 | 386.84–455.97 | +15.43–21.13 | 306.34–380.55 |
| Fractional, whole lineage | 320.4–367.2 | not comparable to v4 | 256.4–303.7 |
| Fractional, attriters only | 378.9–445.4 | +7.5–10.6 | — |

- **Replacement.** Without the immigration, a native parent of a mixed descendant would likely have had a child anyway, with another native. The rows net r × W × added people off the band.
- **Fractional.** This is the people-conserving lineage count: each person counts by their share of Mexican-immigrant ancestry, and the counted people total 34.36M.
  - v4 itself counts as $312.9–356.7bn on 33.12M counted people.
  - The third-plus share dominates the result. Its full bounds give $239.6–422.1bn.
- **Fractional, attriters only.** Union members stay whole and only the added people are weighted.

What is measured and what is assumed:

- **Measured:**
  - The identified G3+ member's cost under v4's rules: $8,548.89 / 11,739.52. It comes from the engine, convention (a).
  - Whites' amounts line by line, from the white lane's re-key of CPS ASEC and MEPS onto v4's lines (not an engine run).
  - The self-identified third-plus count, and the third-generation identification rate of 0.888.
  - C3: the share of the identifiers' BA+ gap that third-generation adults who do not identify close. It pools CPS basic monthly 1994–2026 co-resident adults with NLSY97.
  - Parents' and co-resident grandparents' birthplaces for the fractional count.
- **Assumed:**
  - How identity loss continues past the third generation. This sets the count: 1.81–4.27M across arms a–c.
  - BA+ stands in for dollars in C3.
  - Later losses close none of the gap.
  - The added people are civilians in the identified G3+'s proportion, and they live where the group lives.
  - Lines and production scale linearly with members.
  - In the fractional count, the ancestry of parents and grandparents the CPS does not show.
- **[FRAMING-SENSITIVE] Whole people.** The central counts every person once, at their own measured cost. The replacement and fractional rows above are the alternatives.
- **[FRAMING-SENSITIVE] Age mix.** The added people are priced at the identified G3+'s age mix, with whites at the same ages. The bias most likely runs toward understating the cost, by little at today's rates [INFERENCE]. The reasons:
  - Younger people cost more. G3 minors cost others $12,438 / 21,014 a head, against $8,549 / 11,740 for the average G3+ member; in cash, $9,143 / 21,050 against $6,260 / 10,162. [CALCULATION: `generation_account_2026_09_24/derived/generation_results_sept29*.csv`, convention (a) − (b), over 2,511,081 minors]
  - In 1994–2006, 28% of third-generation children went unidentified, against 15–19% of adults. [SOURCE: `g3_identity_pooled_2026_10_05/RESULT.md` M5]
  - Today the rate is about 11% at every age. [SOURCE: ladder 158]
  - A younger mix raises both ends of the attriters' blend.

## 1. v5 by population arm

| Set | Arm | Added (M) | Band ($bn) | Change from v4 | Per member |
|---|---|---|---|---|---|
| set | v4 | — | 371.41 / 434.84 | — | $9,353 / 10,950 |
| set | floor | 0.80 | 375.38 / 440.47 | +3.97 / +5.63 | $9,266 / 10,873 |
| set | a | 1.81 | 380.37 / 447.55 | +8.96 / +12.71 | $9,161 / 10,779 |
| set | **b (central)** | 3.04 | 390.29 / 461.24 | +18.88 / +26.40 | $9,129 / 10,789 |
| set | c | 4.27 | 400.21 / 474.93 | +28.80 / +40.09 | $9,099 / 10,797 |
| cash | v4 | — | 294.70 / 361.82 | — | $7,421 / 9,111 |
| cash | floor | 0.80 | 297.15 / 366.18 | +2.45 / +4.36 | $7,335 / 9,039 |
| cash | a | 1.81 | 300.22 / 371.66 | +5.52 / +9.84 | $7,231 / 8,952 |
| cash | **b (central)** | 3.04 | 307.38 / 383.41 | +12.68 / +21.59 | $7,190 / 8,968 |
| cash | c | 4.27 | 314.52 / 395.15 | +19.82 / +33.33 | $7,151 / 8,984 |

[CALCULATION: `derived/v5_summary.json`, `derived/v5_bands.csv`]

- Each band runs from specification 48 (shared allocation, low reading) to 11 (personal, high reading). Every arm keeps these ends (gate).
- Changes are differences of the printed bands.
- Per member divides by 39,712,493 plus the added people.

## 2. Who is added

| Arm | Rule (population lane) | Added, CPS frame | Account frame | At the G3 rate | Later losses | Lineage, account frame |
|---|---|---|---|---|---|---|
| floor | third generation only, measured | 0.8017M | 0.7994M | 0.7994M | 0 | 40.51M |
| a | G4+ identify at the G3 rate | 1.8121M | 1.8070M | 1.8070M | 0 | 41.52M |
| **b** | one more step (G4+ rate 0.781) | 3.0483M | 3.0397M | 1.9449M | 1.0948M | 42.75M |
| c | compounding, ρ 0.5 | 4.2845M | 4.2725M | 2.0828M | 2.1897M | 43.98M |

[DATA: `identity_loss_propagation_2026_09_27/derived/population_arms.csv`; floor: `mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv`; CALCULATION: `derived/population_arms_account.csv`]

- **Split rule.** The split is the population lane's, `bounds_coverage_fiscal.py` arm 5:
  - At the G3 rate: min(added, (1 − p3) × corrected third-plus), with p3 = 0.8881. This includes the descendants of G3 attriters.
  - Later losses: everyone else.

  A gate rederives the split. The brief's first reading put only the floor's 0.80M at the G3 rate. That misread the rule, so it is not priced.
- **Frame factor, 0.997189.** This is the account's civilian G3+ (14,342,574.6) over the CPS self-identified third-plus (14,383,006.5); the gap is the armed forces.
  - Audit row 4 reweights only the Mexico-born outside California and Texas, so US-born people keep their CPS weights.
  - The union ratio 39.71 / 40.97 (0.9694) is recorded as `union_ratio_not_used`.
- **Group size.** The added people raise the group's share of residents, s, from 0.1202 to 0.1292 on arm b. The metro shares behind the property-price step scale by 1.0771.

## 3. How the line is priced

The engine evaluates an augmented group. `lineage_case.cjs` adds the people as cell edits on the v4 union:

- **G3+ members.** There are m_G = later + (1 − C3) × G3-rate of them. Each takes the corrected G3+ model's amount in every cell and allocation, per member, plus its production grid.
- **Whites.** There are m_W = C3 × G3-rate of them. Each takes W's amount in every cell of its line.
- **Row 8.** Its edit moves with the group's share: −$0.008bn on arm b.

The case's 64 specifications are then evaluated with the group-size responses recomputed at the larger group. Each response is the stored v4 value plus (formula at the new s − formula at v4's s), so zero added people give v4 to the last bit.

| Response | v4 | v5, arm b |
|---|---|---|
| General government, low / high | 0.600046 / 0.850396 | 0.600527 / 0.851054 |
| Row 8 factor | 0.949163 | 0.945169 |
| Economic affairs, low / high | 0.384015 / 0.638646 | 0.384499 / 0.638740 |
| Recreation and culture (also its state price), low | 0.856175 | 0.856391 |
| State and local highways (also road miles), low | 0.739205 | 0.740198 |
| Owner-occupied property, long run | 0.762903 | 0.772699 |
| Tenant-occupied property, long run | 0.708443 | 0.718912 |

[CALCULATION: `derived/lineage_payload.json` meta.responses against `main_case_2026_09_29/derived/corrections.json`]

| Per person, arm b | Set | Cash |
|---|---|---|
| Identified G3+ member, at the larger group's responses | $8,541 / 11,731 | $6,252 / 10,154 |
| W: third-plus non-Hispanic white at G3+ ages | $2,274 / 3,472 | $682 / 1,880 |
| G3-rate attriter, (1 − C3) × G3+ + C3 × W | $5,052 / 7,133 | $3,151 / 5,548 |
| Added person, average | $6,309 / 8,790 | $4,268 / 7,207 |
| Third-plus white at their own ages (beside) | $596 / 1,851 | $2,448 / 3,702 |

- **Why W is at the G3+'s ages.** C3 is measured on gaps matched by age and sex, so W is whites at the attriters' assumed ages. `white_lines.py` reweights the white lane's CPS and MEPS persons to the identified G3+'s five-year age structure.
- **Production.** Whites carry none.

**Route gap.** The fallback the brief names prices the same people per line at v4's responses. It gives $390.62 / 461.59bn on the set and $307.70 / 383.75bn in cash, which is $0.33 / 0.34bn above the engine route.

- $0.30 / 0.32bn of the gap is the union's own response move. The larger group's removal lowers metro property prices more, so the union's owner and tenant property taxes count for more: −$0.24bn and −$0.10bn.
- The rest is the added people's own lines at the new responses.

## 4. The lineage line by part and line (arm b)

| Part ($bn) | Set low | Set high | Cash low | Cash high |
|---|---|---|---|---|
| receipts: union response move | −0.3 | −0.3 | −0.3 | −0.3 |
| receipts: G3+ members | −26.1 | −21.4 | −26.3 | −21.5 |
| receipts: whites | −18.0 | −18.0 | −18.1 | −18.1 |
| spending: G3+ members | 41.4 | 41.5 | 37.1 | 38.5 |
| spending: whites | 19.5 | 20.1 | 17.9 | 18.5 |
| capital return: G3+ members | 1.7 | 3.0 | 1.7 | 3.0 |
| capital return: whites | 1.0 | 1.7 | 1.0 | 1.7 |
| production gain: G3+ members | −0.3 | −0.2 | −0.3 | −0.2 |
| **total** | **18.9** | **26.4** | **12.7** | **21.6** |

[CALCULATION: `derived/lineage_lines_printed.csv`]

- **Rounding.** One decimal with controlled rounding.
- **Rows not shown.** The union's spending and capital response moves print 0.0. Their actual values are $0.04 / 0.03bn and $0.01 / 0.00bn.

The largest lines on the set:

| Side | Line | Low end ($bn) | High end ($bn) |
|---|---|---|---|
| Spending | education services | +15.8 | +18.4 |
| Spending | Social Security | +9.6 | — |
| Spending | Medicaid and CHIP | +8.3 | — |
| Spending | Medicare | +5.7 | — |
| Spending | public order and safety | +4.7 | — |
| Receipt | federal income tax | −14.5 | −12.3 |
| Receipt | general sales tax | −5.0 | — |
| Receipt | employer and employee OASDI | −4.8 and −4.8 | — |
| Receipt | state and local income tax | −3.3 | — |

[DATA: `derived/lineage_lines.csv`, every arm, set and end]

## 5. Sensitivities (arm b)

| Variant | Set ($bn) | Change | Cash ($bn) | Change |
|---|---|---|---|---|
| central (C3 0.5567, monthly CPS pooled) | 390.29 / 461.24 | +18.88 / +26.40 | 307.38 / 383.41 | +12.68 / +21.59 |
| C3 0.907 (pooled with CPS 2022-26, sensitivity) | 386.02 / 455.62 | +14.61 / +20.78 | 303.58 / 377.77 | +8.88 / +15.95 |
| C3 0: every added person an identified member | 397.08 / 470.19 | +25.67 / +35.35 | 313.41 / 392.37 | +18.71 / +30.55 |
| C3 1: G3-rate attriters cost what whites cost | 384.89 / 454.12 | +13.48 / +19.28 | 302.57 / 376.27 | +7.87 / +14.45 |
| attriters keep the whole production term | 390.15 / 461.15 | +18.74 / +26.31 | 307.23 / 383.31 | +12.53 / +21.49 |
| whites at their own ages | 388.48 / 459.49 | +17.07 / +24.65 | 309.29 / 385.38 | +14.59 / +23.56 |
| [FRAMING-SENSITIVE] replacement, r = 1 | 383.38 / 450.69 | +11.97 / +15.85 | 305.30 / 377.70 | +10.60 / +15.88 |
| [FRAMING-SENSITIVE] replacement, r = 0.5 | 386.84 / 455.97 | +15.43 / +21.13 | 306.34 / 380.55 | +11.64 / +18.73 |
| [FRAMING-SENSITIVE] fractional, attriters only (0.4075 each) | 378.93 / 445.41 | +7.52 / +10.57 | 299.69 / 370.43 | +4.99 / +8.61 |

[CALCULATION: `derived/v5_bands.csv`]

- **Ends.** Every variant keeps 48 / 11 (gate; computed over all 64 specifications for the replacement rows).
- **Changes.** They are differences of the printed bands.

C3 does not move s, so the band is linear in C3 at arm b's responses:

| Set | Low end ($bn) | High end ($bn) |
|---|---|---|
| set | 397.08 − 12.19 × C3 | 470.19 − 16.06 × C3 |
| cash | 313.41 − 10.83 × C3 | 392.37 − 16.09 × C3 |

At C3 ± 1 SE (0.3110 and 0.8024):

| Set | C3 − 1 SE (0.3110) | C3 + 1 SE (0.8024) |
|---|---|---|
| set | $393.29–465.19bn | $387.30–457.30bn |
| cash | $310.04–387.36bn | $304.71–379.46bn |

## 6. [FRAMING-SENSITIVE] Replacement

Without the immigration, a native parent of a mixed descendant would likely have had a child anyway, with another native.

- **The deduction.** The lineage line is reported net of that child: r × W × added people, for r = 1 (full replacement) and r = 0.5.
- **W.** W is the C3 blend's W: a third-plus non-Hispanic white at the identified G3+'s ages, under v4's rules, at each arm's responses.
- **Band and ends.** The band is the minimum and maximum over the 64 specifications. The ends stay at 48 / 11.

| Set | Arm | W per person | Whole person ($bn) | r = 1 ($bn) | Lineage line, r = 1 | r = 0.5 ($bn) | Lineage line, r = 0.5 |
|---|---|---|---|---|---|---|---|
| set | a | $2,279 / 3,477 | 380.37 / 447.55 | 376.26 / 441.27 | +4.85 / +6.43 | 378.32 / 444.41 | +6.91 / +9.57 |
| set | **b** | $2,274 / 3,472 | 390.29 / 461.24 | 383.38 / 450.69 | +11.97 / +15.85 | 386.84 / 455.97 | +15.43 / +21.13 |
| set | c | $2,270 / 3,467 | 400.21 / 474.93 | 390.51 / 460.11 | +19.10 / +25.27 | 395.36 / 467.52 | +23.95 / +32.68 |
| cash | a | $686 / 1,884 | 300.22 / 371.66 | 298.98 / 368.26 | +4.28 / +6.44 | 299.60 / 369.96 | +4.90 / +8.14 |
| cash | **b** | $682 / 1,880 | 307.38 / 383.41 | 305.30 / 377.70 | +10.60 / +15.88 | 306.34 / 380.55 | +11.64 / +18.73 |
| cash | c | $677 / 1,875 | 314.52 / 395.15 | 311.63 / 387.14 | +16.93 / +25.32 | 313.07 / 391.14 | +18.37 / +29.32 |

[CALCULATION: `derived/v5_summary.json` replacement.rows; `derived/v5_bands.csv` replacement_r1, replacement_r0.5]

- **How the lineage lines are computed.** The lineage-line columns are differences of the printed bands from v4's 371.41 / 434.84 and 294.70 / 361.82. The unrounded values are `lineage_line_net_bn`.
- **What replacement removes.** Whites at G3+ ages are net costs at both ends ($2,274 / 3,472 on the set), so replacement removes $6.9 / 10.6bn on arm b. The lineage line stays positive at r = 1 in every arm.

## 7. [FRAMING-SENSITIVE] Fractional count of the whole lineage

This is the people-conserving lineage bookkeeping: `lineage_cost_2026_09_19`'s `per_capita` rule, TFR/2, where each child is shared between two parents. It is the only attribution that counts every person once across all lineages. It is an alternative to the central, not the central.

Each person counts by their share of Mexican-immigrant ancestry:

- A Mexico-born person counts 1.
- A US-born person counts half of each parent's share: ½ per Mexico-born parent, ¼ per Mexico-born grandparent.
- A parent born abroad outside Mexico, or a US-born parent not of Mexican origin, adds nothing [ASSUMPTION].
- The added people take their measured mix, 0.4075. Attrition is 2.1% with four Mexico-born grandparents and 22.0% with one, so the hidden carry less Mexican ancestry than the identified (0.6156).

`fractional.py` measures the shares on the account's own CPS frame.

| Generation | Persons | Measured | Share: low / central / high |
|---|---|---|---|
| G1 (Mexico-born) | 11.04M | birthplace | 1 / 1 / 1 |
| G2 | 14.33M | both parents' birthplaces for all; the other parent's origin when they live with the person | 0.8678 / **0.9248** / 0.9548 |
| G3+ | 14.34M | grandparents only through parents at home | 0.1270 / **0.6156** / 0.9096 |
| added (arm b) | 3.04M | the hidden third generation's grandparent cells | 0.4075 |

[CALCULATION: `derived/fractional_shares.json`, `derived/fractional_classes.csv`]

The linkage reproduces the population lane's grandparent cells and its identified mix (0.615585) on this frame (gate, 0.04 persons).

**G2.**

| G2 class | Share of G2 | Ancestry share |
|---|---|---|
| Two Mexico-born parents | 64.3% | 1 |
| Other parent born abroad outside Mexico | 5.3% | ½ |
| US-born other parent at home, of Mexican origin | 11.2% | 0.89–1.00 |
| US-born other parent at home, not of Mexican origin | 4.2% | 0.555; some of these parents have a Mexico-born parent |
| US-born other parent not at home | 15.0% | ½–1 |

The central gives the last class 0.839, from the co-resident US-born other parents' mean share of 0.679 [ASSUMPTION: adults' parents resemble children's parents].

**G3+.** The CPS shows grandparents only through parents living with the person.

- **Who is seen.** Only 30.4% of members have both biological parents at home; 23.2% have one and 46.4% have none.
- **Most seen members are fourth-plus.** Among the seen, 51.9% have no Mexico-born grandparent.
- **Seen bounds.** For the seen, the strict quarter rule gives 0.3046. Giving every US-born grandparent of a Mexican-origin parent full immigrant ancestry gives 0.7610.
- **Central.** The central is the population lane's convention: the identified third-generation children's mix, 0.6156, applied to every member. Because so many seen members are fourth-plus, the convention probably overstates the third-plus share and so the fractional cost [INFERENCE].

| Set | Arm | Counted people (M) | Fractional ($bn) | Ends | Per counted person | Whole person ($bn) |
|---|---|---|---|---|---|---|
| set | v4 | 33.12 | 312.88 / 356.67 | 48 / 43 | $9,447 / 10,769 | 371.41 / 434.84 |
| set | a | 33.86 | 316.45 / 361.72 | 48 / 11 | $9,347 / 10,684 | 380.37 / 447.55 |
| set | **b** | 34.36 | 320.44 / 367.25 | 48 / 11 | $9,326 / 10,688 | 390.29 / 461.24 |
| set | c | 34.86 | 324.43 / 372.77 | 48 / 11 | $9,306 / 10,693 | 400.21 / 474.93 |
| cash | v4 | 33.12 | 251.30 / 295.13 | 16 / 43 | $7,587 / 8,911 | 294.70 / 361.82 |
| cash | a | 33.86 | 253.51 / 298.94 | 48 / 11 | $7,488 / 8,829 | 300.22 / 371.66 |
| cash | **b** | 34.36 | 256.37 / 303.67 | 48 / 11 | $7,461 / 8,838 | 307.38 / 383.41 |
| cash | c | 34.86 | 259.23 / 308.40 | 48 / 11 | $7,436 / 8,846 | 314.52 / 395.15 |

[CALCULATION: `derived/fractional_lineage.csv`, scenario central]

- **How a generation's share is priced.** Each generation's share is priced at that generation's cost at the arm's responses. The corrected generation models (convention a) are evaluated at all 64 specifications.
  - They add to the union at every specification (gate, 1e-9) and give `generation_results_sept29*.csv`'s costs.
  - With every share at 1 the count gives the whole-person band (gate).
  - Under fractional weights the band's high end can move off specification 11 (v4: 43).

| Scenario (arm b) | G2 share | G3+ share | Counted (M) | Set ($bn) | Cash ($bn) |
|---|---|---|---|---|---|
| central | 0.9248 | 0.6156 | 34.36 | 320.44 / 367.25 | 256.37 / 303.67 |
| G2's unknown ancestors at nothing | 0.8678 | 0.6156 | 33.54 | 311.82 / 357.04 | 249.67 / 295.51 |
| G2's unknown ancestors in full | 0.9548 | 0.6156 | 34.79 | 325.00 / 372.64 | 259.91 / 307.98 |
| G3+ at the seen strict mix | 0.9248 | 0.3046 | 29.90 | 275.39 / 322.13 | 218.85 / 268.27 |
| G3+ at the seen high bound | 0.9248 | 0.7610 | 36.45 | 338.26 / 391.72 | 269.41 / 324.85 |
| every unknown ancestor at nothing | 0.8678 | 0.1270 | 26.54 | 239.62 / 287.57 | 189.15 / 241.47 |
| every unknown ancestor in full | 0.9548 | 0.9096 | 39.01 | 361.02 / 422.11 | 286.27 / 350.80 |

**What is missing for a measured count of the union.** Three things are missing, and the existing files hold none of them:

1. **The other parent's origin, for 15.0% of G2.** When the other parent is US-born and not in the household, the CPS asks only birthplaces, not origin.
2. **Grandparents' birthplaces, for 69.6% of G3+.** These are the members not living with both biological parents. No ancestor beyond grandparents is shown for anyone.
3. **Costs by ancestry share within a generation.** `generation_account_2026_09_24` splits keys, corrections and production by generation only. This count therefore prices each generation's share at its average cost.
   - The class indicators do not settle the direction of that approximation.
   - Two-Mexican-parent G2 hold 23% BA+ among adults 25+, against 28% in the unknown-parent class. Classes with a parent at home are 65–82% minors.

The bound for the union is the last two rows of the scenario table above.

## 8. Payload

`derived/lineage_payload.json` (set) and `derived/lineage_payload_cash.json` (cash) carry arm b, whole persons. Each has 336 edits:

- every engine cell of every line, carrying m_G members' and m_W whites' amounts;
- one lane-constants edit for row 8.

Each payload also carries the production grid. Its meta follows v4's `corrections.json` meta:

- source and status;
- `builds_on`;
- `apply` and `case`;
- `lineage`, with C3, m_G, m_W, s and the metro factor;
- `responses`, with the group-size entries at the new s;
- `capital_return`, with long-run subfunction responses at the new s.

To use the payload:

1. Apply `Engine.applyCorrections(Engine.applyCorrections(MODEL, builds_on payload), this payload)`.
2. Evaluate with this meta's responses and capital return.

A gate applies each payload from its meta alone and reproduces the band (1e-9).

## 9. Gates and reproduction

175 gates pass: population 12, white 26, fractional 8 and engine 129 (`derived/gates.json`).

- **Zero added people.** The case reproduces v4 exactly at all 64 specifications: $371.4146 / 434.8410bn on the set and $294.7011 / 361.8175bn in cash.
- **G3+ member.** $8,548.89 / 11,739.52 reproduce.
- **Whites.** The white lane's A1 and A3 reproduce through its library.
- **Generation models.** The three models add to the union at v4's and every arm's responses.
- **Responses.** They reproduce at v4's s.
- **Parts and lines.** Parts add at every specification, per line and in print.
- **Fractional controls.**
  - With every share at 1 the count gives the whole-person cost.
  - The attriter-only count reproduces its row.
  - The linkage reproduces the population lane's grandparent cells.
- **Payload.** Applied alone, it reproduces the band.

Reproduce from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/population.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/white_lines.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/fractional.py
node infra/immigration-fiscal/main_case_lineage_2026_10_05/lineage_case.cjs
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_lineage_2026_10_05 \
  "uv run --no-project python3 {lane}/population.py" "uv run --no-project python3 {lane}/white_lines.py" \
  "uv run --no-project python3 {lane}/fractional.py" "node {lane}/lineage_case.cjs"
```

The rerun ended `IDENTICAL: 21/21 files unchanged`, exit 0, at 17:03:08 JST. That run was against the C3 chain as committed in 2b0aab3f and 8011c29c.

- **C3 is read at run time.** `population.py` imports C3 from `summarize.py`. When SPLIT_C3 changes, rerun the four steps.
- **Unset entries stop the run.** An entry without a (C3, SE) pair stops the run with `[BLOCKED]`.
- **Test override.** `--c3-override C3,SE` stands in for the central in test runs. Every output is then marked "TEST RUN".

## 10. Limits

- **The count is the largest uncertainty for the central.** Arms a and c differ by $19.8–27.4bn on the set. For the fractional count, the third-plus share is the largest uncertainty.
- **Whites are a rough re-key, not an engine run.** Their amounts are the same at both ends. On the case's component rules their capital return is $926 / 1,520 per person, against $919 / 1,510 on the white lane's own keys.
- **Linear in members.** Only the group-size responses see the larger group.
- **C3 is measured on BA+, not dollars.** At 1 SE the set band moves by about $3–4bn.
- **Sampling error is not propagated.**
- **C3 is now committed.** C3 0.5567 is `summarize.py`'s central as committed in 2b0aab3f ("Propagate C3 0.557 through the attrition chain"). The 17:03 rerun against that commit is IDENTICAL.

## 11. Departures from the brief

1. **The split.**
   - The central follows `population_arms.csv`: 1.94M at the G3 rate and 1.09M later on arm b.
   - The team lead confirmed the rule. The brief's 0.80M reading is not priced.
2. **The frame factor.** It is 0.997189, not the union ratio 0.9694.
3. **The white end.**
   - W is third-plus non-Hispanic whites at the identified G3+'s ages, because C3 is age-matched.
   - Ladder 263's own-age comparison is the `white_own_ages` row.
4. **The G3+ value at the larger group's responses.**
   - At the larger group's responses the member costs $8,541 / 11,731.
   - The brief's $8,548.89 / 11,739.52 reproduce at v4's responses (gate).

## Log (append-only; times from `date`)

- 2026-10-05 15:18 JST: stub written; brief read (worker model claude-opus-5-5). New files only, in this directory;
  nothing is committed.
- 2026-10-05 15:31 JST: inputs read. Findings so far:
  - The engine is linear in cell amounts at given responses; the only group-size terms are the finite-removal
    responses (general government, row 8, the long-run road and park subfunctions and the lines and capital parts
    that follow them) and the long-run owner and tenant property responses (metro price fall). All are recomputed
    at the augmented group's share.
  - The split of added persons in `population_arms.csv` (the canonical rule of
    `bounds_coverage_fiscal.py` arm 5: 1 − p3 of the corrected third-plus is lost at the G3 rate at every
    generation) puts 1.81 / 1.95 / 2.09M at the G3 rate on arms a / b / c, not the brief's ~0.80M (the floor row,
    third generation only). Central follows the files; the brief's reading is priced beside.
  - Row 4 reweights only Mexico-born outside CA and TX; the third-plus keeps its CPS weights. The frame factor for
    added third-plus persons is the account's civilian G3+ over the population lane's self-ID third-plus
    (14,342,575 / 14,383,006.5), not the union ratio 39.71 / 40.97.
  - The v4 white comparator exists: `white_replacement_2026_09_28` sept29 run (rough re-key, A1 third-plus NH
    whites, per line through `rekey_sept29.run29`). It is not an engine run.
- 2026-10-05 15:48 JST: all gates passed at the old central C3 (0.7758, "pooled with CPS 2022-25 (central)"); the
  rerun check then stopped at `population.py`: `summarize.py`'s new central "pooled with CPS monthly 1994-2026
  (central)" held `ba_plus = None`, pending its measurement.
- 2026-10-05 15:52 JST: `load_c3()` now stops with `[BLOCKED]` on any SPLIT_C3 entry without a (C3, SE) pair (no
  fallback). Told team-lead, with the C3 line.
- 2026-10-05 15:55 JST (run log time): the fallback route's price and its gap to the engine route added to
  `v5_summary.json`.
- 2026-10-05 16:13–16:23 JST: polls for the constant read import errors, not the file: a scratch helper of mine named
  `numbers.py` shadowed the standard library in the shared scratch folder. Moved my scratch files to a subfolder and
  re-ran the poll's positive control (it reads HEAD's `summarize.py` as set and the live one as set at 16:25).
- 2026-10-05 16:25 JST: `summarize.py` sets the central to (0.5567, 0.2457). Re-ran the three steps: 153 gates pass.
  Arm b: set $390.29 / 461.24bn, cash $307.38 / 383.41bn.
- 2026-10-05 16:26 JST: `rerun_lane.py` IDENTICAL 16/16, exit 0.
- 2026-10-05 16:29 JST: RESULT written; C3 re-read as 0.5567 just before.
- 2026-10-05 16:32 JST: reported to team-lead. Team-lead's queued messages then read: the split rule is confirmed and
  the brief's 0.80M row is dropped; add a `--c3-override` for test runs; add the replacement (r 1, 0.5) and the
  fractional whole-lineage count as [FRAMING-SENSITIVE] sensitivities; final numbers wait on the C3 chain's GO.
- 2026-10-05 16:49 JST: `fractional.py` added (its linkage reproduces the population lane's grandparent cells);
  replacement, fractional count, generation evaluations and `--c3-override` added; `brief_split` removed. 175 gates
  pass; `rerun_lane.py` with four steps IDENTICAL 21/21, exit 0. C3 still 0.5567 at 16:50; the chain is still
  rerunning upstream lanes.
- 2026-10-05 17:03 JST: the C3 chain is committed (2b0aab3f, 8011c29c; `summarize.py` central 0.5567, SE 0.2457).
  No upstream input this lane reads changed between 16:52 and 17:02 (one hash over all of them). `rerun_lane.py`
  against the committed chain: IDENTICAL 21/21, exit 0. The numbers above are final for that C3.
