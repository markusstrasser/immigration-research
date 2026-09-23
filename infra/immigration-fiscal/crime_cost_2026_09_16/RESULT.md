**Measurement correction, 2026-09-20:** Route A2 applies a sentenced-prisoner offense mix and unit costs to ACS institutional shares, which cannot separate criminal custody, immigration detention or noncorrectional institutions. Its dollar results are conditional proxy scenarios, not measured ordinary-crime or detention costs. See the [current scope](../../../research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md); the historical calculations below are retained for reproducibility.

**Double-count correction, 2026-09-23:** McCollister's aggravated-assault and robbery prices include a statistical-life premium for the chance that the victim dies (76% and 42% of those prices), while murders are also counted separately, so the same deaths are counted twice and these cost figures are biased upward; not re-priced here. The tangible arm also carries the earnings-based slice of the same premium. For the complete account's frame use `infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md`: in the complete account's frame, offences by the whole Mexican-origin population against other US residents cost those victims $4.5bn tangible and $28.9bn full a year (envelope $15–45bn, murder 32%).

# Offence-weighted cost of crime per adult 25–64, by group

Model self-report: claude-opus-5[1m] (Opus 5, 1M context)

**Verdict:** Weighting crimes by their full social cost roughly **quadruples** the crime line in the ledger, and it is still an order of magnitude smaller than the fiscal gap. Priced as the ledger prices prison — a per-inmate-year corrections cost and nothing else — the US-born Mexican-origin minus US-born non-Hispanic white difference at ages 25–64 is **+$356** per adult per year. Adding the victim's own tangible losses takes it to **+$447**. Adding pain, suffering and the statistical value of life lost takes it to **+$1,421**, with a span of **$447 to $2,023** across every arm. Against the −$8,286 extended fiscal gap that is **17.2%** on the central arm, 5.4% tangible-only, and at most 24% on the most adverse arm. The sign is unambiguous and the magnitude does not come close to closing, doubling or reversing anything. Two independent routes agree: the stock route (ACS institutional level × BJS offence mix) gives **+$1,421** and a 2.02× ratio; the flow route (FBI 2019 arrests by ethnicity × offences per arrest × unit cost) gives **+$1,316** and a 2.58× ratio for Hispanic vs non-Hispanic white. Two thirds of the difference is **one offence, murder**, which carries a $13.1m unit cost in 2024 dollars and is therefore the single point of leverage in the whole calculation. The offender's own lost legal earnings add a further **$65–$129**, and they are genuinely missing from the ledger because prisoners live in institutional group quarters and CPS ASEC never sees them. Social cohesion has **no defensible dollar value** and none is offered.

[UNVERIFIED] marks every row priced from a published aggregate rather than measured, and every source read from a secondary summary rather than the paper.

The Mexican **second generation specifically is not separable**. No US arrest, court, prison or group-quarters record carries parents' birthplace. Every figure below for "US-born Mexican-origin" pools the second and third-plus generations on ACS self-identification, exactly as the ledger's institutional-care proxy does.

## Verification

```
cd /Users/alien/Projects/immigration-research && uv run python3 infra/immigration-fiscal/crime_cost_2026_09_16/crime_cost.py
exit=0
```

Integrity gates, all PASS:

```
[McCollister components reconstruct Table 5 total] PASS — 13/13 offences; max residual 0 by construction; removed-slice range 0..737,517 (2008$)
[CPI-U pulled from BLS] PASS — 2008 = 215.303, 2017 = 245.12, 2023 = 304.702, 2024 = 313.689; 2008->2024 = 1.45697, 2017->2024 = 1.27974
[BJS 2021 white offence classes sum to published total] PASS — sum 167.8 vs published total 167.8 per 100k (other/unspecified residual 1.5)
[BJS 2021 hispanic offence classes sum to published total] PASS — sum 358.3 vs published total 358.3 per 100k (other/unspecified residual 1.0)
[ACS 25-64 institutional shares match ledger_residual_micro] PASS — US-born NH white 0.8139%, US-born Mexican-origin 1.4110% (adj 1.7120%)
```

The first gate matters. McCollister's published total is **not** the sum of its own component columns: Table 5 footnote a says an "uncorrected risk-of-homicide" slice is first removed from the victim column so the tangible side does not double count the VSL-based intangible. For murder the removed slice is the entire $737,517 victim cost. The script recovers the slice as a residual and carries a corrected victim cost, so the four components reconstruct the published total exactly for all thirteen offences. A naive tangible-plus-intangible sum would overstate murder by 8.2% and aggravated assault by 7.0%.

## 1. Unit costs per offence

McCollister, French & Fang (2010), *Drug and Alcohol Dependence* 108(1–2):98–109, doi:10.1016/j.drugalcdep.2009.12.002, Tables 3, 4 and 5, 2008 dollars, read from https://pmc.ncbi.nlm.nih.gov/articles/PMC2835847/ this session. Inflated to 2024 dollars with CPI-U annual averages pulled live from the BLS API (series CUUR0000SA0); 2008 → 2024 factor **1.45697**.

| Offence | Victim tangible | Intangible | CJS | Crime career | **Total 2024$** | Total 2008$ |
|---|---|---|---|---|---|---|
| Murder | 1,074,537 | 12,299,701 | 571,643 | 216,439 | **13,087,784** | 8,982,907 |
| Rape / sexual assault | 8,095 | 290,871 | 38,579 | 13,422 | **350,802** | 240,776 |
| Robbery | 4,807 | 32,891 | 20,145 | 6,224 | **61,644** | 42,310 |
| Aggravated assault | 12,676 | 138,445 | 12,590 | 3,098 | **155,924** | 107,020 |
| Arson | 16,685 | 7,479 | 6,399 | 851 | **30,746** | 21,103 |
| Motor vehicle theft | 8,908 | 382 | 5,634 | 806 | **15,694** | 10,772 |
| Stolen property | 0 | 0 | 9,969 | 1,649 | **11,618** | 7,974 |
| Household burglary | 1,984 | 468 | 6,013 | 992 | **9,415** | 6,462 |
| Embezzlement | 0 | 0 | 7,023 | 962 | **7,984** | 5,480 |
| Forgery / counterfeiting | 0 | 0 | 6,709 | 962 | **7,671** | 5,265 |
| Fraud | 0 | 0 | 6,370 | 962 | **7,331** | 5,032 |
| Vandalism | 0 | 0 | 6,061 | 1,021 | **7,081** | 4,860 |
| Larceny / theft | 699 | 15 | 4,195 | 237 | **5,146** | 3,532 |

The intangible column is 94% of the murder total and 83% of the rape total, and it is the reason offence weighting matters at all. It is jury-award and value-of-a-statistical-life derived, so it is a willingness-to-pay number, not an expenditure. Anyone who rejects VSL valuation should read the tangible-only rows throughout, which is why every table below carries both.

**Miller, Cohen, Swedler, Ali & Hendrie (2021)**, *Journal of Benefit-Cost Analysis* 12(1):24–54, the brief's second unit-cost source, was **not obtained at offence level**: the per-offence tables are behind the Cambridge paywall and the Cambridge Core PDF endpoint returns the paywall page. Verified from the open abstract only: 120 million crimes in the USA in 2017 imposed $2.6 trillion of losses ($620bn monetary plus $1.95tn quality-of-life; 95% uncertainty interval $2.2–3.0tn), with violent crime about 85% of the total. That is $3.33tn in 2024 dollars. Because the Miller intangible share (75% of total) is close to the McCollister-weighted intangible share in this lane, substituting Miller would not plausibly move the ratios; it could move the levels. **[UNVERIFIED at offence level.]** A DOJ or Vera per-offence criminal-justice-system cost was also not found; Vera has published no 2024 "Price of Prisons" edition, so the corrections cost below uses the figure the peer ledger lane already uses.

## 2. Annual social cost per prisoner-year

Corrections cost per prisoner-year: **$59,619** in 2024 dollars, from $57,911 in 2023 dollars ($63.6bn state corrections spending 2023 ÷ 1,098,228 state prisoners), the same figure the institutional-care line in `ledger_residual_micro_2026_09_16` uses. Arms at $45,000 and $70,000.

Mean time served, initial releases, from BJS *Time Served in State Prison, 2016* Table 1, as transcribed by the peer lane: murder 15.0 years, rape/sexual assault 6.2, robbery 4.7, assault 2.5, violent overall 4.7, property 1.8, drug 1.8, public order 1.7.

| Class | Time served | Victim tangible /yr | Victim total /yr | + corrections | **= total /yr** |
|---|---|---|---|---|---|
| Murder | 15.0 | 71,636 | 819,980 | 59,619 | **879,599** |
| Rape / sexual assault | 6.2 | 1,306 | 48,194 | 59,619 | **107,813** |
| Aggravated assault | 2.5 | 5,070 | 56,095 | 59,619 | **115,714** |
| Robbery | 4.7 | 1,023 | 7,505 | 59,619 | **67,124** |
| Other violent | 4.7 | 2,697 | 29,838 | 59,619 | **89,457** |
| Burglary | 1.8 | 1,102 | 1,339 | 59,619 | **60,958** |
| Motor vehicle theft | 1.8 | 4,949 | 5,141 | 59,619 | **64,761** |
| Larceny / other property | 1.8 | 389 | 397 | 59,619 | **60,016** |
| Drug | 1.8 | 0 | 0 | 59,619 | **59,619** |
| Public order | 1.7 | 0 | 0 | 59,619 | **59,619** |

A murder prisoner-year is worth 14.8 drug prisoner-years on this accounting. That single ratio is the entire content of "offence weighting", and it is why the Hispanic/white cost ratio (2.56× on route A1) exceeds the Hispanic/white imprisonment ratio (2.14×).

## 3. Route A1 — BJS stock, Hispanic vs non-Hispanic white

BJS 2021 sentenced state prisoners per 100,000 residents by most serious offence, from `acs_institutional_2026_09_16/bjs_offense_by_ethnicity.csv` (BJS *Prisoners in 2022 – Statistical Tables*, Tables 16–17). Converted from per-resident to per-adult-25–64 with ACS 2021 1-year populations pulled from the Census API (B01001H non-Hispanic white alone, B01001I Hispanic).

| Arm | NH white | Hispanic | Difference | Ratio |
|---|---|---|---|---|
| Corrections only (what the ledger already prices) | 192 | 423 | **+231** | 2.21 |
| + victim tangible, amortised | 222 | 508 | **+285** | 2.28 |
| + victim tangible + intangible | 553 | 1,419 | **+866** | 2.56 |
| + victim total, corrections $45k | 506 | 1,315 | +809 | 2.60 |
| + victim total, corrections $70k | 587 | 1,493 | +906 | 2.54 |
| + victim total + full CJS (double counts prison) | 576 | 1,480 | +904 | 2.57 |

Composition of the +$866 central difference:

| Offence | White $ | Hispanic $ | Difference | % of difference |
|---|---|---|---|---|
| Murder | 324 | 889 | +565 | **65.3%** |
| Aggravated assault | 44 | 172 | +128 | 14.8% |
| Rape / sexual assault | 69 | 146 | +77 | 8.9% |
| Robbery | 14 | 57 | +43 | 5.0% |
| Public order | 22 | 41 | +19 | 2.2% |
| Other violent | 16 | 33 | +17 | 2.0% |
| Drug | 29 | 43 | +14 | 1.6% |
| Burglary | 18 | 23 | +5 | 0.6% |
| Motor vehicle theft | 2 | 3 | +2 | 0.2% |
| Fraud | 3 | 2 | −1 | −0.1% |
| Larceny / other property | 12 | 8 | −4 | −0.4% |

Fraud and larceny are the only negative rows, matching the memo's finding that fraud is the one category where the white per-capita prison stock exceeds the Hispanic one. They are worth −$5 together against murder's +$565. Offence weighting does not rescue the property side; it buries it.

## 4. Route A2 — ACS institutional level × BJS offence mix, the ledger's groups

The level comes from ACS 2023 1-year PUMS institutional group quarters at ages 25–64, the same tabulation the ledger's institutional-care line uses: US-born non-Hispanic white **0.8139%**, US-born Mexican-origin (self-ID) **1.4110%**, generic-Hispanic-coding-adjusted **1.7120%**. The offence mix comes from BJS 2021 (white mix for the white group, Hispanic mix for the Mexican-origin group).

| Arm | US-born white | US-born Mexican-origin | Difference | Ratio |
|---|---|---|---|---|
| Corrections only, all institutional GQ counted | 485 | 841 | **+356** | 1.73 |
| Tangible only | 562 | 1,009 | **+447** | 1.79 |
| **BASE: tangible + intangible** | **1,399** | **2,820** | **+1,421** | **2.02** |
| + generic-Hispanic prison-coding adjustment | 1,399 | 3,422 | +2,023 | 2.45 |
| Correctional share of institutional GQ = 0.85 | 1,189 | 2,397 | +1,208 | 2.02 |
| Corrections $45k/yr | 1,280 | 2,614 | +1,334 | 2.04 |
| Corrections $70k/yr | 1,484 | 2,967 | +1,483 | 2.00 |
| Adjusted coding + 0.85 correctional share | 1,189 | 2,909 | +1,719 | 2.45 |

**Full span: +$447 to +$2,023.** The sign never changes.

This line has the **opposite sign** to the institutional-care line in `ledger_residual_micro_2026_09_16`, which *narrows* the gap by $48 in its base arm. Both are correct for their own question. That line charges the group's whole adult 18+ institutional population, including 65+ nursing-home residents, to its 25–64 adults; the white institutional bill is 55% nursing home and the Mexican-origin bill is 11%, so the old-age leg dominates and favours the younger group. A cost-of-**crime** line must drop the 65+ nursing leg, and at ages 25–64 alone the Mexican-origin institutional rate is 1.73× the white rate. If both lines are wanted in one ledger, the clean decomposition is: nursing and 65+ care stay in institutional care, and the under-65 correctional part is replaced by the numbers here.

Route A2 **understates** for one clear reason: it covers only ages 25–64, so it excludes 18–24 prisoners entirely, and that is where the group gap is widest (male imprisonment ratio 2.83× at 18–19 and 2.90× at 20–24 in 2022, against 2.15–2.42× at 30–39). It also excludes the 65+ correctional population, which is small.

## 5. Route B — FBI 2019 arrest flow, Hispanic vs non-Hispanic white

FBI *Crime in the United States 2019* Table 43C (arrests by race and ethnicity, adults 18 and over; ethnicity panel 10,831 agencies, 2019 estimated population 229,735,355), scaled to national adult arrest totals offence by offence using Table 29 (estimated national arrests) and the adult share observed in Table 43A/43C. Arrests are converted to offences with reported offences per arrest from Table 1 ÷ Table 29: murder 1.49, rape 5.60, robbery 3.59, aggravated assault 2.13, burglary 6.51, larceny 6.26, motor vehicle theft 8.95, all others 1.00. Denominators are ACS 2019 adults 18+ (non-Hispanic white 160,282,147; Hispanic 41,856,869).

| Arm | NH white | Hispanic | Difference | Ratio |
|---|---|---|---|---|
| Tangible victim + CJS, reported offences only | 239 | 480 | **+241** | 2.01 |
| + intangible, reported offences only | 834 | 2,150 | **+1,316** | 2.58 |
| + intangible, NCVS reporting uplift 1/0.409 | 2,039 | 5,256 | +3,217 | 2.58 |

The **ratio is invariant** to every multiplier applied equally to both groups — offences per arrest, reporting uplift, national scale-up — so the ratio is the robust output of this route and the level is the fragile one.

| Offence | NH white arrests | Hispanic arrests | NHW $bn | Hisp $bn | Hispanic share |
|---|---|---|---|---|---|
| Murder | 2,641 | 2,014 | 50.5 | 38.5 | **43.3%** |
| Aggravated assault | 131,510 | 91,276 | 42.8 | 29.7 | 41.0% |
| Rape / sexual assault | 8,390 | 6,057 | 15.8 | 11.4 | 41.9% |
| Larceny | 390,029 | 103,324 | 12.0 | 3.2 | 20.9% |
| Motor vehicle theft | 31,173 | 16,969 | 4.2 | 2.3 | 35.2% |
| Burglary | 74,743 | 30,687 | 4.1 | 1.7 | 29.1% |
| Robbery | 14,011 | 13,465 | 2.8 | 2.7 | **49.0%** |
| Fraud | 56,678 | 15,770 | 0.4 | 0.1 | 21.8% |

Non-Hispanic white arrests are **constructed**, not published: the race panel is rescaled to the ethnicity panel's coverage offence by offence and Hispanic arrests are subtracted from white arrests, on the standard assumption that most Hispanic arrestees are coded racially white. **[INFERENCE]**

Excluded for want of a McCollister unit cost: other (simple) assaults, 534,255 adult arrests with an 18.4% Hispanic share; drug 20.0%; driving under the influence 26.4%; weapons 22.6%; and all remaining public-order offences. The overall adult Hispanic arrest share is 18.8%, so the excluded block is close to neutral for the **ratio** but lowers both **levels**.

## 6. Reconciliation with the NCVS 1.4× victim-report ratio

| Measure | Hispanic / white |
|---|---|
| NCVS 2012–15 victim-reported offender index, per capita | **1.37×** |
| Route B, UCR index violent arrests only, unweighted | 2.77× |
| Route B, violent arrests **including simple assault**, unweighted | **1.85×** |
| Route B, violent offences only, cost-weighted | 2.82× |
| Route A1, violent classes only, cost-weighted | 2.69× |
| Route A1, imprisonment rate, all offences | 2.14× |
| Male age-specific imprisonment 25–39, 2022 (memo §8) | 2.15–2.84× |

The 1.37× and the 2.8× are not the same quantity, and the single largest reason is **simple assault**. NCVS violent victimisation is dominated by simple assault, which the UCR index category excludes. Putting simple assault back into the arrest count drops the ratio from 2.77× to **1.85×**, which brackets the victim-report 1.37× far more closely than the headline arrest figure does. The residual gap from 1.85× to 1.37×, and the larger gap to the 2.1–2.9× prison ratio, is the enforcement, charging and sentencing wedge plus the offence-severity mix, and nothing in any of these sources separates the two. Cost weighting deliberately amplifies severity: the Hispanic arrest share is 43% for murder, 49% for robbery and 42% for rape, against 21% for larceny and 22% for fraud. **[FRAMING-SENSITIVE]** An analyst who believes the enforcement wedge explains most of the prison gap should read the NCVS-comparable 1.85× row and scale the cost lines down by roughly a third.

## 7. The offender's own lost legal earnings

Separate line, **not** included in any total above. Group mean earnings for all adults 25–64 from CPS ASEC 2025 (income year 2024), by-generation memo §2: US-born non-Hispanic white $70,424, Mexican second generation $49,789.

| Arm | US-born white | US-born Mexican-origin | Difference |
|---|---|---|---|
| Group mean earnings, all adults 25–64 (upper bound) | 573 | 703 | **+129** |
| Federal minimum wage, full time (McCollister's own basis) | 123 | 213 | +90 |
| Half group mean (negative selection into prison) | 287 | 351 | +65 |

**Is it already inside the ledger's tax gap? No, and the direction is clear.** Incarcerated adults live in institutional group quarters and are therefore outside the CPS ASEC civilian noninstitutional universe. The −$8,286 gap never sees them at all, neither their zero taxes nor their zero transfers. Because the Mexican-origin institutional rate at 25–64 is 1.73× the white rate, adding prisoners back as zero-earning, zero-tax adults would **widen** the measured gap by roughly the amounts in the table. Counting this line and McCollister's "crime career" component together would double count; the ledger-consistent line is the one above.

## 8. Fragmentation and social cohesion — no dollar estimate

Asked for, and refused on the evidence. There is no per-adult dollar figure for lost social cohesion that survives the standards applied to the lines above.

1. **Putnam (2007)**, "E Pluribus Unum", *Scandinavian Political Studies* 30(2):137–174, doi:10.1111/j.1467-9477.2007.00176.x. In the short run, ethnic diversity is associated with lower trust, less altruism and fewer friendships, including within one's own group. It reports no dollar value and proposes none. It is a cross-sectional association on US localities with a long replication dispute about whether the effect survives controls for deprivation and residential sorting. **[UNVERIFIED: the replication literature was not read this session.]**
2. **Algan & Cahuc (2010)**, "Inherited Trust and Growth", *AER* 100(5):2060–2092, and Algan & Cahuc (2013, *Handbook of Economic Growth* ch. 2): about a fifth of cross-country variance in income per head 1980–2009 co-varies with generalised trust, and one standard deviation more trust associates with income per head about 6.8% higher. **[UNVERIFIED: read from secondary summaries, not the papers.]**
3. **Wellbeing-valuation attempts**, e.g. "Valuation of Trust in Government: The Wellbeing Valuation Approach", *Sustainability* 13(19):11000 (2021), doi:10.3390/su131911000, price trust by the income equivalent of its life-satisfaction effect. **[UNVERIFIED: not read.]**

Why none becomes a ledger line, in order of severity. **(a)** None is identified as a causal effect of any specific group's presence; Putnam is a diversity-index correlation and Algan–Cahuc a cross-country growth regression instrumented by ancestors' inherited trust, and neither licenses attributing a dollar cost to US-born Mexican-origin adults. **(b)** Any trust-to-income elasticity applied to a US subgroup would double count the wage and tax effects the ledger measures directly. **(c)** The sign is contested in principle; the same literature finds diversity raising innovation and variety, so a one-sided cost line would be a framing choice, not a measurement. **[FRAMING-SENSITIVE]** **(d)** Any number produced would carry an uncertainty band wider than the entire −$8,286 gap and so could not change a decision.

Verdict on this item: **[UNVERIFIED] / speculative**. Stated as a qualitative consideration, never as a dollar figure.

## 9. Lifetime scale check

Route A2's difference is a flow per adult-year. Over the 40 years from 25 to 64, undiscounted: base arm $1,421 × 40 = **$56,846** per adult; adjusted-coding arm $2,023 × 40 = **$80,912**. Against the by-generation memo's synthetic-cohort lifetime fiscal gap of about $250,000 per adult (undiscounted), crime cost is a **23–32% addition**. Cohen & Piquero (2009), *J Quant Criminol* 25:25–49, abstract read from the publisher page this session: *"We estimate the present value of saving a 14-year-old high risk juvenile from a life of crime to range from $2.6 to $5.3 million. Similarly, saving a high risk youth at birth would save society between $2.6 and $4.4 million."* That is the lifetime cost of one high-risk offender, not a population average, so it is not comparable to the per-adult figures and is quoted only for order of magnitude. The frequently cited $4.2–7.2m "career criminal" figure is **not** in the abstract and was not verified. **[UNVERIFIED]**

## 10. Headline

US-born Mexican-origin minus US-born non-Hispanic white, dollars per adult 25–64 per year, 2024 dollars.

| Measure | Value | % of −$8,286 |
|---|---|---|
| Route A2 corrections only (already in the ledger) | +356 | 4.3% |
| Route A2 tangible (corrections + victim tangible) | +447 | 5.4% |
| **Route A2 total (corrections + victim + intangible)** | **+1,421** | **17.2%** |
| Route A2 span across all arms | +447 … +2,023 | 5.4% … 24.4% |
| Route B tangible (Hispanic vs NH white, adults 18+) | +241 | 2.9% |
| Route B total (Hispanic vs NH white, adults 18+) | +1,316 | 15.9% |
| Lost legal earnings, group-mean arm | +129 | 1.6% |

**Which route is more defensible.** Route A2 for the per-adult level on the groups the ledger actually compares, because its level is an ACS measurement on exactly the self-identified groups the ledger's own institutional proxy uses, and because it is the only route whose denominator is adults 25–64. Route B for the victim-cost component in isolation, because the stock route prices only crimes that ended in a state-prison sentence and therefore misses every uncleared and unprosecuted offence, while the arrest route at least scales by offences known. That the two disagree by 8% on the level ($1,421 vs $1,316) despite different data, different years, different groups and different failure modes is the strongest evidence in this lane that the central number is about right. Neither route is defensible as a *causal* statement about admitting immigrants; both describe resident characteristics.

## Sources

| Item | Source |
|---|---|
| Unit costs per offence, 2008$, Tables 3/4/5 | McCollister KE, French MT, Fang H (2010), *Drug Alcohol Depend* 108(1–2):98–109, doi:10.1016/j.drugalcdep.2009.12.002. https://pmc.ncbi.nlm.nih.gov/articles/PMC2835847/ |
| Total US crime cost 2017, $2.6tn | Miller TR, Cohen MA, Swedler DI, Ali B, Hendrie DV (2021), *J Benefit-Cost Anal* 12(1):24–54, open abstract. https://www.cambridge.org/core/journals/journal-of-benefit-cost-analysis/article/abs/incidence-and-costs-of-personal-and-property-crimes-in-the-usa-2017/37CD0589C84DAEF0FEC415645A6D7977 — per-offence tables paywalled, NOT obtained |
| CPI-U annual averages 2008–2025 | BLS API series CUUR0000SA0. https://api.bls.gov/publicAPI/v2/timeseries/data/ |
| Sentenced state prisoners by offence × race/Hispanic origin, 2021 | BJS *Prisoners in 2022 – Statistical Tables* (p22st), Tables 16–17, via `acs_institutional_2026_09_16/bjs_offense_by_ethnicity.csv` |
| Mean time served by offence | BJS *Time Served in State Prison, 2016* (tssp16) Table 1, via `hisp_violent_stock_2026_09_16/` |
| Corrections $63.6bn / 1,098,228 state prisoners 2023 | USAFacts from Census ASSF and BJS p23st, as used in `ledger_residual_micro_2026_09_16` |
| Arrests by race and ethnicity, 2019 (Tables 43A/43C) | FBI *Crime in the United States 2019*. https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-43 |
| Estimated national arrests 2019 (Table 29) | https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-29 |
| Offences known 2019 (Table 1) | https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-1 |
| Institutional GQ by age band, nativity and origin, ACS 2023 | `ledger_residual_micro_2026_09_16/acs_institutional_by_age_band.csv` (ACS 1-year PUMS, TYPEHUGQ = 2) |
| Populations by ethnicity and age, ACS 2019 and 2021 | Census Data API, B01001H and B01001I. https://api.census.gov/data/2021/acs/acs1 |
| NCVS offender race/ethnicity 2012–15 | BJS *Race and Hispanic Origin of Victims and Offenders, 2012–15*, Tables 2 and 11, via by-generation memo §8 |
| Group mean earnings 25–64 | CPS ASEC 2025, by-generation memo §2 |
| Lifetime cost of a high-risk youth | Cohen MA, Piquero AR (2009), *J Quant Criminol* 25:25–49, doi:10.1007/s10940-008-9057-3, abstract |
| Diversity and social trust | Putnam RD (2007), *Scand Polit Stud* 30(2):137–174, doi:10.1111/j.1467-9477.2007.00176.x |
| Trust and growth | Algan Y, Cahuc P (2010), *AER* 100(5):2060–2092 |

## Assumptions, stated

1. **The offence mix is all-Hispanic, not Mexican-origin.** BJS publishes no Mexican-origin or nativity split of prisoners. Route A2 applies the Hispanic mix to the Mexican-origin group. If Mexican-origin offending is less violent than all-Hispanic offending, this overstates; if more, it understates. No source resolves it.
2. **The level pools generations.** ACS has no parental birthplace, so "US-born Mexican-origin" is second and third-plus combined. The NLSY97 evidence in the by-generation memo §6 finds no significant difference between the Mexican second generation and third-plus whites in time to first arrest, which would put the second-generation-specific figure *below* the pooled one. One cohort, one design.
3. **All institutional group quarters at 25–64 are priced as correctional** in the base arm, as the ledger does. This pools local jails (cheaper, far shorter stays), state psychiatric hospitals (far dearer) and juvenile facilities. The 0.85 arm is an unsourced sensitivity. **[INFERENCE]**
4. **Amortising victim cost over mean time served assumes one offence per sentence and a steady state.** Offenders with multiple victimisations in one sentence are undercounted; the "most serious offence" coding means every lesser offence in the same sentence is priced at zero.
5. **The stock route prices only crimes that ended in a state prison sentence.** Federal prisoners, jail populations and every uncleared offence are outside it. It is a lower bound on victim cost and the flow route exists to show by how much.
6. **Drug, public-order and "other/unspecified" prisoners carry corrections cost and zero victim cost.** McCollister publishes no unit cost for drug offences. Drug crime's externalities — overdose, addiction, property crime committed to fund use — are therefore priced at zero here for both groups. Hispanic drug imprisonment is 36.1 per 100k against white 25.1, so this understates the difference; white drug *use* is higher in self-report, which cuts the other way.
7. **Route B's non-Hispanic white arrests are constructed, not published.** Race and ethnicity panels cover different agency sets, and there is no published race × ethnicity cross-tab. **[INFERENCE]**
8. **Agencies that report ethnicity to the UCR skew toward high-Hispanic states**, so the Hispanic arrest share is biased up and route B's ratio with it. **[FRAMING-SENSITIVE]**
9. **The 2019 arrest year is not the 2021 prison year or the 2023 ACS year.** Each route uses the latest year its source publishes the needed cross-tab; nothing is interpolated.
10. **No standard errors anywhere.** The Census tabulate endpoint returns point estimates without replicate weights, BJS publishes no variance on offence × ethnicity counts, and McCollister publishes no confidence intervals on unit costs. The arm spans are the only uncertainty representation in this lane and they represent specification uncertainty, not sampling error.
11. **Everything is a resident-characteristic accounting, not a policy effect.** None of it identifies the effect of admitting an immigrant.

## What cannot be measured

- **The Mexican second generation on its own.** No US arrest, court, prison or group-quarters record carries parents' birthplace, and the ACS has not carried it since 1970. Only NLSY97 separates it, on one cohort, for time to first arrest.
- **The third generation on its own.** Ethnic attrition means roughly 30% of third-generation Mexican-origin youth do not self-identify, and leavers are positively selected, so the self-identified pool is biased upward.
- **Victim ethnicity against offender ethnicity.** Most crime is intra-group, so a large share of the victim cost computed here falls on members of the same group. Nothing in the ledger framing accounts for that, and the NCVS tables used do not cross victim and offender ethnicity in the form needed.
- **The enforcement wedge separately from the severity mix.** The 1.37× to 2.8× spread contains both and no source in this lane decomposes them.
- **Social cohesion**, per §8.
- **Deterrence and incapacitation benefits**, which are the flip side of corrections spending and are counted nowhere.
- **White-collar and corporate crime by either group.** Miller et al. exclude it, McCollister prices only individual fraud, forgery and embezzlement, and the memo's own note that under-prosecution of financial crime makes the incarceration comparator understate white harm applies with full force to every number here.

## Files

All under `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/crime_cost_2026_09_16/`:

- `RESULT.md` — this file
- `crime_cost.py` — the model; run it as shown above
- `crime_cost_by_group.csv` — every arm of every route, plus the unit-cost table
- `crime_cost_result.txt` — the full printed tables
- `_cache/` — cached BLS and Census API responses (gitignored)
