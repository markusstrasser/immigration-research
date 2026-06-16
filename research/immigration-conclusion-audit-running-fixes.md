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

## 2026-06-16 — Open-borders weight framing separated from empirical inputs

### Issue

`research/immigration-causal-paradigm-escape-synthesis-2026-04-18.md` and confidence-ladder entry 23 described the open-borders verdict as "welfare-weight-determined, not data-determined" and said the repo could not resolve it empirically. That phrasing risked treating model cost/capacity inputs as settled merely because the welfare weight itself is normative. [DATA]

### Why it was wrong

The welfare weight assigned to immigrants is a value choice. But scenario costs, fiscal ledgers, housing/capacity constraints, labor-market adjustment, and sending-country effects are empirical inputs. New evidence cannot pick the moral weight, but it can move the break-even thresholds under any chosen weight. [INFERENCE]

### Fix

Reframed the paradigm synthesis and embedded ladder text around a normative weight plus empirical inputs, annotated confidence-ladder entry 23 as qualified, and added entry 39 with the corrected reading. Added a memo revision row. [SOURCE: memo]

### Updated conclusion

The open-borders conclusion still must state its welfare-weight assumption, but the repo should keep collecting and grading cost/feasibility evidence rather than treating the scenario as fully non-empirical. [INFERENCE]
