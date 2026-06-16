# Restrictionist corpus — full section-by-section extract (2026-06-15)

**Method:** Read every main-body section of 9 marker-modal parses (`~/Projects/corpus/sha_*`). Appendices mined where they contain coefficients (BGH math appendix, w9755 Table VIII).

**Coverage:** 9/9 papers · 62 main sections · **~220 tagged claims** · 15 generators (S01–S15)

**Prior skim memo:** `immigration-restrictionist-corpus-parse-2026-06-15.md` (abstract/conclusion only — superseded for claims).

---

## Corpus index

| Paper | sha | Sections read |
|-------|-----|---------------|
| Borjas w9755 labor demand | `sha_ebb48fc02c714bfe` | I–VIII (skip var-def appendix except immigrant-share table) |
| Borjas w11610 native migration | `sha_d18f2c501794dccc` | I–VI |
| BGH w12518 black employment | `sha_841c0a577e4ffa05` | I–VII + measurement error + accounting |
| Gould w33655 asylum/homelessness | `sha_73e2279cb366d94b` | 1–6 + Table 1 |
| Orrenius NAS fiscal wp1704 | `sha_c731d5cbb632176f` | full (138 lines) |
| Razin-Sadka-Swagel w15597 | `sha_e761985b0f6b84d8` | 1–7 + App A |
| Razin-Wahba w17515 welfare magnet | `sha_15b1f196f1207bc6` | 1–6 + tables |
| Hanson-Liu-McGee w23753 | `sha_c0bc44bdd41dad19` | Intro + I–IV |
| Borjas-Sueyoshi w6175 welfare ethnicity | `sha_c3910a894c59e230` | I–VII |

---

## Cross-paper synthesis

### Perspectives (6)

| ID | Lens | Papers |
|----|------|--------|
| P-S01 | National edu×exp econometrician | w9755, w11610, BGH |
| P-S02 | Subgroup distributional (race) | BGH |
| P-S03 | Local episodic fiscal | Gould |
| P-S04 | NAS fiscal interpreter (avg vs marginal ℓ) | Orrenius |
| P-S05 | Dynamic political economy (3 voter groups) | w15597, w17515 |
| P-S06 | Secular supply demographer | w23753 |

### Narrative arcs (7)

| ID | Arc | Key numbers |
|----|-----|-------------|
| N-S01 | Spatial null is attenuated national harm | w9755: −0.40 national vs −0.13 state elasticity; w11610: migration explains 40–60% of gap |
| N-S02 | Black triple margin >> white | BGH: 10% supply → black emp −3.5pp, inc +0.8pp vs white −1.6pp, +0.1pp |
| N-S03 | Shelter spike ≠ affordability only | Gould: asylum 59–62% of +43% sheltered 2022–24 |
| N-S04 | Public-goods allocation flips sign | Orrenius: avg −$5,021 vs marginal federal +$963 (1st gen) |
| N-S05 | Welfare + open borders incompatible | w15597 Friedman; w17515 magnet (free) vs fiscal burden (restricted) |
| N-S06 | Low-skill wave peaked | w23753: undocumented −160k/yr post-2007; Mexico 15–40 stock <50% by 2040 |
| N-S07 | Ethnic welfare externality persists | w6175: ~80–84% of ethnic welfare gap transmits |

---

## Paper 1 — Borjas w9755 (51 claims)

| Sec | Core claims [SOURCE: section] |
|-----|------------------------------|
| **Abstract** | 10% cell supply → −3–4% wages; experience cells not perfect substitutes |
| **I** | Spatial lit ≈0 inconsistent with theory + large shocks; Card Mariel 7% workforce, null |
| **II** | Endogenous location + native/capital flows bias spatial correlations; BFK simulation only |
| **III** | 2000: 50% foreign-born among dropouts 10–20 yr exp; congruence G≈0.63 same-exp vs 0.53 diff-exp |
| **IV** | θ=−0.572 weekly (SE 0.162) → elasticity −0.40; annual −6.4%, weeks −3.7pp; IV −0.541; decade θ all negative |
| **V** | State θ=−0.124 to −0.217 vs national −0.533; **~⅔ hidden** at state level |
| **VI** | Effective exp: elasticity −0.30; wage-quantile cells: −0.42 |
| **VII** | σ_X=3.5, σ_E≈1.3; own factor-price ε −0.33 mean; 1980–2000 sim: dropout −8.9%, avg native −3.2% |
| **VIII** | Spatial conceals ⅔; policy needs full consequence accounting |

**Generators from full read:** G-LIF-S06 (national cell), G-LIF-S07 (weekly/annual/weeks triple), structural σ stress-test (σ_KL=0.75 → −4.2% avg wage).

---

## Paper 2 — Borjas w11610 (56 claims)

| Sec | Core claims |
|-----|-------------|
| **Abstract** | Migration attenuates local wage impact 40–60% |
| **I** | 69% immigrants in 6 states; national 3–4% vs spatial ≈0 puzzle |
| **II** | γ_W = η(1+γ_N); as t→∞ wage coef on immigration → 0 if migration completes |
| **III** | CA 80% dropout FB; decadal Δ native workforce negatively correlated with Δ immigrant share |
| **IV** | National θ_W=−0.533 → −4% per 10%; state −1.6%; MSA −0.043 (n.s.) |
| **V.A** | θ_N state −0.381 → **2.8 natives leave per 10 immigrants**; MSA −0.839 → **6.1** |
| **V.B** | In-migration θ=−0.151; out-migration +0.133 per 10 immigrants |
| **V.C** | Robust: drop CA, HS+ only, redefine dropouts |
| **V.D** | η=−0.389; migration explains **40% state / 60% MSA** of national-local gap |
| **VI** | Capital/goods flows unmeasured residual |

**Generators:** G-LIF-S08 (native migration offset); synthesis table 6 mechanical decomposition.

---

## Paper 3 — BGH w12518 (48 claims)

| Sec | Core claims |
|-----|-------------|
| **Intro** | Black emp 74.9→67.9%; dropout 72.1→42.1%; inc 0.8→9.6% (black men) |
| **II** | Perfect substitution not rejected (black-white, imm-native); crime sector natives-only |
| **IV national** | Table 2E: 10% → black wage −4.0%, emp −3.5pp, inc +0.8pp; white −4.1%, −1.6pp, +0.1pp; crack controls robust |
| **V state** | Misspecified state-only θ half national; **state+national sum ≈ national** |
| **Meas. error** | Aydemir-Borjas: sum of coefs identifies θ; rejects pure sampling-error story |
| **VI accounting** | 1980–2000 shock explains **~41%** black dropout emp decline, **~8%** incarceration rise |
| **VII** | Immigration numerically important but minority of trends |

**Generators:** G-LIF-S02, G-LIF-S09; state regression must include national share (BGH eq 13).

---

## Paper 4 — Gould w33655 (32 claims)

| Sec | Core claims |
|-----|-------------|
| **1** | Sheltered +43% (+149k); unsheltered +17%; challenges affordability-primary narrative |
| **2** | Top 4 cities = 75% of rise; parole 30.5k→1.7M pre-PIT |
| **3.2 direct** | NYC 66,700 (86.2% local Δ); Chicago 13,679 (93.8%); MA 7,821; Denver 4,300 |
| **3.2 indirect** | Hispanic share counterfactual; national **87,611 (58.95%)** |
| **4.3** | Direct 92,500 (62.2%) vs indirect 87,611 — triangulation |
| **5** | Caveats: non-Hispanic asylum understated; displacement → effect understated; **40% unexplained** |
| **5.2 fiscal** | NYC **$137,600**/family-yr shelter; MA up to $120k; FY25 NYC asylum $3.28B |
| **6** | Asylum **59–62%** of sheltered rise; unsheltered separate phenomenon |

**Generators:** G-LIF-S04, G-LIF-S10; Table 1 as scenario ledger input.

---

## Paper 5 — Orrenius wp1704 (18 claims)

| Sec | Core claims |
|-----|-------------|
| **Static T1** | Avg public goods: 1st gen **−$5,021**; marginal: total **−$782**, federal **+$963**, S&L −$1,746 |
| **Dynamic T2** | Recent immigrant NPV **+$259k** (no public goods); `<HS` recent **−$117k** |
| **Imm-native diff** | Low-skilled immigrant **~$200k less costly** than native dropout (75yr) |
| **Conclusion** | Immigrants cover **93%** of benefits vs natives **77%** (marginal PG); S&L school concentration |

**Generators:** G-LIF-S11; G-LIF-A02 public-goods grid; never cite avg-cost alone.

---

## Paper 6 — Razin w15597 (theory — 35 claims)

| Sec | Core claims |
|-----|-------------|
| **2** | NRC `<HS` burden ~$100k PV; EU aging 20%→40% elderly ratio |
| **4 sincere** | Old decisive → τ=1/(1+ε) Laffer max, μ=1; skilled → τ=0; unskilled → intermediate τ, σ=1 |
| **4.2** | Fiscal leakage: low-σ migration can shrink welfare state |
| **4.3 endog wages** | ∂τ^u/∂σ sign **flips** vs fixed wages |
| **5 strategic** | Coalitions: skilled+unskilled vs old OR unskilled+old vs skilled; τ̃ cutoff |
| **5 equilibria** | Intermediate / Left-winged (old policies) / Right-winged (τ=0) |
| **6 dynamics** | Strategic μ* > sincere restricted μ; unskilled policies featured most often |
| **7** | Skilled migrants help fiscally but threaten via offspring political power |

**Generators:** G-LIF-S05, G-LIF-S12 {τ, μ, σ} shock.

---

## Paper 7 — Razin-Wahba w17515 (28 claims)

| Sec | Core claims |
|-----|-------------|
| **Intro** | EUR social spending ~21% GDP vs US ~18%; EUR more unskilled immigrants |
| **Theory** | Free regime: dσ/dτ<0 (magnet); restricted: skilled voter dσ^e/dτ>0 (fiscal burden) |
| **Data** | Free EUR skill diff +15.77% vs restricted non-EUR DC +59.36% |
| **IV results** | Magnet β₂<0 (free); B×R β₃>0 (restricted); 1% benefits → skill diff +2–3.5% (IV) |
| **Flows** | Table 7 confirms stock results |
| **Conclusion** | Regime conditions magnet vs selectivity; EU harmonization may reduce magnet |

**Generators:** G-LIF-S13 mobility-regime tag.

---

## Paper 8 — Hanson w23753 (42 claims)

| Sec | Core claims |
|-----|-------------|
| **Intro** | Undocumented +510k/yr (1990–07) → −160k/yr (07–14); low-skill stock 8.5→17.8M then flat |
| **I.C selection** | Mexico 1990 mild positive → **2010 ~random draw** from wage distribution |
| **II.C demographics** | 10% rel labor supply → +1.4pp decadal migration; explains >80% of 00s drop |
| **II.C recession** | GDP shock explains only ~109k vs >1.1M observed drop |
| **III.A forecast** | Mexico age 15–40 in US **<50% by 2040**; LA under-40 8.8→4.9M |
| **III.B Katz-Murphy** | γ₁=−0.42 (college vs ≤HS); counterfactual 2015 premium **6–9pp higher** if inflows continued |
| **IV** | Policy shift to aging foreign-born fiscal burden; enforcement >$20B/yr |

**Generators:** G-LIF-S14; Katz-Murphy as partial-equilibrium magnitude only.

---

## Paper 9 — Borjas w6175 (47 claims)

| Sec | Core claims |
|-----|-------------|
| **Abstract** | ~**80%** ethnic welfare participation gap transmits |
| **II model** | Ethnic capital k̄ + group welfare rate p̄ affect child welfare propensity |
| **III data** | Parent on welfare: child rate 35% vs 10.1%; BLK 22.6% vs ENG ~9% incidence |
| **IV incidence** | γ₁=0.770 parental; γ₂=3.065 ethnic (~4×); 10pp parental-gen gap → 8.4pp child (84%) |
| **IV ME** | Omitting ethnic var underestimates transmission ~75% |
| **V duration** | Parental + ethnic welfare lower exit hazard; +10pp ethnic rate → spell 19.1→22.2 mo |
| **VI meas error** | θ₂/θ₁>1 needs implausible >40% misreport to be spurious |
| **VII** | Ethnicity matters; mechanism for policy unspecified |

**Generators:** G-LIF-S15 intergenerational channels.

---

## Restrictionist argument chain (full-read verified)

```
w9755 national ε≈−0.40
  → w11610 natives flee (2–6 per 10 immigrants) → local studies miss harm
  → BGH black emp/inc margins larger than wage-only story
  → Orrenius `<HS` −$117k lifetime BUT −$200k vs native dropout
  → Gould NYC $137k/yr episodic (local ℓ)
  → w15597/w17515 political equilibrium + magnet under free movement
  → w23753 SECULAR DECLINE undermines permanent "flood" without stock discipline
  → w6175 intergenerational welfare persistence (visa selectivity argument)
```

**Strongest fair claim (post full read):** Harm is real and **multi-ledger** — labor (national cell), subgroup (BGH), fiscal (Orrenius marginal vs avg), local episodic (Gould), political (Razin). **Weakest restrictionist overreach:** treating encounters as stock (Hanson falsifies); citing NAS avg public goods only (Orrenius §Conclusion).

---

## Claim register

Machine-readable expansion: `research/.mining/immigration-lifetime-cluster-s-restrictionist-full.json` (220 claims, section refs).

## Revisions

- **2026-06-15:** Full section-by-section read of 9 marker-modal parses; supersedes abstract-only extract.
