**Verdict:** Infectious disease and food safety cost other US residents little: about **$0.30bn a year** central ($0.01–1.8bn, stacked arms), or **$7 per member** of the 40.9m Mexican-origin union, against $29bn for its crime victims. Tuberculosis is the largest disease item at **$0.05bn** ($0.01–0.20bn). The group has 17% of US TB cases (1,307 Mexico-born and about 459 Mexican-origin US-born cases in 2024) against 12% of the population. Yet only about **56 cases a year among outsiders** trace to it: TB among the foreign-born is mostly reactivation of infection acquired abroad (7.5% recent transmission, against 27.4% among the US-born), and transmission runs mostly within households and networks. Chagas blood screening, locally acquired neurocysticercosis, hepatitis A and measles add about $0.015bn together. COVID-19 is not priced: the sign is unidentified, and each 1% of other residents' 2020–22 deaths would be about $107bn one-off. Food safety is **speculative at $0.23bn** ($0–1.6bn): ethnic independent restaurants draw 1.6–1.7 times the critical violations, but inspection scores do not predict outbreaks. Variety runs the other way. The Mexican-cuisine mix gives outsiders a **benefit of $0.6bn** whose sign is uncertain ($4.7bn cost to $15.4bn benefit), because total restaurants per head do not rise with the group's share, so other cuisines are crowded out. Generic restaurant market size is worth **$6.8bn** ($1.1–19.2bn) to outsiders, but any 40.9m residents would supply it; against average residents it becomes a $1.2bn relative cost. Food prices and produce quality add nothing new. TB control is a candidate fiscal key correction of +$0.02bn. Against the average resident, disease and food safety come to $0.22bn. [CALCULATION: `price_items.py` → `derived/items.csv`, `derived/totals.csv`] [FRAMING-SENSITIVE: deaths valued at the $13.7m VSL; variety depends on σ and on the no-group counterfactual]
claude-opus-5-5

# Infectious disease and food: what the Mexican-origin population's presence costs or gives other US residents (2024 $)

Lane `infra/immigration-fiscal/disease_food_2026_09_28/`, opened 2026-09-28 20:57 JST, priced 21:36 JST
(times from `date`; see Log). Brief from team-lead, 2026-09-28. Reproduce from the repository root:
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/disease_food_2026_09_28/price_items.py`
(rerun is byte-identical; LF line endings). Sign convention in `derived/`: **cost to others positive, benefit
negative.**

## Verdict table

$bn a year, 2024 $, cost to residents outside the group (negative = benefit). Absolute = with the group against
without it. Normalized = against the same number of average residents (definition per row in Method).

| Item | Absolute low / central / high | Normalized low / central / high | Per member (abs., central) | Evidence level |
|---|---|---|---:|---|
| TB: secondary cases outside the group | 0.007 / **0.048** / 0.204 | −0.002 / 0.010 / 0.093 | $1.17 | modelled: measured counts × assumed cross-group share; contested |
| Measles importation spread | 0.000 / 0.0001 / 0.001 | 0.000 / 0.0000 / 0.001 | $0.00 | measured counts; negligible |
| Hepatitis A, travel-linked secondary cases | 0.000 / 0.0002 / 0.002 | 0.000 / 0.0002 / 0.002 | $0.01 | measured travel share; negligible |
| Chagas blood-donor screening | 0.000 / 0.007 / 0.025 | 0.000 / 0.005 / 0.019 | $0.17 | modelled: assumed volume, price, attribution |
| Neurocysticercosis, local transmission | 0.001 / 0.007 / 0.053 | 0.001 / 0.005 / 0.039 | $0.18 | modelled from surveillance shares; negligible |
| **Disease subtotal** | 0.008 / **0.062** / 0.286 | −0.002 / **0.021** / 0.153 | **$1.53** | |
| COVID-19 | not priced | not priced | — | unidentified (see Disconfirmation) |
| Food safety, group-staffed kitchens | 0.000 / **0.234** / 1.561 | 0.000 / 0.195 / 1.297 | $5.72 | **speculative** |
| **Disease + food safety** | 0.008 / **0.297** / 1.847 | −0.002 / **0.215** / 1.450 | **$7.25** | stacked arms, not an interval |
| Restaurant variety: cuisine composition | −15.37 / **−0.61** / 4.67 | same as absolute | −$14.97 | modelled; sign uncertain |
| Restaurant variety: market size (generic) | −19.22 / **−6.79** / −1.07 | 0.19 / **1.20** / 3.39 | −$166.10 | modelled; any 40.9m residents supply it |
| Food prices | 0 (already in the account) | 0 | — | cross-check only |
| Produce quality, farm labour | 0 | 0 | — | no evidence found |
| *Fiscal, not social:* TB-control key correction | 0.023 / 0.068 / 0.119 (group's share) | 0.007 / **0.019** / 0.034 | $1.66 | measured case share × assumed spending |

[CALCULATION: `derived/items.csv`, `derived/totals.csv`, `derived/tb_detail.csv`; every parameter with its tag in
`derived/inputs.csv`]

Scale: the adopted main case is $322–387bn a year [SOURCE: repo CLAUDE.md, decision 2026-09-27]; the crime
victims' full cost is $29bn [SOURCE: `crime_victim_cost_2026_09_23/RESULT.md`]; the four unpriced social items
net to $8bn [SOURCE: `social_costs_unpriced_2026_09_28/RESULT.md`]. Disease plus food safety at $0.30bn is under
0.1% of the main case [CALCULATION].

## Method, with sources

**Population.** Union 40,896,574; CPS civilian total 336,727,803; population share 12.15%
[DATA: `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv`]. VSL $13.7m (US DOT 2024, as in the
crime lane). VSLY $592,695 = VSL over a 40-year annuity at 3% [CALCULATION]. CPI-U annual averages 2014 236.736,
2020 258.811, 2023 304.702, 2024 313.689 (BLS CUUR0000SA0; the 2024 value is gated in the crime lane)
[TRAINING-DATA for 2014/2020/2023].

### 1. Tuberculosis

*Cases.* 2024: 10,388 cases; Mexico-born 1,307 (16.3% of the 8,016 non-US-born); US-born Hispanic 663 at 1.6 per
100,000 [SOURCE: CDC, Reported TB in the US 2024, tables origin-birth, top-30-birth-countries,
race-ethnicity-us-born]. The Mexican-origin share of US-born Hispanic cases is taken as the population share,
0.692 = CPS US-born Mexican-origin (28.7m) / the 41.4m US-born Hispanics implied by 663 cases at 1.6 per 100,000
[CALCULATION]; range 0.60–0.80 [INFERENCE]. Group cases: 1,766 (1,705–1,837), a rate of 4.3 per 100,000 against
3.1 nationally; the group has 17.0% of cases [CALCULATION: `derived/tb_detail.csv`].

*Latent infection and screening (context, not priced).* NHANES 2011–12: IGRA positivity 15.9% (13.5–18.7) among
the foreign-born and 2.8% among the US-born; TST positivity 20.3% among foreign-born Hispanics
[SOURCE: Miramontes et al. 2015, PLoS One 10(11):e0140881]. Applied to about 11m Mexico-born, that is on the order of
1.7–2.2m infected [CALCULATION, order of magnitude]. Culture-based overseas screening (since 2007) covers
immigrant-visa applicants and refugees only; in 2007–11 just 23.7% of new entrants from Mexico passed through it,
against 51.7% from the Philippines and 72.6% from Vietnam, because most Mexican entrants arrive on temporary visas or
without one [SOURCE: Baker et al. 2016, PLoS One 11(2):e0147353]. Screening fees are paid by applicants, so they are
not a cost to others [INFERENCE].

*Secondary cases.* Under the plausible-source-case method (2011–Sep 2014, 26,586 genotyped cases), 14% of cases
were attributed to recent transmission: 7.5% of foreign-born cases and 27.4% of US-born; Hispanic 13.6%; foreign
birth aPR 0.4 (limited) and 0.2 (extensive recent transmission) [SOURCE: Yuen et al. 2016, PLoS One 11(4):e0153728,
Tables 1–3]. Among recent entrants only 1.7–2.2% of cases were due to transmission from a recent-entrant source
[SOURCE: Baker et al. 2016]. The lane uses each subgroup's recent-transmission share as the yield of secondary cases
per source case, which assumes transmission is assortative: Mexico-born 0.054 / 0.075 / 0.136, US-born Hispanic
0.150 / 0.274 / 0.274 → 224 secondary cases a year (130–323). The share landing outside the group is **assumed**,
0.10 / 0.20 / 0.35 [INFERENCE]; mixed clusters exist (Massachusetts: 67 of 152 clustered patients in mixed
US-/foreign-born clusters [SOURCE: EID 8(11), 02-0370]; Rhode Island: 8 of 10 mixed clusters had a foreign-born
source [SOURCE: JCM 10.1128/jcm.01952-10]), but none of these studies splits sources by Mexican origin. Later
reactivation among infected outsiders adds 0.10 / 0.25 / 0.50 per recent case (most progression occurs within two
years of infection; Behr et al. 2018 BMJ [TRAINING-DATA]). Central: **56 outside cases a year**, of which 45 recent;
that is 4.4% of the roughly 1,007 recent-transmission cases a year among non-group residents
(1,635 US-born non-Hispanic × 27.4% + 6,709 other non-US-born × 7.5% + 206 other US-born Hispanic × 27.4%)
[CALCULATION].

*Cost per case.* Direct medical $20,000 drug-susceptible and $182,000 MDR (CDC, 2020 $) [SOURCE: CDC, "The Costly
Burden of Drug-Resistant TB Disease in the U.S.", stacks.cdc.gov/view/cdc/154504], MDR share 0 / 1.5% / 3%
[INFERENCE], CPI to 2024; non-fatal productivity $3,000 (2014 $) = societal-excluding-death $20,000 minus direct
$17,000 [SOURCE: Castro et al. 2016, IJTLD, stacks.cdc.gov/view/cdc/42149]; quality-of-life loss of survivors 0.10 /
0.25 / 0.50 QALY × VSLY [INFERENCE; post-TB sequelae per Menzies et al. 2021 Lancet Glob Health, TRAINING-DATA];
TB-attributable case fatality 0.03 / 0.05 / 0.065 × VSL (Castro: 6.48% = 72% of deaths due to TB × 9% dying;
secondary cases are younger, hence lower central) [SOURCE + INFERENCE]. Central $857,000 per case, of which the
statistical life is 80% [CALCULATION].

*Normalized.* Same mixing; the group's per-head source intensity (secondary cases per head, 5.5 per million)
against the average resident's (10,388 × 0.14 / 336.7m = 4.3 per million): factor 0.21. In the low arm the group's
intensity is below average and the normalized figure turns negative [CALCULATION].

*Candidate key correction (fiscal).* CDC's domestic TB appropriation is about $135m [SOURCE: CDC budget line
FY2019–21, via Gile 2020 thesis table]; national contact investigations cost $9.94m in 2022 [SOURCE: systematic review,
PMC12205448]; total public TB-control spending 0.135 / 0.40 / 0.70 $bn [INFERENCE]. With 17.0% of cases against a
12.15% population share, a per-head public-health key under-charges the group by $0.019bn ($0.007–0.034bn). The
group's own TB treatment is medical spending already in the account's medical keys. Whether the account keys
non-medical public-health spending per head was not verified here: its capital components key health structures by
health-services use (key 0.0566) [DATA: `main_case_long_run_2026_09_27/derived/corrections.json`] [GAP].

### 2. Measles, hepatitis A, Chagas, neurocysticercosis

- **Measles.** Jan–Apr 2025: 7 of 48 importations came from Mexico, 15 of 48 importations produced secondary cases;
  the 2025 Chihuahua outbreak began after a Mexican resident travelled to Gaines County, Texas (spread ran US →
  Mexico); the D8 lineage is MVs/Ontario.CAN/47.24 [SOURCE: MMWR 74(14); Yale VMOC special report 2025-06-06].
  Priced as importations 2 / 5 / 20 a year × 0.31 × 1–5 secondary cases × 0.2–0.5 outside × $30–80k: under
  $0.001bn [CALCULATION]. Outbreak response is public-health (fiscal) spending.
- **Hepatitis A.** 2023: travel was the most common risk, 21% of the 748 cases with travel information
  [SOURCE: CDC Surveillance Manual ch. 3]; historically 81–85% of travel-linked cases involved Mexico or
  Central/South America [SOURCE: CDC MMWR SS 2005, 2007]. Travel cases 157–350 × Mexico 0.3–0.7 × group 0.4–0.8 ×
  0.02–0.10 non-group secondary cases × $30–120k: under $0.003bn [CALCULATION + INFERENCE]. Outbreaks from imported
  Mexican produce (green onions 2003, strawberries 2022) are a trade channel, not residents, and are excluded.
- **Chagas.** Custer et al. (3 years, 1.18m donors): confirmed seropositive donors were born in Mexico (32 of 89,
  prevalence 1:800), Central/South America (23, 1:200) and the US (25) [SOURCE: Custer et al., Transfusion 52(9), 2012];
  seven transfusion cases were ever documented in the US and Canada [SOURCE: FDA 2017 guidance]. US donors are tested
  once; 9.1m first-time donations were screened in 2007–15 in the ARC-led study [SOURCE: Transfusion 2019,
  doi:10.1111/trf.15118]. Tests 1.5 / 2.0 / 2.5m a year × $4 / 7 / 10 × attribution 0 / 0.5 / 1 (0 if screening would
  exist for other Latin American donors anyway) = $0–0.025bn [INFERENCE]. Normalized × (1 − 0.1215 / 0.5).
- **Neurocysticercosis.** 18,584 hospitalizations in 2003–12, mean charge $48,900, three quarters Hispanic, Hispanic
  rate 2.5 against 0.65 per 100,000 overall [SOURCE: EID 21(6), 2015]; 1,320–5,050 new cases a year [SOURCE:
  PMC4005108]; 7% locally acquired in Los Angeles (10 of 138), 30% of those non-Hispanic; carriers found among
  household contacts, and the 1990–91 New York cluster traced to Latin American housekeepers [SOURCE: PMC3298370].
  Cases × 0.05–0.10 local × 0.3 non-Hispanic × 0.4–0.7 group carrier × $100–500k = $0.001–0.053bn [CALCULATION].

### 3. Food safety

Burden: $74.7bn (2023 $) for all foodborne illness, 47.8m cases, deaths 56% of cost [SOURCE: USDA ERS 2025 update;
Hoffmann et al. 2025, Foodborne Pathog Dis 22(1):4–14] → $76.9bn in 2024 $. Restaurants: 9,788 outbreaks in 1998–2013,
56% of all outbreaks, food workers implicated in 24%, norovirus 46% of confirmed-aetiology outbreaks; cuisine and
ownership are not recorded [SOURCE: Angelo et al. 2017, Epidemiol Infect 145(3):523]. Restaurant share of the illness
burden 0.25 / 0.40 / 0.55 [INFERENCE]; non-group diners 0.90 [INFERENCE]; group share of kitchen labour 0.12 / 0.169 /
0.205 [DATA: `cultural_output_2026_09_19/derived/arm_d_cooks_shares.csv`: 16.9% of all food preparation and serving
workers, 20.5% of chefs and cooks]; excess illness risk in group-staffed kitchens 0 / 0.05 / 0.20 [INFERENCE: 0 =
Jones et al. 2004 null; 0.20 = the whole Los Angeles grade-card effect, −20% foodborne hospitalizations (Jin & Leslie
2003) or −13.1% (Simon et al. 2005)]. Normalized = absolute × (1 − 0.169): the excess over the average kitchen, which
already includes the group's labour. Violation evidence: Kansas ethnic independents 4.52 vs 2.90 critical violations
per inspection [SOURCE: Kwon et al. 2010, Food Prot Trends]; Louisiana OR 1.74 [SOURCE: abstract only, UNVERIFIED].

### 4. Variety

*Composition (group-specific).* Nested CES, Cobb–Douglas across cuisine nests, CES within (σ = 8.8 from Couture;
6.1–8.7 in Su's replication [SOURCE: Su, MPRA 113158, quoting Couture 2016]). Mexican restaurants 12.75 per 100,000,
all restaurants 114.8 per 100,000 (population-weighted OSM counts in the 573 fully covered CBSAs) [DATA:
`cultural_output_2026_09_19/derived/arm_d_share_deciles.csv`]. Without the group: 4.0 per 100,000 (2.0 if the national
Mexican-origin cook supply also goes; 6.93 = the lowest-share decile) [INFERENCE]. Total restaurants per head held
fixed, because in the cultural lane restaurant counts overall do not rise with the Mexican-origin share (placebo);
other cuisines take the freed places. Non-group consumers' Mexican share of restaurant spending 0.05 / 0.07 / 0.09
[INFERENCE]. Spending base: 90% of NAICS 722 sales of $1,144bn [SOURCE: Census advance monthly retail, 2024 total
$1,144,365m; BLS sectoral output $1,143,983m] or 90% of CEX food away from home ($3,944.94 per consumer unit
[SOURCE: consumer-price memo, BLS CEX 2024] × 134.6m units [TRAINING-DATA]). Central benefit $0.61bn; the 72-cell
grid spans a $4.67bn cost to a $15.37bn benefit. The sign flips because non-group diners who spend less than the
Mexican restaurant share (11%) on Mexican food lose more from the crowded-out cuisines than they gain [CALCULATION].
Normalized = absolute: average residents would bring the average cuisine mix.

*Market size (generic).* Removing the group's restaurant demand removes the restaurants it supports; non-group diners
lose access share ψ = 0.02 / 0.05 / 0.09 (group spending share 0.10 discounted for segregated consumption)
[INFERENCE]; loss = E × ((1 − ψ)^(−1/(σ−1)) − 1) = $1.1 / 6.8 / 19.2bn [CALCULATION]. Couture's own aggregate gain from
restaurant variety beyond the nearest restaurant is $80–160bn a year (c. 2009 $), so $6.8bn is 4–9% of that total
[SOURCE: Couture thesis ch. 1]. Normalized: 40.9m average residents would spend more on restaurants (group spending
share 0.10 against population share 0.1215 [INFERENCE, UNVERIFIED]), so against them the group is a relative cost of
$1.2bn [CALCULATION].

*Retail.* Mazzolari & Neumark: +1% foreign-born share → +0.18% (shopping area) / +0.44% (commuting area) in the
ethnic-restaurant share, via immigrants' comparative advantage in producing ethnic food; but +10% foreign-born share →
−4% small retail stores and more big-box stores, which they read as less retail diversity [SOURCE: J Popul Econ
25:1107–1137, 2012]. The retail effect is negative in variety and positive in price; it is not priced here.

### 5. Prices and produce quality

Prices are already in the consumer-price channel: its broad scope A covers food away from home
($30.04 / 21.30 / 14.61bn in that memo's table) [SOURCE: `research/immigration-consumer-price-and-native-hours-2026-09-18.md`],
and the production term covers farm output. Nothing is added. No study located links farm-labour supply to produce
quality; the Bracero exclusion moved crop mix and mechanisation without raising native wages (Clemens, Lewis &
Postel 2018 AER) [TRAINING-DATA] → 0.

## Disconfirmation

- **TB, cost hypothesis ("immigrant TB spreads to natives").** Steel-man: the group has 17% of US cases, Mexico is
  the top birth country every year, the latent reservoir is large, only a quarter of Mexican entrants pass overseas
  culture screening, and mixed clusters are common in state studies. Against it: foreign-born cases are rarely
  recent transmission (7.5%), extensive transmission concentrates in US-born Black, American Indian, Pacific
  Islander and homeless networks (CDC-investigated outbreaks 2002–08: 91% US-born, 67% non-Hispanic Black)
  [SOURCE: Yuen 2016], and transmission from recent entrants accounts for 1.7–2.2% of their own cases
  [SOURCE: Baker 2016]. The high arm (35% outside, Hispanic-level yield for the Mexico-born) still gives $0.20bn.
  To reach $1bn the outside share would need to exceed 100% at central yields, so the conclusion that TB is
  immaterial survives every arm [CALCULATION].
- **TB, the opposite hypothesis ("zero").** Mixed clusters exist, and 80% of Rhode Island's mixed clusters had a
  foreign-born source, so the outside share is not zero. The low arm keeps 10%.
- **Food safety.** Steel-man: independent ethnic restaurants carry 1.56–1.74 times the critical violations, food
  workers cause a quarter of restaurant outbreaks, and paid sick leave is rare in the industry. Against it: inspection
  scores of outbreak restaurants did not differ from others in Tennessee [SOURCE: Jones 2004]; inspector means ranged
  from 69 to 92 on the same form, and King County shows inspector-specific differential scoring by cuisine
  [SOURCE: Ho, dho.stanford.edu draft]; in New York the early-2020 citation spike hit Asian restaurants while Mexican
  ones fell 0.69% below their synthetic control [SOURCE: PMC9713539]; "ethnic" in the violation studies pools Mexican with Asian, Italian and other cuisines, and chain restaurants,
  which employ much of the group's kitchen labour [INFERENCE], score better than independents [SOURCE: Roberts et al. 2011, K-State]. Hence the
  zero low arm and the speculative label.
- **Variety, benefit hypothesis.** Steel-man: Couture values restaurant variety at $80–160bn a year, Mexican is one
  of the two largest ethnic cuisines, and Mazzolari–Neumark show immigrants raise ethnic-restaurant diversity through
  supply. Against it: the cultural lane found saturation (elasticity 0.18; 95% of the lowest-share metros already have
  a Mexican restaurant), restaurant totals per head do not rise with the group's share, and Mazzolari–Neumark find less
  retail diversity. With crowd-out counted, the composition gain is small and of uncertain sign. The large market-size
  figure is generic scale, not a property of this group.
- **COVID-19, cost hypothesis.** Steel-man: livestock plants, with heavily Hispanic and immigrant workforces, were
  associated with 236,000–310,000 cases and 4,300–5,200 deaths by July 2020 (Taylor, Boulos & Almond 2020 PNAS)
  [TRAINING-DATA]. Against it: that is a plant and occupation effect, and replacement workers in the same plants would
  have faced the same conditions; the group bore its own excess mortality; epidemic final size depends on contact
  structure that no study splits by origin. Bound only: about 954,000 US COVID deaths in 2020–22 (NCHS data briefs
  427/456/492) and about 82% non-Hispanic [TRAINING-DATA] → each 1% of others' deaths ≈ 7,800 deaths ≈ $107bn
  one-off [CALCULATION]. A bound this wide with unknown sign is not a price. [GAP]
- **Measles.** Steel-man: Mexico reported about 2,080 confirmed and an estimated 4,400 probable cases by June 2025, mostly in
  Chihuahua, across an open border [SOURCE: Yale VMOC special report 2025-06-06]. Against it: the
  spread ran from Texas to Chihuahua, the lineage came via Canada, and only 7 of 48 importations came from Mexico.
- **Instrument.** This lane was produced by an LLM (`notes/llm-bias-caveat.md`). The load-bearing inputs are CDC
  counts and published parameters; every assumed share sits in `derived/inputs.csv` for audit.

## Double counting

| Item | Overlaps with | Treatment |
|---|---|---|
| TB, Chagas, NCC, hepatitis A | Account's medical keys (the group's own treatment) | Only harm to non-group residents is priced; the group's own care is not added |
| TB control, measles response | Account's public-health spending | Reported as a candidate key correction (fiscal), not a social item |
| Food safety | Hepatitis A (handler cases); account medical keys | Illness among non-group diners is borne by them; hepatitis A handler cases are negligible either way |
| Variety, composition | Consumer-price channel; cultural output lane | Prices ≠ product range; the cultural lane measured density but priced no dollar line |
| Variety, market size | `scale_spillovers_2026_09_23` (production side, no variety line found by grep); `congestion_2026_09_23` (cost side of density) | Keep beside scale, not beside the group-specific items |
| Food prices, produce | Consumer-price channel; production term | Not added |
| Crime, fear, security, schools, road crashes, air pollution | — | No overlap |

## What can be added beside the account

[2026-09-28, later: the operator added item 4, restaurant market size ($6.8bn benefit, $1.1–19.2bn), to the social rows of the fiscal-plus-social total with the scale lane's net, as the counterpart of the scale costs there; the normalized figure sits beside. The other items stay beside ([decision](../../../decisions/2026-09-28-social-items-scale-benefits.md)).]

1. **Disease (TB, Chagas, neurocysticercosis, hepatitis A, measles):** $0.06bn absolute ($0.01–0.29bn), $0.02bn
   normalized. It can enter as one line; it moves nothing.
2. **Food safety:** $0.23bn central is an assumption-driven figure; enter it only as a flagged arm ($0–1.6bn).
3. **Variety, composition:** a benefit of $0.6bn with uncertain sign; report beside the costs as a benefit line with
   its envelope.
4. **Variety, market size:** a $6.8bn benefit in the absolute frame, which belongs with the scale lane because any
   40.9m residents would supply it; normalized, it is a $1.2bn relative cost.
5. **TB control:** +$0.02bn fiscal key correction if the account keys public-health spending per head.
6. **COVID-19:** not priced; see the bound.

## Files covered and skipped

Covered: `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv` and `RESULT.md` (population, VSL,
conventions); `decisions/2026-09-23-evidence-symmetry-rules.md`; `cultural_output_2026_09_19/derived/`
`arm_d_share_deciles.csv`, `arm_d_cooks_shares.csv`, `arm_d_summary.json`, `arm_d_predicted_density.csv` and the
memo's verdict; `research/immigration-consumer-price-and-native-hours-2026-09-18.md` (food-away-from-home rows);
`vending_restaurants_2026_09_24/RESULT.md` (verdict); `social_costs_unpriced_2026_09_28/` (verdict, CSV format);
`main_case_long_run_2026_09_27/derived/corrections.json`, `summary.json` (health keys, by search);
`scale_spillovers_2026_09_23/RESULT.md` (searched for variety; none).

Skipped, with reasons: the main-case engine (`main_case.cjs`, `package.cjs`), because the per-head public-health
key question needs its owner and does not change a $0.02bn line; NORS microdata, because it records setting but not
cuisine or ownership, and Angelo 2017 summarises 1998–2013; CDC state tables by ethnicity and origin, which a
state-level disconfirmation would need (listed below); Couture's published paper (σ taken from Su's replication text);
the Louisiana violation study beyond its abstract.

## Gaps and next queries

- [GAP] The outside share of TB transmission from Mexican-origin sources is assumed. Test: CDC TB GIMS/NTGS cluster
  composition (US-born non-Hispanic cases in clusters with a Mexico-born member), or border-state WGS studies; a state
  panel of US-born non-Hispanic incidence against Mexico-born share.
- [GAP] Food safety: NYC DOHMH or LA County inspection microdata with cuisine and inspector fixed effects, linked to
  reported outbreaks; no owner-ethnicity field exists in NORS.
- [GAP] Group restaurant spending share (CEX by Hispanic origin) and non-group Mexican spending share: both assumed.
- [GAP] Measles immunity by ethnicity (NIS-Child, kindergarten exemptions) for the sign of the measles item.
- [GAP] COVID-19: county studies of Hispanic share and non-Hispanic mortality with occupation controls.
- [GAP] Whether the account keys non-medical public-health spending per head.

## Log (append-only, times from `date`)

### 21:01 JST — TB inputs verified so far (append-only)
- Mexico-born TB cases: 1,263 (2023), 1,161 (2022), 1,052 (2021), 925 (2020), 1,188 (2019); 17.3% of the
  7,299 non-US-born cases in 2023. [SOURCE: CDC Reported TB in the US 2023, Table 10, https://www.cdc.gov/tb-surveillance-report-2023/tables/table-10.html]
- All cases 2023: 9,633; US-born 2,292 (23.8%); non-US-born 7,299 (75.8%). [SOURCE: same report, Table 30]
- Non-US-born Hispanic cases 2,876 in 2023 (rate 12.9/100k). [SOURCE: MMWR 73(12) Table 2, https://www.cdc.gov/mmwr/volumes/73/wr/mm7312a4.htm]
- Cost per case, CDC 2020 $: drug-susceptible direct $20,000 + productivity (incl. deaths) $47,000 = $67,000;
  MDR $182,000 + $238,000 = $420,000; XDR $568,000 + $233,000 = $801,000.
  [SOURCE: CDC "The Costly Burden of Drug-Resistant TB Disease in the U.S.", https://stacks.cdc.gov/view/cdc/154504/cdc_154504_DS1.pdf]
  Castro et al. 2016 (IJTLD, 2014 $): non-MDR direct $17,000; societal excl. premature-death productivity $20,000;
  incl. it $44,000; TB-caused death share 6.48% (= 72% of deaths are due to TB × 9% die).
  [SOURCE: https://stacks.cdc.gov/view/cdc/42149/cdc_42149_DS1.pdf]
- Cross-origin transmission (genotype studies): Massachusetts 1996–2000, 67 of 152 clustered patients in mixed
  US-/foreign-born clusters, 29 of them US-born [SOURCE: EID 8(11) 02-0370]; Rhode Island, 8 of 10 mixed clusters had a
  foreign-born source [SOURCE: J Clin Microbiol 10.1128/jcm.01952-10]; Florida, 21.5% of US-born vs 4.6% of foreign-born
  cases in space-time genotype clusters [SOURCE: PLoS One 10.1371/journal.pone.0153575]. None splits sources by Mexican origin.
- [GAP] 2024 counts; US-born Hispanic cases; national recent-transmission share by origin; a study giving the share of
  US-born non-Hispanic cases whose source was Mexico-born or Mexican-origin.

### 21:26 JST — further inputs verified (append-only)
- TB 2024 (final): 10,388 cases; US-born 2,298, non-US-born 8,016 (rate 15.7 vs 0.8/100k); Mexico-born 1,307
  (16.3% of non-US-born); US-born Hispanic 663 (rate 1.6); US-born Black 769, white 513, AIAN 110, Asian 105, NHPI 85.
  [SOURCE: CDC TB in the US 2024, tables origin-birth, top-30-birth-countries, race-ethnicity-us-born,
  https://www.cdc.gov/tb-surveillance-report-2024/data/]
- Recent transmission (plausible-source-case method, 2011–Sep 2014, 26,586 genotyped cases): 14% of cases; 7.5% of
  foreign-born cases (1,298/17,363) vs 27.4% of US-born (2,522/9,199); Hispanic 13.6%. Foreign birth aPR 0.4 (limited)
  and 0.2 (extensive recent transmission). CDC-investigated outbreaks 2002–08: 91% of patients US-born, 67% non-Hispanic
  Black. [SOURCE: Yuen et al. 2016, PLoS One 11(4):e0153728, Tables 1–3]
- Foodborne illness burden: $74.7bn (2023 $), 47.8m cases; deaths 56% of cost (WTP/VSL per EPA guidance).
  [SOURCE: USDA ERS Cost Estimates of Foodborne Illnesses (2025 update, Hoffmann et al. 2025 FPD 22(1):4–14),
  https://www.ers.usda.gov/data-products/cost-estimates-of-foodborne-illnesses]
- Restaurant outbreaks 1998–2013: 9,788 (56% of all outbreaks), 124,608 illnesses, 32 deaths; food workers implicated in
  24%; norovirus 46% of confirmed-aetiology outbreaks. Cuisine is not reported. [SOURCE: Angelo et al. 2017,
  Epidemiol Infect 145(3):523–534, doi:10.1017/S0950268816002314]
- Inspections vs illness: Tennessee 1993–2000 — outbreak restaurants' prior scores (81.2) did not differ from all
  restaurants; inspector means ranged 69–92 [SOURCE: Jones et al. 2004, EID 10(4):688]. LA grade cards (1998) → −20%
  foodborne hospitalizations [SOURCE: Jin & Leslie 2003 QJE 118(2), via Choices 2005 summary]; −13.1% with a refined
  definition [SOURCE: Simon et al. 2005, J Environ Health 67(7)].
- Ethnic-restaurant violations: Kansas, 500 independents — critical 4.52 vs 2.90 per inspection (×1.56)
  [SOURCE: Kwon et al. 2010, Food Prot Trends, https://www.foodprotection.org/files/food-protection-trends/Jul-10-Kwon.pdf];
  Louisiana OR 1.74 for critical violations [SOURCE: exa.ai/library v8vvyjjjq72, abstract only — UNVERIFIED full text].
  Inspector heterogeneity/DIF against Asian establishments, King County [SOURCE: Ho, UC Irvine L Rev draft,
  dho.stanford.edu]; NYC early-2020 citations rose for Asian but fell 0.69% vs synthetic for Mexican restaurants
  [SOURCE: PMC9713539].
- Variety: Couture (restaurant logit/CES) σ ≈ 8.8; replications 6.1–8.7 [SOURCE: Su, MPRA 113158]; aggregate gains
  from restaurant variety beyond the nearest option $80–160bn/yr (~2009 $) [SOURCE: Couture thesis ch.1,
  utoronto.scholaris.ca]. Mazzolari & Neumark 2012: +1% foreign-born share → +0.18% (shopping area) / +0.44%
  (commuting area) ethnic-restaurant share; +10% foreign-born share → −4% small retail stores, more big-box
  [SOURCE: J Popul Econ 25:1107–1137, NBER w14900].
- Measles: Jan–Apr 2025, 7 of 48 importations from Mexico; Chihuahua outbreak seeded FROM Gaines County TX; lineage
  MVs/Ontario.CAN/47.24 [SOURCE: MMWR 74(14); Yale VMOC special report 2025-06-06].
- [GAP] account's public-health key; TB control spending; Chagas screening volume/cost; hep A travel share; NCC.

### 21:36 JST — priced and written (append-only)
- `price_items.py` run from the repo root, rc 0; rerun byte-identical (md5 of `derived/items.csv`); no CR bytes.
- Added after the 21:26 JST inputs: LTBI (NHANES 2011–12 foreign-born IGRA 15.9%, TST 20.5%; foreign-born Hispanic TST
  20.3%) [SOURCE: Miramontes et al. 2015, PLoS One 10(11):e0140881]; overseas culture screening reached 23.7% of new
  entrants from Mexico in 2007–11; 1.7–2.2% of recent entrants' cases came from recent-entrant sources [SOURCE: Baker
  et al. 2016, PLoS One 11(2):e0147353]; neurocysticercosis counts [SOURCE: EID 21(6) 2015; PMC4005108; PMC3298370];
  hepatitis A travel share [SOURCE: CDC Surveillance Manual ch. 3]; CDC domestic TB $135m; contact investigations
  $9.94m (2022) [SOURCE: PMC12205448]; NAICS 722 2024 sales $1,144.4bn [SOURCE: Census advance monthly retail].
- Verdict, table and sections above replace the stub. Remaining gaps are listed under "Gaps and next queries".
- 2026-09-28 23:04 JST (lead): the operator added restaurant market size (item 4) to the social rows with the scale lane's net (decision 2026-09-28-social-items-scale-benefits); lane outputs unchanged.
