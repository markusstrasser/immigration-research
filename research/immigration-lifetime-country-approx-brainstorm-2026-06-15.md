# Brainstorm — approximating lifetime fiscal +/- to the country (1st–3rd order)

**Date:** 2026-06-15
**Trigger:** Distribution findings now show a **~1.8× per-adult federal proxy** (NH white US-born vs Mexico-origin) on the built native-white microsim, mostly education composition rather than per-pupil cost — but **lifetime NPV** and **country-level net** still need a stacked approximation.
**Prior:** `research/immigration-federal-distribution-findings-2026-06-15.md`, `research/immigration-lifetime-unified-theory-2026-06-15.md`
**Rule:** No scalar “US immigration is +$X” or “Mexico is −$Y” — output is **cell × layer × time** with explicit order tags.

---

## Central object (target output)

\[
\mathcal{F}_{\text{country}}(\text{cell}, \ell, t) = \underbrace{\mathcal{F}^{(1)}}_{\text{direct ledger}} + \underbrace{\mathcal{F}^{(2)}}_{\text{market GE}} + \underbrace{\mathcal{F}^{(3)}}_{\text{political / spatial / dynamic}}
\]

- **cell** = education × age-at-arrival × legal path × state/PUMA × origin-composition weight
- **ℓ** = federal_annual | lifetime_npv | state_local | local_episodic | private_transfer | admin
- **t** = stock vs surge cohort vs policy counterfactual

**Country rollup:** \(\sum_{\text{cells}} w_{\text{cell},t} \cdot \mathcal{F}(\text{cell},\ell,t)\) — weights from ACS/SIPP/CBO, **never** origin label alone.

---

## Perturbation 1 — Denial cascade (if microdata never arrives)

What still bounds **country lifetime +/-**?

1. **NAS/NRC education NPV table only** — bounds `<HS` … college+ × {individual, descendants}; ACS supplies **weights only**. [SOURCE: corpus NAS 2017]
2. **CBO surge federal vs state-local split** — bounds **ℓ fight** at country level for 2021+ path, not stock lifetime. [SOURCE: CBO 60569/61256 memos]
3. **Static composition shift** — re-weight NAS cells to 2023 ACS education mix → **country stock sensitivity**, not point estimate.
4. **Discount/mortality band** — SSA/CDC life tables + 2–4% real → **sign stability** test, not precision.
5. **Remittance private layer** — World Bank outflows as **lower bound on uncounted household offset** to public ledger. [SOURCE: WB JSON in lifetime corpus]
6. **If only annual proxies exist** — annuitize + declare **incomparable** to NAS without public-goods grid (G-LIF-M01).

**Floor conclusion:** Without micro, country lifetime sign is **education-mix dominated**; direction for **low-education-heavy inflow** leans negative on NAS grammar; **high-education mix** leans positive — same country, opposite sign by cell weights.

---

## Perturbation 2 — Domain forcing (who owns which order)

| Order | Domain | Mechanism | Data we have | Gap |
|-------|--------|-----------|--------------|-----|
| **1st** | Public finance / microsim | Taxes − transfers − allocated spending by age | NAS cells, SIPP/MEPS bridge, ITEP floor | Native-born symmetric microsim; income tax |
| **1st** | Demography | Survival, fertility, descendants | CDC life tables; NAS descendant column | PSID / Synthetic SIPP |
| **1st** | Education | K-12 + postsecondary cost paths | Fixed per-pupil (~$21k), NCES | Marginal vs average pupil |
| **2nd** | Labor GE | Wages, employment, task mix | Card-Peri, Clemens capital-tax | Map wage → federal cell |
| **2nd** | Capital / firm | Payroll on owner side, investment | Clemens +$128k flip | `<HS` US magnitude |
| **2nd** | Housing | Rent incidence, local taxes | Saiz + stage2/5 | Country aggregate vs destination |
| **3rd** | Political economy | Skill mix of migrants × welfare policy | Razin w15597, LPR mix xlsx | US estimation |
| **3rd** | Spatial equilibrium | Native out-migration, sorting | Borjas w11610 | Link to fiscal geography |
| **3rd** | Dynamic composition | Surge vs stock, return migration | Hanson, Duleep-Regets | US return fiscal micro |
| **3rd** | Restriction / admin | Deportation, CBP/ICE, lost GDP | CBO 60569 invert, admin PDFs | Mass-deport PDF blocked |
| **3rd** | Innovation / long run | Productivity, patents | Hunt/Kerr (not in warehouse) | High-order, wide bands |

---

## Perturbation 3 — Constraint inversion

| Inversion | Approximation strategy |
|-----------|------------------------|
| **Only lifetime NPV, no annual** | NAS table × ACS weights; ignore SIPP +$1,519/yr unless bridge built |
| **Only annual, no lifetime** | CBO 60569/61256 + scenario ledger — **surge-era country**, not 75yr stock |
| **Only local, no federal** | Receiver cities + per-pupil × school-age share — **city/state incidence** |
| **Only federal, no state/local** | Current mistake in political debate; CBO already shows split |
| **Only immigrants, no natives** | NAS pairs immigrant vs native in same education cell — **relative**, not country total |
| **Only 1st order** | Deliberately omit Clemens/Colas — **lower bound on optimism** for restriction case |
| **Include 2nd order** | Add capital-tax adjustment + Card-Peri wage band to earnings path before integrating NPV |
| **Include 3rd order** | Monte Carlo over {return migration, housing ε, policy adjustment, descendant path} |

---

## Candidate approximation architectures (15 ideas)

### Tier A — Buildable with current warehouse (next 1–2 sessions)

**A1. Composition-weighted NAS country stock**
Multiply NAS `{education × age-at-arrival}` NPV cells by ACS 2023 foreign-born weights (and separately by Mexico-weighted slice). Output: **distribution of NPV**, not scalar.
*1st order only.*

**A2. Two-ledger country dashboard**
Parallel rollups: (i) lifetime_npv NAS grammar, (ii) federal_annual SIPP proxy — same cells, **never summed**.
*Kills layer laundering.*

**A3. Annual-to-lifetime bridge grid**
For each education cell: annuitize NAS NPV at {2,3,4}% vs microsim federal net; tag MATCH / SCOPE_MISMATCH.
*1st order consistency check.*

**A4. Surge vs stock country tags**
CBO 2024–34 federal path for surge cohort; ACS stock weights for NAS — **two country objects**, same chart.

**A5. Private remittance offset layer**
WB remittance per origin ÷ weighted adults — subtract from public net only in **household welfare** view, not government ledger.
*1st order private ℓ.*

**A6. Local episodic country upper bound**
Sum receiver-city shelter + (per-pupil × school-age children × FB stock) — **gross local shock**, not lifetime NPV line.

### Tier B — Needs one new data pipe

**B7. Native-born SIPP donor symmetry**
Extend `build_federal_microsim_sipp_2024.py` to `EBORNUS=1` — enables white vs Mexico **same machinery** at cell level.

**B8. PSID / NAS descendant calibration**
Replace NAS descendant column with estimated intergenerational transition by parent education × nativity.

**B9. Return-migration attrition integrator**
Duleep-Regets selective emigration → reduce effective horizon in NPV integral (sensitivity band, not point).

**B10. State-level country decomposition**
ACS state × education × NAS cell + stage5 Medicaid/EL + per-pupil — **federal country vs state-country**.

### Tier C — 2nd order (GE stack)

**C11. Earnings-path fan on NAS cells**
Three paths per `<HS` cell: Borjas pessimistic, Card-Peri baseline, Clemens-GE optimistic → re-run payroll/spending integrals.

**C12. Capital-tax overlay (Clemens eq. 14)**
Mechanical α/(1−α) adjustment on same NAS table — **sign flip band** already in corpus.

**C13. Housing incidence country slice**
Saiz ε × rent burden × FB destination concentration — **renter-incidence screen** separate from government budget and not a final welfare-loss scalar.

### Tier D — 3rd order (dynamic / political)

**D14. Razin-style political equilibrium sketch**
LPR mix shifts education weights over policy regimes — **dynamic weights** on NAS cells, not static ACS.

**D15. Restriction counterfactual cube**
{deportation, reduced inflow, skill-selective} × {CBO macro loss, local shelter savings, admin cost} — **3rd order policy**, not immigrant stock.

**D16. Native spatial equilibrium feedback**
Borjas 40–60% out-migration attenuation on **local** ℓ only; federal stock unchanged — **who bears** shifts.

**D17. Innovation / productivity tail**
Hunt-style long-run GDP channel — **wide positive tail** on country NPV; explicit **[SPECULATION]** unless paper staged.

---

## Recommended stack (pragmatic “country +/-” without lying)

```
Layer 0 — Weights:     ACS/SIPP cells (education × age × state × legal × t)
Layer 1 — Direct:      NAS NPV cells + annual SIPP federal proxy + ITEP floor + per-pupil local
Layer 2 — GE band:     Clemens capital-tax + Card-Peri wage fan (same cells)
Layer 3 — Dynamic:     Hanson time weights + return-migration horizon haircut + CBO surge path
Layer 4 — Episodic:    Receiver cities + admin (restriction only)
Output:                Table of (cell, ℓ, order) → $ ; NO single scalar
```

**Country “likely sign” language (allowed):**
> For a **country-weighted stock** resembling 2023 ACS foreign-born with **current education mix**, **1st-order lifetime NPV** leans **negative** on `<HS`-heavy cells and **positive** on college+ cells; **2nd-order GE** widens positive tail; **3rd-order** local episodic + housing can dominate **city/surge** narratives without flipping **federal annual +** for working-age cells. [FRAMING-SENSITIVE] [INFERENCE]

---

## Disconfirmation (brainstorm kills)

1. If native-born symmetric microsim shows **<2×** federal gap at matched education, composition story weakens for **annual** layer only — lifetime NAS unchanged.
2. If bridge grid shows annual and lifetime **scopes incommensurable** by construction, kill any memo that sums them.
3. If return-migration haircut erases `<HS` lifetime negative for **effective horizon**, stock liability overstated.
4. If local per-pupil × school-age share ≪ federal net at **annual** frequency post unit-fix, local layer secondary for **flow** (lifetime may still differ).

---

## Next actions (execution, not more PDFs)

| Priority | Action | Order | Status |
|----------|--------|-------|--------|
| 1 | `country_fiscal_tensor` DuckDB view | 1st | **done** |
| 2 | Native SIPP donors (`EBORNUS=1`) | 1st | **done** |
| 3 | NAS × ACS weight rollup | 1st | **done** (in tensor) |
| 4 | Clemens overlay + wage fan | 2nd | **done** (partial) |
| 5 | CBO surge object separate from stock | 3rd | **done** |
| 6 | Razin/LPR dynamic weights sketch | 3rd | xlsx parse pending |

---

## Iteration 2 — disconfirmation sweep (2026-06-15)

**Trigger:** “Caucasian all nativity vs low-skill” + matched-education kill test from Section “Disconfirmation”.

### Found (warehouse)

| Population | Fed $/adult/yr | Lifetime NPV/adult (NAS) |
|------------|----------------|--------------------------|
| **nh_white_all** | **~$2,803** | [GAP — needs NAS join on all-nativity weights] |
| nh_white_usborn | ~$2,746 | ~−$41k (donor-matched subset only) |
| **nh_white_fborn** | **~$3,898** | [GAP] |
| mexico_origin | ~$1,519 | ~+$45.6k synthetic age-25 benchmark |
| **fb_lt_hs** | **~$677** | **~−$109k** |
| mx_ca_cluster | ~$1,519 | ~+$43.0k synthetic age-25 benchmark |

**New views:** `v_education_matched_federal`, expanded `v_country_fiscal_compare` (all-white vs fb_lt_hs, etc.).
**New table:** `acs_nh_white_education_by_nativity_2023`.

### Disconfirmation results

| Test | Verdict |
|------|---------|
| **D1** Native symmetric microsim at matched education | **Composition story holds for aggregate** — but **within-cell Mexico ≥ white at HS / some-college**; only college+ (`other`) shows white higher (~1.36×). NH white `<HS` SIPP cell **still broken** (−$7.5k); use FB `<HS` donor ($677) for parity. |
| **D2** Annual ↔ lifetime bridge | **Confirmed scope_mismatch** — all education rows; do not sum. |
| **D3** Return-migration haircut | **Not run** — still open. |
| **D4** Local school layer vs federal annual | **Reopened** — never compare ~$21k/pupil directly with ~$1.5k/adult, but the later ~$771/adult Mexico school row paired a scenario-household numerator with the full microsim denominator. Origin `federal - school` needs same-universe recomputation. |

### Matched-education federal (Mexico vs NH white, `<HS` white cell patched)

| Cell | Mexico / white (adj) | Who pays more |
|------|----------------------|---------------|
| `<HS` | ~0.95× | ~parity |
| HS / GED | **~3.9×** | **Mexico** |
| some college | ~1.29× | Mexico |
| college+ (`other`) | ~0.73× | White |

**Implication:** Aggregate “white pays more” is **almost entirely education mix** (52% college+ vs 14%), not a uniform white tax premium. [INFERENCE] [SOURCE: `v_education_matched_federal`]

### Headline ratios (tensor)

| Comparison | Ratio |
|------------|-------|
| nh_white_all / fb_lt_hs | **~4.1×** federal annual |
| nh_white_all / mexico_origin | **~1.8×** |
| nh_white_fborn / nh_white_usborn | **~1.4×** (FB whites **raise** white average) |

### Still open

- NH white `<HS` US-born SIPP donor repair (tiny slice, ~5% — should not move scalars much).
- `nh_white_all` lifetime NPV row in tensor.
- LPR xlsx structured parse (Razin sketch).
- Return-migration horizon haircut (D3).

---

## Iteration 3 — two-corridor surge (2026-06-15)

**Trigger:** EU vs Caucasian write-up + sweep 12 protocol (`notes/immigration-lifetime-sweep-protocol.md`).

### Perturbation 1 — Denial cascade (if “immigrant” is one group)

1. **Kill the monolith** — EU27 federal proxy (~$4.7k/adult) > NH white US-born (~$2.7k) > Mexico (~$1.5k) > FB `<HS` (~$0.7k). Any single “immigrant fiscal sign” is **corridor-selected**.
2. **Kill “natives pay more”** — matched-education cells show Mexico ≥ white at HS/some-college; aggregate white premium = **degree mix only**.
3. **Kill lifetime without college+ NAS** — warehouse `npv_education_benchmarks` has 2 rows; EU/white lifetime comparisons are **blocked**, not negative.
4. **Kill EU = white culturally** — NH white FB and EU27 overlap but EU excludes UK, includes Eastern Europe; Canadian whites in NH-white-FB bucket sit outside EU27.
5. **Floor:** Even denying all GE, Corridor B (EU/India/Canada) stays federal-positive annual; Corridor A stays `<HS`-negative lifetime on NAS grammar.

### Perturbation 2 — Domain forcing (who owns the EU premium?)

| Domain | Mechanism | EU vs native white |
|--------|-----------|-------------------|
| **Labor selection** | Visa/skill/chicken-chain | Primary — similar degrees, higher wages |
| **Public finance** | Same FICA formula | Cannot explain 1.7× alone |
| **Demography** | Age at arrival, retirement FB | Secondary — UK/EU retirees downward tail |
| **Political economy** | Razin — welfare magnet | Predicts *future* mix shift, not current stock |
| **Spatial** | Destination PUMA (coastal metros) | Co-moves with wages — test via stage2 |

### Perturbation 3 — Constraint inversion

| Inversion | What it surfaces |
|-----------|------------------|
| Compare EU to **NH white FB** not USB | Gap shrinks (~$4.7k vs ~$3.9k) — selection partly “white FB” not “European” |
| Compare EU to **India** not Mexico | Same corridor B grammar (~$6.2k India) |
| Use **lifetime only** | Blocked until NAS college+ staged — do not improvise |
| Use **surge cohort only** | CBO −$897B federal vs stock EU positive annual — **time dimension required** |
| Drop federal, keep local only | EU concentrated in high-rent PUMAs — local renter-incidence risk may offset federal gain [SPECULATION] |

### Candidate ideas (iteration 3)

**E1. Corridor tag on every tensor row** — `corridor_a_low_ed` | `corridor_b_selected` | `native_stock` — prevents debate laundering.

**E2. NAS college+ seed from Ch.8** — `some college / associate` + `other` cells → unlock EU/white/Mexico lifetime ordering.

**E3. EU × PUMA rent join** — federal annual vs Saiz rent burden same cells — test “rich federal, poor local incidence.”

**E4. LPR-by-country weights** — replace static ACS origin weights for EU/Mexico surge counterfactuals.

**E5. Matched-education wage table** — PINCP by education × origin (EU, Mexico, NH white) — separate payroll from transfer noise.

**E6. Return-migration haircut on Corridor A only** — Duleep-Regets shortens `<HS` horizon; Corridor B low attrition.

**E7. `v_corridor_compare` view** — fixed ratios: EU/Mexico, EU/NH-USB, India/Mexico, FB-lt-hs/NH-all.

### Execution (iteration 3)

| Action | Status |
|--------|--------|
| Write-up memo `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` | **done** |
| Tensor: `eu27_origin`, `uk_origin` population groups | **done** |
| INDEX row | **done** |
| NAS college+ benchmark seed | **next** |
| EU × PUMA rent incidence join | **next** |
| Return-migration sensitivity (D3) | open |
| LPR xlsx parse | open |

### Disconfirmation (iteration 3)

| Test | Prediction if thesis wrong |
|------|---------------------------|
| EU federal premium vanishes at matched education + earnings band | Selection story weakens |
| EU destinations have **lower** rent burden than NH white | Spatial story weakens local-incidence offset |
| NAS college+ cells show Mexico > EU lifetime | Composition story inverts — unlikely [INFERENCE] |

---

## Revisions

| Date | Change |
|------|--------|
| 2026-06-15 | Initial brainstorm after distribution findings memo |
| 2026-06-15 | Iteration 2 — disconfirmation sweep (matched education, population tensor) |
| 2026-06-15 | Iteration 3 — two-corridor surge; EU tensor groups; write-up memo |
| 2026-06-16 | Trigger line aligned to the corrected distribution memo: current built NH-white/Mexico federal proxy ratio is ~1.8×, not the older ~2–3× wage-imputation headline. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Aligned headline federal ratios to current `country_fiscal_rollup_2023.csv` values: `nh_white_all/fb_lt_hs` ~4.1x, `nh_white_all/mexico_origin` ~1.8x, and `nh_white_fborn/nh_white_usborn` ~1.4x. See `immigration-conclusion-audit-running-fixes.md`. |
