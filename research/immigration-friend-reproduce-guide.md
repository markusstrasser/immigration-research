# Immigration research — friend reproduce guide

**Purpose:** Read the reasoning in order, know which claims are canonical vs superseded, and rerun the headline SQL. **Setup/quickstart now lives in the root [`README.md`](../README.md)** — this is the deep companion (reading order, claim status, warehouse query definitions).

**Date:** 2026-06-24

---

## 1. What you are reproducing

This is **not** one scalar answer (“immigration is good/bad”). It is:

1. A **single warehouse** `immigration.duckdb` — all the cleaned/joined panels in one file, schema-namespaced (`context` / `lifetime` / `fiscal`), with a self-describing `_catalog`. (Built by merging the three per-domain warehouses below.)
2. The per-domain inputs: `immigration_context.duckdb` (ACS/CPS/SIPP panels), `immigration_lifetime_evidence.duckdb` (NPV/lifetime), `immigration_fiscal_union.duckdb` (tensor + cross-domain views)
3. A **memo stack** in `research/immigration-*` with explicit confidence tiers and supersession notes

Read `notes/llm-bias-caveat.md` before treating any synthesis as neutral.

## 1a. Fastest path — download the data (no 50 GB rebuild)

If you just want to query the data, grab the packaged release instead of running the
acquisition pipeline:

```bash
# from a GitHub Release (if published): immigration-data-v<date>.tar.gz (~15 MB)
tar xzf immigration-data-v*.tar.gz && cd immigration-data-v*
shasum -a 256 -c SHA256SUMS                                  # verify integrity
duckdb immigration.duckdb "SELECT * FROM _catalog ORDER BY n_rows DESC"
```

The tarball carries `immigration.duckdb`, per-table Parquet, `DATA_DICTIONARY.md`, the
query pack, and checksums. Maintainer stages it with `reproduce.sh package`. Rebuild from
source only if you need to re-derive or extend the panels (§2).

---

## 2. Machine setup (30 min + download time)

**Setup is in the root [`README.md`](../README.md) → "Rebuild from source":** `init` → `doctor` →
playwright install (only for HUD CHAS + SAFMR, which are WAF-blocked on plain curl) →
`all minimal` (~2 GB, core warehouse) or `all standard` (~50 GB, full public stack).

**Outputs:**

| Artifact | Path |
|----------|------|
| **Unified warehouse (query this)** | `warehouse/immigration.duckdb` |
| Core warehouse | `warehouse/immigration_context.duckdb` |
| Lifetime evidence | `warehouse/immigration_lifetime_evidence.duckdb` |
| Fiscal union (tensor + views) | `warehouse/immigration_fiscal_union.duckdb` |
| Raw data | `$PNY_DATA_ROOT` (default `~/research-data/immigration-fiscal/data`) |

`build all` ends by producing `immigration.duckdb`; rebuild just that with
`./scripts/reproduce-immigration-data.sh build unified` (or `infra/.../reproduce.sh build unified`).

Paths are in `infra/immigration-fiscal/acquire/config.local.env` (gitignored).

**Smoke test:**

```bash
./scripts/reproduce-immigration-data.sh smoke
```

---

## 3. Rerun headline numbers

```bash
./scripts/reproduce-immigration-data.sh query        # all checked-in SQL
./scripts/reproduce-immigration-data.sh query union  # fiscal union queries only
./scripts/reproduce-immigration-data.sh query life   # CDC mortality anchor (lifetime DB)
```

Query pack: `queries/immigration/`. Each file has a `-- requires:` header and `-- backs:` memo pointer.

---

## 4. Reading order (reasoning)

### Start here (2–3 hours)

| Order | File | Why |
|-------|------|-----|
| 1 | `immigration-main-question-reset.md` | What question the repo actually asks |
| 2 | `immigration-glossary.md` | Terms: `low-skill`, `incidence`, `PUMA`, etc. |
| 3 | `immigration-confidence-ladder.md` | Strong vs weak vs contextual-only metrics |
| 4 | `immigration-verified-findings-report-2026-04-10.md` | Best single “what we know” snapshot |
| 5 | `immigration-conclusion-audit-running-fixes.md` | What changed in June 2026 (read before citing numbers) |

### Fiscal / distribution layer (if that’s the hook)

| File | Topic |
|------|-------|
| `immigration-federal-distribution-findings-2026-06-15.md` | Mexico vs NH-white federal proxy decomposition |
| `immigration-country-fiscal-tensor-2026-06-15.md` | Tensor architecture + rollup views |
| `immigration-school-burden-per-adult-2026-06-15.md` | School $/adult — **origin rows now withheld** |
| `immigration-mexico-npv-population-synthesis-2026-06-15.md` | Mexico NPV × population (full ledger stack) |

### Local burden / housing

| File | Topic |
|------|-------|
| `immigration-local-burden-puma-layer.md` | PUMA rent exposure by origin |
| `immigration-household-weighted-correction.md` | Why household WGTP correction matters |
| `immigration-net-negative-dataset-frontier-2026-06-15.md` | Stage-5 cost datasets (SAFMR, SNAP, Medicaid, EL) |

### Deep / historical (read with caution)

| File | Status |
|------|--------|
| `immigration-sweep-cycles-23-32-2026-06-15.md` | Full protocol sweeps — **partially superseded** (see audit memo) |
| `immigration-sweep-cycles-13-22-2026-06-15.md` | **Do not cite** old `$771/+748` origin school/net rows |
| `immigration-lifetime-unified-theory-2026-06-15.md` | Living synthesis — update after each sweep |

---

## 5. Canonical vs superseded claims

| Claim surface | Status | Use instead |
|---------------|--------|-------------|
| April Texas/CPS federal prototype | Superseded | SIPP-style `acs_*_federal_microsim_2023` tables |
| Origin `school_per_adult` / `net_crude` in `v_three_layer_annual` | **Withheld** for Mexico/EU origins (June 2026 guard) | `nh_white_usborn` school row only; see school-burden memo |
| Sweep cycles 13–22 origin fiscal rows | Superseded | `v_three_layer_annual` + audit memo |
| “Low-skill” in warehouse | Operational = `SCHL < 16` + `YOEP >= 2014` + ages 25–64 | Not “all non-college” |
| NAS 2017 full PDF | Partial excerpt mined | `life.npv_education_benchmarks` — treat as benchmark not verdict |
| Clark poll “economists agree” | Scope-limited | `immigration-economist-effects-matrix.md` |

### Added since June 2026 (canonical)

| Surface | What | Memo · table |
|---------|------|--------------|
| Borjas supply-shock cells | <HS immigrant share 9.8% (1980) → 40.8% (2023), education×experience | `immigration-borjas-supply-shock-panel-2026-06-23.md` · `borjas_supply_shock_panel` |
| Source-incentive re-grade | advocacy discounted on **both** sides; against-interest up-weighted | `immigration-source-incentive-regrade-2026-06-23.md` · `source_incentive_grades` |
| Fiscal+welfare ledger map | "positive vs negative?" decomposed into 4 coordinates × the full ledger | `immigration-fiscal-welfare-ledger-map.md` |

---

## 6. Warehouse definitions (for SQL)

**Recent low-skill adults** (`qual_person` view):

- Foreign-born (`NATIVITY = 2`)
- Ages 25–64
- `SCHL < 16` (less than HS diploma in ACS coding)
- `YOEP >= 2014` (entered 2014 or later)

**Federal annual proxy** (narrow ledger):

- FICA 7.65% on wages (capped) minus SNAP + TANF + SSI
- **Not** income tax, Medicare, Medicaid, EITC, or lifetime NPV

**Three-layer view** (`v_three_layer_annual` in fiscal union):

- `federal_per_adult`, `school_per_adult`, `net_crude_per_adult`
- Origin school/net may be `NULL` — check audit memo before exporting

**Borjas supply-shock panel** (`borjas_supply_shock_panel`, in `context` + the unified release):

- IPUMS USA 5% samples 1980–2023, education × work-experience cells
- Foreign-born = `BPL >= 150` (IPUMS birthplace coding) — **not** ACS `NATIVITY = 2`; the two come from different microdata, don't conflate
- The 44 M-row source microdata is **license-restricted and excluded from the release** — only these aggregated cells ship

---

## 7. What is still manual / not reproducible

| Gap | Impact |
|-----|--------|
| EDFacts FS141 EL 2022–23 | ACS school-age foreign-born + CCD 2018–19 substitute; Ed Data Express bot-blocked |
| TRAC court backlog CSV | EOIR pending/receipts/completions (`context_09`) |
| PSID / Synthetic SIPP / FSRDC LEHD | Application-gated — `applications/MANUAL_ACQUIRE.md` |
| Crime/frontier — CBO Emergency Medicaid, OECD IMO | hard-403 WAF — `crime_frontier/MANUAL_ACQUIRE.md` |
| Crime/frontier — ICPSR/openICPSR (Light TX, Abramitzky, BJS SPI/NCRP, AZ, NIS) | free login + DUA click-through; exact study IDs in `crime_frontier/MANUAL_ACQUIRE.md` |

**Now scripted:** SSA→CDC mortality, KFF→CMS+ACS, EL 2018–19 CCD, SAIPE poverty, ACS school-age proxy, NAS PDF, SAFMR, SNAP, receiver cities; **crime/frontier (2026-06-24): DOJ SCAAP, ICE ERO FY23/24, ORR ARC** (`setup-crime-frontier.sh`, folded into `all`); Census ABS owner-nativity via API key.

Lists after download: `$PNY_DATA_ROOT/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md` · `$PNY_DATA_ROOT/external/crime_frontier/MANUAL_ACQUIRE.md`

---

## 8. Share checklist (Markus → friend)

- [ ] Friend has git access to this repo
- [ ] Friend ran `all standard` (or you share `warehouse/*.duckdb` + derived CSVs)
- [ ] Friend read sections 4–5 of this guide
- [ ] Friend ran `./scripts/reproduce-immigration-data.sh query`
- [ ] Friend knows which memos are **superseded** before debating headline numbers

---

## 9. Pointers

| Resource | Path |
|----------|------|
| Data pipeline detail | `infra/immigration-fiscal/REPRODUCE.md` |
| Dataset catalog | `research/immigration-dataset-register.md` |
| Topic index | `research/immigration-INDEX.md` |
| Agent handoff (dense) | `research/immigration-verification-handoff.md` |
| SQL query pack | `queries/immigration/` |
