# Research Coverage Matrix — "every possible research" bounded honestly (2026-06-25)

**Trigger.** Operator goal: *get every possible research on this topic across sociology, urbanism, economics, policy, crime — and get the datasets.* This doc is the **frame** (constitution principle #5, "name the frame"): it states per-domain what is **saturated** vs a **genuine frontier**, so "every possible" is a bounded, falsifiable claim, not a vibe. Filled by a 4-agent parallel research+acquisition pass; the parent integrates.

Instrument note: politically charged topic, LLM-assisted corpus, left-tilted academic field. Disconfirming / against-interest evidence is weighted as **higher-information** throughout (see `notes/llm-bias-caveat.md`).

## The frame — where the repo actually is, by the 5 named domains

| Domain | State | Evidence of saturation / gap |
|--------|-------|------------------------------|
| **Economics** (fiscal NPV, wage, labor supply) | **SATURATED — spine** | Fiscal ledgers, country tensor, microsim, Borjas supply-shock panel (1980-2023), E-Verify wage TWFE, assimilation profile. 57-dataset roadmap returned VEIN:SATURATED on fiscal axes. *Exception:* 4 named wage/fiscal **disconfirmers** never fetched → econ-disc agent. |
| **Crime** | **STRONG — recent** | Light TX (in-data), BJS SPI, SCAAP, INT-06 status spine, 188-spec curve (direction robust). Corpus has Light 2020, Abramitzky 2024 incarceration, homicide-disentangle 2020. Frontier is thin (enforcement/sanctuary *policy* evals) → folded into policy agent. |
| **Policy** (enforcement, legalization, sanctuary, refugee) | **PARTIAL — frontier** | E-Verify wage side + surge/EOIR covered; but DACA/IRCA legalization evals, Secure Communities/287g crime evals, sanctuary-crime nulls, refugee fiscal trajectories under-weighted. Several OA papers *identified but unfetched* (paper-gaps memo). → policy agent. |
| **Sociology** (assimilation, cohesion, enclaves, segregation) | **PARTIAL — frontier** | Corpus already strong on segmented-assimilation (2024/25), Putnam West-EU replication, ethnic networks/capital, deep-roots cluster-V. Gap: the trust **meta-analyses** (van der Meer-Tolsma), CILS/NIS datasets, intermarriage/linguistic indices, generational segregation. → socio agent. |
| **Urbanism** (housing incidence, sorting, agglomeration) | **THIN — biggest gap** | No dedicated urban frame. Saiz rent screen + receiver-node shelter stress only. No MSA rent × immigrant panel (4 warehouse theories pending on it). Housing-incidence ledger flagged missing by both red-team models. → urban agent. |

**Honest headline:** "every possible research" is *not* an open-ended infinite search. Economics and crime are at diminishing returns (saturated/strong). The real, fundable frontier is **urbanism > sociology > policy-disconfirmers**. This pass expands those three and executes the already-scouted econ disconfirmers.

## Corpus baseline (immigration-relevant, already in `research-mcp` corpus as of dispatch)

Already held — agents must NOT recount these as "new acquisitions":
- **Crime:** Light et al. 2020 (TX, PNAS); Abramitzky-Boustan-Jácome-Pérez-Torres 2024 (incarceration gap 1870-2020); homicide-incarceration-by-status TX 2020; "migrant regularization reduces crime" 2025.
- **Sociology:** Putnam-2007 West-European trust replication (2011); "Ethnic networks foster economic integration of refugees" (2019); "Segmented assimilation, then and now" (2025); "Assimilation Theories in the 21st Century" (2024); ethnic-identity transmission, Mexican Americans (2025); Borjas "Ethnic Capital & Intergenerational Mobility" (1992); "Inherited Trust and Growth" (2010); Guiso-Sapienza-Zingales culture; "How Deep Are the Roots of Economic Development?" (2012).
- **Economics:** Peri-Yasenov "Labor Market Effects of a Refugee Wave" (Mariel synthetic control, 2018) — **already in**, so econ-disc's Mariel delta = Clemens-Hunt 2019 + Borjas 2017 reappraisal; Ottaviano-Peri "Rethinking the Effect of Immigration on Wages" (2012); Cortes "Low-skilled immigration on US prices" (2008); "Immigration & Entrepreneurship in the US" (2020); Clemens place-premium (2008); "The new economic case for migration restrictions" (2019).

## Dispatch (4 parallel researcher agents, background; this run)

| Agent | Axis | Memo (on return) | Key deltas it must hit |
|-------|------|------------------|------------------------|
| `socio` | Sociology / cohesion | `immigration-sociology-frontier-2026-06-25.md` | van der Meer-Tolsma trust meta; CILS/NIS datasets; intermarriage/linguistic; generational segregation |
| `urban` | Urban & housing econ | `immigration-urbanism-frontier-2026-06-25.md` | **MSA rent × immigrant panel dataset map**; Saiz-2007 rent incidence; Card tipping/native-mobility; agglomeration |
| `policy` | Policy/enforcement | `immigration-policy-frontier-2026-06-25.md` | fetch 5 OA crime/enforcement papers; DACA/IRCA evals; Secure Communities/287g crime nulls; refugee fiscal |
| `econ-disc` | Econ disconfirmers | `immigration-economics-disconfirmers-2026-06-25.md` | Clemens-Hunt+Borjas-2017 Mariel; Dustmann-Frattini UK; US dynamic NPV + CBO 2024; Cato TX convictions |

## Integration log (parent fills as agents return)

### ✅ socio — returned 2026-06-25 (`immigration-sociology-frontier-2026-06-25.md`)
Intern-rule spot-check: all 4 load-bearing DOIs `resolve_doi`-verified to exact title/journal/year/author (citations real). Full-text fetch of the 2 Annual-Review meta-analyses failed (not on Sci-Hub; OA-repo URLs not downloadable by the tool) — citations verified, full text not corpused; OA links live in the memo.
- **Caveat — low *net-new* corpus yield:** most of socio's "8 saved" were ALREADY in corpus from prior cluster-V work (Drouhot 2024, Kasinitz 2025, Lancee-Dronkers 2011, Martén 2019, Duncan-Trejo 2025). The sociology *papers* frontier is closer to harvested than the brief assumed.
- **Genuine new value (3 things):**
  1. **Trust/cohesion meta-analyses** (Dinesen 2020; van der Meer-Tolsma 2014) — a settled, quantified, two-sided verdict the repo entirely lacked: diversity→trust effect is **real but modest (r ≈ −0.0256, s.e. .0044), local (neighbor-trust), US-stronger than EU, NO spillover to generalized trust**. Kills both the alarmist and the "Putnam debunked" poles. `[FRAMING-SENSITIVE]`: is −0.026 trivial or material? values call.
  2. **Ethnic-attrition method warning** (Duncan-Trejo 2025) — self-ID-coded later-generation tests **understate assimilation** for high-intermarriage groups (Mexicans esp.) because assimilated descendants stop self-IDing. **Directly threatens the repo's pending CPS 2nd-gen-by-origin test (pre-reg P1)** → must use *parental* birthplace, not self-ID. Highest-value item: it's a correction to our own method.
  3. **GSS trust-by-nativity = cheapest buildable-now test** (BORN/PARBORN × TRUST/FAIR/HELPFUL, fully public) — tests immigrant trust *convergence* with zero gating.
- **Dataset cards (→ roadmap, batched):** CILS (ICPSR 20520, public), NIS (38031/38061, tiered), Add Health (tiered; networks restricted), GSS-by-nativity (public, build now), ACS segregation indices (public, additive compute).

### ✅ urban — returned 2026-06-25 (`immigration-urbanism-frontier-2026-06-25.md`) — STRONGEST yield
Intern-rule spot-check: load-bearing new paper **Wilson & Zhou (2026), Dallas Fed WP2607** verified at **primary** (read the PDF byline directly — 1.2 MB/65pp in scratchpad). Note: CrossRef mis-listed the first author as "Lewis"; the PDF title page says **Daniel J. Wilson** — primary beats the proxy, agent's citation correct. Other 3 key DOIs (Saiz-Wachter, Hsieh-Moretti, Jaeger-Ruist-Stuhler) all resolve exact.
- **Single highest-value find — Wilson-Zhou 2026:** first CAUSAL post-2020 housing estimate. UIWF = 1% of initial employment → **+2.2% house prices, +1.4% rents**, permit/supply response **null**, labor-income-per-capita and transfers FELL. Explains ~30% house-price / ~20% rent growth in avg MSA. Outcome var = Zillow ZORI (validates the dataset map). Directly resolves E-cluster E-001/E-003/E-004 with real magnitudes; also feeds the FISCAL ledger (fell income/transfers).
- **THE dataset map (answers "get the datasets") — MSA rent × fb-share × elasticity panel, 7 components, all URLs live:**
  - NEW to acquire: **Zillow ZORI/ZHVI** (public CSV, the primary rent panel), **WRLURI2018** (one-time DL), **Geocorr2022 PUMA↔CBSA crosswalk** (resolves the Saiz-memo unit-mismatch), **LODES/LEHD** (new spatial-mismatch axis).
  - Already in repo: Saiz-2010 elasticity, HUD FMR/SAFMR, BPS permits, ACS housing-by-nativity.
  - **1/10 build (highest-ROI):** Zillow ZORI + ACS B05002/B25064 by CBSA 2015-24, regress Δrent on Δfb-share × Saiz elasticity. Replicates Wilson-Zhou sign at ~zero cost. **This is the concrete answer to HUMAN.md #2 ("build the housing panel?") — now fully spec'd.**
- **New frames:** native-flight *scale-dependence* (Card MSA-null → Saiz-Wachter neighborhood-flight → Boje-Kovacs 2024 building-level) resolves the Card-Borjas tension by scale; Hsieh-Moretti supply-misallocation *bridge* (same elasticity lever governs both rent cost AND foregone agglomeration benefit).
- **Benefit-side anchor:** Burchardi et al. w27075 — causal +innovation AND +native (incl. non-mover) wages, rules out the flight confound. A housing-only urban frame is a one-sided ledger.
- **6-point disconfirmation** (proper, weighted higher): timing/geography don't line up (Harvard JCHS, Yale Budget Lab — rents surged 2021 when inflows were modest); aggregate small (Cabral-Steingress ~1.3% of a 17% rise); sign can flip negative (Sá UK, high-income native out-migration); native flight overstated by conventional methods (Moraga); rent-to-income equalizes (Greulich); benefit ledger is causal. Net frame: **bounded, real-but-secondary cost concentrated in inelastic/high-regulation metros; binding variable is supply elasticity, not immigration per se.**
- Corpus: Saiz (W3121954821), Hsieh-Moretti (W2614214791), Jaeger-Ruist-Stuhler (W2785732282), Hunt-Gauthier-Loiselle (W3023146776) + Wilson-Zhou WP2607 (parent-fetched to corpus).

### ✅ policy — returned 2026-06-25 (`immigration-policy-frontier-2026-06-25.md`) — strong
Intern-rule: load-bearing legalization-cluster DOIs (Pinotti AER, Freedman AEJ:Pol, Baker AER, Miles-Cox JLE) all `resolve_doi`-verified exact. Job-A fetch: Abramitzky w31440 + Butcher-Piehl w13229 newly full-text; Light already in; Ousey-Kubrin/Hausman metadata+findings (PDF fetchers JS/transport-blocked, bodies captured).
- **Biggest gap closed — legalization→crime CAUSAL cluster:** reframes crime from "do immigrants offend" (levels, already held) to "does legal STATUS change behavior" (causal). Converges across designs on **legalization REDUCES crime via the JOBS channel**: Baker (IRCA, −3-5%, property), Pinotti (Italy click-day RD, halves serious crime — best-identified), Freedman-Owens-Bohn (the channel is jobs — IRCA's employer-sanctions side RAISED crime among locked-out recent arrivals), Ibáñez (Colombia regularization).
- **Enforcement→crime ≈ NULL** (Miles-Cox landmark 197c; Kang-Song; Hausman) — deporting "criminal aliens" via Secure Communities didn't measurably cut crime. **Sanctuary→crime null** (Kubrin-Bartos synthetic control). **DACA cluster** (Kuka-Shenhav-Shih ↑HS-completion/↓teen-births; Hsin-Ortega mixed — ↑employment but ↑dropout). **Refugee:** Evans-Fitzgerald w23498 (full text — net-positive ~8-20 yrs in).
- **Two-directional disconfirmation (proper):** against restrictionist prior (enforcement/sanctuary null, legalization reverses); against naive pro-immigration (channel is jobs not status → enforcement-without-work-access is criminogenic; DACA dropout; Comino underreporting cuts BOTH ways — low recorded crime partly reflects silence, not only low offending).
- **5 dataset cards (→ roadmap):** TRAC, DHS Yearbook enforcement tables, Secure-Communities activation dates (the staggered-rollout instrument), state E-Verify mandate dates, ORR/ASR refugee microdata.

### ✅ econ-disc — returned 2026-06-25 (`immigration-economics-disconfirmers-2026-06-25.md`) — highest-stakes (touches the spine)
Intern-rule: all 4 priority DOIs verified at primary; econ-disc **corrected two gap-memo DOI errors** (Dustmann-Frattini `.12181` not `.12180`; Colas-Sachs now PUBLISHED AEJ:Pol, not WP) — both corrections confirm. Effect sizes read from fetched full text (Mariel pair via ask_papers CAG, 78.8k tok reported). **Instrument-bias caveat live: every update below points "less costly than the restrictionist prior," which aligns with the LLM tilt — verified at primary precisely for that reason; magnitudes from unfetched bodies tagged [UNVERIFIED].**
- **Mariel (corpus's #1 blind spot) — Clemens-Hunt 2019 adjudication (full text):** Borjas's "10-30% wage harm" survives ONLY under a 4-way knife-cut (non-Hispanic men 25-59, dropouts) leaving **~17 obs/yr**, riding a **55pp black-share jump** (Haitian-refugee arrival + a March-1981 CPS frame change); a schooling-falsification test confirms compositional contamination. Broadened sample → ≈zero (Peri-Yasenov synth-control agrees). Borjas's 2019 "Role of Race" rebuttal kept as **live counter** (not closed). → ladder: DOWNGRADE Mariel-as-large-harm hard.
- **Colas-Sachs 2024 (AEJ:Pol):** GE indirect benefit **~$750/low-skill-immigrant/yr** (range $770-2,100) — same order as the direct cost, opposite sign → flips NAS optimistic scenarios to surplus. The static NAS number is an **upper bound on cost**. → ladder: DOWNGRADE/qualify NAS net-drain.
- **CBO 2024 (pub 60165):** 2021-26 surge **lowers federal deficits $0.9T** over 2024-34 (+$1.2T revenue, +$8.9T GDP) — FEDERAL only (excludes state/local education = where NAS finds the cost). → ladder: ADD federal-surge-positive (HIGH).
- **Dustmann-Frattini 2014 (EJ):** recent UK EEA immigrants **+34% / +£22.1bn** while natives −11%; non-EEA ≈ native ≈ negative. Pairs with Hansen DK (opposite). → fiscal sign = **f(welfare generosity × cohort participation/skill)**, not a constant. ADD (HIGH).
- **Cato/Nowrasteh TX convictions (4 vintages 2015-22):** illegal homicide-conviction 2.2 vs 3.0/100k native (−26%), all-crime −37-50% — closes "arrests≠guilt." → ladder: UPGRADE crime finding on conviction margin. [FRAMING-SENSITIVE: cite TX DPS counts, attribute Cato framing.]
- [GAP] bodies not fetched: Peri-Yasenov JHR, Borjas-2019 rebuttal, Clemens-2021 bias-correction magnitude — flagged.

### ⏳ crime — running (19 KB on disk, finishing) — recent crime-rate frontier + datasets + disconfirmation

## Synthesis verdict (filled at close)
*(per-domain: did the frontier yield new load-bearing evidence, or confirm saturation? what's the single highest-value next acquisition? what stays gated/HUMAN.md?)*
