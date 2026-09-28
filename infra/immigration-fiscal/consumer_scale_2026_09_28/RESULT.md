**Verdict:** The consumer-side scale benefits not yet in the account are small: **−$2.2bn a year** central (a benefit to other US residents; stacked range −$11.9bn to +$6.1bn), or **$53 per member** of the 40.9m Mexican-origin union. Private network fixed costs give most of it, **−$1.9bn** (−$5.4bn to −$0.5bn). In the long run, delivery costs rise almost one-for-one with customers (Roberts 1986: +1% customers and output → +0.98% cost), so only about 2% of the group's $29.6bn energy bills and 4% of its $32.4bn telecom bills spread fixed costs onto others. Grocery variety from city size is worth **−$0.9bn** (−$1.5bn to −$0.3bn; Handbury–Weinstein −0.011 per log point of population). The lower per-capita income the group brings shifts local grocery assortments away from what the average other household buys (Handbury 2021): **+$0.8bn**, with a wide range (−$4.5bn to +$6.0bn). Groceries therefore net to about zero; Handbury's own two-term specification gives +$0.02bn. Media variety that crosses groups is nil, **−$0.1bn** (−$0.5bn to +$0.9bn). Non-Hispanic radio listening barely moves with Hispanic population: 0.017 (s.e. 0.408) per million, a tenth of the own-group effect. Each million Hispanics also comes with 2.6 fewer non-Hispanic-targeted stations (s.e. 2.0). Any 40.9m average residents would supply more of each item: they would live where others live, spend more per head on these goods, and bring average tastes and income. Against them the group is a **relative cost of +$2.5bn** (−$3.7bn to +$10.0bn). On today's electric grid, which is fixed in the short run, the group's load spreads more fixed cost: about **−$8.3bn**, from the LBNL/Brattle 2025 load–price coefficient. That is outside the long-run frame and is not added. [CALCULATION: `price_items.py` → `derived/items.csv`, `derived/arms.csv`] [FRAMING-SENSITIVE: long-run vs short-run network costs; pooled vs cross-group variety]
claude-opus-5-5

# Consumer-side benefits of population scale: Mexican-origin union, 2024 $

Lane `infra/immigration-fiscal/consumer_scale_2026_09_28/`, opened 2026-09-28 23:01 JST, priced 23:19 JST (times
from `date`; see Log). Brief from team-lead, 2026-09-28. Reproduce from the repository root:
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/consumer_scale_2026_09_28/price_items.py`
(rerun byte-identical; LF line endings). Frame: the adopted September 27 main case, 2024 with and without the
40,896,574 CPS 2025 union, effects on the 299.2m other residents. **Sign convention: cost to others positive,
benefit negative.**

## Verdict table

$bn a year, 2024 $. Absolute = with the group against without it. Normalized = against 40.9m average residents
(same spending per head as the average, spread pro rata across areas, average tastes and income).

| Item | Absolute low / central / high | Normalized low / central / high | Per member (abs.) | Evidence level |
|---|---|---|---:|---|
| Grocery variety from city size (HW 2015) | −1.55 / **−0.94** / −0.34 | 0.05 / 0.14 / 0.24 | −$23.02 | measured cross-city elasticity (49 cities, 2005); not causal |
| Grocery product mix from city income (Handbury 2021) | −4.47 / **+0.75** / +5.97 | same as absolute | +$18.37 | measured cross-city relation; β1 insignificant; sign uncertain |
| *Groceries, net* | | | | Handbury's two-term spec: **+0.02** |
| Network fixed costs: electricity | −1.95 / **−0.47** / 0.00 | 0.00 / 0.14 / 0.56 | −$11.54 | measured long-run cost-function elasticities |
| Network fixed costs: natural gas | −0.50 / **−0.12** / 0.00 | 0.00 / 0.05 / 0.22 | −$2.95 | measured long-run cost-function elasticities |
| Network fixed costs: telephone (mostly wireless) | −1.89 / **−0.84** / −0.31 | 0.05 / 0.13 / 0.29 | −$20.52 | modelled: density-cost table × assumed plant share |
| Network fixed costs: internet | −0.75 / **−0.34** / −0.13 | 0.05 / 0.13 / 0.29 | −$8.20 | modelled, as above |
| Network fixed costs: cable and satellite TV | −0.28 / **−0.12** / −0.05 | 0.07 / 0.18 / 0.41 | −$3.00 | modelled, as above |
| *Networks, subtotal* | −5.37 / **−1.89** / −0.49 | 0.16 / **0.63** / 1.77 | −$46.21 | |
| Media variety across groups (Waldfogel) | −0.51 / **−0.11** / +0.92 | 0.60 / 1.00 / 2.02 | −$2.62 | measured cross-group ratio (radio); valuation modelled |
| **Total** | −11.89 / **−2.19** / +6.06 | −3.66 / **+2.52** / +10.00 | **−$53.47** | stacked arms, not an interval |

Beside the table, not added ([CALCULATION: `derived/arms.csv`]):

| Arm | $bn | Why not added |
|---|---:|---|
| Electricity, short run (LBNL/Brattle 2025 coefficient) | −8.28 | holds today's grid fixed; the main case is a long-run comparison |
| Handbury 2021 population term in place of HW | −0.73 | same channel, conditional on city income; β3 s.e. 0.018 |
| Handbury 2021, both terms together | +0.02 | the net grocery reading; shown in the table as the net |
| HW scaled by the group's grocery spending, not headcount | −0.84 | variety follows spending; the published elasticity is on population |
| Media at σ = 5 | −0.05 | σ is assumed |

Scale: the main case is $322–387bn [SOURCE: repo CLAUDE.md, decision 2026-09-27]. The group's charged scale costs
(congestion, PM2.5, road crashes) are $128.5bn. The two scale benefits being adopted are +$13.9bn (earnings) and
+$6.8bn (restaurants) [SOURCE: team-lead brief]. This lane adds about a tenth of those two.

## Method

**Populations and areas.** Union 40,896,574 [DATA: `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv`].
Per-area group and other persons and earnings come from 925 CBSAs and 44 state non-CBSA remainders. They carry the whole
union and 299,214,416 other persons [DATA: `scale_spillovers_2026_09_23/derived/area_measures_cbsa.csv`]. Group share
of persons in each area s_a; national s̄ = 0.1202 [CALCULATION].

**Spending base (CE 2024).** Per-person spending by category, all consumer units and units with a Mexican,
Mexican-American or Chicano reference person (HORREF1 1–3, as in `consumption_key_2026_09_24`). The source is the
Interview PUMD, FMLI summary variables plus MTBI UCCs 270310 (cable/satellite) and 690114 (internet)
[DATA: `consumption_key_2026_09_24/_cache/sources/intrvw24.zip`]. Interview means match the published all-CU means
for electricity ($1,823 vs $1,833), telephone ($1,449 vs $1,460), cable ($457 vs $454) and internet ($694 vs $698)
[DATA: `consumer_price_benefit_2026_09_18/derived/cex_detail_all.csv`]. Food at home is filled in only 19.5% of
Interview records, so its level is the published $6,224.06 per CU. Reading uses the published $125.41. Only the
group/all ratio comes from the microdata: for food, among reporting units (0.907 per person) [CALCULATION].
Per person, the group spends 0.91× the average on groceries, 0.78× on electricity, 0.69× on gas, 0.87× on telephone,
0.72× on internet, 0.40× on cable and 0.34× on reading. Others' food-at-home spending is $769.7bn and the group's
$94.2bn [CALCULATION: `derived/ce_spending.csv`].

### 1. Variety-adjusted grocery prices

*Scale.* Handbury & Weinstein regress the variety-adjusted exact grocery price index on ln(population) across 49
cities (Homescan 2005). With prices adjusted for purchaser and store heterogeneity, the coefficient is **−0.011
(s.e. 0.0036)**. It combines a common-goods term of +0.0041 (0.0018) with a variety term of −0.015 (0.0028). The
dependent variable is in levels around 1, so the lane reads it as a proportional change. New York's index is 4.2%
below Des Moines' [SOURCE: NBER w17067 (revision after Aug 2013), Table 6 col 9, pp. 34–35]. Others' cost from the
group's presence is Σ_a (others' grocery spending_a) × β × (−ln(1 − s_a)). The others'-spending-weighted
−ln(1 − s) is 0.1112; pro-rata average residents would give 0.1281 [CALCULATION]. The low and high ends use the 95% CI
of β.

*Product mix from city income.* Handbury (2021) puts city per-capita income and population in one regression of
income-specific grocery price indexes (125 CBSAs, 100 bootstrap samples). ln(per-capita income) has β1 **−0.042
(0.10)**, and its interaction with demeaned ln(household income) β2 **−0.15 (0.039)**. ln(population) has β3
−0.0095 (0.018), and its interaction β4 −0.011 (0.0072). The population terms are "precise zeros"; the income
gradient is a within-income-group preference externality [SOURCE: NBER w26574 rev. Apr 2021, Table 4 col 2,
p. 36]. Removing the group raises earnings per head, the lane's proxy for per-capita income, by 0.0346 log points
(others'-spending-weighted) [CALCULATION; INFERENCE: earnings proxy]. The average other household's demeaned log
income is −0.092. It is the food-at-home-weighted mean over non-Mexican-reference CUs, with income in 2012 $, clipped
to Handbury's $25k–$200k grid and demeaned by the grid's mean log [CALCULATION; INFERENCE: demeaning reference]. The
cost is others' spending × −(β1 + β2 m) × 0.0346 = **+$0.75bn**, and β1's CI spans −$4.5bn to +$6.0bn.

*Restaurants.* The base is food at home only. Food away from home is the restaurant lane's
(`disease_food_2026_09_28`, −$6.8bn market size), so nothing is netted twice.

### 2. Fixed-cost spreading in private network industries

Others' benefit is the group's payments above the long-run incremental cost of serving it:
(1 − ε) × the group's CE spending, where ε is the long-run elasticity of total cost with respect to customers and
output together, with the service area fixed.

- **Electricity and gas, fixed share 0.02 (0–0.083).** Roberts (1986), 65 US utilities: "A one percent increase in
  both output and number of customers … results in a .98 percent increase in total cost … no significant economies
  resulting from increased customer density" [SOURCE: Land Economics 62(4):378–387, abstract]. Kwoka (2005), a
  larger US sample, finds significant economies only at low output and a modest cost gradient otherwise
  [SOURCE: Applied Economics 37(20):2373–2386, abstract]. Swiss gas distribution has economies of scale of **0.94
  (CI 0.80–1.09)**, i.e. none; its output-density economies (1.57) hold customers fixed, which population growth does
  not [SOURCE: Farsi, Filippini & Kuenzle 2007, Energy Economics 29:64–78, Table 6]. High end: 1 − 1/1.09.
- **Telephone, internet, cable, fixed share 0.04 (0.015–0.09).** Fibre cost per location falls with household
  density: $1.1K at 100–1,000 per mi², $732 at 1,000–10,000 and $635 above 10,000 [SOURCE: Cartesian/ACA Connects
  2021, table from the FBA 2019 density model]. That is an elasticity of −0.18 to −0.06 per log unit of density
  [CALCULATION]. The lane multiplies it by an **assumed** passing-plant share of the bill of 0.25–0.5
  [INFERENCE; the Kansas City study's $500–674 per home passed and $464 per connection are consistent with it:
  SOURCE: CostQuest/Bernstein, Google Fiber Kansas City study]. Wireless has no comparable estimate; it gets the
  same range [INFERENCE].
- **Public enterprises are excluded.** Option D of the main case carries every government enterprise at response 1:
  +$11.62/17.44bn enterprise capital return and +$5.56bn enterprise surplus, covering water and sewer, public gas and
  electricity, transit, tolls and public housing [SOURCE: `main_case_long_run_2026_09_27/RESULT.md` lines 33–34;
  `capital_return_services_2026_09_27/RESULT.md`]. Response 1 credits no fixed-cost spreading. At the private
  networks' 0.02, the omitted credit would be on the order of $0.3–0.5bn [CALCULATION, order of magnitude: 0.02 ×
  $17–23bn]; it is not added.

### 3. Media and cultural variety, cross-group only

Radio, 246 markets (51 with Hispanic listening data) [SOURCE: Waldfogel, NBER w7391 (1999), published RAND J. Econ.
34(3), 2003]:
- Non-Hispanic listening rises 0.175 (0.150) rating points per million non-Hispanics and 0.017 (0.408) per million
  Hispanics (Table 11). The text states "positive within Hispanic and non-Hispanic groups and zero between them".
- Each million Hispanics adds 5.61 (0.58) Hispanic-targeted stations and −2.56 (2.03) non-Hispanic-targeted ones.
  Each million non-Hispanics adds 3.09 (0.56) non-Hispanic-targeted stations (Table 6).

Newspapers: "blacks and whites are more likely to buy daily newspapers in markets with larger black and white
populations, respectively. Similar results hold for Hispanics and non-Hispanics" [SOURCE: George & Waldfogel 2003,
JPE 111(4):765–784, abstract].

The lane prices the cross-group ratio r against the gain others would get if the group had identical tastes. That
gain is others' CE reading spending ($16.7bn) × ((1 − s̄)^(−1/(σ−1)) − 1) at σ = 3, which is $1.10bn
[CALCULATION; INFERENCE: σ assumed, reading spending as the value base]. Radio and free TV have no expenditure base.
The r values:
- central: listening ratio 0.017/0.175 = 0.097;
- high (cost): station ratio −0.83;
- low: station ratio at its upper 95% bound, 0.46.

## What is already inside the account, and double counting

- **CRY earnings premia** (`scale_spillovers_2026_09_23`, +$13.9bn net): nominal wages on the production side. The
  items here are consumer prices and network tariffs, so there is no overlap. HW's common-goods term already nets the
  pass-through of big-city retail costs into grocery prices; the index is net of local cost.
- **Housing** (`housing_transfer_2026_09_23`): residential rents. No commercial-rent pass-through is charged there
  (searched), so no overlap with HW's net index.
- **Congestion** (`congestion_2026_09_23`, part of the $128.5bn): travel delay, including shopping trips. HW's
  index ignores shopping travel, so the time cost of scale sits in congestion alone. No overlap.
- **Restaurants** (`disease_food_2026_09_28`): food away from home is excluded from the grocery base. Its cuisine
  composition row (−$0.6bn) is the restaurant counterpart of this lane's media and product-mix rows. Different goods;
  additive.
- **Consumer-price channel** (`consumer_price_benefit_2026_09_18`): immigrant-intensive services only; its
  expenditure map has no food-at-home or utility lines. No overlap.
- **Public enterprises**: inside the main case (option D), excluded here.
- **`cultural_output_2026_09_19`**: no dollar line to overlap.

## Disconfirmation

- **Long-run network costs are close to constant returns.** The literature this lane was asked to price finds little
  customer-density economy in electricity (Roberts 0.98) and none in gas scale (Farsi 0.94). A Columbia study of 101
  IOUs over eight years finds growth-related capex under 10% of distribution capex. It finds that 5% annual growth would
  nearly double capacity while raising average distribution cost by only about $1/MWh [SOURCE: "Estimating electricity distribution costs using historical data", Columbia QSEL PDF,
  qsel.columbia.edu]. Growth pays roughly its own
  way.
- **Capacity-expansion costs.** LBNL/Brattle find that 2019–2024 load growth lowered prices: +10% statewide load gave
  −0.6 ¢/kWh on the all-sector average. The residential effect was "smaller and lost statistical significance". They
  warn that "a higher growth future can increase retail prices if new supply and delivery infrastructure is
  constrained and costly" [SOURCE: LBNL/Brattle, Factors Influencing Recent Trends in Retail Electricity Prices,
  Oct 2025]. In the short run the group's load is worth about −$8.3bn to others, but that holds the grid fixed. The
  long-run high end (0.083) and low end (0) bracket vintage effects: new plant at today's costs against depreciated
  embedded plant.
- **Crowding out of other varieties.** It is measured in radio (−2.56 non-Hispanic-targeted stations per million
  Hispanics, t = 1.3) and in cuisine (restaurant lane). In groceries, Handbury's income gradient plays that role, and
  the central composition row (+$0.75bn) offsets 80% of the scale row. Shelf space for group-oriented products is not
  separately measured [GAP].
- **The group's consumption of its own products.** HW's index is pooled across households. Part of the variety the
  group's presence adds (Mexican brands, tortillerías, Spanish-language stations) is bought mostly by the group, and
  those gains are excluded by the frame. The HW row is therefore an upper-leaning estimate of the cross-group gain;
  no grocery study splits it by ethnicity [GAP]. Handbury's population term conditional on income, −0.0095 (0.018),
  is indistinguishable from zero.
- **Identification.** HW and Handbury are cross-sectional (49 and 125 cities). City size is not randomly assigned.
  The 2005 and 2010–14 data predate online grocery, which has since narrowed variety gaps across cities [INFERENCE].
- **Telecom rests on an assumption.** The telecom fixed share uses a density-cost table and an assumed plant share. No
  cost-function estimate of customer-density economies in US wireless or cable was found [GAP].

## What can be added beside the account

- **Add beside the costs:** the total, **−$2.2bn** (−$11.9bn to +$6.1bn) absolute and **+$2.5bn** (−$3.7bn to
  +$10.0bn) normalized. Adopting only the benefit rows would break symmetry: the grocery composition row is the same
  regression's counterpart to the grocery scale row, and both belong together.
- **Where it enters.** These are private real-income effects, like the scale lane's private income; none is a fiscal
  receipt. Where telecom prices do not track cost, the network item accrues partly to shareholders, some of them
  foreign [INFERENCE].
- **Not added:**
  - short-run electricity, −$8.3bn (frame);
  - other retail goods beyond groceries: no estimate found;
  - national market-size effects on product innovation: not checked in this lane [GAP].

## Files covered and skipped

Covered:
- `decisions/2026-09-23-evidence-symmetry-rules.md`;
- `disease_food_2026_09_28/derived/items.csv` and `RESULT.md` (format, restaurant rows);
- `scale_spillovers_2026_09_23/RESULT.md` and `derived/area_measures_cbsa.csv`, `metro_distribution.csv`;
- `congestion_2026_09_23/derived/ua_exposure.csv` (inspected; the CBSA file was used because it carries every area
  and both earnings);
- `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv`;
- `main_case_long_run_2026_09_27/RESULT.md`, `capital_return_services_2026_09_27/RESULT.md`;
- `consumption_key_2026_09_24` (CE PUMD, dictionary, CPI jsons);
- `consumer_price_benefit_2026_09_18/derived/cex_detail_all.csv`, `expenditure_map.csv`;
- `housing_transfer_2026_09_23/RESULT.md` (searched).

Primary texts in `_cache/`:
- HW w17067;
- Handbury w26574;
- Waldfogel w7391;
- George–Waldfogel w7944 (black/white only; the Hispanic result is from the JPE abstract);
- Farsi et al. 2007;
- LBNL/Brattle deck (highlights; the PDF download timed out).

Skipped, with reasons:
- Published REStud 2015 and Econometrica 2021 versions: the NBER revisions were used, and published coefficients
  may differ slightly [GAP].
- George–Waldfogel JPE tables: not fetched; the abstract carries the Hispanic result.
- Roberts 1986 and Kwoka 2005 full texts: abstracts only.
- FCC CACM and the Broadband Availability Gap paper: seen in search, not used.
- A direct EIA-861/FERC Form 1 cost-per-customer regression: not run [GAP].
- `w7382.pdf` in `_cache/` is an unrelated paper (a wrong NBER number) and is unused.

## Log
- 2026-09-28 23:01 JST — stub written; brief read.
- 2026-09-28 23:06 JST — primaries read (NBER texts in `_cache/`):
  - Handbury & Weinstein, NBER w17067 (rev. after Aug 2013), Table 6 col 9: variety-adjusted exact
    grocery price index on ln(population), 49 cities, Homescan 2005: **-0.011 (s.e. 0.0036)**; common-goods
    index +0.0041 (0.0018); variety adjustment -0.015 (0.0028). Dependent variable in levels (constant 1.24).
    NY vs Des Moines: variety-adjusted index 4.2% lower. [SOURCE: w17067 Table 6, p.34-35]
  - Handbury, NBER w26574 (rev. Apr 2021; Econometrica 2021), Table 4 col 2: with per-capita income and
    population together, ln(pop) beta3 **-0.0095 (0.018)**, ln(pop) x demeaned ln(HH income) -0.011 (0.0072);
    ln(per-capita income) beta1 -0.042 (0.10), x demeaned ln(HH income) **-0.15 (0.039)**. Population
    effects are "precise zeros"; the city-income effect is a within-income-group preference externality.
    [SOURCE: w26574 Table 4, p.36]
  - Waldfogel, NBER w7391 (1999; RAND 2003): radio, Table 11: non-Hispanic listening on Hispanic population
    0.017 (s.e. 0.408) per million, vs 0.175 (0.150) on non-Hispanic population; Table 6: each million
    Hispanics -2.561 (2.031) non-Hispanic-targeted stations, +5.609 (0.576) Hispanic-targeted.
    Cross-group preference externality ~0. [SOURCE: w7391 Tables 6, 9, 11; column labels of Table 11
    read from the text "positive within ... zero between"]
- 2026-09-28 23:18 JST — network sources read (Roberts 1986, Kwoka 2005 abstracts; Farsi et al. 2007 Table 6;
  LBNL/Brattle 2025 highlights; Cartesian 2021 density table). CE food-at-home Interview gap found (19.5% filled);
  switched to the published level with the microdata ratio. Script run.
- 2026-09-28 23:19 JST — the short-run LBNL arm had a 10x unit slip (0.06 ¢ written for 0.6 ¢); fixed to −$8.28bn;
  rerun byte-identical.
- 2026-09-28 23:21 JST — wording tightened (Columbia study years removed, congestion figure removed, s.e. added); final.
