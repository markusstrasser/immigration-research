# Immigration conclusion audit — running fixes

**Purpose:** running ledger of statistical, mathematical, logical, and data-science issues fixed while auditing immigration conclusions.

**Rule:** each entry names the broken conclusion, the evidence that changed it, what was edited, and what remains unresolved. This is not a final immigration position memo.

---

## 2026-06-15 — School-burden denominator correction

### Issue

The school-burden memo and a stale exported CSV still supported the conclusion that Mexico-origin adults had a crude annual federal-minus-school balance of about **-$13.5k/adult**. That result used the `origin_fiscal_scenario_2023` scenario subset denominator (~436,819 adults) after multiplying area-weighted per-pupil school spend by household school-age children. [DATA]

That denominator was wrong for a full Mexico-origin adult-stock conclusion. The live tensor now uses the full Mexico microsim adult denominator (~8,496,334 adults). [DATA]

### Evidence Checked

```sql
SELECT *
FROM v_three_layer_annual
WHERE population_group = 'mexico_origin';
```

Current DuckDB result from `warehouse/immigration_fiscal_union.duckdb`:

| federal_per_adult | school_per_adult | net_crude_per_adult | weight_adults |
|------------------:|-----------------:|--------------------:|--------------:|
| 1519.278 | 771.285 | 747.993 | 8496334 |

Scenario source check from `warehouse/immigration_lifetime_evidence.duckdb`:

| origin | scenario adults | avg federal net | area-wtd per pupil | school-age kids/HH | HH weight |
|--------|----------------:|----------------:|-------------------:|-------------------:|----------:|
| Mexico | 436819 | 1519.278 | 20907.09 | 0.9718 | 322540 |

The old ~-$13.5k conclusion came from dividing the household school burden by the scenario subset. The corrected school burden is about:

`20907.09 * 0.9718 * 322540 / 8496334 = ~$771/adult` [INFERENCE]

### Fixes Made

1. Updated `research/immigration-school-burden-per-adult-2026-06-15.md`:
   - Mexico-origin row now reads `$1,519` federal, `$771` school, `+$748` crude annual.
   - Removed the stale verdict that Mexico looks far worse than natives on crude static federal-minus-school math.
   - Added a revision note explaining the scenario-denominator bug.

2. Updated `research/immigration-scenario-composition-2026-06-15.md`:
   - Replaced obsolete `~$21/pupil` text with post-F-33 `~$20,907/pupil`.
   - Added a warning not to use `436,819` scenario adults as the full Mexico-origin stock denominator.

3. Updated `research/immigration-lifetime-fiscal-generators.md`:
   - Rewrote G-LIF-K01 so future audits check both F-33 units and per-adult denominator discipline.

4. Updated `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`:
   - The tensor builder now exports `three_layer_annual_2023.csv` from the live `v_three_layer_annual` view.

5. Regenerated canonical staged CSVs under `infra/immigration-fiscal/build/stage3_proto/`, including `three_layer_annual_2023.csv`, from the live DuckDB view.

### Current Conclusion

The corrected finding is narrower and less rhetorically satisfying: the built annual **federal-minus-school** layer is **positive for Mexico-origin adults** under the current full-stock microsim denominator. [DATA]

This does **not** prove Mexico-origin immigration is all-government fiscally positive. The lifetime NPV, state/local surge, enforcement, courts, and episodic shelter layers are still separate and cannot be collapsed into this crude annual layer. [INFERENCE]

### Remaining Risk

The full-stock denominator may understate school incidence for recent-arrival or unauthorized subgroups if those subgroups are younger and more child-heavy than the full Mexico-born 25-64 stock. That is a legal-status/cohort split, not a license to reuse the scenario denominator for a full-stock conclusion. [INFERENCE]

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

Comparable school-layer row from `v_three_layer_annual` remains about `$771/adult/yr`, making the current crude annual federal-minus-school row `+$748/adult/yr` for Mexico-origin adults under the full-stock denominator. [DATA]

### Fixes Made

1. Updated `research/immigration-lifetime-country-approx-brainstorm-2026-06-15.md`:
   - Replaced the stale Mexico and MX+Central America `~−$80k` lifetime rows with current synthetic age-25 benchmarks.
   - Replaced the invalid `per-pupil ≪ federal annual` verdict with the comparable adult-denominator statement: `$771/adult` school burden vs `$1,519/adult` federal proxy.

### Current Conclusion

The useful conclusion is not that local per-pupil costs are small. The corrected conclusion is narrower: after bridging to the current full-stock adult denominator, the built Mexico school layer is smaller than the narrow federal proxy on an annual basis, leaving a crude `+$748/adult/yr` federal-minus-school row. [INFERENCE]

This does not settle marginal school cost, descendant attribution, legal-status/cohort incidence, or receiver-city episodic costs. [INFERENCE]

---

## 2026-06-16 — Pre-rebuild sweep rows marked superseded

### Issue

Several still-indexed June 15 memos carried first-pass sweep rows after the underlying tensor had changed:

- `immigration-europe-caucasian-fiscal-findings-2026-06-15.md` reported Mexico-origin lifetime NPV as `−$79k` and US foreign-born stock as `−$71k`, from the older `<HS`/HS-only NAS seed.
- `immigration-sweep-cycles-13-22-2026-06-15.md` still reported Mexico crude annual `federal − school` as `−$13.5k/adult` and "Mexico ~4x worse than NH white US-born", from the scenario-subset school denominator.
- `immigration-lifetime-unified-theory-2026-06-15.md` had a compressed thesis line implying Mexico's lifetime layer was simply negative.

### Evidence Checked

Current `v_three_layer_annual` rows:

| population | federal/adult | school/adult | crude net/adult |
|------------|--------------:|-------------:|----------------:|
| Mexico-origin | $1,519.28 | $771.29 | $747.99 |
| MX + N. Triangle | $1,519.02 | $1,091.46 | $427.55 |
| EU27-origin | $4,694.65 | $63.71 | $4,657.82 |
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
