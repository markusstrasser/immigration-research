# Mexico NPV, population denominator, and full ledger — synthesis (2026-06-15)

**Trigger:** Post-sweeps 23–32 session + full-ledger critique (local, justice, legal costs not in NAS headline).

**Frame:** [FRAMING-SENSITIVE]

**Warehouse:** `immigration_fiscal_union.duckdb`, `immigration_context.duckdb`

**Mining:** `.mining/immigration-lifetime-cluster-q-stock-flow.json`, `.mining/immigration-lifetime-cluster-r-full-ledger.json`

**Generators:** `immigration-lifetime-fiscal-generators.md` §Q, §R

---

## I. Conclusions (executive)

### 1. There is no defensible scalar

Honest fiscal object is a **vector across ledger layers ℓ**:

`lifetime_npv | school_burden | state_local | admin_enforcement | justice_courts | episodic_local`

**Kill:** Any single "Mexico net +" or "Mexico net −" without ℓ tags is layer laundering.

### 2. NAS +$45,631/adult is a synthetic age-25 benchmark, not stock NPV

| What +$46k is | What it is NOT |
|---------------|----------------|
| NAS Table 8-13 **individual age-at-arrival-25** education-mix benchmark | Actual remaining-lifetime NPV of current Mexico-born stock |
| Federal + some state/local inside NAS cell | School burden for current HH kids (−$771/yr) |
| Public goods **excluded** | Descendants / US-born kids path |
| 2012$, 3%, 75yr | CBP/ICE/detention (~$2.1k/yr if ÷ stock) |
| Composition-weighted **mean** | EOIR / immigration courts |
| Applied to ACS current 25–64 education weights | Net after all local costs; NYC/Chicago shelter (surge episodic) |

NAS Table 8-13 is explicitly a comparison of an immigrant **entering at age 25** with a native-born person followed from age 25. The warehouse applies those age-25 education cells to the current Mexico-born 25–64 stock because public data lack a full age-at-arrival × education × origin NPV table. That makes `+$45,631/adult` a **synthetic composition benchmark**, not a measured lifetime NPV for existing residents. [SOURCE: NAS 2017 Table 8-13 text via local PDF; `country_fiscal_tensor` notes] [INFERENCE]

**Honest short-horizon (built):** federal − school = **+$748/adult/yr** [SOURCE: `v_three_layer_annual`]

**Illustrative lifetime stack [INFERENCE]:**

| Step | $/adult |
|------|---------|
| NAS age-25 education-mix benchmark | +$45,631 |
| − school annuitized ($771/yr) | −$18,000 |
| − CBO state/local surge annuitized ($657/yr) | −$15,300 |
| − enforcement if fully loaded ($2,100/yr) | −$49,000 |
| **Band** | **−$37k to +$28k** |

Enforcement allocation is **[FRAMING-SENSITIVE]** — fixed vs marginal split not resolved.

### 3. Multiply-out (synthetic NAS age-25 benchmark only)

| Bucket | N | Share | NAS/cell | Bucket $ |
|--------|---|-------|----------|----------|
| `<HS` | 3.96M | 46.6% | −$109k | −$431.5B |
| HS | 2.43M | 28.6% | +$49k | +$119.1B |
| some college | 1.24M | 14.6% | +$205k | +$253.7B |
| BA+ | 0.87M | 10.2% | +$514k | +$446.4B |
| **Total** | **8.50M** | | | **+$387.7B** |

**10.2% BA+** — mean is pulled by thin top tail; median person likely `<HS` or HS.

**Do not read `+$387.7B` as an actual stock asset.** It is `current education mix × NAS age-25 cells`. The denominator is a current 25–64 stock: only **17.4%** of Mexico-origin adults in the microsim are age 25–34, while **53.2%** are age 45–64. The table does not model their remaining working years, prior U.S. taxes/transfers, arrival age, return migration, or legal-status path. [SOURCE: `acs_origin_household_federal_microsim_2023` age bands; NAS 2017 Table 8-13] [INFERENCE]

### 4. Denominator discipline

- **8.5M** = Mexico **birthplace**, foreign-born, 25–64, ACS self-report [SOURCE: microsim]
- **≠** 4.3M Mexico-**unauthorized** (Pew 2023)
- **≠** 437k `origin_national` (recent `<HS` only — wrong denominator)

### 5. Biden “10M+ illegals”

- **~10.8M encounters** (events) + **~2M gotaways** ≠ net residents
- **Net stock Δ:** Pew **+3.5M** (2021→23); CIS **+5.6M** (2021→25)
- **Mexico unauthorized flat ~4.3M**; surge was non-Mexico

### 6. Build priorities (from generators)

1. `v_full_fiscal_stack` view + overlap matrix (G-LIF-R05)
2. Legal-status split within `mexico_origin` (G-LIF-Q03)
3. EOIR → origin rollup (G-LIF-R04)
4. CBP/ICE marginal allocation rule (G-LIF-R03)
5. Never subtract `local_flow` $20,907/pupil from per-adult NPV (G-LIF-R02)

---

## II. Generators

### Cluster Q — stock vs flow

| ID | One-line |
|----|----------|
| G-LIF-Q01 | Encounter ≠ stock — IDENT unique subjects before per-capita |
| G-LIF-Q02 | Gotaway trap — never sum gotaways + encounters + Pew stock |
| G-LIF-Q03 | Birthplace ≠ legal status |
| G-LIF-Q04 | Education-mix mean ≠ median — ship bucket table |
| G-LIF-Q05 | Pew 14M vs CIS 15.8M band on unauthorized-layer only |

### Cluster R — full ledger stack

| ID | One-line |
|----|----------|
| G-LIF-R01 | NAS scope lock — list in/excluded ℓ before net claim |
| G-LIF-R02 | School double-count guard vs descendants |
| G-LIF-R03 | CBP/ICE allocation rule (fixed vs marginal) |
| G-LIF-R04 | EOIR justice/court layer by nationality |
| G-LIF-R05 | Publish stacked vector only — `v_full_fiscal_stack` |

Full prompts: `immigration-lifetime-fiscal-generators.md` §Q, §R.

---

## III. Warehouse layers (`mexico_origin`)

| fiscal_layer | $/adult | Netted into lifetime_npv? |
|--------------|---------|---------------------------|
| `lifetime_npv` | +$45,631 synthetic age-25 benchmark | — |
| `federal_annual` | +$1,519/yr | partial overlap |
| `school_burden_per_adult` | $771/yr | **NO** |
| `net_crude_federal_minus_school` | +$748/yr | **NO** |
| `local_flow` | $20,907/pupil | **NO** (unit mismatch) |

Missing from warehouse rollup: EOIR $/case, ICE bed-days allocated, shelter episodic per Mexico adult.

---

## IV. Disconfirmation

| Hypothesis | Result |
|------------|--------|
| +$46k = immigrant pays for themselves all-in | **Unsupported / not a valid export** — school, admin, courts, shelter not netted |
| Subtract `local_flow` from NPV | **Falsified** — per_pupil ≠ per_adult burden |
| 10M+ net new unauthorized since Biden | **Falsified** — stock +3.5M to +5.6M |
| Mexico drove surge | **Falsified** — Mexico unauthorized flat |
| NAS `<HS` cell applies to the whole Mexico-origin stock | **Falsified** by education mix — but actual current-stock NPV remains unmeasured |
| +$387.7B is the actual lifetime NPV of the current Mexico-born stock | **Falsified** — it is current ACS education weights × NAS age-25 cells |

---

## V. Open gaps

1. Build `v_full_fiscal_stack` + overlap matrix (R-005).
2. Legal-status imputation for Mexico microsim cells.
3. EOIR nationality → `mexico_origin` court cost proxy.
4. ICE marginal $/bed-day × detention probability by status path.
5. EU27/NH-white lifetime rollup (education mix).
6. Surge cohort vs Mexico stock NAS cell separation.
7. Age-at-arrival/current-age NPV mapping for Mexico stock; current warehouse lacks it.

---

## Revisions

| Date | Change |
|------|--------|
| 2026-06-15 | Initial: multiply-out, denominator, Biden stock vs flow (cluster Q) |
| 2026-06-15 | Full-ledger critique: NAS ≠ net; cluster R generators; stacked bounds −$37k to +$28k |
| 2026-06-16 | Corrected lifetime label: `+$45,631/adult` and `+$387.7B` are synthetic NAS age-25 education-mix benchmarks, not actual current-stock lifetime NPV |
| 2026-06-16 | Reframed `+$46k = pays for themselves all-in` from falsified to unsupported/not a valid export: omitted ledgers block the inference, but the full all-in sign remains unmeasured. See `immigration-conclusion-audit-running-fixes.md`. |
