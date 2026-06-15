# Sweep cycles 13–22 — school burden divergence/synthesis (2026-06-15)

**Protocol:** `notes/immigration-lifetime-sweep-protocol.md`, cookbook diverge→converge loop
**Trigger:** User — build school burden (per_pupil × kids/adult), then **10** analyze/write cycles
**Artifact:** `v_three_layer_annual`; memos `immigration-school-burden-per-adult-2026-06-15.md`
**Status:** Superseded/corrected on 2026-06-16 after the scenario-subset denominator bug was found. This file now records the corrected rows; the first-pass `~−$13.5k/adult` Mexico result is not a live conclusion.

---

## Cycle 13 — Build three-layer annual

**Diverge:** What if headlines included `per_pupil × kids_per_adult`?

**Data:** Tensor layers `school_burden_per_adult`, `net_crude_federal_minus_school` added.

| Group | Fed | School | Crude net |
|-------|-----|--------|-----------|
| Mexico | $1,519 | $771 | +$748 |
| NH white USB | $2,746 | $6,024 | −$3,277 |
| EU27 | $4,695 | $64 | +$4,658 |

**Synthesis:** Federal-only headlines can understate local school drag, but the corrected full-stock denominator no longer makes Mexico crude-negative on this built layer. Layer must be labeled **crude static**, not lifetime.

---

## Cycle 14 — NH white symmetric

**Diverge:** Does school burden flip “natives vs immigrants”?

**Data:** NH white school/adult ~$6k (ACS HH linkage + county median pupil); Mexico ~$771 after the full-stock denominator correction.

**Synthesis:** On crude net, Mexico is positive while NH white US-born is negative under the current average-cost school layer. This is a denominator-sensitive static layer, not a welfare verdict.

---

## Cycle 15 — Crude ranking

**Diverge:** Rank populations by `federal − school`.

**Order (lowest crude net first):** NH white ≈ NH white US-born < MX-CA cluster < Mexico < EU27.

**Synthesis:** Corridor A no longer dominates crude annual losses after denominator correction. EU27 remains strongly positive on this narrow annual layer.

**Kill:** UK at bottom — **reject** (scenario N≈1k adults); flag for rebuild.

---

## Cycle 16 — Fertility vs price

**Diverge:** Kids/adult vs per-pupil — which drives school/adult?

**Data:** El Salvador/Guatemala/Mexico top kids/adult; Poland/Germany bottom. Per-pupil ~$20k across.

**Synthesis:** **Composition of children**, not $/pupil ethnicity tariff, drives cross-origin school/adult spread.

---

## Cycle 17 — One-layer politics

**Diverge:** School/federal ratio only — who looks costliest?

| Group | School/Fed |
|-------|------------|
| MX-CA | 0.72× |
| Mexico | 0.51× |
| NH white | 2.2× |
| EU27 | 0.01× |

**Synthesis:** Restrictionists citing school **without** federal layer mirror expansionists citing federal **without** school. Both are layer laundering.

---

## Cycle 18 — Intensive margin (HH with kids)

**Diverge:** Share of HH with school-age children.

Mexico **52%** vs Poland **6%**; kids/HH Mexico **0.97** vs Poland **0.13**.

**Synthesis:** Burden is **both** extensive (% HH with kids) and intensive (kids/HH). Averages hide bimodal HH structure.

---

## Cycle 19 — Per-pupil dispersion

**Diverge:** County F-33 pupil min/median/max.

**$6,338 – $19,385 – $113,176** [SOURCE: `school_finance_county_2023`]

**Synthesis:** School/adult sensitive to location weights; origin PUMA area-weights ≠ NH median shortcut (~2–5% swing [INFERENCE]).

---

## Cycle 20 — Marginal sensitivity

**Diverge:** What if school cost were **50% marginal**?

| Group | Base crude | Half-marginal crude |
|-------|------------|---------------------|
| Mexico | +$748 | +$1,134 |
| NH white | −$3,277 | −$265 |
| EU27 | +$4,658 | +$4,663 |

**Synthesis:** Mexico stays positive under both average and half-marginal school assignment. NH white remains near the sign boundary under this crude average-cost layer.

---

## Cycle 21 — Scope kill (crude vs lifetime)

**Diverge:** Does crude annual net predict NAS lifetime sign?

Mexico: crude **+$748/yr** vs synthetic age-25 NAS benchmark **+$45.6k** (education-mix weighted, not current-stock remaining-lifetime NPV).

**Synthesis:** **Do not sum or rank across layers.** Bridge grid `scope_mismatch` confirmed again.

---

## Cycle 22 — Converge (thesis burst)

**Prior thesis (sweep 12):** Two corridors — selected high-ed federal+ vs low-ed Corridor A.

**Revised thesis (3 sentences):**

1. **Three coexisting ledgers:** federal cash-flow proxy (often **+** for working-age), school burden per adult (separate annual local layer), and lifetime NAS education cells (`<HS` negative, college+ positive). They are **compatible**, not contradictory.

2. **Crude `federal − school` no longer makes Mexico negative** under the full-stock denominator: Mexico is about `+$748/adult/yr`, while NH white US-born is about `−$3,277/adult/yr` on this static average-cost school layer. The result omits descendant taxes, Medicaid, marginal pupil economics, and legal-status/cohort splits; it is a **political visibility** layer, not a welfare verdict.

3. **Scalar collapse error now has three faces:** (a) federal-only “immigrants pay in,” (b) school-only “immigrants bankrupt schools,” (c) lifetime-only “−$109k `<HS`.” The tensor object is **`v_three_layer_annual`**, not any single column.

### Disconfirmation hunts (cycle 22)

| # | Hunt | Flips thesis if… |
|---|------|------------------|
| 1 | Marginal pupil cost << average for immigrant enrollment | Mexico crude net approaches zero |
| 2 | Descendant NAS college+ cells + attribution rules | NH white crude net turns positive with symmetric rules |
| 3 | UK/EU scenario adult weights fixed to microsim N | EU school/adult drops; ranking reshuffles |

### Next execution

1. NAS college+ benchmark seed (Ch.8)
2. Align scenario `weighted_adults` to national microsim for school ratios
3. `fb_lt_hs` school burden row (currently NULL)
4. Export `v_three_layer_annual` → CSV in `stage3_proto/`

---

## Revisions

| Date | Change |
|------|--------|
| 2026-06-15 | Cycles 13–22 after school burden tensor build |
| 2026-06-16 | Corrected scenario-denominator carryover: Mexico school burden now $771/adult and crude net +$748/adult/yr; old ~−$13.5k result superseded |
