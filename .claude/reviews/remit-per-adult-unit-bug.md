# Forensic Audit: `remit_per_adult` = $151,636 Unit Bug

**Status: PROBE IN PROGRESS**

Theory: "Remittance outflow dominates federal net for Mexico" (M-cluster)
Symptom: `remit_per_adult` returns $151,636 for Mexico; expected ~$2,000–5,000/yr.

Warehouse: `/Users/alien/Projects/immigration-research/warehouse/immigration.duckdb` (read_only)

## Findings (appended as confirmed)

### 1. The test query (CONFIRMED)
```sql
SELECT 66237847600/436819 AS remit_per_adult, avg_federal_net
FROM life.origin_fiscal_scenario_2023 WHERE origin_label='Mexico'
```
Reproduces `remit_per_adult = 151636.83`, `avg_federal_net = 1519.28`.
Both numerator and denominator are HARDCODED LITERALS in the theory's `duckdb_test`
(theories_tested table), NOT computed from columns.

### 2. The denominator 436,819 (CONFIRMED = wrong population)
- `436819` == `origin_fiscal_scenario_2023.weighted_adults` for Mexico.
- BUT this is the **local_flow / household-LINKED subset** weight, not the full adult pop.
- Proof from `infra/immigration-fiscal/build/stage3_proto/country_fiscal_rollup_2023.csv`:
  - `mexico_origin, federal_annual` → `weight_adults = 8,496,334` (~8.5M, the REAL adult pop)
  - `mexico_origin, local_flow`     → `weight_adults = 436,819` (n_cells=1, linked subset)
- So the test divided a NATIONAL-total remittance figure by a ~5% linked subsample → ~20x inflation.

### 3. The numerator 66,237,847,600 (~$66.2B) (CONFIRMED external/hardcoded)
- Does NOT appear anywhere in `infra/`.
- `lifetime.remittance_series` table is EMPTY (World Bank source JSON absent at build time;
  `_load_remittances` does `if not p.exists(): continue` — build_lifetime_evidence_warehouse.py:126).
- So 66.2B was hand-entered by the theory author = total Mexico remittances RECEIVED (World Bank,
  ~2014 era value; 2022 actual was ~$61B). It is a NATIONAL TOTAL inflow, not a per-adult or
  per-US-immigrant figure.

### Smell test corroboration
- `origin_fiscal_scenario_2023.avg_medicaid_total_computable = 109,350,743,246` for Mexico —
  a $109B "average" is itself nonsensical (should be hundreds/thousands per adult), confirming
  the table mixes totals and per-adult/averaged columns inconsistently.

### 4. The denominator is itself a NARROW slice, not even the full US-Mexican adult pop (CONFIRMED)
`acs_origin_national_2023.weighted_adults` (Mexico) = 436,819 is built in
`build_immigration_warehouse.py:119-146` from the `qual_person` view, which filters to a
deliberately narrow subpopulation:
```
WHERE AGEP BETWEEN 25 AND 64        -- prime-age only
  AND NATIVITY = '2'                -- foreign-born
  AND SCHL < 16                     -- LESS THAN high-school diploma (low-skill only)
  AND YOEP >= 2014 AND YOEP < 9999  -- arrived 2014 or LATER (recent only)
```
So 436,819 = recent (post-2014), low-skill (<HS), prime-age Mexican immigrants.
By contrast `context.acs_origin_household_federal_microsim_2023` sums to **8,520,718** adults
for Mexico (the broad foreign-born adult population, matching the `federal_annual` rollup's
`weight_adults = 8,496,334`). The `local_flow` rollup row uses the narrow 436,819.

### 5. Numerator verified external (CONFIRMED via World Bank)
Per the theory's own provenance (`research/.mining/immigration-lifetime-cluster-m-annual-bridge.json`,
`parameter_claims[2]`):
- `value_numeric: 66237847600`, labeled "Mexico inbound personal remittances (World Bank BX.TRF.PWKR.CD.DT)"
- Exa verify: confirmed = 2023 total personal remittances RECEIVED by Mexico (~$63–66.2B; the
  $66.2B figure is the World Bank/WDI value).
This is GROSS INBOUND remittances to Mexico FROM THE ENTIRE WORLD — a NATIONAL TOTAL, not a
per-adult figure and not US-origin-only.

### 6. The bug is self-documented in the artifact (CONFIRMED)
The generator that produced the theory (`generators[1]` in the mining JSON):
- prompt: "Join World Bank remittance series ... to origin_fiscal_scenario weighted_adults.
  Compute remittance per weighted adult."
- `unnamed_assumptions_surfaced[0]: "All remittances from US immigrants from that origin"` —
  the generator EXPLICITLY flagged that it was attributing all $66.2B (global inbound) to US immigrants.
The `theories_tested[].duckdb_test` string is loaded VERBATIM into the warehouse table at
`build_lifetime_evidence_warehouse.py:341` (`_load_mining_artifacts`). No SQL build script
computes `remit_per_adult`; it is a hardcoded literal-over-literal in the JSON artifact.

---

## VERDICT

**table.column:** `lifetime.origin_fiscal_scenario_2023` is the table the query reads, but the
`remit_per_adult` value is NOT a stored column — it is the inline literal `66237847600/436819`
in `theories_tested.duckdb_test`. The denominator literal equals the stored column
`origin_fiscal_scenario_2023.weighted_adults` (= `context.acs_origin_national_2023.weighted_adults`).

**Source of the bug (the literal):** `research/.mining/immigration-lifetime-cluster-m-annual-bridge.json`,
`theories_tested[1].duckdb_test`. Copied into the warehouse by
`infra/immigration-fiscal/build/build_lifetime_evidence_warehouse.py:341`.

**Source of the denominator column:** `infra/immigration-fiscal/build/build_immigration_warehouse.py:138-146`
(the `acs_origin_national_2023` CREATE), fed by the `qual_person` filter at lines **119-135**.

**Root cause (one sentence):** TWO compounding errors — (a) the numerator $66.24B is Mexico's
TOTAL worldwide inbound personal remittances (a national total, not US-origin and not per-adult),
and (b) it is divided by 436,819, which is not even the full US-Mexican adult population but a
narrow recent-arrival/low-skill/prime-age slice (the true broad adult count is ~8.52M) — so the
"$151,636 per adult" is a national-total numerator over a ~5% subsample denominator, inflated ~19.5×
beyond even a per-(broad-adult) figure, and the per-adult framing is conceptually invalid regardless.

**Correct per-adult value:**
- If you insist on the per-adult ratio with the 8.52M broad-adult denominator: $66,237,847,600 / 8,520,718 ≈ **$7,774/adult**.
- More defensible still: the ~$66.2B is total inbound to Mexico from ALL countries; the US-origin
  share is ~95% (most Mexican remittances come from the US), so US-origin ≈ $63B; divided by the
  broad ~8.52M Mexican foreign-born adults ≈ **$7,400/adult**, and divided by the larger total
  Mexican-born US population (~10.5–11M incl. those arrived pre-2014) ≈ **$5,700–6,000/adult**.
- The "~$2,000–5,000 expected" target is per *remittance-sending* immigrant or per *total Mexican-born
  person* (incl. children/non-senders); the headline number's order-of-magnitude error is the
  denominator (~437K vs millions), worth ~19.5×.

**Precise fix (READ-ONLY — not applied):**
File `research/.mining/immigration-lifetime-cluster-m-annual-bridge.json`,
`theories_tested[1].duckdb_test`. Replace the hardcoded denominator `436819` with the broad
Mexican adult population. One-line form:
```sql
SELECT 66237847600 / (SELECT SUM(weighted_adults)
                      FROM context.acs_origin_household_federal_microsim_2023
                      WHERE origin_label='Mexico') AS remit_per_adult,
       avg_federal_net
FROM lifetime.origin_fiscal_scenario_2023 WHERE origin_label='Mexico';
```
This yields ~$7,774/adult. (Deeper fix, out of scope for a one-liner: scale the numerator by the
US-origin share ~0.95 and choose the denominator that matches the comparison population, since
`avg_federal_net` in the same row is computed over the 8.52M microsim base — so the denominators
should match for the comparison to be apples-to-apples.)

**STATUS: COMPLETE.**
