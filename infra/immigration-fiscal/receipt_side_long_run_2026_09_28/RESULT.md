claude-opus-5-5

**Verdict:** The case holds every incidence-keyed receipt at response 0 because one list in
`full_account_2026_09_20/welfare.py` (0ab245f) files property taxes with capital taxes. The long-run rule the case
already applies to public capital, roads and parks says three of those lines respond, and the other convention-set
lines on both sides stay where they are. At specifications 48 / 11, old → new ($bn):

1. **The zero, traced:** no change. F holds labor taxes only at every specification, so nothing below is counted twice.
2. **Owner-occupied property tax** at a derived long-run response of **0.763** (range 0.672–1): 321.82 / 387.37 →
   **302.77 / 368.32** (−19.05 at both ends; −16.79 to −24.97 across the range).
3. **Tenant-occupied property tax**, $83.84bn split out of business property and keyed by the group's 11.47% of
   contract rent, at 0.708: → **315.01 / 380.56** (−6.81; −10.00 at the case's own owner scale).
4. **Business property, other production taxes, corporate tax, business transfers:** no change. The production
   module's capital channel carries them and nets to zero under the account's rules. Beside the case: −86.85 / −80.98
   if their taxes on the capital that serves the group's jobs were lost outright.
5. **One rule across all 72 lines:** only personal property tax moves, re-keyed to vehicles at 1: → **320.49 / 386.04**
   (−1.33). Defense stays at 0, with its GDP-share bound of +47.51 to +72.00 beside the case.

All three together: **294.63 / 360.18** (−27.19 at both ends; −24.08 to −40.41 across the ranges). The items add
exactly and the band's ends stay at 48 and 11. The service share at which the group turns into a net cost rises from
−2.9–6.8% to 4.1–14.0% of assigned service costs (personal allocation). These are candidate items. Adoption is the
operator's call.

## Items at 48 / 11

All figures are the case's cost in $bn, both fill-in methods averaged, at specifications 48 and 11; the change is the
same at both ends for every item. [CALCULATION: `probe.cjs` → `derived/items.csv`, `derived/probe.json`]

| Item | Response | Cost at 48 / 11 | Change |
|---|---|---:|---:|
| Adopted September 27 case | | 321.82 / 387.37 | |
| 2. Owner-occupied, central (metro land-price fall) | 0.7629 | 302.77 / 368.32 | −19.05 |
| 2. Owner-occupied, low (national land-price fall) | 0.6724 | 305.03 / 370.58 | −16.79 |
| 2. Owner-occupied, high (benefit view) | 1 | 296.85 / 362.40 | −24.97 |
| 3. Tenant-occupied, BEA national $83.84bn, rent key | 0.7084 | 315.01 / 380.56 | −6.81 |
| 3. Tenant-occupied, low / high response | 0.6202 / 1 | | −5.96 / −9.61 |
| 3. Tenant-occupied, case-scaled national $123.13bn | 0.7084 | 311.82 / 377.37 | −10.00 |
| 5. Personal property tax, vehicle key | 1 | 320.49 / 386.04 | −1.33 |
| **All, central** | | **294.63 / 360.18** | **−27.19** |
| All, low (low responses) | | 297.74 / 363.29 | −24.08 |
| All, high (1 everywhere, case-scaled tenant national) | | 281.40 / 346.96 | −40.41 |

Beside the range, not candidates:

| Reading | Response | Change |
|---|---|---:|
| Owner-occupied, short run with assessment caps binding | 0.0295 | −0.74 |
| Owner-occupied, short run with every roll following the market | 0.3020 | −7.54 |
| Owner-occupied, capital-tax view (fixed national capital) | 0.1342 | −3.35 |
| Owner-occupied, Combes–Duranton–Gobillon land elasticity 0.6 / 0.7 / 0.8 | 0.703 / 0.713 / 0.723 | −17.81 at 0.7 |
| Owner-occupied at the probe's 0.79 | 0.79 | −19.73 |
| Item 4, business taxes on the capital serving the group's jobs, lost at 1 | | −86.85 / −80.98 |
| Item 4, the module's cell at retention 0 with owners excluded | | −212.47 / −140.19 |
| Defense at the group's GDP share (capital fixed / full adjustment) | | +47.51 / +72.00 |

## Item 1: where the zero comes from, and what F holds

**The lines.** Twelve receipt lines carry `direct: false`. At 48 / 11 [DATA: `derived/trace.csv`]:

| Line | National | Key | Class | Group at 48 / 11 | Response |
|---|---:|---|---|---:|---:|
| `modeled_owner_property` | 394.86 | owner-housing model | household_direct | 24.97 / 24.97 | 0 |
| `government_asset_income` | 196.29 | resident population | public_asset | 23.60 / 23.60 | 0 |
| `corporate_capital` | 497.76 | capital | corporate_capital | 15.60 / 12.66 | 0 |
| `corporate_labor` | 165.92 | wage | household_direct | 13.36 / 12.45 | 0 |
| `remaining_production_property` | 357.29 | capital | business_property | 11.19 / 9.08 | 0 |
| `other_production_taxes` | 145.26 | capital | other_business | 4.55 / 3.69 | 0 |
| `business_current_transfers` | 139.98 | capital | other_business | 4.39 / 3.56 | 0 |
| `personal_property_tax` | 12.99 | capital | household_direct | 0.41 / 0.33 | 0 |
| `enterprise_surplus` | −47.46 | resident population | public_asset | −5.56 / −5.56 | 1 (option D) |
| two rest-of-world lines, rounding | | none | foreign, rounding | 0 | 0 |

The brief's $13.28bn for business property is `model.json`'s reference cell before the case's corrections; at the
specifications the capital key gives $11.19bn / $9.08bn. [DATA: `assumption_explorer_2026_09_21/derived/model.json`;
`derived/trace.csv`]

**Where the flag was set.** `full_account_2026_09_20/welfare.py`, `response_pools` (0ab245f, 2026-09-20), lists
`corporate_capital`, `corporate_labor`, `modeled_owner_property`, `remaining_production_property` and
`personal_property_tax` as `capital_category`, and a receipt counts as direct only if its class is `personal_income`
or `household_direct` and it is not in that list. `assumption_explorer_2026_09_21/build_model.py` copied the list as
`CAPITAL_CATEGORIES` (02c9996), and `engine.js` applies `indirect_receipt_response: 0` (lines 44, 156). Three household
classes are zeroed only by that list: owner property, personal property and corporate labor. [SOURCE: those files]
The account memo states the intent as rule 1: "Corporate/property incidence, other-business receipts and public-asset
income receive zero direct response; the production model handles induced capital taxes." [SOURCE:
`research/immigration-complete-annual-account-2026-09-20.md`, primary long-run case] The benefits lane had warned
about housing: "Treat owner housing separately: the source capital-tax adjustment distinguishes imputed owner housing,
but our GDP-normalized CES has no separate housing sector, so no exact property-overlap claim is made." [SOURCE:
`full_account_benefits_2026_09_20/README.md` lines 75–77] The income model "omits housing" [SOURCE:
`matched_benefits_2026_09_19/README.md` line 81]. The receipts builder had flagged the business line too: "Residual
includes rental/business property; consumer versus capital incidence unresolved." [SOURCE:
`full_account_receipts_2026_09_20/builder.py` line 214]

**What F contains.** All 64 specifications use the production cell with full capital adjustment, capital-tax
retention 1 and no excluded owners. There F is the labor-tax gain alone: $13.56bn at 48 (gdp normalization) and
$8.95bn at 11 (cash), each equal to the module's `labor_tax_gain_estimate`, with `capital_tax_gain_estimate` exactly 0
(gated to 1e-6 against the module's export). [CALCULATION: `probe.cjs`;
`full_account_benefits_2026_09_20/derived/upstream_replay/scenarios.csv`] The capital term τk(D − retention·O) is 0
because under full adjustment the capital that follows the group's jobs (D = O = $863.70bn of capital income at gdp,
$569.89bn at cash) pays the same taxes elsewhere. So F carries no property tax, no production tax and no business
transfer. The module's τk = 0.246 is Saez and Zucman's rate on capital income, which includes property taxes
[SOURCE: Clemens 2022, p. 15], 60% business and 40% residential in their accounts [SOURCE: Piketty, Saez and Zucman,
data appendix, p. 26]. At retention 1 it multiplies zero.

**Why P + F ignores retention.** The module books any change in capital taxes on the owners' private income, and
rule 3 makes every owner an included other resident: "Extra capital taxes are not free income: their private
counterpart is already in P." [SOURCE: account memo, lines 138–139] At the gdp normalization, retention 0 raises F
from $13.56bn to $226.03bn and lowers P by the same amount to −$212.71bn; P + F stays $13.32bn at retention 0, 0.5
and 1 ($8.79bn at cash). Only excluding the owners breaks it: at retention 0 with owners excluded P + F is $225.79bn
($148.98bn). [CALCULATION: engine production grid, gated to 1e-8]

**No double counting.** Items 2 and 3 are housing, which the module omits; the personal property item is household
durables. Item 4's lines sit inside F's channel and stay at 0. Gates confirm that each item moves only its named lines
and leaves P, F and the capital return unchanged at all 32 distinct specifications. [CALCULATION: `probe.cjs`]

## Item 2: owner-occupied property tax

A receipt's response is the fraction of the group's payment the budget loses when the group is absent; the spending
side counts the budget's own fall separately.

**The rule.** Split the tax on the group's homes into structures (share 1 − λ of value) and land (λ). [INFERENCE]
- **Structures leave.** In the long run the housing stock follows households, so the homes the group occupies are not
  built and their tax goes with them: response 1 on 1 − λ. The capital that would have built them earns its return
  elsewhere, and any tax it pays there is paid by its owners, who are other residents, so under the account's rule it
  is no gain.
- **Land stays.** Its tax is capitalized into its price: it is the public's share of land rent and stays with the land
  whoever holds it. The budget loses only the price fall δ_L on the group's land: response δ_L on λ. The same fall on
  other residents' land moves money among other residents (the budget's loss is what their land's users stop paying),
  so it is left out, as the account leaves out housing on the private side.
- **Together:** r = (1 − λ) + λδ_L = 1 − λ(1 − δ_L). With structures at construction cost in the long run, the whole
  house-price fall is land, λδ_L = δ_H, so r = 1 − λ + δ_H.
- **The price fall.** With unit demand elasticity and the metro's supply elasticity ε, removing a population share s
  lowers house prices by δ_H = 1 − (1 − s)^(1/(1+ε)), capped at λ (land cannot go below zero). Saiz (2007) finds that
  "immigration inflows equal to 1% of a city's population were associated with increases in average or median housing
  rents and prices of about 1%" [SOURCE: IZA DP 2189, p. 1], which fixes the demand side at 1. The supply elasticities
  are Saiz's (2010) metro estimates, "1.75 in metropolitan areas (2.5 unweighted)" [SOURCE: p. 1281].

**Regimes.**
- **Levy-set** (the rate adjusts to raise a levy; Illinois, Washington and Colorado among the group's top states;
  Texas taxing units also compute each year a no-new-revenue rate, "the rate the taxing unit needs to generate about the
  same amount of revenue it received in the year before" [SOURCE: Texas Property Tax Basics, January 2026, p. 39]).
  In cash, other residents pick up the group's whole payment at every horizon: their bills change by the group's tax
  minus the spending fall. Part of
  that pickup is the tax on land the group would have held, which is capitalized and is no burden. Net of it, their
  burden is r times the group's tax minus the spending fall, with the same r. The rate itself moves by a few percent,
  which scales the retained land term λ(1 − δ_L) ≈ 0.24 and moves r by under 0.01. [INFERENCE]
- **Rate- or assessment-limited** (revenue follows assessed value). Proposition 13 caps the rate at "One percent (1%)
  of the full cash value", lets the base grow at most 2% a year and reassesses on purchase, new construction or change
  of ownership [SOURCE: Cal. Const. art. XIII A, §1(a), §2(a)–(b)]. In a long-run steady state the group's homes and
  the land that stays are assessed under the same acquisition rules, so the assessment ratio cancels and r is the same
  formula. The regime matters in the short run. [INFERENCE]
- **Benefit view.** The tax is the price of local services. Hamilton's fiscal zoning "guarantees that new development
  will pay its own way" [SOURCE: Fischel 2000, p. 3], and "the local property tax is both a benefit tax and an efficient
  tax" [SOURCE: Fischel 2000, p. 2]. Nothing is capitalized and the fee leaves with the household: r = 1. The case's
  spending side already charges the services this way (schools at full average cost; school districts alone collect
  40.8% of local property tax [DATA: Census FY2022 Individual Unit File]). This is the high end. The center departs
  from it because 36% of the group's owner tax is paid in California, where the rate is a constitutional ceiling "to be
  collected by the counties and apportioned according to law to the districts within the counties" [SOURCE: art. XIII A,
  §1(a)]. State law sets and divides that tax, so it prices no local choice of services. [INFERENCE]
- **Capital-tax view.** Mieszkowski's (1972) system of property taxes lowers "the after tax return on capital by an
  amount that approximates the average rate of property tax in the economy" [SOURCE: p. 79]. With a fixed national
  capital stock, the capital the group's homes would use pays the average rate elsewhere, so only the land-price fall is
  lost: r = δ_H = 0.134 (−3.35). The case's production module sets full capital adjustment at every specification,
  the premise under which a tax on reproducible capital falls on its users; Piketty, Saez and Zucman say the same of
  housing: "if the supply of housing is very elastic ... then the incidence falls on tenants" [SOURCE: data appendix,
  pp. 26–27]. This view is inconsistent with the case's own capital assumption, so it stays beside the range.

**Where the group pays.** [DATA: `derived/housing.json`, `derived/states.csv`, `derived/counties.csv`]
- The group's owner tax: 36.2% California, 28.9% Texas, 7.9% Illinois, 2.9% Arizona, 2.1% Washington, 2.1% Colorado.
  By the Lincoln Institute's 2024 flags, 78.0% is paid in states with assessment limits, 18.8% with levy limits, 1.6%
  with rate limits only and 1.6% with none.
- Land share of single-family value (Davis, Larson, Oliner and Shui, FHFA Working Paper 19-01, data Version 4.0; the
  2022 county panel for 95.2% of the weight): 0.371 where the group pays, 0.399 nationally. Albouy and Ehrlich find
  "land typically accounts for one-third of housing costs" [SOURCE: NBER WP 18110, p. 1].
- Metro group share 0.302 and supply elasticity 1.73, tax-weighted; 16% of the weight takes an imputed elasticity.
- House-price fall 0.134. For 9.0% of the weight (55 counties, among them El Paso, Hidalgo, Cameron, Webb, Tulare,
  Nueces and Imperial) the fall reaches the land share, so r = 1 there; 8.5 of those 9.0 points sit in metros where the
  group is over half the residents, up to 89%.
- By state, r is 0.687 in California (λ 0.523), 0.861 in Texas (λ 0.268) and 0.808 in Illinois (λ 0.295). By county:
  Los Angeles 0.568, Cook 0.785, Harris 0.756, Riverside 0.840, Bexar 0.912.

**Central and range.** [CALCULATION: `housing.py`; `probe.cjs`]

| Reading | r | Change | Reason |
|---|---:|---:|---|
| Central: metro price fall | 0.7629 | −19.05 | the demand fall lands on the metros where the group lives, at their own supply elasticity |
| Low: national price fall | 0.6724 | −16.79 | other residents relocate freely, so the fall spreads over every metro (s 0.116, ε 1.757: δ_H 0.044) |
| Combes–Duranton–Gobillon | 0.703–0.723 | −17.56 to −18.05 | land priced directly against population; their land-price elasticity is "mostly between 0.60 and 0.80" [SOURCE: CDG 2018, p. 26] |
| High: benefit view | 1 | −24.97 | the tax is the price of services and leaves with the household |

**The short run, beside.** With a fixed stock and unit demand, the vacated homes sell at a price lower by s, and a
market-value roll loses that fall: r = s. Where assessment caps keep incumbents' values below market, the roll loses
nothing. With caps binding everywhere they apply, r = 0.0295 (−0.74); with every roll following the market down,
0.302 (−7.54). Proposition 13 lets a roll fall to market when value drops below the capped base ("or other factors
causing a decline in value", §2(b)), and Texas caps only increases: a homestead's appraised value is limited to the
lesser of market value and last year's appraised value plus 10% [SOURCE: Texas Property Tax Basics, p. 9]. The true
short run is between the two readings, nearer 0.30 in Texas and for recent buyers anywhere. [INFERENCE] Housing is
durable: supply is "highly elastic with respect to positive shocks and almost completely inelastic with respect to
negative shocks in the medium run" [SOURCE: Glaeser and Gyourko, NBER WP 8598, p. 3]. Under a literal removal the
homes would stand for decades and the short-run readings would hold that long. The long-run rule compares steady
states, the same comparison the case makes for roads and parks. [INFERENCE]

## Item 3: renters' property tax, keyed by occupancy

- **The national amount.** BEA Table 7.4.5 splits housing output by tenure but reports taxes on production only for
  the whole housing sector: $356.01bn in 2024 (line 15), against output of $3,143.69bn, of which owner-occupied
  $2,374.19bn and tenant-occupied $740.34bn [DATA: BEA NIPA Table 7.4.5]. The brief's premise that the table splits
  taxes by tenure does not hold. Split by output share (23.55%), tenant-occupied housing pays $83.84bn [CALCULATION:
  `housing.py`; the equal tax per dollar of output is an INFERENCE]. The alternative keeps the case's own owner scale:
  $394.86bn ×
  740.34 / 2,374.19 = $123.13bn.
- **The key.** The group's share of contract rent is 11.47% (gross rent 11.68%, renters 15.65%) [DATA: ACS 2024 PUMS,
  `derived/housing.json`].
- **The response.** Item 2's rule on the rent-weighted counties: land share 0.4235, price fall 0.132, r = 0.7084 (low
  0.6202, high 1) [CALCULATION]. Long-run incidence on tenants follows Piketty, Saez and Zucman (pp. 26–27), and Blau et
  al. (2017, p. 545) count the tax renters pay "indirectly, as renters whose rental payments pay for owners' property
  taxes" [SOURCE: as quoted by Clemens 2022, p. 18].
- **A reallocation that holds the total.** $83.84bn leaves the capital-keyed line for its own rent-keyed line. The
  group's attributed amount on it rises from $2.63bn / $2.13bn (capital key) to $9.61bn, and other residents' falls by
  the same amount; national totals are unchanged in every scenario and incidence rule (gated to 1e-9). At the case's
  response 0 the reallocation alone changes nothing (gated). At 0.708 the case falls by $6.81bn at both ends.
  [CALCULATION: `items.cjs` `splitTenant`; `probe.cjs`]

## Item 4: business property, other production taxes, business transfers

- **F already carries the channel.** Item 1 shows that at every specification the capital that follows the group's
  jobs pays the same taxes elsewhere (retention 1), and that under rule 3 any change would fall on the owners' private
  income. The brief asks for a change only where F does not carry these taxes, so none of these lines moves. [INFERENCE]
- **Keys.** Under full adjustment the capital that leaves is the capital serving the group's jobs, keyed by its wage
  share, 8.02% / 7.48% at 48 / 11 (the `employer_hi` key). The case keys ownership, 3.13% / 2.54% on the capital key.
  The key would matter only if retention were below 1. [CALCULATION: `derived/probe.json`]
- **Beside the case.** Commercial and industrial property ($273.45bn after the tenant split), other production taxes
  ($145.26bn) and corporate tax ($663.69bn) at the wage share and lost at 1: −86.85 / −80.98. The module's own cell at
  retention 0 with owners excluded: −212.47 / −140.19. Each drops a rule the account states (retention 1, owners
  included), so neither is a candidate. [CALCULATION]
- **Business current transfers** ($139.98bn: business payments such as fines, fees and legal settlements) are not a
  tax on capital and do not scale with the group: 0. [INFERENCE]
- **A trap for later work.** τk includes residential property taxes. A case with retention below 1 would overlap items
  2 and 3 unless τk excludes them. [INFERENCE]

## Item 5: one rule, both sides

The rule: a line responds in the long run as far as its base scales with the group's presence. All 72 lines are in
`derived/one_rule.csv` with their base, whether it scales, the current response and the rule's response (gated: each
line once, and the table's effects equal the items'). The lines a convention sets [DATA: `derived/one_rule.csv`]:

| Side | Line | Group at 48 / 11 | Now | Rule | Effect |
|---|---|---:|---|---|---:|
| receipt | owner-occupied property | 24.97 | 0 | 0.763 (item 2) | −19.05 |
| receipt | business property | 11.19 / 9.08 | 0 | tenant part 0.708 at the rent key (item 3); rest 0 | −6.81 |
| receipt | personal property | 0.41 / 0.33 | 0 | 1 at the vehicle key ($1.33bn) | −1.33 |
| receipt | corporate tax, capital and labor shares | 28.95 / 25.11 | 0 | 0: F's channel | 0 |
| receipt | other production taxes | 4.55 / 3.69 | 0 | 0: F's channel | 0 |
| receipt | business current transfers | 4.39 / 3.56 | 0 | 0 | 0 |
| receipt | government asset income | 23.60 | 0 | 0: the assets stay | 0 |
| receipt | enterprise surplus | −5.56 | 1 | 1 | 0 |
| spending | defense | 100.16 | 0 | 0; GDP-share bound beside | 0 |
| spending | general public services | 47.06 | 0.60 / 0.85 | measured across states | 0 |
| spending | economic affairs | 36.43 | 0.38 / 0.64 | by subfunction, 0 where residents do not drive spending | 0 |
| spending | recreation and culture | 6.37 | 0.86 / 1 | measured across states | 0 |
| spending | existing interest | 131.10 | 0 | 0: a legacy stock | 0 |
| spending | interest to foreign holders | 0 | 0 | 0: external key | 0 |
| spending | agricultural subsidies | 0.69 / 0.64 | 0 | 0: acreage and commodities | 0 |
| spending | transport subsidies | 0.03 | 0 | 0 (at most +0.03) | 0 |
| spending | other business subsidies | 2.04 | 0 | 0: paid to included owners | 0 |
| spending | rental assistance | 4.53 | 1 | 1 | 0 |

The other 53 lines keep their class defaults, which the rule confirms: 15 direct receipts (the group's own income,
payroll, purchases and household taxes) and 24 transfers at 1, 5 services at the case's responses, 3 corrections, and
6 external or rounding lines that carry nothing on residents.

- **Personal property tax** (NIPA Table 3.4 line 11, $12.99bn) taxes household vehicles and boats, which leave with the
  group; the motor-vehicle line already responds at 1. Re-keyed from capital ownership (3.1% / 2.5%) to the group's
  share of household vehicles (10.21%) at 1: −1.33, holding the national total (gated). The key counts vehicles, not
  their value, and ignores which states levy the tax, so this is an upper bound. [INFERENCE]
- **Defense.** The brief's $102.78bn uses `model.json`'s raw population share (0.1202); the case's corrected key gives
  $100.16bn [DATA]. The bound beside the case uses the module's own output falls at its labor share of 0.65 (5.56% with
  capital fixed, 8.42% with full adjustment) on $854.76bn: +$47.51bn to +$72.00bn [CALCULATION]. National defense was
  6.0% of GDP in FY1986, 2.9% in 2000, 4.7% in 2010 and 3.2% in 2024 [SOURCE: DoD, National Defense Budget Estimates
  for FY 2025, Table 7-7, pp. 295–296]. The share halved and recovered with threats, a far larger swing than the
  group's 11.7% of residents could produce, so defense stays at 0. [INFERENCE]
- **Existing interest.** $131.10bn at the corrected key (the brief's $134.54bn is the raw share). The stock is the
  legacy of past deficits. The group's part of them is a stock question, which the historical back-cast and the debt
  legacy lane answer; it is not an annual response [SOURCE: `research/immigration-historical-backcast-2026-09-20.md`,
  "Relation to the interest-on-gap calculation"]. Blau et al. (2017, p. 410), quoted by Clemens (2022, p. 30): interest
  payments "represent the current costs of servicing past deficits".
- **Government asset income** ($23.60bn): royalties, rents, dividends and interest on public land, resources and
  funds. The assets stay, so 0. [INFERENCE]

## Together, and the sign break-even

The items add exactly (gated to 1e-9): each touches its own lines and the engine is linear in receipt responses.
Across the 32 distinct specifications the band's ends stay at 48 and 11 with all items on (gated), so the band is the
same as the values at 48 and 11 in every set. [CALCULATION: `probe.cjs`]

Sign break-even, by the September 24 definition as the September 27 lane runs it (the September 27 column reproduces
its committed csv to 1e-4). The share is the part of assigned service costs that must respond for the group to be a
net cost; the frozen rows are other residents' net, $bn, with services frozen and capital fixed (positive is a gain).
[CALCULATION: `sign_reversal.cjs` → `derived/sign_reversal.csv`]

| Measure | Sept 27 | Owner | Tenant | Personal property | All |
|---|---|---|---|---|---|
| Break-even share, personal | −2.87% to 6.80% | 1.99% to 11.81% | −1.13% to 8.59% | −2.54% to 7.15% | 4.06% to 13.95% |
| Same, enterprises at s | 2.83% to 10.83% | 7.42% to 15.63% | 4.47% to 12.54% | 3.15% to 11.16% | 9.38% to 17.68% |
| Break-even share, shared | −0.21% to 9.65% | 4.70% to 14.72% | 1.55% to 11.46% | 0.13% to 10.00% | 6.80% to 16.88% |
| Same, enterprises at s | 5.40% to 13.60% | 10.04% to 18.45% | 7.06% to 15.33% | 5.72% to 13.94% | 12.02% to 20.52% |
| Frozen services, capital fixed | −53.49 to 57.77 | −34.44 to 76.82 | −46.68 to 64.59 | −52.16 to 59.10 | −26.30 to 84.96 |
| Same, enterprises at s | −30.49 to 74.96 | −11.44 to 94.01 | −23.68 to 81.77 | −29.16 to 76.29 | −3.30 to 102.15 |

With every item on, the group is a net cost wherever more than 4–14% of assigned service costs respond (personal
allocation). The case's service responses sit far above that, so the sign holds. [INFERENCE]

## Adoption routes

- **Owner-occupied (item 2)** fits the payload as it stands: one entry, `"receipt:modeled_owner_property": 0.762903`,
  in `meta.responses` and every specification's `line_responses`, applied in every profile like the enterprise
  receipt. No key changes and the capital return is unchanged (gated).
- **Tenant-occupied (item 3)** needs a receipt line, and `applyCorrections` adds only spending lines. Either extend it
  to add receipt lines and use `items.cjs` `splitTenant`, or carry a correction-constant spending line of −$6.8108bn at
  every specification: the constant gives the split's cost at all 32 specifications to 1e-9 (gated). The constant hides
  the line from consumers that re-key receipts, such as a generation split, so the engine route is cleaner.
- **Personal property (item 5)** is a receipt edit per scenario and incidence rule (the re-key, which `applyCorrections`
  supports with the national total held) plus `"receipt:personal_property_tax": 1`.

## Caveats

- The FHFA land shares cover single-family parcels. Multifamily land shares are lower, so the renters' 0.708 understates
  their response. The group's homes are cheaper than their county's average, which may carry a lower land share than
  the county's, in which case the owners' 0.763 understates too. [INFERENCE]
- FHFA's 2022 panel shares run above its pooled 2012–2022 cross section on the same counties (0.372 against 0.330)
  [DATA: `derived/housing.json`]. At the pooled shares, r would be up to 0.04 higher, since r falls one for one with the
  land share where the cap does not bind. [INFERENCE]
- 16% of the owner weight takes an imputed supply elasticity (Orange County takes Los Angeles's, 2.3%; counties outside
  1999 metros take Saiz's unweighted 2.5, 7.9%; the rest a state median, 5.8%).
- 9.0% of the owner weight reaches the cap, where the model removes most of a metro's residents.
- The unit demand elasticity is Saiz's short-run reduced form. A lower per-person elasticity would deepen price falls
  and raise r.
- The group is the ACS proxy (Mexican Hispanic origin or Mexican birth). Its owner tax, $24.70bn, is within 1.1% of the
  case's $24.97bn, so the case's amount stands.
- The regimes come from the Lincoln Institute's 2024 yes/no flags by limit type, with detail caps from its 2022 summary
  workbooks (`inputs/lincoln_limits_2024.csv`, pinned by hash, a source URL on every row). The parsers that built it sit
  in the ignored `_cache/lincoln/`; the file is a curated input, not rebuilt by a lane script.

## Findings beyond the items

- **The owner line's scale.** The case's owner-housing model carries $394.86bn; ACS owners report $375.82bn
  (household-weighted) or $381.77bn (per person); BEA puts the whole housing sector's taxes at $356.01bn, of which
  owner-occupied and farm housing pay $272.17bn by output share. [DATA] The case's owner line alone exceeds BEA's
  housing total, and the business residual (NIPA property tax minus the owner line) is smaller by the same amount than
  BEA's split implies. This does not move the group's owner amount, which the ACS confirms, but it sets the tenant
  national at $83.84–123.13bn. [INFERENCE]
- **The brief's premise on Table 7.4.5** does not hold: the table has no tenure split of taxes (all 23 lines checked).
- **The brief's amounts** ($13.28bn business property, $102.78bn defense, $134.54bn interest) are `model.json` cells
  before the case's corrections; the specifications give $11.19 / 9.08bn, $100.16bn and $131.10bn.

## Reproduce

From the repository root; `acquire.py` fetches only missing inputs (the Census key is needed only to fetch the 2020
tract populations; `--check` needs none):

```sh
# only to fetch missing inputs: set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 infra/immigration-fiscal/receipt_side_long_run_2026_09_28/acquire.py --check
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/receipt_side_long_run_2026_09_28/housing.py
node infra/immigration-fiscal/receipt_side_long_run_2026_09_28/probe.cjs
node infra/immigration-fiscal/receipt_side_long_run_2026_09_28/sign_reversal.cjs
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/receipt_side_long_run_2026_09_28 \
  "uv run --no-project python3 {lane}/acquire.py --check" \
  "OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 {lane}/housing.py" \
  "node {lane}/probe.cjs" "node {lane}/sign_reversal.cjs" --allow-unrun items.cjs
```

Inputs outside the lane, pinned by sha256 in `housing.py`: the ACS 2024 one-year PUMS zips
(`sources/immigration-fiscal/data/external/acs_pums_2024_1yr/`) and Saiz's 2010 elasticities
(`sources/immigration-fiscal/data/external/lifetime/saiz/saiz_2010_msa_elasticity.dta`). Lane inputs are pinned in
`inputs/pins.json` (56 files). `items.cjs` is a module that `probe.cjs` and `sign_reversal.cjs` import.

## Sources

- Albouy, D. and G. Ehrlich, "Housing Productivity and the Social Cost of Land-Use Restrictions", NBER WP 18110: p. 1.
- BEA, NIPA Table 7.4.5 (Section 7 workbook, sheet T70405-A), 2024; NIPA Tables 3.4, 3.5 via the receipts builder.
- California Constitution, article XIII A, §1(a), §2(a)–(b).
- Census Bureau, 2022 Individual Unit File (`22statetypepu.txt`, item T01); 2020 tract-to-PUMA relationship file;
  1999 MSA definitions; 2020 PL 94-171 tract populations.
- Clemens, M., "The Fiscal Effect of Immigration: Reducing Bias in Influential Estimates", IZA DP 15592 (2022):
  pp. 15, 18, 30.
- Combes, P.-P., G. Duranton and L. Gobillon, "The Costs of Agglomeration: House and Land Prices in French Cities",
  revision of January 2018: p. 26.
- Davis, M., W. Larson, S. Oliner and J. Shui, "The Price of Residential Land for Counties, ZIP Codes, and Census Tracts
  in the United States", FHFA Working Paper 19-01; data Version 4.0 (June 2024).
- DoD, National Defense Budget Estimates for FY 2025 (Green Book), Table 7-7, pp. 294–296.
- Fischel, W., "Municipal Corporations, Homeowners, and the Benefit View of the Property Tax", draft of April 2, 2000,
  for the Lincoln Institute conference volume: pp. 2, 3.
- Glaeser, E. and J. Gyourko, "Urban Decline and Durable Housing", NBER WP 8598: p. 3.
- Lincoln Institute of Land Policy, Significant Features of the Property Tax, tax limits and truth in taxation, 2024.
- Mieszkowski, P., "The Property Tax: An Excise Tax or a Profits Tax?", Journal of Public Economics 1 (1972): p. 79.
- Piketty, T., E. Saez and G. Zucman, Distributional National Accounts, data appendix (November 2017), B.4.3: pp. 26–27.
- Saiz, A., "Immigration and Housing Rents in American Cities", IZA DP 2189 (2006): p. 1.
- Saiz, A., "The Geographic Determinants of Housing Supply", Quarterly Journal of Economics 125 (2010): p. 1281.
- Texas Comptroller of Public Accounts, Texas Property Tax Basics, January 2026: pp. 9, 39.

## Log (append-only)

- 2026-09-28: stub written after reading `BRIEF.md` (2b85073). Candidate items only, never a new case; builds on the
  adopted September 27 package (`main_case_long_run_2026_09_27`) and the probe `receipt_long_run_probe_2026_09_28`
  (3cd946e), neither edited. Worker: mainbuild, model claude-opus-5-5.
- 2026-09-28 08:40 JST: inputs pinned (`acquire.py`, `inputs/pins.json`: FHFA land prices v4.0, BEA Section 7, Census
  tract-to-PUMA, 1999 MSA definitions, FY2022 Individual Unit File, 2020 PL tract populations). `housing.py` ran on ACS
  2024 PUMS. Confirmed so far [DATA: `derived/housing.json`]: the ACS proxy's owner property tax is $24.70bn of $381.8bn
  (6.47%), against the case's CPS-modeled $24.97bn of $394.86bn (6.32%), so the owner line's amount holds. Its share of
  contract rent is 11.47% (population 11.59%, vehicles 10.21%). Tax-weighted, the owner tax sits 36% in California, 29%
  in Texas, 8% in Illinois, and 78% in states with assessment limits. The FHFA land share where the group pays is 0.371.
- Item 1, first findings: the zero on owner-occupied property tax was set in `full_account_2026_09_20/welfare.py`
  `response_pools` (0ab245f, 2026-09-20), which lists `modeled_owner_property` among the capital categories, and copied
  into `assumption_explorer_2026_09_21/build_model.py` (02c9996). The benefits lane's README had said the opposite:
  "Treat owner housing separately ... our GDP-normalized CES has no separate housing sector"
  [SOURCE: `full_account_benefits_2026_09_20/README.md`]. At every one of the 64 specifications the production cell is
  full adjustment, retention 1, excluded 0, so F carries labor taxes only. P + F is invariant to retention because
  the module books a capital-tax change on owners' private income, which counts as other residents'. At the gdp
  normalization, F at retention 0 is $226.03bn against $13.56bn at 1, and P moves by the opposite amount
  [CALCULATION: engine production grid].
- 2026-09-28 08:41 JST, corrections to the entries above: the second entry's time stamp is wrong (it was written
  before 08:10 JST), and the case's owner amount comes from the receipts builder's "existing owner-housing model"
  (`full_account_receipts_2026_09_20/builder.py` line 211), which that entry called CPS-modeled without checking.
- 2026-09-28 08:41 JST: items final. `sign_reversal.cjs` evaluates its proportional references before wrapping the
  engine; inside the wrapper the capital return was added twice and the s = 1 gate failed. `probe.cjs` gained the
  capital-tax view and the market short run beside the range, and a one-rule table over all 72 lines with two gates.
  First pass through `scripts/rerun_lane.py`: IDENTICAL, 17 of 17 files.
- 2026-09-28 08:44 JST: second pass through `scripts/rerun_lane.py` after the last edits (probe header, RESULT text):
  IDENTICAL, 17 of 17 files, no script left unrun. Verdict written; nothing committed, staged or stashed.
