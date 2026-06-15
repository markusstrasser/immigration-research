# Country fiscal tensor — built stack (2026-06-15)

**DuckDB:** `warehouse/immigration_fiscal_union.duckdb`
**Build:** `infra/immigration-fiscal/build/build_country_fiscal_tensor.py`
**CSV exports:** `build/stage3_proto/country_fiscal_rollup_2023.csv`, `annual_npv_bridge_grid.csv`, `three_layer_annual_2023.csv`
**Frame:** cell × ledger × effect_order — **no scalar country NPV.**

---

## What was built

| Artifact | Role |
|----------|------|
| `country_fiscal_tensor` | Long-format facts: population × education × fiscal_layer × order |
| `v_country_fiscal_rollup` | Weighted totals / per-adult |
| `v_country_fiscal_compare` | NH white vs Mexico (matched layers) |
| `annual_npv_bridge_grid` | NAS NPV annuitized vs SIPP federal annual — scope check |
| `ge_wage_fan_scenarios` | 2nd-order earnings multipliers (Borjas / Card-Peri) |
| `cbo_fiscal_objects` | 3rd-order surge cohort (federal + state/local) |
| `acs_nh_white_federal_microsim_2023` | **New** — SIPP US-born donors × ACS NH white persons |
| `sipp_household_donor_cells_usborn_2024` | US-born donor cells |

**Reproduce:**
```bash
cd infra/immigration-fiscal
bash rebuild.sh                    # context + native microsim (HISP='01' fix)
bash rebuild_lifetime_warehouse.sh # lifetime + tensor union DB
```

---

## Rollup anchors [SOURCE: `v_country_fiscal_rollup`]

### Federal annual (1st order, $/adult weighted)

| Population | Per adult/yr | Total proxy/yr |
|------------|--------------|----------------|
| UK-origin | **~$5,486** | — |
| **EU27-origin** | **~$4,695** | — |
| NH white foreign-born | **~$3,898** | — |
| NH white all | **~$2,803** | — |
| NH white US-born | **~$2,746** | **~$253B** |
| US foreign-born stock | **~$3,003** | **~$101B** |
| Mexico-origin | **~$1,519** | **~$12.9B** |
| FB `<HS` pooled | **~$677** | — |

**Key ratios:** EU27/Mexico **~3.1×**; EU27/NH white US-born **~1.7×**; NH white/Mexico **~1.8×**. Full write-up: `immigration-europe-caucasian-fiscal-findings-2026-06-15.md`.

### Synthetic age-25 NPV benchmark (1st order, NAS education cells × weights)

| Population | Per adult (weighted) | Synthetic total |
|------------|---------------------:|----------------:|
| Mexico-origin | **~+$45.6k** | **~+$387.7B** |
| MX + N. Triangle | **~+$43.0k** | **~+$476.1B** |
| US FB stock | **~+$212.5k** | **~+$7.14T** |
| FB `<HS` pooled | **−$109k** | **−$837.9B** |

These are **not** measured lifetime NPVs for the current resident stock. NAS Table 8-13 follows an immigrant entering at age 25; this tensor applies those age-25 education cells to ACS current-stock weights because the warehouse lacks a full age-at-arrival × current-age × education NPV path. Use as a composition benchmark only. [SOURCE: `v_country_fiscal_rollup`; NAS 2017 Table 8-13] [INFERENCE]

### Synthetic age-25 NPV benchmark (2nd order — Clemens capital-tax on `<HS` only)

| Population | Per adult | Total |
|------------|-----------|-------|
| US FB `<HS` slice | **+$128k** | **+$984B** |

Sign flip on same education cell — GE layer only.

### 3rd order (country objects, not per-adult)

| Object | Total |
|--------|-------|
| CBO surge federal (2024–34) | **−$897B** deficit vs no-surge [SOURCE: CBO 60569 memo] |
| CBO surge state/local direct | **+$9.2B** (2023) |
| Receiver cities episodic FY2024 | **~$5.1B** (NYC+Chicago sample) |

### Local flow (1st order)

| Population | Metric |
|------------|--------|
| Mexico-origin | **~$20,907/pupil** area-weighted (not marginal) |

---

## Annual ↔ lifetime bridge

All education rows: **`scope_mismatch`** — annuitized NAS `<HS` (−$109k) vs federal annual (+$677 FB-pooled) are **incommensurable ledgers**, not a sign contradiction. [SOURCE: `annual_npv_bridge_grid`]

---

## Known limitations

1. **NH white `<HS` cell** shows negative federal proxy (−$7.5k) — noisy SIPP US-born transfer donor; **college+ dominates** rollup (+$5.5k/adult).
2. **Lifetime tensor** not yet rolled for `nh_white_usborn` (weights exist in microsim; NAS join pending).
3. **LPR dynamic weights** — xlsx sketch empty (parse); manual pass needed.
4. Proxy = FICA − SNAP/TANF/SSI only — not income tax or Medicare.
5. Synthetic age-25 NPV benchmarks are not current-stock remaining-lifetime estimates.

---

## Next

- Add `nh_white_usborn` lifetime_npv rows to tensor (ACS education weights × NAS).
- Cap NH `<HS` transfer donor or winsorize before rollup.
- MEPS health + remittance layers as separate ℓ rows.
