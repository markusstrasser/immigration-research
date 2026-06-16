# School burden per adult — built layer (2026-06-15)

**Date:** 2026-06-15
**Status:** Working — new tensor layers `school_burden_per_adult`, `net_crude_federal_minus_school`
**Frame:** [FRAMING-SENSITIVE] — crude static local burden; **not** NAS lifetime; **not** marginal pupil cost.
**Related:** `immigration-federal-distribution-findings-2026-06-15.md`, `immigration-europe-caucasian-fiscal-findings-2026-06-15.md`
**View:** `v_three_layer_annual` in `warehouse/immigration_fiscal_union.duckdb`

---

## I. Formula

\[
\text{school\_burden\_per\_adult} = \text{per\_pupil} \times \frac{\text{school\_age\_children\_per\_HH}}{\text{adults\_per\_HH}}
\]

| Input | Source |
|-------|--------|
| `per_pupil` | Area-weighted F-33 `current_spend_per_pupil` by origin PUMA [SOURCE: `origin_fiscal_scenario_2023`] |
| `school_age_children_per_HH` | ACS 2023 HH linkage ages 5–17 [SOURCE: `acs_origin_household_national_2023`] |
| `adults_per_HH` | `weighted_adults / linked_household_wgt` from scenario ledger |

**NH white (symmetric):** county **median** per-pupil × kids/adult from ACS `SERIALNO` HH linkage (ages 5–17 vs NH adults 25–64). [SOURCE: tensor build, ACS person CSV]

**Crude net:**

\[
\text{net\_crude} = \text{federal\_proxy\_per\_adult} - \text{school\_burden\_per\_adult}
\]

Tagged **`derived_crude`** — excludes descendant future taxes, Medicaid, state/local non-school, income tax.

---

## II. Headline table (three-layer annual)

| Population | Federal $/adult | School $/adult | Crude net $/adult | School/Fed |
|------------|-----------------|----------------|-------------------|------------|
| **Mexico-origin** | **$1,519** | **$771** | **+$748** | **0.5×** |
| MX + N. Triangle | $1,519 | $1,091 | +$428 | 0.7× |
| **NH white US-born** | **$2,746** | **$6,024** | **−$3,277** | 2.2× |
| NH white all | $2,803 | $6,055 | −$3,293 | 2.2× |
| NH white FB | $3,898 | $6,537 | −$3,534 | 1.7× |
| **EU27-origin** | **$4,695** | **$64** | **+$4,658** | <0.1× ⚠️ thin school-age row |
| UK-origin | $5,486 | $92 | +$5,372 | <0.1× ⚠️ thin school-age row |

[SOURCE: `warehouse/immigration_fiscal_union.duckdb` view `v_three_layer_annual`, effect_order=1, queried 2026-06-15 with DuckDB CLI]

**Table-scope warning:** The negative NH-white crude rows are not evidence that native whites are fiscally negative. This view assigns current average K–12 costs to current adults without descendant future taxes or a lifetime accounting frame, just as it does for immigrant-origin households. Use it as a static visibility layer only. [INFERENCE]

---

## III. What changes vs prior memos

| Prior headline | Still valid? |
|----------------|--------------|
| Federal: white ~1.8× Mexico | **Yes** — school layer **not** in federal proxy |
| Per-pupil ~$20k both groups | **Yes** — that's **per enrolled pupil**, not per adult |
| “Whites pay more taxes” | **Partial** — on **federal annual only**; current crude federal-minus-school has Mexico still positive because the earlier school denominator was wrong |

**Correction:** the first pass divided Mexico household school burden by the `origin_fiscal_scenario_2023` PUMA-linked recent-low-skill denominator (~437k adults). The current tensor divides by the full Mexico microsim adult denominator (~8.50M adults), revising Mexico from ~−$13.5k/adult to **+$748/adult** on the crude annual federal-minus-school layer. [SOURCE: `v_three_layer_annual`; `origin_fiscal_scenario_2023`; `acs_origin_household_federal_microsim_2023`] [INFERENCE: denominator bug]

This does **not** make the all-government fiscal question positive. It only invalidates the stale narrow export that the built annual school layer alone overwhelms Mexico's federal proxy under the corrected adult denominator. The lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers remain separate ledger objects. [SOURCE: `immigration-mexico-npv-population-synthesis-2026-06-15.md`]

---

## IV. Decomposition — why Mexico changed

| Factor | Mexico |
|--------|-------:|
| Scenario adult subset | 436,819 |
| Full microsim adult denominator | 8,496,334 |
| Household weight | 322,540 |
| School-age children / household | 0.9718 |
| Per-pupil (area-wtd) | ~$20,907 |
| **School/adult with full denominator** | **~$771** |

**Driver:** the per-pupil cost is high, but the denominator is the full Mexico adult microsim stock, not the recent-low-skill scenario subset. Household structure still matters, but it no longer creates a built $15k/adult Mexico school burden after the denominator correction. [SOURCE: `immigration-sweep-cycles-23-32-2026-06-15.md`]

---

## V. Child-attribution caveat [FRAMING-SENSITIVE]

School-age children in immigrant-headed HHs are often **US-born citizens**. This layer assigns full average K–12 cost to the **household origin stock** without crediting those children's future payroll. NAS descendant column is the correct place for intergenerational offset — not this crude net. [SOURCE: `immigration-fiscal-camarota-cis-testimony-audit.md`, Orrenius/Urban Institute framing in corpus]

The same accounting caveat applies symmetrically to native rows: assigning native children's current K–12 costs to current native adults without descendant future taxes is not a welfare or lifetime fiscal sign. [INFERENCE]

---

## VI. Known limitations

| Issue | Impact |
|-------|--------|
| **Average vs marginal** pupil cost | Overstates burden if immigrants enroll in already-funded seats |
| **Scenario `weighted_adults`** | PUMA-linked recent-low-skill subset for origins — do **not** use it as the full adult denominator |
| **UK / EU school rows** | Very low school-age children after microsim-denominator correction; cite only as a sensitivity screen, not a stable conclusion |
| **NH white per-pupil** | County median, not PUMA area-weighted — ~$19,385 vs origin ~$21k |
| **No Medicaid / state / shelter** | Crude net is **not** full local ledger |
| **Lifetime NAS** | Separate layer; college+ cells are staged, but not netted into this crude annual view |

---

## VII. Reproduce

```bash
cd infra/immigration-fiscal
uv run --with duckdb,pandas python build/build_country_fiscal_tensor.py
```

```sql
SELECT * FROM v_three_layer_annual ORDER BY net_crude_per_adult;
```

---

## Revisions

| Date | Change |
|------|--------|
| 2026-06-15 | Initial build — school_burden_per_adult + net_crude layers in tensor |
| 2026-06-15 | Corrected denominator: Mexico school/adult now $771 and crude net +$748 in live `v_three_layer_annual`; prior −$13.5k used the scenario subset denominator |
| 2026-06-16 | Added symmetric table-scope warning: negative NH-white crude rows are static school-cost assignment, not evidence that native whites are fiscally negative. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced "kills the stale claim" with invalidates-the-narrow-export wording; the corrected denominator only blocks the built annual school-layer export, not the all-government fiscal question. See `immigration-conclusion-audit-running-fixes.md`. |
