# Urbanism / Urban & Housing Economics Frontier — Immigration Fiscal/Crime Repo

**Date:** 2026-06-25
**Axis:** Spatial & housing-incidence frontier. The repo's biggest current gap: no dedicated urban frame, MSA rent × immigrant panel unbuilt.
**Status:** COMPLETE. Dataset acquisition map (7 components, all URLs verified live) + 18 graded papers across 3 frontier axes + scale-dependence displacement frame + 6-point disconfirmation. Single highest-priority integration: Wilson-Zhou (2026) Dallas Fed surge×housing causal magnitudes (full PDF read & verified).

**Instrument-bias note:** politically charged topic, LLM-assisted corpus, left-tilted field (urban econ especially). Per repo constitution: disconfirming/against-interest evidence weighted as higher-information; steelman before critique; every claim tagged `[SOURCE]`/`[INFERENCE]`/`[UNVERIFIED]`/`[TRAINING-DATA]`; framing-dependent verdicts flagged `[FRAMING-SENSITIVE]`.

**Already covered in repo (do NOT rediscover — this memo goes BEYOND):**
- `immigration-causal-saiz-elasticity-rent.md` — Saiz 2010 elasticity × ACS rent, CROSS-SECTIONAL 2022 only (panel/IV is the open step).
- Receiver-node shelter stress (NYC/Denver/Chicago/Boston/Bexar); PUMA local-burden layer; BPS permits + HUD PIT/HIC threshold panels.

---

## 1. DATASET ACQUISITION MAP — MSA rent × immigrant panel (the missing build)

The repo's only housing-urban join is the CROSS-SECTIONAL 2022 Saiz×ACS merge. The build below is the **longitudinal MSA rent × foreign-born-share × supply-elasticity panel** that feeds E-cluster theories E-001…E-008. All seven components are pullable-now except WRLURI (one-time download, no API). Recommended panel spine: **CBSA × year, 2015-2025**, with PUMA↔CBSA crosswalk for the existing warehouse join.

### Tier A — Rent / price outcome (the dependent variable)

**A1. Zillow ZORI + ZHVI (RECOMMEND as primary rent panel)** — `pullable-now, free, CSV`
- URL: https://www.zillow.com/research/data/ (CSVs update monthly on the 16th; Econ Data API also exists). [SOURCE: https://www.zillow.com/research/data/]
- **ZORI** = Zillow Observed Rent Index, a **repeat-rent index weighted to the ACS rental stock** (file B25127), dollar-denominated as mean of the 35th–65th percentile of asking rents, smoothed 3-month MA, with a seasonally-adjusted cut. Monthly, geographies: **Metro & US / State / County / City / ZIP**. Begins ~2015. [SOURCE: https://www.zillow.com/research/methodology-zori-repeat-rent-27092/]
- **ZHVI** = Zillow Home Value Index, weighted middle-third home value, monthly back to **April 1996**, at metro/county/city/ZIP/neighborhood; top/bottom/middle tier cuts and bedroom cuts available. [SOURCE: https://www.zillow.com/research/zhvi-user-guide/]
- **Settles:** the demand-shock outcome — lets us replicate Dallas-Fed-style "1% pop shock → X% rent" at CBSA × month, AND test renter (ZORI) vs owner (ZHVI) incidence separately. Free for academic use with attribution.
- **Quirk:** asking-rent index (flow of new leases), not contract rent of sitting tenants — over-states marginal-market movement vs ACS B25064 contract rent. Use BOTH: Zillow for high-frequency timing, ACS for incidence levels. ZORI metro file keys on CBSA code → direct join to Saiz/WRLURI.

**A2. HUD Fair Market Rents + Small Area FMRs (SAFMR)** — `pullable-now, free, xlsx + JSON API`
- FMR API: `https://www.huduser.gov/hudapi/public/fmr/data/{entityid}` (needs free token); metro entity IDs like `METRO47900M47900`. listMetroAreas endpoint enumerates. [SOURCE: https://www.huduser.gov/portal/dataset/fmr-api.html]
- SAFMR (ZIP-level, 65 designated metros, FY2018-FY2026): xlsx at https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html (~4 MB/yr). [SOURCE: https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html]
- **Settles:** an administrative 40th-percentile gross-rent series (HUD's own, not listing-based) for cross-validating Zillow; SAFMR gives ZIP granularity to test WITHIN-metro immigrant-enclave rent gradients (the Saiz-Wachter neighborhood channel). **Quirk:** FMR is a policy benchmark (40th pctile gross rent incl. utilities), not a market index — moves with HUD methodology changes, not just the market. Secondary cross-check, not primary.

### Tier B — Supply-side moderators (the interaction terms E-cluster needs)

**B1. Saiz (2010) housing-supply elasticity** — `already in repo` (`external/lifetime/saiz/saiz_2010_msa_elasticity.dta`, 269 MSAs, 1999 OMB). [SOURCE: repo; https://urbaneconomics.mit.edu/research/data] The `.dta` also carries **S_LAND_50 / FLAT_SHARE** (topographic buildable-land shares) and a **WRLURI2006** column — decompose regulation vs geography (E-002 negative space).

**B2. Wharton WRLURI2018 (Gyourko-Hartley-Krimmel 2021 JUE)** — `pullable-now, free, one-time download (no API)`
- Author mirror: http://www.jonathanhartley.net/data ("Gyourko, Hartley, and Krimmel (2021) WRLURI 2018 Data files"). Canonical: http://real-faculty.wharton.upenn.edu/gyourko/land-use-survey/. [SOURCE: http://www.jonathanhartley.net/data]
- 2,472 communities; aggregate index mean 0 / SD 1; **2,333 obs aggregable to CBSA**; quartile cut: bottom (WRLURI ≤ −0.64) lightly regulated, top (≥ +0.64) highly regulated. A **panel of ~500-890 communities answered BOTH 2006 and 2018** → the only consistent national *change*-in-regulation measure. [SOURCE: https://docs.huduser.gov/archives/portal/periodicals/cityscpe/vol23num1/ch2.pdf]
- **Settles:** a *regulatory* (not topographic) supply constraint distinct from Saiz, updated to 2018, with a within-jurisdiction change panel → tests whether the immigrant-rent pass-through is driven by regulation specifically. Cabral-Steingress (2026) already shows pass-through is larger where permits are fewer — WRLURI lets us replicate with a direct regulatory index.

**B3. Census Building Permits Survey (BPS)** — `already flagged in repo threshold panel; pullable-now` (annual/monthly permits by place/county/MSA, https://www.census.gov/construction/bps/). The supply *response* variable — Dallas Fed and Cabral-Steingress both key on "did permits rise?" BPS is how you measure it directly.

### Tier C — Immigrant exposure (the treatment) + geography spine

**C1. ACS housing-by-nativity** — `pullable-now, Census API` — B05002 (foreign-born), B25064 (median gross/contract rent), B25003 (tenure), B25070 (rent-as-%-income), B19013 (income), at CBSA and PUMA. Already used in the 2022 Saiz merge; the panel just iterates it 2010→2023 (1-yr) or rolling 5-yr. **B25127** is the ACS file Zillow itself weights to — natural reconciliation point.

**C2. LODES / LEHD (workplace × residence flows)** — `pullable-now, free` — https://lehd.ces.census.gov/data/ ; Origin-Destination Employment Statistics at census-block, plus WAC/RAC. **Settles:** the spatial-mismatch / commute channel — where immigrants *work* vs *live*, and whether enclave job access differs. Not in repo. (Heavy; block-level → aggregate to CBSA/PUMA.)

**C3. MABLE/Geocorr 2022 PUMA↔CBSA crosswalk** — `pullable-now, free, on-demand CSV generator` — https://mcdc.missouri.edu/applications/geocorr2022.html. Geocorr2022 uses 2020-census geography and supports **2020 AND 2010 PUMAs**, source=PUMA target=CBSA with population/housing-unit allocation factors (AFACT). [SOURCE: https://mcdc.missouri.edu/applications/geocorr2022.html] **This is the join key** that lets the MSA-level Saiz/WRLURI/Zillow panel map onto the warehouse's PUMA-level rent-burden layer (the unit-mismatch the Saiz memo §Limitation 4 flagged as unresolved). **Quirk:** Geocorr cannot crosswalk *across* decades (blocks change) — pick 2020 PUMAs for current ACS, 2010 PUMAs only for pre-2022 microdata.

### Build order (minimal → full)
1. **1/10 version:** Zillow ZORI metro CSV + ACS B05002/B25064 by CBSA, 2015-2024, join on CBSA code, regress Δrent on Δfb-share with Saiz elasticity interaction. Replicates Dallas-Fed sign at near-zero cost, no new license. (This is the single highest-ROI build.)
2. Add WRLURI2018 quartile + BPS permits as supply moderators → separates regulation from topography (E-002).
3. Add Geocorr PUMA↔CBSA → push elasticity/regulation down to the warehouse PUMA rent layer (resolves Saiz-memo Limitation 4).
4. Add LODES for the work-vs-live spatial-mismatch layer (genuinely new axis).
- **Shift-share IV warning (load-bearing):** the standard Card instrument (1990 origin-shares × national flow) is **contested** — Jaeger-Ruist-Stuhler (2018, 332 cites) show it conflates short- and long-run adjustment and is biased when past and present inflows correlate. Use their recommended multi-period / two-instrument correction, not naive Bartik. [SOURCE: 10.3386/w24285]

## 2. PAPERS (grades + what each tests/disconfirms)

Grade key: **A** = top-5/top-field journal or Fed/NBER with credible identification + replication; **B** = solid peer-reviewed, narrower or older ID; **C** = descriptive/correlational or contested ID. All saved papers are full-text in corpus or archived as source.

### 2a. Housing-cost incidence — the demand-shock ledger

**[A] Wilson & Zhou (2026), "The Impacts of Unauthorized Immigration on U.S. Labor and Housing Markets: New Evidence from Administrative Microdata."** Dallas Fed WP2607, https://doi.org/10.24149/wp2607. **THE single most decision-relevant new paper for this repo.** [SOURCE: https://www.dallasfed.org/~/media/documents/research/papers/2026/wp2607.pdf — full text read]
- **Design (verified from PDF):** restricted-use individual-level immigration-court microdata → monthly net unauthorized working-age entries by **county**, aggregated to **commuting zones (CZ) and MSAs**, 2021m3–2024m3. **Two-way leave-out shift-share IV** (Card 2001 + Burchardi-Chaney-Hassan 2020); placebo tests show no pre-trend; robustness across Freddie Mac HPI, CoreLogic HPI, CoreLogic SFRI; rent outcome = **Zillow ZORI** (validates dataset map A1).
- **Exact magnitudes:** UIWF = 1% of initial employment → **+2.2% house prices, +1.4% rents** (smaller single-family, larger multi-family). **Housing-supply (new permits/existing units) effect small and statistically insignificant across all segments.** Employment rose ~one-for-one; labor income per capita FELL; government transfers strongly fell. Back-of-envelope: UIWF explains **~30% of house-price growth, ~20% of rent growth** in the average MSA over the boom.
- **What it settles / disconfirms:** Directly resolves E-cluster theories E-001/E-003/E-004 with CAUSAL post-2020 magnitudes — confirms the inelastic-supply mechanism (no permit response) the repo's cross-sectional Saiz merge could only infer. Magnitudes "similar to Saiz (2007)." The fell-labor-income + fell-transfers results are independently relevant to the FISCAL ledger. **Against-interest note:** it is unauthorized-specific and a boom-period LATE; external validity to legal/stock immigration rests on the Saiz-magnitude match.

**[A] Saiz (2007), "Immigration and Housing Rents in American Cities"** (saved; the 2003 FRB Philadelphia WP is the OA version, Corpus W3121954821; published RES 2007). The landmark the brief named. Shift-share IV; immigrant inflow = 1% of MSA population → ~1% rise in rents AND housing values. **Tests:** the canonical demand-shock elasticity; every subsequent paper benchmarks to it. **Limit:** 1983-1998 legal-era variation, pre-frontier for the 2020s surge (hence Wilson-Zhou's value).

**[A] Cabral & Steingress (2026), "Immigration and US Shelter Prices: The Role of Geographical and Immigrant Heterogeneity,"** European Economic Review v182; Bank of Canada SWP 24-40. [SOURCE: https://www.bankofcanada.ca/wp-content/uploads/2024/10/swp2024-40.pdf]
- Ancestry-composition IV, US **counties** 1985-2019. House prices respond MORE than rents; pass-through larger where immigrants are more-educated AND where **fewer building permits** are issued (regulation interaction → validates dataset map B2/B3). But aggregate predicted contribution of immigration to shelter-price growth is **SMALL (~1.3% of a 17% house-price rise; ~similar for rents)**. **Disconfirms** strong-aggregate-effect framing while confirming positive local margin — the incidence-vs-aggregate distinction the repo already draws.

**[C, against-interest, HIGH-information] Camarota (CIS, 2024 House testimony).** [SOURCE: https://oversight.house.gov/.../Camarota-Testimony.pdf] Simple 2022 cross-section: +1pp recent-immigrant MSA share → US-born households spend +0.37pp of income on rent; +5pp → "12% increase in rent relative to income." **Explicitly self-labeled "only a simple correlation, does not include homeowners, much more detailed analysis needed."** Restrictionist-side source; its own caveat is the steelman-and-bound: the repo should cite it as the *upper-bound naive correlation* that the IV papers (Wilson-Zhou, Cabral-Steingress) discipline downward. Useful precisely as the over-claim to falsify.

**[C] Cato working-paper-37 (Greulich/Saiz-derived application).** [SOURCE: https://www.cato.org/sites/cato.org/files/pubs/pdf/working-paper-37_1.pdf] Applies Saiz/Ottaviano-Peri elasticities to urban counties: immigration explains 32.4% of 1970-2010 house-price rise in the 20 densest counties; up to 24% of 2010 median rent in Queens, 15% in SF; but "modest" and "not the major explanation" elsewhere. Notes Greulich et al. (2004): rent-to-income ratio is roughly EQUAL across high- vs low-immigrant cities because incomes rise concurrently — a direct caveat on the rent-burden framing.

### 2b. Native displacement / tipping — the spatial-correlations (Borjas) critique

**[A, the canonical NULL] Card (2001 / "Do Immigrant Inflows Lead to Native Outflows?")** [SOURCE: https://davidcard.berkeley.edu/papers/do-immig.pdf] At **MSA × skill-group** level (1970/80/90 Census): **NO native flight** — point estimates if anything show a *slight increase* in same-skill native population. This is the foundational result that area-study wage effects are NOT washed out by native out-migration. **The disconfirming anchor for the whole displacement frame.**

**[A] Saiz & Wachter (2011), "Immigration and the Neighborhood,"** AEJ:Policy 3(2):169-88, DOI 10.1257/pol.3.2.169 (has replication package). [SOURCE: https://www.aeaweb.org/articles?id=10.1257%2Fpol.3.2.169] At the **NEIGHBORHOOD** (sub-MSA) level with a geographic-diffusion IV: growing immigrant density → **native flight AND relatively slower housing-value appreciation** — but driven by **demand for residential segregation by ethnicity/education, NOT foreignness per se.** **Reconciles with Card:** displacement is a within-metro sorting phenomenon invisible at MSA aggregation. This is the scale-dependence that resolves the Card-Borjas tension.

**[A, newest] Boje-Kovacs, Mulalic, Saiz, Sant'Anna & Schultz-Nielsen (2024), "Immigrants and Native Flight: Geographic Extent and Heterogeneous Preferences,"** MIT CRE WP 24/08, SSRN 4883600. [SOURCE: https://www.vpsantanna.com/files/research/immigrants_and_native_flight.pdf] Denmark **building-level** panel 1987-2017, universe of individuals/properties, quasi-random refugee placement + simulated Markov instrument. **Strong causal native flight even at the BUILDING level**; flight stronger among the elderly and in reaction to LOW-INCOME immigrants; housing prices DECLINE as neighborhoods densify; subsequent move-ins are other immigrants or young low-income natives. Confirms Card et al. (2008) tipping at fine scale. **Caveat:** Denmark, refugee-specific — external validity to US owner-heavy suburbs is the open question.

**[B] Sá (2015), "Immigration and House Prices in the UK."** [SOURCE: https://docs.iza.org/dp5893.pdf] Finds immigration has a **NEGATIVE** effect on UK house prices, driven by native out-migration of the *top* of the wage distribution (negative income effect on housing demand). **Direct disconfirmation of the Saiz positive-price result** — sign flips when natives who leave are high-income. Mechanism-dependent; the US (Wilson-Zhou) finds positive because there the demand shock dominates the out-migration income effect. **Names the parameter (native preference for immigration) that flips the sign** — a key model contingency the repo should record.

**[B] Fernández-Huertas Moraga, Ferrer-i-Carbonell & Saiz (2019), "Immigrant locations and native residential preferences: emerging ghettos or new communities?"** JUE 112:133-151. Spain 1998-2008 10% population shock: only **MILD** native displacement from dense established neighborhoods + MORE real-estate development there; natives and immigrants co-locate in booming suburbs → **no net change in segregation.** Argues conventional methods OVERSTATE native flight when arrivals spawn new neighborhoods. The methodological caution against over-reading flight estimates.

### 2c. Urban productivity / agglomeration / innovation — the benefit-side ledger

**[A] Sequeira, Nunn & Qian (2019), "Immigrants and the Making of America,"** RES 86(1) (Corpus). Age of Mass Migration (1850-1920), railroad×flow IV: immigration → higher long-run income, manufacturing, innovation, urbanization, lower poverty. The historical causal benefit anchor.

**[A] Burchardi, Chaney, Hassan, Tarquinio, Terry (2020/NBER w27075), "Immigration, Innovation, and Growth."** [SOURCE: https://www.nber.org/system/files/working_papers/w27075/w27075.pdf] 130-yr ancestry IV, US **counties**: immigration has a **CAUSAL positive impact on patenting AND on native (US-born, even non-mover) wages.** 1 SD adult immigration (~7,000 migrants) → ~6% higher wages per capita; spillovers to wages within 100km. Structural model: post-1965 inflow → +8% innovation, +5% wages. **The single strongest benefit-side urban paper** — and it explicitly rules out the composition/native-flight confound (effect holds for native non-movers). Directly counterweights the cost-side housing ledger.

**[A] Hunt & Gauthier-Loiselle (2010), "How Much Does Immigration Boost Innovation?"** AEJ:Macro (Corpus). Immigrants patent at ~2× native rate (driven by STEM degrees); a 1pp rise in immigrant college graduates → 9-18% rise in patents per capita, with positive spillovers (no crowd-out of natives). Benefit-side micro-foundation.

**[A] Hsieh & Moretti (2019), "Housing Constraints and Spatial Misallocation,"** AEJ:Macro (Corpus). NOT immigration-specific but the load-bearing mechanism: stringent housing-supply restrictions in high-productivity cities (NY, SF Bay) misallocate labor and lowered **US aggregate growth ~36% over 1964-2009.** **The bridge between the two ledgers:** the SAME inelastic-supply regulation that makes immigrant inflows raise rents (cost) also caps the agglomeration gains immigrants could deliver (foregone benefit). Argues the housing-incidence problem is fundamentally a SUPPLY-policy problem, not an immigration problem.

**[B] Kerr & Kerr (immigrant entrepreneurship) + Kerr (2013 high-skill imm. innovation/entrepreneurship), NBER w22385 / w19377.** Immigrants ~25% of US workers in innovation/entrepreneurship and a similar share of patents/firm-starts; immigrant-founded firms survive and grow at least as well as native-founded. The entrepreneurship-density benefit channel the brief named (axis 3). Corpus-discoverable; not yet pulled full-text.

**[B] Buchholz (2021, JEoG) + Buchholz SERC DP "diversity spillovers."** [SOURCE: https://cep.lse.ac.uk/pubs/download/sercdp0175.pdf] LEHD matched employer-employee: +1 SD city immigrant diversity → ~5.8% higher wages (workplace diversity +1.6%); instrumented with lagged predictors. The mechanism (exposure/problem-solving) behind Ottaviano-Peri. **[B] Niebuhr-Peters-Roth (IAB 2022)** — native and foreign workers gain ~equally from big-city agglomeration experience EXCEPT low-skilled foreigners get a lower premium (they sort into lower-quality jobs); ~50% of the gap is job-quality composition. A nuance on WHO captures agglomeration returns.

### 2d. Gateway/sanctuary, congestion/infrastructure (brief axis 4 — thinner, flagged)

- **Congestion / VMT externality:** the repo already mines a Brookings/JPubE-2017 differentiated-VMT-tax paper (E-007/E-008: urban-differentiated VMT tax raising $55B/yr beats gas tax welfare by ~$10.5B; avg VMT price elasticity −0.117). This is the per-mile local externality the NAS lifetime-NPV ledger omits and immigrant urban concentration (FRBSF Albert-Monras channel, E-005) amplifies. **[GAP]** No paper directly estimates *immigration→congestion* cost incidence at MSA level — a genuine open build (could join LODES commute flows × foreign-born share × TTI congestion index).
- **Sanctuary-city dynamics:** **[GAP]** not searched this epoch; the brief ranked it 4th. Flag for a follow-on axis — the relevant frontier is whether sanctuary designation changes *settlement location* (and thus which elasticity quartile immigrants land in), not a housing-price channel per se. Lower priority than the housing-incidence core the brief called the biggest gap.

## 3. Genuinely NEW vs already-covered

| Item | Status | Why new |
|---|---|---|
| **Wilson-Zhou 2026 Dallas Fed surge×housing causal magnitudes** | **NEW** | Repo's surge memo (`immigration-causal-surge-2021-2024.md`) predates this; it is the first causal post-2020 housing estimate and supplies +2.2%/+1.4% + permit-null directly to E-cluster. **Highest-priority integration.** |
| **MSA rent × fb-share × elasticity longitudinal PANEL** (§1 build) | **NEW** | Repo has only the 2022 cross-section. The Zillow-ZORI-spine build (1/10 version) is the missing artifact for E-001…E-008. |
| **Zillow ZORI/ZHVI as rent panel** | **NEW dataset** | Repo used only ACS B25064 levels; ZORI gives high-freq CBSA timing — and is literally the Wilson-Zhou outcome var. |
| **WRLURI2018 + 2006→2018 change panel** | **NEW dataset** | Repo's Saiz `.dta` carries WRLURI2006 only; the 2018 wave + change panel separates regulation from topography (E-002 negative space). |
| **Geocorr2022 PUMA↔CBSA crosswalk** | **NEW dataset** | Resolves the Saiz-memo Limitation 4 unit-mismatch (MSA Saiz ↔ PUMA warehouse). |
| **LODES/LEHD work-vs-live spatial mismatch** | **NEW axis** | No spatial-mismatch/commute layer in repo at all. |
| **Native flight scale-dependence (Card MSA-null vs Saiz-Wachter neighborhood-flight vs Boje-Kovacs 2024 building-level)** | **NEW frame** | Repo has the Card-vs-Borjas WAGE debate (`immigration-causal-everify-card-vs-borjas.md`) but NOT the HOUSING/residential-sorting version. This is the spatial-correlations critique applied to the rent estimate itself. |
| **Hsieh-Moretti supply-misallocation bridge** | **NEW synthesis** | Ties the cost ledger (rents) and benefit ledger (agglomeration) to a single SUPPLY-policy root cause — reframes "immigration raises rents" as "restrictive zoning makes inflows costly AND caps their upside." |
| **Burchardi et al. w27075 native-non-mover wage gain** | **NEW benefit anchor** | Rules out the native-flight composition confound on the benefit side — the mirror of the cost-side displacement question. |
| Saiz 2010 elasticity × ACS rent cross-section | **COVERED** (`immigration-causal-saiz-elasticity-rent.md`) | — |
| Receiver-city shelter stress (NYC/Denver/Chicago/Boston) | **COVERED** + corroborated by CBO 61464 (4 cities = 90% of national shelter-population increase). |

## 4. Disconfirmation / against-interest

Per constitution Principle 4 (disconfirmation mandatory) + instrument-bias mandate (weight against-interest evidence higher). The cost-side housing story is the repo's *prior*; the strongest evidence AGAINST it:

1. **Timing/geography don't line up (Harvard JCHS + Yale Budget Lab + Axios).** [SOURCE: https://www.jchs.harvard.edu/blog/role-recent-immigrant-surge-housing-costs] Rents surged **12% in 2021** (CoreLogic) when immigration was modest (~1.17M, near 20-yr avg), then DECELERATED to ~2.8% in 2023 when inflows peaked (3.3M). Tedeschi (Yale Budget Lab): **no meaningful correlation** between metros with the largest 2019+ immigrant inflows and those with the largest home-price gains. **Reconciliation (not refutation):** this is an *aggregate/timing* argument; Wilson-Zhou's CZ-level IV isolates the marginal local effect *within* the period and still finds it positive — both can hold (near-term demand ↑, but mortgage-rate + native-household-formation shocks dominated the 2021 level surge). The honest statement: immigration is a **real but secondary** driver of the 2021-23 housing run-up (~20-30% of growth per Wilson-Zhou, ~modest per Cabral-Steingress), NOT the primary cause Vance-style rhetoric claims. **[FRAMING-SENSITIVE]**

2. **Aggregate contribution is small even where the local sign is positive (Cabral-Steingress).** Immigration predicted only ~1.3% of a 17% house-price rise nationally — the local coefficient does not aggregate to a large national share because immigrants are concentrated.

3. **Sign can flip negative (Sá 2015, UK).** Where high-income natives out-migrate, the income effect on housing demand dominates and immigration LOWERS house prices. The positive-rent result is contingent on the demand shock outweighing native-out-migration income loss — a model parameter, not a law.

4. **Native flight may be overstated by conventional methods (Moraga-Ferrer-Saiz 2019).** When immigrant arrivals spawn NEW neighborhoods (suburban co-location), net-flow tipping estimates overstate true displacement; Spain's 10% shock produced only mild displacement + more construction.

5. **Rent-to-income equalizes across cities (Greulich et al. 2004, via Cato WP37).** Because incomes rise alongside rents in high-immigrant cities, the rent-BURDEN ratio is roughly constant — undercutting the "renters strictly worse off" read unless you isolate non-mover incumbent renters whose wages don't rise. The repo's incumbent-renter-incidence framing survives this only if it conditions on non-movers.

6. **The benefit ledger is causal and native-inclusive (Burchardi et al., Hunt-Gauthier-Loiselle, Sequeira-Nunn-Qian).** Immigration's positive effect on innovation and on **native (incl. non-mover) wages** is identified with the same class of ancestry/shift-share IVs used on the cost side. A housing-only urban frame that omits this is a one-sided ledger; the net urban welfare sign requires netting agglomeration/innovation gains against rent incidence — and Hsieh-Moretti implies BOTH are governed by the same supply-elasticity policy lever.

**Net frame for the repo [FRAMING-SENSITIVE]:** the urban evidence supports a *bounded* cost claim — low-skill inflows raise incumbent-renter costs in inelastic, high-regulation metros (where immigrants concentrate), by a magnitude that is real but a minority share of recent housing inflation — set against a *causal benefit* (innovation, native-wage agglomeration) that is largest in those same productive cities. The binding variable on BOTH sides is housing-supply elasticity/regulation (Saiz, WRLURI), not immigration per se. This is the synthesis the MSA panel build is designed to quantify.

## Corpus / artifacts
- Saved papers: W3121954821 (Saiz 2003/2007), W2614214791 (Hsieh-Moretti), W2785732282 (Jaeger-Ruist-Stuhler shift-share), W3023146776 (Hunt-Gauthier-Loiselle).
- Archived sources: Dallas Fed WP2607 (full PDF at scratchpad `dallasfed_wp2607.pdf`, 65pp); Harvard JCHS disconfirming memo.
- Key DOIs (verified): 10.24149/wp2607 (Wilson-Zhou); 10.1257/pol.3.2.169 (Saiz-Wachter); 10.3386/w24285 (Jaeger-Ruist-Stuhler); 10.1257/mac.20170388 (Hsieh-Moretti); SSRN 4883600 (Boje-Kovacs et al.); EER v182 (Cabral-Steingress).
- [GAP] LODES/LEHD spatial-mismatch and Bogin-Doerner-Larson FHFA county HPI not yet pulled — flagged for the panel build, not blocking.
- [GAP] WRLURI2018 file not downloaded this session (URL verified live); one-time pull at build time.

