# Restrictionist immigration arguments — steel-man map (2026-06-15)

**Question:** What do papers arguing against immigration actually claim, step by step?

**Method:** Read primary sources in staged corpus (Borjas, BGH, Razin, Hanson, Gould, Orrenius/NAS, FAIR); follow argument chains; tag evidence level.

**Frame:** [FRAMING-SENSITIVE] Steel-man before evaluate. Restrictionist ≠ one argument — **six partially independent chains** that get collapsed in politics.

**Instrument:** LLM may under-weight restrictionist fiscal/local channels — cross-check against corpus PDFs.

---

## Executive map

Restrictionists win politically when they **switch ledgers** the same way expansionists do — but toward **local flow, episodic shock, subgroup labor harm, and full-budget fiscal** instead of **GDP / complementarity / ITEP taxes**.

| Chain | Core claim | Best source | Our warehouse |
|-------|-----------|-------------|---------------|
| **L1 Labor** | More immigrants → lower wages / employment for competing natives | Borjas w9755, w11610 | Partial (earnings proxy, no wage panel) |
| **L2 Subgroup** | Black low-skill men hit on wages, employment, incarceration | BGH w12518 | Not built |
| **F1 Lifetime fiscal** | Low-education immigrants net fiscal drain over life | NAS 2017 Table 8-13; Orrenius wp1704 | Built (`lifetime_npv`) — **partial ℓ** |
| **F2 Annual advocacy ledger** | Unauthorized = $150B+ net cost all levels | FAIR 2023 [advocacy] | ITEP floor only; no reconciled FAIR/ITEP/Pew ledger |
| **C1 Local capacity** | Schools, shelter, homelessness spike with inflow | Gould w33655; receiver cities | School layer + episodic CSV |
| **P1 Political economy** | Low-skill immigration + welfare state → worse policy mix | Razin w15597, w17515 | Not modeled |
| **A1 Admin** | Border/courts/detention = real taxpayer cost | CBP/ICE budgets; EOIR staged | Cluster J, not allocated |

**Verdict:** Restrictionists are **often right that expansionists omit layers**; **often wrong** when they treat encounters as stock, FAIR as science, or NAS `<HS` as “all Mexicans.”

---

## Chain L1 — Labor market (Borjas)

### Argument structure

1. **Premise:** Immigrants and natives with same education are **not perfect substitutes** across experience cells; supply shocks are national, not just local. [SOURCE: Borjas w9755]
2. **Mechanism:** Immigration shifts supply within education×experience cells → **downward-sloping labor demand** → lower wages for competing workers.
3. **Evidence:** 10% increase in cell supply → **3–4% wage decline** (1960–2000 censuses + CPS). [SOURCE: Borjas w9755, abstract]
4. **Local-market critique:** City-level studies (Card) miss effect because **natives and capital leave** — wage hit is diluted geographically. [SOURCE: Borjas w11610]
5. **Migration attenuation:** Native in-migration falls, out-migration rises; local wage effect is **40–60% smaller** than national cell effect because natives flee high-immigrant markets. [SOURCE: Borjas w11610, abstract]
6. **Policy implication [THEIR WORDS]:** Large low-skill inflows harm competing native workers; restriction / lower inflows protect native wages.

### What survives disconfirmation

- **Mariel / area studies:** Card null in Miami; Borjas w21850, w23504 dispute with race/experience composition — **contested**, not settled. [CONTESTED EVIDENCE]
- **GE offsets:** Peri-Ottaviano complementarity, Clemens capital-tax — partial fiscal/labor offsets. [SOURCE: unified theory M2]
- **Our E-Verify TWFE:** Weak native wage response in QWI panel — see `immigration-causal-everify-card-vs-borjas.md`.

### What restrictionists get right

National **education×experience** framing is more coherent than “city has immigrants → city wages” for **incumbent workers in competing cells**.

---

## Chain L2 — Subgroup incidence (Borjas–Grogger–Hanson)

### Argument structure

1. **Premise:** Black male employment fell sharply 1960–2000; incarceration rose (9.6% black men, 21.2% black dropouts institutionalized by 2000). [SOURCE: BGH w12518]
2. **Mechanism:** Immigrants cluster in low-skill labor markets where black men compete; supply shock → lower wages, lower employment, **higher incarceration** (not just crime rates).
3. **Evidence:** 10% immigrant-induced supply increase in a skill group → **−4.0% black wage**, **−3.5 pp employment rate**, **+0.8 pp incarceration rate**. [SOURCE: BGH w12518, abstract]
4. **Anecdote anchor:** Crider plant — post-raid wage hike for black workers when Hispanic workforce left. [SOURCE: BGH, WSJ 2007 epigraph]
5. **Policy implication:** Immigration policy is **distributional** inside the US, not only efficiency vs foreigners.

### Disconfirmation

- Crack epidemic, minimum wage, disability programs — BGH acknowledges; claim is **incremental** immigration effect on top. [SOURCE: BGH intro]
- **Not in our tensor** — need subgroup rows, not education-average NAS cells.

---

## Chain F1 — Lifetime fiscal negative (NAS + Orrenius)

### Argument structure (academic restrictionists)

1. **Premise:** Immigrants pay taxes and use services over life cycle; education at arrival pins earnings path. [SOURCE: NAS 2017]
2. **Mechanism:** Low-education arrivals → low lifetime taxes, high transfer use, **K-12 cost of children** at state/local level.
3. **Evidence:** `<HS` individual at age 25 → **−$109k** NPV (2012$, CBO outlook, public goods excluded). [SOURCE: NAS Table 8-13; warehouse]
4. **Orrenius nuance (still negative for low-skill):** If **average** public goods assigned → negative federal+local; costs **concentrated state/local, largely schooling**; marginal public goods → long-run less negative. [SOURCE: Orrenius Dallas Fed wp1704, abstract]
5. **Policy implication:** Low-skill immigration is a **taxpayer subsidy** to immigrants and employers; high-skill immigration is the opposite (+$514k BA cell).

### Where restrictionists overreach

- Collapse to **one scalar** per origin (Mexico +$46k mix kills monolithic “Mexican drain” — see synthesis memo).
- Ignore **descendants booked separately** — child costs partly in descendant column, not individual.
- Ignore **ITEP tax floor** ($97B taxes paid by unauthorized) — restrictionists undercount taxes; expansionists undercount costs.

### Our warehouse alignment

- We have NAS cells + school crude layer; **missing:** courts, ICE, full state/local NPV, descendants.

---

## Chain F2 — FAIR / advocacy high-cost ledger

### Argument structure

1. **Premise:** Count all federal, state, local spend on unauthorized + US-born children of unauthorized. [SOURCE: FAIR 2023]
2. **Numbers:** **$182B** gross cost − **$32B** taxes = **$150.7B net**/yr; **$8,776**/illegal or US-born child of illegal; **15.5M** + **5.4M** citizen children. [SOURCE: FAIR 2023; Congress testimony Kirchner 2024]
3. **Mechanism:** Education, Medicaid, law enforcement, justice, general public services — **full budget**, not NAS cell.
4. **Policy implication:** Massive net drain; every taxpayer **~$956–1,156**/yr.

### Critical limits [DISCONFIRMATION]

- **Advocacy org**, not peer-reviewed; stock **15.5M** > Pew **14M** [FRAMING-SENSITIVE]
- **Citizen children** counted as cost of immigration — normative accounting choice
- Benefit use often at **household** level; tax at **individual** level — asymmetric
- **Compare:** ITEP **$96.7B** taxes (2022, 10.9M stock) — different stock year/method [SOURCE: cluster G]
- **Our stance:** Use FAIR as an **advocacy high-cost ledger**, not empirical fact and not a proven mathematical upper bound — but **don't ignore** that a full-budget line exists and NAS individual NPV doesn't include it all.

---

## Chain C1 — Local capacity & episodic shock

### Argument structure (Gould et al.)

1. **Premise:** HUD sheltered homelessness **+43%** 2022–2024 after 16-year decline. [SOURCE: Gould w33655, abstract]
2. **Mechanism:** Asylum seekers placed in **emergency shelter** in NYC, Chicago, Massachusetts, Denver — not absorbed by private housing market.
3. **Evidence:** **~60%** of two-year rise in sheltered homelessness = asylum seekers (direct local gov + demographic methods). [SOURCE: Gould w33655]
4. **Policy implication:** Surge-era immigration created **visible local fiscal/social crisis** independent of lifetime NAS averages.

### Repo alignment

- NYC **$3.7B** FY24 shelter — `receiver_city_migrant_costs` [SOURCE: cluster P]
- **Kill-test survived** in surge memo for receiver political swing
- **Not** in the synthetic Mexico age-25 NAS benchmark; **is** in restrictionist “system collapse” story

### Hanson composition (w23753) — supporting thread

- Low-skilled immigration **slowed** post-2007; undocumented **declined**; selection from Mexico less negative over time. [SOURCE: Hanson w23753 abstract region]
- Restrictionist use: when inflows **resume** (2021–23), wage pressure on low-skill natives returns — Hanson implies **+24% wage effect** if inflow had stayed at 1994–2007 pace [INFERENCE from Hanson model discussion in paper].

---

## Chain P1 — Welfare state & magnets (Razin)

### Argument structure

1. **Premise:** Welfare state = tax-financed demogrant; three voter groups (skilled, unskilled, old). [SOURCE: Razin w15597]
2. **Mechanism:** Migrants arrive young, higher fertility → shift political coalitions → equilibrium **tax rate, migrant skill mix, migrant count** respond.
3. **Prediction:** Unskilled voters' preferred policies featured more often than group size would suggest; **fiscal burden and redistribution** drive voting coalitions. [SOURCE: Razin w15597, abstract]
4. **Magnet extension (Razin–Wahba w17515):** Generous welfare **attracts** low-skill migrants — fiscal sign depends on **destination policy**, not immigrant fixed effect. [SOURCE: cluster O generators]
5. **Policy implication:** Immigration + welfare expansion = **fiscal unsustainability** and wrong skill mix; restrict low-skill or restrict benefits.

### Our gap

Not in DuckDB — political ℓ layer. Explains why **fiscal sign co-evolves** with policy (matches unified theory M5).

---

## Chain A1 — Justice, legal, enforcement

### Argument structure (political + think-tank, partial academic)

1. **Premise:** Immigration creates **administrative state** costs not in NAS education NPV.
2. **Items:** CBP/ICE **~$29.5B** FY25; detention **~$187/bed-day**; EOIR court backlog; asylum processing. [SOURCE: cluster J]
3. **Mechanism:** More unauthorized / more asylum → more apprehensions, bed-days, court cases → **marginal taxpayer cost per entrant**.
4. **FAIR line items:** Law enforcement, justice, general expenditures in **$182B** gross. [SOURCE: FAIR 2023]
5. **Policy implication:** Even immigrants who pay some taxes **impose enforcement externalities**.

### Our gap

Cluster J mined budgets; **not allocated** to `mexico_origin` or unauthorized path — validates user critique on +$46k NPV.

---

## Borjas welfare assimilation (w4872) — older fiscal thread

1. **Claim:** Immigrant welfare use **rises with assimilation** (time in US) — opposite of naive “they don't use benefits.” [SOURCE: Borjas w4872 — corpus; not re-read full text this session]
2. **Use in restrictionist rhetoric:** Amnesty / long residence → **higher fiscal cost** over life.
3. **Pairs with:** Razin magnets, Bitler-Hoynes PRWORA participation patterns [SOURCE: cluster C generators]

---

## How restrictionists argue (rhetorical grammar)

From `immigration-economist-rhetorical-failures.md` — **mirror image**:

| Move | Restrictionist version |
|------|------------------------|
| Ledger switch | NAS `<HS` lifetime → “all immigration” |
| Flow → stock | CBP encounters → “millions living here” |
| Advocacy high-cost ledger | FAIR $150B; Gould 60% homelessness as episodic-city evidence |
| Erase offsets | Ignore ITEP taxes, Clemens capital tax, CBO GDP |
| Capacity as proof | NYC shelter = entire national story |
| Subgroup → average | BGH black effects → all natives harmed |

**Strongest fair restrictionist claim (repo-aligned):**

> Low-skill, surge-era, unauthorized-heavy inflows can be **federal-positive on thin annual cash-flow** while **lifetime-negative on education cells**, **locally catastrophic on shelter/school**, and **administratively expensive** — and these are **compatible**.

That is essentially our unified theory sentence 1 — restrictionists are right on **layer multiplication**, wrong on **single-scalar panic**.

---

## Generators (cluster S — restrictionist steel-man)

| ID | Prompt |
|----|--------|
| G-LIF-S01 | For each restrictionist claim, extract {ledger, cell, cohort, layer} before agreeing/disagreeing |
| G-LIF-S02 | Map BGH subgroup results to required tensor rows — block education-only NAS for distributional claims |
| G-LIF-S03 | FAIR vs ITEP vs Pew stock reconciliation table before citing either in warehouse |
| G-LIF-S04 | Gould episodic $ vs NAS lifetime for same cohort year — which dominates incidence story? |
| G-LIF-S05 | Razin equilibrium: how does benefit eligibility change immigrant fiscal sign in ACS cells? |

---

## Disconfirmation summary (mandatory)

| Restrictionist claim | Status |
|---------------------|--------|
| All immigrants fiscal negative | **False** — NAS BA/+ cells strongly positive |
| All immigration hurts average native wages | **Contested** — Card/null areas; small average effects |
| 10M encounters = 10M new illegals | **False** — stock +3.5–5.6M |
| Crime wave from unauthorized | **Mostly false** — repo crime memo |
| Local shelter/school shock in surge cities | **True** as episodic ℓ — Gould 60%, NYC $B |
| Low-skill lifetime fiscal negative (individual NAS) | **True under NAS assumptions** for `<HS` cell |
| +$46k Mexico = net contributor all-in | **False** — missing admin, courts, full local |

---

## Papers read (this session)

| Paper | Role |
|-------|------|
| Borjas w9755 | Labor demand −3–4% |
| Borjas w11610 | Native migration 40–60% attenuation |
| BGH w12518 | Black wage/employment/incarceration |
| Razin w15597 | Welfare state political economy |
| Gould w33655 | Asylum → 60% homelessness rise |
| Hanson w23753 | Low-skill composition / slowdown |
| Orrenius wp1704 | NAS fiscal sensitivity, state/local school |
| FAIR 2023 | Advocacy full ledger $150.7B |

**Not read this session but in corpus:** Borjas w4872 welfare, Razin–Wahba w17515, Borjas Mariel papers, Camarota/CIS CPS residual.

---

## Next reads (corpus)

1. Razin–Wahba w17515 — welfare magnet empirical
2. Borjas w4872 — welfare assimilation full
3. Borjas w22102 — undocumented labor supply elasticity
4. Netzer / Reder fiscal studies (if staged)
5. FAIR methodology section vs ITEP line-by-line

---

## Revisions

| Date | Note |
|------|------|
| 2026-06-15 | Initial steel-man map from corpus PDFs + FAIR web |
| 2026-06-16 | Reframed FAIR from "upper-bound political ledger" to advocacy high-cost ledger; its assumptions are not a mathematical upper bound and need reconciliation against ITEP/Pew before warehouse use. See `immigration-conclusion-audit-running-fixes.md`. |
