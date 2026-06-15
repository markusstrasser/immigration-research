# Immigration lifetime fiscal — unified theory (sweep 11)

**Date:** 2026-06-15
**Corpus:** 110 staged files, 114 catalog sources, 166 mined claims, 80 generators (clusters A–P), `immigration_context.duckdb` + `immigration_lifetime_evidence.duckdb`
**Protocol:** `notes/immigration-lifetime-sweep-protocol.md`
**Frame:** [FRAMING-SENSITIVE] — no defensible scalar "Mexican lifetime NPV."

---

## I. Unified theory (fullest current story)

### Central object

Immigrant fiscal impact is a **layered incidence tensor**:

\[
\mathcal{F}(\text{cell}, \ell, t)
\]

- **cell** = `education_bucket` × `age_at_arrival` × `state_fips`/PUMA × `legal_status_path` × origin-composition weight (Mexico = weight only)
- **ℓ** = ledger layer: `federal_annual` | `lifetime_npv` | `state_local` | `local_episodic` | `private_transfer` | `admin_enforcement`
- **t** = calendar time / cohort (Hanson composition series, surge era vs stock)

There is **no** legitimate reduction to one number. Debate collapse happens when layer ℓ or dimension cell is silently switched.

### Thesis (3 sentences)

**Low-education, recent-arrival immigrants can be mildly federal-positive on an annual cash-flow proxy while lifetime-negative under education-cell NPV accounting and locally costly in inelastic destination metros — and these statements are mutually compatible, not contradictory.** [SOURCE: `origin_fiscal_scenario_2023` Mexico `avg_federal_net` ≈ +$1,519/yr; NAS 2017 `<HS` age-25 individual NPV ≈ −$109k (2012$); Saiz×ACS rent finding in `immigration-causal-saiz-elasticity-rent.md`]

**Sign flips are dominated by accounting rules (public goods, capital-tax GE, descendants, attrition, lifecycle phase), not by "pro- vs anti-immigration" honesty — and sweep 11 showed that even *within* the local layer, a 1000× unit bug made K-12 costs disappear until F-33 thousands were corrected.** Clemens capital-tax adjustment moves the same `<HS` cell from −$109k to +$128k without changing the underlying earnings path. [SOURCE: `npv_education_benchmarks`; Clemens 2023 PDF in corpus]

**The current warehouse-compatible explanation: immigration fiscal politics is a fight over which layer, which cell, and which cohort (surge vs stock) get to stand in for "the immigrant," while restriction and welfare-state politics add equilibrium feedback on skill mix and admin spend.** This is a working synthesis, not proof that every dataset endorses the mechanism. New data can still kill channel magnitudes, cell signs, and annual-to-lifetime bridges; the repeated failure is the one-scalar export.

### What the warehouse actually measures (honest stack)

| Layer | Best current instrument | What it is NOT |
|-------|-------------------------|----------------|
| Federal annual | SIPP donor → `acs_origin_household_federal_microsim_2023` + `origin_fiscal_scenario_2023` | Lifetime NPV; unauthorized-specific |
| Lifetime NPV | NAS/NRC education cells + critiques in `npv_education_benchmarks` | Origin-specific; Mexico scalar |
| Local flow | stage2 county school/housing + stage5 state RPP/Medicaid/EL | Causal attribution to immigrants |
| Local episodic | `receiver_city_migrant_costs` (NYC, Chicago, Denver, …) | Smooth 75-year NPV line item |
| Private offset | World Bank remittances (outflow from US / inflow to Mexico) | Public ledger credit |
| Legal-status floor | ITEP undocumented tax JSON (~$96.7B national, 2022) | Benefit receipt |
| Admin | CBP/ICE FY25 budgets + DHS LPR mix | Per-immigrant marginal cost |
| Housing welfare | Saiz MSA elasticity + PUMA rent context | National CPI argument |
| Bridge (new) | Generators G-LIF-M01–M05: annual↔NPV scope lock | Proof that +$1,519/yr ⇒ −$109k |

### Verifiable anchors (DuckDB, sweep 11)

| Claim | Value | Source |
|-------|-------|--------|
| Mexico-origin scenario weighted adults | 436,819 | `life.origin_fiscal_scenario_2023` |
| Mexico-origin avg federal net (annual proxy) | +$1,519/yr | same |
| Mexico area-wtd per-pupil (**post F-33 fix**) | ~$20,907/pupil | same — was ~$21 pre-fix [INFERENCE: F-33 thousands bug] |
| County per-pupil median (post fix) | ~$19,385 | `life.school_finance_county_2023` |
| Mexico FB `<HS` stock (25–64) | 7,686,859 | `ctx.acs_foreign_born_education_bucket_totals_2023` |
| NAS `<HS` individual NPV (age 25) | −$109,000 (2012$) | `life.npv_education_benchmarks` |
| Clemens `<HS` with capital-tax adj. | +$128,000 | same |
| Mexico remittances inbound (2023) | ~$66.2B | `life` remittance JSON / WB API |
| Mexico federal net proxy × full microsim adults | ~$12.9B/yr | `v_country_fiscal_rollup` federal_annual [DATA] |
| Mexico federal net proxy × scenario subset | ~$664M/yr | 436,819 × $1,519; recent-low-skill/PUMA-linked subset only [INFERENCE] |
| ITEP undocumented taxes (national, 2022) | $96.7B | `life.itep_undocumented_tax_summary` |
| CBO surge federal deficit effect (2024–34) | ~−$897B | [SOURCE: CBO 60569 via `fiscal-impact-unauthorized-immigration-research-memo.md`] |
| CBO surge state/local direct cost (2023) | ~$9.2B | [SOURCE: CBO 61256 via claims evolution ledger] |
| NYC asylum/shelter spend FY2024 | ~$3.7B | `receiver_city_migrant_costs` |
| Saiz elasticity median (MSA) | 2.54 (269 MSAs) | `life.saiz_msa_elasticity` — sweep 31 |
| Mexico NAS age-25 education-mix benchmark | +$45,631/adult | `v_country_fiscal_rollup` lifetime_npv; synthetic age-at-arrival-25 benchmark, not current-stock lifetime NPV — sweep 23 |
| Mexico school burden/adult (microsim weights) | $771 | `v_three_layer_annual` — sweep 26 |
| Mexico crude annual (fed − school) | +$748 | `v_three_layer_annual` — sweep 32 |

### Narrative spine (current synthesis, still falsifiable)

Politicians and advocates pick **one layer** to moralize:

- Restrictionists: NAS lifetime `<HS` negative + local school/shelter headlines
- Expansionists: annual federal surplus + ITEP taxes paid + CBO surge GDP/revenue
- Restrictionists reply: local episodic shelter (Gould) + welfare magnet (Razin)
- Expansionists reply: Clemens/Colas GE + Card-Peri complementarity

Each channel has evidence in its own layer, with different strength and identification quality. Failure modes: **layer laundering** (prove layer A, conclude layer B) and **unit laundering** (sweep 0–10 local school field was 1000× too small).

Return migration (Duleep-Regets) and native out-migration (Borjas w11610) explain why **stock snapshots misstate who bears costs**. Razin political-economy models explain why **skill mix and transfer policy co-evolve** — fiscal sign is not an immigrant fixed effect.

---

## II. Five formal models (competing mechanisms)

Each model is a **ledger grammar** + **prediction map**. Critique = compare grammars, not personalities.

### M1 — NAS education-cell accountant

**Grammar.** Lifetime NPV over 75 years, 3% real discount; education at arrival pins earnings and transfer paths; descendants booked separately; public goods often excluded.

**Core prediction.** `<HS` age-25 immigrant individual NPV ≈ −$109k (2012$). [SOURCE: NAS 2017 Ch.8; `npv_education_benchmarks`]

**Falsifiers.** Marginal-cost public goods; descendant exclusion; **annual federal proxy does not falsify without bridge** (G-LIF-M01).

**Unnamed assumptions.** Education at 25 sufficient; no selective return migration; SIPP annual integrates to NPV — **not tested**.

**Data status.** Strong education gradient; weak origin labels and surge cohort.

---

### M2 — General-equilibrium offset (Clemens / Colas-Sachs / Peri stack)

**Grammar.** Immigrant labor raises capital returns, payroll, indirect tax bases; task complementarity raises native wages in communication tasks.

**Core prediction.** Same `<HS` NAS cell flips positive (+$128k) with capital-tax credit; +~$750/yr indirect federal (Colas-Sachs).

**Falsifiers.** Weak capital complementarity in US `<HS` cells; Borjas-large wage effects.

**Unnamed assumptions.** GE adjustments belong in same ledger as NAS costs (disputed).

**Data status.** Direction credible; magnitude contested; not origin-specific.

---

### M3 — Local incidence / housing welfare (Saiz + stage2/5 + receiver nodes)

**Grammar.** Immigrants sort into low-elasticity MSAs; county school spend scales local flows; asylum/shelter is episodic city ledger.

**Core prediction.** Rent burden in inelastic MSAs; **~$20k/pupil** local K-12 assignment post unit-fix; receiver billions gross.

**Falsifiers.** Topographic vs regulatory inelasticity; renter incidence nuances.

**Unnamed assumptions.** Cross-sectional FB share → causal rent effect; receiver costs amortized into lifetime NPV.

**Data status.** **Local descriptive burden: strong (post unit fix)**; causal rent: medium; net of federal offsets: unbuilt.

---

### M4 — Borjas pessimist (substitution, welfare, spatial equilibrium)

**Grammar.** Immigrant labor reduces competing native wages; welfare recipiency rises; native out-migration attenuates local effects 40–60%.

**Core prediction.** Lifetime `<HS` worse than NAS if earnings path pessimistic.

**Falsifiers.** Card-Peri 2000–2019 complementarity; Clemens-Lewis firm non-substitution.

**Unnamed assumptions.** Wage effect ≡ fiscal effect; Mariel external validity to 2020s surge.

**Data status.** Mariel contested; out-migration attenuation empirical; national wage leaning Card-Peri.

---

### M5 — Dynamic composition & attrition (Hanson / Duleep-Regets / legal-status / Razin)

**Grammar.** Low-skill inflow rates time-vary; return migration negatively selects; border enforcement and welfare politics shift skill/legal mix (Lozano-Lopez; Razin w15597).

**Core prediction.** Static ACS 2023 weights misstate surge liability; restriction changes **cells** not just counts.

**Falsifiers.** Random return migration; surge era dominates stock.

**Unnamed assumptions.** Emigration unobserved in public fiscal micro.

**Data status.** Composition time series strong; return migration fiscal: sensitivity only; political equilibrium: theory + partial LPR data.

---

## III. Cross-model critique matrix

| Question | M1 NAS | M2 GE | M3 Local | M4 Borjas | M5 Dynamic |
|----------|--------|-------|----------|-----------|------------|
| Mexico `<HS` **lifetime** sign | − | + (adj.) | ? (local not in NPV) | − | depends on horizon |
| Mexico recent surge **annual federal** | n/a | + indirect | n/a | − if wage→tax | stock vs flow |
| **K-12 local cost** | in NPV tables | partial | **~$21k/pupil** | omitted | school-age phase |
| **Destination rent burden** | omitted | partial | **core** | attenuated 40–60% | sorting |
| **Shelter/asylum shock** | omitted | omitted | **core episodic** | omitted | surge-era |
| **Remittance private layer** | omitted | omitted | omitted | omitted | partial offset |
| **Restriction admin cost** | omitted | omitted | omitted | omitted | **CBP/ICE ℓ** |
| **CBO surge federal** | n/a | macro band | n/a | n/a | cohort tag |
| **Data we have** | benchmarks | papers | Saiz+stage2/5 fixed | Mariel stack | Hanson+IZA+Razin+LPR |

**Current irreconcilables (scope choices plus empirical gaps):**

1. **Lifetime vs annual** — M1 vs SIPP (+$1,519/yr) — bridge required (G-LIF-M01)
2. **GE inclusion** — M1 vs M2 (−$109k vs +$128k)
3. **Federal surge vs local episodic** — CBO 60569 vs NYC $3.7B
4. **Stock vs surge cohort** — ACS weights vs CBO 2021+ scenario
5. **Wage → fiscal** — M4 vs M2

**What current data has not killed:** The layered-accounting explanation — several models can be locally informative if their ledger and cell scopes are explicit.

**What data can kill:** Specific **scalar exports** and **unit errors** — pre-fix $21/pupil local layer; "Mexico lifetime NPV"; "immigrants don't pay taxes" vs ITEP.

---

## IV. Disconfirmation (active hunts)

1. **Annual↔NPV bridge** — annuitize NAS `<HS` at 2–4% vs SIPP +$1,519/yr; document scope gap (public goods, local school, GE). [G-LIF-M01] **Partially resolved:** scopes differ by construction — not a sign contradiction.
2. **Receiver vs federal dominance** — NYC FY2024 ~$3.7B alone vs ~$664M/yr Mexico scenario-subset federal proxy, but not vs the full Mexico-stock federal proxy (~$12.9B/yr). Episodic local can dominate **city-level surge-subset** storytelling; do not compare it to the entire Mexico-born stock unless the denominators match. [G-LIF-P02] [INFERENCE]
3. **Restriction macro offset** — CBO 60569 inverted for lost workers vs local shelter savings — restriction not free on federal ℓ. [G-LIF-P04]
4. **Unit regression guard** — any per-pupil field outside $8k–$30k triggers F-33 thousands audit. [G-LIF-N01] **Killed pre-fix bug;** monitor on rebuild.

---

## V. Thesis burst

### Sweep 10 thesis (verbatim)

> Fiscal immigration "truth" is a tensor. Mexico is a weight, not a number. Federal annual +, `<HS` lifetime NPV −, education-mix age-25 benchmark +, and local episodic − can coexist. Sign wars are accounting wars. Return migration and native out-migration explain why stock photos lie. Next: fix unit bugs, bridge annual→lifetime formally, stop downloading papers without updating this section.

### Sweep 11 revision

> The tensor got a unit correction: local school was off 1000× until F-33 thousands were fixed (~$21 → ~$21k/pupil). Annual federal+, `<HS` lifetime NPV−, and education-mix age-25 benchmark+ still don't refute each other — they need an explicit bridge (Lee-Miller lifecycle, remittance private layer, CBO surge-vs-stock tags). Restriction and welfare politics shift **which cells arrive**, not just how many; admin and receiver ledgers are real layers politicians ignore when exporting scalars.

**Sharper:** 80 generators; F-33 bug killed; Mexico remittance scale (~$152k/adult inbound to Mexico) dwarfs federal net proxy (~$1.5k/adult) on private ℓ — public ledger fights ignore household budget.

**Killed:** "Local school cost negligible in scenario table" (unit bug); naive annual-vs-lifetime sign contradiction without bridge.

**Survived (weak data):** GE flip magnitude; Mariel bracket for 2020s surge; Storesletten correct PDF still missing (w9489 mis-staged).

**New falsifier:** If post-fix K-12 local assignment × school-age share still << federal annual for Mexico `<HS` surge cells, local-flow layer may be secondary at **annual** frequency even when the NAS `<HS` cell is negative.

---

## VI. Generator map (where to look)

| If you need… | Cluster |
|--------------|---------|
| NPV / public goods / capital tax | A |
| Wage ≠ fiscal / Mariel / out-migration | B |
| Federal+/local− / magnets / shelter | C |
| Composition / descendants / DACA | D |
| Saiz / rent welfare | E |
| H-1B ≠ Mexico `<HS` | F |
| ITEP / Pew / border selection | G |
| Refugee / mortality | H |
| Return migration | I |
| CBP/ICE / LPR mix | J |
| County joins / receiver episodic | K |
| OECD flows / MEPS horizon | L |
| **Annual↔NPV bridge / remittances** | **M** |
| **School finance units / K-12 band** | **N** |
| **CBO split / welfare magnet / Razin** | **O** |
| **Restriction / enforcement / episodic dominance** | **P** |
| **Stock vs flow / denominator discipline** | **Q** |
| **Full ledger stack (NAS ≠ net)** | **R** |
| **Restrictionist steel-man chains** | **S** |

Full text: `research/immigration-lifetime-fiscal-generators.md`

---

## Revisions

| Date | Sweep | Change |
|------|-------|--------|
| 2026-06-15 | 10 | Initial unified theory + five-model critique after rounds 1–10 corpus |
| 2026-06-15 | 11 | F-33 unit fix; clusters M–P; annual↔NPV bridge thesis; CBO layer split; disconfirmation #1 reframed |
| 2026-06-15 | 12 | **Two-corridor model:** EU27/UK/India/FB-white (Corridor B) federal annual **above** NH white US-born; Mexico/`<HS` (Corridor A) below. Matched-education kill: Mexico ≥ white at HS/some-college — aggregate gap = composition. Tensor: `eu27_origin`, `uk_origin`, `nh_white_all`, `fb_lt_hs`. Write-up: `immigration-europe-caucasian-fiscal-findings-2026-06-15.md`. **Blocked:** lifetime EU vs white until NAS college+ cells staged. |
| 2026-06-15 | 13–22 | **Three-layer annual:** `school_burden_per_adult` + `net_crude_federal_minus_school` in tensor; `v_three_layer_annual`. Initial Mexico crude ~−$13.5k/adult used the scenario subset denominator and is superseded by the 2026-06-15 denominator correction: $771 school/adult and +$748 crude annual. Memos: `immigration-school-burden-per-adult-2026-06-15.md`, `immigration-sweep-cycles-13-22-2026-06-15.md`. **Kill:** do not merge with lifetime NAS; UK/EU school rows thin-N. |
| 2026-06-15 | 23–32 | **NAS Table 8-13 college+ cells** staged (`HS` +$49k, some college +$205k, BA +$514k) → Mexico **synthetic age-25 benchmark +$45,631/adult** (education-mix weighted). **Microsim adult weights** revised school burden: Mexico $771/adult (was ~$15k with scenario N) → **crude annual net +$748** (fed $1,519 − school). Return-migration haircut scenarios in `life.return_migration_haircut_scenarios`. LPR xlsx still missing. Saiz median ε = 2.54 (269 MSAs). Memo: `immigration-sweep-cycles-23-32-2026-06-15.md`. **Still blocked:** EU27/NH-white lifetime rollup; UK/EU school rows thin-N; descendant attribution (Akers-Boustan mined only); age-at-arrival/current-age NPV for Mexico stock. |
| 2026-06-15 | session | **Stock vs flow:** Mexico multiply-out +$387.7B / +$46k/adult on **8.5M Mexico-born FB 25–64** is an **age-25 NAS benchmark applied to current stock education weights**, not actual current-stock lifetime NPV. BA+ **10.2%**. Biden: **~10.8M encounters ≠ +10M stock**; Pew **+3.5M** (2021–23), CIS **+5.6M** (2021–25). Mexico unauthorized **flat ~4.3M**. Cluster **Q** generators + memo `immigration-mexico-npv-population-synthesis-2026-06-15.md`. |
| 2026-06-15 | session | **Full ledger (cluster R):** +$46k synthetic NAS age-25 benchmark **not** net of school ($771/yr), state/local surge ($657/yr), CBP/ICE (~$2.1k/yr), courts, shelter. Honest annual crude **+$748**. Illustrative stacked band **−$37k to +$28k/adult** [INFERENCE]. Generators G-LIF-R01–R05; mining `cluster-r-full-ledger.json`. **Kill:** scalar Mexico net without ℓ vector. |
| 2026-06-16 | conclusion audit | **Synthesis confidence bound:** replaced "survives all datasets" / "data cannot kill" language with a current-warehouse-compatible working synthesis. New evidence can still kill channel magnitudes, cell signs, and annual-to-lifetime bridges; the robust correction is against exporting one scalar across layers. See `immigration-conclusion-audit-running-fixes.md`. |
