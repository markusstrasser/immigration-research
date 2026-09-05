# Scenario composition — corrected model status

**Current correction: 2026-09-05.** The SIPP, payroll and health-bridge scenario exports have been rebuilt; see the [repair report](immigration-material-repair-report-2026-09-05.md). Person-month averages annualized by twelve are steady-state illustrations, not person-year tax liabilities; the repaired donor model uses annual person earnings before caps. Household SNAP/TANF ownership and benefit membership are reconciled before assigning an adult share. The MEPS bridge is a statistical match by its supported cells, not observed joint SIPP–MEPS microdata. Coarse matching imposes conditional exchangeability and cannot establish origin-specific or education-specific health spending it does not observe. The old bridge also shifted some five-year age bands into the next ten-year MEPS band; those boundaries are repaired. The origin scenario subset and full adult recipient stock remain different universes.

[SOURCE: [material audit](immigration-conceptual-audit-2026-09-05.md), source-code and table checks recorded in the [repair report](immigration-material-repair-report-2026-09-05.md)] [INFERENCE: accounting and identification limits]

The [repair report](immigration-material-repair-report-2026-09-05.md) is the current result and verification entry point. The original below is retained as explicitly superseded history, including original quotations and earlier revisions.

## Revisions

- **2026-09-05:** Corrected these units, assumptions and current-status claims under the [material inference repair decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical version — retained for provenance</summary>

# Immigration scenario composition — 2026-06-15

## Purpose

First integrated **scenario ledger** joining federal (SIPP donor), health (SIPP→MEPS), and local-cost (stage2+5) channels. This is an input layer for cell-level reasoning — **not** a scalar net-negative verdict. [FRAMING-SENSITIVE]

## Built artifacts

| Output | Rows | Builder |
|--------|------|---------|
| `derived/stage5/state_stage5_context_2023.csv` | 60 states/territories | `build_stage5_local_cost_context.py` |
| `derived/stage5/state_el_lep_2018.csv` | 56 | NCES CCD 2017-18 EL anchor |
| `derived/stage3_proto/sipp_scenario_ledger_2024.csv` | 98 | `compose_scenario_ledger.py` |
| `derived/stage3_proto/origin_fiscal_scenario_2023.csv` | 151 | same |

DuckDB tables added: `state_stage5_context_2023`, `state_el_lep_2018`, `receiver_city_migrant_costs`, `origin_puma_household_stage5_context_2023`.

## Stage-5 inputs integrated

| Source | Use |
|--------|-----|
| BEA RPP Table 2 (2023) | `rpp_all_items_2023` by state — deflate/compare local costs |
| CMS Medicaid financial management | `medicaid_total_computable` by state (latest year in file: 2016) [SOURCE: local CSV] |
| NCES CCD EL 2017-18 | `lep_count_reported` by state — school-service intensity anchor |
| Receiver-city costs CSV | Documented shelter/migrant spend shocks (NYC, Chicago, …) |

Census gov finances 2022 individual-unit zip acquired to `stage5/census/` — not yet parsed into warehouse.

## Scenario ledger logic

### SIPP cells (`sipp_scenario_ledger_2024.csv`)

Per 98 working-age SIPP profile cell:

1. Monthly `TPEARN` → annual earnings
2. SNAP/TANF/SSI monthly → annual transfers
3. `sipp_meps_expected_health_cost_cells_2024` → `expected_mean_totexp23`, `expected_mean_totmcd23`
4. Education bucket mapped to ACS → SIPP federal donor proxies (`federal_net_proxy_annual_edu_bucket`, payroll, transfers)

### Origin rows (`origin_fiscal_scenario_2023.csv`)

Per origin (recent low-skill 25-64 adults from warehouse filter):

1. `acs_origin_national_2023` stock weight
2. Household structure from `acs_origin_household_national_2023`
3. PUMA-area-weighted school spend + housing stress (stage2)
4. State RPP + Medicaid + EL (stage5, PUMA→state join)
5. Origin-weighted federal microsim from `acs_origin_household_federal_microsim_2023`

Example — Mexico: `weighted_adults` ≈ 436,819 for the origin scenario subset; `avg_federal_net` ≈ +$1,519/yr (payroll proxy > transfer proxy at matched donor cells); `area_wtd_current_spend_per_pupil` ≈ $20,907 after the F-33 thousands fix. Do **not** use the 436,819 scenario subset as the denominator for full Mexico-origin adult stock, and do **not** pair its household school numerator with the full microsim adult denominator. [SOURCE: `origin_fiscal_scenario_2023`; `v_three_layer_annual`; `immigration-conclusion-audit-running-fixes.md`]

## Disconfirmation (mandatory)

1. **Federal-positive at cell level does not imply overall net positive** — CBO 60569 macro channel; local shelter/school shocks (receiver CSV) can dominate for selected cities.
2. **MEPS health costs lower for foreign-born working-age** — weakens naive Medicaid-drain story [SOURCE: `meps_health_cost_module_2023.csv`].
3. **CMS Medicaid file is 2016 and undifferentiated by nativity** — state denominator only.
4. **EL counts are 2017-18** — not current 2023-24 district EL (still blocked).
5. **School spend per pupil in scenario table** uses area-weighted county F-33 — the unit is now fixed, but per-pupil values still require a separate children-per-adult bridge before any per-adult welfare conclusion.

## Reproduce

```bash
cd infra/immigration-fiscal
bash acquire/setup.sh
bash build-context.sh          # stage1+2+5 + federal microsim
bash build-mvp.sh      # SIPP/MEPS cells (if not already built)
# compose runs at end of build-context.sh
```

## Next integration targets

1. Parse Census gov-finances 2022 zip → state/local expenditure categories
2. EDFacts / current EL when acquirable
3. Receiver-city flags joined to PUMA/county nodes (not just standalone table)
4. Explicit offset column from CBO PDF tables (manual extract)

</details>
