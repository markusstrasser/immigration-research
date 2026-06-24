# Immigration — Interpreted Insights (adversarially verified)

**Date:** 2026-06-24
**Source findings:** 18 adversarially-verified claims across 5 lenses (scaap-crime-fiscal, claim-conviction-map, crime-evidence-synthesis, net-ledger-conviction). Each claim below carries a post-refutation `conviction_final` (not its prelim grade). Where a refutation dented or corrected the claim, the correction is stated, not hidden.

> **Instrument-bias caveat** (`notes/llm-bias-caveat.md`): this analysis is produced through a frontier LLM whose post-training carries a soft progressive prior, strongest exactly on immigration/crime/justice framings. Mitigation here is structural, not stylistic — every load-bearing magnitude below is anchored to a **nonpartisan or against-interest** primary source (CBO, NAS, BJA, PNAS/AER; Cato corrections that *shrink* Cato's own headline). Direction claims that rest on advocacy sources are deflated or flagged. Read the framing-sensitive section as the place the instrument's thumb is most likely on the scale.

**Posture:** this is the opposite of a hype memo. A single well-verified falsification outranks ten plausible syntheses. Several headline claims below were *corrected* under refutation; those corrections are the most valuable lines in the document.

---

## 1. HIGH CONVICTION — survived refutation (conviction_final ≥ 0.70)

### 1.1 Foreign-born / unauthorized crime runs BELOW native-born — the single best-supported crime node
**[SOURCE]** · **conviction_final = 0.88** · lens: crime-evidence-synthesis

On the strongest U.S. administrative data, unauthorized/foreign-born offending and incarceration run **below** native-born across violent, property, and drug categories. Carried by convergence across independent methods/eras:
- Light, He & Robey 2020 (PNAS 117(51)) — TX DPS 2012–2018, ~700K arrests, the only state recording immigration status at arrest; undocumented ≈ half the native homicide/assault arrest rate, 3–5× lower for property crime, robust to denominator and classification swaps.
- Gunadi 2019 (Oxford Econ Papers) — ACS institutionalization + Altonji-Card IV, undocumented 33% **less** likely institutionalized.
- Abramitzky, Boustan, Jácome, Pérez & Torres 2024 (AER:Insights) — immigrants below US-born for 150 yrs (1870–2020), gap **widening** since 1960.
- Cato/Nowrasteh TX convictions — ~26% lower homicide conviction rate.

**Correction applied under refutation (do not drop these):**
- The headline "half / 2×" **aggregate** ratio is **race-confounded** (predominantly-Hispanic unauthorized vs all-native incl. higher-incarceration Black Americans). The honest within-race gap is ~**30%**, not ~50% (see §1.2).
- The **violent / homicide sub-cell was genuinely contested.** CIS (Kennedy/Richwine/Camarota 2022) documented a real DPS identification-lag undercount: in immature data, recently-convicted illegal immigrants sit in "unknown" and get miscoded native-born. On a 2012-snapshot this flipped Cato's homicide figure to "above average." **Resolution:** Cato PA 977 (2024) rebuilt the data via FOIAs removing the double-count and on **mature** 2013–2022 data found illegal homicide conviction 26% below native, all-crime conviction 48% below — the undercount CIS named, applied to mature data, *predicts and confirms* the direction. CIS itself concedes lower illegal rates for robbery/drugs/lesser offenses.
- "Highest-conviction node in the entire crime picture" should soften to **"among the highest"** (no documented node-ranking supports a strict superlative). Mechanism (selection vs deterrence vs underreporting) is unidentified.

Direction is over-determined; magnitude/scope/framing are where the dents live.

### 1.2 The protective gap is real but its commonly-cited MAGNITUDE is overstated (~30%, not ~50%)
**[SOURCE]** · **conviction_final = 0.90** · lens: crime-evidence-synthesis

Landgrave & Nowrasteh, Cato PA 994 (Apr 2025), race-stratified 2023 incarceration per 100k: Native-born all = 1,221; native-born excl. Black = 891; illegal-immigrant all = 613; illegal excl. Black = 626. The aggregate "~50% lower" (613 vs 1,221) collapses to **~30% lower** (626 vs 891 → 29.7%) once Black Americans — higher-incarceration, absent from the predominantly-Hispanic unauthorized group — are removed from both sides. All four numbers verify **verbatim** against the primary PDF.

- **Direction is bulletproof, magnitude is right to one sig-fig (~25–30%).** Independent newer year (Cato BP198, 2024 ACS) shows illegal < native within **every** racial group (Hispanic 957<1,278; Black 976<3,349; White 374<720; Asian 110<321). The cleanest like-for-like (Hispanic within-race) is ~25% lower — so the honest band is **~25–30%**.
- **The correction is credibility-enhancing, not advocacy:** it *shrinks* the gap Cato touts (and the 613→626 anomaly — removing Black natives *raises* the illegal rate — is the source's own against-interest disclosure). Direction independently corroborated by Abramitzky et al. (NBER w31440, Stanford, non-Cato).
- Caveat: the precise race-decomposition remains a single shop's (Cato/Nowrasteh) internal work; only the *direction* is replicated outside it. Removing race isolates one confound; age/sex/geography/detection/ICE-detention inclusion remain (removing 37,684 ICE detainees drops the illegal rate 674→356).

### 1.3 Federal annual cash-flow: the 2021–2026 surge RAISED revenues and CUT the federal deficit
**[SOURCE]** · **conviction_final = 0.95** · lens: net-ledger-conviction

CBO (pub 60569, 2024): federal revenues **+$1.2T** over 2024–2034, net deficit **reduction ~$0.9T** over 2024–2034 (~$296B over 2024–2028), GDP +$8.9T nominal. Every figure verified verbatim against CBO's own text/tables. A disconfirmation search for *any* source claiming the surge raised the federal deficit returned empty.

- **Coordinate-locked:** FEDERAL + ANNUAL/10-yr + AGGREGATE + SURGE-cohort. NOT lifetime-NPV, NOT state-local, NOT steady-state stock. The contrarian cost figures (Heritage $5T, FAIR) live at a *different* coordinate and are advocacy (deflated to 0.28).
- The finding's own "internal-consistency flag" (a "−$897B" line allegedly contradicting the deficit-reduction headline) was **disproven**: −$897B is CBO's own *signed* delta-to-deficit (negative = reduction), in the same table as the −$296B figure. Resolving it strengthens the case.
- The Borjas "against-interest" corroborating leg is **mildly miscalibrated** — a positive aggregate surplus is near-mechanical from downward-sloping labor demand, which Borjas always conceded; his skepticism is *distributional/fiscal*, not about the aggregate triangle's sign. CBO carries the direction independently, so this dents one leg, not the conclusion.
- This does **not** rest on the advocacy-inflated "immigrants are net contributors" meme (ITEP/Cato, deflated to 0.28) — correctly disclaimed.

### 1.4 At the <HS, first-gen, lifetime-NPV coordinate the sign is NEGATIVE for incumbent natives — but flips positive under one defensible accounting rule
**[SOURCE]** · **conviction_final = 0.90** · lens: net-ledger-conviction

NAS 2016/17 panel (Ch.8): an age-25 <HS individual immigrant has lifetime fiscal NPV ≈ **−$109,000** (2012$). The same cell flips to **+$128,000** under Clemens's capital-tax adjustment, *without changing the earnings path*.

- Both numbers verified **verbatim** from the real CGD PDF (cgdev.org): *"the adjustment changes the sign of lifetime net fiscal impact: from –$109,000 to at least +$128,000 without including children and grandchildren."* Paper is real (CESifo WP 9464 / IZA DP 15592, 2022). The −$109k traces to the NAS panel (Blau et al. 2017, NAS 2017 Table 8-12/8-13).
- **Mechanism MISLABEL — correct the prose:** the finding (and ledger-map M2) call Clemens's adjustment "general-equilibrium / capital-tax GE." Clemens **explicitly rejects** this: *"this is not a general equilibrium effect… an instantaneous, static effect… at partial equilibrium (fixed factor prices)."* It is a **fixed-price partial-equilibrium accounting correction** (firms add capital → that capital is taxed → NAS omitted it). The error cuts *in the finding's favor* — a PE correction needs fewer assumptions than a GE estimate — but the label must be fixed everywhere it appears.
- **Direction NEGATIVE is over-determined:** all 8 NAS <HS scenarios are negative (the NAS <HS average ~−$117k to −$173k is *more* negative than the −$109k point chosen); restrictionist estimates run far more negative. The *only* thing producing a positive sign is Clemens's one rule — exactly "assumption-dependent, flips under a defensible rule."
- **Caps below 0.95:** Clemens is pro-immigration producing a pro-immigration result (with-interest, 0.8); the +$128k is a working paper with **no peer-reviewed rebuttal surfaced** and AEI (Orrenius 2025) applies the model and still finds ≤HS net negative. So "the flip is settled-direction" is too strong — "published but contested" is accurate. The −$109k itself is one scenario in NAS's 8-scenario fan.
- **Provenance gap:** the cited local PDFs (Clemens, NAS) are **not on disk** (`sources/` and `external/` trees empty/absent) — externally verified, not locally re-checkable. Re-archive needed.

### 1.5 Costs are CONCENTRATED, benefits are DIFFUSE — the structural reason it "feels" net-negative without being so
**[SOURCE / INFERENCE]** · **conviction_final = 0.82** · lens: net-ledger-conviction

Two genuinely negative, narrow cells (first-gen **state-local** fiscal; distributional **wage** hit to competing low-skill natives) sit against positive aggregate-native and migrant-welfare books. State-local: CBO 2025 (pub 61256) direct net cost ~$9.2B (2023 surge), nonpartisan (1.0). Wage hit: Borjas, academic weight 0.8. Against these: positive aggregate native surplus (against-interest in Borjas) and a large migrant place premium (2–15×, Clemens-Pritchett). Standard incidence geometry: concentrated costs, diffuse benefits.

- **Real caveats that cap conviction:** (a) the "exactly two negative cells" framing **undercounts** — lifetime-NPV-<HS (§1.4) is also negative, surviving the "two" framing *only* because it's assumption-dependent (not high-conviction); housing/rent incidence is a third concentrated negative folded into the local story. (b) The wage-hit **magnitude** is pulled toward the small end by the repo's *own* E-Verify/QWI test (closer to a Card-style null than large Borjas gains) — the **sign** survives (imperfect-substitutes prediction), the **strength** is weaker than implied.
- **FRAMING-SENSITIVE via the welfare boundary:** the sign of the *whole picture* depends on whose welfare you weight (incumbent-natives-only vs all-residents vs global). The single most refutation-resistant element is the Borjas aggregate surplus up-weighted *because* it's against his prior.

### 1.6 SCAAP captures a real, measurable, highly state-concentrated criminal-alien incarceration footprint — among participating jurisdictions only
**[SOURCE]** · **conviction_final = 0.88** · lens: scaap-crime-fiscal

FY23 SCAAP (BJA): ~**7.83M** DHS-confirmed criminal-alien inmate-days, **$210.4M** reimbursed, ~500 jurisdictions, 43 states + PR + VI. Highly concentrated: **CA (27.9%) + TX (27.3%) = 55%** of confirmed days; top-5 = **73.7%**.

- **Correction:** the jurisdiction count should read **~500/501** (not "482"); the universe is **43 states + PR + VI** with **8 of 51 states+DC entirely absent (incl. DC itself)** — SCAAP is **opt-in**, so 7.83M / $210M are **lower bounds on the participating subset**, not a national census.
- "Criminal alien" = a DHS immigration-status flag spanning LPRs, visa-holders, and unauthorized — **NOT** a synonym for "unauthorized."
- Concentration partly tracks state population/jail size, **not** per-capita propensity (no denominator). Per-foreign-born-capita ratios differ sharply (TX ~2.4×, AZ ~3.1×, NY ~0.5×) — "concentration" must not be read as "where unauthorized immigrants commit crime."

### 1.7 The SCAAP undercount is large and unresolvable from this data — confirmed days are a FLOOR
**[SOURCE]** · **conviction_final = 0.78** · lens: scaap-crime-fiscal

Nationally **6.48M "unknown-status" inmate-days** (83% as many as the 7.83M confirmed); in several states unknown ≈ or > confirmed (FL 0.99, CO 1.83, NV 1.44, OK 1.68). True criminal-alien days plausibly range from ~7.8M (floor) to a ~14.3M ceiling (all-unknown thought experiment, honestly flagged as a bookend, not an estimate). GAO-11-187 confirms SCAAP days "represent only a portion of the criminal alien population."

- **Factual correction (the finding's own hedge was backwards):** the "unknown" pool is **NOT** a mix of citizens and the general inmate population. Primary SCAAP docs show jurisdictions submit only inmates they "know or reasonably believe are undocumented criminal aliens" — the unknown pool is **pre-filtered to suspected non-citizens** and is heavily DHS-verification lag / whole-jurisdiction reporting failure (e.g. PA DOC: 0 confirmed, 181,422 unknown). Unknowns are *more* alien-skewed than the finding stated.
- **Over-hedged agnosticism, corrected:** for the **count**, both structural forces (voluntary undercount + suspected-non-citizen unknowns) push the true number **UP** — the "direction is genuinely ambiguous" hedge is legitimate only for the *severity/welfare* signal. Note the 0.83 ratio partly reflects that confirmed days are only ~1.9% of all inmate-days, so it measures DHS-verification incompleteness as much as hidden criminal aliens.

### 1.8 SCAAP inmate-days are a custody STOCK, not a crime rate — the headline flips with the denominator
**[SOURCE]** · **conviction_final = 0.90** · lens: scaap-crime-fiscal

Within-state criminal-alien share of jail-days is **tiny** (national 1.9%; CA 4.4%, AZ 3.2%, FL 1.3%, GA 1.0%, NY 7.1%). Inmate-days (felony or 2+ misdemeanor conviction AND ≥4 consecutive days) are a person-days-in-custody **stock**, confounding offense frequency with sentence length, bail policy, ICE-detainer holds, and time-to-disposition.

- **The CA-vs-NY divergence is the proof:** CA is #1 in *absolute* national days (27.9%) but mid-pack in *local* share; NY is #1 in *local* share (7.1%) but only ~5% of national days. The headline flips entirely with the choice of denominator. NY's local share is 89% one long-sentence state-prison jurisdiction (DOCCS) — affirmatively custody-duration/policy, **not** offending frequency.
- No immigrant-population denominator exists in these tables, so **no rate of any kind** is computable from this warehouse. Source incentive is against-interest (SCAAP *reimburses* states, biasing toward inflating alien-days) — and the share is still 1.9%.

### 1.9 SCAAP reimbursement dollars are NOT a cost measure; the join's fiscal correlations are spurious-by-construction
**[SOURCE]** · **conviction_final = 0.95** · lens: scaap-crime-fiscal

Award per confirmed inmate-day ranges **67-fold** ($7.28 GA to $488.65; median $27.34) with no relation to actual incarceration cost — SCAAP is a fixed federal appropriation distributed by a salary-weighted, prorated formula (claims exceed funds; every state is prorated). The view's correlations between criminal-alien days and Medicaid/SNAP/LEP (days-vs-LEP r=0.97) are **state-size co-scaling**, not a causal fiscal link.

- The Medicaid/SNAP/LEP columns come from a separate state-context table LEFT-JOINed on state_fips; they describe the **whole state population** (all incomes, all nativities), **not** the incarcerated cohort. Treating any of these as causal is a textbook ecological/population-scaling fallacy — **[FRAMING-SENSITIVE]**.
- Residual nuance: the LEP signal specifically may be immigrant-composition co-scaling rather than pure population; the decisive test (partial correlation controlling for *foreign-born* population) needs the license-restricted IPUMS microdata, not the public warehouse. Even if it survived, it would not make the columns a cost measure.

### 1.10 Q5 state-local cost (≈ −$2.1k/yr per 2023-surge resident) reproduces to the dollar
**[SOURCE]** · **conviction_final = 0.82** · lens: claim-conviction-map

Held CBO 2025 state-local PDF (pub 61256): −$9.2B direct net on 4.4M added 2023 residents → **−$2,091/yr** (−$2,227 "potential"). Reproduces exactly; both inputs are verbatim in the held primary source and independently logged in the claims matrix (VERIFIED/HIGH).

- The point estimate is **shown**; its "fragility under a broader horizon" half is **gated** on a same-universe lifetime micro-sim not built.
- **Fragility DIRECTION partially contradicted:** the finding (via ledger-map L27, ~0/+ dynasty) implies −$2.1k flips toward neutral/positive under a dynasty horizon. But the surge is ~44% <HS, and the only held cell-matched descendant decomposition (NAS 2017 <HS) makes lifetime NPV **worse** (−$109k → −$186k), not better. The aggregate "2nd-gen are top contributors" is an all-education average that does **not** transfer to the low-education surge cell. CBO itself says the longer-term cost "could either rise or fall." Honest reading: **coordinate-bound, dynasty-horizon sign indeterminate** — calling −$2.1k "the" cost is itself the coordinate-switch the claim warns against. (Data-hygiene bug noted: a stale −109000 in `npv_education_benchmarks` includes-descendants <HS row.)

### 1.11 Q6 splits: SCAAP concentration is settleable today (top-5 incl. FL, not the named top-4); the trend is gated
**[SOURCE]** · **conviction_final = 0.86** · lens: claim-conviction-map

Concentration reproduces exactly (CA 27.9% + TX 27.3% + FL 7.1% + AZ 6.5% + NY 5.0% = 73.7%; HHI 1684 "highly concentrated"). **Correction:** the original Q6's named top-4 "CA/TX/AZ/NY" **omits Florida**, which is rank #3 on inmate-days (557,135 days). FL is #3 on days but #4 on dollars, so the safe phrasing is "top-5 incl. FL, not the named top-4."

- The **FY2015–23 trend** sub-claim is **fully gated** — only FY2023 is held. Multi-year SCAAP PDFs are public (testable in principle), and a raw inmate-day trend would be confounded by participation/confirmation drift, so the principal check must be a participation-adjusted per-capita rate.
- Composite Q6 joins concentration AND trend with "and," so as a unit it is correctly ungradeable; the split-decision is the right epistemic move.

---

## 2. CONTESTED / FRAMING-SENSITIVE

### 2.1 Second-generation crime convergence — genuine but deliberately downgraded (the weakest crime node)
**[INFERENCE]** · **conviction_final = 0.88** (on the *scoped* claim) · lens: crime-evidence-synthesis

Later generations drift **toward** (not above) native crime levels — but the supporting evidence is **broad generational literature, not unauthorized-specific or current-cohort**. Anchors: Ousey & Kubrin 2018 (Annual Review, meta of 51 studies / 543 effects) and Rumbaut 2008.

- The macro immigration-crime association is **null-to-weakly-protective**, not strongly so: Ousey-Kubrin mean **r = −0.031** (95% CI −0.055 to −0.003), with heavy design-heterogeneity (longitudinal r=−0.147 vs cross-sectional r=0.000; new-destination r=+0.028). So 2nd-gen convergence is a **caveat ON the first-gen finding (§1.1), not an independent high-certainty claim**.
- The exact r-value is memo-reported, not independently re-confirmed (it lives in a results table snippet retrieval couldn't surface; the qualitative "negative but very weak" is verified). The node does not depend on the third decimal.
- "Convergence toward native rates" ≠ "above native rates" — even converged 2nd-gen is **not shown to be a net crime cost**. The robustly-surviving statement is only the directional "first-gen protective effect attenuates across generations."
- The warehouse holds **no** 2nd-gen crime cell (only binary is_foreign_born; incarceration column 100% NULL) — confirming the scope limit from the repo's own ledger.

### 2.2 Sanctuary/enforcement → crime: protection does NOT raise crime, but the "symmetric null" framing is wrong
**[SOURCE / partial UNVERIFIED]** · **conviction_final = 0.72** · lens: crime-evidence-synthesis

The **load-bearing direction survives**: protecting unauthorized immigrants from deportation does **not** raise crime (Hausman 2020 PNAS matched-county; Kubrin-Bartos post-SB54; corroborated by the low individual base rate in §1.1 + reporting-suppression mechanism).

- **Pillar mischaracterized:** Kang & Song 2021 (JLEO) is **not** "largely null" — `verify_claim` returned CONTRADICTED; it is a geographical-externality finding (crime *reduction* in activated counties when neighbors also activate). One of three named pillars was misread.
- **The "symmetric two-sided null" framing is wrong** — **[FRAMING-SENSITIVE]**. The enforcement side is **not** neutral: frontier work (NBER w32109; Census/AEA community-safety papers; the project's own claim-candidate C5 codes "enforcement reduces crime" as CONTRADICTED) finds enforcement **raises** violent victimization by suppressing reporting. Honest statement: **protection → null/no-harm; enforcement → null-to-HARMFUL.** The tidy "symmetric zero" laundered a directional harm finding.
- Evidence is **scout-verified metadata, not full-text-read** — treat as strong-prior-pending-read. No NCVS-based direct immigrant-victimization measure is held. The warehouse holds only SCAAP, which cannot adjudicate.

---

## 3. GATED — direction expected from literature, NOT shown by this stack

> **Honest framing:** most roadmap crime/mobility datasets are **not downloaded**. For these nodes, conviction is "what the existing peer-reviewed corpus expects," not what this stack has computed. The SHARP/killable versions require micro-data the warehouse lacks.

### 3.1 The entire crime cluster's settling datasets have ZERO downloads
**[UNVERIFIED — gated]** · **conviction_final = 0.85** (on the *negative* claim + direction) · lens: claim-conviction-map

C1 (TX-DPS felony-rate, openICPSR-124923), C2 (BJS-SPI-2016, NACJD-37692), C3 (USSC federal-offender net-of-immigration-offense), S3 (Opportunity-Atlas/NCRP 2nd-gen) are **all ⬜ in the roadmap, triple-confirmed absent** from register and data tree.

- **Precision correction:** the literal "ZERO crime datasets downloaded" is false — SCAAP (`crime_scaap_*`) IS a downloaded crime-adjacent dataset. But SCAAP **structurally cannot** settle any of C1/C2/C3/S3 (no native comparison cell, no arrest numerator, no population denominator, no race stratification), so the **count of settling datasets is genuinely zero**.
- Expected directions (predictions, not shown): C1/C2 confirm-lower-but-narrower (race-stratified gap ~30%, §1.2); C3 likely **overbroad** (federal non-citizen over-representation collapses net of 8 U.S.C. immigration offenses); S3 likely **falsifies** any clean "immigrants-and-descendants are low-crime lineage" narrative (advantage is first-generation, not lineage). The ~30% magnitude is against-interest (Cato conceding its own ~50% overstates).

### 3.2 The <HS NPV sign-flip is documented but not same-universe-reproduced
**[SOURCE published / reproduction UNVERIFIED]** · **conviction_final = 0.82** · lens: claim-conviction-map

(Same flip as §1.4, from the conviction-map lens.) The −$109k → +$128k flip is a real, exactly-transcribed, published result (verified verbatim) — but **no built artifact re-runs both NAS current-law and the capital-tax-corrected side under one micro-sim**. The warehouse's own annual flows annuitize to ~−$2.8k to −$4.6k/yr and carry `bridge_verdict='scope_mismatch'` for the <HS cell — they do **not** tie to NAS −$109k.

- Same corrections as §1.4: **drop "GE," say "fixed-price partial-equilibrium capital-tax accounting correction"**; flip is **published-but-contested** (AEI 2025 rejects the adjustment), not settled-direction. Provenance gap: cited PDFs not on disk.

### 3.3 Second-generation fiscal/mobility (S1, S2) — strongest-anchored gated claims
**[SOURCE external / local UNVERIFIED]** · **conviction_final = 0.93** · lens: claim-conviction-map

S1 (2nd-gen are top net contributors) and S2 (children-of-immigrants out-rise children-of-natives from nearly every origin) are the best-anchored gated claims — NAS 2016 + Abramitzky-Boustan-Jácome-Pérez AER 2021 (millions of admin father-son pairs). The settling micro-data (ABJP openICPSR-120490, Opportunity Atlas 2nd-gen) is **not downloaded** (verified absent: 103 warehouse tables, no rank-rank/mobility/Atlas data).

- **Direction robustly anchored, but "what the literature expects, not locally computed."** The strongest counter-literature (Duncan-Trejo) does **not** realize the killable inverse — it measures the 2nd→3rd transition (S2 is 1st→2nd) and finds the apparent Hispanic stall is largely a selective-ethnic-attrition *artifact*, reinforcing the direction.
- **Citation bug to fix:** claim-candidates line 61 mislabels S1's fiscal anchor as "NBER w26408" — w26408 is the Abramitzky-Boustan **mobility** paper (underpins S2). S1's correct anchor is NAS 2016 (NAP.edu/23550). Both real, distinct.
- Caveat: the verify-pass confidences (0.9–1.0) are Exa /answer web-triage, **not** adversarial cross-model grades.

### 3.4 Dynasty net sign (~0/+) — gross 2nd-gen-positive robust, NET reversal assumption-contingent
**[SOURCE external / local UNVERIFIED]** · **conviction_final = 0.62** · lens: net-ledger-conviction

NAS finds the 2nd generation contributes **more in taxes** than their parents or the rest of the native-born — verified verbatim (1.0). The finding upgrades this to a **NET** claim ("reverses the first-gen state-local deficit"), and **that upgrade is the weak link**:

- The NAS statement is **GROSS taxes-paid**. The NAS Table 8-12 **NET** (immigrant + descendant combined 75-yr NPV) ranges from substantially **negative** to positive across the eight scenarios — negative under average-cost public-goods + CBO-budget assumptions. The finding's own generator A06 carries a disconfirming case (descendants −$15k while immigrant +$92k).
- So **"dynasty NET ~0/+" is assumption-flipped, not robust.** Gross 2nd-gen-positive survives; the net reversal does not, cleanly. Same w26408→NAS-2016 mis-source as §3.3. Honest downgrade: "sign indeterminate, gross-2nd-gen-positive but net-dynasty assumption-dependent."

---

## Cross-cutting cautions (read before quoting any number above)

1. **Coordinate-switching is the central debate error.** Federal-annual (+, §1.3), state-local-first-gen (−, §1.5/1.10), <HS-lifetime-NPV (− or +, §1.4), dynasty (~0/+ gross, indeterminate net, §3.4) are **different books**. Quoting one to rebut another is the named fallacy. There is no single "the cost of immigration" number.
2. **Welfare boundary sets the sign of the whole picture** (§1.5): incumbent-natives-only vs all-residents vs global. Under a global/all-resident boundary the migrant place premium dominates; under an incumbent-low-skill-native-only boundary the two negative cells dominate. **[FRAMING-SENSITIVE]**
3. **SCAAP measures custody/reimbursement, not offending or cost** (§1.6–1.9). It cannot answer "do immigrants commit more crime" or "what do criminal aliens cost."
4. **Provenance gap:** the `external/` PDF tree is absent; the Clemens/NAS figures are externally verified but not locally re-checkable. Re-archive before treating as "primary evidence held."
5. **Evidence base is mildly cost-tilted by composition, not by rule** (mean adj_weight 0.63 cost vs 0.76 benefit) — the corpus is built richer on cost-measurement than benefit-measurement.

## Concrete fixes surfaced (cheap, no-downside)
- SCAAP: correct "482"→~500 jurisdictions and the universe to "43 states + PR + VI; 8 of 51 states+DC absent incl. DC" (§1.6); add a checksum assertion against BJA's $210,386,343 / 500 in `parse_scaap_awards.py`.
- Everywhere: replace "GE / general-equilibrium" → "fixed-price partial-equilibrium capital-tax accounting correction" for the Clemens adjustment; note the flip is published-but-contested (AEI 2025) (§1.4/3.2).
- `immigration-claim-candidates-2026-06-24.md` line 61: fix S1's anchor w26408→NAS-2016 (NAP.edu/23550) (§3.3/3.4).
- `npv_education_benchmarks`: fix the stale −109000 in the includes_descendants <HS row (§1.10).
