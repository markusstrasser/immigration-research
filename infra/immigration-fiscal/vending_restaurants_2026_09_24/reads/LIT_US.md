**Verdict:** No US study measures whether legalizing street vending cost restaurants sales, jobs or establishments; the evidence that exists is weak or indirect. Size: City of LA street food sells roughly $100m a year (2012–14), from one unsourced count (10,000 food vendors) times one convenience-sample revenue figure ($10,098 per vendor), so a one-for-one displacement bound is about $100m a year in the city. Uptake of legal status was small: about 944 city permits a year against an estimated 50,000 vendors, 165 food permits by mid-2021, and 9 compact-mobile-food permits supported in unincorporated county areas by January 2026, so "legalized" vending remains mostly unpermitted.
Effects: food-truck county panels find no lagged drop in restaurant counts (C−); Bogotá's cross-section finds shop-sales elasticity −0.044 to vendors on the block (p 0.08, C); Ulyssea's Brazil model has formal firms gaining 7.4% from enforcement while welfare falls 6.7% (B, model). Sanitation evidence (licensed trucks and carts have fewer violations than restaurants) covers only licensed vendors, not the unpermitted majority the operator's claim is about.

# US literature: street vending, food trucks and restaurants (lane vending_restaurants_2026_09_24)

Reader: literature lane, 2026-09-24/25. Scope: (1) LA street-vending size; (2) food trucks vs restaurants;
(3) evaluations of US vending legalization/enforcement; (4) health/sanitation comparisons;
(5) formal-informal competition (at most 4 sources).

Model self-report: claude-opus-5-5[1m] (Opus 5.5, 1M context).

Quote check: 60 of 60 table rows in the eleven notes files re-found in the saved parsed texts (whitespace-normalized full-quote match by `_cache/reads/verify_quotes.py`, rerun: `python3 _cache/reads/verify_quotes.py`; two-column PDFs checked against raw-order `pdftotext` parses `*_raw.txt`); the MyNewsLA, Sidewalk Stimulus, CAO and county-motion quotes in the size table re-found with `rg -F`. No row was dropped.

## Sources read

| Source | Year | Design | Key number (page) | Grade |
|---|---|---|---|---|
| Liu, Burns & Flaming, *Sidewalk Stimulus* (Economic Roundtable; underwritten by a vending-campaign member) — `sidewalk_stimulus_2015.md` | 2015 | Vendor count × one student-survey revenue figure; IMPLAN; uncontrolled same-block near/far comparison on 284 arrest sites | $504m/yr sales, City of LA (p. 3); food vendors ">$100 million" (p. 5); restaurants near vendors "added one more job" (p. 13) | Size C; restaurant effect D |
| Chief Legislative Analyst, Sidewalk Vending Status Report, CF 13-1493 — `cla_2014_sidewalk_vending_status.md` | 2014 | Attributed Bureau of Street Services estimate, no method | ~50,000 vendors, ~10,000 food (p. 2) | C− |
| StreetsLA report to Council, CF 13-1493-S5 — `streetsla_2019_09_19_report.md` | 2019 | Planning projection | ~16,000 vendors expected to take permits (p. 6) | C |
| City Administrative Officer fee study, CF 13-1493-S15 — `cao_2023_vending_fee_study.md` | 2023 | Administrative receipts and budgets | average 944 permits/yr (p. 3); $3.8m/yr enforcement and outreach (p. 3) | B |
| UCLA Law clinic et al., *Unfinished Business* (vendor advocates) — `ucla_law_unfinished_business_2021.md` | 2021 | Legal analysis; secondary counts; aid-applicant intake survey | 165 food permits of ~10,000 food vendors (p. 12); 73% of food vendors in the high-risk class (p. 10) | Counts C; restaurant claims D |
| Anenberg & Kung, JUE 90 (read: 2014 working paper) — `anenberg_kung_2015_food_trucks.md` | 2015 | Model + DC truck Twitter locations; variety counterfactual | mobility adds 7.6 trucks/week = 18% of nearby restaurants (Table 9, p. 27); no restaurant outcome estimated | B for variety; not evidence on displacement |
| Carpenter & Sweetland, *Food Truck Truth* (Institute for Justice) — `ij_food_truck_truth_2022.md` | 2022 | CBP county panel 2005–16, Arellano-Bond | lagged trucks → restaurants +1.837 (se 1.277, p 0.150; CI −0.67 to +4.34) (Table A1, p. 25) | C− |
| Rocha, Sánchez & García, *Desarrollo y Sociedad* 63 (study for the Bogotá chamber of commerce) — `rocha_sanchez_garcia_2009_bogota.md` | 2009 | Cross-sectional OLS, 694 shops, lagged-outcome controls | sales elasticity −0.044 (p 0.08), employment −0.05 (p 0.00) (Cuadro 4, p. 263); removing all vendors: shops +14% sales, all commerce −2.1% jobs (p. 263) | C |
| Ulyssea, AER 108(8) — `ulyssea_2018_aer.md` | 2018 | Structural equilibrium model, Brazil, simulated minimum distance | 41.9% of informal firms "parasite" (p. 2036); enforcement: formal incumbents +7.4% value, output +3.2%, welfare −6.7% (pp. 2042–44) | B (model) |
| Erickson, *Street Eats, Safe Eats* (Institute for Justice) — `ij_street_eats_safe_eats_2014.md` | 2014 | LA County DPH inspections 2009–12, establishment FE | violations per inspection: trucks 3.6, carts 2.4, restaurants 7.8 (Table 5) | B− for licensed vendors; silent on unpermitted |
| LA County DEO slides (EDPC, 15 Jan 2026) and Board motion (21 May 2024) — `lacounty_cmfo_counts_2024_2026.md` | 2024–26 | Program-output counts; unsourced stock estimate | 9 CMFO permits supported, 86 subsidies, 26 registration certificates (unincorporated areas); "50,000+ unpermitted sidewalk vendors in the County" | Counts B; stock C− |

Evidence-symmetry notes (rules 1–4 of `notes/quant-bias-checklist.md`): every causal or model estimate above carries its SE, p-value or "model counterfactual, no interval" and its population. Sponsorship carried no grade weight for any source: vendor-advocacy (Sidewalk Stimulus, UCLA Law), pro-vendor litigator (both IJ reports) and formal-business sponsor (Bogotá, commissioned by the chamber of commerce) were graded on design alone. Lean of the reading set: four read sources come from vendor-side sponsors and one from a business-side sponsor; the restaurant-side documents found last (California Restaurant Association op-ed, Cal Cities attorneys' whitepaper) were not read, so the restaurant complaint is represented here mainly by Bogotá, Ulyssea's model and quotes inside the other reports [GAP].

## Los Angeles size estimates

| Quantity | Value | Unit | Year | Source (page) | Basis |
|---|---|---|---|---|---|
| Street vendors, City of LA | ~50,000 (10,000 food, 40,000 non-food) | vendors | ~2014 | CLA 2014 (p. 2) | Bureau of Street Services estimate, no method |
| Unpermitted sidewalk vendors, LA County | 50,000+ | vendors | 2024 | County motion 21 May 2024 | stated, no method |
| Revenue per vendor | $204/week; $10,098/yr | $ | 2014 | Sidewalk Stimulus (p. 3), from a UCLA student survey in Westlake | convenience sample |
| All vendor sales, City of LA | $504m/yr | $ | ~2012–14 | Sidewalk Stimulus (p. 3) | [CALCULATION: 50,000 × $10,098 = $504.9m] |
| Food vendor sales, City of LA | >$100m/yr (the report calls it "income") | $ | ~2012–14 | Sidewalk Stimulus (p. 5): "mobile sales of food generated over $100 million in income" | [CALCULATION: 10,000 × $10,098 = $101m] |
| Vendor take-home income | $15,000/yr | $ per vendor | ~2021 | UCLA Law 2021 (p. 10, cited) | secondary |
| Sales tax not collected | ≥$33m/yr | $ | ~2012–14 | Sidewalk Stimulus (p. 6) | IMPLAN |
| Permits planned | ~16,000 | permits | 2019 | StreetsLA (p. 6) | projection |
| Permits actually issued | average 944/yr (78/month) | permits | FY2019-20 to 2022-23 | CAO fee study (p. 3): "an average of 944 permits" | administrative |
| Food permits, City of LA | 165 of ~10,000 food vendors | permits | mid-2021 | UCLA Law 2021 (p. 12) | secondary |
| Active city permits | 687 (53 food, 634 merchandise) = 1.4% of 50,000 | permits | Sept 2024 | MyNewsLA 5 Feb 2025 quoting a StreetsLA report: "there were 687 vendors with active permits, consisting of 53 food sellers" (`_cache/reads/mynewsla_2025_02_05_exa.txt`) | secondary; primary not found |
| County CMFO permits supported by DEO | 9 (86 subsidies; 26 registration certificates) | permits | to Jan 2026 | DEO EDPC slides | unincorporated areas only |
| City enforcement and outreach cost | $3.8m/yr | $ | FY2023-24 | CAO fee study (p. 3) | budget |

[INFERENCE] If every dollar of City of LA food-vending sales came out of restaurants, the loss would be about $100m a year in 2012–14 dollars; both inputs are weak (an unsourced count and one neighbourhood's revenue average), so the bound is uncertain by at least a factor of two either way. Vendors reportedly avoid selling food in front of restaurants (Kettles 2004, as summarized in Sidewalk Stimulus p. 10), which would push actual displacement below one-for-one; the Bogotá congestion channel would push the other way.

## Verified negatives (searches that found no study of the kind sought)

- [VERIFIED NEGATIVE] Exa, "empirical study effect of food truck entry on nearby restaurant sales, survival, openings or employment (Yelp, SafeGraph, permit data, city ordinance)": no study with restaurant sales, visits or survival as the outcome; only the IJ county panel, Schifeling et al. (Yelp ratings) and Freybote et al. (house prices).
- [VERIFIED NEGATIVE] Exa, "causal effect of street vendor eviction or relocation on sales of nearby formal retail stores, Latin America (Bogotá, Lima, Mexico City, Quito) difference-in-differences": no natural-experiment estimate; only the Bogotá cross-section; relocation studies (Quito, Cusco, Lima, Bogotá) are vendor-side or qualitative.
- [VERIFIED NEGATIVE] Exa, "study evaluating effects of California SB 946 sidewalk vending legalization on restaurants, brick-and-mortar businesses, sales tax or complaints": no empirical evaluation; results were Sidewalk Stimulus (pre-law), a UCLA planning capstone (Heil 2019, mapping and observation), a Pomona thesis (interviews), a Cal Cities attorneys' whitepaper (harms asserted without data), a 2019 city-attorneys legal paper, a night-market thesis, and an LA Times op-ed.
- [VERIFIED NEGATIVE] Exa, "evaluation of street vendor permit caps New York City or Chicago 2015 food cart ordinance effect on nearby businesses empirical analysis": none of the 8 results is a study of nearby-business outcomes (titles: NYC IBO fiscal estimate 2024, Illinois Policy 2015, Cornell ILR on NYC reform implementation, IJ Upwardly Mobile, two law-review notes, two geography papers).
- [VERIFIED NEGATIVE] WebSearch, "Los Angeles City Controller sidewalk vending program permits issued report audit": no Controller audit of the vending program.
- [VERIFIED NEGATIVE] WebSearch and Exa for StreetsLA permit counts by year and for LA County DPH compact-mobile-food permit totals: no public year-by-year permit series (the CAO study prints only an average) and no countywide CMFO total.

## Not reachable or not read

- Anenberg & Kung, published JUE text (doi:10.1016/j.jue.2015.09.006): `fetch_paper` failed; `crawling_exa` on doi.org returned metadata only. The April 2014 working paper was read instead.
- Carpenter, *Journal of Foodservice Business Research* (doi:10.1080/15378020.2023.2275514): journal text not attempted; the IJ report with the same analysis was read.
- clkrep.lacity.org timed out on http and https (read via Wayback `id_`); ij.org returned HTTP 403 to curl and file.lacounty.gov returned HTML challenge pages (both read through `crawling_exa`, excerpts saved in `_cache/reads/*_exa.txt`).
- [GAP] The StreetsLA report behind "687 active permits" (Sept 2024); the business-coalition rebuttal to Sidewalk Stimulus (LA Weekly, 25 Jun 2015); outbreak evidence tied to US street vendors (item 4, not searched).
- Found, not read (next epoch): NYC Independent Budget Office, "Fiscal Impact of Eliminating Street Vendor Permit Caps in New York City" (Jan 2024); Cornell ILR evaluation of NYC street-vending reform; Illinois Policy, "Chicago's food-cart ban costs revenue, jobs" (2015); Jot Condie (California Restaurant Association), LA Times op-ed, 29 Jul 2026; Cal Cities city-attorneys whitepaper on SB 946 enforcement; IJ *Upwardly Mobile* (2015 licensed-vendor survey); Schifeling et al. (2025) on food trucks and restaurant ratings; Freybote, Fang & Gebhardt (2017) on food-truck pods and house prices; KCRW (11 Aug 2021: ~1,800 city permits, 479 DPH food-cart permits since Jan 2019). An LA County Board motion (6 Feb 2024) seen only in a search excerpt puts food vendors countywide at "an estimated 10,000", which conflicts with the city-only 10,000 [UNVERIFIED].

## Findings log (appended as confirmed)

Entries 1–7 below, in the order confirmed; the summary tables above supersede none of them.

### 2026-09-24 entry 1: Sidewalk Stimulus (Economic Roundtable 2015) READ
- City of LA: 50,000 vendors/yr (StreetsLA estimate via CLA Nov 2014) × $10,098 revenue/vendor/yr (2014 UCLA student survey, Westlake) = $504m/yr sales; food vendors ~$100m/yr. [SOURCE: economicrt.org LA-Street-Vendor-Report-final-12-16-2015.pdf, pp. 1, 3, 5] Notes: `reads/sidewalk_stimulus_2015.md`.
- Restaurants: uncontrolled same-block near/far comparison on 284 arrest locations; restaurants near vendors "added one more job"; grade D for any effect claim.
- [GAP] root source of 50,000 (CLA report 13-1493, Nov 2014) not yet read; business-coalition rebuttal (LA Weekly 2015-06-25) not yet found.

### 2026-09-24 entry 2: City of LA permit counts READ (CLA 2014, StreetsLA 2019, CAO 2023, UCLA Law 2021)
- The 50,000 figure is an unsourced Bureau of Street Services estimate: "approximately 50,000 sidewalk vendors ... nearly 10,000 are food vendors" (CLA, CF 13-1493, 26 Nov 2014, p. 2). Notes: `reads/cla_2014_sidewalk_vending_status.md`.
- Plan: "approximately 16,000 of those vendors are expected to obtain ... permits" (StreetsLA, 17 Sep 2019, p. 6). Actual: "an average of 944 permits (78 permits per month)" FY2019-20 to 2022-23; enforcement and outreach $3.8m/yr General Fund FY2023-24 (CAO fee study, 25 Jul 2023, p. 3). Notes: `reads/streetsla_2019_09_19_report.md`, `reads/cao_2023_vending_fee_study.md`.
- Food: "only 165 out of an estimated 10,000 sidewalk food vendors ... have obtained permits" (UCLA Law et al., June 2021, p. 12). Notes: `reads/ucla_law_unfinished_business_2021.md`.
- Secondary only (news, primary not yet found): 687 active permits in Sept 2024, 53 food and 634 merchandise (MyNewsLA 5 Feb 2025 quoting a StreetsLA report); ~1,800 permits issued and 479 DPH food-cart permits since Jan 2019 (KCRW 11 Aug 2021). [GAP] StreetsLA Sept 2024 report; LA County CMFO permit counts after SB 972.

### 2026-09-25 entry 3: food trucks vs restaurants READ (Anenberg-Kung 2014 WP of JUE 2015; IJ Food Truck Truth 2022)
- Anenberg & Kung: variety and technology, DC trucks 2010–13; mobility adds 7.6 trucks/week = 18% of nearby restaurants (Table 9). **No restaurant sales/entry/exit outcome is estimated**; published JUE text not fetched [GAP]. Notes: `reads/anenberg_kung_2015_food_trucks.md`.
- IJ (Carpenter & Sweetland 2022): CBP counties 2005–16, Arellano-Bond; lagged food trucks → restaurants +1.837 (se 1.277, p 0.150), i.e. no detectable closures, CI −0.67 to +4.34 restaurants per truck; establishment counts only, ~1 employer truck per county. Grade C-. Notes: `reads/ij_food_truck_truth_2022.md`.
- Leads seen, not read: Schifeling et al. (Temple, 2025) gourmet trucks and Yelp ratings of 34,727 fusion restaurants in 7 metros 2005–14 (ratings, not sales); Freybote, Fang & Gebhardt 2017 (J. Property Research) food-truck pod DiD on nearby Portland house prices, reported negative.

### 2026-09-25 entry 4: formal-informal competition, Bogotá READ
- Rocha, Sánchez & García 2009 (Desarrollo y Sociedad 63; CEDE study for the Bogotá chamber of commerce): cross-section of 694 shops, 2004; elasticity of shop sales to vendors on the block −0.044 (p 0.08), employment −0.05 (p 0.00); vendors = 2% of corridor sales; simulated removal of all vendors: shops +14% sales/+16% jobs, all commerce +11% sales but −2.1% jobs. Grade C. Notes: `reads/rocha_sanchez_garcia_2009_bogota.md`.
- Searched and not found: any US or Latin American eviction/relocation natural experiment with nearby formal-shop sales (Lima, Mexico City Centro Histórico 2007, Quito 2003 relocation, Cusco studies are qualitative or vendor-side only). [VERIFIED NEGATIVE, one Exa search + scan of 9 results]

### 2026-09-25 entry 5: formal-informal competition model, Ulyssea 2018 AER READ
- Brazil structural model: 9.3% of informal firms kept out by entry costs, 41.9% "parasites" that could survive formally, 48.8% survival-only; enforcement that nearly eradicates informal firms raises always-formal firms' value 7.4%, TFP 8.3%, output 3.2%, cuts low-skill wages 8.5% and welfare 6.7%; cutting formal entry costs instead raises welfare 5.5% (pp. 2036–2044, Tables 5–6). Grade B (model; no US magnitudes). Notes: `reads/ulyssea_2018_aer.md`.

### 2026-09-25 entry 6: sanitation, IJ *Street Eats, Safe Eats* 2014 READ
- LA County DPH inspections 2009–July 2012: violations per inspection trucks 3.6, carts 2.4, restaurants 7.8; restaurant–cart gap 5.65 (237% more), significant with establishment FE; only 236 licensed carts inspected, no food-risk control in LA. Grade B− for licensed vendors; says nothing about unpermitted vending. Notes: `reads/ij_street_eats_safe_eats_2014.md`.

### 2026-09-25 entry 7: LA County formalization after SB 972 READ
- DEO (EDPC slides, 15 Jan 2026): unincorporated areas, 162 CMFO workshops, 86 subsidies, 9 CMFO permits supported, 26 sidewalk vending registration certificates; Board motion (21 May 2024): "an estimated 50,000+ unpermitted sidewalk vendors in the County". No countywide DPH CMFO total found [GAP]. Grade B for program counts, C− for the stock estimate. Notes: `reads/lacounty_cmfo_counts_2024_2026.md`.
