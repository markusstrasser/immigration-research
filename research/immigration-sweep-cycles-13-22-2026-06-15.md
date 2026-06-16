# Sweep cycles 13–22 — school burden divergence/synthesis (2026-06-15)

**Protocol:** `notes/immigration-lifetime-sweep-protocol.md`, cookbook diverge→converge loop
**Trigger:** User — build school burden (per_pupil × kids/adult), then **10** analyze/write cycles
**Artifact:** `v_three_layer_annual`; memos `immigration-school-burden-per-adult-2026-06-15.md`
**Status:** Superseded. The first-pass `~−$13.5k/adult` Mexico result used the scenario-subset denominator. The later `$771` / `+$748` correction also proved invalid because it paired a scenario-household numerator with the full microsim denominator. Origin school/net rows are not live until same-universe rebuilt.

---

## Cycle 13 — Build three-layer annual

**Diverge:** What if headlines included `per_pupil × kids_per_adult`?

**Data:** Tensor layers `school_burden_per_adult`, `net_crude_federal_minus_school` added.

| Group | Fed | School | Crude net |
|-------|-----|--------|-----------|
| Mexico | $1,519 | withheld | withheld |
| NH white USB | $2,746 | $6,024 | −$3,277 |
| EU27 | $4,695 | withheld | withheld |

**Synthesis:** Federal-only headlines can understate local school drag, but origin `federal - school` signs are not live in this build. Layer must be labeled **crude static**, not lifetime, and origin rows need same-universe school numerators.

---

## Cycle 14 — NH white symmetric

**Diverge:** Does school burden flip “natives vs immigrants”?

**Data:** NH white school/adult ~$6k (ACS HH linkage + county median pupil); Mexico origin row withheld after the scenario-household/full-microsim universe mismatch was confirmed.

**Synthesis:** On crude net, NH white US-born is negative under the current average-cost school layer, but Mexico-origin crude net is unresolved. This is a denominator-sensitive static layer, not a welfare verdict.

---

## Cycle 15 — Crude ranking

**Diverge:** Rank populations by `federal − school`.

**Order (lowest crude net first):** not live for origin rows; NH white rows remain built, while MX-CA/Mexico/EU27 require same-universe school recomputation.

**Synthesis:** Corridor A crude annual ranking is reopened. EU27 federal annual remains high, but EU27 school/net rows are withheld for the same-universe guard.

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
| MX-CA | withheld |
| Mexico | withheld |
| NH white | 2.2× |
| EU27 | withheld |

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
| Mexico | withheld | withheld |
| NH white | −$3,277 | −$265 |
| EU27 | withheld | withheld |

**Synthesis:** Mexico-origin sign is unresolved. NH white remains near the sign boundary under this crude average-cost layer.

---

## Cycle 21 — Scope kill (crude vs lifetime)

**Diverge:** Does crude annual net predict NAS lifetime sign?

Mexico: crude annual `federal - school` **withheld** vs synthetic age-25 NAS benchmark **+$45.6k** (education-mix weighted, not current-stock remaining-lifetime NPV).

**Synthesis:** **Do not sum or rank across layers.** Bridge grid `scope_mismatch` confirmed again.

---

## Cycle 22 — Converge (thesis burst)

**Prior thesis (sweep 12):** Two corridors — selected high-ed federal+ vs low-ed Corridor A.

**Revised thesis (3 sentences):**

1. **Three coexisting ledgers:** federal cash-flow proxy (often **+** for working-age), school burden per adult (separate annual local layer), and lifetime NAS education cells (`<HS` negative, college+ positive). They are **compatible**, not contradictory.

2. **Crude `federal − school` is unresolved for Mexico-origin rows** because the school numerator and adult denominator did not share a population universe. NH white US-born remains about `−$3,277/adult/yr` on this static average-cost school layer. The result omits descendant taxes, Medicaid, marginal pupil economics, and legal-status/cohort splits; it is a **political visibility** layer, not a welfare verdict.

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
| 2026-06-16 | Reopened origin school layer: the $771/adult and +$748/adult Mexico correction paired a scenario-household numerator with the full microsim denominator; old ~−$13.5k and +$748 signs are both not live. |
