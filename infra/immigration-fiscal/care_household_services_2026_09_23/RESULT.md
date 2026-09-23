**Verdict:** Three channels in this lane add to the fiscal account, and all three are small.

- **Taxes on native women's extra hours.** Cheaper household services lead native women to work more hours, and those hours pay about **$2.7bn a year** in taxes ($1.8–5.8bn across the estimates of the household-service channel).
- **Net Medicaid effect of the group's home-care workers: $1.5bn.** The range across designs is $1.2–7.6bn, and the 90% interval is −$1.8bn to +$8.3bn.
- **Output gain to other factors from those hours: −$0.03bn,** including its taxes.

Together the three come to **$4.1bn a year ($2.6–13.3bn)**. That is **$101 per group member and $14 per other resident**, or 1.7–2.0% of the main-case net cost of $203.2–249.6bn.

The consumer surplus on cheaper services is $21.8bn gross in the union frame, or $11.9bn after netting native low-skill wage gains. It is the expenditure side of P, so it stays a side view and is not added.

Three earlier readings need correcting:

1. The 2026-09-18 hours tax ($8.7bn) rested on a misread regressor, the wrong table and a non-account tax rate. For the household-service channel at the account's tax rate it is $2.7bn. Contrary to FAQ 4, it does not overlap P and should be added.
2. FAQ 13 says the channel "transfers weakly" to the group. That is wrong for home care once US-born Mexican-origin aides are counted: the group supplies 15.4% of home-care hours against 12.0% of residents.
3. FAQ 13's $2.3–14.6bn gross bound still shrinks to about $1.5bn net, for three reasons:
   - the group's own care needs absorb more than half of its home-care supply;
   - Secure Communities raised nursing-home residents by only 2.7% (the ACS institutionalization measure gives 6.8%, but it is less precise);
   - the same workers staff $1.0–1.3bn of Medicaid home care.

[CALCULATION: `summary.py` → `derived/summary.csv`]

| Channel | Ruling | Central $bn/yr | Range | Per member | Per other resident |
|---|---|---:|---|---:|---:|
| Taxes on native women's extra hours, household-service channel | **adds** (fiscal) | 2.69 | 1.80–5.76 (95% of central 1.52–3.86) | $66 | $9.0 |
| Output gain to other factors from those hours, with its taxes | **adds** (second order) | −0.03 | −0.41 (capital fixed) to −0.03 | −$0.7 | −$0.1 |
| Elder care: Medicaid nursing-facility saving net of Medicaid home care | **adds** (fiscal) | 1.49 | 1.20–7.62 (90% of central −1.82 to 8.34) | $36 | $5.0 |
| **Sum of additive channels** | **adds** | **4.15** | **2.60–13.35** | **$101** | **$13.9** |
| Consumer surplus on services, net of native low-skill wage gain | inside P, side view | 11.94 | 3.94–12.82 (gross 21.84) | — | — |
| Native women's private gain from the extra hours | ≈ 0 (envelope) | 0 | — | — | — |
| Non-service part of the Cortés–Tessada hours effect (its taxes) | not added | 8.92 | — | — | — |

The group is the 40,896,574 Mexican-origin residents counted by the CPS. The other residents number 340,110,988 − 40,896,574 = 299,214,414. All figures are 2024 dollars a year, with the group present compared against the group absent. The ranges are the envelope of each channel's point estimates across legitimate specifications. The model-uncertainty intervals are reported separately.

## Overlap ruling, line by line

1. **Consumer surplus on cheaper services is inside P.** In the account's one-good CES a household service is just output. Its price is the cost of the labour that produces it, so the model shows the price fall as a lower low-skill wage.
   - The consumer's gain is made of two parts. The first is a rectangle transferred from native low-skill workers, whose wage loss the wage-distribution lane prices. The second is the triangle, which is P.
   - At β = 1 the rectangle cancels among other residents. What remains is the immigration surplus seen from the expenditure side.
   - Consistency check: in the union frame the surplus net of native low-skill wage gains is $11.9bn (JPE price arm). That sits inside P's $8.8–13.3bn, even though the two come from different models.
   - FAQ 4 is right not to add it. [INFERENCE; CALCULATION: `derived/partA_side_view_union_frame.csv`]
2. **The private gain from the extra hours is about zero.**
   - At the margin a woman is indifferent between an hour of market work and an hour of home time. Her first-order gain is therefore the lower price of the services she buys, which is already the side view in line 1.
   - Re-optimizing her hours adds only a second-order triangle to that same surplus.
   - Neither paper shows a private gain beyond the price effect. Cortés–Tessada mention career concerns but do not quantify them. [INFERENCE]
3. **Taxes on the extra hours add to the account, in F.**
   - The account's central holds native hours fixed.
   - Its grid arm with elasticity 0.33 lets hours respond only to the worker's own wage (`matched_benefits_2026_09_19/model.py`: `desired = elasticity * log_wage`).
   - A one-good model has no service price, so the cross-price response lies outside every arm. The tax is τ·w·Δh, a first-order fiscal externality that other residents receive.
   - **Only the household-service part adds.** The rest of the Cortés–Tessada effect behaves like a wage or labour-demand response. Top-quartile wages rise 8.7% per unit of ℒ (Table 10 Panel C, 0.087, SE 0.027), and men's weekly hours in the same wage band rise 1.487 per unit of ℒ (Table 10 Panel A, SE 0.616). That part is either the account's 0.33 arm or confounding. Adding it would double count: its taxes are the $8.9bn line marked "not added".
4. **The output gain to others is additive but negligible.**
   - The women are paid their marginal product. In the account's CES (σ = 2, capital adjusting), their extra hours raise other factors' income by $0.0002bn.
   - Taxes on the income shift from high-skill to low-skill workers, who face a lower rate, fall by $0.03bn.
   - With capital fixed (grid arm) the shift toward capital, taxed at 0.246, costs $0.41bn in receipts. [CALCULATION: `derived/ces_output_triangle.csv`, 27 rows]
5. **Elder care adds to the fiscal account.**
   - The account charges the group's own Medicaid use to the group.
   - It does not model other residents' nursing-facility spending, which falls when the group's aides keep people at home.
   - It also does not model Medicaid home care that other residents receive because those aides exist. That is an outlay while the group is present.
6. **Aging in place sits beside the account and is unpriced.** When a private-pay family avoids nursing-home costs, that is the consumer surplus on home care (inside P). The non-market value of staying at home has no willingness-to-pay estimate in these sources, so it is not priced.

**Other lanes.**

- The benefit lanes do not price household services, care or women's hours: `scale_spillovers_2026_09_23`, `construction_housing_supply_2026_09_23` and `labor_mobility_insurance_2026_09_23`. Landscaping and gardening appear only inside the side view in line 1.
- Among the cost lanes, `wage_distribution` holds the native low-skill wage loss that nets the surplus in line 1, so this lane adds nothing there.
- `uncompensated_care` covers hospital and physician care, not nursing facilities or home care.
- `distribution_weights` re-weights transfers.
- Justice, victims, housing transfer and congestion do not touch these channels.

## 1. Taxes on native women's extra hours

**The shock is built metro by metro**, because services are local and both papers identify their effects off variation across metros.

- ACS 2024 PUMS PUMAs are allocated to 424 CBSAs or state non-metro remainders by population share, with the group scaled to the CPS count (×1.0372).
- The group holds 35.8% of the no-diploma labour force aged 16–64 and 50.7% of no-diploma immigrants in the civilian labour force.
- Cortés–Tessada's regressor is ℒ = ln[(no-diploma immigrants + no-diploma natives)/labour force]. It falls by 0.283 when weighted by the women's hours value (0.314 on national totals).
- The Cortés (2008) regressor, ln(no-diploma immigrants/labour force), falls by 0.554 when weighted by mothers' earnings (0.582 nationally).
- Six areas hit the 5% floor on remaining low-skill workers (log-linear models break at zero). They carry 0.14% of the Cortés–Tessada weight. For the Cortés shock it is 44 areas and 1.4% of the weight.

[CALCULATION: `hours_tax.py` → `derived/shock_summary.csv`, `derived/metro_shocks.csv`. DATA: `acs_extract.py` → `derived/acs_*.csv`, where the weighted population is 340,110,990 against 340,110,988 published]

**Central estimate.** The central uses the Cortés–Tessada household-service channel: women's hours relative to men's in the same band of the female wage distribution, 0.479 (SE 0.106).

- That gives 0.136 fewer weekly hours (8 minutes) when the group is removed, for 14.37m native, non-group women in the top quartile of their census division's female wage distribution.
- Earnings fall by $6.31bn, and taxes by **$2.69bn** at the account's τ = 0.426 (95%: $1.52–3.86bn).
- At τ = 0.366, which nets out future Social Security accrual, taxes fall by $2.31bn.
- Cortés–Tessada call 0.479 a lower bound, because men might also respond to service prices. East–Velásquez find that fathers of young children do not respond to Secure Communities (−0.19%, p = 0.53), which suggests the bound is close to the service effect.

**Independent check with East–Velásquez.**

- Removing the group raises household-service prices by 12.5% on the Cortés (2008) published elasticity, or 7.9% on the working paper's.
- US-born college mothers of children under 6 respond with an hours elasticity of −0.23. East–Velásquez attribute 72–90% of their effect to household-service costs.
- This gives **$2.77–3.46bn** of taxes (WP price arm: $1.80–2.25bn) on their $337.6bn of earnings.
- Applied to all 29.7m US-born college women (−0.34%, not significant), it gives $3.73–5.76bn, with a 95% interval that crosses zero.

| Specification (metro-weighted, CPS-scaled union, native non-group women) | Δ hours on removal | Earnings $bn | Taxes $bn at τ .426 (95%) |
|---|---:|---:|---:|
| CT Table 10 ℒ×female, 0.479 (0.106) — **central** | −0.136 h/wk | 6.31 | **2.69** (1.52–3.86) |
| CT Table 10 with city×decade effects, 0.468 (0.105) | −0.133 h/wk | 6.17 | 2.63 (1.47–3.78) |
| same, national shock / labour force held fixed | −0.150 / −0.193 h/wk | 6.99 / 8.99 | 2.98 / 3.83 |
| same, group not scaled to CPS | — | — | 2.52 |
| same, with foreign-born non-group women (population transported) | — | — | 3.31 |
| EV mothers, elasticity −0.23 × 0.90, JPE price / WP price | −2.4% / −1.6% | 8.12 / 5.28 | 3.46 (0.74–6.18) / 2.25 |
| EV mothers, −0.23 × 0.72 / −0.23 × 1.0 (JPE price) | −1.9% / −2.7% | 6.51 / 9.00 | 2.77 / 3.84 |
| EV all college women, −0.34%/6.5% (not significant), JPE / WP | −0.6% / −0.4% | 13.51 / 8.76 | 5.76 (−1.27 to 12.78) / 3.73 |
| *Not in range:* EV mothers with all-female household-service wage (+2.0%, not significant) as the price | −8.2% | 27.76 | 11.83 |
| *Not added:* CT Table 7 all channels, 2.068 (0.754) / 2.375 (0.735) | −0.586 / −0.673 h/wk | 27.25 / 31.30 | 11.61 (3.31–19.90) / 13.33 |
| *Not added:* CT Table 7 × East–Velásquez attribution 0.90 / 0.72 | — | 24.52 / 19.62 | 10.45 / 8.36 |

[CALCULATION: `derived/hours_tax_specs.csv`, 168 rows. The grid covers 4 CT coefficients × attribution × 4 shocks × 2 populations × 2 scalings, plus 5 EV elasticities × 2 shocks × 2 price arms × 2 scalings, each at τ .426 and .366, with 95% bounds]

**Does the evidence reach the group? Yes.**

- 86% of Secure Communities deportations were of Mexican and Central American immigrants, against 70% of the undocumented (East–Velásquez fn. 9).
- US-born college mothers' hours fell 0.41 at the mean Mexican/Central American deportation share and 0.65 at one standard deviation above it (Table 9 Panel C).
- The Cortés–Tessada instrument allocates 1970 Mexican settlement across cities (p.102).

## 2. Elder care: the Medicaid saving, net of Medicaid home care

**Dose.** Removing the group takes away its care workers and also its own care needs.

- The group supplies 15.4% of home-care hours (ACS, CPS-scaled; SE about 0.4pp before scaling). That is home health and personal care aides plus maids working in home health care and private households, the AAF definition: 7.8% from foreign-born members and 7.1% from US-born members.
- It holds 8.9% of household residents with a self-care or independent-living difficulty (6.8% at 65+, 10.7% among Medicaid enrollees).
- Care available per unit of other residents' need therefore falls 7.2% (range 5.3–9.3%; 15.4% with no netting).
- Secure Communities cut the same market's hours by 5.95% (SE 2.81). The Wald scale is 1.21.
- On the Kreider–Werner market (aides only, including individual and family services) the group's share is 13.1%. The net dose is 4.7%, against Kreider–Werner's first stage of 7.49% (SE 2.68), a scale of 0.63.

[CALCULATION: `elder_care.py` → `derived/elder_care_doses.csv`]

**Nursing-facility saving.** Each estimate below is gross, before the home-care offset. Per SC dose (see Sources), AAF find nursing-home residents +2.714% (SE 0.508, LTCFocus) and institutionalized US citizens 65+ +6.81% (SE 2.54, ACS). Medicaid spent $78.9bn on nursing facilities in 2024 (CMS NHE Table 15).

- **LTCFocus measure:** 40,100 fewer residents at **$62,703** each ($78.9bn over 1,258,309 residents per day in the Aug 2026 CMS provider file). That is **$2.52bn** gross. The product equals relative effect × dose × Medicaid spending on others, so the file's vintage does not matter.
- **ACS measure:** 113,600 people (8.3% of 1.375m institutionalized other-resident citizens 65+) at **$45,197** each. The price is the 82.1% of Medicaid spending that goes to residents 65+ (NPALS 2020), spread over 1,433,206 ACS institutional residents 65+. That is $5.14bn gross.
- **Pooled:** weighted by the precision of the two reduced forms, the gross saving is **$2.67bn**. The LTCFocus measure carries 94% of the weight.

**Medicaid home care.** Kreider–Werner find that Secure Communities lowered formal home care among Medicaid elders with care needs by 4.6pp (SE 2.1) from 19.8%. Non-Medicaid elders were unaffected (+0.6pp, SE 1.3); agencies ration the fixed-price Medicaid clients first.

- Scaled to the group's dose: 2.88pp × 2.147m other-resident Medicaid enrollees 65+ with needs = 61,700 recipients.
- At $16,847–21,332 each (KFF FY2020 per-person HCBS, state plan and 1915(c) seniors/physical disability, CPI to 2024), that is **−$1.04 to −$1.32bn**. This is an outlay the group's presence causes.

**Net result: $1.35–1.63bn; central $1.49bn.**

- Draws come from independent normal first stages and reduced forms (200,000 draws, seed 20260923).
- The 90% interval is −$1.82bn to +$8.34bn. The first stage's t of 2.1 gives it a long right tail.
- The net is negative with probability 11–18%.

| Net Medicaid, $bn/yr (all-ages netting) | State-plan price | Waiver price | 90% (state plan) |
|---|---:|---:|---|
| AAF pooled — **central** | 1.63 | 1.35 | −1.03 to 8.34 |
| AAF LTCFocus nursing-home residents | 1.48 | 1.20 | −1.15 to 7.83 |
| AAF ACS, relative effect (6.81% of mean) | 4.09 | 3.82 | −0.42 to 17.79 |
| AAF ACS, absolute effect (0.257pp) | 6.96 | 6.68 | 0.50 to 28.15 |
| BMW, mapped by care hours, home care (0.151) | 7.62 | 7.34 | 4.36 to 10.29 |
| BMW, mapped by care hours, all direct care | 4.56 | 4.28 | 2.05 to 6.41 |

**The same numbers under other nettings and mappings** (`derived/elder_care_net.csv`, 48 rows; `derived/elder_care_specs.csv`, 54 rows):

- The central is $1.52–1.92bn at 65+ netting, $1.20–1.36bn at Medicaid netting, and $2.01–2.79bn with no netting.
- BMW mapped by labour share in the union frame (a 2.84pp change in its treatment share, no need netting by construction) gives $9.81bn gross.
- Without California, BMW mapped by care hours gives $5.16bn gross. With year×state effects (not significant) it gives $3.50bn.

## 3. Child care and household production

The childcare hours channel is already inside section 1.

- East–Velásquez's household services include childcare workers.
- The group supplies 15.7% of childcare-worker hours: 6.2% from foreign-born members and 9.5% from US-born members.
- The mothers-of-young-children estimate is the childcare channel. Adding it separately would double count.

**Fertility is not priced.** Furtado (2016, Demography 53(1):27–53; Census 1980–2000, shift-share IV, US-born college women) finds birth probability rises 0.21pp per percentage point of low-skill immigrant share for women with only a college degree, and 0.46pp for those with a graduate degree.

- The effect is carried by immigrants from "high-childcare" origins in the top quartile of childcare propensity. Low-childcare origins show no significant effect.
- The evidence does not reach the group as an origin. The Mexico-born are not identified as a high-childcare origin, and East–Velásquez find no fertility effect of Secure Communities (their Appendix Table A3).
- Even if it did transfer, extra native births in a stationary annual account are schooling costs this year. The parents' gain is theirs by revealed preference, so this is not a benefit to add.

**Household production is not priced.** Cortés–Tessada find that top-quartile women cut household chores by about 7 minutes a week over 1980–2000 (Table 11: interaction −0.739, SE 0.414). That time reallocation is private, and its value is the side view in line 1. It carries no fiscal item.

## 4. Corrections

**The 2026-09-18 memo and lane (not edited).**

1. *Regressor.* The published article (AEJ Applied 3(3), Tables 7–11 notes; p.104 fn. 21) defines ℒ = ln[(no-diploma immigrants + no-diploma natives)/labour force]. It converts an effect per log point of low-skilled immigrants by multiplying by their share of the low-skill supply (fn. 23).
   - The memo instead used a −0.630 change in the log Mexico-born dropout share.
   - The union-frame change in ℒ is −0.314 nationally and −0.283 metro-weighted.
   - The memo's evidence for its reading was Cortés's 2023 survey sentence ("the same empirical strategy"), and the 0.980 × 0.370 ≈ 20-minute match. That match paired the wrong coefficient with the wrong regressor change.
   - Cortés–Tessada's "close to 20 minutes" is Table 7's 2.07 × a city-average Δℒ of about 0.16. That Δℒ is 0.37 × a low-skill immigrant share of about 0.43, which is the chain rule. [INFERENCE from the article's text]
2. *Table.* The memo's 0.980 (SE 0.497) is Table 8 Panel A: women in occupations with the top quarter of male median wages. The wage-quartile coefficient is Table 7's 2.068 (all channels), and the household-service channel is Table 10's 0.479.
3. *Tax rate.* The memo used a built-up 0.35. The account uses 0.426 (0.366 net of future Social Security accrual).
4. *Net effect.* Errors 1 and 2 almost offset for the all-channel level: 0.617 against 0.649 weekly hours on national totals. So the memo's $24.9bn of earnings is close to the corrected all-channel $26.2bn on its own population by coincidence. Only the service channel adds, and on the memo's population at τ = 0.426 its tax is **$2.6bn, not $8.7bn** (`derived/sept18_partB_correction.csv`).
5. *Private earnings.* The memo's "private earnings $11.5–24.9bn" are not a welfare gain, as its own envelope paragraph says. The "$21.8bn defensible native total" adds a side view (inside P) to a fiscal item, so it is neither additive nor a comparable magnitude.
6. *Part A stands.* The memo's Part A reading of Cortés (2008) is right, and its numbers survive the union frame: $21.8bn gross nationally, $23.4bn weighted by other residents' location, and $11.9–12.8bn net of native low-skill wage gains.

**FAQ entry 4.**

- "Consumer prices … overlap the factor-income gains, so they are not added" is right.
- "… and native women's hours" is wrong. The hours taxes, $2.7bn, add.

**FAQ entry 13.**

1. *"Transfers weakly."* The statistic behind it counts the Mexico-born only (14.5% of foreign-born care workers against 37.7% of the less-educated foreign-born). In the union frame the group supplies 15.4% of home-care hours, 13.1% of aide hours and 11.6% of all direct care, against 12.0% of residents. Secure Communities, which reached mostly Mexican and Central American workers, moved both home-care hours and institutionalization (AAF Table 8: Mexican/Central American hours −17.4%, SE 6.2). The channel does transfer.
2. *Size.* It is small for three reasons:
   - net of the group's own needs, the dose is 7.2%;
   - Secure Communities raised certified nursing-home residents by 2.7%;
   - Medicaid pays for the extra home care.
3. *Price.* The FAQ's price of $55,051 is all-age Medicaid spending over residents 65+. The 65+ share gives $45,197, the correction the memo itself flagged.
4. *Replacement.* The FAQ's "$2.3–14.6bn, $5.6bn preferred" is gross of the home-care outlay. Replace it with **$1.5bn net (design range $1.2–7.6bn)**. Its own labour-share route, redone for the Mexico-born at the corrected price, gives $11.7bn gross (`derived/elder_care_specs.csv`).

## Sources with intervals and populations (rule 1)

| Source | Design and population | Estimates used (SE) | Use |
|---|---|---|---|
| Cortés & Tessada 2011, AEJ Applied 3(3):88–123 (`_cache/ct2011_repl_material.txt`) | Census 1980–2000, 1970-settlement IV across metros; native women 20–64, working, by female-wage quartile within division | T7 top quartile: 2.068 (0.754) additional controls, 2.375 (0.735) basic; T10 A ℒ×female: 0.479 (0.106), 0.468 (0.105) with city×decade FE; T10 C log wage: 0.087 (0.027), ×female −0.009 (0.003); T11 chores ×top quartile −0.739 (0.414) | hours, central |
| East & Velásquez, JHR 59(5) 2024 (author draft) | ACS 2005–2014, Secure Communities rollout DiD; US-born college women 20–63 | mothers of children under 5: −0.421 (0.169) h/wk, −1.46%; all −0.114 (0.071); no kids −0.080 (0.088); household-service wage: low-educated +0.065 (0.027), all +0.020 (0.013); triple differences −0.302 (0.184), −0.379 (0.224); fathers −0.19% (p .53) | hours check; reach |
| Cortés 2008, JPE 116(3); 2006 WP (`_cache/cortes_wp2006.txt`) | CPI micro prices across 25–30 cities, IV | 10% more low-skill immigrant share → immigrant-intensive prices −2% (published), −1.3% (WP); no SE used | EV price; side view |
| Almuhaisen, Amuedo-Dorantes & Furtado, J Health Econ 94 (2024) (IZA DP 16357) | ACS 2006–2012, SC DiD, US citizens 65+ (N 3.31m); LTCFocus counties | institutionalized +0.00257 (0.00096), mean 0.04; nursing-home residents +0.02714 (0.00508); home-care hours −1.297 (0.614) on 21.82; Mexican/Central American hours −0.669 (0.239) on 3.85; Hispanic elderly 0.00072 (0.00220) | elder care, central |
| Kreider & Werner, JMP Jan 2025 | ACS CPUMAs 2005–2014 + HRS, SC DiD; HRS 50+ with care needs | home-care workers −29.7 (10.6) per 100k on 396.8; Medicaid: formal helper −0.046 (0.021) on 0.198; non-Medicaid +0.006 (0.013) | home-care offset |
| Butcher, Moran & Watson, NBER w29520; RIE 30(5) 2022 | Commuting zones, 1980–2000 shift-share; US-born 65+ | −0.151 (0.027), F 28.3; without California −0.090 (F 9.2); year×state −0.061 (0.058) | elder-care cross-check |
| Grabowski, Gruber & McGarry, NBER w34791 | ACS 2000–2019 + Medicare 2008–2019, health-weighted shift-share | non-health-weighted instrument −0.00252 (0.00370) = −3.25 deaths per 1,000 immigrants (−12.6 to +6.1) | not priced |
| Furtado 2016, Demography 53(1) | Census 1980–2000, shift-share; US-born college women | +0.21pp / +0.46pp births per pp of share; high-childcare origins only | not priced |
| Prices | CMS NHE 2024 Table 15 (Medicaid $78.9bn, pinned hash in `mr_leads_papers_2026_09_21`); CMS Provider Information Aug 2026 (1,258,309 residents/day); NCHS NHSR 208 (1,294,800 residents in 2020, 17.9% under 65); KFF HCBS FY2020 ($13,900 / $17,600 per person); BLS CPI-U 2020/2024 | — | — |
| Account | `matched_benefits_2026_09_19/model.py`; τ 0.426 / 0.366, Colas–Sachs 2017 components | — | — |

## Every specification computed

| File | Rows | Grid |
|---|---:|---|
| `hours_tax_specs.csv` | 168 | CT: 4 coefficients × attribution (3 for Table 7, 1 for Table 10) × 4 shocks (metro, national, each with labour force fixed) × 2 populations × 2 scalings. EV: 5 elasticities × 2 shocks × 2 price arms × 2 scalings. Each at τ .426 and .366 with 95% bounds |
| `ces_output_triangle.csv` | 27 | 3 hours specs × σ 1.5/2/2.5 × capital adjustment 0/0.5/1 |
| `partA_side_view_union_frame.csv` | 6 | 2 price arms × 3 shocks (the memo's, union national, union metro) |
| `sept18_partB_correction.csv` | 5 | the memo's published line, then regressor, coefficient and τ corrected step by step |
| `elder_care_doses.csv` | 16 | 4 markets × 4 need nettings |
| `elder_care_specs.csv` | 54 | per netting: 3 AAF measures + pooled, 6 BMW care-hour mappings, 2 home-care prices; plus 6 BMW labour-share rows |
| `elder_care_net.csv` | 48 | 6 nursing-facility specs × 2 home-care prices × 4 nettings, with Monte Carlo quantiles and P(net < 0) |
| `shock_summary.csv`, `metro_shocks.csv` | 2, 424 | shocks under both scalings; per-area shocks and weights |

## Limits

- **Out of window.** The group is 36% of no-diploma labour and 51% of no-diploma immigrants. Removing it moves ℒ about twice as far as the 1980–2000 inflow that Cortés–Tessada identify from, in the opposite direction. The care dose is 1.2 times the Secure Communities first stage. Every estimate is a log-linear extrapolation.
- **The two elder-care measures disagree.** AAF's ACS and LTCFocus results differ by 2.5 times. LTCFocus imputes values for years with no survey, which may attenuate its estimate. The ACS measure also counts institutions that are not nursing homes. The pooled central follows precision, and the ACS figure is kept as an upper arm.
- **Transported inputs.**
  - The HCBS price is 2020 KFF data inflated by CPI.
  - The 65+ spending share assumes equal Medicaid spending per resident by age.
  - The share of Kreider–Werner's "formal helper" that Medicaid pays is taken as 1, which overstates the offset.
  - The ACS (PAOC) measures children under 6, against East–Velásquez's under 5.
  - East–Velásquez's elasticity is short-run.
- **The home-care offset assumes fixed Medicaid rates** (Kreider–Werner's rationing). If rates tracked wages, removing the group would raise Medicaid's unit costs instead. Neither response, nor the account-wide "government as buyer" repricing of low-skill public purchases, is priced here.
- **Unpriced channels:**
  - elderly mortality (the transferable estimate is null);
  - labour supply of family caregivers (Kreider–Werner: family as primary helper +7.5pp, SE 3.5; no US labour-supply estimate);
  - the non-market value of aging in place;
  - elderly and disabled people under 65 in home care (neither nursing-facility nor home-care effects are estimated for them).
- **The hours arm covers native non-group women.** Adding foreign-born non-group women (other residents, population transported) raises the central to $3.31bn.
- **Model uncertainty only.** The Monte Carlo treats the papers' estimates as independent and ignores ACS sampling error in the doses, which is about 0.4pp on 15%.

## Evidence-symmetry notes

- **Rule 1:** every estimate above carries its standard error and population.
- **Rule 2:** no study was dismissed.
  - Shift-share designs (Cortés–Tessada, BMW, Grabowski–Gruber–McGarry, Furtado) are graded alike.
  - BMW's year×state fragility and LTCFocus's imputation are both kept as arms, not grounds for dismissal.
  - Kreider–Werner, an unrefereed job-market paper, enters on the cost side of this channel with the same weight as the NBER working papers on the benefit side.
- **Rule 3:** affiliation carries no weight.
- **Rule 4 (lean of these findings):**
  - Two findings run toward immigration: the hours tax now adds, and "transfers weakly" is withdrawn.
  - Three run against it: the hours tax falls from $8.7bn to $2.7bn, the elder-care value falls to $1.5bn net, and the ACS and BMW routes are overstated relative to the nursing-home count.
  - Against the account as it stands, which adds nothing for these channels, the net move is +$4.1bn to the group's side.
- **Rule 5:** every channel is priced to the evidence standard of the cost lanes, in the same table.

## Reproduce

```sh
# from the repository root (acs_extract ~4 min on the local PUMS zip; the others seconds)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/acs_extract.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/hours_tax.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/elder_care.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/summary.py
```

Re-running `hours_tax.py`, `elder_care.py` and `summary.py` reproduced every derived file byte for byte. `acs_extract.py` ran three times as flags were added (the BMW treatment flag, the Kreider–Werner market, all college women). `acs_national.csv` came out byte-identical each time; each change altered only the files it extends.

- **Inputs from other lanes:** `employment_entry_2026_09_18/_cache/xwalk_puma22.csv`, `hedonic_composition_2026_09_19/derived/geo_county_cbsa_2013.csv`, `consumer_price_benefit_2026_09_18/derived/*` (read only) and `matched_benefits_2026_09_19/{model.py, derived/skill_composition.csv}`.
- **Fallbacks:** `_cache/NH_ProviderInfo_Aug2026.csv` falls back to NPALS 2020, and the net result does not depend on that count. The NHE workbook is checked against the published constants when present.

**Files covered.**

- Brief; FAQ entries 4 and 13, plus the combining rules.
- The 2026-09-18 memo and its `compute.py` and derived tables.
- `mr_leads_papers_2026_09_21` (`elder_care_bound.py`, notes on BMW and Grabowski–Gruber–McGarry).
- The account model and README.
- Full texts of Cortés–Tessada, East–Velásquez, AAF, Kreider–Werner and the Cortés WP.

**Skipped:**

- the Furtado 2016 full text (the abstract and search text were enough for a no-price ruling);
- CEX detail by Hispanic origin (it matters only for the side view).

Model: claude-opus-5-5[1m]. Nothing was committed.
