# Brainstorm Synthesis — Immigration paradigm-escape (2026-04-18)

## Design space

**Question:** What else to analyse in the immigration project beyond what's been done?

**Escaping:**
- Done in current cycle: Saiz × rent, E-Verify TWFE, race-stratified crime, federal-vs-local incidence, AGI reframing.
- Done in prior brainstorm (2026-04-11): court/interpreter friction, school complexity, labor standards, institutional overload, stress-test, political feedback, admission-channel.

**Dominant paradigms to escape:** US-centric framing, quantitative econometric estimation, welfare/incidence ledger framing, immigrant-as-variable, linear treatment effects.

## Top EXPLORE candidates (ranked by paradigm-escape value × feasibility)

### Tier 1 — Highest leverage, fresh datasets, clean designs

**`I11` Open-borders calibration (Clemens place-premium + binding constraint identification).**
The single biggest unaddressed lever in the entire project. The repo's verdict ("not net negative, not net positive") implicitly weights immigrant welfare at zero. Clemens 2011 estimates $10–50K/year per migrant. Even at half that, the global welfare calculation flips for any plausible elasticity. Identifies which constraint actually binds (housing? schools? cohesion?). Data: WB Migration & Development Brief, Clemens 2011 reproducible code. Feasible: 2-3 days standalone, no SSD needed.

**`I14` Diversity Visa lottery as RCT.**
True random assignment. ~50K winners/year since 1995, from a pool of 10M+ applicants. Long-run outcomes of winners vs non-winners speak directly to selection vs treatment. Mishra-Mountford have analytical frameworks; State Dept has the data. Feasible: 3-5 days, requires DV winner records (FOIA-able or via existing academic licenses).

**`I16` Immigration judge IV.**
EOIR judge fixed effects produce quasi-random variation in case outcomes (Ramji-Nogales "Refugee Roulette" 2007). TRAC has case-level data. Reveals de facto policy. Feasible: 1 week, TRAC has clean panel.

**`I15` Sanctuary city natural experiment.**
~600 jurisdictions adopted sanctuary policies at different times. ILRC maintains the panel. Outcomes: crime reporting (Light-Miller-style), school enrollment, victimization. Tests "trust between immigrants and local institutions" causally. Feasible: 1 week, all data public.

**`I12` Mass-deportation 11M-scale counterfactual.**
The Borjas mass-shock claim has no empirical analog. But BEA I-O tables × industry FB-share × short-run elasticities can simulate. Identifies which industries collapse, what consumer prices do, what state budgets look like. Feasible: 5 days standalone, clean simulation.

### Tier 2 — High value, harder data acquisition or longer execution

**`I01` Sending-country welfare ledger.**
Honduras/Guatemala/Mexico fiscal-political effects of emigration. Remittance dependence, brain drain (or brain gain via incentive effect: Beine-Docquier-Rapoport), rural depopulation, electoral effects. Data: WB Bilateral Remittances, ENCOVI, INEGI. Feasible: 2 weeks, mostly aggregation work.

**`I17` Internal-native migration as comparison.**
West Virginia → Pittsburgh natives create same school/housing burden as Mexico → Pittsburgh immigrants. If true, "immigrant-specific" framing is wrong; the right frame is "newcomer in general." IRS SOI county-county flows + ACS migration tables. **Reframes the entire project** — could be the single most disruptive finding. Feasible: 1 week.

**`I05` Tipping-point / phase transition.**
Schelling-style threshold detection. Card-Mas-Rothstein methodology applied to immigrant-share crossings. Are there discontinuities in native flight, school quality, or rent at specific FB-share thresholds? Feasible: ACS panel + change-point detection.

**`I09` Wharton WRLURI as instrument for elasticity.**
Sharpens the Saiz finding from the recent cycle. Zoning regulation index is a more exogenous component of supply elasticity than topology. Tests whether the rent-immigrant correlation comes through the regulatory channel specifically (policy-relevant) or topology (not policy-relevant). Feasible: 2 days, requires WRLURI 2018 update.

**`I10` Defense-in-depth cost curves.**
DHS spends ~$30B/year on enforcement across border + interior + workplace + benefits. What's the marginal cost of one deterred entry by venue? CBP/ICE budget × performance metrics. Identifies efficient enforcement margin. Feasible: 1 week.

**`I18` Health and mortality (immigrant health paradox + immigrant care provision).**
Two-sided: immigrants live longer than natives despite lower SES (paradox), AND immigrants provide a large share of elder care. CDC NVSS, MEPS, BLS. Connects to AGI-soon: care work is automation-resistant. Feasible: 1 week.

**`I19+I23` Long-run linked microdata + endogenous fertility (merged).**
1980/1990 immigrant cohort → 2020 outcomes via Census FSRDC linked records. Plus Borjas-Hanson endogenous native fertility test. Speaks directly to NAS descendant projections vs reality. Feasible: 1 month (FSRDC application + analysis).

### Tier 3 — Conceptual reframing, fewer immediate data needs

**`I02` Comparative international regimes (Gulf Kafala, Canada points, Germany 2015).**
Tests what's regime-specific vs universal. Forces honesty about whether US-style verdict generalizes. OECD International Migration Outlook + MPI country profiles. Feasible: 1 week, mostly synthesis.

**`I06` Cohort/vintage Foged-Peri 6-year latent period replication.**
ACS PUMS by year-of-entry × current year. Tests whether wage effects appear with delay (could explain why immediate E-Verify TWFE is null). Feasible: 1 week, sharpens the recent cycle finding.

**`I07` Niche partitioning (Peri-Sparber tasks formalized at MSA level).**
O*NET task vectors × ACS occupation × nativity. Tests the complementarity mechanism directly. Feasible: 1 week.

**`I13` Time-reversed: 1900-1950 wave convergence.**
Abramitzky-Boustan methodology. Italian/Irish/Slavic gen-1/2/3 vs current Hispanic gen-1/2/3. Tests whether 1924-style restrictions actually accelerated convergence. Feasible: 2 weeks.

**`I03` Court case-law evolution text analysis.**
case.law + INS regulatory history. How has the legal regime shifted 1965-2024? Quantifies the production of "illegality." Feasible: 1 week.

**`I08` Real-options migration model.**
Coyote price series as supply curve; enforcement raises strike price not flow at margin. Tests intensive vs extensive enforcement margin. Feasible: 2 weeks.

## PARK

- `I04` Border-as-produced (De Genova) — high novelty but speculative; PARK until data anchor identified.
- `I20` Innovation/entrepreneurship — well-studied externally, no marginal value to this repo.
- `I21` Marriage market intermarriage — interesting but lower urgency.
- `I22` Climate-driven migration projection — forward-looking, speculative until calibration tools mature.

## Paradigm gaps (uncovered cells)

- **Religious institution participation as integration mechanism.** PRRI/ARIS data exist but no idea generated.
- **Language acquisition trajectories.** ACS English ability + cohort, Telles-Ortiz framework.
- **Workplace fatality / VSL compensation differentials.** BLS CFOI by nativity. Who bears physical risk.
- **Ethnographic synthesis from existing fieldwork.** Marrow rural-South Latinos, Lichter-Johnson; not quantitative, not in this brainstorm's idiom.

## Suggested next step

Two natural pairings, given the recent cycle's findings:

**Path A (sharpen current cycle):** `I09` (WRLURI as elasticity instrument) + `I06` (Foged-Peri lag replication) + `I12` (mass-deportation simulation). Tightens the wage and rent findings; adds the counterfactual the Borjas debate actually needs. ~3 weeks combined.

**Path B (escape current cycle):** `I11` (open-borders calibration) + `I17` (internal-native migration comparison) + `I15` (sanctuary city). The biggest paradigm shifts. Either of `I11` or `I17` alone could materially change the project's headline framing. ~3 weeks combined.

**Path C (single highest-leverage):** `I11` Open-borders calibration. The Clemens place-premium reframe is the single biggest unaddressed lever in the entire repo, would force explicit articulation of immigrant-welfare weighting, and connects directly to constitutional principle #5 (name the frame). ~1 week.

## Pain-point gate notes

Most ideas are SPECULATIVE in the strict sense (no prior incident in repo `git log`). Two have stronger pain-point linkage:

- `I11` Open-borders: The repo's explicit rejection of "immigration is bad for country" rests on welfare arithmetic that excludes immigrant welfare — the very critique the repo's own constitutional principles ("steel-man before criticizing") would flag. Pain-point: implicit framing inconsistency.
- `I17` Internal-native migration: Repo memos repeatedly use "newcomer" and "immigrant" interchangeably (e.g., low-skill incidence memo). Pain-point: unit-of-analysis confusion.

Other Tier 1 items are FRESH-DESIGN (no prior incident, but fill structural data gaps).

## Anti-duplication confirmation

Checked `.brainstorm/2026-04-11-immigration-frontier-gaps-b7d2/synthesis.md`. None of this brainstorm's EXPLORE items duplicate that one's modules. Prior covered "what to BUILD on top of the local-burden framework." This one covers "what FRAMINGS / DATASETS / DESIGNS escape the framework entirely."

[SOURCE: matrix.json]
[SOURCE: coverage.json]

<!-- knowledge-index
generated: 2026-04-19T03:55:37Z
hash: 3011f51a5446


end-knowledge-index -->
