# Net-negative immigration: dataset frontier

**Date:** 2026-06-15  
**Frame:** User asked for datasets to support a net-negative verdict. Per [immigration-adversarial-review.md](immigration-adversarial-review.md), we cannot honestly claim **overall** net negative yet — but we *can* tighten tests on **local cost channels** and build a **federal tax-transfer microsim** that might flip the sign by cell. This note maps acquirable data for both sides. [FRAMING-SENSITIVE]

## What “net negative” would require

| Ledger | Must measure | Current repo status |
|--------|--------------|---------------------|
| Federal taxes paid | Income/payroll/CIT proxies by household cell | **SIPP donor rebuilt** — `acs_origin_household_federal_microsim_2023` (79 donor cells, 5 earnings bands) [SOURCE: infra build 2026-06-15] |
| Federal transfers out | SNAP, Medicaid, SSI, refundable credits | SIPP monthly amounts in `sipp_scenario_ledger_2024.csv`; MEPS Medicaid incidence in health bridge |
| State/local direct spend | Schools, Medicaid share, shelter, courts | **Stage5 integrated** — RPP, CMS state Medicaid, EL 2017-18, receiver cities → `origin_puma_household_stage5_context_2023` |
| Local congestion (non-budget) | Class size, shelter overflow, court delay | CBO qual [SOURCE: CBO 61256]; TRAC/EOIR partial |
| Offsets (mandatory disconfirmation) | GDP, federal revenue surge, capital taxes, native complementarity | CBO 60569 positive macro channel [SOURCE: immigration-claims-matrix-2026-04-11.md] |

**Verdict today:** Local-pressure heterogeneity is defensible; **scalar net negative is not**. [SOURCE: immigration-adversarial-review.md]

## Tier A — Acquired this pass (`stage5_net_negative/`)

| ID | Path | Use for cost test | Disconfirmation risk |
|----|------|-------------------|----------------------|
| `CMS_MEDICAID_FM` | `external/stage5_net_negative/cms/medicaid_financial_management.csv` | State Medicaid spend by service category | KFF: emergency Medicaid <1% of total; immigrants lower per-capita spend [SOURCE: https://www.kff.org/racial-equity-and-health-policy/key-facts-on-health-coverage-of-immigrants/] |
| `BEA_RPP` | `external/stage5_net_negative/bea/rpp_state_metro_2024.xlsx` | Deflate local costs; separate price level from burden | High-RPP places may be productivity/amenity, not welfare loss |
| `NCES_EL_1718` | `external/stage5_net_negative/nces/ccd_lea_141_1718_english_learners.zip` | District EL counts (historical anchor) | Current 2023-24 EL not in CCD file-tool — still a gap |
| `RECEIVER_CITY_COSTS` | `external/stage5_net_negative/receiver/receiver_city_migrant_costs.csv` | Assigned local shock ($B NYC/Chicago/Boston) | Not national; selection into receiver cities |

## Tier B — Already in stack, underused for cost ledger

| Dataset | Leverage |
|---------|----------|
| SIPP 2024 + MEPS HC-251 | **Highest** — federal microsim replaces income proxy |
| Census school finance + SAIPE + NCES LEA | District child intensity × spend per pupil |
| IRS SOI migration panel | Tax-base mobility context (not immigrant-specific) |
| CBO 60569 / 61256 PDFs | Official federal-positive vs state-local-negative split for surge |
| ITEP undocumented tax PDF | Tax offset (not spend) |
| EOIR case data (causal) | Court load — venue ≠ residence |
| CBP/OHSS encounters (causal) | Shock timing, not destination |

## Tier C — Acquire next (automatable or manual)

| Priority | Dataset | Source | Blocks |
|----------|---------|--------|--------|
| 1 | **SIPP federal microsim ingest** | Local `pu2024_csv.zip` | Pipe-delimited; needs donor-cell fix |
| 2 | **EDFacts FS141 / FS138 EL enrollment 2022-23** | https://eddataexpress.ed.gov/ | Interactive export; no stable curl |
| 3 | **Census ASL state-local finances** | census.gov gov-finances | 2022 zip URL moved — manual |
| 4 | **HUD CHAS Table 11** | huduser.gov | WAF |
| 5 | **HUD SAFMR** | huduser.gov | WAF |
| 6 | **USDA SNAP state participation** | fns.usda.gov | 403 on curl |
| 7 | **KFF State Health Facts exports** | kff.org | Interactive only |
| 8 | **CBO Emergency Medicaid tables** | cbo.gov | Extract from report |
| 9 | **TRAC backlog time series** | trac.syr.edu | Scrape / manual |
| 10 | **NAS 2017 fiscal impact tables** | NAP | Paywall / purchase for full PDF |
| 11 | **PSID** | psidonline.isr.umich.edu | Registration + Cloudflare |
| 12 | **IRS SOI individual PUF** | IRS | Restricted application |

## Tier D — Causal designs (not bulk download)

These **test** net-negative mechanisms rather than assume it:

1. **County panel 2018–2026** — QWI county + BPS permits + ACS exposure + shelter/HIC (causal `threshold/` partial)
2. **Receiver-node kill-test** — already run; Miami/NYC high synchronized pressure [SOURCE: immigration-receiver-node-kill-test-2026-04-23.md]
3. **Education bucket fiscal cells** — `<HS` foreign-born stock × state school spend × household child structure

## Execution order (if goal is defensible net-negative)

1. ~~Fix SIPP donor library~~ → `acs_origin_household_federal_microsim_2023` **done** [SOURCE: immigration-scenario-composition-2026-06-15.md]
2. ~~Join EL + school finance + RPP/Medicaid to origin×PUMA~~ → **stage5 + scenario ledger done**; EL still 2017-18 anchor
3. Add receiver-city costs to county-stage2 context for flagged nodes
4. Run **disconfirmation pass**: CBO macro offset + KFF Medicaid facts + Clemens/Colas-Sachs indirect fiscal papers
5. Only then publish cell-level “net fiscal balance” — never a single national scalar

## Setup

```bash
bash sources/immigration-fiscal/setup.sh          # includes stage5 via setup-net-negative.sh
bash sources/immigration-fiscal/build-context.sh      # warehouse stage1+2
```

Manual list: `sources/immigration-fiscal/data/external/stage5_net_negative/kff_refs/MANUAL_ACQUIRE.md`
