# Restrictionist corpus — full marker-modal parse + generator extraction (2026-06-15)

**Method:** `corpus ingest --parser marker-modal` on 9 restrictionist PDFs from PNY lifetime corpus → read full `page.md` parses in `~/Projects/corpus/sha_*`.

**Corpus IDs:**

| Paper | sha | parsed |
|-------|-----|--------|
| Borjas w9755 labor demand | `sha_ebb48fc02c714bfe` | ✓ |
| Borjas w11610 native migration | `sha_d18f2c501794dccc` | ✓ |
| BGH w12518 black employment | `sha_841c0a577e4ffa05` | ✓ |
| Gould w33655 asylum/homelessness | `sha_73e2279cb366d94b` | ✓ |
| Razin-Sadka-Swagel w15597 welfare state | `sha_e761985b0f6b84d8` | ✓ |
| Orrenius NAS fiscal wp1704 | `sha_c731d5cbb632176f` | ✓ |
| Hanson-Liu-McGee w23753 low-skill wave | `sha_c0bc44bdd41dad19` | ✓ |
| Razin-Wahba w17515 welfare magnet | `sha_15b1f196f1207bc6` | ✓ |
| Borjas w6175 intergenerational welfare | `sha_c3910a894c59e230` | ✓ |

**Frame:** Extraction for cluster S (restrictionist steel-man). Each paper yields **perspectives** (whose lens), **narratives** (argument arcs), **generators** (reusable audit prompts).

---

## Cross-paper perspective map

| Perspective | Papers | Core move |
|-------------|--------|-----------|
| **National cell econometrician** | Borjas w9755, w11610, BGH | Reject weak spatial correlations; identify on education×experience national cells |
| **Subgroup distributional** | BGH | Black men disproportionately harmed on employment + incarceration, not just wages |
| **Local episodic fiscal** | Gould | 2022–24 shelter spike = asylum inflow in 4 cities, not housing affordability alone |
| **NAS fiscal interpreter** | Orrenius | Public-goods allocation + marginal cost flip sign; state/local school concentration |
| **Political-economy dynamic** | Razin w15597, w17515 | Welfare generosity ↔ migration skill mix co-determined by coalitions / regime |
| **Supply-side demographer** | Hanson w23753 | Low-skill wave peaked; secular decline regardless of enforcement |

**Master narrative (restrictionist synthesis):** Immigration harms are **real but ledger-dependent** — national labor markets show wage/employment hits spatial studies miss; fiscal costs concentrate **state/local + schooling + episodic shelter**; political equilibrium favors **unskilled-heavy inflows + redistribution** unless policy sorts migrants by skill.

---

## Paper-by-paper extraction

### 1. Borjas w9755 — Labor demand curve is downward sloping

**Perspective:** Competing-native worker in **national** education×experience cell (men 18–64, 1960–2000 censuses + CPS).

**Narratives:**
1. **Samuelson textbook** — supply shock → lower competing wages; NAS/Friedberg "small effect" contradicts theory given massive inflows. [SOURCE: abstract, §I]
2. **Spatial correlation trap** — Card Mariel null is artifact of local adjustment; weak MSA correlations ≠ zero national harm. [SOURCE: §II]
3. **Experience cell identification** — immigrant supply uneven within schooling groups over time → identifies national elasticity where education-only aggregation fails. [SOURCE: §II–III]
4. **Two-thirds attenuation** — state-level wage elasticity −0.13 vs national −0.40; spatial arbitrage hides ~⅔ of national effect. [SOURCE: §V, Table V vs III]
5. **1980–2000 cumulative harm** — 11% labor supply increase → average native wage −3.2%; HS dropouts −8.9%. [SOURCE: §VIII]

**Key parameters:** 10% cell supply → **−3–4%** weekly wages; annual earnings −6.4%; weeks worked −3.7pp. [SOURCE: Table III, abstract]

**Generators:**
- **G-LIF-S06** — Before citing Card spatial null, require national education×experience cell regression or document attenuation factor.
- **G-LIF-S07** — Decompose reported wage effect into {weekly, annual, weeks worked} — immigration may reduce labor supply not just wages.

---

### 2. Borjas w11610 — Native internal migration attenuation

**Perspective:** Native worker choosing whether to leave immigrant-penetrated local labor market.

**Narratives:**
1. **Reconcile spatial vs national puzzle** — local ≈0, national large → native migration diffuses harm. [SOURCE: abstract, §VI]
2. **Vote with your feet** — per 10 immigrants: **−2 natives** at state level, **−3 to −6** at MSA. [SOURCE: §VI Summary]
3. **Attenuation arithmetic** — native mobility explains **40%** (state) to **60%** (MSA) of national-vs-local wage gap. [SOURCE: abstract, §VI]
4. **Incomplete adjustment** — capital/goods flows also matter; migration is partial not full. [SOURCE: §VI closing]

**Generators:**
- **G-LIF-S08** — For any local labor-market immigration study, estimate native in/out-migration offset before interpreting wage coefficient as structural.

---

### 3. BGH w12518 — Black employment & incarceration

**Perspective:** African-American men in education×experience cells; formal vs crime sector.

**Narratives:**
1. **Missing link** — literature on black employment decline + incarceration rise ignored immigration. [SOURCE: §I]
2. **Crider anecdote** — enforcement → Hispanic exit → wage bump → black hiring (journalistic anchor). [SOURCE: §I]
3. **Triple margin** — 10% supply shock: black wage **−4.0%**, employment **−3.5pp**, incarceration **+0.8pp** (vs white employment −1.6pp, incarceration +0.1pp). [SOURCE: abstract, §I]
4. **State-national synthesis** — state regressions misspecified without national supply term; fixed spec matches national. [SOURCE: §I]
5. **1980–2000 attribution** — immigration accounts for **~40%** of 17.9pp black employment drop; **~10%** of incarceration rise among HS dropouts — "numerically important" but not majority. [SOURCE: §VII Summary]
6. **Caution frame** — authors stress controls incomplete; much decline unexplained. [SOURCE: §VII]

**Generators:**
- **G-LIF-S02** (existing) — require BGH-style subgroup rows before distributional harm from NAS averages.
- **G-LIF-S09** — For labor harm claims, check {wage, employment, incarceration} triple; wage-only misses black-specific margins.

---

### 4. Gould w33655 — Asylum seekers & homelessness

**Perspective:** Local shelter administrator / HUD PIT counter; restrictionist-leaning (AEI funding). [FRAMING-SENSITIVE]

**Narratives:**
1. **Affordability narrative challenged** — HUD +43% sheltered homeless 2022–24; media blames housing costs; authors attribute **~60%** to asylum seekers. [SOURCE: abstract, §1]
2. **Four-city concentration** — NYC, Chicago, MA, Denver = **75%** of national sheltered rise. [SOURCE: abstract]
3. **Direct + indirect triangulation** — local admin data + Hispanic share counterfactual; estimates **59–62%**. [SOURCE: §6]
4. **Episodic fiscal shock** — NYC **\$137,600**/family-year shelter; MA up to **\$120,000**. [SOURCE: §6]
5. **Not unsheltered** — street homelessness trend predates asylum surge. [SOURCE: §6]
6. **40% unexplained** — housing costs, eviction cliff still matter. [SOURCE: §6]

**Generators:**
- **G-LIF-S04** (existing) — episodic shelter ℓ vs lifetime NAS.
- **G-LIF-S10** — Split HUD PIT into {sheltered asylum-attributable, sheltered other, unsheltered} before fiscal stack synthesis.

---

### 5. Orrenius wp1704 — NAS fiscal sensitivity

**Perspective:** NAS panel member explaining **allocation rules** to policymakers.

**Narratives:**
1. **Everyone is a net drain in deficit era** — cross-section 2013: immigrants −\$5,021/capita (avg public goods) but so are natives; immigrants cover **93%** of benefits vs natives **77%** under marginal public goods. [SOURCE: Table 1, §Conclusion]
2. **Public goods pivot** — avg-cost → negative; marginal-cost → federal **+\$963** for 1st gen immigrants. [SOURCE: abstract, Table 1]
3. **State/local school concentration** — immigrant cost "most acute" locally due to children + lower income. [SOURCE: abstract, §]
4. **Dynamic flip** — recent immigrant NPV up to **+\$259k** (marginal public goods); `<HS` still **−\$117k** but **\$200k less costly than native dropout**. [SOURCE: Table 2–3]
5. **Restrictionist use:** cite `<HS` lifetime negative + local school; expansionist use: marginal federal + recent cohort positive.

**Generators:**
- **G-LIF-A02** (existing) — public goods grid.
- **G-LIF-S11** — Orrenius table: always pair avg-cost row with marginal-cost row + state/local row before restrictionist scalar.

---

### 6. Razin-Sadka-Swagel w15597 — Migration & welfare state (dynamic PE)

**Perspective:** Three voter groups (skilled, unskilled, old) in Markov-perfect political equilibrium.

**Narratives:**
1. **Friedman constraint** — cannot have free immigration + generous welfare simultaneously. [SOURCE: §1]
2. **Young high-fertility migrants** — improve dependency ratio but unskilled may be net beneficiaries. [SOURCE: §2, NAS 1997 cite ~\$100k `<HS` burden]
3. **Coalition blocking** — skilled+unskilled vs unskilled+old strategic alliances to block third group. [SOURCE: abstract]
4. **Unskilled policy dominance** — unskilled ideal policies appear in equilibrium **more often than group size**. [SOURCE: abstract]
5. **Good vs bad migration (Sinn)** — productivity-driven vs welfare-magnet-driven. [SOURCE: §2]

**Generators:**
- **G-LIF-S05** (existing) — Razin policy co-evolution.
- **G-LIF-S12** — Simulate {τ, μ, σ} policy vector change on fiscal sign of fixed ACS cell.

---

### 7. Razin-Wahba w17515 — Welfare magnet hypothesis

**Perspective:** Cross-country comparison EUR free movement vs non-EUR restricted.

**Narratives:**
1. **Regime conditions magnet** — generous welfare + **free migration** → unskilled magnet; **restricted** → voters select skilled (fiscal burden internalized). [SOURCE: abstract]
2. **EUR vs US skill mix** — EUR more unskilled immigrants despite similar generosity → policy not generosity alone. [SOURCE: §1]
3. **Empirical punchline** — magnet hypothesis holds in free regime; fiscal-burden/skill-selectivity holds in restricted regime. [SOURCE: abstract]

**Generators:**
- **G-LIF-S13** — Tag every welfare-magnet claim with {free vs restricted mobility regime}; block cross-regime inference.

---

### 8. Hanson-Liu-McGee w23753 — Rise and fall of low-skilled immigration

**Perspective:** Macro demographer + labor-market tightness; **reframes restrictionist panic** toward secular slowdown.

**Narratives:**
1. **Post-recession stall** — undocumented −160k/yr 2007–14; low-skill stock flat. [SOURCE: abstract]
2. **Secular not cyclical** — Latin American fertility decline + US-Mexico income gap shrink → inflows unlikely to rebound. [SOURCE: §Intro]
3. **Counterfactual wage gap** — if low-skill inflow had continued 2008–15 pace, skill premium **6–9pp higher** in 2015. [SOURCE: §Intro]
4. **Policy implication inversion** — problem is preparing for **lower** immigration, not stopping a wave. [SOURCE: abstract]
5. **Mexico selection neutral** — by 2010 migrants ≈ random draw from Mexican skill distribution. [SOURCE: §Intro]

**Generators:**
- **G-LIF-S14** — Stock-flow + secular supply forecast before "flooding" rhetoric; pair Hanson w23753 with Pew stock series.

---

### 9. Borjas-Sueyoshi w6175 — Ethnicity & intergenerational welfare dependency

**Perspective:** Ethnic-group "capital" externality on human capital + welfare stigma/information channel (NLSY 1979–89).

**Narratives:**
1. **Ethnic persistence** — welfare incidence and spell duration differ by ethnicity and **persist across generations**. [SOURCE: abstract]
2. **80% transmission** — ~**80%** of parental-generation welfare participation gap between ethnic groups transmits to children. [SOURCE: abstract]
3. **Ethnic capital model** — group average skills + group welfare propensity spill over to children's welfare decisions. [SOURCE: §II]
4. **Immigration policy hook** — national-origin skill/welfare differences → long-run costs if visa policy ignores skill selectivity. [SOURCE: §I]

**Generators:**
- **G-LIF-S15** — Intergenerational fiscal claims: separate {parental welfare, ethnic environment, own earnings} channels.

---

## New generators (cluster S extension)

| ID | Prompt | Negative space |
|----|--------|----------------|
| G-LIF-S06 | National education×experience cell required before Card citation | Spatial null as sufficient statistic |
| G-LIF-S07 | Decompose wage impact into weekly / annual / weeks worked | Wage-only labor harm |
| G-LIF-S08 | Estimate native migration offset for local wage studies | MSA coefficient = structural elasticity |
| G-LIF-S09 | Triple margin {wage, employment, incarceration} for subgroup claims | NAS education average as distributional harm |
| G-LIF-S10 | HUD PIT decomposition sheltered-asylum vs other vs unsheltered | Homelessness = affordability only |
| G-LIF-S11 | Orrenius dual-scenario + federal/state split mandatory | Single NAS table cell as politics |
| G-LIF-S12 | Razin {τ, μ, σ} shock on fixed ACS fiscal cell | Static NAS invariant to policy |
| G-LIF-S13 | Welfare-magnet claims require mobility-regime tag | EUR free-movement evidence → US policy |
| G-LIF-S14 | Hanson secular supply + Pew stock before influx rhetoric | Encounters = permanent residents |
| G-LIF-S15 | Intergenerational welfare: separate parental / ethnic / earnings channels | Immigrant NPV = ethnic externality |

**Cluster S totals after parse:** 9 papers fully read, **15 generators** (S01–S15), **21 tagged claims** in `.mining/immigration-lifetime-cluster-s-restrictionist.json`.

---

## Narrative grammar (how restrictionists chain papers)

```
[Labor national]  w9755 elasticity → w11610 "you don't see it locally"
       ↓
[Subgroup]        BGH black employment/incarceration
       ↓
[Fiscal lifetime] Orrenius/NAS `<HS` negative (avg public goods)
       ↓
[Fiscal flow]     Gould shelter $ + FAIR annual (not marker-parsed)
       ↓
[Political]       Razin coalitions / magnet under free movement
       ↓
[Supply fear]     Hanson REJECTS eternal wave — but 6–9pp counterfactual used selectively
```

**Strongest post-parse fair claim:** Restrictionists are right that **identification unit** (national cell, subgroup, local episodic, public-goods allocation) changes the sign and magnitude — wrong to collapse into one scalar.

**Disconfirmation (mandatory):**
- Hanson: secular **decline** in low-skill inflows undermines "accelerating flood" without stock-flow discipline.
- Orrenius: marginal public goods + recent cohort **+\$259k** undermines undifferentiated "immigrants are drains."
- BGH: immigration explains **minority share** of black employment/incarceration trends.
- Gould: **40%** of shelter rise non-asylum; unsheltered trend separate.

---

## Revisions

- **2026-06-15:** Initial memo from marker-modal full parse of 9/9 restrictionist PDFs.
