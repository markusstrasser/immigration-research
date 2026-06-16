# Immigration conclusion audit — running fixes

**Purpose:** running ledger of statistical, mathematical, logical, and data-science issues fixed while auditing immigration conclusions.

**Rule:** each entry names the broken conclusion, the evidence that changed it, what was edited, and what remains unresolved. This is not a final immigration position memo.

---

## 2026-06-15 — School-burden denominator correction

**Status update (2026-06-16): superseded again.** The 2026-06-15 correction fixed one denominator misuse but introduced the mirror-image problem: the school numerator still came from the `origin_fiscal_scenario_2023` household universe (~436,819 Mexico scenario adults / 322,540 linked household weight), while the denominator was changed to the full microsim adult stock (~8,496,334). The live builder now withholds origin school and `federal - school` rows until numerator and denominator universes match.

### Issue

The school-burden memo and a stale exported CSV still supported the conclusion that Mexico-origin adults had a crude annual federal-minus-school balance of about **-$13.5k/adult**. That result used the `origin_fiscal_scenario_2023` scenario subset denominator (~436,819 adults) after multiplying area-weighted per-pupil school spend by household school-age children. [DATA]

That denominator was wrong for a full Mexico-origin adult-stock conclusion. The live tensor now uses the full Mexico microsim adult denominator (~8,496,334 adults). [DATA]

### Evidence Checked

```sql
SELECT *
FROM v_three_layer_annual
WHERE population_group = 'mexico_origin';
```

Then-current DuckDB result from `warehouse/immigration_fiscal_union.duckdb`, now superseded by the 2026-06-16 same-universe guard:

| federal_per_adult | school_per_adult | net_crude_per_adult | weight_adults |
|------------------:|-----------------:|--------------------:|--------------:|
| 1519.278 | 771.285 | 747.993 | 8496334 |

Scenario source check from `warehouse/immigration_lifetime_evidence.duckdb`:

| origin | scenario adults | avg federal net | area-wtd per pupil | school-age kids/HH | HH weight |
|--------|----------------:|----------------:|-------------------:|-------------------:|----------:|
| Mexico | 436819 | 1519.278 | 20907.09 | 0.9718 | 322540 |

The old ~-$13.5k conclusion came from dividing the household school burden by the scenario subset. The intermediate correction computed school burden as:

`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult` [INFERENCE]

### Fixes Made

1. Updated `research/immigration-school-burden-per-adult-2026-06-15.md`:
   - Briefly changed the Mexico-origin row to `$1,519` federal, `$771` school, `+$748` crude annual.
   - This row is now superseded by the 2026-06-16 universe-mismatch fix below.
   - Removed the stale verdict that Mexico looks far worse than natives on crude static federal-minus-school math, but the replacement positive net is also not live.

2. Updated `research/immigration-scenario-composition-2026-06-15.md`:
   - Replaced obsolete `~$21/pupil` text with post-F-33 `~$20,907/pupil`.
   - Added a warning not to use `436,819` scenario adults as the full Mexico-origin stock denominator.

3. Updated `research/immigration-lifetime-fiscal-generators.md`:
   - Rewrote G-LIF-K01 so future audits check both F-33 units and per-adult denominator discipline.

4. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
   - The tensor builder now exports `three_layer_annual_2023.csv` from the live `v_three_layer_annual` view.

5. Regenerated canonical staged CSVs under `infra/immigration-fiscal/build/stage3_proto/`, including `three_layer_annual_2023.csv`, from the live DuckDB view.

### Current Conclusion

This intermediate finding is now superseded: the built annual **federal-minus-school** layer should not be reported for Mexico-origin adults until its school numerator and adult denominator use the same universe. [DATA]

The lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers remain separate and cannot be collapsed into the narrow federal annual row. [INFERENCE]

### Remaining Risk

The corrected current conclusion is now narrower: the Mexico-origin **federal annual** row remains about `$1,519/adult/yr`, but the origin-specific `school_burden_per_adult` and `net_crude_federal_minus_school` rows are unresolved until the school numerator is rebuilt on the same population universe as the adult denominator. The old `+$748/adult/yr` net should not be cited as a live finding. [DATA]

---

## 2026-06-16 — Origin school layer withheld after universe mismatch

### Issue

The 2026-06-15 school correction divided a school-cost numerator from the origin scenario household universe by the full Mexico microsim adult denominator:

`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult`

That arithmetic was reproducible, but the numerator and denominator did not describe the same population. `322,540 * 0.9718` is about `313k` linked school-age children in the scenario household universe; spreading that numerator over `8.5M` full-stock adults implies only about `0.037` school-age children per adult for Mexico-origin households, which is not a defensible full-stock school-incidence estimate. [DATA] [INFERENCE]

### Evidence Checked

Current DB probes:

```text
ctx.acs_origin_household_national_2023 Mexico:
linked_household_wgt=322,539.5
linked_mean_hh_school_age_children=0.971785

ctx.acs_origin_national_2023 Mexico:
weighted_adults=436,819

ctx.acs_origin_household_federal_microsim_2023 Mexico:
weighted_adults=8,496,334
```

After adding the builder guard and rebuilding:

```text
v_three_layer_annual Mexico:
federal_per_adult=1519.278396
school_per_adult=NULL
net_crude_per_adult=NULL
weight_adults=8496334
```

### Fixes Made

1. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
   - Origin school burden is now emitted only when the school numerator adult universe and microsim denominator are within 5%.
   - Aggregate school rows stay `NULL` if any component origin lacks a same-universe school value.

2. Regenerated tracked staged exports:
   - `infra/immigration-fiscal/build/stage3_proto/country_fiscal_rollup_2023.csv`
   - `infra/immigration-fiscal/build/stage3_proto/three_layer_annual_2023.csv`

3. Updated school and lifetime memos so the `+$748/adult/yr` Mexico net is marked superseded/unresolved rather than corrected.

### Current Conclusion

The school layer is still a necessary ledger object, but the origin rows need a same-universe rebuild. Until then, the only live Mexico-origin annual scalar in this tensor is the narrow federal proxy (`~$1,519/adult/yr`). The sign of `federal - school` for the full Mexico-origin stock is unresolved in this build. [DATA]

---

## 2026-06-16 — NAS age-25 benchmark relabeled; current-stock NPV claim killed

### Issue

Several memos described the warehouse `lifetime_npv` rollup as "Mexico lifetime NPV" or treated the `+$387.7B` multiply-out as if it were the lifetime value of the current Mexico-born adult stock. The live tensor actually multiplies current ACS education weights by NAS Table 8-13 cells for an immigrant entering at **age 25**. [DATA]

That is a useful composition benchmark, but it is not an actual remaining-lifetime NPV for current residents. Current Mexico-origin adults in the microsim are not a cohort of new age-25 entrants: only `17.4%` are age `25-34`, while `53.2%` are age `45-64`. [DATA]

### Evidence Checked

NAS source text around Table 8-13 states that the table compares an immigrant entering at age 25 with a native-born person followed from age 25. [SOURCE: local NAS 2017 PDF via `pdftotext`; `external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf`]

Live DuckDB result:

```sql
SELECT population_group, fiscal_layer, effect_order,
       ROUND(weight_adults,0) AS w,
       ROUND(value_per_adult_weighted,2) AS per_adult,
       ROUND(value_total_usd/1e9,3) AS total_b
FROM v_country_fiscal_rollup
WHERE population_group='mexico_origin'
  AND fiscal_layer IN ('federal_annual','lifetime_npv');
```

| layer | adults | per adult | total |
|-------|-------:|----------:|------:|
| federal_annual | 8,496,334 | $1,519.28/yr | $12.908B/yr |
| lifetime_npv | 8,496,334 | $45,631.19 | $387.698B |

Current Mexico-origin age mix:

| age band | adults | share |
|----------|-------:|------:|
| 25-34 | 1,482,136 | 17.4% |
| 35-44 | 2,493,309 | 29.3% |
| 45-54 | 2,656,957 | 31.3% |
| 55-64 | 1,863,932 | 21.9% |

### Fixes Made

1. Updated `research/immigration-mexico-npv-population-synthesis-2026-06-15.md`:
   - Reframed `+$45,631/adult` and `+$387.7B` as **synthetic NAS age-25 education-mix benchmarks**.
   - Added the current-age distribution warning.
   - Replaced "NAS mix negative for Mexico falsified" with the narrower claim that `<HS`-only application is falsified by education mix, while actual current-stock NPV remains unmeasured.

2. Updated `research/immigration-lifetime-unified-theory-2026-06-15.md`:
   - Relabeled the verifiable anchor as a synthetic age-25 benchmark.
   - Corrected the Mexico federal annual total: full microsim stock is about `$12.9B/yr`; `$664M/yr` is the scenario subset only.
   - Corrected receiver-vs-federal dominance language to match denominators.

3. Updated `research/immigration-country-fiscal-tensor-2026-06-15.md`:
   - Replaced stale pre-college-cell negative NAS rows with current positive synthetic benchmark rows.
   - Added a limitation that age-25 NPV benchmarks are not current-stock remaining-lifetime estimates.

4. Updated `research/immigration-lifetime-fiscal-generators.md`:
   - Added G-LIF-Q06: age-25 NPV benchmark is not current-stock NPV.
   - Corrected the remittance comparison to distinguish scenario-subset federal net from full-stock federal net.

5. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
   - Tensor row notes now label `lifetime_npv` as a synthetic age-at-arrival-25 benchmark applied to current ACS education weights.

### Current Conclusion

The `+$45,631/adult` and `+$387.7B` numbers should be read only as **current education mix × NAS age-25 cells**. They kill a crude claim that Mexico-origin adults should all be mapped to the `<HS` NAS cell, but they do **not** establish the actual lifetime NPV of the current Mexico-born stock. [INFERENCE]

The corrected full-stock annual federal proxy is about `$12.9B/yr`; `$664M/yr` is a scenario-subset calculation and should not be used against whole-stock or city-episodic totals without denominator matching. [DATA]

---

## 2026-06-16 — Local school-flow unit comparison corrected

### Issue

`research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still contained an iteration-table verdict saying **"Local per-pupil ≪ federal annual"** and calling it confirmed by `~$21k/pupil vs ~$1.5k federal/adult`. That comparison mixed units and was numerically backwards: `$21k/pupil` is not less than `$1.5k/adult`, and neither number is comparable until the school value is bridged to an adult denominator. [DATA]

The same table still carried superseded Mexico and MX+Central America lifetime rows around `−$79k`/`−$80k`, which came from the older `<HS`-heavy-only approximation rather than the current ACS education-mix benchmark. [DATA]

### Evidence Checked

Live DuckDB rollup:

```sql
SELECT population_group, fiscal_layer, effect_order,
       ROUND(value_per_adult_weighted,2) AS per_adult,
       ROUND(value_total_usd/1e9,3) AS total_b,
       ROUND(weight_adults,0) AS adults
FROM v_country_fiscal_rollup
WHERE fiscal_layer IN ('federal_annual','lifetime_npv')
  AND population_group IN ('mexico_origin','fb_lt_hs','mx_ca_cluster');
```

| population | layer | per adult | total |
|------------|-------|----------:|------:|
| Mexico-origin | federal annual | $1,519.28/yr | $12.908B/yr |
| Mexico-origin | synthetic age-25 NPV benchmark | $45,631.19 | $387.698B |
| FB `<HS` | synthetic age-25 NPV benchmark | −$109,000 | −$837.868B |
| MX + N. Triangle | synthetic age-25 NPV benchmark | $42,971.52 | $476.122B |

The previous comparable school-layer row from `v_three_layer_annual` (`~$771/adult/yr`, crude `+$748/adult/yr`) is now marked invalid for Mexico-origin adults because its numerator and denominator used different population universes. [DATA]

### Fixes Made

1. Updated `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md`:
   - Replaced the stale Mexico and MX+Central America `~−$80k` lifetime rows with current synthetic age-25 benchmarks.
   - Replaced the invalid `per-pupil ≪ federal annual` verdict; the later `$771/adult` school comparison is now also superseded by the universe-mismatch guard.

### Current Conclusion

The useful conclusion is not that local per-pupil costs are small. The live conclusion is narrower: per-pupil school costs must be bridged to an adult denominator on a same-universe basis before comparing with the narrow federal proxy. [INFERENCE]

This does not settle marginal school cost, descendant attribution, legal-status/cohort incidence, or receiver-city episodic costs. [INFERENCE]

---

## 2026-06-16 — Pre-rebuild sweep rows marked superseded

### Issue

Several still-indexed June 15 memos carried first-pass sweep rows after the underlying tensor had changed:

- `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` reported Mexico-origin lifetime NPV as `−$79k` and US foreign-born stock as `−$71k`, from the older `<HS`/HS-only NAS seed.
- `immigration-sweep-cycles-13-22-2026-06-15.md` still reported Mexico crude annual `federal − school` as `−$13.5k/adult` and "Mexico ~4x worse than NH white US-born", from the scenario-subset school denominator.
- `immigration-lifetime-unified-theory-2026-06-15.md` had a compressed thesis line implying Mexico's lifetime layer was simply negative.

### Evidence Checked

Current `v_three_layer_annual` rows at the time of that sweep revision (now superseded for origin school rows):

| population | federal/adult | school/adult | crude net/adult |
|------------|--------------:|-------------:|----------------:|
| Mexico-origin | $1,519.28 | superseded | superseded |
| MX + N. Triangle | $1,519.02 | superseded | superseded |
| EU27-origin | $4,694.65 | superseded | superseded |
| NH white US-born | $2,746.33 | $6,023.53 | −$3,277.20 |

Current `v_country_fiscal_rollup` lifetime rows:

| population | layer | per adult |
|------------|-------|----------:|
| FB `<HS` | synthetic age-25 NPV benchmark | −$109,000 |
| Mexico-origin | synthetic age-25 NPV benchmark | $45,631.19 |
| US foreign-born stock | synthetic age-25 NPV benchmark | $212,535.19 |

### Fixes Made

1. Updated `immigration-europe-caucasian-fiscal-findings-2026-06-15.md`:
   - Replaced stale negative Mexico and US-FB lifetime rows with current synthetic age-25 benchmark rows.
   - Replaced the old "college+ missing" warehouse gap with the current caveat: benchmark is age-25 composition, not current-stock lifetime truth.

2. Updated `immigration-sweep-cycles-13-22-2026-06-15.md`:
   - Added a superseded/corrected status note.
   - Replaced stale cycle tables and conclusions with current `v_three_layer_annual` values.

3. Updated `immigration-lifetime-unified-theory-2026-06-15.md`:
   - Clarified that the coexistence claim is federal annual positive, `<HS` lifetime negative, education-mix age-25 benchmark positive, and local episodic negative.

### Current Conclusion

The old negative Mexico rows were not independent evidence. They were stale artifacts of two fixed bugs: the scenario-subset school denominator and the incomplete NAS education-cell seed. [INFERENCE]

---

## 2026-06-16 — CHNV non-substitution headline reversed

### Issue

`research/immigration-causal-surge-2021-2024.md` still presented the active bottom-line claim that CHNV parole **did not substitute** legal flow for illegal flow and instead added on top. That claim had already been reversed by the later parser-bug decision record: the source series was OFO port-of-entry encounters, the program's own lawful channel, misread as total SWB encounters. [DATA]

The confidence ladder had a later correction entry 34, but older entries 26 and 30 still appeared without inline supersession markers. [DATA]

### Evidence Checked

Corrected `chnv_pretrends/results.json`:

| Nationality | USBP pre-6 mean | USBP post-6 mean | Change | OFO pre-6 mean | OFO post-6 mean |
|-------------|----------------:|-----------------:|-------:|---------------:|----------------:|
| Venezuela | 16,488 | 7,000 | −57.5% | 47 | 3,210 |
| Cuba | 28,563 | 1,355 | −95.3% | 32 | 1,252 |
| Nicaragua | 22,063 | 830 | −96.2% | — | — |
| Haiti | 152 | 150 | ~flat | 5,585 | 5,658 |

Other corrected anchors:

- Event-time mean τ[0,+3]: `−2.17` log points.
- Event-time mean τ[+6,+12]: `−1.83` log points.
- Corrected total-CBP DiD: `β=+0.45`, `t=1.29`, null. [SOURCE: decision record]
- The old `+787%` rise was the lawful OFO channel on a scrambled clock. [SOURCE: decision record]

### Fixes Made

1. Updated `research/immigration-causal-surge-2021-2024.md`:
   - Replaced the active bottom-line CHNV claim with the corrected channel-substitution result.
   - Replaced the stale Title-42 evidence summary with the corrected monthly path.
   - Replaced the stale CHNV DiD section with USBP/OFO-separated evidence.
   - Replaced the receiver-city political headline with the Hispanic-share-controlled `+2.4pp` correlational upper-bound.

2. Updated `research/immigration-confidence-ladder.md`:
   - Marked entries 26 and 30 as superseded by entry 34.

### Current Conclusion

CHNV did substitute lawful port flow for irregular between-port crossings in its initial year. It did **not** reduce total receiver load, because the lawful parole inflow still arrived and still belonged in city, shelter, and political ledgers. [INFERENCE]

---

## 2026-06-16 — Card-vs-Borjas wage verdict bounded to observed marginal policy variation

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` still said **"For U.S. policy-relevant variation, Card wins"** and summarized the debate as **"Resolved for U.S. policy variation. Card."** That was too broad after later surge work. The same memo already had the correct caveat that mass-deportation and border-closure shocks have no direct empirical analog; later surge analysis also says the 2021–2024 regime is outside the pre-2021 marginal-policy variation. [DATA]

### Evidence Checked

Local claim surfaces:

- `immigration-causal-synthesis-2026-04-18.md` E-Verify/QWI evidence: native low-skill wage effects were null under observed staggered enforcement mandates. [SOURCE: memo]
- `immigration-confidence-ladder.md` entry 29: "Static-cycle Card-wins finding is BOUNDED to marginal-policy variation; surge is OUTSIDE that variation." [SOURCE: memo]
- `immigration-causal-surge-2021-2024.md`: wage estimates for the 2021–2024 surge period remain unmeasured; mass-deportation enforcement is outside the E-Verify/sanctuary variation. [SOURCE: memo]

### Fixes Made

1. Updated `research/immigration-causal-synthesis-2026-04-18.md`:
   - Replaced "Card wins" with "Card-side pattern wins for observed marginal enforcement variation."
   - Replaced "resolved" with "bounded to observed marginal U.S. policy variation."
   - Made explicit that surge and mass-shock regimes remain open.

### Current Conclusion

The wage-channel evidence rejects large Borjas-style wage losses for the observed E-Verify/sanctuary-style policy variation in the repo. It does **not** prove workers are unaffected under the 2021–2024 surge, mass deportation, border closure, or other capacity-constrained shock regimes. [INFERENCE]

---

## 2026-06-16 — Paradigm synthesis bounded wage and newcomer-ratio claims

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still contained two stale summary claims:

1. "Card wins decisively" and "Future repo memos should treat this as settled" for the wage channel.
2. Domestic U.S.-origin newcomer flow was summarized as `~33x` recent immigration at the median county.

Both were too broad. Later surge work bounds the wage result to observed marginal enforcement variation, and the corrected internal-vs-immigrant newcomer memo replaced the older `33x` annualized stock proxy with ACS `B07001_081E`, giving about `21.7x` for the ratio of medians and `20.5x` for the median county-level ratio among counties with nonzero moved-from-abroad share. The IRS series is domestic U.S.-origin movement, not native-only identity. [DATA]

### Evidence Checked

- `research/immigration-confidence-ladder.md` entry 29: static-cycle Card-wins finding is bounded to marginal-policy variation; surge is outside that variation. [SOURCE: memo]
- `research/immigration-causal-surge-2021-2024.md`: 2021–2024 surge wage estimates remain unmeasured; mass-deportation enforcement is outside observed E-Verify/sanctuary variation. [SOURCE: memo]
- `research/immigration-causal-internal-vs-immigrant-newcomers.md`: current median county comparison is about `4.59%` IRS `Total Migration-US` inflow versus `0.21%` ACS moved-from-abroad, with ratio of medians `21.7x` and median county-level ratio `20.5x`. [SOURCE: memo]

### Fixes Made

1. Updated `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`:
   - Replaced "Card wins decisively" with the bounded claim that the Card-side pattern wins for observed marginal wage variation.
   - Removed the "settled" language for surge/mass-shock regimes.
   - Replaced `33x` newcomer-ratio language with the corrected `20–22x` descriptive range, unit caveat, and domestic-movement caveat.

### Current Conclusion

The paradigm synthesis now carries the same scope discipline as the later claim ledger: marginal enforcement wage evidence is not surge evidence, and county newcomer comparisons are descriptive domestic-vs-abroad denominator corrections, not direct burden estimates. [INFERENCE]

---

## 2026-06-16 — Surge memo removes stale heading frames

### Issue

`research/immigration-causal-surge-2021-2024.md` qualified two stale prior-cycle claims in body text, but its section headings still carried the old frames:

1. "Card wins decisively for U.S. policy variation."
2. "`33x` native to immigrant newcomer ratio at median county."

Those headings were doing rhetorical work against the corrected evidence. The first overstated scope; the second mixed an outdated ratio with a native-identity label unsupported by the IRS `Total Migration-US` measure. [DATA]

### Evidence Checked

- `research/immigration-causal-surge-2021-2024.md`: surge wage estimates remain unmeasured; the surge and mass-deportation regimes sit outside observed E-Verify/sanctuary variation. [SOURCE: memo]
- `research/immigration-causal-internal-vs-immigrant-newcomers.md`: current median comparison is `21.7x` ratio of medians and `20.5x` median county-level ratio; IRS `Total Migration-US` is not native-only. [SOURCE: memo]

### Fixes Made

1. Replaced the Card heading with "Card-side pattern for marginal pre-surge policy variation — surge caveat."
2. Replaced the `33x` native/immigrant heading with a domestic-vs-abroad median ratio caveat.
3. Weakened the receiver-node paragraph to an estimand caveat: the median county comparison does not measure concentrated receiver-city shelter, legal, language, or school burdens.

### Current Conclusion

The surge memo now says what the evidence can support: marginal pre-surge wage evidence stays bounded, and median domestic-vs-abroad flow comparisons cannot dismiss receiver-node burden channels. [INFERENCE]

---

## 2026-06-16 — Confidence ladder marks receiver-swing causal sentence stale

### Issue

`research/immigration-confidence-ladder.md` entry 28 still contained the sentence "Magnitude implausibly large for non-immigration causes alone." Entry 31 later says that phrase should not be reused, and entry 36 closes the Hispanic-share control with a bounded `+2.4pp` receiver coefficient. Leaving the sentence unmarked created a grep hazard: an agent could quote the old causal-strength language while missing the later correction. [DATA]

### Evidence Checked

- `research/immigration-confidence-ladder.md` entry 31: the "implausibly large" phrase is a plausibility assertion doing causal work and should not be reused. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entry 36: Hispanic-share control leaves receiver coefficient about `+2.4pp`, still cross-sectional and policy-endogenous; use as bounded upper-bound framing. [SOURCE: memo]
- `research/immigration-causal-surge-2021-2024.md`: current most-defensible reading uses the controlled `+2.4pp` as the bounded claim and keeps confounders unresolved. [SOURCE: memo]

### Fixes Made

1. Kept entry 28 append-only, but marked its final causal-implausibility sentence as superseded by entries 31 and 36.
2. Added an inline warning not to reuse the sentence and to use the controlled `+2.4pp` upper-bound framing instead.

### Current Conclusion

The receiver-city election evidence remains a medium-strength correlation that survived the named Hispanic-share kill-test, not a causal proof that the surge alone drove the full raw GOP swing. [INFERENCE]

---

## 2026-06-16 — Paradigm synthesis narrows rent-welfare claim

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said "Rent exposure IS welfare loss." That was stronger than the Saiz memo supports. The source evidence is a strong cross-sectional pattern: immigrants concentrate in low-elasticity MSAs with higher rents, and regulatory constraint predicts foreign-born share better than topographic unavailability in the decomposition. It does not identify immigrant-specific rent causation or net welfare incidence. [DATA]

### Evidence Checked

- `research/immigration-causal-saiz-elasticity-rent.md`: status is "Cross-sectional descriptive"; welfare-loss implication is `MODERATE` and needs IV identification to attribute causation to immigrant inflow specifically. [SOURCE: memo]
- `research/immigration-causal-synthesis-2026-04-18.md`: safer phrasing is "rent exposure is closer to welfare loss in destination markets" and should be elasticity-conditional. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entry 20: implication is "closer to welfare loss than the adversarial review allowed," not a direct welfare-loss proof. [SOURCE: memo]

### Fixes Made

1. Replaced "Rent exposure IS welfare loss" with "Rent exposure is closer to welfare loss in inelastic destination markets."
2. Kept zoning reform as a plausible lever, but attached the causal caveat that immigrant-specific rent causation still needs panel/IV identification.

### Current Conclusion

The housing evidence defeats the blanket "rent exposure is not welfare loss" dismissal, but only conditionally: in inelastic destination markets, rent exposure is a stronger renter-incidence warning, not a completed aggregate welfare proof. [INFERENCE]

---

## 2026-06-16 — Saiz rent memo removes causal language from cross-section

### Issue

`research/immigration-causal-saiz-elasticity-rent.md` labeled itself "Cross-sectional descriptive," but the bottom line and implication bullets still used causal phrases: housing supply "cannot respond," rent appreciation has "nowhere to go," marginal newcomers "drive up cost burden," and the adversarial caveat was "partially defeated." Those phrases overstate what the Saiz x ACS cross-section identifies. [DATA]

### Evidence Checked

- The memo's own status line says the instrumental-variable extension is the next step. [SOURCE: memo]
- The limitations section says the causal reading "immigrant inflows raise rent more in inelastic markets" needs panel variation and an instrument for immigrant share. [SOURCE: memo]
- The numeric results support a descriptive pattern: low-elasticity MSAs have higher foreign-born share and higher rent, but the cross-section does not separate immigrant inflow from amenities, wages, native demand, or other destination selection. [INFERENCE]

### Fixes Made

1. Replaced "cannot respond" / "nowhere to go" / "fixed stock" language with relatively inelastic supply and renter-incidence risk.
2. Added the explicit panel/IV caveat to the implication bullet.
3. Replaced "partially defeated" with "narrowed" for the adversarial rent-exposure caveat.

### Current Conclusion

The Saiz merge strengthens an elasticity-conditional housing-burden warning. It does not by itself prove immigrant-specific rent causation or aggregate welfare loss. [INFERENCE]

---

## 2026-06-16 — Causal synthesis mirrors Saiz rent caveat

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` preserved the same housing overstatement after the Saiz source memo was narrowed. It said supply "can't respond," "rent appreciation is welfare loss," the rent burden question was "Partially resolved ... yes," and the proposed Saiz x PUMA rerun would produce a "rent welfare estimate." Those claims exceed the current cross-sectional evidence. [DATA]

### Evidence Checked

- `research/immigration-causal-saiz-elasticity-rent.md`: descriptive correlation is high-confidence; immigrant-specific rent causation and welfare incidence need panel/IV identification and tenure accounting. [SOURCE: memo]
- `research/immigration-causal-synthesis-2026-04-18.md`: the same memo already lists "Causal IV for housing" as unsettled, so its verdict language needed to match its own limitation section. [SOURCE: memo]

### Fixes Made

1. Replaced "closer to welfare loss because supply can't respond" with "stronger renter-incidence warning because supply response is weaker."
2. Replaced "rent appreciation is welfare loss" with a panel/IV caveat.
3. Replaced "partially resolved ... yes" with "narrowed, not resolved."
4. Relabeled the proposed Saiz x PUMA rerun as an origin-conditional renter-incidence screen, not a final welfare estimate.

### Current Conclusion

The April 18 causal synthesis now treats housing as an elasticity-conditional local-burden warning, not as a completed rent-welfare causal estimate. [INFERENCE]

---

## 2026-06-16 — Lifetime brainstorms stop scalarizing Saiz rent screen

### Issue

Two tracked lifetime-planning memos carried the same Saiz overstatement into future work:

1. `research/immigration-lifetime-dataset-brainstorm-2026-06-15.md` said the Saiz layer shows "rent burden is welfare loss, not price discovery."
2. `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` framed the Saiz country slice as "welfare loss $" and "local welfare loss."

That would make later agents build a scalar welfare-loss line from a screen that is only descriptive until tenure mix and panel/IV identification are added. [DATA]

### Evidence Checked

- `research/immigration-causal-saiz-elasticity-rent.md`: the current evidence is a high-confidence descriptive correlation and only a moderate welfare-interpretation update. [SOURCE: memo]
- `research/immigration-causal-synthesis-2026-04-18.md`: the corrected downstream synthesis now treats the Saiz x PUMA rerun as an origin-conditional renter-incidence screen, not a final welfare estimate. [SOURCE: memo]

### Fixes Made

1. Replaced "rent burden is welfare loss" with "elasticity-conditional renter-incidence screen."
2. Replaced "welfare loss $" / "local welfare loss" future-work language with renter-incidence risk / local-incidence offset language.

### Current Conclusion

Future lifetime-country work should use Saiz as a targeting and incidence screen until it has the missing causal and tenure-incidence pieces needed for a welfare scalar. [INFERENCE]

---

## 2026-06-16 — E-Verify wage null no longer becomes inflow null

### Issue

Two wage memos still converted a marginal-enforcement result into a broader immigration-level conclusion:

1. `research/immigration-causal-everify-card-vs-borjas.md` said native low-skill workers are "not measurably hurt by current low-skill immigration levels."
2. `research/immigration-causal-synthesis-2026-04-18.md` said native low-skill workers "do not lose from immigrant inflows" and the labor-market component is "approximately zero for natives."

The E-Verify design measures wage response to observed state mandate variation, not the full wage effect of current low-skill immigration levels, surge regimes, cash-economy substitution, employment composition, hours, or mass shocks. [DATA]

### Evidence Checked

- `research/immigration-causal-everify-card-vs-borjas.md`: treatment is state E-Verify mandate timing; caveats include external validity, partial compliance, cash-economy substitution, and non-wage channels. [SOURCE: memo]
- `research/immigration-causal-surge-2021-2024.md`: surge-period wage estimates remain unmeasured and outside pre-2021 marginal-policy variation. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entry 29: Card-side finding is bounded to marginal-policy variation; surge is outside that variation. [SOURCE: memo]

### Fixes Made

1. Replaced "not measurably hurt by current low-skill immigration levels" with a narrower claim: no measurable native wage gains from E-Verify-style restrictions, rejecting large Borjas-style gains from marginal removal.
2. Replaced "do not lose from immigrant inflows" and "labor-market component ... approximately zero" with "observed marginal-enforcement wage component is small/null."
3. Reopened non-wage labor-market channels and surge/mass-shock regimes explicitly.

### Current Conclusion

The wage evidence is strong against large native wage gains from observed marginal enforcement contractions. It is not a direct proof that current low-skill immigration levels or surge inflows have zero native labor-market effect. [INFERENCE]

---

## 2026-06-16 — Surge capacity and deportation validation claims bounded

### Issue

`research/immigration-causal-surge-2021-2024.md` overstated two validation claims:

1. Receiver-city gross outlays and shelter stress were described as "system-collapse evidence" and as empirical validation of a national housing/construction capacity calibration.
2. The mass-deportation simulation was labeled "partially validated" using qualitative early indicators, while the same paragraph said quantitative replication awaited post-2025 data.

The available local evidence supports gross receiver-node load and visible shelter/budget stress. It does not estimate net fiscal burden, validate a national 10M+/year arrival threshold, or quantitatively validate the mass-deportation output simulation. [DATA]

### Evidence Checked

- `research/immigration-causal-surge-2021-2024.md`: receiver-city figures are city/state cost trajectories and shelter caps, not a netted burden model. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entry 33: receiver-city figures are gross outlays; federal reimbursements and counterfactual baseline growth are not netted out. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entry 32: mass-deportation output shock is a calibration with frozen replacement hiring, wage response, and capital reallocation. [SOURCE: memo]

### Fixes Made

1. Reframed receiver-city evidence as gross-load and shelter-stress evidence, not "system collapse" or national capacity validation.
2. Replaced "empirically validated" with "directionally consistent" and named the missing national capacity function.
3. Replaced "Mass-deportation simulation — partially validated" with "not yet quantitatively validated."
4. Marked confidence-ladder entry 27 as scope-qualified by entry 33's gross-vs-net caveat.

### Current Conclusion

The surge evidence shows concentrated receiver-node stress. It should not be cited as a net fiscal-burden estimate, a national capacity threshold validation, or a quantitative validation of the mass-deportation output model. [INFERENCE]

---

## 2026-06-16 — Receiver-election wording made correlational

### Issue

`research/immigration-causal-surge-2021-2024.md` already warned that the receiver-city election result is a correlational upper-bound, but its interpretation still said the 2024 election shift was "partially related to surge exposure" and that receiver-city GOP shift reflected "natives' response." That wording overstates identification and erases naturalized-citizen / electorate-composition channels. [DATA]

### Evidence Checked

- `research/immigration-causal-surge-2021-2024.md`: the reading rule says the raw receiver-city gap is descriptive only and the `+2.4pp` coefficient is a correlational upper-bound. [SOURCE: memo]
- The same memo lists unresolved confounders: Hispanic realignment, inflation, pre-existing RGV trend, and noncitizen voting ineligibility. [SOURCE: memo]
- `research/immigration-confidence-ladder.md` entries 31 and 36: use the controlled `+2.4pp` as an upper-bound; causal interpretation needs more work. [SOURCE: memo]

### Fixes Made

1. Replaced "partially related to surge exposure" with "correlated with receiver-city / border-surge exposure."
2. Replaced "natives' response" with "citizen electorate's response or composition."
3. Added unresolved compositional confounding to the CURRENT-inflow interpretation.

### Current Conclusion

The receiver-city election result remains a medium-strength association that survived the named Hispanic-share kill-test. It is not clean causal evidence of voter backlash from the surge. [INFERENCE]

---

## 2026-06-16 — Embedded surge ladder gross-load wording aligned

### Issue

`research/immigration-causal-surge-2021-2024.md` had already reframed receiver-city costs as gross-load and shelter-stress evidence, but its embedded confidence-ladder entry 27 still ended with "System-collapse claim has empirical bite." That sentence recreated the same overclaim inside a later section of the same memo. [DATA]

### Why it was wrong

The administrative cost rows support visible receiver-load stress and concentrated gross outlays. They do not by themselves identify net fiscal burden after reimbursements and counterfactual baseline costs, and they do not validate a national system-collapse threshold. [INFERENCE]

### Fix

Replaced the embedded ladder sentence with the narrower claim that receiver-load stress has empirical bite while the figures remain gross outlays, not net fiscal-burden or national system-collapse proof. [SOURCE: memo]

### Updated conclusion

The surge memo is now internally consistent on receiver-cost scope: receiver-city costs are strong gross-load evidence, not a completed net-burden or national-collapse estimate. [INFERENCE]

---

## 2026-06-16 — Caplan audit political-incidence mechanism bounded

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` still treated "backlash" as a settled mechanism in several verdict and DAG lines. Later receiver-city work supports a political-response association, but explicitly leaves mechanism unresolved: persuasion, turnout, sorting, Hispanic realignment, and busing-target endogeneity are not cleanly separated. [DATA]

### Why it was wrong

Caplan's narrow median-voter argument still fails as a full political-incidence answer because immigrant voting is not the only channel. But the repo should not convert a bounded receiver-city correlation into a completed backlash mechanism. [INFERENCE]

### Fix

Replaced the stale backlash/decisive/impossible phrasing with bounded political-response language. The Caplan audit now says local overload, legitimacy effects, and possible citizen response remain live, while mechanism identification remains unresolved. [SOURCE: memo]

### Updated conclusion

The Caplan critique survives, but on a narrower basis: his political-externality answer is incomplete because local political-response channels cannot be assumed zero, not because the repo has cleanly proven a backlash mechanism. [INFERENCE]

---

## 2026-06-16 — Capacity-frontier political outcome label bounded

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` used "backlash" in its bottom line, claims table, and synthesis even though its own open-questions section says county returns do not identify whether the effect is turnout, persuasion, composition change, or precinct-level backlash. [DATA]

### Why it was wrong

The data rows support a county-level political-response association. They do not identify the voter-level mechanism. Calling the outcome "backlash" hard-codes one interpretation that the memo itself lists as unresolved. [INFERENCE]

### Fix

Replaced the active backlash labels with political-response language, changed "settled enough" to "stable enough," and updated the immigration index descriptions for the Caplan, threshold, and county-outcome memos. [SOURCE: memo]

### Updated conclusion

The capacity-frontier memo now treats GOP margin movement as a political-response metric. Backlash remains one possible mechanism to test, not the name of the measured outcome. [INFERENCE]

---

## 2026-06-16 — Mass-deportation output headline separated from sensitivity

### Issue

`research/immigration-confidence-ladder.md` entry 32 already said the mass-deportation output shock should lead with the first-order figure and keep the Type-II multiplier endpoint only as a labeled sensitivity. But entry 24 still headlined the combined `$1.5-2.3T` / `5-8% GDP` range, and `research/immigration-causal-surge-2021-2024.md` repeated the same `~5-8% GDP` presentation. [DATA]

### Why it was wrong

The Type-II endpoint stacks a modeled multiplier on top of a calibration that freezes replacement hiring, wage response, and capital reallocation. It is useful as a sensitivity, but headlining it as a range launders a modeled amplifier into the main estimate. [INFERENCE]

### Fix

Changed the ladder entry and surge memo to lead with the first-order `~$1.45T` / `~5% GDP` figure and label the `~$2.32T` / `~8%` endpoint as Type-II sensitivity only. [SOURCE: memo]

### Updated conclusion

The mass-deportation output-shock claim remains medium-confidence calibration evidence, but the headline is now the first-order estimate; multiplier amplification is not presented as coequal estimate truth. [INFERENCE]

---

## 2026-06-16 — ICE docket denominator error removed from crime memo

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` correctly warned that the ICE ERO criminal-history counts are docket stock figures rather than rates, but then said dividing by the `~11M` unauthorized immigrant population and an accumulation period yields rates far below native-born equivalents. It also described the source as a non-detained-docket table when the ICE letter reports the **national docket** split into detained and non-detained columns. The source table is for **noncitizens on ICE's national docket**, not an unauthorized-only numerator. [SOURCE: ICE ERO letter]

### Why it was wrong

That denominator move silently mixes universes: all noncitizens on an ICE docket in the numerator, unauthorized immigrant stock in the denominator, and an unspecified accumulation period for person-time. It turns a valid stock-vs-rate warning into a new rate-base error. [INFERENCE]

### Fix

Replaced the naive division claim with a refusal to compute a native comparison from those counts, and relabeled the table as national-docket rather than non-detained-docket. The memo now says the ICE counts do not by themselves provide a per-capita native comparison or overturn rate-based studies. [SOURCE: memo]

### Updated conclusion

The crime memo's bottom-line directional claim is unchanged, but its ICE-docket section no longer uses an invalid unauthorized-stock denominator. [INFERENCE]

---

## 2026-06-16 — Paradigm synthesis calibration headlines bounded

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still carried two stale calibration presentations: mass deportation was headlined as a `$1.5-2.3T` / `5-8% GDP` range, and the open-borders calibration row described housing capacity as binding above `~10M/year` arrivals without enough warning that this was a modeled threshold, not a validated national capacity function. [DATA]

### Why it was wrong

Later fixes established that the deportation multiplier endpoint is a Type-II sensitivity, not a coequal estimate, and that surge-era receiver stress is only directionally consistent with the national capacity calibration. The April synthesis had not inherited those scope bounds. [INFERENCE]

### Fix

Changed the mass-deportation rows and ladder excerpt to lead with the first-order `~$1.45T` / `~5% GDP` output shock, labeling `~$2.32T` / `~8%` as Type-II sensitivity. Reframed the `~10M/year` housing/construction statement as a calibration warning for very-large-arrival scenarios rather than a validated national threshold. [SOURCE: memo]

### Updated conclusion

The paradigm synthesis still flags large-output and capacity risks, but now treats both as calibration outputs with sensitivity labels rather than measured all-scenario thresholds. [INFERENCE]

---

## 2026-06-16 — Capacity-frontier threshold language made descriptive

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` still described the threshold as "real," called `flow / local build capacity` the "right object," and closed by saying "`flow + capacity` is where the new causal traction is coming from." The memo's own design is a county-panel/model-comparison surface, not a clean causal identification design. [DATA]

### Why it was wrong

The threshold grid and model comparisons show recurring descriptive patterns, but they do not by themselves separate inflow effects from housing response, destination selection, baseline affordability, policy targeting, or omitted local shocks. Calling that "causal traction" overstates the design. [INFERENCE]

### Fix

Replaced "real threshold" and "causal traction" phrasing with "recurring/observed/descriptive threshold pattern" and named the need for stronger counterfactual design before causal interpretation. [SOURCE: memo]

### Updated conclusion

The capacity-frontier memo still says load/capacity is the better county stress surface, but it no longer treats the threshold-grid pattern as identified causal truth. [INFERENCE]

---

## 2026-06-16 — Crime conclusion estimand made explicit

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` correctly listed reporting, detection, deportation, and denominator problems, but its bottom line still said unauthorized immigrants "commit crimes" at lower rates. The Caplan audit inherited the same blur when summarizing the crime objection. [DATA]

### Why it was wrong

The strongest evidence is about observed arrest, conviction, incarceration, and institutionalization outcomes. Those are not identical to true offending when underreporting, police contact, deportation censoring, and denominator uncertainty are active mechanisms. [INFERENCE]

### Fix

Reframed the crime memo's question, bottom line, confidence statement, international caveat, and uncertainty section around observed criminal-justice rates. Updated the Caplan audit to say the claim mostly survives for observed U.S. first-generation / unauthorized justice-system rates, while true offending is less directly identified. [SOURCE: memo]

### Updated conclusion

The directional crime finding survives, but its estimand is now explicit: lower observed justice-system rates in current U.S. evidence, not directly measured lower true offending in every subgroup or context. [INFERENCE]

---

## 2026-06-16 — Unified fiscal synthesis bounded from universal survival claim

### Issue

`research/immigration-lifetime-unified-theory-2026-06-15.md` said its explanatory story "survives all datasets," that "data cannot kill" the coherent mechanism, and that "all channels are real in their layer." That overstated what a heterogeneous warehouse of annual proxies, lifetime NPV benchmarks, local descriptive burdens, receiver-city ledgers, and theory papers can identify. [DATA]

### Why it was wrong

A layered tensor is the right anti-scalar frame, but it is still falsifiable. New data can kill channel magnitudes, signs for particular cells, annual-to-lifetime bridges, destination-specific incidence, or equilibrium assumptions. The robust correction is narrower: one dataset layer should not be exported as the total immigration conclusion without matching the ledger, cell, and cohort. [INFERENCE]

### Fix

Replaced the universal "survives all datasets" and "data cannot kill" language with a current-warehouse-compatible working synthesis. Reframed the narrative spine as still falsifiable and changed "all channels are real" to evidence-in-layer language with varying identification strength. Added a memo revision row documenting the confidence bound. [SOURCE: memo]

### Updated conclusion

The fiscal-tensor synthesis still stands as the best current organizing frame, but it is no longer presented as immune to future evidence. Its strongest conclusion is anti-scalar: do not collapse layer, cell, and cohort into one immigration fiscal number. [INFERENCE]

---

## 2026-06-16 — Native-low-skill political-economy inference narrowed

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` said the policy push from native low-skill voters could not easily be justified by their wage data, but "can be justified" by their school-finance and rent exposure. That moved too quickly from incidence evidence to voter motivation and policy justification. [DATA]

### Why it was wrong

The E-Verify wage evidence can weaken a wage-only restriction story within observed marginal-enforcement variation. It does not identify why voters support restriction, and the Saiz/school channels are exposure mechanisms, not proofs that a particular voter group is correctly optimizing over those burdens. Rent incidence depends on renter/owner status; school incidence depends on local fiscal institutions and child composition; political support also includes values and credibility beliefs. [INFERENCE]

### Fix

Replaced the "can be justified" line with a narrower statement: wage data alone are weak support for the native-low-skill wage story, while school-finance and renter exposure remain plausible incidence channels. Added a revision note to the synthesis memo. [SOURCE: memo]

### Updated conclusion

The political-economy conclusion survives only as a channel map: wage evidence is weak for the observed range, and school/rent channels remain live. The memo no longer claims those channels identify voter motivation or justify the policy push. [INFERENCE]

---

## 2026-06-16 — Crime search-log absence claim bounded

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` logged the Exa verification pass for higher-rate studies as "No peer-reviewed support found." In a search log, that reads like a literature-wide proof of absence rather than the result of a particular pass. [DATA]

### Why it was wrong

Search tools can support "not found in this query/pass" much more safely than "does not exist." The memo already has a strong bottom line from named studies and named critiques; it does not need an unbounded absence claim in the provenance table. [INFERENCE]

### Fix

Changed the row to "No peer-reviewed higher-rate study found in this pass; Lott Arizona remained the prominent non-peer-reviewed outlier" and added a memo revision note. [SOURCE: memo]

### Updated conclusion

The crime memo's substantive conclusion is unchanged. The provenance is now narrower: the pass failed to find a peer-reviewed higher-rate study; it does not claim an exhaustive proof that none exists. [INFERENCE]

---

## 2026-06-16 — Capacity-frontier claims table scoped to model output

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` had already been narrowed away from causal-threshold language, but its claims table still listed several county model patterns as `HIGH | VERIFIED` without explaining that those labels were about artifact-backed model output, not causal identification. [DATA]

### Why it was wrong

For a reader scanning the table, `HIGH | VERIFIED` can look like a validated causal effect. The listed artifacts verify correlations, model rankings, interaction-grid patterns, and decile summaries; they do not by themselves identify immigration-caused wage, employment, sorting, or political effects. [INFERENCE]

### Fix

Added a scope note below the claims table: `HIGH` and `VERIFIED` mean the reported model-output pattern is file-backed and reproducible from the listed artifacts, not that the county associations are clean causal effects. Added a memo revision entry. [SOURCE: memo]

### Updated conclusion

The capacity-frontier evidence remains useful as a descriptive stress surface. Its table is now explicitly scoped so reproducibility of the model output is not confused with causal validity. [INFERENCE]

---

## 2026-06-16 — E-Verify Card-vs-Borjas source memo bounded to design margin

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` correctly narrowed several later synthesis claims, but the source memo still said "the data side with Card, not Borjas" and described the result as "a Card-style world." It also said Friedman's Card-style premise was "confirmed" and Camarota's native-wage argument "doesn't pass this test" without enough scope language. [DATA]

### Why it was wrong

The E-Verify TWFE design can reject large Borjas-style native wage gains for the observed enforcement margin. It cannot settle all low-skill immigration wage effects, surge regimes, mass deportation, open borders, or non-wage channels. The commentator-update language needed to inherit that same external-validity bound. [INFERENCE]

### Fix

Replaced the global "data side with Card" phrasing with "in this E-Verify design, the wage results are closer to the Card-style null than to large Borjas-style native wage gains." Reframed "Card-style world" as "for this enforcement margin" and bounded the Friedman/Camarota update lines to the wage-channel test. Added a memo revision note. [SOURCE: memo]

### Updated conclusion

The E-Verify result remains strong against large native wage gains from marginal enforcement. It no longer reads as a global settlement of Card vs Borjas, open borders, or all native labor-market channels. [INFERENCE]

---

## 2026-06-16 — Paradigm synthesis wage-rejection labels scoped

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still compressed the E-Verify and sanctuary wage results into short-form labels like "STRONG REJECTION of Borjas" and "STRONG REJECTION of enforcement-channel wage effects." That was sharper than the source designs justified. [DATA]

### Why it was wrong

The source designs are strong against large native wage gains under observed E-Verify/sanctuary-style policy variation. They do not reject every Borjas-style claim, every enforcement-channel wage effect, or shock regimes outside the tested policy margins. The short-form table needed to carry the same external-validity bound as the body text. [INFERENCE]

### Fix

Changed the findings table and embedded ladder snippet to say the evidence is strong against large Borjas-style wage gains in the tested enforcement margin and shows a strong null result for the tested policy variations. Added a memo revision note. [SOURCE: memo]

### Updated conclusion

The paradigm synthesis still supports a Card-side null for observed marginal wage variation, but its short labels no longer imply global rejection of Borjas or all enforcement-channel wage effects. [INFERENCE]

---

## 2026-06-16 — Saiz zoning-channel inference made descriptive

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and `research/immigration-confidence-ladder.md` described the Saiz decomposition as showing that the inelastic-MSA immigrant concentration was "driven by" regulatory constraint and that zoning reform was a viable policy lever. The source regression only showed WRLURI was a stronger correlate of foreign-born share than topographic unavailability. [DATA]

### Why it was wrong

A cross-sectional regression of foreign-born share on WRLURI, topographic unavailability, and log population does not identify the causal direction. WRLURI may proxy high-demand metro governance, amenities, historical settlement, political economy, or endogenous restrictions. It can make zoning reform a plausible hypothesis, but not a proven causal substitute for immigration restriction or a verified way to reduce immigrant renter burden. [INFERENCE]

### Fix

Replaced "regulatory channel dominates" / "driven by regulatory constraint" language with "WRLURI is the stronger correlate" and "strong descriptive regression, not causal channel proof." Reframed zoning reform as a plausible policy hypothesis rather than an identified causal lever. Added append-only confidence-ladder entry 38 as a scope correction to entry 20. [SOURCE: memo]

### Updated conclusion

The Saiz result still strengthens the housing-incidence warning in inelastic destination markets, but the regulatory decomposition is descriptive. It should motivate a panel/IV zoning test, not be used as proof that zoning caused the concentration or that zoning reform resolves the rent-burden channel. [INFERENCE]

---

## 2026-06-16 — Federal distribution memo aligned to native-white microsim anchor

### Issue

`research/immigration-federal-distribution-findings-2026-06-15.md` still reported an older NH-white federal proxy of `~$3,600–4,000/adult` and a `~2.3–3.0×` per-adult white/Mexico ratio. Later built tensor artifacts report `NH white US-born ~$2,746/adult`, `Mexico-origin ~$1,519/adult`, and an `~1.8×` ratio from `acs_nh_white_federal_microsim_2023`. [DATA]

### Why it was wrong

The older row came from an ACS wage-imputation sensitivity path. Once the native-white microsim existed, keeping the old range as the headline silently forked the current conclusion and overstated the narrow federal-cash-proxy gap. The aggregate total also changed: `~$253B` vs `~$12.9B` is about `19.6×`, not `25×`, with roughly `11×` from population count alone. [DATA]

### Fix

Updated the distribution memo's per-adult table, aggregate table, decomposition, verdict, limitation row, and revision log to use the current built native-white microsim anchor. Marked the older `~2.8–3.1×` wage-imputation sensitivity as superseded for headline use. [SOURCE: memo]

### Updated conclusion

The distribution conclusion is narrower: on the current built narrow federal cash proxy, NH white US-born adults are about `1.8×` Mexico-origin adults, mostly because of education composition. This remains layer-specific and does not settle full federal liability, lifetime NPV, or all-government fiscal incidence. [INFERENCE]

---

## 2026-06-16 — Lifetime-country brainstorm trigger aligned to corrected proxy ratio

### Issue

`research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still opened from the stale premise that distribution findings showed a `~2–3×` per-capita federal proxy gap between whites and Mexico-born adults. That was the older wage-imputation headline superseded by the built native-white microsim. [DATA]

### Why it was wrong

Even though the brainstorm's main tensor logic remained valid, the trigger line would send future readers back into the older ratio. The correct current anchor is `~1.8×` per adult on the narrow federal proxy, with the same larger point intact: lifetime NPV and country-level net still require stacked layer accounting. [INFERENCE]

### Fix

Changed the trigger to the current `~1.8×` NH-white-US-born/Mexico-origin federal proxy ratio and added a revision row pointing back to this audit. [SOURCE: memo]

### Updated conclusion

The brainstorm still motivates a lifetime/country tensor, but no longer inherits the stale `~2–3×` federal-proxy premise. [INFERENCE]

---

## 2026-06-16 — School crude-net table made symmetric on child attribution

### Issue

`research/immigration-school-burden-per-adult-2026-06-15.md` warned that immigrant-headed household school costs should not be read without descendant future taxes, but the headline table also showed NH-white crude rows around `−$3,277/adult` without an equally explicit warning that those native rows are not a native fiscal-loss finding. [DATA]

### Why it was wrong

The `net_crude_federal_minus_school` view assigns current average K–12 costs to current adults and omits descendant future taxes, lifetime accounting, marginal pupil costs, Medicaid, non-school local services, and full federal taxes. That limitation is symmetric. Reading the NH-white negative row as "native whites are fiscally negative" would be the same layer-laundering error as reading the Mexico positive row as all-government fiscal positivity. [INFERENCE]

### Fix

Added a table-scope warning below the headline table and expanded the child-attribution caveat to say the native rows have the same accounting limitation. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The school layer still shows static visibility math: Mexico-origin is `+$748/adult` and NH-white US-born is `−$3,277/adult` under this crude average-cost assignment. Neither row is a welfare verdict or lifetime fiscal sign. [INFERENCE]

---

## 2026-06-16 — FAIR ledger no longer labeled mathematical upper bound

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` described FAIR's `$150.7B` unauthorized-immigration cost estimate as an "upper-bound political ledger." That language was too generous statistically: FAIR is advocacy-sourced and uses contested attribution choices, including citizen-child cost assignment and stock/method differences versus Pew and ITEP. [DATA]

### Why it was wrong

"Upper bound" implies the number bounds the true cost from above. FAIR's construction is better treated as an advocacy high-cost ledger: it may include broad cost categories omitted by NAS individual NPV, but that does not make it a validated upper limit. Some choices can overstate marginal public cost, while omitted or differently treated categories could move in either direction. [INFERENCE]

### Fix

Renamed the chain from "Annual full budget" to "Annual advocacy ledger," replaced "upper-bound political ledger" with "advocacy high-cost ledger," and changed the rhetoric table's "Upper bound" row accordingly. Added a memo revision note. [SOURCE: memo]

### Updated conclusion

The restrictionist steel-man still preserves the full-budget ledger as a real argument family, but FAIR is now source-graded correctly: useful as a high-cost advocacy construction, not as empirical fact or a mathematical upper bound. [INFERENCE]

---

## 2026-06-16 — E-Verify proposed ladder label aligned to margin-specific verdict

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` had already bounded its headline Card-vs-Borjas conclusion, but its "What this updates" section still proposed adding a confidence-ladder entry labeled `STRONG REJECTION`. That leftover label conflicted with the source memo's own external-validity caveat. [DATA]

### Why it was wrong

The E-Verify design is strong against large Borjas-style native wage gains in the observed E-Verify margin. It is not a global rejection of all Borjas-style substitution claims, all enforcement-channel wage effects, or surge/mass-shock regimes. A suggested ladder entry should not be broader than the result it summarizes. [INFERENCE]

### Fix

Changed the proposed ladder label to "strong against large Borjas-style gains in this E-Verify margin" and added a source-memo revision note. The append-only confidence ladder already has entry 29 bounding the older wage entries to marginal policy variation, so no ladder rewrite was needed. [SOURCE: memo]

### Updated conclusion

The source memo's short-form update now matches the main evidence statement: strong against high-end Borjas magnitudes for this policy margin, not a universal rejection. [INFERENCE]

---

## 2026-06-16 — Causal synthesis inherited stale global E-Verify rejection label

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` still embedded a suggested confidence-ladder addition rating the E-Verify wage result as `STRONG REJECTION`. That block is reusable guidance, so it would keep propagating the pre-boundary label even after the source E-Verify memo was narrowed. [DATA]

### Why it was wrong

The synthesis itself already says surge and mass-shock regimes remain open. The E-Verify design excludes large Borjas-style native wage gains for observed mandate variation; it does not reject every labor-substitution claim or every counterfactual enforcement shock. A ladder suggestion cannot be broader than the identification margin that produced it. [INFERENCE]

### Fix

Replaced the embedded ladder rating with "strong against large Borjas-style gains in the E-Verify margin," changed the reason to name the observed mandate design, and narrowed the summary table row from "Borjas wage prediction rejected" to "large Borjas-style native wage gains" in that policy variation. Added a synthesis revision row. [SOURCE: memo]

### Updated conclusion

The April causal synthesis is now aligned with the later bounded source memo: strong Card-side evidence for observed E-Verify policy variation, not a global E-Verify-based rejection of Borjas-style claims. [INFERENCE]

---

## 2026-06-16 — Restrictionist steel-man overread receiver stress as collapse

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still used crisis/collapse/catastrophe language around the receiver-city layer: surge-era immigration "created visible local fiscal/social crisis," the NAS benchmark omitted a "system collapse" story, the admin-budget gap "validates" the +$46k critique, and the strongest fair claim described shelter/school effects as "locally catastrophic." [DATA]

### Why it was wrong

The cited receiver evidence supports gross shelter/budget load and visible receiver-city stress. Gould's sheltered-homelessness result and NYC/receiver-city cost rows are material, but they do not by themselves estimate net fiscal burden after reimbursements and baseline costs, identify national system collapse, or allocate administrative costs to the Mexico-origin NPV cell. The steel-man should preserve the layer without overstating what it identifies. [INFERENCE]

### Fix

Changed the policy implication to receiver-city shelter/budget stress; replaced "system collapse" with receiver-capacity stress; changed "validates" to support for an omitted admin-allocation layer; changed "locally catastrophic" to locally severe in shelter/school-capacity ledgers; and bounded the disconfirmation table to gross episodic receiver-stress evidence rather than net/collapse proof. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The restrictionist steel-man still keeps the receiver-stress objection alive, but it no longer upgrades gross local outlays and shelter stress into a national-collapse or completed net-fiscal verdict. [INFERENCE]

---

## 2026-06-16 — Saiz ladder correction made visible at old entry

### Issue

`research/immigration-confidence-ladder.md` already had append-only entry 38 correcting entry 20's zoning-causation language, but entry 20's title still presented the old causal reading without an inline qualification. A reader scanning the original ladder section could miss the later scope correction. [DATA]

### Why it was wrong

The append-only rule preserves old judgments, but superseded or qualified claims need visible pointers at the old claim site when they are likely to be reused. Entry 20's title said the correlation "operates through" regulation; entry 38 says the WRLURI result is descriptive and not identified zoning causation. Without a title pointer, the old claim remained too easy to quote out of scope. [INFERENCE]

### Fix

Annotated entry 20's title with `QUALIFIED by entry 38` while leaving the historical reason text intact. [SOURCE: memo]

### Updated conclusion

The confidence ladder now keeps its append-only history while making the current Saiz scope correction visible where the older causal title appears. [INFERENCE]

---

## 2026-06-16 — Crime memo downgraded fetched-but-unread European row

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` marked the European mixed-evidence row as `VERIFIED (direction), not fully analyzed`. That status is self-contradictory: the row relied on a fetched Skardhamar et al. paper that the memo explicitly says was not fully analyzed. [DATA]

### Why it was wrong

"Verified" should mean the memo has checked enough of the source to certify the claim. Here the safer claim is only that European evidence may be more mixed and that at least one fetched Scandinavian study appears relevant. Without analyzing the paper's definitions, denominators, offense categories, adjustment set, and immigrant subgroups, the memo should not certify the direction as verified. [INFERENCE]

### Fix

Changed the claims-table row from `MODERATE | VERIFIED (direction), not fully analyzed` to `LOW-MODERATE | PRELIMINARY — fetched but not fully analyzed`, and added a memo revision row. [SOURCE: memo]

### Updated conclusion

The U.S. crime-rate conclusion remains unchanged. The international caveat is now properly provisional until the European paper is read and source-graded. [INFERENCE]

---

## 2026-06-16 — QWI table wording changed from confirmatory to margin-specific

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` still said the Saiz/QWI cycle "confirms wage channel is small" in the local-burden summary table. That phrase was too broad even though the same memo elsewhere bounded the E-Verify design. [DATA]

### Why it was wrong

QWI state-panel evidence supports a small/null wage response in the observed E-Verify mandate margin. It does not confirm that every wage channel is small across surge inflows, mass deportation, cash-economy sectors, within-state heterogeneity, or longer-run adjustment. The table row should not be broader than the tested design. [INFERENCE]

### Fix

Changed the row to say QWI supports a small/null wage response in the observed E-Verify margin, and added a synthesis revision row. [SOURCE: memo]

### Updated conclusion

The synthesis still treats the wage channel as weak in the tested E-Verify design, while preserving the open questions for untested shock regimes and other labor-market margins. [INFERENCE]

---

## 2026-06-16 — E-Verify verdict sentence narrowed to large-gain margin

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` still said "the Borjas wage prediction is rejected at conventional significance levels." That sentence remained broader than the table and ladder wording fixed earlier in the same memo. [DATA]

### Why it was wrong

The E-Verify TWFE result is strong against large Borjas-style native wage gains from E-Verify-style labor-supply contraction. It is not a rejection of the full Borjas wage-prediction family across Mariel-style composition shocks, surge regimes, mass deportation, cash-economy sectors, or longer-run adjustment. This was an external-validity weak link: design margin -> claim family. [INFERENCE]

### Fix

Replaced the broad verdict with the narrower claim that large Borjas-style native wage gains from E-Verify-style labor-supply contraction are rejected at conventional significance levels, and added a synthesis revision row. [SOURCE: memo]

### Updated conclusion

The causal synthesis is now consistent across table, ladder block, and verdict paragraph: strong against high-end Borjas magnitudes in the observed E-Verify margin, not a global labor-substitution verdict. [INFERENCE]

---

## 2026-06-16 — Mexico +$46k all-in row changed from falsified to unsupported

### Issue

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md` labeled the hypothesis `+$46k = immigrant pays for themselves all-in` as **Falsified** because school, admin, courts, and shelter were not netted into the warehouse layer. [DATA]

### Why it was wrong

Missing ledgers block the all-in inference, but they do not by themselves prove the all-in sign is negative or that the immigrant fails to pay for themselves after all offsets are modeled. This is an inference-validity problem, not a falsified empirical proposition. The correct claim is narrower: `+$46k` is not a valid all-in export from the synthetic NAS age-25 benchmark. [INFERENCE]

### Fix

Changed the row to `Unsupported / not a valid export — school, admin, courts, shelter not netted` and added a memo revision row. [SOURCE: memo]

### Updated conclusion

The memo still blocks scalar laundering of the `+$46k` benchmark into an all-in fiscal verdict, but it no longer overclaims that the full all-in sign has been falsified. [INFERENCE]

---

## 2026-06-16 — Restrictionist steel-man aligned on Mexico +$46k export

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still summarized `+$46k Mexico = net contributor all-in` as **False** because admin, courts, and full local layers were missing. That conflicted with the corrected Mexico NPV memo, which now treats the export as unsupported rather than empirically falsified. [DATA]

### Why it was wrong

The restrictionist steel-man should not turn an omitted-ledger critique into a completed negative all-in verdict. Missing admin, court, school, and shelter layers invalidate the scalar export; they do not by themselves measure the all-in sign. [INFERENCE]

### Fix

Changed the disconfirmation row to `Unsupported / invalid scalar export` and added a memo revision row. [SOURCE: memo]

### Updated conclusion

Both memos now carry the same inference boundary: the `+$46k` benchmark cannot be quoted as all-in net contribution, but the full stacked sign remains an open modeling question. [INFERENCE]

---

## 2026-06-16 — Borjas Mariel wording changed from replication to generalization

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` described Borjas's restricted-Mariel reanalysis as a finding that "does not replicate in broader staggered designs." [DATA]

### Why it was wrong

E-Verify TWFE and Foged-Peri refugee-assignment evidence are not direct replications of the Mariel reanalysis. They are adjacent external-validity tests of whether large Borjas-style native low-skill wage losses/gains appear in other quasi-experimental designs. Calling that "replication" overstates the methodological relationship. [INFERENCE]

### Fix

Changed the sentence to "does not generalize to the broader staggered designs tested here" and added a synthesis revision row. [SOURCE: memo]

### Updated conclusion

The wage synthesis now distinguishes direct replication from external-validity evidence: Borjas's restricted-Mariel estimate remains a contested Mariel result, while the repo's newer designs cut against extrapolating that magnitude to observed E-Verify-style policy variation. [INFERENCE]

---

## 2026-06-16 — Mexico surge row scoped to unauthorized-stock growth

### Issue

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md` said "Mexico drove surge" was **Falsified** because Mexico unauthorized stock was flat, and its Biden-stock section said "surge was non-Mexico." [DATA]

### Why it was wrong

The evidence cited there is a stock ledger: Mexico unauthorized population was roughly flat while the post-2021 unauthorized-stock increase came from non-Mexico origins. That does not adjudicate every surge metric. Encounter events, lawful/parole flows, receiver-city shelter load, and local operational pressure are different ledgers. Flat Mexico unauthorized stock falsifies a Mexico-driven unauthorized-stock-growth claim, not the broader phrase "Mexico drove surge." [INFERENCE]

### Fix

Changed the Biden-stock bullet to say post-2021 unauthorized-stock growth was non-Mexico on this ledger, and changed the disconfirmation row to `Mexico drove post-2021 unauthorized-stock growth | Falsified on this stock ledger`. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The Mexico memo still blocks the "10M+ new Mexican unauthorized residents" style claim, but it no longer overextends a stock finding to all encounter, flow, or receiver-load surge interpretations. [INFERENCE]

---

## 2026-06-16 — Steel-man Mexico +$46k line scoped to `<HS` export

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` said "Mexico +$46k mix kills monolithic 'Mexican drain'." After the Mexico NPV memo was corrected, that wording was too strong. [DATA]

### Why it was wrong

The `+$46k` figure is a synthetic NAS age-25 education-mix benchmark. It blocks the restrictionist move of applying the NAS `<HS` cell to all Mexico-origin adults, because the observed education mix includes HS, some-college, and BA+ cells. But it does not kill every possible full-ledger Mexico-origin drain claim once school, state/local, admin, court, legal-status, and episodic shelter layers are modeled. [INFERENCE]

### Fix

Changed the line to say the benchmark blocks `<HS`-only "Mexican drain" exports, but is not an all-in origin scalar. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The steel-man now preserves both sides of the correction: restrictionists cannot launder a low-education NAS cell into "all Mexicans," and expansionists cannot launder the `+$46k` benchmark into an all-in positive origin verdict. [INFERENCE]

---

## 2026-06-16 — GPT calibration removed from wage-evidence stack

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said three convergent tests showed no measurable native low-skill wage gains: E-Verify, sanctuary state DiD, and "GPT-5.4 calibration interpretation." Its verdict table also called the sanctuary result a "third confirmation." [DATA]

### Why it was wrong

The GPT-5.4 calibration is model-assisted parameter-sensitivity reasoning for the open-borders welfare-weight frame. It is not an empirical wage design. Counting it as a wage test inflates the evidence stack and blurs measurement with model interpretation. The wage stack should be QWI E-Verify + QWI sanctuary, read alongside external Card/Foged-Peri literature. [INFERENCE]

### Fix

Changed the sanctuary row to "additional QWI policy-margin check" and rewrote Statement 1 to say two repo QWI policy-margin tests, read alongside Card/Foged-Peri literature, support the bounded wage conclusion. Explicitly moved GPT-5.4 calibration back to the welfare-weight sensitivity frame. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The wage conclusion remains strong for the tested marginal-policy range, but the evidence count is now honest: model sensitivity is not empirical wage confirmation. [INFERENCE]

---

## 2026-06-16 — Confidence ladder stopped calling sanctuary a third wage confirmation

### Issue

`research/immigration-confidence-ladder.md` entry 21 still called the sanctuary QWI null a "Third convergent confirmation" of the Card-side wage channel after the paradigm synthesis had removed GPT-5.4 calibration from the wage-evidence stack. [DATA]

### Why it was wrong

Once model calibration is excluded, the repo has two internal QWI policy-margin wage checks in this cycle: E-Verify and sanctuary policy. External Card/Foged-Peri evidence still matters, but the ladder should not imply a third internal empirical wage design. [INFERENCE]

### Fix

Changed entry 21 to "strong null result in this design" and described it as an additional QWI policy-margin check consistent with E-Verify, bounded to observed marginal policy variation. [SOURCE: memo]

### Updated conclusion

The wage conclusion is unchanged, but its evidence count is no longer inflated. [INFERENCE]

---

## 2026-06-16 — Foged-Peri design label downgraded from random assignment

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` said Foged-Peri native wages rose under "random refugee assignment," and `research/immigration-causal-everify-card-vs-borjas.md` used the opaque design label "RA quasi-IV." [DATA]

### Why it was wrong

The Foged-Peri design is strong, but not a simple randomized trial. The paper describes a Danish refugee dispersal policy that allocated refugees using nationality, family size, housing availability, and clustering goals; identification comes from quasi-experimental dispersal unrelated to local labor demand plus later refugee-country inflows. Calling it merely "random assignment" overstates the design and hides the IV/DiD structure. [SOURCE: /Volumes/2TBPNY/research-data/immigration-fiscal/data/external/lifetime/nber/foged_peri_2016_immigrants_effect_native_workers_w19315.pdf] [INFERENCE]

### Fix

Changed the synthesis wording to "refugee dispersal-policy quasi-experiment" and changed the comparison-table design label to "Dispersal-policy IV / DiD." Added revision rows to both memos. [SOURCE: memo]

### Updated conclusion

Foged-Peri remains useful external evidence against large native low-skill wage losses in that Danish setting, but the repo should export it as quasi-experimental dispersal evidence, not as RCT-style random assignment. [INFERENCE]

---

## 2026-06-16 — Residual wage replication language narrowed

### Issue

After the first Mariel/generalization fix, several wage memos still said this cycle "replicates" Card/Foged-Peri/Card-Peri/Orrenius-Zavodny patterns or that the sanctuary design "replicates E-Verify margin." [DATA]

### Why it was wrong

Those are not direct replications of the same estimands, populations, data, or designs. They are convergent or consistency checks: QWI E-Verify and QWI sanctuary policy margins line up with the Card-side literature, while Foged-Peri is a distinct Danish dispersal-policy design. [INFERENCE]

### Fix

Changed the causal synthesis, E-Verify memo, and paradigm synthesis to use "convergent," "consistent with," "extends," and "aligned with" instead of replication language. Added revision rows in the affected memos. [SOURCE: memo]

### Updated conclusion

The Card-side wage reading is still supported for observed marginal-policy designs, but the repo no longer claims direct replication where it only has adjacent evidence. [INFERENCE]

---

## 2026-06-16 — First causal synthesis stopped treating welfare weight as fully non-empirical

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` said the Clemens place-premium / immigrant-welfare-weight lever was "a values choice, not an empirical question" and that no amount of additional data could resolve it. [DATA]

### Why it was wrong

The welfare weight itself is normative, but the place-premium, native-cost, fiscal, housing/capacity, and sending-country inputs are empirical. Evidence cannot choose the moral weight, but it can move scenario break-evens under any chosen weight. [INFERENCE]

### Fix

Changed the honest-reflection paragraph to separate the normative welfare weight from empirical inputs, and added a revision row to the first causal synthesis. [SOURCE: memo]

### Updated conclusion

The initial synthesis now matches the corrected paradigm memo: state the welfare-weight assumption, but keep collecting and grading the non-weight inputs. [INFERENCE]

---

## 2026-06-16 — Caplan global-gains verdict bounded to direction

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` already said the economic case mostly survives in direction rather than strongest magnitude, but its bottom-line score still said Caplan was simply "strong on global gains" and "wins on migrant welfare and global gains." [DATA]

### Why it was wrong

That shorthand could be read as endorsing the strongest open-borders magnitude or as closing destination-capacity concerns. The memo's own evidence supports a narrower claim: migrant-welfare direction and large global-gains sign survive, while realistic volume, housing, congestion, and political constraints bound magnitude and destination-country incidence. [INFERENCE]

### Fix

Changed the clean verdict and net-summary bullet to say Caplan wins on migrant-welfare direction and large global-gains sign, not strongest magnitude or destination-capacity closure. Added a revision section to the Caplan audit. [SOURCE: memo]

### Updated conclusion

The Caplan audit now keeps its pro-open-borders credit without laundering sign evidence into an unconstrained magnitude/capacity verdict. [INFERENCE]

---

## 2026-06-16 — Capacity frontier native-sorting sentence made descriptive

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` said the load-capacity decile table was a direct answer to the destination-country question because "once immigrant inflow materially outruns local build response, domestic incumbents sort away more aggressively." [DATA]

### Why it was wrong

The decile evidence is a county association: high load-capacity deciles show more negative domestic net migration. It does not by itself identify whether immigrant load caused incumbents to leave, whether destination selection drives both variables, or whether unmodeled local shocks explain part of the pattern. [INFERENCE]

### Fix

Changed the sentence to call the decile table a descriptive screen and state that causal incumbent-exit interpretation still needs counterfactual identification. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The capacity memo still shows a useful load-capacity/native-migration association, but it no longer exports the association as a causal sorting mechanism. [INFERENCE]

---

## 2026-06-16 — Surge ladder stopped endorsing decisive Card-side phrasing

### Issue

`research/immigration-causal-surge-2021-2024.md` and confidence-ladder entry 29 said prior entries claimed a "decisive Card-side win for U.S. policy variation" and then treated that as true for 2008-2021 variation. [DATA]

### Why it was wrong

The static-cycle wage work supports a bounded Card-side reading for observed E-Verify/sanctuary-style marginal policy variation. Calling it "decisive" for U.S. policy variation over-compresses the external-validity boundary and conflicts with later caveats around surge and mass-shock regimes. [INFERENCE]

### Fix

Rewrote entry 29 in both the surge memo and standalone confidence ladder to say the prior phrasing was overcompressed and that the safer reading is strong Card-side evidence for observed 2008-2021 marginal policy variation. Added a surge memo revision row. [SOURCE: memo]

### Updated conclusion

The surge memo still marks 2021-2024 as outside the static-cycle wage variation, but it no longer endorses the static-cycle result as a decisive general U.S. policy verdict. [INFERENCE]

---

## 2026-06-16 — CHNV superseded ladder entries marked invalid, not just superseded

### Issue

`research/immigration-confidence-ladder.md` entries 26 and 30 still carried the old CHNV "did not substitute / added on top" conclusion. Entry 30 even said the descriptive fact survived and "substitution did not happen," despite entry 34 reversing that reading after the OHSS parser correction. [DATA]

### Why it was wrong

The corrected USBP/OFO split changed the descriptive sign: CHNV substituted lawful port flow for irregular between-port crossings in its initial year, even though total lawful parole inflow still landed in receiver-city ledgers. A mere "superseded" label left too much room to quote the old conclusion as a weaker live claim. [SOURCE: decisions/2026-06-11-ohss-date-universe-bugs-chnv-reversal.md] [INFERENCE]

### Fix

Marked entries 26 and 30 as invalidated/historical-only, and rewrote entry 30's reason to say the old `+787%` figure is an error trace from the lawful OFO channel on a scrambled clock. [SOURCE: memo]

### Updated conclusion

The standalone ladder now exports only entry 34 for CHNV: channel substitution occurred initially for USBP between-port crossings, while total lawful parole inflow remains a receiver-load ledger. [INFERENCE]

---

## 2026-06-16 — Lott crime critique downgraded from verified flaw to supported critique

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` rated the claim that Lott's Arizona study had a "fundamental data classification flaw" as `HIGH` and `VERIFIED`. The memo cited Cato, Washington Post, and Latino Decisions critiques, but did not itself reanalyze the Arizona DOC data. [DATA]

### Why it was wrong

Multiple independent critiques are enough to mark Lott as an unresolved outlier and weak source, but they are not the same thing as an independent verification of the underlying classification error. The status label should distinguish "supported critique" from "verified by our own reanalysis." [INFERENCE]

### Fix

Changed the assessment wording from "shown to be unreliable" to "seriously challenged," and changed the claims-table row to `MODERATE-HIGH` / `SUPPORTED CRITIQUE — not independent reanalysis`. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The crime memo still treats Lott as an outlier whose central data issue is unresolved, but it no longer overstates the memo's own evidentiary posture against the contrarian study. [INFERENCE]

---

## 2026-06-16 — NH-white fiscal ratios aligned to tensor anchor

### Issue

`research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md` still listed NH-white-all federal annual as `$2,803–3,005`, and `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md` still listed headline ratios `nh_white_all/fb_lt_hs ~4.4x`, `nh_white_all/mexico_origin ~2.0x`, and `nh_white_fborn/nh_white_usborn ~1.5x`. [DATA]

### Why it was wrong

The current tensor export gives `nh_white_all` federal annual `2802.7`, `fb_lt_hs` `676.8`, `mexico_origin` `1519.3`, `nh_white_fborn` `3897.6`, and `nh_white_usborn` `2746.3`. Those imply roughly `4.1x`, `1.8x`, and `1.4x`, respectively. Keeping stale rounded ratios overstates the white-vs-Mexico and white-vs-low-skill gaps. [SOURCE: infra/immigration-fiscal/build/stage3_proto/country_fiscal_rollup_2023.csv] [DATA]

### Fix

Replaced the stale NH-white-all range with `$2,803` and aligned the brainstorm ratios to the current tensor export. Added revision rows to both affected memos. [SOURCE: memo]

### Updated conclusion

The corridor story remains the same, but the numeric headline is tighter: the current narrow federal proxy shows about `1.8x` NH-white-all/Mexico and about `4.1x` NH-white-all/FB-`<HS`, not the older larger rounded ratios. [DATA]

---

## 2026-06-16 — Open-borders weight framing separated from empirical inputs

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and confidence-ladder entry 23 described the open-borders verdict as "welfare-weight-determined, not data-determined" and said the repo could not resolve it empirically. That phrasing risked treating model cost/capacity inputs as settled merely because the welfare weight itself is normative. [DATA]

### Why it was wrong

The welfare weight assigned to immigrants is a value choice. But scenario costs, fiscal ledgers, housing/capacity constraints, labor-market adjustment, and sending-country effects are empirical inputs. New evidence cannot pick the moral weight, but it can move the break-even thresholds under any chosen weight. [INFERENCE]

### Fix

Reframed the paradigm synthesis and embedded ladder text around a normative weight plus empirical inputs, annotated confidence-ladder entry 23 as qualified, and added entry 39 with the corrected reading. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The open-borders conclusion still must state its welfare-weight assumption, but the repo should keep collecting and grading cost/feasibility evidence rather than treating the scenario as fully non-empirical. [INFERENCE]

---

## 2026-06-16 — Second-generation crime row scoped to broad literature pattern

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` rated "second-generation immigrants have higher crime rates..." as `HIGH` / `VERIFIED`. [DATA]

### Why it was wrong

The memo cites broad generational immigration-crime literature for that row. It is not an unauthorized-only, current-surge, or source-read-fresh estimate, so it should not carry the same status as the Texas DPS/PNAS administrative rows. [INFERENCE]

### Fix

Changed the paragraph and claims-table row to a scope-limited supported literature pattern with `MODERATE` confidence. Added a revision row to the memo. [SOURCE: memo]

### Updated conclusion

The crime memo can still flag generational convergence as a caveat, but not as a high-certainty claim about unauthorized immigrants or the 2021-2024 cohort. [INFERENCE]

---

## 2026-06-16 — Residual replication labels narrowed to consistency checks

### Issue

Two tracked memos still used "replication" language for checks that were not direct replications: `immigration-causal-saiz-elasticity-rent.md` said the 2022 cross-section "replicates Saiz's own pattern," and `immigration-confidence-ladder.md` said the E-Verify QWI result "Replicates Card direction." A receiver-city ladder entry also called a Hispanic-share control a "Replication gate." [DATA]

### Why it was wrong

The Saiz pass is a 2022 descriptive cross-section, not Saiz's 1980-2000 panel/IV design. The E-Verify result is an adjacent QWI policy-margin check that aligns with Card-side direction, not a direct Card replication. The receiver-city Hispanic-share pass is a robustness gate against a named confounder, not a replication. [INFERENCE]

### Fix

Changed the Saiz memo to "consistent with the Saiz elasticity/rent mechanism," changed the E-Verify ladder line to "Aligns with Card direction; not a direct replication," and renamed the receiver-city phrase to "Hispanic-share robustness gate passed." Added a Saiz memo revision row. [SOURCE: memo]

### Updated conclusion

The affected claims remain useful consistency or robustness evidence, but the repo no longer exports them as direct replications. [INFERENCE]

---

## 2026-06-16 — Capacity-frontier causal verbs made descriptive

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` had a scope note saying `HIGH`/`VERIFIED` referred to reproducible model-output patterns rather than causal identification, but the claims table still said wage growth "responds" to load-capacity and native net migration "becomes" more negative as load-capacity rises. The wage section also called the row the "clearest county confirmation" of the worker question. [DATA]

### Why it was wrong

Those phrases made the descriptive county models sound like response or mechanism estimates. The listed artifacts verify coefficient patterns, not the counterfactual effect of immigrant load on wages, employment, or native sorting. [INFERENCE]

### Fix

Changed the wage row to model-loading language, changed the native-migration row to a decile association, and replaced "confirmation" with "descriptive evidence." Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The capacity-frontier memo still supports load-capacity as the cleaner county stress screen, but it no longer overstates the table rows as causal response estimates. [INFERENCE]

---

## 2026-06-16 — Standalone E-Verify ladder row aligned to bounded margin

### Issue

`research/immigration-confidence-ladder.md` entry 17 still rated the E-Verify/Borjas wage result as `strong rejection`, even though the source memo and causal synthesis had already narrowed the result to large Borjas-style native wage gains in the observed E-Verify mandate margin. [DATA]

### Why it was wrong

The QWI design can reject high-end native wage gains for the tested E-Verify policy variation. It does not reject every Borjas-style labor-substitution claim, surge regime, mass-deportation shock, cash-economy margin, or longer-run adjustment channel. [INFERENCE]

### Fix

Renamed the ladder row to "Large Borjas-style native wage gains under observed E-Verify mandates," changed the rating to `strong against large gains in this design`, and made the reason explicitly margin-specific. [SOURCE: memo]

### Updated conclusion

The ladder now matches the source memos: strong Card-side evidence for the tested E-Verify margin, not a global wage-family rejection. [INFERENCE]

---

## 2026-06-16 — Caplan crime shorthand scoped to observed justice-system rates

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` correctly bounded the crime row in its executive table and caveats, but its shorthand verdict still said `strong on crime skepticism`, `crime skepticism`, and `Caplan wins on crime`. [DATA]

### Why it was wrong

The crime memo's corrected estimand is observed U.S. arrest, conviction, incarceration, and institutionalization rates for first-generation / unauthorized immigrants. It is not directly observed true offending, not international evidence, and not a current-surge subgroup estimate. The shorthand needed to carry the same scope as the body. [INFERENCE]

### Fix

Changed the shorthand verdicts to observed U.S. justice-system-rate skepticism and added a Caplan-audit revision row. [SOURCE: memo]

### Updated conclusion

Caplan remains strongest on the U.S. crime-objection lane, but only for the observed justice-system-rate claim already defended in the crime memo. [INFERENCE]

---

## 2026-06-16 — FAIR taxpayer-drain line marked as conditional claim

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` had already renamed FAIR as an advocacy high-cost ledger, but the F2 argument chain still said "Policy implication: Massive net drain; every taxpayer ~$956-1,156/yr" without marking that line as FAIR's implication rather than the repo's conclusion. [DATA]

### Why it was wrong

The number comes from FAIR's contested ledger. It can be preserved as part of the restrictionist steel-man, but it should not read like a validated taxpayer-incidence estimate until FAIR/ITEP/Pew stock, child-attribution, household-benefit, and cost-allocation choices are reconciled. [INFERENCE]

### Fix

Changed the line to "Policy implication [FAIR claim, conditional on its contested ledger]" and added a memo revision row. [SOURCE: memo]

### Updated conclusion

The steel-man still records FAIR's full-budget argument, but the taxpayer-drain implication is now explicitly conditional on FAIR's construction. [INFERENCE]

---

## 2026-06-16 — Steel-man crime-wave row scoped to observed-rate evidence

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` summarized "Crime wave from unauthorized" as `Mostly false — repo crime memo`. [DATA]

### Why it was wrong

The repo crime memo now supports a narrower claim: observed U.S. justice-system rates for first-generation / unauthorized immigrants are lower in the best current evidence. It does not directly measure true offending, all international contexts, or every current-surge subgroup. [INFERENCE]

### Fix

Changed the disconfirmation row to `Unsupported by observed U.S. justice-system-rate evidence` and added the true-offending/current-surge scope caveat. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The steel-man still rejects the simple unauthorized-crime-wave claim, but on the correct observed-rate evidence surface rather than a broader true-crime assertion. [INFERENCE]

---

## 2026-06-16 — Receiver-election exposure wording narrowed to indicators

### Issue

`research/immigration-causal-surge-2021-2024.md` still titled the election section "2024 election shift x surge exposure" and said the shift was correlated with "receiver-city / border-surge exposure." [DATA]

### Why it was wrong

The memo's verified object is a county screen using receiver-city and border/high-immigration indicators, plus foreign-born share and recent foreign-born inflow controls. It does not measure an exposure dose, identify causal voter response to the surge, or decompose border counties from broader Hispanic realignment and local political trends. [INFERENCE]

### Fix

Renamed the section to receiver/border indicators, changed the interpretation paragraph to describe indicator associations, and removed "handling the surge directly" / "absorbing current inflow" language. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The receiver-election result remains a bounded correlational signal: receiver-city status is associated with about +2.4pp GOP shift after controls, but it is not a measured surge-exposure effect. [INFERENCE]

---

## 2026-06-16 — Saiz housing language narrowed to renter incidence

### Issue

Several active Saiz/housing summaries still said rent exposure was "closer to welfare loss" than the adversarial review allowed. The source Saiz memo, the causal synthesis embedded ladder, the paradigm synthesis verdict table, and confidence-ladder entry 18 all carried some version of that shorthand. [DATA]

### Why it was wrong

The Saiz evidence supports an elasticity-conditional renter-incidence warning: immigrants are concentrated in inelastic/high-rent MSAs, so rent exposure is more decision-relevant for renters than a raw price-level measure. But aggregate welfare loss still requires causal identification of immigrant-specific rent effects plus owner/renter incidence and tax-base offsets. [INFERENCE]

### Fix

Replaced the residual "closer to welfare loss" phrasing with "stronger renter-incidence warning" in the source Saiz memo, the causal synthesis, the paradigm synthesis, and confidence-ladder entry 18. Added revision rows where those memos keep revision tables. [SOURCE: memo]

### Updated conclusion

The housing layer remains a real local-incidence warning, especially in inelastic destinations, but it is no longer exported as an aggregate welfare-loss claim. [INFERENCE]

---

## 2026-06-16 — Card-side wage labels softened from wins to favored

### Issue

Active synthesis and ladder text still used "Card-side pattern wins" / "Card-wins" after earlier fixes had bounded the result to observed marginal enforcement variation. [DATA]

### Why it was wrong

"Wins" language suggests debate closure. The evidence is strong against large Borjas-style native wage gains in the tested E-Verify/sanctuary-style margins, but surge, mass-shock, cash-economy, and longer-run channels remain open. [INFERENCE]

### Fix

Replaced active "wins" labels with "Card-side pattern is favored" or "Card-side wage finding is bounded" in the causal synthesis, paradigm synthesis, surge memo embedded ladder, and standalone confidence ladder. [SOURCE: memo]

### Updated conclusion

The Card-side wage reading remains strong for observed marginal enforcement designs, but the repo no longer labels the bounded comparison as a global win. [INFERENCE]

---

## 2026-06-16 — Clark economist correctness language narrowed to channel support

### Issue

The E-Verify memo and causal synthesis still said the Clark "agree" economists were "correct" or "right" on the wage channel after the underlying findings had been bounded to observed marginal policy variation. [DATA]

### Why it was wrong

The source Clark audit treated the strongest agree responses as mostly right only if read as small native-wage-effect or complementarity claims, and explicitly rejected the idea that the poll settled the full welfare/local-capacity question. The E-Verify design supports that narrow premise; it does not adjudicate the economists' broader survey answers or every wage regime. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] [INFERENCE]

### Fix

Replaced "right/correct" language with support for the small-native-wage-effect premise in the observed E-Verify / marginal-policy wage channel. [SOURCE: memo]

### Updated conclusion

The Clark-side wage premise is stronger than the repo initially allowed for observed marginal enforcement variation, but the repo no longer calls the economists globally right even on a compressed "wage channel" label. [INFERENCE]

---

## 2026-06-16 — Capacity frontier settling language narrowed to descriptive updates

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` still said earlier county passes "established" the relevant variables and titled its final synthesis "What this settles, and what it does not." [DATA]

### Why it was wrong

The memo's own scope note says `HIGH` and `VERIFIED` refer to reproducible model-output patterns, not clean causal effects. County capacity regressions can sharpen descriptive stress objects and research priorities, but they do not settle the local-incidence causal graph. [SOURCE: memo] [INFERENCE]

### Fix

Changed "established" to "suggested," retitled the final section as "What this updates, and what it does not settle," and changed "real residual signal" to "model residual signal." [SOURCE: memo]

### Updated conclusion

The capacity-frontier memo now exports descriptive model-output updates rather than settled causal conclusions about flow/capacity thresholds. [INFERENCE]

---

## 2026-06-16 — Restrictionist steel-man binary verdict softened

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` summarized the steel-man as "restrictionists are right on layer multiplication, wrong on single-scalar panic." [DATA]

### Why it was wrong

The memo is a steel-man of claim structure, not a final side-taking verdict. The evidence supports the restrictionist insight that fiscal, local, legal-status, cohort, and service-capacity layers can diverge, but the "right/wrong" formulation over-compressed a mixed evidentiary map into a binary judgment. [INFERENCE]

### Fix

Changed the synthesis to say the restrictionist case is best supported on layer multiplication and weakest when those layers collapse into single-scalar panic. [SOURCE: memo]

### Updated conclusion

The steel-man keeps its strongest mechanism without presenting restrictionism as simply right or wrong in aggregate. [INFERENCE]

---

## 2026-06-16 — Caplan verdict labels changed from wins/loses to strength lanes

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` still used active verdict labels like "mostly right on the sign," "partly right on one channel," and "Caplan wins/loses" in the net summary. [DATA]

### Why it was wrong

The supporting evidence in the memo is lane-specific: global migrant-welfare direction, observed-rate crime skepticism, labor-market caveats, and destination-capacity/political-incidence failures. Binary win/loss language hides that decomposition and invites copying the shorthand without the scoped claims. [INFERENCE]

### Fix

Replaced the residual verdict labels with direction/sign survives, partly supported, strongest/weakest lane language, while preserving the same substantive ranking. [SOURCE: memo]

### Updated conclusion

The Caplan audit now reads as a lane-by-lane support map rather than a debate scorecard. [INFERENCE]

---

## 2026-06-16 — Caplan right-label residue narrowed

### Issue

After the broader Caplan verdict cleanup, the audit still used "Caplan is right" labels in the global-gains, worker-protection, fiscal-ledger, and causal-graph sections. [DATA]

### Why it was wrong

The source evidence is lane-specific and asymmetric: place-premium scale survives, ledger-blurring criticism survives in some fiscal arguments, broad employment-collapse rhetoric is unsupported, and constrained-place wage pressure remains live. Calling Caplan "right" compresses those separable claims with unresolved destination-incidence lanes. [SOURCE: memo] [INFERENCE]

### Fix

Changed the surviving points to claim-support language: place-premium scale, ledger-blurring criticism, unsupported collapse rhetoric, and "where Caplan's case is supported" DAG framing. [SOURCE: memo]

### Updated conclusion

The Caplan audit now separates supported objections from unresolved destination-incidence concerns without relying on "Caplan is right" shorthand. [INFERENCE]

---

## 2026-06-16 — School burden denominator fix scoped to narrow export

### Issue

`research/immigration-school-burden-per-adult-2026-06-15.md` said the corrected denominator "kills the stale claim" that the built annual school layer alone overwhelms Mexico's federal proxy. [DATA]

### Why it was wrong

The correction is real, but its scope is a specific annual school-burden export under the corrected full Mexico adult denominator. "Kills" can be copied as if the broader school-cost or all-government fiscal claim family had been falsified. The memo itself says lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers remain separate. [SOURCE: memo] [INFERENCE]

### Fix

Replaced "kills" with "invalidates the stale narrow export" and named the corrected adult denominator as the reason. [SOURCE: memo]

### Updated conclusion

The school-burden memo now says the corrected denominator blocks one narrow annual-school-layer export, without implying that broader fiscal or school-burden questions are settled. [INFERENCE]

---

## 2026-06-16 — E-Verify adjustment mechanism made unresolved

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` inferred that E-Verify produced employer adjustment through capital, automation, relocation, cash-economy hiring, outsourcing, and similar channels after observing lower QWI E1 employment and flat wages. [DATA]

### Why it was wrong

The QWI design observes stable W-2 employment and earnings cells. It can support the pattern "QWI E1 employment fell while wages did not rise" in the tested state mandate design, but it does not directly measure true labor-supply contraction, capital substitution, firm exit, relocation, cash-economy movement, hours, occupation, or establishment-composition shifts. The weak link was mechanism attribution from a reduced-form wage/employment pattern. [SOURCE: memo] [INFERENCE]

### Fix

Replaced mechanism-identifying language with a bounded interpretation: the large native wage-bidding channel is not observed in this design; the listed adjustment channels are candidate hypotheses, not measured mechanisms. [SOURCE: memo]

### Updated conclusion

The E-Verify result remains evidence against large native wage gains in the observed mandate margin, but the mechanism absorbing the shock is unresolved. [INFERENCE]

---

## 2026-06-16 — E-Verify supply-contraction wording narrowed to measured design

### Issue

The E-Verify source memo and causal synthesis still exported the design as "removing/restricting unauthorized labor" or "E-Verify contracts unauthorized labor supply." [DATA]

### Why it was wrong

The design observes state E-Verify mandate timing, QWI stable W-2 employment, and QWI earnings. It does not directly observe total unauthorized labor supply, off-W-2 work, compliance intensity, or cross-state reallocation. Treating mandate variation as measured labor-supply contraction overstates the data surface. [SOURCE: memo] [INFERENCE]

### Fix

Replaced those exports with "observed E-Verify mandate variation" and QWI wage language in the E-Verify memo and causal synthesis. [SOURCE: memo]

### Updated conclusion

The result remains strong against large native wage gains in observed E-Verify mandate designs, but it no longer implies that total unauthorized labor supply contraction was directly measured. [INFERENCE]

---

## 2026-06-16 — Europe/Caucasian fiscal comparison kept on proxy surface

### Issue

`research/immigration-europe-caucasian-fiscal-findings-2026-06-15.md` said EU27 foreign-born "beat" native Caucasians, that foreign-born whites "raise the Caucasian average," and listed positive-selection mechanisms as if the table decomposed them. [DATA]

### Why it was wrong

The memo's ledger is a narrow federal annual proxy: payroll/FICA minus SNAP, TANF, and SSI. It does not measure full federal taxes, state/local services, lifetime NPV, visa path, age-at-arrival, English proficiency, or cohort timing. The table can show a higher proxy value for EU27/NH-white-FB groups; it cannot by itself prove the selection mechanism or a broad fiscal superiority claim. [SOURCE: memo] [INFERENCE]

### Fix

Replaced "beat"/"raise average" with narrow federal-proxy comparison language, and changed mechanism wording to "consistent with positive selection" while naming unmeasured channels. [SOURCE: memo]

### Updated conclusion

The Europe/Caucasian memo still supports a corridor-selection screen on the federal proxy, but no longer exports that screen as a broad fiscal verdict or measured selection mechanism. [INFERENCE]

---

## 2026-06-16 — Sanctuary wage null phrasing changed to non-significance

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and confidence-ladder entry 21 called the sanctuary QWI wage result a "STRONG null result" and said policy variation "does not change" native low-skill wages either direction. [DATA]

### Why it was wrong

The cited evidence is that all E1 specifications had `|t|<1.0` in the TWFE design. That is a non-significance statement, not an equivalence test proving a zero effect or bounding all practically meaningful effects. The result still aligns with the bounded Card-side reading, but the statistical claim should not exceed "no statistically significant E1 wage change observed." [SOURCE: memo] [INFERENCE]

### Fix

Changed the active paradigm synthesis row, embedded ladder snippet, and standalone confidence-ladder entry to say no statistically significant E1 wage change was observed, and added that equivalence was not tested. [SOURCE: memo]

### Updated conclusion

The sanctuary QWI pass remains a useful policy-margin check against obvious large wage movement, but the repo no longer treats non-significance as a proven strong null. [INFERENCE]

---

## 2026-06-16 — Confidence ladder Saiz zoning entry made descriptive

### Issue

`research/immigration-confidence-ladder.md` entry 20 still said the inelastic-MSA immigrant concentration was "driven by zoning, not topography" and exported zoning reform as a viable lever, even though entry 38 later qualified the result. [DATA]

### Why it was wrong

The Saiz decomposition is a cross-sectional regression where WRLURI is a stronger correlate than topographic unavailability. It does not identify causal direction or prove that zoning reform would reduce immigrant renter burden. Leaving the old causal wording in entry 20 created a grep hazard despite the later qualifier. [SOURCE: memo] [INFERENCE]

### Fix

Replaced entry 20's title, rating, and reason with stronger-correlate/descriptive wording and recast zoning reform as a plausible hypothesis rather than a verified causal lever. [SOURCE: memo]

### Updated conclusion

The confidence ladder now treats the Saiz regulatory result as descriptive evidence for a zoning hypothesis, not as proof that zoning caused immigrant concentration or solves renter incidence. [INFERENCE]

---

## 2026-06-16 — E-Verify wage shorthand changed to statistical non-significance

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` and `research/immigration-causal-synthesis-2026-04-18.md` still used shortcuts like "wages did not rise" and "does not raise native wages" for the E-Verify QWI wage result. [DATA]

### Why it was wrong

The memo's own power caveat says the design rejects large Borjas-style gains for the observed mandate margin but cannot reject small positive effects. The shortcut wording could be reused as an exact-zero or equivalence claim rather than a no-statistically-significant-positive-effect finding. [SOURCE: memo] [INFERENCE]

### Fix

Changed the active E-Verify bullet and synthesis table rows to "no statistically significant positive QWI wage effect" while preserving the existing large-gain rejection and observed-mandate scope. [SOURCE: memo]

### Updated conclusion

The E-Verify wage evidence remains strong against large native wage gains in the tested QWI mandate design, but the repo no longer phrases the result as if it proves wages literally did not rise or could not rise by a small amount. [INFERENCE]

---

## 2026-06-16 — Restrictionist steel-man verdict residue removed

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` still opened with "restrictionists are often right" / "often wrong" verdict language even though the revision log said the binary right/wrong synthesis had been replaced. [DATA]

### Why it was wrong

The memo is a steel-man and layer map, not a side-scoring artifact. The evidence supports some restrictionist claims about omitted layers and weakens some scalar shortcuts, but a right/wrong verdict compresses distinct labor, fiscal, local-capacity, crime, and status claims into a side label. [SOURCE: memo] [INFERENCE]

### Fix

Replaced the active verdict with synthesis language about strongest and weakest claim forms, and renamed the labor-market section header from "What restrictionists get right" to "Supported restrictionist insight." [SOURCE: memo]

### Updated conclusion

The steel-man now evaluates claim structure without presenting restrictionism as a binary winner or loser in aggregate. [INFERENCE]

---

## 2026-06-16 — E-Verify Card-vs-Borjas title scoped to wage channel

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` was titled as a "Card-vs-Borjas verdict for U.S. data," and the synthesis section was headed as an "explicit verdict" even though the current evidence is an observed E-Verify/QWI wage-channel test. [DATA]

### Why it was wrong

The body already says the result is bounded to observed mandate variation and does not settle surge regimes, mass shocks, open borders, cash-economy sectors, or all wage-family claims. Title and heading text are high-reuse surfaces; if overbroad, they can undo the caveats below. [SOURCE: memo] [INFERENCE]

### Fix

Retitled the E-Verify memo as an observed wage-channel test, narrowed the question to positive QWI wage effects under state mandates, changed the synthesis heading to "E-Verify wage-channel verdict," and replaced another "wages did NOT rise" shortcut with statistical non-significance wording. [SOURCE: memo]

### Updated conclusion

The E-Verify material now presents itself as a bounded wage-channel design: strong against large Borjas-style gains in observed mandate variation, not a general Card-vs-Borjas verdict for U.S. immigration data. [INFERENCE]

---

## 2026-06-16 — Open-borders weight shorthand replaced at old claim sites

### Issue

`research/immigration-confidence-ladder.md` entry 23 and `research/immigration-causal-surge-2021-2024.md` still used "welfare-weight-determined" / "not data-determined" shorthand for the open-borders verdict, despite later corrections separating the normative weight from empirical inputs. [DATA]

### Why it was wrong

The immigrant-welfare weight is a value choice, but native-cost benchmarks, fiscal ledgers, housing/capacity constraints, and sending-country effects are empirical inputs that can move break-even thresholds. Leaving "not data-determined" at old claim sites risks turning a framing correction into a reason to stop measuring costs and feasibility. [SOURCE: memo] [INFERENCE]

### Fix

Changed confidence-ladder entry 23 to "welfare-weight-sensitive under current empirical inputs," expanded its reason to name empirical break-even inputs, and changed the surge memo heading to "welfare-weight and capacity-input components." [SOURCE: memo]

### Updated conclusion

The open-borders framing now distinguishes the non-empirical welfare-weight choice from empirical cost and capacity inputs that remain live research targets. [INFERENCE]

---

## 2026-06-16 — Title 42 surge claim narrowed to proximate timing

### Issue

`research/immigration-causal-surge-2021-2024.md` and confidence-ladder entry 35 said the Title 42 lift "did not cause the surge." The corrected event-study evidence shows a Dec-2022 local peak, April-May anticipation spike, June post-lift crash, and a lower six-month post-lift mean; it does not prove a universal zero causal effect. [DATA]

### Why it was wrong

The timing evidence refutes the prior parser-artifact story that a post-lift jump caused the surge. But event timing alone cannot exclude effects through anticipation, routing, composition, enforcement expectations, or later equilibrium channels. "Did not cause" was stronger than the identified claim. [SOURCE: memo] [INFERENCE]

### Fix

Changed the active surge memo and confidence-ladder entries to say the corrected timing does not support the Title 42 lift as the proximate surge onset, and added explicit caveats about nonzero policy effects through other channels. [SOURCE: memo]

### Updated conclusion

The repo now rejects the simple post-lift-jump causal story, while leaving other Title 42 policy-effect channels open unless separately tested. [INFERENCE]

---

## 2026-06-16 — Welfare-magnet policy implication made conditional

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` stated "Immigration + welfare expansion = fiscal unsustainability and wrong skill mix" as a policy implication in the Razin welfare-state chain. [DATA]

### Why it was wrong

The memo is mapping a restrictionist argument chain, and this channel is not modeled in the repo's DuckDB layer. Razin-style welfare-magnet models can support a conditional adverse fiscal/skill-mix equilibrium claim, but the memo had not established an unqualified finding of fiscal unsustainability. [SOURCE: memo] [INFERENCE]

### Fix

Marked the implication as a "Razin-style model claim" and reframed it as a possible adverse fiscal and skill-mix equilibrium with response margins of low-skill restrictions, benefit restrictions, or welfare-state design changes. [SOURCE: memo]

### Updated conclusion

The welfare-magnet chain remains a live restrictionist mechanism, but it is now explicitly conditional on the model rather than a repo-level fiscal-unsustainability verdict. [INFERENCE]

---

## 2026-06-16 — Newcomer denominator comparison kept off burden pressure

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` said "Most county newcomer pressure is not immigration-specific" and that the "local-burden ledger is mostly domestic-mover driven" based on the IRS domestic U.S.-origin flow versus ACS moved-from-abroad median-county comparison. [DATA]

### Why it was wrong

The comparison is a useful denominator correction: at the median county, domestic U.S.-origin mover counts are much larger than moved-from-abroad counts. But the inputs are not like-for-like burden measures, the IRS series is not native-only, and the median-county comparison does not measure concentrated receiver-node shelter, legal, language, school, or wage incidence. [SOURCE: memo] [INFERENCE]

### Fix

Replaced "pressure" and "local-burden ledger" phrasing with median-county count/denominator language in the top verdict table, Statement 2, and embedded ladder reason. [SOURCE: memo]

### Updated conclusion

The domestic-vs-abroad comparison now supports only a descriptive median-county denominator correction; it cannot dismiss immigrant-specific receiver-node burden channels without a separate incidence design. [INFERENCE]

---

## 2026-06-16 — Wage-response shorthand kept off equivalence

### Issue

`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and `research/immigration-causal-everify-card-vs-borjas.md` still used residual shorthand such as "small/null," "do not measurably respond," and "does not measurably transfer rents" for observed E-Verify/sanctuary QWI wage results. [DATA]

### Why it was wrong

The designs support no statistically significant positive QWI wage effect and reject large Borjas-style gains in the tested margins. They do not prove an equivalence-tested zero or rule out small wage effects. Shorthand like "small/null" can collapse large-gain rejection into a stronger no-effect conclusion. [SOURCE: memo] [INFERENCE]

### Fix

Replaced the active shorthand with no-statistically-significant-positive-QWI-wage-effect language, kept the large-gain rejection, and explicitly preserved small effects, employment composition, hours, occupational sorting, cash-economy, and shock-regime channels as outside the current wage result. [SOURCE: memo]

### Updated conclusion

The wage evidence now reads as a bounded statistical result: large native wage gains are not observed in the tested QWI policy margins, but small or unmeasured labor-market effects remain open. [INFERENCE]

---

## 2026-06-16 — E-Verify incidence summary stopped saying wages do not rise

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` still said native low-skill wages "do not rise" and "do not measurably rise" under observed E-Verify mandate variation in its incidence-summary bullets. [DATA]

### Why it was wrong

Those lines were active reader-facing summaries. The source result is no statistically significant positive QWI wage effect plus rejection of large Borjas-style gains in that margin, not a literal no-rise or equivalence-tested zero. [SOURCE: memo] [INFERENCE]

### Fix

Replaced the incidence-summary bullets with no-statistically-significant-positive-QWI-wage-effect language and kept the large-gain rejection scoped to the E-Verify-style enforcement design. [SOURCE: memo]

### Updated conclusion

The causal synthesis now keeps the E-Verify wage result at the same statistical strength in both the top table and the incidence narrative. [INFERENCE]

---

## 2026-06-16 — Mass-deportation simulation kept as calibration output

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` still said mass deportation "would impose" the first-order output shock, and `research/immigration-causal-surge-2021-2024.md` described the lead figure as a GDP "cost" from removing 7M unauthorized workers. [DATA]

### Why it was wrong

The source is a BEA input-output partial-equilibrium calibration, not an observed or validated deportation episode. It freezes replacement hiring, wage response, and capital reallocation, and the Type-II endpoint is a multiplier sensitivity. The claim should present model output under assumptions, not a direct forecast. [SOURCE: memo] [INFERENCE]

### Fix

Changed the paradigm synthesis and surge memo to say the model produces or calibrates to a first-order output shock under calibration assumptions, while keeping the Type-II endpoint labeled as sensitivity. [SOURCE: memo]

### Updated conclusion

The mass-deportation result remains a medium-confidence calibration warning about possible output scale, not an empirical estimate of what would happen under an actual enforcement regime. [INFERENCE]

---

## 2026-06-16 — Card-side wage evidence separated from complementarity mechanism

### Issue

`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-confidence-ladder.md`, and `research/immigration-causal-everify-card-vs-borjas.md` still used shorthand such as Card (1990) "zero wage effect," "Card-style labor-market complementarity," and observed shocks "do not move native low-skill wages much." [DATA]

### Why it was wrong

The cited designs support bounded native-wage-impact evidence against large losses or gains in those designs. They do not prove literal zero effects, identify one shared complementarity mechanism across Mariel/E-Verify/Foged-Peri, or rule out small effects. [SOURCE: memo] [INFERENCE]

### Fix

Changed the Card/Mariel wording to no detected adverse effect, retitled the confidence-ladder and embedded ladder entry as "Card-side bounded native-wage-impact evidence," and replaced "do not move wages much" with no-large-native-wage-loss/gain language plus a mechanism caveat. [SOURCE: memo]

### Updated conclusion

The repo now treats the Card-side stack as bounded wage-impact evidence, not as proof of zero wages or a single identified complementarity mechanism. [INFERENCE]

---

## 2026-06-16 — E-Verify external-validity claim narrowed

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` said the E-Verify QWI design "IS the relevant test for the actual policy debate" after noting it may not generalize to mass deportation, large refugee inflow, or border closure. [DATA]

### Why it was wrong

Observed state E-Verify mandates are one important marginal-enforcement design. They are not the whole policy debate, which includes border closure, interior enforcement intensity, mass deportation, benefit restrictions, legal admissions, and surge regimes. Calling it "the" relevant test overstates external validity. [SOURCE: memo] [INFERENCE]

### Fix

Changed the external-validity caveat to say the E-Verify design is one relevant test for marginal tightening of unauthorized labor supply via state enforcement mandates, not the policy debate as a whole. [SOURCE: memo]

### Updated conclusion

The E-Verify memo now keeps its policy relevance without treating one marginal-enforcement design as sufficient for all immigration-policy wage claims. [INFERENCE]

---

## 2026-06-16 — Borjas restricted-Mariel extrapolation narrowed

### Issue

`research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and confidence-ladder entry 19 still said Borjas's restricted-Mariel result "does not generalize" to the broader designs. [DATA]

### Why it was wrong

The newer E-Verify/sanctuary/Foged-Peri-adjacent evidence cuts against mechanically exporting the restricted-Mariel magnitude to observed marginal enforcement designs. But it does not prove a universal non-generalization of the Mariel result across all possible low-skill shocks. [SOURCE: memo] [INFERENCE]

### Fix

Replaced "does not generalize" with "should not be mechanically extrapolated" to the observed E-Verify/sanctuary-style or broader staggered designs. [SOURCE: memo]

### Updated conclusion

The wage synthesis now treats Borjas's restricted-Mariel result as a contested shock-specific estimate whose magnitude should not be mechanically exported to other designs, while leaving broader external-validity questions open. [INFERENCE]

---

## 2026-06-16 — Crime denominator and race-correction caveats tightened

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` said a larger true unauthorized population would make crime rates "even lower," called the race-corrected gap a general correction to observed criminal-justice rates, and said within-race comparison "eliminates the compositional confound entirely." [DATA]

### Why it was wrong

The denominator statement is only mechanically true if the arrest numerator and immigration-status classification are held fixed. The race correction cited in the memo is an incarceration comparison, not a correction to every arrest/conviction measure. Within-race comparison removes racial composition as a confound, but it does not remove age, sex, geography, detection/reporting, or legal-status-classification uncertainty. [SOURCE: memo] [INFERENCE]

### Fix

Scoped the confidence statement to observed U.S. criminal-justice outcomes while naming the race-corrected figure as incarceration-specific; rewrote denominator sensitivity as conditional on fixed numerator/classification; and narrowed the within-race assessment to removal of the racial-composition confound. [SOURCE: memo]

### Updated conclusion

The crime memo's directional observed-rate finding remains, but its construction caveats now distinguish denominator arithmetic, incarceration-specific race correction, and remaining non-race confounders. [INFERENCE]

---

## 2026-06-16 — Local-burden wage channel scoped to observed margin

### Issue

`research/immigration-causal-synthesis-2026-04-18.md` said "The total local burden is school-finance + housing-rent + service-capacity, NOT wage compression." [DATA]

### Why it was wrong

The E-Verify QWI design rejects large positive native wage gains from marginal enforcement and does not support wage compression as the local-burden channel in that observed margin. It does not measure all current-inflow or surge wage effects, so "NOT wage compression" overstated the scope of the null. [SOURCE: memo] [INFERENCE]

### Fix

Changed the synthesis to say wage compression is not the supported local-burden channel in this cycle's observed E-Verify wage margin, while school-finance, housing-rent, and service capacity remain live channels and surge/current-inflow wage compression remains unmeasured. [SOURCE: memo]

### Updated conclusion

The local-incidence synthesis now distinguishes a bounded wage-margin result from broader wage-shock uncertainty. [INFERENCE]

---

## 2026-06-16 — Caplan channel ranking bounded to evidence surface

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` said the repo's evidence did not point to culture as the "first binding destination-country channel," that current U.S. stress channels run more through housing/services/politics, and that political externalities being manageable by default is "too optimistic." [DATA]

### Why it was wrong

The repo has better-developed evidence for housing, services, shelter, and political-response channels than for a clean culture-collapse mechanism. That does not prove a universal channel ordering or show that culture is never first-binding; it only supports a bounded criticism of Caplan's destination-incidence closure. [SOURCE: memo] [INFERENCE]

### Fix

Changed the Caplan audit to describe the current evidence surface as better developed for housing/service/shelter/political channels; added that this is not proof culture is never first-binding; changed political-response language from stronger signals to association signals; and replaced "too optimistic" with "not established" for manageable-by-default political externalities. [SOURCE: memo]

### Updated conclusion

The Caplan critique still says his destination-local incidence answer is incomplete, but it no longer turns the repo's current evidence coverage into a proved first-binding channel ranking. [INFERENCE]

---

## 2026-06-16 — Cash-economy substitution caveat kept measurable

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` said the true labor-supply contraction was "probably less" than the QWI E1 employment drop suggests and that this made the wage non-result "MORE puzzling for Borjas." [DATA]

### Why it was wrong

Off-W-2 substitution is a real measurement caveat, but the memo did not directly measure how much displaced unauthorized labor moved into cash work. "Probably less" and "MORE puzzling" turned a plausible measurement channel into an unmeasured directional claim. [SOURCE: memo] [INFERENCE]

### Fix

Changed the caveat to say cash-economy substitution weakens interpretation of the QWI E1 drop as a full labor-supply contraction, while not rescuing a large QWI-wage-gain prediction in this design. [SOURCE: memo]

### Updated conclusion

The E-Verify memo now treats cash-economy substitution as a measurement limitation, not as an unmeasured estimate of true labor-supply contraction. [INFERENCE]

---

## 2026-06-16 — Hanson wage counterfactual kept out of surge forecast

### Issue

`research/immigration-restrictionist-arguments-steelman-2026-06-15.md` said that when low-skill inflows resume in `2021–2023`, wage pressure on low-skill natives returns, and that Hanson implies a `+24% wage effect` if inflow had stayed at the `1994–2007` pace. [DATA]

### Why it was wrong

The local extract of Hanson w23753 frames the result as a counterfactual college/low-skill skill-premium gap: if low-skill inflow had continued, the `2015` skill premium would have been about `6–9` percentage points higher. That is a useful restrictionist labor-supply input, but it is not a direct estimate of surge-era native wage pressure and needs a cohort/geography/demand bridge before being exported to `2021–2023`. [SOURCE: research/immigration-restrictionist-corpus-parse-2026-06-15.md] [INFERENCE]

### Fix

Replaced the `+24%` wage-effect and resumed-inflow forecast phrasing with the source's narrower `6–9pp` skill-premium counterfactual and an explicit bridge requirement. [SOURCE: memo]

### Updated conclusion

The restrictionist steelman still gets to use Hanson as a labor-supply counterfactual and secular-supply warning, but not as an unbridged surge-era wage forecast. [INFERENCE]

---

## 2026-06-16 — Cycle summary narrowed to E-Verify wage margin

### Issue

`CYCLE.md` still said the causal cycle would "resolve Card-vs-Borjas verdict for U.S. data," that E-Verify mandates produced "no positive wage effect" and rejected Borjas's wage prediction, and that supply fell with wages flat implying employer adjustment through capital/relocation. [DATA]

### Why it was wrong

The underlying QWI design is an observed E-Verify mandate-margin test. It can reject large Borjas-style native wage gains in that design, but it does not settle the full Card-vs-Borjas family, surge or mass-shock regimes, or the mechanism behind the W-2 employment decline. [SOURCE: CYCLE.md] [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [INFERENCE]

### Fix

Changed the cycle goal, queue, discovery bullets, completion note, and verification result to describe a bounded observed E-Verify QWI wage-channel update. Mechanism language now lists capital, output, relocation, cash-economy substitution, hours, and composition as candidate channels rather than measured adjustment. [SOURCE: memo]

### Updated conclusion

The cycle summary no longer exports a broad labor-market verdict from one marginal enforcement design. [INFERENCE]

---

## 2026-06-16 — Capacity frontier political-map verb kept descriptive

### Issue

`research/immigration-capacity-frontier-2026-04-21.md` said "`stock` drives the broad political map" even though the same section and claims-table scope note treat the county models as descriptive model-output evidence rather than causal identification. [DATA]

### Why it was wrong

The model ranking shows that stock share carries the strongest one-predictor countywide political signal. "Drives" implies causal direction that this model does not identify, especially given confounders like long-run demographic sorting and Hispanic realignment already named in the memo. [SOURCE: memo] [INFERENCE]

### Fix

Changed the summary bullet to say stock carries the broad political-map signal in this county model. [SOURCE: memo]

### Updated conclusion

The capacity frontier memo now keeps its politics result at the descriptive model-signal level throughout that section. [INFERENCE]

---

## 2026-06-16 — E-Verify employment not used as deportation validation

### Issue

`research/immigration-confidence-ladder.md` said the mass-deportation calibration was "consistent with E-Verify empirical finding (-6% E1 employment under 50% compliance)." [DATA]

### Why it was wrong

The E-Verify employment result is a marginal state-enforcement design with partial compliance and QWI W-2 measurement. The mass-deportation run is a BEA partial-equilibrium calibration that freezes replacement hiring, wage response, and capital reallocation. Similar directional employment pressure is not validation of the national shock size or industry-loss magnitudes. [SOURCE: research/immigration-causal-everify-card-vs-borjas.md] [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] [INFERENCE]

### Fix

Changed entry 24 to treat E-Verify employment as, at most, a weak plausibility check under one marginal enforcement setting, and added entry 40 explicitly saying E-Verify employment does not validate the mass-deportation calibration. [SOURCE: memo]

### Updated conclusion

The ladder now separates a bounded empirical employment signal from a national partial-equilibrium deportation calibration. [INFERENCE]

---

## 2026-06-16 — Card setup kept as prediction language

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` described the Card-side theory setup as "Removing [low-skill immigrants] via enforcement will produce small or zero wage gains for natives." [DATA]

### Why it was wrong

That section is a theory/prediction contrast, not a measured result. "Will produce" can read as an established claim rather than the Card-side prediction being tested by the E-Verify design. [SOURCE: memo] [INFERENCE]

### Fix

Changed the line to "is predicted to produce small or zero wage gains," keeping the subsequent empirical result separate from the setup. [SOURCE: memo]

### Updated conclusion

The E-Verify memo now distinguishes theory expectations from observed QWI findings in the interpretation setup. [INFERENCE]

---

## 2026-06-16 — Recent-inflow election mechanism left unresolved

### Issue

`research/immigration-causal-surge-2021-2024.md` said the negative `recent_fb_annual_share` coefficient "probably reflects D-leaning new immigrants voting D, or already-D establishment." [DATA]

### Why it was wrong

The regression output identifies an association in the model, not the mechanism. The memo's own interpretation paragraph correctly lists multiple possibilities, including new citizens, sympathetic natives, and unresolved compositional confounding. The bullet should not promote one mechanism with "probably" language. [SOURCE: memo] [INFERENCE]

### Fix

Changed the bullet to say counties with higher recent inflow swung less GOP in this model, while the mechanism remains unresolved across citizenship timing, already-D county context, sympathetic natives, and other compositional confounding. [SOURCE: memo]

### Updated conclusion

The surge memo now keeps the recent-inflow election coefficient at the model-association level until a mechanism-specific design is run. [INFERENCE]

---

## 2026-06-16 — Caplan worker-incidence channel kept evidence-surface scoped

### Issue

`research/immigration-bryan-caplan-claims-audit-2026-04-21.md` said the "strongest current worker-incidence channel" is slower wage progression in constrained places rather than job destruction. [DATA]

### Why it was wrong

The memo can say current repo evidence better develops constrained-place wage progression than broad job-destruction rhetoric. But "strongest current channel" implies a global channel ranking across worker incidence that the cited county panel does not establish. [SOURCE: memo] [INFERENCE]

### Fix

Changed the line to say that in the repo's current worker-incidence evidence surface, the better-developed concern is slower wage progression in constrained places rather than broad job destruction. [SOURCE: memo]

### Updated conclusion

The Caplan audit still rejects crude job-collapse rhetoric, while keeping the alternative worker-incidence channel scoped to the current evidence surface. [INFERENCE]

---

## 2026-06-16 — E-Verify event-study interpretation kept unresolved

### Issue

`research/immigration-causal-everify-card-vs-borjas.md` said slightly negative, nonsignificant event-study point estimates were "suggestive of mild complementarity loss," and said a mass-deportation shock would "probably not" behave the same as the E-Verify design. [DATA]

### Why it was wrong

The event-study coefficients are not statistically distinguishable from zero, so the memo should not give one mechanism a suggestive gloss. Likewise, mass deportation is outside the observed mandate margin; "probably not" is plausible, but the stronger source-anchored statement is simply that the behavior is unknown because magnitudes and equilibria differ. [SOURCE: memo] [INFERENCE]

### Fix

Changed the event-study sentence to say the slightly negative points should not be read as evidence for a specific complementarity-loss mechanism, and changed the mass-deportation bullet to "unknown" rather than "probably not." [SOURCE: memo]

### Updated conclusion

The E-Verify memo now keeps nonsignificant event-study movement and out-of-margin mass-shock behavior unresolved instead of assigning them a preferred mechanism. [INFERENCE]

---

## 2026-06-16 — E-Verify null and Borjas-scaling language made symmetric

### Issue

A post-fix model review found that the E-Verify memo and summaries still applied significance discipline asymmetrically: wage coefficients were described as nonsignificant, but the E1 employment coefficient was still written as a realized `~6%` fall despite `t=-1.40` / `p≈0.16`. The same review flagged that the memo's `~5-15%` Borjas benchmark was not scaled to the observed mandate-margin shock. [DATA]

### Why it was wrong

The QWI employment point estimate is negative, but not conventionally significant. Treating it as a measured drop made the "employment fell while wages did not rise" contrast too strong. Separately, Borjas's own elasticity framing implies that a smaller effective supply shock maps to a smaller wage benchmark, so the memo can cut against large gains in the observed margin without rejecting every scaled Borjas effect. [SOURCE: `research/immigration-causal-everify-card-vs-borjas.md`] [INFERENCE]

### Fix

Updated `research/immigration-causal-everify-card-vs-borjas.md`, `CYCLE.md`, `research/immigration-causal-synthesis-2026-04-18.md`, `research/immigration-confidence-ladder.md`, `research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md`, and `research/immigration-restrictionist-arguments-steelman-2026-06-15.md`:

- E1 employment is now a negative, statistically nonsignificant point estimate rather than a measured drop.
- The wage result now cuts against large Borjas-style native wage gains in the observed mandate margin, while leaving small effects and scaled-shock benchmarks unresolved.
- "Card/Borjas" comparison labels now name directional readings in each design rather than global debate verdicts.

### Updated conclusion

The current E-Verify conclusion is narrower: observed mandate variation shows no statistically significant positive QWI wage effect for native low-skill workers and cuts against large native wage gains where the source CI/MDE supports that read. It does not prove an exact zero wage effect, a measured labor-supply contraction, a significant employment decline, a heterogeneity-robust staggered-DiD ATT, or a global rejection of Borjas-style mechanisms. [INFERENCE]

---

## 2026-06-16 — Crime memo Lott narrative matched critique status

### Issue

`research/immigration-crime-rates-unauthorized-vs-native-born.md` had downgraded the Lott Arizona row to `SUPPORTED CRITIQUE — not independent reanalysis`, but the bottom line and contrarian-case heading still said Lott had been criticized for a "fundamental data classification error." [DATA]

### Why it was wrong

The memo cites serious critiques from Cato, Washington Post, and Latino Decisions; it does not independently reanalyze Arizona DOC records. The supported claim is an unresolved immigration-status classification critique, not a verified data error. The Texas `>2x` violent-arrest row also needed the memo's own aggregate-native-denominator / race-composition caveat. [SOURCE: memo] [INFERENCE]

### Fix

Changed the bottom-line and contrarian-case Lott wording to "serious unresolved" / "serious possible" immigration-status classification problem. Added a denominator caveat to the Texas `>2x` violent-arrest claim row. [SOURCE: memo]

### Updated conclusion

The crime memo still supports lower observed criminal-justice rates for unauthorized immigrants in the best current U.S. datasets, but it no longer treats the Lott classification critique as independently verified by this memo or the aggregate Texas ratio as race-composition-adjusted. [INFERENCE]

---

## 2026-06-16 — Capacity and surge model rankings kept descriptive

### Issue

Model review flagged several remaining places where descriptive county or receiver-city model output was being read too strongly: the capacity memo called load/capacity the "cleaner" wage signal despite tiny adjusted-`R²` gaps, the surge memo bundled gross fiscal load and election shift into one "empirical support" story, and the Caplan audit treated constrained-place wage pressure as more established than the county screen supports. [DATA]

### Why it was wrong

The county capacity pass is useful descriptive screening, not causal identification. For wages, the load-only adjusted-`R²` edge over stock/flow is only about 0.007-0.010, and permit units in the denominator can proxy local economic vitality. The surge receiver fiscal figures are observable gross loads, but the +2.4pp receiver election coefficient is still correlational. Caplan's labor critique should cite evidence consistent with constrained-place wage pressure, not treat it as a settled channel. [SOURCE: memos] [INFERENCE]

### Fix

Updated:

- `research/immigration-capacity-frontier-2026-04-21.md`: stock/load claims now say "one-predictor county model signal," wage ranking is "marginally best-fitting," q90 threshold weakness is caveated for power/multiple-testing, and permit-denominator confounding is explicit.
- `research/immigration-causal-surge-2021-2024.md`: per-migrant costs are scoped to sheltered-migrant-day gross cost, receiver load is separated from the correlational election result, the stale `~50K/month` flow line is replaced with the corrected Total-CBP range, and the original no-Hispanic receiver regression is reconciled with the later Hispanic-share kill-test sample.
- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md`: constrained-place wage pressure is evidence-consistent rather than a settled pressure channel.

### Updated conclusion

The capacity/surge evidence remains decision-relevant as descriptive screening: it points to load/capacity, receiver fiscal load, and constrained-place wage-growth concerns. It does not yet identify a causal native-exit mechanism, a fiscal-load-to-vote mechanism, or a globally ranked worker-incidence channel. [INFERENCE]

---

## 2026-06-16 — Thesis generator loop widened beyond fiscal ledger monoculture

### Issue

The lifetime generator loop was strong on fiscal layers, denominator discipline, and scalar-export prevention, but the active prompts were still mostly fiscal/lifetime-native. The registry also had a lifecycle-sync problem: `research/immigration-lifetime-fiscal-generators.md` had 106 `G-LIF-*` headings, its header said 105 generators, and DuckDB had 104 `lifetime_generators` rows. [DATA]

### Why it was wrong

The user's search-space shaping has repeatedly added non-fiscal axes: psychology, political legitimacy, narrative formation, urban capacity, macro transition paths, and micro adaptation. A generator loop that only mines fiscal papers risks converging too early on ledger-correct but narrative-blind theses. The count mismatch also blocks honest yield tracking and retirement rules. [SOURCE: `research/immigration-thesis-generator-audit-2026-06-16.md`] [INFERENCE]

### Fix

Added `research/immigration-thesis-generator-audit-2026-06-16.md`, with cross-disciplinary `XDISC-*` generators, a self-prompt packet, a human-replacement flowchart for search-space shaping, and an implementation recommendation for generator lifecycle fields. Updated the topic index, sweep protocol, and divergence cookbook to route future sweeps through this packet. Changed the fiscal-generator header and index wording from stale counts to warehouse-grounded counts plus the explicit reconciliation issue (`G-LIF-Q06`, `G-LIF-S15` MD-only). [SOURCE: memo]

### Updated conclusion

The current loop should not run another immigration sweep from fiscal generators alone. Before source search, it should run the cross-disciplinary packet, then converge with explicit data-vs-frame separation and generator-yield accounting. [INFERENCE]

---

## 2026-06-16 — Verified federal and school surfaces refreshed

### Issue

`research/immigration-verified-findings-report-2026-04-10.md` and `research/immigration-confidence-ladder.md` still treated two April surfaces as if they were current: the household-normalized child-burden correction was easy to read as a live full-stock school/adult or origin net sign, and the failed Texas/CPS donor prototype was still described as the repo's current federal surface. [DATA]

### Why it was wrong

June work changed both surfaces. The school-burden tensor now withholds origin school/net rows because the available school numerator came from the scenario-household universe while the federal row uses full microsim adults. Separately, the SIPP-style federal annual proxy supersedes the April ACS/CPS shortcut for the narrow cash-flow ledger, but only as payroll/FICA minus SNAP, TANF, and SSI; it is not income tax, Medicare/Medicaid, EITC, capital/corporate tax, household filing, lifetime NPV, or all-government net. [SOURCE: `research/immigration-school-burden-per-adult-2026-06-15.md`] [SOURCE: `research/immigration-federal-distribution-findings-2026-06-15.md`] [SOURCE: `research/immigration-country-fiscal-tensor-2026-06-15.md`]

### Fix

Updated:

- `research/immigration-verified-findings-report-2026-04-10.md`: scoped household-normalized school language to linked-household child exposure, marked origin school/net rows as withheld pending same-universe rebuild, replaced the current-federal-prototype language with the June SIPP-style narrow annual proxy plus all-in limitations, and added a revisions table.
- `research/immigration-confidence-ladder.md`: qualified the household metric, downgraded the old ACS income/benefit ranking to historical screen, added entry `41` for the current narrow federal annual proxy, and updated the reading rule.

### Updated conclusion

The current verified surface is narrower and cleaner: strong linked-household child-exposure evidence; medium-strong descriptive evidence for a narrow annual federal cash-flow proxy; no live all-in federal number; and no current origin `federal - school` sign until the school numerator and adult denominator are rebuilt on the same universe. [INFERENCE]

---

## 2026-06-16 — Full-protocol sweep rows marked superseded

### Issue

`research/immigration-sweep-cycles-23-32-2026-06-15.md` was still routed by the topic index as the "full protocol" sweep and contained old origin school/net rows: Mexico `school` `$771`, Mexico `crude` `+$748`, EU27 `school` `$64`, and similar rows for cycle 32. Those rows came from the intermediate correction that was later rejected by the same-universe guard. [DATA]

### Why it was wrong

The current `v_three_layer_annual` view withholds origin and aggregate foreign-born school/net rows. A direct DuckDB query on 2026-06-16 returned `NULL` `school_per_adult` and `net_crude_per_adult` for `mexico_origin`, `mx_ca_cluster`, `eu27_origin`, `uk_origin`, and `fb_lt_hs`; only `nh_white_usborn` retained a built school/net row in that slice. Leaving the old numeric rows unqualified in the full-protocol memo made it too easy for later agents to cite a stale `federal - school` sign. [DATABASE: `warehouse/immigration_fiscal_union.duckdb` view `v_three_layer_annual`] [INFERENCE]

### Fix

Updated `research/immigration-sweep-cycles-23-32-2026-06-15.md` with a 2026-06-16 status block, supersession notes on cycles 24, 26, 30, and 32, and a revisions table. Updated `research/immigration-INDEX.md` so the route row warns not to cite the old `$771/+748` origin school/net outputs. [SOURCE: memo]

### Updated conclusion

Sweeps 23–32 still preserve useful NAS education-mix, federal-proxy, and thesis-generation work, but their origin school/net numbers are historical traces, not current facts. Current live origin `federal - school` signs remain withheld until same-universe school numerators are rebuilt. [INFERENCE]

---

## 2026-06-16 — Quick claims matrix labels narrowed

### Issue

`research/immigration-claims-matrix-2026-04-11.md` was still framed as the current defensible claim set and used terse verdict labels such as `MODERATE-FALSE`, `VERIFIED false`, and `MODERATE-FALSE (as complete fix)` for commentator claims. It also described the household child metric as "school burden" without carrying the later same-universe guard. [DATA]

### Why it was wrong

The named Smith/Decker and Friedman audits support strong critiques, but their own language is narrower: Decker's "must make us richer" fails as a universal theorem; the politics-only claim is false as an exclusivity claim; Friedman's transfer/voting proposal is incomplete rather than empirically false in all frames. Separately, the child rows are linked-household exposure metrics, not current full-stock school-burden-per-adult or origin `federal - school` signs. [SOURCE: `research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md`] [SOURCE: `research/immigration-david-d-friedman-claims-audit-2026-04-11.md`] [SOURCE: `research/immigration-school-burden-per-adult-2026-06-15.md`]

### Fix

Updated `research/immigration-claims-matrix-2026-04-11.md` with a 2026-06-16 status note, added an `OVERBROAD` legend entry, scoped row 5 to linked-household child exposure, replaced hard false labels with scoped overbreadth/incomplete verdicts, and updated the verdict envelope to include the narrow SIPP-style federal proxy plus withheld origin school/net signs. Updated the index route row to warn that this matrix is a quick ledger, not the latest tensor. [SOURCE: memo]

### Updated conclusion

The quick matrix still supports the same broad incidence split, but it no longer exports overconfident boolean labels or treats linked-household child exposure as a live school/adult fiscal scalar. [INFERENCE]

---

## 2026-06-16 — Public economist summaries scoped to descriptive evidence

### Issue

The public-facing economist one-pager, debate sheet, and rhetorical-failures memo still used several stronger causal or mechanism-flavored phrases after the underlying capacity/surge corrections had been narrowed. Examples included treating `flow x capacity x composition x regime` as a live causal object, describing destination-local "harm" rather than stress/gross-load evidence, using native-backlash language where the measured object is political-response association, and presenting constrained-place wage pressure as firmer than the county screen supports. [DATA]

### Why it was wrong

The later capacity/surge corrections say the county capacity pass is useful descriptive screening, not causal identification; the receiver fiscal rows are gross load and shelter-stress evidence, not net fiscal-burden estimates; and the receiver-election result is a correlational `+2.4pp` upper-bound after controls, not a fiscal-load-to-vote mechanism. Public summaries are high-reuse artifacts, so causal overtones there can undo the narrower source memos. [SOURCE: `research/immigration-capacity-frontier-2026-04-21.md`] [SOURCE: `research/immigration-causal-surge-2021-2024.md`] [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`]

### Fix

Updated:

- `research/immigration-economist-one-pager-2026-04-22.md`: added a 2026-06-16 status warning and changed capacity, denominator, federal/local, and political wording to descriptive/gross/correlational language.
- `research/immigration-economist-debate-sheet-2026-04-22.md`: added the same scope warning and narrowed the wage, fiscal, and political counters.
- `research/immigration-economist-rhetorical-failures-2026-04-22.md`: changed "harm," "rejected," "native backlash," and "live causal object" style language to stress/gross-load/political-response/descriptive-screen language.

### Updated conclusion

The public economist critique remains intact: partial efficiency and migrant-gain arguments do not settle destination-country welfare. The evidence basis is now stated more precisely: current capacity/surge support is descriptive and correlational where the underlying designs do not identify causal mechanisms. [INFERENCE]

---

## 2026-06-16 — Legacy synthesis surfaces aligned with same-universe guard

### Issue

Two high-reuse synthesis surfaces still carried language from before the June 16 narrowing pass. `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` said the executive short-horizon row was withheld, but its warehouse-layer table still printed the superseded Mexico-origin `$771` school and `+$748` crude-net rows. `research/immigration-claims-evolution-ledger-2026-04-23.md` also kept older Card/Borjas and native-backlash shorthand that could be read as stronger than the current E-Verify and political-response surfaces support. [DATA]

### Why it was wrong

The same-universe guard withholds origin `school_burden_per_adult` and `net_crude_federal_minus_school` until the school numerator is rebuilt on the same population universe as the adult denominator. Separately, the current E-Verify conclusion is mandate-margin and nonsignificance-scoped, and receiver-election evidence is correlational political response, not identified backlash motivation. [SOURCE: `research/immigration-conclusion-audit-running-fixes.md`] [INFERENCE]

### Fix

Updated `research/immigration-mexico-npv-population-synthesis-2026-06-15.md` to mark the old `$771/+748` rows as withheld/superseded and added an explicit disconfirmation row against citing them as current. Updated `research/immigration-claims-evolution-ledger-2026-04-23.md` with a 2026-06-16 status note, narrowed the labor-market summary to observed E-Verify mandate variation, and replaced native-backlash wording with citizen political-response language. [SOURCE: memos]

### Updated conclusion

The evolution ledger and Mexico synthesis now match the current frontier: no live Mexico-origin `federal - school` sign, no measured E-Verify labor-supply contraction, and no identified fiscal-load-to-vote or backlash mechanism. [INFERENCE]

---

## 2026-06-16 — Final Opus/Cursor review disposed

### Issue

The final post-cleanup Opus/Cursor review packet found three remaining high-impact drift classes: the Mexico NPV synthesis still exported an illustrative `-$37k to +$28k` lifetime band that mixed withheld school, surge, enforcement, discount, and population-universe assumptions; generator/index/cookbook routes still carried stale fiscal or Card/Borjas labels; and the agent-loop docs still presented partially overlapping loops as if they were fully operational automation. [SOURCE: `.model-review/2026-06-16-final-immigration-review/`]

### Why it was wrong

The Mexico lifetime band could not be reproduced from live additive rows without either reintroducing the withheld school row or mixing rate/horizon conventions. The route/process problem was also real: if the index, cookbook, and generator registry point agents at stale or conflicting surfaces, the loop will rediscover known failures instead of replacing human search-space shaping. [INFERENCE]

### Fix

Updated:

- `research/immigration-mexico-npv-population-synthesis-2026-06-15.md`: removed the numeric lifetime band and replaced it with non-additive layer checks.
- `research/immigration-lifetime-fiscal-generators.md`: fixed rounds label, scoped the `$1,519` proxy to `mexico_origin`, and marked the `$771` school retrodiction as withheld.
- `research/immigration-claims-evolution-ledger-2026-04-23.md`, `research/immigration-INDEX.md`, `CYCLE.md`, and `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`: carried June scoping, CI/MDE, and static-TWFE caveats into high-reuse surfaces.
- `research/immigration-economist-rhetorical-failures-2026-04-22.md`: made the job-collapse steel-man cite E-Verify for the wage-channel margin and keep county evidence scoped to constrained-place screens.
- `research/immigration-thesis-generator-audit-2026-06-16.md`, `notes/immigration-lifetime-synthesis-diverge-cookbook.md`, and `notes/immigration-lifetime-sweep-protocol.md`: made `immigration-knowledge-delta-agent-loop-2026-06-16.md` the canonical umbrella loop and the generator audit an XDISC sub-loop.
- `notes/provenance-tags.md`: added a single local tag vocabulary and pointed loop docs at it.
- `infra/immigration-fiscal/derived/stage3_proto/three_layer_annual_2023.csv`: synced the tracked staged mirror to the withheld-origin build output; local ignored `sources/.../stage3_proto` CSV mirrors were synced as well. [DATA]

### Remaining process debt

Generator lifecycle is still manual: Markdown has `106` `G-LIF-*` headings, DuckDB has `104` `lifetime_generators` rows, MD-only IDs are `G-LIF-Q06` and `G-LIF-S15`, and no lifecycle sidecar or DuckDB table yet records `fired`, `adopted`, `dry`, `parked`, and `adoption_judge`. Do not automate yield-based parking or retirement until that state exists. [SOURCE: `research/immigration-thesis-generator-audit-2026-06-16.md`] [LIMIT]

### Updated conclusion

The final reviewed state is narrower: no Mexico-origin lifetime band, no live origin `federal - school` sign, E-Verify remains a bounded static-TWFE mandate-margin wage result with source CI/MDE caveats, and the agent loop is a canonical assisted process rather than a fully autonomous replacement until lifecycle state and adoption judging are implemented. [INFERENCE]
