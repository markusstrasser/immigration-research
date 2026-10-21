**Verdict:** The pairing leaves out harm that members of the 44.90M Mexican-immigrant lineage do to other members. At the v9 case's two ends that harm is about **$94–96bn a year, or $2,080–2,140 per member** (2024 $, whole-population frame). It sits **beside** the "cost to other residents" pairing and is never added to it. Two pieces make up most of it:
- **$63.9 / $66.5bn** is the in-group side of pairing rows that have a defined in-group share. Crime victims are $28.9 / $32.2bn: about 1,370–1,530 killings and 219,000–244,000 non-fatal victimisations of members aged 12 and over. PM2.5 is $11.6bn, road crashes $9.3 / $9.4bn, congestion $7.0 / $5.5bn, fear $5.1 / $5.8bn, private security $1.3bn and property crime $0.6 / $0.7bn.
- **$29.7bn** is harm to victims under 12, whom the NCVS cannot see. Child maltreatment, priced at Peterson et al. 2018's lifetime cost per victim, is $27.9bn. Maltreatment deaths that death records do not code as assault are $1.3bn, and police-recorded non-family violence against under-12s is $0.4–0.5bn.

The victim row has one large alternative. On police records (NIBRS), Hispanic offenders' victims are far more often Hispanic than NCVS victims report. Taking the in-group-to-outside ratio from police records raises the victim row to **$41.7 / $46.4bn** and leaves the pairing's outside count unchanged. The child-maltreatment row rests on one quality-of-life estimate and runs from $2.6bn (health care only) to $45bn (Peterson's own VSL). On a CPS-investigated base instead of the substantiated one it would be $137bn, an arm kept beside.

For members' families in Mexico no defensible central exists. Left-behind schooling runs from −$1.6bn to +$2.4bn a year, because the studies disagree on the sign. Child health improves (sign only), and left-behind mothers' depression comes to $0–0.4bn. In a world frame, A's homicides need a counterfactual first. The Mexico-born members alone avoid about **2,360 homicide deaths a year** by living in the US (Mexico 24.9 against 5.5 per 100,000). That is **−$32bn at the DOT VSL**, more than A's whole homicide part ($18.8–20.9bn). [CALCULATION: `within_group_harm.py` → `derived/rows.csv`, `arms.csv`, `summary.json`; 119 gates in `derived/gates.csv`] [FRAMING-SENSITIVE: whole-population and world frames; VSL/QALY valuations are willingness-to-pay conventions, not expenditures]

Model: claude-opus-5-5. Lane `infra/immigration-fiscal/within_group_harm_2026_10_21/`, opened 2026-10-21 01:16 JST (`date`). Nothing committed.

## Frame and status

The adopted pairing asks what the lineage costs residents outside it. Each social row removes U→U, U→D and D→D harm: the lineage boundary and the P7 recipient rule in `sept24_propagation_2026_09_24` (`lineage_social_rows`, `p7_crime`). This lane prices the removed part and two things that frame never sees:
- **A and B: whole US population, members included.** These rows are harm that members' conduct imposes on other members. Self-harm is excluded, such as a driver's own crash injury or a smoker's own exposure.
- **C: world frame.** These rows are effects of members' US presence on their relatives in Mexico. C0 is the counterfactual a world frame needs before A's victims can enter it.

**These rows sit beside the pairing.** Adding A or B to the pairing would mix the cost to others with the group's own losses. The world ledger already carries one of them: `ingroup_victims_G1/G2/G3+`, which sums to $20.11bn on the Miller murder price and the 40.9M frame. A's victim row **replaces that row** in a world frame and is never added to it. The world ledger also carries remittances ($62.8bn, measured) as a transfer, so C does not count them again.

## Headline

| Block | Row | Low end | High end | Arm range | Per member (low / high) |
|---|---|---:|---:|---:|---:|
| A | Crime victims, homicide + non-fatal 12+ | 28.91 | 32.20 | 4.39–46.44 | $644 / $717 |
| A | Property crime | 0.64 | 0.69 | | $14 / $15 |
| A | Fear and avoidance | 5.11 | 5.75 | 2.56–11.50 | $114 / $128 |
| A | Private security | 1.29 | 1.32 | 0.66–1.32 | $29 / $29 |
| A | PM2.5 from consumption | 11.64 | 11.64 | 4.51–20.42 | $259 |
| A | Road crashes | 9.30 | 9.40 | 2.57–11.23 | $207 / $209 |
| A | Congestion | 6.98 | 5.51 | 5.12–6.98 | $155 / $123 |
| **A** | **Total** | **63.87** | **66.52** | | **$1,422 / $1,481** |
| beside | School disruption (outside A's total) | −1.57 | −1.57 | | −$35 |
| B | Child maltreatment, ages 0–11, non-fatal | 27.94 | 27.94 | 2.60–45.02 (137.28 beside) | $622 |
| B | Child maltreatment deaths, ages 0–11, not coded as assault | 1.33 | 1.33 | 1.14–2.50 | $30 |
| B | Police-recorded non-family violence against under-12s | 0.42 | 0.47 | 0.42–1.06 | $9 / $10 |
| **B** | **Total** | **29.69** | **29.74** | | **$661 / $662** |
| **A+B** | | **93.56** | **96.26** | | **$2,084 / $2,144** |
| C1 | Left-behind schooling | 0 | 0 | −1.59 to +2.45 | interval only |
| C2 | Left-behind child health | benefit, unpriced | | | |
| C3 | Left-behind mothers' depression | 0 | 0 | 0–0.37 | interval only |
| C0 | Homicide risk G1 avoids by US residence (world frame) | −32.34 | −32.34 | −70.27 to −9.69 | −$720 |

All values are $bn a year in 2024 dollars. Per-member figures divide by 44,903,074. The "low" and "high" ends are the case's specifications 16 and 11, on the pairing's own crime footings (mixed and custody). The arm range is the minimum and maximum over the named one-at-a-time arms in `derived/arms.csv`; it is not a confidence interval. [CALCULATION: `derived/rows.csv`]

## Method

One rule covers every A row except victims. Take a row whose current v9 outside level is *L*, whose P7 recipient share is *r* (the lineage boundary, 0.0103; 0.0217 for pupils) and whose completion-receiver share is *c* (0.00067 for all ages). Let ρ be the union-frame ratio of in-group harm to outside harm. Then:

- *O* = *L* / ((1 − *r*)(1 − *c*)) is the lineage senders' harm to people outside the union;
- in-group = *O*(1 + ρ) − *L*. This counts U→U and D→U at ρ, and U→D and D→D through the boundary.

[ASSUMPTION] The lineage's senders share the union's in/out mix. This is the pairing's own exchangeable-recipient assumption. For each row, *L* is the members' own-conduct level from the v9 parts: the P7 or union level, plus the added people, item 11's consumption shift and the completion receivers. A gate checks that these parts reproduce the current v9 row to 1e-9. PM2.5's current row also nets the PM from re-spending the budget saving (−$12.4bn). That PM occurs only in the world without the lineage, so it has no in-group counterpart and is left out.

### A. Crime victims

The row is rebuilt from the victim lane's cells (`crime_victim_cost_2026_09_23/derived/mortality_detail.csv`) on the pairing's own arm: DOT uniform $13.7M, mixed footing at the low end and custody at the high end. The in-group victims are the group's victimisations minus its outside victims. That is the non-fatal and homicide victims of Hispanic origin times the in-group share *m* = 0.786, the tract-level Mexican share of Hispanic neighbours. Each count is scaled by the P7 population factor (0.98563) and by 1 + the sender key (0.0703 at the low end, 0.0661 at the high). The boundary part is added on top.

The lane is gated against the P7 payload and the v9 row:
- union outside: $35.2510 / $39.4135bn;
- lineage senders before the boundary, P7's own: $37.7295 / $42.0172bn;
- the same with v9's completion and item 16 senders (δ = 0.006973, the pairing's `crime_senders`): $37.9753 / $42.2920bn;
- v9 row: $37.5598 / $41.8293bn.

All four reproduce to 1e-9, and the in-group total equals the all-victim harm minus the outside row. [DATA: crime lane cells; CALCULATION]

| End | In-group homicide deaths | $bn | In-group non-fatal victimisations, 12+ | $bn | Tangible only, $bn |
|---|---:|---:|---:|---:|---:|
| low | 1,371 | 18.79 | 218,976 | 10.13 | 4.39 |
| high | 1,527 | 20.92 | 243,867 | 11.28 | 4.89 |

Arms at the low and high ends ($bn):
- NIBRS police-recorded victim mix: **41.70 / 46.44**;
- every Hispanic victim in-group (*m* = 1): 36.66 / 40.83;
- *m* at county exposure 0.744: 27.39 / 30.50;
- *m* at the national share 0.586: 21.66 / 24.12;
- life-years at 0% real, beside: 32.48 / 36.17; at 3%: 30.10 / 33.52.

The NIBRS arm takes the in-group-to-outside cost ratio for non-fatal violence (**0.980**) from the NIBRS lane's preferred structure, "victim-conditional, SHR-calibrated". That structure applies police-recorded offender-given-victim shares to NCVS victim counts. On the NCVS mix the same ratio is about 0.42. The NIBRS lane found that the two corrections nearly cancel for outside victims ($28.6bn against $28.9bn), so this arm moves only the in-group side. [DATA: `offender_ethnicity_nibrs_2026_09_23/derived/cost_by_offence_nibrs_central.csv`]

**Domestic violence is already inside this row.** On TX+AZ police records, family and intimate partners account for 52% of Hispanic-on-Hispanic rape and sexual assault victims aged 12+, 48% of aggravated assault, 69% of simple assault and 8% of robbery. Weighted by the row's cost, that is **$5.3 / $5.9bn of the $10.1 / $11.3bn non-fatal part**, or $6.0 / $6.6bn when the relationship is known. The NCVS undercounts domestic violence against other surveys; that gap is **not priced** [GAP]. [CALCULATION: `derived/nibrs_child_ratios.csv`, `summary.json` `domestic_violence_inside_A`]

### A. Fear, security and property

- **Fear and avoidance.** P7's rule is applied with members as the victims. The willingness-to-pay residual is Cohen 2004's WTP minus the victim price, at the central arm, on in-group victims (≈$11.4 / $12.7bn). Members' own forward security spending is removed from it, and the result is multiplied by φ = 0.5 (0.25–1.0 as arms). As gates, the same code reproduces P7's lineage fear ($6.6105 / $7.5918bn) and security ($0.4585 / $0.5676bn) to 1e-9. [CALCULATION]
- **Private security.** Members' households guard against in-group offending: residential spending × the offending share (0.122 / 0.124) × the in-group victim share (0.344 / 0.345). Members as purchasers also bear their payment share (0.0995) of commercial security against the lineage's offending. [ASSUMPTION: P7's proportional response]
- **Property crime.** The victim lane's arrest-share proxy gives an in-group-to-outside ratio of 0.465. [DATA: `property_proxy.csv`]

### A. PM2.5, crashes and congestion

- **PM2.5.** The ratio is σ/(1 − σ), with σ = **0.11629**, the air-pollution lane's mortality-weighted self-share on row 4 at DOT uniform. A gate checks that the v9 PM union part equals that lane's row-4 central times (1 − *r*). The arms are that lane's CRF grid (5.43–20.33) and the pre-correction exposure self-share of 0.193 (20.42). In the life-year arms (4.51 at 0%, 5.53 at 3%), the ratio of outsiders' life-years to their deaths is carried over to members [ASSUMPTION].
- **Road crashes.** The capacity-arm components (`capacity_components_oct15.csv`, multi-vehicle only, DOT uniform) add to the union central (gated). Each takes its own in-group ratio:
  - multi-vehicle crashes: *q*/(1 − *q*), with *q* = 0.2988, the crash lane's self-exposure, reproduced here;
  - non-motorists: *h*/(1 − *h*), with *h* = 0.158;
  - single-vehicle crashes: members riding with members' drivers, 0.188 (passenger share of occupant deaths) × 0.838 (Hispanic passengers with a Hispanic driver, FARS) × *m* 0.786, over the lane's external share of 0.04. That gives **3.09 in-group per dollar of outside harm**.

  Passengers in single-vehicle crashes are **74%** of the in-group crash cost ($5.9bn of $8.0bn on the union frame). Excluding them as household-internal leaves $2.6 / $2.7bn. The arms are *q* × 1.3 (9.72 / 9.87), uniform mixing (8.69 / 8.73), and every Hispanic passenger in-group (11.13 / 11.23). Own-vehicle passengers in multi-vehicle crashes their own driver causes are not counted, so the row leans low [GAP].
- **Congestion.** In each urban area, members' delay from members' traffic is the outsiders' B1 cost times members' over others' vehicle-minutes (ACS), weighted by B1. That gives ρ = **0.492**, or 0.456 on peak minutes. The rule is the same slowdown at the same DOT value of time. [DATA: congestion lane `metro_distribution.csv`, `ua_exposure.csv`]
- **School disruption is kept out of A's total.** On the same rule, the Mexican-origin isolation index P\* (0.406 by tract) gives ρ = iso/(1 − iso) = 0.684 and −$1.57bn. The pairing's row is a peer effect based on the gap in suspension rates. Its in-group mirror has no without-world for the pupils it would describe, so the number is shown only. [FRAMING-SENSITIVE]

Rows without an in-group harm counterpart:
- Housing gain, scale earnings, consumer scale, trade and travel, restaurant variety and volunteering are prices and transfers. Inside the whole population their in-group counterparts net to zero, or they are gains.
- Unreimbursed care is a cost shifted through payers.

### B. Harm the NCVS cannot see

**Child maltreatment, ages 0–11, non-fatal: $27.94bn.** [SOURCE: NCANDS *Child Maltreatment 2024*; Peterson, Florence & Klevens 2018, Table 2] The row is a product of the following inputs:
- 125,306 Hispanic substantiated victims (Table 3–7);
- 73.82% aged 0–11 (Table 3–5, all victims; no Hispanic-by-age table exists);
- 0.5917, the Mexican-origin share of Hispanic children aged 0–11 on row 4 [ASSUMPTION: equal rates];
- 0.95, the share of perpetrators who are lineage members; parents alone are 0.891 [ASSUMPTION];
- 1.1458 for the lineage's children beyond the union, on the pupil keys [ASSUMPTION];
- 70.8% first-time victims, the base Peterson's lifetime price is defined on.

That gives **42,181 incident victims a year**. Each is priced at 1.02 discounted QALYs × DOT VSL per discounted life-year at 3% ($589k), plus Peterson's health care inflated ($61.5k), for **$662,443 per victim**. Peterson's government services ($32.3k inflated: child welfare, criminal justice, special education) are excluded because the fiscal account carries them.

The arms are:
- Peterson's native Corso VSL: $45.0bn;
- the HHS-guidance QALY: $30.5bn;
- health care only: $2.6bn;
- parents-only perpetrators: $26.2bn;
- the CPS-investigated base, Peterson's alternative incidence (×4.91): $137.3bn, beside and not recommended.

Caveats:
- The QALY decrement rests on one adult ACE sample (0.028 a year; Peterson's Table 1 prints 0.28, a typo).
- Substantiation rules vary by state.
- The health care cost is partly Medicaid and so already counted in the fiscal account.

[FRAMING-SENSITIVE; contested]

**Maltreatment deaths, ages 0–11: $1.33bn.** The count starts from the Hispanic fatality rate of 1.39 per 100,000 (Exhibit 4–D, 45 states) × 19.69M Hispanic children (Table C–3). It is then multiplied by:
- 91.4% aged 0–11 (Table 4–2);
- the Mexican share, the in-group perpetrator share and the lineage scale above;
- **60.1% without physical abuse** (Exhibit 4–E).

The last factor removes deaths that WONDER codes as assault, which A's homicides already count. That leaves **97 deaths** at $13.7M. Counting every maltreatment death, which overlaps A, gives $2.21bn. Life-years at the mean age of 2 (beside) give $2.50bn at 0% and $1.73bn at 3%.

**Police-recorded non-family violence against under-12s: $0.42 / $0.46bn.** The NIBRS state files for TX and AZ, 2022–23, give ratios of Hispanic-offender victims of Hispanic origin under 12 to those aged 12 and over. They are read from the NIBRS lane's cache without copying, with agencies that record ethnicity ≥50% and 1/n offender weights. The ratios are:
- rape and sexual assault: 0.375;
- aggravated assault: 0.051;
- simple assault: 0.032;
- robbery: 0.010.

Each ratio is applied to A's in-group victims aged 12 and over and priced at Miller's victim-only unit costs. Only the non-family part is added (25% / 42% / 44% / 98%), because family perpetrators are inside NCANDS. California's ratios and the pooled TX+AZ+CA ratios give $0.43–0.51bn. On the NIBRS victim mix the figure is $0.95 / $1.05bn. All relationships together give $1.49 / $1.66bn, a police-recorded alternative to NCANDS that is never added to it. The approach assumes children's violence reaches the police at adults' rate, so it is a lower bound. [DATA: `derived/nibrs_child_ratios.csv`]

### C. Members' families in Mexico (world frame)

Every estimate below is the **total migration effect**, including remittances. Adding a remittance gain on top would count it twice. [SOURCE: the papers' own estimands, quoted in the literature worker's notes]

- **C1 Schooling: central 0, interval −$1.6bn to +$2.4bn.** The signs conflict. McKenzie & Rapoport (2011, Table 3, 2SLS) find −1.37 / −1.44 years at ages 16–18. Hanson & Woodruff (2003, Table 9) find +0.89 / +0.73 years for girls whose mothers have little schooling. Antman (2012) finds +0.73 years for girls. The endpoints apply each extreme to every child: 1.3M children under 15 with a father in the US (Nobles 2013, about 2009, a lower bound), of whom 86,700 reach each age. Each year of schooling is valued at a 6–10% return on the present value of Mexican earnings, $206.6k. That rests on $11,092 a year per person aged 15+ in G1's Mexico comparator (world ledger, GDP PPP), over ages 18–64 at 3%. [INFERENCE; ASSUMPTION: return and age distribution]
- **C2 Health: a benefit, unpriced.** Birth weight is +335 to +364 g and infant mortality falls; the reported size is ambiguous. Breastfeeding and vaccination are lower. [SOURCE: Hildebrandt & McKenzie 2005] [GAP]
- **C3 Left-behind mothers' depression: no defensible central; $0.07–0.37bn.** With fixed effects, the depressive index rises 0.031 log points, about 0.126 SD (p < 0.10). The count is 0.59M mothers, at an assumed 2.2 children each. The QALY loss per SD is assumed at 0.01–0.05, valued at an income-scaled VSL ($4.1M at elasticity 1, from GDP per head in PPP terms: Mexico 0.300 of the US). [SOURCE: Nobles, Rubalcava & Teruel 2015, Table 2; ASSUMPTION: QALY mapping, mothers per child] Separation's effect on children's mental health has no causal Mexico study. [GAP]
- **C0 is the counterfactual for A's victims, not a cost row.** In 2023 Mexico's homicide rate was 24.86 per 100,000 (WDI). The US rate for Hispanics in 2024 was 5.54 per 100,000 (WONDER over CPS). At those rates the 12.22M Mexico-born members avoid **2,361 deaths a year** in the US: −$32.3bn at DOT, −$9.7bn at the income-scaled VSL. With the second generation, on the world ledger's raised-in-Mexico convention, they avoid 5,129: −$70.3bn and −$21.1bn. In a world frame, A's homicide part ($18.7–20.8bn) therefore turns into a net gain for the members. Both national rates misstate the members' own rates. Migrants are mostly working-age men, who face far higher rates in Mexico. The Mexico-born likely die by homicide less often in the US than US-born Hispanics. Both biases make the offset larger. [DATA: world ledger WDI cache; CALCULATION; INFERENCE]

## Steel-man and disconfirmation

- **Why the pairing leaves this out.** The pairing answers what the lineage costs other residents. Harm members bear, including from each other, is the group's own welfare, and it belongs in a frame that also counts the group's gains. In the world ledger those gains are the place premium and, as C0 shows, much lower homicide risk than in Mexico. Adding A to the pairing would count the group's losses as others' costs. The rows therefore stay beside.
- **The in-group victim share could be lower.** If members sort less with co-ethnics than tracts suggest, *m* falls: at county exposure the row is $27.4bn, at the national share $21.7bn, an implausible bound. The evidence runs the other way, though. Police records in TX and AZ put 70–81% of Hispanic offenders' victims as Hispanic, against about 40% in the NCVS, which raises the row to $41.7bn. Family and intimate violence, which is in-group by construction, is about half of the non-fatal cost.
- **The PM self-share** fell from 19.3% on exposure to 11.6% once weighted by mortality, because members are younger than the people PM kills. The row therefore halves from the exposure reading; the arm shows $20.4bn.
- **The crash row is mostly passengers in members' own cars.** Calling them household-internal is a defensible choice: $2.6bn without them. Shared driving by family members is, however, harm to another member.
- **The child-maltreatment row** is the largest new item, and it rests on the Hispanic rate (6.4 per 1,000, against 6.2 for white children), a population-share step to Mexican origin, and one QALY study. A tangible-only reading is $2.6bn. The investigated-base reading ($137bn) counts unsubstantiated reports and is not recommended.
- **C1's sign is unsettled.** The negative estimate uses a broad treatment (any adult member who has ever been to the US) and comes from 1997. The positive estimates cover girls whose mothers have low schooling, or rest on 136 families. Zero is the honest central.

## For the parent: observations outside this lane

1. **The v8 added 2.15M people carry no crime sender share.** `added_terms()` sets the share to 0 on `CRIME_KEYS`, so the completion and coverage people's offending against outsiders is not priced in the pairing's victim, fear and security rows. At the head-count share of 5.4% that would be about +$2.0bn victims and +$0.36bn fear at each end. This may be deliberate; it is not documented in the row contract. [CALCULATION, rough] [2026-10-21, resolved in the pairing: the coverage people are already inside the national incident counts, but the completion reporters and item 16's minors are CPS Hispanics outside the union mask. Their located change aged 12+ (δ = 0.006973) now sends crime in every crime row: victims +$0.24 / +0.27bn. This lane's victims and fear/security blocks take the same δ.]
2. **The world ledger's `ingroup_victims_*` rows ($20.11bn)** are on the Miller murder price and the 40.9M frame. On the pairing's DOT uniform standard and the v9 lineage they are $28.9 / $32.2bn (this lane). If the world frame should follow the common mortality standard, those rows need repricing. [2026-10-21: the world ledger's live case now takes this lane's row A victims in their place (`world_ledger.py` `INGROUP_VICTIMS`).]
3. **The NIBRS lane's `age_band`** reads the NIBRS unknown-age code `'00'` (age_id 103) as age 0. Unknown-age victims therefore fall into "under 12" and drop out of its 12+ universe. The effect is about 0.2% of Hispanic-on-Hispanic victims, so it is immaterial there. This lane's reader handles the code (`nibrs_children.age_band`).
4. **P7's commercial-security forward term** is charged as offending share × outside-victim share × (1 − payment share). The docstring says outsiders bear their purchase share of group-attributable costs. Read that way, commercial security against offending whose victims are members, paid for by outsiders as purchasers, sits in neither the pairing nor this lane: about 50.7 × 0.121 × 0.34 × 0.90 ≈ $1.9bn. That is below the $5bn bar. It is an ambiguity, not a verified defect. [2026-10-21: verified against P7's own assumption list and the business lane's pass-through rule; the pairing now carries it as the row `commercial_security_member_victims`, $1.90 / 1.96bn.]

## Limits

- Every A row except victims transports a union-frame in/out ratio to the lineage [ASSUMPTION]. The 3.04M non-reporting descendants are likely less co-ethnically concentrated, which would lower ρ for them.
- NCANDS has no Mexican-origin field and no Hispanic-by-age table, and its fatality race split covers 45 states. NIBRS is TX, AZ and CA only.
- C uses father-absence counts from about 2009 (fathers only, partnered mothers). No count ties the left-behind children to members of this lineage specifically.
- This was produced through an LLM (`notes/llm-bias-caveat.md`). The choices that move the totals most are explicit arms: the NIBRS victim mix, the QALY price, the passenger rule and the C0 VSL.

## Sources and pins

Primary bytes copied from the literature worker's fetch into the ignored `_cache/lit/`. Their sha256 values are in `inputs/pins.json` and verified on every run. Every number from them enters through `inputs/transcribed.csv`, whose quote must appear in the pinned text (43 quote gates).
- NCANDS *Child Maltreatment 2024*, acf.gov/sites/default/files/documents/cb/cm2024.pdf (sha256 a43e2325…).
- Peterson, Florence & Klevens (2018), *Child Abuse Negl* 86:178–183, PMC6289633.
- Nobles (2013), *Demography* 50(4), PMC3766732.
- Nobles, Rubalcava & Teruel (2015), *Soc Sci Med* 132:236–244, PMC4562970.
- McKenzie & Rapoport (2011), *J Popul Econ* 24:1331–1358.
- Hanson & Woodruff (2003), UCSD mimeo.
- Antman (2012), *J Popul Econ* 25:1187–1214.
- Hildebrandt & McKenzie (2005), *Economía* 6(1).
- Also read but not used numerically: Antman (2011), Antman (2013, IZA DP 6374).

Repository inputs are read read-only, each recorded with its sha256 in `derived/source_manifest.csv`:
- crime victim, NIBRS, P7/social, propagation oct16, air pollution, crash, congestion and world-ledger derived files;
- the victim lane's ACS B03001 tract cache, the WDI cache and the six NIBRS zips;
- the crime lane's `vsl_standard.py`, imported for the DOT VSL and the NVSS life table.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_harm_2026_10_21/within_group_harm.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/within_group_harm_2026_10_21 \
    "uv run --no-project python3 {lane}/within_group_harm.py"
```

`nibrs_children.py` is imported by the main script. It stages the NIBRS cells to `_cache/nibrs_cells/`, keyed by each zip's sha256 and a stage version: 25 s and 1.8 GB peak RSS when cold, under 2 s when warm. A missing `_cache/lit/` file stops the run with its URL.

## Covered / skipped

**Covered:**
- the brief;
- the crime victim lane's RESULT and cells;
- the P7 payload and code (`p7_crime.py` `crime_responses`, `response`);
- the propagation lane's `real_costs_totals.py` lineage and v9 environment code and oct16 totals;
- the air-pollution, crash and congestion lanes' RESULTs and derived files;
- the social-costs lane's RESULT (fear, security, schools);
- the NIBRS lane's RESULT, derived files and state zips;
- ladder 148;
- the world ledger RESULT (part E, in-group victims, remittances) and its WDI cache;
- NCANDS CM2024, Peterson 2018 and seven left-behind papers, through the worker (full text).

**Skipped:**
- *NISVS-based domestic-violence undercount:* no primary source was read [GAP].
- *ENVIPE nonfatal victimisation in Mexico for C0:* not fetched; C0 is homicide only.
- *Left-behind children's mental health:* no causal Mexico study was found.
- *Hispanic-by-age NCANDS:* needs NDACAN microdata.
- *A re-pricing of the world ledger or any other lane:* outside the brief.

## Log

Times are from `date`, or from file modification times where marked (mtime).
- 01:16:44 JST: brief read, stub written.
- 01:24:38–01:45:19: literature worker, from its own `date` log (Peterson, NCANDS, left-behind papers).
- 01:50:57: NIBRS cells staged.
- 01:59:09: first full run.
- 02:00:51–02:01:06 (mtime): cells re-staged after I fixed my own reading of NIBRS's unknown-age code `'00'` as age 0; the cache version was bumped.
- 02:02:36 (mtime): outputs with the PM row on the own-conduct level, without re-spending. Rerun IDENTICAL 11/11 just after.
- 02:05:09: RESULT written.
- 12:30 JST, 2026-10-21 (`date`): the victim and fear/security blocks take the pairing's v9 crime senders (completion and item 16, δ = 0.006973) and payers (consumption with item 11). A+B moves from $93.32 / 95.99bn to $93.56 / 96.26bn. Rerun IDENTICAL 12/12.
