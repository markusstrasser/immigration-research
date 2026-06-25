# DuckDB Test Diagnosis — Clusters A, E, K, T

**Status: COMPLETE.** Read-only. All `corrected_sql` below were executed against the live warehouse and return rows. The 4 E-cluster tests are confirmed UNBUILT by an exhaustive negative column/table check (zero occurrences). I did NOT edit `theories_tested` or any cluster JSON — you apply the fixes.

## Setup used
- `uv run --with duckdb python3`, connect read_only to `warehouse/immigration.duckdb`
- `ATTACH .../immigration_microdata.duckdb AS md (READ_ONLY)`
- Substitution applied first: `ctx.`->`context.`, `life.`->`lifetime.`
- After substitution, exactly **11 of 15** A/E/K/T tests still error (matches brief). The 4 that pass post-substitution and need no change: A "Capital-tax adjustment flips sign", A "Education bucket is sufficient statistic", A "Indirect annual incidence (Colas-Sachs)", T "Falling mean education / md.ipums_usa_borjas_panel".

## Schema note (bare table names)
`current_schema` is `main`; `search_path` is empty. The `main` schema mirror-holds every table that also lives in the typed `context`/`lifetime`/`fiscal` schemas, so bare-name references (K#11/K#12 had no prefix) resolve via `main`. The corrected_sql below use explicit `context.`/`lifetime.`/`fiscal.` prefixes for clarity; bare names also work for the K tests.

---

## Fix-list table

| cluster | theory (short) | verdict | missing object | corrected_sql (full runnable) |
|---------|----------------|---------|----------------|-------------------------------|
| A_npv_generational | Annual federal proxy correlates with lifetime NPV rank across education buckets | **FIXABLE** | `ctx.public_mvp_federal_by_education` (never existed) + `e.weighted_total` (col is `weighted_adults`) | `SELECT f.education_bucket, e.weighted_adults AS acs_stock, AVG(f.federal_net_proxy_annual) AS annual_federal_net_proxy, b.individual_npv_2012_usd, b.study FROM context.acs_foreign_born_education_bucket_totals_2023 e JOIN fiscal.v_origin_federal_with_education_npv f ON e.education_bucket=f.education_bucket LEFT JOIN lifetime.npv_education_benchmarks b ON e.education_bucket=b.acs_education_bucket WHERE b.study='NAS 2017' GROUP BY f.education_bucket, e.weighted_adults, b.individual_npv_2012_usd, b.study ORDER BY f.education_bucket` |
| A_npv_generational | No single origin_label scalar maps to lifetime NPV | **FIXABLE** | `ctx.origin_education_composition` (never existed) | `WITH comp AS (SELECT origin_label, education_bucket, SUM(weighted_adults) AS wa FROM context.acs_origin_household_federal_microsim_2023 GROUP BY origin_label, education_bucket) SELECT m.origin_label, m.education_bucket, m.wa / SUM(m.wa) OVER (PARTITION BY m.origin_label) AS share, b.individual_npv_2012_usd FROM comp m JOIN lifetime.npv_education_benchmarks b ON m.education_bucket=b.acs_education_bucket WHERE b.study='NAS 2017' ORDER BY m.origin_label, m.education_bucket` |
| A_npv_generational | Recent-arrival pool NPV exceeds stock-average NPV conditional on education mix | **FIXABLE** | `e.share` col absent (table has `weighted_adults`) — compute share | `WITH tot AS (SELECT SUM(weighted_adults) s FROM context.acs_foreign_born_education_bucket_totals_2023) SELECT b.study, SUM((e.weighted_adults / (SELECT s FROM tot)) * b.individual_npv_2012_usd) AS weighted_npv FROM context.acs_foreign_born_education_bucket_totals_2023 e JOIN lifetime.npv_education_benchmarks b ON e.education_bucket=b.acs_education_bucket WHERE b.study='NAS 2017' GROUP BY b.study` |
| E_housing_rent | FRBSF remittance attenuation does not eliminate inelastic-market rent gradient | **UNBUILT** | `origin_puma_household_context_2023.msa_match_key`, `.foreign_born_share`, `.rent_burden` — none exist; no PUMA->MSA bridge | — (depends on an MSA-joined rent+immigrant panel never built) |
| E_housing_rent | Immigrant-heavy PUMAs map to Saiz inelastic quartile — rent burden ≈ renter welfare loss | **UNBUILT** | `origin_puma_household_context_2023.msa_match_key`, `.rent_to_income_or_burden` — none exist | — |
| E_housing_rent | NAS lifetime NPV omits elasticity-conditional housing wedge — `<HS` understates local renter incidence | **UNBUILT** | `origin_puma_household_context_2023.education_bucket` + `.rent_burden` — neither exists on that table | — |
| E_housing_rent | Regulatory index WRLURI explains elasticity variance beyond topography in gateway MSAs | **UNBUILT** | `saiz_msa_rent_immigrant_2022` (table, incl. `fb_share`) — does not exist | — |
| K_incidence_bridge | County school spend join explains origin scenario per-pupil field | **FIXABLE** | original `ON ..` is a literal unfinished placeholder; both tables exist | `SELECT CORR(s.current_spend_per_pupil, p.current_spend_per_pupil) AS corr_county_perpupil, COUNT(*) AS n_counties FROM lifetime.school_finance_county_2023 s JOIN context.puma_county_context_2023 p ON s.county_fips = p.county_fips` |
| K_incidence_bridge | Receiver cities carry episodic costs larger than annual federal offset for surge cohort | **FIXABLE** | col `cost` -> `total_spending_usd_M` (USD millions) | `SELECT SUM(total_spending_usd_M) AS total_spending_usd_M FROM lifetime.receiver_city_migrant_costs` |
| K_incidence_bridge | State RPP scales federal net proxy differently for border vs gateway states | **FIXABLE** | col `avg_rpp_all_items_2023` -> `rpp_all_items_2023` | `SELECT state_fips, rpp_all_items_2023 FROM lifetime.state_stage5_context_2023 ORDER BY 2 DESC LIMIT 10` |
| T_immigrationist_steelman | The incumbent-fiscal ledger omits the largest welfare term (migrant place premium) | **MALFORMED** | n/a — field is prose, not SQL ("compare border-selection earnings jump (G-LIF-G04 inputs) to life.npv_education_benchmarks magnitudes") | — (rewrite as SQL or move text to a `notes`/`rationale` field; not a `duckdb_test`) |

---

## Detailed findings & rationale

### A-cluster (3 FIXABLE) — all reference renamed/never-built objects but the underlying data exists

- **A#0 (federal proxy ↔ NPV rank):** original joined a nonexistent `ctx.public_mvp_federal_by_education` and used `e.weighted_total` (the column is `weighted_adults`). The federal-net-proxy-by-education concept lives in `fiscal.v_origin_federal_with_education_npv` (col `federal_net_proxy_annual`, keyed origin×education). Corrected SQL aggregates that to education level with `AVG()`, joins the ACS stock totals and `lifetime.npv_education_benchmarks`. Returns 5 rows (the `<HS` bucket legitimately has two NAS-2017 NPV rows: −186k baseline and −109k capital-adjusted). Verified.
- **A#4 (no scalar per origin):** `ctx.origin_education_composition` never existed. The only context table carrying both `origin_label` and `education_bucket` is `context.acs_origin_household_federal_microsim_2023` (at origin×education×age_band×earnings_band granularity). Corrected SQL rolls it up to origin×education and computes a within-origin `share` to match the theory's intent ("reject collapse to one number per origin"). 840 rows. Verified. (If you only want raw rows without the derived share, the un-aggregated form joining the microsim table directly also runs — 12,004 rows.)
- **A#5 (recent-arrival weighted NPV):** `e.share` doesn't exist; computed via a `tot` CTE share over `weighted_adults`. (Note: the table is the *stock* education mix, not a recent-arrival-specific pool — no recent-arrival education table exists, so this tests the stock-weighted NPV; faithful to the data present, but the "recent-arrival" framing in the theory is not separately backed by a table.) Returns weighted_npv ≈ 169,967 for NAS 2017. Verified.

### E-cluster (4 UNBUILT) — depends on an MSA-joined rent + immigrant panel that was never built

Exhaustive negative check (information_schema, whole `immigration` catalog): **0 occurrences** of every column/table these tests need — `msa_match_key` (0), `rent_burden` (0), `rent_to_income` (0), `foreign_born_share` (0), `fb_share` (0), `avg_rent_burden` (0), table `saiz_msa_rent_immigrant_2022` (0). The only elasticity-bearing object is `saiz_msa_elasticity` (keyed on `msaname`, an MSA-name string), and the only geographic crosswalk in the warehouse is `puma_county_area_xwalk_2023` (PUMA→**county**, not PUMA→MSA). `origin_puma_household_context_2023` carries only `{origin_label, state_fips, puma_code, linked_household_wgt, linked_mean_hh_school_age_children, linked_share_households_with_school_age_children_pct}` — no rent, no foreign-born-share, no MSA key, no education_bucket.

These cannot be repaired by a column/schema rename: a join key that doesn't exist can't be aliased into being. To run, the warehouse needs **(a)** a PUMA→CBSA/MSA-name crosswalk (so PUMA rows can attach to `saiz_msa_elasticity.msaname`), **(b)** a `rent_burden`/`rent_to_income` measure and a `foreign_born_share` on the PUMA/origin table, and **(c)** the rolled-up `saiz_msa_rent_immigrant_2022` panel (Saiz elasticity × WRLURI × MSA foreign-born share). Mark all four **pending-data**.

### K-cluster (3 FIXABLE)

- **K#10:** the original literally ends `ON ..` (unfinished placeholder — would also classify MALFORMED as written, but the data exists so it's repairable). Both `school_finance_county_2023` and a county-keyed per-pupil context exist. Corrected SQL correlates NCES county school spend against `puma_county_context_2023.current_spend_per_pupil` on `county_fips`. **CORR returns exactly 1.0** — because `puma_county_context_2023.current_spend_per_pupil` is itself derived from the same NCES `school_finance_county_2023` source, so this confirms the provenance chain feeding `origin_fiscal_scenario_2023.area_wtd_current_spend_per_pupil` (which is keyed on `origin_label` and has no county key, so it cannot be CORR'd directly). If you instead want a non-trivial correlation, this theory may need re-specification against an independent per-pupil series — flag for the cluster author. Query runs and is faithful to the theory text as stated.
- **K#11:** `cost` → `total_spending_usd_M`. SUM = 11,856.9 (USD millions). Verified. (Watch the unit: it's millions, so SUM is ~$11.86B across receiver cities; the theory's "episodic costs vs annual federal offset" comparison should keep the M-scale in mind.)
- **K#12:** `avg_rpp_all_items_2023` → `rpp_all_items_2023`. Returns top-10 states by RPP (CA 112.6, DC 110.8, NJ 108.9, …). Verified.

### T-cluster (1 MALFORMED)

- **T#14:** the `duckdb_test` field contains prose, not SQL: `"compare border-selection earnings jump (G-LIF-G04 inputs) to life.npv_education_benchmarks magnitudes"`. Not executable. Either rewrite as an actual query (the `md.ipums_usa_borjas_panel` + `lifetime.npv_education_benchmarks` ingredients exist for an earnings-jump-vs-NPV comparison) or relocate the prose to a non-test field.

---

## Summary counts
- **FIXABLE: 6** — A#0, A#4, A#5, K#10, K#11, K#12 (all corrected_sql executed successfully)
- **UNBUILT: 4** — all of E_housing_rent (PUMA→MSA crosswalk + rent_burden + foreign_born_share + `saiz_msa_rent_immigrant_2022` panel never built)
- **MALFORMED: 1** — T "incumbent-fiscal ledger omits largest welfare term" (prose, not SQL)
