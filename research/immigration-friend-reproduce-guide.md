# Immigration research — friend reproduce guide

**Purpose:** Clone the repo, rebuild the data stack, read the reasoning in order, rerun the headline SQL checks.

**Date:** 2026-06-18

---

## 1. What you are reproducing

This is **not** one scalar answer (“immigration is good/bad”). It is:

1. A **warehouse** of ACS/CPS/SIPP-linked panels (`immigration_context.duckdb`)
2. A **fiscal union** with education-matched federal proxy + lifetime NPV bridges (`immigration_fiscal_union.duckdb`)
3. A **memo stack** in `research/immigration-*` with explicit confidence tiers and supersession notes

Read `notes/llm-bias-caveat.md` before treating any synthesis as neutral.

---

## 2. Machine setup (30 min + download time)

**Requirements:** macOS/Linux, `bash`, `curl`, `unzip`, [uv](https://docs.astral.sh/uv/), ~50 GB disk for full stack (~2 GB for minimal).

```bash
git clone git@github.com:markusstrasser/research.git
cd research

./scripts/reproduce-immigration-data.sh init
./scripts/reproduce-immigration-data.sh doctor

# Playwright — needed for HUD CHAS + SAFMR (WAF-blocked on plain curl)
uv run --with playwright python -m playwright install chromium

# Pick one:
./scripts/reproduce-immigration-data.sh all minimal    # ~2 GB, core warehouse only
./scripts/reproduce-immigration-data.sh all standard  # ~50 GB, full public stack (recommended)
```

**Outputs:**

| Artifact | Path |
|----------|------|
| Core warehouse | `warehouse/immigration_context.duckdb` |
| Lifetime evidence | `warehouse/immigration_lifetime_evidence.duckdb` |
| Fiscal union (tensor + views) | `warehouse/immigration_fiscal_union.duckdb` |
| Raw data | `$PNY_DATA_ROOT` (default `~/research-data/immigration-fiscal/data`) |

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

---

## 7. What is still manual / not reproducible

| Gap | Impact |
|-----|--------|
| EDFacts FS141 EL 2022–23 | NCES CCD EL newest zip is **2018–19**; Ed Data Express export is JS-gated |
| TRAC court backlog CSV | EOIR PDFs scripted; no stable TRAC bulk download |
| PSID / Synthetic SIPP / FSRDC LEHD | Application-gated — `applications/MANUAL_ACQUIRE.md` |

**Now scripted:** SSA→CDC mortality, KFF Medicaid→CMS, KFF health charts→ACS PUMS, EL 2018–19 CCD, NAS PDF, SAFMR, SNAP, receiver cities.

Lists after download: `$PNY_DATA_ROOT/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md`

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
