**Verdict:** The Mexican-origin union's trade, visitor and investment ties with Mexico are worth about **$6.8bn a year to other US residents** ($1.1–23.7bn), a benefit, so **−$6.8bn** as a cost; that is $166 per member. The trade channel carries almost all of it: $6.2bn ($0.9–22.2bn), all from the Mexico-born in the low and central arms. Visits from relatives in Mexico add $0.47bn ($0.21–0.80bn) and investment returns add $0.11bn ($0–0.79bn). The central assumes the network creates **$72.9bn of US–Mexico trade**, and only 8.5% of that volume is a welfare gain. It equals 6.6% of what all US–Mexico trade is worth to other residents in the same model ($94bn at ε = 5). Against 40.9m average residents, whose ties spread over every trading partner, the benefit disappears: the normalized figure is a **small relative cost of $0.8bn** ($0.25–2.7bn). The absolute figure is not identified in the literature. Every published estimate is marginal, and Gould's saturation curve puts the Mexico-born stock about 800 times past the point where 90% of the export effect is used up. The central therefore stretches the one Mexico-specific estimate (US-state × Mexican-state exports, elasticity 0.086) across the whole stock. [CALCULATION: `price_trade_networks.py` → `derived/items.csv`, `derived/summary.json`] [FRAMING-SENSITIVE: the network share s of trade, the trade elasticity, and the rule for average residents]
claude-opus-5-5

# Trade, investment and travel networks of the Mexican-origin union, priced as a benefit to other US residents

Lane: `infra/immigration-fiscal/trade_networks_2026_09_28/` (analysis only; the parent commits).
Frame: the adopted September 27 main case. It compares 2024 with and without the 40.9m CPS 2025
Mexican-origin residents (the union) and counts effects on all other US residents. A benefit is a
negative cost. All figures are $bn a year at 2024 prices.

## Verdict table

| Item ($bn a year; negative = benefit) | Group | Absolute low / central / high | Normalized low / central / high | Per member (abs., central) | Evidence |
|---|---|---|---|---|---|
| Trade, information channel | Mexico-born | −0.92 / −6.20 / −14.93 | — | −$151 | modelled from marginal elasticities |
| Trade, information channel | US-born descendants | 0 / 0 / −7.23 | — | $0 | high arm only (per-head weight 0.2) |
| **Trade, information channel** | **union** | **−0.92 / −6.20 / −22.16** | **+0.08 / +0.46 / +1.08** | −$151 | as above |
| Trade, preference channel (the group's own demand for Mexican goods) | union | 0 / 0 / 0 | — | $0 | not a gain to others |
| Visitors from Mexico visiting friends and relatives (VFR) | union | −0.21 / −0.47 / −0.80 | +0.17 / +0.11 / +0.05 | −$11 | measured spending, assumed shares |
| FDI excess return | union | 0 / −0.11 / −0.79 | 0 / +0.21 / +1.60 | −$3 | speculative |
| **Total** | **union** | **−1.14 / −6.77 / −23.75** | **+0.25 / +0.78 / +2.73** | **−$166** | stacked arms |

Per member = central ÷ 40,896,574 union members, for every row, so rows add. The arms are stacked:
low with low and high with high. The normalized figures are a relative cost in every arm.
[CALCULATION: `derived/items.csv`]

## Method

**What is priced.** The union's ties are treated as a cut in US–Mexico trade costs for other
residents: information, contacts, language and trust. Welfare is the gain from trade, never trade
volume. The group's own taste for Mexican goods is excluded (the preference channel). In the
counterfactual those imports leave with the group, and no other resident loses from that.

**Welfare model.** There are three regions: the US, Mexico and the rest of the world (ROW). The
model is one-sector Armington/ACR, solved in exact hat algebra with fixed nominal deficits (Dekle,
Eaton & Kortum 2008; Arkolakis, Costinot & Rodríguez-Clare 2012) [SOURCE: the brief's method;
[TRAINING-DATA] citations].
- Removing the network raises the cost of both US–Mexico flows, excluding travel. The raise is set so
  that, at fixed prices, each flow falls by the network share s.
- The US welfare change is the change in real expenditure. It includes trade diversion across
  suppliers and terms-of-trade effects.
- The calibration uses the 2024 flows below [CALCULATION: `derived/summary.json` → `calibration`]:
  - US–Mexico: US exports $384.9bn and imports $548.2bn, goods plus services.
  - US GDP $29,298bn, US exports $3,215bn, US imports $4,114bn.
  - Mexico GDP $1,830bn, Mexico exports $682bn, Mexico imports $698bn.
  - ROW is world GDP less the two.
- Mexico supplies 1.82% of US spending; the US domestic share λ is 0.864.
- The trade elasticity ε is 8, 5 and 4 in the low, central and high arms (the brief's 4–8 range).
- The gain is multiplied by other residents' share, 1 − 0.0889 = 0.911. Here 0.0889 is the union's
  share of the consumption key, `saving_central`
  [DATA: `consumption_key_2026_09_24/derived/key_specs.csv`] [INFERENCE: gains split like consumption].

**Network share s (the crux).**

| Arm | s, Mexico-born | Descendants | s, union | Basis |
|---|---:|---|---:|---|
| Low | 0.020 | 0 | 0.020 | [INFERENCE] Mexico is saturated (Gould) and substitute networks remain, e.g. 28.1m non-union Hispanic residents |
| Central | 0.082 = 1 − e^(−0.086) | 0 | 0.082 | Gove (2017) Mexico-specific elasticity 0.086 (SE 0.039), applied linearly to the whole stock |
| High | 0.156 = 1 − e^(−0.17) | weight 0.2 per head | 0.230 | meta-analysis mean elasticity 0.17 (Genc et al.); descendants in the spirit of Burchardi–Chaney–Hassan |

- **Low arm.** The substitute networks are the non-union Hispanic residents: 68.4m CPS Hispanic
  civilians less 40.3m Hispanic union members [DATA: `target_population_cps2025.csv`].
- **Central arm.** Linearising a marginal elasticity understates the effect if the network effect is
  concave with no substitute network. It overstates it if other networks would supply the
  information, or if state-pair effects partly move trade between states.
- **Grid.** `derived/grid.csv` crosses s with ε. At s = 0.082 the gain is $3.8bn (ε 8), $6.2bn
  (ε 5) and $7.8bn (ε 4).

**Cross-check.** The partial-equilibrium, import-side-only ACR gain is s × M / ε. Centrally that is
$7.84bn against the GE result of $6.20bn. The GE is lower because the network cuts US imports ($43bn)
by more than US exports ($30bn). With the deficit fixed, the US wage rises and the terms of trade
improve, offsetting part of the loss. [CALCULATION: `summary.json` `pe_import_side_check`]

**Visitors (VFR).** In 2024 Mexican residents spent $22.2bn on travel in the US.
- About 21.5% of Mexican visitors travel mainly to visit friends and relatives: 21.3% of 13.4m land
  visitors and 21.7% of 3.5m air visitors [SOURCE: NTTO 2024 land report; SIAT 2024].
- VFR spending = the VFR share (0.15 / 0.215 / 0.25) × the share attributed to the union
  (0.8 / 0.9 / 1.0) × $22.2bn. That is $2.7 / $4.3 / $5.6bn [INFERENCE: spending shares assumed equal
  to or below trip shares].
- The gain has two parts:
  - the GE terms-of-trade gain on these exports;
  - the sales tax paid by foreign visitors, a transfer to US governments. The rate is general sales
    tax ÷ PCE = 602.43 ÷ 19,896 = 3.0%, or 4.9% in the high arm with selective excise
    [DATA: `consumption_key_2026_09_24/RESULT.md` national lines; BEA DPCERC].
- The group's own trips to Mexico are its own consumption and are excluded.

**FDI.** The US direct investment position in Mexico is $155.9bn, of which $15.3bn is in holding
companies. The priced base is the $140.6bn outside them [SOURCE: BEA usdia detailed-country and
country-by-industry xlsx, 2024].
- Network-created share: 0, 0.082 and 0.307. The 0.307 comes from Burchardi–Chaney–Hassan's +29% jobs
  per doubling of ancestry, an elasticity of 0.367.
- The gain counts only the excess return over the next-best use: 0, 1 and 2 percentage points
  [INFERENCE].
- BEA's 2024 returns cap the excess return: 9.0% on outward and 5.6% on inward direct investment
  [SOURCE: BEA SCB, September 2025]. Mexico's 2024 income was $16.0bn [SOURCE: BEA].

**Normalized rule.** 40.9m average residents carry φ = 40.9 / 336.7 = 12.15% of every origin's
network, the group's own included. The rule applies the same s and ε to US trade with every
partner. It gives:
- trade: 12.15% of s on all non-travel US trade;
- VFR: 12.15% of the 0.229 VFR share of all $215.0bn of US travel exports
  [SOURCE: BEA ITA Table 3; SIAT 2024];
- FDI: 12.15% of the $3,504.9bn outward position outside holding companies.

Normalized = absolute − average. The rule is proportional: every origin's network creates the same
share s. A per-head rule would give the group's 12.2m Mexico-born more weight than the foreign-born
among 40.9m average residents. Under it the normalized figure would stay a benefit, roughly half the
absolute [INFERENCE; not computed]. A saturation rule, where large diasporas add nothing more, makes
the relative cost larger. [FRAMING-SENSITIVE]

## What the account already counts, and double counting

- **Production term P.** It is the native-wage response to the group's labour (−$0.20bn central,
  ladder 191). It carries no trade-cost channel [DATA: winners_losers channel registry].
- **Consumer-price channel.** The +$23.8bn CEX side view, never added, prices domestic
  immigrant-intensive services (Cortes) [SOURCE: consumer-price memo 2026-09-18]. It carries no
  imports.
- **Scale and restaurant variety.** City size (Card–Rothstein–Yi) and restaurant variety
  (disease_food lane) are domestic.
- **Receipts.** The account's receipts are keyed to residents' income and consumption. Taxes on other
  residents' extra real income from trade appear nowhere, so no induced receipt overlaps.
  - One overlap is known. The account credits the group with 8.89% of national sales tax, and that
    total includes tax paid by foreign visitors. The VFR line therefore double counts about
    8.89% × $0.12bn ≈ $0.01bn, which is negligible.
- **FDI-linked trade** sits in the trade line; the FDI line adds only the excess return.
- **Travel** is excluded from the trade line and priced once in the VFR line. The joint GE run
  differs from the sum of the two by $0.005bn [CALCULATION].
- **Remittances** are not trade and are excluded. The account's consumption key already nets them
  out.

## Disconfirmation

1. **Most estimates identify allocation, not creation.** The state-level designs (Parsons–Vézina,
   Gove, Dunlevy, Herander–Saavedra) and the county design (Burchardi–Chaney–Hassan) identify where
   trade or FDI goes within the US. National totals fall into the fixed effects.
   - Herander & Saavedra find in-state networks matter more than out-of-state ones. Part of a local
     effect is therefore trade moved between states.
   - The GE handles diversion across countries and domestic suppliers. It cannot undo the
     within-US reallocation built into the elasticities. This pushes toward the low arm.
2. **Saturation.** Gould: 90% of the US export effect is used up at ~15,575 immigrants, and 90% of
   the import effect at ~309,345. Mexico's 12.2m are far beyond both.
   - Genc et al. report elasticities falling as communities grow. They cite Egger et al.: the effect
     may reach zero above ~4,000 immigrants.
   - The marginal Mexican immigrant therefore adds ~0 trade. The with/without effect depends on how
     much of the network other residents would supply. The literature does not measure that.
3. **Geography, NAFTA/USMCA and language.** Mexico's network is collinear with the border and the
   trade agreement.
   - The Mexico-born stock has been roughly flat since about 2007 [TRAINING-DATA: Pew]. Meanwhile
     goods trade rose from $346.6bn (2007) to $837.6bn (2024) [SOURCE: Census c2010]. That growth
     came from supply chains, not the network.
   - Dunlevy finds Spanish-speaking origins cut the immigrant elasticity by 0.33–0.37, from about
     0.46–0.49, because natives already share the language.
4. **Reverse causality.** Trade and investment pull migrants: NAFTA-era agriculture, border
   manufacturing. Instruments exist for other settings, such as the refugee placement of
   Parsons–Vézina and the push-pull instrument of Burchardi–Chaney–Hassan. No Mexico-specific
   instrumental estimate exists; Gove uses propensity scores.
5. **Welfare from created trade is small.** The central's $72.9bn of created trade yields $6.2bn,
   8.5 cents per dollar. All US–Mexico trade is worth $59–118bn a year to other residents in this
   model (ε 8–4) [CALCULATION].
6. **Steel-man for larger.**
   - Parsons–Vézina find elasticities of 0.45–1.38 where information frictions were extreme.
   - White (2009) finds 0.365 for upper-middle-income origins, a group that includes Mexico.
   - Dunlevy's corruption interaction raises the effect for origins like Mexico.
   - Burchardi–Chaney–Hassan find descendants matter more than migrants, for FDI.
   - Models with intermediate inputs and many sectors give larger gains from trade than this
     one-sector model [TRAINING-DATA: Costinot & Rodríguez-Clare 2014; not applied].
   - The high arm ($23.7bn) reflects these.
7. **Premise check.** The brief says descendants have a weaker network effect. For FDI,
   Burchardi–Chaney–Hassan find the reverse: the effect "operates mainly through the descendants of
   migrants rather than migrants themselves". For trade no descendant estimate was found, so
   descendants get 0 in the low and central arms.

## What can be added beside the account

**Recommendation.** Add the absolute total, **−$6.8bn (−$1.1 to −$23.7bn)**, as a benefit line in the
§7b table beside the account, next to care, mobility and scale. Label it "modelled, marginal
elasticities extrapolated". Keep the normalized **+$0.8bn** beside it. Neither belongs in the fiscal
net.
- It is 2% of the $322–387bn main case. It moves neither the sign nor the order of magnitude.
- The VFR sales-tax piece is fiscal ($0.12bn central, after the 0.911 share) but too small to re-key.

## Files covered and skipped

Covered:
- Repository files:
  - `main_case_long_run_2026_09_27/RESULT.md` and `derived/components.csv`;
  - `winners_losers_2026_09_24/RESULT.md` (channel registry);
  - `research/immigration-real-fiscal-and-social-costs-2026-09-23.md` §3, §7, §7b and §8;
  - `decisions/2026-09-23-evidence-symmetry-rules.md`;
  - `disease_food_2026_09_28` `items.csv` and RESULT (format and normalization rule);
  - `consumption_key_2026_09_24` RESULT and `key_specs.csv`;
  - `target_population_cps2025.csv`;
  - BEA `NipaDataA.txt` (backtest cache).
- Primary sources: the Census Mexico trade page; the World Bank API; BEA direct investment xlsx
  (detailed country, country × industry); BEA SCB September 2025; NTTO SIAT 2024 and the land report.
- Papers:
  - Gould 1991 WP (Exa text, `_cache/gould_1991_exa.txt`; the direct PDF download was truncated);
  - Genc et al. (IZA DP 6145, Waikato and NORFACE versions);
  - Parsons–Vézina (IZA DP 10112);
  - Burchardi–Chaney–Hassan (NBER w21847 rev1);
  - Good/Gove 2012 draft (published in IEJ 2017);
  - Dunlevy (DIW working paper);
  - White (2009);
  - the Cohen–Gurun–Malloy abstract.

Skipped, with reasons:
- Head & Ries (1998) and Rauch (2001) were not read this session; the meta-analysis covers their
  estimates. [GAP]
- Cohen–Gurun–Malloy: no dollar magnitude was extracted. [GAP]
- Bandyopadhyay–Coughlin–Wall (2008): its Mexico-specific coefficient was not read. [GAP]
- Steingress (2018) and Aleksynska–Peri: not read.
- The BEA services-by-country table itself: the Mexico services and travel figures come from a
  mirror of BEA data. [GAP] Goods, 90% of the flows, come from Census.
- Mexico's FDI position in the US: the FDIUS xlsx link was not found. Inward FDI is not priced. [GAP]

## Log
- 2026-09-28 23:04 JST — stub written; frame inputs read. Union 40,896,574 (Mexico-born 12,220,782; second
  generation 14,333,218; third-plus self-identified 14,342,575) [DATA: crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv].
- 2026-09-28 23:06 JST — overlap check (first pass; time corrected from an estimate to the `date` call). The account's production term P is the native-wage
  channel only (−$0.20bn central, ladder 191) [DATA: winners_losers_2026_09_24/RESULT.md channel registry].
  The consumer-price channel (+$23.8bn CEX side view, never added) prices domestic immigrant-intensive
  services from Cortes's elasticities [SOURCE: research/immigration-consumer-price-and-native-hours-2026-09-18.md].
  The scale lane (Card–Rothstein–Yi city size) and the restaurant-variety items (disease_food_2026_09_28) are
  domestic. No priced line in the main case or beside it carries US–Mexico trade costs, trade volumes,
  FDI or visitor spending [INFERENCE from rg over main_case_long_run_2026_09_27, winners_losers, the
  real-costs memo §3/§7/§7b]. [GAP] induced receipts: re-check that no lane taxes export-sector output
  attributed to network trade.
- 2026-09-28 23:15 JST — literature, first pass (all quoted numbers read from the primary text or its working-paper version):
  - Genc, Gheasi, Nijkamp & Poot (IZA DP 6145, 2011; in Nijkamp, Poot & Sahin eds. 2012): 48 studies, 300 estimates;
    mean immigrant elasticity 0.17 for exports and for imports; interquartile 0.06–0.28 (exports), 0.07–0.26 (imports);
    after heterogeneity and publication-bias correction "10 percent more immigrants → about 1.5 percent more trade";
    fixed-effect weighted mean 0.10; lower for homogeneous goods; "the impact becomes smaller once a sizeable migrant
    community has been established", citing Egger et al. that the effect may decline to zero above ~4,000 immigrants
    [SOURCE: https://docs.iza.org/dp6145.pdf; researchcommons.waikato.ac.nz version].
  - Gould (1991 Dallas Fed WP 9102 = the 1994 REStat paper's working version): trade ∝ exp(β·M/(θ+M)), US aggregate
    exports β = 4.263, θ = 383; 90% of the information effect is exhausted at ~15,575 immigrants for US exports and
    ~309,345 for US imports; the sample minimum stock is 1,301 (Tanzania); short-run coefficients with a lagged
    dependent variable; θ has t ≈ 1 ("flat peak in the likelihood") [SOURCE: dallasfed.org wp9102.pdf, pp. 26–30,
    text via Exa crawl, _cache/gould_1991_exa.txt]. Mexico (12.2m) sits ~800 times past the export saturation point:
    the marginal Mexican immigrant adds ~0 trade in this model, and the with/without effect lies below the sample's support.
  - Parsons & Vézina (EJ 2018; IZA DP 10112): Vietnamese refugee placement as instrument; a 10% larger Vietnamese
    population raised a state's 1995 exports to Vietnam by 4.5–13.8%; the authors attribute the size to very high
    information frictions right after the 1994 embargo [SOURCE: docs.iza.org/dp10112.pdf]. State-level, identifies
    allocation across states, not national creation.
  - Burchardi, Chaney & Hassan (REStud 2019; NBER w21847): doubling county ancestry from the mean (316 → 632) raises the
    probability of an FDI link by 4 pp (coefficient 0.187 on log(1+ancestry/1000)) and jobs at origin-owned
    subsidiaries by 29%; "operates mainly through the descendants of migrants rather than migrants themselves";
    effect "highly concave" [SOURCE: NBER w21847 rev1 pdf; VoxEU column]. County design with origin fixed effects:
    the national total is absorbed by the fixed effects. **Premise check:** the brief says descendants have a weaker
    network effect; for FDI BCH find the opposite.
  - Cohen, Gurun & Malloy (JF 2017): firms trade more with countries whose residents live near headquarters; internment
    camps as a shock; firms near former camps trade more with Japan 75 years later [SOURCE: SSRN 2370091 abstract;
    phys.org summary]. [GAP] no dollar magnitude extracted.
  - US–Mexico: Good/Gove (IEJ 2017, 31(2):224–244; 2012 draft): US-state × Mexican-state exports, 2007–2011,
    elasticity 0.086 (SE 0.039); $2,467 extra annual exports per extra migrant at the mean pair stock of 2,407
    [SOURCE: 2012 draft Table 2 col. 4, via Exa]. Dunlevy (2006, state exports 1990–92): Spanish-speaking origin cuts the
    immigrant elasticity by 0.33–0.37 from ~0.46–0.49, because natives already speak the language [SOURCE: DIW WP
    Table 2–3]. White (2009): upper-middle-income origins incl. Mexico 0.365. Gove & Meza González (2022): Mexican-state
    panel 2008–2017, migration positively related to Mexico–US trade and US FDI in Mexico.
- 2026-09-28 23:15 JST — 2024 data: US goods exports to Mexico $334,492.1m, imports $503,110.1m (Census basis) [SOURCE:
  census.gov/foreign-trade/balance/c2010.html, fetched 2026-09-28]. Services with Mexico: exports $50.4bn, imports
  $45.1bn; travel exports $22.2bn, travel imports $26.3bn [SOURCE: BEA international services by country, read from
  the ustradesignals.com mirror; [GAP] BEA table itself not fetched]. US GDP $29,298,013m, exports of G&S
  $3,215,368m, imports $4,113,828m [DATA: BEA NipaDataA.txt A191RC/B020RC/B021RC, backtest_published_2026_09_28 cache].
  Mexico GDP $1,830.5bn, exports $682.5bn, imports $698.2bn; world GDP $111,669bn [SOURCE: World Bank API
  NY.GDP.MKTP.CD, NE.EXP/IMP.GNFS.CD]. US direct investment position in Mexico $155,901m, income $16,020m (2024,
  historical cost) [SOURCE: apps.bea.gov usdia-detailedcountry-2020-2025.xlsx]. Mexican visitors 2024: 13.4m overnight
  land visitors (VFR 21.3% of trips) and 3.5m air arrivals (VFR 21.7%, $1,379 spent per visitor) [SOURCE: NTTO via
  trade.gov SIAT 2024 and inboundtravel.org summary of the NTTO land report]. [GAP] Mexico's FDI position in the US.
- 2026-09-28 23:22 JST — priced: `price_trade_networks.py` (3-region DEK/ACR GE) → `derived/items.csv`, `grid.csv`,
  `inputs.csv`, `summary.json`; rc 0. Solver: relative excess-demand update, tolerance 1e-13; zero shock returns
  W-hat = 1 (assert). FDI base switched to positions outside holding companies ($15.3bn Mexico, $3,192.8bn all
  countries) after the first run, which moved the FDI normalized central from +$0.49bn to +$0.21bn. Verdict,
  table, method, overlap, disconfirmation and coverage written above.
