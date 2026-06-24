# Immigration lifetime fiscal — idea generators

**Date:** 2026-06-15 (rounds A–S); 2026-06-23 (round T benefit-side, round U source-incentive meta)
**DuckDB:** `warehouse/immigration_lifetime_evidence.duckdb`

**Totals:** 563 DuckDB `parameter_claims`, 124 Markdown `G-LIF-*` headings / 122 DuckDB `lifetime_generators` rows across **22 clusters (A–V)**. Round T (`T_immigrationist_steelman`, 8 benefit-side lenses) mirrors the 14-lens restrictionist cluster S; its 6 external papers were acquired to corpus 2026-06-24. Round U (`U_source_incentive_meta`, 2 lenses) operationalizes against-interest source weighting — applied pass in `immigration-source-incentive-regrade-2026-06-23.md` (`source_incentive_grades` table). Round V (`V_deep_roots_long_run_skeptic`, 8 lenses, added 2026-06-24) is the LONG-RUN cultural/institutional skeptical complement to S — all 6 external papers acquired to corpus, V08 crime-null verified in-warehouse. Q/R/S names backfilled 2026-06-23 (were null). Count reconciliation: MD-only IDs remain `G-LIF-Q06` and `G-LIF-S15` (2 MD headings without DB rows). See `immigration-thesis-generator-audit-2026-06-16.md`.

## A_npv_generational

### G-LIF-A01 — Capital-tax omission audit

**Prompt:** For each lifetime fiscal NPV study in the corpus: list every tax base counted on the revenue side. If corporate/capital income is absent, mechanically apply α/(1-α) × τ_K/τ_L × labor tax base (Clemens 2023 eq. 14) and re-rank education cells by sign. Flag any headline scalar that flips.

**Retrodiction:** Would have surfaced Clemens (2023) capital-tax flip (-$109k→+$128k for <HS) AND Colas-Sachs critique that Storesletten (2000) omits capital-supply response — both hinge on the same omitted tax base before reading either paper's policy conclusion.

**Negative space:** Standing frame treats 'taxes paid by immigrants' as labor+payroll cashflow only; excludes owner-side capital incidence entirely.

### G-LIF-A02 — Public-goods allocation stress grid

**Prompt:** Build a 3×3 grid for every NPV table: {zero marginal, 0.25×AC, full AC} × {exclude defense, include defense, include all public goods}. Extract the cell each paper reports as 'the' estimate. Never cite a scalar without grid coordinates.

**Retrodiction:** Would have flagged NAS Table 8-12/8-13 dual panels (public goods in/out) AND Orrenius marginal-cost sensitivity AND Colas-Sachs Table 3 (-$86/yr vs -$2,429/yr for HS dropouts) before treating -$109k as robust.

**Negative space:** Debates anchor a single NPV number; papers bury allocation rules in table notes.

### G-LIF-A03 — Composition-vs-level decomposition

**Prompt:** For generational-accounting immigration papers: (1) simulate level change holding 1990 education mix fixed; (2) simulate education-mix shift holding count fixed; (3) report which moves fiscal imbalance >10× more than the other. Reject any study reporting only total immigrant NPV.

**Retrodiction:** Would have extracted Auerbach-Oreopoulos (2000) finding that composition beats level AND Lee-Miller (1998) $2.2k vs $49.7k scale result AND NAS contrast of recent (+$259k) vs all-immigrant (+$58k) pools.

**Negative space:** Policy argument uses 'more immigrants' scalar; literature says education mix is first-order.

### G-LIF-A04 — Unit harmonizer: annual incidence vs lifetime NPV

**Prompt:** Whenever a fiscal claim uses $/year (incidence, MVPF, annuitized direct), convert to 75-year NPV at stated discount AND label incomparable if indirect/general-equilibrium. Block synthesis until units match.

**Retrodiction:** Would have caught Colas-Sachs ~$753/yr indirect vs NAS -$109k lifetime as different objects AND Clemens factor-3.2 adjustment on same NAS table AND Orrenius mixing cross-section billions with NPV thousands.

**Negative space:** Standing frame collapses 'fiscal effect' into one ledger line.

### G-LIF-A05 — Immigrant attribution convention check

**Prompt:** In generational accounting papers: trace whether immigrants' taxes are folded into native cohorts or separate Q_{s,k} terms. Recompute headline imbalance under both conventions. Document which convention each citation uses.

**Retrodiction:** Would have found Lee-Miller 54% vs GPS 72% imbalance gap AND Green-Kotlikoff warning that fiscal labels are reference-dependent AND NAS Table 8-13 native/immigrant pairing.

**Negative space:** Treats generational accounting as objective balance sheet.

### G-LIF-A06 — Descendant ledger split

**Prompt:** For every lifetime NPV, force extraction of {individual, descendants, total} columns. Flag papers that report total only. Test whether descendant surplus drives positive headline for low-skilled arrivals.

**Retrodiction:** Would have surfaced NAS $173k individual + $85k descendants (= $259k) AND Clemens -$109k individual vs +$326k with grandchildren AND NAS No-Budget scenario where descendants are -$15k while immigrant +$92k.

**Negative space:** Headline 'immigrant fiscal impact' silently includes second/third generation without education×age path.

---

## B_labor_market

### G-LIF-B01 — Native out-migration fiscal residue

**Prompt:** For each immigration shock geography (state, MSA, PUMA), ask: what fraction of the measured local wage/fiscal burden is attenuated because natives left (Borjas w11610 40-60% band)? Who remains to pay state/local taxes and use schools — incumbents, in-migrants, or replacement population? Build a sensitivity table: full shock vs attenuated shock on origin×PUMA ledger.

**Retrodiction:** Would have surfaced w11610 attenuation, Card-Peri JEL Table 3 mobility debate, and brainstorm Round 8 note on PUMA fiscal attribution before treating ACS snapshot populations as shock bearers.

**Negative space:** Standing NAS/SIPP frame assigns costs to immigrants present in a cell without modeling native selective exit from high-immigrant PUMAs.

### G-LIF-B02 — Task complementarity vs substitution band

**Prompt:** When national estimates show large wage losses for <HS (Borjas) but area studies show nulls (Card), search for task-specialization or native-immigrant imperfect substitution mechanisms (Peri-Sparber, Ottaviano-Peri, Foged-Peri). Map the implied earnings-path band to indirect fiscal offsets (Colas-Sachs-style) rather than point-estimate NAS <HS NPV.

**Retrodiction:** Would have connected Peri-Sparber w13389, Foged-Peri w19315, Ottaviano-Peri w14188, and Card-Peri w32389 into a single complementarity sensitivity band before treating Borjas -4% as the earnings anchor.

**Negative space:** Canonical CES perfect substitution within education cell — no task reallocation, no σ_IMMI heterogeneity.

### G-LIF-B03 — Mariel <HS calibration bracket

**Prompt:** Treat Mariel boatlift as mandatory stress-test for <HS lifetime cell calibration: Card null (7% labor force, ~20% less-skilled supply) vs Borjas -13% to -15% immediate log wage vs race-adjusted recovery by 1990. Require any <HS NPV projection to declare where it sits in this bracket and why.

**Retrodiction:** Would have flagged Mariel stack (w3069, w21850, w23504) as the key falsifier for mapping wage pessimism into NAS -$109k <HS age-25 cell without sensitivity.

**Negative space:** Single canonical wage elasticity applied to all low-skill inflows regardless of shock size, sample definition, or recovery horizon.

### G-LIF-B04 — Wage effect ≠ fiscal effect

**Prompt:** Whenever a paper reports wage elasticity (e.g., 10% supply → 3-4% wage), ask what fiscal ledger line it actually moves: earnings tax base? transfer take-up? incarceration cost? school demand? Flag papers that infer fiscal sign from wage sign without PAYG, capital adjustment, or local cost channels.

**Retrodiction:** Would have blocked silent import of Borjas w9755 -4% into NAS <HS NPV without Storesletten/Clemens capital-tax and federal-offset disconfirmation passes.

**Negative space:** Competitive labor market partial equilibrium — wage change is sufficient statistic for immigrant fiscal externality.

### G-LIF-B05 — Sample-specification audit for <HS cells

**Prompt:** Before accepting any <HS wage estimate, audit sample rules: age floor (exclude 16-18 enrolled students misclassified as dropouts), sex pooling, Hispanic inclusion in 'native' trends, placebo city choice. Re-run sensitivity on Mexico-weighted <HS cell with each contamination flagged.

**Retrodiction:** Would have caught Borjas w21850 critique of Peri-Yasenov 16-18 misclassification and Card-Peri JEL pit-vs-mit specification fork before locking calibration parameters.

**Negative space:** Education bucket from CPS highest grade completed taken at face value without age/enrollment filters.

### G-LIF-B06 — Distributional spillover beyond average native

**Prompt:** Search for immigration effects on subgroups omitted from average-native fiscal cells: Black employment/incarceration (Borjas-Grogger-Hanson), young/low-tenure manual workers (Foged-Peri). Ask whether lifetime ledger needs subgroup rows, not just education×state averages.

**Retrodiction:** Would have surfaced w12518 incarceration channel and Foged-Peri young-worker upgrading as missing ledger lines in Mexico <HS scalar debates.

**Negative space:** Representative native worker sufficient for fiscal incidence; no racial or tenure heterogeneity.

---

## C_local_welfare_capacity

### G-LIF-C01 — Federal-positive / local-negative ledger split

**Prompt:** For each fiscal immigration study, tag every cost and revenue line as FEDERAL vs STATE/LOCAL vs EPISODIC-SHOCK (shelter, border). Where does the paper silently aggregate jurisdictions? Cross-walk to our narrow SIPP-style `mexico_origin` annual federal proxy (+$1,519/adult/yr; payroll/FICA minus SNAP/TANF/SSI only) vs CBO-style local shock ledger (school, shelter, Medicaid). List papers that report net positive lifetime NPV but omit local surge lines.

**Retrodiction:** Would have surfaced CBO 61256 $9.2B direct net cost, Gould shelter 60% of homelessness rise, Orrenius 2025 federal-positive/state-local-negative split, and our scenario-composition frame tension before treating SIPP cells as scalar verdict.

**Negative space:** Lifetime NPV and generational accounting collapse jurisdiction and time horizon — hiding episodic shelter shocks and balanced-budget state constraints.

### G-LIF-C02 — Welfare magnet: selection vs treatment vs policy regime

**Prompt:** Map each welfare-migration paper to (a) migrant self-selection (treatment on movers), (b) host policy filter (treatment on admissions), (c) free vs restricted mobility regime. Does generosity affect skill mix (Razin-Wahba) or flow level (Landais Denmark DiD)? Flag studies that interpret correlation as magnet without regime dummies.

**Retrodiction:** Would have found Razin-Wahba sign flip, Landais 5k/yr causal reduction and elasticity 1.3, Bitler-Hoynes post-PRWORA immigrant lower participation within poor households, Borjas w4872 assimilation-into-welfare cohort effects.

**Negative space:** US interstate magnet literature often ignores that PRWORA made immigration policy federalism — treatment is policy+selection entangled.

### G-LIF-C03 — Crime/incarceration: fiscal line item or labor spillover?

**Prompt:** Separate incarceration as (1) direct state/local budget line (CBO incarceration spending) from (2) labor-market/competition spillover (Borjas-Grogger-Hanson) from (3) compositional base-rate artifact (Butcher-Piehl native 2.16% vs immigrant 0.7%). Which lifetime fiscal models include any of these channels?

**Retrodiction:** Would have flagged Butcher w6067 low immigrant incarceration vs rising native rates, CBO surge prison share (4% state, 7% pop), and brainstorm note that NAS ledger omits crime channel.

**Negative space:** Advocacy frames swap fiscal incarceration costs for crime rates; empirical lit shows immigrants lower institutionalization — channel is distributional not average fiscal drain.

### G-LIF-C04 — Asylum/shelter episodic shock outside lifetime NPV

**Prompt:** Identify spending that is (a) emergency/episodic, (b) city-concentrated, (c) absent from NAS/CBO federal lifetime tables. Quantify shelter PIT/HUD linkage (Gould) vs K-12 entitlement (CBO Plyler) vs Medicaid federal-state match. Would discounting lifetime NPV miss 2022-2024 shelter spike?

**Retrodiction:** Would have surfaced Gould 60% of 43% sheltered rise, CBO $3.3B shelter in 4 states, NYC +77,352 sheltered 2022-2024, and mismatch with smooth lifetime NPV curves.

**Negative space:** Lifetime fiscal synthesis uses steady-state education/transfer paths — asylum parole surges are state-local balance-sheet events.

### G-LIF-C05 — County fiscal capacity heterogeneity

**Prompt:** Where do national-average fiscal estimates hide county-level capacity constraints? Use BoC county IV design: low-skilled inflow → per-capita revenue down, spending down (Presidio −15%) vs high-skilled uplift (Monterey +14%). Cross to our PUMA/stage5 school spend weights and FRBSF urban concentration.

**Retrodiction:** Would have found BoC 0.3%/yr national offset masking ±15% county swings, FRBSF urban/remittance concentration, VMT $0.218/urban-mile congestion add-on, CBO 56% surge in 6 states.

**Negative space:** Scalar 'Mexico NPV' erases geography — same immigrant type can expand or contract local public goods depending on county skill mix and transfer insurance.

### G-LIF-C06 — Descendant and mobility offsets on local burden

**Prompt:** Track who bears local costs vs who captures fiscal upside: Orrenius assigns K-12 cost to US-born children; Akers-Boustan shows bottom-decile native HS completion +2.2pp per 10pp inflow; Blau-Kahn decomposes inequality not net fiscal position. Does immigrant-headed household federal proxy include citizen-child benefits without citizen-child future taxes?

**Retrodiction:** Would have connected Orrenius descendant-cost framing, Akers-Boustan decile-heterogeneous mobility, Blau-Kahn compositional inequality, Bitler-Hoynes 90% immigrant households contain native-born members.

**Negative space:** Household-weighted federal proxy treats citizen children as immigrant fiscal property in both costs and benefits.

---

## D_composition_descendants

### G-LIF-D01 — Static ACS snapshot vs Hanson composition time series

**Prompt:** For each origin×education_bucket cell in the scenario ledger, compare (a) a single ACS 2023 composition weight to (b) a Hanson w23753 time-varying weight series (1990–2015 Mexico/Latin America <HS shares, post-2007 inflow slowdown). Where does a static snapshot mis-state the stock entering the NAS <HS age-25 NPV cell?

**Retrodiction:** Would have surfaced Hanson 510k→−160k undocumented swing, Mexico share peaking 2005 then declining, and the brainstorm memo's Round 8 'composition over time' angle before building origin_fiscal_scenario with fixed ACS weights.

**Negative space:** Standing frame treats ACS 2023 as sufficient composition prior; excludes epochal composition drift and attrition-driven stock stabilization.

### G-LIF-D02 — Return migration / attrition ledger (CHCP blocked)

**Prompt:** Build an attrition sensitivity band on lifetime NPV: (1) Lubotsky/Dustmann selective re-migration bias on assimilation, (2) Hanson post-2007 net undocumented outflow, (3) Duncan-Trejo ethnic attrition on 3rd+ Hispanic measurement. Flag data gaps: Aydemir-Robinson CHCP working paper HTML-only trap; no US fiscal micro for return migration. What ledger line adjusts NPV horizon when attrition is negatively selected?

**Retrodiction:** Would have flagged brainstorm Round 8 item 10 (CHCP blocked) and Dustmann survey §5.9 return-migration gap before treating SIPP annual proxy as full lifetime residence.

**Negative space:** Lifetime fiscal models assume immigrants remain until death; cross-sectional assimilation overstates economic success.

### G-LIF-D03 — Descendant NPV as separate ledger line

**Prompt:** Split lifetime ledger into (A) first-generation immigrant NPV from NAS education×age cells and (B) descendant offset line with two bounds: Abramitzky w26408 (+3–6 percentile mobility at bottom; geographic sorting explains 70%) vs Duncan-Trejo w24394 (Hispanic 2nd→3rd+ earnings stall; ethnic attrition may understate progress). UK Dustmann-Frattini shows descendant accounting breaks at age 16. Where is descendant NPV missing from compose_scenario_ledger?

**Retrodiction:** Would have paired brainstorm Round 5 items 3–4 (descendant upside/downside) and UK methodology comparator before collapsing descendants into same NAS cell as parents.

**Negative space:** NAS descendant column treated as single calibrated offset; no explicit Abramitzky–Duncan-Trejo band or separate ledger row.

### G-LIF-D04 — Political economy of transfers (taxpayer wallet frame)

**Prompt:** Audit lifetime fiscal memos for the unnamed assumption fiscal impact = native taxpayer wallet only. Cross-read Razin-Sadka-Swagel (demogrant coalitions; unskilled policy dominance), Alesina w24733/w25562 (immigration salience → less redistribution; welfare-state size heterogeneity), and IMF remittance offset. What transfers are excluded from the ledger (remittances, origin-country education subsidy, voter preference shift)?

**Retrodiction:** Would have surfaced brainstorm Round 3 item 4 (Alesina redistribution) and Round 5 political-economy pairing before treating NAS net fiscal as welfare-neutral accounting.

**Negative space:** Technical NPV treated as sufficient for policy; political feedback on transfer generosity and native fiscal capacity ignored.

### G-LIF-D05 — Legal-status → education-bucket transition path

**Prompt:** Map legal-status shocks (DACA w24315: +5.9pp HS completion, 40% citizen gap closure; Hanson undocumented share of <HS stock) to education_bucket transitions in the scenario ledger. Does a legalization path move cells from <HS toward HS, changing NAS NPV sign within the same ACS origin weight?

**Retrodiction:** Would have connected brainstorm Round 4 Kuka DACA item to education-bucket composition before treating legal status as orthogonal to NAS cell assignment.

**Negative space:** Legal status treated as parallel unauthorized earnings path, not as human-capital investment response shifting education bucket.

### G-LIF-D06 — Migrant networks and destination-selection composition

**Prompt:** Borjas-Monras w23756: hurricane shocks × prior US migrant stock (threshold 0.86%) → legal immigration via family reunification. Abramitzky w22381: name-based assimilation closes half the gap in 20 years. How does network-driven destination selection reweight state/PUMA fiscal incidence vs national ACS composition weights?

**Retrodiction:** Would have surfaced network-fixed-cost mechanism and border-state concentration (Hanson table 3) before applying national Mexico weights to state stage5 context.

**Negative space:** Origin composition weights applied nationally; destination network sorting and border-state hours-share ignored.

---

## E_housing_rent

### G-LIF-E01 — Rent exposure vs renter welfare loss (Saiz gate)

**Prompt:** For each fiscal/local-burden memo, tag rent findings as (a) price level, (b) renter incidence, (c) owner offset, (d) supply elasticity quartile. Where does the paper treat median gross rent as welfare loss without Saiz? Cross-walk adversarial review 'rent exposure ≠ welfare loss' to repo merge: inelastic Q1 FB 11.6% vs elastic Q4 4.4%.

**Retrodiction:** Would have surfaced Saiz merge re-grade before using origin_puma_household_context rent burden as benign exposure; Miami/LA/SF/SJ at elasticity floor.

**Negative space:** Lifetime NPV and PUMA rent tables omit housing supply elasticity — same rent $ can be absorbed (elastic) or pure renter loss (inelastic).

### G-LIF-E02 — Regulatory vs topographic supply channel

**Prompt:** Decompose Saiz inelastic MSAs into WRLURI (regulation) vs S_LAND_50 / FLAT_SHARE_50_15 (topography). Which immigrant-heavy destinations are regulation-bound vs land-bound? Flag papers that cite 'build more housing' without naming which constraint binds.

**Retrodiction:** Would have split Boston/NYC/SF (low elasticity + high WRLURI) from mountain/desert MSAs; policy lever differs (zoning reform vs nothing).

**Negative space:** Fiscal immigration debate treats housing as generic local cost — not as regulatory externality vs geographic fact.

### G-LIF-E03 — Remittance-attenuated housing demand (FRBSF offset)

**Prompt:** Map FRBSF/Albert-Monras mechanism (lower housing consumption, remittance-reduced COL pass-through) against Saiz-conditional rent burden. When does urban selection into inelastic cities dominate demand attenuation? Tag origin groups by remittance intensity (World Bank) × MSA elasticity.

**Retrodiction:** Would have reconciled FRBSF 'immigrants less deterred by COL' with repo 'immigrants in inelastic expensive MSAs' — both true; net renter welfare sign needs tenure mix.

**Negative space:** Remittance literature and rent-burden warehouse rarely joint-conditioned on elasticity quartile.

### G-LIF-E04 — Urban per-mile externality layer (VMT) missing from lifetime NPV

**Prompt:** Identify local costs that scale with urban driving not gallons: VMT/congestion (Langer-Maheshri-Winston), differentiated urban/rural tax welfare +$10.5B. Cross to FRBSF urban immigrant concentration. Does NAS lifetime ledger include any non-housing urban externality?

**Retrodiction:** Would have added per-mile congestion margin alongside PUMA rent; immigrant urban sorting → double local channel (rent + VMT) in same MSAs.

**Negative space:** Housing-heavy vs school-heavy typology ignores third 'urban mobility' ledger line.

### G-LIF-E05 — education_bucket × state × elasticity scenario cell

**Prompt:** Refuse scalar Mexico NPV. Build scenario cells: education_bucket × state × descendant_band × Saiz quartile. Which NAS cells assume national average destination when ACS weights imply inelastic-state concentration for <HS vs H-1B/high-skill buckets?

**Retrodiction:** Would have blocked pooling Mexico <HS surge cells with national rent average; CA/NY/TX gateway elasticity Q1 dominates origin_puma weights for multiple groups.

**Negative space:** Lifetime benchmarks in npv_education_benchmarks have no destination elasticity dimension — housing incidence silently averaged out.

---

## F_high_skill

### G-LIF-F01 — H-1B bucket ≠ Mexico <HS NAS cell

**Prompt:** Split lifetime fiscal scenarios by admission channel: H-1B/STEM high-skill (Bound-Khanna) vs <HS unauthorized/surge (Hanson/CBO). Where does any memo pool them into one 'immigrant NPV'? Map H-1B to separate education_bucket with innovation/firm-profit offsets not in NAS Table 8-12.

**Retrodiction:** Would have blocked scalar Mexico verdict from absorbing H-1B federal-positive innovation path; CS wage −2.6–5.1% distributional fork explicit.

**Negative space:** NAS education cells conflate arrival credential with visa/channel-specific fiscal and labor dynamics.

### G-LIF-F02 — Partial vs general equilibrium wage claims

**Prompt:** Tag each wage study as partial (same education cell competition) or GE (capital adjustment + cross-education complementarity). Ottaviano-Peri: σ≈0.13–0.21 → +1.8% avg native vs Borjas −3% partial. Bound-Khanna: CS harmed, non-college +0.44% utility. Which fiscal memos cite partial elasticities as lifetime verdict?

**Retrodiction:** Would have flagged Borjas-style −8% <HS partial estimates incompatible with O-P −2.2% short run when occupational differentiation allowed.

**Negative space:** Lifetime fiscal synthesis cites wage losses without GE capital/complementarity or occupational reallocation.

### G-LIF-F03 — Occupational mobility vs education-at-arrival bucket

**Prompt:** Use Chiswick DP452 U-shaped ANU3 path: pre-migration prestige → arrival downgrade → partial recovery. Does NAS/education_bucket treat sheepskin at arrival as permanent skill proxy? Cross to Ottaviano-Peri occupational congruence 0.6–0.7. High-skilled visa (Business/Humanitarian) vs tied-migrant steepness.

**Retrodiction:** Would have warned that professionals arriving at 67.96 ANU3 score first job at 55.78 — lifetime NPV keyed on education alone misses assimilation dynamics and descendant occupational path.

**Negative space:** Descendant band in scenario ledger has earnings projection but no occupational downgrade/recovery state.

### G-LIF-F04 — Innovation spillover vs substitute crowd-out (H-1B)

**Prompt:** Decompose Bound-Khanna counterfactual: β≈0.23 innovation spillover raises aggregate native utility to ~0.21% vs 0.02–0.03% without; IT profits +0.61–0.70%; CS stayers −5.13% utility. Which lifetime studies count patent/innovation fiscal externality? Separate firm-owner surplus from worker incidence.

**Retrodiction:** Would have surfaced that killing spillovers collapses H-1B welfare case — fiscal ledger needs explicit innovation row or H-1B bucket stays incomplete.

**Negative space:** Federal positive NPV for college+ often assumes static payroll tax without IT sector profit/innovation feedback or CS distributional loss.

### G-LIF-F05 — State × education_bucket high-skill destination sorting

**Prompt:** Map H-1B/STEM concentration (CA/WA/NY/TX) vs <HS surge states. Ottaviano-Peri: 90% of natives have ≥HS and gain 0.7–3.4%. Bound-Khanna: non-college natives gain +0.44% utility from H-1B era GE. Build state×education_bucket×descendants cells — refuse national scalar.

**Retrodiction:** Would have prevented applying Mexico <HS state-local shock ledger to H-1B-heavy states where federal payroll and innovation channels dominate.

**Negative space:** State fiscal capacity literature (BoC Presidio) rarely splits high-skill tech hubs from border <HS counties within same state.

---

## G_legal_status_tax

### G-LIF-G01 — Tax-floor vs benefit-ban ledger split

**Prompt:** For any undocumented/refugee fiscal cell, decompose annual flows into (a) taxes paid regardless of status — payroll, sales, property pass-through, ITIN income tax — and (b) benefits legally barred. ITEP shows 35% of taxes fund SS/Medicare/UI with exclusion from benefits. Do not net to zero without explicit benefit-access matrix.

**Retrodiction:** Would have separated ITEP $96.7B tax floor from NAS benefit-cost rows before treating unauthorized as net-negative by default.

**Negative space:** Single net fiscal scalar assuming undocumented immigrants receive Medicaid/SNAP at citizen rates.

### G-LIF-G02 — Legal-status stock reconciler

**Prompt:** Before lifetime NPV, reconcile population stocks: Pew residual (14M 2023, upward undercount adjustment) vs ITEP/Warren (10.9M 2022) vs temp-protection subgroups (6M). Map each stock to work-authorization, ITIN filing, and benefit-eligibility states. Flag when model uses one stock for taxes and another for costs.

**Retrodiction:** Would have caught 2.5M headcount mismatch and 40% temp-protection heterogeneity before applying scalar Mexico undocumented parameters.

**Negative space:** Single undocumented count from one source year applied to all fiscal lines.

### G-LIF-G03 — ITIN compliance sensitivity band

**Prompt:** Treat federal income tax contribution rate as explicit sensitivity: ITEP base 60% (50–75% literature), json pessimistic −10.6% / optimistic +15.5% on grand total. Require any lifetime undocumented cell to show tax floor under {50%, 60%, 75%} before point estimate.

**Retrodiction:** Would have surfaced ITEP advocacy-adjacent microsim and CBO 50–75% band before locking undocumented federal income proxy.

**Negative space:** 100% compliance or 0% undocumented income tax as unstated extremes.

### G-LIF-G04 — Border-selection earnings updater

**Prompt:** When calibrating Mexico-origin lifetime cells, ask whether border-enforcement era shifted immigrant selection (Lozano-López: fewer older/high-ed women, higher earnings among survivors). Compare pre-2000 vs post-2000 arrival cohorts; do not use pooled Mexico <HS wage path for recent-surge entrants without selection flag.

**Retrodiction:** Would have linked IZA dp4898 positive selection channel to Mexico earnings donor cells before assuming uniform undocumented wage floor.

**Negative space:** Random emigration from Mexican wage distribution (no gender/cost selection).

### G-LIF-G05 — Tenure-split forward stock

**Prompt:** Pew 2023: 3.2M unauthorized <5 years vs 4.3M 18+ years. Split lifetime NPV into forward stock (short tenure, high flow uncertainty, temp protection) vs established stock (ITEP 16+ year median). Apply different discount horizons and legalization uplift ($40.2B/yr scenario) by tenure bucket.

**Retrodiction:** Would have prevented applying established-immigrant tax parameters to 2021–2023 parole-heavy inflow before forward-stock analysis.

**Negative space:** Steady-state unauthorized population with homogeneous tenure.

---

## H_refugee_mortality

### G-LIF-H01 — Refugee employment ramp calibrator

**Prompt:** For humanitarian/refugee lifetime cells, impose employment ramp from Dustmann et al.: −50pp year 0–3, −16pp unconditional steady-state gap, convergence ~15–25 years. Do not use economic-migrant employment rates in arrival year. Pair with Clemens 8-year U.S. fiscal breakeven as cross-check.

**Retrodiction:** Would have blocked flat employment assumption for parole/asylum entrants before forward-stock NPV.

**Negative space:** Refugees enter at native-average employment and earnings in year 1.

### G-LIF-H02 — Mortality forward-stock multiplier

**Prompt:** When projecting SS/Medicare NPV for Hispanic/refugee cells, require explicit life-table anchor: CDC 2021 Hispanic e₀=77.8, e₂₅=53.8, e₆₅=19.3 vs total-pop 76.4. Flag use of White NH or generic SSA tables without Hispanic adjustment. Note Medicare imputation uncertainty for Hispanic old-age mortality.

**Retrodiction:** Would have surfaced +1.4yr Hispanic e₀ vs total before applying uniform 75-year NAS horizon to Latin American humanitarian entrants.

**Negative space:** Single life table for all immigrant origins in lifetime model.

### G-LIF-H03 — Permanence vs subsidiary protection fork

**Prompt:** Dustmann: full GCR asylum → permanent settlement vs subsidiary/temporary protection → return incentive → lower host-country human-capital investment. For U.S. parole/TPS/asylum pending, branch lifetime NPV into {permanent, temporary, rejected} with different education/employment investment paths. EU ~10% recognition rate is lower-bound permanence probability.

**Retrodiction:** Would have split Pew 40% temp-protection subshare into permanence branches before scalar unauthorized NPV.

**Negative space:** All humanitarian entrants eventually permanent with identical integration path.

### G-LIF-H04 — Formal LMA breakeven clock

**Prompt:** Clemens WP496: formal labor market access is lever once refugees already present — avg U.S. refugee net fiscal positive at 8 years; work-access timing shifts breakeven (Marbach). For each humanitarian cell, declare LMA state {banned yr0-3, informal, formal} and map to Evans-Fitzgerald clock.

**Retrodiction:** Would have paired Clemens 8-year breakeven with Dustmann 50pp yr-3 employment ban before assuming humanitarian entrants are permanent fiscal negatives.

**Negative space:** Work authorization irrelevant to refugee fiscal path.

### G-LIF-H05 — Origin-area employment penalty mapper

**Prompt:** Dustmann Figure 9: MENA refugees −32.5pp conditional employment vs natives; other Africa/Asia also elevated. When modeling Syrian/Afghan/Venezuelan humanitarian cells, do not use Mexico <HS employment defaults — apply origin-area penalty decay schedule from EU evidence.

**Retrodiction:** Would have differentiated MENA humanitarian employment penalty from Mexico economic-migrant path in lifetime ledger.

**Negative space:** All humanitarian entrants share one employment gap regardless of origin.

---

## I_return_migration

### G-LIF-I01 — Inverse entry-earnings / assimilation growth band

**Prompt:** For each origin×education_bucket in origin_fiscal_scenario_2023, attach Duleep-Regets inverse elasticity band: unweighted -5.8 pp / weighted -9.7 pp / LDC +28.9 pp per $1,000 lower entry earnings (dp631 Table 1-3). Refuse cross-sectional assimilation slope as lifetime earnings path. Pair low entry with high growth before NAS NPV sign call.

**Retrodiction:** Would have blocked Borjas-style 'slow assimilation' from low entry earnings alone AND Clemens/NAS positive paths that assume flat growth across cohorts — dp631 resolves Chiswick-Borjas contradiction via inverse relationship.

**Negative space:** Lifetime fiscal models use entry earnings or a single YSM coefficient; no paired {entry level, entry-specific growth} cell.

### G-LIF-I02 — Country-of-origin convergence decay on scenario ledger

**Prompt:** Map dp8628 R² and CV convergence (country-origin explanatory power falls 22-91% over 10 years; cross-origin CV -13 to -55%) onto origin_fiscal_scenario rows. Flag origins where year-0 fiscal heterogeneity (avg_federal_net spread) is assumed permanent. Weight Mexico by convergence-adjusted earnings path, not entry-only snapshot.

**Retrodiction:** Would have surfaced that ACS 2023 origin weights × static avg_federal_net overstate Mexico-vs-Europe fiscal gap at year 10+ residence before any return-migration adjustment.

**Negative space:** Origin label treated as permanent fiscal modifier; no time-in-US decay of country-of-origin earnings premium.

### G-LIF-I03 — Return-migration / emigration selection sensitivity grid

**Prompt:** Build 3×3 attrition grid on lifetime NPV horizon: {low, base, high exit rate} × {failure-selective, random, success-selective outflow} × {years 0-5, 5-15, 15+ exit windows}. Anchor base rate: Warren-Kraly 75% emigrants in first 5 years; dp631 high/low emigration cohorts show similar inverse growth (emigration does not kill assimilation signal). No US fiscal micro — manual band only until CHCP acquired.

**Retrodiction:** Would have flagged G-LIF-D02 CHCP blocked gap and Dustmann survey §5.9 before treating SIPP annual proxy × 75-year horizon as full residence.

**Negative space:** Immigrant remains until death; selective return migration absent from NAS/Storesletten generational accounting.

### G-LIF-I04 — Skill-transferability vs immigrant-quality trap audit

**Prompt:** Audit lifetime memos equating low entry earnings with low 'immigrant quality' (Borjas cohort-quality frame). Cross-read dp631: entry earnings are poor human-capital stock measure when transferability τM<1 drives investment; dp8628: post-1965 LDC composition + family-reunification chain (Korean 75%→44% native parity) explains entry decline with rising growth. Separate {transferability, investment rate, exit hazard} before education_bucket NPV assignment.

**Retrodiction:** Would have prevented Mexico <HS scalar from inheriting 'declining immigrant quality' narrative while ignoring IHCI fast-growth offset and IRC A Mexican cohort selection exception.

**Negative space:** Single 'quality' dimension collapses transferability, ability, and selective return into entry wage.

### G-LIF-I05 — Cohort-dummy assimilation methodology falsifier

**Prompt:** For any pooled YSM regression or NAS cell using average assimilation rate: simulate dp8628 bias — recent low-entry cohorts get underestimated growth, high-entry cohorts overestimated when cohort dummies constrain growth. Require separate year-of-entry cohort paths or explicit inverse entry×growth interaction before lifetime NPV aggregation on acs_foreign_born_education_bucket_totals weights.

**Retrodiction:** Would have caught standard dummy-cohort assimilation estimates that dp631/dp8628 prove invalid when entry earnings trend down — directly relevant to building lifetime evidence warehouse assimilation parameters.

**Negative space:** Pooled assimilation coefficient applied to all entry cohorts regardless of entry-earnings level.

---

## J_admin_enforcement

### G-LIF-J01 — Enforcement budget ≠ per-migrant fiscal cost

**Prompt:** For each CBP/ICE appropriation line, tag as (a) fixed agency overhead, (b) volume-linked (encounters/beds/removals), (c) non-immigration mission (HSI fentanyl, trade). Never divide total CBP $19.8B or ICE $9.7B by immigrant stock without an explicit allocation rule. Cross-check to NAS/CBO lifetime tables that omit enforcement entirely.

**Retrodiction:** Would have blocked treating DHS budget growth as direct per-capita immigrant lifetime cost and surfaced NAS enforcement omission.

**Negative space:** Advocacy and restrictionist frames both treat agency budget as immigrant line-item without encounter/bed denominator.

### G-LIF-J02 — Recidivism-inflated flow vs unique-person stock

**Prompt:** Separate CBP apprehension/encounter counts (2.15M interdicted; 2.81 avg per recidivist) from unique-subject stock (1.42M) and from Pew/DHS unauthorized LPR residual. Where do lifetime models use flow denominators on stock numerators?

**Retrodiction:** Would have flagged repeat-encounter inflation before calibrating per-apprehension detention cost or fiscal scalars.

**Negative space:** Headline apprehension totals treated as unduplicated immigrant arrivals in media and some fiscal shorthand.

### G-LIF-J03 — Detention bed-day cost bridge

**Prompt:** Build marginal detention cost from ICE custody PPA ($3.27B FY25) ÷ ADP × 365 vs published bed rate ($187.48/day FY23). Compare to Alternatives to Detention ($360M FY25) and transportation/removal surge (+54% YoY). Which NAS/CBO lifetime paths include interior detention?

**Retrodiction:** Would have quantified interior custody as episodic federal cost absent from state-local K-12/shelter ledgers and NAS education NPV cells.

**Negative space:** Lifetime NPV studies silent on ICE bed-days while local shock ledgers silent on federal detention.

### G-LIF-J04 — LPR admission-class fiscal path decomposition

**Prompt:** For Mexico and top surge origins (Cuba, Venezuela, Haiti), sum LPR totals by admission class (immediate relative, family preference, employment, diversity). Map family-heavy paths to descendant-inclusive NAS rows vs employment paths to high-skill positive cells. Track Fam 2nd Mexico collapse 2005→2022 as legalization-channel shift under visa caps.

**Retrodiction:** Would have prevented treating Mexico as monolithic <HS unauthorized cell when 2022 LPR flow is 83k+ immediate-relative dominated.

**Negative space:** Origin labels in ACS fiscal scenarios collapse legal-status and admission-class heterogeneity.

### G-LIF-J05 — Border enforcement selection interacts with LPR mix

**Prompt:** Joint read: CBP interdiction rate + ICE ADP growth + Lozano-López border-enforcement selection (Round 9) + Mexico LPR class mix. Does rising interior detention correlate with positive earnings selection on observables while LPR family backlog lengthens?

**Retrodiction:** Would have linked Round 9 IZA dp4898 selection story to admin budget shift border→interior and LPR Fam2 collapse.

**Negative space:** Enforcement papers treat selection; budget docs treat dollars; LPR tables treat legal paths — rarely joint.

---

## K_incidence_bridge

### G-LIF-K01 — County incidence join audit

**Prompt:** For each origin in `origin_fiscal_scenario_2023`, trace PUMA→county via `puma_county_area_xwalk_2023` and join `school_finance_county_2023` + `chas_county_housing_stress`. Confirm `area_wtd_current_spend_per_pupil` is in the expected ~$8k–$30k band after the F-33 thousands fix, then bridge per-pupil to per-adult with full microsim adult denominators rather than the scenario subset.

**Retrodiction:** Would have caught both school spend ~$21 unit anomaly and the later Mexico denominator error (~437k scenario adults vs ~8.5M microsim adults) before using the local layer in a per-adult conclusion.

**Negative space:** National NAS education cost vs county-weighted ACS incidence

### G-LIF-K02 — Receiver-node episodic ledger

**Prompt:** Sum receiver_city_migrant_costs by node; compare to federal avg_federal_net for Mexico <HS in origin_fiscal_scenario. Build explicit episodic shock line (shelter/admin) outside 75-year NPV horizon.

**Retrodiction:** Would have separated Gould w33655 asylum shelter shock from Hanson composition weights.

**Negative space:** Lifetime NPV treats all fiscal incidence as smooth annual flows

### G-LIF-K03 — IRS migration × immigrant stock falsifier

**Prompt:** Join irs_migration_county_2022_2023 net inflow to ACS origin_puma stock changes. Does tax-base mobility co-move with immigrant share increases? If not, IRS migration is a weak falsifier for fiscal attribution.

**Retrodiction:** Would have flagged IRS county migration as income mobility not immigrant-specific fiscal shock.

**Negative space:** Tax return address change = immigrant fiscal burden

### G-LIF-K04 — State stage5 heterogeneity band

**Prompt:** From state_stage5_context_2023, build state_fips × education_bucket fiscal capacity quartiles (RPP, Medicaid, EL). Mexico composition weights × state shares should produce state-level lifetime bands, not one national scalar.

**Retrodiction:** Would have blocked national Mexico NPV scalar before stage5 context existed.

**Negative space:** National average fiscal incidence

---

## L_oecd_health_bridge

### G-LIF-L01 — Push-flow vs pull-fiscal attribution split

**Prompt:** For every lifetime fiscal claim citing 'immigration increases GDP/jobs': tag whether evidence is Ortega-Peri-style push-IV macro (scale, flat per-capita) or NAS/CBO micro ledger (education × transfers). Block synthesis that imports macro 1:1 employment response into individual NPV cells without capital-tax and public-goods grid.

**Retrodiction:** Would have separated Ortega-Peri Table 5 ΔL/L≈1 from NAS -$109k <HS before debate conflated 'immigrants grow GDP' with 'immigrants are net fiscal drains'.

**Negative space:** Standing frame: macro OECD panel = US lifetime fiscal scalar.

### G-LIF-L02 — MEPS annual cell → lifetime health NPV harmonizer

**Prompt:** Given meps_health_cost_module_2023 age×nativity×insurance cells: (1) map SIPP arrival age to age-band path; (2) apply survival/ Medicare eligibility; (3) discount at NAS 3% real over 75yr; (4) split payer columns (MCR/MCD/PRV/SLF). Never cite expected_mean_totexp23 as lifetime cost without horizon tag.

**Retrodiction:** Would have flagged scenario-composition memo disconfirmation #2 (FB working-age lower) AND elderly Medicaid reversal (L-009) before treating $600/yr bridge as −$109k NPV health line.

**Negative space:** Annual cross-section MEPS mean = lifetime immigrant health fiscal externality.

### G-LIF-L03 — Employer-recruitment channel vs stock composition

**Prompt:** When Winkelmann-style employer demand shows complementarity (languages, know-how; not wage undercutting), require separate high-skill recruited bucket in scenario ledger — do not pool with ACS stock <HS Mexico weights. Cross-check: firms with ≥1000 employees +32pp FHQE probability vs economy-wide 3.5% FHQE share.

**Retrodiction:** Would have blocked mapping IZA employer survey (IT/R&D 50-68% firm incidence) onto NAS average-recent-immigrant +$259k without education×visa path.

**Negative space:** All immigrants modeled as undifferentiated labor supply shock.

### G-LIF-L04 — Lifecycle Medicaid phase-shift audit

**Prompt:** Compare MEPS mean_totmcd23 by age_band for foreign_born vs us_born. Identify crossover age where fiscal sign flips. For lifetime NPV: stress-test with (a) working-age-only horizon to 65, (b) full 75yr with elderly weights, (c) uninsured→Medicaid transition scenarios. Flag any headline using only 25-44 cells.

**Retrodiction:** Would have surfaced L-007 (−42% working-age totexp) AND L-009 (+252% elderly Medicaid) as mandatory paired disconfirmation before Medicaid-drain advocacy.

**Negative space:** Health fiscal sign from single working-age snapshot.

### G-LIF-L05 — OECD policy-shock × health-bridge scenario grid

**Prompt:** Cross Ortega-Peri entry-law elasticity (−6%/reform) with SIPP scenario_ledger health columns. For each policy counterfactual (tighter entry, income-gap shock): re-weight origin cells AND recompute expected_mean_totmcd23 — immigration policy and health incidence treated as joint state, not independent scalars.

**Retrodiction:** Would have connected OECD law-reform flow shifts to which SIPP nativity/education cells enter the ledger, instead of static 98-cell health attach.

**Negative space:** Immigration policy affects counts only; payer incidence held fixed at 2023 MEPS.

---

## M_annual_npv_bridge

### G-LIF-M01 — Annual→NPV bridge with scope lock

**Prompt:** For cell {education_bucket, origin_label}: (1) pull avg_federal_net from origin_fiscal_scenario_2023; (2) pull NAS individual_npv for same education cell; (3) annuitize NPV at {2%,3%,4%} over 75y; (4) label MATCH/MISMATCH and list which costs are in NAS but not SIPP. Block synthesis if scopes differ.

**Retrodiction:** Would have blocked equating Mexico +$1,519/yr with NAS −$109k; flagged Lee-Miller dynamic vs cross-section mismatch.

**Negative space:** One annual proxy confirms or refutes lifetime NPV.

### G-LIF-M02 — Remittance private-layer offset

**Prompt:** Join World Bank remittance series to both (a) `origin_fiscal_scenario_2023` scenario-subset adults and (b) full `mexico_origin` microsim adults. Compare remittance per adult to `avg_federal_net` only after labeling the denominator.

**Retrodiction:** Mexico ~$66B remittances vs ~$664M scenario-subset federal net, or vs ~$12.9B full-stock federal net, before treating federal layer as household budget.

**Negative space:** Public fiscal ledger = complete household accounting.

### G-LIF-M03 — PAYG pension phase shift

**Prompt:** Map immigrant taxes vs benefits by age (Abel/Lee-Miller). Test if annual federal+ is lifecycle phase not lifetime verdict.

**Retrodiction:** Explains NAS school-age cost vs adult tax timing before working-age cross-section cited as lifetime proof.

**Negative space:** Lifetime NPV collapsed into current working-age cash flow.

### G-LIF-M04 — Policy-adjustment convention audit

**Prompt:** Extract whether generational-accounting PV requires future tax hikes for debt stabilization. Recompute under no-policy-change.

**Retrodiction:** Lee-Miller/NRC +$80k PV policy-adjustment reliance before citing generational surplus.

**Negative space:** Generational accounting as objective balance sheet.

### G-LIF-M05 — Surge cohort vs stock annualization

**Prompt:** Tag CBO surge federal path vs steady-state SIPP Mexico proxy SURGE vs STOCK. Forbid surge gains as lifetime NPV for 1990s stock.

**Retrodiction:** CBO $897B deficit reduction separated from Mexico ACS weights before layer laundering.

**Negative space:** One wave's federal gains applied to all stocks.

---

## N_school_unit_harmonization

### G-LIF-N01 — F-33 thousands gate

**Prompt:** Verify spend/enroll ratio is $8k–$30k/pupil; if median < $500 multiply expenditures by 1000.

**Retrodiction:** Caught ~$21 per-pupil bug before local K-12 lifetime assignment.

**Negative space:** Derived CSVs without unit sanity band.

### G-LIF-N02 — County vs origin per-pupil join audit

**Prompt:** CORR(county per_pupil, origin area_wtd per_pupil) after PUMA join; flag r<0.3.

**Retrodiction:** Failed pre-fix correlation; passes post-fix ~$20k band.

**Negative space:** Origin school cost without county anchor.

### G-LIF-N03 — K-12 lifetime cost band

**Prompt:** per_pupil × 13 years × school_age_share vs NAS education cost component.

**Retrodiction:** Pre-fix K-12 cost ~1000× too low to enter any local sum.

**Negative space:** School costs omitted because proxy numerically negligible (bug).

### G-LIF-N04 — NCES digest triangulation

**Prompt:** NCES 236.20 national per-pupil vs county F-33 weighted mean; reject if ratio outside [0.7,1.3] without RPP.

**Retrodiction:** ~$19k county median triangulated against NCES after unit fix.

**Negative space:** Single derived table without external scalar check.

---

## O_welfare_political

### G-LIF-O01 — Federal vs state-local ledger split enforcer

**Prompt:** Tag FEDERAL (CBO 60569) vs STATE_LOCAL (61256) vs LIFETIME_NPV (NAS). Reject unlike-ledger sums.

**Retrodiction:** Blocked federal $897B surplus dismissing NYC shelter + state/local $9.2B.

**Negative space:** One government budget.

### G-LIF-O02 — Welfare magnet destination sort

**Prompt:** Rank states by Medicaid per capita × immigrant PUMA weights; test magnet sort.

**Retrodiction:** Razin magnet theory linked to stage5 Medicaid heterogeneity before fiscal sign treated as immigrant-fixed.

**Negative space:** Fiscal type independent of destination policy.

### G-LIF-O03 — Tax-paid floor without benefit ceiling

**Prompt:** Pair ITEP taxes with SIPP transfer proxy for same legal-status band.

**Retrodiction:** Blocked $96.7B taxes rhetoric without transfer_outflow pairing.

**Negative space:** Tax contributions as net fiscal verdict.

### G-LIF-O04 — Political equilibrium skill-mix shift

**Prompt:** Map Razin voter blocs to DHS LPR class mix — family vs employment predicts education shift?

**Retrodiction:** Legal-path mix linked to education composition via political economy before static NAS weights.

**Negative space:** Skill mix exogenous to US policy.

---

## P_restriction_admin

### G-LIF-P01 — Enforcement admin ledger

**Prompt:** Sum CBP+ICE budgets per unauthorized (Pew stock); compare to ITEP tax per unauthorized.

**Retrodiction:** Missing admin ℓ layer before restriction advocacy used only NAS negatives.

**Negative space:** Restriction costless aside from lost immigrant surplus.

### G-LIF-P02 — Receiver episodic vs federal annual dominance

**Prompt:** N × avg_federal_net vs sum(receiver_city spending FY2023-24) for surge scale N.

**Retrodiction:** NYC+Chicago episodic rivals federal proxy for surge narrative.

**Negative space:** Federal surplus settles city shelter.

### G-LIF-P03 — Restriction changes cell not scalar

**Prompt:** 20% cut in `<HS` weight vs 20% cut in employment LPR — re-weight NAS cells.

**Retrodiction:** Enforcement selection + LPR mix before count-only restriction debate.

**Negative space:** Restriction = fewer identical immigrants.

### G-LIF-P04 — CBO restriction macro offset

**Prompt:** Invert CBO 60569 GDP/revenue channels for restriction sketch — federal cost of lost workers vs local savings.

**Retrodiction:** Federal GDP/revenue loss required in restriction debates citing only local shelter savings.

**Negative space:** Local relief from restriction has no federal offset cost.

---

## Q_stock_flow_denominator

### G-LIF-Q01 — Encounter ≠ stock

**Prompt:** Before any fiscal per-capita from border data: separate CBP encounter events, IDENT unique subjects, gotaways, and Pew/CIS unauthorized stock. Flag when flow denominators hit stock numerators.

**Retrodiction:** Would have blocked "10M illegals since Biden" → lifetime NPV without dedupe and outflow ledger.

**Negative space:** Encounter count treated as net new US residents.

### G-LIF-Q02 — Gotaway additive trap

**Prompt:** Gotaway sensitivity: add detected gotaways to stock only after subtracting repeat crossers, later apprehensions, and outflows. Never sum gotaways + encounters + Pew stock.

**Retrodiction:** Would have prevented double-counting ~2M gotaways on top of 14M Pew stock.

**Negative space:** Gotaways as permanent additive residents.

### G-LIF-Q03 — Birthplace ≠ legal status

**Prompt:** Map ACS birthplace (POBP) → Pew residual legal-status subcounts by origin before labeling "illegal Mexican" fiscal impact.

**Retrodiction:** Would have separated 8.5M Mexico-born adults from 4.3M Mexico-unauthorized stock.

**Negative space:** `origin_label=Mexico` equals unauthorized pool.

### G-LIF-Q04 — Education-mix mean ≠ median cell

**Prompt:** Any population-weighted NAS NPV scalar must ship with education-bucket share table; report `<HS` cell alongside weighted mean.

**Retrodiction:** Would have blocked "+$46k per Mexican" without 47% `<HS` at −$109k disclosure.

**Negative space:** Single lifetime scalar for heterogeneous education mix.

### G-LIF-Q05 — Pew vs CIS stock band

**Prompt:** Stock band sensitivity: Pew 14M vs CIS 15.8M unauthorized; apply Mexico ~30% share only to unauthorized-layer lines, not NAS education-mix rows.

**Retrodiction:** Would have bounded undercount debate to ~1–2M national band instead of +10M.

**Negative space:** One advocacy stock count applied to all fiscal layers.

### G-LIF-Q06 — Age-25 NPV benchmark ≠ current-stock NPV

**Prompt:** Before multiplying NAS Table 8-13 cells by ACS stock weights, verify whether the claim is about an immigrant entering at age 25, a recent-arrival cohort, or the current age-25–64 stock. If the warehouse lacks age-at-arrival/current-age NPV paths, label the result `synthetic_age25_benchmark`, not lifetime NPV of the stock.

**Retrodiction:** Would have blocked reading Mexico `+$387.7B` as actual stock lifetime NPV when the tensor only applies NAS age-25 cells to current ACS education weights.

**Negative space:** Current-stock population count treated as a cohort of new age-25 entrants.

---

## R_full_ledger_stack

### G-LIF-R01 — NAS scope lock before net claim

**Prompt:** Before citing any NAS NPV scalar: list {in: federal, state/local in cell, descendants, public goods, enforcement, courts, episodic shelter}. Block "net contributor" language until missing ℓ layers tagged.

**Retrodiction:** Would have blocked +$46k Mexico headline without stating descendants excluded and ICE/EOIR absent.

**Negative space:** NAS individual NPV treated as all-government lifetime net.

### G-LIF-R02 — School double-count guard

**Prompt:** Cross-check NAS cell (individual, no descendants) vs `school_burden_per_adult`. If NAS excludes kids' K-12, add school layer; if NAS includes immigrant own education only, do not subtract cross-section school twice.

**Retrodiction:** Would have separated individual NAS path from current-household school burden before merging layers; the interim `$771/yr` origin row is now withheld pending same-universe rebuild.

**Negative space:** Subtract school on top of NAS without checking descendant booking.

### G-LIF-R03 — Admin enforcement allocation rule

**Prompt:** Allocate CBP+ICE only via explicit rule: {per encounter, per bed-day, per unauthorized stock, fixed national}. Never divide total budget by stock without tagging fixed vs marginal share.

**Retrodiction:** Would have flagged $29.5B / 14M ≈ $2.1k/yr enforcement line missing from lifetime NPV.

**Negative space:** Full agency budget attributed to average immigrant.

### G-LIF-R04 — Justice/court layer

**Prompt:** Join EOIR case load × nationality to origin cells; express $/case or $/adult for asylum/backlog cohorts. Separate from NAS criminal-justice paths.

**Retrodiction:** Would have surfaced staged EOIR data with no Mexico rollup before claiming fiscal closure.

**Negative space:** Court costs assumed zero or inside NAS education cell.

### G-LIF-R05 — Publish stacked object only

**Prompt:** Export `v_full_fiscal_stack` with columns per ℓ and explicit overlap matrix. Headline = vector, never scalar.

**Retrodiction:** Would have required three-layer annual + lifetime + admin before any "Mexico net" thesis.

**Negative space:** Single number politics.

---

## S_restrictionist_steelman

### G-LIF-S01 — Restrictionist ledger tagger

**Prompt:** For each restrictionist claim, extract {ledger, cell, cohort, layer} before agreeing/disagreeing.

**Retrodiction:** Would have separated FAIR $150B (advocacy full ℓ) from NAS `<HS` (academic lifetime ℓ) from Gould 60% (episodic local).

**Negative space:** Restrictionist scalar applied to all immigrants.

### G-LIF-S02 — Subgroup row requirement

**Prompt:** Map BGH black employment/incarceration results to required tensor rows — block education-only NAS for distributional harm claims.

**Retrodiction:** Would have blocked inferring all native harm from immigrant `<HS` NPV alone.

**Negative space:** Distributional politics from education-average cells.

### G-LIF-S03 — FAIR vs ITEP vs Pew reconciliation

**Prompt:** Build stock and tax reconciliation before citing FAIR or ITEP in warehouse scalars.

**Retrodiction:** Would have flagged FAIR 15.5M stock vs Pew 14M before $8,776/per-capita.

**Negative space:** Advocacy ledger as empirical fact.

### G-LIF-S04 — Episodic vs lifetime dominance

**Prompt:** Gould shelter $ vs NAS lifetime for same surge cohort — which ℓ drives local political backlash?

**Retrodiction:** Would have connected NYC $3.7B to restrictionist wins independent of Mexico +$46k mix.

**Negative space:** Lifetime NAS settles shelter debate.

### G-LIF-S05 — Razin policy co-evolution

**Prompt:** How does welfare eligibility / magnet policy change fiscal sign of same ACS immigrant cell?

**Retrodiction:** Would have modeled M5 political equilibrium before static NAS weights.

**Negative space:** Fiscal type invariant to destination policy.

### G-LIF-S06 — National cell before Card

**Prompt:** Before citing Card spatial null, require national education×experience cell regression or document spatial attenuation factor (Borjas w9755: ~⅔ hidden).

**Retrodiction:** Would have blocked Mariel → "immigration harmless" without w11610 migration offset.

**Negative space:** MSA coefficient as sufficient statistic for national harm.

### G-LIF-S07 — Wage decomposition triple

**Prompt:** Decompose immigration wage impact into {log weekly, log annual, weeks worked} — does harm operate on intensive or extensive margin?

**Retrodiction:** Would have surfaced w9755 10% supply → −4% weekly but −6.4% annual + −3.7pp weeks.

**Negative space:** Weekly wage elasticity alone.

### G-LIF-S08 — Native migration offset

**Prompt:** For local labor-market immigration regressions, estimate native in/out-migration response; compare implied attenuation to Borjas w11610 40–60% band.

**Retrodiction:** Would have explained Card-Borjas gap as equilibrium diffusion not zero effect.

**Negative space:** Local wage coefficient = structural national elasticity.

### G-LIF-S09 — Subgroup triple margin

**Prompt:** For distributional harm claims, require {wage, employment, incarceration} rows — BGH shows black employment/incarceration elasticities >> white.

**Retrodiction:** Would have blocked NAS `<HS` NPV → "harms all natives equally."

**Negative space:** Education-average fiscal cell as subgroup harm proxy.

### G-LIF-S10 — HUD PIT decomposition

**Prompt:** Split homelessness into {sheltered asylum-attributable, sheltered other, unsheltered}; block Gould 60% → "all homelessness."

**Retrodiction:** Would have separated NYC episodic shelter from lifetime Mexico NPV.

**Negative space:** Affordability-only homelessness narrative.

### G-LIF-S11 — Orrenius dual-scenario gate

**Prompt:** Every NAS fiscal citation must show avg-cost AND marginal-cost rows plus federal/state split (Orrenius Table 1 pattern).

**Retrodiction:** Would have blocked restrictionist use of avg-public-goods negative without marginal federal +$963.

**Negative space:** Single NAS table cell in politics.

### G-LIF-S12 — Razin policy vector shock

**Prompt:** Simulate {τ, μ, σ} change on fiscal sign of fixed ACS immigrant cell (Razin w15597 Markov PE).

**Retrodiction:** Would have linked welfare generosity to skill composition before static lifetime NPV.

**Negative space:** Fiscal type invariant to immigration/welfare policy.

### G-LIF-S13 — Mobility-regime tag

**Prompt:** Welfare-magnet claims require {free vs restricted} mobility regime tag — EUR evidence does not transfer to US selective policy (Razin-Wahba w17515).

**Retrodiction:** Would have blocked "Europe proves magnet" without regime control.

**Negative space:** Cross-regime magnet inference.

### G-LIF-S14 — Secular supply forecast

**Prompt:** Pair Hanson w23753 secular low-skill decline + Pew stock series before "flooding" rhetoric; encounters ≠ residents.

**Retrodiction:** Would have deflated Biden 10M encounter → stock panic against flat Mexico unauthorized.

**Negative space:** Flow headline as permanent stock shock.

### G-LIF-S15 — Intergenerational welfare channels

**Prompt:** For intergenerational fiscal/welfare claims, separate {parental welfare receipt, ethnic environment externality, own earnings path} — Borjas w6175: ~80% of ethnic welfare gap transmits.

**Retrodiction:** Would have blocked attributing second-gen costs to first-gen immigrant NPV alone.

**Negative space:** Immigrant lifetime NPV = ethnic externality.

---

## T_immigrationist_steelman

*Benefit-side lenses — the mirror of S. Added 2026-06-23. The 6 external papers were acquired to the corpus 2026-06-24 (no longer placeholders) — see immigration-acquisition-gaps-2026-06-24.md. See also immigration-fiscal-welfare-ledger-map.md.*

### G-LIF-T01 — Level-not-mean / additive-output gate

**Prompt:** Whenever a claim infers harm from 'immigrants lower the average education / wage / GDP-per-capita', block it until restated in LEVELS: did total output rise, and is any specific incumbent mechanically poorer, by what channel? A falling mean with rising total and no named incumbent loss is a composition artifact, not a welfare loss.

**Retrodiction:** Would have caught that 'the average American is more educated than the average LATAM entrant, therefore harm' confuses the mean with welfare. Output is additive; adding a $35k worker to a $70k-mean economy lowers the mean while raising total output and making no incumbent mechanically poorer. Reconciles rising aggregate GDP with falling GDP-per-capita-of-the-average.

**Negative space:** Standing frame treats national average human capital as a welfare target that below-average entrants 'dilute'.

### G-LIF-T02 — Place premium / migrant-welfare ledger (whose welfare counts)

**Prompt:** For any 'is immigration good' verdict, name the welfare boundary explicitly: incumbent-natives-only, all-residents-incl-immigrants, or global. Then add the migrant's own gain — the place premium, the multiple a observably-identical worker earns in the US vs origin — as a labelled ledger row. A verdict that zeroes it must say so.

**Retrodiction:** Would have surfaced that every NAS / Borjas fiscal ledger is incumbent-only and silently sets the LARGEST welfare term to zero: the 2–15× place premium on the migrant's own earnings (Clemens-Montenegro-Pritchett). 'Net negative' on the incumbent-fiscal ledger is consistent with hugely net-positive on the resident or global ledger.

**Negative space:** Cost ledgers count only the incumbent taxpayer's balance; the immigrant's own welfare gain is structurally invisible.

### G-LIF-T03 — Consumer-surplus / non-traded price channel

**Prompt:** For low-skill labor inflows, add the native real-income gain from lower prices of immigrant-intensive non-traded services (childcare, food prep, construction, housekeeping, gardening). Quantify via the immigrant-share elasticity of local service prices. This benefit sits outside BOTH the fiscal ledger and the wage-competition ledger.

**Retrodiction:** Would have flagged that low-skill immigration's downward effect on non-traded service prices (Cortes 2008 JPE) is a real-wage gain to native consumers, absent from the fiscal NPV and from the Borjas wage ledger — natives who don't compete with immigrants gain as consumers.

**Negative space:** Cost ledgers count fiscal + wage competition; the consumer-price benefit channel is unrepresented entirely.

### G-LIF-T04 — Entrepreneurship / labor-demand offset to the supply shock

**Prompt:** Before treating immigrants as pure labor SUPPLY (substitutes in a fixed job pool), net out the labor DEMAND they create: firm-formation and job-creation rates. Add immigrant founding share as a demand row that partly offsets the substitution in any supply-shock claim (e.g. G-LIF-B02).

**Retrodiction:** Would have caught that the supply-shock framing is one-sided: immigrants found firms at above-population rates and are net job CREATORS, not just takers (Azoulay-Jones-Kim-Miranda 2022) — the lump-of-labor assumption behind 'they take jobs' is the unnamed premise.

**Negative space:** Supply-shock lenses count immigrants as competitors in the labor pool; their firm-formation / labor-demand contribution is uncounted.

### G-LIF-T05 — PAYG demographic dividend / SS–Medicare solvency

**Prompt:** For payroll-funded PAYG programs (OASDI, Medicare HI), credit immigrants' younger age structure: they pay in for decades before claiming, improving the dependency ratio and the trust-fund actuarial balance. Add the SSA actuary's immigration sensitivity (higher net immigration narrows the OASDI deficit) as a federal benefit row; for unauthorized workers add the SSN-mismatch contributions they fund but cannot claim.

**Retrodiction:** Would have surfaced that the static fiscal 'cost' of low-skill immigrants understates federal payroll contributions: the SS Trustees explicitly model higher immigration as IMPROVING OASDI solvency, and the Earnings Suspense File holds large unauthorized contributions never claimed back.

**Negative space:** Static annual-balance ledgers net taxes vs services in a year; the PAYG dynamic — young contributors subsidizing the existing old — is a cross-cohort benefit they miss.

### G-LIF-T06 — GE capital-adjustment wage restoration

**Prompt:** For any short-run native-wage-loss claim, require the long-run general-equilibrium counterpart: immigration raises the return to capital → induces investment → capital stock adjusts → the aggregate native wage effect returns toward zero (one-sector neoclassical). Tag every wage number SR (capital fixed) or LR (capital adjusted); never compare across the tag.

**Retrodiction:** Would have reconciled Borjas's short-run low-skill wage hit with the near-zero-to-positive long-run aggregate effect once capital adjusts (Ottaviano-Peri) — structurally the same omitted-capital-response mechanism as the capital-tax flip (G-LIF-A01), applied to wages instead of taxes.

**Negative space:** Wage-shock lenses (B02–B06) mostly hold capital fixed; the capital-deepening response that restores wages is the missing GE step.

### G-LIF-T07 — Positive selection on unobservables

**Prompt:** Within an education×origin cell, do not treat the immigrant as the cell-average native: migrants are positively selected on unobservables (health, drive, risk-tolerance) — the migration decision is itself a filter. Apply a selection wedge before importing native cell-average welfare-use / earnings onto immigrants.

**Retrodiction:** Would have explained immigrant earnings catch-up and below-predicted welfare take-up: within-cell positive selection (the 'healthy migrant effect' + ambition filter) means the average same-education native overstates immigrant transfer use and understates immigrant earnings growth.

**Negative space:** Fiscal ledgers apply native cell-average behavior to immigrants; the selection wedge (immigrant ≠ average same-education native) is unmodeled.

### G-LIF-T08 — Fiscal externality ≠ exclusion (welfare-economics framing)

**Prompt:** A negative net fiscal transfer is a TRANSFER (a financed externality), not a deadweight loss. Before treating −$X NPV as a reason to exclude, ask the first-best welfare-economics question: is the right response to TAX the surplus the migrant generates (Pareto-improving) rather than EXCLUDE the person (which forgoes the surplus)? Separate 'who pays' from 'is there a net gain to allocate'.

**Retrodiction:** Would have reframed the −$150k <HS lifetime NPV: if the migrant adds aggregate surplus (the immigration surplus is positive even in Borjas) AND a fiscal cost, the cost is a financing/redistribution problem, not a net loss — exclusion forgoes the surplus to avoid the transfer. The sign of the surplus and the sign of the fiscal balance are separable.

**Negative space:** Cost ledgers treat the fiscal deficit as terminal harm; the welfare-economics distinction between a transfer-to-be-financed and a deadweight loss is absent.

## U_source_incentive_meta

*Meta-epistemic lenses (source incentive / against-interest / media-selection). Symmetric by construction. Added 2026-06-23. Applied pass: immigration-source-incentive-regrade-2026-06-23.md.*

### G-LIF-U01 — Source-incentive / against-interest credibility audit

**Prompt:** For every source backing a claim, tag {outlet_type, prior_lean, finding_direction}. Set against_interest = the finding cuts OPPOSITE to the source's own prior (restrictionist source → benefit finding; expansionist source → cost finding). Re-weight: govt-nonpartisan (CBO/Census/NAS/SSA) = high baseline; academic = mid; advocacy = low, and ×1.5 if against-interest, ×0.7 if advocacy confirming its own prior. Re-rank claims by incentive-adjusted credibility, NEVER by citation count or media prominence (which inherit the selection bias). The rule MUST down-weight your own side's advocacy too, or it is not the audit — it is the bias.

**Retrodiction:** Would have shown the 'immigrants are net contributors' headline leans on with-interest expansionist advocacy (ITEP/CAP/Cato) that this rule deflates — AND symmetrically that FAIR/CIS high-cost numbers are with-interest restrictionist advocacy it also deflates; while the claims that SURVIVE are the against-interest ones (Borjas deriving a positive aggregate surplus; NAS, the establishment panel, publishing the <HS lifetime cost) plus the nonpartisan baselines (CBO federal, Census stock).

**Negative space:** Claims are weighted by citation count / media prominence, which directly inherit the left-skewed selection of which findings get written up; the source's incentive structure is unmodeled.

### G-LIF-U02 — Media-selection vs primary-table gap

**Prompt:** For any claim sourced to a news/secondary write-up, locate the PRIMARY table (NAS panel page, CBO appendix, the regression table) and check whether the headline preserved the sign, the cell, and the caveats. Tag the gap. Prefer the primary number; treat the journalist framing as a selection signal, not evidence.

**Retrodiction:** Would have caught that the NAS <HS lifetime-cost table and the CBO state-local cost rows exist in the primary documents but are systematically under-reported in secondary coverage relative to the 'immigrants grow GDP' framing — the gap is selection, not the absence of the finding.

**Negative space:** Secondary coverage is treated as a faithful summary of the primary source; the selection/flattening step is invisible.

## V_deep_roots_long_run_skeptic

*Long-run cultural/institutional-transmission skeptical lenses — the LONG-RUN complement to S's short/medium-run fiscal cost (and the opposite pole to T's benefit side). Added 2026-06-24. All 6 external papers acquired to corpus (corpus:// URIs in the cluster JSON). Carries its own disconfirmation by construction: V08 is an explicit assimilation null (verified in-warehouse), V06 is flagged CONTESTED (stress-test only). [FRAMING-SENSITIVE] throughout; national-IQ data-quality fights route to the iq-sex-differences sister repo. See immigration-acquisition-gaps-2026-06-24.md + immigration-fiscal-welfare-ledger-map.md.*

### G-LIF-V01 — Deep-roots / ancestry-adjusted development

**Prompt:** Before treating an origin group's economic outcomes as set by current host institutions, ask what the deep-roots literature predicts: long-run development correlates with the ANCESTRY-weighted history of a population (early state experience, agricultural transition, technology adoption) more than with the geography it currently occupies. Separate traits that travel WITH people across borders from traits that stay with PLACES. *(Spolaore-Wacziarg; Putterman-Weil)*

**Retrodiction:** Would have flagged that cross-country development gaps shrink but do not vanish when you ancestry-adjust via the Putterman-Weil post-1500 migration matrix — a measurable component of what looks like 'bad geography' travels with populations. That is the long-run channel a first-gen fiscal/crime ledger is blind to.

**Negative space:** Fiscal and crime ledgers are proximate and first-generation; the deep, ancestry-linked component of long-run development sits outside their window.

### G-LIF-V02 — Cultural transmission / epidemiological approach

**Prompt:** Identify cultural traits (work norms, female labor supply, fertility, saving) by the EPIDEMIOLOGICAL method: compare 2nd-generation immigrants from different origins under the SAME US institutions. Origin differences that persist under fixed institutions are transmitted CULTURE, not environment. *(Fernández-Fogli)*

**Retrodiction:** Would have shown that 2nd-gen female labor supply and fertility still track the origin country's values even holding US institutions constant — 'the children are just Americans' overstates assimilation for the traits that drive labor supply and dependency.

**Negative space:** Cost and benefit ledgers alike attribute 2nd-gen behavior to host institutions; the transmitted-culture component is uncounted.

### G-LIF-V03 — Inherited trust as a slow social-capital channel

**Prompt:** For outcomes that depend on social capital (contract enforcement, public goods, low corruption), credit or debit the INHERITED TRUST the inflow carries. Use the trust of descendants-of-immigrants as a time-varying, origin-linked measure. *(Algan-Cahuc; DISCONFIRM: Eder replication, Muller-Torgler comment)*

**Retrodiction:** Would have surfaced that inherited trust of US immigrant descendants is shaped by origin country and arrival timing, and predicts cross-country growth — a slow social-capital effect the static ledger omits. Must survive the replication critiques before it is load-bearing.

**Negative space:** Annual net-fiscal and first-gen crime measures cannot see a social-capital stock that shifts over generations with the origin-mix.

### G-LIF-V04 — Ethnic capital / slow assimilation brake

**Prompt:** Do not assume the 2nd generation regresses to the host mean in one step. Skills transmit via BOTH parental inputs AND the average skills of the parents' ethnic group (ethnic capital); this slows convergence beyond the simple intergenerational model. *(Borjas 1992/1995)*

**Retrodiction:** Would have caught that 'the kids catch up' overstates convergence speed: ethnic capital keeps low-skill origin groups below the host average for two to three generations rather than one — the missing debit on the dynasty-optimism ledger (T, ledger-map).

**Negative space:** The positive dynasty/2nd-gen ledger prices in fast convergence; ethnic-capital persistence is the brake it omits.

### G-LIF-V05 — The new economic case for restrictions (institutional-quality externality)

**Prompt:** State the strongest LONG-RUN restrictionist argument in its own terms, then ASSESS it: large inflows from low-productivity-institution origins could transmit those institutions and lower host TFP — a dynamic externality that, if real, swamps any static fiscal gain. How strong is transmission, how fast does it decay, how elastic are host institutions to immigrant share? *(Clemens-Pritchett pose AND assess it)*

**Retrodiction:** Would have named the one argument that, if true, dominates the ledger — and applied Clemens-Pritchett's own verdict: the channel is theoretically coherent but the institutional elasticities needed to make restriction welfare-optimal are not in the data at observed margins. A coherent worry, not a quantified cost.

**Negative space:** Both S (fiscal) and T (benefit) work in the first-gen window; the institutional-transmission externality is the missing long-run term the restriction case rests on.

### G-LIF-V06 — National cognitive/human capital of origin (CONTESTED — stress-test, do not assume)

**Prompt:** The hardest-edged composition argument: national average cognitive-skill indices predict productivity across countries, so the origin-mix of an inflow could shift host human capital. STEELMAN TO STRESS-TEST, NOT A PREMISE. Three caveats fire automatically: (1) the underlying national-IQ data (Lynn-Vanhanen) is low quality; (2) the cross-country correlation is heavily confounded (institutions, health, schooling, colonial history); (3) a national-average correlation licenses NO individual or first-gen inference (ecological fallacy). *(Jones-Schneider BACE; Jones 'Culture Transplant' book)*

**Retrodiction:** Would have both surfaced the Jones-Schneider result AND immediately attached the data-quality, confounding, and ecological-inference caveats that make it unusable for any individual, first-gen, or short-run immigration claim — preventing the over-extension this channel invites.

**Negative space:** The composition-of-human-capital channel is real in the growth literature but the most frequently misused; absent from the ledgers, and when invoked, almost always over-stretched. Routes to `~/Projects/iq-sex-differences` for the data-quality verdict.

### G-LIF-V07 — Ancestral/cultural/linguistic distance as a diffusion barrier

**Prompt:** Add ancestral, cultural, and linguistic DISTANCE between origin and host as an integration-cost channel: greater distance slows diffusion of technology/norms/institutions and historically raises friction. A COMPOSITION effect — closer-ancestry inflows integrate more cheaply than distant ones of the same size. *(Spolaore-Wacziarg 'Ancestry, Language and Culture')*

**Retrodiction:** Would have predicted integration costs and inter-group frictions scaling with ancestral/cultural distance, not immigrant numbers alone — reframing 'how many' debates as partly 'from where', a composition question the headcount ledger cannot pose.

**Negative space:** Fiscal/crime ledgers price the LEVEL of inflows; the distance-dependent integration cost (a composition effect) is unrepresented.

### G-LIF-V08 — Self-rebuttal: assimilation refutes STRONG persistence (constructive null)

**Prompt:** Before reading V01–V07 as transmission-is-destiny, apply the assimilation NULL. US immigrants and descendants assimilate fast historically (Abramitzky-Boustan), immigrant crime converges DOWN not up (the 1870–2020 incarceration gap; the Texas DPS rates this repo built), and origin persistence DECAYS each generation. V01–V07 bound a LONG-RUN, AVERAGE, COMPOSITION concern — they do NOT license first-gen, individual, or fixed-trait claims. *(Verified in-warehouse: undocumented violent-crime rate 0.41–0.48× true native-born, 2012–2018, no trend to parity.)*

**Retrodiction:** Would have stopped every deep-roots lens above from being misread as a first-gen or individual claim: the same micro-data showing some origin persistence ALSO shows rapid regression toward the host mean and a 150-year immigrant CRIME ADVANTAGE. Partial, decaying transmission — not destiny.

**Negative space:** A steelman without its null is a polemic. This lens is the built-in disconfirmation that keeps cluster-V honest and prevents long-run average claims from being laundered into first-gen or individual ones.
