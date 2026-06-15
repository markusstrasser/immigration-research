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
