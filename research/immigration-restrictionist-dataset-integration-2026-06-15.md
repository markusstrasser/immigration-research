# Restrictionist papers → datasets → DB integration map (2026-06-15)

**Question:** After full read of 9 restrictionist papers, which datasets can we get and wire into the immigration DuckDB stack?

**Frame:** Papers cite **different empirical bases** — not one download. Integration target is `immigration_lifetime_evidence.duckdb` + `immigration_context.duckdb` + `immigration_fiscal_union.duckdb` via existing builders in `infra/immigration-fiscal/build/`.

---

## Summary matrix

| Paper | Data the paper actually uses | In DB today? | Can acquire? | Integrate as |
|-------|------------------------------|--------------|--------------|--------------|
| **Borjas w9755** | Census 1960–2000 + CPS; edu×exp cells | Partial (ACS 2023 only) | **Yes** — IPUMS extracts | `borjas_edu_exp_panel` view |
| **Borjas w11610** | Same + state/MSA geography | Partial (ACS + PUMA bridge) | **Yes** — IPUMS + state FIPS | `native_migration_attenuation` join |
| **BGH w12518** | IPUMS 1960–2000; 160 national cells; group quarters | **No** incarceration panel | **Yes** — IPUMS multi-decennial | `bgh_skill_race_outcomes` |
| **Gould w33655** | HUD PIT; local admin (NYC/CHI/MA/Denver); CBP parole | Partial (receiver CSV, threshold memos) | **Yes** — HUD + OHSS | `hud_pit_coc`, `gould_asylum_attribution` |
| **Orrenius wp1704** | NAS 2016 Tables 8-2/8-12/8-13; March CPS | **Yes** (NAS cells, claims) | Tables in staged NAS PDF | Already in `parameter_claims` / tensor |
| **Razin w15597** | Theory + NRC 1997 fiscal cites | Claims only | N/A (theory) | `parameter_claims` only |
| **Razin-Wahba w17515** | OECD SOCX; Docquier bilateral stocks; EUR migration | **No** | **Yes** — OECD + Docquier | `oecd_welfare_spending`, `bilateral_migration_stocks` |
| **Hanson w23753** | Census/ACS/CPS; Mexico census; UN WPP; IMF; DHS | Partial (ACS, OHSS, CBP budgets) | **Yes** — UN WPP, IMF, Mexico IPUMS | `low_skill_supply_forecast` |
| **Borjas w6175** | NLSY 1979–89; 1980 Census ethnic capital | **No** | **Yes** — NLSY (register) | `nlsy_welfare_ethnicity` (restricted-lite) |

---

## Already integrated (use now)

| Asset | Warehouse table / view | Serves which paper claims |
|-------|------------------------|---------------------------|
| NAS education NPV | `country_fiscal_tensor`, lifetime NAS cells | Orrenius, restrictionist F1 |
| ACS 2023 PUMS + origin | `acs_person_raw`, `country_fiscal_tensor`, microsim | Hanson stock; Mexico mix |
| Receiver city costs | `receiver_city_migrant_costs` | Gould fiscal; C1 local |
| School burden | `v_three_layer_annual`, school finance joins | Orrenius S&L school |
| ITEP / CBO / Saiz | lifetime evidence layers | Disconfirmation vs FAIR |
| EOIR + QWI (causal repo) | `sources/immigration-causal/` | Admin chain A1; not BGH |
| Mining JSON → claims | `parameter_claims`, `lifetime_generators` | All 9 papers (~220 claims) |
| Marker-modal full text | `~/Projects/corpus/sha_*` | Citation / re-extract |

**Gap:** Claims from full extract are in memos + `.mining/` but **not all 220 rows loaded** into `parameter_claims` yet — one `build_lifetime_evidence_warehouse.py` reload fixes that.

---

## Tier A — Acquire next (automatable, highest leverage)

### 1. HUD Point-in-Time / AHAR by CoC (Gould)

- **Gets:** Sheltered vs unsheltered by CoC 2007–2024; Hispanic share breaks; replicate 59–62% band.
- **Source:** [HUD AHAR Part 1](https://www.huduser.gov/portal/datasets/ahar.html) CSV exports.
- **DB:** `hud_pit_coc_annual(coc_id, year, sheltered, unsheltered, hispanic_share, …)`
- **View:** `v_gould_episodic_ledger` joined to `receiver_city_migrant_costs`.
- **Generator:** G-LIF-S10.

### 2. OHSS / CBP parole & encounters monthly (Gould + Hanson)

- **Gets:** Parole timing vs PIT dates (Fig 2 in Gould); post-2007 flow slowdown.
- **Source:** Already partially in `external/origin/ohss/`; extend with OHSS book-out tables.
- **DB:** `ohss_parole_monthly` → join `immigration_context` origin flows.

### 3. Gould Table 1 machine extract (from parsed PDF)

- **Gets:** Direct/indirect asylum counts per city (NYC 66,700, etc.) without re-scraping.
- **Source:** `corpus/sha_73e2279cb366d94b` + manual QA.
- **DB:** `gould_asylum_shelter_attribution_2022_2024` → `parameter_claims` S-007 series.

### 4. IPUMS USA multi-decennial extract (Borjas + BGH)

- **Gets:** Replicate national edu×exp wage regressions; BGH wage/employment/incarceration by race.
- **Source:** IPUMS extract (1960, 1970, 1980, 1990, 2000, ACS) — men 18–64, GQTYPE, weeks worked.
- **Cost:** ~2–4 GB extract; build script ~200 LOC.
- **DB:** `bgh_outcomes_cell` / `borjas_supply_shock_cell` in `immigration_context` or separate analytic DB.
- **Generators:** G-LIF-S06–S09.

### 5. OECD SOCX + Docquier-Mar fouk bilateral stocks (Razin-Wahba)

- **Gets:** Welfare spending % GDP; EUR vs non-EUR skill-mix test (magnet vs fiscal burden).
- **Source:** OECD SOCX CSV; Docquier & Marfouk (2006) or updated bilateral DB.
- **DB:** `oecd_social_spending_host`, `bilateral_migration_stocks` → cross-country panel (not US Mexico rollup).

### 6. UN WPP + IMF GDP (Hanson long-run)

- **Gets:** Mexico/Latin America cohort ratios; 2040 stock forecast; income-gap compression.
- **Source:** UN Population API; IMF WEO or FRED.
- **DB:** `demographic_push_forecast` → disconfirm "flooding" rhetoric (G-LIF-S14).

---

## Tier B — Manual / registration (worth it, not curl-only)

| Dataset | Paper | Blocker | DB target |
|---------|-------|---------|-----------|
| **NLSY79** | w6175 | Registration | `nlsy_afdc_ethnicity` — 80% transmission test |
| **NYC Comptroller asylum census** | Gould direct | PDF/dashboard | `nyc_asylum_shelter_census` |
| **EDFacts FS141 EL 2022–23** | Orrenius school | Interactive export | Upgrade NCES EL 2017–18 anchor |
| **HUD CHAS Table 11** | Housing stress | WAF | `chas_puma_rent_burden` (Playwright script exists) |
| **Mexico IPUMS / MxFLS** | Hanson selection | Separate extract | `mexico_selection_diagnostic` |

---

## Tier C — Blocked or low ROI for restrictionist stack

| Dataset | Why skip for now |
|---------|------------------|
| LEHD person-level | FSRDC; QWI county already covers labor margin |
| IRS SOI PUF | Restricted; SIPP microsim done |
| PSID | Registration; NAS descendants sufficient for lifetime |
| FAIR 2023 micro-ledger | Advocacy; no reproducible tables |
| EU A8 micro (Dustmann) | Razin cites for background only; US stack separate |

---

## Integration architecture (no new scalar)

```
external/{hud,ohss,oecd,ipums}/     ← acquire scripts (extend setup-lifetime.sh)
        ↓
build/build_*_restrictionist.py     ← new thin builders (one per tier-A source)
        ↓
immigration_context.duckdb          ← panels (PIT, edu×exp, bilateral)
immigration_lifetime_evidence.duckdb ← parameter_claims + generators reload
immigration_fiscal_union.duckdb     ← v_full_fiscal_stack = lifetime + episodic + labor ℓ
```

**Priority order** (closes most paper gaps per LOC):

1. Reload **220 claims** from `.mining/` into `parameter_claims`
2. **Gould Table 1 CSV** + HUD PIT CoC history
3. **IPUMS Borjas/BGH panel** (single extract, two builders)
4. OECD + Docquier (Razin-Wahba regime test)
5. UN WPP (Hanson secular decline anchor)

---

## What you cannot get from these papers alone

- **Black incarceration causal panel** without IPUMS group-quarters (Tier A #4).
- **BGH state+national regression** without building the 8,160 state cells.
- **Razin strategic voting** — theory only; no dataset.
- **Scalar "restrictionist net fiscal"** — papers explicitly forbid it (layer multiplication).

---

## Reproduce after integration

```bash
cd infra/immigration-fiscal
bash acquire/setup-lifetime.sh          # papers already staged
# + new: bash acquire/setup-restrictionist-panels.sh  (proposed)
bash rebuild_lifetime_warehouse.sh
uv run --with duckdb,pandas python build/build_country_fiscal_tensor.py
```

---

## Revisions

- **2026-06-15:** Initial map from full section read of 9 marker-modal parses.
